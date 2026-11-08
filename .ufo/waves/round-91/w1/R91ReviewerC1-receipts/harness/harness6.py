#!/usr/bin/env python3
"""R91ReviewerC1 probe 6: indented '# ...' lines under the full --repo form.

A line ' # exit=1' beside a valid '# exit=0' is body text (clause 2 sees one header value), and
'   # FOO=1' supplies the required body token (clause 4). Committed at the carrier, so SELF_PIN passes.
"""
import hashlib
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/chousa-r91/R91ReviewerC1"
DRV = os.path.join(S, "repo/corpus/evidence/round91/control-driver-r91.py")
OUT = []


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


def main():
    root = os.path.join(S, "fx6", "indented-lines")
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    drvrel = "corpus/evidence/round91/control-driver-r91.py"
    exprel = "corpus/evidence/round91/controls/expected.tsv"
    rec = "corpus/evidence/round91/controls/receipts"
    write(os.path.join(root, drvrel), open(DRV, encoding="utf-8").read())
    write(os.path.join(root, "tool.sh"), "#!/bin/sh\nprintf '   # FOO=1\\n'\n", 0o755)
    write(os.path.join(root, exprel),
          "case\tinstrument\texpected_exit\trequired\tpredicates\tsource_of_expectation\n"
          "c1-x\tbash @ROOT@/tool.sh\t0\tFOO=1\t-\tthe indented-comment row\n")
    write(os.path.join(root, "instrument-pins.txt"),
          f"{sha(os.path.join(root, 'tool.sh'))}  tool.sh\n"
          f"{sha(os.path.join(root, exprel))}  {exprel}\n")
    git(root, "init", "-q")
    top = git(root, "rev-parse", "--show-toplevel")
    say("    git toplevel check:", top, "==", root, "->", top == root)
    git(root, "add", "-A")
    git(root, "-c", "user.email=r91@fixture", "-c", "user.name=r91", "commit", "-qm", "X")
    x = git(root, "rev-parse", "HEAD")
    body = (f"# case=c1-x\n# expected_exit=0\n# exit=0\n# computed_against={x}\n"
            " # exit=1\n   # FOO=1\n")
    write(os.path.join(root, rec, "c1-x.txt"), body)
    git(root, "add", "-A")
    git(root, "-c", "user.email=r91@fixture", "-c", "user.name=r91", "commit", "-qm", "Y")
    y = git(root, "rev-parse", "HEAD")
    say("    X =", x, " Y =", y)
    say("    committed receipt:", repr(body))
    work = os.path.join(S, "work6")
    shutil.rmtree(work, ignore_errors=True)
    p = subprocess.run([sys.executable, "-B", os.path.join(root, drvrel), "verify", "--root", ".",
                        "--repo", ".", "--rev", x, "--receipts-rev", y,
                        "--expected", os.path.join(root, exprel),
                        "--receipts", os.path.join(root, rec),
                        "--pins", os.path.join(root, "instrument-pins.txt"),
                        "--work", work], capture_output=True, text=True, cwd=root)
    out = (p.stdout or "") + (p.stderr or "")
    say(f"\n### C1-indented-lines-full-form: exit={p.returncode}")
    for ln in out.strip().splitlines():
        say("   ", ln)
    say("    HEADER_DUPLICATE in output:", "HEADER_DUPLICATE" in out,
        " TOKEN_MISSING in output:", "TOKEN_MISSING" in out)
    open(os.path.join(S, "transcript6.txt"), "w", encoding="utf-8").write("\n".join(OUT) + "\n")
    print("\nTRANSCRIPT6:", os.path.join(S, "transcript6.txt"))


if __name__ == "__main__":
    main()
