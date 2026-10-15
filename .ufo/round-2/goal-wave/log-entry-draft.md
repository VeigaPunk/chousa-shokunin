# LOG.md — round-2 entry draft (parent-owned file; integrate under [PARENT] markers)

<!-- SCRIBE DRAFT. Measured values from the frozen gate revision
     sha256 03a3324455852ea0025115cb0e3ba9c8cdea10da5edc051c4738854a27c14be0
     and the receipts under corpus/evidence/claims-r2-20261015T233027Z-*.log
     (the 232752Z set's selftest line is the superseded quota false negative).
     Lane HEAD at draft time: 6344569. -->

## 2026-10-15 — round-2 coverage: claim-vs-source verification

Round 2 executes the move round 1's continuation pre-registered: a local-only
claim-verification fixture with agreeing, disagreeing and silent sources. The
operator dispatched this wave directly in-session, so the wave ran without a
fleet-rendered route binding and **no Sighting step was invoked**; receipt
identity from round 1 remains open and untouched by this round.

**Before.** The shipped round-1 gate (sha256 `08843552…`, lane HEAD `6344569`)
has no claim-vs-source mode — `grep -c 'verify-claims' tools/research-gate.sh`
is 0 — and run over the real 17-claim fixture it reports `claims=0`, DRIFT,
exit 1. No claim was ever checked against its cited source. Captures:
`corpus/evidence/claims-r2-20261015T232752Z-live.log:9-18` and the scribe's
`/tmp/chousa-scribe-before.txt` (2026-10-15T23:15:27Z).

**The move.** New `verify-claims <claims-file>` mode
(`tools/research-gate.sh:710-859`; usage `:84`; dispatch `:1465`). One JSON
claim per line `{"id","source","span","expect"[, "marker"]}`; blank/`#` lines and
a `{"marker_default":…}` line are allowed. Each claim's span is byte-matched
against its cited **local** source, canonicalized and confined to `CHOUSA_ROOT`
or the lane root (`:655-708`): URLs → `CLAIM_SOURCE_EXTERNAL` crit
("url source refused (no external fetch)"), session/denylist →
`CLAIM_SOURCE_SESSION` crit, ephemeral → warn, outside both roots →
`CLAIM_SOURCE_OUT_OF_CORPUS` crit, unreadable → `CLAIM_SOURCE_MISSING` warn —
all **refused before any read**. Per claim: `CLAIM id=… expected=… observed=…
source=… at=… verdict=…`; then `VERDICT_BEARING_CLAIMS=N/M` and
`RESEARCH_GATE: CLEAN|DRIFT (claims=… supported=… contradicted=… unsupported=…
mismatched=… unproven=… refused=… invalid=… findings=… drift=…)` (`:851-855`).
`contradicted` is structural: a declared marker literal must co-occur inside the
span's source lines, else `unproven`. Exit contract unchanged (0 CLEAN /
1 DRIFT / 2 setup).

**Fixture (pre-registered).** `corpus/fixtures/claims-r2.jsonl`, sha256
`23d078cbfd032ec5ee7de5c21de65eba3a3cd2989a78281ff61bc6db62188802` — 17 real
claims over the three archived inputs at pinned sha256s (A `9033857d…`,
B `6d8dbddd…`, C `e48fe70f…`): 13 supported, 2 contradicted with literal
markers (`could not substantiate` at A05, `is not a standard rank sequence` at
C06), 2 unsupported near-misses (A06 dropped-`do not`; B05 fabricated
"exclusively to worker agents"). Contract:
`corpus/fixtures/claims-r2.README.md` sha256 `44d8a890…` (expected
`claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0`, CLEAN,
exit 0). Authored before the mode existed (gate sha `088435…`, zero
`verify-claims` tokens), so the expectations are a genuine pre-registration. The
fixture's own gate-free byte-check (run before the implementation landed and
independently by the receipts writer): `counts {'supported': 13, 'contradicted':
2, 'unsupported': 2} bad []`, exit 0.

**Measured at frozen gate sha256 `03a3324455852ea0025115cb0e3ba9c8cdea10da5edc051c4738854a27c14be0`:**

```text
bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..
… 17 x CLAIM … verdict=match (at= 52,80,81,88,64,-,47,64,79,69,-,89,92,97,102,130,53)
VERDICT_BEARING_CLAIMS=17/17
RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)
exit=0

bash tools/research-gate.sh --selftest
RESEARCH_GATE_SELFTEST: PASS (30 cases)
exit=0   # round-1 cases 1-20 byte-identical; new cases 21-30 claims/setup

# regression at CHOUSA_NOW_EPOCH=1760000000
verify A/B/C → exit 1 each, stdout byte-identical to the r1 baseline; intake → exit 0; VERDICT_BEARING_EXPORTS=3/3
```

**Negative controls** (receipts `corpus/evidence/claims-r2-20261015T233027Z-live.log`, all exit 1): tampered span A03
`nine`→`ten` → `CLAIM_SPAN_NOT_FOUND`, A03 mismatch, 16/17; external URL X01 →
`refused` + `CLAIM_SOURCE_EXTERNAL` crit, 17/18; out-of-corpus `/etc/hostname`
X02 → `refused` + `CLAIM_SOURCE_OUT_OF_CORPUS` crit, 17/18; contradicted without
marker A05 → `unproven`, 16/17. Setup: no path / missing file → exit 2, stdout
empty.

**Environment defect, named, resolved in-wave.** The first receipts pass ran
while the host `/tmp` tmpfs (carrying `usrquota`) hit its shared user quota; its
selftest capture failed —
`corpus/evidence/claims-r2-20261015T232752Z-selftest.log` records `exit: 1` with
`tools/research-gate.sh: line 873: printf: write error: Disk quota exceeded` —
and its case-line diff is a false negative from the same exhaustion, not a gate
regression. The frozen revision honors `TMPDIR` (`:863-872`); the corrected
receipts set `…-20261015T233027Z-selftest.log` re-ran under
`TMPDIR=/home/vgpnk/.cache/chousa-r2/tmp` → `RESEARCH_GATE_SELFTEST: PASS (30
cases)`, exit 0, round-1 case lines 1-20 byte-identical (the scribe independently
reproduced that PASS). The `232752Z` selftest line is the superseded
environment-blocked capture; the fleet `/tmp` quota remains an environment-owned
item.

**Not claimed.** A CLEAN `verify-claims` run establishes span byte identity at a
reported first-occurrence line inside the allowed local roots, plus literal
marker co-occurrence for `contradicted`; it does **not** establish semantic
support, source truth, location uniqueness, external verification, or adoption.
The mode reads `id/source/span/expect[/marker]` only — the `claim` sentence is
never compared with its span, so a claim label can assert the opposite of its
span and still close CLEAN (`corpus/README.md` Known gaps;
`corpus/lessons/2026-10-15-claims-span-fidelity.md`). Fixture spans are byte
controls, not knowledge (B03 numerals remain kengaku-province material, RJ-03).
No older admitted entry was reverified; no non-author spot-check; no promotion.
Receipt identity remains open.

### Evidence paths

`corpus/evidence/claims-r2-20261015T233027Z-{fixture,gate,live,selftest}.log`
(corrected set; the 232752Z selftest line is the superseded quota false
negative) · `corpus/fixtures/claims-r2.jsonl`, `corpus/fixtures/claims-r2.README.md` ·
`corpus/knowledge/claim-verification-r2.md` · `SKILL.md` gate rows ·
`corpus/lessons/2026-10-15-claims-span-fidelity.md` ·
`corpus/README.md` coverage rows (landed).
