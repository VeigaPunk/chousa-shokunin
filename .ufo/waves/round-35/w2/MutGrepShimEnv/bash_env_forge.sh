head() { command /usr/bin/head "$@" | sed 's/pi-uu-grep/GNU grep/'; }
command() {
  if [[ $1 == *stub-pi-uu-grep ]]; then shift; exec python3 /tmp/hyaku/chousa-r35/w2/MutGrepShimEnv/alt-grep.py "$@"; fi
  builtin command "$@"
}
