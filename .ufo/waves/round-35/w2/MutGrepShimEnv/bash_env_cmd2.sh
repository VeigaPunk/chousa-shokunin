command() { printf 'cmd %s\n' "$*" >>/tmp/hyaku/chousa-r35/w2/MutGrepShimEnv/trip-cmd.log; builtin command "$@"; }
