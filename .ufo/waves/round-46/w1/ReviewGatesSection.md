# ReviewGatesSection — round 46 wave 1

item: the exact `## Gates` column header; how many rows the frozen C2 rule counts; every
`|` line it does not count; whether a `### ` subsection sits inside; the exact insertion
point for this round's rows; whether a fenced-code-block row is counted (/tmp test).

Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`, HEAD `c2f0e9d`. No production file
touched; `/tmp` copies deleted. No installs.

## 0. Basis — two counter implementations (changed mid-wave)

| `corpus/evidence/round46/c2-count.py` | sha256 | note |
|---|---|---|
| at HEAD (`git show HEAD:…`) | `06c9e9bc3865…be5edb` | the frozen rule |
| worktree | `60ad448e99b1…39ca7ff` | ` M`, mtime `2026-10-25 07:28:28`, `+23/−4`, docstring credits round-46 `MutC2Forge` |

The diff adds fence toggling, a per-line `re.sub(r"<!--.*?-->","",line)` before the row
test, and `names()` (delimiter-boundary regex) replacing `p in r`. `c1-count.py` and
`c3-count.py` are also ` M`. Headline numbers coincide; forgeability does not.
`claims.md` **Admission rule**: "A rule changed after any seat has scored is not this
claim's rule" — C2 must be scored on `06c9e9bc`; the hardened file needs a re-freeze or
an erratum before closure.

## 1. Commands (verbatim)

`python3 corpus/evidence/round46/c2-count.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --list | tail -3`
at the frozen tree:
```
REGISTERED=55/72
UNREGISTERED=17
C2=FAIL
```
full run, rc=1, identical from the extracted HEAD file:
```
ENTRY_POINTS=72 (tools=8 counters=50 named=70)
GATES_ROWS=30
REGISTERED=55/72  UNREGISTERED=17  C2=FAIL
```
After sibling `ScribeGatesR46` landed 5 rows (`SKILL.md` ` M`, `+5/−0`) the current tree:
```
ENTRY_POINTS=72 (tools=8 counters=50 named=70)
GATES_ROWS=35
REGISTERED=72/72  UNREGISTERED=0  C2=PASS
```
rc=0. Frozen "Before" was `ENTRY_POINTS=71 (tools=7 counters=50 named=66)`; the worktree
adds untracked `tools/inference-ground.py` (7→8) and round-46 named paths (66→70), so
`≥71` holds.

Structural scan:
```
freeze:  | lines 35  counted 30  not counted 5   next "## " L503
now:     | lines 40  counted 35  not counted 5   next "## " L508
### inside: []   fences before/inside Gates: none (2 in file, both after L508)
```

## 2. Answers

**Column header** (`SKILL.md:77`, 8 columns / 9 pipes):
```
| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
```
Delimiter (`:78`): `|---|---|---|---|---|---|---|---|`

**Rows counted by the frozen rule: 30** (`GATES_ROWS=30`) — 35 `|` lines minus header,
delimiter and three real rows. Current `GATES_ROWS=35` (40 − 2 − 3).

**Every `|` line in the section the rule does NOT count** (the same five before and after):
| line | why |
|---|---|
| `:77` | header — no literal `exit` |
| `:78` | delimiter — no literal `exit` |
| `:80` | `research-gate verify-claims`: real row, verdict map says `could-not-evaluate`, no substring `exit` |
| `:81` | `research-gate verify-chain` — same omission |
| `:85` | `research-gate verify-metadata` — same omission |
No line has <8 pipes. `:79` (`research-gate`) counts only on "expected **exits**/finding
IDs": the test is a case-sensitive substring, so `exits` passes, `Exit`/`exited` would not.

**`### ` inside the section: none.** Next `## ` is `:503` (now `:508`); all `### ` are
543+. Probes: a row after an inserted `### ` counts (`H3_then_row` 31/56); a row after an
inserted `## ` does not (`H2_then_row` 30/55).

**Insertion point.** Append at the table tail, directly after the last row, no blank
separator. At freeze that was **line 112** (0-based 111): `:109` `chousa round-45
counters`, `:110` `parent-lifetime` (r44; exit contract r45), `:111` `tag-count`
(QUALITY 64, r45) ← last row; 112 blank, 113 `**Historical — Round-25 final registry
correction.**`. The scribe's five rows now occupy `:113-117` (`round24–27 counting
instruments`, `round33–34 census instruments`, `qr-harness`, `inference-ground`, `chousa
round-46 counters`), so the next append point is **line 118**, immediately before the
historical paragraph (which lost its blank line — cosmetic: a non-`|` line ends the GFM
table).

**Fenced row inside Gates — implementation-dependent (both measured):**
- frozen `06c9e9bc`: **counted** — fence-blind (`GATES_ROWS=31 REGISTERED=56/72` on the
  lane tree, identical to unfenced).
- hardened `60ad448e`: **refused** — a row between two fences is skipped
  (`0/1` on a one-entry fake root); a balanced fence that does not wrap a needed row is
  harmless (`1/1`).

## 3. Forgery classes, frozen vs hardened (peer `MutC2Forge` cross-check)

On the lane tree via `--skill` (entry point `corpus/evidence/round34/self-audit.py`), and
on a one-entry fake root (`tools/probe.py`) once the lane reached 72/72:
```
class                        frozen 06c9e9bc      hardened 60ad448e
FENCED_row                   GATES=31 REG=56/72   GATES=30 REG=55/72 (lane tree)
INLINE_HTML_comment appx.    GATES=31 REG=72/72*  GATES=31 REG=55/72 (lane tree)
PYC_DECOY_all17 (one row)    GATES=31 REG=72/72*  GATES=31 REG=55/72 (lane tree)
MULTI-LINE_comment wrapper   REG=1/1 PASS*        REG=1/1 PASS*  (fake root)
OWNLINE_comment line         refused              refused
SIX_CELL (7 pipes)           refused              refused
SEVEN_CELL (8 pipes)         counted, registers   counted, registers
H3_then_row                  counted, registers   counted, registers
DEAD_CMD_wrong_verdict       counted, registers   counted, registers
UNBALANCED_fence_in_Gates    counted              GATES_ROWS=0 REG=0/72
BALANCED_fence_wrapping_row  counted              GATES_ROWS=0 REG=0/72
```
`*` = `C2=PASS UNREGISTERED=0` exit 0 with no visible row: all 17 paths inside one
appended HTML comment, named as nonexistent `X.pyc`/`X.shc`, or a row sitting between an
`<!--` line and a `-->` line (the strip is **per line**, so a multi-line comment leaves
the row intact while rendering as nothing). First-hand frozen output on the lane tree:
```
INLINE_comment  GATES_ROWS=31 REGISTERED=72/72 UNREGISTERED=0
PYC_DECOY_all17 GATES_ROWS=31 REGISTERED=72/72 UNREGISTERED=0
```
Fence poisoning on the hardened file is fail-closed, never a false PASS: one unterminated
` ``` ` before or inside Gates gives `GATES_ROWS=0 REGISTERED=0/72` exit 1 — a whole-
registry false negative that prints as "0 rows" indistinguishable from an empty section.
Exit 2 when `GATES_ROWS==0` while entry points exist would separate unreadable-section
from claim-failure (peer proposal; I concur, not implemented).

## 4. Constraints for new rows (hardened counter; the landed five satisfy all)
1. Column 0 `|`; indented rows and prose paths are ignored (`INDENTED_ROW`,
   `PROSE_IN_GATES` both 30/55).
2. No ` ``` ` line anywhere inside Gates: a needed row between fences is skipped, and an
   unbalanced fence zeroes the whole section. A balanced illustration that touches no row
   is harmless, but buys nothing.
3. No `<!--` anywhere in Gates, on its own line or inside a row: a multi-line comment
   hides a counted row from the reader while the counter still credits it.
4. ≥8 pipes; 6 cells refused, 7 cells accepted; house rows use 9 pipes.
5. Literal lowercase `exit`; the `verify-claims`/`verify-chain`/`verify-metadata` dialect
   (no `exit`) does not count — the live trap. All five landed rows carry `exit`.
6. Boundary-exact path: `X.pyc`, `X.py.bak`, URL-embedded copies refused.
7. `### ` inside Gates is harmless; a column-0 `## ` inside Gates ends the section and
   unregisters every later row.

## 5. Coverage
Frozen tree: 17 unregistered (`round24-measure.sh`, `round25-*`, `round26-*`,
`round27-*`, `round33/d2-census.py`, `round33/no-name-signals.sh`,
`round34/self-audit.py`, `round46/{c1,c2,c3}-count.py`, `tools/inference-ground.py`);
after the scribe's rows `UNREGISTERED=0`. Fragility: 48 of 72 entry points are single-row
sourced (`tools/quote-reopen.py` only `:87`, `tools/parent-lifetime.sh` only `:110`);
`tools/research-gate.sh` has 7 rows (`:79,82,83,84,86,104,105`).

## 6. Verdict and residual risk
Structure is sound: no `### ` inside, no fence in the section, one append point (line 112
at freeze → 118 now). C2 passes honestly under the hardened counter (`72/72`, rc 0). Three
calibration defects stand: (i) the `exit` substring test drops three real rows, so
`GATES_ROWS` under-reports the table (38 data rows → 35) and a correct row written in the
L80/L81/L85 dialect is invisible to the counter; (ii) under the frozen rule, fence /
appended-comment / suffix classes forge `C2=PASS` with no registration, closed only by the
mid-wave edit the Admission rule does not recognise; (iii) the hardened comment strip is
per-line, so a multi-line comment still credits an invisible row. Row truth stays
unmeasured by design (a dead command with a wrong verdict map registers on both
implementations). Line numbers are a snapshot; SKILL.md moved during this audit.

Verification gaps: none for the questions asked; every claim above was executed.
