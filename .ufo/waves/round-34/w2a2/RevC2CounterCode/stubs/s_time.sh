#!/bin/bash
# outlives the (patched) gate timeout: must score every record none, gate_timed_out=true
sleep 5
echo "CLAIM id=whatever expected=supported observed=supported source=src at=- verdict=match"
echo "RESEARCH_GATE: DRIFT"
exit 1
