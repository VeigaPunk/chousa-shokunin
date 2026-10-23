#!/usr/bin/env python3
"""Round-29 wave-1 freshness reconnaissance for corpus/SOURCES.md registry rows.

One bounded GET per unique URL (30 s timeout, redirects followed, UA contains
chousa-quote-reopen, Accept-Encoding gzip to mirror c1-count.py fetch_text).
Records, per registry row: id, url, final status, final url, final host, content
type, body bytes read, and whether the frozen contract's content-type/status/
size gate would call the row reachable.
Read-only: opens no lane file for writing except the TSV given as argv[1].
"""
import gzip
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
import zlib
from html.parser import HTMLParser

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
REGISTRY = os.path.join(LANE, "corpus", "SOURCES.md")
UA = "chousa-quote-reopen-registry-fetch/r29 (scout; one GET per URL)"
MAXB = 8 * 1024 * 1024
SUPPORTED = {"text/html", "application/xhtml+xml", "text/plain"}
SKIP = {"script", "style", "noscript", "template", "head"}
BLOCK = {"p", "div", "li", "ul", "ol", "table", "tr", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6",
         "br", "section", "article", "header", "footer", "nav", "pre", "blockquote", "dt", "dd", "dl",
         "figure", "figcaption", "hr", "main", "aside"}
QMAP = str.maketrans({"\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'", "\u201c": '"', "\u201d": '"',
                      "\u201e": '"', "\u201f": '"', "\u00ad": None, "\u200b": None, "\u200c": None,
                      "\u200d": None, "\ufeff": None})


class _Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        elif tag in BLOCK:
            self.out.append(" ")

    def handle_startendtag(self, tag, attrs):
        if tag in BLOCK:
            self.out.append(" ")

    def handle_endtag(self, tag):
        if tag in SKIP:
            self.skip = max(0, self.skip - 1)
        elif tag in BLOCK:
            self.out.append(" ")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def norm(s):
    return " ".join(unicodedata.normalize("NFKC", s).translate(QMAP).split())


def rows():
    out = []
    with open(REGISTRY, encoding="utf-8") as f:
        for ln in f:
            if not ln.startswith("| S"):
                continue
            cells = ln.split("|")
            if len(cells) < 4:
                continue
            sid = cells[1].strip()
            m = re.search(r"https?://\S+", cells[2])
            out.append((sid, m.group(0).rstrip(".,;)") if m else ""))
    return out


def one(url):
    """One GET. Returns a dict of observed facts; never raises."""
    rec = {"status": "", "final_url": "", "ctype": "", "enc": "", "charset": "",
           "bytes": "", "inflated": "", "chars": "", "words": "", "note": ""}
    req = urllib.request.Request(url.split("#")[0],
                                headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    try:
        r = urllib.request.urlopen(req, timeout=30)
    except urllib.error.HTTPError as e:
        rec["status"] = str(e.code)
        rec["final_url"] = e.url or url
        rec["ctype"] = (e.headers.get_content_type() if e.headers else "") or ""
        rec["note"] = "HTTPError"
        try:
            body = e.read(MAXB + 1)
            rec["bytes"] = str(len(body))
        except Exception as e2:  # noqa: BLE001
            rec["note"] += f";body-read-failed:{type(e2).__name__}"
        return rec
    except Exception as e:  # noqa: BLE001  (URLError, timeout, ssl, http.client)
        rec["status"] = "ERR"
        rec["final_url"] = url
        rec["note"] = f"{type(e).__name__}:{str(e)[:120]}"
        return rec
    with r:
        rec["status"] = str(r.status)
        rec["final_url"] = r.geturl()
        rec["ctype"] = r.headers.get_content_type() or ""
        rec["enc"] = (r.headers.get("Content-Encoding") or "").lower()
        rec["charset"] = r.headers.get_content_charset() or ""
        body = r.read(MAXB + 1)
        rec["bytes"] = str(len(body))
        doc = None
        if rec["enc"] == "gzip":
            try:
                doc = gzip.decompress(body)
            except Exception as e:  # noqa: BLE001
                rec["note"] = f"gzip-decompress-failed:{type(e).__name__}"
        elif rec["enc"] == "deflate":
            try:
                doc = zlib.decompress(body)
            except Exception as e:  # noqa: BLE001
                rec["note"] = f"deflate-decompress-failed:{type(e).__name__}"
        else:
            doc = body
    if doc is None:
        return rec
    rec["inflated"] = str(len(doc))
    text = doc.decode(rec["charset"] or "utf-8", "replace")
    rec["chars"] = str(len(text))
    try:
        if rec["ctype"] == "text/plain":
            n = norm(text)
        else:
            p = _Text()
            p.feed(text)
            p.close()
            n = norm("".join(p.out))
        rec["words"] = str(len(n.split(" ")))
    except Exception as e:  # noqa: BLE001
        rec["note"] += f"text-extract-failed:{type(e).__name__}"
    return rec


def main():
    tsv = sys.argv[1]
    rws = rows()
    seen = {}
    order = []
    for sid, url in rws:
        if url and url not in seen:
            seen[url] = None
            order.append(url)
    with open(tsv, "w", encoding="utf-8") as out:
        out.write("id\turl\tfetch\tstatus\tfinal_url\tfinal_host\tcontent_type\tcontent_encoding\t"
                  "charset\tbytes_read\tinflated_bytes\thtml_chars\ttext_words\tcontract_supported\tnote\n")
        out.flush()
        for url in order:
            t0 = time.time()
            rec = one(url)
            dt = f"{time.time() - t0:.1f}s"
            seen[url] = rec
            ids = [sid for sid, u in rws if u == url]
            ok = ("yes" if (rec["status"].isdigit() and rec["status"].startswith("2")
                            and rec["ctype"] in SUPPORTED
                            and rec["bytes"].isdigit() and int(rec["bytes"]) <= MAXB)
                  else "no")
            host = ""
            if rec["final_url"]:
                host = rec["final_url"].split("//", 1)[-1].split("/", 1)[0]
            note = rec["note"] or f"elapsed={dt}"
            for i, sid in enumerate(ids):
                out.write("\t".join([sid, url, "yes" if i == 0 else f"dup-of-{ids[0]}",
                                     rec["status"], rec["final_url"], host, rec["ctype"], rec["enc"],
                                     rec["charset"], rec["bytes"], rec["inflated"], rec["chars"],
                                     rec["words"], ok, note if i == 0 else note]) + "\n")
            out.flush()
            print(f"{ids[0]:5s} {rec['status']:4s} {rec['ctype']:24s} {rec['bytes']:>9s}B "
                  f"words={rec['words']:>7s} {ok:3s} {dt} {url}", flush=True)
    print(f"rows={len(rws)} unique_urls={len(order)}", flush=True)


if __name__ == "__main__":
    main()
