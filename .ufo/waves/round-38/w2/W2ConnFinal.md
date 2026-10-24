# W2ConnFinal

## Verdict
Chousa still absorbs nothing: the narrowing shares no object with the seven lanes; drop wave-1's PATH-inside-7/7 wording, and do not map C2 onto kotodama's single `gate_sha256` or kumitate's authorship ledger.

## Evidence
Axes: operability (C1, name-`env` interposition only), calibration (C2, committed-byte integrity, not authorship). No counter, no seed. No tool installed.

Re-executed 2026-10-24 (python3 + read-only `git`), fleet read-only:

1. `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master` → `8e93bc916527b3c21f0f702967fa65c3b4c31699`. Sibling HEAD: kumitate `ac5674393f68fb6510be48ad3fb3b20ebf4e1cc4`, kake `e54552553eaff4d7033dc2df299300fc056f4a0d`, mori `b2ef71b82195f6638e489a9d6b8eb37ce5db48d5`, kotodama `17c32302c6845c8f164b985a8cb312d3181c8788`, kaidoku `f432c8e3bc58934887c83f1db2b26f9910a9d87f`, kotoba `c019919c97ab5fe98e87a7754b4449ea4e699c99`, tsukuroi `189d8a080ba8d508d5faab12cad9e688aee91dab`.

2. Token counts, `SCORECARD.md`+`PROVINCE.md` only. Chousa: `BASH_FUNC` 2, `research-gate` 33, `gate_sha256` 5, `LD_PRELOAD` 3, `loader-env` 1. Kumitate: `receipt-attest` 7 and none of those. Tsukuroi: `LD_PRELOAD` 4, `loader-env` 6, no `BASH_FUNC`. Kake, mori, kotodama, kaidoku, kotoba: none.

3. Whole-tree `git grep -l` on the seven siblings: `gate_sha256_pre`, `gate_sha256_post`, `ENV_PIN_CAPTURE_MATCH`, `RECEIPT_BINDING_MATCH`, `gate_canonical_capture` → 0 files each. `BASH_FUNC` prose: only `tsukuroi-shokunin/.ufo/waves/round-12/Security.md:93`. Kaidoku hits are round-34 ELF `.bin` fixtures, not claim text.

4. Bare `gate_sha256` (not pre/post): kotodama 831 text hits; the schema is `kotodama-frozen-run-v1` at `kotodama-shokunin/corpus/knowledge/verification/gate-frozen-run-standard.md:86` ("lane convention, not in the fleet clause"); a difference is `gate_revised`, exit 2 (`:123-132`). Mori 86 hits are round-15 probe pins (e.g. `.ufo/waves/round-15/boundary-expected.json:237`), one hash, no pre/post.

5. `pin.receipt-attest=44919763ee523f334adaa4242d370435180d07aa0cdd4b85b0a7be870f48e8d9` (`kumitate-shokunin/SCORECARD.md:322`) equals sha256 of `scripts/receipt-attest.mjs` (37954 bytes). Header binds argv/exit/stdio/nonce/wall; counts inside the file: `nonce` 33, `argv` 26, `BASH_FUNC` 0, `LD_PRELOAD` 0, `research-gate` 0, `gate_sha256` 0. Fleet reports: `round-51/kumitate.md` has `receipt-attest` 6; `round-31/tsukuroi.md` has `loader-env` 1; other listed lanes' fleet reports have none of the claim tokens. Round-38 `kaidoku.md` / `tsukuroi.md` / `chousa.md` absent; round-37/38 kake, kumitate, mori, kotodama present.

6. Capture call is `"$ENV_BIN"` plus `-u` scrubs including `BASH_ENV` (`chousa-shokunin/tools/research-gate.sh:4000-4004`). Verifier usage is `--receipt/--gate/--counter` only (`corpus/evidence/round38/verify-receipts.py:34-36`) and states it does not authenticate authorship (`:43-47`).

## Findings
1. No new shared object. Narrowed C1 is function-export interposition on the capture's `env` invocation plus override refusal (`claims.md:232-236`). Narrowed C2 is integrity against committed bytes — pre/post gate digests, counter family, frozen census, receipt digest — not authorship (`claims.md:177-183`, `verify-receipts.py:7-32`). Those pre/post names and both predicates occur in zero sibling files. `PROVINCE.md:10-17` still refuses kumitate and says report, never absorb.

2. Wave-1 non-claim (a) is stale and would harm calibration. `.ufo/waves/round-38/w1/ConnOverlap.md:26` says the 7/7 "stays function-export/PATH independence". Erratum 6(b) says a PATH-resolved `command env` still scores 7/7 while PATH-poisonable (`claims.md:220-223,234-235`). PATH is an r39 cell, not part of the seven. Leaving (a) in force re-widens C1.

3. Tsukuroi, still two other channels. Loader-env (`SCORECARD.md:1203-1207,1213`) is an execve trace of eleven git tools for `LD_PRELOAD` / `LD_LIBRARY_PATH` / `PYTHONPATH`; the hollow control exits 0 whenever `LD_PRELOAD` is set. R12 R4 accepts `BASH_FUNC_stat%%` / `BASH_ENV` as an env-trusted residual on host `stat` (`Security.md:93-94`). Chousa's limit already keeps loader scrubbing out of the seven (`claims.md:134-139`) and says the `BASH_FUNC_*` channel itself is untouched (`claims.md:216-220`). Folding either sentence into 7/7 would make one count mean two mechanisms.

4. Kumitate pins, still not C2. `pin.receipt-attest` is a script-byte pin, not a receipt schema. Round-51 `receipt-attest` records invocation authorship (argv, exit, stdio sha, nonce, wall). Erratum 2's carried debt is `verifier_sha256` inside chousa receipts (`claims.md:181-183`), not that nonce ledger. A kumitate receipt missing `gate_sha256_pre` is not a C2 kill.

5. Homonym wave 1 could not see from SCORECARDs alone. Kotodama's one freeze-time `gate_sha256` and mori's round-15 probe pin both fail closed when a gate file moves, which is the same *word* as Erratum 2/8 "against committed bytes", and a different binding: no pre/post pair, no scenario census. Generic `counter_sha256` / `receipt_sha256` also appear on other objects (kake `.ufo/waves/round-45/verification/witness-split/split.json:4`, kotodama `reports/round-14/fix-runner-hash.md:50`, tsukuroi `.ufo/waves/round-33/a3w1/C14PostDataDeny/deny-inputs.json:8`, kumitate `.ufo/waves/round-48/close/ReRunCounter48-2-receipt.txt:14`). Kake's forgeable `runner` (`SCORECARD.md:2331-2332`) and mori's env-pin drop (`SCORECARD.md:304-306`) are unchanged homonyms.

## Limits
Contradiction, not a scalar: "committed bytes", `gate_sha256`, "pin", and "receipt" name `kotodama-frozen-run-v1`, round-38 counter receipts, and `kumitate-receipt-attest-v1`. This seat did not re-derive 7/7 and did not open every `gate_sha256` hit body. Kaidoku `BASH_FUNC` bytes were not disassembled.

Move (frontier text only; do not edit frozen `claims.md`): replace wave-1 (a) with (a') the 7/7 is name-`env` at `gate_canonical_capture` plus override refusal — PATH, a `date`/`stat` function, tsukuroi loader-env, and `BASH_FUNC_stat%%` stay outside the seven. Add (e): do not treat kotodama/mori `gate_sha256` or kumitate receipt-attest as `gate_sha256_pre`/`_post`. Keep wave-1 (b)(c)(d).

Risk if ignored: finishing Erratum 2 by calling receipt-attest over-claims authorship; treating kotodama's freeze pin as C2 already owned drops the mid-run pre/post race. Check: sibling `git grep -F gate_sha256_pre` stays empty; no new c1 id `LD_PRELOAD` or `PATH`; verifier usage stays the three paths at `verify-receipts.py:34-36`.
