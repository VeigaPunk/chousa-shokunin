#!/usr/bin/env python3
"""checklist-run — round-81 C2 (operability) counter, frozen before the SKILL.md edit.

Usage:
    python3 -B corpus/evidence/round81/checklist-run.py --root DIR [--fixtures DIR2] [--timeout S]

DIR is a lane tree (working tree, or `git archive <rev>` extracted to scratch).
DIR2 defaults to this file's own directory + `/checklist-fixtures` (the frozen
fixture pairs), so a candidate tree cannot supply its own fixtures.

Reads DIR/SKILL.md section `## Checklist (executable)`. Top-level items are
lines starting `- [ ]` or `- [x]`; the denominator must be exactly 6 (the base
item count) — any other count exits 2 (an item removed to dodge the counter is
refused, never scored). An item is RUNNABLE iff one of its indented sub-lines
matches `- Run: ` followed by a backticked command.

Discrimination legs (items numbered 1..6 in file order), each run with
`bash -c CMD` in cwd DIR, CMD = the item's first Run command with its first
`<...>` placeholder replaced by the absolute fixture path:
  item 2 — `item2-pass.md` exits 0 and `item2-fail.md` exits 1
           (fail = a negative claim whose sweep names nowhere);
  item 4 — `item4-pass.md` exits 0 and `item4-fail.md` exits 1
           (fail = a kept rejection with no flip-condition);
  item 5 — `item5-fail.tsv` exits 1 and stdout carries a line starting
           `QUOTE_REOPEN_SUMMARY ` with `no_source=1` (an unregistered id is
           refused before any fetch; no network is needed).
A non-runnable item fails its leg. A Run command with no `<...>` placeholder
fails its leg.

Output: one `ITEM n runnable=yes|no leg=pass|fail|n/a detail=...` line per item, then
    CHECKLIST_RUN=<runnable>/6 DISCRIMINATE=<legs passed>/3
    CHECKLIST=PASS|FAIL
Exit 0 iff runnable == 6 and legs == 3; 1 otherwise; 2 usage/denominator.

Limit (stated before data): item 5's leg is a fail leg only (the pass leg
needs a live fetch); a command that prints the summary line and exits 1
without re-opening anything would pass it. Items 1, 3 and 6 are counted
runnable from their Run line only; their outcomes are not exercised here.
"""
import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUN_RE = re.compile(r"^\s+-\s+Run:\s+`([^`]+)`")
ITEM_RE = re.compile(r"^- \[[ xX]\] ")
PH_RE = re.compile(r"<[^<>]+>")


def run(cmd, cwd, timeout):
    env = dict(os.environ)
    try:
        p = subprocess.run(["bash", "-c", cmd], cwd=cwd, capture_output=True, text=True,
                           timeout=timeout, env=env)
        return p.returncode, p.stdout
    except subprocess.TimeoutExpired:
        return 124, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--fixtures", default=os.path.join(HERE, "checklist-fixtures"))
    ap.add_argument("--timeout", type=float, default=180.0)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    fx = os.path.abspath(a.fixtures)
    skill = os.path.join(root, "SKILL.md")
    if not os.path.isfile(skill):
        print("CHECKLIST error: no SKILL.md under --root", file=sys.stderr)
        return 2
    lines = open(skill, encoding="utf-8").read().split("\n")
    try:
        s = next(i for i, l in enumerate(lines) if l.strip() == "## Checklist (executable)")
    except StopIteration:
        print("CHECKLIST error: no '## Checklist (executable)' section", file=sys.stderr)
        return 2
    e = next((i for i in range(s + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    items = []
    for l in lines[s + 1:e]:
        if ITEM_RE.match(l):
            items.append([])
        elif items:
            m = RUN_RE.match(l)
            if m:
                items[-1].append(m.group(1))
    if len(items) != 6:
        print("CHECKLIST error: denominator %d != 6" % len(items), file=sys.stderr)
        return 2
    legs = {
        2: [("item2-pass.md", 0, None), ("item2-fail.md", 1, None)],
        4: [("item4-pass.md", 0, None), ("item4-fail.md", 1, None)],
        5: [("item5-fail.tsv", 1, "no_source=1")],
    }
    for n in legs:
        for f, _, _ in legs[n]:
            if not os.path.isfile(os.path.join(fx, f)):
                print("CHECKLIST error: missing fixture %s" % f, file=sys.stderr)
                return 2
    runnable = 0
    passed = 0
    for idx, runs in enumerate(items, 1):
        r = bool(runs)
        runnable += r
        leg = "n/a"
        detail = ""
        if idx in legs:
            ok = r
            details = []
            if not r:
                details.append("no-run-line")
            elif not PH_RE.search(runs[0]):
                ok = False
                details.append("no-placeholder")
            else:
                for f, want, needle in legs[idx]:
                    cmd = PH_RE.sub(os.path.join(fx, f), runs[0], count=1)
                    rc, out = run(cmd, root, a.timeout)
                    good = rc == want
                    if needle is not None:
                        good = good and any(x.startswith("QUOTE_REOPEN_SUMMARY ") and needle in x
                                            for x in out.splitlines())
                    details.append("%s:rc=%d:%s" % (f, rc, "ok" if good else "bad"))
                    ok = ok and good
            leg = "pass" if ok else "fail"
            passed += ok
            detail = ",".join(details)
        print("ITEM %d runnable=%s leg=%s detail=%s" % (idx, "yes" if r else "no", leg, detail or "-"))
    print("CHECKLIST_RUN=%d/6 DISCRIMINATE=%d/3" % (runnable, passed))
    verdict = runnable == 6 and passed == 3
    print("CHECKLIST=%s" % ("PASS" if verdict else "FAIL"))
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
