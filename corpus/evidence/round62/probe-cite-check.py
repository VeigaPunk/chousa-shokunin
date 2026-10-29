#!/usr/bin/env python3
"""probe-cite-check — QUALITY 124. Every `probe(ID, label, observed, expected)` call of a probe script carries a
`# cite ID: S138 "<quote>"` / `# cite ID: S139 "<quote>"` comment whose quote (4+ words) occurs in the whitespace-normalised
rendered page (S138, MANWIDTH=1000 man -l /usr/share/man/man2/openat2.2.gz | col -bx) or header (S139) and, when the expected
value is an errno name, contains it, or `# cite ID: INFERENCE ...`. Usage: python3 -B probe-cite-check.py PROBE.py;
prints `CITES=<k>/<n> SOURCED=<s> INFERENCE=<i>` and `CITE=PASS|FAIL`; exit 0 only when every probe is cited.
"""
import ast, os, re, subprocess, sys, pathlib
def norm(s): return re.sub(r"\s+", " ", s).strip()
man = subprocess.run(["col", "-bx"], input=subprocess.run(["man", "-l", "/usr/share/man/man2/openat2.2.gz"], capture_output=True, env=dict(os.environ, MANWIDTH="1000", LC_ALL="C.UTF-8")).stdout, capture_output=True).stdout
SRC = {"S138": norm(man.decode("utf-8", "replace")), "S139": norm(pathlib.Path("/usr/include/linux/openat2.h").read_text(errors="replace"))}
text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
exp = {}
for n in ast.walk(ast.parse(text)):
    if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "probe" and len(n.args) == 4 and isinstance(n.args[0], ast.Constant):
        exp[n.args[0].value] = n.args[3].value if isinstance(n.args[3], ast.Constant) else None
cites = {}
for l in text.splitlines():
    m = re.match(r"^\s*#\s*cite\s+(P\d+):\s*(.+?)\s*$", l)
    if m: cites.setdefault(m.group(1), []).append(m.group(2))
res = sure = inf = 0
for pid in sorted(exp):
    e, got = exp[pid], None
    for c in cites.get(pid, []):
        if c.startswith("INFERENCE"): got = "i"; break
        m = re.match(r'^(S138|S139) "(.+)"$', c)
        if not m: print(f"  {pid} cite refused: {c[:60]}"); continue
        q = norm(m.group(2))
        if len(q.split()) < 4 or q not in SRC[m.group(1)]: print(f"  {pid} quote not in {m.group(1)}: {q[:60]}"); continue
        if isinstance(e, str) and re.fullmatch(r"E[A-Z0-9]+", e) and e not in q: print(f"  {pid} quote lacks {e}"); continue
        got = "s"; break
    if got is None: print(f"  {pid} expected={e!r} uncited"); continue
    res += 1; sure += got == "s"; inf += got == "i"
print(f"CITES={res}/{len(exp)} SOURCED={sure} INFERENCE={inf}")
ok = bool(exp) and res == len(exp)
print(f"CITE={'PASS' if ok else 'FAIL'}"); sys.exit(0 if ok else 1)
