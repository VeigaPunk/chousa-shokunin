#!/usr/bin/env bash
# Driver: run C1/C2 counters over all baseline controls, 3 fresh seeds each.
# Usage: bash driver.sh <controls_out_dir>
set -u
LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin
SBX=/fast/scratch/hyaku/chousa-r31/CtlBaselineJunk
OUT="${1:-$LANE/.ufo/waves/round-31/controls/CtlBaselineJunk}"
mkdir -p "$OUT"

declare -a CONTROLS=(base junk s_supported s_mislocated s_invalid s_unsupported s_stale s_none label)
declare -a GATES=(
  "tools/research-gate.sh"
  "$SBX/junk.sh"
  "$SBX/stub_supported.sh"
  "$SBX/stub_mislocated.sh"
  "$SBX/stub_invalid.sh"
  "$SBX/stub_unsupported.sh"
  "$SBX/stub_stale.sh"
  "$SBX/stub_none.sh"
  "$SBX/label_keyed.sh"
)
SEEDS=(1001 2002 3003)

cd "$LANE"
for counter in c1 c2; do
  for i in "${!CONTROLS[@]}"; do
    ctl="${CONTROLS[$i]}"; gate="${GATES[$i]}"
    for seed in "${SEEDS[@]}"; do
      rcpt="$OUT/${counter}_${ctl}_seed${seed}.json"
      echo "RUN ${counter} ${ctl} seed=${seed}"
      timeout 900 python3 "corpus/evidence/round31/${counter}-count.py" \
        --gate "$gate" --seed "$seed" --receipt "$rcpt" \
        >/tmp/ctl_${counter}_${ctl}_${seed}.out 2>&1
      r=$?
      echo "  rc=$r $(grep -E 'MATCH=' /tmp/ctl_${counter}_${ctl}_${seed}.out | head -1)"
      if [ ! -s "$rcpt" ]; then echo "  MISSING RECEIPT $rcpt"; exit 3; fi
    done
  done
done
echo DONE
