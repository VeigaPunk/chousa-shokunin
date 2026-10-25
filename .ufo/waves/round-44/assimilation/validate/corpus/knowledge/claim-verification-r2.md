# Claim-vs-source verification — round-2 coverage mode (research-gate)

source: lane HEAD `6344569a68ca9a198df04c7febae58444d821e1f`; frozen gate
`tools/research-gate.sh` sha256 `03a3324455852ea0025115cb0e3ba9c8cdea10da5edc051c4738854a27c14be0`
(observed identical across repeated samples after the wave's last edit); fixture
`corpus/fixtures/claims-r2.jsonl` sha256 `23d078cbfd032ec5ee7de5c21de65eba3a3cd2989a78281ff61bc6db62188802`,
its README sha256 `44d8a890406f0802986adb7b92c653c53d2548ffe7976911250f01c76c48e3e7`
verified-at: 2026-10-15, from the lane cwd; fresh-process CLI runs; read-only
local opens only; nothing was fetched or executed
recheck:
`bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..`
· `bash tools/research-gate.sh --selftest`

All script line numbers below are relative to the frozen revision above.

## The move

Round-1's `verify` mode validates record STRUCTURE only (question, ranked
sources, marked hops, pointed claims, kept rejections — `SKILL.md:80-82`); no
claim was ever checked against its cited source. Round 2's coverage move adds
`verify-claims <claims-file>`: each claim's verbatim span is resolved in its
cited source inside the local corpus boundary, and a per-claim disposition plus
an exact counting summary is emitted under the existing exit contract
(`tools/research-gate.sh:27-45, 710-859`).

Pre-registration held. The fixture was authored before the mode existed
(`corpus/fixtures/claims-r2.README.md`, "Authoring state": gate sha
`088435…` = the round-1 revision, no `verify-claims` token) with fixed expected
verdicts: 13 supported, 2 contradicted, 2 unsupported. The implementation
landed later in the same wave and settled at the frozen sha. Runs taken while
the file was still being written are not results — a mid-edit sample briefly
failed its own selftest on a lagging expectation because the summary format was
being upgraded underneath it; the settled revision passes (receipts below).

## Mode design (frozen revision)

- CLI: `research-gate.sh verify-claims [CLAIMS] [--root PATH]`; `CLAIMS` via
  positional or `CHOUSA_CLAIMS`; mode banner = `mode=claims` (usage line `:84`;
  argparse `:1460-1478`; mode dispatch `:1480-1491`).
- Claims file: JSONL. Blank lines and `#`-comment lines are ignored; a
  `{"marker_default":…}` line sets the default contradiction marker and is not
  a claim; every other line is one JSON object
  `{"id","source","span","expect"[,"marker"]}` with
  `expect ∈ supported|contradicted|unsupported` (`:728-768`).
- Source boundary (fails closed): the source is canonicalized
  (`readlink -f`) and must resolve under `CHOUSA_ROOT` or the lane root;
  session/denylist paths → `CLAIM_SOURCE_SESSION` (crit, printed as path only,
  never opened); ephemeral pointers → `CLAIM_SOURCE_EPHEMERAL` (warn); URLs →
  `CLAIM_SOURCE_EXTERNAL` (crit, "url source refused (no external fetch)");
  outside both roots → `CLAIM_SOURCE_OUT_OF_CORPUS` (crit); unreadable/missing
  → `CLAIM_SOURCE_MISSING` (warn) (`:655-708`). Sources are content-read only
  via `cat` after those checks (`:780-783`); the claims file itself is line-read
  by the JSONL loop (`:728-846`) and its secret shapes are screened (`:726`). The
  local-only bound is absolute: refused claims are never opened, and no fixture
  can pre-register its way past a refusal (expect vocabulary has no `refused`).
- Span check: byte-exact substring test of the source file content
  (`:784-789`); the gate reports the first occurrence as `at=line:N` (or
  `lines:N-M` for multi-line spans).
- Observed dispositions (`:734-832`):
  - `supported` — span present (`:791`).
  - `unsupported` — span absent; silent when `expect=unsupported`, otherwise a
    warn finding `CLAIM_SPAN_NOT_FOUND` with `nearest_line`/`context` (`:810-832`).
  - `contradicted` — span present and the declared marker byte-co-occurs within
    the span's source lines (`:796-808`).
  - `unproven` — `expect=contradicted` but no marker is defined or it is not
    found in the span's lines; finding `CONTRADICTION_MARKER_ABSENT` (warn)
    (`:798-807`).
  - `refused` / `invalid` — boundary refusal, or a malformed record / invalid
    expect / stray marker (`CLAIM_RECORD_INVALID` warn, `:734-771`).
  - A span present where `expect=unsupported` is observed as `supported` with
    finding `CLAIM_SPAN_UNEXPECTED` (warn) (`:792-795`).
- Verdict per line: `match|mismatch`; the line format is
  `CLAIM id=… expected=… observed=… source=… at=… verdict=…` (`:845`).
- Counting summary (`:851-855`): `VERDICT_BEARING_CLAIMS=N/M` where
  `N = M − mismatched − refused − invalid`, then
  `RESEARCH_GATE: CLEAN|DRIFT (claims=… supported=… contradicted=… unsupported=…
  mismatched=… unproven=… refused=… invalid=… findings=… drift=…)`.
  CLEAN iff every read claim matched; any mismatch, refusal, invalid record or
  warn/crit finding drifts. Exit contract unchanged: 0 CLEAN | 1 DRIFT |
  2 setup/usage (setup keeps stdout empty and diagnostics on stderr).

## Verbatim-span semantics and honest limits

What a CLEAN run establishes: for every claim read, the literal bytes of its
span occur in the cited local file, at a reported first-occurrence line, inside
the allowed corpus roots; and for `contradicted` entries the declared marker
literal co-occurs within the span's source lines. That is all.

What structural matching does NOT prove:

- Not semantic support. A byte-exact quote can be contextually misleading; the
  mode never parses meaning. The `contradicted` arm is likewise structural — a
  declared marker literal, not a negation inference.
- Not location binding or uniqueness. The check is "the span occurs somewhere
  in the file"; the reported `at=` line is the first occurrence. The fixture
  pre-registers expectations, not expected lines.
- Not source truth. A verified span in export text does not verify the export's
  own assertions or its onward citations; the round-1 `export-unverified` limits
  stand (`corpus/knowledge/archived-export-intake.md`, `corpus/README.md`
  Known gaps).
- Not external verification. URLs are refused, never fetched; a claim whose
  warrant lives outside the local corpus cannot pass this mode.
- Not adoption. Fixture spans are byte controls, not knowledge
  (`claims-r2.README.md`, "Boundary"): the B03 numerals remain kengaku-province
  benchmark material that the round-1 intake deliberately did not adopt
  (`MINT.md:45-47`, RJ-03), reproduced only because digit-level byte fidelity is
  where claim-vs-source verification matters.
- Text files only, read whole into memory (`:782`); this is a corpus-local
  checker, not a binary differ.

The fixture's A06/B05 near-miss entries are the controls for why byte-exactness
is the bar: inverted-meaning "quotes" (a dropped `do not`; a fabricated
"exclusively to worker agents") read plausibly but cannot byte-match, so the
mode reports them `unsupported` instead of letting a paraphrase pass
(`claims-r2.README.md`, "Provenance").

## Marker convention

`marker` is present only on `contradicted` entries and is the literal negation
marker the fixture declares; the gate checks span bytes and then marker
co-occurrence inside the span's source lines (`:796-808`). A default marker can
be set once per file via `{"marker_default":…}` (`:740-743`). A
`contradicted` entry whose span lacks its marker is `unproven` (drift against a
pre-registered `contradicted` expectation); a non-`contradicted` entry carrying
a `marker` is a fixture violation caught as `CLAIM_RECORD_INVALID`
(`:761-763`; selftest case 27, `claims-fail-stray-marker`). The two fixture
markers: `could not substantiate` (A05, span at A:64) and `is not a standard
rank sequence` (C06, span at C:53).

## Receipts (frozen revision, run by this seat)

- `sha256sum tools/research-gate.sh` →
  `03a3324455852ea0025115cb0e3ba9c8cdea10da5edc051c4738854a27c14be0`
  (identical across repeated samples; intermediate revisions while the file was
  being written — `ce2edbd`, `445ade4`, `cc93d3b`, `c24d9cf`, `b63e282` — are
  not results). Lane HEAD `6344569`; the verified artifacts are uncommitted
  (` M tools/research-gate.sh`, `?? corpus/fixtures/`); no commits by this seat.
- Selftest: `bash tools/research-gate.sh --selftest` → 30 ok-cases, exit 0:
  the 20 round-1 cases unchanged (cases 21-30: `claims-pass`,
  `claims-fail-tampered`, `claims-fail-out-of-corpus`, `claims-fail-external`,
  `claims-fail-session`, `claims-fail-contradicted-unmarked`,
  `claims-fail-stray-marker`, `claims-fail-counting`, `setup-claims-no-path`,
  `setup-claims-missing-file`), closing
  `RESEARCH_GATE_SELFTEST: PASS (30 cases)`.
- Fixture run: `bash tools/research-gate.sh verify-claims
  corpus/fixtures/claims-r2.jsonl --root ..` → 17/17 `CLAIM … verdict=match`
  (gate-reported `at=` = 52, 80, 81, 88, 64, -, 47, 64, 79, 69, -, 89, 92, 97,
  102, 130, 53 — all agree with the fixture's provenance table), then verbatim:

  ```text
  VERDICT_BEARING_CLAIMS=17/17
  RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)
  exit 0
  ```

  This is exactly the fixture's pre-registered ground truth
  (`claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0`).
- Independent byte-check (the fixture README's gate-free python3 checker, run
  by this seat): `counts {'supported': 13, 'contradicted': 2, 'unsupported': 2}
  bad []`, exit 0.
- Setup boundary: `bash tools/research-gate.sh verify-claims` (no path) →
  stderr `research-gate: claims file required (verify-claims PATH or
  CHOUSA_CLAIMS)` + usage; exit 2; no stdout verdict.
- Round-1 behavior byte-stable: A/B/C each exit 1, intake exit 0; stdout
  matched `.ufo/evidence/round-1/acceptance.json` rows after normalizing the
  `ts=` field only; stderr empty on all four.
- Fixture README execution record, authored by the fixture seat, pins the same
  frozen gate sha and the same summary counts; my runs above are an independent
  second execution at that revision.

## Open items

- **Receipt identity (round 1) — STILL OPEN.** The interactive launch supplies
  no authentic queue taskKey or stored expected receipt bag
  (`.ufo/evidence/round-1/receipt-blocker.json`, `.ufo/continuations/round-1.json`);
  mission acceptance remains integrator-owned, no `task_…` value may be
  invented, and proven receipt-backed completed rounds remain 0 with the
  operator target unchanged (≥100). Routing for this wave was satisfied by the
  operator's in-session direct dispatch; receipt identity was not affected.
- Scope-refusal finding IDs (round-1 debt) — not addressed by this move; the
  documented refusals remain documentary (`SKILL.md:82-84`).
- Non-author spot-check (discernment) — still absent; no promotion is implied
  by this note or by any passing selftest.
- Frozen replay gate conformance — `corpus/evidence/round-1/expected.json` pins
  inputs but is not a rerunnable comparator; still open.
- By design, not debt: semantic verification and any external-source check are
  outside this mode; multi-source or chain-level claim verification is not
  built here.