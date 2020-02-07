#!/usr/bin/env python
# -*- coding: utf-8 -*-

from leaderf.utils import *


class KeyMaps(object):
    def __init__(self, keymap_dict, custom_map):
        """
        params:
            keymap_dict = {
                "<C-H>": ["goto_parent", "<F10>"],
                "<C-L>": ["goto_child", "<F9>"],
                "<C-F>": ["toggle_hidden_files", "<F8>"],
                "<C-G>": ["goto_root_marker_dir", "<F7>"],
            }
            keymap_dict = {
                "lhs": ["funcname", "rhs"],
            }

        vaiables:
        """
        self._maps = {}

        # self._default_map = {
        #     "<C-H>": "goto_parent",
        #     "<C-L>": "goto_child",
        #     "<C-F>": "toggle_hidden_files",
        #     "<C-G>": "goto_root_marker_dir",
        # }
        self._default_map = {k.upper(): v[0] for k, v in keymap_dict.items()}

        # self._func_key_dict = {
        #     "goto_parent": "<F10>",
        #     "goto_child": "<F9>",
        #     "toggle_hidden_files": "<F8>",
        #     "goto_root_marker_dir": "<F7>",
        # }
        self._func_key_dict = {item[0]: item[1] for item in keymap_dict.values()}

        self._setup(custom_map)

    def _setup(self, custom_map):
        if custom_map == {}:
            key_func_dict = self._default_map
        else:
            key_func_dict = custom_map

        self._maps = {}
        for key, func in key_func_dict.items():
            if func in self._func_key_dict.keys():
                self._maps[key] = self._func_key_dict[func]

    def updateKeyDict(self, cli):
        cli._key_dict.update(self._maps)

    def getMaps(self):
        """
        Returns a dictionary like:
            {
                "<C-H>": "<F10>",
                "<C-L>": "<F9>",
                "<C-F>": "<F8>",
                "<C-G>": "<F7>",
            }
        """
        return self._maps

    def getFuncKeyDict(self):
        """
        Returns a dictionary like:
            {
                "goto_parent": "<F10>",
                "goto_child": "<F9>",
                "toggle_hidden_files": "<F8>",
                "goto_root_marker_dir": "<F7>",
            }
        """
        return self._func_key_dict
