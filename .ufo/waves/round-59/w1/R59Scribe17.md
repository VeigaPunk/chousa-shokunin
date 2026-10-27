# R59Scribe17 — round-59 Gate/Mistakes wording draft, with a committed-text contradiction audit

Seat: `R59Scribe17` (scribe, leaf; axis: **depth**). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`,
all sources read-only. This file is my only lane write. Scratch `/fast/scratch/hyaku/chousa-r59/R59Scribe17/`
was created, was removed by a concurrent process before I finished (see §10), was recreated for one check, and
is absent now. No dispatch, no fetch, no install, no git/jj/index write, no counter edit, no claim edit.

Assignment: read the round-58 lesson and spot-check, draft evidence-backed round-59 Gate/Mistakes wording,
claim no check that was not run.

## 0. What the round-59 freeze is (and is not)

| input the assignment names | state observed | how |
|---|---|---|
| `corpus/evidence/round59/claims.md` | **absent** at 15:12, at 15:16, and at final recheck before writing | `ls corpus/evidence/round59/` → `census-start.txt`, `controls/` only; `stat` → ENOENT |
| round-59 counter / control builder | **absent** — no `.py` anywhere under `corpus/evidence/round59` | `find corpus/evidence/round59 -type f` → 2 files |
| round-59 claim predicate | **absent** | consequence of the two rows above |
| `.ufo/waves/round-59/predata/` | empty | `ls` |

So the draft below is **conditional**: it fixes what the round-59 Gate may say *now*, what it must say *if* claims
land, and what the round-59 `## Mistakes` rows can assert without borrowing round-58 predicates. I claim **no
round-59 measurement** anywhere in this file. I ran **no** C1/C2 counter; §2.4 is a predicate evaluation on
synthetic leg vectors, not a builder measurement.

## 1. Evidence ledger (commands run by me, exact observations)

| # | command | observation |
|---|---|---|
| 1 | `sha256sum corpus/evidence/round58/c1-count.py` | `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f` |
| 2 | `sha256sum tools/build-spans.py tools/capture-text.py` | `1ed2650a…c80bf6` (identical to the r55 pin) and `2c0140bc…3e2573` |
| 3 | `sha256sum corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` | `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3` (matches the r58 claim) |
| 4 | `python3 tools/capture-text.py <raw> > <scratch>/s101.txt` | exit 0; **27,012 code points** (47,356 bytes); quote `并以[文献类型标识/载体类型标识]表示` at offset **797**, count 1 |
| 5 | same output, probe offsets named by `corpus/SOURCES.md:111` | 11170 = `'ilizing the ocean current to g'`; 11205 = `'te electricity was propo'`; **34374 → OUT_OF_RANGE** (len 27012) |
| 6 | same output, probe r54's mapped counterparts | 11972 = `'为便于文献的统计和期刊评价…'`; 11993 = `'范围，提高检索结果的适用性…'`; 12123 = `'标准技术规范等);\nD——一般动态性信息…'`; 25123 = `'参考文献格式，参照ISO 690…'` |
| 7 | `sha256sum corpus/evidence/round59/controls/c1-before.txt` vs `…/round58/controls/c1-before.txt` | both `2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe`; `diff -u` → **IDENTICAL** |
| 8 | `cat corpus/evidence/round59/census-start.txt` | 5 W04 duplicate-URL warnings (S051, S053, S073, S074, S075) + `exit=0`; it differs from r58's only in `EXIT=0` → `exit=0` |
| 9 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | **133** rows |
| 10 | `git ls-files corpus/evidence/round58` | 17 files; **no** `measure-after`, `c1-measure-after` or `c2-measure-after` |
| 11 | `git log -S'34374' --oneline -- corpus/SOURCES.md` | only `1254ab2` (round 49); the S101 anchor cell has not been re-expressed since |
| 12 | `git log -S'corpus/lessons/round-58.md' --oneline -- corpus/SOURCES.md` | `c9b08e9`; the S101 `used-by` cell was updated there, the anchor cell was not |
| 13 | python compare of `.ufo/waves/round-59/w1-spec.json` items vs `w1-dispatch.json` tasks | 66 spec items, 66 dispatch tasks, **0 identical / 66 different**; `claims.md` appears in 66 item texts (67 lines incl. context) and in **0** dispatch task texts (1× in the shared context) |
| 14 | `stat -c '%y'` on wave files | dispatch 15:12:11 · `w1.ready` 15:12:15 · spec **15:14:46** · `c1-before` 15:14:30 |
| 15 | `git log --diff-filter=A -1 -- .ufo/waves/round-58/w1/R58ScribeCounterReceipt.md` | `c9b08e9`, same commit that added the r58 SCORECARD verdict |
| 16 | `git diff --stat c9b08e9 af8c0a4 -- SCORECARD.md` | empty — the r58 verdict text is unchanged at HEAD |
| 17 | predicate evaluation (§2.4) | `ok_pass=True ref_pass=False verdict=FAIL REFUSE=0/7` (correct legs) and `ok_pass=True ref_pass=True verdict=PASS REFUSE=7/7` (seven *failing* legs carrying the token) |
| 18 | `ls /fast/scratch/hyaku/chousa-r59/` | my own seat directory absent while 20 sibling directories existed — concurrent deletion, §10 |

## 2. F1 — the committed C1 verdict contradicts the committed C1 evidence

This is the finding the canonical round-59 wording must absorb. It is a **text/claim defect in committed
documents**, not a new counter measurement.

### 2.1 The committed texts

| document | line | text |
|---|---|---|
| `SCORECARD.md` (unchanged since `c9b08e9`) | `2908` | "frozen `ref_pass` searches uppercase `=PASS`, while every refusal emitter outputs lowercase `=pass`; **no builder can produce the required token**." |
| `corpus/lessons/round-58.md` | `## Mistakes` row 1 | "vacuous — frozen C1 counter **cannot represent its positive state**" |
| committed W1 evidence, same commit `c9b08e9` | `.ufo/waves/round-58/w1/R58ScribeCounterReceipt.md:67–88` | probe D against the **unmodified** frozen counter: seven `fail(…)` refusal lines → `SUMMARY OK=4/4 REFUSE=7/7 … C1=PASS`, `EXIT=0`; `realdir/spans.tsv` written through the symlink |
| the same report's verdict | `:131–133` | "*Token leak* — a scratch builder … emitting `=PASS` in stderr is credited `C1=PASS`, `REFUSE=7/7`, exit 0: **survives**" |
| round-59 re-run (independent) | `.ufo/waves/round-59/w1/R59Executor03.md:83–120` (run C, mtime 15:22:14) | same result from a different scratch oracle; `(target-dir-written!)` on the passing run |

So the universal in `SCORECARD.md:2908` — "no builder can produce the required token" — is falsified by a file
committed **in the same commit** (`c9b08e9`) and re-demonstrated this round. The round-58 lesson's weaker phrasing
("cannot represent its positive state") is true only for a *conforming* builder; the counter can represent a
positive state, just not a correct one, which is a worse defect than the lesson records.

### 2.2 Mechanism (static, from frozen bytes; digest `65da18bb…`)

`PASS = "pass"` (`:51`), and every refusal emitter interpolates that constant:
`expect_refuse` success (`:160`, used by FOREIGN `:223`, SYMLINK_OUT `:232`→`:234`, SYMLINK_CACHE `:250`,
FIFO `:263`, DEVZERO `:278`, FAT_RAW `:295`, MANY_QUOTES `:306`), while the aggregate (`:391`) and the summary
(`:399`) search `"=PASS"`. Hence no emitter can satisfy the aggregate.

But every failure branch of those same emitters interpolates **builder-controlled text**:
`expect_refuse`'s reason-absent branch embeds `{err[:160]!r}` (`:156–158`, `err = stderr + stdout`), and
FOREIGN's reason-unnamed branch embeds `{err!r}` (`:223`). There is no scrubbing (`grep -n
"replace(\|sanitize\|clean" corpus/evidence/round58/c1-count.py` → no match). Two consequences:

- a *conforming* builder is refused the token it earned (`REFUSE=0/7`, `C1=FAIL`);
- a *non-conforming* builder that refuses nothing by reason and prints `=PASS` in stderr satisfies `ref_pass`;
- `SYMLINK_OUT` is special: `:233–236` overwrites the leg with a lowercase pass **only if the target directory is
  empty**, so a passing verdict requires the leg to keep its fail line, which requires the target to be
  **non-empty** — i.e. the positive verdict requires the output-containment hazard to have fired (also stated
  independently at `R59Executor03.md` F2).

### 2.3 Why the control clause is vacuous

`--controls` (`:365–382`) re-runs the counter per control with `--builder <control>` and **no** `--controls`, so
the inner run's `DENIED=0/0`; since `ref_pass` is False for any control that does not echo the token, the inner
`C1=` line is always `FAIL`, so `DENIED` always equals `total` (`:381`) for every control that never prints
`=PASS`. `c1-controls.txt`'s `DENIED=2/2` is therefore entailed by the defect, not measured by it. (Scribe22 §
`:142–144` and `R58ScribeCounterReceipt.md` §4/§5 reach the same reading; I record it here because the Gate
wording must not cite `DENIED=2/2` as control evidence.)

### 2.4 Predicate evaluation I ran (what it does and does not prove)

I extracted the assignment nodes at `:389–394` and the `REFUSE=` `FormattedValue` at `:399` **verbatim from the
frozen file** with `ast.parse`/`ast.unparse`, `exec`'d them against two synthetic leg vectors, and evaluated the
summary expression:

```
CASE_A_correct_lowercase:       ok_pass=True ref_pass=False integrity=True denied_pass=True verdict=FAIL SUMMARY_REFUSE=0/7
CASE_B_failing_with_token_echo: ok_pass=True ref_pass=True  integrity=True denied_pass=True verdict=PASS SUMMARY_REFUSE=7/7
```

Case A's strings are the counter's own emitted forms. Case B's strings are *shaped* like the counter's fail
branches, with `err` containing `=PASS`. This proves the **aggregate arithmetic** on the frozen bytes; it does not
prove end-to-end reachability. End-to-end is proven elsewhere and is cited, not re-run: `R58ScribeCounterReceipt`
§3 (frozen counter) and `R59Executor03` run C (independent vehicle). My script bytes were lost with the scratch
directory (§10); the evaluation output above is the transcript of the run at 15:2x.

### 2.5 Drop-in wording

Do **not** write:

> no builder can produce the required token / `C1=PASS` is unreachable for any builder.

Write:

> The frozen counter is unsatisfiable **for a conforming builder**: every refusal emitter writes `pass` while the
> aggregate searches `=PASS` (`c1-count.py:51,160,223,234,391,399`), so eleven passing legs still print
> `REFUSE=0/7 C1=FAIL`. It is nevertheless satisfiable **by a non-conforming builder**, and only by one that fails
> all seven refusal legs while printing `=PASS` into its error text (the fail branches embed `err[:160]`/`err` at
> `:156–158,223`), and that also writes through the symlinked `--out` (`:233–236`). The token therefore measures
> rendered text, not refusals: `R58ScribeCounterReceipt.md:67–88` and `R59Executor03.md` §C print `C1=PASS`,
> exit 0, `REFUSE=7/7` over seven `fail` lines. Consequence: the round-58 C1 claim stays **unprovable** (no
> conforming builder can be certified) *and* the predicate is **unsound** (a non-conforming builder is
> certified). Both halves must be stated; the `SCORECARD.md:2908` universal is a carried text defect.

## 3. F2 — the wave was dispatched before any frozen claims existed, and the spec is not the dispatch record

- `w1.ready` 15:12:15 and `w1-dispatch.json` 15:12:11 precede the first round-59 evidence file (`census-start.txt`
  15:12:21) and the before receipt (`c1-before.txt` 15:14:30); `claims.md` was never created.
- `w1-spec.json` mtime **15:14:46** is *after* dispatch. Its items are **not** the dispatched instructions:
  0/66 equal, 66/66 different. For this seat: dispatched
  `"Read round58 lesson and spotcheck, draft evidence-backed round59 Gate/Mistakes or report wording…"` vs spec
  `"For round 59, review ready handoff requirements. Read …/round59/claims.md; read before work…"` — a different
  instruction, not just a wrapper. The only `claims.md` mention in the dispatched payload is in the shared
  `context` (1×), not in any of the 66 task texts.

Wording rule: quote `w1-dispatch.json` for *what was dispatched*; treat `w1-spec.json` as a post-dispatch rewrite.
Neither is a claim freeze — a freeze is a commit containing `claims.md` + predicate bytes (as `9e73a03` did for
round 58, verified: it added `claims.md`, both counters, and `c1-before.txt`).

## 4. F3 — the only round-59 pre-data receipt is a copy, and cannot be cited as a measurement

`corpus/evidence/round59/controls/c1-before.txt` is byte-identical to
`corpus/evidence/round58/controls/c1-before.txt` (sha `2c9bbe54…`, ledger #7). It contains no command line, no
counter path, no builder digest, and `DENIED=0/0` (no `--controls`), and ends `SUMMARY OK=4/4 REFUSE=0/7 …
C1=FAIL`, `EXIT=1`. Two admissible readings, both of which forbid calling it a round-59 measurement:

1. it was copied from round 58, or
2. it was re-run against the unchanged builder (`1ed2650a…`) and reproduced byte-for-byte.

Either way it is a **baseline**, not an after-receipt, and it cannot distinguish "round 59 measured" from "round
58 copied". Round 58's own target receipts (`c1-measure-after.txt`, `c2-measure-after.txt` per
`corpus/evidence/round58/claims.md`) are **absent** from the committed tree (ledger #10: 17 tracked files, none
named `measure-after`). Wording rule: a receipt line is citable only with `(a)` the exact command, `(b)` the
counter and builder digests, and `(c)` a fresh run directory; a byte-identical copy must be labelled
`baseline (copy)`.

## 5. F4 — S101 offline recon: which text form the offsets belong to

Verified this seat (ledger #3–#6, no network):

- the capture `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` is present and hashes to the r58 claim;
- the lane's defined form is `tools/capture-text.py`'s output: **27,012 code points**, and the r58 located quote
  `并以[文献类型标识/载体类型标识]表示` is at **797**, exactly once — the round-58 Gate sentence is true;
- the `SOURCES.md:111` anchor cell names "(UTF-16LE text of the raw .doc capture)" and lists 11170, 11205, 11993,
  12161, 13247, **34374**. In the defined form those first offsets fall in the document's English sample text
  (`'ilizing the ocean current…'`) and 34374 is **beyond the end** (27,012). The same content exists at the
  round-54 mapped offsets: 11972 (`为便于文献的统计和期刊评价…`), 11993, 12123, 25123 (`参考文献格式，参照ISO 690…`).
  `corpus/lessons/round-54.md:15` already records this class ("nine Registry offsets … index a whole-file UTF-16LE
  decode of the `.doc` that no lane command prints"), and the anchor cell has not been re-expressed since
  `1254ab2` (ledger #11–#12).
- the round-58 spot-check's conformance sentence is arithmetically wrong: it says the quote "is exactly **19
  whitespace-delimited words**" (`corpus/lessons/round-58-verifier-spotcheck.md:26`); the quote is **19
  characters, 1 whitespace-delimited word** (counted this seat). `Scribe22:101–102` found the same. The ≤25-word
  cap it invokes is `quote-reopen`'s `TOO_LONG` (`SKILL.md:88`), so the sentence tests nothing as written.

Wording rule for the round-59 Gate: name the form ("`capture-text.py` output, code-point offsets"), record 797
verified once, and do **not** copy cell-5 anchors into a round-59 claim. A register re-anchor is an L1/operator
write (append-only errata), not a seat write; no row was touched here.

## 6. F5 — criterion 115 exists, but its check is not reproducible from committed bytes

`corpus/QUALITY.md:974` (criterion 115) reads: "Check: before a future freeze, run the counter on a positive
builder that satisfies each declared leg and require its exact target token and success exit… Shown able to fail
(ran): the R58 positive-leg probe prints 11 passing leg lines but `REFUSE=0/7`, `C1=FAIL`, exit 1."

Verified: the cited block exists in committed text (`R58ScribeMistakeMine.md:57–83` and
`R58ScribeCounterReceipt.md:27–45`). But:

- the probe builders themselves are **not committed** — `git ls-files | grep -i mock-builder` → empty; the r58
  report says the scratch was removed; the token-leak probe (`probe-d-token-leak.py`) is likewise uncommitted;
- criterion 115 names no receipt path and gives no command line, unlike criteria that cite
  `corpus/evidence/…/measure-after.txt` (e.g. 108, 111, 113);
- its shown-able-to-fail is the **false-negative** direction only. The calibration this round's milestone names
  is two-sided, and the committed evidence for the false-positive direction
  (`R58ScribeCounterReceipt.md:67–88`) is not referenced by 115 or by `SCORECARD.md:2908`.

Proposed wording for the round-59 addition (draft only; I made no `QUALITY.md` edit):

> **A positive verdict path is calibrated only when both directions are committed.** Before a freeze, one
> conforming builder must reach the exact verdict token **and** success exit, and one builder that fails any
> declared leg must not reach it, even when it prints the token. Both controls ship under
> `corpus/evidence/<round>/controls/` with their command lines and digests, and the round's receipt cites them.
> Shown able to fail (ran): `R59Executor03.md` §B/§C/§E — conforming → `C1=FAIL`; hazard-accepting → `C1=PASS`;
> a one-token repair restores both directions but leaves `REFUSE=0/7` beside `C1=PASS` until `:399` is changed
> with `:391`.

## 7. Draft `## Gate` for `corpus/lessons/round-59.md`

Current state (claims never filed) — use Branch B verbatim; keep Branch A as the conditional template.

**Branch B (no claims filed; this is the only defensible round-59 Gate now):**

> **Round-59 freeze absent — no claim is made.** `corpus/evidence/round59/claims.md` does not exist; the wave was
> dispatched at 15:12:11 (`w1-dispatch.json`), its `.ready` was written at 15:12:15, and the only round-59 evidence
> files are `census-start.txt` and `controls/c1-before.txt`. No round-59 counter, control builder or predicate
> exists. The C1/C2 predicates and the C1 receipt in this Gate come from round 58 and are named as such; no
> round-59 measurement is reported and no axis moves.
>
> **Source opened / candidate decisions.** No live fetch (`8d77e6c1` still open, `.ufo/l0-questions.md:136,140`).
> Offline recon only: S101 was re-derived from the committed capture `6dc68fd6…raw` (sha verified) with
> `tools/capture-text.py` → 27,012 code points; the r58 located quote sits at 797, exactly once. Admit as source
> evidence only, not as a knowledge claim; reject any present-status/legal-force claim (no live authority). The S101
> register anchor cell still indexes an undefined whole-file UTF-16LE decode (round-54 lesson row 2); its offsets
> are not usable in the defined form (11170/11205 land in English sample text, 34374 is out of range, and the same
> content sits at 11972/11993/12123/25123). No row, anchor or claim byte was rewritten.
>
> **SOURCES changes.** Rows 133 → 133 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` →
> 133); no tier A/B/C row added; census validator `exit=0` with the five pre-existing W04 duplicate-URL warnings
> (S051, S053, S073, S074, S075) — `corpus/evidence/round59/census-start.txt`.
>
> **Outside spot-check.** Still unavailable for round 59: every seat is same-lane, and the round-58 spot-check is
> the last non-author sample. Its C1 recheck agrees on `unprovable` but omits the false-positive route, and its
> S101 sentence mis-units 19 characters as "19 words". No discernment improvement is claimed.

**Branch A (if claims land before filing):**

> Claims froze at `⟨freeze commit⟩` against `⟨base commit⟩`, with the file inventory `claims.md + counter(s) +
> controls` visible in that commit. Before → target: `⟨exact before receipt path, digest, command line⟩` →
> `⟨exact after receipt path, digest, command line⟩`. Predicate: `⟨one line from claims.md⟩`. Calibration: the
> conforming control reached `⟨verdict token⟩`/exit `⟨n⟩` and the hazard-accepting control did not, both receipts
> committed (`⟨paths⟩`). Where a claim repeats a round-58 predicate, state whether the token/substring defect
> (§2) was repaired or is carried, and do not describe the predicate as merely "unreachable".

## 8. Draft `## Mistakes` rows for round 59 (each with its evidence status)

1. **Contradiction in committed text — the C1 verdict's universal is falsified by its own commit.**
   Evidence: `SCORECARD.md:2908` ("no builder can produce the required token") vs
   `R58ScribeCounterReceipt.md:67–88,131–133` (`C1=PASS`, `REFUSE=7/7`, exit 0) — both added in `c9b08e9`, with
   `SCORECARD.md` unchanged at HEAD (`git diff c9b08e9 af8c0a4 -- SCORECARD.md` empty); re-demonstrated by
   `R59Executor03.md` run C. Captured-by: criterion 115's positive-path principle, applied in the second
   direction. Fix: carry the corrected two-sided sentence (§2.5); do not rewrite `SCORECARD.md` or the frozen
   lesson post-data — record it prospectively.
2. **Wave dispatched with no frozen claims, and the on-disk "spec" is a post-dispatch rewrite.**
   Evidence: §3 (timestamps; 66/66 divergent item texts; `claims.md` absent). Fix: freeze in a commit containing
   claims + predicate bytes before writing `.ready`; record the dispatch payload's own digest in `.ready`; treat
   only the dispatch payload as the instruction of record.
3. **The round-59 pre-data receipt is a byte-identical copy without a command line.**
   Evidence: §4 (`2c9bbe54…` both sides; `DENIED=0/0`; no header). Fix: every receipt carries its command line,
   counter digest, builder digest and fresh `--work`; copied baselines are labelled `baseline (copy)` and never
   cited as an after-state.
4. **The positive-control duty is written down but its probe is not committed.**
   Evidence: §6 (`git ls-files` finds no `mock-builder`; criterion 115 cites no receipt path; the leak probe is
   uncommitted). Fix: commit both control builders (conforming and hazard-accepting) and their receipts under
   `corpus/evidence/round59/controls/`, and cite them from the round's Gate.
5. **Conditional (only if round 59 files claims without an after-receipt):** "frozen predicate with no reachable
   after measurement" — evidence would be the missing `⟨after⟩` path; fix is to date the freeze, not to fit a
   receipt post hoc.

## 9. Sentences the round-59 report must not contain

| forbidden (seen in committed or in-flight text) | required replacement |
|---|---|
| "no builder can produce the required token" (`SCORECARD.md:2908`) | "no **conforming** builder can; a non-conforming builder can, via unsanitized stderr, and only while triggering the containment hazard" |
| "`C1=PASS` is unreachable for *any* builder" (`R59Scribe24.md:95,113`; `R59Scribe28.md:38`) | the two-sided sentence in §2.5 |
| "the counter cannot represent its positive state" (unqualified) | "it cannot represent a *correct* positive state; it can represent an incorrect one" |
| "the wave spec froze the claims" | "`w1-dispatch.json` recorded what was dispatched; no claims file exists" |
| "before receipt measures round 59" | "`c1-before.txt` is a baseline, byte-identical to round 58's" |
| "the quote is 19 words, under the 25-word cap" | "19 characters, 1 whitespace-delimited word" |
| "S101 char 11170/34374 located in the defined form" | "defined form offsets 11972/11993/12123/25123; 34374 is out of range" |
| "`DENIED=2/2` shows the controls cannot pass" | "`DENIED` is constant under the frozen predicate and tests nothing" |

## 10. Out of scope, not run, and the scratch incident

- **Not run:** any live fetch (L0 `8d77e6c1` open, no authorization); any C1/C2 counter invocation against a
  builder (Executor03 owns that surface; I cite its runs, I did not re-run them); C2 predicate re-execution
  (round-58 spot-check and lesson are cited, not re-derived); installs/upgrades (none needed; `RULES.md` unread
  because no install was attempted, `pacman` not run); no lane, fleet, sibling, `shokuknow` or `considerthese`
  write; no git/jj/index mutation.
- **Scratch incident (a finding, not a defense):** `/fast/scratch/hyaku/chousa-r59/R59Scribe17/` existed at 15:20
  with `predicate-demo.py` and `s101-ct.txt`, and by 15:23 the directory was gone while 20 sibling directories
  remained (`ls`, ledger #18). I did not delete it. The predicate script bytes are therefore lost; its output is
  preserved as the transcript quoted in §2.4, and I re-derived the S101 numbers in a fresh copy of the directory
  (ledger #4–#6) before removing it myself. `R59Executor03.md`'s "Scratch collision" note (its parent directory
  held another seat's `c1-count.py`, `controls/`, `probe-d-token-leak.py` at 15:14) is the same class: the
  per-seat scratch convention is not enforced, so a "receipt reproduced from scratch" claim in this round cannot
  be audited afterwards. Peer report (not my observation): `R59Executor07-2` states a C2 poison probe
  (`positive-path/poison-base.py`, `positive-path/c2-poison-zh.stdout`) appeared at 15:23 in its own namespace,
  created by no known seat and left in place. Not mine: I wrote only `predicate-demo.py`, `s101-ct.txt`, `s101.txt`
  under `R59Scribe17/`. Round-59 wording should scope any scratch-derived claim to the transcript.
- **Limits:** the §2.4 evaluation is a predicate arithmetic check on synthetic leg vectors; the end-to-end claim
  rests on the cited reports' transcripts, whose probe builders are uncommitted (mine included). Nothing here
  adjudicates the round-58 C1 claim's verdict; that stays L1's.

## 11. Provenance

| object | revision / digest | observed |
|---|---|---|
| `corpus/evidence/round58/c1-count.py` | `65da18bb…1c703d3f` | `sha256sum`; line numbers cited are from these bytes |
| `corpus/evidence/round58/controls/build-spans-r55.py` = `tools/build-spans.py` | `1ed2650a…1c80bf6` | `sha256sum` |
| `tools/capture-text.py` | `2c0140bc…033e2573` | `sha256sum` |
| `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` | `6063a3af…6d9fddf3` | `sha256sum`; `capture-text.py` → 27,012 code points |
| round-58 freeze / base / W1-record / spot-check commits | `9e73a03` / `b13ca7b` / `c9b08e9` / `af8c0a4` | `git cat-file`, `git log --diff-filter=A`, `git diff --stat` |
| S101 anchor origin | `1254ab2` (round 49); `used-by` → `c9b08e9` | `git log -S` |

Report: `.ufo/waves/round-59/w1/R59Scribe17.md`
