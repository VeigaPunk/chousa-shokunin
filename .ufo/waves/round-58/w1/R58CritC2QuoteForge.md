# R58CritC2QuoteForge — hollow C2 attack

## Result

**The frozen predicate does catch more than a quote-pasted/template-only entry, but the frozen builder/counter offset contract appears internally incompatible.** I could not honestly claim a runnable hollow-entry pass: a builder-generated manifest cannot satisfy the counter's capture-offset check for these quotes. Independently, even if that mismatch is repaired, the counter does not establish that an entry's prose entails or correctly explains the quotes; its own called checker explicitly disclaims entailment.

## Frozen evidence read

- `corpus/evidence/round58/claims.md` lines 13–21 defines C2 as source-grounded carrier alphabet vs carrier identifiers / `[type/carrier]` notation / distinct document-code field; it freezes 12 exact quotes, S101 URL/raw digest, builder/capture pins, and requires `C2=PASS` with rebuild, registry binding, substance, and inference checks.
- Exact `corpus/evidence/round58/c2/quotes.tsv` header is `id\turl\tquote\tentry`; it has 12 S101 rows, all pointing at `corpus/knowledge/carrier-alphabet-china-r58.md`.
- Re-opened `corpus/evidence/round58/c2-count.py` lines 99–115, 116–135: each manifest `offset` must equal the quote's actual occurrence offset in defined capture text; span bytes must match the context slice; quotes must be in entry; anchors >=3; all 12 rows bound.
- Re-opened pinned `tools/build-spans.py` lines 139–149: it computes quote offset `off`, context start `start=max(0, off-80)`, but writes `str(start)` in manifest's `offset` field. This is the mismatch.

## Executed evidence

Verified frozen hashes with:

```text
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && sha256sum tools/build-spans.py tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw
```

```text
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py
2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  tools/capture-text.py
6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3  corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw
```

Ran the pinned builder in a disposable scratch directory (copied only the committed raw capture there; no lane writes/network):

```text
TMPDIR="$S" PYTHONDONTWRITEBYTECODE=1 python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py --quotes /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c2/quotes.tsv --out "$S/out" --cache "$S/cache"
```

Observed `SPANS_ROWS=12 WRITTEN=12`; builder diagnostics report quote character offsets `315, 330, 590, 683, 734, 781, 797, 838, 965, 993, 1460, 11723`. The first manifest offsets are `235, 250, 510`, exactly 80 less than those quote offsets. The first quote is not at capture start, so it already fails counter condition `occurrences[0] == off` (235 != 315); likewise other interior quotes. **I did not run the full C2 counter** because constructing a lane-copy would exceed this leaf assignment's permitted work; no `C2=FAIL` output is claimed. The source-level mismatch plus directly observed builder output is the evidence.

## What the counter catches / misses

Catches (when reachable): exact frozen quote-set/order and rows; URL/raw digest and unique exact offsets; presence of every quote string in entry; span-byte/context consistency; builder byte-rebuild; source-trio/registry `used-by`; stray S IDs; >=3 anchors; absence from base/presence of new ground; minimum quote-size floor; and lexical inference grounding. The quote-substance checker requires non-whitespace content and at least one >=12-character quote per ID, but explicitly says it is **not an entailment check** (`corpus/evidence/round51/quote-substance-check.py` lines 7–14).

Misses: an explanation can be misleading or wrong while copying all required quotes, source headers, and mechanically grounded inference tokens. `tools/inference-ground.py` lines 5–10 and 64–72 explicitly say it checks lexical presence, not meaning; lines 168–179 and 559–595 require each inference bullet to cite a source and contain grounded tokens, not to explain the claim correctly. Thus template-only observation prose (or an unrelated assertion paired with an exact grounded quote) can pass that checker. The frozen C2 predicate's wording that checks pass does not turn lexical grounding into entailment. This is a real quality limitation, separate from the offset incompatibility.

## Smallest safe correction / axes

- **Depth (C2):** do not accept a PASS until the frozen offset contract is reconciled: either builder writes quote offsets (and consumers expecting span starts are updated consistently), or counter compares its quote offset to the manifest's documented span-start convention. Re-freeze before scoring; do not silently patch this frozen round. Then require a human entailment/readability assessment or a narrowly specified semantic criterion; the existing lexical checker cannot certify the carrier-vs-document-code distinction.
- No claim-verdict authority; L1 integrates. No live fetch; no lane evidence/predicate files modified. Scratch was removed by shell trap.

VERDICT: The hollow-explanation attack is **inconclusive as an end-to-end C2 bypass** because the frozen builder's emitted offsets conflict with the frozen counter's required quote offsets; the counter's semantic/entailment blind spot is substantiated by its own checker contract.