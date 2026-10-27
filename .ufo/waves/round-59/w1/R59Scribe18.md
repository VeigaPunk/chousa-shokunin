# R59Scribe18 — Round 59 Gate/Mistakes wording, and the positive-verdict path the round must actually falsify

Seat: `R59Scribe18` (scribe, leaf member; no dispatch, no spawn, no fetch, no install). Axis: **depth**.
Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`, lane HEAD `af8c0a460d087cbfb8245fb9326608783ccc510b`
(`git log --oneline -12`, ran). This file is my only lane write. Scratch
`/fast/scratch/hyaku/chousa-r59/R59Scribe18/` (removed before yield). No git/jj/index write, no pacman, no
fleet/sibling/shokuknow/considerthese write, no edit to frozen claims or counters (there are no round-59 claims or
counters to edit — §1).

Assignment taken literally: read the round-58 lesson and verifier spot-check, then draft evidence-backed round-59
`## Gate` / `## Mistakes` (and report) wording. Everything below is grounded in bytes that exist **now**; every check
I ran is named in §0 and every check I did not run is named in §8.

---

## 0. Commands run (exact, observed)

| # | Command (cwd = lane root unless noted) | Observed |
|---|---|---|
| 1 | `ls -la corpus/evidence/round59/ ; find corpus/evidence/round59/controls -maxdepth 3` | `census-start.txt` (535 B), `controls/`; controls holds only `c1-before.txt` |
| 2 | `read corpus/evidence/round59/claims.md` | tool error: `Path '…/round59/claims.md' not found` |
| 3 | `git ls-files corpus/evidence/round59` | empty |
| 4 | `git status --porcelain` (before and after my counter run) | `?? .ufo/waves/round-59/` and `?? corpus/evidence/round59/` — unchanged |
| 5 | `git log --oneline --all -- corpus/evidence/round59` | empty |
| 6 | `ls -la .ufo/waves/round-59/predata/` | empty (0 entries) |
| 7 | `grep -o "claims.md" .ufo/waves/round-59/w1-spec.json \| wc -l` | `67` (66 seat items + 1 wave `context`; `python3 -c` on the JSON: 66 seats, all 66 items name the path) |
| 8 | `diff corpus/evidence/round58/controls/c1-before.txt corpus/evidence/round59/controls/c1-before.txt` | no output — byte-identical |
| 9 | `sha256sum` on both receipts | both `2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe`, 958 B each |
| 10 | `python3 -B corpus/evidence/round58/c1-count.py --work /fast/scratch/hyaku/chousa-r59/R59Scribe18/rerun` | exit 1; all 14 lines through `SUMMARY` byte-identical to the round-59 receipt (receipt is 16 lines: the 14, then `C1=FAIL`, `EXIT=1`) (§2) |
| 11 | `sed -n`/`grep -n` over `corpus/evidence/round58/c1-count.py` (sha256 `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`) | §2–§3 line cites |
| 12 | `sha256sum tools/build-spans.py corpus/evidence/round58/controls/build-spans-r55.py` | both `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` |
| 13 | `ls -la /fast/scratch/hyaku/chousa-r59/R59Scribe18/rerun/realdir/` | `spans/`, `spans.tsv` (581 B) — the symlink hazard materialised during #10 |
| 14 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` | 5 `W04` lines + `ok …SOURCES.md`, exit 0; identical text to `round59/census-start.txt` |
| 15 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `133` |
| 16 | `sha256sum corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` | `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3` (= round-58 claims' S101 pin) |
| 17 | Python string-level evaluation of the frozen vs. proposed predicates (no files written) | §3–§4 tables |
| 18 | `grep -n "^chousa \| round-41\|^chousa \| round-42" /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` | lines 136, 140 — `8d77e6c1` still open |

Read (not run): `corpus/lessons/round-58.md`, `corpus/lessons/round-58-verifier-spotcheck.md`,
`corpus/evidence/round58/claims.md`, `corpus/QUALITY.md` criterion 115, `w1-spec.json`, `w1.ready`,
`w1.ready.partial`.

---

## 1. Measured state of the round-59 freeze

| Thing every round-59 seat was told to read | State at my read (2026-10-27 15:17–15:25 −03:00) |
|---|---|
| `corpus/evidence/round59/claims.md` | **absent** (check 2); absent from the index (3) and from all history (5) |
| round-59 counter (`c1-count.py` / `c2-count.py`) | **none** in the lane: `corpus/evidence/round59/` has two files, neither is code |
| `controls/c1-before.txt` | present, 958 B, sha256 `2c9bbe54…`; **byte-identical to round-58's receipt** (8–9) |
| `controls/c2-before.txt` | **absent** (round 58 had one) |
| `.ufo/waves/round-59/predata/` | empty (6) |
| builder under test | `tools/build-spans.py` = pinned round-55 **base** builder `1ed2650a…` (12) — no round-58 C1 patch landed |
| controls carried over | round-59 `controls/` = 1 file; round-58 `controls/` = 11 entries incl. `REFUSEALL.py`, `c1-controls.txt`, `c2-controls.txt`, `c2-before.txt` (426 B), `build-c1-controls.py` — **none carried** |
| `census-start.txt` | present and **reproducible**: my run (14) matches it line for line, exit 0, 133 rows, same five `W04` |

Consequence that constrains all round-59 wording: there is no round-59 claim predicate to quote, so no round-59
Gate can state a C1/C2 verdict as measured. The only receipt in the round is a **round-58** receipt whose producing
counter is `corpus/evidence/round58/c1-count.py`, and I reproduced it exactly (10). That is a *provenance* result, not
a defect in the receipt: the receipt is honest and reproducible, it is simply not a round-59 control.

Two things this rules out for the round-59 Gate:

- It must not say the claims were "frozen before wave data" — nothing was frozen.
- It must not cite `c1-before.txt` as the round-59 before-state without naming `round58/c1-count.py` as its producer.

---

## 2. Why the round-58 predicate cannot reach `C1=PASS` (exhaustive emitter audit)

`PASS = "pass"` (`c1-count.py:51`). Every leg emitter that can emit a success uses that constant:

| Emitter | Line | Success string |
|---|---|---|
| `expect_ok` (safe legs) | 147 | `f"{name}={PASS}"` |
| `expect_refuse` (5 refusal legs) | 160 | `f"{name}={PASS}(refused)"` |
| `FOREIGN` | 223 | `f"FOREIGN={PASS}(refused)"` |
| `REBUILD_OK` | 207 | `f"REBUILD_OK={PASS}"` |
| `SYMLINK_OUT` override | 234 | `f"SYMLINK_OUT={PASS}(refused)"` |

The aggregate searches uppercase only:

```python
390:    ok_pass = all(("=pass" in l) for l in ok_legs)
391:    ref_pass = all(("=PASS" in l) for l in ref_legs)
394:    verdict = "PASS" if (ok_pass and ref_pass and integrity and denied_pass) else "FAIL"
399:          f"REFUSE={sum('=PASS' in l for l in ref_legs)}/{len(ref_legs)} "
```

`ref_legs` is drawn from exactly the seven names at 386–388. Since no emitter can produce `=PASS`, `ref_pass` is
`False` and `REFUSE` is `0/7` **for every possible builder**, independent of behaviour. Measured twice: statically by
enumerating every `{PASS}` site, and empirically by rerunning the frozen counter (10) → `SUMMARY OK=4/4 REFUSE=0/7 …
C1=FAIL`, `EXIT=1`. The safe legs are reachable (`OK=4/4`); only the refusal aggregate is dead. Line 389 is dead code
immediately overwritten by 390, which is consistent with the aggregate having been edited twice and never exercised.

This does **not** weaken the receipt as evidence: in my rerun the same counter did record real failures —
`FOREIGN=fail(… foreign gone=True)`, `SYMLINK_OUT=fail(…)(target-dir-written!)`, `MANY_QUOTES=fail(rc=0, expected
refusal)` — and the hazard materialised on disk (13: `realdir/spans.tsv`, 581 B). The counter has *diagnostic* signal
and zero *verdict* resolution. Any wording that says "the before receipt shows the builder is unsafe" is supportable;
any wording that says "the counter measured it" is not, because the counter cannot print anything but FAIL.

---

## 3. Three acceptance holes that survive the obvious repair

The round-58 close routed one fix: "repair/re-freeze C1 output-token comparison". A repair that only normalises case
is unsound, and two further holes are unaddressed by any token fix. These are the properties round 59's positive
control must falsify, and none of them is in the round-58 lesson.

### S1 — the pass token is embedded in a hazard annotation (`233–236`)

```python
232:    legs.append(expect_refuse("SYMLINK_OUT", proc, ["SYMLINK"], [real / "spans.tsv"], ))
233:    if not any(real.iterdir()):
234:        legs[-1] = f"SYMLINK_OUT={PASS}(refused)"
235:    else:
236:        legs[-1] += "(target-dir-written!)"
```

Compose the seven refusal legs as a builder that does everything right except write through the symlink:

```
FOREIGN=pass(refused)      SYMLINK_CACHE=pass(refused)  FIFO_TXT=pass(refused)
DEVZERO_TXT=pass(refused)  FAT_RAW=pass(refused)       MANY_QUOTES=pass(refused)
SYMLINK_OUT=pass(refused)(target-dir-written!)
```

| predicate | result on this leg set |
|---|---|
| frozen `all("=PASS" in l)` | `False` (REFUSE 0/7 — the vacuity of §2) |
| naive repair `all("=pass" in l)` | **`True` → `C1=PASS` with a materialised write-through** |
| field-exact (below) | `False` |

So the repair the round-58 close routes, implemented as a case change, converts a hazard into a claim-level pass.
Same shape at `expect_refuse:157–159`: `if not p.exists(): return FAIL(p was touched/removed)` treats
`forbidden_touch` as *paths that must still exist* — inverted against its name — and for `SYMLINK_OUT` the passed path
is the hazard artifact, so a correct refusal trips that check and is then overwritten by 234 anyway.

### S2 — a wrong-reason refusal also passes `SYMLINK_OUT`

Line 234 overwrites `legs[-1]` unconditionally when `real/` is empty, discarding whatever `expect_refuse` returned. So
a builder that exits **0** and writes nothing (a no-op), or refuses for the wrong reason, is credited with
`SYMLINK_OUT=pass(refused)`. `expect_refuse` itself is only consulted when the target dir was written. The leg's real
predicate is therefore "the target directory is empty", not "the builder refused a symlinked `--out`".

### S3 — containment is asserted for safe legs only, and deny controls may be absent

- `expect_ok` snapshots `out.parent` and fails on writes outside `--out` (142–146). The five helper-based refusal legs
  pass `forbidden_touch=[]` (calls at 250, 263, 278, 295, 306), and `FOREIGN` is inline — so **6 of 7 refusal legs
  assert nothing about writes**. A builder that refuses *after* writing its span files passes all six.
- `denied_pass = (denied == total) if total else True` (393): with no `--controls`, `DENIED=0/0` and the deny gate is
  satisfiable vacuously. The round-59 receipt records `DENIED=0/0` — no control ran.

For calibration this is the crux: round 58's lesson records the *under*-acceptance (a good builder that cannot pass).
S1–S3 are the *over*-acceptance paths that the same predicate family carries, and a positive control that only proves
"a good builder reaches the token" cannot see them. The milestone ("build and falsify controls for positive
verdict-path calibration") is satisfiable only if both directions are controlled.

---

## 4. The positive-control contract this round should freeze

A positive verdict-path control is only worth its receipt if it is itself falsified in both directions. Minimum set
(one probe per hole in §2–§3), each with a named expected outcome:

| probe | fixture builder | required verdict | kills |
|---|---|---|---|
| P1 **must-pass** | conforming builder (all 7 refusals, correct reasons) | `REFUSE=7/7 … C1=PASS`, exit 0 | under-acceptance (§2) |
| P2 **hazard-must-fail** | conforming except writes through the symlinked `--out` | `C1=FAIL`, refusal count ≤ 6 | S1 annotation |
| P3 **no-op-must-fail** | exits 0, writes nothing | `C1=FAIL`; `SYMLINK_OUT` not `pass` | S2 override |
| P4 **vacuous-deny-must-fail** | any builder, `--controls` omitted | verdict not `PASS`, or the receipt is rejected by the freeze | S3 `DENIED=0/0` |

Design constraint that makes P2/P3 checkable (minimal patch shown; the boring alternative is to emit each leg as
`LEG\t<name>\t<pass|fail>\t<annotation…>` and compare field 3 by equality):

```python
name, rest = line.split("=", 1)
verdict = rest.split("(", 1)[0].strip()          # token isolated from annotations
ok = (verdict == "pass") and ("!" not in rest)   # no hazard annotation on a pass
```

Measured on the exact strings from §2–§3:

| leg line | verdict field | `ok` |
|---|---|---|
| `SYMLINK_OUT=pass(refused)` | `pass` | `True` |
| `SYMLINK_OUT=pass(refused)(target-dir-written!)` | `pass` | **`False`** |
| `FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)` | `fail` | `False` |
| `FAT_RAW=fail(rc=1, reason ['SIZE'] absent in …)` | `fail` | `False` |

Receipt schema the round-59 Gate should require (round 58's receipt has none of it — 14 bare lines, no header):
counter path + sha256, builder path + sha256, command line, UTC timestamp, exit code, and `DENIED=n/n` with `n>0`.
The `EXIT=1` line in the round-59 receipt is a wrapper annotation, not counter output (10) — a receipt that mixes the
two cannot be re-derived; say so, or emit exit code as a header field.

---

## 5. Draft `## Gate` wording (ready to paste into `corpus/lessons/round-59.md`)

> ### Source opened / candidate decisions
>
> - **No round-59 claim was frozen.** The path named by the wave context and by all 66 seat items,
>   `corpus/evidence/round59/claims.md`, does not exist; the directory holds `census-start.txt` and
>   `controls/c1-before.txt` only, neither is tracked, and no round-59 counter exists. This round therefore reports no
>   C1/C2 verdict; the absence is recorded, not repaired (frozen-claims rule: findings only).
> - **The one before-receipt is a round-58 receipt, reproducibly.** `controls/c1-before.txt` (958 B, sha256
>   `2c9bbe54…`) is byte-identical to `corpus/evidence/round58/controls/c1-before.txt`, and rerunning
>   `corpus/evidence/round58/c1-count.py` (sha256 `65da18bb…`) with `--work` under round-59 scratch reproduces its 14
>   lines through `SUMMARY` exactly, exit 1, `SUMMARY OK=4/4 REFUSE=0/7 … C1=FAIL`. Its producer is round 58's counter and the
>   builder it exercised is the pinned round-55 base `tools/build-spans.py` (`1ed2650a…`); it is not evidence for a
>   round-59 claim.
> - **Admit as measurement, not as verdict:** the receipt and my rerun show three concrete non-refusals
>   (`FOREIGN=fail(… foreign gone=True)`, `SYMLINK_OUT=fail(…)(target-dir-written!)`, `MANY_QUOTES=fail(rc=0,
>   expected refusal)`) and the hazard wrote through the symlink (`realdir/spans.tsv`, 581 B). The counter's own
>   aggregate cannot convert any of that into `C1=PASS` for any builder (`c1-count.py:51` vs `:391,:399`), so no
>   builder verdict is claimed.
> - **Reject:** any statement that round-59 controls were built, that a positive control ran, or that a round-59
>   counter exists. Flip: a committed `corpus/evidence/round59/` carrying `claims.md` + a counter + a must-pass
>   receipt, with P1–P4 (§4) exercised before the wave.
>
> ### Offline reconnaissance bound
>
> No external fetch this round; the fetch-scope L0 question `8d77e6c1` remains open
> (`/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:136`, restated at `:140`). Reconnaissance is bounded to lane
> bytes: e.g. S101's raw capture `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` is present at sha256 `6063a3af…`,
> matching the round-58 pin, so the round can reopen committed captures but may not refresh them.
>
> ### SOURCES changes
>
> Rows 133 → 133; added A/B/C 0/0/0; census validator exit 0 at start and end with the same five pre-existing `W04`
> warnings; `census-start.txt` reproduced line for line today.

*(If a round-59 claims file lands before filing, insert instead: "Claims frozen at `<sha>`; receipts `<paths+sha256>`;
P1–P4 outcomes `<tokens>`" — and do not reuse the round-58 receipt or builder as the after-state.)*

---

## 6. Draft `## Mistakes` rows

1. **unfrozen — the round ran without a claims file while 66 seats were told to read it.** Evidence: `read
   corpus/evidence/round59/claims.md` → not found; `git ls-files corpus/evidence/round59` → empty; `grep -o claims.md
   w1-spec.json | wc -l` → 67 (66 items + context); `.ufo/waves/round-59/predata/` empty. Captured-by: the round-58
   Gate's own "claims frozen before wave data" line and QUALITY criterion 115's pre-freeze duty; nothing analogous
   bound round 59. Fix (prospective): the wave's `w1.ready` must not be written until the claims file and its
   before-receipts exist and are tracked; a seat that cannot read a named frozen artifact reports the absence and no
   verdict, as here. Flip: a committed `round59/claims.md` + counter + before receipt, cited by sha256 in the lesson.

2. **copied — the round's only control artifact is the previous round's receipt, unlabelled.** Evidence:
   `diff` of `round58/controls/c1-before.txt` and `round59/controls/c1-before.txt` → no output; both sha256
   `2c9bbe54…`; my rerun of the round-58 counter reproduces its 14 lines through `SUMMARY` exactly (output kept in my
   round-59 scratch, removed before yield).
   Affected: `corpus/evidence/round59/controls/c1-before.txt`. Why it matters: a receipt without its producer, builder
   digest, timestamp or command cannot be compared across rounds; here it silently re-certified the round-55 base
   builder (`1ed2650a…`, i.e. no C1 patch exists) as "the base". Fix: header fields per §4 and a `produced-by` line.
   Flip: distinct round-59 receipt naming `round59/c1-count.py` + builder digests.

3. **vacuous — the frozen refusal predicate is unreachable for every builder, and the proposed repair over-accepts a
   materialised hazard.** Evidence: `c1-count.py:51` (`PASS = "pass"`) against `:391` and `:399` (`=PASS`), with every
   success emitter at `:147,:160,:207,:223,:234`; measured `REFUSE=0/7` on rerun. On the seven-leg composition in §3,
   `all("=pass" in l)` returns `True` with `SYMLINK_OUT=pass(refused)(target-dir-written!)` present, while the
   field-exact parse returns `False`. Captured-by: QUALITY 115 required a must-pass control before the freeze but
   named only the under-acceptance direction. Fix: freeze P1–P4 together (§4), and treat a case-only token repair as
   insufficient. Flip: a re-frozen counter whose P2 run prints `C1=FAIL` with the hazard present.

4. **under-asserted — 6 of 7 refusal legs assert no write containment, and `DENIED=0/0` satisfies the deny gate.**
   Evidence: `forbidden_touch=[]` at the five `expect_refuse` call sites (`:250,:263,:278,:295,:306`), `FOREIGN`
   inline with no snapshot, `denied_pass = … if total else True` (`:393`); round-59 receipt records `DENIED=0/0`, and
   round 58's deny-control fixture `REFUSEALL.py` was not carried into round 59, so even P4 has to be rebuilt.
   Fix: snapshot the work root for every refusal leg and require `total > 0` in the frozen target. Flip: a refusal
   leg that fails when the builder writes inside its own `--out` before refusing.

---

## 7. Draft report wording (round-59 report, bullets as they should read)

- **Operability (3/10, lowest scored axis).** No round-59 claim, counter or must-pass control exists; the only control
  artifact is round 58's receipt, reproduced exactly today (`sha256 2c9bbe54…`, `SUMMARY OK=4/4 REFUSE=0/7 C1=FAIL`,
  exit 1). Axis verdict **unchanged**; no score increase claimed.
- **Depth.** No knowledge entry admitted; `SOURCES.md` 133 rows, census exit 0 with the same five `W04`. S101's
  committed capture verifies at `6063a3af…`; no reopening beyond committed bytes (L0 `8d77e6c1` open).
- **Calibration (wording side).** The round-58 repair route (token comparison) is insufficient as stated: a
  case-normalised aggregate credits a materialised `SYMLINK_OUT` write-through (§3 S1), and two further acceptance
  holes (S2, S3) are outside any token fix. Four probes P1–P4 and a receipt header schema are proposed in §4.
- **Controls.** `DENIED=0/0` — state plainly that no deny or positive control ran this round.
- **Waves.** One v2 wave, 66 seats (all 66 item texts name the absent claims path); no seat count of settled reports
  is asserted here — the wave is still running at my read (`w1.ready.partial`).

---

## 8. Not claimed / limits

- I did **not** author or run a conforming (positive) builder; P1 is specified, not executed. So I make no claim about
  the ceiling a repaired counter would reach on a real patched `tools/build-spans.py`.
- I did **not** edit, patch or re-freeze any counter. The "field-exact" parser and the P2 composition were evaluated
  as string predicates in Python against the exact leg strings, not by running a patched counter.
- I ran the **round-58** counter once (check 10), against the lane's current builder, with `--work` under my scratch;
  all writes landed under `/fast/scratch/hyaku/chousa-r59/R59Scribe18/` and `git status --porcelain` was identical
  before and after (check 4).
- I did **not** read sibling round-59 seat report bodies; §1–§4 are independent measurements.
- I did **not** fetch, resolve any URL, install or update a tool, or touch `~/.local/bin`; no pacman transaction (it is
  paused); `/home/vgpnk/.omp/agent/RULES.md` was not needed for an install. No git/jj/index write.
- The round-59 tree is untracked and may change after 15:25 −03:00; §1 is scoped to that window.

## 9. Routing for the round owner

1. Do not file a Gate that asserts a round-59 freeze. File the absence (§5 first bullet) or land `claims.md` + counter
   + before receipt and re-read them by sha256.
2. Freeze P1–P4 with the counter, not after it; require `DENIED=n/n, n>0` and a receipt header (`produced-by`, digests,
   UTC, command, exit).
3. Treat the case-only token repair as insufficient; adopt a field-exact leg parse or TSV legs.
4. When quoting the round-59 receipt, say "round-58 counter, reproduced" and cite `2c9bbe54…`; never call it round 59's
   before-state.

Report: `.ufo/waves/round-59/w1/R59Scribe18.md`
