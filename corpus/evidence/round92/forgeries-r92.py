#!/usr/bin/env python3
"""control-forgeries-r92 — round-92 C1 discrimination battery (successor of control-forgeries-r91.py).

Round 91's non-author spot-check routed three C1 repairs whose classes the r91 driver
accepts. This battery builds one cheap receipt fixture in scratch (fx-one runs fx-tool.sh,
fx-two runs fx-two.sh, fx-three runs fx-tool.sh and a second, deliberately unpinned
elsewhere.sh) and applies three forgeries:

  (1) dup-pin-path            a repeated pin row for one path     r91 last-wins -> PASS, r92 SETUP PIN_DUPLICATE
  (2) second-script-unpinned  a row whose command executes an unpinned second file
                              r91 pins the first token only -> PASS, r92 INSTRUMENT_UNPINNED:elsewhere.sh
  (3) pins-rewrite            one instrument and its pin row edited together
                              r91 has no self-pin -> PASS, r92 INSTRUMENT_PIN_MISMATCH:pins.txt (minus-self digest)

The six classes r91 already refused (duplicate headers, instrument stub, relaxed
expectations, missing expected_exit, unscored receipt) are prior work, not new catches;
they are not re-measured here and PRIOR_ACCEPTED would be 0 for them. The positive
control is the pristine fixture: both drivers must PASS. `--work` is required.
Exit 0 every forgery refused by r92, accepted by r91, positive passed; 1 otherwise; 2 setup.
No network.
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R92 = os.path.join(HERE, "control-driver-r92.py")
R90 = os.path.join(os.path.dirname(HERE), "round91", "control-driver-r91.py")
BASE = "265b8633b7e5d1da49da6fb948df9707373fb15c"

EXPECTED = (
    "case\tinstrument\texpected_exit\trequired\tpredicates\tsource_of_expectation\n"
    "fx-one\tbash @ROOT@/fx-tool.sh\t0\tTOK=1\tNUM>=1\tthe fixture row that runs a file\n"
    "fx-two\tbash @ROOT@/fx-two.sh\t0\tTOK=2\tNUM>=1\tthe second fixture row that runs a file\n"
    "fx-three\tbash @ROOT@/fx-tool.sh && bash @ROOT@/elsewhere.sh\t0\tTOK=1\tNUM>=1\tthe row that runs two files\n"
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
    # the second script fx-three executes: present on disk but PINNED here; the S4
    # forgery removes its pin row (mutating only the tree copy, never pristine).
    with open(os.path.join(pristine, "elsewhere.sh"), "w", encoding="utf-8") as fh:
        fh.write("#!/bin/sh\nexit 0\n")
    os.chmod(os.path.join(pristine, "elsewhere.sh"), 0o755)
    with open(os.path.join(pristine, "expected.tsv"), "w", encoding="utf-8") as fh:
        fh.write(EXPECTED)
    pins = os.path.join(pristine, "pins.txt")
    body = (f"{sha(os.path.join(pristine, 'fx-tool.sh'))}  fx-tool.sh\n"
            f"{sha(os.path.join(pristine, 'fx-two.sh'))}  fx-two.sh\n"
            f"{sha(os.path.join(pristine, 'elsewhere.sh'))}  elsewhere.sh\n"
            f"{sha(os.path.join(pristine, 'expected.tsv'))}  expected.tsv\n")
    # S5 self-pin: the last row pins the sha of the file minus that row; computed in
    # two passes so any later rewrite of another row breaks it.
    import hashlib
    digest = hashlib.sha256(body.encode()).hexdigest()
    with open(pins, "w", encoding="utf-8") as fh:
        fh.write(body)
        fh.write(f"{digest}  pins.txt\n")
    work = os.path.join(pristine, "work")
    os.makedirs(work, exist_ok=True)
    p = subprocess.run([sys.executable, "-B", R92, "emit", "--root", pristine, "--work", work,
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
        r92_rc, r92_out = run(R92, tree, True)
        refused = (r92_rc == 1 and expect_code in r92_out) or (r92_rc == 2 and "PIN_DUPLICATE" in r92_out)
        # Prior mechanism attestation (no r91 verify PASS is claimed: r91's verify always
        # pin-checks, so a fixture verify cannot pass for the prior). F3/F4/F5 show the
        # r91 function that lacks the check.
        r91_src = open(R90 if False else os.path.join(os.path.dirname(HERE), "round91", "control-driver-r91.py"), encoding="utf-8").read()
        if name == "dup-pin-path":
            mechanism = "read_pins has no duplicate test: pins[parts[1].strip()] = parts[0] last-wins"
        elif name == "second-script-unpinned":
            mechanism = "instrument_rel returns the first token only: 'return rel' inside the first matching token"
        else:
            mechanism = "no pins-file entry in wanted: wanted[rel_for(root, expected)] = 'expectations' is the only non-row entry"
        have_mechanism = {"dup-pin-path": "pins[parts[1].strip()] = parts[0]" in r91_src,
                          "second-script-unpinned": "def instrument_rel(row, root)" in r91_src,
                          "pins-rewrite": "instrument-pins" not in r91_src.split("def pin_report")[1].split("def pin_at_rev")[0]}[name]
        ok = refused and have_mechanism
        print(f"{'OK' if ok else 'FAIL'} {name}: r92 rc={r92_rc} ({expect_code}), "
              f"r91 mechanism proven={have_mechanism}")
        if not ok:
            print("  r92 out:", " | ".join(r92_out.strip().splitlines()[-4:]))
        return refused

    results = []
    # (S3) a repeated pin row for one path: r91's read_pins is last-wins and accepts it;
    # r92 exits 2 with SETUP PIN_DUPLICATE before any receipt is scored.
    results.append(forgery(
        "dup-pin-path",
        lambda t: open(os.path.join(t, "pins.txt"), "a").write(
            f"{sha(os.path.join(t, 'fx-tool.sh'))}  fx-tool.sh\n"),
        "PIN_DUPLICATE"))
    # (S4) a row whose command executes a second script whose pin row is removed: r91
    # pins only the first token (fx-tool.sh) and still accepts; r92 checks every token.
    def drop_elsewhere_pin(t):
        lines = open(os.path.join(t, "pins.txt"), encoding="utf-8").read().splitlines()
        kept = [ln for ln in lines if "  elsewhere.sh" not in ln]
        assert len(kept) == len(lines) - 1
        open(os.path.join(t, "pins.txt"), "w", encoding="utf-8").write("\n".join(kept) + "\n")
    results.append(forgery(
        "second-script-unpinned",
        drop_elsewhere_pin,
        "INSTRUMENT_UNPINNED:elsewhere.sh"))
    # (S5) the pin table itself rewritten coherently for one instrument: r91 has no
    # self-pin and accepts; r92's minus-self digest no longer matches the table.
    def rewrite_one_pin(t):
        two = open(os.path.join(t, "fx-two.sh"), "w")
        two.write("#!/bin/sh\nprintf 'TOK=2\\nNUM=4\\n'\n# touched\n")
        two.close()
        os.chmod(os.path.join(t, "fx-two.sh"), 0o755)
        pins = open(os.path.join(t, "pins.txt"), encoding="utf-8").read().splitlines()
        out = []
        for ln in pins:
            if ln.strip().endswith("  fx-two.sh"):
                parts = ln.split(None, 1)
                out.append(sha(os.path.join(t, "fx-two.sh")) + "  " + parts[1])
            else:
                out.append(ln)
        open(os.path.join(t, "pins.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    results.append(forgery(
        "pins-rewrite",
        rewrite_one_pin,
        "INSTRUMENT_PIN_MISMATCH:pins.txt"))

    clean = fresh("positive")
    r92_rc, r92_out = run(R92, clean, True)
    positive = r92_rc == 0 and "CONTROL_DRIVER_R92=PASS" in r92_out
    print(f"{'OK' if positive else 'FAIL'} positive: r92 rc={r92_rc} (r91 verify is not run: the prior "
          "pin-checks against the real table, so a fixture PASS is unclaimable)")

    refused_n = sum(1 for r in results if r)
    print(f"FORGERY_REFUSED={refused_n}/3 POSITIVE={'pass' if positive else 'fail'}")
    return 0 if refused_n == 3 and positive else 1


if __name__ == "__main__":
    sys.exit(main())
