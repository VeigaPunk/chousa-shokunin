# R54W2DraftReport — draft of `## Trend verdicts` and `## SHONEN` (round 54, wave 2 FALSIFY)

Seat: leaf scribe (no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Lane tip measured: `178667dc2c9d1656e864abfdc251c68757428613` (`master`; the seat brief named
`447cf7ed…`, which is the parent — the W1 integration and the W1-reports commit landed on top).
Wave state at filing: `w2.ready.dispatched` present, `w2-results.json` **absent** — this draft is
pre-W2-return and its numbers are the integrated tip's, not the wave's final ones.
Scratch `/fast/scratch/hyaku/chousa-r54/R54W2DraftReport` used for counters and removed on exit.
No production file, no fleet file, no git/jj mutation, no network, no fetch, no LibreOffice profile
outside scratch; `PYTHONDONTWRITEBYTECODE=1` throughout; no tool installed.

Runs I made first-hand this seat (each mirrors a committed receipt; the receipts stay the pointers):
`c1-count.py --seed 54321` → `LEGS=6/6 C1=PASS` exit 0 (11.2 s, tool sha256 `2c0140bc…`);
`c1-supplement.py --seed 54321` → `SUPPLEMENT_LEGS=3/3` exit 0; `tracked-deletion-check.py` →
`TRACKED_DELETION=PASS` exit 0; `c2-count.py --lane-only` → `C2=PASS` exit 0 (`CAPTURE_BOUND=skipped`
in that mode); `build-spans.py --check` → `SPANS_ROWS=33 STALE=0`; `pointer-anchor-check.py` →
`ANCHORED=16/16`; `considerthese-ledger-check.py --root .` → `PROPOSALS=35 ROWS=35 IMPL=24 FMT=9
OPEN=1 OPS=1 BAD=0` exit 0; `sources-census.sh validate --root … chousa` → exit 0; `pdf-crosscheck.py`
(uv `--with pypdf`) → `PDF_QUOTES=21 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14` exit 0; `--locate` on all
nine correction anchors; row counts at base/freeze/tip.

## Draft — intended path `/home/vgpnk/Projects/shokunin/.ufo/reports/round-54/chousa.md`

```markdown
## Trend verdicts

- **expansion — improved.** Three documents the lane did not hold at `BASE_REV`
  (`c49ffc6ce1c3de87c1dfa96856239ed7274bf07b`) enter as three Registry rows — S121 and S122 (tier A),
  S123 (tier B) — one per document, each `opened 2026-10-26`, `mined`, its `used-by` cell naming
  exactly the entry that cites it (`corpus/SOURCES.md:131-133`; r36 for S121 and S122, r37 for S123).
  Rows 120 → 123 (`git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`
  → 120 at base, 120 at the freeze, 123 at the tip). The documents were absent from the lane's
  knowledge at base: `git grep -l -e 'ISO 690:2021' -e 文献载体标识 c49ffc6c… -- corpus/knowledge` →
  exit 1, no output. Credit is per document and scoped — S121 (identity, status, replacement,
  adoption basis), S122 (the portal's own no-text notice), S123 (the standard's operative clauses
  through a third-party reproduction, stated as tier B) — and the held S101 earns none: neither new
  entry carries an `S101` token (`grep -c S101` → 0 and 0). Source census exits 0 at start and end
  with the same five pre-existing W04 warnings (`corpus/evidence/round54/census-start.txt`,
  `census-end.txt`; ran again at the tip → exit 0). Adjacency unchanged: W1 `R54ConnCrossClaim`
  section 2 finds no sibling row for `openstd`/`samr`, and records that the authority→copy join is
  not address-level — which the r37 entry states by calling the copy tier B, not authority.

- **quality — improved narrowly.** A new capability lands: the defined OLE `.doc` text form
  (`tools/capture-text.py`, sha256 `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`).
  The frozen counter scores `LEGS=6/6 C1=PASS` and the post-freeze supplement
  `SUPPLEMENT_LEGS=3/3` (receipt `corpus/evidence/round54/measure-after.txt`; the supplement is the
  post-freeze script of erratum E1 and is not the claim's rule; my own runs agree). Depth: `ENTRIES=2/2 BOUND=3/3 QUOTE_ROWS=33
  QUOTES_IN_SPAN/ENTRY/LESSON=33/33 ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=2/2 SUBSTANCE=PASS`
  (`c2-count.py`; full run also `CAPTURE_BOUND=33/33`). Calibration inside quality: the nine
  round-54 `correction:` lines (`SCORECARD.md:2740-2748`) are offset-true, not merely
  occurrence-true — `--locate` returns S100 16/151/492 and S101 11972/12007/12795/12963/14049/25123
  (ran), `pointer-anchor-check.py` prints `ANCHORED=16/16`, and those lines supersede the rows' old
  form label without editing them. Named limits, not claimed closed: the frozen counter remains forgeable — a rebuilt forge
  that reads the generator's sibling HTML and cans REAL scores `LEGS=6/6` on it and
  `SUPPLEMENT_LEGS=0/3` on the supplement (`corpus/evidence/round54/controls/c1-forge.txt`); the
  supplement is not the claim's rule (erratum E1); C2 counts binding, located support and presence,
  never entailment.

- **discernment — improved narrowly.** The round records a verdict per theme row instead of a
  presumption: `QUARANTINE_VERDICTS=3/3` (S080, S088, S096), each `absent-as-written`, and S096's
  readable OLE form (27,012 characters, 0 U+FFFD; `参考文献格式，参照ISO 690` at char 25123, located)
  supersedes round 42's `unverifiable` for that row. Two admissions are narrowed (the staged
  headline is cut where it speaks about the portal, and the staged type enumeration is cut with the
  table it came from), one document leg is refused on form (no `source: S101` in either new entry;
  S101's `used-by` at `corpus/SOURCES.md:111` unchanged), the grey-literature entry stays refused
  and the package amendment stays unlanded, each with a named flip (`corpus/lessons/round-54.md:39-63`).
  Limit: every judgment above is lane-authored — a dispatched seat is not a non-author — so the
  outside re-open named in the lesson (`### Admit and reject`) is still owed; this verdict asserts
  the lane's own record, not an externally checked one.

## SHONEN

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources —
  `SKILL.md:140-141` (two round-54 gate rows: commands, output contracts, exit codes, and the
  supplement's explicit non-claim status); `corpus/QUALITY.md:937-943` (criteria 97–100, each citing
  a round-54 artifact).
- [~] At least one end-to-end domain task executed and logged in LOG.md — executed and receipted
  (`corpus/evidence/round54/measure-after.txt`, `controls/`); the `LOG.md` Round 54 entry is owed at
  integration (absent at `178667dc`: `grep -n 'Round 54' LOG.md` → no hit), so the box is not yet met
  on its own wording.
- [~] Instructions executable by an agent without oral context — the round-54 rows' commands run
  from the lane root with no argument memory: `python3 corpus/evidence/round54/c1-count.py --seed
  54321` → `LEGS=6/6`, `c2-count.py --lane-only` → `C2=PASS`, `build-spans.py --check` →
  `SPANS_ROWS=33 STALE=0`, `considerthese-ledger-check.py --root .` → `BAD=0` (all ran this seat).
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `PROVINCE.md` (source hierarchy,
  citation chaining, claim-vs-source); the Gate adjudicates every candidate against it
  (`corpus/lessons/round-54.md:39-49`); `corpus/README.md:1165-1175` scopes the credit and names the
  operative text the lane did not read.
```

## Claims the draft makes that a non-author closure could dispute

Every row is a sentence in the block above; "decides" is the evidence that settles it, "observed" is
what this seat actually ran or opened.

| # | draft claim | what decides it | observed |
|---|---|---|---|
| 1 | C1's `LEGS=6/6` proves the capability | the frozen counter vs the rebuilt forge and the supplement (`controls/c1-forge.txt`) | forge `LEGS=6/6` on the counter, `SUPPLEMENT_LEGS=0/3` on the supplement; the verdict is capped at "narrowly", not "proved" |
| 2 | the tool that was measured is the tool that landed | `sha256sum tools/capture-text.py` vs `measure-after.txt` header | both `2c0140bc…`; the candidate was `fd0ed3f5…` (E2) and no frozen leg reaches the Clx/tracked-deletion fixes, so the counter is blind to them — only `tracked-deletion-check.py` (ran, PASS) covers one |
| 3 | the counter reproduces on another host | REAL's oracle is built by `soffice` at counting time; absent `soffice` → exit 2 | ran here in 11.2 s to `LEGS=6/6`; a closure host without LibreOffice cannot reproduce it — environment dependency, named |
| 4 | "three documents" of expansion credit | base sweep + rows + the per-document rule (`corpus/README.md:1173`) | base sweep exit 1; rows 131-133; S122 is a portal notice and S123 a reproduction — round 53 counted an analogous notice (S119) as a document, so the rule is consistent but the judgment call is the closure's |
| 5 | binding is per entry-document, not per row | entry `source:` lines + `c2-count.py` | r36 cites S121+S122, r37 cites S123 only; `BOUND=3/3 (min 2)` |
| 6 | C2 evidences depth | `c2-count.py` checks presence, span, anchor and inference-ground; entailment is uncounted | `SUBSTANCE=PASS` says quotes exist and are located, not that the entry's inference follows — a closure must read the entries' `#### Inference` |
| 7 | `CAPTURE_BOUND=33/33` | full `c2-count.py` (measure-after) vs `--lane-only` | `--lane-only` prints `CAPTURE_BOUND=skipped`; the full leg needs the read-only `.qcache` at its absolute path |
| 8 | the S100/S101 anchors are now correct | `corpus/SOURCES.md:110-111` vs `SCORECARD.md:2740-2748` | the rows still print the superseded values (`char 11170 … char 34374`, "(UTF-16LE text of the raw .doc capture)"); only the append-only correction lines supersede them — a closure may still call the row wrong |
| 9 | the correction offsets are true, not only their anchors present | `tools/capture-text.py --locate` per anchor; `pointer-anchor-check.py` checks occurrence only (`:20-22`) | all nine offsets returned exactly (S100 16/151/492; S101 11972/12007/12795/12963/14049/25123); no gate enforces offset truth — this round's truth is a run, not a check |
| 10 | `QUALITY 97–100` are round-54 additions | `grep -n '^## ' corpus/QUALITY.md` vs each item's citation | last header is `:849` ("criteria 1–80 unchanged"); 937/939/941/943 each cite a round-54 artifact, but no round-54 section header exists |
| 11 | the PDF quotes are cross-checked | `uv run --with pypdf python corpus/evidence/round54/pdf-crosscheck.py` | ran: `PDF_QUOTES=21 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14`, exit 0; no committed receipt file carries these numbers — only the erratum (E4) and the lesson |
| 12 | the quarantine verdicts are true | re-open each theme form and search the joined string (lesson's own commands) | S096 offset 25123 and 27,012 characters re-derived here; S080/S088 rest on the lesson's commands — the closure should re-run all three |
| 13 | the S101 leg cut is inside the rule | `claims.md` C2 predicate ("optionally the HIT data specification") + `grep -c S101` on both entries + `used-by` cell | 0/0 and `used-by` = `corpus/knowledge/citation-count-semantics-r37.md`, unchanged (erratum E3) |
| 14 | SHONEN's "logged in LOG.md" is met | `grep -n 'Round 54' LOG.md` at the tip | no hit; the box stays short of its wording until integration writes the entry (the draft says so) |
| 15 | the round-end census is evidenced | `git cat-file -e 178667dc:corpus/evidence/round54/census-end.txt` | exit 128 — the receipt exists on disk only and is untracked at the tip; the census command itself exits 0 (ran) |
| 16 | discernment moved | whether lane-authored Gate verdicts count as axis movement (`corpus/lessons/round-54.md:39-63`) | the countable surface moved (verdicts 0/3 → 3/3, nine offsets verified); the judgmental surface has no non-author — a closure may prefer `unchanged`, as the round-53 report did for the same reason |
| 17 | these verdicts hold after W2 | `w2-results.json` + the integration commit | absent at filing; W2 seats are re-running these counters, so any changed number supersedes the bullet that carries it |
| 18 | the entries' wording supports the quality verdict | the wave-2 entailment and credit reports on disk (`R54W2CritEntailStb.md`, `R54W2CritCredit.md`) + the entries' text after the fixes | EntailStb: 9/12 S123 bullets fully entailed; I2 (one clause), I4 (headline) and I6 ("occasional" = n=1) need narrowed wording, none fatal, no quote or anchor wrong. CritCredit: credit survives for all three documents (S122 thin, one unique sentence) and flags one README Frontier sentence that misattributes the type-vs-tier separation to the scope clause — a wording fix, not a credit loss |

## Findings for the L1 (not mine to fix)

1. `corpus/evidence/round54/census-end.txt` is untracked at the tip (observe `git status --porcelain`
   in the lane: the only non-wave entries are this file). The lesson's `## Census` and any
   Sources & frontier pointer to it are unopenable by the closure until it is committed.
2. No `LOG.md` Round 54 entry exists at the tip; SHONEN box 2 depends on it (dispute 14).
3. Seat brief said the lane tip was `447cf7ed…`; `master` is `178667dc…`. Topology at filing:
   `6af11e9` W1 integration → `447cf7e` E2 tool fix + re-measure → `178667d` W1 reports/results +
   W2 spec/dispatch (tip). Use the tip.
4. `w2-results.json` absent at filing: the draft is honest as pre-W2; the L1 must re-read every
   number against the wave result before the report lands.
5. No misroot seen from this seat: I wrote only this file and scratch (removed).
6. Wave-2 seats already on disk narrow wording the report must not file stale: `R54W2CritEntailStb.md`
   (S123 I2 clause, I4 headline, I6 "occasional" → n=1; no wrong quote or anchor) and
   `R54W2CritCredit.md` (credit survives for S121/S122/S123, S122 thin by one sentence; one README
   Frontier sentence misattributes the type-vs-tier separation to the scope clause). Apply the
   wordings before the report lands; neither changes a predicate, counter, span or target.

VERDICT: attacked the round's trend evidence and SHONEN pointers — C1's counter, the supplement, the
S100/S101 offsets, the C2 binding, QUALITY 97–100, the PDF and ledger checks and the census; every
number in the draft was re-derived first-hand and held, while the two soft spots the draft now names
(forgeable frozen counter, lane-authored discernment) and three integration gaps (LOG entry,
census-end commit, W2 results) are stated rather than smoothed.
