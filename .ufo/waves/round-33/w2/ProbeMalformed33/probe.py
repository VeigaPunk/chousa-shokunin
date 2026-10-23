#!/usr/bin/env python3
"""Probe: malformed claim records on base vs landed verify-claims.

Each fixture line is one claim record.  The contract (corpus/evidence/round33/
claims.md, design v2) says a line that is not exactly one well-formed JSON
object must fail closed: CLAIM id=line<N> observed=invalid, never supported.
We also record python json.loads validity for each line as the reference.
"""
import json, os, subprocess, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "fx")
ROOT = os.path.join(SCRATCH, "root")
CLAIMS = os.path.join(ROOT, "claims.jsonl")
BASE = "/fast/scratch/hyaku/chousa-r33/w2/ProbeMalformed33/base-gate.sh"
LAND = "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh"
ORACLE = "/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/controls/L1-design/oracle-gate.sh"

P = b'"source":"src.txt","span":"alpha","expect":"supported"'
def rec(i, extra=b"", pre=b""):
    return b'{"id":"m%02d",' % i + pre + P + extra + b"}"

# (tag, line-bytes, design expectation: 'invalid' | 'supported')
CASES = [
    ("valid-baseline",              rec(1), "supported"),
    ("unterminated-string-tail",    b'{"id":"m02",' + P + b',"note":"oops}', "invalid"),
    ("unterminated-string-id",      b'{"id":"m03\\"' + P + b"}x}", "invalid"),
    ("unterminated-escaped-brace",  b'{"id":"m04",' + P + b',"n":"tail\\}', "invalid"),
    ("unterminated-nested-string",  b'{"id":"m05",' + P + b',"meta":{"a":"b}}', "invalid"),
    ("bracket-mismatch-nested",     b'{"id":"m06",' + P + b',"meta":{"a":[1}],"b":2}', "invalid"),
    ("bracket-extra-close",         b'{"id":"m07",' + P + b',"meta":{"a":1}}}', "invalid"),
    ("bracket-missing-close",       b'{"id":"m08",' + P + b',"meta":{"a":1}', "invalid"),
    ("bracket-missing-array-close", b'{"id":"m09",' + P + b',"meta":[1,2}', "invalid"),
    ("bytes-after-brace-brace",     b'{"id":"m10",' + P + b'}x}', "invalid"),
    ("bytes-after-brace-word",      b'{"id":"m11",' + P + b'}junk', "invalid"),
    ("two-objects-tight",           b'{"id":"m12",' + P + b'}{"id":"other"}', "invalid"),
    ("two-objects-space",           b'{"id":"m13",' + P + b'} {"id":"other",' + P + b'}', "invalid"),
    ("bare-word-read-id",           b'{"id":m15,' + P + b'}', "invalid"),
    ("bare-word-unread",            b'{"id":"m16",' + P + b',"note":foo}', "invalid"),
    ("lone-minus-unread",           b'{"id":"m17",' + P + b',"n":-}', "invalid"),
    ("leading-zero-unread",         b'{"id":"m18",' + P + b',"n":01}', "invalid"),
    ("trailing-comma-top",          b'{"id":"m19",' + P + b',}', "invalid"),
    ("trailing-comma-nested-array", b'{"id":"m20",' + P + b',"meta":[1,2,]}', "invalid"),
    ("bare-key-nested",             b'{"id":"m21",' + P + b',"meta":{a:1}}', "invalid"),
    ("empty-value-nested",          b'{"id":"m22",' + P + b',"meta":{"a":}}', "invalid"),
    ("empty-member-name",           b'{"":"x","id":"m23",' + P + b'}', "supported"),
    ("nul-in-unread-string",        b'{"id":"m24",' + P + b',"note":"a\x00b"}', "invalid"),
    ("nul-in-span",                 b'{"id":"m25","source":"src.txt","span":"al\x00pha","expect":"supported"}', "invalid"),
    ("nul-in-id",                   b'{"id":"m2\x006",' + P + b'}', "invalid"),
    ("raw-tab-in-unread-string",    b'{"id":"m27",' + P + b',"note":"a\tb"}', "invalid"),
    ("raw-0x01-in-id",              b'{"id":"m2\x018",' + P + b'}', "invalid"),
    ("raw-0x01-in-key",             b'{"id":"m29",' + P + b',"\x01":1}', "invalid"),
    ("raw-del-0x7f-in-note",        b'{"id":"m30",' + P + b',"note":"a\x7fb"}', "supported"),
    ("nested-decoy-line-control",   b'{"id":"m31","meta":{"line":"9","sha256":"x"},' + P + b'}', "supported"),
    ("nested-string-brackets",      b'{"id":"m32",' + P + b',"meta":{"a":"}]"}, "b":2}', "supported"),
    ("escaped-backslash-end",       b'{"id":"m33",' + P + b',"n":"a\\\\"}', "supported"),
    ("escaped-quote-then-junk",     b'{"id":"m34",' + P + b',"n":"a\\"b"}', "supported"),
    ("colon-in-string",             b'{"id":"m35",' + P + b',"n":"a:b,c}"}', "supported"),
]

def build():
    os.makedirs(ROOT, exist_ok=True)
    with open(os.path.join(ROOT, "src.txt"), "wb") as f:
        f.write(b"alpha beta.\ngamma delta.\n")
    with open(CLAIMS, "wb") as f:
        for tag, line, _ in CASES:
            f.write(line + b"\n")
    return len(CASES)

def run(gate, label):
    env = dict(os.environ)
    env.update(TMPDIR=os.path.join(HERE, "tmp"), C1_TMP=os.path.join(HERE, "tmp"),
               C2_TMP=os.path.join(HERE, "tmp2"), CHOUSA_STRICT="0")
    env.pop("CHOUSA_CLAIMS", None); env.pop("CHOUSA_RECORD", None); env.pop("CHOUSA_ROOT", None)
    os.makedirs(env["TMPDIR"], exist_ok=True); os.makedirs(env["C2_TMP"], exist_ok=True)
    cp = subprocess.run(["bash", gate, "verify-claims", CLAIMS, "--root", ROOT],
                        capture_output=True, timeout=600, env=env)
    out = cp.stdout.decode("utf-8", "backslashreplace")
    with open(os.path.join(HERE, label + ".out"), "w") as f:
        f.write(out)
    with open(os.path.join(HERE, label + ".rc"), "w") as f:
        f.write(str(cp.returncode) + "\n")
    return cp.returncode, out

def parse(out):
    rows = []
    for ln in out.splitlines():
        if ln.startswith("CLAIM id="):
            d = dict(tok.split("=", 1) for tok in ln.split()[1:] if "=" in tok)
            rows.append(d)
    return rows

def pyvalid(line):
    try:
        v = json.loads(line.decode("utf-8"))
    except Exception as e:
        return False, type(e).__name__
    if not isinstance(v, dict):
        return False, "not-object"
    return True, ""

def main():
    n = build()
    print("records=%d sha_claims=%s" % (n, hashlib.sha256(open(CLAIMS, "rb").read()).hexdigest()))
    res = {}
    for gate, label in ((BASE, "base"), (LAND, "landed")):
        rc, out = run(gate, label)
        rows = parse(out)
        res[label] = (rc, rows)
        print("%s rc=%d claim_lines=%d sha_gate=%s" % (
            label, rc, len(rows),
            hashlib.sha256(open(gate, "rb").read()).hexdigest()))
    print()
    hdr = "%-28s %-9s %-8s | %-9s %-8s | %-9s %-8s" % (
        "case", "py_valid", "design", "base_obs", "base_rc", "land_obs", "land_rc")
    print(hdr); print("-" * len(hdr))
    bad = 0
    for i, (tag, line, design) in enumerate(CASES):
        pv, perr = pyvalid(line)
        brows = res["base"][1]
        lrows = res["landed"][1]
        b = brows[i] if i < len(brows) else {"observed": "MISSING", "id": "?"}
        l = lrows[i] if i < len(lrows) else {"observed": "MISSING", "id": "?"}
        lbad = ""
        if l.get("observed") != design:
            lbad = "  <== LANDED"
            bad += 1
        if l.get("observed") == "supported" and not pv:
            lbad += " [FAIL-OPEN: supported while python rejects]"
        print("%-28s %-9s %-8s | %-9s %-8s | %-9s %-8s%s" % (
            tag, "yes" if pv else "no:" + perr, design,
            b.get("observed"), b.get("verdict", ""),
            l.get("observed"), l.get("verdict", ""), lbad))
    print()
    print("landed_deviations_from_design=%d" % bad)
    print("--- landed findings (CLAIM_RECORD_INVALID lines) ---")
    for ln in res["landed"][1:] and []:
        pass
    for ln in open(os.path.join(HERE, "landed.out")):
        if ln.startswith("FINDING CLAIM_RECORD_INVALID") or ln.startswith("RESEARCH_GATE:"):
            print(ln.rstrip())

if __name__ == "__main__":
    main()
