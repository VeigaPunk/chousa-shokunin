# CtlC2StatusBlindB — C2 status-blind controls

## Axes, scope and result

Axes: **operability** (reproducible, bounded local control scoring) and **coverage** (the U/J status distinction and all three U statuses). These are control-counter results, not an admission or canonical Rust judgment.

**All three controls MISSES. None MEETS-TARGET.** After isolating each scratch gate's implicit lane root from the generated fixtures, A scored **108/120**, B **72/120**, and C **108/120**, each on two fresh seeds. The frozen counter rejected all three specified wrong status policies. This does not establish general counter completeness.

A scratch-layout confound was also exercised and corrected without modifying any gate bytes or the frozen counter: a gate placed directly in the seat directory implicitly permits the counter's supposedly out-of-corpus files through `LANE_ROOT`. Initial receipts are retained, not replaced.

## Inputs and changes

Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

- Read `corpus/evidence/round32/claims.md` first, then both counter docstrings. C2's U/J contract is at `claims.md:60-70`; target is `claims.md:77-81`.
- Base gate SHA-256: `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`.
- Frozen C2 counter SHA-256: `b6626b2cb81b2aeaf66a8ff11a06c030612bf4e264dc128f290021c4aa71f54c`.
- Frozen C1 counter SHA-256, read only: `9e787e80b215f6522335c639d5e1b2e60d0a5812b83a9760daf8be9f78415885`.

Observed provenance commands, all exit 0:

```sh
timeout 30s sha256sum tools/research-gate.sh corpus/evidence/round32/c1-count.py corpus/evidence/round32/c2-count.py
timeout 30s git show 7a7259f0ad41a68068131bfa422a829db9fd1b55:tools/research-gate.sh | timeout 30s sha256sum
timeout 30s git show 4111607c857bc29ff31883bc095ae00afb527e50:corpus/evidence/round32/c2-count.py | timeout 30s sha256sum
timeout 30s df -h /fast
```

The working gate and base-commit gate produced the same gate hash above; the working counter and frozen-commit counter produced the same counter hash above. `/fast` reported 236 GiB available before fixture writes.

Define `S=/fast/scratch/hyaku/chousa-r32/w1/CtlC2StatusBlindB` and `R=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2StatusBlindB` below. All code experiments and kept fixtures are under S; all receipts are under R.

Three `timeout 30s cp tools/research-gate.sh S/control-<name>.sh` operations copied the verified base gate. The only applied code edits replaced the copies' exempt arm, originally `tools/research-gate.sh:1880-1883`. The resolved arm, source refusal logic and anchor matcher were not edited. Each control reuses the resolved arm's sequence: `chain_citation`, declared-source lookup, `chain_ref_file`, `claim_source_path`, source read, `chain_anchor_at` (`tools/research-gate.sh:1829-1868`). Non-verifying exempt rows retain the base exempt output without findings. A verifying selected row emits `observed=resolvable`, `verdict=mismatch`, and one `CHAIN_EXEMPT_RESOLVABLE` warning.

| Control | Intentional incorrect policy | Final scratch gate | SHA-256 |
|---|---|---|---|
| A | Run resolution for every exempt status, including rejected/not-applicable | `S/gates/a/tools/research-gate.sh` | `d77e02219865a2388de6237938287912cc6cc9db42442cc8fec170b77c112d63` |
| B | Run resolution and flag only rejected/not-applicable; leave all U unread | `S/gates/b/tools/research-gate.sh` | `3e5a6eaa214247cac75a4c0541f0a33e19a64532a1f70e8f668c4cb53b567b08` |
| C | Run resolution for unresolved/labelled-dead; skip blocked-no-fetch and J | `S/gates/c/tools/research-gate.sh` | `7433cf8ec3efe7b74ed49515623aa8d49944b1d7391b119e9b0655f636d01acd` |

The edited selectors are at each final scratch gate's lines 1880-1883. Original scratch names were `control-a-status-blind.sh`, `control-b-judgment-only.sh`, and `control-c-skip-blocked.sh`; relocating these via bounded `mkdir`/`cp` preserved the hashes, as recorded by the final receipts (`:4-5`).

## Executed score commands and receipts

Every score ran from the lane directory, in the foreground, with this exact command shape (S/R expanded to the absolute paths above; row values substituted literally):

```sh
timeout --kill-after=5s 840s prlimit --as=2147483648 --nproc=2000 -- env C1_TMP=S C2_TMP=S TMPDIR=S python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate S/gates/<control>/tools/research-gate.sh --seed <seed> --receipt R/<receipt> --keep S/fixture-<control>-isolated-s<seed>
```

All six isolated-layout counter commands exited **1**; every receipt records `gate_rc=1`, `gate_timed_out=false`, and `predicate_holds=false` (`:9-14`). Seeds were freshly generated with `secrets.randbits(63)` before the batch. Each C2 invocation is one 120-hop trial; this counter prints per-class lines, not separate per-hop trial lines. All unmatched hop identities and observed/truth values are preserved in each receipt's `misses` array.

| Control | Seed | Exact count line | Verdict | Receipt, relative to this report's directory |
|---|---|---|---|---|
| A | 1174776549879400474 | `EXEMPT_AUDIT_MATCH=108/120` | MISSES | `CtlC2StatusBlindB/a-isolated-s1174776549879400474.json` |
| A | 8048039243246351064 | `EXEMPT_AUDIT_MATCH=108/120` | MISSES | `CtlC2StatusBlindB/a-isolated-s8048039243246351064.json` |
| B | 7972812763224236474 | `EXEMPT_AUDIT_MATCH=72/120` | MISSES | `CtlC2StatusBlindB/b-isolated-s7972812763224236474.json` |
| B | 5576680422128023696 | `EXEMPT_AUDIT_MATCH=72/120` | MISSES | `CtlC2StatusBlindB/b-isolated-s5576680422128023696.json` |
| C | 6108786777257508530 | `EXEMPT_AUDIT_MATCH=108/120` | MISSES | `CtlC2StatusBlindB/c-isolated-s6108786777257508530.json` |
| C | 6936415113134283365 | `EXEMPT_AUDIT_MATCH=108/120` | MISSES | `CtlC2StatusBlindB/c-isolated-s6936415113134283365.json` |

### Per-class output lines

Each block below was identical on **both listed seeds for that control**. Each receipt also stores these exact class counts at lines 16-29.

A, seeds 1174776549879400474 and 8048039243246351064:

```text
EXEMPT_AUDIT_MATCH=108/120
  R1_U_fragment_quote 12/12
  R2_U_path_anchor_cols 12/12
  R3_U_declared_id 12/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 12/12
  E2_U_missing_file 6/6
  E3_U_external_url 6/6
  E4_U_no_citation 6/6
  E5_J_resolvable 0/12
  E6_U_undeclared_id 6/6
  E7_U_out_of_corpus 6/6
  E8_U_quote_glued 6/6
  E9_U_heading_as_plain_line 6/6
  E10_U_line_partial 6/6
```

B, seeds 7972812763224236474 and 5576680422128023696:

```text
EXEMPT_AUDIT_MATCH=72/120
  R1_U_fragment_quote 0/12
  R2_U_path_anchor_cols 0/12
  R3_U_declared_id 0/12
  F1_resolved_verifiable 12/12
  E1_U_anchor_absent 12/12
  E2_U_missing_file 6/6
  E3_U_external_url 6/6
  E4_U_no_citation 6/6
  E5_J_resolvable 0/12
  E6_U_undeclared_id 6/6
  E7_U_out_of_corpus 6/6
  E8_U_quote_glued 6/6
  E9_U_heading_as_plain_line 6/6
  E10_U_line_partial 6/6
```

C, seeds 6108786777257508530 and 6936415113134283365:

```text
EXEMPT_AUDIT_MATCH=108/120
  R1_U_fragment_quote 8/12
  R2_U_path_anchor_cols 8/12
  R3_U_declared_id 8/12
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

## Counterexamples, impacted axes and smallest safe corrections

### A: status-blind auditing overturns explicit judgments

- Counterexample: hop `h9336ad42` is `rejected`, with heading `bituze guyori pezekana`; A reports resolvable instead of exempt. Evidence: `R/a-isolated-s1174776549879400474.json:33-36`; `S/fixture-a-isolated-s1174776549879400474/root/r40ddbfbbdd.md:126`; the heading really exists at `S/fixture-a-isolated-s1174776549879400474/root/f350b57a1d9.md:7`.
- The paired not-applicable example is `h5cf7dac1`: the record at `r40ddbfbbdd.md:116` names that status and the receipt at `:39-42` records the same false resolvable observation.
- Impact: **coverage** — all 12 E5 judgment hops are falsely flagged while the other 108 hops match (`receipt:16-29`).
- Smallest safe correction [INFERENCE]: limit the audit selector to U; leave rejected/not-applicable on the unchanged, unread exempt path. This correction was not built or scored as a candidate.

### B: judgment-only auditing reverses the intended population

- Counterexample: `h38f50595` is unresolved and cites the quote `peguhope rimona`; B leaves it exempt. Evidence: `R/b-isolated-s7972812763224236474.json:33-36`; `S/fixture-b-isolated-s7972812763224236474/root/r66e71b7c6d.md:131`; the complete token-delimited quote is present at `S/fixture-b-isolated-s7972812763224236474/root/f807317c0ff.md:3`.
- Impact: **coverage** — all 36 R1-R3 audit positives are missed and all 12 E5 judgments are wrongly flagged; the remaining 72 match (`receipt:16-29`).
- Smallest safe correction [INFERENCE]: replace the judgment-only selector with exactly U, without auditing J. Not built/scored as a candidate.

### C: interpreting blocked-no-fetch as exempt from the audit leaves a hole

- Counterexample: `h3fcd3754` is blocked-no-fetch and cites `yodahomo vigulo`; C leaves it exempt. Evidence: `R/c-isolated-s6108786777257508530.json:33-36`; `S/fixture-c-isolated-s6108786777257508530/root/r4c57bd6445.md:68`; the token-delimited quote exists at `S/fixture-c-isolated-s6108786777257508530/root/f334c09f38a.md:5`.
- Impact: **coverage** — R1/R2/R3 each fall to 8/12; all other classes match (`receipt:16-29`). The generator cycles U with `ustat = U[i % 3]` (`corpus/evidence/round32/c2-count.py:169-184`), so skipping blocked-no-fetch drops four positives per R class.
- Smallest safe correction [INFERENCE]: include blocked-no-fetch in the U selector while retaining the local-only resolver's URL refusal. A no-fetch declaration is not proof that a local citation is unavailable (`claims.md:60-70`). Not built/scored as a candidate.

These are fixable status-policy defects exposed by the counter, not measured no-harm tradeoffs or an instruction to the canonical judge to accept an implementation.

## Exercised harness/environment finding: scratch gate roots can confound E7

**Counterexample.** In the first layout, a control gate lived at `S/control-a-status-blind.sh`. The gate computes `LANE_ROOT` as the parent of its script directory (`tools/research-gate.sh:290-291`), therefore `/fast/scratch/hyaku/chousa-r32/w1`. The source resolver accepts either the explicit root or that implicit lane root (`tools/research-gate.sh:1213-1221`). The counter creates both `root` and sibling `outside` under C2_TMP (`corpus/evidence/round32/c2-count.py:151-154,208-210,247-249`). Consequently its E7 files were outside the explicit root but inside the permitted implicit lane root.

For example, initial A receipt `R/a-s5437890801268762009.json:105-108` marks hop `h58ab0ff5` truth=exempt but observed=resolvable. The row at `S/fixture-a-s5437890801268762009/root/r31226e0de2.md:110` cites `../outside/f11455087b7.md`; its heading exists at `S/fixture-a-s5437890801268762009/outside/f11455087b7.md:2`. This is an environmental hidden-truth mismatch, not a demonstrated resolver-boundary regression.

Initial commands used the same bounded command shape above, except `--gate S/control-<name>.sh`, `--receipt R/<control>-s<seed>.json`, and `--keep S/fixture-<control>-s<seed>`. Every initial command exited 1. All six initial receipts remain under R:

| Control | Seeds | Count on each | E7 on each | Receipt names |
|---|---|---|---|---|
| A | 5437890801268762009; 4787160415286198860 | 102/120 | 0/6 | `a-s5437890801268762009.json`; `a-s4787160415286198860.json` |
| B | 8312809104522684975; 4557530547418290771 | 72/120 | 6/6 | `b-s8312809104522684975.json`; `b-s4557530547418290771.json` |
| C | 2495862080249477540; 3189195891604452643 | 104/120 | 2/6 | `c-s2495862080249477540.json`; `c-s3189195891604452643.json` |

Their per-class values are retained in each receipt at `:16-29`. Relative to the isolated output blocks above, only E7 changes for A (6/6 to 0/6) and C (6/6 to 2/6); B is identical. Initial A/C receipts therefore include six/four additional E7 misses, respectively.

**Smallest safe correction applied to experiment layout:** copied unchanged gate bytes into `S/gates/{a,b,c}/tools/research-gate.sh`, leaving generated fixtures elsewhere under S. The implicit lane roots then exclude the fixture trees, and all six isolated-layout receipts score E7 at 6/6 while preserving the intended status-policy failures. No counter was patched. This is a counter invocation precondition finding for L1: ensure the fixture's `outside` directory lies outside *both* allowed roots when using `--gate`. It impacts **operability** (score reproducibility) and **coverage** (E7 truth validity).

## Limits and bounds

- Only the three assigned deliberately incorrect C2 controls were scored; no C1/C2 candidate build or feasibility oracle was scored. No production files, Git index, or jj state were written. No canonical runtime was invoked.
- No network, package installation, selftest, no-harm suite, lint, format, or unrelated regression checks were run. The unchanged F1 class matched 12/12 in every run; that is not a general no-harm claim.
- Twelve counter commands completed in foreground batches; none timed out. No background job or subagent was started. Fixtures are finite 120-hop counter fixtures; no unbounded log/fixture writes were used.
- `timeout 30s stat -c '%s %n' R/*.json` exited 0: all 12 receipt artifacts are 2,372–6,567 bytes, below 1 MiB. Scratch gate hashes are retained above and in receipts; scratch fixtures are retained at the `--keep` paths for the sampled path:line evidence.
- The three controls all MISSES, so there is no control acceptance loophole to explain. The exercised root-layout confound is reported without amending the frozen predicate or counter.
