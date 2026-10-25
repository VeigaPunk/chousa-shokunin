# QuarantineS077 — hand-check of chousa round1 `S077` (`payload-absent`)

**Verdict: PRESENT.** The register row does not stand. All four quoted spans
of the census finding sit **verbatim** in a committed on-disk capture of the
cited article — the `aaron papers fetch` text the row's own gate block names.
The `payload-absent` class is doubly wrong for this row: (a) the cited DOI's
curl capture is a 267-byte WAF "Client Challenge" wall, so the source was
never "fetched cleanly"; (b) "local artifacts were all checked" is false —
the aaron artifact lives outside the census's lane-root glob and was never
searched. This is a checker blind spot, not a fabrication. It also supersedes
the round-42 `unverifiable` adjudication, which judged only the bot wall.

## Register row (frozen)

`.../round-48/assimilation/quarantine-slice` line 1: `S077   payload-absent`

`absent-defect-register.md` line 37:
`| chousa | round1 | S077 | payload-absent | https://doi.org/10.1186/s13643-020-01542-z | It is intended to guide reporting…/Include the search strategies…/For each search strategy… |`

Register renders only 3 quotes — writer truncates `r["quotes"][:3]`
(`absent-defect-register.py:142`). Census `quote-lint-full-v5.json` holds 4
ABSENT findings for this row; the 4th is
`each component of a search is completely reported and therefore reproducible.`

## Lane SOURCES row and gate block

Census base: `/home/vgpnk/Projects/shokuknow/lanes/chousa/SOURCES-PROPOSED.md`
(lane dir ⇒ `round1`, quote-lint.py:658-665). IDs drifted: PRISMA-S was S071
(`d9583b5a`), S074 (`9b707a72`), **S077 at census revision `9e91e504`/`a9def15c`**
— matching the register — and S082 at HEAD (line 35). `ID-REMAP.md` maps
`round1 S082→S085`; committed lane `corpus/SOURCES.md` S077 is the pdftotext
manual — a different row; do not confuse them.

Gate block at `9e91e504`, `#### Gate — S077` (lines 47-53):

```
URL: https://doi.org/10.1186/s13643-020-01542-z
Opened: 2026-10-23 (full text retrieved with `aaron papers fetch 10.1186/s13643-020-01542-z`, 110,181 characters;
        the publisher page, PubMed and PMC all serve bot/proof-of-work challenges to a plain fetch)
Quote — Part 2, Checklist: "It is intended to guide reporting, not conduct, of the search."
Quote — Table 1, item 8: "Include the search strategies for each database and information source, copied and pasted exactly as run."
Quote — Table 1, item 13: "For each search strategy, provide the date when the last search occurred."
Quote — Abstract: "each component of a search is completely reported and therefore reproducible."
```

## On-disk captures (only evidence used; no fetch)

1. **Cited-URL cache** — qcache key `sha256(url)[:24]` = `01f657b3d0ab045c494b3f92`
   (`.../corpus-expansion-1/.qcache/`):
   - `.raw` 3,038 B HTML, sha256 `32ed6315…`, a `/_fs-ch-…` challenge shell
   - `.txt` 267 B / 265 chars, sha256 `c42ccd00…`; body: "Client Challenge —
     A required part of this site couldn't load…" (U+2019 at index 79).
   This is a bot wall, **not** the article — so the fetch was not clean.
2. **aaron full text** —
   `/home/vgpnk/Projects/shokuknow/.deepresearch/20261023_171700_prisma-inspired-search-log-format-for-lanes/aaron_10_1186_s13643-020-01542-z.txt`
   — 110,602 B / 110,181 chars (`wc -c -m`; matches the gate's char count),
   sha256 `20f6887699c8e3e10cd167758dbd075b33468bdc5cfaedfa13e69e97664493d7`,
   dated 2026-10-23 17:26. Identity confirmed inside the file:
   `PRISMA-S: an extension to the PRISMA Statement`, `Syst Rev`,
   `10.1186/s13643-020-01542-z`.
3. **Flattened sibling** — same dir `prisma_s.txt`, 77,494 B, sha256
   `d4b3bd4f…`, carries the DOI and all four spans (e.g. quote 1 at
   byte offset 17182).

## Reproduced check (read-only)

```
$ grep -Fbo '<each quote>' aaron_10_1186_s13643-020-01542-z.txt
1441:each component of a search is completely reported and therefore reproducible.
14602:It is intended to guide reporting, not conduct, of the search.
17793:Include the search strategies for each database and information source, copied and pasted exactly as run.
18563:For each search strategy, provide the date when the last search occurred.
```

All four `grep -F` exact-byte hits in capture #2; identical VERBATIM results
in #3. Cache-wide cross-check: `grep -il "guide reporting" .qcache/*.txt|*.raw`
→ zero files; the four PRISMA-cache hits (`0ae65…`, `14aaa…`, `c9d1e…`,
`34fce…`) are the Cochrane ch.4 / JMLA commentary, not the paper.

## Why the census missed it

`quote-lint.py`'s artifact index globs only `lanes/chousa{,/round*}` plus the
fleet `corpus/` dir (lines 250-288). The aaron artifact sits under campaign
`shokuknow/.deepresearch/` — outside every root — so the checker saw only
the bot wall and reported ABSENT, which `absent-defect-register.py` then
mislabeled `payload-absent` (it has no bot-wall test; "clean fetch" is
inferred from `.txt` existence).

## Reason

The quotes are genuine PRISMA-S text, byte-exact, in a locally committed
capture of the cited DOI's article. Row content is true as written; the
register's class and note are the defect. Round-42's `unverifiable`
(bot-wall-only evidence) is resolved upward by the artifact to **present**.
No live fetch performed; L0 `8d77e6c1` untouched. No installs.

Report: .ufo/waves/round-48/w2/QuarantineS077.md
