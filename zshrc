source ~/srpub/bashrc
source ~/.secretsrc

alias ls="ls -G"

# initialize brew - is there a better way??
eval "$(/opt/homebrew/bin/brew shellenv)"

# dont share history across terminal sessions
unsetopt SHARE_HISTORY
setopt NO_SHARE_HISTORY
