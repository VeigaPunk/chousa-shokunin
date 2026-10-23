VERDICT: pass — Separability holds: each counter responds only to its own change, both revisions land as claimed.

Axes: coverage (C1 counter, 106 items) and operability (C2 counter, 27 items). Separability = C1 change moves only C1, C2 change moves only C2.

Setup (scratch clone /fast/scratch/hyaku/chousa-r30/w2/SeparabilityRevs/, git clone of the lane, read-only):
- Extracted with `git show <rev>:tools/quote-reopen.py` → `tool-a3a3710.py` (SHA 72a3ad47…), `tool-bd43bd5.py` (84b851aa…), `tool-49b2aa3.py` (47a657e7… = frozen landed SHA).
- C1-only variant: `patch -p0 -t` of the landed `c1.patch` onto the base → `tool-c1only.py` (SHA 69682ce4…), byte-identical to `.ufo/waves/round-30/build/ExecC1Head/quote-reopen.py` (`diff -q` clean). `grep -n "socket|connect|deadline|DEADLINE|resolve"` over c1.patch: zero hits; the patch touches only docstring, SKIP/HEAD_ELEMENTS and _Text. Base-vs-bd43bd5 diff touches only fetch-layer lines (watchdog, one-resolution `_dial`, TLS hostname).

Results (each run from lane root, `--tool <path> --receipt <path>`; c1/c2 counters SHA 5b312d84…/0a59e373…, harness e2be0dd1… all match claims.md frozen values):

| tool revision | C1 run1 | C1 run2 | C2 run1 | C2 run2 |
|---|---|---|---|---|
| base a3a3710e | 78/106, exit 1 | 78/106, exit 1 | 12/27, exit 1 | 13/27, exit 1 |
| bd43bd53 (C2 only) | 78/106, exit 1 | 78/106, exit 1 | 27/27, exit 0 | 27/27, exit 0 |
| 49b2aa30 (C2+C1, landed) | 106/106, exit 0 | 106/106, exit 0 | 27/27, exit 0 | 27/27, exit 0 |
| c1only (base + c1.patch) | 106/106, exit 0 | 106/106, exit 0 | 12/27, exit 1 | 14/27, exit 1 |

C1: base = bd43bd5 = 78/106 (C2 change does not move C1); c1only = 49b2aa30 = 106/106 (C1 change does). C2: base ≈ c1only ≈ 12–14/27 (C1 change does not move C2); bd43bd5 = 49b2aa30 = 27/27 (C2 change does). Receipts all recorded `predicate_holds` True/False consistently (C2 receipts `design: "v3"`). Counter-absent/C1 base spreads match claims.md pre-freeze v4 values.

Evidence: receipt JSONs in this dir (c1-{base,bd43,c1only,49b2}-run{1,2}.json, c2-{base,bd43,c1only,49b2}-run{1,2}.json); commands quoted above with stdout and exit codes; `diff` proves the two landed commit diffs are disjoint in code region.

[INFERENCE] the 13/27 and 14/27 base-run wobble is the documented end-of-stream-at-deadline read of the round-29 tool (claims.md v3/v4 notes), not a counter or harness drift; both are misses under the kill rule either way.
