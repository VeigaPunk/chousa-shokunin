#!/usr/bin/env python3
"""forgeries-r93 — round-93 C1 (operability) discrimination + derivation battery.

Successor of `forgeries-r92.py`. The r92 driver byte-checks only the instruments its expected rows
execute plus the expectations and pins files (`RECEIPT PINS OK 7/16`), and it reads the committed
receipts without pinning them. Round 93's driver walks the whole pins table and pins each receipt.
This battery builds one archive of the landing revision and applies two forgeries that the r92 driver
accepts on the same bytes:

  F1 unexecuted-instrument  a byte appended to a pinned instrument no expected row executes
                            r92: PINS OK 7/16, rc 0 -> r93: PIN_DISK_MISMATCH path=<rel>, rc 1
  F2 receipt-body           a comment line appended to one committed receipt
                            r92: rc 0 (receipts are not pinned) -> r93: RECEIPT_MISMATCH:<case>, rc 1

Plus the derivation class (T3): with `--root` naming the archive and no explicit `--expected`,
`--receipts` or `--pins`, the r92 driver resolves its defaults from its own directory and refuses
(`SETUP path escapes base`, rc 1) while the r93 driver derives them from `--root` and scores normally
(`DERIVE_OK`). The pristine archive is the positive control for both drivers.

Every run is read-only: the archive is extracted under `--work` and each forgery gets its own copy.

Usage: python3 -B corpus/evidence/round93/forgeries-r93.py --root LANE --repo GITDIR --rev REV \
           --receipts-rev REV --work DIR
Exit 0 both forgeries refused by r93 and accepted by r92, derivation and positive as expected; 1 a
deviation; 2 setup. No network.
"""
import argparse
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
NEW = os.path.join(HERE, "control-driver-r93.py")
OLD = os.path.join(os.path.dirname(HERE), "round92", "control-driver-r92.py")
UNEXECUTED = "corpus/evidence/round93/curation-controls-r93.py"
RECEIPT = "controls/receipts/c2-prior-landing.txt"


def clone(repo, rev, dest):
    """A shared clone at `rev`: the fresh legs run instruments that need a git dir (`--repo @ROOT@`,
    `git -C @ROOT@ show`), so a bare `git archive` tree cannot host them."""
    p = subprocess.run(["git", "clone", "--shared", "--quiet", repo, dest], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"SETUP git clone failed: {p.stderr[:300]}")
    p = subprocess.run(["git", "-C", dest, "checkout", "--quiet", rev], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"SETUP git checkout {rev} failed: {p.stderr[:300]}")
    return dest


def run(driver, root, work, rev, receipts_rev, explicit=True, repo=None, in_tree=False):
    """`in_tree` runs the copy of the driver the tree carries (the `--root <tree> --repo <tree>` form);
    otherwise the lane's copy runs against a foreign root (the dispatch form the DERIVE case measures)."""
    if in_tree:
        cand = os.path.join(root, os.path.relpath(driver, LANE))
        if os.path.isfile(cand):
            driver = cand
    args = [sys.executable, "-B", driver, "verify", "--root", root, "--work", work, "--rev", rev,
            "--receipts-rev", receipts_rev]
    if repo:
        args += ["--repo", repo]
    if explicit:
        args += ["--expected", os.path.join(root, "corpus/evidence/round93/controls/expected.tsv"),
                 "--receipts", os.path.join(root, "corpus/evidence/round93/controls/receipts"),
                 "--pins", os.path.join(root, "corpus/evidence/round93/instrument-pins.txt")]
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
    repo = os.path.abspath(a.repo)
    work = os.path.abspath(a.work)
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work, exist_ok=True)
    pristine = clone(repo, a.receipts_rev, os.path.join(work, "pristine"))

    def fresh(name):
        # every forgery gets its own clone so the fresh legs keep a real git dir
        return clone(repo, a.receipts_rev, os.path.join(work, name))

    def both(tree):
        # r92 is scored without --repo: its self_pin would compare the receipt rows (which r93 added to the
        # table) at --rev, a revision that never held them — a harness artefact, not the class under test.
        return (run(OLD, tree, os.path.join(work, "w92-" + os.path.basename(tree)), a.rev, a.receipts_rev,
                    in_tree=True),
                run(NEW, tree, os.path.join(work, "w93-" + os.path.basename(tree)), a.rev, a.receipts_rev,
                    repo=tree, in_tree=True))

    results = []

    def forgery(name, mutate, code):
        tree = fresh(name)
        mutate(tree)
        (rc_old, out_old), (rc_new, out_new) = both(tree)
        prior = rc_old == 0 and "CONTROL_DRIVER_R92=PASS" in out_old
        refused = rc_new == 1 and code in out_new
        ok = prior and refused
        print(f"{'OK' if ok else 'FAIL'} {name}: r93 rc={rc_new} ({code}), r92 rc={rc_old} accepted={prior}")
        if not ok:
            print("  r93 last:", " | ".join(out_new.strip().splitlines()[-3:]))
            print("  r92 last:", " | ".join(out_old.strip().splitlines()[-3:]))
        results.append(ok)

    def append(path, text):
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(text)

    forgery("unexecuted-instrument",
            lambda t: append(os.path.join(t, UNEXECUTED), "\n# tampered\n"),
            "PIN_DISK_MISMATCH path=" + UNEXECUTED)
    forgery("receipt-body",
            lambda t: append(os.path.join(t, "corpus/evidence/round93", RECEIPT), "# tampered\n"),
            "RECEIPT_MISMATCH:c2-prior-landing")

    # Derivation: no explicit paths; r92's own-directory defaults escape the archive root, r93's
    # --root derivation scores the same archive normally.
    rc_old_d, out_old_d = run(OLD, pristine, os.path.join(work, "w92-derive"), a.rev, a.receipts_rev,
                              explicit=False)
    # the dispatch form: the LANE's driver scored against a foreign root, with --repo naming the lane
    rc_new_d, out_new_d = run(NEW, pristine, os.path.join(work, "w93-derive"), a.rev, a.receipts_rev,
                              explicit=False, repo=LANE)
    derive_ok = rc_old_d != 0 and "escapes base" in out_old_d and rc_new_d == 0 \
        and "CONTROL_DRIVER_R93=PASS" in out_new_d
    print(f"{'OK' if derive_ok else 'FAIL'} derive-from-root: r92 rc={rc_old_d} "
          f"({'escapes base' if 'escapes base' in out_old_d else 'other refusal'}), r93 rc={rc_new_d}")
    if not derive_ok:
        print("  r92 derive:", " | ".join(out_old_d.strip().splitlines()[-3:]))
        print("  r93 derive:", " | ".join(out_new_d.strip().splitlines()[-3:]))

    # Regression classes found by the wave's own reviewer (R93ReviewerC1 H2/M1): deleting the pins table's
    # self row, and a pin row naming a path outside --root, must both be refused at the tree.
    def regression(name, mutate, code):
        tree = fresh(name)
        mutate(tree)
        rc, out = run(NEW, tree, os.path.join(work, "w93-" + name), a.rev, a.receipts_rev,
                      repo=tree, in_tree=True)
        ok = rc == 1 and code in out
        print(f"{'OK' if ok else 'FAIL'} {name}: r93 rc={rc} ({code})")
        if not ok:
            print("  last:", " | ".join(out.strip().splitlines()[-3:]))
        return ok

    pins_rel = "corpus/evidence/round93/instrument-pins.txt"
    reg_self = regression(
        "self-row-deleted",
        lambda t: open(os.path.join(t, pins_rel), "w").write(
            "".join(ln for ln in open(os.path.join(t, pins_rel), encoding="utf-8")
                    if not ln.strip().endswith(pins_rel))),
        "PIN_SELF_ROW_ABSENT")
    reg_outside = regression(
        "row-outside-root",
        lambda t: open(os.path.join(t, pins_rel), "a").write(
            "0" * 64 + "  /etc/hostname\n"),
        "PIN_ROW_OUTSIDE")

    (rc_old_p, out_old_p), (rc_new_p, out_new_p) = both(pristine)
    positive = rc_old_p == 0 and rc_new_p == 0
    print(f"{'OK' if positive else 'FAIL'} positive: r92 rc={rc_old_p} r93 rc={rc_new_p}")

    refused_n = sum(1 for r in results if r)
    prior_n = refused_n  # each refused forgery was accepted by r92 in its own run above
    reg_n = int(reg_self) + int(reg_outside)
    ok = refused_n == 2 and derive_ok and positive and reg_n == 2
    print(f"FORGERY_REFUSED={refused_n}/2 PRIOR_ACCEPTED={prior_n}/2 DERIVE_OK={int(derive_ok)}/1 "
          f"REGRESSION_REFUSED={reg_n}/2 POSITIVE={'pass' if positive else 'fail'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
