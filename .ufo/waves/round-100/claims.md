# chousa round 100 — frozen claims (L1 `ChousaR100`)

Base `929c784c63a1fd17961d21742101b2b109b7b8ff` (round-99 landing plus its non-author spot-check). Two claims, two
axes, no exploratory claim. C1 works the lowest-scoring axis (operability, historical 3/10). C2 is sourced on S238,
opened this round. Pre-freeze controls (do-nothing, forgery, setup) were run on a clean shared clone at the pre-freeze
build commit P and committed before this file (`corpus/evidence/round100/before/`); P's hash is recorded in
`plans/round-100.md` `## Freeze`.

## C1 `C1-GATE-REVCAP-R100` — operability

**Sentence.** `tools/gate-records.py verify` fails a rev-form GATE-RECORD with CHALLENGE when the blob git resolves for
`rev:path` has the object id of a `corpus/captures/<24 hex>.txt` or `.raw` entry of that rev's tree, and that capture's
text — for a `.raw` entry, its sibling `.txt` at that rev when one exists — is a challenge page by the unchanged round-99
rule (≤200 words after normalization and one of 11 markers). Round 99's tool judged a rev record only when its path was
spelled exactly `corpus/captures/<24 hex>.txt`; `./corpus/captures/<key>.txt`, `./corpus//captures/…`,
`./notes/../corpus/captures/…`, `<key>.raw` and a byte copy at another path resolved to a challenge blob and printed OK.
A rev record whose blob is not a capture of that rev is not judged by CHALLENGE.

**Counting command.** `python3 -B corpus/evidence/round100/challenge-controls-r100.py --root . --work <scratch>`

**Predicate (frozen).** stdout carries exactly the line
`NEG=7/7 MARK=11/11 BOUND=3/3 NORM=2/2 POS=4/4 REV=11/11 REVPOS=3/3 PROD=6/6 HARM_SAME=<n>/<n> BASE_REV_ADMITTED=8/11 ORACLES_REJECTED=12/12`
with n ≥ 26, and the line `CHALLENGE_CONTROLS_R100=PASS`; exit 0.

**Before.** The base tool (`git show 929c784c:tools/gate-records.py`) through the same battery, `--tool <base>
--no-oracles`: `REV=3/11`, `PROD=4/6`, `CHALLENGE_CONTROLS_R100=FAIL`, exit 1
(`corpus/evidence/round100/before/c1-base.txt`).

**Kill rule.** C1 fails if the predicate line differs, the battery exits non-zero, any HARM file differs from the base
tool's stdout and exit code, or any wave artifact shows a rev record whose blob has a capture's object id at that rev,
whose capture text is a challenge page by the round-99 rule, and which this tool prints OK.

**Named limits.** (a) The url/admit rule and the challenge rule itself are unchanged: a challenge page in other words,
or longer than 200 words, still passes (round-99 limits). (b) Identity is byte identity: a rev blob that differs from
every capture of that rev by one byte is not judged, whatever its text. (c) The capture set is read from GITDIR's tree
at the record's rev, not from the working tree. (d) A `.raw` entry with no sibling `.txt` at that rev is judged by its
own bytes. (e) The battery's oracles are the twelve named stand-ins, not every possible forger (QUALITY 126).

## C2 `C2-ENTRY-UPDATE-R100` — freshness

**Sentence.** The round-99 entry's `recheck: on-release` fired and was answered: new entry
`corpus/knowledge/quotation-error-update-r100.md` holds the authors' 2025 update (Baethge & Jergas, Research Integrity
and Peer Review 2025, pmid 40696441) through its own abstract in Europe PMC's core record (S238, tier B, opened this
round) — 14 located quotes (U0-U13) plus J1/J2 from S236, and 8 decision rows whose every Do/Never numeral is a token of
that row's own warrant quotes — and `corpus/knowledge/quotation-error-rates-r99.md` carries a `## Update` section that
names the new entry and S238, so the stale 2015 reading is flagged where it is held.

**Counting commands.**
1. `python3 -B tools/gate-records.py verify --root . corpus/knowledge/quotation-error-update-r100.md` →
   `GATE_RECORDS files=1 records=17 ok=17 fail=0`, exit 0
2. `bash tools/research-gate.sh verify-metadata corpus/knowledge/quotation-error-update-r100.md --root .` →
   `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN`, exit 0
3. `python3 -B tools/search-rerun.py verify corpus/knowledge/quotation-error-update-r100.md --root .` → `rev_match=3/3`,
   `SEARCH_RERUN: CLEAN`, exit 0
4. `python3 -B corpus/evidence/round100/entry-controls-r100.py --root .` → the line
   `QUOTES=16/16 FIELD=16/16 IDENTITY=2/2 WARRANTS=8/8 NUMBERS=24/24 NEVER=8/8 FRESH=1/1 TOPIC=1/1 NUMBERS_SOURCED=24/24 BASE_TOPIC_HITS=0 BASE_ENTRY=absent BASE_UPDATE_LINK=0 FORGERY_REFUSED=13/13 ACCEPTED=2/2`
   and `ENTRY_CONTROLS_R100=PASS`, exit 0
5. harm: `python3 -B tools/gate-records.py verify --root . corpus/knowledge/quotation-error-rates-r99.md` → unchanged
   from base (`records=25 ok=25 fail=0`), and `python3 -B corpus/evidence/round99/entry-controls-r99.py --root .` →
   `ENTRY_CONTROLS_R99=PASS`

**Before.** At base the entry is absent (gate exit 2, controls exit 2; `before/c2-base.txt`). Pre-link control — the
new entry present but the round-99 entry without `## Update` (the cheapest do-nothing that skips the freshness flag):
`FRESH=0/1`, `ENTRY_CONTROLS_R100=FAIL`, exit 1 (`before/c2-prelink.txt`).

**Kill rule.** C2 fails if any counting command's line or exit differs, or any wave artifact shows a decision row's Do
or Never cell stating something its warrant quotes do not say (overreach), a quote not located in its capture field, or
a number whose sign or form differs from its warrant.

**Named limits.** (a) S238 is the abstract only; the full text (S239, PMC12285159) answered http 500. (b) The controls
check numerals as tokens; spelled-out quantities ("about half") and a paraphrase's sense are not checked. (c) The 2015
and 2025 rates pool different study sets; the entry computes no difference. (d) Both syntheses are about medicine.

## Separability

C1 touches `tools/gate-records.py` and its battery; C1's battery reads the S233/S236/S229/S230/S234 captures and the
lane's GATE-RECORD files (HARM), which include C2's entry once landed: HARM compares the candidate with the base tool on
that file too, and C2's entry has no rev record. C2's counters run with the base tool unchanged (`tools/gate-records.py`
at base checks url/admit and unreach records identically: no rev record, no challenge capture in C2's entry).

## Amendments

(none at freeze)

### F2 amendments (wave-forced; no predicate, counter code, kill rule or target changed)

Each narrows a sentence to what its instrument enforces, citing the wave artifact; the C1 tool and battery bytes and the
C2 controls bytes are identical F..F2. C2's entry and the round-99 `## Update` prose were repaired (B1-B3); every C2
tally is unchanged at F2.

- **A1 (C1, "that rev's tree").** `R100CriticClaims` F-1, `R100ExecC1Repro` finding 1 and `R100MutantsC1` survivor
  `n-cache-repoonly`: the battery's fixture repo has one commit and its PROD legs read one lane revision, so a stand-in
  that builds the capture set at HEAD, or caches it per repo, prints the frozen PASS line. Seat probes show the F tool
  reads the record's rev (`R100CriticClaims` v1/v2, `R100ExecC1Repro` x-revA/x-revB), but no frozen leg enforces it.
  The sentence is judged without "of that rev's tree": **the blob git resolves for `rev:path` has the object id of a
  `corpus/captures/<24 hex>.txt` or `.raw` entry (in the battery, the one fixture commit's tree or the lane's BASE
  tree)**. Named limit (f): which revision's tree supplies the capture set is shown by seat probes only; a two-commit
  fixture with cross-rev legs and a two-rev single-file record is routed to round 101.
- **A2 (C1, `.raw` sibling).** `R100ConnectorSiblings` F1: a record citing `<key>.raw` whose own bytes are a challenge
  page while its sibling `.txt` is not prints OK — the quote is located in one file and the CHALLENGE verdict read from
  another. The sentence defines the judged text as the sibling `.txt`, so the tool does what it says; named limit (g)
  states the shape so the kill rule's "capture text" reads as the sentence defines it, never the `.raw` bytes.
- **A3 (C1, battery strength).** `R100MutantsC1` battery loosenings b1, b4-b7, b9 pass the F tool: the battery's own
  PASS does not check a REV verdict's code beyond rc (b1), HARM on one channel (b4/b5), a missing oracle site (b6), or
  the BASE count (b7, which the frozen predicate regex does check). Named limit (h): the battery's PASS is weaker than
  the frozen predicate line; the predicate line is the claim.
- **A4 (C1, "not judged" quadrant) — no narrowing.** `R100CriticClaims` F-2 and `R100ExecC1Repro` finding 2 say no leg
  admits a challenge-shaped non-capture blob. REVPOS q3's blob (`corpus/evidence/captures-note.txt`, 16 words,
  "reCAPTCHA") is challenge-shaped by the round-99 rule (`corpus/evidence/round100/after-f2/q3-note-is-challenge.txt`:
  `is_challenge=True`) and must be admitted; both seats' universal stand-ins fail on q3. Recorded, sentence unchanged.
- **B1 (C2, row 2 Do).** `R100ReviewerC2` row 2: "the gap between them is not a measured trend" is stated by no
  warrant; moved to the Lane cell as the lane's reading. The round-99 `## Update`'s "their gap is not a trend" reworded
  the same way. Row 4's "were not" restored to the warrant's "were not statistically significantly associated"
  (`R100ReviewerC2` row 4).
- **B2 (C2, GET count).** `R100ReviewerC2`: the entry said S239 answered 500 to "both"/"two" GETs; `refetch.tsv` has
  three each for S237 and S239. Fixed in the entry.
- **B3 (C2, "located").** `R100ExecC2Repro` F-1: U9 and U11 are not byte substrings of `abstractText` (the record
  prints U+2009 thin spaces); they are located after `tools/gate-records.py`'s normalization. The sentence's "14
  located quotes" means located after that normalization; the entry says so.
- **B4 (C2, "fired and was answered").** `R100ConnectorSiblings` F2 and `R100CriticClaims` F-6: FRESH checks that the
  round-99 `## Update` names the new entry and S238 and that `updates:` points back — not that the section's prose is
  true; an Update stating the opposite passes. The sentence is judged without "fired and was answered": **the round-99
  entry carries a `## Update` section that names the new entry and S238**. Named limit (e): the flag's content is
  checked by review only.
- **B5 (C2, Do/Never numerals).** `R100CriticClaims` F-4/F-5: all 8 Never cells are "(none stated by the sources)" and
  carry no numeral, so "every Do/Never numeral" is vacuous for Never cells; a Do cell that inverts its warrant's sense
  with the same numerals passes (named limit (b) already). The sentence is judged as **every Do numeral is a token of
  that row's own warrant quotes; every Never cell is "(none stated by the sources)"**.
- **B6 (C2, study sets and the full text).** `R100ScoutSources` F-1/F-2a/F-2b: with the lane's own recipe a seat's
  read-only re-open of PMC12285159 answered 200 (S239's flip condition met by a seat, not by a lane GET — the lane's
  three attempts were spent); its body says the 46 studies are 18 new plus the 2015 review's 28 and re-calculates those
  28 at 17.0%. The entry's "different study sets" and the round-99 `## Update`'s same phrase said more than the
  abstracts; both now say the abstracts print 28 and 46 and state no comparison, and record the seat's report as not
  held. C2 named limit (a) is read with "to the lane's three GETs"; a lane GET of the full text is routed to round 101.
- **B7 (C2, row 1).** `R100ScoutSources` F-2d: "major errors 8.0% … over 46 studies" bound both rates to one count;
  the abstract does not say it (the body pools major errors over 36). The Do cell now separates the rates from the
  search's count; numerals unchanged.
- **B8 (C2, round-99 `## Update`, major/minor).** `R100ScoutSources` F-2c: "the 2025 abstract does not define major and
  minor" is true of the abstract only; the Update now says the article body (not held) defines both.
- **B9 (C2, named limit on the impact-factor correlation).** `R100ScoutSources` F-2d: "a correlation over 25 data
  points" said more than the abstract's "binomial test, N = 25"; reworded.

C2 tallies after B1-B9 (entry and Update prose only): identical to F (`corpus/evidence/round100/after-f2/c2-all.txt`).

### F3 amendments (C1, after `R100SentinelC1`, the last seat to report; tool, battery and predicate unchanged)

- **A5 (C1, which sibling).** `R100SentinelC1` F-1: `capture_oids` keeps one path per object id (`.txt` wins, else the
  last listed), and `rev_capture_text` reads the sibling of that mapped path, not of the path the record names. A
  byte-identical copy of S230's `.raw` added under an earlier capture key with a benign sibling makes a rev record on
  the honest `b5b8d050….raw` print OK (`R100SentinelC1-oid-collision-evidence.txt`, rows B-D). This wave artifact meets
  the frozen kill rule's literal text ("a rev record whose blob has a capture's object id at that rev, whose capture
  text is a challenge page … and which this tool prints OK"), reading "capture text" as the text of the capture the
  record names. The sentence is judged as: **for a `.raw` entry, the sibling `.txt` of the one capture path the tool
  binds to that object id (when several capture entries share the id, the binding, not the record's path, decides)**.
  Named limit (i). The lane's tree at F has 14 duplicate-id groups, none with diverging sibling status (measured by the
  seat), so no committed record changes verdict. Remediation (bind `oid -> [paths]` and use the record's own capture
  path when it is among them, or refuse when any sharing entry's sibling is a challenge page) routed to round 101.
- **A6 (C1, `--repo` at a subdirectory).** `R100SentinelC1` F-2: `git ls-tree … -- corpus/captures/` takes the pathspec
  relative to `--repo`'s directory while `rev:path` is root-relative, so `--repo <worktree>/corpus` yields an empty
  capture set and a rev record on S230's challenge capture prints OK (`R100SentinelC1-repo-subdir-evidence.txt`). Every
  lane call site passes the worktree root. The sentence is judged with **`--repo` (or `--root`) naming the worktree
  root**. Named limit (j). Remediation (`--full-name` and `:(top)corpus/captures/`, and a loud error on an empty capture
  set when the tree has `corpus/captures/`) routed to round 101.

The C1 verdict is filed on the A1-A6 sentence. The frozen kill rule's literal text is met by the A5 and A6 artifacts;
the report states this and lets the closure rule.
