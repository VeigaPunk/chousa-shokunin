# Round 26 — Claim 3 registry implementation

- Seat: `ChousaR26.ExecC3Registry-3`; private clone base observed by `git -C /tmp/chousa-r26-ExecC3Registry-3 rev-parse HEAD` → `f361d12e44687841e30ec35710ddb366c6f795e0`.
- Changed only `/tmp/chousa-r26-ExecC3Registry-3/tools/research-gate.sh` in the clone; delivered patch: `/tmp/chousa-r26-ExecC3Registry-3/r26-ExecC3Registry-3.patch`.
- Gate SHA-256: `bfdc349eb04298b4e2845d672a263a76e3d762b126f39ffa03194d4fc74258eb`.
- Patch SHA-256: `67ca6d8292cf66b45b2ca5a4fc9ae2902a0fd81bcda24f0347c8e491b847d104` (430 lines).

## Behavior implemented

- `verify-metadata PATH [--root PATH] [--registry FILE]`; `--registry` is rejected outside metadata mode. Usage updated at `tools/research-gate.sh:310-320`.
- Registry is opened once and parsed from a bounded 8 MiB FD snapshot with a streaming read loop. Blank/non-table lines are skipped before trimming; rows, cells, and `used-by` tokens use inline parameter trimming rather than a trim subprocess per line/cell. It checks denylist (including the opened FD target), regular-file/stat availability, single link, size, NUL, and read result. Refused/unreadable and headerless input exits 2 without a verdict. No universal runtime bound is claimed. Reader/parser: `tools/research-gate.sh:2307-2416`.
- Registry table columns are found by `id`, `status`, `used-by`; row IDs use `S` plus ≥3 digits, duplicates keep the first row. Source IDs use standalone ASCII alnum/underscore boundaries. `used-by` comma tokens are trimmed and only leading `./` is normalized; they must equal the opened entry FD’s canonical path relative to canonical `--root`. An entry resolving outside `--root` cannot match; no basename fallback. Checker/path logic: `tools/research-gate.sh:2418-2467,2511-2513,2632-2635`.
- Findings implemented: `META_SOURCE_NO_ROW_ID` info, `META_SOURCE_ROW_MISSING`, `META_SOURCE_NOT_MINED`, `META_SOURCE_USEDBY_MISSING`, and `META_VERIFIED_AT_BARE` warn. Only IDs and entry basenames appear in finding observations; registry/source cell contents are not printed.
- Source continuation capture and registry maps are opt-in behind `--registry`; ordinary metadata mode does not accumulate the previously ignored source value. Parser/verdict hooks: `tools/research-gate.sh:2568-2652`.
- Eight appended selftest cases after existing `metadata-usage` case 161 cover missing row, non-mined, exact-path used-by miss, bare verified-at, token boundaries, positive reordered columns + source/verified continuations + S0001, duplicate-first-row, and NUL-refused registry exit 2: `tools/research-gate.sh:5865-5964`. Existing case definitions 1–161 were not edited in this clone.

## Evidence, checks, risks

- Pre-registration/spec read first: `corpus/evidence/round26-claims.md:84-115`; correction from L1 message: IDs are S + 3-or-more digits with ASCII word boundaries, and used-by matches the exact root-relative entry path.
- L1 later directed this seat **not** to run builds/tests/formatters; accordingly `round26-measure.sh <clone> c3` and `holds` were not run. `C3_CONTROLS_CAUGHT`, `C3_POSITIVE_CLEAN`, `C3_POP_R24PLUS_CLEAN`, every POP24 finding line, and holds output are therefore **not observed / not retained** here; no values or POP24 defect adjudications are claimed. Main must run the assigned post-integration gate.
- Integration overlap: C1 also rewrites `verify_metadata` header parsing and appends tests after case 161. Retain C1's streaming loop; merge the C3 `source_value` capture only when `REGISTRY_ARG_SET` is true. Append these eight cases after C1's appended cases to preserve both suites.
- LSP unavailable in the exposed tool inventory (no LSP route); no LSP result was available. No tools installed or updated.

VERDICT: C3 implementation and patch complete; C3 probe and holds intentionally unrun per L1 instruction; no installs.