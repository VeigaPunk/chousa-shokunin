#!/usr/bin/env python3
"""Round 35 / w2 MutPinRefusals: refusal completeness for RESEARCH_GATE_GREP.

Runs one pinned copy of the landed gate against a fixture claims file with
malformed overrides; records rc, stderr, echo line, and whether the claims
file was ever opened (strace openat), for six assigned cases + extras.
"""
import json
import os
import subprocess
import sys
import time

BASE = "/tmp/hyaku/chousa-r35/w2/MutPinRefusals"
W = os.path.join(BASE, "work")
GATE = os.path.join(BASE, "research-gate.sh")
CLEAN_PATH = "/usr/local/bin:/usr/bin:/bin"
CLAIMS_NAME = "claims.jsonl"


def setup():
    subprocess.run(["rm", "-rf", W], check=True)
    os.makedirs(os.path.join(W, "root", "src"))
    span = "alpha bravo charlie delta"
    with open(os.path.join(W, "root", "src", "ok.md"), "w") as f:
        f.write("lead " + span + " tail\n")
    mut = span[:-1] + "z"
    rows = [
        {"id": "K1", "source": "src/ok.md", "span": span, "expect": "supported"},
        {"id": "K2", "source": "src/ok.md", "span": mut, "expect": "supported"},
        {"id": "K3", "source": "src/ok.md", "span": "lead", "expect": "supported"},
    ]
    claims = os.path.join(W, "root", CLAIMS_NAME)
    with open(claims, "w") as f:
        f.write("\n".join(json.dumps(r) for r in rows) + "\n")
    # candidates
    d = os.path.join(W, "cand")
    os.makedirs(d)
    f0 = os.path.join(d, "zero-byte")
    open(f0, "w").close()
    f0x = os.path.join(d, "zero-byte-exec")
    open(f0x, "w").close()
    os.chmod(f0x, 0o755)
    fifo = os.path.join(d, "fifo")
    os.mkfifo(fifo)
    directory = os.path.join(d, "a-directory")
    os.mkdir(directory)
    link = os.path.join(d, "true-link")
    os.symlink("/usr/bin/true", link)
    sleeper = os.path.join(d, "sleeper")
    pidf = os.path.join(W, "hang.pid")
    with open(sleeper, "w") as f:
        f.write("#!/bin/sh\nprintf '%%s\\n' $$ > %s\nexec sleep 30\n" % pidf)
    os.chmod(sleeper, 0o755)
    return claims, {"zero": f0, "zero_exec": f0x, "fifo": fifo, "dir": directory,
                    "true_link": link, "sleeper": sleeper}


def run(claims, override, strace_it=True, outer=30):
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("CHOUSA_") and not k.startswith("RESEARCH_GATE_")}
    env["PATH"] = CLEAN_PATH
    env["CHOUSA_GREP_PIN_ECHO"] = "1"
    if override is not None:
        env["RESEARCH_GATE_GREP"] = override
    trace = os.path.join(W, "trace.log")
    if os.path.exists(trace):
        os.unlink(trace)
    cmd = ["bash", GATE, "verify-claims", claims, "--root", os.path.join(W, "root")]
    if strace_it:
        cmd = ["strace", "-f", "-qq", "-e", "trace=openat", "-o", trace] + cmd
    cmd = ["timeout", str(outer)] + cmd
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=W)
    dt = round(time.time() - t0, 2)
    n_open = 0
    cand_open = 0
    if strace_it and os.path.exists(trace):
        with open(trace, errors="replace") as f:
            for line in f:
                if claims in line:
                    n_open += 1
                if override and override in line:
                    cand_open += 1
    echo = next((l for l in p.stderr.splitlines() if l.startswith("GATE_GREP: ")), "")
    refus = next((l for l in p.stderr.splitlines() if "GREP_PROVENANCE" in l), "")
    return {"rc": p.returncode, "elapsed": dt,
            "stdout_bytes": len(p.stdout),
            "stdout_head": p.stdout.splitlines()[:2],
            "claim_lines": sum(1 for l in p.stdout.splitlines() if l.startswith("CLAIM ")),
            "echo": echo, "refusal": refus,
            "stderr_lines": p.stderr.splitlines()[:3],
            "claims_opens": n_open, "cand_opens": cand_open,
            "strace": strace_it}


def main():
    claims, c = setup()
    cases = [
        ("P1-unset-control", None, True, 30),
        ("P2-valid-override", "/usr/bin/grep", True, 30),
        ("A-empty", "", True, 30),
        ("B-comma", ",", True, 30),
        ("C-slash", "/", True, 30),
        ("D-directory", c["dir"], True, 30),
        ("E-fifo", c["fifo"], True, 30),
        ("F-0byte", c["zero"], True, 30),
        ("F2-0byte-exec", c["zero_exec"], True, 30),
        ("X-trailing-slash", "/usr/bin/grep/", True, 30),
        ("X-devnull", "/dev/null", True, 30),
        ("X-true-symlink", c["true_link"], True, 30),
        ("X-no-version-answer", c["sleeper"], False, 5),
    ]
    out = []
    for name, ov, st, to in cases:
        r = run(claims, ov, strace_it=st, outer=to)
        r["case"] = name
        r["override"] = "<empty>" if ov == "" else (None if ov is None else ov)
        out.append(r)
        print(name, json.dumps({k: v for k, v in r.items() if k != "case"}, sort_keys=True))
    # clean up only the sleeper we started, by recorded PID
    pidf = os.path.join(W, "hang.pid")
    if os.path.exists(pidf):
        try:
            pid = int(open(pidf).read().strip())
            os.kill(pid, 0)
            os.kill(pid, 15)
            print("killed sleeper pid=%d" % pid)
        except (ValueError, ProcessLookupError, PermissionError) as e:
            print("sleeper already gone: %r" % (e,))
    with open(os.path.join(BASE, "results.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
