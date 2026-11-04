# R74ExecC — bounded public-CLI fixture

Author-lane evidence only; no admission or promotion decision.

## Result

`BOUNDED_PROBE=7/7`, driver exit 0. Successor SHA256: `9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41`.

Used actual committed bytes of all three protected files and both historical receipts from `5aec90775fc7cc1fe9ad442e0d5491731323eec1`, not the matrix's miniature FILES. Created one isolated Git repository; asserted its exact toplevel before each staging/commit sequence. Invoked only the successor public CLI, never imported or invoked pure `check()`.

- Unchanged control: exit 0, `C2=PASS checks=7/7`.
- Delete LOG title + append lesson: exit 1, only C2-6 FAIL; numstat LOG `0/1`, lesson `2/0`.
- Delete lesson title + append SCORECARD: exit 1, only C2-6 FAIL; lesson `0/1`, SCORECARD `2/0`.
- Delete SCORECARD title + append LOG: exit 1, only C2-6 FAIL; SCORECARD `0/1`, LOG `2/0`.
- Equal-line title replacement separately in LOG, lesson, SCORECARD: each exit 1, only C2-6 FAIL; each numstat `1/1`.

Every negative case printed `C2=FAIL checks=6/7`; C2-1 through C2-5 and C2-7 passed. Both receipts remained byte-identical to fixture base in every case. Cross-file additions did not mask deletions. Each case compared against the same fixture base `ee51b32ce05d1bd6136dfa2dc1883d6365ad675f`.

## Exact retained evidence

All paths below are absolute:

- Driver: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74ExecC/probe.py`
- Complete command/output, input hashes, case revisions, cleanup receipt: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74ExecC/probe-output.txt`
- Machine-readable per-case commands/results: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74ExecC/results.json`
- Original five fixture inputs: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74ExecC/inputs/` preserving original relative paths.
- Per-case raw stdout/stderr/numstat: same output folder, stems `unchanged`, `mixed-0` through `mixed-2`, `equal-0` through `equal-2`, suffixes `.stdout.txt`, `.stderr.txt`, `.numstat.txt`.

## Bounds and risks

No production/frozen artifact changes, installs, network, clones, fleet Git mutations, full battery, or preflight. Scratch `/fast/scratch/hyaku/chousa-r74/R74ExecC/` was removed in the driver's `finally`; transcript records `SCRATCH_REMOVED=True`. Only advisory report, driver, retained inputs and receipts were written. No blockers. Symbol lookup/refactoring was not required; no LSP tool is exposed to this seat.

This bounded probe does not establish the canonical nine-case predicate, historical landing base-to-revision conjunct, or semantic sufficiency beyond these cases; integration remains with L1.

Self-evaluation: accuracy 4/5 (observed seven CLI outcomes; not canonical predicate), completeness 5/5 (all assigned files/operations covered), clarity 4/5 (raw detail separated into receipts), actionability 5/5 (source, inputs, commands and hashes retained), conciseness 4/5 (receipt inventory adds length); overall 4.4/5. Improvement: use the machine-readable results directly during integration rather than treating this report as canonical scoring. The user should agree with the bounded evidence, not infer broader authority.
