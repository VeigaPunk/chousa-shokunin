#!/usr/bin/env python3
"""Round-80 matrix battery v7 — the subject set is drawn per run, so no digest table
built from committed bytes maps it (QUALITY 152 successor to round 79's limit).

Unit under test: a MATRIX program that takes `--counter PATH --work DIR` and exits 0
iff a candidate counter satisfies every case it declares. The battery runs the matrix
against re-emitted copies of two positives and eleven forgers (the round-76 subject
set, referenced byte-identically from `corpus/evidence/round76/forgers/`), three
forged matrices, and the two round-79 oracles that identified a subject without
scoring it, under the round-78 legs plus the round-78 successor requirement, and adds
the round-80 FRESH LEG:

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

  FRESH LEG      Per run the battery draws `--fresh N` fresh positives and N fresh
                 forgers from the two committed positives by AST rewrite (semantics-
                 preserving: comparison-operand swap, if/else inversion, integer
                 constant folding) or AST mutation (operator flip, constant shift,
                 condition negation, branch swap). Ground truth is MEASURED, not
                 assumed: the committed witness matrix (`round76/loader-matrix-v3.py`)
                 runs the base copy and the candidate, and the candidate is a POSITIVE
                 only when verdict, marks and all twelve case cells are identical;
                 otherwise it is a FORGER. The matrix under test must accept every
                 fresh positive and reject every fresh forger. The drawn set is scored
                 by the matrix under test AND by every enumerated oracle, so an oracle
                 whose table was built from committed bytes cannot reach the PASS line.
                 No digest table built from committed bytes maps these subjects.

Predicate (same sentence as `corpus/evidence/round80/claims.md`):

  `python3 -B corpus/evidence/round80/matrix-battery-v7.py --matrix MATRIX --work DIR
   --fresh 2` exits 0 and prints exactly
  `BATTERY=PASS forgers_rejected=11/11 positive=2/2 fresh_positive=2/2 fresh_forgers=2/2 oracles_rejected=5/5`.

A forger is REJECTED only when both runs exit 1 with fewer than full marks; a positive
is ACCEPTED only when both runs exit 0 with full marks, `MATRIX=PASS`, and a valid
contract table. An exit of 2 is never scored in the matrix's favour. The five
enumerated oracles are the three committed forged matrices, the round-79
structure-identity matrix and the round-79 payload-decode forger re-pointed at the
committed lane; each must be REJECTED.

Closure-removal twins (mutation evidence, never the predicate): `--no-permute` runs the
fixed round-76 subject order, `--no-content` drops the contract-table requirement,
`--print-order` re-enables the round-77 `ORDER <i> <digest>` line, and `--no-fresh`
drops the fresh leg (the round-79 behaviour). `--reemit-only` emits one copy of each
committed subject into `--work` and exits 0 (the `derivative-check.py` entry point),
never scoring anything.

Limits (recorded, not closed): the fresh leg's ground truth is the committed witness
matrix, so a witness that is wrong about a case makes both legs wrong together; the
eleven committed forgers and the five oracles are the independent anchor. A classifier
that knows this generator's rewrite operators can still separate fresh positives from
fresh forgers statically; that channel is measured by the round-80 critic seat and
recorded, not certified closed. Line-count detection closes append; a forger that
truncates the receipt is not detected by it (the caller's exit code remains
authoritative).

Usage: python3 corpus/evidence/round80/matrix-battery-v7.py --matrix PATH --work DIR
       [--runs N] [--matrix-timeout S] [--fresh N] [--no-fresh] [--rev REV]
       [--no-permute] [--no-content] [--print-order] [--reemit-only]
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
R79F = LANE / "corpus/evidence/round79/forgers"
R80F = HERE / "forgers"
ORACLES = [("summary-only", R79F / "forge-order-matrix.py"),
           ("contract-table", R79F / "forge-order-matrix-table.py"),
           ("block-position", R79F / "forge-order-matrix-block.py"),
           ("structure-identity",
            LANE / ".ufo/waves/round-79/w1/R79ExecC/matrix-structure-identity.py"),
           ("payload-decode", R80F / "a10-payload-decode.py")]
WITNESS = LANE / "corpus/evidence/round76/loader-matrix-v3.py"

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
CHILD_TIMEOUT = "6"   # v7: raised from 3s; the fleet runs ~60 seats and a
                     # 3s child bound timed out intermittently (measured this round)

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
    env = dict(os.environ, LOADER_MATRIX_CHILD_TIMEOUT=CHILD_TIMEOUT,
               LOADER_MATRIX_LANE=str(LANE))
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


def _emit_tree(tree: ast.Module, work: pathlib.Path) -> pathlib.Path:
    """Write one marshalled-wrapper copy of `tree` under a fresh directory."""
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


def reemit(source: pathlib.Path, work: pathlib.Path) -> pathlib.Path:
    """Write a behaviour-preserving re-emission of `source` and return its path.

    QUALITY 147: a salt family is only ever one normalizer away from being stripped.
    v6 writes no source text at all — the copy is a wrapper around a marshalled code
    object built from a renamed, docstring-free AST under a random file name.
    """
    return _emit_tree(ast.parse(source.read_text()), work)


# ---- round-80 fresh-subject generation -------------------------------------
# Every operator below is a single AST edit applied once. The FRESH LEG never
# assumes which side an edit lands on: the committed witness matrix measures the
# candidate's twelve case cells and its verdict, and the candidate is a POSITIVE
# only when they are identical to its base copy's.

WITNESS_TIMEOUT = "20"   # ground truth only: a timed-out witness run is not evidence

# Rewrite operators must be semantics-preserving; mutation operators must not be.
# A single-op comparison is only swappable when the swap keeps the relation: `x < n`
# is `n > x`, but `x == n` is not `n != x` (measured this round: an Eq in the swap map
# turned the successor counter from 12/12 into 0/12).
_CMP_SWAP = {ast.Lt: ast.Gt, ast.Gt: ast.Lt, ast.LtE: ast.GtE, ast.GtE: ast.LtE}
_CMP_ANY = dict(_CMP_SWAP, Eq=ast.NotEq, NotEq=ast.Eq)


def _is_single_cmp(node) -> bool:
    return isinstance(node, ast.Compare) and len(node.ops) == 1 and type(node.ops[0]) in _CMP_SWAP


def _is_single_cmp_any(node) -> bool:
    return isinstance(node, ast.Compare) and len(node.ops) == 1 and type(node.ops[0]) in _CMP_ANY


def _is_if_else(node) -> bool:
    return isinstance(node, ast.If) and bool(node.orelse)


def _is_small_int(node) -> bool:
    return (isinstance(node, ast.Constant) and type(node.value) is int
            and 2 <= abs(node.value) < 10 ** 6)


def _op_swap_cmp(node):
    node.left, node.comparators = node.comparators[0], [node.left]
    node.ops = [_CMP_SWAP[type(node.ops[0])]()]
    return node


def _op_invert_if(node):
    node.test = ast.UnaryOp(op=ast.Not(), operand=node.test)
    node.body, node.orelse = node.orelse, node.body
    return node


def _op_fold_int(node):
    v = node.value
    new = ast.BinOp(left=ast.Constant(v // 2), op=ast.Add(), right=ast.Constant(v - v // 2))
    return ast.copy_location(new, node)


def _op_flip_cmp(node):
    node.ops = [_CMP_ANY[type(node.ops[0])]()]
    return node


def _op_shift_int(node):
    node.value = node.value + 1
    return node


def _op_negate(node):
    node.test = ast.UnaryOp(op=ast.Not(), operand=node.test)
    return node


def _op_swap_branches(node):
    node.body, node.orelse = node.orelse, node.body
    return node


def _is_return(node) -> bool:
    return isinstance(node, ast.Return) and node.value is not None


def _op_return_const(node):
    node.value = ast.Constant(secrets.randbelow(2))
    return node


def _is_str_const(node) -> bool:
    return (isinstance(node, ast.Constant) and isinstance(node.value, str)
            and 0 < len(node.value) < 80)


def _op_str_shift(node):
    node.value = node.value + "x"
    return node


REWRITE_OPS = [(_is_single_cmp, _op_swap_cmp),
               (_is_if_else, _op_invert_if),
               (_is_small_int, _op_fold_int)]
MUTATION_OPS = [(_is_single_cmp_any, _op_flip_cmp),
                (_is_small_int, _op_shift_int),
                (_is_if_else, _op_negate),
                (_is_if_else, _op_swap_branches),
                (_is_return, _op_return_const),
                (_is_str_const, _op_str_shift)]


class _Once(ast.NodeTransformer):
    """Apply `fn` to the first node `match` accepts; record whether it fired."""

    def __init__(self, match, fn):
        self.match, self.fn, self.fired = match, fn, False

    def visit(self, node):
        if not self.fired and self.match(node):
            self.fired = True
            return self.fn(node)
        return super().visit(node)


def _apply(tree: ast.Module, match, fn) -> bool:
    tr = _Once(match, fn)
    tr.visit(tree)
    return tr.fired


def _witness_out(subject: pathlib.Path, work: pathlib.Path, timeout: int):
    """Run the committed witness matrix; return (rc, marks, case cells) or None."""
    work.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, LOADER_MATRIX_CHILD_TIMEOUT=WITNESS_TIMEOUT,
               LOADER_MATRIX_LANE=str(LANE))
    try:
        p = subprocess.run([sys.executable, "-B", str(WITNESS), "--counter", str(subject),
                            "--work", str(work)], stdin=subprocess.DEVNULL,
                           capture_output=True, text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        return None
    marks = None
    for line in p.stdout.splitlines():
        m = MATRIX_LINE.match(line)
        if m:
            marks = (int(m.group(1)), int(m.group(2)), m.group(3))
    # the matrix emits its twelve cases in a per-run order; compare them as a set
    cells = tuple(sorted(line for line in p.stdout.splitlines() if CASE_LINE.match(line)))
    return p.returncode, marks, cells


def draw_fresh(work: pathlib.Path, timeout: int, want: str, attempts: int = 40):
    """Draw a fresh subject whose ground truth is measured; return (copy, base, group)."""
    for _ in range(attempts):
        base_name, base_path = POSITIVES[secrets.randbelow(len(POSITIVES))]
        tree = ast.parse(base_path.read_text())
        _drop_docstrings(tree)   # a mutation must not land in a docstring that is dropped
        if want == "POSITIVE":
            ops = list(REWRITE_OPS)
            random.Random(secrets.randbits(64)).shuffle(ops)
            fired = False
            for match, fn in ops[:2]:
                fired = _apply(tree, match, fn) or fired
            if not fired:
                continue
        else:
            fired = 0
            for _ in range(2):
                match, fn = MUTATION_OPS[secrets.randbelow(len(MUTATION_OPS))]
                fired += _apply(tree, match, fn)
            if not fired:
                continue
        copy = _emit_tree(tree, work)
        base_copy = _emit_tree(ast.parse(base_path.read_text()), work)
        wb = _witness_out(base_copy, copy.parent / "wb", timeout)
        wc = _witness_out(copy, copy.parent / "wc", timeout)
        shutil.rmtree(base_copy.parent, ignore_errors=True)
        if wb is None or wc is None:
            shutil.rmtree(copy.parent, ignore_errors=True)
            continue
        if any("timeout=True" in cell for cell in wb[2] + wc[2]):
            shutil.rmtree(copy.parent, ignore_errors=True)
            continue
        group = "POSITIVE" if (wb[0] == wc[0] and wb[1] == wc[1] and wb[2] == wc[2]) else "FORGER"
        if group == want:
            return copy, base_name, group
        shutil.rmtree(copy.parent, ignore_errors=True)
    return None, None, None


def score(matrix: pathlib.Path, subjects, runs: int, work: pathlib.Path,
          matrix_timeout: int, permute: bool, content: bool, label: str,
          print_order: bool, fresh=()):
    """Run every committed and every pre-emitted fresh subject `runs` times.

    `fresh` entries are (group, name, copy) with the copy already emitted under `work`;
    they are scored exactly like committed subjects but never re-emitted or removed here,
    so the same drawn set is scored by the matrix under test and by every oracle.
    Returns {positive|forger|fresh_positive|fresh_forger: [ok, all]}.
    """
    entries = [(group, name, source, False) for group, name, source in subjects]
    entries += [(group, name, copy, True) for group, name, copy in fresh]
    results = {name: [] for _group, name, _src, _pre in entries}
    buffered: list[str] = []
    for i in range(runs):
        order = list(entries)
        if permute:
            random.Random(secrets.randbits(64)).shuffle(order)
        if print_order:
            buffered.append(f"{label} ORDER {i} " + hashlib.sha256(
                "|".join(name for _g, name, _s, _p in order).encode()).hexdigest())
        for group, name, source, pre in order:
            subject = source if pre else reemit(source, work)
            rc, marks, ok = run_matrix(matrix, subject, subject.parent / "w", matrix_timeout, content)
            results[name].append((rc, marks, ok))
            buffered.append(f"{label} RUN {group} {name} {i} matrix_exit="
                            f"{'timeout' if rc is None else rc} "
                            f"marks={'/'.join(str(x) for x in marks) if marks else 'none'} "
                            f"content={'ok' if ok else 'bad'}")
            if not pre:
                shutil.rmtree(subject.parent, ignore_errors=True)
    counts = {"positive": [0, 0], "forger": [0, 0],
              "fresh_positive": [0, 0], "fresh_forger": [0, 0]}
    for group, name, _source, pre in entries:
        observed = results[name]
        key = ("fresh_" if pre else "") + group.lower()
        if group == "POSITIVE":
            ok = all(rc == 0 for rc, marks, content_ok in observed)   # N4: exit code only
            counts[key][0] += ok
            counts[key][1] += 1
            buffered.append(f"{label} SUBJECT {group} {name} {'ACCEPTED' if ok else 'MISS'}")
        else:
            ok = all(rc == 1 for rc, marks, content_ok in observed)   # N4: exit code only
            counts[key][0] += ok
            counts[key][1] += 1
            buffered.append(f"{label} SUBJECT {group} {name} {'REJECTED' if ok else 'MISS'}")
    for line in buffered:
        emit(line)
    return counts


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--matrix", default=None)
    ap.add_argument("--work", required=True)
    ap.add_argument("--runs", type=int, default=2)
    ap.add_argument("--matrix-timeout", type=int, default=300)
    ap.add_argument("--fresh", type=int, default=2,
                    help="fresh positives and fresh forgers drawn per run (default 2)")
    ap.add_argument("--no-fresh", action="store_true",
                    help="drop the fresh leg (round-79 behaviour; comparison only)")
    ap.add_argument("--rev", default=None,
                    help="lane revision named in the receipt (default: master tip)")
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
    rev = a.rev or _lane_rev()
    emit(f"LANE_REV={rev}")
    emit(f"RUNS={a.runs} CHILD_TIMEOUT={CHILD_TIMEOUT} MATRIX_TIMEOUT={a.matrix_timeout} "
         f"PERMUTE={permute} CONTENT={content} FRESH={0 if a.no_fresh else a.fresh}")
    fresh_n = 0 if a.no_fresh else a.fresh
    try:
        fresh_list = []
        for i in range(fresh_n):
            for want in ("POSITIVE", "FORGER"):
                copy, base_name, group = draw_fresh(run, a.matrix_timeout, want)
                if copy is None:
                    print(f"matrix-battery-v7: cannot draw a fresh {want} in 40 attempts",
                          file=sys.stderr)
                    return 2
                fresh_list.append((group, f"{base_name}#{i}", copy))
        counts = score(matrix, subjects, a.runs, run, a.matrix_timeout,
                       permute, content, "MATRIX", a.print_order, fresh_list)
        oracle_ok = 0
        for name, source in ORACLES:
            if not source.is_file():
                print(f"matrix-battery-v7: missing oracle {source}", file=sys.stderr)
                return 2
            copy = reemit(source, run)
            o = score(copy, subjects, a.runs, copy.parent / "w", a.matrix_timeout,
                      permute, content, f"ORACLE:{name}", a.print_order, fresh_list)
            full = all(o[key][0] == o[key][1] for key in o)
            oracle_ok += not full
            emit(f"ORACLE {name} {'REJECTED' if not full else 'MISS'} "
                 + " ".join(f"{key}={v[0]}/{v[1]}" for key, v in o.items()))
            shutil.rmtree(copy.parent, ignore_errors=True)
    finally:
        shutil.rmtree(run, ignore_errors=True)
    verdict = (all(counts[key][0] == counts[key][1] for key in counts)
               and oracle_ok == len(ORACLES))
    summary = (f"forgers_rejected={counts['forger'][0]}/{counts['forger'][1]} "
               f"positive={counts['positive'][0]}/{counts['positive'][1]} "
               f"fresh_positive={counts['fresh_positive'][0]}/{counts['fresh_positive'][1]} "
               f"fresh_forgers={counts['fresh_forger'][0]}/{counts['fresh_forger'][1]} "
               f"oracles_rejected={oracle_ok}/{len(ORACLES)}")
    emit(summary)
    emit(f"RECEIPT_LINES={_LINES + 2}")
    emit(f"BATTERY={'PASS' if verdict else 'FAIL'} {summary}")
    return 0 if verdict else 1


def _lane_rev() -> str:
    try:
        p = subprocess.run(["git", "-C", str(LANE), "rev-parse", "master"],
                           capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return "unavailable"
    return p.stdout.strip() or "unavailable"


if __name__ == "__main__":
    sys.exit(main())
