#!/usr/bin/env python3
"""control-forgeries-r90 — the round-90 C1 forgery battery (paired with control-driver-r90.py).

Each case is a receipt/expectation pair that the round-89 driver (`run-controls.sh`) ACCEPTED and the round-90 driver
must REFUSE. The prior driver is the committed round-89 script, copied into a scratch tree beside the forged
`expected.tsv` and `receipts/` so its own `HERE` resolution is exercised unchanged; the round-90 driver is invoked in
`verify` mode with the forged files, without `--repo` (the self-pin leg is exercised by the committed set instead).

Cases (round-89 spot-check §Amendment 7 B1–B4, plus the `considerthese/2026-11-07.md` "duplicate wins" class):
  B2-substring        the output carries `LEG_REREAD=16/160`; the row requires `LEG_REREAD=16/16` (substring match)
  B1-committed        the committed receipt contradicts the row (`LEG_REREAD=0/16`) but a fresh run would pass here
  B3-no-pin           the receipt carries no `# computed_against=` revision pin
  B3b-stale-pin       the pin names a different revision than the one scored
  B4-harm-vacuity     `moved=0 records=0` satisfies the prior row; the successor requires `records>=1`
  C-duplicate-key     the body carries `records=0` and later `records=5` (last-one-wins); prior `grep -F` passes
  POSITIVE            a correct receipt: both drivers must accept it (the repair is not a blanket refusal)

Usage: python3 -B corpus/evidence/round90/control-forgeries-r90.py --root DIR --work DIR --rev REV
Exit 0 every forgery refused by r90, accepted by r89, and the positive accepted by both; 1 a deviation; 2 setup.
"""
import argparse
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NEW = os.path.join(HERE, "control-driver-r90.py")
PRIOR = os.path.join(HERE, "..", "round89", "controls", "run-controls.sh")
STUB = "import sys\nprint(\"\\n\".join(sys.argv[1:]))\n"


def write_stub(path, lines, rc=0):
    body = "import sys\n" + "".join(f"print({ln!r})\n" for ln in lines) + f"sys.exit({rc})\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)


def receipt(path, case, expect, got, rev, lines):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"# case={case}\n# expected_exit={expect}\n# exit={got}\n# computed_against={rev}\n")
        fh.write("\n".join(lines) + "\n")


def case_fixture(work, cid, stub_lines, required, predicates, committed_lines, rev, pin=True,
                 stale_pin=False, stub_rc=0):
    """One forged row: stub instrument, both expected.tsv shapes, and the committed receipt."""
    d = os.path.join(work, cid)
    os.makedirs(os.path.join(d, "receipts"), exist_ok=True)
    stub = os.path.join(d, "stub.py")
    write_stub(stub, stub_lines, stub_rc)
    instr = f"{sys.executable} -B {stub}"
    with open(os.path.join(d, "expected6.tsv"), "w", encoding="utf-8") as fh:
        fh.write("case\tinstrument\texpected_exit\trequired\tpredicates\tsource_of_expectation\n")
        fh.write(f"{cid}\t{instr}\t0\t{' '.join(required)}\t{' '.join(predicates)}\tforgery fixture\n")
    with open(os.path.join(d, "expected5.tsv"), "w", encoding="utf-8") as fh:
        fh.write("case\tinstrument\texpected_exit\trequired\tsource_of_expectation\n")
        fh.write(f"{cid}\t{instr}\t0\t{' '.join(required)}\tforgery fixture\n")
    rec = os.path.join(d, "receipts", cid + ".txt")
    body = committed_lines
    if pin:
        with open(rec, "w", encoding="utf-8") as fh:
            fh.write(f"# case={cid}\n# expected_exit=0\n# exit=0\n")
            if stale_pin:
                fh.write("# computed_against=" + "0" * 40 + "\n")
            else:
                fh.write(f"# computed_against={rev}\n")
            fh.write("\n".join(body) + "\n")
    else:
        with open(rec, "w", encoding="utf-8") as fh:
            fh.write(f"# case={cid}\n# expected_exit=0\n# exit=0\n")
            fh.write("\n".join(body) + "\n")
    return {"dir": d, "expected6": os.path.join(d, "expected6.tsv"),
            "expected5": os.path.join(d, "expected5.tsv"), "receipts": os.path.join(d, "receipts")}


def run_prior(root, fx, work):
    """Exercise the round-89 driver unchanged: its own directory layout, 5-column expected.tsv, receipt rewrite."""
    pdir = os.path.join(fx["dir"], "prior", "corpus", "evidence", "round89", "controls")
    os.makedirs(pdir, exist_ok=True)
    shutil.copy2(PRIOR, os.path.join(pdir, "run-controls.sh"))
    shutil.copy2(fx["expected5"], os.path.join(pdir, "expected.tsv"))
    shutil.copytree(fx["receipts"], os.path.join(pdir, "receipts"), dirs_exist_ok=True)
    p = subprocess.run(["bash", os.path.join(pdir, "run-controls.sh"), root, os.path.join(work, "priorwork")],
                       capture_output=True, text=True)
    return p.returncode, p.stdout


def run_new(fx, work, rev):
    p = subprocess.run([sys.executable, "-B", NEW, "verify", "--root", os.path.abspath(os.path.join(HERE, "..", "..", "..")),
                        "--work", os.path.join(work, "w-" + os.path.basename(fx["dir"])), "--rev", rev,
                        "--expected", fx["expected6"], "--receipts", fx["receipts"]],
                       capture_output=True, text=True)
    return p.returncode, p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    if not os.path.isfile(PRIOR):
        print(f"CONTROL_FORGERIES_R90=SETUP missing prior driver {PRIOR}")
        return 2
    work = os.path.abspath(a.work)
    os.makedirs(work, exist_ok=True)
    cases = []

    cases.append(("B2-substring", case_fixture(
        work, "B2-substring", ["LEG_REREAD=16/160", "DONE=1"], ["LEG_REREAD=16/16", "DONE=1"], [],
        ["LEG_REREAD=16/160", "DONE=1"], a.rev)))
    cases.append(("B1-committed", case_fixture(
        work, "B1-committed", ["LEG_REREAD=16/16", "DONE=1"], ["LEG_REREAD=16/16", "DONE=1"], [],
        ["LEG_REREAD=0/16", "DONE=1"], a.rev)))
    cases.append(("B3-no-pin", case_fixture(
        work, "B3-no-pin", ["LEG_REREAD=16/16", "DONE=1"], ["LEG_REREAD=16/16", "DONE=1"], [],
        ["LEG_REREAD=16/16", "DONE=1"], a.rev, pin=False)))
    cases.append(("B3b-stale-pin", case_fixture(
        work, "B3b-stale-pin", ["LEG_REREAD=16/16", "DONE=1"], ["LEG_REREAD=16/16", "DONE=1"], [],
        ["LEG_REREAD=16/16", "DONE=1"], a.rev, stale_pin=True)))
    cases.append(("B4-harm-vacuity", case_fixture(
        work, "B4-harm-vacuity", ["moved=0", "records=0"], ["moved=0"], ["records>=1"],
        ["moved=0", "records=0"], a.rev)))
    cases.append(("C-duplicate-key", case_fixture(
        work, "C-duplicate-key", ["records=0", "records=5"], ["records=5"], [],
        ["records=0", "records=5"], a.rev)))
    cases.append(("POSITIVE", case_fixture(
        work, "POSITIVE", ["LEG_REREAD=16/16", "DONE=1"], ["LEG_REREAD=16/16", "DONE=1"], [],
        ["LEG_REREAD=16/16", "DONE=1"], a.rev)))

    refused = accepted_prior = positives = 0
    ok_all = True
    for cid, fx in cases:
        prior_rc, prior_out = run_prior(os.path.abspath(a.root), fx, work)
        new_rc, new_out = run_new(fx, work, a.rev)
        if cid == "POSITIVE":
            want = new_rc == 0 and prior_rc == 0 and "CONTROL_DRIVER_R90=PASS" in new_out
            positives += 1 if want else 0
            label = "accepted by both drivers" if want else "NOT accepted by both"
        else:
            want = new_rc != 0 and prior_rc == 0
            refused += 1 if new_rc != 0 else 0
            accepted_prior += 1 if prior_rc == 0 else 0
            codes = [ln for ln in new_out.splitlines() if " FINDING " in ln]
            label = ("r90 refused (" + (codes[0].split(" FINDING ")[1] if codes else "no finding line") +
                     "), r89 accepted") if want else "NOT refused by r90 or NOT accepted by the prior driver"
        print(f"{'OK' if want else 'CASE_DEVIATION'} {cid}: {label}")
        print(f"  r90 rc={new_rc}  prior rc={prior_rc}")
        ok_all = ok_all and want
    print(f"FORGERY_REFUSED={refused}/6 PRIOR_ACCEPTED={accepted_prior}/6 POSITIVE={'pass' if positives == 1 else 'FAIL'}")
    print(f"CONTROL_FORGERIES_R90={'PASS' if ok_all else 'FAIL'}")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
