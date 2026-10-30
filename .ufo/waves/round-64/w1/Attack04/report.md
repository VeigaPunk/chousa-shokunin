# Attack04 — C1 zero-gate semantics

Axes: oracle fidelity; frozen-claim honesty; production/candidate separation; bounded reproducibility. Advisory findings only; no admission or integration.

## Findings by severity

### High — known frozen E12/E13 mismatch prevents an honest C1 pass

`corpus/evidence/round64/c1-battery-v3.py:386–394` draws `tag()` independently for each filename and its README reference. Bounded fixture generation with seed `Attack04/E12` created `escaped_q10aad31d.md` but referenced `escaped\_q8e789eec.md`; E13 created `gate notes q47c548cb.md` but linked `gate%20notes%20q4a206a01.md`. These are unindexed files plus phantom references, not benign normalization fixtures. The frozen leg table nevertheless expects exit 0 (`:442–443`). A conforming G02 must reject these fixtures under `claims.md:47–59`.

Read-only `git show bf40d99bda9eefdad3ed6276da077cfb24ba82f1:corpus/evidence/round64/c1-battery-v3.py` exited 0. Its bytes equal the current frozen file, SHA-256 `4b3f0b658bcd3bb640cd2e6e56a28a91a72d5352f2610887db01e636fc039fe2`. This is a frozen instrument defect, not a newly introduced production regression. The full target is not established and cannot honestly be inferred from the supplement: the kill rule (`claims.md:89–93`) requires the unmodified frozen battery. No full battery rerun was performed or represented as performed.

The inherited `c1-battery-supplement.py` reuses one draw in each fixture; fixture-only probes confirmed consistent references. `diff -u` exited 1 and showed only those two constructor repairs. This distinct supplement does not repair or admit the frozen claim.

### Medium — ZERO oracle accepts a positive run count and arbitrary summary sets

Frozen `c1-battery-v3.py:480–487` checks exit 2, all eight statuses SKIP, and summary group **1** equal to `"0"`. Group 1 is the PASS numerator (`:131`), not the run denominator. It returns before the denominator/FAILED/ENV/SKIPPED consistency checks at `:503–516`.

Minimal counterexample: emit the eight correct ordered SKIP lines, exit 2, then print:

```text
PREFLIGHT=0/8 FAILED=none ENV=none SKIPPED=G01,G02,G03,G04,G05,G06,G07,G08
```

The actual frozen `judge('Z01', {'rc': 2, 'zero': True}, 2, stdout, '')` returned `(True, 'ok')`. This contradicts its own frozen ZERO text (`:51–54`): `PREFLIGHT=0/0`, never a positive run count. Two additional accepted counterexamples were `PREFLIGHT=0/0 FAILED=G01 ENV=G02 SKIPPED=none` and `PREFLIGHT=0/0 FAILED=garbage ENV=garbage SKIPPED=garbage`.

All three invalid summaries were also accepted by the supplement and inherited round63 `c1-battery-v2.py`. The supplement's complete judge source equals the frozen v3 judge. The inherited judge as a whole is not byte-identical (the probe records this honestly), but its ZERO branch at `round63/c1-battery-v2.py:352–359` has the same incomplete checks. Thus this is inherited oracle weakness retained by the supplement, not evidence that current production emits the bad summaries. Route this falsifier to a distinct future instrument per the frozen rule; do not edit frozen predicates or claim closure from it.

## Production and candidate observations

The six bounded real invocations (Z01/Z02/Z03 against production and candidate separately) all exited 2, emitted eight ordered SKIP lines and exactly:

```text
PREFLIGHT=0/0 FAILED=none ENV=none SKIPPED=G01,G02,G03,G04,G05,G06,G07,G08
```

No stderr; frozen judge accepted all six. Production's actual canonical logic is `tools/lane-preflight.py:302–322`: selection prints SKIP, `ran` excludes SKIP, the summary derives its denominator from `len(ran)`, and `not ran` selects exit 2. The candidate has corresponding logic at `controls/ref-preflight-v3.py:297–317`. No production zero-gate defect was observed. The candidate is not production, and this narrow observation proves neither its G02 conformance nor full C1.

## Commands, evidence, and bounds

Executed from the seat output directory:

```text
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Attack04/probe.py
exit 0
```

`Attack04/evidence.json` records exact commands, stdout, stderr, exits, direct judge inputs/results, fixture names and cleanup. `Attack04/probe.py` is the reproducer. Tests used installed `/usr/bin/python3` 3.14.8; no tool installation/update, network access, clone, git/jj mutation, production/frozen edit, service operation or package transaction. Scratch `/fast/scratch/hyaku/chousa-r64/Attack04` was removed in `finally`; evidence records `scratch_removed: true`.

LSP unavailable: `read xd://lsp` returned `No such tool`; mounted inventory contains no LSP device. Source-location searches/read fallback are textual evidence, not semantic-reference proof. No diagnostics or reference results are claimed.

## Residual risk / verification gaps

Only zero-gate execution, actual judge calls, frozen-byte identity, and E12/E13 fixture construction were exercised. No full battery, G08, null control, three-seed landing run, full diff review or resume-continuity execution was performed; resume/rerouting/saturation are outside this scoped item. Findings do not certify broader C1, production integration, or closure. No frozen repair was made.

Self-check: accuracy 4/5 (direct evidence, but no full battery); completeness 4/5 (all scoped zero paths plus fixture distinction; broader closure intentionally untested); clarity 4/5 (explicit severity and claim/oracle separation; report includes lengthy reproducibility detail); actionability 4/5 (exact falsifier and locations; only L1 may choose successor instrument); conciseness 4/5 (raw output is external, though fixture context repeats the known issue). Overall 4.0/5. Highest-impact next verification belongs to L1: preserve the frozen FAIL separately from any distinct supplement result. User agreement expected because no supplemental pass is laundered into frozen admission.
