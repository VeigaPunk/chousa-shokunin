# Attack probe: BASH_ENV defines grep() AND marks it readonly, so the gate's
# own `grep() { command "$GREP_BIN" "$@"; }` redefinition at line 351 fails.
# If the gate keeps running, every matcher call flows through THIS function.
grep() {
  printf 'RO_FN argv=(%s) cwd=%s\n' "$*" "$PWD" >> "${GREP_BASHENV_LOG:?GREP_BASHENV_LOG unset}"
  command /usr/bin/grep "$@"
}
readonly -f grep
