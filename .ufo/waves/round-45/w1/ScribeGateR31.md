# ScribeGateR31 — draft SKILL.md Gates row for round 31

Item assigned: draft the SKILL.md Gates row for round 31's gate entry points
(`corpus/evidence/round31/c1-count.py`, `c1-count-v3.py`, `c2-count.py`, `c2-count-v3.py`),
exactly 8 cells, naming every listed file by repo-relative path, verdict map from observed
runs, control in self-test, measured lane commit/receipts in pinned values, `read-only`/receipt
write scope, `chousa` owner.

## Evidence read (all absolute, lane root = /home/vgpnk/Projects/shokunin/chousa-shokunin)

- `corpus/evidence/round31/claims.md` (present, 239 lines): design v2 frozen; base
  `be7b8d8d`, v1 `d78d1889`, v2 `8070f92b`; P1/P2 predicates; exit contract 0/1/2;
  counters take `--gate PATH --seed N --receipt OUT.json`.
- `SCORECARD.md:1740-1774` (Round 31 verdict): landed C1 `c17948a7` (gate `3b5279eb…bc3b`),
  C2 `6d0ae19f` (gate `c23d7537…823c`); final gate `0bc318b3…1258` after post-falsify fixes;
  receipts `.ufo/waves/round-31/measure/after-c{1,2}-run{1,2}.json`, `after-c{1,2}-run{3,4}-tip.json`,
  `after-c{1,2}-run{7,8}-final.json`; controls `.ufo/waves/round-31/controls/`.
- `corpus/lessons/round-31.md`: v2 control re-score `86188116`; best C1 control 116/120
  (start-line-only), best C2 118/120 (trim); no-reader C1 88/120, C2 86/120; do-nothing 50/120.
- `SKILL.md` Gates section (lines 75-489): no round-31 counters row exists; rows for rounds
  29-39 + 32-39 counters present; conventions copied (e.g. `research-gate round-37 counters` row:
  entry lists `python3 corpus/evidence/round37/c1-count.py` · `c2-count.py` (lane root; flags), verdict map
  counts + `exit 0 iff holds; 1 otherwise; 2 harness`, self-test `before on gate …`, pinned values
  contract/receipts, write scope, `chousa`).

## Commands run (verbatim; all from lane root; defaults; no `--receipt`/`--keep`)

1. `python3 corpus/evidence/round31/c1-count.py` → `LINE_BINDING_MATCH=120/120` (per-class
   12/12 … 8/8), `exit=0` (wall 4.19 s).
2. `python3 corpus/evidence/round31/c1-count-v3.py` → `LINE_BINDING_MATCH=132/132`
   (incl. `I2_nonstring_line_value 12/12`), `exit=0` (wall 4.29 s).
3. `python3 corpus/evidence/round31/c2-count.py` → `REVISION_BINDING_MATCH=120/120` (per-class
   24/24 … 16/16), `exit=0` (wall 2.98 s).
4. `python3 corpus/evidence/round31/c2-count-v3.py` → `REVISION_BINDING_MATCH=132/132`
   (incl. `I2_nonstring_sha_value 12/12`), `exit=0` (wall 3.10 s).
5. `sha256sum tools/research-gate.sh` → `2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34`
6. `git rev-parse HEAD` → `d82cec904bf0fb8736886b9f17be913c7807427a` (round-45 freeze commit; the
   gate blob is unmodified vs HEAD — `git status --porcelain -- tools/research-gate.sh` empty).
7. `ls corpus/evidence/round31/` → claims.md, c1-count.py, c1-count-v3.py, c2-count.py, c2-count-v3.py.

## Verdict

All four counters observed exit 0 today on the working-tree gate (sha256 `2cb04bdd…`, HEAD
`d82cec904`): c1-count.py 120/120, c1-count-v3.py 132/132, c2-count.py 120/120, c2-count-v3.py
132/132. The v3 counters are new files from round-32 routed defect R2 (non-string `"line"`/
`"sha256"` class, TOTAL 132); the v2 counters stay frozen (P1/P2 counters). Draft row below.

## Draft row (verbatim, one line, 8 cells)

```markdown
| research-gate round-31 counters | gate | `python3 corpus/evidence/round31/c1-count.py` · `python3 corpus/evidence/round31/c1-count-v3.py` · `python3 corpus/evidence/round31/c2-count.py` · `python3 corpus/evidence/round31/c2-count-v3.py` (lane root; `--gate PATH`, `--seed N`, `--receipt OUT.json`) | `LINE_BINDING_MATCH=120/120` (c1-count.py v2) · `REVISION_BINDING_MATCH=120/120` (c2-count.py v2), exit `0` iff matched==120; any other count exit `1`; harness error (fixture gen, missing gate, `--keep`/`--receipt` failure) exit `2`; the v3 counters (`c1-count-v3.py`/`c2-count-v3.py`) add the 12 non-string `"line"`/`"sha256"` claims (round-32 routed defect R2), TOTAL 132, labels `LINE_BINDING_MATCH=n/132`/`REVISION_BINDING_MATCH=n/132`, exit `0` iff matched==132; v2 counters stay frozen and are superseded for that class only | before on the base gate `be7b8d8d`: 50/120 each (do-nothing controls, `controls/CtlBaselineJunk/`); best v2 queues C1 116/120 (start-line-only binding, `controls/CtlShortcutC1/v2/`), C2 118/120 (whitespace-trimming, `controls/CtlShortcutC2/v2/`); no-reader C1 88/120, C2 86/120 (`controls/CtlNoReaderC1/v2/`); the v3 counters fail the round-31 nonstring-absent mutants (MutC1Grammar gate `85d85a7b`, MutC2Parse gate `f9da8257`) | contract `corpus/evidence/round31/claims.md` (design v2; base `be7b8d8d`, v1 `d78d1889`, v2 `8070f92b`, control re-score `86188116`); landed C1 `c17948a7` (gate `3b5279eb`), C2 `6d0ae19f` (gate `c23d7537`), final gate `0bc318b3` (post-falsify fixes `65d00cfc`); receipts `.ufo/waves/round-31/measure/after-c{1,2}-run{1,2}.json`, `after-c{1,2}-run{3,4}-tip.json`, `after-c{1,2}-run{7,8}-final.json`; controls `.ufo/waves/round-31/controls/`; falsify re-runs `.ufo/waves/round-31/falsify/Rerun*` | temp dirs only (mkdtemp under `C1_TMP`/`C2_TMP` or system tmp); writes a receipt only when `--receipt` is given; no network | chousa |
```

## Notes

- No tool installs/updates performed (nothing needed). No network egress. No lane writes other
  than this report. No scratch created.
- Observed values above are from today's runs on the current gate; historical before/landed
  values are cited from claims.md/scorecard/lessons (not re-run).
- The existing `verify-claims` row's self-test cell already references the r31 selftest cases
  216-228; this row registers the counters themselves.
