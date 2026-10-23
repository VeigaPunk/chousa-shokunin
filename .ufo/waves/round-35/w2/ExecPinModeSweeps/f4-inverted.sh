#!/usr/bin/env bash
# F4 inverted test: a `realpath` shim that ECHOES ITS ARGUMENT unchanged
# makes sweep_path_guarded accept an out-of-corpus absolute path, because the
# guard canonicalises with realpath -m and compares prefixes. If that flips a
# DRIFT verdict to CLEAN, the pin (which covers grep only) leaves the sweeps
# verdict a function of the caller's PATH — and the failure is SILENT
# (a false CLEAN), not a loud refusal.
#
# Fixture: my own directory (not a committed lane file).
set -uo pipefail
REPO=/home/vgpnk/Projects/shokunin/chousa-shokunin
SCRATCH=/tmp/hyaku/chousa-r35/w2/ExecPinModeSweeps
PINNED="$REPO/.ufo/waves/round-35/w2/ExecPinModeSweeps/pinned/tools/research-gate.sh"
CLEAN_PATH=/usr/local/bin:/usr/bin:/bin
mkdir -p "$SCRATCH/f4"

cat > "$SCRATCH/f4/outside.md" <<'EOF'
outside the corpus
EOF

cat > "$SCRATCH/f4/rec-outside.md" <<'EOF'
# research-record v1
<!-- chousa-record: v1 -->
## Question

Does the sweep boundary refuse a location outside the corpus?

## Rejections

| id | ref | reason | flip_condition |
|---|---|---|---|
| R1 | research/README.md:12 | a reason | a flip |

## Sweeps

| id | claim_id | where | observed |
|---|---|---|---|
| W1 | N1 | /etc/hostname | scanned the outside location |
EOF

mkdir -p "$SCRATCH/f4/realpath-echo"
cat > "$SCRATCH/f4/realpath-echo/realpath" <<'EOF'
#!/bin/sh
# claim every path canonicalises to itself (i.e. no resolution happens)
for a in "$@"; do
  case "$a" in -m) continue;; esac
  printf '%s\n' "$a"
  break
done
exit 0
EOF
chmod +x "$SCRATCH/f4/realpath-echo/realpath"

mkdir -p "$SCRATCH/f4/realpath-root"
cat > "$SCRATCH/f4/realpath-root/realpath" <<'EOF'
#!/bin/sh
# claim every path canonicalises to the root (in-corpus) -> silent accept
printf '%s\n' "$FAKE_ROOT"
exit 0
EOF
chmod +x "$SCRATCH/f4/realpath-root/realpath"

go() { # label path
  local label=$1 path=$2 rc=0
  local out="$SCRATCH/f4/$label.out"
  env -i HOME="$HOME" PATH="$path" TMPDIR="$SCRATCH" \
    /usr/bin/timeout 600 bash "$PINNED" verify-sweeps "$SCRATCH/f4/rec-outside.md" --root "$REPO" \
    >"$out" 2>"$SCRATCH/f4/$label.err" || rc=$?
  printf '--- %s\n  exit=%s\n  summary=%s\n  verdict=%s\n' "$label" "$rc" \
    "$(grep -m1 '^VERIFIED_SWEEPS=' "$out" || true)" "$(grep -m1 '^RESEARCH_GATE: ' "$out" || true)"
  printf '  findings=%s\n' "$(grep '^FINDING ' "$out" || true)"
}

go clean "$CLEAN_PATH"
go realpath-echo "$SCRATCH/f4/realpath-echo:$CLEAN_PATH"
FAKE_ROOT="$REPO" go realpath-root "$SCRATCH/f4/realpath-root:$CLEAN_PATH"
