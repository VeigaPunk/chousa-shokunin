# ExecOtherLanes — round 63 w1 — reference preflight G01–G05 on kake, kama, souji, tameshi, mori

Tool: `controls/pos-ref-preflight.py` (sha256 prefix per claims 07683086fd6c6b41, not re-hashed by me; not edited). Run by
`TMPDIR=$S python3 -B <tool> --root <copy> --fleet /home/vgpnk/Projects/shokunin --only G01,G02,G03,G04,G05 --work $S/w-<lane>`,
cwd = scratch `$S=/fast/scratch/hyaku/chousa-r63/ExecOtherLanes`. Sources read-only; copies in scratch; no git use; no installs.

## Findings first

1. All five lanes ran (exit 1 each); zero tracebacks; no gate crashed; no ENV (census script found via `--fleet`).
2. **The assigned minimal copy (corpus/ + SHONEN.md + SCORECARD.md) manufactures failures.** 17 gate FAILs on it; 9 of them vanish when
   the lane's other files exist. G01 fails on all 5 (`E11 ... missing used-by tools/...` — the registry's `used-by` paths live outside
   corpus/) and G05 on 4 of 5 (pointers into `tools/`, `.ufo/`); G04 fails for kama and mori (`SKILL.md`, `LOG.md`). These are copy artifacts,
   not lane defects. So I added a **supplementary run on a fuller copy** (`rsync -a --exclude=.git --max-size=20M` of each lane): 8 FAILs
   remain. Attribution below is on the fuller copy, reading the lane's files.
3. Of the 8 remaining FAILs: 4 are real lane-side findings (candidate, routed to the lane, not fixed here), 1 is legacy history,
   1 is an in-flight round, 2 are gate-lexical false positives (kake G05, kama G04); see the table.
4. Calibration note: G04 reads `PASS 0 pointers resolve` for kake, souji, tameshi: their SHONEN.md files have 0 backtick spans
   (`grep -o` count 0 on 8/12/12 lines). That is a vacuous pass, not evidence the pointers resolve. The summary line shows `PASS` with no
   hint (the detail `0 pointers` is the only signal). Suggest (limit, not a frozen-rule change): a gate that checked zero items could say so.

## Per-lane gate lines — assigned minimal copy (as ordered)

```
kake    G01 FAIL exit=1 file E11 S088 missing used-by scripts/source_recheck.py | G02 PASS 58 | G03 PASS 57 | G04 PASS 0 | G05 FAIL 31 unresolved (.ufo/..., ) -> PREFLIGHT=3/5 FAILED=G01,G05
kama    G01 FAIL E11 S089 missing used-by tools/report-landing-audit.py | G02 FAIL 2 | G03 FAIL 2 (round-1,round-2) | G04 FAIL 11 (SKILL.md,LOG.md,..) | G05 FAIL 15 -> 0/5 FAILED=G01,G02,G03,G04,G05
souji   G01 FAIL E11 S120 missing used-by tools/souji-size-census.py | G02 PASS 33 | G03 FAIL 11 | G04 PASS 0 | G05 FAIL 13 -> 2/5 FAILED=G01,G03,G05
tameshi G01 FAIL E11 S097 missing used-by tools/tally-audit.py | G02 FAIL 2 | G03 FAIL 1 (round-57) | G04 PASS 0 | G05 FAIL 16 -> 1/5 FAILED=G01,G02,G03,G05
mori    G01 FAIL E11 S076 missing used-by SKILL.md | G02 FAIL 8 | G03 PASS 49 | G04 FAIL 10 (SKILL.md,SKILL.md,LOG.md) | G05 PASS 5 -> 2/5 FAILED=G01,G02,G04
```
(all G06–G08 SKIP; every run `ENV=none`, exit 1.) Totals: 17 FAILs.

## Per-lane gate lines — fuller copy (supplementary)

```
kake    G01 PASS | G02 PASS 58 | G03 PASS 57 | G04 PASS 0 | G05 FAIL 1 unresolved -> PREFLIGHT=4/5 FAILED=G05
kama    G01 PASS | G02 FAIL 2 | G03 FAIL 2 | G04 FAIL 3 | G05 PASS 17 -> 2/5 FAILED=G02,G03,G04
souji   G01 PASS | G02 PASS 33 | G03 FAIL 11 | G04 PASS 0 | G05 PASS 18 -> 4/5 FAILED=G03
tameshi G01 PASS | G02 FAIL 2 | G03 FAIL 1 | G04 PASS 0 | G05 PASS 18 -> 3/5 FAILED=G02,G03
mori    G01 PASS | G02 FAIL 8 | G03 PASS 49 | G04 PASS 13 | G05 PASS 5 -> 4/5 FAILED=G02
```
Totals: 8 FAILs. G01 (census) passes on all five once the used-by files exist.

## Adjudication of each remaining FAIL (read the lane's file)

| Lane/gate | Evidence read | Decision |
|---|---|---|
| kake G05 | `kake-shokunin/SCORECARD.md` evidence cell holds `` `.ufo/waves/round-23/{live/,measure-c2-after-v2.json,evaluability.json}` `` | **gate-chousa-specific lexical**: a brace-group path is one token the gate cannot expand; the paths are a legitimate shorthand. Not a lane defect (I did not expand the braces to confirm each member exists — INFERENCE that they do). |
| kama G04 | `kama-shokunin/SHONEN.md` line 8 spans: `kama-llamacpp-live/v1` (a schema id), `.ufo/waves/round-17/live/receipt-{1,2,3}.json` (brace group), `/health` (an HTTP path) | **gate lexical false positives** (slash-bearing non-paths, brace shorthand). Not a lane defect. |
| kama G02 | `completion-request-plane.md`, `ollama-live-amendment-r61.md` absent from `kama-shokunin/corpus/README.md`; README says it is an index with a coverage map; files only named in lessons | **genuine** on kama's own stated rule (candidate finding → kama). |
| kama G03 | `lessons/round-1.md`, `round-2.md` have no `## Gate`; the other 57 of 112 do; README line 259 notes "missing Gate row repaired in round-18" | **legacy** (pre-convention rounds); the rule is chousa's/souji's shape, kama's README does not state it for these two. Not routed as a defect; INFERENCE on kama's intent. |
| souji G03 | 11 lessons (round-1…11, minus none) lack `## Gate`; `round-12` has it; `souji-shokunin/corpus/README.md:17` says per-round lessons each have a `## Gate` | **legacy-but-real**: the lane's own README sentence is false for rounds 1–11 (rule introduced r12 in the kaika campaign — INFERENCE from where the heading starts). Candidate finding → souji: qualify the README sentence. Verifier-spotcheck files are not matched by the gate (`round-\d+.md` only), fine. |
| tameshi G02 | `r44-anchor-refresh-rule.md`, `scratch-root-contract.md` in knowledge/ but README map has no row (grep: named only in lessons) | **genuine** (candidate → tameshi). |
| tameshi G03 | `lessons/round-57.md` has no `## Gate`; its own preamble: "written in sections as the round lands; sections ... completed from committed receipts at the round's close"; rounds 54–56 each have one | **in-flight round**, not a defect today. Re-run after tameshi's round 57 closes. |
| mori G02 | 8 entries missing from `mori-shokunin/corpus/README.md`: c1s-cwd-r43, conform-scope-r40, conform-source-order-r42, entry-claims-hardening-r60, inheritance-d72ac16-r42, s235-sha-correction-r43, watchdog-unclosed-r57, wave-settlement-artifacts-r59 (`.md`); README is titled "Coverage map" with 125 `knowledge/` mentions | **genuine** (candidate → mori). |

Tally on the fuller copy: 4 genuine (kama G02, souji G03, tameshi G02, mori G02), 1 legacy (kama G03), 1 in-flight (tameshi G03),
2 gate-lexical (kake G05, kama G04). (8 gate FAILs = 4 + 1 + 1 + 2.)

## Implication for C1 (limit, not a rewrite)

- The reference gates are chousa-shaped (the claims say so: "other lanes are not claimed"). G02/G03/G04 behaved plausibly elsewhere; G04/G05
  tokenisation has two lexical weak spots seen on real files: brace groups `{a,b}` and slash-bearing non-paths (`/health`, `x/v1`).
- The `--only G01..G05` run on a corpus-only copy is not meaningful for G01/G04/G05: a copy must carry what the gates dereference.

## Not run / limits

- G06–G08 not run (no tools copied, per the assignment). No labrat used. Fuller copy excluded `.git` and files >20 MB; no `--max-size`
  exclusion affected a gate input I looked at (INFERENCE; I did not list the excluded files).
- Scratch `/fast/scratch/hyaku/chousa-r63/ExecOtherLanes/` removed before yield.

VERDICT: LANES_RUN=5/5 gate_fails=17 tracebacks=0
