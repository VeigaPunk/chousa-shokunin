# R100RevenPrior — prior-round reconstruction (seat R100RevenPrior)

Seat: `R100RevenPrior`. Lane: `chousa`. Round 100, L1 `ChousaR100`.
Freeze attacked: `F = 6d4e8487ee6a16823c24a8e085c6559b92b9fec8` (shared clone at $S/repo, $S=/fast/scratch/hyaku/chousa-r100/R100RevenPrior).
Base: `929c784c63a1fd17961d21742101b2b109b7b8ff` (round-99 landing).
Battery re-run at F: exit 0, `NEG=7/7 MARK=11/11 BOUND=3/3 NORM=2/2 POS=4/4 REV=11/11 REVPOS=3/3 PROD=6/6 HARM_SAME=27/27 BASE_REV_ADMITTED=8/11 ORACLES_REJECTED=12/12`,
`CHALLENGE_CONTROLS_R100=PASS` (receipt R100RevenPrior-battery-f.txt). Base tool under battery `--no-oracles`: `REV=3/11 PROD=4/6`, FAIL exit 1 (R100RevenPrior-battery-base.txt).
Tooling: no installs (git 2.56.0, Python 3.14.8, GNU grep 3.12). Scratch under /fast/scratch/hyaku/chousa-r100/R100RevenPrior/; removed before yield.

Question: is each claim new, and why did round 99 miss F-1 (`.ufo/waves/round-99/w1/R99SentinelC1.md`)?

## (1) Lane GATE-RECORD rev-form inventory at BASE — F changes no verdict (HARM re-derived)

Command: `/usr/bin/grep -rn '^GATE-RECORD .* rev=' corpus/` (also `git grep` sweep of the whole tree for `GATE-RECORD[^ ]* rev=`).
At F the only `corpus/` files carrying `^GATE-RECORD .* rev=` are the seven lessons files below (10 records total; receipt R100RevenPrior-q1-revrecords.txt, plus R100RevenPrior-q1-revrecords-clean.txt with the same 10 lines). Every other `rev=` hit lives under `.ufo/waves/` (fixtures, forge matrices, receipts) — not under `corpus/` and therefore outside the battery's HARM set (`harm_files` = `corpus/knowledge/*.md` + `corpus/lessons/*.md` carrying a `GATE-RECORD` line; battery docstring+HARM code `corpus/evidence/round100/challenge-controls-r100.py:332-337`).

| file | records | path spellings |
|---|---|---|
| `corpus/lessons/round-80.md:19-22` | S199,S200,S201,S202 | `corpus/lessons/round-79-verifier-spotcheck.md`, `corpus/QUALITY.md` (x2), `.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt` |
| `corpus/lessons/round-88.md:17` | S218 | `corpus/QUALITY.md` |
| `corpus/lessons/round-89.md:19` (+:17 S216 url-form) | S218 | `corpus/QUALITY.md` |
| `corpus/lessons/round-91.md:14` / `round-92.md:19` / `round-93.md:22` / `round-94.md:15` | S001 (x4) | `tools/research-gate.sh` (x4) |

Path-spelling audit: **zero** of the 10 records spell `path=corpus/captures/…`; **zero** spell `.raw`, `./…`, `//`, or any copy-path. All paths are ordinary non-capture files (`corpus/QUALITY.md`, `corpus/lessons/…`, `tools/research-gate.sh`). Their 8 distinct revs all exist as commits in the lane and each rev's tree holds 129–183 `corpus/captures/<24 hex>` entries, but the records never point at them.

Verdict comparison (receipts R100RevenPrior-q1-full-f.txt vs R100RevenPrior-q1-full-base.txt; also per-file R100RevenPrior-q1-verdicts-*.txt):

- F tool `python3 -B tools/gate-records.py verify --root . <those 7 files>`: `GATE_RECORDS files=7 records=11 ok=11 fail=0`, exit 0.
- Base tool `git show 929c784c:tools/gate-records.py` same command: identical stdout, exit 0. `diff` = IDENTICAL.
- Including `round-89.md:17` (url-form S216), the 7-file run is 11 records (10 rev + 1 url), all OK under both tools.

So HARM's `27/27` is not a re-derivation accident: no corpus rev record is even *eligible* for the new identity gate (its blob is not a capture of its rev), so changing the gate cannot move any verdict. Independently re-derived: **HARM holds, and the reason is structural (no capture-path rev records exist in the lane), not that the new gate is a no-op**.

Novelty consequence: C1's fix is exercised exclusively by battery fixtures (`REV=11/11`, `REVPOS=3/3`, `PROD=6/6` on the candidate; base tool admits 8/11 REV refusals and 2/6 PROD — `BASE_REV_ADMITTED=8/11`). No live lane record needed the repair; the defect class (round-98's `corpus/lessons/round-98.md:63` / `corpus/QUALITY.md:1432` pattern, re-openable via spelling at round-99 F) is closed prospectively, not by flipping an existing admitted record.

## (2) BASE instruments: nothing else checked rev records by identity or path normalization

Ticket command re-run at BASE: `git -C $S/repo grep -n -e 'ls-tree' -e normpath 929c784c63a1fd17961d21742101b2b109b7b8ff -- tools corpus/evidence` → 31 lines (receipt R100RevenPrior-q2-grep.txt, exit 0). Classified:

- `tools/search-rerun.py:276` (`git ls-tree -r -z --full-tree` at a search record's `rev`) — re-runs search expressions at their recorded rev; it never reads GATE-RECORDs, never inspects captures, never normalizes a `path=` spelling. It is a tree enumerator, not an identity check.
- `tools/digest-in-tree.py:79` (`git ls-tree -r -z`) — digest baseline over blobs; no GATE-RECORD / capture-identity logic.
- `tools/capture-text.py:120` (`posixpath.normpath` on an OOXML relationship `Target`) — ZIP-member containment; unrelated to rev records and to `CAP_RE`.
- `corpus/evidence/**` hits: counting/seeding helpers (`round40/c2-count.py`, `round49/c1-count.py`, `round62/digest-prefix-check.py`, `round78/selfcheck.py`, `round79/selfcheck-v2.py`, `round80/gate-grounding-check.py:89,156` — the last enumerates `corpus/lessons` at revs to ground gate records, but does not judge any GATE-RECORD), `build-spans.py` OOXML normpath (rounds 52–54, 56), size-map forger (`round76/forgers/forge-size-map.py:24` — `git ls-tree -l` sizes for a forgery demo), and `round99/entry-controls-r99.py:130` (knowledge-entry absence check). **None** compares a rev record's blob object id against a capture set, and **none** normalizes a rev `path=` spelling before a regex test.

`tools/gate-records.py` at BASE is the sole rev-record judge, and its only relevant logic is `CAP_RE.fullmatch(kv["path"])` at line 307 — exact-string match, while `git_blob` at line 217 resolves `rev:path` semantically. That asymmetry is the whole of F-1. Search-rerun's `ls-tree` use (files-at-rev for re-execution) does not create a second identity checker; it also proves by contrast that the lane already had the `ls-tree`/`rev-parse` machinery to express identity — it was just never applied to GATE-RECORD rev paths.

## (3) Round-99 mutant rebuild at F's tool: 27/28 now killed, 1 survives

Method: rebuilt all 28 one-site mutants of `R99MutantsC1.md`'s table against F's tool (not the round-99 tool — the code moved: F's rev branch is `ctext = rev_capture_text(...); if ctext is not None and is_challenge(ctext)`). Adaptations, each applied once (receipts: mutants under $S/mutants/, per-mutant battery outputs under $S/mwork/, summary R100RevenPrior-mutant-summary.txt; detector = run-100 battery `--tool <mutant> --no-oracles`, KILLED = `CHALLENGE_CONTROLS_R100=FAIL` exit 1):

- Marker drops m01–m11: literal marker-line deletion (F's `CHALLENGE_MARKERS` tuple identical to round 99's). Verbatim.
- m12 `<=`→`<`, m13 200→199, m14 200→201, m15 200→1000: on `CHALLENGE_MAX_WORDS` / length line. Verbatim.
- m16 drop `norm(` inside `is_challenge`: `t = norm(text).lower()` → `t = text.lower()`.
- m17 drop `.lower()`, m18 `any`→`all`, m19 `and`→`or`, m25 none, m26 `.lower()`→`.casefold()`, m27 first-marker, m28 `[:5]`, m29 `<=`→`>=`: on `is_challenge`'s return, verbatim.
- m20/m23 (admit-branch): F's admit branch is `if is_challenge(text): codes.append("CHALLENGE")` after the QUOTE_ABSENT check — same shape as round 99, so m20 deletes the admit call and m23 gates it on `_qa` verbatim.
- m21/m24 (rev-branch): remapped to F's `if ctext is not None and is_challenge(ctext)` — m21 deletes it; m24 gates it on the LINE-bad predicate recomputed inline.
- m22 (`CAP_RE.fullmatch(...) and` → `True and` in rev branch): F has no `CAP_RE` in the rev branch; the equivalent one-site mutant is `name = capture_oids(...).get(...) if ... else path` (every rev blob judged) — i.e. the gate the round-100 battery's oracle o4 (`every-rev`) encodes. This is the correct port: m22's *intent* (remove the capture gate on the rev path) is preserved; its *syntax* is new. Recorded explicitly so the rebuild is auditable.

Result (28 mutants):

| # | mutant | verdict at F tool under R100 battery | tally |
|---|---|---|---|
| m01 | drop cookies | **KILLED** (was KILLED) | NEG=6/7 MARK=10/11 PROD=5/6 |
| m02 | drop checking | **KILLED** (was SURVIVED) | MARK=10/11 REV=9/11 |
| m03 | drop recaptcha | **KILLED** (was SURVIVED) | MARK=10/11 |
| m04 | drop client-challenge | **KILLED** (was SURVIVED) | MARK=10/11 |
| m05 | drop a-required-part | **KILLED** (was SURVIVED) | MARK=10/11 NORM=1/2 |
| m06 | drop just-a-moment | **KILLED** (was SURVIVED) | MARK=10/11 NORM=1/2 REV=10/11 |
| m07 | drop verify | **KILLED** (was KILLED) | NEG=6/7 MARK=10/11 BOUND=1/3 |
| m08 | drop enable-js | **KILLED** (was SURVIVED) | MARK=10/11 |
| m09 | drop attention | **KILLED** (was KILLED) | NEG=6/7 MARK=10/11 |
| m10 | drop ddos | **KILLED** (was SURVIVED) | MARK=10/11 |
| m11 | drop are-you-a-robot | **KILLED** (was SURVIVED) | MARK=10/11 |
| m12 | `<=`→`<` | **KILLED** (was SURVIVED) | BOUND=2/3 |
| m13 | max 199 | **KILLED** (was SURVIVED) | BOUND=2/3 |
| m14 | max 201 | **KILLED** (was SURVIVED) | BOUND=2/3 |
| m15 | max 1000 | **KILLED** (was KILLED) | BOUND=2/3 POS=3/4 |
| m16 | no norm | **KILLED** (was SURVIVED) | REV=10/11 |
| m17 | no lower | **KILLED** (was KILLED) | NEG=0/7 NORM=0/2 REV=2/11 |
| m18 | any→all | **KILLED** (was KILLED; stricter tally, MARK=0/11 now that MARK leg exists) | NEG=0/7 |
| m19 | and→or | **KILLED** (was KILLED) | BOUND=2/3 POS=2/4 HARM=25/27 |
| m20 | no admit call | **KILLED** (was KILLED) | NEG=0/7 MARK=0/11 |
| m21 | no rev call | **KILLED** (was KILLED) | REV=0/11 PROD=2/6 |
| m22 (ported) | every-rev-blob | **KILLED** (was SURVIVED) | REVPOS=2/3 HARM=20/27 |
| m23 | challenge-only-when-quote-absent | **KILLED** (was KILLED) | NEG=0/7 MARK=0/11 |
| m24 | rev-only-when-line-bad | **KILLED** (was KILLED) | REV=0/11 PROD=2/6 |
| **m26** | **lower→casefold** | **SURVIVED** (was SURVIVED) | exit 0, full PASS (all legs incl. HARM 27/27) — **sole survivor** |
| m27 | first-marker-only | **KILLED** (was KILLED) | NEG=1/7 MARK=1/11 NORM=0/2 REV=0/11 |
| m28 | slice [:5] | **KILLED** (was KILLED) | NEG=4/7 MARK=5/11 NORM=1/2 |
| m29 | `<=`→`>=` | **KILLED** (was KILLED) | NEG=0/7 POS=3/4 REV=0/11 |

**27/28 killed; 1/28 survives (m26).** The 12 round-99 survivors other than m26 are all killed by new legs with a clear division of labour: MARK (m02–m11 marker drops), BOUND (m12–m14 thresholds), NORM (m05/m06/m16 norm), REV (m02/m06), REVPOS+HARM (m22). The coverage shortfall `R99MutantsC1` flagged in §"What does this do to the C1 sentence" is closed: every marker now does isolated work, and the 199/200/201 boundary is tested.

On the survivor, two corrections to the round-99 file, both verified by probe [INFERENCE check, receipt R100RevenPrior-q1-revrecords.txt is not this — probe run inline in scratch, code in §"m26" below]:

1. R99's probe string `"jußt a moment"` does **not** demonstrate the divergence: `"jußt a moment".casefold() == "jusst a moment"`, which contains none of the 11 markers (no marker contains `ss`; the `ß`→`ss` expansion cannot create any of them). The mutant is genuinely non-equivalent, but via the **long s** `ſ`→`s`: `"cookies muſt be enabled".casefold()` contains `"cookies must be enabled"` while `.lower()` does not. So m26 remains UNCOVERED/non-equivalent, but R99's stated evidence for it is wrong and should not be quoted.
2. F's sentence says "lower-cased", so a casefold tool does not falsify C1's sentence; this is a battery-coverage note only. The correct disposition (same as round 99): m26 is a *known* uncovered non-equivalent mutant; the battery's legs are all ASCII. Closing it needs a non-ASCII MARK leg (e.g. a capture with `muſt`), not a tool change.

Note on equivalence class: m26 is the *only* member of round-99's 13 survivors that still survives — and it survived round 99 for the wrong stated reason. The other 12 are killed for the right reasons. The battery mutants b1–b8 (loosened-battery class) were not rebuilt: they mutate the battery, not the tool, and round 100's battery is a different artifact (the o1–o12 oracle set now subsumes their loosening class).

## (4) Freshness: 26 on-release entries, 1 ever answered — and no other rate is known-stale

Counts (F tree; receipts R100RevenPrior-q4-recheck.txt, R100RevenPrior-q4-onrelease-files.txt, R100RevenPrior-q4-base-onrelease.txt, R100RevenPrior-q4-update-excerpt.txt):

- **26 files** under `corpus/knowledge/` hold `recheck: on-release` at F (25 at BASE — the +1 is the new `quotation-error-update-r100.md` itself). 103 knowledge entries total.
- **`## Update` answer flags:** exactly **1** — `corpus/knowledge/quotation-error-rates-r99.md:117` (receipt R100RevenPrior-q4-update-excerpt.txt). C2's entry is the first on-release recheck in lane history to be answered. No other entry has ever been answered, including the PRESS entries (`press-2015-statement-questions-r98.md`, `press-checklist-questions-r97.md`, both `recheck: on-release`, no `## Update`) and the r35–r38 tooling entries, which have sat unanswered since 2026-10-19.
- **Rates held by entries with `on-release`:** of the 26, only the quotation-error lineage (r99 + r100) and `keyed-engine-output-equivalence-r35` (`65%` — a lane-measured rate, not literature) carry `%` rates. The PRESS entries carry no updated-literature rate (S231 is the guideline statement's own abstract, read in round 98; nothing newer is named as its trigger). So at F there is **no other known-stale literature rate awaiting a flag**: the only rate-bearing entry whose trigger has fired is r99, and it is now flagged. (Several `%`-carrying entries use time-based rechecks — `citation-chain-fidelity-r24` 90d, `claim-support-test-r37` 365d, `evidence-pool-versioning-r39` 365d, `evidence-snapshot-coverage-r40` 365d, `grey-literature-field-china-r42` 180d — out of scope for the on-release question; their dates have not been re-derived here.)

Why the r99 trigger fired only now (from the entries themselves): r99's `recheck: on-release` names "a newer synthesis by the same authors". Round 99 could not read it — the publisher view answered with a Client Challenge page (S234) and the Europe PMC record "was reached only by a wave seat, not by a lane GET" (r100 entry §"What this entry governs"). Round 100's lane GET of the Europe PMC core record answered 200 (S238), so the trigger fired. The freshness mechanism worked here because the trigger was *named* (same authors, named pmid) and the blocker (challenge page on the publisher route) was distinct from the firing condition (the index record). For the other 25 unanswered entries the triggers are vaguer ("on-release" of a tool version, a man-pages release, a guideline issuance) and no one has checked whether their releases have happened.

Proposed next-round rule (for the L1 to adopt or reject): convert each of the 26 `recheck: on-release` lines into a *named trigger with a checkable firing condition* (the r99 pattern: `<newer synthesis by X, pmid/doi>` — not "on-release" bare), and add a fresh sweep: at each round, grep `recheck: on-release` and for each hit either fire it, or re-confirm it with one dated line. One round of that sweep would answer the 25 outstanding entries' worthiness; today only 1/26 (3.8%) has been answered and the lane cannot tell whether the other 25 triggers have fired. Minimal enforceable form: the knowledge-entry metadata check (`tools/research-gate.sh verify-metadata`) gains "a bare `on-release` with no trigger noun is INCOMPLETE" — this is a claim about the *next* round's gate, not about C2, which correctly names its trigger.

## Why round 99 missed F-1 (sentinel's question)

Three compounding causes, all evidenced:

1. **The repair was specified as a string form.** Round-99 F's tool gated the rev check on `CAP_RE.fullmatch(kv["path"])` (`corpus/captures/<24 hex>.txt`) while `git_blob` fetched via `git cat-file blob <rev>:<path>`, and git resolves `./`, `//`, `.//`, etc. to the same blob. The sentence's wording ("a rev record whose path is `corpus/captures/<24 hex>.txt`") licensed exactly that reading; the instrument faithfully enforced the *string*, not the *blob*. (Confirmed at BASE line 307; F's diff replaces the string gate with `rev_capture_text` object-id identity — `capture_oids` via `git ls-tree` — which is why F's version is immune.)
2. **The battery only ever exercised the canonical spelling.** Round-99's PROD rev leg built its path by string concatenation only: `path = f"corpus/captures/{CAP[sid][1]}.txt"` (`corpus/evidence/round99/challenge-controls-r99.py:180`), and its NEG/PROD counts could reach 4/4 while the rev leg was open under any other spelling. Sentinel's own words (their receipt): "it establishes only that one spelling is closed" — PROD 4/4 did not mean "the rev form is closed". The round-100 battery fixes exactly this: 11 REV refusals across 5 spellings + `.raw` + byte copies at foreign paths, 3 REVPOS, 6 PROD.
3. **Named limits did not cover the spelling.** Round-99 limit (d) exempted "a rev record whose path is not under `corpus/captures/`" — but `./corpus/captures/…` *is* (git puts it there), so the exemption did not license the admission, yet the claim's wording invited the string reading. The mismatch between limit (d)'s intent (semantic) and sentence's form (syntactic) is where the defect hid. Round 100 closes it by making identity the gate and stating the sentence in identity terms ("has the object id of a `corpus/captures/<24 hex>.txt` or `.raw` entry of that rev's tree").

Net novelty assessment: C1 is new in two senses — (a) the tool change (identity gate added at F, absent at both BASE and round-99 F), and (b) the battery change (spelling matrix + HARM over knowledge+lessons + 12 oracles vs round-99's 4 CANONICAL PROD + 5 oracles). It is not new in the defect it repairs (round-98's lesson was already recorded); round 100 converts a known defect into an enforced gate. C2 is new (first on-release answer; S238 opened this round; tier-B abstract-only synthesis with 14 located quotes + 8 decision rows).

## Verdicts

VERDICT: R100RevenPrior C1 held — F's identity gate is new (absent at BASE and R99's F), HARM 27/27 re-derives with zero corpus capture-path rev records, and the battery kills 27/28 round-99 tool mutants (m26 casefold, probe corrected to long-s, sole survivor).
VERDICT: R100RevenPrior C2 held — first on-release recheck ever answered (1/26 at F, r99 flagged with ## Update naming S238 and the new entry), no other rate-bearing on-release entry is known-stale.
VERDICT: R100RevenPrior n/a — no other claim touched; no production files written.
