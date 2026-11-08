#!/usr/bin/env python3
"""R94ExecC3Repro independent owner-binding measurement (C3 named limit 1 + both-moved).

Fixtures are copies of the carrier SKILL.md plus its two grounding receipts and the committed
selftest receipt; counters run from the carrier clone so only the fixture's SKILL.md varies.
"""
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/chousa-r94/R94ExecC3Repro"
REPO = os.path.join(S, "repo")
NEW = os.path.join(REPO, "corpus/evidence/round94/skill-tally-r94.py")
OLD = os.path.join(REPO, "corpus/evidence/round93/skill-tally-r93.py")
RECEIPT_REL = "corpus/evidence/round94/controls/selftest-r94.txt"
GROUND = ("corpus/evidence/round25-final-measure.log",
          "corpus/evidence/round34/audit-dispositions.md")
SRC_SKILL = os.path.join(REPO, "SKILL.md")
LINE215 = 640   # 1-based in carrier SKILL.md
LINE283 = 781
HEAD37 = 758

T215 = "`PASS (215 cases, 0 skipped)` under the host UTF-8 locale; original187"
T283 = "  userns exists). Selftest `PASS (283 cases, 0 skipped)` on this host."
ALIAS = "### Round 37 — the claim-pin provenance — carried notes (2026-11-08)"


def make_fixture(name):
    root = os.path.join(S, "fix", name)
    if os.path.isdir(root):
        shutil.rmtree(root)
    for rel in GROUND + (RECEIPT_REL,):
        dst = os.path.join(root, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(os.path.join(REPO, rel), dst)
    return root


def read_lines():
    with open(SRC_SKILL, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    assert lines[LINE215 - 1] == T215, repr(lines[LINE215 - 1])
    assert lines[LINE283 - 1] == T283, repr(lines[LINE283 - 1])
    assert lines[HEAD37 - 1].startswith("### Round 37 — the claim-pin provenance"), lines[HEAD37 - 1]
    return lines


def write_fixture(lines, root):
    with open(os.path.join(root, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def drop(lines, idxs):
    out = []
    for i, ln in enumerate(lines, 1):
        if i not in idxs:
            out.append(ln)
    return out


def insert_before_heading(lines, block, heading_prefix):
    out, done = [], False
    for ln in lines:
        if not done and ln.startswith(heading_prefix):
            out.extend(block)
            done = True
        out.append(ln)
    assert done, heading_prefix
    return out


def run_counter(counter, root, tag):
    receipt = os.path.join(root, RECEIPT_REL)
    p = subprocess.run([sys.executable, "-B", counter, "--root", root, "--selftest", receipt],
                       capture_output=True, text=True)
    out = (p.stdout or "") + (p.stderr or "")
    print(f"=== {tag} rc={p.returncode}")
    for ln in out.splitlines():
        if ("SKILL_TALLY_R9" in ln or "TAIL" in ln or "LEG_FAIL" in ln or "TAIL_OWNER" in ln
                or "HIST_" in ln):
            print(ln)
    return p.returncode, out


def main():
    base = read_lines()

    # P: unmodified copy (construction control)
    root = make_fixture("positive")
    write_fixture(base, root)
    results = {}
    results["P-r93"] = run_counter(OLD, root, "positive r93")
    results["P-r94"] = run_counter(NEW, root, "positive r94")

    # B: BOTH tail tallies moved into ONE other section (Round 36), multiset unchanged
    root = make_fixture("both-moved-into-round36")
    lines = drop(base, {LINE215, LINE283})
    lines = insert_before_heading(lines, [T215, T283], "### Round 37 — the claim-pin provenance")
    # verify multiset of tail tallies unchanged
    tail = lines[575:]
    assert sum(1 for ln in tail if "PASS (215 cases, 0 skipped)" in ln) == 1
    assert sum(1 for ln in tail if "PASS (283 cases, 0 skipped)" in ln) == 1
    write_fixture(lines, root)
    results["B-r93"] = run_counter(OLD, root, "both-moved r93")
    results["B-r94"] = run_counter(NEW, root, "both-moved r94")

    # A: only the 283 tally moved under a heading that merely CONTAINS the declared owner string
    root = make_fixture("alias-heading")
    lines = drop(base, {LINE283})
    lines = insert_before_heading(lines, [ALIAS, "", T283, ""],
                                  "### Round 37 — the claim-pin provenance")
    tail = lines[575:]
    assert sum(1 for ln in tail if "PASS (215 cases, 0 skipped)" in ln) == 1
    assert sum(1 for ln in tail if "PASS (283 cases, 0 skipped)" in ln) == 1
    write_fixture(lines, root)
    results["A-r93"] = run_counter(OLD, root, "alias r93")
    results["A-r94"] = run_counter(NEW, root, "alias r94")

    # X: SWAP — each tally parked under the OTHER declared owner's heading (both owners present)
    root = make_fixture("swapped-owners")
    lines = drop(base, {LINE215, LINE283})
    lines = insert_before_heading(lines, [T283], "### Round28 DERIVED honest-negative status")
    lines = lines + [T215]
    tail = lines[575:]
    assert sum(1 for ln in tail if "PASS (215 cases, 0 skipped)" in ln) == 1
    assert sum(1 for ln in tail if "PASS (283 cases, 0 skipped)" in ln) == 1
    write_fixture(lines, root)
    results["X-r93"] = run_counter(OLD, root, "swapped r93")
    results["X-r94"] = run_counter(NEW, root, "swapped r94")

    # T: an undeclared THIRD tail tally (named limit 4: must be declared in the same commit)
    root = make_fixture("third-tail")
    lines = base + ["`PASS (999 cases, 0 skipped)` undeclared third tail tally"]
    write_fixture(lines, root)
    results["T-r93"] = run_counter(OLD, root, "third-tail r93")
    results["T-r94"] = run_counter(NEW, root, "third-tail r94")

    print("\nSUMMARY")
    for k, (rc, out) in results.items():
        verdict = [ln for ln in out.splitlines() if "SKILL_TALLY_R9" in ln and "=" in ln]
        print(f"{k}: rc={rc} {verdict[-1] if verdict else 'no-verdict'}")


if __name__ == "__main__":
    main()
