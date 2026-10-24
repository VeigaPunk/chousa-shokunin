#!/usr/bin/env python3
"""Round-38 receipt verifier — re-derives every binding a counter receipt claims.

A round-38 counter receipt binds, measured by the counter itself (never by the
gate under test):

  gate_sha256_pre / gate_sha256_post  the gate file's digest before the first
                                      and after the last scenario invocation;
                                      the counter refuses to publish when they
                                      differ (the round-37 residual F1: a gate
                                      that rewrites itself mid-run got a receipt
                                      stamped with bytes that did not run every
                                      scenario)
  counter_sha256                      the digest of the counter file that scored
                                      the run (the round-37 residual F4: the
                                      receipt carried no counter identity)
  expect_sha256                       the digest of the frozen expectation
                                      table (expectations.jsonl)
  receipt_sha256                      the digest of the receipt's own canonical
                                      body (every other field, same
                                      serialization) — any field doctoring is
                                      detected

Usage:
  python3 corpus/evidence/round38/verify-receipts.py --receipt F --gate G \
      --counter C [--expectations E]

Exit 0 and one `VERIFY: ok ...` line when every binding re-derives; exit 1 and
`VERIFY-FAIL: <which>` naming the first failed binding otherwise. A receipt from
the round-37 counters (no binding fields at all) fails closed as
`VERIFY-FAIL: missing-field gate_sha256_pre`, never a silent accept.
"""
import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_EXPECTATIONS = os.path.join(HERE, "expectations.jsonl")

REQUIRED = ("counter_sha256", "expect_sha256", "gate_sha256_pre",
            "gate_sha256_post", "receipt_sha256", "scenarios", "matched",
            "total", "predicate_holds")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def receipt_digest(receipt):
    body = {k: v for k, v in receipt.items() if k != "receipt_sha256"}
    text = json.dumps(body, indent=2, sort_keys=True) + "\n"
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fail(which):
    print("VERIFY-FAIL: %s" % which)
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--gate", required=True)
    ap.add_argument("--counter", required=True)
    ap.add_argument("--expectations", default=DEFAULT_EXPECTATIONS)
    args = ap.parse_args()

    try:
        with open(args.receipt, "r", encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        return fail("unreadable-receipt %s" % exc)
    if not isinstance(receipt, dict):
        return fail("receipt-not-an-object")

    for key in REQUIRED:
        if key not in receipt:
            return fail("missing-field %s" % key)

    if receipt["receipt_sha256"] != receipt_digest(receipt):
        return fail("receipt-self-digest")

    if not os.path.isfile(args.counter):
        return fail("counter-unreadable %s" % args.counter)
    if receipt["counter_sha256"] != sha256_file(args.counter):
        return fail("counter-sha256-mismatch")

    if not os.path.isfile(args.expectations):
        return fail("expectations-unreadable %s" % args.expectations)
    if receipt["expect_sha256"] != sha256_file(args.expectations):
        return fail("expect-sha256-mismatch")

    if not os.path.isfile(args.gate):
        return fail("gate-unreadable %s" % args.gate)
    gate_sha = sha256_file(args.gate)
    if receipt["gate_sha256_pre"] != receipt["gate_sha256_post"]:
        return fail("gate-sha-changed-across-run")
    if receipt["gate_sha256_pre"] != gate_sha:
        return fail("gate-sha256-mismatch")
    if receipt.get("gate_sha256") != gate_sha:
        return fail("gate-sha-alias-mismatch")

    scenarios = receipt["scenarios"]
    if not isinstance(scenarios, list):
        return fail("scenarios-not-a-list")
    matched = sum(1 for s in scenarios if isinstance(s, dict) and s.get("ok"))
    if receipt["matched"] != matched:
        return fail("matched-recount-mismatch")
    if receipt["total"] != len(scenarios):
        return fail("total-recount-mismatch")
    if receipt["predicate_holds"] != (matched == len(scenarios)):
        return fail("predicate-holds-inconsistent")

    print("VERIFY: ok receipt=%s gate=%s counter=%s" %
          (os.path.basename(args.receipt), os.path.basename(args.gate),
           os.path.basename(args.counter)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
