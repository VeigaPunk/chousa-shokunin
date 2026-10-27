# R59Reviewer46 — adversarial review: round59 claim design, controls, positive-verdict calibration

Scope: frozen-claims contract, control provenance, counter/claim design for the operability positive-verdict path, source grounding, report contract. Offline only (L0 `8d77e6c1` open; no fetch attempted). Method: direct byte-level reads of lane artifacts, read-only git queries, and bounded scratch runs of the frozen round58 counter (`corpus/evidence/round58/c1-count.py`, unmodified) under `/fast/scratch/hyaku/chousa-r59/R59Reviewer46/`. No LSP device answered in this session, so all line citations below are from direct file reads, not semantic server output. No lane writes; no installs; scratch removed before yield (probe recipe and transcripts are embedded here so findings survive cleanup).

## Findings by severity

### Blocker 1 — the declared frozen-claims input does not exist; wave data is accumulating before any freeze

`w1-dispatch.json` (2026-10-27 15:12:11) ships `taskCall.context` to all 66 seats with "Frozen claims: …/corpus/evidence/round59/claims.md; read before work", and `w1.ready` is stamped 15:12. That path returned not-found when read at ~15:16 and still at 15:31: `corpus/evidence/round59/` contains only `census-start.txt` (15:12), `controls/c1-before.txt` (15:14:30.645), `s101-open.txt` (15:26). `git ls-files corpus/evidence/round59/` is empty and `git status --porcelain` shows `?? corpus/evidence/round59/` (lane tip `af8c0a4`). Round58 froze claims before wave data (`round58/claims.md` header; its lane commit `9e73a03 round-58: freeze claims and before controls`), and the round-58 routed defect requires "freeze must-pass positive controls that exercise the exact final counter predicate before wave data" (`corpus/lessons/round-58-verifier-spotcheck.md`, Routed defects). Round59 has already produced wave data (the 15:14 control receipt, the 15:26 S101 opening) with no claims file and no round59 counter/positive control anywhere in the directory.

Two readings, each with a falsifier. (a) The freeze step failed or was skipped: refuted by producing the authoritative claims bytes with pre-dispatch provenance at that path. (b) Round59 intentionally recon-first with a later freeze: then the dispatch text is false for all 66 seats ("read before work" names a nonexistent artifact), and if `claims.md` later cites the already-accumulated receipts/counter, the round will have frozen claims derived from wave data — repeating the exact ordering that round58's routed defect prohibits. Refuted by an authoritative round59 plan that defines the freeze point and keeps claims independent of w1 artifacts; as of 15:31 no such artifact exists in the wave directory (`w1.ready`, `w1.ready.partial`, `w1-dispatch.json`, `w1-spec.json`, reports only).

### Blocker 2 — the frozen counter's positive verdict is forgeable: C1=PASS for a builder that fails all seven refusal legs

The round58 lesson documents that `C1=PASS` is unreachable for honest builders. It is worse: it is reachable for unsafe builders. `c1-count.py:156` embeds builder-controlled `err[:160]` into the leg string; `:391` sets `ref_pass = all(("=PASS" in l) for l in ref_legs)`; `:394` `verdict = "PASS" if (ok_pass and ref_pass and integrity and denied_pass)`. A refusal attempt that exits rc=1 with stderr `=PASS` and no reason token lands on the `:156` fail path, whose echoed text contains the literal `=PASS` that `:391` counts as a passed refusal. `:232-236`: when the builder writes through the symlinked `--out` (a real hazard), the SYMLINK_OUT override appends `(target-dir-written!)` to that same echoed fail string, preserving the `=PASS` substring.

Demonstrated on the unmodified frozen counter (command: `python3 -B corpus/evidence/round58/c1-count.py --builder <probe> --work <scratch>/w-probe3`, rc=0):

```
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(reason-unnamed:'=PASS\n')
SYMLINK_OUT=fail(rc=1, reason ['SYMLINK'] absent in '=PASS\n')(target-dir-written!)
SYMLINK_CACHE=fail(rc=1, reason ['SYMLINK', 'REGTYPE', 'NOT_REGULAR'] absent in '=PASS\n')
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in '=PASS\n')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in '=PASS\n')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in '=PASS\n')
MANY_QUOTES=fail(rc=1, reason ['SIZE', 'ROWS', 'CAP'] absent in '=PASS\n')
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
```

The probe builder (scratch-only, ~90 lines) genuinely implements the safe legs (span format, digest, `offset=max(0,find(quote)-80)`, byte formula) and on every hazard input exits rc=1 printing only `=PASS` — no reason, foreign file not protected, and for SYMLINK_OUT it wrote `junk-probe.txt` through the symlink outside `--out`. Every refusal leg's own text says `fail(...)`, yet the counter prints `REFUSE=7/7` and the final verdict `C1=PASS`, exit 0. Note `DENIED=0/0`: the do-nothing controls (`controls/REFUSEALL.py` — an always-refuse stub; the r55 builder) still "deny", because deny-only controls cannot catch a reach-PASS forgery. This is the decisive input to round59 claim design: the corrected counter may not classify any leg by a substring of builder-controlled output, and its control set must include unsafe-but-functional reach-PASS attempts, not only deny-alls.

Falsifier: any counter revision whose leg classification depends on text the builder controls remains forgeable by the same recipe (refuse with the verdict token in stderr); a counter that instead requires effect evidence (rc≠0 ∧ nothing written outside `--out` ∧ foreign file preserved ∧ symlink target untouched ∧ reason class matched) cannot be forged this way. Re-running the embedded recipe is the test.

### Major 1 — the frozen counter's honest positive verdict remains unreachable (live-confirmed, both polarities now proven)

`expect_refuse` (`c1-count.py:150-160`) emits only `NAME=pass(refused)` (lowercase, `PASS="pass"`, `:49-50`) or `NAME=fail(...)`; `:391` demands uppercase `=PASS` in every refusal leg. So no conforming builder can produce `ref_pass=True`: `C1=PASS` is structurally unreachable, and `SUMMARY REFUSE=` (`:398`) is 0/7 for the honest r55 receipt, 6/7 for a reason-less refuser, 7/7 for the forger — the headline metric is pure noise in all three cases. Round58 lesson Mistake 1 recorded the unreachable half (`:391`, `:399` cited there); this review adds the forgeable half. Consequence for round59: any claim that "runs the exact round58 frozen counter" and expects `C1=PASS` is dead on arrival without a counter re-freeze; a claim that reuses these aggregation semantics inherits both defects.

### Major 2 — the builder pin covers bytes, not behavior: the pinned copy in `controls/` cannot run its own `.raw` path

`controls/build-spans-r55.py:41` sets `TOOLS = pathlib.Path(__file__).resolve().parent` and `:59` imports `TOOLS / "capture-text.py"`. The frozen directory `corpus/evidence/round58/controls/` contains no `capture-text.py` (listing: REFUSEALL.py, build-c1-controls.py, build-c2-controls.py, build-spans-r55.py, four receipts, c1-control-build.txt, __pycache__). Running the frozen counter with `--builder corpus/evidence/round58/controls/build-spans-r55.py` (sha256 `1ed2650a…` — exactly the pin at `c1-count.py:38`) crashes on every `.raw` leg: `FileNotFoundError: …/round58/controls/capture-text.py` inside `_capture_text`, yielding `FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'Traceback…')` and `HELDOUT_OK=fail(rc=1)`, `SUMMARY OK=3/4` — not the stored receipt. The byte-identical file at `tools/build-spans.py` (same sha256) reproduces the stored receipt exactly, because its sibling `tools/capture-text.py` exists (sha256 `2c0140bc…` = `CAPTURE_TEXT_SHA`, `c1-count.py:39`). The BEFORE leg still reports `BEFORE_FOREIGN=deleted` because it exercises only a `.txt` fixture, so the pin check never touches the broken path. Lesson for round59 claim design: a sha256 pin over one file does not pin behavior; the claim must pin the transitive import closure and the file's context, or the counter must resolve companions itself.

### Major 3 — round59's only controls artifact is a copied, curated round58 transcript, not a round59 measurement

`corpus/evidence/round59/controls/c1-before.txt` and `corpus/evidence/round58/controls/c1-before.txt` are byte-identical (both sha256 `2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe`, 958 bytes); the round59 copy was written 15:14:30, after dispatch (15:12:11). Its leg lines are exactly reproducible today by the frozen counter with the default builder (my `w-def` run differs only by the trailing line `EXIT=1`, which the counter never prints — `grep -c "EXIT=" c1-count.py` → 0), so the file is a curated transcript with an appended exit marker, not raw program output. Calibration nuance against a weaker reading: the copy is faithful to what the counter+default builder produce, and the receipt's content (a destructive r55 baseline) is genuinely the round58 "before" state — the defect is that round59 presents a round58 measurement as its own before-state with no fresh run, no round59-bound counter, and fixtures that embed round58 entry strings by construction (`c1-count.py:233` etc. hardcode `corpus/evidence/round58/…`), so even a fresh run cannot produce round59-specific evidence. Falsifier: a contemporaneous round59 receipt from a round59 counter with recorded command, input hashes, and raw transcript.

### Major 4 — sibling reviewer correction: the dispatch did assign differentiated work; reviewer41 audited the wrong record

`R59Reviewer41.md` (Major) states the item bodies in `w1-spec.json` are identical across all roles, so the wave "does not operationalize its stated build-and-falsify milestone". `w1-spec.json` (15:14) is indeed generic ("For round 59, review ready handoff requirements. Read …claims.md… do not write lane files." — 66 items differing only in report path). But the authoritative dispatch record `w1-dispatch.json` (15:12), whose reviewer item matches this seat's received payload verbatim, contains role-specific items: 16 executor seats ordered to "inspect and run exact round58 frozen counter/tool or controls relevant to positive-verdict-path defect", 7 critics to falsify claims/controls, 5 mutation-testers to mutation-test, 12 scribes to draft Gate/Mistakes wording, 12 scouts for offline data walks. Within-role uniformity is normal swarm practice, not a contract defect. R41's two blockers (missing claims artifact; copied receipt) I independently verified and they stand; the Major as written is miscalibrated to the artifact it cites. Falsifier for this correction: show a seat whose received payload matches `w1-spec.json` rather than `w1-dispatch.json`.

### Verified positive — S101 source grounding is genuine and offline

`corpus/evidence/round59/s101-open.txt` (47,356 bytes) is byte-identical (`cmp`) to the stdout of the pinned `tools/capture-text.py` (sha256 `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573` — equals the round58 pin) run on the lane-held capture `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`. The located quote `并以[文献类型标识/载体类型标识]表示` occurs exactly once, at character index 797, matching the round58 grounding. No network access was involved or needed. The census receipt (`census-start.txt`: five W04 duplicate-URL warnings S051/S053/S073/S074/S075, `SOURCES.md ok`, exit=0) matches the round58 census state; no live-fetch violation observed in any artifact inspected.

### Minor — report contract and scratch hygiene

(1) This seat's report path held an earlier partial draft (2.0K, no trailer) written mid-wave before the evidence above existed; this file supersedes it and carries the wave's trailer convention. (2) R59Executor07-2 reported via IRC at ~15:23 that foreign "poison probe" files (`positive-path/poison-base.py`, `positive-path/c2-poison-zh.stdout`) appeared in `/fast/scratch/hyaku/chousa-r59/R59Executor07/` which that seat did not create — an echo of round57's unidentified-writer incident. I verified the namespace no longer exists (`/fast/scratch/hyaku/chousa-r59/` now holds only `R59Executor10`, `R59Reviewer46`, `predata`), so the report is untraceable on disk; cleanup duty destroyed the evidence. Recorded as reported, unverified.

## What round59 claim design must satisfy (implied by demonstrated defects; each item kills a named failure above)

1. Counter re-freeze in which no leg classification or aggregate reads any builder-controlled text as a verdict token (kills Blocker 2 and Major 1). Refusal = rc≠0 ∧ no writes outside `--out` ∧ foreign file preserved ∧ symlink target untouched, with reason class reported separately from the verdict.
2. A positive control that drives the exact final predicate to its passing verdict with a conforming builder, and adversarial reach-PASS controls (unsafe-but-functional builders), frozen before wave data — deny-only controls provably cannot falsify this claim class (Blocker 2, `DENIED=0/0`).
3. Pins covering the transitive import closure and file context of every pinned tool (Major 2), and receipts stored as raw transcripts with the exact command, arg hashes, and exit status produced by the program itself (Major 3).
4. The claims freeze must precede further wave data, or the dispatch must stop asserting a frozen-claims input that does not exist (Blocker 1).

## Residual risk and verification gaps

- No round59 claims/counter/positive-control exist yet, so no round59 claim verdict is asserted or denied here; Blocker 1's two readings remain open until an authoritative freeze artifact or plan appears.
- The forgery run inherited my shell environment via the counter's `os.environ` propagation; the defect is structural (lines cited), but I did not test under a stripped env.
- C2 (`c2-count.py:100-103` binds the manifest offset to the unique quote occurrence while the span byte formula differs from c1's `min(CTX, offset)` variant) was not re-derived by this seat; scribe seats are measuring it, and round59 has no C2 artifact to review.
- The foreign scratch write reported by R59Executor07-2 could not be attributed or inspected (namespace already removed).
- No installs were made; no git/jj writes; no live fetches; scratch `/fast/scratch/hyaku/chousa-r59/R59Reviewer46/` removed before yield.

## Report trailer

Relative to lane root: `.ufo/waves/round-59/w1/R59Reviewer46.md`
