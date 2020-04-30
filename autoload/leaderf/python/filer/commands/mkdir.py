#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from filer.commands.input import do_command, input_prompt, save_context
from filer.help import _help
from filer.utils import cd, echo_cancel, echo_error
from leaderf.utils import lfEval


@_help.help("create a directory")
def command__mkdir(manager):
    # For dir completion
    save_cwd = lfEval("getcwd()")
    cd(manager._getExplorer().cwd)
    save_context(manager, **{"save_cwd": save_cwd})
    input_prompt(manager, "mkdir", [{"prompt": "Create directory: "}])


@do_command
def command___do_mkdir(manager, context, results):
    dir_name = results[0]
    if dir_name == "":
        echo_cancel()
        return

    path = os.path.join(manager._getExplorer().cwd, dir_name)
    if os.path.exists(os.path.join(manager._getExplorer().cwd, dir_name)):
        echo_error(" Already exists. '{}'".format(path.replace("\\", "/")))
        return

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
