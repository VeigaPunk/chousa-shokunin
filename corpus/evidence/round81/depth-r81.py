#!/usr/bin/env python3
"""depth-r81 — round-81 C1 (depth) counter, frozen before any entry is drafted.

Usage:
    python3 -B corpus/evidence/round81/depth-r81.py --root DIR [--date YYYY-MM-DD]

DIR is a lane tree (the working tree, or `git archive <rev>` extracted into a
scratch dir). Read-only; writes nothing.

An entry is a file `DIR/corpus/knowledge/*-r81.md`. It COUNTS iff all hold:

  P1 header  — one of its first 15 lines starts with `source:`; the S-ids on
               that line include >= 2 FRESH rows. A FRESH row is a
               `corpus/SOURCES.md` Registry row whose status cell is `mined`,
               whose opened cell equals --date (default 2026-11-06) and whose
               used-by cell names `corpus/knowledge/<entry file name>`.
  P2 quotes  — every line of the form  > "<quote>" — S###  is a quote line.
               The entry has >= 3 quote lines, every one of them LOCATED, and
               the located quotes cite >= 2 distinct FRESH rows. A quote line is
               LOCATED iff its S-id is a FRESH row of P1's line, the quote has
               1..25 words, and the quote, whitespace-collapsed, occurs in the
               whitespace-collapsed text of `corpus/captures/<key>.txt`, where
               key = sha256(first http(s) URL in the row's source cell)[:24],
               AND `corpus/evidence/round57/refetch.tsv` holds a row with that
               id, that URL, that key, curl_rc 0, http 2xx, fetched_utc on
               --date, and txt_sha256 equal to the sha256 of that .txt file.
               One unlocated quote line disqualifies the entry.
  P3 table   — the entry holds a Markdown table: a header row, a separator
               row and >= 3 body rows.
  P4 disjoint — a counted entry shares no located quote string with an
               earlier counted entry (sorted by file name), and no two counted
               entries are byte-identical.

Output: one `ENTRY <name> counted=yes|no reason=<first failing check>` line
per entry, then
    DEPTH_R81 entries=<k> fresh_rows=<r> located_quotes=<q>
    DEPTH_R81=PASS|FAIL
Exit 0 iff k >= 2; 1 otherwise; 2 on usage error or a missing/unparseable
corpus/SOURCES.md.

Limit (stated before data): bytes of a capture and its refetch row are
trusted as committed; whether they are what the URL served is checked by
re-fetching (tools/quote-reopen.py, tools/capture-fetch.py), not here.
"""
import argparse
import glob
import hashlib
import os
import re
import sys

QUOTE_RE = re.compile(r'^>\s*"(?P<q>[^"]+)"\s+—\s+(?P<sid>S\d{3,})\s*$')
SID_RE = re.compile(r"S\d{3,}")
URL_RE = re.compile(r"https?://[^\s|)>\]]+")


def collapse(s):
    return " ".join(s.split())


def parse_registry(path):
    rows = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not re.match(r"^ {0,3}\|\s*S\d{3,}\s*\|", line):
                continue
            cells = [c.strip() for c in line.rstrip("\n").strip().strip("|").split("|")]
            if len(cells) != 11:
                continue
            rows[cells[0]] = {
                "source": cells[1], "status": cells[7], "opened": cells[8], "used_by": cells[10],
            }
    return rows


def parse_refetch(path):
    out = []
    if not os.path.isfile(path):
        return out
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            f = line.rstrip("\n").split("\t")
            if len(f) == 9:
                out.append(f)
    return out


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--root", required=True)
    ap.add_argument("--date", default="2026-11-06")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    reg_path = os.path.join(root, "corpus", "SOURCES.md")
    if not os.path.isfile(reg_path):
        print("DEPTH_R81 error: no corpus/SOURCES.md under --root", file=sys.stderr)
        return 2
    reg = parse_registry(reg_path)
    if not reg:
        print("DEPTH_R81 error: registry has no parseable row", file=sys.stderr)
        return 2
    refetch = parse_refetch(os.path.join(root, "corpus", "evidence", "round57", "refetch.tsv"))

    def fresh(sid, entry_rel):
        r = reg.get(sid)
        return bool(r) and r["status"] == "mined" and r["opened"] == a.date and entry_rel in r["used_by"]

    def located(sid, quote):
        r = reg[sid]
        m = URL_RE.search(r["source"])
        if not m:
            return False, "row-has-no-url"
        url = m.group(0)
        key = hashlib.sha256(url.encode("utf-8")).hexdigest()[:24]
        txt = os.path.join(root, "corpus", "captures", key + ".txt")
        if not os.path.isfile(txt):
            return False, "no-capture"
        tsha = sha256_file(txt)
        ok = any(f[0] == sid and f[1] == url and f[2] == key and f[5] == "0"
                 and f[6][:1] == "2" and f[4].startswith(a.date) and f[8] == tsha
                 for f in refetch)
        if not ok:
            return False, "no-fetch-record"
        with open(txt, encoding="utf-8", errors="replace") as fh:
            body = collapse(fh.read())
        if collapse(quote) not in body:
            return False, "absent"
        return True, "located"

    counted = []
    seen_quotes = set()
    seen_bytes = set()
    fresh_rows = set()
    nq = 0
    for path in sorted(glob.glob(os.path.join(root, "corpus", "knowledge", "*-r81.md"))):
        name = os.path.basename(path)
        rel = "corpus/knowledge/" + name
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        lines = text.split("\n")
        reason = None
        src = [l for l in lines[:15] if l.startswith("source:")]
        ids = SID_RE.findall(src[0]) if src else []
        fids = [s for s in dict.fromkeys(ids) if fresh(s, rel)]
        if len(fids) < 2:
            reason = "P1-fresh-rows=%d" % len(fids)
        quotes = []
        if reason is None:
            for l in lines:
                m = QUOTE_RE.match(l)
                if m:
                    quotes.append((m.group("q"), m.group("sid")))
            if len(quotes) < 3:
                reason = "P2-quote-lines=%d" % len(quotes)
        if reason is None:
            for q, sid in quotes:
                if sid not in fids:
                    reason = "P2-quote-cites-non-fresh-%s" % sid
                    break
                w = len(q.split())
                if w < 1 or w > 25:
                    reason = "P2-quote-words=%d" % w
                    break
                ok, why = located(sid, q)
                if not ok:
                    reason = "P2-%s-%s" % (why, sid)
                    break
        if reason is None and len({sid for _, sid in quotes}) < 2:
            reason = "P2-distinct-rows<2"
        if reason is None:
            tbl = False
            for i in range(len(lines) - 4):
                if (lines[i].lstrip().startswith("|") and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1])
                        and all(lines[i + k].lstrip().startswith("|") for k in (2, 3, 4))):
                    tbl = True
                    break
            if not tbl:
                reason = "P3-no-table"
        if reason is None:
            qs = {collapse(q) for q, _ in quotes}
            if text in seen_bytes:
                reason = "P4-duplicate-bytes"
            elif qs & seen_quotes:
                reason = "P4-shared-quote"
            else:
                seen_quotes |= qs
                seen_bytes.add(text)
                fresh_rows |= set(fids)
                nq += len(quotes)
                counted.append(name)
        print("ENTRY %s counted=%s reason=%s" % (name, "yes" if reason is None else "no", reason or "all-pass"))
    k = len(counted)
    print("DEPTH_R81 entries=%d fresh_rows=%d located_quotes=%d" % (k, len(fresh_rows), nq))
    print("DEPTH_R81=%s" % ("PASS" if k >= 2 else "FAIL"))
    return 0 if k >= 2 else 1


if __name__ == "__main__":
    sys.exit(main())
