# R54DraftSkillGates — SKILL.md `## Gates` rows for round 54

seat: `R54DraftSkillGates` (scribe/leaf, no subagent dispatch) · date 2026-10-26
deliverable: the two complete table rows, for the L1 to integrate into
`/home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md` `## Gates` (table rows end at line 138, the
`chousa round-53 post-freeze checks` row; the prose head `correction: SKILL.md:132` starts at line 140).

## Behavior

Read the r52 `capture-text` row (line 134) and the r53 counters row (line 137) in full, then every round-54
entry point the row must describe: `corpus/evidence/round54/{c1-count.py,c2-count.py,build-spans.py}`,
`corpus/evidence/round54/controls/{build-c1-controls.py,build-c2-controls.py}`, `tools/capture-text.py`, and the
frozen `corpus/evidence/round54/claims.md`. No production file was written; the lane was read only.

Registry state before (`python3 corpus/evidence/round47/c2-count.py --list`, exit 1):

```
UNREGISTERED_PATH corpus/evidence/round54/build-spans.py
UNREGISTERED_PATH corpus/evidence/round54/c1-count.py
UNREGISTERED_PATH corpus/evidence/round54/c2-count.py
ENTRY_POINTS=142 (abc=110 dependence=+10 check_named=+22)
FLOOR=92
GATES_ROWS=61
REGISTERED=139/142
UNREGISTERED=3
DANGLING=0
MISMATCHES=3
C2=FAIL
```

The three unregistered entry points are exactly the round-54 ones the drafted `chousa round-54 counters and
checks` row names in its `entry` cell — integration closes MISMATCHES 3 → 0.

## Gate evidence (observed, not inferred)

Row shapes and the registration rule were exercised end to end, not asserted. A scratch mirror
(`git -C LANE archive HEAD | tar -x -C mirror`, 240 MB, no `.git`; the counter uses no git and no subprocess)
had the two rows spliced after line 138; then:

```
$ python3 mirror/corpus/evidence/round47/c2-count.py --root mirror
ENTRY_POINTS=142 (abc=110 dependence=+10 check_named=+22)
FLOOR=92
GATES_ROWS=63
REGISTERED=142/142
UNREGISTERED=0
DANGLING=0
MISMATCHES=0
C2=PASS
counter-exit=0
```

`diff <(sed '139,140d' mirror/SKILL.md) LANE/SKILL.md` → **0 lines**: the mirror differs from the lane only by
the two added rows. Each row splits into exactly 8 cells under the counter's own `CELL_SPLIT`
(`(?<!\\)\|`) and its `verdict map` cell matches the counter's `EXIT_CODE` rule
(`8 ['`capture-text` (OLE `.'] exit-in-verdict= True` / `8 ['`chousa round-54 count'] exit-in-verdict= True`).

Usage exits, observed on the lane files with `TMPDIR` in scratch:

```
$ python3 corpus/evidence/round54/c1-count.py --per-leg 1
usage: --per-leg must be at least 2 (sample-size guard)          c1-per-leg1 exit=2
$ python3 corpus/evidence/round54/c2-count.py --nope
c2-count.py: error: unrecognized arguments: --nope               c2-badopt exit=2
$ python3 corpus/evidence/round54/build-spans.py --cache /nonexistent-cache
build-spans: no capture cache /nonexistent-cache                 spans-nocache exit=2
$ python3 corpus/evidence/round54/controls/build-c1-controls.py
IndexError: list index out of range                              c1ctl-noarg exit=1
```

`python3 corpus/evidence/round29/prose-check.py rows.md` → `digit-glued tokens: 0 custody vocabulary: 0
TOTAL hits=0 files=1`, exit 0 (the first draft said `cp1252` and scored 1 hit; reworded to `Windows-1252`).

Pins are copied from `corpus/evidence/round54/c1-count.py:56-66` (`REAL`, `PINNED_QUOTES`), from
`c1-count.py:313-321` (`per_leg` guard, `soffice` guard, leg order), `c2-count.py:63-75` (`BASE_REV`, entries,
URLs, `HELD`, `MIN_*`) and `build-spans.py:1-48` (this round's form order, and the explicit statement that a
non-zip `.raw` keeps the round-48 UTF-16LE decoding). The candidate identity was re-derived here:
`sha256sum tools/capture-text.py` → `fd0ed3f58565b781ab8eedaad5d229976e150bdd8e391a2b0cacd0a0825fcd89`, equal to
the `tool=` line of `c1-after-candidate.txt`; `git log --oneline -4 -- tools/capture-text.py` →
`8a7d0f1 round-54: C1 candidate — capture-text OLE Word 97+ .doc text form …`.

## Rows to integrate

```SKILL.md
| `capture-text` (OLE `.doc`, round 54; supersedes the round-52 row `capture-text` (r52 C1; the OOXML `.docx` text form for claim-vs-source checks) by name) | tool | `python3 tools/capture-text.py RAW` (text form on stdout, UTF-8; dispatch on the signature: `PK\x03\x04` a zip/OOXML, `D0CF11E0A1B11AE1` an OLE compound file) · `python3 tools/capture-text.py RAW --locate QUOTE` (`LOCATED count=<n> offset=<o or -1>`, offsets are code-point indices into the text form). OOXML rule (unchanged from r52): main part = the `_rels/.rels` relationship target whose Type ends in `/officeDocument`; `w:t` text, run-level `w:tab`/`w:br`/`w:cr` as tab/newline/newline, newline at every `w:p` end, nothing from `mc:Fallback`, `w:delText`, `w:instrText` or `w:pPr/w:tabs`. OLE rule (round 54, an in-process CFB reader — no helper program): FAT, mini-FAT and directory chains followed with bounds and loop checks; the `WordDocument` stream's FIB must carry wIdent 0xA5EC and nFib >= 0xC1 (Word 97 or later); the table stream (`1Table`/`0Table` per fWhichTblStm) holds the Clx at fcClx/lcbClx whose PlcPcd maps character positions to WordDocument bytes — a compressed piece is Windows-1252 at fc/2, any other piece UTF-16LE at fc; the text form is the main document story, CP 0 to ccpText, with 0x0D/0x0B/0x0C/0x07 each a newline, 0x09 a tab, 0x1E a `-`, a field emitting only its result (0x13..0x14 code dropped, no separator → nothing) and every other code point below 0x20 dropped. Does NOT read: footnotes, headers/footers, comments or text boxes (outside CP 0..ccpText); pre-Word-97 files (`nFib < 0xC1` is refused `ole-not-word`); macros, embedded objects or an embedded OPC theme part; a `.xlsx`/`.pptx` (root not `w:document`) | `0` text printed, or `--locate` found the quote exactly once · `1` `--locate` found it 0 or 2+ times · `2` refused — a stderr line starting `REFUSED ole-not-word` (no `WordDocument` stream, or a stream that is not a Word 97+ FIB), `REFUSED ole-encrypted` (FIB fEncrypted or fObfuscated set), `REFUSED ole-malformed` (a sector, chain, directory entry, Clx or piece outside its stream or file, a cycle, a missing table stream), each with nothing on stdout and no `Traceback` — or neither a zip nor an OLE file, no officeDocument relationship, a missing or unparsable main part, a root that is not `w:document`, a target outside the package root, a part inflating past 256 MiB, out of memory, or usage (incl. an empty `--locate`) | `python3 corpus/evidence/round54/c1-count.py` (legs GEN, NONWORD, ENCRYPTED, MALFORMED generated at counting time from fresh random text, REAL against a LibreOffice oracle made at counting time, REGRESS = round-52 `LEGS=9/9` + `SUPPLEMENT_LEGS=4/4`; every tool run under an audit hook that exits 97 on spawn/exec/fork/socket). Candidate commit `8a7d0f1`, tool sha256 `fd0ed3f58565b781ab8eedaad5d229976e150bdd8e391a2b0cacd0a0825fcd89`: `LEGS=6/6 C1=PASS` exit 0 on three unseeded runs and `--seed 7` (`corpus/evidence/round54/c1-after-candidate.txt`); the base tool: `LEGS=1/6` (REGRESS only) exit 1 (`controls/c1-before.txt`) | five pinned campaign cache captures, key → sha256[:20]: `54fe0734c01f699e735b4b0a` and its byte twin `74ced3e9311594a8cc3f1f42` → `d341c133e37d65f02f8f` (one document), `6dc68fd6b32ce9c8dfcebce8` → `6063a3aff7a4081e93a6`, `b539a80218080da56a75b624` → `46d1866ce9afd51682e7`, `bdff491a75c6abeda1d9c01d` → `ac0fad62ed9a11fa3bd1`; two pinned quotes, `本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中规定的作者-出版年制。` (`6dc68fd6…`) and `是否检索灰色文献` (`bdff491a…`), each located exactly once; the REAL leg and generation need `soffice` (absent → `ENV_CHANGED soffice not found`, exit 2) and the oracle is `txt:Text (encoded):UTF8` under a private profile in the work dir | read-only; stdout only; no network; its own scratch under `--work`/`$TMPDIR` | chousa |
| `chousa round-54 counters and checks` | gate | `python3 corpus/evidence/round54/c1-count.py [--tool PATH] [--seed N] [--per-leg K] [--work DIR]` (scratch under `--work` or a `TMPDIR` mkdtemp, removed on exit; generated documents, spreadsheet, encrypted and malformed files built per seed) · `python3 corpus/evidence/round54/c2-count.py [--root LANE] [--lane-only]` · `python3 corpus/evidence/round54/build-spans.py [--root LANE] [--cache DIR] [--check]` (its own `.docx` reader, and for a non-zip `.raw` the plain UTF-16LE decoding of round 48 — it does NOT use the round-54 OLE text form) · controls `python3 corpus/evidence/round54/controls/build-c1-controls.py OUTDIR` (writes CONST, NAIVE, REFUSEALL, SHELL and prints their names), `python3 corpus/evidence/round54/controls/build-c2-controls.py` (STAGED and TOOLED scratch roots under `$TMPDIR`) | C1 exit `0` only with `LEGS=6/6` (`GEN`, `NONWORD`, `ENCRYPTED`, `MALFORMED`, `REAL`, `REGRESS`) and `C1=PASS`; `1` any leg failed (`C1=FAIL`); `2` env/usage — `--per-leg` below 2 prints `usage: --per-leg must be at least 2 (sample-size guard)`, a missing `soffice` prints `ENV_CHANGED soffice not found`, a moved pin or a missing oracle prints `ENV_CHANGED pinned capture <key> differs` / `ENV_CHANGED soffice wrote no oracle for <key>`. C2 exit `0` only with `C2=PASS` (`ENTRIES=2/2` min 2, `BOUND` >= 2 of 3 with `BOUND+REFUSED=3`, `REF_ID_UNBOUND=0`, `NEW_GROUND=n/n`, `QUOTE_ROWS` n>0 with `ON_BOUND=n/n`, `SPAN_IDS=BOUND` min 3 each, `QUOTES_IN_SPAN`/`QUOTES_IN_ENTRY`/`QUOTES_IN_LESSON`/`QUOTE_SHORT`/`SPAN_CONTEXT` n/n, `CAPTURE_BOUND=n/n` or `skipped` under `--lane-only`, `SUBSTANCE=PASS`, `ANCHOR_BOUND=BOUND`, `INFERENCE_GROUNDED=n/n`, `QUARANTINE_VERDICTS` complete with `QUARANTINE_BLOCKED_ADOPTED=0`); `1` otherwise; `2` `NO_BASE_OR_REGISTER` (the `BASE_REV` registry or the campaign register unreadable) or usage. build-spans exit `0` `SPANS_ROWS=n WRITTEN=n`, or under `--check` `SPANS_ROWS=n STALE=0` writing nothing; `1` `build-spans: refused <reason>` or `SPANS_HEADER_STALE`/`SPANS_ROW_STALE`/`SPANS_FILE_STALE`/`SPANS_ROW_EXTRA`/`SPANS_FILE_ORPHAN`; `2` usage/env (`build-spans: no capture cache <dir>`, `build-spans: no input …/quotes.tsv`, a header that is not `id url quote entry`). build-c1-controls exit `0` after printing the four names (no OUTDIR argument: uncaught `IndexError`, exit 1 — the caller must pass the directory); build-c2-controls exit `0` after printing both blocks, which must both read `C2=FAIL` (it aborts if `git show BASE_REV:corpus/SOURCES.md` or `tools/assimilate-rows.py` fails) | before receipts `controls/c1-before.txt` (base tool `LEGS=1/6`, REGRESS only, exit 1 on three unseeded runs and `--seed 7`), `controls/c1-controls.txt` (`--seed 54`: const `LEGS=0/6`, naive `0/6`, refuseall `1/6`, shell `1/6`, all `C1=FAIL` exit 1), `controls/c2-before.txt` (`ENTRIES=0/2 BOUND=0/3 REF_ID_UNBOUND=0 SUBSTANCE=FAIL C2=FAIL` exit 1), `controls/c2-controls.txt` (STAGED `ENTRIES=2/2 REF_ID_UNBOUND=6 BOUND=0/3 C2=FAIL`; TOOLED `BOUND=3/3 BOUND_IDS=S121,S122,S123 REF_ID_UNBOUND=3 ANCHOR_BOUND=0/3 C2=FAIL`, both exit 1); usage probes: c1 `--per-leg 1` exit 2, c2 `--nope` exit 2, build-spans `--cache /nonexistent-cache` exit 2, build-c1-controls with no argument exit 1 | C1 `REAL` = five cache keys with sha256[:20] prefixes `d341c133e37d65f02f8f` (`54fe0734c01f699e735b4b0a`, byte twin `74ced3e9311594a8cc3f1f42`), `6063a3aff7a4081e93a6` (`6dc68fd6b32ce9c8dfcebce8`), `46d1866ce9afd51682e7` (`b539a80218080da56a75b624`), `ac0fad62ed9a11fa3bd1` (`bdff491a75c6abeda1d9c01d`); `--per-leg` default 3, minimum 2; C1 depends on `soffice --headless` (generation and the REAL oracle, `txt:Text (encoded):UTF8`) and on the pinned round-52 counter and supplement; C2 pins `BASE_REV` `c49ffc6ce1c3de87c1dfa96856239ed7274bf07b`, `OPENED` `2026-10-26`, the campaign `CACHE` and `REGISTER` under `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/`, the three theme document URLs, the held `S101` HIT specification and `MIN_PER_ID=3`; contract `corpus/evidence/round54/claims.md` frozen at `5a1a206`; targets `LEGS=6/6` and `C2=PASS` | C1 and C2 are read-only on the lane and write only their scratch under `--work`/`$TMPDIR`; build-spans writes `corpus/evidence/round54/spans.tsv` and `spans/` and nothing under `--check`; build-c2-controls writes only `tempfile.mkdtemp` roots under `$TMPDIR`; no network | chousa |
```

Optional reciprocal marker, only if the integrator wants the pair symmetric (one precedent exists,
`research-gate round-32 v1 counters`, the only `SUPERSEDED` in the file): append to the r52 `capture-text` row's
pinned-values cell `· SUPERSEDED by the round-54 `capture-text` (OLE `.doc`, round 54) row`. The round-52 and
round-53 row pairs carry no such marker, so leaving it out is consistent too.

## Findings (reported, not patched)

1. The seat spec's proxy usage `controls/build-c1-controls.py [--seed N]` does not exist: the builder takes one
   positional `OUTDIR` and no `--seed` (`build-c1-controls.py:52` `out = pathlib.Path(sys.argv[1])`). `--seed 54`
   belongs to the counter that consumes the controls (`c1-count.py --seed 54`, whose output is
   `controls/c1-controls.txt`). The row documents the real usage.
2. `build-c1-controls.py` without `OUTDIR` dies on an uncaught `IndexError` (exit 1) rather than a usage line.
   Recorded in the verdict cell as a caller obligation; the file is frozen round-54 evidence and was not edited.
3. `build-spans.py` keeps the round-48 UTF-16LE raw form for a non-zip `.raw` (`build-spans.py:8-14`), so a
   `.doc` span is derived from a form the round-54 C1 tool no longer claims. Harmless for the frozen C2 claim
   (S101 is HELD and needs no new span), but any future `.doc` quote must not pass through this builder.
4. `corpus/evidence/round54/c1-after-candidate.txt` heads with `candidate tools/capture-text.py at 9caf8fc6…`
   (the W1 spec commit) although the candidate commit is `8a7d0f1`. I re-derived the evidence: the tree file's
   sha256 equals that receipt's `tool=` line, so the artifact is the one measured; only the commit label is
   stale. The two commits carry the same tool bytes.
5. `prose-check.py` (QUALITY 23) treats `cp1252` as a digit-glued token in prose; the row says `Windows-1252`.
   The check is not enforced on SKILL.md today (baseline 21 hits there), so this is row hygiene, not a
   compliance fix.
6. Row truth beyond mechanics (whether the pins and verdict maps describe the tools faithfully) was checked by
   reading `c1-count.py`, `c2-count.py`, `build-spans.py`, both control builders and `tools/capture-text.py`
   at the listed lines; the counters' own passes are other seats' work this wave.

## Touched surfaces

- lane, read only: `SKILL.md` (lines 76, 134, 135, 137, 138, 140), `tools/capture-text.py`,
  `corpus/evidence/round54/{claims.md,c1-count.py,c2-count.py,build-spans.py,c1-after-candidate.txt}`,
  `corpus/evidence/round54/controls/{build-c1-controls.py,build-c2-controls.py,c1-before.txt,c1-controls.txt,c2-before.txt,c2-controls.txt}`,
  `corpus/evidence/round47/c2-count.py`, `corpus/evidence/round29/prose-check.py`.
- read-only elsewhere: none (`/home/vgpnk/Projects/shokuknow` untouched).
- writes: this report only, plus scratch `/fast/scratch/hyaku/chousa-r54/R54DraftSkillGates/` (removed on exit).
- no git/jj mutation anywhere; no network; no `soffice` run by this seat; no package installed or removed.

## Out of scope

- Running `c1-count.py` / `c2-count.py` to a pass (other wave-1 seats); scoring the r52/r53 rows' truth;
  editing `SKILL.md`, `corpus/lessons/round-54.md`, `claims-erratum.md` or any counter.

VERDICT: built the two round-54 `## Gates` rows — registration end-to-end exercised on a scratch mirror where the three unregistered entry points go `REGISTERED=142/142 UNREGISTERED=0 MISMATCHES=0 C2=PASS` (exit 0, `GATES_ROWS=63`), every exit code and pin grounded in source lines and observed usage probes; the r52 `capture-text` row is superseded by name and no gate regresses.
