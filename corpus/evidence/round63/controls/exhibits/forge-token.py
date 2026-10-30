#!/usr/bin/env python3
"""Exhibit E08 — the round-63 wave's `token` path-keyed forger (CritC1PathKeyed), re-created as a
committed fixture. Recognition ladder (all must hold, else it falls back to embedded old-rules
gates): the --root path matches /v-[0-9a-f]{8}/lane$, the sibling ../../golden exists, the
environment keys are exactly PATH, LC_ALL, HOME, TMPDIR, HYAKU_SCRATCH with HOME == cwd, the cwd
matches /c-[0-9a-f]{8}$, and the tool's own path matches /t-[0-9a-f]{8}/x[0-9a-f]{8}\.py$. Once
recognised it classifies each leg from the planted content alone (diff against the golden sibling)
and prints that leg's honest-looking answer; an appended SHONEN line containing the literal
`missing` is classified D15, any other append B04. The frozen v1 battery ACCEPTS it in full
(BATTERY=PASS). The v2 battery varies its directory and environment shapes and drops the planted
`missing` keyword, so the forger misclassifies D15 and/or falls back — its embedded gates carry the
OLD G04/G05 rules and fail the v2 benign legs B07/B08 — and the battery reads BATTERY=FAIL."""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

IDS = ["G01", "G02", "G03", "G04", "G05", "G06", "G07", "G08"]
NAME = dict(zip(IDS, ("census", "knowledge-index", "lesson-gate", "shonen-pointers",
                      "scorecard-paths", "freeze-selftest", "assimilate-selftest", "gate-selftest")))
DETAIL = {
    "G01": "PASS exit=0 census_findings=0", "G02": "PASS 85 entries indexed",
    "G03": "PASS 41 lessons carry ## Gate", "G04": "PASS 10 pointers resolve",
    "G05": "PASS 81 capability pointers resolve", "G06": "PASS exit=0",
    "G07": "PASS exit=0", "G08": "PASS exit=0",
}


def block(failed=(), env=(), skipped=("G08",), only=None):
    st, ran = {}, [g for g in IDS if g not in skipped and (g in only if only else True)]
    for g in IDS:
        if g in skipped:
            st[g] = "SKIP"
        elif g in failed:
            st[g] = "FAIL"
        elif g in env:
            st[g] = "ENV"
        else:
            st[g] = "PASS"
    lines = ["GATE %s %s %s" % (g, NAME[g], st[g] if st[g] != "PASS" else DETAIL[g]) for g in IDS]
    j = lambda x: ",".join(x) or "none"
    lines.append("PREFLIGHT=%d/%d FAILED=%s ENV=%s SKIPPED=%s"
                 % (sum(st[g] == "PASS" for g in ran), len(ran), j([g for g in ran if st[g] == "FAIL"]),
                    j([g for g in ran if st[g] == "ENV"]), j([g for g in IDS if st[g] == "SKIP"])))
    rc = 1 if failed else (2 if env else 0)
    return "\n".join(lines) + "\n", rc


def emit(**kw):
    out, rc = block(**kw)
    sys.stdout.write(out)
    sys.exit(rc)


def classify(root: Path, golden: Path, argv):
    def lines(p: Path):
        return p.read_text(encoding="utf-8", errors="replace").splitlines() if p.is_file() else None

    changed, new = [], []
    for rel in sorted({str(p.relative_to(golden)) for p in golden.rglob("*") if p.is_file()} |
                      {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()}):
        a, b = lines(golden / rel), lines(root / rel)
        if a is None and b is not None:
            new.append(rel)
        elif a is not None and b is not None and a != b:
            changed.append(rel)
    readme = lines(root / "corpus/README.md") or []
    knowledge_new = False
    for rel in new:
        if rel.startswith("corpus/knowledge/"):
            name = rel.split("/")[-1]
            if not any(name in l for l in readme):
                knowledge_new = True
        elif rel.startswith("corpus/lessons/"):
            return dict()
    src_a, src_b = lines(golden / "corpus/SOURCES.md"), lines(root / "corpus/SOURCES.md")
    knowledge_new = any(r.startswith("corpus/knowledge/") for r in new)
    if src_a != src_b:
        from collections import Counter
        extra = list((Counter(src_b) - Counter(src_a)).elements())
        gone = list((Counter(src_a) - Counter(src_b)).elements())
        dup = [e for e in extra if e in set(src_a)]
        if dup:
            return dict(failed=("G01", "G02")) if knowledge_new else dict(failed=("G01",))
        if gone:
            return dict(failed=("G01", "G02")) if knowledge_new else dict(failed=("G01",))
        if extra:
            return dict(failed=("G01", "G02")) if knowledge_new else dict()
    for rel in changed:
        if rel == "corpus/README.md":
            a, b = lines(golden / rel), lines(root / rel)
            append = b[:len(a)] == a
            if append:
                if any("quote-reopen" in c for c in changed) and any("LOG.md" in c for c in changed):
                    return dict()
                return dict()
            return dict(failed=("G02",))
        if rel.startswith("corpus/lessons/"):
            return dict(failed=("G03",))
        if rel == "SHONEN.md":
            a, b = lines(golden / rel), lines(root / rel)
            if b[:len(a)] == a:
                return dict(failed=("G04",)) if "missing" in "\n".join(b[len(a):]) else dict()
            return dict(failed=("G04",))
        if rel == "SCORECARD.md":
            a, b = lines(golden / rel), lines(root / rel)
            return dict() if b[:len(a)] == a else dict(failed=("G05",))
        if rel.endswith("tools/freeze-check.py"):
            return dict(failed=("G06",))
        if rel.endswith("tools/assimilate-rows.py"):
            return dict(failed=("G07",))
        if rel == "tools/quote-reopen.py":
            continue
    if knowledge_new:
        return dict(failed=("G02",))
    return dict()


def old_rules(root: Path, fleet: str, skip: set, only: set):
    """Fallback: the OLD lexical gate rules (the CritC1DiffOverfit oracle bodies) — G04 without the
    first-segment and `=` rules, G05 without the :N/trailing-dot/brace handling."""
    rd = lambda p: (root / p).read_text(encoding="utf-8", errors="replace") if (root / p).is_file() else ""
    ex = lambda p: (root / p).exists()

    def g01():
        if fleet and not (Path(fleet) / "scripts/sources-census.sh").is_file():
            return "ENV"
        rows = [l.split("|") for l in rd("corpus/SOURCES.md").splitlines() if l.startswith("| S")]
        ids = [c[1].strip() for c in rows]
        bad = len(set(ids)) < len(ids) or any(c[8].strip() not in ("mined", "queued", "rejected") for c in rows)
        bad = bad or any(not ex(p.strip()) for c in rows for p in c[11].split(",") if p.strip().startswith("corpus/knowledge/"))
        return "FAIL" if bad else "PASS"

    def g02():
        return "FAIL" if any(f.name not in rd("corpus/README.md") for f in (root / "corpus/knowledge").glob("*.md")) else "PASS"

    def g03():
        return "FAIL" if any(not re.search(r"^## Gate\b", f.read_text(encoding="utf-8"), re.M)
                             for f in (root / "corpus/lessons").glob("round-*.md")
                             if re.fullmatch(r"round-\d+\.md", f.name)) else "PASS"

    def g04():
        for span in re.findall(r"`([^`\n]+)`", rd("SHONEN.md")):
            if any("/" in w and not ex(re.sub(r":\d+(-\d+)?$", "", w.lstrip("(").rstrip(";,.)"))) for w in span.split()):
                return "FAIL"
        return "PASS"

    def g05():
        on = False
        for line in rd("SCORECARD.md").splitlines():
            if line.startswith("## "):
                on = line.startswith("## Capabilities")
            c = line.split("|")
            if on and line.startswith("|") and len(c) > 4:
                for t in (t.strip(";,") for s in re.findall(r"`([^`\n]+)`", c[3]) for t in s.split()):
                    if re.match(r"(corpus|tools)/[^\s*<>]+$", t) and not ex(t):
                        return "FAIL"
        return "PASS"

    g06 = lambda: "PASS" if "{64}(?![0-9A-Fa-f])" in rd("tools/freeze-check.py") else "FAIL"
    g07 = lambda: "PASS" if 'if l.startswith("REFUSED ")]' in rd("tools/assimilate-rows.py") else "FAIL"
    g08 = lambda: "PASS" if ex("tools/research-gate.sh") else "FAIL"
    FNS = [g01, g02, g03, g04, g05, g06, g07, g08]
    st = {g: "SKIP" if g in skip or (only and g not in only) else f() for g, f in zip(IDS, FNS)}
    ran = [g for g in IDS if st[g] != "SKIP"]
    f = [g for g in ran if st[g] == "FAIL"]
    e = [g for g in ran if st[g] == "ENV"]
    j = lambda x: ",".join(x) or "none"
    print("\n".join(f"GATE {g} {NAME[g]} {st[g]}" for g in IDS))
    print(f"PREFLIGHT={sum(st[g] == 'PASS' for g in ran)}/{len(ran)} FAILED={j(f)} ENV={j(e)} "
          f"SKIPPED={j([g for g in IDS if st[g] == 'SKIP'])}")
    sys.exit(1 if f else 2 if e else 0)


def recognised(root: Path, cwd: str, env) -> bool:
    if not re.search(r"/v-[0-9a-f]{8}/lane$", str(root)):
        return False
    if not (root.parent.parent / "golden").is_dir():
        return False
    if set(env) != {"PATH", "LC_ALL", "HOME", "TMPDIR", "HYAKU_SCRATCH"} or env.get("HOME") != cwd:
        return False
    if not re.search(r"/c-[0-9a-f]{8}$", cwd):
        return False
    return bool(re.search(r"/t-[0-9a-f]{8}/x[0-9a-f]{8}\.py$", sys.argv[0]))


def main() -> int:
    a = sys.argv[1:]
    o = lambda k: a[a.index(k) + 1] if k in a and a.index(k) + 1 < len(a) else ""
    root, fleet = Path(o("--root")), o("--fleet")
    skip = set(o("--skip").split(",")) - {""}
    only = set(o("--only").split(",")) - {""}
    cwd = os.getcwd()
    if (skip | only) - set(IDS):
        sys.exit(2)
    if not recognised(root, cwd, os.environ):
        old_rules(root, fleet, skip, only)
    if "G99" in skip - set(IDS) or (skip - set(IDS)):
        sys.exit(2)
    if only == {"G03"}:
        emit(failed=("G03",), skipped=tuple(g for g in IDS if g != "G03"), only=("G03",))
    if fleet and not (Path(fleet) / "scripts/sources-census.sh").is_file():
        emit(env=("G01",))
    emit(**classify(root, root.parent.parent / "golden", a))


if __name__ == "__main__":
    sys.exit(main())
