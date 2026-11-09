# R96RevenPrior — C1 novelty and D1 openness (base `bbf64970`, freeze `2db151c5`)

Seat scope: is C1 new, and was D1 really open? All commands run from the clones
under `/fast/scratch/hyaku/chousa-r96/R96RevenPrior/` (`repo/` = base `bbf64970…`,
`freeze-repo/` = freeze `2db151c5…`). GNU grep via `/usr/bin/grep`.

## Findings

### F0 (structural): the §Gate standard's vocabulary does not say what D1 says

- `PROTOCOL.md:377-379` — "A **gate** is a committed, re-runnable verdict script … A tool that
  cannot fail is a **probe**, and is registered as one."
- `PROTOCOL.md:401-403` (Registry) — "Row fields: name, `gate|probe`, entry command, verdict map …"
- The `- **Registry**` bullet at `PROTOCOL.md:398-403` defines only `gate|probe` as legitimate
  `kind` values. No `tool` kind is permitted by the standard as written at either base or freeze.
- Consequence: the r95 row (`SKILL.md:177` at base: `| `search-rerun verify` (r95) | tool | …`)
  is outside the vocabulary not merely by convention but by the letter of `PROTOCOL.md:401-402`.
  D1's "outside the §Gate standard `gate|probe` vocabulary" is therefore a literal standard
  violation at base, not a stylistic preference.
- Receipt: `.ufo/waves/round-96/w1/R96RevenPrior-standard.txt`
  (command `sed -n '375,403p' /home/vgpnk/Projects/shokunin/PROTOCOL.md`, exit 0;
  observed line 401-402 "Row fields: name, `gate|probe`, entry command, verdict map (code → class),
  self-test command and spelling, pinned-value path, write scope, owner.").

### Q1 — did any lane mechanism at base self-test search-rerun? **No.**

**F1 (base `bbf64970`): `tools/search-rerun.py` exposed no self-invocation mode; only `verify`.**
- `tools/search-rerun.py:378-392` (`def main(argv)`): `ap = argparse.ArgumentParser(prog="search-rerun.py")`;
  `sub = ap.add_subparsers(dest="cmd", required=True)`; `v = sub.add_parser("verify")` — the subparser
  is the only entry; there is no `--selftest` argument, no `selftest()` function, and `a = ap.parse_args(argv)`
  is the sole parse. `a.selftest` is never referenced.
- Runtime check: `python3 -B tools/search-rerun.py --selftest` → stderr `usage: search-rerun.py [-h] {verify} …`
  / `search-rerun.py: error: the following arguments are required: cmd`, **exit 2**. The `--selftest` flag is
  not recognised at base; it is not a usage error meaning "no such flag on a flag-accepting program" but the
  required-subcommand error because the token is not defined.
- Receipt: `.ufo/waves/round-96/w1/R96RevenPrior-base-selftest.txt`
  (commands `python3 -B tools/search-rerun.py --selftest` and `--help`, exits 2 and 0 respectively).
- Grep corroboration (no `selftest` token anywhere in the file):
  `/usr/bin/grep -n "selftest\|self-test" tools/search-rerun.py` → no match (exit 1) at base, versus 14+
  matches at freeze (e.g. `tools/search-rerun.py:46 "python3 tools/search-rerun.py --selftest"`,
  `:419 def selftest():`, `:524 ap.add_argument("--selftest", action="store_true", …)`).

**F2: no other lane mechanism at base self-tested search-rerun.**
- `tools/lane-preflight.py:253,258,269` — its `selftest(...)` helper calls only
  `tools/freeze-check.py --selftest`, `tools/assimilate-rows.py --selftest`, and
  `bash tools/research-gate.sh --selftest` (G06, G07, G08 in `lane-preflight.py:23-25`). No call names
  `search-rerun.py`.
- `tools/research-gate.sh:4495 run_selftest()` tests the gate's own modes (verify, verify-claims, verify-chain, …);
  `/usr/bin/grep -n "search-rerun\|rerun" tools/research-gate.sh` → 0 matches at base, so the gate's self-test
  never invokes `search-rerun.py`.
- `corpus/evidence/round95/rerun-controls-r95.py` (the D1-named alternative) is a **battery**, not a
  self-invocation mode: it runs the tool through its public CLI and compares exit codes. Header
  (`rerun-controls-r95.py:1-3`): "Every case runs the tool under test as a fresh process through its public
  CLI (`python3 -B <tool> verify <record> --root <root> [--strict]`)". It is the round-95 C1 control
  battery, not a flag on the tool, and it existed at base. D1's disjunction ("e.g. `rerun-controls-r95.py`
  or add a `--selftest`") was satisfiable without adding a flag, but no SKILL.md row at base names it as
  the self-test of search-rerun: the r95 row's `self-test` cell at base (`SKILL.md:177`) names the battery
  (`python3 -B corpus/evidence/round95/rerun-controls-r95.py --root . --work DIR → RERUN_CONTROLS=PASS` …)
  under kind `tool`. At freeze C1 chose the second disjunct; either disjunct would close D1, but the
  executed one is unambiguous.
- Receipt: `.ufo/waves/round-96/w1/R96RevenPrior-tools-survey.txt`
  (command survey of `tools/`; `search-rerun` appears in the "no `selftest` token" list at base).

**Answer Q1: No lane mechanism at base self-tested search-rerun by a flag on the tool; the only
self-test-shaped artefact was the round-95 battery (`rerun-controls-r95.py`), cited as the battery under
kind `tool`, not as a gate self-test. C1's novelty (a new `--selftest` flag on the tool) is true, and D1 was
genuinely open as stated** ("`tools/search-rerun.py` has no self-invocation mode (only `verify`)",
`corpus/lessons/round-95-verifier-spotcheck.md:133-135`, exit-2 receipt above).

### Q2 — §Gate standard requirements vs the r96 row

`PROTOCOL.md:375-421` requires of a gate row in `SKILL.md` (child-lane registry home, `PROTOCOL.md:398`):

1. **Verdict map (code → class).** `PROTOCOL.md:380-384`: "`0` = `clean` and `1` = `failed` fleet-wide;
   every other code a gate exits is declared in its registry entry and mapped onto
   `clean | failed | could-not-evaluate`."
   — r96 row at freeze (`SKILL.md:180`, cell 4): "`0` `SEARCH_RERUN: CLEAN` · `1` `DRIFT`
   (`COUNT_DRIFT`/`SET_DRIFT` …) · `2` `SEARCH_RERUN_ERROR <code>` setup or argparse usage".
   Covers 0, 1 and 2 with classes (CLEAN↔clean, DRIFT↔failed, setup/usage↔could-not-evaluate), matching
   the surface's §Flags phrasing (`SKILL.md:82,84`). **Satisfies §Verdict.**
2. **Self-test.** `PROTOCOL.md:385-389`: "Every gate exposes a self-invocation mode over isolated
   fixtures (temp trees, no network, no live-tree write) asserting both the exit code and a stable
   expected finding-id, with the expected values committed in the owning repo and independent of the
   recomputation. The flag spelling is the lane's (`--selftest`, `--self-test`, `run_selftest()`) …"
   — r96 row cell 5 names `python3 -B tools/search-rerun.py --selftest` → `SEARCH_RERUN_SELFTEST: PASS cases=32/32`,
   exit 1 `FAIL cases=k/32`. The flag spelling `--selftest` is one of the three the standard enumerates;
   the self-test at freeze (`tools/search-rerun.py:419-530`) is in-memory (no file/git/socket —
   `sed -n '419,530p' tools/search-rerun.py` contains no `open(`, `socket`, `subprocess` call; only the
   `m08-env-scrub` case touches `os.environ["GIT_DIR"]` and restores it), exits 0/1, and asserts per-case
   expected codes (`SECTION`, `HEADER`, `ENGINE`, `WHERE`, `EXPRESSION`, `REV`, `HIT_SET`, `ROW`, `TABLE`,
   and the `(0,1,1,[])`… judgement tuples through the shared `evaluate(rows, at_rev_of, at_tree_of, strict)`
   at `tools/search-rerun.py:353`). **Satisfies §Self-test on its face.**
3. **Registry row fields.** `PROTOCOL.md:401-403`: "Row fields: name, `gate|probe`, entry command,
   verdict map (code → class), self-test command and spelling, pinned-value path, write scope, owner."
   — r96 row cells: name "`search-rerun` (r96 re-registration …)" ✓; kind `gate` ✓; entry
   "`python3 -B tools/search-rerun.py verify <record> --root LANE [--strict]`" ✓; verdict map (cell 4, above) ✓;
   self-test command and spelling (cell 5, above) ✓; pinned-value path "corpus/fixtures/search-rerun-r95.md →
   `rev_match=8/8`; `corpus/knowledge/search-peer-review-dedup-r96.md` → `rev_match=8/8`" ✓ (the record is
   the persisted expected values committed in the repo, per `PROTOCOL.md:376-378`); write scope "none (as the
   r95 row; `--selftest` reads nothing)" ✓; owner "chousa" ✓.
   — Freeze check: `grep -c '^| \`search-rerun\` (r96 re-registration' SKILL.md` → `1`, kind cell `gate`
   (receipt `.ufo/waves/round-96/w1/R96RevenPrior-row.txt`, command `grep -c …`, exit 0, observed line 180
   with all seven fields). **Satisfies §Registry.**
4. **Two evidences / scope.** `PROTOCOL.md:390-411`: self-test green is capability, not measurement; scope
   read-only over surfaces it does not own. The r96 row asserts neither that the self-test is a measurement
   nor that it substitutes the committed record; write scope is `none`, and the entry command is read-only over
   the record and ROOT files. No conflict.

**Answer Q2: The r96 row satisfies every registry-field requirement enumerated in
`PROTOCOL.md:380-403` (verdict map 0/1/2 with classes, self-test command and an enumerated flag spelling,
pinned-value path, write scope, owner), and is in the permitted `gate|probe` vocabulary the r95 `tool`
kind violated.** Two caveats, both about the instrument rather than the row: (a) §Self-test's "expected
values committed in the owning repo and independent of the recomputation" is only partially met —
the 32 cases' expectations live in the tool itself (`tools/search-rerun.py:419-530`), so for the
parse/matching cases the expectation and the code are the same file; the claim's named limit (d) at
`claims.md:37-39` concedes this, and the external check is the battery's 23 mutants written outside the tool.
(b) §Self-test's "isolated fixtures (temp trees…)" is met by in-memory exclusion (the self-test reads
nothing, so it cannot write the live tree) rather than by temp-tree fixtures; the row's write-scope cell
states this. Neither caveat makes the r96 row non-conformant; both are disclosed.

### Q3 — other `tools/` instruments with no `--selftest` but registered as gates at base

Survey method: `tools/` = 21 files (`tools/*.py tools/*.sh`, counted by `ls | wc -l` → 21). A tool is
flagged "no `--selftest`" if `/usr/bin/grep -qi "selftest" <file>` finds no token. Exit-code probes
confirm all return 2 (argparse/unrecognised) for `--selftest`.

**No `selftest` token at base (14 of 21):**
`tools/absent-split.py`, `tools/argv-witness.py`, `tools/build-spans.py`, `tools/capture-fetch.py`,
`tools/capture-text.py`, `tools/digest-in-tree.py`, `tools/gate-records.py`, `tools/inference-ground.py`,
`tools/mechanism-witness.py`, `tools/quarantine-check.py`, `tools/quote-reopen.py`, `tools/receipt-pin.py`,
`tools/search-rerun.py`, `tools/store-record-audit.py`.
Receipts: `.ufo/waves/round-96/w1/R96RevenPrior-tools-survey.txt` (file list + token grep, exit 0) and
`.ufo/waves/round-96/w1/R96RevenPrior-no-selftest-exits.txt` (every one `--selftest` → exit 2).

**Have a `--selftest` flag (7 of 21):** `tools/assimilate-rows.py`, `tools/claims-audit-v2.py`,
`tools/claims-audit.py`, `tools/freeze-check.py`, `tools/lane-preflight.py` (its `--selftest` is the
test-harness that invokes others; it is itself named in lane-preflight), `tools/parent-lifetime.sh`,
`tools/research-gate.sh`.

**Of the 14, those registered as `gate` kind in `SKILL.md` `## Gates` at base** (routing candidates, not
C1's claim; the r96 freeze adds only search-rerun):

| tool | gate-kind row at base | self-test named in row |
|---|---|---|
| `tools/quarantine-check.py` | `SKILL.md:117` "`quarantine-check` round-42 gates \| gate" (tool exit 0/1/2; C1/C2 counters) | frozen counters `corpus/evidence/round42/c1-count.py`, `c2-count.py` — no `--selftest` on the tool |
| `tools/build-spans.py` | `SKILL.md:154` "round-56 … gate registration \| gate"; `SKILL.md:156` "round-61 … \| gate" | frozen counters `corpus/evidence/round56/c1-count.py`, `round61/c1-count.py` — the tool itself has no `--selftest` |
| `tools/receipt-pin.py` | `SKILL.md:166` "`receipt-pin` (r65) \| gate" | frozen counter `corpus/evidence/round65/c1-count.py` expects `CASES=20/20 C1=PASS` |
| `tools/digest-in-tree.py` | `SKILL.md:170` "`digest-in-tree` (r67) \| gate" | controls in `corpus/evidence/round67/controls/` (committed-fixture receipt, fake digest, digest-free receipt) — no tool `--selftest` |

**Of the 14, registered as something other than `gate` at base (for completeness; not routing candidates
under §Gate standard as written):**
`quote-reopen.py` (`SKILL.md:96,98` kind `tool`; counter kind `counter` at `SKILL.md:137`),
`gate-records.py` (`SKILL.md:97,98` kind `tool`), `inference-ground.py` (`SKILL.md:127` kind `tool`),
`capture-text.py` (`SKILL.md:144,149` kind `tool`), `absent-split.py` (`SKILL.md:118` kind `tool`),
`argv-witness.py` (`SKILL.md:109` kind `tool`), `mechanism-witness.py` (`SKILL.md:110` kind `tool`),
`build-spans.py` also has a `probe` row (`SKILL.md:152`, superseded by the gate rows), `capture-fetch.py`
and `store-record-audit.py` (no `## Gates` row cites them at base; `grep -n "store-record" SKILL.md` → no
match). Under `PROTOCOL.md:401-402` (`gate|probe` only) the six `tool`-kind rows are outside the registry
vocabulary in the same way the r95 search-rerun row was — but unlike search-rerun, none of them was
re-filed D1 at base, so they are the standing routing pool, not defects of C1. This confirms (by the lane's
own repeated pattern) that C1's "`--selftest` on the tool" is a stronger self-test than the
counter-as-self-test the lane uses elsewhere, and that D1's choice between the two disjuncts was open: either
disjunct is attested in the registry, but only the tool flag satisfies §Self-test's
"self-invocation mode" as literally written ("Every gate exposes a self-invocation mode"), since a frozen
counter in `corpus/evidence/` is not an invocation mode of the gate itself.
Receipt: `.ufo/waves/round-96/w1/R96RevenPrior-no-selftest-exits.txt` (each `--selftest` exit 2).

## Conclusion

- C1 is new: the tool gains `--selftest` at freeze (`tools/search-rerun.py:524`) where base had no such
  flag (`:378-392` required subcommand; exit 2 receipt). D1 was really open:
  `corpus/lessons/round-95-verifier-spotcheck.md:133-135` is accurate — kind `tool` outside `gate|probe`
  (`PROTOCOL.md:401-402` permits only `gate|probe`), and no self-invocation mode on the tool at base, only
  the external battery.
- The r96 row (`SKILL.md:180` at freeze) satisfies each §Gate-standard registry field
  (`PROTOCOL.md:376-403`): verdict map 0/1/2 with classes, a `--selftest` self-test whose flag spelling is
  enumerated in `PROTOCOL.md:388`, pinned-value path (the persisted records), write scope `none`, owner `chousa`.
- Routing pool (not this claim): `tools/quarantine-check.py`, `tools/build-spans.py`, `tools/receipt-pin.py`
  and `tools/digest-in-tree.py` are `gate`-kind with no `--selftest` on the tool, naming frozen counters as
  their self-test; `quote-reopen.py`, `gate-records.py`, `inference-ground.py`, `capture-text.py`,
  `absent-split.py`, `argv-witness.py` and `mechanism-witness.py` are registered under kind `tool` outside
  the permitted vocabulary — all are candidates for later D1-class repairs, none are C1's scope.

VERDICT: R96RevenPrior C1 held — the freeze's --selftest is new and D1 was open at base.
