#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
from leaderf.utils import *
from leaderf.explorer import *
from leaderf.manager import *


# *****************************************************
# FilerExplorer
# *****************************************************
class FilerExplorer(Explorer):
    def __init__(self):
        # filename: {
        #   "isdir": ディレクトリかどうか,
        #   "fullpath": パス
        # }
        self._contents = dict()
        self._cwd = None

    def getContent(self, *args, **kwargs):
        # because it is singleton
        self._cwd = None
        return self.getFreshContent()

    def getFreshContent(self, *args, **kwargs):
        self._cwd = self._cwd or os.getcwd()

        self._contents = {
            f: {
                "isdir": os.path.isdir(os.path.join(self._cwd, f)),
                "fullpath": os.path.join(self._cwd, f),
            }
            for f in os.listdir(self._cwd)
        }

        # . => current directory
        return ["."] + [f for f in self._contents.keys()]

    def getStlCategory(self):
        return "Filer"

    def getStlCurDir(self):
        return escQuote(lfEncode(self._cwd))

    def supportsNameOnly(self):
        return True


# *****************************************************
# FilerExplManager
# *****************************************************
class FilerExplManager(Manager):
    def __init__(self):
        super(FilerExplManager, self).__init__()

    def _getExplClass(self):
        return FilerExplorer

    def _defineMaps(self):
        lfCmd("call leaderf#Filer#Maps()")

    def _acceptSelection(self, *args, **kwargs):
        pass

    def _createHelp(self):
        help = []
        help.append('" <CR>/<double-click>/o : execute command under cursor')
        help.append('" i : switch to input mode')
        help.append('" q : quit')
        help.append('" <F1> : toggle this help')
        help.append('" ---------------------------------------------------------')
        return help

    def _cmdExtension(self, cmd):
        # XXX: category ごとにマッピングできるようにしたいな...
        if equal(cmd, '<C-y>'):
            self.down()
        if equal(cmd, '<C-g>'):
            self.up()
        return True

    def down(self):
        line = self._getInstance().currentLine

        if line == ".":
            return

        file_info = self._getExplorer()._contents[line]
        if not file_info['isdir']:
            # file
            # super(FilerExplManager, self)._acceptSelection()
            return

        self._getExplorer()._cwd = os.path.abspath(file_info["fullpath"])
        self._refresh()

    def up(self):
        if len(self._getInstance()._cli._cmdline) > 0:
            self._refresh()
            return
        cwd = self._getExplorer()._cwd or os.getcwd()
        self._getExplorer()._cwd = os.path.abspath(os.path.join(cwd, '..'))
        self._refresh()

    def _refresh(self):
        # initialize like startExplorer()
        self._index = 0
        self._result_content = []
        self._cb_content = []

        # clear input pattern
        self._getInstance()._cli.clear()
        # is not work normal_mode??
        self.refresh()
        self.input()


# *****************************************************
# filerExplManager is a singleton
# *****************************************************
filerExplManager = FilerExplManager()

__all__ = ["filerExplManager"]
