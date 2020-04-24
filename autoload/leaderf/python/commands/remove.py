#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import shutil
from commands.input import (command___input_cancel, get_context, input_prompt,
                            restore_context, save_context, switch_normal_mode)

from help import _help
from leaderf.utils import lfCmd, lfEval
from utils import NO_CONTENT_MSG, echo_cancel, echo_error


@_help.help("remove files")
def command__remove(manager):
    """
    remove
    """
    cmd_remove(manager, _remove)


@_help.help("remove files without confirmation")
def command__remove_force(manager):
    """
    remove_force
    """
    path_list = get_path_list(manager)
    if NO_CONTENT_MSG in path_list:
        return
    _remove(manager, path_list)
    lfCmd("redraw")
    return


@_help.help("remove files and put in the trash")
def command__remove_trash(manager):
    """
    remove_trash
    """
    cmd_remove(manager, _remove_trash)


@_help.help("remove files and put in the trash without confirmation")
def command__remove_trash_force(manager):
    """
    remove_trash_force
    """
    path_list = get_path_list(manager)
    if NO_CONTENT_MSG in path_list:
        return
    _remove_trash(manager, path_list)
    lfCmd("redraw")
    return


def command___do_remove(manager):
    result = manager._instance._cli.pattern
    if not yes(result):
        command___input_cancel(manager)
        return

    ctx = get_context()
    try:
        remove = ctx["remove_func"]
        remove(manager, ctx["path_list"])
    finally:
        restore_context(manager, restore_input_pattern=False, restore_cursor_pos=False)
        switch_normal_mode(manager)


def cmd_remove(manager, remove_func):
    path_list = get_path_list(manager)
    file_cnt = "" if len(path_list) == 1 else len(path_list)

    if NO_CONTENT_MSG in path_list:
        return

    if manager._instance.getWinPos() not in ("popup", "floatwin"):
        try:
            # confirm
            result = lfEval("input('Remove {}files? Y[es]/n[o]: ')".format(file_cnt))
        except KeyboardInterrupt:  # Cancel
            echo_cancel()
            return

        if not yes(result):
            echo_cancel()
            return

        remove_func(manager, path_list)
        lfCmd("redraw")
    else:
        save_context(manager, **{"path_list": path_list, "remove_func": remove_func})
        # confirm
        input_prompt(manager, "remove", "Remove {}files? Y[es]/n[o]: ".format(file_cnt))


def get_path_list(manager):
    if len(manager._selections.keys()) == 0:
        path_list = [
            manager._getExplorer()._contents[manager._instance.currentLine]["fullpath"]
        ]
    else:
        path_list = [
            manager._getExplorer()._contents[line]["fullpath"]
            for line in [
                # content line
                manager._instance._buffer_object[lnum - 1]
                for lnum in manager._selections.keys()
            ]
            # remove "."
            if line != "."
        ]
    return path_list


def _remove(manager, path_list):
    for path in path_list:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    if manager._instance.getWinPos() not in ("popup", "floatwin"):
        manager._refresh()
    else:
        manager._refresh(write_history=False, normal_mode=True)


def _remove_trash(manager, path_list):
    try:
        import send2trash
    except ImportError:
        echo_error('"Send2Trash" is not installed')
        return
    for path in path_list:
        send2trash.send2trash(path)

    if manager._instance.getWinPos() not in ("popup", "floatwin"):
        manager._refresh()
    else:
        manager._refresh(write_history=False, normal_mode=True)


def yes(result):
    if result == "":
        result = "y"
    return re.search(r"^[yY](e?s?)?$", result)
