# CritBotWall

Axes: operability, calibration, depth.

Attacked approach: admit `corpus/knowledge/search-log-fields-r36.md` this round. The approach fails. The landed rejection is the correction. This is not a tradeoff the L1 must reject, and it does not retune rule R43-SPLIT.

## Counterexample

The file's first source line cites the PRISMA-S DOI `https://doi.org/10.1186/s13643-020-01542-z` (packaged id S079; pre-remap staged id S077). The only committed capture of that URL is a 267-byte Client Challenge page. The three checklist sentences the entry would import are absent from it. This round did not re-open the URL. Admitting the file would write those sentences, and the line "full text fetched 2026-10-23", as if the source had been opened.

## First line

The capture's first line is one space, not `Client Challenge`. Python `repr` of that line is `' \n'`.

```
 
```

First non-empty line, line 8, `repr` `' Client Challenge \n'`:

```
 Client Challenge 
```

## Evidence

Cache key, local hash only, no fetch. `sha256(url.encode()).hexdigest()[:24]` is the convention in `tools/quarantine-check.py` `cache_key`.

```
MATCH 01f657b3d0ab045c494b3f92 https://doi.org/10.1186/s13643-020-01542-z
      1edde1019906f2e51f031666 http://doi.org/10.1186/s13643-020-01542-z
      1af72a2c3b0e834693a5344b https://doi.org/10.1186/s13643-020-01542-z/
      79dca69826c9236a2edaa715 https://link.springer.com/article/10.1186/s13643-020-01542-z
      f5f8d37e1b1faa1ba729737c http://link.springer.com/article/10.1186/s13643-020-01542-z
      e666f78d0d0ebc70dc38c7b5 https://link.springer.com/article/10.1186/s13643-020-01542-z/
      87c5a4b740e136986e36f39b https://systematicreviewsjournal.biomedcentral.com/articles/10.1186/s13643-020-01542-z
      2781efb2d0e420d8edbe8e29 https://www.prisma-statement.org/prisma-search
      d7805585bf855ac0d518573e https://pubmed.ncbi.nlm.nih.gov/34285662/
      7a3f1fdd8966cca6c9f94b10 https://pmc.ncbi.nlm.nih.gov/articles/instance/10288090/bin/mmc2.pdf
      14aaa168a5cb4d833ca78b0b https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04
      02b3b0e812df68ca305c7bc3 https://www.jstage.jst.go.jp/article/jjsme/105/2/105_17/_article/-char/ja
      58b1b5641ed80c3554e73727 https://www.jstage.jst.go.jp/article/jjsme/105/2/105_17/_pdf/-char/ja
```

The DOI matches. The Springer URL the campaign rejected as route R2 does not. The wall is the committed capture of the cited URL itself.

```
path /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/01f657b3d0ab045c494b3f92.txt
bytes 267
chars 265
n_lines_splitlines 21
first_line_repr ' \n'
first_nonempty_repr ' Client Challenge \n'
endswith_newline True
absent 'It is intended to guide reporting, not conduct, of the search.'
absent 'copied and pasted exactly as run'
absent 'For each search strategy, provide the date when the last search occurred.'
present 'Client Challenge'
absent 'PRISMA'
absent '参照日'
```

```
267 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/01f657b3d0ab045c494b3f92.txt
c42ccd00e8305111f9269436ae4dd8a66cba6188df6a5a44e5478ce00b4e94f8  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/01f657b3d0ab045c494b3f92.txt
```

The digest matches `corpus/evidence/round42/receipts/digests.txt`. The raw sibling is 3038 bytes. Its first line is `<!DOCTYPE html>`. Its title is `<title>Client Challenge</title>`. `client challenge` and `enable javascript` are present. `PRISMA` and `copied and pasted` are absent. `tools/quarantine-check.py` lists `client challenge` in `INTERSTITIAL_MARKERS`, so this capture is an interstitial, not a page.

A scan of every `*.txt` in that `.qcache` for `copied and pasted exactly as run`:

```
txt_scanned 2444
hits 0
```

The campaign search log's `aaron papers fetch 10.1186/s13643-020-01542-z` / 110,181 characters is a log claim. It was not re-run. It is not a file in the committed cache. No network. No shokuknow tool.

Identity, from local files, not from arithmetic:

- `.ufo/waves/round-43/assimilation/renumber-map.txt`: staged S077 is that DOI, "NOT adopted (bot-wall capture)"; lane S077 stays the Poppler `pdftotext(1)` manual.
- `corpus/SOURCES.md` S077 source cell is the installed pdftotext manual, not the DOI.
- `lanes/chousa/ID-REMAP.md`: round1 `S077` was renumbered to `S079`. The proposed entry cites `source: S079` and "full text fetched 2026-10-23".
- `corpus/knowledge/search-log-fields-r36.md` is not in the lane. The admitted file is `corpus/knowledge/search-log-method-r39.md`, citing S078 and the Europe PMC URL, not this DOI.

## Why admission imports an unreopened source

`search-log-fields-r36.md` is one file with three `source:` lines. The first is the DOI. Its observations quote PRISMA-S item 8 ("copied and pasted exactly as run"), item 13 (a date per strategy), and the scoping sentence ("guide reporting, not conduct, of the search"). Those three strings are the register's quarantined quotes for campaign S077, and they are absent from the capture the register's own cache key names.

Round 43's question, in `corpus/SOURCES.md`, is which search-log requirements can be re-opened from committed captures without a fetch. L0 `8d77e6c1` is still open. Claims freeze "No external fetch" and explicitly do not claim adoption of this file. A source is unreopened here when this round did not open it and the committed capture of the cited URL does not contain the quoted sentences. That is this DOI.

Admitting the file would import that unreopened source in three ways at once:

1. False provenance. The source line says the full text was fetched. The committed bytes are a challenge page. Round 42 already recorded the same failure: the campaign class `payload-absent` ("fetched cleanly") licensed a verdict the capture's form does not support (`corpus/QUALITY.md` criterion 59).
2. Identity change. The file cites packaged S079, which is not a lane id. Rewriting that citation to lane S077 would point it at the pdftotext manual. Copying staged S077 onto lane S077 would overwrite that manual. Either move is a different document wearing the cited id.
3. Unrecomputable depth. A later counter in the C3 shape (citation, URL, quote substring of the committed capture) cannot locate these sentences. The 110,181-character aaron claim is not a capture this round reopened, and it is not in the cache.

The other two source lines do not rescue the file. Cochrane chapter 4's committed capture (`14aaa168a5cb4d833ca78b0b.txt`, 211326 bytes) does contain `Document the search process in enough detail`. That opened sentence is not the PRISMA-S checklist. The file cannot be admitted as a three-literature entry by keeping the Cochrane sentence and dropping the DOI: the DOI source line and the checklist observations are the entry.

## Fixable defect, not a flip

The lesson's second clause, "the Japanese capture does not contain 参照日", is true of the cited article URL and false of the companion PDF text.

Cited article URL `https://www.jstage.jst.go.jp/article/jjsme/105/2/105_17/_article/-char/ja`, capture `02b3b0e812df68ca305c7bc3.txt`: `参照日` absent.

Companion PDF URL `.../105_17/_pdf/-char/ja`, capture `58b1b5641ed80c3554e73727.txt`: present, including `著者名（出版年）．文献名．URL（参照日）` and `参照日の記載は必須とする`.

That PDF does not contain `copied and pasted exactly as run`. It is not a capture of the DOI. Naming the article-page file in the reason clause would fix the wording. Admitting `search-log-fields-r36.md` would not. The bot wall is sufficient by itself.

## Impacted axes

- Depth. The entry's checklist quotes are not substrings of the opened capture. Admitting it would add a sourced claim the committed bytes do not carry. C3's located-quote test, if pointed at this file, would miss. The admitted S078 entry does not cite this DOI; leave it that way.
- Calibration. "Full text fetched" against a 267-byte interstitial is the same miscalibration round 42 refused for S077 (`unverifiable`, never a fabrication). Do not retune the 1/2 bound to absorb it. This row is not in the absent-split table.
- Operability. No local command can re-ground the quotes from the committed capture. A fetch would be required, and the fetch-scope ruling is unanswered. A file that prints the claims without that capture is the do-nothing gate for this adoption.

## Smallest safe correction

Do not admit `search-log-fields-r36.md`. Do not append staged S077 or packaged S079. Do not retarget the citation onto lane S077. Do not fetch. Do not retune the 1/2 bound. The flip already frozen in `corpus/lessons/round-43.md` stands: the fetch-scope ruling is answered, and a capture of each cited source contains the quoted sentences. The landed rejection is that correction.

No lane production file was modified. No network. No tool installed.

Report: .ufo/waves/round-43/w1/CritBotWall.md
