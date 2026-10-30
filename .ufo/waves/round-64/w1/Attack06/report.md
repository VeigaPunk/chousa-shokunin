# Attack06 — C1 Unicode mirror review

Axes: contract fidelity, Unicode mirror completeness, frozen/supplement separation, reproducibility. Advisory only; no admission or production change.

## Findings, by severity

### High — frozen C1 full-pass target is unavailable; supplemental success cannot admit it

`corpus/evidence/round64/c1-battery-v3.py:386–394` independently draws `tag()` for the created filename and the README target in E12/E13. These are not the benign matching names promised by `claims.md:42–44`. A conforming mirror checker rejects their phantom paths. This is the assignment's known frozen failure, also recorded in `claims-erratum.md:5`; it was not repaired or rerun here. The frozen kill rule (`claims.md:89–93`) requires the unmodified full battery to pass three times and explicitly says a miss is an honest stop. The distinct post-freeze `c1-battery-supplement.py:386–396` reuses one tag per leg, but cannot replace that rule.

The probe independently confirms `claims.md` and `c1-battery-v3.py` exactly equal their bytes at `bf40d99bda9eefdad3ed6276da077cfb24ba82f1`. Frozen battery SHA256 starts `4b3f0b658bcd3bb6`, matching the claim.

### Medium — inherited candidate silently accepts Unicode phantom rows

`corpus/evidence/round64/controls/ref-preflight-v3.py:136` only extracts ASCII single-component mirror names, using `[A-Za-z0-9][A-Za-z0-9._-]*`. NFC normalization at lines 156–160 cannot make `é` ASCII. Therefore the later filesystem check (139–148) never sees `knowledge/café.md`, whether README bytes use NFC or NFD. A valid `ok.md` plus an indexed nonexistent `café.md` produces `PREFLIGHT=1/1 FAILED=none`, exit 0. Nested `knowledge/sub/café.md` also passes. ASCII `knowledge/gone.md` correctly fails, exit 1, demonstrating the narrower extraction rather than disabled G02.

This violates the mirror contract at `claims.md:53–59`; its Unicode/recursive path coverage is not limited to ASCII. It is a candidate defect, not proof that C1's frozen numerical target is newly refuted. Per frozen routing at lines 91–93, a fresh falsifier belongs to the next battery. The supplement retains ASCII-only E09 (`:376–377`) and only a positive NFC-file/NFD-index E14 (`:398–401`); these do not test a Unicode phantom. No full supplemental pass is claimed here.

## Current implementation distinction

The observed `tools/lane-preflight.py` was already different from freeze when inspected. Its mirror extraction at lines 142–147 accepts Unicode/nested paths, and its normalized relative-name inventory at 148–152 handles both normalization directions. At SHA256 `3d792f0961434ccd76ef87ccb0b2dcccc022f6f84d958dbc4e35e6f4c260a89d`, all three Unicode phantom probes fail G02 (exit 1), and both NFC-file/NFD-index and NFD-file/NFC-index pass (exit 0). No actionable Unicode normalization/mirror defect was reproduced in these current bytes. This does not establish landing status or satisfy frozen C1 closure.

The inherited candidate also passes both positive normalization cases, but its mirror ignores those Unicode paths entirely: passing those cases alone is not evidence that its mirror lookup normalizes filesystem names correctly.

## Bounded evidence

Driver command (cwd `/fast/scratch/hyaku/chousa-r64/Attack06`):

`python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Attack06/probe.py`

Driver exit 0. Full exact per-tool commands, fixtures (escaped Unicode), stdout/stderr and exits: `probe-output.txt` alongside this report. Each CLI uses only `--only G02`, a minimal scratch corpus, explicit absolute `--root` and seat-owned `--work`; 12 invocations total, 15-second timeout each.

| Fixture | Candidate exit | Current tool exit | Contract expectation |
|---|---:|---:|---:|
| ASCII phantom | 1 | 1 | 1 |
| NFC Unicode phantom | 0 | 1 | 1 |
| NFD Unicode phantom | 0 | 1 | 1 |
| Nested Unicode phantom | 0 | 1 | 1 |
| NFC file / NFD index | 0 | 0 | 0 |
| NFD file / NFC index | 0 | 0 | 0 |

## Residual risk and verification gaps

- `xd://lsp` is unavailable (device returned “No such tool”); definition/reference/diagnostic requests could not be issued. Source searches are textual, not semantic proof. CLI observations provide behavioral evidence.
- No full C1/supplement battery, null controls, multi-seed closure or landing-commit verification was run in this narrow seat; no such success is inferred.
- No production, frozen instrument, sibling, git/jj or operator-input mutation. No clone, network fetch, installation or service operation. Existing Python 3.14.8 (`/usr/bin/python3`, system channel) was used for bounded probes; no tools installed/updated.
- Scratch fixtures removed before handoff; the retained driver and output permit reproduction.

Self-evaluation: accuracy 4 (current-byte hashes, not landing proof); completeness 4 (scoped G02 probes, not full closure); clarity 4 (candidate/current separation explicit); actionability 4 (reproducer retained, integration reserved to L1); conciseness 4 (raw output separate). Overall 4.0/5. Improvements: add these negative Unicode cases to a future distinct battery, preserve frozen failure disclosure, and use landing-bound receipts for any closure. User-agreement check: results are scoped advisory findings, not an admission.
