#!/usr/bin/env python3
"""Compare a literal reading of contract v2 item 1 with Chromium's HTML parser (DOMParser).

Docs: the frozen C1 generator (c1-count.py make_doc, imported read-only) over several seeds,
plus hand-written edge cases. Output: JSON lines with per-doc agreement on (a) extracted text,
(b) the list of elements the parser puts inside <head>.
"""
import importlib.util
import json
import os
import random
import subprocess
import sys
import tempfile
from html.parser import HTMLParser

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(LANE, "corpus/evidence/round30"))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


C1 = load("c1count", os.path.join(LANE, "corpus/evidence/round30/c1-count.py"))
TOOL = load("qrtool", os.path.join(LANE, "tools/quote-reopen.py"))

HEAD_OK = {"base", "basefont", "bgsound", "link", "meta", "noframes", "noscript", "script", "style",
           "template", "title"}
DROP = {"title", "script", "style", "noscript", "template"}
WS = " \t\n\f\r"


class Item1(HTMLParser):
    """Literal contract v2 item 1 on the stdlib parser (scripting=False, as the round-29 tool)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.drop, self.in_head, self.inner = [], 0, False, 0
        self.head_elems = []

    def handle_starttag(self, tag, attrs):
        if tag == "head":
            self.in_head = True
            return
        if self.in_head and not self.inner and (tag == "body" or tag not in HEAD_OK):
            self.in_head = False
        if self.in_head and not self.inner:
            self.head_elems.append(tag)
        if self.in_head and tag in ("noframes", "noscript", "template", "title", "script", "style"):
            self.inner += 1
        if tag in DROP:
            self.drop += 1
        elif tag in TOOL.BLOCK and not self.in_head:
            self.out.append(" ")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag in DROP or (self.in_head and tag in ("noframes",)):
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == "head" and self.in_head:
            self.in_head = False
            return
        if self.in_head and self.inner and tag in ("noframes", "noscript", "template", "title", "script",
                                                    "style"):
            self.inner -= 1
        if tag in DROP:
            self.drop = max(0, self.drop - 1)
        elif tag in TOOL.BLOCK and not self.in_head:
            self.out.append(" ")

    def handle_data(self, data):
        if self.in_head and not self.inner and data.strip(WS):
            self.in_head = False
        if self.in_head or self.drop:
            return
        self.out.append(data)


def item1(doc):
    p = Item1()
    p.feed(doc)
    p.close()
    return TOOL.norm("".join(p.out)), p.head_elems


EDGE = {
    "noscript-link-in-head": "<!doctype html><html><head><noscript><link rel=x></noscript><title>T t</title>"
                             "<p>Body one</p></html>",
    "noscript-p-in-head": "<!doctype html><html><head><noscript><p>Ns text</p></noscript><title>T t</title>"
                          "<p>Body two</p></html>",
    "template-div-in-head": "<!doctype html><html><head><template><div>Tpl text</div></template><meta charset=utf-8>"
                            "<p>Body three</p></html>",
    "br-endtag-in-head": "<!doctype html><html><head><title>T t</title></br>After br text<p>Body four</p></html>",
    "html-starttag-in-head": "<!doctype html><html><head><html lang=x><title>T t</title><p>Body five</p></html>",
    "second-head-in-head": "<!doctype html><html><head><head><title>T t</title><p>Body six</p></html>",
    "body-endtag-in-head": "<!doctype html><html><head><title>T t</title></body>After body end<p>Body seven</p>",
    "noframes-in-head": "<!doctype html><html><head><noframes>Nf head</noframes><p>Body eight</p></html>",
    "noframes-in-body": "<!doctype html><html><head></head><body><noframes>Nf body</noframes><p>Body nine</p>",
    "nbsp-then-p": "<!doctype html><html><head><title>T t</title>&nbsp;<p>Body ten</p></html>",
    "vt-then-text": "<!doctype html><html><head><title>T t</title>\x0bVt text<p>Body eleven</p></html>",
    "comment-in-head": "<!doctype html><html><head><title>T t</title><!-- c --><p>Body twelve</p></html>",
    "head-tag-in-body": "<!doctype html><html><head></head><body><p>A a</p><head>Late head text<p>B b</p>",
    "unclosed-title": "<!doctype html><html><head><title>T t<p>Body thirteen</p></html>",
    "noscript-text-in-head": "<!doctype html><html><head><noscript>Plain ns</noscript><p>Body fourteen</p></html>",
}

JS = r"""
const BLOCK = new Set(%s);
const DROP = new Set(["SCRIPT","STYLE","NOSCRIPT","TEMPLATE","TITLE"]);
const docs = %s;
const res = {};
for (const [k, src] of Object.entries(docs)) {
  const d = new DOMParser().parseFromString(src, "text/html");
  const out = [];
  const walk = (n) => {
    if (n.nodeType === 3) { out.push(n.data); return; }
    if (n.nodeType !== 1) return;
    const t = n.tagName;
    if (t === "HEAD" || DROP.has(t)) return;
    const b = BLOCK.has(t.toLowerCase());
    if (b) out.push(" ");
    for (const c of n.childNodes) walk(c);
    if (b) out.push(" ");
  };
  walk(d.documentElement);
  const inner = (() => { try { return d.body ? d.body.innerText : null; } catch (e) { return null; } })();
  res[k] = {text: out.join(""), head: [...d.head.children].map(e => e.tagName.toLowerCase()),
            noframes_in_body_text: inner};
}
document.body.textContent = "RESULT" + JSON.stringify(res) + "ENDRESULT";
"""


def chromium(docs):
    page = "<!doctype html><html><body><script>%s</script></body></html>" % (
        JS % (json.dumps(sorted(TOOL.BLOCK)), json.dumps(docs).replace("</", "<\\/")))
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=HERE, delete=False) as f:
        f.write(page)
        path = f.name
    prof = tempfile.mkdtemp(dir=HERE, prefix="chprof-")
    cmd = ["timeout", "120", "unshare", "-rn", "chromium", "--headless", "--no-sandbox", "--disable-gpu",
           "--no-first-run", "--disable-background-networking", "--user-data-dir=" + prof,
           "--virtual-time-budget=5000", "--dump-dom", "file://" + path]
    p = subprocess.run(cmd, capture_output=True, text=True)
    os.unlink(path)
    s = p.stdout
    i, j = s.find("RESULT"), s.rfind("ENDRESULT")
    if i < 0:
        sys.stderr.write(p.stderr[-2000:])
        raise SystemExit("chromium produced no result rc=%d" % p.returncode)
    import html as H
    return json.loads(H.unescape(s[i + 6:j]))


def main():
    seeds = [int(a) for a in sys.argv[1:]] or [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    docs, meta = {}, {}
    for seed in seeds:
        rng = random.Random(seed)
        gdocs, *_ = C1.build(rng)
        for k, d in enumerate(gdocs):
            key = "s%d-d%02d" % (seed, k)
            docs[key] = d["body"].decode("utf-8")
            meta[key] = (d["cls"], d["first"])
    for k, v in EDGE.items():
        docs["edge-" + k] = v
        meta["edge-" + k] = ("edge", k)
    ref = chromium(docs)
    agree_text = agree_head = n = 0
    rows = []
    for key, src in docs.items():
        t, he = item1(src)
        r = ref[key]
        rt = TOOL.norm(r["text"])
        ok_t, ok_h = t == rt, he == r["head"]
        r29 = TOOL.norm(TOOL.html_to_text(src))
        if not key.startswith("edge-"):
            n += 1
            agree_text += ok_t
            agree_head += ok_h
        if key.startswith("edge-") or not (ok_t and ok_h):
            rows.append({"doc": key, "cls": meta[key][0], "first": meta[key][1], "text_equal": ok_t,
                         "head_equal": ok_h, "item1_head": he, "chromium_head": r["head"],
                         "item1_text": t[:120], "chromium_text": rt[:120], "round29_text": r29[:120],
                         "chromium_innerText": (r["noframes_in_body_text"] or "")[:120]})
    print(json.dumps({"generated_docs": n, "seeds": seeds, "text_equal": agree_text, "head_equal": agree_head},
                     sort_keys=True))
    for row in rows:
        print(json.dumps(row, sort_keys=True))


if __name__ == "__main__":
    main()
