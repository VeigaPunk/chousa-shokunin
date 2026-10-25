# ExecNoHarmGate

UNCHANGED. The assigned selftest printed the committed pin and exited 0. Round 43 did not change `tools/research-gate.sh` or this gate's selftest result.

Axes named (not judged): operability is whether the selftest runs to its contract line; calibration is whether that line equals the committed pin; depth is whether the line is counted from case results and whether this round's bytes are the pre-round gate.

## Files changed

None in the lane except this report. No production file, git index, or jj state was written. No `--pin` was invoked. No network. No tool install. No subagent.

## Behavior

Command, cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`:

```
bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --selftest; echo "EXIT_CODE=$?"
```

The gate's own summary and the wrapper's record of its exit:

```
RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)
EXIT_CODE=0
```

`EXIT_CODE=0` is `$?` after the selftest, not a second command's status. Capture finished 2026-10-24 21:18:47 -0300 (log mtime). Tool-reported wall time 90.706s. One process; the foreground timeout only moved it to the background.

## Exact evidence

### Selftest stream

Combined stdout+stderr, counted from the capture (13724 bytes, 278 lines):

```
LINES=278
OK_CASE=275
FAIL=0
PASS_LINES=1
RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)
EXIT_CODE=0
FIRST ok-case  1  pass-control                 exit=0
LAST ok-case  275 bash-pin-override-fake       exit=2
OTHER=1
OTHER: metadata-asof-unicode-date-locale=en_US.utf8
```

Case numbers are contiguous:

```
n=275 first=1 last=275 gaps=[] gapcount=0
monotonic True
```

Tail of the same stream, verbatim:

```
ok-case  273 pin-bash-path-shim           exit=0
ok-case  274 bash-pin-override-missing    exit=2
ok-case  275 bash-pin-override-fake       exit=2
RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)
EXIT_CODE=0
```

No `FAIL-case` line. No `skip-case` line.

The one non-case line is the gate's own stdout, printed before case 193 when a Unicode locale exists (`tools/research-gate.sh:7310`). The skip branch at `:7316-7318` did not run. Case 193 still ran and was recorded `ok-case` with `exit=2`.

### Calibration against the committed pin

`SKILL.md:79` pins this command to `RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)`, and names r39 bash-pin cases 273–275. Observed cases 273–275 are `pin-bash-path-shim` exit 0, `bash-pin-override-missing` exit 2, `bash-pin-override-fake` exit 2. Those exits are the expected failures of the cases, still counted as `ok-case`. The summary matches the pin, including `, 0 skipped`.

`SKILL.md:696` records the same host line for the 275-case gate: `PASS (275 cases, 0 skipped)`. That note predates this round.

The summary is not a static banner. It is printed only when `failures` is 0, from the running counters, then the function exits 0 (`tools/research-gate.sh:8684-8686`):

```
printf 'RESEARCH_GATE_SELFTEST: PASS (%d cases%s)\n' "$cases" "${SKIPPED:+, $SKIPPED skipped}"
exit 0
```

`SKIPPED` is initialized to 0 (`:6153`) and incremented only on skip branches. `, 0 skipped` means that counter was still 0, which matches zero `skip-case` lines. A failure would have printed `RESEARCH_GATE_SELFTEST: FAIL (%d/%d cases)` and exited 1 (`:8688-8689`). That line was not printed.

### The round did not change the subject

HEAD is the measured commit. The worktree gate matches that blob. `git diff` and `git status --porcelain` for the path were empty.

```
2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34  tools/research-gate.sh
---HEAD---
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
---MEASURED---
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
---DIFF-STAT---
---WORKTREE-DIFF---
---LOG---
1bd9001 round-41: pin capture invocation surface (12/12); W04 dispositions (5/5); S075/S076; wave-1 spec prepared
6d914e9 round-39: capture bash pin (C1 7/8->8/8) + verifier/subject receipt binding (C2 8/8); r39 counters/verifier/expectations/claims, receipts x6, base+mutant controls, prepared validated w1 wave (32 seats, undispatched per host mapping)
870074e round-38: env-pin capture (C1 2/7->7/7, narrowed Errata 6/13) + receipt binding (C2 0/7->7/7, Errata 2-5,9-12); wave-2 closures (strict schema, type checks, PYTHONPATH -E pin, pre-run stale unlink, POSIXLY_CORRECT unset); S072/S073, knowledge x2, lesson 7 mistakes, QUALITY 55, receipts 9/9 verified; v1 two waves 32+32
504c1d2 round-38 freeze: env-pin capture (C1, ENV_PIN_CAPTURE_MATCH 2/7->7/7) + receipt binding (C2, RECEIPT_BINDING_MATCH 0/7->7/7); counters, verify-receipts, frozen claims, receipts, selftest 272
b905217 round-37 freeze: claim-pin provenance (C1) and pin-capture environment (C2) counters, gate fixes, selftest 262-267, frozen claims, base control
---BLOB-EQ---
ae10363a68ba9fb0375d0865801e16309999464b
ae10363a68ba9fb0375d0865801e16309999464b
```

Committed bytes versus worktree:

```
2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34  -
---WC---
409022 tools/research-gate.sh
409022
---ANCESTOR---
ancestor_exit=0
---TOUCH-SINCE-R41---
---STATUS-GATE---
```

`git show HEAD:tools/research-gate.sh | sha256sum` equals the worktree hash `2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34`. Both are 409022 bytes. Blob ids of `HEAD:tools/research-gate.sh` and `737f40b6aa8f37ffe2269db370fd6d65a720d9a8:tools/research-gate.sh` are the same `ae10363a68ba9fb0375d0865801e16309999464b`.

The last commit that touches the file is `1bd9001` (round 41). It is an ancestor of HEAD (`ancestor_exit=0`). `git log --oneline 1bd9001..HEAD -- tools/research-gate.sh` printed nothing. Round 42 and round 43 did not change the gate. `corpus/lessons/round-43.md:18` says the same; the git measurement is the evidence, not that sentence.

## Remaining risks

- This seat did not re-run `verify`, `verify-claims`, `verify-chain`, `verify-sweeps`, `verify-integrity`, `verify-all`, `--drift`, or the round-1 archive counter. Those results are not claimed here. An unrun check has not passed.
- Stdout and stderr were combined. The stream has no `FAIL-case` and no `skip-case`. Stderr emptiness was not measured on a separate fd.
- No committed transcript of all 275 `ok-case` lines was found to `cmp` against. Calibration is the summary pin plus cases 273–275, not a byte-identical prior log.
- Selftest temp scratch was not inventoried after the run.

## Blockers

None.
