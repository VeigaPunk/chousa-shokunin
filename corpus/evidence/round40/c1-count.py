#!/usr/bin/env python3
"""Count r39 receipts that verify against their committed input bytes."""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "corpus/evidence/round40/active-r39-receipts.tsv"
VERIFIER = ROOT / "corpus/evidence/round39/verify-receipts.py"
EXPECTATIONS = ROOT / "corpus/evidence/round39/expectations.jsonl"
EXPECTED_ACTIVE = 6


def main():
    rows = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or line.startswith("receipt\t"):
            continue
        fields = line.split("\t")
        if len(fields) != 3:
            print("R39_RECEIPT_MANIFEST=malformed", file=sys.stderr)
            return 2
        rows.append(fields)
    if len(rows) != EXPECTED_ACTIVE or len({row[0] for row in rows}) != EXPECTED_ACTIVE:
        print("R39_RECEIPT_MANIFEST=unexpected-population", file=sys.stderr)
        return 2

    passed = 0
    for receipt, gate, counter in rows:
        proc = subprocess.run(
            [sys.executable, str(VERIFIER), "--receipt", str(ROOT / receipt),
             "--gate", str(ROOT / gate), "--counter", str(ROOT / counter),
             "--expectations", str(EXPECTATIONS)],
            cwd=ROOT, capture_output=True, text=True, check=False)
        output = (proc.stdout or proc.stderr).strip()
        ok = proc.returncode == 0 and output.startswith("VERIFY: ok ")
        passed += int(ok)
        print(f"{receipt}: {'ok' if ok else 'fail'} {output}")
    print(f"R39_ACTIVE_RECEIPTS={passed}/{EXPECTED_ACTIVE}")
    return 0 if passed == EXPECTED_ACTIVE else 1


if __name__ == "__main__":
    sys.exit(main())
