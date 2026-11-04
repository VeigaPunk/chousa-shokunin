# R75Scribe — round 75, wave w1 (scribe)

Seat: R75Scribe. Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Frozen revision read: `43a7a0db52c8aabdf32735f58e09610e05200e79`.
Date: 2026-11-04. Lane role: leaf member (no dispatch performed).

## Behavior delivered

Three `corpus/SOURCES.md` registry rows (guessed ids **S184–S186**) and two lesson `## Mistakes`
rows drafted for round 75, each with all eleven registry cells, a ≤25-word located quote taken
verbatim from the committed tree with its line number, and an admit/reject decision with reason and
flip. **Drafted, not committed** — `corpus/SOURCES.md` and `corpus/lessons/` were not touched.

Draft artifact: `.ufo/waves/round-75/w1/R75Scribe/draft.md`

### The admit/reject set

| id | source | decision | tier / status |
|---|---|---|---|
| `S184` | `corpus/lessons/round-74-verifier-spotcheck.md` (routed defects 1 and 2) | **admit** — the only committed source carrying both r75 claim grounds; precedent `S180`/`S182` admit the same source class | B / mined |
| `S185` | `corpus/QUALITY.md` criterion 126 | **reject** — the corpus's own admission bar, not a place facts come from; no lane in the fleet registers a `corpus/QUALITY.md` row (verified across all 20 lanes) | C / rejected |
| `S186` | `.ufo/waves/round-74/w1/R74Critic/forge-order-oracle.py` + `.log` | **admit** — executed attack evidence (the log carries the matrix's own `LOADER_MATRIX=9/9 C1=PASS` verdict line), not intent text; the r75 forger copy is byte-identical (sha256 `180d1a3d92be9e13…`) | B / mined |

Used-by for `S184` and `S186`: `corpus/lessons/round-75.md`. `S185` used-by: `—`.
All three: `own-work`, opened `2026-11-04`, recheck `on-release`.

### Located quotes (all character-exact against committed bytes)

- `S184` — `corpus/lessons/round-74-verifier-spotcheck.md:73` (20 words): `before any future successor binds a candidate-running counter, meet existing QUALITY 126 with committed prefreeze detection-forger controls and record limits`
- `S184` — `corpus/lessons/round-74-verifier-spotcheck.md:74` (13 words): `append a correction to the lesson's quoted-word counts (16/11 whitespace tokens, not 18/13)`
- `S185` — `corpus/QUALITY.md:1002` (25 words): `A counter that runs a candidate tool binds a claim only after a committed detection-forger battery has passed it, and the battery's limits are recorded`
- `S186` — `.ufo/waves/round-74/w1/R74Critic/forge-order-oracle.py:3` (13 words): `Never reads --lane bytes nor any repository content. Scores 9/9 on the frozen`
- `S186` — `.ufo/waves/round-74/w1/R74Critic/forge-order-oracle.log:11` (2 words): `LOADER_MATRIX=9/9 C1=PASS`

### Lesson `## Mistakes` rows (draft for `corpus/lessons/round-75.md`)

1. **class** required prefreeze detection-forger battery omitted; a source-blind order oracle passed the frozen matrix and a digest was mistaken for discrimination — **evidence** `S184` routed defect 1; `S186`; `corpus/evidence/round75/controls/before-battery-r74-matrix.txt:28` (`BATTERY=FAIL forgers_rejected=2/5 positive=2/2`, exit 1) — **captured-by** QUALITY 126 (`corpus/QUALITY.md:1002`), committed before the r74 freeze, plus the r74 non-author verifier's admission ruling — **fix** r75's committed prefreeze battery: `after-battery-v2-matrix.txt:28` (`BATTERY=PASS forgers_rejected=5/5 positive=2/2`, exit 0); the successor matrix shuffles case order with a printed seed and adds three content-decidable cases; the order oracle is rejected at `order-oracle-through-v2.txt:74` (`LOADER_MATRIX=5/12 MATRIX=FAIL`, exit 1).
2. **class** recorded located-quote token counts contradict the quoted bytes (18/13 recorded vs 16/11 derived) — **evidence** `S184` routed defect 2; `corpus/lessons/round-74.md:8-9`; `before-c2.txt:4` (`DERIVED=S182:16 S183:11 RECORDED=S182:18 S183:13`) — **captured-by** the r74 non-author verifier spot-check (status-neutral routed defect) — **fix** one append-only `## Correction — round-74 quote counts` block in `corpus/lessons/round-74.md` naming 16/11 derived and 18/13 superseded with zero removed lines, checked by the frozen `corpus/evidence/round75/c2-count.py` Q1–Q4; at the frozen revision the block is absent and the counter reads `before-c2.txt:9` (`C2=FAIL checks=1/4`).

## Gates observed

| gate | result |
|---|---|
| candidate sources opened in the committed tree at `43a7a0db…` (never a working-copy path) | done, all four files |
| quotes verbatim with line number, ≤25 words | 12/12 verified character-exact |
| registry row grammar (NF=13, kind/tier/status enums, opened date, recheck cadence, used-by path) | validated with the fleet's own `scripts/sources-census.sh` on a scratch copy: exit 0, **no new finding** vs baseline (A/B diff empty) |
| real lane untouched | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, same five pre-existing W04 warnings, `chousa ok` |
| scratch root removed | the `trap 'rm -rf -- "$S"' EXIT` guard did **not** fire in every harness invocation (some commands ran in a temporary shell that lost the session's trap), leaving six `fixture.*` dirs; the seat scratch root was therefore removed **explicitly** with `rm -rf -- /fast/scratch/hyaku/chousa-r75/R75Scribe/` (exit 0) and its absence re-verified. Sibling seat scratch roots (`L1`, `R75Critic`, `R75Review`, `R75Scout`) were left untouched. |
| no commits, no pushes, no lane/fleet git mutation, no network, no subagents, no production edits | none performed |

## Touched surfaces

- **Written (this seat's own output only):** `.ufo/waves/round-75/w1/R75Scribe/draft.md` and
  `.ufo/waves/round-75/w1/R75Scribe.md` (this report).
- **Read-only:** the four candidate files, `corpus/SOURCES.md`, `corpus/QUALITY.md`,
  `corpus/lessons/round-73.md`, `corpus/lessons/round-74.md`,
  `corpus/lessons/round-74-verifier-spotcheck.md`, `corpus/evidence/round75/**`,
  `corpus/evidence/round74/loader-matrix.py`, `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`.
- **Scratch (removed):** `/fast/scratch/hyaku/chousa-r75/R75Scribe/fixture.*` — a full committed
  `corpus/` tree copy used only as a registry-validator target.

## Findings

1. **The S185 (QUALITY.md) row is a reject, and this is a scope judgement the L1 should confirm.**
   `corpus/QUALITY.md` is where admission criteria live, and the `corpus/SOURCES.md` header states
   the two are separate things ("Admission criteria live in `corpus/QUALITY.md`; a row here is a
   claim that its author opened the source…"). Registering the corpus's own admission bar as a
   source of corpus content is self-referential. Cross-lane check: no lane's `corpus/SOURCES.md`
   carries a row whose *source* cell names `corpus/QUALITY.md` (all 20 lanes scanned; the
   `QUALITY.md` strings that do appear are criterion references inside `scope`/`teaches` cells or in
   prose headers). Lane practice agrees — r73 cites "QUALITY 132", r74 cites "existing QUALITY 120
   and 126" inline in lessons rather than as rows. The flip is recorded in the row: admit it scoped
   to criterion 126 if an admitted entry ever cites `corpus/QUALITY.md` as the *origin* of its
   content rather than as the bar that content must meet.
2. **A quote defect in my own draft, caught and corrected.** My first verification pass reported the
   criterion-126 quote as present at `corpus/QUALITY.md:1002`, but the committed text reads
   `detection-forger`, not `detection-forge`. A byte-level re-check (`hexdump` + first-difference
   scan) located the divergence at the trailing `r`; the lane's own vocabulary is `detection-forger`
   (r74 spot-check line 73, and 1 occurrence of `detection-forger` lane-wide vs 0 of the other
   spelling). The draft was corrected and **all twelve** quoted strings were then re-verified
   character-exact. Recorded in the draft as §3a rather than silently fixed.
3. **`E11` is a landing-order constraint for the author.** `S184`/`S186` are `mined` with
   `used-by: corpus/lessons/round-75.md`, and that file does not exist at the frozen revision. The
   validator resolves `used-by` against the filesystem, so the rows must land with (or after) the
   round-75 lesson that cites them, or they will emit `E11`. In the scratch validation a
   placeholder lesson file stood in for it; that is the only thing the placeholder stood in for.
4. **The r75 forger is byte-identical to the r74 attack probe.** `corpus/evidence/round75/forgers/
   forge-order-oracle.py` and `.ufo/waves/round-74/w1/R74Critic/forge-order-oracle.py` are the same
   bytes (sha256 `180d1a3d92be9e13108c88d81a2fb24ecbfbfa13ee1fac5ee208b8659b84ff1c`, `diff` empty).
   This is why `S186` is admitted as a source: the surviving forge is a committed, re-openable
   artifact, not an unrecorded probe.
5. **Rounds 72/73/74 are the registry precedent, not an accident.** `S180` (r72 spot-check) and
   `S182` (r73 spot-check) are `own-work`/B/`mined` with `used-by` pointing at the next round's
   lesson — exactly the shape drafted for `S184`/`S186`. `S183` (r73 counter) is `own-work`/C/
   `rejected` with a flip — the shape drafted for `S185`.
6. **The C2 after-state is not yet committed.** At `43a7a0db…` the lesson has no
   `## Correction — round-74 quote counts` block and the frozen counter reads
   `C2=FAIL checks=1/4` (`before-c2.txt:9`). Lesson row 2 is written as the *required* append-only
   correction with the counter named as its check; it does not assert an after-state that does not
   exist. `corpus/evidence/round75/controls/` holds `before-c2.txt` but no `after-c2.txt`.

## Out of scope / not done

- Nothing committed to `corpus/SOURCES.md`, `corpus/lessons/`, or any other production path.
- No instrument was executed as a claim: `matrix-battery.py`, `loader-matrix-v2.py`, `c2-count.py`,
  `ref-counter.py`, `corpus/evidence/round75/forgers/*.py` were read as bytes only. Every
  battery/counter verdict quoted above comes from the **committed receipts**, not from a fresh run.
- No admission decision is claimed on the lane's behalf — the admit/reject set is a draft for L1 and
  for the non-author spot-check the round requests.
- The optional `## Search log` bullet in draft §4 is offered for the author to include or drop; it
  was not added anywhere.

## Tooling

No tool was installed or upgraded by this seat. Channel n/a, version n/a, reason n/a — the work
needed only `git`, `python3`, and the fleet's existing `scripts/sources-census.sh`, all already
present. Per `/home/vgpnk/.omp/agent/RULES.md`, no pacman transaction was attempted (all pacman
transactions are paused host-wide), and no `~/.local/bin` or other PATH directory was touched.

## Commands run and exits

Read-only inspection of committed bytes (all `git -C <lane> show <rev>:<path>` or
`git -C <lane> ls-tree`; exit 0 throughout): `corpus/evidence/round75/claims.md`,
`corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/lessons/round-73.md`, `corpus/lessons/round-74.md`,
`corpus/lessons/round-74-verifier-spotcheck.md`, `.ufo/waves/round-74/w1/R74Critic/forge-order-oracle.{py,log}`,
`corpus/evidence/round75/{loader-matrix-v2,matrix-battery,c2-count,ref-counter}.py`,
`corpus/evidence/round75/controls/*`, `corpus/evidence/round74/loader-matrix.py`.

Verification commands (each run inside `S=/fast/scratch/hyaku/chousa-r75/R75Scribe` with
`D=$(mktemp -d "$S/fixture.XXXXXX")` and `trap 'rm -rf -- "$S"' EXIT`):

| command | exit |
|---|---|
| `git -C "$LANE" archive $REV corpus \| tar -x -C "$D/lane"` (scratch corpus copy) | 0 |
| `python3` quote-verification harness (substring + token count per quote) | 0 — 12/12 pass after the §3a correction; 1 false positive on the first pass |
| `sources-census.sh validate --file "$D/lane/corpus/SOURCES.md" --today 2026-11-04` (baseline, no new rows) | 0 |
| `python3` row-insertion harness (parse the three rows out of `draft.md`, insert after `S183`) | 0 |
| `sources-census.sh validate --file "$D/lane/corpus/SOURCES.md" --today 2026-11-04` (with the three rows) | 0 |
| `diff "$D/A.txt" "$D/B.txt"` | 0, no output — no new finding introduced |
| `sources-census.sh census --file "$D/lane/corpus/SOURCES.md" --today 2026-11-04` | 0 — rows 186, tier A123/B48/C15, status mined150/queued19/rejected17 |
| `sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` (real lane, read-only) | 0 — five pre-existing W04 warnings, `chousa ok` |
| `ls /fast/scratch/hyaku/chousa-r75/R75Scribe` (scratch removed) | absent |

## Artifact paths

- `.ufo/waves/round-75/w1/R75Scribe/draft.md` — the three registry rows (all eleven cells each),
  the two lesson `## Mistakes` rows, the located quotes, the admit/reject reasons and flips, the
  validation record, the §3a quote-defect record, and the optional search-log bullet.
- `.ufo/waves/round-75/w1/R75Scribe.md` — this report.
