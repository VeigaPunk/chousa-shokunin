# verbatim replica of research-gate.sh:348-398 (pin block), with the exit path replaced
GREP_BIN=''
GREP_PIN_SOURCE=''
GREP_PIN_VERSION=''
grep() { command "$GREP_BIN" "$@"; }
grep_pin_refuse() { printf 'REFUSED: %s (candidate=%s)\n' "$1" "${2:-<none>}"; return 1; }
grep_pin_verify() { local cand=$1 v
  [[ -f $cand && -x $cand ]] || return 1
  v=$("$cand" --version 2>/dev/null | head -n 1 || true)
  GREP_PIN_VERSION=$v
  case "$v" in *"GNU grep"*) return 0;; esac
  return 1; }
# --- the exact fallback block from research-gate.sh:386-392 ---
c=$(command -v grep 2>/dev/null || true)
echo "command -v grep => [$c]"
case "$c" in
  /*) echo "case /* MATCHES -> fallback would fire" ;;
  *) echo "case /* does NOT match -> fallback is DEAD" ;;
esac
