#!/usr/bin/env python3
"""K2 local re-derivation: committed bytes only. No network."""
import hashlib, os, re, subprocess, sys

ROOT = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
REV = "b4a41d251b488f06b4a6ab01a11bc12ce72edd20"
ENTRY = "corpus/knowledge/question-framing-frames-r82.md"
R81 = "corpus/knowledge/correction-retraction-status-r81.md"
SOURCES = "corpus/SOURCES.md"
REFETCH = "corpus/evidence/round57/refetch.tsv"

def git_show(path):
    return subprocess.run(["git", "-C", ROOT, "show", f"{REV}:{path}"],
                          capture_output=True, text=True, check=True).stdout

def git_bytes(path):
    return subprocess.run(["git", "-C", ROOT, "show", f"{REV}:{path}"],
                          capture_output=True, check=True).stdout

def norm(s):
    """whitespace collapse + curly-quote folding (both directions)."""
    table = {
        "\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'",
        "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u201f": '"',
        "\u2032": "'", "\u2033": '"',
        "\u2010": "-", "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2014": "-",
        "\u00a0": " ", "\u2007": " ", "\u2009": " ", "\u202f": " ",
    }
    s = "".join(table.get(ch, ch) for ch in s)
    return re.sub(r"\s+", " ", s).strip()

# ---- parse the 11 located quotes out of the committed entry ----
entry = git_show(ENTRY)
rows = []
in_quotes = False
for line in entry.splitlines():
    if line.startswith("## "):
        in_quotes = line.strip() == "## Located quotes"
        continue
    if not in_quotes:
        continue
    m = re.match(r"^\| *(Q\d+) *\| *(S\d+) *\| *\"(.*)\" *\|$", line)
    if m:
        rows.append((m.group(1), m.group(2), m.group(3)))

# ---- parse S028 quote lines from the r81 addendum ----
r81 = git_show(R81)
s028 = []
for line in r81.splitlines():
    m = re.match(r"^> *\"(.*)\" *\u2014 *S028 *$", line.strip())
    if m:
        s028.append(("S028-quote%d" % (len(s028) + 1), "S028", m.group(1)))

# ---- registry URLs ----
sources = git_show(SOURCES)
urls = {}
for line in sources.splitlines():
    if not line.startswith("|"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 2:
        continue
    m = re.match(r"^S\d+$", cells[0])
    if not m:
        continue
    idm = re.search(r"(https?://\S+?)(?: \||$)", cells[1])
    if idm:
        urls[cells[0]] = idm.group(1)

# ---- refetch rows: last successful row per id/url ----
with open(os.path.join(ROOT, REFETCH), encoding="utf-8") as fh:
    hdr = fh.readline().rstrip("\n").split("\t")
    recs = [dict(zip(hdr, l.rstrip("\n").split("\t"))) for l in fh if l.strip()]

def last_row(sid, url):
    hits = [r for r in recs if r["id"] == sid and r["url"] == url]
    if not hits:
        return None
    return hits[-1]

print("ENTRY_QUOTES=%d S028_QUOTES=%d" % (len(rows), len(s028)))
print()

def check(qid, sid, quote):
    url = urls.get(sid)
    if not url:
        print(f"{qid}\t{sid}\tNO_REGISTRY_ROW")
        return "NO_REGISTRY_ROW"
    key = hashlib.sha256(url.encode()).hexdigest()[:24]
    rr = last_row(sid, url)
    out = [f"{qid}", sid, key, f"words={len(quote.split())}"]
    if rr is None:
        out.append("NO_REFETCH_ROW")
        print("\t".join(out)); return "NO_REFETCH_ROW"
    out.append(f"refetch_utc={rr['fetched_utc']} attempt={rr['attempt']} rc={rr['curl_rc']} http={rr['http_code']}")
    # capture hashes from committed bytes at landing rev
    problems = []
    for ext, col in (("raw", "raw_sha256"), ("txt", "txt_sha256")):
        p = f"corpus/captures/{key}.{ext}"
        try:
            b = git_bytes(p)
        except subprocess.CalledProcessError:
            out.append(f"{ext}=MISSING"); problems.append("capture_missing_" + ext); continue
        h = hashlib.sha256(b).hexdigest()
        want = rr[col]
        ok = (h == want)
        out.append(f"{ext}_sha={h[:16]}… refetch={want[:16]}… {'OK' if ok else 'MISMATCH'}")
        if not ok:
            problems.append("capture_mismatch_" + ext)
    # quote presence in committed capture txt and raw
    present = {}
    for ext in ("txt", "raw"):
        p = f"corpus/captures/{key}.{ext}"
        try:
            b = git_bytes(p).decode("utf-8", "replace")
        except subprocess.CalledProcessError:
            present[ext] = None; continue
        present[ext] = norm(quote) in norm(b)
    out.append("in_txt=%s" % present["txt"])
    out.append("in_raw=%s" % present["raw"])
    if present["txt"] is not True:
        problems.append("quote_absent_from_capture")
    status = "PASS" if not problems else "FAIL:" + ",".join(problems)
    out.append(status)
    print("\t".join(out))
    return status

results = []
print("== entry located quotes ==")
for qid, sid, q in rows:
    results.append(check(qid, sid, q))
print()
print("== S028 addendum quotes (r81 file, round-82 addendum) ==")
for qid, sid, q in s028:
    results.append(check(qid, sid, q))

print()
bad = [r for r in results if r != "PASS"]
print("K2_LOCAL quotes=%d pass=%d fail=%d" % (len(results), len(results) - len(bad), len(bad)))
sys.exit(0 if not bad else 1)
