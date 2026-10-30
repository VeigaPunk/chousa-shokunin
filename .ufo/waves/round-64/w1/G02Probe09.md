# G02 escaped-underscore fixture probe

## Result
The candidate `corpus/evidence/round64/controls/ref-preflight-v3.py` accepts the escaped-underscore index fixture. This is a mismatch with frozen R64-C1's benign D6 target, which treats markdown-escaped underscores as normalized plain underscores but expressly notes markdown-escaped-underscore valid shape as a v2-era false-positive shape the revised rule must accept. For this exact fixture, the observed PASS is consistent with that target; it does not establish all C1 criteria.

## Exact probe
- Recipe: `.ufo/waves/round-64/w1/G02Probe09/fixture_recipe.py`.
- Fixture contains regular `corpus/knowledge/foo_bar.md` and `corpus/README.md` containing `Knowledge entry: foo\\_bar.md` (one literal backslash before underscore).
- Command: `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/G02Probe09/fixture_recipe.py`
- Output:
  `fixture: knowledge/foo_bar.md; README token: foo\\_bar.md`
  `observed: PASS 1 entries indexed`
  `exit: 0`
- Exit status: 0.

The isolated fixture directory was `/fast/scratch/hyaku/chousa-r64/G02Probe09/fixture`; candidate bytes were not edited. No tools were installed or updated.