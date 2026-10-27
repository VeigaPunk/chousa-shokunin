# C1Mutation — round-60 w1 mutation probe

Seat: mutation-tester (leaf, no subagent dispatch). Scope honored: prior committed evidence
(`.ufo/waves/round-60/c1-before.txt`, `c1-control-proof.txt`), the frozen claims
(`corpus/evidence/round60-claims.md`), and the current counter source
(`corpus/evidence/round60/c1-count.py`) only. No external live fetch, no writes outside this
report, no git/jj mutation anywhere, scratch used and removed (proof below).

## Challenged invariant

Frozen C1 predicate (round60-claims.md, C1 frozen predicate): the counter "exits 0 only when
the frozen safe and hazard legs meet their declared requirements", with verdicts "derived from
child return codes and independently observed filesystem state".

## Mutant M1 — one plausible defect, smallest behavior-bearing point

File: `corpus/evidence/round60/c1-count.py` line 38, in `run()` — the sole filesystem-integrity
derivation feeding all three leg labels:

```diff
-        intact = foreign.is_file() and foreign.read_bytes() == before
+        intact = foreign.is_file()
```

One expression, one semantic bit: byte-exact preservation of the foreign span file degrades to
existence-only. Plausibility: this is the natural "simplification" of the check, and it is the
only place the claim's "independently observed filesystem state" enters the verdict.

## Detector (bounded, identical across all phases)

Probe builder `clobber.py` run as `--builder`: exits 0, prints the round-58 target token
(`=PASS`), and REWRITES the seeded foreign file `out/spans/S777-1.txt` (`preserve-me\n` →
`CLOBBERED-BYTES\n`) WITHOUT deleting it. Invocation per the frozen predicate form:
`python3 -B <counter> --builder <clobber.py> --work <fresh-absolute-dir> --seed 6001`.
Expected: pristine must FAIL (exit 1) because bytes differ; if any variant PASSES, the
weakened derivation is a real defect the frozen iff does not cover.

All runs executed on an isolated byte-identical mirror at
`/fast/scratch/hyaku/chousa-r60/C1Mutation/mirror/` (counter sha256 before run:
`66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7`, identical to the lane file;
`corpus/evidence/round58/` copied so the counter's pinned R55 control resolves inside the
mirror). The lane tree was never executed from or modified.

## Outputs (verbatim)

Pristine (sha256 `66e50763…`) vs clobber probe — `C1=FAIL`, exit 1:

```
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
exit=1
```

Mirrored pristine with the declared invocation (`--builder` = mirrored default
`tools/build-spans.py`) reproduces the frozen pre-work receipt `c1-before.txt` exactly
(`INJECTION_REJECTED=1/1`, `BASELINE_DISCRIMINATES=1/1`, `CANDIDATE_REFUSAL=0/1`, `C1=FAIL`,
exit 1) — mirror-faithfulness baseline.

Mutant (sha256 `031e0b5f1f429955acd4bcf0c1ab07e8b96f45eaf0220920580801248cce382c`) vs the SAME
probe — `C1=PASS`, exit 0, while the candidate-leg foreign file on disk held
`CLOBBERED-BYTES\n` (od-verified):

```
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=1/1
C1=PASS
exit=0
```

Restored (sha256 `66e50763…`, `cmp` byte-identical to the saved pristine copy) vs the SAME
probe — pristine behavior returns exactly:

```
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
exit=1
```

## Verdict: KILLED

The detector distinguishes pristine (rejects content-clobber, exit 1) from mutant (accepts it,
exit 0) on identical inputs; restoration returns pristine behavior. The mutated expression is
load-bearing for the frozen C1 iff: byte-exactness is the sole guard that keeps a leg whose
filesystem state was damaged (content destroyed, file present, `=PASS` emitted, exit 0) from
producing `C1=PASS`. Finding is coverage credit for the current bytes, not a contract change;
no lane file was altered.

## Static finding (no second mutation; bounded note)

The `forged_safe` label is unreachable: `forged_safe = p.returncode == 0 and not intact` is
identical to `baseline_bad`, and the return ternary tests `baseline_bad` first
(c1-count.py:41-44), so `"forged_safe"` is never returned. Hence
`forge_blocked = forge_state != "forged_safe"` is vacuously true for every possible outcome —
consistent with observation: all four runs printed `INJECTION_REJECTED=1/1` regardless of
candidate-leg outcome. The INJECTION_REJECTED leg, alone, cannot fail; the claim's
"(c) output-injection mutant … scored as a failure" is carried entirely by the composite
`passed` gate through `candidate_ok` and `baseline_discriminates`. Substance of the claim holds
at the composite level; the leg-level semantics are degenerate. Recorded as a robustness note
for the L1; not a defect in the frozen predicate's observable behavior.

## Integrity discrepancy — immutable claim SHA

The seat tasking states "The exact immutable claim SHA is
`09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`". Observed:
sha256(`corpus/evidence/round60-claims.md`) =
`65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1` (3355 bytes). Canonicalization
variants tried — no-trailing-newline/stripped `cae804fa…`, CRLF `dbb847b8…`, double-newline
`ed2999d0…` — and per-section digests (`## C1…` `99c6729a…`, `## C2…` `db4ffb5f…`), git blob
sha1 `5ea0acf0…`, `w1-dispatch.json` `4d34c1ea…`, `w1-spec.json` `c5662bdb…`: none match
`09d8053f…`. The string appears only inside seat prompts (w1-spec.json/w1-dispatch.json, same
value for every C1 seat); no lane receipt explains what it hashes. Freeze integrity post-dispatch
is intact on available evidence: claims mtime 2026-10-27 17:51:18 -0300 predates `w1.ready`
17:55:21 and `w1.ready.dispatched` 17:56:56, and start/end hashes match. The tasking's hash
corresponds to no current bytes — most plausibly a pre-finalize draft [INFERENCE]. Surfaced for
L1/operator reconciliation; nothing was modified to force a match.

## Restoration and cleanup evidence

- Lane claims file end hash: `65721569…` — identical to session start; mtime unchanged
  (2026-10-27 17:51:18 -0300). Freeze untouched after dispatch.
- Lane counter end hash: `66e50763…` — untouched; no lane write outside this report.
- Scratch `/fast/scratch/hyaku/chousa-r60/C1Mutation/` removed before yield; parent listing
  confirms absence (`CONFIRMED: … absent`), sibling scratch dirs untouched.
- No tool installs; no commits; no git/jj commands beyond read-only inspection.
