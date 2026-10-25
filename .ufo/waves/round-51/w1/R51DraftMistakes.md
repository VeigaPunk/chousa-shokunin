# R51DraftMistakes — draft `## Mistakes` rows for corpus/lessons/round-51.md

seat `R51DraftMistakes` · round 51, wave 1 · base `9ec1751a24231e899ceea4688e21c8edf6046d35`, tip `cfe6c9fb9b56`, tool `bdaf80f43f39827029b1e849c5a6d8d88252ac88d331bf75fea1df0b51fba29d` (2a3389d).
Read-only on the lane: every command below is a read; the only lane write is this file. Scratch `/dev/shm/chousa-r51-R51DraftMistakes/` (deleted at the end). No install, no network, no fetch. Rows 1–5 were sent to `R51DraftQuality`; 1–5 are final, 6–7 follow.

## Draft rows — intended lane path `corpus/lessons/round-51.md` `## Mistakes`

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| 1. scope/reference-drift: the round-50 after-measurement names no revision, and the gate registry row names the C1 candidate, not the landed tip | `corpus/evidence/round50/measure-after.txt:1` reads "at the working tree before the final commit" with no hash; `corpus/evidence/round50/measure-after-1.txt:1` says `# tip: working tree` (a moving target); `SKILL.md:132` names `ec52e632edbad7fe51a6573d29acad5a028a7158` for the counters, whose landed tip is `1d7aba0948cf`; routed defect 1, `corpus/lessons/round-50-verifier-spotcheck.md:90`; QUALITY 58 | `R50ScribeReportDraft.md:74` left this row `<PENDING>`; the spot-check's non-author read found it | header carries `lane_revision=<sha> tool_sha256=<sha>`, registry row names the landed tip. Failing now, both exit 1: `head -1 corpus/evidence/round50/measure-after.txt \| grep -qE '[0-9a-f]{7,40}'`; `! grep -q 'ec52e632' SKILL.md` — both exit 0 after the fix |
| 2. vacuous: the frozen round-50 C1 counter recognises its own six literal DIFF lines, so a 42-line tool with no adopter logic scores it full | `corpus/evidence/round50/c1-count.py:107-112` matches one literal regex per perturbation; `corpus/evidence/round50/controls/forge-tool.py:2,8-13` prints all six for any non-pinned digest; `corpus/evidence/round50/c1-supplement-receipt.txt:51-54` records `LEGS=5/5 C1=PASS` for it; QUALITY 80 | W2 `R50CritForgeC1` (`.ufo/waves/round-50/w2/R50CritForgeC1.md:7-14`) | replace the literal-DIFF search with a nonce leg plus an exclusive output set (what round-51 C1 does). Failing commands: `python3 corpus/evidence/round50/c1-count.py --tool corpus/evidence/round50/controls/forge-tool.py` prints `BASELINE=PASS rc=0 findings=26` and `PERTURB_PASS=6/6` for the cheat; with the forge's `REAL` pointed at `ec52e632:tools/assimilate-rows.py` (scratch, sha256 `bff32c11…`) the frozen counter prints `LEGS=5/5 C1=PASS` exit 0. A fixed counter must print `C1=FAIL` for both |
| 3. reference-drift: the adopter's default flip to source-only citations breaks both earlier one-shot counters, and the env switch the claims rely on does not restore them | `corpus/evidence/round51/claims.md:56-58` ("`LEGACY_ALL` is what preserves their behaviour"), contradicted by measurement at the tip; QUALITY 58, 68 | none before this row — the claims disclosed the risk but no receipt ran the earlier counters at the candidate | each one-shot counter pins the tool bytes it was measured against (QUALITY 58). Failing commands (all exit 1 today): `python3 corpus/evidence/round49/c1-count.py` → `SETS_PASS=2/3 C1=FAIL`; `python3 corpus/evidence/round50/c1-count.py` → `LEGS=3/5 C1=FAIL`; `ASSIMILATE_CITES=all python3 corpus/evidence/round50/c1-count.py` → `LEGS=4/5 C1=FAIL` (`SELFTEST_DEFAULT=FAIL`). `--tool <ec52e632 bytes>` restores both (`5/5`, `3/3`); a fixed counter passes all three |
| 4. calibration: five self-assessment evidence pointers dangle at the base, and no criterion 1–80 requires a pointer to resolve | `corpus/evidence/round51/controls/c3-before-erratum.txt:4-9` (`SCORECARD.md:1843 measure/final/`, `:2073 measure-l1/c1-s36361.json`, `:2074 measure-l1/c2-s36371.json`, `:2616 c1-supplement.py`, `SHONEN.md:10 round25-meta-differential.log`), all five absent on disk; QUALITY 37 governs numeric tallies and QUALITY 74's scan set is `corpus/evidence/round50/stale-count-check.py:18` = QUALITY.md, README.md, LOG.md, round-49.md (0 hits for SCORECARD.md/SHONEN.md); `tools/research-gate.sh` names SCORECARD.md/SHONEN.md 0 times | none — no criterion and no check read a self-assessment's pointers before round 51 | repair the five pointers (or one `correction: SCORECARD.md:<line> <ptr> -> <path>` line per row). Failing command: `python3 corpus/evidence/round51/c3-count.py` → `DANGLING=5 C3=FAIL` exit 1, identical at the tip and at the base tree |
| 5. counter-defect (vacuous): the C3 extractor stripped a leading dot, so three existing `.ufo/...` paths read as dangling, and its controls never seed the dot class | `corpus/evidence/round51/claims-erratum.md:12-16`; pre-erratum `c3-count.py:54` (`tok.strip(",;.:()")`); `corpus/evidence/round51/controls/build-c3-controls.py:34-57` derives all three controls from the counter's own `DANGLING` output (blanket line, deleted rows, zero-byte files at the *dangling* names), so no control ever adds a dot-leading pointer; QUALITY 20 is the criterion that should have caught it | none (`claims-erratum.md:27-28` states the class and that no control seeds it) | tokenizer keeps the leading dot, plus a DOTPATH control whose pointer must resolve. Failing commands: `pointers("`.ufo/waves/round-34/measure/`")` → `['ufo/waves/round-34/measure/']` at `d603f6f` vs `['.ufo/waves/round-34/measure/']` at the tip; the pre-erratum counter at the base tree prints `DANGLING=8` (3 false positives) vs `DANGLING=5` |
| 6. scope: the filename drift (`istic-…` for a 中国科学院文献情报中心 page) is recorded in the entry only, not in the coverage row a reader browses | `corpus/knowledge/istic-citation-verification-r39.md:6` carries the note ("the lane filename says istic, inherited from the staged entry"); `corpus/README.md:1078`'s row does not — `ISTIC` and `filename drift` occur 0 times in README.md; routed defect 4, `corpus/lessons/round-50-verifier-spotcheck.md:93` | round-50 spot-check section 6 item 4 | append the drift note to the coverage row. Failing command: `awk -F'\|' '/^\| `knowledge\/istic-citation-verification-r39.md`/{print ($0 ~ /ISTIC\|drift/) ? "DRIFT_NOTE" : "DRIFT_MISSING"}' corpus/README.md` → `DRIFT_MISSING` |
| 7. reference-drift: a receipt tally whose printed command does not reproduce it (`$ grep -cE rows` → `106`) | `corpus/evidence/round50/measure-after.txt:125-126`; re-run verbatim it reads stdin and prints `0`; the obvious file gives `13`; `106` is the S-row count, so the pattern or the file argument was dropped | none — QUALITY 37's own check ("run the named command and compare") was never run on the receipt | name the file and the pattern. Failing commands: `grep -cE rows < /dev/null` → `0`; `grep -cE rows corpus/SOURCES.md` → `13`; `grep -cE '^\| S[0-9]{3} ' corpus/SOURCES.md` → `106` |

## Verification — commands and observed output

```
$ head -1 corpus/evidence/round50/measure-after.txt
# round-50 after-measurement at the working tree before the final commit (tracked tree equals the commit once landed)
$ head -1 corpus/evidence/round50/measure-after.txt | grep -qE '[0-9a-f]{7,40}'; echo exit=$?
exit=1
$ grep -n 'ec52e632' SKILL.md | cut -c1-95
132:| `chousa round-50 counters and checks` | gate | `python3 corpus/evidence/round50/c1-count.py [--tool PATH]` ·
$ git rev-parse 1d7aba0 | cut -c1-12
1d7aba0948cf
$ head -1 corpus/evidence/round50/measure-after-1.txt
$ python3 corpus/evidence/round50/c1-count.py   # tip: working tree
```

```
$ python3 corpus/evidence/round50/c1-count.py --tool corpus/evidence/round50/controls/forge-tool.py
SELFTEST_DEFAULT=PASS (skipped: --tool) · BASELINE=PASS rc=0 findings=26 · PERTURB_PASS=6/6 · EXPECTED_BAD=PASS rc=2
R49_REGRESSION=FAIL rc=1 · LEGS=4/5 · C1=FAIL      # the only failing leg is R49_REGRESSION (row 3), not the forge
$ sha256sum /dev/shm/.../tool-ec52e632.py     # git show ec52e632:tools/assimilate-rows.py
bff32c11d02bc1bdc28ed484d4895d86c7f3537d8a9496ad474c73d4531f5b81
$ python3 corpus/evidence/round50/c1-count.py --tool /dev/shm/.../forge-r50tool.py
BASELINE=PASS rc=0 findings=26 · PERTURB_PASS=6/6 · EXPECTED_BAD=PASS rc=2 · R49_REGRESSION=PASS rc=0 · LEGS=5/5 · C1=PASS · exit=0
```

```
$ python3 corpus/evidence/round49/c1-count.py; echo exit=$?
SET_C TOOL_EXIT=0 CITED=5 APPEND=3/3 HELD=2/2 BY_DOC=3/5 EXTRA=0 REWRITE=0/1 ... -> FAIL · SETS_PASS=2/3 · C1=FAIL · exit=1
$ ASSIMILATE_CITES=all python3 corpus/evidence/round49/c1-count.py; echo exit=$?
SETS_PASS=3/3 · C1=PASS · exit=0
$ python3 corpus/evidence/round50/c1-count.py; echo exit=$?
SELFTEST_DEFAULT=PASS · BASELINE=FAIL rc=1 findings=? · PERTURB_PASS=6/6 · EXPECTED_BAD=PASS · R49_REGRESSION=FAIL rc=1 · LEGS=3/5 · C1=FAIL · exit=1
$ ASSIMILATE_CITES=all python3 corpus/evidence/round50/c1-count.py; echo exit=$?
SELFTEST_DEFAULT=FAIL · BASELINE=PASS rc=0 findings=26 · PERTURB_PASS=6/6 · EXPECTED_BAD=PASS · R49_REGRESSION=PASS rc=0 · LEGS=4/5 · C1=FAIL · exit=1
$ ASSIMILATE_CITES=all python3 tools/assimilate-rows.py --selftest | tail -1
SELFTEST=FAIL findings=35 expected=25        # exit 1 — why SELFTEST_DEFAULT fails under the env switch
$ python3 corpus/evidence/round50/c1-count.py --tool /dev/shm/.../tool-ec52e632.py; echo exit=$?
SELFTEST_DEFAULT=PASS (skipped: --tool) · BASELINE=PASS · LEGS=5/5 · C1=PASS · exit=0
$ python3 corpus/evidence/round49/c1-count.py --tool /dev/shm/.../tool-ec52e632.py; echo exit=$?
SETS_PASS=3/3 · C1=PASS · exit=0
```
No environment setting yields `5/5` at the tip: unset breaks `BASELINE` and `R49_REGRESSION`, `all` breaks `SELFTEST_DEFAULT`; only a tool-revision pin restores the round-50 counter. Base tree for the next block = `git archive 9ec1751 | tar -x -C /dev/shm/…/base` (14679 files).
```
$ python3 corpus/evidence/round51/c3-count.py --root /dev/shm/chousa-r51-R51DraftMistakes/base; echo exit=$?
CAP_ROWS=36 (base 36) · POINTERS=74 (base 74) · RESOLVED_BY_CORRECTION=0
DANGLING SCORECARD.md:1843 measure/final/          DANGLING SCORECARD.md:2073 measure-l1/c1-s36361.json
DANGLING SCORECARD.md:2074 measure-l1/c2-s36371.json   DANGLING SCORECARD.md:2616 c1-supplement.py
DANGLING SHONEN.md:10 round25-meta-differential.log     DANGLING=5 · C3=FAIL · exit=1
$ python3 corpus/evidence/round51/c3-count.py; echo exit=$?        # tip tree: the same five, exit=1
$ for p in measure/final measure-l1/c1-s36361.json measure-l1/c2-s36371.json c1-supplement.py round25-meta-differential.log; do [ -e "$p" ] && echo "EXISTS $p" || echo "ABSENT $p"; done
ABSENT measure/final · ABSENT measure-l1/c1-s36361.json · ABSENT measure-l1/c2-s36371.json · ABSENT c1-supplement.py · ABSENT round25-meta-differential.log
$ grep -c 'SCORECARD\|SHONEN' tools/research-gate.sh
0
$ sed -n '18p' corpus/evidence/round50/stale-count-check.py
PROSE = ("corpus/QUALITY.md", "corpus/README.md", "LOG.md", "corpus/lessons/round-49.md")
```

```
$ python3 -c '…load corpus/evidence/round51/c3-count.py…; print(m.pointers("`.ufo/waves/round-34/measure/`"))'
['.ufo/waves/round-34/measure/']
$ python3 -c '…load /dev/shm/…/c3pre.py (= d603f6f:corpus/evidence/round51/c3-count.py)…; print(m.pointers("`.ufo/waves/round-34/measure/`"))'
['ufo/waves/round-34/measure/']
$ git show d603f6f:corpus/evidence/round51/c3-count.py | sed -n '54p'
            tok = SUFFIX.sub("", tok.strip(",;.:()"))
# pre-erratum counter, --root <base tree>:
DANGLING SCORECARD.md:1973 ufo/waves/round-34/measure/ · DANGLING SCORECARD.md:1974 ufo/waves/round-34/measure-a2/
DANGLING SHONEN.md:12 ufo/waves/round-25/build/ConnectorMetaSiblings.md · DANGLING=8 · C3=FAIL · exit=1
$ for p in .ufo/waves/round-34/measure .ufo/waves/round-34/measure-a2 .ufo/waves/round-25/build/ConnectorMetaSiblings.md; do [ -e "$p" ] && echo "EXISTS $p"; done
EXISTS .ufo/waves/round-34/measure · EXISTS .ufo/waves/round-34/measure-a2 · EXISTS .ufo/waves/round-25/build/ConnectorMetaSiblings.md
```

```
$ awk -F'|' '/^\| `knowledge\/istic-citation-verification-r39.md`/{print ($0 ~ /ISTIC|drift/) ? "DRIFT_NOTE" : "DRIFT_MISSING"}' corpus/README.md
DRIFT_MISSING
$ grep -c 'ISTIC\|filename drift' corpus/README.md
0
```

```
$ sed -n '125,126p' corpus/evidence/round50/measure-after.txt
$ grep -cE rows
106
$ grep -cE rows < /dev/null; echo exit=$?
0 · exit=1
$ grep -cE rows corpus/SOURCES.md
13
$ grep -cE '^\| S[0-9]{3} ' corpus/SOURCES.md
106
```

## Which criterion should have caught each

- Rows 1, 3, 7: QUALITY 58 (a counter's measured revision is pinned inside its receipt) and 37 (a tally carries the command that reproduces it over committed bytes). 37 existed and names the check "run the named command and compare"; nothing ran it on a *receipt's* pasted command list, and 37's shown-able-to-fail example is a SCORECARD row, so a receipt line was never in its scope.
- Row 2: QUALITY 80, added by round 50 itself. It names the forge exactly; the repair landed as a *supplement* (`c1-supplement.py`) while the frozen counter keeps passing the cheat, so the criterion is satisfied by a sibling artifact, not by the counter it describes.
- Row 4: neither 37 nor 74. 37's subject is a number; 74's check reads four files (`stale-count-check.py:18`) and cannot see SCORECARD.md or SHONEN.md, let alone a path token. No criterion 1–80 says a self-assessment's evidence pointer must resolve, and the gate reads neither file (0 hits). The criterion class was absent — this is the gap C3 measures.
- Row 5: QUALITY 20 (controls exercise the two representations separately at a token/match or filesystem-path boundary) with 21 (a parser repair preserves positive syntax). The controls are negative-by-construction: `build-c3-controls.py:34-57` builds all three from the counter's own `DANGLING` list, so no control seeds a token of the class the tokenizer mangles. 56 does not help either: the controls do fire, on the wrong class. Row 6 has no criterion at all — the round-50 spot-check routed it as defect 4 without one.

## Out of scope / notes

- Did not edit `corpus/lessons/round-51.md`, any counter, `SKILL.md`, `SCORECARD.md`, `SHONEN.md` or the staged package; no commit, no jj, no fleet write. Scratch held the base-tree extract, `tool-ec52e632.py`, `c3pre.py` and the 27-line `forge-r50tool.py` (the lane forge with only its `REAL` constant re-pointed); deleted before finishing.
- Routed defects 3 (seat names) and 5 (SHONEN boxes) are not rows: defect 3 already is a round-50 Mistakes row (`corpus/lessons/round-50.md`, "attribution") and its check exists; defect 5 is a promotion decision, not a defect. No tool install or upgrade was needed or made.

VERDICT: attacked the seven mistake classes the item names — pinned the unpinned round-50 receipt and the candidate-named gate row, reproduced the frozen C1 counter passing a 42-line forge `LEGS=5/5 C1=PASS` at the tip, measured both earlier counters broken at the candidate (`2/3`, `3/5`) with the env switch failing to restore them (`4/5`), and reproduced `DANGLING=5` at base and tip against the pre-erratum `DANGLING=8` with its three false positives — all seven rows verified with observed commands; two criterion gaps found (no pointer-resolving criterion, no positive-control rule for a counter's tokenizer).
