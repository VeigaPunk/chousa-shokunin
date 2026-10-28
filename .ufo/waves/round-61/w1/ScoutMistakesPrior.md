# ScoutMistakesPrior — rounds 58–60 mistakes

Lane HEAD `9f32ac055c591b17abf119aac30b202d6cd52a7e`. Classes are the CORPUS.md set (`vacuous`, `survivor`, `stale-premise`, `reference-drift`, `number-drift`, `scope`, `attribution`, `landing`, `provider`). Captured-by is a QUALITY criterion that already existed and whose check covers the defect. A criterion added in the lesson that records the defect is a sentence, not a capturer. `fixed_with_red_before` means one committed command that exits non-clean on the pre-fix bytes for the named reason, with the fix as the only delta. None of the twenty do. Round-61 `corpus/evidence/round61/controls/c1-controls.txt` was read, not re-run: noop `1/20`, forge-token `7/20`, reference `20/20`, `CONTROLS_UNEXPECTED=0`. That file is a new counter, not a patch of the round-58 or round-60 counters.

## Distinct mistakes

1. **vacuous** — Round-58 C1 emits `=pass(refused)` (`PASS = "pass"`, `corpus/evidence/round58/c1-count.py:51,160`) and `ref_pass` searches `=PASS` (`:391`). Seven honest refusals give `ref_pass` False, so `C1=PASS` is unreachable unless the leg text is forged. Captured-by: `none`. QUALITY 86 is the round-51 tokenizer control `build-c3-controls.py`; it does not run this counter. QUALITY 115 was added in `c9b08e9` with the lesson. Fix: sentence only. The counter still has this predicate. R59Executor09's case-fixed copy stayed in scratch.

2. **survivor** — The same test treats `=PASS` anywhere in the leg line as a pass. Fail-lines interpolate child stderr (`:152`, `:222-224`), so a hazard leg that failed still satisfies `ref_pass`. Captured-by: `none`. QUALITY 117 was added in `026174e` after the finding. Fix: sentence only. I executed the predicate (`stderr_forge_ref_pass True`). I did not re-run the 11-leg `spoof-builder.py` battery; R59Executor09 §6 records `C1=PASS` exit 0 on the frozen bytes.

3. **survivor** — `SYMLINK_OUT` appends `(target-dir-written!)` (`:232-236`). The verdict block (`:389-394`) does not read that marker, and the line still contains `=pass`. Captured-by: `none`. No QUALITY row names the suffix. Fix: sentence in the seat report only. R59Executor09 §3 got `C1=PASS` from a scratch case-fix while writing through the link; that copy is not in the tree.

4. **vacuous** — Round-58 C2 `CAPTURE_BIND` requires `occurrences[0]==off` (`c2-count.py:101`) and `REBUILD` requires byte-identical `tools/build-spans.py` output, which stores `str(start)` for `start=max(0, off-80)` (`:142,149`). First frozen quote in `capture-text` stdout: occurrence 315, start 235. Captured-by: `none`. Fix: sentence in the round-58 routed defect. `corpus/evidence/round58/c2/spans.tsv` is absent. R58ExecC2BuildSpans says its scratch patch was not applied.

5. **vacuous** — C2 `NEW_GROUND` greps U+8F09 `載体类型标识` and tests the entry for U+8F7D `载体类型标识` (`c2-count.py:153-154`). The claim's character cannot trip the grep. Captured-by: `none`. Fix: none. The two lines are unchanged.

6. **landing** — `corpus/evidence/round58/controls/build-spans-r55.py:41,57` imports `capture-text.py` from its own directory. That file is absent. Captured-by: `none`. Fix: none.

7. **landing** — No `corpus/evidence/round59/claims.md` in any commit. At `10b220f3` the directory holds census, quarantine, `s101-open.txt`, and `controls/c1-before.txt` only. Captured-by: `none`. QUALITY 116 was added in `026174e` after the miss. Fix: sentence. Nothing under `tools/` checks claims presence.

8. **landing** — Round-59 `w1-spec.json` mtime 2026-10-27T15:14:46, after `w1-dispatch.json` 15:12:11 and `w1.ready` 15:12:15. The spec `item` is a substring of the dispatched `task` for 0/66 names. R59Executor01's spec item is a handoff review; the launched task is the round-58 counter probe. Captured-by: `none`. QUALITY 118 was added after. Fix: sentence. The files still differ. No digest guard was added.

9. **scope** — Round-59 spec roles: executor 16, scribe 12, scout 12, reviewer 14, critic 7, mutation-tester 5, connector 0. Captured-by: `none`. Fix: sentence in the lesson settlement and the round-59 routed list.

10. **landing** — Round-59 `w1-results.json` row keys are `agent`, `name`, `note`, `output`. Empty output and empty note: R59Scout34, R59Scout36, R59Scout38, R59Scout40. Captured-by: `none`. Fix: sentence in the routed list. The file still has that shape.

11. **vacuous** — Committed round-60 `c1-count.py` (only commit `5d309d1`) scores a builder that prints `SPANS_ROWS=1` and `WRITTEN=1` and exits 0 as `CANDIDATE_REFUSAL=1/1`, `C1=PASS`, exit 0. That run also prints `INJECTION_REJECTED=1/1`. The return (`:41-43`) never yields `forged_safe`, so the flag cannot move. Captured-by: QUALITY 60 (cheapest full-marks gate) and QUALITY 56 (a fixture that cannot fire is not a measurement). Both predate the round. Fix: sentence. The lesson says no post-data fix. QUALITY.md has no Round-60 addition.

12. **reference-drift** — BuildCounter §2.2 records a `sys.exit(0)` noop and the counter's own `=PASS` stub as `C1=PASS` exit 0. Those two builders on the committed file print `C1=FAIL` exit 1. The committed return requires `valid_output`; BuildCounter's line table does not. Captured-by: QUALITY 58 (re-run the bytes the receipt cites). QUALITY 117 covers the wave-time stub-passes state; it does not fail the committed stub run. Fix: none. The lesson still states the wave-time noop pass.

13. **vacuous** — `python3 -B corpus/evidence/round60/c2-count.py` prints `C2=PASS` exit 0. `ENTRY` is the pre-existing `corpus/knowledge/citation-count-semantics-r37.md` (`c2-count.py:8`). `FORM` is `.ufo/waves/round-60/s101-open.txt` (`:7`). The lesson's path `corpus/evidence/round-60/s101-open.txt` is absent. `.ufo/waves/round-60/c2-before.txt` says the baseline must fail; the counter does not. Captured-by: QUALITY 60. Fix: sentence.

14. **landing** — `sha256sum corpus/evidence/round60-claims.md` is `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`. That path is absent at base `b379919a` and first appears at lesson commit `5d309d1`. `w1-spec.json` contains `09d8053f…` 64 times and the real digest 0 times. Captured-by: QUALITY 116 (record the artifact's full revision before ready). The criterion's own shown-failure is a missing file; this incident is a digest that is not the file, in a base revision that does not contain the file. Fix: sentence. No prompt-digest checker under `tools/`.

15. **landing** — `corpus/lessons/round-60.md` headings are Gate, Mistakes, Trends, Wave settlement. It has neither `## Sources & frontier` nor `## Trend verdicts`. The spot-check assigns that contract miss to the fleet report; that path is not in the lane tree at `5d309d1`, so I did not re-read it. Captured-by: `none`. Fix: sentence in the round-60 routed list.

16. **stale-premise** — First `S101` pickaxe on `corpus/SOURCES.md` is `1254ab2` (2026-10-25, round 49). Round 60 reopened that row. Captured-by: `none`. QUALITY 57 is met by the committed capture re-read and does not require a new row. Fix: sentence in the routed list.

17. **scope** — The round-60 Gate has no new source admit paired with a new reject. The spot-check agrees with the claim rejections and says the round-local sample is incomplete. Captured-by: `none`. Fix: sentence.

18. **vacuous** — The round-60 Gate says the synthetic indented assimilation-collision test was not independently proven. Captured-by: `none`. Fix: sentence. I did not re-run the collision lists.

19. **provider** — The round-58 spot-check says dispatch attempt 1 died and attempt 2 completed. Captured-by: `none`. Fix: sentence, routed to the operator. I did not re-run dispatch.

20. **scope** — The round-58 routed list told the next lesson to record the outside admit/reject. `corpus/lessons/round-59.md:32-33` does that in prose. Captured-by: `none`. Fix: sentence only.

The `## Mistakes` sections under-count this set. Round 58 has item 1 only. Round 59 has items 7, the bundle of 1 and 2, and 8. Round 60 has the wave-time form of 11–14 as two rows. Items 3–6, 9, 10, and 15–20 are in the spot-checks, the routed lists, or the seat reports those lessons cite.

## Evidence

Lane root for every command. Scratch `/fast/scratch/hyaku/chousa-r61/ScoutMistakesPrior` was created for the counter runs and removed in the same shell (`trap rm -rf`).

- Predicate execution on the round-58 constants: `FOREIGN=pass(refused)`; `honest_ref_pass False`; `stderr_forge_ref_pass True`; suffix contains `=pass` True; verdict slice contains `target-dir-written` False.
- `python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`: `capture_text_chars 27012`, first quote count 1, occ 315, builder_start 235, equal False.
- NEW_GROUND codepoints `U+8F09` versus `U+8F7D`. `controls/capture-text.py` printed `ABSENT`. `round58/c2/spans.tsv` absent.
- Round-60 C1, `--seed 6001`, fresh `--work`: `sys.exit(0)` → `C1=FAIL` exit 1; `=PASS` stub → `C1=FAIL` exit 1; `SPANS_ROWS=1` plus `WRITTEN=1` → `C1=PASS` exit 0. All three printed `INJECTION_REJECTED=1/1`.
- Round-60 C2: `RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1`, `C2=PASS`, exit 0. `ls` of `corpus/evidence/round-60/s101-open.txt`: No such file.
- `git cat-file -e b379919a873e7080a31ef92c7002f55f5374e2c6:corpus/evidence/round60-claims.md` → absent on that commit, present at `5d309d1`. sha256 `65721569…18d1`. Spec occurrences of `09d8053f…` = 64; of the real digest = 0.
- `git log -- corpus/evidence/round59/claims.md` printed nothing. Spec, dispatch, and ready mtimes are the three timestamps in item 8. Spec-item substring of dispatch task: 0/66. Connectors: 0. Empty result names: the four scouts in item 10.
- QUALITY introductions: 115 in `c9b08e9` (2026-10-27 14:59:26 -0300); 116, 117, and 118 in `026174e` (2026-10-27 15:46:41 -0300). No `Round-60 addition` in QUALITY.md.
- Search of `tools/` for `w1-spec`, `CLAIMS_EXISTS`, and `09d8053f`: no match.
- `git log --reverse -S S101 -- corpus/SOURCES.md` first hit `1254ab2` 2026-10-25, round 49.
- Lesson `##` lines: 6 Gate, 21 Mistakes, 26 Trends, 32 Wave settlement.

INFERENCE: the "shown able to fail" sentences in QUALITY 115–118 describe the unfixed run. They are not a red-before then green-after pair on a committed delta. I did not re-execute round-61 `c1-count.py`.

VERDICT: MISTAKES=20 uncaught=16 fixed_with_red_before=0
