# MutC3Mutants — mutation test of c3-count.py (round 45, wave 1)

Seat: L1Chousa45.MutC3Mutants (mutation-tester, leaf). Target: the frozen C3
counter `corpus/evidence/round45/c3-count.py` (claims.md R45-C3). No production
lane file was written; everything ran on scratch clones under
`/tmp/chousa-r45-MutC3Mutants/` (deleted at the end of this seat).

## 1. Minimal passing tree (baseline)

Built with `--root /tmp/chousa-r45-MutC3Mutants` from the REAL on-disk
captures in `~shokuknow/.ufo/waves/corpus-expansion-1/.qcache` (no fetch):

- `corpus/knowledge/evidence-archive-field-policy-r41.md` — re-grounded from
  the staged entry: `source: S082 — <README URL>` and `source: S083 —
  <PAPER URL>`; carries the four quotes verbatim.
- `corpus/knowledge/evidence-snapshot-coverage-r40.md` — re-grounded from the
  staged entry: `source: S084 — <TRAIN URL>`; carries the seven count figures.
- `corpus/SOURCES.md` — a `## Registry` section with rows S082/S083/S084
  (11 columns, `mined`, used-by = citing entry paths).
- `corpus/evidence/round45/spans.tsv` — header + 4 rows, 7 tab columns
  (id url capture_sha256 offset span_file quote entry).
- `corpus/evidence/round45/spans/s082-a.txt|s082-b.txt|s083-a.txt|s083-b.txt`
  — each span file == the exact quote text (no trailing newline).
- `corpus/evidence/round45/counts.json` — url=TRAIN,
  capture_sha256=ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c,
  counts = re-derived from the train capture (records 3068, evidence_with_field
  6511, evidence_nonempty 6510, evidence_empty 1, claims_with_field 2531,
  claims_nonempty 1145, claims_empty 1386).

Capture file sha256 (real cache): README ce16d572… file
8e1f5bff76c14672de04987fcaa6a0fcecfbb493f4c2b6c8f1c3443d91989fe5; paper
412b146a… file a3ff65e0db9cc4f2178932ce53965e4cba60c6aab0ba3b1d4ce40020a8a7cf8f;
train 974299ae… file ae5eda7c… (matches claims.md). Quote offsets verified by
`.find()`: README 1027 and 1969, paper 14575 and 120884.

Baseline, default mode:

```
$ python3 corpus/evidence/round45/c3-count.py --root /tmp/chousa-r45-MutC3Mutants
ENTRIES=2/2
CITES_BOUND=3/3
QUOTES_IN_SPAN=4/4
QUOTES_IN_ENTRY=4/4
COUNTS_IN_ENTRY=7/7
CAPTURE_BOUND=4/4
COUNTS_REDERIVED=7/7
C3=PASS
exit=0
```

Baseline, --lane-only:

```
ENTRIES=2/2
CITES_BOUND=3/3
QUOTES_IN_SPAN=4/4
QUOTES_IN_ENTRY=4/4
COUNTS_IN_ENTRY=7/7
CAPTURE_BOUND=skipped
COUNTS_REDERIVED=skipped
C3=PASS
exit=0
```

## 2. Mutations (one defect each; each applied to a fresh `cp -r` clone)

| # | defect (file, cell) | default | lane-only |
|---|---|---|---|
| M1 | row URL changed (SOURCES.md S083 url → v4) | KILLED | KILLED |
| M2 | row status `queued` (SOURCES.md S084) | KILLED | KILLED |
| M3 | used-by missing the entry (SOURCES.md S082 → unrelated.md) | KILLED | KILLED |
| M4 | span offset +1 (spans.tsv s083-a 14575→14576) | KILLED | SURVIVED |
| M5 | capture sha256 wrong (spans.tsv s082-a → 64×`a`) | KILLED | SURVIVED |
| M6 | count off by one in the entry (snapshot entry "3,068 records"→"3,069 records", both occurrences) | KILLED | KILLED |
| M7 | entry cites `source: S139` instead of S082 (FIELD entry line 1) | KILLED | KILLED |

Decisive lines, per mutation (default then lane-only):

```
M1 default: CITES_BOUND=2/3 … C3=FAIL exit=1
M1 lane-only: CITES_BOUND=2/3 … C3=FAIL exit=1
M2 default: CITES_BOUND=2/3 … C3=FAIL exit=1
M2 lane-only: CITES_BOUND=2/3 … C3=FAIL exit=1
M3 default: CITES_BOUND=2/3 … C3=FAIL exit=1
M3 lane-only: CITES_BOUND=2/3 … C3=FAIL exit=1
M4 default: CAPTURE_BOUND=3/4 … C3=FAIL exit=1
M4 lane-only: CAPTURE_BOUND=skipped … C3=PASS exit=0
M5 default: CAPTURE_BOUND=3/4 … C3=FAIL exit=1
M5 lane-only: CAPTURE_BOUND=skipped … C3=PASS exit=0
M6 default: COUNTS_IN_ENTRY=6/7 … C3=FAIL exit=1
M6 lane-only: COUNTS_IN_ENTRY=6/7 … C3=FAIL exit=1
M7 default: CITES_BOUND=2/3 … C3=FAIL exit=1
M7 lane-only: CITES_BOUND=2/3 … C3=FAIL exit=1
```

All seven kill the default mode. M4/M5 survive `--lane-only` (the named blind
spot: lane-only skips the capture-bound lines — matches `controls/c3-control-forged-span.txt`).

## 3. Coverage finding (first M6 probe survived)

First M6 probe changed only the source-line occurrence of "3,068 records"
(not the observation-bullet occurrence): default printed `COUNTS_IN_ENTRY=7/7
C3=PASS exit=0` — SURVIVED. The counter checks that each count VALUE appears
somewhere in the snapshot entry, not that the entry's stated total is
consistent with the derived one, so a duplicate correct figure elsewhere in
the entry masks a wrong one. With both occurrences changed, M6 kills. This is
a coverage finding only; no contract change proposed.

## 4. Restoration evidence

- Pristine tree never modified after baseline; each mutation ran on a fresh
  `cp -r` clone (`mut1`…`mut7`); mutated files were written from the pristine
  content with exactly one cell changed.
- Before (pristine) file sha256:
  counts.json 61647234210b778de55904c7b18e0e0c91e22d682a481ea6bb33a17ac298fb1a
  spans/s082-a.txt 15e6fd1d12d16abac3f51cb1c793bd1dce97f53bd5fa9d3b65fc893f2d00c968
  spans/s082-b.txt dd7324c4a21ba4d5fbbc14787e7e0a5246b92c10418804091603e57d727faaf0
  spans/s083-a.txt ccc28b45dcdb7722a24b3c5e1740626d1f09a16361ce54caf1f9f18e0d14ecd3
  spans/s083-b.txt 559e131f86914844aa164d8efa51cb51e16c2f3462bb63214163a621eb6e128f
  spans.tsv d4bcfbddb085e3b2263f4a9ac4f87b97d756ce461454379d24b1d86ee55323d8
  evidence-archive-field-policy-r41.md e21537c15659c9c26718e9490dc5b82821a5e4aa966846817111d5965b94621d
  evidence-snapshot-coverage-r40.md 2e1973856c0e9101aadefb967100086ec37d8b024dfa42317a7d7beaf7e4bdcf
  SOURCES.md e44b29d807a89b4654ab4ed49415cdba41d52088ca621e954b4de49dcce87122
- No lane/git/jj state touched; no tools installed (none needed); no network
  activity (fetch-scope L0 respected).
- Scratch `/tmp/chousa-r45-MutC3Mutants/` removed on seat end.
