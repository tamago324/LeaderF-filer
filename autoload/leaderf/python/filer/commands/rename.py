import os

from filer.commands.input import do_command, input_prompt, save_context
from filer.help import _help
from filer.utils import echo_cancel, echo_error, invalid_line
from leaderf.utils import lfEval


@_help.help("rename files and directories")
def command__rename(manager):
    line = manager._instance.currentLine
    if len(manager._selections) > 0:
        echo_error(" Rename does not support multiple files.")
        return

    if invalid_line(line):
        return

    from_path = manager._getExplorer()._contents[line]["fullpath"]
    basename = os.path.basename(from_path)

    save_context(manager, **{"from_path": from_path, "basename": basename})
    input_prompt(manager, "rename", [{"prompt": "Rename: ", "text": basename}])


@do_command
def command___do_rename(manager, context, results):
    renamed = results[0]
    if renamed == "":
        echo_cancel()
        return

    if renamed == context["basename"]:
        return

    to_path = os.path.join(os.path.dirname(context["from_path"]), renamed)

    if os.path.exists(to_path):
        echo_error(" Already exists. '{}'".format(to_path.replace("\\", "/")))
        return

    os.rename(context["from_path"], to_path)

    if manager._instance.getWinPos() not in ("popup", "floatwin"):
        manager._refresh()
    else:
        manager._refresh(write_history=False, normal_mode=True)
    manager._move_cursor_if_fullpath_match(to_path)
