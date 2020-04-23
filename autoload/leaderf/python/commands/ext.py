#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from help import _help
from leaderf.utils import lfCmd, lfEval
from utils import cd, nearestAncestor


@_help.help("toggle show hidden files")
def command__toggle_hidden_files(self):
    self._getExplorer()._show_hidden_files = not self._getExplorer()._show_hidden_files
    self.refresh(normal_mode=False)


@_help.help("show files of directory where g:Lf_RootMarkers exists")
def command__goto_root_marker_dir(self):
    root_markers = lfEval("g:Lf_RootMarkers")
    rootMarkersDir = nearestAncestor(root_markers, self._getExplorer().cwd)
    if rootMarkersDir:
        # exists root_markers
        self._chcwd(os.path.abspath(rootMarkersDir))


@_help.help("change the current directory to cwd of LeaderF-filer")
def command__change_directory(self):
    cd(self._getExplorer().cwd)
    lfCmd("echon ' cd {}'".format(self._getExplorer().cwd))


@_help.help("go backwards in history")
def command__history_backward(self):
    self._chcwd(self._history.backward())


@_help.help("go forwards in history")
def command__history_forward(self):
    self._chcwd(self._history.forward())
