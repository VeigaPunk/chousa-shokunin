#!/usr/bin/env bash
# Re-run of the non-grep PATH attack against the PINNED landed gate blob
# (1f2fb4f5…), because the worktree copy drifted mid-wave.
#
# F4: the pin covers grep only. The sweeps mode's location-boundary decision
# is taken by OTHER PATH-resolved binaries. Two directions:
#   (a) realpath shim collapses every path to "/"  -> in-corpus path REFUSED
#       (false DRIFT: VERIFIED_SWEEPS 1/2 -> 0/2, exit 0 -> exit 1)
#   (b) readlink shim claims every path is the root -> out-of-corpus path
#       ACCEPTED and, when nothing matches, reported VERIFIED (false CLEAN)
set -uo pipefail
REPO=/home/vgpnk/Projects/shokunin/chousa-shokunin
SCRATCH=/tmp/hyaku/chousa-r35/w2/ExecPinModeSweeps
PINNED="$REPO/.ufo/waves/round-35/w2/ExecPinModeSweeps/pinned/tools/research-gate.sh"
FIXTURE="$REPO/corpus/fixtures/sweeps-r5.md"
CLEAN_PATH=/usr/local/bin:/usr/bin:/bin
mkdir -p "$SCRATCH/f4b"

# (a) realpath -> "/"
mkdir -p "$SCRATCH/f4b/realpath-root"
cat > "$SCRATCH/f4b/realpath-root/realpath" <<'EOF'
#!/bin/sh
printf '/\n'
exit 0
EOF
chmod +x "$SCRATCH/f4b/realpath-root/realpath"

# (b) readlink -> the root (claims every path is in-corpus)
mkdir -p "$SCRATCH/f4b/readlink-root"
cat > "$SCRATCH/f4b/readlink-root/readlink" <<EOF
#!/bin/sh
printf '%s\n' "$REPO"
exit 0
EOF
chmod +x "$SCRATCH/f4b/readlink-root/readlink"

# fixture naming an out-of-corpus absolute path that does not exist
cat > "$SCRATCH/f4b/rec-outside.md" <<'EOF'
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
| W1 | N1 | /etc/hyaku-no-such-file-xyz | scanned the outside location |
EOF

go() { # label path record
  local label=$1 path=$2 record=$3 rc=0
  local out="$SCRATCH/f4b/$label.out"
  env -i HOME="$HOME" PATH="$path" TMPDIR="$SCRATCH" \
    /usr/bin/timeout 600 bash "$PINNED" verify-sweeps "$record" --root "$REPO" \
    >"$out" 2>"$SCRATCH/f4b/$label.err" || rc=$?
  printf '=== %s\n' "$label"
  printf '  exit=%s\n' "$rc"
  printf '  summary=%s\n' "$(grep -m1 '^VERIFIED_SWEEPS=' "$out" || true)"
  printf '  verdict=%s\n' "$(grep -m1 '^RESEARCH_GATE: ' "$out" || true)"
  printf '  findings=%s\n' "$(grep '^FINDING ' "$out" || true)"
  printf '  stderr=%s\n' "$(tr '\n' '|' < "$SCRATCH/f4b/$label.err" | cut -c1-200)"
}

echo "########## committed sweep fixture (corpus/fixtures/sweeps-r5.md) ##########"
go committed-clean       "$CLEAN_PATH" "$FIXTURE"
go committed-realpath-root "$SCRATCH/f4b/realpath-root:$CLEAN_PATH" "$FIXTURE"
echo
echo "########## out-of-corpus fixture (own directory) ##########"
go outside-clean         "$CLEAN_PATH" "$SCRATCH/f4b/rec-outside.md"
go outside-readlink-root "$SCRATCH/f4b/readlink-root:$CLEAN_PATH" "$SCRATCH/f4b/rec-outside.md"
