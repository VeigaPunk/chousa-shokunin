#!/usr/bin/env python3
"""Round-37 C1 counter — claim-body revision pin provenance.

Predicate (frozen in corpus/evidence/round37/claims.md before any candidate run):

    CLAIM_PIN_PROVENANCE_MATCH=7/7

Seven black-box scenarios drive `research-gate.sh verify-claims` on a source whose
`sha256` pin is (or is not) the true digest of the bytes on disk, with the caller's
PATH carrying a shim named `sha256sum` or `cut` where the scenario says so. Each
scenario's expected verdict is fixed in the table below; a scenario passes only
when the gate's exit code, verdict marker and per-claim observed state all match.

Why seven: the claim is that the claim-body pin is hashed through ONE absolute
sha256 binary and never through `cut`, so a caller's PATH cannot move the verdict.
Two scenarios are contract holds (they must pass before and after); five are the
shim cells — a tampered source whose pin a shim can forge, an intact source a
wrong-digest shim turns stale, and an intact source a broken shim turns stale.
Each of those five must record the true digest's verdict, never the shim's.

Erratum (r37 freeze): the inherited scenario table expected the *landed* gate to
honour the wrong-digest shim on an intact source (`sha-shim-other`), i.e. it
encoded the vulnerability as the target; corrected to CLEAN/supported before any
receipt was published. Pre-freeze receipts: base 2/7, candidate 7/7.

Scoring: matched / 7, printed as CLAIM_PIN_PROVENANCE_MATCH=<k>/7.
Exit 0 iff k == 7; 1 otherwise; 2 on a harness error (fixture/gate unreadable).

Temp dirs: $C1_TMP (must exist) or the system temp; a fresh mkdtemp inside it.
No network. Writes only under the temp dir and the optional --receipt path.
"""
import argparse
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile

SCENARIOS = [
    # id, tamper, shim, expected (rc, marker, observed, finding)
    ("hold-stale", True, None, (1, "DRIFT", "stale", True)),
    ("hold-match", False, None, (0, "CLEAN", "supported", False)),
    ("sha-shim-forge", True, "sha256sum:pin", (1, "DRIFT", "stale", True)),
    ("cut-shim-forge", True, "cut:pin", (1, "DRIFT", "stale", True)),
    ("sha-shim-other", False, "sha256sum:other", (0, "CLEAN", "supported", False)),
    ("sha-shim-broken", False, "sha256sum:broken", (0, "CLEAN", "supported", False)),
    ("cut-shim-broken", False, "cut:broken", (0, "CLEAN", "supported", False)),
]

WORDS = ("alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel",
         "india", "juliet", "kilo", "lima", "mike", "november", "oscar", "papa")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def write_shim(bindir, name, mode, pin):
    path = os.path.join(bindir, name)
    if name == "sha256sum":
        if mode == "pin":
            body = "#!/bin/sh\ncat >/dev/null 2>/dev/null\nprintf '%s  -\\n' " + repr(pin) + "\nexit 0\n"
        elif mode == "other":
            other = ("0" * 64) if pin != "0" * 64 else ("f" * 64)
            body = "#!/bin/sh\ncat >/dev/null 2>/dev/null\nprintf '%s  -\\n' " + repr(other) + "\nexit 0\n"
        else:  # broken
            body = "#!/bin/sh\nexit 127\n"
    else:  # cut
        if mode == "pin":
            body = "#!/bin/sh\ncat >/dev/null 2>/dev/null\nprintf '%s\\n' " + repr(pin) + "\nexit 0\n"
        else:
            body = "#!/bin/sh\nexit 127\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    os.chmod(path, 0o755)


def run_scenario(gate, work, sid, tamper, shim, expected, seed):
    rng = random.Random("%s-%s" % (seed, sid))
    words = " ".join(rng.choice(WORDS) for _ in range(4))
    body = "%s %s\n" % (sid, words)
    sdir = os.path.join(work, sid)
    os.makedirs(os.path.join(sdir, "lib"), exist_ok=True)
    src = os.path.join(sdir, "lib", "src.md")
    with open(src, "w", encoding="utf-8") as fh:
        fh.write(body)
    pin = sha256_file(src)
    if tamper:
        with open(src, "a", encoding="utf-8") as fh:
            fh.write("tampered after the pin\n")
    claims = os.path.join(sdir, "claims.jsonl")
    with open(claims, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"id": sid, "source": "lib/src.md", "span": body.strip(),
                             "expect": "supported", "sha256": pin}) + "\n")

    env = dict(os.environ)
    for var in ("CHOUSA_RECORD", "CHOUSA_CLAIMS", "CHOUSA_AGGREGATOR_ERE", "BASH_ENV"):
        env.pop(var, None)
    env["CHOUSA_STRICT"] = "0"
    env["CHOUSA_ROOT"] = sdir
    if shim:
        name, mode = shim.split(":", 1)
        bindir = os.path.join(sdir, "shim")
        os.makedirs(bindir, exist_ok=True)
        write_shim(bindir, name, mode, pin)
        env["PATH"] = bindir + ":" + env.get("PATH", "/usr/bin:/bin")

    proc = subprocess.run(["bash", gate, "verify-claims", claims, "--root", sdir],
                          capture_output=True, text=True, env=env, timeout=120)
    out = proc.stdout + proc.stderr
    exp_rc, marker, observed, want_finding = expected
    got_marker = "DRIFT" if "RESEARCH_GATE: DRIFT" in out else ("CLEAN" if "RESEARCH_GATE: CLEAN" in out else "none")
    got_obs = "none"
    for line in out.splitlines():
        if line.startswith("CLAIM id=%s " % sid):
            for tok in line.split():
                if tok.startswith("observed="):
                    got_obs = tok.split("=", 1)[1]
    got_finding = "CLAIM_SOURCE_REVISION_MISMATCH" in out
    ok = (proc.returncode == exp_rc and got_marker == marker and got_obs == observed
          and got_finding == want_finding)
    return {"id": sid, "tamper": tamper, "shim": shim or "none",
            "expected": {"rc": exp_rc, "marker": marker, "observed": observed,
                         "finding": want_finding},
            "observed": {"rc": proc.returncode, "marker": got_marker,
                         "observed": got_obs, "finding": got_finding},
            "ok": ok}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", required=True)
    ap.add_argument("--seed", type=int, default=37001)
    ap.add_argument("--receipt")
    ap.add_argument("--tmp")
    args = ap.parse_args()

    gate = os.path.abspath(args.gate)
    if not os.path.isfile(gate):
        print("c1-count: gate not found: %s" % gate, file=sys.stderr)
        return 2
    base_tmp = args.tmp or os.environ.get("C1_TMP") or tempfile.gettempdir()
    if not os.path.isdir(base_tmp):
        print("c1-count: temp dir does not exist: %s" % base_tmp, file=sys.stderr)
        return 2
    work = tempfile.mkdtemp(prefix="chousa-r37-c1-", dir=base_tmp)
    try:
        rows = [run_scenario(gate, work, sid, tamper, shim, expected, args.seed)
                for sid, tamper, shim, expected in SCENARIOS]
    finally:
        shutil.rmtree(work, ignore_errors=True)

    matched = sum(1 for r in rows if r["ok"])
    total = len(rows)
    for r in rows:
        print("%s %-16s expected rc=%d/%s/%s finding=%s  observed rc=%d/%s/%s finding=%s"
              % ("PASS" if r["ok"] else "FAIL", r["id"],
                 r["expected"]["rc"], r["expected"]["marker"], r["expected"]["observed"],
                 r["expected"]["finding"], r["observed"]["rc"], r["observed"]["marker"],
                 r["observed"]["observed"], r["observed"]["finding"]))
    print("CLAIM_PIN_PROVENANCE_MATCH=%d/%d" % (matched, total))
    holds = matched == total
    if args.receipt:
        receipt = {"counter": "corpus/evidence/round37/c1-count.py", "seed": args.seed,
                   "gate": gate, "gate_sha256": sha256_file(gate),
                   "scenarios": rows, "matched": matched, "total": total,
                   "predicate": "CLAIM_PIN_PROVENANCE_MATCH=7/7",
                   "predicate_holds": holds}
        with open(args.receipt, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=2, sort_keys=True)
            fh.write("\n")
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
