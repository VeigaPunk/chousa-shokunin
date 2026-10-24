# CritC1Kill

## Verdict

**C1 killed** for the requested caller-environment provenance property.

The decisive measurement is command **C27** below: it runs the unmodified counter against the **original landed gate path**, with `LD_PRELOAD` interposing `SHA256_Update` only for `/usr/bin/sha256sum`. It prints `CLAIM_PIN_PROVENANCE_MATCH=4/7`, exits 1, and turns three tampered sources from `DRIFT/stale` into `CLEAN/supported`. Its receipt records:

```json
{
  "seed": 37410,
  "gate_sha256": "9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39",
  "matched": 4,
  "total": 7,
  "predicate_holds": false
}
```

The independent false-stale direction is command **C18**: intact sources become `DRIFT/stale`, the counter prints `3/7`, and its receipt also has the landed gate hash and `predicate_holds=false`:

```json
{
  "seed": 37403,
  "gate_sha256": "9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39",
  "matched": 3,
  "total": 7,
  "predicate_holds": false
}
```

This is not the named root/mount-namespace limit in `corpus/evidence/round37/claims.md:109-111`. The attack does not replace, bind, rename, or write `/usr/bin/sha256sum`; it needs no privilege and leaves both the absolute path and binary file identity unchanged. The caller's exported loader environment changes what the pinned process hashes. The narrower **PATH-only** subclaim still holds in the clean control, but that is not this ticket's requested ANY-caller-environment property.

Impacted axes: **operability** (both false acceptance and false stale), **provenance/identity** (the digest is not a function of the named source bytes under the pinned binary file alone), and **counter coverage/premature saturation** (the seven PATH cells can all pass while the same verdict is environmentally controlled). C2 was not measured.

## Counterexample

### Mechanism and line references

- `tools/research-gate.sh:432-438` chooses `/usr/bin/sha256sum` first.
- `tools/research-gate.sh:439-445`, especially line 442, executes `out=$("$bin" 2>/dev/null)` with the caller's environment intact. An absolute argv path does not scrub `LD_PRELOAD` from the exec environment.
- The landed `/usr/bin/sha256sum` imports OpenSSL `SHA256_Update` (command C14, dynamic symbol 55). The preload interposes that function only when `/proc/self/exe` is `/usr/bin/sha256sum` or `/bin/sha256sum`.
- In `strip` mode, the interposer removes the counter's exact suffix `tampered after the pin\n` before OpenSSL sees it. The on-disk source and claim pin are unchanged, but line 2019 now compares equal and the claim is accepted.
- In `flip` mode, it flips one input byte before OpenSSL sees it. Lines 2019-2023 then report a false revision mismatch on an intact source.
- The hex checks at lines 444 and 2018 cannot detect either attack: the resulting digest is still exactly 64 lowercase hex characters.

### Exact final preload source

Path: `/tmp/chousa-r37-crit-c1-kill.cKixEw/c1_preload.c`.

```c
#define _GNU_SOURCE
#include <dlfcn.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

typedef struct SHA256state_st SHA256_CTX;
static int (*real_sha256_update)(SHA256_CTX *c, const void *data, size_t len);

static int pinned_sha256sum(void) {
  char exe[PATH_MAX + 1];
  ssize_t n = readlink("/proc/self/exe", exe, PATH_MAX);
  if (n < 0) return 0;
  exe[n] = '\0';
  return strcmp(exe, "/usr/bin/sha256sum") == 0 ||
         strcmp(exe, "/bin/sha256sum") == 0;
}

int SHA256_Update(SHA256_CTX *c, const void *data, size_t len) {
  static const char suffix[] = "tampered after the pin\n";
  const char *mode;
  unsigned char *copy;
  int rc;
  if (!real_sha256_update)
    real_sha256_update = dlsym(RTLD_NEXT, "SHA256_Update");
  if (!real_sha256_update) return 0;
  if (!pinned_sha256sum()) return real_sha256_update(c, data, len);
  mode = getenv("C1_LD_MODE");
  if (mode && strcmp(mode, "strip") == 0) {
    size_t suffix_n = sizeof(suffix) - 1;
    if (len >= suffix_n &&
        memcmp((const char *)data + len - suffix_n, suffix, suffix_n) == 0)
      return real_sha256_update(c, data, len - suffix_n);
  } else if (mode && strcmp(mode, "flip") == 0 && len > 0) {
    copy = malloc(len);
    if (!copy) return 0;
    memcpy(copy, data, len);
    copy[0] ^= 1;
    rc = real_sha256_update(c, copy, len);
    free(copy);
    return rc;
  }
  return real_sha256_update(c, data, len);
}
```

Build with **C15**, sanity-check with **C16**, and reproduce the kill with **C27** (original landed gate) or **C17/C18** (byte-identical scratch copy). The scratch gate and original were both finally measured as `9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39`; the final probe `.so` is `ac3425b5aad6ede79b340c15d8d04515a935361cf91f22e7519acf5dfe1acb23` (C28).

## Required vector results

| Vector | Observed result | Blocking line / assessment |
|---|---|---|
| PATH `cut` shim | Clean control **C08** is 7/7, including `cut-shim-forge` and `cut-shim-broken`. | Covered by the existing seven cells. The pin path uses Bash parameter expansion at `tools/research-gate.sh:443`, not `cut`; comparison is at 2019. |
| `LD_PRELOAD` | **Kills in both directions**: C17/C27 = 4/7 forged matches; C18 = 3/7 false stale. | No blocking line. Line 442 inherits the loader environment; 444/2018 validate only digest syntax. |
| Hostile `TMPDIR` | C19 sets `TMPDIR` to a regular file and still gets 7/7. | The claim-pin operation at 2017 streams the source directly and creates no temp file. `mktemp` at 3925 belongs to canonical pin capture, not `verify-claims` claim hashing. |
| `CHOUSA_ROOT` redirection | The counter itself overwrites the caller value with its fixture root (`c1-count.py:107`), so C23 stays 7/7. Direct probes C25/C26 show the gate environment does move the verdict. | `tools/research-gate.sh:1838` deliberately applies `ROOT=${CHOUSA_ROOT:-$ROOT}` after CLI parsing. C25/C26 select different relative-source bytes; this is source routing, not a fixed-file digest-provenance counterexample, and is not needed for the kill. |
| Exported Bash function `sha256sum` in the gate process | C20 proves a fresh Bash imports the function, then gets 7/7. The counter removes `BASH_ENV`, not exported function variables (`c1-count.py:103-115`). | The selected command contains a slash (`/usr/bin/sha256sum`, lines 434-435) and is invoked as `"$bin"` at 442, so Bash does not resolve the function name. |
| Locale effects on hex comparison | C21 (`C.utf8`) and C22 (`en_US.utf8`) both get 7/7. | No movement observed in either installed non-C UTF-8 locale. Digest syntax is checked at 444/2018 and compared as strings at 2019; no locale normalization is applied. This is a bounded test of the available locales, not proof over every possible locale. |

### CHOUSA_ROOT fixture contents

The direct root probes used one claims file and two different sources. The claim pin is the digest of `root probe\n`:

```json
{"id":"ROOT1","source":"lib/src.md","span":"root probe","expect":"supported","sha256":"b9dae583101c4d7b36d6c42de32cc130293b21900f2de320c99c8f88ba1a082a"}
```

`good/lib/src.md` contains `root probe\n`; `evil/lib/src.md` contains `root probe\ntampered after the pin\n`. C25 sets `CHOUSA_ROOT=good` while passing `--root evil` and reads CLEAN; C26 reverses them and reads DRIFT/stale. That is the documented environment-first root choice at line 1838, not evidence that the pinned hash of one fixed file changed.

## Smallest safe correction

**[INFERENCE; proposed, not applied or benchmarked]** For this concrete digest-child hole, the smallest gate-local correction is at line 442: execute the already-pinned binary with a scrubbed loader environment rather than plain `"$bin"`, and add both the `strip` forged-match and `flip` false-stale cells to the counter. The same exposure exists in `sha256_hex_file` at line 450; leaving it unchanged would preserve a second authority for the other hash surface.

That child scrub alone must **not** be sold as process-wide independence from arbitrary `LD_PRELOAD`: the caller launches Bash with the variable already active, so arbitrary preload code can already affect the gate before line 442. The complete requested property therefore needs either (a) a trusted launcher that removes `LD_PRELOAD`, `LD_AUDIT`, `LD_LIBRARY_PATH`, and related loader controls **before Bash starts**, or (b) an explicit claim/limit narrowing C1 to PATH and naming loader-environment control as debt. Merely pinning the absolute binary is not a safe correction to the demonstrated property.

## Complete command log

All shell commands run by this seat are recorded below, including unsuccessful probe iterations. `O7`, `O4`, and `O3` are exact shared output blocks, reproduced once to avoid hiding the decisive rows among repeated identical output. Commands C09-C13 used superseded intermediate probe builds; the final reproducer is the source above plus C15-C18/C27. Read/write/search tool calls were not shell commands; their relevant contents are included above. No network was used and no tools were installed or updated.

### Shared observed outputs

**O7 — exact output, exit 0:**

```text
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
CLAIM_PIN_PROVENANCE_MATCH=7/7
__RC=0
```

**O4 — exact forged-match output, exit 1:**

```text
FAIL hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
FAIL sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
FAIL cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
CLAIM_PIN_PROVENANCE_MATCH=4/7
__RC=1
```

**O3 — exact false-stale output, exit 1:**

```text
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
FAIL hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
PASS sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
FAIL sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
FAIL sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
FAIL cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
CLAIM_PIN_PROVENANCE_MATCH=3/7
__RC=1
```

### C01 — confirm lane revision

```sh
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master
```

```text
b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65
```

Exit code: 0.

### C02 — read the freeze diff

```sh
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show b905217 -- tools/research-gate.sh
```

<details><summary>Exact observed output (276 lines)</summary>

```diff
commit b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65
Author: chousa-shokunin <chousa@shokunin.local>
Date:   Fri Oct 23 18:55:31 2026 -0300

    round-37 freeze: claim-pin provenance (C1) and pin-capture environment (C2) counters, gate fixes, selftest 262-267, frozen claims, base control

diff --git a/tools/research-gate.sh b/tools/research-gate.sh
index 2a1b231..efbd9f9 100755
--- a/tools/research-gate.sh
+++ b/tools/research-gate.sh
@@ -429,13 +429,24 @@ grep_pin_init() {
 # stamping a poison value. The claims path already fails closed on an
 # unmeasurable hash (sha_actual=unreadable); this gives the manifest the same
 # hex contract it validates on claims.
+sha256_pin_bin() { # -> absolute sha256sum path on stdout; rc 1 when none is executable
+  local bin=''
+  for bin in /usr/bin/sha256sum /bin/sha256sum; do
+    [[ -x $bin ]] && { printf '%s' "$bin"; return 0; }
+  done
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
 sha256_hex_file() { # FILE -> 64 lowercase hex on stdout; rc 1 otherwise
   local f=$1 bin='' out=''
-  for bin in /usr/bin/sha256sum /bin/sha256sum; do
-    [[ -x $bin ]] && break
-    bin=''
-  done
-  [[ -n $bin ]] || return 1
+  bin=$(sha256_pin_bin) || return 1
   out=$("$bin" -- "$f" 2>/dev/null) || return 1
   out=${out%%[ $'\t']*}
   [[ $out =~ ^[0-9a-f]{64}$ ]] || return 1
@@ -1998,9 +2009,12 @@ verify_claims() {
 
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
@@ -3919,7 +3933,7 @@ gate_canonical_capture() { # -> GATE_CAP | GATE_CAP_RC + GATE_CAP_NOTE
   fi
   ( cd "$fx" || exit 2
     env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_STRICT -u CHOUSA_ROOT \
-      -u CHOUSA_AGGREGATOR_ERE -u CHOUSA_GREP_PIN_ECHO \
+      -u CHOUSA_AGGREGATOR_ERE -u CHOUSA_GREP_PIN_ECHO -u BASH_ENV \
       bash "$SELF" verify-all record.md --claims claims.jsonl \
       --json manifest.jsonl --root . >capture.txt 2>&1 ) || rc=$?
   nv=$(grep -c '^RESEARCH_GATE: ' -- "$fx/capture.txt" 2>/dev/null || true)
@@ -7782,13 +7796,15 @@ EOF
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
+  # The same record reads supported on the normal PATH and must never read
+  # supported once the pinned tool is unmeasurable: fail closed to stale with
+  # actual=unreadable (research-gate.sh: fail closed: an unmeasurable source is
+  # not a match). The injection binds a failing stub over /usr/bin/sha256sum
+  # inside an unprivileged user+mount namespace (the r14 ns harness); without a
+  # userns the case is skipped BY NAME and the skip is counted, never passed.
   mkdir -p "$WORK/r2faultbin"
   printf '#!/bin/sh\nexit 127\n' >"$WORK/r2faultbin/sha256sum"
   chmod +x "$WORK/r2faultbin/sha256sum"
@@ -7802,22 +7818,29 @@ EOF
   [[ $r2_ctl_rc -eq 0 ]] || r2_ok=0
   [[ $r2_ctl_out == *'CLAIM id=HF1 expected=supported observed=supported'* ]] || r2_ok=0
   [[ $r2_ctl_out == *'VERDICT_BEARING_CLAIMS=1/1'* ]] || r2_ok=0
-  r2_fault_out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 \
-    CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
-    PATH="$WORK/r2faultbin:$PATH" \
-    bash "$SELF" verify-claims "$WORK/claims-r2-hash-fault.jsonl" 2>&1) || r2_fault_rc=$?
-  [[ $r2_fault_rc -eq 1 ]] || r2_ok=0
-  [[ $r2_fault_out == *'FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=warn surface=claims'* ]] || r2_ok=0
-  [[ $r2_fault_out == *'actual=unreadable'* ]] || r2_ok=0
-  [[ $r2_fault_out == *'VERDICT_BEARING_CLAIMS=0/1'* ]] || r2_ok=0
-  [[ $r2_fault_out != *'observed=supported'* ]] || r2_ok=0
-  if [[ $r2_ok -eq 1 ]]; then
-    printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" r2-hash-fault-shim "$r2_fault_rc"
+  ns_probe
+  if [[ $NS_STATE != yes ]]; then
+    SKIPPED=$((SKIPPED + 1))
+    printf 'skip-case %-2d %-26s reason=%s\n' "$cases" r2-hash-fault-pinned "$NS_WHY"
   else
-    printf 'FAIL-case %-28s control_rc=%d fault_rc=%d\n' \
-      r2-hash-fault-shim "$r2_ctl_rc" "$r2_fault_rc"
-    printf '%s\n' "$r2_ctl_out" "$r2_fault_out" | sed 's/^/    | /'
-    failures=$((failures + 1))
+    r2_fault_out=$(unshare --user --map-root-user --mount --propagation private bash -c '
+      mount --bind "$1/r2faultbin/sha256sum" /usr/bin/sha256sum || exit 97
+      exec env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE -u BASH_ENV \
+        CHOUSA_STRICT=0 CHOUSA_ROOT="$1" CHOUSA_NOW_EPOCH="$2" \
+        bash "$3" verify-claims "$1/claims-r2-hash-fault.jsonl"' _ "$WORK" "$NOW_EPOCH" "$SELF" 2>&1) || r2_fault_rc=$?
+    [[ $r2_fault_rc -eq 1 ]] || r2_ok=0
+    [[ $r2_fault_out == *'FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=warn surface=claims'* ]] || r2_ok=0
+    [[ $r2_fault_out == *'actual=unreadable'* ]] || r2_ok=0
+    [[ $r2_fault_out == *'VERDICT_BEARING_CLAIMS=0/1'* ]] || r2_ok=0
+    [[ $r2_fault_out != *'observed=supported'* ]] || r2_ok=0
+    if [[ $r2_ok -eq 1 ]]; then
+      printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" r2-hash-fault-pinned "$r2_fault_rc"
+    else
+      printf 'FAIL-case %-28s control_rc=%d fault_rc=%d\n' \
+        r2-hash-fault-pinned "$r2_ctl_rc" "$r2_fault_rc"
+      printf '%s\n' "$r2_ctl_out" "$r2_fault_out" | sed 's/^/    | /'
+      failures=$((failures + 1))
+    fi
   fi
   # Nested-key contract, string half: a key spelling inside a STRING value is not
   # a field. The object half ({"meta":{"line":"9"}} read as the record's own key
@@ -8140,6 +8163,143 @@ EOF
     failures=$((failures + 1))
   fi
 
+  # ---- round-37 claim-pin hashing (cases 262-264) ----
+  # verify-claims hashed a pinned source through `sha256sum < FILE | cut -d' '
+  # -f1`: both names resolved through PATH, so a shim printing the pinned
+  # digest made a stale source read current, and `cut` was a second lookup.
+  # The gate now hashes through the same pinned absolute binary the manifest
+  # uses, with no `cut`. Case 262 is the sha256sum shim, 263 the cut shim, 264
+  # the contract hold (a correct pin on the untouched stdin path).
+  mkdir -p "$WORK/lib" "$WORK/r37pinbin" "$WORK/r37cutbin"
+  printf 'pin r37 content\n' >"$WORK/lib/sha-r37.md"
+  r37_pin=$(sha256_hex_file "$WORK/lib/sha-r37.md") || r37_pin=''
+  printf 'pin r37 content\nTAMPERED after the pin\n' >>"$WORK/lib/sha-r37.md"
+  printf '{"id":"P1","source":"lib/sha-r37.md","span":"pin r37 content","expect":"supported","sha256":"%s"}\n' \
+    "$r37_pin" >"$WORK/claims-sha37-path.jsonl"
+  cat >"$WORK/r37pinbin/sha256sum" <<EOF
+#!/bin/sh
+cat >/dev/null 2>/dev/null
+printf '%s  -\\n' '$r37_pin'
+exit 0
+EOF
+  chmod +x "$WORK/r37pinbin/sha256sum"
+  r37_ok=1 r37_rc=0 r37_out=''
+  r37_out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 \
+    CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
+    PATH="$WORK/r37pinbin:$PATH" \
+    bash "$SELF" verify-claims "$WORK/claims-sha37-path.jsonl" 2>&1) || r37_rc=$?
+  cases=$((cases + 1))
+  [[ $r37_rc -eq 1 ]] || r37_ok=0
+  [[ $r37_out == *'RESEARCH_GATE: DRIFT'* ]] || r37_ok=0
+  [[ $r37_out == *'CLAIM_SOURCE_REVISION_MISMATCH'* ]] || r37_ok=0
+  [[ $r37_out == *'CLAIM id=P1 expected=supported observed=stale'* ]] || r37_ok=0
+  if [[ $r37_ok -eq 1 ]]; then
+    printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" claims-sha-path-shim "$r37_rc"
+  else
+    printf 'FAIL-case %-28s exit=%d\n' claims-sha-path-shim "$r37_rc"
+    printf '%s\n' "$r37_out" | sed 's/^/    | /'
+    failures=$((failures + 1))
+  fi
+  cat >"$WORK/r37cutbin/cut" <<EOF
+#!/bin/sh
+cat >/dev/null 2>/dev/null
+printf '%s\\n' '$r37_pin'
+exit 0
+EOF
+  chmod +x "$WORK/r37cutbin/cut"
+  r37_ok=1 r37_rc=0 r37_out=''
+  r37_out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 \
+    CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
+    PATH="$WORK/r37cutbin:$PATH" \
+    bash "$SELF" verify-claims "$WORK/claims-sha37-path.jsonl" 2>&1) || r37_rc=$?
+  cases=$((cases + 1))
+  [[ $r37_rc -eq 1 ]] || r37_ok=0
+  [[ $r37_out == *'RESEARCH_GATE: DRIFT'* ]] || r37_ok=0
+  [[ $r37_out == *'CLAIM_SOURCE_REVISION_MISMATCH'* ]] || r37_ok=0
+  if [[ $r37_ok -eq 1 ]]; then
+    printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" claims-sha-cut-shim "$r37_rc"
+  else
+    printf 'FAIL-case %-28s exit=%d\n' claims-sha-cut-shim "$r37_rc"
+    printf '%s\n' "$r37_out" | sed 's/^/    | /'
+    failures=$((failures + 1))
+  fi
+  printf 'pin r37 hold content\n' >"$WORK/lib/sha-r37-hold.md"
+  r37_hold=$(sha256_hex_file "$WORK/lib/sha-r37-hold.md") || r37_hold=''
+  printf '{"id":"H1","source":"lib/sha-r37-hold.md","span":"pin r37 hold content","expect":"supported","sha256":"%s"}\n' \
+    "$r37_hold" >"$WORK/claims-sha37-hold.jsonl"
+  r37_ok=1 r37_rc=0 r37_out=''
+  r37_out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 \
+    CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
+    bash "$SELF" verify-claims "$WORK/claims-sha37-hold.jsonl" 2>&1) || r37_rc=$?
+  cases=$((cases + 1))
+  [[ $r37_rc -eq 0 ]] || r37_ok=0
+  [[ $r37_out == *'RESEARCH_GATE: CLEAN'* ]] || r37_ok=0
+  [[ $r37_out == *'CLAIM id=H1 expected=supported observed=supported'* ]] || r37_ok=0
+  [[ $r37_out == *'verdict=match'* ]] || r37_ok=0
+  if [[ $r37_ok -eq 1 ]]; then
+    printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" claims-sha-stdin-hold "$r37_rc"
+  else
+    printf 'FAIL-case %-28s exit=%d\n' claims-sha-stdin-hold "$r37_rc"
+    printf '%s\n' "$r37_out" | sed 's/^/    | /'
+    failures=$((failures + 1))
+  fi
+
+  # ---- round-37 pin capture environment (cases 265-267) ----
+  # --pin's capture scrubbed the named CHOUSA_* variables but not BASH_ENV: the
+  # child bash re-sourced the caller's startup file, which re-exported a scrubbed
+  # variable (or moved CHOUSA_ROOT), so the pinned baseline embedded a GATE_GREP
+  # line and a plain --drift reported a phantom drift (-GATE_GREP / +GATE_GREP)
+  # on an unchanged gate. The capture now scrubs BASH_ENV too. Named limit: the
+  # gate process itself already sourced BASH_ENV before its body ran.
+  printf 'export CHOUSA_GREP_PIN_ECHO=1\n' >"$WORK/r37-echo.env"
+  rm -f "$WORK/r37-pin-env.txt" "$WORK/r37-pin-env2.txt" "$WORK/r37-pin-root.txt"
+  e37_ok=1 e37_rc=0 e37_drc=0 e37_out='' e37_dout=''
+  e37_out=$(BASH_ENV="$WORK/r37-echo.env" bash "$SELF" --pin "$WORK/r37-pin-env.txt" 2>&1) || e37_rc=$?
+  e37_dout=$(env -u BASH_ENV -u CHOUSA_GREP_PIN_ECHO bash "$SELF" --drift "$WORK/r37-pin-env.txt" 2>&1) || e37_drc=$?
+  cases=$((cases + 1))
+  [[ $e37_rc -eq 0 ]] || e37_ok=0
+  [[ $e37_drc -eq 0 ]] || e37_ok=0
+  [[ $e37_dout == 'GATE_DRIFT: none' ]] || e37_ok=0
+  grep -q '^GATE_GREP: ' -- "$WORK/r37-pin-env.txt" && e37_ok=0
+  if [[ $e37_ok -eq 1 ]]; then
+    printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" pin-bashenv-echo "$e37_drc"
+  else
+    printf 'FAIL-case %-28s pin_rc=%d drift_rc=%d\n' pin-bashenv-echo "$e37_rc" "$e37_drc"
+    printf '%s\n' "$e37_out" "$e37_dout" | sed 's/^/    | /'
+    failures=$((failures + 1))
+  fi
+  e37_ok=1 e37_drc=0 e37_out='' e37_dout=''
+  e37_out=$(env -u BASH_ENV bash "$SELF" --pin "$WORK/r37-pin-env2.txt" 2>&1)
+  e37_dout=$(BASH_ENV="$WORK/r37-echo.env" bash "$SELF" --drift "$WORK/r37-pin-env2.txt" 2>&1) || e37_drc=$?
+  cases=$((cases + 1))
+  [[ $e37_drc -eq 0 ]] || e37_ok=0
+  # the drift run's own receipt echo is allowed; the verdict is its last line
+  [[ $(printf '%s\n' "$e37_dout" | tail -n1) == 'GATE_DRIFT: none' ]] || e37_ok=0
+  if [[ $e37_ok -eq 1 ]]; then
+    printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" drift-bashenv-echo "$e37_drc"
+  else
+    printf 'FAIL-case %-28s drift_rc=%d\n' drift-bashenv-echo "$e37_drc"
+    printf '%s\n' "$e37_out" "$e37_dout" | sed 's/^/    | /'
+    failures=$((failures + 1))
+  fi
+  printf 'export CHOUSA_ROOT=%s\n' "$WORK/r37-foreign-root" >"$WORK/r37-root.env"
+  mkdir -p "$WORK/r37-foreign-root"
+  e37_ok=1 e37_rc=0 e37_drc=0 e37_out='' e37_dout=''
+  e37_out=$(BASH_ENV="$WORK/r37-root.env" bash "$SELF" --pin "$WORK/r37-pin-root.txt" 2>&1) || e37_rc=$?
+  e37_dout=$(env -u BASH_ENV bash "$SELF" --drift "$WORK/r37-pin-root.txt" 2>&1) || e37_drc=$?
+  cases=$((cases + 1))
+  [[ $e37_rc -eq 0 ]] || e37_ok=0
+  [[ -f $WORK/r37-pin-root.txt ]] || e37_ok=0
+  [[ $e37_drc -eq 0 ]] || e37_ok=0
+  [[ $e37_dout == 'GATE_DRIFT: none' ]] || e37_ok=0
+  if [[ $e37_ok -eq 1 ]]; then
+    printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" pin-bashenv-root "$e37_drc"
+  else
+    printf 'FAIL-case %-28s pin_rc=%d drift_rc=%d\n' pin-bashenv-root "$e37_rc" "$e37_drc"
+    printf '%s\n' "$e37_out" "$e37_dout" | sed 's/^/    | /'
+    failures=$((failures + 1))
+  fi
+
   if [[ $failures -eq 0 ]]; then
     printf 'RESEARCH_GATE_SELFTEST: PASS (%d cases%s)\n' "$cases" "${SKIPPED:+, $SKIPPED skipped}"
     exit 0
```

</details>

Exit code: 0.

### C03 — hash the landed gate

```sh
/usr/bin/sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
```

```text
9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
```

Exit code: 0.

### C04 — check compiler and locales

```sh
command -v gcc; command -v cc; /usr/bin/locale -a; printf '__RC=%d\n' "$?"
```

```text
/usr/bin/gcc
/usr/bin/cc
C
C.utf8
en_US.utf8
POSIX
__RC=0
```

Exit code: 0.

### C05 — create scratch

```sh
mktemp -d /tmp/chousa-r37-crit-c1-kill.XXXXXX; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

```text
/tmp/chousa-r37-crit-c1-kill.cKixEw
__RC=0
```

Exit code: 0.

### C06 — copy and hash the scratch gate

```sh
/usr/bin/cp -- /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /tmp/chousa-r37-crit-c1-kill.cKixEw/research-gate.sh && /usr/bin/sha256sum /tmp/chousa-r37-crit-c1-kill.cKixEw/research-gate.sh; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

```text
9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  /tmp/chousa-r37-crit-c1-kill.cKixEw/research-gate.sh
__RC=0
```

Exit code: 0.

### C07 — compile the first, superseded `read` interposer

```sh
/usr/bin/gcc -shared -fPIC -O2 -Wall -Wextra -o /tmp/chousa-r37-crit-c1-kill.cKixEw/c1_preload.so /tmp/chousa-r37-crit-c1-kill.cKixEw/c1_preload.c; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

```text
__RC=0
```

Exit code: 0. The shared object had an unresolved `__libc_read` reference, as the next two runs exposed.

### C08 — clean byte-identical gate control

```sh
C1_TMP=/tmp/chousa-r37-crit-c1-kill.cKixEw /usr/bin/python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /tmp/chousa-r37-crit-c1-kill.cKixEw/research-gate.sh --seed 37401 --receipt /tmp/chousa-r37-crit-c1-kill.cKixEw/c1-baseline-s37401.json; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

Observed output: **O7**. Exit code: 0.

### C09 — first preload attempt, forged-match mode

```sh
LD_PRELOAD=/tmp/chousa-r37-crit-c1-kill.cKixEw/c1_preload.so C1_LD_MODE=strip C1_TMP=/tmp/chousa-r37-crit-c1-kill.cKixEw /usr/bin/python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /tmp/chousa-r37-crit-c1-kill.cKixEw/research-gate.sh --seed 37402 --receipt /tmp/chousa-r37-crit-c1-kill.cKixEw/c1-ld-strip-s37402.json; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

```text
/usr/bin/python3: symbol lookup error: /tmp/chousa-r37-crit-c1-kill.cKixEw/c1_preload.so: undefined symbol: __libc_read
__RC=127
```

Exit code: 127.

### C10 — first preload attempt, false-stale mode

```sh
LD_PRELOAD=/tmp/chousa-r37-crit-c1-kill.cKixEw/c1_preload.so C1_LD_MODE=flip C1_TMP=/tmp/chousa-r37-crit-c1-kill.cKixEw /usr/bin/python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /tmp/chousa-r37-crit-c1-kill.cKixEw/research-gate.sh --seed 37403 --receipt /tmp/chousa-r37-crit-c1-kill.cKixEw/c1-ld-flip-s37403.json; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

```text
/usr/bin/python3: symbol lookup error: /tmp/chousa-r37-crit-c1-kill.cKixEw/c1_preload.so: undefined symbol: __libc_read
__RC=127
```

Exit code: 127.

### C11 — recompile the superseded `read` interposer through `dlsym`

```sh
/usr/bin/gcc -shared -fPIC -O2 -Wall -Wextra -o /tmp/chousa-r37-crit-c1-kill.cKixEw/c1_preload.so /tmp/chousa-r37-crit-c1-kill.cKixEw/c1_preload.c -ldl; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

```text
__RC=0
```

Exit code: 0.

### C12 — `read` interposer, forged-match mode (no effect)

The command was identical to C09. With that intermediate `.so`, observed output was **O7**. Exit code: 0. This was not treated as a block; C14 identified the actual imported hashing surface.

### C13 — `read` interposer, false-stale mode (no effect)

The command was identical to C10. With that intermediate `.so`, observed output was **O7**. Exit code: 0.

### C14 — inspect pinned binary imports

```sh
/usr/bin/readelf --dyn-syms --wide /usr/bin/sha256sum; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

Observed output: the 82-entry dynamic-symbol table reproduced verbatim under **C29** below. The security-relevant row was:

```text
    55: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND SHA256_Update@OPENSSL_3.0.0 (5)
__RC=0
```

Exit code: 0. C29 repeated the same inspection solely to preserve an exact full-table transcription after a report drafting error; no verdict depends on that drafting error or on any other symbol row.

### C15 — compile the final OpenSSL interposer

```sh
/usr/bin/gcc -shared -fPIC -O2 -Wall -Wextra -o /tmp/chousa-r37-crit-c1-kill.cKixEw/c1_preload.so /tmp/chousa-r37-crit-c1-kill.cKixEw/c1_preload.c -ldl; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

```text
__RC=0
```

Exit code: 0.

### C16 — direct pinned-binary sanity check

```sh
printf 'abc\n' | /usr/bin/sha256sum && printf 'abc\ntampered after the pin\n' | LD_PRELOAD=/tmp/chousa-r37-crit-c1-kill.cKixEw/c1_preload.so C1_LD_MODE=strip /usr/bin/sha256sum && printf 'abc\n' | LD_PRELOAD=/tmp/chousa-r37-crit-c1-kill.cKixEw/c1_preload.so C1_LD_MODE=flip /usr/bin/sha256sum; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

```text
edeaaff3f1774ad2888673770c6d64097e391bc362d7d6fb34982ddf0efd18cb  -
edeaaff3f1774ad2888673770c6d64097e391bc362d7d6fb34982ddf0efd18cb  -
0e00c7d01f144ef7b154c253c24351a9ce4bf42cfa3bdeb465ee02cb0de4c716  -
__RC=0
```

Exit code: 0. The first two inputs differ on disk/stream but receive the same digest under `strip`; the third differs from the clean digest under `flip`.

### C17 — scratch forged-match kill

```sh
LD_PRELOAD=/tmp/chousa-r37-crit-c1-kill.cKixEw/c1_preload.so C1_LD_MODE=strip C1_TMP=/tmp/chousa-r37-crit-c1-kill.cKixEw /usr/bin/python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /tmp/chousa-r37-crit-c1-kill.cKixEw/research-gate.sh --seed 37402 --receipt /tmp/chousa-r37-crit-c1-kill.cKixEw/c1-ld-strip-s37402.json; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

Observed output: **O4**. Exit code: 1. Receipt: seed 37402, landed gate hash, matched 4/7, `predicate_holds=false`.

### C18 — scratch false-stale kill

```sh
LD_PRELOAD=/tmp/chousa-r37-crit-c1-kill.cKixEw/c1_preload.so C1_LD_MODE=flip C1_TMP=/tmp/chousa-r37-crit-c1-kill.cKixEw /usr/bin/python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /tmp/chousa-r37-crit-c1-kill.cKixEw/research-gate.sh --seed 37403 --receipt /tmp/chousa-r37-crit-c1-kill.cKixEw/c1-ld-flip-s37403.json; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

Observed output: **O3**. Exit code: 1. Receipt: seed 37403, landed gate hash, matched 3/7, `predicate_holds=false`.

### C19 — hostile TMPDIR

The file `/tmp/chousa-r37-crit-c1-kill.cKixEw/tmpdir-not-a-directory` was created with contents `not a directory\n`.

```sh
TMPDIR=/tmp/chousa-r37-crit-c1-kill.cKixEw/tmpdir-not-a-directory C1_TMP=/tmp/chousa-r37-crit-c1-kill.cKixEw /usr/bin/python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /tmp/chousa-r37-crit-c1-kill.cKixEw/research-gate.sh --seed 37405 --receipt /tmp/chousa-r37-crit-c1-kill.cKixEw/c1-tmpdir-s37405.json; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

Observed output: **O7**. Exit code: 0.

### C20 — exported `sha256sum` function

```sh
sha256sum() { printf '%s  -\n' '0000000000000000000000000000000000000000000000000000000000000000'; }; export -f sha256sum; /usr/bin/bash -c 'if declare -F sha256sum >/dev/null; then printf "IMPORTED_SHA256SUM_FUNCTION=yes\n"; else printf "IMPORTED_SHA256SUM_FUNCTION=no\n"; fi'; C1_TMP=/tmp/chousa-r37-crit-c1-kill.cKixEw /usr/bin/python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /tmp/chousa-r37-crit-c1-kill.cKixEw/research-gate.sh --seed 37406 --receipt /tmp/chousa-r37-crit-c1-kill.cKixEw/c1-function-s37406.json; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

Observed output: first `IMPORTED_SHA256SUM_FUNCTION=yes`, then **O7**. Exit code: 0.

### C21 — C UTF-8 locale

```sh
LC_ALL=C.utf8 LANG=C.utf8 C1_TMP=/tmp/chousa-r37-crit-c1-kill.cKixEw /usr/bin/python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /tmp/chousa-r37-crit-c1-kill.cKixEw/research-gate.sh --seed 37407 --receipt /tmp/chousa-r37-crit-c1-kill.cKixEw/c1-locale-cutf8-s37407.json; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

Observed output: **O7**. Exit code: 0.

### C22 — English UTF-8 locale

```sh
LC_ALL=en_US.utf8 LANG=en_US.utf8 C1_TMP=/tmp/chousa-r37-crit-c1-kill.cKixEw /usr/bin/python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /tmp/chousa-r37-crit-c1-kill.cKixEw/research-gate.sh --seed 37408 --receipt /tmp/chousa-r37-crit-c1-kill.cKixEw/c1-locale-enus-s37408.json; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

Observed output: **O7**. Exit code: 0.

### C23 — caller CHOUSA_ROOT passed to the counter

```sh
CHOUSA_ROOT=/tmp/chousa-r37-crit-c1-kill.cKixEw/nonexistent-caller-root C1_TMP=/tmp/chousa-r37-crit-c1-kill.cKixEw /usr/bin/python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /tmp/chousa-r37-crit-c1-kill.cKixEw/research-gate.sh --seed 37409 --receipt /tmp/chousa-r37-crit-c1-kill.cKixEw/c1-root-counter-s37409.json; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

Observed output: **O7**. Exit code: 0. The harness replaces the caller root at `c1-count.py:107`.

### C24 — prepare root fixture and derive pin

```sh
/usr/bin/mkdir -p /tmp/chousa-r37-crit-c1-kill.cKixEw/root-probe/good/lib /tmp/chousa-r37-crit-c1-kill.cKixEw/root-probe/evil/lib && printf 'root probe\n' | /usr/bin/sha256sum; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

```text
b9dae583101c4d7b36d6c42de32cc130293b21900f2de320c99c8f88ba1a082a  -
__RC=0
```

Exit code: 0.

### C25 — CHOUSA_ROOT selects intact source despite contrary `--root`

```sh
/usr/bin/env -u BASH_ENV -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 CHOUSA_ROOT=/tmp/chousa-r37-crit-c1-kill.cKixEw/root-probe/good /usr/bin/bash /tmp/chousa-r37-crit-c1-kill.cKixEw/research-gate.sh verify-claims /tmp/chousa-r37-crit-c1-kill.cKixEw/root-probe/claims.jsonl --root /tmp/chousa-r37-crit-c1-kill.cKixEw/root-probe/evil; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

```text
research-gate v2 — ts=2026-10-24T02:42:35Z — mode=claims — claims=/tmp/chousa-r37-crit-c1-kill.cKixEw/root-probe/claims.jsonl
CLAIM id=ROOT1 expected=supported observed=supported source=lib/src.md at=line:1 verdict=match
VERDICT_BEARING_CLAIMS=1/1
RESEARCH_GATE: CLEAN (claims=1 supported=1 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)
__RC=0
```

Exit code: 0.

### C26 — CHOUSA_ROOT selects tampered source despite contrary `--root`

```sh
/usr/bin/env -u BASH_ENV -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 CHOUSA_ROOT=/tmp/chousa-r37-crit-c1-kill.cKixEw/root-probe/evil /usr/bin/bash /tmp/chousa-r37-crit-c1-kill.cKixEw/research-gate.sh verify-claims /tmp/chousa-r37-crit-c1-kill.cKixEw/root-probe/claims.jsonl --root /tmp/chousa-r37-crit-c1-kill.cKixEw/root-probe/good; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

```text
research-gate v2 — ts=2026-10-24T02:42:35Z — mode=claims — claims=/tmp/chousa-r37-crit-c1-kill.cKixEw/root-probe/claims.jsonl
CLAIM id=ROOT1 expected=supported observed=stale source=lib/src.md at=- verdict=mismatch
FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=warn surface=claims obs=id=ROOT1 pin=b9dae583101c actual=f1b7b8189e48
VERDICT_BEARING_CLAIMS=0/1
RESEARCH_GATE: DRIFT (claims=1 supported=0 contradicted=0 unsupported=0 mismatched=1 unproven=0 refused=0 invalid=0 findings=1 drift=1)
__RC=1
```

Exit code: 1.

### C27 — decisive kill against the original landed gate

```sh
LD_PRELOAD=/tmp/chousa-r37-crit-c1-kill.cKixEw/c1_preload.so C1_LD_MODE=strip C1_TMP=/tmp/chousa-r37-crit-c1-kill.cKixEw /usr/bin/python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 37410 --receipt /tmp/chousa-r37-crit-c1-kill.cKixEw/c1-landed-ld-strip-s37410.json; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

Observed output: **O4**. Exit code: 1. This is the original landed path, not a scratch mutant. Receipt fields are quoted at the top of this report.

### C28 — final identity check

```sh
/usr/bin/sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /tmp/chousa-r37-crit-c1-kill.cKixEw/research-gate.sh /tmp/chousa-r37-crit-c1-kill.cKixEw/c1_preload.so; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

```text
9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  /tmp/chousa-r37-crit-c1-kill.cKixEw/research-gate.sh
ac3425b5aad6ede79b340c15d8d04515a935361cf91f22e7519acf5dfe1acb23  /tmp/chousa-r37-crit-c1-kill.cKixEw/c1_preload.so
__RC=0
```

Exit code: 0.

### C29 — exact `readelf` transcription repeat

```sh
/usr/bin/readelf --dyn-syms --wide /usr/bin/sha256sum; rc=$?; printf '__RC=%d\n' "$rc"; exit "$rc"
```

<details><summary>Exact observed output</summary>

```text

Symbol table '.dynsym' contains 82 entries:
   Num:    Value          Size Type    Bind   Vis      Ndx Name
     0: 0000000000000000     0 NOTYPE  LOCAL  DEFAULT  UND 
     1: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __printf_chk@GLIBC_2.3.4 (2)
     2: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND setvbuf@GLIBC_2.2.5 (3)
     3: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __errno_location@GLIBC_2.2.5 (3)
     4: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND strcspn@GLIBC_2.2.5 (3)
     5: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __ctype_get_mb_cur_max@GLIBC_2.2.5 (3)
     6: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND strerror_r@GLIBC_2.2.5 (3)
     7: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __vfprintf_chk@GLIBC_2.3.4 (2)
     8: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND fwrite_unlocked@GLIBC_2.2.5 (3)
     9: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND strchr@GLIBC_2.2.5 (3)
    10: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND strspn@GLIBC_2.2.5 (3)
    11: 0000000000000000     0 FUNC    WEAK   DEFAULT  UND __cxa_finalize@GLIBC_2.2.5 (3)
    12: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND strlen@GLIBC_2.2.5 (3)
    13: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND memcmp@GLIBC_2.2.5 (3)
    14: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND strncmp@GLIBC_2.2.5 (3)
    15: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND memset@GLIBC_2.2.5 (3)
    16: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND abort@GLIBC_2.2.5 (3)
    17: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND fcntl@GLIBC_2.2.5 (3)
    18: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND mbrtoc32@GLIBC_2.16 (4)
    19: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND SHA256_Init@OPENSSL_3.0.0 (5)
    20: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND calloc@GLIBC_2.2.5 (3)
    21: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND dcgettext@GLIBC_2.2.5 (3)
    22: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __libc_start_main@GLIBC_2.34 (6)
    23: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND posix_fadvise@GLIBC_2.2.5 (3)
    24: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND memcpy@GLIBC_2.14 (7)
    25: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND mbsinit@GLIBC_2.2.5 (3)
    26: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __cxa_atexit@GLIBC_2.2.5 (3)
    27: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND setlocale@GLIBC_2.2.5 (3)
    28: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND nl_langinfo@GLIBC_2.2.5 (3)
    29: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND fclose@GLIBC_2.2.5 (3)
    30: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND bindtextdomain@GLIBC_2.2.5 (3)
    31: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND fileno@GLIBC_2.2.5 (3)
    32: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND fdopen@GLIBC_2.2.5 (3)
    33: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __ctype_b_loc@GLIBC_2.3 (8)
    34: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND strrchr@GLIBC_2.2.5 (3)
    35: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __stack_chk_fail@GLIBC_2.4 (9)
    36: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND SHA224_Final@OPENSSL_3.0.0 (5)
    37: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND dcngettext@GLIBC_2.2.5 (3)
    38: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND fopen@GLIBC_2.2.5 (3)
    39: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND free@GLIBC_2.2.5 (3)
    40: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND exit@GLIBC_2.2.5 (3)
    41: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND getenv@GLIBC_2.2.5 (3)
    42: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND SHA256@OPENSSL_3.0.0 (5)
    43: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND malloc@GLIBC_2.2.5 (3)
    44: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND iswprint@GLIBC_2.2.5 (3)
    45: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __overflow@GLIBC_2.2.5 (3)
    46: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __fpending@GLIBC_2.2.5 (3)
    47: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND strcmp@GLIBC_2.2.5 (3)
    48: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __fpurge@GLIBC_2.2.5 (3)
    49: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND textdomain@GLIBC_2.2.5 (3)
    50: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND _exit@GLIBC_2.2.5 (3)
    51: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND realloc@GLIBC_2.2.5 (3)
    52: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __fprintf_chk@GLIBC_2.3.4 (2)
    53: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND getopt_long@GLIBC_2.2.5 (3)
    54: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND fputc_unlocked@GLIBC_2.2.5 (3)
    55: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND SHA256_Update@OPENSSL_3.0.0 (5)
    56: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __memcpy_chk@GLIBC_2.3.4 (2)
    57: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND _ITM_deregisterTMCloneTable
    58: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND SHA224@OPENSSL_3.0.0 (5)
    59: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND SHA224_Init@OPENSSL_3.0.0 (5)
    60: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __fread_unlocked_chk@GLIBC_2.7 (10)
    61: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND __gmon_start__
    62: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND clearerr_unlocked@GLIBC_2.2.5 (3)
    63: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND _ITM_registerTMCloneTable
    64: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND fputs_unlocked@GLIBC_2.2.5 (3)
    65: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND close@GLIBC_2.2.5 (3)
    66: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND fflush_unlocked@GLIBC_2.2.5 (3)
    67: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __getdelim@GLIBC_2.2.5 (3)
    68: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND SHA256_Final@OPENSSL_3.0.0 (5)
    69: 000000000000d148     8 OBJECT  GLOBAL DEFAULT   25 error_print_progname
    70: 000000000000d108     4 OBJECT  GLOBAL DEFAULT   25 optind@GLIBC_2.2.5 (3)
    71: 000000000000d0e0     8 OBJECT  WEAK   DEFAULT   25 program_invocation_short_name@GLIBC_2.2.5 (3)
    72: 000000000000d0c0     8 OBJECT  WEAK   DEFAULT   25 program_invocation_name@GLIBC_2.2.5 (3)
    73: 000000000000d0d0     8 OBJECT  GLOBAL DEFAULT   25 stdin@GLIBC_2.2.5 (3)
    74: 000000000000d0c8     8 OBJECT  GLOBAL DEFAULT   25 stdout@GLIBC_2.2.5 (3)
    75: 000000000000d100     8 OBJECT  GLOBAL DEFAULT   25 stderr@GLIBC_2.2.5 (3)
    76: 000000000000237e   159 FUNC    GLOBAL DEFAULT   11 error_at_line
    77: 000000000000d144     4 OBJECT  GLOBAL DEFAULT   25 error_message_count
    78: 000000000000d0e0     8 OBJECT  GLOBAL DEFAULT   25 __progname@GLIBC_2.2.5 (3)
    79: 000000000000d140     4 OBJECT  GLOBAL DEFAULT   25 error_one_per_line
    80: 000000000000d0c0     8 OBJECT  GLOBAL DEFAULT   25 __progname_full@GLIBC_2.2.5 (3)
    81: 00000000000021ca   173 FUNC    GLOBAL DEFAULT   11 error
__RC=0
```

</details>

Exit code: 0.

## Tooling and scope

- Existing `/usr/bin/gcc` and `/usr/bin/python3` were used. **No installs or updates; no pacman transaction; no network.**
- Scratch artifacts and all receipts are under `/tmp/chousa-r37-crit-c1-kill.cKixEw`.
- No lane gate, counter, claim, receipt, Git index, Git/JJ state, or fleet file was modified. The only lane write made by this seat is this assigned report.
