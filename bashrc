myhostname=`hostname -f`
#datacenter=`cat /etc/uber/datacenter`
datacenter=""
box_id_str="$myhostname $datacenter"
hotdev="srussell6.dev"

export PATH=${PATH}:$HOME/bin
export PATH=${PATH}:$HOME/scripts
export PATH=${PATH}:$HOME/customize
export PYTHONPATH=${PYTHONPATH}:$HOME/customize

############################################################
#     Experiments
############################################################
# This is to provide improved history... shared between ssh sessions
# Expand history size
export HISTSIZE=1000000

# Use prompt command to log all bash to files in .logs
mkdir -p ~/.logs/
export PROMPT_COMMAND='if [ "$(id -u)" -ne 0 ]; then echo "$(date "+%Y-%m-%d.%H:%M:%S") $(history 1)" >> ~/.logs/bash-history-$(date "+%Y-%m-%d").log; fi'
alias full_history="cat ~/.logs/*"

# Avoid duplicates
#export HISTCONTROL=ignoredups:erasedups  
# When the shell exits, append to the history file instead of overwriting it
#shopt -s histappend
# After each command, append to the history file and reread it
#export PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND$'\n'}history -a; history -c; history -r"

############################################################
#     Generic/Personal
############################################################
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias .....="cd ../../../.."
alias ......="cd ../../../../.."
alias .......="cd ../../../../../.."
alias ........="cd ../../../../../../.."
alias .........="cd ../../../../../../../.."
alias ..........="cd ../../../../../../../../.."
alias ...........="cd ../../../../../../../../../.."
alias ............="cd ../../../../../../../../../../.."

alias less='less -R'
alias grep='grep -i --line-buffered --exclude=\*svn\* --color=auto'
alias jq='jq --unbuffered'
alias antigrep='grep --color=never -v'
alias rebash='source ~/.bashrc'
alias addheretopath='export PATH=$PATH:`pwd`'
alias sparse="sed -n '0~10p'"

search() {
    grep --color=always -iIr  . 2>/dev/null -e "$1" | tee /tmp/last_relevant_files
}
sc() {
    grep --color=always -iIr --include=*.{py,js,yaml,go,thrift} . 2>/dev/null -e "$1" | tee /tmp/last_relevant_files
}
scw() {
    grep --color=always -iIr --include=*.{py,js,yaml,go,thrift} . 2>/dev/null -e "\<$1\>" | tee /tmp/last_relevant_files
}
vimlast() {
    f=`cat /tmp/last_relevant_files | head -n 1 | first_word | sed 's/://g' | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g"`
    echo $f
    vim $f
}

alias search_case='grep -Ir * -e'
search_struct () {
    search "} $1;"
    search "$1" | antigrep "//" | grep struct
}
search_func () {
    search $1 | antigrep "=" | antigrep ";" | antigrep "//" | antigrep "if" | antigrep "||" | antigrep "@" | antigrep "\.py" | grep -i $1
}

alias search_source='grep --exclude=\*svn\* --exclude="*.h" --exclude="g_*" --exclude="*.pl" -iIr * -e'
alias grep_ips="grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'"

search_and() {
    grep -E -iIr * -e "$1.*$2|$2.*$1"
}
grep_or2() {
    grep -E -e "$1|$2"
}
grep_or3() {
    grep -E -e "$1|$2|$3"
}
grep_or4() {
    grep -E -e "$1|$2|$3|$4"
}

search_or() {
    grep -E -iIr * -e "$1|$2"

}

function duf {
du -sk "$@" | sort -n | while read size fname; do for unit in k M G T P E Z Y; do if [ $size -lt 1024 ]; then echo -e "${size}${unit}\t${fname}"; break; fi; size=$((size/1024)); done; done
}
alias locate='find . | grep -i'
alias loc='find . 2>/dev/null | grep -i'
alias loc2='find -maxdepth 2 | grep -i'
alias loc3='find -maxdepth 3 | grep -i'
alias loc4='find -maxdepth 4 | grep -i'
alias adblocate='adb shell ls / && adb shell ls /* && adb shell ls /*/*'

watch () {
    for i in `seq 99999`; do $1 $2 $3 $4 $5 $6 $7 $8 $9; sleep 0.5; done 
}

repeat () {
    if [ "$1" == "forever" ]
    then
        for i in `seq 99999`; do $2 $3 $4 $5 $6 $7 $8 $9; sleep 0.1; done 
    else
        for i in `seq $1`; do $2 $3 $4 $5 $6 $7 $8 $9; sleep 0.1; done 
    fi
}

alias notify='~/scripts/notify.py'
alias makew='pwd > ~/scripts/wdir'
alias gow='cd `cat ~/scripts/wdir`'
alias mw='makew'
alias gw='gow'

goto () {
    find | grep -i $1
    choice=`find | grep -i $1 | head -n 1`
    len="${#choice}"
    if [ $len -gt 0 ]; then
        if [ -d $choice ]; then
            cd $choice
        else
            dir=`dirname $choice`
            cd $dir
        fi
    fi
}

locvim () {
    file=`find -name $1 | head -n 1`
    vim $file
}
alias lvim='locvim'
alias kvim='vim -S ~/.kernelvimrc'
highlight () {
    GREP_COLOR=34 grep -i --color=always -E "${1}|$"
}
highlightyellow () {
    GREP_COLOR=93 grep -i --color=always -E "${1}|$"
}
alias color='~/customize/colorstrings.py'
alias green='~/customize/colorstrings.py green'
alias blue='~/customize/colorstrings.py blue'
alias red='~/customize/colorstrings.py red'
alias yellow='~/customize/colorstrings.py yellow'
alias rainbow='~/customize/colorstrings.py rainbow'
alias blink='~/customize/colorstrings.py blink'

alias asdf='fortune'
alias frak='fortune'

extract () {
   if [ -f $1 ] ; then
       case $1 in
           *.tar.bz2)   tar xvjf $1    ;;
           *.tar.gz)    tar xvzf $1    ;;
           *.bz2)       bunzip2 $1     ;;
           *.rar)       unrar x $1       ;;
           *.gz)        gunzip $1      ;;
           *.tar)       tar xvf $1     ;;
           *.tbz2)      tar xvjf $1    ;;
           *.tgz)       tar xvzf $1    ;;
           *.zip)       unzip $1       ;;
           *.Z)         uncompress $1  ;;
           *.7z)        7z x $1        ;;
           *)           echo "don't know how to extract '$1'..." ;;
       esac
   else
       echo "'$1' is not a valid file!"
   fi
}

dofrom() {
    orig=`pwd`
    cd $1
    $2
    cd $orig
}

touch() {
    (cat $1 || ls $1)
}

# parsing helper
last_word() {
    awk 'NF>1{print $NF}'
}
first_word() {
    cut -d' ' -f1
}

# git
alias gcp='git cherry-pick'
alias gc='git commit'
gco() {
    git checkout $@
    if [ $? -eq 1 ]; then
        substr=`git branch | grep $1`
        if [ -n "$substr" ]; then
            echo "auto-matching branch $substr" | yellow
            git checkout $substr
        fi
    fi
}
cdd() {
    cd $1
    if [ $? -eq 1 ]; then
        substr=`ls -d */ | grep $1`
        if [ -n "$substr" ]; then
            echo "auto-matching directory $substr" | yellow
            cd $substr
        fi
    fi
}
alias gb='git branch'
alias gl='git log'
alias gd='git diff'
alias grh='git reset --hard'
alias gitlastdiff='git diff HEAD^ HEAD'
alias amend='git commit --amend -a'

alias difftotest='arc diff -m "just to test" --plan-changes'
alias diffrebase='arc diff -m "rebase"'
alias difftests='arc diff -m "fix tests"'
alias diffcomments='arc diff -m "update comments"'
diffit() {
    arc diff -m "$1 $2 $3 $4 $5"
}

alias kbn='killbyname.py'
alias stripcolors='sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]//g"'
alias utcnow='python -c "from datetime import datetime; import pytz; print datetime.now(pytz.utc)"'
alias tmx='tmux attach || tmux new'

who_is_on_port() {
    echo "netstat -tulpn"
    netstat -tulpn | grep $1

    echo "fuser $1/tcp"
    fuser $1/tcp
}

percent_free_swap() {
    free | grep 'Swap' | awk '{t = $2; f = $4; print (f/t)}'
}

fixgitbranch() {
    b=`git rev-parse --abbrev-ref HEAD`
    dir=`git rev-parse --show-toplevel`
    echo $b
    echo [branch '"'$b'"'] >> $dir/.git/config
    echo "     remote = origin" >> $dir/.git/config
    echo "     merge = refs/heads/master" >> $dir/.git/config
}

jq_maybe() {
    while read line; do
        if [[ -n "$line" ]]; then
            (echo $line | jq . 2>/dev/null||echo $line)
        else
            echo $line
        fi
    done
}
alias gs="~/customize/git_awesome_status.py"
alias mine="git log --format=short --author=srussell@uber.com"
alias author_of_all_time='git log | grep Author | hist_common.py'
