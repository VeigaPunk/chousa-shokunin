# Round 34 W1 — CtlC1Sampled

## Result and axes

Scored axis: **operability**. Control axes: sampled-work fidelity, frozen-detector provenance, exact byte restoration. All three controls **MISSES** on each of two fresh seeds. No control reaches 30/30. The requested six mutant scores completed; auxiliary pristine/restored detector runs did not complete, so the strict mutation-testing verdict is **INCONCLUSIVE**, not a claimed killed mutant.

All paths below are lane-relative unless absolute. Artifact root `A=.ufo/waves/round-34/w1/CtlC1Sampled/`; scratch root `S=/fast/scratch/hyaku/chousa-r34/w1/CtlC1Sampled/`. Access date for opened files: **2026-10-23**. No installs, network, subagents, candidate implementations, production edits, Git/JJ writes, or counter edits.

## Frozen inputs and expected detector

Read `corpus/evidence/round34/claims.md` first, then `corpus/evidence/round34/c1-count.py:1-59`, and `skill://godspeed` plus `/home/vgpnk/.omp/agent/RULES.md` before implementation. Relevant contract: `claims.md:34-43`; per-record detector and run validity: `c1-count.py:280-305`; predicate: `:316-338`.

Located quote, `corpus/evidence/round34/c1-count.py:51-53`: “An id printed on two CLAIM lines scores "none".”

Initial command, exit 0:

```sh
timeout 30s sha256sum "$S/base-gate.sh" corpus/evidence/round34/c1-count.py
```

Observed base SHA-256: `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`.
Observed frozen counter SHA-256: `5ef347874960b52561a1cfa517f3f3fc0d1763830e3580c44b993f8394c0a565`.
Every completed receipt carries those frozen counter bytes, `gate_rc=1`, `gate_timed_out=false`, `predicate_holds=false`. The counter only scores nonzero records after observing the required DRIFT line (`:281-283`).

Expected detector: full literal verification should reject any changed byte, separated halves and glued boundaries, and preserve line binding. These sampled controls should miss the target when skipped mutation bytes produce false support, or when the long-pattern path fails to operate. A passing pristine detector is required before calling a mutant killed; none was established by this seat.

## Mutants, minimal surface and hashes

Copied the verified base into three scratch gates; only the regex-building loops inside `tok_span_at` and `tok_span_all` changed. Existing boundary checks, line binding, parsing, findings and short-span matcher remain intact. Controls apply at span length >=32768; short spans retain the base implementation. Mutated gates were archived before scoring and remain available under A; scratch gate paths were subsequently restored.

| Control | Behavior and archived source location | Archived SHA-256 |
|---|---|---|
| a: stride1024 | 64-byte literal windows at offsets 0,1024,... while a full window fits. DOTALL fixed-length gaps force each later window to its correct offset from the first. A trailing gap consumes the full span length. `A/stride1024-gate.sh:1563-1585,1608-1630`. | `36d30a618e283c5af881538eaabce3d7b8789d41b1aa84741d82c1b2cfa09373` |
| b: fixed32 | 32 literal 64-byte windows at `floor(k*len/32)`, k=0..31; fixed-length DOTALL gaps and trailing gap as above. `A/fixed32-gate.sh:1563-1586,1609-1632`. | `aa9b609d498a3bdc66c5ec29e350e0784c0e49cd8a432998db35d240f45b05a4` |
| c: wildcard7 | Existing hex pattern with `.` at zero-based byte indices `i%7==3`, DOTALL enabled. Stop after a complete byte atom reaches 131000 encoded pattern bytes (maximum overshoot three bytes, still below 131072); remaining suffix is not searched. Full-span boundary and line calculations remain as at base. `A/wildcard7-gate.sh:1563-1574,1597-1608`. | `6a8c50f4fc9910f04ad949577e0f0f6855a02ebd052e9edf6a482e2377baac09` |

Before each mutation, bytes were identical to the recorded base. Artifact sizes from `timeout 30s stat --printf='%n %s bytes\n' ...` (exit 0): stride 358715 bytes; fixed32 358709; wildcard7 358141. Each is below 1 MiB.

## Exact scoring procedure and outputs

Each command ran from `/home/vgpnk/Projects/shokunin/chousa-shokunin`. `A/run-counter.py` preserves the original UTF-8-locale runner; `A/run-counter-final.py` preserves the later explicit-C-locale runner. Both run the committed counter unchanged. Each `A/<name>.run.json` contains the complete argv, cwd, environment, PID/PGID, exit code, elapsed time, input/output hashes. `A/<name>.stdout.txt` and `.stderr.txt` contain actual counter output.

Invocation template for each completed control run:

```sh
timeout --kill-after=15s 1700s python3 "$S/run-counter.py" NAME "$S/CONTROL-gate.sh" SEED
```

The runner invokes the following bounded detector with `C1_TMP=$S TMPDIR=$S PYTHONDONTWRITEBYTECODE=1`; wildcard runs additionally set `LC_ALL=C`. Stride/fixed runs inherited `LANG=en_US.UTF-8`, with LC_ALL unset (observed by `timeout 30s locale`, exit 0).

```sh
timeout --kill-after=15s 1600s prlimit --as=2147483648 --nproc=32768 --fsize=16777216 \
  python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round34/c1-count.py \
  --gate "$S/CONTROL-gate.sh" --seed SEED \
  --receipt "/home/vgpnk/Projects/shokunin/chousa-shokunin/$A/NAME.json"
```

| Control | Seed | Actual count | Counter exit | Elapsed seconds (runner) | Verdict | Receipt under A |
|---|---:|---|---:|---:|---|---|
| a | 348721 | LONGSPAN_MATCH=26/30 | 1 | 924.707 | MISSES | `stride1024-s348721.json` |
| a | 348722 | LONGSPAN_MATCH=25/30 | 1 | 913.591 | MISSES | `stride1024-s348722.json` |
| b | 348721 | LONGSPAN_MATCH=26/30 | 1 | 1088.065 | MISSES | `fixed32-s348721.json` |
| b | 348722 | LONGSPAN_MATCH=25/30 | 1 | 1060.152 | MISSES | `fixed32-s348722.json` |
| c | 348721 | LONGSPAN_MATCH=22/30 | 1 | 599.491 | MISSES | `wildcard7-c-s348721.json` |
| c | 348722 | LONGSPAN_MATCH=21/30 | 1 | 602.085 | MISSES | `wildcard7-c-s348722.json` |

Actual per-class output lines, consolidated without changing counts:

```text
class                 a348721 a348722 b348721 b348722 c348721 c348722
long-verbatim-ml       3/3     3/3     3/3     3/3     0/3     0/3
long-verbatim-1l       2/2     2/2     2/2     2/2     1/2     0/2
long-edge              2/2     2/2     2/2     2/2     2/2     2/2
long-mut-head          2/2     2/2     2/2     2/2     2/2     2/2
long-mut-tail          0/2     0/2     0/2     0/2     2/2     2/2
long-mut-mid           1/3     0/3     1/3     0/3     3/3     3/3
long-split             2/2     2/2     2/2     2/2     2/2     2/2
long-glued-left        2/2     2/2     2/2     2/2     2/2     2/2
long-glued-right       2/2     2/2     2/2     2/2     2/2     2/2
long-line-bound        2/2     2/2     2/2     2/2     0/2     0/2
long-line-wrong        2/2     2/2     2/2     2/2     0/2     0/2
short-verbatim         3/3     3/3     3/3     3/3     3/3     3/3
short-mut              3/3     3/3     3/3     3/3     3/3     3/3
```

For a and b, all misses are false support for tail/middle mutations; e.g. `A/stride1024-s348721.json:31-55` and `A/fixed32-s348722.json:31-61`. Thus the counter distinguishes these sampled approximations on both seeds. No MEETS-TARGET control was observed; no claim that the counter let a shortcut through.

For c, both receipts contain `grep: regular expression is too large` (`A/wildcard7-c-s348721.json:11`, `A/wildcard7-c-s348722.json:11`). Its misses are supported/mislocated truths reported unsupported (`:31-79` and `:31-85` respectively). This is an operability miss confounded by the PCRE compiled-pattern limit, not evidence that wildcarded mutation bytes themselves were comprehensively covered. The long-edge cases do operate (2/2 each); broad unsupported-case scores alone do not prove searches succeeded.

## Pristine/restored detector attempts and limitations

Initial pristine attempts on seeds 348721/348722 used `--nproc=2000`, failed immediately before starting the gate with `BlockingIOError: [Errno 11] Resource temporarily unavailable`, exit 1, elapsed 0.127/0.113 seconds, and produced no receipts. Their actual stderr and metadata remain at `A/pristine-s348721.*` and `A/pristine-s348722.*`. `timeout 30s ps -u vgpnk -o pid= | timeout 30s wc -l` returned 241 processes; [INFERENCE] same-UID thread accounting made the lower nproc cap unusable. Raised the bounded cap to 32768 while retaining 2 GiB address-space cap; no tool installation.

UTF-8 pristine retries were stopped after 1072.122/1072.119 seconds without a completed score, only by their recorded own PGIDs 1611446/1611457 (`A/cancellations.json`; kill command exit 0; runner child return -15, shell exit 241). These are not 0/30 scores or valid receipts.

Ran the exact same frozen counter on pristine `S/base-gate.sh` and restored `S/stride1024-gate.sh`, seed 348721, with explicit `LC_ALL=C`, same caps and receipts requested. Outer bound was `timeout --kill-after=15s 420s ...`, rather than 1700s. Both were stopped before that outer bound to keep the seat time box, after 324.626/324.583 seconds, with empty captured stdout/stderr and no receipt. Child return -15, shell exit 241. Metadata: `A/pristine-c-s348721.run.json`, `A/restored-c-s348721.run.json`; exact signal evidence: `A/baseline-cancellations.json`. Only own recorded PGIDs 2545352/2546292 were signalled. All owned bounded jobs completed before return.

Consequently the required control scores are complete, but a complete pristine/restored behavioral comparison is unavailable. **Strict mutation-test verdict: INCONCLUSIVE.** These cancelled auxiliary runs must not be cited as killed mutants, passing baselines, or completed LONGSPAN_MATCH counts. Locale differs between a/b and c; [INFERENCE] fixture ASCII bytes make the locale change semantically irrelevant, but no paired locale-equivalence proof is claimed.

## Restoration and production safety

After each control's two runs completed, restored its scratch gate with `timeout 30s cp "$S/base-gate.sh" "$S/CONTROL-gate.sh"` (each exit 0). Archived mutant gates under A were intentionally retained. Final `timeout 30s sha256sum` over base, all three restored scratch gates, production gate, frozen counter, and all three archived mutant gates exited 0. All four scratch gates and production gate were exactly:

`43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`

Frozen counter remained exactly:

`5ef347874960b52561a1cfa517f3f3fc0d1763830e3580c44b993f8394c0a565`

All three archived controls retained the mutant hashes recorded above. Full before/mutated/restored values, operations and exit codes: `A/restoration.json`. `timeout 30s df -h /fast` before fixture work showed 88G available. At most four counters were active at once. Two wildcard async launch attempts were refused by the global 100-background-job cap; reran them in foreground concurrent tool calls, yielding the actual receipts above. No production behavior was repaired or shipped by this probe.
