# R55ReviewC3Counter — same-sentence audit of R55-C3 (counter vs claims vs code)

Audited `corpus/evidence/round55/c3-count.py` (265 lines, committed at freeze `1fc5d92`, unchanged
since: `git diff --stat 1fc5d92 HEAD -- <file>` empty) against the frozen C3 predicate in
`corpus/evidence/round55/claims.md`, then ran it and reproduced every stored receipt. Fixture roots
were `git archive dba605de` copies under my scratch; nothing in the lane was written.

Tooling: nothing installed (no need; stock python3/soffice/git). All runs under
`TMPDIR=/fast/scratch/hyaku/chousa-r55/R55ReviewC3Counter`, `PYTHONDONTWRITEBYTECODE=1`, each with
`--work <fresh empty dir>`; no `soffice.bin` survived (final `pgrep -u $USER -af soffice.bin` empty).

## Same-sentence check

Predicate body of the docstring (c3-count.py:3-19) vs claims.md C3 frozen predicate, whitespace-
normalized: **IDENTICAL** (word-for-word diff empty). ITEMS table (:71-82) vs claims items:
11/11 — ids, targets (r36→source-type-taxonomy-r36.md, QUALITY.md, lessons/round-54.md,
round54/c1-supplement.py) and key phrases all match.

## Per-item observation audit (observe(), :142-204)

| item | computes (line) | source bytes | matches item? | deterministic |
|---|---|---|---|---|
| E01 | count+char of 该标准暂无全文，请等待更新 in S122 (:145-147) | S122 `.txt`, universal newlines | yes | yes |
| E02 | char offset of 主管部门为 国家标准委 in S121 (:148-149) | S121 `.txt`, pin `4e46154f4a841d17d858` verified against disk | yes | yes |
| E03 | 4×count 附录/文献类型 both forms (:150) | both captures | yes | yes |
| E04 | count 国家标准委 both forms (:151) | both captures | yes | yes |
| E05 | 6 anchors located in defined OLE form via BASE capture-text.py (git show), drift vs stated (:152-157) | pinned raw `6063a3aff7a4081e93a6` (raw_bytes :135-140) | yes; the 6 hardcoded anchors = the stated offsets (BASE QUALITY holds `11,972 / 12,007 / 12,963 / 12,795 / 14,049 / 25,123`) | yes |
| E06 | 3 C0 counts of UTF-16LE decode (:158-161) | pinned raw | yes | yes |
| E07 | C0+LF of defined form (:162) | BASE tool output | yes | yes |
| E08 | BASE pointer-anchor-check on git-archive mirror, two dumps deleted, last ANCHORED= line (:163-177) | BASE bytes | yes | yes |
| E09 | ctypes `CDLL(None).system()` under BASE c1-count.py HOOK; rc+marker (:178-190) | BASE bytes, self-run probe | yes | yes (2 runs identical) |
| E10 | first `^LEGS=` in `## shell` block of BASE c1-controls.txt (:191-193) | BASE bytes | yes; committed block has exactly one, `LEGS=1/6` (line 43) | yes |
| E11 | last SUPPLEMENT_LEGS of BASE c1-supplement.py --tool echo --seed 11 --per-leg 2 (:194-204) | BASE mirror + ECHO tool (never opens the `.doc`, :93-101) | yes; soffice genuinely exercised (RESAVE/HELDOUT legs) | yes (2 full runs OK) |

Independent cross-check: loaded the module, called `observe()` directly, compared E01-E10 to the
W2-reported observation column of `controls/build-c3-controls.py` — **10/10 MATCH** (E11 validated
by the passing full runs). The counter recomputes exactly what W2 reported.

## Runs (commands + observed)

- Live tree, full: `python3 corpus/evidence/round55/c3-count.py --work $S/w-full` → `ERRATA=11/11
  MISSING=0 ANCHOR=0 WRONG=0` / `C3=PASS` / exit 0 — **reproduced twice**, identical.
- Before: same with `--root $S/before-root` (BASE archive, no errata block) → 11×`MISSING`,
  `ERRATA=0/11 MISSING=11`, `C3=FAIL`, exit 1 — byte-matches `controls/c3-before.txt`.
- `python3 corpus/evidence/round55/controls/build-c3-controls.py $S/c3c` → `restate paraphrase`;
  restate (full run) → 11×`WRONG`, `ERRATA=0/11 WRONG=11`, exit 1; paraphrase → 11×`ANCHOR`,
  `ERRATA=0/11 ANCHOR=11`, exit 1 — both byte-match `controls/c3-controls.txt`.
- `--skip-slow` on live tree → `E11 WRONG (slow item skipped)`, `ERRATA=10/11`, exit 1 — cannot
  pass, as documented.
- Non-empty `--work` → `usage: --work must be empty`, exit 2.

## Parser enforcement (errata :206-218, main :221-256; fixtures on BASE-tree copies)

- Only inside `## Round 55 statement errata`: any `## ` heading closes the section; lines before the
  first heading and under `## Unrelated section` ignored → MISSING (fixture a3). PASS.
- Last line per item wins: bad-then-good → OK, good-then-bad → WRONG (a1/a2); across two errata
  sections, later section's line governs (a8). PASS (:217 dict overwrite).
- Target must equal the item's target (`tgt != target` → ANCHOR): typo'd target → ANCHOR (a6). PASS.
- Anchor must contain the key phrase (`keyp not in anchor` → ANCHOR): anchor without key → ANCHOR (a4). PASS.
- Anchor must occur exactly once in the target **at the counted tree** (`ttext.count(anchor) != 1`,
  working tree of `--root`): duplicated anchor appended to the fixture target → ANCHOR (a5). PASS.
- Column-0 anchored `^erratum:`: indented line silently ignored → MISSING (b10). Enforced.
- Unquoted observed → line unmatched → MISSING (b9). Enforced (fail-safe direction).

**No named clause is unenforced.** The one predicate clause with no code behind it: "appended" —
an erratum line placed anywhere inside the section (even above its own statement) counts; only
anchor-once prevents rewriting the statement away.

## Findings

1. MEDIUM — S122 capture unpinned: `S122 = ("b9ca2a4fdf9455867534f144.txt", None)` (:66);
   `cap_text` (:116-124) checks the digest only when a pin exists. E01 and the S122 halves of
   E03/E04 would silently recompute from mutated capture bytes; the docstring's exit-2 "capture
   digest changed" (:49) holds only for S121/S101RAW. Actual S122 sha256 prefix on disk:
   `2d68faf7c724eb1baca6c201`. Safe direction (drift → WRONG → C3=FAIL, never a false PASS), and
   the cache is read-only, but the env guard is asymmetric.
2. LOW — "appended" position unenforced (see above); also a malformed/unparseable line is
   indistinguishable from an absent one (MISSING either way, no diagnostic).
3. INFO — greedy `(.*)` in LINE_RE (:92) tolerates inner quotes and splits at the LAST
   `" observed: "`; a line with an extra `observed: "…"` clause is accepted with the trailing value
   as the observation. Deterministic; a false OK still requires the parsed anchor to contain the key
   and occur once and the parsed observation to equal the recomputed one — no soundness hole.
4. INFO — E10 takes the first LEGS line of the shell block; the committed block has exactly one, and
   the source is pinned at BASE bytes, so this cannot drift.
5. INFO — E11's legs are judged through the deterministic echo tool though soffice does the
   generation; two full runs (4.3 s, 8.5 s wall) agreed at `oracle-echo SUPPLEMENT_LEGS=3/3`.

Residual risk: a mutated read-only S122 capture (finding 1) would masquerade as errata drift; pin
it in a future frozen revision. Verification gap: ENV_CHANGED exit-2 paths for pins were code-read,
not fired (firing them would require mutating the forbidden read-only cache).

VERDICT: attacked R55-C3's counter sentence-by-sentence and run-by-run — docstring equals the frozen
predicate, all 11 observations compute what their items name from BASE bytes/pinned captures
deterministically (10/10 == W2 reports), every stored receipt reproduced (before MISSING=11, restate
WRONG=11, paraphrase ANCHOR=11, live 11/11 PASS ×2), parser enforces section-scope/last-wins/
target/key/anchor-once; sole real defect is the unpinned S122 capture, plus the unenforced
"appended" position — no false-PASS path found.
