# Round 25 — ExecHoldsBaseline

- Private clone: `/tmp/chousa-r25-ExecHoldsBaseline`, branch `r25-ExecHoldsBaseline`; observed `git rev-parse HEAD` = `b820e4e40ce52deedf53b191140cd7b08ddda929`.
- All gate invocations ran from that clone root. `verify-all`/`verify-claims` used the requested `--root /home/vgpnk/Projects/shokunin`; no `--json` was supplied.
- Claims binding followed `corpus/evidence/README.md:791-799` (r9 uses explicit `claims-r9.jsonl`) and `:422-436`, `:531-546` (the full-r6/integrity recipes omit `--claims`; their records declare companion files at `full-r6.md:8`, `full-r6-broken.md:8`, `integrity-r7.md:8`, `integrity-r7-broken.md:8`). Sweeps/chain were run without a separate claims file, as assigned. Command/output pairs below are the retained observations.

## Exact commands and observed output

- `bash tools/research-gate.sh --selftest` → `RESEARCH_GATE_SELFTEST: PASS (136 cases, 0 skipped)`, exit 0 (`holds/selftest.log`).
- `bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r12-20261019T115519Z.json` → `GATE_DRIFT: none`, exit 0 (`holds/drift-r12.log`).
- `bash tools/research-gate.sh verify-all corpus/fixtures/archives-r9/A-r9.md --claims corpus/fixtures/claims-r9.jsonl --root /home/vgpnk/Projects/shokunin` → CLEAN, exit 0 (`holds/verify-all-A-r9.log`).
- Same command for `corpus/fixtures/archives-r9/B-r9.md` → CLEAN, exit 0 (`holds/verify-all-B-r9.log`).
- Same command for `corpus/fixtures/archives-r9/C-r9.md` → CLEAN, exit 0 (`holds/verify-all-C-r9.log`).
- `bash tools/research-gate.sh verify-all corpus/fixtures/full-r6.md --root /home/vgpnk/Projects/shokunin` → CLEAN, exit 0 (`holds/verify-all-full-r6.log`).
- `bash tools/research-gate.sh verify-all corpus/fixtures/full-r6-broken.md --root /home/vgpnk/Projects/shokunin` → DRIFT, 2 drift sections / 2 findings, exit 1 (`holds/verify-all-full-r6-broken.log`).
- `bash tools/research-gate.sh verify-all corpus/fixtures/integrity-r7.md --root /home/vgpnk/Projects/shokunin` → CLEAN, exit 0 (`holds/verify-all-integrity-r7.log`).
- `bash tools/research-gate.sh verify-all corpus/fixtures/integrity-r7-broken.md --root /home/vgpnk/Projects/shokunin` → DRIFT, 1 drift section / 2 findings, exit 1 (`holds/verify-all-integrity-r7-broken.log`).
- `bash tools/research-gate.sh verify-all corpus/fixtures/sweeps-r5.md --root /home/vgpnk/Projects/shokunin` → CLEAN, exit 0 (`holds/verify-all-sweeps-r5.log`).
- `bash tools/research-gate.sh verify-all corpus/fixtures/chain-r3.md --root /home/vgpnk/Projects/shokunin` → DRIFT, 1 finding: `SWEEP_REJECTION_INCOMPLETE` (`id=R1 missing=flip`), exit 1 (`holds/verify-all-chain-r3.log`).
- `bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root /home/vgpnk/Projects/shokunin` → CLEAN, `VERDICT_BEARING_CLAIMS=17/17`, exit 0 (`holds/verify-claims-r2.log`; recipe command: `corpus/evidence/README.md:63-66`).

## Retained files and SHA-256

- `/tmp/chousa-r25-ExecHoldsBaseline/battery.sh` — `a1dd22c5550faf08513a27bfe0fadc2f8d4534c3094717e6545b508b6e04bfc5`
- `holds/selftest.log` — `469c466a53c01afbf90cd051509d1ee4b5bce5a68001a322408ed545cbe19fb5`
- `holds/drift-r12.log` — `8d50a12c560c6839bc707219d2fb8787bdb6e6495c327aa23d9b554dce90e8a1`
- `holds/verify-all-A-r9.log` — `87751cda1b534bf08e1b35de1f5215cbbb83cc9dafcda7faa42fd78cb4b61ef5`
- `holds/verify-all-B-r9.log` — `09f869eb5361dec9144ff39dd4e5e99361338a1157e089b949ab0f80bb565bb6`
- `holds/verify-all-C-r9.log` — `5cd6c4f32543fb43e2d6bddd0c034ae693d072bd3c451cd628fb32db4bf5b8d0`
- `holds/verify-all-full-r6.log` — `fdac615aa9eb6c7e201fab84587ce1d023f461950bd1830c8e22f99b25a9efb3`
- `holds/verify-all-full-r6-broken.log` — `aa9f9a7a1a2ca8a775141a1353041974d9b9f2277c6f0008e7ab11cc29ea1fb8`
- `holds/verify-all-integrity-r7.log` — `d0991ca17e26bf5cbd18b0db47ec72a40dcf7b1160b6263dbed1235f12d1f25e`
- `holds/verify-all-integrity-r7-broken.log` — `0b446dcaa2aab39aa1fffe856ca70830606bf4bfdead3bfc5b6d8e82e0b8c8e5`
- `holds/verify-all-sweeps-r5.log` — `8992142baa3c1875e6bbb409a4592fb30ef4549420552bc93f2a9b89478ba16a`
- `holds/verify-all-chain-r3.log` — `e056c455ca25a42d45529c5a1cfbab21d6dcc57c1a30587a5735efe2f7abe263`
- `holds/verify-claims-r2.log` — `42b14a19ef1e1a293b11081538adc9532ca9ded2cb21f79bc0a22bcc8a5913d7`

`battery.sh TREE_ROOT [ANALYSIS_ROOT]` reruns this command list against the saved logs; its default analysis root is the exact requested absolute path. It adds and diffs recorded exit codes, normalizing only `ts` and `gate_sha256` values while retaining the rest of each line. The script was written but not run as a second comparison pass. Chain-r3's observed DRIFT is part of this baseline, not normalized away.

LSP was not available in the mounted tool inventory; this shell-only task required no symbol lookup/refactor. Installs/updates: none.

VERDICT: Hold battery captured in the b820e4e private clone; 12 command logs and the rerun/diff script are retained with hashes above.
