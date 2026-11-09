# R99ExecC2Repro — C2 independent reproduction

Freeze F `d41f4cd8b857c6de683e7be5c5e8125b32763a8e`, base `47ed34fa785288837f84cde9db15c41300854a78`.
Shared clone at `$S/repo` (checked out F); base captures at `$S/base` via `git archive 47ed34fa… corpus/captures | tar -x`.
Scratch `/fast/scratch/hyaku/chousa-r99/R99ExecC2Repro`. No lane scripts were used for (c) or (d).

## (a) Four counting commands (cwd `$S/repo`)

| # | command | observed tail | exit |
|---|---|---|---|
| 1 | `python3 -B tools/gate-records.py verify --root . corpus/knowledge/quotation-error-rates-r99.md` | `GATE_RECORDS files=1 records=25 ok=25 fail=0` | 0 |
| 2 | `bash tools/research-gate.sh verify-metadata corpus/knowledge/quotation-error-rates-r99.md --root .` | `METADATA_COMPLETE=1/1` + `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)` | 0 |
| 3 | `python3 -B tools/search-rerun.py verify corpus/knowledge/quotation-error-rates-r99.md --root .` | `SEARCH_RERUN_SUMMARY searches=4 rev_match=4/4 tree_same=0/4` + `SEARCH_RERUN: CLEAN` | 0 |
| 4 | `python3 -B corpus/evidence/round99/entry-controls-r99.py --root .` | `QUOTES=23/23 FIELD=9/9 IDENTITY=2/2 WARRANTS=8/8 NUMBERS=6/6 TOPIC=1/1 NUMBERS_SOURCED=6/6 BASE_TOPIC_HITS=0 BASE_ENTRY=absent FORGERY_REFUSED=10/10 ACCEPTED=2/2` + `ENTRY_CONTROLS_R99=PASS` | 0 |

Receipts: `R99ExecC2Repro-a{1..4}-*.txt`. All match the frozen predicate verbatim.

## (b) `## Searches` re-run at base (GNU grep 3.12, `$S/base`, 97 captures)

| id | expression | recorded | mine | receipt |
|---|---|---|---|---|
| Q1 | `quotation error` | 0 | 0 | `R99ExecC2Repro-b-search.txt` |
| Q2 | `Jergas` | 0 | 0 | same |
| Q3 | `Mogull` | 0 | 0 | same |
| Q4 | `failed to substantiate` | 0 | 0 | same |

Each `/usr/bin/grep -l -F` printed no file (hits=0 by `wc -l`). Agreement 4/4.

## (c) Independent ≤40-line checker (no lane scripts) — `R99ExecC2Repro-mine.py`

Normalizes only curly quotes + whitespace (my own code, not `tools/gate-records.py`):

- `quotes_parsed=23`, `QUOTES_IN_CAPTURE=23/23 J0_OK=1/1 J1-J8_OK=8/8`
- `decision_rows=8`; every Do-cell number found in its row's warrant quotes: row1 `28,25.4%,11,9%,14.5%` all True; row5 `6.7%` True; row7 `64.8%` True; rows 2,3,4,6,8 have no Do-cell numbers (vacuous True, consistent with the controls' `NUMBERS=6/6` counting only the three numbered rows' six numerals).
- J0 normalized-equal to JSON `title` (`Quotation accuracy in medical journal articles-a systematic review and meta-analysis.`); J1–J8 each in `abstractText`. Controls agree: `QUOTES=23/23 FIELD=9/9 NUMBERS_SOURCED=6/6`.
- Identity (K3): JSON `pmid=26528420 doi=10.7717/peerj.1364 journalInfo={volume:3, yearOfPublication:2015, journal:PeerJ}`; S233 capture contains `10.1371/journal.pone.0184727` and the G0 title.

Receipt: `R99ExecC2Repro-c-mine.txt`.

**K5 spot-check (reviewer judgement, my reading):** I find no widening/reversal. Row 1's "treat an unchecked citation as unreliable" is an entry-level gloss, not attributed as the sources' imperative (the Never column makes this explicit); the numbers it states are all warrant-printed. Row 3's "(the cited source was not read)" matches G6's "secondary (or indirect) citations" without reversal. Row 6's "sample quotations, not only references" is supported jointly by G12+G13. Named limit (c)/(d) already disclaim full paraphrase coverage; I add nothing to K5.

## (d) Live re-open (two URLs only, into `$S/live`, one attempt each)

- `curl -sL … journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727` → exit 0, 229201 bytes, sha256 `7af06e35…2b` (live copy in `$S/live/plos.txt`, receipt `R99ExecC2Repro-live-sha.txt`).
- `curl -sL … europepmc …/search?query=EXT_ID:26528420%20AND%20SRC:MED&resultType=core&format=json` → exit 0, 4773 bytes, sha256 `90bb2033…df06d` (`$S/live/epmc.json`).

Located in my own copies (normalized, `R99ExecC2Repro-live2.py` / `R99ExecC2Repro-d-live.txt`): **G4 True, G10 True, G11 True, J2 True, J3 True**. Also: `live_abstr==cap_abstr: True`, `live_title==cap_title: True` — the Europe PMC live record matches the committed capture byte-wise in the checked fields (live sha differs from capture sha `6b0bcbda…` only because the full JSON blob is re-served; the title/abstract fields are identical).

## refetch.tsv comparison (FINDING)

`corpus/evidence/round57/refetch.tsv` rows:

- S233: raw sha `7af06e355a570263cfa6786d7b60d7f3e821e8b5f8597ab29d6605e0a17f8f2b`, text sha `60048511…29a78f790d3`; my live sha `7af06e35…2b` **equals the raw sha exactly** (publisher page byte-identical to the round's fetch) — text sha `60048511…` matches the committed capture.
- S236: raw sha `6b0bcbda…886ac31`, text sha `6b0bcbda…` (JSON served as one line, raw==text); **my** live fetch hashes `90bb2033…f06d`, which matches **neither**. The abstract/title fields are identical, so the difference lies elsewhere in the JSON (presumably server fields such as `cursorMark`/timestamps). This is drift in unquoted envelope fields, not in any cited text — but the refetch row's sha and my live sha differ, and the claim's "opened this round" rests on the capture, which remains valid and quote-accurate. I record the deviation, not a kill: no quote, number, or identity in the entry changes value under the live record.

No control battery (`entry-controls-r99.py`) reads `refetch.tsv`; nothing in the predicate binds live-sha to capture-sha. Named-limit review: none of (a)–(d) is contradicted.

## K1–K5 vs effort

K1 (quote/field): held — 23/23, J0=title, J1–J8 in abstractText. K2 (Do-cell numbers): held — all numbered Do cells sourced. K3 (identity): held (pmid/doi/year/journal/volume; doi/title). K4 (forgeries/no-claim): held — `FORGERY_REFUSED=10/10 ACCEPTED=2/2`. K5 (paraphrase): held on spot-check (above).

Tooling: no installs (operator RULES read; pacman pause noted, nothing installed). All receipts cited are copied into `.ufo/waves/round-99/w1/` as `R99ExecC2Repro-*`.

VERDICT: R99ExecC2Repro C2 held — all four counting commands, searches, quotes, numbers and live re-opens reproduce as frozen; one non-killing drift (Europe PMC envelope sha) recorded.
