# OracleC2B — C2 feasibility only

## Result and axes

**MEETS-TARGET (feasibility oracle, not a candidate or admission judgment).** Final oracle: `EXEMPT_AUDIT_MATCH=120/120` on fresh seeds **320219891** and **320219947**, counter exits **0**, gate exits **1**, no timeout, no misses. Coverage is the C2 exempt-hop surface; operability includes reproducible invocation and preservation of the two named archival fixtures with their documented root.

**Counterexample to the requested regression invocation:** literal `--root <lane>` produces **0/22 DRIFT** and **0/2 DRIFT**, both exit 1 with `CHAIN_SOURCE_MISSING`. The archives are fleet-root-relative, not lane-root-relative. Using the documented fleet root produces **17/22 CLEAN**, exit 0, and **1/2 DRIFT**, exit 1: no change from the supplied base outcomes. This is a fixable invocation defect, not an axis trade to admit.

## Provenance and implementation

Read `corpus/evidence/round32/claims.md` first, then both counter docstrings, relevant gate functions, fixture records and fixture documentation. No counter was edited; no candidate was scored.

Observed SHA-256 values:

| File / version | SHA-256 |
|---|---|
| Base `tools/research-gate.sh` copied into scratch | `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258` |
| Frozen C2 counter | `b6626b2cb81b2aeaf66a8ff11a06c030612bf4e264dc128f290021c4aa71f54c` |
| Intermediate oracle | `d08f0503387347c67c7c133396d13c3d93f7a1329eab2c3467efc16b1f1721bb` |
| **Final oracle** | **`1e3d02fef62e3d434a931313a26e7cb5015b672521769bd0fc2e2fe54e1bda26`** |

Hash commands exited 0. In addition to `timeout 15 sha256sum` on the listed files, the committed C2 bytes were checked with:

```sh
timeout 15 git show 4111607c857bc29ff31883bc095ae00afb527e50:corpus/evidence/round32/c2-count.py | timeout 15 sha256sum
```

Its output was the frozen C2 hash above. The supplied base gate hash matched before editing the scratch copy.

Scratch final gate: `/fast/scratch/hyaku/chousa-r32/w1/OracleC2B/gate/tools/oracle-final-gate.sh`.
Durable byte copy: `.ufo/waves/round-32/w1/OracleC2B/oracle-final-gate.sh`.
Intermediate byte copy: `.ufo/waves/round-32/w1/OracleC2B/oracle-gate.sh`.

Only the original exempt arm was changed (base gate lines 1880–1883; final oracle lines 1880–1912). U statuses call existing `chain_citation`, apply the resolved arm's declared-ID/pointer selection, call existing `chain_ref_file` and `claim_source_path`, read with the same `cat`/sentinel idiom, then call existing `chain_anchor_at`. Successful U citations emit one `CHAIN_EXEMPT_RESOLVABLE`, `observed=resolvable`, `verdict=mismatch`; other U citations remain exempt without findings. `rejected` and `not-applicable` retain the unread original arm. The resolved arm was not changed. Boundary/cap/alias/device checks are inherited from base lines 1167–1271; URL refusal occurs before source reading at lines 1181–1184.

One cheap refinement removed an unnecessary `N_MISM` increment from the intermediate oracle: the existing summary labels that accumulator `anchor-missing` (base lines 1905–1907), although the new finding means the anchor exists. `emit_finding` already records drift. Both versions passed both of their seeds; all receipts and intermediate bytes are retained rather than presenting the final hash as the earlier measured hash.

Gate placement intentionally separates `LANE_ROOT=.../OracleC2B/gate` from fixture temporary directories under `.../OracleC2B/tmp`. [INFERENCE] A flat scratch gate with temporary fixtures beneath its permitted `LANE_ROOT` would admit E7's `../outside` through the second allowed root (base lines 290–291, 1213–1222), contaminating this test. Every observed oracle run had E7 **6/6**.

## Counter commands and receipts

All counter commands ran from the lane checkout. For compactness, each command is the following exact prefix concatenated with one listed suffix; prefix labels are notation, not separately executed programs:

```text
COUNTER_PREFIX = timeout --kill-after=5s 700s prlimit --as=1073741824 --nproc=2000 --fsize=1048576 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/OracleC2B/tmp C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/OracleC2B/tmp TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/OracleC2B/tmp
```

Exact suffixes:

```sh
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/OracleC2B/gate/tools/oracle-gate.sh --seed 320219733 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/OracleC2B/oracle-s320219733.json
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/OracleC2B/gate/tools/oracle-gate.sh --seed 320219839 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/OracleC2B/oracle-s320219839.json
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/OracleC2B/gate/tools/oracle-final-gate.sh --seed 320219891 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/OracleC2B/oracle-final-s320219891.json
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/OracleC2B/gate/tools/oracle-final-gate.sh --seed 320219947 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/OracleC2B/oracle-final-s320219947.json
```

The intermediate scratch file was subsequently refined and renamed; its original bytes remain in the durable intermediate copy above.

| Oracle | Seed | Counter exit | Gate exit | Count | Measured label |
|---|---:|---:|---:|---|---|
| Intermediate | 320219733 | 0 | 1 | 120/120 | MEETS-TARGET |
| Intermediate | 320219839 | 0 | 1 | 120/120 | MEETS-TARGET |
| Final | 320219891 | 0 | 1 | 120/120 | MEETS-TARGET |
| Final | 320219947 | 0 | 1 | 120/120 | MEETS-TARGET |

All four commands printed these per-class lines, preserved separately in the corresponding `OracleC2B/*.stdout` artifacts:

```text
EXEMPT_AUDIT_MATCH=120/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 12/12
  E2_U_missing_file 6/6
  E3_U_external_url 6/6
  E4_U_no_citation 6/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 6/6
  E7_U_out_of_corpus 6/6
  E8_U_quote_glued 6/6
  E9_U_heading_as_plain_line 6/6
  E10_U_line_partial 6/6
```

Each receipt records `predicate_holds=true`, `gate_timed_out=false`, `misses=[]`, the seed and exact hashes (final receipts lines 3–14, 15–31). C2 has one generated 120-hop record per run, not C1-style numbered trials; its counter emits per-class rather than per-hop success lines.

**Why the counter lets this oracle through:** the implementation supplies the intended 36 resolvable U hops with the required finding identity, leaves 12 resolved hops verified, and leaves 72 other hops exempt. It uses the gate's actual parser, source safeguards and anchor matcher rather than an existence/substring shortcut. This establishes feasibility under the frozen fixture, not candidate correctness or adversarial counter soundness. The counter generates its own independent root (counter lines 148–232, 249–264); its pass cannot establish that an archival regression command used the correct root.

## Archival regression commands and counterexample

Final fixture commands used this exact common prefix followed by one listed suffix:

```text
FIXTURE_PREFIX = timeout --kill-after=5s 120s prlimit --as=1073741824 --nproc=2000 --fsize=1048576 -- env -u CHOUSA_ROOT -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_STRICT -u CHOUSA_AGGREGATOR_ERE -u CHOUSA_NOW_EPOCH C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/OracleC2B/tmp C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/OracleC2B/tmp TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/OracleC2B/tmp
```

```sh
bash /fast/scratch/hyaku/chousa-r32/w1/OracleC2B/gate/tools/oracle-final-gate.sh verify-chain corpus/fixtures/chain-r3.md --root /home/vgpnk/Projects/shokunin/chousa-shokunin
bash /fast/scratch/hyaku/chousa-r32/w1/OracleC2B/gate/tools/oracle-final-gate.sh verify-chain corpus/fixtures/chain-r3-broken.md --root /home/vgpnk/Projects/shokunin/chousa-shokunin
bash /fast/scratch/hyaku/chousa-r32/w1/OracleC2B/gate/tools/oracle-final-gate.sh verify-chain corpus/fixtures/chain-r3.md --root /home/vgpnk/Projects/shokunin
bash /fast/scratch/hyaku/chousa-r32/w1/OracleC2B/gate/tools/oracle-final-gate.sh verify-chain corpus/fixtures/chain-r3-broken.md --root /home/vgpnk/Projects/shokunin
```

Final outputs at 06:53:24Z:

| Root | Fixture | Exit | Observed output |
|---|---|---:|---|
| Lane, as requested | chain-r3.md | 1 | `RESOLVED_HOPS=0/22`; DRIFT, refused=17, findings=17 |
| Lane, as requested | chain-r3-broken.md | 1 | `RESOLVED_HOPS=0/2`; DRIFT, refused=2, findings=2 |
| Documented fleet root | chain-r3.md | 0 | `RESOLVED_HOPS=17/22`; CLEAN, verified=17, exempt=5, findings=0 |
| Documented fleet root | chain-r3-broken.md | 1 | `RESOLVED_HOPS=1/2`; DRIFT, anchor-missing=1, findings=1 |

Final stdout excerpts are retained in `OracleC2B/fixture-final-results.txt`. The clean fixture keeps hops 18–22 exempt; the broken fixture keeps exactly the existing `CHAIN_ANCHOR_NOT_FOUND` finding on hop 2, nearest_line=53. Both documented-root outcomes match the supplied base outcomes; the base gate was not re-run to confirm them.

The intermediate oracle was also run with the same four suffixes using basename `oracle-gate.sh`: literal-root runs used the fixture prefix without its six `-u CHOUSA_*` removals; documented-root runs used the full fixture prefix. They produced the same respective counts/verdicts (literal at 06:49:14Z; documented at 06:50:38Z), preserved in `OracleC2B/fixture-results.txt`.

Evidence for the root correction: `corpus/fixtures/chain-r3.README.md:33–51` locates the three archives at the fleet root and explicitly says pointer cells are fleet-root-relative. `corpus/knowledge/citation-chain-fidelity-r24.md:89–97` supplies the explicit fleet-root erratum. A bounded glob of `/home/vgpnk/Projects/shokunin/research/deep-research-2026-09-28/*.md` located all three named targets. An earlier broad recursive glob timed out and was not treated as evidence of absence.

**Smallest safe correction:** run archival checks with `--root /home/vgpnk/Projects/shokunin`. Do not move/copy archival inputs into the lane, alter fixture citations, broaden production boundaries, or modify the frozen counter to hide the invocation defect. Keep the counter's temp fixtures disjoint from the scratch gate's inferred lane root.

## Scope and limits

No production files, corpus files, index, jj state, routing, sibling lanes or fleet files were mutated. No network, installs, subagents, background jobs or canonical runtime invocation. Only this report, its own artifact directory and its isolated scratch directory were written. `timeout 10 df -h /fast` exited 0 and reported 236G available before fixture work. Every executed test was timeout-bounded with memory/process/file-size caps; all returned synchronously. `timeout 15 stat -c '%s %n'` on the twelve retained artifacts exited 0: maximum 308027 bytes, each below 1 MiB.

Not exercised: gate selftest, C1 counter, round-31 counters, claims fixtures or the full round no-harm suite. These are not claimed as passing. Candidate scoring remains outside this seat and follows the L1 control-receipt commit rule. No admission, integration or shipment judgment is made here.
