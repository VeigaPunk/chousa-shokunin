# R50ExecPerturbAdopter — perturbed-input probe of `tools/assimilate-rows.py`

Wave 2, seat R50ExecPerturbAdopter (leaf). Scratch `/dev/shm/chousa-r50-R50ExecPerturbAdopter/` (deleted after this report). Inputs read-only: the lane tool, `corpus/SOURCES.md`, the staged package `/home/vgpnk/Projects/shokuknow/merge/chousa/`. No installs/updates. Nothing outside scratch and this file was written. Claims `claims.md` @ `6a068f2` and the landed bytes @ `74794db` were not touched; this probe attacks the adopter only.

## Method

Base package: `registry.md` = `## Registry` + S001 `https://example.test/held`, S002 `…/other`; `staged.md` = S010 `…/new-a`, S011 `…/held`; `knowledge/corpus/knowledge/a.md` cites both. Every variant is one delta. Template (cwd = scratch; `$T` = lane `tools/assimilate-rows.py`):

```
python3 $T --staged v/<n>/staged.md --knowledge v/<n>/knowledge \
  --registry v/<n>/registry.md --opened 2026-10-25 --out out/<n> --entry corpus/knowledge/a.md
```

Base: `COLLISIONS=0` / `CITED=2 APPEND=1 HELD=1`; renumber `S010 S003 append example.test/new-a`, `S011 S001 held example.test/held`; one 11-cell append row; stripped `S003 opened`. Contract: lane-addendum.md:332 (0–3-space rows), :346-349 (collision, ids continue the registry, by document), :362 (no literal/escaped `|`), :368 (census validate first); CORPUS.md:152 (4+ spaces = code, ignored); tool regexes assimilate-rows.py:82-83.

## (a) Registry row indented 1, 2, 3, 4 spaces

Row `S003 …/held2` indented; staged S012 cites it. Expected: 1–3 spaces = census row (held + collision); 4 spaces ignored (CORPUS.md:152; sources-census.sh:36-38).

| indent | staged S012 | tool collisions | section-10 `grep`+`comm` |
|---|---|---|---|
| 1, 2, 3 | `S012 S003 held example.test/held2`, next append S004 | `S003` | `S003`, identical |
| 4 | `S012 S004 append`, new-a took S003 | empty | empty, identical |

Guard leg (staged id S003, other URL): collisions `S003` at 1/2/3, empty at 4, identical to the section-10 pipeline at every indent (both `S003`; both empty at 4). **Designed.** At 4 spaces the append reuses the number the ignored line displays; per CORPUS.md:152 that line is not a row, so the number is free — a human-facing risk, not a defect.

## (b) CRLF in staged and registry

LF→CRLF copies: `rc=0`, `CITED=2 APPEND=1 HELD=1`; `renumber.tsv`, `append.md`, `collisions`, `reg-ids`, `staged-ids`, `stripped.tsv` all byte-identical to base (python comparison: `IDENTICAL`). CRLF selftest copy (`--selftest --fixtures fix-crlf`, every fixture file CRLF): `SELFTEST=PASS findings=26 expected=26`, `FIXTURES_SHA256=312a3022…`. **Designed.** Note: the entry copy is normalised CRLF→LF (universal newlines; `CR 0 LF 8` in the copied entry) — neutral, but not a preservation guarantee.

## (c) URL differing only by trailing slash, fragment, host case, query

`url_of` (:91) mirrors census `url_of` (sources-census.sh:600-606).

| registry URL vs staged `https://example.test/held` | renumber |
|---|---|
| `…/held/` · `…/held#sec1` · `…/held/#sec` · `https://Example.TEST/held` | `held S001` |
| `…/held?id=1` vs staged `…/held?id=2` | `S011 S004 append example.test/held?id=2` |

Slash/fragment/host-case are **designed** (held). Query is **designed-as-census**: the census keeps the query in identity, so it is a different document and a second row is appended; two URLs for one page differing by a tracking parameter would therefore become two rows and E04/W04 cannot see it. Live check over the real bytes: 114 staged rows / 81 held URLs → **0** raw-different/normalised-equal pairs, **0** query near-misses (the shared `eric.ed.gov/?id=EJ1372738` matches exactly). Latent, not live.

## (d) Escaped pipe in the source cell and in the scope cell

| variant | observed | verdict |
|---|---|---|
| scope cell `scope a \| b` | 11 cells, `scope a / b`, `STRIPPED S003 cell5-pipe` | designed |
| source, pipe before URL | identity correct, `New doc A / alt — https://…/new-a`, `cell2-pipe` | designed |
| source, pipe after URL | identity correct, `…/new-a / alt`, `cell2-pipe` | designed |
| source, pipe **inside** URL (`…/held\|alt`) | `S011 S004 append`, url `example.test/held\`, cell `…/held / alt` | **DEFECT** |
| registry source `Held doc \| alt — https://…/held` | held URL lost: `S011 S004 append example.test/held` | **DEFECT** |

Cause: staged identity is computed on the un-rewritten cell (`url_of(staged[sid][1])`, :319) while the pipe rewrite runs later (:342-344); `registry_rows` splits on plain `"|"` (:133), not the escaped-pipe splitter used for staged rows (:115), so an escaped pipe in a registry source cell truncates the URL (:312 → empty). Mitigation observed: census on a mirror gives `E04 S004 duplicate url example.test/held within scope held scope` (rc=1) for the staged case and `E01 S001 fields=12` (rc=1) for the registry case. Live: the lane registry has 0 escaped pipes; the package's only `\|` is S097's **recheck** cell, and that path is safe (observed `180d`, `cell10-pipe` stripped, 11 cells). Both are latent input-validation gaps, not live corruption.

## (e) Staged row with 10 or 12 cells

`rc=1`, `REFUSED S010: staged row has 10|12 cells, not 11`; `out/` holds only `reg-ids`, `staged-ids`, `collisions` — no `renumber.tsv`/`append.md`/`stripped.tsv`. **Designed** (safe refusal; a literal pipe is a column boundary, so it cannot be rewritten unambiguously). Uncited malformed row: `rc=0`, `CITED=1 APPEND=0 HELD=1`, no refusal — designed per "append only the rows the admitted entries cite", but silent. Doc nit: the docstring's "any other pipe inside a cell rewritten to ` / `" is unreachable — an unescaped pipe always yields ≠11 cells (refusal) or fails `ROW_RE`; only escaped pipes reach the rewrite.

## (f) Entry citing the same staged id twice, and citing none

Duplicate: two more `S010` mentions → `CITED=2 APPEND=1 HELD=1`, one renumber row, one append row, `used-by` = `corpus/knowledge/a.md` once, and **both** body occurrences became `S003`. **Designed** (set semantics; `used-by` = exactly the entries, :362). None: `rc=0`, `CITED=0 APPEND=0 HELD=0`, header-only `renumber.tsv`, 0-byte `append.md`, entry copied unchanged. **Designed** as a no-op (selftest grammar prints `ENTRYCITES <entry> -`), but it exits success with nothing bound — the Gate, not the adopter, must reject such an entry.

## (g) Registry with no `## Registry` heading

Expected: refuse, or continue from the registry maximum; append-only. Observed (`g-noheading`; `g-wrongheading` `## Sources` is identical; renumber tabs shown as spaces):

```
COLLISIONS=0
CITED=2 APPEND=2 HELD=0
S010  S001  append  example.test/new-a    # S001/S002 already exist in the registry
S011  S002  append  example.test/held     # the held document re-appended
```

`registry_rows` requires the exact heading (:125-127), so `base` is empty and `nxt = max(…, default=0)+1` (:315) starts at S001; the held URL is not recognised either. **DEFECT**: the docstring's "next free lane id, contiguous from the registry maximum" is violated; ids are neither free nor append-only. Same class with a valid heading but a row outside it (`g-row-outside`, S002 under `## Other`): `S010 S002 append`, minting S002 twice. Mitigation: `sources-census.sh validate --file corpus/SOURCES.md` on the mirror exits 1 with `E12 … row outside Registry section` (×4, ×2) but **no E03** — census records duplicate ids only inside the Registry section (sources-census.sh:618-622 `next` before `seen[id]=1` at :642), so the duplicate the tool creates is invisible to the duplicate detector and only E12 blocks it. Not live: one heading, 0 outside rows, 0 indented rows.

## (h) `--opened 2026-02-30`

`rc=2`, stderr `assimilate-rows: need --staged FILE, --registry FILE and a calendar-valid --opened YYYY-MM-DD`, **no out directory** (check precedes `out.mkdir`, :263). Same for `2026-02-29` and `2026-13-01`; `2026-02-28` → `rc=0`, `opened=2026-02-28`. **Designed.** Note: calendar-only; `--opened 2027-01-01` is accepted (`rc=0`) and the mirror then fails census `E08 S003 opened=2027-01-01` (rc=1) — covered by the mandated validate step, not the adopter.

## Result

Eight perturbed classes, 31 variant packages beyond the base (32 dirs) plus one CRLF selftest copy. Designed and correct: (a) at 1/2/3 spaces, (b), (c) slash/fragment/host case, (d) scope and outside-URL pipes, (e), (f), (h), and the live S097 recheck pipe. Three input-validation defects, all latent (no live input reaches them) and all blocked downstream by the section-10 census gate: **D1** identity computed before the escaped-pipe rewrite (a held document appended as new), **D2** registry parsed with a plain `"|"` split (escaped pipe in a registry source cell loses the held URL), **D3** next-id computed only from rows inside `## Registry`, with no refusal for a missing/renamed heading or an outside row, minting S001/S002 twice (E12, not E03, is the only signal). The frozen C1 fixture legs and landed C2 bytes are untouched; the CRLF fixture copy still gives `SELFTEST=PASS` 26/26.

VERDICT: attacked the adopter with eight perturbed input classes (31 variants + CRLF selftest copy); frozen claims and landed bytes survive, but three latent input-validation defects found — identity-before-pipe-rewrite (D1), plain-split registry pipe (D2), next-id/heading gap minting duplicate ids (D3), each blocked only by the census gate.
