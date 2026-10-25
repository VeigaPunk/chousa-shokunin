#!/usr/bin/env python3
"""Round-39 C1 counter — the pinned env AND bash of the canonical pin capture.

Predicate (frozen in corpus/evidence/round39/claims.md before any candidate run):

    ENV_PIN_CAPTURE_MATCH=8/8

Round 38 pinned the capture's child `env`; its claims Erratum 6(c) then measured
that the capture's grandchild was a BARE `bash`: PATH resolution inside the
pinned env still consulted the caller — a PATH `bash` shim re-added
CHOUSA_GREP_PIN_ECHO (the baseline embeds a GATE_GREP line and a plain --drift
reports a phantom -GATE_GREP) or suppressed the capture outright, while a
`command env` mutant showed the env pin's PATH half was unmeasured. The
round-39 gate runs the grandchild through ONE pinned absolute bash (default
/usr/bin/bash, GNU-reporting; RESEARCH_GATE_BASH override, absolute +
GNU-reporting, refused exit 2 with BASH_PROVENANCE before any mode runs).

Eight scenarios: the round-38 seven (unchanged, frozen in the same
expectations table this file shares) plus an eighth family,
`capture-bash-path-pin`, whose five cells cover the round-38 Errata 5/6
pre-registered list: the PATH `bash` shim (echo re-add and suppress shapes —
the hostile-drift vector), the PATH `env` shim (a hold on the pinned gate; the
discrimination witness against a PATH-resolved-env mutant is a committed
control run, see claims.md), the positive override-honoured witness, and the
relative-override refusal.

Scoring: matched / 8, printed as ENV_PIN_CAPTURE_MATCH=<k>/8.
Exit 0 iff k == 8; 1 otherwise; 2 on a harness error (fixture/gate unreadable,
or the gate file changed while the scenarios ran — the round-38 receipt
binding: no receipt is published for bytes that did not run every scenario).

Every receipt binds counter/expect/gate/receipt digests and, new in round 39,
verifier_sha256 — the digest of round39/verify-receipts.py, so a replaced
verifier cannot silently re-adjudicate this receipt (the round-38 Erratum 2/11
carried debt, closed for this family by C2's counter).

Temp dirs: $C1_TMP (must exist) or the system temp; a fresh mkdtemp inside it.
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

HERE = os.path.dirname(os.path.abspath(__file__))
EXPECTATIONS = os.path.join(HERE, "expectations.jsonl")
VERIFY = os.path.join(HERE, "verify-receipts.py")

# Scenario ids, in run order. The observable expectations for each id are
# frozen in expectations.jsonl; this table only maps ids to their fixtures.
SCENARIO_ORDER = [
    "hold-plain",
    "hold-fn-benign",
    "env-fn-echo-scrub",
    "env-fn-root-move",
    "env-fn-suppress",
    "env-override-missing",
    "env-override-fake",
    "capture-bash-path-pin",
]

# The interposing function shape: forward the -u scrubs verbatim, then re-add
# the attacker's variable before the utility. Exported through BASH_FUNC_env%%
# in the exact `() { ... }` form bash's function importer accepts.
FN_ECHO = ('() { local o=(); while (($#)); do case "$1" in -u) o+=("$1" "$2"); '
           'shift 2;; *) break;; esac; done; '
           '/usr/bin/env "${o[@]}" CHOUSA_GREP_PIN_ECHO=1 "$@"; }')
FN_SUPPRESS = '() { :; }'
FN_ROOT = ('() { local o=(); while (($#)); do case "$1" in -u) o+=("$1" "$2"); '
           'shift 2;; *) break;; esac; done; '
           '/usr/bin/env "${o[@]}" CHOUSA_ROOT="%s" "$@"; }')
FN_BENIGN = '() { /usr/bin/env "$@"; }'


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_expectations():
    rows = {}
    with open(EXPECTATIONS, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if row.get("counter") == "c1":
                rows[row["id"]] = row["expect"]
    return rows


def base_env():
    """The counter's own environment scrubbed of the families scenarios add
    and of the startup/option channels the GATE ITSELF consumes before its
    body runs (the gate sources BASH_ENV at startup — the round-37 Erratum-5
    channel — so an ambient startup file would install attack functions or
    forge refusal tokens inside the gate process and pass weakened fixtures
    that are not measurements). PATH stays live: the PATH shims are the
    claim's own cells, installed by the scenarios, not the ambient caller."""
    env = dict(os.environ)
    for key in list(env):
        if (key.startswith("BASH_FUNC_") or key.startswith("CHOUSA_")
                or key.startswith("RESEARCH_GATE_") or key.startswith("PYTHON")
                or key in ("BASH_ENV", "ENV", "SHELLOPTS", "BASHOPTS",
                           "POSIXLY_CORRECT")):
            del env[key]
    return env


BASH = "/usr/bin/bash" if os.path.isfile("/usr/bin/bash") else "bash"
REAL_BASH = BASH


def run_pin(gate, baseline, env):
    proc = subprocess.run([BASH, gate, "--pin", baseline], env=env,
                          capture_output=True, text=True, timeout=180)
    return proc


def run_drift(gate, baseline, env):
    proc = subprocess.run([BASH, gate, "--drift", baseline], env=env,
                          capture_output=True, text=True, timeout=180)
    line = ""
    for l in proc.stdout.splitlines():
        if l.startswith("GATE_DRIFT:"):
            line = l
    return proc.returncode, line


def count_echo_lines(path):
    if not os.path.isfile(path):
        return -1
    n = 0
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("GATE_GREP: "):
                n += 1
    return n


def refusal_token(proc, token):
    # Anchored, gate-emitted line — a bare token-anywhere test could be
    # satisfied by any output mentioning the word.
    return token if any(
        l.startswith("research-gate: %s refused:" % token)
        for l in proc.stderr.splitlines()) else ""


def setup_scenario(sid, work):
    """-> (env additions, foreign paths). Each scenario's fixture lives under work."""
    env = {}
    foreign = {}
    if sid == "hold-plain":
        pass
    elif sid == "hold-fn-benign":
        env["BASH_FUNC_env%%"] = FN_BENIGN
    elif sid == "env-fn-echo-scrub":
        env["BASH_FUNC_env%%"] = FN_ECHO
    elif sid == "env-fn-suppress":
        env["BASH_FUNC_env%%"] = FN_SUPPRESS
    elif sid == "env-fn-root-move":
        root = os.path.join(work, "foreign-root")
        os.makedirs(root, exist_ok=True)
        env["BASH_FUNC_env%%"] = FN_ROOT % root
        foreign["root"] = root
    elif sid == "env-override-missing":
        env["RESEARCH_GATE_ENV"] = os.path.join(work, "no-such-dir", "env")
    elif sid == "env-override-fake":
        fake = os.path.join(work, "fake-env")
        with open(fake, "w", encoding="utf-8") as fh:
            fh.write("#!/bin/sh\nexit 0\n")
        os.chmod(fake, 0o755)
        env["RESEARCH_GATE_ENV"] = fake
    elif sid == "capture-bash-path-pin":
        # Five cells, one fixture set: a PATH `bash` shim re-adding the pin
        # echo, a PATH `bash` shim suppressing the capture, a PATH `env` shim
        # re-adding the pin echo (hold on the pinned gate), and the bash-pin
        # override honoured / refused shapes.
        shimdir = os.path.join(work, "r39-shimdir")
        os.makedirs(shimdir, exist_ok=True)
        with open(os.path.join(shimdir, "bash"), "w", encoding="utf-8") as fh:
            fh.write("#!/bin/sh\nCHOUSA_GREP_PIN_ECHO=1 exec %s \"$@\"\n"
                     % REAL_BASH)
        os.chmod(os.path.join(shimdir, "bash"), 0o755)
        suppress = os.path.join(work, "r39-suppressdir")
        os.makedirs(suppress, exist_ok=True)
        with open(os.path.join(suppress, "bash"), "w", encoding="utf-8") as fh:
            fh.write("#!/bin/sh\nexit 0\n")
        os.chmod(os.path.join(suppress, "bash"), 0o755)
        envshim = os.path.join(work, "r39-envshimdir")
        os.makedirs(envshim, exist_ok=True)
        with open(os.path.join(envshim, "env"), "w", encoding="utf-8") as fh:
            # Forward the -u scrub pairs verbatim, THEN re-add the echo
            # variable: a prefix assignment (`VAR=1 exec env -u VAR …`) is
            # un-set again by the forwarded -u, which is exactly the
            # FN_ECHO parsing shape for the binary case.
            fh.write("#!/bin/sh\n"
                     "o=''\n"
                     "while [ $# -gt 0 ]; do\n"
                     "  case \"$1\" in\n"
                     "    -u) o=\"$o $1 $2\"; shift 2;;\n"
                     "    *) break;;\n"
                     "  esac\n"
                     "done\n"
                     "exec /usr/bin/env $o CHOUSA_GREP_PIN_ECHO=1 \"$@\"\n")
        os.chmod(os.path.join(envshim, "env"), 0o755)
        foreign["shimdir"] = shimdir
        foreign["suppressdir"] = suppress
        foreign["envshimdir"] = envshim
    else:
        raise ValueError("unknown scenario: %s" % sid)
    return env, foreign


def run_scenario(gate, work, sid, expect):
    if sid == "capture-bash-path-pin":
        return run_bash_path_family(gate, work, expect)
    baseline = os.path.join(work, "baseline-%s.txt" % sid)
    additions, _foreign = setup_scenario(sid, work)
    env = base_env()
    env.update(additions)
    proc = run_pin(gate, baseline, env)
    observed = {
        "pin_rc": proc.returncode,
        "pin_file": os.path.isfile(baseline),
    }
    if "echo_lines" in expect:
        observed["echo_lines"] = count_echo_lines(baseline)
    if "drift_rc" in expect:
        denv = base_env()
        drc, dline = run_drift(gate, baseline, denv)
        observed["drift_rc"] = drc
        observed["drift_line"] = dline
    if "refusal" in expect:
        # The frozen expect names the token its value; the observation is the
        # anchored gate-emitted refusal line carrying it (or "").
        observed["refusal"] = refusal_token(proc, expect["refusal"])
    ok = all(observed.get(k) == v for k, v in expect.items())
    return {"id": sid, "expect": expect, "observed": observed, "ok": ok}


def run_bash_path_family(gate, work, expect):
    """The eighth family: five cells, each its own pin/drift pair."""
    _adds, foreign = setup_scenario("capture-bash-path-pin", work)
    observed = {}

    def cell(name, env):
        baseline = os.path.join(work, "r39-%s.txt" % name)
        proc = run_pin(gate, baseline, env)
        observed["%s.pin_rc" % name] = proc.returncode
        observed["%s.pin_file" % name] = os.path.isfile(baseline)
        if "%s.echo_lines" % name in expect:
            observed["%s.echo_lines" % name] = count_echo_lines(baseline)
        if "%s.drift_rc" % name in expect:
            drc, dline = run_drift(gate, baseline, base_env())
            observed["%s.drift_rc" % name] = drc
            observed["%s.drift_line" % name] = dline
        if "%s.refusal" % name in expect:
            observed["%s.refusal" % name] = refusal_token(
                proc, expect["%s.refusal" % name])

    env = base_env()
    env["PATH"] = foreign["shimdir"] + os.pathsep + env.get("PATH", "")
    cell("path_bash_shim_echo", env)

    env = base_env()
    env["PATH"] = foreign["suppressdir"] + os.pathsep + env.get("PATH", "")
    cell("path_bash_shim_suppress", env)

    env = base_env()
    env["PATH"] = foreign["envshimdir"] + os.pathsep + env.get("PATH", "")
    cell("path_env_shim_echo", env)

    env = base_env()
    env["RESEARCH_GATE_BASH"] = REAL_BASH
    cell("override_honoured", env)

    env = base_env()
    env["RESEARCH_GATE_BASH"] = "bin/bash"
    cell("override_relative_refused", env)

    ok = all(observed.get(k) == v for k, v in expect.items())
    return {"id": "capture-bash-path-pin", "expect": expect,
            "observed": observed, "ok": ok}


def receipt_digest(receipt):
    body = {k: v for k, v in receipt.items() if k != "receipt_sha256"}
    text = json.dumps(body, indent=2, sort_keys=True) + "\n"
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", required=True)
    ap.add_argument("--seed", type=int, default=39001)
    ap.add_argument("--receipt")
    ap.add_argument("--tmp")
    args = ap.parse_args()

    gate = os.path.abspath(args.gate)
    if args.receipt and os.path.lexists(args.receipt):
        # A run that refuses must not leave a valid-looking stale receipt at
        # the requested path (round-38 Erratum 7/12).
        os.unlink(args.receipt)
    if not os.path.isfile(gate):
        print("c1-count: gate not found: %s" % gate, file=sys.stderr)
        return 2
    if not os.path.isfile(EXPECTATIONS):
        print("c1-count: expectations file missing: %s" % EXPECTATIONS,
              file=sys.stderr)
        return 2
    if not os.path.isfile(VERIFY):
        print("c1-count: verifier not found: %s" % VERIFY, file=sys.stderr)
        return 2
    base_tmp = args.tmp or os.environ.get("C1_TMP") or tempfile.gettempdir()
    if not os.path.isdir(base_tmp):
        print("c1-count: temp dir does not exist: %s" % base_tmp, file=sys.stderr)
        return 2
    expects = load_expectations()
    missing = [s for s in SCENARIO_ORDER if s not in expects]
    if missing:
        print("c1-count: expectations missing for: %s" % ", ".join(missing),
              file=sys.stderr)
        return 2
    # Hash the frozen table BEFORE the scenarios run and require it unchanged
    # afterwards: the receipt must bind the bytes the scenarios actually
    # scored, not a table edited mid-run (round-38 Erratum 8).
    expect_sha = sha256_file(EXPECTATIONS)
    verifier_sha = sha256_file(VERIFY)

    work = tempfile.mkdtemp(prefix="chousa-r39-c1-", dir=base_tmp)
    try:
        gate_sha_pre = sha256_file(gate)
        rows = []
        for sid in SCENARIO_ORDER:
            rows.append(run_scenario(gate, work, sid, expects[sid]))
            if sha256_file(gate) != gate_sha_pre:
                print("c1-count: gate bytes changed across the run "
                      "(pre %s != current) — no receipt published"
                      % gate_sha_pre[:16], file=sys.stderr)
                return 2
        gate_sha_post = sha256_file(gate)
        if sha256_file(EXPECTATIONS) != expect_sha:
            print("c1-count: expectations changed across the run "
                  "(pre %s != current) — no receipt published"
                  % expect_sha[:16], file=sys.stderr)
            return 2
    finally:
        shutil.rmtree(work, ignore_errors=True)

    matched = sum(1 for r in rows if r["ok"])
    total = len(rows)
    for r in rows:
        print("%s %-20s expect=%s observed=%s"
              % ("PASS" if r["ok"] else "FAIL", r["id"], r["expect"],
                 r["observed"]))
    print("ENV_PIN_CAPTURE_MATCH=%d/%d" % (matched, total))
    # The frozen predicate labels 8/8; the count is the claim, not whatever
    # the table happens to hold (a counter edited to seven scenarios must not
    # be able to print a passing 7/7 under this predicate's name).
    holds = matched == 8 and total == 8
    if args.receipt:
        receipt = {
            "counter": os.path.relpath(__file__),
            "counter_sha256": sha256_file(os.path.abspath(__file__)),
            "expectations": os.path.relpath(EXPECTATIONS),
            "expect_sha256": expect_sha,
            "verifier": os.path.relpath(VERIFY),
            "verifier_sha256": verifier_sha,
            "seed": args.seed,
            "gate": gate,
            "gate_sha256": gate_sha_pre,
            "gate_sha256_pre": gate_sha_pre,
            "gate_sha256_post": gate_sha_post,
            "scenarios": rows,
            "matched": matched,
            "total": total,
            "predicate": "ENV_PIN_CAPTURE_MATCH=8/8",
            "predicate_holds": holds,
        }
        receipt["receipt_sha256"] = receipt_digest(receipt)
        with open(args.receipt, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=2, sort_keys=True)
            fh.write("\n")
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
