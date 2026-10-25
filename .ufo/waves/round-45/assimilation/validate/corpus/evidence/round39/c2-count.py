#!/usr/bin/env python3
"""Round-39 C2 counter — receipt binding strength, round-39 edition.

Predicate (frozen in corpus/evidence/round39/claims.md before any candidate run):

    RECEIPT_BINDING_MATCH=8/8

Carries the round-38 seven scenarios (the F1/F4 fixes they freeze: pre==post
gate binding, counter/expect/receipt digests, census-tied verification with ok
re-derivation, strict schema, changed-table refusal) and adds an eighth,
`verifier-subject-rebind`, closing the round-38 Erratum 2/11 carried debt that
was demonstrated live twice: receipts now bind verifier_sha256 (the digest of
round39/verify-receipts.py) and, for c2-family receipts, subject_counter +
subject_counter_sha256 (the counter the run measured), and the verifier
re-derives both — a replaced (weakened) verifier copy refuses
`verifier-sha256-mismatch`; a receipt re-pointed at a different or doctored
subject refuses `subject-counter-sha256-mismatch`. The legacy cell now binds
the committed round-38 receipt bytes themselves: they fail closed under this
verifier (generation predicate), and an r39 receipt with the verifier binding
stripped fails `missing-field verifier_sha256`.

The before-state control is the round-38 pipeline: the same c2 counter shape
pointed at round38/verify-receipts.py accepts a replaced verifier silently
(the round-38 Erratum 11 measurement — five of six verifier mutants re-
adjudicated 7/7); every round-38 receipt lacks both new bindings and refuses
under this verifier.

Eight scenarios; the frozen expectations live in expectations.jsonl next to
this file. Scoring: matched / 8, printed as RECEIPT_BINDING_MATCH=<k>/8.
Exit 0 iff k == 8; 1 otherwise; 2 on a harness error.

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
R38_RECEIPT = os.path.abspath(os.path.join(
    HERE, "..", "round38", "receipts", "c1-after-s38001.json"))
R38_C1 = os.path.abspath(os.path.join(HERE, "..", "round38", "c1-count.py"))
R38_EXPECTATIONS = os.path.abspath(os.path.join(
    HERE, "..", "round38", "expectations.jsonl"))

SCENARIO_ORDER = [
    "hold-receipt-verifies",
    "self-rewrite-refused",
    "foreign-gate-distinguished",
    "counter-tamper-detected",
    "expect-tamper-detected",
    "body-tamper-detected",
    "legacy-receipt-refused",
    "verifier-subject-rebind",
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


def run_counter(counter, gate, seed, receipt, work, extra_env=None):
    # -E ignores PYTHONPATH/PYTHONHOME/PYTHONSTARTUP in the child: the child
    # must hash with the interpreter's own stdlib, not the caller's site.
    env = base_env()
    if extra_env:
        env.update(extra_env)
    proc = subprocess.run(
        [sys.executable, "-E", counter, "--gate", gate, "--seed", str(seed),
         "--receipt", receipt, "--tmp", work],
        capture_output=True, text=True, timeout=3000, env=env)
    return proc


def run_verify(receipt, gate, counter, verifier=None, expectations=None):
    proc = subprocess.run(
        [sys.executable, "-E", verifier or VERIFY, "--receipt", receipt,
         "--gate", gate, "--counter", counter, "--expectations",
         expectations or EXPECTATIONS],
        capture_output=True, text=True, timeout=300, env=base_env())
    return proc.returncode, proc.stdout.strip()


def write_self_rewrite_shim(shim, target, marker):
    # Every interpolated path is shlex-quoted: the gate path arrives from the
    # caller, and unquoted interpolation into shell source would execute an
    # embedded gate filename as commands during scoring (round-38 Erratum 8a).
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
    binding check instead of stopping at the self-digest (round-38 Erratum 3).
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
        with open(foreign, "a", encoding="utf-8") as fh:
            fh.write("\n# round-39 c2 foreign-gate-distinguished fixture\n")
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
        # refusal only restates the before-state, not detection.
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
        # Two legacy shapes, both committed classes: the round-38 receipt bytes
        # themselves (wrong generation for this verifier) and an r39 receipt
        # with the verifier binding stripped (the precise new-binding legacy).
        hold = os.path.join(work, "legacy-hold.json")
        run_counter(counter, gate, seed, hold, work)
        hrc, _ = run_verify(hold, gate, counter)
        observed["hold_verify_rc"] = hrc
        observed["receipt"] = os.path.isfile(hold)
        if os.path.isfile(R38_RECEIPT):
            # The r38 receipt binds the r38 expectation table; verify it
            # against THOSE bytes so the demonstrated refusal is the
            # generation binding (predicate-mismatch), not a table artifact.
            vrc, vout = run_verify(R38_RECEIPT, gate, R38_C1,
                                   expectations=R38_EXPECTATIONS)
            observed["r38_receipt_verify_rc"] = vrc
            observed["r38_receipt_verify_fail"] = vout
        else:
            observed["r38_receipt_verify_rc"] = "not-measured"
        unbound = os.path.join(work, "legacy-unbound.json")
        shutil.copyfile(hold, unbound)
        def strip_verifier(r):
            del r["verifier_sha256"]
        doctor(unbound, strip_verifier, re_digest=True)
        vrc, vout = run_verify(unbound, gate, counter)
        observed["unbound_verifier_verify_rc"] = vrc
        observed["unbound_verifier_verify_fail"] = vout

    elif sid == "verifier-subject-rebind":
        if os.environ.get("CHOUSA_R39_NESTED") == "1":
            # This counter is itself running as a subject inside an outer
            # c2 run's cell 3: nesting another level would recurse without
            # bound. The outer run only needs THIS run's receipt bytes; a
            # not-measured observation keeps the rows honest (ok=False is
            # re-derived consistently by the verifier).
            observed["c2_counter_rc"] = "nested-skip"
            observed["subject_swap_verify_rc"] = "nested-skip"
            return {"id": sid, "expect": expect, "observed": observed,
                    "ok": False}
        # Cell 1 (hold): the honest subject receipt verifies under the landed
        # verifier — its verifier_sha256 binds these exact verifier bytes.
        honest = os.path.join(work, "rebind-honest.json")
        run_counter(counter, gate, seed, honest, work)
        hrc, _ = run_verify(honest, gate, counter)
        observed["honest_verify_rc"] = hrc
        # Cell 2: a REPLACED verifier — this file with the census check
        # deleted (the round-38 Erratum-11 weakening: absent the binding it
        # would re-adjudicate silently) — refuses by the verifier binding
        # against the honest receipt.
        replaced = os.path.join(work, "verify-replaced.py")
        with open(VERIFY, "r", encoding="utf-8") as fh:
            vsrc = fh.read()
        # Weaken: the census check's refusal becomes a pass (the round-38
        # Erratum-11 class — absent the verifier binding, this copy would
        # re-adjudicate an edited-table receipt silently). A deleted line
        # would leave an empty if-body (syntax crash, stderr-only), so the
        # replacement keeps the block valid.
        weakened = vsrc.replace(
            '        return fail("scenario-census-mismatch")\n',
            '        pass  # weakened: census refusal removed\n', 1)
        if weakened == vsrc:
            # The census check moved: refuse loudly rather than score a
            # weakened copy that is not weakened.
            observed["replaced_verifier_verify_rc"] = "not-weakened"
            return {"id": sid, "expect": expect, "observed": observed,
                    "ok": False}
        with open(replaced, "w", encoding="utf-8") as fh:
            fh.write(weakened)
        os.chmod(replaced, 0o755)
        vrc, vout = run_verify(honest, gate, counter, verifier=replaced)
        observed["replaced_verifier_verify_rc"] = vrc
        observed["replaced_verifier_verify_fail"] = vout
        # Cell 3: a c2-family receipt (this counter measuring the subject)
        # re-pointed at a DOCTORED SUBJECT COPY — path re-pointed, digest kept
        # honest, receipt re-sealed. The subject binding refuses by name. The
        # nested c2 run carries CHOUSA_R39_NESTED so its own cell 3 skips the
        # next level (one level of nesting is the measurement).
        c2_receipt = os.path.join(work, "rebind-c2.json")
        proc = run_counter(os.path.abspath(__file__), gate, seed,
                           c2_receipt, work,
                           extra_env={"CHOUSA_R39_NESTED": "1"})
        observed["c2_counter_rc"] = proc.returncode
        if not os.path.isfile(c2_receipt):
            observed["subject_swap_verify_rc"] = "no-receipt"
            return {"id": sid, "expect": expect, "observed": observed,
                    "ok": False}
        doctored_subject = os.path.join(work, "c1-count.py")
        with open(counter, "r", encoding="utf-8") as fh:
            ssrc = fh.read()
        # One byte-class change: the doctored copy MUST differ in content
        # (an earlier draft replaced a string with its implicit-concatenation
        # twin — identical bytes, and the swap cell passed vacuously; the
        # c2 run's own 6/8 caught it, exactly the counter's job).
        doctored = ssrc.replace("ENV_PIN_CAPTURE_MATCH",
                                "ENV_PIN_CAPTURE__MATCH", 1)
        if doctored == ssrc:
            observed["subject_swap_verify_rc"] = "not-doctored"
            return {"id": sid, "expect": expect, "observed": observed,
                    "ok": False}
        with open(doctored_subject, "w", encoding="utf-8") as fh:
            fh.write(doctored)
        os.chmod(doctored_subject, 0o755)
        swapped = os.path.join(work, "rebind-swapped.json")
        shutil.copyfile(c2_receipt, swapped)
        def repoint(r):
            r["subject_counter"] = doctored_subject
        doctor(swapped, repoint, re_digest=True)
        vrc, vout = run_verify(swapped, gate,
                               os.path.abspath(__file__))
        observed["subject_swap_verify_rc"] = vrc
        observed["subject_swap_verify_fail"] = vout

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
    ap.add_argument("--seed", type=int, default=39101)
    ap.add_argument("--receipt")
    ap.add_argument("--tmp")
    args = ap.parse_args()

    gate = os.path.abspath(args.gate)
    counter = os.path.abspath(args.counter)
    if args.receipt and os.path.lexists(args.receipt):
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
    expect_sha = sha256_file(EXPECTATIONS)
    verifier_sha = sha256_file(VERIFY)

    work = tempfile.mkdtemp(prefix="chousa-r39-c2-", dir=base_tmp)
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
    # The frozen predicate labels 8/8; the count is the claim, not whatever
    # the table happens to hold.
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
            "subject_counter": counter,
            "subject_counter_sha256": sha256_file(counter),
            "scenarios": rows,
            "matched": matched,
            "total": total,
            "predicate": "RECEIPT_BINDING_MATCH=8/8",
            "predicate_holds": holds,
        }
        receipt["receipt_sha256"] = receipt_digest(receipt)
        with open(args.receipt, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=2, sort_keys=True)
            fh.write("\n")
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
