#!/usr/bin/env python3
"""curation-r87-controls — the round-87 C2 forgery control battery.

Builds single-cell mirrors of the tree and requires, for every round-86 routed forgery, that
  * the round-87 counter REFUSES it (a FAIL verdict, naming the leg), and
  * the round-86 counter ACCEPTS it (the do-nothing evidence: the forgery was a pass before this round).
The positive (unmodified) mirror must be accepted by both, so the repair is not a blanket refusal.

Cases (`corpus/lessons/round-86-verifier-spotcheck.md` §Routed defect 4 and 5):
  E5b-delete-one-row     the r85 entry's Q7 row deleted (r86 scored `QUOTES_LOCATED=19/19 PASS`)
  E5c2-keep-two-rows     every located-quote row but Q13 (r84) and Q7 (r85) deleted (r86 scored `2/2 PASS`)
  E6-warrant-unlinked    the r84 row "Recording when a resource changed" warrant re-pointed from Q13 to Q10
  T-teaches-contrast     S031's `teaches` gains a contrast against modification dates its capture does not contain

Usage: python3 -B corpus/evidence/round87/curation-r87-controls.py --root DIR --work DIR
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
NEW = os.path.join(HERE, "curation-r87.py")
OLD = os.path.join(HERE, "..", "round86", "curation-r86.py")
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
    verdict = [l for l in lines if re.match(r"^(CURATION_R\d\d=|CURATION_R87=)", l)]
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
    tmp = tempfile.mkdtemp(prefix="cur87-", dir=work)
    ok_all = True
    try:
        cases = []

        def add(cid, mutator):
            d = mirror(root, os.path.join(tmp, cid))
            mutator(d)
            cases.append((cid, d))

        add("POSITIVE", lambda d: None)

        def e5b(d):
            p = os.path.join(d, ENTRY_B)
            out = [ln for ln in open(p, encoding="utf-8", errors="replace").read().split("\n")
                   if not re.match(r"^\s*\|\s*Q7\s*\|", ln)]
            open(p, "w", encoding="utf-8").write("\n".join(out))

        add("E5b-delete-one-row", e5b)

        def e5c2(d):
            drop_quote_rows(os.path.join(d, ENTRY_A), {"Q13"})
            drop_quote_rows(os.path.join(d, ENTRY_B), {"Q7"})

        add("E5c2-keep-two-rows", e5c2)

        def e6(d):
            p = os.path.join(d, ENTRY_A)
            s = open(p, encoding="utf-8", errors="replace").read()
            n = s.replace("| Q13 (S023) |", "| Q10 (S023) |", 1)
            if n == s:
                raise SystemExit("SETUP_MISS e6: warrant cell not found")
            open(p, "w", encoding="utf-8").write(n)

        add("E6-warrant-unlinked", e6)

        def t(d):
            p = os.path.join(d, "corpus", "SOURCES.md")
            out = []
            hit = False
            for ln in open(p, encoding="utf-8", errors="replace").read().split("\n"):
                if ln.startswith("| S031 |"):
                    ln = ln.replace("no comparison to other date properties claimed",
                                    "separate from modification dates", 1)
                    hit = "separate from modification dates" in ln
                out.append(ln)
            if not hit:
                raise SystemExit("SETUP_MISS t: S031 teaches cell not found")
            open(p, "w", encoding="utf-8").write("\n".join(out))

        add("T-teaches-contrast", t)

        for cid, d in cases:
            new_rc, new_v, new_f = run(NEW, d)
            old_rc, old_v, old_f = run(OLD, d)
            if cid == "POSITIVE":
                want = new_rc == 0 and new_v.endswith("=PASS") and old_rc == 0
                label = "positive accepted by both" if want else "positive not accepted"
            else:
                want = (new_rc != 0 and new_v.endswith("=FAIL") and bool(new_f)
                        and old_rc == 0 and old_v.endswith("=PASS"))
                label = ("refused by r87 (" + (new_f[0] if new_f else "no LEG_FAIL") +
                         "), accepted by r86") if want else "NOT refused by r87 or NOT accepted by r86"
            print(f"{'OK' if want else 'CASE_DEVIATION'} {cid}: {label}")
            print(f"  r87: rc={new_rc} {new_v}")
            print(f"  r86: rc={old_rc} {old_v}")
            ok_all = ok_all and want
        forged = [c for c, _ in cases if c != "POSITIVE"]
        print(f"FORGERY_REFUSED={sum(1 for c, d in cases if c != 'POSITIVE' and run(NEW, d)[0] != 0)}/{len(forged)} "
              f"R86_ACCEPTED_FORGERY={sum(1 for c, d in cases if c != 'POSITIVE' and run(OLD, d)[0] == 0)}/{len(forged)}")
        print(f"CONTROLS={'PASS' if ok_all else 'FAIL'}")
        return 0 if ok_all else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
