# R50ConnCrossClaim — Cross-claim and cross-fleet synthesis: C1 anti-echo selftest and C2 CJK grounding

Seat: connector (UFO-FSD, leaf, no delegation, godspeed).
Target: cross-fleet gate self-test standards and non-ASCII grounding parity across fleet lanes.
Evidence base: local repository files across /home/vgpnk/Projects/shokunin. No production or foreign lane edits.

## 1. Fleet Gate Standard in PROTOCOL.md vs Sibling Lane Self-Tests
Command: `grep -n "Gate standard" /home/vgpnk/Projects/shokunin/PROTOCOL.md` -> lines 224, 375.
- `PROTOCOL.md:385-389` (§Gate standard, "Self-test"): requires an isolated fixture run asserting
  both exit code and stable finding-ids, with expected values committed in the owning repo.
- `PROTOCOL.md:390-397` (§Gate standard, "Two evidences"): requires `expected.json` pinning snapshot
  input file digests for frozen verdict runs.
- `PROTOCOL.md:370-373` (§Evidence standard, "Drift pins"): baselines persisted in the repo.
- **Finding**: An expected-finding-ids file with a digest pin does NOT appear under "Self-test"
  (`:385-389`); it appears only under "Two evidences" (`:394-397`) and "Drift pins" (`:370-373`).
Sibling lane tools read (`grep -rn -- '--selftest' <tools/scripts>`):
- `kaidoku-shokunin/tools/round-30/axis-fit-gate.py:388-468`: builds in-memory temp git fixtures;
  asserts hardcoded Python lists of exit codes and finding IDs; no external expected file, no digest pin.
- `kake-shokunin/scripts/canonical_audit.py:941-1021`: runs internal cases in tempdir, asserting
  `actual_exit == expected_exit and actual_id == expected_id`; no external expected file, no digest pin.

## 2. C1 Design Evaluation: Matches, Extends, or Contradicts
- In `chousa-shokunin/tools/assimilate-rows.py:44-60, 206-242`, `--selftest` computes `FIXTURES_SHA256`
  (`:206-210`), diffs observed lines against `expected.json`'s `findings` multiset (`:223-237`), and
  outputs `SELFTEST=PASS|FAIL`.
- In `corpus/evidence/round50/c1-count.py:47-49, 83-134`, the counter asserts `digest(FIX) == PIN`
  (`:83-85`), runs baseline, 6 perturbed copies P1–P6 (`:106-124`), unparseable expected file
  (`:127-132`), and scores against do-nothing controls (`controls/echo-tool.py`, `controls/const-tool.py`).
- **Verdict**: C1 **extends** the PROTOCOL.md Gate standard. It satisfies `:385-389`, imports `:394-397`'s
  snapshot digest pinning into the self-test interface (`FIXTURES_SHA256`), and adds perturbation
  testing (P1–P6) to defeat echo controls. It contradicts nothing in PROTOCOL.md.

## 3. Sibling Tools Passing an Echo Control
- `mori-shokunin/tools/mori-gate-registry.py:439-442`: checks gate rows for `--selftest` via regex
  without executing the tool. In its own selftest fixture (`_mk`), the reference passing tool fixture
  `TOOL_OK` (`:464-465`) is literally an echo control:
  `TOOL_OK = ('#!/bin/sh\ncase "${1-}" in\n  --selftest) echo ok; exit 0 ;;\nesac\nexit 0\n')`
  `mori-gate-registry.py` passes this echo control with zero findings (`GATE_REGISTRY_SELFTEST pass=15 fail=0`).
- `souji-shokunin/tools/souji-landing-gate.py:1209, 1271, 1931`: fixtures use `GOOD_SH = "#!/bin/sh\necho ok\n"`,
  verifying syntax (`bash -n`) only.
- In `chousa`, executing `python3 corpus/evidence/round50/c1-count.py --tool controls/echo-tool.py`
  proves that without perturbation testing, an echo control passes `BASELINE=PASS rc=0 findings=26`
  (failing only on P1–P6 `PERTURB_PASS=0/6`).

## 4. Cross-Lane Non-ASCII / CJK Grounding Parity
- `kake-shokunin` maintains a CJK quote-truth gate in `.ufo/waves/round-52/c52_quote_truth.py:135-142`
  (`CJK_RE` with `units()` counting 1 CJK char or 1 Latin whitespace token as 1 unit; 6–40 units in
  round 52, <=25 units in round 55).
- `kake-shokunin` holds an open defect: `kake-shokunin/corpus/QUALITY.md:1133-1144` and
  `corpus/lessons/round-54-verifier-spotcheck.md:D3` note that "their CJK lexical segmentation remains
  unresolved... CJK <=25-word rule remains open" because CJK text lacks whitespace word delimiters.
- `chousa-shokunin/tools/inference-ground.py:88-98` (QUALITY criterion 79, `corpus/QUALITY.md:832-843`)
  solves this: `has_two_words()` defines 4 CJK characters as the equivalent of "two words"
  (`len(CJK_RE.findall(s)) >= 4`).

## 5. Synthesis Proposal: Two Cross-Fleet Bridges
- **Proposed Move**: Standardize two cross-fleet primitives into `PROTOCOL.md`:
  1) **Anti-Echo Gate Standard**: Extend `PROTOCOL.md:385-389` to require that gate self-tests
     demonstrate perturbation sensitivity or negative control rejection (codified in chousa `QUALITY 73`),
     closing the echo-tool vulnerability in `mori-gate-registry.py` and `souji-landing-gate.py`.
  2) **CJK Word-Cap Parity**: Share `chousa`'s 2-CJK-char-per-word floor (`inference-ground.py:97`)
     with `kake-shokunin` and `kotodama-shokunin` (which noted in `round-72.md` that CJK quotes evaluate
     to 1 token under `wc -w`), resolving `kake`'s open `CORPUS.md` rule 1 defect as `min(25 words, 50 CJK chars)`.
- **Affected Axes**: Improves `operability` (gate selftest discrimination) and `depth` (multilingual
  grounding parity); harms none.
- **Risks**: Increased test maintenance for lanes adding perturbation fixtures; 2:1 character ratio is
  an approximation that defers full morphological segmentation (Jieba/MeCab), but conservatively bounds quote length.
- **Verification**:
  - `python3 corpus/evidence/round50/c1-count.py` -> `LEGS=5/5 C1=PASS`.
  - `python3 corpus/evidence/round50/c1-count.py --tool controls/echo-tool.py` -> `BASELINE=PASS`, `PERTURB_PASS=0/6`, `C1=FAIL`.
  - `python3 corpus/evidence/round50/cjk-ground-check.py` -> `CJK_GROUND=PASS`.

VERDICT: Attacked fleet gate selftest standard and cross-lane CJK grounding parity; survived with cross-fleet synthesis proposal closing echo-tool vulnerability and kake-shokunin CJK word-cap defect.
