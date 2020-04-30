#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from filer.help import _help
from filer.utils import NO_CONTENT_MSG, accessable, echo_error
from leaderf.devicons import webDevIconsGetFileTypeSymbol
from leaderf.utils import lfCmd


@_help.help("open file/dir under cursor")
def command__open_current(manager):
    line = manager._getInstance().currentLine
    if line == NO_CONTENT_MSG:
        return
    if line == "":
        return

    file_info = manager._getExplorer()._contents[line]
    if not file_info["isdir"]:
        manager.accept()
        return True

    if not accessable(file_info["fullpath"]):
        echo_error("Permission denied `{}`".format(file_info["fullpath"]))
        return

    if manager._getInstance().isReverseOrder():
        lfCmd("normal! G")
    else:
        manager._gotoFirstLine()

    manager._chcwd(os.path.abspath(file_info["fullpath"]))
    manager._history.add(manager._getExplorer().cwd)


@_help.help("show files in parent directory")
def command__open_parent_or_clear_line(manager):
    if len(manager._getInstance()._cli._cmdline) > 0:
        manager._refresh()
        return
    manager._history.add(manager._getExplorer().cwd)
    _open_parent(manager)


@_help.help("show files in parent directory")
def command__open_parent_or_backspace(manager):
    if len(manager._getInstance()._cli._cmdline) > 0:
        # like <BS> in cli#input()
        manager._cli._backspace()
        manager._cli._buildPattern()

        # like <Shorten> in manager#input()
        cur_len = len(manager._content)
        cur_content = manager._content[:cur_len]
        manager._index = 0
        manager._search(cur_content)
        if manager._getInstance().isReverseOrder():
            lfCmd("normal! G")
        else:
            manager._gotoFirstLine()
        return
    manager._history.add(manager._getExplorer().cwd)
    _open_parent(manager)


@_help.help("show files in parent directory")
def command__open_parent(manager):
    manager._history.add(manager._getExplorer().cwd)
    _open_parent(manager)


def _open_parent(manager):
    cwd = manager._getExplorer().cwd or os.getcwd()
    abspath = os.path.abspath(os.path.join(cwd, ".."))
    manager._chcwd(abspath)
    manager._move_cursor_if_fullpath_match(cwd)
