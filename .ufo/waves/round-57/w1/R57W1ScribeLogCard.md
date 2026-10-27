# R57W1ScribeLogCard — LOG.md `## Round 57` block and SCORECARD round-57 verdict, drafted parametric

seat: scribe · wave: chousa-r57-w1 (one v2 wave) · lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin` · date 2026-10-27
Snapshot time of every read below: **2026-10-27T08:36:00Z**. The tree is live (siblings are writing `corpus/SOURCES.md`,
`refetch.tsv`, `corpus/captures/`), so all numbers here are that instant's, not the after-measurement.

Nothing in this file is a claim measurement. Both frozen claims are counted by their own counters at the L1's
after-receipt; I ran neither counter.

## 1. What I read (each line is a command I ran; output as observed)

| # | command | observed |
|---|---|---|
| R1 | `read corpus/evidence/round57/claims.md` (whole) | C2 and C3 predicates, targets, controls, separability; freeze commits `c2f914c5…` (R57-C2) and `fd95724d…` (R57-C3); `BASE_REV = 6656f077…` |
| R2 | `cat controls/c2-before.txt` | `SET=47 VERDICTS=0/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=0 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL` · `exit=1` |
| R3 | `cat controls/c3-before.txt` | `ENTRY=no S127_CITED=no NEW_GROUND=no CLAUSE=no` / `BOUND=0/7 (min 4) -` / `SWEPT=0/7 -` / `QUOTE_ROWS=0 IN_SPAN=0 … CAPTURE_BOUND=0` / `SUBSTANCE=FAIL ANCHOR_BOUND=0/0 INFERENCE_GROUNDED=no STRAY_IDS=-` / `C3=FAIL` · `exit=1` |
| R4 | `cat controls/c2-controls.txt` | EMPTY `VERDICTS=0/47`; JUNK `VERDICTS=47/47 REPRODUCED=0 DRIFTED=47 BYTE_BACKED=47 CONSISTENT=47/47 FLAGGED=0/47 C2=FAIL`; ALLFAIL `VERDICTS=47/47 UNREACHABLE=47 C2=FAIL` |
| R5 | `cat controls/c3-controls.txt` | HELD `BOUND=1/7 (min 4) R7:S118 SWEPT=6/6 R1 R2 R3 R4 R5 R6 QUOTE_ROWS=5 … STRAY_IDS=S130 C3=FAIL`; CITER `QUOTE_ROWS=6 … STRAY_IDS=S130,S990 C3=FAIL` |
| R6 | `sed -n '240,242p' c2-count.py`, `sed -n '274,285p' c3-count.py` | the two counters' print formats (quoted in §4) |
| R7 | `git grep -c 规范性引用文件 6656f077 -- corpus/knowledge` | no output, `exit=1` → the term is absent from `corpus/knowledge` at BASE_REV (C3 `NEW_GROUND`) |
| R8 | `ls corpus/knowledge/normative-reference-chain-china-r57.md` | `No such file or directory` at snapshot → C3 entry not yet written |
| R9 | `ls corpus/lessons/round-57.md` | `No such file or directory` at snapshot → the C2 flag target and the C3 quote-carrier do not exist yet |
| R10 | `git log --oneline -8` / `git rev-parse HEAD` | tip `a03824d1…` "W1 spec+dispatch (65 seats … attack share 21/65=32%); L1 fetch pass-1 counter run (43/47, 38 REPRODUCED, 5 DRIFTED absent=0)"; below it `f9736a3` (pass-1 fetch, 43 stored), `fd95724` (C3 freeze), `c2f914c` (C2 freeze), `6656f07` (round-56 spot-check) |
| R11 | python over `refetch.tsv` (stdin, no writes) | 50 ids, 105 attempt rows; 47 of 50 ids carry ≥1 successful attempt; no-success ids `S105 S131 S132`; S100/S103/S106 succeeded on attempt 2 at 08:29:33Z/08:29:53Z/08:30:24Z |
| R12 | `grep -P '^(S105|…)\t' refetch.tsv` | `S105 att=1 08:06:12Z rc=28 http=200`; `S105 att=2 08:30:12Z rc=28`; `S105 att=3 08:33:48Z rc=28` → two failures 1440 s apart; `S131` 404/412, `S132` 412/412, `S133` one 200 |
| R13 | `git status --porcelain` | `M corpus/SOURCES.md`, `M corpus/evidence/round57/refetch.tsv`, 4 capture pairs untracked (`6f545e6c…`, `9695437c…`, `ad3010d2…`, `c71776bc…`) |
| R14 | `git ls-files corpus/captures \| wc -l` vs `ls corpus/captures/*.raw/*.txt` | `tracked=97 raw=54 txt=51` → 8 capture files on disk are not yet committed |
| R15 | python over `w1-spec.json` | 65 items: 12 scouts / 21 executors / 13 reviewers / 6 critics / 6 scribes / 2 mutation-testers / 2 connectors / 1 sentinel / 1 revenger / 1 simplifier (matches the `a03824d` subject) |
| R16 | `sed -n '160,270p' corpus/evidence/round57/c3-count.py` | BOUND mechanics: Registry row ≠ S127/S128/S129, first URL not in their set, `used_by`, `source: X — U` line, raw sha256 = `good_raw[(X,U)]`, form carries token + title-as-heading, ≥2 manifest rows of (X,U) with the form digest, one quote holding the title; `anchors_need` = bound rows not in `base_ids` |

## 2. Draft — LOG.md, appended after the Round 56 block

````markdown
## Round 57 — the lane's pinned captures re-fetched into digest-checked lane-owned bytes; the workflow standard's normative references chained by document (2026-10-27)

Intake: the round-56 closure `corpus/lessons/round-56-verifier-spotcheck.md` §6 (the capture-cache dependency, the three unmeasured C1 attacks, hook classes, the r44 lead) and the orchestrator's round-57 note, recorded verbatim in `corpus/evidence/round57/egress-approval.md`: a claim needing captures must re-fetch into lane-owned evidence (committed bytes + sha256), the counters pinned to the deleted campaign cache must not be presented as measurements, and the cache is not recreated under `shokuknow`. The cache was gone at round start, so this round's claims are counter-only and fetch-scoped. Claims froze at `[HASHES]` (C2 `c2f914c5…` before any fetch of the round, C3 `fd95724d…`) after do-nothing controls; no candidate: neither claim lands a tool.

- **C2 freshness.** `corpus/evidence/round57/c2-count.py` (frozen predicate = its docstring) recomputes exactly one verdict per (id, url, capture_sha256) triple the spans manifests pin at `6656f077`: REPRODUCED binds a lane-owned `corpus/captures/<key>.raw` or `.txt` to the pin by sha256 — the one digest-unforgeable part — while DRIFTED and UNREACHABLE are attested by the fetch record. The L1 re-fetched the 47 pinned URLs through `tools/capture-fetch.py` (the campaign recipe, one credential-free GET per attempt, three at most, retries spaced ≥600 s), one row per attempt in `corpus/evidence/round57/refetch.tsv`, bytes under `corpus/captures/<key>.{raw,txt}`; every byte-backed capture is also CONSISTENT (its `.txt` equals the frozen recipe applied to its `.raw`) and every DRIFTED capture whose pinned quote no longer occurs is FLAGGED in this lesson with the counter's own `absent=<a>/<m>`. Before `SET=47 VERDICTS=0/47 REPRODUCED=0 … C2=FAIL` → `[C2_RESULT]` (`c2-measure-after.txt`, lane master `[HASHES]`); controls EMPTY `VERDICTS=0/47`, JUNK `VERDICTS=47/47 REPRODUCED=0 DRIFTED=47 FLAGGED=0/47`, ALLFAIL `VERDICTS=47/47 UNREACHABLE=47`, none meeting the target. At the after-receipt `[C2_DRIFT]`; `[C2_FLAGS]`. Targets REPRODUCED ≥ 5 and BYTE_BACKED ≥ 32, both fixed before any fetch; DRIFTED and UNREACHABLE remain attested, not proved, as `claims.md` disclosed pre-data.
- **C3 depth (sourced).** Entry `corpus/knowledge/normative-reference-chain-china-r57.md` chains S127's `2 规范性引用文件` — seven instruments (R1 〔2019〕80号, R2 〔2021〕16号, R3 管理指南 2021年版, R4–R6 the 抗肿瘤 / 心血管病 / 儿童 技术指南 2022年版, R7 质量控制指南 2024年版, the held S118 binding R7) — to the documents themselves: `[C3_BOUND]` of seven bound, each a Registry row other than S127/S128/S129 whose lane-owned capture's defined text form carries the reference's edition token and its title as a heading and which the entry cites as `source: X — U`, every unbound reference carrying a `- UNBOUND R<k> sweep:` line; `[C3_ROWS]` manifest rows built by `tools/build-spans.py` are quotes of ≤25 words inside their span files at the recorded offsets, and the round-51 `quote-substance-check.py` and `tools/inference-ground.py` both exit 0. Before `ENTRY=no … BOUND=0/7 (min 4) … C3=FAIL` → `[C3_RESULT]` (`c3-measure-after.txt`, lane master `[HASHES]`); controls HELD `BOUND=1/7 (R7:S118) STRAY_IDS=S130` and CITER `BOUND=1/7 … STRAY_IDS=S130,S990`, both `C3=FAIL`. The heading rule found a heading only in S118 and, for R3's title without its `2021年版` token, in S130 — pre-freeze checks of the rule, not measurements.
- **Routed and integration work.** `[ROUTED_WORK]` (default set: the round-56 §6 D1 correction appended to `corpus/knowledge/grey-literature-field-china-r42.md` as `#### Corrections (round 57)`, whose `recheck:` line still reads `the journal's 表 10 row` at my snapshot; QUALITY rows; lesson Mistakes rows; SKILL.md rows for the round-57 counters and the re-fetch tool; census start exit 0 with the same five pre-existing W04, census end likewise).
- **Waves.** One v2 wave, W1 = 65 seats (12 scouts / 21 executors / 13 reviewers / 6 critics / 6 scribes / 2 mutation-testers / 2 connectors / sentinel / revenger / simplifier; attack share 21/65 = 32%), build and attack in the same wave and not split; report filed after `WAVE-DONE w1` (`[WAVE_STATE]`).
````

## 3. Draft — SCORECARD.md, inserted after the `## Planned — round 57 (not started)` block

````markdown
## Round 57 verdict — 2026-10-27 (the pinned captures re-fetched into lane-owned bytes; the workflow standard's normative reference chain by document)

Claims frozen at `[HASHES]` after do-nothing controls (`corpus/evidence/round57/claims.md`; `controls/c2-before.txt`, `c2-controls.txt`, `c3-before.txt`, `c3-controls.txt`), R57-C2 at `c2f914c5…` before any fetch of the round and R57-C3 at `fd95724d…`. No candidate: both claims count a store the lane must hold, not a tool. After-receipts: C2 at lane master `[HASHES]` (`c2-measure-after.txt`), C3 at lane master `[HASHES]` (`c3-measure-after.txt`). **Live fetch this round** under `corpus/evidence/round57/egress-approval.md` (credential-free GET of public documents: the 47 pinned URLs plus the C3 candidates); L0 `8d77e6c1` stays open.

| claim / axis | before → after | counting command | verdict | tag |
|---|---|---|---|---|
| C2 freshness: the 47 pinned (id, url, capture_sha256) triples re-verified from lane-owned bytes | `SET=47 VERDICTS=0/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=0 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL`; controls EMPTY `VERDICTS=0/47`, JUNK `VERDICTS=47/47 REPRODUCED=0 DRIFTED=47 FLAGGED=0/47`, ALLFAIL `VERDICTS=47/47 UNREACHABLE=47` → `[C2_RESULT]` | `python3 corpus/evidence/round57/c2-count.py` | **improved**: every pinned triple carries a verdict recomputed from bytes the lane holds, the REPRODUCED set bound to its pin by sha256 and the remaining two classes printed separately because they are attested by the fetch record and not provable from bytes (`claims.md`, disclosed before data); the wave's attacks: `[ATTACKS]` | freshness |
| C3 depth (sourced): the workflow standard's seven normative references chained to their own documents | `ENTRY=no S127_CITED=no NEW_GROUND=no CLAUSE=no BOUND=0/7 (min 4) QUOTE_ROWS=0 C3=FAIL`; controls HELD `BOUND=1/7 (R7:S118) STRAY_IDS=S130`, CITER `BOUND=1/7 STRAY_IDS=S130,S990` → `[C3_RESULT]` | `python3 corpus/evidence/round57/c3-count.py` | **improved** as binding and located support in the defined forms: `[C3_BOUND]` bound by document, each with its edition token and title as a heading, `[C3_ROWS]` located quotes, every unbound reference carrying its sweep line; entailment of any clause term is uncounted (`[C3_NARROW]`) | ground |

The numeric operability scale remains 3/10; the round-1 score is its narrow archived-export observable, not these counters. No other numeric score is invented.

| axis | verdict | evidence |
|---|---|---|
| operability | **unchanged** | no claim this round lands a tool; the wave's gate and `build-spans` attacks report in `[ATTACKS]`, and the round-56 opens stand (six uncovered gate clauses, `R55W2SentBuilder`'s destructive `--out`) |
| depth | **improved** | C3; `[C3_BOUND]` of the standard's seven references bound by their own documents and `[C3_ROWS]` located quotes in defined forms — the clause's own terms reach `corpus/knowledge` for the first time (`git grep -c 规范性引用文件 6656f077 -- corpus/knowledge` → exit 1) |
| coverage | **improved narrowly** | the same probe (absent at base, `NEW_GROUND=yes` after) and the Registry rows the bound documents add; the seven-reference field is now mapped reference by reference rather than as one held instrument |
| calibration | **[CALIBRATION]** | `[CALIBRATION]` |
| freshness | **improved** | C2; the axis's first measurement that re-derives a pinned digest from bytes the lane holds, with a recipe-consistency check on every byte-backed capture and a flag line for any drifted capture whose quote is gone |
| adjacency | **unchanged** | `[ADJACENCY]` |

## Capabilities (round-57 addition)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| Pinned-capture freshness measurement | re-fetches each URL a spans manifest pins, stores lane-owned bytes keyed by `sha256(url)[:24]`, and returns exactly one verdict per pinned triple from committed bytes — REPRODUCED bound to the pin by sha256, DRIFTED/UNREACHABLE from the attempt record — with a recipe-consistency check on every byte-backed capture and a mandatory absence count for a drifted capture whose pinned quote no longer occurs | `python3 corpus/evidence/round57/c2-count.py [--verbose]`; `corpus/evidence/round57/refetch.tsv`; `c2-measure-after.txt` | 57 |

## Planned — round 58 (not started)

Candidates: hook classes beyond the two frozen probes — `dir_fd` without `chdir`, native `import`, `sqlite3.connect` — as a new frozen probe set with its own red-before; the S101 carrier-alphabet leg; the remaining grey-literature family (r41, r48; r44 refused at round 56) bound by document; still open from earlier rounds: re-run the three unmeasured C1 attacks now that lane-owned captures exist (`R56CritC1Forge`, `R56MutC1Driver`, `R56MutC2Counter`), harden `tools/build-spans.py` (`R55W2SentBuilder`), battery entries for the six uncovered gate clauses, and the r44 lead's flip condition on the centre's 2022/2024 instruments.
````

## 4. Placeholder legend and branch rules (for the L1)

| token | fill with |
|---|---|
| `[HASHES]` | freeze commits and the two after-receipt lane masters, full 40-hex (C2 `c2f914c5…`, C3 `fd95724d…` are known) |
| `[C2_RESULT]` | the counter's whole final line, order fixed by `c2-count.py:240-242`: `SET=… VERDICTS=…/47 REPRODUCED=… DRIFTED=… UNREACHABLE=… BYTE_BACKED=… CONSISTENT=…/… FLAGGED=…/… C2=PASS\|FAIL` |
| `[C3_RESULT]` | the five lines printed by `c3-count.py:274-285` (`ENTRY=…` / `BOUND=…` / `SWEPT=…` / `QUOTE_ROWS=…` / `SUBSTANCE=…` / `C3=PASS\|FAIL`) |
| `[C2_DRIFT]` | the DRIFTED ids and, per id, whether its pinned quote survived (`absent=0`) |
| `[C2_FLAGS]` | either "no `- FRESHNESS-FLAG` line is due (`FLAGGED=g/g` with g = need_flag)" or the flag lines verbatim as written in the lesson |
| `[C3_BOUND]` | the counter's `BOUND=` line verbatim |
| `[C3_ROWS]` | `QUOTE_ROWS=n` with `IN_SPAN/IN_ENTRY/IN_LESSON/SHORT/CONTEXT/CAPTURE_BOUND` all `=n` |
| `[C3_NARROW]` | the wave's C3 narrowings (`R57W1ReviewC3Same`, `R57W1CritC3Stray`, `R57W1CritC3Held`) |
| `[ATTACKS]` | one clause per attack item: what it attacked, survived / falsified, with its report path |
| `[CALIBRATION]`, `[ADJACENCY]`, `[ROUTED_WORK]`, `[WAVE_STATE]` | the D1/QUALITY/lesson/SKILL/census facts, the sibling-overlap result, the seats reporting at filing |

Branch rules — the drafts above are written for the PASS branch; they are NOT valid as-is if either claim fails:

- If `C2=FAIL`: in the claim table replace "**improved**" with "**not verified**", and append to the verdict cell
  "targets REPRODUCED ≥ 5 / BYTE_BACKED ≥ 32 not met; the failing token is the strategy sentence for round 58, not a
  retarget" (the claim's kill rule forbids changing target, threshold or recipe after the freeze). In LOG, end the C2
  bullet with the failing line and the count of unattempted URLs; drop the capabilities row.
- If `C3=FAIL`: same substitution; if `BOUND < 4`, the LOG bullet names which `R<k>` stayed unbound and their sweep
  lines, and the capabilities row is dropped. A `STRAY_IDS=` value that is not `-` goes verbatim into the row's
  verdict cell (it is the counter's own output, not a correction).
- Both PASS: nothing to change beyond the tokens.

## 5. What the L1 must confirm before these blocks are true (grounded gaps, not style)

1. **Commit order.** `c2-count.py` reads `corpus/captures/` from the working tree (`--root LANE`), while the spans
   manifests it pins come from git at `SET_REV`. At my snapshot 8 capture files were untracked (`tracked=97`, `raw=54
   txt=51`, `git status --porcelain`). The after-receipt's named lane master must therefore contain the very captures
   the counter consumed, or the receipt measures bytes the report does not commit — the C2 predicate's phrase is
   "committed lane bytes".
2. **The lesson must exist before the C2 receipt.** `c2-count.py:188` reads `corpus/lessons/round-57.md`; `c3-count.py`
   requires every manifest quote to occur in it (`IN_LESSON=n`). Neither file existed at snapshot (R9), and C3 needs
   `n>0`.
3. **C2's four pending URLs resolved themselves in the working tree** (R11/R12): S100/S103/S106 succeeded on attempt 2
   at 08:29–08:30Z; S105 has three `curl_rc=28` rows, two of them 1440 s apart, so UNREACHABLE is reachable for it. The
   counter decides; I did not.
4. **The 3 non-C2 ids** S131/S132/S133 in `refetch.tsv` are C3 candidates (two URL variants each, `412`/`404`), not part
   of the 47; the C2 SET comes from the base manifests, so their failures cannot move C2.

## 6. Findings (reported, not patched — both claims are frozen)

- **F1 — C3's anchor clause is vacuous when nothing new is bound.** `c3-count.py:263-264` builds `anchors_need` only
  from bound rows that are *not* in `base_ids`, and `:284` requires `anchors == len(anchors_need)`. With four bound
  rows that are all held (e.g. S118 plus three pre-existing rows), `ANCHOR_BOUND=0/0` satisfies the frozen
  "every `char N` of a new bound row's `anchor` cell (at least one)". The predicate's `(at least one)` is stronger than
  the code on that branch. The controls cannot show it (HELD/CITER both print `0/0` and fail on other clauses).
  Owner: `R57W1ReviewC3Same`.
- **F2 — `FLAGGED=g/g` hides the drift denominator.** `c2-count.py:238-242` prints `need_flag`/`flagged` only, so a run
  with `DRIFTED=1 FLAGGED=0/0` reads as clean; the JUNK control shows the same shape at `FLAGGED=0/47`. Anyone reading
  the receipt must take `need_flag` from the run, not from the ratio. This is why the draft's `[C2_FLAGS]` token asks
  for the flag lines verbatim.
- **F3 — the `SWEPT` denominator moves with BOUND.** `:277` prints `SWEPT={len(swept)}/{7-len(bound)}`, so the
  denominator is not `7` and a reader comparing rounds sees different totals; `claims.md` freezes it this way, so the
  draft quotes the line verbatim rather than normalising it.
- **F4 — D1 was still open at snapshot.** `corpus/knowledge/grey-literature-field-china-r42.md:9` still reads
  "the journal's 表 10 row"; no `#### Corrections (round 57)` block existed, though `.ufo/waves/round-57/w1/R57W1ScribeD1.md`
  already exists in the tree. Confirm the correction before the LOG's routed bullet claims it.

## 7. Writes, scratch, tooling

- Wrote exactly one file: this report. `git status --porcelain` before writing showed no path of mine (R13); the lane
  changes listed there are sibling seats'.
- No scratch directory was created: every script ran from stdin against the lane read-only (heredocs importing only
  stdlib), so nothing under `/fast/scratch/hyaku/chousa-r57/R57W1ScribeLogCard/` exists to delete. I made no
  `__pycache__` in `corpus/` or `tools/` (the pre-existing ones are older rounds').
- No tool installed or upgraded; no pacman transaction; no network fetch; no git/jj mutation; no counter executed.

VERDICT: drafted the LOG `## Round 57` block and the SCORECARD round-57 verdict (claim table, six axis rows, capability
row, `Planned — round 58`) against the frozen claims' own receipts and counters — the drafts hold as *parametric*
text with every unmeasured cell a declared token, and the attacks they hand to round 58 (F1–F4) are reported, not
patched.
