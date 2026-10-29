#!/usr/bin/env python3
"""lane-preflight — one command that runs the chousa lane's committed self-checks and says which failed.

    python3 lane-preflight.py [--root DIR] [--fleet DIR] [--work DIR] [--skip G08[,G..]] [--only G01[,G..]]

Output, one line per gate that was selected:  `GATE <id> <name> PASS|FAIL|ENV <detail>`  (skipped gates:
`GATE <id> <name> SKIP`), then one summary line

    PREFLIGHT=<passed>/<run> FAILED=<ids|none> ENV=<ids|none> SKIPPED=<ids|none>

Exit codes: 0 every gate that ran passed · 1 at least one gate FAILED · 2 usage, or no gate failed but one could
not run (ENV: the census script of the fleet is absent) — a gate that could not run is never counted as a pass.

Gates (the ids are the interface; each reads only files under --root and runs only committed tools):
  G01 census           the fleet's sources-census.sh `validate --file ROOT/corpus/SOURCES.md` exits 0. The script is
                       taken from --fleet DIR/scripts, else $SHOKUNIN_ROOT/scripts, else ROOT/../scripts; none → ENV.
  G02 knowledge-index  every corpus/knowledge/*.md file name occurs in corpus/README.md (an index row is a claim).
  G03 lesson-gate      every corpus/lessons/round-<N>.md has a heading line beginning `## Gate`.
  G04 shonen-pointers  every path-shaped word inside a backtick span of SHONEN.md exists under ROOT.
  G05 scorecard-paths  every corpus/ tools/ .ufo/ path in the evidence cell of a SCORECARD.md `## Capabilities`
                       table row exists under ROOT.
  G06 freeze-selftest  `python3 -B tools/freeze-check.py --selftest` exits 0.
  G07 assimilate-selftest  `python3 -B tools/assimilate-rows.py --selftest` exits 0 and prints `SELFTEST=PASS`.
  G08 gate-selftest    `bash tools/research-gate.sh --selftest` exits 0 and prints `RESEARCH_GATE_SELFTEST: PASS`.

No network, no write outside --work (default: a fresh directory under $HYAKU_SCRATCH, else $TMPDIR, removed on exit).
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

GATES = [("G01", "census"), ("G02", "knowledge-index"), ("G03", "lesson-gate"), ("G04", "shonen-pointers"),
         ("G05", "scorecard-paths"), ("G06", "freeze-selftest"), ("G07", "assimilate-selftest"),
         ("G08", "gate-selftest")]
IDS = [g for g, _ in GATES]
PATHWORD = re.compile(r"(/|\.(md|log|py|sh|json|txt|tsv|jsonl)$)")


def read(p: pathlib.Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def census_script(fleet: str | None, root: pathlib.Path) -> pathlib.Path | None:
    cands = []
    if fleet:
        cands.append(pathlib.Path(fleet) / "scripts" / "sources-census.sh")
    elif os.environ.get("SHOKUNIN_ROOT"):
        cands.append(pathlib.Path(os.environ["SHOKUNIN_ROOT"]) / "scripts" / "sources-census.sh")
    else:
        cands.append(root.resolve().parent / "scripts" / "sources-census.sh")
    return next((c for c in cands if c.is_file()), None)


def run(cmd, root, env, timeout):
    try:
        p = subprocess.run(cmd, cwd=root, env=env, capture_output=True, text=True, timeout=timeout,
                           stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return None, f"timeout after {timeout}s"
    except OSError as e:
        return None, f"cannot run: {e}"
    return p, ""


def g01(root, a, env, work):
    sc = census_script(a.fleet, root)
    if sc is None:
        return "ENV", "no sources-census.sh (pass --fleet DIR, or set SHOKUNIN_ROOT, or run inside a fleet layout)"
    reg = root / "corpus" / "SOURCES.md"
    if not reg.is_file():
        return "FAIL", "corpus/SOURCES.md absent"
    p, err = run(["bash", str(sc), "validate", "--file", str(reg)], root, env, 300)
    if p is None:
        return "FAIL", err
    errs = [l for l in p.stdout.splitlines() if "\tE" in l]
    return ("PASS", f"exit=0 census_findings=0") if p.returncode == 0 else ("FAIL", f"exit={p.returncode} " + (errs[0] if errs else p.stderr.strip()[:80]))


def g02(root, a, env, work):
    kd, rd = root / "corpus" / "knowledge", root.parent / "corpus" / "README.md"
    if not rd.is_file():
        return "FAIL", "corpus/README.md absent"
    readme = read(rd)
    files = sorted(f.name for f in kd.glob("*.md")) if kd.is_dir() else []
    miss = [f for f in files if f not in readme]
    return ("PASS", f"{len(files)} entries indexed") if not miss else ("FAIL", f"{len(miss)} not named in corpus/README.md: " + ",".join(miss[:3]))


def g03(root, a, env, work):
    ld = root / "corpus" / "lessons"
    files = sorted(f for f in ld.glob("round-*.md") if re.fullmatch(r"round-\d+\.md", f.name)) if ld.is_dir() else []
    bad = [f.name for f in files if not re.search(r"^## Gate\b", read(f), re.M)]
    return ("PASS", f"{len(files)} lessons carry ## Gate") if not bad else ("FAIL", f"{len(bad)} without ## Gate: " + ",".join(bad[:3]))


def path_words(span: str):
    for w in span.split():
        w = w.lstrip("(").rstrip(";,.)")
        if not w or w[0] in "<-$" or "*" in w or w.startswith(("http:", "https:")) or "<" in w:
            continue
        w = re.sub(r":\d+(-\d+)?$", "", w)
        if PATHWORD.search(w):
            yield w


def g04(root, a, env, work):
    f = root / "SHONEN.md"
    if not f.is_file():
        return "FAIL", "SHONEN.md absent"
    words = [w for m in re.finditer(r"`([^`\n]+)`", read(f)) for w in path_words(m.group(1))]
    miss = [w for w in words if not (root / w).exists()]
    return ("PASS", f"{len(words)} pointers resolve") if not miss else ("FAIL", f"{len(miss)} unresolved: " + ",".join(miss[:3]))


def g05(root, a, env, work):
    f = root / "SCORECARD.md"
    if not f.is_file():
        return "FAIL", "SCORECARD.md absent"
    on, words = False, []
    for line in read(f).splitlines():
        if line.startswith("## "):
            on = line.startswith("## Capabilities")
            continue
        if on and line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 4 and cells[0] not in ("Capability", "Name") and not set(cells[0]) <= set("-: "):
                for m in re.finditer(r"`([^`\n]+)`", cells[2]):
                    for tok in m.group(1).split():
                        tok = tok.strip(";,")
                        if re.match(r"^(corpus|tools|\.ufo)/[^\s*<>]+$", tok):
                            words.append(tok)
    miss = [w for w in words if not (root / w).exists()]
    return ("PASS", f"{len(words)} capability pointers resolve") if not miss else ("FAIL", f"{len(miss)} unresolved: " + ",".join(miss[:3]))


def selftest(cmd, root, env, token, timeout, tool):
    if not (root / tool).is_file():
        return "FAIL", f"{tool} absent"
    p, err = run(cmd, root, env, timeout)
    if p is None:
        return "FAIL", err
    if p.returncode != 0:
        return "FAIL", f"exit={p.returncode}"
    if token and token not in p.stdout:
        return "FAIL", f"exit=0 but no `{token}` line"
    return "PASS", "exit=0"


def g06(root, a, env, work):
    return selftest([sys.executable, "-B", "tools/freeze-check.py", "--selftest", "--lane-root", str(root),
                     "--work", str(work / "g06")], root, env, "FREEZE_CHECK=", 300, "tools/freeze-check.py")


def g07(root, a, env, work):
    return selftest([sys.executable, "-B", "tools/assimilate-rows.py", "--selftest"], root, env, "SELFTEST=PASS", 300,
                    "tools/assimilate-rows.py")


def g08(root, a, env, work):
    return selftest(["bash", "tools/research-gate.sh", "--selftest"], root, env, "RESEARCH_GATE_SELFTEST: PASS", 1500,
                    "tools/research-gate.sh")


FUNCS = {"G01": g01, "G02": g02, "G03": g03, "G04": g04, "G05": g05, "G06": g06, "G07": g07, "G08": g08}


def idlist(s: str | None, flag: str) -> list[str]:
    out = [x for x in (s or "").replace(" ", "").split(",") if x]
    bad = [x for x in out if x not in IDS]
    if bad:
        print(f"lane-preflight: unknown gate id for {flag}: {','.join(bad)}", file=sys.stderr)
        raise SystemExit(2)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--fleet", default=None)
    ap.add_argument("--work", default=None)
    ap.add_argument("--skip", default=None)
    ap.add_argument("--only", default=None)
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    if not root.is_dir():
        print(f"lane-preflight: --root {a.root} is not a directory", file=sys.stderr)
        return 2
    skip, only = idlist(a.skip, "--skip"), idlist(a.only, "--only")
    base = os.environ.get("HYAKU_SCRATCH") or os.environ.get("TMPDIR") or tempfile.gettempdir()
    own = a.work is None
    work = pathlib.Path(tempfile.mkdtemp(prefix="lane-preflight-", dir=base)) if own else pathlib.Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TMPDIR=str(work), LC_ALL="C.UTF-8", PYTHONDONTWRITEBYTECODE="1")
    res = {}
    try:
        for gid, name in GATES:
            if (only and gid not in only) or gid in skip:
                print(f"GATE {gid} {name} SKIP")
                res[gid] = "SKIP"
                continue
            try:
                st, detail = FUNCS[gid](root, a, env, work)
            except Exception as e:  # a crashing gate is a failing gate, never a pass
                st, detail = "FAIL", f"gate crashed: {type(e).__name__}: {e}"
            res[gid] = st
            print(f"GATE {gid} {name} {st} {detail}")
    finally:
        if own:
            shutil.rmtree(work, ignore_errors=True)
    ran = [g for g in IDS if res[g] != "SKIP"]
    failed = [g for g in ran if res[g] == "FAIL"]
    envs = [g for g in ran if res[g] == "ENV"]
    skipped = [g for g in IDS if res[g] == "SKIP"]
    j = lambda x: ",".join(x) or "none"
    print(f"PREFLIGHT={sum(res[g] == 'PASS' for g in ran)}/{len(ran)} FAILED={j(failed)} ENV={j(envs)} SKIPPED={j(skipped)}")
    return 1 if failed else (2 if envs else 0)


if __name__ == "__main__":
    sys.exit(main())
