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
        self._contents = dict()

        contents = {
            f: {
                "isdir": os.path.isdir(os.path.join(self._cwd, f)),
                "fullpath": os.path.join(self._cwd, f),
            }
            for f in os.listdir(self._cwd)
        }

        for k, v in contents.items():
            if v["isdir"]:
                k += "/"
            self._contents[k] = v

        # . => current directory
        return ["."] + [f for f in self._contents.keys()]

    def getStlCategory(self):
        return "Filer"

    def getStlCurDir(self):
        return escQuote(lfEncode(self._cwd))


# *****************************************************
# FilerExplManager
# *****************************************************
class FilerExplManager(Manager):
    def __init__(self):
        super(FilerExplManager, self).__init__()

        # customize mapping
        # example:
        #   inoremap <C-H> <F9>
        key_dict = {"<C-H>": "<F9>", "<C-L>": "<F10>"}
        self._getInstance()._cli._key_dict.update(key_dict)

    def _getExplClass(self):
        return FilerExplorer

    def _defineMaps(self):
        lfCmd("call leaderf#Filer#Maps()")

    def _acceptSelection(self, *args, **kwargs):
        path = args[0]
        if path == ".":
            path = self._getExplorer()._cwd
        super(FilerExplManager, self)._acceptSelection(path, *args[1:], **kwargs)

    def _createHelp(self):
        help = []
        help.append('" <CR>/<double-click>/o : execute command under cursor')
        help.append('" i : switch to input mode')
        help.append('" q : quit')
        help.append('" <F1> : toggle this help')
        help.append('" ---------------------------------------------------------')
        return help

    def _cmdExtension(self, cmd):
        """
        this function can be overridden to add new cmd
        if return true, exit the input loop
        """
        if equal(cmd, "<F10>"):     # <C-H>
            self.down()
        elif equal(cmd, "<F9>"):    # <C-L>
            self.up()
        else:
            return True

    def _getDigest(self, line, mode):
        if not line:
            return ""

        return line

    def _getDigestStartPos(self, line, mode):
        return 0

    def _afterEnter(self):
        super(FilerExplManager, self)._afterEnter()
        if self._getInstance().getWinPos() == "popup":
            lfCmd(
                """call win_execute(%d, 'let matchid = matchadd(''Lf_hl_filerFile'', ''^[^\/]\+\(\/\)\@!$'')')"""
                % self._getInstance().getPopupWinId()
            )
            id = int(lfEval("matchid"))
            self._match_ids.append(id)
            lfCmd(
                """call win_execute(%d, 'let matchid = matchadd(''Lf_hl_filerDir'', ''^[^\/]\+\/$'')')"""
                % self._getInstance().getPopupWinId()
            )
            id = int(lfEval("matchid"))
            self._match_ids.append(id)
        else:
            id = int(lfEval("matchadd('Lf_hl_filerFile', '^[^\/]\+\(\/\)\@!$')"))
            self._match_ids.append(id)
            id = int(lfEval("matchadd('Lf_hl_filerDir', '^[^\/]\+\/$')"))
            self._match_ids.append(id)

    def down(self):
        line = self._getInstance().currentLine

        if line == ".":
            return

        file_info = self._getExplorer()._contents[line]
        if not file_info["isdir"]:
            # file
            # super(FilerExplManager, self)._acceptSelection()
            return

        abspath = os.path.abspath(file_info["fullpath"])
        self._getExplorer()._cwd = abspath
        self._refresh(cwd=abspath)

    def up(self):
        if len(self._getInstance()._cli._cmdline) > 0:
            self._refresh()
            return
        cwd = self._getExplorer()._cwd or os.getcwd()
        abspath = os.path.abspath(os.path.join(cwd, ".."))
        self._getExplorer()._cwd = abspath
        self._refresh(cwd=abspath)

    def _refresh(self, cwd=None):
        if cwd:
            self._getInstance().setStlCwd(cwd)

        # initialize like startExplorer()
        self._index = 0
        self._result_content = []
        self._cb_content = []

        # add history
        self._cli.writeHistory(self._getExplorer().getStlCategory())

        # clear input pattern
        self._getInstance()._cli.clear()
        self.refresh(normal_mode=False)


# *****************************************************
# filerExplManager is a singleton
# *****************************************************
filerExplManager = FilerExplManager()

__all__ = ["filerExplManager"]
