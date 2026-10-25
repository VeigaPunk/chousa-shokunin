# W2MutId — URL map is not subtract-2

Seat: W2MutId (leaf). No subagent. No network. No fetch. No production edit. No `jj`. No `git commit`.

## Axes

- operability: name the file, the row, and the URL a reader would touch if they applied either function.
- calibration: one agreeing pair is not a series rule. The assimilation copy is not the committed registry.
- depth: the counterexample is a different document, with its own capture, not a missing number.

## One sentence

Mapping staged S081 to lane S079 follows the RFC 7089 URL onto the next free lane id; subtracting 2 from every staged id also sends S081 to S079, but it sends staged S079, the unadopted PRISMA-S DOI, onto lane S077, which is the pdftotext manual.

## The coincidence, and only that

Staged append `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` line 9 is S081, URL `https://www.rfc-editor.org/rfc/rfc7089.txt`. The package entry cites that id and that URL:

```
source: S081 — https://www.rfc-editor.org/rfc/rfc7089.txt — sections 2.1.1, 3.1 and 7 — RFC 7089, February 2013, Informational
```

(`merge/chousa/knowledge/corpus/knowledge/citation-version-binding-r36.md` line 4.)

Committed `corpus/SOURCES.md` (64314 bytes) has no S079 row, no `rfc7089.txt`, and no `10.1186/s13643-020-01542-z`. Its last registry id is S078. The next free lane id is therefore S079. `81 - 2 = 79`, so a constant shift lands the RFC citation on the same token the URL map uses.

That agreement has a local cause, not a general one. The two staged rows before the RFC were not taken, so the first adopted staged id sits two above the first free lane id. The shift describes that gap. It is not the adoption function.

URL map, as specified and as drafted:

- Match the document by URL. C3 freezes the lane URL as `https://www.rfc-editor.org/rfc/rfc7089.txt` and forbids `source: S081` (`corpus/evidence/round44/claims.md`, predicate R44-C3; `corpus/evidence/round44/c3-count.py` lines 29–30 and 56–58).
- Assign the next free lane id, S079, because the committed registry ends at S078.
- Leave every other staged id alone.

The assimilation draft does that one rewrite and says the GB/T row is not cited:

```
source: S079 — https://www.rfc-editor.org/rfc/rfc7089.txt — section 2.1.1, byte offset 14896 of the committed capture — RFC 7089, February 2013, Informational
```

(`.ufo/waves/round-44/assimilation/draft/citation-version-binding-r36.md` line 3; line 6: "Staged S082 (the GB/T record) is not cited.")

The committed capture for that URL is `.qcache/d0c4a09a9de32cb91d5e3797.txt`, 107130 bytes, and it contains `constitutes a promise that the resource state`. This seat did not run `c3-count.py`. An unrun counter has not passed.

## Counterexample: staged S079

Append line 7:

```
| S079 | PRISMA-S: an extension to the PRISMA Statement for Reporting Literature Searches in Systematic Reviews (Rethlefsen, Kirks, Ayala, Moher, Page, Koffel; PRISMA-S Group, Systematic Reviews 10:39) — https://doi.org/10.1186/s13643-020-01542-z | paper | A | ...
```

That DOI is not a lane row. It is absent from committed `corpus/SOURCES.md`. It is also absent from the assimilation validate copy measured below. Round 43 refused the same capture (the map called the DOI "staged S077"; the append id was already S079 — see below). This round's draft does not cite it.

Subtract 2 sends staged S079 to S077. Committed lane S077, line 87, is a different document:

```
| S077 | Poppler `pdftotext(1)` manual — `/usr/share/man/man1/pdftotext.1.gz` (canonical project URL `http://poppler.freedesktop.org/` printed by the installed `pdftotext -v`; not fetched) | docs | A | ...
```

The DOI's committed capture is not the article. URL sha256 prefix `01f657b3d0ab045c494b3f92`, path `.qcache/01f657b3d0ab045c494b3f92.txt`, 267 bytes, contains `Client Challenge`, does not contain `PRISMA`, does not contain the RFC quote. Writing that DOI onto S077 would replace the pdftotext manual with a bot wall. Leaving the citation as S077 would point the refused DOI at the manual. URL mapping does neither: the DOI is not adopted, and lane S077 stays the manual.

A second unadopted prefix row shows the same split. Staged S080 is the Cochrane chapter-04 URL (`https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04`). Subtract 2 sends it to lane S078. Lane S078 is the Europe PMC full-text XML (`https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML`), already adopted in round 43 by that URL, not by copying staged S080. The required counterexample is still S079; S080 is the same function failing one row later.

## The adopted set is not the arithmetic image

The assimilation validate copy is not the committed registry. At the read below it had already placed three new rows by URL, and census output already on disk said `validate_exit=0`. This seat did not run census.

| lane id in that copy | URL | staged id of that URL | subtract-2 preimage | what subtract-2 would attach |
|---|---|---|---|---|
| S079 | `https://www.rfc-editor.org/rfc/rfc7089.txt` | S081 | S081 | RFC 7089 (agrees) |
| S080 | `https://warp.ndl.go.jp/en/info/qanda` | S091 | S082 | GB/T 7714-2025 SAMR record, not WARP |
| S081 | `https://current.ndl.go.jp/e2867` | S092 | S083 | openstd GB/T notice, not E2867 |

`91 - 2 = 89`, not 80. Staged S089 is an ERIC field study (`https://eric.ed.gov/?id=EJ1372738`), not the WARP FAQ. The package's r37 entry cites `source: S091`, `source: S092`, and `source: S093` (Portico). Subtract 2 rewrites those to S089, S090, and S091. The draft rewrites the two adopted URLs to lane S080 and lane S081 and does not cite staged S093. Those are different functions. They happen to agree on the single pair the prompt names.

Round 43 already mislabeled this DOI by the same constant. `.ufo/waves/round-43/assimilation/renumber-map.txt` line 2 calls `https://doi.org/10.1186/s13643-020-01542-z` "staged S077" and says it is not adopted. The append has no S077 row; that DOI is append S079 (`ScribeRenumber.md`). `79 - 2 = 77`. Using that label as a lane id collides with the pdftotext row. The Europe PMC adoption in that round followed the URL to the next free id, not `staged_id + 1` and not the Cochrane row that occupied the neighboring staged number. Same class of mistake, different constant in the lesson's "shift by one" wording. This seat does not treat that wording as a measurement of the append.

## Quoted check

Command: a read-only Python walk of the committed registry, the staged append, the assimilation validate copy, the two r36 source lines, and the two local captures. No census, no `c3-count.py`, no fetch.

```
production_SOURCES 64314 has_S079 False
doi_in_production False
rfc_in_production False
lane S077 L87 url=http://poppler.freedesktop.org/`
lane S078 L88 url=https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML
staged S079 L7 url=https://doi.org/10.1186/s13643-020-01542-z
staged S080 L8 url=https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04
staged S081 L9 url=https://www.rfc-editor.org/rfc/rfc7089.txt
staged S082 L10 url=https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F
staged S091 L19 url=https://warp.ndl.go.jp/en/info/qanda
staged S092 L20 url=https://current.ndl.go.jp/e2867
validate S077 L87 url=http://poppler.freedesktop.org/`
validate S079 L90 url=https://www.rfc-editor.org/rfc/rfc7089.txt
validate S080 L91 url=https://warp.ndl.go.jp/en/info/qanda
validate S081 L92 url=https://current.ndl.go.jp/e2867
pkg36 source: S081 — https://www.rfc-editor.org/rfc/rfc7089.txt — sections 2.1.1, 3.1 and 7 — RFC 7089, February 201
draft36 source: S079 — https://www.rfc-editor.org/rfc/rfc7089.txt — section 2.1.1, byte offset 14896 of the committed
capture 01f657b3d0ab045c494b3f92 bytes=267 challenge=True prisma=False quote=False
capture d0c4a09a9de32cb91d5e3797 bytes=107130 challenge=False prisma=False quote=True
```

The trailing backtick on the poppler print is the markdown closer in the source cell, not part of the URL. The cell text is `http://poppler.freedesktop.org/`.

Raw URL fragments from the append, same read:

```
L7 repr='https://doi.org/10.1186/s13643-020-01542-z | paper | A | the reporting items a s'
L9 repr='https://www.rfc-editor.org/rfc/rfc7089.txt | spec | A | the protocol for binding'
L19 repr='https://warp.ndl.go.jp/en/info/qanda | docs | A | the collection cadence, retent'
L20 repr="https://current.ndl.go.jp/e2867 | paper | A | how Japan's national web archive b"
```

## Not done

- Did not run `python3 corpus/evidence/round44/c3-count.py`. Not passed here.
- Did not run `sources-census.sh`. The on-disk `validate-census.txt` line `validate_exit=0` is another process's output, not this seat's run.
- Did not append a registry row, rewrite a citation, or treat the validate copy as committed. A later edit to that workspace would not change the append URLs or the committed S077/S078 rows quoted above.
