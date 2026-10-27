# R56ExecD3D4 — round-55 closure citation defects D4 and D3, verified

Lane: chousa-shokunin. Base `e5a3795191601797613eb986b36fa0b1a73fe6a1`; lane HEAD when read `99eff0eca3d7440aeb96a9afac6a421759b4f704`. Scope: verification only — no lane file written, no gate or frozen counter executed, no probe run, nothing installed. Scratch `/fast/scratch/hyaku/chousa-r56/R56ExecD3D4` (TMPDIR/PYTHONDONTWRITEBYTECODE set), removed at exit.

## D4 — quarantine-verdict offset (OLE form of the S125 capture)

Command (oracle = landed `tools/capture-text.py`, run twice; source is the on-disk capture, no fetch):

```
$ python3 chousa-shokunin/tools/capture-text.py \
    /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/bdff491a75c6abeda1d9c01d.raw \
    > $S/capture-d4.txt        # exit 0, stderr empty, 34234 bytes on disk
```

Form identity: `sha256(bdff491a… raw) first 8 bytes = D0CF11E0A1B11AE1` (OLE CFB); `sha256("http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc")[:24] = bdff491a75c6abeda1d9c01d` (capture key = S125's URL). Oracle digest `sha256(tools/capture-text.py) = 2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`, identical at `6ca92499`, `53f1ce6b` and `99eff0ec` — so this is the same oracle the round-55 receipt names (`c1-measure-after.txt:2`). Two runs byte-identical (`cmp` clean); form digest `f0b0899794420b0c10aa9d7caa75e8ccd161b8ad73d9c84e62ebf0bd9c1ef01c`; `\r` count 0 (so universal-newline reads are a no-op).

Offsets, read as `open(p, encoding='utf-8', errors='replace').read()` on the whole form (character offsets, len(form)=13718):

| string | count | `find` | closure claim |
|---|---|---|---|
| `即“灰色文献”` (U+201C/U+201D) | 1 | **1012** | 1012 — confirmed |
| `即灰色文献` (straight, no quotes) | 0 | −1 | absent — confirmed |
| `查找时应当注意收集` (sentence start) | 1 | **994** | 994 — confirmed |

Byte slab proving the attribution: `t[994:1012] = '查找时应当注意收集未公开发表的文献，'` and `t[1012:1019] = '即“灰色文献”'`. Sidecar `.txt` holds 0 of `即“灰色文献”`, 0 of `即灰色文献`, 0 of `查找时应当注意收集` (i.e. not the defined form).

The lesson line that still says 994 for the curly-quote phrase — `corpus/lessons/round-55.md:63` (verbatim, truncated only at the end):

> register `S125` (round6) — http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc — verdict: absent-as-written — … but the third, `…即灰色文献，如会议论文…`, occurs 0 times as written: the document prints `即“灰色文献”` with curly quotes (char 994).

So on that line 994 is the containing sentence's start and the phrase is at 1012: **D4 confirmed, exactly as the closure §1 states.** The other two offsets on the same line were spot-checked and are right — `t[761:]` starts `检索策略包括检索的数据库…`, `t[4625:]` starts `文献检索策略：检索途径…` — so the defect is isolated to the curly-quote offset, not the line. `corpus/lessons/round-55.md:86` (`| S124 | 994 | 查找时应当注意收集…|`) is the sentence quote and stands, matching 994 above.

State note: two round-56 append-only bullets already exist and are **committed** in the lane — `corpus/lessons/round-55.md:31` (D4) and `:32` (D3), both present at HEAD `99eff0ec` (`git show HEAD:corpus/lessons/round-55.md | grep -c "Round 56 (closure D"` → 2; `git log -1 -- corpus/lessons/round-55.md` → `99eff0ec round-56: C2 integration …`), working tree clean for that file (`git status --porcelain` shows no entry). Line 31's numbers (`count 1 at 1012`, `count 0`, `count 1 at 994`) match the run above digit for digit, so no second append is needed and a duplicate append would repeat them.

## D3 — measurement-revision citations vs receipt headers

Receipt headers, as committed (`corpus/evidence/round55/`):

```
c1-measure-after.txt:1  # R55-C1 after-measurement (L1), candidate tools/build-spans.py at 6ca924995d48facbf704d2aa22ddaec236059039, frozen counter at 1fc5d92b
c2-measure-after.txt:1  # R55-C2 after-measurement (L1) at lane master 5a35ebd6cff2f165b4785baa592c269fb04179f0
c3-measure-after.txt:1  # R55-C3 after-measurement (L1) at lane master 5a35ebd6cff2f165b4785baa592c269fb04179f0
```

| report claim (`.ufo/reports/round-55/chousa.md`) | receipt header revision | result |
|---|---|---|
| `:30` C1 "measured at `6ca92499` (tool sha256 `1ed2650a…`)" | `c1-measure-after.txt:1` → `6ca924995d48…`; `:2` tool-rev `1ed2650a…` | **match** (digest recomputed: `git show 6ca92499:tools/build-spans.py | sha256sum` = `1ed2650a…c80bf6`) |
| `:31` C2 "measured at `29cfb12a` (`c2-measure-after.txt`)" | `c2-measure-after.txt:1` → `5a35ebd6…` | **mismatch** (report `29cfb12a`, receipt `5a35ebd6`) |
| `:31` C2 "re-run at `53f1ce6b` `C2=PASS`" | no receipt names `53f1ce6b` | **mismatch / unreceipted** (`grep -rn 53f1ce6b corpus/evidence/round55/` → no hits) |
| `:32` C3 "measured at `29cfb12a` (`c3-measure-after.txt`)" | `c3-measure-after.txt:1` → `5a35ebd6…` | **mismatch** |
| `:11`/`:12` C2 and C3 "— commit `5a35ebd6`" | same headers → `5a35ebd6…` | **match** |

Only the revision citation is wrong; the receipts' *values* are the report's values (`c2-measure-after.txt`: `BOUND=3/3 QUOTE_ROWS=19 CAPTURE_BOUND=19/19 ANCHOR_BOUND=3/3 QUARANTINE_VERDICTS=1/1 (S125) C2=PASS exit=0` vs report `:31`; `c3-measure-after.txt`: `ERRATA=11/11 MISSING=0 ANCHOR=0 WRONG=0 C3=PASS exit=0` vs report `:32`, whose `WRONG=11`/`ANCHOR=11` are its own "before" controls).

Provenance detail the closure bullet leaves implicit: the two receipts did not exist at the revision they name — `git cat-file -e 5a35ebd6:corpus/evidence/round55/c2-measure-after.txt` → `fatal: path … exists on disk, but not in '5a35ebd6'`; `git log -- corpus/evidence/round55/c{2,3}-measure-after.txt` → added in `53f1ce6b` (39 insertions, `git diff --stat 5a35ebd6 53f1ce6b -- …`). So "measured at `5a35ebd6`, receipt filed at `53f1ce6b`" — which is why the `:31` "re-run at `53f1ce6b`" line has a file that exists only at that commit but a header that names `5a35ebd6`.

The bullet's load-bearing claim "`29cfb12a` touched none of their inputs" holds: `git diff --name-only 5a35ebd6 29cfb12a` → `corpus/evidence/round55/recurring.tsv`, `corpus/knowledge/source-type-taxonomy-r37.md`. Counter inputs (string literals + constructed paths in `c2-count.py`/`c3-count.py`): `corpus/knowledge/grey-literature-and-chinese-search-record-r40.md`, `corpus/SOURCES.md`, `corpus/evidence/round55/spans.tsv` (c2); `corpus/knowledge/source-type-taxonomy-r36.md`, `corpus/QUALITY.md`, `corpus/lessons/round-54.md`, `corpus/evidence/round54/{c1-supplement.py,c1-count.py,controls/c1-controls.txt}`, `corpus/evidence/round53/pointer-anchor-check.py`, `SCORECARD.md`, `tools/capture-text.py` (c3). r37 ≠ r36 and `recurring.tsv` is read by neither, so the C2/C3 verdicts stand at `29cfb12a` as well.

## Risks / blockers

- Citation-level verification only: neither `c1/c2/c3-count.py` nor any round-56 gate was executed by this seat (leaf wave, no gate runs; also no network, so nothing was re-fetched). Conclusions about the measurement trees rest on receipt headers, `git diff --name-only`, and the counters' input-path sets — not on a re-run.
- `corpus/lessons/round-55.md:31-32` are already committed at `99eff0ec`; the L1 should not append D3/D4 bullets again. The stale text they correct (`:63` "(char 994)", report `:31`/`:32` "measured at `29cfb12a`") remains in place by the lane's append-only convention, which is expected.
- No tool installed; no pacman transaction; nothing written outside this report and the scratch dir (removed).

VERDICT: D4 confirmed — `即“灰色文献”` count 1 at **1012**, `即灰色文献` count 0, sentence `查找时应当注意收集` count 1 at **994** of the defined OLE form (lesson `round-55.md:63` still attributes 994 to the phrase); D3 confirmed — C1's `6ca92499` citation matches its receipt, C2's and C3's `29cfb12a` citations do not (receipts say `5a35ebd6`) and the `53f1ce6b` C2 re-run has no receipt naming it; both closure defects **survive verification** and the two already-committed round-56 correction bullets are accurate.
