# ScribeLogDraft — round 62, wave w1 (scribe)

Scope: draft the round-62 LOG entry, the SCORECARD round-62 verdict block and the corpus/README.md coverage row and Round62 frontier section, from the frozen facts only, with every measured after-value left as the literal marker `<AFTER>`. Output: `.ufo/waves/round-62/w1/ScribeLogDraft/draft.md`. No lane file was written; no counter, battery, probe or control was run; no git mutation; no fetch; no subagent.

## Findings

1. **The draft is complete as four paste sections plus L1 notes.** Section 1 LOG.md entry (append after line 1954), section 2 SCORECARD round-62 verdict (append after line 2963; the round-61 pattern is Planned-N, Verdict-N, Planned-(N+1)), section 3 README coverage row (insert above line 7), section 4 README `## Round62 coverage and frontier` (append after line 1296). Section 5 holds notes for L1 and is not for pasting. The operability score stays 3/10 in section 2, stated as unchanged, with no new score.
2. **Seat count conflict (must be resolved at integration).** The frozen claims text says "One v2 wave `w1`, 64 seats". The dispatch and spec carry 66: `w1-spec.json` has 66 items; `freeze-check-live.txt` reports `66 names match in order`; the dispatch commit `d173d14` is titled "validated v2, 66 seats". The draft uses `<AFTER>` for the settled count and states both figures. The claims file is frozen and was not edited.
3. **Lead id in the claims file is not what SOURCES.md records.** The claims say S138 "is the lead recorded in `corpus/SOURCES.md` `## Leads` by round 61". The Leads line (`corpus/SOURCES.md:326`) carries no id. The draft says the lead was unnumbered and is numbered at landing. This does not change the predicate, which only requires that the rows be present.
4. **Landing dependencies are absent from the tree.** `corpus/evidence/round62/` holds `c1v2-battery.py`, `c1v2-count.py`, `c2v2-count.py`, `claims.md` and `controls/`. The probe the entry rests on, `corpus/evidence/round62/openat2-probe.py` and its output `openat2-probe.txt`, is not there; only `controls/candidate-openat2-probe.py` and `.txt` exist. Registry rows S138–S140 are absent: `grep -c "^| S" corpus/SOURCES.md` prints 137, and the highest id is S137. Without the probe and the rows, `c2v2-count.py` cannot reach `C2=PASS`. This is a landing blocker for L1, not a draft issue.
5. **Id-reuse hazard, low severity.** `corpus/lessons/round-45.md:129-135` names "staged S139 → lane S082, S140 → lane S083" for a different document's renumber map. The registry has no collision. The draft tells readers to cite S138–S140 with the round-62 date.
6. **Frozen predicate text checked against the frozen controls (read-only).** Fixture quote Q6 reads "Block traversal through all symlinks (implies OEXT_NO_MAGICLINKS)"; `/usr/include/linux/openat2.h` lines 37–38 contain it verbatim, including the `OEXT_` spelling. The fixture's S138 quote "which affects the handling of symbolic links only in the final component of path" appears once in `/usr/share/man/man2/openat2.2.gz`. These checks cover only the fixture quotes, not the landed entry's quotes.
7. **Before-values in the draft match the committed receipts.** Each frozen before-value was read from its receipt and matches the claims text: `controls/c1v2-before.txt` (`FORGERS_REJECTED=0/12 … BATTERY=FAIL`, exit 1; all twelve forgers `LEGS=20/20 C1=PASS`); `controls/c2v2-before.txt` (`ENTRY=0/1 … C2=FAIL`, exit 1); `controls/null-counters.txt` (null-pass 0/12 forgers and 0/4 stubs; null-fail and null-hashlist 0/3 landed; all `BATTERY=FAIL`); `controls/c1v2-controls.txt` (X00 `BATTERY=PASS`; X01–X08 and X12 KILLED; X10 SURVIVED as the named gap; `CONTROLS_UNEXPECTED=0`); `controls/c2v2-controls.txt` (positive `C2=PASS` exit 0; 20 FAIL variants, of which 18 are single-defect and two are absent entry and absent rows; `non-sequitur` PASS as the named limit; `C2V2_CONTROLS_UNEXPECTED=0`).
8. **Frontier claim checked, one overreach removed.** The draft's first version said the lane's writers do not call `openat2`, which I had not checked. `grep -rl openat2 tools/ corpus/knowledge/` exits 1 at the current tree; the draft now states that. Frozen-claim statements are taken from `claims.md` as written; the receipts listed below were read directly, and nothing else in the draft was re-derived by a run.
9. **Marker count.** `draft.md` contains 49 `<AFTER>` markers, counted by `grep -o '<AFTER>' draft.md | wc -l` after the last edit. Per-section counts were not tallied and are not claimed.

## Evidence pointers (commands run; observed output)

- `sha256sum corpus/evidence/round62/claims.md` → `a3193ebd328919e2af017011278e423c5940fd9447f0730bd400da9d15c866bc` (matches the wave context digest).
- `sha256sum` prefixes: `c1v2-count.py` → `b7016fba91b03460`; `c2v2-count.py` → `817d5fc0b94e9fc8`; `tools/build-spans.py` → `c366492005ce304a`; `corpus/evidence/round61/c1-count.py` → `f1d8b6fde8dedd88`. All match the claims.
- `git log --oneline -3` → `d173d14` (wave spec, dispatch, freeze check, ready), `388d153` (claims freeze), `8607de8` (round-61 spot-check, base).
- `controls/c1v2-before.txt` tail → `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=0/12 STUBS_REJECTED=4/4 BATTERY=FAIL`, `exit=1`.
- `controls/c2v2-before.txt` → `ENTRY=0/1 … CENSUS=1/1 C2=FAIL`, `exit=1`; rows S138–S140 `absent`; probe `absent`.
- `controls/c2v2-controls.txt` → `C2V2_CONTROLS_UNEXPECTED=0`, `exit=0`.
- `controls/c1v2-controls.txt` → `CONTROLS_UNEXPECTED=0`, `exit=0`.
- `controls/null-counters.txt` → three `BATTERY=FAIL` lines as above.
- `controls/candidate-openat2-probe.txt` → `PROBE_FACTS=14/14`; kernel `7.2.11-arch1-1`, Python `3.14.8` (candidate output; the committed landed file does not yet exist).
- `.ufo/waves/round-62/freeze-check-live.txt` → `FAILED_CHECKS=none`, `FREEZE_CHECK=PASS`, `66 names match in order`.
- `.ufo/waves/round-62/w1-spec.json` → 66 items; `w1-dispatch.json` → `counts` present; the 66 count is the spec's item count.
- `grep -c "^| S" corpus/SOURCES.md` → `137`; `grep -n "S13[6-9]\|S14[0-9]" corpus/SOURCES.md` → rows S136, S137 only, plus the round-45 and round-61 history lines.
- `grep -rl openat2 tools/ corpus/knowledge/` → no output, `exit=1`.
- `/usr/include/linux/openat2.h` lines 37–38 → `RESOLVE_NO_SYMLINKS 0x04 … (implies OEXT_NO_MAGICLINKS)`.
- `zcat /usr/share/man/man2/openat2.2.gz | grep -c "only in the final component"` → `1`.
- LOG.md lines 1944–1954 and SCORECARD.md lines 2939–2963 and corpus/README.md lines 1–12 and 1267–1296 were read as the format sources.

## Out of scope (not done)

- No lane file written; no counter, battery or probe run; no fetch; no subagent; no install. No tool installed, so the tooling line in the draft is a placeholder for L1.
- Verdict cells in SCORECARD and the operability-adjacent axis verdicts are `<AFTER>` because they depend on the kill rules applied at landing and closure. Mapping in draft section 5.
- The round-62 lesson (`corpus/lessons/round-62.md`) and the non-author spot-check are not drafted; the draft only references them.

VERDICT: DRAFT_SECTIONS=4 after_markers=49
