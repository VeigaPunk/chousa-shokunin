# RevSeparability — round-37 residual falsify: the §Separability claim

Target: `corpus/evidence/round37/claims.md` §Separability — "either gate hunk alone
moves its own counter and not the other's". Attack, not re-assertion.

## 1. Verdict

**The separability claim holds as frozen.** Reverting both behavioural hunks moves
both counters down in the same state (C1 2/7, C2 3/7, both exit 1). Reverting only
the C2 hunk leaves C1 at 7/7 (exit 0); reverting only the C1 claim-pin call leaves
C2 at 7/7 (exit 0). The counters' fixtures prove the independence structurally:
C1's counter pops `BASH_ENV` before every gate call and never writes a startup file;
C2's counter never writes or passes a claims file at all, and the gate's canonical
pin fixture carries no `sha256` field, so the claim-pin branch is unreachable in
C2's measurement.

**No disagreement with wave-1** (`ExecMutGateC1.md`, `ExecMutGateC2.md`). My
C1-reverted mutant is byte-identical to the one whose sha256 wave-1 recorded
(`e4fc40a2364baeb534ca61e12c9cc1bfeebdfe1db64a0144e63f7ab8cabec10e`), and every
pass/fail cell matches. Two low-severity notes and the residual risk are in §8/§9;
neither contradicts the claim.

Lane tip read with `git -C … rev-parse master` (never `@{u}`):
`b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65`. Landed gate sha256:
`9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39` (matches the
freeze). No lane file, git/jj state, or Git index was touched; all mutants and
receipts live under `/tmp/chousa-r37-sep/`. No tool was installed or upgraded; no
network; the fleet root was not written.

## 2. Mutants

Four scratch copies of the landed gate, each mutated in exactly one region with the
edit tool (no `sed`):

| mutant | mutation | sha256 |
|---|---|---|
| `gate-both.sh` | :2017 claim-pin call reverted to the base form + `-u BASH_ENV` removed at :3936 | `715b7c5f83c02e68af2568e9b33ad999e95650b1718e1bc9cb13985ce0411a6e` |
| `gate-c1only.sh` | :2017 claim-pin call reverted only | `e4fc40a2364baeb534ca61e12c9cc1bfeebdfe1db64a0144e63f7ab8cabec10e` |
| `gate-c2only.sh` | `-u BASH_ENV` removed only | `06d9fc73e940c326354bcde8ce3e2cf15def5d71f14cb1a5477d641943931438` |
| `gate-fullc1.sh` | base-form claim-pin call **and** the C1 helper block (`sha256_pin_bin` + `sha256_hex_stream` + `sha256_hex_file` reverted to the base single `sha256_hex_file`) | `06f5c404d37f1ac13a5284d8ac73b6a238e1e4eb77a9359afbefccc6c968b762` |

Comments adjacent to the mutated lines were left intact; only code changed, so each
diff below is the complete behavioural delta. `sha256_hex_stream` has exactly two
occurrences in the gate (definition at :439, call at :2017), and each target string
occurred exactly once (uniqueness counts in §4.2), so no other line was touched.

## 3. Results matrix

| # | counter | gate | seed | count | exit | `gate_sha256` in receipt |
|---|---|---|---|---|---|---|
| 1 | C1 | landed | 37159 | **7/7** | 0 | `9fcac047…` |
| 2 | C2 | landed | 37160 | **7/7** | 0 | `9fcac047…` |
| 3 | C1 | only C2 hunk reverted | 37151 | **7/7** | 0 | `06d9fc73…` |
| 4 | C2 | only C1 call reverted | 37152 | **7/7** | 0 | `e4fc40a2…` |
| 5 | C1 | both reverted | 37153 | **2/7** | 1 | `715b7c5f…` |
| 6 | C2 | both reverted | 37154 | **3/7** | 1 | `715b7c5f…` |
| 7 | C1 | only C1 call reverted (negative control) | 37155 | **2/7** | 1 | `e4fc40a2…` |
| 8 | C2 | only C2 hunk reverted (negative control) | 37156 | **3/7** | 1 | `06d9fc73…` |
| 9 | C2 | full C1 revert (helpers + call) | 37157 | **7/7** | 0 | `06f5c404…` |
| 10 | C1 | full C1 revert | 37158 | **2/7** | 1 | `06f5c404…` |
| 11 | C1 | landed, caller `BASH_ENV` echo vector live | 37161 | **7/7** | 0 | `9fcac047…` |
| 12 | C2 | landed, caller `PATH` sha256sum+cut shims live | 37162 | **7/7** | 0 | `9fcac047…` |
| 13 | C1 | committed base control `base-gate-r37.sh` | 37163 | **2/7** | 1 | `a7d3922c…` |
| 14 | C2 | committed base control `base-gate-r37.sh` | 37164 | **3/7** | 1 | `a7d3922c…` |

Rows 5 and 6 are the new both-reverted cell: both counters fail in one state, and
the counts equal the committed base control's (rows 13/14), so the two-line mutant
reproduces the frozen base. Rows 9/10 extend the statement to the *entire* C1
change (helper hunk included): C1 still 2/7, C2 still 7/7.

Seeds are fresh: no committed or wave-1 receipt used 37151–37164 (wave-1 used
37001, 37021, 37101, 37102, 37137, 37138).

## 4. Verbatim run log

All `EXIT=` values are the shell's `$?` echoed immediately after the command. The
harness line "Ran in a temporary shell while the session shell is busy…" is not
command output and is omitted. Python heredoc blocks are shown with the code used.

### 4.1 Lane state, gate identity

```text
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master; sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh; ls -la /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/w1/ /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/residual/ 2>&1
b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65
9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
ls: cannot access '/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/residual/': No such file or directory
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/w1/:
total 68
drwxr-xr-x 1 vgpnk vgpnk   420 Oct 23 20:23 .
drwxr-xr-x 1 vgpnk vgpnk   124 Oct 23 20:12 ..
drwxr-xr-x 1 vgpnk vgpnk    76 Oct 23 20:22 ExecC1BaseRederive
-rw-r--r-- 1 vgpnk vgpnk  4325 Oct 23 20:23 ExecC1BaseRederive.md
-rw-r--r-- 1 vgpnk vgpnk  3785 Oct 23 20:22 ExecC1LandedRederive.md
drwxr-xr-x 1 vgpnk vgpnk    76 Oct 23 20:22 ExecC2BaseRederive
-rw-r--r-- 1 vgpnk vgpnk  2852 Oct 23 20:22 ExecC2BaseRederive.md
-rw-r--r-- 1 vgpnk vgpnk  2647 Oct 23 20:22 ExecC2LandedRederive.md
-rw-r--r-- 1 vgpnk vgpnk  4160 Oct 23 20:22 ExecMutC1Counter.md
-rw-r--r-- 1 vgpnk vgpnk  4518 Oct 23 20:23 ExecMutGateC1.md
-rw-r--r-- 1 vgpnk vgpnk  4456 Oct 23 20:22 ExecMutGateC2.md
-rw-r--r-- 1 vgpnk vgpnk  5089 Oct 23 20:22 ExecNoHarmPin.md
-rw------- 1 vgpnk vgpnk 13036 Oct 23 20:12 swarm-registry.json
EXIT=2
```

(The exit 2 is the `ls` of the not-yet-existing residual directory; it is created
only as the parent of this report.)

### 4.2 Base control vs landed: the complete delta, and mutant creation

```text
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin; ls .ufo/waves/round-37/controls/; sha256sum .ufo/waves/round-37/controls/base-gate-r37.sh; echo '--- diff stat base -> landed ---'; diff -u .ufo/waves/round-37/controls/base-gate-r37.sh tools/research-gate.sh | grep -c '^@@'; diff -u .ufo/waves/round-37/controls/base-gate-r37.sh tools/research-gate.sh | grep '^@@'
base-gate-r37.sh
a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8  .ufo/waves/round-37/controls/base-gate-r37.sh
--- diff stat base -> landed ---
6
@@ -429,13 +429,24 @@
@@ -1998,9 +2009,12 @@
@@ -3919,7 +3933,7 @@
@@ -7782,13 +7796,15 @@
@@ -7802,22 +7818,29 @@
@@ -8140,6 +8163,143 @@
EXIT=0
```

Six hunks in total, not two: hunk 1 is the C1 helper block, hunk 2 the claim-pin
call, hunk 3 the `-u BASH_ENV`; hunks 4–6 are selftest re-basing and the new
262–267 cases. Only hunks 2 and 3 are load-bearing for the counters (see §8 F1).

The helper and call hunks in full (base → landed):

```text
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin; diff -u .ufo/waves/round-37/controls/base-gate-r37.sh tools/research-gate.sh | sed -n '1,70p'
--- .ufo/waves/round-37/controls/base-gate-r37.sh	2026-10-23 19:53:05.029656205 -0300
+++ tools/research-gate.sh	2026-10-23 20:06:44.958039898 -0300
@@ -429,13 +429,24 @@
 # stamping a poison value. The claims path already fails closed on an
 # unmeasurable hash (sha_actual=unreadable); this gives the manifest the same
 # hex contract it validates on claims.
-sha256_hex_file() { # FILE -> 64 lowercase hex on stdout; rc 1 otherwise
-  local f=$1 bin='' out=''
+sha256_pin_bin() { # -> absolute sha256sum path on stdout; rc 1 when none is executable
+  local bin=''
   for bin in /usr/bin/sha256sum /bin/sha256sum; do
-    [[ -x $bin ]] && break
-    bin=''
+    [[ -x $bin ]] && { printf '%s' "$bin"; return 0; }
   done
-  [[ -n $bin ]] || return 1
+  return 1
+}
+sha256_hex_stream() { # stdin -> 64 lowercase hex on stdout; rc 1 otherwise
+  local bin='' out=''
+  bin=$(sha256_pin_bin) || return 1
+  out=$("$bin" 2>/dev/null) || return 1
+  out=${out%%[ $'\t']*}
+  [[ $out =~ ^[0-9a-f]{64}$ ]] || return 1
+  printf '%s' "$out"
+}
+sha256_hex_file() { # FILE -> 64 lowercase hex on stdout; rc 1 otherwise
+  local f=$1 bin='' out=''
+  bin=$(sha256_pin_bin) || return 1
   out=$("$bin" -- "$f" 2>/dev/null) || return 1
   out=${out%%[ $'\t']*}
   [[ $out =~ ^[0-9a-f]{64}$ ]] || return 1
@@ -1998,9 +2009,12 @@
 
     if [[ -n $sha_present ]]; then
       # hash via stdin: sha256sum escapes file names holding '\' or a newline
-      # and would prefix its output with '\' (r31)
-      sha_actual=$(sha256sum < "$path" 2>/dev/null | cut -d' ' -f1 || true)
+      # and would prefix its output with '\' (r31). The binary is the PINNED
+      # absolute one (r37): a PATH `sha256sum` shim that prints the pinned
+      # digest made a stale source read current, and `cut` was a second PATH
+      # lookup. One resolution serves the manifest and the claim pin.
       # fail closed: an unmeasurable source is not a match (r31)
+      sha_actual=$( { sha256_hex_stream < "$path"; } 2>/dev/null ) || sha_actual=unreadable
       [[ $sha_actual =~ ^[0-9a-f]{64}$ ]] || sha_actual=unreadable
       if [[ $sha_actual != "$sha_pin" ]]; then
         observed=stale
@@ -3919,7 +3933,7 @@
   fi
   ( cd "$fx" || exit 2
     env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_STRICT -u CHOUSA_ROOT \
-      -u CHOUSA_AGGREGATOR_ERE -u CHOUSA_GREP_PIN_ECHO \
+      -u CHOUSA_AGGREGATOR_ERE -u CHOUSA_GREP_PIN_ECHO -u BASH_ENV \
       bash "$SELF" verify-all record.md --claims claims.jsonl \
       --json manifest.jsonl --root . >capture.txt 2>&1 ) || rc=$?
   nv=$(grep -c '^RESEARCH_GATE: ' -- "$fx/capture.txt" 2>/dev/null || true)
@@ -7782,13 +7796,15 @@
     'CLAIM id=WP3 expected=supported observed=invalid source=claimsrc/sha-src.txt at=- verdict=invalid' \
     'VERDICT_BEARING_CLAIMS=0/3' \
     'claims=3 supported=0 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=3 findings=3 drift=3'
-  # Hash-read fault injection: sha256sum unavailable through a PATH shim. The
-  # same record reads supported on the normal PATH and must never read supported
-  # once the hash tool is unmeasurable: fail closed to stale with actual=unreadable
-  # (research-gate.sh: fail closed: an unmeasurable source is not a match). The
-  # source-unreadable arm reaches the same sha_actual=unreadable branch; it is a
-  # TOCTOU window (claim_source_path already required -r), so the shim is the
-  # deterministic injection.
+  # Hash-read fault injection, re-based on the pinned binary (r37): the claim
+  # pin now hashes through the pinned absolute sha256sum, so a PATH shim can no
+  # longer make the hash unmeasurable — that arm is covered by case 262/263.
EXIT=0
```

The base helper is already absolute, which is why hunk 1 is behaviour-preserving
(quoted in §6.3).

```text
$ mkdir -p /tmp/chousa-r37-sep && cd /home/vgpnk/Projects/shokunin/chousa-shokunin && for v in both c1only c2only fullc1; do cp -p tools/research-gate.sh /tmp/chousa-r37-sep/gate-$v.sh; done; ls -l /tmp/chousa-r37-sep/; grep -c 'sha256_hex_stream < "\$path"' tools/research-gate.sh; grep -c -- '-u CHOUSA_AGGREGATOR_ERE -u CHOUSA_GREP_PIN_ECHO -u BASH_ENV \\' tools/research-gate.sh; grep -n 'sha256_hex_stream' tools/research-gate.sh
total 1520
-rwxr-xr-x 1 vgpnk vgpnk 389021 Oct 23 20:06 gate-both.sh
-rwxr-xr-x 1 vgpnk vgpnk 389021 Oct 23 20:06 gate-c1only.sh
-rwxr-xr-x 1 vgpnk vgpnk 389021 Oct 23 20:06 gate-c2only.sh
-rwxr-xr-x 1 vgpnk vgpnk 389021 Oct 23 20:06 gate-fullc1.sh
1
1
439:sha256_hex_stream() { # stdin -> 64 lowercase hex on stdout; rc 1 otherwise
2017:      sha_actual=$( { sha256_hex_stream < "$path"; } 2>/dev/null ) || sha_actual=unreadable
EXIT=0
```

Uniqueness counts `1` and `1` prove each edit hit the only occurrence. After the
call is reverted, `sha256_hex_stream` has no caller (only its definition remains),
so the full-C1 mutant's helper revert is the base text restored wholesale.

```text
$ cd /tmp/chousa-r37-sep; sha256sum gate-*.sh; echo '=== both vs landed ==='; diff -U0 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh gate-both.sh; echo "rc=$?"; echo '=== c1only vs landed ==='; diff -U0 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh gate-c1only.sh; echo "rc=$?"; echo '=== c2only vs landed ==='; diff -U0 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh gate-c2only.sh; echo "rc=$?"; echo '=== fullc1 vs landed ==='; diff -U0 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh gate-fullc1.sh; echo "rc=$?"
715b7c5f83c02e68af2568e9b33ad999e95650b1718e1bc9cb13985ce0411a6e  gate-both.sh
e4fc40a2364baeb534ca61e12c9cc1bfeebdfe1db64a0144e63f7ab8cabec10e  gate-c1only.sh
06d9fc73e940c326354bcde8ce3e2cf15def5d71f14cb1a5477d641943931438  gate-c2only.sh
06f5c404d37f1ac13a5284d8ac73b6a238e1e4eb77a9359afbefccc6c968b762  gate-fullc1.sh
=== both vs landed ===
--- /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh	2026-10-23 20:06:44.958039898 -0300
+++ gate-both.sh	2026-10-23 23:36:49.381910924 -0300
@@ -2017 +2017 @@
-      sha_actual=$( { sha256_hex_stream < "$path"; } 2>/dev/null ) || sha_actual=unreadable
+      sha_actual=$(sha256sum < "$path" 2>/dev/null | cut -d' ' -f1 || true)
@@ -3936 +3936 @@
-      -u CHOUSA_AGGREGATOR_ERE -u CHOUSA_GREP_PIN_ECHO -u BASH_ENV \
+      -u CHOUSA_AGGREGATOR_ERE -u CHOUSA_GREP_PIN_ECHO \
rc=1
=== c1only vs landed ===
--- /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh	2026-10-23 20:06:44.958039898 -0300
+++ gate-c1only.sh	2026-10-23 23:36:46.382903509 -0300
@@ -2017 +2017 @@
-      sha_actual=$( { sha256_hex_stream < "$path"; } 2>/dev/null ) || sha_actual=unreadable
+      sha_actual=$(sha256sum < "$path" 2>/dev/null | cut -d' ' -f1 || true)
rc=1
=== c2only vs landed ===
--- /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh	2026-10-23 20:06:44.958039898 -0300
+++ gate-c2only.sh	2026-10-23 23:36:46.388903524 -0300
@@ -3936 +3936 @@
-      -u CHOUSA_AGGREGATOR_ERE -u CHOUSA_GREP_PIN_ECHO -u BASH_ENV \
+      -u CHOUSA_AGGREGATOR_ERE -u CHOUSA_GREP_PIN_ECHO \
rc=1
=== fullc1 vs landed ===
gate-fullc1.sh	2026-10-23 23:36:52.370918379 -0300 | 23 ++++++-----------------
1 file changed, 6 insertions(+), 17 deletions(-)

--- Changes ---

File: gate-fullc1.sh	2026-10-23 23:36:52.370918379 -0300
  @@ -432,2 +432,2 @@
  -sha256_pin_bin() { # -> absolute sha256sum path on stdout; rc 1 when none is executable
  -  local bin=''
  +sha256_hex_file() { # FILE -> 64 lowercase hex on stdout; rc 1 otherwise
  +  local f=$1 bin='' out=''
  @@ -435 +435,2 @@
  -    [[ -x $bin ]] && { printf '%s' "$bin"; return 0; }
  +    [[ -x $bin ]] && break
  +    bin=''
  @@ -437,13 +438 @@
  -  return 1
  -}
  -sha256_hex_stream() { # stdin -> 64 lowercase hex on stdout; rc 1 otherwise
  -  local bin='' out=''
  -  bin=$(sha256_pin_bin) || return 1
  -  out=$("$bin" 2>/dev/null) || return 1
  […8 changed lines elided…]
  @@ -2017 +2006 @@
  -      sha_actual=$( { sha256_hex_stream < "$path"; } 2>/dev/null ) || sha_actual=unreadable
  +      sha_actual=$(sha256sum < "$path" 2>/dev/null | cut -d' ' -f1 || true)
rc=1
```

(For `fullc1` the shell's diff renderer collapsed eight changed lines it judged
mechanical — the `[[ -n $bin ]] || return 1` restore and the `sha256_hex_file`
tail — and I did not re-expand them; the hash of the file and the 23-line churn
account for the complete region. The file still parses: the counter runs in rows
9/10 executed it successfully.)

### 4.3 Counter runs

Row 1 — C1 × landed:

```text
$ C1_TMP=/tmp/chousa-r37-sep python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 37159 --receipt /tmp/chousa-r37-sep/c1-landed-s37159.json; echo "EXIT=$?"
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
CLAIM_PIN_PROVENANCE_MATCH=7/7
EXIT=0
```

Row 2 — C2 × landed:

```text
$ C2_TMP=/tmp/chousa-r37-sep python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 37160 --receipt /tmp/chousa-r37-sep/c2-landed-s37160.json; echo "EXIT=$?"
PASS hold-plain       env=none           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS hold-benign      env=benign         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-pin     env=echo           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-drift   env=echo-on-drift  expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-fn-echo-pin  env=fn             expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-root-pin     env=root           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-strict-pin   env=strict         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PIN_CAPTURE_ENV_MATCH=7/7
EXIT=0
```

Row 3 — C1 × gate-c2only (only the C2 hunk reverted; C1 must not move):

```text
$ C1_TMP=/tmp/chousa-r37-sep python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /tmp/chousa-r37-sep/gate-c2only.sh --seed 37151 --receipt /tmp/chousa-r37-sep/c1-c2only-s37151.json; echo "EXIT=$?"
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
CLAIM_PIN_PROVENANCE_MATCH=7/7
EXIT=0
```

Row 4 — C2 × gate-c1only (only the C1 call reverted; C2 must not move):

```text
$ C2_TMP=/tmp/chousa-r37-sep python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c2-count.py --gate /tmp/chousa-r37-sep/gate-c1only.sh --seed 37152 --receipt /tmp/chousa-r37-sep/c2-c1only-s37152.json; echo "EXIT=$?"
PASS hold-plain       env=none           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS hold-benign      env=benign         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-pin     env=echo           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-drift   env=echo-on-drift  expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-fn-echo-pin  env=fn             expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-root-pin     env=root           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-strict-pin   env=strict         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PIN_CAPTURE_ENV_MATCH=7/7
EXIT=0
```

Row 5 — C1 × gate-both (both reverted):

```text
$ C1_TMP=/tmp/chousa-r37-sep python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /tmp/chousa-r37-sep/gate-both.sh --seed 37153 --receipt /tmp/chousa-r37-sep/c1-both-s37153.json; echo "EXIT=$?"
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
FAIL sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
FAIL cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
FAIL sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
FAIL sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
FAIL cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
CLAIM_PIN_PROVENANCE_MATCH=2/7
EXIT=1
```

Row 6 — C2 × gate-both:

```text
$ C2_TMP=/tmp/chousa-r37-sep python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c2-count.py --gate /tmp/chousa-r37-sep/gate-both.sh --seed 37154 --receipt /tmp/chousa-r37-sep/c2-both-s37154.json; echo "EXIT=$?"
PASS hold-plain       env=none           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS hold-benign      env=benign         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
FAIL env-echo-pin     env=echo           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=1 drift_rc=1 'GATE_DRIFT: -GATE_GREP'
FAIL env-echo-drift   env=echo-on-drift  expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=1 'GATE_DRIFT: +GATE_GREP'
FAIL env-fn-echo-pin  env=fn             expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=1 drift_rc=1 'GATE_DRIFT: -GATE_GREP'
FAIL env-root-pin     env=root           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=1 'GATE_DRIFT: -FINDING:CHAIN_SOURCE_MISSING -FINDING:CLAIM_SOURCE_MISSING -FINDING:POINTER_UNRESOLVED drift drift-sections drift_sections findings native refused root supported tallies tally verdict verified'
PASS env-strict-pin   env=strict         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PIN_CAPTURE_ENV_MATCH=3/7
EXIT=1
```

Row 7 — C1 × gate-c1only (negative control):

```text
$ C1_TMP=/tmp/chousa-r37-sep python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /tmp/chousa-r37-sep/gate-c1only.sh --seed 37155 --receipt /tmp/chousa-r37-sep/c1-c1only-s37155.json; echo "EXIT=$?"
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
FAIL sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
FAIL cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
FAIL sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
FAIL sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
FAIL cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
CLAIM_PIN_PROVENANCE_MATCH=2/7
EXIT=1
```

Row 8 — C2 × gate-c2only (negative control):

```text
$ C2_TMP=/tmp/chousa-r37-sep python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c2-count.py --gate /tmp/chousa-r37-sep/gate-c2only.sh --seed 37156 --receipt /tmp/chousa-r37-sep/c2-c2only-s37156.json; echo "EXIT=$?"
PASS hold-plain       env=none           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS hold-benign      env=benign         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
FAIL env-echo-pin     env=echo           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=1 drift_rc=1 'GATE_DRIFT: -GATE_GREP'
FAIL env-echo-drift   env=echo-on-drift  expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=1 'GATE_DRIFT: +GATE_GREP'
FAIL env-fn-echo-pin  env=fn             expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=1 drift_rc=1 'GATE_DRIFT: -GATE_GREP'
FAIL env-root-pin     env=root           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=1 'GATE_DRIFT: -FINDING:CHAIN_SOURCE_MISSING -FINDING:CLAIM_SOURCE_MISSING -FINDING:POINTER_UNRESOLVED drift drift-sections drift_sections findings native refused root supported tallies tally verdict verified'
PASS env-strict-pin   env=strict         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PIN_CAPTURE_ENV_MATCH=3/7
EXIT=1
```

Row 9 — C2 × gate-fullc1 (full C1 revert, C2 hunk intact):

```text
$ C2_TMP=/tmp/chousa-r37-sep python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c2-count.py --gate /tmp/chousa-r37-sep/gate-fullc1.sh --seed 37157 --receipt /tmp/chousa-r37-sep/c2-fullc1-s37157.json; echo "EXIT=$?"
PASS hold-plain       env=none           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS hold-benign      env=benign         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-pin     env=echo           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-drift   env=echo-on-drift  expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-fn-echo-pin  env=fn             expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-root-pin     env=root           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-strict-pin   env=strict         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PIN_CAPTURE_ENV_MATCH=7/7
EXIT=0
```

Row 10 — C1 × gate-fullc1:

```text
$ C1_TMP=/tmp/chousa-r37-sep python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /tmp/chousa-r37-sep/gate-fullc1.sh --seed 37158 --receipt /tmp/chousa-r37-sep/c1-fullc1-s37158.json; echo "EXIT=$?"
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
FAIL sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
FAIL cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
FAIL sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
FAIL sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
FAIL cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
CLAIM_PIN_PROVENANCE_MATCH=2/7
EXIT=1
```

Rows 11, 12 — each counter with the other axis's vector live in the caller. Shim
setup first:

```text
$ cd /tmp/chousa-r37-sep && mkdir -p shim && printf 'export CHOUSA_GREP_PIN_ECHO=1\n' > echo.env && printf '#!/bin/sh\ncat >/dev/null 2>/dev/null\nprintf "HOSTILE-CUT-OUTPUT  -\\n"\nexit 0\n' > shim/sha256sum && printf '#!/bin/sh\nprintf "HOSTILE\\n"\nexit 0\n' > shim/cut && chmod +x shim/sha256sum shim/cut && ls -l echo.env shim/ && cat echo.env
-rw-r--r-- 1 vgpnk vgpnk 30 Oct 23 23:38 echo.env

shim/:
total 8
-rwxr-xr-x 1 vgpnk vgpnk 36 Oct 23 23:38 cut
-rwxr-xr-x 1 vgpnk vgpnk 77 Oct 23 23:38 sha256sum
export CHOUSA_GREP_PIN_ECHO=1
EXIT=0
```

```text
$ BASH_ENV=/tmp/chousa-r37-sep/echo.env C1_TMP=/tmp/chousa-r37-sep python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 37161 --receipt /tmp/chousa-r37-sep/c1-landed-bashenv-s37161.json; echo "EXIT=$?"
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
CLAIM_PIN_PROVENANCE_MATCH=7/7
EXIT=0
```

```text
$ PATH=/tmp/chousa-r37-sep/shim:$PATH C2_TMP=/tmp/chousa-r37-sep python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 37162 --receipt /tmp/chousa-r37-sep/c2-landed-pathshim-s37162.json; echo "EXIT=$?"
PASS hold-plain       env=none           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS hold-benign      env=benign         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-pin     env=echo           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-drift   env=echo-on-drift  expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-fn-echo-pin  env=fn             expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-root-pin     env=root           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-strict-pin   env=strict         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PIN_CAPTURE_ENV_MATCH=7/7
EXIT=0
```

Rows 13, 14 — committed base control:

```text
$ C1_TMP=/tmp/chousa-r37-sep python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh --seed 37163 --receipt /tmp/chousa-r37-sep/c1-base-s37163.json; echo "EXIT=$?"
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
FAIL sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
FAIL cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
FAIL sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
FAIL sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
FAIL cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
CLAIM_PIN_PROVENANCE_MATCH=2/7
EXIT=1
```

```text
$ C2_TMP=/tmp/chousa-r37-sep python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh --seed 37164 --receipt /tmp/chousa-r37-sep/c2-base-s37164.json; echo "EXIT=$?"
PASS hold-plain       env=none           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS hold-benign      env=benign         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
FAIL env-echo-pin     env=echo           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=1 drift_rc=1 'GATE_DRIFT: -GATE_GREP'
FAIL env-echo-drift   env=echo-on-drift  expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=1 'GATE_DRIFT: +GATE_GREP'
FAIL env-fn-echo-pin  env=fn             expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=1 drift_rc=1 'GATE_DRIFT: -GATE_GREP'
FAIL env-root-pin     env=root           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=1 'GATE_DRIFT: -FINDING:CHAIN_SOURCE_MISSING -FINDING:CLAIM_SOURCE_MISSING -FINDING:POINTER_UNRESOLVED drift drift-sections drift_sections findings native refused root supported tallies tally verdict verified'
PASS env-strict-pin   env=strict         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PIN_CAPTURE_ENV_MATCH=3/7
EXIT=1
```

### 4.4 Receipts

```text
$ cd /tmp/chousa-r37-sep; python3 - <<'PY'
import json, glob, os
for f in sorted(glob.glob("*.json")):
    d = json.load(open(f))
    print("%-30s %-11s %d/%d holds=%-5s gate=%s" % (os.path.basename(f),
        d["counter"].rsplit("/",1)[-1], d["matched"], d["total"],
        str(d["predicate_holds"]), d["gate_sha256"]))
PY
c1-base-s37163.json            c1-count.py 2/7 holds=False gate=a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8
c1-both-s37153.json            c1-count.py 2/7 holds=False gate=715b7c5f83c02e68af2568e9b33ad999e95650b1718e1bc9cb13985ce0411a6e
c1-c1only-s37155.json          c1-count.py 2/7 holds=False gate=e4fc40a2364baeb534ca61e12c9cc1bfeebdfe1db64a0144e63f7ab8cabec10e
c1-c2only-s37151.json          c1-count.py 7/7 holds=True  gate=06d9fc73e940c326354bcde8ce3e2cf15def5d71f14cb1a5477d641943931438
c1-fullc1-s37158.json          c1-count.py 2/7 holds=False gate=06f5c404d37f1ac13a5284d8ac73b6a238e1e4eb77a9359afbefccc6c968b762
c1-landed-bashenv-s37161.json  c1-count.py 7/7 holds=True  gate=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
c1-landed-s37159.json          c1-count.py 7/7 holds=True  gate=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
c2-base-s37164.json            c2-count.py 3/7 holds=False gate=a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8
c2-both-s37154.json            c2-count.py 3/7 holds=False gate=715b7c5f83c02e68af2568e9b33ad999e95650b1718e1bc9cb13985ce0411a6e
c2-c1only-s37152.json          c2-count.py 7/7 holds=True  gate=e4fc40a2364baeb534ca61e12c9cc1bfeebdfe1db64a0144e63f7ab8cabec10e
c2-c2only-s37156.json          c2-count.py 3/7 holds=False gate=06d9fc73e940c326354bcde8ce3e2cf15def5d71f14cb1a5477d641943931438
c2-fullc1-s37157.json          c2-count.py 7/7 holds=True  gate=06f5c404d37f1ac13a5284d8ac73b6a238e1e4eb77a9359afbefccc6c968b762
c2-landed-pathshim-s37162.json c2-count.py 7/7 holds=True  gate=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
c2-landed-s37160.json          c2-count.py 7/7 holds=True  gate=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
EXIT=0
```

(An earlier summary over the then-existing ten receipts produced the same rows for
those ten files; it is recorded verbatim in Appendix A.4 and superseded by the
fourteen-row run above.)

## 5. Code proof — the counters' fixtures are disjoint by construction

### 5.1 C1's counter carries no BASH_ENV vector

`corpus/evidence/round37/c1-count.py:103-105` — the counter strips `BASH_ENV` (and
the other vectors) from the child environment before every gate call:

```python
    env = dict(os.environ)
    for var in ("CHOUSA_RECORD", "CHOUSA_CLAIMS", "CHOUSA_AGGREGATOR_ERE", "BASH_ENV"):
        env.pop(var, None)
```

`corpus/evidence/round37/c1-count.py:98-101` — its only fixture is a claims row
that *carries* the pin (C1's own axis); no startup file is ever written:

```python
    claims = os.path.join(sdir, "claims.jsonl")
    with open(claims, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"id": sid, "source": "lib/src.md", "span": body.strip(),
                             "expect": "supported", "sha256": pin}) + "\n")
```

`corpus/evidence/round37/c1-count.py:115-116` — the gate is driven only in
`verify-claims` mode:

```python
    proc = subprocess.run(["bash", gate, "verify-claims", claims, "--root", sdir],
                          capture_output=True, text=True, env=env, timeout=120)
```

Excerpt from the compound survey command recorded in Appendix A.6 (observed output
lines, in order):

```text
--- GATE_DRIFT in c1-count? ---
0
--- BASH_ENV in c2-count? ---
2:"""Round-37 C2 counter — the pinned baseline versus the caller's BASH_ENV.
9:child environment but not `BASH_ENV`: a non-interactive bash sources `$BASH_ENV`
65:         "CHOUSA_GREP_PIN_ECHO", "BASH_ENV")
81:        env["BASH_ENV"] = bashenv
```

`0` matches for `GATE_DRIFT|--pin|--drift|startup` in `c1-count.py`: the C1 counter
contains no drift vocabulary. The four `BASH_ENV` hits in `c2-count.py` are the
docstring (2), the docstring's explanation (9), the `SCRUB` tuple (65) and the
per-scenario export (81) — all in the counter, none in a claims fixture.

### 5.2 C2's counter carries no sha256 pin

`corpus/evidence/round37/c2-count.py:76-84` — the child env is built from `SCRUB`,
then `BASH_ENV` is *set* per scenario (the vector under test):

```python
def run_gate(gate, args, bashenv=None, cwd=None):
    env = dict(os.environ)
    for var in SCRUB:
        env.pop(var, None)
    if bashenv is not None:
        env["BASH_ENV"] = bashenv
    proc = subprocess.run(["bash", gate] + list(args), capture_output=True,
                          text=True, env=env, cwd=cwd, timeout=180)
    return proc.returncode, proc.stdout + proc.stderr
```

`corpus/evidence/round37/c2-count.py:64-65`:

```python
SCRUB = ("CHOUSA_RECORD", "CHOUSA_CLAIMS", "CHOUSA_AGGREGATOR_ERE",
         "CHOUSA_GREP_PIN_ECHO", "BASH_ENV")
```

`corpus/evidence/round37/c2-count.py:46-62` — all seven scenarios expect the same
observations (`pin_rc=0, pin_file=True, baseline_echo_lines=0, drift_rc=0,
drift_line="GATE_DRIFT: none"`); the only axis is the env-file mode:

```python
SCENARIOS = [
    # id, env-file mode, order, expect
    ("hold-plain", None, ("pin", "drift"),
     dict(pin_rc=0, pin_file=True, baseline_echo_lines=0, drift_rc=0, drift_line="GATE_DRIFT: none")),
    ("hold-benign", "benign", ("pin", "drift"),
     dict(pin_rc=0, pin_file=True, baseline_echo_lines=0, drift_rc=0, drift_line="GATE_DRIFT: none")),
    ("env-echo-pin", "echo", ("pin", "drift"),
     dict(pin_rc=0, pin_file=True, baseline_echo_lines=0, drift_rc=0, drift_line="GATE_DRIFT: none")),
    ("env-echo-drift", "echo-on-drift", ("pin", "drift"),
     dict(pin_rc=0, pin_file=True, baseline_echo_lines=0, drift_rc=0, drift_line="GATE_DRIFT: none")),
    ("env-fn-echo-pin", "fn", ("pin", "drift"),
     dict(pin_rc=0, pin_file=True, baseline_echo_lines=0, drift_rc=0, drift_line="GATE_DRIFT: none")),
    ("env-root-pin", "root", ("pin", "drift"),
     dict(pin_rc=0, pin_file=True, baseline_echo_lines=0, drift_rc=0, drift_line="GATE_DRIFT: none")),
    ("env-strict-pin", "strict", ("pin", "drift"),
     dict(pin_rc=0, pin_file=True, baseline_echo_lines=0, drift_rc=0, drift_line="GATE_DRIFT: none")),
]
```

Its fixture is `baseline.txt`, `startup.env`, `foreign-root`
(`c2-count.py:97,99,112`) — and the file contains no `claims` reference except the
docstring's citation of `claims.md`:

```text
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin; grep -n 'claims' corpus/evidence/round37/c2-count.py
4:Predicate (frozen in corpus/evidence/round37/claims.md before any candidate run):
EXIT=0
```

It invokes only `--pin`/`--drift` (`c2-count.py:119-120`):

```python
    pin_rc, pin_out = run_gate(gate, ["--pin", baseline], bashenv=pin_env, cwd=sdir)
    drift_rc, drift_out = run_gate(gate, ["--drift", baseline], bashenv=drift_env, cwd=sdir)
```

### 5.3 The gate's pin fixture has no `sha256` row, and the C1 branch is keyed on it

`tools/research-gate.sh:3876-3878` (the only claims row the canonical capture runs):

```bash
  cat >"$dir/claims.jsonl" <<'PINFIX' || return 1
{"id":"P1","source":"lib/primary.md","span":"line1 primary material","expect":"supported"}
```

`tools/research-gate.sh:1933-1935` — the claim-pin branch (hence line 2017) is
entered only when the row has a `sha256` key:

```bash
    if json_has_key "$line" sha256; then
      # a present non-string value is malformed, never "absent" (r31)
      sha_present=1; sha_pin='-'
```

### 5.4 The C2 hunk is unreachable from `verify-claims`

`gate_canonical_capture` (`tools/research-gate.sh:3922`) has exactly two callers,
both outside the verify path: `run_pin` (`:4063`, call at `:4065`) and `run_drift`
(`:4099`, call at `:4140`):

Excerpt from the same compound survey command (Appendix A.6):

```text
--- gate anchors ---
1933:    if json_has_key "$line" sha256; then
4063:run_pin() { # PATH
4099:run_drift() { # PATH
```

```text
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin; sed -n '4055,4070p' tools/research-gate.sh; echo '--- drift caller ---'; sed -n '4128,4142p' tools/research-gate.sh
  # The joined strings differed yet no line or field is named: a pure reorder
  # (pass 1 is order-independent). Say so instead of a false 'none'.
  if [[ ${#rep[@]} -eq 0 ]]; then rep+=("output-order"); fi
  joined=$(printf '%s\n' "${rep[@]}")
  sorted=$(LC_ALL=C sort -u <<<"$joined")
  GATE_REPORT=${sorted//$'\n'/ }
}

run_pin() { # PATH
  local path=$1 sha text
  gate_canonical_capture
  if [[ $GATE_CAP_RC -ne 0 || -z $GATE_CAP ]]; then
    printf 'research-gate: --pin canonical capture failed (%s): %s\n' \
      "${GATE_CAP_NOTE:-unknown}" "$path" >&2
    exit 2
  fi
--- drift caller ---
    exit 2
  }
  [[ -n $body ]] || {
    printf 'research-gate: --drift baseline malformed (empty canonical block): %s\n' "$path" >&2
    exit 2
  }
  body=${body%$'\n'}
  # The declared contract is compared too: a baseline pinned under a DIFFERENT
  # volatile list is drifting even when nothing in this run exercises the
  # changed mask (the recorded list is the contract — mori r10's d7710981
  # refinement).
  [[ $declared == "$GATE_DRIFT_VOLATILE_FIELDS" ]] || vol_token=volatile_fields
  gate_canonical_capture
  if [[ $GATE_CAP_RC -ne 0 || -z $GATE_CAP ]]; then
    printf 'research-gate: --drift canonical capture failed (%s): %s\n' \
EXIT=0
```

## 6. Comparison with wave-1

| cell | wave-1 | this seat | agree? |
|---|---|---|---|
| C1 × C1-reverted | `ExecMutGateC1`: 2/7, exit 1, seed 37101, mutant `e4fc40a2…` | 2/7, exit 1, seed 37155, mutant `e4fc40a2…` (byte-identical file) | yes |
| C2 × C1-reverted | `ExecMutGateC1`: 7/7, exit 0, seed 37102 | 7/7, exit 0, seed 37152 | yes |
| C1 × C2-reverted | `ExecMutGateC2`: 7/7, exit 0, seed 37137 | 7/7, exit 0, seed 37151 | yes |
| C2 × C2-reverted | `ExecMutGateC2`: 3/7, exit 1, seed 37138 | 3/7, exit 1, seed 37156 | yes |
| both reverted | not run by wave-1 | 2/7 + 3/7 in one state; equals the committed base control (2/7, 3/7) | new cell |

Per-cell failure sets also match exactly: C1 fails `sha-shim-forge`,
`cut-shim-forge`, `sha-shim-other`, `sha-shim-broken`, `cut-shim-broken`; C2 fails
`env-echo-pin` (echo=1, drift `-GATE_GREP`), `env-echo-drift` (`+GATE_GREP`),
`env-fn-echo-pin` (echo=1, `-GATE_GREP`), `env-root-pin` (token list).
**No disagreement found.**

## 7. Unasked cells I ran, and why

- Rows 11/12 put each counter's *other-axis vector* live in the caller: C1 with
  `BASH_ENV` exporting `CHOUSA_GREP_PIN_ECHO=1`, C2 with hostile `sha256sum`/`cut`
  first on `PATH`. Both stayed 7/7, so neither counter's number moves when the
  other axis's adversary is present (for C1 this is the counter's own
  `env.pop("BASH_ENV")`; for C2 it is the gate's pinned grep and absolute hash
  helpers).
- Rows 9/10 revert the entire C1 change, not just the call, to test whether the
  helper hunk is a hidden coupling. It is not: C2 stays 7/7.
- Rows 13/14 anchor the both-reverted mutant to the committed control; identical
  counts confirm the mutant's fidelity.

## 8. Findings

**No high- or medium-severity defect in the separability claim, the two gate hunks,
or the two counters.**

- **F1 (low — precision, not a contradiction).** The landed diff has six hunks
  (§4.2), not two. The C1 change is hunk 1 (helper block) **plus** hunk 2 (the
  call); only the call is load-bearing for behaviour, because the base
  `sha256_hex_file` already resolved `/usr/bin/sha256sum`/`/bin/sha256sum`
  absolutely. Rows 9/10 show the whole C1 change is still inert to C2 (7/7) and
  still fatal to C1 (2/7), so §Separability's word "hunk" is a harmless
  imprecision. Evidence: `gate-fullc1.sh` sha `06f5c404…`, rows 9/10.
- **F2 (low — evidence completeness in wave-1).** `ExecMutGateC2.md` records no
  `--receipt` paths and no mutant gate sha256, so its C2-reverted mutant cannot be
  byte-identified from the report (the only sha it cites is the *C1* mutant's,
  borrowed from the sibling report). This seat supplies the missing identity:
  `gate-c2only.sh` = `06d9fc73e940c326354bcde8ce3e2cf15def5d71f14cb1a5477d641943931438`,
  with receipts for both counters (rows 3/6/8).

## 9. Residual risk

- **Intra-gate comparison means C2 can never witness C1.** `--pin` and `--drift`
  both run the same binary, so a C1 regression that changed both captures equally
  would still read `GATE_DRIFT: none`. The 7/7 C2 cells on C1 mutants are not
  evidence of C1 health, and the 7/7 C1 cell on the C2 mutant is not evidence of C2
  health. That is exactly what "not the other's" asks for, but it bounds what each
  pass proves: separability of *measurement*, not mutual coverage.
- **C1's honesty bound is unchanged.** `sha256_pin_bin` selects
  `/usr/bin/sha256sum` or `/bin/sha256sum`; a caller who can replace that binary
  (root, mount namespace) still controls the digest. Unchanged from claims.md
  §Limits; nothing here widens it.
- **C2's counter depends on `bash` honouring `BASH_ENV`.** `c2-count.py` invokes
  `bash` by name with `BASH_ENV` set; under `sh`/POSIX mode the vector would vanish
  and the counter would score 7/7 for the wrong reason. The negative control (row
  8, 3/7) shows the vector is live today.
- **Seed independence is reasoned, not exhaustively proven.** Both counters
  parameterize only fixture words (`c1-count.py:53` `WORDS`; the C2 fixture is
  constant); the gate path is seed-independent. Two independent seed sets
  (wave-1's and this seat's, 14 runs) agree on every cell.

## 10. Verification gaps

- No byte diff of `verify-all` manifests across the helper revert: I ground hunk 1's
  behaviour-neutrality in code (base already used absolute paths) and in rows 9/10,
  not in a manifest diff. A direct diff is confounded by the embedded
  `gate_sha256` identity field.
- Out of scope by the frozen §Limits and untouched: `--posix`/`ENV`,
  `SHELLOPTS`/`BASHOPTS`, hostile `TMPDIR`, and the gate process's own pre-body
  `BASH_ENV` sourcing.
- The gate's `RESEARCH_GATE_SELFTEST` was not run (the assignment is the counter
  matrix); no formatter/linter/build was run either.
- `fullc1`'s diff rendering elided eight mechanical lines (§4.2 note); the file's
  sha and successful execution in rows 9/10 are the integrity evidence, not a
  line-by-line proof of the elided text.

## 11. Tooling and compliance

- No tool installed, upgraded, or removed; no `pacman` transaction; no network; no
  delegation.
- Scratch only under `/tmp/chousa-r37-sep/` (mutant gates, receipts, shims,
  `echo.env`). The lane repo was read-only: this report is the only file written;
  the only git command was the read-only `rev-parse master`; the Git index and jj
  state were not touched. The fleet root was not written.

## Appendix A — collateral commands (verbatim)

Every remaining shell command run during this review, with its observed output and
exit code. Where a pipeline truncated output (`| head -40`), the truncation is in
the command itself.

### A.1 Line counts

```text
$ wc -l /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c2-count.py
  8418 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
   183 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py
   185 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c2-count.py
  8786 total
EXIT=0
```

### A.2 Hash-helper survey in the landed gate

```text
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin; grep -n 'sha256_pin_bin()\|sha256_hex_stream\|sha_actual=\|SHA256_PIN\|sha256sum' tools/research-gate.sh | head -40
424:# they were produced by `sha256sum | cut` resolved through PATH and validated
430:# unmeasurable hash (sha_actual=unreadable); this gives the manifest the same
432:sha256_pin_bin() { # -> absolute sha256sum path on stdout; rc 1 when none is executable
434:  for bin in /usr/bin/sha256sum /bin/sha256sum; do
439:sha256_hex_stream() { # stdin -> 64 lowercase hex on stdout; rc 1 otherwise
1850:  local id src span expect marker observed verdict at bad l sha_pin='' sha_present='' sha_actual=''
2011:      # hash via stdin: sha256sum escapes file names holding '\' or a newline
2013:      # absolute one (r37): a PATH `sha256sum` shim that prints the pinned
2017:      sha_actual=$( { sha256_hex_stream < "$path"; } 2>/dev/null ) || sha_actual=unreadable
2018:      [[ $sha_actual =~ ^[0-9a-f]{64}$ ]] || sha_actual=unreadable
3722:      printf 'research-gate: sha256sum unavailable or returned a non-hex value; manifest not written\n' >&2
4073:    printf 'research-gate: sha256sum unavailable or returned a non-hex value; baseline not written\n' >&2
5342:      h1=$(sed -n 1p -- "$WORK/$json" | sha256sum | cut -d' ' -f1)
7414:  SHA_GOOD=$(sha256sum -- "$WORK/claimsrc/sha-src.txt" | cut -d' ' -f1)
7417:  SHA_TAMPERED=$(sha256sum -- "$WORK/claimsrc/sha-src-tampered.txt" | cut -d' ' -f1)
7419:  SHA_CRLF=$(sha256sum -- "$WORK/claimsrc/sha-src-crlf.txt" | cut -d' ' -f1)
7800:  # pin now hashes through the pinned absolute sha256sum, so a PATH shim can no
7805:  # not a match). The injection binds a failing stub over /usr/bin/sha256sum
7809:  printf '#!/bin/sh\nexit 127\n' >"$WORK/r2faultbin/sha256sum"
7810:  chmod +x "$WORK/r2faultbin/sha256sum"
7827:      mount --bind "$1/r2faultbin/sha256sum" /usr/bin/sha256sum || exit 97
8102:  # PATH `sha256sum` shim wrote HOSTILE-CUT-OUTPUT into both fields and the run
8106:  printf '#!/bin/sh\nprintf "HOSTILE-CUT-OUTPUT  -\\n"\nexit 0\n' >"$WORK/r36hashbin/sha256sum"
8107:  chmod +x "$WORK/r36hashbin/sha256sum"
8167:  # verify-claims hashed a pinned source through `sha256sum < FILE | cut -d' `
8171:  # uses, with no `cut`. Case 262 is the sha256sum shim, 263 the cut shim, 264
8179:  cat >"$WORK/r37pinbin/sha256sum" <<EOF
8185:  chmod +x "$WORK/r37pinbin/sha256sum"
EXIT=0
```

### A.3 Base gate's claim-pin region

```text
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin; grep -n 'sha_actual=\|cut -d' .ufo/waves/round-37/controls/base-gate-r37.sh | head -20; echo ---; sed -n '1995,2012p' .ufo/waves/round-37/controls/base-gate-r37.sh
430:# unmeasurable hash (sha_actual=unreadable); this gives the manifest the same
1839:  local id src span expect marker observed verdict at bad l sha_pin='' sha_present='' sha_actual=''
2002:      sha_actual=$(sha256sum < "$path" 2>/dev/null | cut -d' ' -f1 || true)
2004:      [[ $sha_actual =~ ^[0-9a-f]{64}$ ]] || sha_actual=unreadable
2075:              nearer=$(printf '%s\n' "$hay" | grep -Fn -m1 -e "$tok" | head -n1 | cut -d: -f1 || true)
2234:              nearer=$(printf '%s\n' "$hay" | grep -Fn -m1 -e "$tok" | head -n1 | cut -d: -f1 || true)
5328:      h1=$(sed -n 1p -- "$WORK/$json" | sha256sum | cut -d' ' -f1)
7400:  SHA_GOOD=$(sha256sum -- "$WORK/claimsrc/sha-src.txt" | cut -d' ' -f1)
7403:  SHA_TAMPERED=$(sha256sum -- "$WORK/claimsrc/sha-src-tampered.txt" | cut -d' ' -f1)
7405:  SHA_CRLF=$(sha256sum -- "$WORK/claimsrc/sha-src-crlf.txt" | cut -d' ' -f1)
7789:  # source-unreadable arm reaches the same sha_actual=unreadable branch; it is a
---
      continue
    fi
    path=$CLAIM_SRC_PATH

    if [[ -n $sha_present ]]; then
      # hash via stdin: sha256sum escapes file names holding '\' or a newline
      # and would prefix its output with '\' (r31)
      sha_actual=$(sha256sum < "$path" 2>/dev/null | cut -d' ' -f1 || true)
      # fail closed: an unmeasurable source is not a match (r31)
      [[ $sha_actual =~ ^[0-9a-f]{64}$ ]] || sha_actual=unreadable
      if [[ $sha_actual != "$sha_pin" ]]; then
        observed=stale
        at=-
        emit_finding CLAIM_SOURCE_REVISION_MISMATCH warn claims \
          "id=$id pin=${sha_pin:0:12} actual=${sha_actual:0:12}"
      fi
    fi
EXIT=0
```

### A.4 First receipt summary (ten receipts, superseded)

```text
$ cd /tmp/chousa-r37-sep; python3 - <<'PY'
import json, glob, os
for f in sorted(glob.glob("*.json")):
    d = json.load(open(f))
    print("%-28s %-9s matched=%d/%d holds=%s gate_sha256=%s" % (
        os.path.basename(f), d["counter"].rsplit("/",1)[-1], d["matched"], d["total"],
        d["predicate_holds"], d["gate_sha256"]))
PY
c1-both-s37153.json          c1-count.py matched=2/7 holds=False gate_sha256=715b7c5f83c02e68af2568e9b33ad999e95650b1718e1bc9cb13985ce0411a6e
c1-c1only-s37155.json        c1-count.py matched=2/7 holds=False gate_sha256=e4fc40a2364baeb534ca61e12c9cc1bfeebdfe1db64a0144e63f7ab8cabec10e
c1-c2only-s37151.json        c1-count.py matched=7/7 holds=True gate_sha256=06d9fc73e940c326354bcde8ce3e2cf15def5d71f14cb1a5477d641943931438
c1-fullc1-s37158.json        c1-count.py matched=2/7 holds=False gate_sha256=06f5c404d37f1ac13a5284d8ac73b6a238e1e4eb77a9359afbefccc6c968b762
c1-landed-s37159.json        c1-count.py matched=7/7 holds=True gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
c2-both-s37154.json          c2-count.py matched=3/7 holds=False gate_sha256=715b7c5f83c02e68af2568e9b33ad999e95650b1718e1bc9cb13985ce0411a6e
c2-c1only-s37152.json        c2-count.py matched=7/7 holds=True gate_sha256=e4fc40a2364baeb534ca61e12c9cc1bfeebdfe1db64a0144e63f7ab8cabec10e
c2-c2only-s37156.json        c2-count.py matched=3/7 holds=False gate_sha256=06d9fc73e940c326354bcde8ce3e2cf15def5d71f14cb1a5477d641943931438
c2-fullc1-s37157.json        c2-count.py matched=7/7 holds=True gate_sha256=06f5c404d37f1ac13a5284d8ac73b6a238e1e4eb77a9359afbefccc6c968b762
c2-landed-s37160.json        c2-count.py matched=7/7 holds=True gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
EXIT=0
```

### A.5 `sha_present` derivation in the gate

```text
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin; grep -n 'sha_present=' tools/research-gate.sh | head; echo ---; sed -n '1875,1905p' tools/research-gate.sh
1850:  local id src span expect marker observed verdict at bad l sha_pin='' sha_present='' sha_actual=''
1895:    bad=''; observed=''; at=''; sha_present=''; sha_pin=''
1935:      sha_present=1; sha_pin='-'
---
      CLAIM_LINES+=("CLAIM id=line$lineno expected=- observed=invalid source=- at=- verdict=invalid")
      continue
    fi
    # C1: a read field repeated among the top-level members makes the record
    # invalid (RFC 8259 §4: duplicate names make receiver behaviour
    # unpredictable), whether or not the values agree. The first duplicate in a
    # fixed order names the reason. Computed before the marker-default test so
    # a marker-default row with any repeated read field is refused, never
    # silently taken (r33 post-falsify: RerunC1a F1, RerunC1b G2).
    dup=''
    for dupk in id source span expect marker line sha256 marker_default; do
      if json_dup "$line" "$dupk"; then dup=$dupk; break; fi
    done
    # a marker-default row has a top-level "marker_default" string, no top-level
    # "id" string and no repeated read field
    if [[ -z $dup ]] && ! json_str "$line" id >/dev/null 2>&1 \
       && json_str "$line" marker_default >/dev/null 2>&1; then
      default_marker=$(json_unescape "$(jfield "$line" marker_default)")
      continue
    fi
    bad=''; observed=''; at=''; sha_present=''; sha_pin=''
    N_CLAIMS=$((N_CLAIMS + 1))
    if [[ -n $dup ]]; then
      N_INVALID=$((N_INVALID + 1))
      id=$(json_unescape "$(jfield "$line" id)")
      expect=$(json_unescape "$(jfield "$line" expect)")
      src=$(json_unescape "$(jfield "$line" source)")
      show_id=${id:-line$lineno}; show_exp=${expect:--}; show_src=${src:--}
      if [[ $dup == id ]]; then
        # a duplicated id prints that id only when every repeat is a string with
        # the same raw body as the first; otherwise the id is as unreadable as
EXIT=0
```

### A.6 Counter quote and anchor survey (source of §5.1/§5.4 excerpts)

```text
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin; echo '--- c1-count quotes ---'; sed -n '96,116p' corpus/evidence/round37/c1-count.py | cat -n | sed 's/^/   /'; echo '--- c2-count quotes ---'; awk 'NR>=76 && NR<=84 {printf "%d: %s\n", NR, $0}' corpus/evidence/round37/c2-count.py; awk 'NR>=117 && NR<=121 {printf "%d: %s\n", NR, $0}' corpus/evidence/round37/c2-count.py; echo '--- gate anchors ---'; grep -n '^run_pin()\|^run_drift\|json_has_key "$line" sha256' tools/research-gate.sh; echo '--- GATE_DRIFT in c1-count? ---'; grep -c 'GATE_DRIFT\|--pin\|--drift\|startup' corpus/evidence/round37/c1-count.py; echo '--- BASH_ENV in c2-count? ---'; grep -n 'BASH_ENV' corpus/evidence/round37/c2-count.py
--- c1-count quotes ---
        1	        with open(src, "a", encoding="utf-8") as fh:
        2	            fh.write("tampered after the pin\n")
        3	    claims = os.path.join(sdir, "claims.jsonl")
        4	    with open(claims, "w", encoding="utf-8") as fh:
        5	        fh.write(json.dumps({"id": sid, "source": "lib/src.md", "span": body.strip(),
        6	                             "expect": "supported", "sha256": pin}) + "\n")
        7	
        8	    env = dict(os.environ)
        9	    for var in ("CHOUSA_RECORD", "CHOUSA_CLAIMS", "CHOUSA_AGGREGATOR_ERE", "BASH_ENV"):
       10	        env.pop(var, None)
       11	    env["CHOUSA_STRICT"] = "0"
       12	    env["CHOUSA_ROOT"] = sdir
       13	    if shim:
       14	        name, mode = shim.split(":", 1)
       15	        bindir = os.path.join(sdir, "shim")
       16	        os.makedirs(bindir, exist_ok=True)
       17	        write_shim(bindir, name, mode, pin)
       18	        env["PATH"] = bindir + ":" + env.get("PATH", "/usr/bin:/bin")
       19	
       20	    proc = subprocess.run(["bash", gate, "verify-claims", claims, "--root", sdir],
       21	                          capture_output=True, text=True, env=env, timeout=120)
--- c2-count quotes ---
76: def run_gate(gate, args, bashenv=None, cwd=None):
77:     env = dict(os.environ)
78:     for var in SCRUB:
79:         env.pop(var, None)
80:     if bashenv is not None:
81:         env["BASH_ENV"] = bashenv
82:     proc = subprocess.run(["bash", gate] + list(args), capture_output=True,
83:                           text=True, env=env, cwd=cwd, timeout=180)
84:     return proc.returncode, proc.stdout + proc.stderr
117:     drift_env = envfile if mode == "echo-on-drift" else None
118: 
119:     pin_rc, pin_out = run_gate(gate, ["--pin", baseline], bashenv=pin_env, cwd=sdir)
120:     drift_rc, drift_out = run_gate(gate, ["--drift", baseline], bashenv=drift_env, cwd=sdir)
121: 
--- gate anchors ---
1933:    if json_has_key "$line" sha256; then
4063:run_pin() { # PATH
4099:run_drift() { # PATH
--- GATE_DRIFT in c1-count? ---
0
--- BASH_ENV in c2-count? ---
2:"""Round-37 C2 counter — the pinned baseline versus the caller's BASH_ENV.
9:child environment but not `BASH_ENV`: a non-interactive bash sources `$BASH_ENV`
65:         "CHOUSA_GREP_PIN_ECHO", "BASH_ENV")
81:        env["BASH_ENV"] = bashenv
EXIT=0
```

### A.7 Fixture and invocation survey

```text
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin; echo '--- c1-count.py ---'; grep -n 'for var in (\|proc = subprocess.run\|claims = os.path.join\|"sha256": pin\|env\["PATH"\]' corpus/evidence/round37/c1-count.py; echo '--- c2-count.py ---'; grep -n 'SCRUB = \|env\["BASH_ENV"\]\|run_gate(gate, \["--pin"\|run_gate(gate, \["--drift"\|claims' corpus/evidence/round37/c2-count.py; echo '--- gate fixture ---'; grep -n 'claims.jsonl\|"id":"P1"' tools/research-gate.sh | head -8
--- c1-count.py ---
98:    claims = os.path.join(sdir, "claims.jsonl")
101:                             "expect": "supported", "sha256": pin}) + "\n")
104:    for var in ("CHOUSA_RECORD", "CHOUSA_CLAIMS", "CHOUSA_AGGREGATOR_ERE", "BASH_ENV"):
113:        env["PATH"] = bindir + ":" + env.get("PATH", "/usr/bin:/bin")
115:    proc = subprocess.run(["bash", gate, "verify-claims", claims, "--root", sdir],
--- c2-count.py ---
4:Predicate (frozen in corpus/evidence/round37/claims.md before any candidate run):
64:SCRUB = ("CHOUSA_RECORD", "CHOUSA_CLAIMS", "CHOUSA_AGGREGATOR_ERE",
81:        env["BASH_ENV"] = bashenv
119:    pin_rc, pin_out = run_gate(gate, ["--pin", baseline], bashenv=pin_env, cwd=sdir)
120:    drift_rc, drift_out = run_gate(gate, ["--drift", baseline], bashenv=drift_env, cwd=sdir)
--- gate fixture ---
241:# The canonical invocation is `verify-all record.md --claims claims.jsonl
3876:  cat >"$dir/claims.jsonl" <<'PINFIX' || return 1
3877:{"id":"P1","source":"lib/primary.md","span":"line1 primary material","expect":"supported"}
3937:      bash "$SELF" verify-all record.md --claims claims.jsonl \
4086:  text+='# canonical: verify-all record.md --claims claims.jsonl --json manifest.jsonl --root . (cwd = a fresh temp fixture written by the gate)'$'\n'
4190:{"id":"P1","source":"lib/primary.md","span":"line1 primary material","expect":"supported"}
4871:  tsetup claims-missing-file 2 verify-claims "$WORK/no-such-claims.jsonl"
5409:  sed 's;| fetch | none |;| fetch | none |\n| claims | no-such-claims.jsonl |;' \
EXIT=0
```

### A.8 Scenario-table and fixture-path line numbers; report directory

```text
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin; grep -n '^ECHO_ENV\|^SCENARIOS\|^SCRUB\|foreign = os.path.join\|envfile = os.path.join\|baseline = "baseline.txt"' corpus/evidence/round37/c2-count.py; echo '--- c1 SCENARIOS ---'; grep -n '^SCENARIOS\|^WORDS' corpus/evidence/round37/c1-count.py
40:ECHO_ENV = "export CHOUSA_GREP_PIN_ECHO=1\n"
46:SCENARIOS = [
64:SCRUB = ("CHOUSA_RECORD", "CHOUSA_CLAIMS", "CHOUSA_AGGREGATOR_ERE",
97:    baseline = "baseline.txt"
99:    foreign = os.path.join(sdir, "foreign-root")
112:        envfile = os.path.join(sdir, "startup.env")
--- c1 SCENARIOS ---
42:SCENARIOS = [
53:WORDS = ("alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel",
EXIT=0
```

```text
$ mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/residual && ls -ld /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/residual; echo "EXIT=$?"
drwxr-xr-x 1 vgpnk vgpnk 0 Oct 23 23:39 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/residual
EXIT=0
```

