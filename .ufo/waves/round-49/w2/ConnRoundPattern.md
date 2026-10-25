# ConnRoundPattern — W2 cross-claim / cross-round pattern scan (r47-C3, r46-C3)

Seat: ConnRoundPattern (leaf; no subagents/jobs). Skill: godspeed. Read `~/.omp/agent/RULES.md`; no install (no tool needed). Scratch `/dev/shm/chousa-r49-ConnRoundPattern/` created, used, and removed; `TMPDIR` pointed there for counter runs. Read-only on lane and fleet; only write is this report.

## Item attacked

W1 defect classes found against the round-49 C2 counter — (a) hollow-quote passes (CritForgeC2), (b) CR universal-newline mismatch on UTF-16LE `.raw` forms (MutSpans F0 / claims-erratum), (c) staged-id collisions resolving to the wrong document (ReviewToolCode F1), (d) replay passes fixed-input counters (claims-erratum) — tested for applicability to the older span-binding counters round-47 C3 and round-46 C3. (a) and (b) tested empirically on scratch roots; (c)/(d) by W1 evidence plus lane registry scans.

## Fixtures

Replicated the W1 minimal-PASS shape for the older counters on scratch roots: real r47/r46 entries copied verbatim (source lines, `#### Inference` bullets unchanged), 11-cell `## Registry` rows, spans.tsv + span files built from real qcache captures (`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`), real `tools/inference-ground.py` copied for the r47 subprocess leg. All counters run with `--root <scratch>` (C3 does not read lane git).

## Commands and observed output

1. Hollow-quote fixture, round-47 C3 (quotes = single space, spans = whole `.txt` capture at offset 0, anchors = first-space offset, lesson verdict lines = `register S093/S094/S108/S110 verdict: present`):

```
$ python3 <lane>/corpus/evidence/round47/c3-count.py --root /dev/shm/chousa-r49-ConnRoundPattern/r47-A
ENTRIES=2/2 | CITES_BOUND=6/6 | QUOTE_ROWS=12 (min 12) | SPAN_IDS=6/6
QUOTES_IN_SPAN=12/12 | QUOTES_IN_ENTRY=12/12 | SPAN_CONTEXT=12/12
CAPTURE_BOUND=12/12 | REF_ID_UNBOUND=0 | ANCHOR_BOUND=6/6
INFERENCE_GROUNDED=2/2 | QUARANTINE_VERDICTS=4/4 | QUARANTINE_ABSENT_ADOPTED=0
C3=PASS | exit=0
```

2. CR/newline-mismatch immunity, round-47 C3 (span files written with every LF replaced by CRLF — raw-form byte shape — against LF-only `.txt` captures):

```
$ python3 <lane>/corpus/evidence/round47/c3-count.py --root /dev/shm/chousa-r49-ConnRoundPattern/r47-B1
... CAPTURE_BOUND=12/12 ... C3=PASS | exit=0
```

3. Raw UTF-16LE-derived spans (real `.raw` bytes decoded `utf-16le` @0, sliced) vs `.txt` captures, round-47 C3:

```
$ python3 <lane>/corpus/evidence/round47/c3-count.py --root /dev/shm/chousa-r49-ConnRoundPattern/r47-B2
QUOTES_IN_SPAN=6/12 | QUOTES_IN_ENTRY=12/12 | SPAN_CONTEXT=6/12
CAPTURE_BOUND=0/12 | ANCHOR_BOUND=0/6 | INFERENCE_GROUNDED=0/2
C3=FAIL | exit=1
```

4. Hollow-quote fixture, round-46 C3 (11 whole-capture spans, space quotes):

```
$ python3 <lane>/corpus/evidence/round46/c3-count.py --root /dev/shm/chousa-r49-ConnRoundPattern/r46-C
ENTRIES=2/2 | CITES_BOUND=5/5 | QUOTE_ROWS=11/11 | QUOTES_IN_SPAN=11/11
QUOTES_IN_ENTRY=11/11 | CAPTURE_BOUND=11/11 | SPAN_IDS=5/5 | SPAN_CONTEXT=11/11
REF_ID_UNBOUND=0 | REF_BOUND=2/2 | C3=PASS | exit=0
```

5. Real after-states re-run (read-only, lane defaults): round-47 C3 `QUOTE_ROWS=35 ... CAPTURE_BOUND=35/35 ... C3=PASS exit=0`; round-46 C3 `QUOTE_ROWS=11/11 ... CAPTURE_BOUND=11/11 ... C3=PASS exit=0`.

6. Registry scan (`corpus/SOURCES.md`): 103 rows, ids unique (max S103, no duplicate id); normalized-URL duplicates exist only outside legacy block (cochrane S019/S029, w3 S020/S033, pubmed S021/S032, S022/S030, schema.org S024/S031, w3-html52 S050/S051, socket S052/S053, hashlib S059/S074, coreutils S071/S073/S075); legacy S079–S095: 17 rows, all unique, all 11-cell/`mined`/non-empty `used-by`.

## Findings

- **Hollow-quote class applies to both older counters.** r47-C3 and r46-C3 print C3=PASS with single-space quotes over whole-capture spans (tests 1, 4) — the same blind spot as C2. The older *measurements* are unaffected in fact: real quotes are substantive multi-word sentences (e.g. `spans.tsv:2` S090 "greater reason to believe that c is true, all else equal"; `:8` S091 "Each claim in CFEVER is labeled as “Supports”,"), and real spans pass CAPTURE_BOUND. The defect is the counters' capability, not the artifact.
- **CR/newline class does not apply to the older counters.** r47-C3 and r46-C3 bind capture `.txt` only (`c3-count.py` r47:150 `cache / f"{key(url)}.txt"`; r46:131 identical), reading both capture and span file through `Path.read_text` (universal newlines on both sides). Byte-level CRLF differences are erased, so a raw-shaped span with CRLF still passes (test 2). A raw UTF-16LE-derived span fails honestly (test 3: CAPTURE_BOUND=0/12, C3=FAIL) — never a false pass. Their builders never select `.raw` (r47 `build-spans.py:83-89` reads `.txt` only; r46 same), and all six r47 + five r46 captures are LF-only with zero CRLF/bare-CR/FFFD (measured bytes). The r49 failure mode (form decoded untranslated vs span read translated) cannot arise where no form fallback exists.
- **Staged-id collisions do not affect older measurements.** The class materialized this round because the working registry moved mid-adoption (ReviewToolCode F1: stale adopt/scratch renumber S096–S104 vs landed S096–S103). Older C3 counters bind id↔URL by exact strings (`cites` regex + `url in row[1]`; r47 `:120-122`), so any wrong-document resolution would fail CITES_BOUND, not silently pass; post-adoption censuses were clean (round-47/46 `measure-after.txt` show no E03/E04, only pre-existing W04 duplicate-url warnings outside the legacy block), and the legacy block is collision-free today (test 6).
- **Replay-of-fixed-inputs applies to C1-style conformance counters in all three rounds** (claims-erratum: C1 "is a conformance check on fixed inputs"; r46/r47 c1 outputs share the TOOL=present/POSITIVE_PASS/JUNK_KILLED shape), but is not a C3 failure mode: the span-binding counters are deterministic state checks and reproduce (test 5).

## Cleanup and bounds

Scratch removed (`rm -rf /dev/shm/chousa-r49-ConnRoundPattern` → verified absent, `/dev/shm` 1% used). No inst, no network, no production file written.

VERDICT: hollow-quote passes — holds (applies to round-47 and round-46 C3, both reproduce C3=PASS on space-quote whole-capture-span fixtures; real measurements are substantive and unaffected); CR universal-newline mismatch — fails to apply (older counters read `.txt` on both sides, so newline differences are erased and raw spans fail honestly); staged-id collisions — fails to apply (older exact-string bindings and clean censuses exclude it); replay passes fixed-input counters — holds only for C1-style conformance counters in all rounds, not for C3.
