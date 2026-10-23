#!/bin/bash
# CriticEdgeC2 repro (round 31 wave 2). Run from this dir. Reads only; writes only under /fast/scratch.
# Lane gate run below is read-only; mutants are copies in scratch, never the lane file.
set -u
S=/fast/scratch/hyaku/chousa-r31/w2/CriticEdgeC2
LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE

echo "== gate identity =="
sha256sum "$LANE/tools/research-gate.sh" "$S/clone/tools/research-gate.sh"

echo "== rebuild fixtures (edge + pin probes) =="
python3 "$S/build-edge.py" "$S/edge-root" >/dev/null

echo "== D-A/D-B/D-C: landed gate on hand-built edges (exit 1) =="
cd "$S/edge-root" && env -u CHOUSA_ROOT timeout 600 bash "$S/clone/tools/research-gate.sh" \
  verify-claims claims.jsonl --root . 2>&1 | grep -E "^CLAIM id=(E18|E19|E26|E27|E04|E06|E09|E10)|REVISION_MISMATCH"

echo "== counter baseline on the landed gate =="
cd "$S/clone" && timeout 900 python3 corpus/evidence/round31/c2-count.py --seed 777001 \
  --gate tools/research-gate.sh --receipt "$S/receipt-baseline.json" | grep REVISION_BINDING_MATCH

echo "== correction 1+2 on a scratch copy (counter stays 120/120) =="
cd "$S/clone" && timeout 900 python3 corpus/evidence/round31/c2-count.py --seed 99001 \
  --gate "$S/mutant-f1f2.sh" --receipt "$S/receipt-f1f2-seed99001.json" | grep REVISION_BINDING_MATCH
