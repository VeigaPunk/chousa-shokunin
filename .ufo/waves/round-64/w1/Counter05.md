# Counter05 — round 64 C1 frozen digest pins

Compared the seven paths pinned in frozen claims § “Frozen instruments, digests and receipts” against their current original lane bytes with `sha256sum` from the lane root. No fixture, instrument, or production file was changed. The current digest prefixes match all seven frozen pins exactly.

Observed command:

```text
sha256sum corpus/evidence/round64/c1-battery-v3.py corpus/evidence/round64/gen-audit-mutants.py corpus/evidence/round64/c2-mutrun.py corpus/evidence/round64/c3-count.py corpus/evidence/round64/run-receipts-v3.py corpus/evidence/round64/controls/root-shift-mutant.py tools/claims-audit-v2.py
```

Complete stdout (stderr was empty):

```text
4b3f0b658bcd3bb640cd2e6e56a28a91a72d5352f2610887db01e636fc039fe2  corpus/evidence/round64/c1-battery-v3.py
6e1055b28d315e32a3d43ee0866f9c32b78470899826f1d29c8c3707610a4191  corpus/evidence/round64/gen-audit-mutants.py
0045787ee9de39749e1dd06739259cd5f0a494865c921edbed91cfd86249a8c9  corpus/evidence/round64/c2-mutrun.py
465a8c5efbb870f73c7c6306c813c4fe35f4ccaf5a996a56ab71d4da5feec682  corpus/evidence/round64/c3-count.py
0f3cfae75f711f17251174a2e123321040c91394497bafe4a64c9148d7c3abd7  corpus/evidence/round64/run-receipts-v3.py
f0f9b26083ff62c35b9d54fe5bf7733f233c496368a5a62a3da02dbbb3f89175  corpus/evidence/round64/controls/root-shift-mutant.py
db0e28dd4c0332591b8898feb727f23a0e80b6e2ad29cbf0a6237d35a4d0b88d  tools/claims-audit-v2.py
EXIT=0
```

Frozen C1 baseline failure is explicitly retained as written in `corpus/evidence/round64/controls/c1v3-before-full.txt`: `CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL`; the receipt lists E12/E13/E14 benign-leg failures. No post-freeze battery run was part of this digest comparison, and this result does not establish the candidate or supplement's behavior.

Tools installed/updated: none. Scratch: no scratch clone or work directory was needed for this read-only digest comparison.
