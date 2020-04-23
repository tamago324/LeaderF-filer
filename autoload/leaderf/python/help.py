#!/usr/bin/env python
# -*- coding: utf-8 -*-


from leaderf.utils import lfEval


class HelpText:
    def __init__(self):
        self._help_text_list = []
        self._help_dict = dict()

    def help(self, text):
        def decorator(func):
            def inner_func(*args, **kwargs):
                return func(*args, **kwargs)

            self._help_dict[func.__name__.replace("command__", "")] = text
            return inner_func

        return decorator

    @property
    def help_list(self):
        if self._help_text_list:
            return self._help_text_list

        help = []
        key_cmd_dict = dict()
        for [key, cmd_name] in lfEval("leaderf#Filer#NormalMap()").items():
            key_cmd_dict[cmd_name] = key_cmd_dict.get(cmd_name, []) + [key]

        # sort key
        for [key, val] in key_cmd_dict.items():
            key_cmd_dict[key] = sorted(val)

        for [name, text] in self._help_dict.items():
            if name in key_cmd_dict:
                # key1/key2 : help text
                line = '" {} : {}'.format("/".join(key_cmd_dict[name]), text)
                help.append(line)
        help.sort()
        help.append('" ---------------------------------------------------------')

        self._help_text_list = help
        return help


_help = HelpText()
