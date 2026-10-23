# CtlC2JunkB — round 32 attempt 2, wave 1

## Axes and result

- **Coverage (C2):** ten junk/generator-key/row-cell controls, two fresh fixture seeds each: **all MISSES**. No control met 120/120.
- **Operability:** no C1 measurement or candidate score. Two additional counter-launch failures exposed a harness-error exit-code defect, described below.
- Strongest readless shortcut: **generator-union = 108/120 twice**. This is a partial fixture correlation, not a passing counterexample or an admission judgment.

## Scope, provenance, and commands

Read `corpus/evidence/round32/claims.md` first, then both counter docstrings; inspected the C2 generator/scorer and the base gate's chain-cell/citation helpers and verify_chain arm. All gate changes are scratch controls, only replacing the base exempt-arm body (`tools/research-gate.sh:1881-1882`). Resolved behavior and rejected/not-applicable handling are retained. No candidate build was opened, edited, or scored; neither counter was edited. No lane production file, Git index, or jj state was changed. No installs, network accesses, subagents, or background jobs.

Scratch root: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2JunkB`.
Artifact root (lane-relative): `.ufo/waves/round-32/w1/CtlC2JunkB/`.

Observed preparation commands:

```text
timeout 15s df -h /fast
# exit 0; /fast: 804G total, 568G used, 236G available (71%).
timeout 15s cp /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /fast/scratch/hyaku/chousa-r32/w1/CtlC2JunkB/base-gate.sh
# exit 0; subsequent per-control copies also exit 0.
timeout 15s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c1-count.py /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py
# exit 0; gate=0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258
# C1 counter=9e787e80b215f6522335c639d5e1b2e60d0a5812b83a9760daf8be9f78415885
# C2 counter=b6626b2cb81b2aeaf66a8ff11a06c030612bf4e264dc128f290021c4aa71f54c
timeout 15s git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 4111607c857bc29ff31883bc095ae00afb527e50:corpus/evidence/round32/c2-count.py | timeout 15s sha256sum
# exit 0; same C2 counter hash.
```

Every scored command, cwd, exit code, seed, exact stdout/per-class line, and receipt path is retained in `CtlC2JunkB/counter-commands-output.txt:1-419` (relative to this report's directory). SHA-256: `29b9f77b238bbc132954515897967dfd76c2d06dfffe38ebceaaec1cfc7fd2ee`; 22,859 bytes. Commands use a 700-second timeout with a 5-second kill grace, 1-GiB address-space cap, and process cap 2000 (16384 for successful binary-random runs). All three temp environment variables C1_TMP/C2_TMP/TMPDIR point to the scratch root. Up to six scoring commands ran concurrently; all were awaited and exited.

All 20 scored commands exited **1**; all corresponding gate receipts report gate_rc=1, gate_timed_out=false, predicate_holds=false, and the frozen C2 counter hash above (`CtlC2JunkB/*-a.json` and `*-b.json`, fields at lines 3,9-14). The counter correctly treats these as misses.

## Control summary

Each gate path is `<scratch>/<control>-gate.sh`. Each receipt path is `<artifact>/<control>-a.json` or `-b.json`. The detailed sections below include both seeds and all per-class/per-trial lines.

| Control | Trial a | Trial b | Verdict |
|---|---:|---:|---|
| random-labels | 54/120 | 42/120 | MISSES |
| hop-id-shape | 60/120 | 60/120 | MISSES |
| filename-shape | 66/120 | 66/120 | MISSES |
| declared-id-shape | 90/120 | 90/120 | MISSES |
| declared-id-member | 96/120 | 96/120 | MISSES |
| generator-union | 108/120 | 108/120 | MISSES |
| row-position | 79/120 | 67/120 | MISSES |
| notes-shape | 60/120 | 60/120 | MISSES |
| from-shape | 60/120 | 60/120 | MISSES |
| random-valid-labels | 72/120 | 72/120 | MISSES |

## Counterexample, evidence, and smallest safe correction

**Strongest attempted counterexample:** generator-union flags a U hop based only on its citation spelling or membership in Sources. It never opens U source contents. It obtains all 12 R1 and all 12 R3 positives plus every negative, but misses all 12 R2 positives on both seeds: `CtlC2JunkB/generator-union-a.json:15-29`, `generator-union-b.json:15-29`; original stdout at `counter-commands-output.txt:215-229,236-250`. Example missed hop `hfd42e276` is truth=resolvable, observed=exempt (`generator-union-a.json:32-36`). Its two totals are 108/120, so it does **not** defeat the frozen full-target predicate.

**Why the partial shortcut works:** `c2-count.py:174-184` writes `#quote:` fragment citations only for R1 and declared source-id citations for R3. Negative U declared-id rows are undeclared (`:206-207`), and the other negative U classes do not use fragment spelling (`:193-219`). Thus declared-id membership plus fragment format separates R1/R3 in this fixture without provenance verification. The counter's full threshold still rejects the shortcut because R2 remains at 0/12. The schema shapes are explicit at `:105-117,157-168`; the common generated notes/from cells therefore do not identify truth. Chain/source rows are shuffled at `:222-223`, defeating the tested first-36-row guess.

**Coverage impact:** a real implementation that used these shortcuts would confuse generator identity with source verification. Passing R1/R3 under this fixture alone cannot establish that those branches read/verify citations. This is a fixable fixture-orthogonality weakness, not an observed MEETS-TARGET control, and no overall claim verdict is made here.

**Smallest safe correction:** retain the frozen counter unchanged for this design. Real C2 work must derive outcomes from the same parsed citation, declared-id resolution, local-boundary checks, and anchor matcher as resolved rows—not names, notes, or row positions (`claims.md:60-70`; base `research-gate.sh:1831-1878`). For a separately versioned pre-data fixture design, add anchor-absent/missing-source negative twins using both the fragment spelling and declared ids, so neither spelling nor declaration membership carries a free truth label. Do not retrofit these changes into the frozen counter or reinterpret this round's receipts.

## Harness-error finding (not a score)

The first two attempts for the added binary-random control used process cap 2000 and seeds 4069702987433492165 / 4476120378144463570. Both exited 1 with `BlockingIOError: [Errno 11] Resource temporarily unavailable` at frozen `c2-count.py:263`; neither printed a count nor created a receipt. Full commands and tracebacks: `CtlC2JunkB/resource-errors.txt` (4,444 bytes; SHA-256 `b888490fda91d6eea08cc869c7c70b279abc97ab7485e32de549ee1ba449c398`). Fresh runs at cap 16384 produced the two scored 72/120 receipts below. [INFERENCE] The lower process cap interacted with concurrent fleet load; no global process-count diagnosis was performed.

This exposes a bounded reporting defect: the counter documents exit 2 for harness errors (`c2-count.py:36`) but catches only TimeoutExpired around subprocess.run (`:261-267`), allowing spawn OSError to escape as exit 1 with no score/receipt. The counter was not patched. Smallest future-version correction: classify a gate-launch OSError as a harness error (exit 2), not a predicate miss. The counter reviewer was notified with this evidence path.

## Detailed controls and exact per-class/per-trial stdout

### random-labels — MISSES

Choose U observed labels with Bash RANDOM from exempt/resolvable/verified/junk; emit the required finding only for resolvable. All flags apply only to U; rejected/not-applicable stay exempt.

Gate: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2JunkB/random-labels-gate.sh`; SHA-256 `a7011a17644cae50baa604f9c3ae947bab3bb7330c7fc7aeff8341d60ae14871`.

Trial a, seed `4972826197380239916`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/random-labels-a.json`.

```text
EXEMPT_AUDIT_MATCH=54/120
  R1_U_fragment_quote 5/12
  R2_U_path_anchor_cols 1/12
  R3_U_declared_id 3/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 1/12
  E2_U_missing_file 2/6
  E3_U_external_url 2/6
  E4_U_no_citation 2/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 3/6
  E7_U_out_of_corpus 2/6
  E8_U_quote_glued 3/6
  E9_U_heading_as_plain_line 4/6
  E10_U_line_partial 2/6
```

Trial b, seed `384696747690096890`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/random-labels-b.json`.

```text
EXEMPT_AUDIT_MATCH=42/120
  R1_U_fragment_quote 2/12
  R2_U_path_anchor_cols 3/12
  R3_U_declared_id 1/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 2/12
  E2_U_missing_file 3/6
  E3_U_external_url 2/6
  E4_U_no_citation 1/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 0/6
  E7_U_out_of_corpus 1/6
  E8_U_quote_glued 1/6
  E9_U_heading_as_plain_line 2/6
  E10_U_line_partial 0/6
```


### hop-id-shape — MISSES

Flag U iff hop matches ^h[0-9a-f]{8}$. All flags apply only to U; rejected/not-applicable stay exempt.

Gate: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2JunkB/hop-id-shape-gate.sh`; SHA-256 `a4a1dcee4899c5800275bcaee98f76e60fa14b2916a6318c0881e871df1beb22`.

Trial a, seed `2249306968446087722`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/hop-id-shape-a.json`.

```text
EXEMPT_AUDIT_MATCH=60/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 0/12
  E2_U_missing_file 0/6
  E3_U_external_url 0/6
  E4_U_no_citation 0/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 0/6
  E7_U_out_of_corpus 0/6
  E8_U_quote_glued 0/6
  E9_U_heading_as_plain_line 0/6
  E10_U_line_partial 0/6
```

Trial b, seed `261866074059815253`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/hop-id-shape-b.json`.

```text
EXEMPT_AUDIT_MATCH=60/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 0/12
  E2_U_missing_file 0/6
  E3_U_external_url 0/6
  E4_U_no_citation 0/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 0/6
  E7_U_out_of_corpus 0/6
  E8_U_quote_glued 0/6
  E9_U_heading_as_plain_line 0/6
  E10_U_line_partial 0/6
```


### filename-shape — MISSES

Flag U iff raw to matches ^f[0-9a-f]{10}\.md(#.*)?$; no existence/anchor read. All flags apply only to U; rejected/not-applicable stay exempt.

Gate: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2JunkB/filename-shape-gate.sh`; SHA-256 `bae7fd1ca83a7ac3826d7467843199475a4c951487bc35a82387b86c5156d900`.

Trial a, seed `1815058257206145757`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/filename-shape-a.json`.

```text
EXEMPT_AUDIT_MATCH=66/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 0/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 0/12
  E2_U_missing_file 0/6
  E3_U_external_url 6/6
  E4_U_no_citation 0/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 6/6
  E7_U_out_of_corpus 6/6
  E8_U_quote_glued 0/6
  E9_U_heading_as_plain_line 0/6
  E10_U_line_partial 0/6
```

Trial b, seed `5204535861689585628`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/filename-shape-b.json`.

```text
EXEMPT_AUDIT_MATCH=66/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 0/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 0/12
  E2_U_missing_file 0/6
  E3_U_external_url 6/6
  E4_U_no_citation 0/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 6/6
  E7_U_out_of_corpus 6/6
  E8_U_quote_glued 0/6
  E9_U_heading_as_plain_line 0/6
  E10_U_line_partial 0/6
```


### declared-id-shape — MISSES

Flag U iff to matches ^S[0-9a-f]{10}$, without checking declaration or bytes. All flags apply only to U; rejected/not-applicable stay exempt.

Gate: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2JunkB/declared-id-shape-gate.sh`; SHA-256 `0ec9610bc73b732e695ecd2e837464a8680c319630daac374b4b762fcb63bbf8`.

Trial a, seed `3897432351753434821`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/declared-id-shape-a.json`.

```text
EXEMPT_AUDIT_MATCH=90/120
  R1_U_fragment_quote 0/12
  R2_U_path_anchor_cols 0/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 12/12
  E2_U_missing_file 6/6
  E3_U_external_url 6/6
  E4_U_no_citation 6/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 0/6
  E7_U_out_of_corpus 6/6
  E8_U_quote_glued 6/6
  E9_U_heading_as_plain_line 6/6
  E10_U_line_partial 6/6
```

Trial b, seed `8054512970936801120`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/declared-id-shape-b.json`.

```text
EXEMPT_AUDIT_MATCH=90/120
  R1_U_fragment_quote 0/12
  R2_U_path_anchor_cols 0/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 12/12
  E2_U_missing_file 6/6
  E3_U_external_url 6/6
  E4_U_no_citation 6/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 0/6
  E7_U_out_of_corpus 6/6
  E8_U_quote_glued 6/6
  E9_U_heading_as_plain_line 6/6
  E10_U_line_partial 6/6
```


### declared-id-member — MISSES

Flag U iff to has the S+10-hex shape and occurs in the already-loaded Sources map; do not open its target. All flags apply only to U; rejected/not-applicable stay exempt.

Gate: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2JunkB/declared-id-member-gate.sh`; SHA-256 `2dccb4acb10f4583a273d6d7c85e4ebe22b699f1c70b0d32884d4c18ee9997da`.

Trial a, seed `6253936566426190680`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/declared-id-member-a.json`.

```text
EXEMPT_AUDIT_MATCH=96/120
  R1_U_fragment_quote 0/12
  R2_U_path_anchor_cols 0/12
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

Trial b, seed `1256753911267810600`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/declared-id-member-b.json`.

```text
EXEMPT_AUDIT_MATCH=96/120
  R1_U_fragment_quote 0/12
  R2_U_path_anchor_cols 0/12
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


### generator-union — MISSES

Flag U iff to has the f+10-hex.md#quote:... spelling OR is an S+10-hex declared source id; no U source read. All flags apply only to U; rejected/not-applicable stay exempt.

Gate: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2JunkB/generator-union-gate.sh`; SHA-256 `88852cc897b2eb142b7c1c8773b8437dbd05d39c20dac85bbdfdedbab708bd73`.

Trial a, seed `4327098604344159020`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/generator-union-a.json`.

```text
EXEMPT_AUDIT_MATCH=108/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 0/12
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

Trial b, seed `1235637545905057000`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/generator-union-b.json`.

```text
EXEMPT_AUDIT_MATCH=108/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 0/12
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


### row-position — MISSES

Flag U iff its shuffled Chain row number N_HOPS is at most 36. All flags apply only to U; rejected/not-applicable stay exempt.

Gate: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2JunkB/row-position-gate.sh`; SHA-256 `5a517c0d6e158b5a003b34d947a6965a6e947ea0418582799c3e370be9ebe170`.

Trial a, seed `3061493095783762256`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/row-position-a.json`.

```text
EXEMPT_AUDIT_MATCH=79/120
  R1_U_fragment_quote 5/12
  R2_U_path_anchor_cols 4/12
  R3_U_declared_id 5/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 10/12
  E2_U_missing_file 4/6
  E3_U_external_url 5/6
  E4_U_no_citation 3/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 5/6
  E7_U_out_of_corpus 4/6
  E8_U_quote_glued 3/6
  E9_U_heading_as_plain_line 5/6
  E10_U_line_partial 2/6
```

Trial b, seed `3812830316350342026`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/row-position-b.json`.

```text
EXEMPT_AUDIT_MATCH=67/120
  R1_U_fragment_quote 4/12
  R2_U_path_anchor_cols 1/12
  R3_U_declared_id 1/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 5/12
  E2_U_missing_file 5/6
  E3_U_external_url 5/6
  E4_U_no_citation 4/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 3/6
  E7_U_out_of_corpus 3/6
  E8_U_quote_glued 4/6
  E9_U_heading_as_plain_line 4/6
  E10_U_line_partial 4/6
```


### notes-shape — MISSES

Flag U iff notes are exactly three words, each 2-4 syllables from the generator SYL list. All flags apply only to U; rejected/not-applicable stay exempt.

Gate: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2JunkB/notes-shape-gate.sh`; SHA-256 `f22d023965d8e51acc0687b4ead010fd856d7498da491c591fe74c47531c96d9`.

Trial a, seed `5038245323916993564`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/notes-shape-a.json`.

```text
EXEMPT_AUDIT_MATCH=60/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 0/12
  E2_U_missing_file 0/6
  E3_U_external_url 0/6
  E4_U_no_citation 0/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 0/6
  E7_U_out_of_corpus 0/6
  E8_U_quote_glued 0/6
  E9_U_heading_as_plain_line 0/6
  E10_U_line_partial 0/6
```

Trial b, seed `7915050439798829957`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/notes-shape-b.json`.

```text
EXEMPT_AUDIT_MATCH=60/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 0/12
  E2_U_missing_file 0/6
  E3_U_external_url 0/6
  E4_U_no_citation 0/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 0/6
  E7_U_out_of_corpus 0/6
  E8_U_quote_glued 0/6
  E9_U_heading_as_plain_line 0/6
  E10_U_line_partial 0/6
```


### from-shape — MISSES

Flag U iff from matches ^A[0-9a-f]{10}:[1-9][0-9]?$. All flags apply only to U; rejected/not-applicable stay exempt.

Gate: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2JunkB/from-shape-gate.sh`; SHA-256 `6793d7398137a3c18f32f27c7d1133d0fb1198b105ef2b815f2bfbd9543a6af8`.

Trial a, seed `2230574085151978512`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/from-shape-a.json`.

```text
EXEMPT_AUDIT_MATCH=60/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 0/12
  E2_U_missing_file 0/6
  E3_U_external_url 0/6
  E4_U_no_citation 0/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 0/6
  E7_U_out_of_corpus 0/6
  E8_U_quote_glued 0/6
  E9_U_heading_as_plain_line 0/6
  E10_U_line_partial 0/6
```

Trial b, seed `104221434860716233`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/from-shape-b.json`.

```text
EXEMPT_AUDIT_MATCH=60/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 0/12
  E2_U_missing_file 0/6
  E3_U_external_url 0/6
  E4_U_no_citation 0/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 0/6
  E7_U_out_of_corpus 0/6
  E8_U_quote_glued 0/6
  E9_U_heading_as_plain_line 0/6
  E10_U_line_partial 0/6
```


### random-valid-labels — MISSES

Stronger random control: choose only exempt/resolvable for U, equiprobably via Bash RANDOM, with the required finding for resolvable. All flags apply only to U; rejected/not-applicable stay exempt.

Gate: `/fast/scratch/hyaku/chousa-r32/w1/CtlC2JunkB/random-valid-labels-gate.sh`; SHA-256 `34de75569d9e8bac02aa443c2f6071df2744a61456154774dfa91974f00a862f`.

Trial a, seed `40447539003400073`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/random-valid-labels-a.json`.

```text
EXEMPT_AUDIT_MATCH=72/120
  R1_U_fragment_quote 6/12
  R2_U_path_anchor_cols 5/12
  R3_U_declared_id 7/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 2/12
  E2_U_missing_file 2/6
  E3_U_external_url 3/6
  E4_U_no_citation 4/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 3/6
  E7_U_out_of_corpus 3/6
  E8_U_quote_glued 2/6
  E9_U_heading_as_plain_line 6/6
  E10_U_line_partial 5/6
```

Trial b, seed `4732573782758299253`, exit `1`; receipt `.ufo/waves/round-32/w1/CtlC2JunkB/random-valid-labels-b.json`.

```text
EXEMPT_AUDIT_MATCH=72/120
  R1_U_fragment_quote 4/12
  R2_U_path_anchor_cols 3/12
  R3_U_declared_id 5/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 7/12
  E2_U_missing_file 2/6
  E3_U_external_url 4/6
  E4_U_no_citation 1/6
  E5_J_resolvable 12/12
  E6_U_undeclared_id 4/6
  E7_U_out_of_corpus 6/6
  E8_U_quote_glued 3/6
  E9_U_heading_as_plain_line 5/6
  E10_U_line_partial 4/6
```

## Limits

Only these ten controls and two scored seeds per control were tested; this is not proof against every shortcut. The two random controls additionally use Bash RANDOM independently of the fixture seed, so repeat counts need not be identical. No C1, candidate, no-harm, selftest, or round-31 check was run. Flat scratch gate paths were used; the U arms in these controls never call source-path/anchor verification, so these receipts are not boundary-reader tests. Existing resolved F1 rows were left to the base reader.

No production patch or counter change is proposed for integration by this seat. All scoring subprocesses were awaited to completion. `timeout 15s stat -c '%n %s' <artifact>/*.json` showed receipts at 2,430-9,930 bytes; scratch gates were 306,617-307,218 bytes. All artifacts remain below 1 MiB. No installs/updates to report.
