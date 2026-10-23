#!/usr/bin/env python3
"""Round-30 C1 surface recon: GET each registered SOURCES.md URL once.

Records status, content type, <head> start/end tag presence, <body> start
tag presence, and (when </head> is missing) the first start tag after the
last head-content element. No page bodies are saved. One GET per unique
fragment-stripped URL; urllib follows redirects inside that single GET and
the final URL is noted.
"""
import concurrent.futures
import re
import socket
import sys
import urllib.request
import urllib.error
from html.parser import HTMLParser
from urllib.parse import urldefrag

SOURCES = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md"
OUT_TSV = sys.argv[1] if len(sys.argv) > 1 else \
    "/fast/scratch/hyaku/chousa-r30/w1/ScoutRegistryHeadless/pages.tsv"
UA = "chousa-shokunin-round30-registry-survey/1.0 (chousa lane; quote-reopen C1 recon)"
TIMEOUT = 30
MAX_BODY = 8 * 1024 * 1024  # read cap; larger bodies truncated for tag scan

# Head-content elements per tool contract v2 item 1 (claims.md)
HEAD_CONTENT = {"base", "basefont", "bgsound", "link", "meta", "noframes",
                "noscript", "script", "style", "template", "title"}
# Raw-text elements: inner markup is text, not tags (title is RCDATA)
RAWTEXT = {"script", "style", "title"}
# Head-content elements whose subtree stays inside head even when it holds
# non-head-content markup (template contents are a separate fragment)
HEAD_SUBTREE = {"template", "noscript", "noframes"}


def registry_urls(path):
    """Yield (row_id, url) for each http(s) URL in the registry source column."""
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line.startswith("| S"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2:
                continue
            row_id, source = cells[0], cells[1]
            m = re.search(r"https?://\S+", source)
            if m:
                rows.append((row_id, m.group(0).rstrip(".,;)")))
    return rows


class HeadProbe(HTMLParser):
    """Detect head/body tags and the head boundary when </head> is absent."""

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.head_start = False
        self.head_end = False
        self.body_start = False
        self.after_head = None  # first non-head-content start tag after <head>
        self._in_head = False
        self._raw = None        # raw-text element we are inside
        self._subtree = 0       # depth inside template/noscript/noframes

    def handle_starttag(self, tag, attrs):
        t = tag.lower()
        if self._raw:
            return  # inside raw-text element; inner markup is text
        if self._subtree:
            if t in HEAD_SUBTREE:
                self._subtree += 1
            return  # inside template/noscript/noframes fragment
        if t == "head" and not self.head_start:
            self.head_start = True
            self._in_head = True
        elif t == "body":
            self.body_start = True
        if self._in_head and not self.head_end and self.after_head is None:
            if t in HEAD_CONTENT:
                if t in RAWTEXT:
                    self._raw = t
                elif t in HEAD_SUBTREE:
                    self._subtree = 1
            elif t != "head":
                self.after_head = t
                self._in_head = False

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        t = tag.lower()
        if self._raw:
            if t == self._raw:
                self._raw = None
            return
        if self._subtree:
            if t in HEAD_SUBTREE:
                self._subtree -= 1
            return
        if t == "head":
            self.head_end = True
            self._in_head = False

    def handle_data(self, data):
        # non-whitespace character data outside head-content elements ends
        # the head (contract v2 item 1); record the boundary as "#text"
        if self._raw or self._subtree:
            return
        if self._in_head and not self.head_end and self.after_head is None:
            if data.strip():
                self.after_head = "#text"
                self._in_head = False


def probe(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    note = ""
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            status = str(resp.status)
            ctype = resp.headers.get("content-type", "") or ""
            final_url = resp.geturl()
            body = resp.read(MAX_BODY + 1)
    except urllib.error.HTTPError as e:
        status = str(e.code)
        ctype = e.headers.get("content-type", "") if e.headers else ""
        final_url = url
        try:
            body = e.read(MAX_BODY + 1)
        except Exception:
            body = b""
        note = "http-error"
    except Exception as e:
        return dict(status="ERR", ctype="", head_start="", head_end="",
                    body_start="", boundary="",
                    note=f"{type(e).__name__}: {e}")
    if final_url != url:
        note = (note + ";" if note else "") + f"redirected->{final_url}"
    if len(body) > MAX_BODY:
        body = body[:MAX_BODY]
        note = (note + ";" if note else "") + "body-truncated-at-8MiB"
    head_start = head_end = body_start = boundary = ""
    if "html" in ctype.lower():
        m = re.search(r"charset=([\w.-]+)", ctype, re.I)
        enc = m.group(1) if m else "utf-8"
        try:
            text = body.decode(enc, errors="replace")
        except LookupError:
            text = body.decode("utf-8", errors="replace")
        p = HeadProbe()
        try:
            p.feed(text)
            p.close()
        except Exception:
            pass
        head_start = "yes" if p.head_start else "no"
        head_end = "yes" if p.head_end else "no"
        body_start = "yes" if p.body_start else "no"
        if p.head_start and not p.head_end:
            boundary = p.after_head if p.after_head is not None else "EOF"
    return dict(status=status, ctype=ctype.split(";")[0].strip(),
                head_start=head_start, head_end=head_end,
                body_start=body_start, boundary=boundary, note=note)


def main():
    rows = registry_urls(SOURCES)
    seen = {}  # dedup on fragment-stripped URL, first-seen order
    for rid, url in rows:
        u = urldefrag(url)[0]
        seen.setdefault(u, []).append(rid)
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(probe, url): url for url in seen}
        for f in concurrent.futures.as_completed(futs):
            results[futs[f]] = f.result()
    out = ["ids\turl\tstatus\tcontent_type\thead_start\thead_end\tbody_start\t"
           "first_tag_after_last_head_content\tnote"]
    missing = []
    for url, ids in seen.items():
        r = results[url]
        out.append("\t".join([
            ",".join(ids), url, r["status"], r["ctype"],
            r["head_start"], r["head_end"], r["body_start"],
            r["boundary"], r["note"]]))
        if r["head_start"] == "yes" and r["head_end"] == "no":
            missing.extend(ids)
        print(f"{','.join(ids):12s} {r['status']:>4s} {r['ctype']:<28s} "
              f"head={r['head_start'] or '-'} /head={r['head_end'] or '-'} "
              f"body={r['body_start'] or '-'} bound={r['boundary'] or '-'} "
              f"{r['note']} {url}", flush=True)
    with open(OUT_TSV, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"\nunique-urls={len(seen)} rows={len(rows)} "
          f"html-missing-head-end={len(missing)} ids={','.join(missing)}")


if __name__ == "__main__":
    socket.setdefaulttimeout(TIMEOUT)
    main()
