VERDICT: defect — the counter numbers and the metadata header hold, but 4 sentences in `corpus/knowledge/quote-reopen-r30.md` do not match their cited source or receipt, and the landed tool's total DEADLINE does not hold when one validated address does not answer

Target: `corpus/knowledge/quote-reopen-r30.md` at lane tip `a9d3a05a8fd812a60323b08381019152069581fd`. Line numbers are from `nl -ba`. Artifacts are in `.ufo/waves/round-30/falsify/ReviewKnowledge30/`. Scratch work is in `/fast/scratch/hyaku/chousa-r30/w2/ReviewKnowledge30/`.

## Setup checks (all pass)

- SHA-256 at the tip: tool `47a657e7…1201`, `c1-count.py` `5b312d84…9d6e6`, `c2-count.py` `0a59e373…f88f`, `qr_harness.py` `e2be0dd1…50d4`. All 4 equal the frozen values. `git show 49b2aa3:tools/quote-reopen.py | sha256sum` gives `47a657e7…1201`.
- Sources: each of the 5 distinct page URLs was fetched 1 time with `curl --max-redirs 0`. All 5 answered HTTP 200 with curl exit 0, between 03:37:23 and 03:37:24 UTC on 2026-10-23. S050 and S051 share one page, and so do S052 and S053. Receipt: `fetch-receipts.tsv` (URL, code, bytes, SHA-256). The S050/S051 page SHA-256 is `1db65aef…e141`, which equals the Gate record. Page bodies stay in scratch.
- Quote check: I ran the landed tool's own `html_to_text` and `found` on the fetched bytes (`srccheck.py`), with no second fetch. Results: S050, S051, S053, S054, S055 and S056 are VERBATIM. S052 is ABSENT (see finding 3).

## Findings, by severity

### Medium

1. **Lines 35-38: "`DEADLINE` … bounds the whole fetch" and "arms a timer that shuts the socket down at the deadline" do not hold on the landed tool when a connect attempt waits.**
   - In `tools/quote-reopen.py`, lines 383-396 compute `remaining` before `_dial`. `_dial` then gives each validated address `min(remaining, 5.0)` to connect (lines 271-276) and never recomputes it. The watchdog `threading.Timer(remaining, …)` starts only after `_dial` returns.
   - Probe (`probe.py`, `probe-output.json`, exit 0): I replaced only `_check_address`, then served a header drip on 127.0.0.1. 127.0.0.2 was a real kernel black hole (a full accept queue; the control connect timed out at 1.0 s).
     - With 1 address: wall time was 3.001 s at `DEADLINE`=3 and 4.0 s at `DEADLINE`=4.
     - With the black hole first and the good address second: wall time was 6.003 s and 8.003 s, which is 2 × `DEADLINE`. The C2 bound is `DEADLINE` + 1.5 s.
   - [INFERENCE] With the default of 30 s, each address that does not answer adds up to 5 s before the 30 s timer starts.
   - The C2 harness refuses unrouted destinations at once (`ReviewContractV2.md` finding 5), so neither counter can see this. Lines 64-76 list name-resolution time but not connect time or the address fallback.

2. **Lines 67-68: "the TLS path is checked only by a separate real-page run" has no citation.**
   - The only such run I found is `.ufo/waves/round-30/build/ExecC2Fetch.md:49-53`. It was 1 GET to `https://docs.python.org/3/`, on candidate `0150361a…`, which equals `git show 33dd643:tools/quote-reopen.py`. That is not the landed `47a657e7…`.
   - That run has no committed receipt file, and a status 200 alone cannot show that the certificate host check is on.
   - My offline probe on the landed tool does support line 47-48. With a throwaway CA passed through `SSL_CERT_FILE` and a certificate for `good.test` only:
     - `https://good.test` returned 200 and the page text.
     - `https://bad.test` returned `fetch failed: SSLCertVerificationError`.
     - The SNI values the server saw were `good.test`, `bad.test`, `bad.test`.
   - The sentence should cite a receipt on the landed revision.

3. **Line 4 says that "its located quote is in `corpus/lessons/round-30.md` `## Gate`", but the S052 quote there is not verbatim.**
   - `lessons/round-30.md:47` quotes: "…within the timeout specified for the socket."
   - The page reads: "…within the timeout specified for the socket (they raise a timeout exception) or if the system returns an error."
   - The landed tool's `found` gives ABSENT. The other 6 Gate quotes are VERBATIM.
   - QUALITY 25 requires that the ABSENT is recorded. This is a source-wording defect, not a tool limit.

### Low

4. **Line 74 cites the wrong finding number.** It says "`ReviewContractV2.md` finding 4 measured 10.01 s". In `ReviewContractV2.md`, the 10.01 s resolver measurement is finding 2 (lines 39-62). Finding 4 is "IPv6 is entirely outside the C2 harness".

5. **Line 58 says "5 kinds of head shape".** The `c1-count.py` docstring (lines 18-22) and `claims.md:117-118` list 4 document classes: `headless-body`, `headless-nobody`, `headless-text` and `closed-head`. The number 5 is the count of items per document.

6. **Line 17, "HTML lets a page omit the `head` end tag (S050)", goes beyond the row's scope and drops the condition.**
   - The S050 scope is "what the HTML 5.2 Recommendation text states…; not current HTML", so QUALITY 7 requires an inference label on a general "HTML" claim.
   - The source text is conditional: "may be omitted if the head element is not immediately followed by a space character or a comment."

7. **Lines 32-33, "not a whole transfer (S052, S054)", is an unlabelled inference (QUALITY 3).** Both sources say only that blocking operations time out. S052's "Notes on socket timeouts" and the S054 constructor text do not mention a transfer.

8. **Lines 18-26: the paraphrase of S051 is accurate, but contract v2 differs from S051 on 2 tokens.**
   - S051 sends an `html` start tag inside head to the "in body" rules without popping head. Contract v2 and the tool (lines 113-119) end the head on it.
   - S051 sends the `</body>`, `</html>` and `</br>` end tags to "Anything else", which pops head. The tool ignores them while in head.
   - [INFERENCE] Neither difference changes the extracted text on the counter's shapes; `ReviewContractV2.md` finding 9 compared 200 documents.

## Holds (observed)

- **Lines 58-62.**
  - The before receipts `controls/before-c1-v4-run{1,2}.json` give 78/106 twice, and `before-c2-v4-run{1,2}.json` give 12/27 twice. Their tool hash is `72a3ad47…`, which equals the base `a3a3710` tool.
  - The after receipts `measure/after-c{1,2}-run{1,2}.json` give 106/106 twice and 27/27 twice, with `predicate_holds` true and tool `47a657e7…`. In both C2 runs, all 27 items have `bound_ok` and `validated_only` true.
- **Fresh runs in a clone outside the fleet layout.** I cloned the lane to `/fast/scratch/…/clone` and ran the counters there:
  - `timeout 300 python3 corpus/evidence/round30/c1-count.py --receipt …` printed `QUOTE_REOPEN_HEADLESS_MATCH=106/106`, exit 0, seed 17441236271123951616.
  - `c2-count.py`, run 2 times, printed `QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27`, exit 0, with seeds 5422052045005059440 and 15996333217420838697.
  - Receipts: `rerun-c1-clone.json`, `rerun-c2-clone.json`, `rerun-c2-clone-2.json`.
- **Metadata header, QUALITY 6.** All 7 rows (S050-S056) are tier A with status `mined`, `used-by` names this entry, and each carries a URL and an anchor. `verified-at:` gives an ISO date and what was checked. `recheck:` gives the cadence `180d` and a command.
- **Metadata header, QUALITY 13.** The command states its working directory ("from the lane root") and takes no `--root` argument. It ran in the clone outside the fleet layout (above). The `180d` cadence differs from the rows' `365d` and `on-release`, which is allowed.
- **Lines 42-48.** The sentences on S053 (create_connection resolves the name and tries each address), S055 (server_hostname, SNI, hostname match) and S056 (is_global follows the IANA registries) match the fetched pages. Lines 52-54 match `qr_harness.py:7-12`. Lines 75-76 match `quote-reopen-r29.md:93-94`.
- **Prose and placeholder checks.**
  - `python3 corpus/evidence/round29/prose-check.py <entry>` exits 0 with 0 hits.
  - `grep -nwi live <entry>` exits 1, so there are no hits.
  - The QUALITY 10 placeholder grep exits 1, so there are no hits.

## Residual risk and verification gaps

- My first counter runs were under `ulimit -u 2000`. Both failed with `RuntimeError: can't start new thread` in `qr_harness.Server()` and exited 1, not the documented exit 2 for a harness failure (`c1-count.py:8`). A harness crash can therefore look like a miss. Those runs are not scored.
- In finding 1 the black hole was a full loopback accept queue. A real network path was not tested.
- I did not open the undated `/TR/html52/` redirect (line 4), because it is not a registered URL.
- No tool was installed or updated.
