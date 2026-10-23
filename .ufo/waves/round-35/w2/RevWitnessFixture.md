# RevWitnessFixture — audit of tools/mechanism-witness.py fixture generator

Scope: `generate`, `build`, `Gen.span` in `tools/mechanism-witness.py`
(sha256 `9f537bfde0dd53f2240af149e1b7a03fd0a0f372ee1fa1a32e94044115a252b3`,
unchanged at wave base e87c5d7 and HEAD b6f2c0d). Date: 2026-10-23.
Gate pinned for every run: sha256 `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`
(extracted via `git show e87c5d7:tools/research-gate.sh` to
`…/RevWitnessFixture/gate-base-1f2fb4f5.sh`; sha re-verified on the copy).

## Incidental note (not a fixture defect)

The working-tree gate changed under review: `sha256sum tools/research-gate.sh`
returned `1f2fb4f5…` at my start, then `a4768851…` at 17:07 (uncommitted
grep-pin hardening), and the change was later committed as part of tip
`b6f2c0d`. My first 23 witness receipts record `gate_sha256=a4768851…` and are
invalid per the pin rule; every measurement below was re-run against the
pinned blob and those receipts record `1f2fb4f5…`. The claims-loop /
matcher region is identical in both revisions (line numbers +21 only).

## Q1 — span bounds: PASS, no defect

`Gen.span` (tools/mechanism-witness.py:124-135) truncates at the last
separator index `i` with `lo <= i <= min(hi, len(s)-1)`, so `len(s[:i]) == i ∈
[lo,hi]`; `len(s) > hi+12` is guaranteed by `Gen.text` overshoot (words are
≥2 letters + separators). Proof-level bound; measured:

- `build()` 300 draws/class across 20 fresh `Gen` seeds (command:
  `python3 audit_fixture.py`, artifact `fixture_audit.json`):
  every dz-* class n=300, min=32765 max=32767; short-verbatim n=300
  min=4087 max=4096 (⊂ [512,4096], never ≤32764 violation).
- `generate()` on 20 seeds (9100–9119), all 180 records: same ranges.
- `dz-edge` only ever produces 32765 or 32767 (`build` passes lo=hi=n,
  n ∈ {32765,32767}); 32766 for the other dz classes — all > 32764, so all
  8 non-short records route to `tok_span_offsets_chunk`
  (gate blob:1668 `if (( ${#span} > TOK_DIRECT_SPAN_MAX ))`, MAX=32764 at :1650).
- Non-termination: the retry loop only fails a draw when no separator lands
  in the 3-index window [lo,hi] — possible per draw but memoryless retries;
  `mutate`'s `cand` can never be empty (129-char window, letters-only vocab,
  no two adjacent separators ⇒ ≥64 letters); `s.index(" ", len(s)//2)`
  cannot raise (runs only when `"\n" not in s`, so the tail's separators are
  all spaces; the tail is ≥16382 chars ≫ 10-char word+separator span).

## Q2 — line-bound `line` values: PASS, all 20 verified

`build` dz-line-bound (tools/mechanism-witness.py:163-169) emits
`line = "%d-%d" % line_range(src, len(head)+len(s)+len(mid), s)` — the second
occurrence's true offsets. I recomputed delimited occurrences per generated
file with the gate's own boundary rules (blob :1608-1640
`tok_left_ok`/`tok_right_ok`; fixture bytes are letters/space/newline only so
the word-internal `-`/`'` rules can never fire — vocab is LETTERS-only):

- All 20 line-bound records: `raw_occurrences == 2`, and the record's
  `line` equals the 2nd delimited occurrence's `(l1,l2)` exactly
  (e.g. s9100 `line="346-671"`, ranges `[[14,339],[346,671]]`).
- `M > N` always (the `"\n" not in s` injection at :132-134 guarantees ≥1
  newline) ⇒ the gate's `M<=N → invalid` path (:1915-1919) is unreachable;
  the `%d-%d` form is leading-zero-free ⇒ record never takes a `bad` path.
- The 1st occurrence always precedes the 2nd, so ranges can't collide.

## Q3 — randomization: PASS on all claimed axes

Over seeds 9100–9119 (`generate()` output, `fixture_audit.json`):

- temp prefix: `mkdtemp` suffix is per-run random (not just per-seed) — varies.
- id shape: `id_width` ∈ [6,14] observed [9,10,12,13] sample (replay of the
  exact draw order: seeds 3501/3517 → width 13 prefix 'm' / width 10 'r');
  id_prefix 1–4 letters varies (82 distinct prefixes).
- name scheme: `hex`/`word` per seed — observed 63/117 across 180 files,
  both schemes present; scheme is per-seed constant.
- key order: 44 distinct insertion-order permutations over 180 records.
- record order: all 20 seeds produced distinct class orders (20/20).
- Fixed surface remains: `expect` is always `"supported"` (line 206 — the
  truth lives only in `truth`), claims live at `corpus/*.md`, `line` present
  iff dz-line-bound, no marker/sha256 fields. A fixture-wide detector
  (expect=supported everywhere, corpus/ names, mtimes in a fixed
  `1.6e9+…` window) still exists, but under this battery any such engine
  that skips the matcher *fails* the witness, so it aids detection.

## Q4 — `long_records` denominator

**Right shape, one call of slack.** `long_records` (mechanism-witness.py:294)
counts the 8 records with `len(span) > 32764`. The landed gate stamps the
chunk-entry line once per `tok_span_offsets_chunk` call (bash -x traces
`local LC_ALL=C` at blob:1699 per call), and `tok_span_offsets` is reached
from `tok_span_at` for every record — plus a SECOND call through
`tok_span_all` for any record carrying `"line"` (blob :1979
`done < <(tok_span_all …)`). Landed truth is therefore
`long_records + N_linebound = 9`, not 8:

- Measured: 22 pinned-blob runs (seeds 3501, 3517, 9100–9119) — every one
  `WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1 (long records=8)`
  (receipts `base-wit-s*.json`, `landed-sweep/`).
- **Demonstrated slack (finding, low severity):** a gate whose
  `tok_span_all` call site uses an output-equivalent `bytes.find` helper
  instead of `tok_span_offsets` — `gate-shortcut-all.sh` sha256
  `5a1e4b48e3fd66a7d54fceb5f4030926d991fd5afdc7530d528807eabac1db42` —
  prints `WITNESS=pass OUTPUT=9/9 chunk=8`: exactly at threshold, so one
  whole record's (in fact one whole call path's) matcher work can be skipped
  invisibly. The `>=` total-count threshold cannot attribute stamps per
  record. P2 itself is unaffected: K1/K2 route *all* long spans away
  (stamps→0). Note the naive direct-matcher variant does NOT evade
  (`b11e7d3d…` scored 8/9 — direct can't compile a 4·32765-byte PCRE;
  that's the dead-zone fact itself). In current fixtures N_linebound=1 so
  slack is exactly one call; more `"line"` records would widen it.

**Can a seed make the landed gate stamp < `long_records`? No — I could not
construct one, and none is reachable.** Every skip-before-matcher path was
enumerated in the blob and all are unreachable from generated records:
record-invalid paths (:1803 `claim_scan`, :1816 dup keys, :1888-1897 bad
fields, :1905-1922 bad `line`) are structurally excluded (keys unique by
construction, expect always `supported`, `line` always valid "N-M");
`claim_source_path` refusals (:1479-1577 — session/denylist/ephemeral/url,
out-of-corpus, missing, multilinked, >8 MiB, cross-device) are unreachable:
rel names are `corpus/[0-9a-f]{16}.md` or `corpus/[a-z]{3,7}-\d{4}.md`, which
cannot match any `is_denylist_path_value` pattern (:720-731), files are
~35–70 KiB fresh writes with nlink=1 on the same device as root. A `rel`
collision (2⁻⁶⁴ hex or 10⁻⁴·letters word names) would only break OUTPUT, not
stamps — the overwritten record still calls the matcher before missing.
Measured: 22/22 seeds, chunk=9 ≥ 8, zero misses.

`matcher_entry_lines` picks the FIRST `tok_span_offsets_chunk()`
definition (:90 `l.startswith(fn+"()")`); a gate that shadow-defines the
function after a stub would fail the witness (stamps land on the live
definition's lines), i.e. evasion-safe. `stamp_re` requires
`group(1)==abspath(gate)` — no colon/digit false positives on these paths.

## Residual risks / verification gaps

- K2's key (`c2-count.py:77` `/tmp/*|/fast/*|/var/tmp/*`) is an ENVIRONMENT
  dependency, not a seed property: `C2_TMP`/`TMPDIR` outside those prefixes
  leaves K2 inert → witness=pass → P2 fails for environmental reasons.
  [INFERENCE — cannot test inside my bounds; code-evident.]
- `output_full` requires `p.returncode == 1 and drift` (:297) — correct for
  this truth mix (3 engineered misses); a future all-clean fixture would
  need rc==0.
- 20-seed sweep covers fixture-level behaviour; trace-level timing flakes
  were not observed (all runs ≤ ~10 s, GATE_TIMEOUT_S=1500).
- Fixture audit script and full per-seed data:
  `…/RevWitnessFixture/audit_fixture.py`, `fixture_audit.json`;
  generated fixtures (12 MiB) at /tmp/hyaku/chousa-r35/w2/RevWitnessFixture/fx.

## Verdict

No MEETS-affecting defect in the fixture generator: spans provably stay in
32765..32767, line-bound `line` fields are exact, randomization varies all
claimed axes, and no seed can make the landed gate stamp below 8. One
calibration finding: the `long_records` threshold is `long_records +
N_linebound` short of the true landed count — one matcher call (or one
record, in general) can be shortcut invisibly, demonstrated
(`gate-shortcut-all.sh`: OUTPUT 9/9, WITNESS pass at chunk=8).

Report: .ufo/waves/round-35/w2/RevWitnessFixture.md
