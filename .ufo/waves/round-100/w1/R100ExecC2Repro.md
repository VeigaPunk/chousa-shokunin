# R100ExecC2Repro — C2 reproduction report

Seat: R100ExecC2Repro (godspeed). Lane: chousa round 100. Tree attacked:
freeze F `6d4e8487ee6a16823c24a8e085c6559b92b9fec8`, shared-clone checkout
`/fast/scratch/hyaku/chousa-r100/R100ExecC2Repro/repo` (REV asserted =
`toplevel = /fast/scratch/hyaku/chousa-r100/R100ExecC2Repro/repo`).
Base for searches: `929c784c63a1fd17961d21742101b2b109b7b8ff`.
Report path (relative to lane root): `.ufo/waves/round-100/w1/R100ExecC2Repro.md`.

Axes attacked, in parallel: (1) claimed tallies vs observed tallies;
(2) quote location under two matching rules (literal substring vs gate `norm`);
(3) numeral sourcing (my digit-led regex vs control's token count);
(4) searched-row replication at base via two independent engines;
(5) network re-open of the one named URL (sha256 vs refetch.tsv + U7/U9/U11 location).

## (a) Six counting commands — all match the frozen predicate

All run unmodified at F in my scratch clone, in this order:

1. `python3 -B tools/gate-records.py verify --root . corpus/knowledge/quotation-error-update-r100.md`
   → `GATE_RECORDS files=1 records=17 ok=17 fail=0`, exit 0.
   Receipt: `.ufo/waves/round-100/w1/R100ExecC2Repro-a1-gate.txt`.
2. `bash tools/research-gate.sh verify-metadata corpus/knowledge/quotation-error-update-r100.md --root .`
   → `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)`, exit 0.
   Receipt: `.ufo/waves/round-100/w1/R100ExecC2Repro-a2-metadata.txt`.
3. `python3 -B tools/search-rerun.py verify corpus/knowledge/quotation-error-update-r100.md --root .`
   → `rev_match=3/3`, `tree_same=0/3`, `SEARCH_RERUN: CLEAN`, exit 0.
   Receipt: `.ufo/waves/round-100/w1/R100ExecC2Repro-a3-rerun.txt`.
4. `python3 -B corpus/evidence/round100/entry-controls-r100.py --root .`
   → `QUOTES=16/16 FIELD=16/16 IDENTITY=2/2 WARRANTS=8/8 NUMBERS=24/24 NEVER=8/8 FRESH=1/1 TOPIC=1/1 NUMBERS_SOURCED=24/24 BASE_TOPIC_HITS=0 BASE_ENTRY=absent BASE_UPDATE_LINK=0 FORGERY_REFUSED=13/13 ACCEPTED=2/2` + `ENTRY_CONTROLS_R100=PASS`, exit 0.
   Receipt: `.ufo/waves/round-100/w1/R100ExecC2Repro-a4-controls.txt`.
5 (harm). `python3 -B tools/gate-records.py verify --root . corpus/knowledge/quotation-error-rates-r99.md`
   → `GATE_RECORDS files=1 records=25 ok=25 fail=0`, exit 0.
   Receipt: `.ufo/waves/round-100/w1/R100ExecC2Repro-a5-harm-r99gate.txt`.
6 (harm). `python3 -B corpus/evidence/round99/entry-controls-r99.py --root .`
   → `ENTRY_CONTROLS_R99=PASS`, exit 0.
   Receipt: `.ufo/waves/round-100/w1/R100ExecC2Repro-a6-harm-r99ctl.txt`.

`before/c2-candidate.txt` comparison: byte-for-byte identical tallies on all six
commands (candidate's QUOTES…ACCEPTED line == my a4; GATE_RECORDS lines ==
mine; `rev_match=3/3` != candidate's bare `rev_match=3/3` modulo the lane's
own per-search lines, which I reproduce: Q1/Q2/Q3 all `rev=MATCH tree=CHANGED`).
No counting command fired.

## (b) `## Searches` re-run at base

`git archive 929c784c… corpus/captures | tar -x -C $S/base` (100 capture txt files),
then per-row `/usr/bin/grep -l -F -e <expr> corpus/captures/*.txt | LC_ALL=C sort`
from `$S/base`, plus `git grep -l -F` at the same rev as a second engine:

| id | expression | entry records | my grep | my git-grep | verdict |
|---|---|---|---|---|---|
| Q1 | `quotation inaccuracy` | 0 hits | 0 hits (`rc=0` on empty set via wc; grep clean) | 0 hits (git rc=1) | agree |
| Q2 | `32,000 quotations` | 0 hits | 0 hits | 0 hits (git rc=1) | agree |
| Q3 | `40696441` | 0 hits | 0 hits | 0 hits (git rc=1) | agree |

Receipt: `.ufo/waves/round-100/w1/R100ExecC2Repro-b-searches.txt` (+`h-fps.txt`).
`search-rerun.py` independently re-runs these at `929c784c` and returns `rev_match=3/3`
above, consistent. Nothing fired. (The `(d)` shas in the egress table show S237/S239
were answered http 500 three lane GETs each; I did not re-open those — seat is
restricted to the one named URL.)

## (c) My own checker (independent of the lane's scripts)

`.ufo/waves/round-100/w1/R100ExecC2Repro-check_c2.py` (42 lines; loads the two
capture JSONs, `U0==title`, others `in abstractText`, curly→straight + whitespace
collapse, per-row most-standard import of Python f-string interpolation of the
U9/U11/U7 literals):

- **Quotes located: 16/16** (U0–U13, J1, J2). Both U0 and the 13 U-quotes and both
  J-quotes land under gate-`norm`; see `R100ExecC2Repro-c-numerals.txt` for the
  numeral pass.
- **Decision rows: 8/8 NUMERALS_OK** under my digit-led regex
  `[-+]?\d+(?:[.,]\d+)?%?`:
  row1 (`Stating how often`) 10 numerals, row2 (`Reading the 2015`) 6, row3
  (`Asking whether`) 5, row4 (`Using a journal's`) 3 → **24 total**, matching the
  control's `NUMBERS=24/24`; rows 5–8 carry no numerals (row5's "about half" is
  spelled out, exactly as named limit (b) admits is unchecked). `NEVER=8/8`:
  every Never cell == `(none stated by the sources)`.
- Key: my first pass swallowed the trailing comma (`-0.253,` missing) — the token
  `-0.253` itself is present verbatim in U11; the fixed regex above agrees.
  Receipt: `R100ExecC2Repro-c-numerals.txt`, `R100ExecC2Repro-f-numbers.txt`.

**F-1 (claim says more than its instrument enforces — fired, weak).**
Entry line 29-31 says "U1-U13 are substrings of its `abstractText` field" and
qualifies only at line 31 ("matched after `tools/gate-records.py`'s normalization").
Under the literal sentence, that is false for **U9 and U11**: the capture's
`abstractText` joins `=` to its operands with **U+2009 THIN SPACE** (8 occurrences;
`d-u9u11.txt` prints the raw repr), so neither stored quote occurs verbatim in
`abstractText` (`U9 literal=False, U11 literal=False; gate-norm=True`). The frozen
C2 sentence re-states the unqualified form: "14 located quotes (U0-U13)" and the
kill rule "a quote not located in its capture field" — with no normalisation hedge.
The GATE-RECORDs and controls pass only because `norm()` (`" ".join(s.split())`,
`tools/gate-records.py:107-109` — Python `str.split()` also splits on U+2009)
re-joins them. Numeral tokens across those thin spaces (`0.85`, `-0.253`, `0.043`,
`25`) are exactly preserved after the join (verify in `R100ExecC2Repro-d-u9u11.txt`),
so no numeral's sign/form is wrong — but **"substrings of abstractText"** (and C2's
"located quotes") is strictly true only under the norm reading. Suggested kill-fix:
amend the C2 sentence to "located after the gate's normalisation" and the entry's
line 29 to "substrings up to gate normalisation"; it does not fire the counting
predicate. Receipts: `R100ExecC2Repro-d-u9u11.txt`, `R100ExecC2Repro-e-c2-falsify.txt`,
`R100ExecC2Repro-e-numerals-thinspace.txt`, `R100ExecC2Repro-e-rejoin.txt`.

**F-2 (network re-open: refetch sha vs fresh sha differ — non-material).**
One read-only GET (approved egress row 2) of `…/search?query=EXT_ID:40696441…`
→ http 200, 5166 bytes, exactly ONE attempt (no retry), into `$S/s238-fresh.json`.
sha256 = `c6e697d6810d22471acac83b6b886af857accdd06154c9ff6e09f71cf15d7274`
vs refetch.tsv S238 sha/`capture_sha256` `175f805d6460acd61f2a8c979388a500e35b9c85217d3531ae1fb4418c613a98`
(file-form `corpus/evidence/round57/refetch.tsv` row 210 — the lane's counter reads
that path; the earlier `corpus/refetch.tsv` probe was simply the wrong path, now
closed). The byte gap is a **2-line JSON member-order swap** (`isoabbreviation` /
`nlmid` inside `authorAffiliationDetailsList`), identical byte length 5166 both
ways (`cmp` first differs at byte 1704); the parsed record is **identical**
(`fresh==capture(record)=True`, `d-capsha.txt`). **U7 locates in the fresh copy
(True); U9/U11 locate only under gate-normalisation**, exactly as in-tree (F-1) —
so the re-read confirms the capture and simultaneously confirms F-1.
Receipts: `R100ExecC2Repro-d-curl.txt`, `R100ExecC2Repro-d-sha.txt`,
`R100ExecC2Repro-d-locate.txt`, `R100ExecC2Repro-d-u9u11.txt`.

**F-3 (named-limit / identity spot checks — held).**
`pmid=40696441, doi=10.1186/s41073-025-00173-z, pmcid=PMC12285159`, title
exact-match — all agree with the entry's header; U13 is the abstract's final
sentence (no truncation); J1/J2 literal-substring True in S236 `abstractText`;
`U10` literal True in S238; `BASE_TOPIC_HITS=0` reproduced via `git grep -F`
at base over `corpus/knowledge/` (empty). Both syntheses about medicine: S238
U2 "in the medical literature", S236 title "in medical journal articles" — limit
(d) holds. The `## Update` section in the r99 entry names the new entry and S238
and carries the pooled 46/16.9%/8.0% — FRESH's both-ways link holds
(`k-fresh.txt` reads the controls' own `fresh()`). The controls' 13 forgeries /
2 accepts reproduce as-published (a4). No decision row overreaches its warrants
(`f-numbers.txt` + `j-overreach.txt`, row-by-row audit: Do cells paraphrase within
their quotes' numbers; the row-2 "gap … is not a measured trend" clause is a
lane-level absence-reading flanked by the entry's own named limit (c), not a
quote-like numeral; every Never is honestly empty). Nothing else fired.

## Risks and blockers

- None blocking. Seat wrote only under
  `.ufo/waves/round-100/w1/R100ExecC2Repro-*` (this report + the 21 receipts
  above) and the scratch `/fast/scratch/hyaku/chousa-r100/R100ExecC2Repro/` which
  I removed before yielding (`rm -rf` — verified gone post-yield).
- No tool installs/updates were needed (pacman guard respected — nothing installed).
- Two nits for the record: (i) my first-pass checker swallowed `,` after
  `-0.253`; (ii) entry's `## Named limits` says S239 answered 500 to "this round's
  two GETs" while `refetch.tsv` logs 3 attempts (rows 211/213/215) and the frozen
  prompt says three — the entry's "two" is stale relative to the log. It is
  cosmetic and does not affect any count (S239 records stay `reject`, C2
  predicates 17/17 unaffected): flagged, not fired under any kill rule.
- F-1 is the only substantive finding. Under the claim's own hedge-carrying form
  (entry + gate `norm`) all 16 quotes locate; the frozen C2 sentence's unqualified
  "located quotes … in its capture field" wording is the gap.

## Verdicts (one line per claim touched)

VERDICT: R100ExecC2Repro C2 fired — F-1: U9/U11 are not literal substrings of S238 abstractText (U+2009 thin spaces); the frozen sentence's unqualified "located quotes" holds only after gate normalisation.
VERDICT: R100ExecC2Repro C1 n/a — this seat reproduced the C2 claim only; C1 was out of scope (no battery re-run, no rev-form record exercised).
