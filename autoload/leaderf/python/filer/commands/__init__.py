#!/usr/bin/env python
# -*- coding: utf-8 -*-

from commands.basic import *
from commands.copy import *
from commands.create_file import command___do_create_file, command__create_file
from commands.ext import *
from commands.input import command___input_cancel
from commands.mkdir import command___do_mkdir, command__mkdir
from commands.open import (
    command__open_current,
    command__open_parent,
    command__open_parent_or_backspace,
    command__open_parent_or_clear_line,
)
from commands.paste import *
from commands.remove import (
    command___do_remove,
    command__remove,
    command__remove_force,
    command__remove_trash,
    command__remove_trash_force,
)
from commands.rename import command___do_rename, command__rename
