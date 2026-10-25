# CritC2Admission — round 45 wave 2

## Axis impact

**Calibration: improve, with a narrow meaning.** The sampled five new Gates rows' verdict labels map to the corresponding counters' print labels, and the committed C2 inventory now reports zero unregistered paths. This is evidence against row-padding with false labels in this sample; it does not make C2 a semantic audit of all rows (the frozen predicate explicitly permits plausible rows with incorrect verdict maps). It is not evidence of an operability or depth change.

## Counterexample / evidence

Measured archive `5e8c7ad2f7b8254d83358820286e3d12ca4672d1` only, extracted under `/tmp/chousa-r45-CritC2Admission/tree` and removed before finish.

Commands and decisive output:

- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 5e8c7ad2f7b8254d83358820286e3d12ca4672d1 | tar -x -C /tmp/chousa-r45-CritC2Admission/tree` → `EXTRACTED`.
- From that tree, `python3 corpus/evidence/round45/c2-count.py --list`:
  ```
  ENTRY_POINTS=54
  GATES_ROWS=30
  REGISTERED=54/54
  UNREGISTERED=0
  C2=PASS
  ```
- Sampled SKILL.md rows 104–108 (r40, r41, r42, r43, r44) and searched each row's cited counter source for each displayed verdict label. Every row's PASS and control labels appeared in its indicated counter: r40 C1/C2 values in round40/c1-count.py and c2-count.py; r41 capture-pin/W04 values in round41/c1-count.py and c2-count.py; r42 slice/quote/reproducibility and verdict/class/reason/flip/vocabulary labels in round42 c1/c2; r43 absent/class/reproducibility and split/vocabulary labels in round43 c1/c2, and citation/quote/URL labels in c3; r44 spawned/reaped/PID/name labels in round44 c1, consistency/reverification/left-named labels in c2, citation/quote/URL in c3, errata labels in errata-count.py. Negative controls sampled likewise appeared in the relevant counter (including `SPLIT_AGREES=14/15`, `CLASS_CONSISTENT=23/24`, and `REVERIFIED=0/36`).
- The row-to-path check also found no sampled row registering an unrelated gate's path: each listed round counter/tool mapped to its own counter source; the r41 `tools/research-gate.sh` is explicitly the gate input, not a counter.

This falsifies the strongest padding hypothesis for these samples: labels are not merely plausible prose invented for a qualifying row; they match emitted counter strings, and the count is a real complete registration under the frozen path-membership rule. Scope limitation: only five of twelve new rows were sampled, as assigned; this does not establish correctness for the remaining seven or all row semantics.

## Verdict and pointers

**C2 calibration verdict: improve** (limited to sampled verdict-map/path coherence and complete registration; no claim that the frozen counter validates truth). Frozen criterion is not changed. The known counter blind spot remains: C2 checks substring membership, not which gate a row semantically describes or whether its verdict map is correct.

- `SKILL.md:104-108` — sampled rows; `SKILL.md:75-78` — row grammar/header. SHA-256 of archived SKILL.md: `ba4e2c9f14c77e92c582e64c31f5466f31b45cb34e68c346038891941a947544`.
- `corpus/evidence/round45/c2-count.py:45-55,70-81` — row parsing, path-substring registration, output; SHA-256 `fdb2019207d294a53666a4eda4fcf5d41a6be45d342e0fe654f72ca82cfe2af5`.
- Frozen scope caveat: `corpus/evidence/round45/claims.md:65-69` says a plausible row with a wrong verdict map still passes and treats it as a reader's check.

No tools installed or updated.