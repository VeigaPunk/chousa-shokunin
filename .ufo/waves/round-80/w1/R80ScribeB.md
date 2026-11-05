# R80ScribeB — scoped findings (round 80, wave w1, lane chousa)

Scope: draft the round-80 lesson material and the append-only corrections the round-79 closure routed; draft only, the L1 lands it.
Deliverable: `.ufo/waves/round-80/w1/R80ScribeB/draft-lesson.md` (§0 landed state, §1 Mistakes, §2 corrections, §3 QUALITY, §4 considerthese pick, §5 receipt index).
Receipts: `.ufo/waves/round-80/w1/R80ScribeB/receipts/` (byte copies plus the command output that produced each).

## Revisions read (the tip moved twice during the read)

| revision | when (-0300) | what it is |
|---|---|---|
| `b7803829922770b890e9f4efdd30d12c3695439a` | 2026-11-04 | round-79 base |
| `0d253c95732c0ed19a9fa414e5d17769ddefa48d` | 23:08:26 | claims freeze + v1 wave spec (`git log -1 --format=%ad --date=iso 0d253c95`) |
| `44d09edfc20dba26ee8d58a93d365989916a2692` | 23:58:03 | attempt-2 landing: S199–S202, GATE-RECORD lines, re-run controls, `corpus/lessons/round-80.md` |
| `5ba30d87172e94dd76a49e1a94294561e90f6cbd` | 00:06 (read) | L1 landed QUALITY 152–154, `corpus/lessons/round-79-erratum.md`, the after receipt |

Every finding below names the revision it was measured at.

## Findings (command → receipt → observed line → exit)

**F1 — attempt 1 died on a provider quota error; the lane left no report.**
- `grep -o 'Your weekly usage quota has been exhausted' <ChousaR80.jsonl> | head -1` → `receipts/attempt1-transcript-facts.txt` line 4, exit 0.
- Final assistant message: `stopReason":"error"`, `timestamp 2026-11-05T01:31:10.428Z` (transcript `tail -c`, read in this seat), `errorMessage` `Devin stream error failed_precondition: Your weekly usage quota has been exhausted`.
- Fleet watchdog `2635 … lane-dead-no-report chousa round=80; … FAIL report_of (missing …)` → `receipts/watchdog-round80-attempt1.txt`.
- `grep -ci quota` over the round=80 watchdog lines → `0`, exit 1 (`receipts/watchdog-round80-attempt1.txt`). The watchdog does not record the provider cause.

**F2 — the claims, instruments and census were committed 53 min 53 s before any wave spec.**
- `git log -1 --format=%ad --date=iso 0f59b985` → `22:14:33 -0300`; `git show --name-only --format= 0f59b985 | grep -c w1-spec.json` → `0`; `claims-files=1` (`receipts/commit-timeline-r80.txt`).
- `0d253c95` → `23:08:26 -0300`; `w1-spec.json` count `1`; `claims-files=0`.

**F3 — attempt 1's `v7-legit-matrix-after.txt` has no exit status and no revision in its bytes.**
- Capture command in the transcript: `python3 -B … > /fast/scratch/hyaku/chousa-r80/l1/v7-legit2.txt 2>&1; echo "EXIT=$?"` (`receipts/attempt1-transcript-facts.txt` line 2). The file was then `cp`'d into `controls/`.
- Bytes (`receipts/sweeps-r80.txt` sweep 2): `exit_trailer=0 REV_key=0 LANE_REV_key=1 first=[MATRIX_PATH=…]`. Prefreeze: `exit_trailer=0`.
- The transcript contains no pipe to tee: `grep -o '.\{0,160\}| *tee [^"]\{0,60\}'` → no match (`receipts/tee-contexts.txt` holds only its exit line). The task's "tee'd" wording is not what happened. The defect class is the same: the exit status sits outside the bytes.
- Attempt 2's receipts carry `# exit:` lines (`receipts/sweeps-r80.txt` sweep 2: `exit_trailer=1` for `grounding-before-r80.txt`, `oracle-before-r80.txt`, `v7-legit-matrix-r80.txt`).
- Strict `REV=<40-hex>`: no round-80 receipt carries it (`grep -l '^REV=\|[^_A-Z]REV=[0-9a-f]\{40\}'` → none, exit 1; `receipts/landed-153-check-head.txt`).
- The planned landing re-measure with `--rev` never ran in attempt 1; the attempt-2 receipt `v7-legit-matrix-r80.txt` is its successor.

**F4 — scratch outside `$HYAKU_SCRATCH`.**
- `echo "HYAKU_SCRATCH=${HYAKU_SCRATCH:-<unset>}"` → `HYAKU_SCRATCH=<unset>` in this seat's environment.
- `ls -ld /tmp/r80-base` → `drwxr-xr-x 8 vgpnk vgpnk 4096 Nov 4 05:16`; `git -C /tmp/r80-base rev-parse HEAD` → `fatal: not a git repository`, exit 128 (`receipts/probes-r80.txt`).
- `find /tmp -maxdepth 1 -name '*r80*' | wc -l` → `20` (`receipts/tmp-r80-leftovers.txt`), from several lanes. Ownership of each path is not established. Attributing `/tmp/r80-base` to attempt 1 is [INFERENCE].
- Committed round-80 evidence has no `/tmp/` path: `git grep -n '/tmp/' 44d09edf -- corpus/evidence/round80` → empty output (`receipts/sweeps-r80.txt` sweep 3; the printed `exit` is `head`'s, not `git grep`'s).

**F5 — caught by the round's own instrument: the round-79 battery accepted the identity oracle.**
- `corpus/evidence/round80/controls/oracle-structure-v6-accepted.txt`: `BATTERY_EXIT=0 BATTERY_VERDICT=PASS RECEIPT_LINES=113`, `ORACLE=ACCEPTED`, `# exit: 1` (`receipts/oracle-structure-v6-accepted.txt`).
- v7 rejects it: `corpus/evidence/round80/controls/v7-legit-matrix-after.txt` line 178 `ORACLE structure-identity REJECTED positive=0/2 forger=0/11 fresh_positive=0/2 fresh_forger=0/2`.

**F6 — not caught by any round instrument: `claims.md` states a count the record contradicts.**
- `corpus/evidence/round80/claims.md:90` → `15-word located quote that supersedes S196` (`grep -noE '[0-9]+-word' claims.md` → `62:27-word`, `90:15-word`).
- S200 quote, `printf '%s' '…measurement' | wc -w` → `20` (`receipts/placeholders-and-parse.txt`); lesson `GATE-RECORD S200 … words=20`; counter at `44d09edf`: `ROW S200 record=ok quote_words=20 … verdict=OK` (`receipts/gate-grounding-head.txt`, exit 0).
- The counter reads the lesson's GATE-RECORD lines, not `claims.md`, so the frozen 15 is not re-opened by any counter. Frozen claims cannot be amended; the lesson carries an append-only row (draft §2d).

**F7 — the landed criterion 153 and the draft.**
- `grep -L 'REV=[0-9a-f]\{40\}\|LANE_REV=[0-9a-f]\{40\}' corpus/evidence/round80/controls/*.txt` at `5ba30d87` → `oracle-before-r80.txt`, `oracle-structure-v6-accepted.txt` (exit 0). Those two carry no revision key at all. Its text does not say whether a non-empty list is a pass, so as landed it is ambiguous.
- It has no exit-line rule: `v7-legit-matrix-after.txt` and `…-prefreeze.txt` pass it (second block of `receipts/landed-153-check-head.txt`).
- It accepts `LANE_REV=`; the assignment this draft implements asks for `REV=<40-hex>`. The L1 chooses; the draft states the strict rule.
- The draft's number 152 was already taken, so the draft is criterion 155, with its check command and the 8/8 UNSTAMPED output (`receipts/draft-155-and-claims-check-head.txt`). Shown able to fail: 8/8; the pass branch is not exercised by any committed receipt (recorded, not claimed).

**F8 — routed defect 4 is not landed, and the landed erratum says it is.**
- `corpus/lessons/round-79-erratum.md` item 2 says the correction is "appended to `LOG.md` as a named correction entry (§Round 80's 'Correction to the round-79 entry')".
- `git show HEAD:LOG.md | grep -c 'Correction to the round-79 entry'` → `0`, exit 1 (`receipts/draft-155-and-claims-check-head.txt`). `grep -n '^## ' LOG.md | tail -1` → `## Round 79 …` at line 2271.
- The round-79 outcome sentence (`sed -n '2307p;2310,2311p' LOG.md`, `receipts/log-r79-outcome-lines.txt`) still reads "both are refused". The receipts say both kill rules fired (`receipts/r79-selfcheck2-duplicate116-head.txt` line 6 `SELFCHECK2=PASS unresolved=0/3`; `corpus/evidence/round79/selfcheck-v2.py:146` `out[current] = [line]`, inside `def criteria` at line 139). The round-78 newer-block form was refused (`receipts/r79-selfcheck-control-before.txt`: `window v2 rc=1`), which is why the sentence reads as it does.
- Draft §2a is the correction entry, naming `SELFCHECK2=PASS unresolved=0/3` and the duplicate-116 window.

**F9 — routed defects 3 and 5 are landed; the draft keeps only the record and the line numbers.**
- Defect 3: `corpus/lessons/round-79-erratum.md` item 1 names `acca24498b8259d179db144a8bb2d44c0935e2c1`. The placeholder is real: `grep -n LANDING .ufo/reports/round-79/chousa.md` → `6:` and `119:` (`receipts/landing-placeholder.txt`; the report lives in the fleet repo). `git cat-file -t acca2449…` in the lane → `commit`.
- Defect 5: the mislabelled heading is `## Round-80 addition (criteria 1–149 unchanged)` at `corpus/QUALITY.md:1063` (introduced by `acca2449`; `git show acca2449:corpus/QUALITY.md | grep -n '^## '` ). The round-79 heading is at line 1060. The landed `## Round-80 landing` heading is at **line 1069** (not 1071: `git show HEAD:corpus/QUALITY.md | grep -n '^## Round-80 landing'` → `1069`), with 152 at 1071, 153 at 1072, 154 at 1073 (`receipts/landed-152-154.txt`). The draft's record sentence (§2c) is the lesson text.

**F10 — considerthese pick: proposal 4, one independent CJK quote spot-check per review.**
- The newest file is `considerthese/2026-10-26.md` (`ls considerthese/` ends at `2026-10-26.md`). Four proposals, lines 41–44.
- Not picked: 1 (stable ids; bookkeeping, no contact with C1/C2); 2 (streaks, already implemented in `corpus/evidence/round53/recurring.tsv`, `round55/recurring.tsv`, `round62/recurring.tsv`, `RW-4 … rounds 49-62`); 3 (lane-vs-verifier list, partly covered by QUALITY 14 "Spot-check intake"; one pick only).
- Picked: 4. It is still not a standing rule: QUALITY's CJK mentions are criteria 79 (lines 835–840), 95 (933) and 109 (960), all tool or table rules (`receipts/cjk-and-spans.txt`). The round-51 closure did the practice (`corpus/lessons/round-51-verifier-spotcheck.md` lines 86–87; `grep -cE 'spans/|spans\.tsv|qcache'` → `4`). The round-79 window adds zero CJK rows (`git diff ee70e6df acca2449 -- corpus/SOURCES.md | grep -cP '^\+\|.*[\x{3040}-\x{30ff}\x{4e00}-\x{9fff}]'` → `0`, `receipts/sweeps-r80.txt` sweep 4).
- It fits the round: `wc -w` on a CJK span line gives `2` for `69` characters (`corpus/evidence/round51/spans/S107-1.txt` line 5, `receipts/cjk-and-spans.txt`), so 154's word count cannot count a CJK quote. Draft line: QUALITY 156 (§4).

## Mistakes (for the lesson table; full rows and fixes in draft §1)

M1 provider quota exhaustion · M2 claims committed without a wave spec · M3 control receipt with its exit outside the bytes · M4 `/tmp` scratch · M5 caught by the round's own `oracle-check.py` (round-79 battery) · M6 claims count not re-opened by any counter.

## Limits and disclosures

- **Stray write, cleaned.** My first `_write` used a relative path and landed `draft-lesson.md` under the fleet root's `.ufo/waves/round-80/w1/R80ScribeB/`. I rewrote it at the lane path and removed the fleet copy and its directory. The fleet `w1/` directory pre-dates my write (`stat -c '%w'` → `2026-11-04 04:45:47 -0300`) and is now empty; I left it.
- **Mis-measurement, kept.** `receipts/draft-155-and-claims-check-head.txt` reports `29` for the S200 span. That is my regex capturing the title cell; the correct count is `20` (`receipts/placeholders-and-parse.txt`).
- **Sweep 3 exit.** The `# exit:` line in `sweeps-r80.txt` sweep 3 is `head`'s status; the empty output is the observed result.
- **Revisions moved.** Pins are in each command. The landed erratum and criteria 152–154 are read at `5ba30d87`.
- **Not run.** I did not run the battery or the oracle check (`matrix-battery-v7.py`, `oracle-check.py`). The gate-grounding counter ran read-only at `b7803829` (reproduced the before receipt: non-`#` lines identical, `receipts/gate-grounding-base-repro.txt`) and at `44d09edf` (PASS, `receipts/gate-grounding-head.txt`).
- **Tools.** No tool installed or updated; nothing under `~/.local/bin` changed.
- **Scratch.** `/fast/scratch/hyaku/chousa-r80/R80ScribeB` was created for the criterion test and removed (`rm -rf` → `ls -d` → `No such file or directory`, rc 2). No `/tmp` path was written. The located-quote script is kept in `receipts/`.
- **Writes.** Only under `.ufo/waves/round-80/w1/R80ScribeB/` and this report. No edits to frozen artifacts, to `LOG.md`, `QUALITY.md`, `SOURCES.md`, `SCORECARD.md`, `MANIFEST.json`, the fleet repo, `scripts/` or `.ufo/state`. No commits, no pushes.

## What the L1 must do with this draft

1. Land the LOG correction (draft §2a) as an appended entry; the erratum's item 2 currently points at an entry that does not exist.
2. Decide the revision-key rule (`REV=` as assigned, or `LANE_REV=` as 153 landed); append criterion 155 under `## Round-80 landing` if the strict rule stands. Its check's red-before is the 8/8 output.
3. Append the S200 count correction row (§2d). Do not amend `claims.md`.
4. Land criterion 156 (CJK spot-check) only with the L1's own check output; the round-51 diff-form was not measured here.
5. Record the attempt-1 mechanics in the lesson as observed: `> file 2>&1; echo "EXIT=$?"`, not `tee`.
6. Before close, run the M-checks in draft §1 once at the landing revision and paste their output. This seat did not verify the lane's own checks; the M-check outputs above are the observations.
