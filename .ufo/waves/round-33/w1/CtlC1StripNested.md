# CtlC1StripNested — round 33 wave 1 pre-data controls

## Scope and verdict

Axes: **operability**, detector discrimination, and exact restoration/isolation. Only operability is the frozen scored axis. This seat scored the three assigned strip-then-flat CONTROL gates, never a candidate implementation, and did not change the counter or production files.

| Control | Fresh seeds | Counter output on each seed | Control-screen verdict |
|---|---|---|---|
| a — iterative innermost object/array regex deletion | 93331001, 93331002 | `TOPLEVEL_FIELD_MATCH=130/144` | **MISSES** |
| b — one non-greedy member/container deletion pass | 93332001, 93332002 | `TOPLEVEL_FIELD_MATCH=129/144` | **MISSES** |
| c — regex-token bracket-stack deletion, not string-aware | 93333001, 93333002 | `TOPLEVEL_FIELD_MATCH=128/144` | **MISSES** |

None reached 144/144. Every mutated receipt has `predicate_holds=false`, `gate_rc=1`, and `gate_timed_out=false`; every counter invocation exited **1**, including all pristine and restored runs. This is not a killed-mutant claim: the pristine detector already fails at 60/144, so the paired mutation-testing verdict is **INCONCLUSIVE** for each control. The separate requested control-screen verdict is MISSES for all three.

Frozen expected detector: 144/144 and exit 0, matching the top-level id/verdict and exact line/revision-finding sets (`corpus/evidence/round33/claims.md:29-55`; counter docstring `:24-41`, matching implementation `:369-394`). Read claims.md first, then the counter docstring. No contract change or counter tuning followed these results.

## Mutants and hashes

All three started as exact copies of `tools/research-gate.sh`. The only additions were a `json_strip_nested` helper and one call after the existing outer-object check, immediately before the existing flat reads. `json_str`, `json_has_key`, duplicate handling, and downstream verification were otherwise unchanged.

- **a:** save the outside record braces; repeatedly apply `re.sub(r'\{[^{}]*\}', '', body)` and `re.sub(r'\[[^\[\]]*\]', '', body)` until unchanged; restore the outside braces. Archived `CtlC1StripNested/control-a.sh:1109-1123`, call `:1464`.
- **b:** one `re.sub(r'"[^"]*": *[{[].*?[}\]]', '', line)` pass. No iteration, structural parser, or string handling. Archived `CtlC1StripNested/control-b.sh:1109-1116`, call `:1457`.
- **c:** save the outside record braces; find the first remaining `{` or `[` using regex; scan regex-matched bracket characters with a matching-type stack, deleting the opener through the character that empties the stack; repeat. If no matching close is found, leave the remaining text unchanged. Quotes/escapes never affect the scan. Archived `CtlC1StripNested/control-c.sh:1109-1134`, call `:1475`.

Paths beginning `CtlC1StripNested/` in this report are relative to `.ufo/waves/round-33/w1/`.

| Bytes | SHA-256 | Archived gate size |
|---|---|---:|
| pristine base, and every restored scratch gate | `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0` | base 336677 bytes |
| a | `d673f65c833762b5d4d536139d15d739688bcba265cb764959551d7ed34c399e` | 337020 bytes |
| b | `fc5319a24eb1aeb61012606986a6d54a6fda4a9e730a55aab5da009cde67329f` | 336858 bytes |
| c | `4bf7bd35a1545d9ee64bd7fb1f89f97d8d3b68dc5a2349dcc9e4c26e8f8286d0` | 337383 bytes |
| frozen counter, before and after | `ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229` | 19037 bytes |

`timeout 20s sha256sum` on all three mutated scratch gates and subsequently on all three archived gates returned the respective a/b/c hashes above (exit 0). Each archived gate is under 1 MiB. The six mutated receipts independently carry these same gate hashes and the frozen counter hash.

## Actual per-class output

For a, b, and c, **both listed seeds produced the identical column shown**. The pristine/restored column was identical on all six seeds in each phase. These are the class lines printed by the counter, not inferred test coverage.

| Printed class | Pristine / restored | a (both seeds) | b (both seeds) | c (both seeds) |
|---|---:|---:|---:|---:|
| `N1_nested_line_decoy` | 6/12 | 12/12 | 12/12 | 12/12 |
| `N2_nested_line_only` | 0/12 | 12/12 | 12/12 | 12/12 |
| `N3_top_line_wrong_nested_right` | 6/12 | 12/12 | 12/12 | 12/12 |
| `N4_nested_sha_decoy` | 6/12 | 12/12 | 12/12 | 12/12 |
| `N5_nested_sha_only` | 0/12 | 12/12 | 12/12 | 12/12 |
| `N6_top_sha_stale_nested_right` | 6/12 | 12/12 | 12/12 | 12/12 |
| `N7_nested_source_decoy_sup` | 3/6 | 6/6 | 6/6 | 6/6 |
| `N8_nested_source_decoy_uns` | 3/6 | 6/6 | 6/6 | 6/6 |
| `N9_nested_id_decoy` | 3/6 | 6/6 | 6/6 | 6/6 |
| `N10_nested_span_decoy` | 3/6 | 6/6 | 6/6 | 6/6 |
| `N11_nested_marker_expect_decoy` | 0/6 | 6/6 | 6/6 | 6/6 |
| `D1_duplicate_top_level` | 0/12 | 0/12 | 0/12 | 0/12 |
| `S1_flat_confusers` | 12/12 | 12/12 | 12/12 | 12/12 |
| `S2_nested_confusers` | 0/6 | 4/6 | 3/6 | 2/6 |
| `F1_flat_plain` | 12/12 | 12/12 | 12/12 | 12/12 |
| `TOPLEVEL_FIELD_MATCH` | **60/144** | **130/144** | **129/144** | **128/144** |

All three controls pass all ordinary nested classes N1–N11, but fail all 12 duplicate-top-level records and respectively 2, 3, and 4 nested-string-confuser records. Even excluding duplicate policy, the nested-string class distinguishes these three string-unaware shortcuts. This is a bounded observation about the tested controls, not proof against every regex shortcut.

First-seed S2 misses recorded in receipts (each truth `supported`, observed `mislocated`):

- a: `c423699bfe3`, `c242db6e727`. Kept fixture `fixture-a-93331001/claims.jsonl:96,133` contains closing-bracket/brace text in strings before a nested wrong `line`.
- b: `c55297afb01`, `cec0bc53290`, `ceb3079c8c3`. Fixture `fixture-b-93332001/claims.jsonl:22,48,112` contains quoted closing-brace text or JSON-looking string content before a nested wrong `line`.
- c: `c07791062cd`, `c03b938c51e`, `cda257a35ef`, `c661bbc7c5e`. Fixture `fixture-c-93333001/claims.jsonl:55,98,133,135` contains closing-brace or unmatched-opening text inside strings before a nested wrong `line`.

Fixture paths here are under `/fast/scratch/hyaku/chousa-r33/w1/CtlC1StripNested/`. [INFERENCE] The deletions treat those literal string brackets as structural delimiters, retaining the earlier nested `line` for the unchanged flat reader. The observed ids/verdicts and original fixture rows are directly recorded; no additional probe or altered fixture was run.

## Commands, bounds, and receipts

Working directory for every score: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

For readability only, the following quoted command uses these substitutions for the absolute paths used in the actual commands:

```sh
L=/home/vgpnk/Projects/shokunin/chousa-shokunin
S=/fast/scratch/hyaku/chousa-r33/w1/CtlC1StripNested
A=$L/.ufo/waves/round-33/w1/CtlC1StripNested

timeout 180s prlimit --as=1073741824 --nproc=2000 env C1_TMP="$S" C2_TMP="$S" TMPDIR="$S" python3 "$L/corpus/evidence/round33/c1-count.py" --gate "$S/control-$control.sh" --seed "$seed" --receipt "$A/$phase-$control-$seed.json"
```

The complete invocation matrix is below. Each row ran once in each of the three phases, in order **pristine → control → restored**, for 18 detector invocations total; all returned exit **1**. In the control phase only, the first seed per control additionally used `--keep "$S/fixture-$control-$seed"`; no other options differed.

| control | seed | pristine receipt | control receipt | restored receipt |
|---|---:|---|---|---|
| a | 93331001 | `pristine-a-93331001.json` | `control-a-93331001.json` | `restored-a-93331001.json` |
| a | 93331002 | `pristine-a-93331002.json` | `control-a-93331002.json` | `restored-a-93331002.json` |
| b | 93332001 | `pristine-b-93332001.json` | `control-b-93332001.json` | `restored-b-93332001.json` |
| b | 93332002 | `pristine-b-93332002.json` | `control-b-93332002.json` | `restored-b-93332002.json` |
| c | 93333001 | `pristine-c-93333001.json` | `control-c-93333001.json` | `restored-c-93333001.json` |
| c | 93333002 | `pristine-c-93333002.json` | `control-c-93333002.json` | `restored-c-93333002.json` |

Every receipt in this table is under `$A/`. They contain the count, all class results, misses, seed, and gate/counter hashes. Gate copies preserved at `$A/control-{a,b,c}.sh` are the **mutated** bytes. Receipt gate paths point to the original scratch locations, which are now **restored**; reproduce mutated runs using the archived copies, not the restored scratch files.

Other executed commands (same substitutions; every command exited 0):

```sh
timeout 20s df -h /fast
timeout 20s mkdir -p "$S" "$A"
# For each control a, b, c, before the pristine scores:
timeout 20s cp "$L/tools/research-gate.sh" "$S/control-$control.sh"
# After mutation, before restoration, for each control:
timeout 20s cp "$S/control-$control.sh" "$A/control-$control.sh"
# After all six mutated scores, for each control:
timeout 20s cp "$L/tools/research-gate.sh" "$S/control-$control.sh"
# Hash measurements used the explicit paths represented here:
timeout 20s sha256sum "$L/tools/research-gate.sh" "$L/corpus/evidence/round33/c1-count.py"
timeout 20s sha256sum "$S/control-a.sh" "$S/control-b.sh" "$S/control-c.sh"
timeout 20s sha256sum "$A/control-a.sh" "$A/control-b.sh" "$A/control-c.sh"
timeout 20s sha256sum "$S/control-a.sh" "$S/control-b.sh" "$S/control-c.sh" "$L/tools/research-gate.sh" "$L/corpus/evidence/round33/c1-count.py"
timeout 20s wc -c "$L/tools/research-gate.sh" "$L/corpus/evidence/round33/c1-count.py"
timeout 20s wc -c "$A/control-a.sh" "$A/control-b.sh" "$A/control-c.sh"
```

`df` reported 198G available on /fast before copying. No heavy/unbounded writes were used: the frozen counter generates 144 records; only three first-seed fixtures were retained. Counter commands had a 180-second deadline, 1 GiB address-space limit, and 2000-process limit. No invocation timed out. No background jobs, process signals, subagents, network access, tool installations, git/jj writes, or unrelated tests were used.

## Restoration evidence and limits

After restoring with the three copy commands, `sha256sum` returned `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0` for **each** scratch gate and the lane production gate. The counter still returned its frozen `ab6b2ae2…` hash. The restored bytes then scored **60/144 on all six paired seeds**, exactly the pristine per-class output. Preserved mutant artifacts match the mutated receipt hashes rather than the restored hashes.

The expected 144/144 detector did not let any assigned shortcut through. No candidate, no-harm battery, source-fetching claim, or round-32 repair was evaluated by this seat. No permanent feature/fix was made; this is solely the assigned isolated mutation/control probe.
