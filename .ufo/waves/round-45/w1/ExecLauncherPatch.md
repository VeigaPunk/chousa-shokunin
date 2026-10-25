# ExecLauncherPatch — round 45 wave 1 report

Seat: L1Chousa45.ExecLauncherPatch (fleet executor, leaf)
Date: 2026-10-25
Item: probe + build the launcher exit contract (C1, operability axis).
No fetch; no production writes. Only files written: the patched copy under
/tmp/chousa-r45-ExecLauncherPatch/ and this report.

## Deliverable

Patched copy: /tmp/chousa-r45-ExecLauncherPatch/parent-lifetime.sh
(4197 bytes, sha256 4a5a2a48d9f84c2b12a35e5ba1d454f8a9c5bfa6cb8d1b7d6d47f17d92457a2)
Base: lane tool /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/parent-lifetime.sh
(blob 79ee8f29… = round-44 control, CASES_MATCH=1/5).

## Unified diff vs the lane tool (verbatim)

--- /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/parent-lifetime.sh	2026-10-24 21:49:24.365738999 -0300
+++ /tmp/chousa-r45-ExecLauncherPatch/parent-lifetime.sh	2026-10-25 06:35:21.509421374 -0300
@@ -18,24 +18,29 @@
 RECEIPT=""
 AGENT=""
 TIMEOUT=420
+TIMEOUT_SET=0
 SELFTEST=0
 while [[ $# -gt 0 ]]; do
   case "$1" in
     --dispatch) DISPATCH=${2:?}; shift 2 ;;
     --receipt) RECEIPT=${2:?}; shift 2 ;;
     --agent) AGENT=${2:?}; shift 2 ;;
-    --timeout) TIMEOUT=${2:?}; shift 2 ;;
+    --timeout) TIMEOUT=${2:?}; TIMEOUT_SET=1; shift 2 ;;
     --selftest) SELFTEST=1; shift ;;
     *) usage ;;
   esac
 done
 [[ -n "$RECEIPT" ]] || usage
+# Dispatch mode must name a timeout; the receipt start line carries it.
+if [[ "$SELFTEST" -eq 0 && "$TIMEOUT_SET" -eq 0 ]]; then
+  usage
+fi
 
 parent_pid=$$
 start_epoch=$(date +%s)
 mkdir -p -- "$(dirname -- "$RECEIPT")"
 : > "$RECEIPT"
-printf 'start parent_pid=%s epoch=%s\n' "$parent_pid" "$start_epoch" >> "$RECEIPT"
+printf 'start parent_pid=%s epoch=%s timeout_s=%s\n' "$parent_pid" "$start_epoch" "$TIMEOUT" >> "$RECEIPT"
 
 declare -a NAMES=()
 declare -a PIDS=()
@@ -86,6 +91,7 @@
 
 n_spawned=${#PIDS[@]}
 n_reaped=0
+timed_out=0
 for i in "${!PIDS[@]}"; do
   child=${PIDS[$i]}
   name=${NAMES[$i]}
@@ -93,6 +99,9 @@
   wait "$child"
   ec=$?
   set -e
+  if [[ "$ec" -eq 124 || "$ec" -eq 137 ]]; then
+    timed_out=1
+  fi
   n_reaped=$((n_reaped + 1))
   printf 'reap name=%s child_pid=%s exit_code=%s epoch=%s\n' \
     "$name" "$child" "$ec" "$(date +%s)" >> "$RECEIPT"
@@ -105,4 +114,7 @@
 fi
 printf 'end parent_pid=%s epoch=%s n_spawned=%s n_reaped=%s\n' \
   "$$" "$end_epoch" "$n_spawned" "$n_reaped" >> "$RECEIPT"
+if [[ "$n_spawned" -eq 0 || "$timed_out" -eq 1 ]]; then
+  exit 3
+fi
 exit 0

14 insertions(+), 2 deletions(-). The selftest keeps the TIMEOUT=420
default (timeout only required in dispatch mode); the start line records
timeout_s in both modes. Exit 3 is decided after the end line is written,
so receipts (a) and (c) still carry `end ...`.

## Counter run (verbatim)

$ python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round45/c1-count.py --tool /tmp/chousa-r45-ExecLauncherPatch/parent-lifetime.sh; echo "c1_exit=$?"
CASE a_empty_exits_3=ok
CASE b_ok_exits_0=ok
CASE c_timeout_exits_3=ok
CASE d_no_timeout_exits_2=ok
CASE e_start_timeout_s=ok
CASES_MATCH=5/5
C1=PASS
c1_exit=0

## Selftest run (verbatim)

$ bash /tmp/chousa-r45-ExecLauncherPatch/parent-lifetime.sh --selftest --receipt /tmp/chousa-r45-ExecLauncherPatch/st.receipt; echo "selftest_exit=$?"
selftest_exit=0

Receipt st.receipt:
start parent_pid=2312377 epoch=1792920922 timeout_s=420
spawn name=SelfA child_pid=2312389 epoch=1792920922
spawn name=SelfB child_pid=2312394 epoch=1792920922
reap name=SelfA child_pid=2312389 exit_code=0 epoch=1792920923
reap name=SelfB child_pid=2312394 exit_code=0 epoch=1792920923
end parent_pid=2312377 epoch=1792920923 n_spawned=2 n_reaped=2

## Verdict

C1 met: CASES_MATCH=5/5, C1=PASS, exit 0; selftest exit 0 with timeout_s=420
in the start line. Diff is the minimal one (14+/2-): a timeout-set flag,
start-line timeout_s, a timed_out flag, and the exit-3 decision. Existing
contract preserved: exit 0 on success, exit 1 on uncaptured pid, exit 2 on
usage.

## Risks / notes

- Exit 3 also fires on 137 (SIGKILL) reaps per the predicate, not only 124.
- Case (d) exits before any receipt file is created (usage precedes mkdir) —
  matches the counter, which ignores the receipt there.
- Nothing installed (no tool changes needed); no egress; no lane writes.
