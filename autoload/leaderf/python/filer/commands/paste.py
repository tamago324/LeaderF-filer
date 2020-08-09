#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

from filer.help import _help
from filer.utils import echo_error
from leaderf.utils import lfCmd


@_help.help("paste the file or directory")
def command__paste(manager):
    if not manager._copy_mode:
        return

    fullpath = manager._copy_file
    basename = os.path.basename(fullpath)

    cwd = manager._getExplorer().cwd

    to_path = os.path.join(cwd, basename)

    if os.path.exists(to_path):
        name, ext = os.path.splitext(basename)
        to_path = os.path.join(cwd, "{}_copy{}".format(name, ext))

    # *_copy があったら、だめ
    if os.path.exists(to_path):
        echo_error(" Already exists. '{}'".format(to_path.replace("\\", "/")))
        manager._refresh()
        return

    if os.path.isdir(fullpath):
        # shutil.copytree(src, dst)
        shutil.copytree(fullpath, to_path)
    else:
        shutil.copy2(fullpath, to_path)

    manager._refresh()
    manager._move_cursor_if_fullpath_match(to_path)
    lfCmd("redraw | echon ' Pasted.'")
