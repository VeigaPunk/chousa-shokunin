#!/usr/bin/env python3
"""Round-37 C2 counter — the pinned baseline versus the caller's BASH_ENV.

Predicate (frozen in corpus/evidence/round37/claims.md before any candidate run):

    PIN_CAPTURE_ENV_MATCH=7/7

The gate's canonical pin capture scrubbed the named `CHOUSA_*` variables from the
child environment but not `BASH_ENV`: a non-interactive bash sources `$BASH_ENV`
at startup, so the child re-exported a scrubbed variable (or moved `CHOUSA_ROOT`).
A baseline pinned under such a startup file embedded a `GATE_GREP:` receipt line,
and a later plain `--drift` reported a phantom drift (`-GATE_GREP` / `+GATE_GREP`)
against an unchanged gate; a startup file exporting `CHOUSA_ROOT` made the capture
fail, so `--pin` exited 2 and wrote no baseline at all.

Seven scenarios; each expectation is fixed in the table below. Three are contract
holds (they must pass before and after); four are the separation cells (the base
gate reports a phantom drift or writes no baseline). A scenario passes only when
every listed observation matches: the pin exit code, the baseline file's existence
and its `GATE_GREP:` line count, the drift exit code and the drift's exact
`GATE_DRIFT:` line.

Scoring: matched / 7, printed as PIN_CAPTURE_ENV_MATCH=<k>/7.
Exit 0 iff k == 7; 1 otherwise; 2 on a harness error (fixture/gate unreadable).

Temp dirs: $C2_TMP (must exist) or the system temp; a fresh mkdtemp inside it.
No network. Writes only under the temp dir and the optional --receipt path.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

# id, bashenv body or None, pin? drift?, expected observations
#   expect: dict(pin_rc, pin_file, baseline_echo_lines, drift_rc, drift_line)
ECHO_ENV = "export CHOUSA_GREP_PIN_ECHO=1\n"
FN_ENV = "export CHOUSA_GREP_PIN_ECHO=1\ngrep() { command grep \"$@\"; }\n"
STRICT_ENV = "export CHOUSA_STRICT=1\n"
BENIGN_ENV = "export BENIGN_R37=1\n"
ROOT_ENV = "export CHOUSA_ROOT=%s\n"  # %s = a foreign root written per run

SCENARIOS = [
    # id, env-file mode, order, expect
    ("hold-plain", None, ("pin", "drift"),
     dict(pin_rc=0, pin_file=True, baseline_echo_lines=0, drift_rc=0, drift_line="GATE_DRIFT: none")),
    ("hold-benign", "benign", ("pin", "drift"),
     dict(pin_rc=0, pin_file=True, baseline_echo_lines=0, drift_rc=0, drift_line="GATE_DRIFT: none")),
    ("env-echo-pin", "echo", ("pin", "drift"),
     dict(pin_rc=0, pin_file=True, baseline_echo_lines=0, drift_rc=0, drift_line="GATE_DRIFT: none")),
    ("env-echo-drift", "echo-on-drift", ("pin", "drift"),
     dict(pin_rc=0, pin_file=True, baseline_echo_lines=0, drift_rc=0, drift_line="GATE_DRIFT: none")),
    ("env-fn-echo-pin", "fn", ("pin", "drift"),
     dict(pin_rc=0, pin_file=True, baseline_echo_lines=0, drift_rc=0, drift_line="GATE_DRIFT: none")),
    ("env-root-pin", "root", ("pin", "drift"),
     dict(pin_rc=0, pin_file=True, baseline_echo_lines=0, drift_rc=0, drift_line="GATE_DRIFT: none")),
    ("env-strict-pin", "strict", ("pin", "drift"),
     dict(pin_rc=0, pin_file=True, baseline_echo_lines=0, drift_rc=0, drift_line="GATE_DRIFT: none")),
]

SCRUB = ("CHOUSA_RECORD", "CHOUSA_CLAIMS", "CHOUSA_AGGREGATOR_ERE",
         "CHOUSA_GREP_PIN_ECHO", "BASH_ENV")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run_gate(gate, args, bashenv=None, cwd=None):
    env = dict(os.environ)
    for var in SCRUB:
        env.pop(var, None)
    if bashenv is not None:
        env["BASH_ENV"] = bashenv
    proc = subprocess.run(["bash", gate] + list(args), capture_output=True,
                          text=True, env=env, cwd=cwd, timeout=180)
    return proc.returncode, proc.stdout + proc.stderr


def drift_line(out):
    for line in out.splitlines():
        if line.startswith("GATE_DRIFT:"):
            return line.strip()
    return "none"


def run_scenario(gate, work, sid, mode, order, expected):
    sdir = os.path.join(work, sid)
    os.makedirs(sdir, exist_ok=True)
    baseline = "baseline.txt"
    bp = os.path.join(sdir, baseline)
    foreign = os.path.join(sdir, "foreign-root")
    os.makedirs(foreign, exist_ok=True)

    bodies = {
        "benign": BENIGN_ENV,
        "echo": ECHO_ENV,
        "echo-on-drift": ECHO_ENV,
        "fn": FN_ENV,
        "strict": STRICT_ENV,
        "root": ROOT_ENV % foreign,
    }
    envfile = None
    if mode is not None:
        envfile = os.path.join(sdir, "startup.env")
        with open(envfile, "w", encoding="utf-8") as fh:
            fh.write(bodies[mode])

    pin_env = envfile if mode in ("benign", "echo", "fn", "strict", "root") else None
    drift_env = envfile if mode == "echo-on-drift" else None

    pin_rc, pin_out = run_gate(gate, ["--pin", baseline], bashenv=pin_env, cwd=sdir)
    drift_rc, drift_out = run_gate(gate, ["--drift", baseline], bashenv=drift_env, cwd=sdir)

    echo_lines = -1
    if os.path.isfile(bp):
        with open(bp, "r", encoding="utf-8", errors="replace") as fh:
            echo_lines = sum(1 for line in fh if line.startswith("GATE_GREP: "))

    observed = dict(pin_rc=pin_rc, pin_file=os.path.isfile(bp),
                    baseline_echo_lines=echo_lines, drift_rc=drift_rc,
                    drift_line=drift_line(drift_out))
    ok = all(observed[k] == expected[k] for k in expected)
    return {"id": sid, "env": mode or "none", "expected": expected,
            "observed": observed, "ok": ok,
            "pin_out_tail": pin_out.strip().splitlines()[-1:] if pin_out.strip() else [],
            "drift_out_tail": drift_out.strip().splitlines()[-1:] if drift_out.strip() else []}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", required=True)
    ap.add_argument("--seed", type=int, default=37021)
    ap.add_argument("--receipt")
    ap.add_argument("--tmp")
    args = ap.parse_args()

    gate = os.path.abspath(args.gate)
    if not os.path.isfile(gate):
        print("c2-count: gate not found: %s" % gate, file=sys.stderr)
        return 2
    base_tmp = args.tmp or os.environ.get("C2_TMP") or tempfile.gettempdir()
    if not os.path.isdir(base_tmp):
        print("c2-count: temp dir does not exist: %s" % base_tmp, file=sys.stderr)
        return 2
    work = tempfile.mkdtemp(prefix="chousa-r37-c2-", dir=base_tmp)
    try:
        rows = [run_scenario(gate, work, *spec) for spec in SCENARIOS]
    finally:
        shutil.rmtree(work, ignore_errors=True)

    matched = sum(1 for r in rows if r["ok"])
    total = len(rows)
    for r in rows:
        print("%s %-16s env=%-14s expected pin_rc=%d file=%s echo=%d drift_rc=%d %r  "
              "observed pin_rc=%d file=%s echo=%s drift_rc=%d %r"
              % ("PASS" if r["ok"] else "FAIL", r["id"], r["env"],
                 r["expected"]["pin_rc"], r["expected"]["pin_file"],
                 r["expected"]["baseline_echo_lines"], r["expected"]["drift_rc"],
                 r["expected"]["drift_line"], r["observed"]["pin_rc"],
                 r["observed"]["pin_file"], r["observed"]["baseline_echo_lines"],
                 r["observed"]["drift_rc"], r["observed"]["drift_line"]))
    print("PIN_CAPTURE_ENV_MATCH=%d/%d" % (matched, total))
    holds = matched == total
    if args.receipt:
        receipt = {"counter": "corpus/evidence/round37/c2-count.py", "seed": args.seed,
                   "gate": gate, "gate_sha256": sha256_file(gate),
                   "scenarios": rows, "matched": matched, "total": total,
                   "predicate": "PIN_CAPTURE_ENV_MATCH=7/7",
                   "predicate_holds": holds}
        with open(args.receipt, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=2, sort_keys=True)
            fh.write("\n")
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
