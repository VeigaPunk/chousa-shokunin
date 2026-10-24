#!/usr/bin/env python3
"""Round-38 C1 counter — the pinned env of the canonical pin capture.

Predicate (frozen in corpus/evidence/round38/claims.md before any candidate run):

    ENV_PIN_CAPTURE_MATCH=7/7

The gate's canonical pin capture spawned its child through a BARE `env`
invocation. A caller-exported shell function named `env` is delivered to every
child bash through BASH_FUNC_env%% (the round-37 claims Erratum-5 channel), so
the function received the capture call itself: re-adding CHOUSA_GREP_PIN_ECHO
embedded a GATE_GREP line in the baseline and a plain --drift reported a phantom
-GATE_GREP; re-adding CHOUSA_ROOT ran the capture against a foreign root; a
suppressing function killed the capture outright. The landed gate pins ONE
absolute env for the capture child, so the caller's function cannot interpose.

Seven scenarios; the frozen expectations live in expectations.jsonl next to this
file (loaded at runtime and bound into every receipt as expect_sha256 — a
counter edit that silently redefines the expectations is visible in git, and a
receipt proves which expectation bytes it scored against). Two are contract
holds (they pass before and after); five are the separation cells — an exported
env function that re-adds the pin echo, moves CHOUSA_ROOT, suppresses the
capture, or an env pin override that is missing or not GNU coreutils env. A
scenario passes only when every listed observation matches: the pin exit code,
the baseline file's existence and its GATE_GREP line count, the drift exit code
and the drift's exact GATE_DRIFT line, or the refusal token on stderr.

Scoring: matched / 7, printed as ENV_PIN_CAPTURE_MATCH=<k>/7.
Exit 0 iff k == 7; 1 otherwise; 2 on a harness error (fixture/gate unreadable,
or the gate file changed while the scenarios ran — the round-38 receipt binding:
no receipt is published for bytes that did not run every scenario).

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
    that are not measurements). PATH stays live: bare-name resolution inside
    the capture is the claim's named r39 witness, and committed runs are
    made under a clean caller environment.
    """
    env = dict(os.environ)
    for key in list(env):
        if (key.startswith("BASH_FUNC_") or key.startswith("CHOUSA_")
                or key.startswith("RESEARCH_GATE_")
                or key in ("BASH_ENV", "ENV", "SHELLOPTS", "BASHOPTS")):
            del env[key]
    return env


BASH = "/usr/bin/bash" if os.path.isfile("/usr/bin/bash") else "bash"


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
    else:
        raise ValueError("unknown scenario: %s" % sid)
    return env, foreign


def run_scenario(gate, work, sid, expect):
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
        # Anchored, gate-emitted line — a bare token-anywhere test could be
        # satisfied by any output mentioning the word.
        observed["refusal"] = "ENV_PROVENANCE" if any(
            l.startswith("research-gate: ENV_PROVENANCE refused:")
            for l in proc.stderr.splitlines()) else ""
    ok = all(observed.get(k) == v for k, v in expect.items())
    return {"id": sid, "expect": expect, "observed": observed, "ok": ok}


def receipt_digest(receipt):
    body = {k: v for k, v in receipt.items() if k != "receipt_sha256"}
    text = json.dumps(body, indent=2, sort_keys=True) + "\n"
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", required=True)
    ap.add_argument("--seed", type=int, default=38001)
    ap.add_argument("--receipt")
    ap.add_argument("--tmp")
    args = ap.parse_args()

    gate = os.path.abspath(args.gate)
    if not os.path.isfile(gate):
        print("c1-count: gate not found: %s" % gate, file=sys.stderr)
        return 2
    if not os.path.isfile(EXPECTATIONS):
        print("c1-count: expectations file missing: %s" % EXPECTATIONS,
              file=sys.stderr)
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
    # scored, not a table edited mid-run (SentScope finding 2).
    expect_sha = sha256_file(EXPECTATIONS)

    work = tempfile.mkdtemp(prefix="chousa-r38-c1-", dir=base_tmp)
    try:
        if args.receipt and os.path.exists(args.receipt):
            # A run that refuses must not leave a valid-looking stale receipt
            # at the requested path (the refusal publishes nothing).
            os.unlink(args.receipt)
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
    # The frozen predicate labels 7/7; the count is the claim, not whatever
    # the table happens to hold (a counter edited to six scenarios must not
    # be able to print a passing 6/6 under this predicate's name).
    holds = matched == 7 and total == 7
    if args.receipt:
        receipt = {
            "counter": os.path.relpath(__file__),
            "counter_sha256": sha256_file(os.path.abspath(__file__)),
            "expectations": os.path.relpath(EXPECTATIONS),
            "expect_sha256": expect_sha,
            "seed": args.seed,
            "gate": gate,
            "gate_sha256": gate_sha_pre,
            "gate_sha256_pre": gate_sha_pre,
            "gate_sha256_post": gate_sha_post,
            "scenarios": rows,
            "matched": matched,
            "total": total,
            "predicate": "ENV_PIN_CAPTURE_MATCH=7/7",
            "predicate_holds": holds,
        }
        receipt["receipt_sha256"] = receipt_digest(receipt)
        with open(args.receipt, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=2, sort_keys=True)
            fh.write("\n")
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
