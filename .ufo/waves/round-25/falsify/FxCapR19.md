# FxCapR19 — round-19 capability-row falsification

## Findings
None. The backfilled r19 row describes the demonstrated boundary and is retainable; no historical first-working overclaim found.

## Evidence
- Final full integration pin in private clone: `e93ac711f885a10d44fdd80a1734997419595b5a`.
- `LOG.md:697` says both leaf- and directory-symlink escapes are refused after canonicalizing every expanded match; `LOG.md:701` records r19 **ADMIT**, none harmed, `Capabilities +1`.
- `SCORECARD.md:1319` says the whole sweep is refused when a match canonicalizes outside both roots; first-working round 19. This is the exact behavior, not a claim of eliminating the named limits.
- Source confirms cases 120–121 assert `SWEEP_LOCATION_OUT_OF_CORPUS` + `observed=refused`; case 122 is the in-root control (`tools/research-gate.sh:5115-5160`). The knowledge note records post-expansion, TOCTOU, and `--root /` limitations (`corpus/knowledge/sweep-symlink-r19.md:22-39`).
- Row links resolve in the full pin: `corpus/knowledge/sweep-symlink-r19.md` and all four indexed receipts are present; `corpus/evidence/README.md:986-991` identifies the selftest, demo, battery, and drift records. The demo shows pre-round `SWEEP_CLAIM_FALSE` vs landed `SWEEP_LOCATION_OUT_OF_CORPUS` (`corpus/evidence/symlink-r19-20261019T174500Z-demo.log:1-13`).
- Private-clone `bash tools/research-gate.sh --selftest` ran at `d8c8cff3923f10481ac9ced66d0af7c41d38130c`; it passed. The executable SHA-256 at d8c and full pin e93 is identical: `63a39282a15f19f5b0443212e66ad2dfc8ce0315e65697e479a7206879a598b2`.

Relevant current selftest output only:
```text
ok-case  107 claims-root-slash-absent     exit=1
ok-case  108 claims-root-slash-read       exit=0
ok-case  109 claims-root-slash-xdev       exit=1
ok-case  111 sweeps-root-slash            exit=0
ok-case  120 sweeps-symlink-escape        exit=1
ok-case  121 sweeps-symlink-dir           exit=1
ok-case  122 sweeps-inroot-symlink        exit=1
ok-case  129 chain-fence-anchor           exit=1
ok-case  130 claims-config-start          exit=1
ok-case  131 claims-omp-start             exit=1
ok-case  132 claims-localstate-start      exit=1
ok-case  133 claims-config-adjacent       exit=0
RESEARCH_GATE_SELFTEST: PASS (154 cases, 0 skipped)
```
The adjacent historical-row citations therefore use current indices r15 `107–109,111`, r22 `130–133`, and r23 `129`, as requested; the r19 citation `120–122` includes both escape shapes and the in-root control.

## Residual risk / verification gaps
- The initial `0fc037e6b07f3820ead8c9207a8034ac854197a1` checkpoint is invalid for gate claims: it paired 154-case prose with old gate SHA `752e4e38…` / 136 cases (`SCORECARD.md:1387-1392`; `corpus/lessons/round-25.md:111-125`). Intermediate d8 fixed the gate but still omitted the evidence-index update; the lesson records this at `:127-133`. e93 is the full pin used for pointer checks; its gate matches d8 byte-for-byte.
- No LSP device was exposed in this session; grep was used only to locate fixture lines, not as semantic proof. Behavioral evidence is the executed selftest and the cited demo.
- No tools installed or updated.

VERDICT: Retain the r19 row; its first-working round and described capability are supported by the admitted round-19 demonstration, current cases 120–122, and resolving knowledge/evidence pointers, with the scope limits stated.