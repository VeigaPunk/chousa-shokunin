# chousa-shokunin — corpus/evidence

Round-2 receipts for the claim-vs-source verification move (round 2, coverage
axis). Each receipt is a machine-cut capture of public-CLI runs: UTC stamp,
exact command, exit code, pinned gate SHA-256, and the verbatim stdout. Local
files only — no external fetch, no network.

## Round-2 claim-verification receipts — stamp 20261015T233027Z

Revision under test: `tools/research-gate.sh` sha256
`03a3324455852ea0025115cb0e3ba9c8cdea10da5edc051c4738854a27c14be0`
(lane HEAD `6344569`). Fixture `corpus/fixtures/claims-r2.jsonl` sha256
`23d078cbfd032ec5ee7de5c21de65eba3a3cd2989a78281ff61bc6db62188802`; its
contract is `corpus/fixtures/claims-r2.README.md` sha256
`44d8a890406f0802986adb7b92c653c53d2548ffe7976911250f01c76c48e3e7`.

| Receipt (sha256) | Shows | Key result |
|---|---|---|
| `claims-r2-20261015T233027Z-fixture.log` (`cef0297a…`) | fixture inventory, pinned inputs, two independent byte-checks | `counts {'supported': 13, 'contradicted': 2, 'unsupported': 2} bad []`; independent span check 17/17 ok |
| `claims-r2-20261015T233027Z-selftest.log` (`b202d835…`) | full `--selftest` | `RESEARCH_GATE_SELFTEST: PASS (30 cases)`, exit 0; case lines 1–20 byte-identical to the r1 baseline |
| `claims-r2-20261015T233027Z-gate.log` (`5b8c9880…`) | round-1 regression over the three archived inputs (frozen clock) | each exit 1 with one `RESEARCH_GATE: DRIFT` summary; `VERDICT_BEARING_EXPORTS=3/3`; all three byte-identical to the frozen r1 baseline |
| `claims-r2-20261015T233027Z-live.log` (`672797bb…`) | before-state (r1 gate on the claims file), live `verify-claims`, four negative controls | live `VERDICT_BEARING_CLAIMS=17/17` + `RESEARCH_GATE: CLEAN (claims=17 … mismatched=0)`, exit 0; each control DRIFT, exit 1 |

Before → after in one line: the r1 gate on the same claims file is
structure-only (`FINDING RECORD_SCHEMA_INVALID`, `… CLAIM_TABLE_ABSENT`, DRIFT
findings=5); the new `verify-claims` mode adjudicates each claim's verbatim span
against its cited source and closes CLEAN with `claims=17 verified=17`.

### Negative controls (recorded in the live receipt)

Each control is a scratch copy of the fixture (deltas are printed in the
receipt); every one drifts with exit 1.

| Control | Delta | Finding | Summary |
|---|---|---|---|
| tampered span | A03 `nine years` → `ten years` | `CLAIM_SPAN_NOT_FOUND` | 16/17, DRIFT |
| external URL source | X01 `https://example.invalid/x.md` appended | `CLAIM_SOURCE_EXTERNAL` (crit), refused, never fetched | 17/18, DRIFT |
| out-of-corpus source | X02 `/etc/hostname` appended | `CLAIM_SOURCE_OUT_OF_CORPUS` (crit) | 17/18, DRIFT |
| contradicted without marker | A05 `marker` removed | `CONTRADICTION_MARKER_ABSENT` | 16/17, unproven=1, DRIFT |

## Round-1 evidence

- `round-1/expected.json`: archive content digests and expected CLI verdicts
  for the three baseline inputs.

The round-1 acceptance and final-intake JSON live under
`../.ufo/evidence/round-1/` (lane evidence dir).

## Re-run recipe

From the lane root, local only. Exit contract for every run: 0 CLEAN,
1 DRIFT, 2 setup/usage.

```bash
# 0. pin the revision (receipts were cut at this sha)
sha256sum tools/research-gate.sh
#   03a3324455852ea0025115cb0e3ba9c8cdea10da5edc051c4738854a27c14be0

# 1. fixture + live claim verification
bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..
#   expect: 17 CLAIM lines all verdict=match, VERDICT_BEARING_CLAIMS=17/17,
#   RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0), exit 0

# 2. selftest (honours ${TMPDIR:-/tmp}; set TMPDIR if /tmp is crowded)
bash tools/research-gate.sh --selftest
#   expect: RESEARCH_GATE_SELFTEST: PASS (30 cases), exit 0

# 3. round-1 regression count (the scorecard observable)
python3 -c 'import subprocess; names=("A-shokunin-tradition.md","B-multiagent-knowledge.md","C-rank-taxonomy.md"); rows=[subprocess.run(["bash","tools/research-gate.sh","verify","../research/deep-research-2026-09-28/"+n,"--root",".."],capture_output=True,text=True) for n in names]; print("VERDICT_BEARING_EXPORTS=%d/3" % sum(r.returncode==1 and sum(s.startswith("RESEARCH_GATE: DRIFT (") for s in r.stdout.splitlines())==1 for r in rows))'
#   expect: VERDICT_BEARING_EXPORTS=3/3

# 4. fixture provenance byte-check without the gate
#   run the python block in corpus/fixtures/claims-r2.README.md §Re-run
#   expect: counts {'supported': 13, 'contradicted': 2, 'unsupported': 2} bad []
```

### Notes

- Receipts pin gate revision `03a33244…`. If `tools/research-gate.sh` is edited
  again, re-run the recipe above and re-cut; a superseded receipt is not a
  claim about the later revision.
- The receipts were machine-cut by `cut-receipts.sh` (seat scratch, retained
  during the wave at `/home/vgpnk/.cache/chousa-r2/cut-receipts.sh`; not a lane
  file). The recipe above is self-contained and needs no scratch dir.
- Where a receipt records a path under `/home/vgpnk/.cache/chousa-r2/`, that is
  the seat scratch dir: the host `/tmp` intermittently returned `Disk quota
  exceeded`, so scratch and the gate's `TMPDIR` were pointed there. The
  receipts' own runs resolve all sources inside the fleet root.
- The round-2 scribe draft referred to `corpus/evidence/round-2/`; these
  receipts live directly under `corpus/evidence/` as
  `claims-r2-<UTCstamp>-{fixture,selftest,gate,live}.log`, per the
  receipts-writer seat directive. Parent integration can move them, but the
  receipt contents pin their own names.