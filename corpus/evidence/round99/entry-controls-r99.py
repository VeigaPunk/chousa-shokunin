#!/usr/bin/env python3
"""entry-controls-r99 — round-99 C2 (coverage) controls for `corpus/knowledge/quotation-error-rates-r99.md`.

Recomputes what the entry says it holds from files under --root as they are on disk (the entry, captures
`405a0054e1f6dbd1854a3618` (S236) and `4b70901ad80c513f0c2f750c` (S233)) plus `git ls-tree`/`git show` at BASE for the
do-nothing leg; no network, no write. Legs:

  QUOTES      every `## Located quotes` row: its quote, normalized as `tools/gate-records.py` normalizes, occurs in
              its own source's capture, and has 1-25 words
  FIELD       S236's capture parsed as JSON: J0 equals the record's `title` (normalized); every other S236 quote lies
              inside `abstractText`
  IDENTITY    S236 is Jergas & Baethge 2015: `hitCount` 1, `pmid` 26528420, `doi` 10.7717/peerj.1364, `pubYear` 2015,
              journal title PeerJ, volume 3; S233's capture carries doi 10.1371/journal.pone.0184727 and the G0 title
  WARRANTS    every `## Decision table` row's Warrant names only qids of the quote table; every Lane cell non-empty
  NUMBERS     every numeric token (`[0-9]+([.,][0-9]+)*%?`) of every Do cell occurs, as written, in the normalized text
              of that row's own warrant quotes (printed `NUMBERS_SOURCED=k/n`)
  TOPIC       no `corpus/knowledge/*.md` blob at BASE contains "quotation error" (case-insensitive), and this entry does
  BASE        the do-nothing control: the entry path is absent at BASE (the controls refuse it: `BASE_ENTRY=absent`)
  FORGERY     ten in-memory forgeries that the legs above must refuse: f1 G10's "14.5%" made "15.4%"; f2 a Do cell's
              "14.5%" made "24.5%"; f3 J2 attributed to S233; f4 J0 replaced by an abstract sentence (FIELD); f5 a
              warrant naming G99; f6 a Do cell's "11,9%" written "11.9%"; f7 G4 widened to 26 words with text that is
              in the capture; f8 the S236 record with `pmid` changed (IDENTITY); f9 a Lane cell emptied; f10 a Do cell
              number moved to a row whose warrants do not print it ("6.7%" into the first row)
  ACCEPT      two edits that change no claim (a Lane cell reworded, two decision rows swapped) must still PASS

Usage: python3 -B corpus/evidence/round99/entry-controls-r99.py --root LANE
Prints CASE lines, one tally line and `ENTRY_CONTROLS_R99=PASS|FAIL`. Exit 0 PASS, 1 FAIL, 2 setup.
"""
import argparse
import json
import os
import re
import subprocess
import sys

BASE = "47ed34fa785288837f84cde9db15c41300854a78"
ENTRY = "corpus/knowledge/quotation-error-rates-r99.md"
CAPS = {"S236": "corpus/captures/405a0054e1f6dbd1854a3618.txt", "S233": "corpus/captures/4b70901ad80c513f0c2f750c.txt"}
ROW = re.compile(r'^\| ([A-Z][0-9]+) \| (S[0-9]+) \| "(.*)" \|$')
NUM = re.compile(r"[0-9]+(?:[.,][0-9]+)*%?")


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


def score(text, caps):
    """Return dict leg -> (ok, n) for one entry text and capture texts."""
    r = {}
    qs = quotes(text)
    qmap = {q: (s, t) for q, s, t in qs}
    ok = sum(1 for q, s, t in qs if s in caps and norm(t) in norm(caps[s]) and 1 <= len(t.split()) <= 25)
    r["QUOTES"] = (ok, len(qs))
    try:
        rec = json.loads(caps["S236"])["resultList"]["result"][0]
        title, abstract = norm(rec["title"]), norm(rec["abstractText"])
    except (ValueError, KeyError, IndexError):
        rec, title, abstract = None, "", ""
    f236 = [(q, t) for q, s, t in qs if s == "S236"]
    r["FIELD"] = (sum(1 for q, t in f236 if (norm(t) == title if q == "J0" else norm(t) in abstract)), len(f236))
    ident = 0
    try:
        d = json.loads(caps["S236"])
        ident += (d["hitCount"] == 1 and rec["pmid"] == "26528420" and rec["doi"] == "10.7717/peerj.1364"
                  and rec["pubYear"] == "2015" and rec["journalInfo"]["journal"]["title"] == "PeerJ"
                  and rec["journalInfo"]["volume"] == "3")
    except (ValueError, KeyError, IndexError, TypeError):
        pass
    g0 = qmap.get("G0", ("", ""))[1]
    ident += "10.1371/journal.pone.0184727" in caps["S233"] and bool(g0) and norm(g0) in norm(caps["S233"])
    r["IDENTITY"] = (ident, 2)
    rows = decisions(text)
    wok = 0
    nums_ok = nums_n = 0
    for row in rows:
        if len(row) != 5:
            continue
        ids = [w.strip() for w in row[3].split(",")]
        wok += all(i in qmap for i in ids) and bool(row[4])
        wtext = " ".join(norm(qmap[i][1]) for i in ids if i in qmap)
        for n in NUM.findall(row[1]):
            nums_n += 1
            nums_ok += n in wtext
    r["WARRANTS"] = (wok, len(rows))
    r["NUMBERS"] = (nums_ok, nums_n)
    r["TOPIC"] = (int("quotation error" in text.lower()), 1)
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
        caps = {s: open(os.path.join(root, p), encoding="utf-8", errors="replace").read() for s, p in CAPS.items()}
    except OSError as e:
        print(f"ENTRY_CONTROLS_SETUP {e}", file=sys.stderr)
        return 2
    r = score(text, caps)
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
        base_hits += "quotation error" in b.stdout.lower()
    base_entry = ENTRY in ls.stdout.split()
    print(f"CASE BASE entry={'present' if base_entry else 'absent'} topic_hits={base_hits} "
          f"{'PASS' if not base_entry and base_hits == 0 else 'FAIL'}")
    good = good and not base_entry and base_hits == 0
    j2 = next(t for q, s, t in quotes(text) if q == "J2")
    rec = json.loads(caps["S236"])
    rec_bad = json.loads(caps["S236"])
    rec_bad["resultList"]["result"][0]["pmid"] = "26528421"
    g4 = next(t for q, s, t in quotes(text) if q == "G4")
    rows = decisions(text)
    first_do = rows[0][1]
    forgeries = {
        "f1": (text.replace("I estimate that 14.5%", "I estimate that 15.4%", 1), caps),
        "f2": (text.replace(first_do, first_do.replace("14.5%", "24.5%"), 1), caps),
        "f3": (text.replace(f'| J2 | S236 | "{j2}" |', f'| J2 | S233 | "{j2}" |', 1), caps),
        "f4": (text.replace('| J0 | S236 | "Quotation accuracy in medical journal articles-a systematic review and '
                            'meta-analysis." |', '| J0 | S236 | "Indirect references accounted for less than one '
                            'sixth of all quotation problems." |', 1), caps),
        "f5": (text.replace("| G4, G5 |", "| G4, G99 |", 1), caps),
        "f6": (text.replace(first_do, first_do.replace("11,9%", "11.9%"), 1), caps),
        "f7": (text.replace(g4, "As summarized in Table 2 , " + g4, 1), caps),
        "f8": (text, {**caps, "S236": json.dumps(rec_bad)}),
        "f9": (text.replace(rows[1][4], "", 1) if rows[1][4] else text + "x", caps),
        "f10": (text.replace(first_do, first_do + " (lowest 6.7%)", 1), caps),
    }
    refused = 0
    for name, (t, c) in forgeries.items():
        changed = t != text or c is not caps
        bad = changed and not passes(score(t, c))
        refused += bad
        print(f"CASE FORGERY {name} {'refused PASS' if bad else 'accepted FAIL'}")
    acc = 0
    a1 = text.replace(rows[-1][4], rows[-1][4] + " (reworded)", 1)
    lines = text.split("\n")
    idx = [i for i, ln in enumerate(lines) if ln.startswith("| ") and ln.count(" | ") == 4
           and i > lines.index("## Decision table")][2:4]
    a2l = list(lines)
    a2l[idx[0]], a2l[idx[1]] = a2l[idx[1]], a2l[idx[0]]
    for name, t in (("a1", a1), ("a2", "\n".join(a2l))):
        ok = t != text and passes(score(t, caps))
        acc += ok
        print(f"CASE ACCEPT {name} {'PASS' if ok else 'FAIL'}")
    del rec
    print(" ".join(f"{k}={v[0]}/{v[1]}" for k, v in r.items())
          + f" NUMBERS_SOURCED={r['NUMBERS'][0]}/{r['NUMBERS'][1]} BASE_TOPIC_HITS={base_hits}"
          + f" BASE_ENTRY={'present' if base_entry else 'absent'} FORGERY_REFUSED={refused}/{len(forgeries)}"
          + f" ACCEPTED={acc}/2")
    good = good and refused == len(forgeries) and acc == 2
    print(f"ENTRY_CONTROLS_R99={'PASS' if good else 'FAIL'}")
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
