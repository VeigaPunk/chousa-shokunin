# R96ScribeCorrections — append-only corrections owed from the round-95 non-author spot-check

Seat `R96ScribeCorrections` (leaf, scribe). Source of the defects:
`corpus/lessons/round-95-verifier-spotcheck.md`, section **6 "Routed defects"** items **D2, D3, D5** and
section **7's revised D4** (the closure's second non-author pass). D1 is out of this seat's assignment
(it is taken by round 96's C1 and is already landed in `SKILL.md:180` at the round-96 freeze).

Every defect below was re-opened by this seat against committed bytes at the lane root
`/home/vgpnk/Projects/shokunin/chousa-shokunin` (HEAD `2db151c5`, the round-96 claim freeze F), and the
round-95 landing `07e0e332` was cloned into this seat's scratch
`/fast/scratch/hyaku/chousa-r96/R96ScribeCorrections/repo-r95` to re-measure the two round-94 counters the
round-95 report and SCORECARD name. **No original text is rewritten.** These are the append-only correction
entries owed in `LOG.md` (the lane's existing convention for routed-defect corrections: `LOG.md:2767-2785`
carries the eight round-94 spot-check corrections in exactly this shape).

The exact commands and their observed output, with exit codes, are in the receipts copied beside this
draft under `.ufo/waves/round-96/w1/` as `R96ScribeCorrections-*.txt`:

| receipt | covers |
|---|---|
| `R96ScribeCorrections-D2-lesson-nine-quotes.txt` | D2 |
| `R96ScribeCorrections-D3-r94-counter-receipts.txt` | D3 |
| `R96ScribeCorrections-D3b-counters-r95-landing.txt` | D3 (independent re-measurement) |
| `R96ScribeCorrections-D3c-counters-r96-freeze.txt` | D3 (independent re-measurement, r96 freeze tree) |
| `R96ScribeCorrections-D4-locator-external-confirmation.txt` | D4 |
| `R96ScribeCorrections-D5-readme-evidence-pointer.txt` | D5 |

---

## Draft correction bullets

- Correction (r95 spot-check D2): `corpus/lessons/round-95.md:23` says "C2's entry holds nine located
  quotes from this capture."; the record is "thirteen" — the entry `corpus/knowledge/search-rerun-record-r95.md`
  holds 13 located quotes and 13 Gate records at every revision from the wave-forced re-freeze onward
  (`git show 86909f02:corpus/knowledge/search-rerun-record-r95.md | grep -c '^| Q'` → `13`, exit 0;
  `git show 86909f02:corpus/knowledge/search-rerun-record-r95.md | grep -c '^GATE-RECORD'` → `13`, exit 0;
  the landing receipt `corpus/evidence/round95/after-f2/c2-gate.txt:17` prints
  `GATE_RECORDS files=1 records=13 ok=13 fail=0`, and a re-run now at the round-96 freeze exits 0 with the
  same line). The stale count was never correct at any committed revision of the lesson: the lesson file did
  not exist at freeze F `d6429e02` (`git cat-file -e d6429e02:corpus/lessons/round-95.md` → exit 128, "fatal:
  path … exists on disk, but not in 'd6429e02'") and was born at F2 `86909f02`, the very commit that carried
  the entry's 13 quotes (`git show 86909f02:corpus/lessons/round-95.md | sed -n '23p'` → the same "nine"
  sentence). The lane's own `corpus/README.md:1443` already says "the entry carries 13 located quotes after
  the wave-forced Amendment 1", so the lesson and the README disagree inside the same round. The F-measured
  receipt `corpus/evidence/round95/after/c2-gate.txt:13` does print `GATE_RECORDS files=1 records=9 ok=9
  fail=0` — that is the count at F, before Amendment 1, not at the lesson's own revision. The original text
  stays." (evidence: `.ufo/waves/round-96/w1/R96ScribeCorrections-D2-lesson-nine-quotes.txt`.)

- Correction (r95 spot-check D3): `.ufo/reports/round-95/chousa.md:95-96` (fleet repo
  `/home/vgpnk/Projects/shokunin`) says "No axis harmed: `git diff --quiet 7b237358 07e0e332 -- tools/research-gate.sh
  tools/gate-records.py PROVINCE.md` exit 0; on the landing tree `SKILL_TALLY_R94=PASS` and `CURATION_R94=PASS`.",
  and `SCORECARD.md:4258-4259` (lane) says "No axis harmed: `tools/research-gate.sh` and `tools/gate-records.py`
  are byte-identical at base and landing; the r94 counters still pass on the landing tree
  (`SKILL_TALLY_R94=PASS`, `CURATION_R94=PASS`)"; the record is "no round-95 receipt carries either verdict.
  `grep -rl 'SKILL_TALLY_R94' corpus/evidence/round95/` → exit 1, no match; `grep -rl 'CURATION_R94'
  corpus/evidence/round95/` → exit 1, no match; the exhaustive `grep -rl 'SKILL_TALLY_R94\|CURATION_R94'
  corpus/evidence/` returns only round-94 files (`corpus/evidence/round94/after/c2-counter.txt`,
  `…/c3-counter.txt`, the two `*-r94.py` instruments and their `__pycache__`); the two receipt files are
  headed `# computed_against F=ebbcbe396ac9a6352134cae8232968c9cf068c30
  C=d13c2ff24dc8d866239a7428e78ccb82b3817018` — the round-94 freeze, not the round-95 landing — and the
  `*-r94.py` files are the instruments themselves, not receipts. The only
  round-95-tree file that mentions the string is `.ufo/waves/round-95/w1/R95ScribeCorrections-D2-log.md-stale.txt`,
  which quotes the round-94 `LOG.md` prose and prints no verdict line of its own
  (`grep -c '^SKILL_TALLY_R94=' …` → `0`). The two counters do in fact pass on the round-95 landing tree —
  re-measured by this seat in a scratch clone of `07e0e332`: `python3 -B
  corpus/evidence/round94/skill-tally-r94.py --root .` → `… TAIL_OK=1 LEGS=4/4` / `SKILL_TALLY_R94=PASS`,
  exit 0, and `python3 -B corpus/evidence/round94/curation-r94.py --root .` → `… LEGS_MEASURED=16/16` /
  `VERDICT fields_hold=1 legs_ok=16/16 DETECTOR_WITNESS=18/18` / `CURATION_R94=PASS`, exit 0 (the same two
  runs on the round-96 freeze tree `2db151c5` also exit 0 with both PASS). So the sentence's values are
  true and its citation is missing: the verdicts were asserted on the landing tree with no landing-tree
  receipt behind them. The harm verdict rests on the lane's own diff, not on these two counters. The original
  text stays." (evidence: `.ufo/waves/round-96/w1/R96ScribeCorrections-D3-r94-counter-receipts.txt`,
  `…-D3b-counters-r95-landing.txt`, `…-D3c-counters-r96-freeze.txt`.)

- Correction (r95 spot-check D4, revised by the round-95 closure's second pass at
  `corpus/lessons/round-95-verifier-spotcheck.md:180-183`): `corpus/lessons/round-95.md:39-41` says "the
  volume/article locator `10:39` came from the round's web-search summary, not from the capture. Read the cell
  as 'co-published in Systematic Reviews (doi 10.1186/s13643-020-01542-z)'."; the record is "the locator is
  true and only unsupported by the lane's own capture. The round-95 closure re-opened the Europe PMC REST
  full-text XML for PMC7839230 and read `<volume>10</volume>` and `<elocation-id>39</elocation-id>` out of the
  Systematic Reviews front matter (`corpus/lessons/round-95-verifier-spotcheck.md:180-183`), and this seat
  re-opened the same URL read-only into its own scratch and got the same elements on its third attempt
  (`attempt=1 http=500 size=150`, `attempt=2 http=500 size=150`, `attempt=3 http=200 size=226044`;
  `grep -o '<journal-title>[^<]*</journal-title>\|<volume>[^<]*</volume>\|<elocation-id>[^<]*</elocation-id>'`
  → `<journal-title>Systematic Reviews</journal-title>`, `<volume>10</volume>`, `<elocation-id>39</elocation-id>`;
  the same file carries `10.1186/s13643-020-01542-z` and the item-8 sentence "copied and pasted exactly as run"
  twice). So the row's "Systematic Reviews 10:39" cell needs an external confirmation, not a superseding row:
  the lane's own two attempts on that URL are recorded as http 500 (`corpus/evidence/round57/refetch.tsv:190`
  attempt 1 at `2026-11-08T22:51:19Z`, `…:193` attempt 2 at `2026-11-09T00:35:48Z`, both `22 500`), so the
  confirmation is reachable only intermittently, and no capture of it exists in the lane
  (`grep -rl 'elocation-id' corpus/captures/*.txt` → exit 1, no match). The provenance note in the lesson
  stands as written; what is owed is the recording of the external confirmation (or a capture of the
  co-publication). The original text stays." (evidence:
  `.ufo/waves/round-96/w1/R96ScribeCorrections-D4-locator-external-confirmation.txt`.)

  **Plan note, not a lane defect:** `plans/round-96.md:46-47` says "the external confirmation of '10:39'
  recorded by the round-95 closure is cited in the lesson, the row is unchanged". At the round-96 freeze that
  is not so — `grep -c 'elocation\|<volume>\|volume>10\|JATS\|fullTextXML\|PMC7839230'
  corpus/lessons/round-95.md` → `2`, and both hits are the route-rejection prose at lines 28 and 32 (the
  http-500 rejection), not a citation of the confirmation; the only file in the lane that carries
  `<elocation-id>39` is `corpus/lessons/round-95-verifier-spotcheck.md`. The plan also asserts the round-96
  lesson's `## Gate` "records the volume/elocation elements found"
  (`corpus/evidence/round96/egress-approval.md:12`), but the round-96 attempt on that URL answered http 500
  (`refetch.tsv:193`) and no round-96 lesson exists at the freeze (`git ls-tree -r --name-only 2db151c5 --
  corpus/lessons/ | grep -i 96` → exit 1). The route is intermittent, so a later attempt may still yield the
  200 this seat saw; nothing at the freeze records one.

- Correction (r95 spot-check D5): `corpus/README.md:1441` says "…record `fixtures/search-rerun-r95.md`
  (8 searches, `rev_match=8/8`) | S222; `.ufo/waves/round-95/claims.md`; `corpus/evidence/round95/after/` |";
  the record is "the numbers live in `corpus/evidence/round95/after-f2/`, not in `after/`". Every receipt under
  `corpus/evidence/round95/after/` is headed `# computed_against F=d6429e02bb4807bdb4cc26cd35f62f3c5c5dc7d2
  tree_equals_F_for_measured_paths=yes` — freeze F — and `after/` holds no mutant receipt at all
  (`ls corpus/evidence/round95/after/` → `c1-controls.txt c1-verify.txt c2-controls.txt c2-gate.txt
  c2-metadata.txt`; `grep -rn 'MUTANTS_KILLED' corpus/evidence/round95/after/` → exit 1, no match). The
  `after/` set reports the pre-amendment numbers: `after/c1-controls.txt` prints
  `POSITIVE=1/1 STRICT_TREE=1/1 FORGERY_REFUSED=8/8 … ORACLES_REJECTED=3/3` where
  `after-f2/c1-controls.txt` prints `FORGERY_REFUSED=10/10 … GREP_AGREE=4/4 CONTAINMENT=2/2 …
  ORACLES_REJECTED=4/4`, and `after/c2-gate.txt:13` prints `GATE_RECORDS files=1 records=9 ok=9 fail=0` where
  `after-f2/c2-gate.txt:17` prints `GATE_RECORDS files=1 records=13 ok=13 fail=0`. The round's headline
  numbers — 13 located quotes, 10/10 mutants, 10/10 forgeries, 4/4 oracles — are in `after-f2/`, whose
  receipts are headed `# computed_against F=86909f02fdd7d122f42928349e85508a90ba894d`, the revision the round
  landed (F2 = landing for the measured paths: `git diff --stat 86909f02 07e0e332 -- tools corpus/fixtures
  corpus/knowledge corpus/evidence/round95/` → exit 0, and the only lines it prints are the seven `after-f2/`
  additions plus `corpus/evidence/round95/census-end.txt`; `tools/`, `corpus/fixtures/` and
  `corpus/knowledge/` are byte-identical between F2 and the landing). `SKILL.md:179`
  already points at `corpus/evidence/round95/after-f2/c1-*.txt` for the same capability, so the README's
  `after/` pointer is the outlier. The original text stays." (evidence:
  `.ufo/waves/round-96/w1/R96ScribeCorrections-D5-readme-evidence-pointer.txt`.)

---

## What was checked and did not reproduce (recorded, not drafted)

- **D3's numbers are not false.** Re-running both round-94 counters on the round-95 landing tree
  `07e0e332` and on the round-96 freeze `2db151c5` yields `SKILL_TALLY_R94=PASS` and `CURATION_R94=PASS`,
  exit 0 both times. The defect is the missing landing-tree receipt behind the sentence, not a wrong value;
  the bullet above is drafted on that basis and says so.
- **D4's original wording (supersede the row) is withdrawn** by the closure's §7, and the locator is true, so
  no "supersedes S222 —" row is drafted. The revision narrows the defect to recording the external
  confirmation, which is what the bullet above says.
- **D5's pointer defect is a pointer defect only.** `after/c1-verify.txt` and `after-f2/c1-verify.txt` carry
  the same eight `SEARCH_RERUN` lines and the same `SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8
  tree_same=3/8 findings=0`; they differ only in the `computed_against` header and the timestamp
  (`diff` → exit 1, two header lines). So the `rev_match=8/8` figure the README row quotes is readable in
  `after/` as well as `after-f2/`; what `after/` cannot supply is the 13-record gate line, the mutant rebuild
  or the enlarged battery groups. The bullet says so rather than overstating.

## Tooling

No tool was installed or upgraded by this seat; every measurement used binaries already on the host
(`/usr/bin/grep` GNU grep 3.12, `git`, `python3`, `curl`). `curl` was used read-only for the single URL named
in the D4 item (`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7839230/fullTextXML`); the response was
written into this seat's scratch only, never into `corpus/captures/` or `corpus/evidence/round57/refetch.tsv`.
