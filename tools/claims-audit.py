#!/usr/bin/env python3
"""claims-audit — flag self-assessment statements in a frozen claims file that committed files contradict.

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

Self-test: builds isolated fixtures under TMPDIR (never the lane, never /tmp directly), runs all
six classes against a contradicted fixture (6 flags expected) and a corrected fixture (0 flags
expected), and prints `AUDIT_SELFTEST=PASS (<n> cases)`; exit 1 on any unexpected verdict.
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


def selftest() -> int:
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="claims-audit-selftest-", dir=os.environ.get("TMPDIR") or None))
    cases = 0
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
        for tag, claims_text, rules_text, expect_fail in (
                ("bad", bad_claims, rules_bad, True), ("good", good_claims, rules_good, False)):
            d = tmp / tag
            d.mkdir()
            (d / "claims.md").write_text(claims_text, encoding="utf-8")
            (d / "audit.tsv").write_text(rules_text, encoding="utf-8")
            for f in ("spec.json", "SOURCES.md", "SCORECARD.md", "runner.py"):
                (d / f).write_text((tmp / f).read_text(encoding="utf-8"), encoding="utf-8")
            p = subprocess.run([sys.executable, "-B", str(pathlib.Path(__file__).resolve()),
                                "--claims", str(d / "claims.md"), "--audit", str(d / "audit.tsv"),
                                "--root", str(d)], capture_output=True, text=True)
            cases += 1
            ok = (p.returncode == 1 and "FLAGGED=5/6" in p.stdout) if expect_fail \
                else (p.returncode == 0 and "FLAGGED=0/6" in p.stdout)
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
        p = subprocess.run([sys.executable, "-B", str(pathlib.Path(__file__).resolve()),
                            "--claims", str(g / "claims.md"), "--audit", str(g / "audit.tsv"),
                            "--root", str(g)], capture_output=True, text=True)
        cases += 1
        if not (p.returncode == 1 and "FLAGGED=2/3" in p.stdout):
            print(f"AUDIT_SELFTEST: FAIL git rc={p.returncode}\n{p.stdout}{p.stderr}")
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
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.claims and a.audit):
        ap.print_usage()
        return 2
    return run_audit(pathlib.Path(a.claims), pathlib.Path(a.audit), pathlib.Path(a.root).resolve())


if __name__ == "__main__":
    sys.exit(main())
