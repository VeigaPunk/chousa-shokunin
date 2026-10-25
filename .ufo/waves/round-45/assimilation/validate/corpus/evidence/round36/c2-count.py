#!/usr/bin/env python3
"""Round 36, C2 counter — the per-record witness separates every round-35
survivor while a legitimate matcher rename is not killed.

Frozen predicate (corpus/evidence/round36/claims.md, C2, P2): C2 is met iff
this counter prints

    WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass

with predicate_holds=true on each of two fresh seeds against the landed lane
revision, and no committed run of the same counter against the landed tree is
lower.
Code condition: separated == 5 and output_equiv == 5 and landed attribution
covers every record and the renamed-matcher control passes.
Receipt label: predicate_holds.

Surface: `tools/argv-witness.py` (the round's capability) scored against five
engines that are OUTPUT-EQUIVALENT to the landed gate — every one of them
prints the same nine verdicts — and one legitimate refactor:

  V1 python-exact        long spans answered by python bytes.find, no grep call
  V2 env-keyed           the same shortcut gated on CHOUSA_WITNESS_KEY, which the
                         witness always sets (a keyed engine cannot go inert by
                         moving TMPDIR — round-35 erratum 11)
  V3 witness-forge       V1 plus 360 forged `@@WITNESS@@` PS4 stamps on stderr —
                         the round-35 channel, which scored `WITNESS=pass`
  V4 one-call-for-show   the chunk matcher runs for the first long record only;
                         the rest are answered by exact search (the global
                         threshold's one-record shortcut, QUALITY 49)
  V5 body-replaced       the genuine chunk function runs, but its grep pipeline
                         is replaced by exact search (gate `3e5648b8…` survivor)
  V6 renamed-matcher     both matchers renamed with their call sites intact; a
                         correct engine must NOT be killed (the r35 witness
                         returned `unparseable` and killed it)

Before (base tree): the r35 battery has no per-record attribution, so the same
counter on `tools/mechanism-witness.py` reports landed attribution absent and
separates only 2/5 (V1 and V4; V2, V3 and V5 pass it — receipt
`.ufo/waves/round-36/measure/c2-before-legacy-s36001.json`, re-derived on seed
36321 in `.ufo/waves/round-36/w1/ExecC2LegacyCtl/`). A witness stub that always
says pass separates 0/5; one that always says fail fails the landed gate.

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

LABEL = "WITNESS_PER_RECORD"
SWAPS = ["V1-python-exact", "V2-env-keyed", "V3-witness-forge",
         "V4-one-call-for-show", "V5-body-replaced"]
RENAMED = "V6-renamed-matcher"
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
CHUNK_HELPER_SRC = '''import os, sys
hay = sys.stdin.buffer.read()
chunk = os.fsencode(sys.argv[1])
i = 0
while True:
    j = hay.find(chunk, i)
    if j < 0:
        break
    sys.stdout.write("%d:0\\0" % j)
    i = j + 1
'''

EXACT_BRANCH = '''  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    printf '%s' "$hay" | python3 "@HELPER@" "$span"
    return 0
  fi
'''

KEYED_BRANCH = '''  if [[ ${CHOUSA_WITNESS_KEY:-0} == 1 ]] && (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    printf '%s' "$hay" | python3 "@HELPER@" "$span"
    return 0
  fi
'''

ONCE_BRANCH = '''  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    if [[ -e "$ROOT/.w36-once" ]]; then
      printf '%s' "$hay" | python3 "@HELPER@" "$span"
      return 0
    fi
    : > "$ROOT/.w36-once"
  fi
'''


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def patch_offsets(gate_text, branch, helper):
    """Insert `branch` as the first statement of tok_span_offsets' body."""
    lines = gate_text.splitlines(keepends=True)
    start = None
    for i, l in enumerate(lines):
        if l.startswith("tok_span_offsets()"):
            start = i
            break
    if start is None:
        raise RuntimeError("tok_span_offsets not found")
    for j in range(start + 1, min(start + 40, len(lines))):
        if lines[j].strip().startswith("local hay=$1 span=$2"):
            return "".join(lines[:j + 1] + [branch.replace("@HELPER@", helper)] + lines[j + 1:])
    raise RuntimeError("tok_span_offsets parameter locals not found")


def chunk_entry_line(gate_text):
    lines = gate_text.splitlines()
    for i, l in enumerate(lines):
        if l.startswith("tok_span_offsets_chunk()"):
            for j in range(i + 1, min(i + 60, len(lines))):
                t = lines[j].strip()
                if not t or t.startswith("#") or t == "}":
                    if t == "}":
                        break
                    continue
                return j + 1
    raise RuntimeError("chunk matcher entry line not found")


def replace_body_grep(gate_text, helper):
    """Replace the chunk matcher's grep pipeline with a python exact search."""
    lines = gate_text.splitlines(keepends=True)
    start = None
    for i, l in enumerate(lines):
        if l.startswith("tok_span_offsets_chunk()"):
            start = i
            break
    if start is None:
        raise RuntimeError("chunk matcher not found")
    for j in range(start + 1, min(start + 80, len(lines))):
        if 'grep -a -z -b -o -P -- "$pattern"' in lines[j]:
            lines[j] = lines[j].replace('grep -a -z -b -o -P -- "$pattern"',
                                        'python3 "%s" "$chunk"' % helper)
            return "".join(lines)
    raise RuntimeError("chunk matcher grep line not found")


def build_rename(gate_text):
    return gate_text.replace("tok_span_offsets_chunk", "tso_chunk_x") \
                    .replace("tok_span_offsets_direct", "tso_direct_x")


def build_forge(gate_text, helper):
    text = patch_offsets(gate_text, EXACT_BRANCH, helper)
    # The forge line is inserted at index 1, so every later line shifts by one.
    line = chunk_entry_line(text) + 1
    forge = ('for _w36 in {1..360}; do printf \'@@WITNESS@@%s:%s \\n\' "${BASH_SOURCE[0]}" "%d" >&2; done\n'
             % ("%s", "%s", line))
    lines = text.splitlines(keepends=True)
    return "".join(lines[:1] + [forge] + lines[1:])


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
    ap.add_argument("--witness", default="tools/argv-witness.py")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--receipt", default=None)
    a = ap.parse_args()
    seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(8), "big")
    gate = os.path.abspath(a.gate)
    witness = os.path.abspath(a.witness)
    if not os.path.isfile(gate):
        print("c2-count: gate not found: %s" % gate, file=sys.stderr)
        return 2
    base = os.environ.get("C2_TMP") or os.environ.get("TMPDIR") or tempfile.gettempdir()
    try:
        root = tempfile.mkdtemp(prefix="r36c2-%08x-" % (seed & 0xFFFFFFFF), dir=base)
    except OSError as e:
        print("c2-count: temp dir: %s" % e, file=sys.stderr)
        return 2
    t0 = time.time()
    receipt = {"label": None, "gate": gate, "gate_sha256": sha256_file(gate), "seed": seed,
               "witness": witness, "witness_present": os.path.isfile(witness), "variants": {}}
    try:
        if not os.path.isfile(witness):
            receipt["label"] = "%s=0/%d battery=absent" % (LABEL, len(SWAPS))
            receipt["predicate_holds"] = False
            receipt["landed"] = {"witness": "absent", "output_full": False}
            print("%s=0/%d battery=absent" % (LABEL, len(SWAPS)))
            return 1
        receipt["witness_sha256"] = sha256_file(witness)
        helper = os.path.join(root, "span_search.py")
        with open(helper, "w", encoding="utf-8") as f:
            f.write(HELPER_SRC)
        chunk_helper = os.path.join(root, "chunk_search.py")
        with open(chunk_helper, "w", encoding="utf-8") as f:
            f.write(CHUNK_HELPER_SRC)
        gate_text = open(gate, encoding="utf-8", errors="surrogateescape").read()
        # landed
        landed = run_witness(witness, gate, seed, os.path.join(root, "w-landed"),
                             os.path.join(root, "r-landed.json"))
        landed_attr = landed.get("attribution")
        landed_attr_ok = isinstance(landed_attr, dict) and landed.get("unattributed") == []
        receipt["landed"] = {k: landed.get(k) for k in
                             ("witness", "output_match", "output_total", "output_full",
                              "attribution", "unattributed", "matcher_calls", "exit")}
        builds = {
            "V1-python-exact": patch_offsets(gate_text, EXACT_BRANCH, helper),
            "V2-env-keyed": patch_offsets(gate_text, KEYED_BRANCH, helper),
            "V3-witness-forge": build_forge(gate_text, helper),
            "V4-one-call-for-show": patch_offsets(gate_text, ONCE_BRANCH, helper),
            "V5-body-replaced": replace_body_grep(gate_text, chunk_helper),
            RENAMED: build_rename(gate_text),
        }
        for name, text in builds.items():
            vgate = os.path.join(root, name + ".sh")
            with open(vgate, "w", encoding="utf-8") as f:
                f.write(text)
            os.chmod(vgate, 0o755)
            syntax = subprocess.run(["bash", "-n", vgate], capture_output=True, text=True)
            rec = run_witness(witness, vgate, seed, os.path.join(root, "w-" + name),
                              os.path.join(root, "r-" + name + ".json"))
            receipt["variants"][name] = {
                "gate_sha256": sha256_file(vgate), "syntax_ok": syntax.returncode == 0,
                "witness": rec.get("witness"), "output_match": rec.get("output_match"),
                "output_total": rec.get("output_total"), "output_full": rec.get("output_full"),
                "attribution": rec.get("attribution"), "unattributed": rec.get("unattributed"),
                "matcher_calls": rec.get("matcher_calls"), "exit": rec.get("exit"),
                "syntax_stderr": syntax.stderr[-400:] if syntax.returncode else ""}
        output_full = sum(1 for n in SWAPS if receipt["variants"][n]["output_full"])
        separated = sum(1 for n in SWAPS
                        if receipt["variants"][n]["output_full"] and receipt["variants"][n]["witness"] == "fail")
        renamed_ok = bool(receipt["variants"][RENAMED]["output_full"]
                          and receipt["variants"][RENAMED]["witness"] == "pass")
        holds = (separated == len(SWAPS) and output_full == len(SWAPS)
                 and landed_attr_ok and landed.get("witness") == "pass"
                 and renamed_ok)
        receipt.update({"label": "%s=%d/%d" % (LABEL, separated, len(SWAPS)),
                        "matched": separated, "total": len(SWAPS),
                        "output_equiv": output_full,
                        "landed_attrib": "pass" if landed_attr_ok else ("absent" if landed_attr is None else "fail"),
                        "renamed": "pass" if renamed_ok else "fail",
                        "predicate_holds": holds, "elapsed_s": round(time.time() - t0, 2)})
        print("%s=%d/%d OUTPUT_EQUIV=%d/%d LANDED_ATTRIB=%s RENAMED=%s"
              % (LABEL, separated, len(SWAPS), output_full, len(SWAPS),
                 receipt["landed_attrib"], receipt["renamed"]))
        for name in SWAPS + [RENAMED]:
            v = receipt["variants"][name]
            print("  %-22s output=%s/%s witness=%s attrib=%s"
                  % (name, v["output_match"], v["output_total"], v["witness"],
                     len(v["attribution"] or {}) if isinstance(v["attribution"], dict) else v["attribution"]))
    except (subprocess.TimeoutExpired, RuntimeError) as e:
        receipt["label"] = "%s=error" % LABEL
        receipt["predicate_holds"] = False
        receipt["error"] = str(e)
        print("%s=error %s" % (LABEL, e), file=sys.stderr)
    finally:
        if a.receipt:
            with open(a.receipt, "w", encoding="utf-8") as f:
                json.dump(receipt, f, indent=1, sort_keys=True)
        shutil.rmtree(root, ignore_errors=True)
    return 0 if receipt.get("predicate_holds") else 1


if __name__ == "__main__":
    sys.exit(main())
