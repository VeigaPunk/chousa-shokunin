#!/usr/bin/env python3
"""claims-audit-v2 — flags self-assessment statements in a frozen claims file that committed files contradict.

v2 (round 64, claim R64-C2): the round-63 attempt-2 checker (`tools/claims-audit.py`, frozen bytes
`d48247f9c77ac1e7`) with three additions and every rule class below byte-identical:
  1. `load_rules` rejects duplicate rule ids (`duplicate rule id`, exit 1) — mutant class A10.
  2. `--selftest` runs ten cases (the three attempt-2 fixtures plus C4 a stale anchor exiting 2, C5 a
     case-only verbatim-heading mismatch firing, C6 an unreadable revision firing, C7 a duplicate rule id
     rejected, C8 the `nothing in the lane` quantifier arm firing, C9 a digit inside a word not counting
     as a named count, C10 the FLAG lines required on stdout) and prints one `CASE <n> <tag> ok` line per
     case before `AUDIT_SELFTEST=PASS (10 cases)`.
  3. `--selftest-fault N` forces case N's verdict check to fail — the selftest shown able to fail; it
     prints `AUDIT_SELFTEST: FAULT case <N> forced` and exits 1.
The mutant battery over this checker and the v1 checker is `corpus/evidence/round64/c2-mutrun.py` with the
frozen generator `corpus/evidence/round64/gen-audit-mutants.py`.

The lane's frozen claims files have twice carried statements their own files contradict (round 62:
14 statements, `corpus/evidence/round62/claims-erratum.md`; round 63 attempt 1: 4 statements,
`corpus/evidence/round63/claims-erratum.md`), each caught by a non-author reader after the freeze.
This checker mechanises the detectable subset: a rule file (TSV, one row per checkable statement)
names an anchor that locates the statement in the claims file and a generic check class; the
checker re-derives the fact from the committed bytes and flags the row when the statement is false.

Usage:
    python3 tools/claims-audit.py --claims FILE --audit FILE [--root DIR]
    python3 tools/claims-audit.py --selftest

Output: one `FLAG <id> <rule> <detail>` line per rule that fires, one `AUDIT_STALE <id>` line (and
exit 2) when an anchor does not occur in the claims file (the rule file does not match the claims
file), then one summary line `FLAGGED=<k>/<n> AUDIT=PASS|FAIL` — PASS with exit 0 when no rule
fired, FAIL with exit 1 when at least one did. Exit 2 is also usage/IO error.

Rule-file columns (tab-separated): id, rule, anchor, target, expect, note.

Rule classes (each grounded in a demonstrated erratum instance):
  json-count          the anchor line must contain, as a standalone number token, the true count of
                      the JSON array at target `<file>:<key>` (erratum r62 #1: "64 seats" vs 66
                      spec items). A number inside a word (`v2`, `w1`) does not count as named.
  section-contains    the needle `expect` ("<heading-prefix>|<needle>") must occur under that
                      heading of target file; the anchor asserts it does (r62 #13: S138 claimed to
                      be recorded under `## Leads`).
  section-contains-at the same check against the file's blob at a pinned revision, expect
                      "<heading>|<needle>|<revision>" (r62 #13 against the round-62 base, whose
                      `## Leads` bullet does not name S138; the current file does). Read-only
                      `git show <rev>:<path>`.
  git-first-commit    every repo-relative path in target (comma-separated) must first appear in a
                      commit earlier than the claims file's own first-add commit; the anchor asserts
                      they were committed before the freeze (r63 E1: they were added in the same
                      commit). Read-only `git log --diff-filter=A` against --root.
  file-kind           the line of target `<file>::<needle>` that contains needle must name a file
                      of the kind given in expect (e.g. `header`); kinds are classified by suffix
                      (`.h`/`.hpp` header, `.[0-9]`/`.[0-9].gz` man page, `.md` doc, `.py` code,
                      `.json/.tsv/.txt` data) (r63 E2: "wrong header file" where the variant
                      substitutes a man page).
  verbatim-heading    every backtick span in the anchor line must occur verbatim in the target file
                      (r63 E3: a quoted SCORECARD heading that does not occur).
  scope-narrower      a lane-wide absence quantifier ("the lane holds nothing") whose own sweep
                      command (`grep -rl ... PATH`, searched on the anchor line and the two lines
                      after it) names a strict subdirectory (r63 E4).

Named limits: the classes are lexical; a statement is only checked when a rule row anchors it, and
the rule rows are authored by the same lane that wrote the claims file (overfit risk — a reader
still outranks the checker); line-local checks (json-count, verbatim-heading) read the anchor line
only; git-first-commit needs a git checkout and is skipped (counted, flagged as SKIP) when --root
is not a work tree.

Self-test: builds isolated fixtures under TMPDIR (never the lane, never /tmp directly), runs ten cases
(v2 additions named at the top of this docstring), prints one `CASE <n> <tag> ok` line per case and
`AUDIT_SELFTEST=PASS (10 cases)`; exit 1 on any unexpected verdict, and under `--selftest-fault N` it
forces case N's verdict check to fail and exits 1 with `AUDIT_SELFTEST: FAULT case <N> forced`.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

RULES = ("json-count", "section-contains", "section-contains-at", "git-first-commit", "file-kind",
         "verbatim-heading", "scope-narrower")
KIND_SUFFIX = ((".h", "header"), (".hpp", "header"),
               (".gz", "man"), (".1", "man"), (".2", "man"), (".3", "man"), (".7", "man"),
               (".md", "doc"), (".py", "code"), (".json", "data"), (".tsv", "data"), (".txt", "data"))
NUM_RE = re.compile(r"\d+")


def kind_of(path: str) -> str:
    low = path.lower()
    for suf, kind in KIND_SUFFIX:
        if low.endswith(suf):
            return "man" if suf == ".gz" and re.search(r"\.[0-9]\.gz$", low) else kind
    return "other"


def load_rules(path: pathlib.Path):
    rows = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
        if not line.strip() or line.startswith("#"):
            continue
        cols = line.split("\t")
        if len(cols) != 6 or cols[1] not in RULES:
            raise SystemExit(f"claims-audit: bad rule row {path.name}:{i + 1}")
        rows.append(dict(id=cols[0].strip(), rule=cols[1], anchor=cols[2], target=cols[3],
                         expect=cols[4], note=cols[5]))
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("claims-audit-v2: duplicate rule id")
    return rows


def check(rule, text: str, root: pathlib.Path, claims_rel: str):
    """Return (fired, detail). anchor must occur in text (caller guarantees)."""
    lines = text.splitlines()
    li = next(i for i, l in enumerate(lines) if rule["anchor"] in l)
    line = lines[li]
    ctx = "\n".join(lines[li:li + 3])
    if rule["rule"] == "json-count":
        f, key = rule["target"].rsplit(":", 1)
        data = json.loads((root / f).read_text(encoding="utf-8"))
        true = len(data[key]) if isinstance(data, dict) else len(data)
        if not re.search(r"(?<![\w.)])%d(?![\w])" % true, line):
            return True, f"line numbers {NUM_RE.findall(line)[:6]}; {f}:{key} holds {true}"
        return False, f"{f}:{key} = {true} named"
    if rule["rule"] == "section-contains":
        heading, needle = rule["expect"].split("|", 1)
        cur, sect = None, []
        for l in (root / rule["target"]).read_text(encoding="utf-8").splitlines():
            if l.startswith("## "):
                cur = l
            elif cur and cur.startswith(heading):
                sect.append(l)
        if needle not in "\n".join(sect):
            return True, f"{needle} not under `{heading}` of {rule['target']}"
        return False, f"{needle} found under `{heading}`"
    if rule["rule"] == "section-contains-at":
        heading, needle, rev = rule["expect"].split("|", 2)
        q = subprocess.run(["git", "-C", str(root), "show", f"{rev}:{rule['target']}"],
                           capture_output=True, text=True)
        if q.returncode != 0:
            return True, f"revision {rev[:10]} unreadable: {q.stderr.strip()[:60]}"
        cur, sect = None, []
        for l in q.stdout.splitlines():
            if l.startswith("## "):
                cur = l
            elif cur and cur.startswith(heading):
                sect.append(l)
        if needle not in "\n".join(sect):
            return True, f"{needle} not under `{heading}` of {rule['target']} at {rev[:10]}"
        return False, f"{needle} found at {rev[:10]}"
    if rule["rule"] == "git-first-commit":
        if not (root / ".git").exists():
            return False, "SKIP no git root"
        first = {}
        for p in [claims_rel] + [t for t in rule["target"].split(",") if t]:
            q = subprocess.run(["git", "-C", str(root), "log", "--diff-filter=A", "--format=%H", "--", p],
                               capture_output=True, text=True)
            c = q.stdout.strip().splitlines()
            first[p] = c[-1] if c else None
        base = first.get(claims_rel)
        same = [p for p, c in first.items() if p != claims_rel and c and base and c == base]
        if same:
            return True, f"first added with the claims file in {base[:10]}: {','.join(same)}"
        return False, "targets first appear in earlier commits" if base else "SKIP claims file uncommitted"
    if rule["rule"] == "file-kind":
        fname, needle = rule["target"].split("::", 1)
        hit = next((l for l in (root / fname).read_text(encoding="utf-8").splitlines() if needle in l), "")
        paths = re.findall(r"[^\s'\"`,()]+\.(?:h|hpp|[0-9]\.gz|[0-9]|md|py|json|tsv|txt)", hit)
        kinds = {kind_of(p) for p in paths}
        if rule["expect"] not in kinds:
            return True, f"`{rule['expect']}` claimed; {needle} substitutes {sorted(p.rsplit('/', 1)[-1] for p in paths)} ({sorted(kinds)})"
        return False, f"{needle} is a {rule['expect']}"
    if rule["rule"] == "verbatim-heading":
        spans = re.findall(r"`([^`\n]+)`", line)
        body = (root / rule["target"]).read_text(encoding="utf-8")
        miss = [s for s in spans if s not in body]
        if miss:
            return True, f"not found in {rule['target']}: {miss[0][:60]!r}"
        return False, f"{len(spans)} span(s) found"
    if rule["rule"] == "scope-narrower":
        if not re.search(r"the lane holds nothing|nothing in the lane", line):
            return False, "no lane-wide quantifier"
        m = re.search(r"grep -rl\s+\S+\s+(\S+)", ctx)
        path = m.group(1).strip("`") if m else ""
        if path and path not in (".", "./") and "/" in path:
            return True, f"lane-wide claim swept only `{path}`"
        return False, "sweep covers the lane" if path else "no sweep named"
    return False, "unknown rule"


def run_audit(claims: pathlib.Path, audit: pathlib.Path, root: pathlib.Path) -> int:
    text = claims.read_text(encoding="utf-8")
    rows = load_rules(audit)
    fired = 0
    stale = 0
    for r in rows:
        if r["anchor"] not in text:
            print(f"AUDIT_STALE {r['id']} anchor not in claims file")
            stale += 1
            continue
        bad, why = check(r, text, root, claims.relative_to(root).as_posix() if claims.is_relative_to(root) else str(claims))
        if bad:
            fired += 1
            print(f"FLAG {r['id']} {r['rule']} {why} [{r['note']}]")
    print(f"FLAGGED={fired}/{len(rows)} AUDIT={'FAIL' if fired else 'PASS'}")
    return 2 if stale else (1 if fired else 0)


def selftest(fault: int = 0) -> int:
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="claims-audit-selftest-", dir=os.environ.get("TMPDIR") or None))
    cases = 0

    def _run(d):
        return subprocess.run([sys.executable, "-B", str(pathlib.Path(__file__).resolve()),
                               "--claims", str(d / "claims.md"), "--audit", str(d / "audit.tsv"),
                               "--root", str(d)], capture_output=True, text=True)

    def _expect(n, tag, ok, p):
        nonlocal cases
        cases = n
        if fault == cases:
            print(f"AUDIT_SELFTEST: FAULT case {cases} forced")
            return False
        print(f"CASE {cases} {tag} {'ok' if ok else 'FAIL'}")
        if not ok:
            print(f"AUDIT_SELFTEST: FAIL {tag} rc={p.returncode}\n{p.stdout}{p.stderr}")
        return ok

    try:
        (tmp / "spec.json").write_text(json.dumps({"items": list(range(66))}), encoding="utf-8")
        (tmp / "SOURCES.md").write_text("# S\n## Registry\n| S138 | x |\n## Paths\nx\n## Leads (unopened)\n- openat2(2) wrapper\n", encoding="utf-8")
        (tmp / "SCORECARD.md").write_text("## Planned — round 9 (amended, 2026-01-01)\nbody\n", encoding="utf-8")
        (tmp / "runner.py").write_text('V = [("s143-wrong-file", "/usr/share/man/man1/git-log.1.gz")]\n', encoding="utf-8")
        bad_claims = "\n".join([
            "One v2 wave `w1`, 64 seats, done.",
            "(2026-10-28; S138 is the lead recorded in `corpus/SOURCES.md` `## Leads` by round 61).",
            "**Controls (all committed before the freeze; see repo.",
            "variants: missing README map, wrong header file, wrong anchor) all FAIL, 21 FAIL variants",
            "is amended by `Planned — round 9 (amended)` in the same commit.",
            "covers the sha256 pin; the lane holds nothing on what a revision name names. Command:",
            "`grep -rl 'rev' corpus/knowledge` prints nothing.",
        ])
        good_claims = "\n".join([
            "One v2 wave `w1`, 66 seats, done.",
            "(2026-10-28; the openat2(2) bullet is the lead recorded in `corpus/SOURCES.md` `## Leads`; S138 is its row).",
            "**Controls (committed in the freeze commit; see repo.",
            "variants: missing README map, wrong man-page file, wrong anchor) all FAIL, 21 FAIL variants",
            "is amended by `Planned — round 9 (amended, 2026-01-01)` in the same commit.",
            "covers the sha256 pin; the knowledge layer holds nothing on what a revision name names. Command:",
            "`grep -rl 'rev' corpus/knowledge` prints nothing.",
        ])
        rules_bad = "\n".join([
            "R1\tjson-count\tOne v2 wave `w1`, 64 seats\tspec.json:items\t\tselftest r62 #1",
            "R2\tsection-contains\tis the lead recorded in\tSOURCES.md\t## Leads|S138\tselftest r62 #13",
            "R3\tverbatim-heading\tis amended by\tSCORECARD.md\t\tselftest r63 E3",
            "R4\tfile-kind\twrong header file\trunner.py::s143-wrong-file\theader\tselftest r63 E2",
            "R5\tscope-narrower\tthe lane holds nothing on what a revision\t\t\tselftest r63 E4",
            "R6\tsection-contains\tis the lead recorded in\tSOURCES.md\t## Registry|S138\tcontrol: needle present",
        ])
        rules_good = "\n".join([
            "R1\tjson-count\tOne v2 wave `w1`, 66 seats\tspec.json:items\t\tselftest r62 #1",
            "R2\tsection-contains\tis the lead recorded in\tSOURCES.md\t## Leads|openat2(2)\tselftest r62 #13",
            "R3\tverbatim-heading\tis amended by\tSCORECARD.md\t\tselftest r63 E3",
            "R4\tfile-kind\twrong man-page file\trunner.py::s143-wrong-file\tman\tselftest r63 E2",
            "R5\tscope-narrower\tthe knowledge layer holds nothing on what a revision\t\t\tselftest r63 E4",
            "R6\tsection-contains\tis the lead recorded in\tSOURCES.md\t## Registry|S138\tcontrol: needle present",
        ])
        for ci, (tag, claims_text, rules_text, expect_fail) in enumerate(
                (("bad", bad_claims, rules_bad, True), ("good", good_claims, rules_good, False)), 1):
            d = tmp / tag
            d.mkdir()
            (d / "claims.md").write_text(claims_text, encoding="utf-8")
            (d / "audit.tsv").write_text(rules_text, encoding="utf-8")
            for f in ("spec.json", "SOURCES.md", "SCORECARD.md", "runner.py"):
                (d / f).write_text((tmp / f).read_text(encoding="utf-8"), encoding="utf-8")
            p = _run(d)
            ok = (p.returncode == 1 and "FLAGGED=5/6" in p.stdout) if expect_fail \
                else (p.returncode == 0 and "FLAGGED=0/6" in p.stdout)
            if fault == ci:
                print(f"AUDIT_SELFTEST: FAULT case {ci} forced")
                return 1
            print(f"CASE {ci} {tag} {'ok' if ok else 'FAIL'}")
            if not ok:
                print(f"AUDIT_SELFTEST: FAIL {tag} rc={p.returncode}\n{p.stdout}{p.stderr}")
                return 1
        # git-first-commit over a real scratch repo: claims and target added in one commit -> fires.
        g = tmp / "repo"
        g.mkdir()
        for cmd in (["git", "init", "-q"], ["git", "-C", str(g), "config", "user.email", "f@f"],
                    ["git", "-C", str(g), "config", "user.name", "f"]):
            subprocess.run(cmd, cwd=str(g), capture_output=True)
        (g / "claims.md").write_text(
            "**Controls (all committed before the freeze.\n"
            "S138 is the lead recorded in `SRC.md` `## Leads` by the previous round.\n", encoding="utf-8")
        (g / "ctl.txt").write_text("x\n", encoding="utf-8")
        (g / "SRC.md").write_text("## Registry\n| S138 | x |\n## Leads (unopened)\n- unnumbered lead\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(g), "add", "claims.md", "ctl.txt", "SRC.md"], capture_output=True)
        subprocess.run(["git", "-C", str(g), "commit", "-qm", "one"], capture_output=True)
        rev = subprocess.run(["git", "-C", str(g), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        (g / "audit.tsv").write_text(
            "G1\tgit-first-commit\tcommitted before the freeze\tctl.txt\t\tselftest r63 E1\n"
            f"G2\tsection-contains-at\tis the lead recorded in\tSRC.md\t## Leads|S138|{rev}\tselftest r62 #13\n"
            f"G3\tsection-contains-at\tis the lead recorded in\tSRC.md\t## Registry|S138|{rev}\tcontrol at revision\n",
            encoding="utf-8")
        p = _run(g)
        if fault == 3:
            print("AUDIT_SELFTEST: FAULT case 3 forced")
            return 1
        git_ok = (p.returncode == 1 and "FLAGGED=2/3" in p.stdout)
        print(f"CASE 3 git {'ok' if git_ok else 'FAIL'}")
        if not git_ok:
            print(f"AUDIT_SELFTEST: FAIL git rc={p.returncode}\n{p.stdout}{p.stderr}")
            return 1

        # C4: a stale anchor exits 2 with an AUDIT_STALE line (mutant classes A01/A02).
        d4 = tmp / "stale"
        d4.mkdir()
        (d4 / "claims.md").write_text("Nothing here names the anchor.\n", encoding="utf-8")
        (d4 / "audit.tsv").write_text(
            "R9\tsection-contains\tthe anchor absent from claims\tSOURCES.md\t## Registry|x\tstale case\n", encoding="utf-8")
        (d4 / "SOURCES.md").write_text("## Registry\n| S1 | x |\n", encoding="utf-8")
        p = _run(d4)
        if not _expect(4, "stale", p.returncode == 2 and "AUDIT_STALE R9" in p.stdout, p):
            return 1

        # C5: a case-only verbatim-heading mismatch fires (mutant class A05).
        d5 = tmp / "caseonly"
        d5.mkdir()
        (d5 / "SCORECARD.md").write_text("## Planned — round 9 (amended, 2026-01-01)\nbody\n", encoding="utf-8")
        (d5 / "claims.md").write_text("is amended by `planned — round 9` in the same commit.\n", encoding="utf-8")
        (d5 / "audit.tsv").write_text(
            "R5c\tverbatim-heading\tis amended by\tSCORECARD.md\t\tcase-only mismatch\n", encoding="utf-8")
        p = _run(d5)
        if not _expect(5, "caseonly", p.returncode == 1 and "FLAG R5c" in p.stdout, p):
            return 1

        # C6: an unreadable revision fires even when the current file carries the needle (A08).
        d6 = tmp / "deadrev"
        d6.mkdir()
        (d6 / "SRC.md").write_text("## Leads (unopened)\n- S138 lead\n", encoding="utf-8")
        (d6 / "claims.md").write_text("is the lead recorded in `SRC.md` `## Leads` here.\n", encoding="utf-8")
        (d6 / "audit.tsv").write_text(
            "R6d\tsection-contains-at\tis the lead recorded in\tSRC.md\t## Leads|S138|0000000000000000000000000000000000000000\tdead revision\n", encoding="utf-8")
        p = _run(d6)
        if not _expect(6, "deadrev", p.returncode == 1 and "unreadable" in p.stdout, p):
            return 1

        # C7: a duplicate rule id is rejected (mutant class A10).
        d7 = tmp / "dupid"
        d7.mkdir()
        (d7 / "claims.md").write_text("anchor line one\n", encoding="utf-8")
        (d7 / "audit.tsv").write_text(
            "R1\tsection-contains\tanchor line one\tS.md\t## R|x\tdup\n"
            "R1\tsection-contains\tanchor line one\tS.md\t## R|y\tdup\n", encoding="utf-8")
        (d7 / "S.md").write_text("## R\nx\ny\n", encoding="utf-8")
        p = _run(d7)
        if not _expect(7, "dupid", p.returncode == 1 and "duplicate rule id" in p.stderr, p):
            return 1

        # C8: the `nothing in the lane` quantifier arm fires (mutant class A12).
        d8 = tmp / "quant"
        d8.mkdir()
        (d8 / "claims.md").write_text(
            "nothing in the lane on revision names. Command: `grep -rl rev corpus/knowledge` prints nothing.\n", encoding="utf-8")
        (d8 / "audit.tsv").write_text(
            "R8\tscope-narrower\tnothing in the lane on revision\t\t\tquant arm\n", encoding="utf-8")
        p = _run(d8)
        if not _expect(8, "quant", p.returncode == 1 and "FLAG R8" in p.stdout, p):
            return 1

        # C9: a digit inside a word is not a named count (mutant class A06).
        d9 = tmp / "worddig"
        d9.mkdir()
        (d9 / "spec.json").write_text(json.dumps({"items": [1, 2]}), encoding="utf-8")
        (d9 / "claims.md").write_text("One v2 wave `w1`, 64 seats, done.\n", encoding="utf-8")
        (d9 / "audit.tsv").write_text(
            "R9x\tjson-count\tOne v2 wave `w1`, 64 seats\tspec.json:items\t\tword-internal digit\n", encoding="utf-8")
        p = _run(d9)
        if not _expect(9, "worddig", p.returncode == 1 and "FLAG R9x" in p.stdout, p):
            return 1

        # C10: FLAG lines are required on stdout (mutant class A03).
        d10 = tmp / "flagout"
        d10.mkdir()
        (d10 / "spec.json").write_text(json.dumps({"items": list(range(66))}), encoding="utf-8")
        (d10 / "claims.md").write_text("One v2 wave `w1`, 64 seats, done.\n", encoding="utf-8")
        (d10 / "audit.tsv").write_text(
            "R10\tjson-count\tOne v2 wave `w1`, 64 seats\tspec.json:items\t\tflags on stdout\n", encoding="utf-8")
        p = _run(d10)
        if not _expect(10, "flagout", p.returncode == 1 and any(l.startswith("FLAG ") for l in p.stdout.splitlines()), p):
            return 1
        print(f"AUDIT_SELFTEST=PASS ({cases} cases)")
        return 0
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--claims")
    ap.add_argument("--audit")
    ap.add_argument("--root", default=".")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--selftest-fault", type=int, default=0, dest="selftest_fault",
                    help="force case N's verdict check to fail (the selftest shown able to fail)")
    a = ap.parse_args()
    if a.selftest:
        return selftest(fault=a.selftest_fault)
    if a.selftest_fault:
        print("claims-audit-v2: --selftest-fault requires --selftest", file=sys.stderr)
        return 2
    if not (a.claims and a.audit):
        ap.print_usage()
        return 2
    return run_audit(pathlib.Path(a.claims), pathlib.Path(a.audit), pathlib.Path(a.root).resolve())


if __name__ == "__main__":
    sys.exit(main())
