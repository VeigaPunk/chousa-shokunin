#!/usr/bin/env python3
"""c1-count — the frozen counter for round 42 claim C1 (operability).

Claim C1 (operability, the lane's lowest scored non-retired axis, 3/10):
the lane's quarantine scope becomes a RUNNABLE, RE-DERIVED surface — one committed
command re-derives the lane's absent-defect-register slice from the read-only
register and examines every quarantined quote against the capture material that is
already on disk, and the derivation is complete, reproducible and control-discriminating.

This counter grades the SURFACE, not a number of rows:
  SLICE_REDERIVE_MATCH  the tool's slice equals an independent re-parse of the register
  QUOTES_EXAMINED       every independently counted quarantined quote is examined
  REPRODUCIBLE          two runs of the examination agree byte for byte
  POSITIVE_CONTROL     a planted quote inside a scratch capture IS located
  NEGATIVE_CONTROL     a quote absent from a scratch capture is NOT located
  MUTANT_DETECTED       a register with one lane data row removed yields a smaller slice

The do-nothing control is a tree without the tool: this counter cannot run and exits
non-zero. Exit 0 only when every count above holds.

Exit codes: 0 all counts hold · 1 a count failed · 2 usage/env.
"""
from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
TOOL = LANE / "tools" / "quarantine-check.py"
REGISTER = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md")
CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    return ok


def load_tool():
    spec = importlib.util.spec_from_file_location("quarantine_check", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def independent_slice(register: pathlib.Path):
    """An independent re-parse of the register: own regex, own column handling."""
    ids, quotes = [], {}
    for line in register.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 6 or cells[1] != "`chousa`":
            continue
        if not cells[2].startswith("round") or not cells[2][5:].isdigit():
            continue
        rid = cells[3].rstrip("`")
        if not (rid.startswith("S") and rid[1:].isdigit()):
            continue
        ids.append(rid)
        cell = cells[6] if len(cells) >= 8 else ""
        n = 0
        for raw in cell.split("<br>"):
            q = raw.strip()
            if q.startswith("`") and q.endswith("`") and len(q) >= 2:
                n += 1
        quotes[rid] = n
    return ids, quotes


def run_tool(command, register=REGISTER, cache=CACHE):
    proc = subprocess.run([sys.executable, str(TOOL), command, "--register", str(register),
                           "--cache", str(cache)], capture_output=True, text=True)
    return proc


def main():
    if not TOOL.is_file():
        sys.stderr.write("c1-count: the gate tool is absent: %s\n" % TOOL)
        return 1
    mod = load_tool()
    ids, quotes = independent_slice(REGISTER)
    tool_rows = mod.parse_register(REGISTER)
    tool_ids = [r["id"] for r in tool_rows]
    check("SLICE_REDERIVE_MATCH", tool_ids == ids,
          "tool=%d independent=%d" % (len(tool_ids), len(ids)))
    n_expected = sum(quotes.values())

    ex1 = run_tool("examine")
    check("EXAMINE_RUNS", ex1.returncode == 0, "exit=%d %s" % (ex1.returncode, ex1.stderr[:120]))
    examined = [l for l in ex1.stdout.splitlines() if l.strip()]
    check("QUOTES_EXAMINED", len(examined) == n_expected,
          "examined=%d expected=%d" % (len(examined), n_expected))
    check("NO_SKIPPED_QUOTE", all(l.split("\t")[2] in ("located", "loose-only", "absent", "no-capture")
                                  for l in examined),
          "every examined quote carries a status")
    ex2 = run_tool("examine")
    check("REPRODUCIBLE", ex1.stdout == ex2.stdout and ex1.returncode == ex2.returncode,
          "two runs identical=%s" % (ex1.stdout == ex2.stdout))

    # positive and negative controls on a scratch capture
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        scratch = pathlib.Path(td)
        cache = scratch / "cache"
        cache.mkdir()
        planted = "a planted sentence that must be located verbatim in the capture"
        (cache / "a.txt").write_text("prefix\n" + planted + "\nsuffix\n", encoding="utf-8")
        # the tool resolves a URL to a cache file by sha256(url)[:24]; build that file
        import hashlib
        url = "https://example.invalid/control"
        key = hashlib.sha256(url.encode()).hexdigest()[:24]
        (cache / (key + ".txt")).write_text("prefix\n" + planted + "\nsuffix\n", encoding="utf-8")
        (cache / (key + ".raw")).write_bytes(b"<html><body>prefix\n" + planted.encode() + b"\nsuffix\n</body></html>")
        absent = "a sentence that is nowhere in this capture at all"
        fold, strict, _off = mod.examine_quote((cache / (key + ".txt")).read_text(encoding="utf-8"), planted)
        check("POSITIVE_CONTROL", strict and fold is not None, "fold=%s strict=%s" % (fold, strict))
        fold2, strict2, _o2 = mod.examine_quote((cache / (key + ".txt")).read_text(encoding="utf-8"), absent)
        check("NEGATIVE_CONTROL", not strict2 and fold2 is None, "fold=%s strict=%s" % (fold2, strict2))

        # mutant register: drop one lane data row
        reg_lines = REGISTER.read_text(encoding="utf-8").splitlines()
        mutated = []
        dropped = False
        for line in reg_lines:
            cells = [c.strip() for c in line.split("|")]
            if (not dropped and len(cells) >= 8 and cells[1] == "`chousa`"
                    and cells[2].startswith("round") and cells[3].startswith("S")):
                dropped = True
                continue
            mutated.append(line)
        mreg = scratch / "mutated-register.md"
        mreg.write_text("\n".join(mutated) + "\n", encoding="utf-8")
        mrows = mod.parse_register(mreg)
        check("MUTANT_DETECTED", len(mrows) == len(tool_rows) - 1,
              "mutant=%d base=%d" % (len(mrows), len(tool_rows)))

    width = max(len(n) for n, _, _ in RESULTS)
    for name, ok, detail in RESULTS:
        print("%-*s %s  %s" % (width, name, "PASS" if ok else "FAIL", detail))
    counts = {
        "SLICE_REDERIVE_MATCH": "%d/%d" % (len(ids), len(ids)) if tool_ids == ids else "%d/%d" % (len(tool_ids), len(ids)),
        "QUOTES_EXAMINED": "%d/%d" % (len(examined), n_expected),
        "REPRODUCIBLE": "1/1" if dict((n, o) for n, o, _ in RESULTS)["REPRODUCIBLE"] else "0/1",
        "POSITIVE_CONTROL": "1/1" if dict((n, o) for n, o, _ in RESULTS)["POSITIVE_CONTROL"] else "0/1",
        "NEGATIVE_CONTROL": "1/1" if dict((n, o) for n, o, _ in RESULTS)["NEGATIVE_CONTROL"] else "0/1",
        "MUTANT_DETECTED": "1/1" if dict((n, o) for n, o, _ in RESULTS)["MUTANT_DETECTED"] else "0/1",
    }
    for k, v in counts.items():
        print("%s=%s" % (k, v))
    return 0 if all(ok for _, ok, _ in RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
