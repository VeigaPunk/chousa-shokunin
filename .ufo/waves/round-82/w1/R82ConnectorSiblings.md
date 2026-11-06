# R82ConnectorSiblings — seat report (round 82, wave 1)

Seat: `R82ConnectorSiblings` (connector, leaf). Assignment: **sibling-overlap scan, read-only** —
does another lane hold knowledge on research question framing (PICO/PCC/PECO, eligibility derived
from the question), or a gate that refuses placeholder cells (`n/a`, `TBD`, `-`) in records?
Detailed evidence, per-hit quotes and the classification table: `w1/R82ConnectorSiblings/scan.md`.
Nothing absorbed, nothing edited outside this output folder, no claim counter run.

Scratch `/fast/scratch/hyaku/chousa-r82/R82ConnectorSiblings` was created empty for `TMPDIR` and
removed before yield (no clone, archive or fixture was needed: every read was `git show` against a
lane repo). No tool was installed or upgraded.

## Commands, receipts, observed lines, exit codes

All receipts live in `w1/R82ConnectorSiblings/`; `counts.txt` carries their sha256 and line counts.
Working directory for every command: `/home/vgpnk/Projects/shokunin`.

1. **Named scan.**
   `grep -rn -i -E 'PICO|PCC|PECO|question fram|eligibility criteri|placeholder|n/a|TBD' --include=*.md --include=*.py --include=*.sh --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.ufo --exclude-dir=chousa-shokunin .`
   → rc **0**; obs `16002` lines; receipt `raw-grep.txt.gz` (sha256 `8238d50e…`; `zcat | wc -l` = 16002), stderr empty (`raw-grep.txt.err`, 0 bytes).
2. **Framing subset.** `grep -i -E 'PICO|PCC|PECO|question fram|eligibilit(y|ies) criteri' raw-grep.txt`
   → rc **0**, obs **44** lines (`scan-framing-subset.txt`).
3. **Word-bounded frames.** `zcat raw-grep.txt.gz | grep -i -E '\b(PICO|PCC|PECO)\b'`
   → rc **1**, obs **0 lines**. The 10/9/19 substring hits are `pico18_strings`/`picoCTF`, SDDL
   `RPWPCCDCLCSWRCWDWOGA`, and `Pecos`.
4. **Sibling knowledge vocabulary.** `grep -rn -i -E 'research method|research question|systematic review|source verification|claim.vs.source|evidence hierarchy' --include=*.md <each sibling>/corpus/knowledge/` (chousa excluded from the path list)
   → rc **0**, obs **60** lines (`scan-method-vocab-siblings.txt`); none is a question-frame method.
5. **Placeholder machinery.** `grep -E '^\./[^/]+/[^:]*\.(py|sh):' raw-grep.txt | grep -i placeholder`
   → rc **0**, obs **3393** lines (`scan-code-placeholder.txt.gz`), 2441 audio-shokunin RIFF
   `placeholder_ff`/`placeholder_80000000` classes.
6. **Placeholder-cell phrasing.** `grep -rn -i -E 'placeholder (cell|value|vocab|token)' … --exclude-dir=chousa-shokunin .`
   → rc **0**, obs **88** lines (`scan-placeholder-phrase.txt`).
7. **Pins.** `git -C <repo> rev-parse HEAD` and `git -C <repo> rev-parse HEAD:<path>` per cited file
   → `pins.tsv` (15 rows). `git status --porcelain` over all cited paths → rc **0**, empty, so
   worktree = HEAD everywhere.
8. **Committed-byte quotes.** `git -C <repo> show HEAD:<path> | nl -ba | sed -n '<range>p'` per hit →
   `quotes-committed.txt`, `mechanism-quotes-committed.txt`, `kotodama-handoff-gate.txt`,
   `other-vocabularies.txt`, `kagi-placeholder-rule.txt`, `kotoba-census-header.txt`.

Pinned heads (repo → HEAD): tabi `90b9ff04`, kake `dd7a146d`, kengaku `34b28c47`, souji `1c2239cd`,
game-dev-2d `1e033ef0`, kotoba `0344ddae`, kotodama `5fa04a9b`, revenger `654d0929`, kaidoku
`0b518f56`, kagi `f199abc7`, kasegi `4ab54586`, kumitate `d6bbe169`; fleet root
`7a6a6375f823cf3d7375d598448aaacc9794fe5e` (moved from `a77b4ba3…` mid-scan; `CORPUS.md` blob
`882d6ca8…` unchanged); chousa base `142b6f0c…` as reference only.

## Findings

**F1 — no sibling lane holds research question framing (PICO/PCC/PECO, eligibility from the
question).** Evidence: command 3 (obs 0 word-bounded occurrences outside chousa) and command 4 (60
lines, all domain content). The only PICO-level bytes outside chousa are captures inside chousa's own
corpus. Receipts: `scan-framing-subset.txt`, `scan-method-vocab-siblings.txt`. Class: **not contested
— no sibling ground held.**

**F2 — every framing-adjacent hit outside chousa is a deferral to chousa, not a competing claim.**
- `tabi-shokunin/PROVINCE.md:186` (blob `37953cc4…`): `| chousa | adjacent | 378fda82… | PROVINCE.md:5 | question framing; source hierarchy (primary / secondary / aggregator / | tabi opens web sources under chousa's research method and keeps only its own SOURCES rows and browser findings. |`. Pin `378fda82` resolves and `git merge-base --is-ancestor 378fda82… 142b6f0a…` → rc **0**.
- `kake-shokunin/PROVINCE.md:42-43` (blob `fe57a16a…`): "- `chousa` owns research method and source hierarchy; kake keeps only / domain findings and its own `corpus/SOURCES.md` rows."
- `kengaku-shokunin/corpus/knowledge/webarena-task-spec-audit.md:164` (blob `4097220f…`): "Benchmark evaluation stays kengaku; general research method stays chousa, …" — a deferral inside a sibling *knowledge entry*.
- `souji-shokunin/census/round-12/connector.md:32` (blob `8fcd977b…`): "…Owns question framing, primary source hierarchy, claim-vs-source verification…"; souji "adopts Chousa's citation standards".
- fleet `CORPUS.md:119-122` (blob `882d6ca8…`): "**No second method.** … the research method stays chousa's (`chousa-shokunin/SKILL.md`: question → source hierarchy → citation chain → claim-vs-source check)."
Receipt: `quotes-committed.txt`. Class: **not contested.**

**F3 — an independent cross-lane census already classifies chousa `adjacent` with no framing
overlap.** `kotoba-shokunin/corpus/knowledge/sibling-overlap-census-round74.md:51,54` (blob
`6c8d65b5…`), header `| lane | branch | commit | skill file | classification | names kotoba | arbitration | scope quote at | scope quote |`, row `| chousa | master | 00f8c7f5… | SKILL.md | adjacent | no | yes: kasegi, kengaku | PROVINCE.md:3 | "deep-research method (調査) — the reusable craft of source research." |`.
kotoba names only **kasegi and kengaku** as sharing any chousa surface. chousa pin `00f8c7f5` is an
ancestor of base `142b6f0a` (`git -C chousa-shokunin merge-base --is-ancestor`, rc **0**). Receipt:
`kotoba-census-header.txt`.

**F4 — stronger same-axis mechanism (placeholder refusal): `kotodama-shokunin/tools/gates/handoff-packet-check.py`.**
Live gate; blob `6920bc44…`; `PLACEHOLDERS = {"", "-", "--", "—", "–", "n/a", "na", "n.a.", "tbd",
"t.b.d.", "todo", "unknown", "(to-verify)", "to-verify", "?"}` at `:144-160`, `_is_placeholder` at
`:197-198`, refusal `HO-EMPTY` at `:495-503` with message "carries only a blank/placeholder value
(contract §4 required content; §11: unknowns are not blank cells)", planted fixture `TBD` at
`fixtures/handoff-packet-check.md:11`. Distinct properties: the set is closed, `none` is *deliberately
absent* and routed to its own finding id (`HO-BASELINE`) rather than accepted or refused, and the
membership rationale sits beside the set. Province: lore handoff packets — **not contested with
chousa**; reported, not absorbed. Receipt: `kotodama-handoff-gate.txt`.

**F5 — stronger same-axis mechanism (different unit of measure): `kasegi-shokunin/corpus/instruments/r38-closure.sh` G3.**
Blob `5137088c…`; `:80-88` requires the added (`+`, not `+++`) lines of `git diff <base> <ref>` to
contain zero occurrences of a per-round widened vocabulary (`⟨pending`, `<fill`, `filled by the L1`,
`<LANE_HASH>`, `<r38-`) and zero word-bounded `TBD`/`TODO`; `:1164` plants `TODO fill this line in`
and `:1170` asserts the gate fires (`st_neg G3 added-placeholder-token … 'added-placeholders=1'`).
Diff-scoped, so pre-existing tokens cannot create false findings. Province: kasegi closure — **not
contested**. Receipt: `other-vocabularies.txt`.

**F6 — hazard to carry (not a claim): mixed-dash normalization, with a sibling incident.**
`revenger-shokunin/SKILL.md:132` (blob `a827ceeb…`): "a `used-by` placeholder cell (`—` em dash
U+2014, `–` en dash, ASCII `-`/`--`, empty) means NO citation sites; machine parsers must treat the
whole placeholder set as empty — a parser excluding only ASCII hyphens reads the em-dash form as a
path (the r86 preprobe printed 20 phantom no-disk rows before the cross-check caught it)".
Receipt: `other-vocabularies.txt`. Class: **hazard note** for any counter that matches the declared
`-`/`--`/`---`/`–`/`—` forms by literal instead of after the declared normalization.

**F7 — contrast precedent: `n/a` treated as a valid decision value.**
`revenger-shokunin/corpus/lint_entry.py:122-125` (blob `84eb4404…`): the CLEAN self-test fixture
carries `| Q02 | n/a | y |`; the lint's only cell rule is "decision cell non-empty". Receipt:
`mechanism-quotes-committed.txt`. Class: **unrelated province, relevant contrast** — the placeholder
class is a local convention, not a fleet norm.

**F8 — narrower live rules, listed so nothing is hidden.** `kotoba-shokunin/verifiers/check_gate_registry.py:42,220,320`
("the write-scope cell is non-empty and not a dash", control replaces the cell with `—`);
`kaidoku-shokunin/tools/round-50/c2-record.py:883-888` (bare `none` refused unless `none — <reason>`);
`kaidoku-shokunin/tools/round-30/settle-gate.py:152-157` (blank/dash sha allowed only where a blank is
legitimate); `kagi-shokunin/corpus/QUALITY.md:45` QM7 (placeholder token in a *tracked* artifact fails
the stamp; `<FILL …>`/`<LINES>`/`TODO` allowed only in an uncommitted draft);
`game-dev-3d-shokunin/reports/round-102/stub-cleanliness.md:29-31` (report-level census, names the
word-boundary-vs-substring split). Receipts: `mechanism-quotes-committed.txt`,
`kagi-placeholder-rule.txt`, `other-vocabularies.txt`.

**F9 — adjacent ground that is not a lane's knowledge: fleet `CORPUS.md:126-128` already requires a
PRISMA-inspired search log.** Quote: "**Search log.** PRISMA-inspired, not PRISMA-compliant:
question/query, where searched, date, identified / screened / included / excluded counts, exclusion
reasons, stop rationale. A negative claim carries its sweep." It is a search-log requirement, not a
decision table on choosing or aligning a frame — so it is not base-list `knowledge/` ground and not a
K4 subject — but a new entry that restates it duplicates the fleet contract. Receipt:
`quotes-committed.txt`. Class: **flag for the L1; this seat does not judge it.**

**F10 — citation-locality defect in a sibling report (reported, not fixed).**
`game-dev-2d-shokunin/reports/round-105/r105-R105Connector.md:25` (blob `5c03b62e…`) cites
"`SOURCES-CONTRACT-v1.md:52-55` (contract rule 3)". `find /home/vgpnk/Projects/shokunin -name
SOURCES-CONTRACT-v1.md -not -path '*/.git/*' | wc -l` → **1** line, the file being
`./.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`; `git ls-files --error-unmatch
.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` → rc **0**. The cited **line range is accurate** (rule 3 =
52-55; line 56 opens rule 4) — an earlier draft of this report said "overruns by one line"; that was
wrong and is corrected here from committed bytes. The defect is the **path only**: a bare
`SOURCES-CONTRACT-v1.md` does not resolve relative to the report or to `chousa-shokunin/`, and the
real location sits under `.ufo/waves/kaika/`, which a lane scan normally excludes. Receipt:
`quotes-committed.txt`.

**F11 — stronger mechanisms on the harm/selftest axes (notes, not assimilations).**
`kumitate-shokunin/scripts/harm-matrix.mjs:9-20` (blob `95ff189f…`): a registry of the lane's gates
run at BASE and TIP in separate sandbox clones, one transition row per gate (`HELD`, `REPAIRED`,
`HARM`, `HARM_ABSENT`, `GONE`, …), CLEAN only when exit ∈ `ok_exit` and the **last** verdict line
carries a `clean` word, otherwise FAIL_CLOSED; registry `harm-matrix-gates.json` (blob `7333c363…`)
carries per-gate `scope` naming sandbox-pure vs host-state. `scripts/gate-mutants.mjs:6-11` (blob
`977711b4…`): kill predicate requires an evaluable run, `VERDICT: FAIL`, and an immediate second run
with the same sorted FAIL case names (else UNSTABLE, exit-2 class). `kengaku-shokunin/plans/round97_gate_selftest_census.py:18-25`
(blob `35704df7…`): anti-laundering legs `ROW-REMOVED / ROW-DUPLICATE / CELL-CHANGED / DEMOTED /
SCRIPT-CHANGED / MISMATCH` over a lane's gate registry at base and rev. Receipts:
`mechanism-quotes-committed.txt`. Class: **stronger sibling mechanisms on C1's harm/selftest axes;
none is over research records and none is contested with chousa's province.**

## Residuals

- The named scan's `n/a` term (10252 lines) is dominated by other lanes' own evidence tables; I did
  not classify all of it line by line, only the `placeholder cell/value/token` and `TBD`-cell forms
  (commands 5-6). A claim that no *other* phrasing of the placeholder class exists in a sibling is
  therefore not made.
- Fleet root HEAD moved during the scan (`a77b4ba3…` → `7a6a6375…`); `CORPUS.md`'s blob did not. I
  wrote nothing in the fleet root and cite the blob, not the head, for that file.
- No claim predicate was run by this seat: `k2-gate-r82.py`, `depth-r82.py` and the gate `--selftest`
  are untouched here, so this report asserts nothing about C1 or C2 at the landing revision.

VERDICT: R82ConnectorSiblings C1 n/a — this seat ran no C1 predicate; its sibling scan found four live placeholder-refusal mechanisms in other lanes (kotodama closed vocabulary, kasegi diff-scoped sweep, kagi QM7, revenger declared set) but none over research records, so no sibling evidence either confirms or refutes operability at the landing revision.
VERDICT: R82ConnectorSiblings C2 n/a — this seat ran no C2 counter; its sibling scan found zero word-bounded PICO/PCC/PECO occurrences and zero question-frame decision content outside chousa, and the only prior art is the fleet CORPUS.md search-log rule plus four explicit deferrals, so novelty is neither certified nor refuted here.
