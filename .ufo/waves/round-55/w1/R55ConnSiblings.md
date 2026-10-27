# R55ConnSiblings — sibling overlap scan (round 55 wave 1)

## Command and targets
Searched 20 sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin/` (excluding `chousa-shokunin`) across target paths (`corpus/`, `tools/`, `SKILL.md`, `PROVINCE.md` — 66 existing roots).
Search terms: 灰色文献, grey literature, NMPA, 上市药品, PRISMA-S, 检索策略, span builder, build-spans, capture-text, quote offset, text form.

```bash
python3 -c '
import glob, os, subprocess
base = "/home/vgpnk/Projects/shokunin"
lanes = sorted([d for d in glob.glob(f"{base}/*-shokunin") if os.path.isdir(d) and not d.endswith("/chousa-shokunin")])
targets = [os.path.join(l, s) for l in lanes for s in ["corpus", "tools", "SKILL.md", "PROVINCE.md"] if os.path.exists(os.path.join(l, s))]
terms = ["灰色文献", "grey literature", "NMPA", "上市药品", "PRISMA-S", "检索策略", "span builder", "build-spans", "capture-text", "quote offset", "text form"]
for t in terms:
    res = subprocess.run(["rg", "-n", "-F", t] + targets, capture_output=True, text=True)
    hits = [h for h in res.stdout.strip().splitlines() if h]
    print(f"{t}: {len(hits)} hits")
'
```
Observed output:
```
灰色文献: 0 hits
grey literature: 0 hits
NMPA: 0 hits
上市药品: 0 hits
PRISMA-S: 0 hits
检索策略: 0 hits
span builder: 0 hits
build-spans: 0 hits
capture-text: 0 hits
quote offset: 1 hits
text form: 19 hits
```

## Hits by term

### 1. Zero-hit terms (exact in target scopes)
- `灰色文献`: 0 hits
- `grey literature`: 0 hits
- `NMPA`: 0 hits (case-insensitive: 0 in target scopes; `kaidoku-shokunin/corpus/.../oracle.tsv:466` has `libsnmpaif.so`, unrelated)
- `上市药品`: 0 hits
- `PRISMA-S`: 0 hits (case-insensitive: 0 in target scopes; `souji-shokunin/census/round-29/waves/w1-results.json:154` has "PRISMA-style", outside target scope)
- `检索策略`: 0 hits
- `span builder`: 0 hits
- `build-spans`: 0 hits
- `capture-text`: 0 hits

### 2. quote offset (1 hit)
- `tabi-shokunin/corpus/QUALITY.md:162`: `quote offset/excerpt are re-derived after decoding those same bytes. Digest-shaped strings`
  - Context: Q39 requires re-deriving quote offsets from retained decoded response bodies.

### 3. text form (19 hits)
- Literal phrases for non-chousa domain concepts:
  - `game-dev-2d-shokunin/corpus/fixtures/res_uid_w07.gd:85`: engine-generated text forms (`*.gd.uid`)
  - `game-dev-2d-shokunin/corpus/fixtures/res_uid_w07.gd:100`: companion file read text form
  - `game-dev-2d-shokunin/corpus/live/r79-baseline/compare.py:40`, `r87-verifier/compare.py:40`, `r87-verifier2/compare.py:40`, `r88-baseline/compare.py:40`, `r88-verifier/compare.py:40`: `# pids in text form`
  - `mori-shokunin/tools/mori-silence-cases.sh:403`: journalctl text form vs structured JSON
  - `mori-shokunin/corpus/knowledge/observability-surfaces-r2.md:184`: system vs user in text form
  - `mori-shokunin/corpus/knowledge/observability-census-r1.md:154`: text form first, JSON count additional
  - `mori-shokunin/corpus/evidence/recheck-r32/S040.src:25`: cursor passed around in text form
  - `kotodama-shokunin/corpus/knowledge/civilizations/mexica-aztec.md:120`: linguistic text forms of Nahuatl terms
- Substring matches on `text format` / `formula`:
  - `kasegi-shokunin/corpus/source-snapshots/round-35/S052.txt:26070` ("rich text format")
  - `mado-shokunin/corpus/SOURCES.md:135` ("its text format")
  - `mado-shokunin/corpus/knowledge/hyprland-gkeep-geometry-r43.md:56` ("plain-text formatter")
  - `mori-shokunin/corpus/evidence/sources-r37/S221.src:7348` ("hypertext format")
  - `kengaku-shokunin/corpus/evidence/round44/tb2-feal-linear-cryptanalysis/feal.c:103` ("plaintext format")
  - `kotodama-shokunin/corpus/lessons/round-1-triage/Z06.md:33` ("ritual-text formula")
  - `tabi-shokunin/corpus/knowledge/webmcp-nonautosubmit-round-21-corrected.md:35` ("page-context form.submit()")

## Sibling ownership analysis

### (a) Search-record reporting standards
**No sibling owns search-record reporting standards.** Sibling lanes explicitly defer research method, search strategy, and citation hierarchy to `chousa-shokunin`:
- `souji-shokunin/PROVINCE.md:82-83`: "chousa-shokunin owns the research method and source hierarchy; souji's `corpus/SOURCES.md` applies it and does not restate it."
- `kotoba-shokunin/PROVINCE.md:57`: "chousa owns the research method, its tools and gates (PROVINCE.md:3-8 at the head); kotoba cites it and never re-derives it"
- `kengaku-shokunin/PROVINCE.md:137`: "research method — `corpus/QUALITY.md` and the SOURCES contract both state the question -> source-hierarchy -> citation-chain -> claim-vs-source method stays chousa's"
- `chousa-shokunin/PROVINCE.md:5-7`: affirmatively owns "question framing; source hierarchy... citation chaining and hop resolution; claim-vs-source verification; search-strategy taxonomy".

### (b) Span/quote locator tool
**No sibling owns a span/quote locator tool.**
- `tabi-shokunin/corpus/QUALITY.md:162` requires quote offsets/excerpts re-derivation, but `tabi`'s checks (`scripts/check-decision-table.mjs:52`) use simple in-memory substring matching in normalized HTML response bodies. `tabi` owns browser interaction, not quote/span extraction tools.
- `kotodama-shokunin/tools/check-gate-quotes.py` validates a 25-word cap in lesson Markdown tables, not text capture span offsets.
- `chousa-shokunin` uniquely owns `tools/build-spans.py` (generating span manifests from capture defined text forms) and `tools/capture-text.py`.

## Verdict
Closest sibling file: `tabi-shokunin/corpus/QUALITY.md:162`.

VERDICT: Sibling overlap scan complete — no overlap on search-record reporting standards or span locator tooling; closest sibling file is tabi-shokunin/corpus/QUALITY.md:162.
