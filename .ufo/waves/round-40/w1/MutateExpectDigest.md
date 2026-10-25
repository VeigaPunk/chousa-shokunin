# Mutation probe — active receipt `expect_sha256` (round 40, w1)

Seat: `MutateExpectDigest` (leaf). Assigned attack: on a temporary copy only, alter one active
receipt's `expect_sha256`, re-run the committed verifier, record the exact refusal, and show no
repository artifact changes.

Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`
Observed lane HEAD: `6bc90e04ac60307befacd554f7eee2b7284e2652` (claims' control tip `691d264`, measurement
tip `d164f88`; `git diff --stat d164f88..HEAD -- corpus/evidence/round39 corpus/evidence/round40
tools/research-gate.sh` = only `corpus/evidence/round40/measure-after.txt | 51 +`, so the probed bytes
are unchanged since measurement).

Target receipt: `corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json` (active row of
`corpus/evidence/round40/active-r39-receipts.tsv`; gate `tools/research-gate.sh`, counter
`corpus/evidence/round39/c1-count.py`, expectations `corpus/evidence/round39/expectations.jsonl`).

## Mutation

Smallest behavior-bearing change: one hex nibble of the expectation binding.

- pristine `expect_sha256`: `01cbdc3a8208a257e2b0ea4304c87a6d74be313a722cf667c5d126a4c29c583a`
  (equals `sha256(corpus/evidence/round39/expectations.jsonl)` = live file)
- mutant `expect_sha256`: `01cbdc3a8208a257e2b0ea4304c87a6d74be313a722cf667c5d126a4c29c583b`
- pristine receipt file SHA-256: `482e716a4d5a57b5f9f62c3652b82b72ae21e3255b61f4b18d1edc35d99bd131`
- mutant file SHAs (deterministic rebuild, `json.dumps(..., indent=2, sort_keys=True) + "\n"`):
  - M1 (raw edit, `receipt_sha256` untouched): `936d1ef939bb1aa3d69a63135ea1df096e61c23dafae8f0a8433f8ec3820e7f4`
  - M2 (same edit, `receipt_sha256` resealed over the doctored body): `63b19737cd930416e768e9abc11e22f585fb24a5722e69d424d92cc430b515c8`
  - M3 (same shape, but `expect_sha256` set to the *historical* stale digest
    `3abd2dcb1766c404228cf3929024856240a93ea374760ab77a390b92c3fb6480` from
    `.ufo/waves/round-40/controls/r1-stale-before.txt`, resealed):
    `db3afcbea8ccac6186e6d37acc48c52d445881665b4cc8705b9db36cb3b3bbaa`

All mutation work happened under `mktemp -d` (`/tmp/mutesp-*`), never in the lane tree.

## Detector: committed verifier on committed bytes (baseline, must pass first)

Command (cwd = lane root):
```
python3 corpus/evidence/round39/verify-receipts.py \
  --receipt corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json \
  --gate tools/research-gate.sh \
  --counter corpus/evidence/round39/c1-count.py \
  --expectations corpus/evidence/round39/expectations.jsonl
```
Output: `VERIFY: ok receipt=c1-after-s39011-regenerated.json gate=research-gate.sh counter=c1-count.py`, rc=0.

Baseline counter: `python3 corpus/evidence/round40/c1-count.py` → last line `R39_ACTIVE_RECEIPTS=6/6`, rc=0.

## Mutant results (verifier, mutated copy)

| variant | command | rc | exact output |
|---|---|---|---|
| M1 raw edit | same verifier, `--receipt /tmp/mutesp-*/mutated.json` | 1 | `VERIFY-FAIL: receipt-self-digest` |
| M2 resealed | same verifier, resealed copy | 1 | `VERIFY-FAIL: expect-sha256-mismatch` |
| M3 stale-digest resealed | same verifier, historical stale digest | 1 | `VERIFY-FAIL: expect-sha256-mismatch` |

Expected detector: `VERIFY-FAIL: expect-sha256-mismatch`, exit 1 (per `expectations.jsonl` row
`expect-tamper-detected` and the committed before-control). M2/M3 meet it exactly. M1 refuses one
check earlier — see finding F1.

## Counter-level kill (replica temp tree, no lane writes)

Replica `T` = copies of `c1-count.py`, the six-row manifest, and the three round-40 receipts, with
symlinks `T/corpus/evidence/round39`, `T/tools`, `T/.ufo/waves/round-39` → lane (so gate/counter/
verifier hashes are the committed bytes). Command: `python3 corpus/evidence/round40/c1-count.py`, cwd=T.

- Control (byte-identical copy): `R39_ACTIVE_RECEIPTS=6/6`, rc=0 — the replica itself is sound, so a
  later miss is attributable to the mutant, not the harness.
- M1: target row `...: fail VERIFY-FAIL: receipt-self-digest`; other five `ok`; `R39_ACTIVE_RECEIPTS=5/6`, rc=1.
- M2: target row `...: fail VERIFY-FAIL: expect-sha256-mismatch`; `R39_ACTIVE_RECEIPTS=5/6`, rc=1.
- Restored (pristine bytes copied back into T): `R39_ACTIVE_RECEIPTS=6/6`, rc=0.

Verdict: **killed**. Both the receipt self-digest and the frozen `expect_sha256` binding are live;
the C1 counter's aggregate goes 6/6 → 5/6 with the named refusal, so P1's kill rule demonstrably fires.

## Restoration and no-change evidence

- Repo target receipt SHA before all runs: `482e716a…d99bd131`; after all runs: `482e716a…d99bd131`
  (identical to the restored copy hash in T).
- 18 probed lane artifacts (active + superseded receipts, verifier, expectations, round-39/40
  counters, manifest, claims, gate) hashed before and after: **zero changed**.
- `git status --porcelain` before: `M .ufo/waves/round-40/w1/swarm-registry.json` (pre-existing
  harness edit) + untracked sibling report; after: same modified file plus sibling-authored
  `CriticC1Predicate.md`, `CriticR4Disposition.md`, `CriticSourceClaim.md`, `ScoutHashSource.md`,
  `ScoutProvinceBoundary.md`. No production path appears; this report is the only artifact I wrote.
- Temp dirs `/tmp/mutesp-2rtywpcf`, `/tmp/mutesp3-*` removed (`TEMPS_GONE True`).
- No tool installed or updated; no lane git/jj state touched.

## Calibration / coverage findings (not contract violations)

- **F1 — check-order shadowing.** A literal `expect_sha256` edit is refused as
  `VERIFY-FAIL: receipt-self-digest`, because `receipt_sha256` is verified before the expectation
  binding. A tester who asserts `expect-sha256-mismatch` on an unsealed edit would mislabel a real
  kill as a miss. Only a resealed body (M2) exercises the claimed expectation check; I ran both.
- **F2 — the digest is the binding, not the path string.** The verifier compares
  `receipt["expect_sha256"]` against the bytes of the `--expectations` argument; the receipt's own
  `expectations` field and its absolute `gate` field are never compared to the arguments (gate binds
  only via `gate_sha256`). Under P1 (digest equality) this is sound; a path-only mutation would be a
  no-op mutant and is not worth spending a probe on.
- **F3 — population check is path-string based.** `c1-count.py` requires six unique manifest *path
  strings*; two rows pointing at identical receipt bytes under different paths would count twice.
  P1 only freezes "six active rows, no duplicate row", so this is a coverage edge, not a defect.
- **F4 — historical defect class reproduced.** The committed before-control
  (`.ufo/waves/round-40/controls/r1-stale-before.txt`) shows the four superseded originals refusing
  exactly `expect-sha256-mismatch` (three) and `counter-sha256-mismatch` (one). The M3 mutant using
  the real stale digest `3abd2dcb…` is refused with the same token, while all six active rows bind
  the live digest `01cbdc3a…`. The regeneration clears the named defect rather than dead-checking it.
- **F5 — verifier identity is checked after the counter and expectation bindings**, so a replaced
  verifier copy plus stale expectations refuses as `expect-sha256-mismatch` (or
  `counter-sha256-mismatch`), not `verifier-sha256-mismatch`. The docstring's "first binding check"
  holds only among the round-39-added bindings, after the round-38 ones. Observation only: the c2
  expectation row `verifier-subject-rebind` still proves `verifier-sha256-mismatch` fires on a
  replaced verifier with otherwise-current bytes.

## Reproduction

```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
T=$(mktemp -d); python3 - "$T" <<'PY'
import hashlib, json, sys, pathlib
src = pathlib.Path("corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json")
d = json.loads(src.read_text()); d["expect_sha256"] = d["expect_sha256"][:-1] + "b"
body = {k: v for k, v in d.items() if k != "receipt_sha256"}
d["receipt_sha256"] = hashlib.sha256((json.dumps(body, indent=2, sort_keys=True) + "\n").encode()).hexdigest()
pathlib.Path(sys.argv[1], "m.json").write_text(json.dumps(d, indent=2, sort_keys=True) + "\n")
PY
python3 corpus/evidence/round39/verify-receipts.py --receipt "$T/m.json" \
  --gate tools/research-gate.sh --counter corpus/evidence/round39/c1-count.py \
  --expectations corpus/evidence/round39/expectations.jsonl; echo "rc=$?"; rm -rf "$T"
```
Expected: `VERIFY-FAIL: expect-sha256-mismatch`, `rc=1` (drop the reseal step → `receipt-self-digest`).

Artifact pointers: this report; `.ufo/waves/round-40/controls/r1-stale-before.txt`;
`.ufo/waves/round-40/controls/control-before.txt`; `corpus/evidence/round39/verify-receipts.py`;
`corpus/evidence/round40/c1-count.py`; `corpus/evidence/round40/active-r39-receipts.tsv`.
