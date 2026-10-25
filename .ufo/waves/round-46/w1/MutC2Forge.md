# MutC2Forge — R46-C2 counter: five forges, then the revision (wave 1, round 46)

item: attack `corpus/evidence/round46/c2-count.py` with the five assigned forges on /tmp copies
(`--root`/`--skill`). Mutation tester seat; no lane production writes.

**Two instrument states, both measured.**
- frozen blob `06c9e9bc3865b60e127f435f749ec0587e8b7ede3f453678a9de247f9cbe5edb` == `git show
  c2f0e9d:…/c2-count.py` — the bytes the claim is frozen against, and the bytes my five forges hit;
- live revision `60ad448e99b15cb6691e48ce4e01c86ba8f027618f3e2fbb3649485ea39ca7ff`, landed mid-wave by
  a sibling (docstring now credits this seat; adds fence-skip, per-line `<!--…-->` strip and
  `names()` delimiter-bounded credit). Not written or approved by me; ExecCounterRun's ledger counts
  six post-freeze edits across the round's instruments (c1 ×3, c2, c3, tool) — an L1 re-freeze/erratum
  item, since the Admission rule says a rule changed after a seat scored is not this claim's rule.

**Tree caveat:** HEAD == `c2f0e9d`; counts are against `SKILL.md` `7b49e2ae…d05433` (measurement time;
siblings landed rows after, live `2ff29159…5da4`). Tree = freeze **plus untracked wave-1 artifacts**
(`tools/inference-ground.py` absent in `c2f0e9d`), so my baseline is `72/55/17`.

## Provenance of the committed before-line (verified, not inferred)

| tree | entry points | registered | unregistered |
|---|---|---|---|
| bare `git archive 6e2630a6` + frozen counter | `68 (tools=7 counters=47 named=66)` | 55/68 | **13** |
| `git archive c2f0e9d` + frozen counter | `71 (7/50/69 as committed; the receipt prints named=66, reproduced exactly by removing the three `c<N>-count.py` mentions from claims.md — same 71/55/16)` | 55/71 | **16** ← matches `controls/c2-before.txt` |
| live tree (freeze + untracked `tools/inference-ground.py`) | `72 (tools=8 counters=50 named=70)` | 55/72 | 17 |

The receipt is honest: `controls/c1-before.txt:2` declares "`git archive 6e2630a6` … + **this round's
counters and fixtures**; tools/inference-ground.py absent", and `c2-before.txt:2` says "tree: as
above". The imprecision is in `claims.md:40` ("base tree") — that parenthetical names the augmented
tree, whose tally is 71/16, not the bare commit's 68/13. Pre-existing debt at the bare commit is 13;
three of the sixteen are counters the freeze commit itself added.

## Frozen rule under test (verbatim, `git show c2f0e9d:…/c2-count.py`)

    A Gates row is a line of the `## Gates` section (up to the next `## ` heading)
    that starts with `|`, carries at least 8 `|` separators and contains the word
    `exit`.

claims.md C2: entry points "must be named by repo-relative path inside a `## Gates` row"; frozen
credit is `unreg = [p for p in eps if not any(p in r for r in rows)]` (raw substring).

Baseline (snapshot rsync of the lane): `ENTRY_POINTS=72 (tools=8 counters=50 named=70) /
GATES_ROWS=30 / REGISTERED=55/72 / UNREGISTERED=17 / C2=FAIL` exit 1. Forge injection: end of
`## Gates` (lines 75..502), or appended to the last table line (111) to be a real rendered row.

## Forges against the frozen blob — verdicts

| # | forge | GATES_ROWS | REGISTERED | UNREG | exit | frozen rule |
|---|---|---|---|---|---|---|
| a | real 8-col row, all 17 paths, **dead** command, wrong verdict map | 31 | 72/72 | 0 | 0 | matches; claim's named limit ("row truth is not measured") covers it, though a dead command is beyond "verdict map is wrong" |
| b | one 8-pipe line **inside a ``` fence** in Gates | 31 | 72/72 | 0 | 0 | matches the **line** test literally; contradicts "inside a `## Gates` **row**" and the docstring's own anti-cheat → latent cheap gate |
| c | all 17 in an own-line `<!-- … -->` comment | 30 | 55/72 | 17 | 1 | matches (refused) — but only because that comment line starts with `<!--`, not `|`; the multi-line shape credits on this blob too (m-c3 below, and ReviewGatesSection's one-entry root) |
| c2 | same comment **appended to a live row** | 30 | 72/72 | 0 | 0 | literal match, zero visible rows → latent cheap gate |
| d | row under a `### ` subsection inside Gates | 31 | 72/72 | 0 | 0 | matches **by design** (section runs to next `## `) |
| e | row names `…/self-audit.pyc` (no such file); EP is `…/self-audit.py` | 31 | 56/72 | 16 | 1 | **DEVIATION — kill** (55→56: prefix credited) |
| e2 | one row, all 17 as nonexistent `…shc`/`…pyc` | 31 | 72/72 | 0 | **0** | **DEVIATION — C2=PASS, no real path named** |

Decisive forged inputs (verbatim; each file is one inserted block):

    | `forged-e2` | gate | `python3 tools/none.pyc` | `0` ok · `1` drift | none exit 0 | `corpus/evidence/round24-measure.shc` · … · `tools/inference-ground.pyc` | none | nobody |
    | `forged-e`  | gate | `python3 corpus/evidence/round34/self-audit.pyc` | `0` clean · `1` drift · `2` could-not-evaluate | none exit 0 | none | none | nobody |
    ```                                     ← forge b: fence opened after a blank line
    | forged-b | gate | python3 tools/does-not-exist.py | 0 always | exit 0 | <17 paths> | none | nobody |
    ```
    <!-- <17 paths> -->                    ← forge c (own line, refused); c2 = same text appended to row 79

`exists()` checks: `…round24-measure.shc`=False, `…self-audit.pyc`=False, `tools/inference-ground.pyc`=False.
GATES_ROWS 30→31 for (b) proves the fenced line was taken as a row while rendering as code.

## Verdicts on the frozen blob

- **(b), (d) match the frozen rule**; (d) is declared design and agrees with the frozen control
  "a valid row after the next `## ` heading stays unregistered". **(c) matches** (refused).
- **(a) survives in-contract** — row truth is the claim's declared unmeasured limit.
- **(e)/(e2) KILLED**: unbounded substring credit. `…/self-audit.pyc` names a different, nonexistent
  path, yet credits `…/self-audit.py`; one 9-cell row reaches `UNREGISTERED=0 C2=PASS` naming nothing
  real — the cheapest gate for C2, undisclosed by the docstring (QUALITY 60).
- **(b)/(c2)** match the frozen sentence but defeat its intent and the docstring's anti-cheat
  ("pasting the bare paths anywhere in SKILL.md … refused"): an 8-pipe fenced line and a
  row-appended comment are both "anywhere with eight pipes and exit".
- Pristine tree is honest: no fence and no `###` inside real Gates (lines 75–502), and a strict
  re-implementation (fence-aware, comment-stripped, delimiter-bounded, table-context) reproduces
  `55/72 UNREGISTERED=17`. The holes were latent, not exploited.

## Re-run against the live revision `60ad448e` (same snapshot, same mutants)

| mutant | output | read |
|---|---|---|
| baseline | `GATES_ROWS=30 REGISTERED=55/72 UNREGISTERED=17 C2=FAIL` exit 1 | unchanged |
| m-a real row, dead command | `GATES_ROWS=31 REGISTERED=72/72 UNREGISTERED=0 C2=PASS` exit 0 | (a) unchanged — declared limit |
| m-b fenced line | `GATES_ROWS=30 REGISTERED=55/72 UNREGISTERED=17` exit 1 | **killed** |
| m-c2 comment appended to row | `GATES_ROWS=30 REGISTERED=55/72 UNREGISTERED=17` exit 1 | **killed** |
| m-e2 all-17 `.pyc`/`.shc` row | `GATES_ROWS=31 REGISTERED=55/72 UNREGISTERED=17` exit 1 | **killed** |
| m-c3 **multi-line** `<!--` … row … `-->` | `GATES_ROWS=31 REGISTERED=72/72 UNREGISTERED=0 C2=PASS` exit 0 | **NEW KILL — residual cheap gate** |

Residual defect in the revision: `re.sub(r"<!--.*?-->", "", line)` is per line, so a comment opened on
one line and closed on a later one leaves the row between them intact. Forged block (renders as
nothing, registers all 17):

    <!--
    | `m-c3` | gate | `python3 tools/none.pyc` | `0` ok · `1` drift | none exit 0 | <17 paths> | none | nobody |
    -->

Fix: strip HTML comments **statefully** across the section (`in_comment` toggled at `<!--` / `-->`)
before the row test, as the fence toggle already does; keep `names()`. Suggested mutant for the
revision's own control set: `m-c3` above.

## Leg (C) exclusion (raised by ReviewerC2Set, verified)

`NAMED` hard-requires a `tools/` or `corpus/` prefix, so ten existing named paths are dropped: 8 relative
`.ufo/waves/round-{35,36,37,38,39,41}/controls/*.sh|py` plus 2 absolute `SCORECARD.md` mentions
(`.ufo/waves/round-29/falsify/DiffToolB/guarded-run.py`, `scripts/sources-census.sh`). Not gates — control
artifacts — but the exclusion is undeclared.

## Frozen controls, re-run on the live tree (all four hold)

`ctrl-prose` / `ctrl-6cell` / `ctrl-noexit` / `ctrl-after`: each `GATES_ROWS=30 REGISTERED=55/72
UNREGISTERED=17 C2=FAIL exit=1`. Boundary: an exactly-8-pipe row with `exit` registers (17→16,
GATES_ROWS 31); a 7-pipe row does not — matches "at least 8 separators".

## Fence-state poisoning (revision only; fail-closed, not a bypass)

Fence state is global and toggled by any lstrip'ed ``` line, so one stray fence zeroes the registry:

| mutant | output | read |
|---|---|---|
| ``` inserted right after `## Gates`, never closed | `GATES_ROWS=0 REGISTERED=0/72 UNREGISTERED=72` exit 1 | every row **after** the opener is dropped; here the opener precedes all of them |
| ``` inserted ~3 lines **before** `## Gates`, never closed | `GATES_ROWS=0 REGISTERED=0/72 UNREGISTERED=72` exit 1 | same, from outside the section — rows already collected before the opener still count |
| ``` … illustration … ``` balanced inside Gates | `GATES_ROWS=35 REGISTERED=72/72 UNREGISTERED=0 C2=PASS` exit 0 | harmless **only because it wraps no needed row**; wrapping one drops it (`REGISTERED=0/1` on a one-entry root) |

Not a cheap gate (it never yields a false PASS), but a scribe's illustration block inside Gates makes
the counter report `0/72` — a whole-registry false negative that reads like "no rows". Prefer exit 2
when entry points exist and `GATES_ROWS==0`.
Third row-shape route (ExecCounterRun, verified on `60ad448e` with a one-entry root): the ≥8 test counts
**raw** pipes, so `| a | b | c | x\|y\|z\|w\|q | \`tools/foo.py\` exit 0 |` (10 pipes, 5 cells) registers
while the same row unescaped (5 pipes) is refused — count cells, not `|` characters.

## Live drift at finish (recorded, not scored by me)

While the above ran, siblings' rows + the revision landed: live tree `GATES_ROWS=35 REGISTERED=72/72
UNREGISTERED=0 C2=PASS` exit 0. My `55/72/17` baseline is the measurement-time state, not this tree.

## Restoration / side effects

- No writes to the lane: HEAD was `c2f0e9d100c0d46633a6277b2fd51d2ac99678eb` at measurement and
  `d09fc8e` at finish (siblings' landings); `SKILL.md` `7b49e2ae…d05433` → live `efc99c13…`; the counter's live `60ad448e…` is a sibling's edit, not mine (the
  frozen `06c9e9bc…` is what my forges were scored against). No mutating git/jj, no fetch, no installs.
- All forged variants lived under `/tmp/chousa-r46-MutC2Forge{,2,3}/` and are deleted; hashes as run:
  a2 `1108e586…990c`, b `8d000736…0802`, c `330cb5a6…9cc3`, c2 `438749dd…1da2`, d `ba03c865…f4ce`,
  e `d88df518…e9a4`, e2 `0559b3cd…e86b`.
