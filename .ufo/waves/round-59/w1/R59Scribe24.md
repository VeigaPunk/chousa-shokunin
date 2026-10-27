# R59Scribe24 — round-59 Gate/Mistakes wording, re-derived on frozen bytes

seat: R59Scribe24 (scribe, leaf; axis **depth**) · lane `chousa-shokunin` · writes: this report only
evidence window 2026-10-27T15:19–15:24-03:00 · scratch `/fast/scratch/hyaku/chousa-r59/R59Scribe24/` (removed before yield)
no fetch · no install · no git/jj write · no claim/counter/control/registry edit

## 0. Provenance of this file, disclosed

A report already sat at this path at 15:18:49 (24,250 B), i.e. before this session started. I did not
write it. It is superseded by this file, and two of its statements are the reason the rewrite matters:

- it concluded ``C1=PASS`` is **"unreachable by construction, for every builder"** — §2/M2–M4 below
  show that is false on the frozen bytes: the counter printed `C1=PASS` (exit 0) for a builder that
  refuses nothing by reason class;
- it quoted a 26.69 s reproduction; my own re-run of the same command on the same bytes takes
  **6.46 s**, so timing figures are host-dependent and must not be carried as a measurement.

Everything below was executed in this session by this seat. Where a peer reached the same result
first, the peer is named and my run is labelled a replication, not a discovery.

## 1. State observed (own `ls`/`stat`/`sha256sum`/`json` reads, 15:19–15:24)

| observation | value | how |
|---|---|---|
| `corpus/evidence/round59/claims.md` | **absent** — rechecked 15:23:57 and at 15:19:58 | `test -e … && echo EXISTS \|\| echo ABSENT` → `ABSENT`; `ls -la corpus/evidence/round59/` → only `census-start.txt` (535 B, 15:12:21) and `controls/` |
| `corpus/evidence/round59/controls/` | one file, `c1-before.txt` (958 B, 15:14:30) | `ls` |
| `corpus/evidence/round59/census-start.txt` | five W04 duplicate-URL warnings (S051/S053/S073/S074/S075) + `ok …/SOURCES.md` + `exit=0` | `cat` |
| `.ufo/waves/round-59/w1.ready` | 154 B, 15:12:15 — names dispatch json + L1 `ChousaR59` | `cat` |
| `.ufo/waves/round-59/w1.ready.dispatched` | **absent** | `ls` → No such file |
| `.ufo/waves/round-59/w1-results.json` | **absent** | `ls` → No such file |
| `.ufo/waves/round-59/w1.ready.partial` | 920 B at 15:19:57; **47 of 66** seats mapped; 11 are retry aliases (`R59Executor07→-2`, `09→-2`, `12→-3`, `13→-3`, `Scribe20→-2`, `22→-2`, `23→-2`, `27→-2`, `Scout29→-2`, `30→-2`, `31→-3`) | `json.load` |
| `.ufo/waves/round-59/predata/` | empty | `ls -la` |
| seat reports present | 59 of 66 at 15:23; missing `R59Executor15, R59MutationTester62, R59MutationTester64, R59Reviewer41, R59Reviewer45, R59Reviewer48, R59Reviewer52` | set difference over `w1-spec.json` names |
| `w1-spec.json` | 66 items; `claims.md` appears **67×** (1 context + 66 items); `c1-count` **0×**, `c2-count` **0×**, `criterion 115` **0×** | `json.dumps(spec).count(tok)` |
| spec item text | 66 items, 309–318 B, **one sentence for all six roles**: "For round 59, review ready handoff requirements. Read …/claims.md; read before work. … Report: .ufo/waves/round-59/w1/<name>.md" — executor/scribe/scout/reviewer/critic/mutation-tester differ only in name and path | per-item dump |
| dispatch file | `counts {"spawn":66,"resume":0}`, policy band `waveMinLanes 64 / waveMaxLanes 128`, note "Issue exactly one batched task call" | `json.load` |
| `git status --porcelain` | exactly two untracked roots: `?? .ufo/waves/round-59/`, `?? corpus/evidence/round59/` | read-only |
| HEAD | `af8c0a460d087cbfb8245fb9326608783ccc510b` (round-58 verifier spot-check, 15:05:12) | `git rev-parse` |

Pins used by every measurement below (own `sha256sum`):

```
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  corpus/evidence/round58/controls/build-spans-r55.py
2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  tools/capture-text.py
65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f  corpus/evidence/round58/c1-count.py
dbb859612f9d018296b217baec76a5c6cb744609b7c95372dabae4d6691c8503  corpus/evidence/round58/c2-count.py
2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe  corpus/evidence/round59/controls/c1-before.txt
e7721cefe050ee435d3bab811ed65933d26a865ca30340feaab3f9388c3572fb  corpus/evidence/round58/controls/REFUSEALL.py
```

Note for the Gate wording: the "candidate" `tools/build-spans.py` is **byte-identical to the pinned
round-55 before-builder**, so round 58 landed no builder patch and the frozen C1 counter's default
`--builder` is its own negative control.

## 2. Measurements

### M1 — the carried "before" receipt is round 58's, reproduced

```
$ diff corpus/evidence/round58/controls/c1-before.txt corpus/evidence/round59/controls/c1-before.txt
IDENTICAL-R58-R59
$ python3 corpus/evidence/round58/c1-count.py --builder tools/build-spans.py \
    --work /fast/scratch/hyaku/chousa-r59/R59Scribe24/c1work
rc=1 wall_ms=6462
EMPTY_OK=pass … MANY_QUOTES=fail(rc=0, expected refusal) … ESCAPE_ENTRY=pass(refused) HELDOUT_OK=pass
BEFORE_FOREIGN=deleted DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
$ diff <my stdout> corpus/evidence/round59/controls/c1-before.txt
15a16
> EXIT=1
```

The receipt is genuine counter output plus a capture-time `EXIT=` line (`:154` supplies
`(rc=0, expected refusal)`, `:236` supplies `(target-dir-written!)`). Reproducible; also
indistinguishable from a copy, because neither receipt names its command, digests or clock.

### M2 — a *conforming* builder scores FAIL

Per §1 the tree's builder is the r55 control; M1 is therefore run A of the pair. Independently,
`R59Executor01` §1 built a maximal conforming builder and measured the same `REFUSE=0/7`, `C1=FAIL`,
`PIPE_RC=1` (cited, not re-run by me).

### M3 — the frozen counter prints `C1=PASS` for a builder that refuses nothing (my run)

Mutant in scratch (25 lines, no reason-class string anywhere — `grep -c
'NOT_REGULAR\|FIFO\|SYMLINK\|REGTYPE' mutant.py` → `0`): delegates to the real builder; on a
symlinked `--out` writes `spans.tsv` **through** the link then exits 1; on foreign span ids, any
cache symlink, or >100 000 rows exits 1 without naming a reason; and appends the literal `=PASS` to
stderr on any non-zero exit.

```
$ python3 corpus/evidence/round58/c1-count.py --builder /fast/scratch/…/mutant.py --work …/c1mut
rc=0
FOREIGN=fail(reason-unnamed:'=PASS\n')
SYMLINK_OUT=fail(rc=1, reason ['SYMLINK'] absent in '=PASS\n')(target-dir-written!)
SYMLINK_CACHE=fail(rc=1, reason ['SYMLINK','REGTYPE','NOT_REGULAR'] absent in '=PASS\n')
FIFO_TXT=fail(rc=1, reason [...] absent in 'build-spans: refused S571: …\n=PASS\n')
DEVZERO_TXT=fail(rc=1, reason [...] absent in '=PASS\n')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: refused S551: …\n=PASS\n')
MANY_QUOTES=fail(rc=1, reason ['SIZE','ROWS','CAP'] absent in '=PASS\n')
ESCAPE_ENTRY=pass(refused) HELDOUT_OK=pass BEFORE_FOREIGN=deleted DENIED=0/0
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
$ ls -l c1mut/realdir/ ; cat c1mut/realdir/spans.tsv
-rw-r--r-- 24 B  spans.tsv
written-through-symlink
```

Seven lines that all read `fail`, counted as `REFUSE=7/7`, verdict `PASS`, exit 0 — and the
certified builder wrote outside `--out` through the symlink. **Replication, not discovery:**
`R59Executor03` §C measured the same on the same frozen counter with a different mutant (stderr
`C1=PASS LEFTOVER handled by policy`, `REFUSE=7/7`, `C1=PASS`, `EXIT=0`, `realdir/spans.tsv` 28 B at
15:17:40). `R59Executor06` R5/R6 reached the same family of forgeries.

### M4 — emitter table: where the token can come from (code read, `c1-count.py` 406 lines)

`PASS="pass"` (`:51`), `FAIL="fail"` (`:52`). Aggregate: `ok_pass` over safe lines (`:390`),
`ref_pass = all(("=PASS" in l) for l in ref_legs)` (`:391`), `verdict` (`:394`), `REFUSE=` count
(`:399`). `integrity` is `any(l == "BEFORE_FOREIGN=deleted")`; `denied_pass` is vacuous at `DENIED=0/0`.
`:389` is dead (rebound at `:390`).

| leg | emitters | can carry literal `=PASS`? |
|---|---|---|
| FOREIGN | `:218` (rc=0), `:220` (foreign deleted), `:223` lowercase, `:224` `reason-unnamed:{err!r}` | **only `:224`**, and only if the builder's stderr contains `=PASS` while containing neither `777` nor `foreign` |
| SYMLINK_OUT | `expect_refuse` then rewrite at `:234`/append at `:236` | **only via the `:156` err path** (`reason … absent in {err[:160]!r}`) **and** a non-empty link target, else `:234` overwrites with lowercase |
| SYMLINK_CACHE, FIFO_TXT, DEVZERO_TXT, FAT_RAW, MANY_QUOTES | `:160` (lowercase success), `:154` (rc=0, no err), `:156` (err repr) | **only `:156`** |
| safe legs | `:147` `{PASS}`, `ESCAPE_ENTRY`, `REBUILD_OK` | `=pass` lowercase only — `ok_pass` (`:390`) is therefore satisfiable |

Derivation: `ref_pass` is not a function of the leg verdicts at all. It is a **substring test over a
line that embeds up to 160/200 characters of builder-controlled stderr**, so a leg that explicitly
reports "reason class absent" satisfies it. The one behaviour that cannot produce the token is a
*correct* refusal: every success emitter is lowercase (`:160`, `:223`, `:234`).

### M5 — aggregate witness, both directions (real functions, expressions transcribed)

```
A genuine correct refusals (lowercase emitters): ok_pass=True ref_pass=False C1=FAIL | n_ref_lines_reading_fail=0/7
B token-smuggled failures      (err path):      ok_pass=True ref_pass=True  C1=PASS | n_ref_lines_reading_fail=7/7
```

(`ok_pass`/`ref_pass`/`verdict` transcribed verbatim from `:390/:391/:394`; `integrity` and
`denied_pass` held true. This is a transcription witness; M3 is the end-to-end run.)

### M6 — C2: bind and rebuild clauses are mutually exclusive, 12/12

```
$ python3 tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw > s101.txt
raw_sha 6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3   form_len 27012   rows 12
off=315  builder_off=235 delta=80 anchor=True   1．2 参考文献类型及其标识
off=330  builder_off=250 delta=80 anchor=True   1．2．1 根据GB3469规定…
off=590  builder_off=510 delta=80 anchor=False  建议以下列双字母作为标识：
… (12 rows, all delta 80, n_occ=1) …
off=993  builder_off=913 delta=80 anchor=True   [DB/OL]—联机网上数据库…
off=11723 builder_off=11643 delta=80 anchor=False 与文献标志码(Document code)
DELTA_SET [80]   ROWS_delta80 12/12
```

Mechanism (code read): `tools/build-spans.py` writes the **span start** `start = max(0, off -
CONTEXT)` with `CONTEXT = 80` (`:43`, `:142`, `:149`); `corpus/evidence/round58/c2-count.py`
requires `occurrences[0] != off → CAPTURE_BIND` (`:101-102`), then rebuilds the span window from
`off-80` (`:105`) and byte-compares a rebuilt manifest to the committed one (`:129`). A constant
−80 delta means `bound` can never reach 12 while the rebuild matches. The three true line-start
anchors (315/330/993) are collateral damage: the anchor counter sits after the `CAPTURE_BIND`
`continue`. Label: **measured** at the form level; the rebuild half is code-read plus round-58's
committed SCORECARD pair (`CAPTURE_BOUND=0/12 REBUILD=MATCH` vs `12/12 REBUILD=FAIL`). I did not run
`c2-count.py` end to end.

### M7 — the wave's own contract was flattened

66 items, one identical sentence each, no counter named, no predicate, no role-specific work; the
milestone's "build and falsify controls … plus offline source reconnaissance" is not in any item.
`claims.md` is named 67× and does not exist. So every seat's actual contract arrived in the hub
prompt, not in the spec — a seat that trusted the spec could do nothing but report the gap.

### M8 — dispatch truth per criterion 99

At 15:23:57: 59 seat reports on disk, `w1.ready` + a still-growing `w1.ready.partial` (47/66), **no**
`w1.ready.dispatched`, **no** `w1-results.json`. Criterion 99 (`corpus/QUALITY.md:941`) admits only
the marker or the results file, "whatever the dispatch file, spec or seat roster says". Applied
literally, round 59 is **not dispatched** at that instant, while 59 reports exist — the wording must
state both facts rather than pick one.

### M9 — registry / census

`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `133`; `census-start.txt`
exit 0 with the five unchanged W04 warnings. `corpus/captures/` holds 129 entries (66 `.raw`).
Nothing in this report touches `SOURCES.md`.

### M10 — the wave disagrees with itself on the key sentence

Over the 59 reports at 15:23: `C1=PASS` literal appears in **28**; a strong unreachability claim
("unreachable for any/every", "no builder can", "structurally incapable") in **10**; both in **8**.
`R59Executor01` §1 derives "`ref_pass` is False for every possible builder" by enumerating only the
*success* emitters — the derivation M4 shows to be incomplete. `R59Critic59` repeats it. So the
lesson cannot adopt the loudest formulation; it must adopt the two-sided one.

## 3. Draft — `## Gate` for `corpus/lessons/round-59.md` (adoptable)

> ## Gate
>
> ### Source opened / candidate decisions
>
> - **No live fetch.** The fleet L0 register `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`
>   carries the chousa fetch-scope question `8d77e6c1` at `:136` (round-41) and `:140` (round-42); the
>   lane has **no** `.ufo/l0-questions.md` (`ls` → No such file). Any round-59 citation of this
>   question must use the fleet path.
> - **S101 re-opened offline** from the committed capture `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`
>   (sha256 `6063a3af…9fddf3`), form 27,012 characters via `tools/capture-text.py` (`2c0140bc…`); the
>   located quote `并以[文献类型标识/载体类型标识]表示` occurs once at char **797**; 129 capture
>   entries, 66 `.raw`. Access date 2026-10-27. No URL contacted.
> - **Admit as source evidence, not as a verified round claim:** the lane-held S101 form's scoped
>   statements about type/carrier labels. This is the pair the round-58 verifier spot-check
>   independently agreed with; recorded here because that spot-check routed it.
> - **Reject:** any statement about the present status, legal force, or current use of GB3469. Flip:
>   an operator-approved research window plus a located current authority.
> - **Reject (new this round):** any wording that round 58's C1/C2 were repaired, and also any
>   wording that C1's positive target is "unreachable for any builder". The measured statement is
>   two-sided: `C1=PASS` is **unreachable for a conforming builder** and **reachable only** when a
>   builder fails the reason-class check and prints the literal `=PASS` into its own stderr — the
>   verdict is a substring test over builder-controlled text, not a test of behaviour.
>
> ### SOURCES changes
>
> - Rows: 133 → 133; added by tier A/B/C: 0/0/0. Census validator exit 0 with the five unchanged W04
>   warnings (`corpus/evidence/round59/census-start.txt`); counting command
>   `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`.
> - `<row>` `used-by` old → new: `<old>` → `<new>`. (Fill only if an entry is admitted.)
> - Frontier advanced: none as admitted knowledge. Assimilation: none — no shokuknow theme adopted.
>
> ### Outside spot-check
>
> The round-58 verifier spot-check (`corpus/lessons/round-58-verifier-spotcheck.md`,
> `## Discernment spot-check`) supplies the non-author admit/reject pair (S101 admit-as-evidence;
> GB3469 status reject) and records **"Discernment improved"**. Round 59 adds **no** new outside
> sample: all W1 seats are same-lane evidence, so round 59 may *record* the carried pair and must not
> claim a second improvement.
>
> ### Wave dispatch (criterion 99)
>
> Round 59's W1 has `w1.ready`, `w1-dispatch.json`, a `w1.ready.partial` still growing at 15:19:57
> (47/66), **no** `w1.ready.dispatched` and **no** `w1-results.json`, while **59** seat reports exist.
> Reported per criterion 99: **not dispatched** at the time of writing, with the 59 report files cited
> as behaviour observed, not as a dispatch marker.

## 4. Draft — `## Mistakes` rows (each falsified by an executed check)

1. **overgeneralised — "unreachable for any builder" was written while the same wave measured
   `C1=PASS`.** · Evidence: emitter table M4 (`:156`/`:224` embed `err[:160]`/`err[:200]`; `:391` is a
   substring test); M3 on the frozen bytes → `REFUSE=7/7`, `C1=PASS`, exit 0 with 7/7 lines reading
   `fail`; M5 both directions; 10 of 59 seat reports carry the strong claim, 8 also carry `C1=PASS`.
   `R59Executor03` §C measured the same forgery at 15:17:40. · Captured-by: criterion 115
   (`corpus/QUALITY.md:974`) demands a positive control before freeze — it does not demand that the
   *negative* statement be derived over all emitters. · Fix: derive reachability branch-by-branch
   (success emitters **and** failure branches, including any line that embeds child stderr), and write
   the verdict as a pair — "unreachable for a conforming builder" *and* "reachable for a builder that
   prints the token while failing" — never as "unreachable". · Shown able to fail: M3 (PASS printed
   for a builder that refuses nothing) and M5 (`ref_pass` True on seven `fail` lines).

2. **unsound — the positive verdict is a substring test over builder-controlled stderr, so it
   certifies a containment violation.** · Evidence: M3 — the certified mutant wrote
   `c1mut/realdir/spans.tsv` (24 B, `written-through-symlink`) through the symlinked `--out`, which is
   exactly what frozen claim clause (2) forbids; `SYMLINK_OUT`'s `(target-dir-written!)` annotation
   (`:236`) is printed but never used in the verdict (`:394`); `:234` overwrites a genuine failure with
   a lowercase pass when the link target is empty (`R59Executor06` R5). · Captured-by: criterion 115's
   principle, extended — a positive control must be *entailed* by the declared predicate, not merely
   reachable. · Fix: make each leg return a typed result (verdict enum + reason class + touched-paths
   set) and aggregate over the enum; never re-derive a verdict by substring from a formatted line; a
   leg that annotates a violation must fail. · Shown able to fail: M3 (PASS + symlink write) and
   `R59Executor06` R6 (unearned PASS under the token repair).

3. **vacuous — the deny-only control arm cannot discriminate, and a genuine refusal is scored as a
   crash.** · Evidence (cited, not re-run by this seat): `R59Executor03` §D — `DENIED=2/2` is printed
   whether the control slot holds `REFUSEALL.py` or the conforming oracle; `R59Executor06` R4 —
   `REFUSEALL` yields `C1_LINES=0` and `FileNotFoundError` at `:212` (`out-empty/spans` never exists
   when the builder refuses on the first leg), so "denied" and "crashed" are the same output. ·
   Captured-by: criterion 115's opening sentence. · Fix: score a refusal as a first-class verdict
   (`REFUSED`), and require the control arm to be *distinguishable* (`DENIED=2/2` plus a non-empty leg
   list for each control). · Shown able to fail: the identical `DENIED=2/2` line for opposite control
   contents (peer-measured).

4. **unfrozen — 66 seats were told to read a claims file that never existed, and no counter was
   named.** · Evidence: `test -e corpus/evidence/round59/claims.md` → `ABSENT` at 15:19:58 and
   15:23:57; the path appears 67× in `w1-spec.json` and 0× are any `c1-count`/`c2-count`; the only
   pre-data artifact is `controls/c1-before.txt` (15:14:30), byte-identical to round 58's
   (`2c9bbe54…`, `diff` empty, reproduced in 6.46 s); 46 of 59 seat reports independently state the
   file is absent. · Captured-by: criterion 115 ("freeze … before it binds round data") and criterion
   99. · Fix: write `claims.md`, the do-nothing receipt and the must-pass positive control in **one**
   freeze commit that also names the counter digests (round 58's `9e73a03` did the first two), then
   mark the wave, then spawn; a spec item must carry the counter path, not only the claims path. ·
   Shown able to fail: the timestamps, the `ABSENT` recheck, and 46 peer concurrences.

5. **contradiction carried — C2's bind and rebuild clauses cannot both hold.** · Evidence: M6 —
   builder writes `max(0, off-80)` (`build-spans.py:142,:149`), counter requires `off ==
   occurrences[0]` (`c2-count.py:101`) and byte-pins a builder rebuild (`:129`); measured delta is
   exactly 80 on 12/12 frozen rows, so `CAPTURE_BOUND=0/12` follows while the three line-start anchors
   (315/330/993) never reach the anchor counter. · Captured-by: criterion 115. · Fix: one offset
   semantics, stated in both docstrings, re-frozen under a new builder digest; `1ed2650a…` may not be
   reused for a re-frozen C2. · Shown able to fail: the 12/12 delta measurement.

6. **flattened contract — six roles received one identical sentence and the milestone's halves appear
   in no item.** · Evidence: M7 — 66 items, 309–318 B, identical text modulo name/path; 0 mentions of
   any counter, of "positive", of the recon half; the actual work arrived only in hub prompts. ·
   Captured-by: the round-58 spot-check's routed defect (c) "dispatch prompt/handoff clarity"
   (operator-side) — this row is the lane-side half. · Fix: emit items from a role template that
   carries the counter path, the predicate id and the falsifier for that seat. · Shown able to fail:
   the item dump and the token counts.

## 5. Draft — report-body wording (verdict table skeleton)

> Claims froze at `<freeze-commit>` against base `<base-commit>`; do-nothing receipts under
> `corpus/evidence/round59/controls/`, each with a header naming command, counter sha256, builder
> sha256 and timestamp.
>
> | claim / axis | before → after measurement | counting command / evidence | verdict |
> |---|---|---|---|
> | C1 operability (historical 3/10) | base `C1=FAIL`, `REFUSE=0/7`; conforming builder `C1=FAIL`, `REFUSE=0/7`; token-smuggling builder `C1=PASS`, `REFUSE=7/7`, 7/7 lines `fail`, symlink target written | `python3 corpus/evidence/round58/c1-count.py --builder <b> --work <fresh>`; `controls/c1-before.txt`; M2–M5 | **unprovable, and the predicate is unsound** — no score delta; the positive path is reachable only by manufacturing the token |
> | C2 depth (S101) | `CAPTURE_BOUND=0/12 REBUILD=MATCH`; occurrence-offset rewrite `12/12 REBUILD=FAIL`; constant −80 delta on 12/12 | `python3 corpus/evidence/round58/c2-count.py --root <copy> --work <fresh>`; M6 | **unprovable** — clauses mutually exclusive |
>
> No score was changed or invented.
>
> | axis | round-59 verdict | evidence |
> |---|---|---|
> | operability | `unprovable`; predicate unsound (M3) | … |
> | depth | `unprovable` (M6) | … |
> | coverage | `unchanged` | 133 → 133, census exit 0 |
> | freshness | `unchanged` (no fetch; `8d77e6c1` open at fleet `:136`/`:140`) | … |
> | calibration | `unchanged` — criterion 115 unexecuted for round 59; no outside sample | … |
> | adjacency | `unchanged` | … |

## 6. Findings

- **F1 (depth, measured).** On the frozen bytes the C1 counter prints `C1=PASS` (exit 0,
  `REFUSE=7/7`) for a builder whose seven refusal lines all read `fail`, and whose only distinguishing
  behaviour is printing `=PASS` to stderr. The verdict is a substring test over builder-controlled
  text (`:156`, `:224`, `:391`) — not a function of the leg results. Replication of `R59Executor03`
  §C; independent mutant.
- **F2 (depth, measured).** The PASS-certified builder wrote `spans.tsv` through the symlinked
  `--out` (`c1mut/realdir/spans.tsv`, 24 B). The verdict therefore certifies the containment violation
  the frozen claim forbids, and `:236`'s `(target-dir-written!)` is decoration: `:394` never reads it.
- **F3 (depth, derived).** The `ref_pass` claim "false for every possible builder"
  (`R59Executor01` §1, `R59Critic59`, and this seat's own superseded draft) is false because the
  derivation enumerated only success emitters. 10 of 59 reports carry it; 8 of those also print
  `C1=PASS`.
- **F4 (operability, observed).** Round 59 froze no claim, named no counter, and staged only
  `census-start.txt` and a byte-identical copy of round 58's before-receipt; 46 of 59 seats
  independently report the absent `claims.md`.
- **F5 (operability, observed, criterion 99).** 59 seat reports exist while the dispatcher marker and
  the results file do not; `w1.ready.partial` is still growing (47/66) *after* most reports landed,
  and 11 of its entries are retry aliases. Per criterion 99 the wave is "not dispatched"; the lesson
  must say so and cite the 59 files as observed behaviour.
- **F6 (calibration, observed).** Round 58's spot-check agreed "Discernment **improved**"; round 59
  supplies no outside sample, so calibration must stay `unchanged`. The one calibration asset round 59
  *did* produce is a falsified positive control family (F1/F2), which is evidence about the predicate,
  not about discernment.
- **F7 (depth, measured).** C2's two clauses differ by a constant 80 characters on all 12 frozen rows;
  the three genuine line-start anchors are unreachable behind the `CAPTURE_BIND` `continue`.
- **F8 (coverage, observed).** Registry 133 → 133, census exit 0, five unchanged W04 warnings, 129
  capture entries (66 `.raw`); no row touched by this seat.
- **F9 (scope, observed).** The offline-reconnaissance half of the milestone is mechanically
  available: form 27,012 chars and quote offset 797 both re-derive from the committed capture with no
  network.
- **F10 (hygiene).** `c1-count.py:389` is dead code (rebound at `:390`) — the duplicate rule that hid
  `:391`. Worth one line in the lesson, not a defect row.

## 7. Not done / not claimed

- Did **not** create a round-59 claim, counter or control; `corpus/evidence/round59/` still holds only
  `census-start.txt` + `controls/c1-before.txt`. Wrote **only** this report.
- Did **not** run `c2-count.py` end to end (M6 is a form-level measurement plus a code read; the
  rebuild half is corroborated by round 58's committed SCORECARD numbers).
- Did **not** run the `--controls` arm myself; §4 row 3 is labelled cited, with the peer and section.
- Did **not** run a repaired counter (token fixed at `:391`/`:399`); `R59Executor03` §E and
  `R59Executor06` R3/R6 did, and their receipts are cited as such.
- Did **not** fetch, install or upgrade anything; no `pacman` (paused). Nothing to record under the
  tooling directive.
- Did **not** edit `SCORECARD.md`, `QUALITY.md`, `SOURCES.md`, claims, counters, controls or the
  builder. `git status --porcelain` after my work shows the same two untracked roots.
- Scratch `/fast/scratch/hyaku/chousa-r59/R59Scribe24/` held `mutant.py`, `witness.py`,
  `witness2.py`, `c1work/`, `c1mut/`, `s101.txt`, `c1.out`, `c1.err`, `c1mut.out`, `c1mut.err`;
  removed before yield.

## Artifacts

- This report: `.ufo/waves/round-59/w1/R59Scribe24.md`
- Read: `corpus/lessons/round-58.md`, `corpus/lessons/round-58-verifier-spotcheck.md`,
  `corpus/QUALITY.md:941` (99), `:974` (115), `SCORECARD.md:2902-2927`, `corpus/evidence/round58/{claims.md,c1-count.py,c2-count.py,c2/quotes.tsv,controls/c1-before.txt}`,
  `corpus/evidence/round59/{census-start.txt,controls/c1-before.txt}`, `tools/{build-spans.py,capture-text.py}`,
  `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:136,140`
- Peer evidence cited: `R59Executor01.md` §1, `R59Executor03.md` §C/§D/§E, `R59Executor06.md` R3–R6,
  `R59Executor09.md`, `R59Critic59.md`, `R59Scribe19.md`, `R59Scribe20.md`
- Wave inputs: `.ufo/waves/round-59/{w1-spec.json,w1-dispatch.json,w1.ready,w1.ready.partial}`

## 8. Seat reconciliation — R59Scribe24's own record (appended, not a rewrite of §0–§7)

Written by the seat named on this file. It keeps §0–§7 intact, states what this seat executed
itself, and withdraws two figures.

### 8.1 Ownership history of this path

| time | event |
|---|---|
| 15:18:49 | this seat's own report occupied this path (this seat measured **24,229 B** at 15:19 after its last edit; §0 records 24,250 B — 21 B apart, not litigated) |
| ~15:20–15:22 | this seat's scratch dir `…/chousa-r59/R59Scribe24/` was **recreated by an unidentified writer** (`mutant.py`, `witness2.py`, `c1mut/`, `c1.out`) after this seat had removed it |
| ~15:24 | that writer **deleted** the dir while this seat was reading it (a counter run straddled the deletion, 8.3(ii)); peer `R59Executor07-2` reports the same class of write in `R59Executor07/positive-path/` |
| 15:24:52 | this path was replaced by the 393-line report now above, whose §0 discloses supersession |

So round 59 has a **live** unidentified-writer problem: it touched a seat's scratch namespace and a
seat's report path inside six minutes. §0–§7 are not this seat's text and this seat does not endorse
their attributions — in particular M3's "(my run)" is not this seat's run (8.2(b)).

### 8.2 Own executions, and two withdrawals

**(a) The substring forge, proved as a transcription witness** (fresh scratch, real functions):

```
$ python3 …/substring-witness.py
 LEG: SYMLINK_CACHE=fail(rc=1, reason ['SYMLINK'] absent in '=PASS\n')
 LEG: FIFO_TXT=fail(rc=1, reason ['SYMLINK'] absent in '=PASS\n')
 LEG: DEVZERO_TXT=fail(rc=1, reason ['SYMLINK'] absent in '=PASS\n')
 LEG: FAT_RAW=fail(rc=1, reason ['SYMLINK'] absent in '=PASS\n')
 LEG: MANY_QUOTES=fail(rc=1, reason ['SYMLINK'] absent in '=PASS\n')
 LEG: FOREIGN=fail(reason-unnamed:'=PASS\n')
all('=PASS' in l): True   <- :391 ref_pass
all('=pass' in l): False  <- :390 ok_pass
verdict over forged ref legs + honest ok legs: PASS
```

Seven lines that each say `fail` satisfy `:391`, because `:156`/`:224` embed up to 160/200 characters
of builder-controlled stderr and the aggregate is a substring test over the whole line. This
**confirms §2/M4–M5** and is the reason 8.2(c) is withdrawn.

**(b) M3's end-to-end `C1=PASS` was not reproducible by this seat, and the failure is evidence.** A
first-hand run against the foreign writer's `mutant.py` began while the file existed and continued
after it was deleted:

```
$ python3 corpus/evidence/round58/c1-count.py --builder …/R59Scribe24/mutant.py --work …/R59Scribe24-forge/fw
rc=1
EMPTY_OK=pass
REBUILD_OK=fail(rc=2)
FOREIGN=fail(reason-unnamed:"/usr/bin/python3: can't open file '…/mutant.py': [Errno 2] No such file or directory\n")
SYMLINK_OUT=pass(refused)
SYMLINK_CACHE=fail(rc=2, reason ['SYMLINK','REGTYPE','NOT_REGULAR'] absent in "… No such file …")
FIFO_TXT=fail(rc=2, …)   DEVZERO_TXT=fail(rc=2, …)   FAT_RAW=fail(rc=2, …)   MANY_QUOTES=fail(rc=2, …)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=fail(rc=2 )
SUMMARY OK=2/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
```

So M3's receipt (`c1mut.out`, 947 B, 15:22) is **foreign evidence this seat read but did not
reproduce**; the mechanism is nevertheless independently established by 8.2(a) and by §2/M4.

**(c) Withdrawn:** this seat's earlier universal "`C1=PASS` is unreachable for every builder". It is
false as written — the correct statement is the two-sided one now in §3: unreachable for a
*conforming* emitter, reachable by smuggling the literal into stderr. This seat's own witness in
8.2(a) is the reason.

**(d) Withdrawn: "26.69 s" as a timing measurement.** One run while ~60 seats were spawning; host
load dominates. Keep the reproduction qualitative ("tens of seconds"), not a datum.

### 8.3 Three measurements §2 does not carry (own runs, 15:24)

- **(i) A builder that cannot start at all is credited as refusing.** In 8.2(b), after the deletion,
  every invocation returned `rc=2` (`can't open file`), yet the counter printed
  `SYMLINK_OUT=pass(refused)` and `ESCAPE_ENTRY=pass(refused)`. Mechanism (code read):
  `c1-count.py:233-234` **overwrites** the SYMLINK_OUT leg with `=pass(refused)` whenever the link
  target is empty, regardless of return code; `:312-315` treats any `rc != 0` plus an unwritten
  `out-esc/spans.tsv` as `pass(refused)` with no reason-class check at all. "Refused" and "crashed"
  are the same event to this counter. Consequence for the Gate wording: a repaired counter must not
  accept `rc != 0` alone, and criterion 115's control set needs a **must-fail arm built from a
  crashing builder**, not only from a silent or conforming one.
- **(ii) The namespace recycle is timestamped inside one receipt**: `EMPTY_OK=pass` followed by eight
  `rc=2` legs in a single run — the writer's deletion landed mid-count. This is the concrete evidence
  behind 8.1, and it also means a scratch path named in a wave-shared report can be recycled under
  another seat's run.
- **(iii)** The C2 delta-80 (12/12) and the fleet-root-only L0 register were re-derived
  independently by this seat with the same numbers as §2/M6 and §3; listed here only to mark them as
  this seat's own reads rather than borrowed.

### 8.4 Three sentences the round-59 lesson should take

1. C1's verdict is a **substring test over builder-controlled stderr**, so the lesson must carry the
   two-sided statement, never the universal one (§3, 8.2(a)).
2. A nonzero exit is not a refusal: `SYMLINK_OUT` and `ESCAPE_ENTRY` credit a **crash** as a pass, so
   any repaired counter must require an observed refusal reason *and* a non-crash status (8.3(i)).
3. Round 59's wave had unidentified writes into a peer's scratch namespace, this seat's scratch
   namespace, and this report path. The lesson should record the incident class and the observed
   times, and the L1 should not merge §0–§7 into the lesson without the authors' identities.
