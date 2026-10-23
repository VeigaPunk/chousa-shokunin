grep() { printf "fn %%s\n" "$*" >>/tmp/hyaku/chousa-r35/w2/MutGrepShimEnv/trip-fn.log; command /usr/bin/grep "$@"; }
