#!/usr/bin/env python3
"""entry-controls-r100 — round-100 C2 (freshness) controls for `corpus/knowledge/quotation-error-update-r100.md`.

Recomputes what the entry says it holds from files under --root as they are on disk (the entry, the round-99 entry it
updates, captures `b5eec205612ee5f138cf065d` (S238) and `405a0054e1f6dbd1854a3618` (S236)) plus `git ls-tree`/`git show`
at BASE for the do-nothing leg; no network, no write. Legs:

  QUOTES      every `## Located quotes` row: its quote, normalized as `tools/gate-records.py` normalizes, occurs in its
              own source's capture, and has 1-25 words
  FIELD       each JSON capture parsed: U0 equals S238's `title` (normalized); every other S238 or S236 quote lies inside
              its own record's `abstractText`
  IDENTITY    S238 is Baethge & Jergas 2025: `hitCount` 1, `pmid` 40696441, `pmcid` PMC12285159, `doi`
              10.1186/s41073-025-00173-z, `pubYear` 2025, journal volume 10; S236 is Jergas & Baethge 2015 (`pmid`
              26528420, `doi` 10.7717/peerj.1364, `pubYear` 2015)
  WARRANTS    every `## Decision table` row's Warrant names only qids of the quote table; every Lane cell non-empty
  NUMBERS     every numeric token (`-?[0-9]+([.,][0-9]+)*%?`, sign kept) of every Do AND Never cell is one of the numeric
              tokens of that row's own warrant quotes — token equality, not substring (a dropped minus sign, "20.0%"
              for "-20.0%", or "0.002" for "-0.002" is refused) (printed `NUMBERS_SOURCED=k/n`)
  NEVER       every Never cell is exactly "(none stated by the sources)" or carries at least one numeral checked above
  FRESH       the freshness link both ways: the entry's front matter has `updates: corpus/knowledge/quotation-error-rates-r99.md`,
              that file exists, and it has a `## Update` section naming `corpus/knowledge/quotation-error-update-r100.md`
              and S238
  TOPIC       no `corpus/knowledge/*.md` blob at BASE contains "46 studies" or "16.9%", and this entry contains both
  BASE        the do-nothing control: the entry path is absent at BASE and the BASE round-99 entry has no `## Update`
              section (`BASE_ENTRY=absent BASE_UPDATE_LINK=0`)
  FORGERY     thirteen in-memory forgeries the legs above must refuse: f1 U7's "16.9%" made "19.6%" in the quote table; f2
              a Do cell's "16.9%" made "19.6%"; f3 U7 attributed to S236; f4 U0 replaced by an abstract sentence (FIELD);
              f5 a warrant naming U99; f6 a Do number moved to a row whose warrants do not print it ("-0.253" into the
              first row); f7 U4 widened past 25 words with the capture text before it (U3 + U4); f8 the S238 record with `pmid` changed; f9 a
              Lane cell emptied; f10 the round-99 entry's `## Update` section removed; f11 the slope's sign dropped in
              a Do cell ("-0.002" -> "0.002"); f12 a Never cell "never cite a rate under 30%"; f13 the `updates:` line
              pointing at a missing file
  ACCEPT      two edits that change no claim (a Lane cell reworded, two decision rows swapped) must still PASS

Usage: python3 -B corpus/evidence/round100/entry-controls-r100.py --root LANE
Prints CASE lines, one tally line and `ENTRY_CONTROLS_R100=PASS|FAIL`. Exit 0 PASS, 1 FAIL, 2 setup.
"""
import argparse
import json
import os
import re
import subprocess
import sys

BASE = "929c784c63a1fd17961d21742101b2b109b7b8ff"
ENTRY = "corpus/knowledge/quotation-error-update-r100.md"
OLD = "corpus/knowledge/quotation-error-rates-r99.md"
CAPS = {"S238": "corpus/captures/b5eec205612ee5f138cf065d.txt", "S236": "corpus/captures/405a0054e1f6dbd1854a3618.txt"}
ROW = re.compile(r'^\| ([A-Z][0-9]+) \| (S[0-9]+) \| "(.*)" \|$')
NUM = re.compile(r"-?[0-9]+(?:[.,][0-9]+)*%?")
NONE_STATED = "(none stated by the sources)"


def norm(s):
    s = s.replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    return " ".join(s.split())


def section(text, title):
    out, on = [], False
    for ln in text.split("\n"):
        if ln.startswith("## "):
            on = ln.strip() == f"## {title}"
            continue
        if on:
            out.append(ln)
    return out


def quotes(text):
    return [m.groups() for m in (ROW.match(ln) for ln in section(text, "Located quotes")) if m]


def decisions(text):
    rows = [ln for ln in section(text, "Decision table") if ln.startswith("|")]
    return [[c.strip() for c in r.strip()[1:-1].split(" | ")] for r in rows[2:]]


def record(cap):
    try:
        d = json.loads(cap)
        return d, d["resultList"]["result"][0]
    except (ValueError, KeyError, IndexError, TypeError):
        return None, None


def fresh(text, old_text, root):
    front = text.split("\n## ", 1)[0]
    m = re.search(r"^updates: (\S+)$", front, re.M)
    if not m or m.group(1) != OLD or not os.path.isfile(os.path.join(root, m.group(1))):
        return 0
    upd = "\n".join(section(old_text or "", "Update"))
    return int(ENTRY in upd and "S238" in upd)


def score(text, caps, old_text, root):
    """Return dict leg -> (ok, n) for one entry text, capture texts and round-99 entry text."""
    r = {}
    qs = quotes(text)
    qmap = {q: (s, t) for q, s, t in qs}
    r["QUOTES"] = (sum(1 for q, s, t in qs if s in caps and norm(t) in norm(caps[s]) and 1 <= len(t.split()) <= 25),
                   len(qs))
    recs = {s: record(caps[s]) for s in caps}
    field = n_field = 0
    for q, s, t in qs:
        if s not in recs:
            continue
        n_field += 1
        _, rec = recs[s]
        if rec is None:
            continue
        try:
            if q == "U0":
                field += s == "S238" and norm(t) == norm(rec["title"])
            else:
                field += norm(t) in norm(rec["abstractText"])
        except (KeyError, TypeError):
            pass
    r["FIELD"] = (field, n_field)
    ident = 0
    try:
        d, rec = recs["S238"]
        ident += (d["hitCount"] == 1 and rec["pmid"] == "40696441" and rec["pmcid"] == "PMC12285159"
                  and rec["doi"] == "10.1186/s41073-025-00173-z" and rec["pubYear"] == "2025"
                  and rec["journalInfo"]["volume"] == "10")
    except (KeyError, TypeError):
        pass
    try:
        d, rec = recs["S236"]
        ident += (d["hitCount"] == 1 and rec["pmid"] == "26528420" and rec["doi"] == "10.7717/peerj.1364"
                  and rec["pubYear"] == "2015")
    except (KeyError, TypeError):
        pass
    r["IDENTITY"] = (ident, 2)
    rows = decisions(text)
    wok = nums_ok = nums_n = nev_ok = 0
    for row in rows:
        if len(row) != 5:
            continue
        ids = [w.strip() for w in row[3].split(",")]
        wok += all(i in qmap for i in ids) and bool(row[4])
        wtoks = set(NUM.findall(" ".join(norm(qmap[i][1]) for i in ids if i in qmap)))
        for cell in (row[1], row[2]):
            for n in NUM.findall(cell):
                nums_n += 1
                nums_ok += n in wtoks
        nev_ok += row[2] == NONE_STATED or bool(NUM.findall(row[2]))
    r["WARRANTS"] = (wok, len(rows))
    r["NUMBERS"] = (nums_ok, nums_n)
    r["NEVER"] = (nev_ok, len(rows))
    r["FRESH"] = (fresh(text, old_text, root), 1)
    r["TOPIC"] = (int("46 studies" in text and "16.9%" in text), 1)
    return r


def passes(r):
    return all(k == v and v > 0 for k, v in r.values())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    try:
        text = open(os.path.join(root, ENTRY), encoding="utf-8").read()
        old_text = open(os.path.join(root, OLD), encoding="utf-8").read()
        caps = {s: open(os.path.join(root, p), encoding="utf-8", errors="replace").read() for s, p in CAPS.items()}
    except OSError as e:
        print(f"ENTRY_CONTROLS_SETUP {e}", file=sys.stderr)
        return 2
    r = score(text, caps, old_text, root)
    for k, (ok, n) in r.items():
        print(f"CASE {k} {ok}/{n} {'PASS' if ok == n and n > 0 else 'FAIL'}")
    good = passes(r)
    ls = subprocess.run(["git", "-C", root, "ls-tree", "--name-only", BASE, "corpus/knowledge/"], capture_output=True,
                        text=True)
    if ls.returncode != 0:
        print("ENTRY_CONTROLS_SETUP cannot list BASE", file=sys.stderr)
        return 2
    base_hits = 0
    for p in ls.stdout.split():
        b = subprocess.run(["git", "-C", root, "show", f"{BASE}:{p}"], capture_output=True, text=True)
        base_hits += "46 studies" in b.stdout or "16.9%" in b.stdout
    base_entry = ENTRY in ls.stdout.split()
    bo = subprocess.run(["git", "-C", root, "show", f"{BASE}:{OLD}"], capture_output=True, text=True)
    base_link = int(bo.returncode == 0 and bool("\n".join(section(bo.stdout, "Update")).strip()))
    base_ok = not base_entry and base_hits == 0 and base_link == 0
    print(f"CASE BASE entry={'present' if base_entry else 'absent'} topic_hits={base_hits} update_link={base_link} "
          f"{'PASS' if base_ok else 'FAIL'}")
    good = good and base_ok
    qd = {q: t for q, s, t in quotes(text)}
    rows = decisions(text)
    first_do = rows[0][1]
    slope_do = next(rw[1] for rw in rows if "-0.002" in rw[1])
    _, rec = record(caps["S238"])
    d_bad = json.loads(caps["S238"])
    d_bad["resultList"]["result"][0]["pmid"] = "40696442"
    old_cut = re.sub(r"\n## Update\n.*?(?=\n## |\Z)", "\n", old_text, count=1, flags=re.S)
    forgeries = {
        "f1": (text.replace(f'| U7 | S238 | "{qd["U7"]}" |', f'| U7 | S238 | "{qd["U7"].replace("16.9%", "19.6%", 1)}" |',
                            1), caps, old_text),
        "f2": (text.replace(first_do, first_do.replace("16.9%", "19.6%", 1), 1), caps, old_text),
        "f3": (text.replace(f'| U7 | S238 | "{qd["U7"]}" |', f'| U7 | S236 | "{qd["U7"]}" |', 1), caps, old_text),
        "f4": (text.replace(f'| U0 | S238 | "{qd["U0"]}" |', f'| U0 | S238 | "{qd["U12"]}" |', 1), caps, old_text),
        "f5": (text.replace("| U8 |", "| U99 |", 1), caps, old_text),
        "f6": (text.replace(first_do, first_do + " (impact factor -0.253)", 1), caps, old_text),
        "f7": (text.replace(f'"{qd["U4"]}"', f'"{qd["U3"]} {qd["U4"]}"', 1), caps, old_text),
        "f8": (text, {**caps, "S238": json.dumps(d_bad)}, old_text),
        "f9": (text.replace(rows[1][4], "", 1) if rows[1][4] else text + "x", caps, old_text),
        "f10": (text, caps, old_cut),
        "f11": (text.replace(slope_do, slope_do.replace("-0.002", "0.002", 1), 1), caps, old_text),
        "f12": (text.replace(f"| {first_do} | {NONE_STATED} |", f"| {first_do} | never cite a rate under 30% |", 1),
                caps, old_text),
        "f13": (text.replace(f"updates: {OLD}", "updates: corpus/knowledge/quotation-error-rates-r98.md", 1), caps,
                old_text),
    }
    refused = 0
    for name, (t, c, o) in forgeries.items():
        changed = t != text or c is not caps or o != old_text
        bad = changed and not passes(score(t, c, o, root))
        refused += bad
        print(f"CASE FORGERY {name} {'refused PASS' if bad else 'accepted FAIL'}")
    acc = 0
    a1 = text.replace(rows[-1][4], rows[-1][4] + " (reworded)", 1)
    lines = text.split("\n")
    start = lines.index("## Decision table")
    idx = [i for i, ln in enumerate(lines) if i > start and ln.startswith("| ") and ln.count(" | ") == 4][2:4]
    a2l = list(lines)
    a2l[idx[0]], a2l[idx[1]] = a2l[idx[1]], a2l[idx[0]]
    for name, t in (("a1", a1), ("a2", "\n".join(a2l))):
        ok = t != text and passes(score(t, caps, old_text, root))
        acc += ok
        print(f"CASE ACCEPT {name} {'PASS' if ok else 'FAIL'}")
    print(" ".join(f"{k}={v[0]}/{v[1]}" for k, v in r.items())
          + f" NUMBERS_SOURCED={r['NUMBERS'][0]}/{r['NUMBERS'][1]} BASE_TOPIC_HITS={base_hits}"
          + f" BASE_ENTRY={'present' if base_entry else 'absent'} BASE_UPDATE_LINK={base_link}"
          + f" FORGERY_REFUSED={refused}/{len(forgeries)} ACCEPTED={acc}/2")
    good = good and refused == len(forgeries) and acc == 2
    print(f"ENTRY_CONTROLS_R100={'PASS' if good else 'FAIL'}")
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
