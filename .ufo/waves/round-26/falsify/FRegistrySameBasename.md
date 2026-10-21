# FRegistrySameBasename — C3 same-basename relation attack (round26 attempt1)

Seat `ChousaR26R.FRegistrySameBasename` (scout, author-lane advice only; not an outside judge).
Question: can a registry `used-by` naming `otherdir/same.md` (or any non-exact path ending in
`same.md`) authorize `corpus/knowledge/same.md` under `verify-metadata --registry`?

**Verdict: not falsified.** Gate and oracle refused every same-basename authorization attempt
I tried. A basename-rule mutant run against the same fixtures went clean on 22 of them, so these
fixtures do discriminate.

## Target identity (observed)

- Revision `0e9784bd52eca456b24d0bc40921480a47f91a2b` (from `corpus/evidence/round26-measured-revision.json`;
  `git cat-file -t` → `commit`; lane `HEAD` equal at 2026-10-21T12:56Z). Claim base `ba3333254dd337658a4f25e7a9471f9cf4e4567e` (not re-run).
- Sandbox: `git archive 0e9784bd… | tar -x -C /tmp/chousa-r26-falsify-FRegistrySameBasename/tree` → exit 0.
- `sha256sum tree/tools/research-gate.sh` = `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`.
  This equals the pinned digest. Oracle `round26-registry-oracle.py` = `6b2d135c…1d78`, also equal to the pinned digest.
- Runtime: GNU bash 5.3.20, Python 3.14.8. No tools were installed or updated.

## Code under attack (observed, sandbox tree)

- `tools/research-gate.sh:2488-2497`: `used-by` is split on `,`, each token is trimmed, and leading `./` is
  stripped repeatedly. A token matches only by exact string comparison: `[[ $token == "$entry_path" ]]`.
  Because the right-hand side is quoted, glob characters are compared as literal text.
- `:2509-2521` `metadata_registry_entry_path`: the canonical fd path (`readlink -f /proc/$$/fd/N`, `:2590`)
  is made relative to `registry_root=$(cd "$ROOT" && pwd -P)` (`:2572`). An entry outside the root gets an empty path, which never matches.
- Oracle `round26-registry-oracle.py:110-137`: `entry.resolve().relative_to(root.resolve())` is checked for membership
  in a set of tokens that are trimmed and have one leading `./` removed.

## Commands and exits

| command (cwd `/tmp/chousa-r26-falsify-FRegistrySameBasename`) | exit |
|---|---|
| `bash attack.sh \| tee attack.log` | 0 (the driver always exits 0; read the per-row verdicts) |
| `cp -r tree mut`; `sed` line 2496 → `[[ -n $entry_path && ${token##*/} == "${entry_path##*/}" ]]` | 0 (diff confirmed) |
| `bash attack-mut.sh \| grep … \| tee attack-mut.log`; `grep -c FALSIFIED attack-mut.log` | 0; count `22` |

Artifact hashes: `attack.sh` `533abd79…6e707`, `attack.log` `d1b40b0a…357a2`, `attack-mut.log` `48f2fd35…846bb`.
Each fixture is a one-entry file with `source: S001 …`, `verified-at: 2026-10-20 checked anchor y`, `recheck: 90d`,
then `## Body`. The registry is a single `| id | status | used-by |` table where S001 is `mined`. Each case runs
`bash research-gate.sh verify-metadata ENTRY --root ROOT --registry REG`. The fixture tree has
`r1/corpus/knowledge/same.md` and `r1/otherdir/same.md`.

## Results at `0e9784bd` (gate rc / finding; oracle)

Expected `META_SOURCE_USEDBY_MISSING` (exit 1) for every attack row. All were observed as expected:

| id | entry → used-by token (root `r1` unless noted) | gate | oracle |
|---|---|---|---|
| A01 | `corpus/knowledge/same.md` ← `otherdir/same.md` (**the named case**) | rc1 USEDBY_MISSING | USEDBY_MISSING |
| A02 | ← `corpus/otherdir/same.md` | rc1 | agree |
| A03 | ← `same.md` (bare basename) | rc1 | agree |
| A04 | ← `knowledge/same.md` (suffix) | rc1 | agree |
| A05 | ← `./otherdir/same.md` | rc1 | agree |
| A06 | ← `otherdir/../corpus/knowledge/same.md` (lexical traversal, not normalized per spec) | rc1 | agree |
| A07 | ← absolute `$R/otherdir/same.md` | rc1 | agree |
| A08 | ← `*/same.md` (glob) | rc1 | agree |
| A09 | ← `corpus/*/same.md` (glob) | rc1 | agree |
| A10 | ← `xcorpus/knowledge/same.md` (prefix-glued) | rc1 | agree |
| A11 | ← `Corpus/Knowledge/same.md` (case) | rc1 | agree |
| A12 | ← `corpus/knowledge/same.md/` (trailing slash) | rc1 | agree |
| A13 | ← `otherdir/same.md corpus/knowledge/same.md` (space, not comma) | rc1 | agree |
| A14 | ← `otherdir/same.md; corpus/knowledge/same.md` (semicolon) | rc1 | agree |
| A15 | duplicate S001 rows: first `otherdir/same.md`, second exact — first wins | rc1 | agree |
| A16 | root `r1/otherdir/..` ← `otherdir/same.md` | rc1 | agree |
| A17 | root `r1/otherdir`, entry outside root ← `same.md` | rc1 | **oracle exit 2** (`relative_to` ValueError) |
| A18 | reverse: `otherdir/same.md` ← `corpus/knowledge/same.md` | rc1 | agree |
| A19 | dir mode `r1/otherdir` ← `corpus/knowledge/same.md` | rc1 | agree |
| A20 | dir mode `r1/corpus/knowledge` ← `otherdir/same.md` | rc1 | agree |
| A21 | relative `--root r1`, relative entry ← `otherdir/same.md` | rc1 | agree |
| L01 | `otherdir/same.md` is a symlink → knowledge; entry knowledge ← `otherdir/same.md` | rc1 | agree |
| L02 | entry invoked via the symlink `otherdir/same.md` ← `otherdir/same.md` (resolved to canonical knowledge path) | rc1 | agree |
| L04 | root through symlink `rootlink` ← `otherdir/same.md` | rc1 | agree |

The positive controls were all expected clean (exit 0) and all observed clean, with oracle agreement:
P01 exact; P02 `./`-prefixed; P03 `otherdir/same.md ,  corpus/knowledge/same.md  `; P04 relative root/entry;
P05 root and entry via `otherdir/..`; P06 `otherdir/same.md` names itself; L03 symlinked entry ← canonical path;
L05 symlinked root ← exact path.

Mutant control (QUALITY 17). Under the basename rule, 22 attack rows went clean (exit 0): A01–A11, A13–A16, A18–A21,
L01, L02, L04. Three rows survived, for reasons that do not involve the matching rule:
- A12: the token's basename is empty.
- A17: the entry path is empty because the entry is outside the root.
- E01: a positive row.

All positives stayed clean under the mutant. So the exact-path comparison at `:2496` is what kills same-basename authorization, and a parse error does not explain the kills.

## Findings

- **FRSB-1 (not falsified, high confidence).** The C3 relation `otherdir/same.md` ⇏ `corpus/knowledge/same.md`
  holds at `0e9784bd`, and so do all 24 variants listed above. This supports the spec-v1 correction (exact repo-relative path).
  It is evidence for the relation rule only. It says nothing about citation support or truth.
- **FRSB-2 (gate/oracle divergence, low severity, spec ambiguity).** Fixture E01 uses the token `././corpus/knowledge/same.md`.
  The gate returns clean (exit 0) because its `while [[ $token == ./* ]]` loop strips every `./`. The oracle reports
  `USEDBY_MISSING` because it strips only one prefix. The claims text says "only leading `./` is normalized" and
  does not say whether repeated prefixes count. This does not create a same-basename authorization: after stripping, the
  token is the exact path. L1 should pick one reading and align the other implementation. Running the registry differential on such a token
  would show the disagreement; I did not run `round26-registry-differential.sh`.
- **FRSB-3 (oracle robustness, low severity).** In fixture A17 the entry is outside `--root`. The gate treats this conservatively
  and reports `USEDBY_MISSING`. The oracle exits 2 with `… is not in the subpath of …`. The verdicts agree that the entry is not
  authorized, but a differential that treats oracle exit 2 as a mismatch would flag this row.
- **Observation (inference, not a defect).** When a directory alias resolves to the same inode (L02), `used-by` naming the alias
  path does not authorize the entry, because matching uses the canonical path. That is conservative and consistent with
  "exact repo-relative path".

## Not checked

- Backticked or Markdown-linked `used-by` cells are another seat's population question.
- Registry rows with escaped `\|` in cells.
- Non-ASCII or `%q`-escaped basenames.
- The full selftest, the registry differential, and the c3 probe were deliberately not run, because they are outside this item's bounds.
