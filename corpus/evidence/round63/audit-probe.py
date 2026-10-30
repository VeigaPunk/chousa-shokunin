#!/usr/bin/env python3
"""Audit probe — runs tools/claims-audit.py against small fixtures and prints one P-row per case.

The probe exercises every rule class of the round-63 attempt-2 claims audit: a fixture claims file,
a rule file and the target artifacts are built under TMPDIR (never /tmp directly, never the lane),
the checker runs as a subprocess, and each case records observed vs expected. Cases P01-P10:

  P01  json-count fires on a wrong count (64 named, spec holds 66)
  P02  json-count passes when the true count is named
  P03  verbatim-heading fires on a heading that does not occur
  P04  verbatim-heading passes when it occurs
  P05  file-kind fires when a man page is claimed to be a header
  P06  section-contains fires when the needle is absent under the heading
  P07  git-first-commit fires when targets share the claims file's first-add commit
  P08  scope-narrower fires on a lane-wide claim swept only in a subdirectory
  P09  an anchor missing from the claims file is AUDIT_STALE and exits 2
  P10  a clean file with truthful rows passes with FLAGGED=0/n and exit 0

Usage: python3 corpus/evidence/round63/audit-probe.py [--out PATH]  (--out re-prints stdout there).
"""
from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

CHECKER = pathlib.Path(__file__).resolve().parents[3] / "tools" / "claims-audit.py"


def run_checker(claims: pathlib.Path, audit: pathlib.Path, root: pathlib.Path):
    return subprocess.run([sys.executable, "-B", str(CHECKER), "--claims", str(claims),
                           "--audit", str(audit), "--root", str(root)],
                          capture_output=True, text=True)


def main() -> int:
    out = sys.stdout
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="audit-probe-", dir=os.environ.get("TMPDIR") or None))
    results = []
    try:
        d = tmp / "fx"
        d.mkdir()
        (d / "spec.json").write_text(json.dumps({"items": list(range(66))}), encoding="utf-8")
        (d / "SCORECARD.md").write_text("## Planned — round 9 (amended, 2026-01-01)\n", encoding="utf-8")
        (d / "runner.py").write_text('V = [("s143-wrong-file", "/usr/share/man/man1/git-log.1.gz")]\n', encoding="utf-8")
        (d / "SOURCES.md").write_text("## Registry\n| S138 | x |\n## Leads (unopened)\n- unnumbered lead\n", encoding="utf-8")

        def case(name, observed_ok, expected):
            results.append((name, observed_ok, expected))
            print(f"PROBE {name} observed={'ok' if observed_ok else 'no'} expected={expected} "
                  f"{'ok' if observed_ok == expected else 'MISMATCH'}")

        def audit_case(tag: str, claims_lines, rows, needle_rev=None):
            c = d / tag
            c.mkdir(exist_ok=True)
            (c / "claims.md").write_text("\n".join(claims_lines) + "\n", encoding="utf-8")
            (c / "audit.tsv").write_text(rows, encoding="utf-8")
            for f in ("spec.json", "SCORECARD.md", "runner.py", "SOURCES.md"):
                (c / f).write_text((d / f).read_text(encoding="utf-8"), encoding="utf-8")
            return run_checker(c / "claims.md", c / "audit.tsv", c)

        p = audit_case("p01", ["One v2 wave `w1`, 64 seats, done."],
                       "R\tjson-count\tOne v2 wave `w1`, 64 seats\tspec.json:items\t\tt\n")
        case("P01 json-count wrong count fires", p.returncode == 1 and "FLAG R json-count" in p.stdout, True)
        p = audit_case("p02", ["One v2 wave `w1`, 66 seats, done."],
                       "R\tjson-count\tOne v2 wave `w1`, 66 seats\tspec.json:items\t\tt\n")
        case("P02 json-count true count passes", p.returncode == 0 and "FLAGGED=0/1" in p.stdout, True)
        p = audit_case("p03", ["is amended by `Planned — round 9 (amended)` in the same commit."],
                       "R\tverbatim-heading\tis amended by\tSCORECARD.md\t\tt\n")
        case("P03 verbatim-heading miss fires", p.returncode == 1 and "FLAG R verbatim-heading" in p.stdout, True)
        p = audit_case("p04", ["is amended by `Planned — round 9 (amended, 2026-01-01)` in the same commit."],
                       "R\tverbatim-heading\tis amended by\tSCORECARD.md\t\tt\n")
        case("P04 verbatim-heading hit passes", p.returncode == 0 and "FLAGGED=0/1" in p.stdout, True)
        p = audit_case("p05", ["variants: wrong header file, wrong anchor) all FAIL"],
                       "R\tfile-kind\twrong header file\trunner.py::s143-wrong-file\theader\tt\n")
        case("P05 file-kind man-not-header fires", p.returncode == 1 and "FLAG R file-kind" in p.stdout, True)
        p = audit_case("p06", ["S138 is the lead recorded in `SOURCES.md` `## Leads`."],
                       "R\tsection-contains\tis the lead recorded in\tSOURCES.md\t## Leads|S138\tt\n")
        case("P06 needle absent under heading fires", p.returncode == 1 and "FLAG R section-contains" in p.stdout, True)
        p = audit_case("p08", ["the lane holds nothing on what a revision name names. Command:",
                               "`grep -rl 'rev' corpus/knowledge` prints nothing."],
                       "R\tscope-narrower\tthe lane holds nothing on what a revision\t\t\tt\n")
        case("P08 lane-wide quantifier fires", p.returncode == 1 and "FLAG R scope-narrower" in p.stdout, True)
        p = audit_case("p09", ["totally unrelated text."],
                       "R\tjson-count\tOne v2 wave `w1`, 64 seats\tspec.json:items\t\tt\n")
        case("P09 stale anchor exits 2", p.returncode == 2 and "AUDIT_STALE" in p.stdout, True)
        p = audit_case("p10", ["One v2 wave `w1`, 66 seats, done.",
                               "is amended by `Planned — round 9 (amended, 2026-01-01)` in the same commit.",
                               "variants: wrong man-page file, wrong anchor) all FAIL"],
                       "R1\tjson-count\tOne v2 wave `w1`, 66 seats\tspec.json:items\t\tt\n"
                       "R2\tverbatim-heading\tis amended by\tSCORECARD.md\t\tt\n"
                       "R3\tfile-kind\twrong man-page file\trunner.py::s143-wrong-file\tman\tt\n")
        case("P10 truthful rows pass clean", p.returncode == 0 and "FLAGGED=0/3 AUDIT=PASS" in p.stdout, True)

        # P07 needs a real scratch git repo.
        g = d / "repo"
        g.mkdir()
        for cmd in (["git", "init", "-q"], ["git", "-C", str(g), "config", "user.email", "p@p"],
                    ["git", "-C", str(g), "config", "user.name", "p"]):
            subprocess.run(cmd, cwd=str(g), capture_output=True)
        (g / "claims.md").write_text("**Controls (all committed before the freeze.\n", encoding="utf-8")
        (g / "ctl.txt").write_text("x\n", encoding="utf-8")
        (g / "S.md").write_text("## Registry\n| S138 | x |\n## Leads (unopened)\n- unnumbered lead\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(g), "add", "claims.md", "ctl.txt", "S.md"], capture_output=True)
        subprocess.run(["git", "-C", str(g), "commit", "-qm", "one"], capture_output=True)
        rev = subprocess.run(["git", "-C", str(g), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        (g / "audit.tsv").write_text(
            "R\tgit-first-commit\tcommitted before the freeze\tctl.txt\t\tt\n", encoding="utf-8")
        p = run_checker(g / "claims.md", g / "audit.tsv", g)
        case("P07 same-commit target fires", p.returncode == 1 and "FLAG R git-first-commit" in p.stdout, True)
        # P06 rerun against the pinned revision of the repo (needle absent under ## Leads there).
        (g / "audit.tsv").write_text(
            f"R\tsection-contains-at\tis the lead recorded in\tS.md\t## Leads|S138|{rev}\tt\n", encoding="utf-8")
        (g / "claims.md").write_text("S138 is the lead recorded in `S.md` `## Leads`.\n", encoding="utf-8")
        p = run_checker(g / "claims.md", g / "audit.tsv", g)
        case("P06b pinned blob lacks needle -> fires", p.returncode == 1 and "FLAG R section-contains-at" in p.stdout, True)

        n_ok = sum(1 for _, obs, exp in results if obs == exp)
        print(f"PROBE_FACTS={n_ok}/{len(results)}")
        rc = 0 if n_ok == len(results) else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return rc


if __name__ == "__main__":
    sys.exit(main())
