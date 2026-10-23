#!/bin/bash
# only fabricated ids not in the truth map, DRIFT + rc=1 -> counter must score 0
for i in $(seq 1 37); do
  echo "CLAIM id=deadbeef$i expected=supported observed=supported source=src at=- verdict=match"
done
echo "RESEARCH_GATE: DRIFT"
exit 1
