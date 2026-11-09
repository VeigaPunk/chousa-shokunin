#!/usr/bin/env python3
"""Independent C2 verifier: quote location + numeral sourcing (R100ExecC2Repro)."""
import json, re, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
ENTRY = ROOT + "/corpus/knowledge/quotation-error-update-r100.md"
CAP = {  # source id -> capture file
    "S238": ROOT + "/corpus/captures/b5eec205612ee5f138cf065d.txt",
    "S236": ROOT + "/corpus/captures/405a0054e1f6dbd1854a3618.txt",
}
def norm(s):
    for a, b in [("‘","'"),("’","'"),("“",'"'),("”",'"')]:
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()
def field(src, qid):
    j = json.load(open(CAP[src], encoding="utf-8"))
    rec = j["resultList"]["result"][0]
    return norm(rec["title"]) if qid == "U0" else norm(rec["abstractText"])
def parse_rows(text):
    lines = text.splitlines()
    i = next(k for k, l in enumerate(lines) if l.startswith("## Located quotes"))
    j = next(k for k, l in enumerate(lines) if l.startswith("## Decision table"))
    rows = []
    for l in lines[i:j]:
        m = re.match(r"\|\s*(\w+)\s*\|\s*(S\d+)\s*\|\s*\"(.*)\"\s*\|", l)
        if m: rows.append((m.group(1), m.group(2), m.group(3)))
    drows = []
    for l in lines[j:]:
        if l.startswith("| ") and l.count("|") >= 6:
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if len(cells) >= 5 and cells[0] not in ("Situation", "---"):
                drows.append(cells)
    return rows, drows
text = open(ENTRY, encoding="utf-8").read()
qrows, drows = parse_rows(text)
print(f"quoted_rows={len(qrows)} decision_rows={len(drows)}")
quotes = {}
ok = bad = 0
for qid, src, q in qrows:
    quotes[qid] = q
    hit = norm(q) in field(src, qid)
    print(("PASS" if hit else "FAIL"), qid, src, "located" if hit else "ABSENT")
    ok += hit; bad += not hit
print(f"QUOTES_LOCATED={ok}/{len(qrows)}")
numre = re.compile(r"[-+]?\d[\d.,]*%?|\d[\d.,]*%\b")
wok = wbad = 0
for cells in drows:
    sit, do, never, warrant, lane = cells[0], cells[1], cells[2], cells[3], cells[4]
    wq = [w.strip() for w in warrant.split(",") if w.strip()]
    pool = " ".join(norm(quotes[w]) for w in wq if w in quotes)
    nums = numre.findall(do + " " + never)
    nums = [n.strip() for n in nums if n.strip()]
    # also catch spelled '-' sign attached: covered by regex
    miss = []
    for n in nums:
        # token-equal incl sign & form: exact substring token check
        if n not in pool:
            # allow trailing % vs % variant? no -- strict
            miss.append(n)
    status = "PASS" if not miss else "FAIL"
    print(status, sit[:42], "| numerals:", len(nums), "| missing:", miss, "| warrants:", wq)
    wok += not miss; wbad += bool(miss)
print(f"DECISION_NUMERALS_OK={wok}/{len(drows)}")
sys.exit(0 if bad == 0 and wbad == 0 else 1)
