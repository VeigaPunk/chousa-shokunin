# ScoutExemptCorpus32 — C2 no-harm recon

Verdict: **no record in this scope would flip CLEAN→DRIFT under C2.** Every U hop (`unresolved` / `blocked-no-fetch` / `labelled-dead`) that carries a citation fails the gate's own resolved path (invalid citation or anchor-missing). None would print `observed=verified`, so none would become `observed=resolvable` / `FINDING CHAIN_EXEMPT_RESOLVABLE`.

C2 rule used (`corpus/evidence/round32/claims.md` C2 contract; `tools/research-gate.sh` `verify_chain` resolved arm `1827-1878`, exempt arm `1880-1882`, `chain_citation` `1646-1686`): a U hop drifts only when the same row with status `resolved` would verify (citation parses; source is a declared id with a pointer or a local path inside the boundary; `chain_anchor_at` finds the anchor). Invalid, refused, and anchor-missing stay exempt.

Gate actually run: `tools/research-gate.sh` SHA-256 `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258` (matches `claims.md`). No `c1-count.py` / `c2-count.py`. No installs. Lane files not modified. Counterfactual copies: `/fast/scratch/hyaku/chousa-r32/w1/ScoutExemptCorpus32/gate-probe/`. Notes: `.ufo/waves/round-32/w1/ScoutExemptCorpus32/probe-notes.txt`.

Scope check: `corpus/**/*.md` has 19 `## Chain` sections (python line match `^## Chain`). `research/` and top-level `fixtures/` do not exist (`ls`: No such file or directory). No corpus chain row has status `labelled-dead`.

## Corpus hops (U + a citation)

"Citation" here is a non-empty `to` and/or anchor cell. Resolvable? = base gate on a scratch copy whose **only** change was that hop's status cell → `resolved`, invoked as `timeout 120 bash tools/research-gate.sh verify-chain <copy> --root /home/vgpnk/Projects/shokunin`.

### `corpus/fixtures/chain-r3.md` lines 43-47 — would NOT flip (stays 17/22 CLEAN)

Unmodified: `CLEAN (hops=22 verified=17 exempt=5 ...)`.

| hop | status | to | anchor | if status were `resolved` | C2 |
|---|---|---|---|---|---|
| 18 | blocked-no-fetch | `https://kotobank.jp/` | kind `-`, text `-` | `observed=invalid` (`anchor_kind=- not in heading\|quote\|line`) | stays exempt |
| 19 | blocked-no-fetch | `https://arxiv.org/` | kind `-`, text `-` | `observed=invalid` (same) | stays exempt |
| 20 | unresolved | S3 → `research/deep-research-2026-09-28/C-rank-taxonomy.md` | quote `人為 — jin’i-ryū` | `observed=anchor-missing` nearest_line=53 | stays exempt |
| 21 | unresolved | S2 → `.../B-multiagent-knowledge.md` | line `When to split a domain into a new specialist` | `observed=anchor-missing` nearest_line=- | stays exempt |
| 22 | unresolved | S1 → `.../A-shokunin-tradition.md` | quote `Minarai → Shokunin with a self-iteration license` | `observed=anchor-missing` nearest_line=- | stays exempt |

Reading behind 20-22: C:118 is `人為 — jin’i` plus a tab and "Human action...", not `人為 — jin’i-ryū` (`C-rank-taxonomy.md:118`). B:35 contains the lowercase words inside a long prompt line, not as one whole line (`B-multiagent-knowledge.md:35`); kind is `line`. C:69 has `Minarai → Shokunin → Shokunin with a self-iteration license`, a different string, and the hop cites A, not C (`C-rank-taxonomy.md:69`). Flipped run kept `RESOLVED_HOPS=17/22` (the other 17 still verified).

### `corpus/fixtures/sweeps-r5.md:29` — would NOT flip (stays 2/3 CLEAN)

Hop 3 `blocked-no-fetch` to `https://kotobank.jp/`, kind `-`, anchor `-`. Unmodified: `observed=exempt`, `CLEAN (hops=3 verified=2 exempt=1)`. Flipped: `observed=invalid`, `anchor_kind=-`. Same shape as chain-r3 hop 18.

`sweeps-r5-broken.md` chain has one hop, status `resolved` only (`:24`). No U hop.

### `corpus/knowledge/archived-export-intake.md:68-70` — U hops would NOT become resolvable

Table is `hop | status | to | notes` (no anchor column), `:63-70`.

| hop | status | to | if `resolved` |
|---|---|---|---|
| H4 | unresolved | S8 (`research/README.md:10` at `:53`) | `observed=invalid`, `resolved hop missing anchor` |
| H5 | unresolved | `arxiv.org` (not a URL, not an id) | same, missing anchor |
| H6 | blocked-no-fetch | `arxiv.org` | same |

Unmodified verify-chain is **already** `DRIFT (hops=8 verified=0 exempt=4 invalid=4 findings=4)`. The four invalids are the anchor-less `resolved` rows H1-H3 and H8 (`:65-67`, `:72`), independent of C2. H7 is `rejected` (`:71`), outside U, and also has no anchor. C2 would not add `CHAIN_EXEMPT_RESOLVABLE` for H4-H6.

### Archive chip hops — would NOT flip the CLEAN parents

Empty `anchor_kind` and `anchor`. Flipped parent → `observed=invalid`, `resolved hop missing anchor`. Verified counts unchanged.

| record | line | hop | status | to | unmodified |
|---|---|---|---|---|---|
| `corpus/fixtures/archives-r9/A-r9.md` | 42 | 7 | blocked-no-fetch | `コトバンク` | CLEAN 6/7 exempt=1 |
| `corpus/fixtures/archives-r9/B-r9.md` | 43 | 7 | blocked-no-fetch | `arxiv.org` | CLEAN 6/7 exempt=1 |
| `corpus/fixtures/archives-r9/C-r9.md` | 43 | 8 | blocked-no-fetch | `jstage.jst.go.jp` | CLEAN 7/8 exempt=1 |

Not declared source ids (A's Sources are S1-S6, `A-r9.md:25-30`; the chip is a bare token). `chain_citation` fails before path lookup because the anchor cell is empty.

Controls, chip row byte-equal to the parent hop line (compared, `equal=True`; not re-run): `controls/A-r9-span-not-found.md:42`, `controls/A-r9-anchor-missing.md:42`, `controls/B-r9-false-sweep.md:43`, `controls/B-r9-rejection-missing-flip.md:43`, `controls/C-r9-dangling-ref.md:43`, `controls/C-r9-structure-break.md:39`. Same citation → same non-resolvable result. [INFERENCE] from the equal hop line plus the parent gate run. Those controls already DRIFT for their planted non-chain or other-chain defect; C2 would not add `CHAIN_EXEMPT_RESOLVABLE`.

### Chain sections with no U hop (C2 exempt arm cannot touch them)

`corpus/fixtures/chain-r3-broken.md` (hop 2 is `resolved` with the same absent quote as chain-r3 hop 20, `:26`), `sweeps-r5-broken.md`, `full-r6.md`, `full-r6-broken.md`, `full-r6-absent.md`, `integrity-r7.md`, `integrity-r7-broken.md`. The `unresolved` cells in full-r6 / integrity-r7 are Negatives rows, not Chain hops.

## Selftest fixtures inside `tools/research-gate.sh`

Cases that assert `observed=exempt` for a U **chain** hop:

1. **`chain-pass`** `tchain` at `4296-4304`. Fixture hop 5 (`4293`): `unresolved`, to `https://example.invalid/x`, empty anchor, notes `blocked-no-fetch`. Asserts the full line `CHAIN hop=5 status=unresolved observed=exempt source=https://example.invalid/x anchor=- at=- verdict=exempt`, plus `RESOLVED_HOPS=5/6` and `exempt=1`. Empty anchor → `chain_citation` returns "resolved hop missing anchor" (`1675`); a URL would also be `CHAIN_SOURCE_EXTERNAL` (`1181-1184`) if an anchor existed. Not locally resolvable. The assertion stays true under C2. Not executed here (selftest writes `lib/` under `$WORK`); judgment is from the parser and the same missing-anchor result on the corpus URL/chip hops.

2. **`chain-fail-counting`** `tchain` at `4374-4380`. Printf fixture hops 3 `unresolved` and 4 `labelled-dead`, both `to=S1` (`lib/chain_target.md`) with empty anchor cells. Asserts the substring `observed=exempt` and summary `exempt=2` (the case already expects DRIFT: `RESOLVED_HOPS=2/8`, anchor-missing + out-of-corpus + two invalid). Empty anchors → not verified if rewritten to `resolved`. C2 leaves both exempt, so the substring still matches. This is the only `labelled-dead` chain hop in the gate file.

Not `observed=exempt` assertions, but they depend on a U hop staying non-verified:

- **`all-pass`** hop 2 (`4655`): `unresolved`, to S1, empty anchor, notes `blocked-no-fetch`. `tall` at `4754-4761` asserts `SECTION chain ... tally=RESOLVED_HOPS=1/2` and composed `CLEAN`. It does not assert the token `observed=exempt`. Empty anchor → C2 would not flip that section to DRIFT.
- **`pass-hop-marked-unresolved`** (`3841-3870`): structural `tcase`, asserts only `RESEARCH_GATE: CLEAN`. Hop 1 is `unresolved` to `https://example.invalid/x` with notes and no anchor column. Not a verify-chain `observed=exempt` assertion. C2's edit is the exempt arm of `verify_chain`, not this structural case.

Adjacent, not chain-arm (C2 does not change `verify_integrity` / sweeps):

- `integrity-exempt-counted` `4956-4961`: `REF ... section=chain row=1 ... observed=exempt ... status=blocked-no-fetch` for hop `C9 → S7` with empty anchor (`4950`).
- `integrity-fail-counting` `4999`: `REF ... section=chain row=2 ... observed=exempt ... status=unresolved` for hop `C9 → S7` empty anchor (`4974`).
- Sweeps `4493-4495` assert `SWEEP ... observed=exempt` for non-local / source-id / `blocked-no-fetch` sweep rows, not chain hops.

## Limits

Controls were not passed through the gate; only the chip line was compared to the parent. Selftest fixtures were read, not executed. `rejected` / `not-applicable` were excluded (C2 leaves them exempt). No network.
