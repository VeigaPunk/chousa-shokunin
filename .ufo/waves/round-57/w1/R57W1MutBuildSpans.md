# R57W1MutBuildSpans — mutation probe: tools/build-spans.py (single-edit mutants vs R57-C3 manifest legs)

Scope: scratch copy of lane `tools/build-spans.py` at `1ed2650a…c80bf6` (sha256 = lane HEAD copy,
verified `diff` = byte-identical after every restore). Fixture: S127 capture (`.raw` = `%PDF-1.7`,
`.txt` = 70038-char defined form, sha256 `.txt` `23306b9f…`, `.raw` `51550c5c…`), key
`b27ffd2f0161104c6a28c9f5` = sha256(S127_URL)[:24], copied into scratch cache. Quotes TSVs:
A = two 1x quotes (`规范性引用而构成本文件必不可少的条款` off 4709; `本文件按照GB/T` off 2361);
B = one 0x ghost (`抗肿瘤药物临床应用管理指南`) + CLAUSE; C = one 2x quote (`规范性引用文件`, form
offsets 907 and 4684) + CLAUSE. Detector (same for all phases): builder exit/stderr + `legcheck.py`
re-implementing the frozen `c3-count.py` manifest legs verbatim (IN_SPAN, SHORT, CONTEXT =
`len(span)>len(quote)`, CAPTURE_BOUND = `dg==digest && form[o:o+len(span)]==span`, anchors) plus the
round-51 `quote-substance-check.py` run on the fixture manifest. All runs under
`TMPDIR=/fast/scratch/hyaku/chousa-r57/R57W1MutBuildSpans`, `PYTHONDONTWRITEBYTECODE=1`.

## Baseline (pristine, hash 1ed2650a)

- A: `QUOTE S127 char 4709 …` `SPANS_ROWS=2 WRITTEN=2`, `LEGCHECK=PASS` (all legs 2/2, SUBSTANCE FAILURES=0).
- B: `build-spans: refused S127: quote occurs 0x …` exit 1, nothing written. C: `… occurs 2x …` exit 1.
  The exactly-once guard is a load-bearing refusal, not a warning.

## Mutants (each a single edit; full logs in scratch runs/, deleted at yield)

| mut | edit | sha256 | fixture | build | detector | verdict |
|---|---|---|---|---|---|---|
| M1 | `if n != 1:` → `if n < 0:` | `331a9a26…` | A | rc0, identical output | PASS | equivalent |
|   |   |   | B | rc0, `QUOTE S127 char -1`, manifest offset=0 for a quote absent from the form | IN_SPAN=1/2 → FAIL | **killed** (quote-in-span) |
|   |   |   | C | rc0, `char 907` | all legs 2/2, SUBSTANCE 0 | **SURVIVED** |
| M2 | `CONTEXT = 80` → `4_000_000_000` | `78ed63f8…` | A | rc0, spanlen=70038 (whole form), offset=0 | IN_SPAN/SHORT/CONTEXT/CAPTURE_BOUND all pass; SUBSTANCE `OVERWIDE_SPAN ×2` → FAIL | **killed**, by round-51 floor only |
| M3 | `.txt` branch digest → `sha256(raw.read_bytes())` | `6d536daa…` | A | rc0, manifest pins `51550c5c…` (.raw), not `23306b9f…` (.txt actually read) | CAPTURE_BOUND=0/2 → FAIL | **killed** |
| M4 | span write → `(out.parent / name)` | `b2341ccb…` | A | (a) escape dir absent → FileNotFoundError crash rc1; (b) `spans/` pre-existing at parent → rc0, `spans.tsv` in OUT, span files escaped | IN_SPAN=0/2 CONTEXT=0/2 SPAN_FILE_MISSING → FAIL; `--check` prints `SPANS_FILE_STALE ×2 STALE=2` | **killed** |

Restore evidence: after every mutant `cp` of the pristine copy restored sha256 `1ed2650a…` and
`diff` vs lane original printed byte-identical; final re-run on A is green (`LEGCHECK=PASS`).

## What each mutant would silently break (R57-C3 leg view)

- **M1/0x**: builder exits 0 and writes a manifest row whose `offset`=0 span is a genuine exact
  prefix slice — CAPTURE_BOUND and CONTEXT pass *vacuously*, SUBSTANCE passes (92 ≤ 13+162);
  only IN_SPAN fails (`抗肿瘤…` not in span). Anchor leg: no `char N` exists for the ghost row.
  The leg that carries quote-presence is IN_SPAN alone; slice-exactness does not imply it.
- **M1/2x — coverage finding (survived)**: with uniqueness dropped, a 2x quote builds a fully
  conforming row: anchor `char 907` binds the first occurrence while the second (4684 — inside the
  CLAUSE row's own span) is unrecorded. Frozen `c3-count.py` has no exactly-once leg: `in_span`
  tests membership only, `CAPTURE_BOUND` tests slice equality, `ANCHOR_BOUND` only that recorded
  `char N` is *a* quote offset. Quote uniqueness is enforced solely at build time by
  `build-spans.py`; a non-unique quote in a spans row silently loses its second locus. Reported,
  not patched (C3 frozen).
- **M2**: frozen CONTEXT leg is one-sided (`len(span) > len(quote)`); a whole-capture span
  (offset 0, 70038 chars) passes CONTEXT, IN_SPAN, CAPTURE_BOUND. Only the round-51 floor
  (`span ≤ quote+2·CONTEXT+2`) kills it — the width bound lives in the substance tool, not the
  counter's CONTEXT leg. Reported, not patched.
- **M3**: build prints success while `capture_sha256` silently desyncs to `.raw`. Counter's
  `m[2] == digest-of-file-read` leg is the sole guard; without it BOUND collapses. Also observed:
  on a `.txt`-only capture this mutant is a FileNotFoundError crash, not a clean refusal.
- **M4**: manifest intact, files land outside OUT — kills IN_SPAN/CONTEXT via `SPAN_FILE_MISSING`
  and trips builder `--check` (`STALE=2`). CAPTURE_BOUND passes vacuously on missing spans
  (`form[o:o+0] == ""`): worth noting — the leg never asserts the span file exists. Either a crash
  or a counter-kill; no silent pass.

Verdict matrix: 1 surviving mutant (M1-2x), 3 killed, 1 equivalent-on-input. The surviving path is
the second-occurrence ambiguity — a coverage gap in the frozen legs, not a builder defect to patch.

Scratch `/fast/scratch/hyaku/chousa-r57/R57W1MutBuildSpans/` deleted before yield; no lane or
fleet writes outside this report; no network. Tools installed: none (pacman paused; none needed).

VERDICT: mutated build-spans.py scratch copy (4 single-edit mutants, pristine→mutant→restored);
M1's 2-occurrence path SURVIVES every frozen c3-count manifest leg — exactly-once is build-time
only; M1-0x killed by IN_SPAN, M2 killed only by the round-51 substance floor, M3 killed by
CAPTURE_BOUND, M4 killed/crashed; pristine restored byte-identical (sha256 `1ed2650a…`).
