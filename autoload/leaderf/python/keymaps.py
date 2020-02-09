#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from leaderf.utils import *


class KeyMaps(object):
    def __init__(self, custom_map):
        """
        custom_map = {
                "<C-H>": 'open_parent',
                "<C-L>": 'open_current',
            }
        """

        # { 'open_parent': ["<C-H>", <function object>] }
        self._commands = {}

        # { '<C-H>': "open_parent" }
        self._custom_maps = {
            k.upper(): func_name for k, func_name in custom_map.items()
        }
        self._maps = {}

    def updateKeyDict(self, cli):
        cli._key_dict.update(self.getMaps())

    def getMaps(self):
        return self._custom_maps or self._maps

    def command(self, name, default_key):
        """
        usage:
            @command(name="open_parent", default_key="<C-H>")
            def goto_parent(self):
                ...
        """

        def decorator(func):
            def inner_func(*args, **kwargs):
                return func(args, kwargs)

            # { 'open_parent': <function object> }
            self._commands[name] = func

            return inner_func

        # { "<C-H>": "open_parent" }
        self._maps[default_key.upper()] = name
        return decorator

    def doCommand(self, name, *args, **kwargs):
        self._commands[name](args, kwargs)

    def setSelf(self, instance):
        self._commands = {
            name: partial(func, instance) for name, func in self._commands.items()
        }
