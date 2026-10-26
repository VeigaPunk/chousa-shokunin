#!/usr/bin/env python3
"""Round-52 C1 control: the cheap reading of a .docx — unzip the fixed member
word/document.xml, newline at </w:p>, tab at <w:tab.../>, newline at <w:br/>,
strip every other tag, html.unescape; --locate by str.find/count; refuse a
non-zip. No relationship lookup, no revision/field/Fallback/tab-stop rule."""
import html, re, sys, zipfile
def text(p):
    if not zipfile.is_zipfile(p):
        print("REFUSED not a zip", file=sys.stderr); sys.exit(2)
    try:
        x = zipfile.ZipFile(p).read("word/document.xml").decode("utf-8")
    except KeyError:
        print("REFUSED no word/document.xml", file=sys.stderr); sys.exit(2)
    x = re.sub(r"</w:p>", "\n", x); x = re.sub(r"<w:tab\b[^>]*/>", "\t", x); x = re.sub(r"<w:(?:br|cr)\b[^>]*/>", "\n", x)
    x = re.sub(r"<\?xml[^>]*\?>\s*", "", x)
    return html.unescape(re.sub(r"<[^>]+>", "", x))
a = sys.argv[1:]
t = text(a[0])
if "--locate" in a:
    q = a[a.index("--locate") + 1]; n = t.count(q)
    print(f"LOCATED count={n} offset={t.find(q) if n else -1}"); sys.exit(0 if n == 1 else 1)
sys.stdout.buffer.write(t.encode()); sys.exit(0)
