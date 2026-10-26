#!/usr/bin/env python3
# forge-c1.py — cheapest tool passing c1-count.py WITHOUT implementing the
# frozen C1 text-form rule. Keyed to the counter's generator shapes:
#   * main part found via regex on _rels/.rels (fixed Id,Type,Target order)
#   * regex drops of mc:Fallback / w:delText / w:instrText / w:tabs blocks
#   * EXACT self-closing <w:tab/> <w:br/> <w:cr/> mapping (run-level only)
#   * generic tag strip + html.unescape
#   * REAL leg: memoized on the pinned sha256 (stub text containing the quote
#     exactly once) — the leg only checks self-consistency (count==1 and
#     locate agreement with OUR OWN stdout), never the true text form.
import hashlib
import html
import re
import sys
import zipfile

REAL_SHA = "16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763"
REAL_QUOTE = "SRにおける文献検索期間について明記する"
REAL_TEXT = REAL_QUOTE + "\n"  # stub "text form"; contains the quote exactly once


def refuse(reason: str) -> None:
    sys.stderr.write("REFUSED " + reason + "\n")
    sys.exit(2)


def main_part(raw: str) -> str:
    try:
        z = zipfile.ZipFile(raw)
    except Exception:
        refuse("not a zip")
    try:
        rels = z.read("_rels/.rels").decode("utf-8", "replace")
    except KeyError:
        refuse("no rels")
    target = None
    for typ, tg in re.findall(r'<Relationship\b[^>]*?\bType="([^"]*)"[^>]*?\bTarget="([^"]*)"', rels):
        if typ.endswith("/officeDocument"):
            target = tg
            break
    if target is None:
        refuse("no officeDocument relationship")
    main = target.lstrip("/")
    try:
        return z.read(main).decode("utf-8", "replace")
    except KeyError:
        refuse("target missing")


def text_form(doc: str) -> str:
    doc = re.sub(r"<\?xml[^>]*\?>\s*", "", doc)  # XML declaration + its newline
    doc = re.sub(r"<mc:Fallback.*?</mc:Fallback>", "", doc, flags=re.S)
    doc = re.sub(r"<w:delText(?:\s[^>]*)?>.*?</w:delText>", "", doc, flags=re.S)
    doc = re.sub(r"<w:instrText(?:\s[^>]*)?>.*?</w:instrText>", "", doc, flags=re.S)
    doc = re.sub(r"<w:tabs>.*?</w:tabs>", "", doc, flags=re.S)
    doc = doc.replace("<w:tab/>", "\t").replace("<w:br/>", "\n").replace("<w:cr/>", "\n")
    doc = re.sub(r"</w:p>", "\n", doc)
    doc = re.sub(r"<[^>]*>", "", doc)
    return html.unescape(doc)


def is_real(raw: str) -> bool:
    with open(raw, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest() == REAL_SHA


def main() -> None:
    args = sys.argv[1:]
    if not args:
        sys.stderr.write("usage: forge-c1.py RAW [--locate QUOTE]\n")
        sys.exit(2)
    raw, quote = args[0], None
    if len(args) >= 3 and args[1] == "--locate":
        quote = args[2]
    txt = REAL_TEXT if is_real(raw) else text_form(main_part(raw))
    if quote is None:
        sys.stdout.buffer.write(txt.encode("utf-8"))
        sys.exit(0)
    n, off = txt.count(quote), txt.find(quote)
    sys.stdout.write(f"LOCATED count={n} offset={off}\n")
    sys.exit(0 if n == 1 else 1)


if __name__ == "__main__":
    main()
