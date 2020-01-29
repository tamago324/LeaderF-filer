" ============================================================================
" File:        Filer.vim
" Description:
" Author:      tamago324 <tamago_pad@yahoo.co.jp>
" Website:     https://github.com/tamago324
" Note:
" License:     Apache License, Version 2.0
" ============================================================================

if leaderf#versionCheck() == 0
    finish
endif

exec g:Lf_py "import vim, sys, os.path"
exec g:Lf_py "cwd = vim.eval('expand(\"<sfile>:p:h\")')"
exec g:Lf_py "sys.path.insert(0, os.path.join(cwd, 'python'))"
exec g:Lf_py "from filerExpl import *"

function! leaderf#Filer#Maps()
    nmapclear <buffer>
    " nnoremap <buffer> <silent> <CR>          :exec g:Lf_py "filerExplManager.accept()"<CR>
    " nnoremap <buffer> <silent> o             :exec g:Lf_py "filerExplManager.accept()"<CR>
    " nnoremap <buffer> <silent> <2-LeftMouse> :exec g:Lf_py "filerExplManager.accept()"<CR>
    nnoremap <buffer> <silent> q             :exec g:Lf_py "filerExplManager.quit()"<CR>
    nnoremap <buffer> <silent> <Tab>         :exec g:Lf_py "filerExplManager.input()"<CR>
    nnoremap <buffer> <silent> <F1>          :exec g:Lf_py "filerExplManager.toggleHelp()"<CR>
    if has_key(g:Lf_NormalMap, "Filer")
        for i in g:Lf_NormalMap["Filer"]
            exec 'nnoremap <buffer> <silent> '.i[0].' '.i[1]
        endfor
    endif
endfunction

function! leaderf#Filer#managerId()
    " pyxeval() has bug
    if g:Lf_PythonVersion == 2
        return pyeval("id(filerExplManager)")
    else
        return py3eval("id(filerExplManager)")
    endif
endfunction

function! leaderf#Filer#NormalModeFilter(winid, key) abort
    let key = get(g:Lf_KeyDict, get(g:Lf_KeyMap, a:key, a:key), a:key)

    if key !=# "g"
        call win_execute(a:winid, "let g:Lf_Filer_is_g_pressed = 0")
    endif

    if key ==# "j" || key ==? "<Down>"
        call win_execute(a:winid, "norm! j")
        exec g:Lf_py "filerExplManager._cli._buildPopupPrompt()"
        "redraw
        exec g:Lf_py "filerExplManager._getInstance().refreshPopupStatusline()"
    elseif key ==# "k" || key ==? "<Up>"
        call win_execute(a:winid, "norm! k")
        exec g:Lf_py "filerExplManager._cli._buildPopupPrompt()"
        "redraw
        exec g:Lf_py "filerExplManager._getInstance().refreshPopupStatusline()"
    elseif key ==? "<PageUp>" || key ==? "<C-B>"
        call win_execute(a:winid, "norm! \<PageUp>")
        exec g:Lf_py "filerExplManager._cli._buildPopupPrompt()"
        exec g:Lf_py "filerExplManager._getInstance().refreshPopupStatusline()"
    elseif key ==? "<PageDown>" || key ==? "<C-F>"
        call win_execute(a:winid, "norm! \<PageDown>")
        exec g:Lf_py "filerExplManager._cli._buildPopupPrompt()"
        exec g:Lf_py "filerExplManager._getInstance().refreshPopupStatusline()"
    elseif key ==# "g"
        if get(g:, "Lf_Filer_is_g_pressed", 0) == 0
            let g:Lf_Filer_is_g_pressed = 1
        else
            let g:Lf_Filer_is_g_pressed = 0
            call win_execute(a:winid, "norm! gg")
            exec g:Lf_py "filerExplManager._cli._buildPopupPrompt()"
            redraw
        endif
    elseif key ==# "G"
        call win_execute(a:winid, "norm! G")
        exec g:Lf_py "filerExplManager._cli._buildPopupPrompt()"
        redraw
    elseif key ==? "<C-U>"
        call win_execute(a:winid, "norm! \<C-U>")
        exec g:Lf_py "filerExplManager._cli._buildPopupPrompt()"
        redraw
    elseif key ==? "<C-D>"
        call win_execute(a:winid, "norm! \<C-D>")
        exec g:Lf_py "filerExplManager._cli._buildPopupPrompt()"
        redraw
    elseif key ==? "<LeftMouse>"
        if has('patch-8.1.2266')
            call win_execute(a:winid, "exec v:mouse_lnum")
            call win_execute(a:winid, "exec 'norm!'.v:mouse_col.'|'")
            exec g:Lf_py "filerExplManager._cli._buildPopupPrompt()"
            redraw
        endif
    elseif key ==? "<ScrollWheelUp>"
        call win_execute(a:winid, "norm! 3k")
        exec g:Lf_py "filerExplManager._cli._buildPopupPrompt()"
        redraw
        exec g:Lf_py "filerExplManager._getInstance().refreshPopupStatusline()"
    elseif key ==? "<ScrollWheelDown>"
        call win_execute(a:winid, "norm! 3j")
        exec g:Lf_py "filerExplManager._cli._buildPopupPrompt()"
        redraw
        exec g:Lf_py "filerExplManager._getInstance().refreshPopupStatusline()"
    elseif key ==# "q" || key ==? "<ESC>"
        exec g:Lf_py "filerExplManager.quit()"
    elseif key ==# "i" || key ==? "<Tab>"
        call leaderf#ResetPopupOptions(a:winid, 'filter', 'leaderf#PopupFilter')
        exec g:Lf_py "filerExplManager.input()"
    elseif key ==# "o" || key ==? "<CR>" || key ==? "<2-LeftMouse>"
        exec g:Lf_py "filerExplManager.accept()"
    elseif key ==? "<F1>"
        exec g:Lf_py "filerExplManager.toggleHelp()"
    endif

    return 1
endfunction
