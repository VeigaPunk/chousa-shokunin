# CtlC2NoReaderB — design-v2 re-score

Axes: **coverage**, **operability**. Read `claims.md:119-189` and the committed v2 counter contract. Re-scored all three unique controls previously built; flat/isolated copies are the same control bytes. No oracle was built by this seat. **All three MISSES on both fresh seeds; no control meets 132/132.**

Counter SHA-256: `8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a`, observed with `timeout 15s sha256sum` and matched independently to committed revision `3d586d3a` by `timeout 15s git show 3d586d3a:corpus/evidence/round32/c2-count-v2.py | timeout 15s sha256sum` (exit 0). All six receipts carry that hash.

## Controls and results

Gate prefix: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/gates/`. Each gate is at `<prefix>/<control>/tools/research-gate.sh`; its lane root excludes `C1_TMP`/`C2_TMP`. Existing mutated bytes were intact, so no rebuild was needed. `timeout 15s sha256sum` exited 0; every gate hash differs from pristine `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`.

| Control | Gate SHA-256 |
|---|---|
| a — regular-file existence, no anchor read | `308dab5001553e04f83fe850455e50527bd5da1547697a634b4806c5a66b9b08` |
| b — a + canonical inside-ROOT boundary, no anchor read | `0cdc8cb738b957f12c2a5b6409930e50b2b48fd48d4ca5ce397665c07356b533` |
| c — nonempty anchor cell + non-URL `to`, no anchor read | `afa7bfdeab02ef9815adc76649325d72d63c2c5f04b2264fde2d6d915a1448e9` |

Receipt prefix: `.ufo/waves/round-32/w1/CtlC2NoReaderB/v2/`.

| Control | Fresh seed | Printed count | RECORD_CHECKS | Counter/gate exit | Verdict | Receipt basename |
|---|---:|---|---|---|---|---|
| a | 355301654105070 | 78/132 | ok | 1 / 1 | MISSES | `a-s355301654105070.json` |
| a | 837026118534419 | 78/132 | ok | 1 / 1 | MISSES | `a-s837026118534419.json` |
| b | 697195336995729 | 84/132 | ok | 1 / 1 | MISSES | `b-s697195336995729.json` |
| b | 473245838044569 | 84/132 | ok | 1 / 1 | MISSES | `b-s473245838044569.json` |
| c | 301515719818218 | 60/132 | ok | 1 / 1 | MISSES | `c-s301515719818218.json` |
| c | 376766768938991 | 60/132 | ok | 1 / 1 | MISSES | `c-s376766768938991.json` |

All six receipts were opened: `record_fails=[]`, `gate_timed_out=false`, `predicate_holds=false`, and the gate/counter hashes match those above. Every command completed in 3.70–4.08 seconds of tool wall time, with no layout refusal or harness-launch failure.

## Invocation evidence

Working directory: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. The six independent scoring calls were dispatched together. This is a presentation template of their exact arguments; substitute control, seed and receipt basename from the corresponding table row (no other arguments vary):

```sh
timeout --kill-after=5s 45s prlimit --as=1073741824 --nproc=8192 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count-v2.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2NoReaderB/gates/<control>/tools/research-gate.sh --seed <seed> --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2NoReaderB/v2/<receipt-basename>
```

Seeds came from `timeout 10s shuf -i 100000000000000-999999999999999 -n 6` (exit 0), in table order. `timeout 15s mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2NoReaderB/v2` exited 0.

## Per-class/per-trial printed counts

| Class | a / 355301654105070 | a / 837026118534419 | b / 697195336995729 | b / 473245838044569 | c / 301515719818218 | c / 376766768938991 |
|---|---|---|---|---|---|---|
| R1_U_fragment_quote | 12/12 | 12/12 | 12/12 | 12/12 | 0/12 | 0/12 |
| R2_U_path_anchor_cols | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| R3_U_declared_id | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| F1_resolved_verifiable | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| E1_U_anchor_absent | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 |
| E2_U_missing_file | 6/6 | 6/6 | 6/6 | 6/6 | 0/6 | 0/6 |
| E3_U_external_url | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| E4_U_no_citation | 0/6 | 0/6 | 0/6 | 0/6 | 6/6 | 6/6 |
| E5_J_resolvable | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| E6_U_undeclared_id | 6/6 | 6/6 | 6/6 | 6/6 | 0/6 | 0/6 |
| E7_U_out_of_corpus | 0/6 | 0/6 | 6/6 | 6/6 | 0/6 | 0/6 |
| E8_U_quote_glued | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 |
| E9_U_heading_as_plain_line | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 |
| E10_U_line_partial | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 |
| E11_U_case_only | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 |
| E12_U_whitespace_only | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 |

## Counterexamples, correction, limits

Coverage defects persist despite successful record/operability checks. In `v2/a-s355301654105070.json`, hop `h1239ab6a` is E1 truth `exempt` but observed `resolvable`. In `v2/b-s697195336995729.json`, hop `hb21ffbaa` has the same false-positive absent-anchor result despite canonical boundary checking. In `v2/c-s301515719818218.json`, fragment-citation hop `hf69c3aa5` is truth `resolvable` but observed `exempt`. The new E11/E12 classes also reject all three shortcuts on every hop.

Smallest safe correction [INFERENCE; not implemented/scored]: use the resolved path's citation parsing, source policy and actual kind-specific anchor verification for U hops, finding only verification success and preserving exemptions otherwise. None of these no-reader results warrants a target change or establishes broader saturation. No candidate scored, counter edited, production file changed, tool installed, source fetched, or background job started. Only the assigned v2 control re-score was exercised.
