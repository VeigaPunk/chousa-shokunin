# R79ReviewB — independent attack on C2 (calibration), round 79

Seat: R79ReviewB (leaf, no subagents). Base `ee70e6df19fe43b1b384166cf5d360c3b99dafe2`.
Lane HEAD observed `b58a02dbc8876dd1ad7647d88ca2c9cb2ae51ff9`. Scratch clone:
`/fast/scratch/hyaku/chousa-r79/R79ReviewB/mirror` (`git clone --shared`, each fixture built by
`drive.py`, `git rev-parse --show-toplevel` asserted before every reset). Scratch deleted at yield.

Frozen counters run from the lane tree, read-only, `python3 -B`, never copied or amended:
- `corpus/evidence/round78/selfcheck.py` sha256 `f5acdd82…9af` (= claims table)
- `corpus/evidence/round79/selfcheck-v2.py` sha256 `b99ccee5…ed2` (= claims table)

Not run: `selfcheck-control.py` (lane control script not reused, per assignment).

Receipts: `.ufo/waves/round-79/w1/R79ReviewB/` — `drive.py` (case builder, sha256 `4fe39a13…7737`),
`instrument-digests.txt`, `lane-status-before.txt` / `lane-status-after.txt` (identical; the
pre-existing ` M LOG.md` and ` M SCORECARD.md` are not mine and were not touched),
`summary.txt`, one `<case>-v1.txt` / `<case>-v2.txt` per run (predicate on line 5, `EXIT=` on line 6),
and a `<case>.diff` per fixture. Each case below is `drive.py` case `NN`; commands are
`python3 -B <instrument> --lane <mirror>` unless stated.

## Verdict

- Honest direction: **AGREE**. Unmodified lane tree prints `SELFCHECK2=PASS unresolved=0/3`, exit 0.
- HOLLOW (case 01): **AGREE**. Predecessor false-green reproduced; successor refuses all three classes.
- WINDOW (case 02): **AGREE**. Predecessor PASS; successor still sees criterion 116.
- PARTIAL (case 03): **AGREE**. One broken digit: successor fails exactly S1 (`unresolved=1/3`), predecessor passes.
- C2 is **not closed**. Three further fixtures reach `SELFCHECK2=PASS unresolved=0/3`, exit 0 with a
  named defect still present in the bytes (cases 05, 07, and the S3 class in case 08). Each is
  reproduced below with its mechanism. The frozen kill rule's literal clauses (hollow repair resolves
  a class; newer block hides an earlier criterion) are not triggered by these probes, but the target
  sentence "audits every block, so neither false-green survives" is falsified for duplicate ids and
  for a blank-line window.

## Case table

| case | command / receipt | observed (line, exit) | reading |
|---|---|---|---|
| 00 base, v1 | `round78/selfcheck.py` → `00-base-v1.txt` | line 5 `SELFCHECK=PASS unresolved=0/3`, exit 0 | predecessor passes the base defects (as claimed) |
| 00 base, v2 | `round79/selfcheck-v2.py` → `00-base-v2.txt` | line 5 `SELFCHECK2=FAIL unresolved=3/3`, exit 1 | AGREE with claims |
| 00 base, v2 `--digests` | → `00-base-v2-digests.txt` | lines 2,4,6 print `e6e751ec67878243` (row 168), `ae134338138ad3e0` (116), `7f2d54a7eb33df54` (line 73) | digests in the frozen repairs re-derive |
| 00 lane `--rev ee70e6df` | `--lane <lane> --rev ee70e6df…` → `00-lane-rev-base-v2.txt` | line 5 `FAIL unresolved=3/3`, exit 1 | AGREE with claims |
| 01 HOLLOW, v1 | three hollow lines (`cells=8 digest=deadbeefdeadbeef`, `supersedes: 116 digest=deadbeefdeadbeef`, `erratum: … digest=deadbeefdeadbeef`) → `01-hollow-v1.txt` | line 5 `SELFCHECK=PASS unresolved=0/3`, exit 0 | predecessor false-green reproduced — **AGREE** |
| 01 HOLLOW, v2 | → `01-hollow-v2.txt` | lines 2–4 each FAIL (`repairs=[168]`, `superseders={116: [149]}`, `errata=[73]` all rejected by digest); line 5 `FAIL unresolved=3/3`, exit 1 | successor refuses all three hollow lines — **AGREE** |
| 02 WINDOW, v1 | new `## Round-79 addition` block with one resolving criterion → `02-window-v1.txt` | line 5 `PASS unresolved=0/3`, exit 0 | predecessor hides 116 — **AGREE** |
| 02 WINDOW, v2 | → `02-window-v2.txt` | line 3 `criteria=50 missing=[116]`, line 5 `FAIL unresolved=3/3`, exit 1 | successor still audits 116 — **AGREE** |
| 03 PARTIAL | lane HEAD bytes, digest `…67878243`→`…67878244` (one hex digit) → `03-partial-one-digit-v1.txt`, `-v2.txt` | v1 line 5 `PASS 0/3` exit 0; v2 line 2 `S1 FAIL repairs=[168] unresolved=[168]`, lines 3–4 ok, line 5 `SELFCHECK2=FAIL unresolved=1/3`, exit 1 | successor fails exactly the broken class; predecessor passes — **AGREE** |
| 04 honest, lane tree | `--lane <lane>` in lane root → `04-lane-worktree-v2.txt`, `04-lane-worktree-v1.txt` | v2 line 5 `SELFCHECK2=PASS unresolved=0/3`, exit 0; v1 line 5 `PASS 0/3` exit 0 | honest direction — **AGREE** |
| 04 honest, HEAD copy | `04-head-honest-v2.txt` | line 5 `PASS unresolved=0/3`, exit 0 | same bytes in scratch — **AGREE** |
| 05 DUPID | honest S1/S3 repairs + second `116.` criterion with resolving pointer (original 116 kept) → `05-dupid-v2.txt`, `05-dupid-deadpointer-grep.txt` | v2 line 3 `criteria=49 missing=[]`, line 5 `SELFCHECK2=PASS unresolved=0/3`, exit 0; grep: `corpus/QUALITY.md:978:116. … corpus/evidence/round59/claims.md` still present | **DISAGREE** — PASS with the defect in the bytes |
| 06 BLANKWINDOW (repair kept) | blank line inserted before malformed row 168 → `06-blankwindow-correction-kept-v2.txt`, `06-row168-pipes.txt` | v2 line 2 `S1 ok header_cells=8 malformed=[] repairs=[168]`, exit 0; row 168 has 8 pipes = 7 cells vs 9-pipe header | **DISAGREE** — the malformed row is invisible to S1 |
| 07 BLANKWINDOW no repair | as 06 plus the digest-bearing 168 correction removed → `07-blankwindow-no-repair-v2.txt`, `-v1.txt` | v2 line 2 `malformed=[] repairs=[]`, line 5 `SELFCHECK2=PASS unresolved=0/3`, exit 0; v1 line 5 PASS exit 0 | **DISAGREE** — PASS with row 168 still 7 cells and no repair line |
| 08 STRANDED-PROBES | two appended rows at lesson lines 144 (`\| class \| …`) and 145 (`\| probe \| …`) → `08-stranded-probes-v2.txt` | line 4 `S3 FAIL stranded=[73, 145]`, exit 1 | **DISAGREE** — row 144 not flagged (see finding C) |
| 09 CONTENT | correct digest of 116 carried by unrelated criterion 149 → `09-correct-digest-unrelated-superseder-v2.txt` | line 3 `S2 ok missing=[116] superseders={116: [149]}`, line 5 `PASS unresolved=0/3`, exit 0 | limit: the digest is validated, relation of the superseder to 116 is not (lexical limit, as declared) |
| 10 DIRPTR | new criterion 149 citing `` `corpus/` `` → `10-dir-pointer-new-criterion-v2.txt`, `-v1.txt` | v2 line 3 `missing=[116]` (149 not flagged); v1 line 3 `unresolved=['149:corpus/']` | behaviour change: v2 resolves a directory prefix, v1 did not; not named in the frozen claims |

## Findings

**A. Duplicate criterion id hides a dead pointer (PASS with defect present).** Command:
`python3 -B corpus/evidence/round79/selfcheck-v2.py --lane <mirror>` after appending a second
`116.` criterion. Receipt `05-dupid-v2.txt`: line 3 `criteria=49 missing=[]` (the base count, though
one criterion was added), line 5 `SELFCHECK2=PASS unresolved=0/3`, exit 0. The original criterion
116 still names `corpus/evidence/round59/claims.md` (`05-dupid-deadpointer-grep.txt`, line 1, lane
`corpus/QUALITY.md:978`). Cause: `selfcheck-v2.py:146` `out[current] = [line]` overwrites the first
body with the second. Criterion 140 of the lane's own `corpus/QUALITY.md:1038` requires "duplicate exact
identifiers fail closed"; the successor violates it. Predecessor also PASS (`05-dupid-v1.txt`).

**B. Gates blank-line window hides a malformed row (PASS with defect present).** Command:
`python3 -B corpus/evidence/round79/selfcheck-v2.py --lane <mirror>` on lane bytes with a blank line
inserted before row 168 and the digest-bearing 168 correction removed. Receipt
`07-blankwindow-no-repair-v2.txt`: line 2 `malformed=[] repairs=[]`, line 5
`SELFCHECK2=PASS unresolved=0/3`, exit 0. The row is still 7 cells against an 8-cell header
(`06-row168-pipes.txt`). Cause: `selfcheck-v2.py:132` `if rows and not line.strip(): break` ends
the audit at the first blank line after rows begin, so S1 audits only the first contiguous run of
the Gates table. Same mechanism with the correction kept (`06-…-v2.txt`, `malformed=[]`, PASS).

**C. S3 exempts any stranded row whose first cell is the literal word `class`.** Command:
`python3 -B corpus/evidence/round79/selfcheck-v2.py --lane <mirror>` after appending
`| class | class-probe | … |` (lesson line 144) and `| probe | plain-probe | … |` (line 145). Receipt
`08-stranded-probes-v2.txt`: line 4 `stranded=[73, 145] unresolved=[73, 145]`, exit 1. Only 145 is
flagged; 144 is not. Cause: `selfcheck-v2.py:237` `row[0].strip() not in ("", "class")`, which treats a
data row as a header by its text. (Line 144 is by construction: base `round-77.md` is 142 lines.)

**D. Limit (not a bypass of the declared scope).** `09-correct-digest-unrelated-superseder-v2.txt`:
a criterion whose text is unrelated to 116 but which carries `supersedes: 116 digest=ae134338138ad3e0`
resolves 116 (line 3, `superseders={116: [149]}`, PASS). The digest proves byte identity of the
superseded body, not that the superseder addresses it. This is the declared lexical limit; recorded,
not counted as a falsification of the frozen digest sentence.

**E. Behaviour change, unnamed.** `selfcheck-v2.py:80` adds `path.startswith(tok + "/")`, so a bare
directory pointer resolves (`10-…-v2.txt` line 3 accepts 149's `corpus/`; v1 flags it). Harmless for
extant directories, but the frozen claims do not name it.

## Answer to the seat question

Yes. `SELFCHECK2=PASS unresolved=0/3` (exit 0) is reachable with (A) a duplicate criterion id that
overwrites a dead pointer, and (B) a blank line before a malformed Gates row, each with the named
defect still present in the bytes; (C) an S3 row with first cell `class` also escapes. Of these, (A)
and (B) falsify the target sentence's "audits every block" and "validates every repair line" clauses
as applied to the successor's audit windows; (C) is an S3 scanner gap of the same class.

## Recommendations (post-freeze, reported only; no predicate repaired)

1. `criteria()`: fail closed on a duplicate id (C2 instrument `selfcheck-v2.py:146`).
2. `skill_rows()`: scan to the next `## ` heading instead of the first blank line (`:132`).
3. `check_lesson()`: detect the header by position, not by the literal `class` (`:237`).
4. Keep D as a declared limit; a relation check needs a non-lexical reader.

## Residual risk and verification gaps

- Not verified: `selfcheck-control.py` (not run, per assignment); no network; no other seat's data read.
- The sweep covers the three named classes only; other S2 criteria beyond 116 are unexamined beyond
  their presence in the counter's count (49/50).
- Two `correction: SKILL.md:168` lines exist at lane HEAD (177 digest-bearing; 171 presence-only). v2
  reads only the digest-bearing one; no verdict changed.
- Tools installed: none. Scratch removed at yield.
