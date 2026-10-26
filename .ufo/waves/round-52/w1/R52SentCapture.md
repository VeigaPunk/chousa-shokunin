# R52 w1 — sentinel: hostile-package and write-path review of the C1 tool, the round's counters and controls

author: R52SentCapture (sentinel) · 2026-10-26 · interpreter `Python 3.14.8`, `pyexpat.EXPAT_VERSION=expat_2.9.0`
targets (sha256): `tools/capture-text.py` `1726cd04…` (live, uncommitted) / `3986a97…` (= candidate `804a453`); `c1-count.py` `4ec29333…`;
`c2-count.py` `206ae11d…`; `build-spans.py` `17326154…`; `controls/build-c2-controls.py` `ae96f696…`; other controls are stdout-only readers.
Scratch `/fast/scratch/hyaku/chousa-r52/R52SentCapture` (TMPDIR exported), removed at exit. No installs.
**§0 disclosure.** `git status` at 20:10:27 shows `M tools/capture-text.py` (mtime 20:10:09): another seat edited it mid-review. `git diff` adds
`el.clear()` in the `iterparse` end-branch and a refusal `if not stack and el.tag != W+"document": raise Refused(...)`. I kept both revisions
(`tool-head.py`, `tool-wt.py`) in scratch and labelled every number by hash; §7 is what the new refusal does to the frozen claim.

## 1. Summary

| # | hazard | severity | observed | smallest fix |
|---|---|---|---|---|
| H1 | zip bomb in the main part or `_rels/.rels`; text accumulated in a list | **medium** — DoS on the lane's own reader of web-fetched captures, and the refusal contract is lost | 1.04 MB → 1 GiB text, 3.03 GB RSS, rc 0; under `ulimit -v 2000000` (1.91 GiB) rc **1** + traceback, no `REFUSED` | `ZipInfo.file_size` gate before parse, `io.StringIO`, `MemoryError`→`Refused` |
| H2 | billion laughs / external entities | **none open** | expat 2.9 amplification limit → `REFUSED` rc 2; no external entity fetch | pin interpreter+expat in the receipt |
| H3 | `Target` with `../../` | **none open** | reads a *zip member* of that name; strace shows no `/etc/passwd` open; absent target → `REFUSED` | optional: refuse `..`/absolute targets |
| H4 | write paths | **low** (lane write, `/tmp`) | `build-spans` writes under `--root` (default LANE) and unlinks; controls use `/tmp` when TMPDIR unset and leak on exception | explicit `--root`/`--work` + lane-root refusal; `finally` |
| H5 | `c1-count` scratch lifecycle | **low** | TMPDIR/`--work` honoured; SIGINT cleans (`rc=130`, 0 dirs); **SIGTERM leaks**; absent `--work` → rc 1 not 2 | SIGTERM handler → `SystemExit`; validate `--work` |
| H6 | frozen predicate vs live bytes | **medium, for the Gate** | `workbook.docx`/`strict.docx`: HEAD rc 0 + empty text, live rc **2 REFUSED** — a refusal class the frozen sentence does not list, unmeasured by the counter | revert, or `claims-erratum.md` |

## 2. H1 — zip bomb: the parse streams, the output does not
```
$ python3 -c "import zipfile; [print(i.filename,i.compress_size,i.file_size) for i in zipfile.ZipFile('fx/bomb_1g.docx').infolist()]"
_rels/.rels compressed 166 uncompressed 284
word/document.xml compressed 1043831 uncompressed 1073742079      # whole package 1,044,247 B
$ python3 run.py 2000000 fx/n1.out  python3 tool-wt.py fx/bomb_1g.docx    # child under ulimit -v 2000000
rc=1 elapsed=2.66s maxrss=1081272KB stdout=0B
ERR|   File "tool-wt.py", line 92, in text_form / out.append(el.text or "") / MemoryError
$ python3 run.py 0 fx/n1u.out python3 tool-wt.py fx/bomb_1g.docx          # no cap
rc=0 elapsed=3.40s maxrss=3030856KB stdout=1073741825B
$ python3 run.py 2000000 fx/n2.out python3 tool-wt.py fx/bomb_2g.docx     # 2,087,890 B package
rc=1 elapsed=4.91s maxrss=1989572KB stdout=0B  ERR| object type name: MemoryError … lost sys.stderr
$ python3 run.py 2000000 fx/nr.out python3 tool-wt.py fx/bomb_rels.docx   # only _rels/.rels inflates, 1 GiB
rc=1 elapsed=1.57s maxrss=1066456KB stdout=0B  ERR| zipfile/__init__.py:1197 in _read1 … MemoryError: Unable to allocate output buffer.
```
The literal "1 MB → 2 GB" shape is not reachable through deflate (ceiling ≈1032:1; 2 GiB needs 2,087,890 B — my `bomb_2g`). What is reachable is
3× the text resident, because every `w:t`/`w:p` appends to `out` and the result is joined; `el.clear()` changes nothing (3.033 GB → 3.031 GB). Under a cap the tool dies with `rc=1` + traceback — **outside the frozen refusal shape** ("exit 2, `REFUSED` on stderr,
nothing on stdout"), and on the 2 GiB file it cannot even print the traceback. Newline-dense shape (QUALITY 18):
```
$ python3 run.py 2000000 fx/np.out python3 tool-wt.py fx/paras_1m.docx    # 1,000,000 <w:p/> in 9,323 B
rc=0 elapsed=0.57s maxrss=109728KB stdout=1000000B                        # 110× the output size
```
The nine legs never build a big package, so C1 passes either way. Fix: check `ZipInfo.file_size` for rels+main before `read`/`open`, build
into `io.StringIO`, `except MemoryError: raise Refused("package too large to render")`. Do not call this reader resource-bounded (QUALITY 18).
## 3. H2 — entity expansion and external entities: bounded by expat, not by the tool
```
$ python3 run.py 2000000 fx/n-laughs7.out python3 tool-wt.py fx/laughs7.docx
rc=2 … REFUSED unreadable package: limit on input amplification factor (from DTD and entities) breached: line 11, column 106
$ …fx/laughs9.docx → rc=2 (same) · fx/laughs_rels.docx (DTD inside _rels/.rels) → rc=2 "REFUSED _rels/.rels does not parse: … breached"
$ …fx/laughs4.docx → rc=0, 100001 B (10^4 expansion works: a limit, not a ban)
$ …fx/xxe_int.docx → rc=2 REFUSED unreadable package: undefined entity &x;   ·  fx/xxe_pe.docx → rc=2 (undefined entity)
$ …fx/xxe_extdtd.docx (DOCTYPE SYSTEM "file:///etc/hostname") → rc=0, "OK\n"
$ strace -f -e trace=openat,open -o fx/xxe.strace python3 tool-wt.py fx/xxe_extdtd.docx; grep -E 'hostname|/etc' fx/xxe.strace
/etc/ld.so.cache · /etc/localtime only (loader, locale) — no external DTD fetch
```
Residual: that protection is an expat ≥2.4 default and the receipt pins neither interpreter nor expat; on an older expat `laughs9` becomes an OOM
(H1's shape). One line: print `sys.version` and `pyexpat.EXPAT_VERSION` into the counter's output.
## 4. H3 — traversing `Target`: zip members only, no filesystem read
```
$ python3 tool-wt.py fx/trav.docx; echo rc=$?      # zip member named ../../../../etc/passwd, Target the same
ZIPTRAVERSAL-MARKER                                # that MEMBER's text, not the file
rc=0
$ strace -f -e trace=openat,open -o fx/trav.strace python3 tool-wt.py fx/trav.docx; grep -E '/etc|passwd' fx/trav.strace
/etc/ld.so.cache · /etc/localtime — no /etc/passwd
$ fx/trav_rel.docx → rc=2 REFUSED officeDocument target '../../../../etc/passwd' is not in the package
$ fx/trav_missing.docx → rc=2 (same; no filesystem fallback)  ·  fx/trav_back.docx (..\..\) → rc=2
$ fx/trav_ext.docx (Target file:///etc/passwd, TargetMode="External") → rc=2 REFUSED no officeDocument relationship in _rels/.rels
```
`posixpath.normpath` + `target in z.namelist()` (`capture-text.py:60`) keeps every read inside the package and nothing is extracted, so there is
no traversal write either. Residual cosmetic risk: a receipt can print a text form read from a member *named* like an escape; refusing a
normalized target that starts with `..` or is absolute (one condition) removes the ambiguity.

## 5. H4 — write paths (`grep -n 'write|mkdtemp|open('`, plus strace of each run)
| file | writes | `/tmp` | into the lane? |
|---|---|---|---|
| `tools/capture-text.py` | none — 0 `O_WRONLY/O_CREAT` among 179 `openat` | none | no |
| `c1-count.py` | one `mkdtemp(prefix="c1r52-", dir=a.work)` `:258` + 11 package files, `finally: rmtree` `:327-328` | none (`--work`, else `tempfile`→`$TMPDIR`) | no — strace: 1 `mkdir`, all writes under the work dir |
| `c2-count.py` | no write-mode syscall in a `--lane-only` strace (its `inference-ground` loop is skipped while entries are absent; that tool writes only with `--json`, not passed); `git show/grep` are read-only | none | only `__pycache__` via `importlib` of `build-spans` `:89` — proved on a mirror copy; `.gitignore:3 corpus/**/__pycache__/` covers it (info) |
| `build-spans.py` | `spans.tsv` `:256` + `spans/*.txt` `:258`, and **unlinks** stale spans `:255`; `--root` default `LANE` `:238` | none | **yes by default** — on a scratch root `--check` wrote nothing, default mode wrote `spans.tsv` + `spans/S113-1.txt` |
| `controls/build-c2-controls.py` | `mkdtemp` `:35` **without `dir=`**; `rmtree` `:52`/`:69` with **no `try/finally`** | none literal, but ambient `TMPDIR` is **unset** here → a bare run creates `/tmp/chousa-r52-c2ctl-*` | no (`git show BASE:…`); a `PKG` failure leaks — same-depth copy, `PKG` redirected: `rc=1`, leftover `chousa-r52-c2ctl-staged-op7twt50`; success path 0 |
| `controls/{naive,cache-txt,const}-tool.py` | stdout only | none | no |
Fixes: `build-spans` should refuse `--root == LANE` unless `--land` is passed; `c1-count` should refuse a `--work` inside `LANE` (QUALITY 35's rule —
the round-32 counter exits 2 for that; here `LANE` appears only at `:45` and `:248`, no path comparison); `build-c2-controls` should pass
`dir=os.environ["TMPDIR"]` and wrap both stages in `try/finally`.
## 6. H5 — TMPDIR, `--work`, and killing it
```
$ python3 -c "import tempfile;print(tempfile.gettempdir())"   # TMPDIR exported → /fast/scratch/…/R52SentCapture; no /tmp/c1r52-*
$ (c1-count.py --per-leg 40 --work sigint & sleep 0.5; kill -INT $!)    # during: 1 dir  →  rc=130, after INT: 0 entries
$ (c1-count.py --per-leg 40 --work sigterm & sleep 0.5; kill -TERM $!)  # during: 1 dir  →  rc=143, after TERM: 1 (c1r52-ths3n4c2)
$ c1-count.py --per-leg 1 --work does-not-exist                         # rc=1, FileNotFoundError traceback (docstring promises 2)
```
Default receipt (live bytes; identical 9/9 on the HEAD bytes): `LEGS=9/9 C1=PASS`, 1.36 s,
`REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682`, 0 leftover dirs. Fix: `signal.signal(SIGTERM, …)` raising `SystemExit` so `finally` runs,
and `--work` must be an existing dir → exit 2.

## 7. H6 — the live edit diverges from the frozen C1 sentence (route to Gate/L1)
```
$ for t in tool-head.py tool-wt.py; do for f in workbook strict; do python3 $t fx/$f.docx; echo "rc=$?"; done; done
tool-head.py workbook rc=0 (no output)   tool-head.py strict rc=0 (no output)
tool-wt.py   workbook rc=2 REFUSED main part 'xl/workbook.xml' is not WordprocessingML (root {…spreadsheetml…})
tool-wt.py   strict   rc=2 REFUSED main part 'word/document.xml' is not WordprocessingML (root {http://purl.oclc.org/ooxml/…})
```
The frozen predicate fixes the refusal set to "not a zip, no officeDocument relationship, or target missing". A `.xlsx` **and a Strict-OOXML
`.docx`** now exit 2 where HEAD printed the (empty) text form with exit 0; `c1-count`'s REFUSE leg builds neither, so the counter scores 9/9 on
both revisions and cannot see the change. Per the claims' admission rule this needs `claims-erratum.md`, or an unknown root should render as
text-form `""` (the predicate). It also breaks the claims' "both readers implement the one rule": `build-spans.docx_text` still gives `''` for
`fx/workbook.docx` (checked; and on the NIPH `.raw` it gives 19682 chars — byte-identical to the tool's stdout). `el.clear()` is harmless.

## 8. Claim impact
- **C1**: all nine frozen legs pass on both revisions (measured); no predicate change needed. The reader is **not** resource-bounded (H1), and
  the live bytes add an unmeasured refusal class (H6). H2/H3 closed.
- **C2**: the counter writes nothing and reads only; on the NIPH capture `build-spans.docx_text` is char-identical to the tool (19682). It shares
  H1: `z.read(part)` materialises the whole part (`bomb_1g` → 1,073,741,825 chars in 3.42 s; under the 1.91 GiB cap a traceback in `zipfile.read`),
  so a hostile cache capture crashes the counter rather than being refused — one size gate in `docx_text` closes it.
- Discipline: no lane writes by me outside this report; one transient 0-byte `/tmp/e.$$` stderr sink (locale probe) was removed at once; no `/tmp`
  or lane scratch leftovers; my scratch removed.

VERDICT — attacked the C1 reader and the counters with a deflate bomb, entity bombs, external entities and traversing `Target`s: the
entity/external/traversal surfaces are closed, but the reader is memory-unbounded with a crash path outside the frozen refusal shape,
`build-spans`/the controls carry lane and `/tmp` write paths, and an uncommitted edit adds a refusal class the frozen counter cannot see.