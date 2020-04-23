#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Thanks ranger (https://github.com/ranger/ranger)
"""


class HistoryEmptyException(Exception):
    pass


class History(object):
    def __init__(self, maxlen=100):
        self.history = []
        self.index = 0
        self.maxlen = maxlen

    @property
    def current(self):
        if self.history:
            return self.history[self.index]
        else:
            raise HistoryEmptyException

    def add(self, item):
        # Delete back
        del self.history[self.index + 1 :]
        # If it is maxed out, delete the head
        if len(self.history) > max(self.maxlen - 1, 0):
            del self.history[0]
        self.history.append(item)
        self.index = len(self.history) - 1

    def backward(self):
        # 0 is the minimum
        self.index -= 1
        if self.index < 0:
            self.index = 0
        return self.current

    def forward(self):
        if self.history:
            self.index += 1
            # index is up to the number of history
            if self.index > len(self.history) - 1:
                self.index = len(self.history) - 1
        else:
            self.index = 0
        return self.current
