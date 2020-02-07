# LeaderF-filer

This Plugin use [LeaderF](https://github.com/Yggdroot/LeaderF) to navigate the files in directory.

Inspired by [vim-clap's filer provider](https://github.com/liuchengxu/vim-clap/pull/272), [helm's find-files](https://github.com/emacs-helm/helm).


Buffer

<img src="./images/buffer.png" alt="buffer" />

Popup Window

<img src="./images/popup.png" alt="popup" />

## Installation

```
Plug 'Yggdroot/LeaderF'
Plug 'tamago324/LeaderF-filer'

" optional
Plug 'ryanoasis/vim-devicons'
```

## Usage

```
:LeaderfFiler
```
or
```
:Leaderf filer
```

## Mappings

INSERT MODE:

| Key     | Action                                                                                            |
|---------|---------------------------------------------------------------------------------------------------|
| `<C-h>` | Show files in parent directory                                                                    |
| `<C-l>` | Show files in directory under cursor                                                              |
| `<C-f>` | Toggle show hidden files                                                                          |
| `<C-g>` | Show files of directory where `g:Lf_RootMarkers` exists                                           |
| `<CR>`  | Open the file under cursor or create a file with the input pattern file name (when empty results) |

NORMAL MODE:

| Key           | Action                                                                                            |
|---------------|---------------------------------------------------------------------------------------------------|
| `<C-h>` / `h` | Show files in parent directory                                                                    |
| `<C-l>` / `l` | Show files in directory under cursor                                                              |
| `I`           | Toggle show hidden files                                                                          |
| `<C-g>`       | Show files of directory where root marker exists                                                  |
| `I`           | Toggle show hidden files                                                                          |
| `<CR>` / `o`  | Open the file under cursor or create a file with the input pattern file name (when empty results) |


## Settings

Show icons.

```vim
" Plug 'ryanoasis/vim-devicons'
let g:Lf_FilerShowDevIcons = 1
```

## Screenshots

`Leaderf filer`

<img src="./images/buffer.png" alt="buffer" />

`Leaderf filer --popup`

<img src="./images/popup.png" alt="popup" />
