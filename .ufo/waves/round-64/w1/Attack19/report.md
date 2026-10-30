# Attack19 — frozen digest and history falsification

Axes: calibration (provenance and audit authority), operability (C1 fixture validity), depth (precise evidence boundaries). Advisory review only; no admission or canonical judgment.

## Findings

### 1. Digest substitution attack did not succeed

All seven prefixes in frozen `corpus/evidence/round64/claims.md:263–266` match both committed bytes at `bf40d99bda9eefdad3ed6276da077cfb24ba82f1` and inherited working-tree bytes. The v1 checker also matches its claimed `d48247f9c77ac1e7` prefix. Claims and these eight instruments have no diff against that revision. This establishes byte identity, not behavioral correctness or execution chronology.

| Instrument | Full SHA-256 at freeze and in inherited tree |
|---|---|
| c1-battery-v3.py | 4b3f0b658bcd3bb640cd2e6e56a28a91a72d5352f2610887db01e636fc039fe2 |
| gen-audit-mutants.py | 6e1055b28d315e32a3d43ee0866f9c32b78470899826f1d29c8c3707610a4191 |
| c2-mutrun.py | 0045787ee9de39749e1dd06739259cd5f0a494865c921edbed91cfd86249a8c9 |
| c3-count.py | 465a8c5efbb870f73c7c6306c813c4fe35f4ccaf5a996a56ab71d4da5feec682 |
| run-receipts-v3.py | 0f3cfae75f711f17251174a2e123321040c91394497bafe4a64c9148d7c3abd7 |
| controls/root-shift-mutant.py | f0f9b26083ff62c35b9d54fe5bf7733f233c496368a5a62a3da02dbbb3f89175 |
| tools/claims-audit-v2.py | db0e28dd4c0332591b8898feb727f23a0e80b6e2ad29cbf0a6237d35a4d0b88d |
| tools/claims-audit.py | d48247f9c77ac1e736ae627cd191168b741956982adb948e76c8057df405cb1b |

Committed claims SHA-256: `bab186919f4518f3662c31661d1e2060b4f9f3d186b33d184c365a3f82d7cfc0`; comparison confirms inherited claims unchanged.

### 2. Minimal history counterexample: same-commit instruments were replaced as audit subjects

`git log --diff-filter=A` shows the claims file and all six original R5 subjects first added together in `92a084175f9534296527b77a2b7fe38560b96b18`. This contradicts original R5's explanation that the instruments were in a pre-freeze commit and claims in a separate freeze commit. It does NOT establish that an after-measurement preceded the freeze; git contains no such runtime ordering evidence.

At `bf40d99bda9eefdad3ed6276da077cfb24ba82f1`, `audit/audit-r64.tsv` R5 changed from those six round64 instruments to `corpus/evidence/round63/claims-a2.md,tools/claims-audit.py`. The same commit added the one-line receipt `FLAGGED=0/5 AUDIT=PASS`. The changed row openly acknowledges the same-commit issue, so this is not a hidden claims-file edit. Nevertheless, the green receipt now answers a different provenance question: older round63 subjects cannot establish round64 instrument precedence.

Counterexample needs no new fixture: retain the original R5 subjects and inspect their first-add commit. `tools/claims-audit-v2.py:163–166` explicitly flags subjects whose first-add equals the claims first-add. [INFERENCE] Evaluating the original R5 row against this history would therefore flag R5. I did not execute the checker or create a replacement authority.

Impacted axis: calibration. This is an audit-scope/provenance weakness, not evidence that the frozen C2 twelve-mutant kill rule failed. Smallest safe correction: preserve the historical original R5 failure alongside the openly amended audit result, and state that the latter checks round63 ancestry only. Do not rewrite frozen claims, counters, or retrospectively turn this receipt into round64 chronology proof. A future separately named audit can test an explicitly chosen chronology contract.

### 3. Matching digests preserve C1's known fixture failure; they do not cure it

Frozen `c1-battery-v3.py:386–394` draws `tag()` independently for each created E12/E13 filename and its README reference. The frozen expected outcomes at lines 442–443 are benign exit 0. A distinct generated name in the README is instead an unindexed real file plus a phantom reference, contradicting the frozen G02 contract (`claims.md:55–59`). The committed before-receipt has `LEG E12 benign FAIL rc=1 want 0`, `LEG E13 benign FAIL rc=1 want 0`, and final `CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL`.

Impacted axes: operability and calibration. Smallest safe correction: keep the frozen full-pass failure honest and keep repaired `c1-battery-supplement.py` results distinct. The supplemental repair is not a frozen C1 pass. No new battery execution was necessary or performed; the user-reported defect is ground truth and the frozen source independently exposes its cause.

## Commands and evidence

All shell commands used absolute lane cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`; only read-only git operations and hashing ran.

1. `sha256sum corpus/evidence/round64/{c1-battery-v3.py,gen-audit-mutants.py,c2-mutrun.py,c3-count.py,run-receipts-v3.py,controls/root-shift-mutant.py} tools/claims-audit-v2.py tools/claims-audit.py` — successful output: table above.
2. For each table path and `corpus/evidence/round64/claims.md`: `git show bf40d99bda9eefdad3ed6276da077cfb24ba82f1:PATH | sha256sum` — successful pipeline output: table above and claims hash. These were dispatched concurrently; pipeline status alone is not used as object-existence evidence, since `git ls-tree` separately listed the round64 files.
3. `git diff --exit-code bf40d99bda9eefdad3ed6276da077cfb24ba82f1 -- corpus/evidence/round64/claims.md corpus/evidence/round64/c1-battery-v3.py corpus/evidence/round64/gen-audit-mutants.py corpus/evidence/round64/c2-mutrun.py corpus/evidence/round64/c3-count.py corpus/evidence/round64/run-receipts-v3.py corpus/evidence/round64/controls/root-shift-mutant.py tools/claims-audit-v2.py tools/claims-audit.py && printf 'FREEZE_BYTES_UNCHANGED EXIT=0\n'` — output `FREEZE_BYTES_UNCHANGED EXIT=0`; exit 0.
4. `git log --diff-filter=A --format='%H %s' --name-only -- corpus/evidence/round64/claims.md corpus/evidence/round64/c1-battery-v3.py tools/claims-audit-v2.py corpus/evidence/round64/c2-mutrun.py corpus/evidence/round64/c3-count.py corpus/evidence/round64/run-receipts-v3.py corpus/evidence/round64/gen-audit-mutants.py && printf 'HISTORY_READ EXIT=0\n'` — output one first-add commit `92a084175f9534296527b77a2b7fe38560b96b18`, all seven requested paths, `HISTORY_READ EXIT=0`; exit 0.
5. `git show bf40d99bda9eefdad3ed6276da077cfb24ba82f1 -- corpus/evidence/round64/audit/audit-r64.tsv corpus/evidence/round64/audit/audit-r64-postfreeze.txt` — successful output: R5 subject substitution and added PASS receipt described above.
6. `git log -3 --format='%H %s' --name-status -- corpus/evidence/round64 tools/claims-audit.py tools/claims-audit-v2.py tools/lane-preflight.py` — successful output: later `34cbd847fa374ce7baa61147209b5772212a3d64` adds the separately named supplement and erratum, modifies production preflight, and does not list frozen counter changes. Candidate identity is not inferred from the production modification.

No claims, operator inputs, counters, production files, sibling files, git state, or PATH directories changed. No network, installs, clone, scratch tree, battery runs, or other runtime invocation. Scratch cleanup is vacuous: this seat created no scratch directory. No tool installation/update to record.

Self-evaluation: accuracy 4/5 (runtime chronology intentionally not inferred); completeness 4/5 (scoped byte/history review, not independent battery execution); clarity 4/5 (full digest table retained for auditability); actionability 4/5 (small correction specified without changing authority); conciseness 4/5 (commands retained to make evidence reproducible). Overall 4.0/5. Highest-impact improvement belongs to L1: retain the original R5 failure explicitly, and label the amended audit's narrower subjects. The user should agree with these stated evidence boundaries.
