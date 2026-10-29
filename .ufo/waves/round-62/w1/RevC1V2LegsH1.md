# RevC1V2LegsH1 — review of legs H07 FOREIGN, H08 REPLACE, H09 ORPHAN (c1v2-count.py, both profiles)

Read-only review. Frozen counter sha256 prefix `b7016fba91b03460` (checked after my runs, unchanged). No file
under corpus/evidence/round62, tools/, corpus/ or SKILL.md was written. No installs. Scratch
`/fast/scratch/hyaku/chousa-r62/RevC1V2LegsH1` removed before yield.

## Method
- Read the counter docstring (lines 24–27: H07/H08/H09 contract) and the leg code (`leg_h07_h08`, `leg_h09`,
  `run`, `_env_and_limits`, lines 280–488).
- Correct builders: the three controls `pos-indep1/2/3.py`, the landed `tools/build-spans.py`, and three new
  variants I wrote in scratch from the controls with different guard order and write order:
  - vA (from pos-indep1): orphan refusal checked before the differing-file loop; span files written before the
    manifest; orphans removed last.
  - vB (from pos-indep2): orphan refusal checked before the manifest check (not only when no manifest exists);
    orphans removed after the writes.
  - vC (from pos-indep3): span files written before the manifest; orphans removed last.
- Command used (each seed separately): `C1V2_SEED=<N> python3 -B corpus/evidence/round62/c1v2-count.py --builder <B> --work <fresh>`.
- Negative and probe builders in scratch: stub2 (`sys.exit(2)`), stub1, stub0, stub2touch (exit 2 after writing
  marks into the cache and the cache's parent), naive (reads each whole `.txt`, exits 1), vE (vA plus an
  over-broad `--replace` that deletes every non-span file under `spans/`), and the round-61 base builder.

## F1 — false positives: none
Correct builders, all runs: `LEGS=20/20 C1V2=PASS` in both profiles, so H07, H08 and H09 pass for each.

| builder | seeds | result |
|---|---|---|
| tools/build-spans.py (landed, c366492005ce304a) | 1, 2, 3 | 20/20 ×3 |
| controls pos-indep1 | 1, 2, 3 | 20/20 ×3 |
| controls pos-indep2 | 1, 2, 3 | 20/20 ×3 |
| controls pos-indep3 | 1, 2, 3 | 20/20 ×3 |
| vA | 1, 2, 3 | 20/20 ×3 |
| vB | 1, 2, 3 | 20/20 ×3 |
| vC | 1, 2, 3 | 20/20 ×3 |

Evidence: `LEG H07 FOREIGN pass neutral: ok rc=2,2 | plain: ok rc=2,2`; `LEG H08 REPLACE pass neutral: ok rc=0 | plain: ok rc=0`;
`LEG H09 ORPHAN pass neutral: ok rc=2 | plain: ok rc=2` (same lines for every row above).

## F2 — tautology: H07 and H09 pass with a builder that always exits 2 and writes nothing
Repro: `import sys; sys.exit(2)` saved as stub2.py, run with seed 1:
```
LEG H07 FOREIGN pass neutral: ok rc=2,2 | plain: ok rc=2,2
LEG H08 REPLACE fail neutral: FAIL rc=2 | plain: FAIL rc=2
LEG H09 ORPHAN pass neutral: ok rc=2 | plain: ok rc=2
LEGS=14/20 C1V2=FAIL
```
The stub passes 14 of 20 legs (P03 and H07, H09–H20 except H08). H07 and H09 check only `rc == 2` plus an
unchanged tree, so refusing everything satisfies them. H08 cannot be passed without writing the golden tree.
The battery still rejects the stub through the P legs, so this is a per-leg tautology, not a battery hole.

## F3 — coverage: H07 and H09 snapshot only DIR
Repro: stub2touch.py (exit 2 after writing `<cache>/../touched-outside-dir.txt` and `<cache>/leftover.lock`):
```
LEG H07 FOREIGN pass neutral: ok rc=2,2 | plain: ok rc=2,2
LEG H09 ORPHAN pass neutral: ok rc=2 | plain: ok rc=2
```
`snap` covers only `fx.out`. The landed docstring says a refusal writes "nothing written or removed" in DIR, so
this is inside the contract's scope; the leg just does not look outside DIR. Severity: low.

## F4 — coverage/policy: no leg plants a differing span file under an identical manifest
Repro with the landed builder (no --replace): build S101, overwrite `spans/S101-1.txt` with `X-TAMPERED`, rebuild.
```
tools_build-spans first_build_rc=0 rebuild_after_span_tamper_rc=0 span_now=amma delta alpha bet | QUOTE S101 char 276 ...
b_vA first_build_rc=0 rebuild_after_span_tamper_rc=2 span_now=X-TAMPERED | build-spans: refused output: .../spans/S101-1.txt exists and dif...
b_vB  ... rebuild_after_span_tamper_rc=0 ... (overwritten)
b_vC  ... rebuild_after_span_tamper_rc=0 ... (overwritten)
controls_pos-indep1 ... rebuild_after_span_tamper_rc=2 ... (refused)
```
The landed builder silently repairs the span file (exit 0). Its docstring refusal list (lines 41–44) names a differing
spans.tsv, an extra span file, and a leftover `.tmp`, not a differing span file. The strict policy in pos-indep1's
docstring does refuse it. Every leg here sets up a differing spans.tsv, so H07 cannot tell the two policies apart:
the landed builder, vB and vC all score 20/20 at seeds 1–3. This is a policy question the counter does not decide;
route it as a counter limit or a supplement, and do not treat it as a leg rewrite.

## F5 — coverage: H08 plants no non-span file under spans/
vE (over-broad --replace deletion) passes 20/20 at seeds 1 and 2 (`LEG H08 REPLACE pass ... rc=0`). Repro:
after a build, create `spans/notes.md`, then rerun with `--replace`: vE exits 0 and removes `notes.md`; the landed
builder exits 0 and keeps it (`notes_md_exists=yes`). pos-indep1's docstring (lines 36–37) says non-output files are
never touched, which the landed docstring does not state. H08 only plants `README.txt` at the DIR root, so no leg
pins this.

## F6 — tautology in H14/H15 (not in scope, noted for the battery)
naive.py (reads each whole `.txt`, then exits 1) and stub1 both pass H14 and H15 in both profiles
(`LEG H14 BIGTXT pass ... rc=1 rss_kib=19356 limit=98304`). Any nonzero exit with RSS under 96 MiB counts as a
refusal; the naive read dies with MemoryError under the 200 MiB address-space limit, which is what passes it.

## (b) Name masking
No name-based masking reproduced. The neutral profile randomises only parent-level names (fixture dir, tools dir,
cache, quotes file, out, builder file, cwd). The contract names `spans`, `spans.tsv`, `README.txt`, `S404-9.txt` and
`victim*` are fixed in both profiles, so a hazard keyed to them is seen by both. Out/cache collision probability
is (1/25)·Σ_{L=4..8} 26^-L = 9.1e-8 (computed), so it cannot mask anything in practice (INFERENCE from the code).

## (c) Profile-dependent verdicts
- H07, H08, H09: no name, env, pipe or stdin input in the verdict. Observed `rc` and detail were identical in both
  profiles for every builder above (stub2, stub1, base, naive, vA–vE, landed, pos-indep1–3).
- H14, H15: the verdict uses the address-space limit (200 MiB plain; 200–224 MiB neutral, random offset 0–24 MiB).
  A builder whose 192 MiB read fits in one profile and not the other would flip the verdict. Not observed: the naive
  read fails by MemoryError in both profiles. INFERENCE that a flip is reachable near the boundary.
- H20: verdict is `rc != 0` plus clean out; the same address-space offset applies. Not observed to flip.
- H17: uid-dependent (`SystemExit` under root); not a profile effect.
- H18: depends on the FIFO and stdin (DEVNULL in plain, closed pipe in neutral). Verdict uses rc and timeout only.
  Not observed to flip.

## Other observations (out of H07–H09 scope)
- pos-indep3 (a control) writes `spans.tsv` before its span files; the landed docstring requires span files first.
  No leg checks write order; there is no fault injection.

VERDICT: LEG_DEFECTS=4 false_positive=0 tautology=2 legs=H07 FOREIGN, H08 REPLACE, H09 ORPHAN
