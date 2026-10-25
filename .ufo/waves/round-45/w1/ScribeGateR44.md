# Round 44 Gates row — scoped findings

Item: draft one Gates row for round-44 gate entry points, grounded in claims, counter help/docstrings, scorecard verdict, LOG, and lesson; run each listed counter and capture outcomes. No SKILL.md or production files edited.

## Proposed row

```text
| `research-gate round-44 counters` | gate | `python3 corpus/evidence/round44/c1-count.py` · `python3 corpus/evidence/round44/c2-count.py` · `python3 corpus/evidence/round44/c3-count.py` · `python3 corpus/evidence/round44/errata-count.py --file PATH` | C1 exit 0: `N_SPAWNED=64/64 N_REAPED=64/64 PARENT_PID_MATCH=1/1 ZERO_PIDS=0 NAMES_MATCH=64/64 C1=PASS`; exit 1 otherwise; exit 2 usage/env. C2 exit 0: `CONSISTENT=39/39 REVERIFIED=36/36 LEFT_NAMED=3/3 C2=PASS`; exit 1 otherwise; exit 2 usage/env. C3 exit 0: `ENTRY_CITES=1/1 QUOTE_LOCATED=1/1 URL_MATCH=1/1 C3=PASS`; exit 1 otherwise; exit 2 usage/env; D1: reads an untracked campaign capture path, not reproducible from the lane tree alone. Errata exit 0 iff `ERRATA_COUNT=PASS` (positive count; observed `ERRATA=2`); exit 1 iff zero (`ERRATA=0 ERRATA_COUNT=FAIL`); exit 2 usage/missing file. No superseding counter observed. | C1 do-nothing missing receipt, `controls/pids0.receipt`, `controls/prose.receipt` (each exit 1); C2 `controls/all-left.tsv` (`REVERIFIED=0/36`, exit 1); C3 `--entry` nonexistent (`C3=FAIL entry-missing`, exit 1); errata `controls/errata-zero.txt` (exit 1) against `controls/errata-two.txt` (exit 0). | claims frozen at `043f19a1db91288947493d9f879e61e7a9f07241`; measured lane HEAD `d82cec904bf0fb8736886b9f17be913c7807427a`; round-44 closure measurement `44aaf33cd37e2583fff13397f5a4b60a011ec1ab` | read-only; counters write no lane receipts | chousa |
```

## Executed commands and outputs

All runs used cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Each output below is verbatim, including the explicit shell exit marker:

```text
$ python3 corpus/evidence/round44/c1-count.py; echo "EXIT=$?"
N_SPAWNED=64/64
N_REAPED=64/64
PARENT_PID_MATCH=1/1
ZERO_PIDS=0
NAMES_MATCH=64/64
C1=PASS
EXIT=0

$ python3 corpus/evidence/round44/c2-count.py; echo "EXIT=$?"
CONSISTENT=39/39
REVERIFIED=36/36
LEFT_NAMED=3/3
C2=PASS
EXIT=0

$ python3 corpus/evidence/round44/c3-count.py; echo "EXIT=$?"
ENTRY_CITES=1/1
QUOTE_LOCATED=1/1
URL_MATCH=1/1
C3=PASS
EXIT=0

$ python3 corpus/evidence/round44/errata-count.py --file corpus/evidence/round44/controls/errata-two.txt; echo "EXIT=$?"
ERRATA=2
ERRATA_COUNT=PASS
EXIT=0

$ python3 corpus/evidence/round44/errata-count.py --file corpus/evidence/round44/controls/errata-zero.txt; echo "EXIT=$?"
ERRATA=0
ERRATA_COUNT=FAIL
EXIT=1
```

## Evidence, gates, and limits

- Claims: `corpus/evidence/round44/claims.md:16-104`; C1 and C2 targets and controls at lines 28-35, 59-63; C3 target/control lines 83-89.
- Counter interfaces: c1 docstring/argparse at `corpus/evidence/round44/c1-count.py:2-14,49-53`; c2 at `corpus/evidence/round44/c2-count.py:2-10,75-79`; c3 at `corpus/evidence/round44/c3-count.py:2-14,42-46`; errata at `corpus/evidence/round44/errata-count.py:2-5,17-20`.
- Round verdict and reported outputs: `SCORECARD.md:2378-2406`; round landing: `LOG.md:1568-1630`; lesson and limits: `corpus/lessons/round-44.md:31-78,140-175`; non-author closure D1/D2: `corpus/lessons/round-44-verifier-spotcheck.md:75-95,152-159`.
- D1 confirmed in closure: C3 hardcodes `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` and its URL-derived capture is untracked/ignored; successful local execution here depended on that external on-disk path. The row explicitly disclaims lane-tree-only reproducibility.
- SCORECARD: C1 operability, C2 calibration, C3 depth each improved; closure says D1 does not harm the depth axis. Errata is a QUALITY 62 demonstration, not a frozen claim counter. Row groups it only to register the requested entry point.
- No counter shown superseded in the requested evidence or checked interfaces; no `-v2`/`-v3` successor observed for these four paths.
- Measured HEAD: `d82cec904bf0fb8736886b9f17be913c7807427a`. Working-tree output also showed three inherited modified paths and untracked round-45 wave artifacts; no action taken on them.
- No tools installed or updated.
- Verification was limited to the five explicitly reported counter invocations. No build, test suite, or lint was run.
