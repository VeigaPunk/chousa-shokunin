#!/usr/bin/env python3
"""gen-audit-mutants — the frozen generator of the twelve claims-audit mutants (claim R64-C2).

Each mutant is one textual patch (old, new, count) applied to a target's committed bytes; `old` must occur
exactly `count` times or the patch is a harness error (exit 2), never a kill. The twelve classes, frozen
before any mutant is scored:

  A01  stale-anchor exit 2 turned exit 0 (the run_audit return line's stale arm)
  A02  stale-anchor detection removed (the AUDIT_STALE print and stale counter dropped, silent skip)
  A03  per-rule FLAG lines moved to stderr (consumer breakage)
  A04  detections suppressed (fired += 0: FLAGGED=0/n and exit 0 everywhere)
  A05  verbatim-heading matching made case-insensitive
  A06  json-count matching digits inside words (the round-63 attempt-2 mistake-2 class)
  A07  git-first-commit run with --diff-filter=AM (a later modification moves the first-commit read)
  A08  section-contains-at treating an unreadable revision as a pass (the git-show guard dropped)
  A09  the summary count fabricated (FLAGGED=0/n printed without deriving it)
  A10  rule-row validation weakened (an unknown rule name accepted, check silently returns unknown)
  A11  the selftest's own failing-case exit turned 0 (the bad-fixture guard)
  A12  the scope-narrower quantifier narrowed to one literal (the "nothing in the lane" arm dies)

The patches anchor on source spans of the round-63 attempt-2 checker (`tools/claims-audit.py`,
`d48247f9c77ac1e7`) that `tools/claims-audit-v2.py` preserves verbatim; a refactor that moves a span is a
harness error, disclosed, not a pass.
"""
from __future__ import annotations

import pathlib
import sys

MUTANTS = [
    ("A01", "stale exit 2->0",
     "    return 2 if stale else (1 if fired else 0)",
     "    return 0 if stale else (1 if fired else 0)", 1),
    ("A02", "stale detection removed",
     """            print(f"AUDIT_STALE {r['id']} anchor not in claims file")
            stale += 1
            continue""",
     "            continue", 1),
    ("A03", "FLAG lines to stderr",
     """            print(f"FLAG {r['id']} {r['rule']} {why} [{r['note']}]")""",
     """            print(f"FLAG {r['id']} {r['rule']} {why} [{r['note']}]", file=sys.stderr)""", 1),
    ("A04", "detections suppressed",
     """        if bad:
            fired += 1""",
     """        if bad:
            fired += 0""", 1),
    ("A05", "verbatim case-insensitive",
     "        miss = [s for s in spans if s not in body]",
     "        miss = [s for s in spans if s.lower() not in body.lower()]", 1),
    ("A06", "json-count digits in words",
     'if not re.search(r"(?<![\\w.)])%d(?![\\w])" % true, line):',
     'if not re.search(r"%d" % true, line):', 1),
    ("A07", "diff-filter A->AM",
     '"log", "--diff-filter=A", "--format=%H", "--", p]',
     '"log", "--diff-filter=AM", "--format=%H", "--", p]', 1),
    ("A08", "unreadable revision passes",
     """        if q.returncode != 0:
            return True, f"revision {rev[:10]} unreadable: {q.stderr.strip()[:60]}\"""",
     """        if False:
            return True, f"revision {rev[:10]} unreadable: {q.stderr.strip()[:60]}\"""", 1),
    ("A09", "summary count fabricated",
     """print(f"FLAGGED={fired}/{len(rows)} AUDIT={'FAIL' if fired else 'PASS'}")""",
     """print(f"FLAGGED=0/{len(rows)} AUDIT={'FAIL' if fired else 'PASS'}")""", 1),
    ("A10", "rule validation weakened",
     "if len(cols) != 6 or cols[1] not in RULES:",
     "if len(cols) != 6 and cols[1] not in RULES:", 1),
    ("A11", "selftest bad-case exit 1->0",
     """                print(f"AUDIT_SELFTEST: FAIL {tag} rc={p.returncode}\\n{p.stdout}{p.stderr}")
                return 1""",
     """                print(f"AUDIT_SELFTEST: FAIL {tag} rc={p.returncode}\\n{p.stdout}{p.stderr}")
                return 0""", 1),
    ("A12", "quantifier narrowed",
     'if not re.search(r"the lane holds nothing|nothing in the lane", line):',
     'if not re.search(r"the lane holds nothing at all", line):', 1),
]


def apply_mutant(src: pathlib.Path, dst: pathlib.Path, mid: str) -> None:
    """Write the mutant mid of source file src to dst; harness-error (exit 2) on a bad anchor."""
    text = src.read_text(encoding="utf-8")
    for m_id, _name, old, new, count in MUTANTS:
        if m_id != mid:
            continue
        got = text.count(old)
        if got != count:
            print(f"c2-mutrun: mutant {mid} anchor occurs {got} times in {src.name} (want {count})",
                  file=sys.stderr)
            raise SystemExit(2)
        dst.write_text(text.replace(old, new), encoding="utf-8")
        return
    print(f"c2-mutrun: unknown mutant {mid}", file=sys.stderr)
    raise SystemExit(2)
