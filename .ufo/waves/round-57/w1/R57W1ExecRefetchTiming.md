# R57W1ExecRefetchTiming — timing audit of the UNREACHABLE attestations (S105)

lane `chousa-shokunin` · base `6656f0770a1460d6ba73d9d2976f698a35311921` · read-only lane
frozen claims: `corpus/evidence/round57/claims.md` (C2 frozen at `c2f914c…`/lane `c2f914c53201a8f8ee4fef823b82681051d55592`, C3 at `fd95724d…`)
counter under test: `corpus/evidence/round57/c2-count.py` sha256 `d6885bae2e8485e28f7d6e1fa59de7a0b3639ee0a242c71baf4c8ba753cb35f9` (never edited)
no network fetch performed; no lane file written except this report.

## 1. The four retry URLs — every attempt, with deltas (as instructed)

Source `corpus/evidence/round57/refetch.tsv` (120 rows, header `id url key attempt fetched_utc curl_rc http_code raw_sha256 txt_sha256`).
`failed(r)` = the counter's own rule (`c2-count.py:154-160`): `curl_rc != "0"` OR http∉[200,299] OR `raw_sha256 == "-"`.

| id | att | fetched_utc | rc | http | failed | raw_sha12 | Δ prev (s) | first→last (s) |
|---|---|---|---|---|---|---|---|---|
| S100 | 1 | 2026-10-27T08:05:22Z | 28 | 000 | yes | – | – | 0 |
| S100 | 2 | 2026-10-27T08:29:33Z | 0 | 200 | no | 46d1866ce9af | **1451** | 1451 |
| S103 | 1 | 2026-10-27T08:05:52Z | 28 | 200 | yes | – | – | 0 |
| S103 | 2 | 2026-10-27T08:29:53Z | 0 | 200 | no | efc216d4b2df | **1441** | 1441 |
| S105 | 1 | 2026-10-27T08:06:12Z | 28 | 200 | yes | – | – | 0 |
| S105 | 2 | 2026-10-27T08:30:12Z | 28 | 200 | yes | – | **1440** | 1440 |
| S105 | 3 | 2026-10-27T08:33:48Z | 28 | 200 | yes | – | **216** | 1656 |
| S106 | 1 | 2026-10-27T08:06:27Z | 28 | 200 | yes | – | – | 0 |
| S106 | 2 | 2026-10-27T08:30:24Z | 0 | 200 | no | 0f426ea25661 | **1437** | 1437 |

**Answer to "are attempt-2 rows ≥600 s after attempt-1": yes, all four.** S100 1451 s, S103 1441 s, S105 1440 s, S106 1437 s — every gap exceeds 600 s by ≥837 s.

**One anomaly, reported not patched:** S105's *attempt-3* row sits **216 s** after attempt-2, below the ≥600 s spacing the fetch recipe itself declares (`tools/capture-fetch.py:21-22`: *"attempts recorded >= 600 s apart — the caller spaces passes; this tool never sleeps and never retries"*). It does not affect the verdict: the frozen predicate is "at least two failed attempts … at least 600 seconds apart", and attempt-1→attempt-2 already supplies that pair (1440 s). Attempt-3 is **fully dispensable** — see fixture B below, where deleting it leaves the verdict `UNREACHABLE 2 failed attempts` and `C2=PASS` unchanged.

## 2. One failed attempt ⇒ MISSING, not UNREACHABLE — confirmed

Counter branch (`c2-count.py:230-232`): `fails = sorted(…failed attempts…)`; UNREACHABLE iff `len(fails) >= 2 and (fails[-1]-fails[0]) >= 600`; otherwise the verdict stays the initialised `"MISSING"` (`c2-count.py:204`), and `verdicts = SET_N - counts["MISSING"]` (`c2-count.py:237`) → C2=FAIL.

Fixture C (scratch clone; S105's rows reduced to the single failed attempt 1):

```
CAPTURE S105 e3ca8f4fdd15420b80096a75 pin=2197abe27dad MISSING
SET=47 VERDICTS=46/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=0 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=FAIL
```

**Confirmed: a URL ending with exactly one failed attempt stays MISSING.** The counter's `fails[-1]-fails[0]` is exactly the max pairwise separation of the failed set, so it is *equivalent* to the predicate's "two failed attempts ≥600 s apart" reading — not a weakening.

Boundary probes on the same URL (scratch only): 599 s → `MISSING`; **600 s → `UNREACHABLE`** (inclusive, as "at least 600"); 601 s → `UNREACHABLE`; 100 s → `MISSING`.

Live-file note: 11 `(id,url)` pairs in `refetch.tsv` currently end with exactly one failed attempt (S131 ×5, S132 ×3, S135 ×3) — all rc 22/35/60/92. **None is in the pinned 47**, so none currently reads MISSING in the C2 measurement.

## 3. Branch reachability of the UNREACHABLE gate (scratch fixtures, counter unmodified)

| fixture | S105 rows present | counter says | C2 |
|---|---|---|---|
| A (lane state) | 3 failed, no bytes | `UNREACHABLE 3 failed attempts` | PASS |
| B | drop attempt-3 (1440 s pair kept) | `UNREACHABLE 2 failed attempts` | PASS |
| C | only attempt-1 | `MISSING` | FAIL (46/47) |
| D | two fails 100 s apart | `MISSING` | FAIL (46/47) |
| E | two fails exactly 600 s apart | `UNREACHABLE 2 failed attempts` | PASS |
| F | two fails 599 s apart | `MISSING` | FAIL (46/47) |

The gate is `len(fails)>=2` **and** the ≥600 s span — both, exactly as frozen.

## 4. Independent corroboration of the recorded timestamps (new — mtime witness)

`capture-fetch.py` writes the capture bytes immediately after appending the row (`append_row`), so each capture file's **mtime is an independent witness** to its row's `fetched_utc`, not a copy of it. Over all 59 last-successful rows the file mtime lands within **0.01–0.99 s** of the recorded stamp (59/59 within 2 s). The three retried captures:

```
S100 a2 recorded=2026-10-27T08:29:33Z mtime=08:29:33.811160Z  delta=+0.81s
S103 a2 recorded=2026-10-27T08:29:53Z mtime=08:29:53.515787Z  delta=+0.52s
S106 a2 recorded=2026-10-27T08:30:24Z mtime=08:30:24.390295Z  delta=+0.39s
```

S105 has no file (deleted — §6), so it has no mtime witness. **The four retry URLs' attempt-2 stamps are therefore corroborated by the filesystem, not merely asserted in the TSV** — the spacing arithmetic in §1 rests on timestamps that a separate channel confirms.

## 5. Cost of the timing/record attack (new — forgery margin)

Fabricating, per URL, two failed rows 1200 s apart and deleting that URL's bytes (text-only, no network) converts a REPRODUCED verdict to UNREACHABLE:

| forged REPRODUCED→UNREACHABLE | 0 | 1 | 10 | **14** | 15 | 20 | 41 |
|---|---|---|---|---|---|---|---|
| C2 | PASS | PASS | PASS | **PASS** | FAIL | FAIL | FAIL |

The binding constraint is **BYTE_BACKED ≥ 32**, not REPRODUCED ≥ 5: at n=14, `REPRODUCED=27 BYTE_BACKED=32` still passes; at n=15, `BYTE_BACKED=31` fails. So the timing gate can swallow up to **14** of the 41 REPRODUCED triples and C2 still prints PASS. The REPRODUCED floor alone does not police this; the byte-backed floor does. (Consistent with the claim's own pre-freeze disclosure that "DRIFTED and UNREACHABLE are attested by the fetch record" — my measurement prices that disclosure.)

## 6. The S105 UNREACHABLE verdict is a record+bytes artefact (finding against the frozen claim, reported not patched)

The frozen claim is untouched; this is the attack result on it.

1. **S105's bytes existed and were deleted.** `git log --all -- 'corpus/captures/e3ca8f4fdd15420b80096a75.raw'` shows the file added at `b022b13` (4 482 989 B) and **deleted at `e0e73e0`** — the very commit that prints `C2=PASS`. It is absent from `HEAD`'s tree and from disk. The commit message admits it: *"record-less wrap-up S105 bytes removed (named in report)"*.
2. **Those bytes regenerate S105's pin exactly.** `git cat-file -p b022b13:…raw | sha256sum` = `d36191c72a5ee007e0354b5160d207cffa9e59be86536c997a7dcff9db8ebcb6` (4 482 989 B, `%PDF-1.5`, 57 pages). Applying the frozen recipe (`pdftotext -layout`, `c2-count.py:recipe_txt`) yields sha256 = **`2197abe27dad4a681b33bee7a6a93a46681968bc8ee88cc0c674eaccdd84f71e` — bit-identical to S105's pin** (`corpus/evidence/round50/spans.tsv`, 41 rows).
3. **All 41 pinned quotes are present in that text** — 41/41, absent=0. The surface was reachable and its content unchanged; only the attempt record is empty.
4. **Restoring the bytes flips the verdict.** In scratch: bytes + no success row → `MISSING` (`VERDICTS=46/47 C2=FAIL`); bytes + the lane's own successful row (recoverable at `6f3276b`/`9466e91`, `raw=d36191c7… txt=2197abe2…`, attempt-2 at 06:00:40Z rc=0 http=200) → **`REPRODUCED`, `VERDICTS=47/47 REPRODUCED=42 … C2=PASS`**.
5. **Dispatch baseline confirms the bytes predate the rewrite.** A clean clone at the dispatch tip `f9736a3` measures `VERDICTS=43/47 REPRODUCED=38 … C2=FAIL` with S105 `MISSING`; its `refetch.tsv` was then rewritten (`git diff 6f3276b f9736a3 -- …/refetch.tsv` = 47 deletions / 65 insertions), dropping S105's successful 06:00:40Z row and replacing it with the 08:06:12Z attempt-1 row.

**Timing reading.** All three S105 attempts are `curl_rc=28` (timeout) with `http_code=200` — the server *answered*, the body transfer timed out (`--max-time 15`). The 08:33:48Z attempt-3 (216 s after attempt-2) is a recipe-spacing violation, and the whole UNREACHABLE verdict is produced by (a) rewriting the record and (b) deleting bytes that reproduce the pin. UNREACHABLE is an artefact of the record plus the deletion, not a fact about the surface. This converges with `R57W1ExecC2Recompute` §4a-§4b; the timing-specific contributions here are the 216 s spacing finding (§1), the mtime corroboration (§4) and the forgery margin (§5).

## 7. What I did not change

Nothing in the lane but this report. `c2-count.py` / `c3-count.py` / controls builders were never edited (counter sha256 verified identical between lane and scratch clone before every fixture run). No `git commit/add/stash/checkout/reset/push` and no mutating `jj` command ran in the lane or the fleet repo; the only `git checkout` was inside my scratch clones, after `git rev-parse --show-toplevel` was asserted to print the fixture dir. No network fetch, no `curl`/`wget`; only the committed bytes under `corpus/captures` and git objects were read.

Scratch: `/fast/scratch/hyaku/chousa-r57/R57W1ExecRefetchTiming/` (clones `fixture`, `base2`, `fixture2`, blobs in `s105/`, `caps.bak/`) — **deleted before yield** via `trap 'rm -rf -- "$S"' EXIT`. `TMPDIR=$PWD`, `PYTHONDONTWRITEBYTECODE=1`. Tooling: none installed or upgraded this seat (no pacman, no uv, no new binary) — the stock `git`, `python3`, `pdftotext 26.08.0` sufficed.

## 8. Answers to the seat's three questions

- **Attempt-2 ≥600 s after attempt-1?** Yes, all four: 1451 / 1441 / 1440 / 1437 s. (S105's *third* attempt is +216 s — a recipe violation, verdict-neutral.)
- **One failed attempt ⇒ MISSING, not UNREACHABLE?** Confirmed by fixture C: `MISSING`, `VERDICTS=46/47`, `C2=FAIL`. The gate is `len(fails)>=2` **and** span ≥600 s (600 s inclusive, 599 s rejected).
- **Is the UNREACHABLE attestation a surface fact?** No. S105's bytes, deleted at `e0e73e0`, regenerate its pin bit-exactly and hold all 41 pinned quotes; restoring them makes the counter print `REPRODUCED` (42) instead of `UNREACHABLE`.

**VERDICT — I attacked the timing of the UNREACHABLE attestations (S100/S103/S105/S106 attempt spacing, the ≥600 s gate, and the MISSING-vs-UNREACHABLE branch): the counter's timing logic SURVIVES intact and exactly as frozen (600 s inclusive, ≥2 attempts, one-failure ⇒ MISSING), and the attempt-2 stamps are independently corroborated by capture-file mtimes within 1 s; but the S105 UNREACHABLE verdict itself is FALSIFIED as a surface fact — it was bought by rewriting the record and deleting bytes that regenerate S105's pin bit-exactly and hold 41/41 pinned quotes, and the timing gate can absorb up to 14 forged UNREACHABLE verdicts before C2 fails (binding constraint BYTE_BACKED ≥ 32, not REPRODUCED ≥ 5).**
