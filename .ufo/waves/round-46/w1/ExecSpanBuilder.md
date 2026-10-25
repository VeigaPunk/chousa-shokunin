# Round 46 / wave 1 — ExecSpanBuilder (span manifest)

Item: derive `corpus/evidence/round46/spans.tsv` + `spans/*.txt` for the eleven fixed quotes in a /tmp tree, validate with frozen `c3-count.py`, paste offsets, byte lengths and the re-derivation. No lane writes, no fetch, no install.
Span contract: capture = `sha256(url)[:24].txt`; offset = first occurrence; span = `capture[o:o+len(quote)+1]`; row = 7 tab columns `id url capture_sha256 offset span_file quote entry`.
## Commands (verbatim decisive output)
1. `python3 /tmp/chousa-r46-ExecSpanBuilder/build-spans.py --out …/tree` → 11 rows, `rederive … cap_sha=True slice=True quote_in_span=True` ×11, `ROWS=11/11 REDERIVE=11/11`, exit 0; compaction re-run into a fresh tree gave `diff -r` → `TREES_IDENTICAL` and manifest sha256 `7b5d09258d4fc51b1b09562c2ed57f1e06d827bfd2597344453d723c56c645f6` both runs.
2. `c3-count.py --root …/tree` (spans only, entries absent): `ENTRIES=0/2 CITES_BOUND=0/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=0/11 CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=0/2 C3=FAIL`, exit 1.
3. `c3-count.py --root …/tree-live-entries` (my spans + live lane entries + lane `corpus/SOURCES.md`): `ENTRIES=2/2 CITES_BOUND=0/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11 REF_ID_UNBOUND=2 REF_BOUND=2/2 C3=FAIL`, exit 1; `--lane-only` identical with `CAPTURE_BOUND=skipped`.
4. lane root `c3-count.py` (sibling-committed manifest): the same nine numbers as (3), exit 1.
## Manifest — offset in capture chars; chars/bytes of the span file; sha256 abbreviated
| # | id | quote | offset | chars | bytes | after | span sha256 |
|---|----|-------|--------|-------|-------|-------|-------------|
| 1 | S085 | A list of evidence sets | 2360 | 24 | 24 | `' '` | 74cec9a9…1367a7b5 |
| 2 | S085 | Pre-processed Wikipedia Pages (June 2017 dump) | 1271 | 47 | 47 | `' '` | 2ae0885d…d06c13db3 |
| 3 | S086 | used the June 2017 Wikipedia dump, processed | 15269 | 45 | 45 | `' '` | 2e78b837…428e2d5ca1 |
| 4 | S086 | recall of 72.36% | 42011 | 17 | 17 | `'\n'` | 06eeea67…7b75d4982cf |
| 5 | S086 | We found that 91.2% | 20847 | 20 | 20 | `'\n'` | 85e88937…64b5772b45 |
| 6 | S087 | 10.5281/zenodo.4925953 | 186 | 23 | 23 | `'"'` | baf3a0c7…efb50c6fc38 |
| 7 | S087 | wiki-pages.zip | 4937 | 15 | 15 | `'"'` | c062a283…b01557b5e6e1 |
| 8 | S088 | An archive.org link for the source url | 3929 | 39 | 39 | `'.'` | a1091725…747979a846 |
| 9 | S088 | Our best estimate for the date the claim first appeared | 2904 | 56 | 56 | `'.'` | e4245946…34e785d8f3 |
| 10 | S089 | temporally constrained evidence annotation | 3022 | 43 | 43 | `','` | 4a975b89…2b135a9830 |
| 11 | S089 | published before the claim’s date | 7137 | 34 | 36 | `'.'` | a42e4cf9…bd94061aa01 |

Re-derivation from disk (not memory): `CAPTURE_BOUND=11/11` in runs (2)/(3) *is* `capture[o:o+len(span)] == span` for all eleven, plus per-span capture-sha equality from the builder's `rederive` pass (`cap_sha=True slice=True quote_in_span=True` ×11). S087 quotes are non-unique in their capture (3 and 2 occurrences) → first occurrence, deterministic. Capture sha256s: S085 `e18eeb26…1ba92`, S086 `c508913a…d563f`, S087 `dfc3e0f5…e00ed`, S088 `603f9b42…7528b`, S089 `35bdf1c1…7480c`.
## Re-measurement after the registry rows landed (both modes)
`ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=2/2 C3=PASS`, exit 0; `--lane-only` identical with `CAPTURE_BOUND=skipped`. All eleven bare-string quotes are still substrings of the current entry prose (`MISSING=0/11`), so my `+1`/bare-string manifest stays an equivalent alternative; the committed manifest is the lane builder's `len(quote)` one and passes the same eight legs.
## Findings (measured)
- F1 span legs close: with the contract-exact manifest against the live entries all four span legs were 11/11 in both modes at 07:2x, when the only failing legs were the two entry-side ones; both have since landed (re-measurement above).
- F2 `CITES_BOUND` was 0/5 at 07:2x purely from missing Registry rows: all five `source:` lines already matched the counter's regex (True ×5) and `corpus/SOURCES.md` had no S085–S089 row (`grep -c '^| S08'` = 5 → S080–S084). Rows landed at `corpus/SOURCES.md:96–100` (next heading `## Paths` at 101) and the leg now measures 5/5.
- F3 `REF_ID_UNBOUND` was 2 at 07:2x — `S071` and `S095` on `corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md:29`. That line now re-binds the two staged prose ids by document to `S079` (RFC 7089) and `S081` (WARP), `S095` is absent from both entries and the Registry, and the leg measures 0.
- F4 lane manifest (sibling, 07:25) diverges from this dispatch in two ways and both variants pass every span leg: (a) S087 rows quote `"conceptdoi": "10.5281/zenodo.4925953"` @171 (38 B) and `"key": "wiki-pages.zip"` @4929 (23 B) instead of the bare strings @186/@4937; (b) lane spans are `len(quote)` slices (`build-spans.py:69`) vs this wave's `+1`. `QUOTES_IN_ENTRY` passes either way because the bare strings are substrings of the entry prose; offsets 171/4929 vs 186/4937 are the durable datum that differs.
- F5 independent cross-check against ScribeRows' longer fragments: their S085 @2349 + 11 = my 2360, S088 @3909 + 20 = my 3929, S089 @7084 + 53 = my 7137 — my offsets are the exact character positions of the fixed quotes.
- F6 S087's quoted DOI is the record `conceptdoi` (…4925953); the record's own `doi` is …4925954. Prose calling 4925953 the record doi would be false; the live entry says `conceptdoi` (ok).
## Risks / limits
- Scratch tree deleted per seat contract; the builder below reproduces every byte deterministically (first-occurrence offsets, digest-checked).
- `+1` appends a space/quote/punctuation on 9 of 11 spans (those quotes are not newline-terminated); the counter cannot distinguish trailer 0 from 1, so this is a contract-shape choice for the L1, not a correctness one.
- No tools installed or upgraded (pacman paused; nothing needed).
## Builder source (`/tmp/chousa-r46-ExecSpanBuilder/build-spans.py`, 113 lines, as run)
```python
#!/usr/bin/env python3
"""build-spans — derive r46's eleven spans + manifest from on-disk captures (scratch seat tree only).

capture = sha256(url)[:24].txt in the campaign cache; offset = first occurrence of the
quote; span file = EXACT slice capture[offset:offset+len(quote)+1] (quote + the one
character after it, a newline where the capture has one), so the frozen counter's
capture[o:o+len(span)] == span holds by construction; manifest row = 7 tab columns
id url capture_sha256 offset span_file quote entry. Refuses any --out inside the lane.
"""
import argparse, hashlib, pathlib, sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
BASE = "corpus/knowledge/evidence-pool-versioning-r39.md"
AMEND = "corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md"
U = {"S085": "https://fever.ai/dataset/fever.html",
     "S086": "https://aclanthology.org/N18-1074.pdf",
     "S087": "https://zenodo.org/api/records/4925954",
     "S088": "https://fever.ai/dataset/averitec.html",
     "S089": "https://arxiv.org/html/2505.17978v2"}
ENTRY = {"S085": BASE, "S086": BASE, "S087": BASE, "S088": AMEND, "S089": AMEND}
QUOTES = [("S085", "A list of evidence sets"),
          ("S085", "Pre-processed Wikipedia Pages (June 2017 dump)"),
          ("S086", "used the June 2017 Wikipedia dump, processed"),
          ("S086", "recall of 72.36%"),
          ("S086", "We found that 91.2%"),
          ("S087", "10.5281/zenodo.4925953"),
          ("S087", "wiki-pages.zip"),
          ("S088", "An archive.org link for the source url"),
          ("S088", "Our best estimate for the date the claim first appeared"),
          ("S089", "temporally constrained evidence annotation"),
          ("S089", "published before the claim\u2019s date")]
HEADER = "id\turl\tcapture_sha256\toffset\tspan_file\tquote\tentry"


def key(url):
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def build(cache, trailer):
    rows, files, seen = [HEADER], {}, {}
    print("id\ti\toccs\toffset\tq_chars\tspan_chars\tspan_bytes\ttail")
    for i, (sid, quote) in enumerate(QUOTES, 1):
        assert "\t" not in quote and "\n" not in quote, repr(quote)
        cap = cache / (key(U[sid]) + ".txt")
        if not cap.is_file():
            raise SystemExit(f"no capture {cap}")
        text = cap.read_text(encoding="utf-8", errors="replace")
        off = text.find(quote)
        if off < 0:
            raise SystemExit(f"quote absent from {cap.name}: {quote!r}")
        span = text[off:off + len(quote) + trailer]
        if not span.startswith(quote):
            raise SystemExit(f"slice does not start with quote: {sid}")
        seen[sid] = seen.get(sid, 0) + 1
        name = f"spans/{sid}-{seen[sid]}.txt"
        files[name] = span.encode("utf-8")
        rows.append("\t".join([sid, U[sid], sha(cap), str(off), name, quote, ENTRY[sid]]))
        print(f"{sid}\t{i}\t{text.count(quote)}\t{off}\t{len(quote)}\t{len(span)}\t"
              f"{len(files[name])}\t{span[len(quote)] if trailer else ''!r}")
    return "\n".join(rows) + "\n", files


def write_tree(out, manifest, files):
    ev = out / "corpus" / "evidence" / "round46"
    (ev / "spans").mkdir(parents=True, exist_ok=True)
    (ev / "spans.tsv").write_text(manifest, encoding="utf-8")
    for name, blob in files.items():
        (ev / name).write_bytes(blob)
    return ev


def rederive(ev, cache):
    ok = 0
    for line in (ev / "spans.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        sid, url, cap_sha, off, span_file, quote, _ = line.split("\t")
        cap = cache / (key(url) + ".txt")
        span = (ev / span_file).read_text(encoding="utf-8")
        text = cap.read_text(encoding="utf-8", errors="replace")
        good = (sha(cap) == cap_sha and text[int(off):int(off) + len(span)] == span
                and span.startswith(quote) and quote in span)
        ok += good
        print(f"rederive {sid} {span_file} cap_sha={sha(cap) == cap_sha} "
              f"slice={text[int(off):int(off) + len(span)] == span} "
              f"quote_in_span={quote in span} chars={len(span)} bytes={len(span.encode())}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/tmp/chousa-r46-ExecSpanBuilder/tree")
    ap.add_argument("--cache", default=str(CACHE))
    ap.add_argument("--trailer", type=int, default=1)
    a = ap.parse_args()
    out, cache = pathlib.Path(a.out), pathlib.Path(a.cache)
    try:
        out.resolve().relative_to(LANE)
        raise SystemExit(f"refusing to write inside the lane: {out}")
    except ValueError:
        pass
    manifest, files = build(cache, a.trailer)
    ev = write_tree(out, manifest, files)
    ok = rederive(ev, cache)
    print(f"ROWS={len(files)}/11 REDERIVE={ok}/11 TREE={ev}")
    return 0 if len(files) == 11 and ok == 11 else 1


if __name__ == "__main__":
    sys.exit(main())
```
