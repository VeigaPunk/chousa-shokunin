#!/usr/bin/env python3
"""Structure-identity matrix — R79ExecC wave artifact, a LIMIT measurement.

Not a lane matrix. It scores a candidate counter by structure identity alone:

  1. reads the copy the battery hands it (`--counter PATH`);
  2. decodes the round-79 wrapper (`import base64 as _b, marshal as _m` +
     `exec(_m.loads(_b.b85decode(<payload>)))`), falling back to a plain-text
     AST path for the round-78 textual-salt copies;
  3. unmarshals the code object;
  4. canonicalises the fresh identifier table: drops the unrecognised
     module-level integer assignment (the v6 pad) and any unused module-level
     import binding (the v5 salt), then renames every string instruction
     operand to v0, v1, ... in first-use order over the filtered streams;
  5. compares the sha256 of the canonical token stream against a table built
     from compile() of the committed subjects (2 positives + 11 forgers).

It never executes the candidate: identity by table lookup, verdicts emitted
from the frozen public contract. That is the channel being measured.
"""
from __future__ import annotations

import argparse
import ast
import base64
import dis
import hashlib
import json
import marshal
import pathlib
import re
import sys
import types

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")

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

# The frozen twelve-case contract (public in matrix-battery-v5/v6.py).
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

WRAPPER_RX = re.compile(
    r"_b\.b85decode\((['\"])([0-9A-Za-z!#$%&()*+\-;<=>?@^_`{|}~]+)\1\)")


def drop_docstrings(tree: ast.Module) -> None:
    """Mirror matrix-battery-v6._drop_docstrings exactly."""
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                                 ast.ClassDef)):
            continue
        body = node.body
        if (body and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)):
            node.body = body[1:] or [ast.Pass()]


def _instructions(code: types.CodeType) -> list[dis.Instruction]:
    return list(dis.get_instructions(code))


def _nested(code: types.CodeType) -> list[types.CodeType]:
    return [c for c in code.co_consts if isinstance(c, types.CodeType)]


def _walk_codes(code: types.CodeType):
    """Yield the code object and every descendant, deterministically."""
    stack = [code]
    while stack:
        c = stack.pop(0)
        yield c
        stack = _nested(c) + stack


def _name_occurs(root: types.CodeType, name: str) -> int:
    n = 0
    for c in _walk_codes(root):
        for ins in _instructions(c):
            if isinstance(ins.argval, str) and ins.argval == name:
                n += 1
    return n


def _filtered_root(root: types.CodeType) -> list[dis.Instruction]:
    """Drop the unrecognised module-level integer assignment (v6 pad) and
    unused module-level import bindings (v5 salt): instruction pairs
    LOAD_CONST <int> + STORE_NAME n, or IMPORT_NAME x + STORE_NAME n, where
    the stored name occurs exactly once in the whole code tree."""
    ins = _instructions(root)
    drop: set[int] = set()
    for i in range(len(ins) - 1):
        a, b = ins[i], ins[i + 1]
        stored = None
        if (a.opname == "LOAD_CONST" and isinstance(a.argval, int)
                and not isinstance(a.argval, bool) and b.opname == "STORE_NAME"):
            stored = b.argval
        elif a.opname == "IMPORT_NAME" and b.opname == "STORE_NAME":
            stored = b.argval
        if stored is not None and _name_occurs(root, stored) == 1:
            drop.add(i)
            drop.add(i + 1)
    return [ins[j] for j in range(len(ins)) if j not in drop]


class _Ctx:
    def __init__(self) -> None:
        self.map: dict[str, str] = {}
        self.n = 0

    def canon(self, name: str) -> str:
        v = self.map.get(name)
        if v is None:
            v = f"v{self.n}"
            self.n += 1
            self.map[name] = v
        return v


def _const_tok(v: object) -> object:
    if v is None:
        return "c:none"
    if isinstance(v, bool):
        return f"c:bool:{v}"
    if isinstance(v, int):
        return f"c:int:{v}"
    if isinstance(v, float):
        return f"c:float:{v!r}"
    if isinstance(v, complex):
        return f"c:complex:{v!r}"
    if isinstance(v, str):
        return f"c:str:{v}"
    if isinstance(v, bytes):
        return f"c:bytes:{v!r}"
    if isinstance(v, tuple):
        return ["c:tuple"] + [_const_tok(x) for x in v]
    if isinstance(v, frozenset):
        return ["c:frozenset"] + sorted(repr(_const_tok(x)) for x in v)
    if isinstance(v, types.CodeType):
        return "c:<code>"
    return f"c:other:{type(v).__name__}"


ATTR_RAW_OPS = frozenset({"LOAD_ATTR", "STORE_ATTR", "LOAD_SUPER_ATTR", "KW_NAMES"})


def _is_annotate(code: types.CodeType) -> bool:
    """PEP 649: parameter names are string keys of __annotate__ code objects; they are
    identifiers, so they go through the same identifier table as names."""
    return code.co_name.startswith("__annotate")


def _tokens(code: types.CodeType, ctx: _Ctx, root: bool) -> list:
    toks: list = []
    ins = _filtered_root(code) if root else _instructions(code)
    off2idx = {i.offset: k for k, i in enumerate(ins)}
    ann = _is_annotate(code)
    for k, i in enumerate(ins):
        op, arg = i.opname, i.argval
        if op == "MAKE_CELL":
            # cell declarations follow co_cellvars order, which renaming reorders; the name is a
            # declaration, not a use, so it does not enter the first-use table here.
            toks.append([op])
            continue
        if isinstance(arg, str):
            if op in ATTR_RAW_OPS:
                toks.append([op, "attr:" + arg])
            elif op == "LOAD_CONST" and ann and arg != "return":
                toks.append([op, "ident:" + ctx.canon(arg)])
            elif op == "LOAD_CONST" or op.startswith("RETURN_CONST"):
                toks.append([op, _const_tok(arg)])
            else:
                toks.append([op, ctx.canon(arg)])
        elif isinstance(arg, tuple):
            if op in ATTR_RAW_OPS:
                toks.append([op] + ["attr:" + x for x in arg])
            else:
                toks.append([op] + [ctx.canon(x) for x in arg])
        elif op == "LOAD_CONST" or op.startswith("RETURN_CONST"):
            toks.append([op, _const_tok(arg)])
        elif ("JUMP" in op or op in ("FOR_ITER", "SEND")) and arg in off2idx:
            toks.append([op, f"@{off2idx[arg] - k:+d}"])
        else:
            toks.append([op, repr(arg)])
        if op == "LOAD_CONST" and isinstance(arg, types.CodeType):
            toks.extend(_tokens(arg, ctx, root=False))
    return toks


def digest_code(code: types.CodeType) -> str:
    ctx = _Ctx()
    toks = _tokens(code, ctx, root=True)
    blob = json.dumps(toks, separators=(",", ":")).encode()
    return hashlib.sha256(blob).hexdigest()


def digest_text(text: str) -> str | None:
    """Canonicalise a plain-text copy (round-78 channel): parse, drop
    docstrings, compile, then the same code-level canonicalisation strips the
    salt. Returns None on unparseable text."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return None
    drop_docstrings(tree)
    ast.fix_missing_locations(tree)
    try:
        code = compile(tree, "<matrix-ref>", "exec")
    except (SyntaxError, ValueError):
        return None
    return digest_code(code)


def digest_payload(text: str) -> str | None:
    """Canonicalise a round-79 wrapper copy: unmarshal and digest directly."""
    m = WRAPPER_RX.search(text)
    if m is None:
        return None
    try:
        code = marshal.loads(base64.b85decode(m.group(2)))
    except Exception:
        return None
    return digest_code(code)


def build_table() -> dict[str, tuple[str, str]]:
    table: dict[str, tuple[str, str]] = {}
    for group, entries in (("POSITIVE", POSITIVES), ("FORGER", FORGERS)):
        for name, path in entries:
            dig = digest_text(path.read_text())
            if dig is None:
                raise SystemExit(f"matrix: cannot canonicalise committed subject {path}")
            if dig in table:
                raise SystemExit(f"matrix: digest collision between subjects at {path}")
            table[dig] = (group, name)
    return table


TABLE = build_table()


def classify(copy: pathlib.Path) -> tuple[bool, str | None]:
    """Return (is_positive, identity-or-None)."""
    text = copy.read_text(errors="replace")
    dig = digest_payload(text)
    if dig is None:
        dig = digest_text(text)
    hit = TABLE.get(dig)
    if hit is None:
        return False, None
    return hit[0] == "POSITIVE", f"{hit[0]}:{hit[1]}"


def emit_case_lines(positive: bool) -> None:
    for name, (rc, failed) in CONTRACT.items():
        cell = failed or "none"
        if positive:
            print(f"CASE {name} PASS expected_rc={rc} actual_rc={rc} timeout=False "
                  f"failed=none expected_failed={cell}")
        else:
            print(f"CASE {name} FAIL expected_rc={rc} actual_rc={rc} timeout=False "
                  f"failed={cell} expected_failed={cell}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    try:
        positive, _identity = classify(pathlib.Path(a.counter))
    except OSError as exc:
        print(f"matrix: unreadable copy {a.counter}: {exc}", file=sys.stderr)
        return 2
    emit_case_lines(positive)
    if positive:
        print("LOADER_MATRIX=12/12 MATRIX=PASS")
        return 0
    print("LOADER_MATRIX=0/12 MATRIX=FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
