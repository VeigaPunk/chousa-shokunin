#!/usr/bin/env python3
"""R94CriticClaims C1 wording probe: mutate the pins table in the scratch clone, run the counting
command, record the printed ratios/codes. Restores the pristine table after every case.
Usage: c1mut.py [case ...]   (no args = all cases)"""
import hashlib
import os
import shutil
import subprocess
import sys

ROOT = "/fast/scratch/hyaku/chousa-r94/R94CriticClaims/repo"
PINS_REL = "corpus/evidence/round94/instrument-pins.txt"
SELF_REL = PINS_REL
DRIVER = os.path.join(ROOT, "corpus/evidence/round94/control-driver-r94.py")
REV = "41038ed7c40cffc4cf86d649a6ba433c4b9eec1a"
CARRIER = "352924bbea624caf3771ef291be98fd4ec679dda"
WORK = "/fast/scratch/hyaku/chousa-r94/R94CriticClaims/c1/mutwork"
OUT = "/fast/scratch/hyaku/chousa-r94/R94CriticClaims/c1"
CENSUS = "corpus/evidence/round94/census-start.txt"


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


def run(work):
    args = [sys.executable, "-B", DRIVER, "verify", "--root", ROOT, "--repo", ROOT,
            "--rev", REV, "--receipts-rev", CARRIER, "--work", work]
    p = subprocess.run(args, capture_output=True, text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def main():
    only = set(sys.argv[1:])
    os.makedirs(OUT, exist_ok=True)
    pristine_bytes = open(os.path.join(ROOT, PINS_REL), "rb").read()
    base_rows = parse_rows(os.path.join(ROOT, PINS_REL))
    census_sha = sha256_file(os.path.join(ROOT, CENSUS))

    def relabel(old_role, new_role):
        rows = [list(r) for r in base_rows]
        hit = [r for r in rows if r[1] == old_role]
        if not hit:
            raise SystemExit(f"no role={old_role}")
        hit[0][1] = new_role
        return rows

    def drop(path):
        rows = [list(r) for r in base_rows if r[2] != path]
        if len(rows) == len(base_rows):
            raise SystemExit(f"no row {path}")
        return rows

    def add(sha, role, rel):
        return [list(r) for r in base_rows] + [[sha, role, rel]]

    cases = [
        ("pristine", lambda: [list(r) for r in base_rows]),
        ("expectation-relabel-receipt", lambda: relabel("expectation", "receipt")),
        ("claims-drop-md", lambda: drop(".ufo/waves/round-94/claims.md")),
        ("claims-extra", lambda: add(census_sha, "claims", CENSUS)),
        ("expectation-extra", lambda: add(census_sha, "expectation", CENSUS)),
        ("driver-drop-make-pins", lambda: drop("corpus/evidence/round94/make-pins-r94.py")),
        ("driver-invent", lambda: add(census_sha, "driver", CENSUS)),
        ("role-unknown", lambda: [["0" * 64, "witness", CENSUS]] + [list(r) for r in base_rows]),
    ]
    report = []
    for name, mut in cases:
        if only and name not in only:
            continue
        rows = mut()
        write_r94(os.path.join(ROOT, PINS_REL), rows, SELF_REL)
        rc, out = run(os.path.join(WORK, name))
        open(os.path.join(OUT, f"mut-{name}.txt"), "w", encoding="utf-8").write(f"# rc={rc}\n" + out)
        keep = [ln for ln in out.splitlines()
                if ln.startswith(("PIN_ROLE_FINDING", "RECEIPT PINS", "RECEIPT SELF_PIN", "SETUP",
                                  "COMMITTED_OK", "PINNED_FILES", "CONTROL_DRIVER_R94"))]
        report.append((name, rc, keep))
        open(os.path.join(ROOT, PINS_REL), "wb").write(pristine_bytes)
        print(f"## {name} rc={rc}")
        for ln in keep:
            print(ln)
    if not only or "schema-two-column" in only:
        write_r93(os.path.join(ROOT, PINS_REL), base_rows, SELF_REL)
        rc, out = run(os.path.join(WORK, "schema"))
        open(os.path.join(OUT, "mut-schema-two-column.txt"), "w", encoding="utf-8").write(f"# rc={rc}\n" + out)
        keep = [ln for ln in out.splitlines() if ln.startswith(("SETUP", "CONTROL_DRIVER"))]
        report.append(("schema-two-column", rc, keep))
        open(os.path.join(ROOT, PINS_REL), "wb").write(pristine_bytes)
        print(f"## schema-two-column rc={rc}")
        for ln in keep:
            print(ln)
    open(os.path.join(OUT, "mutations.out"), "a", encoding="utf-8").write(
        "".join(f"## {n} rc={rc}\n" + "".join(l + "\n" for l in keep) for n, rc, keep in report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
