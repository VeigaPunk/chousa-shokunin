# R58ExecC2BuildSpans — C2 S101 span set, round 58

Build the frozen 12-row S101 span set with the pinned round-55 `tools/build-spans.py` against the lane capture store, in scratch only; report command, rows, offsets, digests; compare against the frozen quote set. Lane @ `5da0a63` (freeze `9e73a03`); source reads read-only; only this report written.

**Headline: the artifact builds cleanly and reproducibly, but the frozen C2 counter cannot accept any artifact the pinned builder can produce. Three frozen defects — one in `c2-count.py` (offset convention), one in the round-58 control set, one in the NEW_GROUND grep. Fixing them is the L1's call, not mine.**

## 1. Build — SUCCESS

```
python3 -B tools/build-spans.py --quotes corpus/evidence/round58/c2/quotes.tsv \
  --out <scratch>/c2-spans --cache corpus/captures
QUOTE S101 char 315/330/590/683/734/781/797/838/965/993/1460/11723  spans/S101-1..12.txt
SPANS_ROWS=12 WRITTEN=12          EXIT=0
```

Pins verified: `tools/build-spans.py` = `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` = `controls/build-spans-r55.py` (identical bytes); `tools/capture-text.py` = `2c0140bc…02573`; capture `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` = `6063a3af…fddf3` (= claims.md, `c2-count.py` `RAW_SHA`); `sha256(url)[:24] == 6dc68fd6b32ce9c8dfcebce8`. No network; the `.raw` (OLE magic `d0cf11e0a1b11ae1`) is decoded by `capture-text.py`. Determinism: two builds → identical `spans.tsv` and identical span bytes; `--check` → `SPANS_ROWS=12 STALE=0`, exit 0.

## 2. Rows, offsets, digests

`offset` = **context start** (`max(0, quote_abs-80)`), the convention `tools/build-spans.py` has used since round 50 (`str(start)` in every round-5x builder). Quote abs = `offset+80`. Files under `corpus/evidence/round58/c2/spans/`; `spans.tsv` = `8b910a5ec191e023ed9416f07ce58b8109f33ca1973a666a470db752800b460b`; every row's `capture_sha256` = `6063a3af…fddf3`.

|file|offset|abs|sha256| |file|offset|abs|sha256|
|---|---|---|---|---|---|---|---|
|`S101-1.txt`|235|315|`60ae136202c74b70c7246da9650f510eac2bfadaffe74536639e270a5a1b75c2`|`S101-7.txt`|717|797|`34972427eaf386ed0ea30b71fe12b51c01d37dfc8eb10fcc7d33af2296017b6f`|
|`S101-2.txt`|250|330|`dd4b69755a91aa0e7b707063c5f6e163908c4e07b253cbc5a4b930ae99d19589`|`S101-8.txt`|758|838|`712e7eb55dcdd0c3ce2adc24c67a32c547d3c85dfd00b1cc08499dfcac2be1ac`|
|`S101-3.txt`|510|590|`d7360b13c8c54b8dd322b250cbb10b14c31c6c8b75faad698206ea9f8cba19fd`|`S101-9.txt`|885|965|`4f2fe6f32f6d1afcad676be0f8f0d97a6ddc91411242b103d76ca60c804b9383`|
|`S101-4.txt`|603|683|`826f4efac276c5b3da3a600e28a04ea9f20710100d50a1ea2de5c6e62855cad4`|`S101-10.txt`|913|993|`5f5a1fcf6c53cefd5f3d2c4a44c868629ec56192a8080fd0b63f9767772cf22c`|
|`S101-5.txt`|654|734|`4edb42217b9dacc82a7fdb6ddaf4178a9ace5346dea034d0bf2c45819ddcb808`|`S101-11.txt`|1380|1460|`f5c95486a6f212e3516a03b8da260926b8786a9d141c3297d82571010099d558`|
|`S101-6.txt`|701|781|`bea294e4212debb63aba30afc8d0c903a12f0e5042a2ad12a940aae1ffd699bf`|`S101-12.txt`|11643|11723|`475d4635aa58130dd2d410a78d7f46500fc37bcb49b0771beb716461ffe124fd`|

## 3. Quote-set comparison — PASS

`c2/quotes.tsv` header `id\turl\tquote\tentry`; its 12 quote cells are byte-identical to `c2-count.py`'s frozen `QUOTES` (`tsv == c2.QUOTES` → True, 12 entries, unique). Each quote occurs **exactly once** in the defined text form (the builder refuses 0 or ≥2 occurrences; it wrote 12 rows). All 12 are ≤36 chars (counter's `QUOTE_TOO_LONG` leg satisfied) and appear in the built spans and in the proposed entry. The `.txt` sidecar `6dc68fd6b32ce9c8dfcebce8.txt` contains **none** of the 12 (count 0 each) — it is the UTF-16LE text, not the defined form; only `.raw` → `capture-text.py` binds them (round-54 lesson; round-55 builder's `Forms.get` routes OLE captures to `capture-text.py` and ignores the sidecar).

## 4. DEFECT 1 — frozen `c2-count.py` offset convention contradicts the pinned builder

`c2-count.py:101` requires the manifest `offset` to equal the **absolute quote position** (`occurrences[0] != off` → `CAPTURE_BIND`). The pinned builder writes the **context start** (`tools/build-spans.py:149`, `str(start)`). They differ by exactly 80 on all 12 rows. A genuine mutual exclusion, not a misreading: builder output as-is → `CAPTURE_BOUND=0/12`, `ANCHOR_BOUND=0/3`, `C2=FAIL`; rewrite only the `offset` column to absolute → `CAPTURE_BOUND=12/12`, `ANCHOR_BOUND=3/3`, but `REBUILD=FAIL` (`BUILDER_REBUILD_MISMATCH`), because the counter re-runs the pinned builder and byte-compares the manifest. **No artifact can satisfy both the binding leg and the rebuild leg.** The C1 counter's `expect_ok` (`start = max(0, form.find(quote) - CONTEXT); if offset != start`) and every prior round's counter (rounds 50–56: `int(offset) + span.find(quote)`) use the context-start convention — C1 agrees with the builder; round-58's C2 counter is the outlier. Frozen counter, unmodified, on a scratch copy (entry + registry row + builder output):

```
QUOTE_ROWS=12/12 CAPTURE_BOUND=0/12 ENTRY_QUOTES=0/12
SUBSTANCE=PASS ANCHOR_BOUND=0/3 INFERENCE_GROUNDED=yes STRAY_IDS=- NEW_GROUND=yes REBUILD=MATCH
ERROR CAPTURE_BIND:S101  (×12)   ERROR CAPTURE_BOUND=0/12   ERROR ANCHOR_BOUND=0/3
ERROR ENTRY_QUOTES=0/12          C2=FAIL
```

`ENTRY_QUOTES=0/12` is a symptom of the same bug: the `continue` at line 103 skips the `quote in text` check for any row that failed `CAPTURE_BIND`.

**Proposed patch (report only — lane file not edited; `git apply --check` clean at `5da0a63`):**

```diff
--- a/corpus/evidence/round58/c2-count.py
+++ b/corpus/evidence/round58/c2-count.py
@@ -98,11 +98,15 @@
             try: off=int(offset)
             except ValueError: errors.append('OFFSET_INVALID'); continue
             occurrences=[m.start() for m in re.finditer(re.escape(quote),form)]
-            if url!=URL or digest!=RAW_SHA or len(occurrences)!=1 or occurrences[0]!=off:
+            occ = occurrences[0] if len(occurrences)==1 else -1
+            # build-spans.py records the CONTEXT START in `offset`; the quote's absolute
+            # position is that start plus the quote's index within the span.
+            exp_start = max(0, occ-80)
+            if url!=URL or digest!=RAW_SHA or occ<0 or off!=exp_start:
                 errors.append('CAPTURE_BIND:'+sid)
                 continue
             bound+=1
-            start=max(0,off-80); end=off+len(quote)+80
+            start=exp_start; end=occ+len(quote)+80
@@ -112,7 +116,7 @@
-            if off==0 or form.rfind('\n',0,off)+1==off: anchors+=1
+            if occ==0 or form.rfind('\n',0,occ)+1==occ: anchors+=1
```

Restores the builder's convention **without weakening any check**: span bytes are still compared byte-for-byte against `form[exp_start:occ+len+80]`. Validated with the patched counter — builder output + entry + registry → `C2=PASS` exit 0; absolute-offset manifest → `C2=FAIL`; both no-do-nothing controls (`STAGED`, `REWRITE`) → `C2=FAIL`; tampered `spans/S101-5.txt` → `C2=FAIL` (`SPAN_BYTES:S101`, `REBUILD=FAIL`).

## 5. DEFECT 2 — the pinned r55 control copy is not self-contained

`controls/build-spans-r55.py` is byte-identical to `tools/build-spans.py` but resolves `TOOLS = Path(__file__).parent`, so `_capture_text()` imports `.../round58/controls/capture-text.py` — **which does not exist**:

```
FileNotFoundError: [Errno 2] No such file or directory:
  '.../corpus/evidence/round58/controls/capture-text.py'
```

So on the lane's OLE store the control dies with an exception instead of exercising the refusal it models. `c1-count.py` on the r55 control: `HELDOUT_OK=fail(rc=1)`; on `tools/build-spans.py`: `HELDOUT_OK=pass`. The control is not a faithful stand-in for the builder it is pinned against. Also observed (unmodified frozen C1 counter, lane builder):

```
FIFO_TXT=fail(rc=1, reason [...] absent in 'build-spans: refused S571: no defined text form for f4088c6… (raw neither OLE nor zip, no .txt)')
DEVZERO_TXT=fail(... same "no defined text form" reason ...)
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'capture-text refused f96cbd6d…: ole-malformed: sector shift 0, mini shift 0')
MANY_QUOTES=fail(rc=0, expected refusal)   SYMLINK_OUT=fail(rc=0)(target-dir-written!)
SYMLINK_CACHE=fail(rc=0, expected refusal)  FOREIGN=fail(rc=0, orphans deleted)
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2   C1=FAIL
```

Notes for the L1: (a) FIFO and `/dev/zero` refuse for the wrong *reason class* (`no defined text form` — the builder stats a FIFO via `is_file()` and never opens it, which is safe) but C1 requires the refusal to name the type, so the hardened builder must classify the object before the `.txt` fallback; (b) `FAT_RAW` dies inside `capture-text` with `ole-malformed`, so a size cap must precede the `capture-text` call. `BEFORE_FOREIGN=deleted` and `DENIED=2/2` confirm the leg discriminates.

## 6. DEFECT 3 — NEW_GROUND grep uses a different character than the claim

`c2-count.py:153` greps the base tree for **`載`体类型标识** (U+8F09, traditional) while line 154 tests the entry for **`载`体类型标识** (U+8F7D, simplified) — and claims.md names the simplified form. Proved in a scratch clone: planting the simplified string into a `corpus/knowledge` file and committing it, the counter's own grep still returns rc=1 while the claim's grep returns rc=0:

```
git grep -l '載体类型标识' HEAD -- corpus/knowledge   → rc=1   (counter's pattern)
git grep -l '载体类型标识' HEAD -- corpus/knowledge   → rc=0   (claim's pattern)
```

The "absent from the base" precondition is therefore **vacuous** — it can never fire for the string the claim names. At the true base `b13ca7b5` neither variant is present (`rc=1` both), so the ground is genuinely new and `NEW_GROUND=yes` is currently correct — but the check tests the wrong string. One-line fix: use `载体类型标识` in the `git grep` at line 153.

## 7. Copyable artifact patch

`artifact.patch` (261 lines) against `5da0a63`; `git apply --check` clean. Adds exactly the C2 surface: `corpus/evidence/round58/c2/spans.tsv` (12 rows, builder output verbatim), `corpus/evidence/round58/c2/spans/S101-1..12.txt`, `corpus/knowledge/carrier-alphabet-china-r58.md` (trio `source:`/`verified-at:`/`recheck:` as lines 1–3, all 12 quotes verbatim, `载体类型标识` present, no stray S-id), and `corpus/SOURCES.md` (S101 `used-by` **appended** with the new entry; the pre-existing `citation-count-semantics-r37.md` reference preserved). Applied to a fresh clone at `5da0a63` and run against the patched counter: `C2=PASS`, exit 0. The `SOURCES.md` change is a one-cell append on a very long line — re-derive it from the base row if applying by patch is inconvenient. `git apply` reports 3 trailing-whitespace warnings on span files: genuine bytes of the defined text form, not patch damage.

## 8. Unrun checks

- The §4 counter patch and the §6 character fix were **not** applied to lane files; validated only on scratch copies.
- `c2-count.py` against the unmodified lane at `5da0a63`: `C2=FAIL` with `ENTRY_MISSING`, `MANIFEST_MISSING`, `QUOTE_ROWS=0/12` — the expected pre-build baseline, matching `controls/c2-before.txt`.
- No live fetch; the round-57 r2 egress-scope L0 question untouched.
- C1's remaining hazard legs need a hardened builder — outside this seat's assignment.

VERDICT: the C2 S101 12-row span build via the pinned round-55 builder against the lane capture store **survives** (12/12 rows, deterministic, quote set byte-identical, digests in §2), while the frozen round-58 C2 counter's offset-convention leg **falsifies** C2 as specified — no artifact the pinned builder can produce reaches `C2=PASS` — and the C1 control-copy and NEW_GROUND character defects **falsify** the round-58 control and ground preconditions; proposed fixes validated in scratch restore `C2=PASS` while keeping the no-do-nothing controls and a tampered-span attack failing.
