#!/usr/bin/env python3
"""R91ReviewerC1 probe 3: duplicate pin rows (last-wins) and canonical no-write check."""
import hashlib
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/chousa-r91/R91ReviewerC1"
REPO = os.path.join(S, "repo")
DRV = os.path.join(REPO, "corpus/evidence/round91/control-driver-r91.py")
REV = "a" * 40
OUT = []


def say(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    OUT.append(line)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def write(p, text, mode=None):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)
    if mode is not None:
        os.chmod(p, mode)


def run(root, tag, pins_text):
    work = os.path.join(S, "work3", tag)
    shutil.rmtree(work, ignore_errors=True)
    write(os.path.join(root, "pins.txt"), pins_text)
    p = subprocess.run([sys.executable, "-B", DRV, "verify", "--root", root, "--work", work,
                        "--rev", REV, "--expected", os.path.join(root, "expected.tsv"),
                        "--receipts", os.path.join(root, "receipts"),
                        "--pins", os.path.join(root, "pins.txt")],
                       capture_output=True, text=True, cwd=root)
    out = (p.stdout or "") + (p.stderr or "")
    say(f"\n### {tag}: exit={p.returncode}")
    for ln in out.strip().splitlines()[-4:]:
        say("   ", ln)


def main():
    root = os.path.join(S, "fx3", "dup-pin")
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(os.path.join(root, "receipts"))
    write(os.path.join(root, "tool.sh"), "#!/bin/sh\nprintf 'TOK=1\\n'\n", 0o755)
    write(os.path.join(root, "expected.tsv"),
          "case\tinstrument\texpected_exit\trequired\tpredicates\tsource_of_expectation\n"
          "c1-x\tbash @ROOT@/tool.sh\t0\tTOK=1\t-\tthe row\n")
    write(os.path.join(root, "receipts", "c1-x.txt"),
          f"# case=c1-x\n# expected_exit=0\n# exit=0\n# computed_against={REV}\nTOK=1\n")
    good_tool = sha(os.path.join(root, "tool.sh"))
    good_exp = sha(os.path.join(root, "expected.tsv"))
    run(root, "B1-wrong-then-right",
        f"{'0'*64}  tool.sh\n{good_tool}  tool.sh\n{good_exp}  expected.tsv\n")
    run(root, "B2-right-then-wrong",
        f"{good_tool}  tool.sh\n{'0'*64}  tool.sh\n{good_exp}  expected.tsv\n")
    # B3: substring must not satisfy a whole token
    root3 = os.path.join(S, "fx3", "substring")
    shutil.rmtree(root3, ignore_errors=True)
    os.makedirs(os.path.join(root3, "receipts"))
    write(os.path.join(root3, "tool.sh"), "#!/bin/sh\nprintf 'TOK=10\\nNUM=0\\n'\n", 0o755)
    write(os.path.join(root3, "expected.tsv"),
          "case\tinstrument\texpected_exit\trequired\tpredicates\tsource_of_expectation\n"
          "c1-x\tbash @ROOT@/tool.sh\t0\tTOK=1\tNUM>=1\tthe row\n")
    write(os.path.join(root3, "receipts", "c1-x.txt"),
          f"# case=c1-x\n# expected_exit=0\n# exit=0\n# computed_against={REV}\nTOK=10\nNUM=0\n")
    run(root3, "B3-substring-and-predicate",
        f"{sha(os.path.join(root3, 'tool.sh'))}  tool.sh\n{sha(os.path.join(root3, 'expected.tsv'))}  expected.tsv\n")
    # B4: missing committed receipt
    root4 = os.path.join(S, "fx3", "missing")
    shutil.rmtree(root4, ignore_errors=True)
    os.makedirs(os.path.join(root4, "receipts"))
    write(os.path.join(root4, "tool.sh"), "#!/bin/sh\nprintf 'TOK=1\\n'\n", 0o755)
    write(os.path.join(root4, "expected.tsv"),
          "case\tinstrument\texpected_exit\trequired\tpredicates\tsource_of_expectation\n"
          "c1-x\tbash @ROOT@/tool.sh\t0\tTOK=1\t-\tthe row\n")
    run(root4, "B4-missing-receipt",
        f"{sha(os.path.join(root4, 'tool.sh'))}  tool.sh\n{sha(os.path.join(root4, 'expected.tsv'))}  expected.tsv\n")
    open(os.path.join(S, "transcript3.txt"), "w", encoding="utf-8").write("\n".join(OUT) + "\n")
    print("\nTRANSCRIPT3:", os.path.join(S, "transcript3.txt"))


if __name__ == "__main__":
    main()
