ATTACKS: sweep r47-vs-r46 inference tool over all knowledge entries × 3 span/counts configs; judge every exit difference and every INF_POLARITY_FLIP finding
VERDICT: defect (calibration) — 2 false-positive `INF_POLARITY_FLIP` findings on `evidence-snapshot-coverage-r40.md` (r45 counts manifest); no exit-code regression

## Setup
- Lane tip `1fc5ed193ad48a482402c862f4e4cc47e46d5b2d`; working tree clean for `corpus/knowledge/`, `tools/inference-ground.py`, `corpus/SOURCES.md`, `corpus/evidence/round45|46|47` (only untracked: round47 `measure-after.txt`). Scratch `/tmp/chousa-r47w2-SweepC1Corpus/`.
- Tools: r47 = `tools/inference-ground.py` (sha256 `244a1897…9667e`); r46 base = `corpus/evidence/round47/controls/base-tool-r46.py` (sha256 `c3ea067e…6bb3` printed by c1-count; not re-hashed here).
- Manifests: r46 `spans.tsv` `d9bdd226…5964`, r45 `spans.tsv` `fbb6862c…80ac`, r45 `counts.json` `ded8747e…665c`, `SOURCES.md` `c69c75bd…6274` — byte-identical to the pins in the wave-1 report (`ExecC1Regress.md:24-25`).

## Commands (verbatim decisive output)
`python3 /tmp/chousa-r47w2-SweepC1Corpus/sweep.py` — 63 entries × 3 configs × 2 tools = 378 runs:
```
RUNS=378 EXIT_DIFFS=0 FLIP_LINES=2
FLIP evidence-snapshot-coverage-r40.md r45all FINDING INF_POLARITY_FLIP bullet=2 token='7,572 / counts key extra_not_frozen/real_source_answers'
FLIP evidence-snapshot-coverage-r40.md r45all FINDING INF_POLARITY_FLIP bullet=2 token='5,959 / counts key extra_not_frozen/filled_web_archive,extra_not_frozen/real_source_answers_web_archive'
```
No exit differs between r47 and r46 under any config. Under r46 spans (a) and r47 spans (c) the two tools' outputs are identical for every entry; under r45 spans+counts (b) the only output differences are the two r47 flip lines above.

## Finding table (entries whose exit or findings differ between tools)
| entry | config | r46 exit | r47 exit | r47 new findings | judge |
|---|---|---|---|---|---|
| `evidence-snapshot-coverage-r40.md` | r45 spans+counts | 1 | 1 | 2× `INF_POLARITY_FLIP` (bullet 2: `7,572`, `5,959`) | both FALSE POSITIVE |
| all other 62 entries × 3 configs | — | identical | identical | none | — |

## Judgment of the two findings (true flip vs false positive)
- Tokens: `7,572` → key path `extra_not_frozen/real_source_answers`; `5,959` → `extra_not_frozen/filled_web_archive` and `extra_not_frozen/real_source_answers_web_archive`. Both paths carry `not` only from the **ancestor group label** `extra_not_frozen` (`KEY_PART_RE` splits `extra_not_frozen` → `['extra','not','frozen']`; `key_negated` → True).
- Entry text (`corpus/knowledge/evidence-snapshot-coverage-r40.md:21`): "Counted over the citations, it is not near-universal. Of the 7,572 answers that name a real source (a `source_url` other than `Metadata`), 5,959 (78.7%) carry a web.archive.org link, the target the README names; the rest carry no archive field, a placeholder or another archiver. Lane arithmetic over S084."
- The figures are affirmative assertions about the capture: 7,572 answers name a real source; 5,959 of them carry a web.archive.org link. No negator follows either figure (`7,572` → `answers that name a`; `5,959` → `carry a web archive`), correctly matching the leaf-key polarity (`real_source_answers`, `filled_web_archive`, `real_source_answers_web_archive` are all positive). `KEY_not_frozen` is a **partition label** — the round-45 recount's extra figures that were not frozen into the round-45 C3 counter (`corpus/lessons/round-45.md:34-45`; `corpus/evidence/round45/build-spans.py:92`; `corpus/QUALITY.md:605-612`) — it does not negate its children's count predicates.
- Verdict: both findings are FALSE POSITIVES — correct, affirmative bullet refused. Not true flips (the bullet asserts the same polarity as the data), not accepted junk. Root cause: the wave-1 key-path fix (`980fe43f`, docstring "a key path's parts … carry its negation") was written for keys whose own name negates the count (`answers_without_key`, `without_archive/count` — `ReviewerC1Polarity` L1/F7), but it reads the negator from ANY ancestor segment, so a group label such as `extra_not_frozen` poisons every figure nested under it. This is a new over-refusal this regress sweep exposes on real corpus text that the wave-1 trace did not (see below).

## Context: why wave-1 missed this
- `ExecC1Regress.md` (wave 1, at `a15610a5`, pre-refinements) reported `0 INF_POLARITY_FLIP` with 17 probe evaluations, including the same r45 manifest (`counts.json` sha identical). That run's commit predates the key-path fix (`git log a15610a5..1fc5ed1` → `980fe43f` "key paths"), whose `count_keys` changed leaf-key names to full ancestor paths (`git diff a15610a5 1fc5ed1 -- tools/inference-ground.py`: `walk(v, str(k))` → `walk(v, f"{path}/{k}")`; new `key_negated`). Under the pre-refinement leaf-key read, `real_source_answers`/`filled_web_archive` are positive and no flip fires — the tip's `TRUE NEGATIVE` is stale for the landed tool.
- The frozen C1 counter checks only the six fixtures (`corpus/fixtures/inference-ground-r47/`), whose counts JSON is flat (`answers_named_source`, `answers_archived`, `answers_without_archive_key`) and cannot reach the nested-group case; `c1-count.py` still prints `C1=PASS` (see below).

## Counter re-runs at tip (verbatim)
```
$ python3 corpus/evidence/round47/c1-count.py
TOOL=present / POSITIVE_PASS=3/3 / JUNK_KILLED=3/3 / CANARY=pass / R46_COUNTER=pass / R46_ENTRIES=2/2 / C1=PASS / exit=0
$ python3 corpus/evidence/round47/c2-count.py --list
ENTRY_POINTS=94 (abc=85 dependence=+2 check_named=+7) FLOOR=92 GATES_ROWS=51 REGISTERED=94/94 UNREGISTERED=0 DANGLING=0 MISMATCHES=0 C2=PASS exit=0
$ python3 corpus/evidence/round47/c3-count.py
ENTRIES=2/2 CITES_BOUND=6/6 QUOTE_ROWS=35 ANCHOR_BOUND=6/6 INFERENCE_GROUNDED=2/2 QUARANTINE_VERDICTS=4/4 QUARANTINE_ABSENT_ADOPTED=0 C3=PASS exit=0
```
(C2 prints `ENTRY_POINTS=94` vs the claim's stated 93; freeze-time counter (`git show 22a44b8b:corpus/evidence/round47/c2-count.py`) was not re-run by me — C2 is out of this seat's scope.)

## Reachability (sweep is not vacuous)
`#### Inference` sections exist in 8 entries; tokens ground only under r46/r47 spans (`evidence-pool-versioning-r39.md` 7, amendment 5) and under r45 counts (r40 7 figures). The r45-counts figure path is the only place P3 (figure flip) is exercised on real corpus text; the two findings above are its entire output.

## Risks / limits
- Scope: r45 manifest is the older side; r40 is not a round-47 C3 entry. The findings affect the C1 probe's calibration on real corpus text, not any frozen counter result.
- I did not run `write xd://report_issue` (no such device configured in this seat).

## Cleanup
`rm -rf /tmp/chousa-r47w2-SweepC1Corpus` (scratch) — run after this report was written. No installs were made. No network egress; no lane files changed (this report is the only lane write). Full results (378-row TSV) were in scratch; the decisive rows are quoted above.
