# Quarantine hand-check — chousa register row S103

Row under check: `.ufo/waves/round-48/assimilation/quarantine-slice` line 24
(`S103`` ` `the gate block named no locator, so no quote was checked`), matching
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:272`
(`| chousa | round3 | S103` | the gate block named no locator … | #### Gate — S103 |`).

## Verdict: **PRESENT** (register's "no locator" basis falsified by local bytes)

## What the row actually attests (as committed when the lint ran)

The lint input was `lanes/chousa/round3/SOURCES-PROPOSED.md` at shokuknow commit
`9e91e504` (2026-10-24 06:38; worktree file re-edited 23:26, S-ids shifted). At
that revision the row reads:

- row (line 33): `| S103 | chousa revision-binding entry —
  corpus/knowledge/revision-binding-r31.md (lane-local artifact) | own-work | A
  | … sha256 prefix 845ea270d8e56b4b, 4,259 bytes, read 2026-10-23 |`
- `#### Gate — S103` block:
  - `URL (repository locator): https://github.com/VeigaPunk/shokunin`
  - `Local artifact: \`chousa-shokunin/corpus/knowledge/revision-binding-r31.md\``
  - `Opened: 2026-10-23 (read from the lane tree; untracked in the repository,
    so the sha256 is the content pin)`, 4 `Quote —` lines.

So a locator **was** named — twice. Two checker mechanics produced `no-locator`:

1. `quote-lint.py` `URL_LINE_RE`
   (`^\s*[-*]?\s*(?:URL|url|Source|Locator)\s*[:=]\s*(\S+)`, line 66) demands
   `:`/`=` immediately after `URL`; `URL (repository locator):` has a
   parenthetical between, so `block_url` returned None (quote-lint.py:323–335).
   The row `source` cell carries a path, not an http(s) URL, so the row-level
   URL fallback also returned None.
2. `local_locator` (quote-lint.py:348–373) probes `Path(raw).exists()` then
   `lane_dir/raw`. Both candidates it can see — `chousa-shokunin/corpus/
   knowledge/revision-binding-r31.md` (the `Local artifact:` line) and
   `corpus/knowledge/revision-binding-r31.md` (the `source`/`anchor` cells) —
   are rooted at `~/Projects/shokunin/`, not at the lint CWD (`shokuknow`) or
   `lanes/chousa/`, and the `Opened:` line's `~/Projects/shokunin/` fails
   `ABS_PATH_RE` (leading `~`, no extension on the last segment). Both probes
   missed, so `verdict: "no-locator", detail: "#### Gate — S103"` was emitted
   (quote-lint.py:784–788) into quote-lint-full-v4.json **and** v5 (identical
   finding in both).

## Local byte evidence (ran today; no fetch)

Artifact: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/revision-binding-r31.md`
`ls -la` + `wc -c` + `sha256sum`: **4,259 bytes**, sha256
`845ea270d8e56b4ba25eb501ee4f252d8fff502967f8143834884a35f8afe86a` — byte length
and sha256 prefix `845ea270d8e56b4b` match the row's declared anchor exactly
(committed S103 row; same anchor carried at worktree line 33 under S108 and in
`merge/chousa/SOURCES.append.md` line 33 under S108).

Quote check (`python3`, `str.find` on UTF-8 text; offsets = char / byte, all
ASCII so identical spacing):

- Q4 `## Why pin the revision`: "A path alone identifies where to look, not
  which contents were read." — **present, char 2385 / byte 2388**, 68 chars.
- Q1 `## Why hash exact bytes`: "The pin covers the whole source file as bytes,
  not a decoded or normalized representation and not just the quoted span." —
  **present, char 2723 / byte 2726**, 119 chars.
- Q2 `## Limits`: "The digest pins content, not a Git commit or repository
  revision. Different commits with identical source bytes have the same content
  pin." — **present, char 3758 / byte 3761**, 138 chars.
- Q3 `## Limits`: "A matching digest establishes byte identity for the checked
  content only. It does not prove that the claim is true, that the span is
  meaningful in context, or that the source itself is correct." — **present,
  char 4062 / byte 4065**, 193 chars.

4/4 quoted spans verbatim-exact, each occurring exactly once, 0 ABSENT. The
repository-URL half of the locator pair is unchecked (no fetch permitted; L0
`8d77e6c1` open) but is a tree-locator only — the row itself declares the
artifact untracked and pins content by sha256, which matches.

## Reason

The register's "no locator, no quote checked" is a checker artifact: a locator
was named but mis-parsed (parenthetical `URL (` label; repo-root-relative path
probed from the wrong CWD). Per the hand-check rule, local byte evidence
resolves the row → **present**, not unverifiable. This row's quarantine
rationale is falsified: the quarantine tag says "no quote was checked," but the
named source exists, matches the sha256 pin and byte length, and contains all
four quotes byte-for-byte.

ID-space note for calibration: the census key `(chousa, round3, S103)` is the
*pre-merge staged* id — the revision-binding own-work row. The merged registry
(`merge/chousa/SOURCES.append.md:28`) names a different artifact "S103" (round2's
澳门科技大學圖書館 CNKI-AI row, renumbered from S100), and this row landed as
**S108** there. The lane's own `ID-REMAP.md` table says round3 `S103`→`S106`,
which matches neither the committed numbering nor the merged one — stale remap
metadata, not this row's problem. The `#### Gate — S103` detail string in both
census versions fixes the census-time reading: staged S103 = revision-binding.

Caveat for grading calibration: `kind: own-work`, so PRESENT asserts only that
the local artifact exists and holds the quoted spans byte-exactly — not that
the entry's claims about the world are true. "Present" = present-as-written in
the attested source.

## Commands run

- `grep -n "S103" …/absent-defect-register.md` → line 272 (row under
  "Rows whose quotes were NEVER CHECKED").
- `git -C /home/vgpnk/Projects/shokuknow rev-list --all --
  lanes/chousa/round3/SOURCES-PROPOSED.md` → 9e91e504 (2026-10-24 06:38, rev
  current at v5 lint time 08:05); `git status` → worktree file ` M` (edited
  23:26, post-lint renumber S100–S110 → S105–S115).
- `git show 9e91e504:lanes/chousa/round3/SOURCES-PROPOSED.md` → row line 33
  (S103) + `#### Gate — S103` block quoted above.
- `sha256sum`, `wc -c` on artifact → 4,259 bytes, `845ea270d8e56b4b…`.
- python `str.find` per quote → offsets above; all ≥0, `text.count(q)==1`.
- `quote-lint.py` lines 60–66, 91–94, 323–373, 784–788 → parse/resolve/
  no-locator emission mechanics cited.
- `locator.py` GATE_LOCATOR_PATTERNS → contract-level confirmation the gate's
  URL/path forms are valid locators the census grammar rejected.
- `python3` over `quote-lint-full-v4.json` / `v5.json` → identical
  `{lane: chousa, round: round3, id: S103, verdict: no-locator, detail:
  "#### Gate — S103"}` finding in both.

## Remaining unknowns

- Whether `github.com/VeigaPunk/shokunin` still serves a matching tree (not
  fetchable this wave; the row declares the URL non-binding anyway — the
  sha256 is the pin, and it matches).
- Why `ID-REMAP.md`'s round3 map (S103→S106) disagrees with the merged
  registry's landed id (S108); a lane-internal metadata defect worth a note,
  outside this row's byte check.
