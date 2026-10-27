# R57W2CritC3Forge — forge C3=PASS without genuine documents (residual W2 vs C3 @ `1c9626ef`, freeze `fd95724`)

Fixture: `git clone --shared <lane> lane` → `git checkout 1c9626ef`; mutations inside the clone only; TMPDIR/PYTHONDONTWRITEBYTECODE exported; no fetch, no lane writes, counter never edited.

Baseline (pristine clone):
```
$ python3 corpus/evidence/round57/c3-count.py
BOUND=4/7 (min 4) R1:S131 R2:S132 R3:S133 R7:S118
SWEPT=3/3 R4 R5 R6
QUOTE_ROWS=10 IN_SPAN=10 IN_ENTRY=10 IN_LESSON=10 SHORT=10 CONTEXT=10 CAPTURE_BOUND=10
SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=yes STRAY_IDS=-
C3=PASS   EXIT=0
```

## FALSIFIER — attack 1: `good_raw[(id,url)]` does NOT block replay; both variants reach C3=PASS

`c3-count.py:183-188` builds `good_raw` from `refetch.tsv` alone and `:213` only checks
`good_raw[(rid,url)] == sha256(.raw bytes)`. A fabricated success record plus a byte-copied capture
re-homed under `key(new-url)` therefore satisfies the "successful attempt" clause with no fetch and
no byte provenance. `form_of` reads the attacker-placed `.txt` (`:145-147`); nothing ties `.txt` to `.raw` either.

### A1a — same id S118, different URL `https://mirror.invalid.example/r57/replayed-quality-guideline-2024.pdf`

Staged: second `| S118 |` registry row (URL=U2, `used-by` names entry); fabricated refetch line
`S118  U2  79224cb582cb2ae8c2e3b901  1  2026-10-27T09:12:00Z  0  200  7b600fe3…  927ff71c…`
(sha256s of the copied files); `cp` of `16fe8487….raw/.txt` → `79224cb5….raw/.txt`; entry `source:` URL → U2;
manifest `url` cells → U2 (digest column unchanged: it is the `.txt` sha, same bytes).

```
$ python3 corpus/evidence/round57/c3-count.py
BOUND=4/7 (min 4) R1:S131 R2:S132 R3:S133 R7:S118
SWEPT=3/3 R4 R5 R6
QUOTE_ROWS=10 IN_SPAN=10 IN_ENTRY=10 IN_LESSON=10 SHORT=10 CONTEXT=10 CAPTURE_BOUND=10
SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=yes STRAY_IDS=-
C3=PASS   EXIT=0
```
Output byte-identical to baseline except R7 now rests on a URL no fetch ever touched; the refetch
key column is unused and attempt/time arbitrary (the record needs only 9 columns, rc=0, HTTP 2xx,
and raw_sha256 != "-").

### A1b — different id S135 AND different URL (literal seat attack)

Same replay via a fresh S135 row, manifest ids S118→S135, entry tokens S118→S135, anchors char 3334/78.

```
$ python3 corpus/evidence/round57/c3-count.py
BOUND=4/7 (min 4) R1:S131 R2:S132 R3:S133 R7:S135
SWEPT=3/3 R4 R5 R6
QUOTE_ROWS=10 IN_SPAN=10 IN_ENTRY=10 IN_LESSON=10 SHORT=10 CONTEXT=10 CAPTURE_BOUND=10
SUBSTANCE=PASS ANCHOR_BOUND=4/4 INFERENCE_GROUNDED=yes STRAY_IDS=-
C3=PASS   EXIT=0
```
R7 now bound by S135 — U2, a URL no fetch produced. Freeze disclosure covers edition identity and
entailment, not record honesty; C3 has no digest-pinned leg. No in-contract fix (any changes predicate).

## Attack 2 — new row S140 pointing at the catcm page cannot bind R4 — survives

Staged new S140 mined row (used-by entry), fabricated success record reusing catcm's real sha256s,
and `source: S140 — <catcm>` in entry. Catcm mentions R1 only inside 《》 citations, not R4.

```
$ python3 corpus/evidence/round57/c3-count.py
BOUND=4/7 (min 4) R1:S131 R2:S132 R3:S133 R7:S118
SWEPT=3/3 R4 R5 R6   STRAY_IDS=S140   C3=FAIL   EXIT=1
direct probe: heading_title(catcm_form, '抗肿瘤药品临床综合评价技术指南') = False
              heading_title(catcm_form, '关于开展药品使用监测和临床综合评价工作的通知') = False
```
R4 title and `2022年版` token absent; S140 goes stray → C3=FAIL. Survives.

## Attack 3 — one real-slice quote padded to 161 chars — SHORT fails; survives

### A3 (as run first): padded S132's row-2 quote to `form[1036:1197]` (161 chars, one line, exact slice)

```
BOUND=4/7 (min 4) R1:S131 R2:S132 R3:S132 R7:S118
QUOTE_ROWS=10 IN_SPAN=10 IN_ENTRY=10 IN_LESSON=10 SHORT=9 CONTEXT=10 CAPTURE_BOUND=10
SUBSTANCE=PASS ANCHOR_BOUND=2/2 INFERENCE_GROUNDED=yes STRAY_IDS=S133   C3=FAIL
```
SHORT fired as required — and a bonus defect surfaced: the padded slice happens to carry R3's title
`药品临床综合评价管理指南`, so R3 re-bound to S132 (sorted first) and S133 went stray. A long quote can
smuggle a second reference's title into a wrong row's quote set; the title-quote leg (`:229`) does not
check which reference the quote evidences. Reported, not patched.

### A3' (isolated SHORT): third S132 row, quote = `form[a:a+161]` of catcm line 341 (no REF title)

```
BOUND=4/7 R1:S131 R2:S132 R3:S133 R7:S118
QUOTE_ROWS=11 IN_SPAN=11 IN_ENTRY=11 IN_LESSON=11 SHORT=10 CONTEXT=11 CAPTURE_BOUND=11
SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=yes STRAY_IDS=-   C3=FAIL
```
Single failed leg: SHORT 10/11. Survives exactly as specified (160-char boundary enforced; the quote
must be newline-free to stay one manifest row — a `\n` quote just splits the row and is skipped, not
counted, so the newline-smuggle path is also closed).

## Attack 4 — `S130` mentioned in entry prose — STRAY_IDS fails; survives

Added one `#### Limits` bullet: "The 2020 management-guideline copy S130 is held but could not bind R3…"

```
BOUND=4/7 R1:S131 R2:S132 R3:S133 R7:S118   STRAY_IDS=S130   C3=FAIL   EXIT=1
```
`STRAY_IDS` scans all entry `S###` tokens outside `{S127}∪bound_ids` (`:272`); Limits placement
avoids inference-ground but still triggers. Survives.

- depth/sourced: **falsified at the provenance layer** — "the bytes of a successful attempt for (X,U) in
  refetch.tsv" is checkable only as record-vs-bytes self-consistency; replayed or fabricated records
  bind (A1a, A1b → C3=PASS). The R7 binding's truth value is unchanged (real S118 row remains), but the
  receipt names a URL/id pair that was never fetched — the same class of hole W1 CritC3Stray found in
  the id regex (lowercase `s128`), here in the fetch-record trust.
- Leg integrity: heading_title, SHORT (160/25 boundary, both directions), STRAY_IDS, IN_SPAN/
  IN_ENTRY/IN_LESSON, CAPTURE_BOUND, SUBSTANCE, ANCHOR_BOUND all hold under direct attack.
- Secondary: title-smuggling via a long multi-sentence quote (A3: R3 re-bound to S132) — counter
  still fails via STRAY_IDS, but a quieter composition of the same trick is the follow-on attack surface.

VERDICT: attacked C3's byte-provenance and leg set — FALSIFIED once: `good_raw` admits a fabricated
refetch record, so replayed capture bytes under a forged (id,url) reach C3=PASS in both same-id and
different-id form (A1a/A1b); the R4-heading, padded-quote, and stray-id attacks all fail as designed,
with a reported (unpatched) title-smuggling surface in the per-id quote leg.
