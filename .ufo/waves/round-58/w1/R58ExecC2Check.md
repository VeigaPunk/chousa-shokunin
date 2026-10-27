# R58ExecC2Check — frozen C2 counter against the base state (round 58, wave 1)

Scope: run the frozen `corpus/evidence/round58/c2-count.py` on a scratch mirror holding only the committed S101 capture, the registry and the frozen quotes (no new entry); identify the first failure; verify the counter correctly rejects the base state. Only lane write: this report; no live fetch; no installation (nothing to install, `pacman` untouched).

## 1. Setup (scratch only; lane read-only)

```
SCR=/fast/scratch/hyaku/chousa-r58/R58ExecC2Check
git clone --local --no-hardlinks /home/vgpnk/Projects/shokunin/chousa-shokunin "$SCR/m2"
git -C "$SCR/m2" rev-parse --show-toplevel   # -> $SCR/m2   (assert before any git op)
git -C "$SCR/m2" checkout --detach b13ca7b5c8bbb40d2d29a37fb443c64ca043f791
mkdir -p "$SCR/m2/corpus/evidence/round58/c2"
git -C "$SCR/m2" show 9e73a031ab1ac3bac343de008850d7d87f9e5634:corpus/evidence/round58/c2/quotes.tsv \
    > "$SCR/m2/corpus/evidence/round58/c2/quotes.tsv"
```

Verified: raw sha256 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3` (= frozen `RAW_SHA`; OLE magic `d0cf11e0a1b11ae1`); `quotes.tsv` sha256 `73705361909911e9e03be9f4ca3a72a5ba9723844f0e42df39939f0095222868` (frozen set, freeze commit); `tools/build-spans.py` `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` (= `BUILDER_SHA`); `tools/capture-text.py` `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573` (= `CT_SHA`); `corpus/knowledge/carrier-alphabet-china-r58.md` **absent**; `…/c2/spans.tsv` **absent**.

## 2. Base-state counter run (exact command and output)

```
export TMPDIR="$SCR/wA"; mkdir -p "$SCR/wA"
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c2-count.py \
  --root "$SCR/m2" --work "$SCR/wA"
```
```
ENTRIES=0/1 BOUND=0/1 REF_ID_UNBOUND=1
QUOTE_ROWS=0/12 CAPTURE_BOUND=0/12 ENTRY_QUOTES=0/12
SUBSTANCE=FAIL ANCHOR_BOUND=0/3 INFERENCE_GROUNDED=no STRAY_IDS=- NEW_GROUND=no REBUILD=FAIL
ERROR ENTRY_MISSING
ERROR PROVENANCE_TRIO
ERROR S101_NOT_IN_SOURCE
ERROR REF_ID_UNBOUND
ERROR MANIFEST_MISSING
ERROR BUILDER_REBUILD_MISMATCH
ERROR CAPTURE_BOUND=0/12
ERROR ANCHOR_BOUND=0/3
ERROR ENTRY_QUOTES=0/12
ERROR NEW_GROUND_FAIL
C2=FAIL
```

exit 1. **First failure: `ERROR ENTRY_MISSING`** — the counter's first evaluated check is `entry.is_file()` for the r58 entry, absent at base. The lane's own baseline receipt `corpus/evidence/round58/controls/c2-before-frozen.txt` (landed in a sibling commit after the freeze) is **byte-identical** to my 10 error lines and summary, and agrees on the first failure. The counter **does** correctly reject the base state.

## 3. Depth probe: is `C2=PASS` reachable at all?

I built a complete, honest candidate **in scratch only** (registry `used-by` updated, a real entry with the provenance trio and all 12 quotes, the frozen builder's manifest) and drove the counter leg by leg. Two of its legs are mutually contradictory.

### 3a. The offset-column convention conflict (fatal)

The pinned builder writes the **`offset` column as the span-context start** (`quote_pos-80`): `tools/build-spans.py` (`build()`) does `off = text.find(quote)`, `start = max(0, off - CONTEXT)` (`CONTEXT = 80`), `span = text[start:off+len(quote)+CONTEXT]`, then appends `str(start)` as the manifest's `offset` cell. But `c2-count.py` binds the manifest against the **quote position** — `if ... or len(occurrences)!=1 or occurrences[0]!=off: errors.append('CAPTURE_BIND:'+sid)` — and `SPAN_BYTES` recomputes the expected span from the same `off` (`form[max(0,off-80) : off+len(quote)+80]`).

Measured over the frozen 12 quotes against the builder's own output, **all 12 rows fail both binding legs**: `quote_pos` 315/330/590/…/11723 vs builder `offset` 235/250/510/…/11643 — `SPAN_BYTES` False and `CAPTURE_BIND` False on every row, because `offset` is `quote_pos-80` and the recomputed expected span is displaced by 80 characters. `CAPTURE_BIND` fires first and `continue`s, masking `SPAN_BYTES`.

The requirements are **mutually exclusive**, because the counter also demands `REBUILD` — the committed manifest must be **byte-identical** to the pinned builder's output (`(tmp/'spans.tsv').read_bytes()==manifest.read_bytes()`). Byte-identical builder output ⇒ `offset = quote_pos-80` ⇒ `CAPTURE_BIND` fails. `CAPTURE_BIND` passing ⇒ `offset = quote_pos` ⇒ bytes differ from the builder's ⇒ `REBUILD` fails. No frozen quote sits at position 0 (`min(quote_pos)=315`), so the conventions can never coincide. Both directions confirmed:
- Commit the **builder's** manifest bytes → `CAPTURE_BOUND=0/12`, `REBUILD=MATCH`, `ERROR CAPTURE_BIND:S101` ×12.
- Rewrite the same manifest's `offset` column to the **quote positions** → `CAPTURE_BOUND=12/12`, `ANCHOR_BOUND=3/3`, all `SPAN_BYTES` pass, but `ERROR BUILDER_REBUILD_MISMATCH`, `REBUILD=FAIL`.

Either way `C2=FAIL`. **`C2=PASS` is unreachable under the frozen counter + frozen builder** — a defect in the frozen predicate, not in the entry under test. The counter is the outlier, not the lane: across **every** committed lane manifest the `offset` column is the *span start*, and the quote position is recovered as `offset + span.find(quote)` — exactly what `round57/c3-count.py` does. Over all 13 committed `spans.tsv` files (365 rows): `offset == quote position` holds for **1** row (a round-52 row with `offset=0`, `quote_pos=0`); `offset + span.find(quote) == quote position` holds for **353**. `round45/c3-count.py` and `round57/c3-count.py` both check `form[o:o+len(span)] == span`, i.e. the span-start convention. The frozen C2 counter introduces a third, contradictory convention.

### 3b. Secondary findings (do not change the verdict)

1. **`PROVENANCE_TRIO`/`S101_NOT_IN_SOURCE` is stricter than the lane's entry format.** `lines[:3]` must be exactly `source:`, `verified-at:`, `recheck:` — no title heading may precede them. Most lane entries lead with `# Title`; only 5 in `corpus/knowledge/` are trio-first, and `S101_NOT_IN_SOURCE` fires unless the `source:` line contains `S101`.
2. **One frozen quote needs a full-width comma reproduced byte-for-byte in the entry.** `1．2．1 根据GB3469规定,以单字母方式标识以下各种参考文献类型：` uses U+FF0C. The capture's defined text form carries U+FF0C there (verified `form[i+16] == '，'`; the ASCII-comma variant does not occur at all), so the frozen quote is faithful to the source — but an entry typing U+002C there fails `QUOTE_NOT_IN_ENTRY`/`ENTRY_QUOTES=11/12`. The only character-level trap in the set; the other 11 quotes matched exactly.
3. **`NEW_GROUND`'s base-side grep uses the wrong character form.** It greps the base tree for `載体类型标识` (**traditional** 載, U+8F09) but requires the **simplified** `载体类型标识` (U+8F7D) in the entry. `git log --all -S` over `corpus/knowledge` shows **neither** form has ever appeared there, so the grep returns rc=1 ("absent") regardless: in a scratch probe I injected the simplified form into a base commit's `citation-count-semantics-r37.md` and the traditional-form grep still returned rc=1. The leg cannot detect prior simplified-form ground — vacuously true this round (the ground is genuinely new at base), a latent weakness, not a live bypass. The leg also needs a git worktree with the base commit reachable: against a plain directory copy (no `.git`) it fails with `NEW_GROUND_FAIL`.
4. **C1's tool change collides with C2's `BUILDER_PIN`/`REBUILD` legs.** `c2-count.py` pins `tools/build-spans.py` to the round-55 sha and requires a byte-identical rebuild, while C1's claim is to modify `tools/build-spans.py`. In a scratch probe I applied a functional C1-style 64 MiB size cap to the mirror's builder: C2 then printed `ERROR BUILDER_PIN` and `ERROR BUILDER_REBUILD_MISMATCH`, `C2=FAIL`. Claims.md asserts "C2 uses the pinned round-55 builder and capture-text, so it is independent of C1's tool change" — true only if C1's builder lands elsewhere, or C2 is scored against a snapshot holding the round-55 builder. `c1-count.py` is itself path-flexible (`--builder`; its own round-55 copy at `controls/build-spans-r55.py`).

## 4. What the counter did well, and the proposed patch

- It rejects the base state cleanly, for the right reason (`ENTRY_MISSING`, first check), matching the lane's own frozen baseline receipt exactly; its pins are byte-exact and it detects a mutated builder (`BUILDER_PIN`).
- Its quote-set check is exact: the frozen `quotes.tsv` passed `QUOTES_HEADER`/`QUOTE_SET` with no error, and all 12 quotes occur **exactly once** in the capture's defined text form (the pinned `capture-text.py` stdout form and the builder's internal form are byte-identical, 27012 chars).
- It is not merely refusing everything: with a trio-first entry and a quote-position manifest it printed `SUBSTANCE=PASS ... INFERENCE_GROUNDED=yes NEW_GROUND=yes ANCHOR_BOUND=3/3 CAPTURE_BOUND=12/12 ENTRY_QUOTES=12/12` and failed on **only** `BUILDER_REBUILD_MISMATCH`.
- Proposed patch (proposal only; no frozen file edited): read the manifest `offset` as the span start and recover the quote position from the span, exactly as `round57/c3-count.py` does — replace the `occurrences[0]!=off` test with a comparison against `off + span.find(quote)`, and compute the expected span as `form[off:off+len(span)]`. Under that reading the pinned builder's bytes satisfy `CAPTURE_BIND`, `SPAN_BYTES` and `REBUILD` at once. Equivalently, accept the builder's manifest as-is and drop the offset-equality test for a `span.find(quote)`-based check. Either change must be made by the L1 against a re-frozen counter.

## 5. Evidence hygiene

- No lane file created, modified or deleted by this seat; `git status --porcelain` shows only `?? .ufo/waves/round-58/` (pre-existing wave directory holding sibling reports). This report is the sole lane write. The lane HEAD moved to `5da0a63` during my run — a sibling's integration commit, not mine; no commit, push or git mutation was performed in the lane.
- All probing was under `/fast/scratch/hyaku/chousa-r58/R58ExecC2Check/` (mirrors `m2`, `m3`, `ng`, `nogit`; work dirs `wA`–`wD`). No `/tmp` evidence. Scratch removed after the run. No live-target fetch; only the lane-owned committed capture was read. Tooling: no install or update requested or performed; `/home/vgpnk/.omp/agent/RULES.md` was read and its channel order was not exercised because nothing needed installing.
- Unrun checks (marked unrun, not inferred): `c1-count.py`, the full `research-gate.sh` census and `quote-substance-check.py` standalone were not run; I did not test whether the L1 prefers a counter rewrite over a builder change; and I made no live re-fetch of the S101 URL.

VERDICT: The attack — running the frozen `c2-count.py` against a scratch mirror holding only the committed S101 capture, the registry and the frozen quote set — **survives**: the counter correctly rejects the base state, `ERROR ENTRY_MISSING` first, `C2=FAIL`/exit 1, byte-identical to the lane's own `c2-before-frozen.txt`. But the converse probe **falsifies** the frozen C2 predicate: `CAPTURE_BIND` (manifest `offset` must equal the quote position) and `REBUILD` (manifest must be byte-identical to the pinned builder, which writes `offset = quote_pos-80`) are mutually exclusive for all 12 frozen quotes (`min(quote_pos)=315`), so **no C2 artifact can reach `C2=PASS`** under the frozen counter and frozen builder. Three supporting defects (provenance-trio strictness, a U+FF0C quote-character trap in the entry, and a `NEW_GROUND` grep on the wrong 載/载 character form) and one cross-claim coupling (an in-place C1 edit to `tools/build-spans.py` breaks C2's `BUILDER_PIN`) are documented above as evidence, not as fixes.
