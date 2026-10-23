# Round 29 liveness wording drafts

## A. Append-only correction block for SCORECARD.md

Place this dated block immediately below the round 29 capabilities table. Draft only; not applied.

### 2026-10-23 correction — capabilities-row wording

The phrase “live URL” in the round 29 capabilities row is not shown by the round 29 counter. The counter can be met without a network fetch: the cache-only verifier described in `.ufo/waves/round-29/falsify/CriticClaimDesign.md` scored 130/130. Separate network evidence is `.ufo/waves/round-29/falsify/DiffToolB/landed-fixture.network.json`, bound by `.ufo/waves/round-29/falsify/DiffToolB/differential-receipt.json`: the `landed-fixture` network record has 8 allowed request events with `"method": "GET"` and 8 response entries with `"status": 200`. The bound run records `"production_bytes_unchanged": true`, 40 expected and 40 observed items, and the command and exit shown below. Its verdict summary is `verbatim=14 absent=20 too_long=3 no_source=3 unreachable=0`. This is evidence for those GETs and HTTP 200 responses in that one fixture run, not evidence that the counter itself fetches or that every registered URL is reachable. [INFERENCE] Keep the row's counter result distinct from this bounded network observation.

Recorded command (from `differential-receipt.json`; not rerun by this seat):

```text
timeout --kill-after=5s 590s python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/DiffToolB/guarded-run.py /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/DiffToolB/landed-fixture.network.json tools/quote-reopen.py verify --items corpus/fixtures/quote-reopen-r29/items.tsv --registry corpus/SOURCES.md
```

The receipt records `cwd` `/home/vgpnk/Projects/shokunin/chousa-shokunin`, `exit_code` 1, `expected_count` 40, `observed_count` 40, and `production_bytes_unchanged` true. The exit and mixed verdict summary are reported as recorded, not interpreted as a pass.

## B. Case-insensitive `live` grep inventory

Search used `functions.grep(pattern="live", case=false)` on each named surface, then the round 29 section was scoped by its headings. Receipt assessment is deliberately bounded: `landed-fixture.network.json` plus its binding receipt establish only the recorded requests; the cited counterexample and loopback evidence do not establish an external fetch.

| Surface and line | Matching wording | Receipt assessment |
|---|---|---|
| `corpus/lessons/round-29.md:1` | “against their live source” | The DiffToolB network receipt backs a bounded instance: 8 GETs and 8 HTTP 200 responses in one fixture run; not a general statement about every URL. |
| `corpus/lessons/round-29.md:6` | “against the live URL named by `corpus/SOURCES.md`” | Same bounded external-network evidence; the counter result alone does not back it. |
| `corpus/lessons/round-29.md:78` | “re-opening against live sources” | Same bounded evidence only. |
| `corpus/lessons/round-29.md:96` | “not that the answering process fetched live” | The cited cache-only counterexample in `CriticClaimDesign.md` supports the limit; it is not positive network evidence. |
| `corpus/lessons/round-29.md:98` | “Live fetching is evidenced by the loopback harness” | The line cites `OfflineConformance.md` for loopback hits (65/65 with the address guard disabled; 20/64 as landed). That supports loopback harness activity, not public-URL GETs. |
| `corpus/knowledge/quote-reopen-r29.md:1` | “against their live source” | DiffToolB backs only its recorded 8 GET/200 responses; not every URL or invocation. |
| `corpus/knowledge/quote-reopen-r29.md:107` | “does not prove a live fetch” | The cache-only 130/130 counterexample supports this limitation; it does not show external fetches. |
| `corpus/knowledge/quote-reopen-r29.md:112` | “re-opens pages live comes from elsewhere” | The adjacent cited support is loopback-only. The separate DiffToolB receipt now supplies bounded external-GET evidence for one fixture run, though this line does not cite it. |
| `SCORECARD.md:1617` | “counter does not prove a live fetch” | Supported by the cache-only counterexample at `falsify/CriticClaimDesign.md`; no positive network evidence in the counter. |
| `SCORECARD.md:1619` | “Liveness rests on the loopback harness” | The cited `falsify/OfflineConformance.md` evidence is loopback harness activity, not a public-URL fetch. |
| `SCORECARD.md:1635` | “live URL” | The row's cited counter does not establish this. The DiffToolB receipt supplies bounded evidence for the one landed-fixture run and should be cited separately. |
| `corpus/README.md:932` | “against their live registered” | DiffToolB backs a bounded one-run instance, not universal availability or all registry URLs. |
| `LOG.md`, round 29 section (`1186-1201`) | No `live` match | No round 29 `live` wording found in the searched section. |

Additional frozen-file scope note: the spot-check also points to `corpus/evidence/round29/claims.md:41-42` (“against the live source”). That file was opened but was outside the five-surface grep list; it remains unchanged.
