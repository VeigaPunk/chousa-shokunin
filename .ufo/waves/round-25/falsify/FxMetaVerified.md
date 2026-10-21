# FxMetaVerified — verify-metadata date-start attack

## Finding
- **Medium — continuation-only verified-at can be reported clean under a literal date-start reading.** In `tools/research-gate.sh:2391-2392,2404-2410`, continuation text is appended with a newline, then `[[:space:]]*` before the date digits accepts that newline. The probe below used `verified-at:` with an empty key-line value and `2026-10-21` on the next line; output was `verified_at=dated ... verdict=clean`. Spec v1 defines the value as the key-line remainder plus continuations and calls it undated when it does not begin `YYYY-MM-DD` (`corpus/evidence/round25-claims.md:26-32`). The raw value begins with LF, not a date: this diverges under a literal first-line/start reading. Spec v1 does not state whether leading newlines are trimmed, so the boundary is ambiguous; if “begin” means first non-whitespace text, the result matches that interpretation.

## Probe: exact command and output
Tested in private clone at full integrated checkpoint `e93ac711f885a10d44fdd80a1734997419595b5a`. The directory contained the four named committed fixtures (`missing-verified-at.md`, `undated-verified-at.md`, `undated-verified-at-slash.md`, `verified-at-below-heading.md`) plus two probes: `verified-at: 2026-99-99 (shape only)` and an empty `verified-at:` followed by `2026-10-21` on its continuation line.

Command executed:
```sh
set -eu
probe=/tmp/chousa-r25-FxMetaVerified/tmp/meta-date-probe
mkdir -p "$probe"
cp corpus/fixtures/metadata-r25/missing-verified-at.md corpus/fixtures/metadata-r25/undated-verified-at.md corpus/fixtures/metadata-r25/undated-verified-at-slash.md corpus/fixtures/metadata-r25/verified-at-below-heading.md "$probe/"
printf '%s\n' '# Date-shape probe' 'source: S001' 'verified-at: 2026-99-99 (shape only)' 'recheck: 90d' '## Claim' > "$probe/invalid-calendar-date.md"
printf '%s\n' '# Continuation probe' 'source: S001' 'verified-at:' '2026-10-21 (on continuation line)' 'recheck: 90d' '## Claim' > "$probe/continuation-date.md"
set +e
bash tools/research-gate.sh verify-metadata "$probe" --root /tmp/chousa-r25-FxMetaVerified
rc=$?
printf 'GATE_EXIT=%s\n' "$rc"
exit 0
```

Output:
```text
research-gate v2 — ts=2026-10-21T08:00:29Z — mode=verify-metadata — path=/tmp/chousa-r25-FxMetaVerified/tmp/meta-date-probe — root=/tmp/chousa-r25-FxMetaVerified
META entry=continuation-date.md source=present verified_at=dated recheck=scheduled verdict=clean
META entry=invalid-calendar-date.md source=present verified_at=dated recheck=scheduled verdict=clean
META entry=missing-verified-at.md source=present verified_at=absent recheck=scheduled verdict=drift
META entry=undated-verified-at-slash.md source=present verified_at=undated recheck=scheduled verdict=drift
META entry=undated-verified-at.md source=present verified_at=undated recheck=scheduled verdict=drift
META entry=verified-at-below-heading.md source=present verified_at=absent recheck=scheduled verdict=drift
FINDING META_VERIFIED_AT_ABSENT severity=warn surface=metadata obs=entry=missing-verified-at.md key=verified-at absent
FINDING META_VERIFIED_AT_UNDATED severity=warn surface=metadata obs=entry=undated-verified-at-slash.md key=verified-at does not begin YYYY-MM-DD
FINDING META_VERIFIED_AT_UNDATED severity=warn surface=metadata obs=entry=undated-verified-at.md key=verified-at does not begin YYYY-MM-DD
FINDING META_VERIFIED_AT_ABSENT severity=warn surface=metadata obs=entry=verified-at-below-heading.md key=verified-at absent
METADATA_COMPLETE=2/6
RESEARCH_GATE: DRIFT (entries=6 complete=2 findings=4 drift=4)
GATE_EXIT=1
```

## Interpretation and evidence
- The four committed fixtures match the hand expectations in `corpus/fixtures/metadata-r25/README.md:10,12-13,23` (missing, prose-undated, slash date, below heading).
- `2026-99-99` passes because it matches the digit shape, not because it is a valid calendar date. This is **spec-match for the stated `YYYY-MM-DD` shape**, not actual ISO-date validation. Spec v1 does not require calendar validation (`round25-claims.md:29-32`); criterion 6 says ISO date (`corpus/QUALITY.md:17-23`), while the screen explicitly disclaims full criterion-6 enforcement (`corpus/knowledge/metadata-screen-r25.md:71-75`). Treat valid-calendar checking as a disclosed residual gap, not an implementation divergence here.
- Initial checkpoint `0fc037e6b07f3820ead8c9207a8034ac854197a1` is not a valid test target: the round-25 lesson records its omitted gate and the omitted `corpus/evidence/README.md` in both `0fc037e` and `d8c8cff` (`corpus/lessons/round-25.md:109-133`). `0fc` gate Git blob `896a13ebc544c03c64985f5a1a21c6f407f86452`; `d8c8cff` and full checkpoint `e93ac711f885a10d44fdd80a1734997419595b5a` both have gate blob `90e43b0293fe04a89f056970a54669c1948c0161`. The latter is the measured checkpoint; private clone HEAD was observed as `e93ac711f885a10d44fdd80a1734997419595b5a`.
- LSP device unavailable: `read xd://lsp` returned `No such tool: xd://lsp`; no grep result is used as semantic proof. No build or full selftest was assigned or run. Probe fixtures were removed from the private clone after capture. Installs: none.

VERDICT: Recommend clarifying whether verified-at must start on its key line; continuation-only dates currently pass, while invalid calendar dates are accepted by the disclosed shape-only screen.