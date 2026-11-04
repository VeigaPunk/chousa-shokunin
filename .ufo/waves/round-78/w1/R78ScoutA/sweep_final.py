#!/usr/bin/env python3
"""Widened QUALITY.md pointer sweep (all criteria, both resolution rules, classified).

Rule A = corpus/evidence/round78/selfcheck.py's rule verbatim (token.lstrip("./")).
Rule B = same match with only a literal leading "./" removed (the hidden-path fix).
Every unresolved token is classified so content gaps are separable from token shapes
the frozen lexical rule cannot parse.
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

PATH_TOKEN = re.compile(r"`([^`\s]+)`")
NOT_A_PATH = ("http", "-", "$", "python", "git", "bash", "cc", "/")
CRIT = re.compile(r"^(\d{1,3})\.\s")
LINE_RANGE = re.compile(r"^(.+):\d+(?:[,-]\d+)*$")


def git(lane: pathlib.Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True)
    if p.returncode:
        raise SystemExit(f"git {' '.join(args)}: {p.stderr}")
    return p.stdout


def load(lane: pathlib.Path, rev: str | None) -> tuple[str, list[str]]:
    if rev:
        text = git(lane, "show", f"{rev}:corpus/QUALITY.md")
        tree = git(lane, "ls-tree", "-r", "--name-only", rev).splitlines()
    else:
        text = (lane / "corpus/QUALITY.md").read_text()
        tree = git(lane, "ls-files").splitlines()
    return text, [x for x in tree if x]


def match(tok: str, tree: list[str]) -> bool:
    if "*" in tok:
        rx = re.compile("^" + re.escape(tok).replace(r"\*", ".*") + "$")
        return any(rx.search(p) for p in tree)
    return any(p == tok or p.endswith("/" + tok) for p in tree)


def rule_a(tok: str, tree: list[str]) -> bool:
    return match(tok.lstrip("./"), tree)


def rule_b(tok: str, tree: list[str]) -> bool:
    return match(tok[2:] if tok.startswith("./") else tok, tree)


def classify(tok: str, tree: list[str]) -> str:
    if "=" in tok:
        return "output-snippet(not a path)"
    if re.fullmatch(r"[A-Za-z0-9_.+-]*\d+/\d+[A-Za-z0-9_.+-]*", tok):
        return "ratio(not a path)"
    if any(ch in tok for ch in "<>{}…") or "..." in tok:
        return "placeholder/fragment(not a path)"
    if tok in ("word/document.xml",):
        return "archive-internal(not a repo path)"
    if re.fullmatch(r"S\d+/S\d+/S\d+", tok):
        return "source-id shorthand(not a path)"
    if tok.endswith("/"):
        return "directory-token"
    if tok.startswith(".") and rule_b(tok, tree):
        return "HIDDEN-PATH rule artifact (lstrip)"
    if tok.startswith("real/"):
        return "runtime work tree (not committed by design)"
    if tok == "corpus/evidence/round59/claims.md":
        return "intentional negative citation (criterion 116)"
    if tok.startswith("knowledge/"):
        return "intentional negative citation (criterion 129)"
    if tok.startswith("R78ReviewB/"):
        return "UNCOMMITTED receipt (exists in .ufo/waves/round-78/w1/R78ReviewB/)"
    m = LINE_RANGE.match(tok)
    if m:
        base = m.group(1)
        if match(base, tree) or match(base.lstrip("./"), tree):
            return "LINE-ANCHORED path resolves (rule cannot strip :range)"
        return "GENUINE-UNRESOLVED (line-anchored, base missing)"
    if match(tok, tree):
        return "resolves under corrected rule only"
    if re.search(r"\{[^}]*\}", tok):
        return "brace-shorthand (expanded files exist)"
    if not any(p.startswith(tok + "/") for p in tree):
        return "GENUINE-UNRESOLVED"
    return "directory-token"


def main() -> int:
    lane = pathlib.Path(sys.argv[1])
    rev = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "worktree" else None
    text, tree = load(lane, rev)
    bodies: dict[int, str] = {}
    cur = None
    for line in text.splitlines():
        m = CRIT.match(line)
        if m:
            cur = int(m.group(1))
            bodies[cur] = line
        elif cur is not None and line and not line.startswith("#"):
            bodies[cur] += "\n" + line
    print(f"REV={rev or 'worktree'} TREE={len(tree)} CRITERIA={len(bodies)} "
          f"QUALITY_LINES={len(text.splitlines())} "
          f"QUALITY_SHA={__import__('hashlib').sha256(text.encode()).hexdigest()}")
    A: dict[int, list[str]] = {}
    B: dict[int, list[str]] = {}
    for cid in sorted(bodies):
        toks = [t for t in PATH_TOKEN.findall(bodies[cid])
                if " " not in t and not t.startswith(NOT_A_PATH) and "/" in t]
        a = [t for t in toks if not rule_a(t, tree)]
        b = [t for t in toks if not rule_b(t, tree)]
        if a:
            A[cid] = a
        if b:
            B[cid] = b
    print(f"RULE_A(exact instrument) criteria_with_gaps={len(A)} ids={sorted(A)}")
    print(f"RULE_B(hidden-path fixed) criteria_with_gaps={len(B)} ids={sorted(B)}")
    print(f"A_only(lstrip artifact alone) ids={sorted(set(A) - set(B))}")
    print("--- classified tokens under Rule B ---")
    genuine: dict[int, list[str]] = {}
    for cid in sorted(B):
        for t in B[cid]:
            kind = classify(t, tree)
            print(f"  {cid}\t{t}\t{kind}")
            if kind.startswith("GENUINE") or kind.startswith("UNTRACKED") or \
               kind.startswith("UNCOMMITTED"):
                genuine.setdefault(cid, []).append(t)
    print(f"CONTENT-LEVEL criteria={sorted(genuine)}")
    for cid, ts in genuine.items():
        print(f"  CONTENT {cid}: {ts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
