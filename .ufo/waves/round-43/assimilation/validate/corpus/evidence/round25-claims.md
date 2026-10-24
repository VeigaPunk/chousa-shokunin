# Round-25 pre-registration — claims, frozen populations, predictions

Lane `chousa-shokunin`, claim base `d730ae4c33989ad9c8535764d4cae77b4db869f6`
(2026-10-21, hyaku block 25–34, recovery attempt 2; attempt 1 left no lane
output: no commit, no `.ufo/waves/round-25/`, 0 seats). Registered before any
implementation. The counting script is `corpus/evidence/round25-measure.sh`;
its before-output on the base tree is `corpus/evidence/round25-measure-before.log`.
Source: `SCORECARD.md` `## Planned — round 25` (lines 1282–1303 at the base).

## Claim 1 — operability: metadata screen (capability acquisition)

`QUALITY.md` criterion 6 (metadata header) has no machine check: at the base
`bash tools/research-gate.sh verify-metadata corpus/knowledge` exits 2
(`multiple record paths` — the mode does not exist), so the 3 legacy entries
lacking `recheck:` are invisible to every mode.

Frozen population: the 28 `corpus/knowledge/*.md` files at the base (sha256
prefixes in the round-25 lesson's Gate; list in `round25-measure.sh` POP1).

Spec v1 (`tools/research-gate.sh verify-metadata PATH [--root PATH]`):

- PATH is one `.md` file or a directory (its direct `*.md` children, `LC_ALL=C`
  sorted). Missing/unreadable PATH, or a directory with no `.md`, exits 2.
- Header region = lines before the first `## ` heading that sits outside a
  fenced block (whole file when none). Trailing `\r` is stripped per line.
- Key lines start at column 0, outside fences, inside the header:
  `source:`, `verified-at:`, `recheck:`. A key's value is the rest of its line
  plus continuation lines until a blank line, another key line, or the header end.
- Findings (`FINDING <ID> severity=… surface=metadata obs=entry=<basename> …`):
  `META_SOURCE_ABSENT` warn; `META_VERIFIED_AT_ABSENT` warn;
  `META_VERIFIED_AT_UNDATED` warn (value does not begin `YYYY-MM-DD`);
  `META_RECHECK_ABSENT` warn; `META_RECHECK_UNSCHEDULED` info (value's first
  token is not an ISO date, `<N>d`, or `on-release`);
  `META_RECHECK_ROOT_PARENT` info (value passes `--root ..`: the root then
  depends on where the checkout sits — round-24 spot-check debt).
- Per entry: `META entry=<basename> source=present|absent
  verified_at=dated|undated|absent recheck=scheduled|unscheduled|absent
  verdict=clean|drift`. Summary `METADATA_COMPLETE=N/M` (source present,
  verified-at dated, recheck present) and one `RESEARCH_GATE:` line. Exit 0
  CLEAN, 1 DRIFT; info drifts only under `CHOUSA_STRICT=1` (existing rule).
- Not composed into `verify-all`; the `--pin`/`--drift` canonical invocation is
  unchanged, so `--drift` vs the r12 baseline must stay `GATE_DRIFT: none`.

Prediction (after, same population): exit 1; `METADATA_COMPLETE=25/28`;
`META_NAMED_DRIFT_ENTRIES=[entry=archives-verified-r9.md entry=audit-r11.md
entry=gate-baseline-r8.md]`, each `META_RECHECK_ABSENT` only. Holds: selftest
cases 1–136 byte-identical, new cases 137+ pass; `GATE_DRIFT: none`;
`VERDICT_BEARING_EXPORTS=3/3`. Falsified if any other entry drifts, any of the
three is missed, a hold moves, or the mode exits 0 on the population.
Sourced: the claim's knowledge entry cites a `SOURCES.md` row opened this round.

## Claim 2 — freshness: re-derive the indexes and ledgers

Before (base): `STALE_INDEX_ITEMS=66` = 2 unindexed base files (2a) + 13
Frontier rounds 11–23 without a paragraph (2b) + 43 evidence-index rows filed
under another round's heading (2c) + 8 `LOG.md` `Capabilities +1` rounds
without a `SCORECARD.md` capabilities row (2d). Population: the base file list
and base records named in `round25-measure.sh`. Prediction: `STALE_INDEX_ITEMS=0`
with every new Frontier paragraph and capability row carrying a re-derivable
pointer (selftest case range or receipt path) re-run at the landing.

## Claim 3 — calibration: close stale restatements

Before (base): `STALE_RESTATEMENTS=15` = `SKILL.md` restating the A-r9 C3
finding as open after its round-12 closure (3a = 1) + 3 `SKILL.md` ledger
tuples ≠ the latest ledger revision `38·21·10·0·3` + 2 queue sizes ≠ 24 (3b)
+ 1 unfilled `${GSHA}` slot (3c) + 8 missing ledger addenda r16–r23 (3d).
Prediction: `STALE_RESTATEMENTS=0`; `SKILL.md` restatements replaced by a
pointer to the owning revision plus the re-deriving command (criterion 9);
the substitution recorded in an appended erratum (criterion 4).

## Separability and holds

Claim 1 touches `tools/research-gate.sh` and a new knowledge entry; claim 2
touches `corpus/README.md`, `corpus/evidence/README.md` and the `SCORECARD.md`
capabilities tables; claim 3 touches `SKILL.md` and appends to
`corpus/knowledge/hardening-r10.md`. Each counting block reads only its own
files, so each verifies with the others reverted. No axis may be harmed: the
holds block (selftest, drift, r1 3/3) runs at the landing.
