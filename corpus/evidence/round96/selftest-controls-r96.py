#!/usr/bin/env python3
"""selftest-controls-r96 — round-96 C1 (operability) control battery for `tools/search-rerun.py --selftest`.

Round-95 spot-check D1: the tool had no self-invocation mode, so its Gates row could not register it as a gate.
This battery scores the new `--selftest` through the public CLI as fresh processes, against expectations written
here before any scored run:

  POSITIVE      `python3 -B <tool> --selftest` exits 0 and prints `SEARCH_RERUN_SELFTEST: PASS cases=32/32`
  DO_NOTHING    the tool at the base revision (git show BASE:tools/search-rerun.py) given `--selftest` exits 2 and
                prints no PASS line — the base tool has no self-test
  MUTANTS       23 one-site mutants of the tool's parse, match, digest and decision code (each replacement applies
                exactly once, or the battery is a setup error); each mutant's `--selftest` must exit 1 and print
                `SEARCH_RERUN_SELFTEST: FAIL` — the self-test can fail on the defects it names. Pre-freeze run 1
                (plans/round-96.md, fix P1): m16-set-dedup survived (j05 then listed one duplicate path in place of a
                second path, so a set comparison also refused it — j05 now lists both real paths plus a duplicate)
                and m34 (drop `g.startswith("/")`) survived because it is equivalent: an absolute glob's first
                segment is empty and the empty-segment check refuses it; m34 is removed, not counted
  ORACLES       three stand-ins scored by this same battery must FAIL it: a constant stub printing the PASS line, a
                hollow self-test (the real tool whose selftest() prints PASS before testing anything), and an
                always-FAIL self-test (blanket refusal is not a gain)
  NO_WRITE      `--selftest` run with cwd and HOME in an empty directory under --work leaves that directory empty
                and the lane's `git status --porcelain` unchanged
  REGRESSION    the round-95 instruments still pass on the tool under test: `rerun-controls-r95.py` prints
                `RERUN_CONTROLS=PASS` and `mutants-r95.py` prints `MUTANTS_KILLED=10/10` (only with the default tool)

Usage: python3 -B corpus/evidence/round96/selftest-controls-r96.py --root LANE --work DIR [--tool PATH] [--no-regression]
Prints one CASE line per case, the tallies and `SELFTEST_CONTROLS=PASS|FAIL`. Exit 0 PASS, 1 FAIL, 2 setup.
Writes only under --work (removed at exit). Read-only on the lane (`git show`, `git status`).
"""
import argparse
import os
import shutil
import subprocess
import sys

BASE = "bbf64970b6c73ca64bcc5f6de2f33b0550459813"
TOOL = "tools/search-rerun.py"
N_CASES = 32
PASS_LINE = f"SEARCH_RERUN_SELFTEST: PASS cases={N_CASES}/{N_CASES}"

MUTANTS = {
    # the ten round-95 survivor rebuilds (corpus/evidence/round95/mutants-r95.py), same sites
    "m10-whole-file": ("    for line in lines_of(data):\n", "    for line in [data]:\n"),
    "m11-ci-fixed": ('            if r["needle"] in line:', '            if r["needle"].lower() in line.lower():'),
    "m13-hits-len-set": ('        if len(at_rev) != r["n"]:',
                         '        if len(at_rev) != (len(r["set"]) if "set" in r else r["n"]):'),
    "m14-revok-mask": ('        rev_ok += 0 if ("COUNT_DRIFT" in codes or "SET_DRIFT" in codes) else 1',
                       "        rev_ok += 1"),
    "m15-tree-count": ("        changed = at_tree != at_rev", "        changed = len(at_tree) != len(at_rev)"),
    "m16-set-dedup": ('        elif sorted(r["set"]) != at_rev:', '        elif set(r["set"]) != set(at_rev):'),
    "m17-fnmatch": ("        if len(pats) == len(segs) and all(seg_match(s, p) for s, p in zip(segs, pats)):",
                    '        if __import__("fnmatch").fnmatchcase(path, g):'),
    "m18-phantom-line": ("    if lines and lines[-1] == b\"\":\n        lines.pop()\n", ""),
    "m19-dotglob": ('    if name.startswith(".") and not pat.startswith("."):\n        return False\n', ""),
    "m20-no-env-scrub": ('    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}',
                         "    env = dict(os.environ)"),
    # round-96 sites
    "m21-no-count-drift": ('            codes.append("COUNT_DRIFT")', "            pass"),
    "m22-no-digest-compare": ('            if digest(at_rev) != r["digest"]:', "            if False:"),
    "m23-strict-ignored": ('        bad = [c for c in codes if c != "TREE_CHANGED" or strict]',
                           '        bad = [c for c in codes if c != "TREE_CHANGED"]'),
    "m24-tree-always-bad": ('        bad = [c for c in codes if c != "TREE_CHANGED" or strict]',
                            "        bad = list(codes)"),
    "m25-digest-unsorted": ('    keys = sorted(p.encode("utf-8", "surrogateescape") for p in paths)',
                            '    keys = [p.encode("utf-8", "surrogateescape") for p in paths]'),
    "m26-globstar-allowed": ('            if "**" in g:', "            if False:"),
    "m27-dotdot-allowed": ('".." in parts or ', ""),
    "m28-posix-allowed": ('            if POSIX_CLASS_RE.search(r["expr"]):', "            if False:"),
    "m29-zero-with-set": ('            if hs != "-":', "            if False:"),
    "m30-dup-id": ('if not ID_RE.match(r["id"]) or r["id"] in seen:', 'if not ID_RE.match(r["id"]):'),
    "m31-pipe-literal": ('return [c.strip().replace("\\\\|", "|") for c in SPLIT_RE.split(s[1:-1])]',
                         "return [c.strip() for c in SPLIT_RE.split(s[1:-1])]"),
    "m32-static-dir-skip": ("            break\n        out.append(s)", "            continue\n        out.append(s)"),
    "m33-revok-count-only": ('        rev_ok += 0 if ("COUNT_DRIFT" in codes or "SET_DRIFT" in codes) else 1',
                             '        rev_ok += 0 if "COUNT_DRIFT" in codes else 1'),
}


def run(cmd, cwd=None, env=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout, p.stderr


def selftest(tool, cwd=None, env=None):
    return run([sys.executable, "-B", tool, "--selftest"], cwd=cwd, env=env)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--tool", default=None)
    ap.add_argument("--no-regression", action="store_true")
    a = ap.parse_args(argv)
    root = os.path.realpath(a.root)
    work = os.path.join(os.path.realpath(a.work), "selftest-controls-r96")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    default_tool = a.tool is None
    tool = os.path.join(root, TOOL) if default_tool else os.path.realpath(a.tool)
    try:
        t = {}
        rc, out, _ = selftest(tool)
        ok = rc == 0 and PASS_LINE in out.splitlines()
        print(f"CASE positive rc={rc} expect=0 {'ok' if ok else 'FAIL'}")
        t["POSITIVE"] = (1 if ok else 0, 1)

        brc, bsrc, _ = run(["git", "-C", root, "show", f"{BASE}:{TOOL}"])
        if brc != 0:
            print(f"SETUP base tool unreadable at {BASE}")
            return 2
        bp = os.path.join(work, "base-tool.py")
        open(bp, "w", encoding="utf-8").write(bsrc)
        rc, out, _ = selftest(bp)
        ok = rc == 2 and "SEARCH_RERUN_SELFTEST: PASS" not in out
        print(f"CASE do-nothing-base rc={rc} expect=2 {'ok' if ok else 'FAIL'}")
        t["DO_NOTHING_REFUSED"] = (1 if ok else 0, 1)

        src = open(tool, encoding="utf-8").read()
        killed = 0
        for name, (old, new) in MUTANTS.items():
            n = src.count(old)
            if n != 1:
                print(f"CASE mutant {name} SETUP applies {n} times FAIL")
                continue
            mp = os.path.join(work, name + ".py")
            open(mp, "w", encoding="utf-8").write(src.replace(old, new))
            rc, out, _ = selftest(mp)
            dead = rc == 1 and "SEARCH_RERUN_SELFTEST: FAIL" in out
            failed = next((ln.split("failed=")[1] for ln in out.splitlines() if "failed=" in ln), "-")
            print(f"CASE mutant {name} rc={rc} {'KILLED' if dead else 'SURVIVED'} failed={failed}")
            killed += 1 if dead else 0
        t["MUTANTS_KILLED"] = (killed, len(MUTANTS))

        if default_tool:
            stubs = {
                "constant-pass": f"import sys\nprint({PASS_LINE!r})\nsys.exit(0)\n",
                "hollow-selftest": src.replace("    good = ST_HEAD + st_row()\n",
                                               f"    print({PASS_LINE!r})\n    return 0\n    good = ST_HEAD + st_row()\n"),
                "always-fail": src.replace("    good = ST_HEAD + st_row()\n",
                                           "    print('SEARCH_RERUN_SELFTEST: FAIL cases=0/32')\n    return 1\n"
                                           "    good = ST_HEAD + st_row()\n"),
            }
            rejected = 0
            for name, body in stubs.items():
                if body == src:
                    print(f"SETUP oracle {name} did not apply")
                    return 2
                sp = os.path.join(work, f"oracle-{name}.py")
                open(sp, "w", encoding="utf-8").write(body)
                orc, oout, _ = run([sys.executable, "-B", os.path.abspath(__file__), "--root", root, "--work",
                                    os.path.join(work, "o-" + name), "--tool", sp, "--no-regression"])
                ok = orc == 1 and "SELFTEST_CONTROLS=FAIL" in oout
                tally = next((ln for ln in oout.splitlines() if ln.startswith("POSITIVE=")), "")
                print(f"CASE oracle-{name} battery_rc={orc} expect=1 tally=[{tally}] {'ok' if ok else 'FAIL'}")
                rejected += 1 if ok else 0
            t["ORACLES_REJECTED"] = (rejected, len(stubs))

        empty = os.path.join(work, "empty")
        os.makedirs(empty)
        _, before, _ = run(["git", "-C", root, "status", "--porcelain"])
        env = dict(os.environ, HOME=empty, TMPDIR=empty)
        rc, out, _ = selftest(tool, cwd=empty, env=env)
        _, after, _ = run(["git", "-C", root, "status", "--porcelain"])
        ok = os.listdir(empty) == [] and before == after
        print(f"CASE no-write rc={rc} left={os.listdir(empty)} lane_status_same={before == after} {'ok' if ok else 'FAIL'}")
        t["NO_WRITE"] = (1 if ok else 0, 1)

        if default_tool and not a.no_regression:
            reg = 0
            rc, out, _ = run([sys.executable, "-B", os.path.join(root, "corpus/evidence/round95/rerun-controls-r95.py"),
                              "--root", root, "--work", os.path.join(work, "r95"), "--tool", tool])
            ok = rc == 0 and "RERUN_CONTROLS=PASS" in out
            print(f"CASE regression-rerun-controls-r95 rc={rc} {'ok' if ok else 'FAIL'}")
            reg += 1 if ok else 0
            rc, out, _ = run([sys.executable, "-B", os.path.join(root, "corpus/evidence/round95/mutants-r95.py"),
                              "--root", root, "--work", os.path.join(work, "m95")])
            ok = rc == 0 and "MUTANTS_KILLED=10/10" in out
            print(f"CASE regression-mutants-r95 rc={rc} {'ok' if ok else 'FAIL'}")
            reg += 1 if ok else 0
            t["REGRESSION_R95"] = (reg, 2)

        print(" ".join(f"{k}={x}/{y}" for k, (x, y) in t.items()) + f" CASES={N_CASES}")
        passed = all(x == y and y > 0 for x, y in t.values())
        print("SELFTEST_CONTROLS=" + ("PASS" if passed else "FAIL"))
        return 0 if passed else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
