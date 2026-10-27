# R54W2DraftLog — LOG.md round-54 entry draft

seat: R54W2DraftLog (scribe, round 54 wave 2, leaf — no subagent dispatch)
lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`
tip read: `178667dc2c9d1656e864abfdc251c68757428613`; base `c49ffc6ce1c3de87c1dfa96856239ed7274bf07b`; freeze `5a1a20630d8176a816a60bb43b0d0e7ee2db19a0`; C1 candidate `8a7d0f137a352000d78704ba5695ded8857104fe`
date: 2026-10-26

Scope: draft the `## Round 54` LOG.md entry in the shape of the Round 53 entry. No counter was re-run
(no C1/C2 measurement is claimed here); every number below is read from a receipt, a lane file or a
command in section 2. The only lane write is this report.

## 1. What I read (all opened, not guessed)

- `corpus/evidence/round54/claims.md` (frozen predicate, targets, kill rules, routed items) and
  `claims-erratum.md` E1–E4.
- `LOG.md:1843-1852` (the whole Round 53 entry, in the file to its last line; `LOG.md` is 1852 lines).
- `corpus/lessons/round-53-verifier-spotcheck.md` section 6 (items 1–6) and `corpus/lessons/round-54.md`
  (Mistakes, Spot-check intake, Gate, Quarantine slice, All located quotes, Census, Disclosed changes).
- Receipts: `measure-after.txt`, `c1-after-candidate.txt`, `controls/c1-before.txt`,
  `controls/c1-controls.txt`, `controls/c1-forge.txt`, `controls/c2-before.txt`,
  `controls/c2-controls.txt`, `census-start.txt`, `census-end.txt`.
- `SCORECARD.md:2734` (round-54 plan) and `:2736-2752` (Round 54 pointer corrections, nine `correction:`
  lines); `corpus/QUALITY.md:937-943` (criteria 97–100); `SKILL.md:139-141`; `corpus/README.md:1165-1177`.
- All 44 `.ufo/waves/round-54/w1/*.md` VERDICT blocks (extracted with one Python pass, UTF-8 with a
  `replace` fallback after a `UnicodeDecodeError` on one report).

## 2. Gates (commands run, observed)

```
$ ls corpus/evidence/round54/ corpus/evidence/round54/controls/
18 files, 3 dirs → c1-count.py c2-count.py c1-supplement.py build-spans.py pdf-crosscheck.py
considerthese-ledger.tsv+check.py tracked-deletion-check.py spans.tsv quotes.tsv
measure-after.txt c1-after-candidate.txt census-{start,end}.txt S100-text-form.txt S101-text-form.txt
controls/ → build-c1-controls.py build-c1-forge.py build-c2-controls.py
            c1-before.txt c1-controls.txt c1-forge.txt c2-before.txt c2-controls.txt   (8 entries)

$ git log --oneline c49ffc6ce1c3de87c1dfa96856239ed7274bf07b..HEAD
178667d round-54: W1 reports and results (44 reports; 3 seats cancelled, 2 dead), W1 markers; W2 spec/dispatch (38 seats)
447cf7e round-54: capture-text drops OLE tracked-deletion runs (E2), fixture + check, SKILL rows, erratum, re-measure
6af11e9 round-54: W1 integration — GB/T 7714 entries r36/r37, rows S121-S123, spans, lesson, QUALITY 97-100, SKILL/README rows, S100/S101 anchored corrections, capture-text Prc bound (E2), C1 supplement + forge control (E1), considerthese ledger, pdf crosscheck, after-measurement
9caf8fc round-54: W1 spec/dispatch (49 seats) and section-10 assimilation scratch (ids, collisions, quarantine slice)
8a7d0f1 round-54: C1 candidate — capture-text OLE Word 97+ .doc text form (CFB reader, piece table, field results, ole-* refusals)
5a1a206 round-54: freeze R54-C1 (OLE .doc text form) and R54-C2 (GB/T 7714 theme) with counters, controls, before receipts, census start; inherit round-53 W2 registry

$ python (rows/tier/status per revision, parsing `| S### |` rows of corpus/SOURCES.md)
c49ffc6c  rows 120  tier A 102 B 13 C 5   status mined 96 queued 19 rejected 5
HEAD      rows 123  tier A 104 B 14 C 5   status mined 99 queued 19 rejected 5
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md → 123   (census-end.txt tail)

$ python (w1 results/report diff)
results 49  reports 44  no-report: ['R54ExecNegSweep','R54ExecPdfForm','R54CritSeparable','R54SentCounters','R54ConnSiblings']
$ python (roles, w1-results.json) → scribe 15 executor 14 critic 6 reviewer 5 scout 3 mutation-tester 2 connector 2 sentinel 1 simplifier 1
$ python (roles, w2-spec.json items=38) → executor 14 critic 8 reviewer 5 scribe 4 mutation-tester 2 connector 2 sentinel 1 simplifier 1 scout 1
$ cat .ufo/waves/round-54/w1.ready.dispatched → 2026-10-26T22:40:28 + id map; w2.ready.dispatched → 2026-10-26T23:43:50 + id map
$ ls .ufo/waves/round-54/w2-results.json → No such file or directory

$ grep -n '^source:' corpus/knowledge/source-type-taxonomy-r37.md → 3:source: S123 — … (only line; E3 cut holds)
$ python (row S101 cells) → used-by = corpus/knowledge/citation-count-semantics-r37.md (unchanged)
$ grep -c '^correction: corpus/SOURCES.md:1[01][01] ' SCORECARD.md → 9
$ grep -n '/home/vgpnk' corpus/knowledge/source-type-taxonomy-r3[67].md → r36:6,30 r37:5,58 (host-absolute recheck commands present)
$ grep -c '现行' corpus/evidence/round54/quotes.tsv corpus/lessons/round-54.md → 0 and 0 (cited in r36:35, no span row)
$ sed -n '107,113p' corpus/evidence/round54/build-spans.py → raw_form(): `return b.decode("utf-16le", errors="replace")` for a non-zip .raw
$ python3 tools/capture-text.py /fast/scratch/hyaku/chousa-r54-probe.*/absent.doc
Traceback (most recent call last): … FileNotFoundError: [Errno 2] No such file or directory: '…/absent.doc'   exit=1
$ rm -rf /fast/scratch/hyaku/chousa-r54-probe.*   (the one probe dir removed; no other scratch kept)
```

## 3. Draft — intended path `LOG.md`, append after line 1852

```LOG.md
## Round 54 — a defined OLE `.doc` text form; the PRC citation standard GB/T 7714-2025 by document (2026-10-26)

Evidence that motivated the round: the round-53 closure's routed defects (`corpus/lessons/round-53-verifier-spotcheck.md` section 6 — the uncommitted W2 registry, the W2 that was never dispatched, assertion-only receipts, a mislabelled digest, the five un-adjudicated W04 warnings, the forgeable-counter streak RW-1) and the SCORECARD round-54 plan ("a C1 counter with a non-vacuous sample-size guard, generic calendar-invalid inputs and a non-canned held-out REAL leg"; "a defined OLE `.doc` text form or a narrower refusal"; "continue theme C (GB/T 7714 source-type)"). Claims froze at `5a1a20630d8176a816a60bb43b0d0e7ee2db19a0` after their do-nothing controls (`corpus/evidence/round54/claims.md`; `controls/c1-before.txt`, `c1-controls.txt`, `c2-before.txt`, `c2-controls.txt`, `census-start.txt`; the round-53 W2 `swarm-registry.json` committed at the same commit). C1 candidate `8a7d0f137a352000d78704ba5695ded8857104fe`; post-candidate hardening `447cf7e`. No external fetch; L0 `8d77e6c1` open; every source an on-disk capture under the read-only campaign cache.

- **C1 operability (lowest scored axis, 3/10; capability acquisition, plumbing).** `tools/capture-text.py` prints a defined text form for an OLE Word 97+ `.doc` — CFB sector chains, FIB `wIdent`/`nFib`, Clx piece table, cp1252/UTF-16LE pieces, main story CP `0..ccpText`, field results only — and refuses `ole-not-word` / `ole-encrypted` / `ole-malformed`. Frozen counter `python3 corpus/evidence/round54/c1-count.py`: base tool (`6902db6a`) `LEGS=1/6 C1=FAIL` on three unseeded runs and `--seed 7` (`controls/c1-before.txt`) → candidate (`fd0ed3f5`) `LEGS=6/6 C1=PASS` on three unseeded runs and `--seed 7` (`c1-after-candidate.txt`) → landed tool (`2c0140bc`, E2) `LEGS=6/6 C1=PASS` four runs with `REGRESS r52 ['LEGS=9/9'] ['SUPPLEMENT_LEGS=4/4']` (`measure-after.txt`); its post-freeze supplement is `SUPPLEMENT_LEGS=3/3` on four runs (ibid.). Controls CONST 0/6, NAIVE 0/6, REFUSEALL 1/6 (NONWORD), SHELL 1/6 — the audit hook stops its spawn (`controls/c1-controls.txt`). W1 `R54ReviewOleTool` F1 (the Clx walk trusted a signed `cbGrpprl`: a malformed `.doc` hung or exited 1 with a Traceback) and W1 `R54ReviewOleSpec`'s tracked-deletion finding were fixed after the candidate (`Prc GrpPrl` bound; CHPX FKP runs carrying `sprmCFRMarkDel` dropped; fixture `corpus/fixtures/capture-text-ole/tracked.doc`, `tracked-deletion-check.py` PASS where the candidate FAILs); the five pinned captures' text forms are byte-identical before and after both changes, and no frozen leg reaches the Clx walk (E2).
- **W1 forged the frozen counter (RW-1, sixth round).** W1 `R54CritForgeC1` passed `LEGS=6/6` on four runs with a tool that never parses the compound file — it read the sibling HTML the counter leaves beside each generated `.doc`, returned LibreOffice exports canned by the pinned sha256 prefixes, and keyed refusals on byte markers. The L1 rebuilt that shape as `controls/build-c1-forge.py` and wrote the post-freeze `c1-supplement.py` (ISOLATED, RESAVE, HELDOUT; every run under the frozen audit hook); receipt `controls/c1-forge.txt`: the forge still scores `LEGS=6/6` on the frozen counter and `SUPPLEMENT_LEGS=0/3`, while CONST, NAIVE, REFUSEALL and SHELL also score 0/3. The frozen counter remains forgeable; C1's verdict is judged on it and capped accordingly (E1).
- **C2 depth (sourced, ground; theme C, the PRC citation standard).** Entries `corpus/knowledge/source-type-taxonomy-r36.md` (S121 the SAMR detail record, S122 the openstd notice) and `source-type-taxonomy-r37.md` (S123 the 集美大学学报 journal office's PDF reproduction), rows S121–S123 new since the base, 33 located quotes in `spans.tsv`/`quotes.tsv`. `python3 corpus/evidence/round54/c2-count.py`: `ENTRIES=0/2 BOUND=0/3 SUBSTANCE=FAIL QUARANTINE_VERDICTS=0/3 C2=FAIL` (`controls/c2-before.txt`) → `ENTRIES=2/2 BOUND=3/3 REFUSED=0 QUOTE_ROWS=33 ON_BOUND=33/33 SPAN_IDS=3/3 QUOTES_IN_SPAN=33/33 QUOTES_IN_LESSON=33/33 CAPTURE_BOUND=33/33 SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=2/2 QUARANTINE_VERDICTS=3/3 (S080,S088,S096) C2=PASS`, `--lane-only` likewise (`measure-after.txt`). Controls: the staged entries copied unchanged `REF_ID_UNBOUND=6 HELD_BAD=1 BOUND=0/3`; the base adopter's mechanical adoption `BOUND=3/3 REF_ID_UNBOUND=3 HELD_BAD=1 ANCHOR_BOUND=0/3`, both `C2=FAIL` (`controls/c2-controls.txt`) — binding alone is mechanical, the claim's substance is the located quotes, spans, anchors and inference ground. W1 `R54CritForgeC2` falsified the ordinary counter as a semantic oracle; W1 `R54CritTheme` granted depth only for the scope/version/provenance findings, not the code list alone; `R54GroundSamrA/B` and `R54GroundJmuA/B` supplied the identity, adoption and operative-text ground.
- **The S101 leg cut (E3) and the NFKC fold (E4).** The W1 r37 draft cited the held S101 with four quotes anchored in the raw UTF-16LE decode — the form `## Mistakes` row 2 finds undefined. The leg was cut: r37 carries only `source: S123` and S101's `used-by` is unchanged at `corpus/knowledge/citation-count-semantics-r37.md`; the frozen predicate makes S101 optional, so this is a narrowing inside the rule. The S123 PDF quotes are cross-checked against a pypdf extraction under NFKC — `pdf-crosscheck.py` → `PDF_QUOTES=21 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14`, the 14 width-only — while the frozen span builder still reads a non-zip `.raw` as UTF-16LE.
- **Corrections and calibration.** Nine anchored `correction:` lines (S100 ×3, S101 ×6) re-point the round-49 Registry anchors from the undefined whole-file UTF-16LE decode into the defined OLE form, against the dumps `corpus/evidence/round54/S100-text-form.txt` / `S101-text-form.txt` (`SCORECARD.md` "Round 54 pointer corrections"); W1 `R54DraftS101Reanchor` measured all six S101 offsets dead in the new form (one out of range) and `ANCHORED=13/13` on a mirror once the dump lands, `BAD=6` without it. QUALITY 97–100: a binary capture's text form is a defined reading and an anchor names the form it indexes; a counting-time oracle with refusal of delegators; a wave is dispatched only with its marker or results; a held row's `used-by` moves old→new. `SKILL.md` Gates: the round-52 `capture-text` row superseded by name, `chousa round-54 counters and checks` and `chousa round-54 post-freeze checks` added. `corpus/README.md` "Round54 coverage and frontier". `considerthese/2026-10-26.md` proposal 1 implemented as `considerthese-ledger.tsv` + `considerthese-ledger-check.py` (`BAD=0`, rc 0 at the integrated tree, four mutants failing; W1 `R54ScoutConsiderthese`).
- **Frontier / census.** Rows 120 → 123 (tier A 102 → 104, B 13 → 14, C 5; `mined` 96 → 99, `queued` 19, `rejected` 5); census exit 0 at start and end with the same five pre-existing W04 (S051 S053 S073 S074 S075); no existing row touched. Coverage credit per document: S121 and S123 are new ground, S122 only for its own no-text notice; the held S101 earns none.
- **Waves.** W1 dispatched 49 seats (marker `w1.ready.dispatched` 2026-10-26T22:40:28; scribe 15, executor 14, critic 6, reviewer 5, scout 3, mutation-tester 2, connector 2, sentinel 1, simplifier 1); 44 seat reports, and the integration commit records 3 seats cancelled and 2 dead — the five without a report are `R54ExecNegSweep`, `R54ExecPdfForm`, `R54CritSeparable`, `R54SentCounters`, `R54ConnSiblings` (prose fragments in the results file, no structured output), and no per-seat cancelled/dead classification is recorded. W2 dispatched 38 seats (marker `w2.ready.dispatched` 2026-10-26T23:43:50; executor 14, critic 8, reviewer 5, scribe 4, mutation-tester 2, connector 2, sentinel 1, simplifier 1, scout 1); at this draft `w2-results.json` does not exist, so no W2 outcome is claimed. The L1 held the planner seat.
- **Unfixed seat findings** (reported, no predicate, target, counter or control changed). Frozen C1 counter: the REAL leg accepts capped table-stream junk and appended non-main-story text, both 6/6 (`R54CritOracle`), fails a document with a footnote reference mark and a ≥40-item numbered list at ratio 0.898 (`R54ExecOleCorpus`), and its MALFORMED leg never reaches the Clx walk (`R54ReviewOleTool` F2); fObfuscated-only refusal, anchor uniqueness and audit-hook no-spawn are not fully measured (`R54ReviewC1Counter`); 7 of 16 single-point mutants survive (m05 m06 m07 m09 m12 m13 m14, `R54MutOle`); the REGRESS leg runs outside the audit hook, writes a `.pyc` into the lane, and the default `--tool` moved mid-wave (`R54DraftQuality` 2, `R54ExecSeedRuns`). Frozen C2 counter: it passes boilerplate/TOC quotes, duplicate rows, opposite inference, a wrong held anchor and a two-of-three refusal (`R54CritForgeC2`); the held leg is falsified twice — a HIT URL named outside a `source:` line passes and a stray `S101` token is never unbound — with a REFUSED row-shape hole (`R54ReviewC2Counter`); the held guard `r[0] in base_ids` is unfalsifiable and the bound `used-by == citing` half is not measured against the entries' own citations (`R54MutC2` M3, finding 2). Tool: a missing input path still exits 1 with a `FileNotFoundError` traceback where the base refused exit 2 (`R54ExecHistCounters` F2, reproduced at the tip), the non-zip refusal wording changed over 2,583 files (F1), hidden text is still emitted and the U+2011 flattening, U+00AD dropping and cell/row-boundary erasure are undeclared (`R54ReviewOleSpec`; E2 declares only tracked deletion), `build-spans.py` still slices a non-zip `.raw` as UTF-16LE so two text forms exist for one document (F3, `R54DraftQuality` 4), and the two inert lines `R54SimplifyOle` found were kept. Entries/evidence: the S100/S101 `anchor` cells still print undefined-form offsets with the repair only in appended `correction:` lines, S123's anchor cell is misdescribed, the layout-only `图书 … Ｍ` quote is in the lesson, `现行` is asserted without a span, and both entries' `recheck:` commands are host-absolute (`R54ReviewProvince`, six defects; its NFKC-fold item is now recorded in E4); `corpus/lessons/round-49.md:158` still records a two-entry S101 `used-by` the Registry cell does not (`R54DraftQuality` 3); the round-52 SKILL row's QUALITY 90 narrative still describes the pre-OLE behaviour (`R54ExecHistCounters` F4). Unlanded: the package amendment `citation-version-binding-r36.md`, S130's second flip half plus a span builder that reads the defined OLE form (`R54ExecS130Probe`), the SAMR round-44 flip unmet as written on S121 and staged S085's `used-by` naming an entry that refuses the record (`R54DraftReadme`, `R54DraftRows`), two last-match-wins/id-collision hazards in the quarantine slice (`R54ExecQuarantineRest`).
- **Tooling.** No system tool installed, upgraded or written; `pypdf` was invoked ephemerally (`uv run --quiet --with pypdf`) for the independent PDF extraction as in round 53; LibreOffice 26.8.1.1 is the counters' counting-time oracle under a private profile. L0 `8d77e6c1` remains open.
```

## 4. Draft-level findings for the L1 (things the entry must not overstate)

1. **W1 accounting is five seats, two counts.** `w1-results.json` has 49 entries but 44 reports; the five
   without a report carry pasted prose fragments, not structured output. The commit message supplies the
   counts (3 cancelled, 2 dead) but no per-seat map; the draft names the five and says the classification
   is unrecorded rather than guessing which is which.
2. **QUALITY 99's own trigger has since cleared.** `R54DraftQuality` measured `w1.ready.partial` (43 ids)
   and no `w1.ready.dispatched` at 22:38:19. Both markers now exist (W1 22:40:28, W2 23:43:50), so the
   entry may say W1 dispatched — with the marker date, not the dispatch file alone.
3. **`R54ReviewProvince`'s six defects are not all still open.** Its NFKC-fold item is what E4 records;
   the draft lists the other five and names E4, so the entry does not contradict the erratum. Three of
   the five I re-observed myself (host-absolute recheck commands, `现行` without a span, the layout-only
   `图书 … Ｍ` row); the misdescribed S123 anchor cell is attributed to the seat, not upgraded.
4. **Two `used-by` records disagree.** `corpus/lessons/round-49.md:158` lists two entries for S101 while
   `corpus/SOURCES.md:111` lists only `citation-count-semantics-r37.md`; criterion 100's "old" value must
   be the row's cell, not the lesson's copy (W1 `R54DraftQuality` 3, verified).
5. **E2 did not close the traceback class.** The landed tool still exits 1 with a `FileNotFoundError`
   traceback on a missing path (reproduced at the tip); E2 bounded only the `Prc` length and dropped
   tracked-deletion runs. The draft keeps that under unfixed findings.
6. **Two tool shas belong in the entry.** The candidate receipt names `fd0ed3f5` and the landed
   after-measurement names `2c0140bc`; the draft names both so the C1 numbers cannot be read as one run's.

## 5. Touched surfaces

- Written: this report only.
- Read: lane files listed in section 1 and the two wave directories.
- Scratch: one `mktemp -d` probe dir under `/fast/scratch/hyaku/chousa-r54-probe.*`, removed; nothing
  kept under `/fast/scratch/hyaku/chousa-r54/<seat>/` was needed (no fixtures, no counters run).
- No git/jj command that mutates, no lane file, no index, no sibling lane, no fleet-root tracked file,
  no PATH directory, no install or upgrade.

## 6. Out of scope

- Adjudicating C1/C2 or any Gate/quarantine verdict; editing `LOG.md`, `SCORECARD.md`, the lesson, the
  counters or the entries; running any counter or check for a fresh measurement; claiming any W2 outcome.

VERDICT: attacked the round-54 LOG entry — its motivating evidence, freeze/candidate commits, per-change evidence paths, census 120→123, the W1 forge and supplement, the S101 cut and the unfixed seat-finding ledger — against the receipts, the commit files, the 44 W1 VERDICT blocks and four live probes; the draft survived as a draft (nine bullets, every number receipt-backed, no unfixed finding upgraded to fixed), and three draft-level corrections were found and applied (the W1 3-cancelled/2-dead mapping is unrecorded; the NFKC item is E4, not open; E2 left the missing-path traceback in place).
