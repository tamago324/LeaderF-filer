#!/usr/bin/env python
# -*- coding: utf-8 -*-

from filer.help import _help
from leaderf.utils import lfCmd, lfEval


@_help.help("move the cursor upward")
def command__down(manager):
    lfCmd("normal! j")
    manager._previewResult(False)


@_help.help("move the cursor downward")
def command__up(manager):
    lfCmd("normal! k")
    manager._previewResult(False)


# def _page_up(manager):
#     lfCmd('normal! <PageUp>')
#     manager._previewResult(False)

# def _page_down(manager):
#     lfCmd('normal! <PageDown>')
#     manager._previewResult(False)

# def _left_mouse(manager):
#     lfCmd('normal! <LeftMouse>')
#     manager._previewResult(False)


@_help.help("preview the result")
def command__preview(manager):
    manager._previewResult(True)


@_help.help("toggle this help")
def command__toggle_help(manager):
    manager.toggleHelp()


@_help.help("quit")
def command__quit(manager):
    manager.quit()


@_help.help("switch to input mode")
def command__switch_insert_mode(manager):
    manager.input()


@_help.help("open the file under cursor")
def command__accept(manager):
    manager.accept()


@_help.help("open the file under cursor in horizontal split window")
def command__accept_horizontal(manager):
    manager.accept("h")


@_help.help("open the file under cursor in vertical split window")
def command__accept_vertical(manager):
    manager.accept("v")


@_help.help("open the file under cursor new tabpage")
def command__accept_tab(manager):
    manager.accept("t")


@_help.help("scroll up in the popup preview window (nvim only)")
def command__page_up_in_preview(manager):
    if lfEval("has('nvim')"):
        manager._toUpInPopup()


@_help.help("scroll down in the popup preview window (nvim only)")
def command__page_down_in_preview(manager):
    if lfEval("has('nvim')"):
        manager._toDownInPopup()


@_help.help("close popup preview window (nvim only)")
def command__close_preview_popup(manager):
    if lfEval("has('nvim')"):
        manager._closePreviewPopup()


@_help.help("select multiple result")
def command__add_selections(manager):
    manager.addSelections()


@_help.help("select all result")
def command__select_all(manager):
    manager.selectAll()


@_help.help("clear all selections")
def command__clear_selections(manager):
    manager.clearSelections()
