#!/usr/bin/env python3
"""Round-30 C1 counter: quote re-open on HTML documents that omit the head end tag.

Usage (lane root):
    python3 corpus/evidence/round30/c1-count.py [--tool tools/quote-reopen.py] [--receipt OUT.json]

Prints one line `QUOTE_REOPEN_HEADLESS_MATCH=<n>/<t>` and exits 0 iff n == t == FROZEN_TOTAL.
Exit 1 is a miss. Exit 2 is a failed measurement (harness error), never a pass.

Every run draws a fresh 64-bit seed from os.urandom; there is no seed option. All documents,
words, ids, paths and host names are generated at run time and served by the loopback
harness (qr_harness.py); nothing is fetched from the network. Labels are true by
construction: the counter knows which words it put in reader-visible body blocks and which
it put only in head content, script content or nowhere.

Per run, FROZEN_TOTAL = 106 items:

  20 documents, 5 items each (100 items):
    headless-body     5 docs  `<head>` opened, no `</head>`, `<body>` start tag present
    headless-nobody   5 docs  `<head>` opened, no `</head>`, no `<body>` start tag
    headless-text     4 docs  `<head>` opened, no `</head>`, body starts with bare text
    closed-head       6 docs  regular `<head>…</head><body>` (regression class)
  The first body element of a headless document rotates over
    p div h1 section span a img table ul (and bare text for headless-text).
  Items per document:
    body-window       2  VERBATIM  6-15 consecutive words of one body block; one is from the
                                    first body block
    title-window      1  ABSENT    4-8 words of the head <title>
    script-window     1  ABSENT    4-8 words of a JS string in a <script> (head or body)
    case-flip         1  ABSENT    a body window with one inner letter's case flipped

  6 verdict-order items:
    TOO_LONG     2  26-30 true body words; source answers 404 (length before fetch)
    NO_SOURCE    1  over-long, id with no registry row
    NO_SOURCE    1  over-long, registry row without a URL
    UNREACHABLE  1  8 true words; source answers 404
    TOO_LONG     1  26-30 true body words on a reachable document

The predicate (frozen, round-30 claims.md): C1 holds iff this command prints
QUOTE_REOPEN_HEADLESS_MATCH=106/106 against tools/quote-reopen.py on the measured revision.
"""
import argparse
import hashlib
import html
import json
import os
import random
import shutil
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import qr_harness as H  # noqa: E402

FROZEN_TOTAL = 106
LABEL = "QUOTE_REOPEN_HEADLESS_MATCH"
FIRST_ELEMENTS = ["p", "div", "h1", "section", "span", "a", "img", "table", "ul"]
CONS = "bcdfghjklmnprstvz"
VOWS = "aeiou"


def sha256(path):
    if not os.path.isfile(path):
        return None
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


class Words:
    """Unique pseudo-words; every word is used once per run, so windows never collide."""

    def __init__(self, rng):
        self.rng = rng
        self.used = set()

    def one(self):
        while True:
            w = "".join(self.rng.choice(CONS) + self.rng.choice(VOWS) for _ in range(self.rng.randint(2, 4)))
            if self.rng.random() < 0.3:
                w += self.rng.choice(CONS)
            if w not in self.used:
                self.used.add(w)
                return w

    def run(self, n, capitalize_first=True):
        ws = [self.one() for _ in range(n)]
        if capitalize_first:
            ws[0] = ws[0][0].upper() + ws[0][1:]
        return ws


def found(text, q):
    """Boundary-aware occurrence (same rule as the frozen tool contract), for label self-checks."""
    i = 0
    while True:
        i = text.find(q, i)
        if i < 0:
            return False
        j = i + len(q)
        if (i == 0 or not text[i - 1].isalnum()) and (j == len(text) or not text[j].isalnum()):
            return True
        i += 1


def inline_markup(rng, words):
    """Render words as HTML with inline tags that emit no text boundary."""
    out = []
    i = 0
    while i < len(words):
        r = rng.random()
        if r < 0.15 and i + 2 <= len(words):
            out.append("<em>%s %s</em>" % (words[i], words[i + 1]))
            i += 2
        elif r < 0.25:
            out.append('<a href="#x%d">%s</a>' % (i, words[i]))
            i += 1
        elif r < 0.30:
            out.append("<code>%s</code>" % words[i])
            i += 1
        else:
            out.append(words[i])
            i += 1
    return " ".join(out)


def block(rng, tag, words):
    body = inline_markup(rng, words)
    if tag == "table":
        return "<table><tr><td>%s</td></tr></table>" % body
    if tag == "ul":
        return "<ul><li>%s</li></ul>" % body
    if tag == "img":
        return '<img src="x.png" alt="figure"><p>%s</p>' % body
    if tag in ("span", "a"):
        attr = ' href="#top"' if tag == "a" else ""
        return "<%s%s>%s</%s>" % (tag, attr, body, tag)
    return "<%s>%s</%s>" % (tag, body, tag)


def make_doc(rng, W, cls, first):
    """Return (html_bytes, body_blocks [list of word lists], title_words, script_words)."""
    title = W.run(rng.randint(6, 10))
    script = W.run(rng.randint(6, 10), capitalize_first=False)
    style_word = W.one()
    blocks = [W.run(rng.randint(30, 42)) for _ in range(rng.randint(2, 3))]
    script_in_head = rng.random() < 0.5
    js = '<script>var note = "%s";</script>' % " ".join(script)
    head = ['<meta charset="utf-8">', "<title>%s</title>" % " ".join(title),
            '<link rel="stylesheet" href="s.css">', "<style>.%s { color: red }</style>" % style_word]
    if script_in_head:
        head.append(js)
    rng.shuffle(head)
    parts = ["<!doctype html>", '<html lang="en">', "<head>"] + head
    if cls == "closed-head":
        parts.append("</head>")
    if cls in ("closed-head", "headless-body"):
        parts.append('<body class="page">')
    # first body content
    if cls == "headless-text":
        parts.append("\n" + inline_markup(rng, blocks[0]))
        rest = blocks[1:]
    else:
        parts.append(block(rng, first, blocks[0]))
        rest = blocks[1:]
    for k, b in enumerate(rest):
        if not script_in_head and k == 0:
            parts.append(js)
        parts.append(block(rng, rng.choice(["p", "div", "section"]), b))
    if not script_in_head and not rest:
        parts.append(js)
    if cls in ("closed-head", "headless-body"):
        parts.append("</body>")
    parts.append("</html>")
    return "\n".join(parts).encode("utf-8"), blocks, title, script


def window(rng, words, lo, hi):
    n = rng.randint(lo, min(hi, len(words)))
    s = rng.randint(0, len(words) - n)
    return words[s:s + n]


def case_flip(rng, words):
    """Flip the case of one inner lowercase letter of one word in a window."""
    w = window(rng, words, 6, 12)
    k = rng.randrange(len(w))
    word = w[k]
    pos = [i for i in range(1, len(word)) if word[i].islower()]
    i = rng.choice(pos)
    w = list(w)
    w[k] = word[:i] + word[i].upper() + word[i + 1:]
    return w


def build(rng):
    W = Words(rng)
    docs, items, rows = [], [], []
    plan = (["headless-body"] * 5 + ["headless-nobody"] * 5 + ["headless-text"] * 4 + ["closed-head"] * 6)
    firsts = FIRST_ELEMENTS[:]
    rng.shuffle(firsts)
    sid_n = rng.randint(100, 800)

    def new_sid():
        nonlocal sid_n
        sid_n += 1
        return "S%d" % sid_n

    def new_id():
        return "%016x" % rng.getrandbits(64)

    visible_all = []
    for d, cls in enumerate(plan):
        first = firsts[d % len(firsts)]
        body, blocks, title, script = make_doc(rng, W, cls, first)
        path = "/d/%016x" % rng.getrandbits(64)
        host = "h%x.example-%x.test" % (rng.getrandbits(24), d)
        sid = new_sid()
        docs.append({"path": path, "body": body, "host": host, "sid": sid, "cls": cls, "first": first})
        rows.append((sid, "http://%s%s" % (host, path)))
        visible_all.append(" ".join(" ".join(b) for b in blocks))
        items.append((new_id(), sid, " ".join(window(rng, blocks[0], 6, 15)), "VERBATIM", cls, "body-window"))
        other = blocks[rng.randrange(len(blocks))]
        items.append((new_id(), sid, " ".join(window(rng, other, 6, 15)), "VERBATIM", cls, "body-window"))
        items.append((new_id(), sid, " ".join(window(rng, title, 4, 8)), "ABSENT", cls, "title-window"))
        items.append((new_id(), sid, " ".join(window(rng, script, 4, 8)), "ABSENT", cls, "script-window"))
        items.append((new_id(), sid, " ".join(case_flip(rng, blocks[rng.randrange(len(blocks))])), "ABSENT",
                      cls, "case-flip"))
    # verdict-order items
    gone_sid, gone_host = new_sid(), "gone%x.test" % rng.getrandbits(24)
    rows.append((gone_sid, "http://%s/nf/%016x" % (gone_host, rng.getrandbits(64))))
    src_words = W.run(60)
    reach = docs[rng.randrange(len(docs))]
    long_true = []
    for _ in range(3):
        n = rng.randint(26, 30)
        s = rng.randint(0, 60 - n)
        long_true.append(" ".join(src_words[s:s + n]))
    items.append((new_id(), gone_sid, long_true[0], "TOO_LONG", "order", "too-long-unreachable"))
    items.append((new_id(), gone_sid, long_true[1], "TOO_LONG", "order", "too-long-unreachable"))
    items.append((new_id(), new_sid(), long_true[2], "NO_SOURCE", "order", "no-source-unregistered"))
    urlless = new_sid()
    rows.append((urlless, None))
    items.append((new_id(), urlless, long_true[0], "NO_SOURCE", "order", "no-source-urlless"))
    items.append((new_id(), gone_sid, " ".join(src_words[:8]), "UNREACHABLE", "order", "unreachable"))
    # too-long true text on a reachable doc: rebuild from that doc's own first block
    items.append((new_id(), reach["sid"], None, "TOO_LONG", "order", "too-long-reachable"))
    return docs, items, rows, visible_all, gone_host, reach


def main(argv):
    ap = argparse.ArgumentParser(prog="c1-count.py")
    ap.add_argument("--tool", default=os.path.join(LANE, "tools", "quote-reopen.py"))
    ap.add_argument("--receipt", default=None)
    args = ap.parse_args(argv)
    seed = int.from_bytes(os.urandom(8), "big")
    rng = random.Random(seed)
    docs, items, rows, visible_all, gone_host, reach = build(rng)
    # fill the reachable too-long item from that document's own visible text
    vis_reach = visible_all[docs.index(reach)].split()
    n = rng.randint(26, 30)
    s = rng.randint(0, len(vis_reach) - n)
    fixed = []
    for it in items:
        if it[2] is None:
            it = (it[0], it[1], " ".join(vis_reach[s:s + n])) + it[3:]
        fixed.append(it)
    items = fixed
    # label self-checks by construction
    vis = "  ".join(visible_all)
    for it in items:
        q, lab, kind = it[2], it[3], it[5]
        if kind == "body-window" and not found(vis, q):
            sys.stderr.write("c1-count: construction error (body window not visible)\n")
            return 2
        if kind in ("title-window", "script-window", "case-flip") and found(vis, q):
            sys.stderr.write("c1-count: construction error (absent item visible)\n")
            return 2
        if lab == "TOO_LONG" and not (25 < len(q.split()) <= 30):
            sys.stderr.write("c1-count: construction error (length)\n")
            return 2
    rng.shuffle(items)
    gaddrs = H.global_addrs(rng, len(docs) + 1)
    resolve = {}
    for d, g in zip(docs, gaddrs):
        resolve[d["host"]] = [[g]]
    resolve[gone_host] = [[gaddrs[-1]]]
    srv = H.Server()
    work = tempfile.mkdtemp(prefix="chousa-r30-c1-")
    try:
        for d in docs:
            srv.add(d["path"], d["body"])
        res = H.run_tool(args.tool, work, [(i, s, q) for i, s, q, *_ in items], rows, resolve,
                         gaddrs, srv.port, deadline=None, cap=180.0)
    finally:
        srv.close()
    n_ok = 0
    by_class = {}
    misses = []
    for it in items:
        got = res["verdicts"].get(it[0])
        ok = got == it[3]
        n_ok += ok
        key = "%s/%s" % (it[4], it[5])
        c = by_class.setdefault(key, [0, 0])
        c[0] += ok
        c[1] += 1
        if not ok and len(misses) < 40:
            misses.append({"class": key, "label": it[3], "got": got})
    t = len(items)
    holds = (n_ok == t == FROZEN_TOTAL)
    print("%s=%d/%d" % (LABEL, n_ok, t))
    receipt = {
        "label": LABEL, "n": n_ok, "t": t, "frozen_total": FROZEN_TOTAL, "predicate_holds": holds,
        "seed": seed, "counter_sha256": sha256(os.path.abspath(__file__)),
        "harness_sha256": sha256(os.path.join(HERE, "qr_harness.py")),
        "tool": os.path.relpath(os.path.abspath(args.tool), LANE), "tool_sha256": sha256(args.tool),
        "tool_rc": res["rc"], "tool_killed": res["killed"], "wall_s": round(res["wall"], 3),
        "by_class": by_class, "misses_first40": misses,
        "net_connect_events": sum(1 for e in res["net"] if e.get("ev") == "connect"),
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "argv": ["python3", "corpus/evidence/round30/c1-count.py"] + argv,
    }
    if args.receipt:
        with open(args.receipt, "w", encoding="utf-8") as f:
            json.dump(receipt, f, indent=1, sort_keys=True)
            f.write("\n")
    shutil.rmtree(work, ignore_errors=True)
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
