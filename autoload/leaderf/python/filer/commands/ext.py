#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from filer.help import _help
from filer.utils import cd, nearestAncestor
from leaderf.utils import lfCmd, lfEval


@_help.help("toggle show hidden files")
def command__toggle_hidden_files(manager):
    manager._getExplorer()._show_hidden_files = (
        not manager._getExplorer()._show_hidden_files
    )
    manager.refresh(normal_mode=False)


@_help.help("show files of directory where g:Lf_RootMarkers exists")
def command__goto_root_marker_dir(manager):
    root_markers = lfEval("g:Lf_RootMarkers")
    rootMarkersDir = nearestAncestor(root_markers, manager._getExplorer().cwd)
    if rootMarkersDir:
        # exists root_markers
        manager._chcwd(os.path.abspath(rootMarkersDir))


@_help.help("change the current directory to cwd of LeaderF-filer")
def command__change_directory(manager):
    cd(manager._getExplorer().cwd)
    lfCmd("redraw | echon ' cd {}'".format(manager._getExplorer().cwd))


@_help.help("go backwards in history")
def command__history_backward(manager):
    manager._chcwd(manager._history.backward())


@_help.help("go forwards in history")
def command__history_forward(manager):
    manager._chcwd(manager._history.forward())
