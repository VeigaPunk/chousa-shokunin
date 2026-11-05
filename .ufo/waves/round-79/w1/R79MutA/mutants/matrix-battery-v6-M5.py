#!/usr/bin/env python3
"""Round-79 matrix battery v6 — the subject copy is not a textual derivative of a
public file (QUALITY 147 successor).

Unit under test: a MATRIX program that takes `--counter PATH --work DIR` and exits 0
iff a candidate counter satisfies every case it declares. The battery runs the matrix
against re-emitted copies of two positives and eleven forgers (the round-76 subject
set, referenced byte-identically from `corpus/evidence/round76/forgers/`) and three
forged matrices, under the round-78 legs plus the round-78 successor requirement:

  ORDER LEG      The subject list is permuted per run with a fresh 64-bit seed
                 (`secrets.randbits`). The permutation is never printed and no digest
                 of it is printed.
  QUIET LEG      No per-subject line is printed while subjects are running; every
                 `MATRIX RUN`/`SUBJECT` line is buffered and flushed after the scoring
                 loop ends.
  CONTENT LEG    Every matrix run must print the twelve `CASE` lines of the frozen
                 contract with cells equal to the battery's own independently stated
                 contract map, and a summary count equal to the number of `PASS` lines.
  IDENTITY LEG   **Re-emission, not salting.** Round 78 inserted an inert statement into
                 the source text, so a four-line normalizer deleted the `_r78<hex>`
                 family and recovered every subject byte-for-byte (`R78L1/a8-normalizer.py`).
                 v6 never writes the source text: it parses the subject, drops every
                 docstring, renames every bound identifier through a fresh per-copy table
                 (imports, keyword-argument names, builtins and dunders excluded), inserts
                 one random-named integer assignment after the last `__future__` import at a
                 random top-level position, compiles the tree under a random file name and
                 writes a wrapper that `exec`s the marshalled code object. No 40-byte window
                 of the committed source occurs in the copy.
  RECEIPT LEG    The verdict is bound to the process exit code and to a `RECEIPT_LINES`
                 trailer printed immediately before the predicate line.

Predicate (same sentence as `corpus/evidence/round79/claims.md`):

  `python3 -B corpus/evidence/round79/matrix-battery-v6.py --matrix MATRIX --work DIR`
  exits 0 and prints exactly
  `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`.

A forger is REJECTED only when both runs exit 1 with fewer than full marks; a positive
is ACCEPTED only when both runs exit 0 with full marks, `MATRIX=PASS`, and a valid
contract table. An exit of 2 is never scored in the matrix's favour.

Closure-removal twins (mutation evidence, never the predicate): `--no-permute` runs the
fixed round-76 subject order, `--no-content` drops the contract-table requirement and
`--print-order` re-enables the round-77 `ORDER <i> <digest>` line for comparison.
`--reemit-only` emits one copy of each subject into `--work` and exits 0 (the
`derivative-check.py` entry point), never scoring anything.

Limits (recorded, not closed): re-emission preserves behaviour, so the subject's
*semantics* are still identical and a normalizer that unmarshals the payload and
canonicalizes the fresh identifier table recovers the module's structure; that is a
structure-identity channel, measured by the wave, not a textual one. The battery proves
these thirteen subjects plus three forged matrices at these re-emissions and these
permutations. It does not prove arbitrary-forgery freedom. Line-count detection closes
append; a forger that truncates the receipt is not detected by it (the caller's exit
code remains authoritative).

Usage: python3 corpus/evidence/round79/matrix-battery-v6.py --matrix PATH --work DIR
       [--runs N] [--matrix-timeout S] [--no-permute] [--no-content] [--print-order]
       [--reemit-only]
Exit: 0 BATTERY=PASS · 1 BATTERY=FAIL · 2 usage/env.
"""
from __future__ import annotations

import argparse
import ast
import base64
import builtins
import hashlib
import marshal
import os
import pathlib
import random
import re
import secrets
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[2]

POSITIVES = [("successor-counter", LANE / "corpus/evidence/round74/correction-count.py"),
             ("ref-counter", LANE / "corpus/evidence/round75/ref-counter.py")]
R76F = LANE / "corpus/evidence/round76/forgers"
FORGERS = [("constant-pass", R76F / "forge-constant-pass.py"),
           ("constant-fail", R76F / "forge-constant-fail.py"),
           ("order-twelve", R76F / "forge-order-twelve.py"),
           ("diff-only", R76F / "forge-diff-only.py"),
           ("naive-grep", R76F / "forge-naive-grep.py"),
           ("subject-map", R76F / "forge-subject-map.py"),
           ("tree-identity", R76F / "forge-tree-identity.py"),
           ("size-map", R76F / "forge-size-map.py"),
           ("harness-source", R76F / "forge-harness-source.py"),
           ("seed-leak", R76F / "forge-seed-leak.py"),
           ("hang", R76F / "forge-hang.py")]
ORACLES = [("summary-only", HERE / "forgers" / "forge-order-matrix.py"),
           ("contract-table", HERE / "forgers" / "forge-order-matrix-table.py"),
           ("block-position", HERE / "forgers" / "forge-order-matrix-block.py")]

# The twelve-case contract, stated here independently of the matrix's own CASES table
# (QUALITY 128: an expected root is independently stated, never inferred from the
# subject's own assertion). name -> (expected_rc, expected_failed set).
CONTRACT = {
    "case-00-unchanged": (0, ""),
    "case-01-append": (0, ""),
    "case-02-append": (0, ""),
    "case-03-append": (0, ""),
    "case-04-delete": (1, "C2-6"),
    "case-05-delete": (1, "C2-6"),
    "case-06-delete": (1, "C2-6"),
    "case-07-replace-equal": (1, "C2-6"),
    "case-08-receipt-change": (1, "C2-7"),
    "case-09-dup-log-heading": (1, "C2-1,C2-2"),
    "case-10-dup-lesson-heading": (1, "C2-3,C2-5"),
    "case-11-dup-card-heading": (1, "C2-4"),
}

MATRIX_LINE = re.compile(r"^LOADER_MATRIX=(\d+)/(\d+) (?:MATRIX|C1)=(PASS|FAIL)$")
CASE_LINE = re.compile(r"^CASE (\S+) (PASS|FAIL) expected_rc=(-?\d+) actual_rc=(-?\d+) "
                       r"timeout=(True|False) failed=(\S+) expected_failed=(\S+)$")
CHILD_TIMEOUT = "3"

WRAPPER = '''#!/usr/bin/env python3
import base64 as _b, marshal as _m
exec(_m.loads(_b.b85decode({payload!r})), {{"__name__": "__main__", "__file__": __file__}})
'''

_LINES = 0


def emit(text: str = "") -> None:
    """Write one receipt line and count it (the RECEIPT_LINES trailer is bound to this)."""
    global _LINES
    print(text)
    _LINES += 1


def contract_table_ok(out: str, marks) -> bool:
    """Content leg: the twelve contract lines, their expected cells, and a consistent count."""
    seen: dict[str, tuple[str, str]] = {}
    for line in out.splitlines():
        m = CASE_LINE.match(line)
        if not m:
            continue
        name = m.group(1)
        if name in seen:
            return False
        seen[name] = (m.group(3), m.group(7))
    if set(seen) != set(CONTRACT):
        return False
    for name, (expected_rc, expected_failed) in CONTRACT.items():
        rc_cell, failed_cell = seen[name]
        if rc_cell != str(expected_rc) or failed_cell != (expected_failed or "none"):
            return False
    if marks is None:
        return False
    passed = sum(1 for line in out.splitlines()
                 if CASE_LINE.match(line) and CASE_LINE.match(line).group(2) == "PASS")
    return passed == marks[0]


def run_matrix(matrix: pathlib.Path, subject: pathlib.Path, work: pathlib.Path,
               matrix_timeout: int, content: bool):
    """Return (rc_or_None, marks_or_None, content_ok)."""
    work.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, LOADER_MATRIX_CHILD_TIMEOUT=CHILD_TIMEOUT)
    try:
        p = subprocess.run([sys.executable, "-B", str(matrix), "--counter", str(subject),
                            "--work", str(work)],
                           stdin=subprocess.DEVNULL, capture_output=True, text=True,
                           timeout=matrix_timeout, env=env)
    except subprocess.TimeoutExpired:
        return None, None, False
    marks = None
    for line in p.stdout.splitlines():
        m = MATRIX_LINE.match(line)
        if m:
            marks = (int(m.group(1)), int(m.group(2)), m.group(3))
    ok = contract_table_ok(p.stdout, marks) if content else True
    return p.returncode, marks, ok


def _drop_docstrings(tree: ast.Module) -> None:
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                                 ast.ClassDef)):
            continue
        body = node.body
        if (body and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)):
            node.body = body[1:] or [ast.Pass()]


def _fresh(taken: set[str]) -> str:
    while True:
        name = "_" + secrets.token_hex(4)
        if name not in taken:
            return name


def _rename(tree: ast.Module) -> dict[str, str]:
    """Rename every bound identifier through a fresh per-copy table.

    A single string-keyed map applied to every `Name`, parameter, def/class name,
    handler and global/nonlocal name preserves shadowing exactly. Excluded: imported
    names (their binding is an alias node), keyword-argument names (a caller passes
    them by spelling), builtins and dunders.
    """
    excluded: set[str] = set(dir(builtins))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                excluded.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                excluded.add(alias.asname or alias.name)
        elif isinstance(node, ast.keyword) and node.arg:
            excluded.add(node.arg)
    mapping: dict[str, str] = {}

    def name_for(old: str) -> str:
        if old in mapping:
            return mapping[old]
        if old in excluded or old.startswith("__"):
            mapping[old] = old
            return old
        new = _fresh(excluded)
        excluded.add(new)
        mapping[old] = new
        return new

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            node.id = name_for(node.id)
        elif isinstance(node, ast.arg):
            node.arg = name_for(node.arg)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            node.name = name_for(node.name)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            node.name = name_for(node.name)
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            node.names = [name_for(n) for n in node.names]
        elif type(node).__name__ in ("MatchAs", "MatchStar"):
            rest = getattr(node, "name", None)
            if rest:
                node.name = name_for(rest)
        elif type(node).__name__ == "MatchMapping":
            rest = getattr(node, "rest", None)
            if rest:
                node.rest = name_for(rest)
    return mapping


def reemit(source: pathlib.Path, work: pathlib.Path) -> pathlib.Path:
    """Write a behaviour-preserving re-emission of `source` and return its path.

    QUALITY 147: a salt family is only ever one normalizer away from being stripped.
    v6 writes no source text at all — the copy is a wrapper around a marshalled code
    object built from a renamed, docstring-free AST under a random file name.
    """
    text = source.read_text()
    tree = ast.parse(text)
    _drop_docstrings(tree)
    _rename(tree)
    pad = "_" + secrets.token_hex(5)
    stmt = ast.parse(f"{pad} = {secrets.randbelow(10 ** 9)}\n").body[0]
    futures = [n.lineno for n in tree.body
               if isinstance(n, ast.ImportFrom) and n.module == "__future__"]
    floor = max(futures) if futures else 0
    anchors = [i for i, n in enumerate(tree.body) if n.lineno > floor]
    pos = anchors[secrets.randbelow(len(anchors))] if anchors else len(tree.body)
    tree.body.insert(pos, stmt)
    ast.fix_missing_locations(tree)
    code = compile(tree, "<" + secrets.token_hex(6) + ">", "exec")
    payload = base64.b85encode(marshal.dumps(code)).decode()
    d = work / secrets.token_hex(8)
    d.mkdir(parents=True)
    target = d / "subject.py"
    target.write_text(WRAPPER.format(payload=payload))
    return target


def score(matrix: pathlib.Path, subjects, runs: int, work: pathlib.Path,
          matrix_timeout: int, permute: bool, content: bool, label: str,
          print_order: bool):
    """Run every subject `runs` times; return (pos_ok, pos_all, forg_ok, forg_all)."""
    results = {name: [] for _group, name, _src in subjects}
    buffered: list[str] = []
    for i in range(runs):
        order = list(subjects)
        if permute:
            random.Random(secrets.randbits(64)).shuffle(order)
        if print_order:
            buffered.append(f"{label} ORDER {i} " + hashlib.sha256(
                "|".join(name for _g, name, _s in order).encode()).hexdigest())
        for group, name, source in order:
            subject = reemit(source, work)
            rc, marks, ok = run_matrix(matrix, subject, subject.parent / "w", matrix_timeout, content)
            results[name].append((rc, marks, ok))
            buffered.append(f"{label} RUN {group} {name} {i} matrix_exit="
                            f"{'timeout' if rc is None else rc} "
                            f"marks={'/'.join(str(x) for x in marks) if marks else 'none'} "
                            f"content={'ok' if ok else 'bad'}")
            shutil.rmtree(subject.parent, ignore_errors=True)
    pos_ok = pos_all = forg_ok = forg_all = 0
    for group, name, _source in subjects:
        observed = results[name]
        if group == "POSITIVE":
            ok = all(rc == 0 and marks is not None and marks[0] == marks[1]
                     and marks[2] == "PASS" and content_ok for rc, marks, content_ok in observed)
            pos_ok += ok
            pos_all += 1
            buffered.append(f"{label} SUBJECT {group} {name} {'ACCEPTED' if ok else 'MISS'}")
        else:
            ok = all(rc == 1 and marks is not None and marks[0] < marks[1] and content_ok
                     for rc, marks, content_ok in observed)
            forg_ok += ok
            forg_all += 1
            buffered.append(f"{label} SUBJECT {group} {name} {'REJECTED' if ok else 'MISS'}")
    for line in buffered:
        emit(line)
    return pos_ok, pos_all, forg_ok, forg_all


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--matrix", default=None)
    ap.add_argument("--work", required=True)
    ap.add_argument("--runs", type=int, default=2)
    ap.add_argument("--matrix-timeout", type=int, default=300)
    ap.add_argument("--no-permute", action="store_true")
    ap.add_argument("--no-content", action="store_true")
    ap.add_argument("--print-order", action="store_true",
                    help="re-enable the round-77 ORDER digest line (comparison only)")
    ap.add_argument("--reemit-only", action="store_true",
                    help="emit one copy of every subject into --work and exit 0")
    a = ap.parse_args()
    work = pathlib.Path(a.work).resolve()
    if a.runs < 1 or a.matrix_timeout < 1:
        print("matrix-battery-v6: --runs and --matrix-timeout must be >= 1", file=sys.stderr)
        return 2
    try:
        work.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"matrix-battery-v6: cannot create --work {work}: {exc}", file=sys.stderr)
        return 2
    if not work.is_dir():
        print(f"matrix-battery-v6: --work {work} is not a directory", file=sys.stderr)
        return 2
    subjects = ([("POSITIVE", n, p) for n, p in POSITIVES]
                + [("FORGER", n, p) for n, p in FORGERS])
    for _group, _name, source in subjects:
        if not pathlib.Path(source).resolve().is_file():
            print(f"matrix-battery-v6: missing subject {source}", file=sys.stderr)
            return 2
    if a.reemit_only:
        run = work / ("r79-emit-" + secrets.token_hex(8))
        run.mkdir()
        for _group, name, source in subjects:
            copy = reemit(source, run)
            print(f"EMIT {name} {copy}")
        return 0
    if not a.matrix:
        print("matrix-battery-v6: --matrix is required unless --reemit-only", file=sys.stderr)
        return 2
    matrix = pathlib.Path(a.matrix).resolve()
    if not matrix.is_file():
        print(f"matrix-battery-v6: missing matrix {matrix}", file=sys.stderr)
        return 2
    permute = not a.no_permute
    content = not a.no_content
    run = work / ("r79-" + secrets.token_hex(8))
    try:
        run.mkdir()
    except OSError as exc:
        print(f"matrix-battery-v6: cannot create {run}: {exc}", file=sys.stderr)
        return 2
    emit("MATRIX_PATH=" + str(matrix))
    emit("MATRIX_SHA256=" + hashlib.sha256(matrix.read_bytes()).hexdigest())
    emit(f"RUNS={a.runs} CHILD_TIMEOUT={CHILD_TIMEOUT} MATRIX_TIMEOUT={a.matrix_timeout} "
         f"PERMUTE={permute} CONTENT={content}")
    try:
        p_ok, p_all, f_ok, f_all = score(matrix, subjects, a.runs, run, a.matrix_timeout,
                                         permute, content, "MATRIX", a.print_order)
        oracle_ok = 0
        for name, source in ORACLES:
            if not source.is_file():
                print(f"matrix-battery-v6: missing oracle {source}", file=sys.stderr)
                return 2
            copy = reemit(source, run)
            op_ok, op_all, of_ok, of_all = score(copy, subjects, a.runs, copy.parent / "w",
                                                 a.matrix_timeout, permute, content,
                                                 f"ORACLE:{name}", a.print_order)
            full = op_ok == op_all and of_ok == of_all
            oracle_ok += not full
            emit(f"ORACLE {name} {'REJECTED' if not full else 'MISS'} "
                 f"positive={op_ok}/{op_all} forgers_rejected={of_ok}/{of_all}")
            shutil.rmtree(copy.parent, ignore_errors=True)
    finally:
        shutil.rmtree(run, ignore_errors=True)
    verdict = (p_ok == p_all and f_ok == f_all and oracle_ok == len(ORACLES))
    emit(f"forgers_rejected={f_ok}/{f_all} positive={p_ok}/{p_all} "
         f"oracle={'REJECTED' if oracle_ok == len(ORACLES) else 'MISS'}")
    emit(f"BATTERY={'PASS' if verdict else 'FAIL'} forgers_rejected={f_ok}/{f_all} "
         f"positive={p_ok}/{p_all} oracle={'REJECTED' if oracle_ok == len(ORACLES) else 'MISS'}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
