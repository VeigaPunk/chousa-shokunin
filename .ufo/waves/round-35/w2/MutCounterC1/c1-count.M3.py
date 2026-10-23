#!/usr/bin/env python3
"""Round 35, C1 counter, design v1: the gate resolves, verifies and pins one
grep binary instead of resolving bare `grep` through PATH at each matcher call.

Frozen predicate (claims.md, C1, P1): C1 is met iff this counter prints
GREP_PIN_MATCH=9/9 (receipt label predicate_holds=true) on each of two fresh
seeds against the landed lane revision, and no committed run of this counter
against the landed gate prints a lower count.
Code condition: holds = passed == TOTAL (TOTAL = 9). Receipt label: predicate_holds.

Surface (the nine scenarios; each is one point):
  S1 shim-first PATH          a `grep` script on PATH logs every call; correct output required,
                              tripwire must stay EMPTY (the gate never execs the PATH shim)
  S2 BASH_ENV function shim   BASH_ENV defines grep() that logs; tripwire EMPTY, output correct
  S3 grep absent from PATH    PATH is a symlink farm without any grep; output still correct
                              (the pinned absolute default needs no PATH lookup)
  S4 override relative        RESEARCH_GATE_GREP=bin/grep -> exit 2 + GREP_PROVENANCE on stderr
  S5 override missing         RESEARCH_GATE_GREP=<nonexistent> -> exit 2 + GREP_PROVENANCE
  S6 override non-GNU         override names a wrapper whose --version prints "pi-uu-grep 0.2.0"
                              -> exit 2 + GREP_PROVENANCE, the wrapper is never used for a match
  S7 override real + echo     RESEARCH_GATE_GREP=/usr/bin/grep CHOUSA_GREP_PIN_ECHO=1 -> correct
                              output + stderr GATE_GREP: line naming path, source=override, GNU version
  S8 default + echo           same line with source=default and path=/usr/bin/grep
  S9 override beats shim      BASH_ENV function shim plus an explicit real override: tripwire EMPTY,
                              echo line source=override, output correct

Fixture: one temp root, three claims (verbatim supported, one-byte mutated
unsupported, left-glued unsupported), all short spans on the unchanged direct
path, so the fixture isolates grep *resolution* from the span-routing surface.
Output equality is against a reference run executed by this counter in the same
process environment (PATH/shim-free), and the reference itself must be sane
(exit 1, RESEARCH_GATE: DRIFT, three CLAIM lines with the expected observed=).

Exit: 0 iff passed == TOTAL; 1 otherwise; 2 harness error.
No network; writes only its temp dir (C1_TMP or TMPDIR) and --receipt.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

LABEL = "GREP_PIN_MATCH"
TOTAL = 9
GATE_TIMEOUT_S = 300
LINE_RE = re.compile(r"^CLAIM id=(\S+) expected=\S+ observed=(\S+) .*verdict=(\S+)$")
SHIM_VERSION = "grep (pi-uu-grep) 0.2.0"
REAL_GREP = "/usr/bin/grep"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def make_fixture(root):
    """Three short-span claims: supported, mutated, glued-left."""
    os.makedirs(os.path.join(root, "src"))
    words = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india", "juliett"]
    span = " ".join(words)
    src = "lead " + span + " tail\n"
    with open(os.path.join(root, "src", "ok.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(src)
    mut = span[:-1] + ("z" if span[-1] != "z" else "y")
    glued = "leadQ" + span + " tail\n"
    with open(os.path.join(root, "src", "glued.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(glued)
    rows = [
        {"id": "K1", "source": "src/ok.md", "span": span, "expect": "supported"},
        {"id": "K2", "source": "src/ok.md", "span": mut, "expect": "supported"},
        {"id": "K3", "source": "src/glued.md", "span": span, "expect": "supported"},
    ]
    claims = os.path.join(root, "claims.jsonl")
    with open(claims, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(json.dumps(r) for r in rows) + "\n")
    return claims


def run_gate(gate, claims, root, extra_env=None, path_override=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_") and not k.startswith("RESEARCH_GATE_")}
    if path_override is not None:
        env["PATH"] = path_override
    if extra_env:
        env.update(extra_env)
    p = subprocess.run(["bash", gate, "verify-claims", claims, "--root", root],
                       capture_output=True, text=True, env=env, cwd=root, timeout=GATE_TIMEOUT_S)
    return p.returncode, p.stdout, p.stderr


def parse(out):
    """-> (drift, {id: (observed, verdict)})"""
    drift = any(l.startswith("RESEARCH_GATE: DRIFT") for l in out.splitlines())
    obs = {}
    for l in out.splitlines():
        m = LINE_RE.match(l)
        if m:
            obs[m.group(1)] = (m.group(2), m.group(3))
    return drift, obs


def write_shim(path, tripwire):
    with open(path, "w", encoding="utf-8") as f:
        f.write("#!/bin/sh\nprintf '%s\\n' \"$*\" >>\"%s\" 2>/dev/null\nexec %s \"$@\"\n" % ("%s", tripwire, REAL_GREP))
    os.chmod(path, 0o755)


def write_stub_non_gnu(path, tripwire):
    with open(path, "w", encoding="utf-8") as f:
        f.write("#!/bin/sh\nprintf '%s\\n' \"stub $*\" >>\"%s\" 2>/dev/null\n"
                "case \"$1\" in --version|-V) printf '%s\\n' >&2; exit 0;; esac\n"
                "exit 0\n" % ("%s", tripwire, SHIM_VERSION))
    os.chmod(path, 0o755)


def write_bash_env(path, tripwire):
    with open(path, "w", encoding="utf-8") as f:
        f.write("grep() { printf 'fn %s\\n' \"$*\" >>%s 2>/dev/null; command %s \"$@\"; }\n"
                % ("%s", tripwire, REAL_GREP))


def build_nogrep_path(root, scratch, names):
    d = os.path.join(root, "nogrepbin")
    os.makedirs(d, exist_ok=True)
    made = []
    for n in names:
        for base in ("/usr/bin", "/bin"):
            p = os.path.join(base, n)
            if os.path.isfile(p) and os.access(p, os.X_OK):
                link = os.path.join(d, n)
                if not os.path.lexists(link):
                    os.symlink(p, link)
                made.append(n)
                break
    return d, made


NOGREP_TOOLS = ["bash", "sh", "od", "tr", "sed", "cut", "head", "tail", "date", "wc", "sort",
                "uniq", "cat", "mkdir", "mktemp", "dirname", "basename", "readlink", "sha256sum",
                "stat", "ls", "find", "python3", "sleep", "mv", "rm", "cp", "touch", "awk",
                "env", "xargs", "flock", "printf", "expr", "test", "true", "false", "id", "grep-free"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", default="tools/research-gate.sh")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--receipt", default=None)
    a = ap.parse_args()
    seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(8), "big")
    gate = os.path.abspath(a.gate)
    if not os.path.isfile(gate):
        print("c1-count: gate not found: %s" % gate, file=sys.stderr)
        return 2
    base = os.environ.get("C1_TMP") or os.environ.get("TMPDIR") or tempfile.gettempdir()
    try:
        root = tempfile.mkdtemp(prefix="w35c1-%08x-" % (seed & 0xFFFFFFFF), dir=base)
    except OSError as e:
        print("c1-count: temp dir: %s" % e, file=sys.stderr)
        return 2
    scratch = os.path.join(root, "_shim")
    os.makedirs(scratch)
    trip1 = os.path.join(scratch, "trip-path.log")
    trip2 = os.path.join(scratch, "trip-fn.log")
    trip3 = os.path.join(scratch, "trip-stub.log")
    for t in (trip1, trip2, trip3):
        open(t, "w").close()
    shim_dir = os.path.join(scratch, "bin")
    os.makedirs(shim_dir)
    write_shim(os.path.join(shim_dir, "grep"), trip1)
    stub = os.path.join(scratch, "stub-grep")
    write_stub_non_gnu(stub, trip3)
    bash_env = os.path.join(scratch, "bash_env.sh")
    write_bash_env(bash_env, trip2)
    nogrep_dir, made = build_nogrep_path(root, scratch, NOGREP_TOOLS)
    clean_path = "/usr/local/bin:/usr/bin:/bin"
    results, receipt_runs = [], []
    t0 = time.time()
    try:
        claims = make_fixture(root)
        # reference: real PATH, no shims, no overrides
        rc0, out0, err0 = run_gate(gate, claims, root, path_override=clean_path)
        drift0, obs0 = parse(out0)
        ref_ok = (rc0 == 1 and drift0 and obs0.get("K1") == ("supported", "match")
                  and obs0.get("K2") == ("unsupported", "mismatch") and obs0.get("K3") == ("unsupported", "mismatch"))
        ref = {"rc": rc0, "drift": drift0, "obs": obs0}
        receipt_runs.append({"scenario": "reference", "rc": rc0, "drift": drift0, "obs": obs0,
                             "stderr_tail": err0[-600:]})

        def score(name, ok, detail, runs):
            results.append({"scenario": name, "pass": bool(ok), "detail": detail})
            receipt_runs.extend(runs)

        def empty_trip(p):
            try:
                return os.path.getsize(p) == 0
            except OSError:
                return False

        def same_as_ref(rc, out):
            d, o = parse(out)
            return rc == ref["rc"] and d == ref["drift"] and o == ref["obs"]

        # S1 shim-first PATH
        old = open(trip1, "w"); old.close()
        rc, out, err = run_gate(gate, claims, root, path_override=shim_dir + ":" + clean_path)
        score("S1-shim-first-path", empty_trip(trip1) and same_as_ref(rc, out),
              {"tripwire_bytes": os.path.getsize(trip1), "output_matches_reference": same_as_ref(rc, out), "rc": rc},
              [{"scenario": "S1", "rc": rc, "stderr_tail": err[-600:]}])
        # S2 BASH_ENV function shim
        open(trip2, "w").close()
        rc, out, err = run_gate(gate, claims, root, extra_env={"BASH_ENV": bash_env}, path_override=clean_path)
        score("S2-bash-env-function", empty_trip(trip2) and same_as_ref(rc, out),
              {"tripwire_bytes": os.path.getsize(trip2), "output_matches_reference": same_as_ref(rc, out), "rc": rc},
              [{"scenario": "S2", "rc": rc, "stderr_tail": err[-600:]}])
        # S3 grep absent from PATH
        rc, out, err = run_gate(gate, claims, root, path_override=nogrep_dir)
        score("S3-no-grep-on-path", "not found" not in err,
              {"rc": rc, "output_matches_reference": same_as_ref(rc, out), "path_tools": len(made),
               "stderr_tail": err[-400:]},
              [{"scenario": "S3", "rc": rc, "stderr_tail": err[-600:]}])
        # S4 override relative
        rc, out, err = run_gate(gate, claims, root, extra_env={"RESEARCH_GATE_GREP": "bin/grep"}, path_override=clean_path)
        score("S4-override-relative", rc == 2 and "GREP_PROVENANCE" in err,
              {"rc": rc, "marker": "GREP_PROVENANCE" in err, "stderr_tail": err[-400:]},
              [{"scenario": "S4", "rc": rc, "stderr_tail": err[-600:]}])
        # S5 override missing
        rc, out, err = run_gate(gate, claims, root, extra_env={"RESEARCH_GATE_GREP": os.path.join(scratch, "absent-grep")},
                                path_override=clean_path)
        score("S5-override-missing", rc == 2 and "GREP_PROVENANCE" in err,
              {"rc": rc, "marker": "GREP_PROVENANCE" in err, "stderr_tail": err[-400:]},
              [{"scenario": "S5", "rc": rc, "stderr_tail": err[-600:]}])
        # S6 override non-GNU stub
        open(trip3, "w").close()
        rc, out, err = run_gate(gate, claims, root, extra_env={"RESEARCH_GATE_GREP": stub}, path_override=clean_path)
        stub_calls = open(trip3).read()
        score("S6-override-non-gnu", rc == 2 and "GREP_PROVENANCE" in err,
              {"rc": rc, "marker": "GREP_PROVENANCE" in err, "stub_calls": len(stub_calls.splitlines()),
               "stderr_tail": err[-400:]},
              [{"scenario": "S6", "rc": rc, "stub_calls": stub_calls[:400], "stderr_tail": err[-600:]}])
        # S7 override real + echo
        rc, out, err = run_gate(gate, claims, root,
                                extra_env={"RESEARCH_GATE_GREP": REAL_GREP, "CHOUSA_GREP_PIN_ECHO": "1"},
                                path_override=clean_path)
        line = next((l for l in err.splitlines() if l.startswith("GATE_GREP: ")), "")
        score("S7-override-real-echo",
              same_as_ref(rc, out) and "path=%s" % REAL_GREP in line and "source=override" in line and "GNU grep" in line,
              {"rc": rc, "output_matches_reference": same_as_ref(rc, out), "echo_line": line},
              [{"scenario": "S7", "rc": rc, "echo_line": line, "stderr_tail": err[-600:]}])
        # S8 default + echo
        rc, out, err = run_gate(gate, claims, root, extra_env={"CHOUSA_GREP_PIN_ECHO": "1"}, path_override=clean_path)
        line = next((l for l in err.splitlines() if l.startswith("GATE_GREP: ")), "")
        score("S8-default-echo",
              same_as_ref(rc, out) and "path=%s" % REAL_GREP in line and "source=default" in line and "GNU grep" in line,
              {"rc": rc, "output_matches_reference": same_as_ref(rc, out), "echo_line": line},
              [{"scenario": "S8", "rc": rc, "echo_line": line, "stderr_tail": err[-600:]}])
        # S9 override beats BASH_ENV shim
        open(trip2, "w").close()
        rc, out, err = run_gate(gate, claims, root,
                                extra_env={"BASH_ENV": bash_env, "RESEARCH_GATE_GREP": REAL_GREP,
                                           "CHOUSA_GREP_PIN_ECHO": "1"},
                                path_override=clean_path)
        line = next((l for l in err.splitlines() if l.startswith("GATE_GREP: ")), "")
        score("S9-override-beats-shim",
              empty_trip(trip2) and same_as_ref(rc, out) and "source=override" in line,
              {"tripwire_bytes": os.path.getsize(trip2), "output_matches_reference": same_as_ref(rc, out),
               "echo_line": line},
              [{"scenario": "S9", "rc": rc, "stderr_tail": err[-600:]}])

        passed = sum(1 for r in results if r["pass"])
        holds = passed == TOTAL and ref_ok
        receipt = {"label": "%s=%d/%d" % (LABEL, passed, TOTAL), "matched": passed, "total": TOTAL,
                   "predicate_holds": holds, "reference_sane": ref_ok, "reference": ref,
                   "gate": gate, "gate_sha256": sha256_file(gate), "seed": seed,
                   "elapsed_s": round(time.time() - t0, 2), "scenarios": results, "runs": receipt_runs}
        print("%s=%d/%d" % (LABEL, passed, TOTAL))
        for r in results:
            print("  %-28s %s  %s" % (r["scenario"], "PASS" if r["pass"] else "FAIL",
                                      json.dumps(r["detail"], sort_keys=True)[:300]))
        if not ref_ok:
            print("  reference run not sane: rc=%s drift=%s obs=%s" % (rc0, drift0, obs0), file=sys.stderr)
    except subprocess.TimeoutExpired:
        receipt = {"label": "%s=timeout" % LABEL, "predicate_holds": False, "gate": gate, "seed": seed}
    finally:
        if a.receipt:
            with open(a.receipt, "w", encoding="utf-8") as f:
                json.dump(receipt, f, indent=1, sort_keys=True)
        shutil.rmtree(root, ignore_errors=True)
    return 0 if receipt.get("predicate_holds") else 1


if __name__ == "__main__":
    sys.exit(main())
