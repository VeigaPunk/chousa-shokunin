# R58ConnectorFrontier — carrier alphabet vs corpus/README.md Frontier

Seat: connector (leaf, no dispatch). Read-only. Only write: this file. No scratch created; no installs; no live fetch; no git mutation.
Lane HEAD at read time: `5da0a63` (`git rev-parse --show-toplevel` → lane root). Claim base: `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791`. Freeze: `9e73a031ab1ac3bac343de008850d7d87f9e5634`.

## 1. Frozen R58 claims touching the carrier alphabet

- C2 (`corpus/evidence/round58/claims.md:13-21`): add `corpus/knowledge/carrier-alphabet-china-r58.md` from S101 only; distinguishes GB3469 single-letter type alphabet, electronic types, carrier identifiers and `[type/carrier]` notation from the separate document-code field (claims.md:15).
- Novelty predicate (claims.md:19): `载体类型标识` absent from base `corpus/knowledge`, present in new entry. This is the only novelty test in the frozen counter.
- Used-by predicate (claims.md:19): S101 `used-by` names the entry.
- Scope limit (claims.md:15): "the source's located text, not present-day standards validity or semantic truth". No comparison to the standard's own table is in scope.

## 2. README Frontier: where the carrier alphabet is named

Named gap, two sites (verbatim bullets):
- `corpus/README.md:1187` (Round54 `### Frontier` → `Left open`, section starts 1165/1177): "The HIT data specification's carrier alphabet beside the standard's (W1 `R54DraftEntryStb`): waits for a span builder that reads an OLE `.doc` through `tools/capture-text.py`."
- `corpus/README.md:1210` (Round55 `### Frontier` → `Left open`, section starts 1191/1200): "The HIT data specification's carrier alphabet beside the standard's (round 54): the span builder now reads the OLE `.doc` (W1 `R55ExecS101Leg`: the four round-54 S101 quotes build 4/4); the entry leg waits for a round whose counter covers S101's `used-by`."

Precondition satisfied by base: `README.md:1175` (OLE `.doc` defined text form) and `README.md:1196` (`../tools/build-spans.py` reads OLE through `capture-text.py`). The Round-55 wait condition is the exact remaining trigger: "a round whose counter covers S101's `used-by`". C2's used-by predicate (claims.md:19) matches it.

Round57 frontier (`README.md:1242-1262`) has no carrier item. Planned-row name: `corpus/lessons/round-57-verifier-spotcheck.md:72` cites base "## Planned — round 57" naming "S101 carrier-alphabet leg".

## 3. Base query and held-ground checks (run; exact commands and outputs)

```
git -C <lane> grep -c -e 载体类型标识 b13ca7b5c8bbb40d2d29a37fb443c64ca043f791 -- corpus/knowledge
  (no output; exit 1)  -> term absent at base (matches claims.md:19 predicate)
git -C <lane> grep -n -e 文献载体标识 -e 文献类型标识 b13ca7b5… -- corpus/knowledge
  b13ca7b5…:corpus/knowledge/source-type-taxonomy-r36.md:18,30
  b13ca7b5…:corpus/knowledge/source-type-taxonomy-r37.md:5,20,21,22,38,58
git -C <lane> grep -n -e 磁带 -e 联机网络 b13ca7b5… -- corpus/knowledge
  b13ca7b5…:corpus/knowledge/source-type-taxonomy-r37.md:25   (carrier rows 磁带 MT, 磁盘 DK, 光盘 CD, 联机网络 OL, 缩微资料 MM)
git -C <lane> grep -n -e 文献标志码 -e 文献类型及载体 -e 载体类型 b13ca7b5… -- corpus/knowledge
  b13ca7b5…:corpus/knowledge/citation-count-semantics-r37.md:24-27 (文献标志码; 文献类型及载体类型标志; S101)
git -C <lane> grep -n -e GB3469 -e 单字母 -e 双字母 -e 'DB/OL' -e '[J/OL]' -e '[M/CD]' b13ca7b5… -- corpus/knowledge
  (no output)  -> the GB3469 alphabet, 双字母 recommendation, DB/OL, J/OL, M/CD notation are new at base
```
Note: source-type-taxonomy-r37.md:58 states the S123 reproduction "names neither the older code standard nor ISO 690" (`[32, 0, 0, 0]` for `文献载体标识`, `3469`, `ＩＳＯ ６９０`, `690`; command quoted in that note, not rerun here).

S101 row at base (`corpus/SOURCES.md:111`): last cells read via `git show b13ca7b5…:corpus/SOURCES.md`: `used-by` = `corpus/knowledge/citation-count-semantics-r37.md` only (13 cells). C2 must add the entry to this cell (claims.md:19). `corpus/lessons/round-49.md:158` lists two used-by entries (source-type-taxonomy-r37 and citation-count-semantics-r37); the SOURCES row at base lists one. Noted discrepancy; the SOURCES row is the registry authority.

## 4. Frozen quote set vs S101 defined text form (run)

Command (read-only, python reading `git show` output; no file written):
`text = git show b13ca7b5…:corpus/evidence/round54/S101-text-form.txt` (27012 chars); quotes from `git show 9e73a031…:corpus/evidence/round58/c2/quotes.tsv` (12 data rows).
Output: each of the 12 quotes occurs exactly once; offsets 315, 330, 590, 683, 734, 781, 797, 838, 965, 993, 1460, 11723. Matches `corpus/evidence/round58/s101-open.txt` offsets (797 for `并以[文献类型标识/载体类型标识]表示`, etc.).

## 5. Classification

| Item | Status | Basis |
|---|---|---|
| Round-55 entry-leg wait ("a round whose counter covers S101's used-by") | **closed if C2=PASS** | README:1210; claims.md:19 used-by predicate |
| Round-54 span-builder precondition (OLE `.doc` read) | already closed at base | README:1175, :1196 |
| "beside the standard's" comparison (S101 alphabet vs GB/T 7714 table) | **not closed by C2** | README:1187, :1210 name the comparison; claims.md:15 is S101-internal and states no comparison; standard's table held only as S123 rows (source-type-taxonomy-r37.md:24-25) |
| S101 document-code field / 文献类型及载体类型标志 | already held (advances nothing new as a fact) | citation-count-semantics-r37.md:23-27 |
| Carrier identifiers MT, OL, CD, DK, MM | overlap held ground | source-type-taxonomy-r37.md:25 (from S123); S101 quotes 734, 781 repeat MT/OL |
| GB3469 single-letter alphabet, 双字母 recommendation, `[type/carrier]` notation, DB/OL, J/OL, M/CD | new ground at base (zero hits, section 3) | S101 quotes 330, 590, 797, 838, 965, 993 (section 4) |

Net: the carrier alphabet closes the named **entry leg** of the round-55 Left-open item (README:1210) and advances held ground on carrier identifiers and the document-code field. It does not close the **"beside the standard's"** comparison that README:1187 and README:1210 both name.

## 6. Attack on the frozen novelty predicate (finding, not a fix)

claims.md:19 tests novelty with one lexical token (`载体类型标识`). That token is absent at base, but the frozen 12-quote set contains `磁带(magnetic tape)—MT` and `联机网络(online)—OL` (quotes.tsv rows 5-6), whose tokens `磁带 MT` and `联机网络 OL` are already held at source-type-taxonomy-r37.md:25 from S123. The counter therefore cannot distinguish a held-ground re-statement of the carrier table from new S101 ground. A C2 entry built only from the 12 quotes would pass the novelty predicate while repeating held carrier rows. This is a predicate-scope finding for L1; no frozen file was edited.

## 7. Runs not performed

- `c2-count.py` not run. The entry `corpus/knowledge/carrier-alphabet-china-r58.md` is absent at both base `b13ca7b5…` and HEAD `5da0a63…` (`git cat-file -e`), so the counter cannot print `C2=PASS` on the lane tree; the executor must author it first.
- `c1-count.py` not run (outside this seat).
- No live fetch; no tool installs (none needed; `/home/vgpnk/.omp/agent/RULES.md` not read because nothing was installed).

## 8. Proposed patch (for the executor's report only; not applied)

- Add to S101 row `used-by` (`corpus/SOURCES.md:111`) the new entry path.
- Add a Round-58 `### Frontier` bullet that states the comparison leg (`beside the standard's`, README:1187/1210) remains open and names the GB3469-vs-GB/T 7714 relation as the untested question (source-type-taxonomy-r37.md:58).

VERDICT: C2 carrier-alphabet leg — survives as closure of the round-55 entry-leg wait (README:1210, claims.md:19 used-by predicate); falsified as closure of the named "beside the standard's" comparison (README:1187, :1210) and the single-term novelty predicate (claims.md:19) does not measure held carrier ground; C2=PASS itself inconclusive (counter unrun, entry absent at base and HEAD).
