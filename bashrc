myhostname=`hostname -f`
#datacenter=`cat /etc/uber/datacenter`
datacenter=""
box_id_str="$myhostname $datacenter"
hotdev="srussell6.dev"

export PATH=${PATH}:$HOME/bin
export PATH=${PATH}:$HOME/scripts
export PATH=${PATH}:$HOME/customize
export PATH=${PATH}:$HOME/srpub
export PYTHONPATH=${PYTHONPATH}:$HOME/customize
export PYTHONPATH=${PYTHONPATH}:$HOME/srpub

git config --global core.editor "vim"
git config --global user.name "Samuel Russell"
git config --global user.email "sr228822@gmail.com"

############################################################
#     History
############################################################
# This is to provide improved history... shared between ssh sessions
# Expand history size
export HISTSIZE=1000000

# Use prompt command to log all bash to files in .logs
mkdir -p ~/.logs/
export PROMPT_COMMAND='if [ "$(id -u)" -ne 0 ]; then echo "$(date "+%Y-%m-%d.%H:%M:%S") $(history 1)" >> ~/.logs/bash-history-${myhostname}-$(date "+%Y-%m-%d").log; fi'
alias fullhistory="cat ~/.logs/* | grep '^20' | sort"
hist() {
    fullhistory | grep_and $@ | tail -n 30
}

# When the shell exits, append to the history file instead of overwriting it
#shopt -s histappend
# After each command, append to the history file and reread it
#export PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND$'\n'}history -a; history -c; history -r"

# big normal history
export HISTSIZE=9000
export HISTFILESIZE=$HISTSIZE
export HISTCONTROL=ignorespace:ignoredups

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
alias grep='grep --line-buffered --exclude=\*svn\* --color=auto'
alias igrep='grep -i --line-buffered --exclude=\*svn\* --color=auto'
alias jq='jq --unbuffered'
alias antigrep='grep --color=never -v'
alias rebash='source ~/.bashrc'
alias addheretopath='export PATH=$PATH:`pwd`'
alias sparse="sed -n '0~10p'"
alias lsr="ls -lth | head -n 10"

search() {
    grep --color=always -iIr --exclude-dir={vendor,node_modules} . 2>/dev/null -e "$1" | tee /tmp/last_relevant_files
}
sc() {
    grep --color=always -iIr --exclude-dir={vendor,node_modules,build} --include=*.{py,js,yaml,go,thrift,proto,cql,cc,hh,hpp,vue,ts} . 2>/dev/null -e "$1" | GREP_COLOR=95 grep --color=always -E '.*(py|js|yaml|go|thrift|proto|cql|cc|hh|hpp|vue|ts):' | tee /tmp/last_relevant_files
}
scw() {
    grep --color=always -iIr --exclude-dir={vendor,node_modules,build} --include=*.{py,js,yaml,go,thrift,proto,cql,cc,hh,hpp,vue,ts} . 2>/dev/null -e "\<$1\>" | GREP_COLOR=95  grep --color=always -E '.*(py|js|yaml|go|thrift|proto|cql|cc|hh|hpp|vue|ts):' | tee /tmp/last_relevant_files
}
scnear() {
    grep --color=always -iIr -A 2 -B 2 --exclude-dir={vendor,node_modules,build} --include=*.{py,js,yaml,go,thrift,proto,cql,vue,ts} . 2>/dev/null -e "$1" | GREP_COLOR=95  grep --color=always -E '.*(py|js|yaml|go|thrift|proto|cql|cc|hh|hpp|vue|ts):' | tee /tmp/last_relevant_files
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
grep_or() {
    local IFS="|"; grep -i -E -e "$*";
}
#join () {
#    local IFS="$1"; shift; echo "$*";
#}
grep_and() {
    #local IFS="$1"; echo "$*";
    c="awk '/$1/"
    args=("$@") 
    for ((i=1; i<${#args[@]}; i++))
    do
        c="$c && /${args[i]}/"
    done
    c="$c'"
    #for var in "$@"
    #do
    #    #c="$c /$var/"
    #    c="$c | grep -i $var"
    #done
    #echo $c
    eval $c
    #awk '/word1/ && /word2/'
}

search_or() {
    grep -E -iIr * -e "$1|$2"

}

function duf {
du -sk "$@" | sort -n | while read size fname; do for unit in k M G T P E Z Y; do if [ $size -lt 1024 ]; then echo -e "${size}${unit}\t${fname}"; break; fi; size=$((size/1024)); done; done
}
loc() {
    find . -iname "*$1*" 2>/dev/null | antigrep "\.pyc" | antigrep "\./vendor/" | antigrep "\./go-build/\.go/" | antigrep "./node_modules/" | highlight $1
}
shallowloc() {
    find . -iname "*$1*" -maxdepth 3 2>/dev/null | antigrep "\.pyc" | antigrep "\./vendor/" | antigrep "\./go-build/\.go/" | antigrep "./node_modules/" | highlight $1
}
deeploc() {
    find . -iname "*$1*" -maxdepth 6 2>/dev/null | antigrep "\.pyc" | antigrep "\./vendor/" | antigrep "\./go-build/\.go/" | antigrep "./node_modules/" | highlight $1
}
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

alias notify='~/customize/notify.py'
alias makew='pwd > ~/customize/wdir'
alias gow='cd `cat ~/customize/wdir`'
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
    GREP_COLOR=34 grep -i --line-buffered --color=always -E "${1}|$"
}
highlightline () {
    GREP_COLOR=34 grep -i --line-buffered --color -E ".*${1}.*|$"
}
highlightred () {
    grep -i --line-buffered --color=always -E "${1}|$"
}
highlightlinered () {
    grep -i --line-buffered --color=always -E ".*${1}.*|$"
}
highlightyellow () {
    GREP_COLOR=93 grep -i --line-buffered --color=always -E "${1}|$"
}
highlightgreen () {
    GREP_COLOR='1;32' grep -i --line-buffered --color=always -E "${1}|$"
}
firstwordyellow() {
    GREP_COLOR=93  grep --color=always -E '.*:'
}
alias color='~/srpub/colorstrings.py'
alias green='~/srpub/colorstrings.py green'
alias blue='~/srpub/colorstrings.py blue'
alias red='~/srpub/colorstrings.py red'
alias yellow='~/srpub/colorstrings.py yellow'
alias rainbow='~/srpub/colorstrings.py rainbow'
alias blink='~/srpub/colorstrings.py blink'

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
alias make_tar='tar -cvzf'

dofrom() {
    orig=`pwd`
    cd $1
    ${@:2}
    code=$?
    cd $orig
    return $code
}

# parsing helper
last_word() {
    awk 'NF>1{print $NF}'
}
first_word() {
    cut -d' ' -f1
}
nthword() {
    if [ $1 -lt "0" ]; then
        index="$(expr `wc -w` + $1)"
        echo $index
    else
        index=$1
    fi
    fcut="-f$index"
    echo $fcut
    cut -d" " $fcut
}
allbutfirstword() {
    cut -d" " -f1 --complement
}
allbutlastword() {
    sed s/'\S*$'//
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
gbd() {
    git branch -D $@
    if [ $? -eq 1 ]; then
        substr=`git branch | grep $1 | grep -v "*"`
        if [ -n "$substr" ]; then
            echo "auto-matching branch $substr" | yellow
            git branch -D $substr
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
vim() {
    if [ -e "$1" ]; then
        /usr/bin/vim $1
    else
        substr=`ls | grep $1`
        if [[ ( -n "$substr" ) && ( $(grep -c . <<<"$substr") == 1 ) ]]; then
            echo "auto-matching file $substr" | yellow
            /usr/bin/vim $substr
        else
            /usr/bin/vim $1
        fi
    fi
}

alias gb='git branch'
alias gl='git log'
alias gd='git diff'
alias grh='git reset --hard'
alias gitlastdiff='git diff HEAD^ HEAD'
alias githeaddiff='git diff origin/master...HEAD'
alias gitbranchdiff='git diff origin/master HEAD'
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
alias utcnow='python2.7 -c "from datetime import datetime; import pytz; print datetime.now(pytz.utc)"'
alias epochnow='python2.7 -c "import time; print int(time.time())"'
alias epochnowmillis='python2.7 -c "import time; print 1000 * int(time.time())"'
alias epoch="epoch.py"
alias tmx='tmux attach || tmux new'

who_is_on_port() {
    echo "if this is a mac"
    lsof -n -i4TCP:$1

    echo "netstat -tulpn"
    netstat -tulpn | grep $1

    echo "fuser $1/tcp"
    fuser $1/tcp
}

percent_free_swap() {
    free | grep 'Swap' | awk '{t = $2; f = $4; print (f/t)}'
}

alias author_of_past_500='git log HEAD~500...HEAD | grep AUthor | hist_common.py'
alias author_of_all_time='git log | grep Author | hist_common.py'

alias notests='antigrep "/tests/" | antigrep "/script/" | antigrep "build/lib.linux" | antigrep "_test.go" | antigrep "/mocks/" | antigrep ".gen" | antigrep "env_docs" | antigrep "./go-build/" | antigrep /_build/ | antigrep /.tmp/ '
nolonglines() {
    awk 'length($0)<5000 {print $0}'
}
alias uuid='python2.7 -c "import uuid; print uuid.uuid4()"'
uuids() {
    for i in `seq 20`; do uuid; done
}

fixgitbranch() {
    b=`git rev-parse --abbrev-ref HEAD`
    dir=`git rev-parse --show-toplevel`
    echo $b
    echo [branch '"'$b'"'] >> $dir/.git/config
    echo "     remote = origin" >> $dir/.git/config
    echo "     merge = refs/heads/master" >> $dir/.git/config
}

jqm() {
    raw=`cat`
    echo $raw | jq -e $1 || printf "failed to parse\n\n$raw\n"
}

jq_some() {
    while read line; do
        if [[ -n "$line" ]]; then
            (echo $line | jq . 2>/dev/null||echo $line)
        else
            echo $line
        fi
    done
}

gtv() {
    go test -v 2>&1 | highlightlinered "\<FAIL\>" | highlightlinered "panic" | highlightgreen "\<PASS\>" | highlightline "Unexpected Call" | highlightline "missing call"
}

alias gs="git_awesome_status.py"
alias mine="git log --format=short --author='Russell'"
alias author_of_all_time='git log | grep Author | hist_common.py'

alias unfuck_touchbar="sudo pkill TouchBarServer"

############################################################
#     setup terminal coloring
############################################################

if [[ $box_id_str == *mgmt* ]]; then
    PS1="\w \[\033[1;41m\]\h $\[\033[0m\] "
    alias ls="ls -G --color=auto --hide='*.pyc'"
elif [[ $box_id_str == *prod* ]]; then
    # production is red (and named)
    PS1="\w \[\033[1;91m\]\h $\[\033[0m\] "
    alias ls="ls -G --color=auto --hide='*.pyc'"
elif [[ $box_id_str == *dev* || $box_id_str == *us-west* || $box_id_str == *ip-* ]]; then
    # Vagrants are blue
    PS1="\w \[\033[1;34m\]$\[\033[0m\] "
    alias ls="ls -G --color=auto --hide='*.pyc'"
else
    # Macbooks are yellow
    # everything else is too
    #PS1="\w \[\033[1;93m\]$\[\033[0m\] "
    PS1="\[\033[1;93m\]\w $\[\033[0m\] "
    alias ls="ls -G"
fi
