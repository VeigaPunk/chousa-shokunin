# FxMetaContinue — round-25 metadata continuation falsification
Axes: operability; spec-v1 fidelity; gate/oracle parity; checkpoint integrity.
Checkpoint: private clone HEAD `e93ac711f885a10d44fdd80a1734997419595b5a`; gate SHA-256 `63a39282a15f19f5b0443212e66ad2dfc8ce0315e65697e479a7206879a598b2`.
Selftest command: `cd /tmp/chousa-r25-FxMetaContinue && bash tools/research-gate.sh --selftest 2>&1 | tail -8`.
Output: `ok-case 153 metadata-nonkey-continuation exit=0`; `RESEARCH_GATE_SELFTEST: PASS (154 cases, 0 skipped)`.
Probe command: `bash /tmp/chousa-r25-FxMetaContinue/probe-runs.sh > /tmp/chousa-r25-FxMetaContinue/probe-runs.log 2>&1` (rc 0; exact output saved; SHA-256 `70f7eb25d17fad88fa0ab8fb40e2e74fbed6603cc3bd4bd1145f56dc497634a0`).
Additional command: `bash /tmp/chousa-r25-FxMetaContinue/probe-extra.sh > /tmp/chousa-r25-FxMetaContinue/probe-extra.log 2>&1` (rc 0; exact output saved; SHA-256 `8bc1fd79613f83fcbbd9375dbf1ce84124e178f3e20503444cf297c638e05ca7`).
LSP check: `xd://lsp` returned “No such tool”; this review used source reads and runtime differential output, not grep as semantic proof.

## Finding — Medium
Invalid calendar date passes as scheduled and bypasses strict drift: spec v1 calls for an ISO date (`corpus/evidence/round25-claims.md:32-33`); gate checks only the numeric shape (`tools/research-gate.sh:2423-25`).
Counterexample `recheck: 2026-13-45`: `CHOUSA_STRICT=1` gate output says `recheck=scheduled verdict=clean`, rc 0; oracle says `recheck=unscheduled verdict=drift` with `META_RECHECK_UNSCHEDULED`, rc 1 (`probe-extra.log:11-21`).
Oracle validates calendar dates with `date.fromisoformat` (`corpus/evidence/round25-meta-oracle.py:82-89`). This is a spec-v1 implementation divergence, not a continuation-parser difference.

## Requested continuation probes
Case 153 and independent `note: ... --root ..` continuation: MATCH; both gate and oracle retain `META_RECHECK_ROOT_PARENT` (`probe-runs.log`, p1; selftest case 153).
Blank/whitespace-only line and blank inside fenced continuation: MATCH; both terminate continuation (`p2a`, `p2b`, `p2d`; no root-parent finding when it appears only after the blank).
Recognized key end and indented key-like continuation: MATCH (`p3a`, `p3c`); `verified-at:` ends `recheck`, while indented `source:` stays continuation.
URL continuation beginning `https:`: MATCH (`p4a`, `p4b`); URL is not treated as a key; empty `recheck:` followed by URL is unscheduled from its first token.
Fenced continuation, including tilde fence with an inner backtick fence: MATCH (`p5a`, `p5b`); `--root ..` within the continued value is found. Strict info-to-drift behavior on p4a also matches (both rc 1).
Duplicate `recheck:` is a gate/oracle divergence: gate uses last value (`someday`), oracle first (`2026-01-01`) (`probe-runs.log:67-78`). Oracle itself says v1 does not define duplicates (`round25-meta-oracle.py:66-68`): spec ambiguity, not a demonstrated implementation violation.

## Other differences classified
Bare `source:`: gate treats key presence as `source=present`, complete 1/1, rc 0; oracle treats empty value as absent, complete 0/1, rc 1 (`probe-runs.log:150-161`). Spec does not say whether an empty value is absent: ambiguity.
`##\tClaim`: gate ends header because it accepts any whitespace after `##`; oracle requires literal `## ` (`probe-runs.log:176-187`; gate `tools/research-gate.sh:2374`, oracle `round25-meta-oracle.py:40-41`). Spec wording leaves tab-heading interpretation ambiguous.
Directory dotfile: gate’s shell `*.md` scan omits `.hidden.md`, while oracle includes it (`probe-runs.log:217-226`). Spec says direct `*.md` children; likely glob/oracle interpretation difference, not a demonstrated gate defect.
NUL entry: gate refuses it and oracle parses it (`probe-runs.log:189-201`); this is the disclosed post-registration `META_ENTRY_REFUSED` hardening (`corpus/knowledge/metadata-screen-r25.md:41-46`), not a new regression.

## Packaging correction evidence
At original 0fc pin, `git show ...:tools/research-gate.sh | sha256sum` measured `752e4e382ed77c06ac5030ce2179c7ca524934f86fd2a6b25ef946ab027ac553` (old gate; the initial checkpoint omitted this mode).
At d8 pin, gate was `63a39282…`, but evidence README remained `6faa9aae3230300d19df5ed8f7c730729d4aafc02e609c64f4dda1dd02ca492c`, same as 0fc; e93 README is `ce808c19a8df2176f8402d4740d732007a778c074f9b0847f422d7b2b23cfa1c`. Both packaging omissions are preserved here; e93 is the full pin used for probes.

## Private-clone scratch file SHA-256
- `probe-runs.sh` 9527f21c72eddf84f73e0c247803f87b790ca114e96bf2065185dcc8a703abaa; `probe-runs.log` 70f7eb25d17fad88fa0ab8fb40e2e74fbed6603cc3bd4bd1145f56dc497634a0
- `probe-extra.sh` 46f1634c15e8cf8b77a6cf0522646d9ccdaac533a93bef829a086fc0a07190bc; `probe-extra.log` 8bc1fd79613f83fcbbd9375dbf1ce84124e178f3e20503444cf297c638e05ca7
- `probe/p1-note-continuation.md` df94eb11aaf5946286c3f54565fae5af3a74629ef650d1383b96b8a495e6a7f5; `probe/p2a-blank-before-continuation.md` 996195c2249fa64cbd15afacf96c121bbfc145519b92413381d02a623b5696e3
- `probe/p2b-ws-blank.md` f634bd5b0a7923befb2a95405a6997a798e4d5380e1cdf103dc14fad4a47021b; `probe/p2c-blank-inside-fence.md` b68d1263a3d3727837133bb4601410b3b39e87fecc2b7d5c7145bf63d6e3c4d7
- `probe/p2d-blank-after-fence.md` 588580761744e53617b1ea7250f3c70365078ad143fe44ed670dd2a5a4784207; `probe/p3a-key-end.md` d84b0778b1098128c1a89819fccb9fde76444e4246805181ac9b0ecbdf3cdf42
- `probe/p3b-dup-recheck.md` e3a63480239659d266edcd4ecaee28daed213af465537d9dfbfe8afb22132601; `probe/p3c-indented-key.md` 621e25eb111667e8a76536e0bc3079a7b4dbcaa950d535688f73e03f9b729be1
- `probe/p4a-https-continuation.md` 16949c1fd88f45d173e8857635f90a7b9ad5de6520af6e575c01d06a56ac9b61; `probe/p4b-bare-recheck-https.md` b06fe1d6bdc4829e81f1992a9b0035b1119cddb758130faad1501fb911c110b1
- `probe/p5a-fenced-continuation.md` 93c458dfb0e9e8a676e5d68d30b63f27bbdde515986716cd93fc621dfa492a7a; `probe/p5b-tilde-fence.md` f3824a5b54f8159df8c3f48883cea4f4d4cac02dc8f2c8ca5e4f7cdf72f45599
- `probe/p6a-bare-source.md` f31acfde518660030ca525bbdbb5b076efc0540f4723094982cf48ab6e9bc382; `probe/p6b-bad-iso.md` c616f6314f0bfdb6fbebeb693e36378466074a9d22c401fa588f1465846f5534
- `probe/p6c-tab-heading.md` b51c1f6c823cb457bdc60f568ec39a1667d262b60e9541c5659fc0de997461ae; `probe/p6d-dir/.hidden.md` 0aa5a52ce39d53b61e5c3dad689cf77df6800e86bb206f2acc203b29e5b94842
- `probe/p6d-dir/a.md` 0aa5a52ce39d53b61e5c3dad689cf77df6800e86bb206f2acc203b29e5b94842; `probe/p6e-nul.md` b26d03f43b310c3b00e3a619d1bf1859e0a2534e930d38c36f4d9bb871ce5290
VERDICT: One medium spec-v1 divergence: invalid ISO-date shape bypasses strict drift; requested continuation probes otherwise match. Installs: none.