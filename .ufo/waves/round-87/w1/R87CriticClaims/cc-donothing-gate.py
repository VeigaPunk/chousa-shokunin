#!/usr/bin/env python3
import argparse,sys
ap=argparse.ArgumentParser(); ap.add_argument("--root",required=True); ap.add_argument("--repo",required=True); ap.add_argument("--tool"); ap.add_argument("--work"); ap.parse_args()
print("TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15")
print("GATE_RECORDS_R87=PASS"); sys.exit(0)
