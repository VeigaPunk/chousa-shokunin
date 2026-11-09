# R96ScribeCorrections — round-96 wave-1 scoped findings (scribe, leaf seat)

Lane `chousa`, round 96, wave 1, seat `R96ScribeCorrections` (leaf; no subagents dispatched).
Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Round-96 claim freeze F `2db151c5ea0883de0b9dc8d95c6fac1755e1056a` (the tree this seat attacked);
base `bbf64970b6c73ca64bcc5f6de2f33b0550459813`; round-95 landing `07e0e3323db692da4f726437bbc388acea4ae5e0`.

**Scope.** This seat owes append-only corrections drafted from the round-95 non-author spot-check
(`corpus/lessons/round-95-verifier-spotcheck.md`), section 6 "Routed defects" items **D2, D3, D5** and
section 7's **revised D4**. D1 is out of scope (round 96's C1 takes it; it is already landed at
`SKILL.md:180`). The draft lives at
`.ufo/waves/round-96/w1/R96ScribeCorrections-log-draft.md`.

**Falsification method.** Each defect was re-opened by this seat against committed bytes (not from the
spot-check's prose), the cited file and line were read directly, and the defect was confirmed by an
independent command. Where the defect's stated *number* turned out to be true while its *evidence* was
missing, the correction bullet says so rather than overstating. Where a defect did not reproduce, it is
recorded as not reproducing instead of drafted.

---

## 1. Behavior — the four corrections drafted

All four defects reproduce. One (`D3`) reproduces as an **evidence gap, not a false number**; one (`D4`)
reproduces in the **revised** (narrower) form the closure gave it, not in its original "supersede the row"
form. Two sub-findings about the round-96 plan are reported in §3.

### D2 — the round-95 lesson's quote count was never right (`corpus/lessons/round-95.md:23`)

`corpus/lessons/round-95.md:23` reads, at the round-95 landing, at F2 `86909f02`, and at the round-96
freeze `2db151c5` alike:

> `  for a different re-run count; C2's entry holds nine located quotes from this capture.`

The entry holds **13**. `git show 86909f02:corpus/knowledge/search-rerun-record-r95.md | grep -c '^| Q'` → `13`
and `grep -c '^GATE-RECORD'` → `13`; the same counts hold at `07e0e332` and `2db151c5`. The landing receipt
`corpus/evidence/round95/after-f2/c2-gate.txt:17` prints `GATE_RECORDS files=1 records=13 ok=13 fail=0`, and a
re-run of `python3 -B tools/gate-records.py verify --root . corpus/knowledge/search-rerun-record-r95.md` at the
freeze exits 0 with the same line.

The sharper point, which the spot-check did not make: the stale count was **never correct at any committed
revision of that lesson**. `git cat-file -e d6429e02:corpus/lessons/round-95.md` exits 128 — the lesson file
did not exist at freeze F — and it was born at F2 `86909f02`, the very commit that carried the entry's 13
quotes. So this is not a number that drifted; it was written wrong at birth and the corrections sweep missed
it. The lane's own `corpus/README.md:1443` already says "the entry carries 13 located quotes after the
wave-forced Amendment 1", so the lesson and the README contradict each other inside the same round.

The F-measured receipt `corpus/evidence/round95/after/c2-gate.txt:13` does print
`GATE_RECORDS files=1 records=9 ok=9 fail=0` — that is the count *at F, before Amendment 1*, not at the
lesson's own revision. The bullet names this so the correction cannot be mistaken for "the count was 9 at
some point".

**Receipt:** `.ufo/waves/round-96/w1/R96ScribeCorrections-D2-lesson-nine-quotes.txt`

### D3 — the two counter verdicts are true but had no round-95 receipt behind them

Two sites assert the round-94 counters on the round-95 landing tree:

- `/home/vgpnk/Projects/shokunin/.ufo/reports/round-95/chousa.md:95-96` (fleet repo):
  > `No axis harmed: git diff --quiet 7b237358 07e0e332 -- tools/research-gate.sh tools/gate-records.py PROVINCE.md exit 0;`
  > `on the landing tree SKILL_TALLY_R94=PASS and CURATION_R94=PASS.`
- `SCORECARD.md:4258-4259` (lane):
  > `r94 counters still pass on the landing tree (SKILL_TALLY_R94=PASS, CURATION_R94=PASS);`

`grep -rl 'SKILL_TALLY_R94' corpus/evidence/round95/` → exit 1, no match.
`grep -rl 'CURATION_R94' corpus/evidence/round95/` → exit 1, no match.
The exhaustive `grep -rl 'SKILL_TALLY_R94\|CURATION_R94' corpus/evidence/` returns only round-94 files: the
two receipts `corpus/evidence/round94/after/c2-counter.txt` and `…/c3-counter.txt` (each headed
`# computed_against F=ebbcbe39… C=d13c2ff2…` — the round-94 freeze, not the round-95 landing), the two
`*-r94.py` instruments, and their `__pycache__`. The single round-95-tree file that mentions the string,
`.ufo/waves/round-95/w1/R95ScribeCorrections-D2-log.md-stale.txt`, quotes the round-94 `LOG.md` prose and
prints no verdict line of its own (`grep -c '^SKILL_TALLY_R94='` → `0`).

**This seat re-measured, and the values are true.** In a scratch clone of the round-95 landing `07e0e332`:
`python3 -B corpus/evidence/round94/skill-tally-r94.py --root .` → `… TAIL_OK=1 LEGS=4/4` /
`SKILL_TALLY_R94=PASS`, exit 0; `python3 -B corpus/evidence/round94/curation-r94.py --root .` → `…
LEGS_MEASURED=16/16` / `VERDICT fields_hold=1 legs_ok=16/16 DETECTOR_WITNESS=18/18` / `CURATION_R94=PASS`,
exit 0. The same two runs on the round-96 freeze `2db151c5` also exit 0 with both PASS.

So the sentence's *values* are correct and its *citation* is missing: the verdicts were asserted on the
landing tree with no landing-tree receipt behind them. The correction bullet is drafted on exactly that
basis — it does not claim the counters fail, and it notes that the harm verdict rests on the lane's own
diff rather than on these two counters.

**Receipts:** `.ufo/waves/round-96/w1/R96ScribeCorrections-D3-r94-counter-receipts.txt`,
`…-D3b-counters-r95-landing.txt`, `…-D3c-counters-r96-freeze.txt`

### D4 (revised) — the "10:39" locator is true; the confirmation is not in the lane

The closure's §7 (`corpus/lessons/round-95-verifier-spotcheck.md:180-183`) withdrew the original D4 and
narrowed it: the S222 locator "Systematic Reviews 10:39" is **true**, only unsupported by the lane's own
capture, and the defect narrows to *recording the external confirmation* (or a capture of the
co-publication) rather than superseding the row.

`corpus/lessons/round-95.md:39-41` still says:

> `  volume/article locator 10:39 came from the round's web-search summary, not from the capture. Read the cell as`
> `  "co-published in Systematic Reviews (doi 10.1186/s13643-020-01542-z)".`

This seat re-opened the Europe PMC REST full-text XML for PMC7839230 read-only into its own scratch and got
the same elements on its third attempt — `attempt=1 http=500 size=150`, `attempt=2 http=500 size=150`,
`attempt=3 http=200 size=226044` — and
`grep -o '<journal-title>[^<]*</journal-title>\|<volume>[^<]*</volume>\|<elocation-id>[^<]*</elocation-id>'`
yields `<journal-title>Systematic Reviews</journal-title>`, `<volume>10</volume>`,
`<elocation-id>39</elocation-id>`; the same body carries `10.1186/s13643-020-01542-z` and the item-8
sentence "copied and pasted exactly as run" twice. The locator is confirmed externally.

Two facts constrain what the lane can do: the lane's own two attempts on that URL are recorded as http 500
(`corpus/evidence/round57/refetch.tsv:190` attempt 1 at `2026-11-08T22:51:19Z` and `:193` attempt 2 at
`2026-11-09T00:35:48Z`, both `22 500`), and no capture of it exists in the lane
(`grep -rl 'elocation-id' corpus/captures/*.txt` → exit 1). So the route is intermittent, not dead, and
the confirmation is currently reachable only by a lucky attempt. The correction bullet accordingly records
the external confirmation as the record, keeps the lesson's provenance note standing, and does **not**
draft the withdrawn "supersedes S222 —" row.

**Receipt:** `.ufo/waves/round-96/w1/R96ScribeCorrections-D4-locator-external-confirmation.txt`

### D5 — the README's Round95 row points at the superseded receipt set

`corpus/README.md:1441` (Round95 section, the `../tools/search-rerun.py` row) ends its Sources cell with
`corpus/evidence/round95/after/`. Every receipt under `after/` is headed
`# computed_against F=d6429e02… tree_equals_F_for_measured_paths=yes` — freeze F — and `after/` holds **no
mutant receipt at all** (`ls corpus/evidence/round95/after/` → `c1-controls.txt c1-verify.txt c2-controls.txt
c2-gate.txt c2-metadata.txt`; `grep -rn 'MUTANTS_KILLED' corpus/evidence/round95/after/` → exit 1).

The numbers the round reports live in `after-f2/`:

| receipt | `after/` (F) | `after-f2/` (F2 = landing) |
|---|---|---|
| `c2-gate.txt` | `GATE_RECORDS files=1 records=9 ok=9 fail=0` | `GATE_RECORDS files=1 records=13 ok=13 fail=0` |
| `c1-controls.txt` | `FORGERY_REFUSED=8/8 … ORACLES_REJECTED=3/3` | `FORGERY_REFUSED=10/10 … GREP_AGREE=4/4 CONTAINMENT=2/2 … ORACLES_REJECTED=4/4` |
| `c1-mutants.txt` | *absent* | `MUTANTS_KILLED=10/10` |

`git diff --stat 86909f02 07e0e332 -- tools corpus/fixtures corpus/knowledge corpus/evidence/round95/` exits 0
and prints only the seven `after-f2/` additions plus `census-end.txt`; `tools/`, `corpus/fixtures/` and
`corpus/knowledge/` are byte-identical between F2 and the landing. `SKILL.md:179` already points at
`corpus/evidence/round95/after-f2/c1-*.txt` for the same capability, so the README's `after/` pointer is the
outlier.

One precision note the bullet carries: `after/c1-verify.txt` and `after-f2/c1-verify.txt` print the *same*
eight `SEARCH_RERUN` lines and the same `SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8 tree_same=3/8
findings=0` (`diff` → exit 1, two header lines only). So the `rev_match=8/8` figure the README row quotes is
readable in `after/` too; what `after/` cannot supply is the 13-record gate line, the mutant rebuild or the
enlarged battery groups. The bullet states that rather than claiming the quoted number is unreadable.

**Receipt:** `.ufo/waves/round-96/w1/R96ScribeCorrections-D5-readme-evidence-pointer.txt`

---

## 2. Gates and instruments run by this seat

| check | command | observed | result |
|---|---|---|---|
| D2 entry count | `git show 2db151c5:corpus/knowledge/search-rerun-record-r95.md \| grep -c '^\| Q'` | `13` | reproduced |
| D2 gate re-run | `python3 -B tools/gate-records.py verify --root . corpus/knowledge/search-rerun-record-r95.md` | `GATE_RECORDS files=1 records=13 ok=13 fail=0`, exit 0 | reproduced |
| D2 lesson birth | `git cat-file -e d6429e02:corpus/lessons/round-95.md` | exit 128 ("exists on disk, but not in 'd6429e02'") | lesson never existed at F |
| D3 receipt search | `grep -rl 'SKILL_TALLY_R94' corpus/evidence/round95/` / `'CURATION_R94'` | exit 1, no match (both) | reproduced |
| D3 counter re-run (r95 landing) | `skill-tally-r94.py --root .` / `curation-r94.py --root .` in a scratch clone of `07e0e332` | `SKILL_TALLY_R94=PASS` exit 0; `CURATION_R94=PASS` exit 0 | values true, receipt missing |
| D3 counter re-run (r96 freeze) | same two on `2db151c5` | `SKILL_TALLY_R94=PASS` exit 0; `CURATION_R94=PASS` exit 0 | values true |
| D3 r95 record re-run | `python3 -B tools/search-rerun.py verify corpus/fixtures/search-rerun-r95.md --root .` on `07e0e332` | `rev_match=8/8 tree_same=3/8 findings=0`, `SEARCH_RERUN: CLEAN`, exit 0 | round-95 record still verifies |
| D4 external re-open | `curl -sS --max-time 60 …/PMC7839230/fullTextXML` (3 attempts, read-only into scratch) | 500, 500, then 200 / 226044 B | locator confirmed |
| D4 locator elements | `grep -o '<volume>[^<]*</volume>\|<elocation-id>[^<]*</elocation-id>'` | `<volume>10</volume>`, `<elocation-id>39</elocation-id>` | locator true |
| D4 lane capture search | `grep -rl 'elocation-id' corpus/captures/*.txt` | exit 1, no match | no capture exists |
| D5 receipt headers | `head -1` over every `after/*.txt` and `after-f2/*.txt` | `after/` all `F=d6429e02…`; `after-f2/` all `F=86909f02…` | reproduced |
| D5 F2 = landing | `git diff --stat 86909f02 07e0e332 -- tools corpus/fixtures corpus/knowledge corpus/evidence/round95/` | exit 0; only `after-f2/` additions + `census-end.txt` | reproduced |

Every command above names the tree it ran against; the two clones live under this seat's scratch and were
checked with `git rev-parse --show-toplevel` before any mutating git call.

---

## 3. Findings — the round-96 plan states two things the freeze does not support

These are **not** lane production edits and **not** part of the four owed corrections; they are reported so
the canonical planner seat (`ChousaR96`) can act on them before the round lands.

**F-A (plan D4 sub-claim, false as stated).** `plans/round-96.md:46-47` says: *"the external confirmation of
'10:39' recorded by the round-95 closure **is cited in the lesson**, the row is unchanged."* It is not.
`grep -c 'elocation\|<volume>\|volume>10\|JATS\|fullTextXML\|PMC7839230' corpus/lessons/round-95.md` → `2`,
and both hits are the route-**rejection** prose at lines 28 and 32 (the http-500 rejection), not a citation
of the confirmation. The only file in the lane carrying `<elocation-id>39` is
`corpus/lessons/round-95-verifier-spotcheck.md` (the closure's own file). The lesson's §Gate still carries
the *uncited* prose "Read the cell as 'co-published in Systematic Reviews (doi 10.1186/s13643-020-01542-z)'",
which reads as a live instruction to drop a locator that is in fact true.

**F-B (plan/egress-approval promise, unmet at the freeze).** `corpus/evidence/round96/egress-approval.md:12`
promises "the round-96 lesson `## Gate` records the volume/elocation elements found". At the freeze no
round-96 lesson exists (`git ls-tree -r --name-only 2db151c5 -- corpus/lessons/ | grep -i 96` → exit 1) and
the round-96 attempt on that URL answered http 500 (`refetch.tsv:193`, attempt 2 at `2026-11-09T00:35:48Z`),
so nothing was found to record. This seat's own third attempt did return http 200 with the elements, so the
route is intermittent rather than closed — a later attempt may still yield the bytes, but no attempt at the
freeze did.

**F-C (minor, informational).** `plans/round-96.md:45` routes D3 as "the r94 counters were not re-run in
round 95". That is true as stated (no round-95 receipt carries the runs), but this seat's re-measurement
shows the counters would pass on the landing tree, so the correction owed is a missing receipt, not a
retraction of the claim. The drafted D3 bullet is written on that basis.

---

## 4. Touched surfaces

**Written (this seat's allowed scope only):**

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-96/w1/R96ScribeCorrections-log-draft.md` — the drafted corrections
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-96/w1/R96ScribeCorrections.md` — this report
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-96/w1/R96ScribeCorrections-D2-lesson-nine-quotes.txt`
- `…/R96ScribeCorrections-D3-r94-counter-receipts.txt`
- `…/R96ScribeCorrections-D3b-counters-r95-landing.txt`
- `…/R96ScribeCorrections-D3c-counters-r96-freeze.txt`
- `…/R96ScribeCorrections-D4-locator-external-confirmation.txt`
- `…/R96ScribeCorrections-D5-readme-evidence-pointer.txt`

**Read only (no writes):** the lane repo at `2db151c5`, the fleet repo's `.ufo/reports/round-95/chousa.md`,
`corpus/lessons/round-95.md`, `corpus/lessons/round-95-verifier-spotcheck.md`, `SCORECARD.md`,
`corpus/README.md`, `corpus/SOURCES.md`, `SKILL.md`, `plans/round-96.md`, `corpus/evidence/round95/**`,
`corpus/evidence/round96/egress-approval.md`, `corpus/evidence/round57/refetch.tsv`.

**Scratch (deleted before yield):** `/fast/scratch/hyaku/chousa-r96/R96ScribeCorrections/` — clones
`repo-r95` (at `07e0e332`) and `repo-f96` (at `2db151c5`), plus the JATS re-open bytes
(`jats-try{1,2,3}.xml`, `jats-pmc7839230.xml`) and the two counter transcripts.

**Not touched:** no production file, no product code, no judge, no commit, no push, no publish, no deploy,
no other runtime; nothing under `/home/vgpnk/Projects/shokunin/scripts`, `.ufo/state`, `MANIFEST.json`,
`considerthese/` or any sibling repo; no git/jj mutation of the lane or fleet; no host sysctl, no `sudo`, no
service restart, no CPU burner; nothing written under `/tmp`.

## 5. Out of scope (declared, not silently skipped)

- **D1** (the `search-rerun verify` Gates row's kind and missing self-invocation mode) — round 96's C1
  takes it; already landed at `SKILL.md:180` at the freeze. Not drafted, not re-measured here beyond
  confirming the row exists and `--selftest` is present in `tools/search-rerun.py` (10 occurrences at the
  freeze).
- **The round-96 claims C1/C2 themselves** — this seat's assignment is the corrections, not the claims.
  No claim was scored and no claim verdict is asserted.
- **The r95 lesson's other prose, the S222 registry row, and the round-95 report's other sentences** — not
  routed defects; left alone.
- **Any correction to production files** — this seat drafted; it did not apply. The four bullets are for the
  planner seat to append to `LOG.md` (the lane's existing convention, `LOG.md:2767-2785`).

## 6. Known limits

- The Europe PMC route is intermittent: three attempts by this seat gave 500, 500, 200. The lane's own two
  recorded attempts are both 500. The `<volume>10</volume>` / `<elocation-id>39</elocation-id>` confirmation
  is therefore currently reachable only opportunistically, and this seat's bytes live in scratch only — they
  are not a lane capture.
- The r94 counter re-runs are this seat's own measurement, not a lane receipt; they show the *values* are
  true, not that the round-95 report was entitled to cite them without a receipt.
- `git cat-file -e d6429e02:corpus/lessons/round-95.md` exiting 128 shows the lesson file was not in the F
  tree. It does not by itself prove the sentence was never written somewhere else; the claim is scoped to
  the committed lesson file at every revision that contains it (F2, landing, r96 freeze).
- This seat did not re-run the round-95 battery or the mutant rebuild; it re-ran only the two counters D3
  names, plus the round-95 record's own `search-rerun verify` (which still returns `rev_match=8/8`,
  `SEARCH_RERUN: CLEAN`, exit 0 on the landing tree).

## 7. Artifact paths

- Drafted corrections: `.ufo/waves/round-96/w1/R96ScribeCorrections-log-draft.md`
- This report: `.ufo/waves/round-96/w1/R96ScribeCorrections.md`
- Receipts: `.ufo/waves/round-96/w1/R96ScribeCorrections-D2-lesson-nine-quotes.txt`,
  `…-D3-r94-counter-receipts.txt`, `…-D3b-counters-r95-landing.txt`, `…-D3c-counters-r96-freeze.txt`,
  `…-D4-locator-external-confirmation.txt`, `…-D5-readme-evidence-pointer.txt`

---

VERDICT: R96ScribeCorrections C1 n/a — this seat scored no round-96 claim; its work is the four append-only corrections drafted from the round-95 spot-check.
VERDICT: R96ScribeCorrections C2 n/a — this seat scored no round-96 claim; its work is the four append-only corrections drafted from the round-95 spot-check.
