# Round 59 calibration review

## Findings (severity order)

### Blocker — frozen claim authority is missing, so no Round 59 positive verdict can be calibrated

The assignment and `.ufo/waves/round-59/w1-spec.json` (context line 10; reviewer task lines 485–490) require `corpus/evidence/round59/claims.md`. A direct read of that exact path returned “Path not found”; the round59 evidence directory lists only `census-start.txt` and `controls/c1-before.txt` (plus the controls directory). I cannot assess claim predicates, scope, source pins, or whether any counter verdict measures those predicates. This is an evidence-package defect, not proof that a proposed claim/control is false. The available round58 claims/lesson are predecessor evidence and cannot substitute for a round59 freeze.

**Falsifier:** produce the authoritative round59 claims bytes at the prescribed path (or identify the exact authoritative alternate plus its immutable identity/hash and correct the handoff), then re-evaluate the control against those bytes. Until then, a positive round59 verdict is unsupported.

### High — the only available C1 receipt is negative baseline evidence, not positive-path calibration

`corpus/evidence/round59/controls/c1-before.txt` lines 1–16 records `OK=4/4 REFUSE=0/7`, `C1=FAIL`, `EXIT=1`. In particular FOREIGN returned rc=0 while deleting the foreign file (line 3), SYMLINK_OUT returned rc=0 and wrote to the target directory (line 4), and SYMLINK_CACHE/MANY_QUOTES returned rc=0 despite expected refusal (lines 5, 9). This falsifies any reading of the nominal EMPTY_OK/REBUILD_OK successes (lines 1–2) as sufficient evidence of safe operation. It is explicitly a `before` capture; it does not establish the state of a later builder/counter or identify any round59 frozen acceptance criteria.

**Falsifier:** a bounded, reproducible post-change run against the pinned claim/counter/builder inputs must reach the declared positive final verdict while all refusal, integrity, and side-effect controls pass; preserve the before receipt and report exact input identities and results. No such result is present in the reviewed round59 evidence snapshot.

## Scope and source grounding

`census-start.txt` records validator success for `corpus/SOURCES.md` and five duplicate-URL-across-scopes warnings (S051, S053, S073, S074, S075), then `exit=0`. That supports only the recorded local census outcome. It neither establishes that the rows are invalid nor independently verifies the underlying sources. Round58 lesson §“Candidate decisions” also records that the L0 fetch-scope ruling remains open and no live fetch occurred; therefore current external truth/freshness must not be claimed from this offline reconnaissance. For the same reason, the absent round59 claims prevent judging whether the intended source/claim scope is properly bounded.

## Residual risk and verification gaps

No claim-level verdict is possible without the frozen artifact; no post-change positive-path receipt or end census is in the listed round59 evidence. I made no external fetch, source-repository access, edits beyond this report, tool installs, or runtime/control execution. No LSP server was consulted: this is a read-only evidence/artifact review, not source-code semantic review.
### Critical — frozen verdict for the HIT document contradicts same-round rendered evidence

The lane quarantine register row `S096` is not chousa `SOURCES.md` S096: the register line 46 URL is the HIT `.doc` URL, identical to chousa S101 (`corpus/SOURCES.md:111`) and to the URL reopened in `corpus/lessons/round-59.md:10`. Yet `quarantine-verdict-lane.txt` labels register-S096 `unverifiable` because the binary capture was “never rendered to text.” The round had rendered it before the verdict run: `s101-open.txt` (mtime 15:26, before the verdict artifacts at 15:42–43) contains 27,012 characters and the register quote “根据GB3469规定，以单字母方式标识以下各种参考文献类型” at line 15; the round-59 lesson independently records a located S101 quote at character 797. The checker confirms the mechanism: `tools/quarantine-check.py:219-240` labels OLE captures `binary-office`, and `:304-308,370-372` skips quote examination and returns unverifiable for that class, without any option to pass the newly rendered form. Thus the recorded register-S096 verdict fails to account for available same-round evidence; applying the checker’s own strict rule to `s101-open.txt` makes at least one of three register-S096 quotes located (mixed, not unverifiable).

**Falsifier:** show that the rendered form is not the cited URL’s document or that the quoted text is not present under the frozen strict NFKC/whitespace test. The register row, lesson URL, raw key, and exact quote occurrence currently contradict that.

### High — quarantine identifiers are ambiguous in the lane’s own evidence namespace

The quarantine artifacts use bare `S###` ids, but they are parsed from the shokuknow register’s separate id space. For example register rows `S095/S096/S120/S125` name respectively a ZCMU `.doc`, the HIT `.doc`, a NIPH `.docx`, and a GCP Union `.doc`; chousa `corpus/SOURCES.md:105-106,130,135` uses those same ids for an own-work lesson, CiNii HTML manual, Cochrane handbook, and cnpharm HTML report. `round-59.md:22` lists the four bare ids as binary-office cases, with no namespace qualification. A reader resolving those ids against chousa SOURCES.md will attribute the quarantine findings to different sources.

**Falsifier:** prove the quarantine files’ ids are explicitly scoped to the absent-defect-register namespace at every handoff/use site, or replace bare ids with stable lane+register-row/source identities.

### High — the preserved digests do not pin the lane captures used for the verdict

`quarantine-digests.txt` contains only the register digest (matching the current register); it has no `capture` rows. But `quarantine-check.py:345-353` emits one digest per cache text file found, and the lane verdict/examine artifacts identify capture files such as `adf6ba934e813b2c326fa150.txt`. The digest receipt therefore does not identify the capture bytes used by the `--cache corpus/captures` run, despite `round-59.md:22` claiming that cache/register digests are preserved alongside the lane outputs. The unsuffixed `quarantine-verdict.txt` / `quarantine-examine.txt` also record materially different default-cache results (no captures) without a run/cache identity; they coexist with the `-lane` outputs.

**Falsifier:** provide a digest receipt generated with `--cache corpus/captures` that covers every capture consumed by the lane verdict, and identify the unsuffixed run’s cache and status as superseded or canonical.

### High — the pre-dispatch check detected the missing freeze, but dispatch still proceeded

The round-59 lesson says its pre-data presence check returned `CLAIMS_EXISTS=False` and the `claims.md` path was absent. File mtimes show `w1-dispatch.json` at 15:12:11, `w1.ready` at 15:12:15, the lesson at 15:46, and `w1.ready.dispatched` at 16:37:47; the dispatched context still directs all seats to read the nonexistent claims path. This is stronger than an unnoticed dangling reference: the missing-freeze condition was known before the recorded dispatch, yet the 66-seat wave was sent without the required predicate artifact.

**Falsifier:** show that the dispatched task payload carried an immutable, authoritative claims artifact despite the missing prescribed path. The recorded task context and evidence directory show no such artifact.

### High — persisted spec is not the task payload that was dispatched

`w1-spec.json` was modified after dispatch: its mtime is 15:14:46, later than `w1-dispatch.json` (15:12:11). Comparing all 66 item bodies to the dispatch task bodies yields 66 differences; the current spec’s generic “review ready handoff requirements” text is not the role-specific dispatched task (including this seat’s adversarial-review task). Therefore the persisted spec cannot serve as an accurate audit record of what the seats received.

**Falsifier:** an immutable pre-dispatch spec digest matching the dispatch payload; the available timestamps and full item comparison show the opposite.

### High — C1’s frozen predicate has no honest positive path and admits stderr spoofing

The copied `round59/controls/c1-before.txt` is byte-identical to round58’s before receipt. In the frozen `round58/c1-count.py`, `PASS = "pass"` (line 51), refusal legs emit lowercase `=pass(refused)` (e.g. `expect_refuse`, lines 150–160), but the aggregate and summary search uppercase `=PASS` (lines 391, 399); hence an honest successful refusal cannot satisfy the declared target. More seriously, those failure branches interpolate candidate stderr into leg strings, and the aggregate scans those strings for `=PASS`. W1 report `R59Executor09.md` documents an adversarial builder that fails all seven refusal checks, writes through the symlinked output, echoes `=PASS`, and nevertheless obtains `C1=PASS`, exit 0 (report lines 215–254). Round 59 froze no replacement counter or positive-path control, as its lesson acknowledges.

**Falsifier:** a repaired, frozen counter must reject that recorded spoof and demonstrate a genuine positive control reaching its exact verdict. No round-59 receipt demonstrates this.

## Verification gaps

No tests or runtime checks were run for this review; evidence checks were read-only. The register digest matched. The S101 quote count/offset matched the round-59 lesson. No live fetch was made; L0 fetch-scope question `8d77e6c1` remains open. The report’s findings are recommendations, not an admission or score change.

Report: `.ufo/waves/round-59/w1/R59Reviewer50.md`