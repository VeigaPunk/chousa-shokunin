# R59Critic56 — round-59 falsification (calibration)

A report from an earlier run existed at this path; this file supersedes it. Its claims-absence and `c1-before.txt` observations were re-checked below and hold. This run adds a static proof that the inherited counter cannot emit a positive verdict.

## Verdict
Both claims were falsified: the round-59 frozen claims file is absent, and the counter every seat is running against can never print `C1=PASS`.

## Counterexample 1 — the frozen claims file does not exist (provenance)
- `corpus/evidence/round59/claims.md` is absent on disk. The directory holds only `census-*`, `quarantine-*`, `s101-open.txt` and `controls/c1-before.txt`.
- `git log --all -- corpus/evidence/round59/claims.md` is empty, so the file never existed in any revision. HEAD is `026174e` "round-59: preserve partial unadjudicated evidence".
- `git status` shows only `?? .ufo/waves/round-59/`, so the file was not simply left uncommitted.
- `w1-spec.json` and `w1-dispatch.json` both tell every seat to read this path. The only claims file nearby is `corpus/evidence/round58/claims.md` (sha256 `7aedd8156c9fce185841a740b894600f8a4149b2d8e2034039f634c808373457`).
- No round-59 predicate, counter revision, kill rule or accepted source boundary is therefore frozen. Any "positive path reached" statement for round 59 has nothing to be calibrated against.

## Counterexample 2 — the inherited counter cannot emit a positive verdict (mechanical, static)
Counter: `corpus/evidence/round58/c1-count.py`, sha256 `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`. This is the object the round-59 C1 receipt was copied from.

- `:51` sets `PASS = "pass"` (lowercase).
- Every refusal-leg success emitter uses that constant, so it prints lowercase:
  - `:160` prints `{name}=pass(refused)`.
  - `:223` prints `FOREIGN=pass(refused)`.
  - `:234` prints `SYMLINK_OUT=pass(refused)`.
  - The `ESCAPE_ENTRY=pass(refused)` leg is lowercase too.
- `:391` computes `ref_pass = all("=PASS" in l for l in ref_legs)`, and `:399` computes the summary `REFUSE=` from `'=PASS' in l`. Both are case-sensitive uppercase checks.
- I confirmed the mismatch with `python3 -c "print('=PASS' in 'FOREIGN=pass(refused)')"`, which prints `False`.
- The only literal `=PASS` in the file is in the `CONTROL_…=PASS(!)` leg at `:378`, and that leg is not in `ref_legs`.
- So even a builder that satisfies all 7 refusal legs prints `REFUSE=0/7`, then `C1=FAIL`, and exits 1. `REFUSE=0/7` in the receipt is therefore not evidence about the builder.
- The 4 safe legs are checked as lowercase `=pass` at `:390`, which is why they show `OK=4/4`. `:389` is a dead assignment, immediately overwritten by `:390`.
- `ESCAPE_ENTRY` is a refusal-shaped leg (`pass(refused)`) but is counted in `ok_legs` at `:384-385`. The `OK`/`REFUSE` split is internally inconsistent.

## Counterexample 3 — the do-nothing control discriminates nothing
- `:377` marks a control "denied" whenever its output is not exactly `C1=PASS`.
- Because of counterexample 2, every candidate (do-nothing, flawed base, or perfect builder) is denied. `round58/controls/c1-controls.txt` shows `DENIED=2/2`, and that carries no information.
- A control that fails by import crash or wrong reason is indistinguishable from one that fails by design.
- The round-59 receipt `controls/c1-before.txt` shows `DENIED=0/0`, so no controls were run. It is also byte-identical to round 58's: both are 958 B, sha256 `2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe` (digest quoted from R59Reviewer44, not recomputed here).
- The copy has no header: no command line, builder identity or counter revision. It cannot satisfy the lane rule that a counter's revision is pinned inside its receipt. The round-58 `c1-controls.txt` does carry a command header and an interpretation footer.

## Smaller observations
- `c1-before.txt` is a pinned r55 base run, so its `FOREIGN=fail … foreign gone=True` and `BEFORE_FOREIGN=deleted` are legitimate negative evidence that the destructive leg can fail.
- `FIFO_TXT` and `DEVZERO_TXT` fail on token mismatch. The builder refused with "no defined text form … no .txt", which suggests those fixtures do not exercise the intended hazard. The token rule, as the receipt shows it, accepts only `NOT_REGULAR`/`SIZE`/… words.
- `FAT_RAW` refused with `ole-malformed: sector shift 0`. That is a refusal, but not a size-cap refusal, so the fixture does not hit the intended `SIZE` path.
- `census-start.txt` and `census-end.txt` are identical (`diff` clean). The five W04 duplicate-url warnings are unchanged and not addressed.
- The quarantine files show 20 of 24 ids unverifiable or absent from local captures (`no-capture` or binary office docs never rendered). The register-family ids `S100`–`S103` are unchecked because no locator was named. This evidence supports no positive claim.

## Impacted axes
- **Calibration** is hit hardest. A positive verdict path is unreachable by construction, and the two receipts that exist carry zero or vacuous control information.
- **Operability** is hit by the missing claims file, which every seat was told to read.
- **Depth** is hit because the offline reconnaissance output is only the census copy and the quarantine tables.

## Smallest safe correction
1. Commit a round-59 `claims.md` before any seat is scored. It must name a counter revision by sha256 and say whether `c1-count.py` is amended.
2. Amend the counter by normalising the case of the `=PASS`/`=pass` comparisons. This is a frozen-counter change, so it needs its own pin and a fresh receipt.
3. Before trusting any `C1=PASS`, generate two controls: a perfect-refuser builder that must reach `C1=PASS`, and a do-nothing builder that must be denied for the named reason.
4. Preserve `c1-before.txt` unchanged as the negative baseline, with a header added in a sibling file rather than by editing it.

## Scope
Read-only. No scratch was created (none needed), no external fetch, no install, no lane or frozen-file edits. The only write is this file.
