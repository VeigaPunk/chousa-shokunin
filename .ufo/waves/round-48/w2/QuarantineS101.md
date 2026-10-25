# Quarantine hand-check — chousa register row S101

Row under check: `.ufo/waves/round-48/assimilation/quarantine-slice` line 22
(`S101`` ` `the gate block named no locator, so no quote was checked`), matching
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:270`
(`| chousa | round3 | S101` | the gate block named no locator … | #### Gate — S101 |`).

## Verdict: **PRESENT** (register's "no locator" basis falsified by local bytes)

## What the row actually attests (as committed when the lint ran)

The lint input was `lanes/chousa/round3/SOURCES-PROPOSED.md` at shokuknow commit
`9e91e504` (2026-10-24 06:38; the file was edited again at 23:26, S-ids shifted).
At that revision, `#### Gate — S101` (confirmed by `git show 9e91e504:…`) reads:

- `URL (repository locator): https://github.com/VeigaPunk/shokunin`
- `Local artifact: \`chousa-shokunin/corpus/knowledge/citation-chain-fidelity-r24.md\``
- `Opened: 2026-10-23 … sha256 is the content pin`, 4 `Quote —` lines.

So a locator **was** named — twice. Two checker mechanics produced `no-locator`:

1. `quote-lint.py` `URL_LINE_RE` (`^\s*[-*]?\s*(?:URL|url|Source|Locator)\s*[:=]\s*(\S+)`)
   demands `:`/`=` immediately after `URL`; `URL (repository locator):` has a
   parenthetical between, so `block_url` returned None (quote-lint.py:323–335).
2. `local_locator` (quote-lint.py:351–374) tries `Path(raw).exists()` then
   `lane_dir/raw`; `chousa-shokunin/…` is rooted at `~/Projects/shokunin/`, not
   at the lint CWD (`shokuknow`) or `lanes/chousa/`, so both probes missed and
   the finding `verdict: "no-locator", detail: "#### Gate — S101"` was emitted
   (quote-lint.py:786–788 → quote-lint-full-v4.json & v5.json, identical detail).

## Local byte evidence (ran today; no fetch)

Artifact: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/citation-chain-fidelity-r24.md`
`ls -la` + `wc -c` + `sha256sum`: **8,931 bytes**, sha256
`b4e5d36cafde9250f4701dd437504ffa7a777cb69766b50dc6a9bca2e7203b72` — byte length
and sha256 prefix `b4e5d36cafde9250` match the registry row's declared anchor
exactly (SOURCES-PROPOSED S101 row, `9e91e504`; also worktree line 31 under S106).

Quote check (`python3`, `str.find` on UTF-8 text; offsets = char / byte):

- Q1 `## Claim` (heading at char 1046): "A `faithful` disposition requires a
  per-hop comparison of the relayed claim against that hop's own source text
  (proposition, scope, quantity, hedge, date); a hop whose anchor resolves but
  whose relay was never compared stays `resolved-unchecked`" — **present,
  char 1274 / byte 1291**, 245 chars exact.
- Q2 `## How chousa applies it` (char 3020): "Per-hop fidelity checklist — at
  each `resolved` hop, compare the relay text against the source text the
  anchor landed on" — **present, char 3046 / byte 3082**, 120 chars exact.
- Q4 `## Limits` (char 4515): "Observation: `verdict=match` is byte existence
  at token boundaries; semantic comparison stays outside the mode by design
  (chain-resolution-r3.md:258)." — **present, char 4931 / byte 4998**, 150 chars.
- Q3 `## Limits`: "Unknown: no lane-local fidelity measurement exists —
  verify-chain has no semantic arm, and the checklist's error rate on real
  chains is unmeasured this round." — **present, char 5084 / byte 5151**, 158 chars.

4/4 quoted spans verbatim-exact, 0 ABSENT. The repository-URL half of the
locator pair is unchecked (no fetch permitted; L0 `8d77e6c1` open) but is a
tree-locator only — the row itself declares the artifact untracked and pins
content by sha256, which matches.

## Reason

The register's "no locator, no quote checked" is a checker artifact: locator
was named but mis-parsed (parenthetical `URL (` label; repo-root-relative path
probed from the wrong CWD). Per the hand-check rule, local byte evidence
resolves the row → **present**, not unverifiable. This row's quarantine
rationale is falsified; the "no-locator" population of the 24-row slice
(S100–S103 share identical `URL (repository locator)` + lane-tree `Local
artifact` blocks, quote-lint detail strings confirm) inherits the same
mechanism — each sibling still needs its own byte check.

Caveat for grading calibration: `kind: own-work`, so PRESENT asserts only that
the local artifact exists and holds the quoted spans byte-exactly — not that
the entry's claims about the world are true. "Present" here = present-as-written
in the attested source.

## Commands run

- `grep -n "S101" …/absent-defect-register.md` → line 270 (row), line 68
  (unrelated `game-dev-2d` S101).
- `git -C /home/vgpnk/Projects/shokuknow rev-list --all -- lanes/chousa/round3/SOURCES-PROPOSED.md`
  → 9e91e504 (2026-10-24 06:38, rev current at v4/v5 lint times 06:29/08:05).
- `git show 9e91e504:lanes/chousa/round3/SOURCES-PROPOSED.md` → table row S101
  + `#### Gate — S101` block quoted above.
- `sha256sum`, `wc -c` on artifact → 8931 bytes, `b4e5d36cafde9250…`.
- python `str.find` per quote → offsets above; all ≥0.
- `sed -n` on `quote-lint.py` lines 61–66, 323–335, 351–374, 776–788 →
  parse/resolve/no-locator emission mechanics cited.

## Remaining unknowns

- Whether `github.com/VeigaPunk/shokunin` still serves a matching tree (not
  fetchable this wave; row declares it non-binding anyway).
- Whether the checker-fix itself (URL label / CWD anchoring) is already tracked
  elsewhere — outside this row's scope.
