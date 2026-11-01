# Round 68 verifier spot-check — chousa (closure, non-author)

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

Round: chousa lane-round 68. Base `27df950df83a2c0aea84cfe8de8ddb7b0ff432d4` → tip `3c05f08c9aaa66ca9c0f588e93190755424eb1e9` (branch `master`, pushed). Verified 2026-11-01T05:39Z. Method: index-free git only (`rev-parse`, `cat-file`, `ls-tree`, `diff-tree`, `merge-base --is-ancestor`, `show`, `log`, `ls-remote`), `grep`/`awk`/`sha256sum` over committed bytes (`git show <rev>:<path>`), one live re-open per spot-check item. Per the protocol's gate standard I did **not** execute the lane's gate (`tools/freeze-check.py --selftest`) or its preflight: C1's selftest evidence is **evidence-verified** (committed receipts, pins re-derived over committed blobs); C2's counter is a counting command, re-measured by me over committed bytes in a scratch repo.

## 1. Step-1 conformance — all pass

| check | command (abridged) | observed |
|---|---|---|
| report committed by lane identity | `git -C <fleet> log --format='%an %H' -1 -- .ufo/reports/round-68/chousa.md` | `chousa-shokunin 3042647ecd498b2d669b3cc98f9429f335871b0c` |
| `## SHONEN` heading | `git show HEAD:.ufo/reports/round-68/chousa.md \| grep -n '^## SHONEN'` | line 45; four `[~]` author assertions, no `[x]` manufactured |
| cited commits exist + ancestry | `cat-file -t`; `merge-base --is-ancestor <c> refs/heads/master` | `27df950d`, `061880ca`, `948afaa0`, `75deb9b8` all commits, all ancestors of master |
| branch tip pushed | `rev-parse refs/heads/master` vs `ls-remote origin refs/heads/master` | both `3c05f08c9aaa66ca9c0f588e93190755424eb1e9` — match |
| round work in range | `log 27df950d..master` | exactly the report's three commits (freeze `061880ca`, landing `948afaa0`, verdicts `3c05f08c`), all authored `chousa-shokunin` |
| dispatch/complete digest | `grep 'chousa round=68' .ufo/watchdog.log` | `21:34:10 launch chousa round=68 base=27df950df83a` / `22:23:21 complete chousa round=68 head=3c05f08c9aaa pushed=True` — matches the closure contract's digest |
| prompt durability | `log -- .ufo/prompts/chousa-round-68.md` | committed by `chousa-shokunin` (`07606617`), blob present at fleet HEAD |
| write scope | `diff-tree -r --name-status 27df950d 3c05f08c` | lane paths only (`tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`, `SKILL.md`, `.ufo/waves/round-68/`); PROVINCE.md untouched; no sibling writes |

## 2. C1 — operability (routed r67 G06 freeze-check host-drift repair): verified

**Two surgical edits, nothing else.** `git diff-tree -r -p 27df950d 948afaa0 -- tools/freeze-check.py` yields exactly two hunks: (a) `LANE_ROOT_DEFAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` replacing the hardcoded `'/home/vgpnk/Projects/shokunin/chousa-shokunin'` (base line 48), with the derivation comment; (b) inside `mk()`, `fs_name = re.sub(r'[<>:"/\\|?*]', '_', name)` plus a `seen_dirs` set and `assert fs_name not in seen_dirs` collision guard, the directory then joined from `fs_name`. The tool is unchanged landing→tip.

**34 frozen case literals byte-unchanged.** Extraction of all `case('…'`/`mut('…'` literals from base, landing, and tip bytes: 9 + 25 = 34 at each revision; `diff` of the three literal lists is empty — byte-identical. Matches the receipt's `TOOL_CASE_LITERALS=9 TOOL_MUT_LITERALS=25`.

**Before-receipts corroborated against base bytes.** `before-freeze-default-root.txt`: base line 48 is the hardcoded foreign root; the receipt's traceback cites `load_json` open at line 78 and `real()` join at line 292 — both verified at the cited lines of `git show 27df950d:tools/freeze-check.py`; `FileNotFoundError` path `/home/vgpnk/…\.ufo\waves\round-61\w1.ready` is exactly what a Windows `os.path.join` over that constant produces; `EXIT=1`. `before-freeze-colon-case.txt`: base `mk()` line 300 is `os.makedirs(rd)` on the raw display name `M01 red: claims file empty` (colon is Win32-reserved); `NotADirectoryError: [WinError 267]`, `EXIT=1`. `before-g06-preflight.txt`: `PREFLIGHT=6/7 FAILED=G06`, `EXIT=1`, with the honest note that G06 passes `--lane-root` explicitly (so this FAIL is the colon-fixture defect alone).

**Receipt pins re-derive (my own sha256 over committed blobs, no lane tool executed):**

| pin | receipt | re-derived | verdict |
|---|---|---|---|
| `TOOL_SHA256=d43c6845…e91cfa` (base) | before-freeze-default-root.txt, before-freeze-colon-case.txt | `git show 27df950d:tools/freeze-check.py \| sha256sum` = `d43c6845ebcd2081b15e47bc2f3c46b6964b7bca098639a9cabf79e533e91cfa` | match |
| `REPAIRED_TOOL_SHA256=da9f6e16…b55c2` (landing) | after-freeze-battery.txt | `git show 948afaa0:tools/freeze-check.py \| sha256sum` = `da9f6e16b9913a63fc6b16445cbe7b97ac878e6863ab8bb4e92e7922735b55c2` | match |
| `PREFLIGHT 6/7→7/7`, `G06 FAIL→PASS` | before/after-g06-preflight.txt, preflight-final.txt | evidence-verified: before `PREFLIGHT=6/7 FAILED=G06 EXIT=1`, after `PREFLIGHT=7/7 FAILED=none EXIT=0` (G08 skip disclosed in all three) | consistent |

**After-battery receipt defect (status-neutral, routed below).** `after-freeze-battery.txt` line 9 is a bare `EXIT=` (byte-verified: `EXIT=$`) — invocation 1 (bare `--selftest`) transcribes the tally (`SELFTEST 34/34 pass`, `VERDICT: FREEZE_CHECK=34/34 red_before_exit=1`) but not its exit code; only invocation 2 (`--lane-root .`) carries `EXIT=0`. The report's "34/34 exit 0, both invocations" therefore slightly over-reads the receipt bytes. Mitigation: the second invocation is the same battery through the same code path with an explicit root and documents `EXIT=0`, and the tool's own frozen semantics (red run exits 1) make 34/34 → 0 derivable. Ironically the exact class the round mined (`receipt-exit-transcription`).

**Do-nothing control holds:** at base the tool bytes carry the foreign constant and raw-name `mk()` (verified), so no counting command reaches the after state without the edit.

C1 verdict: **verified / improved**, on evidence-verified receipts + my re-derived pins and literal extraction. One capability row entered (`host-portable gate selftest execution`, first-working round 68) with the battery demonstrated in the round — no pre-claiming.

## 3. C2 — depth (sourced entry on S164–S165): verified, re-measured

- Entry absent at base (`cat-file -e` fails), present at tip; opens with the `source:` / `verified-at:` / `recheck:` provenance trio; cites S164 + S165 in `source:` and in the body.
- Registry counts from committed bytes (`git show <rev>:corpus/SOURCES.md`): base rows=163, A=122 B=30 C=11, mined=131, queued=19, rejected=13 → tip rows=165, A=123 B=31 C=11, mined=133, queued=19, rejected=13. `grep -c '^| S164 |'` 0→1, S165 0→1. Matches the report and the `after-c2-entry.txt` tallies exactly. Malformed rows 0, duplicate ids none, enum violations none (contract census awk).
- `diff-tree -p` SOURCES.md base→tip: **0 deleted lines** — additions-only; no held status/recheck/used-by cell changed.
- Semantic counter re-measured: I extracted the tip blobs of `c2-semantic-count.py` (read first: pure reads + `git rev-parse`; no network, no writes), the entry, and SOURCES.md into a fresh scratch git repo (tree ids verified equal to the lane tip blobs), then `python -I corpus/evidence/round66/c2-semantic-count.py --entry corpus/knowledge/host-portable-gate-selftest-r68.md` → all 9 checks ok, `SEMANTIC=9/9 C2SEM=PASS`, exit 0; `ENTRY_SHA256=6de8c3da…` and `REGISTRY_SHA256=ff08b249…` match the receipt's pins. (The receipt's `LANE_REVISION=27df950d` field names the then-HEAD because it was measured on the working tree pre-landing — disclosed in the receipt itself; its pins match the landed tip bytes, as my re-run shows.)
- S164 capture digest: `git show <tip>:corpus/evidence/round68/captures/microsoft-naming-a-file-63e70903.md | sha256sum` = `bf2485c9f36d278b7d96f947869e36247ff8c56eacda6b65124ad0418d7bdcec` — matches the S164 row pin and the report.
- S164 quote re-open (my own fetch, not the lane's tool): the pinned raw URL serves the sentence verbatim, and the reserved-characters list immediately below it is exactly `< > : " / \ | ? *` plus NUL and 1–31 — the set the sanitizer implements. Quote is 21 words (≤25). I did not execute `tools/quote-reopen.py`; the receipt records `verbatim=1` exit 0.

C2 verdict: **verified / improved**. Causally separable from C1 (counter + greps + capture + quote run on the base bytes too); do-nothing control holds (all four artifacts absent at base).

## 4. Self-found r67 repairs — verified; correction-note convention: respected

1. **Truncated r67 SCORECARD capability row.** Confirmed at `git show 75deb9b8:SCORECARD.md`: last line ends `` `python -I tools/digest-in-tree.py -- `` — mid-cell, no fourth cell, no row terminator. The r68 diff repairs exactly that line (+30/−1 in SCORECARD.md): the row is completed (real exit contract, controls receipt `corpus/evidence/round67/controls/after-d2-battery.txt`, first-working round 67 retained) and a correction note in the `## Round 68 verdict` section names the superseded text, the commit (`75deb9b8`), and the disposition. **Convention judgment: respected.** SCORECARD.md is a living table file, not an append-only log; the correction landed as a new commit (no amend), the truncated r67 bytes remain in history, the note is discoverable in the same file's verdict section, the report discloses it as self-found and not scored, and the lesson carries a `landing-truncation` `## Mistakes` row. The completed cell adds no new capability claim (the battery receipt it cites is an r67 artifact). One imprecision, routed below: the note's "G05 still passed because the truncated tail names no path" is not the mechanism — the tail does name `tools/digest-in-tree.py` (unterminated backtick); G05 actually skips the row because its parser requires ≥4 cells (`len(cells) >= 4`, verified in `tools/lane-preflight.py` `g05`), and a 3-cell row is never parsed. Operative fact (G05 passed over the truncated row — r67 receipts show `G05 … 90 capability pointers resolve`) is true either way.
2. **r67 preflight receipt EXIT contradiction.** Confirmed at `git show 27df950d:.ufo/waves/round-67/preflight.txt`: line 11 `PREFLIGHT=5/7 FAILED=G02,G06 …`, line 12 `PREFLIGHT_EXIT=0` — contradicting `tools/lane-preflight.py`'s documented contract ("1 at least one gate FAILED") and the round's own `preflight-after.txt` (`PREFLIGHT_EXIT=1`). Both defects are mined in `corpus/lessons/round-68.md` `## Mistakes` (receipt-exit-transcription, with the round's own scratch pipeline recurrence; landing-truncation), with class · evidence · captured-by · fix, and the r67 receipt bytes are explicitly left untouched as history. The mined lesson satisfies the frontier duty.

## 5. Owned-axis harm check

`diff-tree -r -p 27df950d 3c05f08c -- SCORECARD.md`: +30/−1, all inside the r67-capabilities/r68-planned/r68-verdict region (the −1 is the truncated row being completed). The `## Axes` table is byte-unchanged: operability stays 3/10 (last-change round 1, deliberately frozen), the other five axes unscored. No axis's evidence pointer was altered or deleted; SOURCES.md held cells unchanged; SKILL.md's only change is the freeze-check registry row gaining the r68 receipts and the two named drift classes; LOG.md additions-only. **No owned axis harmed.**

## 6. Discernment spot-check (non-author, this review)

Sample: 2 admits (S164-driven entry admission; S165 own-work row) + 1 reject (pre-open screen-out of the unpinned learn.microsoft.com URL).

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| admit `corpus/knowledge/host-portable-gate-selftest-r68.md` (narrow: two host assumptions + two error signatures; limits named) | admit | entry bytes at tip; r66 semantic counter re-run on extracted tip bytes → 9/9 PASS; receipts verified in §2 | **agree** | the entry claims exactly what was measured (base tracebacks corroborated line-for-line), scopes itself to the two repaired defect classes, and names reserved device names / trailing dots / path length / case-folded collisions out of scope — no overreach |
| admit S165 (own-work red receipts, tier B, mined) | admit | `git show` of all three before-receipts + base tool bytes (§2) | **agree** | the receipts are real committed failure transcripts whose pins re-derive from the base blob; B (not A) is conservative for own-work evidence |
| reject (pre-open screen-out): the unpinned learn.microsoft.com naming-a-file page, in favor of the pinned raw source markdown at commit `63e70903` | reject pre-open | live page fetched 2026-11-01; pinned raw URL fetched (S164 re-open) | **agree** | the rendered page's URL is not a durable revision anchor and can drift under its fixed URL; the pinned source markdown is the verifiable anchor — and the live page's frontmatter `git_commit_id: 63e70903…` today equals the pin, corroborating that the capture was taken without distortion |

Census: `bash <fleet>/scripts/sources-census.sh validate --root <fleet> chousa` → exit 0, the same five pre-existing W04 duplicate-URL warnings (S051/S053/S073/S074/S075), no new findings; the fleet-root checkout's SOURCES.md is byte-identical to the lane tip (`ff08b249…`), so the census read the landed bytes.

## 7. Trend verdicts

- **expansion: unchanged** — both new rows and the entry live inside the lane's own gates/provenance ground; PROVINCE.md untouched; no new source kind (the spec-pin practice extends the existing S160–S163 pin family). Agrees with the lane's verdict.
- **quality: improved** — a gate whose selftest exited 1 on this host at base (three red receipts, pins re-derived) now has a committed 34/34 tally with the only delta being the two host-assumption edits; the routed G06 defect closes reproducibly from committed bytes alone; the practice is written down against a pinned canonical source with a 9/9 reconciliation; no admitted entry failed a re-check. Agrees with the lane's verdict.
- **discernment: unchanged** — verdicts are counter-and-receipt-derived; no exploratory claim (budget unused); the round's own capture-practice slip is mined rather than absorbed; this outside review agrees with the sampled admit and reject decisions, and the one receipt defect found is routed below, not absorbed. Agrees with the lane's verdict.

## 8. Routed items for round 69 (status-neutral; none bars admission)

1. **Receipt exit-code transcription (this round's own):** `corpus/evidence/round68/controls/after-freeze-battery.txt` invocation 1 carries a bare `EXIT=` — the bare-mode exit 0 is evidenced only by the tally line plus the identical second invocation (`EXIT=0`). Fix next round the same way the r67 receipt was handled: keep the bytes, append a correction note (or a re-issued receipt) naming the superseded `EXIT=` line, per the round's own no-rewrite discipline.
2. **Correction-note precision:** the SCORECARD r68 correction note's G05 mechanism ("the truncated tail names no path") should say "the row lacks the fourth cell, so G05's ≥4-cell parser never reads it" — the tail does name `tools/digest-in-tree.py` in an unterminated backtick.
3. Carried from the lesson's own continuation list (unchanged dispositions, verified present): the semantic counter's filler-author residual (non-author entailment review), the two historical bare `## Capabilities` headings (operator call), the G08 full-run receipt (skip now three rounds old), and the standing L0 questions (fetch scope, SKILL-size threshold, L2-floor template) — all routed around, never treated as answered.

## 9. SHONEN note for the operator

The report's four SHONEN boxes remain `[~]` author assertions; no `[x]` was manufactured and no promotion review was performed. As in r67's verifier note: the boxes look checkable by a non-author promotion review (decision tables + cited sources in SKILL.md; end-to-end logged rounds with committed evidence; re-runnable instructions; PROVINCE.md untouched) — that review remains a separate act for the operator to schedule.
