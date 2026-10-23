#!/usr/bin/env python3
# round-35 w2 RevSlenSweep: dynamic-scope sweep of local/declare/export/readonly
# statements. Static: any statement assigning N1..Nk whose later (or same-word)
# RHS references an earlier assigned name — bash expands every RHS before any
# assignment, so the reference reads the CALLER's dynamic scope.
# Empirical: poison-differential — set each statement's own assigned names to a
# sentinel in the caller scope, run the statement, declare -p the names; a
# dynamic read makes outputs differ. Positive control: base blob L1632.
# Usage: python3 slen-sweep.py GATE [--empirical]
import re, subprocess, sys

POISON = 'zzPOISONzz'

def words_of(s):
    words = []; cur = ''
    i = 0; L = len(s)
    while i < L:
        c = s[i]
        if c in ' \t':
            if cur: words.append(cur); cur = ''
            i += 1; continue
        if c == '\\':
            cur += c + (s[i+1] if i+1 < L else ''); i += 2; continue
        if c == "'":
            j = s.find("'", i+1)
            if j == -1: cur += s[i:]; break
            cur += s[i:j+1]; i = j+1; continue
        if c == '"':
            j = i+1
            while j < L:
                if s[j] == '\\': j += 2; continue
                if s[j] == '"': break
                j += 1
            cur += s[i:min(j+1, L)]; i = j+1; continue
        if s[i:i+2] == '${':
            depth = 0; j = i+1
            while j < L:
                if s[j] == '{': depth += 1
                elif s[j] == '}':
                    depth -= 1
                    if depth == 0: break
                j += 1
            cur += s[i:j+1]; i = j+1; continue
        if s[i:i+2] == '$(':
            depth = 0; j = i+1
            while j < L:
                if s[j] == '(': depth += 1
                elif s[j] == ')':
                    depth -= 1
                    if depth == 0: break
                j += 1
            cur += s[i:j+1]; i = j+1; continue
        cur += c; i += 1
    if cur: words.append(cur)
    return words

def refs_to(text, X):
    hits = []
    if re.search(r'\$\{\s*#\s*' + X + r'\s*\}', text): hits.append(f'len ${{#{X}}}')
    if re.search(r'\$\{' + X + r'([^A-Za-z0-9_]|$)', text): hits.append(f'param ${{{X}...}}')
    if re.search(r'\$' + X + r'(?![A-Za-z0-9_])', text): hits.append(f'bare ${X}')
    for m in re.finditer(r'\$\(\((.*?)\)\)', text):
        if re.search(r'(?<![A-Za-z0-9_])' + X + r'(?![A-Za-z0-9_])', m.group(1)):
            hits.append(f'arith $(({m.group(1)[:30]}))'); break
    return hits

def stmts_of(path, kws=('local',)):
    lines = open(path).read().split('\n')
    n = len(lines)
    def cont(line):
        c = 0
        for ch in reversed(line):
            if ch == '\\': c += 1
            else: break
        return c % 2 == 1
    out = []; i = 0
    while i < n:
        if re.match(rf'\s*({"|".join(kws)})(\s|$)', lines[i]):
            full = lines[i]; start = i
            while cont(full) and i + 1 < n:
                i += 1
                full = full[:-1].rstrip() + ' ' + lines[i]
            out.append((start + 1, full))
        i += 1
    return out

def static_sweep(path, kws):
    hits = []
    for lineno, full in stmts_of(path, kws):
        ws = words_of(full)
        assigned = []
        for wi, w in enumerate(ws[1:], start=1):
            if w.startswith('-'): continue
            m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\+?[=(]', w)
            if m and m.group(1) not in [a[0] for a in assigned]:
                assigned.append((m.group(1), w.split('=', 1)[1] if '=' in w else ''))
        for order, (name, val) in enumerate(assigned):
            for X in [a[0] for a in assigned[:order]]:
                if X == name: continue
                for h in refs_to(val, X):
                    hits.append(('DIFF', lineno, name, X, h, full.strip()[:160]))
            for h in refs_to(val, name):
                hits.append(('SELF', lineno, name, name, h, full.strip()[:160]))
    return hits

NONDET = re.compile(r'RANDOM|SECONDS|EPOCHREALTIME|EPOCHSECONDS|LINENO|LC_ALL|LANG=|\bdate\b')

def empirical_sweep(path):
    results = []
    for idx, (lineno, full) in enumerate(stmts_of(path, ('local',))):
        ws = words_of(full)
        names = []
        for w in ws[1:]:
            if w.startswith('-'): continue
            m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\+?[=(]', w)
            if m and m.group(1) not in names: names.append(m.group(1))
        if not names or NONDET.search(full):
            results.append((lineno, full, 'SKIP', '')); continue
        fn = f'__t{idx}'
        dps = ' '.join(f'"{x}"' for x in names)
        poison_stmt = ' '.join(f'{x}={POISON}' for x in names)
        script = f'{fn}() {{\n{full}\ndeclare -p {dps} 2>&1\n}}\n' + f'''
a=$( {{ {fn} 2>&1; }} | grep -v setlocale; printf X )
{poison_stmt}
b=$( {{ {fn} 2>&1; }} | grep -v setlocale; printf X )
unset {' '.join(names)} 2>/dev/null
if [[ $a == "$b" ]]; then echo SAME; else echo DIFFER; fi
'''
        p = subprocess.run(['bash', '-c', script], capture_output=True, text=True, timeout=60)
        out = p.stdout or ''
        v = 'DIFFER' if 'DIFFER' in out else ('SAME' if 'SAME' in out else 'ERR')
        results.append((lineno, full, v, out[:300]))
    return results

if __name__ == '__main__':
    gate = sys.argv[1]
    kws = ('local',) if '--local-only' in sys.argv else ('local', 'declare', 'export', 'readonly')
    static = static_sweep(gate, kws)
    print(f'STATIC refs in {gate}: {len(static)}')
    for kind, l, nm, X, h, ctx in static:
        print(f'  [{kind}] L{l} {nm} <- {X} ({h}) | {ctx}')
    if '--empirical' in sys.argv:
        emp = empirical_sweep(gate)
        same = sum(1 for r in emp if r[2] == 'SAME')
        dif = [r for r in emp if r[2] == 'DIFFER']
        skip = [r for r in emp if r[2] != 'SAME' and r[2] != 'DIFFER']
        print(f'EMPIRICAL: SAME={same} DIFFER={len(dif)} skip/err={len(skip)}')
        for (l, full, v, extra) in dif:
            print(f'  DIFFER L{l}: {full.strip()[:140]}')
        for (l, full, v, extra) in skip:
            print(f'  {v} L{l}: {full.strip()[:100]}')
