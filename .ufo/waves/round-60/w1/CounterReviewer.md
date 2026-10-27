# CounterReviewer — round 60

## Scope and freeze identity

Reviewed the assigned frozen claims, current round-60 C1/C2 counters and their inputs, and prior committed C1 evidence only; no external fetch or source edits. The assigned SHA-256 is `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`, but `sha256sum corpus/evidence/round60-claims.md` returned `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`. The path is untracked (`git status --porcelain -- corpus/evidence/round60-claims.md` → `??`) and is absent from declared base `b379919a873e7080a31ef92c7002f55f5374e2c6` (`git cat-file -e <base>:corpus/evidence/round60-claims.md` exits 128). I left it untouched; cause/timing of the mismatch is unresolved, so conclusions below are conditional on the currently present claim text, not proof of the assigned bytes.

## Findings (high)

### C1 counter still admits an output-only/no-op builder

The current counter violates the stated requirement that the output-injection mutant be scored as failure (`corpus/evidence/round60-claims.md:7-11`). I reproduced with a builder whose only action is `print('=PASS')`, no filesystem output, and implicit exit 0:

```text
python3 corpus/evidence/round60/c1-count.py --builder /fast/scratch/hyaku/chousa-r60/CounterReviewer/forge.py --work /fast/scratch/hyaku/chousa-r60/CounterReviewer/c1 --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=1/1
C1=PASS
C1_EXIT=0
```

Mechanism: `run()` seeds the foreign sentinel, then defines candidate success as only `p.returncode == 0 and intact` (`corpus/evidence/round60/c1-count.py:35-44`). The output-only builder leaves the sentinel intact and is classified `candidate_safe`; the probe is considered blocked merely because its state is not the distinct `forged_safe` state (`:58-70`). Thus `INJECTION_REJECTED=1/1` means only “not classified as destructive,” while the same mutant also satisfies `candidate_ok` and produces top-level `C1=PASS`. No emitted bytes need enter verdict parsing for this false acceptance. This is distinct from, and does not repair, the prior R59 demonstrated stderr-token injection in the R58 counter (`.ufo/waves/round-59/w1/R59Executor09.md:215-260`). The narrow sentinel is insufficient to establish a functioning safe path; the declared counter target is not met.

### C2 counter passes the required-failing base and does not test a new note

Reproduced against the current lane root; the unchanged existing state exits 0:

```text
python3 corpus/evidence/round60/c2-count.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --work /fast/scratch/hyaku/chousa-r60/CounterReviewer/c2
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
C2_EXIT=0
```

The frozen text requires base failure because no round-60 entry exists and requires checking the new note's exact observation/no-overreach (`round60-claims.md:15-17`). Instead `ENTRY` is the pre-existing `corpus/knowledge/citation-count-semantics-r37.md` (`corpus/evidence/round60/c2-count.py:8,13`); `metadata` and `scoped` are substring tests against that existing entry (`:17-18`). This provides a direct base-pass counterexample and cannot establish a newly admitted round-60 correction. Additionally, although `--root` controls `raw` and `entry`, `form` is resolved from script-global `ROOT` (`:7,13`), so a lane-copy test mixes roots and is not isolated as the predicate specifies.

## Residual risk and verification gaps

- Both counters can print PASS while failing their respective declared predicates; neither claim is supported by its counter's current verdict.
- No `lsp` device/status route was exposed in the available tool inventory; this review used literal source inspection and execution, not semantic LSP references/diagnostics.
- Freeze provenance is unresolved; do not silently treat the local hash as the assigned frozen artifact or alter/redefine the predicate to compensate.
- No builder safety beyond the narrow sentinel check, present-day external truth, or broader C1 hazard matrix was assessed.
