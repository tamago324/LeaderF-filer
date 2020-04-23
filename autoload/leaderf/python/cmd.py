#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands
from commands import *

from utils import lfCmd


class Cmd:
    def __init__(self, manager):
        self._manager = manager
        self._command_names = set()

    def exec(self, cmd_name):
        return eval("command__" + cmd_name)(self._manager)

    @property
    def command_names(self):
        if len(self._command_names) == 0:
            self._command_names = {
                x[len("command__") :]
                for x in commands.__dir__()
                if x.startswith("command__")
            }
        return self._command_names
