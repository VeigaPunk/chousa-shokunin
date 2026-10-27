# R59Scribe23 (attempt 2) — Round 59 Gate / Mistakes drafts, recalibrated on the positive verdict path

seat: R59Scribe23 · retry identity `R59Scribe23-2` (`.ufo/waves/round-59/w1.ready.partial`, 15:21:33)
lane: `chousa-shokunin`, root `/home/vgpnk/Projects/shokunin/chousa-shokunin` (read-only for this seat)
read window: 2026-10-27 15:20–15:22 -03:00 · no lane writes outside this report · no installs · no fetch
assignment: read the round-58 lesson and verifier spot-check; draft evidence-backed round-59 Gate/Mistakes
(or report) wording; do not claim unrun checks.

**Evidence classes.** `RAN` = command executed by this seat now, output quoted verbatim. `READ` = bytes
read, no execution. `DERIVED` = static consequence of read bytes, line-cited. `PEER` = another seat's
report, attributed by path and line; not re-run by this seat.

**Retry disclosure.** A report already existed at this path when this attempt started
(29,693 B, mtime 15:20), written by the previous attempt at this seat. This attempt re-ran its
load-bearing measurements independently, kept what held, and records corrections in §5. Nothing was
inherited as `RAN` without re-execution.

## 0. Headline (what the round-59 wording must say)

The milestone is "build and falsify controls for **positive verdict-path calibration**". Measured state:

1. **No round-59 claim was frozen.** `corpus/evidence/round59/claims.md` does not exist at any point in
   this read window; the round-59 evidence directory is untracked at HEAD
   `af8c0a460d087cbfb8245fb9326608783ccc510b`; there is no round-59 counter. The wave context names
   the missing file (the spec repeats it 67 times across its 66 templated items); the 66 dispatched
   items do not (0/66, §5.2). So no claim-level `before → after` verdict is possible.
2. **The inherited counter's positive path is inverted, and this is now measured in both directions.**
   `ref_pass = all(("=PASS" in l) …)` (:391) can never be true for an honest refusal emitter that
   prints `=pass` (:51, :160), so `C1=PASS`/exit 0 is unreachable for *every* honest builder; but the
   same substring test reads whole leg lines that embed the builder's own stderr (`{err[:160]!r}`,
   :150–161), so a builder that prints the token reaches `C1=PASS` while its hazard legs are printed
   `fail(...)` (PEER `R59Executor03` § Runs C). `R59Executor01` §2 reaches `C1=PASS` with an honest builder
   only after a one-token scratch repair; `R59Executor02` then shows that repaired gate credits a
   zero-check forge — **satisfiable but non-discriminating**.
3. **Zero positive and zero negative controls exist for round 59.** `corpus/evidence/round59/controls/`
   holds one file (`c1-before.txt`), which is byte-identical to round 58's before-receipt and opens
   with `EMPTY_OK=pass` — no command, digest, builder pin, timestamp or exit-code provenance.
   `denied_pass` accepts `0/0` (:393).
4. Therefore the adoptable verdict is **unfrozen + unprovable**, not "controls were built and
   falsified". The falsification evidence below is *counter calibration*, not operability of any
   candidate: no candidate was hardened this round.

## 1. State at read time (`RAN`)

```
$ date -u                                  → Tue 27 Oct 2026 18:21:40 UTC  (15:21:40 -03:00)
$ git rev-parse HEAD                       → af8c0a460d087cbfb8245fb9326608783ccc510b
$ git status --porcelain                   → ?? .ufo/waves/round-59/
                                             ?? corpus/evidence/round59/
$ git ls-tree -r --name-only HEAD corpus/evidence/round59
                                           → (no output)
$ ls corpus/evidence/round59/
                                           → census-start.txt  controls/
$ ls corpus/evidence/round59/controls/     → c1-before.txt
$ ls .ufo/waves/round-59/w1.ready.dispatched .ufo/waves/round-59/w1-results.json
                                           → both: No such file or directory
$ ls .ufo/waves/round-59/w1/*.md | wc -l   → 51
```

| artifact | mtime (-03:00) | size | state |
|---|---|---|---|
| `.ufo/waves/round-59/w1-dispatch.json` | 15:12:11 | 77,324 B | 66 members, 0 resumes |
| `.ufo/waves/round-59/w1.ready` | 15:12:15 | 154 B | names `w1-dispatch.json`, L1 `ChousaR59` |
| `corpus/evidence/round59/census-start.txt` | 15:12:21 | 535 B | `exit=0`, five W04 duplicate-URL warnings |
| `corpus/evidence/round59/controls/c1-before.txt` | 15:14:30 | 958 B | sha256 `2c9bbe54…aebfe` |
| `.ufo/waves/round-59/w1-spec.json` | 15:14:46 | 30,346 B | **after** dispatch and `ready`; 66 templated items |
| `.ufo/waves/round-59/w1.ready.partial` | 15:21:33 | 1,500 B | 66 name→agent pairs, 11 retry suffixes |
| `corpus/evidence/round59/claims.md` | — | — | **absent** |
| `.ufo/waves/round-59/w1.ready.dispatched` | — | — | **absent** |
| `.ufo/waves/round-59/w1-results.json` | — | — | **absent** |

Retry pressure is visible and growing inside the wave: `w1.ready.partial` was 414 B with 5 retry
suffixes (mtime 15:17:38, PEER prior attempt), 950 B with 10 (15:20, this seat), 1,500 B with 11
(15:21:33, this seat). Current pairs include `R59Executor12-3`, `R59Executor13-3`, `R59Scout31-3`,
`R59Scribe23-2`. Reports went 37 → 48 → 51 over the same interval.

## 2. Inherited artifacts, re-verified byte-for-byte (`RAN`)

```
$ sha256sum corpus/evidence/round58/c1-count.py            → 65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f
$ wc -l corpus/evidence/round58/{c1-count.py,c2-count.py,claims.md}
                                                           → 406 / 165 / 25
$ sha256sum corpus/evidence/round59/controls/c1-before.txt corpus/evidence/round58/controls/c1-before.txt
                                                           → both 2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe
$ diff corpus/evidence/round59/controls/c1-before.txt corpus/evidence/round58/controls/c1-before.txt
                                                           → (no output; IDENTICAL)
$ sha256sum tools/build-spans.py corpus/evidence/round58/controls/build-spans-r55.py
                                                           → both 1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6
$ sha256sum corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw  → 6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3
$ sha256sum tools/capture-text.py                          → 2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573
$ ls -l corpus/evidence/round58/controls/                  → REFUSEALL.py, build-spans-r55.py, build-c1-controls.py, …
```

Three consequences, each from bytes:

- The round-59 "before" receipt is **the round-58 receipt**, not a measurement of round 59. It has no
  header (`head -1` → `EMPTY_OK=pass`); round 58's `c1-controls.txt` does carry a `Command:` header.
- The candidate builder is **the pinned control builder** (`1ed2650a…`), so the receipt's one
  passing integrity clause (`BEFORE_FOREIGN=deleted`) compares the candidate with itself.
- The round-58 controls directory holds the deny pair; the round-59 directory holds **neither** a deny
  control nor a positive control. Round 59 is weaker than "deny-only", the exact state criterion 115
  (`corpus/QUALITY.md:974`) was written against.

## 3. Mechanism: the positive path is inverted in both directions (`READ` + `DERIVED` + `RAN` witness)

Line citations are to `corpus/evidence/round58/c1-count.py` (sha256 `65da18bb…`, 406 lines):

| line | bytes | consequence |
|---|---|---|
| :51 | `PASS = "pass"` / `FAIL = "fail"` | one lowercase vocabulary |
| :150–161 | `expect_refuse(...)`: `=FAIL(rc=0, expected refusal)`; `=FAIL(rc=… reason {reason_classes!r} absent in {err[:160]!r})`; `=PASS(refused)` | every refusal leg prints **lowercase**, and the reason-absent branch **embeds builder stderr inside the leg line** |
| :158–159 | `for p in forbidden_touch: if not p.exists(): return f"{name}={FAIL}({p} was touched/removed)"` | inverted containment test: a *correct* refusal with nothing written fails this branch |
| :233–236 | `legs.append(expect_refuse("SYMLINK_OUT", … [real/"spans.tsv"]))`; `if not any(real.iterdir()): legs[-1] = f"SYMLINK_OUT={PASS}(refused)"`; `else: legs[-1] += "(target-dir-written!)"` | the write-through marker is appended to, never subtracted from, a passing leg; an empty target dir is force-PASSed |
| :389–390 | `ok_pass = all(("=pass" in l) …)` (the `:389` expression is dead, overwritten at `:390`) | safe legs use lowercase |
| :391 | `ref_pass = all(("=PASS" in l) for l in ref_legs)` | refusal legs require **uppercase** |
| :392 | `integrity = any(l == "BEFORE_FOREIGN=deleted" …)` | exact-equality on one leg |
| :393 | `denied_pass = (denied == total) if total else True` | empty control set passes |
| :394 | `verdict = "PASS" if (ok_pass and ref_pass and integrity and denied_pass) else "FAIL"` | `ref_pass` is a constant `False` for honest emitters |
| :399 | `REFUSE={sum('=PASS' in l for l in ref_legs)}` | the summary repeats the uppercase test, so it can print `REFUSE=0/7` on a `PASS` verdict |

`RAN` unit witness (scratch, no lane bytes; models the two leg strings the counter produces):

```
honest '=pass': True | honest '=PASS': False
forged  '=PASS': True | forged '=pass': False
ref_pass over 7 forged legs: True
```

The honest leg string is `FIFO_TXT=pass(refused)`; the forged one is
`FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR'] absent in 'boom =PASS')`. The verdict therefore has two
states and neither is a measurement of builder behaviour: `FAIL` for correct candidates, `PASS` for
candidates that print the token into stderr.

## 4. What peer seats measured this round (`PEER`, attributed, not re-run here)

| seat | builder / counter | result | location |
|---|---|---|---|
| `R59Executor01` | maximal honest builder (136 lines, scratch) on the frozen counter | all 11 legs pass, `REFUSE=0/7 C1=FAIL`, exit 1 | report §1 |
| `R59Executor01` | same builder, counter patched **one token** (:391 `=PASS`→`=pass`) | `C1=PASS`, exit 0, `DENIED=2/2` | §2 |
| `R59Executor01` F3 | after the token repair, a builder that writes `spans.tsv` through the symlinked `--out` before refusing | still `C1=PASS` — containment unsound | §4, §5 table |
| `R59Executor01` F2 | summary line on a PASS verdict | prints `REFUSE=0/7`, contradicting the verdict line | §2 |
| `R59Executor02` | zero-check, name-keyed forge on a token-corrected counter | `REFUSE=7/7 C1=PASS` — **false positive** | §3 table |
| `R59Executor02` | correct-output builder (`--seed 35`) | `OK=3/4` false negative persists | §3 table |
| `R59Executor03` | forge that prints `C1=PASS` to stderr, frozen counter | `REFUSE=7/7 C1=PASS`, exit 0, and the symlinked `--out` receives `spans.tsv` (28 B) | § Runs C |
| `R59Executor05` | token-only diagnostic copy (sha256 `21dae5d3…eeba`) on a positive mock | `REFUSE=7/7 C1=PASS`, exit 0 | §5 |
| `R59MutationTester63` | verdict-gate mutant (`if True`) | `C1=PASS` while the same leg output still shows failures — mutant **survived** | whole report |

No seat reports an honest, unpatched, frozen-counter `C1=PASS`. The three `PASS` receipts split into:
(a) token-repaired counter (Exec01 §2, Exec05 §5), (b) forgery through stderr (Exec03 run C),
(c) verdict-gate mutation (MutationTester63). This is the calibration answer the milestone asked for:
**the positive path exists, but only for the party the gate exists to reject.**

## 5. Corrections to the previous attempt at this path

1. **"No peer report records a `C1=PASS` obtained this round" is now false.** At 51 reports,
   `R59Executor01` §2, `R59Executor03` § Runs C, `R59Executor05` §5, `R59Executor02` §3 and
   `R59MutationTester63` all print `C1=PASS` (quoted above). The correct distinction is not "nobody
   reached PASS" but "nobody reached PASS honestly on the frozen bytes".
2. **"0 of them mention `claims.md`" needs precision.** `RAN` census over the 66 dispatch items:
   `claims.md` in 0/66 items, but present once in `taskCall.context`; the spec names it 67 times and
   `c1-count` 0 times. The conclusion (wave dispatched against a missing file) stands; the count is
   now exact.
3. **Stale counts, not wrong at their time.** `w1.ready.partial` 414 B → 950 B → 1,500 B; retry
   pairs 5 → 10 → 11; reports 37 → 48 → 51; §1 of the prior attempt captured the 15:17–15:19 slice.
4. **Confirmed unchanged:** receipt identity (`2c9bbe54…`), candidate/control digest equality
   (`1ed2650a…`), capture pins (`6063a3af…`, `2c0140bc…`), empty `git ls-tree` for round 59, absent
   dispatch marker and results file, `DENIED=0/0`, `REFUSE=0/7`, and the C2 offset contradiction.

## 6. Draft — `## Gate` (adoptable text for `corpus/lessons/round-59.md`; slots in `<…>`)

> ## Gate
>
> ### Freeze status — no round-59 claim was frozen
>
> - `corpus/evidence/round59/claims.md` does not exist; at HEAD `af8c0a460d087cbfb8245fb9326608783ccc510b`
>   `git ls-tree -r --name-only HEAD corpus/evidence/round59` prints nothing and `git status` shows
>   `?? corpus/evidence/round59/`. There is no round-59 counter and no freeze commit, while
>   `.ufo/waves/round-59/w1.ready` (15:12:15) preceded the only control receipt (15:14:30) and
>   `w1-spec.json` was written at 15:14:46, after the wave was declared ready. The wave context names
>   the missing path (spec: 67 mentions); the 66 dispatched items do not (0/66, §5.2).
> - `.ufo/waves/round-59/w1.ready.dispatched` and `w1-results.json` are absent while 51 seat reports
>   exist; per criterion 99 (`corpus/QUALITY.md:941`) the wave is reported **not dispatched** as of
>   this Gate, and no claim may cite `w1.ready` or the roster as dispatch evidence.
> - Therefore **no claim-level verdict exists for round 59**. This Gate records counter calibration
>   against inherited round-58 bytes; it adopts no round-58 claim as round 59's and rewrites no frozen
>   byte.
>
> ### Positive verdict-path calibration (the milestone) — answer: inverted, then non-discriminating
>
> - **Unreachable for honest builders.** `c1-count.py:391` searches `=PASS` over refusal legs that
>   `:150-161` emit as `=pass(refused)` (`PASS` at `:51`); `verdict` (`:394`) is therefore a constant
>   `FAIL` for every honest candidate. Measured: a maximal honest builder passes all 11 legs and still
>   prints `REFUSE=0/7 C1=FAIL` (`PEER` `R59Executor01` §1). Unit witness this seat ran:
>   `"=pass" in "FIFO_TXT=pass(refused)"` → `True`, `"=PASS"` → `False`.
> - **Reachable by forgery.** The same substring test reads whole leg lines, and `:150-161` embeds
>   builder stderr (`{err[:160]!r}`); a builder that prints `=PASS` to stderr reaches
>   `REFUSE=7/7 C1=PASS`, exit 0, while every hazard leg is printed `fail(...)` and the symlinked
>   `--out` is written through (`PEER` `R59Executor03` § Runs C; `:233-236` appends the marker to, rather
>   than failing, the leg).
> - **A one-token repair is necessary but not sufficient.** With `:391`/`:399` aligned to `=pass`, the
>   honest builder reaches `C1=PASS` (`PEER` `R59Executor01` §2, `R59Executor05` §5) — and so does a
>   zero-check forge (`PEER` `R59Executor02` §3) and a symlink write-through mutant
>   (`R59Executor01` F3). The repaired gate is *satisfiable but non-discriminating*, and its summary
>   line still prints `REFUSE=0/7` on a `PASS` verdict (`R59Executor01` F2).
> - **Controls.** `corpus/evidence/round59/controls/` holds one file, `c1-before.txt`
>   (sha256 `2c9bbe54…aebfe`, byte-identical to round 58's before-receipt, no provenance header).
>   `denied_pass = (denied == total) if total else True` (`:393`) accepts the printed `DENIED=0/0`.
>   The candidate `tools/build-spans.py` is byte-identical to the pinned control
>   `corpus/evidence/round58/controls/build-spans-r55.py` (`1ed2650a…`), so `BEFORE_FOREIGN=deleted`
>   compares the candidate with itself. Round 59 supplied **no** positive, deny or fixture control.
> - **Hazard legs are heterogeneous.** In the accepted run at
>   `/fast/scratch/hyaku/chousa-r59/predata/c1-real/`: `out-link` → `realdir`, and `realdir/` holds
>   `spans.tsv` (581 B) plus `spans/` (symlink write-through); `cache3/f4088c6d…txt` is a FIFO
>   (`prw-r--r--`); `cache4/a172f0…txt` is a symlink to `/dev/zero`; `out-many/` holds **100,001**
>   span files and an **18,389,131 B** manifest (**413 MiB** total). FIFO and device legs are safe only
>   because `Path.is_file()` is false for those types (`tools/build-spans.py:74,85,96`), not because a
>   named guard fired; `FAT_RAW` is refused by the OLE parser (`ole-malformed: sector shift 0`) before
>   any size check. The builder has no `st_size`/row cap.
>
> ### C2 / depth — offline chain intact, inherited predicate unsatisfiable
>
> - No live fetch; L0 `8d77e6c1` remains open. S101 re-opened from lane bytes only: raw
>   `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` sha256 `6063a3af…ddf3`, defined form by
>   `tools/capture-text.py` (`2c0140bc…2573`). Admit as **source evidence only**, exactly as the
>   round-58 verifier spot-check independently agreed; no `knowledge/` entry is admitted and
>   `corpus/knowledge/carrier-alphabet-china-r58.md` does not exist.
> - Reject present status/legal force/current use of GB3469: no fetch authority, no current
>   instrument. Flip = operator-approved research window plus a located current authority.
> - The inherited C2 predicate is unsatisfiable as frozen: `tools/build-spans.py:43,142` writes
>   `start = max(0, off - CONTEXT)` (`CONTEXT = 80`) into the `offset` column (docstring `:16`), while
>   `corpus/evidence/round58/c2-count.py:101` requires `occurrences[0] == off` (`CAPTURE_BIND`) and
>   `:129` requires a byte-identical rebuild. One column cannot satisfy both. A future depth claim
>   must pick one invariant, re-freeze a counter, and re-pin the builder digest.
>
> ### SOURCES changes
>
> - Rows 133 → 133; added by tier A/B/C 0/0/0; census `exit=0` with the five unchanged W04
>   duplicate-URL warnings (S051, S053, S073, S074, S075):
>   `corpus/evidence/round59/census-start.txt`; count command
>   `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`.
> - S101 `used-by` unchanged this round; status `mined`, recheck `180d`. <slot: update only if a
>   round-59 entry is admitted>
> - Frontier advanced: none as admitted knowledge. Assimilation: none.
>
> ### Outside spot-check
>
> - Record, do not re-claim: `corpus/lessons/round-58-verifier-spotcheck.md` is a non-author closure
>   artifact whose discernment table agreed with both lane decisions (S101 admitted as source
>   evidence only: quote `并以[文献类型标识/载体类型标识]表示`; GB3469 present-day status rejected).
>   Its routed defect "freeze must-pass positive controls before wave data" is **not** satisfied this
>   round — round 59 dispatched with no claims file and no positive control (§above).
> - No outside sample exists for round 59; every W1 seat is same-lane evidence. Calibration gain
>   claimed: none.

## 7. Draft — `## Mistakes` (adoptable rows; each falsified by bytes above)

> 1. **unfrozen — the wave ran against a claim file that does not exist.** · Evidence: the wave
>    context names `corpus/evidence/round59/claims.md` (the spec repeats it 67 times; the 66
>    dispatched items do not, 0/66); the file is absent at
>    15:20–15:22; `git ls-tree -r --name-only HEAD corpus/evidence/round59` is empty and the evidence
>    directory is untracked at HEAD `af8c0a46`; `w1.ready` (15:12:15) precedes the only control
>    receipt (15:14:30); `w1.ready.dispatched` and `w1-results.json` are absent with 51 reports filed.
>    · Captured-by: criteria 99 and 115 (`corpus/QUALITY.md:941,974`). · Fix: land claims, positive
>    control, deny control and counter digest in one freeze commit, then mark dispatch; report marker
>    truth, not roster truth. · Shown able to fail: absent file, empty `ls-tree`, empty marker set.
>
> 2. **inverted token — the positive verdict is unreachable for honest builders.** · Evidence:
>    `PASS="pass"` (:51) and `=PASS(refused)` (:160) against `ref_pass`/`REFUSE` searching `=PASS`
>    (:391,:399); unit witness `"=pass" in "FIFO_TXT=pass(refused)"` → `True`, `"=PASS"` → `False`;
>    an honest maximal builder passes 11/11 legs and prints `REFUSE=0/7 C1=FAIL` (PEER
>    `R59Executor01` §1). · Captured-by: criterion 115 first sentence. · Fix: derive emitter and
>    aggregate from one token constant; a new counter path with a new digest. · Shown able to fail:
>    the constant-False `ref_pass` under a fully passing leg set.
>
> 3. **forgeable — the positive verdict is reachable by printing the token.** · Evidence: `ref_pass`
>    scans whole leg lines and `expect_refuse` embeds `{err[:160]!r}` (:150–161), so a builder whose
>    stderr contains `=PASS` yields `REFUSE=7/7 C1=PASS` while every hazard leg prints `fail(...)`
>    (PEER `R59Executor03` § Runs C, with `realdir/spans.tsv` (28 B) written through the symlink). ·
>    Captured-by: criterion 86's positive-control principle, inverted: the control must be able to
>    show the measured class and must not be able to fake the verdict. · Fix: parse structured leg
>    records (or compare exit codes and named predicates), never scan free text that embeds the
>    subject's stderr. · Shown able to fail: the run C receipt with seven `fail(...)` lines and
>    `C1=PASS`.
>
> 4. **non-discriminating after repair — the token fix credits a zero-check forge.** · Evidence: with
>    only :391/:399 aligned, `C1=PASS` is reached by an honest builder (PEER `R59Executor01` §2,
>    `R59Executor05` §5) and by a name-keyed forge performing no check (`REFUSE=7/7 C1=PASS`, PEER
>    `R59Executor02` §3); a symlink write-through mutant still reaches `C1=PASS` (`R59Executor01` F3),
>    and the summary line still prints `REFUSE=0/7` on a PASS verdict (F2). · Captured-by: criterion
>    115's reachability requirement, extended: reachability without discrimination is a second
>    vacuity. · Fix: the freeze pairs a must-pass positive control with a **must-fail near-miss**
>    control that satisfies the same textual vocabulary but violates one guard; require the pair to
>    separate. · Shown able to fail: the forge PASS and the write-through PASS.
>
> 5. **vacuous denial gate — an empty control set passes, and round 59 supplied no fixtures.** ·
>    Evidence: `denied_pass = (denied == total) if total else True` (:393); receipt prints
>    `DENIED=0/0`; `ls corpus/evidence/round59/controls/` → only `c1-before.txt`, while round 58's
>    directory holds `REFUSEALL.py` and `build-spans-r55.py`. · Captured-by: criterion 115, which
>    forbids treating a deny-only set as reachability evidence; round 59 is weaker than deny-only. ·
>    Fix: require `DENIED>=1` and a `CONTROL_*` line; fail the counter when `--controls` is omitted. ·
>    Shown able to fail: the literal `DENIED=0/0` with `denied_pass` true.
>
> 6. **non-discriminating — the "can fail" control is the candidate.** · Evidence:
>    `sha256sum tools/build-spans.py corpus/evidence/round58/controls/build-spans-r55.py` → both
>    `1ed2650a…bf6`; `integrity` (:392) requires `BEFORE_FOREIGN=deleted` from that pinned file, so
>    the leg compares the candidate with its own bytes. · Captured-by: criterion 86. · Fix: print
>    candidate and control digests and fail on equality; land a changed builder before any C1
>    re-claim. · Shown able to fail: digest equality plus the verbatim `BEFORE_FOREIGN=deleted`.
>
> 7. **provenance — an unheaded receipt, a copied receipt, and two conflicting peer citations.** ·
>    Evidence: `c1-before.txt` opens `EMPTY_OK=pass` (no command/digest/builder/time/exit) and is
>    byte-identical to round 58's (`2c9bbe54…`); `R59Critic59.md:5` states `git ls-tree` "lists only
>    round59 `census-start.txt` and `controls/c1-before.txt`" while this seat's `git ls-tree -r HEAD
>    corpus/evidence/round59` prints nothing; `R59Scout39.md:5` reports the receipt as "0 bytes" while
>    `stat` gives 958 B at 15:14:30.645, and that report's own mtime is 15:14:43 — a write race would
>    require the read to fall before the receipt's final write, which is not excluded but not proven.
>    · Captured-by: criterion 95's re-derivability principle. · Fix:
>    every receipt carries a header (command, counter sha256, builder sha256, input digests,
>    timestamp, exit); every report quoting a file cites size+mtime+digest and the exact HEAD for any
>    `git` result. · Shown able to fail: the missing header, the empty `ls-tree`, the 0-B/958-B
>    conflict.
>
> 8. **spot-check intake, carried without change.** Round-58 verifier spot-check's routed defects:
>    (a) positive-control freeze — **not** satisfied by round 59 (§6); (b) record the external
>    admit/reject pair and its quote — done in §6 Gate; (c) dispatch prompt/handoff clarity —
>    operator-side, with new evidence here: 0/66 dispatch items name the frozen file their context
>    requires, 0/66 own the milestone's *build* verb (`build`/`author`/`patch` = 0; `inspect` 16,
>    `run` 16, `mutation-test` 5, `assess` 14, `read` 24, `draft` 12), the spec postdates the
>    dispatch, and 11 retry suffixes appear inside one wave. Also carried: five W04 URL warnings
>    (pre-existing, `exit=0`) and open fetch-scope question `8d77e6c1`.

## 8. Draft — report-body verdict wording (use only after a freeze exists)

> Claims froze at `<freeze-commit>` against base `<base-commit>`; pre-data receipts are
> `corpus/evidence/round59/controls/c1-before.txt` and `c2-before.txt`, each header-named with
> command, counter sha256, builder sha256, input digests, timestamp and exit. Positive controls
> `<c1-positive>` reach the declared final token by honest behaviour and exit 0 in the same commit;
> near-miss controls `<c1-near-miss>` satisfy the same vocabulary but must not reach it; deny controls
> `<deny-…>` are denied with `DENIED>=1`.
>
> | claim / axis | before → after | counting command / evidence | verdict |
> |---|---|---|---|
> | C1 operability (historical 3/10) | `C1=FAIL, REFUSE=0/7` → `<after>` | `python3 corpus/evidence/round59/c1-count.py --builder <b> --controls <dir> --work <fresh>` | `<provable>` only with a positive receipt + a near-miss fail + `DENIED>=1`; else **unprovable — clause `<x>` unreachable** |
> | C2 depth (`<S-id>`) | `C2=FAIL (<missing>)` → `<after>` | `python3 corpus/evidence/round59/c2-count.py --root <copy> --work <fresh>` | `<provable/unprovable — offset-vs-rebuild clause>` |
>
> No score was changed or invented. Round 59 records **no numeric axis gain**. The gate below is the
> adoptable verdict for the round as it actually ran (nothing frozen):
>
> | axis | round-59 verdict | evidence |
> |---|---|---|
> | operability | `unprovable` — no claim; inherited counter's positive path inverted, then non-discriminating after repair | §3, §4 |
> | depth | `unprovable` — no claim; C2 offset clauses mutually exclusive; S101 re-opened offline as source evidence only | §6 |
> | coverage | `unchanged` — 133 rows, five W04 | census-start |
> | freshness | `unchanged` — no fetch; `8d77e6c1` open | §6 |
> | calibration | `unchanged` — no positive/negative control, no new outside sample; counter defects localised | §6, §7 rows 2–6 |
> | adjacency | `unchanged` | — |

## 9. Not run / not claimed by this seat

- This seat did **not** run `c1-count.py` or `c2-count.py`; it read their bytes, quoted the round-59
  receipt, ran a two-string unit witness of the token comparison, and attributed peer measurements
  by path. No `C1=` or `C2=` verdict is claimed by me.
- The 100,001-file / 18,389,131 B / 413 MiB side-effect figures are `RAN` (`find`, `stat`, `du`) over
  `predata/c1-real/out-many`, an artifact produced at 15:14 by another seat's pre-data run; I did not
  produce it and did not re-run the counter that produced it.
- Peer receipts in §4 were read, not reproduced. `R59Executor05`'s diagnostic digest
  (`21dae5d3…eeba`) and `R59Executor03`'s upperfix digest (`6b6000ed…3a46`) are quoted as reported.
- No lane file, claim, counter, control, builder, `SCORECARD.md`, `QUALITY.md`, registry or frozen
  artifact was written or edited. Only read-only `git` inspection (`rev-parse`, `status`, `ls-tree`);
  no index or working-copy write.
- No fetch, no install, no pacman transaction. Scratch `/fast/scratch/hyaku/chousa-r59/R59Scribe23/`
  held only the unit-witness script and was removed before yield.

## Artifacts

- Report (this file, relative to lane root): `.ufo/waves/round-59/w1/R59Scribe23.md`
- Read: `corpus/evidence/round58/{claims.md,c1-count.py,c2-count.py,controls/*}`,
  `corpus/evidence/round59/{census-start.txt,controls/c1-before.txt}`,
  `corpus/lessons/round-58.md`, `corpus/lessons/round-58-verifier-spotcheck.md`,
  `corpus/QUALITY.md:915,941,974`, `corpus/SOURCES.md:111`, `SCORECARD.md`,
  `tools/build-spans.py`, `corpus/evidence/round58/s101-open.txt`
- Read (peers, not re-run): `.ufo/waves/round-59/w1/{R59Executor01,R59Executor02,R59Executor03,R59Executor05,R59MutationTester63,R59Critic59,R59Scout39}.md`
- Inspected (produced by others): `/fast/scratch/hyaku/chousa-r59/predata/c1-real/`
- Wave artifacts: `.ufo/waves/round-59/{w1-dispatch.json,w1-spec.json,w1.ready,w1.ready.partial}`, `w1/*.md` (51 at read time)

Report trailer: `.ufo/waves/round-59/w1/R59Scribe23.md`
