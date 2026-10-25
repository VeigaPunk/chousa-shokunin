# RevRowR45 — SKILL.md Gates row `chousa round-45 counters` (5e8c7ad2f7b8254d83358820286e3d12ca4672d1)

Item: Gates row at SKILL.md:109 (archive tree). Verdict: **HOLDS** — all 8 cells verified; every entry command rerun in the archive tree matches the verdict map; both c2 and c1 self-tests reproduced byte-for-byte from the cited sources; c3 do-nothing and forged-span controls reproduced. Row cell count = 8 (9 `|` separators; header line 77 has the same 8 columns).

## Per-cell

**name** ` `chousa round-45 counters` ` — matches task. HOLDS.

**kind** — `gate`. HOLDS.

**entry** — 4 commands, rerun verbatim inside `/tmp/chousa-r45-RevRowR45/tree` (git archive of 5e8c7ad), all exit 0:
- `python3 corpus/evidence/round45/c1-count.py` → case lines a–e all `ok`, `CASES_MATCH=5/5`, `C1=PASS`, EXIT=0
- `python3 corpus/evidence/round45/c2-count.py --list` → `ENTRY_POINTS=54 GATES_ROWS=30 REGISTERED=54/54 UNREGISTERED=0 C2=PASS`, EXIT=0
- `python3 corpus/evidence/round45/c3-count.py` → `ENTRIES=2/2 CITES_BOUND=3/3 QUOTES_IN_SPAN=4/4 QUOTES_IN_ENTRY=4/4 COUNTS_IN_ENTRY=7/7 CAPTURE_BOUND=4/4 COUNTS_REDERIVED=7/7 C3=PASS`, EXIT=0
- `python3 corpus/evidence/round45/c3-count.py --lane-only` → same first five, `CAPTURE_BOUND=skipped COUNTS_REDERIVED=skipped C3=PASS`, EXIT=0
HOLDS.

**verdict map** — C1 `CASES_MATCH=5/5`/`C1=PASS`/exit 0 observed; C2 `UNREGISTERED=0`/`C2=PASS`/exit 0 observed; C3 default and `--lane-only` values observed exactly as written. Exit-code clauses: `--bogus` on c1 and c3 → argparse exit 2; c2 with empty `--root` → `C2=FAIL no-entry-points` exit 2; a failed case (r44 launcher run below) → exit 1; do-nothing/forged fixtures → exit 1. All verdict-map exit branches observed. HOLDS.

**self-test** — all four controls reproduced:
- c1-control-r44-tool.txt: provenance resolved — blob `79ee8f29` is `tools/parent-lifetime.sh` at r44 commit b603302 and at freeze d82cec9 (sha256 `f3b0baac…`). `c1-count.py --tool <blob>` → `CASES_MATCH=1/5 C1=FAIL` exit 1; identical to control file lines. HOLDS.
- c2-control-base.txt: base `d29bf47d94149a1b71581eeb0f36d9ff22d41da3` (exists as commit; no `round45` dir). Counter run with `--root` base → `ENTRY_POINTS=51 GATES_ROWS=18 REGISTERED=25/51 UNREGISTERED=26 C2=FAIL`, exit 1, 26 unregistered paths identical to control. HOLDS.
- Freeze-tree clause "adds this round's three counters → 29": counter run with `--root` d82cec9 archive → `ENTRY_POINTS=54 GATES_ROWS=18 REGISTERED=25/54 UNREGISTERED=29`, exit 1 (26 + c1/c2/c3 round45). HOLDS.
- c3-control-do-nothing.txt: rebuilt fixture (entries, spans.tsv, spans/, counts.json removed) → exact control output `ENTRIES=0/2 … C3=FAIL`, exit 1. HOLDS.
- c3-control-forged-span.txt: rebuilt fixture (bogus capture sha in spans.tsv and counts.json) → default `CAPTURE_BOUND=0/4 COUNTS_REDERIVED=0/7 C3=FAIL` exit 1; `--lane-only` `C3=PASS` exit 0 (blind spot confirmed). HOLDS.

**pinned values** — `d82cec904bf0fb8736886b9f17be913c7807427a` exists (commit, "round-45: freeze three claims…"); `corpus/evidence/round45/claims.md` sha256 identical at d82cec9 and 5e8c7ad (`e213d9e6…`) → claims frozen at the cited commit. HOLDS.

**write scope** — "read-only (c1 writes receipts to its own temp dir only)": c1-count.py code uses `tempfile.TemporaryDirectory` and writes only there; c2/c3 read-only. No lane writes performed during review. HOLDS.

**owner** — `chousa`. HOLDS (nontestable).

## Residual risk / gaps
- Blob `79ee8f29` is not in `.qcache` (capture cache holds 24-hex names); provenance established via git objects instead (r44 commit b603302 and freeze d82cec9 hold an identical launcher, sha256 `f3b0baac457710d6a210ad4e1f27e8d398f6b51c58290d8c90fea8bdca3e33cb`).
- c3 fixtures rebuilt from the final tree approximate the original wave-1 fixture mutations; outputs matched the committed control transcripts exactly.

## Tooling
No tools installed (none needed).
