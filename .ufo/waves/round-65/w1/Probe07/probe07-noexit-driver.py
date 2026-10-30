#!/usr/bin/env python3
"""Probe07 isolated fixture: no-exit receipt header case, one surface only.

Runs the round65 reference validator (controls/ref-receipt-pin.py) against a
single receipt whose EXIT header line has been removed, exactly matching the
frozen counter c1-count.py's 'no-exit' case construction
(valid receipt with 'EXIT=0\\n' deleted).

Expected result is derived independently from the frozen format in claims.md:
  "Format: exactly ordered REVISION full lowercase 40 hex, EXIT decimal 0..255,
   SHA256 full lowercase 64 hex plus canonical relative POSIX path, empty
   separator, nonempty output."
  and "0 consistent,1 invalid,2 usage/environment".
A receipt with no EXIT line violates the exactly-ordered header set, and also
yields fewer than 5 lines, so it must be rejected: exit 1, stdout token
RECEIPT_PIN=FAIL <reason>.

Read-only git only, explicit -C, no mutation. Receipt digest binds the blob at
the declared revision (BASE d6ed8155...), computed here from git cat-file.
"""
import hashlib, json, os, pathlib, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
BASE = "d6ed8155e9b4735639a2cf0a3e479c62f2056195"
REF = f"{LANE}/corpus/evidence/round65/controls/ref-receipt-pin.py"
OUT = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-65/w1/Probe07")
HERE = pathlib.Path("/fast/scratch/hyaku/chousa-r65/Probe07")

def sh(*argv):
    return subprocess.run(list(argv), capture_output=True, text=False)

def main():
    # lane sanity: read-only rev-parse, explicit -C
    top = subprocess.run(["git", "-C", LANE, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    head = subprocess.run(["git", "-C", LANE, "rev-parse", "HEAD"],
                          capture_output=True, text=True)

    # independently derive blob digest at declared revision (no working-tree hashing)
    q = sh("git", "-C", LANE, "cat-file", "blob", f"{BASE}:SKILL.md")
    if q.returncode != 0:
        print(q.stderr.decode(), file=sys.stderr); return 2
    digest = hashlib.sha256(q.stdout).hexdigest()

    valid = f"REVISION={BASE}\nEXIT=0\nSHA256={digest} SKILL.md\n\nmeasured output\n"
    noexit = valid.replace("EXIT=0\n", "")  # frozen c1 'no-exit' construction

    (HERE / "probe07-noexit-receipt.txt").write_text(noexit, encoding="utf-8")

    # preserved argv shape from c1-count.py
    argv = [sys.executable, "-B", REF, "--receipt",
            str(HERE / "probe07-noexit-receipt.txt"),
            "--root", LANE, "--revision", BASE]
    r = subprocess.run(argv, capture_output=True, text=True, timeout=20)

    # independent expectation from frozen format
    lines = noexit.splitlines()
    expected_rc = 1
    expected_prefix = "RECEIPT_PIN=FAIL "
    deriv = {
        "line_count": len(lines),
        "five_lines_required_by_format": len(lines) >= 5,
        "exit_line_present": any(l.startswith("EXIT=") for l in lines),
        "order_violation": True,  # EXIT slot missing from exactly-ordered header set
        "expected_rc": expected_rc,
        "expected_stdout_prefix": expected_prefix,
    }
    result = {
        "fixture": "no-exit",
        "derivation": deriv,
        "argv": argv,
        "rc": r.returncode,
        "stdout": r.stdout,
        "stderr": r.stderr,
        "observed_matches_expected": (r.returncode == expected_rc
                                      and r.stdout.startswith(expected_prefix)),
        "lane_toplevel": top.stdout.strip(),
        "lane_head": head.stdout.strip(),
        "lane_head_is_freeze": head.stdout.strip() == "f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd",
        "revision_used": BASE,
        "blob_sha256": digest,
        "receipt_bytes": len(noexit.encode()),
        "py": sys.version,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "probe07-noexit-run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (OUT / "probe07-noexit-receipt.txt").write_text(noexit, encoding="utf-8")
    print(json.dumps({"rc": r.returncode, "stdout": r.stdout.strip(),
                      "stderr": r.stderr.strip(),
                      "match": result["observed_matches_expected"]}))
    return 0 if result["observed_matches_expected"] else 1

if __name__ == "__main__":
    sys.exit(main())
