# R74ReviewFreeze — author-lane recommendation

Frozen revision reviewed: `1eaa30ad248bbd3bd7469b2c17295fcda5fc02bb`. Axes: depth, coverage, operability, freshness, calibration, adjacency; C1 selects operability only. This is not independent admission or promotion authority.

## Findings, by severity

### Medium — prefreeze detection-forger obligation is not evidenced by the submitted control matrix

Frozen `corpus/QUALITY.md:1002` criterion 126 requires a committed detection-forger battery before a counter running a candidate binds a claim, supplementing criterion 119 (`:986`). `corpus/evidence/round74/loader-matrix.py` runs the candidate counter as a subprocess, but its nine cases vary repository edits, not candidate implementation. The frozen round74 evidence directory contains only claims, matrix, successor, before receipt and positive receipt. Those receipts establish base discrimination and positive reachability, not rejection of counter-detecting candidates. No detection-forger battery receipt is supplied by the frozen claim.

This is a freeze-process evidence gap against the lane's own criterion, not evidence that the one-line repair is wrong. Integration should explicitly disposition applicability/compliance rather than silently treating 9/9 as anti-forgery certification. Do not change the frozen predicate to conceal the gap. I did not run an unauthorized broader battery or construct a forger.

### Low — the nine-case predicate does not exercise the nonnumeric deletion branch

`corpus/evidence/round74/correction-count.py:131` both switches to numstat column 1 and changes the nonnumeric fallback from zero to one. All nine matrix inputs are ordinary text edits (`loader-matrix.py`, FILES/CASES); none produces Git's binary `-` deletion cell. Therefore the frozen matrix establishes the numeric-column repair on its named cases but cannot establish the fallback change. [INFERENCE] A column-1 implementation retaining `else 0` would be observationally identical on these nine fixtures. This is a certification limit, not a blocker to the explicitly bounded numeric loader result. Binary/text-decoding behavior is not certified here.

## Freeze, controls and narrow result

- HEAD initially equalled the supplied freeze. Six reviewed artifact working copies exactly matched their frozen Git blobs: claims, matrix, successor, original, before receipt and positive receipt. Unrelated in-flight lane edits were not treated as frozen evidence or modified.
- SHA256 original: `e6e22b1ec8d270171cf015d44cac3d544a61bd23a3fa67d14c91fa26585dc320`; successor: `9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41`; matrix: `979638251845071cfb2c5e130cd81800251c5a6cb041438deb258d8877e2ff8d`. Both control receipts bind the matching counter digest.
- Frozen source comparison shows exactly the title change and loader assignment change; additionally the successor is mode 100644 versus original 100755. All claimed commands invoke Python explicitly, so that mode difference does not break the declared CLI contract. `check()`, its callers, and inherited semantic checks remain unchanged.
- Before receipt: 3/9, exit 1; the three appends wrongly fail C2-6 and the three deletions wrongly pass. Positive receipt: 9/9, exit 0, including unchanged, all three appends, all three deletions, equal replacement and receipt modification. Cases are evaluated against one fixed base; restoring FILES before each commit prevents previous case edits contaminating the base-to-revision comparison.
- The matrix checks child exit, seven distinct CHECK entries and the exact expected failed-id set. The actual successor emits fixed C2-1 through C2-7; matrix parsing alone does not authenticate arbitrary candidate output or execution provenance.
- I executed only the bounded historical second conjunct, read-only: exit 0, `C2=PASS checks=7/7 rev=5aec90775fc7 base=f748abbb6bf5`. Absolute receipt: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74ReviewFreeze/historical-conjunct.txt`.

## Axes, sources and frontier duties

`AXES.md:27-38` allows one claim and requires the lowest-scored non-retired axis plus no harmed axis. With one C1, cross-claim causal separability is vacuous; the two conjuncts jointly test one repair, not two axis claims. Frozen `SCORECARD.md:7-13` scores only operability at historical 3/10, explicitly capped by its three-input observable. Frozen `:486-495` leaves the saturation waiver dormant: 3 is below 8 and unscored axes are not saturated. C1 works the owed axis without claiming a numeric increase. No frontier/capability waiver or saturation claim is justified or needed.

The source anchor is real: frozen `corpus/lessons/round-73-verifier-spotcheck.md:65-67`, section 5 item 1, routes the exact loader defect and requires real committed append/deletion exercises before a successor calibration freeze. Matrix appends/deletions address that mechanism. S182 is absent from the frozen registry; claims deliberately says it **will** register this source. That is pending source/frontier integration work, not a false claim of a row already present. This review does not certify later registry curation, census, mistake mining or report completeness. Historical r73 rejection remains unchanged (`SCORECARD.md:3338-3342`); successor success cannot retroactively admit it.

## Residual risk / verification gaps

No technical blocker found to the narrow nine-text-case numeric loader result plus historical landing result. The medium procedural finding remains a separate admission consideration for the canonical integrator. Fixed fixtures do not prove general semantic correctness, hostile-counter resistance, binary handling, every Git configuration or every setup failure. Inherited substring checks remain intentionally uncertified. Frozen control receipts were inspected, not rerun; this seat did not execute the full matrix, full battery, preflight, build or lint.

LSP was unavailable: `xd://lsp` returned `No such tool`; caller/definition review therefore used the actual source and frozen Git comparison, not semantic-reference claims. No installs, network, fixture Git mutation, clone or scratch directory were used; no scratch cleanup was required. Writes were confined to the named report and seat receipt folder.

Self-evaluation (1–5): accuracy 4 (static fallback inference explicitly labelled); completeness 4 (matrix execution intentionally delegated to other assigned seats); clarity 4 (formal obligation distinguished from technical scope); actionability 4 (criterion disposition is integrator-owned); conciseness 4 (audit evidence retained). Overall 4.0. Best improvement: attach any already-frozen qualifying detection-forger receipt if the canonical integrator locates one; do not reinterpret this review as non-author admission.
