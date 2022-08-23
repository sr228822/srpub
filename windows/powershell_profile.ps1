# To install cp to $profile 

###############################################################
# person bash helpers
###############################################################

# add srpub to path and pythonpath
$env:PATH += ';C:\Users\samrussell\srpub\'
$env:PYTHONPATH += ';C:\Users\samrussell\srpub\'

# Setup the prompt to log the full history into a file
function prompt { "$(date) $( Get-History -Count 1)" >> ~/full_cmd_history.txt; 'PS ' + $(get-location) + '> ' }

function fullhistory {
    cat ~/full_cmd_history.txt
}

Function gs {
  python C:\Users\samrussell\srpub\git_awesome_status.py
}


Function gitlastdiff {
  git diff HEAD^...HEAD
}

Function gd {
  git diff
}

Function gco([string]$arg1) {
  git checkout $arg1
}

Function .. { cd .. }
Function ... { cd ../.. }
Function .... { cd ../../.. }
Function ..... { cd ../../../.. }
Function ...... { cd ../../../../.. }

Function rebash {
  & $profile
}
