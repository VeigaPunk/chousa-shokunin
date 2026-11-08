#!/usr/bin/env python3
"""curation-r89-controls — the round-89 C2 forgery control battery.

Builds single-cell mirrors of the tree and requires, for every round-88 wave finding this round closes,
  * the round-89 counter REFUSES it (a FAIL verdict, naming the leg), and
  * the round-88 counter ACCEPTS it (the do-nothing evidence: the forgery was a pass before this round).
The positive (unmodified) mirror must be accepted by both, so the repair is not a blanket refusal.

Cases:
  A1c-junk-substitute    the r84 Q11 row deleted and a one-word verbatim quote added in its place, warrant re-pointed
  A1d-truncate           the r84 Q11 quote replaced by the bare verbatim word "range"
  caseG-relabel          the uncited Q10 row deleted and a duplicate of Q13 re-labelled as Q14
  F2-rejected-superseder S031 set to `rejected` while still naming `supersedes S024 —`
  B1b-padding-qid        the r84 "Linking a claim" row gains a second qid whose quote shares nothing with the row
  D1-duplicate-qid       (r89) the repaired warrant row cites `Q1, Q1 (S215)` — one qid counted twice
                         (R88ExecC2Forge finding 3; the r88 counter had no duplicate guard)
  SUP-clause-mirror      (r89) a superseder carries a contrast phrase and a date term absent from its own capture,
                         behind a mined superseder so the main TEACHES loop resolves it. The r88 superseder clause
                         matched a case-sensitive pattern against a lowercased cell and could never fire
                         (R88ScoutRegistry `receipt-supclause-dead.txt`), so it ACCEPTS this mirror; the r89 clause
                         matches the raw cell and refuses it with SUP_UNRESOLVED=1 and TEACHES_UNRESOLVED=0.

Usage: python3 -B corpus/evidence/round89/curation-r90-controls.py --root DIR --work DIR
Exit 0 every case as expected, 1 a case deviating (printed `CASE_DEVIATION`), 2 setup.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
NEW = os.path.join(HERE, "curation-r90.py")
R89 = os.path.join(HERE, "..", "round89", "curation-r89.py")
R88 = os.path.join(HERE, "..", "round88", "curation-r88.py")
R87 = os.path.join(HERE, "..", "round87", "curation-r87.py")
ENTRY_A = "corpus/knowledge/search-transparency-reporting-r84.md"
ENTRY_B = "corpus/knowledge/provenance-recording-r85.md"
# the r84 entry the two term-floor cases were measured on; kept named for the receipt line
S219_ROW = ("| S219 | mirror row (own-work) — corpus/SOURCES.md | own-work | A | mirror | "
            "corpus/SOURCES.md:1 | supersedes S031 — mirror disposal row | mined | 2026-11-08 | 365d | — |")


def mirror(root, dst):
    """A minimal tree the counters read: the registry and the two entries as real copies, captures and the refetch
    ledger linked (the counters only read them)."""
    os.makedirs(os.path.join(dst, "corpus", "knowledge"), exist_ok=True)
    os.makedirs(os.path.join(dst, "corpus", "evidence"), exist_ok=True)
    shutil.copy2(os.path.join(root, "corpus", "SOURCES.md"), os.path.join(dst, "corpus", "SOURCES.md"))
    for rel in (ENTRY_A, ENTRY_B):
        shutil.copy2(os.path.join(root, rel), os.path.join(dst, rel))
    for rel in (os.path.join("corpus", "captures"), os.path.join("corpus", "evidence", "round57")):
        src = os.path.join(root, rel)
        if os.path.isdir(src):
            os.symlink(src, os.path.join(dst, rel))
    return dst


def run(counter, root):
    p = subprocess.run([sys.executable, "-B", counter, "--root", root], capture_output=True, text=True)
    verdict = [ln for ln in p.stdout.splitlines()
               if ln.startswith(("CURATION_R90=", "CURATION_R89=", "CURATION_R88=", "CURATION_R87=", "CURATION_R86="))]
    fails = [ln for ln in p.stdout.splitlines() if ln.startswith("LEG_FAIL")]
    return p.returncode, (verdict[0] if verdict else "no-verdict"), fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--work")
    ap.add_argument("--counter", help="score this counter instead of the committed curation-r90.py")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    global NEW
    if a.counter:
        NEW = os.path.abspath(a.counter)
    work = a.work or os.environ.get("TMPDIR") or "/fast/scratch/hyaku"
    os.makedirs(work, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="cur89-", dir=work)
    ok_all = True
    try:
        cases = []

        def add(cid, mutator, before=R89):
            """`before` is the counter that ACCEPTED this shape: r87 for the five round-87 forgeries the round-88
            counter already refuses, r88 for the two guard classes this round adds."""
            d = mirror(root, os.path.join(tmp, cid))
            mutator(d)
            cases.append((cid, d, before))

        add("POSITIVE", lambda d: None)

        def a1c(d):
            # delete the real Q11 row and add a one-word verbatim quote ("validity" is verbatim in the S023 capture),
            # then re-point the decision row's warrant Q11 -> Q99. The r87 floor counted rows, so it passed.
            pp = os.path.join(d, ENTRY_A)
            out = []
            lines = open(pp, encoding="utf-8", errors="replace").read().split("\n")
            on = False
            for ln in lines:
                if ln.startswith("## "):
                    on = ln.strip() == "## Located quotes"
                    out.append(ln)
                    continue
                if on and re.match(r"^\s*\|\s*Q11\s*\|", ln):
                    continue
                if on and re.match(r"^\s*\|\s*Q13\s*\|", ln):
                    out.append(ln)
                    out.append('| Q99 | S023 | "validity" |')
                    continue
                if "| Q11 (S023) |" in ln:
                    ln = ln.replace("| Q11 (S023) |", "| Q99 (S023) |", 1)
                out.append(ln)
            open(pp, "w", encoding="utf-8").write("\n".join(out))

        add("A1c-junk-substitute", a1c)

        def a1d(d):
            pp = os.path.join(d, ENTRY_A)
            s = open(pp, encoding="utf-8", errors="replace").read()
            n = re.sub(r'^\|\s*Q11\s*\|.*$', '| Q11 | S023 | "range" |', s, count=1, flags=re.M)
            if n == s:
                raise SystemExit("SETUP_MISS a1d: Q11 row not found")
            open(pp, "w", encoding="utf-8").write(n)

        add("A1d-truncate", a1d)

        def caseg(d):
            # delete the uncited Q10 row and re-label a duplicate copy of Q13 as Q14 (the R87 caseG bytes).
            pp = os.path.join(d, ENTRY_A)
            lines = open(pp, encoding="utf-8", errors="replace").read().split("\n")

            def span(lines):
                on = False
                s = e = None
                for i, ln in enumerate(lines):
                    if ln.startswith("## "):
                        if on and s is not None:
                            e = i
                            break
                        on = ln.strip() == "## Located quotes"
                        if on:
                            s = i + 1
                return s, (e if e is not None else len(lines))

            s_, e_ = span(lines)
            q13 = None
            out = []
            for i, ln in enumerate(lines):
                if s_ is not None and s_ <= i < e_ and re.match(r"^\s*\|\s*(Q\d+)", ln):
                    if re.match(r"^\s*\|\s*Q10\s*\|", ln):
                        continue
                    if re.match(r"^\s*\|\s*Q13\s*\|", ln):
                        q13 = ln
                out.append(ln)
            if q13 is None:
                raise SystemExit("SETUP_MISS caseg: Q13 row not found")
            s2, e2 = span(out)
            out[e2:e2] = [re.sub(r"Q13", "Q14", q13, count=1)]
            open(pp, "w", encoding="utf-8").write("\n".join(out))

        add("caseG-relabel", caseg)

        def f2(d):
            pp = os.path.join(d, "corpus", "SOURCES.md")
            out = []
            hit = False
            for ln in open(pp, encoding="utf-8", errors="replace").read().split("\n"):
                if ln.startswith("| S031 |"):
                    ln = ln.replace("| mined | 2026-10-21 |", "| rejected | 2026-10-21 |", 1)
                    hit = "| rejected | 2026-10-21 |" in ln
                out.append(ln)
            if not hit:
                raise SystemExit("SETUP_MISS f2: S031 status cell not found")
            open(pp, "w", encoding="utf-8").write("\n".join(out))

        add("F2-rejected-superseder", f2)

        def b1b(d):
            pp = os.path.join(d, ENTRY_B)
            s = open(pp, encoding="utf-8", errors="replace").read()
            n = s.replace("| Q1 (S215) |", "| Q1, Q3 (S215) |", 1)
            if n == s:
                raise SystemExit("SETUP_MISS b1b: warrant cell not found")
            open(pp, "w", encoding="utf-8").write(n)

        add("B1b-padding-qid", b1b)

        def d1dup(d):
            # R88ExecC2Forge finding 3: `Q1, Q1 (S215)` — the same qid cited twice. The r88 warrant leg found
            # both resolved and both sharing a term, so the row passed; nothing checked for repeats.
            pp = os.path.join(d, ENTRY_B)
            s = open(pp, encoding="utf-8", errors="replace").read()
            n = s.replace("| Q1 (S215) |", "| Q1, Q1 (S215) |", 1)
            if n == s:
                raise SystemExit("SETUP_MISS d1dup: warrant cell not found")
            open(pp, "w", encoding="utf-8").write(n)

        add("D1-duplicate-qid", d1dup, before=R89)

        def supclause(d):
            # A superseder that carries a contrast phrase and a date term absent from its own capture, disposed
            # by a mined mirror row so the main TEACHES loop resolves it. Only the superseder-own-read clause can
            # flag this. S031's capture (Schema.org lastReviewed) contains no `publication`.
            rg = os.path.join(d, "corpus", "SOURCES.md")
            lines = open(rg, encoding="utf-8", errors="replace").read().split("\n")
            out, hit = [], False
            for ln in lines:
                if ln.startswith("| S031 |"):
                    if "distinct from publication dates" not in ln:
                        ln = ln.replace(
                            "no comparison to other date properties claimed",
                            "no comparison to other date properties claimed; distinct from publication dates",
                            1)
                    hit = "distinct from publication dates" in ln
                    out.append(ln)
                    out.append(S219_ROW)
                    continue
                out.append(ln)
            if not hit:
                raise SystemExit("SETUP_MISS supclause: S031 teaches cell not found")
            open(rg, "w", encoding="utf-8").write("\n".join(out))

        add("SUP-clause-mirror", supclause, before=R89)

        for cid, d, before in cases:
            new_rc, new_v, new_f = run(NEW, d)
            old_rc, old_v, old_f = run(before, d)
            if cid == "POSITIVE":
                want = new_rc == 0 and new_v.endswith("=PASS") and old_rc == 0
                label = "positive accepted by both" if want else "positive not accepted"
            else:
                # Round-90 frame: the seven tree-forgery classes were closed by round 89, so the prior counter
                # must refuse them too (a regression hold). The NEW detection credit this round is carried by the
                # counter-edit mutants, where the prior counter is measured to accept (curation-r90-mutants.py).
                want = (new_rc != 0 and new_v.endswith("=FAIL") and bool(new_f)
                        and old_rc != 0 and old_v.endswith("=FAIL"))
                label = ("refused by r90 (" + (new_f[0] if new_f else "no LEG_FAIL") +
                         "), refused by the prior counter (regression held)") if want else "NOT refused by both counters"
            print(f"{'OK' if want else 'CASE_DEVIATION'} {cid}: {label}")
            print(f"  r90: rc={new_rc} {new_v}")
            print(f"  prior: rc={old_rc} {old_v}")
            ok_all = ok_all and want
        forged = [c for c, _, _ in cases if c != "POSITIVE"]
        print(f"FORGERY_REFUSED={sum(1 for c, d, _b in cases if c != 'POSITIVE' and run(NEW, d)[0] != 0)}/{len(forged)} "
              f"PRIOR_REGRESSION="
              f"{sum(1 for c, d, b in cases if c != 'POSITIVE' and run(b, d)[0] != 0)}/{len(forged)}")
        print(f"CONTROLS={'PASS' if ok_all else 'FAIL'}")
        return 0 if ok_all else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
