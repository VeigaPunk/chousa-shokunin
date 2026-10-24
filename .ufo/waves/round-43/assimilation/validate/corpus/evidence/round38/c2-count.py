#!/usr/bin/env python3
"""Round-38 C2 counter — receipt binding strength (the round-37 F1/F4 debt).

Predicate (frozen in corpus/evidence/round38/claims.md before any candidate run):

    RECEIPT_BINDING_MATCH=7/7

The round-37 residual wave demonstrated two receipt forgery paths
(.ufo/waves/round-37/residual/RevC1FreshSeed.md):

  F1 a gate that rewrites itself after the first scenario got a receipt stamped
     with the landed gate's sha256, because the counter hashed the gate file
     AFTER the run — the receipt could not establish which bytes answered each
     scenario;
  F4 the receipt carried no counter identity at all: an edited counter that kept
     seven scenarios and seven passes would silently redefine the predicate it
     claimed to measure.

The round-38 counters bind, measured by the counter itself before/after the
run: gate_sha256_pre == gate_sha256_post (a changed gate refuses exit 2 with no
receipt), counter_sha256, expect_sha256 (the frozen expectation table), and
receipt_sha256 (the receipt body's own digest). verify-receipts.py re-derives
every binding from committed bytes.

Seven scenarios; the frozen expectations live in expectations.jsonl next to
this file. A scenario passes only when every listed observation matches: the
counter's exit code, the receipt file's existence, and the verify command's
exit code for the honest, foreign, doctored and legacy receipts. The
before-state control is this same counter pointed at the round-37 c1 counter
(--counter corpus/evidence/round37/c1-count.py): no binding fields exist, so
every scenario fails.

Scoring: matched / 7, printed as RECEIPT_BINDING_MATCH=<k>/7.
Exit 0 iff k == 7; 1 otherwise; 2 on a harness error.

Temp dirs: $C2_TMP (must exist) or the system temp; a fresh mkdtemp inside it.
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
R37_C1 = os.path.join(HERE, "..", "round37", "c1-count.py")

SCENARIO_ORDER = [
    "hold-receipt-verifies",
    "self-rewrite-refused",
    "foreign-gate-distinguished",
    "counter-tamper-detected",
    "expect-tamper-detected",
    "body-tamper-detected",
    "legacy-receipt-refused",
]


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
            if row.get("counter") == "c2":
                rows[row["id"]] = row["expect"]
    return rows


def base_env():
    """Scrub the startup/option channels a child would itself consume (the
    gate sources BASH_ENV before its body runs) plus the families scenarios
    add and the Python startup channel (W2RevC2Final: a hostile PYTHONPATH
    reaches the sys.executable children through sitecustomize); PATH stays
    live: committed runs are made under a clean caller environment."""
    env = dict(os.environ)
    for key in list(env):
        if (key.startswith("BASH_FUNC_") or key.startswith("CHOUSA_")
                or key.startswith("RESEARCH_GATE_")
                or key.startswith("PYTHON")
                or key in ("BASH_ENV", "ENV", "SHELLOPTS", "BASHOPTS",
                           "POSIXLY_CORRECT")):
            del env[key]
    return env


def run_counter(counter, gate, seed, receipt, work):
    # -E ignores PYTHONPATH/PYTHONHOME/PYTHONSTARTUP in the child: the child
    # must hash with the interpreter's own stdlib, not the caller's site.
    proc = subprocess.run(
        [sys.executable, "-E", counter, "--gate", gate, "--seed", str(seed),
         "--receipt", receipt, "--tmp", work],
        capture_output=True, text=True, timeout=3000, env=base_env())
    return proc


def run_verify(receipt, gate, counter):
    proc = subprocess.run(
        [sys.executable, "-E", VERIFY, "--receipt", receipt, "--gate", gate,
         "--counter", counter, "--expectations", EXPECTATIONS],
        capture_output=True, text=True, timeout=300, env=base_env())
    return proc.returncode, proc.stdout.strip()


def write_self_rewrite_shim(shim, target, marker):
    # Every interpolated path is shlex-quoted: the gate path arrives from the
    # caller, and unquoted interpolation into shell source would execute an
    # embedded gate filename as commands during scoring (SentScope finding 1).
    import shlex
    q_marker = shlex.quote(marker)
    q_target = shlex.quote(target)
    body = ("#!/bin/bash\n"
            "# round-37 residual F1 replay: the first invocation restores the\n"
            "# target gate over this shim's own path, so the post-run bytes are\n"
            "# the target's while the shim bytes answered the first invocation.\n"
            "if [[ ! -e %s ]]; then\n"
            "  touch %s\n"
            "  cat %s > \"$0.tmp\" && mv \"$0.tmp\" \"$0\"\n"
            "fi\n"
            "exec bash %s \"$@\"\n" % (q_marker, q_marker, q_target, q_target))
    with open(shim, "w", encoding="utf-8") as fh:
        fh.write(body)
    os.chmod(shim, 0o755)


def doctor(receipt_path, mutate, re_digest=False):
    """Apply mutate to the receipt and optionally re-seal its self-digest.

    re_digest=True rebuilds receipt_sha256 so the doctoring reaches the NAMED
    binding check (counter/expect) instead of stopping at the self-digest;
    re_digest=False leaves the digest stale so the self-digest check fires.
    A field the legacy shape lacks stays absent — verify-receipts fails either
    way (a doctored binding mismatches, an absent binding is a missing-field
    refusal).
    """
    with open(receipt_path, "r", encoding="utf-8") as fh:
        receipt = json.load(fh)
    try:
        mutate(receipt)
    except (KeyError, TypeError):
        pass
    if re_digest and "receipt_sha256" in receipt:
        receipt["receipt_sha256"] = receipt_digest(receipt)
    with open(receipt_path, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=2, sort_keys=True)
        fh.write("\n")


def run_scenario(counter, gate, seed, work, sid, expect):
    observed = {}
    if sid == "hold-receipt-verifies":
        rcpt = os.path.join(work, "hold-receipt.json")
        proc = run_counter(counter, gate, seed, rcpt, work)
        observed["counter_rc"] = proc.returncode
        observed["receipt"] = os.path.isfile(rcpt)
        if "verify_rc" in expect:
            vrc, _ = run_verify(rcpt, gate, counter)
            observed["verify_rc"] = vrc

    elif sid == "self-rewrite-refused":
        shim = os.path.join(work, "f1-shim-gate.sh")
        marker = os.path.join(work, "f1-marker")
        write_self_rewrite_shim(shim, gate, marker)
        rcpt = os.path.join(work, "f1-receipt.json")
        proc = run_counter(counter, shim, seed, rcpt, work)
        observed["counter_rc"] = proc.returncode
        observed["receipt"] = os.path.isfile(rcpt)

    elif sid == "foreign-gate-distinguished":
        foreign = os.path.join(work, "foreign-gate.sh")
        shutil.copyfile(gate, foreign)
        # The foreign gate must differ in bytes from the landed one, or its
        # receipt's binding equals the landed hash and the landed verification
        # cannot be expected to fail.
        with open(foreign, "a", encoding="utf-8") as fh:
            fh.write("\n# round-38 c2 foreign-gate-distinguished fixture\n")
        os.chmod(foreign, 0o755)
        rcpt = os.path.join(work, "foreign-receipt.json")
        proc = run_counter(counter, foreign, seed, rcpt, work)
        observed["counter_rc"] = proc.returncode
        observed["receipt"] = os.path.isfile(rcpt)
        if "verify_foreign_rc" in expect and os.path.isfile(rcpt):
            vrc, _ = run_verify(rcpt, foreign, counter)
            observed["verify_foreign_rc"] = vrc
        if "verify_landed_rc" in expect and os.path.isfile(rcpt):
            vrc, _ = run_verify(rcpt, gate, counter)
            observed["verify_landed_rc"] = vrc

    elif sid in ("counter-tamper-detected", "expect-tamper-detected",
                 "body-tamper-detected"):
        # The honest receipt must verify first: otherwise the tampered copy's
        # refusal only restates that the pipeline is unverifiable (the
        # before-state), not that the doctoring was detected. The counter and
        # expectation doctors RE-SEAL the self-digest so the refusal must come
        # from the NAMED binding check; the body doctor stays unsealed so the
        # self-digest check fires. The exact verifier line is recorded so the
        # named check is the asserted observable, not any refusal.
        clean = os.path.join(work, "%s-clean.json" % sid)
        run_counter(counter, gate, seed, clean, work)
        crc, cout = run_verify(clean, gate, counter)
        observed["clean_verify_rc"] = crc
        observed["clean_verify_out"] = cout
        if crc != 0:
            observed["verify_rc"] = "not-measured"
            return {"id": sid, "expect": expect, "observed": observed,
                    "ok": False}
        tampered = os.path.join(work, "%s-tampered.json" % sid)
        shutil.copyfile(clean, tampered)
        if sid == "counter-tamper-detected":
            def flip_counter(r):
                r["counter_sha256"] = ("0" if r["counter_sha256"][0] != "0"
                                       else "1") + r["counter_sha256"][1:]
            doctor(tampered, flip_counter, re_digest=True)
        elif sid == "expect-tamper-detected":
            def flip_expect(r):
                r["expect_sha256"] = ("0" if r["expect_sha256"][0] != "0"
                                      else "1") + r["expect_sha256"][1:]
            doctor(tampered, flip_expect, re_digest=True)
        else:
            def flip_body(r):
                r["matched"] = r["matched"] - 1 if r["matched"] > 0 else 1
                r["predicate_holds"] = not r["predicate_holds"]
            doctor(tampered, flip_body)
        vrc, vout = run_verify(tampered, gate, counter)
        observed["verify_rc"] = vrc
        observed["verify_fail"] = vout

    elif sid == "legacy-receipt-refused":
        # A legacy (round-37 shape) receipt must fail closed — and the subject
        # counter's own honest receipt must verify, so the refusal is
        # discrimination against the legacy shape, not the absence of any
        # verifiable pipeline (which is the before-state).
        hold = os.path.join(work, "legacy-hold.json")
        run_counter(counter, gate, seed, hold, work)
        hrc, _ = run_verify(hold, gate, counter)
        observed["hold_verify_rc"] = hrc
        r37 = os.path.abspath(R37_C1)
        rcpt = os.path.join(work, "legacy-receipt.json")
        proc = run_counter(r37, gate, seed, rcpt, work)
        observed["counter_rc"] = proc.returncode
        observed["receipt"] = os.path.isfile(rcpt)
        if "verify_rc" in expect and os.path.isfile(rcpt):
            vrc, _ = run_verify(rcpt, gate, r37)
            observed["verify_rc"] = vrc

    else:
        raise ValueError("unknown scenario: %s" % sid)

    ok = True
    for k, v in expect.items():
        if k.endswith("_contains"):
            if v not in str(observed.get(k[:-len("_contains")], "")):
                ok = False
        elif observed.get(k) != v:
            ok = False
    return {"id": sid, "expect": expect, "observed": observed, "ok": ok}


def receipt_digest(receipt):
    body = {k: v for k, v in receipt.items() if k != "receipt_sha256"}
    text = json.dumps(body, indent=2, sort_keys=True) + "\n"
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", required=True)
    ap.add_argument("--counter", default=os.path.join(HERE, "c1-count.py"))
    ap.add_argument("--seed", type=int, default=38101)
    ap.add_argument("--receipt")
    ap.add_argument("--tmp")
    args = ap.parse_args()

    gate = os.path.abspath(args.gate)
    counter = os.path.abspath(args.counter)
    if args.receipt and os.path.lexists(args.receipt):
        # A run that refuses must not leave a valid-looking stale receipt at
        # the requested path — unlinked BEFORE any refusal path (W2RevErrata
        # finding 1: missing-gate refusals used to preserve it).
        os.unlink(args.receipt)
    for path, name in ((gate, "gate"), (counter, "counter"),
                       (VERIFY, "verify-receipts.py")):
        if not os.path.isfile(path):
            print("c2-count: %s not found: %s" % (name, path), file=sys.stderr)
            return 2
    if not os.path.isfile(EXPECTATIONS):
        print("c2-count: expectations file missing: %s" % EXPECTATIONS,
              file=sys.stderr)
        return 2
    base_tmp = args.tmp or os.environ.get("C2_TMP") or tempfile.gettempdir()
    if not os.path.isdir(base_tmp):
        print("c2-count: temp dir does not exist: %s" % base_tmp, file=sys.stderr)
        return 2
    expects = load_expectations()
    missing = [s for s in SCENARIO_ORDER if s not in expects]
    if missing:
        print("c2-count: expectations missing for: %s" % ", ".join(missing),
              file=sys.stderr)
        return 2
    # Hash the frozen table BEFORE the scenarios run and require it unchanged
    # afterwards: the receipt must bind the bytes the scenarios actually
    # scored, not a table edited mid-run (SentScope finding 2).
    expect_sha = sha256_file(EXPECTATIONS)

    work = tempfile.mkdtemp(prefix="chousa-r38-c2-", dir=base_tmp)
    try:
        gate_sha_pre = sha256_file(gate)
        rows = []
        for sid in SCENARIO_ORDER:
            rows.append(run_scenario(counter, gate, args.seed, work, sid,
                                     expects[sid]))
            if sha256_file(gate) != gate_sha_pre:
                print("c2-count: gate bytes changed across the run "
                      "(pre %s != current) — no receipt published"
                      % gate_sha_pre[:16], file=sys.stderr)
                return 2
        gate_sha_post = sha256_file(gate)
        if sha256_file(EXPECTATIONS) != expect_sha:
            print("c2-count: expectations changed across the run "
                  "(pre %s != current) — no receipt published"
                  % expect_sha[:16], file=sys.stderr)
            return 2
    finally:
        shutil.rmtree(work, ignore_errors=True)

    matched = sum(1 for r in rows if r["ok"])
    total = len(rows)
    for r in rows:
        print("%s %-26s expect=%s observed=%s"
              % ("PASS" if r["ok"] else "FAIL", r["id"], r["expect"],
                 r["observed"]))
    print("RECEIPT_BINDING_MATCH=%d/%d" % (matched, total))
    # The frozen predicate labels 7/7; the count is the claim, not whatever
    # the table happens to hold.
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
            "subject_counter": counter,
            "scenarios": rows,
            "matched": matched,
            "total": total,
            "predicate": "RECEIPT_BINDING_MATCH=7/7",
            "predicate_holds": holds,
        }
        receipt["receipt_sha256"] = receipt_digest(receipt)
        with open(args.receipt, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=2, sort_keys=True)
            fh.write("\n")
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
