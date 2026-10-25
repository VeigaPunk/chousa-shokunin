#!/usr/bin/env python3
"""c2-count — frozen counter for round 44 claim C2 (calibration).

Predicate R44-C2, the same sentence as corpus/evidence/round44/claims.md:
36 untracked reports are reverified-commit (stem, round token, sha256,
length > 80) and 3 modified paths are left-named with not hunk-verified.
The all-left table is the cheapest naming-only gate and must fail.

Exit codes: 0 all counts hold · 1 a count failed · 2 usage/env.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
TABLE = LANE / "corpus" / "evidence" / "round44" / "disposition.tsv"

UNTRACKED = (
    '.ufo/waves/round-40/w1/ConnectorSiblingScan.md',
    '.ufo/waves/round-40/w1/CriticC1Control.md',
    '.ufo/waves/round-40/w1/CriticC1Predicate.md',
    '.ufo/waves/round-40/w1/CriticC1Scope.md',
    '.ufo/waves/round-40/w1/CriticC2Calibration.md',
    '.ufo/waves/round-40/w1/CriticR4Disposition.md',
    '.ufo/waves/round-40/w1/CriticSourceClaim.md',
    '.ufo/waves/round-40/w1/ExecC1BaseReceipt.md',
    '.ufo/waves/round-40/w1/ExecC1Count.md',
    '.ufo/waves/round-40/w1/ExecC1LandedReceipt.md',
    '.ufo/waves/round-40/w1/ExecC1MutantReceipt.md',
    '.ufo/waves/round-40/w1/ExecC2Count.md',
    '.ufo/waves/round-40/w1/ExecNoHarm.md',
    '.ufo/waves/round-40/w1/MutateExpectDigest.md',
    '.ufo/waves/round-40/w1/MutateGateDigest.md',
    '.ufo/waves/round-40/w1/MutateVerifierSubject.md',
    '.ufo/waves/round-40/w1/RevengerR1History.md',
    '.ufo/waves/round-40/w1/RevengerR2R5History.md',
    '.ufo/waves/round-40/w1/ReviewActivePopulation.md',
    '.ufo/waves/round-40/w1/ReviewC2Bindings.md',
    '.ufo/waves/round-40/w1/ReviewR2CommitTruth.md',
    '.ufo/waves/round-40/w1/ReviewR3Counts.md',
    '.ufo/waves/round-40/w1/ReviewR4RoleMix.md',
    '.ufo/waves/round-40/w1/ReviewReplacementBindings.md',
    '.ufo/waves/round-40/w1/ScoutFrontierOverlap.md',
    '.ufo/waves/round-40/w1/ScoutHashSource.md',
    '.ufo/waves/round-40/w1/ScoutProvinceBoundary.md',
    '.ufo/waves/round-40/w1/ScribeClaimSurfaces.md',
    '.ufo/waves/round-40/w1/ScribeKnowledgeEntry.md',
    '.ufo/waves/round-40/w1/ScribeLessonGate.md',
    '.ufo/waves/round-40/w1/SentinelFetchScope.md',
    '.ufo/waves/round-40/w1/SentinelWriteScope.md',
    '.ufo/waves/round-40/w1/SimplifierAudit.md',
    '.ufo/waves/round-41/w1/ConnectorSiblingScan.md',
    '.ufo/waves/round-41/w1/ExecC2Before.md',
    '.ufo/waves/round-41/w1/MutateC2Join.md',
)
MODIFIED = (
    '.ufo/waves/round-40/w1/swarm-registry.json',
    '.ufo/waves/round-41/w1/swarm-registry.json',
    'corpus/evidence/round41/receipts/cells/cells.json',
)

def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()

def round_ok(rel: str, text: str) -> bool:
    token = "40" if "/round-40/" in rel else "41"
    low = text.lower()
    return (f"round {token}" in low) or (f"round-{token}" in low) or (f"r{token}" in low)

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--table", default=str(TABLE))
    ap.add_argument("--root", default=str(LANE))
    args = ap.parse_args(argv)
    table = pathlib.Path(args.table)
    root = pathlib.Path(args.root)
    if not table.is_file():
        print("CONSISTENT=0/39")
        print("REVERIFIED=0/36")
        print("LEFT_NAMED=0/3")
        print("C2=FAIL table-missing")
        return 1
    rows = {}
    for line in table.read_text(encoding='utf-8').splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        parts = line.split('\t')
        if len(parts) < 4:
            continue
        rows[parts[0]] = (parts[1], parts[2], parts[3])
    rev = left = consistent = 0
    for rel in UNTRACKED:
        cls, digest, reason = rows.get(rel, ('', '', ''))
        path = root / rel
        ok = False
        if cls == 'reverified-commit' and reason.strip() and path.is_file():
            text = path.read_text(encoding='utf-8', errors='replace')
            stem = path.stem
            ok = stem in text and round_ok(rel, text) and len(text) > 80 and sha256(path) == digest
        if ok:
            rev += 1
            consistent += 1
    for rel in MODIFIED:
        cls, digest, reason = rows.get(rel, ('', '', ''))
        ok = cls == 'left-named' and 'not hunk-verified' in reason and reason.strip()
        if ok:
            left += 1
            consistent += 1
    print("CONSISTENT=%d/39" % consistent)
    print("REVERIFIED=%d/36" % rev)
    print("LEFT_NAMED=%d/3" % left)
    ok = consistent == 39 and rev == 36 and left == 3
    print("C2=%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
