#!/usr/bin/env python3
"""Round-41 C1 counter: canonical-capture PATH/loader independence.

Usage: python3 corpus/evidence/round41/c1-count.py [--gate PATH]
Runs the frozen 12-cell scenario table (claims.md) against a gate script and
prints CAPTURE_PIN_MATCH=<k>/<n>. Exit 0 iff every applicable cell holds.
Receipts are written under corpus/evidence/round41/receipts/<seed>/.
Deterministic: no randomness; all temp roots under a caller-mkdir'd work dir.
"""
import json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

LANE = Path(__file__).resolve().parents[3]
GATE_DEFAULT = LANE / "tools" / "research-gate.sh"
RCPTS = LANE / "corpus" / "evidence" / "round41" / "receipts"

TRAP_TOOLS = ["mktemp", "sed", "mkdir", "cat", "rm", "sort", "env", "bash",
              "grep", "tr", "date", "readlink", "dirname", "wc", "od", "head",
              "sha256sum", "timeout"]

LOG = "trap.log"

def make_traps(d: Path, names, mode="pass", log_ld=False):
    """Write trap binaries into d. mode pass = log+delegate; suppress = log+exit 0."""
    d.mkdir(parents=True, exist_ok=True)
    for n in names:
        body = [
            "#!/bin/sh",
            'tag=OUTER; case "$PWD" in */chousa-gate-pin.*) tag=CHILD;; esac',
        ]
        if log_ld:
            body.append(f'echo "$tag:{n}:LD=${{LD_PRELOAD:-EMPTY}} argv:$*" >> "$TRAPLOG"')
        else:
            body.append(f'echo "$tag:{n}:argv:$*" >> "$TRAPLOG"')
        if mode == "suppress":
            body.append("exit 0")
        elif mode == "tr-poison" and n == "tr":
            body.append('if [ "$1" = "A-Z" ] && [ "$2" = "a-z" ]; then printf "POISONED_TR_%s\\n" "$tag"; exit 0; fi')
            body.append(f'exec /usr/bin/{n} "$@"')
        elif mode == "cat-poison" and n == "cat":
            body.append('out=$(readlink "/proc/$$/fd/1" 2>/dev/null || true)')
            body.append('case "$out" in */claims.jsonl|*/record.md)')
            body.append(f'  /usr/bin/{n} "$@"; printf \'{{"id":"POISON","source":"lib/primary.md","span":"x","expect":"supported"}}\\n\'; exit 0;;')
            body.append('esac')
            body.append(f'exec /usr/bin/{n} "$@"')
        elif mode == "sort-reverse" and n == "sort":
            body.append(f'exec /usr/bin/{n} -r "$@"')
        elif mode == "mktemp-preseed" and n == "mktemp":
            body.append('echo "PRESEED-USED" >> "$TRAPLOG"')
            body.append('printf "%s\\n" "$PRESEED_DIR"')
            body.append("exit 0")
        else:
            body.append(f'exec /usr/bin/{n} "$@"')
        p = d / n
        p.write_text("\n".join(body) + "\n")
        p.chmod(0o755)

def read_log(w: Path):
    f = w / LOG
    if not f.exists():
        return []
    return [l.strip() for l in f.read_text().splitlines() if l.strip()]

def run_gate(gate: Path, args, w: Path, env_extra=None, timeout=120):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    env["TRAPLOG"] = str(w / LOG)
    p = subprocess.run(["/usr/bin/bash", str(gate), *args], cwd=str(LANE), env=env,
                       capture_output=True, text=True, timeout=timeout)
    return p

def leftovers():
    return [p for p in Path(tempfile.gettempdir()).glob("chousa-gate-pin.*") if p.is_dir()]

def pin_and_drift(gate, w: Path, env_extra=None):
    """Run --pin into w/baseline.txt then --drift on it. Returns (pin, drift)."""
    base = w / "baseline.txt"
    pin = run_gate(gate, ["--pin", str(base)], w, env_extra)
    drift = run_gate(gate, ["--drift", str(base)], w, env_extra)
    return pin, drift, base

def tamper(base: Path):
    t = base.read_text()
    marker = "# --- canonical output follows ---"
    t = t.replace(marker, marker + "\nTAMPERED_SENTINEL_LINE =1")
    base.write_text(t)

def cell(name, ok, evidence):
    return {"cell": name, "predicate_holds": bool(ok), "evidence": evidence}

def main():
    gate = GATE_DEFAULT
    if "--gate" in sys.argv:
        gate = Path(sys.argv[sys.argv.index("--gate") + 1]).resolve()
    work = Path(tempfile.mkdtemp(prefix="chousa-r41-c1-"))
    RCPTS.mkdir(parents=True, exist_ok=True)
    results = []
    out_dir = RCPTS / "cells"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    # S1 base-clean
    w = work / "s1"; w.mkdir()
    pin, drift, base = pin_and_drift(gate, w)
    ok = (drift.returncode == 0 and "GATE_DRIFT: none" in drift.stdout
          and pin.returncode == 0 and "GATE_PIN: ok" in pin.stdout)
    results.append(cell("S1-base-clean", ok,
        {"pin_rc": pin.returncode, "drift_rc": drift.returncode,
         "drift_stdout": drift.stdout.strip()[:200]}))

    # S2 trap-inventory
    w = work / "s2"; w.mkdir()
    td = w / "traps"; make_traps(td, TRAP_TOOLS, "pass")
    env = {"PATH": f"{td}:/usr/bin:/bin"}
    pin, drift, _ = pin_and_drift(gate, w, env)
    marks = read_log(w)
    cap_marks = [m for m in marks if "SELFWRAP" not in m]
    ok = len(cap_marks) == 0 and "GATE_DRIFT: none" in drift.stdout
    results.append(cell("S2-trap-inventory", ok,
        {"trap_marks": cap_marks[:40], "count": len(cap_marks),
         "drift": drift.stdout.strip()[:120]}))

    # S3 sed-suppress
    w = work / "s3"; w.mkdir()
    td = w / "traps"; make_traps(td, ["sed"], "suppress")
    env = {"PATH": f"{td}:/usr/bin:/bin"}
    pin, drift, _ = pin_and_drift(gate, w, env)
    marks = read_log(w)
    ok = ("GATE_DRIFT: none" in drift.stdout and drift.returncode == 0
          and not any(m.endswith("sed:argv") or ":sed:" in m for m in marks))
    results.append(cell("S3-sed-suppress", ok,
        {"drift_rc": drift.returncode, "drift": drift.stdout.strip()[:200],
         "sed_marks": [m for m in marks if ":sed:" in m][:10]}))

    # S4 mktemp-preseed
    w = work / "s4"; w.mkdir()
    pre = w / "preseed"; pre.mkdir()
    (pre / "capture.txt").write_text("RESEARCH_GATE: DRIFT (sections=5)\n" * 1)
    (pre / "manifest.jsonl").write_text('{"schema":"chousa-verify-all/v1","x":1}\n')
    td = w / "traps"; make_traps(td, ["mktemp"], "mktemp-preseed")
    env = {"PATH": f"{td}:/usr/bin:/bin", "PRESEED_DIR": str(pre)}
    pin, drift, _ = pin_and_drift(gate, w, env)
    marks = read_log(w)
    ok = ("GATE_DRIFT: none" in drift.stdout and drift.returncode == 0
          and not any("PRESEED-USED" in m for m in marks))
    results.append(cell("S4-mktemp-preseed", ok,
        {"drift": drift.stdout.strip()[:200], "stderr": drift.stderr.strip()[:200],
         "preseed_used": any("PRESEED-USED" in m for m in marks)}))

    # S5 cat-poison
    w = work / "s5"; w.mkdir()
    td = w / "traps"; make_traps(td, ["cat"], "cat-poison")
    env = {"PATH": f"{td}:/usr/bin:/bin"}
    pin, drift, _ = pin_and_drift(gate, w, env)
    marks = read_log(w)
    ok = ("GATE_DRIFT: none" in drift.stdout and drift.returncode == 0
          and not any(":cat:" in m for m in marks))
    results.append(cell("S5-cat-poison", ok,
        {"drift_rc": drift.returncode, "drift": drift.stdout.strip()[:200],
         "stderr": (pin.stderr + drift.stderr)[:300],
         "cat_marks": [m for m in marks if ":cat:" in m][:10]}))

    # S6 rm-suppress
    for p in leftovers():
        shutil.rmtree(p, ignore_errors=True)
    w = work / "s6"; w.mkdir()
    td = w / "traps"; make_traps(td, ["rm"], "suppress")
    env = {"PATH": f"{td}:/usr/bin:/bin"}
    pin, drift, _ = pin_and_drift(gate, w, env)
    lo = leftovers()
    marks = read_log(w)
    ok = ("GATE_DRIFT: none" in drift.stdout and len(lo) == 0
          and not any(":rm:" in m for m in marks))
    results.append(cell("S6-rm-suppress", ok,
        {"leftovers": [str(p) for p in lo], "drift": drift.stdout.strip()[:120],
         "rm_marks": [m for m in marks if ":rm:" in m][:5]}))

    # S7 sort-reverse (tampered baseline forces gate_drift_report)
    w = work / "s7"; w.mkdir()
    td = w / "traps"; make_traps(td, ["sort"], "sort-reverse")
    env = {"PATH": f"{td}:/usr/bin:/bin"}
    pin, drift, base = pin_and_drift(gate, w, env)
    # regenerate: tamper then re-drift
    tamper(base)
    drift2 = run_gate(gate, ["--drift", str(base)], w, env)
    marks = read_log(w)
    ok = (drift2.returncode == 1 and "GATE_DRIFT:" in drift2.stdout
          and not any(":sort:" in m for m in marks))
    results.append(cell("S7-sort-reverse", ok,
        {"drift": drift2.stdout.strip()[:240],
         "sort_marks": [m for m in marks if ":sort:" in m][:5]}))

    # S8 mkdir-suppress
    w = work / "s8"; w.mkdir()
    td = w / "traps"; make_traps(td, ["mkdir"], "suppress")
    env = {"PATH": f"{td}:/usr/bin:/bin"}
    pin, drift, _ = pin_and_drift(gate, w, env)
    marks = read_log(w)
    ok = ("GATE_DRIFT: none" in drift.stdout and drift.returncode == 0
          and not any(":mkdir:" in m for m in marks))
    results.append(cell("S8-mkdir-suppress", ok,
        {"drift": drift.stdout.strip()[:200], "stderr": drift.stderr.strip()[:200],
         "mkdir_marks": [m for m in marks if ":mkdir:" in m][:5]}))

    # S9 override-relative (after-only; mechanism absent before)
    w = work / "s9"; w.mkdir()
    env = {"RESEARCH_GATE_SED": "relative/path sed"}
    pin = run_gate(gate, ["--pin", str(w / "b.txt")], w, env)
    ok = (pin.returncode == 2 and "SED_PROVENANCE refused" in pin.stderr)
    results.append(cell("S9-override-relative", ok,
        {"rc": pin.returncode, "stderr": pin.stderr.strip()[:200],
         "applicable": "after-only"}))

    # S10 override-nongnu
    w = work / "s10"; w.mkdir()
    stub = w / "faketemp"
    stub.write_text("#!/bin/sh\necho 'not coreutils'\n")
    stub.chmod(0o755)
    env = {"RESEARCH_GATE_MKTEMP": str(stub)}
    pin = run_gate(gate, ["--pin", str(w / "b.txt")], w, env)
    ok = (pin.returncode == 2 and "MKTEMP_PROVENANCE refused" in pin.stderr)
    results.append(cell("S10-override-nongnu", ok,
        {"rc": pin.returncode, "stderr": pin.stderr.strip()[:200],
         "applicable": "after-only"}))

    # S11 child-tr
    w = work / "s11"; w.mkdir()
    td = w / "traps"; make_traps(td, ["tr"], "tr-poison")
    env = {"PATH": f"{td}:/usr/bin:/bin"}
    pin, drift, _ = pin_and_drift(gate, w, env)
    marks = read_log(w)
    child_tr = [m for m in marks if m.startswith("CHILD:tr:")]
    ok = ("GATE_DRIFT: none" in drift.stdout and drift.returncode == 0
          and len(child_tr) == 0)
    results.append(cell("S11-child-tr", ok,
        {"drift": drift.stdout.strip()[:240],
         "child_tr_marks": child_tr[:10], "all_tr": [m for m in marks if ":tr:" in m][:10]}))

    # S12 loader-env
    w = work / "s12"; w.mkdir()
    td = w / "traps"; make_traps(td, ["tr", "mktemp", "sed"], "pass", log_ld=True)
    env = {"PATH": f"{td}:/usr/bin:/bin", "LD_PRELOAD": "/tmp/cap/ld-mark.so"}
    pin, drift, _ = pin_and_drift(gate, w, env)
    marks = read_log(w)
    child_ld = [m for m in marks if m.startswith("CHILD:") and "LD=" in m]
    bad = [m for m in child_ld if "LD=EMPTY" not in m]
    ok = (len(bad) == 0)
    results.append(cell("S12-loader-env", ok,
        {"child_ld_marks": child_ld[:15], "violations": bad[:10],
         "drift": drift.stdout.strip()[:120]}))

    applicable = [r for r in results]
    k = sum(1 for r in applicable if r["predicate_holds"])
    n = len(applicable)
    receipt = {"gate": str(gate), "k": k, "n": n, "cells": results}
    (out_dir / "cells.json").write_text(json.dumps(receipt, indent=1))
    print(f"CAPTURE_PIN_MATCH={k}/{n}")
    for r in results:
        print(f"  {'PASS' if r['predicate_holds'] else 'FAIL'} {r['cell']}")
    shutil.rmtree(work, ignore_errors=True)
    sys.exit(0 if k == n else 1)

if __name__ == "__main__":
    main()
