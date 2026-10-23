#!/usr/bin/env python3
"""Find `local` statements in a shell file where one declared variable's
initializer references a SIBLING declared in the same statement.

bash expands every right-hand side of a `local` command before it performs any
of the assignments, so such a reference resolves to the CALLER's dynamically
visible variable, not to the sibling being declared in that same statement.

usage: scope-scan.py FILE...
"""
import re
import sys

DECL = re.compile(r'(?<![A-Za-z0-9_$])([A-Za-z_][A-Za-z0-9_]*)=')
REF = re.compile(r'\$\{#?([A-Za-z_][A-Za-z0-9_]*)')


def logical_lines(path):
    """Yield (lineno, statement_text) for each `local ...` logical statement."""
    with open(path, encoding='utf-8', errors='replace') as fh:
        pending = None
        start = 0
        for lineno, raw in enumerate(fh, 1):
            stripped = raw.strip()
            if pending is None:
                if not (stripped.startswith('local ') or stripped == 'local'):
                    continue
                start = lineno
                pending = stripped
            else:
                pending += ' ' + stripped
            if pending.endswith('\\'):
                pending = pending[:-1]
                continue
            yield start, pending
            pending = None
        if pending is not None:
            yield start, pending


def scan(path):
    hits = []
    for lineno, stmt in logical_lines(path):
        body = stmt[len('local'):].strip()
        if not body:
            continue
        decls = list(DECL.finditer(body))
        if len(decls) < 2:
            continue
        names = [d.group(1) for d in decls]
        for i, d in enumerate(decls):
            nm = d.group(1)
            end = decls[i + 1].start() if i + 1 < len(decls) else len(body)
            rhs = body[d.end():end]
            for j, sib in enumerate(names):
                if j == i:
                    continue
                for m in REF.finditer(rhs):
                    if m.group(1) == sib:
                        hits.append((lineno, nm, sib, stmt))
    return hits


def main():
    rc = 0
    for path in sys.argv[1:]:
        hits = scan(path)
        print(f'== {path}')
        if not hits:
            print('   (no same-statement sibling reference found)')
        for lineno, nm, sib, stmt in hits:
            print(f'   line {lineno}: local var "{nm}" reads sibling "{sib}" '
                  f'in the SAME local statement')
            print(f'      {stmt}')
        if hits:
            rc = 1
    return rc


if __name__ == '__main__':
    sys.exit(main())
