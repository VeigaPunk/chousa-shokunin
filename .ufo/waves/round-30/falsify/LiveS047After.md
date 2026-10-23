VERDICT: pass — against the real S047 page (https://wicg.github.io/scroll-to-text-fragment/, no `</head>`) the round-29 tool reports ABSENT and the landed tool VERBATIM on all three items; C1 head-boundary behavior reproduced on the page it was built for.

Evidence:
- Fetched S047 once (registered in corpus/SOURCES.md): `timeout 60 curl -fsSL --max-filesize 8000000 https://wicg.github.io/scroll-to-text-fragment/ -o s047.html`; 368361 bytes; `grep -c -i "</head" s047.html` = 0, one `<head>` start tag → headless page confirmed.
- Items TSV (3 items, written to /fast/scratch/hyaku/chousa-r30/w2/LiveS047After/items.tsv): `s047-gate` Gate quote "Intuitively, this is a case-insensitive search also ignoring accents, umlauts, and other marks." (13 words); `s047-wordbounded` "Intuitively, a substring is word bounded if it neither begins nor ends in the middle of a word." (18 words); `s047-useful` "Text directive links can be useful despite this problem." (9 words). All three pre-checked to match the landed tool's own `norm(html_to_text(doc))` on the local copy (found=True for each).
- Round-29 tool: `git show a3a3710e:tools/quote-reopen.py > …/r29.py` (440 lines, SHA-256 72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea).
- From lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`:
  - Landed: `python3 tools/quote-reopen.py verify --items …/items.tsv` → `QUOTE_REOPEN_SUMMARY verbatim=3 absent=0 too_long=0 no_source=0 unreachable=0`, exit 0 (VERBATIM ×3, "matched in normalized page text").
  - Round-29: `python3 …/r29.py verify --items …/items.tsv --registry corpus/SOURCES.md` → `QUOTE_REOPEN_SUMMARY verbatim=0 absent=3 too_long=0 no_source=0 unreachable=0`, exit 1 (ABSENT ×3, "no match in normalized page text").
- No counters, harness, claims.md, sources, or lane files edited; nothing installed (no package changes needed). Report path relative to lane: `.ufo/waves/round-30/falsify/LiveS047After.md`.
