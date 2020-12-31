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
exec g:Lf_py "from leaderf.utils import *"

function! leaderf#Filer#NormalMap() abort
    let l:default_map = {}
    if get(g:, 'Lf_FilerUseDefaultNormalMap', v:true)
        let l:default_map = {
        \   '<C-g>':         'goto_root_marker_dir',
        \   '<C-h>':         'toggle_hidden_files',
        \   'j':             'down',
        \   'k':             'up',
        \   '<Down>':        'down',
        \   '<Up>':          'up',
        \   '<F1>':          'toggle_help',
        \   '<Tab>':         'switch_insert_mode',
        \   'p':             'preview',
        \   'q':             'quit',
        \   '<CR>':          'open_current',
        \   's':             'accept_horizontal',
        \   'v':             'accept_vertical',
        \   't':             'accept_tab',
        \   '<Pageup>':      'page_up_in_preview',
        \   '<Pagedown>':    'page_down_in_preview',
        \   '<Esc>':         'close_preview_popup',
        \   '<Space>':       'add_selections',
        \   'a':             'select_all',
        \   'c':             'clear_selections',
        \   'K':             'mkdir',
        \   'C':             'copy',
        \   'P':             'paste',
        \   'R':             'rename',
        \   'O':             'create_file',
        \   '@':             'change_directory',
        \}
    endif
    return extend(l:default_map, get(g:, 'Lf_FilerNormalMap', {}))
endfunction

let s:normal_map = leaderf#Filer#NormalMap()

function! leaderf#Filer#Maps()
    exec g:Lf_py "from filerExpl import *"
    nmapclear <buffer>
    for [l:key, l:cmd] in items(s:normal_map)
        if l:cmd ==? 'nop'
            exec printf('nnoremap <buffer> <silent> %s <Nop>', l:key)
        endif
        exec printf('nnoremap <buffer> <silent> %s :exec g:Lf_py "filerExplManager.do_command(''%s'')"<CR>', l:key, l:cmd)
    endfor

    if has_key(g:Lf_NormalMap, 'Filer')
        for i in g:Lf_NormalMap['Filer']
            exec 'nnoremap <buffer> <silent> '.i[0].' '.i[1]
        endfor
    endif
endfunction

function! leaderf#Filer#InsertMap() abort
    let l:default_map = {}
    if get(g:, 'Lf_FilerUseDefaultInsertMap', v:true)
        let l:default_map = {
        \   '<C-h>':        'toggle_hidden_files',
        \   '<C-g>':        'goto_root_marker_dir',
        \   '<Esc>':        'quit',
        \   '<CR>':         'open_current',
        \   '<C-r>':        'toggle_regex',
        \   '<BS>':         'backspace',
        \   '<Del>':        'delete',
        \   '<C-v>':        'paste',
        \   '<Home>':       'home',
        \   '<C-b>':        'home',
        \   '<End>':        'end',
        \   '<C-e>':        'end',
        \   '<Left>':       'left',
        \   '<Right>':      'right',
        \   '<Down>':       'down',
        \   '<Up>':         'up',
        \   '<Tab>':        'switch_normal_mode',
        \   '<Pageup>':     'page_up_in_preview',
        \   '<Pagedown>':   'page_down_in_preview',
        \}
    endif

    let l:custom_map = extend(l:default_map, get(g:, 'Lf_FilerInsertMap', {}))

    " from cli.py
    let l:cli_map = {
    \   'quit': '<Esc>',
    \   'accept': '<CR>',
    \   'toggle_regex': '<C-r>',
    \   'backspace': '<BS>',
    \   'delete': '<Del>',
    \   'paste': '<C-v>',
    \   'home': '<Home>',
    \   'end': '<End>',
    \   'left': '<Left>',
    \   'right': '<Right>',
    \   'up': '<Up>',
    \   'down': '<Down>',
    \   'switch_normal_mode': '<Tab>',
    \   'page_up_in_preview': '<Pageup>',
    \   'page_down_in_preview': '<Pagedown>',
    \}

    " { '<C-e>': 'end' } => { '<C-e>': '<End>' }
    let l:ret = {}
    for [l:key, l:cmd] in items(l:custom_map)
        if has_key(l:cli_map, l:cmd)
            let l:ret[toupper(l:key)] = l:cli_map[l:cmd]
        else
            let l:ret[toupper(l:key)] = l:cmd
        endif
    endfor

    return l:ret
endfunction

function! leaderf#Filer#managerId()
    exec g:Lf_py "from filerExpl import *"
    " pyxeval() has bug
    if g:Lf_PythonVersion == 2
        return pyeval("id(filerExplManager)")
    else
        return py3eval("id(filerExplManager)")
    endif
endfunction

function! leaderf#Filer#NormalModeFilter(winid, key) abort
    exec g:Lf_py "from filerExpl import *"
    " Converted to uppercase just in case
    let l:key = get(g:Lf_KeyMap, a:key, a:key)
    let l:cmd = get(s:normal_map, l:key, '')

    if l:key !=# "g"
        call win_execute(a:winid, "let g:Lf_Filer_is_g_pressed = 0")
    endif

    if l:cmd ==? "down"  || l:key ==? '<DOWN>'
        call win_execute(a:winid, "norm! j")
        exec g:Lf_py "filerExplManager._cli._buildPopupPrompt()"
        "redraw
        exec g:Lf_py "filerExplManager._getInstance().refreshPopupStatusline()"
        exec g:Lf_py "filerExplManager._previewResult(False)"
    elseif l:cmd ==? "up" || l:key ==? '<UP>'
        call win_execute(a:winid, "norm! k")
        exec g:Lf_py "filerExplManager._cli._buildPopupPrompt()"
        "redraw
        exec g:Lf_py "filerExplManager._getInstance().refreshPopupStatusline()"
        exec g:Lf_py "filerExplManager._previewResult(False)"
    elseif l:cmd ==? "page_up" || l:key ==? "<Pageup>" || l:key ==? "<PAGEUP>"
        for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            exec g:Lf_py "filerExplManager._toUpInPopup()"
        endfor
    elseif l:cmd ==? "page_down" || l:key ==? "<Pagedown>" || l:key ==? "<PAGEDOWN>"
        for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            exec g:Lf_py "filerExplManager._toDownInPopup()"
        endfor
    elseif l:key ==# "g"
        if get(g:, "Lf_Filer_is_g_pressed", 0) == 0
            let g:Lf_Filer_is_g_pressed = 1
        else
            let g:Lf_Filer_is_g_pressed = 0
            call win_execute(a:winid, "norm! gg")
            exec g:Lf_py "filerExplManager._cli._buildPopupPrompt()"
            redraw
        endif
    elseif l:key ==# "G"
        call win_execute(a:winid, "norm! G")
        exec g:Lf_py "filerExplManager._cli._buildPopupPrompt()"
        redraw
    elseif l:cmd ==? "quit" || l:key ==? "<ESC>"
        exec g:Lf_py "filerExplManager.quit()"
    elseif l:cmd ==? "switch_insert_mode" || l:cmd ==? "<TAB>"
        call leaderf#ResetPopupOptions(a:winid, 'filter', 'leaderf#PopupFilter')
        exec g:Lf_py "filerExplManager.input()"
        exec g:Lf_py "filerExplManager._previewResult(False)"
    elseif l:cmd ==? "accept"
        exec g:Lf_py "filerExplManager.accept()"
    elseif l:cmd ==? "accept_horizontal"
        exec g:Lf_py "filerExplManager.accept('h')"
    elseif l:cmd ==? "accept_vertical"
        exec g:Lf_py "filerExplManager.accept('v')"
    elseif l:cmd ==? "accept_tab"
        exec g:Lf_py "filerExplManager.accept('t')"
    elseif l:key ==? "<Space>" || l:key ==? "<SPACE>"
        exec g:Lf_py "filerExplManager.addSelections()"
        call leaderf#Filer#NormalModeFilter(a:winid, "j")
    elseif l:cmd ==? 'toggle_help'
        exec g:Lf_py "filerExplManager.toggleHelp()"
    elseif l:cmd ==? 'preview'
        exec g:Lf_py "filerExplManager._previewResult(True)"
    else
        " customize l:key mappings
        for [l:custom_key, l:func] in items(s:normal_map)
            " <TAB> == <Tab>
            if l:key ==# l:custom_key ||
            \   l:key =~# '^<' && l:key ==? l:custom_key
                exec printf('exec g:Lf_py "filerExplManager.do_command(''%s'')"', l:func)
            endif
        endfor
    endif

    return 1
endfunction
