# R51W2CritAdmission — the operator's case for rejecting C1, C2, C3, and what survives it

seat: R51W2CritAdmission (critic, w2) · lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Scored at `4436e279…`;
HEAD `72566c8`, and `git diff --stat 4436e27 72566c8 -- corpus tools SKILL.md QUALITY.md SCORECARD.md SHONEN.md LOG.md | wc -l` → `0`, so every number is the scored tip's. base `9ec1751a…`; freeze `d603f6f0…`. Counters run `env -u ASSIMILATE_CITES` except where the ambient case is the test. Scratch `/dev/shm/chousa-r51-R51W2CritAdmission-2/` (a `git archive` copy, never a symlink), deleted before finishing. No install; no lane file written.

```
$ c1-count.py            → LEGS=5/5 C1=PASS rc=0   (three fresh-nonce runs; --seed 7 and --seed 4242: same)
$ c2-count.py            → BOUND=6/7 REFUSED=1 QUOTE_ROWS=61 ON_BOUND=61/61 … C2=PASS rc=0; --lane-only C2=PASS
$ c3-count.py            → CAP_ROWS=36 (base 36) POINTERS=74 (base 74) RESOLVED_BY_CORRECTION=4 DANGLING=0 C3=PASS
$ build-spans.py --check → SPANS_ROWS=61 STALE=0 rc=0
```

## C1 — operability: forgeable, wedging, ambient-sensitive, and the repair instrument is itself broken

**Rejection case (strongest form).** `C1=PASS` is produced by a tool implementing none of the five behaviours:
`controls/forge-dirname.py:30` reads the subtest name out of its own `--out` (`scene = out.parent.name`) and the counter names its work directories literally (`c1-count.py:141` `"s"`, `:158` `"s-all"`, `:167` `"d1"`, `:174` `"d2"`, `:194` `tmp/name`).

```
$ python3 corpus/evidence/round51/c1-count.py --tool corpus/evidence/round51/controls/forge-dirname.py
SELFTEST_DEFAULT=PASS (skipped: --tool) … REGISTRY_STRUCTURE=PASS 4/4 LEGS=5/5 C1=PASS rc=0
$ … --tool controls/echo-tool.py → LEGS=2/5 C1=FAIL    $ … --tool controls/const-tool.py → LEGS=1/5
$ … --tool controls/flag-noop-tool.py → LEGS=2/5 C1=FAIL
```

Second, the round-49/50 one-shot counters are red at the tip. Third, the freeze target is unmeasurable on ~0.25 % of nonces: `c1-count.py:125` redraws only `c_id`, so when the first two draws collide the set can never reach 3.

```
$ timeout 25 python3 corpus/evidence/round51/c1-count.py --seed 13   → rc=124 (no C1 line)
$ faulthandler.dump_traceback_later(12) … runpy c1-count.py --seed 13
Timeout (0:00:12)! … File "corpus/evidence/round51/c1-count.py", line 125 in main
  (counter draws 13/182/324/785992967: n=getrandbits(32); top=randint(12,40); a=b=850/619/866/735 → HANG)
$ ASSIMILATE_CITES=all python3 corpus/evidence/round51/c1-count.py → SOURCE_ONLY=FAIL … LEGS=3/5 C1=FAIL
```

The ambient flip is in the frozen instrument, not merely disclosed: `grep -n "env=" …/c1-count.py` → no hit (only `c1-supplement.py:51,116`), so the tool docstring's "the round-51 counters run the tool with the variable removed from their environment" (`tools/assimilate-rows.py:75`) is false for the counter it names.

Fourth — what this seat adds — the **post-freeze supplement, the only artifact that separates the forge from the tool, dies on the same hang**. `c1-supplement.py:89-97` simulates the counter's draw order but omits the leading `getrandbits(32)` (`c1-count.py:121`), so `safe_seed` validates draws that are not the counter's:

```
$ python3 corpus/evidence/round51/c1-supplement.py          # unseeded, my run
Traceback … subprocess.TimeoutExpired: … c1-count.py --tool …/tools/assimilate-rows.py --seed 785992967
           timed out after 300 seconds          EXIT=1
$ simulation: seed 785992967 counter draws a=b=735 (HANG); safe_seed saw 602,735 (ok)
```

Three rounds per run × 1/401 ≈ 0.75 % crash rate, and the failure mode is a traceback, not `C1_SUPPLEMENT=FAIL`.

**Rebuttal from committed bytes.** (1) The kill target is met on my runs (three fresh nonces, two fixed seeds); a collision stall is an unrun seed, not a wrong answer, and it did not occur in those five. (2) Specificity is real when the supplement runs: `controls/c1-supplement-controls.txt` records real `6/6`, `forge-dirname` `1/6` (`SHAPE=PASS 3/3 MUTATION 0/3 CROSS_ENTRY 0/3 SOURCE_LINE 0/3 UNKNOWN_SRC 0/3 CLASH 0/3`), `tool-candidate1` `3/6`, `flag-noop` `1/6`, echo/const/tool-before `0/6`; `SKILL.md:133` registers it beside the frozen counter. (3) The r49/r50 red is the default flip, not a tool regression: `ASSIMILATE_CITES=all …/round49/c1-count.py` → `SETS_PASS=3/3 C1=PASS`; `round50/c1-count.py` → `LEGS=4/5` (`SELFTEST_DEFAULT=FAIL`, `BASELINE=PASS findings=26`, `R49_REGRESSION=PASS`) against `3/5` unset; `measure-r50-at-tip.txt` re-measures all four round-50 counters at `1d7aba0` as PASS, and `SKILL.md:135` carries the append-only correction naming `2a3389d`.

**C1 verdict: ADMIT as a capability extension — on counter + supplement, never on the frozen counter alone.** The tool's operability is not harmed (5/5 at the tip; legacy behaviour preserved by `--cites all`). The instrument is forgeable, can wedge forever, and honours an ambient variable — instrument defects, not axis harm. Corrections, no predicate/target change: in `safe_seed` add `r.getrandbits(32)` before `r.randint(12, 40)` (simulated: rejects 13/182/324/785992967, accepts 7) and catch `TimeoutExpired` with a reseed; strip `ASSIMILATE_CITES` in `c1-count.run()`; either implement random scene names or rewrite QUALITY 85's first clause and `c1-supplement.py:12` (SHAPE at `:115` is `c1-count.py --tool …` verbatim, so it inherits `s`/`d1` and the forge passes it).

## C2 — depth: entailment uncounted, one refusal for capture form, a three-term NEW_GROUND

**Rejection case.** (a) Nothing counts entailment: 61 quotes are proved present in span, entry, lesson and capture, and `quote-substance-check.py` is a floor ("a long quote can still be beside the point"). (b) One of seven documents is refused, and the theme is by document, so a refusal for *capture form* reads as declining readable evidence. (c) `NEW_GROUND` is one `git grep` over the union of three terms, so it cannot say which entry is new.

**Tested.** (1) The limit is declared before data (`claims.md` §R51-C2: "measures binding and presence, not entailment … restated before data"), and the Gate carries the per-entry judgment: `corpus/lessons/round-51.md:58` adjudicates **every** unadopted staged entry with reason and flip; `:72-87` gives six register verdicts in named forms. (2) All 61 manifest quotes, re-located by me against the cache: every span is the exact capture slice at its recorded offset (`t[offset:offset+len(span)] == span`, 61/61), every quote occurs exactly once in its `.txt` (61/61) and once inside its span, all ≤25 whitespace words and ≤160 characters (61/61), and the quote offsets match the lesson table (S107 → 10232, 10234, 10239, 10301). (3) The refusal is evidenced, not a skip: the S125 `.txt` opens `PK\x03\x04`, is 168 952 characters with 72 117 U+FFFD, and holds the document's phrases 0 times; the substance sits only in the zip member — `word/document.xml` run-concatenated, `SRにおける文献検索期間について明記する。` occurs once at char 160571, 0 times in the `.txt`. No lane row (`corpus/SOURCES.md` has no line with that URL), no `source:` line in the three entries, and `corpus/lessons/round-51.md:56` is the `refused-doc:` line with the flip (a counter that reads a zip member) and the reason "for its capture form, not for its source quality". (4) NEW_GROUND errs strict, not loose: `held_terms.returncode == 1` is one grep over all three terms, so one old term zeroes all three (`git grep -l` per term at `9ec1751a` → 0 files each; entries hold 検索式 6, 检索策略 6, 検索期間 4 lines).

**C2 verdict: ADMIT; the depth axis is not harmed.** Its ceiling is "binding + presence + a human Gate", declared, and the Gate is populated. Corrections: one grep per term; drop the dead `HELD: set[str] = set()` (`c2-count.py:81`, `unb` is stricter with it empty); apply the zip-member form next round — the named flip, not a frozen-predicate change.

## C3 — calibration: existence, an erratum after the freeze, and false sentences

**Rejection case.** The counter passes on existence, so a `correction:` line is a general escape hatch; and a *counter* changed after the freeze commit.

**Tested.** (1) The escape hatch is real and I ran it: on the archive copy, append ``| fabricated capability row (critic control) | … | `nope/missing-evidence.py` | 51 |`` plus `correction: SCORECARD.md:2635 nope/missing-evidence.py -> LOG.md` (LOG.md never mentions it) → `CAP_ROWS=38 POINTERS=75 RESOLVED_BY_CORRECTION=5 DANGLING=0 C3=PASS rc=0`. The landed repairs are not that: all five targets existed at the base (`git cat-file -e 9ec1751a:<path>` → `PRESENT_AT_BASE` for `.ufo/waves/round-32/measure/final/battery.out`, both round-36 JSONs, `corpus/evidence/round50/c1-supplement.py`, `corpus/evidence/round25-meta-differential.log`) and each shows the claim. All four SCORECARD corrections preserve the pointer's basename, so basename equality is a safe tightening; the blanket control gives `RESOLVED_BY_CORRECTION=0 DANGLING=5 C3=FAIL` (`controls/c3-controls-final.txt`), so a correction must name the row's exact line and pointer already. (2) The erratum is post-freeze but pre-dispatch: `git log -1 cfe6c9f` → 20:07:05; `stat …/w1.ready.dispatched` → 20:18:36; earliest wave-1 seat report 20:20:47; `git diff d603f6f HEAD -- …/c1-count.py …/c2-count.py …/claims.md` is empty (only `c3-count.py` differs, and only in `pointers()` — extraction, not target).

**What breaks — and it is not the counter.** `corpus/lessons/round-51.md:27` says "`corpus/evidence/round51/measure-after.txt` opens with a `tool-rev:` header and `receipt-check.py` (QUALITY 84) prints `RECEIPT_OK`". That file has never existed:

```
$ ls corpus/evidence/round51/measure-after.txt   → No such file or directory
$ git log --all --oneline -- corpus/evidence/round51/measure-after.txt | wc -l → 0
$ python3 corpus/evidence/round51/receipt-check.py corpus/evidence/round51/measure-r50-at-tip.txt --skill SKILL.md
RECEIPT_NO_REV corpus/evidence/round51/measure-r50-at-tip.txt
SKILL_NO_PIN SKILL.md          CHECKS=2 OK=0 FAILS=2 RECEIPT_CHECK=FAIL   EXIT=1
```

The `SKILL_NO_PIN` half is disclosed — `corpus/QUALITY.md:906-907` names exactly `RECEIPT_NO_REV …measure-after.txt` and `SKILL_NO_PIN SKILL.md`, `FAILS=2 rc 1` as the state its check catches, and `receipt-check.py:57` reads only the first five lines while the pin sits in `SKILL.md:133`. The lesson sentence is disclosed nowhere. Second false sentence: `corpus/QUALITY.md:916` says of the echo control "at the tip it scored `LEGS=5/5` and had stopped being a control" — at the tip it scores `LEGS=2/5` (my run above), because `cf642c6` re-pointed its delegation to `tool-before.py` (`controls/echo-tool.py:12`). Third: `claims-erratum.md` carries E1 only (`grep -c '^## E'` → 1) while `c1-supplement.py:4` and `QUALITY.md:916` cite E2–E4 (the forge, hang and ambient classes — each real, each reproduced above); corroborated by `w2/R51W2ReviewGatesRows.md:39` and `w2/R51W2ReviewQuality8186.md:28`.

**C3 verdict: the frozen predicate HOLDS at the tip; the calibration axis IS harmed** — not by the counter, by three committed sentences asserting artifacts or measurements the tip does not have (lesson row 27, QUALITY 85's echo clause, the E2–E4 citations). All fixable without touching the predicate: file a `measure-after.txt` with the five-line header (or correct row 27), add the `tool-rev:` header to `SKILL.md:133` and scan the whole file in `header()`, write E2–E4 into `claims-erratum.md`, add the basename-equality correction rule.

## Verdicts

**C1 operability — ADMIT** (on counter + supplement); axis not harmed; instrument forgeable / wedging at 1/401 / ambient-sensitive, and the supplement's seed guard is off by one draw (observed crash). **C2 depth — ADMIT**; axis not harmed; ceiling is binding + presence with a populated, unaudited Gate. **C3 calibration — ADMIT on the frozen target, AXIS HARMED** by three false self-assessment sentences. No frozen predicate, target, counter or control needs changing.

**Could not decide:** (i) whether the supplement's five non-SHAPE legs are themselves forgeable — I did not attempt a forge against them (the mutation seat owns that); (ii) whether round-50's counter is restorable at the tip by any single environment — `4/5` with `ASSIMILATE_CITES=all`, `3/5` without, its `SELFTEST_DEFAULT` leg reading fixtures that are now source-mode; (iii) whether lesson row 27's receipt was planned-and-dropped or lost — it has no history at all.

VERDICT: attacked C1's instrument (forge 5/5, infinite loop at `c1-count.py:125` reproduced by seeds 13/182/324/785992967, ambient flip at 3/5, and the supplement's `safe_seed` off by one draw crashing my own unseeded run), C2's refusal and entailment (S125 `.txt` is zip bytes, 72 117 U+FFFD, quote only at 160571 in the unzipped member; all 61 quotes unique and exact in their captures) and C3's existence/erratum (a fabricated correction passes; the erratum preceded dispatch; lesson row 27, QUALITY 85's echo clause and the E2–E4 citations are false at the tip) — C1 and C2 stand, C3's target stands but its axis is harmed by three sentences, and no frozen predicate needs changing.
