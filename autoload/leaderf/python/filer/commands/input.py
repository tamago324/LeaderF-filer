#!/usr/bin/env python
# -*- coding: utf-8 -*-

from leaderf.utils import lfCmd

_switch_normal_mode_key = ""
_context = {}
# search_func
# additional_prompt_string
# cli_key_dict
# cli_cmdline
# cli_cursor_pos
# cli_pattern
# cursor_pos
# results
# input_prompt_prompts
# input_prompt_command


def command___input_cancel(manager):
    _restore_context(manager)
    _switch_normal_mode(manager)


def command___input_prompt(manager):
    global _context
    prompts = _context["input_prompt_prompts"]
    command = _context["input_prompt_command"]

    # Chains the input prompt
    # Save the previous input value.
    if "results" not in _context:
        _context["results"] = []
    _context["results"].append(manager._instance._cli.pattern)

    _context["input_prompt_prompts"] = prompts[1:]

    # reset prompt text
    prompt = prompts[0].get("prompt")
    text = prompts[0].get("text", "")
    manager._instance._cli._additional_prompt_string = prompt
    manager._instance._cli.setPattern(text)

    key_dict = manager._instance._cli._key_dict
    if len(prompts) == 1:
        # done
        key_dict["<CR>"] = "_do_" + command
    else:
        key_dict["<CR>"] = "_input_prompt"
    manager._instance._cli._key_dict = key_dict


def input_prompt(manager, command, prompts=[]):
    """
    params:
        command:
            "delete" or "edit" or ("add")
            When <CR> is pressed, manager.command___co_{command}() is executed.
        prompts:
            input prompts
            [
                {"prompt": prompt1, "text": text1},
                ...
            ]
    """
    global _context
    _context["input_prompt_prompts"] = prompts[1:]
    _context["input_prompt_command"] = command

    # set pattern
    prompt = prompts[0].get("prompt", "")
    text = prompts[0].get("text", "")
    manager._instance._cli._additional_prompt_string = prompt
    manager._instance._cli.setPattern(text)

    # update key_dict
    key_dict = {
        lhs: rhs
        for [lhs, rhs] in manager._instance._cli._key_dict.items()
        if rhs.lower()
        in {
            "<esc>",
            "<c-c>",
            "<bs>",
            "<c-h>",
            "<c-u>",
            "<c-w>",
            "<del>",
            "<c-v>",
            "<s-insert>",
            "<home>",
            "<c-b>",
            "<end>",
            "<c-e>",
            "<left>",
            "<right>",
            "<up>",
            "<down>",
            "open_parent_or_backspace",
            "open_parent_or_clear_line",
        }
    }

    # To be able to do general input
    for [lrs, rhs] in key_dict.items():
        rhs_low = rhs.lower()
        if rhs_low in {"open_parent_or_backspace", "open_parent_or_clear_line"}:
            key_dict[lrs] = "<BS>"
        elif rhs_low in {"<esc>", "<c-c>"}:
            key_dict[lrs] = "_input_cancel"
    # add command
    if len(prompts) == 1:
        key_dict["<CR>"] = "_do_" + command
    else:
        # chain
        key_dict["<CR>"] = "_input_prompt"
    manager._instance._cli._key_dict = key_dict
    manager.input()


def do_command(func):
    """
        example:
            @do_command
            def command___do_xxx(manager, context, results):
                ...
    """
    # Give a list of input results to a function
    def inner_func(manager):
        # The first argument must be manager
        global _context
        results = _context.get("results", [])
        results.append(manager._instance._cli.pattern)

        try:
            func(manager, _context, results)
        finally:
            _restore_context(
                manager, restore_input_pattern=False, restore_cursor_pos=False
            )
            _switch_normal_mode(manager)
            manager._instance._cli.setPattern("")

    return inner_func


def save_context(manager, **kwargs):
    """ For input_prompt
    """
    global _context
    _context = {}
    _context["search_func"] = manager._search
    _context[
        "additional_prompt_string"
    ] = manager._instance._cli._additional_prompt_string
    _context["cli_key_dict"] = dict(manager._instance._cli._key_dict)
    _context["cli_cmdline"] = list(manager._instance._cli._cmdline)
    _context["cli_cursor_pos"] = manager._instance._cli._cursor_pos
    _context["cli_pattern"] = manager._instance._cli._pattern
    _context["cursor_pos"] = manager._getInstance()._window_object.cursor
    _context.update(**kwargs)

    manager._search = lambda content, is_continue=False, step=0: ""


def _restore_context(manager, restore_input_pattern=True, restore_cursor_pos=True):
    """ For input_prompt

    params:
        restore_input_pattern:
            The following attributes of the `cli` will not be restored
            * _cmdline
            * _cursor_pos
            * _pattern
        restore_cursor_pos:
            cursor position
    """
    global _context
    manager._search = _context["search_func"]
    manager._instance._cli._additional_prompt_string = _context[
        "additional_prompt_string"
    ]
    manager._instance._cli._key_dict = _context["cli_key_dict"]
    if restore_cursor_pos:
        # To restore only in case of cancel
        [row, col] = _context["cursor_pos"]
        lfCmd(
            """call win_execute({}, 'exec "norm! {}G"')""".format(
                manager._instance._popup_winid, row
            )
        )
        manager._getInstance().refreshPopupStatusline()
    if restore_input_pattern:
        # To restore only in case of cancel
        manager._instance._cli._cmdline = _context["cli_cmdline"]
        manager._instance._cli._cursor_pos = _context["cli_cursor_pos"]
        manager._instance._cli._pattern = _context["cli_pattern"]
    _context = {}


def _switch_normal_mode(manager):
    lfCmd(r'call feedkeys("{}", "n")'.format(_get_switch_normal_mode_key(manager)))


def _get_switch_normal_mode_key(manager):
    """ Returns the key to go into normal mode.
    """
    global _switch_normal_mode_key
    if _switch_normal_mode_key:
        return _switch_normal_mode_key

    keys = [
        lrs
        for [lrs, rhs] in manager._instance._cli._key_dict.items()
        if rhs.lower() == "<tab>"
    ]
    if len(keys) == 0:
        _switch_normal_mode_key = r"\<Tab>"
    else:
        # <Tab> => \<Tab>
        _switch_normal_mode_key = keys[0].replace("<", r"\<")
    return _switch_normal_mode_key
