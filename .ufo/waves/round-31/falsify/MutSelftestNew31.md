# MutSelftestNew31 — coverage / operability

**Verdict: selftest sensitivity broken for 2/6 assigned mutants; 4 killed, 2 survived, 0 inconclusive.** Only the full selftest was the behavioral detector. The frozen counters were neither run nor edited; this does not falsify P1/P2 on the landed gate.

Scratch clone: `/fast/scratch/hyaku/chousa-r31/w2/MutSelftestNew31/clone`, checked out at `ee1024fd492144c9c7b315890fac247543c37208`. Six independent ordinary gate copies remained under its `tools/` directory, preserving the clone's lane-root resolution. Artifacts: [MutSelftestNew31/](MutSelftestNew31/).

## Mutant × NEW cases

P = case passed; F = case failed. Exit columns are pristine / mutated / restored. Every run completed all 228 cases, with zero skips; no old case failed.

| Mutant |216|217|218|219|220|221|222|223|224|225|226|227|228|Exits|Verdict|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| first-occurrence |F|P|P|P|P|P|P|P|P|P|P|P|P|0/1/0|killed|
| start-only |P|F|P|P|P|P|P|P|P|P|P|P|P|0/1/0|killed|
| grammar-07 |P|P|F|P|P|P|P|P|P|P|P|P|P|0/1/0|killed|
| hash-case-insensitive |P|P|P|P|P|P|P|P|P|F|P|P|P|0/1/0|killed|
| fail-open-unreadable |P|P|P|P|P|P|P|P|P|P|P|P|P|0/0/0|survived — gap|
| span-before-stale |P|P|P|P|P|P|P|P|P|P|P|P|P|0/0/0|survived — gap|

Mutation points (original gate line numbers), expected detector, and actual output:
- **First occurrence**, 1377: return immediately after emitting the first delimited occurrence. Expected 216 (`c1-pass-bound`); observed that sole failure, `RESEARCH_GATE_SELFTEST: FAIL (1/228 cases)`.
- **Start only**, 1532: compare the start line but omit end-line equality. Expected 217 (`c1-fail-mislocated`); observed that sole failure, same FAIL summary.
- **Grammar accepts `07`**, 1470: positive single-line grammar becomes `^0*[1-9][0-9]*$`. Expected 218 (`c1-fail-invalid-line`); observed that sole failure, same FAIL summary.
- **Hash case-insensitive**, after 1448: lowercase the parsed pin before validation/comparison. Expected 225 (`claims-sha-invalid`); observed that sole failure, same FAIL summary.
- **Fail-open unreadable**, 1506: an unmeasurable digest falls back to the supplied pin rather than `unreadable`. Expected full-selftest rejection of this fail-open behavior; observed `RESEARCH_GATE_SELFTEST: PASS (228 cases, 0 skipped)`. The new fixtures contain no hash-read-failure injection.
- **Span before stale**, 1503: load the source exactly and gate hashing on a successful boundary-delimited span match. Expected 224 (`claims-sha-stale`) to reject absence overriding staleness; observed the same PASS summary. [INFERENCE] T2 can become unsupported while remaining mismatched; T1/T3 still satisfy the aggregate `observed=stale` check. The case does not assert each stale claim's verdict/finding.

## Reproduction and restoration

Let A be this report's sibling `MutSelftestNew31/` artifact directory and S be `/fast/scratch/hyaku/chousa-r31/w2/MutSelftestNew31`. For each of the six row names and each phase (`pristine`, `mutated`, `restored`), the foreground command was `timeout -k 10 1200 python3 A/run-selftest.py PHASE MUTANT S/clone/tools/probe-MUTANT.sh`; the recorder invokes `bash <gate> --selftest`, clears inherited `CHOUSA_*`, sets `LC_ALL=C.UTF-8`, places temporary fixtures under S, caps address space at 2 GiB and user processes at 8192, and kills its child process group on completion/interruption. Exact expanded commands, exit codes, all case results and full output are in the 18 phase/mutant JSON/log pairs. There were no timeouts. The six baseline and six restored runs each printed `RESEARCH_GATE_SELFTEST: PASS (228 cases, 0 skipped)`.

All six copies were restored with ordinary `cp` from `pristine-gate.sh`. Every pristine and restored detector recorded identical before/after SHA-256: `c23d7537e03482f2844c9cbc43fc055d3d08d564857a89529b6f13473403823c`. The distinct mutated hashes and full matrix are in [matrix.csv](MutSelftestNew31/matrix.csv); exact mutant snapshots are `mutant-<row-name>.sh`. Thus each mutation has a passing byte-identical baseline and restoration, not a baseline-failure kill.

Limits: synthetic full-selftest sensitivity only; no counters, network, production edits, fixes, integration or shipping. Initial clone setup exited 254 because a 192-process cap was below the already-running user workload; the bounded retry at 8192 succeeded, before any detector ran. No tools installed or updated. PTY requests on the pristine batch fell back to non-terminal execution; this was reported to the tool issue device. No subagents or background jobs were launched.
