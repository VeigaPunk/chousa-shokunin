#!/usr/bin/env python3
"""R75ExecB: mechanically diff contract-derived case expectations against the
matrix's printed expected_rc/expected_failed for both recorded runs.

Derived table encodes the derivation in derived-expectations.md (from the
frozen r74 correction-count contract only), NOT loader-matrix-v2.py's CASES.

Exit 0 iff every printed expectation in every supplied log equals the derived
value; nonzero on any mismatch. Counter ACTUAL results are reported but do not
affect the exit (the diff under test is derived-vs-printed, not actual-vs-printed).
"""
import re
import sys

DERIVED = {
    "unchanged":          (0, frozenset()),
    "append-0":           (0, frozenset()),
    "append-1":           (0, frozenset()),
    "append-2":           (0, frozenset()),
    "delete-0":           (1, frozenset({"C2-6"})),
    "delete-1":           (1, frozenset({"C2-6"})),
    "delete-2":           (1, frozenset({"C2-6"})),
    "replace-equal":      (1, frozenset({"C2-6"})),
    "receipt-change":     (1, frozenset({"C2-7"})),
    "dup-log-heading":    (1, frozenset({"C2-1", "C2-2"})),
    "dup-lesson-heading": (1, frozenset({"C2-3", "C2-5"})),
    "dup-card-heading":   (1, frozenset({"C2-4"})),
}
ORDER = ["unchanged", "append-0", "append-1", "append-2", "delete-0", "delete-1",
         "delete-2", "replace-equal", "receipt-change", "dup-log-heading",
         "dup-lesson-heading", "dup-card-heading"]

CASE_RE = re.compile(
    r"^CASE (\S+) (PASS|FAIL) expected_rc=(\d+) actual_rc=(-?\d+) "
    r"failed=(\S*) expected_failed=(\S*) ")


def as_set(tok):
    """Matrix prints 'none' for an empty failed-check set."""
    return frozenset(x for x in tok.split(",") if x and x != "none")


def parse(path):
    cases, seed, counter, summary = {}, None, None, None
    for line in open(path, encoding="utf-8"):
        if line.startswith("COUNTER_SHA256="):
            counter = line.strip()
        elif line.startswith("SEED="):
            seed = line.strip()
        elif line.startswith("LOADER_MATRIX="):
            summary = line.strip()
        else:
            m = CASE_RE.match(line)
            if m:
                name, verdict, erc, arc, failed, efailed = m.groups()
                cases[name] = {
                    "verdict": verdict,
                    "expected_rc": int(erc),
                    "actual_rc": int(arc),
                    "failed": as_set(failed),
                    "expected_failed": as_set(efailed),
                }
    return {"cases": cases, "seed": seed, "counter": counter, "summary": summary}


def fmt(s):
    return ",".join(sorted(s)) or "none"


def main(paths):
    any_mismatch = False
    for path in paths:
        d = parse(path)
        file_mismatches = 0
        print(f"=== {path}")
        print(d["counter"] or "COUNTER_SHA256=<missing>")
        print(d["seed"] or "SEED=<missing>")
        print(d["summary"] or "LOADER_MATRIX=<missing>")
        for name in ORDER:
            c = d["cases"].get(name)
            derc, derf = DERIVED[name]
            if c is None:
                print(f"{name}: MISSING-FROM-LOG")
                file_mismatches += 1
                continue
            ok = c["expected_rc"] == derc and c["expected_failed"] == derf
            if not ok:
                file_mismatches += 1
            print(f"{name}: printed(rc={c['expected_rc']},failed={fmt(c['expected_failed'])}) "
                  f"derived(rc={derc},failed={fmt(derf)}) "
                  f"DERIVED_VS_PRINTED={'MATCH' if ok else 'MISMATCH'}; "
                  f"counter_actual rc={c['actual_rc']} failed={fmt(c['failed'])} "
                  f"case_verdict={c['verdict']}")
        extra = sorted(set(d["cases"]) - set(ORDER))
        if extra:
            print("EXTRA CASES IN LOG:", extra)
            file_mismatches += len(extra)
        if file_mismatches:
            any_mismatch = True
        print(f"FILE_DIFF={file_mismatches} mismatch(es) across {len(ORDER)} cases")
    verdict = "ALL MATCH (no expectation decided by the diff alone)" if not any_mismatch \
        else "MISMATCH PRESENT"
    print(f"DERIVED_VS_PRINTED={verdict}")
    return 0 if not any_mismatch else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
