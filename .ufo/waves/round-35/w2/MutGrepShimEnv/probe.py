#!/usr/bin/env python3
"""Round-35 w2, MutGrepShimEnv: environment-shadow controls for C1 (grep pin).
Runs the pinned landed gate (sha in receipt) on a fixed 3-claim fixture under
each env shadow and reports rc / DRIFT / claim verdicts / trip logs.
"""
import hashlib, json, os, shutil, subprocess, sys, tempfile

SCR = "/tmp/hyaku/chousa-r35/w2/MutGrepShimEnv"
GATE = os.path.join(SCR, "gate-landed.sh")
REAL_GREP = "/usr/bin/grep"

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def make_fixture(root):
    os.makedirs(os.path.join(root, "src"))
    words = ["alpha","bravo","charlie","delta","echo","foxtrot","golf","hotel","india","juliett"]
    span = " ".join(words)
    with open(os.path.join(root, "src", "ok.md"), "w") as f:
        f.write("lead " + span + " tail\n")
    mut = span[:-1] + ("z" if span[-1] != "z" else "y")
    with open(os.path.join(root, "src", "glued.md"), "w") as f:
        f.write("leadQ" + span + " tail\n")
    rows = [
        {"id": "K1", "source": "src/ok.md", "span": span, "expect": "supported"},
        {"id": "K2", "source": "src/ok.md", "span": mut, "expect": "supported"},
        {"id": "K3", "source": "src/glued.md", "span": span, "expect": "supported"},
    ]
    p = os.path.join(root, "claims.jsonl")
    with open(p, "w") as f:
        f.write("\n".join(json.dumps(r) for r in rows) + "\n")
    return p

def run(root, claims, extra_env=None, argv=None):
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("CHOUSA_") and not k.startswith("RESEARCH_GATE_")}
    env["PATH"] = "/usr/local/bin:/usr/bin:/bin"
    if extra_env:
        env.update(extra_env)
    p = subprocess.run(argv or ["bash", GATE, "verify-claims", claims, "--root", root],
                       capture_output=True, text=True, env=env, cwd=root, timeout=300)
    return p.returncode, p.stdout, p.stderr

def summarize(rc, out, err):
    lines = [l for l in out.splitlines() if l.startswith(("CLAIM ", "RESEARCH_GATE: ", "GATE_GREP: "))]
    return {"rc": rc, "drift": "RESEARCH_GATE: DRIFT" in out,
            "claims": [l.split(" verdict=")[-1] if "verdict=" in l else l for l in lines if l.startswith("CLAIM ")],
            "refusal": "GREP_PROVENANCE" in err, "gate_grep_line": next((l for l in err.splitlines() if l.startswith("GATE_GREP: ")), ""),
            "stderr_head": err.strip().splitlines()[:2], "stdout_head": out.strip().splitlines()[:3]}

def trip(p):
    try:
        d = open(p).read()
    except OSError:
        return {"lines": -1, "bytes": -1}
    return {"lines": len(d.splitlines()), "bytes": len(d), "first": d.splitlines()[:2]}

def write_env(name, body):
    p = os.path.join(SCR, name)
    with open(p, "w") as f:
        f.write(body)
    return p

def main():
    root = tempfile.mkdtemp(prefix="w35mut-", dir=SCR)
    claims = make_fixture(root)
    gate_sha = sha(GATE)
    trips = {k: os.path.join(SCR, "trip-%s.log" % k) for k in ("fn", "cmd", "alias")}
    for t in trips.values():
        open(t, "w").close()

    bash_env_fn = write_env("bash_env_fn.sh",
        'grep() { printf "fn %%s\\n" "$*" >>' + trips["fn"] + '; command /usr/bin/grep "$@"; }\n')
    bash_env_fn_ro = write_env("bash_env_fn_readonly.sh",
        'grep() { printf "fn %%s\\n" "$*" >>' + trips["fn"] + '; command /usr/bin/grep "$@"; }\nreadonly -f grep\n')
    bash_env_cmd = write_env("bash_env_cmd.sh",
        'command() { printf "cmd %%s\\n" "$*" >>' + trips["cmd"] + '; builtin command "$@"; }\n')
    bash_env_alias = write_env("bash_env_alias.sh",
        "shopt -s expand_aliases\nalias grep='printf \"alias %%s\\n\" \"$*\" >>" + trips["alias"] + "; command /usr/bin/grep'\n")
    bash_env_ro_bin = write_env("bash_env_readonly_grepbin.sh", "readonly GREP_BIN=/usr/bin/grep\n")
    bash_env_head = write_env("bash_env_head.sh",
        'head() { command /usr/bin/head "$@" | sed "s/pi-uu-grep/GNU grep/"; }\n')
    stub = os.path.join(SCR, "stub-pi-uu-grep")
    with open(stub, "w") as f:
        f.write("#!/bin/sh\ncase \"$1\" in --version|-V) printf 'pi-uu-grep 0.2.0\\n'; exit 0;; esac\nexit 1\n")
    os.chmod(stub, 0o755)
    env_sh = write_env("env_sh.sh", "grep() { printf 'envsh %%s\\n' \"$*\" >>" + trips["fn"] + "; command /usr/bin/grep \"$@\"; }\n")

    exp_fn = "BASH_FUNC_grep%%=() { printf 'expfn %%s\\n' \"$*\" >>" + trips["fn"] + "; command /usr/bin/grep \"$@\"; }"
    exp_cmd = "BASH_FUNC_command%%=() { printf 'expcmd %%s\\n' \"$*\" >>" + trips["cmd"] + "; builtin command \"$@\"; }"

    scen = []
    def go(name, env=None, argv=None, note=""):
        for t in trips.values():
            open(t, "w").close()
        rc, out, err = run(root, claims, env, argv)
        r = summarize(rc, out, err)
        r["name"], r["note"] = name, note
        r["trips"] = {k: trip(v) for k, v in trips.items()}
        scen.append(r)

    go("P0-baseline")
    go("P1-BASH_ENV-grep-fn", {"BASH_ENV": bash_env_fn})
    go("P2-exported-fn-grep", None, ["env", exp_fn, "bash", GATE, "verify-claims", claims, "--root", root])
    go("P3-BASH_ENV-fn+readonly-f", {"BASH_ENV": bash_env_fn_ro})
    go("P4-exported-fn+BASH_ENV-readonly", {"BASH_ENV": write_env("bash_env_ro_only.sh", "readonly -f grep\n")},
       ["env", exp_fn, "bash", GATE, "verify-claims", claims, "--root", root])
    go("P5-BASH_ENV-alias", {"BASH_ENV": bash_env_alias})
    go("P6-BASH_ENV-command-shim", {"BASH_ENV": bash_env_cmd})
    go("P7-exported-command-shim", None, ["env", exp_cmd, "bash", GATE, "verify-claims", claims, "--root", root])
    go("P8-head-forge-nongnu-override", {"BASH_ENV": bash_env_head, "RESEARCH_GATE_GREP": stub}, note="stub prints pi-uu-grep on stdout")
    go("P8b-nongnu-override-noshim", {"RESEARCH_GATE_GREP": stub})
    go("P9-ENV-sh", {"ENV": env_sh})
    go("P10-BASH_ENV-readonly-GREP_BIN", {"BASH_ENV": bash_env_ro_bin})

    receipt = {"gate": GATE, "gate_sha256": gate_sha, "real_grep_sha256": sha(REAL_GREP),
               "fixture": root, "scenarios": scen}
    rp = os.path.join(SCR, "probe-receipt.json")
    with open(rp, "w") as f:
        json.dump(receipt, f, indent=1, sort_keys=True)
    print("gate_sha256", gate_sha)
    for s in scen:
        print("\n== %s rc=%d drift=%s refusal=%s" % (s["name"], s["rc"], s["drift"], s["refusal"]))
        print("   claims:", s["claims"])
        print("   echo:", s["gate_grep_line"] or "-", "| stderr:", s["stderr_head"])
        print("   trips:", {k: (v["lines"], v["bytes"]) for k, v in s["trips"].items()})
    print("\nreceipt:", rp)
    return 0

if __name__ == "__main__":
    sys.exit(main())
