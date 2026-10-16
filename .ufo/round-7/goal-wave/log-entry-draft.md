# LOG.md — round-7 entry draft (parent-owned file; integrate under [PARENT] markers)

<!-- SCRIBE DRAFT — MEASURED FINAL. Before: gate sha256
     0c3d51ed1a131146ac33eebf24eefe5830ecaaf3e59a1b03e6c91cd8debfd5f8
     (== `git show 4835426:tools/research-gate.sh`; lane HEAD 4835426),
     measured via an extracted copy. After: gate sha256
     3ba718bf9207eed70c66b8c849ac43b44c76890785e1576eeb5e795a604166b2
     (+536/−20 vs HEAD; stable ≥2 min before the battery, sha identical
     before and after it; the revision moved through ~11 hashes during the
     wave — Defect 2 of the report records the convergence). Lane HEAD still
     4835426; no commits by any seat. Scribe scratch
     $HOME/.cache/chousa-tmp/scribe-r7/ (declared ephemeral, cleaned at end
     of run). [PARENT] marks parent-only bindings. The debts section keeps
     the receipt-identity debt OPEN per the mission contract. -->

## 2026-10-16 — round-7 coverage: reference integrity — `verify-integrity` and the fifth composed section

Round 7 executes the move round 6 registered: binding integrity. Before it,
`verify-all` composed four sections that each checked their own rows, but
nothing checked the REFERENCES between rows: a Sweeps row could name an
undeclared `claim_id`, a Chain hop an undeclared `from` id, a Claims or
Negatives `sweep` cell an undeclared sweep row id, and the composed verdict
still read CLEAN (the round-6 omission-hunter's dangling class; re-measured
by this seat below). The operator dispatched this wave directly in-session
(same routing as rounds 2–6; **no Sighting step was invoked**); receipt
identity from round 1 remains open and untouched by this round.

**Before.** At gate `0c3d51ed…` (lane HEAD `4835426`), the r7 fixture pair
through an extracted r6 gate (race-free; the working gate was mid-landing):

```text
$ r6-gate verify-all corpus/fixtures/integrity-r7.md --root ..          → CLEAN run=4 (chain 4/4, sweeps 2/3) exit=0
$ r6-gate verify-all corpus/fixtures/integrity-r7-broken.md --root ..   → CLEAN run=4 (chain 4/4, sweeps 2/3) exit=0
  the hole: chain row 4 from=S9 and sweeps SW3 claim_id=C9 pass all six r1-r6 modes;
  chain alone on the twin verifies hop 4 (source=S4 …intake.md, at=line:11 verdict=match) —
  the `from` cell is never read.

scratch single-cell dangling variants of full-r6.md, same r6 gate:
  d1 Sweeps claim_id → Z9      → CLEAN run=4
  d2 Chain hop 3 from → C9     → CLEAN run=4
  d4 Claims sweep → SW9        → CLEAN run=4
  d5 Negatives sweep → SW9     → CLEAN run=4
  (controls: d3 hop to=S9 → DRIFT drift-sections=2; d6 sweep where=S9 → DRIFT drift-sections=1)
  grep -c 'INTEGRITY' tools/research-gate.sh = 0 ; grep -c 'REF_UNRESOLVED' = 0 at 0c3d51ed…
```

**The move.** `tools/research-gate.sh` (uncommitted, +536/−20 vs HEAD, gate
`3ba718bf…`): a SOLO mode `verify-integrity <record>` (dispatch
`:3390-3392`) plus its fifth `verify-all` section. Declared ids: source ids
from `## Sources`, claim ids from `## Claims` and `## Negatives`, sweep ids
from `## Sweeps`. Reference cells: chain `from`/`claim`/`to` (a `to`
fragment after `#` is cut), claims `sweep`/`source`/`src`/`ref`/`cite`/
`pointer`, negatives `sweep`/`where`, sweeps `claim_id`/`where`, rejections
`ref`/`reference`; tokens split on whitespace/commas/semicolons with edge
decoration trimmed. Classification (`integ_token` `:1733`): a token equal to
a declared id resolves (kind=source|claim|sweep); an UNDECLARED id-shaped
token (`S<digit>…`, `C|N<digit>…`, `SW<digit>…`) is `REF_UNRESOLVED`
severity=warn (drift) naming kind/id/section/row/cell; a non-local naming is
exempt (`reason=non-local`); local paths/globs, prose and sentinels are not
references and are not counted. An EXEMPT-STATUS row (chain
unresolved|blocked-no-fetch|rejected|labelled-dead|not-applicable; negatives/
sweeps unresolved|blocked-no-fetch|labelled-dead|not-applicable) has its
tokens counted exempt (`status=…`) rather than required to resolve; per-ref
lines `REF kind=… id=… section=… row=… cell=… observed=resolved|unresolved|exempt verdict=match|mismatch|exempt [status=|reason=]`,
summary `INTEGRITY refs=N resolved=M unresolved=K` (exempt = N−M−K), CLEAN
iff K=0 and no drift; exit 0/1/2 as before. `verify-all` composes five
sections (`VA_ORDER … integrity` `:1980`; integrity runs whenever ≥1 other
section runs, `:2027-2034`), prints `SECTION integrity … [tally=INTEGRITY …]`
and `VERIFY_ALL sections=5 …`; the `--json` manifest line carries the
integrity tallies + native string in the same `chousa-verify-all/v1` schema.

**Fixtures.** `corpus/fixtures/integrity-r7.md` (`4310ce86…`): the
`full-r6.md` bytes + a resolved hop 4 (`from=C3, to=S4`, line anchor at
`archived-export-intake.md:11`) + Sweeps SW3 bound to declared claim `C2`.
`integrity-r7-broken.md` (`fd4e213f…`): differs in exactly five lines — the
two planted dangling cells (row 4 `from=C3→S9`; SW3 `claim_id=C2→C9`) plus
its `claims_file`/`note`/`question` text; companions
`integrity-r7.claims.jsonl`/`-broken` (`8e83b23d…`, one sha);
`integrity-r7.README.md` (`df06b293…`) pre-registers the contract and the
before-state, and names the reshape (Defect 2 below).

**Selftest.** 64 → 74 cases, all PASS; case lines 1–64 BYTE-IDENTICAL
(`cmp` vs the r6 receipt's first 64). New cases 65–74: `integrity-pass`;
`integrity-fail-dangling-claim`; `-source`; `-chain-claim`; `-sweep`;
`integrity-exempt-counted` (exempt-status tokens exempt, URL exempt);
`integrity-fail-counting` (refs=9 resolved=5 unresolved=2 exempt=2); setup
`integrity-no-path`/`-missing-file` (exit 2); composed `all-dangling.md`
DRIFT through integrity alone.

**Measurements after the move** (gate `3ba718bf…`; stable ≥2 min, sha
identical before/after the battery; fresh processes; verbatim):

```text
$ verify-all corpus/fixtures/integrity-r7.md --root ..              → CLEAN (sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0) exit=0
    SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=16 resolved=15 unresolved=0
$ verify-all corpus/fixtures/integrity-r7-broken.md --root ..       → DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=2 drift=2) exit=1
    SECTION integrity state=run verdict=DRIFT findings=2 drift=2 tally=INTEGRITY refs=16 resolved=13 unresolved=2
    FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=source id=S9 section=chain row=4 cell=from
    FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=claim id=C9 section=sweeps row=SW3 cell=claim_id
  the integrity section is the ONLY drifting section and the two planted ids the only findings —
  the twin's pre-registered contract is met.

$ verify-integrity corpus/fixtures/integrity-r7.md --root ..        → CLEAN (refs=16 resolved=15 unresolved=0 exempt=1 findings=0 drift=0) exit=0
    exempt in place: REF kind=sweep id=SW2 section=negatives row=N2 cell=sweep observed=exempt verdict=exempt status=unresolved
$ verify-integrity corpus/fixtures/integrity-r7-broken.md --root .. → DRIFT (refs=16 resolved=13 unresolved=2 exempt=1 findings=2 drift=2) exit=1

scratch classes at the settled gate:
  d1 Z9 sweep cell            → CLEAN refs=12 resolved=11 — Z9 not id-shaped: not counted (shape boundary)
  d2 hop from=C9              → DRIFT 1 finding kind=claim id=C9 section=chain row=3 cell=from
  d3 hop to=S9                → DRIFT drift-sections=3: structure + chain + integrity all name S9
  d4 claims sweep=SW9         → DRIFT 1 finding kind=sweep id=SW9 section=claims row=C1 cell=sweep
  d5 negatives sweep=SW9      → DRIFT 1 finding kind=sweep id=SW9 section=negatives row=N1 cell=sweep
  d6 sweep where=S9           → DRIFT drift-sections=2: sweeps + integrity
  d7 https URL in a ref cell  → CLEAN, REF … observed=exempt verdict=exempt reason=non-local
  d8 local:// in a ref cell   → CLEAN, REF … observed=exempt verdict=exempt reason=non-local
  full-r6.md CLEAN (integrity 13/12); full-r6-broken.md DRIFT drift-sections=2 (chain+sweeps; integrity 13/12 CLEAN); full-r6-absent.md CLEAN run=4 absent=1 (integrity 2/2)

selftest            → RESEARCH_GATE_SELFTEST: PASS (74 cases); exit 0; case lines 1–64 byte-identical
regressions         → claims 17/17 CLEAN · chain 17/22 CLEAN + broken 1/2 DRIFT · sweeps 1/2+3/3 CLEAN +
                      broken 0/1+0/1 DRIFT · r1 verify CLEAN on the r6 pair · A/B/C each exit 1 (3/3)
exit contract       → CLEAN 0 / DRIFT 1 / setup 2 (missing record; unknown flag; --json dir missing;
                      --json path is a dir; --json/--claims outside verify-all)
manifest (--json)   → 2 appends; line 1 byte-stable across append 2; schema chousa-verify-all/v1,
                      sections_run=5, integrity {refs:16,resolved:15,unresolved:0,exempt:1,findings:0,drift:0}
                      + native INTEGRITY refs=16 resolved=15 unresolved=0 (CLEAN line); {16,13,2,1,2,2} (DRIFT line)
zero network        → strace -f -e trace=network, composed run: 0 network lines of 7976; exit 0
```

**Named limits (measured by this seat).** The id-SHAPE boundary: only
S/C|N/SW+digit-shaped tokens are references — `Z9` (d1) is invisible
(measured CLEAN, refs drop). Exempt classes stay exempt-but-counted, pinned
by case 70 and measured in place (N2 sweep=SW2 `status=unresolved`; URL and
`local://` namings `reason=non-local`). Wave convergence: the first fixture
shaping put the source defect behind an exempt hop and measured one finding
instead of two at `3ba718bf…` on the first fixture shas
(`e2dfc7de…`/`7af72514…`); the author re-shaped the pair to a non-exempt
`resolved` hop (settled `4310ce86…`/`fd4e213f…`) and the README now names
the class boundary — the settled contract measures exactly two findings.
Manifest growth: `sections_run=5` + the integrity tallies object under the
same v1 schema (consumers that pinned `sections=4` read stale). Banner still
`research-gate-r1` (cosmetic, carried).

**Admission.** [PARENT: ADMIT/REJECT line + commit hashes; no scalar; axis
verdicts live in SCORECARD.md's round-7 sections.]

**Debt.** Receipt identity (round 1) STILL OPEN — no authentic queue
taskKey/expected receipt bag exists; mission acceptance is integrator-owned,
no `task_…` value was invented, proven receipt-backed completed rounds remain
0, operator target unchanged (≥100). Round-7 artifacts at draft time
(uncommitted): gate `3ba718bf…` (+536/−20), fixtures + README (shas above),
lesson `corpus/lessons/2026-10-16-reference-integrity.md` (19506 B,
`8c047145…`), `SKILL.md` r7 rows (`99930459…` at check) [PARENT: note
`corpus/knowledge/reference-integrity-r7.md`, receipts, `corpus/README.md` /
`corpus/evidence/README.md` rows — not landed by 03:03Z when this seat last
checked; integrate only what lands]. Carried debts: the
id-shape boundary; manifest schema growth; nested execution cost (up to five
subprocesses per composed run); absent!=drift omission limit (r6); non-vacuous
flip screening (r5); non-author spot-check (integrator/operator); carried
residuals (in-root hardlinks, no source size cap, token-aligned shortening,
non-ASCII-adjacent fail-closed edges, scope-refusal finding IDs, frozen-replay
comparator). Lane hygiene: no commits by seats.