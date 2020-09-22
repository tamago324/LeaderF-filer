"""
from BurntSushi/ripgrep/crates/ignore/src/gitignore.rs
"""
import os
import re
from os.path import join

RE_EXCLUDESFILE = re.compile(
    r"^\s*excludesfile\s*=\s*(.+)\s*$", re.IGNORECASE | re.MULTILINE
)


def _expand(p):
    p = os.path.expanduser(p)
    return os.path.abspath(p)


def gitconfig_excludes_path():
    """
    Return file path for global .gitignore file
    """
    lines = _gitconfig_home_contents()
    if lines:
        return _expand(_parse_exclude_file(lines))

    lines = _gitconfig_xdg_contents()
    if lines:
        return _expand(_parse_exclude_file(lines))

    return _expand(_exclude_file_default())


def _gitconfig_home_contents():
    """
    Returns the file contents of git's global config file, if one exists,
    in the user's home directory.
    """
    home = os.environ.get("HOME")
    if home is None:
        return None

    # $HOME/.gitconfig
    gitconfig = join(home, ".gitconfig")
    if os.path.exists(gitconfig):
        with open(gitconfig, "r", encoding="utf-8") as f:
            lines = "\n".join(f.readlines())
        return lines
    return None


def _gitconfig_xdg_contents():
    path = os.environ.get("XDG_CONFIG_HOME")
    if path is None:
        home = os.environ.get("HOME")
        path = join(home, ".config")
    else:
        return None

    # $XDG_CONFIG_HOME/git/config
    # $HOME/.config/git/config
    gitconfig = join(join(path, "git"), "config")
    if os.path.exists(gitconfig):
        with open(gitconfig, "r", encoding="utf-8") as f:
            lines = "\n".join(f.readlines())
        return lines
    return None


def _exclude_file_default():
    """
    Default file path for global .gitignore file
    """
    path = os.environ.get("XDG_CONFIG_HOME")
    if path is None:
        home = os.environ.get("HOME")
        path = join(home, ".config")
    # $XDG_CONFIG_HOME/git/ignore
    # $HOME/.config/git/ignore
    return join(join(path, "git"), "ignore")


def _parse_exclude_file(lines):
    m = RE_EXCLUDESFILE.findall(lines)
    if m:
        return m[0]
    return None
