# R57W1ReviewCaptures — capture-store spot-check (10 captures) + store census

Seat: reviewer, leaf. Lane tip at run time: `e0e73e0` (C2 after-receipt, C2=PASS). refetch.tsv snapshotted to
scratch at 113 rows (file is live; L1 concurrently logging wave fetches). pdftotext 26.08.0 confirmed
(`pdftotext -v`). Independent recipe re-implemented from the frozen text (claims.md / capture-fetch.py:
`pdftotext -layout` for `%PDF-`, else UTF-8/replace decode, `html_to_text` only if the html-start regex
matches the first 4000 chars) — never imported the lane's modules for the recompute.

## Per-capture results (check 1 = committed sha vs last successful refetch row; check 2 = independent recipe recompute; check 3 = capture-text.py for OLE)

```
S082 ce16d57277fedfd4f0e7750e [text]   raw_sha OK(a2) txt_sha OK | recipe-recompute OK 8e1f5bff76c1
S090 4132ec1b265e60624523251f [PDF]    raw_sha OK(a2) txt_sha OK | recipe-recompute OK 2f8047a877c3
S100 b539a80218080da56a75b624 [OLE]    raw_sha OK(a2) txt_sha OK | capture-text rc=0 out=842B err='' | recipe(utf8-replace path) OK ce30e73574e7
S118 16fe8487aa97b98576a0dbac [PDF]    raw_sha OK(a2) txt_sha OK | recipe-recompute OK 927ff71c6d49
S122 b9ca2a4fdf9455867534f144 [HTML]   raw_sha OK(a2) txt_sha OK | recipe-recompute OK 2d68faf7c724 (raw==txt: html-start regex does not fire in first 4000B)
S127 b27ffd2f0161104c6a28c9f5 [PDF]    raw_sha OK(a2) txt_sha OK | recipe-recompute OK 23306b9f84c9
S128 de9f5afc3809acbf61f4d5bb [PDF]    raw_sha OK(a2) txt_sha OK | recipe-recompute OK 7e3e3cf426a7
S130 a42feae4448612f949cc715f [PDF]    raw_sha OK(a2) txt_sha OK | recipe-recompute OK 71fed1a3bc95
S083 412b146a2720ce6557268d05 [HTML DRIFTED] raw_sha OK(a2) txt_sha OK | recipe-recompute OK d37b64ed18a8
ORPHAN d473754a0cbf8d3095255d5a [PDF]  no successful refetch row; only failed rows (see below)
```

All 9 pinned targets: **OK** — committed `.raw`/`.txt` digests equal the last successful row's columns, and each
`.txt` byte-matches my independent regeneration of the frozen recipe. No CONSISTENT-leg falsifier found.
S100 note: attempt-2 row (`08:29:33Z rc=0 http=200`) landed after dispatch; it is OLE, `capture-text.py` runs
clean, and the store `.txt` equals the recipe's utf-8-replace decode path exactly (CONSISTENT per counter's
definition; C2 defined-form for OLE remains `capture-text.py` stdout, which I exercised).

Frozen counter re-run at HEAD: `SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 (S083 S087 S113 S114 S121,
absent=0) UNREACHABLE=1 (S105) BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS` rc=0 — consistent with
the e0e73e0 receipt. S083's DRIFT is genuine vs pin `a3ff65e0db9c` but its bytes/text are internally recipe-consistent.

## Orphan + store census (escalated, still in scope: spot-check of "one orphan")

The orphan is **S135** `https://www.hnysfww.com/data/article/1656481023744041713.pdf` (hnysfww.com).
Trace: refetch.tsv rows = attempt 1 `08:37:14Z rc=28 http=200 raw_sha=-`, attempt 2 `08:38:32Z rc=28` — both
FAILED, no successful row, yet `corpus/captures/d473754a0cbf8d3095255d5a.raw` (1,486,070 B, sha256
`47435e4b…b536da25`) was committed in wrap-up `b022b13` and survives at HEAD. No `.txt`. PDF is complete
(`%%EOF`, startxref 1485882 consistent). S135 is **not** in the pinned 47 (verified by running the frozen
`pinned_set`: SET_N=47, ids S082–S130 minus S084/S095/S131/S132 etc.; no S135, no wave URLs), so C2 is
unaffected — I ran the counter with the orphan on disk and it prints C2=PASS.

Full-store census (54 `.raw`): every raw whose key has a successful refetch row sha-matches it (0 mismatches);
every `.txt` has a successful-row key. **3 raws lack any successful-row backing**, all committed by wrap-up
`b022b13`: `d473754a0cbf8d3095255d5a` (S135), `d8b4f8f8829b813f16227893` (S136, same host, 2 failed rows
rc=28), `53a92273a452a58f28368691` (NHC gazette PDF for R2 candidate 国卫办药政发〔2021〕16号 — **zero** rows in
round57/refetch.tsv for its URL; scout R3 hashed the store bytes `460121b41…` which matches my census). HEAD
commit e0e73e0 says "record-less wrap-up S105 bytes removed (named in report)" — the L1's sweep removed S105's
record-less raw but missed these three.

Impact: C2 safe (none of the 3 is pinned; byte-backed verdicts all row-backed). C3 safe by construction —
the frozen predicate requires a bound capture to be "the bytes of a successful attempt", which these are not;
if the L1 wants the gazette (or hnysfww PDFs) as C3 backing, a successful `capture-fetch.py` attempt must be
logged first. Residual risk is hygiene/provenance only: the store invariant "committed bytes ⇔ successful
refetch row" is violated for 3 files; anyone citing `53a92273…raw` from the store without a refetch row is
relying on wrap-up-harvested bytes outside the frozen fetch protocol.

## Notes

- No tools installed/upgraded (none needed). No lane/fleet writes except this report. No network use.
- Scratch `/fast/scratch/hyaku/chousa-r57/R57W1ReviewCaptures` deleted at exit (trap rm -rf; spotcheck.py,
  refetch-snapshot.tsv gone). No mutating git/jj run anywhere.

VERDICT: attacked the CONSISTENT leg of R57-C2 (10-capture spot-check incl. OLE, DRIFTED, and the d473754a
orphan) — recipe/row consistency SURVIVED for all 9 pinned captures; orphan + 2 sibling wrap-up raws reported
(store-bytes-without-successful-row, no counter impact, sweep miss vs e0e73e0's stated cleanup).
