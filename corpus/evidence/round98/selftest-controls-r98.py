#!/usr/bin/env python3
"""selftest-controls-r98 — round-98 C1 (operability) control battery for `tools/search-rerun.py --selftest`.

Round 97's seat `R97MutantsC1` wrote 37 new one-site mutants of the tool; 25 survived the round-97 self-test and
19 of those were caught by no lane instrument (`.ufo/waves/round-97/w1/R97MutantsC1.md`), among them all five
mutants of the guard and summary code (g01-g05). The round-97 spot-check also routed limit (g): a self-test that
detects mutants by hashing its own source passes every mutant-kill leg. This battery scores the round-98 self-test
against exactly those 37 mutants, read from the committed round-97 probe bytes, through the public CLI as fresh
processes (cwd = a scratch directory under --work, never the lane):

  POSITIVE      `python3 -B <tool> --selftest` exits 0, its last line is `SEARCH_RERUN_SELFTEST: PASS cases=67/67`, and
                it prints the 67 `CASE_IDS` lines `SELFTEST <id> ok` in order
  EXTERNAL_R97  the 37 `R97MutantsC1` mutants (`MUTANTS` of the probe at BASE) applied one at a time; KILLED = exit 1,
                `SEARCH_RERUN_SELFTEST: FAIL` printed, at least one `CASE_IDS` id (or `setup`) in `failed=`, no
                `Traceback` on stderr. Required: every mutant outside `NAMED_SURVIVORS` is KILLED (35 of 37); the two
                named survivors are reported, not required
  DO_NOTHING    the same 37 applied to the tool at BASE (the round-97 landing) under the same rule; the control is
                refused when it fails the EXTERNAL_R97 requirement; its count is printed as BASE_KILLED
  PRIOR         the 34 external mutants of the round-97 battery (its `EXCLUDED`, `SENTINEL`, `RESIDUE` literals and
                the round-96 probe it reads, all at BASE) and the 23 `MUTANTS` of the round-96 battery, still killed
  EQUIVALENT    three mutants that do not change what the tool computes (a trailing comment line, a reworded
                docstring, `lines[-1] == b""` written as `not lines[-1]` on a list of bytes) must SURVIVE: exit 0 and
                the POSITIVE last line. A self-test that kills by noticing any change to its own bytes fails here
  ORACLES       five stand-ins scored by this battery must FAIL it: a constant PASS printer, a hollow self-test,
                an always-FAIL self-test, a guard-blind self-test (canary result forced ok), and a hash-of-self
                self-test (the real tool plus a check of its own sha256 that fails on any byte change)
  KILL_RULE     (F2, `R98MutantsC1` B1) `killed()` is scored on four planted stand-ins: FAIL with exit 0, FAIL with a
                `Traceback`, FAIL naming no known case, and FAIL exit 1 naming `setup`; only the last counts as KILLED
  DIRECT_PATH   (F2, `R98MutantsC1` D01-D04, X3) the tool under test with its canary call forced to fail, and forced to
                raise: each must exit 1, print exactly `SEARCH_RERUN_SELFTEST: FAIL guard-canary failed=g00-guard-canary`
                as its last line and no `Traceback`
  NO_WRITE      the lane's `git status --porcelain` and `git diff` digest at battery start; `--selftest` run with cwd,
                HOME and TMPDIR in an empty directory under --work; the directory stays empty and the lane status and
                diff digest equal the battery-start ones
  REGRESSION    `corpus/evidence/round95/rerun-controls-r95.py --tool <tool>` prints `RERUN_CONTROLS=PASS` and
                `corpus/evidence/round95/mutants-r95.py` prints `MUTANTS_KILLED=10/10` (only with the default tool)

Pinned sizes (F2, `R98MutantsC1` B3, B5): the battery refuses to run (SETUP, exit 2) unless the required set has 35
mutants, the prior sets 34 and 23, the equivalent set 3 and the oracle set 5, so a widened exclusion or a dropped
oracle cannot keep the printed tallies whole.

Named survivors (not required to die; the self-test does not exercise these readers): `u01-verify-return-0`
(`verify`'s exit code; the round-95 battery catches it) and `u05-tree-files-jj` (the disk reader's `.jj` pruning;
no lane instrument catches it).

Usage: python3 -B corpus/evidence/round98/selftest-controls-r98.py --root LANE --work DIR [--tool PATH] [--no-regression]
Prints one CASE line per case, the tallies and `SELFTEST_CONTROLS_R98=PASS|FAIL`. Exit 0 PASS, 1 FAIL, 2 setup.
Writes only under --work (removed at exit). On the lane it runs `git show`, `git status --porcelain` and `git diff`
(git may refresh the index stat cache while doing so); it never writes a lane file itself. It does not see changes
to git-ignored paths.
"""
import argparse
import ast
import hashlib
import os
import shutil
import subprocess
import sys

BASE = "98b8177c1e8b39cdf1167928e4f5d609f6fa81b6"
TOOL = "tools/search-rerun.py"
R97_PROBE = ".ufo/waves/round-97/w1/R97MutantsC1-mutprobe.py.txt"
R97_BATTERY = "corpus/evidence/round97/selftest-controls-r97.py"
R96_BATTERY = "corpus/evidence/round96/selftest-controls-r96.py"
N_CASES = 67
PASS_LINE = f"SEARCH_RERUN_SELFTEST: PASS cases={N_CASES}/{N_CASES}"
NAMED_SURVIVORS = ("u01-verify-return-0", "u05-tree-files-jj")
CASE_IDS = (
    "g00-guard-canary",
    "p01-parse-good", "p02-no-section", "p03-header", "p04-engine", "p05-globstar", "p06-dotdot", "p07-posix-class",
    "p08-backtick", "p09-short-rev", "p10-zero-with-set", "p11-dup-id", "p12-row-after-break", "p13-absolute-glob",
    "r01-signed-hits", "r02-bad-date", "r03-upper-rev", "r04-q0-id", "r05-empty-expression", "r06-empty-segment",
    "r07-trailing-comma", "r16-sep-width", "p14-escaped-pipe", "r08-upper-digest-is-a-path", "m01-lines",
    "m02-dotfile", "m03-segment", "r09-glob-longer", "m04-per-line", "m05-case", "r10-regex-mid-line",
    "r11-regex-non-utf8", "m06-digest", "m07-static-dir", "r12-static-dir-literal", "m08-env-scrub", "r13-env-guards",
    "j01-exact", "j02-count", "j03-set", "j04-digest", "j05-dup-path", "j06-tree-moved", "j07-tree-strict",
    "j08-tree-swap", "j09-zero", "r14-two-codes", "r15-digest-at-rev", "j10-tally",
    "r17-row-no-end-pipe", "r18-heading-suffix", "r19-two-sections", "r20-two-dash-sep", "r21-dash-set-nonzero",
    "r22-dot-segment", "r23-open-backtick", "r24-posix-upper", "r25-digest-byte-order",
    "r26-git-prefix-not-git-underscore", "r27-static-dir-bracket", "r28-at-rev-two-static-dirs",
    "r29-blob-unreadable", "r30-record-not-symlink", "r31-fixed-mid-line", "r32-rev-token", "r33-count-over",
    "r34-git-runs-bounded",
)
EQUIVALENT = {
    "e1-trailing-comment": ("\nif __name__ == \"__main__\":\n    sys.exit(main(sys.argv[1:]))\n",
                            "\nif __name__ == \"__main__\":\n    sys.exit(main(sys.argv[1:]))\n# equivalent mutant\n"),
    "e2-digest-docstring": ("    \"\"\"sha256 of the paths as bytes, byte-sorted,",
                            "    \"\"\"SHA-256 of the paths as bytes, byte-sorted,"),
    "e3-lines-not-empty": ('    if lines and lines[-1] == b"":', "    if lines and not lines[-1]:"),
}
CANARY_CALL = "        guard_ok, guard_detail = _guard_canary()\n"
DIRECT_LINE = "SEARCH_RERUN_SELFTEST: FAIL guard-canary failed=g00-guard-canary"
KILL_RULE_STUBS = {  # name: (stub source, expected killed())
    "fail-exit-0": ("import sys\nprint('SEARCH_RERUN_SELFTEST: FAIL cases=0/1 failed=setup')\nsys.exit(0)\n", False),
    "fail-traceback": ("print('SEARCH_RERUN_SELFTEST: FAIL cases=0/1 failed=setup')\nraise RuntimeError('stub')\n", False),
    "fail-unnamed": ("import sys\nprint('SEARCH_RERUN_SELFTEST: FAIL cases=0/1 failed=no-such-case')\nsys.exit(1)\n", False),
    "fail-named": ("import sys\nprint('SEARCH_RERUN_SELFTEST: FAIL cases=0/1 failed=setup')\nsys.exit(1)\n", True),
}
HASH_ANCHOR = "    try:\n        guard_ok, guard_detail = _guard_canary()\n"
HASH_CHECK = ('    import hashlib as _h\n'
              '    _s = "".join(ln for ln in open(__file__, encoding="utf-8").readlines() if not ln.startswith("    _H = "))\n'
              '    _H = "{h}"\n'
              '    if _h.sha256(_s.encode("utf-8")).hexdigest() != _H:\n'
              '        print("SEARCH_RERUN_SELFTEST: FAIL cases=0/{n} failed=setup")\n'
              '        return 1\n')


def run(cmd, cwd=None, env=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout, p.stderr


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


class Runner:
    def __init__(self, work):
        self.cwd = os.path.join(work, "cwd")
        os.makedirs(self.cwd, exist_ok=True)

    def selftest(self, tool, cwd=None, env=None):
        return run([sys.executable, "-B", tool, "--selftest"], cwd=cwd or self.cwd, env=env)

    def killed(self, tool):
        rc, out, err = self.selftest(tool)
        failed = next((ln.split("failed=")[1] for ln in out.splitlines() if "failed=" in ln), "-")
        named = set(failed.split(",")) & (set(CASE_IDS) | {"setup"})
        dead = rc == 1 and "SEARCH_RERUN_SELFTEST: FAIL" in out and "Traceback" not in err and bool(named)
        return dead, rc, failed, out

    def score(self, src, mutants, work, tag):
        """Apply each (old, new) once to src; returns ({name: killed}, setup_errors)."""
        res, setup = {}, 0
        for name, (old, new) in mutants.items():
            n = src.count(old)
            if n != 1:
                print(f"CASE {tag} {name} SETUP applies {n} times FAIL")
                setup += 1
                continue
            mp = os.path.join(work, f"{tag}-{name}.py")
            with open(mp, "w", encoding="utf-8") as fh:
                fh.write(src.replace(old, new))
            dead, rc, failed, _ = self.killed(mp)
            print(f"CASE {tag} {name} rc={rc} {'KILLED' if dead else 'SURVIVED'} failed={failed}")
            res[name] = dead
        return res, setup


def lane_state(root):
    _, st, _ = run(["git", "-C", root, "status", "--porcelain"])
    _, df, _ = run(["git", "-C", root, "diff"])
    return st, hashlib.sha256(df.encode("utf-8", "surrogateescape")).hexdigest()


def hash_of_self(src):
    """The real tool plus a check of its own sha256 at the top of `selftest()` (R97 routed limit (g))."""
    if src.count(HASH_ANCHOR) != 1:
        return None
    body = src.replace(HASH_ANCHOR, HASH_CHECK.replace("{n}", str(N_CASES)) + HASH_ANCHOR)
    stripped = "".join(ln for ln in body.splitlines(keepends=True) if not ln.startswith("    _H = "))
    return body.replace("{h}", hashlib.sha256(stripped.encode("utf-8")).hexdigest())


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--tool", default=None)
    ap.add_argument("--no-regression", action="store_true")
    a = ap.parse_args(argv)
    root = os.path.realpath(a.root)
    work = os.path.join(os.path.realpath(a.work), "selftest-controls-r98")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    default_tool = a.tool is None
    tool = os.path.join(root, TOOL) if default_tool else os.path.realpath(a.tool)
    rn = Runner(work)
    try:
        start_state = lane_state(root)
        t = {}
        rc, out, _ = rn.selftest(tool)
        lines = out.splitlines()
        case_lines = [ln for ln in lines if ln.startswith("SELFTEST ")]
        lines_ok = [ln.split()[1:3] for ln in case_lines] == [[i, "ok"] for i in CASE_IDS]
        ok = rc == 0 and bool(lines) and lines[-1] == PASS_LINE and lines_ok
        print(f"CASE positive rc={rc} expect=0 last={lines[-1] if lines else ''!r} case_lines={len(case_lines)}"
              f"/{len(CASE_IDS)} named_ok={lines_ok} {'ok' if ok else 'FAIL'}")
        t["POSITIVE"] = (1 if ok else 0, 1)

        reads = {}
        for key, path in (("probe", R97_PROBE), ("base", TOOL), ("r97", R97_BATTERY), ("r96", R96_BATTERY)):
            prc, body, _ = run(["git", "-C", root, "show", f"{BASE}:{path}"])
            if prc:
                print(f"SETUP unreadable at {BASE}: {path} rc={prc}")
                return 2
            reads[key] = body
        r97_lits = {n: literal(reads["r97"], n) for n in ("BASE", "MUTPROBE", "EXCLUDED", "SENTINEL", "RESIDUE")}
        prc, r96_probe, _ = run(["git", "-C", root, "show", f"{r97_lits['BASE']}:{r97_lits['MUTPROBE']}"])
        if prc:
            print(f"SETUP unreadable: {r97_lits['BASE']}:{r97_lits['MUTPROBE']} rc={prc}")
            return 2
        external = {m[0]: (m[1], m[2]) for m in literal(reads["probe"], "MUTANTS")}
        if len(external) != 37 or not set(NAMED_SURVIVORS) <= set(external):
            print(f"SETUP expected 37 R97MutantsC1 mutants including the named survivors, got {len(external)}")
            return 2
        required = sorted(set(external) - set(NAMED_SURVIVORS))
        src = open(tool, encoding="utf-8").read()
        prior = {m[0]: (m[1], m[2]) for m in literal(r96_probe, "MUTANTS") if m[0] not in r97_lits["EXCLUDED"]}
        prior.update(r97_lits["SENTINEL"])
        prior.update(r97_lits["RESIDUE"])
        r96_mutants = literal(reads["r96"], "MUTANTS")
        sizes = (len(required), len(prior), len(r96_mutants), len(EQUIVALENT))
        if sizes != (35, 34, 23, 3):
            print(f"SETUP pinned sizes (required, prior, r96, equivalent) expected (35, 34, 23, 3), got {sizes}")
            return 2

        calib = 0
        for name, (body, want) in KILL_RULE_STUBS.items():
            sp = os.path.join(work, f"calib-{name}.py")
            with open(sp, "w", encoding="utf-8") as fh:
                fh.write(body)
            dead = rn.killed(sp)[0]
            ok = dead == want
            print(f"CASE kill-rule {name} killed={dead} expect={want} {'ok' if ok else 'FAIL'}")
            calib += 1 if ok else 0
        t["KILL_RULE"] = (calib, len(KILL_RULE_STUBS))

        direct = 0
        for name, repl in (("forced-false", "        guard_ok, guard_detail = False, \"forced\"\n"),
                           ("forced-raise", "        guard_ok, guard_detail = (_ for _ in ()).throw(ValueError(\"forced\"))\n")):
            if src.count(CANARY_CALL) != 1:
                print(f"CASE direct-path {name} canary call not found FAIL")
                continue
            dp = os.path.join(work, f"direct-{name}.py")
            with open(dp, "w", encoding="utf-8") as fh:
                fh.write(src.replace(CANARY_CALL, repl))
            drc, dout, derr = rn.selftest(dp)
            dl = dout.splitlines()
            ok = drc == 1 and bool(dl) and dl[-1] == DIRECT_LINE and "Traceback" not in derr
            print(f"CASE direct-path {name} rc={drc} last={dl[-1] if dl else ''!r} {'ok' if ok else 'FAIL'}")
            direct += 1 if ok else 0
        t["DIRECT_PATH"] = (direct, 2)

        res, setup = rn.score(src, external, work, "r97ext")
        k_req = sum(1 for m in required if res.get(m))
        k_all = sum(1 for v in res.values() if v)
        survivors = sorted(m for m, v in res.items() if not v)
        t["KILL_REQUIRED"] = (k_req if not setup else 0, len(required))
        print(f"CASE external-r97 EXTERNAL_R97_KILLED={k_all}/{len(external)} setup={setup} "
              f"survivors={','.join(survivors) or '-'}")

        bres, bsetup = rn.score(reads["base"], external, work, "base")
        bk = sum(1 for v in bres.values() if v)
        breq = sum(1 for m in required if bres.get(m))
        ok = bsetup == 0 and breq < len(required)
        print(f"CASE do-nothing-base BASE_KILLED={bk}/{len(external)} required_killed={breq}/{len(required)}"
              f" setup={bsetup} expect<{len(required)} {'ok' if ok else 'FAIL'}")
        t["DO_NOTHING_REFUSED"] = (1 if ok else 0, 1)

        pres, psetup = rn.score(src, prior, work, "r97prior")
        t["PRIOR_R97_KILLED"] = (sum(pres.values()) if not psetup else 0, len(prior))
        r96res, r96setup = rn.score(src, r96_mutants, work, "r96")
        t["R96_MUTANTS_KILLED"] = (sum(r96res.values()) if not r96setup else 0, len(r96_mutants))

        surv = 0
        for name, (old, new) in EQUIVALENT.items():
            n = src.count(old)
            if n != 1:
                print(f"CASE equivalent {name} SETUP applies {n} times FAIL")
                continue
            mp = os.path.join(work, f"equiv-{name}.py")
            with open(mp, "w", encoding="utf-8") as fh:
                fh.write(src.replace(old, new))
            erc, eout, eerr = rn.selftest(mp)
            elines = eout.splitlines()
            ok = erc == 0 and bool(elines) and elines[-1] == PASS_LINE and "Traceback" not in eerr
            print(f"CASE equivalent {name} rc={erc} last={elines[-1] if elines else ''!r} "
                  f"{'SURVIVED ok' if ok else 'KILLED FAIL'}")
            surv += 1 if ok else 0
        t["EQUIVALENT_SURVIVED"] = (surv, len(EQUIVALENT))

        if default_tool:
            hos = hash_of_self(src)
            stubs = {
                "constant-pass": f"import sys\nprint({PASS_LINE!r})\nsys.exit(0)\n",
                "hollow-selftest": src.replace(HASH_ANCHOR, f"    print({PASS_LINE!r})\n    return 0\n" + HASH_ANCHOR),
                "always-fail": src.replace(HASH_ANCHOR, f"    print('SEARCH_RERUN_SELFTEST: FAIL cases=0/{N_CASES}"
                                                        " failed=setup')\n    return 1\n" + HASH_ANCHOR),
                "guard-blind": src.replace(CANARY_CALL, "        guard_ok, guard_detail = True, \"fail_set=ok pass_set=ok\"\n"),
                "hash-of-self": hos,
            }
            if len(stubs) != 5:
                print(f"SETUP pinned oracle count expected 5, got {len(stubs)}")
                return 2
            rejected = 0
            for name, body in stubs.items():
                if body is None or body == src:
                    print(f"SETUP oracle {name} did not apply")
                    return 2
                sp = os.path.join(work, f"oracle-{name}.py")
                with open(sp, "w", encoding="utf-8") as fh:
                    fh.write(body)
                orc, oout, _ = run([sys.executable, "-B", os.path.abspath(__file__), "--root", root, "--work",
                                    os.path.join(work, "o-" + name), "--tool", sp, "--no-regression"])
                ok = orc == 1 and "SELFTEST_CONTROLS_R98=FAIL" in oout
                tally = next((ln for ln in oout.splitlines() if ln.startswith("POSITIVE=")), "")
                print(f"CASE oracle-{name} battery_rc={orc} expect=1 tally=[{tally}] {'ok' if ok else 'FAIL'}")
                rejected += 1 if ok else 0
            t["ORACLES_REJECTED"] = (rejected, len(stubs))

        empty = os.path.join(work, "empty")
        os.makedirs(empty)
        env = dict(os.environ, HOME=empty, TMPDIR=empty)
        rc, out, _ = rn.selftest(tool, cwd=empty, env=env)
        after = lane_state(root)
        ok = os.listdir(empty) == [] and after == start_state and rc == 0
        print(f"CASE no-write rc={rc} left={os.listdir(empty)} status_same={after[0] == start_state[0]}"
              f" diff_same={after[1] == start_state[1]} {'ok' if ok else 'FAIL'}")
        t["NO_WRITE"] = (1 if ok else 0, 1)

        if default_tool and not a.no_regression:
            reg = 0
            rc, out, _ = run([sys.executable, "-B", os.path.join(root, "corpus/evidence/round95/rerun-controls-r95.py"),
                              "--root", root, "--work", os.path.join(work, "r95"), "--tool", tool], cwd=rn.cwd)
            ok = rc == 0 and "RERUN_CONTROLS=PASS" in out
            print(f"CASE regression-rerun-controls-r95 rc={rc} {'ok' if ok else 'FAIL'}")
            reg += 1 if ok else 0
            rc, out, _ = run([sys.executable, "-B", os.path.join(root, "corpus/evidence/round95/mutants-r95.py"),
                              "--root", root, "--work", os.path.join(work, "m95")], cwd=rn.cwd)
            ok = rc == 0 and "MUTANTS_KILLED=10/10" in out
            print(f"CASE regression-mutants-r95 rc={rc} {'ok' if ok else 'FAIL'}")
            reg += 1 if ok else 0
            t["REGRESSION_R95"] = (reg, 2)

        print(" ".join(f"{k}={x}/{y}" for k, (x, y) in t.items())
              + f" EXTERNAL_R97_KILLED={k_all}/{len(external)} BASE_KILLED={bk}/{len(external)} CASES={N_CASES}")
        passed = all(x == y and y > 0 for x, y in t.values())
        print("SELFTEST_CONTROLS_R98=" + ("PASS" if passed else "FAIL"))
        return 0 if passed else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
