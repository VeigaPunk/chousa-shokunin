# Round-25 — FxOracleCompare

- Tested full pin `e93ac711f885a10d44fdd80a1734997419595b5a`; `tools/research-gate.sh` SHA-256 `63a39282a15f19f5b0443212e66ad2dfc8ce0315e65697e479a7206879a598b2` (same gate hash at d8c8cff).
- 15 private scratch fixtures × normal/strict = 30 gate/oracle comparisons: 18 agreed, 12 differed. Scratch files only; no production edits.

## Findings (by severity)

### MEDIUM — calendar-invalid `recheck` date passes as scheduled
- Frozen spec requires an ISO date (`corpus/evidence/round25-claims.md:32-33`); gate tests only date-shaped digits (`tools/research-gate.sh:2423-2425`), while oracle validates calendar dates (`corpus/evidence/round25-meta-oracle.py:82-89`).
- Scratch `invalid-recheck-calendar.md:3` uses `2026-02-29`: normal gate says `recheck=scheduled`, CLEAN/rc=0; oracle says `recheck=unscheduled` with `META_RECHECK_UNSCHEDULED` (CLEAN/rc=0). Strict: gate rc=0, oracle DRIFT/rc=1. Valid `2024-02-29` agrees. The frozen fixture table has only a valid ISO recheck date (`metadata-r25/README.md:30`), so 54/54 misses this class.

### LOW — tab after `##` prematurely ends the header
- Spec delimiter is literal `## ` (`corpus/evidence/round25-claims.md:24-25`); gate accepts any whitespace after `##` (`tools/research-gate.sh:2374`), unlike oracle's `line.startswith("## ")` (`round25-meta-oracle.py:39-41`).
- Scratch `heading-tab.md:3-4` has `##\tClaim` followed by `recheck: 90d`: gate reports `recheck=absent`, DRIFT/rc=1; oracle reports scheduled, CLEAN/rc=0, in both modes.

## Residual risk and coverage
- Blank `source:` is a real divergence but not adjudicable from v1 wording: scratch `empty-source.md:1` yields gate `source=present`, CLEAN/rc=0 versus oracle `source=absent`, `META_SOURCE_ABSENT`, DRIFT/rc=1. Gate records key presence only (`research-gate.sh:2398-2402`); oracle requires a nonempty value (`round25-meta-oracle.py:107-111`). Spec lines 26-28/36-39 do not define empty-value semantics.
- Duplicate keys are under-specified: oracle explicitly says v1 does not define duplicates and chooses first (`round25-meta-oracle.py:66-68`); gate overwrites with later key lines (`research-gate.sh:2381-2385`). Conflicting duplicate rechecks and duplicate `verified-at` produced different states/findings/strict exits in scratch tests; do not count these as spec defects until precedence is specified.
- The 54 cells are the 27 named fixtures × two strictness modes (`round25-meta-differential.sh:31-42`; receipt `round25-meta-differential.log:1`). The table (`metadata-r25/README.md:7-35`) covers ordinary missing/valid/unrecognized values, but no invalid calendar date, duplicate keys, blank source value, or tab heading. Thus 54/54 is not evidence for these behavioral classes.
- All three fence variants and all three continuation variants agreed in both modes, including the post-correction quoted continuation containing `--root ..` (`continuation-root.md`). The CLI root-only call (`verify-metadata --root <clone-root>`, no PATH) returned 2 for both gate and oracle, as spec requires; diagnostic text differs but no status mismatch.

## Checkpoint provenance
- Initial `0fc037e` lacked the mode (literal search in that private clone found no `verify-metadata`); lesson records old gate SHA `752e4e38…`/136 cases vs prose 154 (`corpus/lessons/round-25.md:111-120`).
- Interim `d8c8cff` carried the gate but not the `corpus/evidence/README.md` index update; the d8→e93 diff shows that file changed. The differential runs above use the full pin e93. (`round-25.md:127-133` records this correction.)

## Verification gaps
- No LSP device is mounted (`read xd://lsp` returned “No such tool”); source search was only a locator. Conclusions rest on the pinned source and direct gate/oracle outputs.
- Did not rerun the 54-case differential or full selftest; used its committed receipt and ran only the 30 assigned scratch comparisons. No tools installed.

## Private scratch fixture SHA-256
- `continuation-fence.md` `feef3b7067e2d1911b95beb2435310d83cf248f5d66d72e830424c91ac59c04b`
- `continuation-root.md` `3e1544cb9711c753d5db4dcb3f23df19999b3f4e5c9f9f1187fa53a04e18d123`
- `continuation-values.md` `d7c1a07bdbda546bd7066993aa925e5e89bc22eb76046a1dc2146249dff32342`
- `duplicate-recheck-last-scheduled.md` `ec4e07dd7ea6620059877fe21c260427b35d9e5e7d51ac8edbe2a0ce2a73d799`
- `duplicate-recheck-last-unscheduled.md` `745806c6e27e4b5f3260d20f9434451f613bd6b6b91cbec96e4a8582e3837f74`
- `duplicate-verified-at.md` `6487e095f2b45a46eb733f1a9bb8a20b686187e94bd372a98961e686e9b50dc8`
- `empty-source.md` `85520fa4af3bc47153a7becd9d3eb48d37ad78c10ad4523294133e901bf420f2`
- `fence-mismatched-close.md` `f380d596f48c30a864cd73359a82a0fc541d3b4aa35a952fe84deb17560e1b6c`
- `fence-opener-closer.md` `71dcea84452d925bd37f4ef603d42e5906b6c1fee2345a8b096b81fe0d5903bc`
- `fence-tilde-length.md` `0910851e4f180a4ae725bf023faabc09a394a26eddf29792639504fb0043565a`
- `heading-tab.md` `5a57d485ee76c2792f9758a4b095f61e57dcb7b54b3990be1a5c0174b168c5a3`
- `invalid-recheck-calendar.md` `b9d7d1db448bffd85512bb95404c3b8821dbae23747db1ce07137d968327f9b8`
- `malformed-recheck-date.md` `7991203296c0465b2b4f7e1a29e64ce023bc5b78c9e677e468254b8e796b64bd`
- `valid-leap.md` `52aa8536b8e419a919a949863b229978eaf9fc7fabc0d89d7a8910317754c75e`
- `verified-invalid-calendar-prefix.md` `faf80b07cce1095f3a46b46840609866076790d8f5121358286b002cc02f20ef`

VERDICT: Advisory review found two confirmed spec divergences; the 54/54 suite misses them and the under-specified blank/duplicate-key cases.
Installs: none.