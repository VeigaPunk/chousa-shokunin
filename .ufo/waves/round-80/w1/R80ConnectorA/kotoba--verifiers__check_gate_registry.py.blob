#!/usr/bin/env python3
r"""check_gate_registry.py -- frozen counter for the round-54 C2 (consistency) claim.

Round 54, claim C2 (axis: consistency, the calibration sub-axis this lane
owns): the lane's registry home, `SKILL.md` (PROTOCOL.md § Gate standard,
Registry), has no `## Gate registry` table, so the lane's own description of
its gates and the scripts in `verifiers/` cannot be compared.  Round 54 adds
the table; this counter counts how many of the lane's verifier scripts have a
registry row that agrees with the repository at the measured revision.

This counter is frozen at the round-54 plan commit.  The heading, the header,
the universe rule, the allowed kinds and verdict classes and the owner are
pinned here and never read from the revision measured.  A later change is a
second measurement, never the declared one (corpus/QUALITY.md Q28).

Universe (M): every blob directly under `verifiers/` at the revision whose
name ends in `.py` or `.sh` (`git ls-tree`, no recursion; `__pycache__` and
`fixtures/` are trees and never count).

A verifier `verifiers/F` is CONFORMANT iff exactly one row of the first table
under the heading `## Gate registry` in SKILL.md (header cells, lower-cased,
backticks stripped: `name | kind | entry command | verdict map | self-test |
pinned values | write scope | owner`) has name cell `verifiers/F`, and:
  * kind cell is `gate` or `probe`;
  * the entry-command cell contains the text `verifiers/F`;
  * the verdict-map cell declares at least one `<code>=<class>` pair
    (`=`, `->` or `→`; class one of clean, failed, could-not-evaluate), no
    code twice; a `gate` declares `0=clean` and `1=failed`;
  * the self-test cell is `none` or names one or more backticked flags (`--x`).
    Each named flag must be an exact active handler in the file: a Python
    `add_argument` call with that exact string argument, or a shell `case` arm
    whose exact pattern is that flag. Comments and longer lookalike flags do
    not count. A `gate` may not say `none`.
  * a `probe` is rejected if its verdict map declares `1=failed` or its source
    has an exact active `--self-test` handler. This check reads only the row's
    verdict pairs and the script's Python AST `add_argument` string arguments
    or shell `case` arms; it does not run the script. This is a narrow
    failure-capability rule, not a proof of all possible exit behavior (Q31).
  * the pinned-values cell is `none`, `in-file`, or one or more backticked
    repo-relative paths each of which exists at the revision (`git cat-file -e
    <rev>:<path>`); a `gate` may not say `none`;
  * the write-scope cell is non-empty and not a dash;
  * the owner cell is `kotoba`.

A row whose name cell is a `verifiers/...` path outside the universe is a
PHANTOM row. The counter does not run verifier scripts or prove their actual
exit statuses; reviewers remain responsible for the limits of the checks
above (Q31).

Output: `gate registry rows conformant <K> of <M> lane verifiers; phantom <P>`.
Exit 0 iff K == M and P == 0, 1 otherwise, 2 = could not evaluate.

Usage:
  python3 -B verifiers/check_gate_registry.py --rev <rev> [--json]
  python3 -B verifiers/check_gate_registry.py --self-test
"""
from __future__ import annotations

import ast
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent.parent
HEADING = "## Gate registry"
HEADER = ("name", "kind", "entry command", "verdict map", "self-test",
          "pinned values", "write scope", "owner")
KINDS = ("gate", "probe")
CLASSES = ("clean", "failed", "could-not-evaluate")
OWNER = "kotoba"
PAIR_RE = re.compile(r"(\d+)\s*(?:=|->|\u2192)\s*(clean|failed|could-not-evaluate)\b")
FLAG_RE = re.compile(r"`(--[A-Za-z0-9][A-Za-z0-9-]*)`")
PATH_RE = re.compile(r"`([^`\s]+)`")

def has_flag_handler(path: str, src: bytes, flag: str) -> bool:
    if path.endswith(".py"):
        try:
            tree = ast.parse(src.decode("utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            return False
        return any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "add_argument"
            and any(isinstance(arg, ast.Constant) and arg.value == flag
                    for arg in node.args)
            for node in ast.walk(tree)
        )
    if path.endswith(".sh"):
        in_case = False
        for line in src.decode("utf-8", errors="replace").splitlines():
            if re.match(r"^\s*#", line):
                continue
            if re.match(r"^\s*case\b.*\bin\b", line):
                in_case = True
                continue
            if in_case and re.match(r"^\s*esac(?:\s|$)", line):
                in_case = False
                continue
            if in_case and re.match(r"^\s*" + re.escape(flag) + r"\)(?:\s|$)", line):
                return True
    return False


def git(rev_args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(LANE)] + rev_args, capture_output=True)


class Tree:
    """Read access to one revision of the lane."""

    def __init__(self, rev: str):
        self.rev = rev

    def universe(self) -> list[str]:
        r = git(["ls-tree", "-z", self.rev, "verifiers/"])
        if r.returncode != 0:
            raise RuntimeError("git ls-tree failed: %s" % r.stderr.decode(errors="replace").strip())
        out = []
        for rec in r.stdout.decode("utf-8").split("\0"):
            if not rec:
                continue
            meta, _, path = rec.partition("\t")
            if meta.split()[1] == "blob" and (path.endswith(".py") or path.endswith(".sh")):
                out.append(path)
        return sorted(out)

    def read(self, path: str) -> bytes | None:
        r = git(["show", "%s:%s" % (self.rev, path)])
        return r.stdout if r.returncode == 0 else None

    def exists(self, path: str) -> bool:
        return git(["cat-file", "-e", "%s:%s" % (self.rev, path.rstrip("/"))]).returncode == 0


def cells(line: str) -> list[str]:
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")) or len(s) < 2:
        return []
    return [c.strip() for c in s[1:-1].split("|")]


def clean(cell: str) -> str:
    return re.sub(r"[`*]", "", cell).strip().lower()


def registry_rows(text: str) -> list[list[str]]:
    rows, in_sec, header_ok, done = [], False, False, False
    for ln in text.splitlines():
        m = re.match(r"^(#{1,6})\s+", ln)
        if m:
            if ln.rstrip() == HEADING:
                in_sec, header_ok = True, False
                continue
            if in_sec and len(m.group(1)) <= 2:
                in_sec = False
            continue
        if not in_sec or done:
            continue
        c = cells(ln)
        if not c:
            if header_ok and rows:
                done = True
            continue
        if not header_ok:
            if tuple(clean(x) for x in c[:len(HEADER)]) == HEADER:
                header_ok = True
            continue
        if all(re.fullmatch(r":?-{3,}:?", x) for x in c):
            continue
        rows.append(c + [""] * (len(HEADER) - len(c)))
    return rows


def judge_row(r: list[str], path: str, src: bytes, exists) -> list[str]:
    why = []
    kind = clean(r[1])
    if kind not in KINDS:
        why.append("kind %r" % r[1])
    if path not in r[2]:
        why.append("entry command lacks %s" % path)
    pairs = PAIR_RE.findall(r[3])
    codes = [p[0] for p in pairs]
    if not pairs:
        why.append("verdict map declares no code=class pair")
    if len(codes) != len(set(codes)):
        why.append("verdict map declares a code twice")
    if kind == "gate" and not (("0", "clean") in pairs and ("1", "failed") in pairs):
        why.append("gate verdict map lacks 0=clean and 1=failed")
    if kind == "probe":
        if ("1", "failed") in pairs:
            why.append("probe verdict map declares 1=failed")
        if has_flag_handler(path, src, "--self-test"):
            why.append("probe script has an exact --self-test handler")
    st = r[4].strip()
    if clean(st) == "none":
        if kind == "gate":
            why.append("gate with self-test none")
    else:
        flags = FLAG_RE.findall(st)
        if not flags:
            why.append("self-test cell names no backticked flag")
        for f in flags:
            if not has_flag_handler(path, src, f):
                why.append("self-test flag %s lacks an exact handler" % f)
    pv = r[5].strip()
    if clean(pv) == "none":
        if kind == "gate":
            why.append("gate with pinned values none")
    elif clean(pv) != "in-file":
        paths = PATH_RE.findall(pv)
        if not paths:
            why.append("pinned-values cell names no backticked path")
        for p in paths:
            if p.startswith("/") or ".." in p.split("/") or not exists(p):
                why.append("pinned path %s does not exist" % p)
    if clean(r[6]) in ("", "-", "\u2014", "\u2013"):
        why.append("write scope empty")
    if clean(r[7]) != OWNER:
        why.append("owner %r" % r[7])
    return why


def judge(skill: str, universe: list[str], read, exists) -> tuple[list[dict], list[str]]:
    rows = registry_rows(skill)
    report = []
    for path in universe:
        mine = [r for r in rows if clean(r[0]) == path.lower()]
        if len(mine) != 1:
            report.append({"verifier": path, "conformant": False,
                           "why": ["registry rows naming it: %d (need 1)" % len(mine)]})
            continue
        src = read(path) or b""
        why = judge_row(mine[0], path, src, exists)
        report.append({"verifier": path, "conformant": not why, "why": why})
    uni = {p.lower() for p in universe}
    phantom = [clean(r[0]) for r in rows
               if clean(r[0]).startswith("verifiers/") and clean(r[0]) not in uni]
    return report, phantom


def self_test() -> int:
    assertions = 0
    failures = 0

    def check(name: str, actual: object, expected: object) -> None:
        nonlocal assertions, failures
        assertions += 1
        if actual != expected:
            failures += 1
            print("FAIL %s: got %r, expected %r" % (name, actual, expected))

    files = {"verifiers/a.py": b"import argparse\nap=argparse.ArgumentParser()\n"
             b"ap.add_argument('--self-test')", "verifiers/b.sh": b"echo",
             "verifiers/base.json": b"{}"}
    uni = ["verifiers/a.py", "verifiers/b.sh"]
    head = ("# s\n\n## Gate registry\n\n| Name | Kind | Entry command | Verdict map | Self-test |"
            " Pinned values | Write scope | Owner |\n|---|---|---|---|---|---|---|---|\n")
    row_a = ("| `verifiers/a.py` | gate | `python3 -B verifiers/a.py` | 0=clean, 1=failed, "
             "2=could-not-evaluate | `--self-test` | `verifiers/base.json` | none (read-only) | kotoba |\n")
    row_b = ("| `verifiers/b.sh` | probe | `bash verifiers/b.sh` | 0=clean | none | none |"
             " tmp clones | kotoba |\n")
    skill = head + row_a + row_b + "\n## Next\n"

    def ok(sk=skill, u=uni, fs=files):
        rep, ph = judge(sk, u, fs.get, lambda p: p in fs)
        return [r["verifier"] for r in rep if r["conformant"]], ph

    check("base world: both conformant", ok(), (["verifiers/a.py", "verifiers/b.sh"], []))
    check("missing row", ok(sk=head + row_a), (["verifiers/a.py"], []))
    check("duplicate row", ok(sk=head + row_a + row_a + row_b), (["verifiers/b.sh"], []))
    check("phantom row", ok(sk=skill.replace("## Next", "") + row_b.replace("b.sh", "c.sh")),
          (["verifiers/a.py", "verifiers/b.sh"], []))
    check("phantom row counted when inside the table",
          ok(sk=head + row_a + row_b + row_b.replace("b.sh", "c.sh")),
          (["verifiers/a.py", "verifiers/b.sh"], ["verifiers/c.sh"]))
    check("self-test flag absent from file",
          ok(sk=skill.replace("`--self-test`", "`--selftest`")), (["verifiers/b.sh"], []))
    borrowed = (b"import argparse\nap=argparse.ArgumentParser()\n"
                b"ap.add_argument('--other')\n# --self-test is handled elsewhere\n")
    check("self-test flag borrowed in a comment",
          ok(fs={**files, "verifiers/a.py": borrowed}), (["verifiers/b.sh"], []))
    check("shell exact case arm",
          has_flag_handler("verifiers/b.sh",
                           b'case "$1" in\n  --self-test) SELFTEST=1 ;;\nesac\n',
                           "--self-test"), True)
    check("shell lookalike case arm",
          has_flag_handler("verifiers/b.sh",
                           b'case "$1" in\n  --self-testing) SELFTEST=1 ;;\nesac\n',
                           "--self-test"), False)
    check("shell comment is not a case arm",
          has_flag_handler("verifiers/b.sh",
                           b'case "$1" in\n  # --self-test) SELFTEST=1 ;;\nesac\n',
                           "--self-test"), False)
    check("gate with self-test none", ok(sk=skill.replace("`--self-test`", "none")),
          (["verifiers/b.sh"], []))
    check("gate lacking 1=failed", ok(sk=skill.replace("1=failed, ", "")), (["verifiers/b.sh"], []))
    check("gate mapping 1 to clean", ok(sk=skill.replace("1=failed", "1=clean")),
          (["verifiers/b.sh"], []))
    check("code declared twice", ok(sk=skill.replace("2=could-not-evaluate", "1=could-not-evaluate")),
          (["verifiers/b.sh"], []))
    check("arrow form accepted", ok(sk=skill.replace("0=clean, 1=failed", "0 \u2192 clean, 1 -> failed")),
          (["verifiers/a.py", "verifiers/b.sh"], []))
    check("pinned path missing", ok(sk=skill.replace("`verifiers/base.json`", "`verifiers/gone.json`")),
          (["verifiers/b.sh"], []))
    check("pinned path climbing out", ok(sk=skill.replace("`verifiers/base.json`", "`../x/base.json`")),
          (["verifiers/b.sh"], []))
    check("gate pinned none", ok(sk=skill.replace("`verifiers/base.json`", "none")),
          (["verifiers/b.sh"], []))
    check("in-file pinned accepted", ok(sk=skill.replace("`verifiers/base.json`", "in-file")),
          (["verifiers/a.py", "verifiers/b.sh"], []))
    check("bad kind", ok(sk=skill.replace("| probe |", "| tool |")), (["verifiers/a.py"], []))
    check("entry command not naming file", ok(sk=skill.replace("`bash verifiers/b.sh`", "`bash b.sh`")),
          (["verifiers/a.py"], []))
    check("wrong owner", ok(sk=skill.replace("tmp clones | kotoba", "tmp clones | kake")),
          (["verifiers/a.py"], []))
    check("empty write scope", ok(sk=skill.replace("tmp clones", "\u2014")), (["verifiers/a.py"], []))
    check("table under another heading not read", ok(sk=skill.replace("## Gate registry", "## Gates")),
          ([], []))
    check("wrong header not read", ok(sk=skill.replace("| Owner |", "| Who |")), ([], []))
    check("probe without any pair", ok(sk=skill.replace("| 0=clean | none |", "| exits | none |")),
          (["verifiers/a.py"], []))
    probe_failed = row_b.replace("| 0=clean |", "| 0=clean, 1=failed |")
    check("probe with failed verdict is rejected",
          ok(sk=head + row_a + probe_failed), (["verifiers/a.py"], []))
    probe_none = (row_a.replace("| gate |", "| probe |")
                  .replace("0=clean, 1=failed, 2=could-not-evaluate", "0=clean")
                  .replace("| `--self-test` | `verifiers/base.json` |", "| none | none |"))
    check("all-probe/none table rejects script with self-test handler",
          ok(sk=head + probe_none + row_b), (["verifiers/b.sh"], []))

    print("self-test: %d failure(s) over %d assertions" % (failures, assertions))
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--rev")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        if args.rev or args.json:
            ap.error("--self-test cannot be combined with --rev or --json")
        return self_test()
    if not args.rev:
        ap.error("--rev is required")
    try:
        t = Tree(args.rev)
        universe = t.universe()
        raw = t.read("SKILL.md")
        if raw is None:
            raise RuntimeError("SKILL.md absent at %s" % args.rev)
        skill = raw.decode("utf-8")
        report, phantom = judge(skill, universe, t.read, t.exists)
    except (RuntimeError, UnicodeDecodeError, OSError) as e:
        print("could-not-evaluate: %s" % e, file=sys.stderr)
        return 2
    k = sum(1 for r in report if r["conformant"])
    if args.json:
        print(json.dumps({"conformant": k, "of": len(universe), "phantom": phantom,
                          "verifiers": report}, indent=1))
    else:
        for r in report:
            print("%-44s %s %s" % (r["verifier"], "OK" if r["conformant"] else "no",
                                   "; ".join(r["why"])))
        for p in phantom:
            print("PHANTOM %s" % p)
    print("gate registry rows conformant %d of %d lane verifiers; phantom %d"
          % (k, len(universe), len(phantom)))
    return 0 if k == len(universe) and not phantom else 1


if __name__ == "__main__":
    sys.exit(main())
