#!/usr/bin/env python3
"""entry-controls-r95 — round-95 C2 (depth) controls for corpus/knowledge/search-rerun-record-r95.md.

The instruments are the lane's own, unchanged this round: `tools/gate-records.py verify` (the quote of every
`GATE-RECORD` line, normalized, occurs in its committed capture, whose bytes match a refetch.tsv row of the same
id/url/time with http 200) and `bash tools/research-gate.sh verify-metadata` (source / verified-at / recheck).
This script runs them as fresh processes and adds two bindings of its own, both over the entry's bytes:

  LQ_BOUND     every `## Located quotes` row's quote equals the quote of one GATE-RECORD line (one-to-one), so
               the human-readable table cannot carry text the gate never located
  WARRANTS_OK  every decision-table row's Warrant cell names at least one qid, and every named qid is a
               Located-quotes row

Groups: POSITIVE (the committed entry), FORGERY (8 copies under --work, each must fail gate-records with the named
code), DO_NOTHING (the entry path at base 7b237358 does not exist and gate-records on it exits 2).

Usage: python3 -B corpus/evidence/round95/entry-controls-r95.py --root LANE --work DIR
Exit 0 PASS, 1 FAIL, 2 setup. Writes only under --work (removed at exit).
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

BASE = "7b2373586fb70f0ead6446c671fcc8b546d3e687"
ENTRY = "corpus/knowledge/search-rerun-record-r95.md"
N_RECORDS = 9


def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def section(text, head):
    m = re.search(r"^## " + re.escape(head) + r"\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


def bindings(text):
    recs = re.findall(r'^GATE-RECORD .* quote="(.*)"$', text, re.M)
    lq = {}
    for ln in section(text, "Located quotes").splitlines():
        m = re.match(r'^\| (Q[0-9]+) \| (S[0-9]+) \| "(.*)" \|$', ln)
        if m:
            lq[m.group(1)] = m.group(3)
    pool = list(recs)
    bound = 0
    for q in lq.values():
        if q in pool:
            pool.remove(q)
            bound += 1
    lq_ok = bound == len(lq) == len(recs) and not pool
    rows = [ln for ln in section(text, "Decision table").splitlines()
            if ln.startswith("| ") and not ln.startswith("| Situation") and not ln.startswith("|---")]
    w_ok = 0
    for ln in rows:
        cells = [c.strip() for c in ln.strip()[1:-1].split("|")]
        named = re.findall(r"\bQ[0-9]+\b", cells[3]) if len(cells) >= 4 else []
        if named and all(q in lq for q in named):
            w_ok += 1
    return bound, len(lq), len(recs), lq_ok, w_ok, len(rows)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args(argv)
    root = os.path.realpath(a.root)
    work = os.path.join(os.path.realpath(a.work), "entry-controls-r95")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    try:
        path = os.path.join(root, ENTRY)
        if not os.path.isfile(path):
            print(f"ENTRY_CONTROLS=SETUP missing {ENTRY}")
            return 2
        text = open(path, encoding="utf-8").read()
        t = {}

        rc, out, err = run([sys.executable, "-B", "tools/gate-records.py", "verify", "--root", ".", ENTRY], root)
        g_ok = rc == 0 and f"GATE_RECORDS files=1 records={N_RECORDS} ok={N_RECORDS} fail=0" in out
        mrc, mout, _ = run(["bash", "tools/research-gate.sh", "verify-metadata", ENTRY, "--root", "."], root)
        m_ok = mrc == 0 and "RESEARCH_GATE: CLEAN" in mout and "METADATA_COMPLETE=1/1" in mout
        bound, nlq, nrec, lq_ok, w_ok, nrows = bindings(text)
        pos = g_ok and m_ok and lq_ok and nrows > 0 and w_ok == nrows
        print(f"CASE positive gate_rc={rc} meta_rc={mrc} LQ_BOUND={bound}/{nlq} records={nrec}"
              f" WARRANTS_OK={w_ok}/{nrows} {'ok' if pos else 'FAIL'}")
        t["POSITIVE"] = (1 if pos else 0, 1)

        first = re.search(r"^GATE-RECORD .*$", text, re.M).group(0)

        def rec_with(q):
            return re.search(r'^GATE-RECORD .* quote="' + re.escape(q) + r'"$', text, re.M).group(0)

        q3 = "Document the total number of records identified from each database and other information sources."
        q7 = "If a reader tries to duplicate a search from"
        q7_joined = "If a reader tries to duplicate a search from a systematic review"
        q1 = "Include the search strategies for each database and information source, copied and pasted exactly as run."
        long_q = q1 + " Limits and restrictions 9 Specify that no limits were used, or describe any limits or restrictions"
        forgeries = [
            ("g1-word", rec_with(q3), rec_with(q3).replace("total number", "overall number"), "QUOTE_ABSENT"),
            ("g2-column-join", rec_with(q7),
             rec_with(q7).replace(f"words=9 quote=\"{q7}\"", f"words=12 quote=\"{q7_joined}\""), "QUOTE_ABSENT"),
            ("g3-capture-key", first, first.replace("1a8c36c4c24444967bd9c3ce", "0ae65ac01b93119d3c2f3fed"),
             "CAPTURE_KEY"),
            ("g4-words", first, re.sub(r"words=(\d+)", lambda m: f"words={int(m.group(1)) + 1}", first), "WORDS"),
            ("g5-tier", first, first.replace("tier=A", "tier=B"), "TIER"),
            ("g6-fetched", first, first.replace("22:51:39Z", "22:51:40Z"), "REFETCH"),
            ("g7-long", rec_with(q1), rec_with(q1).replace(f"words=16 quote=\"{q1}\"",
                                                          f"words={len(long_q.split())} quote=\"{long_q}\""),
             "QUOTE_LEN"),
        ]
        refused = 0
        for name, old, new, code in forgeries:
            if old == new:
                print(f"SETUP forgery {name} no-op")
                return 2
            fp = os.path.join(work, name + ".md")
            open(fp, "w", encoding="utf-8").write(text.replace(old, new, 1))
            rc, out, err = run([sys.executable, "-B", "tools/gate-records.py", "verify", "--root", ".", fp], root)
            fails = re.findall(r"FAIL ([A-Z_,]+)", out)
            ok = rc == 1 and any(code in f.split(",") for f in fails) and len(fails) == 1
            print(f"CASE {name} rc={rc} expect=1 fail={fails} want={code} {'ok' if ok else 'FAIL'}")
            refused += 1 if ok else 0
        # g8: the same entry with every GATE-RECORD line removed (a sourceless copy of the tables): no record.
        fp = os.path.join(work, "g8-sourceless.md")
        open(fp, "w", encoding="utf-8").write(re.sub(r"^GATE-RECORD .*\n", "", text, flags=re.M))
        rc, out, err = run([sys.executable, "-B", "tools/gate-records.py", "verify", "--root", ".", fp], root)
        ok = rc == 1 and "records=0" in out
        print(f"CASE g8-sourceless rc={rc} expect=1 records=0 {'ok' if ok else 'FAIL'}")
        refused += 1 if ok else 0
        t["FORGERY_REFUSED"] = (refused, len(forgeries) + 1)

        brc, _, _ = run(["git", "cat-file", "-e", f"{BASE}:{ENTRY}"], root)
        absent = os.path.join(work, "base-absent", ENTRY)
        rc, out, err = run([sys.executable, "-B", "tools/gate-records.py", "verify", "--root", ".", absent], root)
        ok = brc != 0 and rc == 2
        print(f"CASE do-nothing-base entry_at_base={'absent' if brc else 'present'} gate_rc={rc} expect=2"
              f" {'ok' if ok else 'FAIL'}")
        t["DO_NOTHING_REFUSED"] = (1 if ok else 0, 1)

        print(" ".join(f"{k}={a}/{b}" for k, (a, b) in t.items())
              + f" GATE_RECORDS={N_RECORDS if g_ok else 'x'}/{N_RECORDS} LQ_BOUND={bound}/{nlq}"
                f" WARRANTS_OK={w_ok}/{nrows} METADATA={'clean' if m_ok else 'FAIL'}")
        passed = all(a == b and b > 0 for a, b in t.values())
        print("ENTRY_CONTROLS=" + ("PASS" if passed else "FAIL"))
        return 0 if passed else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
