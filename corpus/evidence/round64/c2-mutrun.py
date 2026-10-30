#!/usr/bin/env python3
"""c2-mutrun — the frozen runner that scores the twelve claims-audit mutants against a target checker.

Predicate R64-C2 (the same sentence as corpus/evidence/round64/claims.md, C2): for each mutant of the
frozen generator `gen-audit-mutants.py`, a scratch copy of the target's committed bytes is patched (an
anchor that does not occur exactly once is a harness error, exit 2, never a kill) and scored against the
matrix frozen for the named target:

  --matrix v1  (the round-63 attempt-2 receipts, re-derived at run time)
    R1  <target> --selftest                    rc 0, stdout contains `AUDIT_SELFTEST=PASS (3 cases)`
    R2  <target> --claims corpus/evidence/round62/claims.md --audit corpus/evidence/round63/audit/audit-r62.tsv
        --root <lane>                          rc 1, stdout contains `FLAGGED=2/2 AUDIT=FAIL`
    R3  <target> --claims corpus/evidence/round63/claims.md --audit corpus/evidence/round63/audit/audit-r63.tsv
        --root <lane>                          rc 1, stdout contains `FLAGGED=4/4 AUDIT=FAIL`
    R4  <target> --claims corpus/evidence/round63/claims-a2.md --audit corpus/evidence/round63/audit/audit-a2.tsv
        --root <lane>                          rc 0, stdout contains `FLAGGED=0/4 AUDIT=PASS`
    R5  the frozen probe run against the mutant through a scratch mirror tree (the probe's CHECKER is
        derived from its own `__file__`, so the mirror places the mutant at `<mirror>/tools/claims-audit.py`
        and the probe at `<mirror>/corpus/evidence/round63/audit-probe.py`)
                                               rc 0, stdout contains `PROBE_FACTS=11/11`
  --matrix v2  (the claims-audit-v2 contract: the same five legs with R1 expecting
    `AUDIT_SELFTEST=PASS (10 cases)`, R2 additionally requiring a stdout line starting `FLAG `, plus)
    R6  <target> --selftest --selftest-fault 1   rc 1, stdout contains `FAULT`
    R7  git-first-commit over a scratch repo whose target is modified after the add commit (commit 1 adds
        claims.md + target, commit 2 modifies the target): the rule must still fire (rc 1, `FLAG` on
        stdout) — the first-add read must not move to a later modification (mutant class A07)

A mutant is KILLED when at least one leg's exit code or required output differs from its frozen
expectation (the matrix detects the mutation); it SURVIVES when every leg holds its expectation (the
matrix cannot distinguish it from the correct checker). A leg that itself errors is a harness error
(exit 2). Prints one `MUT <id> <killed|SURVIVED> <failing legs>` line per mutant — SURVIVED lines name
no failing leg, killed lines name every leg that fired — and one summary `AUDIT_MUTANTS_KILLED=<k>/12`,
exit 0 iff k == 12.

Usage: python3 c2-mutrun.py --target PATH --matrix v1|v2 --work DIR [--lane DIR]
(the work directory must be absent or empty; it is removed at the end; scratch under $HYAKU_SCRATCH/chousa-r64/)
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[2]
if not (LANE / "corpus" / "SOURCES.md").is_file():
    print(f"c2-mutrun: MISSING_LANE_FILE: {LANE / 'corpus' / 'SOURCES.md'}", file=sys.stderr)
    raise SystemExit(2)
PROBE = LANE / "corpus/evidence/round63/audit-probe.py"
LEG_TIMEOUT = 300


def run(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=LEG_TIMEOUT, cwd=cwd,
                          stdin=subprocess.DEVNULL)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--target", required=True)
    ap.add_argument("--matrix", choices=("v1", "v2"), required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--lane", default=str(LANE))
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    target = pathlib.Path(a.target)
    if not target.is_file():
        print(f"c2-mutrun: target {target} absent", file=sys.stderr)
        return 2
    work = pathlib.Path(a.work)
    if work.exists() and any(work.iterdir()):
        print("c2-mutrun: --work must be absent or empty", file=sys.stderr)
        return 2
    if os.geteuid() == 0:
        print("c2-mutrun: refusing to run as root", file=sys.stderr)
        return 2
    spec = importlib.util.spec_from_file_location("gen_audit_mutants", HERE / "gen-audit-mutants.py")
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    work.mkdir(parents=True)
    src_bytes = target.read_bytes()
    tgt_text = src_bytes.decode("utf-8")
    receipts = (
        ("R2", ["--claims", str(lane / "corpus/evidence/round62/claims.md"),
                "--audit", str(lane / "corpus/evidence/round63/audit/audit-r62.tsv"), "--root", str(lane)],
         1, "FLAGGED=2/2 AUDIT=FAIL"),
        ("R3", ["--claims", str(lane / "corpus/evidence/round63/claims.md"),
                "--audit", str(lane / "corpus/evidence/round63/audit/audit-r63.tsv"), "--root", str(lane)],
         1, "FLAGGED=4/4 AUDIT=FAIL"),
        ("R4", ["--claims", str(lane / "corpus/evidence/round63/claims-a2.md"),
                "--audit", str(lane / "corpus/evidence/round63/audit/audit-a2.tsv"), "--root", str(lane)],
         0, "FLAGGED=0/4 AUDIT=PASS"),
    )
    summary_v1 = "AUDIT_SELFTEST=PASS (3 cases)"
    summary_v2 = "AUDIT_SELFTEST=PASS (10 cases)"
    results = []

    def probe_leg(mutant: pathlib.Path) -> tuple[bool, str]:
        mirror = work / ("m-%s" % mid)
        (mirror / "corpus/evidence/round63").mkdir(parents=True)
        (mirror / "tools").mkdir()
        shutil.copy2(PROBE, mirror / "corpus/evidence/round63/audit-probe.py")
        shutil.copy2(mutant, mirror / "tools/claims-audit.py")
        p = run([sys.executable, "-B", str(mirror / "corpus/evidence/round63/audit-probe.py")])
        shutil.rmtree(mirror, ignore_errors=True)
        ok = p.returncode == 0 and "PROBE_FACTS=11/11" in p.stdout
        return ok, f"R5 rc={p.returncode}"

    def scratch_repo_leg(mutant: pathlib.Path) -> tuple[bool, str]:
        import os
        d = pathlib.Path(tempfile.mkdtemp(prefix="c2mutrepo-", dir=work))
        for cmd in (["git", "init", "-q"], ["git", "-C", str(d), "config", "user.email", "f@f"],
                    ["git", "-C", str(d), "config", "user.name", "f"]):
            run(cmd, cwd=str(d))
        (d / "claims.md").write_text("committed before the freeze says the report.\n", encoding="utf-8")
        (d / "target.txt").write_text("v1\n", encoding="utf-8")
        run(["git", "-C", str(d), "add", "claims.md", "target.txt"], cwd=str(d))
        run(["git", "-C", str(d), "commit", "-qm", "one"], cwd=str(d))
        (d / "target.txt").write_text("v2\n", encoding="utf-8")
        run(["git", "-C", str(d), "add", "target.txt"], cwd=str(d))
        run(["git", "-C", str(d), "commit", "-qm", "two"], cwd=str(d))
        (d / "audit.tsv").write_text(
            "R7\tgit-first-commit\tcommitted before the freeze\ttarget.txt\t\tmodified after add\n", encoding="utf-8")
        p = run([sys.executable, "-B", str(mutant), "--claims", str(d / "claims.md"),
                 "--audit", str(d / "audit.tsv"), "--root", str(d)])
        shutil.rmtree(d, ignore_errors=True)
        ok = p.returncode == 1 and "FLAG R7" in p.stdout
        return ok, f"R7 rc={p.returncode}"

    try:
        for mid, _name, old, new, count in gen.MUTANTS:
            got = tgt_text.count(old)
            if got != count:
                print(f"c2-mutrun: mutant {mid} anchor occurs {got} times in {target.name} (want {count})",
                      file=sys.stderr)
                return 2
            mroot = work / ("w-%s" % mid)
            mroot.mkdir()
            mutant = mroot / ("mut-%s.py" % mid)
            mutant.write_text(tgt_text.replace(old, new), encoding="utf-8")
            legs = []
            try:
                p = run([sys.executable, "-B", str(mutant), "--selftest"])
                want = summary_v1 if a.matrix == "v1" else summary_v2
                legs.append(("R1", p.returncode == 0 and want in p.stdout, f"R1 rc={p.returncode}"))
                for lid, args, rc, needle in receipts:
                    p = run([sys.executable, "-B", str(mutant)] + args)
                    ok = p.returncode == rc and needle in p.stdout
                    if a.matrix == "v2" and lid == "R2":
                        ok = ok and any(l.startswith("FLAG ") for l in p.stdout.splitlines())
                    legs.append((lid, ok, f"{lid} rc={p.returncode}"))
                ok, why = probe_leg(mutant)
                legs.append((why.split()[0], ok, why))
                if a.matrix == "v2":
                    p = run([sys.executable, "-B", str(mutant), "--selftest", "--selftest-fault", "1"])
                    legs.append(("R6", p.returncode == 1 and "FAULT" in p.stdout, f"R6 rc={p.returncode}"))
                    ok, why = scratch_repo_leg(mutant)
                    legs.append((why.split()[0], ok, why))
            except subprocess.TimeoutExpired:
                legs.append(("TIMEOUT", False, "leg timeout"))
            fired = [(lid, why) for lid, ok, why in legs if not ok]
            killed = bool(fired)
            results.append((mid, killed, "; ".join(why for _lid, why in fired) if fired else "all legs hold"))
            shutil.rmtree(mroot, ignore_errors=True)
        for mid, killed, why in results:
            print(f"MUT {mid} {'killed' if killed else 'SURVIVED'} {why}")
        k = sum(1 for _m, killed, _w in results if killed)
        print(f"AUDIT_MUTANTS_KILLED={k}/12")
        return 0 if (k == 12 and len(results) == 12) else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    import os
    sys.exit(main())
