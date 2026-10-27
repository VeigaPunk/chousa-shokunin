# R54ExecHistCounters — regression sweep of the round-54 `capture-text` change

Seat: R54ExecHistCounters (executor) · date 2026-10-26 · lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`
Subject: candidate `8a7d0f137a352000d78704ba5695ded8857104fe` (`tools/capture-text.py`, sha256 `fd0ed3f58565b781ab8eedaad5d229976e150bdd8e391a2b0cacd0a0825fcd89`) over base `c49ffc6ce1c3de87c1dfa96856239ed7274bf07b` (base tool sha256 `6902db6acf3ae5a0ac579ff88ae4fe4a36877b7b960c438bf36a67007b26be17`).
No claim, predicate, counter, control or target was changed by this seat. Scratch `/fast/scratch/hyaku/chousa-r54/R54ExecHistCounters`, `TMPDIR` set to it for every counter run; removed on exit.

## 1. Counter table — base result · candidate result · changed?

| counter | base result | candidate result | changed? |
|---|---|---|---|
| `corpus/evidence/round52/c1-count.py` (3 unseeded + `--seed 7`) | `LEGS=9/9 C1=PASS` rc 0 ×4 | `LEGS=9/9 C1=PASS` rc 0 ×4 | **no** |
| `corpus/evidence/round52/c1-supplement.py` (3 unseeded + `--seed 7`) | `SUPPLEMENT_LEGS=4/4 C1_SUPPLEMENT=PASS` rc 0 ×4 | `SUPPLEMENT_LEGS=4/4 C1_SUPPLEMENT=PASS` rc 0 ×4 | **no** |
| `corpus/evidence/round54/c1-count.py` (3 unseeded + `--seed 7`) | `LEGS=1/6 C1=FAIL` rc 1 ×4 (REGRESS only) | `LEGS=6/6 C1=PASS` rc 0 ×4 | **yes — expected** (this is R54-C1) |
| `corpus/evidence/round52/c2-count.py` | `C2=PASS` rc 0 | `C2=PASS` rc 0 | no (never runs the tool) |
| `corpus/evidence/round53/c2-count.py` | `C2=PASS` rc 0 | `C2=PASS` rc 0 | no |
| `corpus/evidence/round54/c1-supplement.py` (post-freeze, erratum E1; appeared in the lane during this seat's run) | `SUPPLEMENT_LEGS=0/3 SUPPLEMENT=FAIL` rc 1 ×4 (ISOLATED, RESAVE, HELDOUT all fail) | `SUPPLEMENT_LEGS=3/3 SUPPLEMENT=PASS` rc 0 ×4 | **yes — expected** (it is an OLE-path supplement) |
| `corpus/evidence/round54/c2-count.py` | `C2=PASS` rc 0 (`ENTRIES=2/2 BOUND=3/3 QUARANTINE_VERDICTS=3/3`) | same | no (never runs the tool) |
| `corpus/evidence/round52/build-spans.py --check` | `SPANS_ROWS=39 STALE=0` rc 0 | same | no (own `.docx` reader) |

```
$ export TMPDIR=/fast/scratch/hyaku/chousa-r54/R54ExecHistCounters
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ git show c49ffc6ce1c3de87c1dfa96856239ed7274bf07b:tools/capture-text.py > $S/base.py
$ for i in 1 2 3; do python3 corpus/evidence/round52/c1-count.py --tool $S/base.py; done; python3 … --tool $S/base.py --seed 7
LEGS=9/9 C1=PASS          (x3 unseeded)
LEGS=9/9 C1=PASS          (--seed 7)
$ for i in 1 2 3; do python3 corpus/evidence/round52/c1-count.py --tool tools/capture-text.py; done; … --seed 7
LEGS=9/9 C1=PASS          (x3 unseeded)
LEGS=9/9 C1=PASS          (--seed 7)
$ python3 corpus/evidence/round52/c1-supplement.py --tool $S/base.py    -> SUPPLEMENT_LEGS=4/4 C1_SUPPLEMENT=PASS   (x3 + --seed 7)
$ python3 corpus/evidence/round52/c1-supplement.py --tool tools/capture-text.py -> SUPPLEMENT_LEGS=4/4 C1_SUPPLEMENT=PASS (x3 + --seed 7)
$ python3 corpus/evidence/round54/c1-count.py --tool $S/base.py         -> LEGS=1/6 C1=FAIL  (x3 + --seed 7; REGRESS=PASS ['LEGS=9/9'] ['SUPPLEMENT_LEGS=4/4'])
$ python3 corpus/evidence/round54/c1-count.py --tool tools/capture-text.py -> LEGS=6/6 C1=PASS (x3 + --seed 7)
$ python3 corpus/evidence/round54/c1-supplement.py --tool $S/base.py
ISOLATED=FAIL ub04wk7v04.doc rc=2 b'REFUSED not a zip (an OOXML capture is a zip package)\n'
RESAVE=FAIL crgze4kzgs.doc rc=2 b'REFUSED unreadable package: Bad magic number for file header\n'
HELDOUT=FAIL mc0b53pytt.doc rc=2 b'REFUSED not a zip (an OOXML capture is a zip package)\n'
SUPPLEMENT_LEGS=0/3 SUPPLEMENT=FAIL      (x3 + --seed 7)
$ python3 corpus/evidence/round54/c1-supplement.py --tool $S/cand_committed.py
ISOLATED=PASS 3 docs / RESAVE=PASS 5 resaved captures / HELDOUT=PASS 3 lane files
SUPPLEMENT_LEGS=3/3 SUPPLEMENT=PASS      (x3 + --seed 7)
```
Every run above used `--tool`; every run wrote its scratch under `$TMPDIR` and removed it on exit (`ls -d $S/c1r52-* $S/c1r54-*` → no matches after the runs).

## 2. Every other lane file that runs or imports `capture-text`

`grep -rn 'capture-text' /home/vgpnk/Projects/shokunin/chousa-shokunin --include=*.py --include=*.sh --include=*.md | grep -v '/waves/'` → 34 hits in 13 files. Of these the runnable ones are the two round-52 counters, the round-54 counter, `corpus/evidence/round52/build-spans.py` (own reader; `grep -n 'subprocess' corpus/evidence/round54/build-spans.py` → no match, it never calls the tool), the entry/lesson recheck commands, and QUALITY 87/89/90. Each was run with **both** tools:

| lane file / command | base | candidate | changed? |
|---|---|---|---|
| `corpus/knowledge/japanese-search-record-niph-form-r52.md:5` recheck — `capture-text.py <raw> --locate 'SRにおける文献検索期間について明記する。'` | `LOCATED count=1 offset=8996` rc 0 | `LOCATED count=1 offset=8996` rc 0 | no |
| `corpus/lessons/round-52.md:82` — same `--locate` | `LOCATED count=1 offset=8996` | same | no |
| `corpus/lessons/round-52.md` S120 verdict offsets 8996 / 9020 / 9428 (form capture-text) | all three located once at the stated offsets | same | no |
| `corpus/lessons/round-52.md` S115 quote table, all 15 stated offsets (9, 42, 125, 1446, 8389, 8996, 9020, 9189, 9257, 9391, 9408, 9419, 9428, 19496, 19521) | `SAME rc=0` on 15/15, each `count=1 offset=<stated>` | `SAME rc=0` on 15/15 | no |
| `corpus/lessons/round-52-verifier-spotcheck.md` §7 probe (verbatim copy of the closure's `c1probe.py`, 9 cases) | `PROBE=9/9` | `PROBE=9/9` | no |
| QUALITY 90 — `cb101e95f5f5e98d019eeca1.raw` and `e9761e99ba404f708f97c4eb.raw` | rc 2 `REFUSED main part 'xl/workbook.xml' is not WordprocessingML (root {http://schemas.openxmlformats.org/spreadsheetml/2006/main}workbook)` | byte-identical | no |
| QUALITY 90 — a part over 256 MiB | rc 2 `REFUSED 'word/document.xml' inflates to 283115666 bytes (limit 268435456)` | byte-identical | no |

The 15-offset run (`SAME rc=0 stated=8996 cand='LOCATED count=1 offset=8996' base='LOCATED count=1 offset=8996'` … `ROWS 15 MISMATCH_OR_FAIL 0`) and the probe run (`spelling+form=PASS … refuse-escape=PASS` / `PROBE=9/9` for both tools) are the two receipts behind this table.

## 3. Full differential over the campaign cache — 2,596 `.raw` files

Every `.raw` under `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` was run with both tools; the compared observables are exit code, sha256 of stdout, stdout length and the first stderr line.

```
CLASS zip 8   CLASS ole 5   CLASS other 2583
DIFF[ole] 54fe0734c01f699e735b4b0a.raw cand=(0,'7dbf2a21706b5c04',33239,'') base=(2,'e3b0c44298fc1c14',0,'REFUSED not a zip (an OOXML capture is a zip package)')
DIFF[ole] 6dc68fd6b32ce9c8dfcebce8.raw cand=(0,'a8e3e7ad213b6ec5',47356,'') base=(2,…,'REFUSED not a zip (an OOXML capture is a zip package)')
DIFF[ole] 74ced3e9311594a8cc3f1f42.raw cand=(0,'7dbf2a21706b5c04',33239,'') base=(2,…,'REFUSED not a zip (an OOXML capture is a zip package)')
DIFF[ole] b539a80218080da56a75b624.raw cand=(0,'70ca0f0d6d4a7c34',2290,'')  base=(2,…,"REFUSED main part 'theme/theme/themeManager.xml' is not WordprocessingML …")
DIFF[ole] bdff491a75c6abeda1d9c01d.raw cand=(0,'f0b0899794420b0c',34234,'') base=(2,…,'REFUSED not a zip (an OOXML capture is a zip package)')
IDENTICAL 8   RC_ONLY_DIFF 2583   STDOUT_DIFF 5
```

- **All 8 zip captures: byte-identical** stdout, stderr and exit code (the two `.docx` at 48,936 and 43,030 bytes; the six refusals at their exact reason strings). The OOXML path is untouched.
- **The 5 OLE captures differ** — this is the claimed new capability, and each is the intended change: the base refused every OLE file, the candidate renders the Word text form. `b539a80218080da56a75b624.raw` is the file whose base refusal was `theme/theme/themeManager.xml` (a zip read of an OLE file that also carries an embedded OPC zip); the candidate now reads it as the OLE Word document it is (842 characters, 0 U+FFFD) and the three quotes the lane already holds are present once each (`中国知网他引频次的查询需要使用` at 16, `对于合作发文的参考文献中` at 151, `文献来源` at 493).
- **The 2,583 non-OLE captures differ only in the refusal wording** (exit code 2 and empty stdout on both sides).

## 4. Findings against the frozen claims

**F1 — the non-zip refusal wording changed on 2,583 real captures (no counter leg moves; a documentation drift).**
Base: `REFUSED not a zip (an OOXML capture is a zip package)`. Candidate: `REFUSED neither a zip package nor an OLE compound file (a Word capture is one of them)`. Exit code 2 and empty stdout are identical on every one of the 2,583. No lane file depends on the string: `grep -rn 'not a zip (an OOXML capture is a zip package)' --include=*.py --include=*.sh --include=*.md . | grep -v '/waves/'` → no hits, and the frozen counter's refusal test is prefix-only (`corpus/evidence/round52/c1-count.py:245-248`: `p.returncode == 2 and not p.stdout and any(l.startswith("REFUSED") for l in err)`). QUALITY 90 names only the `.xlsx` and inflate strings, both unchanged. **Reported, not patched** (a frozen counter and its predicate may not be proposed for change).

**F2 — the candidate no longer refuses a missing path or a directory; it dies with a traceback (a behaviour change outside the OLE path, and outside the tool's stated exit-code contract).**
`text_form` now opens the file to sniff the signature before any other check (`tools/capture-text.py:335`, `with open(path, "rb") as f: head = f.read(8)`), and that open is outside the `except OSError` guard that the base's `zipfile.is_zipfile` path relied on.

```
$ python3 tools/capture-text.py $S/nope.raw
cand rc=1   FileNotFoundError: [Errno 2] No such file or directory: '…/nope.raw'
base rc=2   REFUSED not a zip (an OOXML capture is a zip package)
$ python3 tools/capture-text.py $S            # a directory
cand rc=1   IsADirectoryError: [Errno 21] Is a directory: '…'
base rc=2   REFUSED not a zip (an OOXML capture is a zip package)
```
Same with the committed candidate `8a7d0f1` (byte-identical to the worktree file apart from a sibling's separate `Prc GrpPrl` bounds patch, which changes none of the 5 OLE outputs). The frozen r54 predicate's "no `Traceback`" clause is scoped to the three OLE refusal classes, and the r54 counter always passes existing paths, so **no leg moves**; but the tool's own docstring states exit codes 0/1/2 with `2` = refused, and a `Traceback` at exit 1 is none of them. Reported for the L1 to route; not patched by this seat.

**F3 — two text forms now exist for the same `.doc` captures with different offsets, and the round-54 artefacts use different ones.**
The tool's OLE form for `6dc68fd6b32ce9c8dfcebce8.raw` is 27,012 characters, 0 U+FFFD; `corpus/evidence/round54/build-spans.py` `raw_form` (which the r54 C2 counter uses, `c2-count.py:123-133`) still falls back to UTF-16LE for a non-zip `.raw`: 64,512 characters, 263 U+FFFD. The same S101 quotes therefore sit at different offsets in each form — `本规范推荐采用GB/T 7714中规定的顺序编码制格式著录` at **11993** (UTF-16LE, the offset `corpus/SOURCES.md` S101 cell 5 and `corpus/knowledge/citation-count-semantics-r37.md` state) and at **12795** (the OLE form); `参考文献格式，参照ISO 690` at **34374** vs **25123**. `corpus/lessons/round-54.md:57` (the S096 verdict) already uses the OLE form's 25,123. No current C2 leg fails (`ANCHOR_BOUND=3/3`, `CAPTURE_BOUND=33/33` — S101 is HELD and carries no span row), but any future `char N` for S101 must name its form. Risk for the L1 to state in the lesson, not a defect in the tool.

**F4 — the round-52 SKILL Gates row for `capture-text` is superseded by the round-54 row in the same lane; QUALITY 90's narrative still describes the old behaviour.** `SKILL.md:134` ("Reads OOXML zips only: an OLE `.doc` … is refused, not converted") is superseded by `SKILL.md:139` ("`capture-text` (OLE `.doc`, round 54; supersedes the round-52 row … by name)"), and `corpus/QUALITY.md:923` still narrates the OLE theme-part file as "accepted at exit 0 with an empty text form" whereas the landed candidate renders it as Word text (842 characters). QUALITY 90's *check* commands still pass on both named cases, so this is narrative drift, not a failing criterion. Reported only.

**Not a finding:** the counter-leg results of F1/F2 are unaffected — every counter leg of both round-52 counters and all six legs of the round-54 counter reproduce on both tools (section 1).

## 5. Risks, blockers, tooling

- No blocker. No network, no live fetch, no campaign tool run, no write outside this report and the seat scratch. The campaign cache was read only.
- `soffice` was used only by the round-54 counter (its REAL oracle), under the counter's own private profile inside `$TMPDIR`; `pgrep -u $USER -af soffice` after the runs → no match (rc 1).
- A sibling seat modified `tools/capture-text.py` in the worktree during this seat's run (worktree sha256 `e7e381b6…` vs committed `fd0ed3f5…`; the delta is a `Prc GrpPrl` bounds check). All findings above were re-verified against the **committed** candidate `8a7d0f1`; the sibling's patch changes none of the 5 OLE outputs (same stdout sha256 on all five).
- Tooling: no install, no upgrade, no `pacman` transaction. `python3` and `uv` (unused) only.
- Unverified by this seat: the round-54 counter's own LibreOffice oracle internals (I read its receipts, not its export), and any behaviour of the tool on captures absent from the campaign cache.

**VERDICT: attacked the round-54 `capture-text` candidate with the round-52 `c1-count`/`c1-supplement` counters (9/9 and 4/4 on both tools, four runs each), the round-54 counter and its new supplement (base 1/6 and 0/3, candidate 6/6 and 3/3), and a 2,596-file cache differential — no counter leg regressed and the OOXML path is byte-identical, but two real behaviour changes outside the OLE path are reported: the non-zip refusal wording (F1, 2,583 files, no leg affected) and an uncaught `FileNotFoundError`/`IsADirectoryError` traceback at exit 1 where the base refused with exit 2 (F2).**
