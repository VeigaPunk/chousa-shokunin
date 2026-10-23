#!/usr/bin/env bash
# Attack 2: the pin covers grep only. verify-sweeps' location-boundary
# decision is taken by OTHER PATH-resolved binaries (readlink, realpath, cd,
# pwd, sed, tr, head). A shim for one of those changes the sweeps verdict
# without touching grep at all -> the pin does not make the mode's verdict
# environment-independent.
set -uo pipefail
REPO=/home/vgpnk/Projects/shokunin/chousa-shokunin
SCRATCH=/tmp/hyaku/chousa-r35/w2/ExecPinModeSweeps
GATE="$REPO/tools/research-gate.sh"
FIXTURE="$REPO/corpus/fixtures/sweeps-r5.md"
TIMEOUT=/usr/bin/timeout
CLEAN_PATH=/usr/local/bin:/usr/bin:/bin

mkdir -p "$SCRATCH/attack2"

go() { # NAME PATH
  local name=$1 path=$2 rc=0
  local out="$SCRATCH/attack2/$name.stdout" err="$SCRATCH/attack2/$name.stderr"
  env -i HOME="$HOME" PATH="$path" TMPDIR="$SCRATCH" \
    "$TIMEOUT" 600 bash "$GATE" verify-sweeps "$FIXTURE" --root "$REPO" \
    >"$out" 2>"$err" || rc=$?
  printf '=== %s ===\n' "$name"
  printf 'rc=%s\n' "$rc"
  printf 'summary=%s\n' "$(grep -m1 '^VERIFIED_SWEEPS=' "$out" || true)"
  printf 'verdict=%s\n' "$(grep -m1 '^RESEARCH_GATE: ' "$out" || true)"
  printf 'findings:\n%s\n' "$(grep '^FINDING ' "$out" || true)"
}

# A1: realpath shim that collapses every path to "/" -> boundary guard denies
mkdir -p "$SCRATCH/attack2/realpath-shim"
cat > "$SCRATCH/attack2/realpath-shim/realpath" <<'EOF'
#!/bin/sh
# ignore arguments, claim everything canonicalises to /
printf '/\n'
exit 0
EOF
chmod +x "$SCRATCH/attack2/realpath-shim/realpath"
go A1-realpath-shim "$SCRATCH/attack2/realpath-shim:$CLEAN_PATH"

# A2: realpath shim that fails (exit 1) -> canon falls back to the raw path
mkdir -p "$SCRATCH/attack2/realpath-fail"
cat > "$SCRATCH/attack2/realpath-fail/realpath" <<'EOF'
#!/bin/sh
exit 1
EOF
chmod +x "$SCRATCH/attack2/realpath-fail/realpath"
go A2-realpath-fails "$SCRATCH/attack2/realpath-fail:$CLEAN_PATH"

# A3: readlink shim that reports every path as outside the root
mkdir -p "$SCRATCH/attack2/readlink-shim"
cat > "$SCRATCH/attack2/readlink-shim/readlink" <<'EOF'
#!/bin/sh
# report a path that is outside every root
printf '/etc/elsewhere\n'
exit 0
EOF
chmod +x "$SCRATCH/attack2/readlink-shim/readlink"
go A3-readlink-shim "$SCRATCH/attack2/readlink-shim:$CLEAN_PATH"

# A4: sed shim that drops every line (table_rows uses sed for cell trimming)
mkdir -p "$SCRATCH/attack2/sed-shim"
cat > "$SCRATCH/attack2/sed-shim/sed" <<'EOF'
#!/bin/sh
exit 0
EOF
chmod +x "$SCRATCH/attack2/sed-shim/sed"
go A4-sed-shim "$SCRATCH/attack2/sed-shim:$CLEAN_PATH"

# A5: tr shim that deletes every character
mkdir -p "$SCRATCH/attack2/tr-shim"
cat > "$SCRATCH/attack2/tr-shim/tr" <<'EOF'
#!/bin/sh
exit 0
EOF
chmod +x "$SCRATCH/attack2/tr-shim/tr"
go A5-tr-shim "$SCRATCH/attack2/tr-shim:$CLEAN_PATH"

# A6: clean control
go A6-clean "$CLEAN_PATH"
