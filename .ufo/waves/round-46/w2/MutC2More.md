# MutC2More — R46-C2 registry: forges (a)–(d) against the hardened counter (round 46, wave 2)

item: four new forges on /tmp `SKILL.md` copies — (a) 8-cell row inside a `<!-- -->` that also
contains a `|`, (b) a path with a trailing `;` and a path inside `[x](path)`, (c) a 4-space
indented row, (d) a row inside a fence opened before `## Gates` and never closed.
Target: lane commit `d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a`.
Bytes scored: `corpus/evidence/round46/c2-count.py` sha256 `60ad448e99b15cb6691e48ce4e01c86ba8f027618f3e2fbb3649485ea39ca7ff`
(identical at HEAD `3807537`); archived `SKILL.md` sha256 `2ff29159fa610d7b59e6100ed301790432fabff7b80446178c4523d3c3dd5da4`.
Baseline on that archive: `ENTRY_POINTS=72 (tools=8 counters=50 named=70) GATES_ROWS=35
REGISTERED=72/72 UNREGISTERED=0 C2=PASS` rc 0 — reproduced on two runs.

## Method (why the landed SKILL.md cannot score a forge)

Everything is already registered by the 35 landed rows, so a forge appended to the real file is
unmeasured. Each variant therefore keeps `## Gates`, its table header, 396 non-row body lines, and
the 35 data rows **removed**; one forged block is the only candidate row. Harness calibration on the
same emptied file: no row → `GATES_ROWS=0 REGISTERED=0/72 UNREGISTERED=72 C2=FAIL` rc 1; one
column-0 8-cell row naming all 72 → `GATES_ROWS=1 REGISTERED=72/72 UNREGISTERED=0 C2=PASS` rc 0.
Runs: `python3 corpus/evidence/round46/c2-count.py --skill <variant>`, cwd = the pinned archive.
Path cell = backticked repo-relative paths, ` · `-separated; entry cell = `python3 tools/none.py`
(nonexistent, never executed — the counter does not run entries).

## Results (pinned tree, 72 entry points)

| id | forge | GATES_ROWS | REGISTERED | UNREG | rc | refused? |
|---|---|---|---|---|---|---|
| a1 | whole row inside a same-line `<!-- … -->` | 0 | 0/72 | 72 | 1 | **REFUSED** (correct) |
| a2 | `<!--` / row / `-->` on three lines | 1 | 72/72 | 0 | 0 | not refused — **known** (w1 `m-c3`) |
| a3 | `<!-- note \| x -->` then the row, **no space** after `-->` | 1 | 72/72 | 0 | 0 | **NOT REFUSED — new** |
| a4 | a3 plus one space after `-->` | 0 | 0/72 | 72 | 1 | refused (by the space, not by rendering) |
| a5 | comment carries the 8 pipes + `exit`, body only 4 pipes | 0 | 0/72 | 72 | 1 | **REFUSED** (no pipe laundering) |
| b1 | every path as `` `path`; `` | 1 | 72/72 | 0 | 0 | not refused (correct) |
| b2 | every path as `[x](path)` | 1 | 72/72 | 0 | 0 | not refused (correct) |
| b4 | `` [`path`](https://example.invalid/x.py) `` | 1 | 72/72 | 0 | 0 | not refused (correct) |
| b5 | only remote targets `https://example.invalid/<path>` | 1 | 0/72 | 72 | 1 | **REFUSED** (correct) |
| b6 | nonexistent paths with a trailing `;` | 1 | 0/72 | 72 | 1 | **REFUSED** (no false credit) |
| b3 | every path as `` `./path` `` | 1 | 0/72 | 72 | 1 | **REFUSED — new false negative** |
| c1 | row indented 4 spaces | 0 | 0/72 | 72 | 1 | **REFUSED** (correct: code block) |
| c2 | row indented 2 spaces | 0 | 0/72 | 72 | 1 | refused; 1–3-space band undeclared |
| d1 | ``` opener **before** `## Gates`, never closed | 0 | 0/72 | 72 | 1 | **REFUSED**, fail-closed (known) |
| d2 | ``` opener+closer before the heading (balanced) | 1 | 72/72 | 0 | 0 | not refused (correct) |

Frozen C2 controls re-run on the same harness, all `C2=FAIL` rc 1 as committed: paths as prose,
6-cell row, 8-pipe row without `exit`, valid row after the next `## ` heading.

## The four assigned questions, answered

**(a) Row inside a comment that also has a `|` in it — refused or not?** Both, and the discriminator
is not the comment. Row fully inside a same-line comment → refused (a1). Comment body containing a
pipe is irrelevant: its pipes are stripped before counting (`c2-count.py:91` runs before `:92`), and
a comment cannot donate separators to a short row (a5 refused). But a comment **prefix abutting** the
row (`<!-- note | x -->| … |`) is credited at `72/72 C2=PASS` (a3, sha256 prefix `a7e879d6`), while
the same line with one added space is refused (a4, `8dc0a03d`). Both variants render identically as
one `html_block` (`cmark --to xml --unsafe` → `<html_block`), i.e. neither is a Markdown table row
in any CommonMark/GFM renderer.

**(b) Trailing `;` and `[x](path)` — refused?** No, and correctly so: `;` and `(`/`)` are outside the
boundary class in `names()` (`c2-count.py:99`), and neither form buys false credit — nonexistent
paths with `;` stay 0/72 (b6) and remote-URL targets stay 0/72 (b5). Same-forge reverse direction is
the real defect: an explicit `./` prefix is **refused** (b3, 0/72) because the left boundary includes
`/` and `.`; `names()` returns False for `` `./tools/inference-ground.py` ``,
`` `/home/u/lane/tools/inference-ground.py` ``, `` `sub/tools/inference-ground.py` `` and
`[x](https://example.invalid/tools/inference-ground.py)`, True for `` `path` ``, `` `path`; ``,
`[x](path)` and `` [`path`](…) ``.

**(c) 4-space row — refused?** Yes: `GATES_ROWS=0`, 0/72, rc 1. Correct — 4 spaces is an indented
code block (`cmark --to xml`: `<code_block`). The adjacent 2-space case is also refused (0/72),
although GFM parses a `|` line indented up to three spaces as a table row **[INFERENCE: GFM spec;
the local `cmark` has no table extension, so only the code-block side is observed]** — a false
negative band that costs a correct scribe, and cannot manufacture a pass.

**(d) Row inside a fence opened before `## Gates`, never closed — refused?** Yes, fail-closed:
`GATES_ROWS=0 REGISTERED=0/72 UNREGISTERED=72 C2=FAIL` rc 1. The opener toggles fence state on the
`## Gates` line itself (`:86-88` precede `:89`), so the heading is never seen and `inside` stays
False; no row is credited. No false PASS is reachable this way. It is reported as rc 1 `C2=FAIL`,
indistinguishable from a genuine unregistered tree (w1's exit-2 recommendation, confirmed here, not
new). A balanced fence before the heading is harmless (d2, 72/72).

## New findings (not in the 32 wave-1 reports)

**N1 — comment strip manufactures the row it tests (`c2-count.py:91-92`).** `re.sub(r"<!--.*?-->")`
runs before `startswith("|")`, so a line that begins `<` in the source is credited as a row when the
closing `-->` abuts the pipe. Cheapest measured form: 9 characters, `<!--x-->` + one 8-cell line,
`GATES_ROWS=1 REGISTERED=72/72 UNREGISTERED=0 C2=PASS` rc 0 on the pinned tree (sha256 prefix
`0f49dc5a`), and the same line at HEAD with 73/73. This is a deviation from the counter's own rule
("a line … that starts with `|`") — unlike w1's `m-c3`, which starts with `|` and merely defeats the
intent. Fix shape: strip comments statefully across the section and test the *source* line's
indentation, or refuse a line whose first non-space characters open a comment.

**N2 — `./`-prefixed paths are invisible (`c2-count.py:99`).** A row naming
`` `./corpus/evidence/round34/self-audit.py` `` registers 0/72. The claim's predicate says "named by
repo-relative path", and `./x` is the same repo-relative path; C2's kill rule (`UNREGISTERED>0`) would
then fail a compliant document. Direction is safe (no false PASS) but the gate is not faithful to its
own predicate. Fix shape: allow an optional `./` in the lookbehind, keep the `[A-Za-z0-9_./-]` guard
for true suffixes.

**N3 — indentation band (1–3 spaces) is refused and undeclared.** See (c). Same class as N2: a
false negative that renders as `C2=FAIL`; no false PASS.

Positive results worth keeping in the counter: comment pipes cannot launder separators (a5), remote
URL targets do not register (b5), `;`/link forms neither break nor cheat (b1/b2/b4/b6), an unclosed
fence before the heading is fail-closed (d1), 4-space indentation is refused (c1).

## Current bytes (recorded, not the scored target)

HEAD moved to `3807537` during this seat (wave-2 corrections; `SKILL.md` +1/−1 line,
sha256 `efc99c13…f576a928`). The counter bytes are unchanged (`60ad448e`). Re-running the same
forged blocks against HEAD `SKILL.md` with `ENTRY_POINTS=73 (tools=8 counters=50 named=71)`:
no row 0/73 FAIL; a1 0/73 FAIL; a2 73/73 PASS; a3 73/73 PASS; a4 0/73 FAIL; b1 73/73; b2 73/73;
b3 0/73 FAIL; c1 0/73; d1 0/73. Live tree itself: `GATES_ROWS=35 REGISTERED=73/73 UNREGISTERED=0
C2=PASS` rc 0 — C2 still holds; N1–N3 are latent, not exploited by the landed rows.

## Limits of this seat

Verdicts are the counter's own output; whether a credited line is a *true* dependency (command
actually run, verdict map correct) is out of scope and already named. One `--list` run appears as
`C2=PASS` rc 0 on both trees; the only rc I assert is the one captured by `subprocess.returncode`
(stated per cell). The a3 rendering claim is observed for a shortened line of the same shape; the
72-path line shares the identical prefix.

## Restoration evidence

- No lane production file, index, jj state or fleet repo touched. Scratch `/tmp/chousa-r46w2-MutC2More/`
  (archive tree + 19 variant `SKILL.md` files) deleted; `ls` → "No such file or directory".
- Byproduct removed: my `importlib` load of the live counter created
  `corpus/evidence/round46/__pycache__/c2-count.cpython-314.pyc` (mtime 07:29:18); deleted, and the
  now-empty `__pycache__` removed (gitignored, never in the C2 entry set).
- Lane hashes at finish: `SKILL.md` `efc99c13…f576a928`, `c2-count.py` `60ad448e…39ca7ff` (unchanged
  from measurement); pinned archive hashes as in the header. No install, no network, no git mutation.
