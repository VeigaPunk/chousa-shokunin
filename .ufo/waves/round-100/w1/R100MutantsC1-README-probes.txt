Seat R100MutantsC1 receipt index (scratch /fast/scratch/hyaku/chousa-r100/R100MutantsC1)
- gen_mutants.py: 38 tool mutants (each site asserted exactly once by count==1 in script)
- gen_batt_mutants.py: 12 battery mutants (b7 fixed to single-line count fix)
- probe_multi.py / probe_txtwins.py: advisory probes (final cache proof was run inline against c2proj/two.md)
- muts/tool-results.txt + tool-results-2.txt: 38 tool mutant battery runs (--tool <mutant> --no-oracles)
- muts/batt-results.txt + batt-results-rest.txt: 12 battery mutants run vs F tool (with oracles) and vs base tool
- pristine-r100.txt: pristine F battery PASS (full oracles)
- base-noor.txt: base tool --no-oracles FAIL REV=3/11 PROD=4/6
- c2proj + cproot + two.md: two-rev cache divergence proof (full tool vs n-cache-repoonly)
- repo/ : shared clone at F 6d4e8487 (never mutated; sha256 a40505d8 tools/gate-records.py matches F)
Manifest prints: m_drop 11, new code 21, r99 rules 6 = 38 total.
Verdicts: TOOL KILLED 30, SURVIVED 8 eligible next.
BATT: 12 tested; F-PASS survivors: b1,b3,b4,b5,b6,b7,b9 (7); killed b2,b8,b10,b11; b12 also F-PASS (8 survivors). Base FAIL for all 12.
