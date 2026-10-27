# R59Scribe28 — round-59 Gate/Mistakes draft: the positive verdict path is inverted, and the offline bound

Seat: scribe (leaf; no dispatch, no fetch, no install, no git/jj write). Axis **depth**. Lane
`/home/vgpnk/Projects/shokunin/chousa-shokunin`, lane HEAD `af8c0a4` (round-58 verifier spot-check). Round-59
evidence and wave directories are untracked at write time. Scratch `/fast/scratch/hyaku/chousa-r59/R59Scribe28/`
(removed before yield); the only lane write is this report.

Method note: this path carried an earlier draft by a prior instance of this seat (mtime 15:17). Every number
below was **re-derived from the frozen bytes in this session**; where my number differs from that draft's, the
new measurement is given and the difference is named (the weak-proxy bullet in §4). Nothing below is copied from a sibling report, and
no sibling in-flight report was read.

Read first: `corpus/lessons/round-58.md`, `corpus/lessons/round-58-verifier-spotcheck.md` (committed `af8c0a4`),
`corpus/evidence/round58/{claims.md,c1-count.py,c2-count.py,c2/quotes.tsv,controls/}`, `corpus/QUALITY.md`
criteria 103/110/115, `SCORECARD.md` round-58 block, `.ufo/waves/round-59/{w1-spec.json,w1-dispatch.json,w1.ready}`.

---

## 1. The round-59 freeze does not exist (measured; blocks every re-claim)

```
$ ls corpus/evidence/round59/            → census-start.txt  controls/
$ ls corpus/evidence/round59/controls/   → c1-before.txt   (958 B)
$ git ls-files corpus/evidence/round59 .ufo/waves/round-59   → (empty)
$ git status --porcelain                 → ?? .ufo/waves/round-59/
                                           ?? corpus/evidence/round59/
```

- **`corpus/evidence/round59/claims.md` is absent.** It is the file the lane context names and that every
  executor-level seat was told to read before work.
- The only C1 receipt is **byte-identical to round 58's**:
  `sha256sum` both files → `2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe` (958 B);
  `diff` is empty. Its mtime is `2026-10-27 15:14:30`, i.e. **135 s after `w1.ready` (15:12:15)**: a copied
  prior measurement, not a round-59 run, and it post-dates dispatch.
- `census-start.txt` **is** a genuine round-59 measurement: 6 validator lines. Re-running the validator
  read-only reproduces them exactly; the file additionally carries a hand-appended `exit=0` line:

  ```
  $ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
        --root /home/vgpnk/Projects/shokunin chousa   | wc -l   → 6   (rc=0)
  $ diff <that output> corpus/evidence/round59/census-start.txt
  6a7
  > exit=0
  ```
  Warnings: five `W04` duplicate-URL rows, `S051 S053 S073 S074 S075`, unchanged from round 58.

### 1.1 The wave has two records of what was asked, and they disagree

| artifact | items | what each item says |
|---|---|---|
| `.ufo/waves/round-59/w1-spec.json` | 66 | **66/66 are the same generated stub**: "For round 59, review ready handoff requirements. Read `<context's claims.md path>`; read before work…". It reproduces the phantom claims path 66× and contains **0** occurrences of `round58`, `C1`, `C2`, `positive`, `control`, `token`, `PASS`, `SOURCES`, `queued`, `offline` or `falsif`. |
| `.ufo/waves/round-59/w1-dispatch.json` (`registry.members`) | 66 | the real (templated) items: `round58` 33, `round59` 45, `positive` 16, `control` 37, `verdict` 21, `offline` 12, `SOURCES` 12, `claims.md` **0**. |

The 66 dispatched items collapse to **6 template classes** (16 executor / 14 reviewer / 12 scribe / 12 scout /
7 critic / 5 mutation-tester). After normalising seat name, scratch dir and report path, the class counts are
exactly those. **0/66** name an `S###` id, a file under `corpus/evidence/`, or a line number; the only
specificity is the executor template's "exact round58 frozen counter/tool or controls relevant to
positive-verdict-path defect" (16 seats). So each seat chose its own target inside a template, and the
`w1-spec.json` stub — the artifact a spec-level audit would read — drops the task entirely while carrying the
one path that does not exist.

Consequence for the Gate: **no round-59 claim can be stated against a frozen round-59 predicate.** The
positive-verdict-path calibration the milestone names (`w1-spec.json.milestone`: "build and falsify controls for
positive verdict-path calibration plus offline source reconnaissance") was measured here (§2–§4) but was never
frozen, and nothing in `corpus/evidence/round59/` can carry it.

---

## 2. C1 — the positive verdict path is not merely unreachable, it is inverted

Frozen bytes: `corpus/evidence/round58/c1-count.py`
`sha256 65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f` (406 lines). Probe: the module is
loaded with `importlib` (its `main` is guarded by `if __name__ == "__main__"` at `:405`), so the frozen
functions and verdict expression are exercised **unmodified**. No fixture battery was run (§8).

### 2.1 Defect A — the token comparison (named by round 58; re-measured)

`PASS = "pass"` (`:51`); refusal emitters return `f"{name}={PASS}(refused)"` (`:160`, `:223`, `:234`) and the
literal `ESCAPE_ENTRY=pass(refused)` (`:315`); the aggregate searches the opposite case:
`ref_pass = all(("=PASS" in l) for l in ref_legs)` (`:391`), and the summary counts `sum('=PASS' in l …)` (`:399`).

Measured on the module's own functions, seven honest refusals (one per declared refusal leg) →

```
PASS token: 'pass'   FAIL token: 'fail'
honest leg sample: FOREIGN=pass(refused)
honest: ok_pass=True ref_pass=False integrity=True denied_pass=True
        verdict=FAIL | REFUSE=0/7 | OK=4/4
```

A builder that refuses all seven hazards exactly as claimed prints `REFUSE=0/7`, `C1=FAIL`, exit 1.

### 2.2 Defect B — the inversion: `C1=PASS` is reachable **only** by failing the refusals and echoing the token

`expect_refuse`'s miss branch embeds builder-controlled text:
`return f"{name}={FAIL}(rc={proc.returncode}, reason {reason_classes!r} absent in {err[:160]!r})"` (`:157`),
where `err = (proc.stderr or "") + (proc.stdout or "")` (`:152`). So a *failing* leg can itself contain `=PASS`.

Probe with a stub process (`rc=1`, stderr `"something went wrong =PASS oops"`, reason classes absent):

```
inject leg sample: FOREIGN=fail(rc=1, reason ['FOREIGN-refused'] absent in 'something went wrong =PASS oops')
injected: ok_pass=True ref_pass=True integrity=True denied_pass=True
          verdict=PASS | REFUSE=7/7 | OK=4/4
```

Read together, A and B state one thing: the counter's PASS token is **only** obtainable from a builder that
failed every refusal while printing the token in its error text. The gate therefore does not measure
"refusals happened"; it measures "the error text contains `=PASS`". This is the round's positive-control
result in the most literal sense: build the positive control that criterion 115 asks for, and it fails; build
an anti-control that refuses nothing and echoes the token, and it passes.

### 2.3 Defect C — the control clause inherits B (this reconciles the round-58 receipt)

The controls block (`:362-382`) re-runs the same counter with `--builder <control>` and requires the nested
run's first `C1=` line to be exactly `C1=PASS`; otherwise `denied += 1`. Because Defect A makes
`C1=PASS` unreachable for any honest builder, **every honest control is "denied"**. That is precisely what the
round-58 control receipt records:

```
corpus/evidence/round58/controls/c1-controls.txt
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
```

so `DENIED=2/2` proves nothing: it would print identically if the "control" were the best possible builder.
The receipt's own interpretation line — "controls do not reach C1=PASS" — is true for the wrong reason.

### 2.4 Defect D — a declared *safe* leg is emitted as a refusal (not named by round 58)

`claims.md:9` freezes `ESCAPE_ENTRY` among the **safe** legs; `c1-count.py:315` emits it as
`ESCAPE_ENTRY=pass(refused)` (an entry-column `..` escape is refused, which is a *refusal* behaviour).
`ok_legs` includes it (`:384-385`) and `ok_pass` accepts any `=pass` (`:390`), so **`OK=4/4` counts three
acceptances plus one refusal** — the before-receipt's own `OK=4/4` cannot be read as "four safe behaviours".

Also in that block: `:389` is a dead assignment (overwritten by `:390`), and its expression would have accepted
`=pass(refused)` as an ok leg too — the verdict block was never executed against its own output.

### 2.5 Defect E — the control conjunct is vacuous at `DENIED=0/0`

`:393` is `denied_pass = (denied == total) if total else True`. The round-59 receipt prints `DENIED=0/0`
(no `--controls` argument), so the conjunct is `True`. This violates `corpus/QUALITY.md` criterion 103 ("zero
rows … is a failure, never a vacuous pass", `:949`) inside the frozen counter, and the round-59 baseline
repeats it.

### 2.6 Defect F — refusal reasons are self-attested text, not observed behaviour

The reason clause is `if not any(c.lower() in err.lower() for c in reason_classes)` (`:155`) over the
builder's own stdout+stderr. Measured on the frozen function:

```
expect_refuse("FIFO_TXT", rc=1, stderr="NOT_REGULAR", classes=["NOT_REGULAR","FIFO"], []) → FIFO_TXT=pass(refused)
expect_refuse("FIFO_TXT", rc=0, stderr="NOT_REGULAR", …)                              → FIFO_TXT=fail(rc=0, expected refusal)
```

A builder that does nothing but print the class name and exit nonzero passes the leg. The only behavioural
clauses in the battery are `rc != 0` and the `forbidden_touch` loop — and that loop is itself inverted (§2.7).
The FOREIGN leg avoids the helper and checks the surviving file directly (`:213-225`), which is why it is the
one leg whose evidence is behavioural.

### 2.7 Defect G — `forbidden_touch` semantics are inverted, and fixing the token alone would make it live

```
:154-158   for p in forbidden_touch:
               if not p.exists():
                   return f"{name}={FAIL}({p} was touched/removed)"     # fails when the path is ABSENT
```

i.e. a path in `forbidden_touch` is *required to exist*. Only `SYMLINK_OUT` passes a non-empty list
(`[real/"spans.tsv"]`, `:233`), and the caller papers over the inversion with an ad-hoc overwrite (`:234-236`).
Reproducing the two-line sequence with real `pathlib` objects:

```
hazard materialized, spans.tsv present -> SYMLINK_OUT=pass(refused)(target-dir-written!)
safe (dir untouched)                   -> SYMLINK_OUT=pass(refused)
```

So a builder that writes `spans.tsv` **through the symlink** — the exact hazard the leg exists to catch — ends
with a `=pass` token plus a footnote, while a builder that writes a partial file *other than* `spans.tsv` into
the target dir ends with `fail(...)(target-dir-written!)`.

Consequence for the planned repair: flipping `ref_legs`' needle to `=pass` (the obvious fix for Defect A) would
turn `SYMLINK_OUT` into a **live false pass** for the hazard case. The repair has to fix the helper's
semantics and make the note fatal in the same change. This is the single most useful thing this seat can hand
the next freeze.

### 2.8 The falsification matrix the milestone asks for

| control | declared expectation | measured on the frozen counter | source |
|---|---|---|---|
| honest builder satisfying all 11 legs | `C1=PASS`, exit 0 | `REFUSE=0/7`, `C1=FAIL`, exit 1 | §2.1 probe |
| failing builder echoing `=PASS` in stderr | `C1=FAIL` | `REFUSE=7/7`, `C1=PASS` | §2.2 probe |
| pinned round-55 builder (honest, near-conforming) | `C1=FAIL` | `C1=FAIL` (`CONTROL_build-spans-r55=denied`) | `controls/c1-controls.txt` |
| do-nothing builder (`REFUSEALL`) | `C1=FAIL` | `C1=FAIL` | `controls/c1-controls.txt` |
| any control, with `--controls` | must be able to differ | `DENIED=total` for every honest file; `=PASS(!)` only if it injects the token | §2.3 |
| no `--controls` at all | must not pass | `DENIED=0/0` → conjunct `True` | §2.5 |

Criterion 115 as written (`QUALITY.md:974`: "run the counter on a positive builder that satisfies each declared
leg and require its exact target token and success exit") is satisfied by the **forging** row and violated by
the **honest** row. It cannot separate "target reachable" from "target reachable by injection", so it needs a
second conjunct — an anti-control that must fail — or it will certify an inverted gate.

---

## 3. C2 — two real counter runs, both round-58 receipts reproduced exactly

The earlier draft re-derived the counter's predicates; this section **runs the frozen counter** (165 lines,
`sha256 dbb859612f9d018296b217baec76a5c6cb744609b7c95372dabae4d6691c8503`) against a scratch root. Pins
verified first:

```
tools/build-spans.py     1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6
tools/capture-text.py    2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573
captures/6dc68fd6….raw   6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3
```

Defined form: `python3 -B capture-text.py cache/6dc68fd6b32ce9c8dfcebce8.raw` →
**27,012 chars / 47,356 bytes**, `sha256 a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867`
(matches the round-58 opening record).

Scratch root tree: `root/tools/` (pinned copies), `root/corpus/captures → lane/captures` (read-only symlink),
`root/corpus/SOURCES.md → lane copy`, `root/corpus/knowledge → lane`, and
`root/corpus/evidence/round58/c2/{quotes.tsv,spans.tsv,spans/}` from the pinned builder.

### 3.1 The builder writes the **span start**; the counter wants the **quote occurrence**

Builder run: `python3 -B build-spans.py --quotes quotes.tsv --out out1 --cache cache` → `rc=0`,
`SPANS_ROWS=12 WRITTEN=12`; it prints `QUOTE S101 char <occurrence>` but writes `<occurrence> − 80` into the
`offset` column, because the span is `form[occ-80 : occ+len(quote)+80]`. Measured over all 12 rows:

| row | `offset` column | quote occurrence | column − occurrence |
|---|---|---|---|
| 1 | 235 | 315 | −80 |
| 2 | 250 | 330 | −80 |
| 3 | 510 | 590 | −80 |
| … | … | … | −80 (all 12) |

`bind(offset == occurrence)` **0/12**; `span == form[offset-80 : offset+len(quote)+80]` **0/12**;
`span == form[occ-80 : occ+len(quote)+80]` **12/12**. Both counter clauses (`:101` bind, `:105-108` span
window) are internally consistent with each other and agree with the occurrence reading; the contradiction is
between the counter and the **pinned builder**, not between the counter's own two clauses.

### 3.2 Run 1 — builder manifest (frozen counter, real output)

```
$ python3 -B corpus/evidence/round58/c2-count.py --root root --work work
ENTRIES=0/1 BOUND=0/1 REF_ID_UNBOUND=1
QUOTE_ROWS=12/12 CAPTURE_BOUND=0/12 ENTRY_QUOTES=0/12
SUBSTANCE=FAIL ANCHOR_BOUND=0/3 INFERENCE_GROUNDED=no STRAY_IDS=- NEW_GROUND=no REBUILD=MATCH
ERROR ENTRY_MISSING
ERROR PROVENANCE_TRIO
ERROR S101_NOT_IN_SOURCE
ERROR REF_ID_UNBOUND
ERROR CAPTURE_BIND:S101   ×12
ERROR CAPTURE_BOUND=0/12
ERROR ANCHOR_BOUND=0/3
ERROR ENTRY_QUOTES=0/12
ERROR NEW_GROUND_FAIL
C2=FAIL
EXIT=1
```

This is the `SCORECARD.md:2909` receipt line `CAPTURE_BOUND=0/12 … REBUILD=MATCH`, reproduced.

### 3.3 Run 2 — same manifest with the offset column rewritten to occurrences (real output)

```
$ python3 -B corpus/evidence/round58/c2-count.py --root root --work work
ENTRIES=0/1 BOUND=0/1 REF_ID_UNBOUND=1
QUOTE_ROWS=12/12 CAPTURE_BOUND=12/12 ENTRY_QUOTES=0/12
SUBSTANCE=FAIL ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=no STRAY_IDS=- NEW_GROUND=no REBUILD=FAIL
ERROR ENTRY_MISSING
ERROR PROVENANCE_TRIO
ERROR S101_NOT_IN_SOURCE
ERROR REF_ID_UNBOUND
ERROR QUOTE_NOT_IN_ENTRY:S101   ×12
ERROR BUILDER_REBUILD_MISMATCH
ERROR ENTRY_QUOTES=0/12
ERROR NEW_GROUND_FAIL
C2=FAIL
EXIT=1
```

This is the `SCORECARD.md:2909` second receipt `CAPTURE_BOUND=12/12 REBUILD=FAIL`, reproduced — including the
counter's own `BUILDER_REBUILD_MISMATCH` name for it. So the frozen predicate has exactly one property: no
manifest can satisfy bind and rebuild at once, because one clause reads the column as occurrence and the other
compares the file to a builder that writes span-start. The scratch root's missing entry accounts for the other
errors; they are not needed for this conclusion.

### 3.4 Three properties of the C2 counter that the round-58 lesson did not name

1. **Failure cascades suppress the measurements.** The per-row loop `continue`s on a bind failure (`:101-103`),
   so `SPAN_BYTES`, `QUOTE_NOT_IN_ENTRY`, `short`, `context` and `anchors` never execute. In Run 1
   `ANCHOR_BOUND=0/3` and `ENTRY_QUOTES=0/12` are therefore **artifacts of the bind failure, not findings about
   the entry** — with no entry at all, Run 2 reports the identical `ENTRY_QUOTES=0/12` but `ANCHOR_BOUND=3/3`.
   Any Gate sentence that reads `ANCHOR_BOUND=0/3` as "the anchors are wrong" is unsupported.
2. **The anchor floor is met with zero margin.** Under the occurrence reading only three quote occurrences are
   at a line start: `S101-1@315`, `S101-2@330`, `S101-10@993` (clause `:115`, threshold `anchors < 3` at
   `:134`). Re-cutting any one of those three quotes changes `ANCHOR_BOUND` to 2/3 and fails the claim.
3. **`NEW_GROUND` is a mis-variant probe and needs git history.** `:153` greps the base tree for `載体类型标识`
   (traditional `載`) while `:154` tests the entry text for `载体类型标识` (simplified `载`) — the same variant
   `claims.md:19` freezes. Today both strings are absent from `corpus/knowledge` at `b13ca7b` (both greps
   `rc=1`), so the clause is satisfied either way; it becomes **latent-wrong** the moment the base gains the
   simplified form, since the traditional-variant grep would still miss it and `new_ground` would stay true.
   Separately, the probe needs the pinned base in git: against a non-repository root `git -C root grep` returns
   **128**, so `new_ground` is `False` and the counter prints `NEW_GROUND_FAIL` (Run 1/2 above). A wave recipe
   that tells a seat to copy the lane to plain scratch and run this counter can never reach `C2=PASS` — the
   same class of defect criterion 110 dry-runs for.

---

## 4. Offline source reconnaissance — the hard bound for round 59 (no fetch)

Read-only over the lane:

- `corpus/SOURCES.md` rows **133**; statuses `mined 109`, `queued 19`, `rejected 5` (sums to 133).
- **15 rows carry no URL at all** (`S001, S034, S035, S036, S040, S041, S042, S043, S045, S065, S066, S068, S069,
  S070, S095`), all `mined` — own-work and internal-record rows. Any "N/133 rows re-openable" figure is capped
  at 118 by construction.
- Capture store: **129 files, 120 distinct sha256 digests** (member files dedupe by content).
- **Strict form** — a manifest-shaped evidence line naming both the row's URL and a digest whose bytes are in
  the store — **49/133** rows. All 49 are `mined`; ids `S082…S133`, 49 distinct. So the re-checkable part of
  the *mined* set is **49/109**; **60 mined rows have no offline-held bytes** under this reading.
- **Queued rows: 0/19** have any offline evidence under either reading.
- Weak proxy (URL string anywhere in the 705 text files under `corpus/evidence`, 1,492,585 B): **52/133**.
  This session measures 52 where the earlier draft on this path recorded 51; the method (suffix set
  `.tsv/.txt/.md/.json/.jsonl`, whole-file substring) is stated here so the figure is reproducible. It is a
  weak proxy either way and is not load-bearing.

Consequence: within round 59, "reconnaissance" can only re-open ground the lane already holds (49 rows, all
already mined). No queued row is reachable without a fetch, and the fetch-scope L0 question `8d77e6c1` remains
open — fleet `.ufo/l0-questions.md:136`: "Pending the still-open fetch-scope ruling (8d77e6c1): may a wave
dispatch item ever constitute egress approval on its own text?" (chousa round 41; id = fleet commit `8d77e6c1`,
"round-29: chousa L0 question (quote re-open fetch scope)"). Any round-59 sentence of the form "opened S1xx
(queued)" or "the reconnaissance advanced the frontier" is unsupported by lane bytes.

---

## 5. Draft `## Gate` for `corpus/lessons/round-59.md`

> ### Claims and controls
>
> - **No round-59 predicate was frozen.** `corpus/evidence/round59/claims.md` is absent; the directory is
>   untracked and holds only `census-start.txt` (a genuine validator run: 6 lines plus an appended `exit=0`)
>   and `c1-before.txt`, which is byte-identical to `round58/controls/c1-before.txt`
>   (`sha256 2c9bbe54…`, 958 B) and stamped 135 s *after* `w1.ready`. This round therefore re-claims neither C1
>   nor C2; it records control facts only.
> - **C1 (operability) — refuse to re-claim, and record that the gate is inverted.** The frozen counter's
>   refusal legs print `=pass(refused)` while the aggregate requires `=PASS`
>   (`c1-count.py:51,160,223,234,315,391,399`), so an honest builder passing all eleven legs prints
>   `REFUSE=0/7 C1=FAIL`. Measured on the frozen functions, the converse also holds: a builder that fails the
>   refusals and prints `=PASS` inside its error text reaches `REFUSE=7/7 C1=PASS`, because the miss message
>   embeds `err[:160]` (`:157`). The pass token is thus reachable only by forgoing the behaviour. Four further
>   measured defects: `ESCAPE_ENTRY` is declared a *safe* leg (`claims.md:9`) but emitted as a refusal (`:315`),
>   so `OK=4/4` is three acceptances plus one refusal; `denied_pass` is `True` at `DENIED=0/0` (`:393`),
>   vacuous against `corpus/QUALITY.md` 103; refusal reasons are matched in the builder's own output (`:155`), so
>   `rc≠0` plus the class name passes without a refusal; and `forbidden_touch` fails on an *absent* path
>   (`:154-158`), so the one hazard-materializing case leaves `SYMLINK_OUT=pass(refused)(target-dir-written!)`.
>   Flip: a re-frozen counter whose refusal emitters and aggregate share one token, whose controls include an
>   honest positive builder that reaches the exact target with exit 0 **and** an anti-control that refuses
>   nothing and must fail, with a non-zero `DENIED` denominator, receipted in the round's own evidence dir.
> - **C2 (depth, S101) — refuse to re-claim; both round-58 receipts now reproduced by the real counter.** For
>   the pinned builder's manifest the counter prints `CAPTURE_BOUND=0/12 … REBUILD=MATCH`; with the same
>   manifest's offset column rewritten to quote occurrences it prints `CAPTURE_BOUND=12/12 ANCHOR_BOUND=3/3 …
>   REBUILD=FAIL ERROR BUILDER_REBUILD_MISMATCH`. The builder stores span-start (`occurrence−80`, all 12 rows),
>   the counter binds and slices at the occurrence. `ANCHOR_BOUND=0/3` in the first receipt is a cascade
>   artifact (bind failure `continue`s past the anchor loop), not an entry finding; the occurrence reading
>   reaches the anchor floor with exactly 3 of 12. Flip: one producer and one predicate agreeing on the offset
>   column, re-frozen before wave data, with a positive manifest reaching `C2=PASS` and exit 0 on a
>   git-history-bearing root.
> - **Offline reconnaissance — admissible only as a measurement.** 49/133 registry rows have a manifest line
>   naming both their URL and store-held bytes, and all 49 are already `mined` (49/109 of the mined set); 0/19
>   queued rows have any offline evidence; 15 rows carry no URL. No row was opened this round. The fetch-scope
>   L0 question `8d77e6c1` stays open. Flip: an operator-approved research window, or a queued row whose bytes
>   are already in `corpus/captures/`.
> - **Refuse a new `SOURCES.md` row.** Rows 133 → 133; validator exit 0 with the same five W04 warnings at
>   round start. Nothing opened, so nothing to register.
>
> | surface | decision | evidence | flip |
> |---|---|---|---|
> | C1 re-claim | **refuse** | `:391` vs `:160`/`:315`; probe `ok_pass=True ref_pass=False`; converse probe `REFUSE=7/7 C1=PASS` from stderr injection | token-consistent re-freeze with a positive **and** an anti-control |
> | C1 "controls were exercised" | **refuse the reading** | `c1-controls.txt` `CONTROL_*…=denied`, `DENIED=2/2`; every honest control is denied by construction | a control that can differ: honest→PASS, forger→FAIL |
> | C2 re-claim | **refuse** | 12/12 `offset = occurrence−80`; builder manifest `CAPTURE_BOUND=0/12 REBUILD=MATCH`; occurrence rewrite `CAPTURE_BOUND=12/12 … REBUILD=FAIL ERROR BUILDER_REBUILD_MISMATCH` | agreeing producer/predicate, re-frozen pre-data |
> | round-59 freeze | **refuse the phrase "frozen"** | `claims.md` absent; baseline receipt byte-identical to round 58 and post-`.ready` | a committed claims file before `.ready` |
> | offline opening of a queued row | **refuse** | 0/19 queued rows have held bytes | approved fetch window, or store-held bytes |
> | a new SOURCES row | **refuse** | 133 → 133; census exit 0; five W04 unchanged | opened ground, then register |
>
> ### SOURCES changes
>
> Rows 133 → 133; added by tier A/B/C: 0/0/0. `scripts/sources-census.sh validate --root … chousa` exits 0
> with the same five W04 duplicate-URL warnings as `corpus/evidence/round59/census-start.txt`. Monitoring rows
> only — no identity, anchor or `used-by` cell changed. Counting command:
> `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 133.
>
> ### Outside spot-check
>
> The round-58 lesson recorded "no non-author sample available"; `corpus/lessons/round-58-verifier-spotcheck.md`
> (committed `af8c0a4`) is that sample — it re-opened both S101 decisions and agreed with both. Round 59 cites
> it as the non-author admit/reject record instead of re-asserting "none"; no lesson or `SCORECARD.md` line
> cites it today.

---

## 6. Draft `## Mistakes` rows

1. **calibration — a freeze named by reference was never written.** The round-59 context and all 66
   `w1-spec.json` items name `corpus/evidence/round59/claims.md`; the file is absent, the directory untracked,
   and the only C1 receipt is byte-identical to round 58's (`sha256 2c9bbe54…`) stamped 135 s after
   `w1.ready`. The `w1-spec.json` items are generated stubs that contain the real task nowhere; the real items
   live only in `w1-dispatch.json`. Captured-by: criterion 115's "before a future freeze" and criterion 110's
   dry-run duty both presuppose a freeze artifact. Fix: write and commit the claims file (predicate, counter
   pin, leg/quote sets, positive **and** anti-control) before writing `.ready`, and make the spec item the
   dispatch item rather than a stub. Flip: a committed claims file whose mtime precedes `w1.ready`, and a
   `w1-spec.json` whose item text matches what was dispatched.
2. **inverted gate — the pass token is reachable only by failing the refusals.** `expect_refuse`'s miss branch
   embeds builder output (`c1-count.py:157`), so a builder that refuses nothing and prints `=PASS` in its
   stderr yields `REFUSE=7/7 C1=PASS`, while an honest builder yields `REFUSE=0/7 C1=FAIL` (both measured on
   the frozen functions). Captured-by: criterion 115 requires a positive control but not an anti-control. Fix:
   build the pass/fail token from the counter's own emitter, never from the measured tool's text, and freeze
   **both** a positive and an anti-control in the same receipt. Flip: the honest builder reaches `C1=PASS` and
   the token-injecting builder prints `C1=FAIL`.
3. **vacuous — a control conjunct that passes with no controls.** `:393`
   `denied_pass = (denied == total) if total else True` returns `True` at `DENIED=0/0`, the value both before
   receipts print. Contradicts `corpus/QUALITY.md` 103. Fix: require `total > 0` and at least one must-deny
   control in every receipt that carries a verdict. Flip: a receipt with `DENIED=0/0` cannot print a verdict.
4. **inverted precondition — "forbidden" is implemented as "must exist".** `:154-158` fails the leg when the
   listed path is *absent*; only `SYMLINK_OUT` uses it, and `:234-236` patches the safe case by overwrite. A
   hazard-materializing builder that writes `spans.tsv` through the symlink therefore keeps
   `SYMLINK_OUT=pass(refused)(target-dir-written!)` (measured with the frozen helper). Fix: make a non-empty
   `forbidden_touch` fatal, drop the ad-hoc overwrite, and treat the target-dir contents as the observation.
   Flip: either state yields a leg token that matches the observed tree.
5. **semantic drift — a "safe" leg that is emitted as a refusal.** `claims.md:9` lists `ESCAPE_ENTRY` with the
   safe legs; `:315` emits `ESCAPE_ENTRY=pass(refused)`; `:390` accepts any `=pass`, so `OK=4/4` conflates
   three acceptances with one refusal. Fix: classify legs by the token the counter emits and keep separate
   accepted/refused denominators. Flip: `OK`'s numerator equals the number of legs that produced files.
6. **attestation instead of observation — refusal reasons are read out of the tool's own output.**
   `:155` matches `reason_classes` in `stderr+stdout`, so `rc≠0` plus the class name passes the leg with no
   refusal performed (measured: `FIFO_TXT=pass(refused)`). Fix: derive the class from the filesystem/IO state
   the leg created (as the FOREIGN leg does), or require the refusal text to be the only output and the hazard
   path untouched. Flip: a builder that names the class without refusing prints `=fail`.
7. **cascade — a single failed clause zeroes the clauses after it.** `c2-count.py:101-103` `continue`s on a
   bind failure, so the first receipt's `ANCHOR_BOUND=0/3`/`ENTRY_QUOTES=0/12` are artifacts, not
   measurements; Run 2 with the same (absent) entry reports `ANCHOR_BOUND=3/3`. Fix: count independent clauses
   independently and label cascaded clauses as not-measured. Flip: a run where the entry clauses differ from
   the bind outcome.

---

## 7. Round-58 spot-check intake (dispositions, append-only)

| round-58 routed obligation | status now | evidence |
|---|---|---|
| freeze must-pass positive controls before wave data | **partly landed, violated in practice** | criterion 115 exists (`QUALITY.md:974`) and is shown able to fail; round-59 has no freeze and no positive control |
| repair/re-freeze C1 token comparison | **not done**; and the naive fix is now known to be insufficient | `:391/:399` unchanged; §2.7 shows a token flip alone makes `SYMLINK_OUT` a live false pass |
| repair/re-freeze C2 offset/rebuild | **not done**; both receipts reproduced | §3.2, §3.3 |
| record the external admit/reject check in the next lesson | **open, source exists** | `corpus/lessons/round-58-verifier-spotcheck.md` (committed `af8c0a4`); cited by no lesson or `SCORECARD.md` line |
| keep correction append-only, reachable after receipts | **held** | `git log --oneline -6`: `af8c0a4, c9b08e9, 5da0a63, 718e8d2, 9e73a03, b13ca7b`; no rewrite observed |
| operator: dispatch prompt/handoff clarity | **carried, and now quantified** | 66 stub spec items vs 66 templated dispatch items in 6 classes; 0 items naming an S-id or evidence file; phantom `claims.md` in the context string |

---

## 8. Not run / limits (explicit)

- **The C1 fixture battery was not run end to end.** My C1 evidence loads the frozen module and exercises its
  own `expect_refuse` plus the verdict expressions with stub processes. The full battery (FIFO/DEVZERO/FAT_RAW
  /MANY_QUOTES, rebuild, held-out, symlink) needs a candidate builder and multi-minute scratch work that
  belongs to an executor seat; `REFUSE=0/7`, `OK=4/4`, `DENIED=0/0`, `C1=FAIL`, `EXIT=1` are cited from the
  committed/present receipts, not re-measured.
- **The C2 counter was run for real, but on a scratch root with no entry.** `ENTRY_MISSING`,
  `REF_ID_UNBOUND`, `QUOTE_NOT_IN_ENTRY`, `NEW_GROUND_FAIL` in §3.2–§3.3 are consequences of that root and are
  not claims about the lane. The load-bearing outputs are `CAPTURE_BOUND`, `ANCHOR_BOUND`, `REBUILD` and
  `BUILDER_REBUILD_MISMATCH`.
- **No git/jj write, no install, no fetch.** `corpus/evidence/round59/` and `.ufo/waves/round-59/` were read
  only; the census validator was run read-only (it writes only with `--out`).
- The 49-row offline bound is a **manifest-line intersection** (URL + store-held digest on one line of an
  evidence text file). It is stricter than the 52-row URL-in-text proxy but is not proof that each row's
  opening was re-verified this round.
- `NEW_GROUND`'s variant mismatch is **latent**, not currently firing: both character variants are absent from
  `corpus/knowledge` at `b13ca7b`.
- Round-59 wave results do not exist at write time; nothing here describes the round's after-state.

---

## 9. Artifact paths (relative to lane root)

- This report: `.ufo/waves/round-59/w1/R59Scribe28.md`
- Round-58 frozen inputs: `corpus/evidence/round58/{claims.md,c1-count.py,c2-count.py,c2/quotes.tsv,controls/}`
- Round-59 state: `corpus/evidence/round59/{census-start.txt,controls/c1-before.txt}`,
  `.ufo/waves/round-59/{w1-spec.json,w1-dispatch.json,w1.ready}`
- Rules and axes: `SCORECARD.md` (round-58 block), `corpus/QUALITY.md` 103 (`:949`), 110 (`:961`), 115 (`:974`)
- Scratch (removed): `/fast/scratch/hyaku/chousa-r59/R59Scribe28/`

**VERDICT.** The round-59 Gate must be **refuse-to-re-claim**. Measured, not inferred: `claims.md` is absent
and the sole C1 receipt is a byte-identical copy of round 58's stamped after `.ready`; C1's positive path is
*inverted* — an honest all-legs builder prints `REFUSE=0/7 C1=FAIL`, while a builder that fails every refusal
and echoes `=PASS` in its error text prints `REFUSE=7/7 C1=PASS` (both from the frozen functions); the round-58
control receipt's `DENIED=2/2` is guaranteed by that defect and cannot differ; C2's bind and rebuild are
mutually unsatisfiable for the pinned builder's manifest, and both round-58 receipts are reproduced by running
the frozen counter (`CAPTURE_BOUND=0/12 … REBUILD=MATCH` vs `CAPTURE_BOUND=12/12 … REBUILD=FAIL ERROR
BUILDER_REBUILD_MISMATCH`); 49/133 registry rows (49/109 mined) are offline-recheckable and 0/19 queued rows
are, with `8d77e6c1` open. Falsified as readings of round 59: "claims frozen before wave data", "`OK=4/4` means
four safe behaviours", "controls were exercised", "`C1=PASS` would evidence safety", "the C2 anchors are
missing" (a cascade artifact), and "a queued source can be opened offline". Depth contribution beyond the
round-58 lesson: the inversion (only forgeries can pass), the control clause's inheritance of it, the inverted
`forbidden_touch` precondition that makes the obvious token fix unsafe, the attestation-only reason checks, and
the real-counter reproduction of both C2 receipts including the `continue` cascade and the zero-margin anchor
floor.

---

## 10. Second instance — replication of §4, and the collision provenance the overwrite dropped

Appended by the earlier instance of this seat (its draft occupied this path until 15:25:58, then was replaced
by §1-§9 at 15:26:13). I did **not** re-measure §2-§3 and do not adopt them as mine; §1-§9 above stand as filed
by the instance that wrote them. What follows is independent and limited to what I ran.

**Path collision, facts.** My draft (18,625 B, sections 1-7, written 15:1x) is gone: `grep` for its distinctive
phrases in `.ufo/waves/round-59/w1/` returns 0 hits, no copy exists in that directory, and the file was rewritten
whole (mtime jumped 15:25:58 → 15:26:13, size 34,555 → 34,578 B). Two instances of `R59Scribe28` therefore shared
one report path; the later write won. The draft's §7 (scratch-collision addendum) was dropped in that overwrite
and is re-stated below. Nothing was restored over §1-§9: a superset report that explicitly cites the prior draft
is worth more to the wave than a reverted one.

**Independent replication of §4** (second implementation, my own code, read-only):

| quantity | §4 | this instance | verdict |
|---|---|---|---|
| rows / mined / queued / rejected | 133 / 109 / 19 / 5 | 133 / 109 / 19 / 5 | agree |
| rows with no URL at all | 15 | 15 (133−118 parsed) | agree |
| capture store | 129 files / 120 digests | 129 / 120 | agree |
| strict form (URL + store-held digest on one evidence line) | 49/133, all mined | 49/133, all mined, same 49 ids | agree |
| queued rows with offline evidence | 0/19 | 0/19 | agree |
| weak proxy, suffix set `.tsv/.md/.txt/.jsonl` | — | **51/133** (649 files, 1,164,358 B) | — |
| weak proxy, suffix set `+ .json` | **52/133** | **52/133** (706 files, 1,539,941 B); the one added row is **S084** | agree, delta explained |

So the 51 → 52 difference between the draft and §4 is entirely the `.json` suffix, not a measurement error:
`S084`'s URL appears only in JSON evidence. The remaining denominator gap is live, not methodological:
§4 scanned 705 files / 1,492,585 B, I scanned 706 / 1,539,941 B, and the difference is exactly
`corpus/evidence/round59/s101-open.txt` — 47,356 B, mtime 15:26, sha256 `a8e3e7ad213b6ec50479…`, byte-identical
to `corpus/evidence/round54/S101-text-form.txt`: the S101 defined form (27,012 characters) written into the
round-59 evidence directory during the wave. Consequence for wording: any "N/133 rows" sentence must name its
file set **and** its time, because the evidence tree is still growing while the wave runs.

**Collision provenance (re-stated from the dropped §7).** Scratch namespaces are per-seat by convention only.
`R59Executor07-2` reported a foreign C2 poison probe (`positive-path/poison-base.py`,
`positive-path/c2-poison-zh.stdout`, 15:23) in its namespace; my own was deleted and repopulated at 15:23-15:24
with a 66-file / 54 MB capture cache, a lane-copy `root/`, a `work/c2-rebuild/` tree whose `spans.tsv` is
byte-identical to the pinned-builder manifest, a census-validate output, and 15:24 `tmp*` working dirs; three
sibling scratch dirs (`R59Scribe17`, `R59Scribe19`, `R59Executor01`) were present in one listing and absent in
the next. I deleted my own bytes once and then left the foreign ones in place (a live writer was using the
path). Finding: a seat's "isolated scratch" claim needs file-level provenance — pinned sha and/or an mtime
window — not a directory name; `corpus/QUALITY.md` 105 covers lane containment, not cross-seat reuse.

**Not run by this instance.** No end-to-end `c1-count.py` or `c2-count.py` run (§2.2's injection probe, §2.7's
`forbidden_touch` inversion and §3's two counter runs are the other instance's measurements, unverified by me);
no fetch; no install; no edit to any counter, claim or control. My own C1 probe (importlib over the frozen
module) produced `expect_refuse → 'SYMLINK_OUT=pass(refused)'`, `ok_pass=True ref_pass=False`, `REFUSE=0/7`, and
the `DENIED=0/0` vacuity, consistent with §2.1/§2.4/§2.5.
