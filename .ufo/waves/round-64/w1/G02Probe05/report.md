# G02 nested knowledge probe

- **Command:** isolated Python fixture driver imported `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round64/controls/ref-preflight-v3.py` and invoked `g02` directly. Exit reported by driver: `0` for PASS.
- **Fixture:** `corpus/knowledge/top.md` plus `corpus/knowledge/sub/nested.md`; README mentioned both basenames without `knowledge/` prefix.
- **Observed:** `PASS`, `2 entries indexed`.
- **Frozen contract:** claims.md R64-C1 (lines 47–61) requires recursive knowledge walk and basename-level token matching; README path prefix is allowed but never required. Therefore the observed PASS conforms.
- **Negative control:** retained both files, removed `nested.md` from README; observed `FAIL`, `1 not named in corpus/README.md: nested.md`, consistent with the expected missing-index failure.
- **Evidence/recipe:** `nested-knowledge-fixture.json` beside this report. Candidate left unchanged. Probe limited to nested-path indexing; no broader claims about C1 or candidate status.
- **Tool installs:** none.
- **Scratch:** fixture was created under `/fast/scratch/hyaku/chousa-r64/G02Probe05/`; this worker did not remove it.
