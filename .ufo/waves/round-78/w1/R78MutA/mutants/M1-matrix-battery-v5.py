#!/usr/bin/env python3
"""Round-78 matrix battery v5 — no invertible answer key, no strippable subject
identity, no appendable verdict receipt (QUALITY 143).

Unit under test: a MATRIX program that takes `--counter PATH --work DIR` and exits 0
iff a candidate counter satisfies every case it declares. The battery runs the matrix
against salted copies of two positives and eleven forgers (the round-76 subject set,
referenced byte-identically from `corpus/evidence/round76/forgers/`) and three forged
matrices, under the round-77 legs plus the three closures round 77 carried:

  ORDER LEG      The subject list is permuted per run with a fresh 64-bit seed
                 (`secrets.randbits`). The permutation is never printed and no digest
                 of it is printed: round 77 printed `sha256` of the permuted names and a
                 critic recovered both permutations by enumerating 13! inside the
                 battery's own cap (`R77CriticA/rcpt-a7.txt`). This battery prints no
                 order line at all.
  QUIET LEG      No per-subject line is printed while subjects are running. Every
                 `MATRIX RUN`/`SUBJECT` line is buffered and flushed after the whole
                 scoring loop has finished, so a matrix child that reads the judge's
                 stdout target through `/proc/<ppid>/fd/1` learns neither its own
                 position nor its own identity while it runs.
  CONTENT LEG    Every matrix run must print the twelve `CASE` lines of the frozen
                 contract with `expected_rc` / `expected_failed` cells equal to the
                 battery's own independently stated contract map, and a summary count
                 equal to the number of `PASS` case lines. The contract is public by
                 design; this leg is a shape requirement, not a secrecy boundary.
  IDENTITY LEG   Each subject copy carries a random *statement* inserted at a random
                 interior line (never a strippable suffix), so a hash of the copy equals
                 no committed object and stripping a trailing salt line recovers nothing
                 (`R77CriticA/rcpt-a1.txt` stripped `\\n# salt <hex>` and classified every
                 subject). See Limits for what this does not close.
  RECEIPT LEG    The verdict is bound to the process exit code and to a line-count
                 trailer: the battery prints `RECEIPT_LINES=<n>` immediately before its
                 predicate line, where n is the total number of lines it wrote. A child
                 that appends a forged predicate line after the battery exits changes the
                 receipt's line count, so `forge-battery.py` detects the append instead
                 of reading it as a verdict (`R77CriticA/rcpt-a5d.txt` appended 26 copies
                 of the exact predicate line after exit 1).

Predicate (same sentence as `corpus/evidence/round78/claims.md`):

  `python3 -B corpus/evidence/round78/matrix-battery-v5.py --matrix MATRIX --work DIR`
  exits 0 and prints exactly
  `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`.

A forger is REJECTED only when both runs exit 1 with fewer than full marks; a positive
is ACCEPTED only when both runs exit 0 with full marks, `MATRIX=PASS`, and a valid
contract table. An exit of 2 is never scored in the matrix's favour.

Closure-removal twins (mutation evidence, never the predicate): `--no-permute` runs the
fixed round-76 subject order and `--no-content` drops the contract-table requirement.
`--print-order` re-enables the round-77 `ORDER <i> <digest>` line for comparison.

Limits (recorded, not closed): the battery proves these thirteen subjects plus three
forged matrices at these salts and these permutations. It does not prove
arbitrary-forgery freedom. The identity leg closes the trailing-suffix strip class; a
normalizer that deletes every inert statement it does not recognise can still recover a
subject's source, and a matrix that reads subject content semantically is correct for
these inputs. Line-count detection closes append; a forger that truncates the receipt is
not detected by it (the caller's exit code remains authoritative).

Usage: python3 corpus/evidence/round78/matrix-battery-v5.py --matrix PATH --work DIR
       [--runs N] [--matrix-timeout S] [--no-permute] [--no-content] [--print-order]
Exit: 0 BATTERY=PASS · 1 BATTERY=FAIL · 2 usage/env.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
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


def salted_copy(source: pathlib.Path, work: pathlib.Path) -> pathlib.Path:
    """Copy a subject with a random inert *statement* at a random interior line.

    QUALITY 143: the round-77 salt was an appended suffix line, so `data.rfind(b"\\n# salt ")`
    recovered the source byte-for-byte. Here the inserted bytes are a statement at an
    interior position and their shape varies per copy, so no trailing-line strip and no
    single fixed-marker strip recovers a committed object.
    """
    d = work / secrets.token_hex(8)
    d.mkdir(parents=True)
    target = d / "subject.py"
    text = source.read_text()
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    name = "_r78" + secrets.token_hex(6)
    if secrets.randbits(1):
        inserted = f"import os as {name}\n"
    else:
        inserted = f"{name} = {secrets.randbelow(10 ** 6)}\n"
    # Insert before a random *top-level* statement, never inside an indented block or a
    # multi-line literal: an inert statement at a module statement boundary cannot change
    # the subject's behaviour or its syntax.
    anchors = []
    try:
        body = ast.parse(text).body
        futures = [n.lineno for n in body
                   if isinstance(n, ast.ImportFrom) and n.module == "__future__"]
        floor = max(futures) if futures else 0
        anchors = [n.lineno for n in body
                   if n.lineno > floor
                   and not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant)
                            and isinstance(n.value.value, str))]
    except SyntaxError:
        anchors = []
    pos = anchors[secrets.randbelow(len(anchors))] - 1 if anchors else len(lines)
    lines.insert(pos, inserted)
    target.write_text("".join(lines))
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
            subject = salted_copy(source, work)
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
    ap.add_argument("--matrix", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--runs", type=int, default=2)
    ap.add_argument("--matrix-timeout", type=int, default=300)
    ap.add_argument("--no-permute", action="store_true")
    ap.add_argument("--no-content", action="store_true")
    ap.add_argument("--print-order", action="store_true",
                    help="re-enable the round-77 ORDER digest line (comparison only)")
    a = ap.parse_args()
    a.print_order = True
    matrix = pathlib.Path(a.matrix).resolve()
    work = pathlib.Path(a.work).resolve()
    if not matrix.is_file():
        print(f"matrix-battery-v5: missing matrix {matrix}", file=sys.stderr)
        return 2
    if a.runs < 1 or a.matrix_timeout < 1:
        print("matrix-battery-v5: --runs and --matrix-timeout must be >= 1", file=sys.stderr)
        return 2
    permute = not a.no_permute
    content = not a.no_content
    try:
        work.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"matrix-battery-v5: cannot create --work {work}: {exc}", file=sys.stderr)
        return 2
    if not work.is_dir():
        print(f"matrix-battery-v5: --work {work} is not a directory", file=sys.stderr)
        return 2
    run = work / ("r78-" + secrets.token_hex(8))
    try:
        run.mkdir()
    except OSError as exc:
        print(f"matrix-battery-v5: cannot create {run}: {exc}", file=sys.stderr)
        return 2
    emit("MATRIX_PATH=" + str(matrix))
    emit("MATRIX_SHA256=" + hashlib.sha256(matrix.read_bytes()).hexdigest())
    emit(f"RUNS={a.runs} CHILD_TIMEOUT={CHILD_TIMEOUT} MATRIX_TIMEOUT={a.matrix_timeout} "
         f"PERMUTE={permute} CONTENT={content}")
    subjects = ([("POSITIVE", n, p) for n, p in POSITIVES]
                + [("FORGER", n, p) for n, p in FORGERS])
    for _group, _name, source in subjects:
        if not pathlib.Path(source).resolve().is_file():
            print(f"matrix-battery-v5: missing subject {source}", file=sys.stderr)
            return 2
    try:
        p_ok, p_all, f_ok, f_all = score(matrix, subjects, a.runs, run, a.matrix_timeout,
                                         permute, content, "MATRIX", a.print_order)
        oracle_ok = 0
        for name, source in ORACLES:
            if not source.is_file():
                print(f"matrix-battery-v5: missing oracle {source}", file=sys.stderr)
                return 2
            copy = salted_copy(source, run)
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
    emit(f"RECEIPT_LINES={_LINES + 2}")
    emit(f"BATTERY={'PASS' if verdict else 'FAIL'} forgers_rejected={f_ok}/{f_all} "
         f"positive={p_ok}/{p_all} oracle={'REJECTED' if oracle_ok == len(ORACLES) else 'MISS'}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
