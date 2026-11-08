import re, pathlib, html

OUT = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-85/w1/R85ExecReopen")
CAP = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/captures")

QUOTES = {
 "S215": [
  ("Q1", "Provenance chains comprising only Entities can be formed using the prov:wasDerivedFrom property."),
  ("Q2", "A derivation is a transformation of one entity into another."),
  ("Q3", "then we can say that the bar chart prov:wasDerivedFrom the dataset."),
  ("Q4", "The properties prov:generatedAtTime and prov:invalidatedAtTime can be used to bound the starting and ending moments of an Entity's existence."),
 ],
 "S026": [
  ("Q5", "Detailed provenance includes facets such as how the resource was generated, why it was generated, by whom, under what conditions"),
  ("Q6", "using what starting-data or source-resource, using what funding/resources, who owns the data, who should be given credit"),
 ],
 "S024": [
  ("Q7", "Date on which the content on this web page was last reviewed for accuracy and/or completeness."),
 ],
}
KEYS = {"S215":"6e48bcc4a04d13b7b3ebb68e","S026":"67983a3dbbd1d690aa648744","S024":"11d6cc56bb24adfc61eea2b4"}

def norm(s):
    s = s.replace("\u2019","'").replace("\u2018","'").replace("\u201c",'"').replace("\u201d",'"')
    return " ".join(s.split())

# Also fold curly apostrophes fold - counter norm handles those 4; also handle \u2019 variations already.

for sid, quotes in QUOTES.items():
    text = (CAP / f"{KEYS[sid]}.txt").read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    ntext = norm(text)
    print(f"=== {sid} key={KEYS[sid]} lines={len(lines)} norm_chars={len(ntext)} ===")
    for qid, quote in quotes:
        nq = norm(quote)
        found = nq in ntext
        # word count
        wc = len(quote.split())
        flag = "" if 8 <= wc <= 25 else " *** OUTSIDE 8..25 ***"
        # find line number: first line whose normalized form contains the normalized quote OR where normalized line contains quote fragment
        line_no = None
        nlines = [norm(ln) for ln in lines]
        # try exact containment per line
        for i, nl in enumerate(nlines, 1):
            if nq in nl:
                line_no = i
                break
        if line_no is None:
            # sliding: find in whole normalized text, then map char pos -> line approx
            # fallback: find which lines overlapping? Just report not found per-line
            line_no = "none-per-line"
        print(f"{qid} FOUND={found} line={line_no} words={wc}{flag}")
        print(f"  quote: {quote}")
        print(f"  norm-quote: {nq}")
        if found and line_no != "none-per-line":
            print(f"  line-text: {lines[line_no-1][:300]!r}")
        print()
