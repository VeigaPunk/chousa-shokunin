#!/usr/bin/env bash
# Round-35 w2 ExecPinModeIntegrity — the pin's verification reads the version
# through an UNPINNED PATH tool (`head`), research-gate.sh:361:
#
#   v=$("$cand" --version 2>/dev/null | head -n 1 || true)
#   case "$v" in *"GNU grep"*) return 0 ;;
#
# Consequences measured here, both directions:
#   D1  `head` ABSENT from PATH -> the genuine /usr/bin/grep cannot be verified
#       -> the gate refuses to run at all (a PATH shim can deny service).
#   D2  `head` PRESENT but silent -> same refusal, on a PATH that has grep.
#   D3  `head` FORGES a GNU line -> a non-GNU binary is accepted as GNU grep
#       (the bypass; see pin-bypass-refined.sh).
#   D4  the same head() under the BASE (pre-pin) gate: the base never reads a
#       version, so it is unaffected -> the landed gate ADDED a PATH dependency.
#
# Usage: pin-head-dependency.sh GATE BASE_GATE OUTDIR
set -u
GATE=$1; BASE=$2; OUT=$3
LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin
W=$OUT/headdep
rm -rf "$W"; mkdir -p "$W"
CLEAN=/usr/local/bin:/usr/bin:/bin

# a PATH with everything the integrity mode needs EXCEPT head
NOHEAD=$W/noheadbin; mkdir -p "$NOHEAD"
for n in bash sh od tr sed cut tail date wc sort uniq cat mkdir mktemp dirname basename \
         readlink sha256sum stat ls find python3 sleep mv rm cp touch awk env xargs flock printf \
         expr test true false id timeout grep; do
  for base in /usr/bin /bin; do
    if [[ -f $base/$n && -x $base/$n ]]; then ln -sf "$base/$n" "$NOHEAD/$n" 2>/dev/null; break; fi
  done
done

# a `head` that prints nothing (consumes stdin, outputs nothing)
SILENT=$W/silentbin; mkdir -p "$SILENT"
cat >"$SILENT/head" <<'EOF'
#!/bin/sh
cat >/dev/null
exit 0
EOF
chmod +x "$SILENT/head"

show() { # NAME RC OUT
  printf '\n=== %s ===\n' "$1"
  printf 'exit=%s\n' "$2"
  printf 'integrity_line=%s\n' "$(printf '%s\n' "$3" | grep -m1 '^INTEGRITY refs=' || echo NONE)"
  printf 'refusal=%s\n' "$(printf '%s\n' "$3" | grep -m1 'GREP_PROVENANCE' || echo NONE)"
  printf 'other_stderr=%s\n' "$(printf '%s\n' "$3" | grep -m1 'research-gate:' | grep -v GREP_PROVENANCE || echo NONE)"
}

r=$( cd "$LANE" && env -i PATH="$NOHEAD" HOME="$HOME" LANG=C \
      timeout 300 bash "$GATE" verify-integrity corpus/fixtures/integrity-r7.md --root . 2>&1 ); rc=$?
show "D1-landed-head-absent-from-PATH" "$rc" "$r"

r=$( cd "$LANE" && env -i PATH="$SILENT:$CLEAN" HOME="$HOME" LANG=C \
      timeout 300 bash "$GATE" verify-integrity corpus/fixtures/integrity-r7.md --root . 2>&1 ); rc=$?
show "D2-landed-head-silent" "$rc" "$r"

r=$( cd "$LANE" && env -i PATH="$NOHEAD" HOME="$HOME" LANG=C \
      timeout 300 bash "$BASE" verify-integrity corpus/fixtures/integrity-r7.md --root . 2>&1 ); rc=$?
show "D4-base-head-absent-from-PATH" "$rc" "$r"

r=$( cd "$LANE" && env -i PATH="$SILENT:$CLEAN" HOME="$HOME" LANG=C \
      timeout 300 bash "$BASE" verify-integrity corpus/fixtures/integrity-r7.md --root . 2>&1 ); rc=$?
show "D4b-base-head-silent" "$rc" "$r"

# D5: the base gate under the forged-version PATH shim, for symmetry: the base
# resolves bare grep through PATH, so a PATH *grep* shim IS honoured there.
GSHIM=$W/gshim; mkdir -p "$GSHIM"
cat >"$GSHIM/grep" <<EOF
#!/bin/sh
printf 'base-grep-shim %s\n' "\$*" >>"$W/base-grep-calls.log" 2>/dev/null
exec /usr/bin/grep "\$@"
EOF
chmod +x "$GSHIM/grep"
: >"$W/base-grep-calls.log"
r=$( cd "$LANE" && env -i PATH="$GSHIM:$CLEAN" HOME="$HOME" LANG=C \
      timeout 300 bash "$BASE" verify-integrity corpus/fixtures/integrity-r7.md --root . 2>&1 ); rc=$?
show "D5-base-grep-shim-on-PATH (integrity mode)" "$rc" "$r"
printf 'base-grep-shim call count (integrity mode)=%s\n' "$(wc -l <"$W/base-grep-calls.log" | tr -d ' ')"

# D6: the same base grep shim on the CLAIMS mode — the surface the pin covers.
: >"$W/base-grep-calls.log"
cat >"$W/claims.jsonl" <<'EOF'
{"id":"K1","source":"corpus/fixtures/integrity-r7.md","span":"research-record v1","expect":"supported"}
EOF
r=$( cd "$LANE" && env -i PATH="$GSHIM:$CLEAN" HOME="$HOME" LANG=C \
      timeout 300 bash "$BASE" verify-claims "$W/claims.jsonl" --root . 2>&1 ); rc=$?
printf '\n=== D6-base-grep-shim-on-PATH (claims mode) ===\n'
printf 'exit=%s\n' "$rc"
printf 'claim_line=%s\n' "$(printf '%s\n' "$r" | grep -m1 '^CLAIM id=' || echo NONE)"
printf 'base-grep-shim call count (claims mode)=%s\n' "$(wc -l <"$W/base-grep-calls.log" | tr -d ' ')"
