#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from commands.input import (
    get_context,
    input_prompt,
    restore_context,
    save_context,
    switch_normal_mode,
)

from help import _help
from leaderf.utils import lfEval, lfCmd
from utils import cd, echo_cancel, echo_error


@_help.help("create a directory")
def command__mkdir(manager):
    # For dir completion
    save_cwd = lfEval("getcwd()")
    cd(manager._getExplorer().cwd)

    if manager._instance.getWinPos() not in ("popup", "floatwin"):
        try:
            dir_name = lfEval("input('Create Directory: ', '', 'dir')")
        except KeyboardInterrupt:  # Cancel
            echo_cancel()
            return
        finally:
            # restore
            cd(save_cwd)
        _mkdir(manager, dir_name)
    else:
        save_context(manager, **{"save_cwd": save_cwd})
        # in popup
        input_prompt(manager, "mkdir", "Create directory: ")


def command___do_mkdir(manager):
    """
    private
    """
    dir_name = manager._instance._cli.pattern
    try:
        _mkdir(manager, dir_name)
    finally:
        cd(get_context()["save_cwd"])
        # restore cwd
        restore_context(manager, restore_input_pattern=False, restore_cursor_pos=False)
        switch_normal_mode(manager)


def _mkdir(manager, dir_name):
    if dir_name == "":
        echo_cancel()
        return

    path = os.path.join(manager._getExplorer().cwd, dir_name)
    if os.path.isdir(os.path.join(manager._getExplorer().cwd, dir_name)):
        echo_error(" Already exists. '{}'".format(path))
    else:
        os.makedirs(path)

    if manager._instance.getWinPos() not in ("popup", "floatwin"):
        if lfEval("get(g:, 'Lf_FilerMkdirAutoChdir', 0)") == "1":
            manager._chcwd(path)
        else:
            manager._refresh()
    else:
        if lfEval("get(g:, 'Lf_FilerMkdirAutoChdir', 0)") == "1":
            manager._chcwd(path, write_history=False, normal_mode=True)
        else:
            manager._refresh(write_history=False, normal_mode=True)

    manager._move_cursor_if_fullpath_match(path)
