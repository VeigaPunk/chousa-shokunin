"""
Probe (a): qualifying disagreement between _qualifying_203 and count_203_rows
Predicate differences (from read):
_qualifying_203:
  if f[5] != "0" or f[8] in ("-", ""): continue
  if not f[6].isdigit() or f[6] == "200": continue
  ... registry, key, capture exists, sha==txt, quotable line 8-25 words exists
  appends (sid,url,...) per ROW -> duplicates kept (test: same sid+url repeated rows produce dupes?)
count_203_rows:
  if rc != "0" or http == "200" or txt == "-" or not http.isdigit() or len(http) != 3: continue
  ... registry, key, capture exists+sha==txt, quotable line exists
  seen.add((sid,url)) -> deduplicates

Differences:
1) count requires len(http)==3, _qual does not. So for http like "2030" or "0203" or "2" with 0? Let's see: isdigit true, !=200, so _qual accepts, count rejects.
   Also http "0200"? Hmm 0200 isdigit !=200 -> _qual accepts as qualifying (non-200). count: len!=3 -> rejects. But 0200 is 200 numerically.
   Also http "203" both accept.
2) _qual dedup? No: returns list with dupes. count uses set of (sid,url). So duplicate refetch rows for same sid+url
   (e.g. S021/S032 share url 17638714 but distinct sid; or S021 repeated attempt rows) would make len(_qual) > len(set).
   Actually S021 and S032 are different sid, same url -> both counted. But duplicate (sid,url) pairs from attempt 1 vs 2 would dedup in count but not in _qual.
3) count checks txt == "-" only, _qual checks txt in ("-",""). Empty string txt would pass count's first filter? txt=="" != "-" so passes first check, then later sha check: sha != "" so fails. So equivalent.
4) count checks http == "200" before isdigit/len; _qual checks isdigit then ==200. Order irrelevant except for http="abc": _qual: not isdigit -> reject; count: not isdigit -> reject.
5) build_d1/d2 use _qual's http value verbatim in D2 record: http={http} where http may be non-3-digit.
   D1 record does not include http at all (admit form).
6) w-len check identical: 8..25 with split().

Concrete committed-bytes case: http_code = "0203" or "1203"? Need digits, non-200, len !=3.
   _qual: isdigit True, != "200" -> qualifies, builds D1 admit + D2 reject with http=0203
   count: len("0203")=4 -> skips, returns lower count.
   Then D1_WIDTH leg: len(d1) != d1_expected -> fails. So the two builders disagree -> width leg catches.
   But attacker could patch BOTH sides (E1-style) to narrow.

Test: construct fake refetch.tsv + SOURCES.md + capture to prove disagreement.
Also test duplicate (sid,url) rows: two identical rows produce 2 entries from _qual but 1 from count.

We do this in Python importing the instrument functions.
"""
import sys, os, hashlib, tempfile, shutil
sys.path.insert(0, "/fast/scratch/hyaku/chousa-r87/R87ReviewerC1/wt/corpus/evidence/round87")

# import
import importlib.util
spec = importlib.util.spec_from_file_location("gr87", "/fast/scratch/hyaku/chousa-r87/R87ReviewerC1/wt/corpus/evidence/round87/gate-records-r87.py")
gr87 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gr87)

# Build minimal tree: corpus/SOURCES.md, corpus/evidence/round57/refetch.tsv, corpus/captures/<key>.txt
def build_tree(mut_refetch_rows, tmp):
    os.makedirs(os.path.join(tmp, "corpus/captures"), exist_ok=True)
    os.makedirs(os.path.join(tmp, "corpus/evidence/round57"), exist_ok=True)
    # registry rows: need 11 cells, cells[0]=sid, cells[1] contains url, cells[3]=tier
    # Format: `| S001 | url row | x | A | ... |` -> 11 cells. We use emit_reg helper.
    def reg(sid, url, tier="A"):
        cells = [sid, url, "x", tier, "x", "x", "x", "mined", "x", "x", "x"]
        return "| " + " | ".join(cells) + " |"
    srcs = "\n".join(reg(sid, url, tier) for sid, url, tier in [("S001","https://example.test/a","A"),("S002","https://example.test/b","A")])
    with open(os.path.join(tmp, "corpus/SOURCES.md"), "w") as f:
        f.write(srcs + "\n")
    with open(os.path.join(tmp, "corpus/evidence/round57/refetch.tsv"), "w") as f:
        f.write("id\turl\tkey\tattempt\tfetched_utc\tcurl_rc\thttp_code\traw_sha256\ttxt_sha256\n")
        for row in mut_refetch_rows:
            f.write("\t".join(row) + "\n")

    # captures: each distinct url needs capture file whose sha equals txt
    for row in mut_refetch_rows:
        sid, url, key = row[0], row[1], row[2]
        if row[8] not in ("-", ""):
            cap = os.path.join(tmp, "corpus/captures", key + ".txt")
            # write capture with quotable line: 10 words
            quote = "one two three four five six seven eight nine ten"
            body = (quote + "\n").encode()
            with open(cap, "wb") as f:
                f.write(body)
            # fix txt to actual sha
            row[8] = hashlib.sha256(body).hexdigest()
    # rewrite refetch with corrected shas
    with open(os.path.join(tmp, "corpus/evidence/round57/refetch.tsv"), "w") as f:
        f.write("id\turl\tkey\tattempt\tfetched_utc\tcurl_rc\thttp_code\traw_sha256\ttxt_sha256\n")
        for row in mut_refetch_rows:
            f.write("\t".join(row) + "\n")
    # also key must equal sha256(url)[:24]
    return tmp

def mkrow(sid, url, http, rc="0", key=None):
    if key is None:
        key = hashlib.sha256(url.encode()).hexdigest()[:24]
    return [sid, url, key, "1", "2026-01-01T00:00:00Z", rc, http, "deadbeef", "x"]

print("=== test 1: normal 203 ===")
t = tempfile.mkdtemp()
b = build_tree([mkrow("S001","https://example.test/a","203")], t)
print(" _qual:", [(x[0],x[7]) for x in gr87._qualifying_203(b)], "count:", gr87.count_203_rows(b))
shutil.rmtree(t)

print("=== test 2: http=0203 (4 digits) ===")
t = tempfile.mkdtemp()
b = build_tree([mkrow("S001","https://example.test/a","0203")], t)
print(" _qual len:", len(gr87._qualifying_203(b)), "count:", gr87.count_203_rows(b))
print(" _qual http values:", [x[7] for x in gr87._qualifying_203(b)])
shutil.rmtree(t)

print("=== test 3: duplicate (sid,url) rows (attempt 1+2 identical) ===")
t = tempfile.mkdtemp()
r1 = mkrow("S001","https://example.test/a","203"); r2 = mkrow("S001","https://example.test/a","203")
b = build_tree([r1,r2], t)
print(" _qual len (dup rows):", len(gr87._qualifying_203(b)), "count (deduped):", gr87.count_203_rows(b))
print(" D1 forges:", len(gr87.build_d1_203_admits(b)), "D2 forges:", len(gr87.build_d2_203_rejects(b)))
shutil.rmtree(t)

print("=== test 4: committed S021/S032 duplicate url distinct sid ===")
# S021 and S032 in real tree share url+key+fetched? They share url 17638714 but fetched differs by 11s and sha same txt.
# In our model both are _qual entries, count dedups only on (sid,url) so distinct sid -> not deduped. OK.
# But what about S021 with two identical (sid,url) rows at different fetched? count collapses, _qual does not.
t = tempfile.mkdtemp()
b = build_tree([mkrow("S001","https://example.test/a","203"), mkrow("S001","https://example.test/a","203")], t)
print(" _qual len:", len(gr87._qualifying_203(b)), "count:", gr87.count_203_rows(b))
shutil.rmtree(t)

print("=== test 5: http=20 (2 digits) ===")
t = tempfile.mkdtemp()
b = build_tree([mkrow("S001","https://example.test/a","20")], t)
print(" _qual len:", len(gr87._qualifying_203(b)), "count:", gr87.count_203_rows(b))
shutil.rmtree(t)
