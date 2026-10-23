# MutOracleC2 — C2 feasibility and sensitivity

**Disclosed feasibility reference only, never a candidate implementation.** [Oracle](MutOracleC2/oracle.sh): self-contained bash launcher with Python gate; exact raw-byte SHA-256, strict lowercase 64-hex strings, source refusals before file reads/hashing, stale before span lookup, and the documented byte-exact token boundaries (including word-internal hyphens/apostrophes). It also retains absent-pin and contradiction-marker behavior. Only the frozen C2 counter was exercised; no claim is made that these fixtures exhaust the contract.

Seeds were freshly drawn once, before running: A=`957710451340456525`, B=`1158866592272045467`, C=`6871766983261281141`, D=`7173473380861898692`, E=`1742427719550887417`. Scores below are `REVISION_BINDING_MATCH=k/120`, in listed seed order.

| Control | Counter | Seeds | Score | Counter receipts |
|---|---|---|---|---|
| Full-contract oracle | C2 | A/B/C/D/E | 120/120 each | [A](MutOracleC2/oracle-feasibility-seed957710451340456525.json), [B](MutOracleC2/oracle-feasibility-seed1158866592272045467.json), [C](MutOracleC2/oracle-feasibility-seed6871766983261281141.json), [D](MutOracleC2/oracle-feasibility-seed7173473380861898692.json), [E](MutOracleC2/oracle-feasibility-seed1742427719550887417.json) |
| [Case-insensitive](MutOracleC2/case-insensitive.sh) | C2 | A/B/C | 117/120, 116/120, 115/120 | [A](MutOracleC2/case-insensitive-mutated-seed957710451340456525.json), [B](MutOracleC2/case-insensitive-mutated-seed1158866592272045467.json), [C](MutOracleC2/case-insensitive-mutated-seed6871766983261281141.json) |
| [Strip/normalize line ends](MutOracleC2/normalized-eol.sh) | C2 | A/B/C | 84/120, 83/120, 82/120 | [A](MutOracleC2/normalized-eol-mutated-seed957710451340456525.json), [B](MutOracleC2/normalized-eol-mutated-seed1158866592272045467.json), [C](MutOracleC2/normalized-eol-mutated-seed6871766983261281141.json) |
| [Span before stale](MutOracleC2/span-before-stale.sh) | C2 | A/B/C | 110/120 each | [A](MutOracleC2/span-before-stale-mutated-seed957710451340456525.json), [B](MutOracleC2/span-before-stale-mutated-seed1158866592272045467.json), [C](MutOracleC2/span-before-stale-mutated-seed6871766983261281141.json) |
| [Accept `sha256:` prefix](MutOracleC2/accept-prefix.sh) | C2 | A/B/C | 116/120, 113/120, 119/120 | [A](MutOracleC2/accept-prefix-mutated-seed957710451340456525.json), [B](MutOracleC2/accept-prefix-mutated-seed1158866592272045467.json), [C](MutOracleC2/accept-prefix-mutated-seed6871766983261281141.json) |
| [Trim whitespace](MutOracleC2/trim-value.sh) | C2 | A/B/C | 117/120, **120/120**, 119/120 | [A](MutOracleC2/trim-value-mutated-seed957710451340456525.json), [B](MutOracleC2/trim-value-mutated-seed1158866592272045467.json), [C](MutOracleC2/trim-value-mutated-seed6871766983261281141.json) |
| [Bash `$(cat)` bytes](MutOracleC2/bash-cat.sh) | C2 | A/B/C | 84/120, 83/120, 82/120 | [A](MutOracleC2/bash-cat-mutated-seed957710451340456525.json), [B](MutOracleC2/bash-cat-mutated-seed1158866592272045467.json), [C](MutOracleC2/bash-cat-mutated-seed6871766983261281141.json) |

## Kill matrix and expected detector

Expected for every mutation: the same frozen counter on the same seed passes pristine/restored bytes at 120/120 and rejects mutated bytes below 120/120. **All 36 pristine/restored runs passed.** K=killed; S=survived; no inconclusive runs.

| Dropped rule / precise mutation | Exposed class(es) | A | B | C |
|---|---|---|---|---|
| Lowercase-only hash: lowercase the supplied string before validation/equality | I1 uppercase: 3/4/5 misses | K | K | K |
| Exact source bytes: CRLF/CR→LF, then remove trailing LF before hashing | R1 24 misses; R2 10; S2 2/3/4 | K | K | K |
| Stale precedence: an absent delimited span returns unsupported before comparing the hash | S4 all 10 misses | K | K | K |
| Exact hash spelling: remove `sha256:` before validation/equality | I1 prefixed: 4/7/1 misses | K | K | K |
| Exact hash spelling: `.strip()` before validation/equality | I1 spaced: 3/0/1 misses | K | **S** | K |
| Exact source bytes: discard NUL and trailing LF as bash command substitution does; preserve CR | R1 24 misses; R2 10; S2 2/3/4 | K | K | K |

Case-insensitive here means uppercase pins are accepted. Case-folding only the comparison behind an unchanged lowercase-only validator would be an equivalent mutant, not a defect. Each retained mutant changes only its named rule. The newline mutants use different transforms despite identical score vectors on these seeds.

## Findings

- **Maximum defective score: 120/120.** Whitespace trimming survives seed B. The unmodified generator randomly draws the 14 I1 subtypes rather than guaranteeing each subtype: B contains seven prefixed, four uppercase, one long, two short, and **zero spaced** pins. [Fixture replay receipt](MutOracleC2/fixture-subtypes.json) records the actual subtype counts; this is a sensitivity gap, not a label trick or source-reading shortcut. Prefix acceptance also approaches the target at 119/120 on C, with only one prefixed pin.
- Feasibility holds on all five requested fresh seeds; no correct-reference class failed. Five mutants are killed on every requested seed; whitespace trimming is killed on A/C but survives B (17 seeded kills, one survival). The frozen multi-run P2 would still reject that trim mutant on the observed A/C failures; the separate pre-data control rule is violated by its B pass.

## Restoration, bounds and evidence

All edits were isolated to `/fast/scratch/hyaku/chousa-r31/MutOracleC2/active.sh`. Before/final SHA-256 are identical: `96d63bcd3fb4f832e518730f52b2519fb1242c8bf7bb57a2e90f44d5e1cd2656`; final bytes also compare exactly equal to the original. [Restoration receipt](MutOracleC2/restoration.json) records this, all detector runs' byte stability, and unchanged counter/base-gate hashes. [Machine-readable kill matrix](MutOracleC2/kill-matrix.json) includes each mutant's full hash, all pristine/mutated/restored receipt paths, per-class misses and verdicts. Every counter receipt has a neighboring `.execution.json` with actual stdout/stderr, exit status, command, and before/after gate hashes.

59 counter runs total, each from the lane root, wrapped in `timeout 900`, limited to 512 MiB address space, 90 CPU seconds and 4096 UID processes, with one counter at a time. Each detector subprocess had a separate process group, cleaned after completion; no background services remain. No network, git/jj writes, lane source/counter edits, or tool installations/updates. Reproduction supervisor and fixture-audit source are archived beside the receipts; [campaign](MutOracleC2/campaign.json) freezes seeds, inputs and limits.

design broken: randomized invalid-pin subtypes omit whitespace cases, letting a whitespace-trimming control reach 120/120 on seed 1158866592272045467.

## v2 re-score

The preceding sections and receipts are preserved v1 evidence. Re-scored all seven frozen controls under design v2, commit `8070f92bac6ba1f2dfb6c29d66303d60a1e7dac7`. Every one of the **24 new counter receipts** was checked against C2 SHA-256 `1064fdb356e25440c64bb4d4d5363acb9c1bbc32c687c8ea50096d74c849d500`. All scripts are byte-identical to their v1 artifacts: they already emit the required revision-mismatch finding exactly for their own stale verdicts, so no finding-only repair was needed.

Three fresh, pre-drawn seeds shared across controls: F=`2015044819141004956`, G=`3568399740835207276`, H=`6840692661700775995`. The oracle was run first on all three seeds and again after the mutants, scoring 120/120 throughout.

| Control | Counter | Seeds | Scores F/G/H | Counter receipts | Verdict |
|---|---|---|---|---|---|
| Full-contract feasibility oracle | C2 v2 | F/G/H | 120/120 each | [F](MutOracleC2/v2/oracle-rescore-seed2015044819141004956.json), [G](MutOracleC2/v2/oracle-rescore-seed3568399740835207276.json), [H](MutOracleC2/v2/oracle-rescore-seed6840692661700775995.json) | Feasible, not a candidate |
| Case-insensitive | C2 v2 | F/G/H | 117/120 each | [F](MutOracleC2/v2/case-insensitive-rescore-seed2015044819141004956.json), [G](MutOracleC2/v2/case-insensitive-rescore-seed3568399740835207276.json), [H](MutOracleC2/v2/case-insensitive-rescore-seed6840692661700775995.json) | K/K/K |
| Strip/normalize line ends | C2 v2 | F/G/H | 83/120 each | [F](MutOracleC2/v2/normalized-eol-rescore-seed2015044819141004956.json), [G](MutOracleC2/v2/normalized-eol-rescore-seed3568399740835207276.json), [H](MutOracleC2/v2/normalized-eol-rescore-seed6840692661700775995.json) | K/K/K |
| Span before stale | C2 v2 | F/G/H | 110/120 each | [F](MutOracleC2/v2/span-before-stale-rescore-seed2015044819141004956.json), [G](MutOracleC2/v2/span-before-stale-rescore-seed3568399740835207276.json), [H](MutOracleC2/v2/span-before-stale-rescore-seed6840692661700775995.json) | K/K/K |
| Accept `sha256:` prefix | C2 v2 | F/G/H | 117/120 each | [F](MutOracleC2/v2/accept-prefix-rescore-seed2015044819141004956.json), [G](MutOracleC2/v2/accept-prefix-rescore-seed3568399740835207276.json), [H](MutOracleC2/v2/accept-prefix-rescore-seed6840692661700775995.json) | K/K/K |
| Trim whitespace | C2 v2 | F/G/H | **118/120 each** | [F](MutOracleC2/v2/trim-value-rescore-seed2015044819141004956.json), [G](MutOracleC2/v2/trim-value-rescore-seed3568399740835207276.json), [H](MutOracleC2/v2/trim-value-rescore-seed6840692661700775995.json) | K/K/K |
| Bash `$(cat)` bytes | C2 v2 | F/G/H | 83/120 each | [F](MutOracleC2/v2/bash-cat-rescore-seed2015044819141004956.json), [G](MutOracleC2/v2/bash-cat-rescore-seed3568399740835207276.json), [H](MutOracleC2/v2/bash-cat-rescore-seed6840692661700775995.json) | K/K/K |

**New defective-control maximum: 118/120**, whitespace trimming, on all three seeds; including the disclosed feasibility reference, the maximum is 120/120. No mutant survives (18 seeded kills, zero inconclusive). v2's fixed subtype counts close the observed v1 omission: every run exposes two spaced pins, three uppercase pins and three prefixed pins. The highest score is still close to 120 because a whitespace-only defect affects only two fixtures, but it consistently fails the frozen 120/120 threshold.

[v2 kill matrix](MutOracleC2/v2/kill-matrix.json) records every score, expected baseline/restored receipt, miss and full gate hash. [v2 restoration evidence](MutOracleC2/v2/restoration.json) records all v1 artifact/receipt hashes unchanged, identical frozen gate bytes, stable per-run hashes, all 24 verified counter hashes, and three post-mutant oracle passes. Scratch bytes remain exactly restored at SHA-256 `96d63bcd3fb4f832e518730f52b2519fb1242c8bf7bb57a2e90f44d5e1cd2656`. Each new receipt has its actual stdout/stderr and bounded command in the neighboring `.execution.json`; bounds/process-group cleanup match v1. No network, candidate runs, source edits, git/jj writes or tool installations/updates.

design holds for the assigned v2 mutation probes: oracle 120/120 on three fresh seeds; all six defective controls below 120/120 on every seed.
