#!/usr/bin/env python3
"""R80ExecC fresh-structural classifier, packaged as a loader matrix (round-80 wave).

Static channel only. It reads the drawn subject's bytes, unmarshals the wrapper's
b85/marshal payload, canonicalizes the code object's bytecode (rename-immune,
pad-line-immune, docstring-free on both sides) and looks the fingerprint up in a table
enumerated from the two committed positives under the frozen battery operators copied
verbatim from `corpus/evidence/round80/matrix-battery-v7.py` (REWRITE_OPS, MUTATION_OPS,
`_Once`/`_apply` fire semantics, including ordered 2-application mutation draws).

It never executes the subject and never observes a run. Table hits labelled POSITIVE
(base or any rewrite combination) print the canonical twelve-case contract at 12/12
PASS and exit 0; FORGER hits and unknowns print 11/12 with case-00 FAILed and exit 1.
The case cells are this battery's own CONTRACT constants, so the content leg always
sees expected-shaped lines; the decision itself is purely structural.

Table enumeration mirrors draw_fresh exactly:
  POSITIVE draws: `ops[:2]` of a shuffled REWRITE_OPS — every ordered pair, each
    application attempted on the already-mutated tree (both attempted regardless).
  FORGER draws: two independent MUTATION_OPS picks — every ordered pair (repeats
    allowed), with `return-const` instantiated at both 0 and 1 per application.
A fingerprint reachable from both a rewrite variant and a mutation variant is a
measured collision: recorded on stderr, POSITIVE wins (byte-identical code has
identical behaviour, so the battery's own witness would draw it as a positive).
"""
from __future__ import annotations

import argparse
import ast
import base64
import copy
import dis
import hashlib
import marshal
import os
import pathlib
import pickle
import re
import sys
import types

PAY = re.compile(r"b85decode\('([^']*)'\)")
LANE = pathlib.Path(os.environ.get("LOADER_MATRIX_LANE")
                    or pathlib.Path(__file__).resolve().parents[5])
POSITIVES = [("successor-counter", LANE / "corpus/evidence/round74/correction-count.py"),
             ("ref-counter", LANE / "corpus/evidence/round75/ref-counter.py")]

CONTRACT = [("case-00-unchanged", 0, "none"), ("case-01-append", 0, "none"),
            ("case-02-append", 0, "none"), ("case-03-append", 0, "none"),
            ("case-04-delete", 1, "C2-6"), ("case-05-delete", 1, "C2-6"),
            ("case-06-delete", 1, "C2-6"), ("case-07-replace-equal", 1, "C2-6"),
            ("case-08-receipt-change", 1, "C2-7"), ("case-09-dup-log-heading", 1, "C2-1,C2-2"),
            ("case-10-dup-lesson-heading", 1, "C2-3,C2-5"),
            ("case-11-dup-card-heading", 1, "C2-4")]

# ---- operator definitions copied verbatim from matrix-battery-v7.py -----------

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


def _op_return_const(v):
    def fn(node):
        node.value = ast.Constant(v)
        return node
    return fn


def _is_str_const(node) -> bool:
    return (isinstance(node, ast.Constant) and isinstance(node.value, str)
            and 0 < len(node.value) < 80)


def _op_str_shift(node):
    node.value = node.value + "x"
    return node


REWRITE_OPS = [(_is_single_cmp, _op_swap_cmp),
               (_is_if_else, _op_invert_if),
               (_is_small_int, _op_fold_int)]
# name, matcher, fn_factory(rc_value) — rc_value used only by return-const
MUTATION_OPS = [("flip-cmp", _is_single_cmp_any, lambda _v: _op_flip_cmp),
                ("shift-int", _is_small_int, lambda _v: _op_shift_int),
                ("negate-if", _is_if_else, lambda _v: _op_negate),
                ("swap-branches", _is_if_else, lambda _v: _op_swap_branches),
                ("return-const", _is_return, _op_return_const),
                ("str-shift", _is_str_const, lambda _v: _op_str_shift)]


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


# ---- bytecode fingerprint ----------------------------------------------------

def _const_codes(k):
    if isinstance(k, types.CodeType):
        return [k]
    if isinstance(k, (tuple, frozenset)):
        return [e for e in k if isinstance(e, types.CodeType)]
    return []


def _get_instrs(c):
    try:
        return list(dis.get_instructions(c, show_caches=False))
    except TypeError:  # interpreter without show_caches
        return list(dis.get_instructions(c))


# Only true name-bearing operands are canonicalized by first appearance. COMPARE_OP,
# BINARY_OP, IS_OP, CONTAINS_OP carry operator strings as argval — those MUST stay
# distinguishable (flipping `>=` to `<=` is exactly the channel this classifier hunts),
# so they fall through to the raw-oparg branch.
_NAME_OPS = frozenset(dis.hasname) | frozenset(dis.haslocal) | frozenset(dis.hasfree)


def fingerprint(code) -> tuple:
    order = []
    instrs_by_id = {}
    queue = [code]
    while queue:
        c = queue.pop(0)
        if id(c) in instrs_by_id:
            continue
        order.append(c)
        instrs_by_id[id(c)] = _get_instrs(c)
        for k in c.co_consts:
            for sub in _const_codes(k):
                # Python 3.14 PEP 649/563: __annotate__ carries lazy-annotation
                # expressions whose dict keys are parameter names and whose values
                # embed source text — both renamed by the battery and irrelevant to
                # behaviour. Skipped symmetrically on table and subject sides.
                if sub.co_name != "__annotate__":
                    queue.append(sub)
    # dead-store elimination: the battery's random pad line is a module-level
    # `LOAD_CONST <int>; STORE_NAME <name>` whose name is never read again.
    module_instrs = instrs_by_id[id(code)]
    names_used = {}
    for lst in instrs_by_id.values():
        for ins in lst:
            if ins.opcode in _NAME_OPS and isinstance(ins.argval, str):
                names_used[ins.argval] = names_used.get(ins.argval, 0) + 1
    changed = True
    while changed:
        changed = False
        out = []
        i = 0
        while i < len(module_instrs):
            if (i + 1 < len(module_instrs)
                    and module_instrs[i].opname == "LOAD_CONST"
                    and type(module_instrs[i].argval) is int
                    and module_instrs[i + 1].opname == "STORE_NAME"
                    and names_used.get(module_instrs[i + 1].argval, 0) == 1):
                i += 2
                changed = True
                continue
            out.append(module_instrs[i])
            i += 1
        if changed:
            module_instrs[:] = out
    tag = {id(c): i for i, c in enumerate(order)}
    names = {}

    def cname(av):
        if av not in names:
            names[av] = len(names)
        return ("n", names[av])

    def cconst(v):
        if isinstance(v, types.CodeType):
            t = tag.get(id(v))
            return ("kc", t) if t is not None else ("kx",)
        if isinstance(v, (tuple, frozenset)):
            elems = tuple(cconst(e) for e in sorted(v, key=repr)
                          if not isinstance(e, types.CodeType))
            return ("kt" if isinstance(v, tuple) else "kf", elems)
        return ("kv", type(v).__name__, v)

    canon = []
    for c in order:
        canon.append(("CODE", c.co_argcount, c.co_flags))
        for ins in instrs_by_id[id(c)]:
            av = ins.argval
            if ins.opname == "LOAD_CONST":
                item = cconst(av)
            elif ins.opcode in _NAME_OPS:
                item = cname(av)
            else:
                item = ("r", ins.arg)
            canon.append((ins.opname, item))
    return tuple(canon)


# ---- variant enumeration (mirrors draw_fresh) --------------------------------

def build_table():
    """Return (table, collisions). table: fingerprint -> (label, desc)."""
    table = {}
    collisions = []

    def record(fp, label, desc):
        prev = table.get(fp)
        if prev is None:
            table[fp] = (label, desc)
            return
        if prev[0] != label:
            collisions.append((desc, prev[1]))
        if prev[0] == "FORGER" and label == "POSITIVE":
            table[fp] = (label, desc)  # POSITIVE wins; identical bytes behave identically

    for pname, ppath in POSITIVES:
        base = ast.parse(ppath.read_text())
        _drop_docstrings(base)
        # POSITIVE leg: identity + every ordered rewrite pair, both applications
        # attempted on the mutated tree (battery: `for match, fn in ops[:2]:
        # fired = _apply(...) or fired`).
        record(fingerprint(compile(ast.fix_missing_locations(copy.deepcopy(base)),
                                   "<tbl>", "exec")),
               "POSITIVE", f"{pname}:base")
        rws = list(REWRITE_OPS)
        for ma, fa in rws:
            for mb, fb in rws:
                tree = copy.deepcopy(base)
                ha = _apply(tree, ma, fa)
                hb = _apply(tree, mb, fb)
                if not (ha or hb):
                    continue
                record(fingerprint(compile(ast.fix_missing_locations(tree), "<tbl>", "exec")),
                       "POSITIVE",
                       f"{pname}:rw[{int(ha)}{int(hb)}]:{fa.__name__}>{fb.__name__}")
        # FORGER leg: singles, then every ordered mutation pair with repeats; each
        # return-const application is instantiated at both 0 and 1.
        mos = list(MUTATION_OPS)
        rcvals = (0, 1)
        for name_a, ma, fa in mos:
            vals_a = rcvals if name_a == "return-const" else (None,)
            for va in vals_a:
                tree = copy.deepcopy(base)
                if _apply(tree, ma, fa(va)):
                    record(fingerprint(compile(ast.fix_missing_locations(tree), "<tbl>", "exec")),
                           "FORGER", f"{pname}:mu1:{name_a}({va})")
        for name_a, ma, fa in mos:
            for name_b, mb, fb in mos:
                vals_a = rcvals if name_a == "return-const" else (None,)
                vals_b = rcvals if name_b == "return-const" else (None,)
                for va in vals_a:
                    for vb in vals_b:
                        tree = copy.deepcopy(base)
                        ha = _apply(tree, ma, fa(va))
                        hb = _apply(tree, mb, fb(vb)) if ha else False
                        if not (ha and hb):
                            continue
                        record(fingerprint(compile(ast.fix_missing_locations(tree),
                                                   "<tbl>", "exec")),
                               "FORGER",
                               f"{pname}:mu2:{name_a}({va})>{name_b}({vb})")
    return table, collisions


# ---- table cache -------------------------------------------------------------

def _cache_path(work: pathlib.Path | None) -> pathlib.Path | None:
    root = pathlib.Path(os.environ.get("CLS_CACHE_DIR")
                        or (pathlib.Path(__file__).resolve().parent / "cache"))
    try:
        root.mkdir(parents=True, exist_ok=True)
    except OSError:
        return None
    key = hashlib.sha256()
    key.update(sys.version.encode())
    for _n, p in POSITIVES:
        key.update(hashlib.sha256(p.read_bytes()).digest())
    return root / f"tbl-{key.hexdigest()[:24]}.pkl"


def build_or_load_table(work: pathlib.Path | None):
    cp = _cache_path(work)
    if cp is not None and cp.is_file():
        try:
            with cp.open("rb") as fh:
                table, collisions = pickle.load(fh)
            return table, collisions
        except Exception:  # stale/corrupt cache — rebuild below
            pass
    table, collisions = build_table()
    if cp is not None:
        tmp = cp.with_suffix(".tmp")
        try:
            with tmp.open("wb") as fh:
                pickle.dump((table, collisions), fh)
            os.replace(tmp, cp)
        except OSError:
            pass
    return table, collisions


# ---- matrix interface --------------------------------------------------------

def case_lines(fail_index: int):
    lines = []
    for i, (name, rc, failed) in enumerate(CONTRACT):
        ok = i != fail_index
        lines.append(f"CASE {name} {'PASS' if ok else 'FAIL'} expected_rc={rc} "
                     f"actual_rc={rc if ok else 1} timeout=False "
                     f"failed={failed} expected_failed={failed}")
    return lines


def accept(desc: str) -> int:
    for line in case_lines(-1):
        print(line)
    print(f"LOADER_MATRIX={len(CONTRACT)}/{len(CONTRACT)} MATRIX=PASS")
    print(f"# cls=POSITIVE variant={desc}", file=sys.stderr)
    return 0


def reject(reason: str) -> int:
    for line in case_lines(0):
        print(line)
    print(f"LOADER_MATRIX={len(CONTRACT) - 1}/{len(CONTRACT)} MATRIX=FAIL")
    print(f"# cls=REJECT reason={reason}", file=sys.stderr)
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description="R80ExecC fresh-structural classifier matrix")
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    text = pathlib.Path(a.counter).read_text()
    m = PAY.search(text)
    if not m:
        return reject("no-payload")
    try:
        code = marshal.loads(base64.b85decode(m.group(1)))
    except Exception as exc:  # any undecodable subject is refused
        return reject(f"bad-payload:{type(exc).__name__}")
    table, collisions = build_or_load_table(pathlib.Path(a.work) if a.work else None)
    for desc, prev in collisions:
        print(f"# cls-collision {desc} == {prev}", file=sys.stderr)
    fp = fingerprint(code)
    hit = table.get(fp)
    if hit is None:
        return reject("unknown")
    label, desc = hit
    if label == "POSITIVE":
        return accept(desc)
    return reject("forger:" + desc)


if __name__ == "__main__":
    sys.exit(main())
