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
