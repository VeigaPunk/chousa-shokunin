# Round 80 — draft lesson material (seat R80ScribeB; draft only, the L1 lands it)

Lane `chousa`. Base `b7803829922770b890e9f4efdd30d12c3695439a`. The lane tip moved during this read:
`0d253c95` (claims freeze, 23:08 -0300) → `44d09edfc20dba26ee8d58a93d365989916a2692` (attempt-2 landing,
23:58 -0300; `git log --oneline 0d253c95..44d09edf` shows the register/controls commit) → `5ba30d87172e94dd76a49e1a94294561e90f6cbd`
(`git rev-parse HEAD` at 00:06 -0300, after the L1 landed QUALITY 152–154, the round-79 erratum and the after receipt).
Each command below names the revision it ran at. Receipts are byte copies in `receipts/` of this folder; the index is §5.

## 0. Already landed at `5ba30d87` — do not re-land

| routed defect (round-79 closure §5) | state at `5ba30d87` | evidence |
|---|---|---|
| 1 — S196/S197/S198 record defects | landed: rows S200–S202 `supersedes S196/S197/S198`, `GATE-RECORD` lines (words 20/25/2), counter PASS | `receipts/gate-grounding-head.txt` last line `GATE_GROUNDING=PASS unresolved=0 superseded_resolved=3 audited=S199,S200,S201,S202` (at 44d09edf). Residual: claims.md count, see M6 |
| 2 — landing receipt untracked | landed, but inside the attempt-1 preservation commit | `git log --oneline -- corpus/evidence/round79/controls/selfcheck2-after-landing.txt` → `0f59b985 chousa r80: preserve in-flight work at hyaku run-15 wrap-up (L1 died on provider failure; not a landed round)` (`receipts/probes-r80.txt`) |
| 3 — report `LANDING` placeholder | landed as erratum item 1 in `corpus/lessons/round-79-erratum.md`, naming `acca24498b8259d179db144a8bb2d44c0935e2c1` | the placeholder is real: `grep -n LANDING .ufo/reports/round-79/chousa.md` → `6: … landing commit \`LANDING\`.` and `119: … \`LANDING\` |` (`receipts/landing-placeholder.txt`); `git cat-file -t acca2449…` in the lane → `commit` (same file) |
| 4 — LOG §Round 79 contradicts the receipt | **NOT landed.** The erratum (item 2) says the correction is "appended to `LOG.md` as a named correction entry (§Round 80's 'Correction to the round-79 entry')". No such entry exists | `git show HEAD:LOG.md \| grep -c 'Correction to the round-79 entry'` → `0`, exit 1 (`receipts/draft-155-and-claims-check-head.txt`). The LOG's last heading is `## Round 79 …` at line 2271 (`grep -n '^## ' LOG.md \| tail -1`). §2a is still needed |
| 5 — QUALITY 150–151 under `## Round-80 addition` | landed: new heading `## Round-80 landing` at `corpus/QUALITY.md:1069` records the mislabel; erratum item 3 | `git show HEAD:corpus/QUALITY.md \| sed -n '1069p' \| cut -c1-200` → `## Round-80 landing (criteria 1–151 unchanged; the block above headed "Round-80 addition" is a round-79 mislabel …` |
| 6 — control revision binding | landed as criterion 153 (`LANE_REV=` accepted) and 154 (located quote); the 153 check, run at HEAD, names two receipts with no revision at all | `grep -L 'REV=[0-9a-f]\{40\}\|LANE_REV=[0-9a-f]\{40\}' corpus/evidence/round80/controls/*.txt` → `oracle-before-r80.txt`, `oracle-structure-v6-accepted.txt` (`receipts/landed-153-check-head.txt`). Criterion 153's text does not say whether a non-empty list is a pass, so the check is ambiguous as landed. §3 |

## 1. `## Mistakes` (round 80)

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| M1 — provider quota exhaustion ended attempt 1; no report, no landed round | ChousaR80 transcript (`~/.omp/agent/sessions/-Projects-shokunin/2026-11-03T17-37-19-922Z_01a1a27c-a432-71e1-944b-0900e4e7a66b/ChousaR80.jsonl`), last assistant message `stopReason":"error"` at `2026-11-05T01:31:10.428Z`, `errorMessage` `Devin stream error failed_precondition: Your weekly usage quota has been exhausted` (`receipts/attempt1-transcript-facts.txt` line 4); watchdog `2635 … lane-dead-no-report chousa round=80 …` (`receipts/watchdog-round80-attempt1.txt`) | the watchdog, as `lane-dead-no-report` / `FAIL report_of`; the cause was in the transcript only | the death line carries the transcript's last `errorMessage` before any retry. Check that can fail: M1-C1 below (today 0 matches) |
| M2 — claims, instruments and census committed 53 min 53 s before any wave spec, so the freeze names no wave | `receipts/commit-timeline-r80.txt`: `0f59b985 2026-11-04 22:14:33 -0300 w1-spec-files=0 claims-files=1` and `0d253c95 2026-11-04 23:08:26 -0300 w1-spec-files=1 claims-files=0`; `0f59b985` message "preserve in-flight work at hyaku run-15 wrap-up (L1 died on provider failure; not a landed round)" | nothing at commit time; `claims.md` header says "frozen … at the claims-freeze commit named in the round report", and no commit is named | a claims-freeze commit lists its wave spec. Check that can fail: M2-C1 (0f59b985 → 0, fails; 0d253c95 → 1) |
| M3 — control receipt without its exit status or revision in its own bytes; the exit went to the transcript | transcript: `python3 -B corpus/evidence/round80/matrix-battery-v7.py … --work /fast/scratch/hyaku/chousa-r80/l1/v7-test2 … > /fast/scratch/hyaku/chousa-r80/l1/v7-legit2.txt 2>&1; echo \"EXIT=$?\"` then `cp` into `controls/v7-legit-matrix-after.txt` (`receipts/attempt1-transcript-facts.txt` line 2). Bytes: `# exit:` 0, `REV=` 0, `LANE_REV=` 1, first line `MATRIX_PATH=` (`receipts/sweeps-r80.txt` sweep 2). The transcript has no `\| tee` (`receipts/tee-contexts.txt` has no match lines), so "tee'd" is not what happened: the defect is the same class (exit status outside the bytes). The planned `--rev` landing re-measure never ran (no `controls/v7-legit-matrix-landing.txt` at HEAD). Two header commands carry a placeholder: `--work <scratch>` (`oracle-structure-v6-accepted.txt`) and `--work DIR` (`v7-legit-matrix-prefreeze.txt`) | 153 does not test exit lines; `v7-legit-matrix-after.txt` passes 153 (absent from its output in `receipts/landed-153-check-head.txt`) | §3 criterion 155 check: every control has `# command:`, `# exit:` and `REV=`; at `5ba30d87` it prints 8 of 8 UNSTAMPED (`receipts/draft-155-and-claims-check-head.txt`). `<scratch>` in a header fails to parse: `sh -c 'echo x --work <scratch>'` → `syntax error near unexpected token newline`, exit 2 (`receipts/placeholders-and-parse.txt`) |
| M4 — scratch outside `$HYAKU_SCRATCH` | `HYAKU_SCRATCH` unset in this seat's environment (`echo "HYAKU_SCRATCH=${HYAKU_SCRATCH:-<unset>}"` → `<unset>`); `/tmp/r80-base` is a non-git copy (`drwxr-xr-x 8 vgpnk vgpnk 4096 Nov 4 05:16`; `git -C /tmp/r80-base rev-parse HEAD` → `fatal: not a git repository`, exit 128; `receipts/probes-r80.txt`); `find /tmp -maxdepth 1 -name '*r80*'` lists 20 paths from several lanes (`receipts/tmp-r80-leftovers.txt`). Ownership of each path is not established; attributing `/tmp/r80-base` to attempt 1 is [INFERENCE] | `build_spec.py:181` scans committed round-80 evidence and `census-start.txt` for `/tmp/`; the committed tree has none (`receipts/sweeps-r80.txt` sweep 3, empty output). An uncited scratch path is outside that scan | M4-C1 below: 20 at close, must be 0 |
| M5 — caught by the round's own instrument: the round-79 battery printed `BATTERY=PASS` while accepting the subject-identity oracle | `controls/oracle-structure-v6-accepted.txt`: `BATTERY_EXIT=0 BATTERY_VERDICT=PASS RECEIPT_LINES=113`, `ORACLE=ACCEPTED`, `# exit: 1` (`receipts/oracle-structure-v6-accepted.txt`) | `corpus/evidence/round80/oracle-check.py` (exit 1 on `ACCEPTED`) | v7 adds the oracle table: `controls/v7-legit-matrix-after.txt:178` `ORACLE structure-identity REJECTED positive=0/2 forger=0/11 fresh_positive=0/2 fresh_forger=0/2`. The check can fail: the v6 control exits 1 on the same oracle (M5-C1) |
| M6 — not caught by any round instrument: the frozen claims file states a count the record contradicts | `corpus/evidence/round80/claims.md:90` "the corrected 15-word located quote that supersedes S196"; S200 quote is 20 words: `corpus/SOURCES.md:212` teaches span, `printf … \| wc -w` → `20` (`receipts/placeholders-and-parse.txt`); lesson `GATE-RECORD S200 … words=20` (`receipts/draft-155-and-claims-check-head.txt`); counter at 44d09edf `ROW S200 record=ok quote_words=20 … verdict=OK` (`receipts/gate-grounding-head.txt`) | this seat only (`receipts/criterion-located-quote-tests.txt` T3, `WORDS=20`). No round counter reads `claims.md` | M6-C1 below; claims.md is frozen, so the lesson carries the correction as an append-only row (§2d) |

**Sweep that found no further round-80 mistakes (pasted, so the absence is checkable):** instrument hashes
match `claims.md` 7 of 7 (`receipts/sweeps-r80.txt` sweep 1); no `/tmp/` path in committed round-80 evidence
(sweep 3); no CJK-quoting `SOURCES.md` row added by round 79 (sweep 4 → `0`); the gate-grounding counter
reproduces its committed before-receipt at base `b7803829` (`receipts/gate-grounding-base-repro.txt` against
`corpus/evidence/round80/controls/grounding-before.txt`: non-`#` lines identical, `diff` exit 0).

### Checks named in the Fix column (each can fail; output at the stated revision)

```
# M1-C1: retry log must carry the provider cause (fails today)
grep -ci quota /home/vgpnk/Projects/shokunin/.ufo/watchdog.log   # restrict to round=80 lines
# → 0 (receipts/watchdog-round80-attempt1.txt), exit 1: no provider cause recorded

# M2-C1: a claims-freeze commit lists its wave spec
git show --name-only --format= 0f59b985 | grep -c 'w1-spec.json'   # → 0  (fails)
git show --name-only --format= 0d253c95 | grep -c 'w1-spec.json'   # → 1  (passes)

# M4-C1: no scratch under /tmp at round close
find /tmp -maxdepth 1 -name '*r80*' | wc -l    # → 20 (fails; receipts/tmp-r80-leftovers.txt)

# M5-C1: the oracle check must exit 0 with ORACLE=REJECTED
python3 -B corpus/evidence/round80/oracle-check.py --battery corpus/evidence/round79/matrix-battery-v6.py --oracle .ufo/waves/round-79/w1/R79ExecC/matrix-structure-identity.py --work <fresh-dir> --runs 1
# → ORACLE=ACCEPTED, exit 1 on v6 (receipts/oracle-structure-v6-accepted.txt); a v7 receipt must show ORACLE structure-identity REJECTED

# M6-C1: a count the frozen claims file states must equal the count of its GATE-RECORD
grep -oE '[0-9]+-word' corpus/evidence/round80/claims.md | sed -n '2p'     # → 15-word (claims.md:90)
git show HEAD:corpus/lessons/round-80.md | grep -oE 'GATE-RECORD S200 .* words=[0-9]+' | grep -oE 'words=[0-9]+'   # → words=20
# 15 ≠ 20 → fails
```

## 2. Append-only correction texts

### 2a. Routed defect 4 — `LOG.md` §Round 79 (NOT landed; the erratum's claim is false)

Evidence the sentence is wrong: `sed -n '2307p;2310,2311p' LOG.md` (`receipts/log-r79-outcome-lines.txt`) reads
"both frozen predicates hold on the committed bytes" … "C2's kill rule names the hollow repair and the
newer-block window; both are refused." The receipts say the kill rules fired:
`.ufo/waves/round-79/w1/R79CriticA/selfcheck2-duplicate116-head.txt` line 6 `SELFCHECK2=PASS unresolved=0/3`
(`receipts/r79-selfcheck2-duplicate116-head.txt`), and `corpus/evidence/round79/selfcheck-v2.py:146`
`out[current] = [line]` inside `def criteria` at line 139 (`sed -n '146p' corpus/evidence/round79/selfcheck-v2.py` → `out[current] = [line]`).
The round-78 newer-block form *is* refused (`receipts/r79-selfcheck-control-before.txt`: `window v2 rc=1 SELFCHECK2=FAIL unresolved=3/3`;
`CONTROL=PASS cases=4 v1_false_greens=2/2 v2_refusals=2/2`), which is why the LOG sentence reads as it does.

Correction entry (append to `LOG.md` after the Round 79 entry; do not edit the entry above it):

```
## Round 79 correction (appended in round 80; the §Round 79 entry above is unedited)

Corrects the Outcome bullet of §Round 79 (LOG.md lines 2307–2311). That bullet says both frozen kill
rules were refused. Both fired.

- C2 (calibration). The round-78 newer-block form was refused (`selfcheck-control-before.txt`:
  `window v2 rc=1`). The duplicate-number form was not: a newer `## Round-<n> addition` block that re-uses
  criterion number `116.` makes the round-79 counter print `SELFCHECK2=PASS unresolved=0/3` at exit 0
  (`.ufo/waves/round-79/w1/R79CriticA/selfcheck2-duplicate116-head.txt`, line 6) while criterion 116's
  dead pointer stays live, because `criteria()` writes `out[current] = [line]` (`corpus/evidence/round79/selfcheck-v2.py:146`)
  and overwrites the earlier body. The kill rule fired. Routed to QUALITY 150 (landed at `5ba30d87`).
- C1 (operability). The payload-decoding forger `.ufo/waves/round-79/w1/R79CriticA/a10-payload-decode.py`
  reached `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` at exit 0 without scoring a
  subject. The kill rule's universal clause ("if any forger is FORGED") counted six forgers and fired on
  a seventh. Routed to QUALITY 151 (landed at `5ba30d87`).

Sources: `corpus/lessons/round-79.md` §Claim outcomes ("both frozen kill rules fired") and
`corpus/lessons/round-79-verifier-spotcheck.md` §2.
```

### 2b. Routed defect 3 — the `LANDING` erratum (already landed; no second erratum needed)

Landed as `corpus/lessons/round-79-erratum.md` item 1. The substance is verified: the placeholder lines
(`receipts/landing-placeholder.txt`) and the hash `acca24498b8259d179db144a8bb2d44c0935e2c1` resolving as
a commit in the lane (`git cat-file -t` → `commit`). The report bytes stay as filed in the fleet repo.

### 2c. Routed defect 5 — record sentence for the lesson

> Record (round 80). QUALITY criteria 150 and 151 are round-79 wave findings: `git log -S'150. **A counter' --oneline -- corpus/QUALITY.md`
> → `acca2449 round-79: land the wave, the honest claim outcomes, QUALITY 150-151, the lesson and the verdict rows`,
> and their evidence paths name `.ufo/waves/round-79/w1/` (`sed -n '1065p;1067p' corpus/QUALITY.md | grep -o '\.ufo/waves/round-79/w1/[A-Za-z0-9_./-]*'`).
> They were filed under `## Round-80 addition (criteria 1–149 unchanged)`, a heading `acca2449` introduced at
> `corpus/QUALITY.md:1063`, with the round-79 heading at line 1060. The round of record for 150–151 is 79. The
> heading is not moved (append-only); the round-80 criteria 152–154 sit under `## Round-80 landing` at line 1069.

### 2d. Frozen-claims count (M6) — append-only row for the lesson

> Correction (round 80). `corpus/evidence/round80/claims.md:90` states the S200 located quote as "15-word". The
> S200 quote is 20 words: `printf '%s' '<quote>' | wc -w` → `20`, `corpus/SOURCES.md:212` teaches span, and the lesson's
> `GATE-RECORD S200 … words=20`. The frozen file is not amended; this row governs the count.

## 3. QUALITY — criteria 153/154 landed; the draft below is 155 (no number collision)

Criterion 152 is the number this seat was given for the defect-6 draft and it is already taken by a landed
criterion, so the draft is 155. What 153 and 154 leave open, measured at `5ba30d87`:

- **No exit line.** 153 names revisions; it does not require `# exit:`. `v7-legit-matrix-after.txt` and
  `v7-legit-matrix-prefreeze.txt` have no exit line and pass 153 (`receipts/landed-153-check-head.txt`, second block: exit trailer absent in exactly those two).
- **`LANE_REV=` versus `REV=`.** The assignment that this draft implements asks for `REV=<40-hex>`; 153 accepts
  `LANE_REV=`. Strict `REV=` on all eight control receipts: no match (`grep -l '^REV=\|[^_A-Z]REV=[0-9a-f]\{40\}'` → none, exit 1).
  The L1 chooses which rule stands; this draft states the strict one.
- **CJK counts.** 154 counts by `len(quote.split())`, which is `wc -w`. On a 69-character Japanese span line `wc -w` → `2`
  (`receipts/cjk-and-spans.txt`). A CJK located quote is not counted.
- **Claims counts** are not re-opened by 154 (M6-C1).

Draft criterion 155 (append after 154 under `## Round-80 landing`):

> 155. **A control receipt is self-describing: its own bytes carry its command, an exit status and the revision it was measured at as `REV=<40-hex>`, and a count that a frozen claims file states must equal the count of the record that cites it.** Round 80's attempt-1 receipts `controls/v7-legit-matrix-after.txt` and `…-prefreeze.txt` carry no `# exit:` line (the exit was echoed to the transcript, not written to the file), and no round-80 receipt carries `REV=`; `LANE_REV=` is the only revision key. `claims.md:90` states "15-word" for S200; the record and `wc -w` say 20. Check (prospective: applies to receipts created after this criterion lands; the round-80 receipts are the red-before):
>
> ```
> for f in corpus/evidence/round80/controls/*.txt; do
>   ok=1
>   grep -q '^# command:' "$f" || ok=0
>   grep -q '^# exit: [0-9]' "$f" || ok=0
>   grep -qE '(^|[^A-Z_])REV=[0-9a-f]{40}' "$f" || ok=0
>   [ $ok -eq 1 ] && echo "STAMPED $f" || echo "UNSTAMPED $f"
> done
> ```
>
> At `5ba30d87` this prints `UNSTAMPED` for all eight round-80 control receipts (`receipts/draft-155-and-claims-check-head.txt`; the loop's own exit is 0, so the auditor reads the words, not the status). Shown able to fail: 8/8. The pass branch is not exercised by any committed receipt, and this seat did not build one; recorded, not claimed. Limit: the check tests presence of the three lines, not that the `REV=` value is the revision the command ran at.

## 4. `considerthese/` proposal mined — one pick

Newest file: `considerthese/2026-10-26.md` (`ls considerthese/` → `2026-10-19.md` … `2026-10-26.md`; no later file). Four self-improvement proposals (`grep -n '^- \*\*' considerthese/2026-10-26.md`, lines 41–44).

| # | proposal | still unimplemented? | fits round 80? | pick |
|---|---|---|---|---|
| 1 | stable ids `CT-20261026-1` | yes: `grep -c 'CT-' considerthese/*.md` → only the example in 2026-10-26.md | no: bookkeeping of the daily file; no C1/C2 contact | no |
| 2 | track recurring weaknesses as streaks | **implemented**: `corpus/evidence/round53/recurring.tsv`, `round55/recurring.tsv`, `round62/recurring.tsv` carry `RW-n` rows with round ranges (`RW-4 … rounds 49-62`, `round62/recurring.tsv` line 1) | — | no |
| 3 | report where the lane and the verifier disagree | partly: QUALITY 14 "Spot-check intake" is the lane-side debt intake; no axis-verdict gap list exists | yes, but one pick only | no |
| 4 | one independent CJK quote spot-check per review | **still open as a standing rule**: QUALITY names CJK only in criteria 79 (lines 835–840), 95 (line 933) and 109 (line 960), all tool or table rules; round 51's closure did the practice (`corpus/lessons/round-51-verifier-spotcheck.md` lines 86–87, S107–S112 re-opened from `spans.tsv`/qcache); round 79's closure has zero span references and zero CJK rows added (sweep 4) | yes: 154's `wc -w` cannot count CJK (below) | **yes** |

**Grounding for pick 4 (opened the repo bytes it points at):**

- Span files exist: `ls corpus/evidence/round51/spans | wc -l` → `70` (`receipts/cjk-and-spans.txt`).
- The `wc -w` gap: `corpus/evidence/round51/spans/S107-1.txt` line 5 → `wc -w` `2`, `wc -m` `69` (`receipts/cjk-and-spans.txt`).
- CJK rows: `grep -cP '^\| *S1(0[4-9]|1[0-2]) \|.*[\x{3040}-\x{30ff}\x{4e00}-\x{9fff}]' corpus/SOURCES.md` → `9` (S104–S112, round 51).
- Round-51 closure span references: `grep -cE 'spans/|spans\.tsv|qcache' corpus/lessons/round-51-verifier-spotcheck.md` → `4`.
- Round-79 window: `git diff ee70e6df acca2449 -- corpus/SOURCES.md | grep -cP '^\+\|.*[\x{3040}-\x{30ff}\x{4e00}-\x{9fff}]'` → `0`, so the rule is not applicable there (sweep 4).

Draft line that this would land as — QUALITY 156 (under `## Round-80 landing`):

> 156. **A non-author closure whose round adds a registry row with CJK quote text re-opens at least one such quote in its committed span file and counts it by criterion 79's convention (four CJK characters count as two words), not by `wc -w`.** Check: `git diff <base> <tip> -- corpus/SOURCES.md | grep -cP '^\+\|.*[\x{3040}-\x{30ff}\x{4e00}-\x{9fff}]'` ≥ 1 implies `grep -cE 'spans/|spans\.tsv|qcache' corpus/lessons/round-<N>-verifier-spotcheck.md` ≥ 1. Round 79: first command 0, so not applicable. Round 51's base–tip diff was not measured here (`9` CJK rows at tip, `4` span references), so this seat does not claim the round-51 rule passes in the diff form. Limit: a reference is checked, not the agreement of the re-open.

## 5. Receipt index (all in `receipts/`)

| file | what it shows (command in its header or in §1–§4) |
|---|---|
| `grounding-before.txt`, `grounding-before-r80.txt`, `grounding-after.txt`, `oracle-structure-v6-accepted.txt`, `oracle-before-r80.txt`, `v7-legit-matrix-prefreeze.txt`, `v7-legit-matrix-after.txt`, `v7-legit-matrix-r80.txt` | copies of the round-80 control receipts as committed at `5ba30d87` |
| `claims.md`, `selfcheck2-before.txt`, `selfcheck2-after.txt`, `selfcheck2-after-landing.txt` | the frozen claims and round-79 counter receipts |
| `r79-selfcheck-control-before.txt`, `r79-selfcheck2-duplicate116-head.txt` | round-79 control and duplicate-116 receipt (2a) |
| `sweeps-r80.txt` | sweeps 1–5: hashes, receipt shape, `/tmp` grep, CJK rows, count pair |
| `commit-timeline-r80.txt`, `probes-r80.txt`, `tmp-r80-leftovers.txt`, `watchdog-round80-attempt1.txt`, `attempt1-transcript-facts.txt`, `tee-contexts.txt`, `placeholders-and-parse.txt` | M1–M4 and M3 detail |
| `landing-placeholder.txt`, `log-r79-outcome-lines.txt` | defects 3 and 4 |
| `landed-152-154.txt`, `landed-153-check-head.txt`, `span-lines-154.txt`, `draft-155-and-claims-check-head.txt` | landed criteria, the 153 check, span counts, the 155 draft check. `draft-155-and-claims-check-head.txt` also contains one mis-measurement (`S200 teaches span words … 29`, a regex error that captured the title cell); the correct count, 20, is in `placeholders-and-parse.txt` |
| `criterion-located-quote-tests.txt`, `located-quote-check.sh` | the located-quote script and its six test cases (T1 13-word PASS, T2 27-word FAIL, T3 20-word PASS, T4 25-word PASS, T5 no-REV FAIL, T6 wrong-line FAIL) |
| `gate-grounding-head.txt`, `gate-grounding-base-repro.txt`, `gate-record-lines-head.txt` | counter at 44d09edf (PASS), base reproduction (FAIL, matches control), GATE-RECORD lines |
| `cjk-and-spans.txt` | `wc -w`/`wc -m` on a CJK span line; round-51 span references; CJK row count; QUALITY CJK mentions; proposal 4 text |
| `landed-152-154.txt` | full text of QUALITY 153 and 154 (line 1072, 1073) as landed at `5ba30d87` |

Measurement notes: sweep 3's `# exit:` line reports `head`'s status, not `grep`'s; its output is empty, which is the observed result.
