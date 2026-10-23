#!/usr/bin/env python3
"""Offline conformance harness for the round-29 C1 quote-reopen tool contract.

The contract under test is the frozen "Tool contract (frozen)" section of
`corpus/evidence/round29/claims.md`.  The harness is loopback-only: it starts
a private HTTP server on 127.0.0.1 (random port), serves synthetic pages,
writes a temporary registry (`SOURCES.md`) whose rows name those loopback
URLs, writes an `items.tsv`, runs the candidate command and compares every
verdict with the expectation built into the case table below.

The harness never reads the frozen fixture and never runs the frozen counter:
every case is a synthetic page served by the harness's own server, and every
item file is written by the harness itself.

Usage:
    python3 quote-reopen-offline-test.py [--lane-root DIR] [--work-dir DIR]
                                         [--quiet] -- CMD...

`CMD` is the candidate command.  If its last word is not already the
subcommand `verify`, the harness appends `verify`; the harness then always
appends `--items <items.tsv> --registry <SOURCES.md>`.

Output:
    one line per check, then the summary line
        OFFLINE_TEST_PASS=<passed>/<total>
    Exit status is 0 iff every check passed.
"""
import argparse
import http.server
import os
import shutil
import subprocess
import sys
import tempfile
import threading

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# server
# --------------------------------------------------------------------------

PAGES = {}          # path -> spec dict
HITS = []           # recorded requests
LOCK = threading.Lock()


def _record(path, method, headers):
    with LOCK:
        HITS.append({"path": path, "method": method,
                     "ua": headers.get("User-Agent", "") or "",
                     "headers": {k.lower(): v for k, v in headers.items()}})


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        pass

    def _send(self, status, ctype, body, extra=None):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        try:
            for i in range(0, len(body), 65536):
                self.wfile.write(body[i:i + 65536])
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_GET(self):
        _record(self.path, "GET", self.headers)
        path = self.path.split("#")[0].split("?")[0]
        spec = PAGES.get(path)
        if spec is None:
            self._send(404, "text/html; charset=utf-8",
                       b"<html><body><p>no such loopback page</p></body></html>")
            return
        if "location" in spec:
            self._send(spec.get("status", 302), "text/html; charset=utf-8", b"", spec)
            return
        self._send(spec.get("status", 200), spec.get("ctype", "text/html; charset=utf-8"),
                   spec["body"])

    def do_HEAD(self):
        _record(self.path, "HEAD", self.headers)
        self._send(405, "text/plain; charset=utf-8", b"")

    def do_POST(self):
        _record(self.path, "POST", self.headers)
        self._send(405, "text/plain; charset=utf-8", b"")


class Server(http.server.ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


# --------------------------------------------------------------------------
# page fixtures
# --------------------------------------------------------------------------

# Exotic characters are built with chr() so that this source file stays plain
# ASCII and no invisible character can be lost in transit.
SHY = chr(0x00AD)        # soft hyphen
ZWSP = chr(0x200B)       # zero width space
ZWNJ = chr(0x200C)       # zero width non joiner
ZWJ = chr(0x200D)        # zero width joiner
BOM = chr(0xFEFF)        # byte order mark
FI_LIG = chr(0xFB01)     # fi ligature
LSQ, RSQ = chr(0x2018), chr(0x2019)
LSQ2, RSQ2 = chr(0x201A), chr(0x201B)
LDQ, RDQ = chr(0x201C), chr(0x201D)
LDQ2, RDQ2 = chr(0x201E), chr(0x201F)


def _page(body):
    return ("<html><head><title>loopback fixture</title></head><body>"
            + body + "</body></html>").encode("utf-8")


def build_pages():
    PAGES.clear()
    # entity decoded text: &amp; &#8217; &nbsp; plus a plain paragraph
    PAGES["/entities"] = {"body": _page(
        "<p>Tom &amp; Jerry &#8217;s cafe&nbsp;here now</p>")}
    # a quote that spans <em> and <a>
    PAGES["/markup"] = {"body": _page(
        '<p>she said <em>hello</em> and <a href="/other">linked words</a> here</p>')}
    # a newline inside the source paragraph
    PAGES["/newline"] = {"body": _page("<p>first line\nsecond line</p>")}
    # script, style, noscript, template and head content
    PAGES["/script"] = {"body": (
        "<html><head><title>HEADTOKEN</title></head><body>"
        "<style>STYLETOKEN</style><script>SCRIPTTOKEN</script>"
        "<noscript>NOSCRIPTTOKEN</noscript><template>TEMPLATETOKEN</template>"
        "<p>visible script page text</p></body></html>").encode("utf-8")}
    # an html comment
    PAGES["/comment"] = {"body": _page(
        "<p>visible comment page text</p><!-- COMMENTTOKEN -->")}
    # soft hyphen, zero width space, zero width non joiner, zero width joiner, BOM
    PAGES["/invisible"] = {"body": _page(
        "<p>soft" + SHY + "hyphen and zero" + ZWSP + "width and mid" + ZWNJ + "word and "
        "join" + ZWJ + "word and bom" + BOM + "word and more</p>")}
    # curly apostrophe and curly double quotes in the page
    PAGES["/curly"] = {"body": _page(
        "<p>don&rsquo;t say \"no\" today</p>"
        "<p>plain " + LSQ + "single" + RSQ + " and " + LDQ + "double" + RDQ + " text</p>")}
    # straight quotes in the page, for the reverse mapping
    PAGES["/straight"] = {"body": _page(
        "<p>left ' ' ' ' right \" \" \" \" end</p>")}
    # every curly quote character the contract names
    PAGES["/curlyall"] = {"body": _page(
        "<p>left " + LSQ + " " + RSQ + " " + LSQ2 + " " + RSQ2 + " right "
        + LDQ + " " + RDQ + " " + LDQ2 + " " + RDQ2 + " end</p>")}
    # an NFKC ligature
    PAGES["/ligature"] = {"body": _page("<p>the pro" + FI_LIG + "le page text</p>")}
    # boundary rule: alpha beta gamma
    PAGES["/boundary"] = {"body": _page("<p>alpha beta gamma</p>")}
    # case sensitivity
    PAGES["/case"] = {"body": _page("<p>Alpha Beta Gamma</p>")}
    PAGES["/notfound"] = {"status": 404, "body": _page("<p>gone</p>")}
    PAGES["/pdf"] = {"ctype": "application/pdf", "body": b"%PDF-1.4 fake pdf body"}
    # 9 MiB of html
    PAGES["/big"] = {"body": (b"<html><body><p>" + (b"filler " * 1400000)
                              + b"</p></body></html>")}
    PAGES["/shared"] = {"body": _page("<p>shared page text for both items</p>")}
    PAGES["/first"] = {"body": _page("<p>first page text only</p>")}
    PAGES["/second"] = {"body": _page("<p>second page text only</p>")}
    PAGES["/trailing"] = {"body": _page("<p>trailing dot page text</p>")}
    PAGES["/plain"] = {"ctype": "text/plain; charset=utf-8", "body": b"plain text content here"}
    PAGES["/frag"] = {"body": _page("<p>fragment page text</p>")}
    PAGES["/toolong"] = {"body": _page("<p>toolong page text</p>")}
    PAGES["/exit0"] = {"body": _page("<p>exit zero page text</p>")}
    # a redirect to a scheme that is not http or https
    PAGES["/redirect"] = {"status": 302, "location": "gopher://127.0.0.1:1/nowhere"}


# --------------------------------------------------------------------------
# registry and items
# --------------------------------------------------------------------------

REGISTRY_HEADER = (
    "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|\n"
)

REGISTRY_ROWS = [
    ("S901", "Loopback entity page — {b}/entities"),
    ("S902", "Loopback markup page — {b}/markup"),
    ("S903", "Loopback newline page — {b}/newline"),
    ("S904", "Loopback script page — {b}/script"),
    ("S905", "Loopback comment page — {b}/comment"),
    ("S906", "Loopback invisible page — {b}/invisible"),
    ("S907", "Loopback curly page — {b}/curly"),
    ("S908", "Loopback ligature page — {b}/ligature"),
    ("S909", "Loopback boundary page — {b}/boundary"),
    ("S910", "Loopback case page — {b}/case"),
    ("S911", "Loopback missing page — {b}/notfound"),
    ("S912", "Loopback pdf page — {b}/pdf"),
    ("S913", "Loopback redirect page — {b}/redirect"),
    ("S914", "Loopback big page — {b}/big"),
    ("S915", "Loopback shared page — {b}/shared"),
    ("S916", "chousa own work — tools/research-gate.sh (no url in this cell)"),
    ("S917", "Loopback first of two — {b}/first and also {b}/second"),
    ("S918", "Loopback refused host — http://127.0.0.1:1/never"),
    ("S919", "Loopback trailing dot — {b}/trailing."),
    ("S920", "Loopback plain text page — {b}/plain"),
    ("S921", "Loopback toolong page — {b}/toolong"),
    ("S922", "Loopback fragment page — {b}/frag#sec"),
    ("S923", "Loopback curly all page — {b}/curlyall"),
    ("S924", "Loopback straight page — {b}/straight"),
]


def registry_text(base):
    out = ["# SOURCES — loopback conformance registry", "",
           "## Registry", "", REGISTRY_HEADER.rstrip("\n")]
    for rid, source in REGISTRY_ROWS:
        cell = source.format(b=base)
        out.append("| {rid} | {cell} | docs | A | loopback conformance scope | page text | "
                   "the contract rule under test | mined | 2026-10-23 | on-release | — |".format(
                       rid=rid, cell=cell))
    out.append("")
    return "\n".join(out)


W26 = " ".join("word{}".format(i + 1) for i in range(26))
W25 = " ".join("word{}".format(i + 1) for i in range(25))
CURLY_ALL_QUOTE = ("left " + LSQ + " " + RSQ + " " + LSQ2 + " " + RSQ2 + " right "
                   + LDQ + " " + RDQ + " " + LDQ2 + " " + RDQ2 + " end")
CURLY_ALL_STRAIGHT = "left ' ' ' ' right \" \" \" \" end"


def items_rows():
    """(id, source_id, quote, expected verdict, note)"""
    return [
        ("i01", "S901", "Tom & Jerry 's cafe here", "VERBATIM", "entity decoded text"),
        ("i02", "S901", "Tom &amp; Jerry", "ABSENT", "raw entity text is not page text"),
        ("i03", "S902", "she said hello and linked words here", "VERBATIM", "quote spans em and a"),
        ("i04", "S902", "hello and", "VERBATIM", "quote inside inline markup"),
        ("i05", "S903", "first line second line", "VERBATIM", "newline inside paragraph"),
        ("i06", "S904", "SCRIPTTOKEN", "ABSENT", "script content not matchable"),
        ("i07", "S904", "STYLETOKEN", "ABSENT", "style content not matchable"),
        ("i08", "S904", "HEADTOKEN", "ABSENT", "head content not matchable"),
        ("i09", "S905", "COMMENTTOKEN", "ABSENT", "html comment not matchable"),
        ("i10", "S906", "softhyphen", "VERBATIM", "soft hyphen deleted"),
        ("i11", "S906", "zerowidth", "VERBATIM", "zero width space deleted"),
        ("i12", "S906", "zero" + ZWSP + "width", "VERBATIM", "zero width deleted in the quote too"),
        ("i13", "S907", "don't say \"no\"", "VERBATIM", "curly apostrophe maps to straight"),
        ("i14", "S907", "plain 'single' and \"double\" text", "VERBATIM", "curly quotes map to straight"),
        ("i15", "S908", "profile page", "VERBATIM", "NFKC ligature fi"),
        ("i16", "S909", "alpha", "VERBATIM", "boundary at start of page text"),
        ("i17", "S909", "gamma", "VERBATIM", "boundary at end of page text"),
        ("i18", "S909", "lpha", "ABSENT", "start boundary violated"),
        ("i19", "S909", "gamm", "ABSENT", "end boundary violated"),
        ("i20", "S910", "alpha beta", "ABSENT", "match is case sensitive"),
        ("i21", "S918", W26, "TOO_LONG", "26 words beats an unreachable url"),
        ("i22", "S918", W25, "UNREACHABLE", "25 words is not too long"),
        ("i23", "S999", "some unregistered quote", "NO_SOURCE", "id not a registry row"),
        ("i24", "S999", W26, "NO_SOURCE", "no source beats too long"),
        ("i25", "S916", "any quote at all", "NO_SOURCE", "row without a url"),
        ("i26", "S911", "any quote at all", "UNREACHABLE", "404 status"),
        ("i27", "S912", "any quote at all", "UNREACHABLE", "application/pdf content type"),
        ("i28", "S913", "any quote at all", "UNREACHABLE", "redirect to a non http scheme"),
        ("i29", "S914", "any quote at all", "UNREACHABLE", "body over 8 MiB"),
        ("i30", "S915", "shared page text", "VERBATIM", "first item on the shared url"),
        ("i31", "S915", "shared page text", "VERBATIM", "second item on the shared url"),
        ("i32", "S917", "first page text", "VERBATIM", "first url in the cell wins"),
        ("i33", "S919", "trailing dot page text", "VERBATIM", "trailing dot stripped from url"),
        ("i34", "S920", "plain text content", "VERBATIM", "text/plain is allowed"),
        ("i35", "S901", "no such phrase in entities page", "ABSENT", "plain absent case"),
        ("i36", "S921", W26, "TOO_LONG", "too long decided on a reachable url"),
        ("i37", "S922", "fragment page text", "VERBATIM", "fragment removed from url"),
        ("i38", "S904", "NOSCRIPTTOKEN", "ABSENT", "noscript content not matchable"),
        ("i39", "S904", "TEMPLATETOKEN", "ABSENT", "template content not matchable"),
        ("i40", "S906", "midword", "VERBATIM", "zero width non joiner deleted"),
        ("i41", "S906", "joinword", "VERBATIM", "zero width joiner deleted"),
        ("i42", "S906", "bomword", "VERBATIM", "byte order mark deleted"),
        ("i43", "S923", CURLY_ALL_STRAIGHT, "VERBATIM", "every curly quote maps to straight"),
        ("i44", "S924", CURLY_ALL_QUOTE, "VERBATIM", "curly quote in the quote maps to straight"),
    ]


def items_text(rows):
    out = ["id\tsource_id\tquote"]
    for rid, sid, quote, _exp, _note in rows:
        out.append("{}\t{}\t{}".format(rid, sid, quote))
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------
# running the candidate
# --------------------------------------------------------------------------

def run_candidate(cmd, items_path, registry_path, lane_root, timeout=300):
    argv = list(cmd)
    if not argv or argv[-1] != "verify":
        argv = argv + ["verify"]
    argv = argv + ["--items", items_path, "--registry", registry_path]
    return _spawn(argv, lane_root, timeout)


def _spawn(argv, cwd, timeout=300):
    env = {k: v for k, v in os.environ.items()
           if k.lower() not in ("http_proxy", "https_proxy", "all_proxy")}
    env["NO_PROXY"] = "127.0.0.1,localhost"
    env["no_proxy"] = "127.0.0.1,localhost"
    shown = " ".join(argv)
    try:
        p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True,
                           timeout=timeout, env=env)
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        err = e.stderr.decode("utf-8", "replace") if isinstance(e.stderr, bytes) else (e.stderr or "")
        return 124, out, err, shown
    except FileNotFoundError as e:
        return 127, "", str(e), shown
    return p.returncode, p.stdout, p.stderr, shown


def find_tool_script(cmd, lane_root):
    """The candidate script, if the command names one that exists on disk."""
    for a in cmd:
        if not a.endswith(".py"):
            continue
        for cand in (a, os.path.join(lane_root, a)):
            if os.path.isfile(cand):
                return os.path.abspath(cand)
    return None


def parse_out(stdout):
    verdicts = {}
    order = []
    summary = None
    detail_lines = 0
    for line in stdout.splitlines():
        if line.startswith("QUOTE_REOPEN_SUMMARY"):
            summary = line
            continue
        parts = line.split("\t")
        if parts and parts[0] == "QUOTE_REOPEN" and len(parts) >= 3:
            if len(parts) >= 4:
                detail_lines += 1
            if parts[1] not in verdicts:
                verdicts[parts[1]] = parts[2]
                order.append(parts[1])
    return verdicts, order, summary, detail_lines


def parse_summary(line):
    if not line:
        return {}
    out = {}
    for part in line.split()[1:]:
        if "=" in part:
            k, v = part.split("=", 1)
            out[k] = v
    return out


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def find_lane_root(explicit):
    if explicit:
        return os.path.abspath(explicit)
    cur = HERE
    for _ in range(8):
        if os.path.isfile(os.path.join(cur, "corpus", "SOURCES.md")):
            return cur
        cur = os.path.dirname(cur)
    return os.getcwd()


def main(argv):
    if "--" not in argv:
        print("usage: quote-reopen-offline-test.py [--lane-root DIR] [--work-dir DIR] "
              "[--quiet] -- CMD...", file=sys.stderr)
        return 2
    k = argv.index("--")
    pre, cmd = argv[:k], argv[k + 1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane-root", default=None)
    ap.add_argument("--work-dir", default=None)
    ap.add_argument("--quiet", action="store_true")
    opts = ap.parse_args(pre)
    if not cmd:
        print("usage: empty CMD", file=sys.stderr)
        return 2

    lane_root = find_lane_root(opts.lane_root)
    if not os.path.isdir(lane_root):
        print("lane root not found: {}".format(lane_root), file=sys.stderr)
        return 2

    build_pages()
    srv = Server(("127.0.0.1", 0), Handler)
    port = srv.server_address[1]
    base = "http://127.0.0.1:{}".format(port)
    t = threading.Thread(target=srv.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
    t.start()

    # The scratch workspace lives inside the lane (so a tool that requires the
    # registry to sit under the lane root still works) but outside every
    # production path, and it is removed again before the harness returns.
    work_parent = opts.work_dir or HERE
    if not os.path.isdir(work_parent):
        work_parent = None
    work = tempfile.mkdtemp(prefix="quote-reopen-offline-", dir=work_parent)
    checks = []

    def check(name, ok, detail=""):
        checks.append((name, bool(ok), detail))
        if not opts.quiet:
            print("{} {}{}".format("PASS" if ok else "FAIL", name,
                                   ("  -- " + detail) if detail else ""))

    try:
        reg_path = os.path.join(work, "SOURCES.md")
        with open(reg_path, "w", encoding="utf-8") as f:
            f.write(registry_text(base))
        rows = items_rows()
        items_path = os.path.join(work, "items.tsv")
        with open(items_path, "w", encoding="utf-8") as f:
            f.write(items_text(rows))

        rc, out, err, shown = run_candidate(cmd, items_path, reg_path, lane_root)
        verdicts, order, summary, detail_lines = parse_out(out)

        check("exit code is 1 for a mixed verdict run", rc == 1,
              "rc={} cmd={}".format(rc, shown))

        expected_ids = [r[0] for r in rows]
        check("one verdict line per item, in input order", order == expected_ids,
              "got {} lines, expected {}".format(len(order), len(expected_ids)))
        check("every verdict line carries a detail field", detail_lines == len(rows),
              "{} of {} lines have a detail field".format(detail_lines, len(rows)))

        for rid, sid, quote, exp, note in rows:
            got = verdicts.get(rid)
            check("verdict {} ({})".format(rid, note), got == exp,
                  "expected {}, got {}".format(exp, got))

        counts = {"VERBATIM": 0, "ABSENT": 0, "TOO_LONG": 0, "NO_SOURCE": 0, "UNREACHABLE": 0}
        for _r, _s, _q, exp, _n in rows:
            counts[exp] += 1
        want = {"verbatim": str(counts["VERBATIM"]), "absent": str(counts["ABSENT"]),
                "too_long": str(counts["TOO_LONG"]), "no_source": str(counts["NO_SOURCE"]),
                "unreachable": str(counts["UNREACHABLE"])}
        got_sum = parse_summary(summary)
        check("summary line counts", got_sum == want,
              "got {}, want {}".format(got_sum, want))
        want_keys = ["verbatim", "absent", "too_long", "no_source", "unreachable"]
        got_keys = [p.split("=")[0] for p in (summary or "").split()[1:]]
        check("summary line key order", got_keys == want_keys,
              "got {}, want {}".format(got_keys, want_keys))

        with LOCK:
            hits1 = list(HITS)
        paths = [h["path"] for h in hits1]
        shared = [p for p in paths if p == "/shared"]
        entities = [p for p in paths if p == "/entities"]
        invisible = [p for p in paths if p == "/invisible"]
        check("each url fetched once per run (shared url, two items)", len(shared) == 1,
              "{} hits on /shared".format(len(shared)))
        check("each url fetched once per run (entities url, three items)", len(entities) == 1,
              "{} hits on /entities".format(len(entities)))
        check("each url fetched once per run (invisible url, six items)", len(invisible) == 1,
              "{} hits on /invisible".format(len(invisible)))
        check("every request used GET",
              bool(hits1) and all(h["method"] == "GET" for h in hits1),
              "methods: {}".format(sorted({h["method"] for h in hits1})))
        check("user agent names chousa-quote-reopen",
              bool(hits1) and all("chousa-quote-reopen" in h["ua"] for h in hits1),
              "agents: {}".format(sorted({h["ua"] for h in hits1})[:3]))
        cred = [h["path"] for h in hits1
                if "authorization" in h["headers"] or "cookie" in h["headers"]]
        check("no cookies or credentials sent", not cred, "paths: {}".format(cred[:3]))
        check("fragment removed from the request target",
              all("#" not in h["path"] for h in hits1),
              "paths with fragment: {}".format([p for p in paths if "#" in p][:3]))
        allowed = {"/entities", "/markup", "/newline", "/script", "/comment", "/invisible",
                   "/curly", "/straight", "/curlyall", "/ligature", "/boundary", "/case",
                   "/notfound", "/pdf", "/redirect", "/big", "/shared", "/first", "/second",
                   "/trailing", "/plain", "/frag", "/toolong", "/exit0"}
        outside = sorted({p for p in paths if p.split("#")[0].split("?")[0] not in allowed})
        check("no request outside the registry urls", not outside, "paths: {}".format(outside[:5]))

        rows2 = [("j01", "S920", "plain text content", "VERBATIM", "all verbatim run")]
        items2 = os.path.join(work, "items2.tsv")
        with open(items2, "w", encoding="utf-8") as f:
            f.write(items_text(rows2))
        rc2, out2, err2, shown2 = run_candidate(cmd, items2, reg_path, lane_root)
        v2, _o2, _s2, _d2 = parse_out(out2)
        check("exit code is 0 when every item is verbatim", rc2 == 0,
              "rc={} cmd={}".format(rc2, shown2))
        check("verdict on the all-verbatim run", v2.get("j01") == "VERBATIM",
              "got {}".format(v2.get("j01")))

        # The frozen counter passes only --items, so the tool must find the
        # default registry (corpus/SOURCES.md under the tool's lane root, the
        # parent of tools/) by itself.  This phase builds a fake lane with the
        # candidate script under tools/ and the loopback registry under
        # corpus/, then runs the tool with no --registry flag.
        tool_script = find_tool_script(cmd, lane_root)
        if tool_script:
            fake = os.path.join(work, "fakelane")
            os.makedirs(os.path.join(fake, "tools"), exist_ok=True)
            os.makedirs(os.path.join(fake, "corpus"), exist_ok=True)
            shutil.copy2(tool_script, os.path.join(fake, "tools", "quote-reopen.py"))
            with open(os.path.join(fake, "corpus", "SOURCES.md"), "w", encoding="utf-8") as f:
                f.write(registry_text(base))
            argv3 = [sys.executable, os.path.join(fake, "tools", "quote-reopen.py"), "verify",
                     "--items", items_path]
            rc3, out3, err3, shown3 = _spawn(argv3, fake)
            v3, order3, _sum3, _d3 = parse_out(out3)
            check("default registry resolves without --registry", len(order3) == len(rows),
                  "got {} verdict lines, expected {} (stderr: {})".format(
                      len(order3), len(rows), err3.strip()[:200]))
            wrong3 = [(rid, exp, v3.get(rid)) for rid, _s, _q, exp, _n in rows
                      if v3.get(rid) != exp]
            check("verdicts with the default registry", not wrong3,
                  "{} wrong, first: {}".format(len(wrong3), wrong3[:3]))
        else:
            print("SKIP default registry phase -- the command names no readable script")

        if err.strip() and not opts.quiet:
            print("--- candidate stderr (first 800 chars) ---")
            print(err[:800])
            print("--- end candidate stderr ---")
    finally:
        shutil.rmtree(work, ignore_errors=True)
        srv.shutdown()
        srv.server_close()

    passed = sum(1 for _n, ok, _d in checks if ok)
    total = len(checks)
    print("OFFLINE_TEST_PASS={}/{}".format(passed, total))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
