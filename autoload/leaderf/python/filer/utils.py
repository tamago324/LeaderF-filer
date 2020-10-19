#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from leaderf.utils import escQuote, lfCmd, lfEval

NO_CONTENT_MSG = " No content!"


def accessable(path):
    try:
        os.listdir(path)
        return True
    except PermissionError:
        return False


def invalid_line(line):
    return line in (".", NO_CONTENT_MSG, "")


def echo_cancel():
    lfCmd("redraw | echon ' Canceled.'")


def echo_error(msg):
    lfCmd(
        "echohl ErrorMsg | redraw | echon ' [LeaderF] {}' | echohl NONE".format(
            escQuote(msg)
        )
    )


def nearestAncestor(markers, path):
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


def cd(path):
    # XXX: from defx.nvim
    if lfEval("exists('*chdir')") == "1":
        lfCmd("call chdir('%s')" % path)
    else:
        lfCmd("silent execute (haslocaldir() ? 'lcd' : 'cd') '%s'" % path)
