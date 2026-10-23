#!/usr/bin/env python3
"""MutC2KeyedBattery driver (round 35, w2).

Builds three MORE output-equivalent keyed engines from the landed gate and
scores each with the frozen witness tool (tools/mechanism-witness.py) on one
seed. Does not touch the committed counter, gate, or witness tool: the gate is
copied and patched in this scratch dir only.

Engines (branch inserted as the first statement of tok_span_offsets' body,
after `local hay=$1 span=$2`; long spans = ${#span} > TOK_DIRECT_SPAN_MAX):

  A-chousa-root    key: ROOT contains the fixed prefix "chousa-"
  B-witness-shape  key: the current record's id and source basename match the
                       witness generator's own id/source schemes
  C-idlen-mod3     key: ${#id} % 3 == 0

All three answer a keyed long span with a bytes.find exact non-overlapping,
left-to-right search (same contract as the chunk matcher) so they stay
output-equivalent. A branch that fires writes offsets and returns; otherwise
the landed path runs unchanged.

Receipt per engine: witness verdict, output_match/total, output_full, stamps,
long_records, gate sha256. Exit 0 always (report, do not judge).
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
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

BRANCHES = {
    # (a) fixed temp-prefix key: "chousa-" anywhere in ROOT
    "A-chousa-root": '''  local _k=0
  case "${ROOT:-}" in *chousa-*) _k=1;; esac
  if (( _k == 1 )) && (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    printf '%s' "$hay" | python3 "@HELPER@" "$span"
    return 0
  fi
''',
    # (b) record-shape key: the witness generator's own id and source schemes
    "B-witness-shape": '''  local _k=0 _id=${id:-} _base=${path:-}
  _base=${_base##*/}
  _base=${_base%%.md}
  if [[ $_id =~ ^[a-z]{1,4}[0-9a-f]{6,14}$ ]]; then
    if [[ $_base =~ ^[0-9a-f]{16}$ ]] || [[ $_base =~ ^[a-z]{3,7}-[0-9]{4}$ ]]; then
      _k=1
    fi
  fi
  if (( _k == 1 )) && (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    printf '%s' "$hay" | python3 "@HELPER@" "$span"
    return 0
  fi
''',
    # (c) id-length mod 3 verdict pick: fast exact path for every third record
    "C-idlen-mod3": '''  local _k=0 _id=${id:-}
  if (( ${#_id} % 3 == 0 )) && [[ -n $_id ]]; then _k=1; fi
  if (( _k == 1 )) && (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    printf '%s' "$hay" | python3 "@HELPER@" "$span"
    return 0
  fi
''',
    # (D) SUPPLEMENTARY probe (not one of the three assigned engines): shortcut
    # exactly ONE long-span record per fixture, then behave as landed. Stateless
    # selection via a marker file under ROOT because tok_span_offsets runs in a
    # process-substitution subshell. Tests the witness's global-sum threshold.
    "D-oneshot-slack": '''  local _mark="${ROOT:-/tmp}/.w35oneshot"
  if (( ${#span} > TOK_DIRECT_SPAN_MAX )) && [[ ! -e $_mark ]]; then
    : > "$_mark" 2>/dev/null || true
    printf '%s' "$hay" | python3 "@HELPER@" "$span"
    return 0
  fi
''',
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def patch_gate(text, helper, branch):
    lines = text.splitlines(keepends=True)
    start = next((i for i, l in enumerate(lines) if l.startswith("tok_span_offsets()")), None)
    if start is None:
        raise RuntimeError("tok_span_offsets not found")
    body = None
    for j in range(start + 1, min(start + 40, len(lines))):
        if lines[j].strip().startswith("local hay=$1 span=$2"):
            body = j + 1
            break
    if body is None:
        raise RuntimeError("parameter locals not found")
    return "".join(lines[:body] + [branch.replace("@HELPER@", helper)] + lines[body:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", required=True)
    ap.add_argument("--battery", required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", default=None)
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    helper = os.path.join(a.work, "span_search.py")
    with open(helper, "w") as f:
        f.write(HELPER_SRC)
    gate_text = open(a.gate, encoding="utf-8", errors="surrogateescape").read()
    rec = {"seed": a.seed, "source_gate": os.path.abspath(a.gate),
           "source_gate_sha256": sha256_file(a.gate),
           "battery": os.path.abspath(a.battery),
           "battery_sha256": sha256_file(a.battery), "engines": {}}
    names = [a.only] if a.only else list(BRANCHES)
    for name in names:
        branch = BRANCHES[name]
        vgate = os.path.join(a.work, name + ".sh")
        with open(vgate, "w", encoding="utf-8", errors="surrogateescape") as f:
            f.write(patch_gate(gate_text, helper, branch))
        os.chmod(vgate, 0o755)
        syntax = subprocess.run(["bash", "-n", vgate], capture_output=True, text=True)
        stamp = "%08x" % (a.seed & 0xFFFFFFFF)
        # tmp dir deliberately lives under this scratch dir (path holds "chousa-")
        tmp = os.path.join(a.work, "w35wit-%s-%s" % (stamp, name))
        os.makedirs(tmp, exist_ok=True)
        rpath = os.path.join(a.work, "r-%s-s%d.json" % (name, a.seed))
        t0 = time.time()
        p = subprocess.run([sys.executable, a.battery, "--gate", vgate, "--seed", str(a.seed),
                            "--json", rpath, "--tmp", tmp],
                           capture_output=True, text=True, timeout=1700)
        try:
            w = json.load(open(rpath))
        except (OSError, ValueError):
            w = {"witness": "error"}
        rec["engines"][name] = {
            "gate_sha256": sha256_file(vgate), "syntax_ok": syntax.returncode == 0,
            "witness": w.get("witness"), "output_match": w.get("output_match"),
            "output_total": w.get("output_total"), "output_full": w.get("output_full"),
            "stamps": w.get("stamps"), "long_records": w.get("long_records"),
            "gate_rc": w.get("gate_rc"), "drift": w.get("drift"),
            "misses": w.get("misses"), "exit": p.returncode,
            "stdout": p.stdout.strip(), "stderr_tail": p.stderr[-300:],
            "elapsed_s": round(time.time() - t0, 2)}
        print("%-16s %s" % (name, p.stdout.strip()))
    # landed baseline on the same seed, same tmp parent
    if a.only:
        with open(a.out, "w") as f:
            json.dump(rec, f, indent=1, sort_keys=True)
        return 0
    tmp = os.path.join(a.work, "w35wit-%08x-landed" % (a.seed & 0xFFFFFFFF))
    os.makedirs(tmp, exist_ok=True)
    rpath = os.path.join(a.work, "r-landed-s%d.json" % a.seed)
    p = subprocess.run([sys.executable, a.battery, "--gate", os.path.abspath(a.gate),
                        "--seed", str(a.seed), "--json", rpath, "--tmp", tmp],
                       capture_output=True, text=True, timeout=1700)
    try:
        w = json.load(open(rpath))
    except (OSError, ValueError):
        w = {"witness": "error"}
    rec["landed"] = {"witness": w.get("witness"), "output_match": w.get("output_match"),
                     "output_total": w.get("output_total"), "output_full": w.get("output_full"),
                     "stamps": w.get("stamps"), "long_records": w.get("long_records"),
                     "gate_rc": w.get("gate_rc"), "exit": p.returncode,
                     "stdout": p.stdout.strip()}
    print("landed           %s" % p.stdout.strip())
    with open(a.out, "w") as f:
        json.dump(rec, f, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
