#!/usr/bin/env python3
"""Check a seat's description of a record's defect against the record's bytes.

A description like "reason present, flip empty" is a claim about two table cells.
This checker reads the record, finds the kept-rejection table under any heading
containing "reject" (the convention research-gate.sh uses since round 82), and
tests each described leg: is the reason cell non-placeholder? is the flip cell
empty or declared-vocabulary?

Exit 0 when every described leg is present in the bytes, exit 1 otherwise --
so a description that does not match the record fails.

usage: check-described-form.py <record.md> [--reason present|absent] [--flip absent|present]
"""
import re
import sys

PLACEHOLDERS = {
    "", "-", "--", "---", "\u2014", "\u2013", "n/a", "na", "n.a", "none", "nil",
    "null", "tbd", "tba", "todo", "?", "??", "...", "\u2026", "x", "unknown",
    "not applicable", "same", "ditto", "see above", "idem",
}


def norm(cell):
    c = cell.strip().lower().replace("`", "").replace("'", "").replace('"', "")
    c = c.replace("*", "").replace("_", "")
    c = " ".join(c.split())
    return c.rstrip(".").strip()


def cell_is_placeholder(cell):
    return norm(cell) in PLACEHOLDERS


def rejections(path):
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    rows, heading, header_seen = [], None, False
    for ln in lines:
        if ln.startswith("## "):
            heading = ln
            header_seen = False
            continue
        if heading is None or "reject" not in heading.lower():
            continue
        if not ln.strip().startswith("|"):
            header_seen = False
            continue
        cells = [c for c in ln.strip().strip("|").split("|")]
        if not header_seen:
            header_seen = True  # column header row
            continue
        if len(cells) < 4 or set(cells[0].strip()) <= set("-: "):
            continue
        rows.append({"id": cells[0].strip(), "reason": cells[2], "flip": cells[3], "heading": heading})
    return rows


def main(argv):
    path = argv[1]
    want = {"reason": None, "flip": None}
    i = 2
    while i + 1 < len(argv):
        if argv[i] in ("--reason", "--flip"):
            want[argv[i][2:]] = argv[i + 1]
        i += 2
    rows = rejections(path)
    bad = 0
    print(f"RECORD {path}")
    print(f"REJECTIONS rows under a reject heading: {len(rows)}")
    for r in rows:
        reason_present = not cell_is_placeholder(r["reason"])
        flip_present = not cell_is_placeholder(r["flip"])
        print(f"  id={r['id']} heading={r['heading'].strip()!r} "
              f"reason_present={int(reason_present)} flip_present={int(flip_present)}")
        for leg, described, actual in (("reason", want["reason"], reason_present),
                                       ("flip", want["flip"], flip_present)):
            if described is None:
                continue
            expected = described == "present"
            if actual != expected:
                print(f"  DESCRIBED-FORM MISMATCH id={r['id']} leg={leg} "
                      f"described={described} bytes={'present' if actual else 'absent'}")
                bad += 1
                continue
            print(f"  DESCRIBED-FORM OK id={r['id']} leg={leg} described={described}")
    print(f"DESCRIBED_FORM bad={bad}")
    print(f"RC={1 if bad else 0}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
