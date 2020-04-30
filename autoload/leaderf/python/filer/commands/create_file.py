import os

from filer.commands.input import (
    input_prompt,
    restore_context,
    save_context,
    switch_normal_mode,
)
from filer.help import _help
from filer.utils import echo_cancel, echo_error
from leaderf.utils import lfEval


@_help.help("create a file")
def command__create_file(manager):
    if manager._instance.getWinPos() not in ("popup", "floatwin"):
        try:
            file_name = lfEval("input('Create file: ')")
        except KeyboardInterrupt:
            echo_cancel()
            return
        _create_file(manager, file_name)
    else:
        save_context(manager)
        # in popup
        input_prompt(manager, "create_file", "Create file: ")


def command___do_create_file(manager):
    file_name = manager._instance._cli.pattern
    try:
        _create_file(manager, file_name)
    finally:
        restore_context(manager, restore_input_pattern=False, restore_cursor_pos=False)
        switch_normal_mode(manager)


def _create_file(manager, file_name):
    if file_name == "":
        echo_cancel()
        return

    path = os.path.join(manager._getExplorer().cwd, file_name)
    if os.path.exists(path):
        echo_error(" Already exists. '{}'".format(path))
    else:
        # create file
        open(path, "w").close()

    if manager._instance.getWinPos() not in ("popup", "floatwin"):
        manager._refresh()
    else:
        manager._refresh(write_history=False, normal_mode=True)
    manager._move_cursor_if_fullpath_match(path)
