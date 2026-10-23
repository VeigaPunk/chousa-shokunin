#!/usr/bin/env bash
# Round-35 w2 ExecPinModeIntegrity — verify-integrity under the grep pin.
#
# Four environments on the committed integrity fixture (corpus/fixtures/integrity-r7.md):
#   E1 baseline            clean PATH, no shims, no override
#   E2 shim-first PATH     a logging `grep` shim first on PATH (tripwire T1)
#   E3 BASH_ENV fn shim    BASH_ENV defines grep() that logs (tripwire T2)
#   E4 grep-free PATH      symlink farm with no grep at all
# Plus the refusal family (bad RESEARCH_GATE_GREP): relative, missing, non-GNU stub.
#
# Each run reports: exit code, the `INTEGRITY refs=` line, the tripwire byte
# count, and the refusal line (stderr, GREP_PROVENANCE).
#
# Usage: integ-env-probe.sh GATE LABEL OUTDIR
#   GATE   path to the gate to score (sha256 pinned by the caller)
#   LABEL  short label used in the log
#   OUTDIR directory for per-run logs
set -u
GATE=$1; LABEL=$2; OUT=$3
LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin
FIX=$LANE/corpus/fixtures/integrity-r7.md
W=$OUT/$LABEL
mkdir -p "$W"

SHIM=$W/shimbin
mkdir -p "$SHIM"
TRIP1=$W/trip-path.log
TRIP2=$W/trip-fn.log
TRIP3=$W/trip-stub.log
: >"$TRIP1"; : >"$TRIP2"; : >"$TRIP3"

cat >"$SHIM/grep" <<EOF
#!/bin/sh
printf '%s\n' "\$*" >>"$TRIP1" 2>/dev/null
exec /usr/bin/grep "\$@"
EOF
chmod +x "$SHIM/grep"

cat >"$W/bash_env.sh" <<EOF
grep() { printf 'fn %s\n' "\$*" >>"$TRIP2" 2>/dev/null; command /usr/bin/grep "\$@"; }
EOF

# non-GNU stub (self-reports a uutils version, never matches)
cat >"$W/stub-grep" <<EOF
#!/bin/sh
printf 'stub %s\n' "\$*" >>"$TRIP3" 2>/dev/null
case "\$1" in --version|-V) printf '%s\n' >&2; exit 0;; esac
exit 0
EOF
chmod +x "$W/stub-grep"

# grep-free PATH farm: every tool the integrity path needs except grep
NOG=$W/nogrepbin
mkdir -p "$NOG"
for n in bash sh od tr sed cut head tail date wc sort uniq cat mkdir mktemp dirname basename \
         readlink sha256sum stat ls find python3 sleep mv rm cp touch awk env xargs flock printf \
         expr test true false id timeout; do
  for base in /usr/bin /bin; do
    if [[ -f $base/$n && -x $base/$n ]]; then ln -sf "$base/$n" "$NOG/$n" 2>/dev/null; break; fi
  done
done
CLEAN=/usr/local/bin:/usr/bin:/bin

run() { # NAME ENVSPEC...
  local name=$1; shift
  local envspec=()
  while [[ $# -gt 0 ]]; do envspec+=("$1"); shift; done
  local log=$W/$name.log
  : >"$TRIP1"; : >"$TRIP2"; : >"$TRIP3"
  ( cd "$LANE" && env -i PATH="$CLEAN" HOME="$HOME" LANG=C "${envspec[@]}" \
      timeout 300 bash "$GATE" verify-integrity corpus/fixtures/integrity-r7.md --root . ) \
      >"$log.out" 2>"$log.err"
  local rc=$?
  {
    printf '### %s/%s\n' "$LABEL" "$name"
    printf 'exit=%d\n' "$rc"
    printf 'integrity_line=%s\n' "$(grep -m1 '^INTEGRITY refs=' "$log.out" 2>/dev/null || echo NONE)"
    printf 'verdict_line=%s\n' "$(grep -m1 '^RESEARCH_GATE: ' "$log.out" 2>/dev/null || echo NONE)"
    printf 'trip_path_bytes=%s\n' "$(wc -c <"$TRIP1" | tr -d ' ')"
    printf 'trip_fn_bytes=%s\n' "$(wc -c <"$TRIP2" | tr -d ' ')"
    printf 'trip_stub_bytes=%s\n' "$(wc -c <"$TRIP3" | tr -d ' ')"
    printf 'refusal=%s\n' "$(grep -m1 'GREP_PROVENANCE' "$log.err" 2>/dev/null || echo NONE)"
    printf 'grep_line=%s\n' "$(grep -m1 '^GATE_GREP: ' "$log.err" 2>/dev/null || echo NONE)"
    printf 'stdout_lines=%s\n' "$(wc -l <"$log.out" | tr -d ' ')"
  } >>"$W/summary.txt"
  printf '%s\n' "$name done (rc=$rc)"
}

: >"$W/summary.txt"
run E1-baseline
run E2-shim-first-path PATH="$SHIM:$CLEAN"
run E3-bash-env-function BASH_ENV="$W/bash_env.sh"
run E4-grep-free-path PATH="$NOG"
run R1-override-relative RESEARCH_GATE_GREP=bin/grep
run R2-override-missing RESEARCH_GATE_GREP="$W/absent-grep"
run R3-override-non-gnu RESEARCH_GATE_GREP="$W/stub-grep"
run R4-override-real-echo RESEARCH_GATE_GREP=/usr/bin/grep CHOUSA_GREP_PIN_ECHO=1
run R5-default-echo CHOUSA_GREP_PIN_ECHO=1
run R6-override-beats-bashenv BASH_ENV="$W/bash_env.sh" RESEARCH_GATE_GREP=/usr/bin/grep CHOUSA_GREP_PIN_ECHO=1
cat "$W/summary.txt"
