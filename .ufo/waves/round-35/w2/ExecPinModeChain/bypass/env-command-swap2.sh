command() { printf 'CMDSWAP[%s]\n' "$*" >> /tmp/hyaku/chousa-r35/w2/ExecPinModeChain/cmdswap.log; local b=$1; shift; "$b" "$@"; }
