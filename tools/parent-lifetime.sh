#!/usr/bin/env bash
# parent-lifetime.sh — chousa launcher receipt (round 44; exit contract round 45).
# Contract: this process stays alive until every child it spawned has been
# reaped by this same pid. It appends the receipt itself. A pipeline must
# not own the wait. The per-wave seat timeout is required in dispatch mode
# and recorded as timeout_s= in the start line (QUALITY 63).
# Exit 0: end line written, n_spawned > 0, every child reaped, no seat
# timed out. Exit 3: end line written, but zero tasks were spawned or a
# seat exited 124/137 (timeout) — the receipt is complete, the wave is not.
# Exit 1: a child pid was not captured or the parent pid changed. Exit 2:
# usage, including a dispatch run without --timeout.
# The receipt is not proof against a later hand-edit.
set -u

usage() {
  echo "usage: parent-lifetime.sh --dispatch JSON --receipt PATH --agent FILE --timeout SECS" >&2
  echo "       parent-lifetime.sh --selftest --receipt PATH" >&2
  exit 2
}

DISPATCH=""
RECEIPT=""
AGENT=""
TIMEOUT=""
SELFTEST=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dispatch) DISPATCH=${2:?}; shift 2 ;;
    --receipt) RECEIPT=${2:?}; shift 2 ;;
    --agent) AGENT=${2:?}; shift 2 ;;
    --timeout) TIMEOUT=${2:?}; shift 2 ;;
    --selftest) SELFTEST=1; shift ;;
    *) usage ;;
  esac
done
[[ -n "$RECEIPT" ]] || usage
if [[ "$SELFTEST" -eq 1 ]]; then
  TIMEOUT=${TIMEOUT:-0}
else
  [[ "$TIMEOUT" =~ ^[1-9][0-9]*$ ]] || usage
fi

parent_pid=$$
start_epoch=$(date +%s)
mkdir -p -- "$(dirname -- "$RECEIPT")"
: > "$RECEIPT"
printf 'start parent_pid=%s epoch=%s timeout_s=%s\n' "$parent_pid" "$start_epoch" "$TIMEOUT" >> "$RECEIPT"

declare -a NAMES=()
declare -a PIDS=()

if [[ "$SELFTEST" -eq 1 ]]; then
  for name in SelfA SelfB; do
    sleep 0.2 &
    child=$!
    NAMES+=("$name")
    PIDS+=("$child")
    printf 'spawn name=%s child_pid=%s epoch=%s\n' "$name" "$child" "$(date +%s)" >> "$RECEIPT"
  done
else
  [[ -n "$DISPATCH" && -n "$AGENT" && -f "$DISPATCH" && -f "$AGENT" ]] || usage
  mapfile -t TASKS < <(python3 - "$DISPATCH" << 'PY'
import json, sys
doc = json.load(open(sys.argv[1], encoding="utf-8"))
tasks = doc["taskCall"]["tasks"]
for t in tasks:
    # name, then the task text, separated by a unit separator
    sys.stdout.write(t["name"] + "\x1f" + t["task"].replace("\n", "\x1e") + "\n")
PY
)
  logdir=$(dirname -- "$RECEIPT")/seat-logs
  mkdir -p -- "$logdir"
  for row in "${TASKS[@]}"; do
    name=${row%%$'\x1f'*}
    body=${row#*$'\x1f'}
    body=${body//$'\x1e'/$'\n'}
    prompt_file="$logdir/$name.prompt"
    printf '%s\n' "$body" > "$prompt_file"
    # Same shell owns the background pid. Not a pipeline.
    # --auto and --yolo cannot combine with --prompt (kimi 2.3.1). The host
    # default permission mode is already auto, so the flag is omitted.
    timeout --signal=TERM --kill-after=20 "$TIMEOUT" \
      kimi --agent-file "$AGENT" --prompt "$(cat "$prompt_file")" \
      --output-format text > "$logdir/$name.log" 2>&1 &
    child=$!
    if [[ -z "$child" || "$child" -le 0 ]]; then
      echo "parent-lifetime: no pid for $name" >&2
      exit 1
    fi
    NAMES+=("$name")
    PIDS+=("$child")
    printf 'spawn name=%s child_pid=%s epoch=%s\n' "$name" "$child" "$(date +%s)" >> "$RECEIPT"
  done
fi

n_spawned=${#PIDS[@]}
n_reaped=0
n_timeout=0
for i in "${!PIDS[@]}"; do
  child=${PIDS[$i]}
  name=${NAMES[$i]}
  # A bare wait would abort under an inherited errexit and truncate the receipt.
  if wait "$child"; then ec=0; else ec=$?; fi
  n_reaped=$((n_reaped + 1))
  if [[ "$ec" -eq 124 || "$ec" -eq 137 ]]; then
    n_timeout=$((n_timeout + 1))
  fi
  printf 'reap name=%s child_pid=%s exit_code=%s epoch=%s\n' \
    "$name" "$child" "$ec" "$(date +%s)" >> "$RECEIPT"
done

end_epoch=$(date +%s)
if [[ "$$" -ne "$parent_pid" ]]; then
  echo "parent-lifetime: pid changed $$ != $parent_pid" >&2
  exit 1
fi
printf 'end parent_pid=%s epoch=%s n_spawned=%s n_reaped=%s\n' \
  "$$" "$end_epoch" "$n_spawned" "$n_reaped" >> "$RECEIPT"
if [[ "$n_spawned" -eq 0 || "$n_timeout" -gt 0 ]]; then
  echo "parent-lifetime: incomplete wave n_spawned=$n_spawned n_timeout=$n_timeout" >&2
  exit 3
fi
exit 0
