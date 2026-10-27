# R56 C2 counter review

## Finding — quote uniqueness is not measured (contract gap)

The R56 assignment requires each located quote to occur **exactly once** in its defined form. The frozen sentence in `claims.md` lines 109–119 and the `c2-count.py` docstring (identical after whitespace normalization: 374 words each) do not state that requirement. The counter checks quote length and containment, then verifies that the span is a slice at the recorded offset (`c2-count.py:255–266`); it never counts the quote occurrences in the defined form. `quote-substance-check.py:9–14,49–64` checks substance and span width, not uniqueness. `inference-ground.py:203–223` loads cited span text and ignores the manifest quote field.

[INFERENCE] A quote duplicated elsewhere in a document can still satisfy the checked slice/anchor conditions; C2 would not establish the assignment's exactly-once condition. This is a measurement/contract gap against the frozen claim, not a proposal to alter the frozen predicate. No patch made.

## Same-sentence and constants audit

- Claims C2 predicate: `claims.md:89–120`; counter docstring: `c2-count.py:2–61`. Normalized predicate comparison: `claims_words=374 docstring_words=374 identical=True`.
- `BASE_REV` is `e5a3795191601797613eb986b36fa0b1a73fe6a1` (`c2-count.py:65`), matching the frozen base. The counter file is unchanged since freeze commit `41c58925580af6be22049f13cfde234c5475b858` (`git diff ... -- corpus/evidence/round56/c2-count.py` produced 0 lines).
- `DOCS` mappings and `MUST_BIND = STD` are at `c2-count.py:70–85`; `key()` derives SHA-256(URL)[:24] at lines 137–138. Computed keys matched all assigned keys and each `.txt`/`.raw` capture existed: STD `b27ffd2f0161104c6a28c9f5`, NOTE `de9f5afc3809acbf61f4d5bb`, JRN `5233bf47babaa1ca2b49ed15`, NHC `a42feae4448612f949cc715f`, QCG `16fe8487aa97b98576a0dbac`. Each raw begins `%PDF`, so the counter correctly selects the `.txt` form for these captures (`defined_raw`, lines 141–142; `form_text`, lines 148–163).
- `HELD = {QCG: "S118"}` (`c2-count.py:74–75`) matches S118's first source-cell URL at `corpus/SOURCES.md:128`; the registry header at line 9 confirms the source/status/opened/anchor/used-by cell layout. S118 occurs once in the BASE_REV Registry.
- `TERMS` is `中国循证医学中心` (`c2-count.py:85`). Ran `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -c 中国循证医学中心 e5a3795191601797613eb986b36fa0b1a73fe6a1 -- corpus/knowledge`; observed no matches, exit 1, as required.

## Controls replay

Ran `python3 .../controls/build-c2-controls.py $S/ctl`, then `python3 .../c2-count.py --root $S/ctl/staged` and `--root $S/ctl/rewrite` (C2 counter has no `--work` option). Both outputs and exit codes matched `controls/c2-controls.txt` exactly:

- STAGED: `BOUND=0/4`, `REF_ID_UNBOUND=3`, `C2=FAIL`, exit 1; `STAGED_RECEIPT_MATCH=True`.
- REWRITE: `BOUND=3/4`, `BOUND_IDS=S128,S129,S130 GUIDELINE_BOUND=no`, `C2=FAIL`, exit 1; `REWRITE_RECEIPT_MATCH=True`.

Also reproduced `controls/c2-before.txt` against a scratch extraction of BASE_REV: `ENTRIES=0/1`, `BOUND=0/4`, `C2=FAIL`, exit 1; `BEFORE_RECEIPT_MATCH=True`.

## Verification gap and verdict

No `lsp` device/status is exposed in this session; source inspection and literal searches were used as fallback, not semantic LSP proof. I did not run the lane's after-measurement/candidate counter; this seat replayed only the C2 controls and freeze baseline.

VERDICT: R56-C2 counter/docstring audit and controls replay — controls reproduced; exactly-once quote uniqueness remains unverified by the frozen predicate/counter.
