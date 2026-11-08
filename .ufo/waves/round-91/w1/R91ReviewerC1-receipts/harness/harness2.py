#!/usr/bin/env python3
"""R91ReviewerC1 fixture harness 2b: clause-1 ordering, PASS/EXACT_OK gating, clause-5 script identity."""
import hashlib
import importlib.util
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/chousa-r91/R91ReviewerC1"
REPO = os.path.join(S, "repo")
DRV = os.path.join(REPO, "corpus/evidence/round91/control-driver-r91.py")
OUT = []
FIX = os.path.join(S, "fx2")
REVX = "a" * 40


def say(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    OUT.append(line)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def write(p, text, mode=None):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)
    if mode is not None:
        os.chmod(p, mode)


def git(root, *args):
    p = subprocess.run(["git", "-C", root] + list(args), capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"git {args} failed: {p.stderr}")
    return p.stdout.strip()


def commit(root, msg):
    git(root, "add", "-A")
    git(root, "-c", "user.email=r91@fixture", "-c", "user.name=r91", "commit", "-qm", msg)
    return git(root, "rev-parse", "HEAD")


def run_verify(root, tag, rev, receipts_rev=None, repo=False):
    work = os.path.join(S, "work2", tag)
    shutil.rmtree(work, ignore_errors=True)
    drv = os.path.join(root, "corpus/evidence/round91/control-driver-r91.py")
    exp = os.path.join(root, "corpus/evidence/round91/controls/expected.tsv")
    args = [sys.executable, "-B", drv, "verify", "--root", ".", "--work", work, "--rev", rev,
            "--expected", exp,
            "--receipts", os.path.join(root, "corpus/evidence/round91/controls/receipts"),
            "--pins", os.path.join(root, "instrument-pins.txt")]
    if repo:
        args += ["--repo", ".", "--receipts-rev", receipts_rev]
    p = subprocess.run(args, capture_output=True, text=True, cwd=root)
    out = (p.stdout or "") + (p.stderr or "")
    say(f"\n### {tag}: exit={p.returncode}")
    for ln in out.strip().splitlines()[-9:]:
        say("   ", ln)
    return p.returncode, out


def base_tree(root, restore):
    drvrel = "corpus/evidence/round91/control-driver-r91.py"
    exprel = "corpus/evidence/round91/controls/expected.tsv"
    rec = "corpus/evidence/round91/controls/receipts"
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    write(os.path.join(root, drvrel), open(DRV, encoding="utf-8").read())
    write(os.path.join(root, "r1.sh"),
          "#!/bin/sh\nprintf 'A=1\\n'\n"
          "rev=$(sed -n 's/^# computed_against=//p' corpus/evidence/round91/controls/receipts/a.txt)\n"
          "printf '# case=b\\n# expected_exit=0\\n# exit=0\\n# computed_against=%s\\nB=1\\n' "
          "\"$rev\" > corpus/evidence/round91/controls/receipts/b.txt\n", 0o755)
    tail = "cp b_committed.dat corpus/evidence/round91/controls/receipts/b.txt\n" if restore else ""
    write(os.path.join(root, "r2.sh"), "#!/bin/sh\nprintf 'B=1\\n'\n" + tail, 0o755)
    exp = ("case\tinstrument\texpected_exit\trequired\tpredicates\tsource_of_expectation\n"
           "a\tbash @ROOT@/r1.sh\t0\tA=1\t-\tthe overwriter row\n"
           "b\tbash @ROOT@/r2.sh\t0\tB=1\t-\tthe overwritten row\n")
    write(os.path.join(root, exprel), exp)
    lines = ""
    for rel in ["r1.sh", "r2.sh", exprel]:
        lines += f"{sha(os.path.join(root, rel))}  {rel}\n"
    write(os.path.join(root, "instrument-pins.txt"), lines)
    git(root, "init", "-q")
    top = git(root, "rev-parse", "--show-toplevel")
    say("    git toplevel check:", top, "==", root, "->", top == root)
    x = commit(root, "X: driver, expected, scripts, pins")
    a = f"# case=a\n# expected_exit=0\n# exit=0\n# computed_against={x}\nA=1\n"
    b = f"# case=b\n# expected_exit=0\n# exit=0\n# computed_against={x}\nB=0\nmarker=committed\n"
    write(os.path.join(root, rec, "a.txt"), a)
    write(os.path.join(root, rec, "b.txt"), b)
    write(os.path.join(root, "b_committed.dat"), b)
    y = commit(root, "Y: receipts")
    say("    X =", x, " Y =", y)
    say("    committed b.txt:", repr(b))
    return x, y


def copy_of(src, dst):
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst, symlinks=True)


def main():
    shutil.rmtree(FIX, ignore_errors=True)
    os.makedirs(FIX)

    # A10a: with --repo; r2 restores the committed bytes after row b was read
    root = os.path.join(FIX, "restore")
    x, y = base_tree(root, restore=True)
    run_verify(root, "A10a-with-repo-restore", x, y, repo=True)
    say("    final b.txt equals committed bytes:",
        open(os.path.join(root, "corpus/evidence/round91/controls/receipts/b.txt"), "rb").read()
        == open(os.path.join(root, "b_committed.dat"), "rb").read())

    # A10b/A10c: no restore; with --repo must drift, without --repo is accepted (copies)
    root2 = os.path.join(FIX, "norestore")
    x2, y2 = base_tree(root2, restore=False)
    cp = os.path.join(FIX, "norestore-with-repo")
    copy_of(root2, cp)
    run_verify(cp, "A10b-with-repo-norestore", x2, y2, repo=True)
    say("    cp b.txt after with-repo run says B=",
        [ln for ln in open(os.path.join(cp, "corpus/evidence/round91/controls/receipts/b.txt")).read().splitlines() if ln.startswith("B=")])
    cp2 = os.path.join(FIX, "norestore-no-repo")
    copy_of(root2, cp2)
    run_verify(cp2, "A10c-without-repo-norestore", x2, repo=False)
    say("    cp2 b.txt after without-repo run says B=",
        [ln for ln in open(os.path.join(cp2, "corpus/evidence/round91/controls/receipts/b.txt")).read().splitlines() if ln.startswith("B=")])

    # A15: exact-gap — PASS with EXACT_OK < rows (no --repo)
    root5 = os.path.join(FIX, "exact-gap")
    shutil.rmtree(root5, ignore_errors=True)
    os.makedirs(root5)
    rec5 = os.path.join(root5, "corpus/evidence/round91/controls/receipts")
    os.makedirs(rec5)
    write(os.path.join(root5, "corpus/evidence/round91/control-driver-r91.py"), open(DRV).read())
    write(os.path.join(root5, "r1.sh"),
          "#!/bin/sh\nprintf 'A=1\\n'\n"
          f"printf '# case=b\\n# expected_exit=0\\n# exit=0\\n# computed_against={REVX}\\nB=1\\n' > corpus/evidence/round91/controls/receipts/b.txt\n",
          0o755)
    write(os.path.join(root5, "r2.sh"), "#!/bin/sh\nprintf 'B=1\\n'\ncp b_committed.dat corpus/evidence/round91/controls/receipts/b.txt\n",
          0o755)
    write(os.path.join(root5, "corpus/evidence/round91/controls/expected.tsv"),
          "case\tinstrument\texpected_exit\trequired\tpredicates\tsource_of_expectation\n"
          "a\tbash @ROOT@/r1.sh\t0\tA=1\t-\tthe overwriter row\n"
          "b\tbash @ROOT@/r2.sh\t0\tB=1\t-\tthe restored row\n")
    write(os.path.join(rec5, "a.txt"),
          f"# case=a\n# expected_exit=0\n# exit=0\n# computed_against={REVX}\nA=1\n")
    bad_b = f"# case=b\n# expected_exit=0\n# exit=0\n# computed_against={REVX}\nB=0\nmarker=committed\n"
    write(os.path.join(rec5, "b.txt"), bad_b)
    write(os.path.join(root5, "b_committed.dat"), bad_b)
    write(os.path.join(root5, "instrument-pins.txt"),
          f"{sha(os.path.join(root5, 'r1.sh'))}  r1.sh\n"
          f"{sha(os.path.join(root5, 'r2.sh'))}  r2.sh\n"
          f"{sha(os.path.join(root5, 'corpus/evidence/round91/controls/expected.tsv'))}  corpus/evidence/round91/controls/expected.tsv\n")
    run_verify(root5, "A15-exact-gap-no-repo", REVX, repo=False)
    say("    b.txt after run says B=",
        [ln for ln in open(os.path.join(rec5, "b.txt")).read().splitlines() if ln.startswith("B=")])

    # A13: first .py token is a data operand; the executed script is unpinned
    root3 = os.path.join(FIX, "data-first")
    shutil.rmtree(root3, ignore_errors=True)
    os.makedirs(root3)
    write(os.path.join(root3, "data.py"), "DATA=1\n")
    write(os.path.join(root3, "real.sh"), "#!/bin/sh\nprintf 'TOK=1\\n'\n", 0o755)
    exp = ("case\tinstrument\texpected_exit\trequired\tpredicates\tsource_of_expectation\n"
           "c1-x\tcat @ROOT@/data.py && bash @ROOT@/real.sh\t0\tTOK=1\t-\tthe data-first row\n")
    write(os.path.join(root3, "expected.tsv"), exp)
    write(os.path.join(root3, "receipts", "c1-x.txt"),
          f"# case=c1-x\n# expected_exit=0\n# exit=0\n# computed_against={REVX}\nDATA=1\nTOK=1\n")
    lines = ""
    for rel in ["data.py", "expected.tsv"]:
        lines += f"{sha(os.path.join(root3, rel))}  {rel}\n"
    write(os.path.join(root3, "pins.txt"), lines)
    spec = importlib.util.spec_from_file_location("cd91", DRV)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    row = {"instrument": "cat @ROOT@/data.py && bash @ROOT@/real.sh"}
    say("    instrument_rel(row) =", mod.instrument_rel(row, root3))
    args = [sys.executable, "-B", DRV, "verify", "--root", root3, "--work",
            os.path.join(S, "work2", "A13a"), "--rev", REVX,
            "--expected", os.path.join(root3, "expected.tsv"),
            "--receipts", os.path.join(root3, "receipts"),
            "--pins", os.path.join(root3, "pins.txt")]
    p = subprocess.run(args, capture_output=True, text=True, cwd=root3)
    say(f"\n### A13a-data-operand-first: exit={p.returncode}")
    for ln in ((p.stdout or "") + (p.stderr or "")).strip().splitlines()[-5:]:
        say("   ", ln)
    before = sha(os.path.join(root3, "real.sh"))
    write(os.path.join(root3, "real.sh"), "#!/bin/sh\n# substituted stub, same output\nprintf 'TOK=1\\n'\n", 0o755)
    after = sha(os.path.join(root3, "real.sh"))
    args[args.index("--work") + 1] = os.path.join(S, "work2", "A13b")
    p = subprocess.run(args, capture_output=True, text=True, cwd=root3)
    say(f"\n### A13b-executed-script-substituted: real.sh {before[:12]}.. -> {after[:12]}.. exit={p.returncode}")
    for ln in ((p.stdout or "") + (p.stderr or "")).strip().splitlines()[-5:]:
        say("   ", ln)

    # A14: computed_against names another revision
    root4 = os.path.join(FIX, "pin-mismatch")
    shutil.rmtree(root4, ignore_errors=True)
    os.makedirs(root4)
    write(os.path.join(root4, "tool.sh"), "#!/bin/sh\nprintf 'TOK=1\\n'\n", 0o755)
    write(os.path.join(root4, "expected.tsv"),
          "case\tinstrument\texpected_exit\trequired\tpredicates\tsource_of_expectation\n"
          "c1-x\tbash @ROOT@/tool.sh\t0\tTOK=1\t-\tthe row\n")
    write(os.path.join(root4, "receipts", "c1-x.txt"),
          f"# case=c1-x\n# expected_exit=0\n# exit=0\n# computed_against={'b'*40}\nTOK=1\n")
    write(os.path.join(root4, "pins.txt"),
          f"{sha(os.path.join(root4, 'tool.sh'))}  tool.sh\n"
          f"{sha(os.path.join(root4, 'expected.tsv'))}  expected.tsv\n")
    args = [sys.executable, "-B", DRV, "verify", "--root", root4, "--work",
            os.path.join(S, "work2", "A14"), "--rev", REVX,
            "--expected", os.path.join(root4, "expected.tsv"),
            "--receipts", os.path.join(root4, "receipts"),
            "--pins", os.path.join(root4, "pins.txt")]
    p = subprocess.run(args, capture_output=True, text=True, cwd=root4)
    say(f"\n### A14-computed-against-other-rev: exit={p.returncode}")
    for ln in ((p.stdout or "") + (p.stderr or "")).strip().splitlines()[-5:]:
        say("   ", ln)

    open(os.path.join(S, "transcript2.txt"), "w", encoding="utf-8").write("\n".join(OUT) + "\n")
    print("\nTRANSCRIPT2:", os.path.join(S, "transcript2.txt"))


if __name__ == "__main__":
    main()
