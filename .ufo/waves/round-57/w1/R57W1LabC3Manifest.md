# R57W1LabC3Manifest — c3 manifest leg boundaries, pinned by synthetic states

Seat: R57W1LabC3Manifest (leaf labrat; no dispatch). Claim probed: **R57-C3** (frozen, `fd95724`), manifest legs only — no predicate, target, counter, control or recipe touched. Counter `corpus/evidence/round57/c3-count.py` sha256 `c565ce4a78b439411dc6e088bc5f8a92781888fe895f2ee9b43170867c1e6e33`, byte-identical in the lane and in my scratch clone; never edited. Every run used the copy's own `--root`, so only fixture state changed. No network, no install, no pacman (paused); nothing written outside this report and my scratch.

## Setup
```
$ git clone <lane> $S/lane ; git -C $S/lane rev-parse --show-toplevel
/fast/scratch/hyaku/chousa-r57/R57W1LabC3Manifest/lane
$ sha256sum $S/lane/corpus/evidence/round57/c3-count.py <lane>/corpus/evidence/round57/c3-count.py
c565ce4a…1e6e33  both paths  (identical)
```
`LANE` resolves from the counter's own path (git BASE_REV lookups, `tools/capture-text.py`, the round-51 substance check); data comes from `--root`. The clone carries BASE_REV, so only fixture state varies per case. Baseline fixture: 4 rows, each span `form[offset:offset+len(span)]` with `len(span) = len(quote)+160` (the round-51 builder's ±80).
```
$ python3 $S/lane/.../c3-count.py --root $S/fx/baseline
QUOTE_ROWS=4 IN_SPAN=4 IN_ENTRY=4 IN_LESSON=4 SHORT=4 CONTEXT=4 CAPTURE_BOUND=4
SUBSTANCE=PASS ANCHOR_BOUND=0/0 INFERENCE_GROUNDED=no STRAY_IDS=-
```
## The four assigned legs

**(1) `capture_sha256` must be the digest of the form READ — else CAPTURE_BOUND fails.** Span is the exact slice of the `.txt` at the recorded offset, but the manifest pins the *other* form's digest:
```
c1_stale_digest     → QUOTE_ROWS=4 IN_SPAN=4 IN_ENTRY=4 IN_LESSON=4 SHORT=4 CONTEXT=4 CAPTURE_BOUND=3  ← fails
c1b_offset_shift    → … CAPTURE_BOUND=3   (digest right, offset+1: slice conjunct fails)
c1c_span_middle_cut → QUOTE_ROWS=4 IN_SPAN=3 … CAPTURE_BOUND=3  (one middle char deleted)
```
Same on the real S127 capture (`b27ffd2f0161104c6a28c9f5`) with the clause quote:
```
txt_digest 23306b9f… → … CAPTURE_BOUND=1     raw_digest 51550c5c… → … CAPTURE_BOUND=0
raw_digest + offset on the raw-decoded form  → … CAPTURE_BOUND=0
```
**(2) quote in the span but not in the entry → IN_ENTRY fails** (`S904`'s quote removed from the entry only):
```
c2_not_in_entry   → QUOTE_ROWS=4 IN_SPAN=4 IN_ENTRY=3 IN_LESSON=4 SHORT=4 CONTEXT=4 CAPTURE_BOUND=4
c7_not_in_lesson  → … IN_LESSON=3 …   (same quote dropped from corpus/lessons/round-57.md)
```
**(3) SHORT = `len(quote.split()) <= 25 and len(quote) <= 160`** (chars, not bytes):
```
25 words / 160 chars   (baseline S901) → SHORT=4/4   ← boundary PASSES
26 words / 160 chars   (c3a_26words)   → SHORT=3/4   ← word leg fails
25 words / 161 chars   (c3b_161chars)  → SHORT=3/4   ← char leg fails
CJK 160 chars / 1 word (c3c_cjk160)    → SHORT=5/5   ← passes
CJK 161 chars / 1 word (c3d_cjk161)    → SHORT=4/5   ← fails
```
For Chinese quotes `split()` yields ~1 token, so the **160-character limit is the only binding one**.

**(4) offset non-numeric → CONTEXT fails, and CAPTURE_BOUND with it:**
```
c4_nonnumeric_offset → QUOTE_ROWS=4 IN_SPAN=4 IN_ENTRY=4 IN_LESSON=4 SHORT=4 CONTEXT=3 CAPTURE_BOUND=3
```
`c3-count.py:253-257`: `ctx += offset.isdigit() and len(span) > len(quote)`, and the `cap` branch is itself gated by `offset.isdigit()`. `c5_span_eq_quote` (`span == quote` exactly) → `IN_SPAN=4 CONTEXT=3 CAPTURE_BOUND=3`: the span must be strictly *longer* than the quote. Adjacent legs: `c6_span_overwide` (`span = quote+200`) → `SUBSTANCE=FAIL CAPTURE_BOUND=3` (round-51 floor `len(span) <= len(quote)+162`); `c9_malformed_row` (a 4-cell extra row) → `QUOTE_ROWS=5` against `IN_SPAN/IN_ENTRY/IN_LESSON/SHORT/CONTEXT/CAPTURE_BOUND=4` and `SUBSTANCE=FAIL` (every counter must equal the row count); `c8_stray_id` → `STRAY_IDS=S999`.

## Form/digest conventions, measured on committed captures
```
S127 .txt 23306b9f… / .raw 51550c5c…   PDF  → digest = .txt, offsets in the newline-normalized text
S121 .txt ed4dde2e…  877 CRLF, form 3599 chars from 6650 bytes
     bytes-digest + normalized offset → CAPTURE_BOUND=1
     normalized-text digest           → CAPTURE_BOUND=0
     byte offset (pre-normalization)  → CAPTURE_BOUND=0
S115 .raw 16fc8c55…  PK zip .docx → form = capture-text.py at BASE_REV, digest = .raw → CAPTURE_BOUND=1
S124 .raw ac0fad62…  OLE .doc     → form = capture-text.py,           digest = .raw → CAPTURE_BOUND=1 (.txt digest → 0)
```
**PDF/HTML → digest over the `.txt` BYTES, offset into the normalized text; OLE/zip → digest over the `.raw`, offset into the capture-text form.** Independently, the candidate gate (`good_raw`, `c3-count.py:188`) compares `refetch.tsv` `raw_sha256` against the `.raw`, so a bound row carries **two** digests: the manifest's form digest and the refetch raw.

## Binding, anchor, sweep (real bytes)
```
held S118 + R7 rows, manifest digest = .txt 927ff71c… → BOUND=1/7 (R7:S118)
same rows with the .raw digest 7b600fe3…              → BOUND=0/7 and CAPTURE_BOUND=0
```
`per_id` requires `m[2] == cand[rid][2]` — the *form* digest — so the wrong digest costs the binding too. Anchor (`char N` = `offset + span.find(quote)`): `char 136` → `ANCHOR_BOUND=1/1`; `char 135` → `0/1`; `char X` → `0/1`; `char 136, char 160` → `0/1`; `char 136, char 163` → `1/1`. Sweep: `- UNBOUND R1 sweep: abc` → `SWEPT=0/6`; well-formed `R1` → `1/6`; `R9` → `0/6` (the tag is matched, not the prose).

## Registry/manifest consistency facts (found wiring the live manifest; nothing patched)
1. Registry rows must lie **inside `## Registry`** — `registry()` closes at the next heading. Three rows appended at EOF parsed as 0 rows (`BOUND=1/7 STRAY_IDS=S131,S132,S133`); moved above `## Paths`, they bind.
2. The URL must be **byte-identical** in the manifest row, the registry's first source-cell URL and the entry's `source: X — U` line. An `http://` registry URL against an `https://` manifest/entry URL dropped R1 (`BOUND=3/7`) because `first_url()` also selects the capture key `sha256(url)[:24]`.
3. The manifest's 7th column (`entry`) is read by neither `c3-count.py` nor `quote-substance-check.py`; the entry path is carried by the registry `used-by` cell and the `source:` line.

## Ceiling against the current store
Scanning all 63 captures with a successful refetch row and a matching `.raw`, using the counter's own `REFS`/`heading_title`/`nows`: R1, R2, R3, R7 each have **token ∧ heading** candidates; R4/R5/R6 have token-only candidates. Their only title lines are numbered list items — ` 2.抗肿瘤药品临床综合评价技术指南（2022年版 试行） ` → `nows` prefix `2.`, and `BAD_PREFIX` contains `.`, so `heading_title` is False. **The reachable BOUND is exactly 4 = MIN_BOUND**, and the other three need sweep lines (the live entry carries them). Live lane at measurement (`corpus/evidence/round57/c3/spans.tsv` sha256 `c10e1406f9257a0e…19b088b`):
```
ENTRY=yes S127_CITED=yes NEW_GROUND=yes CLAUSE=yes
BOUND=4/7 (min 4) R1:S131 R2:S132 R3:S133 R7:S118
SWEPT=3/3 R4 R5 R6
QUOTE_ROWS=10 IN_SPAN=10 IN_ENTRY=10 IN_LESSON=0 SHORT=10 CONTEXT=10 CAPTURE_BOUND=10
SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=no STRAY_IDS=-
C3=FAIL
```
Every manifest leg pinned here is green 10/10 on the landed manifest, and its manifest-derived quote offsets (S127 4709/4794, S131 271/352, S132 68/1036, S133 19/54, S118 3334/78) equal the `char N` figures the entry states. The two failing legs are outside this seat: `IN_LESSON=0` (`corpus/lessons/round-57.md` absent) and `INFERENCE_GROUNDED=no` (live `tools/inference-ground.py` → `rc=1`, `FINDING INF_TOKEN_NOT_IN_SPAN bullet=3 token='2022'`).

## Risks and limits
- Synthetic fixtures pin leg *arithmetic*, not entailment: green CAPTURE_BOUND says bytes and offsets agree, not that the quote supports the sentence (the freeze's own disclosed limit).
- The heading rule is a shape test: a numbered list item can never bind, nor can a copy whose cover typesets the title across lines — measured for R4/R5/R6 above.
- `SUBSTANCE` reuses the round-51 checker from the clone, so fixtures inherit its 3-char / 12-char / quote+162 floors.
- Snapshot-based: the lane moved during the run (entry and registry rows landed while I probed); the numbers are from the sha256'd manifest, not a later state.
- No `pacman`/install and no network fetch; the only capture bytes read are committed ones under `corpus/captures/`.
- Scratch `/fast/scratch/hyaku/chousa-r57/R57W1LabC3Manifest/` was removed before yielding (`trap 'rm -rf -- "$S"' EXIT`).

VERDICT: attacked the R57-C3 manifest legs with synthetic states and real committed captures — all four assigned boundaries survive as specified (wrong-form digest kills CAPTURE_BOUND; a quote missing from the entry kills IN_ENTRY; 25 words/160 chars passes while 26 words or 161 chars fails; a non-numeric offset kills CONTEXT and CAPTURE_BOUND), and the landed 10-row lane manifest satisfies every one of them 10/10.
