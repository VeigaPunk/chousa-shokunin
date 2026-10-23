# CtlC2StatusBlindB — frozen v2 re-score

Axes: operability and coverage. Re-scored all **three unique controls** built by this seat; no oracle or candidate was built/scored. Historical flat-layout copies have the same bytes as these isolated copies, not additional controls. Original report and v1 receipts remain unchanged.

Read `corpus/evidence/round32/claims.md:119-189` and the v2 counter. Target: **132/132**, per `claims.md:171-175`.

## Provenance and gate hashes

`timeout 30s sha256sum corpus/evidence/round32/c2-count-v2.py` and `timeout 30s git show 3d586d3a:corpus/evidence/round32/c2-count-v2.py | timeout 30s sha256sum` both exited 0 and produced **`8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a`**. No counter was edited.

Define `S=/fast/scratch/hyaku/chousa-r32/w1/CtlC2StatusBlindB`; gates remain at `S/gates/<control>/tools/research-gate.sh`. Their implicit lane roots exclude C1_TMP/C2_TMP, both set to S. The v2 layout guard is at `c2-count-v2.py:290-295`.

`timeout 30s sha256sum` on the three gates exited 0 and confirmed these original mutated hashes, all different from pristine `0bc318b3…`; no rebuild was needed:

| Control | Policy | Gate SHA-256 |
|---|---|---|
| a | Audit every exempt status, including J | `d77e02219865a2388de6237938287912cc6cc9db42442cc8fec170b77c112d63` |
| b | Audit only rejected/not-applicable | `3e5a6eaa214247cac75a4c0541f0a33e19a64532a1f70e8f668c4cb53b567b08` |
| c | Audit unresolved/labelled-dead; skip blocked-no-fetch | `7433cf8ec3efe7b74ed49515623aa8d49944b1d7391b119e9b0655f636d01acd` |

## Six executed runs

From `/home/vgpnk/Projects/shokunin/chousa-shokunin`, the literal command shape was (S/R expanded; table values substituted):

```sh
timeout --kill-after=5s 840s prlimit --as=2147483648 --nproc=2000 -- env C1_TMP=S C2_TMP=S TMPDIR=S python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count-v2.py --gate S/gates/<control>/tools/research-gate.sh --seed <seed> --receipt R/v2/<control>-s<seed>.json --keep S/fixture-v2-<control>-s<seed>
```

Here `R=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2StatusBlindB`. All six seeds were newly generated using `secrets.randbits(63)`. The six commands completed in a foreground parallel batch, each exiting **1** and printing **`RECORD_CHECKS=ok`**.

| Control | Seed | Exact count line | Verdict | Receipt relative to this supplement |
|---|---|---|---|---|
| a | 1414181642572804917 | `EXEMPT_AUDIT_MATCH=120/132` | MISSES | `v2/a-s1414181642572804917.json` |
| a | 420130869321930543 | `EXEMPT_AUDIT_MATCH=120/132` | MISSES | `v2/a-s420130869321930543.json` |
| b | 8528809386071819226 | `EXEMPT_AUDIT_MATCH=84/132` | MISSES | `v2/b-s8528809386071819226.json` |
| b | 2225435942560517398 | `EXEMPT_AUDIT_MATCH=84/132` | MISSES | `v2/b-s2225435942560517398.json` |
| c | 7809869176852868085 | `EXEMPT_AUDIT_MATCH=120/132` | MISSES | `v2/c-s7809869176852868085.json` |
| c | 8797509587882078238 | `EXEMPT_AUDIT_MATCH=120/132` | MISSES | `v2/c-s8797509587882078238.json` |

Receipt evidence: each stores the counter/gate hashes and seed, record failure list, gate exit, count and predicate. The opened first receipt for each control has `record_fails=[]` at line 3, `gate_rc=1` and no timeout at lines 10-11, and count/predicate at lines 13-15. Per-class counts are at lines 17-32; missed-hop details start at line 34.

Per-class outputs below were identical on both seeds for each respective control:

| Counter class | a, each seed | b, each seed | c, each seed |
|---|---|---|---|
| R1_U_fragment_quote | 12/12 | 0/12 | 8/12 |
| R2_U_path_anchor_cols | 12/12 | 0/12 | 8/12 |
| R3_U_declared_id | 12/12 | 0/12 | 8/12 |
| F1_resolved_verifiable | 12/12 | 12/12 | 12/12 |
| E1_U_anchor_absent | 12/12 | 12/12 | 12/12 |
| E2_U_missing_file | 6/6 | 6/6 | 6/6 |
| E3_U_external_url | 6/6 | 6/6 | 6/6 |
| E4_U_no_citation | 6/6 | 6/6 | 6/6 |
| E5_J_resolvable | 0/12 | 0/12 | 12/12 |
| E6_U_undeclared_id | 6/6 | 6/6 | 6/6 |
| E7_U_out_of_corpus | 6/6 | 6/6 | 6/6 |
| E8_U_quote_glued | 6/6 | 6/6 | 6/6 |
| E9_U_heading_as_plain_line | 6/6 | 6/6 | 6/6 |
| E10_U_line_partial | 6/6 | 6/6 | 6/6 |
| E11_U_case_only | 6/6 | 6/6 | 6/6 |
| E12_U_whitespace_only | 6/6 | 6/6 | 6/6 |

## Scoped finding

**None MEETS-TARGET under v2.** A still falsely flags all 12 J hops; B misses all 36 U positives and falsely flags all 12 J hops; C still misses the 12 blocked-no-fetch positives. E7 and both new negative classes match throughout. The original status-policy counterexamples and smallest correction remain: audit exactly U, including blocked-no-fetch, and leave J unread/exempt. That correction was not implemented or scored as a candidate.

No production files, index, jj state, or counters were changed. No installs/network/no-harm suite/canonical judgment. `timeout 30s df -h /fast` exited 0 (231 GiB available); `timeout 30s stat -c '%s %n' R/v2/*.json` exited 0 and reported six receipts of 2,454–6,650 bytes. All six score commands finished; no background jobs or subagents were started.
