# R82ConnectorSiblings — sibling-overlap scan (round 82, read-only)

Seat: `R82ConnectorSiblings` (leaf, connector). Lane: `chousa-shokunin`.
Question asked of this seat: **does another lane hold knowledge on research question framing
(PICO/PCC/PECO, eligibility derived from the question), or a gate that refuses placeholder cells
(`n/a`, `TBD`, `-`) in records?**

Nothing absorbed, nothing edited outside this output folder. No sibling working tree was written.
No claim counter was run: this seat measures sibling overlap, not the round's frozen predicates.

## 0. Revisions read (pinned before reading; `pins.tsv`)

| repo | HEAD | cited file blob |
|---|---|---|
| fleet root (`/home/vgpnk/Projects/shokunin`) | `7a6a6375f823cf3d7375d598448aaacc9794fe5e` (was `a77b4ba3…` at 17:00Z — moved mid-scan by another actor; `CORPUS.md` blob unchanged) | `CORPUS.md` = `882d6ca87fac60c0df1c038711c21259c873a39e` |
| tabi-shokunin | `90b9ff045542651fb59814fe32f73fee0d1d8243` | `PROVINCE.md` = `37953cc494870c03afceafe5fd483f9372776d8a` |
| kake-shokunin | `dd7a146df338ec3de07a88f08f36c8278760afec` | `PROVINCE.md` = `fe57a16ae42090151359206e51e879ef25bf4f32` |
| kengaku-shokunin | `34b28c47bc38b4e0aa11f44f2dfe7c9470d551ac` | `corpus/knowledge/webarena-task-spec-audit.md` = `4097220f3afffe29f24ae252fab135cd05115409`; `plans/round97_gate_selftest_census.py` = `35704df7cce6fa55292968bd5110eb4d6fdbef88` |
| souji-shokunin | `1c2239cd13c8b1c9a2e0786509940754d58664d5` | `census/round-12/connector.md` = `8fcd977b39acf37173d061f64cd6a47bc0d12e93` |
| game-dev-2d-shokunin | `1e033ef053beedf9a201daa21fbeb9c8b2f72dc3` | `reports/round-105/r105-R105Connector.md` = `5c03b62e28f5d67ea3ee775a76eaf37cb1ff5f70` |
| kotoba-shokunin | `0344ddaea831b92546360a55ae02db2654fbccf8` | `verifiers/check_gate_registry.py` = `95ffed389f483c3d6f93db3c08dcfdb9a2240576`; `corpus/knowledge/sibling-overlap-census-round74.md` = `6c8d65b56199b7ab7b4a99dba56ee928fbf01422` (`…round49.md` = `6b966d0182c962c616040d6092c45c734cd804c0`) |
| kotodama-shokunin | `5fa04a9bbda25aa31c8270265fd9997eb97d9ebb` | `tools/gates/handoff-packet-check.py` = `6920bc449f7c09f2ceb82d52f8ec1b63b5575952`; `tools/gates/provenance-audit.py` = `428c5b15fedf66ae36bddf2fdcd97d70d49d0d0b` |
| revenger-shokunin | `654d09298960d0886274d37a0492b8e6d98b2c96` | `corpus/lint_entry.py` = `84eb44045ec0ddcdbb755e87a1a6d3f9ef079fe3`; `SKILL.md` = `a827ceeb9cc569e0e01799f221dd672cf3f26323` |
| kaidoku-shokunin | `0b518f568da7b40a4ab026508d63c942faa7badf` | `tools/round-50/c2-record.py` = `214f2065c3d44816c711e0d701aa9f1dd1cb9f4a`; `tools/round-30/settle-gate.py` = `14db0a72251e288963655f28857b395ec2753340` |
| kagi-shokunin | `f199abc7ae2fe94c31d395721e231dd243b36e6e` | `corpus/QUALITY.md` = `3ad95bd83848eb0c9826598dd7c5d3aff9e153f6` |
| kasegi-shokunin | `4ab545865f747fca8456370b5927fe51236fe579` | `corpus/instruments/r38-closure.sh` = `5137088c4326f54e96f939f1b1ece2cb81c67477` |
| kumitate-shokunin | `d6bbe1690bfc520ddf49787f0bdde2e32ce2cbb0` | `scripts/harm-matrix.mjs` = `95ff189ff6110305a019f65a92be37ce4cdf18f3`; `scripts/gate-mutants.mjs` = `977711b4e7aaaabb69698badf4f8b98e4152cb09`; `harm-matrix-gates.json` = `7333c363a8e97b84618eb9b089ff60830f0e59dd` |
| chousa-shokunin (base `142b6f0c…`) | reference only, not a sibling | `SKILL.md` = `5dbb95d156390da5408949594edf37facc31275e`; `PROVINCE.md` = `0f94a0c4f73cec2e36d587b199d7c43716ceae8c` |

Every quote below was re-read from **committed bytes** (`git -C <repo> show HEAD:<path>`), not the
working tree; `git status --porcelain` over every cited path printed nothing (rc 0), so worktree =
HEAD for all of them. Raw captures: `quotes-committed.txt`, `mechanism-quotes-committed.txt`,
`kotodama-handoff-gate.txt`, `kotoba-census-header.txt`, `other-vocabularies.txt`,
`kagi-placeholder-rule.txt`.

## 1. Command and answer for the named scan

```
cd /home/vgpnk/Projects/shokunin
grep -rn -i -E 'PICO|PCC|PECO|question fram|eligibility criteri|placeholder|n/a|TBD' \
  --include=*.md --include=*.py --include=*.sh \
  --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.ufo \
  --exclude-dir=chousa-shokunin .
```
obs: rc 0, **16002 lines** → `raw-grep.txt.gz` (sha256 `8238d50e…`, `zcat | wc -l` = 16002).
The `n/a` term alone accounts for 10252 lines (audio 5548, souji 718, game-dev-2d 561, …) and `TBD`
for 205; both are dominated by unrelated vocabulary (RIFF size placeholders, `n/a` in other lanes'
own evidence tables). The useful split:

| filter | command | obs |
|---|---|---|
| framing terms | `grep -i -E 'PICO\|PCC\|PECO\|question fram\|eligibilit(y\|ies) criteri' raw-grep.txt` | rc 0, 44 lines → `scan-framing-subset.txt` |
| word-bounded PICO / PCC / PECO | `zcat raw-grep.txt.gz \| grep -i -E '\b(PICO\|PCC\|PECO)\b'` | rc 1, **0 lines** |
| placeholder machinery | `grep -i 'placeholder' raw-grep.txt` restricted to `*.py`/`*.sh` | rc 0, 3393 lines → `scan-code-placeholder.txt.gz`; 2441 of them audio-shokunin RIFF `placeholder_ff`/`placeholder_80000000` classes |
| placeholder *cell/value/token* phrasing | `grep -rn -i -E 'placeholder (cell\|value\|vocab\|token)' …` | rc 0, 88 lines → `scan-placeholder-phrase.txt` |
| sibling knowledge vocabulary, chousa excluded | `grep -rn -i -E 'research method\|research question\|systematic review\|source verification\|claim.vs.source\|evidence hierarchy' --include=*.md <each sibling>/corpus/knowledge/` | rc 0, 60 lines → `scan-method-vocab-siblings.txt` |

**Word-bounded `PICO`, `PCC`, `PECO` occur zero times anywhere outside chousa.** The 10 `PICO` hits
are substrings (`pico18_strings`, `picoCTF` challenge names in revenger), the 9 `PCC` hits are
inside SDDL strings (`RPWPCCDCLCSWRCWDWOGA`, tsukuroi) and one PE resource report, the 19 `PECO`
hits are `Pecos` (kotodama's ancestral-Puebloan entry).

### 1a. Every framing-adjacent hit, classified

| hit | quote (committed bytes) | classification |
|---|---|---|
| `tabi-shokunin/PROVINCE.md:186` | `\| chousa \| adjacent \| 378fda82dc2cbcc555a0565052cc408121813cef \| PROVINCE.md:5 \| question framing; source hierarchy (primary / secondary / aggregator / \| tabi opens web sources under chousa's research method and keeps only its own SOURCES rows and browser findings. \|` | **not contested — deferral.** tabi claims no question-framing ground; it routes its searches through chousa's method. Its pinned chousa head `378fda82` resolves and is an ancestor of base `142b6f0a` (`git merge-base --is-ancestor`, rc 0) — stale pin, valid ancestry. |
| `kake-shokunin/PROVINCE.md:42-43` | "- `chousa` owns research method and source hierarchy; kake keeps only / domain findings and its own `corpus/SOURCES.md` rows." | **not contested — deferral.** |
| `kengaku-shokunin/corpus/knowledge/webarena-task-spec-audit.md:164` | "Benchmark evaluation stays kengaku; general research method stays chousa, reusable testing patterns / stay tameshi, prompt-writing advice stays kotoba, actual web-property operations stay kake." | **not contested — deferral inside a knowledge entry** (a sibling's *entry*, not only its PROVINCE, routes research method to chousa). |
| `souji-shokunin/census/round-12/connector.md:32` | "Deep-research methodology (`…/chousa-shokunin/PROVINCE.md:3,5,10`). Owns question framing, primary source hierarchy, claim-vs-source verification, referential integrity gates." … "Souji adopts Chousa's citation standards for `corpus/SOURCES.md` and knowledge entries" | **not contested — third-party census assigns the ground to chousa and adopts its standard.** |
| `game-dev-2d-shokunin/reports/round-105/r105-R105Connector.md:25` | "- `chousa-shokunin/SKILL.md:6-21` and `SOURCES-CONTRACT-v1.md:52-55` (contract rule 3): Question framing → source hierarchy (primary > secondary > aggregator > unsourced) → citation chain → claim-vs-source verification." | **not contested — pointer to chousa.** Citation-locality defect (§4). |
| `kotoba-shokunin/corpus/knowledge/sibling-overlap-census-round74.md:51,54` | header: `\| lane \| branch \| commit \| skill file \| classification \| names kotoba \| arbitration \| scope quote at \| scope quote \|`; row: `\| chousa \| master \| 00f8c7f5272a1d98b6d34913985fa4537e00aaf9 \| SKILL.md \| adjacent \| no \| yes: kasegi, kengaku \| PROVINCE.md:3 \| "deep-research method (調査) — the reusable craft of source research." \|` | **not contested.** kotoba's cross-lane census classifies chousa `adjacent`, arbitration `yes: kasegi, kengaku`, i.e. it names **no** question-framing overlap; only kasegi and kengaku share any surface at all. chousa pin `00f8c7f5` is an ancestor of base `142b6f0a` (rc 0). |
| `kake-shokunin/corpus/knowledge/crux-keyless-check.md:26` | "It does not establish eligibility criteria, revise the held methodology, authorize credentials, …" | unrelated — a scope disclaimer, no frame. |
| `kasegi-shokunin/corpus/knowledge/cna-assignment-and-vulnerability-rules.md:13` | "These are CVE Program rules for CNAs, not universal bounty eligibility criteria." | unrelated — bounty/program eligibility, not review-question eligibility. |
| `kotodama-shokunin/corpus/SOURCES.md:447` | "…College of Arms… Granting of Arms… page captured 31 October 2025…" | unrelated — `PCC` substring/noise; genealogy source row. |
| `kasegi-shokunin/corpus/SOURCES.md:169` | "Round-62 bounded CERT Guide screen… question — does CERT/CC's phase-to-five-role matrix add a report-review attribution beyond held CISA program stages…? Where — …" | **sibling practice, not knowledge.** kasegi *uses* a bounded question + "Where" statement in a SOURCES row; it holds no frame taxonomy and claims none. |

**Answer A:** no sibling lane holds knowledge, a decision table, or a gate on choosing or aligning a
review question frame. The only PICO-level material anywhere in the fleet outside chousa is *captured
source text inside chousa's own corpus* (base `corpus/captures/34fcefc1….txt`, `16fe8487….txt`), which
is chousa's province, not a sibling's.

## 2. Placeholder-cell refusal: what siblings actually run

Two live gate-shaped mechanisms and four weaker/report-level precedents. None is over research records.

### 2a. `kotodama-shokunin/tools/gates/handoff-packet-check.py` — live, closed vocabulary, per-field carve-out

```
141  # Values that mean "no evidence supplied". `none` is deliberately absent:
142  # §4 accepts `none` for baseline_bible_ref (routed to HO-BASELINE), and an
143  # explicit "no open questions" is content.
144  PLACEHOLDERS = {
145      "",  "-", "--", "—", "–", "n/a", "na", "n.a.", "tbd", "t.b.d.", "todo",
156      "unknown", "(to-verify)", "to-verify", "?",  }
197  def _is_placeholder(value):
198      return _norm_cell(value).lower() in PLACEHOLDERS
495          elif _is_placeholder(entry["value"]):
496              findings.append(_finding("HO-EMPTY", "FAIL",
500                  f"required field `{name}` is present at {entry['where']} but carries only a "
501                  "blank/placeholder value (contract §4 required content; §11: unknowns are not blank cells)"))
```
Fixture `tools/gates/fixtures/handoff-packet-check.md:11`: "HO-EMPTY ×1 — `subject_refs` is `TBD`
instead of namespaced candidate IDs."

Classification: **stronger sibling mechanism worth noting on the same axis as C1's class refusal.**
Same shape as chousa's declared class (closed set, lower-cased, normalized cell), plus two things
chousa's rule does not have: (i) a *licensed sentinel* (`none`) removed from the set and routed to its
own finding id instead of being refused or silently passed — the operability distinction between "no
evidence" and "declared absence"; (ii) membership rationale recorded in a comment beside the set.
Vocabulary delta against the frozen chousa set: kotodama refuses `n.a.`, `t.b.d.`, `(to-verify)`,
`to-verify` (all outside chousa's declared class → residual, not kill) and does **not** refuse `none`,
`nil`, `null`, `x`, `same`, `ditto`, `see above`, `idem`, `...`, `…`, `??`, `---`, `not applicable`
(inside chousa's class). Province: kotodama's lore/handoff packets — not contested with chousa.

Also live in the same lane: `tools/gates/provenance-audit.py:315,323` —
"'- sources:' names no source (blank or placeholder value only)" / "'- couples:' names nothing it
connects (blank or placeholder value only)". Narrower: two named fields, two finding keys.

### 2b. `kasegi-shokunin/corpus/instruments/r38-closure.sh` G3 — live, widened vocabulary over added diff lines

```
80  #   G3 (D-C) Pending-marker resolutions. … and the added (`+`,
84  #       not `+++`) lines of `git diff <base> <ref>` over the lane tree, minus
85  #       `.ufo/` and this suite's own paths, contain ZERO occurrences of the
86  #       widened placeholder vocabulary (`⟨pending`, `<fill>`,
87  #       `filled by the L1`, `<LANE_HASH>`, `<r38-`) and ZERO word-bounded
88  #       `TBD` / `TODO`. The base commit is a constant of this file.
1157 # a green resolutions section, so only the placeholder vocabulary is reopened
1164   printf 'TODO fill this line in\n' > "$repo/corpus/lessons/r38-probe.md"
1170   st_neg G3 added-placeholder-token "$repo" "$c1" 'added-placeholders=1' \
```
Classification: **stronger sibling mechanism (different unit of measure).** It does not police cells;
it polices *added lines* between a frozen base and a ref, with a closed per-round vocabulary, and it
ships a negative fixture that plants `TODO fill this line in` and requires the gate to fire. Two
transferable properties: the vocabulary is *widened per round from the previous round's lesson*
(round-37 → round-38), and the sweep is diff-scoped so pre-existing tokens do not create false
findings. Province: kasegi's own closure gate — not contested.

### 2c. `kagi-shokunin/corpus/QUALITY.md:45` (QM7) — rule, not a gate

"A placeholder token in a durable artifact fails the stamp; `<FILL …>`, `<LINES>` and `TODO` are
allowed only in an uncommitted draft, and a named-debt row is not the fix." Defect form: "`<…>`,
`TODO` or `FILL` tokens in a tracked file; the same debt row open across rounds."
Enforcement point in `corpus/claim-ledger.sh:1017` skips "ellipsis/placeholder tokens … shapes, not
artifacts". Classification: **adjacent quality rule** (tracked-vs-draft boundary, not cell values).

### 2d. `revenger-shokunin/SKILL.md:132` — declared placeholder *set* with an incident behind it

"a `used-by` placeholder cell (`—` em dash U+2014, `–` en dash, ASCII `-`/`--`, empty) means NO
citation sites; machine parsers must treat the whole placeholder set as empty — a parser excluding
only ASCII hyphens reads the em-dash form as a path (the r86 preprobe printed 20 phantom no-disk
rows before the cross-check caught it) | … orphan_sweep7 `USED_BY_PLACEHOLDERS`".
Classification: **hazard note.** revenger's set is a strict subset of the frozen chousa set and its
recorded failure mode is exactly the one a mixed dash vocabulary (`-`, `--`, `---`, `–`, `—`) invites:
a parser that normalizes some forms and not others reads the unnormalized form as data. Relevant to
any counter over `c1-manifest.tsv`/`c1-records/` or `depth-r82.py` that matches dash forms by literal
rather than after the declared normalization.

### 2e. `revenger-shokunin/corpus/lint_entry.py` — the opposite policy, same table shape

`122  \| criterion \| decision \| basis \|` … `125  \| Q02 \| n/a \| y \|` is the **CLEAN** fixture
line; the lint's only cell rule is "decision cell non-empty" (docstring, `lint_qmap`, and the
`QMAP` mutant deletes row Q02 rather than replacing its cell). Classification: **contrast precedent** —
`n/a` is treated as a legitimate decision value in revenger's entry schema. Reinforces that the
placeholder class is a *local convention*, not a fleet norm.

### 2f. Weaker / narrower, listed so nothing is hidden

| mechanism | quote | weight |
|---|---|---|
| `kotoba-shokunin/verifiers/check_gate_registry.py:42`, `:220`, `:320` | "the write-scope cell is non-empty and not a dash"; `if clean(r[6]) in ("", "-", "\u2014", "\u2013"): why.append("write scope empty")`; control `check("empty write scope", …replace("tmp clones", "\u2014")…` | dash-only, one cell of a lane's own gate registry |
| `kaidoku-shokunin/tools/round-50/c2-record.py:883-888` | self-test cell must be `<interpreter> … --selftest` **or** `none — <reason>` (`r'none\s*[\u2014\-:;,]\s*\S+(?:\s+\S+){2,}'`); pinned-value cell same with `{1,}` | refuses bare `none`, not `n/a`/`TBD`; demands a reason instead |
| `kaidoku-shokunin/tools/round-30/settle-gate.py:152-157` | `if sha in ("", "-"): sha = None` … `if row["status"] == "returned" and sha is None: raise Unevaluable(...)` | conditional: dash allowed only where a blank is legitimate |
| `kengaku-shokunin/plans/round97_gate_selftest_census.py:18-25` | anti-laundering legs `ROW-REMOVED / ROW-DUPLICATE / CELL-CHANGED / DEMOTED / SCRIPT-CHANGED / MISMATCH` over a lane's gate registry | not placeholder-related; **stronger sibling mechanism on C1's K3/K4 axis** (§3) |
| `game-dev-3d-shokunin/reports/round-102/stub-cleanliness.md:29-31` | "**strict** … word-boundary `TODO\|TBD\|FIXME\|XXX\|WIP\|PLACEHOLDER`" vs "**seat-spec loose** (the brief's literal list, case-insensitive, substring): `TODO\|TBD\|{{...}}\|pending\|placeholder\|XXX\|FIXME`" | report-level census, no gate file; names the word-boundary-vs-substring hazard |

**Answer B:** no sibling lane runs a gate that refuses `n/a`/`TBD`/dash cells across *research
records*. The two live mechanisms (§2a, §2b) refuse placeholders in a lore handoff packet and in added
diff lines of a bounty lane. Both are same-family instruments; neither has chousa's province or its
`c1-manifest.tsv`/`c1-records/` surface.

## 3. Cross-cutting: stronger mechanisms on the same axes (notes, not assimilations)

- **`kumitate-shokunin/scripts/harm-matrix.mjs:9-20`** — "runs a registry of the lane's gates at BASE
  and at TIP, each revision in its own sandbox clone … HELD · REPAIRED · HARM · HARM_ABSENT · NEW_OK /
  NEW_RED · GONE · CARRIED · CARRIED_MOVED", with "a gate is CLEAN only when its exit code is in
  `ok_exit` AND the LAST line … matching `verdict` carries a word in `clean`", and a registry
  (`harm-matrix-gates.json`, 36 gates, per-gate `scope` naming sandbox-pure vs host-state). This is a
  differential harm instrument over a *registry of gates*; chousa's K3 is a single-record harm rule.
  The transferable idea is the machine-readable registry with per-gate verdict regex + `ok_exit`, not
  the tool.
- **`kumitate-shokunin/scripts/gate-mutants.mjs:6-11`** — K43 kill predicate: "a mutant is KILLED
  iff its run is evaluable …, the selftest exits with a numeric non-zero status, stdout carries the
  exact line `VERDICT: FAIL`, and an immediate second run of the same mutated bytes meets the same
  conditions with the same sorted FAIL case names." Same family as chousa's forgery controls, with an
  added *stability* leg (a second run must agree; otherwise UNSTABLE, exit-2 class).
- **`kengaku-shokunin/plans/round97_gate_selftest_census.py`** — checks that a `gate` row's script
  actually exposes a self-test spelling at the measured revision, with legs that stop a lane from
  laundering the census (a spelling added to a *closed round's* instrument is treated as harm, "not a
  repair"). Complements — does not replace — running the selftest.

Not contested with chousa's province: each is a lane-local instrument over that lane's own artifacts.

## 4. Adjacent ground that is **not** a sibling: the fleet contract already names question framing

Fleet root `CORPUS.md` (blob `882d6ca8…`, tracked) is the fleet-level sources contract, not a lane
knowledge entry:

```
119  3. **No second method.** Claim admission stays in `corpus/QUALITY.md`; the research method
120     stays chousa's (`chousa-shokunin/SKILL.md`: question → source hierarchy → citation
121     chain → claim-vs-source check). `SOURCES.md` duplicates neither; `QUALITY.md` points
122     here for tier definitions.
126  5. **Search log.** PRISMA-inspired, not PRISMA-compliant: question/query, where searched,
127     date, identified / screened / included / excluded counts, exclusion reasons, stop
128     rationale. A negative claim carries its sweep.
```

Two consequences for round 82, stated and not acted on:
1. Rule 3 is the fleet-level assignment of the method to chousa; every deferral in §1a is consistent
   with it.
2. Rule 5 already requires a *search log* with `identified / screened / included / excluded` counts
   and exclusion reasons. That is a search-log requirement, **not** a decision table on choosing or
   aligning a frame, so it is not base-list `knowledge/` ground and not a K4 subject — but a new
   round-82 entry that restates rule 5 in its own rows is duplicating the fleet contract. Flagged so
   the L1 can decide; this seat does not judge it.

## 5. Citation-locality defect found in a sibling report

`game-dev-2d-shokunin/reports/round-105/r105-R105Connector.md:25` cites
"`SOURCES-CONTRACT-v1.md:52-55` (contract rule 3)". Facts, each run:
- `find /home/vgpnk/Projects/shokunin -name SOURCES-CONTRACT-v1.md -not -path '*/.git/*' | wc -l`
  → **1**; the single file is `./.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`.
- `git ls-files --error-unmatch .ufo/waves/kaika/SOURCES-CONTRACT-v1.md` → rc **0** (tracked at the
  fleet HEAD, inside `.ufo/`).
- Line span, from `awk 'NR>=49&&NR<=56'`: line 52 = `3. **No second method.** Claim admission …`,
  53-55 = its continuation ending "here for tier definitions.", line 56 = `4. **Expansion is
  knowledge, not rows.**`. **Rule 3 is exactly 52-55, so the cited range is line-accurate.** An
  earlier draft of this scan recorded an overrun to line 56; that was wrong and is corrected here
  from the committed bytes.
- The *defect* is the path only: a bare `SOURCES-CONTRACT-v1.md` is not resolvable relative to that
  report or to `chousa-shokunin/`, and the real location is under `.ufo/waves/kaika/`, a directory a
  lane scan normally excludes. Classification: **citation-locality defect in a sibling, reported not
  fixed** (sibling is a read-only surface for this seat).

Observation, no action: the fleet root HEAD moved during the scan (`a77b4ba3…` → `7a6a6375…`) while
`CORPUS.md`'s blob stayed `882d6ca8…`; another actor is committing to the fleet root. This seat wrote
nothing there.

## 6. What this seat did not do

- No claim predicate run: neither `k2-gate-r82.py` nor `depth-r82.py` was executed; no gate selftest
  was run; no tree was archived and no gate edit was touched.
- No chousa working-tree content was read for this scan's findings: the named scan excludes
  `chousa-shokunin`, and the two follow-up greps that lacked the exclusion were re-run with it before
  being kept as receipts.
- Nothing was absorbed: no sibling entry was copied, no sibling instrument was imported, no lane was
  edited. No network access (this seat's item names no re-open).

## 7. Classification summary

| sibling artefact | domain | class |
|---|---|---|
| tabi `PROVINCE.md:186`; kake `PROVINCE.md:42-43`; kengaku `knowledge/webarena-task-spec-audit.md:164`; souji `census/round-12/connector.md:32`; kotoba `knowledge/sibling-overlap-census-round74.md:51,54`; fleet `CORPUS.md:119-122` | scope | **deferral to chousa — not contested, no sibling ground held** |
| game-dev-2d `reports/round-105/r105-R105Connector.md:25` | pointer | **deferral + path-locality defect (line range accurate; path resolves only under `.ufo/waves/kaika/`)** |
| kasegi `corpus/SOURCES.md:169` | practice | **uses a bounded question, holds no frame taxonomy** |
| kotodama `tools/gates/handoff-packet-check.py:141-160,495-503` + fixture `:11` | gate | **stronger same-axis mechanism (closed vocabulary + licensed-sentinel carve-out + planted fixture)** |
| kasegi `corpus/instruments/r38-closure.sh:80-88,1157-1170` | gate | **stronger same-axis mechanism (diff-scoped widened vocabulary + negative fixture)** |
| kagi `corpus/QUALITY.md:45` | rule | **adjacent (durable-vs-draft placeholder rule)** |
| revenger `SKILL.md:132` | hazard | **mixed-dash normalization hazard, with incident** |
| revenger `corpus/lint_entry.py:122-125` | lint | **contrast: `n/a` is a valid decision value** |
| kotoba `verifiers/check_gate_registry.py:42,220,320`; kaidoku `tools/round-50/c2-record.py:883-888`; kaidoku `tools/round-30/settle-gate.py:152-157`; game-dev-3d `reports/round-102/stub-cleanliness.md:29-31` | gates/reports | **narrower or report-level; dash / bare-`none` / stub-token only** |
| kumitate `scripts/harm-matrix.mjs`, `scripts/gate-mutants.mjs`; kengaku `plans/round97_gate_selftest_census.py` | gates | **stronger mechanisms on the harm/selftest axes; not placeholder-related** |
| fleet `CORPUS.md:126-128` | contract | **adjacent: PRISMA-inspired search log already required fleet-wide** |
