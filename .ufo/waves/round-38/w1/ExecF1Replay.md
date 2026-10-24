# ExecF1Replay

## Verdict
Reproduced the round-37 F1 acceptance and round-38 changed-gate refusal on fresh seeds; the receipt gate hash equals the target hash.

## Evidence
- Isolated workspace: `/tmp/chousa-r38-f1-replay.C4yRgP/`. The shim embeds a pin baseline captured from the target, emits a synthetic first `--pin` answer or `hold-stale` answer from its own bytes, then copies the target gate over `$0`. Before each counter run, the same shim path was restored from the identical template; the r38 run itself replaced it with target bytes.
- Baseline setup command: `mkdir -p /tmp/chousa-r38-f1-replay.C4yRgP/probe && bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --pin /tmp/chousa-r38-f1-replay.C4yRgP/probe/baseline; status=$?; printf 'PIN_EXIT=%s\n' "$status"`

  Observed:
  ```text
  GATE_PIN: ok path=/tmp/chousa-r38-f1-replay.C4yRgP/probe/baseline gate_sha256=37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d
  PIN_EXIT=0
  ```
- Round-38 command (seed `38238`): `cp /tmp/chousa-r38-f1-replay.C4yRgP/attack.template /tmp/chousa-r38-f1-replay.C4yRgP/attacking-gate.sh && C1_TMP=/tmp/chousa-r38-f1-replay.C4yRgP C2_TMP=/tmp/chousa-r38-f1-replay.C4yRgP python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py --gate /tmp/chousa-r38-f1-replay.C4yRgP/attacking-gate.sh --seed 38238 --receipt /tmp/chousa-r38-f1-replay.C4yRgP/r38-receipt.json; status=$?; printf 'EXIT=%s\n' "$status"; if test -e /tmp/chousa-r38-f1-replay.C4yRgP/r38-receipt.json; then printf 'RECEIPT=PRESENT\n'; else printf 'RECEIPT=ABSENT\n'; fi`

  Verbatim output:
  ```text
  c1-count: gate bytes changed across the run (pre 61822c8c8b6de6f4 != current) — no receipt published
  EXIT=2
  RECEIPT=ABSENT
  ```
- Round-37 command (seed `38239`): `cp /tmp/chousa-r38-f1-replay.C4yRgP/attack.template /tmp/chousa-r38-f1-replay.C4yRgP/attacking-gate.sh && C1_TMP=/tmp/chousa-r38-f1-replay.C4yRgP C2_TMP=/tmp/chousa-r38-f1-replay.C4yRgP python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round37/c1-count.py --gate /tmp/chousa-r38-f1-replay.C4yRgP/attacking-gate.sh --seed 38239 --receipt /tmp/chousa-r38-f1-replay.C4yRgP/r37-receipt.json; status=$?; printf 'EXIT=%s\n' "$status"; printf 'POST_RUN_GATE_SHA256='; sha256sum /tmp/chousa-r38-f1-replay.C4yRgP/attacking-gate.sh; printf 'TARGET_GATE_SHA256='; sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`

  Verbatim output:
  ```text
  PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
  PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
  PASS sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
  PASS cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
  PASS sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
  PASS sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
  PASS cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
  CLAIM_PIN_PROVENANCE_MATCH=7/7
  EXIT=0
  POST_RUN_GATE_SHA256=37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d  /tmp/chousa-r38-f1-replay.C4yRgP/attacking-gate.sh
  TARGET_GATE_SHA256=37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d  /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
  ```
- Read of `/tmp/chousa-r38-f1-replay.C4yRgP/r37-receipt.json` (`gate`, `gate_sha256`, `seed`, `matched`, `total`, `predicate_holds`):
  ```json
  {
    "gate": "/tmp/chousa-r38-f1-replay.C4yRgP/attacking-gate.sh",
    "gate_sha256": "37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d",
    "seed": 38239,
    "matched": 7,
    "total": 7,
    "predicate_holds": true
  }
  ```

## Findings
1. Round-38 counter detects the shim's first-invocation replacement and exits 2 without a receipt; the stderr names the changed gate. This is the frozen C2 changed-gate behavior (`corpus/evidence/round38/c1-count.py:218-228`; `corpus/evidence/round38/claims.md:74-84`).
2. Round-37 counter accepts the same self-restoring shim path at 7/7, then stamps the receipt with target bytes despite the synthetic first scenario (`corpus/evidence/round37/c1-count.py:170-177`; `.ufo/waves/round-37/residual/RevC1FreshSeed.md:31-51`). Post-run shim and target SHA-256 both equal `37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d`.

## Limits
One fresh seed per counter was exercised (`38238`, `38239`). The shim was reset from the same template between runs because the first run restores the target over itself; both runs used the same gate pathname. Temporary attack files remain only under `/tmp/chousa-r38-f1-replay.C4yRgP`.
