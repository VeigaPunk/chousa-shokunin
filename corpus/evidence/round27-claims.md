# Round 27 — repair the falsified contracts, not their tests

Base: 64eec5d41c7cf7f17f5ce1e968e28b3769952596 (master). Attempt1 only. The reported round26 FAIL3/187 and counterexamples are accepted as ground truth, not rerun for confirmation.

## C1 — operability (lowest measured axis)

Repair the three failing usage selftests without deleting their cases, accepting fewer required diagnostics, changing expected exit2, or allowing an actual verdict on a usage error. Count verdict records by anchored `^RESEARCH_GATE: `, not help-text substrings. Add independent harness controls: correct usage passes, exit1 fails, missing diagnostic fails, actual CLEAN/DRIFT verdict fails. Before FAIL3/187 (round26 FNoTrade:115–137); after full selftest PASS with all187 original case identities preserved and the new controls passing. Existing numeric score3 is frozen at r26; no numeric resource-safety inference.

## C2 — freshness

Repair date-input locale dependence and recursive leading-zero normalization. Date grammar is ASCII YYYY-MM-DD under any inherited locale. A long decimal cadence with leading zeros must compute its representable value without termination; out-of-range values remain unknown. Preserve year1–9999, strict as-of>due overdue semantics, calendar arithmetic, and plain mode. Independently persisted controls include Unicode-digit rejection, 128KiB leading-zero cadence, all-zero cadence, maximum representable span and overflow. Reported baseline failures: FDateAsOfUsage, FDateHugeCadence. After target: 0 contract mismatches in the new synthetic regression suite and original date differential, no weakened expectations.

## C3 — calibration

Repair registry-header state leaking across non-table lines and S-id consumed-text rescanning. Filesystem-path denylist checks must inspect complete filesystem paths, not citation-anchor prefixes; preserve existing citation-pointer semantics. Synthetic temporary fixtures only, no host files or live-process probes. Require fresh named headers after breaks, matching header/delimiter widths, standalone ASCII S-ids without invented or duplicate occurrences, and no reading a denylisted synthetic path when a colon occurs earlier. Existing well-formed registry behavior and exact used-by rules remain. Reported failures: FRegistryHeaderless, FRegistryIdBoundary, FRegistryRegistryDeny. After target: 0 mismatches in persisted independent controls; report inherited broader parser/resource/grammar limitations rather than claim whole-gate safety.

## Shared holds and frontier

Run the final full selftest once after integration; original187 identities must remain, legacy161 unchanged except the explicitly faulty usage-harness predicate lies outside those161. Run existing date/registry differential scripts and frozen metadata checks on isolated copies as applicable; record all exit codes. No external network or live-target fetch. Open local sources this round, cite a new own-work S-row in the lesson/knowledge evidence, record initial/final source census. Public-source conclusions from r26 stay withdrawn unless independently revalidated; fixing these regressions does not retroactively admit r26 or claim full criterion6 semantic verification.

## Counting command

`python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh` (independent synthetic expectations, nonzero on mismatch). Run unchanged on an isolated base archive and the final integrated tree; unsafe old long-token crash reproduction is not rerun: use the accepted committed r26 failure receipt for that baseline item and mark its baseline skip explicitly. The default final run exercises it. Full selftest: `bash tools/research-gate.sh --selftest`. Original failure receipt is committed under round26; no threshold changes can make it disappear.

## Measurement clarification before integration

Do not rerun the reported baseline failures to confirm them, including via a
new wrapper. The behavioral before evidence is the accepted committed r26
receipts. The same safe counting probe is instead run before/after over code:
`python3 corpus/evidence/round27-mechanisms.py GATE`. At base it prints
C1=1 faulty substring predicate; C2=2 locale/recursive-normalization sites;
C3=5 (stale state, rescan, three raw-registry-path calls). Desired after0
on each is only a source-mechanism count, not a semantic verdict. The
independent synthetic regression gate and complete selftest supply after
behavioral verdicts. This supersedes the earlier proposal to run the new
regression suite on the old gate; no baseline gate run was performed.
