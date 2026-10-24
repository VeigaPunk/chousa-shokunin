#!/usr/bin/env python3
"""Round 35, C2 counter, design v1: the lane can distinguish an output-equivalent
keyed engine from the landed dead-zone mechanism (mechanism witness), where the
output-only counters cannot.

Frozen predicate (claims.md, C2, P2): C2 is met iff this counter prints
WITNESS_SEPARATED=2/2 with LANDED_WITNESS=pass on each of two fresh seeds against
the landed lane revision, and no committed run of this counter against the landed
gate prints a lower separation.
Code condition: holds = separated == VARIANTS and variant_output_full == VARIANTS
                and landed witness == "pass" and landed output full.
Receipt label: predicate_holds.

Surface: `tools/mechanism-witness.py` (the round's capability) vs the two
output-equivalent keyed engines this counter builds from the candidate gate:

  K1 python-exact     for a long span, `tok_span_offsets` calls a python
                      bytes.find exact search instead of the chunk matcher.
                      It implements the same contract (exact occurrence,
                      non-overlapping, left to right), so every output counter
                      scores it full.
  K2 root-keyed       as K1, but the branch fires only when ROOT looks like a
                      harness temp dir (/tmp, /fast, /var/tmp). On the real
                      corpus it is inert (the gate behaves as landed); on any
                      counter fixture it shortcuts. No fixture-prefix or
                      record-shape key is needed, so per-seed randomization of
                      the fixture does not remove it.

Both are correct implementations of the written contract, so an output counter
*kills* neither (that is the round-34 finding: controls ctl4/ctl6 scored 37/37).
The witness separates them from the landed gate because their long-span path
never calls the chunk matcher.

Before-state: with no witness battery the same counter prints
WITNESS_SEPARATED=0/2 (battery=absent) — the base tree holds no
tools/mechanism-witness.py.

Also built: a `--stub-pass` / `--stub-fail` self-check (the battery's own
trivial-stub resistance: a witness that always says pass separates nothing, a
witness that always says fail also fails the landed gate).

Exit: 0 iff holds; 1 otherwise; 2 harness error.
No network; writes only its temp dir (C2_TMP or TMPDIR) and --receipt.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

LABEL = "WITNESS_SEPARATED"
VARIANTS = ["K1-python-exact", "K2-root-keyed"]
WITNESS_TIMEOUT_S = 1800
HELPER_SRC = '''import os, sys
hay = sys.stdin.buffer.read()
span = os.fsencode(sys.argv[1])
off = 0
while True:
    i = hay.find(span, off)
    if i < 0:
        break
    sys.stdout.write("%d\\n" % i)
    off = i + len(span)
'''

K1_BRANCH = '''  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    printf '%s' "$hay" | python3 "@HELPER@" "$span"
    return 0
  fi
'''

K2_BRANCH = '''  local _wkey=0
  case "${ROOT:-}" in /tmp/*|/fast/*|/var/tmp/*) _wkey=1;; esac
  if (( _wkey == 1 )) && (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    printf '%s' "$hay" | python3 "@HELPER@" "$span"
    return 0
  fi
'''


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def patch_gate(gate_text, helper, branch):
    """Insert `branch` as the first statement of tok_span_offsets' body."""
    lines = gate_text.splitlines(keepends=True)
    start = None
    for i, l in enumerate(lines):
        if l.startswith("tok_span_offsets()"):
            start = i
            break
    if start is None:
        raise RuntimeError("tok_span_offsets not found")
    body = None
    for j in range(start + 1, min(start + 40, len(lines))):
        t = lines[j].strip()
        if t.startswith("local hay=$1 span=$2"):
            body = j + 1          # after the parameter locals: hay/span are in scope
            break
    if body is None:
        raise RuntimeError("tok_span_offsets parameter locals not found")
    out = lines[:body] + [branch.replace("@HELPER@", helper)] + lines[body:]
    return "".join(out)


def run_witness(tool, gate, seed, tmp, receipt_path):
    os.makedirs(tmp, exist_ok=True)
    p = subprocess.run([sys.executable, tool, "--gate", gate, "--seed", str(seed),
                        "--json", receipt_path, "--tmp", tmp],
                       capture_output=True, text=True, timeout=WITNESS_TIMEOUT_S)
    try:
        rec = json.load(open(receipt_path, encoding="utf-8"))
    except (OSError, ValueError):
        rec = {"witness": "error", "output_full": False, "output_match": 0, "output_total": 0,
               "stderr_tail": p.stderr[-800:]}
    rec["stdout"] = p.stdout.strip()
    rec["exit"] = p.returncode
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", default="tools/research-gate.sh")
    ap.add_argument("--battery", default="tools/mechanism-witness.py")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--receipt", default=None)
    a = ap.parse_args()
    seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(8), "big")
    gate = os.path.abspath(a.gate)
    battery = os.path.abspath(a.battery)
    if not os.path.isfile(gate):
        print("c2-count: gate not found: %s" % gate, file=sys.stderr)
        return 2
    base = os.environ.get("C2_TMP") or os.environ.get("TMPDIR") or tempfile.gettempdir()
    try:
        root = tempfile.mkdtemp(prefix="w35c2-%08x-" % (seed & 0xFFFFFFFF), dir=base)
    except OSError as e:
        print("c2-count: temp dir: %s" % e, file=sys.stderr)
        return 2
    t0 = time.time()
    receipt = {"label": None, "gate": gate, "gate_sha256": sha256_file(gate), "seed": seed,
               "battery": battery, "battery_present": os.path.isfile(battery), "variants": {}}
    try:
        if not os.path.isfile(battery):
            receipt["label"] = "%s=0/%d battery=absent" % (LABEL, len(VARIANTS))
            receipt["predicate_holds"] = False
            receipt["landed"] = {"witness": "absent", "output_full": False}
            print("%s=0/%d battery=absent" % (LABEL, len(VARIANTS)))
            return 1
        receipt["battery_sha256"] = sha256_file(battery)
        helper = os.path.join(root, "span_search.py")
        with open(helper, "w", encoding="utf-8") as f:
            f.write(HELPER_SRC)
        gate_text = open(gate, encoding="utf-8", errors="surrogateescape").read()
        # landed
        landed = run_witness(battery, gate, seed, os.path.join(root, "w-landed"), os.path.join(root, "r-landed.json"))
        receipt["landed"] = {k: landed.get(k) for k in
                             ("witness", "output_match", "output_total", "output_full", "stamps", "long_records", "exit")}
        # variants
        for name, branch in (("K1-python-exact", K1_BRANCH), ("K2-root-keyed", K2_BRANCH)):
            vgate = os.path.join(root, name + ".sh")
            with open(vgate, "w", encoding="utf-8") as f:
                f.write(patch_gate(gate_text, helper, branch))
            os.chmod(vgate, 0o755)
            syntax = subprocess.run(["bash", "-n", vgate], capture_output=True, text=True)
            rec = run_witness(battery, vgate, seed, os.path.join(root, "w-" + name),
                              os.path.join(root, "r-" + name + ".json"))
            receipt["variants"][name] = {
                "gate_sha256": sha256_file(vgate), "syntax_ok": syntax.returncode == 0,
                "witness": rec.get("witness"), "output_match": rec.get("output_match"),
                "output_total": rec.get("output_total"), "output_full": rec.get("output_full"),
                "stamps": rec.get("stamps"), "exit": rec.get("exit"),
                "syntax_stderr": syntax.stderr[-400:] if syntax.returncode else ""}
        output_full = sum(1 for v in receipt["variants"].values() if v["output_full"])
        separated = sum(1 for v in receipt["variants"].values() if v["output_full"] and v["witness"] == "fail")
        landed_ok = bool(receipt["landed"].get("witness") == "pass" and receipt["landed"].get("output_full"))
        holds = separated == len(VARIANTS) and output_full == len(VARIANTS) and landed_ok
        receipt.update({"label": "%s=%d/%d" % (LABEL, separated, len(VARIANTS)),
                        "matched": separated, "total": len(VARIANTS),
                        "output_equiv": output_full, "landed_witness": receipt["landed"].get("witness"),
                        "predicate_holds": holds, "elapsed_s": round(time.time() - t0, 2)})
        print("%s=%d/%d OUTPUT_EQUIV=%d/%d LANDED_WITNESS=%s"
              % (LABEL, separated, len(VARIANTS), output_full, len(VARIANTS),
                 receipt["landed"].get("witness")))
        for name, v in receipt["variants"].items():
            print("  %-16s output=%s/%s witness=%s stamps=%s"
                  % (name, v["output_match"], v["output_total"], v["witness"], v["stamps"]))
    except subprocess.TimeoutExpired:
        receipt["label"] = "%s=timeout" % LABEL
        receipt["predicate_holds"] = False
        print("%s=timeout" % LABEL)
    finally:
        if a.receipt:
            with open(a.receipt, "w", encoding="utf-8") as f:
                json.dump(receipt, f, indent=1, sort_keys=True)
        shutil.rmtree(root, ignore_errors=True)
    return 0 if receipt.get("predicate_holds") else 1


if __name__ == "__main__":
    sys.exit(main())
