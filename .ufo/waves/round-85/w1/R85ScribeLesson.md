# R85ScribeLesson — round-85 lesson scribe

Seat: `R85ScribeLesson`. Lane: chousa, round 85. Revision read: `64803d33362f50cf9094e91fc3a4a07216c563ca`
(the scored landing; also the current tip of the lane's `master` — `863d624e` is the wave-spec commit on top).
Base for every tree: `git archive 64803d33362f50cf9094e91fc3a4a07216c563ca | tar -x -C <scratch>`.

**Deliverable:** `.ufo/waves/round-85/w1/R85ScribeLesson/lesson-draft.md` — a **draft**, not landed. It carries the
four drafted sections (`## Mistakes`, `## considerthese`, `## Assimilation`, `## Gate` addendum). Nothing under
`corpus/` was edited; `git status --porcelain` for the lane is unchanged by this seat (the pre-existing
modifications to `SKILL.md`, `corpus/QUALITY.md`, `corpus/evidence/round85/after/*.txt`, `plans/round-85.md` and the
untracked wave folders are other seats'/the L1's; this seat wrote only inside
`.ufo/waves/round-85/w1/R85ScribeLesson/`).

**Receipts:** 13 files under `.ufo/waves/round-85/w1/R85ScribeLesson/receipts/`, plus
`00-fixture-construction.sh` which rebuilds every fixture from the landing revision alone.

**Adoption.** While this seat was measuring, the L1 appended to the working-tree lesson a `## Corrections` block
(items 1–3) and a `## Corrections (second block — wave R85ScribeLesson)` block (items 4–6), and added
`plans/round-85.md` amendment 10 and `corpus/QUALITY.md` criterion 172 — all citing this seat's receipts 01/02/04.
Items 4–6 state the same three findings this seat's report carries (F3/F4 the Gate narration, F2 the relaxed
floors, F1 the missing "first candidate run" receipt). This seat's draft is therefore the narrative form of
already-recorded corrections; the `## Mistakes` and `## Gate` sections should be merged with that block rather
than filed beside it. Those `corpus/` edits are the L1's, not this seat's — this seat wrote only inside
`.ufo/waves/round-85/w1/R85ScribeLesson/`.

---

## 1. Behaviour — what this seat did

Drafted the round-85 lesson sections and measured every claim they rest on, without landing anything.

1. Read the frozen predicate set (`corpus/evidence/round85/claims.md`) and `plans/round-85.md` first, as required.
2. Ran the frozen **depth counter** (`corpus/evidence/round85/depth-r85.py`) at the landing revision and on four
   constructed fixtures, to decide whether the two drafted `## Mistakes` rows survive their own evidence pointers.
3. Ran the **production tool** `tools/gate-records.py verify` at the landing revision, over the round-85 lesson,
   and over all 134 committed lessons.
4. Re-located each of the three Gate quotes in its committed capture by the rounds 81–82 hand "Location command".
5. Read `considerthese/2026-11-07.md` and `considerthese/2026-11-06.md` (newest first) and checked the one
   still-unimplemented proposal against the lane's committed bytes.
6. Re-counted the round-78 assimilation collisions file.

**Commands (exact, reproducible):**

```
python3 -B corpus/evidence/round85/depth-r85.py --root <scratch>/tree            # landing
python3 -B corpus/evidence/round85/depth-r85.py --root <scratch>/b1               # prefreeze ground
python3 -B corpus/evidence/round85/depth-r85.py --root <scratch>/b2               # fresh_sources=2 attempt
python3 -B corpus/evidence/round85/depth-r85.py --root <scratch>/b3               # prefreeze numeric floors
python3 -B corpus/evidence/round85/depth-r85.py --root <scratch>/b4               # S023 made FRESH (isolates E7)
python3 -B <scratch>/tree/tools/gate-records.py verify --root <scratch>/tree <scratch>/tree/corpus/lessons/round-85.md
python3 -B tools/gate-records.py verify --root . corpus/lessons/*.md              # 134 lessons, 24 records
python3 -B <scratch>/tree/tools/gate-records.py verify --root <scratch>/tree <scratch>/spotcheck/planned-reject-s0{33,20}.md
grep -rn "fails=E6,E7" .                                                        # 3 hits, all prose, 0 receipts
grep -rn "quotes=4/9" .                                                         # 1 hit: the lesson row citing itself
wc -l .ufo/waves/round-78/assimilation/collisions .ufo/waves/round-78/assimilation/staged-ids .ufo/waves/round-78/assimilation/reg-ids
```

---

## 2. Gates — what was measured, and the result

| gate | command | observed line | exit |
|---|---|---|---|
| C2 predicate at landing | `depth-r85.py --root <tree>` | `ENTRY provenance-recording-r85.md ok=yes rows=6 quotes=7/7 fails=-` / `DEPTH_R85 entries=1 ok_entries=1 rows=6 located_quotes=7 fresh_sources=3` / `DEPTH_R85=PASS` | 0 |
| C1 predicate at landing | `gate-records-r85.py --root <tree> --repo <lane> --work <scratch>/work` | `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=354/354 EXPECTED_CODE=354/354 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1` / `GATE_RECORDS_R85=PASS` | 0 |
| Gate records, round-85 lesson | `gate-records.py verify --root <tree> <lesson>` | `GATE_RECORD …/round-85.md:14 S215 OK` / `:15 S026 OK` / `:16 S024 OK` / `GATE_RECORDS files=1 records=3 ok=3 fail=0` | 0 |
| Gate sweep, all lessons | `gate-records.py verify --root . corpus/lessons/*.md` | `GATE_RECORDS files=134 records=24 ok=24 fail=0` | 0 |
| Quote location ×3 | rounds 81–82 hand locator | `FOUND` ×3 (wc -w = 12 / 20 / 16, matching each `words=`) | 0 |
| Prefreeze ground (b1) | `depth-r85.py --root <scratch>/b1` | `fails=E6,E7` / `fresh_sources=1` / `DEPTH_R85=FAIL` | 1 |
| `fresh_sources=2` (b2) | `depth-r85.py --root <scratch>/b2` | `fails=E6,E7` / `fresh_sources=2` / `DEPTH_R85=FAIL` | 1 |
| Prefreeze floors reachable (b3) | `depth-r85.py --root <scratch>/b3` | `rows=7 quotes=8/8 fails=-` / `DEPTH_R85=PASS` | 0 |
| S023 made FRESH (b4) | `depth-r85.py --root <scratch>/b4` | `fails=E7` / `fresh_sources=3` / `DEPTH_R85=FAIL` | 1 |
| b1/b2/b3/b4 rebuild | `sh receipts/00-fixture-construction.sh` | `fixtures written: b1 b2 b3 b4` / `spotcheck rows written`; every counter receipt above re-derives byte-identically from it | 0 |
| Planned reject S033 | `gate-records.py verify --root <tree> <spotcheck>/planned-reject-s033.md` | `GATE_RECORD …:1 S033 OK` / `records=1 ok=1 fail=0` | 0 |
| Planned reject S020 | `gate-records.py verify --root <tree> <spotcheck>/planned-reject-s020.md` | `GATE_RECORD …:1 S020 OK` / `records=1 ok=1 fail=0` | 0 |
| Capture SHA prefixes | `sha256sum <capture> \| cut -c1-16` | `8c9aeabb466fb6d1` / `27ee75739788bd9a` / `97fe1a6adbd2ded4` — all three match the records' `capture_sha256=` fields; each `capture` key = `sha256(url)[:24]` | 0 |
| Assimilation re-count | `wc -l .ufo/waves/round-78/assimilation/{collisions,staged-ids,reg-ids}` | `111` / `114` / `192` | 0 |

---

## 3. Touched surfaces

- **Written:** `.ufo/waves/round-85/w1/R85ScribeLesson/lesson-draft.md`, `.ufo/waves/round-85/w1/R85ScribeLesson.md`,
  `.ufo/waves/round-85/w1/R85ScribeLesson/receipts/00`–`12`.
- **Read:** `corpus/evidence/round85/claims.md` (freeze + amended), `plans/round-85.md` (amendments 1–9),
  `corpus/lessons/round-8{0,1,2,3,4,5}.md`, `corpus/lessons/round-84-verifier-spotcheck.md`,
  `corpus/knowledge/provenance-recording-r85.md`, `corpus/knowledge/search-transparency-reporting-r84.md`,
  `corpus/SOURCES.md`, `corpus/evidence/round57/refetch.tsv`, `corpus/evidence/round85/depth-r85.py`,
  `corpus/evidence/round85/gate-records-r85.py`, `tools/gate-records.py`, `corpus/QUALITY.md`,
  `corpus/evidence/round85/base-knowledge.txt`, `corpus/evidence/round85/controls/receipts/*`,
  `considerthese/2026-11-07.md`, `considerthese/2026-11-06.md`, `.ufo/waves/round-78/assimilation/*`,
  `.ufo/waves/round-85/w1/R85CriticClaims.md`, `.ufo/waves/round-85/w1/R85ReviewerEntry.md`,
  `.ufo/waves/round-85/w1/R85ConnectorSiblings.md`, `.ufo/waves/round-85/w1/R85ExecReopen.md`.
- **Scratch:** `/fast/scratch/hyaku/chousa-r85/R85ScribeLesson/` (trees `tree`, `b1`–`b4`, `work`, `spotcheck`) —
  **deleted before this report** (`rm -rf -- /fast/scratch/hyaku/chousa-r85/R85ScribeLesson`); every receipt cited
  above was copied into the wave output folder first, and `00-fixture-construction.sh` rebuilds all of it.

---

## 4. Out of scope — not done by this seat

- No production edit: `corpus/lessons/round-85.md` is **unchanged**; the draft is not landed.
- No claim adjudication. C1's honest stop (amendment 7, `R85CriticClaims` / `R85MutationTool`) and C2's honest stop
  (amendment 8, `R85ReviewerEntry`; amendment 9, `R85ScoutGround`) are other seats' findings; this seat neither
  contests nor re-derives them. This seat's verdict lines below are scoped to what was measured here.
- No network fetch. No `corpus/captures/` write, no `refetch.tsv` write. The egress table
  (`corpus/evidence/round85/egress-approval.md`) was read, not exercised; the re-open allowance was not used.
- No git/jj mutation of the lane, no commit, no push, no sibling-repo edit (`/home/vgpnk/Projects/shokuknow/merge/chousa`
  was listed read-only to establish that the merge package is not in this lane; its bytes were not read).
- No tool install. `python3` (3.13, stdlib only) and `git` were sufficient; `RULES.md` read first, pacman not touched.

---

## 5. Findings

### F1 — Drafted `## Mistakes` row 1 is confirmed on substance, but its cited receipt does not contain what it is cited for (finding)

`corpus/lessons/round-85.md:53` cites "scoring receipt `corpus/evidence/round85/controls/receipts/c2-d0-donothing.txt`
and the E6/E7 lines of the first candidate run".

- `c2-d0-donothing.txt` holds three lines — `DEPTH_R85 entries=0 ok_entries=0 rows=0 located_quotes=0
  fresh_sources=0` / `DEPTH_R85=FAIL` / `depth rc=1`. It is the **tree-at-base do-nothing control**; it contains no
  `E6` and no `E7`. Receipt `corpus/evidence/round85/controls/receipts/c2-d0-donothing.txt`.
- **The "first candidate run" receipt does not exist in the lane.** `grep -rn "fails=E6,E7" .` over the whole
  repository returns three hits — `corpus/QUALITY.md:1100`, `corpus/lessons/round-85.md:53`, `plans/round-85.md:22` —
  all prose, and **zero receipt files**. The same grep over `.ufo/waves/round-85/` finds only `R85CriticClaims`'s
  unrelated `c2-reland` control. QUALITY 169's own pointer — "scoring in `.ufo/waves/round-85/` evidence" — names a
  directory in which no such scoring receipt exists.
- Separately, `claims.md` at the freeze points its "**Before**" line at `controls/receipts/c1-d0-donothing.txt`
  while the file on disk is `c2-d0-donothing.txt` — a broken pointer inside the frozen claims file.

**The claim itself is true and now has a receipt.** `fresh_sources` is the count of FRESH ids on the `source:` line,
so the frozen predicate `fresh_sources=2` can only be printed beside a FAIL: receipt 02 prints
`fresh_sources=2` with `fails=E6,E7` and `DEPTH_R85=FAIL` rc 1. The prefreeze ground is reproduced in receipt 01
(`fails=E6,E7`, rc 1); receipt 04 isolates the two rules (b4 makes S023 FRESH and still fails on E7 alone).

**Fix (shown able to fail):** dry-run the frozen counter against a stub entry before the freeze. Before: receipt 01,
rc 1, `fails=E6,E7`. After: receipt 03, rc 0, `fails=-`.

### F2 — Drafted `## Mistakes` row 2 is not confirmable and is replaced (finding)

`corpus/lessons/round-85.md:54` asserts the prefreeze "predicted a 9-quote, 7-row entry while the counter's E4
novelty rule rejects every quote the round-84 entry already carries, so only 7 quotes / 6 rows were reachable",
citing "first candidate run `quotes=4/9`, `rows=7`".

- `grep -rn "quotes=4/9" .` returns **one hit: the lesson row citing itself**. No receipt of that run exists.
- The "9 quotes" figure is not in the frozen claims: at the freeze the predicate reads `rows= ≥ 7`,
  `located_quotes= ≥ 8`, `fresh_sources=2` (`git show 5d0b9413:corpus/evidence/round85/claims.md`). The number 9
  first appears in QUALITY 169 — which is **working-tree only** (`git status --porcelain` shows `M corpus/QUALITY.md`;
  `git show 64803d3:corpus/QUALITY.md` ends at criterion 168) — and in the lesson row.
- The E4 attribution is **refuted by the counter**: the amended entry's seven quotes come from S215/S026/S024, none
  quoted by the round-84 entry, so E4 never fires (`fails=-`, receipt 03). And the amended ground reaches
  `rows=7 located_quotes=8` with `DEPTH_R85=PASS` rc 0 (receipt 04) — the prefreeze floors were satisfiable, so the
  count relaxation was a choice, not a ceiling.

**Replacement row** (`predicate-relaxed-to-the-artifact`): the amendment that re-pointed the ground also lowered the
numeric floors to the landed values in the same commit (`rows= ≥ 7` → `≥ 6`, `located_quotes= ≥ 8` → `≥ 7`;
`git diff 5d0b9413 02df67db -- corpus/evidence/round85/claims.md`). A frozen count lowered in the same breath as
the ground it was measured against measures nothing.

### F3 — The landing `## Gate` block mis-attributes this round's fetches (finding)

`corpus/lessons/round-85.md:23-24` states the canonical `REC-prov-o-20130430` URL "answered HTTP 403 on three
attempts in round 84 **and again this round** (rows in `refetch.tsv`, `curl_rc=22`)". **No round-85 row carries the
canonical URL.** The three canonical-URL rows (`refetch.tsv` lines 167–169) are dated `2026-11-08T02:16:01Z`–
`02:16:08Z`, before the freeze commit's committer time `2026-11-08T00:54:30-03:00` = `03:54:30Z` — they are round
84's, and round 84's lesson already lists "S020 PROV-O (HTTP 403, three attempts)" as its own rejection
(`corpus/lessons/round-80.md`… `corpus/lessons/round-84.md`). The round-85 403 rows are on the **alternate** URL:
lines 175, 176 (id `S020`) and 179 (id `S033`). Receipt 09 prints all of this from committed bytes.

### F4 — "Rejected this round … none new — every candidate URL opened answered 200" is not accurate as written (finding)

`corpus/lessons/round-85.md:39-40`. The round-85 ledger holds **three** non-200 rows after the freeze
(`curl_rc=22`, `http=403`): lines 175, 176, 179 (receipt 09). The correct reading is that all three are attempts on
the alternate PROV-O URL, which then succeeded on attempt 3 under `S215` (line 177) — so **no candidate source was
turned down** and *no new reject row is the right call*, but the sentence's reason is wrong and should be reworded;
and the canonical-URL sentence beside it (F3) is wrong outright. Both corrections are cheap and checkable from
`refetch.tsv` alone; neither needs a fetch.

### F5 — The Gate block's per-id narrative hides that three ids share one URL (finding)

The S215 record's `fetched=2026-11-08T03:55:52Z` is the **third** attempt on the alternate URL; the two earlier
attempts are filed under `S020` (lines 175–176) and a later refused attempt under `S033` (line 179) — the same URL,
four attempts, three ids, and the registry carries S020, S033 and S215 as three separate rows for one document
(`corpus/SOURCES.md` lines 30, 43, 228). The block's `## Registry changes` says only "S020: unchanged (`queued`)"
and mentions none of this. A spot-check reading the block would not learn it. The tool accepts either refused
attempt as an unreach-form row (receipt 11: `S033 OK` rc 0, `S020 OK` rc 0), so a reject row is available if the
round wants one.

### F6 — "One open Gate-record S-id per daily review" is still unimplemented, and the tool cannot substitute for it (finding)

`considerthese/2026-11-06.md`'s proposal (still carried as open in `considerthese/2026-11-07.md`: "Twelve open
Gate-record defects from the r80 ScoutA survey still unopened") asks for one backlog id per day, re-counted by hand
at its cited revision. It is **not implemented** this round:

- The twelve ids (`corpus/lessons/round-80.md:141`) are `S170 S171 S173 S174 S175 S176 S178 S179 S182 S183 S191
  S193`. `grep -l -E '^GATE-RECORD (S170|…|S193) ' corpus/lessons/*.md` returns **no file** (receipt 08): none of
  the twelve carries a `GATE-RECORD` line, so `tools/gate-records.py verify` cannot reach them at all — it reads
  only lines whose first text is `GATE-RECORD`, and every lesson's `## Gate` block from round 80 on is the
  four-column pipe-table form.
- The one-command sweep does run clean — `GATE_RECORDS files=134 records=24 ok=24 fail=0` rc 0 (receipt 07) — but
  its 24 records are the rounds 80–85 lessons, not the backlog.
- No round-85 wave artifact touches any of the twelve ids.

**What would count as implementing it:** give one seat one backlog id, have it `git show <rev>:<path>` and re-count
the quote, and write the verdict as a receipt (as the r80 ScoutA survey did).

### F7 — Two pointer defects inside committed bytes (findings)

- `corpus/evidence/round85/claims.md` (both the freeze and the amended revision) points its "**Before**" line at
  `controls/receipts/c1-d0-donothing.txt`; the file on disk is `c2-d0-donothing.txt`. Broken pointer.
- `corpus/QUALITY.md` at the landing revision ends at criterion **168**; 169–171 are working-tree only
  (`git status --porcelain` → `M corpus/QUALITY.md`; `git show 64803d3:corpus/QUALITY.md | grep -c '^169\.'` → 0).
  The round-85 lesson's `## Mistakes` row cites "QUALITY 169 (new)" as the capturing rule, and
  `corpus/lessons/round-85.md:76-80` cites "169–171" — all uncommitted at the revision under review. The lesson's
  own `## Mistakes` row also cites `c2-d0-donothing.txt` for E6/E7 lines it does not contain (F1).

### F8 — The r85 counters carry the QUALITY-164 pattern the repaired production tool just dropped (finding, routed)

`tools/gate-records.py` was repaired this round to ASCII-only digit classes (`[0-9]{3,}` etc.; `grep -n 'd{3,}\|isdigit\|re.ASCII' tools/gate-records.py` → no hits at the landing rev). The **two counters landed this round** use the Unicode-aware class in five places: `corpus/evidence/round85/depth-r85.py:54,55,57` (`S\d{3,}`, `\bQ\d+\b`) and
`corpus/evidence/round85/gate-records-r85.py:154,204,244` (`S\d{3,}`, `S\d+`). Verified: `re.match(r'^ {0,3}\| (S\d{3,}) \|(.+)\|$', '| S٢٢٢ | x |')` matches, while the tool's `S[0-9]{3,}` does not; `int('٢٢')` is `22`.

This seat did **not** construct a forgery that exploits it, so it is reported as a routed item, not as a claim
verdict: the pattern is QUALITY 164's class ("a parser's numeric fields match ASCII digits only"), the repairs this
round removed it from the production tool, and the two new parsers reintroduced it. It belongs in the round-86
routing alongside QUALITY 164/167.

---

## 6. Artifacts

| path | what |
|---|---|
| `.ufo/waves/round-85/w1/R85ScribeLesson/lesson-draft.md` | the four drafted lesson sections (draft, not landed) |
| `.ufo/waves/round-85/w1/R85ScribeLesson.md` | this report |
| `.ufo/waves/round-85/w1/R85ScribeLesson/receipts/00-fixture-construction.sh` | rebuilds every fixture from the landing rev |
| `…/receipts/01-counter-prefreeze-ground.txt` | prefreeze ground → `fails=E6,E7` rc 1 |
| `…/receipts/02-counter-fresh-sources-2.txt` | `fresh_sources=2` printed beside a FAIL rc 1 |
| `…/receipts/03-counter-after-landing.txt` | landing → `DEPTH_R85=PASS` rc 0 |
| `…/receipts/04-counter-prefreeze-floors-reachable.txt` | prefreeze floors reachable on the amended ground, rc 0 |
| `…/receipts/05-gate-tool-verify-landing-lesson.txt` | three Gate records OK rc 0 |
| `…/receipts/06-hand-location-three-gate-quotes.txt` | three quotes FOUND, word counts 12/20/16 |
| `…/receipts/07-gate-tool-all-lessons.txt` | 134 lessons, 24 records, 24 OK rc 0 |
| `…/receipts/08-scouting-backlog-twelve-ids.txt` | none of the twelve ids carries a Gate record |
| `…/receipts/09-round85-ledger-and-canonical-url.txt` | the round-85 ledger rows; canonical URL not fetched this round |
| `…/receipts/10-assimilation-collisions-recount.txt` | 111 / 114 / 192 |
| `…/receipts/11-planned-reject-rows.txt` | S033 and S020 unreach rows accepted by the tool rc 0 |
| `…/receipts/12-capture-sha-prefixes.txt` | capture SHA prefixes match the records' `capture_sha256=` fields |
| `…/receipts/13-counter-e7-isolated.txt` | S023 made FRESH → E7 alone still fires, rc 1 |

---

VERDICT: R85ScribeLesson C1 n/a — this seat is the lesson scribe, not a C1 attack seat: it measured the landing predicate (`POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=354/354 EXPECTED_CODE=354/354 SETUP=1/1`, rc 0) and the Gate records (`records=3 ok=3 fail=0`, rc 0), and adjudicated no C1 kill rule; C1's honest stop (amendment 7) is `R85CriticClaims`/`R85MutationTool`'s finding, not this seat's.
VERDICT: R85ScribeLesson C2 n/a — this seat adjudicated no C2 kill rule (amendments 8 and 9 are `R85ReviewerEntry`'s and `R85ScoutGround`'s findings); what this seat found is that the lesson's two `## Mistakes` rows do not survive their own evidence pointers — the cited `c2-d0-donothing.txt` is the do-nothing control, the "first candidate run" receipt exists nowhere in the lane, and `quotes=4/9` occurs only in the row citing itself — and that the landing `## Gate` block's canonical-URL and "none new" sentences are contradicted by `refetch.tsv` lines 175–179.
