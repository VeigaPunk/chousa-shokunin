# R58ExecC1SizeCaps — C1 size/row-bound probe (operability)
Leaf executor, no subagent dispatch. Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`; source reads read-only; only write is this report. Scratch (removed): `/fast/scratch/hyaku/chousa-r58/R58ExecC1SizeCaps/`. No install (no pacman txn; `RULES.md` read first).

## Inputs read
`claims.md`; `c1-count.py` (frozen, 406 lines, read in full `:raw:40-406`); `controls/c1-before.txt`, `c1-controls.txt`, `c1-control-build.txt`; `tools/build-spans.py`; `tools/capture-text.py` (pinned `2c0140bc…2573`); `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` (sha256 `6063a3af…fdf3`, 129,024 B — matches claims). Lane `HEAD`=`5da0a63`, freeze `9e73a03`; `git diff 9e73a03 HEAD -- corpus/evidence/round58/c1-count.py` **empty** ⇒ frozen counter byte-unchanged. `tools/build-spans.py` is still sha256 `1ed2650af…c80bf6`, **byte-identical to the pinned r55 control** (`diff` empty) ⇒ the base builder is unhardened.

## Frozen counters actually run
`python3 -B corpus/evidence/round58/c1-count.py --builder <path> --work <fresh dir>`, `HYAKU_SCRATCH=/fast/scratch/hyaku`, fresh work dir per run. **Run A — base builder:**
    EMPTY_OK=pass / REBUILD_OK=pass / ESCAPE_ENTRY=pass(refused) / HELDOUT_OK=pass
    FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
    SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
    SYMLINK_CACHE=fail(rc=0, expected refusal)
    FIFO_TXT=fail(rc=1, reason [...] absent in '... refused S571: no defined text form ...')
    DEVZERO_TXT=fail(rc=1, reason [...] absent in '... refused S581: no defined text form ...')
    FAT_RAW=fail(rc=1, reason ['SIZE'] absent in '... capture-text refused
      f96cbd6d82dbae8a8e2c6223.raw: ole-malformed: sector shift 0, mini shift 0')
    MANY_QUOTES=fail(rc=0, expected refusal)
    BEFORE_FOREIGN=deleted
    SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
    C1=FAIL          (exit 1)
Reproduces `controls/c1-before.txt` exactly.

## Finding 1 — the current code reaches the parser first, and accepts an oversized *valid* OLE
The frozen `FAT_RAW` fixture is OLE-magic + zeros, so capture-text rejects it as `ole-malformed` — a **parser** refusal, not a size refusal; it never exercises the size path. I built the stronger case the seat item names: a **valid** OLE-headed raw above 64 MiB (real S101 capture bytes, then `truncate()` to 80 MiB — sparse, 128 KiB on disk): apparent 83,886,080 B, `st_blocks` 256, first 8 B = `d0cf11e0a1b11ae1`. **Base builder on that valid 80 MiB OLE — accepted, not refused:**
    rc= 0 elapsed=0.19s maxrss=181.6 MiB
    stdout: QUOTE S551 char 12007 spans/S551-1.txt / SPANS_ROWS=1 WRITTEN=1
    OUT outA/spans/S551-1.txt 445 ; OUT outA/spans.tsv 287
The base reads the whole oversized capture **twice** then parses it:
    strace -e trace=openat,read: total bytes read from the 80MiB raw: 168034304 (160.2 MiB)
(one `raw.read_bytes()` in `Forms.get` + capture-text's own `f.read(MAX_PART + 1)`; `MAX_PART = 256*1024*1024`, `capture-text.py:78`, so 80 MiB sits well inside it). Instrumented base copy (`print` before the parser call):
    PROBE: read_bytes() returned 83886080 bytes; NOW CALLING capture-text parser
    QUOTE S551 char 12007 spans/S551-1.txt
**Yes — the current code reaches the parser first**: the parser is entered with the full oversized payload and the build succeeds. The same instrumented *candidate* never prints the probe line — the refusal happens before the parser is reached. So C1 leg (4) "raw reads are bounded at 64 MiB" is not merely unreached in the base: for a **valid** oversized OLE the base produces output and exits 0. The frozen `FAT_RAW` fixture trips the parser's `ole-malformed` first, so that leg fails for a *reason-label* reason (`SIZE` absent), not because a size bound exists — a finding against the fixture's coverage, not a fix I may make.

## Finding 2 — the 100,001-row quotes.tsv is fully processed; 100,001 span files written
Counter's own generator (`synth_text`/`synth_quotes`, seed 7, `QUOTES_CAP+1` rows of `S900`):
    rc= 0 elapsed=2.19s maxrss=147.9 MiB
    span files written: 100001
    outB tree bytes: 36389311
36 MB output tree, exit 0, no refusal. Base `read_quotes` has no row bound. This is the real shape of the `MANY_QUOTES` leg.

## Proposed safe early bound (patch proposed here only; no lane file edited)
Both bounds are checked **before** any capture bytes are read and before any output is written. (a) 64 MiB capture cap — stat first, then a hard bounded read. `SIZE_CAP = 64*1024*1024`.
    def _over_size(path):
        try: st = os.stat(path)          # follows symlinks: bound is on bytes really read
        except OSError: return None
        if st.st_size > SIZE_CAP:
            return f"{path.name} is {st.st_size} bytes, over the {SIZE_CAP}-byte size cap (SIZE)"
        return None
    def _read_capped(path):              # hard bound: a file that grows is still refused
        with path.open("rb") as f: data = f.read(SIZE_CAP + 1)
        return None if len(data) > SIZE_CAP else data
The `read(SIZE_CAP + 1)` is the *hard* bound: never more than `SIZE_CAP` bytes are held; `(SIZE)` is inside the counter's reason class. (b) 100,000-row quotes.tsv cap — counted streaming, before the table is materialised. `QUOTES_ROW_CAP = 100_000`; `QUOTES_BYTE_CAP = 64*1024*1024` (my addition, to make the row count cheap to reach).
    st = os.stat(path)
    if st.st_size > QUOTES_BYTE_CAP: refuse (SIZE)
    with path.open("r", encoding="utf-8") as fh:
        fh.readline(); n = 0
        for line in fh:
            if line.strip():
                n += 1
                if n > QUOTES_ROW_CAP: refuse(f"{path} has more than {QUOTES_ROW_CAP} data rows (ROWS)")
Counting during the read keeps the oversized table from being materialised at all; `ROWS` is inside the counter's `MANY_QUOTES` reason class `["SIZE","ROWS","CAP"]`. Candidate behaviour:
    CAND2 rows=100000: rc=0 spanfiles=100000 stderr=''
    CAND2 rows=100001: rc=2 spanfiles=0 stderr='... more than 100000 data rows (ROWS)'
    CAND2 on VALID 80MiB OLE: rc=1 maxrss=19.5 MiB
      stderr: refused S551: f96cbd6d82dbae8a8e2c6223.raw is 83886080 bytes, over the
              67108864-byte size cap (SIZE)   -> spans written: NONE
Refuses **before** the parser (instrumented probe line absent) and never writes. Isolated measurements, same fixtures:
    BASE  rc=0 peak_child_rss=181.9 MiB   (accepted; wrote spans.tsv + S551-1.txt)
    CAND3 rc=1 peak_child_rss=18.3 MiB    (refused; wrote nothing)
    MANY_QUOTES base  rc=0 span_files_written 100001 peak_child_rss=149.2 MiB
    MANY_QUOTES cand3 rc=2 span_files_written 0     peak_child_rss=19.6 MiB
**No regression on real lane data** — candidate output byte-identical to base (spans.tsv, every span file, stdout, stderr) on all five real quote tables in the lane:
    round58/c2 files=13 IDENTICAL=True ; round56 files=24 True ; round55 files=20 True
    round57/c3 files=11 True ; round54 files=34 True ;  ALL IDENTICAL: True
Counter with the candidate (size/row legs only; the other legs are another seat's surface):
    FAT_RAW=pass(refused) / MANY_QUOTES=pass(refused) / ESCAPE_ENTRY=pass(refused)
    SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
    C1=FAIL
Both size/row legs flip `fail` → `pass(refused)`; the counter still prints `C1=FAIL` (Finding 3). Symlink-to-large-file variant (200 MiB regular file behind an absolute symlink):
    base:  rc=1 'refused S611: quote occurs 209715200x in d443f8c...txt: 'A''
    cand3: rc=1 'refused S611: d443f8c2007dd54859e0e5fd.txt is 209715200 bytes, over the
                  67108864-byte size cap (SIZE)'
The base admits the symlinked path into its read path; the candidate refuses it by size.

## Finding 3 — the frozen counter's verdict can never be `PASS` (counter defect, not builder defect)
`c1-count.py:51-52` define `PASS = "pass"`, `FAIL = "fail"` (lowercase). Every refusal-leg string uses `{PASS}` — `expect_refuse` at `:160` returns `f"{name}={PASS}(refused)"`; explicit appends at `:223` (`FOREIGN`) and `:234` (`SYMLINK_OUT`) likewise; `:315` (`ESCAPE_ENTRY`) is a literal lowercase `"pass(refused)"`. But the aggregation at `:391` is
    ref_pass = all(("=PASS" in l) for l in ref_legs)
and the summary at `:399` uses `'=PASS' in l` — uppercase. No refusal-leg string can ever contain `"=PASS"`, so `ref_pass` is a constant `False` and `SUMMARY REFUSE` a constant `0/7`, whatever the builder does. Proven by a reference builder satisfying **all seven** refusal predicates and all four safe legs (guards: `--out` symlink, cache symlink, FIFO/device `NOT_REGULAR`, 64 MiB raw cap, 100,000-row quotes cap, foreign-span refusal before orphan deletion). Frozen counter output:
    EMPTY_OK=pass / REBUILD_OK=pass / HELDOUT_OK=pass / ESCAPE_ENTRY=pass(refused)
    FOREIGN=pass(refused) / SYMLINK_OUT=pass(refused) / SYMLINK_CACHE=pass(refused)
    FIFO_TXT=pass(refused) / DEVZERO_TXT=pass(refused) / FAT_RAW=pass(refused)
    MANY_QUOTES=pass(refused)
    BEFORE_FOREIGN=deleted / CONTROL_REFUSEALL=denied / CONTROL_build-spans-r55=denied / DENIED=2/2
    SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
    C1=FAIL
All eleven legs read `pass`; the verdict is still `FAIL`. Executing the frozen aggregation block standalone against that leg set gives `verdict=FAIL ok_pass=True ref_pass=False`. **Consequence for the L1:** the frozen target "`c1-count.py` must print `C1=PASS` and exit 0" is unreachable by any builder, including a perfect one. `C1=FAIL` from this counter is therefore not evidence that a builder is unhardened, and `REFUSE=0/7` is not evidence that the refusal legs failed. The per-leg strings (which do discriminate) are the usable signal. I did not edit the counter; this is a finding against it. Two further counter observations, confirmed by running it (independently corroborated by `R58ScribeC1PatchNotes`, whose line anchors differ but whose claims are identical): (i) `CONTROL_REFUSEALL=denied` is **denial-by-crash** — `c1-count.py:212` writes `out-empty/spans/S777-1.txt`, but `out-empty/spans/` is created only by a *successful* `EMPTY_OK`, so an always-refusing builder never creates it and the counter dies before printing any `C1=` line (observed `FileNotFoundError: .../work/refuseall/out-empty/spans/S777-1.txt` at `c1-count.py:212`; the control sub-run then sees no `C1=` line and records `denied`). (ii) `SYMLINK_OUT` is non-discriminating: `expect_refuse` receives `forbidden_touch=[real/'spans.tsv']`, a path that cannot pre-exist, and `:233-237` overwrites `legs[-1]` with `SYMLINK_OUT=pass(refused)` regardless; a builder writing *through* the link yields `SYMLINK_OUT=pass(refused)(target-dir-written!)`. The annotation is not read by the verdict, and neither string contains `"=PASS"`.

## Findings against the frozen claims/counter (reported, not fixed)
1. C1 leg (4) "raw reads are bounded at 64 MiB" — **not implemented in the base**, and the frozen `FAT_RAW` fixture cannot detect its absence (a malformed OLE is refused by the parser first). A *valid* oversized OLE is accepted by the base (rc=0, output written, 160.2 MiB read).
2. C1 leg (5) "quotes.tsv is bounded at 100,000 rows" — **not implemented in the base**; 100,001 rows are fully processed into 100,001 span files.
3. The frozen predicate's `C1=PASS` is unreachable (Finding 3). Either the case-sensitive comparison at `:391`/`:399` or the lowercase leg formatting must change; both are the L1's call, and the counter is frozen so I made no change.
4. `c1-count.py:212` crashes on an early-refusing builder, making `CONTROL_REFUSEALL=denied` vacuous.

## Risks, limits, what I did not do
Scope: size/row bounds only (the seat item). `FOREIGN`, `SYMLINK_OUT`, `SYMLINK_CACHE`, `FIFO_TXT`, `DEVZERO_TXT` still fail on the base and are another seat's surface; my candidate does not claim them. My reference builder (Finding 3) implements all of them, as a counter test vehicle only. The bound is a size/row bound: it does not bound text-size classes more generally, does not close the `--out` symlink race, and does not address broader races — the claim does not claim those. `_over_size` + `read(SIZE_CAP+1)` bounds bytes, but a file replaced between stat and open is not identity-pinned; a same-size substitution between the two reads is not detected. No live target fetched; all fixtures synthetic and in scratch; lane captures read-only. Unrun: no build/lint/test gate (not this seat's scope; parent owns post-integration gating). No lane file edited, no git/jj mutation, no commit, no push.

VERDICT: The current code reaches the parser first — a valid OLE-headed raw above 64 MiB is read twice (160.2 MiB) and **accepted** with output written (base rc=0, 181.9 MiB RSS), and a 100,001-row quotes.tsv is fully processed into 100,001 span files. A proposed early bound (64 MiB stat + hard `read(SIZE_CAP+1)` on captures; 100,000-row streaming count with a 64 MiB byte pre-check on quotes.tsv) flips both frozen legs `FAT_RAW` and `MANY_QUOTES` to `pass(refused)`, refuses before the parser is entered, writes nothing, and is byte-identical to base output on all five real lane quote tables. **However** the frozen counter's `C1=PASS` is unreachable by any builder (lowercase `PASS="pass"` leg strings vs. uppercase `"=PASS"` comparison at `c1-count.py:391`/`:399`), proven by a reference builder satisfying all eleven legs that still prints `C1=FAIL` with `REFUSE=0/7`. The size/row hardening **survives** as a builder change; the frozen C1 predicate as written is **falsified** — it cannot measure the claim it is supposed to measure, and its `FAT_RAW` fixture additionally under-covers the hazard (malformed-OLE refusal masks the absent size bound).
