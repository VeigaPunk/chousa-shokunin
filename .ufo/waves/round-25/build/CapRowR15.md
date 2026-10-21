# Round 15 capability-row review

## Evidence

- `LOG.md:622` identifies Claim 1 as “the `--root /` boundary dead-arm” and says absolute in-`/` sources read after the fix; before-behavior was pinned. `LOG.md:626` records the round-15 verdict: “coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1.”
- `SCORECARD.md:735-740` names the capability as the `--root /` boundary dead-arm: root `/` made the prefix pattern `//*`, so absolute in-`/` sources were falsely refused as `CLAIM_SOURCE_OUT_OF_CORPUS`. `SCORECARD.md:751-760` says the `in_root()` helper strips the trailing slash for prefix checks and all three same-class sites (`claim_source_path`, `ptr_resolves_meta`, `sweep_path_guarded`) were converted.
- No Round 15 capability row is present after the Round 14 addition (`SCORECARD.md:727-733`); `SCORECARD.md:1278-1280` explicitly lists Round 15 among the unbackfilled capability acquisitions.

## Pinned-base rerun

Cloned to `/tmp/chousa-r25-CapRowR15`, switched to `b820e4e40ce52deedf53b191140cd7b08ddda929`; observed `git rev-parse HEAD` returned that exact hash. Ran `bash tools/research-gate.sh --selftest` there: `RESEARCH_GATE_SELFTEST: PASS (136 cases, 0 skipped)`.

Relevant `ok-case` output from that run (verbatim):

```text
ok-case  107 claims-root-slash-absent     exit=1
ok-case  108 claims-root-slash-read       exit=0
ok-case  109 claims-root-slash-xdev       exit=1
ok-case  110 claims-root-dslash           exit=0
ok-case  111 sweeps-root-slash            exit=0
```

The current pinned-base run's case 110 is the distinct double-slash claim test; the Round 15 sweep case is now 111. The original Round 15 receipt records its four cases as 107–110, with `sweeps-root-slash` at 110 (`corpus/evidence/root-r15-20261019T152000Z-selftest.log:107-111`). The evidence index confirms the Round 15 receipt and `/etc/hostname` demo (`corpus/evidence/README.md:640-643`).

## Proposed SCORECARD row (not applied)

| root-slash source resolution | Reads a same-device absolute claim source under `--root /` instead of falsely refusing it as `CLAIM_SOURCE_OUT_OF_CORPUS`. | Round 15 receipt selftest cases 107–110 (`corpus/evidence/root-r15-20261019T152000Z-selftest.log`); pinned-base rerun cases 107–109, 111; `corpus/knowledge/root-slash-boundary-r15.md` | 15 |

## Residual risk and verification gaps

- The requested gate selftest passed. I did not rerun the separate live `/etc/hostname` demo; the recorded before/after demo is indexed at `corpus/evidence/README.md:641`.
- No `lsp` device is mounted (`read xd://lsp` returned “No such tool” and listed mounted devices without `lsp`); source text and the pinned-clone run are the evidence here. Text search was used only to locate literal references, not as semantic proof.
- No installs. No SCORECARD or other lane source file was edited.

VERDICT: Evidence supports backfilling a Round 15 capability row; use the current case mapping as shown so case 110 is not misattributed.