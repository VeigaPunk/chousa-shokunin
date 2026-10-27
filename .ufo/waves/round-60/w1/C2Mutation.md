# C2Mutation — round 60 bounded probe

## Scope and frozen input

Targeted frozen claim C2, “depth (sourced S101),” in `corpus/evidence/round60-claims.md`. The task supplied immutable SHA-256 `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`; observed file SHA-256 was `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`. The file was untracked (`git status --porcelain` reported `?? corpus/evidence/round60-claims.md`), so its bytes do not match the specified frozen input. I left it untouched; this probe is against the currently observed claim/counter/source only and must not be treated as validating the supplied hash.

## Mutation and detector

Mutant: change the counter's `EXPECTED` phrase from `文献类型及载体类型标志` to the plausible wrong-section wording `文献类型及载体类型标识` (one-character behavior-bearing constant change). The changed phrase occurs once in the pinned source form, but at line 7 rather than the intended section-14.2 quote at line 245. This tests whether the counter binds the claimed quote to its intended source location rather than merely locating the phrase somewhere in the capture form.

Detector, same command each time, in an isolated copy under `/fast/scratch/hyaku/chousa-r60/C2Mutation`:

```sh
python3 /fast/scratch/hyaku/chousa-r60/C2Mutation/corpus/evidence/round60/c2-count.py --root /fast/scratch/hyaku/chousa-r60/C2Mutation --work /fast/scratch/hyaku/chousa-r60/C2Mutation/work
```

| State | Counter SHA-256 | Actual detector output | Exit |
|---|---|---|---:|
| Pristine | `a19b06789f02a3aa9d4bf52a7a215f5614076706056ab9fcd300fdc131e83abe` | `RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1` then `C2=PASS` | 0 |
| Mutated | `67b2d0ee3aabef812d6d3ac452a11934bd1f6820d856ddc01fee20cae3535901` | `RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=7 METADATA=1/1 LIMIT=1/1` then `C2=PASS` | 0 |
| Restored | `a19b06789f02a3aa9d4bf52a7a215f5614076706056ab9fcd300fdc131e83abe` | `RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1` then `C2=PASS` | 0 |

## Verdict and restoration

**SURVIVED** — detector does not reject the plausible wrong-section quote constant. It requires a unique occurrence of the configured substring, but not the section/quote location or semantic identity required by the frozen C2 claim (“quote locations” and verification of the “exact observation”). The mutant's output demonstrates the false pass at line 7. This is a coverage finding about the counter only; it does not change the claim contract or authorize a repair.

Restoration evidence: restored counter bytes hash exactly matches the pristine hash (`a19b…83abe`); restored detector again passes at intended line 245. The frozen claim was never edited. Scratch was explicitly removed before handoff.
