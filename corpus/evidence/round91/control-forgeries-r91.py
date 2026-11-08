#!/usr/bin/env python3
"""control-forgeries-r91 — round-91 C1 discrimination battery.

Builds one cheap receipt fixture in scratch (`fx-one` runs a file, `fx-two` runs `printf`), emits committed receipts
with the r91 driver, and applies six forgeries that round 90's driver accepts:

  (1) dup-header-exit          `# exit=1` before `# exit=0`           r90 last-wins -> PASS, r91 HEADER_DUPLICATE
  (2) dup-header-computed      a second `# computed_against=` first   r90 last-wins -> PASS, r91 HEADER_DUPLICATE
  (3) instrument-stub          the executed file replaced, same output r90 never pins -> PASS, r91 PIN_MISMATCH
  (4) expected-swap            the expectations file relaxed           r90 reads it -> PASS, r91 EXPECTED pin
  (5) missing-expected_exit    the `# expected_exit=` header removed   r90 never reads it -> PASS, r91 MISSING_HEADER
  (6) extra-receipt            a receipt no expected row scores        r90 ignores it -> PASS, r91 UNSCORED_RECEIPT

The positive control is the pristine fixture: both drivers must PASS. `--work` is required and removed by the caller.
Exit 0 every forgery refused by r91, accepted by r90, positive passed; 1 otherwise; 2 setup. No network.
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R91 = os.path.join(HERE, "control-driver-r91.py")
R90 = os.path.join(os.path.dirname(HERE), "round90", "control-driver-r90.py")
BASE = "265b8633b7e5d1da49da6fb948df9707373fb15c"

EXPECTED = (
    "case\tinstrument\texpected_exit\trequired\tpredicates\tsource_of_expectation\n"
    "fx-one\tbash @ROOT@/fx-tool.sh\t0\tTOK=1\tNUM>=1\tthe fixture row that runs a file\n"
    "fx-two\tbash @ROOT@/fx-two.sh\t0\tTOK=2\tNUM>=1\tthe second fixture row that runs a file\n"
)
TOOL = "#!/bin/sh\nprintf 'TOK=1\\nNUM=3\\n'\n"


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def build(pristine):
    os.makedirs(os.path.join(pristine, "receipts"), exist_ok=True)
    with open(os.path.join(pristine, "fx-tool.sh"), "w", encoding="utf-8") as fh:
        fh.write(TOOL)
    os.chmod(os.path.join(pristine, "fx-tool.sh"), 0o755)
    with open(os.path.join(pristine, "fx-two.sh"), "w", encoding="utf-8") as fh:
        fh.write("#!/bin/sh\nprintf 'TOK=2\\nNUM=4\\n'\n")
    os.chmod(os.path.join(pristine, "fx-two.sh"), 0o755)
    with open(os.path.join(pristine, "expected.tsv"), "w", encoding="utf-8") as fh:
        fh.write(EXPECTED)
    pins = os.path.join(pristine, "pins.txt")
    with open(pins, "w", encoding="utf-8") as fh:
        fh.write(f"{sha(os.path.join(pristine, 'fx-tool.sh'))}  fx-tool.sh\n")
        fh.write(f"{sha(os.path.join(pristine, 'fx-two.sh'))}  fx-two.sh\n")
        fh.write(f"{sha(os.path.join(pristine, 'expected.tsv'))}  expected.tsv\n")
    work = os.path.join(pristine, "work")
    os.makedirs(work, exist_ok=True)
    p = subprocess.run([sys.executable, "-B", R91, "emit", "--root", pristine, "--work", work,
                        "--rev", BASE, "--expected", os.path.join(pristine, "expected.tsv"),
                        "--receipts", os.path.join(pristine, "receipts")],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"SETUP emit failed: {p.stdout}{p.stderr}")


def run(driver, tree, extra_pins):
    work = os.path.join(tree, "w-" + os.path.basename(driver))
    os.makedirs(work, exist_ok=True)
    args = [sys.executable, "-B", driver, "verify", "--root", tree, "--work", work, "--rev", BASE,
            "--expected", os.path.join(tree, "expected.tsv"),
            "--receipts", os.path.join(tree, "receipts")]
    if extra_pins:
        args += ["--pins", os.path.join(tree, "pins.txt")]
    p = subprocess.run(args, capture_output=True, text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    work = os.path.abspath(a.work)
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work, exist_ok=True)
    pristine = os.path.join(work, "pristine")
    build(pristine)

    def fresh(name):
        d = os.path.join(work, name)
        shutil.copytree(pristine, d)
        return d

    def edit_receipt(tree, case, fn):
        p = os.path.join(tree, "receipts", case + ".txt")
        text = open(p, encoding="utf-8").read()
        open(p, "w", encoding="utf-8").write(fn(text))

    def forgery(name, mutate, expect_code):
        tree = fresh(name)
        mutate(tree)
        r90_rc, r90_out = run(R90, tree, False)
        r91_rc, r91_out = run(R91, tree, True)
        prior_ok = r90_rc == 0
        refused = r91_rc == 1 and expect_code in r91_out
        print(f"{'OK' if prior_ok and refused else 'FAIL'} {name}: r91 rc={r91_rc} ({expect_code}), "
              f"r90 rc={r90_rc}")
        if not (prior_ok and refused):
            print("  r91 out:", " | ".join(r91_out.strip().splitlines()[-4:]))
            print("  r90 out:", " | ".join(r90_out.strip().splitlines()[-4:]))
        return prior_ok and refused

    results = []
    results.append(forgery(
        "dup-header-exit",
        lambda t: edit_receipt(t, "fx-one", lambda s: s.replace("# exit=0\n", "# exit=1\n# exit=0\n", 1)),
        "HEADER_DUPLICATE:exit"))
    results.append(forgery(
        "dup-header-computed",
        lambda t: edit_receipt(t, "fx-one", lambda s: s.replace(
            f"# computed_against={BASE}\n", f"# computed_against={'0' * 40}\n# computed_against={BASE}\n", 1)),
        "HEADER_DUPLICATE:computed_against"))
    results.append(forgery(
        "instrument-stub",
        lambda t: (open(os.path.join(t, "fx-tool.sh"), "w").write("#!/bin/sh\n# substituted stub, same output\nprintf 'TOK=1\\nNUM=3\\n'\n"),
                   os.chmod(os.path.join(t, "fx-tool.sh"), 0o755)),
        "INSTRUMENT_PIN_MISMATCH:fx-tool.sh"))
    results.append(forgery(
        "expected-swap",
        lambda t: open(os.path.join(t, "expected.tsv"), "w").write(
            EXPECTED.replace("TOK=1\tNUM>=1", "TOK=1\tNUM>=0")),
        "INSTRUMENT_PIN_MISMATCH:expected.tsv"))
    results.append(forgery(
        "missing-expected_exit",
        lambda t: edit_receipt(t, "fx-one", lambda s: s.replace("# expected_exit=0\n", "", 1)),
        "MISSING_HEADER:expected_exit"))
    results.append(forgery(
        "extra-receipt",
        lambda t: open(os.path.join(t, "receipts", "fx-extra.txt"), "w").write(
            "# case=fx-extra\n# expected_exit=0\n# exit=0\n# computed_against=" + BASE + "\nTOK=9\n"),
        "UNSCORED_RECEIPT"))

    clean = fresh("positive")
    r90_rc, _ = run(R90, clean, False)
    r91_rc, r91_out = run(R91, clean, True)
    positive = r90_rc == 0 and r91_rc == 0 and "CONTROL_DRIVER_R91=PASS" in r91_out
    print(f"{'OK' if positive else 'FAIL'} positive: r90 rc={r90_rc} r91 rc={r91_rc}")

    refused_n = sum(1 for r in results if r)
    print(f"FORGERY_REFUSED={refused_n}/6 PRIOR_ACCEPTED={refused_n}/6 POSITIVE={'pass' if positive else 'fail'}")
    return 0 if refused_n == 6 and positive else 1


if __name__ == "__main__":
    sys.exit(main())
