# Recurring frozen-counter weaknesses, rounds 49-60 (lesson draft)

Source: considerthese 2026-10-26, proposal 2 ("Track recurring weaknesses as streaks"). This proposal is already implemented in round 53 as `corpus/evidence/round53/weakness-streak.py` with `recurring.tsv` (`corpus/lessons/round-53.md:78`, `LOG.md:1850`, `SKILL.md:138`). Round 61 has no closure lesson yet; its row shows only the frozen controls.

The implemented tool does not pass on this tree. Run read-only, `python3 -B corpus/evidence/round53/weakness-streak.py --root . --table corpus/evidence/round53/recurring.tsv` prints `RW-1 streak=12 claimed=5` and `RW-3 streak=0 claimed=2`, `WEAKNESS_ROWS=2 FAILING=2`, exit 1. Its regex counts mentions, not weaknesses, and its claimed column is typed by hand. The table below is classed and does not depend on the regex.

Classes: **F** a forge or replay passes the frozen counter. **M** the frozen gate misses a mutant or a hook class. **U** a correct output cannot reach the target. **T** a do-nothing builder reaches the target. **P** the claims were not frozen before dispatch.

| Round | Class | Weakness | Evidence (path:line; all opened) | Red-before fix landed? |
|---|---|---|---|---|
| 49 | F | C1 passes a replay of the tool's outputs (W1 `CritForgeC1`) | `corpus/lessons/round-49-verifier-spotcheck.md:45` | No. Named limit only (QUALITY 72). |
| 50 | F | A 42-line forge passes the frozen C1 at `LEGS=5/5` | `corpus/lessons/round-50-verifier-spotcheck.md:38`; `:36` (supplement: real 5/5, forge 1/5, base 1/5, constant 0/5) | Partial. Post-freeze supplement with red controls. Frozen counter unchanged. |
| 51 | F | A 94-line tool keyed on fixed directory names passes `LEGS=5/5` | `.ufo/reports/round-51/chousa.md:13` (fleet repo); `corpus/lessons/round-51-verifier-spotcheck.md:38`, `:100` | Partial. Random-name supplement: dirname forge 1/10 (`:38`). Frozen counter not replaced (`:100`). |
| 52 | F | Representation forge (XML spelling) passes frozen 9/9. The supplement scores the same forge 0/4 | `corpus/lessons/round-52-verifier-spotcheck.md:34`, `:94`; `corpus/evidence/round52/measure-after.txt:74`, `:88` | Partial. Supplement red (0/4). Frozen counter not changed (`:94` routed). |
| 53 | F | A 189-line forge passes frozen 8/8, canning REAL on the pinned digest | `.ufo/waves/round-53/w1/R53CritForgeC1.md:13`; `corpus/lessons/round-53-verifier-spotcheck.md:27`, `:83` | No receipted red. Supplement forge 1/3 is assertion-only (`:27`). |
| 54 | F | Forge passes frozen 6/6 twice. A 20-line tool that never opens the `.doc` scores 3/3 on the supplement | `corpus/evidence/round54/controls/c1-forge.txt` (`LEGS=6/6 C1=PASS`); `corpus/lessons/round-54-verifier-spotcheck.md:44`, `:56`, `:130` | No. Routed (`:130`: needs an inspection-independent leg). |
| 55 | F, M | Frozen counter: 9 of 9 mutants survive (NO_SLICE ... NO_ORACLE_SHA). Hook is not a complete boundary | `.ufo/waves/round-55/w1/R55MutC1Counter.md:39-47`, `:86`; `corpus/lessons/round-55-verifier-spotcheck.md:48`, `:119` | Yes, for the mutants. Round-56 counter: `KILLED=1/9` (`corpus/evidence/round56/controls/c1-before.txt:21`) then `KILLED=9/9` (`corpus/evidence/round56/c1-measure-after.txt:28`, `:57`). |
| 56 | M | Residual: `dir_fd` without `chdir` and native `import` unprobed. Three C1 attacks did not measure (capture cache deleted, `ENV_CHANGED`) | `corpus/lessons/round-56-verifier-spotcheck.md:13`, `:36`, `:107` | Partial. Clause kills landed (row 55). Hook classes routed (`:107`). Attacks unrun (`:36`). |
| 57 | F | C3 provenance: a fabricated (id,url) success row plus replayed bytes reach `C3=PASS` (A1a, A1b) | `.ufo/waves/round-57/w2/R57W2CritC3Forge.md:22`, `:41`; `corpus/lessons/round-57-verifier-spotcheck.md:62`, `:98`; `corpus/evidence/round57/sidecar-audits.md:59` | No. Routed to a future re-freeze (`:98`). Committed state is genuine (`sidecar-audits.md:59`). |
| 58 | U | C1 refusal legs print lowercase `=pass` (`PASS = "pass"`, `c1-count.py:51`; legs at `:147`, `:223`, `:234`, `:315`), but the verdict tests `=PASS` (`:391`). Code-read, not run: a correct refusal cannot pass. C2 offset contradiction is lesson-only | `corpus/evidence/round58/c1-count.py:51`, `:223`, `:391`; `corpus/lessons/round-58-verifier-spotcheck.md:15`, `:36` | No. Routed (`:36`). The C2 half is not re-derived from `c2-count.py`. |
| 59 | P | No claims freeze before dispatch. `CLAIMS_EXISTS=False`, `ITEM_BODY_EQUAL=0` | `corpus/lessons/round-59-verifier-spotcheck.md:8`, `:41`; `LOG.md:1917-1921`; `corpus/QUALITY.md:978` (criterion 116) | Yes, as a process rule (QUALITY 116). Round 61 followed it: freeze `1661b85` precedes dispatch `9f32ac0` (`git log`). |
| 60 | T, P | A do-nothing builder reaches `C1=PASS` (W1 `BuildCounter`). The injection clause is a tautology. Frozen claim digest differs from the dispatched prompt | `.ufo/waves/round-60/w1/BuildCounter.md:102`, `:176`; `corpus/lessons/round-60-verifier-spotcheck.md:18`, `:44`; `.ufo/waves/round-60/c1-before.txt:6`; `.ufo/waves/round-60/c1-after.txt:2` | No. Routed (`:44`). Round-60 after-receipt still `C1=FAIL exit 1`. |
| 61 | none recorded yet | Controls at freeze. C1: base 7/20; no-op exit 0 1/20; exit 2 14/20; forge-token 7/20; naive guard 10/20; reference 20/20; M01-M14 each KILLED. C2 limit: an echo of the quote passes (`echo-claims`) | `corpus/evidence/round61/claims.md` (sha256 `9afec8d4...` matched); `corpus/evidence/round61/controls/c1-before.txt`, `c1-controls.txt`, `c2-controls.txt` | Pending. Red-before recorded at freeze. Landed builder absent: `git diff --stat 9eef15e7 HEAD -- tools/build-spans.py` prints nothing. |

## Streaks from the table

- Class F runs 49-55 consecutively (7 rounds). This matches `LOG.md:1871` ("RW-1 streak 7").
- Round 56 has an unmeasured F attempt (`:36`), not a survival. Round 57 recurs. Rounds 58-60 are not F. The F run ending at round 60 is 0.
- Red-before landed for: the round-55 mutants (round 56), and the freeze-before-dispatch rule (rounds 59-61). Partial for the supplements (rounds 50-54). Not landed for the frozen counters in rounds 49, 52-54, 57, 58, 60. Pending for round 61.

## Notes for the lane

1. Replace the regex in `recurring.tsv` with the class column above. `forg(e|ed|able|ery)` matches seat names, for example `CritForgeC1` at round-49 `:45`.
2. Compute the streak. Do not type it. The claimed `5` in `recurring.tsv` is the round-53 value; `LOG.md:1871` says 7 at round 55.
3. The registered gate (`SKILL.md:138`) exits 1 on this tree. Fix or re-register it before any round cites it as green.
4. Add a red-before column: the control that failed before the fix, and the receipt path that shows it.
