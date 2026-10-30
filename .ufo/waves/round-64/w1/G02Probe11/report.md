# G02 NFC/NFD fixture probe

Candidate: `corpus/evidence/round64/controls/ref-preflight-v3.py` (read-only; not production). Frozen reference: C1 claims lines 53–56 specify NFC normalization on both README and filename before matching; the named D8 leg is NFC-file/NFD-index (lines 95–99).

Recipe: `recipe.json`; isolated fixture under `/fast/scratch/hyaku/chousa-r64/G02Probe11/fixture`. The knowledge entry is NFC `café.md`; the README index token uses NFD `café.md`.

Command: `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round64/controls/ref-preflight-v3.py --root /fast/scratch/hyaku/chousa-r64/G02Probe11/fixture --fleet /nonexistent --work /fast/scratch/hyaku/chousa-r64/G02Probe11/work --only G02`

Observed exit: **0**. Stdout: `GATE G01 census SKIP`; `GATE G02 knowledge-index PASS 1 entries indexed`; G03–G08 SKIP; `PREFLIGHT=1/1 FAILED=none ENV=none SKIPPED=G01,G03,G04,G05,G06,G07,G08`. Stderr empty.

Assessment: observed result matches the frozen NFC/NFD contract for this direction. This is one bounded fixture, not a full C1 battery or production verification. No tools installed or updated.
