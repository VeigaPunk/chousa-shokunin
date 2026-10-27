# R57W1LabSpacing — probing the c2 UNREACHABLE spacing leg with synthetic records

seat R57W1LabSpacing (labrat, leaf) · 2026-10-27 · lane chousa
target: **R57-C2** `corpus/evidence/round57/c2-count.py`, the UNREACHABLE verdict leg only.
frozen counter sha256 `d6885bae2e8485e28f7d6e1fa59de7a0b3639ee0a242c71baf4c8ba753cb35f9` — **never
edited**; lane copy and scratch copy byte-identical, re-checked before every run.

**Method.** Scratch clone of the lane (`$S/clone`, `git clone --no-hardlinks`) with the four pending
captures **removed** from the store, plus synthetic `refetch.tsv` rows generated programmatically
(UTC stamps from base epoch `2026-10-27T09:00:00Z` + integer offsets). The frozen counter is then
run **unmodified** against the clone (`--root <clone> --verbose`) and its per-id `CAPTURE` line read.
No network fetch: every byte came from the committed lane store. Lane write: this report only.

## Per-case verdicts (counter `CAPTURE` lines, verbatim)

| # | carrier | synthetic attempt shape (offsets from 09:00:00Z) | counter verdict line |
|---|---------|----------------------------------------------------|----------------------|
| 1 | S100 | two failures **599 s** apart: fail@0, fail@599 | `S100 b539a80218080da56a75b624 pin=46d1866ce9af MISSING` |
| 2 | S103 | two failures **600 s** apart: fail@0, fail@600 | `S103 02aefcf570a7108e699d0990 pin=32a5907e701f UNREACHABLE 2 failed attempts` |
| 3 | S105 | three failures, only **first&last** >=600 s: fail@0, fail@300, fail@700 (gaps 300 s, 400 s) | `S105 e3ca8f4fdd15420b80096a75 pin=2197abe27dad UNREACHABLE 3 failed attempts` |
| 4a | S106 | success **between** two failures, capture present: fail@0, **ok@300**, fail@1000; store restored from HEAD | `S106 28750bcdf5d36cd90a7709fb pin=c799044be4e0 REPRODUCED` |
| 4b | S106 | same rows, **no** capture file: fail@0, ok@300, fail@1000; store empty | `S106 28750bcdf5d36cd90a7709fb pin=c799044be4e0 UNREACHABLE 2 failed attempts` |
| 5a | S100 | **http 500** failures (curl_rc 0): 500@0, 500@700 | `S100 b539a80218080da56a75b624 pin=46d1866ce9af UNREACHABLE 2 failed attempts` |
| 5b | S103 | **connect-timeout** failures (rc 28, http 000): timeout@0, timeout@700 | `S103 02aefcf570a7108e699d0990 pin=32a5907e701f UNREACHABLE 2 failed attempts` |
| 5c | S105 | **mixed** 500 + timeout 700 s apart: 500@0, timeout@700 | `S105 e3ca8f4fdd15420b80096a75 pin=2197abe27dad UNREACHABLE 2 failed attempts` |
| 6 | S100 | rc 0 / http 200 but **empty body**: empty@0, empty@700 | `S100 b539a80218080da56a75b624 pin=46d1866ce9af UNREACHABLE 2 failed attempts` |
| 7 | S103 | 2nd failure's stamp **unparsable**: fail@0, fail@700 stamped `2026-10-27 09:11:40` | `S103 02aefcf570a7108e699d0990 pin=32a5907e701f MISSING` |
| 8 | S100 | capture present but **not the last success's bytes**: fail@0, ok@300 (wrong digest), fail@1000 | `S100 b539a80218080da56a75b624 pin=46d1866ce9af MISSING capture not the last successful attempt's bytes` |
| 9 | S106 | success **after** both failures, capture present: fail@0, fail@700, ok@800 | `S106 28750bcdf5d36cd90a7709fb pin=c799044be4e0 REPRODUCED` |
| 10 | S105 | fallback-**URL** failures 700 s apart: fail@0 on the pinned URL + fail@0, fail@700 on a `web.archive.org` mirror | `S105 e3ca8f4fdd15420b80096a75 pin=2197abe27dad MISSING` |

Set totals per case: `SET=47 VERDICTS=…/47 REPRODUCED=38 DRIFTED=5 UNREACHABLE=1|2 BYTE_BACKED=43
CONSISTENT=43/43` — only the carrier's verdict moves, as intended.

## What each case proves

- **(1) vs (2) — the 600 s boundary is exact and inclusive.** 599 s → `MISSING` (not UNREACHABLE);
  600 s → `UNREACHABLE`. The predicate says "at least 600 seconds apart", the code is `>= 600`
  (`c2-count.py:231`), so the boundary lands where the frozen text says. **Survives.**
- **(3) — the rule uses the OUTERMOST pair, not "some pair".** Gaps of 300 s and 400 s (no
  consecutive pair reaches 600 s) still give `UNREACHABLE`, because `fails[-1]-fails[0] = 700 s`
  (`c2-count.py:230-231`). This matches the frozen wording ("at least two failed attempts … at
  least 600 seconds apart" — the outermost pair qualifies). Consequence for the L1: the rule is
  satisfied by the **first-to-last** span, so retry spacing must be real in the TSV's own stamps,
  not merely intended backoff.
- **(4a)/(4b) — a success BETWEEN two failures: the capture path governs.** Store present →
  verdict from the bytes: `REPRODUCED` (4a), and `REPRODUCED` again when the success is the *last*
  attempt (9). Store absent → the same history yields `UNREACHABLE` (4b). The `else:` at line 229
  is reached only when `raw_p.is_file()` is false (line 205), so **the byte store, not the attempt
  log, is the discriminator** — exactly the item's hypothesis.
- **(5a)/(5b)/(5c) — both failure shapes count as failed, per `failed()`.** `failed()`
  (`c2-count.py:154-159`) is true for `curl_rc != "0"` OR http outside 200-299 OR
  `raw_sha256 == "-"`. An **http 500 with curl_rc 0** fails via the status clause (5a); a
  **connect-timeout (rc 28, http 000)** via the rc clause (5b); mixed pairs also work (5c).
  **Survives** — the two shapes are interchangeable, as the item required. **(6)** `rc=0, http=200`
  with `raw_sha256 == "-"` (empty body) is failed too — the third clause, matching the frozen
  predicate's "or an empty body".
- **(7) — robustness edge, reported not patched.** A `fetched_utc` that `when()` cannot parse
  (space separator instead of `T…Z`) is silently dropped from `fails`, degrading `UNREACHABLE` to
  `MISSING`. The counter's own writer (`tools/capture-fetch.py:109`) always emits
  `%Y-%m-%dT%H:%M:%SZ`, so this is unreachable from the frozen recipe — only a hand-edited TSV.
- **(8)** With a store file present but not equal to the last successful attempt's bytes, the
  counter refuses REPRODUCED/DRIFTED and emits `MISSING capture not the last successful attempt's
  bytes` — the byte binding stays strict. **Survives.**
- **(10) — attempt rows are matched per (id, url, key).** The `mine` filter
  (`c2-count.py:201`) requires all three, so a fallback URL's two failures 700 s apart do **not**
  satisfy the pinned URL's spacing (carrier → `MISSING`). **No cross-URL contamination.** This
  matters for the L1's URL-swap retries (the committed `refetch.tsv` already uses that shape for
  S131/S132, whose second attempt is on a `web.archive.org` mirror URL with a different key): the
  pinned URL must itself log two failures >= 600 s apart — a mirror URL's failures are inert.
  (S131/S132 are new ids outside the frozen 47, so they carry no verdict either way.)

**Calibration.** The frozen text defines UNREACHABLE as "no capture, and at least two failed
attempts … at least 600 seconds apart"; the code implements exactly that. Two consequences for the
L1, neither changing the frozen counter: the spacing is measured on **failed** attempts only, so a
success between two failures (4b) does not defeat UNREACHABLE when the store file is missing —
UNREACHABLE means "no bytes and >= 600 s between the outermost failures", not "the URL never
answered"; and the clock is the record's own `fetched_utc`, so the L1's >= 600 s retry spacing must
be real wall-clock spacing in the TSV.

**Live-lane state** (read-only; `python3 <lane>/corpus/evidence/round57/c2-count.py --root <lane>
--verbose`, exit 0):

```
CAPTURE S100 b539a80218080da56a75b624 pin=46d1866ce9af REPRODUCED
CAPTURE S103 02aefcf570a7108e699d0990 pin=32a5907e701f REPRODUCED
CAPTURE S105 e3ca8f4fdd15420b80096a75 pin=2197abe27dad UNREACHABLE 3 failed attempts
CAPTURE S106 28750bcdf5d36cd90a7709fb pin=c799044be4e0 REPRODUCED
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS
```

The dispatch note said 43/47 with S100/S103/S105/S106 pending; by probe time the L1's attempt-2 rows
for S100, S103 and S106 had landed with their store bytes, so the lane now reads 47/47 with **only
S105 UNREACHABLE**. S105's three attempts are stamped `08:06:12Z`, `08:30:12Z`, `08:33:48Z` —
outermost span **1656 s** >= 600 s — and no store file exists for key `e3ca8f4fdd15420b80096a75`
(`committed_files=0` at HEAD), so `UNREACHABLE` is correct under the frozen rule. `REPRODUCED=41`
and `BYTE_BACKED=46` clear the frozen targets (>= 5, >= 32). Every DRIFTED capture (S083 S087 S113
S114 S121) still contains all of its pinned quotes (`absent=0/m`), so `need_flag == 0` and
`corpus/lessons/round-57.md` needs no `FRESHNESS-FLAG` line for the counter to pass; that file does
not yet exist in the lane, and the counter does not require it when `need_flag == 0`.

## Commands (abridged, observed output)

```
$ git clone --no-hardlinks --quiet /home/vgpnk/Projects/shokunin/chousa-shokunin $S/clone
$ git -C $S/clone rev-parse --show-toplevel
/fast/scratch/hyaku/chousa-r57/R57W1LabSpacing/clone
$ sha256sum <lane>/.../c2-count.py <clone>/.../c2-count.py
d6885bae2e8485e28f7d6e1fa59de7a0b3639ee0a242c71baf4c8ba753cb35f9  (both, identical)
$ python3 run_cases.py <13 cases>   # each prints its synthetic ROW lines + the counter CAPTURE line
$ python3 <lane>/corpus/evidence/round57/c2-count.py --root <lane> --verbose   # read-only
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS
```

## Hygiene and findings

- Scratch only under `/fast/scratch/hyaku/chousa-r57/R57W1LabSpacing/` (`clone/`, `pristine/`,
  `out/`, `probe.py`, `run_cases.py`, `refetch.base.tsv`); `TMPDIR=$PWD`,
  `PYTHONDONTWRITEBYTECODE=1`. **Deleted before yielding**
  (`rm -rf -- /fast/scratch/hyaku/chousa-r57/R57W1LabSpacing`).
- Frozen counters read, never edited (sha256 re-verified before every run). No
  `git commit/add/stash/checkout/reset/push`, no mutating `jj` command; the scratch clone's
  `git rev-parse --show-toplevel` was asserted before any in-clone git use. No network fetch. The
  fleet repo `/home/vgpnk/Projects/shokunin` and `/home/vgpnk/Projects/shokuknow` were not written.
  Tooling: nothing installed or upgraded (none needed) — `pdftotext -v` -> `pdftotext version
  26.08.0`, `git --version` -> `git version 2.56.0`, both pre-existing.
- **No change to any frozen predicate, target, counter, control or recipe is proposed.** Recorded
  as observations for the L1: the outermost-pair reading of the 600 s rule (case 3), the silence of
  an unparsable `fetched_utc` (case 7), and the fact that a recorded success does not by itself
  defeat UNREACHABLE when the store file is absent (case 4b). None is a falsification — the
  frozen predicate's wording is satisfied in each case.

VERDICT: the c2 UNREACHABLE spacing leg SURVIVED all five assigned probes (599 s not UNREACHABLE,
600 s UNREACHABLE, outermost-pair rule UNREACHABLE, success-between-failures governed by the capture
path, and http-500 and connect-timeout both counted as failed); 13 synthetic cases on an unmodified
frozen counter, plus 8 extra discriminators — no falsification, no patch proposed.
