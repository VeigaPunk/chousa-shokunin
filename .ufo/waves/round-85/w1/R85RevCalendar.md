# R85RevCalendar — calendar check reverse-engineering (C1 leg)

Seat: R85RevCalendar. Lane: chousa round 85. Claim touched: C1 (operability) — the `fetched` calendar leg.
Falsifiable hypothesis: the round-85 `_valid_ts` (`datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")`) and the `TS_RE` shape check together accept exactly the real UTC instants and reject every shape-valid impossible date, and the check cannot be bypassed by a value that `strptime` accepts while a reader would call it invalid.

Landing revision attacked: `64803d33362f50cf9094e91fc3a4a07216c563ca` (sha256 `2de7972…b97703beb` for `tools/gate-records.py`, verified identical to checkout).
Extraction: `git archive 64803d33… | tar -x -C /fast/scratch/hyaku/chousa-r85/R85RevCalendar`.
Frozen claims read first: `corpus/evidence/round85/claims.md` (including every kill rule) and `plans/round-85.md`.

## Reconstructed contract (what the landed bytes do)

In `tools/gate-records.py` (landing):

- `import datetime` at line 60; `TS_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")` (line 69) — ASCII-only shape, capital `T`, capital `Z`, exactly 20 chars via `fullmatch`.
- `def _valid_ts(s): try: datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ"); return True; except ValueError: return False` (lines 197–202). Note: only `ValueError` is caught; no other exception type is handled.
- Enforcement at line 144, inside `parse()`, only for `form in ("admit", "unreach")`:
  `if not re.fullmatch(r"https?://\S+", kv["url"]) or not TS_RE.fullmatch(kv["fetched"]) or not _valid_ts(kv["fetched"]): return None`
  → a parse failure is reported by `main()` as `FAIL PARSE` with process rc 1 (line 313).
- The `rev` form (`REV_KEYS = ("rev","path","line","words")`) has **no `fetched` key at all** and never touches `TS_RE` / `_valid_ts`. A rev line is validated for `rev/path/line/words/quote` only. Adding a `fetched=` token to a rev line is an extra-key parse failure (`FAIL PARSE`), not a calendar check.

Therefore the "calendar check" is a property of two grammars (admit/unreach) that share one gate; rev is a third grammar with no timestamp.

## Evidence chain — independent boundary set (not the counter's list)

One admit base (S203, frozen positive from `corpus/evidence/round85/c2-positives.tsv`), one unreach base (S208), one rev base (S199). For each of 18 candidate `fetched` values, `fetched=<value>` was substituted by `kv_set` into the admit and unreach lines; the rev line (no `fetched` key) was left unchanged (a no-op substitution, `fetched_tok=None`) and additionally a rev line with a spurious `fetched=` token was probed separately.

Command: `python3 -B /fast/scratch/hyaku/chousa-r85/R85RevCalendar/make_and_run2.py` (receipt `receipts/make_and_run2.py`, output `receipts/run2-output.txt`). Tool invocation per case:
`python3 -B tools/gate-records.py verify --root <scratch-root> --repo /home/vgpnk/Projects/shokunin/chousa-shokunin <fixture>.md`
Fixture dir (scratch): `fixtures2/`. Backend repo is the live lane checkout (`git rev-parse --show-toplevel` = `/home/vgpnk/Projects/shokunin/chousa-shokunin`); the first run with `--repo <scratch>` correctly exited 2 (`GATE_RECORDS_ERROR not a git repo`) — the round-85 setup repair — and was discarded (receipt: `run-output.txt` shows rc=2 lines only; the valid receipt is `run2-output.txt`).

Results (admit / unreach / rev — rev is always `rc=0 OK` because it has no `fetched` gate; the table shows admit and unreach verdicts, which matched in every case):

| # | Candidate `fetched` | TS_RE | `strptime` | Tool (admit S203) | Tool (unreach S208) |
|---|---|---|---|---|---|
| 1 | `2024-02-29T12:00:00Z` (leap day, accept) | True | accept | `FAIL REFETCH` rc=1 | `FAIL REFETCH` rc=1 |
| 2 | `2025-02-29T12:00:00Z` (non-leap, reject) | True | `ValueError: day 29 must be in range 1..28 for month 2 in year 2025` | `FAIL PARSE` rc=1 | `FAIL PARSE` rc=1 |
| 3 | `2026-04-31T00:00:00Z` (April 31, reject) | True | `ValueError: day 31 must be in range 1..30 for month 4 in year 2026` | `FAIL PARSE` rc=1 | `FAIL PARSE` rc=1 |
| 4 | `2026-12-31T23:59:59Z` (accept) | True | accept | `FAIL REFETCH` rc=1 | `FAIL REFETCH` rc=1 |
| 5 | `2026-01-01T00:00:00Z` (accept) | True | accept | `FAIL REFETCH` rc=1 | `FAIL REFETCH` rc=1 |
| 6 | `2026-01-01T24:00:00Z` (hour 24, reject) | True | `ValueError: time data '2026-01-01T24:00:00Z' does not match format …` | `FAIL PARSE` rc=1 | `FAIL PARSE` rc=1 |
| 7 | `2026-01-01T00:00:60Z` (second 60, reject) | True | `ValueError: second must be in 0..59, not 60` | `FAIL PARSE` rc=1 | `FAIL PARSE` rc=1 |
| 8 | `0000-01-01T00:00:00Z` (year 0000, reject) | True | `ValueError: year must be in 1..9999, not 0` | `FAIL PARSE` rc=1 | `FAIL PARSE` rc=1 |
| 9 | `2026-00-15T00:00:00Z` (month 00, reject) | True | ValueError (format mismatch) | `FAIL PARSE` rc=1 | `FAIL PARSE` rc=1 |
| 10 | `2026-01-01T00:00:00+00:00` (offset text, reject shape) | False | ValueError (unconverted data) | `FAIL PARSE` rc=1 | `FAIL PARSE` rc=1 |
| 11 | `2026-01-01t00:00:00Z` (lowercase `t`, reject) | False | **accept** | `FAIL PARSE` rc=1 | `FAIL PARSE` rc=1 |
| 12 | `2026-01-01T00:00:00z` (lowercase `z`, reject) | False | **accept** | `FAIL PARSE` rc=1 | `FAIL PARSE` rc=1 |
| 13 | `2026-01-01T00:00:00Z ` (trailing `Z `) | False | ValueError (unconverted data) | `FAIL PARSE` rc=1* | `FAIL PARSE` rc=1* |
| 14 | `2026-01-01T00:00:00Z` + U+0660 (`٠`) (trailing unicode digit, reject) | False | ValueError (unconverted data) | `FAIL PARSE` rc=1 | `FAIL PARSE` rc=1 |
| 15 | `2026-13-40T00:00:00Z` (D4 class, reject) | True | ValueError (format mismatch) | `FAIL PARSE` rc=1 | `FAIL PARSE` rc=1 |
| 16 | `2026-01-00T00:00:00Z` (day 00, reject) | True | ValueError (format mismatch) | `FAIL PARSE` rc=1 | `FAIL PARSE` rc=1 |
| 17 | `2026-01-01T00:60:00Z` (minute 60, reject) | True | ValueError (format mismatch) | `FAIL PARSE` rc=1 | `FAIL PARSE` rc=1 |
| 18 | `2026-٠١-15T00:00:00Z` (unicode digits in month, reject) | False | ValueError | `FAIL PARSE` rc=1 | `FAIL PARSE` rc=1 |

`*` Case 13 note: the harness `kv_set` uses `\S+`, so the injected trailing space truncates the token to `2026-01-01T00:00:00Z` and instead inserts an empty head token (`""`) between `fetched=` and `tier=`; `parse()` rejects the empty token (`"=" not in tok` → `return None`) before the timestamp is ever examined. The receipt fixture therefore records a `PARSE` verdict via the empty-token path, which is also a correct rejection but is **not** evidence about `TS_RE`/`_valid_ts` handling of a literal trailing space. Verified by token dump in-session (receipt `final_probes.py` / `final-probes-output.txt` replays the same). The literal-space question is moot: since the head is split on single spaces and tokens are `\S+`, a trailing space cannot survive into `kv["fetched"]` — it is structurally excluded.

Key readings:

- **Calendar-accept does not imply tool-OK.** All three "accept" values (leap day, Y2K-day boundaries, `2024-02-29`, `2026-12-31T23:59:59Z`, `2026-01-01T00:00:00Z`) pass the calendar gate (PARSE succeeds) and fail later at `REFETCH` because no `refetch.tsv` row admits that `(sid, url, fetched)` triple. This is the correct two-layer design: `PARSE` = shape + calendar; `REFETCH` = ledger agreement. The hypothesis's "accept" is therefore observed as "FILTERED at PARSE, rejected at REFETCH" — the calendar leg is not holding the tool open.
- **Calendar-reject (`FAIL PARSE`) is consistent between admit and unreach in all 18 cases** — one value grammar, one reading for the two `fetched`-bearing forms.
- **Second 60 / leap second:** `strptime` on CPython 3.14 raises `ValueError: second must be in 0..59, not 60` (no leap-second support). `TS_RE` matches the shape, `_valid_ts` returns `False`, the tool rejects with `FAIL PARSE` rc=1. `2026-12-31T23:59:60Z` was separately confirmed `TS_RE=True strptime_ok=False combined=False`. There is no leap-second acceptance path.
- **Year 0000:** `strptime` raises `ValueError: year must be in 1..9999, not 0`; rejected `PARSE`.
- **Lowercase `t`/`z`:** `strptime` *accepts* `2026-01-01t00:00:00Z`, `2026-01-01T00:00:00z`, `2026-01-01t00:00:00z` (Python's `strptime` is case-insensitive for the `T`/`Z` literals in this position). `TS_RE` rejects them (`[0-9]{4}-…T…Z` is case-sensitive), so the combined `TS_RE and _valid_ts` gate rejects them (`FAIL PARSE`). The asymmetry is on the **safe** side: the combined gate is strictly narrower than `strptime` alone. A "value that `strptime` accepts while a reader would call it invalid" (lowercase delimiters) **cannot bypass** the tool, because `TS_RE.fullmatch` runs first (or, equivalently, the `or`-chain at line 144 short-circuits to `PARSE` before `_valid_ts` matters).
- **Unicode digits:** Arabic-Indic digits (`٠`, `٠١`) in any field are rejected by `TS_RE` (ASCII `[0-9]` class + `fullmatch`) despite any `strptime`/numeric leniency, and also by `strptime`'s unconverted-data check. `FAIL PARSE`.
- **Offset form `+00:00`:** rejected by both shape (`TS_RE` length/character class) and `strptime`. `FAIL PARSE`.

Supplementary probes (`receipts/final_probes.py` → `receipts/final-probes-output.txt`):

- `M07` (second+1, a genuine-calendar but ledger-mismatched value, `2026-11-06T18:44:30Z`) → `FAIL REFETCH` rc=1, not `PARSE` — proving the tool still distinguishes calendar validity from ledger agreement and does not conflate them (no false `PARSE` on a real instant).
- Pristine frozen admit S203 (byte-identical from `c2-positives.tsv`) → `OK` rc=0 — the calendar repair did not harm a genuine record (C1 K3 leg on this seat's slice).
- Counter M21 (`fetched` + `٠`) and D4 (`2026-13-40T00:00:00Z`) are consistent with the above: both on the `PARSE` path.

## Rev vs admit — one grammar, two readings? No.

All 18 rev probes returned `rc=0 S199 OK` with `fetched_tok=None`, because the rev grammar has no `fetched` key. This is **not** a divergent reading of the same value grammar — it is a different record form (content-blob reference vs URL fetch), exactly as the frozen claims and the tool docstring define it. The only way to give a rev line a timestamp is to add a `fetched=` token, which makes it neither `REV_KEYS`, `URL_ADMIT`, nor `URL_UNREACH` and yields `FAIL PARSE` rc=1 (verified: `rev-extra-fetched` probe, `run2-output.txt`).

That is therefore **not** a QUALITY-164-class finding ("one value grammar, two readings"). The two grammars share the admit/unreach `fetched` interpretation consistently (18/18 admit-vs-unreach agreement), and the third grammar does not interpret `fetched` at all. **No finding.**

## Hypothesis verdict and kill-rule mapping

The hypothesis is **sustained** on every axis probed:

1. Every shape-valid impossible date (non-leap Feb 29, Apr 31, hour 24, second 60, year 0000, month 00, day 00, minute 60, D4 `2026-13-40`) is rejected `FAIL PARSE` rc=1 by both admit and unreach — no `OK`, no `REFETCH`-only slip.
2. Every genuine instant passes the calendar leg; its rejection, when it occurs, is `REFETCH` (ledger), not `PARSE`.
3. The one direction where `strptime` is more lenient than a reader (lowercase `t`/`z`) is closed by `TS_RE` (case-sensitive `fullmatch`), so there is no `strptime`-accepts-but-reader-rejects bypass.
4. Leap-second 60 is rejected by `strptime` itself and by the tool; recorded as `ValueError: second must be in 0..59, not 60`.

Kill rules (frozen, `claims.md` lines 74–83 for C1):

- **K1 (predicate not met):** baseline counter (pristine landing tool) prints
  `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=354/354 EXPECTED_CODE=354/354 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1` and `GATE_RECORDS_R85=PASS` rc=0 (receipt `receipts/counter-baseline.txt`). Not fired on this seat's leg.
- **K2 (in-class forgery accepted, or refused with a code outside the frozen EXPECTED_CODE set):** the calendar leg's differentiated class (D4 `2026-13-40…`, EXPECTED=P…`PARSE`) and my independent 18-value set are all refused with exactly `PARSE` where the hypothesis requires rejection, and with `REFETCH` (not `PARSE`) where the instant is genuine. No in-class acceptance, no wrong code observed in this leg. Not fired.
- **K3 (harm):** pristine frozen admit S203 is `OK` rc=0; the M07 sec+1 real-instant is `REFETCH` not `PARSE`; the counter's 15/15 + 5/5 fresh positives confirm no genuine record is refused by the calendar repair. Not fired.
- **K4 (whitelist):** not this seat's leg (counter-battery as a whole); the mutated-tool run below shows the counter does discriminate tool identity.

Result: **C1 held on the calendar leg** (no K1/K2/K3 fired by this seat's probes; K4 is owned by the counter/whitelist controls, untouched here).

## Missing-`datetime`-import mutation

Question: is `import datetime` verified present and does dropping it fail the counter?

- `grep` on the landing file: line 60 `import datetime` present (also `TS_RE` line 69, `_valid_ts` lines 197–202, enforcement line 144).
- Mutation: copy of the landed tool with the `import datetime\n` line removed (receipt `receipts/gate-records-noimports.py`, built by `receipts/mutate_import.py`).
  Direct run on the D4 forged line (`receipts/d4-test.md`): pristine tool → `FAIL PARSE` rc=1; mutated tool → traceback `NameError: name 'datetime' is not defined. Did you forget to import 'datetime'?` at `_valid_ts` line 198, rc=1, empty stdout (receipt `receipts/mutate-output.txt`). So the missing import is loud, not silent.
- Counter with `--tool <mutated>`: `TOOL=present POSITIVE=4/15 FRESH_POSITIVE=0/5 FORGED_REFUSED=44/354 EXPECTED_CODE=44/354 EMPTY_REFUSED=1/1 RC=2/4 SETUP=1/1`, `GATE_RECORDS_R85=FAIL` rc=1 (receipt `receipts/counter-baseline.txt`, MUTATED block). The mutated tool **fails** the counter decisively — but note the mechanism: the crash aborts the whole batch run, so most forgeries appear `NOT_REFUSED` (no stdout line to parse). The counter does catch the missing import, through batch abort + fresh-positive failures, not through a targeted "import check" assertion. No byte-level import pin is needed beyond this behavioral discrimination. **Caught.**

## Uncertainty / inference

- All verdicts are for the CPython on this host (`python3 --version` 3.14 via the `strptime` tracebacks). `strptime` lowercase-`t`/`z` leniency and the `year 1..9999` bound are CPython-specific; on a different `strptime` implementation the direction could differ, but the combined `TS_RE and _valid_ts` gate can only be narrowed by `TS_RE`'s case-sensitive ASCII shape, so the bypass direction (strptime-accepts-reader-rejects) remains closed on any Python that loads this file, since `_valid_ts` alone is never sufficient.
- The `REFETCH` vs `PARSE` distinction for "accept" values is read off stdout; the exact `refetch.tsv` row-set for S203/S208 was not inspected to prove that the `REFETCH` failure is "no matching row" rather than a subtle sha/capture mismatch introduced by my `kv_set` (I changed only `fetched=`, so the row mismatch is exactly the `fetched` field, by construction).
- Rev-form "OK" reflects the rev line I reused (S199) with its original `rev/path/line/words/quote`; I did not re-prove the rev law beyond noting the absence of a `fetched` gate, which is structural from `REV_KEYS`/`parse()`.

## Receipts (all under `.ufo/waves/round-85/w1/R85RevCalendar/receipts/`)

- `run2-output.txt` — 18-value × admit/unreach/rev table with per-case rc (the authoritative verdict source).
- `final-probes-output.txt` — lowercase-`t`/`z` asymmetry, leap-second `strptime` ValueError, M07-vs-D4 layer separation, pristine-positives harm check.
- `counter-baseline.txt` — baseline `GATE_RECORDS_R85=PASS` rc=0 and mutated-tool `GATE_RECORDS_R85=FAIL` rc=1 counter summaries.
- `mutate-output.txt` — direct `--tool` comparison (pristine `FAIL PARSE` vs mutated `NameError` traceback) + counter-with-mutated excerpt.
- `d4-test.md` — the D4 forged line used for the direct comparison.
- `make_and_run2.py`, `final_probes.py`, `mutate_import.py` — the three drivers.
- `gate-records-noimports.py` — the mutated tool copy (landing tool minus `import datetime`).

Every finding above names the command and the receipt path; scratch originals were under `/fast/scratch/hyaku/chousa-r85/R85RevCalendar/` (extraction of `64803d33362f50cf9094e91fc3a4a07216c563ca` plus `fixtures2/`). No commits, no edits to lane/fleet files, no network use; the only writes outside scratch are this report and `receipts/`.

VERDICT: R85RevCalendar C1 held — the landed TS_RE+strptime calendar gate accepts exactly genuine instants at PARSE (genuine-but-unledgered instants fail correctly at REFETCH) and rejects every shape-valid impossible date including leap-second 60, with no strptime-vs-reader bypass (lowercase t/z closed by TS_RE) and no admit/unreach/rev grammar divergence.
