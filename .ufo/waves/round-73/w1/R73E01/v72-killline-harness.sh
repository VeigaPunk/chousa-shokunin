#!/usr/bin/env bash
# V72-1: mirror gate :8426 and :8435 without reading or running the gate.
# Axes: causal precision, repeatability, isolation. Only the driver omits -e;
# each fresh child script explicitly enables the gate's set -euo pipefail.
set -uo pipefail
export LC_ALL=C
work=$(mktemp -d "${TMPDIR:-/tmp}/v72-killline.XXXXXXXX") || exit 1
trap 'rm -rf -- "$work"' EXIT
cd -- "$work" || exit 1

cat > grep-and-list.sh <<'PROBE'
#!/usr/bin/env bash
set -euo pipefail
p36_ok=1
grep -q '^GATE_GREP: ' -- missing-r36-pin.txt && p36_ok=0
rc=$?
printf 'GREP_LIST_RC=%d\n' "$rc"
printf 'GREP_LIST_SURVIVED\n'
PROBE

cat > child-exit-2.sh <<'PROBE'
#!/usr/bin/env bash
printf 'CHILD_DESIGNED_RC=2\n'
exit 2
PROBE

cat > unguarded-assignment.sh <<'PROBE'
#!/usr/bin/env bash
set -euo pipefail
printf 'UNGUARDED_ASSIGNMENT_ENTERED\n'
p36_out=$(bash child-exit-2.sh 2>&1)
printf 'UNGUARDED_ASSIGNMENT_AFTER_MARKER\n'
PROBE

cat > guarded-if.sh <<'PROBE'
#!/usr/bin/env bash
set -euo pipefail
if p36_out=$(bash child-exit-2.sh 2>&1); then
  printf 'UNEXPECTED_ASSIGNMENT_SUCCESS\n'
  exit 1
else
  rc=$?
  printf 'IF_ASSIGNMENT_RC=%d captured=%s\n' "$rc" "$p36_out"
fi
printf 'IF_ASSIGNMENT_SURVIVED\n'
# The final pipeline command succeeds; pipefail must propagate the child rc=2.
if bash child-exit-2.sh | cat; then
  printf 'UNEXPECTED_PIPELINE_SUCCESS\n'
  exit 1
else
  rc=$?
  printf 'IF_PIPELINE_RC=%d\n' "$rc"
fi
printf 'IF_PIPELINE_SURVIVED\n'
PROBE

failures=0
out=''
rc=0
run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  out=$("$@" 2>&1)
  rc=$?
  if [[ -n $out ]]; then printf '%s\n' "$out"; fi
  printf 'rc=%d\n' "$rc"
}
expect() {
  local label=$1 expected_rc=$2 present=$3 absent=${4:-}
  if [[ $rc -eq $expected_rc && $out == *"$present"* &&
        ( -z $absent || $out != *"$absent"* ) ]]; then
    printf 'EXPECT %s: PASS\n' "$label"
  else
    printf 'EXPECT %s: FAIL\n' "$label"
    failures=$((failures + 1))
  fi
}

printf '# Each bash probe below is invoked directly, not in an if/AND/OR context.\n'
for source in grep-and-list.sh child-exit-2.sh unguarded-assignment.sh guarded-if.sh; do
  run cat "$source"
done
run bash grep-and-list.sh
expect grep-list-status 0 'GREP_LIST_RC=2'
expect grep-list-survival 0 'GREP_LIST_SURVIVED'
run bash child-exit-2.sh
expect child-designed-status 2 'CHILD_DESIGNED_RC=2'
run bash unguarded-assignment.sh
expect assignment-terminates 2 'UNGUARDED_ASSIGNMENT_ENTERED' 'UNGUARDED_ASSIGNMENT_AFTER_MARKER'
run bash guarded-if.sh
expect guarded-assignment-status 0 'IF_ASSIGNMENT_RC=2 captured=CHILD_DESIGNED_RC=2'
expect guarded-assignment-survival 0 'IF_ASSIGNMENT_SURVIVED'
expect guarded-pipeline-status 0 'IF_PIPELINE_RC=2'
expect guarded-pipeline-survival 0 'IF_PIPELINE_SURVIVED'
if [[ $failures -eq 0 ]]; then
  printf 'HARNESS: PASS expectations=8/8\n'
  exit 0
fi
printf 'HARNESS: FAIL failures=%d\n' "$failures"
exit 1
