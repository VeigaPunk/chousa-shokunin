# Round 78 corpus text — Scribe draft (drafted, not landed)

Seat `R78ScribeA`, lane `chousa-shokunin`. Base `53dbd512d0ab70055338cb44898a6db70049537f`
(round-77 tip); prefreeze instruments and controls
`93e0432eb5bb9c4492d540bc6a6358ed3f8d4392`; claims freeze
`01b444b7f8d90785515e77c7ba9db5d63361329b`. This file drafts three `corpus/SOURCES.md` rows,
the `## Gate` block for `corpus/lessons/round-78.md` and two `## Mistakes` rows. It lands
nothing: `corpus/`, `tools/` and the lane tree are read-only for this seat, and the two
instrument defects are evidenced by the probes in this folder, whose receipts are
`.ufo/waves/round-78/w1/R78ScribeA/salt-future.out` and
`.ufo/waves/round-78/w1/R78ScribeA/trailer-verdict.out` (untracked until the wave commits).

## (a) `corpus/SOURCES.md` — three registry rows

Contract shape from `/home/vgpnk/Projects/shokunin/CORPUS.md` § *SOURCES.md* (11 cells,
`NF=13` on `|`).

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S193 | chousa round-77 verifier spot-check, routed defect 1 — corpus/lessons/round-77-verifier-spotcheck.md | own-work | B | the r77 gate registry row's cell count: the registered battery row carries 7 cells against its header's 8, and no owner cell | 53dbd512d0ab70055338cb44898a6db70049537f, lines 156-160 (quote line 156) | A gate-registry row that loses a cell is a row whose owner and self-test go unrecorded; the repair appends a correction row or cell, because the registry is append-only evidence | mined | 2026-11-04 | on-release | corpus/lessons/round-78.md |
| S194 | chousa corpus quality criterion 143 — corpus/QUALITY.md | own-work | B | the successor outer battery's leak channels: a printed permutation digest, a strippable subject salt, a judge-source contract read, and a predicate read apart from its exit code | 53dbd512d0ab70055338cb44898a6db70049537f, line 1046 (quote inside the Check sentence) | An outer battery prints the seed digest rather than the permutation, rewrites rather than suffixes the salted copy, derives its contract cells per run, and reads its predicate together with the recorded exit code | mined | 2026-11-04 | on-release | corpus/lessons/round-78.md |
| S195 | chousa round-78 controls receipt — corpus/evidence/round78/controls/forge-battery-after-v5.txt | own-work | C | this round's own predicate receipt as source evidence | 93e0432eb5bb9c4492d540bc6a6358ed3f8d4392, lines 1-12 (quote line 9) | REJECTED: a receipt is the lane's own measurement of its own instrument, not evidence that the predicate holds — the r76 S189 and r77 S192 precedent; flip: admit scoped to the receipt text if an admitted entry ever rests on a measurement receipt as the only record of a prediction | rejected | 2026-11-04 | on-release | — |

Anchors, pinned:

- **S193** — `git show 53dbd512:corpus/lessons/round-77-verifier-spotcheck.md`, lines 156-160.
  Line 156 is the bolded defect sentence, 157-160 the cell count and the repair; line 154 is
  the `## Routed defects (owner chousa, next round)` heading, so a span that starts at 154
  includes the heading. The file is byte-identical at `53dbd512` and at the freeze commit
  (`sha256 a4d979ba380b18f763e9ec9df2bb14003c62e1ec3da6ec612572d4a96e8a0c22` on both).
- **S194** — `corpus/QUALITY.md` line 1046, the criterion's single paragraph. Verified
  byte-identical at `53dbd512` and at the freeze commit
  (`sha256 861ec27b4ae14b34790ace89dfadec431b4b47479c325c5ed45873725656d13a` for that line on
  both), because criteria 144-146 were appended *after* it. Lines 1040-1045 are criteria 141
  and 142, so a span that starts at 1040 covers three criteria.
- **S195** — `git show 93e0432e:corpus/evidence/round78/controls/forge-battery-after-v5.txt`,
  12 lines; the predicate is line 9, `# exit: 0` line 10, the lane-rev line 11. Quoting line 8
  quotes the positive control's line, not the predicate.

Census, run on a scratch copy of the base registry with these three rows appended (a stub
`corpus/lessons/round-78.md` present for the used-by leg), from that scratch root:

```sh
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md          # 195 (192 + 3)
awk -F'|' '... NF!=13 ...' corpus/SOURCES.md                                   # 0
awk -F'|' '... tier/status/kind enum ...' corpus/SOURCES.md                    # no output
awk -F'|' '... print id ...' | sort | uniq -d                                  # no output
awk -F'|' '... mined used-by ...' | while read -r p; do [ -e "$p" ] || ...; done  # no output
```

Tier histogram `A=123 B=54 C=18`; status `mined=156 queued=19 rejected=20`. Exit 0 for the
run. Limit: `corpus/lessons/round-78.md` does not exist at the frozen base, so the used-by leg
resolves only once the lesson lands; re-run the census at landing.

## (b) `## Gate` block for `corpus/lessons/round-78.md`

```markdown
## Gate

- Admit S193, own-work B, scoped to the r77 spot-check's routed defect 1 — the gate-registry
  row with no owner cell. `corpus/lessons/round-77-verifier-spotcheck.md` at
  `53dbd512d0ab70055338cb44898a6db70049537f`, lines 156–160, quote on line 156. Opened
  2026-11-04. Located quote: "`SKILL.md` registry row `round77 order-and-content battery` is
  missing its owner cell." (11 words, `wc -w`). Grounds C2's first class: it is the closure
  record that names the defect, not independent truth that the successor repairs it — the
  committed counter is.
- Admit S194, own-work B, scoped to QUALITY 143's check sentence for a successor outer
  battery. `corpus/QUALITY.md` at `53dbd512d0ab70055338cb44898a6db70049537f`, line 1046,
  quote inside the Check sentence on that line. Opened 2026-11-04. Located quote: "the
  printed digest is of the seed, not of the permutation" (11 words, `wc -w`). Grounds C1's
  target: the sentence is a requirement on the successor, not a measurement of it.
- Reject S195, own-work C, scoped to this round's own predicate receipt as a source row.
  `corpus/evidence/round78/controls/forge-battery-after-v5.txt` at
  `93e0432eb5bb9c4492d540bc6a6358ed3f8d4392`, lines 1–12, quote on line 9. Opened
  2026-11-04. Located quote: "FORGE_BATTERY=PASS forgers_handled=4/4 positive=1/1" (3
  words, `wc -w`). REJECTED: a receipt is the lane's own measurement of its own instrument,
  not evidence that the predicate holds — the r76 S189 and r77 S192 precedent; a row here
  would let a later round cite its own measurement as a source. Flip: admit scoped to the
  receipt text if an admitted knowledge entry ever rests on a measurement receipt as the
  only record of a prediction.
- New registry rows S193/S194 mined, used-by this lesson; S195 rejected, used-by `—`.
  Existing status/recheck/used-by cells unchanged. No URL opened or fetched: all three are
  revision-pinned committed paths.
- Non-author spot-check requested: two admits and one reject above. Dispatched wave seats are
  author-lane evidence, not independent admission or promotion reviewers.
- Assimilation: none — no package bytes adopted this round, so no id-collision check is run
  on adopted ids. `considerthese/` was opened; no proposal adopted (claim cap), recorded
  rather than implemented. No operator-authored consideration was edited.
```

## (c) `## Mistakes` rows for `corpus/lessons/round-78.md`

Classes from `mistakes.md` §5 (`vacuous`, `survivor`, `stale-premise`, `reference-drift`,
`number-drift`, `scope`, `attribution`, `landing`, `provider`).

| class | evidence | captured-by | fix |
|---|---|---|---|
| scope | The salt transform claimed an invariant its anchor rule did not hold: its own comment reads "an inert statement at a module statement boundary cannot change the subject's behaviour or its syntax", but a statement inserted above `from __future__ import annotations` is a compile error. Measured on the committed positives: `.ufo/waves/round-78/w1/R78ScribeA/salt-future.out` — `naive_broken=2` (`corpus/evidence/round74/correction-count.py:46 from __future__ imports must occur at the beginning of the file (line 47)` and the same at `corpus/evidence/round76/loader-matrix-v3.py:37`), `guarded_broken=0`, `frozen_broken=0` over 60 copies of the frozen transform; `# exit: 0`. | QUALITY 145's positive-control clause — the legitimate matrix must stay ACCEPTED, `positive=1/1`; the content leg and the subject loop both score a syntactically invalid copy as "forger rejected", so only the positive leg can see it. | `salted_copy()` restricts its anchors to `n.lineno > max(__future__ import lines)` and excludes bare-string `Expr` docstrings (`matrix-battery-v5.py` lines 203-212). Shown able to fail: the probe's naive leg breaks both future-carrying positives and its guarded leg breaks none — `python3 -B .ufo/waves/round-78/w1/R78ScribeA/probe-salt-future.py --lane . --work DIR` prints `SALT_FUTURE=REPRODUCED naive_broken=2 guarded_broken=0 frozen_broken=0`, exit 0. |
| vacuous | The forge battery's verdict rule credited a battery that prints no `RECEIPT_LINES` trailer with DETECTED whenever the receipt carried more than one `BATTERY=` line, so the round-77 battery scored `handled` for the detached append with no detection mechanism of its own, and the before control would have printed `forgers_handled=1/4` — a control meeting the counter. Measured: `.ufo/waves/round-78/w1/R78ScribeA/trailer-verdict.out` — the frozen reader returns `real_integrity=n/a` for a trailer-less two-`BATTERY=` receipt, `defect_rule=DETECTED`, `current_rule=FORGED`, `defect_handled=1/4 current_handled=0/4`; `# exit: 0`. The committed before receipt keeps the fixed reading: `trailer=no integrity=n/a verdict=FORGED` (`controls/forge-battery-before-v4.txt` line 7). | QUALITY 24 — a control that meets the counter re-designs the claim; the round-77 battery is exactly that control, and QUALITY 145's DETECTED definition ("a receipt that fails *its own* integrity rule") is what the fixed rule now reads. | `read_receipt()` returns `None` when the battery prints no trailer, and only `integrity is False` maps to DETECTED (`forge-battery.py` lines 68-84, 131-142). Shown able to fail: `python3 -B .ufo/waves/round-78/w1/R78ScribeA/probe-trailer-verdict.py --lane . --work DIR` prints `TRAILER_VERDICT=REPRODUCED defect_handled=1/4 current_handled=0/4`, exit 0, and the frozen reader's `n/a` on the trailer-less receipt is what makes the defect rule fire. |

## Measured word counts

| row | quote | `wc -w` | command |
|---|---|---|---|
| S193 | `` `SKILL.md` registry row `round77 order-and-content battery` is missing its owner cell. `` | 11 | `git show 53dbd512:corpus/lessons/round-77-verifier-spotcheck.md \| sed -n '156p' \| ... \| wc -w` |
| S194 | the printed digest is of the seed, not of the permutation | 11 | `git show 53dbd512:corpus/QUALITY.md \| sed -n '1046p' \| ... \| wc -w` |
| S195 | FORGE_BATTERY=PASS forgers_handled=4/4 positive=1/1 | 3 | `git show 93e0432e:corpus/evidence/round78/controls/forge-battery-after-v5.txt \| sed -n '9p' \| wc -w` |

Receipts: `.ufo/waves/round-78/w1/R78ScribeA/quote-counts.out` (`wc -w` output, 11 / 11 / 3),
`s193-quote.txt`, `s194-quote.txt`, `s195-quote.txt` (the exact strings counted).

## Deltas against the working-tree rows (report-only; the lane tree is read-only here)

The lane working tree already carries S193-S195 and a `## Gate`/`## Mistakes` draft
(`corpus/SOURCES.md` modified, `corpus/lessons/round-78.md` untracked). Deltas this draft
would close:

1. **S193 anchor start line.** Working tree: `lines 154-158`. Line 154 is the
   `## Routed defects` heading and line 155 is blank; the defect item is 156-160. Draft: 156-160.
2. **S194 anchor span and quote.** Working tree: `lines 1040-1046`, quoting the criterion's
   bold lead sentence (20 words). Lines 1040-1045 are criteria 141 and 142. Draft: line 1046,
   quoting the Check sentence clause (11 words) as this seat was asked.
3. **S195 anchor span and quote line.** Working tree: `lines 1-9 (quote line 8)`, while the
   Gate's own located quote is the predicate, which is line 9. The receipt is 12 lines. Draft:
   lines 1-12, quote line 9.
4. **`## Mistakes` class cells.** Working tree rows carry descriptions in the class column
   ("an inert salt inserted before `from __future__` broke both positives", "a verdict rule
   credited a battery with detecting an append it has no mechanism to detect") instead of a
   §5 vocabulary token. Draft: `scope` and `vacuous`.
5. **`## Mistakes` evidence pointers.** Working tree rows cite the observation in prose
   ("the first v5 predicate run printed …") with no committed receipt. Draft: a probe plus a
   committed receipt under this wave folder, with the exact command and its exit code.
6. **`## Gate` S193 quote.** Working tree renders the quote without the inner backticks
   (`SKILL.md registry row …`); the line carries them. Word count is 11 either way. Draft
   keeps the line's own punctuation.
