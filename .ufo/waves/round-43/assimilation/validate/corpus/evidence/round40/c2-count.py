#!/usr/bin/env python3
"""Count evidence-backed dispositions for the four routed r39 findings."""
import collections
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
FLEET = ROOT.parent
DISPOSITIONS = ROOT / "corpus/evidence/round40/routed-defect-dispositions.json"
CLAIMS39 = ROOT / "corpus/evidence/round39/claims.md"
LESSON39 = ROOT / "corpus/lessons/round-39.md"
SCORECARD = ROOT / "SCORECARD.md"
REPORT39 = FLEET / ".ufo/reports/round-39/chousa.md"
SPOTCHECK39 = ROOT / "corpus/lessons/round-39-verifier-spotcheck.md"
SPEC39 = ROOT / ".ufo/waves/round-39/w1-spec.json"
PLAN39 = ROOT / ".ufo/waves/round-39/w1-plan.json"
BASE39 = "8c7c867b66e103712ae33e1d076786f50dd3239e"
TIP39 = "6ac1007e6a5d699d0742801026554fac1d900b5d"
EXPECTED = {"R2": "corrected", "R3": "corrected", "R4": "not-reproduced", "R5": "corrected"}


def text(path):
    return path.read_text(encoding="utf-8")


def md_count(revision):
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "ls-tree", "-r", "--name-only", revision,
         "--", "corpus/knowledge"], capture_output=True, text=True, check=False)
    if proc.returncode:
        raise RuntimeError(proc.stderr.strip())
    return sum(name.endswith(".md") for name in proc.stdout.splitlines())


def tracked(path):
    return subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--error-unmatch", path],
        capture_output=True, text=True, check=False).returncode == 0


def role_mix(path, key):
    data = json.loads(path.read_text(encoding="utf-8"))
    return collections.Counter(row[key] for row in data["items"] if key in row) if key == "role" else collections.Counter(row[key] for row in data["tasks"] if key in row)


def main():
    passed = 0
    results = {}
    try:
        claims = text(CLAIMS39)
        lesson = text(LESSON39)
        scorecard = text(SCORECARD)
        report = text(REPORT39)
        spotcheck = text(SPOTCHECK39)
        dispositions = (json.loads(text(DISPOSITIONS))
                        if DISPOSITIONS.is_file() else {})

        receipt = "corpus/evidence/round39/receipts/c1-mutenv-s39003.json"
        r2 = (tracked(receipt) and (ROOT / receipt).is_file()
              and "not committed" in lesson
              and "R2" in claims and receipt in claims and "superseded" in claims
              and dispositions.get("R2", {}).get("status") == EXPECTED["R2"])

        before_count, after_count = md_count(BASE39), md_count(TIP39)
        r3 = ("29 → 31" in report and (before_count, after_count) == (50, 52)
              and "R3" in claims and "29 → 31" in claims
              and "50 → 52" in claims
              and dispositions.get("R3", {}).get("status") == EXPECTED["R3"])

        spec_mix = role_mix(SPEC39, "role")
        plan_mix = role_mix(PLAN39, "agent")
        reported_match = ("reviewer 6 / critic 5" in report
                          and "revenger 2" in report)
        closure_mismatch = "reviewer 8 / revenger 0" in spotcheck
        r4 = (spec_mix == plan_mix and spec_mix["reviewer"] == 6
              and spec_mix["revenger"] == 2 and reported_match and closure_mismatch
              and dispositions.get("R4", {}).get("status") == EXPECTED["R4"])

        freeze_discloses_l1 = "L1's construction runs" in claims
        r5 = ("two independent runners" in scorecard and freeze_discloses_l1
              and "R5" in scorecard and "two seeds" in scorecard
              and dispositions.get("R5", {}).get("status") == EXPECTED["R5"])
        results = {"R2": r2, "R3": r3, "R4": r4, "R5": r5}
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as exc:
        print(f"R39_CORRECTION_COUNTER_ERROR={exc}", file=sys.stderr)
        return 2

    for defect, ok in results.items():
        passed += int(ok)
        print(f"{defect}_DISPOSITION={'ok' if ok else 'missing-or-unverified'}")
    print(f"R39_CALIBRATION_DISPOSITIONS={passed}/4")
    return 0 if passed == 4 else 1


if __name__ == "__main__":
    sys.exit(main())
