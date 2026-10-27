# R54W2SentFinal — hazard review of the round-54 post-freeze scripts

seat: sentinel (leaf, no dispatch) · lane tip `447cf7ed4dc1a3708518b99e9a5e62e177c11ce9`
scope: `corpus/evidence/round54/{c1-supplement.py, controls/build-c1-forge.py,
considerthese-ledger-check.py, pdf-crosscheck.py}` — nothing else; no predicate, target, counter,
control or production file touched, my only write is this file. scratch:
`/fast/scratch/hyaku/chousa-r54/R54W2SentFinal` (removed at exit; `TMPDIR` there,
`PYTHONDONTWRITEBYTECODE=1` on every run). Tooling: nothing installed; `uv run --offline --with pypdf`
hit an existing cache (pypdf 6.21.2, no network); pacman untouched.

Trust boundary under test: the frozen counter's hook (`c1-count.py:66-76`) audits `subprocess.Popen/
os.system/os.exec*/os.fork*/pty.spawn/socket.connect/socket.bind` but **not** `open`, `os.listdir`,
`os.scandir` — so the judge's reference text lives in a filesystem the judged tool can read.

## F1 — CRITICAL — the supplement's "isolation" is not a boundary: oracle echo scores 3/3

Attack: the reference the supplement judges against is written *before* the tool runs, into
`c.work`, and its name is the **isolated doc's own stem** (`c1-supplement.py:72-80`: `oracle()` writes
`oracle-<tag>/<d.stem>.txt`; `judge()` runs the tool afterwards). For RESAVE/HELDOUT the path is
derivable from `argv[1]` alone; for ISOLATED the generation HTML survives at `../../src-iso/*.html`.

```
$ python3 corpus/evidence/round54/c1-supplement.py --tool $S/cheat-tool.py --seed 11 --per-leg 3 --work $S/cheatwork
ISOLATED=PASS 3 docs
RESAVE=PASS 5 resaved captures
HELDOUT=PASS 3 lane files
SUPPLEMENT_LEGS=3/3
SUPPLEMENT=PASS
```
Leg-precise variants (`--seed 11 --per-leg 3`, same work root):
```
$ .../c1-supplement.py --tool $S/cheat-oracleonly.py ...   # reads only ../../oracle-{resave,held}/<stem>.txt
RESAVE=PASS 5 resaved captures
HELDOUT=PASS 3 lane files
SUPPLEMENT_LEGS=2/3
$ .../c1-supplement.py --tool $S/cheat-srconly.py ...      # reads only ../../src-iso/*.html, tags stripped
RESAVE=FAIL ecavt4fmvp.doc oracle line missing '2\u3000规范性引用文件\t1'
HELDOUT=FAIL as3kf2w74e.doc oracle line missing '# Mount-alias (cross-device) boundary (round 14)'
SUPPLEMENT_LEGS=1/3
```
Neither fixture opens the `.doc`. ISOLATED passes because stripping `<...>` also removes the `href`
URL, so the field-code leg stays satisfied. Docstring claim falsified: "copied ALONE … outside the
generation tree (no HTML, no sibling)" (`c1-supplement.py:8-11`) — the directory has no sibling, its
grandparent `c.work` does.

Impact: E1's "0/3 on the supplement" holds for that one forge, not the class; `controls/c1-forge.txt`
is no evidence the supplement discriminates, and `measure-after.txt`'s supplement block cannot carry
the anti-forgery cap E1 assigns it. C1's own verdict (judged on the frozen counter, already disclosed
forgeable) is unaffected — what fails is the *closure claim*.

Smallest remediation: audit reads, not just spawns (draft below). Weaker and insufficient alone:
delete `oracle-<tag>/` after each judge — `open` stays unrestricted.

## F2 — HIGH — the frozen counter's REAL leg is echo-able through the inherited `TMPDIR`

Same defect, different leg, and this one is *inside the frozen rule*. `leg_real` builds
`work/oracle/<pin>.txt` (`c1-count.py:250-256`) and the work dir is `mkdtemp` under `$TMPDIR`
(`:308`); the tool inherits `TMPDIR`, and the pin stem is `argv[1]`.

```
$ TMPDIR=$S/tmp python3 legreal.py            # driver: F.Ctx(cheat2.py,...); F.leg_real(c)
TMPDIR= /fast/scratch/hyaku/chousa-r54/R54W2SentFinal/tmp
(True, '5 captures')
oracle files: ['54fe0734c01f699e735b4b0a.txt', '6dc68fd6b32ce9c8dfcebce8.txt', '74ced3e9311594a8cc3f1f42.txt', 'b539a80218080da56a75b624.txt', 'bdff491a75c6abeda1d9c01d.txt']
```
(`cheat2.py` globs `$TMPDIR/*/oracle/<stem>.txt` and also answers the two `--locate` calls, so REAL's
quote leg is satisfied from the export too.) So REAL — 5 of 6 legs, the leg carrying the LibreOffice
comparison — is forgeable by a tool that never parses a compound file and needs no canned data. E1
discloses the counter as forgeable; this widens the mechanism from "canned exports keyed on pins" to
"read the judge's oracle", which is generic. Frozen: disclose with the mechanism named, do not edit,
because "which tool produced the after-measurement" is what the axis is credited on.

## F3 — HIGH — `TemporaryDirectory(dir=out)` copies the campaign captures into `OUTDIR`

`controls/build-c1-forge.py:57-61`: `out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True,
exist_ok=True)` then `with tempfile.TemporaryDirectory(dir=out)`; the four pinned `.raw` captures are
written into that temp dir (`:61`) and a LibreOffice profile under `tp/prof` (`:62`). `out` is
unvalidated, so the documented call `build-c1-forge.py corpus/evidence/round54/controls` writes
capture bytes and a profile into a tracked lane directory.

```
$ D=<git fixture in scratch>, base commit clean; python3 controls/build-c1-forge.py "$D/controls" & ; kill -9
== git status after SIGKILL:  ?? controls/
== untracked .doc inside the repo: <repo>/controls/tmp2u80ca54/{54fe0734…,6dc68fd6…,b539a802…,bdff491a…}.doc
  (digests 6063a3af…, 46d1866c…, ac0fad62…, d341c133… = the REAL pins)
```
Normal exit leaves `OUTDIR` clean (`ls -A forgeout` → `forge.py` only, 58 573 bytes); the residue needs
one crash/OOM/kill, and a committed residue puts read-only campaign bytes in the lane.

Fix: `TemporaryDirectory(prefix="r54forge-")` (honours `TMPDIR`), keep only `forge.py` in `out`, and
refuse `out` inside `LANE` (`out.resolve()` is not under `LANE.resolve()`) with usage exit 2.

## F4 — MEDIUM — SIGINT leaves a LibreOffice profile behind (rmtree races the dying child)

`c1-supplement.py:164-168`: on any exit the `finally` runs `shutil.rmtree(work, ignore_errors=True)`
while the just-killed `soffice` is still flushing its profile; `ignore_errors` hides the failure.

```
== soffice alive under my TMPDIR: oosplash 1594718 / soffice.bin 1596124 (my profile path)
== SIGINT -> 1593617 ; child_rc=130 ; t+0/t+1/t+3s pgrep my profile: (empty)  <- no soffice survives
== leftover: .../tmp/r54c1s-lwzsmcmb/soffice-profile/ (user/registrymodifications.xcu 8 427 B, user/pack/*)
```
With `TMPDIR` unset the same 20 K lands in `/tmp` (no script hardcodes `/tmp`; `mkdtemp` honours
`TMPDIR`). The 600 s timeout path was **not** reproduced; it shares the `subprocess.run` `except` that
killed the child here, so survival is expected identical, not measured.

Fix: retry the rmtree (0.2 s ×5) and report what remains instead of `ignore_errors`, or keep the
profile in its own `TemporaryDirectory` joined after the doc tree. Same pattern in the frozen counter
(`c1-count.py:326`) — disclose, do not edit.

## F5 — MEDIUM — `considerthese-ledger-check.py` executes ledger cells as filesystem+regex authority

`ct:33` — `f = root / p` then `f.read_text(...)` and `re.search(rx, …)` with both cells taken from
the ledger. Three reproduced consequences:

```
== absolute pointer escapes the lane root
$ printf 'CT-20261026-1\tIMPL\t/etc/hostname::^\tnote\n' > ct/escape/led.tsv
$ python3 considerthese-ledger-check.py --root ct/escape --ledger ct/escape/led.tsv
PROPOSALS=1 ROWS=1 IMPL=1 FMT=0 OPEN=0 OPS=0 BAD=0        rc=0   (pathlib drops root for an absolute p)
== catastrophic regex from the ledger
$ printf 'CT-20261026-1\tIMPL\tpayload.txt::(a+)+$\t…'   payload = 40x'a' + 'b'
$ timeout 10 python3 considerthese-ledger-check.py --root ct/redos --ledger ct/redos/led.tsv
rc=124                                                        (exponential backtracking, single-threaded)
== unbounded read
$ truncate -s 512M ct/big/payload.bin ; pointer payload.bin::ZZZ
FAIL REGEX CT-20261026-1 payload.bin::ZZZ  … rc=1 wall=1.36s maxRSS=1063812kB   (=1.0 GiB for one cell)
```
Also: `ct:17` globs `root/considerthese/2026-*.md`; with the tree absent and an empty ledger it prints
a clean `PROPOSALS=0 ROWS=0 … BAD=0` and exits 0 — a vacuous pass (FIFO pointer, by contrast, is
rejected by `is_file()` before reading: no hang).

Impact: the checker is evidence-of-record for the ledger; one cell can hang the check, allocate 1 GiB,
or validate a regex against any readable file. Fix: contain the path and cap the read (see draft); bound
the regex (reject >128 chars with nested quantifiers, or cap the subject); add a `PROPOSALS==0` guard.

## F6 — MEDIUM — `pdf-crosscheck.py` passes vacuously three ways and is unpinned

`pdf:40-42`: rows are counted only `if sid in ext`; `n` is the count of *matched* rows, so the
denominator is whatever the file happens to contain, and an empty quote is a substring of everything.
Fixture copies of the script + `quotes.tsv` in scratch (`uv run --offline --with pypdf`):

```
baseline (lane quotes.tsv):  PDF_QUOTES=21 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14   rc=0
A one S123 row renamed S124: PDF_QUOTES=21 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14   rc=0   (silently skipped)
B extra S123 row, empty quote: PDF_QUOTES=22 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14 rc=0   (empty quote "occurs")
C header only, zero rows:    PDF_QUOTES=0  NOT_IN_INDEPENDENT=0 RAW_NOT_IN=0    rc=0   (pass, checked nothing)
D row whose quote contains a tab: ValueError: too many values to unpack (expected 4)   rc=1, traceback
```
`pdf:22` pins only the *file name*; no digest guard (contrast `c1-count.py:246-248`), so a replaced
`.qcache` file silently changes what "independent extraction" means. Memory is not a hazard (6.2 MB PDF
→ 38 404 kB peak RSS). Fix: assert `n == count of S123 rows`, reject empty quotes, pin the PDF sha256
with `ENV_CHANGED` exit 2, and catch short/long rows.

## F7 — LOW — two operability gaps (supplement re-run, forge pin discipline)

Re-running `c1-supplement.py` with the same `--work` dies on `src-iso` because legs use `mkdir()`
without `exist_ok` — `FileExistsError: [Errno 17] File exists: '.../rework/src-iso'` (first run rc=0);
`--work` also accepts any path, including a lane directory, and `own=False` means no cleanup.
Fix: `mkdir(parents=True, exist_ok=True)` or refuse a non-empty work dir; refuse `--work` under `LANE`.
`controls/build-c1-forge.py:61,67` hashes whatever bytes sit at `CACHE/<KEY>.raw` and never compares
them to `REAL`'s five pins (no `ENV_CHANGED` exit 2), so a changed cache silently forges different
documents. Fix: copy the pin check from `leg_real`.

## Tested and NOT vulnerable (negatives on record)

- No hardcoded `/tmp` in any of the four; `mkdtemp` honoured my `TMPDIR` (all residue landed there).
- No writes to `~/.config/libreoffice`: dir mtime `2026-10-22 09:32:29`, `find … -newer marker` empty
  after every run; every `soffice` call passes a private `-env:UserInstallation` under work/temp.
- No `soffice` survives SIGINT (`oosplash` + `soffice.bin` gone at t+0) or SIGKILL (none after 3 s);
  `pgrep -af R54W2SentFinal | grep -c soffice` = 0 at the end.
- FIFO pointer: rejected by `is_file()` before any read (no hang).
- Nothing written into the lane by these four: `git status --porcelain corpus/evidence/round54 tools
  corpus/knowledge` empty after all runs (only a sibling's untracked `census-end.txt`).
- `build-c1-forge.py`'s 4 `KEYS` vs 5 `REAL` rows is correct: `74ced3e9…` is a byte twin of
  `54fe0734…` (`c1-count.py:55`), and `CANNED` is keyed on the file digest.

## For integration (drafts; intended paths as labelled — I did not land them)

```python
# corpus/evidence/round54/c1-supplement.py — audit reads too (replaces F.HOOK for its own runs)
HOOK2 = r'''
import os, sys, runpy
ALLOW = tuple(p for p in os.environ["R54_ALLOW_READ"].split(os.pathsep) if p)
BAD = ("subprocess.Popen","os.system","os.exec","os.posix_spawn","os.spawn","os.fork","os.forkpty","pty.spawn","socket.connect","socket.bind")
def deny(w): sys.stderr.write("AUDIT_FORBIDDEN " + w + "\n"); sys.stderr.flush(); os._exit(97)
def hook(ev, args):
    if ev in ("open","os.listdir","os.scandir"):
        p = args[0]
        if isinstance(p,(str,bytes,os.PathLike)) and not os.path.abspath(os.fsdecode(p)).startswith(ALLOW): deny(f"{ev} {p}")
    elif ev in BAD: deny(ev)
sys.addaudithook(hook); tool = sys.argv[1]; sys.argv = sys.argv[1:]; runpy.run_path(tool, run_name="__main__")
'''
# Ctx.run sets R54_ALLOW_READ = doc parent, doc, tool, sys.prefix, sys.base_prefix, the stdlib dir;
# judge() deletes oracle-<tag>/ before running the tool.

# corpus/evidence/round54/controls/build-c1-forge.py — refuse out under LANE; TemporaryDirectory(prefix="r54forge-")
# corpus/evidence/round54/considerthese-ledger-check.py — reject absolute p and (root/p).resolve() outside root;
#   body = f.read_text(encoding="utf-8", errors="replace")[:1_048_576]; fail when considerthese/ is absent
# corpus/evidence/round54/pdf-crosscheck.py — n == S123 row count, reject empty quotes, pin the PDF sha256
```

## Corrections the round's text needs (attack each names)

1. `claims-erratum.md` E1 — "copied alone … no HTML, no sibling" and "0/3 on the supplement": keep the
   receipt, drop the closure claim; F1 shows 3/3 for a non-parsing tool and names why (`open` unaudited).
2. `measure-after.txt` supplement block — measures the landed tool, not the check's power; F1/F2 mean it
   cannot be cited as forgery resistance. C1's verdict on the frozen counter is unchanged.
3. `controls/build-c1-forge.py` docstring line 5 — "writes OUTDIR/forge.py" understates: the four pinned
   captures and a LibreOffice profile also land in OUTDIR while it runs (F3).
4. QUALITY 96 (`pdf-crosscheck` as the independent-extraction leg) — passes with zero rows and with an
   empty quote (F6); cite it with `PDF_QUOTES>=21` and a pinned digest or not at all.

VERDICT: attacked the four post-freeze scripts' trust boundaries — the supplement's isolation claim did
NOT survive (a 20-line tool that never opens the `.doc` scores SUPPLEMENT_LEGS=3/3, and the frozen
counter's REAL leg is echo-able through the inherited `TMPDIR`), the forge builder's temp-dir placement
did NOT survive (pinned captures left untracked inside the caller's directory on SIGKILL), the ledger
checker's cell authority did NOT survive (absolute-path escape, 1 GiB read, unbounded regex), and the
PDF cross-check did NOT survive (three vacuous passes, no digest pin); SIGINT process cleanup (the 600 s
timeout path shares its kill path but was not run), `~/.config/libreoffice` isolation, `/tmp` hardcoding
and lane writes DID survive.
