# RevC1Controls — R46-C1 control receipts re-run (wave 2)

seat L1Chousa46.RevC1Controls (reviewer, leaf). Item: re-run `controls/c1-controls.txt`
and `controls/c1-before.txt` verbatim, paste actual vs recorded, report drift incl. the
counter revision. No fetch. Only this file written; scratch removed at close.

## 0. The record moved under the re-run (times -03:00, sampled)

| instant | HEAD | c1-count.py | controls / before |
|---|---|---|---|
| 07:33 | d09fc8e | 819287e2 (no canary) | 4-line rows, 2 forges (f23a202f / f484f3a1) |
| 07:38:05 | d09fc8e | b389e96b (broken canary) | — |
| 07:38:16 | d09fc8e | 8473abf6 (canary + `spans_dir`) | — |
| 07:38:27 | d09fc8e | 8473abf6 | regenerated: 5-line rows, 3 forges (b1dac74c / 60209699) |
| 07:39 / 07:42:00 | 3807537 → e50b388 | 8473abf6 (committed) | same; tool 819f83eb → 3018b1d2 → 0c8f7ba9 |
| 07:42:26 | e50b388 | **275d2dc6 — SyntaxError line 268** | — |
| 07:42:52 | e50b388 | **8fa8e5cc** (settled; 320 lines) | receipts not regenerated |

Both receipt generations were re-run. Result: **every recorded row reproduces exactly at
the bytes it was written against.** The drift is in the record's binding, not the arithmetic.

## 1. Forge gap

Receipts name forges by label only (`always-exit-0`, `citation-presence-only`, now
`always-pass.py`/`cite-only.py`/`name-oracle.py`). No such file exists in the lane
(`find .ufo/waves/round-46 corpus/evidence/round46 -name 'always-pass.py' -o -name
'cite-only.py' -o -name 'name-oracle.py'` → empty; labels appear only in w1
`ExecCounterRun.md` / `ScoutInheritedTree.md`). Round-35 shipped `build-forge.py` in-lane
for exactly this. I rebuilt all three from the declared semantics (`exit(0)`; every
`#### Inference` bullet must carry `` (`S###`) ``, fences skipped; `exit(0)` iff the
basename starts `positive-`). Every row matched — but an alternative `cite-only` (one that
also checks `#### Observation`) is indistinguishable from the receipt.

## 2. Generation 1 — d09fc8e / 3807537 (counter 819287e2)

```
$ python3 c1-count.py(819287e2) --root <archive 6e2630a6 + counters + fixtures>
recorded: TOOL=absent / 0/3 / 0/3 / C1=FAIL / exit=1
actual:   TOOL=absent / 0/3 / 0/3 / C1=FAIL / exit=1                    MATCH
$ ... --tool <always-exit-0>      recorded 3/3 0/3 FAIL exit1    actual identical  MATCH
$ ... --tool <citation-presence>  recorded 3/3 1/3 FAIL exit1    actual identical  MATCH
```
`cite-only` kills exactly one junk live: junk-uncited exit 1, junk-ungrounded exit 0,
junk-borrowed exit 0 — consistent with the recorded `1/3`.

## 3. Generation 2 — e50b388 (counter 8473abf6; also 8fa8e5cc, identical rows)

```
$ ... --tool always-pass.py   TOOL=present 3/3 0/3 CANARY=fail C1=FAIL exit=1   MATCH (rec :6-8)
$ ... --tool cite-only.py     TOOL=present 3/3 1/3 CANARY=pass C1=FAIL exit=1   MATCH (rec :11-16)
$ ... --tool name-oracle.py   TOOL=present 3/3 3/3 CANARY=fail C1=FAIL exit=1   MATCH (rec :19-24)
$ ... --root <before tree>    TOOL=absent 0/3 0/3 CANARY=pass C1=FAIL exit=1    MATCH (rec :5-10)
$ ... (default)               TOOL=present 3/3 3/3 CANARY=pass C1=PASS exit=0
                              ^ five lines; measure-after.txt records four
```

## 4. Drift and defects

**D1 (HIGH) — stale after-receipt, committed beside the counter it no longer describes.**
At e50b388: counter 8473abf6, controls b1dac74c, before 60209699, but `measure-after.txt`
= 6baf6635 still declares `c1 819287e2075c3f5b` and omits the `CANARY=` line the committed
counter now prints. Numbers unchanged (3/3, 3/3, PASS, exit 0); the receipt cannot be
reproduced verbatim from the tree it ships in.

**D2 (HIGH) — CANARY is an undeclared pass-rule change.** `claims.md` is byte-identical to
the freeze (sha256 `60098df…`): its predicate requires only the six `positive-*`/`junk-*`
exit codes, its control block still names two controls, and no `CANARY` token appears.
The committed counter now makes `C1=PASS` additionally require `CANARY=pass`. Under the
claims' own admission rule ("A rule changed after any seat has scored is not this claim's
rule") wave-2 verdicts must be scored on 819287e2's rule; the leg must be declared and the
claim re-frozen, or the verdict pinned.

**D3 (HIGH, transient) — the counter was red twice mid-flight.** b389e96b (07:38:05) made
the *real* tool print `CANARY=fail C1=FAIL exit=1`: the canary copied only the two `.md`
files and passed `--spans TMP/spans.tsv` (missing), so any correct tool reports
`INF_TOKEN_NOT_IN_SPAN` on the renamed positive. Deterministic repro: same files with
`spans.tsv`/`counts.json`/`spans/` present → `GROUND: PASS` exit 0. Fixed in 8473abf6 by
`spans_dir=fixture_dir`. Then 275d2dc6 (07:42:26) raised `SyntaxError: unterminated string
literal (detected at line 268)` — the counter did not run at all. Any seat sampling either
window reports a false regression (or a crash on a frozen instrument).

**D4 (HIGH, structural) — 8fa8e5cc is a botched append.** 320 lines, `def main(` ×4,
`if __name__` ×4: three verbatim copies of `digest`/`run`/`main` sit *after* the first
`if __name__ … sys.exit(main())`, so they are dead. Behaviour equals 8473abf6 plus two new
`PINNED` span digests (verified: S901-1 `7c2aa321…`, S902-1 `c2184ca7…` match disk), so no
numeric effect — but four copies make any future whole-file/replace-all edit ambiguous, and
the "final counter revision" label is stale again.

**D5 (MED) — forges unshipped** (§1): the three control rows are not byte-reproducible from
the repo, and the canary's own falsifier (`name-oracle.py`) has no in-lane artifact.

**D6 (LOW) — the before row is revision-invariant and cannot evidence calibration.**
`TOOL=absent` is a compile-time branch (`present = tool.is_file()`). Same before tree:
frozen e7686236 → `absent 0/3 0/3 FAIL exit 1`; 819287e2 → identical; 8473abf6 and
8fa8e5cc → identical plus `CANARY=pass`. It evidences the tool's absence (true), never that
the counter discriminates.

**D7 (LOW) — `CANARY=pass` when the tool is absent** (`canary_ok` initialised to 1): the
regenerated before receipt prints `CANARY=pass`, which means "not tested", not "verified".

**D8 (LOW, closed by 8fa8e5cc) — span files were unpinned at 8473abf6.** A benign append to
`fixtures/…/spans/S901-1.txt` gave `C1=PASS` with no `FIXTURES_CHANGED`; a verdict-flipping
append gave `JUNK_KILLED=2/3`. 8fa8e5cc now pins both span files (digests match disk).

**Positive — the canary is real hardening.** Filename oracle: under 819287e2 `3/3 3/3
C1=PASS exit 0` (full marks, zero work — ExecCounterRun F1); under 8473abf6 and 8fa8e5cc
`CANARY=fail C1=FAIL exit 1`. Keep it — declared.

## 5. Verdict

Both receipts and the before row reproduce exactly, row for row, at both generations and at
the settled counter; revisions used are declared here (819287e2; 8473abf6; 8fa8e5cc; the
before row is invariant across all four incl. frozen e7686236). **No drifted or forged
number.** R46-C1's arithmetic holds at d09fc8e7 and at HEAD e50b388.

The round **record** does not hold: stale after-receipt (D1), undeclared pass-rule (D2), two
red windows on a frozen instrument (D3), a ×4-duplicated counter (D4), unshipped forges (D5).
In order: declare the CANARY leg in `claims.md` and re-freeze (or pin verdicts to 819287e2);
regenerate `measure-after.txt` at the settled sha; deduplicate to one `main`; ship the three
forges; freeze `c1-count.py` for the rest of the wave — 32 seats are scoring an artifact that
changed five times mid-flight.

## 6. Residual risk

- Forge semantics are my reconstruction; only exit codes compared, not stderr.
- The canary neutral-names only `POSITIVES[0]` and `JUNKS[0]`; defects keyed on the other junk
  classes or on the fixture-directory path are outside its reach.
- The span-pin probe is behavioural only; C1's span contents are RevC1Pin's item.
- `c2-count.py` also changed in the worktree (c2729d7f) — flagged for RevRerunC2.
- All times are point samples under concurrent commit; §0 is movement evidence, not a trace.
