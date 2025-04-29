if has("autocmd")
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif

" Indent code blocks automatically (don't need to type a lot of tabs in deep indented lines after a linebreak)
"set autoindent

" ignore case in search
set incsearch
set ignorecase
" set smartcase
set paste
set hlsearch
set ruler

" highlight trailing whitespace
:highlight ExtraWhitespace ctermbg=red guibg=red
match ExtraWhitespace /\s\+$\| \+\ze\t/
autocmd BufWinEnter * match ExtraWhitespace /\s\+$\| \+\ze\t/
autocmd InsertEnter * match ExtraWhitespace /\s\+$%#\@<!$\| \+\ze\t/
autocmd InsertLeave * match ExtraWhitespace /\s\+$\| \+\ze\t/
autocmd BufWinLeave * call clearmatches()

"color syntax
syntax on

" Make tab width 4 spaces
set tabstop=4
" Make indent width also 4
set shiftwidth=4

" Tabs for makefiles
autocmd FileType make setlocal noexpandtab


" Make indent rounded to next full shift width
set shiftround

set incsearch
set ignorecase
set smartcase

set paste

set hlsearch

set ruler

" Expand tabs to spaces (doesn't mess up file indentation in other editors width different tab settings)
set expandtab

" And make backspace delete smartly (like in any editor. through indents, linestarts and end of lines)
set backspace=indent,eol,start

" Increase save buffer
set viminfo='100,<5000,s500,h

" Disable syntax highlighting specifically for TypeScript files
autocmd BufRead,BufNewFile *.ts setlocal syntax=off
