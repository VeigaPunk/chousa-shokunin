# R95ExecC2Repro — frozen C2 reproduction from clean tree

Attacked tree: carrier C `d27e9891ba6d2bae8b1f6060f7c01bf13a1a6ea1` cloned to
`/fast/scratch/hyaku/chousa-r95/R95ExecC2Repro/repo` (verified HEAD). All commands below run from that clone root.

## (a) Three C2 counting commands vs committed `corpus/evidence/round95/after/c2-*.txt`

### 1. `python3 -B tools/gate-records.py verify --root . corpus/knowledge/search-rerun-record-r95.md`

Command (cwd = clone root):
`python3 -B tools/gate-records.py verify --root . corpus/knowledge/search-rerun-record-r95.md > work1/c2-gate-rerun.txt 2>&1`
Observed: exit 0, output

```
GATE_RECORD corpus/knowledge/search-rerun-record-r95.md:63 S222 OK
GATE_RECORD corpus/knowledge/search-rerun-record-r95.md:64 S222 OK
GATE_RECORD corpus/knowledge/search-rerun-record-r95.md:65 S222 OK
GATE_RECORD corpus/knowledge/search-rerun-record-r95.md:66 S222 OK
GATE_RECORD corpus/knowledge/search-rerun-record-r95.md:67 S222 OK
GATE_RECORD corpus/knowledge/search-rerun-record-r95.md:68 S222 OK
GATE_RECORD corpus/knowledge/search-rerun-record-r95.md:69 S222 OK
GATE_RECORD corpus/knowledge/search-rerun-record-r95.md:70 S222 OK
GATE_RECORD corpus/knowledge/search-rerun-record-r95.md:71 S222 OK
GATE_RECORDS files=1 records=9 ok=9 fail=0
```

Receipt: `.ufo/waves/round-95/w1/R95ExecC2Repro-c2-gate-rerun.txt`
Diff vs `corpus/evidence/round95/after/c2-gate.txt`: identical body after stripping the volatile `# computed_against` / `# command` / `# measured_at` / `# exit=0` header lines (see §Evidence). Matches claim predicate (`GATE_RECORDS files=1 records=9 ok=9 fail=0`, exit 0).

### 2. `bash tools/research-gate.sh verify-metadata corpus/knowledge/search-rerun-record-r95.md --root .`

Command: `bash tools/research-gate.sh verify-metadata corpus/knowledge/search-rerun-record-r95.md --root . > work1/c2-metadata-rerun.txt 2>&1`
Observed: exit 0,

```
research-gate v2 — ts=2026-11-08T23:07:04Z — mode=verify-metadata — path=corpus/knowledge/search-rerun-record-r95.md — root=.
META entry=search-rerun-record-r95.md source=present verified_at=dated recheck=scheduled verdict=clean
METADATA_COMPLETE=1/1
RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)
```

Receipt: `.ufo/waves/round-95/w1/R95ExecC2Repro-c2-metadata-rerun.txt`
Diff vs `after/c2-metadata.txt`: identical modulo the `ts=` timestamp. Matches claim predicate (exit 0, CLEAN).

### 3. `python3 -B corpus/evidence/round95/entry-controls-r95.py --root . --work <scratch>`

Command: `python3 -B corpus/evidence/round95/entry-controls-r95.py --root . --work work1 > work1/c2-controls-rerun.txt 2>&1`
Observed: exit 0,

```
CASE positive gate_rc=0 meta_rc=0 LQ_BOUND=9/9 records=9 WARRANTS_OK=7/7 ok
CASE g1-word rc=1 expect=1 fail=['QUOTE_ABSENT'] want=QUOTE_ABSENT ok
CASE g2-column-join rc=1 expect=1 fail=['QUOTE_ABSENT'] want=QUOTE_ABSENT ok
CASE g3-capture-key rc=1 expect=1 fail=['CAPTURE_KEY,CAPTURE_SHA,QUOTE_ABSENT,REFETCH'] want=CAPTURE_KEY ok
CASE g4-words rc=1 expect=1 fail=['WORDS'] want=WORDS ok
CASE g5-tier rc=1 expect=1 fail=['TIER'] want=TIER ok
CASE g6-fetched rc=1 expect=1 fail=['REFETCH'] want=REFETCH ok
CASE g7-long rc=1 expect=1 fail=['QUOTE_LEN'] want=QUOTE_LEN ok
CASE g8-sourceless rc=1 expect=1 records=0 ok
CASE do-nothing-base entry_at_base=absent gate_rc=2 expect=2 ok
POSITIVE=1/1 FORGERY_REFUSED=8/8 DO_NOTHING_REFUSED=1/1 GATE_RECORDS=9/9 LQ_BOUND=9/9 WARRANTS_OK=7/7 METADATA=clean
ENTRY_CONTROLS=PASS
```

Receipt: `.ufo/waves/round-95/w1/R95ExecC2Repro-c2-controls-rerun.txt`
Diff vs `after/c2-controls.txt`: identical body (`diff` clean after stripping `#` header). Matches claim predicate.

Verdict on (a): all three reproduce exactly. No deviation.

## (b) Independent recount of the 9 GATE-RECORD quotes (no `gate-records.py` import)

Script: `.ufo/waves/round-95/w1/R95ExecC2Repro-independent-census.py` (10-line normaliser mirroring
`tools/gate-records.py:92-94` — U+2018/19→', U+201C/22→", `" ".join(s.split())` — but counting on its own).
Output receipt: `.ufo/waves/round-95/w1/R95ExecC2Repro-independent-census.txt`

Command: `python3 -B work1/independent_census.py corpus/captures/1a8c36c4c24444967bd9c3ce.txt corpus/knowledge/search-rerun-record-r95.md`

Observed (abridged):

```
records_extracted=9 full_norm_chars=122212
Q1 entry_line=63 words=16 count_full=1 line_hits=[] quote='Include the search strategies…'
Q2 entry_line=64 words=12 count_full=1 line_hits=[] …
Q3 entry_line=65 words=14 count_full=1 line_hits=[] …
Q4 entry_line=66 words=13 count_full=1 line_hits=[] …
Q5 entry_line=67 words=12 count_full=1 line_hits=[270] …
Q6 entry_line=68 words=11 count_full=1 line_hits=[843] …
Q7 entry_line=69 words=9  count_full=1 line_hits=[943] …
Q8 entry_line=70 words=9  count_full=1 line_hits=[947] …
Q9 entry_line=71 words=10 count_full=1 line_hits=[949] …
Q7Q8Q9_joint joint_in_full=False joint_count=0
```

Each quote occurs exactly once in the whole normalised capture. Q1–Q4 span a line break in the `-layout` text
(they wrap within a column), so no single raw line contains them; Q5–Q9 sit on one raw line each (lines 270,
843, 943, 947, 949) — consistent with the entry's "single column-line fragment" claim for Q6–Q9. Word counts
match the `words=` fields of the GATE-RECORD lines.

## (c) Capture re-derivation and the Q7–Q9 one-sentence question

Tools: `pdftotext` 26.10.0 (Poppler) at `/usr/bin/pdftotext`.

Commands:

```
pdftotext -layout corpus/captures/1a8c36c4c24444967bd9c3ce.raw work1/regen-layout.txt
sha256sum work1/regen-layout.txt corpus/captures/1a8c36c4c24444967bd9c3ce.txt
pdftotext corpus/captures/1a8c36c4c24444967bd9c3ce.raw work1/regen-nolayout.txt
```

Observed:

- `regen-layout.txt` sha256 = `86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871`, byte-identical (`cmp` exit 0) to the committed `corpus/captures/1a8c36c4c24444967bd9c3ce.txt`. That is also the `txt_sha256` on the S222 JMLA row of `corpus/evidence/round57/refetch.tsv` (and the `capture_sha256` in each GATE-RECORD line). Receipts: `.ufo/waves/round-95/w1/R95ExecC2Repro-regen-layout.txt`.
- `regen-nolayout.txt` sha256 = `6f33fffdcc70367dc043055ee87d052f74e0c6364025f55c47bd26d2d7537184` (different, as expected without `-layout`). Receipt: `.ufo/waves/round-95/w1/R95ExecC2Repro-regen-nolayout.txt`.
- Normalised-contiguity probe (same normaliser as gate-records) over the three texts:
  - Each of Q7, Q8, Q9 occurs once in all three texts (layout, nolayout, committed), so location is not in dispute.
  - The joint string `"If a reader tries to duplicate a search from drastically different number … both"` occurs **0 times** in all three texts (as it must in `-layout`, where the columns interleave; see below).
  - In **nolayout**, the source paragraph is two sentences, each contiguous:
    1. `"If a reader tries to duplicate a search from a systematic review, one would expect to retrieve nearly the same results when limiting to the timeframe in the original review."` — contains Q7, does not contain Q8/Q9.
    2. `"If instead, the searcher locates a drastically different number of results than reported in the original review, this can be indicative of errors in the published search [22] or major changes to a database, both of which might be reasons to update a systematic review or view the systematic review's results with skepticism."` — contains Q8 and Q9, does not contain Q7.
    - Boundary check: `s1 end 59807 … s2 start 59824` — the two sentences are adjacent, separated by one space; Q7 belongs to sentence 1, Q8+Q9 to sentence 2.

### FINDING F1 (against the entry's named limit and the claim's named limit (a))

The entry states (`corpus/knowledge/search-rerun-record-r95.md:22-24` and the `Named limits` bullet at line 59):
"that Q7-Q9 belong to one ITEM 15 sentence is read from the PDF's layout, not located" / "Q7-Q9 are three
located fragments of one sentence". The frozen claim's named limit (a) repeats it: "that Q7–Q9 form one
sentence is read from layout" (`claims.md:63-64`).

The nolayout text form **refutes** that reading: Q7 belongs to a first sentence about expecting "nearly the same
results", and Q8+Q9 belong to a second, separate sentence ("If instead, …"). They are two sentences, not one.
The entry's own decision rows already treat them that way in effect — row 5 ("Re-running a recorded search",
warrant `Q7, Q8`) draws on the "nearly the same results" content of sentence 1 + the "drastically different"
content of sentence 2, and row 6 ("Reading a different re-run count", warrant `Q9, Q8`) draws on sentence 2
alone — but the entry's prose claims a single sentence, which is false as stated. This is squarely the kind of
overstatement the lane's K2 targets ("a Do/Never cell asserting what its warranting quote(s) do not say") and that
the claim's sentence relies on for warranting 7 decision rows from 9 quotes: an adversary reading only the
committed evidence would conclude Q7–Q9 are one sentence because the entry says so, whereas the source says two.

Note what is *not* false: each of Q7, Q8, Q9 is individually located (count 1 each, §b), the joined
Q7+Q8+Q9 string appears nowhere, and no single quote is located by joining across columns. The falsity is in
the "one sentence" joining assertion, which the lane says it "reads from layout" — but layout (`-layout` output
at lines 943–949, verified in §c) also shows the sentence break: Q7's line ends `"… duplicate a search from"`
followed by `"a systematic review, one would expect…"` (sentence 1) and line 947's `"original review. If
instead, the searcher locates a"` begins sentence 2. Even on the layout text, a careful reader can see the
period boundary; the lane's reading simply got it wrong.

Corrected treatment (for L1 to apply; this seat writes no production files): the "one sentence" sentence in the
entry's `Named limits` and `Text form` paragraph should read "Q7 is sentence 1; Q8–Q9 are sentence 2" (two
ITEM 15 sentences), and decision rows 5–6's warrants re-examined — row 5's warrant `Q7, Q8` spans the two
sentences, which is fine as a two-sentence warrant but not as a one-sentence warrant.

## (d) S222 registry row columns and census validate

- The seat asked for "11 columns". The registry is `corpus/SOURCES.md` (not `refetch.tsv`). S222 is at line 234:
  `| S222 | Rethlefsen ML, … | paper | A | what the PRISMA-S checklist … | Table 1 checklist items 8, 9, 12, 13… | … | mined | 2026-11-08 | on-release | corpus/knowledge/search-rerun-record-r95.md |`
  Splitting on `|` gives 13 fields because of the leading/trailing empty fields from the outer pipes; the
  content cells are 11 (id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by) —
  exactly what `tools/gate-records.py:166-168` (`load_registry`: `len(cells) != 11: continue`) counts. `gate-records.py verify` itself passed with S222 OK on all 9 records ( §a.1 ), which independently proves the loader accepted that row as 11-column. No finding here; just a terminology note on how the 11 is counted.
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` (read-only): output lists 5 pre-existing W04 duplicate-url warnings (S051, S053, S073, S074, S075 — none is S222) then `chousa ok /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md`. Exit code 0. Matches the seat's expected outcome.

## Secondary checks done in passing

- Item numbers in the entry's decision rows (`Q1=item 8, Q5=item 9, Q2=item 13, Q3=item 15, Q4=item 12`) verified against `regen-nolayout.txt`: "Full search strategies / 8" (l.393), "Limits and restrictions / 9" (l.398), "Updates / 12" (l.437), "Dates of searches / 13" (l.448), "Total records / 15" (l.456), and the body heads `ITEM 8` (l.919), `ITEM 9` (l.1029), `ITEM 12` (l.1202), `ITEM 13` (l.1271), `ITEM 15` (l.1367) all agree. `WARRANTS_OK` in the controls only checks that each row names ≥1 existing qid; it does not check entailment of the Do/Never paraphrase — that is the claim's named limit (b) ("the wave's reviewer item"), so no finding against the instrument, but it means a paraphrase error like F1 would not be caught by the battery; F1's falsity is in the entry's prose, visible only to a human reader of the source.
- Q5's quote truncates the source sentence without the period (`"… restrictions"` vs source `"… restrictions applied to a search (e.g. …)"`); gate-records only requires the quote's normalised form to occur, so this is not a location failure.
- Q6 (`"to view the same "slice" of the database that the original"`) is attributed to S222 generally; it occurs in the ITEM 13 explanation (l.1290 in nolayout), which is consistent with the entry's hedging, not a falsity.

## Evidence

- `.ufo/waves/round-95/w1/R95ExecC2Repro-c2-gate-rerun.txt` — rerun of gate-records verify (exit 0)
- `.ufo/waves/round-95/w1/R95ExecC2Repro-c2-metadata-rerun.txt` — rerun of research-gate verify-metadata (exit 0)
- `.ufo/waves/round-95/w1/R95ExecC2Repro-c2-controls-rerun.txt` — rerun of entry-controls (exit 0, `ENTRY_CONTROLS=PASS`)
- `.ufo/waves/round-95/w1/R95ExecC2Repro-independent-census.py` — independent 10-line recount script (no gate-records import)
- `.ufo/waves/round-95/w1/R95ExecC2Repro-independent-census.txt` — output: 9/9 quotes count=1, word counts match
- `.ufo/waves/round-95/w1/R95ExecC2Repro-regen-layout.txt` — `pdftotext -layout` re-derivation, sha256 `86f1aacd…`, byte-identical to committed capture
- `.ufo/waves/round-95/w1/R95ExecC2Repro-regen-nolayout.txt` — `pdftotext` without `-layout`, sha256 `6f33fffd…`, contains the two full ITEM 15 sentences contiguous
- Source lines cited: entry `corpus/knowledge/search-rerun-record-r95.md:22-24, 48-49, 59`; claim `claims.md:63-64`.

## Findings summary

1. **F1 (falsity, in entry + claim named limit (a))**: Q7–Q9 are not one sentence. Nolayout text shows Q7 ∈ sentence 1 ("If a reader tries to duplicate a search from a systematic review, …") while Q8+Q9 ∈ sentence 2 ("If instead, … both …"). The entry's `Named limits` and `Text form` statements that they form one sentence are false as stated, and the claim's named limit (a) repeats the falsity. All predicate counts (records=9, LQ_BOUND=9/9, WARRANTS_OK=7/7) still reproduce, so the instruments are not wrong — the entry's prose sentence is.
2. No other deviation found. (a) all three counting commands reproduce the committed receipts (modulo volatile header/timestamp). (b) all 9 quotes locate exactly once under independent normalisation. (c) capture byte-derivation holds; refetch `txt_sha256` agrees. (d) S222 registry row is 11 content columns as gate-records counts; census validate exits 0 (only pre-existing W04 warnings).

VERDICT: R95ExecC2Repro C2 fired — entry and claim describe Q7–Q9 as one sentence; the source has two.
