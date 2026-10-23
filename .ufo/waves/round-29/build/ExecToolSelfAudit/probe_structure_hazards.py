#!/usr/bin/env python3
"""Structural hazard probe for the counter's skip-region bookkeeping.

Checks the eight cached registry source pages for the markup shapes that
expose the three skip-region divergences found by the audit:

  D1  a block-level element inside a dropped region (the reference still
      emits that element's one space; the contract reading drops it)
  D2  a stray end tag of one drop element inside another drop element (the
      reference's single depth counter ends the wrong region)
  D3  a self-closing drop element (<script/>, <template/>), which the
      reference does not treat as opening a dropped region

It also checks whether each page closes <head>, since an unclosed <head>
would leave the reference's depth counter above zero for the whole document.

Uses the cached pages in _cache/ (no network on a re-run).
"""
import os
import re
import sys
from html.parser import HTMLParser

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import contract_model as cm  # noqa: E402

CACHE = os.path.join(HERE, "_cache")
SOURCE_IDS = ["S002", "S003", "S008", "S013", "S019", "S020", "S038", "S044"]
SKIP = cm.CONTRACT_SKIP


class SkipScan(HTMLParser):
    """Finds the markup shapes that expose D1, D2 and D3."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # contract-literal: one region per open element
        self.depth = 0           # reference: one shared counter
        self.d1 = []             # block tag inside a dropped region
        self.d2 = []             # end tag of another drop element inside a region
        self.d3 = []             # self-closing drop element
        self.head_closed = False
        self.head_opened = False
        self.unclosed_regions = []

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            if tag == "head":
                self.head_opened = True
            self.stack.append(tag)
            self.depth += 1
            return
        if self.depth and tag in cm.CONTRACT_BLOCK:
            self.d1.append((tag, list(self.stack)))

    def handle_startendtag(self, tag, attrs):
        if tag in SKIP:
            self.d3.append(tag)
            return
        if self.depth and tag in cm.CONTRACT_BLOCK:
            self.d1.append((tag, list(self.stack)))

    def handle_endtag(self, tag):
        if tag in SKIP:
            if tag == "head":
                self.head_closed = True
            if tag not in self.stack:
                # an end tag with no matching open region
                self.d2.append((tag, list(self.stack), "no-open"))
            elif self.stack and self.stack[-1] != tag:
                self.d2.append((tag, list(self.stack), "crossed"))
            else:
                self.stack.pop()
            self.depth = max(0, self.depth - 1)
            return
        if self.depth and tag in cm.CONTRACT_BLOCK:
            self.d1.append((tag, list(self.stack)))

    def close(self):
        super().close()
        self.unclosed_regions = list(self.stack)


def main():
    print("### structural hazards on the eight registry source pages ###")
    for sid in SOURCE_IDS:
        path = os.path.join(CACHE, sid + ".html")
        if not os.path.exists(path):
            print(f"  {sid}: not cached")
            continue
        doc = open(path, encoding="utf-8").read()
        s = SkipScan()
        s.feed(doc)
        s.close()
        # raw markup spot checks
        selfclose = re.findall(r"<(script|template|style|noscript|head)\b[^>]*/>", doc, re.I)
        print(f"  {sid}:")
        print(f"    D1 block tags inside dropped regions: {len(s.d1)} {s.d1[:3]}")
        print(f"    D2 crossed/absent drop end tags: {len(s.d2)} {s.d2[:3]}")
        print(f"    D3 self-closing drop elements: {len(selfclose)} {selfclose[:3]}")
        print(f"    head opened={s.head_opened} closed={s.head_closed} "
              f"unclosed regions at EOF={s.unclosed_regions}")

    print("\n### does the reference's shared depth counter end the WRONG region? ###")
    # a demonstration that the reference leaks text where the contract drops it
    sys.path.insert(0, HERE)
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "c1_count_frozen",
        "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round29/c1-count.py")
    C = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(C)

    def ref(doc):
        p = C._Text()
        p.feed(doc)
        p.close()
        return "".join(p.out)

    for doc in ("<noscript>a</script>SECRET</noscript>",
                "<template>x</script>SECRET</template>",
                "<script/>SECRET</script>",
                "foo<noscript><p>x</p></noscript>bar"):
        print(f"  {doc!r}")
        print(f"    reference: {ref(doc)!r}")
        print(f"    contract : {cm.contract_html_to_text(doc)!r}")
        print(f"    reference norm: {C.norm(ref(doc))!r}   contract norm: {cm.contract_norm(cm.contract_html_to_text(doc))!r}")


if __name__ == "__main__":
    main()
