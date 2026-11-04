# Round 75 — SOURCES registry and lesson `## Mistakes` DRAFT (not committed)

Seat: R75Scribe (scribe, wave w1, round 75). Date opened: 2026-11-04.
Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Frozen revision read: `43a7a0db52c8aabdf32735f58e09610e05200e79`.
Status: **draft only.** Nothing in `corpus/SOURCES.md`, `corpus/lessons/`, or any production path was
written. Only this file (`.ufo/waves/round-75/w1/R75Scribe/draft.md`) was written.

## 0. What was opened, and how

Every candidate was opened in the **committed tree** at the frozen revision (`git show REV:path`),
never from a working-copy path, so each quote below is a committed-bytes quote.

| candidate | committed path opened at `43a7a0db…` | read |
|---|---|---|
| (a) | `corpus/lessons/round-74-verifier-spotcheck.md` | full file (78 lines); routed defects at lines 73–74 |
| (b) | `corpus/QUALITY.md` | line 1002 (criterion 126) |
| (c) | `.ufo/waves/round-74/w1/R74Critic/forge-order-oracle.py` | full file (45 lines) |
| (c) | `.ufo/waves/round-74/w1/R74Critic/forge-order-oracle.log` | full file (13 lines) |

Supporting reads (committed bytes at the same revision): `corpus/SOURCES.md` (schema header line 9,
rows S180–S183 at lines 192–195), `corpus/lessons/round-73.md` and `corpus/lessons/round-74.md`
(`## Mistakes` table shapes), `corpus/evidence/round75/c2-count.py`,
`corpus/evidence/round75/loader-matrix-v2.py`, `corpus/evidence/round75/controls/*`,
`corpus/evidence/round74/loader-matrix.py`, and the fleet script
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (row grammar, E/W codes).

## 1. Three registry rows — full eleven cells

Schema of `corpus/SOURCES.md` (header line 9): `id | source | kind | tier | scope | anchor | teaches |
status | opened | recheck | used-by`. IDs guessed as **S184–S186** (registry holds 183 rows at the
frozen revision; `S183` is the highest).

### S184 — ADMIT

| cell | value |
|---|---|
| id | `S184` |
| source | chousa round-74 verifier spot-check — `corpus/lessons/round-74-verifier-spotcheck.md` |
| kind | `own-work` |
| tier | `B` |
| scope | the two defects routed by the r74 non-author verifier: QUALITY 126 admission debt before a candidate-running counter may bind a claim, and the r74 lesson's miscounted located-quote token counts |
| anchor | `43a7a0db52c8aabdf32735f58e09610e05200e79`, `corpus/lessons/round-74-verifier-spotcheck.md` lines 73–74 ("Routed defects / operator notes", items 1 and 2); the file's own pins are reviewed landing `5f754bd12ec5d0d006ca05751250d5ee1caaf29e`, before `8a28732b3c1591b52449a982849b758cda6f4c45`, freeze `1eaa30ad248bbd3bd7469b2c17295fcda5fc02bb` |
| teaches | Bind a candidate-running counter only after a committed detection-forger battery has passed it; correct a miscounted token count append-only, never by rewriting the authored lesson |
| status | `mined` |
| opened | `2026-11-04` |
| recheck | `on-release` |
| used-by | `corpus/lessons/round-75.md` |

**Located quotes (each ≤25 words, verbatim, with line number):**

- line 73: `before any future successor binds a candidate-running counter, meet existing QUALITY 126 with committed prefreeze detection-forger controls and record limits` (20 words)
- line 74: `append a correction to the lesson's quoted-word counts (16/11 whitespace tokens, not 18/13)` (13 words)

**Decision: admit.** Reason: this is the lane's own non-author verifier record, and it is the only
committed source for both r75 claim grounds — the QUALITY 126 admission debt that C1 must discharge,
and the derived 16/11 token counts that C2's correction block must state. Precedent: `S180`
(r72 spot-check, own-work/B/mined) and `S182` (r73 spot-check, own-work/B/mined) admit the same
source class; `S182`'s scope is likewise "routed … defect and required public-path controls".
Scope is bounded to what the record states about the r74 closure and does not extend to the truth of
any counter or of arbitrary prose. Flip: if the r74 spot-check is ever amended, this row must be
re-derived against the amended bytes rather than kept as-is.

### S185 — REJECT

| cell | value |
|---|---|
| id | `S185` |
| source | chousa quality criteria corpus — `corpus/QUALITY.md` (criterion 126) |
| kind | `own-work` |
| tier | `C` |
| scope | criterion 126's own text as this lane's binding rule for admitting a candidate-running counter |
| anchor | `43a7a0db52c8aabdf32735f58e09610e05200e79`, `corpus/QUALITY.md` line 1002 (criterion 126) |
| teaches | REJECTED: `corpus/QUALITY.md` is this lane's admission-criteria corpus, not a place facts come from — the `corpus/SOURCES.md` header separates them ("Admission criteria live in `corpus/QUALITY.md`; a row here is a claim that its author opened the source and judged its tier"), and the r73/r74 lessons cite criterion numbers inline (r74 lesson "existing QUALITY 120 and 126") instead of registering criteria as rows; no lane in the fleet registers a `corpus/QUALITY.md` row; flip: admit it scoped to criterion 126's text if an admitted entry ever cites `corpus/QUALITY.md` as the origin of its content rather than as the bar that content must meet |
| status | `rejected` |
| opened | `2026-11-04` |
| recheck | `on-release` |
| used-by | `—` |

**Located quote (≤25 words, verbatim, with line number):**

- line 1002: `A counter that runs a candidate tool binds a claim only after a committed detection-forger battery has passed it, and the battery's limits are recorded` (25 words)

**Decision: reject.** Reason: the criterion is a gate the corpus is measured against, not a source
of corpus content; registering it would make the registry cite its own admission bar. This matches
lane practice (criteria cited inline in lessons: r73 lesson "QUALITY 132", r74 lesson "existing
QUALITY 120 and 126") and fleet practice (no lane's `corpus/SOURCES.md` carries a `corpus/QUALITY.md`
row). Flip stated in the `teaches` cell. The criterion's binding force for C1 is unaffected — it is
enforced by `corpus/evidence/round75/matrix-battery.py`, not by this row.

### S186 — ADMIT

| cell | value |
|---|---|
| id | `S186` |
| source | chousa r74 order-oracle forge probe and its receipt — `.ufo/waves/round-74/w1/R74Critic/forge-order-oracle.py` and `.ufo/waves/round-74/w1/R74Critic/forge-order-oracle.log` (own-work attack probe and its committed run log; the same bytes are frozen for r75 at `corpus/evidence/round75/forgers/forge-order-oracle.py`, sha256 `180d1a3d92be9e13108c88d81a2fb24ecbfbfa13ee1fac5ee208b8659b84ff1c` — verified byte-identical) |
| kind | `own-work` |
| tier | `B` |
| scope | the r74 loader matrix's source-blind discrimination failure: a counter that reads no repository bytes scored 9/9 on the fixed-order matrix |
| anchor | `43a7a0db52c8aabdf32735f58e09610e05200e79`, `forge-order-oracle.py` line 3 (module docstring) and `forge-order-oracle.log` line 11 (`LOADER_MATRIX=9/9 C1=PASS`), with the digest on `forge-order-oracle.log` line 1 |
| teaches | A CLI-boundary matrix with a fixed deterministic case order can be passed by a counter that reads no sources; binding a digest of an implementation establishes identity, not that the matrix discriminates forgeries |
| status | `mined` |
| opened | `2026-11-04` |
| recheck | `on-release` |
| used-by | `corpus/lessons/round-75.md` |

**Located quote (≤25 words, verbatim, with line number):**

- `forge-order-oracle.py` line 3: `Never reads --lane bytes nor any repository content. Scores 9/9 on the frozen` (13 words)
- `forge-order-oracle.log` line 11: `LOADER_MATRIX=9/9 C1=PASS` (2 words)

**Decision: admit.** Reason: executed attack evidence, not intent text. The probe's own docstring
admits it "Never reads --lane bytes" and the committed log records the matrix's own verdict line
(`LOADER_MATRIX=9/9 C1=PASS`), so the row supports exactly the claim it states — the r74 matrix was
not a discriminator — and nothing about any counter's correctness. Precedent: probe/receipt rows in
this lane are admitted at own-work/B (e.g. `S140`, `S148`, `S162`, `S165`, `S175`, `S179`);
`S153`/`S157` were rejected only because they were docstrings asserting intent with no execution
behind them, which is not the case here. Scope excludes any general forge-freedom claim. Flip: if
the r74 wave artifact is removed or re-frozen, re-derive this row against the surviving bytes.

## 2. Two lesson `## Mistakes` rows (draft for `corpus/lessons/round-75.md`)

Table shape copied from `corpus/lessons/round-73.md` (`| class | evidence pointer | captured-by | fix |`).

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| required prefreeze detection-forger battery omitted; a source-blind order oracle passed the frozen matrix and a digest was mistaken for discrimination | S184 routed defect 1 (`corpus/lessons/round-74-verifier-spotcheck.md:73`); S186 (`.ufo/waves/round-74/w1/R74Critic/forge-order-oracle.log:11`, `forge-order-oracle.py:3`); `corpus/evidence/round75/controls/before-battery-r74-matrix.txt:28` (`BATTERY=FAIL forgers_rejected=2/5 positive=2/2`, exit 1) | QUALITY 126 (`corpus/QUALITY.md:1002`), already committed before the r74 freeze; the r74 non-author verifier's admission ruling, which withheld admission rather than certifying the matrix | r75 discharges the debt with a committed prefreeze battery: `corpus/evidence/round75/matrix-battery.py` over seven salted subjects, result `corpus/evidence/round75/controls/after-battery-v2-matrix.txt:28` (`BATTERY=PASS forgers_rejected=5/5 positive=2/2`, exit 0); the successor matrix shuffles case order with a printed seed and adds three append-only-but-structurally-wrong cases decidable only from protected-file content; the order oracle is rejected at 5/12 (`corpus/evidence/round75/controls/order-oracle-through-v2.txt:74`, `LOADER_MATRIX=5/12 MATRIX=FAIL`, exit 1) |
| recorded located-quote token counts contradict the quoted bytes (18/13 recorded vs 16/11 derived) | S184 routed defect 2 (`corpus/lessons/round-74-verifier-spotcheck.md:74`); the authored lesson's own quotes (`corpus/lessons/round-74.md:8-9`); `corpus/evidence/round75/controls/before-c2.txt:4` (`DERIVED=S182:16 S183:11 RECORDED=S182:18 S183:13`) | the r74 non-author verifier spot-check, routed as a status-neutral count defect with no quote absence and no source disagreement | append-only correction: one `## Correction — round-74 quote counts` block in `corpus/lessons/round-74.md` naming the derived 16/11 and marking the recorded 18/13 superseded, with zero removed lines — checked by the frozen `corpus/evidence/round75/c2-count.py` (Q1 exactly one block, Q2 states 16/11, Q3 names 18/13 as superseded, Q4 zero deletions). At the frozen revision the block is absent and the counter reads `C2=FAIL checks=1/4` (`corpus/evidence/round75/controls/before-c2.txt:9`); the after-state is the C2 claim's landing content, not yet committed |

## 3. Draft validation actually performed

The three drafted rows were extracted from this file by a parser (not retyped) and validated with the
fleet's own registry validator against a **scratch copy**, under the seat's scratch root
`/fast/scratch/hyaku/chousa-r75/R75Scribe/`, so no fleet or lane file was touched. The scratch lane
copy was the full committed `corpus/` tree at the frozen revision
(`git archive 43a7a0db… corpus`), with the three rows appended inside the `## Registry` section
(immediately after the last registry row, `S183`, before the `## Paths` heading at line 197), plus a
placeholder `corpus/lessons/round-75.md` so the new rows' `used-by` paths resolve as they will once
the round-75 lesson lands.

Commands and exits, exactly as run:

```
# A — baseline, scratch copy, no new rows
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --file "$D/lane/corpus/SOURCES.md" --today 2026-11-04        # exit 0

# B — same file with the three drafted rows inserted
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --file "$D/lane/corpus/SOURCES.md" --today 2026-11-04        # exit 0

diff "$D/A.txt" "$D/B.txt"                                     # exit 0, no output
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census \
  --file "$D/lane/corpus/SOURCES.md" --today 2026-11-04        # exit 0
```

A and B produce **identical** finding sets: the five pre-existing W04 cross-scope duplicate-URL
warnings (`S051`, `S053`, `S073`, `S074`, `S075`) and `ok`. The three rows introduce **no new E or W
finding** — NF=13 rows, `own-work` kind, tiers `B`/`C`/`B`, statuses `mined`/`rejected`/`mined`,
`opened=2026-11-04` not in the future, `recheck=on-release` accepted as a symbolic cadence, and
both `used-by` paths present on disk.

Read-only check of the untouched real lane (not modified by this seat):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --root /home/vgpnk/Projects/shokunin chousa                   # exit 0
```
→ the same five W04 warnings and `chousa ok …/corpus/SOURCES.md`.

**Ordering gate for the author.** `E11` requires a mined row's `used-by` path to exist on disk at
validation time. `corpus/lessons/round-75.md` does not exist at the frozen revision, so the three
rows must not be committed before the round-75 lesson file that cites them (or the rows must be
staged with the lesson in the same change).

**Scratch cleanup.** The `trap 'rm -rf -- "$S"' EXIT` guard did not fire in every harness invocation
(some commands ran in a temporary shell that lost the session's trap), leaving six `fixture.*`
directories under the seat scratch root. The seat scratch root was therefore removed explicitly with
`rm -rf -- /fast/scratch/hyaku/chousa-r75/R75Scribe/` (exit 0) and its absence re-verified. No
sibling seat's scratch root was touched.

## 3a. A quote defect this seat caught in its own draft (recorded, not hidden)

The first verification pass of the QUALITY criterion 126 quote returned a **false positive**: the
harness reported the quote as present on line 1002, but the committed text reads
`detection-forger` (QUALITY.md:1002, and 1 occurrence lane-wide), while the drafted quote read
`detection-forge`. A byte-level re-check (`hexdump` of the line plus a first-difference scan)
located the divergence at the `r` of `forger`. The committed wording is authoritative and the draft
quote was corrected to `detection-forger`; the same word appears in the r74 spot-check's own routed
defect 1 (line 73: "committed prefreeze detection-forger controls"), so the lane's own vocabulary
is `detection-forger`.

All twelve quoted strings were then re-verified **character-exact** (substring test against the
committed line at the stated line number, plus a whitespace-token count) and all passed:

| quote | committed location | words | ≤25 |
|---|---|---|---|
| S184 quote A | `corpus/lessons/round-74-verifier-spotcheck.md:73` | 20 | yes |
| S184 quote B | `corpus/lessons/round-74-verifier-spotcheck.md:74` | 13 | yes |
| S185 quote | `corpus/QUALITY.md:1002` | 25 | yes |
| S186 quote (probe) | `.ufo/waves/round-74/w1/R74Critic/forge-order-oracle.py:3` | 13 | yes |
| S186 quote (receipt) | `.ufo/waves/round-74/w1/R74Critic/forge-order-oracle.log:11` | 2 | yes |
| S186 digest | `.ufo/waves/round-74/w1/R74Critic/forge-order-oracle.log:1` | 1 | yes |
| lesson counts | `corpus/lessons/round-74.md:8` / `:9` | 2 / 5 | yes |
| before-battery verdict | `corpus/evidence/round75/controls/before-battery-r74-matrix.txt:28` | 3 | yes |
| after-battery verdict | `corpus/evidence/round75/controls/after-battery-v2-matrix.txt:28` | 3 | yes |
| C2 derived/recorded | `corpus/evidence/round75/controls/before-c2.txt:4` | 4 | yes |
| C2 before verdict | `corpus/evidence/round75/controls/before-c2.txt:9` | 2 | yes |
| order-oracle-through-v2 verdict | `corpus/evidence/round75/controls/order-oracle-through-v2.txt:74` | 5 | yes |


## 4. Optional appendix — proposed `## Search log` bullet (author's to include or drop)

> Round 75 (2026-11-04): question — which committed bytes ground the round-75 loader-matrix and
> quote-count claims? Where: opened in the committed tree at `43a7a0db52c8aabdf32735f58e09610e05200e79` —
> `corpus/lessons/round-74-verifier-spotcheck.md` (routed defects 1 and 2), `corpus/QUALITY.md`
> (criterion 126), `.ufo/waves/round-74/w1/R74Critic/forge-order-oracle.py` and its `.log`. Identified
> 3, screened 3, included 2 (S184, S186), excluded 1 (S185, admission-criteria corpus, rejected as a
> self-referential source). Stop: the r74 closure record and the r74 attack probe are the only
> committed sources that carry these two grounds; no external fetch was made or needed.

## 5. Explicitly out of scope for this seat

- Not committed: no row was written into `corpus/SOURCES.md`; no lesson file was created or edited.
- No instrument was edited or run as a claim: `matrix-battery.py`, `loader-matrix-v2.py`,
  `c2-count.py`, `ref-counter.py` and `corpus/evidence/round75/forgers/*.py` were read as bytes only;
  the battery/counter verdicts quoted here come from the committed receipts, not from a fresh run.
- No admission decision is claimed: the admit/reject set above is a draft for the L1 planner seat and
  for the non-author spot-check the round requests.
