# ScribeSrcInHead
- Verdict: The HTML 5.2 source supports C1 and tool contract v2 item 1; C2 is out of scope.
- Direct fetch: `timeout 30s curl --silent --show-error --max-redirs 0 --write-out '\nHTTP_STATUS=%{http_code} URL=%{url_effective}\n' --output /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-30/build/ScribeSrcInHead/html52-snapshot.html 'https://www.w3.org/TR/2017/REC-html52-20171214/syntax.html'`; output `HTTP_STATUS=200 URL=https://www.w3.org/TR/2017/REC-html52-20171214/syntax.html`; no redirects followed (exit status not displayed).
- Section 8.2.5.4.4, “The "in head" insertion mode,” accessed 2026-10-23. Quote (18 words): “Anything else Pop the current node (which will be the head element) off the stack of open elements.”
- The static reader followed the legacy W3C URL to WHATWG and returned only W3C API metadata for the dated URL; the direct no-follow curl fetch retrieved the named W3C snapshot.
- Draft row is `queued` / `—`: `corpus/knowledge/quote-reopen-r30.md` was absent when checked; `CORPUS.md` defines `mined` as cited by a `used-by` path. `corpus/SOURCES.md` was not changed.
- No tools installed; no tests run. Setup command: `timeout 10s mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-30/build/ScribeSrcInHead`; no output (exit status not displayed).
