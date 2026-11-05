# Draft registry rows, GATE-RECORD lines and Gate prose — C2 calibration (R80ScribeA)

Draft only. Nothing here is landed: `corpus/SOURCES.md` and `corpus/lessons/round-80.md` are untouched.
Pinned base: `b7803829922770b890e9f4efdd30d12c3695439a` (`git show <rev>:<path>` only; no URL opened).
Every count below was measured by this seat with `wc -w`, `wc -l` or `grep -c -F` on the pinned bytes.
Receipts for each measurement are in `receipts/` beside this file.

## 1. Registry rows

Insert the four lines directly after the `S198` row inside the `## Registry` table
(at b7803829 the `S198` row is line 210, the table closes before `## Paths` at line 212). Do not append
them at end of file; round 79 lost three rows that way (`E12`).

```text
| S199 | chousa round-79 non-author spot-check — corpus/lessons/round-79-verifier-spotcheck.md | own-work | B | the round-79 spot-check's payload-channel finding on the operability axis, read as a source about battery forgeability | b7803829922770b890e9f4efdd30d12c3695439a, line 222 | A battery can be fully forgeable through a payload channel on both batteries, so a per-channel operability gain is a narrow artifact delta, not a capability gain | mined | 2026-11-04 | on-release | corpus/lessons/round-80.md |
| S200 | chousa QUALITY criterion 147 — corpus/QUALITY.md | own-work | B | the successor requirement an outer battery's subject copy must meet when the salt family is known to a normalizer | b7803829922770b890e9f4efdd30d12c3695439a, criterion 147 at line 1056 | supersedes S196 — a subject-identity salt is defeated by any normalizer that knows its marker family, so the closure is a per-channel measurement and not a property of the salt; a successor copy must not be a textual derivative of a committed file | mined | 2026-11-04 | on-release | corpus/lessons/round-80.md |
| S201 | chousa QUALITY criterion 146 — corpus/QUALITY.md | own-work | B | the successor requirement a self-assessment counter must meet when its repair lines are presence-only | b7803829922770b890e9f4efdd30d12c3695439a, criterion 146 at line 1054 | supersedes S197 — a self-assessment counter validates each resolution line against the bytes it claims to repair, and its audit window covers every block rather than the newest; a repair line must be validated against the bytes it names | mined | 2026-11-04 | on-release | corpus/lessons/round-80.md |
| S202 | round-78 hollow-mirror receipt — .ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt | own-work | C | a defect receipt offered as a source about verification method | 3eb4a3cad8febf75698a017cb6c4441f763b3454, lines 1-11 | supersedes S198 — REJECTED: a receipt that demonstrates one counter's false green is that counter's own evidence, not a source about how self-assessment should be audited (the S195 class one layer out); anchor corrected from lines 1-20, the receipt is 11 lines; flip: admit scoped to what a control receipt must carry if an admitted entry ever rests on receipt format | rejected | 2026-11-04 | on-release | — |
```

Shape check (measured, `awk -F'|' '{print NF-1}'` and a split on `|`): each row has 12 pipes, i.e. 11 cells;
statuses `mined, mined, mined, rejected`; tiers `B, B, B, C`; no cell contains `|`.

## 2. GATE-RECORD lines

Grammar: `GATE-RECORD S### rev=<40-hex> path=<repo-relative> line=<n> words=<w> quote=<verbatim substring>`.

```text
GATE-RECORD S199 rev=b7803829922770b890e9f4efdd30d12c3695439a path=corpus/lessons/round-79-verifier-spotcheck.md line=222 words=16 quote=the round also shows the battery is fully forgeable through the payload channel on **both** batteries
GATE-RECORD S200 rev=b7803829922770b890e9f4efdd30d12c3695439a path=corpus/QUALITY.md line=1056 words=15 quote=by any normalizer that knows its marker family, so the closure is a per-channel measurement
GATE-RECORD S201 rev=b7803829922770b890e9f4efdd30d12c3695439a path=corpus/QUALITY.md line=1054 words=25 quote=A self-assessment counter validates each resolution line against the bytes it claims to repair, and its audit window covers every block rather than the newest
GATE-RECORD S202 rev=3eb4a3cad8febf75698a017cb6c4441f763b3454 path=.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt line=2 words=9 quote=HEAD QUALITY + empty Round-79 block; no supersedes anywhere
```

### 2a. Per-line verification (commands and observed output, exit codes as printed)

Receipt: `receipts/row-verify.txt`; the four-line counter run is `receipts/gate-check.txt`
(`check_gate.py`, reads only `git show <rev>:<path>` and `git cat-file`).

```text
## S199
$ git show b7803829922770b890e9f4efdd30d12c3695439a:corpus/lessons/round-79-verifier-spotcheck.md | sed -n '222p' | grep -c -F "the round also shows the battery is fully forgeable through the payload channel on **both** batteries"
1
# exit: 0
$ printf '%s' "the round also shows the battery is fully forgeable through the payload channel on **both** batteries" | wc -w
16
## S200
$ git show b7803829922770b890e9f4efdd30d12c3695439a:corpus/QUALITY.md | sed -n '1056p' | grep -c -F "by any normalizer that knows its marker family, so the closure is a per-channel measurement"
1
# exit: 0
$ printf '%s' "by any normalizer that knows its marker family, so the closure is a per-channel measurement" | wc -w
15
## S201
$ git show b7803829922770b890e9f4efdd30d12c3695439a:corpus/QUALITY.md | sed -n '1054p' | grep -c -F "A self-assessment counter validates each resolution line against the bytes it claims to repair, and its audit window covers every block rather than the newest"
1
# exit: 0
$ printf '%s' "A self-assessment counter validates each resolution line against the bytes it claims to repair, and its audit window covers every block rather than the newest" | wc -w
25
## S202
$ git show 3eb4a3cad8febf75698a017cb6c4441f763b3454:.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt | sed -n '2p' | grep -c -F "HEAD QUALITY + empty Round-79 block; no supersedes anywhere"
1
# exit: 0
$ printf '%s' "HEAD QUALITY + empty Round-79 block; no supersedes anywhere" | wc -w
9
```

Counter run (`check_gate.py`, the same four R1–R4 tests the grounding counter names; `python3 -B check_gate.py gate-records.txt`):

```text
S199 R1=ok R2=ok R3=ok R4=ok words_recorded=16 words_measured=16 line_n=222 line_len_chars=671 PASS
S200 R1=ok R2=ok R3=ok R4=ok words_recorded=15 words_measured=15 line_n=1056 line_len_chars=1090 PASS
S201 R1=ok R2=ok R3=ok R4=ok words_recorded=25 words_measured=25 line_n=1054 line_len_chars=1225 PASS
S202 R1=ok R2=ok R3=ok R4=ok words_recorded=9 words_measured=9 line_n=2 line_len_chars=61 PASS
GATE_RECORDS_CHECK=PASS failures=0
exit=0
```

Note: `check_gate.py` is this seat's own counter, not `corpus/evidence/round80/gate-grounding-check.py`
(that file is frozen and was not run here). Its PASS is evidence about these four lines only.

## 3. Old-record measurements (the round-79 lesson's Gate, `corpus/lessons/round-79.md` at b7803829)

Receipt: `receipts/old-record.txt`.

```text
## S196 old (lesson states 25)
1
27
## S197 old (lesson states 24)
1
25
## S198 old
0
# exit: 1
10
```

Read as: the S196 quote in the lesson is verbatim on QUALITY line 1056 but is **27** words, not 25.
The S197 quote is verbatim on line 1054 and is **25** words, not 24. The S198 "located quote"
(`the audit window is the last` … `block`, 10 words) occurs **0** times in its cited receipt, and the receipt is
**11** lines (`git show 3eb4a3ca:<path> | wc -l` → 11), not the 1–20 the row states.

## 4. The `## Gate` block for `corpus/lessons/round-80.md`

```markdown
## Gate

- Admit S199, own-work B, scoped to the round-79 non-author spot-check's payload-channel finding on the operability axis. `corpus/lessons/round-79-verifier-spotcheck.md` at `b7803829922770b890e9f4efdd30d12c3695439a`, line 222 (the operability row). Opened 2026-11-04. Located quote: "the round also shows the battery is fully forgeable through the payload channel on **both** batteries" (16 words, `wc -w`). Grounds C1's evidence: the battery accepts a payload-decoding forger on both batteries, so the operability gain is a narrow artifact delta, not a capability gain. Note: the frozen `corpus/evidence/round80/claims.md` describes S199 as "own-work A: the round-79 structure-identity receipts"; this row follows the round's dispatch (own-work B, the spot-check finding). The L1 reconciles the two before landing; the frozen claims file is not amended.
- Admit S200, own-work B, superseding S196. `corpus/QUALITY.md` at `b7803829922770b890e9f4efdd30d12c3695439a`, criterion 147 at line 1056. Opened 2026-11-04. Located quote: "by any normalizer that knows its marker family, so the closure is a per-channel measurement" (15 words, `wc -w`). Grounds C1's target: the successor subject copy must not be a textual derivative of a committed file, because a salt is only as strong as the normalizers that know its marker family.
- Admit S201, own-work B, superseding S197. `corpus/QUALITY.md` at `b7803829922770b890e9f4efdd30d12c3695439a`, criterion 146 at line 1054. Opened 2026-11-04. Located quote: "A self-assessment counter validates each resolution line against the bytes it claims to repair, and its audit window covers every block rather than the newest" (25 words, `wc -w`). Grounds C2's target: a repair line must be checked against the bytes it names, and the pointer audit must cover every block, not only the newest.
- Reject S202, own-work C, superseding S198. `.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt` at `3eb4a3cad8febf75698a017cb6c4441f763b3454`, lines 1–11 (the file is 11 lines). Opened 2026-11-04. Located quote on line 2: "HEAD QUALITY + empty Round-79 block; no supersedes anywhere" (9 words, `wc -w`). REJECTED: a receipt that demonstrates one counter's false green is that counter's own evidence, not a source about how self-assessment should be audited (the S195 class one layer out); flip: admit scoped to what a control receipt must carry if an admitted entry ever rests on receipt format.
- Record correction (append-only; S196, S197 and S198 are not edited). S196 → S200: the old quote was 27 words, not the 25 stated; the new quote is 15 words. S197 → S201: the old quote was 25 words, not the 24 stated; the new quote is 25 words. S198 → S202: the old located quote (10 words) is not in the cited receipt and the receipt is 11 lines, not 20; the new anchor is lines 1–11 and the new quote is 9 words.
- No URL was fetched: all four rows are revision-pinned committed paths read with `git show <rev>:<path>` and `git cat-file`.
- Non-author spot-check requested: re-open each `GATE-RECORD` line at its pinned revision and re-measure its quote with `wc -w` before admitting S199, S200, S201 and S202. Dispatched wave seats are author-lane evidence, not an independent admission review.
```

## 5. Flags for the L1

- **S199 kind conflict.** The frozen `claims.md` (C1 "Sourced claims") says S199 is `own-work A`, the round-79 structure-identity receipts. The dispatch says `own-work B`, the spot-check's payload finding at line 222. This draft follows the dispatch. The L1 must pick one; the frozen file is not amended here.
- **Quote length for S200.** The frozen `claims.md` names a "15-word located quote" for S200 but does not print its text. The row uses `by any normalizer that knows its marker family, so the closure is a per-channel measurement` (15 words by `wc -w`, verbatim on line 1056 at the base revision). I did not exhaustively search criterion 147 for other 15-word runs; the L1 may pick a different substring, which must be re-measured with the same `GATE-RECORD` checks.
- **Lineage.** `b7803829` = `acca2449` + one commit (`git log acca2449..b7803829` → `b7803829`, `git show --stat` → 1 file, 286 insertions) that adds `corpus/lessons/round-79-verifier-spotcheck.md`. The file does not exist at `acca2449` (`git cat-file -e` → rc 128). The round-79 spot-check's line 222 therefore exists only at the base revision used here.
- **Not run:** `scripts/sources-census.sh validate` against the drafted table (not run; the L1 should run it after landing the rows). `corpus/evidence/round80/gate-grounding-check.py` was not run (frozen, and the L1's landed copy is the one that counts).
