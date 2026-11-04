# R76Scribe — drafted SOURCES.md registry rows (round 76)

Seat R76Scribe (chousa lane). Draft only — NOT committed; the lane's `corpus/SOURCES.md`
is READ-ONLY for this seat. The L1 (ChousaR76) already drafted S187/S188/S189 in the
worktree; this file is the scribe's **corrected** draft plus its verification evidence.

Schema: the censused 11-column table of `corpus/SOURCES.md` (`id | source | kind | tier |
scope | anchor | teaches | status | opened | recheck | used-by`). No `|` character inside
any cell. Statuses `queued|mined|rejected`; kinds in the census enum; tiers `A|B|C`.

---

## S187 — ADMIT (own-work B)

Source: `corpus/lessons/round-75-verifier-spotcheck.md` — the r75 non-author spot-check,
routed defect 1 (C1 rationale and battery coverage).

Located quotes, re-opened at the anchor revision (fail-closed probe
`.ufo/waves/round-76/w1/R76Scribe/probe-corrected.txt`, exit 0):

- line 125, 14 words: "commit subject, tree ids and byte sizes are stable metadata channels,
  and four content-blind"
- line 127, 9 words: "the twelve-entry declared-order oracle to the battery's subject set"

Anchor: `1af39fed6058ad46fc075b72fddaae838f43273e` (the commit that adds the spot-check;
blob `c53d32c944460213812368d92b8f21527c0b464e` is byte-identical at `da9ac7ec…` and at
`5daa3628…`), lines 124–128.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S187 | chousa round-75 verifier spot-check, routed defect 1 — corpus/lessons/round-75-verifier-spotcheck.md | own-work | B | the r75 candidate-running matrix's surviving metadata answer keys (commit subject, tree ids, byte sizes) and the twelve-entry declared-order oracle the frozen battery did not observe | 1af39fed6058ad46fc075b72fddaae838f43273e (blob c53d32c9 identical at da9ac7ec), lines 124-128, quotes on lines 125 and 127 | A matrix whose case identity is readable from commit subjects, tree ids or byte sizes can be passed without opening a protected file, and a shuffle the battery never exercises leaves the order oracle unmeasured; neutralise the subject, salt the fixture content, and put a metadata reader and the declared-order oracle in the battery's subject set | mined | 2026-11-04 | on-release | corpus/lessons/round-76.md |

## S188 — ADMIT (own-work B)

Source: the same file, routed defect 2 (the C2 counter is a presence test).

Located quote, re-opened at the anchor revision (probe exit 0):

- line 130, 16 words: "polarity and magnitude rather than substring presence, require the
  correction block to be the final section"

Anchor: `1af39fed6058ad46fc075b72fddaae838f43273e` (blob `c53d32c944460213812368d92b8f21527c0b464e`,
identical at `da9ac7ec…`), lines 129–131.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S188 | chousa round-75 verifier spot-check, routed defect 2 — corpus/lessons/round-75-verifier-spotcheck.md | own-work | B | the r75 correction counter's presence-test limits: derivation binding, polarity, magnitude, last-section position, base ancestry | 1af39fed6058ad46fc075b72fddaae838f43273e (blob c53d32c9 identical at da9ac7ec), lines 129-131, quote on line 130 | A record-correction counter must bind its derivation to the authored bullet and test polarity, magnitude and position, never substring presence | mined | 2026-11-04 | on-release | corpus/lessons/round-76.md |

## S189 — REJECT (own-work C)

Source: `corpus/evidence/round76/claims.md` at `5daa3628389c164f6ee34027be77d26b175c0de7`,
line 27 — this round's own frozen predicate text.

Located quote, re-opened at the anchor revision (probe exit 0):

- line 27, 3 words: "`BATTERY=PASS forgers_rejected=11/11 positive=2/2`"

Concrete flip (the reject reason names what would be admissible instead): the claims file
is the lane's own declaration of its own predicate, so it is not evidence that the
predicate holds — the committed receipts are. Flip: admit scoped to the claim text if an
admitted entry ever rests on a declaration as the only record of a prediction.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S189 | chousa round-76 frozen claims file — corpus/evidence/round76/claims.md | own-work | C | this round's own frozen predicates as source evidence | 5daa3628389c164f6ee34027be77d26b175c0de7, line 27 | REJECTED: the claims file is the lane's own declaration of its predicate, not evidence that it holds; flip: admit scoped to the claim text if an admitted entry ever rests on a declaration as the only record of a prediction | rejected | 2026-11-04 | on-release | — |

---

## Verification receipts

- Census on scratch mirrors of the lane at `5daa3628` (never on the lane):
  `.ufo/waves/round-76/w1/R76Scribe/census-receipts.txt`.
  Baseline 186 rows / A123 B48 C15 / mined 150 queued 19 rejected 17 → with the three rows
  189 rows / A123 B50 C16 / mined 152 queued 19 rejected 18. `validate` exit 0 on baseline,
  on the L1's rows and on these corrected rows, with only the five pre-existing W04
  duplicate-URL warnings (S051, S053, S073, S074, S075). A mirror with the rows but without
  the cited lesson file returns E11 for S187 and S188 and exit 1 — the check is fail-closed.
- Quote/anchor probe (fail-closed, exit 1 on any failure):
  `.ufo/waves/round-76/w1/R76Scribe/probe-corrected.txt` (exit 0),
  `.ufo/waves/round-76/w1/R76Scribe/probe-as-drafted.txt` (exit 1 — the L1's draft anchors,
  see the seat report).
