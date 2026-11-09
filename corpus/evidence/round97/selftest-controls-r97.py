#!/usr/bin/env python3
"""selftest-controls-r97 — round-97 C1 (operability) control battery for `tools/search-rerun.py --selftest`.

Round 96 left the self-test's grip measured by a non-author seat: `R96MutantsC1` wrote 30 one-site mutants of the
tool, and 19 of them survived `--selftest` (classes A, B, C of `.ufo/waves/round-96/w1/R96MutantsC1.md`);
`R96SentinelC1` wrote two more that survived it (F1: `GIT_NO_REPLACE_OBJECTS` dropped from `git_env`; F7: only
`GIT_DIR` scrubbed). This battery scores the round-97 self-test against exactly those mutants, read from the
committed round-96 bytes (never retyped here), through the public CLI as fresh processes:

  POSITIVE      `python3 -B <tool> --selftest` exits 0 and its last line is `SEARCH_RERUN_SELFTEST: PASS cases=47/47`
  EXTERNAL      the 30 external mutants (below) applied one at a time to the tool under test; each must exit 1,
                print `SEARCH_RERUN_SELFTEST: FAIL` and print no `Traceback` (a crash is not a detection)
  DO_NOTHING    the same 30 mutants applied to the tool at BASE (the round-96 landing, before any round-97 work),
                scored by the same rule; the do-nothing control is refused when it kills fewer than 30 — its count
                is printed as BASE_KILLED
  R96_MUTANTS   the 23 round-96 battery mutants (`MUTANTS` of corpus/evidence/round96/selftest-controls-r96.py at
                BASE) still killed on the tool under test, by the same rule
  ORACLES       three stand-ins scored by this battery must FAIL it: a constant PASS printer, a hollow self-test,
                an always-FAIL self-test
  NO_WRITE      the lane's `git status --porcelain` and `git diff` digest are taken at battery start, before any
                scored run; `--selftest` is then run with cwd, HOME and TMPDIR in an empty directory under --work;
                the directory must stay empty and the lane status and diff digest must equal the battery-start ones
  REGRESSION    `corpus/evidence/round95/rerun-controls-r95.py --tool <tool>` prints `RERUN_CONTROLS=PASS` and
                `corpus/evidence/round95/mutants-r95.py` prints `MUTANTS_KILLED=10/10` (only with the default tool)

The 30 external mutants: the 29 `R96MutantsC1` mutants that applied in round 96 (`n08` applied 0 times there and
is not counted) minus `n30` (the seat's own verdict: equivalent, since the header check already fixes the
separator width) — 28 — plus `s1-no-replace-objects` and `s2-partial-scrub`, transcribed from the one edited
line in `R96SentinelC1-replace-refs-false-clean.txt` (F1) and `R96SentinelC1-partial-git-scrub.txt` (F7).

Usage: python3 -B corpus/evidence/round97/selftest-controls-r97.py --root LANE --work DIR [--tool PATH] [--no-regression]
Prints one CASE line per case, the tallies and `SELFTEST_CONTROLS_R97=PASS|FAIL`. Exit 0 PASS, 1 FAIL, 2 setup.
Writes only under --work (removed at exit). Read-only on the lane (`git show`, `git status`, `git diff`).
"""
import argparse
import ast
import hashlib
import os
import shutil
import subprocess
import sys

BASE = "c8087ac529003e667505bcc624f9a7bde0cffbce"
TOOL = "tools/search-rerun.py"
MUTPROBE = ".ufo/waves/round-96/w1/R96MutantsC1-mutprobe.py.txt"
R96_BATTERY = "corpus/evidence/round96/selftest-controls-r96.py"
N_CASES = 47
PASS_LINE = f"SEARCH_RERUN_SELFTEST: PASS cases={N_CASES}/{N_CASES}"
EXCLUDED = {"n08-hits-regex-sign": "applied 0 times in round 96 (R96MutantsC1.md:34)",
            "n30-sep-row-lenient": "equivalent (R96MutantsC1.md:154-159)"}
SENTINEL = {
    "s1-no-replace-objects": (
        '    env.update({"GIT_NO_REPLACE_OBJECTS": "1", "GIT_NO_LAZY_FETCH": "1", "GIT_TERMINAL_PROMPT": "0"})\n',
        '    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_TERMINAL_PROMPT": "0"})\n'),
    "s2-partial-scrub": (
        '    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}\n',
        '    env = {k: v for k, v in os.environ.items() if k != "GIT_DIR"}\n'),
}


def run(cmd, cwd=None, env=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout, p.stderr


def selftest(tool, cwd=None, env=None):
    return run([sys.executable, "-B", tool, "--selftest"], cwd=cwd, env=env)

def _lit(node):
    """ast.literal_eval plus `str + str` (the round-96 probe writes n08's old string as `r'...' + "\\n"`)."""
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = _lit(node.left), _lit(node.right)
        if isinstance(left, str) and isinstance(right, str):
            return left + right
        raise ValueError("non-string concatenation")
    if isinstance(node, (ast.List, ast.Tuple)):
        items = [_lit(e) for e in node.elts]
        return items if isinstance(node, ast.List) else tuple(items)
    if isinstance(node, ast.Dict):
        return {_lit(k): _lit(v) for k, v in zip(node.keys, node.values)}
    return ast.literal_eval(node)


def literal(src, name):
    """The literal value of the top-level assignment `name = ...` in `src` (no code of `src` is executed)."""
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return _lit(node.value)
    raise KeyError(name)


def killed(tool_path):
    rc, out, err = selftest(tool_path)
    dead = rc == 1 and "SEARCH_RERUN_SELFTEST: FAIL" in out and "Traceback" not in err
    failed = next((ln.split("failed=")[1] for ln in out.splitlines() if "failed=" in ln), "-")
    return dead, rc, failed


def score(src, mutants, work, tag):
    """Apply each (old, new) once to src, score with `killed`; returns (killed, total, setup_errors)."""
    k, setup = 0, 0
    for name, (old, new) in mutants.items():
        n = src.count(old)
        if n != 1:
            print(f"CASE {tag} {name} SETUP applies {n} times FAIL")
            setup += 1
            continue
        mp = os.path.join(work, f"{tag}-{name}.py")
        open(mp, "w", encoding="utf-8").write(src.replace(old, new))
        dead, rc, failed = killed(mp)
        print(f"CASE {tag} {name} rc={rc} {'KILLED' if dead else 'SURVIVED'} failed={failed}")
        k += 1 if dead else 0
    return k, len(mutants), setup


def lane_state(root):
    _, st, _ = run(["git", "-C", root, "status", "--porcelain"])
    _, df, _ = run(["git", "-C", root, "diff"])
    return st, hashlib.sha256(df.encode("utf-8", "surrogateescape")).hexdigest()


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--tool", default=None)
    ap.add_argument("--no-regression", action="store_true")
    a = ap.parse_args(argv)
    root = os.path.realpath(a.root)
    work = os.path.join(os.path.realpath(a.work), "selftest-controls-r97")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    default_tool = a.tool is None
    tool = os.path.join(root, TOOL) if default_tool else os.path.realpath(a.tool)
    try:
        start_state = lane_state(root)
        t = {}
        rc, out, _ = selftest(tool)
        lines = out.splitlines()
        ok = rc == 0 and bool(lines) and lines[-1] == PASS_LINE
        print(f"CASE positive rc={rc} expect=0 last={lines[-1] if lines else ''!r} {'ok' if ok else 'FAIL'}")
        t["POSITIVE"] = (1 if ok else 0, 1)

        prc, probe, _ = run(["git", "-C", root, "show", f"{BASE}:{MUTPROBE}"])
        brc, base_src, _ = run(["git", "-C", root, "show", f"{BASE}:{TOOL}"])
        rrc, r96, _ = run(["git", "-C", root, "show", f"{BASE}:{R96_BATTERY}"])
        if prc or brc or rrc:
            print(f"SETUP unreadable at {BASE}: mutprobe={prc} tool={brc} r96-battery={rrc}")
            return 2
        external = {m[0]: (m[1], m[2]) for m in literal(probe, "MUTANTS") if m[0] not in EXCLUDED}
        if len(external) != 28:
            print(f"SETUP expected 28 R96MutantsC1 mutants after exclusions, got {len(external)}")
            return 2
        external.update(SENTINEL)
        src = open(tool, encoding="utf-8").read()

        k, n, setup = score(src, external, work, "external")
        t["EXTERNAL_KILLED"] = (k if not setup else 0, n)

        bk, bn, bsetup = score(base_src, external, work, "base")
        ok = bsetup == 0 and bk < bn
        print(f"CASE do-nothing-base BASE_KILLED={bk}/{bn} setup={bsetup} expect<{bn} {'ok' if ok else 'FAIL'}")
        t["DO_NOTHING_REFUSED"] = (1 if ok else 0, 1)

        k96, n96, s96 = score(src, literal(r96, "MUTANTS"), work, "r96")
        t["R96_MUTANTS_KILLED"] = (k96 if not s96 else 0, n96)

        if default_tool:
            stubs = {
                "constant-pass": f"import sys\nprint({PASS_LINE!r})\nsys.exit(0)\n",
                "hollow-selftest": src.replace("    good = ST_HEAD + st_row()\n",
                                               f"    print({PASS_LINE!r})\n    return 0\n    good = ST_HEAD + st_row()\n"),
                "always-fail": src.replace("    good = ST_HEAD + st_row()\n",
                                           f"    print('SEARCH_RERUN_SELFTEST: FAIL cases=0/{N_CASES}')\n    return 1\n"
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
                ok = orc == 1 and "SELFTEST_CONTROLS_R97=FAIL" in oout
                tally = next((ln for ln in oout.splitlines() if ln.startswith("POSITIVE=")), "")
                print(f"CASE oracle-{name} battery_rc={orc} expect=1 tally=[{tally}] {'ok' if ok else 'FAIL'}")
                rejected += 1 if ok else 0
            t["ORACLES_REJECTED"] = (rejected, len(stubs))

        empty = os.path.join(work, "empty")
        os.makedirs(empty)
        env = dict(os.environ, HOME=empty, TMPDIR=empty)
        rc, out, _ = selftest(tool, cwd=empty, env=env)
        after = lane_state(root)
        ok = os.listdir(empty) == [] and after == start_state and rc == 0
        print(f"CASE no-write rc={rc} left={os.listdir(empty)} status_same={after[0] == start_state[0]}"
              f" diff_same={after[1] == start_state[1]} {'ok' if ok else 'FAIL'}")
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

        print(" ".join(f"{k}={x}/{y}" for k, (x, y) in t.items()) + f" BASE_KILLED={bk}/{bn} CASES={N_CASES}")
        passed = all(x == y and y > 0 for x, y in t.values())
        print("SELFTEST_CONTROLS_R97=" + ("PASS" if passed else "FAIL"))
        return 0 if passed else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
