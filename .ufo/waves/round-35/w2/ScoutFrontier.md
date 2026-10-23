# ScoutFrontier — round 35 frontier rows vs knowledge

Axes named: operability (C1 grep pin), calibration (C2 mechanism witness / keyed-engine class).
Access date: 2026-10-23. Read-only. No gate was scored.

HEAD `2b2e0171153f63c2fb657ba601d74c7830662c1b` (base `e87c5d7ea2dbf3730b36a3961de3f06261d015e4` is an ancestor).
`sha256sum`: `corpus/README.md` `ad6ac1fe…c63c`; `corpus/QUALITY.md` `623d73a6…405c`;
`corpus/lessons/round-34.md` `5215b017…1f49`; `corpus/knowledge/dead-zone-pcre-r34.md` `c212615f…0a45`;
`corpus/knowledge/long-span-argv-r34.md` `53437ebb…d3e6`.

## Verdict

None of the three round-35 themes is a named open row in `corpus/README.md` §Frontier
(`## Frontier` at line 348; last disposition is the round-34 paragraph at 998–1004).
Grep pin, the mechanism witness, and the keyed-engine class do not move any of those
rows to held ground. The keyed-engine class is not in any committed `corpus/knowledge/`
entry at base. An untracked draft of that entry already exists on disk (duplicate if a
second note is added).

## What round 35 actually aims at (not a frontier row)

`corpus/evidence/round35/claims.md:14-17` says the round comes from
`corpus/lessons/round-34-verifier-spotcheck.md` routed defects 1–5 and the session
closure note, not from §Frontier.

| Theme | Where it is written | Frontier row it closes |
|---|---|---|
| Grep pin (C1) | spot-check defect 3, `corpus/lessons/round-34-verifier-spotcheck.md:85`; lesson row `corpus/lessons/round-34.md:122` | none |
| Mechanism witness (C2) | `claims.md:61-79`; lesson row `corpus/lessons/round-34.md:119` ("r35: work-proof battery") | none |
| Keyed-engine class | same lesson row 119 (`MutC2Keyed.md` ctl4/ctl6 37/37) | none |

Nearest frontier sentence, and why it stays open: `corpus/README.md:1001-1002`

> Not moved to held ground: the claim is unverified because its required shortcut controls ended on provider holds.

That claim is round-34 C1 (spans 32768..65536), not the grep pin and not the witness.
Spot-check defect 5 (`round-34-verifier-spotcheck.md:87`) says the next C1-touching round
must re-open that verification with the exclusion intact, or retire the claim.
`claims.md` C1 is the grep pin; C2 witnesses the dead-zone mechanism. Neither re-opens
spans ≥32768. QUALITY criterion 44 (`corpus/QUALITY.md:336`) is why that row cannot be
closed by rebuilding the held controls.

Round 28's operability sentence is a different C1 and is not the grep pin
(`corpus/README.md:913-915`):

> The full C1 operability target is **not achieved / unprovable**.
> Parent did not approve the proposed default/nested-root relaxation;
> denylist not waived.

## Frontier rows that stay open (exact)

Later dispositions supersede earlier "still open" sentences. Concurrent JSON appenders
(`README.md:848`) were moved to held ground at round 32 (`README.md:976-979`). The
standing open text is:

Round 30 correction, fetch bounds not held (`README.md:958`, first clause):

> The Round30 held-ground change is limited to pages that omit `</head>` (C1). C2 fetch bounds did not meet their frozen kill rule and are not held ground

Carried quote-reopen edges (`README.md:950-953`, restated at 969–970 and 988):

> Still open: pages without a `<head>` start tag, 2xx challenge pages, PDF sources, prefix and suffix disambiguation, resolver time inside the deadline, IPv6, and the L0 fetch-scope question.

Round 31 (`README.md:967-969`):

> Still open: line binding for records' `## Claims` table pointers (`path:N`) in `verify` mode, chain hops, uniqueness, and whether the named line is the right one for the claim's meaning; a claim without a pin is not checked for revision.

Round 32 (`README.md:986-987`):

> Still open: non-cooperating writers and network filesystems (C1); URL hops, transitive chains and whether a local copy is the source the hop meant (C2)

Round 33 (`README.md:995-996`):

> Still open from it: marker_default rows, keys spelled with escapes, and the per-character cost of the bash reader on very long lines.

Round 34 (`README.md:1002-1004`):

> Still open: the PCRE dead zone below the threshold (about 28000–32767 bytes for escape-diverse spans), spans above 65536 bytes, and long `verify-chain` quote anchors (now verified too, by R34NoHarm's probe, but not counted).

Round 28 denylist/nested-root operability (`README.md:913-915`) stays open, as quoted above.
Path-denylist debts are "carried unchanged" at `README.md:953-954`.
`rejected` / `not-applicable` hops "stay unread" (`README.md:984`) — a stated limit, not a moved row.

Integrator-owned sentence still in the file (`README.md:833-835`): receipt identity
(proven receipt-backed rounds remain 0), the non-author admit/reject spot-check, and
frozen-replay conformance. Later rounds did run spot-checks; this sentence was not
rewritten. Not advanced by round 35. [INFERENCE] it is stale as a status, not as text.

## Stale frontier sentence (not a round-35 close)

`README.md:1002-1004` still calls the PCRE dead zone open and still says "about 28000–32767".
The same file's coverage row already indexes the close (`README.md:1012`):
`knowledge/dead-zone-pcre-r34.md` holds the measured 32765–32767 window.
That note (`dead-zone-pcre-r34.md:27-32`) says the planned window shrank to three lengths
and the fix landed (`DEADZONE_MATCH=37/37`, gate `a6307edf…`).
`SCORECARD.md:1979-1981` says the dead zone was "Landed by round 34 attempt 2 and removed
from this list" and was "measured as exactly the 3 lengths 32765–32767, not
'about 28000–32767'". Round 35's witness does not edit this contradiction. Spans above
65536 and long `verify-chain` quote anchors stay open in both places (the SCORECARD
planned-round-35 list at 1976–1981 names E2, the `LC_ALL=C` selftest, and the L0
fetch-scope answer; it does not name grep pin or a mechanism witness).

## Knowledge census — keyed-engine class

Command: `git ls-tree --name-only e87c5d7ea2dbf3730b36a3961de3f06261d015e4 corpus/knowledge/`
→ 41 `*.md` files. `git grep` of `output-equivalent|keyed engine|keyed-engine|mechanism witness|mechanism-witness|fingerprint the fixture`
at that revision under `corpus/knowledge` → NONE.
The only committed hit is a lesson, not a knowledge entry: `corpus/lessons/round-34.md:119`.
`dead-zone-pcre-r34.md` and `long-span-argv-r34.md` do not document the class.

Disk now has 44 `*.md` (`ls corpus/knowledge/*.md | wc -l`). The three extras are untracked
(`git status --porcelain`; `git cat-file -e e87c5d7:corpus/knowledge/keyed-engine-output-equivalence-r35.md`
→ `AT_BASE=no`; same for HEAD):

| path | bytes | mtime | sha256 |
|---|---:|---|---|
| `corpus/knowledge/keyed-engine-output-equivalence-r35.md` | 4278 | 2026-10-23 16:58:30 -0300 | `03087a582a63b1e21294ea30e4fe45dbca3fd5de269197f1c482140afd04dbcb` |
| `corpus/knowledge/grep-pin-r35.md` | 3945 | 2026-10-23 16:58:30 -0300 | `edb3a2d87d74610458f03b97c033a8f37353937334e424d18cc18b1ae3d370ca` |
| `corpus/knowledge/bash-local-expansion-r35.md` | 2832 | 2026-10-23 16:58:39 -0300 | `5ba7d626ca429a0307ce748eb6e0c216f73e533838e05f1c23165288b366205e` |

Finding: `keyed-engine-output-equivalence-r35.md` already documents the class (title
"The keyed-engine class — output equivalence cannot prove a mechanism"; K1/K2, witness
limits, `WITNESS_SEPARATED=2/2`). It is not a committed entry. A second knowledge note
for the same class would be a duplicate of this draft. `grep-pin-r35.md` is the same
kind of untracked draft for C1. Not present at the start of this scout's directory
listing; written during the wave by another seat. Not edited here.

## QUALITY.md — last 10 criteria (35–44)

File ends at criterion 44 (`QUALITY.md:336-344`). Titles:

- 35 (`:265`) A control gate is scored in the gate's own layout.
- 36 (`:275`) Fixture metadata cannot stand in for reading.
- 37 (`:286`) Every numeric tally carries its counting command.
- 38 (`:293`) A battery output starts with its revision header.
- 39 (`:300`) Seats signal only processes they recorded.
- 40 (`:308`) Adversarial fixture content is not a fixed list.
- 41 (`:315`) Repairs are not edited into a gate that seats are scoring.
- 42 (`:321`) Measurements are bound to committed gate bytes.
- 43 (`:330`) A misrooted copy has committed byte-identity proof before deletion.
- 44 (`:336`) A held control is never re-authored; its claim is declared unverified before data.

Round-35 binding, from the text only: criterion 44 keeps the round-34 long-span row
unverified; criterion 42 is the receipt-to-blob rule this wave's contract restates.
The untracked keyed-engine draft cites "QUALITY 28/42" (`keyed-engine-output-equivalence-r35.md:32`).
Criteria 35–43 are not what C1 or C2 claim to close.

## Limits

Did not re-run counters, did not score a gate, did not edit corpus. Frontier quotes are
the file's current sentences; superseded sentences (line 848) are marked as superseded,
not as open. Whether the three untracked notes are complete enough to admit was not judged.
