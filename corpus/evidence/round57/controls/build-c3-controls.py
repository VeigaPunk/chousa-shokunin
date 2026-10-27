#!/usr/bin/env python3
"""Build the R57-C3 do-nothing controls as fixture roots under OUT for `c3-count.py --root`:
HELD — an entry chained only through rows the lane already holds (S127's clause, S118, S130), every quote
real and built by `tools/build-spans.py` from the lane-owned captures, every other reference "swept";
CITER — HELD plus a new row S990 opened today on the explanatory note's capture (S128's URL), the
document that cites the references, with quotes of their titles.
Usage: python3 build-c3-controls.py OUT   (reads the lane's corpus/captures and refetch.tsv)"""
import hashlib
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[3]
OUT = pathlib.Path(sys.argv[1])
ENTRY = "corpus/knowledge/normative-reference-chain-china-r57.md"
STORE = LANE / "corpus" / "captures"
U = {
    "S127": "https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf",
    "S118": "https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf",
    "S130": "https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf",
    "S990": "https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf",
}
Q = {
    "S127": ["下列文件中的内容通过文中的规范性引用而构成本文件必不可少的条款。其中，注日期"],
    "S118": ["药品临床综合评价质量控制指南", "（2024 年版 试行）"],
    "S130": ["药品临床综合评价管理指南", "二〇二〇年十一月"],
    "S990": ["关于开展药品使用监测和临床综合评价工作的通知", "抗肿瘤药品临床综合评价技术指南"],
}


def key(u):
    return hashlib.sha256(u.encode()).hexdigest()[:24]


def once(form, q):
    return form.count(q) == 1


for name, ids in (("HELD", ["S127", "S118", "S130"]), ("CITER", ["S127", "S118", "S130", "S990"])):
    r = OUT / name
    (r / "corpus" / "captures").mkdir(parents=True)
    (r / "corpus" / "evidence" / "round57" / "c3").mkdir(parents=True)
    (r / "corpus" / "lessons").mkdir(parents=True)
    (r / "corpus" / "knowledge").mkdir(parents=True)
    shutil.copytree(LANE / "tools", r / "tools", ignore=shutil.ignore_patterns("__pycache__"))
    rec = (LANE / "corpus" / "evidence" / "round57" / "refetch.tsv").read_text(encoding="utf-8").splitlines()
    out_rec = [rec[0]]
    quotes = ["id\turl\tquote\tentry"]
    for sid in ids:
        k = key(U[sid])
        for ext in (".raw", ".txt"):
            if (STORE / f"{k}{ext}").is_file():
                shutil.copyfile(STORE / f"{k}{ext}", r / "corpus" / "captures" / f"{k}{ext}")
        src_id = "S128" if sid == "S990" else sid
        for line in rec[1:]:
            c = line.split("\t")
            if c[0] == src_id and c[1] == U[sid]:
                c[0] = sid
                out_rec.append("\t".join(c))
        form = (STORE / f"{k}.txt").read_text(encoding="utf-8")
        for q in Q[sid]:
            hit = [l.strip() for l in form.splitlines() if q in l]
            qq = q if once(form, q) else None
            if qq is None:
                for l in hit:
                    if once(form, l.strip()) and len(l.strip()) <= 60:
                        qq = l.strip()
                        break
            if qq:
                quotes.append(f"{sid}\t{U[sid]}\t{qq}\t{ENTRY}")
    (r / "corpus" / "evidence" / "round57" / "refetch.tsv").write_text("\n".join(out_rec) + "\n", encoding="utf-8")
    qf = r / "q.tsv"
    qf.write_text("\n".join(quotes) + "\n", encoding="utf-8")
    p = subprocess.run([sys.executable, str(LANE / "tools" / "build-spans.py"), "--quotes", str(qf), "--out",
                        str(r / "corpus" / "evidence" / "round57" / "c3"), "--cache", str(r / "corpus" / "captures")],
                       capture_output=True, text=True)
    lines = [l.split("\t")[5] for l in (r / "corpus/evidence/round57/c3/spans.tsv").read_text(encoding="utf-8").splitlines()[1:]] if p.returncode == 0 else []
    src = (LANE / "corpus" / "SOURCES.md").read_text(encoding="utf-8").splitlines()
    new = []
    for line in src:
        m = re.match(r"^ {0,3}\|\s*(S\d+)\s*\|", line)
        if m and m.group(1) in ids:
            line = line.rstrip()[:-1].rstrip() + f", {ENTRY} |"
        new.append(line)
    if "S990" in ids:
        new.append(f"| S990 | 编制说明 — {U['S990']} | docs | B | control | char 0 | control | mined | 2026-10-27 | 180d | {ENTRY} |")
    (r / "corpus" / "SOURCES.md").write_text("\n".join(new) + "\n", encoding="utf-8")
    body = [f"# control {name}", ""] + [f"source: {i} — {U[i]}" for i in ids] + ["", "规范性引用文件", "",
            "#### Observation", ""] + [f"- `{q}`" for q in lines] + [""] + \
        [f"- UNBOUND R{k} sweep: control searched nothing, hosts none" for k in range(1, 8)]
    (r / ENTRY).write_text("\n".join(body) + "\n", encoding="utf-8")
    (r / "corpus" / "lessons" / "round-57.md").write_text("\n".join(f"- `{q}`" for q in lines) + "\n", encoding="utf-8")
    print(name, "build-spans rc", p.returncode, p.stderr.strip()[:200])
