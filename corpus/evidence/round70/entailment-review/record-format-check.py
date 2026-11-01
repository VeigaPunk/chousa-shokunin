#!/usr/bin/env python3
"""record-format-check — format checker for a filled entailment-review record (r70 C2 packet).

    python -I record-format-check.py --record <review-record.md> [--scope claims-scope.tsv] [--root .]

This tool checks the FORMAT of a filled entailment-review record only. It cannot and does not
check whether any verdict is CORRECT — that judgment is the reviewer's, and is the reason the
packet exists (the QUALITY-131 residual: the r66 semantic counter proves registration and form,
never entailment; a format check proves neither).

A record passes (exit 0, `REVIEW_FORMAT=PASS`) when:
  - it states `reviewer:` with a nonempty name and `reviewed-at:` with an ISO date;
  - its `## Verdicts` table has at least one verdict row;
  - every verdict row has a claim id named in the scope file (when --scope is given),
    a verdict word in {supported, contradicted, unsupported}, a reason of >= 8 words,
    an entry path that exists under --root, and an S-row id that matches `^S[0-9]{3}$`
    and appears in <root>/corpus/SOURCES.md.

Exit contract: 0 = format PASS · 1 = format FAIL (each defect named on its own `defect:` line)
· 2 = ERROR, fail-closed (record or scope unreadable/absent, --root corpus registry absent).
A record that cannot be read is never a pass.

No network, no writes. The fixtures in fixtures/ are format demonstrations only — their
verdicts are invented for the battery and are not a review of any entry.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

VERDICTS = {"supported", "contradicted", "unsupported"}
SID = re.compile(r"^S[0-9]{3}$")
ISO = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}")


def rows_of(table_lines):
    for line in table_lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 5 and cells[0] not in ("claim", "Claim", "claim id", "---", ""):
            yield cells


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--record", required=True)
    ap.add_argument("--scope", default=None)
    ap.add_argument("--root", default=".")
    a = ap.parse_args()
    root = pathlib.Path(a.root)

    reg = root / "corpus" / "SOURCES.md"
    if not reg.is_file():
        print("RECORD_FORMAT=ERROR REVIEW_FORMAT=ERROR no registry at --root/corpus/SOURCES.md (fail-closed)")
        return 2
    reg_text = reg.read_text(encoding="utf-8", errors="replace")

    scope = None
    if a.scope:
        sp = pathlib.Path(a.scope)
        if not sp.is_file():
            print("RECORD_FORMAT=ERROR REVIEW_FORMAT=ERROR scope file absent (fail-closed)")
            return 2
        scope = {line.split("#")[0].strip() + "#" + line.split("#")[1].strip()
                 for line in sp.read_text(encoding="utf-8", errors="replace").splitlines()
                 if line.strip() and not line.startswith("#")}

    rp = pathlib.Path(a.record)
    if not rp.is_file():
        print("RECORD_FORMAT=ERROR REVIEW_FORMAT=ERROR record absent (fail-closed)")
        return 2
    text = rp.read_text(encoding="utf-8", errors="replace")

    defects = []

    def field(name):
        for line in text.splitlines():
            if line.strip().startswith(name + ":"):
                value = line.split(":", 1)[1].strip()
                return value
        return None

    reviewer = field("reviewer")
    reviewed_at = field("reviewed-at")
    if not reviewer:
        defects.append("no nonempty `reviewer:` line")
    if not reviewed_at or not ISO.match(reviewed_at):
        defects.append("no `reviewed-at:` line carrying an ISO date")

    body = text
    verdicts = []
    for heading in ("## Verdicts",):
        idx = text.find(heading)
        if idx >= 0:
            body = text[idx:]
    for cells in rows_of([l for l in body.splitlines() if l.strip().startswith("|")]):
        verdicts.append(cells)
    if not verdicts:
        defects.append("no verdict table rows under `## Verdicts`")

    ok = 0
    for n, cells in enumerate(verdicts, 1):
        claim_id, entry_rel, sid = cells[0], cells[1], cells[2]
        verdict, reason = cells[3], cells[4] if len(cells) > 4 else ""
        row_defects = []
        if scope is not None and claim_id not in scope:
            row_defects.append("claim id not in scope")
        if verdict not in VERDICTS:
            row_defects.append(f"verdict word `{verdict}` not in supported/contradicted/unsupported")
        if len(reason.split()) < 8:
            row_defects.append("reason shorter than 8 words")
        if not SID.match(sid):
            row_defects.append(f"S-row id `{sid}` not shaped S###")
        elif f"| {sid} |" not in reg_text:
            row_defects.append(f"S-row id `{sid}` not in corpus/SOURCES.md")
        entry = root / entry_rel
        if not entry.is_file():
            row_defects.append(f"entry path `{entry_rel}` does not exist under --root")
        if row_defects:
            for d in row_defects:
                defects.append(f"row {n} ({claim_id}): {d}")
        else:
            ok += 1

    total = len(verdicts)
    passed = not defects
    print(f"RECORD_FORMAT={ok}/{total} REVIEW_FORMAT={'PASS' if passed else 'FAIL'}")
    for d in defects:
        print(f"defect: {d}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
