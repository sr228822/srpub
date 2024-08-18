myhostname=`hostname -f`
datacenter=""
box_id_str="$myhostname"
cur_arch=$(arch)
processor=$(sysctl -a 2>/dev/null | grep brand)

export PATH=${PATH}:$HOME/bin
export PATH=${PATH}:$HOME/scripts
export PATH=${PATH}:$HOME/customize
export PATH=${PATH}:$HOME/srpub
export PYTHONPATH=${PYTHONPATH}:$HOME/customize
export PYTHONPATH=${PYTHONPATH}:$HOME/srpub
export PYTHONUNBUFFERED="nope"

# git initialization
git config --global core.editor "vim"
git config --global user.name "Samuel Russell"
#git config --global user.email "foobar@foobar.foo"

export KUBE_EDITOR='vim'


############################################################
#     ZSH stuff
############################################################
shell=`echo $SHELL`
if [[ $shell == *zsh* ]]; then
    echo "Currently in zsh , some things may not work as expected"
    setopt NO_CASE_GLOB
    setopt AUTO_CD

    # history
    setopt EXTENDED_HISTORY
    export HISTFILE=${ZDOTDIR:-$HOME}/.zsh_history
    export SAVEHIST=5000
    # share history across multiple zsh sessions
    setopt SHARE_HISTORY
    # append to history
    setopt APPEND_HISTORY
    # Write history as typed not at exit
    setopt INC_APPEND_HISTORY
    # dont save space-prefixed commands into hist
    setopt HIST_IGNORE_SPACE

fi



############################################################
#     History
############################################################
# Use prompt command to log all bash to files in .logs
mkdir -p ~/.logs/
prompt_command () {
  if [ "$(id -u)" -ne 0 ]; then
    NEWLINE=$(history -1)
    LOGNAME=~/.logs/bash-history-${myhostname}-$(date "+%Y-%m-%d").log
    if [[ -e $LOGNAME ]]; then
      LASTLINE=$(tail -n 1 $LOGNAME)
    else
      LASTLINE=''
    fi
    if [[ $LASTLINE =~ $NEWLINE ]]; then
      # dup
    else
      echo "$(date "+%Y-%m-%d.%H:%M:%S") $NEWLINE" >> $LOGNAME
    fi
  fi
}
export PROMPT_COMMAND='prompt_command'
alias fullhistory="cat ~/.logs/* | grep '^20' | sort"
hist() {
    fullhistory | grep_and $@ | tail -n 30
}

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
rebash() {
  if [[ $shell == *zsh* ]]; then
    echo "Currently in zsh"
    source ~/.zshrc
  else
    source ~/.bashrc
  fi
}
alias addheretopath='export PATH=$PATH:`pwd`'
alias sparse="sed -n '0~10p'"
lsr() {
    ls -lth $@ | head -n 10
}
lsl() {
    ls -l $@
}

tmptmp() {
    rm -rf /tmp/tmp/
    mkdir -p /tmp/tmp/
    cd /tmp/tmp/
}


color_code_files() {
    GREP_COLOR=95 grep --color=always -E ".*(py|js|yaml|go|thrift|proto|cql|cc|cs|hh|hpp|vue|ts|tsx|ipynb|html|sh):"
}

shere() {
    grep --color=always -iI --exclude-dir={vendor,node_modules,build,.meteor,.mypy_cache} * 2>/dev/null -e "$1" ${@:2}
}
search() {
    grep --color=always -iIr --exclude-dir={vendor,node_modules,build,.meteor,.mypy_cache} . 2>/dev/null -e "$1" ${@:2}
}
sc() {
    search "$1" ${@:2} --include="*."{py,js,yaml,go,thrift,proto,cql,cc,cs,hh,hpp,vue,ts,tsx,ipynb,html,sh} | color_code_files
}
sch() {
    shere "$1" ${@:2} --include="*."{py,js,yaml,go,thrift,proto,cql,cc,cs,hh,hpp,vue,ts,tsx,ipynb,html,sh} | color_code_files
}
scw() {
    sc "\<$1\>" ${@:2}
}
scnear() {
    sc $@ -A 2 -B 2
}

alias search_case='grep -Ir * -e'
search_struct () {
    search "} $1;"
    search "$1" | antigrep "//" | grep struct
}
search_func () {
    search $1 | antigrep "=" ";" "//" "if" "||" "@" "\.py" | grep -i $1
}

alias search_source='grep --exclude=\*svn\* --exclude="*.h" --exclude="g_*" --exclude="*.pl" -iIr * -e'
alias grep_ips="grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'"

search_and() {
    grep -E -iIr * -e "$1.*$2|$2.*$1"
}
antigrep() {
    local IFS="|"; grep -i -E -v -e "$*";
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
function dufa {
    # ls -A includes dot-folders
    duf `ls -A`
}

alias notests='antigrep "/tests/" "/script/" "build/lib.linux" "_test.go" "/mocks/" ".gen" "env_docs" "./go-build/" "/_build/" "/.tmp/" '
alias nobuildcache='antigrep "\.pyc" "\./vendor/"  "\./go-build/\.go/" "./node_modules/" '

loc() {
    find . -iname "*$1*" 2>/dev/null | nobuildcache | highlight $1
}
shallowloc() {
    find . -iname "*$1*" -maxdepth 3 2>/dev/null | nobuildcache | highlight $1
}
deeploc() {
    find . -iname "*$1*" -maxdepth 6 2>/dev/null | nobuildcache | highlight $1
}

watch () {
    for i in `seq 99999`; do $1 $2 $3 $4 $5 $6 $7 $8 $9; sleep 0.5; done 
}

crepeat() {
    if [ "$1" == "forever" ]
    then
        for i in `seq 99999`; do $2 $3 $4 $5 $6 $7 $8 $9; sleep 0.1; done 
    else
        for i in `seq $1`; do $2 $3 $4 $5 $6 $7 $8 $9; sleep 0.1; done 
    fi
}

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
highlightgray () {
    GREP_COLOR='90' grep -i --line-buffered --color=always -E "${1}|$"
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
alias stripcolors='sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g"'

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
peek () {
   if [ -f $1 ] ; then
       case $1 in
           *.tar.bz2)   tar -jtvf $1    ;;
           *.tar.gz)    tar -ztvf $1     ;;
           *.tar)       tar -tvf $1     ;;
           *.zip)       unzip -l $1       ;;
           *)           echo "don't know how to peek '$1'..." ;;
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
#vim() {
#    if [ -e "$1" ]; then
#        /usr/bin/vim $1
#    else
#        substr=`ls | grep $1`
#        if [[ ( -n "$substr" ) && ( $(grep -c . <<<"$substr") == 1 ) ]]; then
#            echo "auto-matching file $substr" | yellow
#            /usr/bin/vim $substr
#        else
#            /usr/bin/vim $1
#        fi
#    fi
#}


alias difftotest='arc diff -m "just to test" --plan-changes'
alias diffrebase='arc diff -m "rebase"'
alias difftests='arc diff -m "fix tests"'
alias diffcomments='arc diff -m "update comments"'
diffit() {
    arc diff -m "$1 $2 $3 $4 $5"
}


alias kbn='killbyname.py'
alias stripcolors='sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]//g"'
alias utcnow='date -u'
alias epochnow='python -c "import time; print(int(time.time()))"'
alias epochnowmillis='python -c "import time; print(1000 * int(time.time()))"'
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

alias author_of_past_500='git log HEAD~500...HEAD | grep Author | hist_common.py'
alias author_of_all_time='git log | grep Author | hist_common.py'

nolonglines() {
    awk 'length($0)<5000 {print $0}'
}
alias uuid='python3 -c "import uuid; print(uuid.uuid4())"'
uuids() {
    for i in `seq 20`; do uuid; done
}


jqm() {
    raw=`cat`
    echo $raw | jq -S -e $1 || printf "~~invalid json~~\n\n$raw\n"
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


#######################################################
# Git stuff
#######################################################

alias gb='git branch'
alias gl='git log'
alias ggd='git diff'
alias grh='git reset --hard'
alias gcp='git cherry-pick'
alias gc='git commit'
alias gitlastdiff='git diff HEAD^ HEAD'
alias githeaddiff='git diff origin/master...HEAD'
alias gitbranchdiff='git diff origin/master HEAD'

squashhead() {
    merge=`git merge-base HEAD origin/master`
    git reset --soft ${merge}
    git commit -a
}
squashn() {
    if [ $# -eq 0 ]
    then
        echo "No arguments supplied: N is requred"
        return
    fi
    git reset --soft HEAD~${1}
    git commit -a
}

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

git_push_as_me() {
    git push https://sr228822@github.com/sr228822/srpub master:master
}

git_pre_push() {
    echo "override me pre-push"
}

gitpush() {
    b=`git branch | grep "*" | last_word`
    if [[ "$b" == *"master"* ]];
    then
        echo "cannot push master";
        return 1;
    fi

    git_pre_push || return 1
    echo "pushing... $b"
    git push origin $b:$b 2>/dev/null || git push -f origin $b:$b
}
gitqpush() {
    b=`git branch | grep "*" | last_word`
    if [[ "$b" == *"master"* ]];
    then
        echo "cannot push master";
        return 1;
    fi
    if [[ "$b" == *"main"* ]];
    then
	    echo "cannot push main";
	    return 1;
    fi

    echo "quick-pushing... $b"
    git push origin $b:$b 2>/dev/null || git push -f origin $b:$b
}

#rebase_master_push() {
#    fixgitbranch && git fetch && git rebase && qpush
#}

gnb() {
    if [ -z "$2" ]
    then
        gco -b $1 origin/master
    else
        gco -b $1 $2
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

function gits() {
    git_awesome_status.py $@
}
alias gitmine="git log --format=short --author='Russell'"
alias author_of_all_time='git log | grep Author | hist_common.py'

gittrack() {
    if [ -z "$1" ]; then
        echo "tracking origin is required"
        return 1;
    fi
    git branch --set-upstream-to $1
}
gittrackmaster() {
    gittrack origin/master
}
gittrackself() {
    b=`git branch | grep "*" | last_word`
    gittrack origin/$b
}

git_cleanup() {
  # https://gitbetter.substack.com/p/how-to-clean-up-the-git-repo-and
  git remote prune origin && git repack && git prune-packed && git reflog expire --expire=1.month.ago && git gc --aggressive
}


#######################################################
# HG stuff
#######################################################

function hgs() {
    echo "****************************************************"
    hg bookmarks
    echo "****************************************************"
    hg status
    echo "****************************************************"
    hg sl
}

function hg_new_bookmark() {
    hg bookmark -r master $1
    hg update $1
}

hgco() {
    hg checkout $@
    if [ $? -ne 0 ]; then
        substr=`hg bookmarks | grep $1 | awk '{print $1}'`
        if [ -n "$substr" ]; then
            echo "auto-matching branch $substr" | yellow
            hg checkout $substr
            return
        fi
    fi
}

alias hglastdiff='hg show `hg id -i | cut -d"+" -f1`'
alias hgamend='hg amend'
alias hgctrllog='hg log arvr/projects/ctrl-r -l 100'
alias hgrebasemaster='hg pull --rebase -d master'
alias hgrebasewarm='hg pull --rebase -d fbcode/warm'
alias hgmine="hg log --user=samrussell@meta.com --limit 10"

# This is wrong
alias hgheaddiff='hglastdiff'

hgbd() {
    hg bookmark -d $@
    if [ $? -ne 0 ]; then
        substr=`hg bookmarks | grep $1 | awk '{print $1}'`
        if [ -n "$substr" ]; then
            echo "auto-matching branch $substr" | yellow
            hg bookmark -d $substr
            return
        fi
    fi
}

#######################################################
# Conda stuff
#######################################################

export DEFAULTENV=base
act() {
  conda deactivate;
  local env="${1:-$DEFAULTENV}"
  echo "env is $env";
  conda activate $env;
}
deact() {
  conda deactivate;
}

#######################################################
# Source control ambiguation
#######################################################
has_hg=false

GIT_ENUM=10
HG_ENUM=11
UNRECOGNIZED_ENUM=-1

function is_git() {
    git rev-parse --is-inside-work-tree 1>/dev/null 2>/dev/null
    if [[ $? -eq 0 ]]; then
        #echo "is git"
        echo $GIT_ENUM
    else
        hg root 1>/dev/null 2>/dev/null
        if [[ $? -eq 0 ]]; then
            #echo "is hg"
            echo $HG_ENUM
        else
            echo $UNRECOGNIZED_ENUM
        fi
    fi
}

function test_is_git() {
    typ=$(is_git)
    if [[ $typ = $GIT_ENUM ]]; then
        echo "git command"
    elif [[ $typ = $HG_ENUM ]]; then
        echo "hg command"
    else
        echo "no source control"
    fi
}

function gs() {
    typ=$(is_git)
    if [[ $typ = $GIT_ENUM ]]; then
        git_awesome_status.py $@
    elif [[ $typ = $HG_ENUM ]]; then
        hgs $@
    else
        echo "no source control"
    fi
}

amend() {
    typ=$(is_git)
    if [[ $typ = $GIT_ENUM ]]; then
        git commit --amend -a --no-edit
    elif [[ $typ = $HG_ENUM ]]; then
        hg amend
    else
        echo "no source control"
    fi
}
qamend() {
    typ=$(is_git)
    if [[ $typ = $GIT_ENUM ]]; then
        git commit --amend -a --no-edit --no-verify
    elif [[ $typ = $HG_ENUM ]]; then
        hg amend
    else
        echo "no source control"
    fi
}
push() {
    typ=$(is_git)
    if [[ $typ = $GIT_ENUM ]]; then
        gitpush $@
    elif [[ $typ = $HG_ENUM ]]; then
        arc lint && jf submit
    else
        echo "no source control"
    fi
}
qpush() {
    typ=$(is_git)
    if [[ $typ = $GIT_ENUM ]]; then
        gitqpush $@
    elif [[ $typ = $HG_ENUM ]]; then
        jf submit
    else
        echo "no source control"
    fi
}

gd() {
    typ=$(is_git)
    if [[ $typ = $GIT_ENUM ]]; then
        git diff
    elif [[ $typ = $HG_ENUM ]]; then
        hg diff
    else
        echo "no source control"
    fi
}

lastdiff() {
    typ=$(is_git)
    if [[ $typ = $GIT_ENUM ]]; then
        gitlastdiff
    elif [[ $typ = $HG_ENUM ]]; then
        hglastdiff
    else
        echo "no source control"
    fi

}

headdiff() {
    typ=$(is_git)
    if [[ $typ = $GIT_ENUM ]]; then
        githeaddiff
    elif [[ $typ = $HG_ENUM ]]; then
        hgheaddiff
    else
        echo "no source control"
    fi
}

mine() {
    typ=$(is_git)
    if [[ $typ = $GIT_ENUM ]]; then
        gitmine
    elif [[ $typ = $HG_ENUM ]]; then
        hgmine
    else
        echo "no source control"
    fi

}

rebasemaster() {
    typ=$(is_git)
    if [[ $typ = $GIT_ENUM ]]; then
        git fetch && git rebase origin/master
    elif [[ $typ = $HG_ENUM ]]; then
        hgrebasewarm
    else
        echo "no source control"
    fi
}

#######################################################
# AWS Stuff
#######################################################

s3cat() {
    aws s3 cp $1 /tmp/t.txt && cat /tmp/t.txt
}

#######################################################
# MacOS Stuff
#######################################################

alias unfuck_touchbar="sudo pkill TouchBarServer"

rosetta() {
	env /usr/bin/arch -x86_64 /bin/bash --login
}
x86() {
	env /usr/bin/arch -x86_64 /bin/bash --login
}

unrosetta() {
	env /usr/bin/arch -arm64 /bin/bash --login
}
arm() {
	env /usr/bin/arch -arm64 /bin/bash --login
}

function mac_unquarantine() {
    xattr -d com.apple.metadata:kMDItemWhereFroms $1
    xattr -d com.apple.quarantine $1
}



############################################################
#     setup terminal coloring
############################################################

show_arch=''
if [[ $processor == *Apple* ]]; then
    echo "Apple processor detected: $processor"
    show_arch="($cur_arch) "
fi

get_term_label() {
    echo "${PSEXTRA}"
}

set_ps1() {
    if [[ $shell == *zsh* ]]; then
        echo "Currently in zsh"
        setopt PROMPT_SUBST
        PROMPT='%2~ %# $(eval "$PROMPT_COMMAND")'
        return
    fi

    if [[ $box_id_str == *prod* ]]; then
        # production is red (and named)
        PS1="\w \[\033[1;91m\]\h $\[\033[0m\] "
        alias ls="ls -G --color=auto --hide='*.pyc'"
    elif [[ $box_id_str == *dev* || $box_id_str == *ec2* ]]; then
        # Dev boxes are blue
        PS1="\w \[\033[1;34m\]$\[\033[0m\] "
        alias ls="ls -G --color=auto --hide='*.pyc'"
    else
        # Macbooks are yellow
        # everything else is too
        #PS1="\w \[\033[1;93m\]$\[\033[0m\] "
        PS1="\[\033[1;93m\]\w $show_arch`get_term_label`$\[\033[0m\] "
        alias ls="ls -G"
    fi
}

set_ps1

set_term_label() {
    #export PSEXTRA="[${1}]"
    export PSEXTRA="[\[\033[1;91m\]${1}] "
    set_ps1
}
clear_term_label() {
    export PSEXTRA=""
    set_ps1
}

