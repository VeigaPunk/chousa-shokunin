# Gate-record surface survey — chousa, round 80, seat R80ScoutA

Read-only reconnaissance of the lane's Gate-record surface: the ground C2 moves on.

- Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`
- Base revision (round-79 lane tip): `b7803829922770b890e9f4efdd30d12c3695439a`
- Scratch (all clones/fixtures): `/fast/scratch/hyaku/chousa-r80/R80ScoutA/` — deleted before yield
- Lane repo mutated: **no**. Every source was read with `git -C <lane> show <rev>:<path>`.
- Instrument cited: `corpus/evidence/round80/gate-grounding-check.py`, sha256
  `d9e426216665a098cd90adf8fbf5e5dd62e02dc7b5b707c322b404b3eb55c553`
  (measured: `sha256sum` of the lane working-tree copy and of the scratch copy — identical).
- Tooling: none installed. Everything below is stock `git`, `grep`, `wc`, `python3` (3.x, stdlib only).

---

## 0. Method and its one limit

Every located quote in a lesson's `## Gate` block was re-opened at the cited revision, `grep -c`'d
and `wc -w`'d. The extraction is script-driven (`receipts/table-out.txt`, `receipts/table.json`);
each extracted fragment was first proven to appear **verbatim in its lesson's own `## Gate` block**
so that no quote could be silently paraphrased by this seat.

**Limit (stated, not hidden).** Five fragments (S177, S193, S194, S196, S197) are *line-wrapped* in
the lesson markdown, so they are not byte-contiguous in the lesson file. They were proven present
after whitespace normalisation of the `## Gate` block; the counts and the cited-path checks are
unaffected. Provenance output:

```
r71 S177: normalized-in-lesson=False  raw-in-lesson=False   <- see note below
r78 S193: normalized-in-lesson=True   raw-in-lesson=False
r78 S194: normalized-in-lesson=True   raw-in-lesson=False
r79 S196: normalized-in-lesson=True   raw-in-lesson=False
r79 S197: normalized-in-lesson=True   raw-in-lesson=False
```

S177's `False` is not a provenance failure: the round-71 lesson states the quote as **two pieces**
— `` `the battery completes and prints` `` **+** "the verdict-line literal it asserts" — and the
lesson's own words count (12) is the count of the *whole* reconstructed cell string, not of the
first fragment alone. This seat reconstructed that cell string from the cited SKILL.md row 83 and
measured it independently (12 words, present). S177 is therefore scored on its reconstructed form,
and this is flagged in the table.

---

## 1. The table

Columns: row id · lesson · cited location (path @ revision, cited lines) · quote · stated count ·
measured count · verdict.

`measured` = `wc -w` of the quote as the lesson writes it (joined fragments, whitespace split).
`grep_c` = number of lines in the cited file @ the cited revision containing the quote.

| row | lesson | cited location | quote | stated | measured | grep_c | verdict |
|---|---|---|---|---|---|---|---|
| S168 | r70 | `.ufo/waves/round-69/preflight-final.txt` @ `1db6babf5286`, line 12 | `PREFLIGHT=7/7 FAILED=none ENV=none SKIPPED=G08` | 4 | 4 | 1 | **ok** |
| S169 | r70 | `tools/research-gate.sh` @ `1db6babf5286`, lines 3970–3971 | `a host without flock(1) cannot serialize, so it fails closed` + `# instead of appending unlocked.` | 15 | 15 | 2 | **ok** |
| S170 | r70 | `tools/research-gate.sh` @ `1db6babf5286`, lines 7904–7905 | `cases=$((cases + 1)); SKIPPED=$((SKIPPED + 1))` + `printf 'skip-case %-2d %-26s reason=%s\n'` | 10 | 11 | 11 | **mismatch** |
| S171 | r70 | `corpus/evidence/round70/controls/recon-run-r70.txt` @ `b2f88eccf603` | `tools/research-gate.sh: line 5548: /tmp/chousa-research-gate-selftest.dcCFup/r6-manifest.jsonl: No such file or directory` | 10 | 9 | **0** | **absent** |
| S172 | r70 | `corpus/lessons/round-69-verifier-spotcheck.md` @ `1db6babf5286`, §8 item 1 | `the preflight receipts skip G08 (minutes-long research-gate selftest), r66–r69 disclosure chain; a full-run receipt remains owed` | 16 | 16 | 1 | **ok** |
| S173 | r71 | `corpus/lessons/round-70-verifier-spotcheck.md` @ `11b51988d387`, §5 D-70-5 | `correct the row to the measured state (runs truthfully through case 257, ended at case 258, no verdict line; honest-stop)` | 21 | 20 | 1 | **mismatch** |
| S174 | r71 | `corpus/evidence/round70/controls/after-battery-completes-r70.txt` @ `11b51988d387` | `the run was ended by the round at case 258 (claims-locale-boundary) - its gate ran >70 minutes without emitting the case line` | 22 | 22 | **0** | **absent** |
| S175 | r71 | `corpus/evidence/round71/controls/probe-timeout-capability-r71.txt` @ `58232b27d1ea` | `tprobe_rc=124` + `real 0m16.333s` + `RESEARCH_GATE: CLEAN` | 6 | 5 | 3 | **mismatch** |
| S176 | r71 | `corpus/evidence/round70/controls/before-g08-selftest-partial.txt` @ `11b51988d387` | `tools/research-gate.sh: line 5548: /tmp/chousa-research-gate-selftest.dcCFup/r6-manifest.jsonl: No such file or directory` | 10 | 9 | 1 | **mismatch** |
| S177 | r71 | `SKILL.md` @ `b2f88eccf603`, row 83 | `the battery completes and prints` + verdict literal | 12 | 12 | 1 | **ok** (reconstructed) |
| S178 | r72 | `corpus/lessons/round-71-verifier-spotcheck.md` @ `7851c4ce29ef`, §6 item 2 | `The committed receipts carry **9** (\`battery-partial-r71.txt\`) + **16** (\`killtest-partial-scratch-copy.txt\`) = **25** ok-case lines` | 11 | 13 | 1 | **mismatch** |
| S179 | r72 | `corpus/evidence/round72/controls/probe-r72-sizing.txt` @ `97b6ea754b23` | `tprobe_rc=124` + `real 0m18.131s` + `RESEARCH_GATE: CLEAN` | 6 | 5 | 3 | **mismatch** |
| S180 | r73 | `corpus/lessons/round-72-verifier-spotcheck.md` @ `f748abbb6bf5`, line 90 | `The line that actually exits is the next unguarded sub-run assignment` | — | 11 | 1 | **ok** (no count asserted) |
| S181 | r73 | `corpus/evidence/round72/controls/after-r72-corrections.txt` @ `f748abbb6bf5`, line 1 | `every count line re-run fresh at the verdicts tree, immediately before the verdicts commit` | — | 14 | 1 | **ok** (no count asserted) |
| S182 | r74 | `corpus/lessons/round-73-verifier-spotcheck.md` @ `8a28732b3c15`, §5 item 1 | `Before any successor calibration freeze, exercise a real committed append and a real deletion through \`load()\`` | 18 | 16 | 1 | **mismatch** (known & corrected in-lane) |
| S183 | r74 | `corpus/evidence/round73/c2-count.py` @ `8a28732b3c15`, line 163 | `base = check({k: v for k, v in FIXTURE.items()}, {}, set())` | 13 | 11 | 1 | **mismatch** (known & corrected in-lane) |
| S184a | r75 | `corpus/lessons/round-74-verifier-spotcheck.md` @ `43a7a0db52c8`, line 73 | `before any future successor binds a candidate-running counter, meet existing QUALITY 126 with committed prefreeze detection-forger controls and record limits` | 20 | 20 | 1 | **ok** |
| S184b | r75 | `corpus/lessons/round-74-verifier-spotcheck.md` @ `43a7a0db52c8`, line 74 | `append a correction to the lesson's quoted-word counts (16/11 whitespace tokens, not 18/13)` | 13 | 13 | 1 | **ok** |
| S185 | r75 | `corpus/QUALITY.md` @ `43a7a0db52c8`, line 1002 | *no quote stated* — "Located anchor: criterion 126's text" | — | — | — | **no quote** (anchor only) |
| S186a | r75 | `.ufo/waves/round-74/w1/R74Critic/forge-order-oracle.py` @ `43a7a0db52c8`, line 3 | `Never reads --lane bytes nor any repository content. Scores 9/9 on the frozen` | 13 | 13 | 1 | **ok** |
| S186b | r75 | `.ufo/waves/round-74/w1/R74Critic/forge-order-oracle.log` @ `43a7a0db52c8`, line 11 | `LOADER_MATRIX=9/9 C1=PASS` | 2 | 2 | 1 | **ok** |
| S187 | r76 | `corpus/lessons/round-75-verifier-spotcheck.md` @ `1af39fed6058`, line 125 | `commit subject, tree ids and byte sizes are stable metadata channels, and four content-blind` | 14 | 14 | 1 | **ok** |
| S188 | r76 | `corpus/lessons/round-75-verifier-spotcheck.md` @ `1af39fed6058`, line 130 | `polarity and magnitude rather than substring presence, require the correction block to be the final section` | 16 | 16 | 1 | **ok** |
| S189 | r76 | `corpus/evidence/round76/claims.md` @ `5daa3628389c`, line 27 | `` `BATTERY=PASS forgers_rejected=11/11 positive=2/2` `` | — | 3 | 2 | **ok** (no count asserted) |
| S190 | r77 | `corpus/lessons/round-76-verifier-spotcheck.md` @ `6defa58dbdc40`, line 150 | `Outer batteries score exit codes in a fixed subject order.` | 10 | 10 | 1 | **ok** |
| S191 | r77 | `corpus/lessons/round-76-verifier-spotcheck.md` @ `6defa58dbdc40`, lines 163–164 | `supersede it with an append-only correction entry naming the superseded text` | 11 | 11 | **0** | **absent** (line-wrapped) |
| S192 | r77 | `corpus/evidence/round77/claims.md` @ `a95307825787`, line 1 | `# Round 77 frozen claims — the outer battery's order and content legs` | — | 13 | 1 | **ok** (no count asserted) |
| S193 | r78 | `corpus/lessons/round-77-verifier-spotcheck.md` @ `53dbd512d0ab`, line 156 | `SKILL.md registry row \`round77 order-and-content battery\` is missing its owner cell.` | 11 | 11 | **0** | **absent** |
| S194 | r78 | `corpus/QUALITY.md` @ `53dbd512d0ab`, line 1046 | `An outer battery prints no invertible answer key, no strippable subject identity and no receipt a child can append to` | 20 | 20 | 1 | **ok** |
| S195 | r78 | `corpus/evidence/round78/controls/forge-battery-after-v5.txt` @ `93e0432eb5bb`, line 9 | `FORGE_BATTERY=PASS forgers_handled=4/4 positive=1/1` | — | 3 | 1 | **ok** (no count asserted) |
| S196 | r79 | `corpus/QUALITY.md` @ `ee70e6df19fe`, line 1056 | `A subject-identity salt is defeated by any normalizer that knows its marker family, so the closure is a per-channel measurement and not a property of the salt` | 25 | 27 | 1 | **mismatch** (known) |
| S197 | r79 | `corpus/QUALITY.md` @ `ee70e6df19fe`, line 1054 | `A self-assessment counter validates each resolution line against the bytes it claims to repair, and its audit window covers every block rather than the newest` | 24 | 25 | 1 | **mismatch** (known) |
| S198 | r79 | `.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt` @ `3eb4a3cad8fe`, lines 1–20 | `the audit window is the last \`## Round-\d+ addition\` block` | — | 10 | **0** | **absent** (known) |

**Totals: 33 records · 17 ok · 10 mismatch · 5 absent · 1 no-quote-stated.**
Of the 15 defective records (mismatch + absent), 3 (S196/S197/S198) are the ones the round-79
closure named. **12 are beyond that closure.**
(Counted programmatically from `receipts/table.json`; the table above lists one row per record,
S184 and S186 contributing two records each for their two located quotes.)

Full machine-readable table: `receipts/table.json`. Full command-by-command trace:
`receipts/measure-out.txt`.

---

## 2. Every defective record beyond S196/S197/S198

Each entry names the command and its observed output.

### 2.1 S170 — round-70 lesson — stated 10, measured 11 (mismatch)

```
CMD: git -C <lane> show 1db6babf528692d871a2b97be0b3e519614fa300:tools/research-gate.sh | sed -n '7904,7905p' | cat -A
OUT:    cases=$((cases + 1)); SKIPPED=$((SKIPPED + 1))$
OUT:    printf 'skip-case %-2d %-26s reason=%s\n' "$cases" c1lk-holder-blocks-append 'no /proc/locks or no flock(1)'$

CMD: printf %s 'cases=$((cases + 1)); SKIPPED=$((SKIPPED + 1))' | wc -w
OUT: 6
CMD: printf %s "printf 'skip-case %-2d %-26s reason=%s\\n'" | wc -w
OUT: 5
CMD: printf %s 'cases=$((cases + 1)); SKIPPED=$((SKIPPED + 1)) printf '"'"'skip-case %-2d %-26s reason=%s\n'"'"'' | wc -w   (joined fragments)
OUT: 11
```
The lesson states "10 tokens" for the two fragments; the fragments carry 6 + 5 = 11 whitespace
tokens. The lesson also cites "lines 7904–7905", and both fragments are on those lines — the
location is right, the count is off by one. Note also that `grep -c` for these fragments returns
**11** hits, not 1: `cases=$((cases + 1)); SKIPPED=$((SKIPPED + 1))` alone occurs on 5 lines of the
script (6268, 6288, 6712, 7316, 7904). The counter's R3 checks *containment on the named line*, not
uniqueness, so this is not a counter blocker — but it is a record-ambiguity the lesson does not note.

### 2.2 S171 — round-70 lesson — quote absent from the file it cites (absent)

```
CMD: git -C <lane> show b2f88eccf603be88aa4c217adb5f49813cd82182:corpus/evidence/round70/controls/recon-run-r70.txt | grep -c -F 'chousa-research-gate-selftest.dcCFup'
OUT: 0
grep_exit=1
CMD: git -C <lane> show b2f88eccf603be88aa4c217adb5f49813cd82182:corpus/evidence/round70/controls/recon-run-r70.txt | grep -n -F 'research-gate.sh: line 5548:'
OUT: 66:C:/Users/jpvei/.../scratch/chousa-r70/recon/research-gate.sh: line 5548: /tmp/chousa-research-gate-selftest.K1Yhut/r6-manifest.jsonl: No such file or directory
OUT: 74:C:/Users/jpvei/.../scratch/chousa-r70/recon/research-gate.sh: line 5548: /tmp/chousa-research-gate-selftest.K1Yhut/r6-manifest.jsonl: No such file or directory
CMD: git -C <lane> show 11b51988d3878cd33b826295304f6f266718ba86:corpus/evidence/round70/controls/before-g08-selftest-partial.txt | grep -c -F 'chousa-research-gate-selftest.dcCFup'
OUT: 7
grep_exit=0
CMD: printf %s 'tools/research-gate.sh: line 5548: /tmp/chousa-research-gate-selftest.dcCFup/r6-manifest.jsonl: No such file or directory' | wc -w
OUT: 9
```
The lesson calls this quote "verbatim" from `recon-run-r70.txt`; that file contains the **K1Yhut**
tmpdir variant, never **dcCFup**. The dcCFup crash line lives in `before-g08-selftest-partial.txt`.
Stated 10 tokens, measured 9.

**This defect is already recorded in-lane** — it is not new. `corpus/lessons/round-70.md:45`
(`## Mistakes`) states it as **D-70-1**, `corpus/lessons/round-71.md:33` records it as *fixed
append-only*, and registry row **S176**'s `teaches` cell opens `supersedes S171 — for the location
attribution only`. The round-70 lesson's own `## Gate` table was, correctly, not rewritten
(append-only). What this seat adds: **the round-70 `## Gate` cell remains defective in the
committed bytes** and is unreachable by the round-80 counter for two independent reasons (see §3.2
and §3.3) — so the defect is *known* but not *machine-closed*.

### 2.3 S173 — round-71 lesson — stated 21, measured 20 (mismatch)

```
CMD: git -C <lane> show 11b51988d3878cd33b826295304f6f266718ba86:corpus/lessons/round-70-verifier-spotcheck.md | grep -n -F 'correct the row to the measured state (runs truthfully through case 257, ended at case 258, no verdict line; honest-stop)'
OUT: 84:- **D-70-5 (SKILL registry row 83 contradicts its own cited receipt).** ... Fix next round: correct the row to the measured state (runs truthfully through case 257, ended at case 258, no verdict line; honest-stop), per the corrections-sweep rule.
CMD: printf %s 'correct the row to the measured state (runs truthfully through case 257, ended at case 258, no verdict line; honest-stop)' | wc -w
OUT: 20
```
Location correct (line 84, section 5 D-70-5). Count off by one.

### 2.4 S174 — round-71 lesson — quote absent from the file it cites (absent)

```
CMD: git -C <lane> show 11b51988d3878cd33b826295304f6f266718ba86:corpus/evidence/round70/controls/after-battery-completes-r70.txt | grep -c -F 'the run was ended by the round at case 258'
OUT: 0
grep_exit=1
CMD: git -C <lane> show 11b51988...:corpus/evidence/round70/controls/after-battery-completes-r70.txt | sed -n '308,309p' | cat -A
OUT: # RUN-END ADDENDUM (appended by the round after the transcript; the transcript bytes above are untouched): the run was$
OUT: # ended by the round at case 258 (claims-locale-boundary) - its gate ran >70 minutes without emitting the case line$
```
The quoted sentence is **stitched across two lines** (308/309) of the receipt and each half carries
a leading `# ` comment marker. The lesson presents it as a single "ADDENDUM, verbatim" quote. Count
22 is correct; the quote as written does not occur in the file. Whitespace-normalised containment is
also False (`the run was\n# ended by the round…` → `the run was # ended by the round…` ≠ the quote),
because the `# ` prefix is *inside* the join.

### 2.5 S175 — round-71 lesson — stated 6, measured 5 (mismatch)

```
CMD: git -C <lane> show 58232b27d1ea542f4189d093c13f5865521c07ca:corpus/evidence/round71/controls/probe-timeout-capability-r71.txt | grep -n -F 'tprobe_rc=124'
OUT: 5:tprobe_rc=124
CMD: git -C <lane> show 58232b27d1ea...:.../probe-timeout-capability-r71.txt | grep -n -F 'RESEARCH_GATE: CLEAN'
OUT: 16:RESEARCH_GATE: CLEAN (claims=1 supported=1 contradicted=0 ...)
CMD: printf %s 'tprobe_rc=124 real	0m16.333s RESEARCH_GATE: CLEAN' | wc -w
OUT: 5
```
1 + 2 + 2 = 5 whitespace tokens, stated 6. Same pattern as S179.

### 2.6 S176 — round-71 lesson — stated 10, measured 9 (mismatch)

```
CMD: git -C <lane> show 11b51988d3878cd33b826295304f6f266718ba86:corpus/evidence/round70/controls/before-g08-selftest-partial.txt | grep -n -F 'tools/research-gate.sh: line 5548: /tmp/chousa-research-gate-selftest.dcCFup/r6-manifest.jsonl: No such file or directory'
OUT: 65:tools/research-gate.sh: line 5548: /tmp/chousa-research-gate-selftest.dcCFup/r6-manifest.jsonl: No such file or directory
CMD: printf %s 'tools/research-gate.sh: line 5548: /tmp/chousa-research-gate-selftest.dcCFup/r6-manifest.jsonl: No such file or directory' | wc -w
OUT: 9
```
S176 is the *corrected* attribution of S171's quote — the location is right and the quote is
verbatim — but the stated count (10) was copied from S171's defective cell and is off by one.
**The correction row inherits the count defect it was written to fix.** This is a new observation:
the round-71 lesson records the *location* fix and does not re-derive the *count*.

### 2.7 S178 — round-72 lesson — stated 11, measured 13 (mismatch)

```
CMD: git -C <lane> show 7851c4ce29ef4c13d2c6ffd67b2ea1ea2646a536:corpus/lessons/round-71-verifier-spotcheck.md | grep -n -F 'The committed receipts carry **9** (`battery-partial-r71.txt`) + **16** (`killtest-partial-scratch-copy.txt`) = **25** ok-case lines'
OUT: 87:2. **Number drift: "18 healthy ok-case lines … across two runs"** ... The committed receipts carry **9** (`battery-partial-r71.txt`) + **16** (`killtest-partial-scratch-copy.txt`) = **25** ok-case lines; 18 is not re-derivable ...
CMD: printf %s 'The committed receipts carry **9** (`battery-partial-r71.txt`) + **16** (`killtest-partial-scratch-copy.txt`) = **25** ok-case lines' | wc -w
OUT: 13
```
The lesson states "11 words"; the quote carries 13 whitespace tokens. Off by two — the largest
count error in the survey. (This is the very row the round-74 closure later cites for the
"16/11 whitespace tokens" correction of a *different* pair.)

### 2.8 S179 — round-72 lesson — stated 6, measured 5 (mismatch)

```
CMD: git -C <lane> show 97b6ea754b2341cacdfeb29728de0e81c388ad29:corpus/evidence/round72/controls/probe-r72-sizing.txt | grep -n -F 'tprobe_rc=124'
OUT: 6:tprobe_rc=124
CMD: git -C <lane> show 97b6ea754b23...:.../probe-r72-sizing.txt | grep -n -F 'RESEARCH_GATE: CLEAN'
OUT: 16:RESEARCH_GATE: CLEAN (claims=1 supported=1 ...)
CMD: printf %s 'tprobe_rc=124 real	0m18.131s RESEARCH_GATE: CLEAN' | wc -w
OUT: 5
```
Same shape as S175.

### 2.9 S182 / S183 — round-74 lesson — stated 18/13, measured 16/11 (mismatch) — **already corrected in-lane**

```
CMD: printf %s 'Before any successor calibration freeze, exercise a real committed append and a real deletion through `load()`' | wc -w
OUT: 16
CMD: printf %s 'base = check({k: v for k, v in FIXTURE.items()}, {}, set())' | wc -w
OUT: 11
CMD: git -C <lane> show b7803829922770b890e9f4efdd30d12c3695439a:corpus/lessons/round-74.md | sed -n '44p'
OUT: Round 75, routed by `corpus/lessons/round-74-verifier-spotcheck.md` ("The lesson's parenthetical 18/13 counts are inaccurate"). Superseded: this lesson's `## Gate` records the two `Located quote:` sizes as "18 words" and "13 whitespace tokens". The quoted strings carry **16** and **11** whitespace tokens ...
```
`corpus/lessons/round-74.md`'s own `## Correction — round-74 quote counts` block states the true
counts (16 and 11) and names the instrument that derived them. The `## Gate` cells were not
rewritten (append-only, correct). **The lesson is self-consistent; only the raw `## Gate` cells
still read 18/13.** Listed here for completeness — it is *not* an unrecorded defect.

### 2.10 S191 — round-77 lesson — quote absent as a contiguous string (absent)

```
CMD: git -C <lane> show 6defa58dbdc40856f4e7dd24df98dc7ebd3459c0:corpus/lessons/round-76-verifier-spotcheck.md | grep -c -F 'supersede it with an append-only correction entry naming the superseded text'
OUT: 0
grep_exit=1
CMD: git -C <lane> show 6defa58dbdc40...:.../round-76-verifier-spotcheck.md | sed -n '163,164p' | cat -A
OUT:    the artifact a successor will read — supersede it with an append-only correction entry naming the$
OUT:    superseded text, and do not repeat the sentence in a successor claims file.$
```
The lesson says "quote on lines 163–164" and states 11 words — the count is right. The quote is
**split across a line boundary** inside the cited file, so no single line contains it and
`grep -c` returns 0. Whitespace-normalised it *is* present. This is the same class as S174 but with
the join marker *outside* the quote, so normalisation recovers it.

### 2.11 S193 — round-78 lesson — quote absent from the file it cites (absent)

```
CMD: git -C <lane> show 53dbd512d0ab70055338cb44898a6db70049537f:corpus/lessons/round-77-verifier-spotcheck.md | grep -c -F 'SKILL.md registry row `round77 order-and-content battery` is missing its owner cell.'
OUT: 0
grep_exit=1
CMD: git -C <lane> show 53dbd512d0ab...:.../round-77-verifier-spotcheck.md | grep -c -F 'SKILL.md` registry row `round77 order-and-content battery` is missing its owner cell.'
OUT: 1
grep_exit=0
CMD: git -C <lane> show 53dbd512d0ab...:.../round-77-verifier-spotcheck.md | sed -n '156p' | cat -A
OUT: 1. **`SKILL.md` registry row `round77 order-and-content battery` is missing its owner cell.**$
```
The lesson's quote renders `SKILL.md` **without** backticks; the file renders it **with**
backticks (`` `SKILL.md` ``). The lesson's string does not occur in the file at all (not even
whitespace-normalised). The stated count (11) is coincidentally correct for *both* renderings —
the defect is invisible to a word count and only a substring check catches it.

**This is a fourth "located quote absent from the file it cites" case, of the same class as the
round-79 closure's S198 finding, and it is not among the three the closure named.** It is in the
round-78 lesson, one round earlier than S198.

### 2.12 S185 — round-75 lesson — no located quote at all (a format gap, **not** counted among the 12)

```
CMD: git -C <lane> show 43a7a0db52c8aabdf32735f58e09610e05200e79:corpus/QUALITY.md | sed -n '1002p'
OUT: 126. **A counter that runs a candidate tool binds a claim only after a committed detection-forger battery has passed it, and the battery's limits are recorded; this supplements criterion 119.** ...
CMD: git -C <lane> show 43a7a0db52c8...:corpus/QUALITY.md | grep -c -F '126. **A counter that runs a candidate tool binds a claim only after'
OUT: 1
```
The row states "Located anchor: criterion 126's text" — an anchor, not a quote. The cited line
1002 does carry criterion 126, so the *anchor* is right, but there is no located quote and no
count, so there is nothing for a `GATE-RECORD` line to carry. This is a structural gap in the
record format, not a miscount.

---

## 3. The counter's audit window and its own blind spot

### 3.1 What the counter audits, at each `--since-round`

Command (in the scratch clone, so the lane's working tree is untouched; the counter resolves
`LANE` from `parents[3]` of its own path, so it must be run from inside a repo):

```
CMD: python3 -B <scratch-clone>/corpus/evidence/round80/gate-grounding-check.py --rev b7803829922770b890e9f4efdd30d12c3695439a --since-round N
```

| `--since-round` | TIPS | AUDITED | `audited=` |
|---|---|---|---|
| 79 (default) | 191 | **3** | `S196,S197,S198` |
| 78 | 191 | 6 | `S193,S194,S195,S196,S197,S198` |
| 77 | 191 | 9 | `S190,…,S198` |
| 74 | 191 | **17** | `S182,…,S198` |
| 73 / 72 / 71 / 70 / 69 / 60 / 30 / 26 / 1 | 191 | **17** | `S182,…,S198` |

Observed output at the default:

```
LANE_REV=b7803829922770b890e9f4efdd30d12c3695439a SINCE_ROUND=79 TIPS=191 AUDITED=3
ROW S196 record=none quote_words=- location=- verdict=UNRESOLVED
ROW S197 record=none quote_words=- location=- verdict=UNRESOLVED
ROW S198 record=none quote_words=- location=- verdict=UNRESOLVED
GATE_GROUNDING=FAIL unresolved=3 superseded_resolved=0 audited=S196,S197,S198
exit=1
```
This reproduces the frozen control `corpus/evidence/round80/controls/grounding-before.txt`
(`GATE_GROUNDING=FAIL unresolved=3 superseded_resolved=0 audited=S196,S197,S198`, exit 1).

### 3.2 The window delta is real but small: 79 → 60 adds 14 rows

Rows that escape at `--since-round 79` but enter at `--since-round 60`:
`S182, S183, S184, S185, S186, S187, S188, S189, S190, S191, S192, S193, S194, S195` — 14 rows.

### 3.3 The blind spot: 60 → 1 adds **nothing**, and the cap is 17

Widening the window all the way to `--since-round 1` adds **zero** rows beyond `--since-round 60`.
The cause is the counter's `DECIDED` regex (`corpus/evidence/round80/gate-grounding-check.py:22`):

```python
DECIDED = re.compile(r"^- (?:Admit|Reject) (S\d{3,})\b")
```

It matches only the **plain bullet** form `- Admit S###` / `- Reject S###`, which the lane has used
since round 74. Earlier rounds record their decisions in two other shapes, neither of which the
regex matches:

- **markdown table rows** — `| S168 | … |` (rounds 26–31, 48–55, 61–72)
- **bold bullets** — `- **Admit S180**, own-work B: …` (round 73)

Measured census over every `corpus/lessons/round-<n>.md` at the base revision:

```
total rows with a gate decision in a round-N.md lesson: 119
caught by DECIDED: 17
MISSED by DECIDED: 102
```
Broken down by the round whose lesson decided them:
rounds 26–31: 23 rows · 48–55: 49 rows · 61–69: 25 rows · **70: 5 (S168–S172)** ·
**71: 5 (S173–S177)** · **72: 2 (S178, S179)** · **73: 2 (S180, S181)**.

**Blind-spot size: 102 of the 119 gate-decided registry rows are invisible to the counter at every
`--since-round` value.** The counter's audit set is capped at 17 rows no matter how far the window
is widened, while 119 rows carry a Gate decision. Within the round-70..79 band this seat was
assigned, the invisible rows are exactly **S168–S181** (14 rows), which is where 8 of the 12
newly-found defects live (S170, S171, S173, S174, S175, S176, S178, S179).

Two further consequences, both measured:

- **The window is not the only gate — the record format is.** A row whose decision is a table row
  *can* be audited: planting a `GATE-RECORD` for S168 in a scratch `corpus/lessons/round-80.md`
  puts it in the audit set at `--since-round 79`:

  ```
  LANE_REV=9b3dd4db778222321dba67060aa2f40d0a3b2048 SINCE_ROUND=79 TIPS=191 AUDITED=4
  ROW S168 record=ok quote_words=16 location=corpus/lessons/round-69-verifier-spotcheck.md:91@b78038299227 words=16 verdict=OK
  ROW S196 record=none … verdict=UNRESOLVED
  ROW S197 record=none … verdict=UNRESOLVED
  ROW S198 record=none … verdict=UNRESOLVED
  GATE_GROUNDING=FAIL unresolved=3 superseded_resolved=0 audited=S168,S196,S197,S198
  ```
  So the fix for the blind spot is a `GATE-RECORD` line per row, not a wider window.

- **The `SUPERSEDED` branch cannot reach a table-row decision either.** S171 is a *parent* row
  (superseded by S176), so it is never a tip and never appears in `audited=`. The `SUPERSEDED`
  branch fires only when `rid in decided`, i.e. when the superseded row's own id satisfies
  `DECIDED`. For S171 that never happens — the round-70 lesson records it as `| S171 |`. Measured:

  ```
  --- GATE-RECORD for S176 (the superseder) only
      ROW S176 record=ok quote_words=9 location=…/before-g08-selftest-partial.txt:65@b78038299227 words=9 verdict=OK
      GATE_GROUNDING=FAIL unresolved=3 superseded_resolved=0 audited=S176,S196,S197,S198
  --- same, but ALSO a '- Admit S171' bullet so S171 enters `decided`
      ROW S176 record=ok … verdict=OK
      SUPERSEDED S171 by S176 record=ok verdict=RESOLVED
      GATE_GROUNDING=FAIL unresolved=3 superseded_resolved=1 audited=S176,S196,S197,S198
  ```
  So **the one registry row whose Gate record is known-defective and already superseded (S171) is
  structurally invisible to the counter at every window.** The `superseded_resolved` counter the
  C2 predicate names can only ever count superseded rows whose decision was a plain bullet.

### 3.4 The counter's R3/R4 behaviour on the real defective records

Measured by planting each record's own lesson quote and stated count as a `GATE-RECORD` line in a
scratch `corpus/lessons/round-80.md` and running the counter at that scratch commit
(`receipts/r4-probe-out.txt`):

| planted record | counter verdict |
|---|---|
| S193 with the lesson's exact quote | `R3 quote absent from corpus/lessons/round-77-verifier-spotcheck.md:156` |
| S193 with the file's real backticked string | `record=ok … words=11 verdict=OK` |
| S191 (quote spans lines 163–164) | `R3 quote absent from corpus/lessons/round-76-verifier-spotcheck.md:163` |
| S174 (quote spans lines 308–309) | `R3 quote absent from …/after-battery-completes-r70.txt:308` |
| S196 with `words=25` (the lesson's stated count) | `R4 quote is 27 words, record says 25` |
| S196 with `words=27` (the measured count) | `R4 quote is 27 words (contract bound is 25)` |
| S197 with `words=24` (the lesson's stated count) | `R4 quote is 25 words, record says 24` |
| S197 with `words=25` (the measured count) | `record=ok … verdict=OK` |
| S198 with its lesson quote | `R3 quote absent from .ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt:9` |
| S170 `words=10` / S173 `words=21` / S178 `words=11` (lessons' stated) | `R4 quote is 6 words, record says 10` / `R4 quote is 20 words, record says 21` / `R4 quote is 13 words, record says 11` |
| S170 `words=6` / S173 `words=20` / S178 `words=13` (measured) | all three `record=ok … verdict=OK` |

Two consequences the C2 design must absorb:

1. **R4's ≤25-word bound caps the S196 correction.** S196's quote is 27 words; there is no word
   count that makes it pass R4. The row can only be resolved by a **different, shorter** quote (a
   superseding row), never by correcting S196's own count in place. S197's quote is exactly 25 and
   can be repaired in place.
2. **R3 requires a single-line, byte-exact quote.** Every record whose quote spans two source lines
   (S174, S191) or differs from the source by backticks (S193) cannot be expressed as a
   `GATE-RECORD` line at all; the superseding row must carry a *re-quoted* string.

### 3.5 The C2 landing predicate is reachable — measured

The frozen predicate is `GATE_GROUNDING=PASS unresolved=0 superseded_resolved=3` with
`audited=S199,S200,S201,S202`. Built in the scratch clone (four new registry rows whose `teaches`
cells open `supersedes S196/S197/S198`, plus four `GATE-RECORD` lines in a scratch
`corpus/lessons/round-80.md`), with all four quotes re-measured by `wc -w` before planting:

```
LANE_REV=bc3060ac59ba493525d8a50a5d51dfa255132102 SINCE_ROUND=79 TIPS=192 AUDITED=4
ROW S199 record=ok quote_words=13 location=corpus/QUALITY.md:1056@ee70e6df19fe words=13 verdict=OK
ROW S200 record=ok quote_words=11 location=corpus/QUALITY.md:1054@ee70e6df19fe words=11 verdict=OK
ROW S201 record=ok quote_words=2 location=.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt:11@3eb4a3cad8fe words=2 verdict=OK
ROW S202 record=ok quote_words=3 location=.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt:8@3eb4a3cad8fe words=3 verdict=OK
SUPERSEDED S196 by S199 record=ok verdict=RESOLVED
SUPERSEDED S197 by S200 record=ok verdict=RESOLVED
SUPERSEDED S198 by S201 record=ok verdict=RESOLVED
GATE_GROUNDING=PASS unresolved=0 superseded_resolved=3 audited=S199,S200,S201,S202
exit=0
```
**The predicate is reachable, and it is reachable only with a shorter quote for S196** (13 words,
not 27) — which is exactly the shape C2's own sourced claim describes ("the corrected 15-word
located quote that supersedes S196").

The scratch clone was reset to the base revision afterwards (`clone reset: True`); the lane repo
was never written.

---

## 4. Part 4 — where round-79.md's `## Gate` states a word count its own quote does not have

Both are confirmed, with the exact commands:

```
CMD: printf %s 'A subject-identity salt is defeated by any normalizer that knows its marker family, so the closure is a per-channel measurement and not a property of the salt' | wc -w
OUT: 27
CMD: printf %s 'A self-assessment counter validates each resolution line against the bytes it claims to repair, and its audit window covers every block rather than the newest' | wc -w
OUT: 25
```

- **S196 — CONFIRMED.** The lesson states "25 words, `wc -w`"; the quote is **27** words. Off by
  two, and **over the ≤25-word contract bound** — so the round-79 closure's reading ("verbatim, but
  27 words … breaches the ≤25-word bound") is right, and the count error is larger than "off by
  one".
- **S197 — CONFIRMED.** The lesson states "24 words"; the quote is **25** words. Off by one, and
  exactly **at** the ≤25-word bound (25 ≤ 25, so R4's bound does not fire on it — only the count
  mismatch does).

Both statements are in `corpus/lessons/round-79.md:17` and `:24` respectively, and both quotes sit
on the lines the lesson cites (`corpus/QUALITY.md` lines 1056 and 1054 @ `ee70e6df19fe`), so the
*anchor* is right and only the *count* is wrong — matching the round-79 closure's judgement that
the admit decisions stand and only the records are defective.

---

## 5. Summary for the round-80 integrator

1. **12 defective Gate records exist beyond the three the round-79 closure named**, across lessons
   round-70 (S170, S171), round-71 (S173, S174, S175, S176), round-72 (S178, S179),
   round-77 (S191) and round-78 (S193). Counts, locations and commands above.
2. **The defect class is three-way, not one-way.** The round-79 closure found "count off by one" and
   "quote absent". The survey adds a third class the counter also detects: **a quote that differs
   from the source by backticks only** (S193) — invisible to `wc -w`, caught only by `grep -F`.
3. **The counter's blind spot is 102 rows**, not a handful. Widening `--since-round` to 1 adds
   nothing over `--since-round 60`; the `DECIDED` regex cannot see table-row or bold-bullet
   decisions. The 14 round-70..73 rows S168–S181 are exactly the invisible ones.
4. **S171 — a known defect that is still open to the counter** — because it is a parent row whose
   own decision was a table row, so neither the `audited` path nor the `SUPERSEDED` path can reach
   it at any window.
5. **The C2 landing predicate is reachable** (measured, §3.5), and requires a *shorter* S196 quote
   (13 words measured, bound 25) — R4 cannot be satisfied by S196's own 27-word quote at any
   stated count.
6. **A machine-checkable record must carry a single-line, byte-exact quote** (R3) and a count that
   equals `wc -w` of that exact string (R4). Every multi-line or re-rendered record (S174, S191,
   S193) needs a re-quoted superseding row, not a corrected count.

## Receipts (all under `.ufo/waves/round-80/w1/R80ScoutA/receipts/`)

| file | what it is |
|---|---|
| `measure-out.txt` | per-record `git show … \| grep -n -F` + `wc -w` trace, all 33 records |
| `table-out.txt` | the table builder's output: provenance check, the table, the defect list |
| `table.json` | the same table, machine-readable |
| `blindspot-out.txt` | `--since-round` sweep of the counter at the base revision |
| `r4-probe-out.txt` | R3/R4 behaviour of the counter on the real defective records |
| `superseded-probe-out.txt` | the `SUPERSEDED` branch and the S171 blind spot |
| `landing-probe-out.txt` | the C2 landing-predicate reachability probe |
