# R96CriticClaims — falsification of C1 and C2 at freeze 2db151c5 (lane chousa round 96)

Attacked tree: `git clone -q --shared` of `/home/vgpnk/Projects/shokunin/chousa-shokunin`, `git checkout 2db151c5ea0883de0b9dc8d95c6fac1755e1056a`.
Base `bbf64970b6c73ca64bcc5f6de2f33b0550459813`. Seat scratch `/fast/scratch/hyaku/chousa-r96/R96CriticClaims/` (deleted at yield).
No tool installs (pacman paused; `grep` semantics via `/usr/bin/grep`). No network. No production edits; scratch repo status verified clean after each swap.
Every `Report:` trailer path is relative to `/home/vgpnk/Projects/shokunin/chousa-shokunin` — this file is `.ufo/waves/round-96/w1/R96CriticClaims.md`.
Receipts cited are also copied as `R96CriticClaims-*.txt` in the same `w1/` dir (see §Receipts index).

**Counterexamples:** (1) a shim whose `verify` computes `evaluate(...)` then discards it and always returns CLEAN; (2) a source-blind cheat that never calls `parse_text`/`matches`/`evaluate` but detects each of the 23 mutants by embedded (base64) mutant strings; (3) a dirty selftest that writes outside the NO_WRITE directory and opens a socket; (4) a fluent negated-misreading entry whose every Do cell still passes WARRANT_TERMS; (5) a Located-quotes table with a wrong `S` source column that passes both `gate-records` and `bindings()`. None needs network, sudo, or host mutation; each is a few lines on top of the frozen files.

## §Godspeed axes (used, not admired)

1. **Clausal enforcement** — for each substantive clause of each claim sentence, name the instrument + line that enforces it, or mark it `unenforced`.
2. **Surrogate discrimination** — does the battery reject a surrogate that achieves its tallies without the claimed capability? (Shim, cheat, dirty, oracle.)
3. **Temporal/counterfactual honesty** — `opened this round`, `real searches`, `re-run at base`: is the filed evidence what the wording asserts?
4. **Claim–instrument gap** — where sentence words exceed K1–K5 / named-limit honesty. Propose the smallest narrowing that makes the sentence true without weakening the instrument.

All four axes were iterated cheap-first, in parallel batches where independent: positives and predicates first (§Holds), then surrogates (§Aa–§Db), then quote/decision forensic (§Ec–§Ef).

## §Holds (verified, with exact commands)

### H1. C1 positives and counts — HELD
- `python3 -B tools/search-rerun.py --selftest` → exit 0, last line `SEARCH_RERUN_SELFTEST: PASS cases=32/32`.
  Case split measured from output: `p01`–`p14` = 14 parse, `m01`–`m08` = 8 matching, `j01`–`j10` = 10 judgement; 14+8+10=32.
- `python3 -B corpus/evidence/round96/selftest-controls-r96.py --root . --work <scratch> --no-regression` → `POSITIVE=1/1 DO_NOTHING_REFUSED=1/1 MUTANTS_KILLED=23/23 ORACLES_REJECTED=3/3 NO_WRITE=1/1 CASES=32 / SELFTEST_CONTROLS=PASS` (exit 0). Full battery with regression was not re-run end-to-end (claimed ~10 min); its two regression legs were exercised separately (see §Aa2).
- Base: `git show BASE:tools/search-rerun.py` + `--selftest` → exit 2, no PASS line (matches `before/c1-base.txt`).
- `m34`-equivalence (named limit e): `"/x".startswith("/")` is true and `"" in "/x".split("/")` is also true, so the stranded absolute-glob check is refused twice; removal is sound.
- Docstring overcount (not a claim falsehood): `tools/search-rerun.py:48` says “14 parse cases (13 setup refusals …)”. Measured: only 12 carry `want=` (p02–p13); `p01-parse-good` and `p14-escaped-pipe` are positives. So the tool comment overcounts refusals by 1. The C1 claim sentence and `claims.json` assert only “14 parse cases”, which is true. **Narrow:** «14 parse cases (12 refusals, 2 positives)».

### H2. C2 predicates 1–4 — HELD as tallies
- `python3 -B tools/gate-records.py verify --root . corpus/knowledge/search-peer-review-dedup-r96.md` → `GATE_RECORDS files=1 records=31 ok=31 fail=0` (exit 0).
- `bash tools/research-gate.sh verify-metadata … --root .` → `METADATA_COMPLETE=1/1 / RESEARCH_GATE: CLEAN` (exit 0).
- `python3 -B tools/search-rerun.py verify … --root .` → `SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8 … / SEARCH_RERUN: CLEAN` (exit 0).
- `python3 -B corpus/evidence/round96/entry-controls-r96.py --root . --work <scratch>` → `POSITIVE=1/1 FORGERY_REFUSED=8/8 BINDING_REFUSED=3/3 SEARCHES=3/3 DO_NOTHING_REFUSED=1/1 ORACLE_REJECTED=1/1 / ENTRY_CONTROLS=PASS` (exit 0).
- GNU grep agreement at base (independent re-run, `git archive bbf64970 corpus/captures`): Q1=2, Q2=2, Q3=3, Q4=4 with digest `sha256:075e…` equal to the record, Q5=1, Q6=0, Q7=3, Q8=0. So the 8 recorded counts agree with both GNU grep and the Python re-run. The per-Q digest and hit-set equality are real measurements, not just tallies.

### H3. S224 “re-opened this round” / S223 freshness — HELD as wording, tradeoff noted
- `refetch.tsv` holds distinct fetch rows: S222 `2026-11-08T22:51:39Z` (http 200, raw `0703…`, txt `86f1…`) vs S224 `2026-11-09T00:43:50Z` (http 200, same raw/txt digests); S223 has both an http 200 abstract fetch `2026-11-09T00:35:55Z` and the http 403 CADTH reject `2026-11-09T00:35:47Z`. So “opened this round” is a new timestamp, not a date rewrite; “identical bytes” is disclosed in `SOURCES.md` S224 anchor, in the entry head (`verified-at`), and in plan P3. S224 adds scope, not bytes — an honest tradeoff, not a falsehood. S222’s scope excludes items 14/16; S224 is therefore necessary to hold them without violating CORPUS rule 2.

### H4. Separability — HELD
- `git show bbf64970:tools/search-rerun.py > base-tool.py; python3 -B base-tool.py verify corpus/knowledge/search-peer-review-dedup-r96.md --root .` → `rev_match=8/8 … CLEAN` (exit 0), reproducing `before/c2-separable-base-tool.txt`. C2 needs no C1 code; C1’s selftest touches no entry. The two claims are separable as worded.

## §Aa. C1: “scored by the same `evaluate` function `verify` runs” — unenforced directly; enforced only by the slow leg

**Clause map (C1 sentence):** `evaluate`-sameness → no instrument in predicate 1; `23 mutants exit 1` → `selftest-controls-r96.py` MUTANTS leg (each `src.count(old)==1` + `--selftest` must print `FAIL`); `three stand-ins fail` → ORACLES leg (default mode only); `empty cwd/HOME + lane unchanged` → NO_WRITE leg; `round-95 battery + mutant rebuild still pass` → REGRESSION leg (full battery only); `SKILL.md registers as gate naming self-test` → predicate-3 grep in part (see §Ac).

**Instrument lines:** `evaluate` is defined once (`tools/search-rerun.py:353`); `verify` calls it at `:399`; selftest calls it at `:490` and `:511`. The battery NEVER asserts that the `verify` call site (or the verdict it prints) is the function the selftest uses — it cannot, without textual or dynamic linkage, since Python has no identity check across call sites. Two incidental tripwires exist: (a) each mutant `old` must apply exactly once, which DOES catch a full duplicate-`evaluate` fork (the duplication makes `old` appear twice → `SETUP applies … FAIL`); but it does NOT catch a verdict-discard; (b) REGRESSION (full battery) runs the r95 CLI battery against `verify`, which DOES judge verdict semantics — but that leg takes ~10 min and is skipped under `--no-regression`.

**Counterexample (shim) — command:** built `shim.py` = frozen tool with one inserted line after `:399`:
`findings, rev_ok, tree_same = 0, len(rows), len(rows)  # SHIM: discard real verdict` (everything else byte-identical).
- `python3 -B shim.py --selftest` → `PASS cases=32/32` (exit 0).
- Forged record (Q2 `2→3`): `python3 -B shim.py verify forged-Q2.md --root .` → `rev_match=8/8 findings=0 / CLEAN` (exit 0); real tool → `rev_match=7/8 findings=1 / DRIFT` incl. `Q2 COUNT_DRIFT` (exit 1). The shim’s verdict is false on a real forgery.
- `selftest-controls-r96.py --tool shim.py --no-regression` → `POSITIVE=1/1 MUTANTS_KILLED=23/23 NO_WRITE=1/1 SELFTEST_CONTROLS=PASS` (exit 0). The mutant strings still apply once; mutants are still “killed” via the selftest’s `evaluate` copy, which the shim never removed.
- Only the slowed REGRESSION legs catch it: `rerun-controls-r95.py --tool shim.py` → `STRICT_TREE=0/1 FORGERY_REFUSED=0/10 / RERUN_CONTROLS=FAIL` (exit 1). (Shim verdicts make every forgery return CLEAN.)

**Verdict on clause:** as a bare sentence about `--selftest` (predicate 1) it is **unenforced** — the selftest cannot prove it shares code with `verify`. As bundled into predicate 2 **with REGRESSION_R95=2/2** it is indirectly enforced, but only by the slowest leg and only for verdict-level divergence of the tested fixtures. The claim’s present-tense “scored by the same … function `verify` runs” overstates what predicate 1 proves.

**Narrowed wording (smallest safe correction):** «10 judgement cases scored by `evaluate`, the function `verify` also calls (`tools/search-rerun.py:399` and `:490` — checked by reading, not by the selftest); sameness of verdict semantics is exercised by the battery’s REGRESSION leg, not by `--selftest` itself.» If the visual line must stay short, the instrument fix is one dynamic check — e.g., selftest `judge()` and `verify()` both go through the importable `evaluate` symbol and a battery leg asserts `verify`'s call is that symbol — but as frozen, the prose must say so.

## §Ab. C1: source-blind cheat passes the battery — “can fail” proves less than implied

**Counterexample (cheat):** `cheat.py` = frozen tool with `selftest()` replaced by: read own `__file__`, base64-decode 23 embedded `NEW` strings and 23 embedded `OLD` strings, FAIL iff a `NEW` is present in the file or an `OLD` is absent. It never calls `parse_text`, `matches`, `hit`, or `evaluate`; it returns 32 synthetic `SELFTEST cNN` lines. It retains one dead anchor line (`good = ST_HEAD + st_row()`) only so the battery’s hollow-oracle anchor applies.
- `python3 -B cheat.py --selftest` → `PASS cases=32/32` (exit 0).
- `selftest-controls-r96.py --tool cheat.py --no-regression` → `MUTANTS_KILLED=23/23 … SELFTEST_CONTROLS=PASS` (exit 0). Each mutant file contains its `NEW` (inserted by the battery) → cheat FAILs. No behavioural test runs.
- As the committed tool in default mode: `… --no-regression` → `POSITIVE=1/1 MUTANTS_KILLED=23/23 ORACLES_REJECTED=3/3 SELFTEST_CONTROLS=PASS` (exit 0). The three named oracles are still rejected because they are built from the cheat’s source (mutants of a blind tool are killed by the cheat’s textual detector; the constant stub still fails MUTANTS; hollow still prints PASS before testing; always-fail still fails POSITIVE).
- **Novel-defect blindness:** `cheat-novel` = cheat + `if head != HEADER:` → `if False:` (accepts any header). `python3 -B cheat-novel.py --selftest` → `PASS cases=32/32` (exit 0), while the same defect on the real tool → `FAIL cases=31/32 failed=p03-header`. The battery’s mutant leg cannot see novel defects by design (named limit b admits this), but the cheat proves the stronger point: the battery accepts a tool with NO behavioural cases at all.

**Verdict on clause:** the claim sentence (“Each of the 23 … makes it exit 1”) is true of the frozen file, but the battery’s power is **tautological for the 23 named sites**: it verifies the selftest has tripwires at those coordinates, not that it scores behaviour anywhere else. Named limit (d) already admits expectations live in the tool (“an edit that changes code and expectation together passes”), but the cheat shows the admission is wider: a tool that does not execute the claimed behaviour at all still masses 23/23. The sentence should add that the battery’s mutant leg certifies failure AT the named sites, not behavioural coverage in general.

**Narrowed wording:** append after the mutant clause: «the 23 sites are the lane’s; a self-test that merely text-matches those sites would also mass 23/23 (checked), so the mutant leg proves tripwire placement, not general defect-finding.»

## §Ac. C1: “registers the tool as a gate” vs predicate-3 grep — kind unenforced

**Command:** `/usr/bin/grep -c '^| `search-rerun` (r96 re-registration' SKILL.md` → `1` (exit 0). In `claims.json` the predicate is only `skill_gate_rows: 1`; in `claims.md` prose it adds “and that row's kind cell is `gate`”.

**Counterexample:** copied SKILL.md, changed the r96 row’s kind cell `gate→tool` (`| gate |` → `| tool |` on line 180 only). The same grep still returns `1`. No instrument reads the kind cell. The row in fact has `kind=gate` (8 cells: name, `gate`, verify command, exit table, selftest expectation, evidence, write-scope `none (as the r95 row…)`, owner `chousa`), and the row text names the selftest — so the claim is true of the bytes, but predicate 3 as a counting command cannot verify the most important word in it (`gate`).

**Narrowed wording / instrument fix:** either extend predicate 3 to a kind-checking grep (e.g. `grep -c '^| `search-rerun` (r96 re-registration[^|]*| gate |'`) or narrow the sentence to «SKILL.md carries one row headed `search-rerun (r96 re-registration…)` whose kind cell reads `gate` (read by eye, unenforced)».

## §Ad. C1: “leaves an empty cwd/HOME directory empty and the lane status unchanged” vs K4 “writes a file, runs git or opens a socket”

The claim sentence itself stays inside NO_WRITE’s scope and is accurate; the **kill rule K4 and the tool docstring** (“It reads no file, runs no git and opens no socket … No writes”) exceed it.

**Counterexample (dirty):** `dirty.py` = frozen tool + inside `selftest()`: `open("/fast/…/dirty-write.txt","w").write("dirty")` and `socket.socket().connect_ex(("127.0.0.1",1))`.
- `selftest-controls-r96.py --tool dirty.py --no-regression` → `NO_WRITE=1/1 … SELFTEST_CONTROLS=PASS` (exit 0); `dirty-write.txt` present (`dirty`). NO_WRITE lists only the empty dir and compares `git status --porcelain`; it cannot see writes elsewhere, reads, git spawns, or sockets. Named limit (c) admits “not system calls”.

**Verdict:** K4 is **unenforceable as written** — a selftest that writes a file, runs git, or opens a socket passes K4’s instrument. “In-memory” in the tool/skill (`SKILL.md:180` “in memory, no file, git or network”) inherits the same gap.

**Smallest safe correction (pick one, do not relax K4 silently):** (a) narrow K4 and the tool/skill sentences to the measured scope («writes nothing into cwd/HOME and leaves `git status --porcelain` unchanged; not a syscall claim»), or (b) add a syscall-level leg (e.g., audit-hook run that refuses `open`/`socket`/spawn during `--selftest`). Do not keep the current split where the sentence is narrow but K4/docstring are broad.

## §Ae. C1: DO_NOTHING — could it pass for the wrong reason?

`DO_NOTHING` runs the BASE tool (`git show BASE:tools/search-rerun.py`) with `--selftest` and requires exit 2 + no PASS line. The base exits 2 because the subcommand is required. The check does NOT prove “no self-test” in general — any base that exits 2 for another reason (usage error, top-level refusal) and omits the PASS line passes DO_NOTHING. Conversely, a base that had a selftest but selftest returned 2 spuriously would also pass (and only POSITIVE on the new tool would catch the pair). In this round the antecedent is fixed (base known to lack `--selftest`) and the `before/` receipt pins the exact argparse error, so the leg is sound as a before-check; as a general “no self-test” detector it is weak. **Narrowed:** «the base tool exits 2 without a PASS line (its argparse usage error; `before/c1-base.txt`)» rather than using DO_NOTHING alone as proof of absence. Same shape in C2 DO_NOTHING (absent path → `gate-records` exit 2; any unreadable path would also exit 2, but the battery also checks `git cat-file -e BASE:entry` is absent, which pins it).

## §Db. C2: “warranted” vs WARRANT_TERMS’ lexical floor — negotiation in the entry’s own terms, proven in the entry’s own numbers

C2 named limit (a) already concedes the instruments “check that a warrant exists and shares a content word, not that the paraphrase is faithful — that is the wave's reviewer item”, and the battery docstring calls it “a lexical floor, not entailment: a nonsense Do or a wrong qid fails it, a fluent misreading can pass it”. That concession is documented and is why §H2 tallies hold. The falsification therefore goes to the claim sentence’s word «warranted», measured in WARRANT_TERMS’ own vocabulary:

- `entry-controls-r96.py` `WARRANT_TERMS` keeps a Do iff its content words (lowercase ≥5 letters, minus 17 STOP words) intersect its warrant quotes’. `words()` never sees negation, Deletes the Do’s direction, or reads the Never cell at all.
- **Negation counterexample (all 8 rows):** prepending `not ` to every Do leaves sharing unchanged — `negated-passes=True` for 8/8 (measured; `R96CriticClaims-warrant-negation.txt`). Example Row 2 Do «strongly consider having the search strategy peer reviewed by an experienced searcher…» → “not strongly consider … inexperienced …” still shares `[consider, searcher, specialist, librarian]`. Example Row 8 Do «report the total number of references after deduplication in the flow diagram» → “suppress the total number …” still shares `[total, number, references, deduplication, diagram]`.
- The BINDING leg’s `b1-nonsense-do` (“DELETE EVERYTHING…”) proves only that content-free nonsense fails; it does not touch fluent reversal, which is the natural failure mode for a depth claim.

**Verdict:** «warranted» (C2 sentence) asserts entailment-by-located-quotes; the instrument enforces **lexical overlap**. The named limit already says so, but the sentence does not carry the qualifier. **Narrowed:** «whose 8 decision rows each cite at least one located quote and whose Do cells each share a content word with those quotes (lexical floor; paraphrase fidelity is the reviewer item per named limit a)». If «warranted» is kept, the instrument must gain a reviewer-facing check (a human or model entailment audit of the 8 rows) — not more string matching.

## §Dc. C2: “real searches” vs what the record proves

The entry’s `## Searches` files 8 real expressions at base with recorded counts/sets; `verify` re-runs them at `rev=bbf64970` with Python `re` (under the `\|` → `|` rule). What is **measured**: Python-re counts equal recorded counts (and Q4’s digest matches `sha256:075e…`) and Q1–Q8 hit-sets match the grep re-run above. What is **asserted but not filed**: that GNU grep (rather than the Python tool) produced the recordings, and that no other expression produced the same counts. No grep transcript is committed; the `## As run` block is prose. The gap matters because the agreement claim is per-expression: `verify` equality would also hold if the author had generated counts with `search-rerun.py` itself and labelled them “GNU grep”. The r95 battery’s `grep-agree` leg measures grep-vs-tool agreement on ITS fixture, not on these 8 Q-rows; for this entry the equality in §H2 closes the loop on counts but not on provenance. **Narrowed:** «8 searches filed with counts later reproduced both by GNU grep at base (reviewer re-run, no transcript filed) and by `verify`» — or file the 8-line grep transcript so “run with GNU grep” is itself an instrument.

## §Dd. C2: S224 — “opened this round” is honest; the depth delta is re-scoping

No falsehood (see §H3). For the record: items 14/16 and Box 1 text were byte-present in S222’s capture since r95 (L-lines sit at `1a8c36c…:307–1059`). S224’s contribution is a second registry row + scope + 18 Located-quotes selections, with identical raw (`0703…`) and text (`86f1…`) digests and a later `fetched` timestamp. That is the CORPUS-rule-2-correct way to hold second scope without rewriting S222 (plan P3). It is also why C1/C2 are separable only in code, not in evidence: C2’s S224 fetch exists in the same freeze commit as C1 (`git show --stat HEAD` lists both). The claim says “rested on S223 and S224, both opened this round” — true. The depth claim should not be read as “new bytes for PRISMA-S”; the new bytes this round are S223 only (abstract, tier B, via the http-403-noted CADTH reject). No wording change required beyond making that distinction visible at the claim level:
**Narrowed:** «C2 rests on new bytes S223 (tier B abstract) and re-scoping S224 (same PDF bytes as S222, second scope)».

## §Ec. C2: “Consecutive … fragments” (named limit d) — false for two of nine chains

**Counterexample:** `entry` lists chains `L4-L6, L7-L8, L9-L10, L11-L13, L14-L16, L17-L18, L19-L23, L24-L25, L26-L29` as “consecutive fragments … read as one sentence from line order”, and named limit (d) repeats “Consecutive column-line fragments”. Measured against the captures:
- `L17` at S224 line 934, `L18` at line 936; line 935 is left-column text (`review process is a key component of the PRISMA`). Not consecutive column-lines.
- `L24` at S223 line 169 (right column, p.98), `L25` at line 173 (left column, p.99); lines 170 (empty), 171 (`LIGHTNING TALKS … 99` page header), 172 (empty) intervene. Not consecutive; crosses a page break and a column switch.
- The other seven chains are consecutive (including `L11-L13` etc., where the “intervening” lines are the same table’s second cell on the same raw lines). Also `L30` (line 160) precedes `L19` (line 161) in the capture; the table lists it after `L29` — table order ≠ capture order, though no sentence claims otherwise.

K3 (“a quote located only by joining text across columns”) does **not** fire — each individual L-quote is within one raw line and one column (spot-checked raw positions: 65/106/67/0 consistent per chain; the g2 column-join forgery correctly refuses a cross-line join). The overstatement is in the *sentence-reconstruction* description, not in quote location. **Narrowed:** «fragments in one column read in line order (L24-L25 crosses a page break, L17-L18 skips a left-column line)» or drop “Consecutive” from named limit (d) and the `Text forms` paragraph. The Q6 phenomenon the entry itself discloses (line-wrap makes Q6 miss at tree while S223 holds the sentence) already relies on fragments spanning breaks — the limits should say so uniformly.

## §Ed. C2: Located-quotes “equals … one-to-one” — quote-string equality, source unattested

`bindings()` compares Located-quotes quote *strings* as a multiset against GATE-RECORD `quote="…"` strings; GATE-RECORD lines carry no qid. The `source` column of the LQ table is never compared to the GATE-RECORD’s `S…` or capture.
**Counterexample:** `wrong-source.md` = committed entry with `| L1 | S224 → S223`. `bindings(wrong-source)` → `(30, 30, 30, True, 8, 8, 8, 8)` identical to committed; `gate-records verify wrong-source.md` → `records=31 ok=31 fail=0` (exit 0). A systematically wrong source column (or a quote attributed to the wrong capture) passes predicates 1 and 4. All 30 actual rows happen to be correctly attributed (L1–L18 S224, L19–L30 S223, matching GATE-RECORD sid order) — so the claim is true of the bytes, but the “one-to-one” equality is string equality, not attribution equality.
**Narrowed:** «whose Located-quotes quote strings equal, as a multiset, the 30 admitted GATE-RECORD quotes (source column unchecked — reviewer item)» or add a source-equality leg to `entry-controls-r96.py` (zip LQ rows in order against GATE-RECORD lines and compare `S` and capture key).

## §Ee. C2: Do/Never cells — human-review items, not fires under K2 as written

K2 fires when a wave artifact shows a Do/Never cell “asserting what its warranting quotes do not say”. A strict read of the two weakest rows:
- Row 1 Do «document the review of this search specifically» from `L7+L8` (“be conducted generally with publication of a protocol, for / example, this item is designed to document search-specific”) — the quoted fragments end mid-sentence; “peer review.” (next line 892) is unquoted. The Do’s “specifically” leans on the truncated fragment plus the protocol/search-specific contrast in `L7`. Defensible, thin.
- Row 5 Lane «checklists improved search quality in several studies» — `L30` alone (“that peer review checklists were effective at improving search”) does not say “several studies” (line 159 right column, unquoted). Lane cells are by definition the lane’s reading, and named limit (a) reserves fidelity to the reviewer; K2 by its terms covers Do/Never, not Lane. Not fired. Nor does any Do/Never assert improvement of PRISMA-S itself (S224 scope correctly excludes it); Row 5’s Do stays inside `L3` purpose language.
I do not fire K2 under the frozen wording; the lexical-floor finding (§Db) is the operative one. If «warranted» is retained at claim level, then the reviewer item named in limit (a) must actually be executed and filed before landing — it is not filed this round.

## §Ef. C1/C2 axes the brief named, status

- **“scored by the same evaluate”**: §Aa (unenforced directly; regression-leg only). Investigated suspects listed in the seat brief are now ledgered — patched nothing.
- **“writes nothing” vs NO_WRITE**: §Ad (sentence accurate; K4/docstring broad, unenforced).
- **“registers as a gate” vs predicate-3 grep**: §Ac (kind unenforced).
- **DO_NOTHING for another reason**: §Ae (sound as before-check, weak as detector).
- **Source-blind stand-in**: §Ab (encoded cheat passes 23/23, blind to novel defect that real selftest catches at `p03-header`).
- **“warranted” vs lexical floor**: §Db (8/8 negations pass).
- **“real searches” vs the record**: §Dc (counts measured twice; grep provenance prose-only).
- **“opened this round” for S224**: §Dd (timestamp real, bytes identical — honest, re-scoping).
- **Separability**: §H4 (holds; base tool re-runs C2 CLEAN).
- **Text-matching 23-line cheat / regression / shims**: §Aa–§Ab (shim passes noreg, fails only r95 leg; cheat passes noreg default battery; both documented above with shim-forged / real-forged receipts).

## §Receipts index (copied into `w1/`)

- `R96CriticClaims-receipts.txt` — command ledger (positives, predicates, grep, separability, F1–F8).
- `R96CriticClaims-shim-forged.txt` / `R96CriticClaims-real-forged.txt` — shim CLEAN on forged Q2 (exit 0) vs real DRIFT `Q2 COUNT_DRIFT` (exit 1).
- `R96CriticClaims-E1b-shim-noreg.txt` — shim + battery `--no-regression` PASS 23/23.
- `R96CriticClaims-E1b-r95.txt` — shim + r95 battery `RERUN_CONTROLS=FAIL` (only slow leg catches).
- `R96CriticClaims-E2-cheat2-battery.txt` / `R96CriticClaims-E2-cheat-full2.txt` — encoded cheat 23/23 as `--tool` and as committed (default battery, noreg) PASS; cheat-novel PASS vs real-novel `FAIL p03-header` recorded in ledger (scripts retained in scratch, removed there; this receipt holds the lines).
- `R96CriticClaims-E3-dirty-battery.txt` — dirty selftest NO_WRITE=1/1 PASS while writing outside + socket use.
- `R96CriticClaims-warrant-negation.txt` — 8/8 negated-Do passes.
- `R96CriticClaims-C2-gate.txt`, `-C2-meta.txt`, `-C2-rerun.txt`, `-C2-entry-controls.txt` — C2 predicates.
- `R96CriticClaims-C1-battery-noreg.txt` — C1 battery noreg PASS.
- `R96CriticClaims-pcases.txt` — 14 p-cases, 12 with `want=` (refusals), proving docstring 13-overcount.

## §Verdicts

VERDICT: R96CriticClaims C1 fired — "scored by the same evaluate" is unenforced by --selftest (a shim discards the verdict yet still passes every fast leg, and an encoded source-blind cheat scores 23/23 while blind to a novel defect), so the wording claims more than its instruments prove.
VERDICT: R96CriticClaims C2 fired — "each decision row is warranted" asserts entailment while WARRANT_TERMS is a lexical floor passing all 8 negations, and the "consecutive fragments" description is false for L24-L25 and L17-L18.
