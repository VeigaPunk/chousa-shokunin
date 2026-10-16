# Chain-hop resolution — round-3 coverage mode (research-gate)

source: lane HEAD `0aa794db58c2aafae0a50b25b8ae9822f4007900`; frozen gate
`tools/research-gate.sh` sha256 `67daf85ecc49c4c7accbee9534c31b0734061b7f329e8de7a98254a57f9d6084`
(mtime 2026-10-15T23:49:26Z; observed identical across every run below);
fixture `corpus/fixtures/chain-r3.md` sha256
`06115f2f8e6db3c60034411dc6be42c4e0887352b09ab9cbd7f760801237ba07`,
control `corpus/fixtures/chain-r3-broken.md` sha256
`b66222a16d4c5323ee6932839ff5746af5f716f36372af506755aed18e0f5c6a`,
their contract `corpus/fixtures/chain-r3.README.md` sha256
`72dbee4e1d8c22df898842f2edf406769c8aa7894fcaecdfe5922137f867292a` (read at
this writing; the README was revised during the wave and its earlier sample
pinned gate `7379b7ee…`, which the implementation then moved past); round-2
claims fixture unchanged sha256
`23d078cbfd032ec5ee7de5c21de65eba3a3cd2989a78281ff61bc6db62188802`; archive
pins `9033857d…` / `6d8dbddd…` / `e48fe70f…`.
verified-at: 2026-10-15, from the lane cwd; fresh-process CLI runs; read-only
local opens only; nothing was fetched or executed
recheck:
`bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..`
· `bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3-broken.md --root ..`
· `bash tools/research-gate.sh --selftest`

All script line numbers below are relative to the frozen revision above.

## The move

Round-1's `verify` checks chain hops STRUCTURALLY only: a hop with
`status=resolved` passes when its `to` names a declared source id or an
existing file path (`tools/research-gate.sh:540-577`; the resolved branch
`:556-561` calls `ptr_resolves_meta` at most — the anchor it cites is never
looked for and the target is never opened). The round's falsifiable claim:
before the move, a hop can cite an anchor that does not exist in the target
and still pass. After the move, `verify-chain <record.md>` resolves each
resolved hop's citation — source under the corpus boundary plus the anchor
present in the target (heading, verbatim quote, or whole line) — emits
per-hop verdicts and `RESOLVED_HOPS=N/M` under the existing CLEAN|DRIFT/exit
contract, while unresolved-or-marked hops stay exempt but counted.

The live before/after pair is `corpus/fixtures/chain-r3-broken.md`: under
`verify` it closes CLEAN, exit 0, because `to=S3` resolves structurally;
under `verify-chain` hop 2 reads `anchor-missing` and the record drifts
(receipts below). The fixture dispatch named `chain-r3.jsonl`; the landed
mode reads Markdown records, so the fixture is the record `chain-r3.md` and
the JSONL pre-draft was superseded and removed rather than kept as a
drift-prone second copy of the same hops (`chain-r3.README.md`, "Authoring
state") — a premise adjustment recorded here, not silently absorbed.

## Mode design (frozen revision)

- CLI: `research-gate.sh verify-chain [RECORD] [--root PATH]` (usage `:106`,
  chain paragraph `:115-121`; dispatch `:1917`, `:1938-1941`); RECORD via
  positional, `--record`, or `CHOUSA_RECORD`. Mode banner = `mode=chain`.
- Input: a research record. `## Sources` is read once into an id→pointer map
  (`:1047-1057`; any id, not only `S…` forms); `## Chain` rows come from the
  shared table reader (`:1142`). Expected columns: `hop`, `status`, `to`,
  `anchor_kind` (alias `kind`), `anchor` (aliases `anchor_text|span|
  fragment|locator`), `notes`.
- Citation grammar (`chain_citation :910-950`): the `to` cell may carry a
  `path#kind:text` fragment; `anchor_kind`+`anchor` columns are the
  alternative form. `kind` ∈ `heading|quote|line`; a bare `#text` fragment
  reads as `heading`; a kind prefix inside the anchor cell
  (`kind:text`) is accepted. Both an anchor column and a `to` fragment, a
  missing source, a missing anchor, or an `anchor_kind` outside the set are
  record violations → `CHAIN_CITATION_INVALID` (warn) and an `invalid` hop
  (`:1078-1082`).
- Source resolution (fails closed, same boundary and canonicalization as
  `verify-claims` — `claim_source_path :684-730`): a `to` naming a source id
  is replaced by that row's pointer (empty pointer → `CHAIN_SOURCE_MISSING`);
  an `S…`-shaped id absent from `## Sources` → `CHAIN_SOURCE_MISSING`
  (`:1084-1097`); any other `to` is a path, canonicalized with
  `readlink -f` and required to resolve under `CHOUSA_ROOT` or the lane
  root. Refusals map to `CHAIN_SOURCE_EXTERNAL` (crit, URL never fetched),
  `CHAIN_SOURCE_SESSION` (crit, denylist/session paths never opened),
  `CHAIN_SOURCE_EPHEMERAL` (warn), `CHAIN_SOURCE_OUT_OF_CORPUS` (crit),
  `CHAIN_SOURCE_MISSING` (warn) (`chain_refuse_id :1017-1024`,
  `chain_source_sev :1027-1031`, `:1101-1108`). Sources are content-read with
  `cat` only after those checks (`:1112`).
- Anchor kinds (`chain_anchor_at :953-985`):
  - `heading` — a Markdown heading line (`^#+` + space), its trailing-
    whitespace-trimmed text required to equal the anchor.
  - `quote` — byte-exact substring of the target; the hit is reported as
    `at=line:N` (first occurrence) or `lines:N-M` for multi-line spans.
  - `line` — one whole line equal to the anchor after trailing-whitespace
    trimming.
- Miss: `observed=anchor-missing`, `verdict=mismatch`, finding
  `CHAIN_ANCHOR_NOT_FOUND` (warn) with `nearest_line`/`context` for
  quote-kind misses via the quote-style probes (`:1117-1123`,
  `chain_nearest :988-1005`).
- Exempt statuses — `unresolved|blocked-no-fetch|rejected|labelled-dead|
  not-applicable` — count as hops read (M) but are never resolved or
  checked; a missing or unknown `status` is `invalid`
  (`CHAIN_CITATION_INVALID`, `:1127-1139`). A record with no `## Chain`, or
  a `## Chain` with no rows, drifts via `CHAIN_ABSENT` (`:1060-1061,
  1143-1144`).
- Per hop: `CHAIN hop=… status=… observed=… source=… anchor=… at=… verdict=…`
  (`observed` verified|anchor-missing|refused|invalid|exempt; `verdict`
  match|mismatch|refused|invalid|exempt, `:1125`). Summary (`:1151-1157`):
  `RESOLVED_HOPS=N/M` where N = verified; CLEAN iff every non-exempt hop
  verified (`N + exempt = M`) and no finding drifts; the closing summary
  carries `hops/verified/exempt/anchor-missing/refused/invalid/findings/
  drift`. Exit contract unchanged: 0 CLEAN | 1 DRIFT | 2 setup/usage
  (setup keeps stdout empty, diagnostics on stderr).

## Anchor semantics

- The mode verifies anchor EXISTENCE, not line binding or uniqueness. The
  reported `at=` is the first occurrence, informational; a duplicate of the
  same bytes elsewhere is neither reported nor required
  (`chain-r3.README.md`, "Hops" preamble).
- Quotes and lines are byte controls: the check is literal containment /
  whole-line equality, so typographic bytes (人為, `→`, `級`/`段`,
  en-dashes, curly quotes) must match exactly; a paraphrase or an
  inverted-meaning "quote" cannot pass.
- Quote containment is not quote integrity: an anchor shortened while it
  remains a substring of the target still resolves — the round's own
  receipts include a one-byte-truncated hop-3 anchor (`…kiwami semantic`)
  that closed CLEAN 17/22 (`chain-r3-20261015T235411Z-live.log`, "negative
  control 1"). Only bytes absent from the target fail, as the broken
  control's `人為 — jin’i-ryū` anchor does.
- Heading is the Markdown form (`#…`); the three archived exports contain
  zero `#` headings (`grep -c '^#'` = 0), so their section-title anchors are
  carried as `line` (whole trimmed line) or `quote`. The `heading` kind is
  exercised by the gate's own selftest on generated records
  (`chain-r3.README.md`, "Honest boundaries").
- Exemption is the record author's declaration, not a resolution: hops that
  cannot resolve locally are marked (`unresolved` with a reason,
  `blocked-no-fetch` for out-of-boundary chips) and remain counted instead
  of silently passing.

## What resolving does NOT establish

- **Not semantic support or agreement.** A present anchor can be
  contextually misleading; the mode never parses meaning. Hop 6 of the
  fixture (A's four axes vs B's five) resolves while the two statements
  disagree — resolution says the target carries the bytes, not that the
  claim follows from them.
- **Cross-input hops are co-anchors only.** The exports do not cite each
  other; cross-input rows (4, 5, 6, 10, 11, 14, 15, 16) assert solely that
  the anchor bytes exist in the target input. They never establish that the
  target cites, endorses, or originates from the source input
  (`chain-r3.README.md`, "Honest boundaries").
- **Exempt ≠ verified.** The five exempt hops of `chain-r3.md` (18–22)
  prove nothing; 20–22 are real chain breaks the record marks instead of
  hiding as structural `resolved`s. The mode cannot check that an
  exemption is truthful — it only forces hops that CLAIM `resolved` to
  carry anchors that exist.
- **Not source truth and not external verification.** Anchor bytes in an
  export do not verify the export's own assertions or its onward citations;
  the round-1 `export-unverified` limits stand
  (`corpus/knowledge/archived-export-intake.md`). URL sources are refused
  unopened — never fetched — so a warrant living outside the local corpus
  cannot resolve in this mode.
- **One hop, one source, no transitivity.** Each row is judged against its
  own target; resolving A→B and B→C does not establish A→C, and no
  chain-level entailment is attempted.
- **Text files only**, read whole into memory after canonicalization
  (`:1112`); carried residuals from round 2 remain: in-root hardlinks still
  bypass path canonicalization (no inode/nlink check in the frozen
  revision) and there is still no size cap on source reads. The banner
  string still reads `research-gate-r1` (cosmetic).

## Receipts (frozen revision, run by this seat)

All runs at gate sha256 `67daf85e…` (identical before and after each run);
lane cwd; fixtures at the shas in the header.

- Selftest: `bash tools/research-gate.sh --selftest` → 40 ok-cases, exit 0,
  closing `RESEARCH_GATE_SELFTEST: PASS (40 cases)`; the first 30
  `ok-case` lines are byte-identical to the round-2 receipt
  `corpus/evidence/claims-r2-20261015T233027Z-selftest.log`; the new cases
  31–40 are `chain-pass`, `chain-fail-tampered`,
  `chain-fail-anchor-kinds`, `chain-fail-out-of-corpus`,
  `chain-fail-external`, `chain-fail-invalid`, `chain-fail-counting`,
  `chain-fail-no-chain`, `setup-chain-no-path`, `setup-chain-missing-file`
  (`:1780-1894, 1900-1901`).
- Positive fixture: `bash tools/research-gate.sh verify-chain
  corpus/fixtures/chain-r3.md --root ..` → 17 × `CHAIN … verdict=match`
  with gate-reported `at=` = 74, 64, 35, 107, 109, 57, 71, 67, 79, 88, 67,
  87, 89, 52, 63, 55, 107 (all agree with the README provenance table),
  then verbatim:

  ```text
  RESOLVED_HOPS=17/22
  RESEARCH_GATE: CLEAN (hops=22 verified=17 exempt=5 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0)
  exit 0
  ```

- Broken control: `bash tools/research-gate.sh verify-chain
  corpus/fixtures/chain-r3-broken.md --root ..` → exit 1, verbatim:

  ```text
  CHAIN hop=2 status=resolved observed=anchor-missing source=research/deep-research-2026-09-28/C-rank-taxonomy.md anchor=quote:"人為 — jin’i-ryū" at=- verdict=mismatch
  FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn surface=chain obs=hop=2 source=research/deep-research-2026-09-28/C-rank-taxonomy.md anchor=quote:"人為 — jin’i-ryū" nearest_line=53 context=The key distinction is between skill, teaching authority, and permission to act.
  RESOLVED_HOPS=1/2
  RESEARCH_GATE: DRIFT (hops=2 verified=1 exempt=0 anchor-missing=1 refused=0 invalid=0 findings=1 drift=1)
  ```

- Before-state: `bash tools/research-gate.sh verify
  corpus/fixtures/chain-r3-broken.md --root ..` → `RESEARCH_GATE: CLEAN
  (findings=0 drift=0 questions=1 sources=2 chains=2 claims=1 negatives=0
  rejections=1 approvals=1)`, exit 0 — the r1 structural hole, live, on the
  same record the new mode drifts.
- Round-2 regression: `bash tools/research-gate.sh verify-claims
  corpus/fixtures/claims-r2.jsonl --root ..` → `VERDICT_BEARING_CLAIMS=17/17`,
  `RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2
  unsupported=2 mismatched=0 …)`, exit 0; stdout matches the round-2 live
  receipt modulo the `ts=` field.
- Round-1 regression: A/B/C under `CHOUSA_NOW_EPOCH=1760000000` and
  `--root ..` → each exit 1, stderr empty, stdout byte-identical to the
  round-2 receipt `corpus/evidence/claims-r2-20261015T233027Z-gate.log`
  sections (no normalization needed).
- Independent check without the gate (this seat's own python, `/tmp` only;
  source-id resolution + heading/quote/line semantics re-implemented):
  `chain-r3.md` → `hops=22 verified=17 exempt=5 anchor-missing=0 refused=0
  invalid=0`, `RESOLVED_HOPS=17/22`; `chain-r3-broken.md` → `hops=2
  verified=1 anchor-missing=1`, `RESOLVED_HOPS=1/2`. The fixture README's
  separate gate-free byte-check reports the same (`bad_hops=[]` and
  `bad_hops=['2']`).
- Zero network: `strace -f -e trace=network` around the positive
  `verify-chain` run recorded no socket/connect/network syscall at all (the
  trace contains only SIGCHLD/exit lines); exit 0. The mode's only reads are
  the record and the cited canonicalized sources under the allowed roots.
- Standing machine-cut receipts (receipts-writer seat, cut after this seat's
  runs, same frozen gate and fixture shas):
  `corpus/evidence/chain-r3-20261015T235411Z-fixture.log` (`77c6bd14…`),
  `-gate.log` (`4f672db6…`), `-live.log` (`8ac9903e…`), `-selftest.log`
  (`a4bd6578…`). They agree with every result above and add the r2-gate
  before-states (structural CLEAN on both records), the out-of-corpus and
  external-URL refusals (`CHAIN_SOURCE_OUT_OF_CORPUS` / `CHAIN_SOURCE_EXTERNAL`
  crit, never fetched), an existing-anchor hop re-marked `unresolved` →
  exempt, `RESOLVED_HOPS=16/22`, CLEAN (the live demonstration that an
  exemption is the author's declaration and is not itself checkable), the
  one-byte-truncated quote control above, and the same zero-network strace
  result (0 network syscalls). Their labels are read literally: the receipt
  marked "tampered quote anchor" closed CLEAN because the truncation stayed
  a substring.

## Open items

- **Receipt identity (round 1) — STILL OPEN.** These are lane-local
  evidence runs, not queue taskKey/expected-receipt bags; mission acceptance
  remains integrator-owned and no `task_…` value may be invented. Proven
  receipt-backed completed rounds remain 0; the operator target is
  unchanged (≥100), routing supplied by the operator's in-session direct
  dispatch.
- No commits by this seat; the gate and fixtures are uncommitted lane
  changes at lane HEAD `0aa794d` (`tools/research-gate.sh`,
  `corpus/fixtures/chain-r3*.md`); parent integrates under the chousa lane
  identity.
- `SKILL.md` gate rows are the skill-row-updater seat's write, not this
  note's; nothing here should be read as a promotion or field-readiness
  claim.
- Scope-refusal finding IDs and the non-author admit/reject spot-check
  remain as in round 1/2 (documentary province boundary; discernment
  unchanged).
- By design, not debt: semantic support, source truth, transitive chaining
  and external-source verification are outside this mode.