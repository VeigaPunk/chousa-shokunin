# ExecC2LandedRederive

## Verdict
Both fresh C2 re-derivations passed 7/7 with exit 0; both receipts record the same gate SHA-256, independently confirmed against the gate bytes.

## Evidence

- Seed 37211 command:
  ```text
  C2_TMP=/tmp/chousa-r37-c2-37211.9DTG9I python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 37211 --receipt /tmp/chousa-r37-c2-37211.9DTG9I/c2-s37211.json; rc=$?; printf 'EXIT_CODE=%s\n' "$rc"; exit "$rc"
  ```
  Observed: all seven scenarios `PASS`; `PIN_CAPTURE_ENV_MATCH=7/7`; `EXIT_CODE=0`.
- Seed 37311 command:
  ```text
  C2_TMP=/tmp/chousa-r37-c2-37311.KB8ewM python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 37311 --receipt /tmp/chousa-r37-c2-37311.KB8ewM/c2-s37311.json; rc=$?; printf 'EXIT_CODE=%s\n' "$rc"; exit "$rc"
  ```
  Observed: all seven scenarios `PASS`; `PIN_CAPTURE_ENV_MATCH=7/7`; `EXIT_CODE=0`.
- Receipt fields read from `/tmp/chousa-r37-c2-37211.9DTG9I/c2-s37211.json` and `/tmp/chousa-r37-c2-37311.KB8ewM/c2-s37311.json` (seed, gate, gate_sha256, matched, total, predicate, predicate_holds):
  ```text
  [37211,"/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh","9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39",7,7,"PIN_CAPTURE_ENV_MATCH=7/7",true]
  [37311,"/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh","9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39",7,7,"PIN_CAPTURE_ENV_MATCH=7/7",true]
  ```
- Independent command: `sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`
  Observed: `9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`.

## Findings
1. C2 freshness predicate is satisfied on both requested fresh seeds; each receipt records `matched=7`, `total=7`, and `predicate_holds=true`. Pointers: the two receipts and counter outputs above.
2. Both receipt pins equal the independently re-derived gate digest `9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39`. Pointers: receipt `gate_sha256` fields and `sha256sum` output above.

## Limits
The seat boundary allows writing only this report in the lane and temp artifacts under `/tmp`; therefore receipts are at the two `/tmp` paths above, not the requested persistent `.../w1/ExecC2LandedRederive/` directory. No source or other lane files were changed; no tools were installed.
