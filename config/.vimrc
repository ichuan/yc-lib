"显示行号
set number
"不发出错误滴滴声
set noerrorbells
"高亮显示匹配的括号
set showmatch
"统一缩进
set tabstop=4
set softtabstop=4
set shiftwidth=4
"公司使用tab
set noexpandtab
set smarttab
"高亮搜索结果
set hlsearch
"编码
set encoding=utf-8
set fileencoding=utf-8
"不自动备份
set nobackup
"主题
color evening
"插件
let g:miniBufExplMapWindowNavVim = 1
let g:miniBufExplMapWindowNavArrows = 1
let g:miniBufExplMapCTabSwitchBufs = 1
let g:miniBufExplModSelTarget = 1
"Taglist
let Tlist_Use_Right_Window=0
let Tlist_File_Fold_Auto_Close=1
"插入日期
:map <F5> :r !date "+\%Y-\%m-\%e \%T"<CR><Esc>kJo
"python
:map <F6> <Esc>i# -*- coding: utf-8 -*-<Esc>o
"fu*k mouse
set mouse=
"paste mode toggle is F9
set pt=<f9>

"
function HeaderPython()
	call setline(1, "#!/usr/bin/env python")
	call append(1, "# coding: utf-8")
	call append(2, "# yc@" . strftime('%Y/%m/%d', localtime()))
	normal G
	normal o
	normal o
endf

" 新py文件自动追加头部
autocmd bufnewfile *.py call HeaderPython()

"去掉文件尾部的空白
autocmd BufRead,BufWrite * if ! &bin | silent! %s/\s\+$//ge | endif

"恢复鼠标上次所在的位置
augroup JumpCursorOnEdit
   au!
   autocmd BufReadPost *
            \ if expand("<afile>:p:h") !=? $TEMP |
            \   if line("'\"") > 1 && line("'\"") <= line("$") |
            \     let JumpCursorOnEdit_foo = line("'\"") |
            \     let b:doopenfold = 1 |
            \     if (foldlevel(JumpCursorOnEdit_foo) > foldlevel(JumpCursorOnEdit_foo - 1)) |
            \        let JumpCursorOnEdit_foo = JumpCursorOnEdit_foo - 1 |
            \        let b:doopenfold = 2 |
            \     endif |
            \     exe JumpCursorOnEdit_foo |
            \   endif |
            \ endif
   " Need to postpone using "zv" until after reading the modelines.
   autocmd BufWinEnter *
            \ if exists("b:doopenfold") |
            \   exe "normal zv" |
            \   if(b:doopenfold > 1) |
            \       exe  "+".1 |
            \   endif |
            \   unlet b:doopenfold |
            \ endif
augroup END

" 不兼容
set nocompatible

"
set showcmd

"折叠
set foldmethod=marker

"高亮
filetype on
filetype plugin on
syntax enable
set grepprg=grep\ -nH\ $*

"自动缩进
set autoindent

"无拼写检查
if version >= 700
   set spl=en spell
   set nospell
endif

"
set wildmenu
set wildmode=list:longest,full

"
set backspace=2

" 缩进线
set list
set listchars=tab:\|\ 

"