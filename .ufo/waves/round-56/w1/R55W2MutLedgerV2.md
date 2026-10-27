# R55W2MutLedgerV2 — attack of round-55 `considerthese-ledger-check.py`

Target: `corpus/evidence/round55/considerthese-ledger-check.py` (claims: pointer resolves inside
--root; >1 MiB refused before read; regex cell ≤128 chars and no nested quantifier; missing
considerthese/ or zero proposals exits 1; ids for every bullet under `## Self-improvement proposals`).
Method: scratch fixtures only under `/fast/scratch/hyaku/chousa-r56/R55W2MutLedgerV2/` (removed at end);
the lane script was only ever **read** (sha256 `2be71524…91673` before all probes == after, re-verified
post-run). Python 3.14.8. Each run: `python3 <checker> --root <fixture>/root --ledger <fixture>/ledger.tsv`.

## Receipt `corpus/evidence/round55/considerthese-ledger-check.txt` reproduces — YES (all 5 lines rerun)

| receipt line | rerun observed |
|---|---|
| `PROPOSALS=35 ROWS=35 IMPL=24 FMT=9 OPEN=1 OPS=1 BAD=0` exit=0 | identical, exit=0 wall=0.09s |
| `[absolute pointer /etc/hostname::^]` → `FAIL POINTER CT-20261026-1 /etc/hostname` exit=1 | identical, exit=1 |
| `[regex cell (a+)+$ on 40a+b]` → `FAIL REGEX …(a+)+$` exit=1 | identical, exit=1 (instant; heuristic `\([^)]*[+*][^)]*\)[+*{]` matches `(a+)+$`) |
| `[512 MiB pointer target]` → `FAIL SIZE` exit=1 maxRSS_children=15848kB | `FAIL SIZE CT-20261026-1 payload.bin`, exit=1, wall=0.13s, child maxRSS=16040kB (sparse file, st_blocks=0) |
| `[no considerthese/ tree, empty ledger]` → `USAGE considerthese/ is absent` exit=1 | identical, exit=1 |

## Fixtures: exit code / wall time / outcome

| probe | observed | verdict |
|---|---|---|
| BASE healthy (1 bullet, IMPL `payload.txt::^a`) | exit=0, 0.03s, `BAD=0` | baseline sound |
| F1a pointer target is symlink → /etc/hostname | exit=1, 0.03s, `FAIL POINTER … payload.txt` | killed (resolve()+is_relative_to holds) |
| F1b pointer via dir symlink `outside` → /etc | exit=1, 0.04s, `FAIL POINTER … outside/hostname` | killed |
| F1c **proposal .md itself is symlink to file outside root** | exit=1, 0.04s, `FAIL MISSING CT-20260202-1` `PROPOSALS=1 ROWS=0` — id CT-20260202-1 was minted from bytes of a file outside the root | **SURVIVED** (unrooted read, see E3) |
| F2 pointer `a/../../etc/hostname` | exit=1, 0.04s, `FAIL POINTER` | killed |
| F3a regex `(a|a)+$` vs `a`×24+`b` | exit=1 after **2.04s**, then correct `FAIL REGEX` | latency DoS; eventually correct |
| F3b regex `(a|a)+$` vs `a`×28+`b` | **no output, killed at 15s timeout** | **SURVIVED** (E1) |
| F4 regex `(a|aa)*c` vs `a`×40+`b` | **no output, killed at 15s timeout** | **SURVIVED** (E1) |
| F5 regex `(.*a){20}` (heuristic control) | exit=1, 0.03s, `FAIL REGEX` refused before execution | killed (heuristic catches quantifier inside parens) |
| F6a 1 MiB+1 byte target, rx `^` | exit=1, 0.05s, `FAIL SIZE`, maxRSS 15776kB | killed |
| F6b exactly 1 MiB target, rx `^` | exit=0, 0.05s, `BAD=0` (file read) | contract-consistent ("over 1 MiB" refused; exact 1 MiB read) |
| F7 **file grows between stat and read** (target atomically swapped 1 B ↔ 8 MiB at ~1e6 links/s; 80 checker runs) | **21/80 runs** stat'ed the 1-byte file then read the 8 MiB body: exit=0 `BAD=0`, child maxRSS 32032–32536kB (baseline small/big-at-stat runs: 16060kB / `FAIL SIZE`) | **SURVIVED** (E2) |
| F8 ledger row with 5 columns | exit=1, 0.03s, `FAIL COLUMNS CT-20260101-1` | killed |
| F9a real bullet + bullet under `## Notes` | exit=0, `PROPOSALS=1` — the `## Notes` bullet gets no id, needs no row | **SURVIVED** (E4a, undercount) |
| F9b bullet under `## Self-improvement proposals (archived)` | exit=0, `PROPOSALS=2` — lenient `line.startswith("## Self-improvement proposals")` counts the archived section too | E4b, overcount (fail-closed direction) |

## Escapes that work

- **E1 regex DoS through the nested-quantifier heuristic.** `\([^)]*[+*][^)]*\)[+*{]` requires a
  quantifier char *inside* the group; alternation-duplicated units have none. Verified pre-flight:
  `(a|a)+$` len 7 → heuristic_catches False; `(a|aa)*c` len 8 → False (vs `(.*a){20}`/`(a+)+$` True).
  Both pass the ≤128-length gate and reach `re.search`, which then backtracks exponentially:
  standalone timings `(a|a)+$`: n=20 0.37s, n=24 5.14s, n=28 >8s; `(a|aa)*c`: n=30 0.58s, n=40 >8s.
  Through the checker (payloads `a`×n+`b`): exit=1 at 2.04s (n=24), killed-with-no-output at 15s
  (n=28 and n=40). The gate is hangable to arbitrary wall time by a 128-char-or-less ledger cell —
  denial of service, not a false pass.
- **E2 SIZE gate is TOCTOU-racy: `f.stat().st_size` then `f.read_text()` re-opens the path.**
  21/80 checker runs against an atomic-swap writer passed the size check on the 1-byte inode and
  read the 8 MiB body to EOF (`read_text` is unbounded by the stat'ed size), printing `BAD=0`
  exit=0. Fix shape: open once, `fstat` the fd, read that fd.
- **E3 proposal scan is unrooted.** Pointer files are resolve()-contained (F1a/F1b killed), but the
  `considerthese/*.md` scan `f.read_text()`s whatever the glob yields, symlinks followed: a
  proposal file symlinked outside the root had its bullets minted into ids (`CT-20260202-1` from
  outside bytes). Exit stays fail-closed on a mismatched ledger, but id/uptake counts are
  controllable from outside-root content.
- **E4 heading semantics.** (a) a bullet filed under any other `## ` heading vanishes from
  `PROPOSALS` and needs no ledger row while the run exits 0 — uptake tallies silently undercount;
  (b) conversely the `startswith` heading match counts `## Self-improvement proposals (archived)`.
  (a) is arguably in-contract ("bullets under a `## Self-improvement proposals` heading") but is a
  real coverage hole for the stated purpose "uptake is cited by id".

Killed as claimed: symlinked/dir-symlink/`..` pointer escapes, `(.*a){20}` and `(a+)+$` regex
refusals, 1 MiB+1 and 512 MiB size refusals, 5-column rows, absent tree and zero-proposal exits.

## Restoration

`sha256sum corpus/evidence/round55/considerthese-ledger-check.py` after all probes:
`2be7152465f491c84315aa7b434db7c2ed8c5c0f4f22a78160ddd96181a91673` — identical to the pre-probe
hash; the lane file was never opened for write. Scratch (fixtures, drivers, 8 MiB/512 MiB payloads)
removed below; no writes outside this report and the scratch.

VERDICT: attacked round-55 considerthese-ledger-check.py — 4 escapes survived (regex DoS via
`(a|a)+$`/`(a|aa)*c` heuristic miss, stat→read TOCTOU bypassing SIZE 21/80, unrooted symlinked
proposal read, heading undercount); pointer/size/column/tree guards and all 5 receipt lines held;
receipts reproduce.
