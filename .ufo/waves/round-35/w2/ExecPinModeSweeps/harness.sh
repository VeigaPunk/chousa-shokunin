#!/usr/bin/env bash
# Round-35 w2 / ExecPinModeSweeps — scoped attack on mode `verify-sweeps` under
# the landed grep pin. Read-only against the lane; all writes under this seat's
# own directory (/tmp scratch + .ufo/waves/round-35/w2/ExecPinModeSweeps/).
#
# Four environments on the committed sweep fixture + a refused override.
set -uo pipefail

REPO=/home/vgpnk/Projects/shokunin/chousa-shokunin
HERE=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-35/w2/ExecPinModeSweeps
SCRATCH=/tmp/hyaku/chousa-r35/w2/ExecPinModeSweeps
GATE="$REPO/tools/research-gate.sh"
BASE_GATE="$SCRATCH/clone/tools/research-gate.sh"
FIXTURE="$REPO/corpus/fixtures/sweeps-r5.md"
REAL_GREP=/usr/bin/grep
TIMEOUT=/usr/bin/timeout

rm -rf "$SCRATCH/run"; mkdir -p "$SCRATCH/run"

norm() { sed -E 's/ts=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]+Z/ts=TS/'; }
summary_of() { grep -m1 '^VERIFIED_SWEEPS=' "$1" 2>/dev/null || true; }
verdict_of() { grep -m1 '^RESEARCH_GATE: ' "$1" 2>/dev/null || true; }

# ---- shim construction ------------------------------------------------------
SHIMDIR="$SCRATCH/shim"
rm -rf "$SHIMDIR"; mkdir -p "$SHIMDIR/bin" "$SHIMDIR/hostile"
TRIP_PATH="$SHIMDIR/trip-path.log"
TRIP_FN="$SHIMDIR/trip-fn.log"
TRIP_HOSTILE="$SHIMDIR/hostile/trip-hostile.log"

cat > "$SHIMDIR/bin/grep" <<EOF
#!/bin/sh
printf '%s\n' "\$*" >>"$TRIP_PATH" 2>/dev/null
exec $REAL_GREP "\$@"
EOF
chmod +x "$SHIMDIR/bin/grep"

# hostile grep: prints nothing, exit 0 — a wrong matcher that any
# grep-dependent mode must notice.
cat > "$SHIMDIR/hostile/grep" <<EOF
#!/bin/sh
printf 'hostile %s\n' "\$*" >>"$TRIP_HOSTILE" 2>/dev/null
exit 0
EOF
chmod +x "$SHIMDIR/hostile/grep"

cat > "$SHIMDIR/bash_env.sh" <<EOF
grep() { printf 'fn %s\n' "\$*" >>"$TRIP_FN" 2>/dev/null; command $REAL_GREP "\$@"; }
EOF

NOGREP="$SCRATCH/nogrepbin"
rm -rf "$NOGREP"; mkdir -p "$NOGREP"
TOOLS="bash sh od tr sed cut head tail date wc sort uniq cat mkdir mktemp dirname basename readlink sha256sum stat ls find python3 sleep mv rm cp touch awk env xargs flock printf expr test true false id realpath timeout grep-free"
for n in $TOOLS; do
  for base in /usr/bin /bin; do
    p="$base/$n"
    if [[ -f $p && -x $p && ! -e "$NOGREP/$n" ]]; then ln -s "$p" "$NOGREP/$n"; break; fi
  done
done
CLEAN_PATH=/usr/local/bin:/usr/bin:/bin

# ---- run one environment ----------------------------------------------------
run_env() { # NAME GATE PATH ENVSPEC
  local name=$1 gate=$2 path=$3 envspec=$4
  local dir="$SCRATCH/run/$name"
  rm -rf "$dir"; mkdir -p "$dir"
  : > "$TRIP_PATH"; : > "$TRIP_FN"; : > "$TRIP_HOSTILE"
  local out="$dir/stdout.txt" err="$dir/stderr.txt" rc=0
  # shellcheck disable=SC2086
  env -i HOME="$HOME" PATH="$path" TMPDIR="$SCRATCH" \
      ${envspec:+$(printf '%s' "$envspec" | tr '|' ' ')} \
      "$TIMEOUT" 600 bash "$gate" verify-sweeps "$FIXTURE" --root "$REPO" \
      >"$out" 2>"$err" || rc=$?
  printf '%s\n' "$rc" > "$dir/rc.txt"
  norm < "$out" > "$dir/stdout.norm"
  printf '=== %s ===\n' "$name"
  printf 'rc=%s\n' "$rc"
  printf 'summary=%s\n' "$(summary_of "$out")"
  printf 'verdict=%s\n' "$(verdict_of "$out")"
  printf 'trip_path_bytes=%s trip_fn_bytes=%s trip_hostile_bytes=%s\n' \
    "$(stat -c %s "$TRIP_PATH")" "$(stat -c %s "$TRIP_FN")" "$(stat -c %s "$TRIP_HOSTILE")"
  printf 'stderr=%s\n' "$(tr '\n' '|' < "$err" | cut -c1-500)"
  printf 'stdout_norm_sha=%s\n' "$(sha256sum < "$dir/stdout.norm" | cut -d' ' -f1)"
  if [[ -s "$TRIP_PATH" ]]; then printf 'TRIP_PATH_CONTENT:\n%s\n' "$(cut -c1-300 "$TRIP_PATH")"; fi
  if [[ -s "$TRIP_FN" ]]; then printf 'TRIP_FN_CONTENT:\n%s\n' "$(cut -c1-300 "$TRIP_FN")"; fi
  if [[ -s "$TRIP_HOSTILE" ]]; then printf 'TRIP_HOSTILE_CONTENT:\n%s\n' "$(cut -c1-300 "$TRIP_HOSTILE")"; fi
}

echo "### pins"
sha256sum "$GATE" "$BASE_GATE" "$FIXTURE"
echo "### no-grep PATH contains grep? $(ls "$NOGREP" | grep -c '^grep$') (0 expected)"
echo

echo "########## LANDED GATE (sha 1f2fb4f5…) ##########"
run_env E1-clean          "$GATE" "$CLEAN_PATH" ""
run_env E2-shim-first-path "$GATE" "$SHIMDIR/bin:$CLEAN_PATH" ""
run_env E3-bash-env-function "$GATE" "$CLEAN_PATH" "BASH_ENV=$SHIMDIR/bash_env.sh"
run_env E4-no-grep-on-path "$GATE" "$NOGREP" ""
run_env E5-hostile-grep-on-path "$GATE" "$SHIMDIR/hostile:$CLEAN_PATH" ""
echo

echo "########## BASE GATE (round-34 blob a6307edf…, NO pin) ##########"
run_env B1-clean          "$BASE_GATE" "$CLEAN_PATH" ""
run_env B2-shim-first-path "$BASE_GATE" "$SHIMDIR/bin:$CLEAN_PATH" ""
run_env B3-bash-env-function "$BASE_GATE" "$CLEAN_PATH" "BASH_ENV=$SHIMDIR/bash_env.sh"
run_env B4-no-grep-on-path "$BASE_GATE" "$NOGREP" ""
run_env B5-hostile-grep-on-path "$BASE_GATE" "$SHIMDIR/hostile:$CLEAN_PATH" ""
echo

# ---- refused override -------------------------------------------------------
echo "########## OVERRIDE REFUSALS ##########"
ovr() { # NAME ENVSRC
  local name=$1 envsrc=$2 rc=0
  local out="$SCRATCH/run/$name.stdout" err="$SCRATCH/run/$name.stderr"
  : > "$TRIP_PATH"; : > "$TRIP_FN"; : > "$TRIP_HOSTILE"
  # shellcheck disable=SC2086
  env -i HOME="$HOME" PATH="$CLEAN_PATH" TMPDIR="$SCRATCH" $envsrc \
    "$TIMEOUT" 600 bash "$GATE" verify-sweeps "$FIXTURE" --root "$REPO" \
    >"$out" 2>"$err" || rc=$?
  printf '%s rc=%s stdout_bytes=%s\n' "$name" "$rc" "$(stat -c %s "$out")"
  printf '  stderr=%s\n' "$(tr '\n' '|' < "$err")"
  printf '  summary=%s\n' "$(summary_of "$out")"
  printf '  trip_path=%s trip_hostile=%s\n' "$(stat -c %s "$TRIP_PATH")" "$(stat -c %s "$TRIP_HOSTILE")"
}
ovr OVR-relative "RESEARCH_GATE_GREP=bin/grep"
ovr OVR-missing  "RESEARCH_GATE_GREP=/tmp/hyaku/chousa-r35/w2/ExecPinModeSweeps/run/absent-grep"

# non-GNU stub
cat > "$SCRATCH/run/stub-grep" <<'EOF'
#!/bin/sh
printf 'stub %s\n' "$*" >>"/tmp/hyaku/chousa-r35/w2/ExecPinModeSweeps/run/trip-stub.log" 2>/dev/null
case "$1" in --version|-V) printf '%s\n' 'grep (pi-uu-grep) 0.2.0' >&2; exit 0;; esac
exit 0
EOF
chmod +x "$SCRATCH/run/stub-grep"
: > "$SCRATCH/run/trip-stub.log"
ovr OVR-non-gnu-stub "RESEARCH_GATE_GREP=$SCRATCH/run/stub-grep"
printf '  stub_calls=%s\n' "$(wc -l < "$SCRATCH/run/trip-stub.log")"

ovr OVR-ok-override-echo "RESEARCH_GATE_GREP=$REAL_GREP CHOUSA_GREP_PIN_ECHO=1"
ovr DEF-echo "CHOUSA_GREP_PIN_ECHO=1"
