# R75Review2 — C2 measurement-semantics attack

Seat: reviewer (attack), round 75 w1. Root `chousa-shokunin`, frozen rev
`43a7a0db52c8aabdf32735f58e09610e05200e79` (worktree clean for the instrument).
Target: `corpus/evidence/round75/c2-count.py` (sha256 `bf0250e7e1c3f3ebf80626d68f743b2b8ac1f3640e5a15a4d4d4048a186e48b8`,
identical to its blob at the frozen rev; not bound in `claims.md` C2 or in `controls/before-c2.txt`).

Verdict: the derivation **is** taken from the lesson at `--rev` (not from the spot-check's
copies), and a block that merely states the wrong numbers **is** rejected — but a block that
states the wrong thing, or a block that points the measurement at the wrong bytes, **passes
4/4 exit 0**. C2's Q3 as implemented does not test what C2's sentence claims.

## Confirmed, not defects

1. **Derivation source is the lesson at `--rev`.** The only content read is
   `git show <rev>:corpus/lessons/round-74.md` (`c2-count.py:76`); the spot-check is referenced
   in comments only (`:4,:7`). Case M put a spot-check copy stating `99`/`88` in the fixture and
   `DERIVED` stayed `S182:16 S183:11`.
2. **The derived numbers are right.** Independent recount over the lesson bytes at base
   `8022f72c…`: quote A = 16 whitespace-split tokens (15 whitespace runs), quote B = 11 (10 runs);
   the recorded 18 and 13 are reachable by no whitespace measure of either quote. Both lesson
   quotes are byte-identical to the spot-check's copies.
3. **Wrong numbers alone do not pass.** Case A (block says 17/12, names superseded 18/13):
   `Q2 FAIL` → 3/4 exit 1. Case B (block says 16/11, omits 18/13): `Q3 FAIL` → 3/4 exit 1.
   Case C (correct block plus one deleted authored line): `Q4 FAIL removed lines=1` → 3/4 exit 1.
   Case R (proper append): 4/4 exit 0. The counter is not broken; it is under-specified.
4. **Before-state reproduces exactly.** `--rev 8022f72c… --base 8022f72c…` prints
   `C2=FAIL checks=1/4` exit 1 with `DERIVED=S182:16 S183:11 RECORDED=S182:18 S183:13`, byte-equal
   to `corpus/evidence/round75/controls/before-c2.txt`.

## Findings

### F1 — HIGH — the measured bytes are first-regex-match anywhere, so an insertion-only edit rebinds `RECORDED` and a block can pass without correcting 18/13

`derive()` takes `QUOTE_A.search(text)` / `QUOTE_B.search(text)` (`c2-count.py:64-67`): the first
match in file order, not the authored bullet. Case K inserted, below the title and above the
authored bullets (zero removals, `numstat 6 0`):

```
Located quote: “The quick brown fox jumps over the lazy dog and then some more words here today” (20 words).
- Located quote: `alpha beta gamma delta epsilon zeta eta theta iota kappa lambda` (line 1, 19 whitespace tokens).
```

and appended a block naming 20/19, never 18/13. Observed:

```
DERIVED=S182:16 S183:11 RECORDED=S182:20 S183:19
CHECK Q1 PASS  CHECK Q2 PASS  CHECK Q3 PASS  CHECK Q4 PASS removed lines=0
C2=PASS checks=4/4 rev=caseK            EXIT=0
```

The authored lines are untouched: `git show caseK:corpus/lessons/round-74.md | grep -n '18 words\|13 whitespace tokens'`
still returns the two original bullets (`(18 words)` and `(line 163, 13 whitespace tokens)`).
So C2 — whose text is "the recorded 18 and 13 are superseded by 16 and 11" — can pass with the
recorded 18/13 never named in the block and never corrected. Q3 tests the digits of the
counter's own re-bound measurement, not "the superseded 18 and 13" of the claim sentence.
This is **not** covered by the disclosed limit in `corpus/lessons/round-74.md` Boundaries
("correction checks still use substring statements"): it is a measurement-point defect, not a
matching-semantics one.

### F2 — HIGH — Q2/Q3 test substring presence only; a block asserting the opposite, wrong magnitudes, or no prose at all scores 4/4

`checks.append(("Q2", n == 1 and str(n_a) in block and str(n_b) in block, …))` and the Q3 twin
(`c2-count.py:83-86`) test `"16" in block` / `"18" in block`. Observed passes, all exit 0:

- **Case D (negation):** block text `Correction withdrawn: the authored 18 words and 13 whitespace tokens are correct; 16 and 11 are miscounts of the same quotes.` → `C2=PASS checks=4/4`.
- **Case F (wrong magnitudes):** block text `… carry 161 and 117 whitespace tokens, superseding the recorded 18 words and 13 whitespace tokens.` → `C2=PASS checks=4/4`. ("16" matches inside "161", "11" inside "117".)
- **Case G (no statement at all):** whole block body is `<!-- 16 11 18 13 -->` → `C2=PASS checks=4/4`.

The claim's Check Q3 wording "names the superseded values 18 and 13 as superseded" is not what
the check does; polarity, adjacency, and even visibility are untested. The round-74 lesson
discloses the family limit for substring statements, but C2 as frozen records **no** limit at
all in `claims.md` under C2 (the "Recorded limits (QUALITY 126)" paragraph belongs to C1).

### F3 — MEDIUM — Q4 is an endpoint diff over a caller-supplied base; history and base identity are unverified

`c2-count.py:88-92` reads only `git diff --numstat <base> <rev> -- corpus/lessons/round-74.md`.

- **Case H:** commit 1 deletes an authored line under `## Boundaries`, commit 2 restores it
  verbatim and appends the correct block. History holds a real deletion; endpoint numstat is
  `4 0` → `C2=PASS checks=4/4`. "Append-only" is therefore a net-tree property, not an
  edit-history property.
- **Case S:** the non-append-only Case C scores `C2=PASS checks=4/4` when `--base` is the measured
  rev itself (`removed lines=0`). The base is never checked for ancestry or for preceding the
  edit, so any re-run with a drifting base silently neuters Q4.
Both are outside C2's pinned command (`--base 8022f72c…`), which is why this is medium and not
high: the claim's predicate is safe only by caller discipline, not by instrument.

### F4 — LOW — "appended at the end" (docstring `:11`) is not enforced

Case E inserted the correct block just above `## Mistakes` (pure insertion, `numstat 4 0`):
`Q1 PASS` (anchored count 1) → `C2=PASS checks=4/4`. Q1 counts headings; nothing checks that the
block is the last section or that its heading follows all authored content. The expectation is
restated as "appended correction block" in `SCORECARD.md:3363`, so the instrument is weaker than
the text it is cited for — though this alone cannot hide a wrong correction.

### F5 — LOW — missing-quote path exits 1 with no `C2=` line

Case L deleted every `Located quote:` line: output is `c2-count: located quotes not found` on
stderr and exit 1, with no `DERIVED=`, no `CHECK`, and no `C2=FAIL` line. Fail-closed on exit
code, but a driver that greps `C2=` records "no verdict" rather than FAIL.

## Residual risk

- C2's numbers cannot distinguish a correct block from F2's negation/wrong-magnitude/comment
  blocks at these inputs. Landing review must read the block by eye; the counter is a
  presence test, not a correction test.
- A landing that appends a genuine block (Case R shape) passes, and Case A/B/C prove wrong
  numbers and deletions are caught — so the counter does kill the two cheap forges (mis-numbered
  block, non-zero net deletion) while missing the four above.

## Verification gaps

- No C2 after-state receipt is committed: `controls/` holds `before-c2.txt` only, and at the
  frozen rev the predicate itself prints `C2=FAIL checks=1/4` exit 1 (`--rev 43a7a0db…`,
  `git diff --numstat 8022f72c… 43a7a0db… -- corpus/lessons/round-74.md` is empty). C2 is
  prospective at this freeze; the landing rev and its receipt must be named when scored.
- No digest binding for `c2-count.py` in the C2 text or `before-c2.txt`, unlike C1's matrix
  digests (`claims.md` C1 Instrument/Before). Frozen bytes were verified by me at
  `bf0250e7…`, not by the claim.
- Everything below was measured in a scratch fixture (`/fast/scratch/hyaku/chousa-r75/R75Review2/fix`,
  `git rev-parse --show-toplevel` asserted equal to it, throwaway identity, one commit per case,
  scratch removed). No lane, fleet, or production file was modified.
- No `lsp` device exists in this session and no Python language server is installed
  (`pylsp`, `pyright` absent), so caller/definition checks are text-only: a repo-wide grep for
  `round75/c2-count` finds three references, all invocations, no importer —
  `corpus/evidence/round75/claims.md:76`, `SCORECARD.md:3363`, `controls/before-c2.txt:3` — and the
  script imports only the stdlib and shells out only to `git` (`c2-count.py:40`). Nothing here is
  presented as semantic-reference proof.

## Commands and exits (exact)

Fixture: `D=/fast/scratch/hyaku/chousa-r75/R75Review2/fix`, base `e28e2ac3f95a` = committed copy of
`corpus/lessons/round-74.md` alone. Counter invoked by absolute path, `--lane "$D" --base <base>`.

| case | command (edit summarised) | observed | exit |
|---|---|---|---|
| real base | `python3 -B corpus/evidence/round75/c2-count.py --lane . --rev 8022f72c889c904b5657d52c7f29e1643392a216 --base 8022f72c889c904b5657d52c7f29e1643392a216` (cwd = lane) | `C2=FAIL checks=1/4`, DERIVED 16/11 RECORDED 18/13 | 1 |
| real freeze | same, `--rev 43a7a0db52c8aabdf32735f58e09610e05200e79` | `C2=FAIL checks=1/4`, Q1..Q3 FAIL, Q4 PASS | 1 |
| A | append block 17/12 naming 18/13 | Q1 P, Q2 F, Q3 P, Q4 P → 3/4 | 1 |
| B | append 16/11, omit 18/13 | Q1 P, Q2 P, Q3 F, Q4 P → 3/4 | 1 |
| C | correct block + delete 1 authored line | Q1 P, Q2 P, Q3 P, Q4 F `removed lines=1` → 3/4 | 1 |
| D | block negates the claim | 4/4 PASS | 0 |
| E | correct block inserted mid-file | 4/4 PASS | 0 |
| F | block says 161/117 + 18/13 | 4/4 PASS | 0 |
| G | block = `<!-- 16 11 18 13 -->` | 4/4 PASS | 0 |
| H | delete line (c1), restore (c2), append block | 4/4 PASS, endpoint numstat `4 0` | 0 |
| K | fake `Located quote:` lines inserted above; block names 20/19 | 4/4 PASS, RECORDED 20/19 | 0 |
| L | all `Located quote:` lines deleted | `c2-count: located quotes not found`, no `C2=` | 1 |
| M | spot-check copy with 99/88 committed in fixture | DERIVED unchanged 16/11 → 1/4 | 1 |
| N | only the block heading inserted | 2/4 | 1 |
| P | copy + rewrite parentheticals in place | Q4 `removed lines=2` → 3/4 | 1 |
| Q | delete file, write new rewrite at same path | Q4 `removed lines=35` → 3/4 | 1 |
| R | proper append (positive control) | 4/4 PASS | 0 |
| S | Case C with `--base caseC` | 4/4 PASS (`removed lines=0`) | 0 |

Every case above was run through the public `--lane --base --rev` CLI only; no instrument byte,
lane file, or committed receipt was modified. No tool install or upgrade was performed
(`git 2.56.0`, `python3` from the host); pacman untouched.

## Recommendation (advisory)

Admit C2 only with the block inspected by eye in the landing diff, and only if the landing receipt
names the measured rev. Do not restate C2 as "the counter proves the correction": at these inputs
it proves presence of four decimal substrings at a first-match measurement point that an append
can move, and a zero net deletion at a caller-chosen base.
