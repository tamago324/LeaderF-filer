#!/usr/bin/env python
# -*- coding: utf-8 -*-

from help import _help
from leaderf.utils import lfCmd, lfPrintError
from utils import invalid_line


@_help.help("copy files and directories under cursor")
def command__copy(manager):
    if len(manager._selections) > 0:
        lfPrintError(" Copy does not support multiple files.")
        return

    line = manager._getInstance().currentLine
    if invalid_line(line):
        return

    manager._copy_file = manager._getExplorer()._contents[line]["fullpath"]
    manager._copy_mode = True
    lfCmd("echon ' Copied.'")
    # Updat estatus line
    manager._getExplorer().setCommandMode("COPY")
    manager._redrawStlCwd()
