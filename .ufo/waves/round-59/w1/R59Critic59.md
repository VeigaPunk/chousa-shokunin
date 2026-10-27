# R59Critic59 — falsification review (calibration)

Lane HEAD at review: `026174e` ("round-59: preserve partial unadjudicated evidence"). Read-only; scratch `/fast/scratch/hyaku/chousa-r59/R59Critic59/` (removed before yield). No lane/source writes, no installs, no network. This replaces an earlier draft of this report that only covered round58.

## 0. Provenance gap
`corpus/evidence/round59/claims.md` does not exist in the working tree or at HEAD (`git ls-tree` of `corpus/evidence/round59` lists census-start/end, controls/c1-before.txt, quarantine-*.txt/tsv, s101-open.txt). No frozen round59 claim text exists to attribute. The only proposed round59 verdict-path material is (a) `controls/c1-before.txt` + the unchanged round58 counter, and (b) the committed `quarantine-*` verdict outputs. I attack both.

## 1. Counterexample A — frozen C1 counter's positive path is unreachable (re-verified from committed bytes)
`corpus/evidence/round58/c1-count.py` sha256 `65da18bb…703d3f` (matches the frozen digest; counter unchanged since commit `9e73a03`).
- L51 `PASS = "pass"`; refusal legs are emitted as `f"{name}={PASS}(refused)"` (L160, L223, L234) → `FOREIGN=pass(refused)`.
- L391 `ref_pass = all("=PASS" in l for l in ref_legs)` and L399 `REFUSE=sum('=PASS' in l …)` look for UPPERCASE.
- Consequence: `ref_pass` is False for every builder (even one whose 7 refusal legs all print `=pass(refused)`), so `verdict = "PASS"` (L394) is unreachable. `C1=PASS` can never print. (Sibling audit R58ExecC1CounterAudit reports a scratch reproduction `REFUSE=0/7 → 7/7` after lowercasing; I verified the source mechanism directly, did not rerun.)
- Second fail-open: L392 `denied_pass = (denied == total) if total else True`. `controls/c1-before.txt` shows `DENIED=0/0` — zero do-nothing controls were executed and the denial gate still counted as satisfied. Combined with the above, the control suite neither proves a positive path nor proves refusal-of-do-nothing.
- Impacted axes: calibration (verdict path cannot calibrate; a "before" receipt of `C1=FAIL` is non-informative because the counter fails every builder), operability (no usable gate).
- Smallest safe correction: one comparison constant (`PASS`) used in L391/L399; make `denied_pass` require `total > 0`; then require a positive fixture that prints `C1=PASS` exit 0 plus the REFUSEALL/pinned-r55 controls failing it, all with exact committed bytes.

## 2. Counterexample B — quarantine verdict `absent` ("refuse, fabrication class") is false for committed rows
Tool: `tools/quarantine-check.py`; evidence `quarantine-verdict-lane.txt` (14 `absent`, 10 `unverifiable`). I re-ran its own `parse_register` + `cache_doc` (read-only import) and compared each quote against the local capture under a punctuation/whitespace-insensitive match (NFKC, lowercase, strip `\W_`):
- **S108** (`b502d4c6…txt`): quote *"The claims are classified as Supported, Refuted or NotEnoughInfo by annotators achieving 0.6841 in Fleiss κ."* The capture contains the sentence verbatim except an HTML→text artifact: `…0.6841 in Fleiss κ \kappa .` (MathML alt-text duplicated). The sentence is present; verdict `absent` = fabrication class is wrong; capture-rendering defect, not quote defect.
- **S080** (samr GB/T 7714-2025): quote joins table cells `标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01`; capture holds all three label/value pairs separated by newlines (full match after stripping punctuation).
- **S088** (PDF GB spec): quote `磁带（ｍａｇｎｅｔｉｃ ｔａｐｅ）ＭＴ / 磁盘…` — all five items present in order in the `pdftotext -layout` capture; the strict fold fails only on the editor's ` / ` joiner and column spacing.
- **S084 quote 1**: bullet list present, separated by `・` and newlines. Quote 2 is *not* fully present (22/…), so S084 should be `mixed`, not `absent` (rule: 0<located<n).
- Many other `absent` rows have 80–90% of 12-char shingles present (S093 70/83, S094 51/62·68/77·80/89, S110 76/87·72/87·71/92, S116 65/87·71/89, S112 36/41), i.e. near-verbatim with layout/hyphen/ellipsis/∼ differences — the same class of mismatch. Only S111 (0/7), S105 q2 (0/38), S114 q2 (0/10), S082 (4/27) show genuinely low overlap.
- So the frozen decision rule (strict NFKC+whitespace only counts as "located") maps "capture-rendering/join mismatch" onto `absent` = fabrication. Of 14 `absent` verdicts at least 3 (S080, S088, S108) are demonstrably containing the cited content, and ≥1 (S084) is mis-binned. The verdict file's reason text ("none of the quote(s) is present… under the eleven folds") is thus overconfident. No negative control (a known-present quote through a table/PDF capture must come out `present`) is committed.

## 3. Counterexample C — `unverifiable (binary office never rendered)` is avoidable for S096
Capture `6dc68fd6b32ce9c8dfcebce8.raw` sha256 `6063a3af…ddd6d9fddf3` is the same raw round58 C2 pinned for S101, and `corpus/evidence/round59/s101-open.txt` is its rendered text. Running `examine_quote` of S096's quote 2 (`根据GB3469规定，以单字母方式标识以下各种参考文献类型`) against `s101-open.txt` → `('exact', True, 336)`. Quotes 1 and 3 contain `…` elisions (would need segment matching). So S096 is at best `mixed`/`present`-after-rendering, not `unverifiable`; the lane already holds a rendering path (`tools/capture-text.py`) that the checker does not use. (For S095/S120/S125 I did not render; their `unverifiable` is untested, not refuted.)

## 4. Defects in the committed receipts
- `quarantine-examine-lane.txt` prints status `no-capture` for S095/S096/S120/S125 with the capture filename column populated — it contradicts itself (capture exists, was just not examined); verdict file says "binary office". Status vocabulary conflates "no capture" with "capture not examinable".
- `quarantine-digests.txt` is a single register line; the verdict/examine-lane outputs depend on 21 captures in `corpus/captures/` whose sha256 are not recorded (the tool's `digests` command lists captures only for the cache passed; the committed digest file came from the default empty `.qcache`). The lane verdict inputs are therefore not digest-bound. Register digest itself matches the live file (`5afe1810…64bad833`).
- `quarantine-examine.txt`/`quarantine-verdict.txt` (default empty cache: every row `no-capture`/`unverifiable cache`) are committed beside the `-lane` variants with no label; a reader can take the vacuous run as the result. Same source rows give opposite verdicts between the two (e.g. S080: `unverifiable` vs `absent`), i.e. the verdict is a function of cache location, not of the source.
- `quarantine-slice-bad-ids.txt` is 0 bytes — that is consistent with no bad ids but it is also what a failed/skipped check produces; no accompanying positive control.
- `census-start.txt` == `census-end.txt` (byte-identical), 5 W04 duplicate-url lines — not a positive control of anything.

## 5. Axes / what survives
- Calibration: A (fatal for any C1 verdict), B (absent → fabrication overclaim; reversible only by labelling rows `absent-under-strict-fold`), C (unverifiable overclaim for S096).
- Operability: A's fail-open denial gate; B's lack of any "known-present passes" control means the tool cannot demonstrate it can say `present` on a table/PDF capture — it has no committed `present` verdict at all (0 present of 24 rows), so the positive path is un-exercised, the same shape as round58's C1.
- Depth: not assessed.

## 6. Smallest safe corrections (recommendations only)
1. Fix `PASS` casing in L391/L399 and require `total>0` for denied; add a positive control that must print `C1=PASS`.
2. Add to the quarantine rule a quote-segment/punctuation-insensitive fold used *only* to demote `absent` to `mixed`/`needs-review` and never to promote to `present`; add a positive control from S108/S088 (known-present text through HTML/PDF capture) that must be `present` or `needs-review`, not `absent`.
3. Record capture digests for the lane cache run; label or drop the empty-cache variants.
4. Render OLE/OOXML captures through the lane's capture-text path before judging, or keep `unverifiable` but state that a rendering exists for S096.

## Limits
No round59 claims.md to test; no scratch run of the C1 counter (source reading only for A); B/C used `quarantine-check.py` internals read-only plus Python string matching in scratch. Report path relative to lane root: `.ufo/waves/round-59/w1/R59Critic59.md`.
