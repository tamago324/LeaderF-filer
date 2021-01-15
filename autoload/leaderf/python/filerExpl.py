#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import re

from filer.cmd import Cmd
from filer.help import _help
from filer.history import History
from filer.utils import NO_CONTENT_MSG, accessable, cd, echo_error
from leaderf.devicons import *
from leaderf.explorer import *
from leaderf.manager import *
from leaderf.utils import *

MODE_DICT = {"NORMAL": "", "COPY": "[COPY] "}


# *****************************************************
# FilerExplorer
# *****************************************************
class FilerExplorer(Explorer):
    def __init__(self):
        # filename: {
        #   "isdir": bool,
        #   "fullpath": str
        # }
        self._contents = dict()
        self._cwd = None
        self._show_hidden_files = lfEval("get(g:, 'Lf_FilerShowHiddenFiles', 0)") == "1"
        self._show_devicons = lfEval("get(g:, 'Lf_ShowDevIcons', 1)") == "1"
        # NORMAL or COPY
        self._command_mode = "NORMAL"
        self._prefix_length = 0

    def getContent(self, *args, **kwargs):
        self.cwd = self.cwd or os.getcwd()
        return self.getFreshContent()

    def getFreshContent(self, *args, **kwargs):
        self._contents = dict()

        contents = {
            lfEncode(f): {
                "isdir": os.path.isdir(os.path.join(self.cwd, f)),
                "fullpath": os.path.abspath(os.path.join(self.cwd, f)),
            }
            for f in os.listdir(self.cwd)
        }

        # hide dotfiles
        if not self._show_hidden_files:
            contents = {k: v for k, v in contents.items() if not k.startswith(".")}

        for k, v in contents.items():
            if self._show_devicons:
                icon = webDevIconsGetFileTypeSymbol(k, v["isdir"])
                k = icon + k
            if v["isdir"]:
                k += "/"
            self._contents[k] = v

        self._prefix_length = 0
        if self._show_devicons:
            self._prefix_length = webDevIconsStrLen()
            # Remove icon
            func = lambda x: x[self._prefix_length :]
        else:
            self._prefix_length = 0
            func = lambda x: x
        # Sort directories and files by each
        files = sorted(
            [k for k, v in self._contents.items() if not v["isdir"]], key=func
        )
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
        return MODE_DICT.get(self._command_mode, "") + escQuote(lfEncode(self.cwd))

    @property
    def cwd(self):
        return self._cwd

    @cwd.setter
    def cwd(self, cwd):
        self._cwd = cwd.replace("\\", "/")

    def supportsMulti(self):
        return True

    def setCommandMode(self, mode):
        """
        "NORMAL" or "COPY"
        """
        self._command_mode = mode

    def getPrefixLength(self):
        return self._prefix_length


# *****************************************************
# FilerExplManager
# *****************************************************
class FilerExplManager(Manager):
    def __init__(self):
        super(FilerExplManager, self).__init__()
        self._update_insert_maps()
        self._copy_file = ""
        self._copy_mode = False
        self._command = Cmd(self)
        self._history = History()

    def _update_insert_maps(self):
        insert_map = lfEval("leaderf#Filer#InsertMap()")
        maps = {key.upper(): cmd for key, cmd in insert_map.items()}
        self._getInstance()._cli._key_dict = maps

    def _getExplClass(self):
        return FilerExplorer

    def _defineMaps(self):
        lfCmd("call leaderf#Filer#Maps()")

    def accept(self, mode=""):
        instance = self._getInstance()
        line = instance.currentLine
        # instance._cli.pattern
        pattern = "".join(instance._cli._cmdline)

        if line in ("", NO_CONTENT_MSG):
            # edit (new file)
            path = os.path.join(self._getExplorer().cwd, pattern)
            self._getInstance().exitBuffer()
            lfCmd("edit %s" % path)
            return

        super(FilerExplManager, self).accept(mode)

    def _acceptSelection(self, *args, **kwargs):
        path = args[0]
        if path == NO_CONTENT_MSG:
            return

        if path == ".":
            path = self._getExplorer().cwd
        else:
            path = self._getDigest(path, 0)

        if not os.path.isabs(path):
            path = os.path.join(self._getExplorer().cwd, lfDecode(path))
            path = os.path.normpath(lfEncode(path))

        if os.path.isdir(path):
            cmd = lfEval("get(g:, 'Lf_FilerAcceptDirSelectionCmd', 'lcd')")
            lfCmd("%s %s" % (cmd, escSpecial(path)))
            return

        # from manager.py
        try:
            if kwargs.get("mode", "") != "t" or (
                lfEval("get(g:, 'Lf_DiscardEmptyBuffer', 0)") == "1"
                and len(vim.tabpages) == 1
                and len(vim.current.tabpage.windows) == 1
                and vim.current.buffer.name == ""
                and len(vim.current.buffer) == 1
                and vim.current.buffer[0] == ""
                and not vim.current.buffer.options["modified"]
            ):

                if vim.current.buffer.options["modified"]:
                    lfCmd("hide edit %s" % escSpecial(path))
                else:
                    lfCmd("edit %s" % escSpecial(path))
            else:
                lfCmd("tab drop %s" % escSpecial(path))
        except vim.error as e:  # E37
            lfPrintError(e)

    def _createHelp(self):
        return _help.help_list

    def do_command(self, cmd_name):
        if self._command.contains(cmd_name):
            return self._command.execute_command(cmd_name)
        else:
            echo_error("Not found command: {}".format(cmd_name))

    def _cmdExtension(self, cmd_name):
        """
        this function can be overridden to add new cmd
        if return true, exit the input loop
        """
        if self._command.contains(cmd_name):
            return self.do_command(cmd_name)
        elif equal(cmd_name, "nop"):
            pass

    def _getDigest(self, line, mode):
        if not line:
            return ""

        prefix_len = self._getExplorer().getPrefixLength()
        return line[prefix_len:]

    def _getDigestStartPos(self, line, mode):
        if self._getExplorer()._show_devicons:
            prefix_len = (
                self._getExplorer().getPrefixLength()
                - webDevIconsStrLen()
                + webDevIconsBytesLen()
            )
        else:
            prefix_len = self._getExplorer().getPrefixLength()
        return prefix_len

    def _beforeEnter(self):
        super(FilerExplManager, self)._beforeEnter()
        self._copy_file = ""
        self._copy_mode = False
        self._getExplorer().setCommandMode("NORMAL")

    def _afterEnter(self):
        super(FilerExplManager, self)._afterEnter()

        winid = None

        if self._getInstance().getWinPos() == "popup":
            lfCmd(
                r"""call win_execute(%d, 'let matchid = matchadd(''Lf_hl_filerFile'', ''^[^\/]\+\(\/\)\@!$'')')"""
                % self._getInstance().getPopupWinId()
            )
            id = int(lfEval("matchid"))
            self._match_ids.append(id)

            if lfEval("get(g:, 'Lf_FilerOnlyIconHighlight', 0)") == "1":
                lfCmd(
                    """call win_execute(%d, 'let matchid = matchadd(''Lf_hl_filerDir'', ''^%s'')')"""
                    % (
                        self._getInstance().getPopupWinId(),
                        webDevIconsGetFileTypeSymbol("", isdir=True),
                    )
                )
            else:
                lfCmd(
                    r"""call win_execute(%d, 'let matchid = matchadd(''Lf_hl_filerDir'', ''^[^\/]\+\/$'')')"""
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
            winid = self._getInstance().getPopupWinId()
        else:
            id = int(lfEval(r"matchadd('Lf_hl_filerFile', '^[^\/]\+\(\/\)\@!$')"))
            self._match_ids.append(id)

            if lfEval("get(g:, 'Lf_FilerOnlyIconHighlight', 0)") == "1":
                id = int(
                    lfEval(
                        "matchadd('Lf_hl_filerDir', '^%s')"
                        % webDevIconsGetFileTypeSymbol("", isdir=True)
                    )
                )
            else:
                id = int(lfEval(r"matchadd('Lf_hl_filerDir', '^[^\/]\+\/$')"))

            self._match_ids.append(id)

            id = int(
                lfEval("matchadd('Lf_hl_filerNoContent', '^%s$')" % NO_CONTENT_MSG)
            )
            self._match_ids.append(id)

        if lfEval("get(g:, 'Lf_FilerMoveCursorCufBuf', 0)") == "1":
            self._move_cursor_if_fullpath_match(self._cur_buffer.name)

        # devicons
        if self._getExplorer()._show_devicons:
            self._match_ids.extend(
                matchaddDevIconsExtension(r"^__icon__\ze\s\+\S\+\.__name__$", winid)
            )
            self._match_ids.extend(
                matchaddDevIconsExact(r"^__icon__\ze\s\+__name__$", winid)
            )
            self._match_ids.extend(matchaddDevIconsDefault(r"^__icon__", winid))

    def startExplorer(self, win_pos, *args, **kwargs):
        _dir = ""
        if kwargs.get("arguments", {}).get("directory"):
            _dir = kwargs.get("arguments", {}).get("directory")[0]
            # Get a quoted path
            # e,g,
            #   :Leaderf filer 'C:\Program Files'
            #   :Leaderf filer "C:\Program Files"
            m = re.match(r"""("[^"]+"|'[^']+')""", _dir)
            if m:
                _dir = m.groups()[0][1:-1]
            _dir = os.path.expanduser(lfDecode(_dir))
            _dir = os.path.expandvars(_dir)
            _dir = os.path.abspath(_dir)

            if not os.path.exists(_dir):
                echo_error("Unknown directory `{}`".format(_dir))
                return

            elif not accessable(_dir):
                echo_error("Permission denied `{}`".format(_dir))
                return

        _dir = _dir or os.getcwd()

        # Set vars because super().startExplorer() is calling self._getExplorer()
        self._getExplorer().cwd = _dir

        # To call _buildPrompt() in super().startExplorer()
        if lfEval("get(g:, 'Lf_FilerShowPromptPath', 0)") == "1":
            self._getInstance()._cli._additional_prompt_string = self._adjust_path(_dir)

        super(FilerExplManager, self).startExplorer(win_pos, *args, **kwargs)

        # super().startExplorer() updates cwd to os.getcwd()
        self._getInstance().setCwd(_dir)
        self._history.add(_dir)

    def _move_cursor(self, lnum):
        if self._getInstance().getWinPos() == "popup":
            lfCmd(
                """call win_execute({}, 'normal! {}G')""".format(
                    self._getInstance().getPopupWinId(), lnum
                )
            )
            lfCmd(
                """call win_execute(%d, "let cursor_pos = getcurpos()[1:2]")"""
                % (self._getInstance()._popup_winid)
            )
        else:
            lfCmd("normal! {}G".format(lnum))
            lfCmd("normal! 0")
        self._getInstance().mimicCursor()

    def _move_cursor_if_fullpath_match(self, path):
        """
        Move the cursor to the line where fullpath matches path.
        """
        for line, info in self._getExplorer()._contents.items():
            if info["fullpath"] == os.path.abspath(path):
                if line in self._content:
                    lnum = self._content.index(line)
                    if self._instance._reverse_order:
                        # Reverse the position.
                        lnum = len(self._content) - lnum
                    else:
                        lnum += 1
                    self._move_cursor(lnum)
                    break

    def _refresh(self, cwd=None, write_history=True, normal_mode=False):
        if cwd:
            if self._copy_mode:
                # update status line
                self._redrawStlCwd()
            else:
                self._redrawStlCwd(cwd)

            self._getInstance().setCwd(cwd)

        # initialize like startExplorer()
        self._index = 0
        self._result_content = []
        self._cb_content = []

        # add history
        if write_history:
            self._cli.writeHistory(self._getExplorer().getStlCategory())

        # clear input pattern
        self._getInstance()._cli.clear()
        self.refresh(normal_mode=normal_mode)
        if lfEval("get(g:, 'Lf_FilerShowPromptPath', 0)") == "1":
            self._getInstance()._cli._additional_prompt_string = self._adjust_path(
                self._getExplorer().cwd
            )
        self._getInstance()._cli._buildPrompt()

    def _chcwd(self, path, write_history=True, normal_mode=False):
        self._getExplorer().cwd = path
        self._refresh(cwd=path, write_history=write_history, normal_mode=normal_mode)
        if "--auto-cd" in self.getArguments():
            cd(path)

    def _previewInPopup(self, *args, **kwargs):
        if len(args) == 0:
            return

        line = args[0]
        if line == "." or line[-1] == "/":
            return

        file = self._getDigest(line, 0)
        file = os.path.join(self._getInstance().getCwd(), lfDecode(file))
        file = os.path.normpath(lfEncode(file))
        buf_number = int(lfEval("bufadd('%s')" % escQuote(file)))
        lfCmd("echomsg '{}'".format(file))
        self._createPopupPreview(file, buf_number, 0)

    def _redrawStlCwd(self, cwd=None):
        if cwd is None:
            self._getInstance().setStlCwd(self._getExplorer().getStlCurDir())
        else:
            self._getInstance().setStlCwd(cwd.replace("\\", "/"))

        if self._getInstance().getWinPos() in ("popup", "floatwin"):
            self._getInstance().setPopupStl(self._current_mode)
            self._getInstance().refreshPopupStatusline()

    def _adjust_path(self, path):
        if os.name == "nt":
            path = path.replace("\\", "/")
            if len(path) == 3:
                return path
        else:
            if path == "/":
                return path
        path = lfEval("pathshorten('{}')".format(path))
        return path + "/"


# *****************************************************
# filerExplManager is a singleton
# *****************************************************
filerExplManager = FilerExplManager()

__all__ = ["filerExplManager"]
