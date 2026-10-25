# MutC3Entries — C3 (depth) adopted-entry mutation probe

Seat: `L1Chousa45.MutC3Entries` (mutation-tester, leaf). Round 45 wave 2, FALSIFY.
Target: C3 counter `corpus/evidence/round45/c3-count.py` (default mode) and the adopted entries
`corpus/knowledge/evidence-archive-field-policy-r41.md` (FIELD) and
`corpus/knowledge/evidence-snapshot-coverage-r40.md` (SNAP) at lane commit
`5e8c7ad2f7b8254d83358820286e3d12ca4672d1`.

## Method

- Measured over committed bytes: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 5e8c7ad... | tar -x -C /tmp/chousa-r45-MutC3Entries/tree`.
- Baseline (pristine tree, default mode, real cache `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`):
  `python3 corpus/evidence/round45/c3-count.py --root .` → `ENTRIES=2/2 CITES_BOUND=3/3 QUOTES_IN_SPAN=4/4 QUOTES_IN_ENTRY=4/4 COUNTS_IN_ENTRY=7/7 CAPTURE_BOUND=4/4 COUNTS_REDERIVED=7/7 C3=PASS`, exit 0. Baseline is clean; each kill below is conclusive.
- Four scratch copies (m1–m4), one mutation each, rerun identical detector. All four killed (C3=FAIL, exit 1). No survivor. No lane/git/jj/fleet/campaign writes; no fetches; cache read-only.

## Mutants (each adopted, each killed)

### M1 — remove one of the four quotes from FIELD
- Mutation: deleted `"An archive.org link for the source url"` from FIELD line 11.
- Detector output (default): `ENTRIES=2/2 CITES_BOUND=3/3 QUOTES_IN_SPAN=4/4 QUOTES_IN_ENTRY=3/4 COUNTS_IN_ENTRY=7/7 CAPTURE_BOUND=4/4 COUNTS_REDERIVED=7/7 C3=FAIL`, exit 1.
- Caught by **QUOTES_IN_ENTRY** (3/4; the only count that drops). QUOTES_IN_SPAN/CAPTURE_BOUND stay 4/4 (span files and captures untouched).
- Pointers: FIELD line 11 (mutated file sha256 `92c73cd1412785092adb0f0bdf8193413a605d1cd8c2f6379b864c24525b35b5`; pristine `0b6fa57357317a5324719af599d7b6955f99ff67dc87cc7ecc2915b24a933fa5`). Quote `An archive.org link for the source url` = spans.tsv row S082-1.

### M2 — change `1,386` → `1,387` everywhere in SNAP
- Mutation: both occurrences (SNAP lines 16 and 20) `1,386` → `1,387` (grep confirms exactly two before, zero `1,386` after).
- Detector output: `ENTRIES=2/2 CITES_BOUND=3/3 QUOTES_IN_SPAN=4/4 QUOTES_IN_ENTRY=4/4 COUNTS_IN_ENTRY=6/7 CAPTURE_BOUND=4/4 COUNTS_REDERIVED=7/7 C3=FAIL`, exit 1.
- Caught by **COUNTS_IN_ENTRY** (6/7; only count that drops). COUNTS_REDERIVED stays 7/7 (re-derivation reads train.json capture, not SNAP text).
- Pointers: SNAP lines 16, 20 (mutated sha256 `36270796485293a04898e96a50d767fa99bb5fea247361c68ac84c110508724a`; pristine `9de48f81b0e491a4c12ac414f0f2849cb2c73972cc3d614e07c13eb1c6c6d38f`). Key `claims_empty`=1386 in counts.json (`corpus/evidence/round45/counts.json:14`).

### M3 — swap URLs of the two `source:` lines in FIELD
- Mutation: FIELD line 3 (S082) ↔ line 4 (S083) URLs swapped (README ↔ arxiv v3).
- Detector output: `ENTRIES=2/2 CITES_BOUND=1/3 QUOTES_IN_SPAN=4/4 QUOTES_IN_ENTRY=4/4 COUNTS_IN_ENTRY=7/7 CAPTURE_BOUND=4/4 COUNTS_REDERIVED=7/7 C3=FAIL`, exit 1.
- Caught by **CITES_BOUND** (1/3: S082 and S083 bindings both fail `^source:\s*S0XX\s+—\s+<expected url>`; S084 unaffected).
- Pointers: FIELD lines 3–4 (mutated sha256 `155bd4ef372948d3c3514e77623eceae67e117b86aadb0c87f9a7014e364ffa4`; pristine as M1).

### M4 — change S084 row status to `queued`
- Mutation: `corpus/SOURCES.md` row S084 status cell `mined` → `queued` (line 94 only).
- Detector output: `ENTRIES=2/2 CITES_BOUND=2/3 QUOTES_IN_SPAN=4/4 QUOTES_IN_ENTRY=4/4 COUNTS_IN_ENTRY=7/7 CAPTURE_BOUND=4/4 COUNTS_REDERIVED=7/7 C3=FAIL`, exit 1.
- Caught by **CITES_BOUND** (2/3: S084 row fails `row[7] == "mined"`; S082/S083 rows still pass).
- Pointers: SOURCES.md line 94 (mutated sha256 `ff8ff646eeea1299c10b8bcacde853e3f3aab7a7ad9d4c410fb42e0411b32d16`; pristine `1b53080660abcc64b79c6421fb3280ef5b7acc2836c3804bb9db1ece1149d384`).

## Verdict

All four mutations are killed; zero survivors. Claim R45-C3 (default mode) holds against all four
one-change defects. Each mutation is caught by exactly the count that was designed for it:
QUOTES_IN_ENTRY (M1), COUNTS_IN_ENTRY (M2), CITES_BOUND (M3, M4). No count misfires on another
mutation; all other counts remain at target in every run. No tool installs performed.
Scratch `/tmp/chousa-r45-MutC3Entries/` removed.