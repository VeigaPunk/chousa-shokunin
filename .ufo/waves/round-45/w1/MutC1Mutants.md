# C1 mutation probe — MutC1Mutants

Item: four launcher mutants, each intended to break one frozen C1 case. Detector: `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round45/c1-count.py --tool <mutant>`. Frozen predicate: `corpus/evidence/round45/claims.md:23-39`; counter behavior: `corpus/evidence/round45/c1-count.py:93-119`.

## Commands and output

- `cat /home/vgpnk/.omp/agent/RULES.md` → printed tooling authorization rules; no install/update was needed.
- `cp /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/parent-lifetime.sh /tmp/chousa-r45-MutC1Mutants/committed-round44-tool.sh` → copied source into scratch.
- `sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/parent-lifetime.sh` → `f3b0baac457710d6a210ad4e1f27e8d398f6b51c58290d8c90fea8bdca3e33cb`.
- Mutants were written under `/tmp/chousa-r45-MutC1Mutants/`: `mutant-1-zero-exit.sh` adds zero-task exit 0; `mutant-2-no-timeout-field.sh` removes `epoch=%s` from the start line; `mutant-3-default-timeout.sh` changes default 420 to 5; `mutant-4-timeout-exit.sh` changes child status 124 to 0 before receipt logging.
- Counter command was run once per mutant. Each produced exactly:

```text
CASE a_empty_exits_3=FAIL
CASE b_ok_exits_0=ok
CASE c_timeout_exits_3=FAIL
CASE d_no_timeout_exits_2=FAIL
CASE e_start_timeout_s=FAIL
CASES_MATCH=1/5
C1=FAIL
```

Each command exited 1. The identical outputs occur because all four begin from the committed round-44 launcher, which already exhibits these mismatches; the intended one-case behavior cannot be isolated by simply mutating that baseline.

## Verdict

Inconclusive for the four requested falsifiers. The detector does not pass on the pristine launcher, so per contract a baseline failure is not a killed mutant. No mutant survived at 5/5, but none can be credited as a kill. In particular, the start-line mutant intended to affect only case (e) removes the epoch field, not `timeout_s` (already absent in baseline). The default-timeout variant changes 420 to 5, but case (d) only checks omission returns exit 2; it does not measure the default duration. The zero-task and timed-out-seat variants modify their respective behavior, but baseline already fails the other cases and the counter reports only aggregate case booleans.

Hashes: committed scratch copy and production source both `f3b0baac457710d6a210ad4e1f27e8d398f6b51c58290d8c90fea8bdca3e33cb`; mutant hashes: 1 `6974ba4be2ccb28ca896ce7ff49f5a38f20ae6377e03524d50575d4af40216cc`, 2 `717ce0ea2421ffab8f93991d5eb6aaacc6905827eb7e751c355af50ebb83dd64`, 3 `73a0f9dd5d37c6e28dd9874220fb31b25e7a792fab6a9e85c141a7a939fc35bc`, 4 `19f37aa5dffcc2986e87459e55061ba90d7a8a4a7798ced17a19186c53b47278`.

No production, index, or jj state was modified. No tools installed. Scratch cleanup remains required before completion.
