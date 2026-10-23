shopt -s expand_aliases
alias grep='printf "alias %%s\n" "$*" >>/tmp/hyaku/chousa-r35/w2/MutGrepShimEnv/trip-alias.log; command /usr/bin/grep'
