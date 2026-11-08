#!/usr/bin/env python3
"""curation-r88-controls — the round-88 C2 forgery control battery.

Builds single-cell mirrors of the tree and requires, for every round-86 routed forgery, that
  * the round-88 counter REFUSES it (a FAIL verdict, naming the leg), and
  * the round-87 counter ACCEPTS it (the do-nothing evidence: the forgery was a pass before this round).
The positive (unmodified) mirror must be accepted by both, so the repair is not a blanket refusal.

Cases (`plans/round-87.md` Amendments 1, 2, 3, 6 — the round-87 wave findings this round closes):
  A1c-junk-substitute    the r84 Q11 row deleted and a one-word verbatim quote added in its place, warrant re-pointed
  A1d-truncate           the r84 Q11 quote replaced by the bare verbatim word "range"
  caseG-relabel          the uncited Q10 row deleted and a duplicate of Q13 re-labelled as Q14
  F2-rejected-superseder S031 set to `rejected` while still naming `supersedes S024 —`
  B1b-padding-qid        the r84 "Linking a claim" row gains a second qid whose quote shares nothing with the row

Usage: python3 -B corpus/evidence/round88/curation-r88-controls.py --root DIR --work DIR
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
NEW = os.path.join(HERE, "curation-r88.py")
OLD = os.path.join(HERE, "..", "round87", "curation-r87.py")
ENTRY_A = "corpus/knowledge/search-transparency-reporting-r84.md"
ENTRY_B = "corpus/knowledge/provenance-recording-r85.md"


def mirror(root, dst):
    """A minimal tree the counters read: the registry and the two entries as real copies, captures and the refetch
    ledger as symlinks (read-only)."""
    os.makedirs(os.path.join(dst, "corpus", "knowledge"), exist_ok=True)
    os.makedirs(os.path.join(dst, "corpus", "evidence"), exist_ok=True)
    for rel in ("corpus/SOURCES.md", ENTRY_A, ENTRY_B):
        shutil.copy2(os.path.join(root, rel), os.path.join(dst, rel))
    for link, target in (("corpus/captures", os.path.join(root, "corpus", "captures")),
                         ("corpus/evidence/round57", os.path.join(root, "corpus", "evidence", "round57"))):
        p = os.path.join(dst, link)
        if not os.path.exists(p):
            os.symlink(target, p)
    return dst


def drop_quote_rows(path, keep):
    """Keep only the located-quote rows whose qid is in `keep`."""
    out = []
    on = False
    for ln in open(path, encoding="utf-8", errors="replace").read().split("\n"):
        if ln.startswith("## "):
            on = ln.strip() == "## Located quotes"
            out.append(ln)
            continue
        if on and ln.lstrip().startswith("|"):
            m = re.match(r"^\s*\|\s*(Q\d+)", ln)
            if m and m.group(1) not in keep:
                continue
        out.append(ln)
    open(path, "w", encoding="utf-8").write("\n".join(out))


def run(counter, root):
    p = subprocess.run([sys.executable, "-B", counter, "--root", root], capture_output=True, text=True)
    lines = p.stdout.splitlines()
    verdict = [l for l in lines if re.match(r"^(CURATION_R\d\d=|CURATION_R88=)", l)]
    fails = [l for l in lines if l.startswith("LEG_FAIL")]
    return p.returncode, (verdict[0] if verdict else "no-verdict"), fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--work")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    work = a.work or os.environ.get("TMPDIR") or "/fast/scratch/hyaku"
    os.makedirs(work, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="cur88-", dir=work)
    ok_all = True
    try:
        cases = []

        def add(cid, mutator):
            d = mirror(root, os.path.join(tmp, cid))
            mutator(d)
            cases.append((cid, d))

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
                    cells = [c for c in ln.split("|")]
                    # status is cell 9 (index 9 in the split with leading empty): ... | mined | 2026-10-21 | 365d |
                    ln = ln.replace("| mined | 2026-10-21 |", "| rejected | 2026-10-21 |", 1)
                    hit = "| rejected | 2026-10-21 |" in ln
                out.append(ln)
            if not hit:
                raise SystemExit("SETUP_MISS f2: S031 status cell not found")
            open(pp, "w", encoding="utf-8").write("\n".join(out))

        add("F2-rejected-superseder", f2)

        def b1b(d):
            # r87 B1b: a second qid is added to the "Linking a claim" row; its quote shares nothing with the row.
            # The repaired r85 row now names Q1 alone, so the padding qid is Q3 (whose quote shares nothing either).
            pp = os.path.join(d, ENTRY_B)
            s = open(pp, encoding="utf-8", errors="replace").read()
            n = s.replace('| Q1 (S215) |', '| Q1, Q3 (S215) |', 1)
            if n == s:
                raise SystemExit("SETUP_MISS b1b: warrant cell not found")
            open(pp, "w", encoding="utf-8").write(n)

        add("B1b-padding-qid", b1b)

        for cid, d in cases:
            new_rc, new_v, new_f = run(NEW, d)
            old_rc, old_v, old_f = run(OLD, d)
            if cid == "POSITIVE":
                want = new_rc == 0 and new_v.endswith("=PASS") and old_rc == 0
                label = "positive accepted by both" if want else "positive not accepted"
            else:
                want = (new_rc != 0 and new_v.endswith("=FAIL") and bool(new_f)
                        and old_rc == 0 and old_v.endswith("=PASS"))
                label = ("refused by r88 (" + (new_f[0] if new_f else "no LEG_FAIL") +
                         "), accepted by r87") if want else "NOT refused by r88 or NOT accepted by r87"
            print(f"{'OK' if want else 'CASE_DEVIATION'} {cid}: {label}")
            print(f"  r88: rc={new_rc} {new_v}")
            print(f"  r87: rc={old_rc} {old_v}")
            ok_all = ok_all and want
        forged = [c for c, _ in cases if c != "POSITIVE"]
        print(f"FORGERY_REFUSED={sum(1 for c, d in cases if c != 'POSITIVE' and run(NEW, d)[0] != 0)}/{len(forged)} "
              f"R87_ACCEPTED_FORGERY={sum(1 for c, d in cases if c != 'POSITIVE' and run(OLD, d)[0] == 0)}/{len(forged)}")
        print(f"CONTROLS={'PASS' if ok_all else 'FAIL'}")
        return 0 if ok_all else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
