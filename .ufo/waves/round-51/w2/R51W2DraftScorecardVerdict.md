# R51W2DraftScorecardVerdict — round-51 SCORECARD block, drafted against measured state

Seat: R51W2DraftScorecardVerdict (leaf) · 2026-10-25 · lane `chousa-shokunin` at `72566c84` (claimed tip `4436e279`, base `9ec1751a`, claims frozen `d603f6f0`).
Tooling: nothing installed (RULES.md read; pacman paused). Scratch `/dev/shm/chousa-r51-R51W2DraftScorecardVerdict/` deleted at the end. All counters run with `env -u ASSIMILATE_CITES` from the lane root.

## 1. Gates replayed at the tip

```
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-count.py; echo RC=$?
… LEGS=5/5 / C1=PASS   RC=0            (fresh nonce; --seed 7 prints the same)
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-supplement.py; echo RC=$?
SHAPE=PASS 3/3 MUTATION=PASS 3/3 CROSS_ENTRY=PASS 3/3 SOURCE_LINE=PASS 3/3
UNKNOWN_SRC=PASS 3/3 CLASH=PASS 3/3 · SUPPLEMENT_LEGS=6/6 · C1_SUPPLEMENT=PASS  RC=0
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c2-count.py; echo RC=$?
ENTRIES=3/3 · BOUND=6/7 (min 5) REFUSED=1 · BOUND_IDS=S107,S108,S109,S110,S111,S112
QUOTE_ROWS=61 ON_BOUND=61/61 · SPAN_IDS=6/6 · QUOTES_IN_{SPAN,ENTRY,LESSON}=61/61
CAPTURE_BOUND=61/61 · SUBSTANCE=PASS · ANCHOR_BOUND=6/6 · INFERENCE_GROUNDED=3/3
QUARANTINE_VERDICTS=6/6 (S104,S105,S111,S112,S114,S120) · QUARANTINE_BLOCKED_ADOPTED=0 · C2=PASS  RC=0
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c3-count.py; echo RC=$?
CAP_ROWS=36 (base 36) · POINTERS=74 (base 74) · RESOLVED_BY_CORRECTION=4 · DANGLING=0 · C3=PASS  RC=0
$ python3 tools/assimilate-rows.py --selftest | tail -2
FIXTURES_SHA256=3b7ad258…bd00 / SELFTEST=PASS findings=27 expected=27   (exit 0)
```

## 2. The two discriminations the C1 verdict rests on

```
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-count.py --tool corpus/evidence/round51/controls/forge-dirname.py
SOURCE_ONLY=PASS … REGISTRY_STRUCTURE=PASS 4/4 · LEGS=5/5 · C1=PASS   RC=0     ← forge passes the frozen counter
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-supplement.py --tool …/controls/forge-dirname.py
SHAPE=PASS 3/3, the other five legs FAIL 0/3 · SUPPLEMENT_LEGS=1/6 · C1_SUPPLEMENT=FAIL   RC=1
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round50/c1-count.py >/dev/null; echo RC=$?   → RC=1 (LEGS=3/5, C1=FAIL)
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round49/c1-count.py >/dev/null; echo RC=$?   → RC=1 (SETS_PASS=2/3, C1=FAIL)
$ ASSIMILATE_CITES=all python3 corpus/evidence/round51/c1-count.py | tail -2   → LEGS=3/5 / C1=FAIL, exit 1
   (so the `env -u` in every command above is load-bearing; rc via PIPESTATUS)
```

`corpus/evidence/round51/measure-r50-at-tip.txt` records the same round-50 counter as `LEGS=5/5 C1=PASS exit=0` at `1d7aba0948cf62f6158f77e220f64320a5b6c6cc` with tool digest `382aca9b…`; the tip tool is `6b975f91…`. The round-49 and round-50 counters are therefore tied to the earlier tool revision, exactly as `corpus/lessons/round-51.md:16` (mistake 3) and `:21` (mistake 8) record. Re-observed, not merely quoted: the forge failing the supplement `1/6`, the real tool `6/6`, and the legacy counters failing at the tip are all my own runs.

Supporting facts checked for the block's other rows: `git grep` at `9ec1751a` over `corpus/knowledge` finds 0 files for 検索式, 検索期間 and 检索策略; the registry has 106 rows at base and 112 at the tip, with no `S107`–`S112` row at base; the six bound captures are dated 2026-10-23 20:38–20:40 and the newest cache file is still 2026-10-24 23:26; all 61 span rows resolve to the `.txt` form (`sha256(.txt)` equals the manifest digest 61/61; none to `.raw`); the four `correction:` targets and the rewritten `SHONEN.md` pointer are real non-empty files/dirs (dir with 9 files; 7039 B, 4069 B, 4175 B, 47 B); the lesson Gate `corpus/lessons/round-51.md:60` says "Admitted as narrowed: three entries".

## 3. The draft does not break the counter it documents

Appended to a `git archive 72566c84 | tar -x` copy (never to the lane) and counted with the lane's frozen counter:

```
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c3-count.py --root /dev/shm/chousa-r51-R51W2DraftScorecardVerdict/tree
CAP_ROWS=39 (base 36) · POINTERS=80 (base 74) · RESOLVED_BY_CORRECTION=4 · DANGLING=0 · C3=PASS   RC=0
```

The six pointer tokens of the three new capability rows were also resolved through the counter's own extractor (`importlib` load of `c3-count.py`, `scorecard_rows`): `DANGLING []`.

## 4. Findings

- **F0 (integration blocker for the block as written).** The block names `corpus/evidence/round51/measure-after.txt` as the pinned after-measurement; that file does not exist at `72566c84` (`ls corpus/evidence/round51/` — no such name). The L1 must land the transcript of §1 (four counter outputs, `lane_revision=72566c84…`, `tool_sha256=6b975f91…`) with the block, or delete the clause. No counter reads it.
- **F1 (dangling reference, reference-drift).** `corpus/evidence/round51/c1-supplement.py:4` says "disclosed in claims-erratum.md E2-E4", but `corpus/evidence/round51/claims-erratum.md` carries only `## E1` at both `4436e27` and `72566c84` (`grep -c '^## E'` → 1; 29 lines). My block discloses E1 only. Fix: file E2–E4, or correct the docstring.
- **F2 (counter defect, calibration class).** `receipt-check.py`'s skill leg cannot read the Gates row it documents: `header()` scans `splitlines()[:5]` (`receipt-check.py:57`) for every file it is given, so `--skill SKILL.md` prints `SKILL_NO_PIN` although `SKILL.md:130` carries `tool-rev: cf642c669b736bfba6b9fbb91fd5b16cb5579d9d tool: tools/assimilate-rows.py`. The pin is not even stale: `git rev-parse cf642c6:tools/assimilate-rows.py HEAD:…` prints one blob `d1483e79` twice. Demonstrated working on a header-carrying receipt instead: `RECEIPT_OK … CHECKS=1 OK=1 FAILS=0 RECEIPT_CHECK=PASS` exit 0.
- **F3.** No landed receipt carries the header form yet (`grep -rn 'tool-rev:' corpus/evidence/` → only `receipt-check.py` itself), so the round's own receipts report `RECEIPT_NO_REV` (`python3 corpus/evidence/round51/receipt-check.py corpus/evidence/round51/measure-r50-at-tip.txt` → `CHECKS=1 OK=0 FAILS=1`, exit 1). The capability is prospective.
- **F4.** C3's pass expression never reads the correction channel (`c3-count.py:118`: `ok = not dangling and len(rows) >= len(brows) and n_ptr >= b_ptr`), which is why the verdict is "existence, not truth"; W1 `R51CritForgeC3`'s V/W pair shows a repair and a retarget printing byte-identical `C3=PASS`. Not re-run by me (wave-1 evidence), so cited, not re-observed.
- **F5, not re-observed:** the frozen C1 counter's id draws can collide and hang it (seeds 13, 182, 324 — `corpus/lessons/round-51.md:21`). I ran the default and `--seed 7` only.

## 5. Surfaces and out of scope

Wrote only this report. Read `SCORECARD.md`, `SHONEN.md`, `SKILL.md`, `corpus/SOURCES.md`, `corpus/lessons/round-51.md`, `QUALITY.md`, `AXES.md` (fleet), the round-51 counters/controls/receipts, four wave-1 reports, and the read-only capture cache. Did not touch the lane tree, the git index, jj, the fleet repo or `shokuknow`; ran none of its campaign tools. Draft-validation copy and scratch deleted.

## 6. Draft block — intended lane path `SCORECARD.md`, appended at EOF after the four `correction:` lines (so the row line numbers those lines name stay valid)

```markdown SCORECARD.md
## Round 51 verdict — 2026-10-25 (adopter v2 cites by `source:` line; Japanese/Chinese search-record theme bound to six documents; pointer repair)

Claims frozen in `corpus/evidence/round51/claims.md` at `d603f6f00f78d64f123d3aed2dd9f8701547a4ba` after scoring their do-nothing controls. After-measurement: the four counters replayed at `72566c84` (outputs in the wave-2 seat reports under `.ufo/waves/round-51/w2/`); the L1 lands the verbatim transcript, with a `lane_revision=` header, as `corpus/evidence/round51/measure-after.txt`. Disclosures: `corpus/evidence/round51/claims-erratum.md` E1 (the C3 extractor stripped a leading dot before any seat scored: `DANGLING=8` → `5`). No fetch; L0 `8d77e6c1` open. Every count runs `env -u ASSIMILATE_CITES`: an ambient `ASSIMILATE_CITES` flips C1 to `LEGS=3/5` (lesson `## Mistakes` row 8).

| claim / axis | before → after | counting command | verdict | tag |
|---|---|---|---|---|
| C1 operability (lowest scored axis, 3/10; capability extension) | base tool `LEGS=1/5`, `C1=FAIL` exit 1 (`corpus/evidence/round51/controls/c1-lane-before.txt`; do-nothing controls at most `2/5`) → `LEGS=5/5`, `C1=PASS` exit 0 on fresh nonces and with `--seed 7`; supplement `SUPPLEMENT_LEGS=6/6`, `C1_SUPPLEMENT=PASS` | `python3 corpus/evidence/round51/c1-count.py`; `python3 corpus/evidence/round51/c1-supplement.py` | **improved narrowly**: the frozen counter cannot tell the tool from a forge that implements none of its five behaviours — `--tool controls/forge-dirname.py` prints `LEGS=5/5 C1=PASS`, while the post-freeze supplement, whose legs vary shapes the frozen counter does not (mutation, cross-entry, `source:` line, unknown source, clash), passes the real tool `6/6` and the forge `1/6` (a near-miss candidate `3/6`); the round-49 and round-50 counters are one-shot against the earlier tool revision — replayed at the tip they print `SETS_PASS=2/3 C1=FAIL` and `LEGS=3/5 C1=FAIL` (both exit 1), where `corpus/evidence/round51/measure-r50-at-tip.txt` records `C1=PASS` at `1d7aba09` | plumbing |
| C2 depth (sourced) | `ENTRIES=0/3 BOUND=0/7 NEW_GROUND=0/3 SUBSTANCE=FAIL C2=FAIL` exit 1 (`corpus/evidence/round51/controls/c2-before.txt`) → `ENTRIES=3/3 BOUND=6/7 REFUSED=1`, `QUOTE_ROWS=61 ON_BOUND=61/61`, `SPAN_IDS=6/6`, `QUOTES_IN_SPAN/ENTRY/LESSON=61/61`, `CAPTURE_BOUND=61/61`, `SUBSTANCE=PASS ANCHOR_BOUND=6/6 INFERENCE_GROUNDED=3/3 QUARANTINE_VERDICTS=6/6 C2=PASS` exit 0 | `python3 corpus/evidence/round51/c2-count.py` | **improved**, as a presence-and-binding result: six of seven staged documents bound to lane rows and `source:` lines with 61 quotes located at their offsets in the `.txt` text form; the seventh (国立保健医療科学院 submission form, staged S125) is refused for its capture form — its text exists only inside the `word/document.xml` zip member (`corpus/lessons/round-51.md:56`) — and entailment is uncounted: the counter reads binding and presence, not whether a quote supports the claim | ground |
| C3 calibration | `CAP_ROWS=36 POINTERS=74 DANGLING=5 C3=FAIL` exit 1 (`corpus/evidence/round51/controls/c3-before-erratum.txt`; `8` on the counter's first run, erratum E1) → `CAP_ROWS=36 POINTERS=74 RESOLVED_BY_CORRECTION=4 DANGLING=0 C3=PASS` exit 0 | `python3 corpus/evidence/round51/c3-count.py` | **improved narrowly**: the four `correction:` lines and the one rewritten `SHONEN.md` line resolve to existing non-empty files; but the pass expression never consults `RESOLVED_BY_CORRECTION`, so a retarget that repairs nothing prints byte-identical stdout (W1 `R51CritForgeC3` pair V/W) and 9 of 24 cheats pass, including 1-byte planted files and rewritten pointer strings with no correction line — the axis it measures is link-rot, not self-assessment truth | plumbing |

The numeric operability scale stays 3/10; its round-1 observable counts three archived inputs, not these tests. No other score is invented.

| axis | verdict | evidence |
|---|---|---|
| operability | **improved narrowly** | C1; `c1-count.py` ends `LEGS=5/5` / `C1=PASS`, `c1-supplement.py` ends `SUPPLEMENT_LEGS=6/6` / `C1_SUPPLEMENT=PASS`, and `tools/assimilate-rows.py --selftest` ends `SELFTEST=PASS findings=27 expected=27`; the same frozen counter scores a 94-line forge `5/5`, the supplement scores it `1/6` |
| depth | **improved** | C2; `c2-count.py` ends `QUARANTINE_BLOCKED_ADOPTED=0` / `C2=PASS` — six documents bound of seven, one refused for capture form, 61 quotes located; three entries admitted as narrowed (`corpus/lessons/round-51.md:60`) |
| calibration | **improved narrowly** | C3; `c3-count.py` ends `DANGLING=0` / `C3=PASS` after four correction lines and one rewritten `SHONEN.md` line; limits: existence not truth, link-rot only (W1 `R51CritForgeC3`, `R51ConnCrossClaim`) |
| coverage | **improved narrowly** | the theme was not held at base: `git grep` at `9ec1751a` over `corpus/knowledge` finds 0 files for 検索式, 検索期間 and 检索策略; J-STAGE, 实验动物与比较医学 and SinoMed rows are new |
| freshness | **unchanged** | this round's six captures are dated 2026-10-23 20:38–20:40; the newest readable capture is still 2026-10-24 23:26, and no capture was taken this round |
| adjacency | **unchanged** | W1 `R51ConnSiblings`: 検索式・検索期間・检索策略・PRISMA-S・灰色文献 0 hits across 20 sibling lanes; `search record` 3 generic hits, none on this theme |

## Capabilities (round-51 addition)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| adopter v2, source-line citation | cites only the ids on an entry's `source:` lines and leaves body-only ids unchanged, lists them in `bodyonly.tsv` and a body-only id that is also a lane id in `bodyclash.tsv`; `--cites all` / `ASSIMILATE_CITES` keeps the round-50 behaviour; refuses an unknown source id and an ill-structured registry (no `## Registry` heading, a row outside it) | `python3 corpus/evidence/round51/c1-count.py`; `tools/assimilate-rows.py` | 51 |
| C1 supplement counter | separates a working adopter from a canned-shape forge on shapes the frozen counter never varies (entry shape, mutation, cross-entry, `source:` line, unknown source, clash): real tool 6/6, forge 1/6 | `python3 corpus/evidence/round51/c1-supplement.py`; `corpus/evidence/round51/controls/c1-supplement-controls.txt` | 51 |
| receipt revision pin | checks a receipt's header against the lane: the named revision is a landed commit, still carries the tool, and the recorded digest matches — `RECEIPT_OK` / `RECEIPT_NO_REV` / `RECEIPT_REV_UNKNOWN` / `RECEIPT_REV_UNLANDED` / `RECEIPT_TOOL_MOVED` / `RECEIPT_DIGEST_MISMATCH`; demonstrated `RECEIPT_OK` on a header-carrying receipt. Named limits: no landed receipt carries the header yet, so every one reports `RECEIPT_NO_REV`; and the skill leg reads only the first five lines of the file it is given, so the pin at SKILL.md:130 is reported `SKILL_NO_PIN` | `python3 corpus/evidence/round51/receipt-check.py`; `SKILL.md` | 51 |

## Planned — round 52 (not started)

Candidates: a zip-member text form for the NIPH submission form (`word/document.xml`, `w:t` runs concatenated), after which the refused seventh document can be re-grounded and bound; the lesson Gate's other neighbourhood entries — `search-log-fields-r36.md` needs a real PRISMA-S capture (its S082 leg is a 267-character challenge page), and the three `admit-later` rows (`search-tracking-record-r40.md`, `chinese-search-log-r37-amendment-2026-10-23.md`, `japanese-prisma-item-wording-r40.md`) each name the cell to repair first; the mutation campaign's survivors against the adopter v2 and the supplement, each survivor named with the leg that missed it; and folding the supplement's six legs into the next frozen counter, since the frozen one admits a forge 5/5.
```

VERDICT: attacked C1's frozen counter (a forge passes it 5/5 while the post-freeze supplement scores the same forge 1/6 and the real tool 6/6, and both legacy counters fail at the tip), C2's binding (6/7 bound, 61/61 quotes located, entailment uncounted), C3's repair (DANGLING=0 but 9/24 cheats pass and the correction channel is outside the pass expression) and the round's own instrumentation (receipt-check's skill leg blind to SKILL.md:130, no landed receipt carrying a header, supplements' docstring citing unfiled E2–E4, and a measure-after file the block names but the tree lacks); the block is drafted to the round-50 shape and, appended to a tip copy, keeps C3 at PASS (CAP_ROWS=39 POINTERS=80 DANGLING=0).
