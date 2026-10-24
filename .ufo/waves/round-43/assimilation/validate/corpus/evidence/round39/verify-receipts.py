#!/usr/bin/env python3
"""Round-39 receipt verifier — re-derives every binding a counter receipt claims.

Extends the round-38 verifier (whose kills it keeps: census, expect-tie,
ok re-derivation, type checks, strict schema) with the round-39 bindings that
close the round-38 Erratum 2/11 carried debt, demonstrated live twice:

  verifier_sha256        the digest of THIS verifier file at receipt time, bound
                         by the counter into every round-39 receipt. A replaced
                         (weakened or doctored) verifier copy cannot silently
                         re-adjudicate old receipts: its bytes hash differently
                         and the first binding check refuses by name.
  subject_counter_sha256 (c2-family receipts only) the digest of the subject
                         counter the c2 run measured, bound alongside its path.
                         Re-pointing a receipt at a different subject (or a
                         doctored copy of the same one) without re-deriving the
                         digest refuses `subject-counter-sha256-mismatch`;
                         a missing subject path refuses `subject-counter-
                         unreadable`. Re-pointing WITH a re-derived digest is a
                         new self-consistent receipt, not a forgery of an old
                         one — the round-37 F2 residual class, named in
                         claims.md §Limits, out of scope for the binding.

Usage:
  python3 corpus/evidence/round39/verify-receipts.py --receipt F --gate G \
      --counter C [--expectations E]

Exit 0 and one `VERIFY: ok ...` line when every binding re-derives; exit 1 and
`VERIFY-FAIL: <which>` naming the first failed binding otherwise. Receipts from
the round-37 or round-38 counters (no verifier/subject binding fields) fail
closed as `VERIFY-FAIL: missing-field <name>`, never a silent accept; each
round's receipts stay verified by that round's own committed verifier.

Limits (carried from round 38, narrowed in claims.md): this certifies
integrity and self-consistency against committed bytes — body, file bindings,
frozen census, arithmetic, verifier and subject identity. It does not
authenticate authorship: a fabricator holding the public hashes who reproduces
honest observations can write a receipt indistinguishable from an honest one.
Receipt-path symlink identity is not bound (the body is what is verified).
"""
import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_EXPECTATIONS = os.path.join(HERE, "expectations.jsonl")

# counter basename -> (family key in expectations.jsonl, frozen predicate,
#                      family-specific required binding fields)
FAMILIES = {
    "c1-count.py": ("c1", "ENV_PIN_CAPTURE_MATCH=8/8",
                    ("verifier_sha256",)),
    "c2-count.py": ("c2", "RECEIPT_BINDING_MATCH=8/8",
                    ("verifier_sha256", "subject_counter",
                     "subject_counter_sha256")),
}

REQUIRED = ("counter_sha256", "expect_sha256", "gate_sha256_pre",
            "gate_sha256_post", "receipt_sha256", "scenarios", "matched",
            "total", "predicate_holds", "predicate")

# Strict schema: a receipt is exactly this field set. An added field is a
# doctoring of the body — re-sealed or not, it must refuse (round-38
# Erratum 9). Round-39 fields enter the known set.
KNOWN = set(REQUIRED) | {"counter", "expectations", "seed", "gate",
                         "gate_sha256", "subject_counter",
                         "verifier", "verifier_sha256",
                         "subject_counter_sha256"}


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


def load_frozen_expectations(path, family):
    frozen = {}
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if row.get("counter") == family:
                frozen[row["id"]] = row["expect"]
    return frozen


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
    unknown = sorted(set(receipt) - KNOWN)
    if unknown:
        return fail("unknown-field %s" % ",".join(unknown))

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

    family = FAMILIES.get(os.path.basename(args.counter))
    if family is None:
        return fail("unknown-counter %s" % os.path.basename(args.counter))
    fam_key, fam_predicate, fam_required = family
    if receipt.get("predicate") != fam_predicate:
        return fail("predicate-mismatch")
    for key in fam_required:
        if key not in receipt:
            return fail("missing-field %s" % key)

    frozen = load_frozen_expectations(args.expectations, fam_key)
    scenarios = receipt["scenarios"]
    if not isinstance(scenarios, list):
        return fail("scenarios-not-a-list")
    if any(not isinstance(s, dict) or not isinstance(s.get("id"), str)
           for s in scenarios):
        return fail("scenario-row-malformed")
    # Strict types: Python equality launders 1 == True and 7.0 == 7, which a
    # strict JSON consumer would not accept (round-38 Erratum 10).
    if any(not isinstance(s.get("ok"), bool) for s in scenarios):
        return fail("ok-type-mismatch")
    if type(receipt["matched"]) is not int or type(receipt["total"]) is not int:
        return fail("count-type-mismatch")
    if not isinstance(receipt["predicate_holds"], bool):
        return fail("predicate-holds-type-mismatch")
    ids = sorted(s.get("id") for s in scenarios
                 if isinstance(s, dict)) if scenarios else []
    if len(scenarios) != len(frozen) or ids != sorted(frozen):
        return fail("scenario-census-mismatch")
    matched = 0
    for row in scenarios:
        sid = row["id"]
        want = frozen[sid]
        if row.get("expect") != want:
            return fail("expect-tie-mismatch %s" % sid)
        observed = row.get("observed")
        if not isinstance(observed, dict):
            return fail("observed-not-an-object %s" % sid)
        # Keys ending in _contains are harness assertion annotations, not
        # receipt-observable equalities; the equality keys are re-derived.
        ok = all(observed.get(k) == v for k, v in want.items()
                 if not k.endswith("_contains"))
        if row.get("ok") != ok:
            return fail("ok-rederivation-mismatch %s" % sid)
        matched += 1 if ok else 0
    if receipt["matched"] != matched:
        return fail("matched-recount-mismatch")
    if receipt["total"] != len(scenarios):
        return fail("total-recount-mismatch")
    if receipt["predicate_holds"] != (matched == len(scenarios)):
        return fail("predicate-holds-inconsistent")

    # Round-39 binding: the verifier that is re-adjudicating this receipt IS
    # the verifier the receipt binds (a replaced copy refuses by name before
    # any other check runs).
    if receipt["verifier_sha256"] != sha256_file(os.path.abspath(__file__)):
        return fail("verifier-sha256-mismatch")

    # Round-39 binding (c2 family only): the subject counter the run measured
    # — its path must be readable and its bytes must equal the bound digest.
    if fam_key == "c2":
        subject = receipt["subject_counter"]
        if not isinstance(subject, str) or not os.path.isfile(subject):
            return fail("subject-counter-unreadable %s" % subject)
        if receipt["subject_counter_sha256"] != sha256_file(subject):
            return fail("subject-counter-sha256-mismatch")

    if not os.path.isfile(args.gate):
        return fail("gate-unreadable %s" % args.gate)
    gate_sha = sha256_file(args.gate)
    if receipt["gate_sha256_pre"] != receipt["gate_sha256_post"]:
        return fail("gate-sha-changed-across-run")
    if receipt["gate_sha256_pre"] != gate_sha:
        return fail("gate-sha256-mismatch")
    if receipt.get("gate_sha256") != gate_sha:
        return fail("gate-sha-alias-mismatch")

    print("VERIFY: ok receipt=%s gate=%s counter=%s" %
          (os.path.basename(args.receipt), os.path.basename(args.gate),
           os.path.basename(args.counter)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
