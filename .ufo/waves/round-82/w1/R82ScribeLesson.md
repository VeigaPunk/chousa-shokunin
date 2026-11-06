# R82ScribeLesson — round-82 lesson draft (leaf scribe)

Seat `R82ScribeLesson`, lane chousa, wave `chousa-r82-w1`. Leaf: no subagents, no `agent://all`, no network, no
commits, no lane or fleet git/jj mutation, no production edits. Every command ran from the lane root
`/home/vgpnk/Projects/shokunin/chousa-shokunin`; scratch was `/fast/scratch/hyaku/chousa-r82/R82ScribeLesson/`
(created with `mkdir -p`, deleted before this report was finalised).

## Behavior

1. Read the frozen claims (`corpus/evidence/round82/claims.md`) first, including the four C1 kill rules and four C2
   kill rules, then the round-81 lesson for format.
2. Built the `## Gate` section from committed bytes only: five registry rows (S008, S209, S210, S211, S028), their
   2026-11-06T19:42Z `refetch.tsv` rows, their captures, and the base→landing `corpus/SOURCES.md` diff.
3. Mined one mistake: R81ReviewerC2's `r4-07-alt-section.md`, described as "reason present, flip empty" while its
   flip cell is filled and the only change from `item4-pass.md` is the heading.
4. Read `considerthese/2026-11-06.md` and `2026-11-05.md` (never edited), named one still-unimplemented proposal,
   and re-counted the round-78 collision file for `## Assimilation`.
5. Wrote the draft at `.ufo/waves/round-82/w1/R82ScribeLesson/lesson-draft.md`; no production file was edited.

## Gates (what was run, and what it printed)

| check | command (lane root) | observed | rc | receipt |
|---|---|---|---|---|
| five Gate quotes located | `python3 -c "$LOC" corpus/captures/<key>.txt '<quote>'` ×5 | `FOUND` ×5; `wc -w` = 18/20/17/21/16 | 0 | `receipts/01-gate-quote-locate.txt:6-39` |
| captures = fetch bytes | sha256 of each `corpus/captures/<key>.txt` vs its `refetch.tsv` `txt_sha256` | `MATCH` ×5 | 0 | `receipts/02-capture-sha-vs-refetch.txt:3-7` |
| registry delta | `git diff --numstat 142b6f0c… b4a41d25… -- corpus/SOURCES.md` | `5 2 corpus/SOURCES.md`; base has 0 of the three new rows (rc 1), landing has 3 | 0 | `receipts/03-registry-diff.txt:3,15-19` |
| S008 anchor structure | `grep -n 'Key Points\|2.1 Rationale\|2.3 Defining' corpus/captures/fd7eed5e….txt` | `Key Points:` at 531, **before** `2.1 Rationale` at 538; `2.3 Defining` at 556, Q1 at 560 | 0 | `receipts/03-registry-diff.txt:55-93` |
| S209 title vs slug | `grep -n '10.2.2'` + nav list + content area | served title `10.2.2 Developing your protocol` at 189/715/733; nav lists 10.2.1–10.2.12 | 0 | `receipts/04-s209-title-slug.txt:6-9,27-52` |
| SPIDER / PRISMA-ScR unopened | `grep -c` over `SOURCES.md`, `refetch.tsv`, five captures | 0 rows, 0 refetch rows, 0/5 captures, 0 entry hits | 0 (counts 0) | `receipts/05-unopened-candidates.txt` |
| old gate on the two records | `bash "$S/tree-r81/tools/research-gate.sh" verify-sweeps <record> --root "$S/tree-r81"` (tree = `7e2da96a`) | identical `VERIFIED_SWEEPS=1/1 REJECTIONS_OK=0/0` / `CLEAN` for r4-07 and r4-07b | 0 / 0 | `receipts/06-r4-07-description-vs-bytes.txt:31-42` |
| landed gate on the two records | `bash tools/research-gate.sh verify-sweeps <record> --root .` | r4-07 `flip=present … complete` `REJECTIONS_OK=1/1`; r4-07b `flip=absent … incomplete` + `SWEEP_REJECTION_INCOMPLETE`, `REJECTIONS_OK=0/1` | 0 / 1 | `receipts/06-r4-07-description-vs-bytes.txt:45-59` |
| described-form checker | `python3 .ufo/waves/round-82/w1/R82ScribeLesson/check-described-form.py <record> --reason present --flip absent` | r4-07 `DESCRIBED-FORM MISMATCH … bytes=present`, `bad=1`; r4-07b `bad=0` | 1 / 0 | `receipts/07-described-form-check.txt:5-24` |
| closure's eleven | `grep -n 'eleven K2' corpus/lessons/round-81-verifier-spotcheck.md`; `grep -c '^| F2-\|^| F4-' attack.md` | line 103 says eleven; 6 F2 + 5 F4 rows, F4-5 present | 0 | `receipts/07-described-form-check.txt:37-44` |
| considerthese | twelve-id grep over round-82 material; `ls corpus/lessons/round-82.md`; `git diff --name-only …` | 0/12 outside one fleet-grep artifact (its S183 is `mado-shokunin`'s); lessons file absent (rc 2); no considerthese/lessons in the round diff | 2 on `ls` | `receipts/08-considerthese.txt:12-21` |
| assimilation | `wc -l` on the round-78 collision files | `collisions` 111, `staged-ids` 114, `reg-ids` 192, live registry 211 | 0 | `receipts/09-collisions.txt:3-10` |

No claim predicate was run: `k2-gate-r82.py`, `depth-r82.py` and `research-gate.sh --selftest` were **not**
executed by this seat. The gate runs above are the two r4-07 records, which are evidence about the mistake
section, not the C1 predicate.

## Touched surfaces

- `.ufo/waves/round-82/w1/R82ScribeLesson/lesson-draft.md` — the deliverable.
- `.ufo/waves/round-82/w1/R82ScribeLesson.md` — this report.
- `.ufo/waves/round-82/w1/R82ScribeLesson/receipts/01-gate-quote-locate.txt` … `09-collisions.txt` — nine receipts.
- `.ufo/waves/round-82/w1/R82ScribeLesson/check-described-form.py` — the described-form checker.
- `/fast/scratch/hyaku/chousa-r82/R82ScribeLesson/` — `tree-r81/` (a `git archive 7e2da96a` extraction) and one
  command output file; deleted before yield.

## Out of scope (not done)

No edits to `corpus/` (claims, counters, manifests, fixtures, receipts, captures, `SOURCES.md`, `README.md`,
`lessons/`), `SKILL.md`, `tools/`, `.ufo/waves/round-78/`, `considerthese/`, `/home/vgpnk/Projects/shokunin/scripts`,
`/home/vgpnk/Projects/shokunin/.ufo/state`, `MANIFEST.json`, `LOG.md`, `SCORECARD.md`, `QUALITY.md`, or any sibling
repo. No commits, pushes, lane git/jj mutation, or fixture git repo. No network, no `/tmp` writes, no host sysctl or
service changes. No tools installed; no pacman, `uv`, or `npx` transaction was attempted.

## Findings

**F1 — five Gate records are grounded; the bytes located are the bytes fetched.** The five 19:42Z rows answer
HTTP 200 / `curl_rc=0`, and each capture's sha256 equals its `refetch.tsv` `txt_sha256`
(`receipts/02-capture-sha-vs-refetch.txt:3-7`, `MATCH` ×5, rc 0). Each ≤25-word quote prints `FOUND`, rc 0
(`receipts/01-gate-quote-locate.txt`, sections S008/S209/S210/S211/S028). Registry delta is exactly the five rows:
`git diff --numstat` = `5 2 corpus/SOURCES.md`; no other line changed (`receipts/03-registry-diff.txt:3,21-52`).

**F2 — the S008 anchor cell misdescribes the page (reported, not repaired).** The new cell reads "sections 2.1 Key
Points and 2.3 …". Command:
`grep -n 'Key Points\|2.1 Rationale\|2.3 Defining' corpus/captures/fd7eed5e0e6c64e22bc1470c.txt` → `531: Key
Points:` before `538: 2.1 Rationale for well-formulated questions`; the chapter's Key Points box is not section
2.1, and no heading "2.1 Key Points" exists (rc 0). The old anchor's `2.1 rationale` names a heading the page still
carries. The row's `teaches` claim is unaffected (the entry's quotes sit under `2.3 Defining`, heading line 556,
Q1 line 560). Receipt: `receipts/03-registry-diff.txt:55-93`. This is a residual, not a kill: no frozen rule names a
registry anchor cell.

**F3 — S209's slug and served title differ; admitted with the drift recorded.** Command:
`grep -n '10.2.2' corpus/captures/213237301753814b95b24684.txt` → title at 189, breadcrumb 715, h1 733; the nav
sidebar lists 10.2.1–10.2.12 (495–583), so the sibling titles are present but the served page is 10.2.2 (rc 0).
The page id `355862667` occurs 0 times in the capture. Receipt: `receipts/04-s209-title-slug.txt:6-9,27-52`.

**F4 — SPIDER and PRISMA-ScR are rejected-for-now, not taught.** No registry row (`spider` 0, `prisma-scr` 0 in
`SOURCES.md`), no round-82 refetch row (0), no round-82 capture token (0/5), no entry hit (0); the lane's only
SPIDER sentence is the round-29 absent-quote fixture (`ReviewFixtureAbsentEdits.md:40`). Receipt:
`receipts/05-unopened-candidates.txt`.

**F5 — the round-81 seat's description of its own record is contradicted by the record's bytes.** The seat called
F4-5 "reason present, flip empty"; the flip cell is filled (12 words) and
`diff -u item4-pass.md records/r4-07-alt-section.md` prints exactly one changed line, the heading (diff rc 1 =
files differ). At `7e2da96a` the old gate printed the *same* line for the complete record and for the empty-flip
record (`REJECTIONS_OK=0/0`, `CLEAN`, rc 0 each), so the description could not be checked from the gate output; the
checker now fails it (`MISMATCH … bytes=present`, `bad=1`, rc 1) and passes on the r82-built form (rc 0). The K2
firing itself stands (both exited 0); what was wrong is the stated mechanism, and the closure's "eleven K2 records"
(`corpus/lessons/round-81-verifier-spotcheck.md:103`) names it. Receipts: `06-r4-07-description-vs-bytes.txt`,
`07-described-form-check.txt`.

**F6 — the named considerthese proposal is still unimplemented.** "One open Gate-record S-id per daily review"
(2026-11-06): 0 of the twelve remainder ids occur in round-82 material outside one fleet-wide grep artifact whose
single hit is a `mado-shokunin` id; `corpus/lessons/round-82.md` does not exist (rc 2);
`git diff --name-only 142b6f0c b4a41d25 | grep -E 'considerthese|lessons'` prints nothing. Receipt:
`receipts/08-considerthese.txt:12-21`. The 2026-11-06 "keep a proposal→adoption ledger" proposal is **not** open: a
35-row ledger exists (`corpus/evidence/round54/considerthese-ledger.tsv`).

**F7 — assimilation none, re-counted.** `collisions` 111 / `staged-ids` 114 / `reg-ids` 192 / live registry 211
(`receipts/09-collisions.txt:3-10`, rc 0); the collision file's last commit is `3eb4a3ca` (2026-11-04), the same
bytes round 81 counted. No package bytes read, no campaign tool run.

## Known limits

- The captures are trusted as committed bytes matching their fetch rows and were not re-opened live; the C2/K2
  live check belongs to the seat that owns it, and this seat's item names no re-open.
- Whether each located quote grounds the decision row it warrants (C2/K3) was not judged here.
- The S008 anchor drift is logged with line evidence, not corrected: the registry is frozen at the landing.
- The described-form checker is a cell-level test; it does not read the gate's code, and the gate's own
  distinguishing output is what F5 cites for the landed repair.
- The L1's helper `corpus/evidence/round82/mistake-r4-07.txt` is **untracked** and not in the landing commit
  (`git cat-file -e b4a41d25:corpus/evidence/round82/mistake-r4-07.txt` → rc 128, "exists on disk, but not in
  'b4a41d25…'"), so this seat cites `claims.md` §Prefreeze discovery (committed) and its own receipts, never that
  file as evidence.

## Artifact paths

- Deliverable: `.ufo/waves/round-82/w1/R82ScribeLesson/lesson-draft.md`
- This report: `.ufo/waves/round-82/w1/R82ScribeLesson.md`
- Receipts: `.ufo/waves/round-82/w1/R82ScribeLesson/receipts/01-gate-quote-locate.txt`,
  `02-capture-sha-vs-refetch.txt`, `03-registry-diff.txt`, `04-s209-title-slug.txt`,
  `05-unopened-candidates.txt`, `06-r4-07-description-vs-bytes.txt`, `07-described-form-check.txt`,
  `08-considerthese.txt`, `09-collisions.txt`
- Checker: `.ufo/waves/round-82/w1/R82ScribeLesson/check-described-form.py`

VERDICT: R82ScribeLesson C1 n/a — the frozen k2-gate counter and the selftest were not run by this seat; its only gate runs were the r4-07 record pair (landed gate rc 0 on the positive control, rc 1 on the F4-5 form), recorded as mistake evidence, not as the C1 predicate.
VERDICT: R82ScribeLesson C2 n/a — the depth counter was not run by this seat; its Gate section only locates the five rows' quotes in their committed captures (all FOUND, hashes MATCH), which is not the frozen predicate.
