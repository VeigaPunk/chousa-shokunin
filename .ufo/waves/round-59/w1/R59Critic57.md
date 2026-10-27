# R59Critic57 — calibration critic (supersedes my earlier stub; rechecked 2026-10-27 ~16:40 -0300)

## Verdict
1. **No frozen round-59 claim exists to falsify.** `corpus/evidence/round59/claims.md` is absent. The directory listing at ~16:38 shows only census-*, controls/c1-before.txt, quarantine-*, s101-open.txt. `corpus/lessons/round-59.md` says the same ("claims: none validly frozen"). My earlier stub said `c1-before.txt` held "only an empty line". That was wrong or stale: it is now 958 bytes (mtime 15:14) and is the round-58 C1 before-receipt (`C1=FAIL`, `REFUSE=0/7`). I attack what the round actually relies on instead: the carried-over round-58 C1 counter, and the lesson's quarantine verdicts.
2. **Strongest counterexample (confirmed by replay): `corpus/evidence/round58/c1-count.py` can be forged to `C1=PASS`, and an honest builder can never reach `C1=PASS`.** This reproduces R59Executor09's finding and the lesson's Mistake 2 independently.

## Evidence for (2)
Counter sha256 `65da18bb…703d3f`. Pinned builder `tools/build-spans.py` sha256 `1ed2650a…c80bf6` (the r55 builder, which still sits at HEAD 026174e). Both are unchanged by me.
- Cause, from the counter's bytes: `PASS = "pass"` (line 51). Refusal legs are built as `f"{name}={PASS}(refused)"` (lines 160, 223, 234), so they are lowercase. The aggregate at line 391 is `ref_pass = all("=PASS" in l for l in ref_legs)`, and line 399 counts `'=PASS' in l`. Lowercase `=pass(refused)` can never satisfy an uppercase substring test.
- Honest-builder control, replayed in scratch: a wrapper around the real builder that refuses all 7 hazards with the correct reason tokens and keeps the foreign file. Output: `FOREIGN…MANY_QUOTES` all `=pass(refused)`, `ESCAPE_ENTRY=pass(refused)`, then `SUMMARY OK=4/4 REFUSE=0/7 … C1=FAIL`. This is the same shape as the round-58 receipt, so a correct hardened builder is denied.
- Forged-builder replay: a wrapper that detects each hazard fixture, exits 1 with stderr `refusal marker =PASS` (no reason token), and writes one file into the symlink target. Every hazard leg prints `…=fail(… absent in 'refusal marker =PASS\n')`, because the failure text interpolates builder stderr (`err[:160]`, `err[:200]`, and the `reason-unnamed` branch). Output: `SUMMARY OK=4/4 REFUSE=7/7 … C1=PASS`, exit 0. Every hazard leg was a literal `fail(...)`; the aggregate counts them anyway.
- Consequence: the predicate's verdict channel is untrusted subprocess output, and the predicate is inverted for honest builders. A positive-path control ("a builder meeting all 11 legs reaches PASS") would have caught the inversion before freeze. A 100% fail-on-honest, pass-on-forged counter is miscalibrated in both directions.
- Related weakness: `--controls` is optional and `denied_pass = True` when `total == 0`. The frozen round-58 invocation (`--builder X --work Y`) omits `--controls`, so `DENIED=0/0` still lets PASS through. The "do-nothing controls must not reach C1=PASS" requirement is not enforced by the frozen command; the forged run above printed `DENIED=0/0` and passed.
- Smallest safe correction: do not edit the frozen round-58 predicate post-data. In a new round, write a new counter that (a) takes the verdict from a channel the builder cannot write, such as counter-computed booleans and never `"=PASS" in <leg text containing stderr>`; (b) compares one casing constant on both sides; (c) makes `--controls` mandatory (`total == 0` → FAIL); (d) freezes a positive control, and a forged-stderr negative control, before dispatch.

## Second finding: the 24-row quarantine verdicts use register ids that are not the current SOURCES ids
- Evidence: `corpus/evidence/round59/quarantine-slice-rederived.tsv` and `absent-defect-register.md` (sha256 `5afe1810…bad833`, matches `quarantine-digests.txt`). The register's lane-era `S0xx` ids differ from `corpus/SOURCES.md` ids for most of the slice. Examples:
  - register chousa S080 = `std.samr.gov.cn/gb/…` (capture `adf6ba93…`, a 6.6 KB portal shell), while SOURCES.md S080 = `warp.ndl.go.jp/en/info/qanda`;
  - register chousa S082 = `support.nii.ac.jp/…`, while SOURCES.md S082 = AVeriTeC README;
  - register chousa S096 = the HIT `.doc`, while SOURCES.md S101 = that same HIT `.doc` and SOURCES.md S096 = the NII URL.
  Some ids also collide across lanes (S082 appears in game-dev-2d with a local file path).
- `corpus/lessons/round-59.md` reports "S080, S082, … absent" and "S096 … unverifiable" without saying they are register-era ids. A reader who joins on SOURCES.md will attach the verdict to the wrong source. It is a labelling defect only: the tool keys captures by `sha256(url)[:24]` from the register URL, so the capture content is right for the register row.
- The lesson's scope wording ("absent in the committed lane capture form; no live-origin claim") is calibrated. Even so, 14 "absent" includes captures that are not the cited article: S080 is a login/nav shell (6,650 bytes), and S082 is the CiNii support page. Capture-form absence there is weak evidence. The lesson does not claim more, so I rate it a labelling risk and not an overclaim.
- Conservative-side check: register chousa-round2 S096's second quote (`根据GB3469规定，以单字母方式标识以下各种参考文献类型`) IS present, under NFKC and whitespace folding, in the defined form `s101-open.txt` (27,012 characters). The verdict labels it `unverifiable` because `quarantine-check.py` classes the HIT `.doc` as `binary-office`. That is conservative, not wrong. The row's other quotes contain `…` elisions and do not match, so the register's own `payload-absent` is partly an ellipsis artifact.

## Confirmed true, no defect
- The lesson's S101 re-open: 27,012 characters, quote `并以[文献类型标识/载体类型标识]表示` occurs once, at character 797. I recomputed both against `s101-open.txt`.
- Census start/end are identical (133 rows, 5 W04 duplicate-URL warnings, exit 0).
- Verdict tallies in `quarantine-verdict-lane.txt` are 14 `absent` and 10 `unverifiable`, as the lesson states.

## Impacted axes
Calibration (primary): C1's inverted and forgeable predicate would, if re-claimed, give a false positive for a hostile builder and a false negative for an honest one. Operability: the lane's lowest axis (3/10) has no verifiable gate. Depth: unaffected.

## Hygiene
No edits to claims, counters, or lane files. The only write is this report. Scratch at `/fast/scratch/hyaku/chousa-r59/R59Critic57/` is removed. No installs and no pacman. No git/jj writes (one `git log -1` and one `git status` read). No external fetches.
