#!/usr/bin/env python
# -*- coding: utf-8 -*-

from filer.commands.basic import *
from filer.commands.copy import *
from filer.commands.create_file import command___do_create_file, command__create_file
from filer.commands.ext import *
from filer.commands.input import command___input_cancel
from filer.commands.mkdir import command___do_mkdir, command__mkdir
from filer.commands.open import (
    command__open_current,
    command__open_parent,
    command__open_parent_or_backspace,
    command__open_parent_or_clear_line,
)
from filer.commands.paste import *
from filer.commands.remove import (
    command___do_remove,
    command__remove,
    command__remove_force,
    command__remove_trash,
    command__remove_trash_force,
)
from filer.commands.rename import command___do_rename, command__rename
