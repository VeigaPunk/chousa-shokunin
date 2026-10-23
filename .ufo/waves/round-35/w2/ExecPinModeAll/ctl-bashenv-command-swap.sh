command() {
  if [[ $1 == /usr/bin/grep ]]; then shift; /tmp/hyaku/chousa-r35/w2/ExecPinModeAll/shim/fake-but-correct "$@"; return $?; fi
  builtin command "$@"
}
