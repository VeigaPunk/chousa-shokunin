#!/usr/bin/env python3
"""probe-cite-check (generalised from round 62's hardcoded S138/S139 version). Every `probe(ID, label, observed, expected)`
call of a probe script must carry a `# cite ID: S<id> "<quote>"` comment whose quote (4+ words) occurs in the
whitespace-normalised rendered source registered for S<id> with `--source`, or a `# cite ID: INFERENCE <reason>` comment.
Sources: `--source S142=man:/usr/share/man/man1/git-rev-parse.1.gz` (rendered `MANWIDTH=1000 man -l FILE | col -bx`,
LC_ALL=C.UTF-8) and `--source S139=file:/usr/include/linux/openat2.h` (the plain file text); repeatable.
Usage: python3 -B probe-cite-check.py --source S142=man:PAGE [--source S143=file:PATH ...] PROBE.py
Prints one line per refused cite or uncited probe, then `CITES=<k>/<n> SOURCED=<s> INFERENCE=<i>` and `CITE=PASS|FAIL`.
Exit 0 only when at least one probe call exists and every probe call is cited; 1 on FAIL; 2 on a usage or source error
(bad --source spec, unreadable source, `man`/`col` missing, probe file unreadable or not Python).
A cite whose source id was not registered is refused (the probe stays uncited unless another cite of it passes).
A cite comment naming an ID with no probe call is listed as `orphan cite` and does not change the verdict.
"""
import argparse, ast, os, pathlib, re, subprocess, sys


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def render_man(path):
    env = dict(os.environ, MANWIDTH="1000", LC_ALL="C.UTF-8")
    try:
        m = subprocess.run(["man", "-l", path], capture_output=True, env=env, timeout=60)
        c = subprocess.run(["col", "-bx"], input=m.stdout, capture_output=True, timeout=60)
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"probe-cite-check: man or col unavailable ({e})", file=sys.stderr)
        sys.exit(2)
    if m.returncode != 0 or not c.stdout.strip():
        print(f"probe-cite-check: man -l {path} rendered nothing (exit {m.returncode})", file=sys.stderr)
        sys.exit(2)
    return c.stdout.decode("utf-8", "replace")


def load_source(spec):
    m = re.fullmatch(r"(S\d+)=(man|file):(.+)", spec)
    if not m:
        print(f"probe-cite-check: bad --source {spec!r} (want S<id>=man:PATH or S<id>=file:PATH)", file=sys.stderr)
        sys.exit(2)
    sid, kind, path = m.groups()
    try:
        text = render_man(path) if kind == "man" else pathlib.Path(path).read_text(errors="replace")
    except OSError as e:
        print(f"probe-cite-check: cannot read {path}: {e}", file=sys.stderr)
        sys.exit(2)
    return sid, norm(text)


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--source", action="append", default=[], metavar="S<id>=man:PATH|file:PATH")
    ap.add_argument("probe")
    a = ap.parse_args()
    src = {}
    for spec in a.source:
        sid, text = load_source(spec)
        if sid in src:
            print(f"probe-cite-check: --source {sid} given twice", file=sys.stderr)
            return 2
        src[sid] = text
    if not src:
        print("probe-cite-check: at least one --source is required", file=sys.stderr)
        return 2
    try:
        text = pathlib.Path(a.probe).read_text(encoding="utf-8")
        tree = ast.parse(text)
    except (OSError, SyntaxError, UnicodeDecodeError) as e:
        print(f"probe-cite-check: cannot parse {a.probe}: {e}", file=sys.stderr)
        return 2
    ids = []
    for n in ast.walk(tree):
        if (isinstance(n, ast.Call) and getattr(n.func, "id", None) == "probe" and len(n.args) == 4
                and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str)):
            ids.append(n.args[0].value)
    ids = sorted(set(ids))
    cites = {}
    for l in text.splitlines():
        m = re.match(r"^\s*#\s*cite\s+(P\d+):\s*(.+?)\s*$", l)
        if m:
            cites.setdefault(m.group(1), []).append(m.group(2))
    res = sure = inf = 0
    for pid in ids:
        got = None
        for c in cites.get(pid, []):
            if c.startswith("INFERENCE"):
                got = "i"
                break
            m = re.match(r'^(S\d+) "(.+)"$', c)
            if not m:
                print(f"  {pid} cite refused: {c[:60]}")
                continue
            if m.group(1) not in src:
                print(f"  {pid} cite names unregistered source {m.group(1)}")
                continue
            q = norm(m.group(2))
            if len(q.split()) < 4:
                print(f"  {pid} quote under 4 words: {q[:60]}")
                continue
            if q not in src[m.group(1)]:
                print(f"  {pid} quote not in {m.group(1)}: {q[:60]}")
                continue
            got = "s"
            break
        if got is None:
            print(f"  {pid} uncited")
            continue
        res += 1
        sure += got == "s"
        inf += got == "i"
    for pid in sorted(set(cites) - set(ids)):
        print(f"  orphan cite {pid}: no probe call")
    print(f"CITES={res}/{len(ids)} SOURCED={sure} INFERENCE={inf}")
    ok = bool(ids) and res == len(ids)
    print(f"CITE={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
