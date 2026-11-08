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
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
NEW = os.path.join(HERE, "control-driver-r93.py")
OLD = os.path.join(os.path.dirname(HERE), "round92", "control-driver-r92.py")
UNEXECUTED = "corpus/evidence/round93/curation-controls-r93.py"
RECEIPT = "controls/receipts/c2-prior-landing.txt"


def archive(repo, rev, dest):
    p = subprocess.run(["git", "-C", repo, "archive", rev], capture_output=True)
    if p.returncode != 0:
        raise SystemExit(f"SETUP git archive {rev} failed: {p.stderr.decode(errors='replace')[:300]}")
    tar = os.path.join(os.path.dirname(dest), "tree.tar")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(tar, "wb") as fh:
        fh.write(p.stdout)
    os.makedirs(dest, exist_ok=True)
    with tarfile.open(tar) as tf:
        tf.extractall(dest)
    os.remove(tar)
    return dest


def run(driver, root, work, rev, receipts_rev, explicit=True):
    args = [sys.executable, "-B", driver, "verify", "--root", root, "--work", work, "--rev", rev,
            "--receipts-rev", receipts_rev]
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
    pristine = archive(repo, a.receipts_rev, os.path.join(work, "pristine"))

    def fresh(name):
        d = os.path.join(work, name)
        shutil.copytree(pristine, d, symlinks=True)
        return d

    def both(tree):
        return (run(OLD, tree, os.path.join(work, "w92-" + os.path.basename(tree)), a.rev, a.receipts_rev),
                run(NEW, tree, os.path.join(work, "w93-" + os.path.basename(tree)), a.rev, a.receipts_rev))

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
    rc_new_d, out_new_d = run(NEW, pristine, os.path.join(work, "w93-derive"), a.rev, a.receipts_rev,
                              explicit=False)
    derive_ok = rc_old_d != 0 and "escapes base" in out_old_d and rc_new_d == 0 \
        and "CONTROL_DRIVER_R93=PASS" in out_new_d
    print(f"{'OK' if derive_ok else 'FAIL'} derive-from-root: r92 rc={rc_old_d} "
          f"({'escapes base' if 'escapes base' in out_old_d else 'other refusal'}), r93 rc={rc_new_d}")
    if not derive_ok:
        print("  r92 derive:", " | ".join(out_old_d.strip().splitlines()[-3:]))
        print("  r93 derive:", " | ".join(out_new_d.strip().splitlines()[-3:]))

    (rc_old_p, out_old_p), (rc_new_p, out_new_p) = both(fresh("positive"))
    positive = rc_old_p == 0 and rc_new_p == 0
    print(f"{'OK' if positive else 'FAIL'} positive: r92 rc={rc_old_p} r93 rc={rc_new_p}")

    refused_n = sum(1 for r in results if r)
    prior_n = refused_n  # each refused forgery was accepted by r92 in its own run above
    ok = refused_n == 2 and derive_ok and positive
    print(f"FORGERY_REFUSED={refused_n}/2 PRIOR_ACCEPTED={prior_n}/2 DERIVE_OK={int(derive_ok)}/1 "
          f"POSITIVE={'pass' if positive else 'fail'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
