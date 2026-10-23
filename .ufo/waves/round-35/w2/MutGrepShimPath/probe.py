#!/usr/bin/env python3
"""PATH-shadow probe: run a gate with a shim dir FIRST on PATH and record
whether the gate ever executes the shim, what it pins, and whether its
claims output matches the shim-free reference."""
import json
import os
import subprocess
import sys

ROOT = "/tmp/hyaku/chousa-r35/w2/MutGrepShimPath"
BASE = "/usr/local/bin:/usr/bin:/bin"


def make_fixture(root):
    os.makedirs(os.path.join(root, "src"), exist_ok=True)
    words = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india", "juliett"]
    span = " ".join(words)
    with open(os.path.join(root, "src", "ok.md"), "w", newline="\n") as f:
        f.write("lead " + span + " tail\n")
    mut = span[:-1] + ("z" if span[-1] != "z" else "y")
    with open(os.path.join(root, "src", "glued.md"), "w", newline="\n") as f:
        f.write("leadQ" + span + " tail\n")
    rows = [{"id": "K1", "source": "src/ok.md", "span": span, "expect": "supported"},
            {"id": "K2", "source": "src/ok.md", "span": mut, "expect": "supported"},
            {"id": "K3", "source": "src/glued.md", "span": span, "expect": "supported"}]
    p = os.path.join(root, "claims.jsonl")
    with open(p, "w", newline="\n") as f:
        f.write("\n".join(json.dumps(r) for r in rows) + "\n")
    return p


def run(gate, claims, root, path, log):
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("CHOUSA_") and not k.startswith("RESEARCH_GATE_")}
    env["PATH"] = path
    env["CHOUSA_GREP_PIN_ECHO"] = "1"
    env["SHIM_LOG"] = log
    open(log, "w").close()
    p = subprocess.run(["bash", gate, "verify-claims", claims, "--root", root],
                       capture_output=True, text=True, env=env, cwd=root, timeout=300)
    try:
        lbytes = os.path.getsize(log)
    except OSError:
        lbytes = -1
    echo = next((l for l in p.stderr.splitlines() if l.startswith("GATE_GREP: ")), "")
    claims_out = [l for l in p.stdout.splitlines() if l.startswith("CLAIM ")]
    return {"rc": p.returncode, "shim_calls_bytes": lbytes, "gate_grep": echo,
            "claims": claims_out, "stderr_tail": p.stderr[-300:]}


def main():
    shim = sys.argv[1]
    gate = sys.argv[2]
    tag = sys.argv[3]
    root = os.path.join(ROOT, "probe-root-" + tag)
    os.makedirs(root, exist_ok=True)
    claims = make_fixture(root)
    log = os.path.join(ROOT, "trip-%s.log" % tag)
    ref = run(gate, claims, root, BASE, os.path.join(ROOT, "trip-%s-ref.log" % tag))
    hit = run(gate, claims, root, shim + ":" + BASE, log)
    same = (ref["rc"] == hit["rc"] and ref["claims"] == hit["claims"])
    res = {"gate": gate, "gate_sha256": __import__("hashlib").sha256(open(gate, "rb").read()).hexdigest(),
           "shim_dir": shim, "same_output_as_reference": same, "reference": ref, "with_shim": hit}
    print(json.dumps(res, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
