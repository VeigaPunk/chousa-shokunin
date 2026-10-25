# ReviewBoundSides — frozen 1/2 sides of the six named absent rows

Seat: leaf reviewer (L2). Date: 2026-10-24.
Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Measured commit: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8` (`git rev-parse HEAD` matched; subject `round-43: split the absent class and adopt one locally re-opened search-log entry`).
`git diff --exit-code 737f40b6aa8f37ffe2269db370fd6d65a720d9a8 -- corpus/evidence/round43/absent-split.tsv` exited 0. Porcelain status of that file after the checks below was empty.
Production edits: none. Bound: not retuned. Network: none. Descendants spawned: none.
Writes: this report only, plus a stdout capture under `/tmp/review-bound-sides-tool.tsv` (not the lane).

This is a review recommendation, not an admission of the claim.

## Axes

- operability: the committed table is readable, the six ids are present once each, and `tools/absent-split.py` reproduces those six lines.
- calibration: under frozen rule R43-SPLIT (row-maximum NFKC + whitespace-collapse longest contiguous run / quote length, misquote iff `>= 1/2`, else not-carried), S093, S094, S108, and S116 are misquote and S086 and S114 are not-carried.
- depth: the sides are checked from integer `run*2 ? qlen`, from per-quote figures, and from a longest-run implementation that is not the tool's DP. The bound is not moved to absorb a near miss.

## Six lines (verbatim)

Command:

```
awk -F'\t' '$1=="S086"||$1=="S093"||$1=="S094"||$1=="S108"||$1=="S114"||$1=="S116"' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/absent-split.tsv
```

Stdout, exit 0:

```
S086	not-carried	4	46	0.086957	2
S093	misquote	79	120	0.658333	1
S094	misquote	63	86	0.732558	3
S108	misquote	69	108	0.638889	1
S114	not-carried	7	32	0.218750	2
S116	misquote	34	36	0.944444	3
```

Python `repr` of the same six committed lines (tabs visible):

```
'S086\tnot-carried\t4\t46\t0.086957\t2'
'S093\tmisquote\t79\t120\t0.658333\t1'
'S094\tmisquote\t63\t86\t0.732558\t3'
'S108\tmisquote\t69\t108\t0.638889\t1'
'S114\tnot-carried\t7\t32\t0.218750\t2'
'S116\tmisquote\t34\t36\t0.944444\t3'
```

`git show 737f40b6aa8f37ffe2269db370fd6d65a720d9a8:corpus/evidence/round43/absent-split.tsv` emitted the same six lines. File pin: 15 lines, 484 bytes, newline-terminated, sha256 `bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58`. No header. Columns are id, class, max_run, max_qlen, max_ratio, nquotes.

## Confirmation

Recommendation: the six labels hold on the frozen sides.

| id | stored class | winning run | `run*2 >= qlen` | side |
|---|---|---|---|---|
| S093 | misquote | 79/120 | 158 >= 120 | misquote |
| S094 | misquote | 63/86 | 126 >= 86 | misquote |
| S108 | misquote | 69/108 | 138 >= 108 | misquote |
| S116 | misquote | 34/36 | 68 >= 36 | misquote |
| S086 | not-carried | 4/46 | 8 < 46 | not-carried |
| S114 | not-carried | 7/32 | 14 < 32 | not-carried |

None of the six winning ratios equals 1/2 (`equal_half=False` on every row). Integer comparison and the stored label agree. The printed 6-decimal ratio is a display of `run/qlen` (`4/46` rounds to `0.086957`); it does not cross 1/2 on any of these six, and the class is carried by the integers.

Same identity, not a renumber: round-42 `quarantine-verdicts.tsv` labels each of these six `absent`.

```
S086	absent
S093	absent
S094	absent
S108	absent
S114	absent
S116	absent
```

Published construction figures in `corpus/lessons/round-42.md` (S093 79/120, S094 63/86, S108 69/108, S116 34/36; S086 4/46 and 2/29; S114 7/32 and 2/30) are the figures stored as the row maximum. `corpus/evidence/round43/claims.md` names the same six and the same sides. The bound was not retuned.

## Canonical runtime

`python3 tools/absent-split.py` exited 0. Its six lines matched the committed lines (`S086 MATCH` through `S116 MATCH`). `diff -q` of the full tool stdout against the committed TSV exited 0 (`full_diff_exit=0`). The table is not a hand edit of these six against a different command output.

The tool writes stdout only. It does not write the cache, the register, or the table (`tools/absent-split.py` contract and source). After the run, porcelain status of the TSV was empty. There is no resume path and no continuity preflight in this command. A failed preflight is not implemented here; the observed path mutated nothing in the lane.

## Independent recompute (not the tool DP)

Quotes and captures were read through `tools/quarantine-check.py` `parse_register` / `cache_doc` (read-only). Longest contiguous common run was recomputed by binary search plus `str.find` of quote slices, after the same NFKC + whitespace collapse. No fetch.

Verbatim:

```
INDEPENDENT
S086 label=not-carried run=4 qlen=46 ratio=0.086957 nquotes=2 kind=page+text per=4/46,2/29 table_agree=YES integer_side=not-carried url=https://www.ncpssd.cn/
S093 label=misquote run=79 qlen=120 ratio=0.658333 nquotes=1 kind=page+pdf-text per=79/120 table_agree=YES integer_side=misquote url=https://aclanthology.org/2026.findings-acl.19.pdf
S094 label=misquote run=63 qlen=86 ratio=0.732558 nquotes=3 kind=page+pdf-text per=63/86,60/115,59/119 table_agree=YES integer_side=misquote url=https://ojs.aaai.org/index.php/AAAI/article/download/29825/31432
S108 label=misquote run=69 qlen=108 ratio=0.638889 nquotes=1 kind=page+text per=69/108 table_agree=YES integer_side=misquote url=https://arxiv.org/html/1803.05355
S114 label=not-carried run=7 qlen=32 ratio=0.218750 nquotes=2 kind=page+text per=7/32,2/30 table_agree=YES integer_side=not-carried url=https://www.sinomed.ac.cn/article.do?ui=2026335073
S116 label=misquote run=34 qlen=36 ratio=0.944444 nquotes=3 kind=page+pdf-text per=54/120,34/36,48/120 table_agree=YES integer_side=misquote url=https://aclanthology.org/N18-1074.pdf
```

Per-quote figures match the round-42 reason cells (S094 63/86, 60/115, 59/119; S116 54/120, 34/36, 48/120; S086 4/46 and 2/29; S114 7/32 and 2/30). Winning quote is unique inside each of the six rows, so the tool's strict `>` tie-break does not choose these stored runs.

Callers of the table in lane production: `corpus/evidence/round43/c2-count.py` (`read_table`, columns 0 and 1 only) and the claim sentence in `corpus/evidence/round43/claims.md`. c2 does not grade the ratio column. The ratio column still matches the independent winning ratio at 6 decimals for these six. No caller in scope misreads these six labels.

## Findings by severity

No actionable defect in scope.

- Critical: none.
- High: none.
- Medium: none.
- Low: none.

The stored classes are the classes R43-SPLIT assigns. S093, S094, S108, and S116 are misquote. S086 and S114 are not-carried.

## Residual risk

- Row-maximum is not a per-quote classifier. S094's third quote is 59/119 (`118 < 119`, below 1/2) while 63/86 and 60/115 are at or above 1/2, so the row is misquote. S116's first and third quotes are 54/120 and 48/120 (both below 1/2) while 34/36 is above, so the row is misquote. That is what the frozen sentence says. It is not a miss of these six labels, and it is not a reason to retune 1/2. The claim does not say every quote on a misquote row clears the bound. This seat does not claim that saturation.
- The six winning ratios do not sit on the equality case. They do not show whether `>=` and `>` would diverge. Among these six, the nearest winning ratios are S114 at 7/32 and S108 at 69/108. The tight quote is S094's non-winning 59/119, one character under half, and it does not decide the row.
- Display rounding of `4/46` to `0.086957` is away from the exact fraction and still far below 1/2. A later reader who re-derives the class from the printed float rather than from `max_run`/`max_qlen` is not led across the bound on these six.
- Live-web truth of any quote was not checked. The claims do not claim it. No network reopen was performed.

## Verification gaps

- `c1-count.py`, `c2-count.py`, and `c3-count.py` were not run by this seat. Their receipts were not treated as a pass. This seat does not report `C1=PASS`, `SPLIT_AGREES=15/15`, or `C3=PASS`.
- Independent slice-search recompute covered these six ids only. The other nine rows match the canonical tool byte-for-byte (`diff -q` exit 0) but were not recomputed with the second algorithm.
- No equality-case row (`run*2 == qlen`) exists among these six, so the `>=` edge of the frozen bound is untested here.
- No resume or continuity-preflight path exists in `tools/absent-split.py`. Zero mutation was observed on the path that does exist; a failed-preflight mutant was not injected, because there is no preflight to fail.

Report: `.ufo/waves/round-43/w1/ReviewBoundSides.md`
