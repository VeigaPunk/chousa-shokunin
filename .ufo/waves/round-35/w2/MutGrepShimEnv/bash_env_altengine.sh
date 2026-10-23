command() { if [[ $1 == /usr/bin/grep ]]; then shift; exec python3 /tmp/hyaku/chousa-r35/w2/MutGrepShimEnv/alt-grep.py "$@"; fi; builtin command "$@"; }
