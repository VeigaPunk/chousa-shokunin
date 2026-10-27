# R54ExecQuarantineRest — round-54 W1, quarantine slice: verdict coverage and canonical-line drafts

Seat: leaf executor (no subagents, no background jobs, no installs — pacman is host-wide paused;
`awk`/`python3`/`grep` sufficed). Lane repo `/home/vgpnk/Projects/shokunin/chousa-shokunin` (read-only
for me); the read-only campaign register at `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`.
My only write is this report. Scratch `/fast/scratch/hyaku/chousa-r54/R54ExecQuarantineRest` (`TMPDIR`
there), removed at the end. No network, no git/jj mutation, no campaign tool run.

## 1. The slice — 24 rows, re-derived with the prompt's own command

```
$ R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
$ awk -F'|' -v l='chousa' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" | wc -l
24
```

The lane's own round-54 slice file `.ufo/waves/round-54/assimilation/quarantine-slice` (788 B) holds the
same 24 ids in the same order (`S077 S080 S082 S084 S086 S088 S093 S094 S095 S096 S104 S105 S108 S110
S111 S112 S114 S116 S120 S125`, then `S100 S101 S102 S103` in the five-column "NEVER CHECKED" table).
Register line numbers: S077=37, S080=38, S082=39, S084=40, S086=41, S088=42, S093=43, S094=44, S095=45,
S096=46, S104=47, S105=48, S108=49, S110=50, S111=51, S112=52, S114=53, S116=54, S120=55, S125=56,
S100=269, S101=270, S102=271, S103=272.

## 2. The counter's own view — which rows the C2 counter will even look at

Replayed `c2-count.py:255-263` with the counter imported unmodified (module-level constants only;
`main()` never called, so nothing was counted or written):

```
$ python3 sim.py   # imports corpus/evidence/round54/c2-count.py, replays its reg_ids loop
REGISTER_EXISTS True
LESSON_R54_EXISTS False
REG_IDS 3 ['S080', 'S088', 'S096']
   S080 -> https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F
   S088 -> https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf
   S096 -> https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc
```

`reg_ids` is filled only from register rows with `len(f) > 6` (the seven-column `## Rows` shape) whose
`f[5]` normalises into the theme set; the five-column `## Rows whose quotes were NEVER CHECKED` shape
(S100–S103) has no URL cell and therefore can never enter `reg_ids`. **Only three of the 24 rows are
visible to the counter**, and they are exactly the three the freeze names: register S080 (SAMR record),
S088 (JMU copy), S096 (HIT specification). The other 21 rows are non-theme and cannot flip
`QUARANTINE_BLOCKED_ADOPTED` this round.

Baseline of the frozen counter on the landed tree (read-only; it writes nothing):

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && TMPDIR=<scratch> python3 corpus/evidence/round54/c2-count.py
ENTRIES=0/2 (min 2) REFUSED_ENTRIES=0
...
QUARANTINE_VERDICTS=0/3 (S080,S088,S096)
QUARANTINE_BLOCKED_ADOPTED=0
C2=FAIL
EXIT=1
```

`QUARANTINE_VERDICTS=0/3` is not a slice defect: `corpus/lessons/round-54.md` does not exist yet
(`LESSON_R54_EXISTS False`), so the counter's `lesson` is the empty string and it finds no verdict
lines at all. The 3/3 the freeze demands is a round-54-lesson obligation, not a lesson-history
obligation — see §5.

## 3. The coverage census against the counter's own regex

`VERDICT_RE` (`c2-count.py:84`) is
`register\s+\`?(S\d{3,})\`?.*?verdict[:=]?\s*\**\`?(present|absent-as-written|unverifiable|fabricated)\`?`
— one line, `register` then the id then the word `verdict`, then one of four verdict words. The counter
searches **only** `corpus/lessons/round-54.md` (`c2-count.py:150,160,265-268`). Reading every file in
`corpus/lessons/` with that exact regex:

```
$ python3 census.py   # counter's VERDICT_RE imported unmodified
SLICE_IDS 24
WITH_VERDICT_RE_LINE 15 S082 S084 S086 S093 S094 S095 S096 S104 S105 S108 S110 S111 S112 S114 S120
WITHOUT_VERDICT_RE_LINE 9 S077 S080 S088 S116 S125 S100 S101 S102 S103
```

**Correction to round-53 W1's "18 of 24 lack the canonical line"** (`R53ExecQuarantine.md` §5, and
`corpus/lessons/round-53.md:70`). That count came from the narrower grep `register S[0-9]* (round`,
which misses the round-47/round-49 prose forms. Under the counter's actual regex, **9** of 24 rows lack
a matching line, not 18: nine of round-53's eighteen (S082 S084 S086 S093 S094 S095 S096 S108 S110)
*do* have a VERDICT_RE-matching line (round-47.md:205-208, round-49.md:111-124). The nine that truly
lack one are S077 S080 S088 S116 S125 S100 S101 S102 S103. The gap count is a fact about the lane's
*lesson history*; it is not what the counter reads, which is the new round-54 lesson only.

## 4. Per-row table — verdict, its lesson file:line, and whether a VERDICT_RE line exists

Verdict column is the lane's own latest verdict-bearing lesson line (not my judgement). "REG_CANON"
= a line matching the counter's VERDICT_RE exists somewhere in `corpus/lessons/`.

| register id | verdict | lesson file:line giving the verdict | REG_CANON | canonical line / note |
|---|---|---|---|---|
| S077 | present | `corpus/lessons/round-48.md:42` (r42 `unverifiable` at `round-42-verifier-spotcheck.md:120` superseded) | no | draft below |
| S080 | absent-as-written | `corpus/lessons/round-48.md:43` | no | draft below — **theme row** |
| S082 | absent-as-written | `corpus/lessons/round-49.md:111` | yes | `round-49.md:111` |
| S084 | absent-as-written | `corpus/lessons/round-49.md:115` | yes | `round-49.md:115` |
| S086 | absent-as-written (cited homepage) | `corpus/lessons/round-49.md:118`; r48 `present` (companion capture) at `round-48.md:46` — scope split, not a contradiction | yes | `round-49.md:118` |
| S088 | absent-as-written | `corpus/lessons/round-48.md:47` | no | draft below — **theme row** |
| S093 | present (disputed, ruled present as-substance) | `corpus/lessons/round-47.md:205`; r48 `present — disputed` at `round-48.md:48`; ruling `round-48-verifier-spotcheck.md:56` | yes | `round-47.md:205` |
| S094 | present | `corpus/lessons/round-47.md:206`; `round-48.md:49` | yes | `round-47.md:206` |
| S095 | absent-as-written | `corpus/lessons/round-49.md:122` | yes | `round-49.md:122` |
| S096 | absent-as-written | `corpus/lessons/round-49.md:124` | yes | `round-49.md:124` — **theme row** (HIT spec; q2 exact, q1/q3 spliced, ISO for GB/T) |
| S104 | absent-as-written | `corpus/lessons/round-51.md:78`; r48 `present` at `round-48.md:52` — later lesson governs | yes | `round-51.md:78` |
| S105 | absent-as-written | `corpus/lessons/round-51.md:80` | yes | `round-51.md:80` |
| S108 | present | `corpus/lessons/round-47.md:207` | yes | `round-47.md:207` |
| S110 | present | `corpus/lessons/round-47.md:208` | yes | `round-47.md:208` |
| S111 | present | `corpus/lessons/round-51.md:82` | yes | `round-51.md:82` |
| S112 | absent-as-written | `corpus/lessons/round-51.md:84` | yes | `round-51.md:84` |
| S114 | absent-as-written | `corpus/lessons/round-51.md:86`; r48 `present` at `round-48.md:58` — later lesson governs | yes | `round-51.md:86` |
| S116 | present | `corpus/lessons/round-48.md:59`; earlier r46 hand-check at `round-46.md:263` | no | draft below |
| S120 | present | `corpus/lessons/round-51.md:88` and `round-52.md:72` (r52 supersedes r51's bad `char 39411`, see `round-52.md:15`) | yes | `round-52.md:72` |
| S125 | present | `corpus/lessons/round-48.md:61` | no | draft below |
| S100 | present | `corpus/lessons/round-48.md:62`; r42 `unverifiable` (family) at `round-42-verifier-spotcheck.md:121` superseded | no | draft below |
| S101 | present | `corpus/lessons/round-48.md:63` | no | draft below |
| S102 | present | `corpus/lessons/round-48.md:64` | no | draft below |
| S103 | present | `corpus/lessons/round-48.md:65` | no | draft below |

No slice row lacks a verdict statement somewhere: `corpus/lessons/round-48.md:42-65` is a table over the
identical 24 ids (set equality checked: `SLICE_MINUS_R48 []`, `R48_MINUS_SLICE []`), tally
"16 present (including S104's literal disclosure text), 8 absent-as-written, 0 unverifiable"
(`round-48.md:67`). Rows with **no** verdict anywhere: **none**.

## 5. Drafted canonical lines (for the L1 to place in `corpus/lessons/round-54.md`)

Drafted from each row's own latest lesson verdict, without re-judging. Format per the seat spec:
`register \`S0xx\` (roundN) — <url> — verdict: <v> — see <lesson path:line>`. The `roundN` is the
register row's own round cell; the URL is the register row's cited source (S100–S103's source cell
holds a gate heading, not a URL, so the gate heading is reproduced). Verified against the counter's
own regex — all ten match, all with the intended id and verdict word:

```
$ python3 verify_drafts.py
MATCH True ('S077', 'present') | register `S077` (round1) — https://doi.org/10.1186/s13643-020-01542-z …
MATCH True ('S080', 'absent-as-written') | register `S080` (round1) — https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F …
MATCH True ('S088', 'absent-as-written') | register `S088` (round2) — https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf …
MATCH True ('S096', 'absent-as-written') | register `S096` (round2) — https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc …
MATCH True ('S116', 'present') | register `S116` (round4) — https://aclanthology.org/N18-1074.pdf …
MATCH True ('S125', 'present') | register `S125` (round6) — http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc …
MATCH True ('S100', 'present') | register `S100` (round3) — #### Gate — S100 …
MATCH True ('S101', 'present') | register `S101` (round3) — #### Gate — S101 …
MATCH True ('S102', 'present') | register `S102` (round3) — #### Gate — S102 …
MATCH True ('S103', 'present') | register `S103` (round3) — #### Gate — S103 …
```

```
register `S077` (round1) — https://doi.org/10.1186/s13643-020-01542-z — verdict: present — see corpus/lessons/round-48.md:42
register `S080` (round1) — https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F — verdict: absent-as-written — see corpus/lessons/round-48.md:43
register `S088` (round2) — https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf — verdict: absent-as-written — see corpus/lessons/round-48.md:47
register `S096` (round2) — https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc — verdict: absent-as-written — see corpus/lessons/round-49.md:124
register `S116` (round4) — https://aclanthology.org/N18-1074.pdf — verdict: present — see corpus/lessons/round-48.md:59
register `S125` (round6) — http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc — verdict: present — see corpus/lessons/round-48.md:61
register `S100` (round3) — #### Gate — S100 — verdict: present — see corpus/lessons/round-48.md:62
register `S101` (round3) — #### Gate — S101 — verdict: present — see corpus/lessons/round-48.md:63
register `S102` (round3) — #### Gate — S102 — verdict: present — see corpus/lessons/round-48.md:64
register `S103` (round3) — #### Gate — S103 — verdict: present — see corpus/lessons/round-48.md:65
```

Scope of the block: the nine gap rows of §4 (S077 S080 S088 S116 S125 S100 S101 S102 S103) plus S096.
S096 is included because the counter reads **only** `corpus/lessons/round-54.md` — its existing
canonical line lives in `round-49.md:124` and is invisible to the counter, so S096's theme verdict must
be restated in the new lesson too. The other fourteen rows (S082 S084 S086 S093 S094 S095 S104 S105 S108
S110 S111 S112 S114 S120) need no draft: they already have a VERDICT_RE-matching line, and none of them
is visible to the counter this round.

## 6. What the counter will do with these lines — simulated, and two hazards

```
$ python3 sim2.py
REG_IDS ['S080', 'S088', 'S096']
SIM_DRAFTS_ONLY verdicts=3/3 {'S080': 'absent-as-written', 'S088': 'absent-as-written', 'S096': 'absent-as-written'} blocked=0
SIM_WITH_LATE_UNVERIFIABLE verdicts=3/3 {'S080': 'unverifiable', 'S088': 'absent-as-written', 'S096': 'absent-as-written'} blocked=1
SIM_PROSE_TAIL verdicts=3/3 {'S080': 'absent-as-written', 'S088': 'absent-as-written', 'S096': 'absent-as-written'} blocked=0
SIM_THEME_ONLY verdicts=3/3 {'S080': 'absent-as-written', 'S088': 'absent-as-written', 'S096': 'absent-as-written'} blocked=0
```

With the three theme lines present in the round-54 lesson the counter reaches
`QUARANTINE_VERDICTS=3/3` with `QUARANTINE_BLOCKED_ADOPTED=0`: none of the three is `fabricated` or
`unverifiable`, so no bound document is blocked. Note the verdicts are the *register row's* verdicts
(`absent-as-written` for S080/S088/S096) — they say the register's own quote is not written as the
source renders it, not that the documents are unusable; S080's hand-check (`round-48/w2/QuarantineS080.md`)
confirms every datum (GB/T 7714-2025, 2025-12-02, 2026-07-01) is on the captured page.

**Hazard 1 — last match wins.** `c2-count.py:265-268` overwrites `verdicts[id]` on every matching line,
so a *later* line naming S080 with `unverifiable` silently flips the verdict and sets
`QUARANTINE_BLOCKED_ADOPTED=1` (shown above). Any prose in the round-54 lesson that mentions
`register \`S080\`` must not carry a second verdict word, and the three canonical theme lines should be
placed after such prose.

**Hazard 2 — the id space collides.** The register id `S101` (never-checked family, gate heading) and
the *lane* registry row `S101` (`corpus/SOURCES.md:111`, the HIT data specification) are different
documents in different id spaces, and `c2-count.py` matches `S101` in the lesson by the register id.
The drafted `register \`S101\` (round3)` line names the register row; the HIT specification the C2
predicate holds as lane S101 is register row **S096**. Writing a `register \`S101\`` line that names the
HIT document's URL would put the wrong id on the theme URL and leave S096 uncovered.

## 7. Limits of this seat

- I did not re-judge any row: every verdict above is quoted from a lesson line, and every drafted line
  carries that lesson's file:line. Where lessons disagree (S104, S114 present in r48 vs
  absent-as-written in r51; S077 r42 unverifiable vs r48 present; S093 disputed) I took the later
  lesson and cited both, as round-53 did.
- `QUARANTINE_VERDICTS=3/3` is a simulation over the counter's own regex and its own `reg_ids` loop
  with a hypothetical round-54 lesson; the counter itself was run only on the real tree (§2). I did not
  write `corpus/lessons/round-54.md`, so the counter still prints `0/3` today.
- The other 21 rows are not visible to the counter this round (no theme URL); their canonical lines
  are documentation completeness for a future round, not a score input.

VERDICT: attacked the round-54 quarantine slice (24 rows) — re-derived it, found the counter reads only
the new round-54 lesson and only 3 of 24 rows (S080/S088/S096), corrected round-53's "18 of 24 lack the
canonical line" to 9 under the counter's own regex, tabled every row's verdict with its lesson
file:line, and drafted 10 VERDICT_RE-matching canonical lines (all 9 gaps plus S096's restatement) that
take the counter to a simulated `QUARANTINE_VERDICTS=3/3, QUARANTINE_BLOCKED_ADOPTED=0`, with two
last-match-wins / id-collision hazards flagged for the L1.
