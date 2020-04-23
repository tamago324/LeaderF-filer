#!/usr/bin/env python
# -*- coding: utf-8 -*-

from help import _help
from leaderf.utils import lfCmd, lfEval


@_help.help("move the cursor upward")
def command__down(self):
    lfCmd("normal! j")
    self._previewResult(False)


@_help.help("move the cursor downward")
def command__up(self):
    lfCmd("normal! k")
    self._previewResult(False)


# def _page_up(self):
#     lfCmd('normal! <PageUp>')
#     self._previewResult(False)

# def _page_down(self):
#     lfCmd('normal! <PageDown>')
#     self._previewResult(False)

# def _left_mouse(self):
#     lfCmd('normal! <LeftMouse>')
#     self._previewResult(False)


@_help.help("preview the result")
def command__preview(self):
    self._previewResult(True)


@_help.help("toggle this help")
def command__toggle_help(self):
    self.toggleHelp()


@_help.help("quit")
def command__quit(self):
    self.quit()


@_help.help("switch to input mode")
def command__switch_insert_mode(self):
    self.input()


@_help.help("open the file under cursor")
def command__accept(self):
    self.accept()


@_help.help("open the file under cursor in horizontal split window")
def command__accept_horizontal(self):
    self.accept("h")


@_help.help("open the file under cursor in vertical split window")
def command__accept_vertical(self):
    self.accept("v")


@_help.help("open the file under cursor new tabpage")
def command__accept_tab(self):
    self.accept("t")


@_help.help("scroll up in the popup preview window (nvim only)")
def command__page_up_in_preview(self):
    if lfEval("has('nvim')"):
        self._toUpInPopup()


@_help.help("scroll down in the popup preview window (nvim only)")
def command__page_down_in_preview(self):
    if lfEval("has('nvim')"):
        self._toDownInPopup()


@_help.help("close popup preview window (nvim only)")
def command__close_preview_popup(self):
    if lfEval("has('nvim')"):
        self._closePreviewPopup()


@_help.help("select multiple result")
def command__add_selections(self):
    self.addSelections()


@_help.help("select all result")
def command__select_all(self):
    self.selectAll()


@_help.help("clear all selections")
def command__clear_selections(self):
    self.clearSelections()
