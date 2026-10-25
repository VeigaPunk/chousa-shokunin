# RevRoutedRepairs

Seat: revenger, round-43 w1. Measured commit `737f40b6aa8f37ffe2269db370fd6d65a720d9a8` (HEAD; lesson files have an empty diff against that commit). No lane production file, index, or fleet file was edited. No counter was re-run. No capture byte length was re-measured. No network.

## Axes

- Operability: the check is a search of two files plus the commands that show a claimed pointer is or is not there. Those commands were run. An unrun check is not treated as passed.
- Calibration: a disposition counts only if it is in `corpus/lessons/round-43.md` or in the round-43 erratum section of `corpus/lessons/round-42.md`. A pre-erratum sentence in `round-42.md`, a `LOG.md` claim, and a `QUALITY.md` sentence are not that surface. They are quoted only as divergences or as text a pointer cites.
- Depth: each routed ask is quoted, then the pointer or the negative search, then whether the pointer lands the ask or only a narrower rule.

## Reconstructed contract

The five repairs are the list under `## Routed defects for round 43 (lane must fix)` in `corpus/lessons/round-42-verifier-spotcheck.md` (lines 164–182), written against lane tip `e0f4895c48d6c6e739ce9deb614b97c771a3a096`. This seat's contract is: each of those five has a disposition in `corpus/lessons/round-43.md` or in the erratum in `corpus/lessons/round-42.md`; quote the pointer; do not edit.

Last-known-good invariant for this surface: a routed repair is closed only by a later sentence in one of those two places that addresses that repair. Current behavior diverges on two of the five: the lesson and the erratum are silent, while `LOG.md` asserts dispositions that those files do not carry.

## Verdict

| # | repair | in the required surfaces? | pointer |
|---|---|---|---|
| 1 | absent-class split | yes | `corpus/lessons/round-43.md:1`, `:14–15`, `:24` |
| 2 | wave completion | yes, narrow | `corpus/lessons/round-43.md:26` (cites QUALITY 61; neither receipt-form the spot-check named is in the lesson or the erratum) |
| 3 | inherited debt | no | no sentence in either allowed file |
| 4 | register staleness | no | no sentence in either allowed file; the pre-erratum stale-summary rows are the defect the spot-check already recorded, not an r43 disposition |
| 5 | 265/267 bytes | yes, both files | `corpus/lessons/round-43.md:25` and `corpus/lessons/round-42.md:151–153` |

3/5 have a pointer. 2/5 do not. Of the three pointers, wave completion does not land either form the spot-check named.

## 1. Absent-class split — disposed

Spot-check ask (`corpus/lessons/round-42-verifier-spotcheck.md:166–168`):

> 1. `absent`-class split named but not landed: separate "the source carries the text and the row quotes it wrongly" (e.g. S093 79/120) from "the source does not carry it" (e.g. S086 4/46) — already in `SCORECARD.md` planned for r43; keep it routed until landed.

Pointer in `corpus/lessons/round-43.md`:

> # Round 43 — the absent class splits, and one search-log entry is re-grounded locally

> | class-collapse — one label hid two failure modes | round-42 table labelled 15 rows `absent`; S093 is 79/120 of the quote and S086 is 4/46 | none — QUALITY 59 names capture form, not overlap | rule R43-SPLIT and `tools/absent-split.py`; shown able to fail by the flipped-row control (14/15) |

The same file's claims bullets (`:14–15`) name the two classes the rule emits: `BOTH_NONEMPTY=1/1` (misquote 9, not-carried 6) and `SPLIT_AGREES=15/15`, with flipped S086 at `14/15`. Those counts are the lesson's assertion. This seat did not re-run `c1-count.py` or `c2-count.py`, so they are not re-measured here.

The name `R43-SPLIT` resolves in `corpus/evidence/round43/claims.md:14–19` (cited by the lesson, not itself one of the two disposition files): a round-42 `absent` row is `misquote` iff its max NFKC+whitespace-collapse longest-run ratio is `>= 1/2`, else `not-carried`. That is the operationalization of the spot-check's two prose classes. The bound was not retuned by this seat.

Inference, marked as such: the author treated landing `tools/absent-split.py` plus the flipped-row control as closing "keep it routed until landed." The pointer exists and names that landing. Whether the 9/6 split actually places S093 on the misquote side and S086 on the not-carried side is other seats' measurement, not this one.

## 2. Wave completion — disposed narrowly

Spot-check ask (`corpus/lessons/round-42-verifier-spotcheck.md:169–172`):

> 2. Wave shortfall: 64-seat dispatch issued but unsettled at budget close — name the dispatch-completion mechanism in r43 (a receipt the wave seats actually ran, or a smaller validated wave that settles inside the budget). Recorded as honest shortfall, not a defect of the claims.

Pointer in `corpus/lessons/round-43.md:26`:

> | prepared-as-dispatched — a validated spec with null agent ids was the round's wave evidence | `.ufo/waves/round-42/w1/swarm-registry.json` members have null agent ids; 0 seat reports | none until this round | QUALITY 61; a spec is not a dispatch. Shown able to fail: the r42 registry fails a check that requires a non-null agent id or a seat report |

That sentence is in the required file. It names the failure mode and points at QUALITY 61. It does not contain either alternative the spot-check parenthesized: no receipt that wave seats ran, and no smaller validated wave that settled. The erratum does not mention a wave.

The cited criterion, outside the two files, is `corpus/QUALITY.md:542–552`:

> 61. **A validated wave spec is not a completed dispatch.** A spec, a plan, and a registry whose agent ids are null are preparation. A dispatch is complete only when the dispatcher stayed alive until each seat settled, and the record names the seats that returned a report and the seats that died. Counting a prepared spec as a dispatched wave hides the shortfall. Check: the round report's wave section cites seat reports or names the dead seats with their last error; a registry of null ids with zero reports is a shortfall, not a completed wave. Shown able to fail: round 42's `w1/swarm-registry.json` has 64 members and null agent ids, and zero seat reports landed. Operator proposal mined from `considerthese/2026-10-24.md` (2026-10-24), "Track prepared-but-undispatched waves". — `lessons/round-43.md`.

The positive completion sentence ("dispatcher stayed alive… names the seats that returned… and the seats that died") lives in QUALITY 61, not in the lesson sentence and not in the erratum. The lesson's own words are the negative half: "a spec is not a dispatch."

Observed support for the shown-able-to-fail half, this seat:

```
members=64 null_agentId=64
```

```
=== r42 w1 markdown reports ===
0
=== untracked md under r42 w1 ===
(no porcelain md lines)
```

Round 43's own wave is this in-flight wave. Commit `737f40b` cannot cite its seat reports. `SCORECARD.md:2376` records "discernment unchanged until a non-author spot-check" and does not claim this wave settled. `corpus/lessons/round-43.md:60` says the non-author spot-check is pending and that seats this lane dispatches are still the lane. That is an independence note, not a completion receipt.

## 3. Inherited debt — no disposition in the allowed files

Spot-check ask (`corpus/lessons/round-42-verifier-spotcheck.md:173–177`):

> 3. Inherited working-tree debt: `PROVINCE.md` mode bit, two modified prior-wave swarm-registries, r41 `cells.json`, and 36 untracked r40/r41 seat reports remain uncommitted — the lane's respawn rule requires resolving lane-authored leftovers; orchestrator-owned seat reports need an operator/orchestrator decision (commit as wave evidence or leave). Named, not swept.

Negative search of the required lesson (exit 1, no matches):

```
=== tighter inherited-debt negative (r43 lesson) ===
exit=1
```

Command: `rg -n -e 'inherited' -e 'working-tree' -e 'working tree' -e 'PROVINCE' -e 'cells\.json' -e 'uncommitted' -e 'respawn' -e 'mode bit' -e 'untracked' corpus/lessons/round-43.md`

The same tokens are absent from the erratum body (the `awk 'NR>=151'` probe exited 1). The erratum text is only the 265/267 sentence quoted under item 5.

A looser first probe matched `round-43.md:26` on the substring `seat reports`. That line is the wave-completion row ("0 seat reports"), not inherited debt. It is not a pointer for this item.

The pre-erratum body of `round-42.md` also does not name this debt. The spot-check found it after that lesson was written (`e0f4895`).

Out of surface, not a satisfying pointer: `LOG.md:1554` says

> Inherited debt, deliberate: `PROVINCE.md` mode restored to 644 (content unchanged). Prior-wave registries, r41 `cells.json`, and untracked r40/r41 seat reports left untouched and named; they are not this round's work.

That sentence is not in the lesson or the erratum. Observed worktree against `737f40b`, this seat, read-only:

```
 M .ufo/waves/round-40/w1/swarm-registry.json
 M .ufo/waves/round-41/w1/swarm-registry.json
 M corpus/evidence/round41/receipts/cells/cells.json
```

```
r40 ?? 33
r41 ?? 3
```

```
644 /home/vgpnk/Projects/shokunin/chousa-shokunin/PROVINCE.md
100644 0f94a0c4f73cec2e36d587b199d7c43716ceae8c 0	PROVINCE.md
```

`git ls-tree` at both `e0f4895` and `737f40b` shows `100644` and the same blob. `git diff --stat` between those commits for `PROVINCE.md` is empty. `git show --name-only 737f40b --` those four debt paths prints nothing. The mode restore, if it happened, is a worktree chmod back to the committed mode, not a committed lesson disposition. The two registries, `cells.json`, and the 33+3 untracked reports are still the debt the spot-check named. They are named in `LOG.md`, not in the required files.

## 4. Register staleness — no disposition in the allowed files

Spot-check ask (`corpus/lessons/round-42-verifier-spotcheck.md:178–181`):

> 4. Register staleness upstream (operator-side, not lane-fixable): the register's `## By lane` summary (chousa 20) and header (194/324) are stale vs the derived 24; the M12 census's 25 is not reproduced by the operator's own extraction recipe. Route to the campaign owner via the existing L0 channel.

Negative search of `corpus/lessons/round-43.md` (exit 1, no matches):

```
=== NEGATIVE: register-staleness tokens in r43 lesson ===
r43_stale_exit=1
```

Command: `rg -n -e 'staleness' -e 'stale' -e 'By lane' -e '194' -e '324' -e 'M12' -e 'campaign owner' -e 'absent-defect-register' corpus/lessons/round-43.md`

The only L0 token in that file is line 12, the still-open fetch-scope question, not a register routing:

> No external fetch (L0 `8d77e6c1` still open).

The erratum does not mention the register.

Not counted as the r43 disposition: `corpus/lessons/round-42.md:49–50` and `:84` already named the stale totals and said the slice is derived and the register is never edited. Those sentences are in the round-42 body that commit `e0f4895` already contained (`git show --numstat 737f40b -- corpus/lessons/round-42.md` is `4 0`, erratum only). The spot-check read that lesson and still routed a further action: route the staleness to the campaign owner via L0. The pre-erratum rows do not do that action, and they are not the erratum.

Out of surface, and not backed by the L0 file: `LOG.md:1545–1546` and `:1554` claim "the register-staleness L0" and "Register staleness routed by L0; the register was not edited."

Observed L0 queue, read-only, fleet porcelain of `.ufo/l0-questions.md` empty:

```
=== l0 staleness tokens ===
l0_stale_exit=1
```

```
=== l0 round-43 lines ===
118:kumitate | round-43 | Drift sentinel + same-blocker rule: ...
```

No `chousa | round-43` line. The last chousa line is round-42 (`l0-questions.md:140`), which asks about fetch re-open and id renumber. It does not say the `## By lane` summary is `chousa 20`, does not cite header `194/324`, and does not ask the campaign owner to correct the register. A fleet-wide search for `chousa 20` / `194/324` / `register staleness` under `.ufo/**/*.md` hit only `.ufo/reports/round-42/chousa.md:32`, which is the round-42 report restating the same stale totals, not an r43 routing.

Inference: the LOG sentence asserts an L0 routing that is not in the L0 queue and not in the required lesson surfaces. Residual: a routing line could exist in a file this seat did not open. It is not in the canonical L0 queue, and no round-43 chousa fleet report exists (`**/round-43/chousa.md` unmatched).

## 5. 265/267 bytes — disposed in both allowed files

Spot-check ask (`corpus/lessons/round-42-verifier-spotcheck.md:182`):

> 5. Cosmetic: report says "265-char" for the S077 capture; the file is 267 bytes. Non-blocking.

Pointer in `corpus/lessons/round-43.md:25`:

> | byte-count nit — "265-char" and "267 bytes" were reported as if one of them were wrong | S077 capture `01f657b3d0ab045c494b3f92.txt` is 267 bytes and 265 Unicode characters | the round-42 spot-check, cosmetic | append-only erratum in `corpus/lessons/round-42.md`; the r42 sentence is not rewritten |

Pointer in the erratum (`corpus/lessons/round-42.md:151–153`):

> ## Erratum — 2026-10-24, round 43 (append-only; the sentences above are not rewritten)
>
> The S077 capture `.qcache/01f657b3d0ab045c494b3f92.txt` is 267 bytes and 265 Unicode characters. The "265-char" wording above matches the decoded length. The spot-check's "267 bytes" matches `wc -c`. Neither number corrects the other. A later reader should cite both.

The earlier sentences were not rewritten. Still present:

```
73:is a 265-character bot-challenge page, S095/S096/S120/S125 are binary office documents
81:| provenance-class — ... a 265-char `Client Challenge` page ...
```

Append-only proof for that file in the measured commit:

```
--- numstat r42 lesson ---
4	0	corpus/lessons/round-42.md
```

```
 corpus/lessons/round-42.md |  4 +++
 corpus/lessons/round-43.md | 66 ++++++++++++++++++++++++++++++++++++++++++++++
 2 files changed, 70 insertions(+)
```

The hunk is only the erratum heading and the one sentence. This seat did not re-run `wc -c` or `len()` on the capture. The numeric claim is quoted from the erratum, not re-measured here. The disposition's existence, and the fact that the 265-char sentences remain, are observed.

## Evidence chain

1. Spot-check list read at `corpus/lessons/round-42-verifier-spotcheck.md:164–182`. `nl -ba` of that range matches the five asks quoted above.
2. `git rev-parse HEAD` → `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`. `git diff --stat 737f40b --` the two lesson files and the spot-check file printed nothing. `git merge-base --is-ancestor 737f40b HEAD` exited 0. The commit subject is `round-43: split the absent class and adopt one locally re-opened search-log entry`.
3. Full read of `corpus/lessons/round-43.md` (66 lines) and `corpus/lessons/round-42.md` (153 lines). The erratum is the only round-43 addition to the latter (`4` insertions, `0` deletions).
4. Positive `rg` on `round-43.md` for absent-class and wave tokens hits lines 1, 10, 14, 15, 24, 26, and 60, as quoted.
5. Negative `rg` for inherited-debt tokens on `round-43.md` exited 1. Negative `rg` for register-staleness tokens on `round-43.md` exited 1. Erratum-body probe for those tokens exited 1 except the 265/267 sentence itself.
6. `LOG.md:1541–1554` claims all five as motive and claims an inherited-debt disposition plus an L0 routing. Those two claims are not in the required files. The L0 file does not contain the routing (`rg` exit 1; no `chousa | round-43` line; fleet status of that file empty).
7. Worktree debt still present except the PROVINCE mode bit, which matches the committed `100644` blob at both `e0f4895` and `737f40b`. Round-43 commit does not touch the four debt paths.
8. r42 registry: `members=64 null_agentId=64`. Committed and untracked `*.md` under `.ufo/waves/round-42/w1`: 0.

A later python one-liner that tried to `sorted()` the agent ids raised `TypeError: '<' not supported between instances of 'NoneType' and 'NoneType'` and exited 1. That failure is consistent with all-null ids already counted; it is not an independent count.

## Divergences

- Required surface vs LOG. `LOG.md:1545–1546` lists five motives as if each were dispositioned. Items 3 and 4 have no pointer in `round-43.md` or the erratum. Item 2's pointer does not contain the receipt or the smaller settled wave the spot-check named.
- LOG vs L0. "Register staleness routed by L0" is not in `.ufo/l0-questions.md`. The register was not edited, which matches the older round-42 rule, but that is not the routed L0 action.
- LOG vs worktree on inherited debt. Mode 644 matches the committed blob. The registries, `cells.json`, and 36 untracked reports are still dirty. "Named" is true of `LOG.md` only.
- Wave pointer vs cited criterion. The lesson says "a spec is not a dispatch." QUALITY 61 also states the positive completion rule. A reader who stops at the lesson sentence has the negative half only.
- Not a divergence: the 265-char sentences remain, and the erratum distinguishes characters from bytes instead of rewriting them. The spot-check called the nit cosmetic and non-blocking. The disposition treats both numbers as true of different units. Unverified here: the file's actual `wc -c` and Unicode length.

## Confidence

- Pointer present or absent in the two allowed files: high. Both files were read whole; the negative searches exited 1; the positive lines were quoted from those reads; the measured commit matches HEAD.
- Absent-class pointer closes the routed "until landed" ask: medium. The pointer names the landing. This seat did not re-run the split. [inference] the author intended line 24 as the close.
- Wave-completion pointer fully lands the spot-check ask: low for "fully," high for "a narrower pointer exists." Neither parenthetical form is in the allowed files. QUALITY 61 names a completion rule the lesson cites but does not copy.
- Inherited debt and register staleness have no required-surface disposition: high.
- LOG's L0 claim is false of the canonical queue: high for that file; residual low that some other unsearched note holds a routing line. No round-43 chousa fleet report was found.
- 265/267 disposition exists and the old sentences were not rewritten: high. The byte/character arithmetic itself: not measured by this seat.

Stop. Assigned surface was the five dispositions. No edit to the lessons.
