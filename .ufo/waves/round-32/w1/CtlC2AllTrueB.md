# CtlC2AllTrueB — C2 all-true controls

## Axes and result

Axes: **operability** (bounded successful counter execution and replayable provenance) and **coverage** (correct discrimination of resolvable U hops from the exempt negative classes).

All three controls **MISSES** the frozen 120/120 target on both fresh seeds. No control MEETS-TARGET; there is no all-true counter escape in these six runs. These are deliberately invalid CONTROL gates, not C2 candidates or feasibility oracles. No candidate implementation was scored.

| Run | Control | Fresh seed | Counter output | Counter exit | Verdict | Receipt under `.ufo/waves/round-32/w1/CtlC2AllTrueB/` |
|---|---|---:|---|---:|---|---|
| A1 | U + parseable citation | 67593827045123011 | EXEMPT_AUDIT_MATCH=66/120 | 1 | MISSES | `a-s67593827045123011.json` |
| A2 | U + parseable citation | 67593827045123029 | EXEMPT_AUDIT_MATCH=66/120 | 1 | MISSES | `a-s67593827045123029.json` |
| B1 | Every exempt status + parseable citation | 67593827045123107 | EXEMPT_AUDIT_MATCH=54/120 | 1 | MISSES | `b-s67593827045123107.json` |
| B2 | Every exempt status + parseable citation | 67593827045123119 | EXEMPT_AUDIT_MATCH=54/120 | 1 | MISSES | `b-s67593827045123119.json` |
| C1 | U + non-empty `to` cell | 67593827045123203 | EXEMPT_AUDIT_MATCH=60/120 | 1 | MISSES | `c-s67593827045123203.json` |
| C2 | U + non-empty `to` cell | 67593827045123221 | EXEMPT_AUDIT_MATCH=60/120 | 1 | MISSES | `c-s67593827045123221.json` |

For each receipt, lines 3–14 bind the counter hash, control hash, seed, gate exit 1, no timeout, count, and `predicate_holds=false`; lines 15–30 contain every per-class result. C1/C2 in this table are run labels for control (c), not the manifest-lock claim or a candidate build.

## Frozen inputs and control construction

Opened `corpus/evidence/round32/claims.md` first, then both counter docstrings. Relevant contract: `claims.md:60-70`; frozen target: `claims.md:77-81`. Also opened the round-31 repair exclusions at `corpus/lessons/round-31-verifier-spotcheck.md:201-234`; none was added to these controls or counters. Read `skill://godspeed` and `/home/vgpnk/.omp/agent/RULES.md`.

Executed, exit 0:

```sh
timeout 30s df -h /fast
# /dev/nvme1n1p2: 804G total, 568G used, 236G available, 71%
timeout 30s sha256sum tools/research-gate.sh corpus/evidence/round32/c1-count.py corpus/evidence/round32/c2-count.py
timeout 30s git show 4111607c857bc29ff31883bc095ae00afb527e50:corpus/evidence/round32/c2-count.py | timeout 30s sha256sum
```

Observed hashes:

- Base gate: `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`, exactly the frozen base hash at `claims.md:3-4`.
- C1 counter, read only and never run: `9e787e80b215f6522335c639d5e1b2e60d0a5812b83a9760daf8be9f78415885`.
- C2 counter: `b6626b2cb81b2aeaf66a8ff11a06c030612bf4e264dc128f290021c4aa71f54c`, also the hash printed by the read-only `git show` of the frozen commit. All six receipts carry this hash.

Created only the assigned scratch/artifact directories and copied the base gate, using these commands (all exit 0):

```sh
timeout 30s mkdir -p /fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2AllTrueB
timeout 30s cp tools/research-gate.sh /fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/control-a-u-citation.sh && timeout 30s cp tools/research-gate.sh /fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/control-b-all-citation.sh && timeout 30s cp tools/research-gate.sh /fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/control-c-u-to.sh
```

Only base lines 1881–1882 (inside the exempt-status arm) were replaced in each scratch copy. All replacement branches emit exactly one `CHAIN` line per hop. A flagged hop gets one `emit_finding CHAIN_EXEMPT_RESOLVABLE warn chain "hop=$hop status=$st control=all-true-no-read"`, `observed=resolvable`, `anchor=-`, `at=-`, `verdict=mismatch`, and one mismatch increment. Otherwise the original exemption behavior remains. No exempt branch calls `claim_source_path`, reads a cited source, or checks an anchor. The resolved branch is unchanged.

- **(a)** `control-a-u-citation.sh:1881-1890`: normalize/display `to`; flag only when status is neither `rejected` nor `not-applicable` and `chain_citation "$hrow"` succeeds. Here “any citation” means syntactically parseable citation, not merely a source cell: `chain_citation` requires source and anchor but does not read the source (`tools/research-gate.sh:1646-1686`).
- **(b)** `control-b-all-citation.sh:1881-1890`: same, without the U-only status guard; thus it also flags `rejected`/`not-applicable` citations.
- **(c)** `control-c-u-to.sh:1881-1890`: retains the U-only guard but replaces citation parsing with `[[ -n $to ]]` on the `chain_cell` value. This intentionally flags rows with a source cell but no anchor. `rejected`/`not-applicable` remain exempt.

Executed, exit 0:

```sh
timeout 30s sha256sum /fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/control-a-u-citation.sh /fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/control-b-all-citation.sh /fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/control-c-u-to.sh
```

| Scratch gate | SHA-256 | Size (bytes) |
|---|---|---:|
| `/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/control-a-u-citation.sh` | `2c45d74e4542fb1de481265a4a1e3265e27f17f55752566cf3fe29dc2ef631fa` | 307040 |
| `/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/control-b-all-citation.sh` | `36e2326f8e7291272169df2861a576776a61285c6871f03e9e254f96ea62ecc8` | 306990 |
| `/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/control-c-u-to.sh` | `43c0ef8833e27ec02f2c04394f6c443a85e7e42fa5b67a8f98fc7734a5ba72e9` | 307024 |

## Commands and complete per-trial output

All six commands ran concurrently as foreground calls, from `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Each returned **exit 1**, not a harness error; all gate runs returned 1 without timeout. Exact command lines:

```sh
timeout --kill-after=5s 720s prlimit --as=1073741824 --nproc=2000 --fsize=1048576 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/control-a-u-citation.sh --seed 67593827045123011 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2AllTrueB/a-s67593827045123011.json
timeout --kill-after=5s 720s prlimit --as=1073741824 --nproc=2000 --fsize=1048576 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/control-a-u-citation.sh --seed 67593827045123029 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2AllTrueB/a-s67593827045123029.json
timeout --kill-after=5s 720s prlimit --as=1073741824 --nproc=2000 --fsize=1048576 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/control-b-all-citation.sh --seed 67593827045123107 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2AllTrueB/b-s67593827045123107.json
timeout --kill-after=5s 720s prlimit --as=1073741824 --nproc=2000 --fsize=1048576 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/control-b-all-citation.sh --seed 67593827045123119 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2AllTrueB/b-s67593827045123119.json
timeout --kill-after=5s 720s prlimit --as=1073741824 --nproc=2000 --fsize=1048576 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/control-c-u-to.sh --seed 67593827045123203 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2AllTrueB/c-s67593827045123203.json
timeout --kill-after=5s 720s prlimit --as=1073741824 --nproc=2000 --fsize=1048576 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/control-c-u-to.sh --seed 67593827045123221 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2AllTrueB/c-s67593827045123221.json
```

All per-class/per-trial lines are transcribed from observed stdout in `.ufo/waves/round-32/w1/CtlC2AllTrueB/counter-stdout.txt` (2655 bytes): A1 lines 1–16, A2 18–33, B1 35–50, B2 52–67, C1 69–84, C2 86–101. The counter emits one total plus fourteen class lines per run, not a separate hop-by-hop trial stream (`c2-count.py:303-306`); hop-level misses are in the six receipts. Full per-class values:

| Class | A1 | A2 | B1 | B2 | C1 | C2 |
|---|---|---|---|---|---|---|
| R1_U_fragment_quote | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| R2_U_path_anchor_cols | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| R3_U_declared_id | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| F1_resolved_verifiable | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| E1_U_anchor_absent | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 | 0/12 |
| E2_U_missing_file | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 |
| E3_U_external_url | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 |
| E4_U_no_citation | 6/6 | 6/6 | 6/6 | 6/6 | 0/6 | 0/6 |
| E5_J_resolvable | 12/12 | 12/12 | 0/12 | 0/12 | 12/12 | 12/12 |
| E6_U_undeclared_id | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 |
| E7_U_out_of_corpus | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 |
| E8_U_quote_glued | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 |
| E9_U_heading_as_plain_line | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 |
| E10_U_line_partial | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 | 0/6 |

## Counterexamples, affected axes, smallest safe correction

1. **Citation presence is not resolvability (a).** Receipt `a-s67593827045123011.json:32-37` records `h24d366a7`, class `E1_U_anchor_absent`, truth `exempt`, observed `resolvable`. All 54 negative U hops with parseable citations are false positives in both seeds. Source construction deliberately excludes the full anchor (`c2-count.py:131-135,193-195`); syntax alone also mislabels missing files, external URLs, undeclared ids, out-of-corpus paths, glued quotes, plain-line headings, and partial lines. Impact: **coverage**, with false provenance of successful resolution. The positive R1–R3 results alone would be premature saturation; the negative classes kill it.
2. **Judgment statuses are not unavailability (b).** In addition to those 54 false positives, all 12 `rejected`/`not-applicable` rows are mislabeled. Concrete receipt: `b-s67593827045123107.json:176-181`, `hf4c47858`, `E5_J_resolvable`, truth `exempt`, observed `resolvable`. The E5 generator alternates the two judgment statuses (`c2-count.py:55,203-205`). Impact: **coverage** and status identity semantics. This is an additional fixable defect, not a legitimate coverage/operability tradeoff under the frozen contract.
3. **A non-empty source cell is not a citation (c).** Beyond the 54 common false positives, all six E4 rows fail. Concrete receipt: `c-s67593827045123203.json:176-181`, `hffc0b9d6`, `E4_U_no_citation`, truth `exempt`, observed `resolvable`. E4 explicitly writes a present source file and `to` but omits both anchor fields (`c2-count.py:200-202`); the resolved parser requires an anchor (`research-gate.sh:1674-1675`). Impact: **coverage**. This also shows the fixed suite distinguishes parse-only all-true from to-cell-only all-true.

**Smallest safe correction:** do not infer resolvability from citation syntax or cell presence. For U only, apply the same source-id lookup, boundary/refusal rules, source read, and anchor matcher used by the existing resolved path (`research-gate.sh:1831-1878`); emit the one new finding only on an actual successful verification. Preserve every unsuccessful U hop as exempt and leave judgment statuses unread/exempt. No production correction was made or evaluated here. Canonical admission/judgment remains outside this review.

**Inspection-only counter limitation [INFERENCE; not exercised]:** the claimed “exactly one” finding is not occurrence-counted. `c2-count.py:269-274` accumulates finding ids in a set, and `:284-286` compares sets; duplicate occurrences of the same id would collapse. `FIND_RE` at `:79` also accepts arbitrary non-whitespace severity/surface values. These observations do not explain away any of the six misses and were not exploited or patched. The frozen counter and P2 remain unchanged; this review does not establish the counter's sufficiency for every C2 contract clause.

## Bounds and limits

- No network, installs, alternate runtime, subagents, background jobs, production edits, lane/fleet git or jj writes, or index changes. All counter invocations completed; no lingering job was started.
- Only the three scratch controls were scored. No C1 execution, candidate execution, selftest, no-harm battery, or source-read syscall audit was run. Operability here is limited to the six normal gate exits and receipts; manifest-lock operability is untested.
- Counter subprocesses were bounded by 720 seconds plus a 5-second kill grace, 1 GiB address space per process, 2000-process limit, and 1 MiB per-file limit. C1_TMP/C2_TMP/TMPDIR all named this seat's scratch directory.
- Artifact sizes were observed with the following command, exit 0; gates were 306990–307040 bytes, receipts 7288–8646 bytes, stdout transcript 2655 bytes, each below 1 MiB:

```sh
timeout 30s stat -c '%s %n' /fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/control-a-u-citation.sh /fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/control-b-all-citation.sh /fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/control-c-u-to.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2AllTrueB/*.json /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2AllTrueB/counter-stdout.txt
```

No tools were installed or updated.
