# LeaderF-filer

This Plugin use [LeaderF](https://github.com/Yggdroot/LeaderF) to navigate the files in directory.

Inspired by [vim-clap's filer provider](https://github.com/liuchengxu/vim-clap/pull/272), [helm's find-files](https://github.com/emacs-helm/helm).

<p align="center">
  <img src="https://github.com/tamago324/images/blob/master/leaderf_filer/leaderf-filer.gif" alt="leaderf-filer-gif" width="700" style=""/>
</p>

## Installation

```
Plug 'Yggdroot/LeaderF'
Plug 'tamago324/LeaderF-filer'
```

If you use `remove_trash` and `remove_trash_force`, you need [Send2Trash](https://pypi.org/project/Send2Trash/).

## Usage

```
:Leaderf filer
:Leaderf filer --popup
```

## Screenshots

`:Leaderf filer`

<img src="https://github.com/tamago324/images/blob/master/leaderf_filer/buffer.png" alt="buffer" />

`:Leaderf filer --popup`

<img src="https://github.com/tamago324/images/blob/master/leaderf_filer/popup.png" alt="popup" />

`let g:Lf_FilerShowPromptPath = 1`

<img src="https://github.com/tamago324/images/blob/master/leaderf_filer/popup_show_path.png" alt="popup-show-path-in-prompt" />

## Mappings

### Insert mode


| Mapping                     | Command                   | Description                                                                                             |
|-----------------------------|---------------------------|---------------------------------------------------------------------------------------------------------|
|                             | nop                       | Does nothing like `<Nop>`.                                                                              |
| `<Esc>` <br> `<C-c>`        | quit                      | Quit from LeaderF.                                                                                      |
| `<C-k>`                     | up                        | move the cursor downward in the result window.                                                          |
| `<C-j>`                     | down                      | move the cursor upward in the result window.                                                            |
| `<CR>` <br> `<2-LeftMouse>` | accept                    | Open the file under cursor or create a file with the input pattern file name (when empty results).      |
| `<C-x>`                     | accept_horizontal         | Open the file under cursor in horizontal split window.                                                  |
| `<C-]>`                     | accept_vertical           | Open the file under cursor in vertical split window.                                                    |
| `<C-t>`                     | accept_tab                | Open the file under cursor new tabpage.                                                                 |
| `<C-s>`                     | add_selections            | select multiple result.                                                                                 |
| `<C-a>`                     | select_all                | select all result.                                                                                      |
| `<F3>`                      | clear_selections          | clear all selections.                                                                                   |
| `<C-p>`                     | preview                   | Preview the result.                                                                                     |
| `<C-Up>`                    | page_up_in_preview        | Scroll up in the popup preview window.                                                                  |
| `<C-Down>`                  | page_down_in_preview      | Scroll down in the popup preview window.                                                                |
|                             | close_preview_popup       | Close popup preview window.                                                                             |
|                             | open_parent               | The prompt string is cleared and show files files in the parent directory.                              |
| `<C-l>`                     | open_current              | Show files in directory under cursor or open the file under the cursor.                                 |
| `<C-f>`                     | toggle_hidden_files       | Toggle show hidden files.                                                                               |
| `<C-g>`                     | goto_root_marker_dir      | Show files of directory where `g:Lf_RootMarkers` exists.                                                |
|                             | change_directory          | Change the current directory to cwd of LeaderF-filer.                                                   |
|                             |                           |                                                                                                         |
| `<C-r>`                     | toggle_regex              | Switch between fuzzy search mode and regex mode.                                                        |
| `<Tab>`                     | switch_normal_mode        | Switch to normal mode.                                                                                  |
|                             | open_parent_or_backspace  | Show files in parent directory or delete the preceding character in the prompt if a pattern wasentered. |
| `<C-h>`                     | open_parent_or_clear_line | Show files in parent directory or clears the prompt if a pattern was entered.                           |
| `<C-v>` <br> `<S-Insert>`   | paste                     | Paste from clipboard.                                                                                   |
| `<C-u>`                     | clear_line                | Clear the prompt.                                                                                       |
| `<C-w>`                     | delete_left_word          | Delete the word before the cursor in the prompt.                                                        |
| `<Up>`                      | prev_history              | Recall last input pattern from history.                                                                 |
| `<Down>`                    | next_history              | Recall next input pattern from history.                                                                 |
| `<BS>`                      | backspace                 | Delete the preceding character in the prompt.                                                           |
| `<Del>`                     | delete                    | Delete the current character in the prompt.                                                             |
| `<C-a>` <br> `<Home>`       | home                      | Move the cursor to the begin of the prompt.                                                             |
| `<C-e>` <br> `<End>`        | end                       | Move the cursor to the end of the prompt.                                                               |
| `<Left>`                    | left                      | Move the cursor one character to the left.                                                              |
| `<Right>`                   | right                     | Move the cursor one character to the right.                                                             |


### Normal mode

You can view help in F1.

| Mapping                              | Command              | Description                                                                                        |
|--------------------------------------|----------------------|----------------------------------------------------------------------------------------------------|
|                                      | nop                  | Does nothing like `<Nop>`.                                                                         |
| `q`                                  | quit                 | Quit from LeaderF.                                                                                 |
| `<Up>`                               | up                   | move the cursor downward in the result window.                                                     |
| `<Down>`                             | down                 | move the cursor upward in the result window.                                                       |
| `o` <br> `<CR>` <br> `<2-LeftMouse>` | accept               | Open the file under cursor or create a file with the input pattern file name (when empty results). |
| `x`                                  | accept_horizontal    | Open the file under cursor in horizontal split window.                                             |
| `v`                                  | accept_vertical      | Open the file under cursor in vertical split window.                                               |
| `t`                                  | accept_tab           | Open the file under cursor new tabpage.                                                            |
| `s`                                  | add_selections       | select multiple result.                                                                            |
| `a`                                  | select_all           | select all result.                                                                                 |
| `c`                                  | clear_selections     | clear all selections.                                                                              |
| `p`                                  | preview              | Preview the result.                                                                                |
| `<C-Up>`                             | page_up_in_preview   | Scroll up in the popup preview window.                                                             |
| `<C-Down>`                           | page_down_in_preview | Scroll down in the popup preview window.                                                           |
| `<Esc>`                              | close_preview_popup  | Close popup preview window.                                                                        |
| `h` <br> `<C-h>`                     | open_parent          | The prompt string is cleared and show files files in the parent directory.                         |
| `l` <br> `<C-l>`                     | open_current         | Show files in directory under cursor or open the file under the cursor.                            |
| `I`                                  | toggle_hidden_files  | Toggle show hidden files.                                                                          |
| `<C-g>`                              | goto_root_marker_dir | Show files of directory where `g:Lf_RootMarkers` exists.                                           |
| `@`                                  | change_directory     | Change the current directory to cwd of LeaderF-filer.                                              |
|                                      |                      |                                                                                                    |
| `<F1>`                               | toggle_help          | Toggle this help.                                                                                  |
| `<Tab>`                              | switch_insert_mode   | Switch to insert mode.                                                                             |
| `H`                                  | history_backward     | Go backwards in history.                                                                           |
| `L`                                  | history_forward      | Go forwards in history.                                                                            |
| `K`                                  | mkdir                | Create a directory.<br> See `g:Lf_FilerMkdirAutoChdir`                                             |
| `O`                                  | create_file          | Create a file.                                                                                     |
| `R`                                  | rename               | Rename files and directories.                                                                      |
| `C`                                  | copy                 | Copy files and directories under cursor.                                                           |
| `P`                                  | paste                | Paste the file or directory copied by the copy command to cwd of LeaderF-filer.                    |
|                                      | remove               | Remove files.                                                                                      |
|                                      | remove_force         | Remove files without confirmation.                                                                 |
|                                      | remove_trash         | Remove files and put in the trash.                                                                 |
|                                      | remove_trash_force   | Remove files and put in the trash without confirmation.                                            |



## Credit

* LeaderF-filer uses some code from [defx.nvim](https://github.com/Shougo/defx.nvim), [ranger](https://github.com/ranger/ranger).
* Thanks [Send2Trash](https://pypi.org/project/Send2Trash/).

## License

Apache-2.0
