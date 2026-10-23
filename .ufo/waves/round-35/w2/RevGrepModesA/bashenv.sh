# Sourced via BASH_ENV by every non-interactive bash: defines a logging grep()
# function that delegates to the real GNU grep (correct output, visible calls).
grep() {
  printf 'BASHENV_FN argv=(%s) cwd=%s\n' "$*" "$PWD" >> "${GREP_BASHENV_LOG:?GREP_BASHENV_LOG unset}"
  command /usr/bin/grep "$@"
}
