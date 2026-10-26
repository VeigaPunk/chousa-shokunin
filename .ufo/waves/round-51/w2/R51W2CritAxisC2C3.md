# R51W2CritAxisC2C3 — C2 and C3 attacked as axis moves

Critic, wave 2. I attack only the axis attribution and the evidence these two claims are scored on; frozen predicates, targets, counters, controls and produced text are untouched. Lane HEAD at review `72566c8` (the brief's `4436e279` is the last content commit; the delta is the wave-2 spec commit). Counters run `env -u ASSIMILATE_CITES`; scratch `/dev/shm/chousa-r51-R51W2CritAxisC2C3/` (deleted); no install, no network, no lane write.

## 1. C2 — is `depth` the right axis, and does "name the axis by the surface the round changes" apply?

**1.1 The cited rule is precedent, not AXES.md.** `grep -n "surface" AXES.md` prints only `:12` (coverage) and `:14` (freshness); the sentence is at `.ufo/prompts/chousa-round-29.md:361`, applied at `.ufo/reports/round-29/chousa.md:7`. I judge C2 against it, and against `AXES.md:21` — "Expansion ↔ `coverage` + `adjacency`; quality ↔ `depth` + `freshness` + `operability`".

**1.2 Two surfaces moved, one axis named.** (a) Expansion: six new Registry rows (`corpus/SOURCES.md:117-122`, S107–S112) and three new `corpus/knowledge/` files — the lane's word is coverage: `corpus/README.md:1093` "Coverage credit for round 51 is per document … six documents is six registry rows (`S107`–`S112`)". (b) Entry detail: depth's surface (`AXES.md:11`). Depth's discriminating artifacts are absent: `grep -c '^|'` on the three entries → `0 0 0` (no decision table, threshold or error signature), and depth's signal — "a reader can act on SKILL.md alone" — is not advanced (`grep -c "search-record" SKILL.md` → `0`; `corpus/README.md` → `6`). In province, not adjacency: `PROVINCE.md:5,7` owns "search-strategy taxonomy".

**What holds.** The sourced-detail surface did move. I re-implemented the quote legs over all 61 manifest rows against the read-only cache (capture resolved by recorded sha256; form = `.txt` read in Python text mode, which is what `build-spans.py` and `c2-count.py` use):

```
ROWS 61  digest_mismatch 0  offset_mismatch 0  span_not_longer 0  not_in_span 0  not_in_entry 0
         not_in_lesson 0  over_160_chars_or_25_words 0  count(quote)!=1 0
$ python3 corpus/evidence/round51/c2-count.py → ENTRIES=3/3 BOUND=6/7 (min 5) REFUSED=1
  BOUND_IDS=S107..S112 REF_ID_UNBOUND=0 NEW_GROUND=3/3 QUOTE_ROWS=61 ON_BOUND=61/61 SPAN_IDS=6/6
  QUOTES_IN_SPAN/ENTRY/LESSON=61/61 each SUBSTANCE=PASS CAPTURE_BOUND=61/61 ANCHOR_BOUND=6/6
  INFERENCE_GROUNDED=3/3 QUARANTINE_VERDICTS=6/6 C2=PASS rc=0
$ python3 corpus/evidence/round51/quote-substance-check.py → IDS=6 QUOTES=61 FAILURES=0 rc=0
```

New ground, not a re-score of an entry: `git grep -c -e 検索式 -e 検索期間 -e 检索策略 9ec1751a… -- corpus/knowledge` → rc=1 (absent at base). But the leg is narrower than "ground": `git grep -c 検索 9ec1751a… -- corpus/knowledge` → `aggregator-vs-source-r36.md:6`, `citation-count-semantics-r37.md:1`, and the theme already had a base entry (`git ls-tree -r 9ec1751a… corpus/knowledge | grep -c search` → `1`, `search-log-method-r39.md`). So `NEW_GROUND=3/3` proves three *words* are new, not that the theme's ground is.

**Counterexample (survives all three counters).** `corpus/README.md:1090` says "what a Chinese search record carries **and that China has no standard for one yet**"; its own entry `corpus/knowledge/chinese-search-record-r39.md:26` says "neither copy supports a statement that no Chinese standard for search reporting exists". C2 reads entries/registry/spans/lesson, C3 reads SCORECARD/SHONEN, C1 neither — the overreach is unmeasured.

**C2 verdict — holds only as depth(sourced), for the entries, not the documents.** Depth is the defensible axis for the surface actually scored (61 located quotes, six anchors, grounding 3/3); the six documents are expansion/coverage credit by the README's own words, and C2's headline legs (`BOUND=6/7`, `NEW_GROUND=3/3`) count documents — coverage evidence inside a depth claim. No axis harmed. The SCORECARD row must not claim decision-grade depth and must not book the documents twice.

## 2. C3 — does pointer resolution measure AXES.md calibration, or link-rot?

**2.1 Axis naming holds; the measurement does not reach the axis.** The surface C3 changes is the self-assessment (`SCORECARD.md` evidence cells, `SHONEN.md` lines) → calibration by the rule. But `AXES.md:15` defines calibration as "gaps named honestly, confidence graded, overreach caught", signal "SHONEN.md/SCORECARD entries match observed repo state", while `c3-count.py:44-62` resolves tokens with `real()` = non-empty file *or a directory holding any file*, plus a `correction:` line naming an existing non-empty path. That is resolution, not match. W1 `R51ConnCrossClaim` ("link-rot only") is confirmed — and it is reachable, not merely declared:

```
$ python3 corpus/evidence/round51/c3-count.py        # tip
CAP_ROWS=36 (base 36) POINTERS=74 (base 74) RESOLVED_BY_CORRECTION=4 DANGLING=0 C3=PASS rc=0
$ python3 corpus/evidence/round51/c3-count.py --root /dev/shm/…/base   # base self-assessment
DANGLING SCORECARD.md:1843 measure/final/ :2073 …c1-s36361.json :2074 …c2-s36371.json
        :2616 c1-supplement.py  DANGLING SHONEN.md:10 round25-meta-differential.log
DANGLING=5 C3=FAIL rc=1
# scratch copy of tip; retarget ONE landed correction (row 2073) at a file that says nothing about it
$ python3 -c 'p="/dev/shm/…/wrong/SCORECARD.md";t=open(p).read();open(p,"w").write(
  t.replace("-> .ufo/waves/round-36/measure-l1/c1-s36361.json","-> corpus/README.md"))'
$ python3 corpus/evidence/round51/c3-count.py --root /dev/shm/…/wrong
RESOLVED_BY_CORRECTION=4 DANGLING=0 C3=PASS rc=0
# second scratch copy; row 1843 retargeted at a whole directory
  "-> .ufo/waves/round-32/measure/final/" → "-> corpus"  → same three lines, C3=PASS rc=0
```

So `C3=PASS` is reachable with false provenance: an unrelated file, or any directory holding a file, repairs a pointer. The predicate's named limit ("existence, not truth") covers this, and QUALITY 83 (`corpus/QUALITY.md:882`) *is* "resolves, or carries a `correction:` line naming a non-empty target" — the criterion is met; the axis is not.

**What holds.** The four landed corrections are substantively right (targets opened): 1843 → `.ufo/waves/round-32/measure/final/c1-s32101.json` (`APPEND_SERIALIZED=24/24`), 2073 → `c1-s36361.json` (`ENGINE_SWAP_CANARY=14/14`), 2074 → `c2-s36371.json` (`WITNESS_PER_RECORD=5/5`), 2616 → `corpus/evidence/round50/c1-supplement.py` (4175 B, docstring says round 50). The paralleled `corpus/evidence/round3{2,6}/measure*` paths do not exist, so no resolution was possible without a correction; `SHONEN.md:10` was fixed in place (`corpus/evidence/round25-meta-differential.log`, 47 B). Four of 36 rows still *print* the bare pointer a reader follows — repairs sit at `SCORECARD.md:2626-2629`.

**Control gap.** `controls/build-c3-controls.py` seeds BLANKET (unparseable line), DELETED (rows gone), EMPTY (zero-byte files) and DOTPATH (a real dot path); none seeds a *mis-targeted but existing* correction, so the class above escapes every control — the QUALITY 86 lesson applied to the correction leg. **Doc/code divergence (minor):** the docstring says "a later line of `SCORECARD.md`"; the parser (`c3-count.py:96-99`) scans the whole file and checks no order (no exploit found; row number must match exactly).

**C3 verdict — holds as a narrow calibration repair (pointer existence, QUALITY 83), not as the AXES calibration signal.** The round may say "evidence-pointer text resolves", never "SCORECARD/SHONEN entries match observed repo state".

## 3. E1 — honest before→after when the tokenizer was corrected after the freeze?

Yes, on the evidence, with two caveats to carry. **Replayed:** the corrected counter over the BASE self-assessment reproduces the erratum's `DANGLING=5` exactly (identical list to `controls/c3-before-erratum.txt`); the 8 is the pre-erratum instrument, whose three extra lines are tracked dot-leading paths (`git ls-tree -r --name-only 9ec1751a… | grep -cE '^\.ufo/waves/(round-34/measure|round-25/build/ConnectorMetaSiblings)'` → `66`). The tuning makes the before *smaller* (5, not 8), so the improvement is 5→0, never 8→0 — conservative; and no landed self-assessment quotes the 8 (`grep -rn "DANGLING=8" SCORECARD.md LOG.md corpus/README.md SKILL.md` → no hit). The report must quote 5 and show both receipts; frozen `claims.md`'s "`DANGLING=8`" must not be repeated.

**Caveat 1 — provenance sentence.** `claims-erratum.md` says the fix landed "before the wave-1 `.ready` file was taken"; `.ufo/waves/round-51/w1.ready` mtime is `20:01:22`, the fix commit `cfe6c9f` is `20:07:05`. What guarantees no seat scored with the buggy counter is `w1.ready.dispatched` = `2026-10-25T20:18:36` (spec regenerated 20:06:59) — dispatch, not the `.ready` take. Smallest correction: say "before wave-1 was dispatched".

**Caveat 2 — quote form.** Offsets are into the `.txt` read in Python text mode (universal newlines). Read byte-preserving and six S111 offsets shift (`695→896, 702→903, 934→1168, 1078→1334, 1138→1404, 1366→1706`) — the only CRLF capture. The counter is self-consistent (61/61 both legs), but the lesson's "form `.txt` read as UTF-8" should read "(universal newlines)" so `char N` is reproducible.

## 4. Smallest safe corrections (drafts; L1 integrates)

```markdown
# intended lane path: corpus/README.md:1090 — drop the clause the entry forbids, keep the narrow one already there
| `knowledge/chinese-search-record-r39.md` | Round-51 note (adopted by document from `merge/chousa/`): what a Chinese search record carries — …

# intended lane path: SCORECARD.md — round-51 C2 verdict row
| depth (sourced) | `ENTRIES=0/3 BOUND=0/7 C2=FAIL` → `BOUND=6/7 REFUSED=1 NEW_GROUND=3/3 QUOTE_ROWS=61 SUBSTANCE=PASS ANCHOR_BOUND=6/6 C2=PASS` | `python3 corpus/evidence/round51/c2-count.py` | **improved, provenance only**: depth moves through cited sources (61 located quotes, six anchors); no decision table, threshold or error signature, and `SKILL.md` names none of the entries. `BOUND`/`NEW_GROUND` count documents and are coverage credit (`corpus/README.md:1093`), not depth evidence | ground |

# intended lane path: SCORECARD.md — round-51 C3 verdict row
| calibration | `DANGLING=8` (pre-erratum) / `DANGLING=5` (corrected, same instrument as the after) `C3=FAIL` → `DANGLING=0 C3=PASS`; `CAP_ROWS=36 (base 36) POINTERS=74 (base 74)` | `python3 corpus/evidence/round51/c3-count.py` | **improved narrowly**: evidence-pointer existence only (QUALITY 83); a `correction:` naming an unrelated existing file, or a directory, also passes (demonstrated); four rows print the bare pointer, repaired only at `:2626-2629`; gaps/confidence/overreach unmeasured | plumbing |

# intended lane path: corpus/evidence/round51/claims-erratum.md — append-only E5
E5 — E1's timing sentence: the fix landed before wave-1 was DISPATCHED (`w1.ready.dispatched` 20:18:36,
fix `cfe6c9f` 20:07:05); `w1.ready` was taken 20:01:22, before the fix, and deferred.
```

Next-round hardening (predicate frozen): a `WRONGTARGET` control — one landed correction retargeted at an unrelated non-empty file, one at a directory — must print `C3=FAIL` under a counter that checks something about the target (existence at BASE, or the row's named command).

## 5. Observed, untouched

`git status --porcelain`: `M .ufo/waves/round-51/w1/R51DraftSkillGates.md` (a wave-1 seat report edited in the worktree after its commit), plus untracked `w2.ready*` and `w2/`. Wave-1 reports are read-only evidence; no lane file is mine to edit. No tool installed; no network; scratch deleted.

VERDICT: attacked C2's depth attribution and C3's calibration attribution — C2 stands as depth(sourced) for the entries' cited-source surface, with the six documents booked as coverage and `README:1090` contradicting its own `chinese-search-record-r39.md:26`; C3 stands only as pointer resolution (QUALITY 83), demonstrated to pass with an unrelated file and with a bare directory, so it is not AXES.md calibration; E1's before→after is honest (5→0 replayed with the corrected instrument, the 8 being three tracked dot-leading false positives), with the erratum's `.ready` timing sentence and the universal-newline quote form to correct.
