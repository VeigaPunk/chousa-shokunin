#!/usr/bin/env python3
"""Independent hand-built mutation battery for tools/gate-records.py (R83ExecRepro).

Built from the claims text + docstring only; each case is one file with one in-class line.
Prints CASE <name> expected=<CODE> -> observed=<codes|OK> rc=<n>.
"""
import hashlib
import os
import re
import subprocess
import sys

TREE = sys.argv[1]
REPO = sys.argv[2]
WORK = sys.argv[3]
TOOL = os.path.join(TREE, "tools/gate-records.py")
os.makedirs(WORK, exist_ok=True)

lesson = open(os.path.join(TREE, "corpus/lessons/round-83.md"), encoding="utf-8").read().split("\n")
adm = [l for l in lesson if l.startswith("GATE-RECORD")][0]
r80 = open(os.path.join(TREE, "corpus/lessons/round-80.md"), encoding="utf-8").read().split("\n")
rev = [l for l in r80 if l.startswith("GATE-RECORD")][0]


def kv_set(line, key, val):
    return re.sub(r"(?<= )" + re.escape(key) + r"=\S+", key + r"=" + val, line, count=1)


def kv_get(line, key):
    m = re.search(r"(?<= )" + re.escape(key) + r"=(\S+)", line)
    return m.group(1) if m else None


def quote_of(line):
    return line.split(" quote=", 1)[1]


def with_quote(line, q, quoted=True):
    head = line.split(" quote=", 1)[0]
    return head + " quote=" + ('"' + q + '"' if quoted else q)


q = quote_of(adm)[1:-1]
words = q.split()
cs = kv_get(adm, "capture_sha256")
ts = kv_get(adm, "fetched")
sec = int(ts[17:19])
capfiles = sorted(f for f in os.listdir(os.path.join(TREE, "corpus/captures"))
                  if f.endswith(".txt") and f != os.path.basename(kv_get(adm, "capture")))
other_cap = "corpus/captures/" + capfiles[0] if capfiles else None

cases = [
    # name, expected code (or None for OK), line
    ("R0-genuine-admit", None, adm),
    ("R0b-genuine-rev", None, rev),
    # a changed URL keeps the S-id in the registry, so REGISTRY must NOT fire; the key and refetch checks do
    ("R1-url-changed", "CAPTURE_KEY", kv_set(adm, "url", kv_get(adm, "url") + "x")),
    ("R2-tier", "TIER", kv_set(kv_set(adm, "tier", "B"), "url", kv_get(adm, "url"))),
    ("R3-capture-path-traversal", "CAPTURE_PATH", kv_set(adm, "capture", "corpus/captures/../SOURCES.md")),
    ("R4-capture-key-other-file", "CAPTURE_KEY", kv_set(adm, "capture", other_cap) if other_cap else adm),
    ("R5-capture-sha-flip", "CAPTURE_SHA", kv_set(adm, "capture_sha256", ("0" if cs[0] != "0" else "1") + cs[1:])),
    ("R6-refetch-fetched", "REFETCH", kv_set(adm, "fetched", ts[:17] + "%02d" % ((sec + 1) % 60) + "Z")),
    ("R7-words", "WORDS", kv_set(adm, "words", str(len(words) + 1))),
    ("R8-quote-len", "QUOTE_LEN", kv_set(with_quote(adm, " ".join(["one"] * 26)), "words", "26")),
    ("R9-quote-absent", "QUOTE_ABSENT", with_quote(adm, " ".join(["Zyzzyva"] + words[1:]))),
    ("R10-parse-unknown-key", "PARSE", adm.replace(" tier=", " bogus=1 tier=", 1)),
    ("R11-rev-bogus-commit", "REV", kv_set(rev, "rev", "0" * 40)),
    ("R12-line-off", "LINE", kv_set(rev, "line", str(int(kv_get(rev, "line")) + 1))),
    ("R13-unknown-sid", "REGISTRY", adm.replace("GATE-RECORD S009", "GATE-RECORD S999", 1)),
    # class edges
    ("C1-BOM-prefixed-genuine", None, "\ufeff" + adm),
    ("C2-ZWSP-prefixed-forged", "QUOTE_ABSENT", "\u200b" + with_quote(adm, " ".join(["Zyzzyva"] + words[1:]))),
    ("C3-tab-separated", "PARSE", adm.replace("GATE-RECORD ", "GATE-RECORD\t", 1)),
    ("C4-bare-token", "PARSE", "GATE-RECORD"),
]

files = []
for name, exp, line in cases:
    p = os.path.join(WORK, name + ".md")
    open(p, "w", encoding="utf-8").write("# " + name + "\n\n" + line + "\n")
    files.append((name, exp, p))

# out-of-class prose file: four mention forms, no in-class line
prose = os.path.join(WORK, "P-prose.md")
open(prose, "w", encoding="utf-8").write(
    "# prose\n\n"
    "Inline `GATE-RECORD S009 url=x` mention.\n"
    "- GATE-RECORD S009 url=x list item\n"
    "> GATE-RECORD S009 url=x blockquote\n"
    "<!-- GATE-RECORD S009 url=x html comment -->\n"
    "Prose word GATE-RECORDS is not a record either.\n")

p = subprocess.run([sys.executable, "-B", TOOL, "verify", "--root", TREE, "--repo", REPO]
                   + [f[2] for f in files] + [prose], capture_output=True, text=True)
obs = {}
for ln in p.stdout.split("\n"):
    m = re.match(r"^GATE_RECORD (.+):(\d+) (S\d+|\?) (OK|FAIL) ?(.*)$", ln)
    if m:
        obs[os.path.basename(m.group(1))] = m.group(4) + (":" + m.group(5) if m.group(5) else "")
bad = 0
for name, exp, path in files:
    got = obs.get(os.path.basename(path), "MISSING")
    codes = got.split(":", 1)[1].split(",") if got.startswith("FAIL") else []
    okk = (exp is None and got == "OK") or (exp is not None and exp in codes)
    bad += 0 if okk else 1
    print(f"CASE {name} expected={exp or 'OK'} -> observed={got} match={'yes' if okk else 'NO'}")
print("PROSE file observed:", obs.get(os.path.basename(prose), "MISSING"), "(MISSING = no in-class record, as the class requires)")
print("SUMMARY lines:", p.stdout.strip().split("\n")[-1])
print(f"tool rc={p.returncode} cases={len(files)} mismatched={bad}")
sys.exit(1 if bad else 0)
