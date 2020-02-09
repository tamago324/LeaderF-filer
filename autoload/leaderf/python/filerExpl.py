#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
from leaderf.utils import *
from leaderf.explorer import *
from leaderf.manager import *

NO_CONTENT_MSG = ' No content!'

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
        self._show_hidden_files = lfEval("get(g:, 'Lf_FilerShowHiddenFiles', 0)") == "1"
        self._show_devicons = (
            lfEval("exists('*WebDevIconsGetFileTypeSymbol')") == "1"
            and lfEval("get(g:, 'Lf_FilerShowDevIcons', 0)") == "1"
        )

    def getContent(self, *args, **kwargs):
        if kwargs.get("arguments", {}).get("directory"):
            # from fileExpl.py
            _dir = kwargs.get("arguments", {}).get("directory")[0]
            _dir = os.path.expanduser(lfDecode(_dir))
            if os.path.exists(_dir):
                self._cwd = os.path.abspath(_dir)
            else:
                lfCmd(
                    "echohl ErrorMsg | redraw | echon "
                    "'Unknown directory `%s`' | echohl NONE" % _dir
                )
                return None
        else:
            self._cwd = os.getcwd()
        return self.getFreshContent()

    def getFreshContent(self, *args, **kwargs):
        self._contents = dict()

        contents = {
            lfEncode(f): {
                "isdir": os.path.isdir(os.path.join(self._cwd, f)),
                "fullpath": os.path.join(self._cwd, f),
            }
            for f in os.listdir(self._cwd)
        }

        # hide dotfiles
        if not self._show_hidden_files:
            contents = {k: v for k, v in contents.items() if not k.startswith(".")}

        for k, v in contents.items():
            if self._show_devicons:
                isdir = "1" if v["isdir"] else "0"
                icon = lfEval('WebDevIconsGetFileTypeSymbol("%s", %s)' % (k, isdir))
                k = icon + k
            if v["isdir"]:
                k += "/"
            self._contents[k] = v

        # Sort directories and files by each
        files = sorted([k for k, v in self._contents.items() if not v["isdir"]])
        dirs = sorted([k for k, v in self._contents.items() if v["isdir"]])

        if lfEval("get(g:, 'Lf_FilerShowCurrentDirDot', 0)") == "1":
            # . => current directory
            return ["."] + dirs + files
        else:
            if len(dirs + files) == 0:
                return [NO_CONTENT_MSG]
            return dirs + files

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
        key_dict = {"<C-H>": "<F9>", "<C-L>": "<F10>", "<C-F>": "<F8>", "<C-G>": "<F7>"}
        self._getInstance()._cli._key_dict.update(key_dict)

    def _getExplClass(self):
        return FilerExplorer

    def _defineMaps(self):
        lfCmd("call leaderf#Filer#Maps()")

    # XXX: better to use commands.
    # def accept(self, mode=''):
    #     instance = self._getInstance()
    #     line = instance.currentLine
    #     pattern = ''.join(instance._cli._cmdline)
    #
    #     if line == "":
    #         self._edit(pattern)
    #         return
    #
    #     super(FilerExplManager, self).accept(mode)

    def _acceptSelection(self, *args, **kwargs):
        path = args[0]
        if path == NO_CONTENT_MSG:
            return

        if path == ".":
            path = self._getExplorer()._cwd

        if self._getExplorer()._show_devicons:
            path = path[2:]

        if os.path.isabs(path):
            path = os.path.join(self._getInstance().getCwd(), lfDecode(path))
            path = os.path.normpath(lfEncode(path))

        if os.path.isdir(path):
            cmd = lfEval("get(g:, 'Lf_FilerAcceptDirSelectionCmd', 'lcd')")
            lfCmd("%s %s" % (cmd, escSpecial(path)))
            return

        super(FilerExplManager, self)._acceptSelection(path, *args[1:], **kwargs)

    def _createHelp(self):
        help = []
        help.append('" <CR>/<double-click>/o : execute command under cursor')
        help.append('" <TAB> : switch to input mode')
        help.append('" <C-h>/h : Show files in parent directory')
        help.append('" <C-l>/l : Show files in directory under cursor')
        help.append('" I : Toggle show hidden files')
        help.append('" <C-g> : Show files of directory where g:Lf_RootMarkers exists')
        help.append('" q : quit')
        help.append('" <F1> : toggle this help')
        help.append('" ---------------------------------------------------------')
        return help

    def _cmdExtension(self, cmd):
        """
        this function can be overridden to add new cmd
        if return true, exit the input loop
        """
        if equal(cmd, "<F10>"):  # <C-H>
            self.down()
        elif equal(cmd, "<F9>"):  # <C-L>
            self.up()
        elif equal(cmd, "<F8>"):  # <C-F>
            self.toggleHiddenFiles()
        elif equal(cmd, "<F7>"):  # <C-G>
            self.gotoRootMarkersDir()
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

            lfCmd(
                """call win_execute(%d, 'let matchid = matchadd(''Lf_hl_filerNoContent'', ''^%s$'')')"""
                % (self._getInstance().getPopupWinId(), NO_CONTENT_MSG)
            )
            id = int(lfEval("matchid"))
            self._match_ids.append(id)
        else:
            id = int(lfEval("matchadd('Lf_hl_filerFile', '^[^\/]\+\(\/\)\@!$')"))
            self._match_ids.append(id)
            id = int(lfEval("matchadd('Lf_hl_filerDir', '^[^\/]\+\/$')"))
            self._match_ids.append(id)
            id = int(lfEval("matchadd('Lf_hl_filerNoContent', '^%s$')" % NO_CONTENT_MSG))
            self._match_ids.append(id)

    def down(self):
        line = self._getInstance().currentLine

        if line in (".", NO_CONTENT_MSG):
            return

        file_info = self._getExplorer()._contents[line]
        if not file_info["isdir"]:
            # file
            # super(FilerExplManager, self)._acceptSelection()
            return

        if self._getInstance().isReverseOrder():
            lfCmd("normal! G")
        else:
            self._gotoFirstLine()

        self._chcwd(os.path.abspath(file_info["fullpath"]))

    def up(self):
        if len(self._getInstance()._cli._cmdline) > 0:
            self._refresh()
            return
        cwd = self._getExplorer()._cwd or os.getcwd()
        abspath = os.path.abspath(os.path.join(cwd, ".."))
        self._chcwd(abspath)

        if self._getExplorer()._show_devicons:
            dir_icon = lfEval('WebDevIconsGetFileTypeSymbol("", 1)')
            pattern = r'\v^{}{}/$'.format(dir_icon, os.path.basename(cwd))
        else:
            pattern = r'\v^{}/$'.format(os.path.basename(cwd))
        lfCmd("call search('%s')" % pattern)
        lfCmd('normal! 0')

    def toggleHiddenFiles(self):
        self._getExplorer()._show_hidden_files = (
            not self._getExplorer()._show_hidden_files
        )
        self.refresh(normal_mode=False)

    def gotoRootMarkersDir(self):
        root_markers = lfEval("g:Lf_RootMarkers")
        rootMarkersDir = self._nearestAncestor(
            root_markers, self._getInstance().getCwd()
        )
        if rootMarkersDir:
            # exists root_markers
            self._chcwd(os.path.abspath(rootMarkersDir))

    def cd(self, path):
        # XXX: from defx.nvim
        if lfEval("exists('*chdir')") == "1":
            lfCmd("call chdir('%s')" % path)
        else:
            lfCmd("silent execute (haslocaldir() ? 'lcd' : 'cd') '%s'" % path)

    def _refresh(self, cwd=None):
        if cwd:
            self._getInstance().setStlCwd(cwd)
            self._getInstance().setCwd(cwd)

        # initialize like startExplorer()
        self._index = 0
        self._result_content = []
        self._cb_content = []

        # add history
        self._cli.writeHistory(self._getExplorer().getStlCategory())

        # clear input pattern
        self._getInstance()._cli.clear()
        self.refresh(normal_mode=False)

    def _nearestAncestor(self, markers, path):
        """
        return the nearest ancestor path(including itself) of `path` that contains
        one of files or directories in `markers`.
        `markers` is a list of file or directory names.

        """
        # XXX: from LeaderF fileExpl.py
        if os.name == "nt":
            # e.g. C:\\
            root = os.path.splitdrive(os.path.abspath(path))[0] + os.sep
        else:
            root = "/"

        path = os.path.abspath(path)
        while path != root:
            for name in markers:
                if os.path.exists(os.path.join(path, name)):
                    return path
            path = os.path.abspath(os.path.join(path, ".."))

        for name in markers:
            if os.path.exists(os.path.join(path, name)):
                return path

        return ""

    # def _edit(self, name):
    #     path = os.path.join(self._getInstance().getCwd(), name)
    #     self._getInstance().exitBuffer()
    #     lfCmd('edit %s' % path)

    def _chcwd(self, path):
        self._getExplorer()._cwd = path
        self._refresh(cwd=path)
        if '--auto-cd' in self.getArguments():
            self.cd(path)


# *****************************************************
# filerExplManager is a singleton
# *****************************************************
filerExplManager = FilerExplManager()

__all__ = ["filerExplManager"]
