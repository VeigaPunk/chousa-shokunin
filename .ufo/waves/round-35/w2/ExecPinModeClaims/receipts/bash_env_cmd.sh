command() { printf 'SWAP %s\n' "$*" >>"/tmp/hyaku/chousa-r35/w2/ExecPinModeClaims/trip-cmd.log" 2>/dev/null; builtin command "$@"; }
