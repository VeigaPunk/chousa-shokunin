# OfflineConformance — round 29 wave 2

**Verdict: INCONCLUSIVE for frozen C1 and mutation scoring.** No remaining offline conformance defect was found after the explicitly authorized, scratch-only global-address-check bypass. The baseline detector fails because its loopback fixtures conflict with intentional T1 hardening; this is not a killed mutant or a C1 falsification.

**Axes:** operability/conformance, detector discrimination, exact restoration/isolation.

## What was attacked

The wave-1 loopback conformance harness was run against the landed `tools/quote-reopen.py verify`, then against identical pristine, one-line-mutated and exactly restored scratch bytes. No frozen claim, counter or corpus fixture was changed. The frozen live-source `c1-count.py` predicate was not run in this assignment.

The lane harness changed concurrently: the initial requested direct invocation had 64 checks; the subsequent immutable scratch snapshot had 65, adding the missing-items-file exit-2 check. All paired pristine/mutated/restored runs used the same pinned 65-check harness and the same supplemental detector. The original direct run is retained separately, not silently combined with a different detector denominator.

## Actual outputs

| Phase | Wave-1 harness | Supplemental detector |
|---|---|---|
| Landed direct | `OFFLINE_TEST_PASS=20/64`; exit 1 | `EXTRA_CONFORMANCE_PASS=1/2`; exit 1 |
| Pinned pristine | `OFFLINE_TEST_PASS=21/65`; exit 1 | `EXTRA_CONFORMANCE_PASS=1/2`; exit 1 |
| One-line address-check bypass | `OFFLINE_TEST_PASS=65/65`; exit 0 | `EXTRA_CONFORMANCE_PASS=2/2`; exit 0 |
| Pinned restored | `OFFLINE_TEST_PASS=21/65`; exit 1 | `EXTRA_CONFORMANCE_PASS=1/2`; exit 1 |

All detector stderr streams were empty. The mixed candidate run exited 1 as required. With the bypass, the all-verbatim candidate run exited 0, and the missing-input candidate run exited 2.

**44 of 64 initial checks, and the same 44 of 65 pinned checks, fail only because loopback is rejected:** 35 primary item verdicts and 9 derived summary/request/exit/default-registry checks. The all-verbatim singleton and default-registry rerun are included in those 9 checks; the latter repeats the same 35 item mismatches. Every one becomes a pass when only the global-address guard is disabled. Diagnosis for each is **test-policy incompatibility, not a tool defect**. The separate file-redirect detector has 1 additional policy-blocked check on pristine/restored bytes and no failures with the bypass.

Baseline primary verdicts that expected UNREACHABLE (404, PDF, non-HTTP redirect, oversize body) also pass without reaching those conditions, so baseline passes alone do not establish those behaviors. The bypass run removes that confound.

## Supplemental bounded cases

The existing harness tests a redirect to `gopher:`, not specifically `file:`. The scratch supplemental detector tests a loopback HTTP 302 to an owned scratch `file:` URI, and directly records whether a 26-word quote causes a fetch. With the bypass, its actual candidate output was:

```text
COMMAND=/usr/bin/python3 /fast/scratch/hyaku/chousa-r29/w2/OfflineConformance/tools/quote-reopen.py verify --items /fast/scratch/hyaku/chousa-r29/w2/OfflineConformance/extra-29_m1buw/items.tsv --registry /fast/scratch/hyaku/chousa-r29/w2/OfflineConformance/extra-29_m1buw/SOURCES.md
CANDIDATE_EXIT=1
QUOTE_REOPEN	file	UNREACHABLE	scheme not http or https
QUOTE_REOPEN	long	TOO_LONG	26 words, limit 25
QUOTE_REOPEN_SUMMARY verbatim=0 absent=0 too_long=1 no_source=0 unreachable=1
REQUEST_PATHS=['/file-redirect']
PASS file redirect refused after receiving 302
PASS TOO_LONG decided without fetching its URL
EXTRA_CONFORMANCE_PASS=2/2
```

The only GET recorded was `/file-redirect`; `/too-long` was not fetched. The redirect was received and rejected with `scheme not http or https`. Without the bypass (and after restoration), that redirect check is blocked before receiving a 302: `host resolves to a non-global address`, `REQUEST_PATHS=[]`.

## Exact mutation and detector expectation

Only scratch `tools/quote-reopen.py` line 204 changed; DNS resolution, address parsing, URL-scheme checks, redirects, parsing and verdict logic were left intact:

```diff
--- tools/quote-reopen.py (pristine scratch)
+++ tools/quote-reopen.py (probe-only scratch)
@@ -204 +204 @@
-        if not addr.is_global:
+        if False and not addr.is_global:
```

Expected after this explicit test accommodation: the 65-check harness passes, while the supplemental file-scheme refusal and TOO_LONG-before-fetch checks pass. Observed: 65/65 and 2/2. This is not a production patch recommendation. Mutation verdict is **INCONCLUSIVE**, not killed/survived: its pristine behavioral baseline was already failing by design.

## Every failing pinned-baseline check and diagnosis

Every line below has the same diagnosis: the harness assumes fetchable loopback but T1 refuses loopback, producing UNREACHABLE before any HTTP request. There were no residual FAIL lines in either bypass detector. Restored bytes reproduce the same failures.

```text
FAIL verdict i01 (entity decoded text)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i02 (raw entity text is not page text)  -- expected ABSENT, got UNREACHABLE
FAIL verdict i03 (quote spans em and a)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i04 (quote inside inline markup)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i05 (newline inside paragraph)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i06 (script content not matchable)  -- expected ABSENT, got UNREACHABLE
FAIL verdict i07 (style content not matchable)  -- expected ABSENT, got UNREACHABLE
FAIL verdict i08 (head content not matchable)  -- expected ABSENT, got UNREACHABLE
FAIL verdict i09 (html comment not matchable)  -- expected ABSENT, got UNREACHABLE
FAIL verdict i10 (soft hyphen deleted)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i11 (zero width space deleted)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i12 (zero width deleted in the quote too)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i13 (curly apostrophe maps to straight)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i14 (curly quotes map to straight)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i15 (NFKC ligature fi)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i16 (boundary at start of page text)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i17 (boundary at end of page text)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i18 (start boundary violated)  -- expected ABSENT, got UNREACHABLE
FAIL verdict i19 (end boundary violated)  -- expected ABSENT, got UNREACHABLE
FAIL verdict i20 (match is case sensitive)  -- expected ABSENT, got UNREACHABLE
FAIL verdict i30 (first item on the shared url)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i31 (second item on the shared url)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i32 (first url in the cell wins)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i33 (trailing dot stripped from url)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i34 (text/plain is allowed)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i35 (plain absent case)  -- expected ABSENT, got UNREACHABLE
FAIL verdict i37 (fragment removed from url)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i38 (noscript content not matchable)  -- expected ABSENT, got UNREACHABLE
FAIL verdict i39 (template content not matchable)  -- expected ABSENT, got UNREACHABLE
FAIL verdict i40 (zero width non joiner deleted)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i41 (zero width joiner deleted)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i42 (byte order mark deleted)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i43 (every curly quote maps to straight)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i44 (curly quote in the quote maps to straight)  -- expected VERBATIM, got UNREACHABLE
FAIL verdict i45 (trailing paren stripped from url)  -- expected VERBATIM, got UNREACHABLE
FAIL summary line counts  -- got {'verbatim': '0', 'absent': '0', 'too_long': '2', 'no_source': '3', 'unreachable': '40'}, want {'verbatim': '24', 'absent': '11', 'too_long': '2', 'no_source': '3', 'unreachable': '5'}
FAIL each url fetched once per run (shared url, two items)  -- 0 hits on /shared
FAIL each url fetched once per run (entities url, three items)  -- 0 hits on /entities
FAIL each url fetched once per run (invisible url, six items)  -- 0 hits on /invisible
FAIL every request used GET  -- methods: []
FAIL user agent names chousa-quote-reopen  -- agents: []
FAIL exit code is 0 when every item is verbatim  -- rc=1 cmd=python3 /fast/scratch/hyaku/chousa-r29/w2/OfflineConformance/tools/quote-reopen.py verify --items /fast/scratch/hyaku/chousa-r29/w2/OfflineConformance/quote-reopen-offline-ir_cumu6/items2.tsv --registry /fast/scratch/hyaku/chousa-r29/w2/OfflineConformance/quote-reopen-offline-ir_cumu6/SOURCES.md
FAIL verdict on the all-verbatim run  -- got UNREACHABLE
FAIL verdicts with the default registry  -- 35 wrong, first: [('i01', 'VERBATIM', 'UNREACHABLE'), ('i02', 'ABSENT', 'UNREACHABLE'), ('i03', 'VERBATIM', 'UNREACHABLE')]
```

## Commands and receipts

Each command was wrapped in `timeout --signal=TERM --kill-after=3s 120s`, executed synchronously with a private process group, and followed by process-group cleanup. Each receipt records the exact absolute argv, cwd, exit code, full stdout/stderr, elapsed time and cleanup result. All process groups were absent when the bounded commands returned; there were no background jobs to leave running. The harness's own child timeouts are 300 s; the supplemental child timeout is 60 s; the outer 120 s bound applies to the entire detector invocation.

Initial requested landed-tool command:

```sh
timeout --signal=TERM --kill-after=3s 120s python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/build/ExecOfflineTest/quote-reopen-offline-test.py --lane-root /home/vgpnk/Projects/shokunin/chousa-shokunin --work-dir /fast/scratch/hyaku/chousa-r29/w2/OfflineConformance -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/quote-reopen.py verify
```

Pinned pristine command (same pinned detector and command shape for mutated/restored phases):

```sh
timeout --signal=TERM --kill-after=3s 120s python3 /fast/scratch/hyaku/chousa-r29/w2/OfflineConformance/quote-reopen-offline-test.py --lane-root /home/vgpnk/Projects/shokunin/chousa-shokunin --work-dir /fast/scratch/hyaku/chousa-r29/w2/OfflineConformance -- python3 /fast/scratch/hyaku/chousa-r29/w2/OfflineConformance/tools/quote-reopen.py verify
```

Supplemental command for the scratch phases:

```sh
timeout --signal=TERM --kill-after=3s 120s python3 /fast/scratch/hyaku/chousa-r29/w2/OfflineConformance/extra-conformance.py /fast/scratch/hyaku/chousa-r29/w2/OfflineConformance/tools/quote-reopen.py
```

Receipts are under `.ufo/waves/round-29/falsify/OfflineConformance/`:

- [`pristine-landed-offline.json`](OfflineConformance/pristine-landed-offline.json)
- [`pristine-landed-extra.json`](OfflineConformance/pristine-landed-extra.json)
- [`pristine-pinned-offline.json`](OfflineConformance/pristine-pinned-offline.json)
- [`pristine-pinned-extra.json`](OfflineConformance/pristine-pinned-extra.json)
- [`global-check-disabled-offline.json`](OfflineConformance/global-check-disabled-offline.json)
- [`global-check-disabled-extra.json`](OfflineConformance/global-check-disabled-extra.json)
- [`restored-pinned-offline.json`](OfflineConformance/restored-pinned-offline.json)
- [`restored-pinned-extra.json`](OfflineConformance/restored-pinned-extra.json)

## Hashes and restoration evidence

SHA-256:

| Bytes | Hash |
|---|---|
| Lane tool before and after; pristine and restored scratch tool, including after the restored detector | `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea` |
| Scratch tool while the one-line bypass was applied | `badac1ef16290ced21ce485ed83d54b9bd1b784874387db0e78314b15963b4ce` |
| Immutable 65-check harness, unchanged for all paired runs | `e09aebdb370d955a8cae81c7534e1cb7f8f136fd015debf95cabe2ff5dd989c6` |
| Supplemental detector, unchanged for all paired runs | `3b50ca2a990a047976b55f7987c77ada807bbc1969f252b6f2933ed634532733` |
| Lane harness at the initial 64-check direct invocation | `5f963489c55c916150d87ebc168ea3afe133c296f72ca1c1743a75d79d80795f` |

The scratch tool was restored before its final detector run. `restoration.json` records equal pristine/restored/lane hashes and unchanged paired detectors. `initial-hashes.json`, `pinned-hashes.json` and `mutant-hash.json` preserve the earlier states.

## Limits and isolation

This is synthetic loopback conformance evidence, not a re-measurement of `QUOTE_REOPEN_MATCH=130/130` and not a claim about every parser/network edge case or the public-address policy itself. A failing pristine baseline cannot be scored as a killed mutation. No live external network requests were made. No lane production file, Git index, jj state, sibling source or fleet file was edited. All experiment code lives in `/fast/scratch/hyaku/chousa-r29/w2/OfflineConformance/`; only this requested report and its owned evidence directory were written in the lane. No tools were installed or updated.
