# RevScenarioS3S4S5 — audit of c1-count.py S3 / S4 / S5

Date: 2026-10-23. Counter `corpus/evidence/round35/c1-count.py` sha256
`da207fd725658b84469ce1fe540a7b94fcb1027cef49da376a8d7ac19ac715e3`.
Landed gate sha256 `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`
(matches the wave's landed pin; verified by `sha256sum` and by the counter receipt
`landed-s3501.json` `gate_sha256`). Host scratch: `/tmp/hyaku/chousa-r35/w2/RevScenarioS3S4S5`.
Artifacts in `.ufo/waves/round-35/w2/RevScenarioS3S4S5/`; hashes in `artifact-sha256.txt`.

## Setup

Rebuilt the counter's fixture byte-for-byte (same `words`, same 3 rows K1/K2/K3,
same `lead … tail\n` sources) at `fixA/` and the counter's `nogrepbin` farm by
importing `build_nogrep_path`/`NOGREP_TOOLS` from the committed counter (no edits).
Farm result: 38 of 39 tools linked; `grep-free` absent from `/usr/bin` and `/bin`
on this host (expected — it is a sentinel name, not a real tool). No `grep`-named
entry in the farm (`ls nogrepbin | grep -i grep` → nothing).

## Q1 — Is the S3 symlink farm complete? What does the claims path actually exec?

Command (fixture root as cwd, `env -i` to keep only PATH+HOME — stricter than the
counter, which leaks other env):

```
strace -f -e trace=execve -o s3.strace env -i PATH=$PWD/../nogrepbin HOME=$HOME \
  bash /home/vgpnk/.../research-gate.sh verify-claims claims.jsonl --root .
```

Result: rc=1, stdout differs from the clean-PATH reference only in the `ts=`
banner field (`diff ref.out s3.out` → only line 1), stderr empty, **zero failed
execve**. Full exec census of the claims path on this fixture (s3.strace):

- resolved through the farm PATH: `tr`(8) `stat`(6) `sed`(5) `readlink`(4) `wc`(3)
  `od`(3) `cat`(3) `head`(2) `date`(2) `dirname`(1) `cut`(1) `bash`(1, the gate
  interpreter re-exec is `nogrepbin/bash`… actually the outer `bash` was exec'd by
  `env` via PATH → farm `bash`; the gate itself spawns no second bash here)
- resolved absolute, bypassing PATH: `/usr/bin/grep`(6 — the pin; proves S3's point),
  `/usr/bin/env`(1 — my wrapper's own exec of `env`, harness artifact not gate work)
- `env`/`bash` entries attributable to my wrapper: `env`(1), `bash`(1) at line 2 of
  the strace (the farm `bash` exec-ing the gate).

So the names the claims path really execs on this fixture:
`tr stat sed readlink wc od cat head date dirname cut` (+ interpreter `bash`,
harness `env`) and pinned `/usr/bin/grep`. **All** of those names are in
`NOGREP_TOOLS` (c1-count.py:145-148). Farm also carries `sh awk basename cp expr
false find flock id ls mkdir mktemp mv printf python3 rm sha256sum sh sleep sort
tail test touch true uniq xargs` which this path never execs — harmless
over-provisioning, plus coverage for claims shapes my fixture doesn't reach
(`sha256` pin → `sha256sum`, per-header `flock`).

**S3 verdict: a MISS on this host is about grep, not a missing tool.** Every
PATH-resolved exec under the farm succeeds; the only binary that leaves PATH is
the pinned `/usr/bin/grep` (6 execs, all absolute). Had a tool been missing, S3's
own check `same_as_ref(rc,out) and "not found" not in err` (c1-count.py:225)
catches it either via `bash: …: command not found` on stderr or via output drift —
but no such failure exists: `grep -c 'not found\|No such' s3.err` → 0.

Residual caveat [INFERENCE]: `build_nogrep_path` links only what exists on the
scoring host. On a hypothetical host missing e.g. `od` or `flock`, the farm would
be thinner and S3 could MISS for a non-grep reason. That is host-portability of
the harness, not a defect in the current measurement: on this canonical host the
farm covers 100% of observed execs.

## Q2 — Do S4/S5 refusals fire before any record read?

Yes — trace evidence, not structural inference.

S4 (`RESEARCH_GATE_GREP=bin/grep`, `bash -x` with `PS4='+L${LINENO} '`, s4.trace):

```
+L8039 grep_pin_init            <- pin call site, tools/research-gate.sh:8039
+L370  local cand= c=
+L371  [[ -n bin/grep ]]
+L374  case "$cand" in
+L376  grep_pin_refuse 'override is not an absolute path' bin/grep
+L354  printf 'research-gate: GREP_PROVENANCE refused: %s …'
+L355  exit 2
```

`verify_claims` is defined at gate line 1767; its body starts ~1786
(`scan_secrets "$claims"` at 1787 reads the claims file). **No traced line number
≥1767 appears anywhere in s4.trace** — every executed line belongs to argument
parsing or `grep_pin_init` (max traced LINENO in the file: L8039 callsite, then
function bodies 353-397). Same shape for S5 (`RESEARCH_GATE_GREP=<absent path>`,
s5.trace): refusal at L378 (`[[ -f $cand ]]` fails → "not a regular file"),
exit 2 at L355.

Open audit: `strace -f -e trace=openat,open` on the S4 invocation shows
**0 opens of `claims.jsonl`** (`grep -c 'claims.jsonl' s4.open.strace` → 0;
file kept at /tmp/hyaku/chousa-r35/w2/RevScenarioS3S4S5/s4.open.strace). The
record file is never opened; refusal precedes `scan_secrets`, the claims read
loop, and `verify_claims` dispatch (case arm at ~8065).

## Q3 — Does a gate that refuses exit-2 for ANY override still score S4/S5?

Yes for S4/S5 (and S6); no overall. Built `mutant-anyrefuse.sh` (one-line
insertion: unconditional `grep_pin_refuse "any override refused unconditionally"`
at the top of the override branch; sha256
`323f745ee48af7694f01b532e171d6781b6174b253332922bd6187b398e4e603`). Smoke:
`RESEARCH_GATE_GREP=/usr/bin/grep … bash mutant-anyrefuse.sh verify-claims …`
→ rc=2 with GREP_PROVENANCE. Scored with the real counter, seed 3501
(`C1_TMP=… python3 c1-count.py --gate ./mutant-anyrefuse.sh --seed 3501 --receipt
mutant-s3501.json`):

`GREP_PIN_MATCH=7/9` — S1 S2 S3 S4 S5 S6 S8 PASS; **S7 FAIL** (`echo_line=""`,
rc=2, no output) and **S9 FAIL** (same). So a blanket refuser wins every negative
scenario: S4/S5/S6 score refusal *shape* (`rc==2 and "GREP_PROVENANCE" in err`,
c1-count.py:231,238,244) with no check that a valid override is accepted. The
discriminators are S7 (override must actually run and echo `source=override`) and
S9 (override must beat the BASH_ENV shim). Not a P1 hole — the mutant still fails
the predicate — but S4+S5 alone cannot tell a correct verifier from a
refuse-everything gate.

## Anchor check on the landed gate

`C1_TMP=… python3 c1-count.py --gate tools/research-gate.sh --seed 3501
--receipt landed-s3501.json` → `GREP_PIN_MATCH=9/9`, exit 0, receipt
`gate_sha256` = landed pin. S6 detail: the non-GNU stub was invoked exactly once
(`stub_calls=1` — the `--version` probe), then refused "does not report GNU grep";
consistent with `grep_pin_verify` exec'ing only `--version` before any match work.

## Findings

1. **[Info] S3 farm complete on this host** — all 12 exec'd PATH tools are in
   `NOGREP_TOOLS`; 0 failed execs; only `/usr/bin/grep` bypasses PATH by pin.
2. **[Confirmed spec] S4/S5 refuse before any record read** — last traced source
   lines are 376/378 inside `grep_pin_init` (invoked at line 8039); no line
   ≥1767 executes; `claims.jsonl` never opened under strace.
3. **[Low / by-design] S4/S5 (and S6) accept any refuser** — refuse-any-override
   mutant scores those 3 points and reaches 7/9; S7/S9 are the only positive-
   acceptance checks. Worth knowing if a future round reuses S4/S5 semantics
   standalone.
4. **[Low / host-portability] Farm is host-dependent** — `build_nogrep_path`
   silently skips tools absent on the scoring host (only `grep-free` missing
   here, which is a decoy name anyway). An S3 MISS on a thinner host could be
   infrastructural; on this host it cannot be.

## Limits

- Fixture covers short-span direct-path claims only; sha256-pinned and
  long-span (chunk matcher ≥32765) claims may exec additional tools
  (`sha256sum` is farmed; the chunk matcher is still grep). [INFERENCE]
- `env -i` run is stricter than the counter's env (counter passes HOME, locale,
  etc. minus `CHOUSA_*`/`RESEARCH_GATE_*`); no env-sensitive behavior observed.
- Traces/receipts: `s4.trace`, `s5.trace`, `s4.open.strace` (in /tmp
  scratch), `s3.strace`, `ref.strace`, `landed-s3501.json`, `mutant-s3501.json`,
  `mutant-anyrefuse.sh` in the artifact dir; sha256s in `artifact-sha256.txt`.

Report: .ufo/waves/round-35/w2/RevScenarioS3S4S5.md
