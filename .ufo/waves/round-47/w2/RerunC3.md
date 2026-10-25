ATTACKS: C3 after-state — re-ran c3-count (default + --lane-only) and build-spans --check on a /tmp archive of lane tip 1fc5ed193ad48a482402c862f4e4cc47e46d5b2d; independently verified all 35 spans.tsv rows (capture sha256, span slice, quote in span, quote in citing entry, quote uniqueness, span context), anchor char offsets, registry rows, quarantine verdicts vs absent-defect register, and inference-ground grounding.
VERDICT: holds

Commands and decisive output:

$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 1fc5ed193ad48a482402c862f4e4cc47e46d5b2d | tar -x -C /tmp/chousa-r47w2-RerunC3/tree
EXTRACT_OK

$ python3 /tmp/chousa-r47w2-RerunC3/tree/corpus/evidence/round47/c3-count.py --root /tmp/chousa-r47w2-RerunC3/tree
ENTRIES=2/2
CITES_BOUND=6/6
QUOTE_ROWS=35 (min 12)
SPAN_IDS=6/6
QUOTES_IN_SPAN=35/35
QUOTES_IN_ENTRY=35/35
SPAN_CONTEXT=35/35
CAPTURE_BOUND=35/35
REF_ID_UNBOUND=0
ANCHOR_BOUND=6/6
INFERENCE_GROUNDED=2/2
QUARANTINE_VERDICTS=4/4
QUARANTINE_ABSENT_ADOPTED=0
C3=PASS
exit=0

$ python3 .../c3-count.py --root ... --lane-only
CAPTURE_BOUND=skipped
C3=PASS
exit=0

$ python3 .../build-spans.py --root ... --check
SPANS_ROWS=35 STALE=0
exit=0

Independent verification (own Python, strict utf-8; counter uses errors="replace" — my check is stricter):
- All 35 rows: capture `sha256(url)[:24].txt` exists and byte-sha256 == capture_sha256; decoded `capture[offset:offset+len(span)] == span`; quote in span; quote in citing entry text (lane-relative path); quote occurs exactly once in capture; len(span) > len(quote).
- FAILS 0 / ALL35_OK.
- Anchor char offsets from SOURCES.md all bound to computed quote offsets (span offset + span.find(quote)):
  S085 [2360,1271], S090 [1526,1576,1669], S091 [966,1567,10406], S092 [2821,2849,6601], S093 [5157,13373,16287], S094 [19167,20462,20650].
- No duplicate (id,quote) rows; spans/ dir has no orphans and no missing files; quotes.tsv = 35 rows = spans.tsv rows.
- Entry S### tokens {S085,S086,S090,S091,S092,S093,S094} all within S079–S094.
- Registry rows for S085/S090–S094: url matches source line, status `mined`, citing entry in used-by (c3-count CITES_BOUND=6/6 re-asserts).

$ python3 tools/inference-ground.py --entry <entry> --spans corpus/evidence/round47/spans.tsv --counts /dev/null --registry corpus/SOURCES.md --root <archive> --quiet
claim-support-test-r37.md exit= 0
claim-support-test-r37-amendment-2026-10-23.md exit= 0

Quarantine: round-47.md carries verdict `present` lines for register S093 (https://aclanthology.org/2026.findings-acl.19.pdf), S094 (https://ojs.aaai.org/index.php/AAAI/article/download/29825/31432), S108 (https://arxiv.org/html/1803.05355), S110 (https://aclanthology.org/2025.coling-main.108.pdf) — 4/4, none `absent`; absent-defect-register.md holds the four chousa `payload-absent` rows (register lines: S093 chousa round2, S094 chousa round2, S108 chousa round3, S110 chousa round3).

Agreement with measure-after.txt: every printed line of the c3-count runs (default and --lane-only) and build-spans --check matches measure-after.txt lines 37–73 exactly (C3=PASS, exit=0, SPANS_ROWS=35 STALE=0). No disagreement found. (measure-after's C2 line ENTRY_POINTS=94/exitentation0 concerns C2, out of my C3 scope; RerunC2 covers it.)

Residual risk: spans.tsv is not field-validated (malformed id/entry cells would still count toward row totals), but all 35 committed rows are valid per the independent check; the counter is self-referential by design (spans derived from captures via build-spans), so the claim holds exactly as worded.
