# R96ScribeCorrections receipt — D5 (README evidence pointer after/ vs after-f2/)
# date 2026-11-08 lane root

$ grep -n "evidence/round95" corpus/README.md
1441:| `../tools/search-rerun.py` | Round-95 capability: re-runs each recorded local search expression at the recorded revision (`COUNT_DRIFT`/`SET_DRIFT` = the record is wrong) and over the current tree (`TREE_CHANGED` = the corpus moved); record `fixtures/search-rerun-r95.md` (8 searches, `rev_match=8/8`) | S222; `.ufo/waves/round-95/claims.md`; `corpus/evidence/round95/after/` |
grep_exit=0

$ grep -n "" corpus/README.md | sed -n "1441p"
1441:| `../tools/search-rerun.py` | Round-95 capability: re-runs each recorded local search expression at the recorded revision (`COUNT_DRIFT`/`SET_DRIFT` = the record is wrong) and over the current tree (`TREE_CHANGED` = the corpus moved); record `fixtures/search-rerun-r95.md` (8 searches, `rev_match=8/8`) | S222; `.ufo/waves/round-95/claims.md`; `corpus/evidence/round95/after/` |

$ grep -n "" corpus/README.md | sed -n "1443p"
1443:- `lessons/round-95.md` — S222 admitted (JMLA publisher PDF; the Europe PMC route answered 500 and is a url/unreach Gate record), six mined mistakes; the entry carries 13 located quotes after the wave-forced Amendment 1.

--- headers of every receipt under corpus/evidence/round95/after/ ---
[corpus/evidence/round95/after/c1-controls.txt]
# computed_against F=d6429e02bb4807bdb4cc26cd35f62f3c5c5dc7d2 tree_equals_F_for_measured_paths=yes
[corpus/evidence/round95/after/c1-verify.txt]
# computed_against F=d6429e02bb4807bdb4cc26cd35f62f3c5c5dc7d2 tree_equals_F_for_measured_paths=yes
[corpus/evidence/round95/after/c2-controls.txt]
# computed_against F=d6429e02bb4807bdb4cc26cd35f62f3c5c5dc7d2 tree_equals_F_for_measured_paths=yes
[corpus/evidence/round95/after/c2-gate.txt]
# computed_against F=d6429e02bb4807bdb4cc26cd35f62f3c5c5dc7d2 tree_equals_F_for_measured_paths=yes
[corpus/evidence/round95/after/c2-metadata.txt]
# computed_against F=d6429e02bb4807bdb4cc26cd35f62f3c5c5dc7d2 tree_equals_F_for_measured_paths=yes

--- headers of every receipt under corpus/evidence/round95/after-f2/ ---
[corpus/evidence/round95/after-f2/c1-controls.txt]
# computed_against F=86909f02fdd7d122f42928349e85508a90ba894d tree_equals_F_for_measured_paths=yes
[corpus/evidence/round95/after-f2/c1-mutants.txt]
# computed_against F=86909f02fdd7d122f42928349e85508a90ba894d tree_equals_F_for_measured_paths=yes
[corpus/evidence/round95/after-f2/c1-verify.txt]
# computed_against F=86909f02fdd7d122f42928349e85508a90ba894d tree_equals_F_for_measured_paths=yes
[corpus/evidence/round95/after-f2/c2-controls.txt]
# computed_against F=86909f02fdd7d122f42928349e85508a90ba894d tree_equals_F_for_measured_paths=yes
[corpus/evidence/round95/after-f2/c2-gate.txt]
# computed_against F=86909f02fdd7d122f42928349e85508a90ba894d tree_equals_F_for_measured_paths=yes
[corpus/evidence/round95/after-f2/c2-metadata.txt]
# computed_against F=86909f02fdd7d122f42928349e85508a90ba894d tree_equals_F_for_measured_paths=yes
[corpus/evidence/round95/after-f2/lesson-gate.txt]
# computed_against F=86909f02fdd7d122f42928349e85508a90ba894d tree_equals_F_for_measured_paths=yes

$ grep -rn "records=9\|records=13\|MUTANTS_KILLED" corpus/evidence/round95/after/ corpus/evidence/round95/after-f2/
corpus/evidence/round95/after/c2-gate.txt:13:GATE_RECORDS files=1 records=9 ok=9 fail=0
corpus/evidence/round95/after/c2-controls.txt:4:CASE positive gate_rc=0 meta_rc=0 LQ_BOUND=9/9 records=9 WARRANTS_OK=7/7 ok
corpus/evidence/round95/after-f2/c1-mutants.txt:14:MUTANTS_KILLED=10/10
corpus/evidence/round95/after-f2/c2-gate.txt:17:GATE_RECORDS files=1 records=13 ok=13 fail=0
corpus/evidence/round95/after-f2/c2-controls.txt:4:CASE positive gate_rc=0 meta_rc=0 LQ_BOUND=13/13 records=13 WARRANTS_OK=7/7 WARRANT_TERMS=7/7 LANE_FILLED=7/7 ok
grep_exit=0

$ ls corpus/evidence/round95/after/   (no mutants receipt)
c1-controls.txt
c1-verify.txt
c2-controls.txt
c2-gate.txt
c2-metadata.txt
