import re, html, pathlib

SCRATCH = pathlib.Path("/fast/scratch/hyaku/chousa-r85/R85ExecReopen")

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
FILES = {"S215": "S215-plain.html", "S026": "S026.html", "S024": "S024.html"}

def strip_tags(s):
    # drop script/style
    s = re.sub(r'<script[^>]*>.*?</script>', ' ', s, flags=re.I|re.S)
    s = re.sub(r'<style[^>]*>.*?</style>', ' ', s, flags=re.I|re.S)
    # replace tags with space
    s = re.sub(r'<[^>]+>', ' ', s)
    return s

def norm(s):
    s = s.replace("\u2019","'").replace("\u2018","'").replace("\u201c",'"').replace("\u201d",'"')
    return " ".join(s.split())

for sid, quotes in QUOTES.items():
    raw = (SCRATCH / FILES[sid]).read_bytes()
    print(f"=== {sid} file={FILES[sid]} bytes_on_disk={len(raw)} ===")
    text = raw.decode("utf-8", errors="replace")
    stripped = html.unescape(strip_tags(text))
    ntext = norm(stripped)
    print(f"norm_chars={len(ntext)}")
    for qid, quote in quotes:
        nq = norm(quote)
        found = nq in ntext
        wc = len(quote.split())
        flag = "" if 8 <= wc <= 25 else " *** OUTSIDE 8..25 ***"
        print(f"{qid} FOUND={found} words={wc}{flag}")
        print(f"  quote: {quote}")
        if not found:
            # debug: search for distinctive substring
            frag = norm(quote[:40])
            idx = ntext.find(frag)
            print(f"  [debug] first-40 frag found at {idx}: {ntext[idx:idx+200] if idx>=0 else 'NONE'}")
            # try keywords
            for kw in re.findall(r'\S+', quote)[:6]:
                print(f"    kw {kw!r}: {'YES' if kw in ntext else 'no'}")
    print()
