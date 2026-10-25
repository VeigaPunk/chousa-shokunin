#!/usr/bin/env bash
# parent-lifetime.sh — chousa round-44 launcher receipt.
# Contract: this process stays alive until every child it spawned has been
# reaped by this same pid. It appends the receipt itself. A pipeline must
# not own the wait. Exit 0 when the end line is written. Exit 1 if a child
# pid was not captured. Exit 2 on usage.
# The receipt is not proof against a later hand-edit. It is the log the
# round-43 closure could not resolve.
set -u

usage() {
  echo "usage: parent-lifetime.sh --dispatch JSON --receipt PATH --agent FILE [--timeout SECS]" >&2
  echo "       parent-lifetime.sh --selftest --receipt PATH" >&2
  exit 2
}

DISPATCH=""
RECEIPT=""
AGENT=""
TIMEOUT=420
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

parent_pid=$$
start_epoch=$(date +%s)
mkdir -p -- "$(dirname -- "$RECEIPT")"
: > "$RECEIPT"
printf 'start parent_pid=%s epoch=%s\n' "$parent_pid" "$start_epoch" >> "$RECEIPT"

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
for i in "${!PIDS[@]}"; do
  child=${PIDS[$i]}
  name=${NAMES[$i]}
  set +e
  wait "$child"
  ec=$?
  set -e
  n_reaped=$((n_reaped + 1))
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
exit 0
