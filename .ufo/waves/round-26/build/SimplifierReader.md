# Round 26 — SimplifierReader (WRITER)
Axes: operability (primary), byte-identical metadata output, refusal/snapshot integrity, maintenance weight.
Observed base: `git -C /tmp/chousa-r26-SimplifierReader rev-parse HEAD` → f361d12e44687841e30ec35710ddb366c6f795e0.
Scope: private proposal only; no live implementation edits; no later round work.

## Smallest proposal
Patch: `/tmp/chousa-r26-SimplifierReader/r26-SimplifierReader.patch` (3 hunks; net −5 lines).
File: `/tmp/chousa-r26-SimplifierReader/tools/research-gate.sh:2310,2383-2429`.
Delete the per-line `lines` array; feed the existing parser directly from the existing bounded `content` snapshot.
Keep the here-string, `IFS= read -r`, nonempty-final-line guard, and single-terminal-CR stripping.
The parser still runs in the current shell, not a pipeline subshell; findings and metadata state survive.

Removed-line responsibilities (base line numbers in tools/research-gate.sh):
- 2310 `lines=()` declared private array storage: remove only this declarator; retain the other arrays.
- 2383 `lines=()` discarded the prior entry's array: unnecessary without array storage.
- 2384 `while ...` iterated the snapshot, preserving whitespace/backslashes: moved to parser entry at new 2386.
- 2385 CR stripping normalized each parsed line: moved to new 2387, before every existing parser branch.
- 2386 `lines+=(...)` retained every normalized line including body: deleted without replacement.
- 2387 `done <<<...` supplied the same fd-bound snapshot plus the here-string newline: moved to new 2429.
- 2388 blank separator: deleted with the obsolete pass; no runtime behavior.
- 2392 array iteration provided ordered lines: replaced with direct ordered reads, now stoppable at the same heading.
- 2434 loop closer: retains its role, now bearing the snapshot redirection.

## Preserved contract and stopping point
Base 2342-2382 (denylist/stat/multilink/size/NUL/read refusals and fd-bound snapshot) is untouched.
Base 2393-2433 parser decisions and base 2436-2496 verdict/output code are untouched.
[INFERENCE] Each line reaching the old parser reaches the new parser identically; early heading termination now avoids reading body lines into Bash objects.
No-heading inputs still scan their header; existing verified/recheck continuation strings may grow with that header, but the per-line whole-snapshot array is gone.
Fence branches at base 2394-2413 are deliberately retained: closer requires same character, sufficient length, and whitespace-only tail; opener permits info text.
Their repeated append cases also preserve ordering relative to blank reset, fence recognition, heading cutoff, and key reset.
Deleting fence state would change semantics; deduplicating append cases needs another control-flow change and is not required for C1.
Stop here: the next deletion either risks output semantics or exceeds the smallest C1 cutover.

## Evidence and limits
`read xd://lsp` → “No such tool”; no LSP device/server is available here, so no semantic-reference proof is claimed.
Literal fallback: `grep` on base verify_metadata 2303-2497 found `lines` only at 2310,2383,2386,2392; all four uses are replaced/deleted together.
One selftest, in clone, after no active selftest was reported by `pgrep`; execution serialized with `/tmp/chousa-r26-selftest.lock`.
Command: `flock /tmp/chousa-r26-selftest.lock bash /tmp/chousa-r26-SimplifierReader/tools/research-gate.sh --selftest`.
Observed: exit 0; `RESEARCH_GATE_SELFTEST: PASS (161 cases, 0 skipped)`.
Observed case-line SHA256: 5eac4a7e2af964f6e81631f66990426e5c8ef58fb41ba6ec6d0054ef819e01cb (matches registered legacy digest).
No 8 MiB input, C1 amplification probe, frozen-population output comparison, build, lint, or formatter was run.
Thus full-population byte identity and C1_AMPLIFIED=0/4 remain integration-owner measurements, not observed claims here.
Shared-tree check: SHA256 snapshots before/after work over all 460 tracked live files found zero changed bytes; own report is outside that tracked snapshot.

## Every written clone artifact (SHA256)
`tools/research-gate.sh`: c3fbffb6f685efdf2cd4e84ecd3900405150a0b5c540a8bd37c406443ff9fbc8
`r26-SimplifierReader.patch`: f1bc6472d8ed430134fdb6b5289a1c9bc02589a841b353a105d2741ecf1cb49f
`r26-SimplifierReader-selftest.log`: 4b4ff707f6c3ece36836d0e34ae28e6a572287b65b89ce20e5851f62bdf38534
Patch generated from `git -C /tmp/chousa-r26-SimplifierReader diff f361d12e44687841e30ec35710ddb366c6f795e0 -- tools/research-gate.sh`.
Installs: none.
VERDICT: Minimal array-deletion proposal preserves all 161 existing cases; bounded-reader population/RSS acceptance remains unmeasured here.
