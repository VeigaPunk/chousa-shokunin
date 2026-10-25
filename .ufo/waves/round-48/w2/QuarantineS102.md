# Quarantine hand-check — `chousa` register row S102 (W2 falsification)

## Verdict: **PRESENT** (the register's "never checked" reason is a checker defect, not missing evidence)

Register row (shokuknow `.ufo/waves/corpus-expansion-1/absent-defect-register.md:271`,
in "Rows whose quotes were NEVER CHECKED", rows: 109):

```
| `chousa` | round3 | S102` | the gate block named no locator, so no quote was checked | #### Gate — S102 |
```

Slice row (chousa-shokunin `.ufo/waves/round-48/assimilation/quarantine-slice:23`): `S102` — same
"gate block named no locator" class.

## Row identity (resolved through two renumbers)

- Checker's tree state = shokuknow commit `9e91e504` (2026-10-24 06:38 -0300, "Round 8 complete");
  lint run `quote-lint-full-v5.json` 2026-10-24T08:05; register written 08:37.
- At that commit, `lanes/chousa/round3/SOURCES-PROPOSED.md` line 32 = **S102, "chousa exempt-hop
  audit entry"**, and lines 54–61 hold `#### Gate — S102`.
- The lane was renumbered **again** at 2026-10-24T23:26 (+5 for this round), so on disk today the
  same row is **S107** (`lanes/chousa/round3/SOURCES-PROPOSED.md:32` → gate block lines 54–61; the
  merge package `merge/chousa/SOURCES.append.md:32` also labels it S107). The +5 mapping is
  independently confirmed by every other chousa round3 register row
  (reg S104→disk S109 jstage, S105→S110 jaohfa, S108→S113 arxiv 1803.05355, S110→S115 coling).
- The unrelated `Gate — S102` in `lanes/chousa/round2/SOURCES-PROPOSED.md:113` (CNKI KNS8.0 guide,
  register round2 S097, folded/pass) is a different row in the same id space.

## Local byte evidence

Artifact: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/exempt-hop-audit-r32.md`
(row's declared pin: "sha256 prefix fdc55c65d8ed94c5, 3,515 bytes").

```
$ sha256sum exempt-hop-audit-r32.md
fdc55c65d8ed94c585575a58969e9fc79a377044f6d7202ac70eea3cfd5f91e2
$ wc -c → 3515        (prefix + length both match the row's declared pin)
$ git ls-files → corpus/knowledge/exempt-hop-audit-r32.md   (tracked; the gate block's
  "untracked in the repository" parenthetical is stale — cosmetic, the pin is what binds)
```

Quote verification (checker-time gate block, commit `9e91e504` lines 58–60):

| # | Quote | Result | Byte span |
|---|-------|--------|-----------|
| "The audit" | `For hops marked … the record drifts.` (365 B) | match after whitespace fold (md line-wrap inside span) | 1455–1820 |
| "Limits" | `URL sources stay unread, so a hop marked …` (91 B) | **raw-byte exact** | offset 3273, 3273–3364 |
| "The gap" | `a record could say … "exemption is record-declared and unverifiable"` (179 B) | match after whitespace fold | 745–924 |

Whitespace folding is the lane's sanctioned normalization (`round2/SEARCH-LOG.md:116` records
"line-wrap inside the quoted span … whitespace normalisation resolves it").

## Why the checker reported "no locator" (mechanism, reproduced)

The gate block *does* name two locators: `URL (repository locator): https://github.com/VeigaPunk/shokunin`
and `Local artifact: \`chousa-shokunin/corpus/knowledge/exempt-hop-audit-r32.md\``.

1. `quote-lint.py:66` `URL_LINE_RE` requires the label to be followed directly by `:`/`=`
   (`(?:URL|url|Source|Locator)\s*[:=]`); `URL (repository locator):` fails — verified:
   `URL_LINE_RE.search(body)` → `None`. Fallback needs an `https?://` in the row's `source` cell;
   this row's source cell is a lane-local path, so `block_url` returns `None`.
2. `local_locator()` (quote-lint.py:348) does extract the backticked path
   `chousa-shokunin/corpus/knowledge/exempt-hop-audit-r32.md`, but resolves it only against
   `lane_dir` = `shokuknow/lanes/chousa/` — where it does not exist — never against the actual
   repo root `/home/vgpnk/Projects/shokunin/`. Verified: `lane_dir / raw` → absent; the real file
   exists. Cross-repo relative paths are structurally unreachable for this checker.
3. `absent-defect-register.py` then renders `detail=head[:80]` — the literal heading —
   into the "cited source" column, so the register's `#### Gate — S102` is not a locator at all,
   just the truncated finding detail.

## Residual risk / gaps

- The earlier `quote-lint-full.json` (03:32) lists two `chousa round3 S102` **folded** findings at
  `chinagp.net`; that binding was pre-recheck (v4/v5 corrected it to `no-locator`). It does not
  change the byte-level verdict: the three gate quotes are present in the pinned artifact.
- No live fetch performed (forbidden); the repository URL `github.com/VeigaPunk/shokunin` itself is
  unverified, but the operative locator is the local artifact, which is verified byte-exact.
- Classification for the register's purpose: the "never checked" section entry is a false
  unverifiable — byte evidence resolves it to **present**, same pattern the tool's own docstring
  admits for tabi round-8 receipts ("the evidence for its … rows — were all in that blind spot").

Report: `.ufo/waves/round-48/w2/QuarantineS102.md`
