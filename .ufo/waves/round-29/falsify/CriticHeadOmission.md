# CriticHeadOmission — bounded registry head-omission sweep

## Scope, axes, local verdict

Attacked the Wave-1 extraction limit: whether omitted `</head>` tags make real body quotes `ABSENT`, how many registry URLs exhibit it, and whether any C1 fixture page is exposed.

Axes: **operability**, body-quote correctness, source provenance, bounded network / no harm.

**Verdict: HOLDS for the stated limitation and fixture-isolation characterization.** The S047 failure reproduces; no additional omitted-head HTML response was found. This is not a canonical C1 judgment: the frozen counter was not rerun, changed, or re-scaled. No frozen-predicate falsification is established by this attack.

## Counts and affected-page list

One bounded GET was issued for each of **35 distinct source-column URLs**, covering **40 registry rows**. All 35 requests completed; there were no retries or followed redirects. Each request had a 25 s deadline and 8 MiB wire / inflated caps. The sweep used the landed tool's User-Agent and requested gzip, with no cookies or credentials sent.

- **31 responses were 2xx HTML**; exactly **1** lacked a head end-tag event: **S047**.
- **32 HTML responses total**, including the S014 403 error body; again only **S047** lacked the tag.
- The other responses were **2 PDFs** and **1 empty 301 redirect**, not additional HTML head-omission cases.
- **0 of the 8 C1 fixture pages** lacked the tag.

| id | registry URL | has `</head>` | landed tool on a true body quote |
|---|---|---|---|
| S047 | https://wicg.github.io/scroll-to-text-fragment/ | no | `ABSENT`, exit 1 |

Copied quote, exactly 10 whitespace-separated words:

> Context terms are used to disambiguate the target text fragment.

It occurs in the captured page's body, section 3.2.1 Context Terms, at [S047.html line 1031](CriticHeadOmission/S047.html). `<body>` occurs at line 812. HTMLParser tag events show **1 head start, 0 head ends, 1 body start**. An independent body-only extraction contains **98,413 normalized characters** and the exact quote passes the landed boundary matcher there; the unchanged landed full-document extractor produces **0 normalized characters**. The period is copied from the source, not the comma-ended quotation in the knowledge entry.

The complete deduplicated list, including IDs, URLs, status, content type, head-end presence and actual/not-run verdict, is [registry-pages.tsv](CriticHeadOmission/registry-pages.tsv). Non-HTML entries use `None` rather than being counted as malformed HTML. Pages with a closing head tag were not given extra quote runs; the assignment required the one-row probe for omitted-head pages only.

## C1 fixture exposure

Each of these source pages returned HTTP 200 HTML with a head end-tag event:

| fixture id | registry URL | has `</head>` |
|---|---|---|
| S002 | https://ifcncodeofprinciples.poynter.org/the-commitments | yes |
| S003 | https://hapgood.us/2019/06/19/sift-the-four-moves/ | yes |
| S008 | https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-02 | yes |
| S013 | https://jsonlines.org/ | yes |
| S019 | https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv | yes |
| S020 | https://www.w3.org/TR/2013/REC-prov-o-20130430/ | yes |
| S038 | https://docs.python.org/3/library/datetime.html | yes |
| S044 | https://docs.python.org/3/library/os.path.html | yes |

This establishes no exposure to this specific head-omission mechanism in the fixture responses, not correctness of every possible quote or a fresh `130/130` result.

## Exact landed-tool probe and provenance

To honor ONE live GET per URL, the CLI probe **replayed the already captured S047 HTTP response at the HTTPConnection transport seam**, rather than fetching the source again. Only the HTTP/HTTPS connection classes were substituted. The original registry, landed script, CLI argument parser, global-address DNS check, gzip inflation, charset handling, HTML extraction, normalization, word limit, boundary matcher, output and exit-code path executed unchanged. No loopback server was needed. This is a cached-response CLI execution, not a second live-fetch invocation.

Logical landed CLI argv:

```text
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/quote-reopen.py verify --items /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/CriticHeadOmission/S047.items.tsv
```

Actual bounded commands, in order:

```text
timeout --kill-after=2s 50s python3 -B /fast/scratch/hyaku/chousa-r29/w2/CriticHeadOmission/head_sweep.py
# exit 0; source_url_rows=40, unique_urls=35, fetch_complete=35,
# successful_html_urls=31, successful_html_missing_head_end=["S047"]

timeout 10s git show 30c9d24da1815e01e161ed2f52d5f951005cc2b8:tools/quote-reopen.py | timeout 10s sha256sum
# exit 0; 72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea

timeout --kill-after=2s 20s python3 -B /fast/scratch/hyaku/chousa-r29/w2/CriticHeadOmission/replay_cli.py
# exit 1; output below

timeout --kill-after=2s 20s python3 -B /fast/scratch/hyaku/chousa-r29/w2/CriticHeadOmission/audit_cached.py
# exit 0; html_responses=32, successful_html_responses=31,
# html_responses_missing_head_end=[["S047"]], fixture_ids_affected=[]
```

Probe output:

```text
QUOTE_REOPEN	head-omission-S047	ABSENT	no match in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=0 absent=1 too_long=0 no_source=0 unreachable=0
REPLAY_EXIT_CODE=1 REPLAY_EVENTS=1 FRESH_NETWORK_GETS=0
```

The current script's SHA-256 equals the script at the named landed commit:
`72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea`.
Registry snapshot SHA-256:
`d8aa0454b50bbe229f255885c970660540f8ecf5bac633ec136165b3425819be`.
S047 decoded source body SHA-256:
`37510e6ba14ae3a6fe166c10f3bb1d2194029c01e3d6acf433395ac6b00306bf`.

Evidence: [sweep.json](CriticHeadOmission/sweep.json), [tag-audit.json](CriticHeadOmission/tag-audit.json), [one-row items](CriticHeadOmission/S047.items.tsv), [CLI receipt](CriticHeadOmission/S047.run.json), [HTTP response metadata](CriticHeadOmission/S047.response.json), and captured `.wire`, `.body`, `.html` files beside them. The harness sources remain in the authorized scratch directory. Python was 3.14.8 (`timeout 10s python3 --version`, exit 0). No tool installation or update was performed.

## Limits and smallest safe correction

This is an observed-response bound, not a claim about every underlying publisher page or future fetch. S014 returned a CloudFront 403 error document with a closing head tag. S021/S032 and S022/S030 returned HTTP 203 cookie/JavaScript challenge documents with closing head tags, not the papers. S025 returned an empty 301 pointing to a URL outside the allowed source-column set; it was not followed. S011 and S037 were PDFs, which C1 explicitly excludes. These inaccessible/challenge targets' underlying HTML structure was not established; they must not be counted as confirmed clean source bodies.

The smallest safe correction **within the frozen round** is interpretation: `ABSENT` means absent from the contract-extracted normalized text, not absent from a browser-visible body. The existing knowledge entry's Limits section already warns about S047. The real body quote here is false-negative evidence for that broader interpretation, but `ABSENT` follows the frozen Python-parser extraction rule. Silently adding implicit head closure or relabeling this item would change the frozen contract, not repair a demonstrated C1 implementation mismatch. No production edit or predicate/fixture adjustment is proposed.

Only the assigned report and evidence directory were written in the lane; code experiments were confined to the authorized scratch directory. No git/jj/index writes, subagents, background jobs, or retained processes were used.
