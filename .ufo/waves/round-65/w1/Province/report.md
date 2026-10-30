# Province scan — round65 w1, seat Province (chousa-shokunin)

Scope (assigned): read-only scan of chousa and sibling provinces for **receipt
identity**, **generic testing**, **orchestration**; identify contested ground;
**no absorption**. Frozen claims read at
`corpus/evidence/round65/claims.md` (freeze `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`,
base master `d6ed8155e9b4735639a2cf0a3e479c62f2056195`, exactly C1 + C2).
No probes, no tests, no git mutations, no writes outside this folder. No tools
installed (none needed). No scratch used (`/fast/scratch/hyaku/chousa-r65/Province/`
never created, so nothing to delete).

All paths below are relative to the fleet root `/home/vgpnk/Projects/shokunin`
unless absolute. Line numbers are working-tree reads today; sibling declarations
drift (kotoba's round-74 re-pin found 15/20 round-49 pins stale,
`kotoba-shokunin/PROVINCE.md:53`), so these are citations of bytes read, not
frozen pins.

## 1. Receipt identity

### Observed — chousa's own ground supports C1/C2, lane-local

- `chousa-shokunin/PROVINCE.md:1-14`: owns deep-research method, its own corpus
  and gates; refuses orchestration (→ kumitate), model-quality/eval (→ kengaku),
  bounty claim packages (→ kasegi), secret values (→ kagi, shape-only here).
  "Out of province → report, never absorb."
- `kama-shokunin/PROVINCE.md:167-170`: prior cross-lane cession — "The generic
  pinning *method* (how to pin any repo tag) is chousa's ground; the specific
  re-pin of the two held docs rows is kama's." C1's `tools/receipt-pin.py`
  (revision + blob-digest pinning) sits squarely on already-recognized chousa
  ground. No sibling contests the generic pinning method.
- In-lane precedent for receipt↔revision binding: QUALITY 42 `receipt-binding`
  census (`chousa-shokunin/SKILL.md:128`, `git rev-list --all` + `cat-file
  --batch`, UNBOUND landed/final receipts gate) and the round-38/39
  `RECEIPT_BINDING_MATCH=7/7,8/8` counters (`SKILL.md:100-101`). C1 continues
  existing lane ground; it is not new cross-lane territory.
- `chousa-shokunin/SKILL.md:159-160` already carries the r65 `receipt-pin` and
  round65-counter gate rows ("header consistency only, never execution
  authenticity") — registration matches the frozen claims.
- C2's anchors verified in-lane: `corpus/SOURCES.md` rows S154 (git-cat-file(1),
  blob bytes not working-tree bytes), S155 (`/usr/lib/python3.14/hashlib.py`,
  digest of supplied bytes, not provenance), S156 (round64 before receipt
  `c1v3-before-full.txt:1-44` — confirmed read: 44 LEG verdict lines with no
  REVISION/EXIT/SHA256 headers), S157 REJECTED (validator docstring as execution
  proof). The reference validator `corpus/evidence/round65/controls/ref-receipt-pin.py`
  is exactly a consistency checker: header shape, caller-supplied `--revision`
  equality, `git cat-file blob <rev>:<path>` digest, read-only.

### Observed — sibling "receipt" semantics are different in kind; none conflict, none may be absorbed

- **souji** (`souji-shokunin/PROVINCE.md:3-4,95-97`): receipt-gated removal;
  evidence-integrity checking limited to its own receipt fragments, "does not
  become fleet orchestration or an independent promotion authority." Its pushed
  receipt establishes removal-safety/recoverability only
  (`mori-shokunin/PROVINCE.md:89,184-188`).
- **souji jj receipt-root rule** (`souji-shokunin/PROVINCE.md:114-124`): in
  colocated repos every ref except `refs/jj/*` is a durable receipt root;
  `refs/jj/keep/*` is a GC grace ref, "never a receipt of record."
- **mori** (`mori-shokunin/PROVINCE.md:179-181,199-205`): actor identity fields
  are declared evidence requiring outside adjudication, "not authenticated by
  mori's hash checker"; a reconciler receipt match is accounting agreement only,
  not authentication, and cannot authorize baseline acceptance, cleanup, reap,
  continuation or dispatch.
- **kaidoku** (`kaidoku-shokunin/PROVINCE.md:32-35`): "the evidence ID alone
  does not authenticate module attribution"; round-27 renamed-copy identity work
  (`:314-335`) measured content-keyed vs rename-sensitive evidence IDs — object
  identity ≠ content digest ≠ attribution, empirically, on kaidoku's own RE
  surfaces.
- **kagi** (`kagi-shokunin/PROVINCE.md:37`): `~/.local/bin/tac-check`, offline
  receipt check for credential handoff custody.
- **tsukuroi** (`tsukuroi-shokunin/PROVINCE.md` Core): pacman `.pkg.tar.zst`
  receipt discipline — package receipts, an unrelated kind sharing only the word.
- Duplicate-tooling check: grep for `RECEIPT_PIN|receipt-pin|receipt_pin` over
  nine sibling/chousa tool directories (tameshi/tools, kumitate/scripts,
  kaidoku/tools, mori/tools, souji/tools, kama/tools, kagi/corpus,
  tsukuroi/tools, chousa/tools) → **0 matches**. No competing implementation;
  chousa `tools/receipt-pin.py` does not exist yet (C1 before-state: absent
  target, consistent).

### Contested ground (report only)

- **G1 — "receipt" is a six-lane homonym.** Removal receipts (souji), accounting
  receipts (mori), evidence-ID envelopes (kaidoku), custody receipts (kagi),
  package receipts (tsukuroi), and chousa's git-blob header receipts carry
  different guarantees. C2's four-way distinction (object identity / content
  digest / reported exit / execution authenticity) must stay scoped to chousa's
  receipt class and cite siblings, never generalize over them. A fleet-wide
  receipt taxonomy is protocol/integrator ground (`PROTOCOL.md:457-461`).
- **G2 — revision durability is not chousa's call.** C1 binds a digest to the
  blob at a caller-supplied revision; whether that revision is a *durable*
  receipt root is souji's admitted jj rule, and jj-workspace seat containment is
  kumitate's round-64 ground (`kumitate-shokunin/PROVINCE.md:22`). C1 correctly
  stops at consistency; any durability adjudication must be reported out, not
  absorbed into the validator or the C2 entry.
- **G3 — execution authenticity is unowned and disclaimed everywhere.** C1
  explicitly disclaims it; mori and kaidoku precedents above support the
  disclaimer. kengaku's round-11 preregistration-standard referral
  (`kengaku-shokunin/PROVINCE.md` round-11 report-outs) sets the pattern:
  fleet-wide standards go to protocol/integrator. Any future signed-receipt or
  execution-authenticity work routes to kagi (credential custody) plus the
  integrator — never chousa.

## 2. Generic testing (verification / mutation craft)

### Observed

- **tameshi owns the reusable craft, not the gates**
  (`tameshi-shokunin/PROVINCE.md:3-17`): hermetic suites, mutation testing,
  fail-closed arms, verdict-line discipline, before/after proof. "Every lane's
  gate remains its own; tameshi owns only the reusable craft (a pattern is
  admitted from evidence in TWO independent lanes before it is claimed
  general). Never edits a sibling's gate code (read-only probes; recommendations
  travel in round reports)." Kotoba's census independently classifies tameshi
  adjacent on exactly this basis (`kotoba-shokunin/PROVINCE.md:75`).
- C1's counter design (before control 0/20, always-pass 3/20, always-fail
  17/20, exact exit+token per case, 20/20 target) is tameshi's published
  discipline applied to chousa's own gate — the expected, uncontested pattern.
  Chousa has run this shape since round 29 (`SKILL.md` Gates table).
- Round64 battery/mutation continuation: L1 considered but did **not** declare
  it this round (claims.md preamble: "those require independently validated
  oracles first"). Round64's instruments are registered as an evidence-only
  exemption — "historical evidence; never admission gates for a successor";
  frozen C1 literal `BATTERY=FAIL`, C3 `C3=FAIL`, supplement `BATTERY=PASS`
  replaces neither (`chousa-shokunin/SKILL.md:158`).

### Contested ground (report only)

- **G4 — generalizing receipt-pin into a generic/fleet receipt-test harness
  would triple-cross:** tameshi's two-independent-lanes admission rule, the
  each-lane-owns-its-gate rule, and protocol integrator arbitration
  (`PROTOCOL.md:457-461`). Keep C1 lane-local; method recommendations travel to
  tameshi as report text (the tsukuroi ADJ-07 handoff pattern,
  `tsukuroi-shokunin/PROVINCE.md` ADJ-07: "ask for method advice, not transfer
  of gate ownership or a general claim from one lane").
- **G5 — C2's structural counter is not a quality oracle.** claims.md itself:
  "A boilerplate entry could pass; no semantic-quality claim rests on this
  counter alone," and the structural counter "cannot establish entailment."
  This matches chousa's own QUALITY 66 (`SKILL.md:73`: a passing entry still
  needs a reader). Do not let any seat upgrade ENTRY_CHECKS=10/10 into a
  generic sourced-knowledge-quality test — that would be both a tameshi-method
  overclaim and a kengaku-style evaluation claim chousa refuses.

## 3. Orchestration

### Observed

- **kumitate owns orchestration & tooling** (`kumitate-shokunin/PROVINCE.md:3`):
  OMP task/hub, ufo-fsd scripts/runtime; wave plan/run/record/collect semantics
  (via `mori-shokunin/PROVINCE.md:65`); isolation substrates and jj-workspace
  seat containment (`:22`); multi-agent coordinator topology *decisions*
  (`:24`, "adjacent, not absorbed: kengaku evaluates agents, this lane arranges
  the seats"). Its Adjacent list routes "Research method → chousa"
  (`kumitate-shokunin/PROVINCE.md` Adjacent) — the reverse of chousa's refusal;
  the boundary is mutually declared and clean.
- **chousa refuses orchestration explicitly** (`chousa-shokunin/PROVINCE.md`
  Refuses): "orchestration, multi-agent dispatch and agent lifecycle (→
  kumitate — the mint's roster scan rejected it as complementary, and this
  clause closes that omission)."
- **mori observes, never verdicts** (`mori-shokunin/PROVINCE.md:23,46,119-120`):
  wave-settlement reporting is filesystem shape only; kumitate owns
  orchestration/result semantics; "receipt review stays offline"; "No scan is an
  orchestration verdict."
- Round65's wave artifacts (`.ufo/waves/round-65/w1.ready.dispatched`,
  `w1/swarm-registry.json`, the freeze/kill rule, L1-only integration) are
  orchestration surfaces under fleet PROTOCOL. Seats report anomalies; they
  never repair or claim them. Protocol arbitration for any contested scope:
  integrator refines PROVINCE.md and records the ruling; "silence is not a
  ruling and must never default scope to whichever lane wrote first"
  (`PROTOCOL.md:457-461`).

### Contested ground (report only)

- **G6 — no orchestration claims from this wave.** Any seat finding about
  dispatch, seat containment, wave settlement, or roster semantics (including
  ones motivated by receipt validation, e.g. "receipt X proves seat Y ran") is
  kumitate/mori ground and kagi/integrator ground respectively — report in the
  lane report, never absorb into C1/C2. C1's "reported exit" is a header field,
  not dispatch evidence; this is precisely C2's distinction applied to
  orchestration.
- **G7 — neighboring open splits are not chousa's.** The only open ownership
  split encountered in the scan is kaidoku↔revenger shipped-artifact RE
  (`tsukuroi-shokunin/PROVINCE.md` ADJ-06 + Frontier; `kotoba-shokunin/PROVINCE.md:62`
  kaidoku row). Kotoba's round-74 census classifies chousa **adjacent** with no
  contested cell: "chousa owns the research method, its tools and gates"
  (`kotoba-shokunin/PROVINCE.md:57`). No absorption of the RE split; no
  contested classification against chousa found.

## Contested-ground ledger for L1

| ID | Ground | Adjacent owner(s) | R65 exposure | Disposition |
|---|---|---|---|---|
| G1 | "Receipt" homonym across 6 lanes | souji, mori, kaidoku, kagi, tsukuroi; protocol for taxonomy | C2 entry wording | Scope C2 to git-blob header receipts; cite, never generalize |
| G2 | Revision durability / receipt roots | souji (jj refs), kumitate (jj workspaces) | C1 `--revision` semantics | Validator stays consistency-only; durability questions reported out |
| G3 | Execution authenticity | unowned; kagi + integrator for any future signing | C1 disclaimer, C2 fourth category | Keep disclaimer; no authenticity machinery in lane |
| G4 | Generic/fleet receipt-test harness | tameshi (two-lane rule), each lane's gate, integrator | C1 framing | Lane-local gate; method notes to tameshi as recommendations |
| G5 | Structural counter ≠ semantic quality | tameshi (method), kengaku (eval, refused) | C2 scoring interpretation | ENTRY_CHECKS stays structural; source/claim review separate |
| G6 | Wave/dispatch/seat semantics | kumitate, mori (observation only) | Wave artifacts, seat reports | Report anomalies only; zero orchestration claims in C1/C2 |
| G7 | kaidoku↔revenger RE split | integrator (unruled) | None directly | Not chousa's; do not absorb or arbitrate |

## Limits

- Read-only working-tree scan; no commit-pinned sibling re-reads (unlike
  kotoba's round-74 census). Sibling declarations can drift after this read.
- Grep-based keyword scan (`receipt|identity|oracle|generic|orchestrat`) over
  14 sibling PROVINCE.md files plus full reads of chousa, tameshi, kumitate and
  targeted reads of tsukuroi/kengaku/kotoba; not an exhaustive corpus read of
  every sibling SKILL.md/LOG.md. A contested claim buried only in a sibling
  corpus entry could be missed.
- No verification of round65 tooling performed (other seats own probes/attacks);
  this report is scope/boundary evidence only and carries no shipping authority.
