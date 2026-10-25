# RevCensus — SOURCES.md census, independent re-derivation (round 46, wave 2)

Item: count rows/statuses in `corpus/SOURCES.md` with the frozen manual commands (`/home/vgpnk/Projects/shokunin/CORPUS.md:133-149`); paste each command and output; report every non-empty check. Read-only seat: no spawn, no lane git/jj mutation, no fetch.
Tree measured: `git archive d09fc8e7… | tar -x -C /tmp/chousa-r46w2-RevCensus` (the landing); `corpus/SOURCES.md` sha256 `38ca3bd26ebc8580822ab22a3d79a6ec301c84d4e9923899374ca6437af69005`.
The lane has since advanced (`3807537`, `e50b388`). At HEAD (`e50b388`) `corpus/SOURCES.md` = `73cb81f3…ef9ce`, whose only change from the landing is S088's anchor line, and the census below reproduces identically there (`rows=89`, same histograms) — so every number and finding holds at HEAD too. F1 re-checked at HEAD: same five.

## Seven frozen commands, from the lane root

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
89
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
A=83 B=1 C=5
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
mined=65 queued=19 rejected=5
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
(empty)
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md
(empty)
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
(empty)
```
**All seven empty/nominal: 0 malformed, 0 dup ids, 0 enum violations, 0 tier inflation, 0 missing used-by paths.** Ids contiguous `S001`–`S089` (`n=89`; `comm -13` vs `seq -f 'S%03g' 1 89` empty). `## Registry` (`SOURCES.md:7`) = 91 table lines = header + separator + 89 rows. No `S###` row outside column 0 (the indented-row class the column-zero patterns would miss is empty).

## Delta base `6e2630a` → landing `d09fc8e7`

```
$ git diff --stat 6e2630a d09fc8e7 -- corpus/SOURCES.md
 corpus/SOURCES.md | 5 +++++      (1 file changed, 5 insertions(+))
$ git diff … -- corpus/SOURCES.md | grep -E '^[+-]\| S[0-9]' | cut -c1-24
+| S085 | FEVER (2018) dataset
+| S086 | FEVER: a large-scale
+| S087 | FEVER: Fact Extraction
+| S088 | AVeriTeC Dataset release
+| S089 | AVeriMaTeC: A Dataset for
   (5 additions, 0 deletions; no existing row edited)
```
Base census `84 / mined=60 queued=19 rejected=5` → landing `89 / 65 / 19 / 5`: the `+5 mined` is exactly the five new rows; `tools/` 7 → 8 (matches C2's declared `tools=7`→`8`). No perturbation beyond the declared scope.

## The seven are not vacuous (mutation battery on a copy, `mut2/SOURCES.md`)

Planted malformed row, dup id, tier `D`, status `watch`, kind `blog`, missing used-by path; same seven commands, lane root:
```
rows=91  malformed=1  tiers=A=84 B=1 C=5 D=1  status=mined=66 watch=1 queued=19 rejected=5
duplicates=[S005]  enum=[tier S002 D / status S003 watch / kind S004 blog]
missing-used-by=[missing: corpus/knowledge/nope-r99.md]
```
Every leg fires. (A first attempt ran command 7 with cwd inside `mut/`, so all relative paths read as missing — harness error, corrected, not a lane finding.)

## Independent re-derivation of the same operand

```
$ bash corpus/evidence/round25-sources-census.sh          # the README-designated re-run
rows=89 / malformed=0 / tiers=A=83 B=1 C=5 / status=mined=65 queued=19 rejected=5
duplicates=[] / enum=[] / missing-used-by=[]              exit=0
$ scripts/sources-census.sh validate --file …/corpus/SOURCES.md
file	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
file	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
file	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
file	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	ok	/tmp/chousa-r46w2-RevCensus/corpus/SOURCES.md          exit=0
```
Zero E-codes (E01–E12 incl. E04 dup URL+scope, E08 date, E09 recheck, E11 used-by, E12 row outside `## Registry`). The five W04 are scope-sensitive duplicates by design and pre-existing (S051/S053 r29-30, S073 r38, S074 r40, S075 r41 — none round-46); W04 never fails a clean lane (`scripts/sources-census.sh:33`).

## F1 — five `source:`→`used-by` backlink breaches, invisible to all seven commands and to E11

The frozen census and `E11` test only that a `used-by` path *exists*; `QUALITY.md:19` requires the cited row's `used-by` to **name the citing entry**. Bidirectional pass over 61 `knowledge/*.md` (every `source:` line, every `S###`):
```
bash-local-expansion-r35.md  S068  used-by=…grep-pin-r35.md, …pin-capture-env-r37.md
capture-bash-pin-r39.md      S072  used-by=…env-pin-capture-r38.md
capture-path-pin-r41.md      S067  used-by=…grep-pin-r35.md
capture-path-pin-r41.md      S071  used-by=…pin-capture-env-r37.md, …capture-bash-pin-r39.md
capture-path-pin-r41.md      S072  used-by=…env-pin-capture-r38.md
```
Spot-confirmed on the rows (`SOURCES.md:77` S067, `:78` S068, `:81` S071, `:82` S072) and the citing lines (`capture-path-pin-r41.md:1`, `bash-local-expansion-r35.md:6`, `capture-bash-pin-r39.md:3`). Re-run verbatim in the HEAD tree (`git archive e50b388`): `VIOLATIONS=5`, the identical five. All five pre-date round 46 (r35/r39/r41). They do **not** falsify C1/C2/C3 — C2 names row truth as its declared limit, and C3 requires the bidirectional bind only for S085–S089, which it has. They do falsify "the census is clean, therefore criterion 6 holds".

## F2 — the README-named census script is outside both the C2 set and the Gates registry

`corpus/README.md:54` names `corpus/evidence/round25-sources-census.sh` as *the* way to re-derive registry counts. It matches neither set B (it is `corpus/evidence/round25-*.sh`, not under a `round*/` dir) nor set C (README not scanned — `c2-count.py:56,59` read only `SCORECARD.md` and `corpus/evidence/round*/claims*.md`):
```
$ python3 corpus/evidence/round46/c2-count.py --list
ENTRY_POINTS=72 (tools=8 counters=50 named=70) / GATES_ROWS=35 / REGISTERED=72/72
UNREGISTERED=0 / C2=PASS / exit=0
$ python3 corpus/evidence/round46/c2-count.py --list | grep -c 'round25-sources-census'
0
$ grep -c 'round25-sources-census' SKILL.md corpus/SOURCES.md SCORECARD.md
0 0 0
```
At HEAD (`e50b388`) the same counter prints `ENTRY_POINTS=73 (tools=8 counters=50 named=71) … REGISTERED=73/73 … C2=PASS`, and the `--list | grep -c 'round25-sources-census'` count is still `0` with the three registry greps still `0 0 0`: the set grew by one, the omitted README-named script did not.
`UNREGISTERED=0` is true **for the declared set**; that set is narrower than the docs naming counting commands. New *instance* (path + doc) of the known `CritC2Framing` class — wave 1's example was `corpus/evidence/round34/self-audit.py` — not a re-claim of the class. Census-side fact: the operand that re-derives the registry is the omitted one, and its naming doc is outside set C.

## F3 — the frozen seven are weaker than the lane's own validator (limit, not defect)

E02/E04/E08/E09/E12 have no frozen counterpart, and the maintained parser accepts 0–3 leading spaces while the frozen commands are column-zero (`CORPUS.md:152-155`). Those classes are clean at the landing too, so the census's empty output is necessary, not sufficient.

## Span arithmetic re-derived (supporting; not the headline)

All 11 `corpus/evidence/round46/spans.tsv` rows re-derive against the five on-disk captures: `sha256(capture)==capture_sha256`, `capture[offset:offset+len(span)]==span_file`, `span_file[80:80+len(quote)]==quote` — 11/11 each leg. Registry/entry offsets use a different (quote, not slice) convention and are mutually consistent: S086-2 `41931+80=42011`, S088-1 `3909+len("cached_source_url : ")=3929`, S085-1 `2349+len("evidence : ")=2360`. `spans.tsv` sha256 `d9bdd226bb5a8be658b49582c4379f8e6996febbb4b35426d3565446f0225964`.

## Verdict

- **Census operand: CLEAN.** Seven frozen commands empty/nominal at `d09fc8e7`; ids contiguous; 89 = 83 A + 1 B + 5 C = 65 mined + 19 queued + 5 rejected; round delta exactly `+5` rows S085–S089, all `mined`, all naming the citing entry.
- **C1 / C2 / C3: not falsified by this operand.** C2's pass is conditional on its declared set (F2); its declared limit covers F1.
- **F1 is the one real defect** (lane bytes I may not edit): five criterion-6 backlink gaps no committed counting command can see. Fix = one `used-by` append per row (S067, S068, S071, S072), not a claim change.
- No disagreement with any frozen predicate, target or kill rule.

Pointers: `SOURCES.md` sha256 `38ca3bd2…69005`, rows `:77,:78,:81,:82,:96-100`; `QUALITY.md:19`; `corpus/README.md:54`; `corpus/evidence/round46/c2-count.py:56,59`; fleet `scripts/sources-census.sh:33`. Scratch `/tmp/chousa-r46w2-RevCensus/` removed. No installs, no tool changes, no network.
