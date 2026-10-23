# CtlC2WeakReaderB — frozen v1 weak-reader controls

Axes: operability (bounded, reversible experiments); coverage (reject semantically weak exempt-hop readers).

## Result

Two deliberately wrong readers passed the v1 detector after isolating the gate lane roots: case-insensitive matching and horizontal-whitespace collapse each scored **120/120 twice (MEETS-TARGET)**. Grep-anywhere, boundary bypass, and file-only source resolution MISSED. These are controls, not candidate builds or landed-P2 claims.

All relative evidence filenames below are under `.ufo/waves/round-32/w1/CtlC2WeakReaderB/`. Complete command/output, receipt hashes, all 60 counter invocations and 8 witness invocations are in `probe-ledger.json` (SHA-256 `e6494eeadba809638a81d434d5c33e6b8fd2cf0e097e0f04f7615f1bcc18b106`).

## Detector and scope

`corpus/evidence/round32/claims.md:60-79` supplies the unchanged C2 contract and v1 120/120 target. `c2-count.py:281-294` scores observed labels and finding IDs per hop. All controls began as exact copies of the BASE gate; only the U audit arm was added, with a deliberately weak behavior. Rejected/not-applicable and resolved branches were retained. The boundary control additionally gates the canonicalization/root checks only during U reads.

| Control | Behavior-bearing mutation evidence |
|---|---|
| grep-anywhere | `grep-anywhere.patch:22`: `grep -Fq` against the source file, without heading/whole-line/token-edge semantics |
| skip-boundary | `skip-boundary.patch:8-23,44`: retain the raw path and bypass allowed-root membership only for the U call |
| case-insensitive | `case-insensitive.patch:23`: lowercase haystack and anchor before the existing kind-aware matcher |
| whitespace-collapse | `whitespace-collapse.patch:23-26`: squeeze horizontal whitespace in haystack and anchor, retaining existing kind semantics |
| file-only | `file-only.patch:13`: use CITE_TO as a file path, ignoring declared-id pointers |

Exact command template (every concrete invocation, environment, exit and output is in its `.txt` file):

```sh
C1_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2WeakReaderB C2_TMP=/fast/scratch/hyaku/chousa-r32/w1/CtlC2WeakReaderB TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC2WeakReaderB \
  timeout --kill-after=5s 660s prlimit --as=1073741824 --nproc=2000 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC2WeakReaderB/gates/grep-anywhere/tools/research-gate.sh --seed 1226555173 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2WeakReaderB/grep-anywhere-isolated-mutated-s1226555173.json
```

Cwd: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Maximum two awaited foreground probes concurrently; counter timeout 660 s, kill-after 5 s, address-space cap 1 GiB, process cap 2000. No network, installs, candidate scoring, counter edits, Git/JJ writes, builds or general test suites.

## Isolated-layout trials

Gate paths: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2WeakReaderB/gates/<control>/tools/research-gate.sh`. Their SELF-derived lane roots exclude the counter temp-fixture siblings. Each seed was run on pristine, mutated and exact-restored bytes.

| Control | Seed | Pristine | Mutated | Restored | Counter exit (mutated) | Verdict | Mutated receipt |
|---|---:|---:|---:|---:|---:|---|---|
| grep-anywhere | 1226555173 | 84/120 | 102/120 | 84/120 | 1 | MISSES | `grep-anywhere-isolated-mutated-s1226555173.json` |
| grep-anywhere | 4112867825 | 84/120 | 102/120 | 84/120 | 1 | MISSES | `grep-anywhere-isolated-mutated-s4112867825.json` |
| skip-boundary | 702683671 | 84/120 | 114/120 | 84/120 | 1 | MISSES | `skip-boundary-isolated-mutated-s702683671.json` |
| skip-boundary | 3815148080 | 84/120 | 114/120 | 84/120 | 1 | MISSES | `skip-boundary-isolated-mutated-s3815148080.json` |
| case-insensitive | 3908516132 | 84/120 | 120/120 | 84/120 | 0 | MEETS-TARGET | `case-insensitive-isolated-mutated-s3908516132.json` |
| case-insensitive | 1030166489 | 84/120 | 120/120 | 84/120 | 0 | MEETS-TARGET | `case-insensitive-isolated-mutated-s1030166489.json` |
| whitespace-collapse | 2971276398 | 84/120 | 120/120 | 84/120 | 0 | MEETS-TARGET | `whitespace-collapse-isolated-mutated-s2971276398.json` |
| whitespace-collapse | 1506610368 | 84/120 | 120/120 | 84/120 | 0 | MEETS-TARGET | `whitespace-collapse-isolated-mutated-s1506610368.json` |
| file-only | 535510181 | 84/120 | 108/120 | 84/120 | 1 | MISSES | `file-only-isolated-mutated-s535510181.json` |
| file-only | 1594822793 | 84/120 | 108/120 | 84/120 | 1 | MISSES | `file-only-isolated-mutated-s1594822793.json` |

Per-trial/per-class output, copied verbatim from the detector (corresponding `.txt` files include exact commands and exit codes):

### grep-anywhere, seed 1226555173, exit 1

```text
EXEMPT_AUDIT_MATCH=102/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 12/12
  E2_U_missing_file 6/6
  E3_U_external_url 6/6
  E4_U_no_citation 6/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 6/6
  E7_U_out_of_corpus 6/6
  E8_U_quote_glued 0/6
  E9_U_heading_as_plain_line 0/6
  E10_U_line_partial 0/6
```

### grep-anywhere, seed 4112867825, exit 1

```text
EXEMPT_AUDIT_MATCH=102/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 12/12
  E2_U_missing_file 6/6
  E3_U_external_url 6/6
  E4_U_no_citation 6/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 6/6
  E7_U_out_of_corpus 6/6
  E8_U_quote_glued 0/6
  E9_U_heading_as_plain_line 0/6
  E10_U_line_partial 0/6
```

### skip-boundary, seed 702683671, exit 1

```text
EXEMPT_AUDIT_MATCH=114/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 12/12
  E2_U_missing_file 6/6
  E3_U_external_url 6/6
  E4_U_no_citation 6/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 6/6
  E7_U_out_of_corpus 0/6
  E8_U_quote_glued 6/6
  E9_U_heading_as_plain_line 6/6
  E10_U_line_partial 6/6
```

### skip-boundary, seed 3815148080, exit 1

```text
EXEMPT_AUDIT_MATCH=114/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 12/12
  E2_U_missing_file 6/6
  E3_U_external_url 6/6
  E4_U_no_citation 6/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 6/6
  E7_U_out_of_corpus 0/6
  E8_U_quote_glued 6/6
  E9_U_heading_as_plain_line 6/6
  E10_U_line_partial 6/6
```

### case-insensitive, seed 3908516132, exit 0

```text
EXEMPT_AUDIT_MATCH=120/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 12/12
  E2_U_missing_file 6/6
  E3_U_external_url 6/6
  E4_U_no_citation 6/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 6/6
  E7_U_out_of_corpus 6/6
  E8_U_quote_glued 6/6
  E9_U_heading_as_plain_line 6/6
  E10_U_line_partial 6/6
```

### case-insensitive, seed 1030166489, exit 0

```text
EXEMPT_AUDIT_MATCH=120/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 12/12
  E2_U_missing_file 6/6
  E3_U_external_url 6/6
  E4_U_no_citation 6/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 6/6
  E7_U_out_of_corpus 6/6
  E8_U_quote_glued 6/6
  E9_U_heading_as_plain_line 6/6
  E10_U_line_partial 6/6
```

### whitespace-collapse, seed 2971276398, exit 0

```text
EXEMPT_AUDIT_MATCH=120/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 12/12
  E2_U_missing_file 6/6
  E3_U_external_url 6/6
  E4_U_no_citation 6/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 6/6
  E7_U_out_of_corpus 6/6
  E8_U_quote_glued 6/6
  E9_U_heading_as_plain_line 6/6
  E10_U_line_partial 6/6
```

### whitespace-collapse, seed 1506610368, exit 0

```text
EXEMPT_AUDIT_MATCH=120/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 12/12
  E2_U_missing_file 6/6
  E3_U_external_url 6/6
  E4_U_no_citation 6/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 6/6
  E7_U_out_of_corpus 6/6
  E8_U_quote_glued 6/6
  E9_U_heading_as_plain_line 6/6
  E10_U_line_partial 6/6
```

### file-only, seed 535510181, exit 1

```text
EXEMPT_AUDIT_MATCH=108/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 0/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 12/12
  E2_U_missing_file 6/6
  E3_U_external_url 6/6
  E4_U_no_citation 6/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 6/6
  E7_U_out_of_corpus 6/6
  E8_U_quote_glued 6/6
  E9_U_heading_as_plain_line 6/6
  E10_U_line_partial 6/6
```

### file-only, seed 1594822793, exit 1

```text
EXEMPT_AUDIT_MATCH=108/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 0/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 12/12
  E2_U_missing_file 6/6
  E3_U_external_url 6/6
  E4_U_no_citation 6/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 6/6
  E7_U_out_of_corpus 6/6
  E8_U_quote_glued 6/6
  E9_U_heading_as_plain_line 6/6
  E10_U_line_partial 6/6
```

## Why the two wrong readers passed

`c2-count.py:77,95-103` generates anchor words only from lowercase syllables and joins them with one ASCII space. `:120-145` inserts the same literal anchor in positives; its negatives alter words, glue a prefix, remove heading syntax, or add words to the line. There is no case-only or horizontal-whitespace-only negative. Lowercasing or squeezing whitespace therefore leaves the generated distinctions intact while weakening real resolved-citation semantics.

Two paired witnesses demonstrate the actual defect, not just an inferred implementation shortcut:

- Case source contains only `EXACT CASE ANCHOR`, while both rows cite `exact case anchor`. `case-insensitive-isolated-mutated-witness.txt:7-10` shows the U row `observed=resolvable` plus its finding, but its identical resolved citation is `observed=anchor-missing`.
- Whitespace source is `exact  spacing\tanchor` (two spaces plus a literal tab), while the rows cite `exact spacing anchor`. `whitespace-collapse-isolated-mutated-witness.txt:7-10` shows the same disagreement.
- `case-insensitive-pristine-witness.txt`, `whitespace-collapse-pristine-witness.txt` and both `*-isolated-restored-witness.txt` outputs show U=exempt and resolved=anchor-missing on base bytes. Every witness returned gate exit 1, as its resolved row drifts.

Some isolated witness commands emitted `fork: retry: Resource temporarily unavailable` under the shared-host process cap; their complete stderr is retained in the witness logs and ledger. The quoted CHAIN/FINDING output and exit codes were actually observed; these runs are not described as warning-free.

## Initial flat-layout results (retained, not silently discarded)

Initial gates were at `/fast/scratch/hyaku/chousa-r32/w1/CtlC2WeakReaderB/<control>-gate.sh`, with C2_TMP/TMPDIR pointing at `/fast/scratch/hyaku/chousa-r32/w1/CtlC2WeakReaderB`. Gate `tools/research-gate.sh:290-291` derives LANE_ROOT from the gate directory parent; `:1213-1222` admits sources inside either root. Consequently, the counter E7 `../outside` fixture (`c2-count.py:208-210`) lay inside that synthetic lane root. E7 was incorrectly truth-labelled exempt for that invocation geometry; these scores are not used as reader-discrimination results. No counter was modified.

| Control | Two initial seeds | Pristine → mutated → restored, both seeds |
|---|---|---|
| grep-anywhere | 1656605796, 3386496079 | 84/120 → 96/120 → 84/120 (all counter exits 1) |
| skip-boundary | 3267812547, 911795097 | 84/120 → 114/120 → 84/120 (all counter exits 1) |
| case-insensitive | 1855202720, 3016985094 | 84/120 → 114/120 → 84/120 (all counter exits 1) |
| whitespace-collapse | 3764733144, 3466617587 | 84/120 → 114/120 → 84/120 (all counter exits 1) |
| file-only | 1978999705, 2648768445 | 84/120 → 102/120 → 84/120 (all counter exits 1) |

Every initial receipt and raw class line remains in `<control>-{pristine,mutated,restored}-s<seed>.{json,txt}` and the ledger. The isolated runs used fresh seeds and **identical mutant SHA-256 bytes**. The four otherwise-boundary-respecting controls recovered E7 from 0/6 to 6/6; boundary bypass remained 0/6. No claim that full landed P2 holds is made: the initial lower counts remain disclosed.

## Hashes, restoration and mutation verdict

Pristine SHA-256 for every control: `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`.
All flat and isolated gates were restored byte-for-byte to that hash in `finally`, then the same seeded counter was run again. All 20 restored invocations returned counter exit 1, `EXEMPT_AUDIT_MATCH=84/120`, R1/R2/R3 each 0/12, every other class full.

| Control | Mutated SHA-256 (same in both layouts) |
|---|---|
| grep-anywhere | `7be8f1d2acb8fae1b6e52baae6a22e8c449cb3d88809c476d70b5f20d4ad19f8` |
| skip-boundary | `a4552ca0157098fda889f339e2373a6150aa060fc3a284b7e2e6840dfed2e081` |
| case-insensitive | `a0eab06c1546516a21ce54003271742d1b20b742bb319f06939c3a35b4700d06` |
| whitespace-collapse | `32e03f4f5ccae47fa613efad47b75ee167b4aef03bc61e807213428dda8e8c5d` |
| file-only | `6bed45fb8c4f4735eea3c2db7eb67a59788dd7aabdf5a338851115e9e73629b4` |

Final production gate SHA-256 remained `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`; v1 counter SHA-256 remained `b6626b2cb81b2aeaf66a8ff11a06c030612bf4e264dc128f290021c4aa71f54c`. The final bounded `sha256sum` covered production gate, frozen v1 counter, base copy and all ten restored scratch gates; output showed every gate equal to BASE. The ledger records separate before/mutated/after hashes and all receipt/log hashes.

**Strict mutation-test kill attribution: INCONCLUSIVE, not killed.** The required pristine baseline itself fails P2 at 84/120, so a failing weak control is not presented as a killed mutant. Separately, the two observed 120/120 control passes are detector-survival/coverage findings. No contract or counter was changed by this seat.

All probe subprocesses were awaited/reaped; no background jobs or services were started. All 133 evidence artifacts preceding the ledger were individually below 1 MiB (largest 5,220 bytes); the ledger is 117,813 bytes. Code experiments/fixtures are confined to the assigned scratch directory. This report is written once; later v2 rescoring, requested separately by L1, belongs in its own supplement.
