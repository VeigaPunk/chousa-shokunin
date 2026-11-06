#!/usr/bin/env python3
"""depth-r82 — round-82 C2 (depth) counter, frozen before the candidate entry is drafted.

Successor to depth-r81.py (round-81 routed defect 1: two 10-line filler entries reached PASS).
Usage:  python3 -B corpus/evidence/round82/depth-r82.py --root DIR
DIR is a lane tree (`git archive <rev>` extracted). Read-only; writes nothing.

NEW entries are files in DIR/corpus/knowledge/*.md whose names are not in the frozen base list
corpus/evidence/round82/base-knowledge.txt (the knowledge set at 5d792e1e, the round-82 egress
commit). Each new entry is checked:

  E1 rows     — a `## Decision table` section holds a Markdown table with a `Warrant` column and
                >= 5 body rows.
  E2 warrant  — every body row's Warrant cell names >= 1 quote id (Q<n>) declared in the entry's
                `## Located quotes` table (columns qid | source | quote), and names the S-id of
                every quote id it names.
  E3 located  — every declared quote has 8..25 words and is LOCATED: its source row is FRESH and
                the quote, whitespace-collapsed (curly quotes/apostrophes folded to ASCII), occurs
                in the equally normalized text of corpus/captures/<key>.txt.
                FRESH: a Registry row of corpus/SOURCES.md, status `mined`, used-by naming
                `corpus/knowledge/<entry>`, whose first http(s) URL u gives key=sha256(u)[:24], and
                corpus/evidence/round57/refetch.tsv holds a row (id, u, key, curl_rc 0, http 2xx,
                fetched_utc >= ROUND_START) whose txt_sha256 equals sha256 of that .txt file.
                ROUND_START is the commit time of the egress table, 2026-11-06T19:41:56Z.
  E4 novel    — declared quotes are pairwise distinct, and no declared quote (normalized) occurs in
                the normalized text of any base-list entry.
  E5 content  — in every body row each non-Warrant cell has >= 3 words and is not a placeholder
                (empty, -, n/a, none, tbd, ...), and the non-Warrant cells of a row, joined, differ
                from every other row's.
  E6 coverage — every S-id on the entry's `source:` line is FRESH and named by >= 1 Warrant cell;
                every declared quote id is named by >= 1 Warrant cell; the `source:` line names
                >= 3 S-ids.
  E7 new ground — no S-id on the `source:` line is named on the `source:` line of any base-list
                entry, and its URL appears in no base-list entry.

Output: `ENTRY <name> ok=yes|no rows=<r> quotes=<q> fails=<E..>` per new entry, then
    DEPTH_R82 entries=<k> ok_entries=<j> rows=<r> located_quotes=<q> fresh_sources=<f>
    DEPTH_R82=PASS|FAIL
PASS iff k >= 1 and j == k (every new entry passes E1..E7). Exit 0 PASS, 1 FAIL, 2 usage error.

Limit (stated before data): the counter checks that every decision row is tied to a verbatim,
freshly located quote from a source no base entry used; it does NOT judge whether a row's Do/Never
follows from its quote. That is checked by a non-author reviewer under kill rule K3 of the
frozen claims file.
"""
import argparse
import hashlib
import os
import re
import sys

ROUND_START = "2026-11-06T19:41:56Z"
BASE_LIST = "corpus/evidence/round82/base-knowledge.txt"
SID_RE = re.compile(r"S\d{3,}")
QID_RE = re.compile(r"\bQ\d+\b")
URL_RE = re.compile(r"https?://[^\s|)>\]]+")
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
PLACEHOLDERS = {"", "-", "--", "—", "–", "n/a", "na", "none", "nil", "null", "tbd", "tba", "todo",
                "?", "...", "…", "x", "unknown", "not applicable", "same", "ditto", "see above"}


def norm(s):
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return " ".join(s.split())


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def section(text, name):
    out, on = [], False
    for ln in text.splitlines():
        if ln.startswith("## "):
            on = ln[3:].strip().lower() == name.lower()
            continue
        if on:
            out.append(ln)
    return out


def table(lines):
    rows = [ln for ln in lines if ln.strip().startswith("|")]
    if len(rows) < 2:
        return None, []
    hdr = [c.strip().lower() for c in rows[0].strip().strip("|").split("|")]
    if not re.match(r"^\s*\|?\s*:?-{3,}", rows[1]):
        return None, []
    body = []
    for r in rows[2:]:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        if len(cells) != len(hdr):
            return hdr, None
        body.append(dict(zip(hdr, cells)))
    return hdr, body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    root = os.path.abspath(ap.parse_args().root)
    kdir = os.path.join(root, "corpus/knowledge")
    for rel in (BASE_LIST, "corpus/SOURCES.md", "corpus/evidence/round57/refetch.tsv"):
        if not os.path.isfile(os.path.join(root, rel)):
            print(f"DEPTH_R82_ERROR missing {rel}")
            return 2
    base = [ln.strip() for ln in open(os.path.join(root, BASE_LIST)) if ln.strip()]
    base_text, base_sids = "", set()
    for b in base:
        p = os.path.join(kdir, b)
        if os.path.isfile(p):
            t = open(p, encoding="utf-8", errors="replace").read()
            base_text += "\n" + t
            for ln in t.splitlines()[:15]:
                if ln.startswith("source:"):
                    base_sids |= set(SID_RE.findall(ln))
    base_norm = norm(base_text)
    reg = {}
    for ln in open(os.path.join(root, "corpus/SOURCES.md"), encoding="utf-8"):
        m = ROW_RE.match(ln)
        if not m:
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) != 11:
            continue
        reg[cells[0]] = {"source": cells[1], "status": cells[7], "usedby": cells[10]}
    fetch = {}
    for ln in open(os.path.join(root, "corpus/evidence/round57/refetch.tsv"), encoding="utf-8"):
        f = ln.rstrip("\n").split("\t")
        if len(f) != 9 or f[5] != "0" or not f[6].startswith("2") or f[4] < ROUND_START:
            continue
        fetch.setdefault((f[0], f[1]), []).append(f)

    def fresh(sid, entry):
        r = reg.get(sid)
        if not r or r["status"] != "mined" or f"corpus/knowledge/{entry}" not in r["usedby"]:
            return None
        m = URL_RE.search(r["source"])
        if not m:
            return None
        url = m.group(0)
        key = hashlib.sha256(url.encode()).hexdigest()[:24]
        cap = os.path.join(root, "corpus/captures", key + ".txt")
        if not os.path.isfile(cap):
            return None
        rows = [f for f in fetch.get((sid, url), []) if f[2] == key]
        if not rows or rows[-1][8] != sha(cap):
            return None
        return url, norm(open(cap, encoding="utf-8", errors="replace").read())

    new = sorted(f for f in os.listdir(kdir) if f.endswith(".md") and f not in set(base))
    tot_rows = tot_q = ok_n = 0
    fresh_all = set()
    for e in new:
        text = open(os.path.join(kdir, e), encoding="utf-8", errors="replace").read()
        fails = []
        srcline = next((ln for ln in text.splitlines()[:15] if ln.startswith("source:")), "")
        sids = list(dict.fromkeys(SID_RE.findall(srcline)))
        _, qrows = table(section(text, "Located quotes"))
        quotes = {}
        for q in qrows or []:
            qid, src, qt = q.get("qid", ""), q.get("source", ""), q.get("quote", "").strip('"')
            if QID_RE.fullmatch(qid) and SID_RE.fullmatch(src):
                quotes[qid] = (src, qt)
        hdr, body = table(section(text, "Decision table"))
        if not hdr or body is None or len(body) < 5:
            fails.append("E1")
            body = body or []
        named_q, named_s = set(), set()
        for r in body:
            w = r.get("warrant", "")
            qs = QID_RE.findall(w)
            if not qs or any(q not in quotes or quotes[q][0] not in w for q in qs):
                fails.append("E2")
            named_q |= set(qs)
            named_s |= set(SID_RE.findall(w))
        located = 0
        fr = {}
        for s in sids:
            fr[s] = fresh(s, e)
        for qid, (src, qt) in quotes.items():
            n = len(qt.split())
            if src not in fr:
                fr[src] = fresh(src, e)
            if not (8 <= n <= 25) or fr[src] is None or norm(qt) not in fr[src][1]:
                fails.append("E3")
            else:
                located += 1
        qn = [norm(q[1]) for q in quotes.values()]
        if len(set(qn)) != len(qn) or any(q in base_norm for q in qn):
            fails.append("E4")
        seen = set()
        for r in body:
            other = [v for k, v in r.items() if k != "warrant"]
            joined = " | ".join(other)
            if any(len(v.split()) < 3 or norm(v).lower().strip("`.") in PLACEHOLDERS for v in other) or joined in seen:
                fails.append("E5")
            seen.add(joined)
        if len(sids) < 3 or any(fr.get(s) is None or s not in named_s for s in sids) or set(quotes) - named_q:
            fails.append("E6")
        for s in sids:
            if s in base_sids or (fr.get(s) and fr[s][0] in base_text):
                fails.append("E7")
        fails = sorted(set(fails))
        ok = not fails and bool(quotes)
        ok_n += ok
        tot_rows += len(body)
        tot_q += located
        fresh_all |= {s for s in sids if fr.get(s)}
        print(f"ENTRY {e} ok={'yes' if ok else 'no'} rows={len(body)} quotes={located}/{len(quotes)} fails={','.join(fails) or '-'}")
    k = len(new)
    passed = k >= 1 and ok_n == k
    print(f"DEPTH_R82 entries={k} ok_entries={ok_n} rows={tot_rows} located_quotes={tot_q} fresh_sources={len(fresh_all)}")
    print(f"DEPTH_R82={'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
