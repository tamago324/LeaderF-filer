import os
from commands.input import (
    get_context,
    input_prompt,
    restore_context,
    save_context,
    switch_normal_mode,
)

from help import _help
from leaderf.utils import lfCmd, lfEval, lfPrintError
from utils import echo_cancel, invalid_line


@_help.help("rename files and directories")
def command__rename(manager):
    line = manager._instance.currentLine
    if len(manager._selections) > 0:
        lfPrintError(" Rename does not support multiple files.")
        return

    if invalid_line(line):
        return

    from_path = manager._getExplorer()._contents[line]["fullpath"]
    basename = os.path.basename(from_path)

    if manager._instance.getWinPos() not in ("popup", "floatwin"):
        try:
            renamed = lfEval("input('Rename: ', '{}')".format(basename))
        except KeyboardInterrupt:  # Cancel
            echo_cancel()
            return

        _rename(manager, from_path, renamed, basename)
        lfCmd("redraw")
    else:
        save_context(manager, **{"from_path": from_path, "basename": basename})
        # in popup
        input_prompt(manager, "rename", "Rename: ", basename)


def command___do_rename(manager):
    renamed = manager._instance._cli.pattern
    try:
        _rename(
            manager, get_context()["from_path"], renamed, get_context()["basename"],
        )
    finally:
        restore_context(manager, restore_input_pattern=False, restore_cursor_pos=False)
        switch_normal_mode(manager)


def _rename(manager, from_path, renamed, basename):
    if renamed == "":
        echo_cancel()
        return

    if renamed == basename:
        return

    to_path = os.path.join(os.path.dirname(from_path), renamed)

    if os.path.exists(to_path):
        lfPrintError(" Already exists. '{}'".format(to_path))
        return

    os.rename(from_path, to_path)

    if manager._instance.getWinPos() not in ("popup", "floatwin"):
        manager._refresh()
    else:
        manager._refresh(write_history=False, normal_mode=True)
    manager._move_cursor_if_fullpath_match(to_path)
