#!/usr/bin/env bash
# Round-35 w2 ExecPinModeIntegrity — attack the pin's OWN provenance check.
#
# grep_pin_verify (research-gate.sh:358-366) reads the candidate's version with
#   v=$("$cand" --version 2>/dev/null | head -n 1 || true)
# `head` is resolved through PATH, so a BASH_ENV-provided head() can rewrite the
# version line the pin believes. If a head() that prints a fake "GNU grep" line
# makes a NON-GNU binary pass the check, the pin's refusal (GREP_PROVENANCE) is
# bypassable — the refusal is the C1 claim's fail-closed half.
#
# Usage: pin-provenance-attack.sh GATE OUTDIR
set -u
GATE=$1; OUT=$2
LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin
W=$OUT/attack
rm -rf "$W"; mkdir -p "$W"

# A non-GNU binary: reports the uutils version, and for a real match returns
# NOTHING (exit 0) — a silent wrong-answer engine if the pin accepts it.
cat >"$W/stub-grep" <<'EOF'
#!/bin/sh
case "$1" in --version|-V) printf 'grep (pi-uu-grep) 0.2.0\n' >&2; exit 0;; esac
exit 0
EOF
chmod +x "$W/stub-grep"

# BASH_ENV that shims `head` for the --version probe only: consume the first
# stdin line and print a fake GNU version. Every other head() use is delegated.
cat >"$W/fakehead_env.sh" <<'EOF'
head() {
  if [[ ${1-} == -n && ${2-} == 1 ]]; then
    local line
    IFS= read -r line || true
    printf 'grep (GNU grep) 3.12-modified\n'
    return 0
  fi
  command head "$@"
}
EOF

CLEAN=/usr/local/bin:/usr/bin:/bin

hdr() { printf '\n=== %s ===\n' "$1"; }

# A1: the stub alone must be refused (the committed S6 behaviour).
hdr "A1 stub-alone (expect exit 2, GREP_PROVENANCE)"
( cd "$LANE" && env -i PATH="$CLEAN" HOME="$HOME" LANG=C \
    RESEARCH_GATE_GREP="$W/stub-grep" CHOUSA_GREP_PIN_ECHO=1 \
    timeout 300 bash "$GATE" verify-integrity corpus/fixtures/integrity-r7.md --root . ) \
    >"$W/A1.out" 2>"$W/A1.err"; echo "exit=$?"
echo "integrity_line=$(grep -m1 '^INTEGRITY refs=' "$W/A1.out" || echo NONE)"
echo "refusal=$(grep -m1 'GREP_PROVENANCE' "$W/A1.err" || echo NONE)"
echo "grep_line=$(grep -m1 '^GATE_GREP: ' "$W/A1.err" || echo NONE)"

# A2: the SAME stub + a BASH_ENV head() shim. If the pin accepts it, the
# provenance refusal is defeatable.
hdr "A2 stub + BASH_ENV head() shim (attack)"
( cd "$LANE" && env -i PATH="$CLEAN" HOME="$HOME" LANG=C BASH_ENV="$W/fakehead_env.sh" \
    RESEARCH_GATE_GREP="$W/stub-grep" CHOUSA_GREP_PIN_ECHO=1 \
    timeout 300 bash "$GATE" verify-integrity corpus/fixtures/integrity-r7.md --root . ) \
    >"$W/A2.out" 2>"$W/A2.err"; echo "exit=$?"
echo "integrity_line=$(grep -m1 '^INTEGRITY refs=' "$W/A2.out" || echo NONE)"
echo "verdict_line=$(grep -m1 '^RESEARCH_GATE: ' "$W/A2.out" || echo NONE)"
echo "refusal=$(grep -m1 'GREP_PROVENANCE' "$W/A2.err" || echo NONE)"
echo "grep_line=$(grep -m1 '^GATE_GREP: ' "$W/A2.err" || echo NONE)"

# A3: same attack against verify-claims — the mode that actually matches spans.
# If the stub is accepted, the matcher answers with the stub (no output) and
# the claim verdicts change.
hdr "A3 stub + head() shim against verify-claims (matcher surface)"
cat >"$W/claims.jsonl" <<'EOF'
{"id":"K1","source":"corpus/fixtures/integrity-r7.md","span":"research-record v1","expect":"supported"}
EOF
( cd "$LANE" && env -i PATH="$CLEAN" HOME="$HOME" LANG=C BASH_ENV="$W/fakehead_env.sh" \
    RESEARCH_GATE_GREP="$W/stub-grep" CHOUSA_GREP_PIN_ECHO=1 \
    timeout 300 bash "$GATE" verify-claims "$W/claims.jsonl" --root . ) \
    >"$W/A3.out" 2>"$W/A3.err"; echo "exit=$?"
echo "claim_line=$(grep -m1 '^CLAIM id=' "$W/A3.out" || echo NONE)"
echo "summary=$(grep -m1 '^VERDICT_BEARING_CLAIMS=' "$W/A3.out" || echo NONE)"
echo "verdict_line=$(grep -m1 '^RESEARCH_GATE: ' "$W/A3.out" || echo NONE)"
echo "refusal=$(grep -m1 'GREP_PROVENANCE' "$W/A3.err" || echo NONE)"
echo "grep_line=$(grep -m1 '^GATE_GREP: ' "$W/A3.err" || echo NONE)"

# A4: the same attack with a REAL GNU grep as the candidate, to separate
# "the head() shim rewrote the version" from "the stub was used".
hdr "A4 real /usr/bin/grep + head() shim (control)"
( cd "$LANE" && env -i PATH="$CLEAN" HOME="$HOME" LANG=C BASH_ENV="$W/fakehead_env.sh" \
    RESEARCH_GATE_GREP=/usr/bin/grep CHOUSA_GREP_PIN_ECHO=1 \
    timeout 300 bash "$GATE" verify-integrity corpus/fixtures/integrity-r7.md --root . ) \
    >"$W/A4.out" 2>"$W/A4.err"; echo "exit=$?"
echo "integrity_line=$(grep -m1 '^INTEGRITY refs=' "$W/A4.out" || echo NONE)"
echo "grep_line=$(grep -m1 '^GATE_GREP: ' "$W/A4.err" || echo NONE)"

# A5: control — the same head() shim WITHOUT an override (default pin). The
# default candidate is /usr/bin/grep (real), so the version line is faked but
# the binary is genuine: the mode must still be CLEAN and identical.
hdr "A5 default pin + head() shim (control)"
( cd "$LANE" && env -i PATH="$CLEAN" HOME="$HOME" LANG=C BASH_ENV="$W/fakehead_env.sh" \
    CHOUSA_GREP_PIN_ECHO=1 \
    timeout 300 bash "$GATE" verify-integrity corpus/fixtures/integrity-r7.md --root . ) \
    >"$W/A5.out" 2>"$W/A5.err"; echo "exit=$?"
echo "integrity_line=$(grep -m1 '^INTEGRITY refs=' "$W/A5.out" || echo NONE)"
echo "grep_line=$(grep -m1 '^GATE_GREP: ' "$W/A5.err" || echo NONE)"

# A6: is the accepted stub actually USED as the matcher? verify-claims on a
# fixture whose span must match: if the stub answers nothing, the claim reads
# unsupported instead of supported. Compare A3 (stub accepted) vs A7 (real).
hdr "A6 verify-claims with REAL grep (control for A3)"
( cd "$LANE" && env -i PATH="$CLEAN" HOME="$HOME" LANG=C \
    RESEARCH_GATE_GREP=/usr/bin/grep CHOUSA_GREP_PIN_ECHO=1 \
    timeout 300 bash "$GATE" verify-claims "$W/claims.jsonl" --root . ) \
    >"$W/A6.out" 2>"$W/A6.err"; echo "exit=$?"
echo "claim_line=$(grep -m1 '^CLAIM id=' "$W/A6.out" || echo NONE)"
echo "summary=$(grep -m1 '^VERDICT_BEARING_CLAIMS=' "$W/A6.out" || echo NONE)"
echo "grep_line=$(grep -m1 '^GATE_GREP: ' "$W/A6.err" || echo NONE)"
