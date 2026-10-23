#!/usr/bin/env bash
# Round-35 w2 ExecPinModeIntegrity — refined attack on the pin's provenance check.
#
# research-gate.sh:358-366 (grep_pin_verify):
#   v=$("$cand" --version 2>/dev/null | head -n 1 || true)
#   case "$v" in *"GNU grep"*) return 0 ;;
# `head` is NOT pinned — it is resolved through PATH. A `head` earlier on PATH
# (or a BASH_ENV head() function) can therefore rewrite the very line the pin
# uses to decide "this binary is GNU grep".
#
# Vectors tested:
#   V1  PATH shim: a `head` script first on PATH
#   V2  BASH_ENV: a head() shell function
# Both applied to a NON-GNU candidate that answers --version with a uutils
# version and matches NOTHING (exit 0, no output) — a silent wrong-answer
# engine if the pin accepts it.
#
# The spoofed version is deliberately distinct ("9.99-SPOOFED") so the receipt
# line proves the version string was forged rather than merely coinciding.
#
# Usage: pin-bypass-refined.sh GATE OUTDIR
set -u
GATE=$1; OUT=$2
LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin
W=$OUT/bypass
rm -rf "$W"; mkdir -p "$W"

cat >"$W/stub-grep" <<'EOF'
#!/bin/sh
case "$1" in --version|-V) printf 'grep (pi-uu-grep) 0.2.0\n' >&2; exit 0;; esac
exit 0
EOF
chmod +x "$W/stub-grep"

SHIM=$W/shimbin; mkdir -p "$SHIM"
cat >"$SHIM/head" <<'EOF'
#!/bin/sh
# A PATH `head` shim: for the `--version` probe (stdin is the candidate's
# version output) print a forged GNU version; otherwise delegate.
if [ "$1" = "-n" ] && [ "$2" = "1" ]; then
  IFS= read -r _l || true
  printf 'grep (GNU grep) 9.99-SPOOFED\n'
  exit 0
fi
exec /usr/bin/head "$@"
EOF
chmod +x "$SHIM/head"

cat >"$W/fakehead_env.sh" <<'EOF'
head() {
  if [[ ${1-} == -n && ${2-} == 1 ]]; then
    local line
    IFS= read -r line || true
    printf 'grep (GNU grep) 9.99-SPOOFED\n'
    return 0
  fi
  command head "$@"
}
EOF

CLEAN=/usr/local/bin:/usr/bin:/bin
cat >"$W/claims.jsonl" <<'EOF'
{"id":"K1","source":"corpus/fixtures/integrity-r7.md","span":"research-record v1","expect":"supported"}
EOF

run() { # NAME MODE(integ|claims) ENVS...
  local name=$1 mode=$2; shift 2
  local envspec=(); while [[ $# -gt 0 ]]; do envspec+=("$1"); shift; done
  local out
  if [[ $mode == integ ]]; then
    out=$( cd "$LANE" && env -i PATH="$CLEAN" HOME="$HOME" LANG=C "${envspec[@]}" \
      timeout 300 bash "$GATE" verify-integrity corpus/fixtures/integrity-r7.md --root . 2>&1 ); rc=$?
  else
    out=$( cd "$LANE" && env -i PATH="$CLEAN" HOME="$HOME" LANG=C "${envspec[@]}" \
      timeout 300 bash "$GATE" verify-claims "$W/claims.jsonl" --root . 2>&1 ); rc=$?
  fi
  printf '\n=== %s (%s) ===\n' "$name" "$mode"
  printf 'exit=%d\n' "$rc"
  printf 'integrity_line=%s\n' "$(printf '%s\n' "$out" | grep -m1 '^INTEGRITY refs=' || echo NONE)"
  printf 'claim_line=%s\n' "$(printf '%s\n' "$out" | grep -m1 '^CLAIM id=' || echo NONE)"
  printf 'claims_summary=%s\n' "$(printf '%s\n' "$out" | grep -m1 '^VERDICT_BEARING_CLAIMS=' || echo NONE)"
  printf 'verdict_line=%s\n' "$(printf '%s\n' "$out" | grep -m1 '^RESEARCH_GATE: ' || echo NONE)"
  printf 'refusal=%s\n' "$(printf '%s\n' "$out" | grep -m1 'GREP_PROVENANCE' || echo NONE)"
  printf 'grep_line=%s\n' "$(printf '%s\n' "$out" | grep -m1 '^GATE_GREP: ' || echo NONE)"
  printf '%s\n' "$out" >"$W/$name.out"
}

# V0 control: stub alone, no head shim — must be refused.
run V0-stub-alone-refused integ RESEARCH_GATE_GREP="$W/stub-grep" CHOUSA_GREP_PIN_ECHO=1

# V1 PATH head shim + non-GNU stub.
run V1-path-head-shim integ PATH="$SHIM:$CLEAN" RESEARCH_GATE_GREP="$W/stub-grep" CHOUSA_GREP_PIN_ECHO=1

# V2 BASH_ENV head() + non-GNU stub.
run V2-bashenv-head-shim integ BASH_ENV="$W/fakehead_env.sh" RESEARCH_GATE_GREP="$W/stub-grep" CHOUSA_GREP_PIN_ECHO=1

# V3 the bypass on the MATCHER surface (verify-claims): if the stub is
# accepted it becomes the matcher and answers nothing.
run V3-path-head-shim-claims claims PATH="$SHIM:$CLEAN" RESEARCH_GATE_GREP="$W/stub-grep" CHOUSA_GREP_PIN_ECHO=1

# V4 control: real grep, same PATH head shim.
run V4-real-grep-path-head-shim claims PATH="$SHIM:$CLEAN" RESEARCH_GATE_GREP=/usr/bin/grep CHOUSA_GREP_PIN_ECHO=1

# V5 control: stub + head shim, but the stub is asked to ALSO log its calls,
# proving it is the binary actually used as the matcher.
cat >"$W/stub-logging-grep" <<EOF
#!/bin/sh
printf '%s\n' "\$*" >>"$W/stub-calls.log" 2>/dev/null
case "\$1" in --version|-V) printf 'grep (pi-uu-grep) 0.2.0\n' >&2; exit 0;; esac
exit 0
EOF
chmod +x "$W/stub-logging-grep"
: >"$W/stub-calls.log"
run V5-logging-stub-bypass claims PATH="$SHIM:$CLEAN" RESEARCH_GATE_GREP="$W/stub-logging-grep" CHOUSA_GREP_PIN_ECHO=1
printf '\n=== V5 stub call log (proves the stub ran as the matcher) ===\n'
cat "$W/stub-calls.log"
