# Round 34 — Independent truth audit of the C1 counter (no candidate involved)

Seat: `ChousaR34.AuditC1Truth` · wave 1 · lane `chousa-shokunin`
Date: 2026-10-23 · scope: `corpus/evidence/round34/c1-count.py` (design v1) against
`tools/research-gate.sh` (base/landed bytes).

**Verdict: the C1 counter's truth labels are correct on all three fresh seeds — 0 disagreements
in 90 records, 0 structural problems, 0 class-semantics problems. No counter defect found.**

This seat scored **no candidate**: the gate run was against the landed base gate
`sha256 43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`, which is the
do-nothing control, not an `ExecC1Build*` patch. The counter run was the plain
`c1-count.py` on the landed gate — no scratch gate copies were built or scored here.

---

## 1. What was run

### 1.1 Counter runs (base gate, three fresh seeds)

```
C1_TMP=$PWD/tmp$s timeout 1800 python3 \
  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round34/c1-count.py \
  --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh \
  --seed $s --keep $PWD/k$s --receipt $PWD/rc$s.json
```
seeds 5101, 5102, 5103 (outside the reserved 3401–3409 band), run in parallel.

| seed | exit | label | gate_rc | elapsed_s | gate_sha256 | counter_sha256 |
|---|---|---|---|---|---|---|
| 5101 | 1 | `LONGSPAN_MATCH=19/30` | 1 | 695.964 | `43a1af35ca66…` | `5ef347874960…` |
| 5102 | 1 | `LONGSPAN_MATCH=19/30` | 1 | 819.668 | `43a1af35ca66…` | `5ef347874960…` |
| 5103 | 1 | `LONGSPAN_MATCH=19/30` | 1 | 883.697 | `43a1af35ca66…` | `5ef347874960…` |

Per-class (identical on all three seeds): `long-verbatim-ml 0/3`, `long-verbatim-1l 0/2`,
`long-edge 0/2`, `long-line-bound 0/2`, `long-line-wrong 0/2`, and every long `unsupported`
class at full marks (`long-mut-head 2/2`, `long-mut-tail 2/2`, `long-mut-mid 3/3`,
`long-split 2/2`, `long-glued-left 2/2`, `long-glued-right 2/2`), `short-verbatim 3/3`,
`short-mut 3/3`.

Receipt stderr tail, all three seeds:
`/usr/bin/grep: Argument list too long` at `research-gate.sh: line 1553` (`tok_span_at`).

19/30 is the value claims.md ("Before") predicts for the base gate: the 6 short records plus
the 13 long `unsupported` records match; the 11 long `supported`/`mislocated` records miss.

**Hash binding (E4 discipline).** The gate bytes and counter bytes were hashed before and
after the runs and are the committed blobs:
`research-gate.sh` → `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`
(claims.md base and landed value); `c1-count.py` →
`5ef347874960b52561a1cfa517f3f3fc0d1763830e3580c44b993f8394c0a565` (claims.md value).
Both were unchanged after the runs. Receipts carry the same two hashes, so they bind to
committed bytes, not to an uncommitted state.

Note on lane state: `git log` shows the lane HEAD moved to `ef16afb` ("design v2 before data")
during this wave. That commit does **not** touch the gate or the v1 counter — the hashes above
are identical before and after. The v1 counter file is still present and unmodified; a second
counter `c1-count-v2.py` (`7127246260390a8e…`) also exists at HEAD, which was **not** used or
scored here (this seat's assignment names `c1-count.py`).

### 1.2 Independent verifier (own code, not the counter's)

`.ufo/waves/round-34/w1/AuditC1Truth/verify_truth.py` — written from scratch; it does not
import, exec, or copy `c1-count.py`. It re-implements the boundary rules from the gate text
and derives every record's truth from the fixture bytes:

- `tok_word_char` / `tok_left_ok` / `tok_right_ok` transcribed from
  `tools/research-gate.sh:1513-1551` (TOK_WS ` \t\n\r\v\f`, TOK_PUNCT
  `!"#$%&()*+,./:;<=>?@[\]^_`{|}~`, `-` and `'` as conditional joiners, non-ASCII bytes as
  word characters), operating on **bytes** under the gate's `LC_ALL=C`.
- Occurrence enumeration: every occurrence of the span in the source bytes, then the
  boundary test, then the round-31 line binding — `l1 = newlines(hay[:off]) + 1`,
  `l2 = l1 + newlines(span)`; a record with a `line` field binds iff some delimited
  occurrence has exactly `(l1, l2) == (line_n, line_m)`.
- Verdict derivation follows the gate's own flow (`research-gate.sh:1802-1890`): no delimited
  occurrence → `unsupported`; delimited occurrence but no binding → `mislocated`; binding →
  `supported`.

### 1.3 Differential tests against the gate's own code

Three differentials were run so that my model is not merely self-consistent:

**(a) Boundary-rule differential — 7680 cases, IDENTICAL.**
The gate's own `tok_left_ok` / `tok_right_ok` / `tok_word_char` were extracted verbatim
(`sed -n '1506,1551p'` → `tok.sh`, sha `613ded6e5b5dc199…`) and run against my Python model
over exhaustive single-character edge cases plus 6000 random byte triples (alnum, whitespace,
punctuation, `-`, `'`, and non-ASCII). Result: `diff cases.expect cases.got` empty, 7680/7680
identical. An earlier 26-case mismatch was a defect **in my harness** (bash command substitution
stripping a trailing newline from the `before` field), fixed by sentinel-appending in the
decoder; after the fix the two implementations agree exactly.

**(b) Occurrence/line-range differential — 18 records, 0 disagreements.**
The gate's own `tok_span_all` (`sed -n '1582,1607p'` → `tok_all.sh`, sha
`79d54f3e5ee9d8bc…`) was run on every short-span record of all three fixtures; my model's
`(L1, L2)` list matched the gate's output exactly for all 18 (`agree=6 disagree=0` per seed).
Long records are skipped here because the gate's own argv path cannot search them — that is
the defect under test.

**(c) JSON-reader differential — 90 records, 0 disagreements.**
The gate's own bash JSON reader (`claim_scan` / `json_str` / `json_has_key` / `json_unescape`,
`sed -n '1139,1375p'` → `jsonread.sh`, sha `aed60eed485d86c6…`) parsed all 90 fixture lines:
every line `RC 0` (one well-formed JSON object), the key set seen by the gate equals the
Python-parsed key set for all 90, and the gate's decoded span byte length equals the Python
span byte length for all 90.

**(d) Counter output-regex check — PASS.**
`counter_regex_check.py` builds a 7-record local fixture and runs the real gate on it, then
applies the counter's own `LINE_RE` and `FIND_LINE_RE` to the gate's stdout. Result:
`COUNTER REGEX CHECK: PASS` — the observed map and the `CLAIM_LINE_MISMATCH` id set both match
expectation, including the `mislocated` path (`obs=id=A2 line=3-4 …`) and the single-line
`"line"` form.

---

## 2. Findings

### 2.1 Truth agreement (the core question)

`verify_truth.py` over `k5101 k5102 k5103`: **TOTAL PROBLEMS: 0**, every seed reported
`clean: no disagreements, no structural problems, no band notes`. Per class, all 90 records
agree between the counter's `truth.json` and my independent derivation:

```
long-edge 2/2, long-glued-left 2/2, long-glued-right 2/2, long-line-bound 2/2,
long-line-wrong 2/2, long-mut-head 2/2, long-mut-mid 3/3, long-mut-tail 2/2,
long-split 2/2, long-verbatim-1l 2/2, long-verbatim-ml 3/3, short-mut 3/3, short-verbatim 3/3
```

**Disagreements by class: none.** Zero of 90 records disagree.

### 2.2 Structural checks on claims.jsonl (all pass)

Per seed, all 30 lines: valid JSON, one object per line; top-level key set is exactly
`{id, source, span, expect}` (+ `line` on the 4 line-class records) — every key is one the
gate reads, none outside `{id, source, span, expect, marker, line, sha256}`; ids unique and
11 chars `c` + 10 hex; `expect` always `supported` (the label carries no truth); no `marker`
with a non-`contradicted` expect; every `line` value well formed with M > N; `source` files
present and non-empty; the id set equals the `truth.json` key set; class counts match the
docstring (3/2/2/2/2/3/2/2/2/2/2/3/3 = 30).

### 2.3 Span byte lengths (all pass)

Every span length sits inside its class's docstring band, and every long-class span is
≥ 32768 bytes. Observed extremes over the three seeds:

| class | band (docstring) | observed min..max (bytes) |
|---|---|---|
| long-verbatim-ml | 33000..65000 | 37670..64396 |
| long-verbatim-1l | 33000..65000 | 33658..53076 |
| long-edge | 32768..32900 | 32785..32843 |
| long-mut-head | 34000..65000 | 37310..56577 |
| long-mut-tail | 34000..65000 | 37237..55926 |
| long-mut-mid | 34000..65000 | 43982..61754 |
| long-split | 33000..65000 | 34894..59127 |
| long-glued-left | 33000..65000 | 45274..62897 |
| long-glued-right | 33000..65000 | 33599..61023 |
| long-line-bound | 33000..65000 | 37684..63388 |
| long-line-wrong | 33000..65000 | 34111..58370 |
| short-verbatim | 64..4096 | 109..3665 |
| short-mut | 64..4096 | 98..4007 |

All 72 long records are inside the claimed contract band 32768..65536 (0 outside). The smallest
long span present is 32785 bytes.

### 2.4 Class semantics (all pass)

`class_semantics.py` re-derives each class's property from the fixture bytes alone and checks
it against the docstring: multi-line vs single-line spans; `long-edge` in 32768..32900;
`long-mut-head` mutation offset ≤ 63, `long-mut-tail` in the last 64 bytes, `long-mut-mid` in
8192..len−8192 (all confirmed by locating the one-letter-mutated occurrence and aligning it);
`long-split` — both halves present in the source and **never adjacent**; `long-glued-left` /
`long-glued-right` — exactly one occurrence, glued to a word character on the named side and
delimited on the other, so the verdict rests on the glue rather than on a boundary accident;
`long-line-bound` — two delimited occurrences with `line` naming the second;
`long-line-wrong` — two delimited occurrences with `line` naming neither.
**TOTAL CLASS-SEMANTICS PROBLEMS: 0** on all three seeds.

### 2.5 The defect the counter is built to detect (confirmed present at base)

Measured directly: the largest argv string `/usr/bin/grep` accepts is **131071 bytes**, first
rejected at **131072** — exactly `MAX_ARG_STRLEN` (32 pages × 4096). The gate builds a
four-bytes-per-span-byte PCRE pattern (`research-gate.sh:1556-1566`), so the largest span the
argv path can search is 131071 // 4 = **32767 bytes**; a span of 32768 bytes or more fails with
E2BIG and the exec never runs. This matches the base measurement (grep "Argument list too long"
at `research-gate.sh: line 1553`) and the counter's `long-edge` class, whose smallest spans
(32785+) all sit above the threshold.

### 2.6 Observations (not defects)

1. **The counter is sound but not sharp.** The `long-line-wrong` truth is `mislocated`, and the
   gate reaches that verdict only when a delimited occurrence exists but none binds
   (`research-gate.sh:1829-1836`). A candidate that fixed only the argv path but broke the
   line-binding loop would read these 4 records as `supported`, and the counter scores that as
   a miss — correct behaviour for the counter, and worth noting for candidate scoring.
2. **Fixture size vs gate runtime.** Each base-gate run took 696–884 s of a 1500 s budget.
   Three seeds in parallel fit comfortably, but a candidate that removes the argv failure will
   make the gate *search* 30 large spans, so runtime may move up, not down. The counter's
   1500 s bound is the binding constraint to watch. [INFERENCE — not measured on a fixed gate,
   which this seat is not permitted to score.]
3. **`--keep` is the audit handle and it works.** `truth.json` plus `claims.jsonl` plus `src/`
   reproduce the fixture exactly, which is what makes an independent re-derivation possible at
   all.

---

## 3. Limits of this audit

- **No candidate was scored and no gate patch was built.** This seat verifies the *truth
  labels* of the counter, not whether a candidate reaches 30/30. The base gate's 19/30 is the
  do-nothing measurement, not a candidate result.
- **Occurrence-set differential covers short records only** (18 of 90). For long records the
  gate's argv path cannot enumerate at all, so the long-span occurrence set rests on my
  derivation plus the class-semantics reconstruction (which locates the actual mutated and
  split occurrences in the source bytes). [INFERENCE for the long-span occurrence sets; the
  boundary rules they apply were differentially verified (a) on 7680 cases and (b) on the
  18 short records.]
- **`--keep` fixtures were produced by the counter itself.** The audit re-derives truth from
  the kept bytes; it does not independently re-generate the fixture from the seed, so a defect
  in the *generator* that is self-consistent between generation and `truth.json` would not be
  caught by the truth comparison. The class-semantics check (2.4) is the guard against that
  class of defect, and it passed.
- **The gate's bash JSON reader is O(n²) in line length**; parsing one 60 KB fixture line took
  seconds, so the JSON differential is slow but complete (30/30/30 lines).
- The lane HEAD moved to design v2 mid-wave (`ef16afb`); the v1 counter and the base gate bytes
  audited here are unchanged from the frozen design v1 commit `70feb5e`.

---

## 4. Artifacts

All under `.ufo/waves/round-34/w1/AuditC1Truth/` (96 KB total; no fixture copies, which stay
in scratch and are cited by path):

| file | sha256 | purpose |
|---|---|---|
| `verify_truth.py` | `c527282ea56ac096…` | independent truth + structure verifier |
| `class_semantics.py` | `20ca602da31f779a…` | per-class property audit from fixture bytes |
| `evidence.py` | `a20e746dc00cafc4…` | per-record evidence table dumper |
| `diff_boundary.sh` | `7def478fa5d76efa…` | boundary differential driver (gate code vs model) |
| `diff_json.sh` | `5a66439a22014cfb…` | JSON-reader differential driver |
| `diff_occ.sh` | `9dab9042e418d96c…` | gate `tok_span_all` occurrence oracle |
| `diff_occ.py` | `a4a8ccd35ac3b720…` | occurrence-set differential driver |
| `counter_regex_check.py` | `96038e88f93d7cd1…` | counter `LINE_RE`/`FIND_LINE_RE` check on real gate output |
| `gen_cases.py` | `1b4ac5845bcd6546…` | boundary case generator |
| `tok.sh` | `613ded6e5b5dc199…` | gate `:1506-1551` extracted verbatim |
| `tok_all.sh` | `79d54f3e5ee9d8bc…` | gate `:1582-1607` extracted verbatim |
| `jsonread.sh` | `aed60eed485d86c6…` | gate `:1139-1375` extracted verbatim |
| `V1.txt` | `179d08c11c09cb0f…` | verify_truth.py run log (3 seeds, 0 problems) |
| `V2.txt` | `6080857da258a79b…` | class_semantics.py run log (3 seeds, 0 problems) |

Scratch (large, not copied): `/fast/scratch/hyaku/chousa-r34/w1/AuditC1Truth/`
— fixtures `k5101/ k5102/ k5103/`, receipts `rc5101.json rc5102.json rc5103.json`,
logs `log510*.txt`, gate-reader output `json510*.txt`, boundary cases `cases.tsv cases.expect
cases.got`, verification logs `V1.txt V2.txt`, evidence tables `evidence510*.txt`.

No tool was installed or updated for this audit (no pacman, uv, cargo, or npm action).

---

## 5. Summary

| question asked | answer |
|---|---|
| Do the counter's truth labels match an independent derivation? | Yes — 90/90 records, 3 seeds, 0 disagreements |
| Any counter defect? | **None found** |
| claims.jsonl valid JSON, keys only what the gate reads? | Yes — 90/90 lines, RC 0, key sets match |
| Span byte lengths match the docstring bands? | Yes — 13/13 classes within band on all seeds |
| Every long span ≥ 32768 bytes? | Yes — 72/72; smallest 32785; all inside 32768..65536 |
| Does the base gate really fail at ≥32768-byte spans? | Yes — grep argv limit 131071 B / 4 = 32767 B max searchable span |
| Base-gate score | 19/30 on each of seeds 5101/5102/5103, as claims.md predicts |
