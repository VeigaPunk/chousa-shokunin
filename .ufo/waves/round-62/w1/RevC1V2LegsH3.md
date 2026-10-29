# RevC1V2LegsH3 — review of legs H13 OUTSIDE, H14 BIGTXT, H15 BIGRAW (c1v2-count.py, both profiles)

Scope: read-only review of `corpus/evidence/round62/c1v2-count.py` (docstring, `Fx`, `_env_and_limits`, `run`, `leg_h13`, `big_leg`, `main`). Frozen files untouched. Variant builders and probes lived in scratch (`/fast/scratch/hyaku/chousa-r62/RevC1V2LegsH3/`), deleted before yield. No tools installed. No network.

## Findings (by severity)

### D1 — FALSE POSITIVE: H14 rejects a correct builder that refuses the 192 MiB capture
- Builder `b1-cap80.py` = pos-indep1 with `MAX_BYTES = 80 MiB` and the `st_size` pre-check removed from `safe_read`: it reads 1 MiB chunks and refuses past the cap; exit 1, nothing written.
- Repro: `C1V2_SEED=1 python3 -B corpus/evidence/round62/c1v2-count.py --builder <scratch>/b1-cap80.py --work <scratch>/w`
- Observed: `LEG H14 BIGTXT fail neutral: FAIL rc=1 rss_kib=102776 limit=98304 | plain: FAIL rc=1 rss_kib=102552 limit=98304` / `LEGS=19/20 C1V2=FAIL`. Same at seeds 2 and 3 (RSS 101.6–103.1 MiB). Leg probe, 10 trials per profile: `SUMMARY b1-cap80 H14 plain pass=0/10`, `... neutral pass=0/10`.
- Cause: H14 measures `ru_maxrss` of the child, so a builder that refuses correctly after buffering its own cap fails. Interpreter baseline is ~20 MiB; the buffer adds the cap. The docstring fixes no cap value, so the verdict tracks the builder's cap, not the hazard (INFERENCE: any buffered cap above ~74 MiB fails).
- Not a defect of the builders with pre-checks: pos-indep1/2/3, b2, b3x all pass.

### D2 — TAUTOLOGY / false negative: H13 passes a builder that follows the cache link, writes output from the victim, and exits 1
- Builder `leaky_h13.py`: `open(cache/<key>.txt)` follows the symlink, writes `spans/S101-1.txt` from the victim's text, then `sys.exit(1)`.
- Observed (seed 1): `LEG H13 OUTSIDE pass neutral: ok rc=1 leaked=False | plain: ok rc=1 leaked=False`.
- Manual check (fixture with a symlinked cache capture): `S101-1.txt` = `orem051 … needle phrase here tail000 … tail009`, i.e. victim content; `grep -c OUTSIDE` = 0.
- Cause: H13 requires only `rc != 0` and a marker search at byte 0 of the victim; the 80-char window never reaches the marker. Unlike H14/H15/H18/H19, H13 does not require `clean_out`.

### D3 — TAUTOLOGY: H14 passes a builder with NO size guard in the plain profile
- Builder `naive_read.py`: `open(p,'rb').read()` on every `.txt`/`.raw` in the cache, then `sys.exit(2)`.
- Plain profile fixes `RLIMIT_AS` at 200 MiB. `as_probe.py`: a 192 MiB read raises MemoryError at 200/204/208 MiB.
- Observed: `SUMMARY naive_read H14 plain pass=10/10`; `rc=1 rss_kib=~19000`. The leg passes an unbounded read. The H14 RSS criterion is never exercised in plain.

### D4 — TAUTOLOGY (unmeasured): H15 passes through capture-text's own allocation failure
- Builder `b2-captext.py`: calls `capture-text.text_form` on the OLE `.raw` with no pre-size check (the `.raw` path normally slurps first).
- capture-text reads `MAX_PART + 1` = 256 MiB+1 (`tools/capture-text.py:395`); under the 200–224 MiB address-space limit this raises MemoryError, converted to `Refused: package too large to render in memory` (`:399–400`). Probe `ct_probe.py` at AS 200/224/256 MiB: all `Refused`.
- Observed: `LEG H15` pass, `rc=1 rss_kib≈22000`, 3 seeds × 2 profiles, plus leg probe 10/10 and 10/10.
- The builder refuses correctly; the leg does not measure the bound it names (RSS < 96 MiB). Pass is an address-space artifact.

### D5 — PROFILE-DEPENDENT and NOT REPRODUCIBLE from `C1V2_SEED`: H14/H15 verdict for an unchanged builder flips
- `_env_and_limits` draws the neutral address-space limit with `secrets.choice(range(0, 25))` (`c1v2-count.py:291`); names, URLs, env and `RLIMIT_FSIZE` also use `secrets` (lines 153, 170, 178, 188, 285–290). `C1V2_SEED` seeds only leg order and content RNGs (lines 698–704). The docstring's "the leg order and fixture contents come from a seed" is therefore only partly true.
- Probe `neutral_probe.py 20` (naive_read, H14, neutral): AS 201–221 MiB → ok (17/20); AS 223–224 MiB → `FAIL rc=2 rss_kib≈215000` (3/20). Plain is always 200 MiB → always ok.
- Earlier probe run: neutral H14 10/10 pass; a second run: 2/6 neutral FAIL (trials 0 and 5). Same builder, same leg, different verdict.
- The effective threshold inside the counter (~222 MiB) differs from a bare Python probe (~212 MiB); I did not isolate why (INFERENCE: the sandboxed child's baseline differs).

## Checked and passing (both profiles unless stated)
| builder | seeds | result |
|---|---|---|
| tools/build-spans.py (landing) | 1 | `LEGS=20/20 C1V2=PASS` |
| controls pos-indep1 / pos-indep2 / pos-indep3 | 1 | `LEGS=20/20` each (pos-indep2 heals H11/H12 by exit 0, permitted) |
| b2-captext (correct, D4 builder) | 1,2,3 | `LEGS=20/20` each |
| b3x-exitcodes (pos-indep2; exit 2 only for oversize refusals, 1 otherwise) | 1,2,3 | `LEGS=20/20` each |
| b1-cap80 (correct refusal, 80 MiB cap) | 1,2,3 | `LEGS=19/20`, only H14 (D1) |

My first b3 variant (every refusal exit 2) failed P05 (`P05 REFUSEROW fail … rc=2`; P05 requires exit 1). That was my variant's error, not a counter defect; the corrected b3x passes.

## Do-nothing builders (criterion b)
- `stub_exit2.py` (`sys.exit(2)`): H13, H14, H15 pass in both profiles (`LEG H14 BIGTXT pass neutral: ok rc=2 rss_kib=16212`). In fact H07, H09–H12, H16–H20 pass too; `LEGS=14/20 C1V2=FAIL`, the rejection comes from P01/P02/P04/P05/P06/H08. This is the named design (refusal legs), caught by the battery's stub rows; not counted as a leg defect.

## Profile-dependent verdicts (criterion c)
- H14, H15 for any builder that reads a whole capture: plain fixed at 200 MiB (always MemoryError, always pass); neutral 200–224 MiB unseeded (flips near ~222 MiB). See D3, D5.
- H15 via capture-text (D4): profile-invariant within the 200–224 MiB range (always `Refused`).
- H13: no profile dependence observed (leaky and stub verdicts identical in both profiles).
- Names: no masking observed. The victim path is absolute (`fx.dir/outside.txt`); the random cache and out names do not collide in any run.
- INFERENCE, not run: the neutral cwd is an empty directory outside the fixture; a builder that resolves `capture-text.py` relative to cwd would crash (exit 1) only in neutral and pass H13–H15 vacuously.

## Commands and receipts
- `C1V2_SEED=1 python3 -B corpus/evidence/round62/c1v2-count.py --builder tools/build-spans.py --work …` → `LEGS=20/20 C1V2=PASS`.
- `C1V2_SEED=N … --builder <variant>` for seeds 1–3, variants above; outputs under scratch `r-*/out.txt`.
- `leg_probe.py 10` and `leg_probe.py 6`: per-leg repeats, `SUMMARY` lines quoted above.
- `neutral_probe.py 20`: AS draw vs H14 verdict.
- `as_probe.py <MiB> sparse192.txt`: MemoryError at 200–208, ok at 212+ (bare Python).
- `ct_probe.py <MiB>`: `Refused: package too large to render in memory` at 200/224/256.

## Recommendations (not applied; frozen counter)
1. H13: require `clean_out` or a byte-run check on the victim's body, not only the marker at byte 0.
2. H14/H15: state the memory bound as a policy (cap) or drop the RSS criterion for refusals; measure RSS in plain against a real read.
3. Derive the neutral address-space limit and names from the seed, or record them in the receipt.

Verdict input for the battery: the three legs are not clean. D1 is a false positive; D2–D4 are tautologies; D5 is a reproducibility/profile defect.

VERDICT: LEG_DEFECTS=5 false_positive=1 tautology=3 legs=H13 OUTSIDE, H14 BIGTXT, H15 BIGRAW
