# Round 54 verifier spot-check — chousa

author: hyaku closure (non-author integrator, @m_opus)
date: 2026-10-27
scope: chousa round 54; BASE `c49ffc6ce1c3de87c1dfa96856239ed7274bf07b` → TIP `25abbe82b9f2b7c6e24580ac3f028611ba21f01f` (== `master` == `origin/master`, ahead=0); FREEZE `5a1a20630d8176a816a60bb43b0d0e7ee2db19a0`; report `.ufo/reports/round-54/chousa.md`.
Non-author: the hyaku closure judge wrote this file, not the lane. No lane gate or frozen counter was executed (PROTOCOL §Gate standard, Closure consequence). Gate claims were verified through committed evidence. The plain counts and the tool's behaviour were re-measured by the judge, over a `git archive` export of TIP into `/fast/scratch/hyaku/closure-chousa-r54` (removed after the run). The independent oracle was LibreOffice `--convert-to txt`, run by the judge.

Driver digest (copied from the mutable `.ufo/watchdog.log`):
`2026-10-26T22:15:22-03:00 launch chousa round=54 pgid=540574 driver=hyaku-inline attempt=1` · `2026-10-26T23:55:10-03:00 complete chousa round=54; hyaku-inline attempt=1`.

## 1. Step-1 conformance

- **Report.** Commit `86023b972ef9c975e21ad6cb78c6c050aa25c625` (2026-10-26 23:50:07 -0300), author `chousa-shokunin <chousa@shokunin.local>`. That is after the lane tip (23:49:22) and before the driver's `complete` (23:55:10). It has a `## SHONEN` heading with four `[~]`+pointer lines, one per box. It is a real report (work, landed-changes table with hashes, before→after with commands, Sources & frontier, trend verdicts), not a marker. CONFORM.
- **Prompt.** `.ufo/prompts/chousa-round-54.md` (628 lines) was committed by the lane identity (`ce1af7e5…`). It carries §1 MISSION/AXES binding, §2 1–3 claims plus the lowest-axis rule, §2b frontier step, §3 L2 floor, §4 report contract (path, SHONEN heading, hash citation, commit before report), §5 commit-then-push, push scope and the L0 channel, plus the hyaku addendum §6 and scratch discipline §7. CONFORM.
- **Cited commits.** All eight exist (`git cat-file -t` → `commit`), and `git merge-base --is-ancestor <h> master` holds for each: c49ffc6c, 5a1a2063, 8a7d0f13, 9caf8fc6, 6af11e9f, 447cf7ed, 178667dc, 25abbe82. Every round commit is authored by `chousa-shokunin`.
- **Pushed.** `jj-lane.sh state` → `branch=master local=remote=25abbe82… ahead=0 behind=0 head=detached tracked=1 untracked=25`. `git ls-remote origin refs/heads/master` → `25abbe82…`.
- **Leftovers (defect, status-neutral).** `git status --porcelain` shows uncommitted W2 output:
  - modified: ` M .ufo/waves/round-54/w2/R54W2DraftScorecard.md`;
  - untracked: `?? .ufo/waves/round-54/w2-results.json` (written 00:14, after the report) and 24 `w2/R54W2*.md` seat reports.
  - The report says it was filed before W2 WAVE-DONE under the request-budget wrap. It takes no W2 credit. The W2 bytes are round work that is still uncommitted, and W2 is not integrated (see §6).
- **SHONEN.md.** Unchanged BASE..TIP (`git diff --numstat` prints nothing). No `[x]` written.

## 2. Claim re-checks

### R54-C1 — operability (capability: OLE Word 97+ `.doc` text form) — improved (re-measured + evidence-verified)

**Evidence-verified (gate):**

- The frozen counters are intact. `git diff FREEZE TIP -- c1-count.py c2-count.py claims.md` is empty, and the sha256 at FREEZE equals the sha256 at TIP (`633430a4…`, `0b836197…`). No commit after the freeze touches `claims.md`.
- Tool revisions of `tools/capture-text.py` (sha256):

  | revision | sha256 |
  |---|---|
  | base | `6902db6a…` |
  | candidate 8a7d0f13 | `fd0ed3f5…` |
  | 6af11e9f | `e7e381b6…` |
  | 447cf7ed | `2c0140bc…` |
  | TIP | `2c0140bc…` |

  The TIP hash equals the `tool-rev:` header of `measure-after.txt`.
- `controls/c1-before.txt`: the base tool (sha `6902db6a…`) prints `LEGS=1/6 C1=FAIL` ×4 (three unseeded runs and seed 7).
- `controls/c1-controls.txt`: const 0/6, naive 0/6, refuseall 1/6, shell 1/6, all `C1=FAIL`.
- `measure-after.txt`: `LEGS=6/6 C1=PASS` ×4, `SUPPLEMENT_LEGS=3/3` ×4, `TRACKED_DELETION=PASS`.
- `controls/c1-forge.txt`: the forge passes the frozen counter 6/6 ×2 and fails the supplement (0/3); the four controls also score 0/3. The report states all of this.

**Re-measured by the judge (tool run over committed bytes; this is not the gate):**

- **Base vs landed on the five pinned captures.** The base tool exits `rc=2` on all five (`REFUSED not a zip`; for b539a802 it reports a theme part that is not WordprocessingML). The landed tool exits `rc=0` with 0 U+FFFD on all five. Twin 54fe0734 and 74ced3e9 give identical output.
- **Independent oracle.** I applied the frozen REAL rule myself to my own LibreOffice text export: every line of ≥8 non-space characters must occur, directly or after one leading label of ≤12 characters, in the whitespace-free text form, with a length ratio of 0.90–1.10. Result: 0 missing lines on all four distinct documents (386, 14, 248 and 344 lines), with ratios 1.000, 0.990, 0.999 and 0.972.
- **Pinned quotes.** Both pinned quotes give `LOCATED count=1` (offsets 12795 and 4678).
- **Refusals.** A truncated `.doc` gives `REFUSED ole-malformed` (rc 2). An `.xls` made with soffice gives `REFUSED ole-not-word` (rc 2). Random bytes are refused (rc 2). There is no Traceback.
- **Tracked deletions (E2).** On `corpus/fixtures/capture-text-ole/tracked.doc` the candidate prints `DELETEDTEXT` and `删除的中文`. The landed tool drops both, and its output equals the `.docx` twin's.
- **Unchanged pinned captures.** The candidate and landed text forms of the five pinned captures are byte-identical, which confirms the report's claim.
- **No helper program.** The tool imports only stdlib modules (struct, zipfile, zlib, ET, …) and contains no subprocess, ctypes or soffice call (grep).

**Verdict.** The capability is real. The lane's own words are "improved narrowly", and it discloses that the frozen counter is forgeable (E1, RW-1). The uncommitted W2 seat `R54W2SentFinal` also reports that the supplement can be forged: a 20-line tool that never opens the `.doc` scores 3/3. That weakens the instrument, not the tool, and my independent oracle run separates the two.

### R54-C2 — depth (sourced: GB/T 7714-2025 by document) — improved (re-measured)

- **Entries.** `ENTRIES=2/2`: `source-type-taxonomy-r36.md` and `-r37.md` are absent at BASE and present at TIP. Their `source:` lines cite only S121, S122 and S123, all bound, so `REF_ID_UNBOUND=0`. Neither entry cites S101 or S130.
- **Rows.** `BOUND=3/3`: rows go 120 → 123 (CORPUS census grep). The `SOURCES.md` diff is +3/−0, append-only. S121–S123 have NF=13 and are `mined`, opened 2026-10-26, recheck `180d`, tiers A/A/B, with `used-by` paths that resolve. None of the three URL keys occurs in BASE knowledge or SOURCES (`git grep` → 0). The novelty sweep `git grep -e 'ISO 690:2021' -e 文献载体标识 BASE -- corpus/knowledge` exits 1.
- **Quotes.** `spans.tsv` has 33 rows with 7 uniform columns (S121=6, S122=6, S123=21). All 33 span files exist. Each quote occurs in its span, its entry and the lesson (33/33, NFKC-tolerant) and is ≤25 words and ≤160 characters (33/33).
- **Captures.** `capture_sha256` resolves to a cache file for all three ids. Every quote occurs **exactly once** in its capture (33/33). Every span file is the exact capture window starting at the `offset` column (33/33; the column is the span-window start, 80 characters before the quote, read with newline normalisation).
- **Anchors.** `ANCHOR_BOUND=3/3`: the anchor offsets re-derive on the normalised `.txt` forms. S121 has char 1029, 1048 and 1797. S122 has char 15188. S123 has char 5602 and 11542.
- **Quarantine.** `QUARANTINE_VERDICTS=3/3`, re-derived:
  - S080: the joined string occurs 0 times and `标准号：` 0 times; the cells sit at 1029 and 1048.
  - S088: the carrier rows are separate lines (59025, 59201).
  - S096: the `GB/T 7714，采用` piece occurs 0 times in the defined OLE form (27,012 characters, 0 U+FFFD), and `参考文献格式，参照ISO 690` occurs at 25123.
  - All three verdicts are `absent-as-written`. I agree.
- **Limit.** Entailment is not counted, and the lane discloses this (`R54CritForgeC2`). See §6 item 4 for one overstated sentence that uncommitted W2 found.

### Calibration (axis verdict, not a declared claim) — re-measured

- **Anchored corrections.** There are nine `correction:` lines in SCORECARD "Round 54 pointer corrections". Each anchor occurs exactly once in its target, at exactly the stated new offset (9/9): 16, 151, 492, 11972, 12007, 12795, 12963, 14049, 25123.
- **Dumps.** The committed `S100-text-form.txt` and `S101-text-form.txt` are byte-identical to my own runs of the landed tool on b539a802 and 6dc68fd6.

### Axis-harm check

`git diff --numstat BASE TIP`:

| file | added | removed |
|---|---|---|
| SCORECARD.md | 44 | 0 |
| LOG.md | 10 | 0 |
| SKILL.md | 3 | 0 |
| QUALITY.md | 8 | 0 |
| README.md | 26 | 0 |
| SOURCES.md | 3 | 0 |
| tools/capture-text.py | 300 | 4 |

The four removed lines in `tools/capture-text.py` are the docstring and the `not a zip` refusal, which is replaced by signature dispatch; the OOXML path is unchanged. No axis row decreased, and the numeric operability scale is left at 3/10 as before. **No axis harmed.**

## 3. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| operability | improved | C1: an independent oracle and re-measured refusals and tracked deletions; the frozen-counter receipts verified (narrow: the instrument is forgeable) |
| depth | improved | C2 re-measured: 33/33 quotes unique in their captures, spans exact, anchors 3/3 |
| coverage | improved | three documents absent at BASE are now bound; a new capture form (OLE `.doc`) is read |
| calibration | improved | 9/9 anchored corrections exact; QUALITY 97–100 appended; round-53 W2 non-dispatch recorded; E1 forgeability disclosed |
| freshness | unchanged | no fetch; L0 `8d77e6c1` open |
| adjacency | unchanged | contested scope not absorbed; the S130 grey-literature entry stays refused |

## 4. Discernment spot-check (non-author re-open; cache `shokuknow/.ufo/waves/corpus-expansion-1/.qcache`, no fetch)

| item | decision | re-opened source | verdict | reason |
|---|---|---|---|---|
| `source-type-taxonomy-r36.md` (S121) | admit, narrowed | `adf6ba934e813b2c326fa150.txt`, 3,591 chars normalised: `本标准非等效采用ISO国际标准：ISO 690:2021。` occurs once at 1797 | **agree** | located quote is unique at the stated offset |
| r36 (S122 notice) | admit, narrowed | `b9ca2a4fdf9455867534f144.txt`, 22,007 chars: `…本系统不提供文本阅读服务` once at 15188 | **agree** | the subject is `本系统`, the portal's own service, so narrowing to the notice is correct. W2 `R54W2CritEntailSta`'s latent i18n string `该标准暂无全文，请等待更新` (once at 1712) is real; it overstates the r36 phrase "belongs to no line here" and does not falsify the admission |
| `source-type-taxonomy-r37.md` (S123) | admit, narrowed | `0f33243fd7ac2fe88b85c1ba.txt`, 83,061 chars: `本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。` once at 5602; 7.3 quote once at 11542 | **agree** | scope-clause quote unique; the 7.3 re-cut at the line break is warranted |
| S101 leg of the r37 draft | reject (this round) | `SOURCES.md` S101 row byte-identical to BASE, `used-by` = `corpus/knowledge/citation-count-semantics-r37.md`; `S101` absent from both new entries; `build-spans.py` has no OLE form (its SKILL row says so) | **agree** | the draft anchors used the undefined UTF-16LE decode; refusing until the span builder reads through the tool is calibrated, and the flip condition can be checked |
| grey-literature-r40 (S130) | reject (still) | landed tool on `bdff491a….raw`: `是否检索灰色文献` `LOCATED count=1 offset=4678`, 0 U+FFFD; `grep -rl S130 corpus/knowledge` → none | **agree** | the text-form blocker is gone, but the entry is outside the frozen document set and has no located quote set; the refusal is honest |
| S122 row, `## Gate` quote | new SOURCES row | the quote `该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务` is one whitespace word (≤25), at char 15188 | **agree** | verbatim, unique, at the recorded location |
| quarantine S096 | `absent-as-written` | defined OLE form 6dc68fd6: the splice piece occurs 0 times; `参考文献格式，参照ISO 690` once at 25123 | **agree** | supersedes round 42's `unverifiable`, on bytes the judge re-derived |

Census, run by the judge: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, `ok`, five pre-existing W04 (S051, S053, S073, S074, S075). This is identical to `census-end.txt`.

## 5. Trend verdicts

- **expansion — improved.** Rows 120 → 123. Three documents absent at BASE are bound to two new entries, all `mined`. A new capture form (OLE `.doc`) is read. The S101 leg and S130 are refused and earn no credit.
- **quality — improved.** All 33 quotes are unique and exact in their captures. Nine undefined-form anchors are re-pointed exactly. The OLE reader was hardened (Prc bound, tracked deletions), and the fix was confirmed against the candidate. No admitted entry was found false. One overstated sentence is routed (§6.4).
- **discernment — improved.** The non-author re-open agrees with the gate on 3 admits, 2 rejects, 1 row quote and 1 quarantine verdict. Each rejection carries a flip condition that can be checked.

## 6. Routed defects (lane fixes next round)

1. **Uncommitted W2 output at the lane tip.** The modified `R54W2DraftScorecard.md`, the untracked `w2-results.json` and 24 W2 seat reports are uncommitted. Commit them with an integration entry, or record why they are left out. This is the second round running in which a wave's runtime output was left on disk (round-53 item 1).
2. **W2 findings not integrated.** Fold the falsifications into errata or corrections, not credit:
   - `R54W2SentFinal`: the supplement can be forged by a tool that never opens the `.doc` (3/3); the REAL leg can echo through the inherited `TMPDIR`; the forge builder leaves pinned captures on SIGKILL; the ledger checker escapes its root; the PDF cross-check passes vacuously.
   - `R54W2CritC1Verdict`: a ctypes delegate bypasses the audit hook, so QUALITY 98's "refuses a tool that delegates" is not a measured guarantee.
3. **RW-1, sixth round as of r54.** Both the frozen C1 counter and its supplement can be forged. A future frozen predicate needs an inspection-independent leg, for example held-out documents that are generated outside the tool's reach and carry no oracle sibling.
4. **r36 wording.** "the stronger claim that the text is unavailable belongs to no line here" is overstated. Capture `b9ca2a4f…` carries `'noFullText': '该标准暂无全文，请等待更新'` at char 1712, inside a JS i18n map. Narrow the sentence to the lines the page displays (W2 `R54W2CritEntailSta` I3), and hedge I5 "prescribes".
5. **QUALITY 97 F1.** W2 `R54W2ReviewQuality`: the located offsets listed under the criterion fail its own check for 2/6 phrases. Correct by an appended line.
6. **Lesson Mistakes row 2.** Its "mirror without the two dumps → BAD=6" is wrong; the observed result is `ANCHORED=7/16 UNANCHORED=9 BAD=9` (W2 `R54W2CritMistakes`). Append a correction.
7. **Carried.** The five W04 duplicate-url warnings (S051/S053/S073/S074/S075) are still un-adjudicated.

## 7. Note for the operator

The four SHONEN boxes are `[~]` with resolvable pointers: SKILL round-54 gate rows and QUALITY 97–100, LOG Round 54 with `measure-after.txt`, runnable counter and check commands, and PROVINCE fit with refusal records. They look fully checkable by a non-author. Promotion review is operator-owned.
