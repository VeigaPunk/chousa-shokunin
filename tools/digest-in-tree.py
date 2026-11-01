#!/usr/bin/env python
"""R67-C2 receipt-digest provenance checker: every sha256 a receipt pins must
re-derive from bytes committed in the repository (the object database).

Routed defect (round-66 verifier spot-check item 2): a before-receipt pinned
ENTRY_SHA256/REGISTRY_SHA256 values from a scratch clone whose mutated bytes
were never committed, so no reader could re-derive them. This tool closes the
class for new receipts: it extracts every 64-hex sha256 pin from a receipt and
checks each against sha256 of committed blob bytes -- by default all blobs
reachable at --revision (default HEAD), with --all-objects every blob object
in the repository's object database (history plus unreachable objects). A
receipt with no digest pin exits 2 (fail-closed: no vacuous pass). The verdict
certifies re-derivability only: not which command produced the bytes, not
execution authenticity (tools/receipt-pin.py covers receipt-header consistency
against a named revision), and not entailment.

Usage:
    python tools/digest-in-tree.py --receipt <receipt.txt> [--lane <lane-root>]
        [--revision <rev>] [--all-objects]

Exit contract: 0 = every pinned digest re-derives from committed bytes
(DIGEST_IN_TREE=PASS); 1 = at least one pinned digest is out of tree
(DIGEST_IN_TREE=FAIL); 2 = usage/environment (missing --receipt, unreadable
receipt, git unavailable, revision unresolvable, or no 64-hex digest in the
receipt) with DIGEST_IN_TREE=ERROR on stderr.
"""
import argparse
import hashlib
import re
import subprocess
import sys

HEX64_RE = re.compile(r"\b[0-9a-fA-F]{64}\b")


def die_env(msg):
    print("DIGEST_IN_TREE=ERROR %s" % msg, file=sys.stderr)
    raise SystemExit(2)


def run_git(args, lane):
    try:
        proc = subprocess.run(
            ["git", "-C", lane] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        die_env("git unavailable: %s" % exc)
    if proc.returncode != 0:
        die_env("git %s failed: %s" % (args[0], proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout


def extract_digests(text):
    seen = []
    for tok in HEX64_RE.findall(text):
        low = tok.lower()
        if low not in seen:
            seen.append(low)
    return seen


def list_blobs(lane, revision, all_objects):
    """Return list of (oid, path_or_empty) blob descriptors."""
    if all_objects:
        out = run_git(
            ["cat-file", "--batch-all-objects", "--batch-check=%(objectname) %(objecttype)"],
            lane,
        ).decode("ascii", "replace")
        blobs = []
        for line in out.splitlines():
            parts = line.split()
            if len(parts) == 2 and parts[1] == "blob":
                blobs.append((parts[0], ""))
        return blobs
    out = run_git(["rev-parse", "--verify", revision], lane).decode("ascii", "strip")
    rev = out.strip()
    raw = run_git(["ls-tree", "-r", "-z", rev], lane)
    blobs = []
    for entry in raw.split(b"\0"):
        if not entry:
            continue
        meta, _, path = entry.partition(b"\t")
        fields = meta.decode("ascii", "replace").split()
        if len(fields) >= 3 and fields[1] == "blob":
            blobs.append((fields[2], path.decode("utf-8", "replace")))
    return blobs, rev


def sha256_of_blobs(lane, oids):
    """Return {oid: sha256hex} by streaming git cat-file --batch.

    Strict request-response (write one oid, read one payload) so neither pipe
    can fill while the other side is blocked: pre-writing every request
    deadlocks once the oids exceed the pipe buffer.
    """
    proc = subprocess.Popen(
        ["git", "-C", lane, "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    digests = {}
    out = proc.stdout
    for oid in oids:
        try:
            proc.stdin.write((oid + "\n").encode("ascii"))
            proc.stdin.flush()
        except OSError as exc:
            proc.kill()
            die_env("cat-file write failed: %s" % exc)
        header = out.readline()
        if not header:
            break
        parts = header.decode("ascii", "replace").split()
        if len(parts) != 3 or parts[1] == "missing":
            continue
        size = int(parts[2])
        h = hashlib.sha256()
        remaining = size
        while remaining > 0:
            chunk = out.read(min(65536, remaining))
            if not chunk:
                break
            h.update(chunk)
            remaining -= len(chunk)
        out.read(1)  # trailing newline after the payload
        digests[parts[0]] = h.hexdigest()
    proc.stdin.close()
    proc.wait()
    return digests


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--lane", default=".")
    ap.add_argument("--revision", default="HEAD")
    ap.add_argument("--all-objects", action="store_true")
    args = ap.parse_args()

    try:
        with open(args.receipt, "rb") as fh:
            text = fh.read().decode("utf-8", "replace")
    except OSError as exc:
        die_env("unreadable receipt: %s" % exc)

    digests_wanted = extract_digests(text)
    if not digests_wanted:
        die_env("NO_DIGESTS: no 64-hex sha256 pin found in %s" % args.receipt)

    lane_rev = run_git(["rev-parse", "HEAD"], args.lane).decode("ascii", "strip").strip()
    blobs = list_blobs(args.lane, args.revision, args.all_objects)
    if args.all_objects:
        blobs = blobs  # (oid, "") tuples
    else:
        blobs, rev_resolved = blobs
    oids = [oid for oid, _ in blobs]
    computed = sha256_of_blobs(args.lane, oids)

    in_tree = 0
    lines = []
    lines.append("LANE_REVISION=%s" % lane_rev)
    lines.append("MODE=%s SCANNED_BLOBS=%d" % ("all-objects" if args.all_objects else "rev", len(oids)))
    for want in digests_wanted:
        hit = None
        for oid, path in blobs:
            if computed.get(oid) == want:
                hit = (oid, path)
                break
        if hit is None:
            lines.append("DIGEST %s OUT_OF_TREE" % want)
        else:
            in_tree += 1
            where = "oid=%s" % hit[0] if not hit[1] else "path=%s oid=%s" % (hit[1], hit[0])
            lines.append("DIGEST %s IN_TREE %s" % (want, where))
    total = len(digests_wanted)
    ok = in_tree == total
    lines.append("DIGESTS_IN_TREE=%d/%d DIGEST_IN_TREE=%s" % (in_tree, total, "PASS" if ok else "FAIL"))
    lines.append("EXIT=%d" % (0 if ok else 1))
    print("\n".join(lines))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
