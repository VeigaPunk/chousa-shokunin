# R52 w2 — sentinel: the wave-1 hazard set re-run against the LANDED tool and counters, plus three new attempts

author: R52W2SentToolFinal (sentinel) · 2026-10-26 · `Python 3.14.8`, `pyexpat.EXPAT_VERSION=expat_2.9.0` · attacked commit `e769c03738d08c36109556ebf301a1db0dcf143d` (`git diff --stat e769c03 HEAD -- tools/ corpus/evidence/round52/ …` empty; every file below is byte-identical in the work tree and at `e769c03`). sha256[:8]: `capture-text.py` `81ba0db0` · `c1-count.py` `4ec29333` · `c2-count.py` `206ae11d` · `build-spans.py` `17326154` · `controls/build-c2-controls.py` `ae96f696` · `c1-supplement.py` `86711a5f` · `verdict-gap.py` `20b9c0f3`.
Scratch `/fast/scratch/hyaku/chousa-r52/R52W2SentToolFinal` (TMPDIR exported), removed at exit. No installs. Every fixture is mine and rebuildable from the commands shown; the only lane writes are this report and one `build-spans.py --check` read-only run.

## 1. Summary

| # | attack (what it attacks) | severity | state at `e769c03` |
|---|---|---|---|
| H1 | truthful 1 GiB part (re-run of w1 H1) | was medium | **CLOSED** — gate refuses before parse, 0.03 s, no allocation |
| H1′ | the same on the `_rels/.rels` read path (new) | **medium** | **OPEN** — `MAX_PART` is compared to the *declared* size, then `z.read` allocates the *real* expansion |
| H2 | 9-deep entity ladder, external DTD (re-run) | was none | **CLOSED**, unchanged; residual: no interpreter/expat line in any receipt |
| H3 | traversing / External `Target` (re-run) | was none | **CLOSED + hardened** (new `..`-refusal fires) |
| A | zip whose central directory declares a small `file_size` for a large member (new) | **medium** | tool main part bounded and refused; `build-spans` `docx_text` **MemoryError** — a `file_size` gate is bypassed |
| B | deflate stream that ends early / is corrupt (new) | **medium** | short-but-valid prefix → refused; corrupt stream → **exit 1 + traceback, uncaught `zlib.error`**, in the tool *and* in `docx_text` |
| C | 50,000-deep nested element (new) | **medium** | tool rc 0 (50005 chars, 0.06 s); `docx_text` **RecursionError** from depth ≈1000 |
| D | `TargetMode`/traversal inside `docx_text` (bonus) | low | `docx_text` reads the traversing member (`len=20`), the tool refuses — extends erratum E3 |
| H4 | write paths (re-run) | low | **OPEN** — `build-spans` default root writes **and unlinks** the lane; `build-c2-controls` still `mkdtemp` without `dir=` and leaks on exception |
| H5 | `c1-count` scratch lifecycle (re-run) | low | **OPEN** — SIGTERM leaks 1 dir (rc 143); `--work` missing ⇒ rc 1 traceback, not 2 |

Counter replay on the landed bytes — all green, so nothing above is counter-visible: `c1-count.py` → `LEGS=9/9 C1=PASS` rc 0 (`REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682`), `--seed 7` → 9/9 · `c1-supplement.py` → `SUPPLEMENT_LEGS=4/4 C1_SUPPLEMENT=PASS` rc 0 · `c2-count.py` → `C2=PASS` rc 0 in both default and `--lane-only` mode · `build-spans.py --check` → `SPANS_ROWS=38 STALE=0` rc 0.

## 2. H1 — closed on the main part, open on `_rels/.rels`
```
$ python3 run.py 2000000 fx/b1.out python3 $T fx/bomb_1g.docx      # main part declares 1109174566 B
rc=2 elapsed=0.03s maxrss=17572KB stdout=0B
ERR| REFUSED 'word/document.xml' inflates to 1109174566 bytes (limit 268435456)
$ ( ulimit -v 100000; python3 $T fx/lied_256m.docx )                # declares 268435455, really 1.1 GB
REFUSED package too large to render in memory                       # rc 2 — the MemoryError map works
```
The streaming path is bounded by the declaration (`_read1` slices to `self._left`, `zipfile/__init__.py:1216`), so w1's "crash outside the refusal shape" is gone. But `main_part()` calls `z.read("_rels/.rels")` on a size the attacker writes:
```
$ python3 -c "import zipfile;print([(i.filename,i.compress_size,i.file_size) for i in zipfile.ZipFile('fx/rels_lie.docx').infolist()])"
[('_rels/.rels', 268495, 1024), ('word/document.xml', 111, 148)]    # a 268 KB package whose rels is really 276,000,270 B
$ ( ulimit -v 100000; python3 $T fx/rels_lie.docx )   → rc 2 REFUSED package too large to render in memory
$ ( ulimit -v 700000; python3 $T fx/rels_lie.docx )   → rc 2 REFUSED _rels/.rels does not parse: unclosed token: line 1, column 105
$ ( ulimit -v 100000; python3 $T fx/rels_big_truth.docx )
REFUSED '_rels/.rels' inflates to 276000270 bytes (limit 268435456)  # the gate does fire on a truthful declaration
```
It fails safe (refusal), but a 268 KB capture allocates 276 MB first and `bounded()` never applied: `ZipFile.read()` decompresses with `n = max(n, MIN_READ_SIZE) ≈ 2**31−1` in one call and slices afterwards (`zipfile/__init__.py:1197,1216`). Fix (intended path `tools/capture-text.py`, `main_part`): parse the rels through the stream — `rels = ET.parse(z.open("_rels/.rels")).getroot()` after the same `bounded()` call (verified: refuses `rels_lie` at a 100 MB cap; `plain.docx` still yields `Relationships`). The same line closes item A for the rels.

## 3. H2 / H3 — re-run, still closed
```
$ python3 $T fx/laughs9.docx    → rc 2  REFUSED unreadable package: limit on input amplification factor (from DTD and entities) breached
$ python3 $T fx/xxe_extdtd.docx → rc 0  "OK"            # DOCTYPE SYSTEM "file:///etc/hostname"
$ strace -f -e trace=openat,open … fx/xxe_extdtd.docx; grep -E 'hostname|/etc/' fx/xxe.strace
  /etc/ld.so.cache · /etc/localtime only                 # no external fetch
$ python3 $T fx/trav.docx       → rc 2 REFUSED officeDocument target '../../../../etc/passwd' leaves the package root
$ python3 $T fx/trav_ext.docx   → rc 2 REFUSED no officeDocument relationship in _rels/.rels
$ python3 $T fx/enc.docx        → rc 2 REFUSED unreadable package: File '_rels/.rels' is encrypted, password required for extraction
```
Residual from w1 stands: the entity bound is expat's and no receipt pins `sys.version`/`pyexpat.EXPAT_VERSION` (my replay prints the same nine lines, no version line).

## 4. New A — a central directory that declares a small `file_size` for a large member
Fixture: main part of 276,844,113 B, with `file_size` **and** CRC both consistent with the first 1024 bytes, so no CRC error can reveal the lie:
```
$ python3 -c "import zipfile;z=zipfile.ZipFile('fx/lied_crc.docx');print([(i.filename,i.compress_size,i.file_size) for i in z.infolist()], len(z.read('word/document.xml')))"
[('_rels/.rels', 149, 263), ('word/document.xml', 646980, 1024)] 1024        # 647 KB package, silent 1024-byte read
$ ( ulimit -v 100000; python3 $T fx/lied_crc.docx )
rc=2 REFUSED unreadable package: no element found: line 1, column 1024        # bounded, refuses
$ ( ulimit -v 400000; python3 probe1.py fx/lied_crc.docx )                    # build-spans.docx_text
fx/lied_crc.docx: EXC MemoryError: Unable to allocate output buffer.          # dies under a 400 MB cap
$ ( ulimit -v 700000; python3 probe1.py fx/lied_crc.docx )   → OK len=None
```
So the streaming reader is bounded by the declaration; `docx_text`'s `z.read(part)` is bounded by the *real* expansion, and a `file_size` gate does **not** close it — the lie keeps the gate passing while the allocation follows the stream. (`bomb_1g` and `lied_256m` in `docx_text`: `MemoryError` under a 2 GiB cap, `OK len=1074814741` with none — w1's H1 finding, still open, now with the gate-bypass reason.)

## 5. New B — a deflate stream that ends early / is corrupt
```
$ python3 $T fx/deflate_early.docx    # valid deflate prefix, truthful central directory, CRC therefore wrong
rc=2 REFUSED unreadable package: Bad CRC-32 for file 'word/document.xml'      # refused; docx_text → len=None
$ python3 $T fx/deflate_cut.docx      # same length, corrupt block header
Traceback (most recent call last):
  File "…/tools/capture-text.py", line 94, in text_form
    for event, el in ET.iterparse(data, events=("start", "end")):
  File "…/zipfile/__init__.py", line 1197, in _read1
    data = self._decompressor.decompress(data, n)
zlib.error: Error -3 while decompressing data: invalid stored block lengths   # rc=1, 546-byte file
$ python3 probe1.py fx/deflate_cut.docx → EXC error: Error -3 while decompressing data …
```
`zlib.error` is raised inside the generator, i.e. inside `text_form`'s `try`, but is not in the caught tuple (`capture-text.py:115`: `BadZipFile, ET.ParseError, OSError, RuntimeError, NotImplementedError`; `zlib.error` is none of them), so both the claim's "exit 2 + `REFUSED`" shape and the `capture-text` Gates row's exit-code cell are violated. Erratum E2(e) fixed this class for encrypted members and missed it here. Fix (verified on a scratch copy): add `zlib.error` and `EOFError` to that tuple — `deflate_cut` then gives `rc=2 REFUSED unreadable package: Error -3 …` and `plain.docx` still prints `hello`.

## 6. New C — 50,000 nested elements: the tool survives, the builder does not
```
$ python3 $T fx/deep50k.docx | wc -c ; echo rc=$?    → 50005  rc=0   (0.06 s)
$ python3 probe1.py fx/deep50k.docx                  → EXC RecursionError: maximum recursion depth exceeded
$ …docx_text at depth 500 / 900 / 1000 / 50000       → OK len=501 · OK len=901 · EXC RecursionError · EXC RecursionError
$ cd clone && python3 corpus/evidence/round52/build-spans.py --cache ../cache2   # .raw = fx/deep50k.docx for a quoted URL
    walk(child, el.tag)
  [Previous line repeated 991 more times]
RecursionError: maximum recursion depth exceeded                                    rc=1
```
`docx_text`'s `walk()` recurses per element, outside its `try`; `RecursionError` is a `RuntimeError` subclass that tuple never sees. The builder dies instead of writing the row or refusing the quote, and `claims.md`'s "both readers implement the one rule" is false on any document deeper than ~1000 elements — a legal WordprocessingML shape the tool renders. Fix (intended path `corpus/evidence/round52/build-spans.py`, `docx_text`): replace `walk` + `ET.fromstring` with the tool's `ET.iterparse` + tag-stack loop inside one `try`. Verified in scratch: `deep50k` → `len=50005`, byte-equal to the tool; `lied_crc`, `bomb_1g`, `deflate_cut`, `deflate_early` → `None` at a **100 MB** cap; the NIPH capture still `len=19682`, equal to the tool's 19682 chars. That one rewrite closes §4, §5 and §6 for the builder.

## 7. H4 / H5 — re-run, unchanged and open
```
$ git clone -q --shared <lane> clone && python3 -c "…bs.LANE…"
LANE for the lane script = /home/vgpnk/Projects/shokunin/chousa-shokunin        # the --root default, build-spans.py:238
$ touch clone/…/spans/S999-1.txt; rm clone/…/spans/S113-1.txt
$ cd clone && python3 corpus/evidence/round52/build-spans.py → SPANS_ROWS=38 WRITTEN=38 rc=0
  S999-1.txt: No such file or directory (unlinked) · S113-1.txt: restored
$ grep -n "mkdtemp|rmtree" controls/build-c2-controls.py → 35: mkdtemp(prefix=…)   (no dir=) · 52,69: rmtree (no try/finally)
$ ( PKG→nonexistent; TMPDIR=$PWD; python3 ctl.py ) → rc=1 FileNotFoundError; leftover: chousa-r52-c2ctl-staged-nvj5_bmm
$ python3 -c "import tempfile,os; os.environ.pop('TMPDIR',None); print(tempfile.gettempdir())" → /tmp
$ ( c1-count.py --per-leg 40 --work w2 & … kill -TERM $! ) → rc=143, dirs-after-TERM=1 (c1r52-7dau83l_)
$ ( … kill -INT … )                                        → rc=130, dirs-after-INT=0
$ python3 c1-count.py --per-leg 1 --work nope → FileNotFoundError … rc=1         # usage errors are 2 elsewhere
```
`c1-count` never compares `--work` to `LANE` (`LANE` appears only at `:45`, `:248`). Fixes (unchanged from w1): refuse `--root`/`--work` that resolves inside `LANE` without an explicit flag; `mkdtemp(dir=os.environ.get("TMPDIR"))` + `try/finally`; `signal.signal(SIGTERM, …)` raising `SystemExit`; `--work` must exist ⇒ exit 2.

## 8. Claim and Gate text this falsifies
- `SKILL.md:134` (`capture-text`), exit-code cell: the refusal classes are enumerated and a **corrupt deflate stream is not one of them**, yet a 546-byte package yields rc 1 + traceback (§5). Route: fix the tuple, or add the class to the row and to `claims-erratum.md`.
- `SKILL.md:135` (`chousa round-52 counters and checks`), last cell: "read-only on the lane; C1 and the controls write only their own scratch" — `build-spans.py`, listed in the same row, writes `spans.tsv` + `spans/*.txt` **and unlinks** stale `S###-N.txt` under `--root` (default `LANE`) with no `--check` required, and `build-c2-controls.py` leaks its scratch on failure (§7).
- `corpus/QUALITY.md:917` (criterion 90), named limit "the bound is uncompressed bytes per part": the bound is enforced against the *declared* `file_size` on `_rels/.rels` and not at all in `docx_text` (§2, §4). The criterion's own check command still holds (both inputs are refused) — the limit sentence is what to correct.
- `claims.md` "Both readers implement the one rule…": false at depth ≳1000 (§6) and on a traversing `.rels` target (§9), in addition to the External-relationship case already named in E3.
- `claims-erratum.md` E2(e) reports the encrypted/unsupported-compression class closed; the same-shape `zlib.error` was not (§5).

## 9. Named, not scored (extends E3)
`docx_text` takes the first `/officeDocument` relationship with no `TargetMode`, `normpath` or `..` check, so `fx/trav.docx` (member `../../../../etc/passwd`) gives `len=20` where the tool refuses. No C2 capture has such a relationship, and only a zip member is read (no filesystem escape) — low; the tool's two existing conditions close it.

VERDICT — attacked the landed C1 reader, the C2 span builder and the round-52 counters with the wave-1 bomb/entity/traversal set plus a declared-size lie, a truncated/corrupt deflate stream and 50,000-deep nesting: H1/H2/H3 are closed for the tool's main-part path, but the `_rels/.rels` read is still bounded by the attacker's declaration (276 MB from a 268 KB package), `docx_text` is unbounded and crashes (MemoryError, RecursionError, and an uncaught `zlib.error` that also escapes the tool as exit 1 + traceback, falsifying its Gates row), and `build-spans` default-root writes/unlinks the lane while `build-c2-controls` and `c1-count` still leak scratch on failure/SIGTERM; every counter replays green, so none of it is counter-visible.
