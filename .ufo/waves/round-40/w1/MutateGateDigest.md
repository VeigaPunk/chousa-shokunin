# MutateGateDigest — R1 receipt-integrity predicate, gate-digest mutant

Round 40 / wave w1. Seat: mutation tester (leaf). Lane tip observed: `6bc90e04ac60307befacd554f7eee2b7284e2652`
(frozen claims' control tip was `691d26476ac39b8ec8b65155b41199e6f6d1f299`; re-observed baseline at the
current tip is unchanged, see §Baseline).

## Assigned attack

Alter an **active** receipt's gate digest while leaving the gate bytes unchanged, then re-run the committed
verifier and require the named mismatch refusal. Temporary copies only; no lane file touched.

- Target receipt: `corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json`
  (row 3 of `corpus/evidence/round40/active-r39-receipts.tsv`; re-sealed round-40 replacement).
- Gate (unchanged): `.ufo/waves/round-39/controls/mut-gate-path-env.sh`, sha256 `e1251030ef61…231a`.
- Defect shape: the receipt's three gate fields are re-pointed to the digest of the *adjacent committed gate*
  `tools/research-gate.sh` (`4253c18738f8…b07e3`) — the exact artefact a copy-paste receipt re-point produces.
- The mutant **re-seals `receipt_sha256`** with the verifier's own `receipt_digest()` recipe, so the
  receipt-self-digest check cannot mask the gate binding. This is the load-bearing part of the probe.

## Commands (exact)

Detector, run identically on pristine / mutated / restored bytes:

```
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/verify-receipts.py \
  --receipt /tmp/mut-gatedigest.g0v8zh2n/receipt.json \
  --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-39/controls/mut-gate-path-env.sh \
  --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/c1-count.py \
  --expectations /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/expectations.jsonl
```

Mutant construction (in-process, `/tmp` copy only):

```python
r = json.load(open(receipt)); decoy = sha256("tools/research-gate.sh")
r["gate_sha256_pre"] = r["gate_sha256_post"] = r["gate_sha256"] = decoy
r["receipt_sha256"] = vr.receipt_digest(r)          # verifier's own canonical reseal
json.dump(r, open(mut, "w"), indent=2, sort_keys=True); open(mut, "a").write("\n")
```

## Output

| Phase | receipt sha256 | rc | stdout |
|---|---|---|---|
| A pristine | `ac2c24fa1040…50fcb` | 0 | `VERIFY: ok receipt=receipt.json gate=mut-gate-path-env.sh counter=c1-count.py` |
| B mutated (re-sealed) | `6d1f8913dd0f…b34c4` | 1 | `VERIFY-FAIL: gate-sha256-mismatch` |
| C variant: stale seal | — | 1 | `VERIFY-FAIL: receipt-self-digest` |
| D variant: alias-only re-point, re-sealed | — | 1 | `VERIFY-FAIL: gate-sha-alias-mismatch` |
| E restored | `ac2c24fa1040…50fcb` | 0 | `VERIFY: ok receipt=receipt.json gate=mut-gate-path-env.sh counter=c1-count.py` |

Verdict: **killed**, by the named refusal. Gate bytes were never modified (`e1251030…231a` before and after);
only the receipt body changed and was re-sealed, so the kill is attributable to the gate binding and not to
the self-digest, counter, expectations, census, or verifier-identity checks — all of those passed on B before
the gate check fired (`verify-receipts.py:211-219` order).

## Frozen-predicate level (C1 detector)

Same defect injected into a fully temporary lane copy (`corpus/evidence/round39`, `corpus/evidence/round40`,
`tools/research-gate.sh`, `.ufo/waves/round-39/controls`), then `python3 <copy>/corpus/evidence/round40/c1-count.py`:

- A copy pristine: `R39_ACTIVE_RECEIPTS=6/6`, rc 0, all six `ok`.
- B copy with mutant: rc 1, the mutated row prints
  `corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json: fail VERIFY-FAIL: gate-sha256-mismatch`,
  all five other rows `ok`, `R39_ACTIVE_RECEIPTS=5/6`.
- C copy restored: `R39_ACTIVE_RECEIPTS=6/6`, rc 0.

So P1's code condition ("any verifier refusal is a miss") holds on this defect and the counter surfaces the
named refusal rather than a generic fail. Copy was discarded; the lane was never the tested tree.

## Baseline (pristine, lane tip)

`python3 corpus/evidence/round40/c1-count.py` → six `ok` lines, `R39_ACTIVE_RECEIPTS=6/6`, rc 0, at HEAD
`6bc90e0`. Manifest sha256 `e4623159…b40c`; counter sha256 `91618e91…05d5`; verifier sha256 `1b6e0de6…6267`;
expectations sha256 `01cbdc3a…583a`. Matches the frozen predicate; baseline is a pass, so refusals below are
not baseline noise.

## Calibration notes

1. **Redundant triple binding is real, not decorative.** Variant D shows the `gate_sha256` alias is checked
   independently (`gate-sha-alias-mismatch`), and B shows `gate_sha256_pre/post` are re-derived from the gate
   bytes (`gate-sha256-mismatch`). A single-field edit and the all-field edit are both refused.
2. **Re-sealing does not launder the gate.** B is the strongest form of the assigned defect (self-consistent
   receipt, correct counter/expect/verifier digests, frozen census satisfied) and still refuses.
3. **Seal ordering.** With a stale seal (C), `receipt-self-digest` fires first. That refusal is also correct
   but is not evidence about the gate binding; only B/D answer the assigned question.

## Coverage finding (not a contract change)

The verifier binds gate **bytes**, not gate **identity**: neither the manifest nor `expectations.jsonl` pins a
gate digest per receipt, so a receipt re-pointed to *different gate bytes together with* those bytes' digest
would pass. `[INFERENCE]` from `verify-receipts.py:211-219`; not exercised, because changing the gate is
outside this probe and the verifier docstring already names integrity/self-consistency as its contract
(the r37-F2 residual class). Recorded as a limit only.

## Restoration evidence

- Temp receipt restored byte-exactly: `ac2c24fa10406fad8c60cb7225b43632ccd8ac7fe5372df8b86d2ce5e8150fcb`
  before mutation and after restore, equal to the lane original; E re-verifies `ok`.
- Lane receipt and gate hashes after the probe: receipt `ac2c24fa…50fcb`, gate `e1251030…231a` — unchanged.
- Both `/tmp/mut-gatedigest.*` trees removed. No lane production file, git index, jj state, or fleet path
  written. No tools installed or updated; no pacman transaction.

## Artifact pointers

- This report: `.ufo/waves/round-40/w1/MutateGateDigest.md` (lane-relative; absolute
  `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-40/w1/MutateGateDigest.md`).
- Detector: `corpus/evidence/round39/verify-receipts.py`; gate check at lines 211-219.
- Predicate: `corpus/evidence/round40/c1-count.py`; population `corpus/evidence/round40/active-r39-receipts.tsv`.
- Target: `corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json`.
