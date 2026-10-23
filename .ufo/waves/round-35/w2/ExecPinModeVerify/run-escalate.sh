#!/usr/bin/env bash
# ExecPinModeVerify escalation: can a PATH 'head' shim make the gate PIN AND USE a
# non-GNU grep, producing a DIFFERENT (wrong) verdict from the honest run?
set -u
D=/tmp/hyaku/chousa-r35/w2/ExecPinModeVerify
CLONE=$D/clone
OUT=$D/out4
mkdir -p "$OUT"

# 'gnu-liar': behaves like grep but WITHOUT -z (multi-line/offset) support,
# and self-reports as pi-uu-grep so grep_pin_verify MUST refuse it.
cat > "$D/gnu-liar" <<'EOF'
#!/bin/sh
case "$1" in --version|-V) printf '%s\n' "grep (pi-uu-grep) 0.2.0"; exit 0;; esac
args=""
for a in "$@"; do
  case "$a" in -z) continue;; esac
  args="$args '$a'"
done
eval "exec /usr/bin/grep $args"
EOF
chmod 755 "$D/gnu-liar"

# Surgical head shim: lie only on the pi-uu-grep version banner.
mkdir -p "$D/shim4"
cat > "$D/shim4/head" <<'EOF'
#!/bin/sh
tmp=$(mktemp); cat > "$tmp"
if grep -q 'pi-uu-grep' "$tmp" 2>/dev/null; then
  printf '%s\n' "grep (GNU grep) 3.12-modified"
else
  exec /usr/bin/head "$@" < "$tmp"
fi
rm -f "$tmp"
EOF
chmod 755 "$D/shim4/head"

# Claim fixture: a multi-line span whose -z match needs -z.
R=$D/croot; mkdir -p "$R/src"
printf 'alpha\nbravo\ncharlie\ndelta\n' > "$R/src/multi.md"
cat > "$R/claims.jsonl" <<'EOF'
{"id":"M1","source":"src/multi.md","span":"bravo\ncharlie","expect":"supported"}
EOF

run() { # name path rgrep mode
  local name=$1 p=$2 rg=${3:-} mode=${4:-verify-claims}
  ( cd "$CLONE" && env -i HOME=/tmp PATH="$p" ${rg:+RESEARCH_GATE_GREP="$rg"} \
      CHOUSA_NOW_EPOCH=1750000000 \
      bash tools/research-gate.sh "$mode" "$R/claims.jsonl" --root "$R" \
      >"$OUT/$name.out" 2>"$OUT/$name.err"; echo $? > "$OUT/$name.rc" )
  echo "=== $name rc=$(cat "$OUT/$name.rc")"
  grep -hE '^RESEARCH_GATE: |^CLAIM |^VERDICT_BEARING_CLAIMS' "$OUT/$name.out" | sed 's/^/    /'
  grep -hE 'GREP_PROVENANCE|GATE_GREP:|GNU grep with' "$OUT/$name.err" | sed 's/^/    ERR: /' || true
}

echo "### E1 honest: real GNU grep, no shim (reference)"
run E1-honest "/usr/local/bin:/usr/bin:/bin" "" verify-claims
echo "### E2 non-GNU override, NO head shim -> expect exit 2 refusal"
run E2-refused "/usr/local/bin:/usr/bin:/bin" "$D/gnu-liar" verify-claims
echo "### E3 non-GNU override WITH head shim -> expect pin accepted (bypass)"
run E3-bypassed "$D/shim4:/usr/local/bin:/usr/bin:/bin" "$D/gnu-liar" verify-claims
echo "### E4 same record in verify mode, honest vs bypass"
run E4-honest-verify "/usr/local/bin:/usr/bin:/bin" "" verify
run E5-bypass-verify "$D/shim4:/usr/local/bin:/usr/bin:/bin" "$D/gnu-liar" verify
