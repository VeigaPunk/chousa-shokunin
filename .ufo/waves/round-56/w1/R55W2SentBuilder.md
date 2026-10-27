# R55W2SentBuilder — hazard review of round-55 C1 `tools/build-spans.py`

Seat R55W2SentBuilder (leaf, no dispatch). Target `tools/build-spans.py` at rev `29cfb12abd70f688b48c0d17f31e636f2d81104a` (`1ed2650a…c80bf6`, byte-identical to
`46e1758f`'s copy) and `tools/capture-text.py` (`2c0140bc…e2573`); no lane file edited. Each fixture is my own `example.invalid` URL (`key = sha256(url)[:24]`)
with bytes I wrote, nothing from the campaign cache. Scratch `$S=/fast/scratch/hyaku/chousa-r56/R55W2SentBuilder` (removed at exit), `PYTHONDONTWRITEBYTECODE=1`
except the pycache probe; one child per measured run (`$S/run.py`), peak RSS = its `ru_maxrss`, baseline (one `.txt`, one row) 19.6 MiB.

| case | hazard | exit | wall | peak RSS | write/destroy outside `--out` |
|---|---|---|---|---|---|
| h1/hcoll | `--out` holds another round's spans (hcoll = the real round-55 dir) | 0 | 0.12 s | 19.6 MiB | h1 loses files **inside** `--out`; hcoll **destroys 19 committed spans + manifest** |
| h2 | `out/spans` symlink → dir | 0 | 0.17 s | 19.6 MiB | **unlink + create in the link target** |
| h3 | span file and `spans.tsv` are symlinks | 0 | 0.12 s | 19.6 MiB | **truncated both link targets** |
| h4a/b | docx bomb, 64 / 250 MiB form (64 / 249 KiB `.raw`) | 0 | 0.67 / 1.37 s | 197 / **759 MiB** | no |
| h4e | 6 URLs × 250 MiB form (1.5 MB on disk) | 0 | **20.18 s** | **2008 MiB** | no |
| h5e/f | `.txt` 1 GiB · `.raw` 1.5 GiB OLE-magic | 0 / 1 | 4.36 / 3.74 s | **3092 / 1814 MiB** | no (`.raw` refused) |
| h5a/b/c | `.txt` FIFO · `.txt`→/dev/zero · `.raw`→/dev/zero | 1 | ≤0.12 s | 19.4 MiB | no, no hang |
| h5d | `.txt` symlink → file outside the cache | 0 | 0.12 s | 19.6 MiB | no; **its bytes+digest enter the manifest** |
| h6a/b | 100 000 rows, 4 KiB / 1 MiB form | 0 | 8.58 / **31.48 s** | 192 / 193 MiB | 100 000 files, 32.9 MB in `--out` |
| h7a-f | entry `../..`, `/etc/…`, `a/../b`, `..hidden/x`; quote U+2028 | 2/0/2 | ≤0.22 s | 19.6 MiB | no — guarded, inert |
| h8/h9 | `--out` is a file; `.raw`/`.txt` unreadable | 1 | ≤0.22 s | 19.9 MiB | no — traceback, not exit 2 |
| h11 | `spans.tsv` is a directory | 1 | 0.12 s | 19.9 MiB | **orphans already unlinked, nothing written** |
| trace | clean zip run, all write syscalls | 0 | — | — | **`tools/__pycache__/capture-text…pyc`** |

## 1. `--out` is trusted; `spans/` and span files are not checked for links

`main()`: `sd.mkdir(parents=True, exist_ok=True)` → **unlink every `spans/S###-N.txt` not in this run's rows** (`:202-205`) → write `spans.tsv` (`:206`) → span
files (`:208`). Nothing inspects what was already there.

    # h1     in: S404-9.txt(34) S405-1.txt(21) S406-2.txt.bak(37) README.txt(12) spans.tsv(110) — exit=0
    #        out: S404-9 gone, S405-1 gone, .bak + README kept, spans.tsv 110→243
    # hcoll  in: spans=19 tsv=aa73b1e4… tsvlines=20 → out: spans=1 [S001-1.txt] tsv=83ccac31… tsvlines=2, exit=0
    $ git -C <lane> ls-tree --name-only 29cfb12 corpus/evidence/round55/spans/ | wc -l → 19
    # h2     victim/S404-9.txt(28) before → absent after; victim/S001-1.txt(457) created; exit 0, stderr empty
    # h3     victim/IMPORTANT.txt 10→457 B, victim/LEDGER.tsv 74→243 B (both targets truncated); exit 0
    # h11    S888-1.txt unlinked, then IsADirectoryError on spans.tsv → exit 1, nothing written

`--check` is honest on an intact tree (reduced quotes file: `SPANS_ROWS=1 STALE=38`, exit 1, nothing rewritten), so the loss is detectable only *before* the
next build. **Smallest guard:** refuse when `--out` holds a `spans.tsv` whose rows differ from this run's (`return 2`, `--check` exempt); refuse when
`sd.is_symlink()`, `(out/"spans.tsv").is_symlink()` or `sd.resolve().parent != out.resolve()`; write span files, then `spans.tsv` via `.tmp` + `os.replace`,
unlink orphans **last**, and open span files with `O_NOFOLLOW`.

## 2. Memory is bounded per part, not per run

`Forms.get` reads the whole file just to digest it (`b = raw.read_bytes()` `:80`, `b = txt.read_bytes()` `:86`) and keeps `memo[url] = form`; there is no size
check, and `MAX_PART = 256 MiB` (`capture-text.py:78`) applies only after the bytes are materialised.

    # h5f .raw = OLE magic + padding, 1 610 612 736 B   exit=1 maxrss=1813.9 MiB
      refused S001: capture-text refused ca234aaf….raw: OLE file larger than 268435456 bytes
    # h4b 249 KiB deflated docx, declared 262 144 000 B (under MAX_PART)  exit=0 maxrss=758.9 MiB  char 262144000
    # h4e six such captures in one quotes file          exit=0 wall=20.18s maxrss=2007.7 MiB (1.5 MB input)
    # h4c declared 314 572 954 B                        exit=1 maxrss=22.3 MiB (… inflates past 268435456)

A part may be 256 MiB, the parse costs ~3× it, `memo` multiplies that by URL count, and raw/`.txt` bytes are read whole *before* any cap (1.5 GiB OLE → 1.8 GiB)
— on a shared 30 GiB host a 0.1 s run becomes an OOM kill. **Smallest guard:** `st = (raw if raw.exists() else txt).stat(); if st.st_size > 64 << 20: refuse`
(the cache's largest `.txt` is 15 444 093 B, largest `.raw` 39 947 105 B, so nothing real is refused), plus `if len(form) > 64 << 20: refuse` and a bounded
`memo`.

## 3. FIFO and device captures: refused, but the receipt is false

    # h5a mkfifo .txt · h5b .txt→/dev/zero · h5c .raw→/dev/zero → exit=1, 19.4 MiB, ≤0.12 s
    build-spans: refused S001: no defined text form for bbc267db… (raw neither OLE nor zip, no .txt)

No hang, no read: `Path.is_file()` is false for a FIFO and a char device, so `elif txt.is_file()` (`:85`) never opens them — neutralised by accident, with a
false receipt (a `.txt` exists; it is not a regular file). **Smallest guard:** `stat.S_ISREG(os.stat(p).st_mode)`, reason `… is not a regular file`.

## 4. A `.txt` that points anywhere is read, digested and copied

    # h5d cache/<key>.txt → $S/outside/SECRET-on-lane.md ; exit=0 ; QUOTE S001 char 35 spans/S001-1.txt
    $ cat cases/h5d/out/spans/S001-1.txt → "# unrelated file outside the cache" + 药品临床综合评价应当以人民健康为中心
    $ cut -f3 cases/h5d/out/spans.tsv → 5abb17868e44bc110c1b817f85cc2580c6a1d69d9fffa1c6b08cfb1722ef1290 (digest of that outside file)

`capture_sha256` is "the digest of the file read", and here that file is not a capture: content from outside the cache is copied into `--out/spans/` and stamped
as the document's digest. Legal under the frozen predicate (a symlinked `.txt` is a `.txt`) — a provenance hole, not a violation. **Smallest guard:** require
`os.path.realpath()` to sit inside `cache.resolve()` with basename `<key>.txt`/`.raw`, else `refused …: capture outside the cache`; better, add a `capture_file`
column.

## 5. Row count × form size, twice per row

    # h6a form 4096 B      exit=0 wall=8.58s  maxrss=191.6 MiB   ┐ files=100000 bytes=32902851
    # h6b form 1 048 576 B exit=0 wall=31.48s maxrss=193.3 MiB   ┘ same 100 000 rows, 100 000 files

Each row scans the form twice — `text.count(quote)` (`:135`) then `text.find(quote)` (`:139`) — so ~2.2 h for 100 000 rows against h4b's 250 MiB form
[INFERENCE: arithmetic from the measured rates, not run], and one `spans/` takes 100 000 entries that every later `sd.iterdir()` (`:178`) pays for. **Smallest
guard:** one scan (`off = text.find(quote)`; unique iff `text.find(quote, off + len(quote)) < 0`); refuse quotes files over a row cap (exit 2 — refusal, not
truncation); cap span files per `spans/`.

## 6. Guards that held; two exit-code and one parsing gap

`entry` traversal is refused up front (`:116`, exit 2 `must be lane-relative`) for `../../../../etc/cron.d/x`, `/etc/cron.d/x`, `corpus/../SCORECARD.md`;
`entry` is only written as a cell (`:149`), so this is defence in depth, and `..hidden/x.md` builds inertly. What bites is `str.splitlines()` (`:99`), which
also splits on U+2028, U+0085, \x0b, \x0c, \x1c-\x1e: such a quote is unrepresentable and the failure reads `need 4 non-empty tab cells, got 3` (h7e, h7f) — a
column error for a well-formed row; split `\r\n`-normalised text on `\n` and name the real problem per cell. Two exit-code gaps: `--out` a file raises
`NotADirectoryError` (h8), an unreadable capture `PermissionError` (h9, h9b) — exit 1 with a traceback where the docstring reserves 2 for usage/env; wrap the
`mkdir` and both read sites → `refused <id>: unreadable capture (<e.strerror>)` / `return 2`.

## 7. One write outside `--out`, and the default cache

    $ env -u PYTHONDONTWRITEBYTECODE strace -f -qq -e trace=openat,mkdirat,unlinkat,renameat2,renameat,rename -o m/trace-zip.txt \
        python3 pyc2/tools/build-spans.py --quotes cases/h4a/quotes.tsv --out cases/h4a/out3 --cache cases/h4a/cache
    openat(… "cases/h4a/out3/spans/S001-1.txt", O_WRONLY|O_CREAT|O_TRUNC…) = 4 ; same for "…/out3/spans.tsv" = 4
    openat(… "__pycache__/capture-text.cpython-314.pyc.1406730…", O_WRONLY|O_CREAT|O_EXCL…) = 4; rename(… → capture-text.cpython-314.pyc) = 0
    # no write-intent open under /home, /tmp, /dev, /var anywhere in the trace

`_capture_text()` (`:59`) execs `capture-text.py` via `importlib`, writing a `.pyc` into the **tool's own directory** on every OLE/zip run: a write outside
`--out`, permitted by C1's hook and hidden from `git status` by `.gitignore:2`; set/restore `sys.dont_write_bytecode = True` around `exec_module`. Separately
`DEFAULT_CACHE` (`:35`) points into the campaign cache, which the frozen predicate forbids opening, so omitting `--cache` exits 97 under the gate; make
`--cache` required.

## Assessment

No round-55 C1 clause is falsified: refusals still write nothing, the legs' semantics are untouched, and the tool imports no `os`/`subprocess`, so it fits the
round-56 gate's added `_posixsubprocess.fork_exec`/`os.chdir` hooks. Destructive and unbounded is the tool when its inputs are not the counter's: one wrong
`--out` erases a committed manifest and 19 span files at exit 0; a symlinked `spans/` or span file writes outside `--out`; 249 KiB of deflated capture costs 759
MiB (2.0 GiB for six); 1 GiB of `.txt` costs 3.1 GiB; 100 000 rows cost 31.5 s against 1 MiB. Severity: the `--out` clobber and symlinked-output writes are
exploitable (evidence integrity, arbitrary overwrite); the memory cases are availability hazards; the `.txt` symlink is a provenance hole.

VERDICT: attacked round-55 C1 `tools/build-spans.py` (`1ed2650a…`) with 26 fixtures — `--out`-driven deletion of committed spans and manifests, symlinked
`spans/` and span files, zip bomb (759 MiB, 2.0 GiB), 1.5 GiB OLE, 1 GiB `.txt`, FIFO and `/dev/zero` captures, 100 000-row quotes, `..` entries, U+2028 quotes,
unreadable captures, write-time failure ordering, and a syscall trace — the frozen predicate survives (no refusal writes, no spawn, no `chdir`); the tool's
operability does not: destructive `--out`, writes outside `--out`, unbounded memory and time all reproduce.
