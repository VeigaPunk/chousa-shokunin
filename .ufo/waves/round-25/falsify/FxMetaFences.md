# FxMetaFences — round 25

Axes: operability; scope is the integrated `verify-metadata` header/fence screen.

## Checkpoint provenance

- Initial private clone was based at `0fc037e6b07f3820ead8c9207a8034ac854197a1`; that tree lacked `verify_metadata` (private-clone search returned no match). L1 corrected the checkpoint because `tools/research-gate.sh` was omitted from the first helper path list.
- L1 then reported `d8c8cff3923f10481ac9ced66d0af7c41d38130c` still omitted `corpus/evidence/README.md`; full checkpoint is `e93ac711f885a10d44fdd80a1734997419595b5a`.
- Private clone now points at e93. `git rev-parse` observed identical d8/e93 gate blob `90e43b0293fe04a89f056970a54669c1948c0161`; the fixture run below was on d8, and its tested gate bytes are therefore identical to e93. No live-lane writes.

## Findings

- No actionable fence-parsing defect observed in the requested cases.
- `verify_metadata` uses a separate scanner (not a literal call to `load_sections`), but its opener/closer tests and 0–3-space, same-character, close-length-at-least-open state transitions match `load_sections`: `tools/research-gate.sh:2349-2394` vs `:397-418,427-449`.
- Spec-match: paired backtick and tilde fences, 0/1/2/3-space openers, shorter same-character fence inside a longer fence, and a 4-space-indented fence-like line. Fake fields inside paired fences are ignored; true `source:` and dated `verified-at:` after closure are read. The indented-code fake fields are ignored by the column-0 key rule; true fields afterward are read.
- Unclosed opener: observed fail-closed behavior matches `load_sections`' explicit unclosed-fence rule (`:419-421`); the fixture's later `## Claim` and true-looking fields remain fenced. This is an ambiguity, not a demonstrated divergence: spec v1 (`corpus/evidence/round25-claims.md:24-28`) and the hardening note (`corpus/knowledge/metadata-screen-r25.md:31-35`) do not define unclosed-fence handling.

## Exact fixture command and output

```sh
rc=0; out=$(bash /tmp/chousa-r25-FxMetaFences/tools/research-gate.sh verify-metadata /tmp/chousa-r25-FxMetaFences/fixtures/fence-scan --root /tmp/chousa-r25-FxMetaFences 2>&1) || rc=$?; printf '%s\nEXIT=%s\n' "$out" "$rc"
```

```text
research-gate v2 — ts=2026-10-21T07:58:16Z — mode=verify-metadata — path=/tmp/chousa-r25-FxMetaFences/fixtures/fence-scan — root=/tmp/chousa-r25-FxMetaFences
META entry=00-backtick.md source=present verified_at=dated recheck=absent verdict=drift
META entry=01-tilde.md source=present verified_at=dated recheck=absent verdict=drift
META entry=02-backtick.md source=present verified_at=dated recheck=absent verdict=drift
META entry=03-tilde.md source=present verified_at=dated recheck=absent verdict=drift
META entry=04-shorter.md source=present verified_at=dated recheck=absent verdict=drift
META entry=05-four-indent.md source=present verified_at=dated recheck=absent verdict=drift
META entry=06-unclosed.md source=absent verified_at=absent recheck=absent verdict=drift
FINDING META_RECHECK_ABSENT severity=warn surface=metadata obs=entry=00-backtick.md key=recheck absent
FINDING META_RECHECK_ABSENT severity=warn surface=metadata obs=entry=01-tilde.md key=recheck absent
FINDING META_RECHECK_ABSENT severity=warn surface=metadata obs=entry=02-backtick.md key=recheck absent
FINDING META_RECHECK_ABSENT severity=warn surface=metadata obs=entry=03-tilde.md key=recheck absent
FINDING META_RECHECK_ABSENT severity=warn surface=metadata obs=entry=04-shorter.md key=recheck absent
FINDING META_RECHECK_ABSENT severity=warn surface=metadata obs=entry=05-four-indent.md key=recheck absent
FINDING META_SOURCE_ABSENT severity=warn surface=metadata obs=entry=06-unclosed.md key=source absent
FINDING META_VERIFIED_AT_ABSENT severity=warn surface=metadata obs=entry=06-unclosed.md key=verified-at absent
FINDING META_RECHECK_ABSENT severity=warn surface=metadata obs=entry=06-unclosed.md key=recheck absent
METADATA_COMPLETE=0/7
RESEARCH_GATE: DRIFT (entries=7 complete=0 findings=9 drift=9)
EXIT=1
```

## Residual risk / verification gaps

- LSP device unavailable: `read xd://lsp` returned `No such tool: xd://lsp`; therefore no LSP status/references/definition/diagnostics were available. Review used direct source ranges only.
- No selftest or differential suite run; outside this scoped fixture attack, no claim is made about them. Refusal hardening paths in `metadata-screen-r25.md:41-45` were not exercised here.
- No tools installed.
- Private fixture files retained; SHA-256:
  - `fixtures/fence-scan/00-backtick.md` `52fe70b332bbebdb687e9e818eb9b4af2b3bd7297de757167a30a1ff4c5ad201`
  - `fixtures/fence-scan/01-tilde.md` `9fb0fa6671db3ed04bb1761e3c45ee4b802f7f8eef803276ef9fd0ce13451feb`
  - `fixtures/fence-scan/02-backtick.md` `959b9e66d9ab9e48a55197deca13b91e39b05bc0263d8e37e2e79e7a18e2d5f1`
  - `fixtures/fence-scan/03-tilde.md` `3b2a2e8159221f636b9736d48e26031cc079f010fb3c6a980fffb230c4bf895f`
  - `fixtures/fence-scan/04-shorter.md` `001348eedece92e8e404dc874ec9711d7bd3566604db39bfa05ed7d34b9c502b`
  - `fixtures/fence-scan/05-four-indent.md` `40c532775367f974869afaebc496c418e9fd00835442d68e99bd30353fa11105`
  - `fixtures/fence-scan/06-unclosed.md` `6e2677ee33501473472d047b551f2677c8c30cb648747df0fae52982c9f32fa6`

VERDICT: No fence-parser divergence found; unclosed-fence semantics remain unspecified in v1, while implementation follows `load_sections` fail-closed behavior.