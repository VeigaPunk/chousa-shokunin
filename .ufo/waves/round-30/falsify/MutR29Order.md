VERDICT: pass — C 1 KILLED the landed tool's round-29 MutOrder mutant: 104/106 in both runs.
Axes: coverage, operability. Exactly one branch move: fetch/UNREACHABLE before TOO_LONG, with NO_SOURCE still first; [diff](MutR29Order/mutant.patch).
Expected detector: 106/106. [Baseline](MutR29Order/baseline-wide.json) 106/106, exit 0; [run 1](MutR29Order/run1.json) and [run 2](MutR29Order/run2.json) 104/106, exit 1 each; [restored](MutR29Order/restored.json) 106/106, exit 0.
Both mutant receipts miss only `order/too-long-unreachable`: 0/2 matched, expected TOO_LONG but got UNREACHABLE twice; every other class/kind matched.
SHA-256 before/restored/lane: `47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201`; mutant: `6855d84b6c062a28de4c0fe8ecc851990b6528cea2d0d8e7e39cc115d8a0a5df`. Both `cmp` comparisons passed, exit 0, `EXACT_BYTES_RESTORED=True`.
Counter and harness hashes matched the supplied values before scoring and after restoration; exact bounded commands, outputs, exits and full hashes: [commands](MutR29Order/commands.txt).
An initial 1 GiB baseline scored 0/106, exit 1, and is inconclusive; the scored baseline, mutants and restoration all used 8 GiB and a process cap of 16384. An earlier preparation at process cap 128 failed with exit 254; both events are recorded.
C 2 not run. No production edits, external fetches, background jobs, subagents or installations; all foreground detector processes exited.
