#!/usr/bin/env python3
"""K2 live re-open check: committed captures vs live GETs, quote presence both sides."""
import hashlib, html, os, re, subprocess, sys

ROOT = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r82/R82ExecReopen"
REV = "b4a41d251b488f06b4a6ab01a11bc12ce72edd20"
ENTRY = "corpus/knowledge/question-framing-frames-r82.md"
R81 = "corpus/knowledge/correction-retraction-status-r81.md"
SOURCES = "corpus/SOURCES.md"
REFETCH = "corpus/evidence/round57/refetch.tsv"

def git_bytes(path):
    return subprocess.run(["git", "-C", ROOT, "show", f"{REV}:{path}"],
                          capture_output=True, check=True).stdout

def html_to_text(s):
    s = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?s)<!--.*?-->", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>|</tr>|</h[1-6]>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    return s

def recipe_txt(raw):
    txt = raw.decode("utf-8", "replace")
    if re.search(r"(?is)^\s*(?:<!doctype\s+html|<html[\s>]|<head[\s>]|<body[\s>])", txt[:4000]):
        txt = html_to_text(txt)
    return txt

FOLD = {"\u2018":"'","\u2019":"'","\u201a":"'","\u201b":"'","\u201c":'"',"\u201d":'"',
        "\u201e":'"',"\u201f":'"',"\u2032":"'","\u2033":'"',"\u00a0":" ",
        "\u2010":"-","\u2011":"-","\u2012":"-","\u2013":"-","\u2014":"-"}

def norm(s):
    s = "".join(FOLD.get(c, c) for c in s)
    return re.sub(r"\s+", " ", s).strip()

# quotes
entry = git_show_txt = git_bytes(ENTRY).decode()
rows, inq = [], False
for line in entry.splitlines():
    if line.startswith("## "):
        inq = line.strip() == "## Located quotes"; continue
    if inq:
        m = re.match(r"^\| *(Q\d+) *\| *(S\d+) *\| *\"(.*)\" *\|$", line)
        if m: rows.append((m.group(1), m.group(2), m.group(3)))
r81 = git_bytes(R81).decode()
s028 = []
for line in r81.splitlines():
    m = re.match(r"^> *\"(.*)\" *\u2014 *S028 *$", line.strip())
    if m: s028.append(("S028-q%d" % (len(s028)+1), "S028", m.group(1)))
items = rows + s028

sources = git_bytes(SOURCES).decode()
urls = {}
for line in sources.splitlines():
    if not line.startswith("|"): continue
    c = [x.strip() for x in line.strip().strip("|").split("|")]
    if len(c) < 2 or not re.match(r"^S\d+$", c[0]): continue
    m = re.search(r"(https?://\S+?)(?: \||$)", c[1])
    if m: urls[c[0]] = m.group(1)

with open(os.path.join(ROOT, REFETCH), encoding="utf-8") as fh:
    hdr = fh.readline().rstrip("\n").split("\t")
    recs = [dict(zip(hdr, l.rstrip("\n").split("\t"))) for l in fh if l.strip()]
def last_row(sid, url):
    hits = [r for r in recs if r["id"] == sid and r["url"] == url]
    return hits[-1] if hits else None

print("== capture integrity: is committed .txt reproducible from committed .raw? ==")
by_src = {}
for qid, sid, q in items:
    by_src.setdefault(sid, []).append((qid, q))
live = {}
fails = []
for sid in by_src:
    url = urls[sid]
    key = hashlib.sha256(url.encode()).hexdigest()[:24]
    raw = git_bytes(f"corpus/captures/{key}.raw")
    txtb = git_bytes(f"corpus/captures/{key}.txt")
    rr = last_row(sid, url)
    re_derived = recipe_txt(raw).encode("utf-8", "replace")
    same = hashlib.sha256(re_derived).hexdigest() == hashlib.sha256(txtb).hexdigest()
    live_path = os.path.join(SCRATCH, "live", f"{sid}.raw")
    lraw = open(live_path, "rb").read() if os.path.exists(live_path) else b""
    lsha = hashlib.sha256(lraw).hexdigest() if lraw else "-"
    print(f"{sid}\tkey={key}\trefetch={rr['fetched_utc']}\tcommitted_raw_sha={hashlib.sha256(raw).hexdigest()[:16]}"
          f"\ttxt_reproduced_from_raw={same}\tlive_sha={lsha[:16]}\tlive_bytes={len(lraw)}"
          f"\tlive_raw_matches_committed={'YES' if lsha == hashlib.sha256(raw).hexdigest() else 'NO'}")
    live[sid] = norm(recipe_txt(lraw)) if lraw else ""
    by_src[sid] = (by_src[sid], norm(txtb.decode("utf-8", "replace")), rr, url, key)

print()
print("== per-quote: committed capture vs live ==")
print("qid\tsource\twords\tin_committed_capture\tin_live\tverdict")
for sid, (qlist, capnorm, rr, url, key) in by_src.items():
    for qid, q in qlist:
        n = norm(q)
        inc = n in capnorm
        inl = n in live[sid]
        v = "LIVE_VERBATIM" if (inc and inl) else ("DRIFT_LIVE_ABSENT" if inc and not inl else
            ("MISSING_FROM_CAPTURE" if not inc else "?"))
        if not inc: fails.append((qid, "absent_from_committed_capture"))
        print(f"{qid}\t{sid}\t{len(q.split())}\t{inc}\t{inl}\t{v}")
        if not (8 <= len(q.split()) <= 25):
            fails.append((qid, "word_count_%d_out_of_8_25" % len(q.split())))

print()
print("K2_LIVE fails=%d %s" % (len(fails), fails if fails else ""))
sys.exit(0 if not fails else 1)
