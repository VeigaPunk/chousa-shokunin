#!/usr/bin/env bash
# ExecPinModeVerify attacks on the pin itself, in `verify` mode.
set -u
BASE=/tmp/hyaku/chousa-r35/w2/ExecPinModeVerify
CLONE=$BASE/clone
OUT=$BASE/out3
TRIP=$BASE/tripwire3
CLEANPATH=/usr/local/bin:/usr/bin:/bin
RECORD=corpus/fixtures/archives-r9/A-r9.md
ROOT=$BASE/root
CLOCK=1750000000
mkdir -p "$OUT" "$TRIP" "$BASE/shim2"

# A stub that is NOT GNU grep and prints its version on STDOUT.
cat > "$BASE/stub-non-gnu" <<'EOF'
#!/bin/sh
case "$1" in --version|-V) printf '%s\n' "grep (pi-uu-grep) 0.2.0"; exit 0;; esac
printf '%s\n' "$*" >>"/tmp/hyaku/chousa-r35/w2/ExecPinModeVerify/tripwire3/stub.log"
exit 0
EOF
chmod 755 "$BASE/stub-non-gnu"

# A PATH shim for `head` that ALWAYS claims GNU grep (provenance spoof).
cat > "$BASE/shim2/head" <<'EOF'
#!/bin/sh
printf '%s\n' "grep (GNU grep) 3.12-modified"
EOF
chmod 755 "$BASE/shim2/head"

run() { # NAME PATH [RGREP] [ECHO]
  local name=$1 p=$2 rg=${3:-} ec=${4:-}
  ( cd "$CLONE" && env -i HOME=/tmp PATH="$p" \
      ${rg:+RESEARCH_GATE_GREP="$rg"} ${ec:+CHOUSA_GREP_PIN_ECHO="$ec"} \
      CHOUSA_NOW_EPOCH="$CLOCK" \
      bash tools/research-gate.sh verify --record "$RECORD" --root "$ROOT" \
      >"$OUT/$name.out" 2>"$OUT/$name.err"; echo $? > "$OUT/$name.rc" )
  printf '=== %s rc=%s\n' "$name" "$(cat "$OUT/$name.rc")"
  printf '  stdout: %s\n' "$(grep -h '^RESEARCH_GATE: ' "$OUT/$name.out" || echo '(no verdict line)')"
  printf '  stderr: %s\n' "$(grep -hE 'GREP_PROVENANCE|GATE_GREP:' "$OUT/$name.err" | head -2 || true)"
}

: > "$TRIP/stub.log"
echo "### A1: non-GNU override WITHOUT head shim (expect refusal)"
run A1-nonGNU-override "$CLEANPATH" "$BASE/stub-non-gnu"

echo "### A2: non-GNU override WITH head spoof shim (expect ??? )"
run A2-nonGNU-override-headspoof "$BASE/shim2:$CLEANPATH" "$BASE/stub-non-gnu"

echo "### A3: same but with echo, to see which binary got pinned"
run A3-headspoof-echo "$BASE/shim2:$CLEANPATH" "$BASE/stub-non-gnu" "1"

echo "### A4: relative override (expect exit 2 refusal)"
run A4-relative "$CLEANPATH" "bin/grep"

echo "### A5: missing override (expect exit 2 refusal)"
run A5-missing "$CLEANPATH" "$BASE/does-not-exist"

echo "### A6: PATH without any grep at all, default pin (expect CLEAN, pin absolute)"
mkdir -p "$BASE/nogrepbin"
for t in bash sh od tr sed cut head tail date wc sort uniq cat mkdir mktemp dirname basename readlink sha256sum stat ls find python3 sleep mv rm cp touch awk env xargs flock printf expr test true false id; do
  for b in /usr/bin /bin; do [ -x "$b/$t" ] && { ln -sf "$b/$t" "$BASE/nogrepbin/$t" 2>/dev/null; break; }; done
done
run A6-nogrep-on-path "$BASE/nogrepbin"

echo "### stub invocation count (A2/A3 runs):"
wc -c "$TRIP/stub.log" 2>/dev/null || echo "  (no stub log)"
echo "### A6 stderr tail:"
tail -3 "$OUT/A6-nogrep-on-path.err"
