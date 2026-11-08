#!/usr/bin/env python3
"""Probe trees for the R87MutCounter survivors: show the leg that should have killed each survivor failing."""
import hashlib
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/chousa-r87/R87MutCounter"
L = os.path.join(S, "land")
REPO = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
GATE = os.path.join(L, "corpus/evidence/round87/gate-records-r87.py")
CUR = os.path.join(L, "corpus/evidence/round87/curation-r87.py")
TOOL = os.path.join(L, "tools/gate-records.py")
POS = os.path.join(L, "corpus/evidence/round87/c1-positives.tsv")
P = os.path.join(S, "probes")
OUT = os.path.join(S, "receipts")
os.makedirs(P, exist_ok=True)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(cmd, work):
    os.makedirs(work, exist_ok=True)
    env = dict(os.environ)
    env["TMPDIR"] = work
    p = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout, p.stderr


def edit_copy(src, dst, edits):
    s = open(src, encoding="utf-8").read()
    for old, new in edits:
        assert s.count(old) == 1, (src, old[:60], s.count(old))
        s = s.replace(old, new, 1)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(s)
    return dst


def tree(name):
    d = os.path.join(P, name)
    if os.path.isdir(d):
        shutil.rmtree(d)
    shutil.copytree(L, d, symlinks=True)
    return d


def legfails(out):
    return [ln for ln in out.splitlines() if ln.startswith(("LEG_FAIL", "WRONG_CODE", "NOT_REFUSED"))]


def summary(out):
    keep = [ln for ln in out.splitlines() if ("=" in ln.split(" ")[0] and not ln.startswith("LEG_FAIL"))
            or ln.startswith(("LEG_FAIL", "GATE_RECORDS_R87=", "CURATION_R87=", "WRONG_CODE", "NOT_REFUSED"))]
    return "\n".join(keep)


def main():
    results = []
    ctools = os.path.join(P, "counters")

    # ---- mutant counter copies ----
    def mut_counter(src, mid, old, new):
        d = os.path.join(ctools, mid)
        os.makedirs(d, exist_ok=True)
        shutil.copy2(POS, os.path.join(d, "c1-positives.tsv"))
        mp = os.path.join(d, os.path.basename(src))
        edit_copy(src, mp, [(old, new)])
        return mp

    gate = os.path.join(ctools, "gate-pristine", "gate-records-r87.py")
    edit_copy(GATE, gate, [])
    shutil.copy2(POS, os.path.join(ctools, "gate-pristine", "c1-positives.tsv"))
    cur = os.path.join(ctools, "cur-pristine", "curation-r87.py")
    edit_copy(CUR, cur, [])

    A2 = mut_counter(GATE, "A2", "                    if code in v[1]:", "                    if True:")
    A4 = mut_counter(GATE, "A4", "            ffiles = []", "            fresh_ok = 5\n            ffiles = []")
    A6 = mut_counter(GATE, "A6", "            fresh_files = []", "            p_ok = len(pos)\n            fresh_files = []")
    A8 = mut_counter(GATE, "A8",
                     '            setup_ok = 1 if (p.returncode == 2 and "GATE_RECORDS_ERROR" in p.stderr) else 0',
                     "            setup_ok = 1")
    B1 = mut_counter(CUR, "B1", "floors_ok = all(loc >= fl and loc == tot for _rel, loc, tot, fl in floor_rows)",
                     "floors_ok = all(loc == tot for _rel, loc, tot, fl in floor_rows)")
    B2 = mut_counter(CUR, "B2",
                     "            total += 1\n            cap = capture_text(root, reg, sid)\n"
                     "            if cap is not None and norm(quote) in cap:\n                located += 1",
                     "            cap = capture_text(root, reg, sid)\n"
                     "            if cap is not None and norm(quote) in cap:\n                total += 1\n                located += 1")
    B3 = mut_counter(CUR, "B3", "            if qids and len(resolved) == len(qids) and shares:",
                     "            if qids and len(resolved) == len(qids):")
    B8 = mut_counter(CUR, "B8", "            if qids and len(resolved) == len(qids) and shares:", "            if True:")

    # ---- probe tools ----
    TA2 = edit_copy(TOOL, os.path.join(P, "tools", "A2-wrongcode.py"),
                    [('        if not ok:\n            codes.append("REFETCH")\n        if cap is not None:',
                      '        if not ok:\n            codes.append("WRONGCODE")\n        if cap is not None:')])
    TA4 = edit_copy(TOOL, os.path.join(P, "tools", "A4-freshfail.py"),
                    [("                n += 1\n",
                      "                n += 1\n"
                      "                if os.path.basename(f).startswith(\"fresh\"):\n"
                      "                    print(f\"GATE_RECORD {f}:{i} ? FAIL PARSE\")\n"
                      "                    continue\n")])
    TA8 = edit_copy(TOOL, os.path.join(P, "tools", "A8-norepocheck.py"),
                    [('        p = subprocess.run(["git", "-C", a.repo, "rev-parse", "--git-dir"], capture_output=True, text=True)\n'
                      '        if p.returncode != 0:\n'
                      '            print(f"GATE_RECORDS_ERROR not a git repo: {a.repo!r}", file=sys.stderr)\n'
                      '            return 2\n',
                      "        pass\n")])

    # ---- probe trees ----
    T6 = tree("A6-lesson-line-drift")
    lp = os.path.join(T6, "corpus", "lessons", "round-80.md")
    lines = open(lp, encoding="utf-8").read().split("\n")
    assert lines[18].startswith("GATE-RECORD S199 rev=")
    lines[18] = lines[18] + " "
    open(lp, "w", encoding="utf-8").write("\n".join(lines))

    TB1 = tree("B1-q10-deleted")
    edit_copy(os.path.join(L, "corpus/knowledge/search-transparency-reporting-r84.md"),
              os.path.join(TB1, "corpus/knowledge/search-transparency-reporting-r84.md"),
              [('| Q10 | S023 | "Recommended practice is to describe the date, date/time, or period of time as recommended for the property Date, of which this is a subproperty." |\n', "")])

    TB2 = tree("B2-extra-unlocated-quote")
    edit_copy(os.path.join(L, "corpus/knowledge/search-transparency-reporting-r84.md"),
              os.path.join(TB2, "corpus/knowledge/search-transparency-reporting-r84.md"),
              [('| Q13 | S023 | "Date on which the resource was changed." |\n',
                '| Q13 | S023 | "Date on which the resource was changed." |\n'
                '| Q14 | S214 | "Zyzzyva quokka xylophone trabecular" |\n')])

    TB3 = tree("B3-warrant-repointed")
    edit_copy(os.path.join(L, "corpus/knowledge/provenance-recording-r85.md"),
              os.path.join(TB3, "corpus/knowledge/provenance-recording-r85.md"),
              [("| Recording a derivation's direction | state the transformation from one entity into another | call two unrelated entities a derivation | Q2 (S215) |",
                "| Recording a derivation's direction | state the transformation from one entity into another | call two unrelated entities a derivation | Q7 (S031) |")])

    TB8 = tree("B8-extra-unresolved-warrant")
    edit_copy(os.path.join(L, "corpus/knowledge/provenance-recording-r85.md"),
              os.path.join(TB8, "corpus/knowledge/provenance-recording-r85.md"),
              [("| Recording when content was last reviewed | state the date the content was last reviewed for accuracy and completeness | record a review date for content that was not reviewed for accuracy or completeness | Q7 (S031) |\n",
                "| Recording when content was last reviewed | state the date the content was last reviewed for accuracy and completeness | record a review date for content that was not reviewed for accuracy or completeness | Q7 (S031) |\n"
                "| Recording a test warrant | state the test value for the probe | record the test value without its warrant | Q99 (S215) |\n")])

    cases = [
        # (survivor, probe, counter-cmd, label)
        ("A2-code-credit-blind", "tool:admit refuses with WRONGCODE", [sys.executable, "-B", gate, "--root", L, "--repo", REPO, "--tool", TA2]),
        ("A2-code-credit-blind", "tool:admit refuses with WRONGCODE", [sys.executable, "-B", A2, "--root", L, "--repo", REPO, "--tool", TA2]),
        ("A4-freshok-hardcode", "tool:every fresh record fails", [sys.executable, "-B", gate, "--root", L, "--repo", REPO, "--tool", TA4]),
        ("A4-freshok-hardcode", "tool:every fresh record fails", [sys.executable, "-B", A4, "--root", L, "--repo", REPO, "--tool", TA4]),
        ("A6-pok-hardcode", "tree:corpus/lessons/round-80.md:19 drifts from c1-positives.tsv", [sys.executable, "-B", gate, "--root", T6, "--repo", REPO]),
        ("A6-pok-hardcode", "tree:corpus/lessons/round-80.md:19 drifts from c1-positives.tsv", [sys.executable, "-B", A6, "--root", T6, "--repo", REPO]),
        ("A8-setupok-hardcode", "tool:--repo validation deleted (non-git repo exits 1, not 2)", [sys.executable, "-B", gate, "--root", L, "--repo", REPO, "--tool", TA8]),
        ("A8-setupok-hardcode", "tool:--repo validation deleted (non-git repo exits 1, not 2)", [sys.executable, "-B", A8, "--root", L, "--repo", REPO, "--tool", TA8]),
        ("B1-floor-drop", "tree:Q10 (unreferenced, located) deleted, entry1 12/12", [sys.executable, "-B", cur, "--root", TB1]),
        ("B1-floor-drop", "tree:Q10 (unreferenced, located) deleted, entry1 12/12", [sys.executable, "-B", B1, "--root", TB1]),
        ("B2-total-only-located", "tree:extra unlocated Q14 row added, entry1 13/14", [sys.executable, "-B", cur, "--root", TB2]),
        ("B2-total-only-located", "tree:extra unlocated Q14 row added, entry1 13/14", [sys.executable, "-B", B2, "--root", TB2]),
        ("B3-warrant-drop-shares", "tree:row 'derivation direction' warrant re-pointed Q2->Q7 (resolves, shares no content word)", [sys.executable, "-B", cur, "--root", TB3]),
        ("B3-warrant-drop-shares", "tree:row 'derivation direction' warrant re-pointed Q2->Q7 (resolves, shares no content word)", [sys.executable, "-B", B3, "--root", TB3]),
        ("B8-warrant-dead-detector", "tree:extra decision row with unresolved warrant Q99", [sys.executable, "-B", cur, "--root", TB8]),
        ("B8-warrant-dead-detector", "tree:extra decision row with unresolved warrant Q99", [sys.executable, "-B", B8, "--root", TB8]),
    ]

    for i, (mid, probe, cmd) in enumerate(cases):
        rc, out, err = run(cmd, os.path.join(S, "work", "probe%02d" % i))
        which = "pristine" if ("gate-pristine" in " ".join(cmd) or "cur-pristine" in " ".join(cmd)) else "mutant"
        v = [ln for ln in out.splitlines() if ln.startswith(("GATE_RECORDS_R87=", "CURATION_R87="))]
        body = (f"survivor: {mid}\nprobe: {probe}\nwhich: {which}\n"
                f"cmd: {' '.join(cmd)}\nrc={rc}\nverdict={v[0] if v else 'no-verdict'}\n"
                f"leg-fails:{legfails(out)}\nsummary:\n{summary(out)}\nstderr:\n{err}\n")
        name = f"probe-{mid}-{which}.txt"
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            fh.write(body)
        results.append({"survivor": mid, "probe": probe, "which": which, "rc": rc,
                        "verdict": v[0] if v else "no-verdict", "legfails": legfails(out),
                        "receipt": f"receipts/{name}"})
        print(f"{mid:26s} {which:8s} rc={rc} {v[0] if v else 'no-verdict'} {legfails(out)}")

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
