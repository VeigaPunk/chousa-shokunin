#!/usr/bin/env python3
"""R78ExecB independent `--work` contract probe — NOT the control, and not the predicate.

Everything here re-derives, outside `corpus/evidence/round78/work-contract.py`, what the
`--work` contract control asserts, and adds the edges the control does not touch:

  P1  v5 leaves a caller's sentinel BYTE-identical (crlf/nul/trailing-space/no-final-newline
      payload) and adds/removes nothing in the caller's directory, on a run where the forger
      is refused (battery exit 1).
  P2  same, on a run where the battery PASSes (exit 0, legitimate positive matrix).
  P3  `--work` is a regular file -> exit 2, exactly one stderr line, no traceback, the file's
      own bytes unchanged.
  P4  `--work` under an unwritable parent -> exit 2, no traceback.
  P5  a missing subject -> exit 2 and (defect hunt) does the run dir it created get removed?
      Probed with a byte-identical scratch copy of the instrument whose HERE-relative subject
      table therefore resolves to nothing; the copy's sha256 is asserted equal to the
      frozen instrument's.
  P6  `--work` reached through a symlink -> sentinel survives, the symlink itself survives.
  P7  the parent of `--work` gains nothing.

Fail-closed: any check that does not hold prints FAIL and the process exits 1.
Usage: probe-work-contract.py --lane LANE_ROOT --scratch DIR
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys

RESULTS: list[tuple[str, bool, str]] = []
PARENTS: dict[str, list[str]] = {}


def check(name: str, ok: bool, detail: str) -> None:
    RESULTS.append((name, ok, detail))
    print(f"{'ok  ' if ok else 'FAIL'} {name}: {detail}")


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def manifest(root: pathlib.Path) -> dict[str, str]:
    """Relative-path -> sha256 for every regular file under root, plus dirs as DIR entries."""
    out: dict[str, str] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        base = pathlib.Path(dirpath)
        for d in dirnames:
            out[str((base / d).relative_to(root)) + "/"] = "DIR"
        for f in filenames:
            p = base / f
            if p.is_symlink():
                out[str(p.relative_to(root))] = "LINK->" + os.readlink(p)
            else:
                out[str(p.relative_to(root))] = sha(p)
    return out


def run(battery: pathlib.Path, matrix: pathlib.Path, work: str, runs: int = 1,
        timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-B", str(battery), "--matrix", str(matrix),
                           "--work", work, "--runs", str(runs),
                           "--matrix-timeout", str(timeout)],
                          stdin=subprocess.DEVNULL, capture_output=True, text=True,
                          timeout=900)


TRICKY = b"the caller put this here\r\n\x00tab\there   \ntrailing spaces   \nno final newline"


def seed(work: pathlib.Path) -> None:
    work.mkdir(parents=True)
    (work / "caller-file.txt").write_bytes(TRICKY)
    (work / "other.bin").write_bytes(bytes(range(256)))
    (work / "keep").mkdir()
    (work / "keep" / "deep.txt").write_bytes(b"deep\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--scratch", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    scratch = pathlib.Path(a.scratch).resolve()
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)

    v5 = lane / "corpus/evidence/round78/matrix-battery-v5.py"
    a1 = lane / "corpus/evidence/round78/forgers/a1-hash-identity.py"
    pos = lane / "corpus/evidence/round76/loader-matrix-v3.py"
    v5_sha = sha(v5)
    check("v5.digest", v5_sha ==
          "5545a4718690a80e5d3d6611e43132fdd5cb4dcd67e87be9a27ed44c032b5af0",
          v5_sha)

    # ---- P1: refused run, sentinel byte-identical -------------------------------
    p1 = scratch / "p1" / "work"
    p1.parent.mkdir()
    seed(p1)
    PARENTS["P1"] = sorted(q.name for q in p1.parent.iterdir())
    before = manifest(p1)
    r = run(v5, a1, str(p1))
    after = manifest(p1)
    check("P1.exit", r.returncode == 1, f"rc={r.returncode}")
    check("P1.sentinel-bytes", sha(p1 / "caller-file.txt") ==
          hashlib.sha256(TRICKY).hexdigest(),
          f"sha={sha(p1 / 'caller-file.txt')}")
    check("P1.manifest-unchanged", before == after,
          f"added={sorted(set(after) - set(before))} removed={sorted(set(before) - set(after))}")
    check("P1.no-run-debris", not any(k.startswith("r78-") for k in after),
          f"entries={sorted(after)}")
    check("P1.no-traceback", "Traceback" not in r.stderr,
          f"stderr_lines={len(r.stderr.strip().splitlines())}")
    (p1 / "stdout.txt").write_text(r.stdout)
    (p1 / "stderr.txt").write_text(r.stderr)

    # ---- P2: PASS run, sentinel byte-identical ----------------------------------
    p2 = scratch / "p2" / "work"
    p2.parent.mkdir()
    seed(p2)
    PARENTS["P2"] = sorted(q.name for q in p2.parent.iterdir())
    before2 = manifest(p2)
    r2 = run(v5, pos, str(p2))
    after2 = manifest(p2)
    last = [l for l in r2.stdout.splitlines() if l.startswith("BATTERY=")]
    check("P2.exit", r2.returncode == 0, f"rc={r2.returncode}")
    check("P2.predicate", last[-1:] == [
        "BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED"],
        f"last={last[-1:]}")
    check("P2.sentinel-bytes", sha(p2 / "caller-file.txt") ==
          hashlib.sha256(TRICKY).hexdigest(),
          f"sha={sha(p2 / 'caller-file.txt')}")
    check("P2.manifest-unchanged", before2 == after2,
          f"added={sorted(set(after2) - set(before2))} removed={sorted(set(before2) - set(after2))}")
    (p2 / "stdout.txt").write_text(r2.stdout)
    (p2 / "stderr.txt").write_text(r2.stderr)

    # ---- P3: --work is a regular file -------------------------------------------
    p3 = scratch / "p3"
    p3.mkdir()
    wf = p3 / "regular-file"
    wf.write_bytes(b"not a directory\nsecond line\n")
    fsha = sha(wf)
    r3 = run(v5, a1, str(wf))
    err3 = r3.stderr.strip().splitlines()
    check("P3.exit", r3.returncode == 2, f"rc={r3.returncode}")
    check("P3.one-line", len(err3) == 1, f"lines={len(err3)} first={err3[0][:160] if err3 else '<none>'}")
    check("P3.no-traceback", "Traceback" not in r3.stderr, "checked")
    check("P3.diagnostic-shape",
          bool(err3) and err3[0].startswith("matrix-battery-v5: cannot create --work"),
          err3[0][:160] if err3 else "<none>")
    check("P3.file-bytes-unchanged", sha(wf) == fsha, f"sha={sha(wf)}")
    check("P3.stdout-empty", r3.stdout == "", f"stdout={r3.stdout!r}")
    (p3 / "stderr.txt").write_text(r3.stderr)

    # ---- P4: --work under an unwritable parent ----------------------------------
    p4 = scratch / "p4"
    p4.mkdir()
    (p4 / "ro").mkdir()
    os.chmod(p4 / "ro", 0o555)
    r4 = run(v5, a1, str(p4 / "ro" / "child"))
    os.chmod(p4 / "ro", 0o755)
    check("P4.exit", r4.returncode == 2, f"rc={r4.returncode}")
    check("P4.no-traceback", "Traceback" not in r4.stderr,
          (r4.stderr.strip().splitlines() or ["<empty>"])[0][:160])
    (p4 / "stderr.txt").write_text(r4.stderr)

    # ---- P5: missing subject -> exit 2, and run-dir cleanup ---------------------
    p5 = scratch / "p5"
    p5.mkdir()
    copy = p5 / "matrix-battery-v5.py"
    copy.write_bytes(v5.read_bytes())
    check("P5.copy-is-instrument", sha(copy) == v5_sha, sha(copy))
    p5work = p5 / "work"
    p5work.mkdir()
    (p5work / "caller-file.txt").write_bytes(TRICKY)
    r5 = run(copy, a1, str(p5work))
    left = sorted(p.name for p in p5work.iterdir())
    check("P5.exit", r5.returncode == 2, f"rc={r5.returncode}")
    check("P5.no-traceback", "Traceback" not in r5.stderr,
          (r5.stderr.strip().splitlines() or ["<empty>"])[0][:160])
    leaked = [n for n in left if n.startswith("r78-")]
    inside = sorted(q.name for q in (p5work / leaked[0]).iterdir()) if leaked else []
    check("P5.run-dir-cleaned", left == ["caller-file.txt"],
          f"left={left} leaked_dir_empty={inside == []} inside={inside}")
    check("P5.sentinel-bytes", sha(p5work / "caller-file.txt") ==
          hashlib.sha256(TRICKY).hexdigest(), "checked")
    (p5 / "stderr.txt").write_text(r5.stderr)

    # ---- P6: --work through a symlink -------------------------------------------
    p6 = scratch / "p6"
    p6.mkdir()
    real = p6 / "real"
    seed(real)
    link = p6 / "link"
    link.symlink_to(real)
    PARENTS["P6"] = sorted(q.name for q in p6.iterdir())
    before6 = manifest(real)
    r6 = run(v5, a1, str(link))
    after6 = manifest(real)
    check("P6.exit", r6.returncode == 1, f"rc={r6.returncode}")
    check("P6.link-survives", link.is_symlink() and os.readlink(link) == str(real),
          f"is_symlink={link.is_symlink()}")
    check("P6.sentinel-bytes", sha(real / "caller-file.txt") ==
          hashlib.sha256(TRICKY).hexdigest(), "checked")
    check("P6.manifest-unchanged", before6 == after6,
          f"added={sorted(set(after6) - set(before6))} removed={sorted(set(before6) - set(after6))}")

    # ---- P7: --work's parent gains nothing --------------------------------------
    for tag, snapshot in PARENTS.items():
        now = sorted(p.name for p in (p6 if tag == "P6" else scratch / tag.lower()).iterdir())
        check(f"P7.{tag}.parent-stable", now == snapshot,
              f"before={snapshot} after={now}")

    failed = [n for n, ok, _ in RESULTS if not ok]
    print(f"PROBE={'PASS' if not failed else 'FAIL'} checks={len(RESULTS)} "
          f"failed={len(failed)}{'' if not failed else ' names=' + ','.join(failed)}")
    (scratch / "results.json").write_text(json.dumps(
        [{"check": n, "ok": ok, "detail": d} for n, ok, d in RESULTS], indent=1) + "\n")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
