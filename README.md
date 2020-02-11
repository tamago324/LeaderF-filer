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

## Mappings

see `:h LeaderF-filer-mapping`

### Show devicons

```vim
" Plug 'ryanoasis/vim-devicons'
let g:Lf_FilerShowDevIcons = 1
```

## Screenshots

`:Leaderf filer`

<img src="./images/buffer.png" alt="buffer" />

`:Leaderf filer --popup`

<img src="./images/popup.png" alt="popup" />
