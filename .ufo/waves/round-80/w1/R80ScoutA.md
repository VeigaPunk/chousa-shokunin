# R80ScoutA — Gate-record surface survey (chousa, round 80)

Seat: **R80ScoutA** (scout, wave 1, round 80, lane `chousa-shokunin`).
Scope: per-surface reconnaissance of the lane's Gate-record surface — the ground C2 moves on.
**Read-only.** No production edit, no lane/fleet git or jj mutation, no commit, no push, no
subagent dispatch, no network.

- Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`
- Base revision: `b7803829922770b890e9f4efdd30d12c3695439a` (round-79 lane tip)
- Full survey: **`.ufo/waves/round-80/w1/R80ScoutA/survey.md`**
- Receipts: **`.ufo/waves/round-80/w1/R80ScoutA/receipts/`** (7 files)
- Scratch: `/fast/scratch/hyaku/chousa-r80/R80ScoutA/` — **deleted before yield** (see §6)
- Tooling: **none installed.** Stock `git`, `grep`, `wc`, `sed`, `python3` (3.x, stdlib only).

---

## 1. What I was asked and what I did

Four sub-questions, all answered against committed bytes only:

1. **The table.** Every lesson file matching `round-<n>.md` with n ≥ 70 (rounds 70–79; ten files),
   every located quote in each `## Gate` block, re-opened at the cited revision, `grep -c`'d and
   `wc -w`'d.
2. **Every defective record beyond S196/S197/S198.**
3. **The counter's audit window and its blind spot** — what
   `corpus/evidence/round80/gate-grounding-check.py` audits at `--since-round 79`, and what escapes
   at `--since-round 60` / `--since-round 1`.
4. **Round-79.md's own counts** — S196 states 25, S197 states 24.

Every claim below names the command, the receipt path, the observed line, and the exit code.

---

## 2. Findings

### 2.1 The table (survey.md §1)

**33 records · 17 ok · 10 mismatch · 5 absent · 1 no-quote-stated.**
Machine-readable: `receipts/table.json`. Command trace: `receipts/measure-out.txt`.

Extraction was script-driven with a **provenance gate**: each extracted quote was first proven to
appear verbatim (after whitespace normalisation, for the five line-wrapped quotes) in its own
lesson's `## Gate` block, so this seat cannot have paraphrased a quote into existence. The one
record whose lesson states its quote as two pieces plus a description (S177) was reconstructed from
the cited SKILL.md row and measured independently; this is flagged in the survey.

### 2.2 Twelve defective records beyond the three the round-79 closure named

| row | lesson | class | stated | measured | evidence |
|---|---|---|---|---|---|
| **S170** | r70 | mismatch | 10 | 11 | `receipts/measure-out.txt` (frag 1–2, joined `wc -w` → 11) |
| **S171** | r70 | **absent** | 10 | 9 | `grep -c -F '…selftest.dcCFup'` on `recon-run-r70.txt` → **0**, exit 1; the file holds the **K1Yhut** variant |
| **S173** | r71 | mismatch | 21 | 20 | `wc -w` → 20; located at line 84 ✓ |
| **S174** | r71 | **absent** | 22 | 22 | `grep -c -F` → **0**, exit 1; the sentence is stitched across lines 308/309, each half prefixed `# ` |
| **S175** | r71 | mismatch | 6 | 5 | 1 + 2 + 2 = 5 |
| **S176** | r71 | mismatch | 10 | 9 | located at `before-g08-selftest-partial.txt:65` ✓, count off by one |
| **S178** | r72 | mismatch | 11 | 13 | `wc -w` → 13 — the largest count error in the survey |
| **S179** | r72 | mismatch | 6 | 5 | 1 + 2 + 2 = 5 |
| **S182** | r74 | mismatch | 18 | 16 | **already corrected in-lane** by round-74.md's `## Correction — round-74 quote counts` block |
| **S183** | r74 | mismatch | 13 | 11 | same in-lane correction block |
| **S191** | r77 | **absent** | 11 | 11 | `grep -c -F` → **0**, exit 1; quote split across lines 163–164 (whitespace-normalised: present) |
| **S193** | r78 | **absent** | 11 | 11 | lesson renders `SKILL.md`, file renders `` `SKILL.md` ``; `grep -c` → **0** vs **1** for the backticked form |

Two findings worth the integrator's attention specifically:

- **S176 inherits the count defect it was written to fix.** S176 is the *corrected* attribution of
  S171's quote (location right, quote verbatim) — but its stated count (10) was copied from S171's
  defective cell and is off by one (9). The round-71 lesson re-derived the *location* and did not
  re-derive the *count*.
- **S193 is a fourth "located quote absent from the file it cites"**, of the same class as the
  round-79 closure's S198 finding, one round earlier, and not among the three the closure named.
  Its stated count (11) is correct for *both* renderings, so a word-count check cannot see it — only
  a byte-exact substring check does.

**S171 is a known defect that remains open to the counter.** It is recorded in-lane
(`round-70.md:45` = D-70-1; `round-71.md:33` = fixed append-only; registry row S176's `teaches`
cell opens `supersedes S171 —`), but the round-70 `## Gate` cell is still defective in the committed
bytes and is structurally unreachable by the round-80 counter (§2.4).

### 2.3 The counter's window, and the blind spot's size (survey.md §3)

Measured with the frozen instrument (sha256 `d9e426216665a098cd90adf8fbf5e5dd62e02dc7b5b707c322b404b3eb55c553`,
verified identical in the lane working tree and in the scratch copy), run inside a scratch
`git clone --shared` of the lane:

| `--since-round` | TIPS | AUDITED | `audited=` |
|---|---|---|---|
| 79 (default) | 191 | **3** | `S196,S197,S198` |
| 78 | 191 | 6 | `S193,S194,S195,S196,S197,S198` |
| 74 | 191 | **17** | `S182,…,S198` |
| 73 / 72 / 71 / 70 / 69 / **60** / 30 / 26 / **1** | 191 | **17** | `S182,…,S198` |

The default run reproduces the frozen control byte-for-byte:
`GATE_GROUNDING=FAIL unresolved=3 superseded_resolved=0 audited=S196,S197,S198`, exit 1
(`receipts/blindspot-out.txt`).

- **79 → 60 adds 14 rows:** `S182 S183 S184 S185 S186 S187 S188 S189 S190 S191 S192 S193 S194 S195`.
- **60 → 1 adds nothing.** The counter's `DECIDED` regex
  (`gate-grounding-check.py:22`, `^- (?:Admit|Reject) (S\d{3,})\b`) matches only the plain-bullet
  decision form the lane has used since round 74. Rounds 26–73 record decisions as **markdown
  table rows** (`| S168 |`) or **bold bullets** (`- **Admit S180**`), neither of which it matches.

**Blind-spot size: 102 of the 119 registry rows that carry a Gate decision in a `round-<n>.md`
lesson are invisible to the counter at every `--since-round` value.** Census in
`receipts/table-out.txt` §C and `receipts/blindspot-out.txt` §B. Within my assigned round-70..79
band the invisible rows are exactly **S168–S181** (14 rows) — where 8 of the 12 new defects live.

The fix is a `GATE-RECORD` line per row, not a wider window: planting one for the table-row row
S168 puts it in the audit set at `--since-round 79`
(`ROW S168 record=ok quote_words=16 … verdict=OK`, `receipts/r4-probe-out.txt` §1).

### 2.4 The `SUPERSEDED` branch cannot reach S171 (survey.md §3.3)

S171 is a **parent** row (superseded by S176), so it is never a tip and never appears in
`audited=`. The `SUPERSEDED` branch fires only when `rid in decided` — i.e. when the superseded
row's own id satisfies `DECIDED`. For S171 that never happens, because the round-70 lesson records
it as a table row. Measured (`receipts/superseded-probe-out.txt`):

```
--- GATE-RECORD for S176 (the superseder) only
    GATE_GROUNDING=FAIL unresolved=3 superseded_resolved=0 audited=S176,S196,S197,S198
--- same, but ALSO a '- Admit S171' bullet so S171 enters `decided`
    SUPERSEDED S171 by S176 record=ok verdict=RESOLVED
    GATE_GROUNDING=FAIL unresolved=3 superseded_resolved=1 audited=S176,S196,S197,S198
```

So **the one registry row whose Gate record is known-defective and already superseded is
structurally invisible to the counter at every window** — and the `superseded_resolved` counter
C2's predicate names can only ever count superseded rows whose decision was a plain bullet.

### 2.5 R3/R4 behaviour on the real defective records (survey.md §3.4)

Each record's own lesson quote and stated count were planted as a `GATE-RECORD` line in a scratch
`corpus/lessons/round-80.md` and the counter run at that scratch commit
(`receipts/r4-probe-out.txt`):

- **R4 cannot be satisfied by S196 at any stated count** — the quote is 27 words, so
  `words=25` gives `R4 quote is 27 words, record says 25` and `words=27` gives
  `R4 quote is 27 words (contract bound is 25)`. S196 can only be resolved by a **different,
  shorter** quote in a superseding row. S197's quote is exactly 25 and *can* be repaired in place
  (`words=25` → `record=ok … verdict=OK`).
- **R3 requires a single-line, byte-exact quote.** S174 (spans lines 308–309), S191 (spans lines
  163–164) and S193 (backtick difference) all fail R3 as their lessons write them; S193 passes
  immediately with the file's real backticked string (`record=ok … verdict=OK`).
- Correcting the counts to the measured values turns S170/S173/S178 green
  (`words=6/20/13` → all three `record=ok … verdict=OK`).

### 2.6 The C2 landing predicate is reachable (survey.md §3.5)

Built in the scratch clone — four new registry rows whose `teaches` cells open
`supersedes S196/S197/S198`, plus four `GATE-RECORD` lines in a scratch `corpus/lessons/round-80.md`,
with all four quotes `wc -w`-measured *before* planting:

```
LANE_REV=bc3060ac59ba493525d8a50a5d51dfa255132102 SINCE_ROUND=79 TIPS=192 AUDITED=4
ROW S199 record=ok quote_words=13 location=corpus/QUALITY.md:1056@ee70e6df19fe words=13 verdict=OK
ROW S200 record=ok quote_words=11 location=corpus/QUALITY.md:1054@ee70e6df19fe words=11 verdict=OK
ROW S201 record=ok quote_words=2 location=.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt:11@3eb4a3cad8fe words=2 verdict=OK
ROW S202 record=ok quote_words=3 location=.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt:8@3eb4a3cad8fe words=3 verdict=OK
SUPERSEDED S196 by S199 record=ok verdict=RESOLVED
SUPERSEDED S197 by S200 record=ok verdict=RESOLVED
SUPERSEDED S198 by S201 record=ok verdict=RESOLVED
GATE_GROUNDING=PASS unresolved=0 superseded_resolved=3 audited=S199,S200,S201,S202
exit=0
```
`GATE_GROUNDING=PASS unresolved=0 superseded_resolved=3` — **the frozen C2 predicate is met**, and
only with a **shorter** S196 quote (13 words measured, bound 25), which is the shape C2's own
sourced claim describes. The scratch clone was reset to the base revision afterwards
(`clone reset: True`); the lane repo was never written.

### 2.7 Part 4 — round-79.md's own counts: both confirmed

```
CMD: printf %s 'A subject-identity salt is defeated by any normalizer that knows its marker family, so the closure is a per-channel measurement and not a property of the salt' | wc -w
OUT: 27
CMD: printf %s 'A self-assessment counter validates each resolution line against the bytes it claims to repair, and its audit window covers every block rather than the newest' | wc -w
OUT: 25
```

- **S196 — CONFIRMED.** Stated 25, actual **27** — off by **two**, and over the ≤25-word bound.
- **S197 — CONFIRMED.** Stated 24, actual **25** — off by one, exactly **at** the bound (so R4's
  bound clause does not fire; only the count mismatch does).

Both quotes sit on the lines the lesson cites (`corpus/QUALITY.md` 1056 and 1054 @
`ee70e6df19fe`), so the anchors are right and only the counts are wrong — matching the round-79
closure's judgement that the admit decisions stand.

---

## 3. Confidence and remaining unknowns

**High confidence** (every claim re-derived by me from committed bytes, commands and outputs in
the receipts): the table and all 15 defective records; the `--since-round` sweep; the 102-row
blind spot and its cause; the S171 unreachability; the R3/R4 behaviour; the landing-predicate
reachability.

**Stated limits.**
- Five quotes (S177, S193, S194, S196, S197) are line-wrapped in the lesson markdown; their
  provenance was proven after whitespace normalisation, not byte-exactly. S177's lesson cell states
  its quote as *two pieces plus a description*; this seat reconstructed the whole cell string from
  the cited SKILL.md row 83 and measured it independently (12 words, present). Flagged in the
  survey.
- "Stated count" is taken to be the count of the quote as the lesson writes it, fragments joined by
  one space — the reading the round-80 counter's R4 implements (`len(quote.split())`). For a
  multi-fragment record (S169, S170, S175, S179) a different counting convention would change the
  verdict; the per-fragment counts are in `receipts/table.json` so any other convention can be
  re-applied without re-measuring.
- S185 states no quote ("Located anchor: criterion 126's text"). The cited line does carry
  criterion 126, so the *anchor* is right; there is no count to check and no quote a
  `GATE-RECORD` line could carry. That is a format gap, not a miscount, and this seat does not
  claim it is a defect the counter should flag.

**Open, not resolved here.**
- Whether the lane wants the 14 round-70..73 rows (S168–S181) machine-closed, and by what
  mechanism (retrofit `GATE-RECORD` lines for each, versus extending `DECIDED` to the table and
  bold-bullet forms). Widening `DECIDED` would pull in 102 rows, most of whose located quotes were
  written before the `## Gate` block carried one at all — a retrofit of that size is a lane
  decision, not a seat's.
- Whether the round-80 landing's four `GATE-RECORD` rows will use the 13/11/2/3-word quotes this
  seat measured, or the 15-word quote C2's sourced claim names. This seat measured that a 15-word
  quote for S196 exists and is present on the cited line; the exact wording is the lane's call.

---

## 4. What I did NOT do

- No edit to any file outside `.ufo/waves/round-80/w1/R80ScoutA/` and my scratch dir.
- No read of, or write to, `corpus/evidence/round79/` or `corpus/evidence/round80/` as *content* —
  both were read-only sources. The counter was **copied** into the scratch clone to be run; the
  lane's copy was never executed in place and never modified.
- No git/jj mutation in the lane or the fleet repo. The scratch clone's commits are in the scratch
  clone's history only (a `--shared` clone of the lane; its objects are the lane's, its commits are
  not), and the clone was reset to the base revision afterwards.
- No commit, no push, no `git`/`jj` write against the fleet root.
- No subagent dispatch (`task` tool not used), no `agent://all` broadcast, no network access.

---

## 5. Files written by this seat

```
.ufo/waves/round-80/w1/R80ScoutA.md            (this report)
.ufo/waves/round-80/w1/R80ScoutA/survey.md     (the full survey, §1-§5)
.ufo/waves/round-80/w1/R80ScoutA/receipts/measure-out.txt
.ufo/waves/round-80/w1/R80ScoutA/receipts/table-out.txt
.ufo/waves/round-80/w1/R80ScoutA/receipts/table.json
.ufo/waves/round-80/w1/R80ScoutA/receipts/blindspot-out.txt
.ufo/waves/round-80/w1/R80ScoutA/receipts/r4-probe-out.txt
.ufo/waves/round-80/w1/R80ScoutA/receipts/superseded-probe-out.txt
.ufo/waves/round-80/w1/R80ScoutA/receipts/landing-probe-out.txt
```

Every receipt cited above was copied out of scratch into this folder **before** scratch was
deleted.

## 6. Scratch lifecycle

`/fast/scratch/hyaku/chousa-r80/R80ScoutA/` held the `git clone --shared` scratch clone, the
measurement driver, the four probe scripts and their outputs. The clone was reset to
`b7803829922770b890e9f4efdd30d12c3695439a` (`clone reset: True`) and the whole directory was
removed after the receipts were copied into the wave folder. Nothing under `/tmp` was written;
no scratch path is cited as evidence.
