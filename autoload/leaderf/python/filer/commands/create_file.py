import os

from filer.commands.input import do_command, input_prompt, save_context
from filer.help import _help
from filer.utils import echo_cancel, echo_error


@_help.help("create a file")
def command__create_file(manager):
    save_context(manager)
    input_prompt(manager, "create_file", [{"prompt": "Create file: "}])


@do_command
def command___do_create_file(manager, context, results):
    file_name = results[0]
    if file_name == "":
        echo_cancel()
        return

    path = os.path.join(manager._getExplorer().cwd, file_name)
    if os.path.exists(path):
        echo_error(" Already exists. '{}'".format(path.replace("\\", "/")))
        return

    open(path, "w").close()

    if manager._instance.getWinPos() not in ("popup", "floatwin"):
        manager._refresh()
    else:
        manager._refresh(write_history=False, normal_mode=True)
    manager._move_cursor_if_fullpath_match(path)
