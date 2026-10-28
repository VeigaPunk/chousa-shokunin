#!/usr/bin/env python3
"""R62-C2 frozen counter — the sourced entry on kernel-enforced path resolution (openat2).

Predicate R62-C2 (the same sentence as corpus/evidence/round62/claims.md): in the lane tree ROOT
(default this lane) the file `corpus/knowledge/openat2-resolve-r62.md` exists and

  TRIO     its first 12 lines carry `source:`, `verified-at:` and `recheck:`, and the `source:` line
           names S138, S139 and S140;
  ROWS     the registry rows S138, S139, S140 each have 11 cells, tier A (S138, S139) or B (S140),
           status `mined`, `opened` on or after 2026-10-28, a `used-by` naming the entry's
           repo-relative path, and a `source` cell that resolves to local text — S138 to
           `/usr/share/man/man2/openat2.2.gz` (rendered `MANWIDTH=1000 man -l FILE | col -bx`), S139 to
           `/usr/include/linux/openat2.h`, S140 to a lane file `corpus/evidence/round62/openat2-probe.txt`
           that exists;
  QUOTES   the entry's `## Located quotes` section holds lines `- Q<n> | S<id> | <quote> | <anchor>`;
           every quote has 4 to 25 words, occurs in the whitespace-normalised text its row resolves
           to, and its anchor text occurs in that row's `anchor` cell; at least 3 quotes are bound to
           S138, 1 to S139 and 2 to S140;
  CLAIMS   the `## Claims` section holds at least 5 lines `Claim <n>. <text> [Q<a>, Q<b>]`; every cited
           Q exists, every Q is cited by some claim, and each claim shares at least 2 distinct words
           of 5 or more letters with the quotes it cites;
  ECHO     in every claim at least 3 words of 5 or more letters, and at least 30 % of such words, occur in
           none of the quotes it cites (a claim that only repeats its quote fails);
  LIMITS   the `## Limits` section holds at least 3 bullet lines, at least one starting `- [INFERENCE]`;
  PROBE    `python3 corpus/evidence/round62/openat2-probe.py --work <fresh dir>` exits 0 with
           `PROBE_FACTS=k/k`, and its `PROBE` lines equal the committed `openat2-probe.txt` lines;
  MAP      `corpus/README.md` names the entry's repo-relative path;
  CENSUS   `scripts/sources-census.sh validate --file ROOT/corpus/SOURCES.md`, run with ROOT as its working
           directory, exits 0,

counted `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=k/k COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1
CENSUS=1/1 C2=PASS`. The counter is structural plus an echo screen: it proves the located quotes exist where
the rows say, that each claim and quote reference resolves, that no claim only repeats its quote and that the
probe the entry rests on still runs; it does not judge that a claim follows from its quotes (named limit —
reviewers judge that).

Usage: python3 corpus/evidence/round62/c2v2-count.py [--root DIR] [--fleet DIR] [--work DIR]
Exit codes: 0 C2=PASS · 1 C2=FAIL · 2 usage/env (no `man`/`col`, no census script).
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[2]
ENTRY_REL = "corpus/knowledge/openat2-resolve-r62.md"
IDS = ("S138", "S139", "S140")
TIER = {"S138": "A", "S139": "A", "S140": "B"}
MAN = {"S138": "/usr/share/man/man2/openat2.2.gz"}
FILE = {"S139": "/usr/include/linux/openat2.h"}
OWN = {"S140": "corpus/evidence/round62/openat2-probe.txt"}
MIN_QUOTES = {"S138": 3, "S139": 1, "S140": 2}
MIN_OPENED = "2026-10-28"
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def registry(root: pathlib.Path) -> dict[str, list[str]]:
    rows = {}
    f = root / "corpus" / "SOURCES.md"
    if not f.is_file():
        return rows
    for line in f.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if m:
            cells = line.split("|")
            if len(cells) == 13:
                rows[m.group(1)] = [c.strip() for c in cells[1:12]]
    return rows


def render_man(path: str) -> str | None:
    env = dict(os.environ, MANWIDTH="1000", LC_ALL="C.UTF-8")
    try:
        m = subprocess.run(["man", "-l", path], capture_output=True, env=env, timeout=60)
        c = subprocess.run(["col", "-bx"], input=m.stdout, capture_output=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        raise SystemExit("c2v2-count: man or col unavailable")
    if m.returncode != 0 or not c.stdout:
        return None
    return norm(c.stdout.decode("utf-8", errors="replace"))


def resolve(root: pathlib.Path, sid: str, row: list[str]) -> str | None:
    src = row[1]
    if sid in MAN:
        return render_man(MAN[sid]) if MAN[sid] in src and os.path.exists(MAN[sid]) else None
    if sid in FILE:
        p = pathlib.Path(FILE[sid])
        return norm(p.read_text(encoding="utf-8", errors="replace")) if FILE[sid] in src and p.is_file() else None
    p = root / OWN[sid]
    return norm(p.read_text(encoding="utf-8", errors="replace")) if OWN[sid] in src and p.is_file() else None


def section(text: str, heading: str) -> list[str]:
    out, on = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            on = line.strip() == heading
            continue
        if on:
            out.append(line)
    return out


def words(s: str) -> set[str]:
    return {w.lower() for w in re.findall(r"[A-Za-z]{5,}", s)}


def probe_lines(text: str) -> list[str]:
    return [l.rstrip() for l in text.splitlines() if l.startswith("PROBE ") or l.startswith("PROBE_FACTS=") or l.startswith("HEADER ")]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE))
    ap.add_argument("--fleet", default=str(LANE.parent))
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    root, fleet = pathlib.Path(a.root), pathlib.Path(a.fleet)
    census = fleet / "scripts" / "sources-census.sh"
    if not census.is_file():
        print(f"c2v2-count: no census script {census}", file=sys.stderr)
        return 2
    entry = root / ENTRY_REL
    res: dict[str, str] = {}
    detail: list[str] = []
    ok_entry = entry.is_file()
    text = entry.read_text(encoding="utf-8") if ok_entry else ""
    res["ENTRY"] = f"{int(ok_entry)}/1"
    head = "\n".join(text.splitlines()[:12])
    src_line = next((l for l in head.splitlines() if l.startswith("source:")), "")
    trio = ok_entry and all(re.search(rf"^{k}:", head, re.M) for k in ("source", "verified-at", "recheck")) \
        and all(i in src_line for i in IDS)
    res["TRIO"] = f"{int(bool(trio))}/1"
    rows = registry(root)
    good = 0
    texts: dict[str, str | None] = {}
    for sid in IDS:
        r = rows.get(sid)
        if not r:
            detail.append(f"ROW {sid} absent")
            continue
        tier_ok = r[3] == TIER[sid]
        texts[sid] = resolve(root, sid, r)
        used = ENTRY_REL in [u.strip() for u in re.split(r"[,;]", r[10])]
        ok = tier_ok and r[7] == "mined" and r[8] >= MIN_OPENED and re.match(r"^\d{4}-\d{2}-\d{2}$", r[8]) \
            and used and texts[sid] is not None
        if not ok:
            detail.append(f"ROW {sid} tier={r[3]} status={r[7]} opened={r[8]} used_by_entry={used} resolves={texts[sid] is not None}")
        good += bool(ok)
    res["ROWS"] = f"{good}/3"
    qlines = [l for l in section(text, "## Located quotes") if l.startswith("- Q")]
    quotes: dict[str, tuple[str, str]] = {}
    qok = 0
    per_row = {i: 0 for i in IDS}
    for l in qlines:
        cells = [c.strip() for c in l[2:].split(" | ")]
        if len(cells) != 4 or not re.match(r"^Q\d+$", cells[0]) or cells[1] not in IDS:
            detail.append(f"QUOTE malformed: {l[:60]}")
            continue
        qid, sid, quote, anchor = cells
        n = len(quote.split())
        found = texts.get(sid) is not None and norm(quote) in texts[sid]
        anch = anchor != "" and rows.get(sid) is not None and anchor in rows[sid][5] and anchor in (texts[sid] or "")
        if 4 <= n <= 25 and found and anch and qid not in quotes:
            quotes[qid] = (sid, quote)
            per_row[sid] += 1
            qok += 1
        else:
            detail.append(f"QUOTE {qid} {sid} words={n} found={found} anchor_ok={anch}")
    res["QUOTES"] = f"{qok}/{len(qlines)}" if qlines else "0/0"
    cov = all(per_row[i] >= MIN_QUOTES[i] for i in IDS) and qok == len(qlines) > 0
    res["COVERAGE"] = f"{int(cov)}/1"
    claims = [l for l in section(text, "## Claims") if re.match(r"^Claim \d+\.", l)]
    cited, claims_ok, echo_ok = set(), len(claims) >= 5, len(claims) >= 5
    for l in claims:
        m = re.match(r"^Claim \d+\.\s+(.*)\s\[((?:Q\d+(?:,\s*)?)+)\]\s*$", l)
        if not m:
            claims_ok = echo_ok = False
            detail.append(f"CLAIM malformed: {l[:60]}")
            continue
        qs = [q.strip() for q in m.group(2).split(",")]
        if any(q not in quotes for q in qs):
            claims_ok = echo_ok = False
            detail.append(f"CLAIM cites unknown quote: {l[:60]}")
            continue
        cited.update(qs)
        qwords = set().union(*(words(quotes[q][1]) for q in qs))
        cw = words(m.group(1))
        shared = cw & qwords
        if len(shared) < 2:
            claims_ok = False
            detail.append(f"CLAIM shares {len(shared)} words with its quotes: {l[:60]}")
        fresh = cw - qwords
        if len(fresh) < 3 or len(fresh) < 0.3 * len(cw):
            echo_ok = False
            detail.append(f"ECHO claim has {len(fresh)} of {len(cw)} words outside its quotes: {l[:60]}")
    claims_ok = claims_ok and bool(quotes) and cited == set(quotes)
    res["CLAIMS"] = f"{int(claims_ok)}/1"
    res["ECHO"] = f"{int(echo_ok)}/1"
    limits = [l for l in section(text, "## Limits") if l.lstrip().startswith("- ")]
    res["LIMITS"] = f"{int(len(limits) >= 3 and any(l.lstrip().startswith('- [INFERENCE]') for l in limits))}/1"
    # PROBE: live run of the probe against the committed output
    probe_ok = False
    committed = root / OWN["S140"]
    script = root / "corpus" / "evidence" / "round62" / "openat2-probe.py"
    if committed.is_file() and script.is_file():
        tmp = pathlib.Path(a.work) if a.work else pathlib.Path(tempfile.mkdtemp(prefix="c2v2-"))
        try:
            p = subprocess.run([sys.executable, "-B", str(script), "--work", str(tmp / "probe")],
                               capture_output=True, text=True, timeout=120, stdin=subprocess.DEVNULL)
            m = re.search(r"PROBE_FACTS=(\d+)/(\d+)", p.stdout)
            same = probe_lines(p.stdout) == probe_lines(committed.read_text(encoding="utf-8"))
            probe_ok = p.returncode == 0 and bool(m) and m.group(1) == m.group(2) and same
            if not probe_ok:
                detail.append(f"PROBE exit={p.returncode} facts={m.group(0) if m else None} same_as_committed={same}")
        except (OSError, subprocess.TimeoutExpired) as e:
            detail.append(f"PROBE could not run: {e}")
        finally:
            if not a.work:
                shutil.rmtree(tmp, ignore_errors=True)
    else:
        detail.append("PROBE script or committed output absent")
    res["PROBE"] = f"{int(probe_ok)}/1"
    readme = root / "corpus" / "README.md"
    res["MAP"] = f"{int(readme.is_file() and ENTRY_REL in readme.read_text(encoding='utf-8'))}/1"
    c = subprocess.run(["bash", str(census), "validate", "--file", str(root / "corpus" / "SOURCES.md")],
                       capture_output=True, text=True, cwd=root)
    res["CENSUS"] = f"{int(c.returncode == 0)}/1"
    passed = all(v.split("/")[0] == v.split("/")[1] and v != "0/0" for v in res.values())
    print(" ".join(f"{k}={v}" for k, v in res.items()) + f" C2={'PASS' if passed else 'FAIL'}")
    for d in detail:
        print("  " + d)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
