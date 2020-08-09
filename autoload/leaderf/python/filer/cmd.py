#!/usr/bin/env python
# -*- coding: utf-8 -*-

import filer.commands
from filer.commands import *


class Cmd:
    def __init__(self, manager):
        self._manager = manager
        self._command_names = set()

    def execute_command(self, cmd_name):
        return eval("command__" + cmd_name)(self._manager)

    @property
    def command_names(self):
        if len(self._command_names) == 0:
            self._command_names = {
                x[len("command__") :]
                for x in dir(filer.commands)
                if x.startswith("command__")
            }
        return self._command_names

    def contains(self, cmd_name):
        return cmd_name in self.command_names
