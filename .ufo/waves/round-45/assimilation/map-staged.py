#!/usr/bin/env python3
"""map-staged.py — round-45 scratch map of the staged chousa package (read-only).

For every staged row in merge/chousa/SOURCES.append.md: the URL its source cell
names, the campaign capture cache key (sha256(url)[:24]), whether a .txt capture
is on disk and its size, whether the URL sits in the lane's r42 quarantine slice
(and that row's r42 verdict), and which staged knowledge entries cite the row.
Output TSV to stdout. Reads only; writes nothing in /home/vgpnk/Projects/shokuknow.
"""
import hashlib
import pathlib
import re
import subprocess
import sys

S = pathlib.Path("/home/vgpnk/Projects/shokuknow")
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
APPEND = S / "merge/chousa/SOURCES.append.md"
KNOW = S / "merge/chousa/knowledge/corpus/knowledge"
CACHE = S / ".ufo/waves/corpus-expansion-1/.qcache"
ROW = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
URL = re.compile(r"https?://[^\s|)>\]`*]+")


def cites():
    out = {}
    for p in sorted(KNOW.glob("*.md")):
        for sid in sorted(set(re.findall(r"\bS\d{3}\b", p.read_text(encoding="utf-8")))):
            out.setdefault(sid, []).append(p.name)
    return out


def quarantine():
    res = subprocess.run([sys.executable, str(LANE / "tools/quarantine-check.py"), "slice"],
                         capture_output=True, text=True, check=True)
    urls = {}
    for line in res.stdout.splitlines():
        f = line.split("\t")
        if len(f) >= 4 and f[3].startswith("http"):
            urls[f[3]] = f[0]
    verdicts = {}
    for line in (LANE / "corpus/evidence/round42/quarantine-verdicts.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        f = line.split("\t")
        verdicts[f[0]] = f[1]
    return urls, verdicts


def main():
    cite = cites()
    qurls, qv = quarantine()
    print("staged\turl\tkey\tcapture_chars\tquarantine_reg_id\tr42_verdict\tcited_by")
    for line in APPEND.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if not m:
            continue
        sid = m.group(1)
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        u = URL.search(cells[1]) or URL.search(cells[5] if len(cells) > 5 else "")
        url = u.group(0).rstrip(".,;") if u else ""
        key = hashlib.sha256(url.encode()).hexdigest()[:24] if url else ""
        txt = CACHE / f"{key}.txt"
        size = len(txt.read_text(encoding="utf-8", errors="replace")) if url and txt.exists() else 0
        reg = qurls.get(url, "")
        print("\t".join([sid, url, key, str(size), reg, qv.get(reg, ""), ",".join(cite.get(sid, []))]))


if __name__ == "__main__":
    main()
