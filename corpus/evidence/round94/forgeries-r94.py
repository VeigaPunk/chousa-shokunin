#!/usr/bin/env python3
"""forgeries-r94 — round-94 C1 (operability) role-discrimination + carried-refusal battery.

Successor of `forgeries-r93.py`. Round 93 byte-checks every row of the pins table but the table says
nothing about what a row IS: a row for a file no expected row executes and a row for an instrument are
the same line, and nothing requires the round's claims files to be pinned. Every fixture below is a
mutation of the pins table only; the pin *population* is unchanged.

  D1 dangling-instrument   the driver row re-labelled `instrument`: nothing executes it
                           r93 (two-column projection of the same rows): PASS -> r94: PIN_ROLE_DANGLING
  D2 missing-claims        the two claims rows removed from the table
                           r93: PASS (nothing requires them) -> r94: PIN_ROLE_MISSING role=claims
  D3 mis-role-expectation  the expectations file re-labelled `receipt`
                           r93: PASS -> r94: PIN_ROLE_MISMATCH role=expectation
  D4 unknown-role          one role string replaced by `witness`
                           r93: PASS -> r94: SETUP PIN_ROLE_UNKNOWN (exit 2)
  S1 schema-two-column     the whole table written in the r93 (two-column) shape — the do-nothing form
                           r93: PASS -> r94: SETUP PIN_SCHEMA (exit 2)
  C1 carried-instrument    a byte appended to a role=`driver` pinned file: r94 PIN_DISK_MISMATCH
  C2 carried-receipt       a comment appended to a committed receipt body: r94 RECEIPT_MISMATCH
  P  positive             the landing table: r94 PASS

The r93 runs use the two-column *projection* of each fixture's rows (r93 cannot read a role column); the
projection's self row is re-digested under r93's own minus-self rule, so a projection is a legitimate
r93 table over the same population, not a broken file r93 refuses for another reason.

Usage: python3 -B corpus/evidence/round94/forgeries-r94.py --root LANE --repo GITDIR --rev FREEZE \
           --receipts-rev CARRIER --work DIR
Exit 0 every case as expected, 1 a deviation, 2 setup. No network.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
NEW = os.path.join(HERE, "control-driver-r94.py")
OLD = os.path.join(os.path.dirname(HERE), "round93", "control-driver-r93.py")
PINS_REL = "corpus/evidence/round94/instrument-pins.txt"
EXPECTED_REL = "corpus/evidence/round94/controls/expected.tsv"
RECEIPTS_REL = "corpus/evidence/round94/controls/receipts"
CLAIMS = (".ufo/waves/round-94/claims.json", ".ufo/waves/round-94/claims.md")


def refuse_work_root(work):
    """R94SentinelScope F2: every battery rmtree()s --work, so a system root is refused, never deleted."""
    bad = ("/", "/home", "/tmp", "/var/tmp", os.path.expanduser("~"), os.path.expanduser("~/"))
    if os.path.abspath(work) in bad:
        print(f"SETUP --work is not a scratch path: {work}")
        raise SystemExit(2)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_rows(path):
    rows = []
    for ln in open(path, encoding="utf-8"):
        ln = ln.rstrip("\n")
        if not ln or ln.startswith("#"):
            continue
        sha, role, rel = ln.split()
        rows.append([sha, role, rel])
    return rows


def write_r94(path, rows, self_rel):
    body = "".join(f"{sha}  {role}  {rel}\n" for sha, role, rel in rows if rel != self_rel)
    self_sha = hashlib.sha256(body.encode()).hexdigest()
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
        fh.write(f"{self_sha}  driver  {self_rel}\n")


def write_r93(path, rows, self_rel):
    body = "".join(f"{sha}  {rel}\n" for sha, _role, rel in rows if rel != self_rel)
    self_sha = hashlib.sha256(body.encode()).hexdigest()
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
        fh.write(f"{self_sha}  {self_rel}\n")


def run(driver, root, work, rev, receipts_rev):
    args = [sys.executable, "-B", driver, "verify", "--root", root, "--work", work, "--rev", rev,
            "--receipts-rev", receipts_rev,
            "--expected", os.path.join(root, EXPECTED_REL),
            "--receipts", os.path.join(root, RECEIPTS_REL),
            "--pins", os.path.join(root, PINS_REL)]
    p = subprocess.run(args, capture_output=True, text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--receipts-rev", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    work = os.path.abspath(a.work)
    refuse_work_root(work)
    pins = os.path.join(root, PINS_REL)
    if not os.path.isfile(pins):
        print(f"SETUP missing pins table {pins}")
        return 2
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work, exist_ok=True)

    tree = os.path.join(work, "tree")
    p = subprocess.run(["git", "clone", "--shared", "--quiet", a.repo, tree], capture_output=True, text=True)
    if p.returncode != 0:
        print(f"SETUP git clone failed: {p.stderr[:300]}")
        return 2
    p = subprocess.run(["git", "-C", tree, "checkout", "--quiet", a.receipts_rev], capture_output=True, text=True)
    if p.returncode != 0:
        print(f"SETUP git checkout {a.receipts_rev} failed: {p.stderr[:300]}")
        return 2
    tpins = os.path.join(tree, PINS_REL)
    base_rows = parse_rows(tpins)
    selftree_pins = os.path.join(work, "pristine-pins.txt")
    shutil.copy2(tpins, selftree_pins)

    results = {}
    old_rcs = {}

    def case(name, rows_mutator, want_r94_rc, want_needles, expect_r93_rc=0):
        rows = [list(r) for r in base_rows]
        if rows_mutator is not None:
            rows_mutator(rows, tree)
        write_r94(tpins, rows, PINS_REL)
        rc_new, out_new = run(NEW, tree, os.path.join(work, "w-" + name), a.rev, a.receipts_rev)
        write_r93(tpins, rows, PINS_REL)
        rc_old, out_old = run(OLD, tree, os.path.join(work, "o-" + name), a.rev, a.receipts_rev)
        new_ok = rc_new == want_r94_rc and all(n in out_new for n in want_needles)
        old_ok = rc_old == expect_r93_rc
        results[name] = new_ok and old_ok
        old_rcs[name] = rc_old
        print(f"{'OK' if results[name] else 'FAIL'} {name}: r93 rc={rc_old} r94 rc={rc_new}"
              f" needles={'+'.join(want_needles) if want_needles else '-'}")
        if not results[name]:
            print("  r94:", " | ".join(ln for ln in out_new.splitlines()
                                       if ln.startswith(("PIN_", "SETUP", "RECEIPT PINS", "CONTROL_DRIVER")))[-500:])
        shutil.copy2(selftree_pins, tpins)
        return results[name]

    def relabel(old_role, new_role):
        def mut(rows, _tree):
            hit = [r for r in rows if r[1] == old_role]
            if not hit:
                raise SystemExit(f"SETUP no row with role={old_role}")
            hit[0][1] = new_role
        return mut

    def drop(paths):
        def mut(rows, _tree):
            keep = [r for r in rows if r[2] not in paths]
            if len(keep) == len(rows):
                raise SystemExit(f"SETUP no row among {paths}")
            rows[:] = keep
        return mut

    def unknown_role(rows, _tree):
        rows[0][1] = "witness"

    case("d1-dangling-instrument", relabel("driver", "instrument"), 1,
         ["PIN_ROLE_DANGLING role=instrument"])
    case("d2-missing-claims", drop(set(CLAIMS)), 1, ["PIN_ROLE_MISSING role=claims"])
    case("d3-mis-role-expectation", relabel("expectation", "receipt"), 1,
         ["PIN_ROLE_MISMATCH role=expectation"])
    case("d4-unknown-role", unknown_role, 2, ["SETUP PIN_ROLE_UNKNOWN"])

    # The do-nothing form: the r93-shaped table (the schema the round would keep without the role work).
    write_r93(tpins, base_rows, PINS_REL)
    rc_old, _out_old = run(OLD, tree, os.path.join(work, "o-schema"), a.rev, a.receipts_rev)
    rc_new, out_new = run(NEW, tree, os.path.join(work, "w-schema"), a.rev, a.receipts_rev)
    schema_ok = rc_old == 0 and rc_new == 2 and "SETUP PIN_SCHEMA" in out_new
    results["s0-schema-prior"] = schema_ok
    print(f"{'OK' if schema_ok else 'FAIL'} s0-schema-prior: r93 rc={rc_old} (two-column table scores)"
          f" r94 rc={rc_new} (PIN_SCHEMA)")

    # Carried refusals (regression of the r93 pin walk): a tampered driver row and a tampered receipt body.
    shutil.copy2(selftree_pins, tpins)
    driver_rel = next(r[2] for r in base_rows if r[2].endswith("control-driver-r94.py"))
    with open(os.path.join(tree, driver_rel), "a", encoding="utf-8") as fh:
        fh.write("# tampered\n")
    rc_c1, out_c1 = run(NEW, tree, os.path.join(work, "w-c1"), a.rev, a.receipts_rev)
    ok_c1 = rc_c1 == 1 and "PIN_DISK_MISMATCH path=" + driver_rel in out_c1
    results["c1-carried-instrument"] = ok_c1
    print(f"{'OK' if ok_c1 else 'FAIL'} c1-carried-instrument: r94 rc={rc_c1} (PIN_DISK_MISMATCH)")
    subprocess.run(["git", "-C", tree, "checkout", "--quiet", "--", driver_rel], check=False)

    receipts_dir = os.path.join(tree, RECEIPTS_REL)
    victim = os.path.join(receipts_dir, sorted(f for f in os.listdir(receipts_dir) if f.endswith(".txt"))[0])
    with open(victim, "a", encoding="utf-8") as fh:
        fh.write("# tampered\n")
    rc_c2, out_c2 = run(NEW, tree, os.path.join(work, "w-c2"), a.rev, a.receipts_rev)
    ok_c2 = rc_c2 == 1 and "RECEIPT_MISMATCH:" in out_c2
    results["c2-carried-receipt"] = ok_c2
    print(f"{'OK' if ok_c2 else 'FAIL'} c2-carried-receipt: r94 rc={rc_c2} (RECEIPT_MISMATCH)")
    subprocess.run(["git", "-C", tree, "checkout", "--quiet", "--", os.path.relpath(victim, tree)], check=False)

    # Positive: the landing table scores.
    shutil.copy2(selftree_pins, tpins)
    rc_p, out_p = run(NEW, tree, os.path.join(work, "w-p"), a.rev, a.receipts_rev)
    pos_ok = rc_p == 0 and "CONTROL_DRIVER_R94=PASS" in out_p
    results["positive"] = pos_ok
    print(f"{'OK' if pos_ok else 'FAIL'} positive: r94 rc={rc_p}")

    role_names = ("d1-dangling-instrument", "d2-missing-claims", "d3-mis-role-expectation", "d4-unknown-role")
    role_forgeries = sum(1 for n in role_names if results.get(n))
    # Prior acceptance is its own measurement (R94ExecC1Repro F2): the r93 run's rc on the projected table,
    # not the r94 case's result printed twice.
    prior = sum(1 for n in role_names if old_rcs.get(n) == 0)
    carried = sum(1 for n in ("c1-carried-instrument", "c2-carried-receipt") if results.get(n))
    ok = all(results.values())
    shutil.rmtree(tree, ignore_errors=True)
    print(f"FORGERIES={'PASS' if ok else 'FAIL'} FORGERY_REFUSED={role_forgeries}/4 PRIOR_ACCEPTED={prior}/4 "
          f"SCHEMA_REFUSED={int(schema_ok)}/1 SCHEMA_PRIOR_ACCEPTED={int(schema_ok)}/1 "
          f"CARRIED_REFUSED={carried}/2 POSITIVE={'pass' if pos_ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
