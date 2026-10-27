# EvidenceScribe — round 60 evidence ledger (C1 / C2 frozen predicates)

Seat: leaf scribe, round 60 wave 1. **Scope:** record exact commands, outcomes, affected files,
provenance and known limits for the two frozen claims `corpus/evidence/round60-claims.md:5-11` (C1)
and `:13-19` (C2), against the frozen claims, prior committed evidence, and the current
counter/source only. No product edits, no verdict invented, no peer report treated as evidence
except where labelled corroboration.

Observation window: **2026-10-27 17:50–18:00 -03**. Every finding below binds to the digests in
§1. If a counter changes after this file was written, the finding must be re-measured, not quoted.

---

## 1. Pins — measured, not assumed

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ sha256sum corpus/evidence/round60-claims.md corpus/evidence/round60/c1-count.py \
            corpus/evidence/round60/c2-count.py tools/build-spans.py \
            corpus/evidence/round58/controls/build-spans-r55.py corpus/evidence/round58/c1-count.py \
            tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw \
            .ufo/waves/round-60/s101-open.txt
65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1  corpus/evidence/round60-claims.md
66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7  corpus/evidence/round60/c1-count.py
a19b06789f02a3aa9d4bf52a7a215f5614076706056ab9fcd300fdc131e83abe  corpus/evidence/round60/c2-count.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  corpus/evidence/round58/controls/build-spans-r55.py
65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f  corpus/evidence/round58/c1-count.py
2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  tools/capture-text.py
6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3  corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867  .ufo/waves/round-60/s101-open.txt
```

Four facts this pin block establishes:

1. **Candidate == control.** `diff -q tools/build-spans.py corpus/evidence/round58/controls/build-spans-r55.py`
   prints nothing; both hash `1ed2650a…`. The C1 counter's "candidate" leg and its "pinned r55"
   baseline leg therefore run the *same bytes* at base.
2. The frozen r58 counter bytes are unchanged since R59 measured them (`65da18bb…`, matching
   `.ufo/waves/round-59/w1/R59Executor09.md` §1).
3. The S101 form is re-producible from the **tracked** capture:
   `python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` → sha256
   `a8e3e7ad…`, byte-identical to `.ufo/waves/round-60/s101-open.txt` (`cmp -s` silent). Positive
   provenance finding for C2's raw side.
4. Tracked state (`git ls-files --error-unmatch` / `git status --porcelain`):
   `corpus/evidence/round60-claims.md`, `corpus/evidence/round60/{c1,c2}-count.py` and
   `.ufo/waves/round-60/s101-open.txt` are all **UNTRACKED** (`??`); `round58/c1-count.py`,
   `round58/controls/build-spans-r55.py`, `tools/build-spans.py`, the captures and
   `round-59/w1/R59Executor09.md` are tracked. Lane tip `b379919a873e7080a31ef92c7002f55f5374e2c6`;
   jj `@` = `f1dcc6e02184` (2026-10-27 17:05:42, empty).

Artifact order (mtime, `stat -c '%y %n'`): census 17:50:48 → claims 17:51:18 → c1-counter 17:51:38
→ c1-before 17:51:47 → s101-receipt 17:52:00 → c1-control-proof 17:52:08 → c2-counter 17:52:14 →
c2-before 17:52:19 → spec 17:55:15 → `w1.ready` 17:55:21. The freeze, both counters and both
before-receipts were written **before dispatch**; no seat had run when this evidence existed.

---

## 2. E1 — the pinned claim digest does not reproduce (critical)

The assignment (and every one of the 64 seat specs in `w1-dispatch.json`) pins
`09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`. The file at the named frozen
path hashes `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`.

```
$ sha256sum corpus/evidence/round60-claims.md
65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1  corpus/evidence/round60-claims.md
$ git hash-object corpus/evidence/round60-claims.md      # blob, not sha256
5ea0acf0881f950be640754a21408a71ebd95e5e
$ git log --oneline -5 -- corpus/evidence/round60-claims.md
(no output: never committed)
$ git status --porcelain -- corpus/evidence/round60-claims.md
?? corpus/evidence/round60-claims.md
$ jj --ignore-working-copy file show -r @ corpus/evidence/round60-claims.md
Error: No such path: corpus/evidence/round60-claims.md     # same at @-
```

Serialization sweep — 14 transforms, **0 reproduce the pin**:

```
$ python3 - <<'PY'   # (raw, NFC, NFD, line-rstrip, em dash→-, em dash→--, CRLF,
                     #  blank-lines-stripped, trailing-NL stripped, extra NL,
                     #  UTF-16LE, json.dumps, blob+path, bytes+path)
variants_tested=14 reproduced_pin=0 []
  raw / utf8-nfc / utf8-nfd / line-rstrip   65721569fc1336b1
  strip-final-nl                            cae804faeb016bf1
  crlf                                      dbb847b81e834ecf
  ...
pin                                       09d8053f5f09a26c
```

**What can and cannot be concluded.** The claims file's mtime (17:51:18) *precedes* the spec build
(17:55:15), so this is not a post-dispatch edit of the frozen path. The digest is nonetheless not a
digest of the bytes at that path by any of the 14 plausible serializations, and no pre-image exists
in git or in the jj snapshot history (`@` is empty and predates the file). Both surviving
hypotheses are integrity defects inside the freeze contract: either the digest was computed over a
pre-write in-memory serialization and never re-checked, or the file was rewritten between digesting
and freezing with the digest not recomputed. **Consequence for the closure:** the freeze cannot be
verified by the handed SHA, and the frozen claims have no committed copy from which the pin could be
re-derived. A freeze step that recomputes the digest and refuses dispatch on mismatch is the only
check that would have caught this.

Corroboration (concurrent, uncommitted seat reports — not evidence): `w1/BuildCounter.md:21,41,48`
and `w1/C1AlternateControl.md:5` report the same mismatch independently.

---

## 3. E2 — C1 counter: measured behaviour (`66e50763…`)

### 3.1 Base run reproduces the pre-dispatch receipt

```
$ mkdir -p /fast/scratch/hyaku/chousa-r60/EvidenceScribe/c1a
$ python3 -B corpus/evidence/round60/c1-count.py --builder tools/build-spans.py \
      --work /fast/scratch/hyaku/chousa-r60/EvidenceScribe/c1a --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
exit=1
```

Identical, leg for leg, to `.ufo/waves/round-60/c1-before.txt:3-7`. So the receipt is faithful and
the base verdict is honest: candidate == r55 bytes ⇒ legs (a) and (b) are mutually exclusive at base.

### 3.2 Leg-state classification (imported `run()`, no edits)

```
forged(injection mutant, prints =PASS): rc=0 state='candidate_safe'
noop(exit 0, no work):                  rc=0 state='candidate_safe'
forge0(prints =PASS, exit 0):           rc=0 state='candidate_safe'
pinned-r55(known unsafe):               rc=0 state='baseline_bad'
candidate tools/build-spans.py:         rc=0 state='baseline_bad'
```

Exhaustive truth table over the only two observable inputs (`c1-count.py:37-44`):

```
rc=0 intact=True  -> 'candidate_safe'
rc=0 intact=False -> 'baseline_bad'
rc=1 intact=True  -> ''
rc=1 intact=False -> ''
```

`forged_safe` is **unreachable for every input**, because its condition is byte-for-byte the
`baseline_bad` condition and is tested second. `forge_blocked = forge_state != "forged_safe"` is
therefore a constant `True`, and `INJECTION_REJECTED=1/1` is not a measurement.

### 3.3 Frozen requirement (c) is not implemented

The frozen predicate requires "the output-injection mutant prints `=PASS` but is scored as a
failure". The counter's own mutant (`--work`/`forged.py`, source in-file at `c1-count.py:60`) is
classified **`candidate_safe`** — the same state as a legitimate safe candidate. Scored honestly the
leg reads `0/1`; the counter prints `1/1`.

### 3.4 The target predicate is reachable by an inert child (kill rule)

```
$ cat noop.py            # trace §3.2 above; 2 lines, embedded for re-derivation
import sys
sys.exit(0)
$ python3 -B corpus/evidence/round60/c1-count.py --builder <scratch>/noop.py \
      --work <scratch>/c1-noop --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=1/1
C1=PASS
exit=0
```

```
$ cat forge0.py          # prints the target token, touches nothing
print('=PASS')
print('all seven hazards accepted')
$ python3 -B corpus/evidence/round60/c1-count.py --builder <scratch>/forge0.py \
      --work <scratch>/c1-forge0 --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=1/1
C1=PASS
exit=0
```

Cause: the "safe path" leg is `rc == 0 and foreign.is_file() and foreign.read_bytes() == before`
(`c1-count.py:37-43`). Nothing requires the builder to have produced a span, so an inert child and
a token-printing child are both `candidate_safe`. The frozen kill rule names exactly this case —
"**any child output injection passes target**" — and it is met, with `exit 0`.

Attribution, stated precisely: `forge0` passes because the safe-path leg checks no artifact, *not*
because the counter reads its output (it never does; `p.stdout`/`p.stderr` are captured and
discarded — see §3.6). The two are separate defects that combine into clause (c) failing.

### 3.5 Operability defects

```
$ python3 -B corpus/evidence/round60/c1-count.py --builder tools/build-spans.py --work <same-dir>
    File "/usr/lib/python3.14/pathlib/__init__.py", line 1011, in mkdir
FileExistsError: [Errno 17] File exists: '.../c1a/forge/cache'  # run():25, via base.mkdir(exist_ok=True) at :56
exit=1        # traceback, no leg line, no C1 line
```

A non-fresh `--work` crashes with exit 1 — the same exit code as an honest `C1=FAIL`. A driver that
reads only the exit code cannot distinguish "claim failed" from "counter crashed", and a crash
leaves no verdict for the receipt.

Relocation probe (scratch copy at `<scratch>/lanecopy/corpus/evidence/round60/c1-count.py`):

```
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=0/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
```

`ROOT = parents[3]` moves with the copy, so the r55 control silently goes missing; the counter has
no reason field distinguishing "control absent" from "control not discriminating". r58 pinned the
control (`R55_BUILDER_SHA = "1ed2650a…"`, `CAPTURE_TEXT_SHA = "2c0140bc…"`, `round58/c1-count.py:38-39`;
checked at `:350`, `:322`). The r60 counter contains **no** such constant (`grep -c R55_BUILDER_SHA
→ 0`): editing `controls/build-spans-r55.py` redefines what "the known unsafe control" means, and nothing
in the counter detects it. The relocation run above is the observed instance of that class (`0/1`
with no reason field); a subtracted/edited control was **not** tested here, so no claim is made
about that leg's value.

### 3.6 Declared-but-inert surface (C1)

| Clause in the frozen predicate / claim | Observed in `66e50763…` |
|---|---|
| `--seed 6001` | accepted, never read (`grep -c 'a.seed'` → 0); no sampling exists to seed |
| "captures child output only for diagnosis" | `capture_output=True` at `:37`, then `p.stdout`/`p.stderr` never referenced anywhere in the file |
| "per-leg structured states" | three `NAME=<0|1>/1` prints (`:71-73`); two are real, `INJECTION_REJECTED` is constant |
| "the frozen safe and hazard legs" | r58 had 11 named legs (EMPTY_OK, REBUILD_OK, FOREIGN, SYMLINK_OUT, SYMLINK_CACHE, FIFO_TXT, DEVZERO_TXT, FAT_RAW, MANY_QUOTES, ESCAPE_ENTRY, HELDOUT_OK); r60 has one hazard scenario + two controls |

The last row is a scoping observation for the judge, not a defect of the claim as frozen: the claim
explicitly says it "does not claim the builder itself meets all hazard legs". But the sentence "the
counter exits 0 only when the frozen safe and hazard legs meet their declared requirements" then has
no referent in the implementation.

---

## 4. E3 — C2 counter: measured behaviour (`a19b0678…`)

### 4.1 The declared base-fail does not hold — C2 passes with no round-60 entry

```
$ ls corpus/knowledge | grep -i 60            # no round-60 entry exists
(none)
$ git diff --stat b379919a873e… -- corpus/knowledge/citation-count-semantics-r37.md
(empty: the checked entry is byte-identical to the claim base)

$ mkdir -p /fast/scratch/hyaku/chousa-r60/EvidenceScribe/c2a
$ python3 -B corpus/evidence/round60/c2-count.py --root . --work <scratch>/c2a
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
exit=0
```

The frozen predicate says "**Base must fail because no round-60 entry exists**". Base does not
fail: the counter never looks for a round-60 entry. It scans
`corpus/knowledge/citation-count-semantics-r37.md` (`c2-count.py:8,15`) for two substrings that the
entry already carried before this round:

```
$ grep -c '#### Unknown' corpus/knowledge/citation-count-semantics-r37.md                       # 1
$ grep -c 'Whether the specification copy (S101) is the version in force' ...r37.md             # 1
```

(`#### Unknown`, r37 lines 74-77, already records the S101-version limit that C2 claims to add.)
A do-nothing control therefore reaches the C2 target, which §9 of the round contract forbids
("a target must be one a do-nothing control cannot reach"). The pre-dispatch receipt
`.ufo/waves/round-60/c2-before.txt` acknowledges the same fact in prose ("the existing source-bound
note predates this round") while the frozen predicate asserts the opposite; the frozen predicate is
the judging sentence, so this is a claim-integrity finding, not a wording quibble.

### 4.2 Root scoping: the form is not read under `--root`

```
$ R=<scratch>/root-copy; mkdir -p "$R/corpus/captures" "$R/corpus/knowledge"
$ cp corpus/captures/6dc68fd6….raw "$R/corpus/captures/"; cp corpus/knowledge/citation-count-semantics-r37.md "$R/corpus/knowledge/"
$ ls "$R/.ufo" ; ls: cannot access '.../root-copy/.ufo': No such file or directory
$ python3 -B corpus/evidence/round60/c2-count.py --root "$R" --work <scratch>/c2-root
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
exit=0
```

`FORM = ROOT/'.ufo/waves/round-60/s101-open.txt'` (`:7`) is resolved against the counter's own lane,
not `--root`, so a root-scoped lane copy cannot govern the form: `FORM_PIN` is checked against the
live (currently untracked) lane file while `RAW_PIN` and the entry are checked under `--root`. The
entry read *is* root-scoped — mutating the scratch copy flips the verdict:

```
$ # remove the S101-limit phrase from the scratch entry
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=0/1
C2=FAIL
exit=1
```

### 4.3 Predicate clauses with no implementation

| Frozen predicate clause | Observed |
|---|---|
| "verify the new entry's exact observation and no overreach against those source bytes" | no new-entry path exists; two fixed substrings of the **old** r37 entry are matched |
| "require the scorecard's declared disposition" | `grep -c 'SCORECARD\|scorecard'` → 0; `grep -n 'round-60' SCORECARD.md` → no output (no round-60 row yet) |
| `--work <fresh-absolute-dir>` | `a.work` is never referenced (`grep -n 'a.work'` → none); the argument is inert |
| metadata shape | `body.startswith('\n# ')` (`:17`) rejects the lane's own format: **80 of 82** `corpus/knowledge/*.md` entries start at byte 0 with `#`, and fail this test; only 2 pass |

The metadata clause is calibrated to the single file it checks (r37 begins with a blank line). Any
future entry written in the lane's normal shape would read `METADATA=0/1`.

---

## 5. E4 — Before-state citation chain (verified, not re-run)

The claims file's before-state rests on `W1 R59Executor09.md`. That path exists, is **tracked**
(`git ls-files --error-unmatch` succeeds), and supports the claim it carries: R59 §6 runs the
frozen r58 counter (`65da18bb…`, still the current bytes per §1) against a spoof builder and reports
every refusal leg as `fail(...)`, `SUMMARY … REFUSE=7/7`, `C1=PASS`, `EXIT=0`. The mechanism is
visible in the frozen source: `expect_refuse` concatenates candidate stderr+stdout and substring-
matches reason tokens (`round58/c1-count.py:150-160`), and the aggregate scans the assembled leg text
for uppercase `=PASS` (`:391`, `:399`). So the claim's "before" sentence — "frozen round-58 C1
permits forged target-token output from the builder to satisfy refusal checks" — is supported by
committed evidence and by the unchanged bytes. I did **not** re-run the spoof.

This matters for the C1 judgement: the round-60 counter does remove output from verdict derivation
(real progress, as far as it goes), but it replaces the forgeable aggregate with an unmeasured
injection leg and an artifact-free safe leg (§3.3–3.4), so clause (c) is *worse* than unimplemented —
it reports `1/1` for a mutant it scores as a pass.

---

## 6. Defect list (reported, nothing edited)

| # | severity | location | finding | evidence |
|---|---|---|---|---|
| D1 | critical | `round60/c1-count.py:37-44,60-63` | `forged_safe` unreachable ⇒ `INJECTION_REJECTED` is a constant `1/1`; frozen clause (c) unimplemented; the counter's own mutant is scored `candidate_safe` | §3.2, §3.3 truth table |
| D2 | critical | `round60/c1-count.py:37-43` | "safe path" leg checks only `rc==0` + foreign file intact; an inert builder and a token-printing builder both reach `C1=PASS`, `exit 0` — kill rule "any child output injection passes target" met | §3.4 (two runs, exit 0) |
| D3 | critical | `round60/c2-count.py:8,15` | C2 target already met at base: `C2=PASS`, `exit 0`, no round-60 entry; the counter checks two substrings of the pre-existing r37 entry; the frozen "base must fail because no round-60 entry exists" is false | §4.1 |
| D4 | high | `round60/c2-count.py:7,13` | `FORM` resolved from the lane, not `--root`; root-scoped verification bypassed (PASS on a `--root` with no `.ufo` tree) | §4.2 |
| D5 | critical | `corpus/evidence/round60-claims.md` + `w1-dispatch.json` | pinned digest `09d8053f…` does not reproduce from the frozen path (`65721569…`); no pre-image in git or jj; claims and both counters untracked at measurement | §2 |
| D6 | high | `round60/c1-count.py` (absent pin) | r58 pinned `R55_BUILDER_SHA`/`CAPTURE_TEXT_SHA`; r60 pins neither, so the "known unsafe control" can change silently and absence reads as `0/1` with no reason | §3.5, §1 |
| D7 | medium | `round60/c1-count.py:23-26` (`cache.mkdir()` at `:25`) | non-fresh `--work` raises uncaught `FileExistsError`; `exit 1` is shared by crash and honest `C1=FAIL`, so exit-code-only drivers misread a crash as a verdict | §3.5 |
| D8 | medium | `round60/c1-count.py:41-46,62-68` | no typed failure reasons: "control absent", "control did not discriminate", and "candidate refused wrongly" all collapse into `0/1`; the claim's "per-leg structured states" is only partially implemented | §3.5 relocation probe |
| D9 | medium | both counters | predicate clauses declared but inert: `--seed` (C1), `--work` (C2), "capture for diagnosis" (C1 discards output), "scorecard disposition" (C2 absent) | §3.6, §4.3 |
| D10 | low | `round60/c2-count.py:17` | `startswith('\n# ')` metadata test rejects 80/82 lane knowledge entries | §4.3 |
| D11 | low (scope note) | `round60/c1-count.py:71-73` | 3 legs vs r58's 11; "the frozen safe and hazard legs" has no implementation referent | §3.6 |

---

## 7. What the closure can re-derive, from committed bytes only

Once the wave dir and counters are committed, each finding re-derives with one command:

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
sha256sum corpus/evidence/round60-claims.md              # D5: compare to the dispatch pin
python3 -B corpus/evidence/round60/c1-count.py --builder tools/build-spans.py \
    --work "$(mktemp -d -p /fast/scratch/hyaku)" --seed 6001     # §3.1: C1=FAIL, exit 1
python3 -B corpus/evidence/round60/c1-count.py --builder <2-line no-op> \
    --work "$(mktemp -d -p /fast/scratch/hyaku)" --seed 6001     # D2: C1=PASS, exit 0
python3 -B corpus/evidence/round60/c2-count.py --root . --work "$(mktemp -d -p /fast/scratch/hyaku)"
                                                          # D3: C2=PASS, exit 0 at base
sha256sum corpus/evidence/round58/controls/build-spans-r55.py tools/build-spans.py   # §1: identical
```

**Discriminating tests the current bytes fail** (suggestions for the next freeze; no edits made):

- C1 (a): require a safe-path *artifact* — `spans.tsv` header, one row for the seeded S601, and span
  bytes equal to the cache text, as r58's `expect_ok` already did (`round58/c1-count.py:110-148`).
  Without it, "reaches the independently observed safe path" is satisfied by `sys.exit(0)`.
- C1 (c): make the injection mutant a *patched safe builder that also emits `=PASS`*, and require a
  leg state that separates it from the candidate; delete the unreachable `forged_safe` branch.
- C1: pin the control bytes (`R55_BUILDER_SHA`) and type the failure reasons; give crash its own
  exit code.
- C2: name an artifact absent at base (a round-60 `##` block with the located quote and a
  no-overreach sentence) or compare base vs head; read every input under `--root`; implement or
  delete the scorecard clause.

---

## 8. Limits / non-findings

- **Not run:** R59's spoof builder (cited from committed evidence, §5); the r58 counter; any
  external fetch; any install (none needed); any subagent.
- **Read-only git/jj only:** `rev-parse`, `log`, `status`, `ls-files`, `diff`, `hash-object`,
  `jj --ignore-working-copy log|file show`. No mutation, no commit, no push.
- **Peer reports** (`w1/*.md`, 43 present at 17:59) are concurrent and uncommitted; used only as
  labelled corroboration in §2, never as evidence for a finding.
- **Wave in flight:** no C1/C2 *after*-receipt existed at 18:00; only `c1-before.txt`,
  `c1-control-proof.txt`, `c2-before.txt`, `s101-receipt.txt`, `census-start.txt` (duplicate-URL
  warnings on S051/S053/S073/S074/S075, `exit=0`). This ledger records the **pre-work** state; it
  makes no claim about what the L1 lands after the wave.
- **Not my scope:** assimilation (`collisions` shows 52 lane/staged id collisions, S082–S133 —
  recorded as observed, not judged), the census, the lesson, and the round report.
- Findings bind to the digests in §1; if any counter changes, re-measure before quoting.

---
seat: EvidenceScribe
lane-root: /home/vgpnk/Projects/shokunin/chousa-shokunin
report: .ufo/waves/round-60/w1/EvidenceScribe.md
scratch: /fast/scratch/hyaku/chousa-r60/EvidenceScribe (created, used, removed)
lane writes: this file only
