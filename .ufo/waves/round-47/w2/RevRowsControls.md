ATTACKS: round35–41 gate controls row; round-29 quote-reopen counter row; round-26 registry oracle row (SKILL.md `## Gates`)
VERDICT: holds

## 1. `round35–41 gate controls` row (SKILL.md:113)

All eight entry files exist and are tracked at lane tip `1fc5ed1`; the five sha256 pins match byte-exact at the round-46 commit `1e9756f` (sha256sum of `git show 1e9756f:<path>`):
- ctl-c1-hardcoded-grep.sh `05bdf654…` ✓
- base-gate-r36.sh `a4768851…` ✓
- ctl-c2-stub-pass.py `ee0e0cc7…` ✓
- base-gate-r37.sh `a7d3922c…` ✓
- mut-gate-path-env.sh `e1251030…` ✓
(r38/r39/r41 base gates have no sha pin — consistent with being r47 additions.)

Run each shell control on trivial inputs (no args / nonexistent record path / bogus record): all seven exit `2` with the documented usage/not-found messages (`die_usage` → `exit 2`, e.g. r36 lines 536, 952-955). `ctl-c2-stub-pass.py` prints exactly `WITNESS=pass OUTPUT=9/9 ATTRIB=9/9 (stub)` and exits `0` without reading input. Header contract `0 CLEAN · 1 DRIFT · 2 setup/usage` is present in every copy (line 8-9) and the `0`/`1` paths exist (`exit 0`/`exit 1` in the drift/composed-verdict machinery). No false exit-code statement.

Defect found (minor): the self-test cell says "quote each invoked command and its expected outcome (five citations)" and names four claims files (r35, r36, r37, r39). The five citations map to the five research-gate copy controls (r35: ctl-c1-hardcoded-grep.sh; r36: base-gate-r36.sh + ctl-c2-stub-pass.py; r37: base-gate-r37.sh; r39: mut-gate-path-env.sh). The r47-added `base-gate-r38.sh` and `base-gate-r41.sh` are not covered by the quoted self-test even though both are named in their rounds' frozen claims (r38 claims.md:231; r41 claims.md:40) and get exit-code naming in the verdict map. The row's own statements are all true; this is a coverage gap of the added gates, not a false claim.

## 2. `round-29 quote-reopen counter` row (SKILL.md:127)

- No `--` → `usage: c1-count.py [--receipt PATH] -- CMD...`, exit `2` ✓.
- `--receipt X --` with empty CMD → `usage: empty CMD`, exit `2` ✓.
- Candidate that emits no verdict lines → prints `QUOTE_REOPEN_MATCH=0/130`, exit `1` ✓ (two runs; `tool_exit=2`). Exit `1` on any mismatch confirmed as the `return 0 if n == t == FROZEN_TOTAL else 1` predicate (line 299).
- Exit `2` on fetch/setup error confirmed: in this environment the counter's own page-sampling `build()` fails fetching registry URLs and exits `2` with `fixture error: Sxxx: no registry URL`/fetch error before the candidate runs — matching the docstring "2 on usage/fixture/fetch error".
- "A verifier that answers VERBATIM for every item scores below 130/130": holds by construction (frozen 40 incl. 14 VERBATIM + 42 runtime variants incl. 28 non-verbatim + 48 page-sampled incl. 24 transposes).
- Exit `0`-only-when-130/130 is consistent with the code predicate; page-sampled items require re-opening pages, so a no-fetch verifier cannot reach it. No false exit-code statement.

## 3. `round-26 registry oracle` row (SKILL.md:128)

Oracle `main()`: prints JSON, returns `0` on success; catches `OSError/UnicodeError/ValueError` → stderr + `2`; argparse errors → `2`. Verified:
- minimal valid registry+entry → JSON + `0` ✓
- unreadable entry → `[Errno 13] Permission denied` + `2` ✓
- registry with no id/status/used-by table → `registry has no table…` + `2` ✓
- missing `--registry` → argparse error + `2` ✓

Differential (`round26-registry-differential.sh`) computes the disagreement verdict: exits `0` iff all suites ran, oracle_rc==0, and every finding matches; else `1` — it does own the admission verdict; oracle values are only compared. Row statements hold.

Residual risk: exit-0 of the r29 counter (130/130) could not be *observed* because page-sampled cases require live fetches, which the seat contract forbids; the predicate was verified by reading the code path (line 299), not by execution. No tool installs.
