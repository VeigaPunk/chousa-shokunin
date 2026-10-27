#!/usr/bin/env python3
"""R56-C1 frozen counter — clause coverage and hook closure of the build-spans gate.

Predicate R56-C1, the same sentence as corpus/evidence/round56/claims.md:
run on gate G (default `corpus/evidence/round56/c1-gate.py`) and battery B
(default `corpus/evidence/round56/battery/`) at seeds 7 and 56 with
`--per-leg 2`, (i) G passes the lane's `tools/build-spans.py` with all four
legs PASS and exit 0 at both seeds (CANDIDATE=2/2); (ii) each of the nine
frozen mutants M1-M9 of G (the nine edits `R55MutC1Counter` applied to the
round-55 counter: NO_SLICE, NO_CHAR, NO_SHA, NO_QUOTE, NO_EXTRA, REF_TSV,
ALLOW_ROOT, NO_ORACLE_SHA, WIN_NL) is KILLED — some single battery entry,
at EACH seed, fails a leg of G with the reason the mutated clause returns
(M8: G's `ENV_CHANGED` oracle line) in its first G run and in three more G
runs, and passes that leg (M8: runs without `ENV_CHANGED`) in three mutant
runs, the six runs in a random order; M9, whose clause returns no reason, is
KILLED when, at some seed, the landed builder's verdict vector (exit code and
each leg's PASS/FAIL) equals its first G vector in three G runs and differs
from it in three mutant runs, in a random order; and
(iii) each of the two
frozen hook probes P1 FORKEXEC (`_posixsubprocess.fork_exec` of /bin/true,
then the landed builder) and P2 DIRFD (chdir into a subdirectory of the run
directory, then a `dir_fd`-relative open of the lane's SKILL.md, then the
landed builder) is DENIED — at both seeds G exits 1 with all four legs FAIL
and every leg reason carrying `AUDIT_FORBIDDEN` or the hook's exit `rc=97` — counted
`CANDIDATE=2/2 KILLED=9/9 DENIED=2/2 C1=PASS`.

Run directories carry random names, so no tool can tell a G run from a mutant
run by its path; the tripled random-order runs at both seeds refuse a tool that
alternates or counts its calls (a fixed call pattern matches one random order of
six runs in 20, and both seeds in 400).
A battery entry is a `*.py` file of B run as G's `--tool`; an entry named
`oracle-*.py` is instead run as G's oracle (env `R56_ORACLE`) with the landed
builder as the tool; the landed builder itself is always an entry
(`CANDIDATE`). Both G and every mutant run from scratch copies carrying the
same two harness edits (H1: `LANE` pinned to this lane; H2: the oracle path
read from `R56_ORACLE`, default the lane's `tools/capture-text.py`); an
anchor not found exactly once is exit 2 (`ANCHOR_MISSING`), never a kill.

Usage: python3 corpus/evidence/round56/c1-count.py [--gate G] [--battery B] [--work DIR]
`--work` must be empty or absent (default a mkdtemp under $TMPDIR, removed on exit).
Exit codes: 0 C1=PASS · 1 C1=FAIL · 2 usage/env.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import pathlib
import random
import re
import secrets
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[2]
BUILDER = LANE / "tools" / "build-spans.py"
PROBES = HERE / "probes"
SEEDS = (7, 56)
PER_LEG = "2"
LEGS = ("GENOLE", "OLEPIN", "REFUSE", "REGRESS")

HARNESS = [
    ("H1", "LANE = HERE.parents[2]\n", f"LANE = pathlib.Path({str(LANE)!r})\n"),
    ("H2", 'CAPTURE_TEXT = TOOLS / "capture-text.py"\n',
     'CAPTURE_TEXT = pathlib.Path(os.environ.get("R56_ORACLE") or TOOLS / "capture-text.py")\n'),
]
MUTANTS = [
    ("M1", "NO_SLICE", "if form[o:o + len(span)] != span or len(span) <= len(quote):", "if False:"),
    ("M2", "NO_CHAR", "if span.find(quote) < 0 or o + span.find(quote) != char:", "if False:"),
    ("M3", "NO_SHA", "if cells[2] != hashlib.sha256(fbytes).hexdigest():", "if False:"),
    ("M4", "NO_QUOTE", 'if f"QUOTE {sid} char {char} {name}" not in out:', "if False:"),
    ("M5", "NO_EXTRA", "if have != names:", "if False:"),
    ("M6", "REF_TSV", 'if (run / "out" / "spans.tsv").exists():', "if False:"),
    ("M7", "ALLOW_ROOT",
     'ALLOW = tuple(os.path.realpath(p) + os.sep for p in os.environ.pop("R55_ALLOW").split(os.pathsep) if p)',
     'ALLOW = ("/",)'),
    ("M8", "NO_ORACLE_SHA",
     "if not CAPTURE_TEXT.is_file() or hashlib.sha256(CAPTURE_TEXT.read_bytes()).hexdigest() != CAPTURE_TEXT_SHA:",
     "if not CAPTURE_TEXT.is_file():"),
    ("M9", "WIN_NL", 'any(c in w for c in "\\t\\n\\r\\ufffd")', 'any(c in w for c in "\\t\\ufffd")'),
]
# the reason each mutated clause returns (leg-reason regex; M8 matches G's stdout; M9 has none)
MARKER = {
    "M1": r"span is not a slice of the defined form",
    "M2": r"\bS\d+ char$",
    "M3": r"\bS\d+ capture_sha256$",
    "M4": r"\bS\d+ QUOTE line$",
    "M5": r"extra or missing span files",
    "M6": r"spans\.tsv written",
    "M7": r"AUDIT_FORBIDDEN (open|os\.listdir|os\.scandir) ",
    "M8": r"ENV_CHANGED tools/capture-text\.py is not the pinned oracle",
    "M9": None,
}
# M9 also drops the window filter's second newline guard (ord < 0x20); without it M9 is an equivalent mutant
EXTRA = {"M9": [("or any(ord(c) < 0x20 for c in w) or w in out", "or w in out")]}
PROBE_NAMES = (("P1", "FORKEXEC", "p1-forkexec.py"), ("P2", "DIRFD", "p2-dirfd.py"))
LEG_RE = re.compile(r"^(GENOLE|OLEPIN|REFUSE|REGRESS)=(PASS|FAIL)\b(.*)$")


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def edit(src: str, anchor: str, repl: str, tag: str) -> str:
    n = src.count(anchor)
    if n != 1:
        print(f"ANCHOR_MISSING {tag} count={n}")
        sys.exit(2)
    return src.replace(anchor, repl)


class Runner:
    def __init__(self, work: pathlib.Path):
        self.work, self.n = work, 0

    def run(self, gate: pathlib.Path, tool: pathlib.Path, seed: int, oracle: pathlib.Path | None):
        """Return (vector, leg lines) for one gate run."""
        self.n += 1
        w = self.work / secrets.token_hex(8)
        w.mkdir()
        env = {k: v for k, v in os.environ.items() if k != "R56_ORACLE"}
        env.update({"PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(self.work)})
        if oracle is not None:
            env["R56_ORACLE"] = str(oracle)
        try:
            r = subprocess.run([sys.executable, str(gate), "--tool", str(tool), "--seed", str(seed),
                                "--per-leg", PER_LEG, "--work", str(w / "g")], capture_output=True, text=True,
                               timeout=1800, env=env, cwd=str(w))
            out, rc = r.stdout, r.returncode
        except subprocess.TimeoutExpired:
            out, rc = "", "timeout"
        shutil.rmtree(w, ignore_errors=True)
        legs = {}
        for line in out.splitlines():
            m = LEG_RE.match(line)
            if m:
                legs[m.group(1)] = (m.group(2), m.group(3))
        if "ENV_CHANGED" in out:
            vec = ("ENV", rc)
        else:
            vec = (rc,) + tuple(legs.get(k, ("MISSING", ""))[0] for k in LEGS)
        return vec, legs, out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--gate", default=str(HERE / "c1-gate.py"))
    ap.add_argument("--battery", default=str(HERE / "battery"))
    ap.add_argument("--work")
    a = ap.parse_args()
    gate_p, bat = pathlib.Path(a.gate).resolve(), pathlib.Path(a.battery).resolve()
    if not gate_p.is_file() or not BUILDER.is_file():
        print("NO_GATE_OR_BUILDER")
        return 2
    own = a.work is None
    work = pathlib.Path(tempfile.mkdtemp(prefix="r56c1-")) if own else pathlib.Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    if any(work.iterdir()):
        print("usage: --work must be empty", file=sys.stderr)
        return 2
    try:
        src = gate_p.read_text(encoding="utf-8")
        for tag, anc, rep in HARNESS:
            src = edit(src, anc, rep, tag)
        gates = {"G": src}
        for tag, name, anc, rep in MUTANTS:
            m = edit(src, anc, rep, f"{tag} {name}")
            for anc2, rep2 in EXTRA.get(tag, []):
                m = edit(m, anc2, rep2, f"{tag} {name} extra")
            gates[tag] = m
        gdir = work / "gates"
        gdir.mkdir()
        paths = {}
        for tag, text in gates.items():
            p = gdir / f"{tag}.py"
            p.write_text(text, encoding="utf-8")
            paths[tag] = p
        entries = [("CANDIDATE", BUILDER, None)]
        if bat.is_dir():
            for p in sorted(bat.glob("*.py")):
                entries.append((p.name, BUILDER, p) if p.name.startswith("oracle-") else (p.name, p, None))
        print(f"gate={gate_p} sha256={sha(gate_p)}")
        print(f"builder={BUILDER} sha256={sha(BUILDER)}")
        for name, tool, oracle in entries[1:]:
            print(f"battery {name} sha256={sha(oracle or tool)}")
        R = Runner(work / "runs")
        R.work.mkdir()
        base = {}
        for seed in SEEDS:
            for name, tool, oracle in entries:
                base[(seed, name)] = R.run(paths["G"], tool, seed, oracle)
        cand = sum(base[(s, "CANDIDATE")][0] == (0, "PASS", "PASS", "PASS", "PASS") for s in SEEDS)
        print(f"CANDIDATE={cand}/{len(SEEDS)} " + " ".join(f"seed{s}={base[(s, 'CANDIDATE')][0]}" for s in SEEDS))
        order_rng = random.Random(secrets.randbits(64))

        def failing_legs(res, rx, tag) -> list[str]:
            vec, legs, out = res
            if rx is None:
                return []
            if tag == "M8":
                return ["ENV"] if re.search(rx, out, re.M) else []
            return [k for k in LEGS if legs.get(k, ("", ""))[0] == "FAIL" and re.search(rx, legs[k][1].strip())]

        killed = 0

        def attempt(tag, rx, seed, name, tool, oracle):
            """Six runs (3 G, 3 mutant) in a random order; return a kill description or None."""
            seq = ["G"] * 3 + [tag] * 3
            order_rng.shuffle(seq)
            res = [(g, R.run(paths[g], tool, seed, oracle)) for g in seq]
            gs = [r for g, r in res if g == "G"]
            ms = [r for g, r in res if g != "G"]
            order = "".join("G" if g == "G" else "m" for g, _ in res)
            if rx is None:
                b = base[(seed, name)][0]
                if all(r[0] == b for r in gs) and all(r[0] != b for r in ms):
                    return f"seed {seed} order {order}: G={b} mutant={ms[0][0]}"
                return None
            if tag == "M8":
                if (all(failing_legs(r, rx, tag) for r in gs)
                        and all("ENV_CHANGED" not in r[2] and r[0][0] in (0, 1) for r in ms)):
                    return f"seed {seed} order {order}: G={gs[0][0]} mutant={ms[0][0]}"
                return None
            fl = failing_legs(base[(seed, name)], rx, tag)
            ok = [k for k in fl if all(k in failing_legs(r, rx, tag) for r in gs)
                  and all(r[1].get(k, ("", ""))[0] == "PASS" for r in ms)]
            if ok:
                return f"seed {seed} order {order}: leg {ok[0]} G={gs[0][1][ok[0]][1].strip()[:80]!r} mutant=PASS"
            return None

        for tag, mname, _a, _r in MUTANTS:
            rx = MARKER[tag]
            hit = None
            for name, tool, oracle in entries:
                if rx is None:
                    if name != "CANDIDATE":
                        continue
                    for seed in SEEDS:
                        h = attempt(tag, rx, seed, name, tool, oracle)
                        if h:
                            hit = (name, [h])
                            break
                else:
                    if not all(failing_legs(base[(s, name)], rx, tag) for s in SEEDS):
                        continue
                    hs = []
                    for seed in SEEDS:
                        h = attempt(tag, rx, seed, name, tool, oracle)
                        if not h:
                            break
                        hs.append(h)
                    if len(hs) == len(SEEDS):
                        hit = (name, hs)
                if hit:
                    break
            killed += hit is not None
            if hit:
                print(f"MUTANT {tag} {mname} KILLED by {hit[0]}: " + " | ".join(hit[1]))
            else:
                print(f"MUTANT {tag} {mname} SURVIVED")
        denied = 0
        for tag, pname, fn in PROBE_NAMES:
            p = PROBES / fn
            ok = p.is_file()
            why = []
            for seed in SEEDS:
                if not ok:
                    break
                vec, legs, _out = R.run(paths["G"], p, seed, None)
                good = (vec == (1, "FAIL", "FAIL", "FAIL", "FAIL")
                        and all("AUDIT_FORBIDDEN" in legs[k][1] or "rc=97" in legs[k][1] for k in LEGS))
                why.append(f"seed{seed}={vec}")
                ok = ok and good
            denied += ok
            print(f"PROBE {tag} {pname} {'DENIED' if ok else 'NOT_DENIED'} " + " ".join(why))
        print(f"RUNS={R.n}")
        print(f"CANDIDATE={cand}/{len(SEEDS)} KILLED={killed}/{len(MUTANTS)} DENIED={denied}/{len(PROBE_NAMES)}")
        passed = cand == len(SEEDS) and killed == len(MUTANTS) and denied == len(PROBE_NAMES)
        print("C1=PASS" if passed else "C1=FAIL")
        return 0 if passed else 1
    finally:
        if own:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
