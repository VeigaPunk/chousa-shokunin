# MutC1ExtraProbe — round 61 w1 — mutation probe of the C1 reference builder

Scope: 22 new mutants of `controls/ref-build-spans.py` (none of them is M01–M14), aimed at
`Forms._probe`, `Forms.get`, `Forms._read` and `_capture_text`. Each mutant is a copy in scratch
with one or two anchored text edits (every anchor asserted to occur exactly once; every copy parses).
The reference and the frozen counter were not edited. Counter run unmodified:
`python3 -B corpus/evidence/round61/c1-count.py --builder <copy> --work /fast/scratch/hyaku/chousa-r61/MutC1ExtraProbe/w/<name> --seed 61001`
(cwd lane root). Reference control: `LEGS=20/20 C1=PASS`, exit 0. Installs/updates: none.

## Findings

1. The frozen counter kills 7 of 22 mutants (D, F, I, J, K, R, T). Of the 15 survivors, 4 are equivalent
   for the counter (G, P, Q, U) and 11 are coverage gaps (A, B, C, E, H, L, M, N, O, S, Y).
2. Most serious gap, A: a cache entry that is a symlink into a *sibling* directory whose name shares the
   cache's string prefix passes containment (`startswith`). The builder reads the file and writes its
   contents into `spans/`. H13 uses an outside file with no shared prefix, so it cannot see this.
3. Gap Y: the cap is applied to the size of the link, not its target. A 70 MiB target behind an in-cache
   symlink is read and written (exit 0) where the reference refuses it (exit 1). No leg reads a link's
   target for size; the cap legs use direct sparse files only.
4. Operability/calibration gaps (not safety): E (in-cache symlink refused), H (symlinked `--cache` path
   refused), S (invalid UTF-8 `.txt` refused, though the docstring says errors are replaced), L (a real
   OLE `.doc` capture is refused; P-legs only test ZIP), B and C (cap boundary and value are not pinned:
   64 MiB exact and 20 MiB are not tested).
5. Hygiene gaps: M, N, O let a refusal or OS error escape as a `Traceback`. Exit is still non-zero and
   nothing is written, so the counter passes. The no-Traceback check exists only in H16/H17.
6. Equivalent for the counter: G (memo store removed; output identical, cost ~3x on a 200-row fixture),
   Q (CAPTURE_TEXT re-exec per DOCX row; output identical), P (restore removed; no later import in the
   process, P03 passes, output identical), U (`exists` for `lexists`; rc and tree identical, only the
   error text differs; no leg reads text).

## Table (seed 61001; "legs failed" from the counter's `LEG` lines)

| Mutant | Edit to ref-build-spans.py | Legs failed | Result |
|---|---|---|---|
| BASE | none (control) | - (20/20) | PASS (control) |
| A-startswith | `commonpath([real, root]) != root` -> `not real.startswith(root)` | - | SURVIVED (gap, safety) |
| B-cap-ge | `if size > MAX_CAPTURE` -> `>=` | - | SURVIVED (gap, boundary) |
| C-cap16 | `MAX_CAPTURE = 64 << 20` -> `16 << 20` | - | SURVIVED (gap, calibration) |
| D-noS_ISREG | `if not stat.S_ISREG(...)` -> `if False:` | H18 (timeout, rc -9) | KILLED |
| E-lstat-kind | `st = os.stat(real)` -> `st = os.lstat(p)` | - | SURVIVED (gap, operability) |
| F-no-realpath | `real = os.path.realpath(p)` -> `real = str(p)` | H13 (leaked) | KILLED |
| G-no-memo | `self.memo[url] = res` -> `pass` | - | SURVIVED (equivalent, cost) |
| H-root-raw | `self.root = os.path.realpath(cache)` -> `str(cache)` | - | SURVIVED (gap, operability) |
| I-cap-after-read | size check moved after `read_bytes()` | H14, H15 (RSS) | KILLED |
| J-head-whole | `head = f.read(8)` -> `f.read()` | H15 (RSS) | KILLED |
| K-no-head | `head = f.read(8)` -> `head = b""` | P02 | KILLED |
| L-no-ole | `head[:8] == OLE or` dropped from the `.raw` dispatch | - | SURVIVED (gap, operability) |
| M-except-valueerror | `except Exception as e:` -> `except ValueError as e:` | - | SURVIVED (gap, hygiene) |
| N-unguarded-stat | `_probe` stat without its `except OSError` | - | SURVIVED (gap, hygiene) |
| O-unguarded-head | raw head read without its `except OSError` | - | SURVIVED (gap, hygiene) |
| P-no-bytecode-restore | `finally: sys.dont_write_bytecode = old` -> `pass` | - | SURVIVED (equivalent) |
| Q-no-ct-memo | `if self.ct is None:` guard removed | - | SURVIVED (equivalent, cost) |
| R-no-crlf-fold | `.replace("\r\n","\n")` removed from TXT decode | P01, P06, H08 | KILLED |
| S-strict-decode | `errors="replace"` removed | - | SURVIVED (gap, operability) |
| T-digest-form | `sha256(b)` -> `sha256(form.encode())` | P01, P02, P06, H08 | KILLED |
| U-exists | `os.path.lexists(p)` -> `os.path.exists(p)` | - | SURVIVED (equivalent in outcome) |
| Y-link-size | `return "ok", st.st_size` -> `os.lstat(p).st_size` | - | SURVIVED (gap, safety) |

Raw counter outputs: `out/<name>.txt` in scratch (deleted at yield); the summary above was tabulated from
the `LEG` and `LEGS=` lines of those files. R and T are seed-dependent in part: the counter draws CRLF
per fixture from the seed.

## Survivor evidence: smallest fixture that separates each gap

Each row was run as `python3 -B tools/build-spans.py --quotes q.tsv --out out --cache cache` in a fresh
fixture (tools/ holds the builder copy and the lane's `capture-text.py`). "REF" is the reference.

- **A** — `cache/<key>.txt` -> `../cache-evil/x.txt` (sibling dir sharing the prefix `cache`), file holds
  `MARK-R61-PROBE` + quote. REF: `rc=1 resolves outside the cache`. A: `rc=0`, marker found in
  `spans/S101-1.txt`. Leak demonstrated.
- **B** — `cache/<key>.txt` of exactly 67108864 bytes (quote then zeros). REF: `rc=0`. B: `rc=1`
  (`over the 67108864-byte capture cap`).
- **C** — `cache/<key>.txt` of 20 MiB. REF: `rc=0`. C: `rc=1` (`over the 16777216-byte capture cap`).
- **E** — `cache/<key>.txt` -> `other.txt` (regular file inside the cache). REF: `rc=0`. E: `rc=1`
  (`not a regular file`).
- **H** — `--cache link` where `link` -> `realcache/` (both real dirs). REF: `rc=0`. H: `rc=1`
  (`resolves outside the cache`).
- **L** — real Word 97 capture `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` (129024 bytes, OLE magic),
  one quote taken from its `capture-text` form. REF: `rc=0`. L: `rc=1` (`no defined text form`).
- **M** — `cache/<key>.raw` = zip with `x.txt` only (no `_rels/.rels`). REF: `rc=1`,
  `capture-text refused ... no _rels/.rels`, no Traceback. M: `rc=1` with `Traceback`.
- **N** — `cache/<key>.txt` -> `nowhere.txt` (dangling). REF: `rc=1`, `unreadable (No such file...)`,
  no Traceback. N: `rc=1` with `Traceback`.
- **O** — `cache/<key>.raw` mode 000 (uid 1000; non-root only, as H17 notes), no `.txt`. REF: `rc=1`, no
  Traceback. O: `rc=1` with `Traceback`.
- **S** — `cache/<key>.txt` holding byte `0xff` outside the quote. REF: `rc=0`. S: `rc=1`
  (`capture-text refused ... invalid start byte`).
- **Y** — `cache/<key(v)>.txt` = 70 MiB of 3-byte CJK characters (23.4 M chars, under the 64 Mi-char form
  cap), `cache/<key(u)>.txt` -> it. REF: `rc=1` (`73400320 bytes, over the 67108864-byte cap`). Y: `rc=0`,
  spans written. Cap bypass demonstrated.

Equivalence checks (REF vs mutant, same fixture, outcome compared on rc, tree hashes, stderr):
- G: three rows, one URL, 16-MiB text: identical outputs. Timing on 200 rows over one 16 MiB text:
  REF 1.2 s, G 3.7 s (INFERENCE: cost is linear in rows; a 60 s counter timeout would need ~4000 rows).
- Q: two DOCX captures, rows alternating: identical outputs.
- P: DOCX row; `tools/` after run is `[build-spans.py, capture-text.py]` for both; identical outputs.
- U: dangling `.raw` with no `.txt`: identical rc and tree, error text differs. Dangling `.raw` with a
  valid `.txt`: identical rc, tree and span hash.

## Reference observation (no mutant; route to L1)

Fixture: `cache/<key>.raw` -> outside valid DOCX (`DOCXSIDE` + quote); `cache/<key>.txt` = `TXTSIDE` + quote.
REF: `rc=0`, span = `TXTSIDE alpha beta gamma delta epsilon tail`. The docstring says a `.raw` symlink
out of the cache is "a refused row, decided before any byte is read". The reference instead falls
through to the `.txt`. The read stays inside the cache, so this is not a leak; it is a documented-behaviour
deviation outside the 20 legs. INFERENCE: intent is the docstring's refusal.

## Limits

- Seed 61001 only, as assigned. R and T are partly seed-dependent (CRLF draws).
- D's kill takes the 60 s FIFO timeout; no other run timed out.
- O is root-blind (H17 precedent): on a root run it would survive trivially.
- Fixtures are the smallest I found, not proven minimal.
- Nothing in the frozen counter, controls, predicates or kill rules was changed; scratch deleted.

VERDICT: KILLED=7/22 survivors_that_are_gaps=11
