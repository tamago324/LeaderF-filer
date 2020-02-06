" ============================================================================
" File:        leaderf.vim
" Description:
" Author:      tamago324 <tamago_pad@yahoo.co.jp>
" Website:     https://github.com/tamago324
" Note:
" License:     Apache License, Version 2.0
" ============================================================================

" Definition of 'arguments' can be similar as
" https://github.com/Yggdroot/LeaderF/blob/master/autoload/leaderf/Any.vim#L85-L140
let s:extension = {
            \   "name": "filer",
            \   "help": "navigate the files in directory",
            \   "manager_id": "leaderf#Filer#managerId",
            \   "arguments": [
            \       {"name": ["directory"], "nargs": "?", "help": "show files under <directory>"},
            \       {"name": ["--auto-cd"], "nargs": "0", "help": "change the working directory while navigating with LeaderF-filer"},
            \   ]
            \ }

" In order that `Leaderf ghq` is available
call g:LfRegisterPythonExtension(s:extension.name, s:extension)

command! -bar -nargs=? -complete=dir LeaderfFiler Leaderf filer <args>

" In order to be listed by :LeaderfSelf
call g:LfRegisterSelf("LeaderfFiler", "navigate the files in directory")
