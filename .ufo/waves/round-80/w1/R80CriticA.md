# R80CriticA — falsification of the two frozen round-80 predicates

Lane `chousa`. Seat `R80CriticA` (critic, leaf). Frozen subject:
`corpus/evidence/round80/claims.md` at the claims-freeze commit
`0d253c95732c0ed19a9fa414e5d17769ddefa48d`; base revision
`b7803829922770b890e9f4efdd30d12c3695439a`. The round-79 closure lesson
(`corpus/lessons/round-79-verifier-spotcheck.md`) was read before anything was scored.

Every measurement below is my own run or my own read over committed bytes. The lane moved
while I reviewed (`0d253c95` -> `44d09edf` -> `5ba30d87`); each finding names the revision it
was measured at. My clone lived at `/fast/scratch/hyaku/chousa-r80/R80CriticA/lane`
(`git clone --shared`, detached at `0d253c95`) and is deleted; every receipt cited here was
copied into `.ufo/waves/round-80/w1/R80CriticA/receipts/` first.

No tool was installed or upgraded. No lane, fleet or sibling repository was mutated. No
frozen artifact was amended: all mutation happened in `/fast/scratch/hyaku/chousa-r80/R80CriticA/`
(`lane`, `dn` worktree, `src`, `rc`, `re`).

## 0. Answers in one place

| question asked of this seat | answer |
|---|---|
| Does C1's predicate enumerate exactly the set its kill rule counts? | **No — and worse, neither measures what it names.** The two are numerically aligned clause for clause, but `fresh_positive`/`fresh_forgers` are computed from a dict keyed by subject *name*, so a fresh positive and a fresh forger drawn from one base are merged and both scored MISS. Finding **F1**. |
| Is a sixth oracle, written today, rejected by construction or only by the fixed list? | **Only by the fixed list.** `ORACLES` is a literal five-tuple, `--fresh` draws subjects only, and the instrument takes no `--oracle` argument. Finding **F4**. |
| Does `superseded_resolved=3` measure a resolution or a re-filing? | **A re-filing.** A do-nothing round (base bytes + four empty rows + four records that quote the word `chousa` from `SOURCES.md:1`) prints the exact frozen predicate string at exit 0. Findings **F7**, **F8**. |
| Does `audited=S199,S200,S201,S202` name rows that exist only because this round added them? | **Yes.** 0 of the four exist at `b7803829`; the registry goes 198 -> 202 rows. Finding **F9**. |
| Are the claims.md instrument sha256 values the committed bytes? | **Yes, all six** — verified with `git show 0d253c95:<path> | sha256sum`. Finding **F11** records the gaps in that table. |
| Does `v7-legit-matrix-after.txt` name a revision or a worktree? | **A revision label over worktree bytes.** `LANE_REV=b7803829…` is `git rev-parse master` echoed at run time; every subject path is resolved from the worktree; the instrument does not exist at that revision. Finding **F6**. |

**Ruling on the two claims as written.** C1 does not verify: the frozen counting command
prints `BATTERY=FAIL … fresh_positive=1/2 fresh_forgers=1/2`, exit 1, on the committed
legitimate matrix at the freeze commit (`receipts/c1-frozen-command.txt`), so its own kill
rule fires on a matrix that is correct. C2 does not verify either: its predicate is reached
by a round that corrects nothing (`receipts/c2-donothing-control.txt`). Both failures are
predicate defects, not lane misbehaviour — the round's instruments do what they say, and the
two sentences frozen about them do not.

---

## 1. C1 — operability

### 1.1 Every clause of the predicate and every clause of the kill rule

Predicate, `claims.md` §C1 (one sentence, "the command exits 0 and prints exactly …"):

- **P1** exit status 0.
- **P2** the line starts `BATTERY=PASS`.
- **P3** `forgers_rejected=11/11`.
- **P4** `positive=2/2`.
- **P5** `fresh_positive=2/2`.
- **P6** `fresh_forgers=2/2`.
- **P7** `oracles_rejected=5/5`.

Kill rule, `claims.md` §C1:

- **K1** any of the eleven named committed forgers is a MISS.
- **K2** either of the two named committed positives is a MISS.
- **K3** either of the two drawn fresh positives is a MISS.
- **K4** either of the two drawn fresh forgers is a MISS.
- **K5** any of the five enumerated oracles is a MISS.
- **K6** the legitimate matrix is refused (blanket refusal is not a gain).

Pairing: K1<->P3, K2<->P4, K3<->P5, K4<->P6, K5<->P7, K6<->P4 (partial). Unlike round 79's
C1 — where the predicate counted six forgers and the kill rule said "any forger" — the two
enumerations here **agree in cardinality**. The defect is one layer down: the counts are not
counts of the thing K3/K4/K5 name.

### 1.2 F1 — the fresh leg is keyed by name, so a base collision makes both legs MISS

`matrix-battery-v7.py:508` builds

```
results = {name: [] for _group, name, _src, _pre in entries}
```

and `:624` builds the fresh names

```
fresh_list.append((group, f"{base_name}#{i}", copy))
```

The fresh positive and the fresh forger of slot `i` are drawn from a base chosen by
`POSITIVES[secrets.randbelow(len(POSITIVES))]` (`:460`). When both draws of one slot land on
the same base they carry the **same name** `"<base>#i"`, so both entries append into one
list, and at `:529-541` each is tested with `all(…)` over the *other's* observation:

- the POSITIVE entry needs `all(rc == 0 and full marks and PASS and content_ok)` and sees the
  forger's `rc=1, 0/12`;
- the FORGER entry needs `all(rc == 1 and marks[0] < marks[1])` and sees the positive's
  `rc=0`.

Both are reported MISS. Probability per slot is 1/2; with `--fresh 2` the chance that no slot
collides is 1/4, so **about 75 % of runs fail P5/P6 on a correct matrix**.

Deterministic A/B, same two copies, only the name changes
(`receipts/c1-name-collision-probe.txt`, instrument sha256
`35351b2328bb6a284da13e61240a6ec598f39a148b8d8948d4e3d60dd78d914d`):

```
SOLO SUBJECT POSITIVE P#0 ACCEPTED
SOLO SUBJECT FORGER F#0 REJECTED
# SOLO  fresh_positive=1/1 fresh_forger=1/1
SAME SUBJECT POSITIVE X#0 MISS
SAME SUBJECT FORGER X#0 MISS
# SAME  fresh_positive=0/1 fresh_forger=0/1
```

Command: `python3 -B corpus/evidence/round80/matrix-battery-v7.py`'s own `score()`, imported
from the committed file and driven with the committed witness matrix; the identical stdout
`matrix_exit=0 marks=12/12/PASS content=ok` / `matrix_exit=1 marks=0/12/FAIL content=ok`
appears in **both** runs.

Live occurrence on the frozen counting command (`receipts/c1-frozen-command.txt`, exit 1):

```
5:MATRIX RUN FORGER ref-counter#1 0 matrix_exit=1 marks=0/12/FAIL content=ok
10:MATRIX RUN POSITIVE ref-counter#1 0 matrix_exit=0 marks=12/12/PASS content=ok
37:MATRIX SUBJECT POSITIVE ref-counter#1 MISS
38:MATRIX SUBJECT FORGER ref-counter#1 MISS
...
BATTERY=FAIL forgers_rejected=11/11 positive=2/2 fresh_positive=1/2 fresh_forgers=1/2 oracles_rejected=5/5
```

Both individual runs are correct; both SUBJECT verdicts are wrong. Kill rule K3 and K4 fire
on a matrix that has done nothing wrong, and P5/P6 are unreachable except by luck.

Four independent runs of the frozen counting command at the freeze commit with the committed
legitimate matrix (`receipts/c1-frozen-command.txt` plus
`receipts/c1-frozen-command-repeat.txt`; `--runs 1 --fresh 2 --rev 0d253c95…`, identical
`MATRIX_SHA256=b79d6441057a01b27eb465c6b0625cd46502114f8b622b370c2cd2805c81913f`):

| run | fresh positives | fresh forgers | colliding slot | predicate |
|---|---|---|---|---|
| frozen command | `successor#0` ACCEPTED, `ref#1` MISS | `ref#0` REJECTED, `ref#1` MISS | slot 1 on `ref-counter` | **FAIL** (`1/2`, `1/2`) |
| repeat 1 | `successor#0` ACCEPTED, `ref#1` MISS | `ref#0` REJECTED, `ref#1` MISS | slot 1 on `ref-counter` | **FAIL** (`1/2`, `1/2`) |
| repeat 2 | `successor#0` MISS, `successor#1` ACCEPTED | `successor#0` MISS, `ref#1` REJECTED | slot 0 on `successor-counter` | **FAIL** (`1/2`, `1/2`) |
| repeat 3 | `ref#0` ACCEPTED, `successor#1` ACCEPTED | `successor#0` REJECTED, `ref#1` REJECTED | none | PASS (`2/2`, `2/2`) |

3 of 4 fail, on the collision, with `forgers_rejected=11/11 positive=2/2
oracles_rejected=5/5` unchanged every time. The prediction from the code is a 1/4 pass rate;
the measurement is 1/4.

Impacts: axes **operability** (the predicate cannot be used as a gate) and **calibration**
(the round's own after-receipt is a 1-in-4 draw presented as a stable result).

### 1.3 F2 — the round has one C1 measurement, filed twice

`corpus/evidence/round80/controls/v7-legit-matrix-after.txt` is 216 lines with no header.
`corpus/evidence/round80/controls/v7-legit-matrix-prefreeze.txt` is that same file with two
comment lines prepended:

```
$ sha256sum corpus/evidence/round80/controls/v7-legit-matrix-after.txt
5b49d45cd5eb5def3d774a81580b4028ecc1842c06132433942aa4250dd2ccf7  …
$ tail -n +3 corpus/evidence/round80/controls/v7-legit-matrix-prefreeze.txt | sha256sum
5b49d45cd5eb5def3d774a81580b4028ecc1842c06132433942aa4250dd2ccf7  -
$ diff …prefreeze.txt …after.txt | wc -l
3
```

Two independent runs cannot produce the same 216 lines: `score()` appends its `MATRIX RUN`
lines in the per-run permutation (`random.Random(secrets.randbits(64)).shuffle`), and the
fresh draws come from `secrets`. Identical output means one capture under two names, and the
file named *prefreeze* carries the **later** mtime (22:31 vs 22:30). The post-freeze
`v7-legit-matrix-r80.txt` **is** a second, genuinely different capture (different fresh
bases, different sha), so the duplicate is confined to the prefreeze/after pair.

### 1.4 F3 — `oracles_rejected=5/5` counts an instrument crash as a detection

`score()`'s oracle leg (`:628-638`) counts an oracle REJECTED whenever `not full`; a matrix
that never ran is `not full`. Four of the five oracles are rejected on **committed** subjects
and one is rejected by a crash (`receipts/c1-oracle-attribution.txt`, `receipts/c1-reemit-class-defect.txt`):

| oracle | POSITIVE | FORGER | rejected because |
|---|---|---|---|
| `summary-only` | 12/12 PASS, `content_ok=False` | 12/12 PASS, `content_ok=False` | content leg only |
| `contract-table` | 12/12 PASS, ok | 12/12 PASS, ok | forger leg (scores nothing) |
| `block-position` | 12/12 PASS, ok | 12/12 PASS, ok | forger leg (scores nothing) |
| `structure-identity` | rc=1, no output | rc=1, no output | **crash** |
| `payload-decode` | 12/12 PASS, ok | 11/12 FAIL, ok | fresh forger leg only |

`structure-identity` dies with

```
AttributeError: '_a2bd431b' object has no attribute 'canon'
```

`v7._rename` (`:255-278`) renames `ast.Name`, `ast.arg`, `FunctionDef.name`,
`ClassDef.name`, `ExceptHandler.name`, `Global/Nonlocal` and the `Match*` bindings, but it
never renames `ast.Attribute.attr`. A method definition is renamed; the call site
`self.canon(…)` is not. Minimal isolation — a six-line class, original vs re-emitted:

```
# original   : rc=0 out='OK x'
# re-emitted: rc=1 err="AttributeError: '_23ff6e79' object has no attribute 'canon'"
```

So re-emission is **not semantics-preserving for any subject that defines a class method**.
The eleven committed forgers and both positives carry no `class` (measured: `class=0` on all
thirteen), so the other clauses survive today; the first class-bearing forgery channel
submitted will be rejected by a traceback and counted as a detection. K5 says "is a MISS";
P7 counts "is not full". Those are different sets.

### 1.5 F4 — a sixth oracle is invisible, not impossible

`ORACLES` is a literal five-tuple (`:88-96`), `main()` iterates it once (`:628`), and there is
no `--oracle` argument; `--fresh` feeds `subjects` and `fresh_list` only. `oracles_rejected`
is printed as `{oracle_ok}/{len(ORACLES)}` (`:648`), so the denominator is *whatever the list
says* — the frozen `5/5` cannot distinguish "v7 rejects subject-identifying matrices" from
"v7 rejects these five". A sixth oracle written today is rejected by nothing: it is never
executed, and no clause of P7 has a slot for it.

The claim sentence is universal — "an oracle whose table was built from committed bytes
cannot reach the PASS line" — while P7 tests five instances of which **one** is stopped by
the fresh leg (`payload-decode`, `fresh_forger=0/2`). The other four fail on committed
subjects or on receipt formatting. P7 therefore evidences the claim's mechanism at 1/5, and
F3 removes one of those five from the count entirely.

### 1.6 F5 — the predicate does not bind the matrix, and `--runs 1` voids two legs

- `MATRIX_SHA256` is emitted (`:609`) but appears in no clause of P1-P7. The counting command
  in `claims.md` pins `--matrix corpus/evidence/round76/loader-matrix-v3.py`, but the
  predicate sentence only pins the *output*. K6 speaks about "the legitimate matrix" and has
  no corresponding predicate term.
- The frozen counting command passes `--runs 1`, while the instrument's own rule is "a forger
  is REJECTED only when **both** runs exit 1". At one run that clause is vacuous.
- The ORDER LEG is asserted in the docstring ("permuted per run with a fresh 64-bit seed …
  no digest of it is printed") but the receipt carries no order evidence at `--runs 1`
  (`--print-order` is a closure-removal twin, unused). The permuted order is only indirectly
  visible in the sequence of `MATRIX RUN` lines, which is not a stated pairing.

### 1.7 F6 — the after receipt names a revision it never opened, and the round has three

`v7-legit-matrix-after.txt` line 3 reads `LANE_REV=b7803829922770b890e9f4efdd30d12c3695439a`.
That value is `_lane_rev()` = `git rev-parse master` echoed at run time (`:611`, `:655-662`),
while every path is resolved from the worktree (`LANE = HERE.parents[2]`, `:101`) and every
subject is read with `reemit(source, work)` (`:518`). At `b7803829` the instrument
`matrix-battery-v7.py` does not exist. The receipt also carries **no `# command:` line and no
`# exit:` line** — uniquely among the round-80 controls — so P1 is unverified by it.

Three receipts now claim the same after-measurement: `v7-legit-matrix-after.txt` and
`v7-legit-matrix-prefreeze.txt` (frozen at `0d253c95`, one capture), and
`v7-legit-matrix-r80.txt` (added at `44d09edf`, a real second capture whose header does name
`--rev b7803829…`). The frozen claims name none of them.

This is round-79's routed defect 6 recurring: a control receipt must name the revision it was
measured at, and here the name is a label over worktree bytes.

---

## 2. C2 — calibration

### 2.1 Clauses

Predicate (`claims.md` §C2): exit 0 and
`GATE_GROUNDING=PASS unresolved=0 superseded_resolved=3` with `audited=` listing
`S199,S200,S201,S202`.

Kill rule: does not verify if any audited tip or superseded row resolves while
**R1** the named revision does not resolve, **R2** the named path is absent at that revision,
**R3** the named line does not contain the quote, or **R4** the quote's word count disagrees
with the record or exceeds 25; or if the counter reports `unresolved=0` while a
`GATE-RECORD` line names bytes it never opened.

The counter enumerates R1-R4 faithfully: `check()` (`:150-170`) applies exactly those four
and the negative control confirms R4 bites (`receipts/c2-r4-negative-control.txt`, a 26-word
quote -> `ROW S199 record=bad … verdict=UNRESOLVED`, `GATE_GROUNDING=FAIL unresolved=2`,
exit 1). The asymmetry is not in R1-R4; it is in *what the counter applies them to*.

### 2.2 F7 — `superseded_resolved=3` measures a re-filing, not a resolution

`check()` is called at `:177` for audited tips and at `:189` for **the superseder's** record
(`records.get(tip)`). The superseded row's own bytes are never opened — `rows_at` reads only
`teaches/status/opened/used-by` (`:66-85`), and nothing reads the S196/S197/S198 quote, the
stated word count, or the anchor span that the round-79 spot-check found defective.

A superseded row is therefore "resolved" by a syntactic fact: some other row's `teaches` cell
opens `supersedes S196`, and that other row carries a well-formed `GATE-RECORD` line whose
quote exists somewhere in the named file at the named revision — **any** file, **any** quote,
**any** subject.

**Do-nothing control** (`receipts/c2-donothing-control.txt`). Fixture: `b7803829` bytes + the
counter + four registry rows whose body is literally "nothing: this row exists only to be
counted" + a lesson with four `GATE-RECORD` lines whose quote is the single word `chousa` on
`corpus/SOURCES.md:1` — the registry quoting itself. No correction, no criterion, no fix
(`git diff --stat b7803829 HEAD` shows only the three files; `corpus/QUALITY.md` is
untouched).

```
GATE_GROUNDING=PASS unresolved=0 superseded_resolved=3 audited=S199,S200,S201,S202
# exit: 0
```

That is the frozen predicate string, character for character, at exit 0. **C2's counter is
satisfied by bookkeeping alone.**

What the claim would have to count instead, if it is to mean "resolves": (a) the superseded
row's own bytes re-opened and its stated quote/word-count/anchor compared with the
superseder's, with the delta recorded (27 -> 20 words, 25 -> 25, `lines 1-20` -> `line 11`);
(b) the superseder's quote bound to *the same source object* as the row it supersedes (same
`path` family and a stated relation), not just to a resolvable line; and (c) the parent's
`teaches`/`scope` cells bound to the child's, so a row cannot "supersede" an unrelated id.

### 2.3 F8 — a record's quote need not relate to its row

Demonstrated by F7's fixture: four rows about nothing, four records quoting `chousa` from
`corpus/SOURCES.md:1`, all `verdict=OK`. R3 is a substring test against the named line; no
clause ties the quote to the row's `source`, `scope` or `teaches` cell. A record can therefore
name bytes it opened and still say nothing about the row it grounds — which is the class of
defect round 79 opened this axis to close, one indirection further out.

### 2.4 F9 — the audit set is produced by the round's own append

At `b7803829` the registry holds 198 rows and no `S199`-`S202` (`git show b7803829:corpus/SOURCES.md
| grep -cE '^\|\s*S20[0-2]\s*\|'` -> 0). At `44d09edf` it holds 202. `audited=` is
`{tips} ∩ {ids a round>=79 lesson decides or records}` (`:157-166`), so the four names in the
frozen predicate exist *because the round wrote them*. A round that writes four rows and four
records and nothing else reaches the same line (F7).

The one thing the exact-string predicate does buy: `audited=` pins the set, so a round cannot
quietly drop a defective row out of the audit by malforming its cell count (`rows_at` skips
rows with fewer than 13 `split("|")` elements, `:75-77`) or by chaining a supersession over an
audited tip. That protection is real and should be kept.

### 2.5 F10 — kill-rule clause (iii) is raisable while the predicate passes

Kill rule: "or if the counter reports `unresolved=0` while a `GATE-RECORD` line names bytes it
never opened". The parent loop (`:185-196`) skips any parent that is not in `decided`, and
`check()` there reads the *superseder's* record. So a record on a superseded row outside the
audit set is never opened.

`receipts/c2-unopened-superseded-record.txt`: one extra row `S203` with
`teaches = supersedes S195 —`, one valid record for `S203`, plus

```
GATE-RECORD S195 rev=b7803829… path=corpus/lessons/does-not-exist.md line=9999 words=1 quote=x
```

`git cat-file -e b7803829:corpus/lessons/does-not-exist.md` -> rc 128 (absent). The counter:

```
SUPERSEDED S195 by S203 record=ok verdict=RESOLVED
GATE_GROUNDING=PASS unresolved=0 superseded_resolved=4 audited=S199,S200,S201,S202,S203
# exit: 0
```

`unresolved=0` with a `GATE-RECORD` line naming bytes it never opened: the predicate passes
and the kill rule's last clause is true at the same time. In this round's own landing the four
records are all on audited tips and all four are opened (`git grep -c '^GATE-RECORD ' 44d09edf --
corpus/lessons` -> 4, all in `round-80.md`), so the round is not in that state — but the
predicate cannot see it if it ever is.

Boundary, recorded not raised: `decided` treats a `GATE-RECORD` line for a tip as a decision,
so any record puts its row into the audit set; and `records_at` is last-write-wins over lesson
paths in `git ls-tree` order, which is lexical, not numeric — `round-79-…` sorts before
`round-80.md` by accident, and a `round-100` lesson would sort before `round-80`. A later
round can therefore silently replace an earlier record for the same id.

### 2.6 What C2 gets right

- `receipts/c2-before-repro.txt` and `receipts/c2-after-repro.txt` reproduce
  `grounding-before.txt` and `grounding-after.txt` line for line at `b7803829` and
  `44d09edf`, exit 1 and exit 0.
- Both C2 receipts name `--rev` explicitly and the counter opens bytes **at that revision**
  (`check()` uses `record["rev"]`, and R1/R2/R3 all read through `git show`). This is the
  binding C1's receipts lack.
- The frozen instrument sha256 `d9e426216665a098cd90adf8fbf5e5dd62e02dc7b5b707c322b404b3eb55c553`
  is the committed byte at `0d253c95` and is what all three C2 receipts carry.

---

## 3. claims.md consistency (the frozen file's own instrument table)

**F11 — hash table.** All six rows match the committed bytes at the freeze commit
(`receipts/claims-instrument-identity.txt`):

| instrument | claims.md | `git show 0d253c95:<path> \| sha256sum` |
|---|---|---|
| `matrix-battery-v7.py` | `35351b23…d78d914d` | `35351b23…d78d914d` |
| `oracle-check.py` | `580233ad…7c5e0289` | `580233ad…7c5e0289` |
| `gate-grounding-check.py` | `d9e42621…3eb55c553` | `d9e42621…3eb55c553` |
| `forgers/a10-payload-decode.py` | `3cb234be…690ca9f64` | `3cb234be…690ca9f64` |
| `round79/matrix-battery-v6.py` | `bb91406e…a61e1d` | `bb91406e…a61e1d` |
| `round76/loader-matrix-v3.py` | `b79d6441…5c81913f` | `b79d6441…5c81913f` |

The gap is the other four of the five oracles the kill rule enumerates. Only `a10` is pinned
by the claims table. `round79/forgers/forge-order-matrix{,-table,-block}.py` and
`R79ExecC/matrix-structure-identity.py` are named by **path** only; their bytes appear in no
frozen table (the structure matrix's sha256 `2614b11692367393ba1b339aa707c714a06ce72589b347075cbdb3c4f06428db`
is quoted only inside `oracle-structure-v6-accepted.txt`, i.e. inside a control, not in the
claim). One of those four (`structure-identity`) is a `.ufo/waves/` artifact rather than a
`corpus/` instrument — committed at `acca2449`, so it is durable, but it is land under
`.ufo/`, not under `corpus/`.

**F12 — one label, two computations (no defect observed).** `oracle-check.py:72` prints
`RECEIPT_LINES={len(p.stdout.splitlines())}`, i.e. a count taken from outside; the v6 and v7
batteries print their own `RECEIPT_LINES={_LINES + 2}` (`v6:406`, `v7:650`), i.e. a
self-count. The two agree by construction (a battery that miscounts its own trailer prints a
wrong trailer, and `len(lines)` then disagrees) and they agree in fact: the v6 control is
`113` both ways and the v7 receipt is 216 lines with `RECEIPT_LINES=216`. Recorded only so
the next reader does not treat the label as one field: `oracle-check.py`'s value is the
authoritative one and the battery's is the claim.

**F13 — `oracle-check.py` reads a crashed battery as an acceptance.** `rejected = p.returncode
!= 0 and last == "FAIL"` (`:70`): a battery that exits 2 without a `BATTERY=` line is
reported `ORACLE=ACCEPTED`, exit 1. That direction is safe (fails toward "not refused"), but
it means the C1 before-control's `ORACLE=ACCEPTED` is not by itself evidence the oracle
reached the PASS line — the receipt's `BATTERY_VERDICT=PASS` is, and it is present. Recorded,
not raised.

**Reproductions.** `receipts/c1-before-control-repro.txt` reproduces
`oracle-structure-v6-accepted.txt` exactly (`BATTERY_EXIT=0 BATTERY_VERDICT=PASS
RECEIPT_LINES=113`, `ORACLE=ACCEPTED`, exit 1), so the C1 do-nothing control is sound: at the
base the only battery is v6 and it accepts the structure-identity matrix.

---

## 4. What I did not test

- I did not run `--no-content`, `--no-permute`, `--print-order` or `--no-fresh` as full
  batteries; the content-leg attribution in F3 comes from applying `contract_table_ok` and
  `run_matrix` to the re-emitted oracles directly (ten child runs), not from a twin run.
- I did not build a sixth oracle that reaches the PASS line. F4 is demonstrated from the
  instrument's own control flow (no argument, closed loop, `len(ORACLES)` denominator) plus
  the frozen receipt's exactly five `ORACLE ` lines, not from a counterexample oracle.
- The two frozen v7 receipts could not be independently regenerated: both are the 1-in-4
  draw that avoids the F1 collision, so their `2/2` is real but not reproducible on demand.
- I did not attempt an outside-registry source (no network). Everything above is committed
  bytes plus local execution.

## 5. Smallest safe corrections

1. **F1** — key `score()`'s observations by `(group, name)` or by index in `entries`, not by
   name; or give fresh subjects the slot in the name (`f"{base_name}#{'P' if POSITIVE else
   'F'}{i}"`). One line at `:508` plus `:529-541`. Until then P5/P6 must not be read as a
   stable property: a FAIL at `1/2` is not evidence about the matrix.
2. **F3** — either rename `Attribute.attr` when its value is a bound `Name` inside the same
   class, or exclude method names from `_rename`; and make `score()` distinguish "the oracle
   produced no verdict" (rc without a `LOADER_MATRIX=` line, or a traceback) from "the oracle
   was refused", counting the former as an instrument error rather than REJECTED.
3. **F4** — restate P7 as `oracles_rejected=5/5` **on the enumerated list** and drop the
   universal sentence from the claim, or draw oracles the way subjects are drawn. As written
   the claim is broader than its counter.
4. **F5/P1** — put `MATRIX_SHA256=…` into the predicate string, and run the counting command
   at `--runs 2` so the instrument's own "both runs" rule is not vacuous.
5. **F6** — add `# command:` and `# exit:` to every control receipt and make `--rev` default
   to `"unavailable"` rather than `master` unless the run actually reads that revision; or
   make `LANE_REV` read `git rev-parse HEAD` **and** state that subjects are worktree bytes.
6. **F7/F8** — add a third operands pair to `GATE-RECORD`: `supersedes=<id> old_words=<n>
   new_words=<n>`; require the superseder's `path` to be the same object as the superseded
   row's `source`; and re-open the superseded row's bytes so `resolved` is a delta, not a
   presence test.
7. **F10** — iterate every `GATE-RECORD` id in `records`, not only audited tips and decided
   parents, so kill-rule clause (iii) becomes checkable; and order lesson paths by parsed
   round number instead of lexical path so a later round cannot overwrite an earlier record.
8. **F11** — move the four unpinned oracles into the claims table with their sha256, and
   prefer a `corpus/` copy over the `.ufo/waves/` artifact for the structure-identity oracle.

## 6. Receipt index

All paths relative to `.ufo/waves/round-80/w1/R80CriticA/receipts/`. Every one was produced by this seat
in `/fast/scratch/hyaku/chousa-r80/R80CriticA` and copied here before the scratch was purged.

| receipt | produced by | lines | sha256 |
|---|---|---|---|
| `c1-before-control-repro.txt` | oracle-check.py + v6 + structure-identity, exit 1 | 9 | `11b67a25e7c0a66570842ba657a499af7b517ba6669f8884a2003285e2af7d6a` |
| `c1-frozen-command-repeat.txt` | same command x3, exits 1/1/0 | 657 | `fab3a6ac9fa424aa2439fcb9d61da4e412d2929bd44ddec1ae9d9532ab4d0a7c` |
| `c1-frozen-command.txt` | frozen C1 counting command, --rev 0d253c95, exit 1 | 222 | `23ce02061a996ab34de62d88dfadb734048b8c031963dd95abe0e001b3816fdd` |
| `c1-name-collision-probe.txt` | v7 score() with shared vs distinct subject names | 17 | `d02e5c644b1ea083ffece105b1240fe8409496c1c5dedfb61ec3589e14a6b60d` |
| `c1-oracle-attribution.txt` | all five ORACLES entries, re-emitted, on one positive and one forger | 9 | `a1ecf7bce2f2bc497043189e8727fab8bd6a9e1f638cfaaa3804625edeafdddf` |
| `c1-reemit-class-defect.txt` | six-line class, original vs v7-re-emitted | 11 | `aa74139516f73ace688592c86d4f56ac1ecbe5a0f25780a96c8f139be285a9d5` |
| `c2-after-repro.txt` | C2 after at 44d09edf, diff vs committed receipt rc=0 | 15 | `910754870081c074a5b0a292a1c343c7c787e34d5e92ed7c8144297deb53e396` |
| `c2-before-repro.txt` | C2 before at b7803829, diff vs frozen receipt rc=0 | 11 | `236f32fc1d7344f660219c6d333b60c70fce97022de99dbe2d1af2ebc75fda75` |
| `c2-donothing-control.txt` | base + 4 empty rows + 4 records, exit 0 | 22 | `bff717c0c66431cfc2239fa23ca0c22a07f26b931e8e9412c3e3b0f9b3595cb4` |
| `c2-r4-negative-control.txt` | 26-word quote, exit 1 | 8 | `efe7a4de6afea4124f7e14def9e1cdc28d7b415fbc579fd930919ccc02e5e318` |
| `c2-unopened-record.txt` | GATE-RECORD for a non-tip, path absent at rev, exit 1 | 18 | `c0b6d146efa71ae80981fd47e13be07df271994a5ed62b05f422ca363336b462` |
| `c2-unopened-superseded-record.txt` | GATE-RECORD on a superseded row outside the audit set, exit 0 | 19 | `3b6a2a4cf6f657c2b28436539001e9a56898adb8124e9c12c7895c6c0f3afd3b` |
| `claims-instrument-identity.txt` | six instrument sha256 at 0d253c95 + registry census | 21 | `448322879198e19b9a5e09ee51f876b471b57306d00a578bb0a80c07afffedd0` |

Tool log: no package, binary or runtime was installed, upgraded or removed this seat.
