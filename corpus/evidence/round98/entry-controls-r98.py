#!/usr/bin/env python3
"""entry-controls-r98 — round-98 C2 (depth) controls for `corpus/knowledge/press-2015-statement-questions-r98.md`.

Recomputes, from committed lane bytes only (no network, no lane write), what the entry says it holds:

  QUESTION_LINES  S225's capture lines between the line `PRESS 2015 Guideline Evidence-Based Checklist` and the line
                  `Derived from:` that contain `?`; a line is HELD when its whitespace-collapsed text equals one S225
                  quote, or consecutive S225 quotes of one entry's `## Located quotes` table joined by one space,
                  in the round-97 entry or this entry. Required: every line held (printed `QUESTION_LINES_HELD=k/n`)
  BASE            the same count with the entries as they stand at BASE (the round-97 landing: the round-97 entry
                  only); the do-nothing control is refused when it holds every line (printed `BASE_HELD=k/n`)
  NEW_ONLY        no S225 quote of this entry already holds a line the round-97 entry holds
  QUOTES          every quote of this entry, normalized as `tools/gate-records.py` normalizes, occurs in its own
                  source's capture; every S225 quote lies inside one capture line; at most 25 words
  ELEMENTS        `## Element names compared`: each S231 cell occurs in S231's normalized capture (7 rows), each S225
                  cell (except the row marked `(not in the checklist)`) is one whole S225 capture line (6 rows)
  WARRANTS        every decision row's Warrant names only qids of this entry's table, each group under the source
                  its parenthesis names; Lane cells non-empty
  FIELD (F2)      S231's capture parsed as JSON: each S231 quote equals the record's `title` (normalized) or lies inside
                  its `abstractText` with no `<h4>` markup inside the quote (amendment B1, `R98ReviewerC2` F1)
  IDENTITY (F2)   the record is the PRESS 2015 Guideline Statement: `hitCount` 1, `pmid` 27005575, `doi`
                  10.1016/j.jclinepi.2016.01.021, the statement's title, volume 75, pages 40-46 (kill rule K5;
                  `R98ConnectorSiblings` R4)
  FORGERY         in-memory forgeries of the entry that the counters above must refuse: a K quote with a word
                  dropped; K18 and K19 swapped; a K quote widened across two capture lines; an S225 element cell in
                  S223's grouping; an S231 element cell in S225's wording; a warrant naming a qid that is not in the
                  table; a warrant naming an S231 qid under (S225); and at F2 (`R98MutantsC2` survivors m08, m12, m13,
                  E5) an S225 element cell that is part of a line, not the line; an extra 26-word quote inside one
                  capture line; an extra quote spanning two capture lines; an S231 quote from outside the abstract
                  and title; plus a record whose `pmid` is changed (IDENTITY)
  ACCEPT (F2)     two edits that change no claim (a Lane cell reworded, two decision rows swapped) must still PASS,
                  so a counter that refuses every entry fails it. (`R98MutantsC2` m10, a forced forgery tally, still
                  survives: every forgery here is refused, so forcing the tally changes nothing on these bytes.)

Usage: python3 -B corpus/evidence/round98/entry-controls-r98.py --root LANE
Prints one CASE line per check, the tallies and `ENTRY_CONTROLS_R98=PASS|FAIL`. Exit 0 PASS, 1 FAIL, 2 setup.
"""
import argparse
import json
import os
import re
import subprocess
import sys

BASE = "98b8177c1e8b39cdf1167928e4f5d609f6fa81b6"
ENTRY = "corpus/knowledge/press-2015-statement-questions-r98.md"
PRIOR = "corpus/knowledge/press-checklist-questions-r97.md"
CAPS = {"S225": "corpus/captures/347c55ba9be9d63afe17986e.txt", "S231": "corpus/captures/4ec85a1e83553aa272caeb69.txt"}
HEAD, FOOT = "PRESS 2015 Guideline Evidence-Based Checklist", "Derived from:"
ROW = re.compile(r'^\| ([A-Z][0-9]+) \| (S[0-9]+) \| "(.*)" \|$')


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
    """[(qid, source, quote)] of the `## Located quotes` table, in table order."""
    return [m.groups() for m in (ROW.match(ln) for ln in section(text, "Located quotes")) if m]


def table(text, title):
    rows = [ln for ln in section(text, title) if ln.startswith("|")]
    return [[c.strip() for c in r.strip()[1:-1].split(" | ")] for r in rows[2:]]


def question_lines(s225):
    lines = s225.split("\n")
    a = next(i for i, ln in enumerate(lines) if ln.strip() == HEAD)
    b = next(i for i, ln in enumerate(lines) if ln.strip() == FOOT)
    return [(i + 1, norm(lines[i])) for i in range(a, b) if "?" in lines[i]]


def held(qlines, entries):
    """Line numbers held: a line equals a run of consecutive S225 quotes of one entry joined by one space."""
    runs = set()
    for text in entries:
        qs = [norm(q) for _, src, q in quotes(text) if src == "S225"]
        for i in range(len(qs)):
            for j in range(i + 1, min(len(qs), i + 4) + 1):
                runs.add(" ".join(qs[i:j]))
    return {n for n, t in qlines if t in runs}


def check_quotes(text, caps):
    bad = []
    s225_lines = [norm(ln) for ln in caps["S225"].split("\n")]
    for qid, src, q in quotes(text):
        nq = norm(q)
        if src not in caps or nq not in norm(caps[src]) or not 1 <= len(q.split()) <= 25:
            bad.append(qid)
        elif src == "S225" and not any(nq in ln for ln in s225_lines):
            bad.append(qid)
    return bad


def check_elements(text, caps):
    rows = table(text, "Element names compared")
    s225_lines = {norm(ln) for ln in caps["S225"].split("\n")}
    ok231 = sum(1 for r in rows if len(r) == 4 and norm(r[1]) in norm(caps["S231"]))
    ok225 = sum(1 for r in rows if len(r) == 4 and r[2] != "(not in the checklist)" and norm(r[2]) in s225_lines)
    return ok231, ok225, len(rows)


def check_warrants(text):
    ids = {qid: src for qid, src, _ in quotes(text)}
    rows = table(text, "Decision table")
    ok, filled = 0, 0
    for r in rows:
        if len(r) != 5:
            continue
        groups = re.findall(r"([A-Z0-9, ]+?) \((S[0-9]+)\)", r[3])
        named = [(q.strip(), src) for g, src in groups for q in g.split(",") if q.strip()]
        ok += 1 if named and all(ids.get(q) == src for q, src in named) else 0
        filled += 1 if r[4] else 0
    return ok, filled, len(rows)


def record(caps):
    return json.loads(caps["S231"])["resultList"]["result"][0]


def check_fields(text, caps):
    """S231 quotes outside their JSON field: not the title and not inside abstractText (or spanning `<h4>`)."""
    rec = record(caps)
    title, abstract = norm(rec.get("title", "")), norm(rec.get("abstractText", ""))
    bad, n = [], 0
    for qid, src, q in quotes(text):
        if src != "S231":
            continue
        n += 1
        nq = norm(q)
        if not (nq == title or (nq in abstract and "<h4>" not in q)):
            bad.append(qid)
    return bad, n


def identity(caps):
    d = json.loads(caps["S231"])
    rec = d["resultList"]["result"][0]
    return (d.get("hitCount") == 1 and rec.get("pmid") == "27005575" and rec.get("doi") == "10.1016/j.jclinepi.2016.01.021"
            and norm(rec.get("title", "")) == "PRESS Peer Review of Electronic Search Strategies: 2015 Guideline Statement."
            and rec.get("journalInfo", {}).get("volume") == "75" and rec.get("pageInfo") == "40-46")


def score(text, prior, caps):
    qlines = question_lines(caps["S225"])
    h = held(qlines, [prior, text])
    bad = check_quotes(text, caps)
    e231, e225, en = check_elements(text, caps)
    w, f, wn = check_warrants(text)
    fbad, fn = check_fields(text, caps)
    ident = identity(caps)
    passed = (len(h) == len(qlines) and not bad and (e231, e225, en) == (7, 6, 7) and w == wn and f == wn and wn > 0
              and not fbad and fn > 0 and ident)
    return passed, dict(held=len(h), n=len(qlines), bad=bad, e231=e231, e225=e225, en=en, w=w, f=f, wn=wn,
                        fbad=fbad, fn=fn, ident=ident)


def show(root, rev, path):
    p = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"], capture_output=True, text=True)
    return p.returncode, p.stdout


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args(argv)
    root = os.path.realpath(a.root)
    try:
        caps = {k: open(os.path.join(root, v), encoding="utf-8").read() for k, v in CAPS.items()}
        text = open(os.path.join(root, ENTRY), encoding="utf-8").read()
        prior = open(os.path.join(root, PRIOR), encoding="utf-8").read()
    except OSError as exc:
        print(f"SETUP {exc}")
        return 2
    t = {}
    passed, d = score(text, prior, caps)
    print(f"CASE positive held={d['held']}/{d['n']} bad_quotes={d['bad'] or '-'} elements231={d['e231']}/{d['en']}"
          f" elements225={d['e225']}/6 warrants={d['w']}/{d['wn']} lane_filled={d['f']}/{d['wn']}"
          f" field_bad={d['fbad'] or '-'}/{d['fn']} identity={d['ident']} {'ok' if passed else 'FAIL'}")
    t["POSITIVE"] = (1 if passed else 0, 1)

    brc, base_prior = show(root, BASE, PRIOR)
    erc, _ = show(root, BASE, ENTRY)
    if brc:
        print(f"SETUP {PRIOR} unreadable at {BASE}")
        return 2
    qlines = question_lines(caps["S225"])
    base_held = held(qlines, [base_prior])
    ok = erc != 0 and len(base_held) < len(qlines)
    print(f"CASE do-nothing-base entry_at_base={'absent' if erc else 'present'} BASE_HELD={len(base_held)}/{len(qlines)}"
          f" {'ok' if ok else 'FAIL'}")
    t["DO_NOTHING_REFUSED"] = (1 if ok else 0, 1)

    prior_held = held(qlines, [prior])
    own_held = held(qlines, [text])
    overlap = sorted(prior_held & own_held)
    ok = not overlap and prior_held | own_held == {n for n, _ in qlines}
    print(f"CASE new-only prior={len(prior_held)} own={len(own_held)} overlap={overlap or '-'} {'ok' if ok else 'FAIL'}")
    t["NEW_ONLY"] = (1 if ok else 0, 1)

    forgeries = {
        "f1-drop-word": text.replace('"Are the search concepts too narrow or too broad?"',
                                     '"Are the search concepts narrow or too broad?"'),
        "f2-swap-k18-k19": text.replace('| K18 | S225 | "Are there any other fields to be included" |\n'
                                        '| K19 | S225 | "or excluded (database specific)?" |',
                                        '| K19 | S225 | "or excluded (database specific)?" |\n'
                                        '| K18 | S225 | "Are there any other fields to be included" |'),
        "f3-widen-across-lines": text.replace('"Are the search concepts clear?"',
                                              '"Are the search concepts clear? Are there too many or too few PICO"'),
        "f4-s223-grouping": text.replace("| 5. Spelling, syntax, and line numbers |",
                                         "| 5. Limits and filters, syntax and line numbers |"),
        "f5-s231-in-s225-words": text.replace("| text word search | 4.", "| Text word searching (free text) | 4."),
        "f6-unknown-qid": text.replace("| K1, K2 (S225) |", "| K1, K2, K40 (S225) |"),
        "f7-wrong-source": text.replace("| K3, K4, K5 (S225) |", "| K3, K4, M5 (S225) |"),
        # F2 (R98MutantsC2 m08, m12, m13, E5)
        "f8-element-part-of-line": text.replace("| 1. Translation of the research question |",
                                                "| Translation of the research question |"),
        "f9-quote-26-words": text.replace(
            '| K22 | S225 | "Can any limits or filters be added or taken away?" |',
            '| K22 | S225 | "Can any limits or filters be added or taken away?" |\n'
            '| K23 | S225 | "Are there incorrect line combinations or orphan lines (ie, lines that are not referred to in the final summation that could indicate an error in an" |'),
        "f10-extra-quote-two-lines": text.replace(
            '| K22 | S225 | "Can any limits or filters be added or taken away?" |',
            '| K22 | S225 | "Can any limits or filters be added or taken away?" |\n'
            '| K23 | S225 | "Are the search concepts clear? Are there too many or too few PICO elements included?" |'),
        "f11-s231-outside-abstract": text.replace(
            '| M15 | S231 | "The PRESS 2015 Guideline Statement should help to guide and improve the peer review of electronic literature search strategies." |',
            '| M15 | S231 | "Journal of clinical epidemiology" |'),
    }
    refused = 0
    for name, body in forgeries.items():
        if body == text:
            print(f"SETUP forgery {name} did not apply")
            return 2
        fp, fd = score(body, prior, caps)
        print(f"CASE forgery {name} held={fd['held']}/{fd['n']} bad_quotes={fd['bad'] or '-'} "
              f"elements={fd['e231']}/{fd['e225']} warrants={fd['w']}/{fd['wn']} field_bad={fd['fbad'] or '-'} "
              f"{'refused ok' if not fp else 'ACCEPTED FAIL'}")
        refused += 0 if fp else 1
    forged_caps = dict(caps, S231=caps["S231"].replace('"pmid":"27005575"', '"pmid":"27005576"', 1))
    if forged_caps["S231"] == caps["S231"]:
        print("SETUP forgery f12-record-identity did not apply")
        return 2
    fp, fd = score(text, prior, forged_caps)
    print(f"CASE forgery f12-record-identity identity={fd['ident']} {'refused ok' if not fp else 'ACCEPTED FAIL'}")
    refused += 0 if fp else 1
    t["FORGERY_REFUSED"] = (refused, len(forgeries) + 1)
    t["IDENTITY"] = (1 if d["ident"] else 0, 1)
    t["FIELD_SCOPED"] = (d["fn"] - len(d["fbad"]), d["fn"])

    rows = [ln for ln in text.split("\n") if ln.startswith("| Checking ")]
    benign = {
        "a1-lane-reworded": text.replace("(round-97 entry, limits row) |", "(see the round-97 entry, limits row) |"),
        "a2-rows-swapped": text.replace(rows[0] + "\n" + rows[1], rows[1] + "\n" + rows[0]) if len(rows) > 1 else text,
    }
    accepted = 0
    for name, body in benign.items():
        if body == text:
            print(f"SETUP benign {name} did not apply")
            return 2
        fp, _ = score(body, prior, caps)
        print(f"CASE benign {name} {'accepted ok' if fp else 'REFUSED FAIL'}")
        accepted += 1 if fp else 0
    t["ACCEPTED"] = (accepted, len(benign))

    print(" ".join(f"{k}={x}/{y}" for k, (x, y) in t.items())
          + f" QUESTION_LINES_HELD={d['held']}/{d['n']} BASE_HELD={len(base_held)}/{len(qlines)}"
          f" ELEMENTS={d['e231']}+{d['e225']}/{d['en']}+6 WARRANTS_OK={d['w']}/{d['wn']} LANE_FILLED={d['f']}/{d['wn']}")
    ok = all(x == y and y > 0 for x, y in t.values())
    print("ENTRY_CONTROLS_R98=" + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
