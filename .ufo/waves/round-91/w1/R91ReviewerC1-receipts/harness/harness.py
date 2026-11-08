#!/usr/bin/env python3
"""R91ReviewerC1 fixture harness: attack the frozen C1 sentence against control-driver-r91.py."""
import hashlib
import importlib.util
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


def build(root, rows, files, receipts, pins):
    """rows: (case, instrument, exit, required, predicates); files/receipts/pins: rel -> text."""
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    for rel, body in files.items():
        write(os.path.join(root, rel), body, 0o755 if rel.endswith(".sh") else None)
    exp = "case\tinstrument\texpected_exit\trequired\tpredicates\tsource_of_expectation\n"
    for case, instr, ex, req, pred in rows:
        exp += f"{case}\t{instr}\t{ex}\t{req}\t{pred}\tthe fixture row\n"
    write(os.path.join(root, "expected.tsv"), exp)
    for rel, body in receipts.items():
        write(os.path.join(root, "receipts", rel), body)
    lines = ""
    for rel in pins:
        lines += f"{sha(os.path.join(root, rel))}  {rel}\n"
    write(os.path.join(root, "pins.txt"), lines)


def receipt(case, rc, required_body, rev=REV, extra_headers=""):
    return (f"# case={case}\n# expected_exit={rc}\n# exit={rc}\n# computed_against={rev}\n"
            + extra_headers + required_body)


def verify(root, tag, repo=None, receipts_rev=None, expected=None, receipts=None, pins=None,
           driver=None):
    work = os.path.join(S, "work", tag)
    shutil.rmtree(work, ignore_errors=True)
    args = [sys.executable, "-B", driver or DRV, "verify", "--root", root, "--work", work,
            "--rev", REV,
            "--expected", expected or os.path.join(root, "expected.tsv"),
            "--receipts", receipts or os.path.join(root, "receipts"),
            "--pins", pins or os.path.join(root, "pins.txt")]
    if repo:
        args += ["--repo", repo, "--receipts-rev", receipts_rev or REV]
    p = subprocess.run(args, capture_output=True, text=True, cwd=root)
    out = (p.stdout or "") + (p.stderr or "")
    say(f"\n### {tag}: exit={p.returncode}")
    for ln in out.strip().splitlines()[-8:]:
        say("   ", ln)
    return p.returncode, out


def main():
    fxs = os.path.join(S, "fx")
    shutil.rmtree(fxs, ignore_errors=True)
    os.makedirs(fxs)
    say("REV(fixture)=", REV)

    # --- A1: duplicate expected_exit with the SAME value --------------------------------
    root = os.path.join(fxs, "dup-eq")
    build(root,
          [("c1-x", "bash @ROOT@/tool.sh", 0, "TOK=1", "-")],
          {"tool.sh": "#!/bin/sh\nprintf 'TOK=1\\n'\n"},
          {"c1-x.txt": receipt("c1-x", 0, "TOK=1\n", extra_headers="# expected_exit=0\n")},
          ["tool.sh", "expected.tsv"])
    verify(root, "A1-dup-expected_exit-equal")

    # --- A2: # exit=+0 / # exit= 0 ------------------------------------------------------
    root = os.path.join(fxs, "plus-zero")
    build(root,
          [("c1-x", "bash @ROOT@/tool.sh", 0, "TOK=1", "-")],
          {"tool.sh": "#!/bin/sh\nprintf 'TOK=1\\n'\n"},
          {"c1-x.txt": "# case=c1-x\n# expected_exit=0\n# exit=+0\n# computed_against=" + REV + "\nTOK=1\n"},
          ["tool.sh", "expected.tsv"])
    verify(root, "A2-exit-plus-zero")
    root = os.path.join(fxs, "space-zero")
    build(root,
          [("c1-x", "bash @ROOT@/tool.sh", 0, "TOK=1", "-")],
          {"tool.sh": "#!/bin/sh\nprintf 'TOK=1\\n'\n"},
          {"c1-x.txt": "# case=c1-x\n# expected_exit=0\n# exit= 0\n# computed_against=" + REV + "\nTOK=1\n"},
          ["tool.sh", "expected.tsv"])
    verify(root, "A2b-exit-space-zero")

    # --- A3: two scripts; which one is pinned -------------------------------------------
    root = os.path.join(fxs, "two-scripts")
    build(root,
          [("c1-x", "bash @ROOT@/first.sh && python3 -B @ROOT@/real.py", 0, "TOK=3", "NUM>=1")],
          {"first.sh": "#!/bin/sh\ntrue\n",
           "real.py": "print('TOK=3')\nprint('NUM=4')\n"},
          {"c1-x.txt": receipt("c1-x", 0, "TOK=3\nNUM=4\n")},
          ["first.sh", "expected.tsv"])
    verify(root, "A3-two-scripts-pin-first")
    root = os.path.join(fxs, "two-scripts-rev")
    build(root,
          [("c1-x", "bash @ROOT@/first.sh && python3 -B @ROOT@/real.py", 0, "TOK=3", "NUM>=1")],
          {"first.sh": "#!/bin/sh\ntrue\n",
           "real.py": "print('TOK=3')\nprint('NUM=4')\n"},
          {"c1-x.txt": receipt("c1-x", 0, "TOK=3\nNUM=4\n")},
          ["real.py", "expected.tsv"])
    verify(root, "A3b-two-scripts-pin-second")

    # --- A4: pinned script reads an unpinned data file -----------------------------------
    root = os.path.join(fxs, "data-file")
    build(root,
          [("c1-x", "bash @ROOT@/tool.sh", 0, "TOK=1", "-")],
          {"tool.sh": "#!/bin/sh\nprintf 'TOK=1\\n'\ncat data.txt\n",
           "data.txt": "EXTRA=1\n"},
          {"c1-x.txt": receipt("c1-x", 0, "TOK=1\nEXTRA=1\n")},
          ["tool.sh", "expected.tsv"])
    verify(root, "A4a-data-file-pristine")
    write(os.path.join(root, "data.txt"), "EXTRA=2\n")
    verify(root, "A4b-data-file-edited-unpinned")

    # --- A5: instrument without .py/.sh suffix ------------------------------------------
    root = os.path.join(fxs, "no-suffix")
    build(root,
          [("c1-x", "bash @ROOT@/fx-tool", 0, "TOK=1", "-")],
          {"fx-tool": "#!/bin/sh\nprintf 'TOK=1\\n'\n"},
          {"c1-x.txt": receipt("c1-x", 0, "TOK=1\n")},
          ["fx-tool", "expected.tsv"])
    verify(root, "A5-script-no-extension")

    # --- A6: required body token only on an INDENTED comment line -----------------------
    root = os.path.join(fxs, "indented-token")
    build(root,
          [("c1-x", "bash @ROOT@/tool.sh", 0, "FOO=1", "-")],
          {"tool.sh": "#!/bin/sh\nprintf '   # FOO=1\\n'\n"},
          {"c1-x.txt": receipt("c1-x", 0, "   # FOO=1\n")},
          ["tool.sh", "expected.tsv"])
    verify(root, "A6a-indented-token")
    root = os.path.join(fxs, "column0-token")
    build(root,
          [("c1-x", "bash @ROOT@/tool.sh", 0, "FOO=1", "-")],
          {"tool.sh": "#!/bin/sh\nprintf '# FOO=1\\n'\n"},
          {"c1-x.txt": receipt("c1-x", 0, "# FOO=1\n")},
          ["tool.sh", "expected.tsv"])
    verify(root, "A6b-column0-comment-token")

    # --- A7: indented duplicate of a required header ------------------------------------
    root = os.path.join(fxs, "indented-dup-header")
    build(root,
          [("c1-x", "bash @ROOT@/tool.sh", 0, "TOK=1", "-")],
          {"tool.sh": "#!/bin/sh\nprintf 'TOK=1\\n'\n"},
          {"c1-x.txt": "# case=c1-x\n# expected_exit=0\n# exit=0\n# computed_against=" + REV
           + "\n # exit=1\nTOK=1\n"},
          ["tool.sh", "expected.tsv"])
    verify(root, "A7-indented-duplicate-exit")

    # --- A8: extra .txt that parses as a receipt but escapes the substring scan ---------
    root = os.path.join(fxs, "unscored-spacing")
    build(root,
          [("c1-x", "bash @ROOT@/tool.sh", 0, "TOK=1", "-")],
          {"tool.sh": "#!/bin/sh\nprintf 'TOK=1\\n'\n"},
          {"c1-x.txt": receipt("c1-x", 0, "TOK=1\n"),
           "evil.txt": "#  case=evil\n# expected_exit=0\n# exit=0\n# computed_against=" + REV + "\nX=1\n"},
          ["tool.sh", "expected.tsv"])
    verify(root, "A8a-unscored-two-space-case")
    spec = importlib.util.spec_from_file_location("cd91", DRV)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    evil = open(os.path.join(root, "receipts", "evil.txt"), encoding="utf-8").read()
    say("    header_multi(evil) =", mod.header_multi(evil))

    # --- A8b: raw evidence mentioning '# case=' off-column is flagged as a receipt ------
    root = os.path.join(fxs, "unscored-false-positive")
    build(root,
          [("c1-x", "bash @ROOT@/tool.sh", 0, "TOK=1", "-")],
          {"tool.sh": "#!/bin/sh\nprintf 'TOK=1\\n'\n"},
          {"c1-x.txt": receipt("c1-x", 0, "TOK=1\n"),
           "raw.txt": "raw instrument evidence\nnote # case=fake here\n"},
          ["tool.sh", "expected.tsv"])
    rc, out = verify(root, "A8b-raw-mention-flagged")
    raw = open(os.path.join(root, "receipts", "raw.txt"), encoding="utf-8").read()
    say("    header_multi(raw) =", mod.header_multi(raw))

    # --- A9: --work inside the receipts directory --------------------------------------
    root = os.path.join(fxs, "work-in-receipts")
    build(root,
          [("c1-x", "bash @ROOT@/tool.sh", 0, "TOK=1", "-")],
          {"tool.sh": "#!/bin/sh\nprintf 'TOK=1\\n'\n"},
          {"c1-x.txt": receipt("c1-x", 0, "TOK=1\n")},
          ["tool.sh", "expected.tsv"])
    work = os.path.join(root, "receipts", "w")
    os.makedirs(work)
    args = [sys.executable, "-B", DRV, "verify", "--root", root, "--work", work, "--rev", REV,
            "--expected", os.path.join(root, "expected.tsv"),
            "--receipts", os.path.join(root, "receipts"),
            "--pins", os.path.join(root, "pins.txt")]
    p = subprocess.run(args, capture_output=True, text=True, cwd=root)
    say(f"\n### A9-work-inside-receipts: exit={p.returncode}")
    for ln in ((p.stdout or "") + (p.stderr or "")).strip().splitlines()[-4:]:
        say("   ", ln)
    mine = sorted(os.listdir(os.path.join(root, "receipts", "w")))
    say("    receipts/w contents after verify =", mine)

    # --- A10: clause-1 ordering, synthetic fixture (git, --repo) ------------------------
    root = os.path.join(fxs, "clause1")
    drvrel = "corpus/evidence/round91/control-driver-r91.py"
    exprel = "corpus/evidence/round91/controls/expected.tsv"
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    write(os.path.join(root, drvrel), open(DRV, encoding="utf-8").read())
    write(os.path.join(root, "r1.sh"),
          "#!/bin/sh\nprintf 'A=1\\n'\n"
          f"printf '# case=b\\n# expected_exit=0\\n# exit=0\\n# computed_against={REV}\\nB=1\\n' "
          f"> '{os.path.join(root, 'receipts', 'b.txt')}'\n", 0o755)
    write(os.path.join(root, "r2.sh"), "#!/bin/sh\nprintf 'B=1\\n'\n", 0o755)
    exp = ("case\tinstrument\texpected_exit\trequired\tpredicates\tsource_of_expectation\n"
           "a\tbash @ROOT@/r1.sh\t0\tA=1\t-\tthe overwriter row\n"
           "b\tbash @ROOT@/r2.sh\t0\tB=1\t-\tthe overwritten row\n")
    write(os.path.join(root, exprel), exp)
    write(os.path.join(root, "receipts", "a.txt"), receipt("a", 0, "A=1\n"))
    write(os.path.join(root, "receipts", "b.txt"), receipt("b", 0, "B=0\nmarker=committed\n"))
    lines = ""
    for rel in ["r1.sh", "r2.sh", exprel]:
        lines += f"{sha(os.path.join(root, rel))}  {rel}\n"
    write(os.path.join(root, "instrument-pins.txt"), lines)
    subprocess.run(["git", "-C", root, "init", "-q"], check=True)
    subprocess.run(["git", "-C", root, "add", "-A"], check=True)
    subprocess.run(["git", "-C", root, "-c", "user.email=r91@fixture", "-c", "user.name=r91",
                    "commit", "-qm", "fixture"], check=True)
    ffix = subprocess.run(["git", "-C", root, "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True).stdout.strip()
    top = subprocess.run(["git", "-C", root, "rev-parse", "--show-toplevel"], capture_output=True,
                         text=True).stdout.strip()
    say("\n### A10 fixture git toplevel check:", top, "==", root, "->", top == root)
    say("    committed b.txt before any run:\n" + open(os.path.join(root, "receipts", "b.txt")).read())
    # with --repo on a copy of the pristine tree: r1 overwrites b.txt, SELF_PIN must fire
    copy = os.path.join(fxs, "clause1-repo")
    shutil.rmtree(copy, ignore_errors=True)
    shutil.copytree(root, copy)
    drv2 = os.path.join(copy, drvrel)
    verify(copy, "A10a-clause1-with-repo", repo=copy, receipts_rev=ffix,
           expected=os.path.join(copy, exprel),
           receipts=os.path.join(copy, "receipts"),
           pins=os.path.join(copy, "instrument-pins.txt"), driver=drv2)
    say("    b.txt after with-repo run:\n" + open(os.path.join(copy, "receipts", "b.txt")).read())
    # without --repo on another pristine copy: the overwritten receipt is accepted
    copy2 = os.path.join(fxs, "clause1-norepo")
    shutil.rmtree(copy2, ignore_errors=True)
    shutil.copytree(root, copy2)
    drv3 = os.path.join(copy2, drvrel)
    verify(copy2, "A10b-clause1-without-repo",
           expected=os.path.join(copy2, exprel),
           receipts=os.path.join(copy2, "receipts"),
           pins=os.path.join(copy2, "instrument-pins.txt"), driver=drv3)
    say("    b.txt after without-repo run:\n" + open(os.path.join(copy2, "receipts", "b.txt")).read())

    # --- A11: trim instrument-pins.txt to the six wanted rows; canonical-style verify ---
    root = os.path.join(fxs, "pins-trim")
    shutil.rmtree(root, ignore_errors=True)
    shutil.copytree(REPO, root, symlinks=True)
    pins = os.path.join(root, "corpus/evidence/round91/instrument-pins.txt")
    kept = ("49102204fa9698df97f2f8ac467468ee57dff1a358e934d52654821cd880b40c  corpus/evidence/round91/control-driver-r91.py\n"
            "f62921b60ceed00fe147350d433c16fe18a17c00af369e7416030592f06562d7  corpus/evidence/round91/controls/expected.tsv\n"
            "f34f59c87c08c11d762a1ae702251183eb72a27f7728504882e64ce24e6d2103  corpus/evidence/round89/gate-records-r89.py\n"
            "10b43d8a69bfd56308320c7843291c2f425562a35d89aa9a360478d5b284c8eb  corpus/evidence/round89/mutate-r89.py\n"
            "4967755433f19b8ca5f070dcae377ba23989ae6c7971afa4d9936b06c3b3d3c8  corpus/evidence/round90/harm-recheck-r90.py\n"
            "2c063f8bfab6922d199546494d2545f495b05ab9350a7379e1b7f4cde8939f4b  corpus/evidence/round89/curation-r89.py\n"
            "fd54ab3cbc1c0ef9d64e7c586db6068e3afb3675d6274328e34c32b2bbf20d4b  corpus/evidence/round89/curation-r89-controls.py\n")
    write(pins, kept)
    p = subprocess.run([sys.executable, "-B", os.path.join(root, "corpus/evidence/round91/control-driver-r91.py"),
                        "verify", "--root", ".", "--repo", ".", "--rev",
                        "4d00d7519290569879f853d7122b82a927cda1f3", "--receipts-rev",
                        "67954adc599bd605705d94a1ea7abb582491a907",
                        "--work", os.path.join(S, "work", "A11")],
                       capture_output=True, text=True, cwd=root)
    say(f"\n### A11-pins-trimmed-on-disk: exit={p.returncode}")
    for ln in ((p.stdout or "") + (p.stderr or "")).strip().splitlines()[-6:]:
        say("   ", ln)

    # --- A12: self_pin without --repo print surface ------------------------------------
    root = os.path.join(fxs, "no-repo-print")
    build(root,
          [("c1-x", "bash @ROOT@/tool.sh", 0, "TOK=1", "-")],
          {"tool.sh": "#!/bin/sh\nprintf 'TOK=1\\n'\n"},
          {"c1-x.txt": receipt("c1-x", 0, "TOK=1\n")},
          ["tool.sh", "expected.tsv"])
    rc, out = verify(root, "A12-no-repo")
    say("    SELF_PIN present in output:", "SELF_PIN" in out)

    open(os.path.join(S, "transcript.txt"), "w", encoding="utf-8").write("\n".join(OUT) + "\n")
    print("\nTRANSCRIPT:", os.path.join(S, "transcript.txt"))


if __name__ == "__main__":
    main()
