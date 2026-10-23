source: S070 (GNU coreutils `sha256sum(1)`, routed in the round-36 source task; source row was not located in the lane text search when drafted); `.ufo/waves/round-36/measure/c1-after-s36001.json`; `.ufo/waves/round-36/measure/c1-after-s36011.json`; `.ufo/waves/round-36/measure/c1-before-s36001.json`; `corpus/evidence/round36/claims.md` §C1.
verified-at: 2026-10-23 (committed construction receipts only; not an independent fresh-seed remeasurement)
recheck: on-release (`python3 corpus/evidence/round36/c1-count.py --seed N --receipt F`; use two fresh seeds and pin the gate SHA in each receipt)

# Round 36 C1 — engine-swap canary

## Mechanism and scenarios

The gate pins its grep engine; the C1 counter challenges that path through fourteen named scenarios, comparing output where relevant and checking the receipt fields below. The detailed fields listed here are from the committed seed-36001 receipt; the seed-36011 receipt independently records the aggregate `14/14` result and `predicate_holds=true` against the same gate SHA.

| Scenario | What it proves in this fixture | Receipt field (`c1-after-s36001.json`) |
|---|---|---|
| S1 `shim-first-path` | A PATH-first grep shim does not replace the selected matcher while the reference output is preserved. | `detail.tripwire_bytes=0`; `detail.output_matches_reference=true` |
| S2 `bash-env-function` | An imported `BASH_ENV` grep function does not replace the selected matcher while output is preserved. | `detail.tripwire_bytes=0`; `detail.output_matches_reference=true` |
| S3 `no-grep-on-path` | The gate still handles a PATH containing its other tools but no grep. | `detail.path_tools=38`; `detail.rc=1`; `detail.stderr_tail=""` |
| S4 `override-relative` | A relative `RESEARCH_GATE_GREP` override is refused. | `detail.rc=2`; `detail.marker=true` |
| S5 `override-missing` | A missing override is refused. | `detail.rc=2`; `detail.marker=true` |
| S6 `override-non-gnu` | A non-GNU override is refused after its `--version` probe only. | `detail.rc=2`; `detail.stub_calls=["stub --version"]`; `detail.version_only=true` |
| S7 `override-distinct-path` | A distinct-path override is honored and observed receiving matcher invocations; output remains reference-equivalent. | `detail.matcher_calls=4`; `detail.echo_line`; `detail.output_matches_reference=true` |
| S8 `default-echo` | The default pin is named with its reported version and preserves output. | `detail.echo_fullmatch=true`; `detail.echo_line`; `detail.output_matches_reference=true` |
| S9 `override-beats-shim` | An explicit override wins over an imported shim. | `detail.echo_line` names the override; `detail.tripwire_bytes=0` |
| S10 `semantic-canary` | The exact-search control is output-equivalent but misses the long record's matcher query; the landed matcher is attributed both the long and short records. | `detail.k1_output_equivalent=true`; `detail.k1_long_missing=true`; `detail.landed_attributed` |
| S11 `manifest-hash-shim` | The manifest check retains the actual gate and record digests under a hostile `sha256sum`. | `detail.manifest_ok=true`; `detail.true_gate_sha`; `detail.true_record_sha` |
| S12 `locale-c` | The C-locale decode agrees with the UTF-8 observation for the supported match. | `detail.c_obs`; `detail.c_rc`; `detail.utf8_obs`; `detail.utf8_rc` |
| S13 `pin-echo-isolation` | Pin echo is absent from baseline output and does not create drift. | `detail.baseline_echo=false`; `detail.drift_out="GATE_DRIFT: none"`; `detail.drift_rc=0` |
| S14 `pin-drift-token` | An injected pin line is identified as `-GATE_GREP`, not as a generic `-LINE` drift. | `detail.drift_out="GATE_DRIFT: -GATE_GREP"`; `detail.drift_rc=1`; `detail.pin_rc=0` |

### Aggregate evidence and commands

- Landed gate `tools/research-gate.sh`, SHA-256 `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`: `ENGINE_SWAP_CANARY=14/14`, `predicate_holds=true` on seed 36001 in `.ufo/waves/round-36/measure/c1-after-s36001.json`. Counting command, per frozen P1 (the counter's default gate is `tools/research-gate.sh`): `python3 corpus/evidence/round36/c1-count.py --seed 36001 --receipt <F>`.
- The same landed-gate SHA scores `ENGINE_SWAP_CANARY=14/14`, `predicate_holds=true` on seed 36011 in `.ufo/waves/round-36/measure/c1-after-s36011.json`. Counting command: `python3 corpus/evidence/round36/c1-count.py --seed 36011 --receipt <F>`.
- The committed base control `.ufo/waves/round-36/controls/base-gate-r36.sh`, SHA-256 `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`, scores `ENGINE_SWAP_CANARY=10/14`, `predicate_holds=false` in `.ufo/waves/round-36/measure/c1-before-s36001.json`. Counting command with the counter's explicit `--gate` option: `python3 corpus/evidence/round36/c1-count.py --gate .ufo/waves/round-36/controls/base-gate-r36.sh --seed 36001 --receipt <F>`.

The command forms above describe the frozen counter invocation; they were not run by the author of this draft. The receipts are the evidence for the reported counts and gate identities.

## Before state and do-nothing control

The base gate scores 10/14; its four misses are S11–S14: hostile `sha256sum` poisons both manifest fields while the run exits zero; C-locale `\u00e9` decodes as `unsupported`; pin echo leaks into baseline and drift is reported as `-LINE`; and an injected `GATE_GREP:` line is paired as `-LINE`. The cheapest do-nothing control is the base gate itself: it reaches neither 14/14 nor the four fixes.

## Stated limits (frozen claims, verbatim excerpts)

- “C1's semantic canary proves the pinned engine was queried for each record, not that its answer was used” (`corpus/evidence/round36/claims.md:121-122`, accessed 2026-10-23).
- “an output-equivalent call-for-show engine survives — stated, not argued away.” (`corpus/evidence/round36/claims.md:124-125`, accessed 2026-10-23).
- “A gate that READS the recorder script can learn the log path and marker and forge records (active anti-instrumentation is out of scope).” (`corpus/evidence/round36/claims.md:126-127`, accessed 2026-10-23).
- “C2's witness shares the same call-for-show limit; it kills engines that skip the call, not engines that make the call and ignore it.” (`corpus/evidence/round36/claims.md:131-132`, accessed 2026-10-23).

## Reading rule

The counter proves what its scenarios assert, one at a time; it never proves “the engine is genuine.” The semantic query can be attributed while its answer is discarded, and output equality is not proof of provenance or general correctness.

**What this entry does not claim:** that the engine is genuine, or that a queried engine's result was used.