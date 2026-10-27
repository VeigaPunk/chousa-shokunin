# R59Reviewer48 — adversarial review of round-59 claim design, controls, source grounding, scope and report contract

Seat: R59Reviewer48 (leaf reviewer; no spawns; no lane edits; no live fetch; L0 `8d77e6c1` untouched).
Everything below was measured in this seat. Scratch used and removed: `/fast/scratch/hyaku/chousa-r59/R59Reviewer48/`.

## Findings

### H1 (High, scope/dispatch) — The round dispatched 66 seats against a claims artifact that never existed; no preregistered predicate exists to calibrate against

The dispatch binds every seat to `corpus/evidence/round59/claims.md` "read before work": `w1-dispatch.json` `taskCall.context` (the line beginning `"context": "/skill:godspeed\nRound 59 chousa…` ≈ `:696`, repeated in every task body) and `w1-spec.json:10`. `test -f` on that path returns false today; every file now in `corpus/evidence/round59/` has mtime 2026-10-27T15:12:21 or later, i.e. all were written after `w1-dispatch.json` (15:12:11) and `w1.ready` (15:12:15) — no claims bytes predate the dispatch. The lane's own lesson confesses this (`corpus/lessons/round-59.md` `## Mistakes` row 1; criterion 116). The milestone ("build and falsify controls for positive verdict-path calibration") was also unbuildable by construction: all 66 items are read-only ("Never edit lane files"), so no seat could land a replacement counter even had a freeze existed. The round's honest handling (lesson header "claims: none validly frozen", Trends unchanged, r58 debts explicitly not closed) is correct; the dispatch itself is the defect.

**Falsifier:** produce pre-dispatch claims bytes for `corpus/evidence/round59/claims.md` with a timestamped or digest receipt predating 2026-10-27T15:12:11. A file created after the wave does not falsify.

### H2 (High, calibration) — Forged positive verdict on the frozen round-58 C1 counter, independently reproduced with my own fixture; the honest positive path is simultaneously unsatisfiable

Counter and pins verified: `corpus/evidence/round58/c1-count.py` sha256 `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f` (the round-58 freeze), `tools/build-spans.py` = `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` (the r55 pin).

Mechanism (frozen bytes): `PASS = "pass"` (`:51`) while the refusal aggregate scans uppercase — `ref_pass = all(("=PASS" in l) for l in ref_legs)` (`:391`) and the SUMMARY count `=PASS` (`:399`); `expect_refuse` (`:150-160`) and the FOREIGN leg (`:223`) interpolate up to 160/200 chars of candidate-controlled stderr into the leg string; the containment annotation `(target-dir-written!)` (`:233-236`) is never read by the verdict.

My run (scratch builder sha256 `8c54020311c6415c7b11d8b76632dd8de2802265adc2f3624dd44eaec7df8e70`, written independently of `R59Executor09.md` §6's `1a3aad9b…`): all seven hazard legs printed `fail(rc=2, reason […] absent in 'build-spans: refused undifferentiated refusal, no reason token: X=pass? =PASS forged\n')`, the symlink leg printed `(target-dir-written!)` — the escape artifact really was written through the link — and the frozen counter printed `SUMMARY … REFUSE=7/7 … C1=PASS` with `EXIT=0` and `DENIED=0/0`. Conversely the honest path cannot emit the target: every refusal success renders lowercase (`=pass(refused)`), so `ref_pass` is False for any non-spoofing builder (`controls/c1-before.txt` shows this live: `ESCAPE_ENTRY=pass(refused)` alongside `REFUSE=0/7`, `C1=FAIL`). The frozen target `C1=PASS` (round-58 `claims.md` C1) is therefore unreachable-honest and reachable-forged; the 3/10 operability axis cannot be moved by this counter in either direction. Recorded as criteria 115/117; round 59 froze no replacement, so the debt stays open (lesson, "Round-58 outside-review intake").

**Falsifier:** any honest candidate that satisfies all seven refusal legs and prints `C1=PASS` exit 0 on `65da18bb…`; or show my spoof output above was not produced by the frozen bytes (digests cited).

### H3 (High, source grounding) — The quarantine receipts' S-ids follow the external campaign register's numbering, which collides with `corpus/SOURCES.md` ids; the lesson reports the verdicts without disclosing the namespace

`tools/quarantine-check.py` resolves captures by `cache_key(url) = sha256(url)[:24]` of the **register row's URL** (docstring `:22-26`, `:142-143`, `cache_doc` `:244-258`; slice columns `id, round, class, url` from the register, `:13-14`, `:187-202`). Comparing `quarantine-slice-rederived.tsv` URLs with `corpus/SOURCES.md` rows, at least ten ids denote different sources in the two registries:

| register id | register URL = capture key (verified where noted) | lane row with that id | lane row holding that URL |
|---|---|---|---|
| S077 | doi.org/10.1186/s13643-020-01542-z | pdftotext manual | — |
| S080 | std.samr.gov.cn gbDetailed | WARP FAQ | — |
| S082 | support.nii.ac.jp/ja/cir/manual_articles_detail | AVeriTeC README | lane **S096** |
| S084 | jstage FAQs TAB2 | AVeriTeC train.json | lane **S098** |
| S086 | ncpssd.cn (receipt: "missing capture") | FEVER PDF **with committed capture** quoted in its own anchor cell | — |
| S093 | aclanthology 2026.findings-acl.19.pdf | arXiv climate-fever | lane **S090** |
| S094 | ojs.aaai 29825/31432 | COLING 2025 paper | lane **S091** |
| S095 | zcmu …C3A00.doc → `b539a802…` (sha256(url)[:24] verified) | round-47 spotcheck | lane **S100** |
| S096 | jc.hit.edu.cn HIT .doc → `6dc68fd6…` (verified; = S101's pinned capture) | CiNii manual | lane **S101** |
| S116 | aclanthology N18-1074.pdf → `1c15b611…` (verified) | (lane S086 holds this URL) | lane **S086** |

Also matching the pattern: register S110 = `2025.coling-main.108.pdf` → capture `a9cf4170…` (key verified) = lane S094's source. Register S108 genuinely matches lane S108 (arXiv 1803.05355) — the mapping is partially aligned, which makes silent reading more likely to err. The reader-facing contradiction sits inside one document: the lesson's Gate section opens **lane** S101 (HIT doc, quote located at char 797) while its quarantine list says "S101 unverifiable — the gate block named no locator, so no quote was checked" (**register** S101, a different source); likewise "S086 missing local capture" though lane S086 has a committed, row-anchored capture. The verdicts themselves are internally valid under the register mapping and the round's honesty guards hold ("no absent label asserts the live origin is absent"; nothing admitted; "not marked complete") — but the lesson never states that the ids are register-namespace ids, which QUALITY 3/9 (observation/inference separation; restatements name their owning set) requires for a restated finding.

**Falsifier:** any round-59 artifact disclosing the namespace difference, or one disputed id whose register URL equals its `corpus/SOURCES.md` URL (the ten rows above show the opposite; digests.txt pins the register at `5afe1810…`).

### M4 (Moderate, receipt custody) — Two contradictory receipt pairs preserved without provenance, and the lesson's "cache/register digests are preserved" claim is false as written

`corpus/evidence/round59/` holds two examine/verdict pairs: the non-lane pair (`quarantine-examine.txt`, `quarantine-verdict.txt`, mtimes 15:42:46-47) shows **all 24 rows `no-capture`/`unverifiable`** — a run whose `--cache` resolved nothing (wrong cwd/root) — and the lane pair (`quarantine-examine-lane.txt`, `quarantine-verdict-lane.txt`, 15:43:03-04) with the real per-capture results the lesson reports. Neither file carries a header naming its cwd, cache path, or run identity. The preserved `quarantine-digests.txt` (mtime 15:42:47 — the **non-lane** run) contains only the `register` line; the tool's `digests` command prints a `capture` line for every consulted capture (`tools/quarantine-check.py:380-388`), and the lane run demonstrably consulted captures (14 `absent` verdicts name capture files), so a lane-run digests receipt would list ~18 `capture` lines. No such receipt exists anywhere in the round: the reported lane run's cache digests are preserved nowhere, and the only digests receipt documents the unreported run. The lesson sentence "full outputs and cache/register digests are preserved in `quarantine-{examine-lane,verdict-lane,digests}.txt`" is therefore wrong on both halves.

**Falsifier:** a round-59 receipt with `capture<TAB>…` lines matching the lane run, or a provenance header on the non-lane pair. Neither exists today.

### M5 (Moderate, claim design) — The frozen C1 predicate never exercises the do-nothing controls the claim itself declares

Round-58 `claims.md` freezes the C1 predicate as `python3 corpus/evidence/round58/c1-count.py --builder <builder> --work <fresh-absolute-dir>` — no `--controls` — while the counter runs its control loop only `if args.controls:` (`:376-381`), and the same claims file says "Do-nothing controls must not reach C1=PASS" and the freeze-time receipt `controls/c1-controls.txt` did pass `--controls` (DENIED=2/2). My H2 run satisfied the predicate verbatim: `C1=PASS`, exit 0, `DENIED=0/0` — the control gate never binds a claimant. Two aggravators, both measured by `R59Executor09.md` and consistent with the code I read: the REFUSEALL control, when scored, crashes the counter as candidate (`FileNotFoundError` at `:212`), so `denied` counts a crash indistinguishably from a scored refusal (`:376-381` counts any non-`C1=PASS` tail); and the integrity leg requires `controls/build-spans-r55.py` to sit beside the counter copy (`:355-360`), so the positive verdict also depends on a control artifact's presence, not only the candidate's behaviour.

**Falsifier:** run the frozen predicate command exactly as written with a candidate that passes all legs and show the output names the controls (it cannot: no `--controls`, no `CONTROL_*` lines, `DENIED=0/0`).

### M6 (Minor, report contract) — Criterion 14's literal intake heading is gone, and the persisted spec is confirmed non-authoritative on my own seat

(a) Criterion 14 (round 25, in force: "criteria 1–115 unchanged") requires each lesson to carry `## Spot-check intake`; `grep -qx '## Spot-check intake' corpus/lessons/round-59.md` exits 1 (heading is `## Round-58 outside-review intake`, `round-59.md:31`; round-58's `## Spot-check intake from round 57` also fails the exact match). The per-debt substance is present, so this is a letter violation, not a substantive one. (b) The spec/dispatch binding defect (criterion 118) reproduces exactly: `SPEC_ITEMS=66 DISPATCH_TASKS=66 REGISTRY_MEMBERS=66`, item bodies equal to dispatch tasks **0/66** and to registry members **0/66**; on my own seat the persisted spec item reads "For round 59, review ready handoff requirements. Read …/round59/claims.md…" while the dispatched task I received reads "Adversarially assess round59 claim design…" — the spec reconstructs no seat's assignment, and even the rewritten spec still binds seats to the absent claims file. (c) Verified accurate, for the record: the lesson's citation `round-58-verifier-spotcheck.md:19-26` does land on the Discernment table recording the S101-admit / GB3469-reject agreement.

## Verified-accurate (source grounding that checks out)

- **S101 chain:** raw capture sha256 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3` matches the round-58 pin; `tools/capture-text.py` sha256 `2c0140bc…` matches the frozen pin; the pinned tool prints `LOCATED count=1 offset=797` for `并以[文献类型标识/载体类型标识]表示`; a fresh render is 27,012 characters and byte-equal to `s101-open.txt`. The 14.3.4 variant `标志/载体类型标志` also occurs once, so the located quote's uniqueness is real, not a variant artifact.
- **Census:** recount of `corpus/SOURCES.md` with the lesson's command semantics = 133 rows, matching census-start/census-end receipts (exit 0); the five W04 warnings are exactly the fragment-stripped canonical-URL duplicate set (S050/S051, S052/S053, S059/S074, S071/S073/S075 → subsequent rows flagged), so no in-lane duplicate is missed; the register-S096/lane-S101 duplication is cross-repo and invisible to W04 by construction.
- **used-by old→new:** S101 row now carries `citation-count-semantics-r37.md, lessons/round-58.md, lessons/round-59.md`, status `mined`, recheck `180d` — exactly as the lesson states; no other cell changed.
- **Quarantine arithmetic:** lane verdict = 14 `absent` + 6 cache-`unverifiable` + 4 register-`unverifiable`; the lesson's "14 absent … 10 unverifiable" split and its per-id lists match `quarantine-verdict-lane.txt` row for row (under the register namespace, see H3). `quarantine-slice-bad-ids.txt` is 0 bytes = "0 invalid IDs".

## Residual risk

- Until a counter derives its verdict from structured per-leg states (criterion 117's fix) and a claims freeze precedes dispatch (116), any future positive operability verdict on this axis is uninterpretable: the same bytes both block honest candidates and credit forgeries, and my H2 fixture is reproducible by anyone.
- The quarantine id collision (H3) means every future restatement of "S### absent/unverifiable" from this register must carry the namespace or it will be read against the wrong rows; nothing in the round binds the two id spaces.
- The register digest `5afe1810…` is taken from the tool's own output; I did not reopen the shokuknow register file to re-hash it (sibling tree left untouched).
- Round-58 C2's offset/rebuild contradiction and the S101 row's deprecated UTF-16LE anchor form (criteria 97/101/100) remain unrepaired by design this round; the round-59 Gate wisely cites only the defined form.

## Verification gaps

- No LSP device was available in this session; all code-level claims are from direct reads of the named lines plus executed reproductions, not semantic indexing.
- I did not re-run `c2-count.py`, did not re-derive the register slice from shokuknow bytes, and did not execute the round-58 C1 counter against a *honest* all-legs candidate (the lowercase-token unsatisfiability is established from the frozen code paths plus `c1-before.txt`/`R59Executor09.md` §2-3, not from my own positive-build run).
- Wave-level: I sampled one sibling report (`R59Reviewer47.md`) for cross-checking; I did not audit the other 65.

Report: `.ufo/waves/round-59/w1/R59Reviewer48.md`
