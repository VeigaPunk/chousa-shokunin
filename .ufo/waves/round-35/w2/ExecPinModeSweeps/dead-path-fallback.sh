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
TIMEOUT=/usr/bin/timeout

mkdir -p "$SCRATCH/attack3/fake" "$SCRATCH/attack3/pathbin"

# a NON-GNU stub standing in for /usr/bin/grep and /bin/grep
cat > "$SCRATCH/attack3/fake/grep" <<'EOF'
#!/bin/sh
case "$1" in --version|-V) printf '%s\n' 'grep (pi-uu-grep) 0.2.0' >&2; exit 0;; esac
exit 0
EOF
chmod +x "$SCRATCH/attack3/fake/grep"

# a REAL GNU grep at a non-standard absolute path, placed FIRST on PATH
cp /usr/bin/grep "$SCRATCH/attack3/pathbin/grep"

for label in pinned landed-pinned drift-worktree; do
  case $label in
    pinned) gate=$PINNED ;;
    landed-pinned) gate=$PINNED ;;
    drift-worktree) gate=$DRIFTED ;;
  esac
  printf '=== %s (%s) ===\n' "$label" "$(sha256sum "$gate" | cut -c1-16)"
  unshare --user --map-root-user --mount --propagation private bash -c '
    set -u
    mount --bind "$1/fake/grep" /usr/bin/grep
    [[ -e /bin/grep ]] && mount --bind "$1/fake/grep" /bin/grep
    rc=0
    env -i HOME=/root PATH="$1/pathbin:/usr/local/bin:/usr/bin:/bin" TMPDIR="$1" \
      /usr/bin/timeout 600 bash "$2" verify-sweeps "$3" --root "'"$REPO"'" \
      >"$1/$label.out" 2>"$1/$label.err" || rc=$?
    printf "rc=%s\n" "$rc"
    printf "stderr=%s\n" "$(tr "\n" "|" < "$1/$label.err")"
    printf "stdout_bytes=%s\n" "$(stat -c %s "$1/$label.out")"
    printf "summary=%s\n" "$(grep -m1 "^VERIFIED_SWEEPS=" "$1/$label.out" || true)"
  ' _ "$SCRATCH/attack3" "$gate" "$FIXTURE"
  echo
done

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
echo "### proof that the function shadows the PATH lookup (exact lines 348-351 of the pinned gate)"
sed -n '348,352p' "$PINNED"
echo "--- effect:"
bash -c 'GREP_BIN=""; grep() { command "$GREP_BIN" "$@"; }; c=$(command -v grep 2>/dev/null || true); printf "command -v grep -> [%s]\n" "$c"; case "$c" in /*) echo "arm taken";; *) echo "absolute-path arm NOT taken -> PATH fallback unreachable";; esac'
