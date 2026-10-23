#!/usr/bin/env bash
# Attack 3: the PINNED landed gate (sha 1f2fb4f5…) default branch.
#
# grep_pin_init's fallback consults `command -v grep`, but the script defines
# a shell FUNCTION named grep at line 351 BEFORE grep_pin_init runs. In bash a
# function shadows the PATH lookup, so `command -v grep` answers "grep"
# (the function), not an absolute path; the `case "$c" in /*)` arm therefore
# never matches and the "or on PATH" arm of the refusal message is DEAD CODE.
#
# End-to-end measurement: make /usr/bin/grep and /bin/grep both fail the GNU
# check (non-GNU stubs, bind-mounted inside a private user namespace so the
# host is untouched) and put a REAL GNU grep on PATH at a non-standard
# absolute path. The pinned gate must then refuse with a message that claims
# it looked on PATH — while a working GNU grep was on PATH.
set -uo pipefail
REPO=/home/vgpnk/Projects/shokunin/chousa-shokunin
SCRATCH=/tmp/hyaku/chousa-r35/w2/ExecPinModeSweeps
PINNED="$REPO/.ufo/waves/round-35/w2/ExecPinModeSweeps/pinned/tools/research-gate.sh"
DRIFTED="$REPO/tools/research-gate.sh"
FIXTURE="$REPO/corpus/fixtures/sweeps-r5.md"

mkdir -p "$SCRATCH/attack3/fake" "$SCRATCH/attack3/pathbin"

cat > "$SCRATCH/attack3/fake/grep" <<'EOF'
#!/bin/sh
case "$1" in --version|-V) printf '%s\n' 'grep (pi-uu-grep) 0.2.0' >&2; exit 0;; esac
exit 0
EOF
chmod +x "$SCRATCH/attack3/fake/grep"
cp /usr/bin/grep "$SCRATCH/attack3/pathbin/grep"

ns_run() { # label gate
  local label=$1 gate=$2
  printf '=== %s (%s) ===\n' "$label" "$(sha256sum "$gate" | cut -c1-16)"
  unshare --user --map-root-user --mount --propagation private bash -c '
    set -u
    L=$1; G=$2; F=$3; A=$4; REPO=$5
    mount --bind "$A/fake/grep" /usr/bin/grep
    if [[ -e /bin/grep ]] && ! [[ -L /bin/grep ]]; then mount --bind "$A/fake/grep" /bin/grep; fi
    rc=0
    env -i HOME=/root PATH="$A/pathbin:/usr/local/bin:/usr/bin:/bin" TMPDIR="$A" \
      /usr/bin/timeout 600 bash "$G" verify-sweeps "$F" --root "$REPO" \
      >"$A/$L.out" 2>"$A/$L.err" || rc=$?
    printf "rc=%s\n" "$rc"
    printf "stderr=%s\n" "$(tr "\n" "|" < "$A/$L.err")"
    printf "stdout_bytes=%s\n" "$(stat -c %s "$A/$L.out")"
    printf "summary=%s\n" "$(grep -m1 "^VERIFIED_SWEEPS=" "$A/$L.out" || true)"
  ' _ "$label" "$gate" "$FIXTURE" "$SCRATCH/attack3" "$REPO"
  echo
}

ns_run pinned "$PINNED"
ns_run drift-worktree "$DRIFTED"

echo "### control: same namespace, real /usr/bin/grep (no stub bind-mount)"
unshare --user --map-root-user --mount --propagation private bash -c '
  set -u
  rc=0
  env -i HOME=/root PATH="/usr/local/bin:/usr/bin:/bin" TMPDIR="$1" \
    /usr/bin/timeout 600 bash "$2" verify-sweeps "$3" --root "'"$REPO"'" \
    >"$1/control.out" 2>"$1/control.err" || rc=$?
  printf "rc=%s stderr=%s\n" "$rc" "$(tr "\n" "|" < "$1/control.err")"
  printf "summary=%s\n" "$(grep -m1 "^VERIFIED_SWEEPS=" "$1/control.out" || true)"
' _ "$SCRATCH/attack3" "$PINNED" "$FIXTURE"
echo

echo "### proof that the function shadows the PATH lookup (pinned gate lines 348-352)"
sed -n '348,352p' "$PINNED"
echo "--- effect:"
bash -c 'GREP_BIN=""; grep() { command "$GREP_BIN" "$@"; }; c=$(command -v grep 2>/dev/null || true); printf "command -v grep -> [%s]\n" "$c"; case "$c" in /*) echo "arm taken";; *) echo "absolute-path arm NOT taken -> PATH fallback unreachable";; esac'
