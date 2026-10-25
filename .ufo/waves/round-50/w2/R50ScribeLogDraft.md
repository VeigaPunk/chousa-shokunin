# R50ScribeLogDraft — round-50 LOG.md entry draft (chousa, wave 2)

Seat: `R50ScribeLogDraft` (scribe, leaf). Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Write boundary honoured: this report is the only file written in the lane. No production file, no
git index, no jj state, no `/home/vgpnk/Projects/shokuknow` write, no campaign tool run
(`renumber-staged.py`, `merge-plan.py`, `quote-lint.py`, `absent-defect-register.py` untouched).
No network, no fetch (L0 `8d77e6c1` open). No tool install or upgrade was needed or made.

## Facts I verified before drafting (command → observed)

```
$ git log --oneline -12
c5b8dca round-50: wave-2 spec and validated dispatch
74794db round-50: C2 adoption (S104-S106, three entries, 55-quote manifest, lesson), CJK grounding fix, five checks and receipts, QUALITY 73-79, SKILL gate rows
2573dc1 round-50: assimilate-rows selftest hardening (...)
ec52e63 round-50: assimilate-rows --selftest and lane default fixtures (C1 candidate); late round-49 seat reports
6a068f2 round-50: frozen claims, counters and do-nothing controls (pre-candidate)
4d13657 ... 3c51da7 round-49 verifier spot-check (integrator, hyaku): non-author admit/reject
$ git status --porcelain | head -3     → only ?? .ufo/waves/round-50/{w2.ready,w2.ready.dispatched,w2/}  (tree clean)
$ python3 corpus/evidence/round50/c1-count.py
SELFTEST_DEFAULT=PASS / BASELINE=PASS rc=0 findings=26 / PERTURB_PASS=6/6 / EXPECTED_BAD=PASS rc=2
R49_REGRESSION=PASS / LEGS=5/5 / C1=PASS                                    (rc=0)
$ python3 corpus/evidence/round50/c2-count.py
ENTRIES=3/3 / BOUND=3/4 (min 3) REFUSED=1 / BOUND_IDS=S104,S105,S106 / REF_ID_UNBOUND=0
NEW_GROUND=3/3 / QUOTE_ROWS=55 ON_BOUND=55/55 / SPAN_IDS=3/3
QUOTES_IN_SPAN=55/55 QUOTES_IN_ENTRY=55/55 QUOTES_IN_LESSON=55/55 QUOTE_SHORT=55/55 SPAN_CONTEXT=55/55
CAPTURE_BOUND=55/55 / SUBSTANCE=PASS / ANCHOR_BOUND=3/3 / INFERENCE_GROUNDED=3/3 / C2=PASS   (rc=0)
$ git show 3c51da77:corpus/SOURCES.md | grep -c "^| S[0-9]"   → 103
$ grep -c "^| S[0-9]" corpus/SOURCES.md                       → 106
$ git diff 3c51da77 74794db -- corpus/SOURCES.md | grep -c "^-[^-]"  → 0   (no registry cell edited)
$ python3 corpus/evidence/round50/name-collision-check.py .ufo/waves/round-50/w1-spec.json | tail -1
NAME_COLLISIONS=13 ITEMS=42
$ python3 corpus/evidence/round50/name-collision-check.py .ufo/waves/round-50/w2-spec.json
NAME_COLLISIONS=0 ITEMS=43
$ python3 corpus/evidence/round50/wave-complete-check.py .ufo/waves/round-50/w1-spec.json .ufo/waves/round-50/w1 | tail -1
OK 29/42 reports present in .ufo/waves/round-50/w1
$ python3 corpus/evidence/round50/wave-complete-check.py .ufo/waves/round-50/w2-spec.json .ufo/waves/round-50/w2 | tail -1
OK 12/43 reports present in .ufo/waves/round-50/w2      (piped through tail: its own exit code not captured)
$ python3 corpus/evidence/round50/decode-form-check.py corpus/lessons/round-50.md corpus/lessons/round-49.md
FORM_NAMED ×2 / DECODE_FORM=PASS (rc=0)
$ python3 corpus/evidence/round50/cjk-ground-check.py
CASE A rc=0 / CASE B rc=1 INF_TOKEN_NOT_IN_SPAN / CASE C rc=1 INF_UNCITED / CJK_GROUND=PASS (rc=0)
```

Wave shapes read from the specs themselves (`w1-spec.json`, `w2-spec.json`, key `items`): W1 42 seats
(scribe 18, executor 10, critic 4, reviewer 3, mutation-tester 2, connector 2, scout 2, simplifier 1);
W2 43 (reviewer 9, critic 9, executor 7, scout 6, mutation-tester 6, scribe 3, connector 2, simplifier 1).
All 43 W2 names carry the `R50` prefix; the 13 collided names map one-to-one (e.g. `CritForgeC1`→
`R50CritForgeC1`, `MineConsider`→`R50ScoutConsider`, `ExecMirrorCensus`→`R50ExecCensusMirror`).
Census receipt `.ufo/waves/round-50/assimilation/validate/census.txt` opened: exit 0, five W04
(S051, S053, S073, S074, S075), scratch mirror of base + append block. Lesson line 37 opened:
registry ids 103 (S001–S103) × staged ids 114 (S082–S195) → 22 collisions (S082–S103), 18 hard.
Lesson line 53 opened: the `refused-doc:` line for the 教师 manual (`bs.bnu.edu.cn`). Mistakes table:
7 data rows. `corpus/evidence/round50/claims-erratum.md` opened: items 1–3 changes + item 4 refusal.

Span re-slice I ran myself (peer claim below): each round-50 span file sliced out of its capture
`.txt` at the recorded `offset` — S104 `001287c4` 18 rows, S105 `e3ca8f4f` (sha `2197abe2…`) 34 rows,
S106 `28750bcd` 3 rows → **55/55 exact, 0 mismatches**.

## Draft — intended lane path `/home/vgpnk/Projects/shokunin/chousa-shokunin/LOG.md` (append after line 1807)

```markdown

## Round 50 — 2026-10-25 (second package adoption under section 10; citation-check theme; falsify round)

Claims froze in `corpus/evidence/round50/claims.md` at `6a068f2ae4847a1e4aa959f088a39ddc1b167bc0` after scoring the do-nothing controls: the base tool copied to `controls/tool-before.py` gives `BASELINE=FAIL rc=2`, `PERTURB_PASS=0/6`, `LEGS=2/5`, `C1=FAIL` exit 1; `controls/echo-tool.py` (replays the expected findings) `BASELINE=PASS` but `PERTURB_PASS=0/6`, `C1=FAIL`; `controls/const-tool.py` `BASELINE=FAIL`, `PERTURB_PASS=0/6`, `C1=FAIL`; the lane at base `3c51da77b3696ed884c943548ec4b4006e3ca528` gives `ENTRIES=0/3 BOUND=0/4 C2=FAIL` (`controls/c1-before.txt`, `controls/c2-before.txt`). C1 candidate `ec52e632`; C1 hardening `2573dc16`; C2 adoption `74794db07e1b383d5c3e96ad5122fd158a541271`; wave-2 spec `c5b8dca`; after-measurement `corpus/evidence/round50/measure-after-1.txt` (`<FINAL-HASH>`). No fetch; L0 `8d77e6c1` open.

- **C1 operability (capability extension)**: `tools/assimilate-rows.py --selftest` runs the adopter on an isolated fixture package (digest-pinned `corpus/evidence/round50/c1-fixtures/`) and diffs its finding lines against a hand-written `expected.json`; each of six perturbed copies must exit 1 naming the perturbation, and an unparseable expected file exit 2. `python3 corpus/evidence/round50/c1-count.py` → `SELFTEST_DEFAULT=PASS BASELINE=PASS rc=0 findings=26`, `PERTURB_PASS=6/6`, `EXPECTED_BAD=PASS rc=2`, `R49_REGRESSION=PASS`, `LEGS=5/5`, `C1=PASS` exit 0. Post-freeze hardening from W1 `ReviewSelftestCode` F1–F4 and `ExecSelftestEdge`: multiset comparison (a duplicated expected line printed `SELFTEST=PASS findings=26 expected=27` exit 0 at `ec52e632`, `SELFTEST=FAIL` exit 1 after — `selftest-duplicates-after.txt`), exit 2 on an option clash or a fixture with no entry, `ENTRYCITES … -` for an entry citing no id, a 120 s child timeout, tab-free findings, and `used-by` across twin staged ids. The frozen counter was not touched; it stayed `LEGS=5/5`.
- **C2 depth (sourced)**: the citation-check theme adopted BY DOCUMENT as `corpus/knowledge/istic-citation-verification-r39.md` (S104, tier A), `cnki-citation-check-r40.md` and `citation-matching-semantics-r41.md` (S105, S106, tier B); registry 103 → 106, the three rows new since base, 0 deleted registry lines in the diff, `used-by` naming their citing entries. The fourth staged document (CNKI 大学生论文管理系统使用手册（教师）, capture `275c79d45b1e9b0fd32cef93`) is refused: no lane row, no `source:` line, a `refused-doc:` line at `corpus/lessons/round-50.md:53`; a first integration draft that had bound it as S107 was reverted before any commit. `python3 corpus/evidence/round50/c2-count.py` → `ENTRIES=3/3 BOUND=3/4 (min 3) REFUSED=1 BOUND_IDS=S104,S105,S106 REF_ID_UNBOUND=0 NEW_GROUND=3/3`, `QUOTE_ROWS=55 ON_BOUND=55/55`, `SPAN_IDS=3/3`, `QUOTES_IN_SPAN=55/55 QUOTES_IN_ENTRY=55/55 QUOTES_IN_LESSON=55/55 QUOTE_SHORT=55/55 SPAN_CONTEXT=55/55`, the `CAPTURE_BOUND` leg 55/55, `SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=3/3`, `C2=PASS` exit 0. The manifest is `quotes.tsv` → `spans.tsv`, 55 quote rows; each span file is the exact capture slice at its recorded offset (re-sliced independently this round: 18 S104 + 34 S105 + 3 S106 rows, 0 mismatches). Controls: the three staged entries copied unchanged → `REF_ID_UNBOUND=15 BOUND=0/4 C2=FAIL`; the adopter's rewritten entries with its append block but no quote, span or lesson → `BOUND=3/4 REF_ID_UNBOUND=8 SPAN_IDS=0/3 C2=FAIL`. Named limit, declared before data: the counter cannot tell a re-grounded quote that supports its bullet from one that merely occurs in the capture; the Gate reader and the closure judge that.
- **Frontier / SOURCES**: registry 103 → 106 (S104 tier A, an own-service page; S105/S106 tier B vendor manuals), no older status/recheck/used-by cell edited; census `validate` on a pre-append mirror of base + append block + lessons, tools and the three entries: exit 0, the five pre-existing W04 only (`assimilation/validate/census.txt`); search-log entry Round 50. Section-10 collision check (`ExecCollision`, lesson line 37): registry ids 103 (S001–S103) against staged ids 114 (S082–S195) → 22 collisions (S082–S103), 18 hard (S082–S099) and four re-staged rows (S100–S103); renumber by document, one simultaneous substitution. `cited-id-check.py` on the as-staged renumber table → `BODY_CROSSREF S109->S104`, `BODY_CROSSREF S111->S105`, `CITED_IDS=FAIL rows=7` exit 1; with the body-only ids removed → `CITED_IDS=PASS rows=5` exit 0 (`cited-id-before.txt`).
- **Corrections / quality**: QUALITY 73 (a self-test compares against a hand-written expected file), 74 (a prose count is derived from a receipt by a check), 75 (a report is filed only after every seat report exists), 76 (every `char N` names its capture form), 77 (a run's renumbered ids are `source:` ids, never body cross-references), 78 (seat names unique across rounds), 79 (a grounding gate handles its inputs' script). Six new checks in `corpus/evidence/round50/`: `stale-count-check.py` (before: four `STALE … says 28, receipt 31`, exit 1), `wave-complete-check.py` (`MISSING` per absent seat report; at `5275c892` the round-49 w2 gaps, 27/35, exit 1), `cited-id-check.py`, `name-collision-check.py` (13 `NAME_COLLISION` of 42 items, exit 1), `decode-form-check.py` (`DECODE_FORM=PASS` on the round-49 and round-50 lessons), `cjk-ground-check.py` (cases A–C, `CJK_GROUND=PASS`).
- **Open at this entry**: `stale-count-check.py` prints one unresolved hit, `STALE corpus/README.md:1080 says 55, receipt 31` — a round-50 count read against the round-49 receipt, the check's named "one receipt per scan" limit; under the round-50 receipt the same scan leaves four unresolved (the `28`-era correction lines now disagree with 55). The after-receipt QUALITY 74 names, `stale-count-after.txt`, is absent at the tip (`git log --all` on that path is empty). Closure value: `<AFTER>`.
- **Post-freeze changes (erratum)**: `corpus/evidence/round50/claims-erratum.md` discloses three changes outside the frozen counters — `tools/assimilate-rows.py` hardening, `tools/inference-ground.py` `has_two_words` accepting four CJK characters (before it a correctly grounded pure-Chinese bullet read as zero tokens, so the frozen C2 leg was unattainable on these captures: `w1/DraftEntryR41.md` F1), and `build-spans.py` / `quote-substance-check.py` renumbered from round 49 — plus item 4, the 教师 manual row refused after a first draft bound it. No claim text, target or kill rule was narrowed after data. The round-46/47/48 counters print identical output before and after the CJK change (`inference-regression-before.txt`, `inference-regression-after.txt`); two of 65 entries differ in `--spans /dev/null` output and both exit 0 with their committed round-49 spans.
- **Inherited / spot-check intake**: the five round-49 routed items are recorded in `corpus/lessons/round-50.md` `## Spot-check intake` — late seat reports committed (`4d13657e`, `ec52e632`, `2573dc16`); the 28-versus-31 count closed by append-only `correction:` lines in `QUALITY.md`, `README.md` and `lessons/round-49.md` and, by this entry, in `LOG.md`; the self-test and digest-pin gate standard; report filed only after WAVE-DONE; decode form beside offsets. The lesson's `exit 1 → 0` for the stale-count check holds only once this entry's correction line lands, and then only for the LOG hit (see Open).
- **Waves**: W1 42 seats (scribe 18, executor 10, critic 4, reviewer 3, mutation-tester 2, connector 2, scout 2, simplifier 1); 13 of them reused round-49 seat names, the dispatcher resumed the parked round-49 agents of those names and each returned its round-49 report (`w1-results.json`; lesson Mistakes row 4), so 29/42 reports exist and `wave-complete-check.py .ufo/waves/round-50/w1-spec.json .ufo/waves/round-50/w1` prints 13 `MISSING`, exit 1. W2 43 seats (reviewer 9, critic 9, executor 7, scout 6, mutation-tester 6, scribe 3, connector 2, simplifier 1), every name carrying the `R50` prefix and re-assigning the 13 (`CritForgeC1` → `R50CritForgeC1`, `MineConsider` → `R50ScoutConsider`); `name-collision-check.py .ufo/waves/round-50/w2-spec.json` → `NAME_COLLISIONS=0 ITEMS=43` exit 0. WAVE-DONE: `<AFTER>`. L1 held the planner seat. No tool installs.
- **Append-only correction**: correction: LOG.md:1803 ("28 located quotes … `CAPTURE_BOUND=28/28`") superseded by 31 — round-49's `spans.tsv` carries 31 quote rows (`awk 'NR>1 && NF' corpus/evidence/round49/spans.tsv | wc -l` → 31); the 28 was that counter's capture-bound leg, and round 50's own counts belong to `corpus/evidence/round50/spans.tsv`, not to a round-49 form.
```

## Correction-line verification (scratch copy, lane untouched)

```
$ S=/dev/shm/chousa-r50-R50ScribeLogDraft   # LOG.md, corpus/{QUALITY,README}.md, lessons/round-49.md, evidence/round49/spans.tsv copied
$ cp LOG.md $S/LOG.md && cat entry.md >> $S/LOG.md          # 1807 + 14 = 1821 lines
$ python3 corpus/evidence/round50/stale-count-check.py --root $S
RESOLVED corpus/QUALITY.md:746 says 28, receipt 31
RESOLVED corpus/QUALITY.md:786 says 28, receipt 31
RESOLVED corpus/README.md:1074 says 28, receipt 31
STALE    corpus/README.md:1080 says 55, receipt 31
RESOLVED corpus/README.md:1083 says 28, receipt 31
RESOLVED LOG.md:1803 says 28, receipt 31          <-- the mandated line resolves
RESOLVED LOG.md:1821 says 28, receipt 31          (the correction line's own quote, self-named)
RESOLVED corpus/lessons/round-49.md:20 says 28, receipt 31
RESOLVED corpus/lessons/round-49.md:220 says 28, receipt 31
STALE_HITS=9 UNRESOLVED=1 RECEIPT_ROWS=31 / STALE_COUNT=FAIL (exit 1)
$ ... --root $S --receipt corpus/evidence/round50/spans.tsv
STALE corpus/QUALITY.md:746 says 28 / RESOLVED …786 says 28 / STALE …786 says 31 / STALE lessons/round-49.md:20 says 28 / STALE …:220 says 31
STALE_HITS=10 UNRESOLVED=4 RECEIPT_ROWS=55 / STALE_COUNT=FAIL (exit 1)
```

Before the draft, on the untouched lane: `STALE LOG.md:1803 says 28, receipt 31`, `UNRESOLVED=2`
(plus `README.md:1080`), exit 1 — and `grep -cE "correction:.*superseded by" LOG.md` → **0**.

## Findings

1. **QUALITY 74 cites a receipt that never existed.** `git log --all --oneline -- corpus/evidence/round50/stale-count-after.txt`
   prints nothing; the check, the QUALITY row and the round-50 README row all landed in the same commit
   `74794db`. QUALITY 74 states "after them `STALE_COUNT=PASS`, exit 0 (`stale-count-after.txt`)"; on the
   tip the check exits 1 with one unresolved hit, and with the round-50 receipt it exits 1 with four. The
   "shown able to fail" half is backed (`stale-count-before.txt`); the "after" half is not.
2. **Lesson Spot-check intake row 2 overstates the closure.** It says the 28-vs-31 count was corrected by
   append-only `correction:` lines in `corpus/QUALITY.md`, `corpus/README.md`, `LOG.md` and
   `corpus/lessons/round-49.md`, "`stale-count-check.py` exit 1 → 0". At the tip LOG.md holds 0 such lines
   and the check exits 1. The LOG half is supplied by this draft; the README half cannot be closed by an
   append (line 1080 is round-50 prose flagged against the round-49 receipt) without a later
   `correction:` line naming `corpus/README.md:1080` and quoting 55 — outside my write boundary.
3. **The correction mechanism is receipt-fragile, not round-fragile.** A correction line that quotes the
   superseding value (`… superseded by 31`) is itself a disagreeing number under any other receipt, so the
   same scan cannot pass under both round-49 (31) and round-50 (55) manifests: 4 unresolved under 55.
   QUALITY 74 names "one receipt per scan" but not that the correction lines bind to that one receipt.
   This is a design note for the check, not a defect in the round-50 claim counters.
4. **No defect in the two frozen counters at the tip**: both pass with the exact numbers quoted in the draft,
   and the do-nothing controls fail as frozen. I did not mutate them (out of seat scope; `R50Mut*` holds that).
5. **Peer IRC, resolved**: `R50ReopenRowS105` first flagged a uniform −80/−48 shift in the S105 offsets, then
   retracted it (the offset column is the span-block start; `CONTEXT=80`). My independent re-slice agrees with
   the retraction: 55/55 spans are exact capture slices, 0 mismatches. I sent that confirmation; the draft
   carries only the counter's result.

## Out of scope / not done
No edit to `LOG.md`, `README.md`, `QUALITY.md`, `SOURCES.md`, any counter or check. Wave 2 was at 12/43
reports when read, so the entry uses `<AFTER>` for WAVE-DONE and for the stale-count closure, and
`<FINAL-HASH>` for the after-measurement commit; no other value is a placeholder. Scratch
`/dev/shm/chousa-r50-R50ScribeLogDraft` deleted after the verification above.

VERDICT: attacked the round-50 LOG entry's factual base (frozen hashes, both counters, registry growth,
wave shapes, the 13-name collision and its W2 re-assignment) and the append-only correction path — survived
on every count and on the `LOG.md:1803` resolution (scratch: `RESOLVED`, exit 1 → the single remaining hit is
`README.md:1080`); **defect found** in calibration, not in the claim: QUALITY 74's after-receipt
`stale-count-after.txt` is absent from every commit and `STALE_COUNT=PASS` is unreachable at the tip, with the
lesson's intake row 2 claiming an `exit 1 → 0` that has not happened.
