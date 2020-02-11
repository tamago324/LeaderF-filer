# LeaderF-filer

This Plugin use [LeaderF](https://github.com/Yggdroot/LeaderF) to navigate the files in directory.

Inspired by [vim-clap's filer provider](https://github.com/liuchengxu/vim-clap/pull/272), [helm's find-files](https://github.com/emacs-helm/helm).


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

Popup

```
:Leaderf filer --popup
```

## Configuration

see `:h LeaderF-filer-mapping`

### Example

```vim
" ====================
" show devicons
" ====================
call plug#begin('~/vimfiles/plugged')

Plug 'Yggdroot/LeaderF'
Plug 'tamago324/LeaderF-filer'
Plug 'ryanoasis/vim-devicons'

call plug#end()

let g:Lf_FilerShowDevIcons = 1

" ====================
" customize mappings
" ====================

" Default value 1
let g:Lf_FilerNormalMap = 1

let g:Lf_FilerNormalMap = {
\   '<C-h>': 'nop',
\   '<C-l>': 'nop',
\   'i':     'switch_insert_mode',
\   'I':     'nop',
\   '.':     'toggle_hidden_files',
\   '<C-g>': 'nop',
\   '~':     'goto_root_marker_dir',
\}
```

## Screenshots

`:Leaderf filer`

<img src="./images/buffer.png" alt="buffer" />

`:Leaderf filer --popup`

<img src="./images/popup.png" alt="popup" />
