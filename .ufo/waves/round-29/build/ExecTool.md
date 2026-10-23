# ExecTool — `tools/quote-reopen.py` to the frozen v3 tool contract

Seat: ExecTool (executor, leaf, no subagents). Judged on: operability.
Lane clone: `/fast/scratch/hyaku/chousa-r29/w1/ExecTool/lane` (clone of the lane,
reset to `66bf1b9300733b24e76efe393646b3037402080e`).
Delivered file: `.ufo/waves/round-29/build/ExecTool/quote-reopen.py`, 440 lines,
SHA-256 `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea`.
Read before writing: `corpus/evidence/round29/claims.md` (frozen contract, v3),
`corpus/evidence/round29/c1-count.py` (frozen counter, SHA-256
`cd50965032278c355f780d357c5672f14840fc218bb1b7dc4adaa6993b5c175d`),
`corpus/SOURCES.md`, `corpus/lessons/round-28-verifier-spotcheck.md`,
`.ufo/waves/round-29/build/SentinelFetchBounds.md`.

## Verdict

C1's after value is reached on the frozen counter, unseeded, nine times:

`QUOTE_REOPEN_MATCH=130/130`, counter exit `0`, `predicate_holds=True`.

## What the tool does

CLI `verify --items ITEMS.tsv [--registry SOURCES.md]`. Verdict order
NO_SOURCE > TOO_LONG > UNREACHABLE > VERBATIM/ABSENT. Output is
`QUOTE_REOPEN<TAB>id<TAB>VERDICT<TAB>detail` in input order, then
`QUOTE_REOPEN_SUMMARY verbatim=… absent=… too_long=… no_source=… unreachable=…`.
Exit 0 only when every item is VERBATIM, 1 when any item carries another verdict,
2 on a usage or input/output error. Default registry is `corpus/SOURCES.md` under
the parent of `tools/`, resolved from `__file__`, so it holds under any working
directory.

Rules implemented as the contract states them: NFKC first, then the four
typographic single quotes to `'`, the four double quotes to `"`, deletion of
U+00AD U+200B U+200C U+200D U+FEFF, whitespace collapse by `str.split`, strip;
`html.parser` with `convert_charrefs=True`, content of `script style noscript
template head` and comments dropped, the exact 31-element block list emitting one
space at start and end; case-sensitive match with the non-alphanumeric boundary
rule on both sides.

## Evidence

### Counter runs (from the clone root, unseeded v3 counter)

Command shape, nine times:
`python3 corpus/evidence/round29/c1-count.py --receipt <dir>/receipt-v3-run<N>.json -- python3 tools/quote-reopen.py verify`

| run | seed | `QUOTE_REOPEN_MATCH` | counter exit | receipt |
|---|---|---|---|---|
| 1 | 15018527867440131039 | 130/130 | 0 | `receipt-v3-run1.json` |
| 2 | 2889479057100865372 | 130/130 | 0 | `receipt-v3-run2.json` |
| 3 | 14757313487062423439 | 130/130 | 0 | `receipt-v3-run3.json` |
| 4 | 14053332335586484186 | 130/130 | 0 | `receipt-v3-run4.json` |
| 5 | 2464196529495521496 | 130/130 | 0 | `receipt-v3-run5.json` |
| 6 | 2881458727613914661 | 130/130 | 0 | `receipt-v3-run6.json` |
| 7 | 9607448982071204361 | 130/130 | 0 | `receipt-v3-run7.json` |
| 8 | 8063707200229870254 | 130/130 | 0 | `receipt-v3-run8.json` |
| 9 (delivered bytes, fresh clone) | 11907449071710365797 | 130/130 | 0 | `receipt-v3-delivered.json` |

Every receipt records `"predicate_holds": true`, `"tool_exit": 1`,
`"stderr_tail": ""`. `tool_exit` 1 is the contract's own rule: the item set
contains ABSENT, TOO_LONG and NO_SOURCE items by design, and exit 0 is reserved
for an all-VERBATIM run. The measured `exit 0` in the claim is the counter's.

Per-class result on run 6, identical on every run: frozen fixture classes
9/9, 3/3, 2/2, 3/3, 1/1, 2/2, 4/4, 4/4, 4/4, 4/4, 4/4 and the run-time classes
`runtime-subspan 14/14`, `runtime-transpose 14/14`, `runtime-crossattr 14/14`,
`runtime-page-window 24/24`, `runtime-page-transpose 24/24`.

`wall_s` for the tool subprocess was 2.23 s to 2.32 s per run.

### Self-test (30 cases, only my own strings and my own items files)

`python3 selftest.py` from the clone root, and again from the fresh clone holding
the delivered bytes: `Ran 30 tests ... OK`, exit 0. Cases cover NFKC and the four
single and four double quote folds, the five deleted code points, whitespace
collapse, `script/style/noscript/template/head` and comment dropping, the block
space rule, inline elements emitting nothing, `handle_startendtag`, charref
decoding, the boundary rule on both sides, case sensitivity, registry URL
extraction and trailing `.,;)` strip, `NO_SOURCE` outranking `TOO_LONG`, gzip and
identity bodies, the wire and inflated 8 MiB caps, refusal of `ftp:` `file:`
`data:` and userinfo, refusal of loopback and private addresses, and a failure
detail that carries no URL.

### Fetch bounds actually exercised

* One connection per distinct URL: instrumented run over 10 items on 2 registry
  rows opened 2 connections to 2 hosts (`docs.python.org:443`,
  `jsonlines.org:443`). The in-memory cache is keyed by URL, so each URL is
  fetched once per run and rows sharing a URL cost one fetch.
* No disk write: a before/after walk of the clone tree around a full run shows
  `new files after run: []`. Page text lives only in a process-local dict.
* `detail` never carries a URL or an exception message: a fetch of
  `https://alice:s3cr3t@example.invalid/x` returns
  `detail = "url carries userinfo"`.

### Security findings folded in (T1 to T7 of the sentinel report)

T1 both the registry URL and every redirect hop are refused unless every address
the host resolves to satisfies `ipaddress.ip_address(...).is_global`, which
excludes loopback, private, link-local and the metadata ranges. T2 the tool uses
`http.client` directly, so no `FileHandler`, `DataHandler`, `FTPHandler` or
ambient proxy handler exists, and a redirect whose scheme is not `http`/`https`
is refused before a connection. T3 the wire bytes and the inflated bytes are both
capped at 8 MiB + 1, inflation runs through `zlib.decompressobj(...).decompress`
with `max_length`, and an unsupported `Content-Encoding` is refused rather than
read raw. T4 one monotonic deadline of 30 s per URL spans every redirect hop, the
body read and the single retry; each read re-arms the socket timeout to the
remaining budget. T5 `http.client.HTTPException`, `InvalidURL`, `OSError`,
`ValueError`, `UnicodeError`, `ssl.SSLError` and `zlib.error` are all caught and
mapped to UNREACHABLE for that item, so one bad host cannot abort the run. T6 a
URL with userinfo is refused and no URL or exception text is printed. T7 memory
only, and stdout carries exactly the contract lines.

### Registry parity

`adhoc/check_registry.py` (scratch) compared my row parser against the contract's
lookup logic transcribed from `claims.md` over `corpus/SOURCES.md`: at the
committed revision `registry rows parsed: 45`, `url mismatches vs reference
transcription: []`, `ids only in file: []`, `ids only parsed: []`; re-run with the
working-tree rows S046 to S049 present, `registry rows parsed: 49` and still zero
mismatches, 49 ids in file and 49 parsed.

### Tool has no fixture or id knowledge

`grep -nE 'S[0-9]{3}|<fixture ids>' tools/quote-reopen.py` → none found.
`grep -nE 'https?://[a-z]' tools/quote-reopen.py` → none found. The only files
opened are the items file and the registry.

## Basis sources S046 to S049

The four rows are in the lane working tree's `corpus/SOURCES.md` (added by other
seats in this wave; I did not write or edit them). I re-opened three of them and
matched a quote I copied myself, through the delivered tool:

| row | URL opened | my quote | verdict |
|---|---|---|---|
| S046 | `https://www.w3.org/TR/annotation-model/` (fragment stripped per contract) | "This Selector describes a range of text by copying it, and including some of the text immediately before (a prefix) and after (a suffix) it" (25 words) | VERBATIM |
| S048 | `https://unicode.org/reports/tr15/` | "Normalization Forms KC and KD must not be blindly applied to arbitrary text." | VERBATIM |
| S049 | `https://docs.python.org/3/library/html.parser.html` | "all character references (except the ones in elements like script and style) are automatically converted to the corresponding Unicode characters" | VERBATIM |
| S047 | `https://wicg.github.io/scroll-to-text-fragment/` | "Context terms are used to disambiguate the target text fragment." | ABSENT |

Access date recorded as 2026-10-23, the round's date convention; this session's
clock reads 2026-10-22.

## Risks and limits

1. **S047's page cannot yield a VERBATIM verdict under the frozen rule.** The
   served page has one `<head>` start tag and no `</head>`, so the contract's skip
   counter never returns to zero and the extracted text is empty (measured:
   `doc len 366456`, `html_to_text len 2869` of which all is inter-tag space,
   `norm` result empty). The frozen counter's reference functions use the same
   skip counter, so this is contract-faithful, not a defect in my file — but a
   quote from that page can never be located, so `corpus/knowledge/quote-reopen-r29.md`
   should not lean on S047 as tool-verified. S047 is not one of the eight
   fixture sources, so the 130/130 measurement is unaffected.
2. **Extraction is the reference's, deliberately.** The tool reproduces the
   frozen reference functions element for element. Where the reference is coarse
   (an unclosed `head`, a `template` never closed), the tool is equally coarse.
   Diverging would have broken the page-window labels; I did not.
3. **Address check and DNS.** The global-address test runs before connect and is
   repeated per redirect hop, but the connect resolves again, so a hostile
   resolver could in principle answer differently between the check and the
   connect. The sentinel's note asks for the resolved-peer check, which is what
   this does; closing the remaining window would need a pinned-IP connect.
4. **No proxy support.** The tool speaks `http.client` directly, so an
   environment that requires an egress proxy would return UNREACHABLE. No proxy
   variable is set on this host.
5. **Network variance is outside the tool's control.** The page-window items are
   sampled by the counter from its own two fetches of each source, and the tool
   fetches a third time. Ten unseeded runs agreed 130/130; a page that changed
   between the counter's fetch and the tool's could still miss, and a miss is
   reported as a miss, not re-scaled.
6. **Named fidelity limit from the sentinel, kept as the contract states it.**
   `rstrip(".,;)")` also removes a legitimate `)` ending a URL path. No registry
   row ends that way today.

## Installs

None. No package was installed or updated; the tool and the self-test use only
the Python 3.14.8 standard library already on the host.

## Files written by this seat

* `.ufo/waves/round-29/build/ExecTool.md` (this report)
* `.ufo/waves/round-29/build/ExecTool/quote-reopen.py` (the deliverable)
* `.ufo/waves/round-29/build/ExecTool/selftest.py` (30-case contract self-test)
* `.ufo/waves/round-29/build/ExecTool/receipt-v3-run1.json`,
  `.ufo/waves/round-29/build/ExecTool/receipt-v3-run8.json`,
  `.ufo/waves/round-29/build/ExecTool/receipt-v3-delivered.json`

Scratch only, not delivered: `/fast/scratch/hyaku/chousa-r29/w1/ExecTool/`
(clone, `adhoc/items.tsv`, `adhoc/items2.tsv`, `adhoc/check_registry.py`,
`adhoc/check_bounds.py`, `receipt-v3-run2..5.json`, `receipt-v3-delivered.json`,
`verify/lane2`). No git or jj write command was run in the lane or the fleet
repo; the lane's index and working tree were not touched.

Report: .ufo/waves/round-29/build/ExecTool.md
