# ScoutSourcesFrontier33 — frontier recon (round 33, wave 1)

Read-only. No installs. No lane or fleet writes except this report. Access date for file reads: 2026-10-23.

## Verdict

`sources-census.sh validate` on lane `chousa` exits **0** (two W04 warnings, then `ok`). No registry row has an ISO `recheck` date, and none is due on or before 2026-10-23. No row has status `candidate` or `unopened`. **RFC 8259 and the Python `json` docs have no row.** Round 33 C1 advances the still-open Round32 item “nested `"line"`/`"sha256"` keys read as the record's own” (`corpus/README.md:987-988`).

## 1. Census validate

Command:

```
timeout 120 /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
```

Exit **0**. Stdout (complete):

```
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

`scripts/sources-census.sh:16-18` and `:32-33`: W-codes do not change a clean lane’s status. `df -h /fast` before the run: 198G free (76% used).

## 2. Recheck date ≤ 2026-10-23, or status candidate/unopened

Parsed `corpus/SOURCES.md` `## Registry` (lines 11–71): **61** data rows, 11 cells each.

| status | n |
|---|---|
| mined | 38 |
| queued | 19 |
| rejected | 4 |

Allowed statuses are `queued|mined|rejected` (`scripts/sources-census.sh:4`). Observed statuses match that set. **Zero rows** have status `candidate` or `unopened`.

`recheck` cells are only cadences, never ISO dates:

| recheck | n |
|---|---|
| 365d | 29 |
| on-release | 25 |
| 90d | 4 |
| 180d | 3 |

**Zero rows** have a `recheck` date on or before 2026-10-23, because no `recheck` cell is a date.

Computed dues (census rule `scripts/sources-census.sh:34-37`: due = `opened` + N days; symbolic cadences never overdue):

```
timeout 60 /home/vgpnk/Projects/shokunin/scripts/sources-census.sh overdue --root /home/vgpnk/Projects/shokunin --today 2026-10-23 chousa
```

Exit **0**. 61 `cadence` lines (one per row, including every `NNd` row — `scripts/sources-census.sh:676-677` prints `cadence` for both `NNd` and symbolic values) and **zero** `overdue` lines. `NNd` is also printed as `overdue` only when due ≤ today (`:684-685`). Earliest `NNd` due is S006/S007/S015: opened `2026-10-19` + `90d` = **2027-01-17**, after 2026-10-23.

Not registry rows: `## Leads (unopened)` (`corpus/SOURCES.md:217-230`) is six bullets, with no status or recheck column:

- TREC RAG track website — https://trec-rag.github.io/ (`:219-220`)
- AVeriTeC — https://arxiv.org/html/2410.23850v1 (`:221-222`)
- Check, Please! starter course, linked from S003 (`:223-224`)
- DRBench — https://arxiv.org/abs/2510.00172 (`:225-226`)
- OCEBM Levels background document behind S014 (`:227-228`)
- Garner et al. 2016, BMJ 354:i3507 — https://www.bmj.com/content/354/bmj.i3507 — blocked HTTP 403 on 2026-10-21 (`:229-230`)

The words `candidate` / `unopened` elsewhere in `SOURCES.md` are search-log prose (`:149`, `:181`, `:209-217`), not row statuses.

## 3. RFC 8259 and Python `json` docs

Whole-file search of `corpus/SOURCES.md` for `8259`, `library/json`, and `json module`: **no hits**.

- **RFC 8259: no row.** Closest JSON row is S013, JSON Lines (`https://jsonlines.org/`), `corpus/SOURCES.md:23`, status `mined`, recheck `365d`. That is not RFC 8259.
- **Python `json` documentation: no row.** Python library rows that do exist are S038 `datetime`, S044 `os.path`, S049 `html.parser`, S052–S053 `socket`, S054 `http.client`, S055 `ssl`, S056 `ipaddress`, S059 `hashlib`, S060 `fcntl`. None is `library/json`.

`corpus/evidence/round33/claims.md:85-90` says C1 rests on a `SOURCES.md` row opened this round for RFC 8259 §4, and that a second row (Python `json`, repeated names) may record last-value behaviour. Neither row is in the registry at this read.

## 4. `## Frontier` items still open, and which C1 advances

Section starts at `corpus/README.md:348`. Latest standing list is Round32 (`:986-989`), which does not close the earlier items it does not move to held ground.

**Round32 still open (`:986-989`), current explicit list:**

1. Non-cooperating writers and network filesystems (round-32 C1 residual). Cooperating `verify-all --json` appenders were moved to held ground (`:976-979`).
2. URL hops, transitive chains, and whether a local copy is the source the hop meant (round-32 C2 residual). Exempt-hop audit for `unresolved` / `blocked-no-fetch` / `labelled-dead` was moved to held ground (`:980-984`); `rejected` and `not-applicable` stay unread (`:983-984`).
3. Nested `"line"` / `"sha256"` keys read as the record’s own (round-31 carry) (`:987-988`).
4. Line binding for `## Claims` table pointers (`:988`).
5. Quote re-open items of rounds 29 and 30 (`:988-989`).
6. L0 fetch-scope question (`:989`).

**Still named open earlier, and not moved to held ground later:**

- Integrator/operator-owned (`:833-835`): receipt identity (proven receipt-backed rounds remain 0), non-author admit/reject spot-check, frozen-replay conformance. Semantic and external-source verification stay out of scope by design. Round26 says those carried debts remain open (`:893`).
- Round24 (`:848-851`): queued rows S008–S012, S017, S018 still waiting to be mined. Confirmed still `queued` at `SOURCES.md:18-22` and `:27-28`.
- Round26 still unclosed (`:877-879`), except the cooperating-appender part closed at round 32: filesystem races, parent-root legacy rechecks, receipt gaps, pairing a span’s occurrence with a named pointer line (the last restated as item 4 above). Path-denylist debts of rounds 26–28 are “carried unchanged” at `:941-942` and `:953-954`.
- Round28 (`:913-915`): that round’s C1 (default/nested-root relaxation) is “not achieved / unprovable”. Different claim from round-33 C1. Denylist not waived.
- Round29 open edges not closed by the Round30 correction (`:938-941`, `:950-953`, `:956-958`): pages without a `<head>` start tag, 2xx challenge pages, PDF sources, prefix and suffix disambiguation, and (after the D1 correction) fetch bounds — C2 is not held ground (`QUOTE_REOPEN_FETCH_BOUND_MATCH` 26/27 on 3 of 44 runs). Resolver time and IPv6 stay open (`:952`).
- Round31 limits not restated as closed (`:967-970`): chain-hop line binding, uniqueness, whether the named line is the right one for the claim’s meaning, and a claim without a pin is not checked for revision. [INFERENCE] these remain open because Round32’s held ground (`:974-984`) does not include them; Round32’s still-open sentence (`:986-989`) restates only part of this list.

**This round’s C1 advances item 3**, `corpus/README.md:987-988`. Frozen design (`corpus/evidence/round33/claims.md:16-36`) names the same surface: `json_str` / `json_has_key` (`tools/research-gate.sh:1109-1128`, callers `:1448-1483`) read `id`/`source`/`span`/`expect`/`marker`/`line`/`sha256` from the top-level object only; a nested member of the same name changes nothing; a duplicated top-level read field makes the record invalid. `claims.md:9-11` says round-32 D4 is the defect C1 removes (carried as round-31 D-C). It does not advance quote re-open, L0 fetch-scope, table-pointer line binding, exempt-hop URL/transitivity, or the round-28 root C1.

## Limits

Did not open RFC 8259 or the Python `json` docs (no network; no registry URL for either). Did not score C1 or run `c1-count.py`. Did not edit `SOURCES.md` or `README.md`. Overdue `cadence` lines were counted from the command’s stdout (61 lines, exit 0), not re-copied here in full.
