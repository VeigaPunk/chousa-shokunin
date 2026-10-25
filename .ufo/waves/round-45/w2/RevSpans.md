# Review: spans.tsv (round 45, wave 2) — RevSpans

Seat: L1Chousa45.RevSpans. Item attacked: every row of
`corpus/evidence/round45/spans.tsv` at lane commit
5e8c7ad2f7b8254d83358820286e3d12ca4672d1 — capture-hash match, span/offset
alignment, quote containment + uniqueness, quote verbatim in citing entry.

Measurement: committed bytes extracted via `git archive 5e8c7ad2f7b8254d83358820286e3d12ca4672d1 | tar -x` into
`/tmp/chousa-r45-RevSpans/tree`; all checks run from inside that tree. Captures
read from `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`
(read-only). Scratch deleted at end. No lane writes, no network.

## Method (one Python pass over all 4 rows)

- `fn = sha256(url).hexdigest()[:24] + '.txt'`; byte sha256 of that capture file
  vs `capture_sha256` column.
- `span` = committed `spans/<id>.txt` decoded utf-8; `text` = capture decoded
  utf-8; check `text[offset:offset+len(span)] == span` (Python char offsets).
- Check `quote in span` and `text.count(quote) == 1`.
- Check `quote in (committed citing entry)` (utf-8).

## Per-row verdicts

| Row | capture exists | sha256 match | span==cap[off:off+len] | quote in span | quote count in capture | quote in citing entry | Verdict |
|-----|----------------|--------------|------------------------|---------------|------------------------|------------------------|---------|
| S082-1 (README.md, off 1809) | yes | yes (8e1f5bff76c14672…) | yes (len 358) | yes | 1 | yes | HOLDS |
| S082-2 (README.md, off 867) | yes | yes (8e1f5bff76c14672…) | yes (len 381) | yes | 1 | yes | HOLDS |
| S083-1 (arxiv 2305.13117v3, off 14415) | yes | yes (a3ff65e0db9cc4f2…) | yes (len 379) | yes | 1 | yes | HOLDS |
| S083-2 (arxiv 2305.13117v3, off 120724) | yes | yes (a3ff65e0db9cc4f2…) | yes (len 360) | yes | 1 | yes | HOLDS |

Decisive output (verbatim, condensed per row):
```
capture file exists: True | sha match: True | col-sha: 8e1f5bff76c14672 | actual: 8e1f5bff76c14672
span==cap[off:off+len]: True off 1809 len(span) 358 len(text) 4771
quote in span: True | quote count in capture: 1
quote verbatim in citing entry: True
```
(same pattern for S082-2 off 867 len 381; S083-1 off 14415 len 379 len(text) 144049;
S083-2 off 120724 len 360). Capture filenames used: `ce16d57277fedfd4f0e7750e.txt`
(S082) and `412b146a2720ce6557268d05.txt` (S083) = sha256(url)[:24].

## Verdict

All 4 spans.tsv rows HOLD. No defect found. The spans are exact slices of the
captures at the recorded char offsets, quotes are contained in their spans,
unique in the capture, and appear verbatim in the citing entry
(`corpus/knowledge/evidence-archive-field-policy-r41.md`).

## Residual risk / verification gaps

- `capture_sha256` is verified against the `.txt` (reader-extracted) capture; the
  parallel `.raw` files were not part of the claimed contract and were not
  checked.
- Span boundaries (start/end) were not semantically validated against the source
  page structure — only the recorded offset/quote contract was checked; offsets
  are consistent with the quote sitting inside the span.
- No live fetches performed (fetch-scope L0 open); capture existence was
  confirmed on disk.
