# hardening-r10.md — archive-scale negative controls, the exempt-item audit, and the final limit-disposition ledger (the round-11 audit's starting map)

source: gate `tools/research-gate.sh` sha256
`46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd` — unchanged
through round 10 (fixture-led by design: re-derived at 05:37Z and 05:44Z; the
working-tree sha equals the lane HEAD `d5c99c2` blob and
`git diff --numstat tools/research-gate.sh` is empty; a gate change without a
reported defect would itself be a finding — none occurred, and none was
needed). Records `corpus/fixtures/archives-r9/{A,B,C}-r9.md` at
`338918fc…` / `abfa5290…` / `97be0e69…` (re-derived); archive sources at
`9033857d…` / `6d8dbddd…` / `e48fe70f…`; controls under
`corpus/fixtures/archives-r9/controls/` at the shas in §1 (their README
`23f477225aa290c0c3fdf97887b9d954d9b81ab1bb4364815fcd01b07380a688`); shared
claims surface `corpus/fixtures/claims-r9.jsonl` `f6f0d1ab…`.
verified-at: 2026-10-16T05:35–05:45Z, from the lane cwd (`--root ..`), fresh
processes, read-only local opens only; nothing fetched; this seat wrote no
lane file but this note.
recheck:
`bash tools/research-gate.sh --selftest`
· `bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r8-20261016T033757Z.json`
· one `verify-all` per control (§1; the controls README carries the re-run
loop) · `bash tools/research-gate.sh verify-all corpus/fixtures/archives-r9/A-r9.md --root ..`

Abbreviations used below: r2 note = `corpus/knowledge/claim-verification-r2.md`;
r3 note = `chain-resolution-r3.md`; r4 note = `anchor-boundaries-r4.md`;
r5 note = `sweeps-rejections-r5.md`; r6 note = `verify-all-r6.md`;
r7 note = `reference-integrity-r7.md`; r8 note = `gate-baseline-r8.md`;
r9 note = `archives-verified-r9.md`; README gaps = `corpus/README.md`
§Known gaps; controls README = `corpus/fixtures/archives-r9/controls/README.md`.

## 1. The controls suite — six broken archive records, one per defect class

Round 10's first move: negative controls at archive scale. Before this round
no broken archive record existed (`ls corpus/fixtures/archives-r9/controls/` →
No such file or directory at 05:35Z; the lane's only negatives were
small-fixture scale). Six controls now exist, each a byte-copy of one clean
archive record with the defect isolated to one section (diff-verified by this
seat: exactly the `## Meta` `note` row plus the defect cell(s)); the
span-not-found control additionally binds a per-control claims copy. The
authoring asserts, the class table, and the full measured outputs are in the
controls README; this section records what this seat independently measured
(fresh runs, 05:41:15–05:42:10Z) and the class map.

| control (sha256) | class | base | defect edit (besides note row) | drifting section (tally) | finding id | exit |
|---|---|---|---|---|---|---|
| `A-r9-span-not-found.md` `5dedb73b…` (+ `A-r9-span-not-found.claims.jsonl` `0edb78ee…`) | span-not-found | A | `claims_file` → control copy; copy mutates A07 span `keep four axes separate…` → `keep five axes separate…` (absent from A) | claims DRIFT `VERDICT_BEARING_CLAIMS=9/10` | `CLAIM_SPAN_NOT_FOUND` | 1 |
| `A-r9-anchor-missing.md` `e3490cf4…` | anchor-missing | A | hop 2 anchor `…not a universal rank ladder.` → `…not a universal certification ladder.` (absent from A) | chain DRIFT `RESOLVED_HOPS=5/7` | `CHAIN_ANCHOR_NOT_FOUND` | 1 |
| `B-r9-rejection-missing-flip.md` `b0d488aa…` | rejection-missing-flip | B | R2 `flip_condition` cell emptied | sweeps DRIFT `VERIFIED_SWEEPS=1/1 REJECTIONS_OK=2/3` | `SWEEP_REJECTION_INCOMPLETE` | 1 |
| `B-r9-false-sweep.md` `69b7b08f…` | false-sweep | B | SW1 `where` → `research/deep-research-2026-09-28/*.md` (a glob the archive directory satisfies) | sweeps DRIFT `VERIFIED_SWEEPS=0/1 REJECTIONS_OK=3/3` | `SWEEP_CLAIM_FALSE` | 1 |
| `C-r9-dangling-ref.md` `b24be0f0…` | dangling-ref | C | hop 1 `from` `C1` → undeclared claim id `C9` | integrity DRIFT `refs=15 resolved=13 unresolved=1` | `REF_UNRESOLVED` | 1 |
| `C-r9-structure-break.md` `21d77e6c…` | structure-break | C | `## Question` section (heading and body) removed | structure DRIFT `findings=1` | `NO_QUESTION` (crit) | 1 |

The six finding lines, verbatim from this seat's runs (the composed line read
`VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1` and
`RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=1
drift=1)` on every control; exit 1 everywhere):

```text
FINDING CLAIM_SPAN_NOT_FOUND severity=warn surface=claims obs=id=A07 nearest_line=35 context=Deep research: The shokunin (職人) concept in Japanese artisan tradition — a
FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn surface=chain obs=hop=2 source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"The sources point to craft-specific apprenticeship systems, " nearest_line=47 context=The sources point to craft-specific apprenticeship systems, not a universal rank
FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=id=R2 missing=flip
FINDING SWEEP_CLAIM_FALSE severity=warn surface=sweeps obs=id=SW1 where=research/deep-research-2026-09-28/*.md hits=3 first=research/deep-research-2026-09-28/A-shokunin-tradition.md listed=research/deep-research-2026-09-28/A-shokunin-tradition.md research/deep-research-2026-09-28/B-multiagent-knowledge.md research/deep-research-2026-09-28/C-rank-taxonomy.md
FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=claim id=C9 section=chain row=1 cell=from
FINDING NO_QUESTION severity=crit surface=question obs=missing ## Question section
```

Measured properties (this seat, independent of the controls README's own
runs — the two agree on every verdict, class and tally, modulo `ts=` and run
order):

- **Exactly its class.** In all six runs exactly one section drifted, with
  exactly one finding; every other section closed CLEAN with its base
  record's tallies (A: claims 10/10 · sweeps 1/1 `REJECTIONS_OK=4/4` ·
  integrity `refs=13 resolved=12 unresolved=0`; B: 10/10 · 1/1 3/3 ·
  14/13/0; C: 10/10 · 1/1 4/4 · 15/14/0; structure CLEAN 0/0 in all six).
  The clean bases stay CLEAN in the same window (controls README §Clean
  bases; this seat's solo runs on A/B/C — chain 6/7 · 6/7 · 7/8, integrity
  13/12/0 · 14/13/0 · 15/14/0, sweeps 1/1 with 4/4 · 3/3 · 4/4 — match).
- **The class set is the round's.** The six classes named by the round
  (span-not-found, anchor-missing, dangling-ref, rejection-missing-flip,
  false-sweep, structure-break) map one-to-one onto the six controls; each
  DRIFTs `verify-all` naming exactly its class.
- **structure-break is `NO_QUESTION`, not `RECORD_SCHEMA_INVALID`, by
  measurement**: a full-schema break drags three more structure findings into
  the same run (controls README §Why structure-break is `NO_QUESTION`), so
  the smallest single-finding edit (remove `## Question`) is the isolated
  class.
- **No gate defect surfaced; no gate change.** The battery ran at the
  unchanged `46f5ddb3…`; every observed behavior matches the documented
  contracts (r2–r7 notes). Nothing in this suite required or motivated a gate
  edit. The one known defect *class* no mode catches — a row pointer's
  `path:line` is never compared with its span's occurrence line — is row 56
  of §3 and predates this round (r9); it was not one of this round's six
  classes and was deliberately not acted on ("no gate change without a
  reported defect" — the defect is reported, the decision is not this
  round's).

Named non-coverage of the set (controls README §What this set does not
cover; carried into §3.7): one class per record, no multi-defect interaction;
no out-of-corpus/URL/session refusals at archive scale (the small r2/r3
fixtures own refusal classes); no semantic-drift detection (r8 note owns that
cannot-catch); one existence proof per class, not a measured fraction of
defect space. The false-sweep control's `hits=`/`listed=` values are
directory-at-runtime properties (3 hits measured); the class and finding id
are not.

## 2. The exempt-item audit — 6/6 justified by source bytes

Round 10's second move. Before: every archive record carries exempt items
that every mode counts but never resolves, and no audit existed saying the
exemptions are truthful. This seat's audit at the unchanged gate found the
complete exempt set — **6 items, 6/6 justified, 0 findings**. The composition
is exhaustive across modes: structure has no exempt class; claims has none
(all 10/10 matched, `refused=invalid=0`); sweeps count `exempt=0` on all
three records (`VERIFIED_SWEEPS=1/1`; the named `saved-*`/`*-snapshot-*`
globs re-run empty); chain carries one `blocked-no-fetch` hop per record;
integrity carries one exempt token per record (`refs−resolved−unresolved =
1`). The six items, verbatim from this seat's solo runs:

```text
A-r9.md: CHAIN hop=7 status=blocked-no-fetch observed=exempt source=コトバンク anchor=- at=- verdict=exempt
          REF kind=claim id=C1 section=chain row=7 cell=from observed=exempt verdict=exempt status=blocked-no-fetch
B-r9.md: CHAIN hop=7 status=blocked-no-fetch observed=exempt source=arxiv.org anchor=- at=- verdict=exempt
          REF kind=claim id=C3 section=chain row=7 cell=from observed=exempt verdict=exempt status=blocked-no-fetch
C-r9.md: CHAIN hop=8 status=blocked-no-fetch observed=exempt source=jstage.jst.go.jp anchor=- at=- verdict=exempt
          REF kind=claim id=C8 section=chain row=8 cell=from observed=exempt verdict=exempt status=blocked-no-fetch
```

Per-item justification against the read-only archive bytes (the exemption's
claim is that the hop cannot resolve locally because the target is citation
furniture and nothing external is opened):

1. **A hop 7 `コトバンク`** — the hop note names "the A:68 chip naming the
   aggregator behind A's lexical checks"; source bytes: A:68 is the bare chip
   `コトバンク` alone on its line (preceded at A:67 by the Daijisen / Nihon
   Kokugo Daijiten / Kanjipedia sentence; collapsed counter `+3` at A:69;
   second chip A:72). A bare aggregator name is not a URL and not a local
   path; the archives contain zero `https?://` strings (r1 W2 / r9 census),
   no local copy exists, and the window opens nothing external. JUSTIFIED.
2. **B hop 7 `arxiv.org`** — the hop note names "the B:51 and B:72 chips";
   source bytes: B:51 and B:72 are the bare host `arxiv.org` alone on its
   lines (`+6` at B:73). Same justification. JUSTIFIED.
3. **C hop 8 `jstage.jst.go.jp`** — the hop note names "the C:103 chip behind
   the Todo/Murata reference"; source bytes: C:102 carries the Todo/Murata
   sentence, C:103 is the bare host `jstage.jst.go.jp` alone on its line.
   Same justification. JUSTIFIED.
4–6. **The three integrity tokens** (A `C1`, B `C3`, C `C8`) are the
   `from` cells of those same exempt-status rows; the integrity contract
   counts an exempt-status row's reference tokens exempt, and each token is a
   **declared** claim id in its record (A `## Claims` declares C1; B C3; C
   C8) — the exemption covers tokens that would have resolved anyway, so no
   undeclared or dangling id hides behind it. JUSTIFIED.

Agreement: the scribe's independent audit
(`.ufo/round-10/goal-wave/report-draft.md` §The move, part 2) captured the
same 6 items from its own runs and reached the same 6/6 justification — two
witnesses, same result.

Boundary of the audit (kept named, not hidden): exemption truthfulness is
still not mode-checkable (r3 limit; §3 row 19). This audit byte-justifies
exactly the three records' six exempt items; it says nothing about any other
record's exemptions. Adjacent carried defect, re-derived here: `A-r9.md:50`
(row C3) cites `A:76` while its span occurs at `A:86`; this seat's gate-free
re-run of all 19 in-record claim rows returned `18 MATCH / 1 MISMATCH` (the
single miss is A C3), reproducing the r9 audit and confirming the row is
still live at record sha `338918fc…` (§3 row 56).

## 3. The final limit-disposition ledger

Every limit named across rounds 2–9 (plus the r1-origin debts and the new
limits this round surfaced) in one place, dispositioned.

Disposition vocabulary:

- **closed(rN)** — a later landed check covers it (round named);
- **by-design** — a permanent boundary of a structural, local-only method
  (semantic truth, external fetch ban, author-declared exemptions, selection
  in a conversion, one-invocation pins …): no local falsifier exists;
- **carried** — still open; a named candidate with no landed closure; it
  belongs in the round-11 audit queue;
- **finding** — a measured defect with a path;
- **operator** — mission-level debt outside gate scope.

Rows marked ⊕ are additions beyond the scribe's on-disk enumeration
(`.ufo/round-10/goal-wave/report-draft.md` §Named limits, read 05:44Z) —
drawn this seat from the notes, the lessons and README gaps; no separately
named `limit-ledger` artifact was observed on disk (searched the `corpus/`
tree and `.ufo/round-10/` at 05:44Z — the scribe draft's enumeration is the
only on-disk one). Completeness: every enumerated class has a row here
(mapped item-by-item); §3.7's r10 rows (63–66) are new this round.

### 3.1 Matching semantics and boundaries (r2–r4)

| # | limit (as named) | origin | disposition | evidence |
|---|---|---|---|---|
| 1 | occurrence of bytes ≠ semantic support / agreement / context | r2 §limits; r3; r4 | by-design | r2/r3/r4 notes; r3 hop 6 resolves across disagreement; r9 custody |
| 2 | not location binding or uniqueness (`at=` is the first occurrence, informational) | r2, r3 | by-design | notes |
| 3 | `contradicted` arm is structural (a declared marker literal, not negation inference) | r2 | by-design | r2 §marker convention |
| 4 | not source truth (an export's own assertions / onward citations) | r2 | by-design | r2 note; r9 §5.5 chain-of-custody |
| 5 | not external verification; refusals absolute (URLs/session/out-of-corpus refused unopened; no fixture can pre-register past a refusal) | r2 | by-design | r2 note; strace zeros r2–r9; archives' zero-URL census |
| 6 | not adoption (fixture spans are byte controls; exports stay tier `export`) | r2 | by-design | r2 note; MINT RJ-03; r9 README tier rule |
| 7 | text files only, read whole into memory (not a binary differ) | r2 | by-design | r2 note |
| 8 | in-root hardlinks bypass path canonicalization | r2 (critic) | carried | carried residual r3–r7; re-derived 05:41Z: no inode/nlink/`-samefile` logic in the gate at `46f5ddb3…` |
| 9 | no size cap on source reads | r2 (boundary-tester) | carried | carried residual r3–r7; re-derived 05:41Z: no size cap in the gate |
| 10 | banner still reads `research-gate-r1` (cosmetic) | r2 | carried (cosmetic) | carried residual r3–r7; `VERSION=research-gate-r1` at `tools/research-gate.sh:227` |
| 11 | claim-label sentence never compared with its span (a label can assert the opposite of its span) ⊕ | r2 lesson | carried | `lessons/2026-10-15-claims-span-fidelity.md`; README gaps; claims mode reads id/source/span/expect only |
| 12 | glued truncation/padding resolved (the r3 substring class) | r3 | closed(r4) | r4 before→after (claims TA1/TA2, chain hop 2/3 DRIFT at `6b83705b…`) |
| 13 | token-aligned shortening still passes (whole words dropped at genuine edges — the residual substring gap) | r4 | carried | r4 §cannot (TA3, hop 4 resolve); round-11 candidate |
| 14 | non-ASCII-adjacent edges fail closed (typographic `” ’ — 。 →` neighbours are misses — also a false-negative risk) | r4 | carried | r4 probe battery (15/86); candidate: promote typographic punctuation, unasserted as safe |
| 15 | `_` is a boundary by decision (identifier-like gluing residual) | r4 | by-design | r4 header/note |
| 16 | only outer edges checked (a multi-line span may cut mid-token inside) | r4 | by-design | r4 note |
| 17 | `heading`/`line` kinds stay trimmed equality (no boundary question) | r4 | by-design | r4 note |
| 18 | only resolved hops affected; exempt hops unchanged | r4 | by-design | r4 note |

### 3.2 Chain / hops (r3)

| # | limit (as named) | origin | disposition | evidence |
|---|---|---|---|---|
| 19 | exempt hop = author's declaration; the mode cannot check truthfulness (general class) | r3 | by-design (+r10 audit of the 6 actual instances) | r3 note; §2 above; r10 audit justifies exactly the records' items, widens nothing |
| 20 | cross-input hops are co-anchors only (no citation, authorship or endorsement established) | r3 | by-design | r3 note; r9 no-cross-citation grep 0/0/0 |
| 21 | one hop, one source; no transitivity / chain-level entailment | r3 | by-design | r3 note |
| 22 | `heading` kind unusable against the archives (zero `#` lines; r9 records use `quote`/`line`) | r3 | carried (contextual) | r3 note; r9 lesson m2; selftest covers `heading` on synthetic records only |
| 23 | `nearest_line` is a heuristic, not a location claim ⊕ | r3 lesson | by-design (informational) | r3 lesson |
| 24 | r3 note cites a superseded receipt log for its one-byte-truncation example ⊕ | README gaps | carried (documentation) | README gaps; the fact is re-established by r4's before-state |
| 25 | `to` written `path#kind:text` drifts structure while chain resolves it (r1-vs-r3 seam) | r7 (b16), r9 | carried | r7 catalog b16; r9 authoring notes; deliberately unfixed |

### 3.3 Sweeps (r5)

| # | limit (as named) | origin | disposition | evidence |
|---|---|---|---|---|
| 26 | flip-condition checked for presence only; vacuous / placeholder / tautology / never-fires / vague strings pass | r5 | carried | r5 class table (12 probes); candidate: placeholder blacklist, not built |
| 27 | the recorded sweep command is never executed; its `observed` prose is never compared | r5 | by-design | r5 note |
| 28 | emptiness of the named location set ≠ the right place to have looked ⊕ | r5 | by-design | r5 note |
| 29 | sweeps mode does not flag section absence (r1 `verify` owns it; the modes compose) | r5 | carried | r5 open items; r6 omission limit |
| 30 | non-local / declared-source-id / status-exempt sweeps are exempt-but-counted | r5 | by-design | r5 note; r9 records' sweeps count exempt=0 |

### 3.4 Composition (r6)

| # | limit (as named) | origin | disposition | evidence |
|---|---|---|---|---|
| 31 | r5 fixture README desync (resynced in-wave) — kept for the record | r5 | closed(in-wave) | r5 open items |
| 32 | omission limit: an absent section is reported, never asserted to have been needed; the claims-surface omission composes CLEAN | r6 | carried (r7 candidate, not taken) | r6 §omission; README gaps |
| 33 | sweeps-with-only-rejections representation seam (`VERIFIED_SWEEPS=0/0` run rather than absent) | r6 | carried | r6 note; `full-r6.README.md` |
| 34 | nested execution cost (one fresh subprocess per run section) | r6 | by-design | r6 note |
| 35 | composed CLEAN covers only RUN sections and inherits every mode limit | r6 | by-design | r6 §what composed CLEAN does not prove |
| 36 | manifest is append-only by discipline: never read back, foreign lines preserved unvalidated, record/gate shas bind the recorded bytes; schema growth beyond `chousa-verify-all/v1` unmapped | r6 | by-design | r6 lesson; README gaps |
| 37 | two transient r6 revisions during the wave (recorded on the record, fixed) | r6 | closed(in-wave) | r6 note |

### 3.5 Reference integrity (r7)

| # | limit (as named) | origin | disposition | evidence |
|---|---|---|---|---|
| 38 | duplicate declarations tolerated (declared-ness is set membership) | r7 | carried | r7 catalog b17 |
| 39 | non-id-shape variants invisible (`C.` trims to `C`, not id-shaped) | r7 | carried | b26 |
| 40 | lowercase id-shaped tokens invisible (id shapes are case-sensitive) | r7 | carried | b11/b34 |
| 41 | kind-blind: a wrong-namespace but declared token passes (declared-is-declared) ⊕ | r7 | carried | b20/b21/b24 |
| 42 | companion-file / foreign ids are not a declaration surface | r7 | carried | b23 |
| 43 | unscanned cells invisible (e.g. `notes`, extra columns) | r7 | carried | b13/b33, P2 |
| 44 | prose inside a scanned cell can over-extract into a false positive (fail-closed direction) | r7 | carried | P1 |
| 45 | exempt-status rows blanket-exempt (an undeclared id behind an exempt status passes) | r7 | carried | b3/b30; r10 audit covers the records' actual tokens only |
| 46 | `refs=N` counts the extractor's tokens, not every reference a record carries | r7 | by-design (definition) | r7 §counting |

### 3.6 Gate baseline (r8)

| # | limit (as named) | origin | disposition | evidence |
|---|---|---|---|---|
| 47 | exit-code-only regressions invisible to the pin (rc is sanity-checked `∈{0,1}`, never compared) | r8 | carried | r8 §4.1; candidate: record the capture rc in the baseline header |
| 48 | behavior outside the canonical invocation invisible (incl. usage/refusal paths and `AGG_ERE` defaults the capture never exercises) | r8 | by-design | r8 §4.2 |
| 49 | oracle strength: weakened selftest assertions / dropped unasserted fields pass byte-identically (the PASS set is case names + exits, never assertion text) | r8 | carried | r8 §4.3; lesson m1 (weakened assertion) / m3 (dropped field) |
| 50 | a semantic regression inside a stable field is unobservable; the guaranteed converse is: if the unmasked canonical bytes move, the move is named | r8 | by-design | r8 §4.4 |
| 51 | masked fields (`ts`, `gate_sha256`) are declared blind spots; the masked set travels in the artifact and a changed list is itself drift | r8 | by-design | r8 §2, §4.5 |
| 52 | per-row movement outside the pinned composed surface invisible (a claim `at=line:1`→`2` shift passes the pin; solo claims names it) | r8 | by-design | r8 §4.6; r8 lesson span-shift probe |
| 53 | two transient selftest FAILs under 32-seat load (fail-closed, non-reproduced; committed receipt PASS 85) ⊕ | r8 lesson | carried (contextual) | r8 lesson §Limits; committed `evidence/pin-r8-…-selftest.log` |
| 54 | `LANE_ROOT` boundary fallback in scratch copies (environment caveat, not a gate defect) | r8 | by-design (env) | r8 §7 |
| 55 | re-pin discipline: a red drift must be dispositioned (intended → recorded re-pin with reason; else regression); "re-pinning to turn red green" is the named failure mode | r8 | by-design (ritual) | r8 §6 |

### 3.7 Conversion / archive scale (r9–r10)

| # | limit (as named) | origin | disposition | evidence |
|---|---|---|---|---|
| 56 | `A-r9.md:50` row C3 pointer `A:76` vs span occurrence `A:86`; no mode pairs a row's `path:line` with its span's occurrence line | r9 | **finding** (still live at `338918fc…`; 18/19 re-derived here; fix-or-absorb pending, fixtures seat) | r9 §5.1; §2 above; a fixed record moves its sha row and requires re-measuring |
| 57 | in-record claims-table `span` column sits outside every gate check (verbatimness rests on authoring + independent byte checks) | r9 | carried | r9 §5.2; r10 controls do not cover it (the span-not-found control uses the claims surface) |
| 58 | coverage is a selection (~1/5 prose lines under a span check: 27 spans / 23 lines / union 31 of 109) | r9 | by-design | r9 §3; r9 lesson m4 |
| 59 | chain of custody stops at the export | r9 | by-design | r9 §5.5 |
| 60 | exports are cut mid-response (an absent section is not an answer of "no") | r9 | by-design | r9 §5.6 |
| 61 | conversion authors structure the source cannot supply; durable rules (ship the raw-DRIFT control beside conversion-CLEAN; report spans-over-lines; record anchor kinds; selection is the conversion's unchecked act) | r9 | by-design | r9 lesson §applying; archives-r9 README |
| 62 | reframing residual (`text` cells paraphrase; read span+pointer, not prose) | r9 | by-design | r9 lesson m6; archives-r9 README |
| 63 | controls isolate one class per record; multi-defect interaction uncovered | r10 | by-design | controls README §What this set does not cover |
| 64 | refusal classes (out-of-corpus / URL / session) not exercised at archive scale; the small r2/r3 fixtures own them | r10 | by-design | controls README §What this set does not cover |
| 65 | one existence proof per class, not a measured fraction of defect space | r10 | by-design | controls README §What this set does not cover |
| 66 | false-sweep `hits=`/`listed=` are directory-at-runtime values (class and finding id are not) | r10 | by-design | controls README (3 hits measured) |

### 3.8 Standing lane debts (r1-origin)

| # | limit (as named) | origin | disposition | evidence |
|---|---|---|---|---|
| 67 | export-unverified tier; CLEAN = declaration-and-pointer acceptance only | r1 | by-design | `archived-export-intake.md`; r9 |
| 68 | receipt identity open (no authentic queue taskKey / expected receipt bag; rounds 2–10 remain lane-local evidence) | r1 | operator | every note's Open items; SCORECARD debt |
| 69 | non-author admit/reject spot-check absent (discernment unchanged) | r1 | operator | README gaps; `lessons/round-1.md` |
| 70 | scope-refusal finding IDs never landed (documentary province boundary) | r1 | operator | README gaps |
| 71 | frozen-replay conformance (`expected.json` pins inputs; not a rerunnable comparator — the r8 pin covers only the canonical gate invocation) | r1/r2 | operator | r2 open items; README gaps/frontier |

### 3.9 Counts, reconciliation, and the round-11 audit queue

Counts (71 rows): **by-design 38 · carried 25 · closed 3 · finding 1 ·
operator 4**. Closed: 12 (r4), 31 and 37 (in-wave). By design, row 19 now
carries the round-10 audit annotation; nothing was silently reclassified.

Reconciliation: the scribe's enumeration (report draft §Named limits; read
05:44Z) lists, by round, the same limit set this ledger dispositions. Checked
item-by-item: every enumerated class has a row above — r2 → rows 1–11; r3 →
12, 19–25; r4 → 13–18; r5 → 26–31; r6 → 32–37; r7 → 38–46; r8 → 47–55; r9 →
56–62; r10 → 63–66; r1/debts → 67–71. Deliberate deltas: this ledger splits
some grouped classes into separate rows (e.g. r7's eight named limits; r5's
emptiness-vs-rightness) and adds ⊕ rows from the notes/lessons/README (11,
23, 24, 28, 41, 53) plus the r10 rows (63–66), which the enumeration
predates. The scribe's "manifest schema growth" debt maps to row 36 (§3.4);
its "usage/outside-path pin blind spot" maps to row 48.

Round-11 audit queue — the open items this map hands forward: **30 items**
(25 carried: 8, 9, 10, 11, 13, 14, 22, 24, 25, 26, 29, 32, 33, 38–45, 47, 49,
53, 57; 1 finding: 56; 4 operator: 68–71). Suggested order for the capstone
audit, cheapest-first, each with what would move it:

1. **56 (finding)** — fix-or-absorb `A-r9.md:50`; if fixed, the record sha
   row, the archives-r9 README and r9 note pins all move; decide whether the
   pointer/span class (including a `:99999`-style pointer probe, r9 lesson
   m5) ever deserves a gate check.
2. **11, 57** (attribution): decide whether any in-record label/span or
   pointer/line pairing is checkable without semantics; today both are
   authoring-discipline checks with independent byte audits only.
3. **8–10, 13, 14** (carried residuals + boundary residues): in-root
   hardlinks, no source size cap, cosmetic banner; token-aligned shortening;
   non-ASCII adjacency. The shortening/non-ASCII pair needs a fixture before
   any rule change and the r4 note explicitly does not assert a fix is safe;
   the three residuals are mechanical/reporting items.
4. **26, 29** (sweeps): vacuous flip strings; section absence owned by r1.
5. **32, 33** (composition): omission assertions; the rejections-only
   representation seam.
6. **38–45** (integrity fail-open classes): duplicates, non-id shapes,
   case, kind, companion ids, unscanned cells, over-extraction, the
   exempt-status blanket.
7. **22, 24, 25** (documentation/coverage residues): heading-kind coverage;
   the superseded-receipt citation; the `path#quote:text` seam.
8. **47, 49, 53** (baseline): exit-code-only regressions; oracle strength;
   the transient-load FAIL class.
9. **68–71** (operator): receipt identity, spot-check, scope-refusal IDs,
   frozen replay — absorb or carry with the mission contract.

Nothing in the queue is newly created by this note; the queue is the
disposition of what rounds 2–10 already named.

## 4. Holds, receipts, and pins (this seat's runs)

- `bash tools/research-gate.sh --selftest` → `RESEARCH_GATE_SELFTEST: PASS
  (85 cases)`, exit 0 (05:43:03Z).
- `bash tools/research-gate.sh --drift
  corpus/evidence/gate-baseline-r8-20261016T033757Z.json` → `GATE_DRIFT:
  none`, exit 0 (measured behavior matches the r8 baseline; baseline sha
  `1c81a6cb…`).
- Gate sha re-derived `46f5ddb3…` before and after the battery; working-tree
  == HEAD blob; `git diff --numstat tools/research-gate.sh` empty.
- Six control runs (`verify-all`, one per control): each DRIFT exit 1,
  `drift-sections=1 findings=1`, findings as §1 (log:
  `$HOME/.cache/chousa-tmp/r10-note/logs/controls-verify-all.log`, scratch,
  declared ephemeral).
- Records / sources / controls / claims shas re-derived for the pins above;
  control shas were unchanged before and after the battery (measurement-time
  stability).
- The standing round receipts are the receipts-writer's artifacts; at this
  note's write time (05:45Z) no r10 receipt file had landed under
  `corpus/evidence/` — the runs cited here are this note's own and the
  controls README's. The controls README's measured block is an independent
  second execution of §1 and agrees everywhere (modulo `ts=`).

## 5. Open items / what this note does not claim

- **The ledger-record premise, stated plainly.** The dispatch named a
  `limit-ledger` seat; no artifact under that name was observed on disk by
  this seat (searches at 05:44Z: the `corpus/` tree, `.ufo/round-10/`). The
  only on-disk enumeration is the scribe's draft `report-draft.md` §Named
  limits, and §3 reconciles against it. This note's ledger is independently
  re-derived from the nine knowledge notes, the README's Known gaps and the
  lessons; if a separate ledger artifact lands at integration, reconcile it
  against §3 rather than assuming they agree.
- **This note moved after first landing; the round-10 lesson pins the
  interim revision.** The lesson
  (`corpus/lessons/2026-10-16-archive-scale-controls-and-ledger.md`) cites
  this note at sha `f5dc8889…` (68 rows, 27-item queue) and spot-checks rows
  9/16/29/53. That revision was superseded at ~05:47Z because it was missing
  three r2 carried residuals — rows 8–10 here (in-root hardlinks, no source
  size cap, cosmetic banner) — that both the scribe's enumeration and §3.9's
  completeness claim require, and it carried a mislabeled queue entry; the
  revision on disk now is the final one (71 rows; 38/25/3/1/4; 30-item
  queue). The lesson's spot-check rows map 9→12, 16→19, 29→32, 53→56;
  reconcile the lesson against this revision at integration.
- **`A-r9.md:50` fix-or-absorb is pending** (fixtures seat); any fix moves
  `A-r9.md`'s sha and requires re-measuring the records, their README pins
  and §2's row audit.
- **Receipts, SKILL.md rows and the corpus README row** are other seats'
  artifacts (not observed landed at 05:45Z; the round-10 lesson landed
  05:47Z and is addressed by the version bullet above); this note cites only
  this seat's runs, the controls README, the knowledge trail and the scribe
  drafts.
- Not claimed: no scalar score, no admission verdict, no promotion, no
  field-readiness; no gate verdict here; the archives were read, never
  written; nothing was fetched (zero external opens in every run above).
- This note is the round-11 audit's starting map: the controls map (§1), the
  audited exemption set (§2), and the disposition ledger with its 30-item
  queue (§3).
## 6. Errata — append-only (round 12, 2026-10-19)

E1 — four rows dispositioned by round-12 work, none by a gate check where the
row names detection. Superseded cells (quoted, with their §3 line):

- Row 9 (`:204`) "no size cap on source reads … carried … no size cap in the
  gate" → **closed(r12, partial)**: claim/chain source reads are now capped at
  8 MiB (`SOURCE_READ_MAX_BYTES`; `CLAIM_SOURCE_READ_TOO_LARGE` /
  `CHAIN_SOURCE_READ_TOO_LARGE`, refused before any read, at the shared
  `claim_source_path` chokepoint, selftest cases 95–98). The residual the cell
  also names — record reads (`load_sections`, `scan_secrets`) and the
  verify-all claims-surface binding — stay uncapped and are carried here in
  the closure text, not a new row: a claims-surface read over the cap degrades
  to `VERIFY_ALL_CLAIMS_UNRESOLVED` by construction, and record reads are
  bounded by the operator's own corpus.
- Row 10 (`:205`) "banner still reads `research-gate-r1` (cosmetic) …
  `VERSION=research-gate-r1` at `tools/research-gate.sh:227`" → **closed(r12)**:
  `VERSION=v2` (revision token alone; the r1–r11 stutter removed from all six
  banner sites), pinned by selftest cases 93–94 including a drift-mutant arm
  (`GATE_DRIFT: GATE`); the r8 behavioral baseline was re-pinned at the final
  bytes as `corpus/evidence/gate-baseline-r12-20261019T115519Z.json` with the
  reason recorded (see `knowledge/gate-baseline-r12.md`).
- Row 56 (`:281`) "**finding** (still live at `338918fc…`; 18/19 re-derived
  here; fix-or-absorb pending, fixtures seat)" → **closed(r12,
  fixture-correction; no check added)**: A-r9.md line 50 pointer `:76` → `:86`
  (one cell; 7210 B / 73 lines unchanged); record sha `338918fc…` →
  `dfd2ae1a…`; post-fix sweep 19/19, `verify-all` CLEAN at the corrected
  bytes. The class the row's second clause names — no mode pairs a row's
  `path:line` with its span's occurrence line — stays true and remains a
  named non-coverage; the round-11 queue's "decide whether the class ever
  deserves a gate check" is answered "not this round". Closure must not be
  read as detection. The two A-derived controls stay byte-copies of the
  pre-fix base (`controls/README.md` carries the desync note).
- Row 70 (`:300`) "scope-refusal finding IDs never landed … operator" →
  **closed(r12)**: the structure check screens a record's DECLARED scope
  (`## Meta` `domain`/`scope` rows only — both table and `key: value` forms;
  prose never keyword-scanned) and emits `SCOPE_BOUNTY_ABSORBED` /
  `SCOPE_MODEL_QUALITY_ABSORBED` / `SCOPE_ORCHESTRATION_ABSORBED` at warn
  (drift, exit 1), one finding per matched refused province per declaration
  row; selftest cases 86–92 pin the three provinces, both clean grammars,
  the near-miss declared vocabulary, and the prose decoy.

Counts at this revision (71 rows, numbering unchanged): **by-design 38 ·
carried 23 · closed 7 · finding 0 · operator 3**; round-11 queue **30 → 26**
(items 9, 10, 56, 70 out). This supersedes §3.9's "Counts (71 rows):
by-design 38 · carried 25 · closed 3 · finding 1 · operator 4" and its
30-item queue line; §3.9's other reconciliation stands. Revision trail:
`f5dc8889…` (interim) → `3845709b…` (71 / 38·25·3·1·4 / 30) → this revision
(71 / 38·23·7·0·3 / 26).

This file's sha moves off `3845709b…`; sites naming it must cite this
revision or carry a superseded mark: `audit-r11.md` (`:9`, `:307`),
`corpus/README.md:17`, `evidence/README.md:853`, `audit-r11.md:80,152,224`
(D5 lesson reconciliation now maps to this revision). Lessons
`2026-10-16-archive-scale-controls-and-ledger.md` (`:17`, `:165`, `:203`) and
`2026-10-16-verifying-conversion-not-original.md` (`:19`) keep pre-fix pins as
round-dated history and are superseded by this erratum. Gate revision
`91a01695…` (was `46f5ddb3…`).

### Round-13 addendum (2026-10-19, append-only)

E2 — row 8 (`:203`) "in-root hardlinks bypass path canonicalization …
carried … no inode/nlink/`-samefile` logic in the gate" → **closed(r13,
hardlink class)**: the shared `claim_source_path` chokepoint now refuses
multi-linked sources unread (`CLAIM_SOURCE_MULTILINKED` /
`CHAIN_SOURCE_MULTILINKED`, crit, one `stat -c '%s %h'` probe before any
read); live bypass receipts `evidence/alias-r13-20261019T123621Z-bypass-
{before,after}.log`; selftest cases 99–102. Carried INSIDE the closure, not
new rows: TOCTOU (stat-then-read), same-device bind mounts (nlink=1,
stat-invisible mounts), unmeasurable-stat fallback, and legit in-root
multi-link families refusing (`knowledge/hardlink-alias-r13.md` — the r13
claim closes the hardlink class only, per the round-13 reviewers).

Counts at this revision (71 rows, numbering unchanged): **by-design 38 ·
carried 22 · closed 8 · finding 0 · operator 3**; round-11 queue **26 → 25**
(item 8 out). This supersedes the §6 counts line (71 / 38·23·7·0·3 / 26);
the §6 text stands otherwise. Revision trail: `3845709b…` → `46534902…`
(r12 §6) → this revision. Gate `91a01695…` → `${GSHA}…`. Sites naming
`46534902…` (audit-r11 erratum table, corpus/README) carry the r12
revision; update on next touch or cite this addendum.

### Round-14 addendum (2026-10-19, append-only)

E3 — the bind-mount item carried inside E2 closes: **cross-device mount
aliases are now refused unread** at the shared chokepoint
(`CLAIM_SOURCE_CROSS_DEVICE` / `CHAIN_SOURCE_CROSS_DEVICE`, crit; one
`stat -c '%s %h %d'` probe, device compared against the RESOLVING root —
longest-prefix rule, per the live sweeps-r5 S4 lane-fallback case). Live
before/after receipts `evidence/mount-r14-20261019T125621Z-bypass-
{before,after}.log`; selftest cases 103–106 (0 skipped on this host; 105 is
the same-device true-positive control, 106 the lane-fallback control that
defeats a naive ROOT-only compare). Same-device binds stay a named limit
(stat-invisible — only mountinfo path-walking could see them; r15+
candidate).

Counts at this revision (71 rows, numbering unchanged): **by-design 38 ·
carried 21 · closed 9 · finding 0 · operator 3**; round-11 queue **25 →
25** (bind item out; the discovered `--root /` boundary dead-arm — `case
"$canon" in "$root_r"/*` becomes `//*`, every source refuses — enters the
queue; fix `"${root_r%/}"/*` named, not landed: outside the r14 claim).

This supersedes the E2 carried list's bind bullet; E2/E1 stand otherwise.
Revision trail: `46534902…` (r12 §6) → `16f93821…` (r13) → this revision.
Gate `6b17e50c…` → `d8bbd0bf…`. Sites naming `16f93821…` carry the r13
revision; update on next touch or cite this addendum.
(E3 correction, same round: the bypass receipt files are
`evidence/mount-r14-20261019T132025Z-bypass-{before,after}.log` — the
`125621Z` stamp above is a typo; the file names on disk are authoritative.)

### Round-15 addendum (2026-10-19, append-only)

E4 — the `--root /` queue item (entered E3) closes: **absolute paths under
`--root /` are matched again.** Root cause (measured, bash 5.3.15): with
`root_r=/` the prefix pattern renders `//*`, which matches nothing, so every
root-resolved source refused `CLAIM_SOURCE_OUT_OF_CORPUS` crit (demo: a
claim citing `/etc/hostname` — dev 31 = / dev 31, nlink 1, a legitimate
read — refused unread; lane-resolved relative sources were unaffected,
falling to `CLAIM_SOURCE_MISSING` on genuinely absent paths). The fix
normalizes the prefix TEST only, never the stat'ed root: a single
`in_root()` helper (`tools/research-gate.sh` ~:612) strips the trailing
slash before composing the glob — `${r%/}` on `/` yields the empty string,
`""/*` renders `/*`, which matches `/` itself and every descendant. The
materialized helper is mandatory: **inline `case "$canon" in
"${root_r%/}"/*)` is itself dead when the expansion strips to empty**
(measured — a quoted `${var%/}` that expands empty quashes the trailing
unquoted glob). Three same-class sites, all converted: `claim_source_path`
(:1044-1075), `ptr_resolves_meta` (:546-551 — the third site, found by this
round's symmetric audit, not named in the opening), `sweep_path_guarded`
(:1750-1756). `src_root` stays the original root, so the r14 device probe
still stats `/` (the closure cannot weaken CROSS_DEVICE at the / boundary).
Selftest cases 107–110 pin the healed arm (ghost-missing, /etc/hostname
read, tmpfs cross-device, sweeps absolute glob); the CHOUSA_ROOT=/
selftest override rides a new harness channel (six runners gained a
`^CHOUSA_[A-Z_]+=` env-override classifier, tcase's override placement
corrected to last-wins). Receipts
`evidence/root-r15-20261019T152000Z-{demo,selftest,battery,drift}.log`;
gate sha `d8bbd0bf…` → `dd0951d7…`.

Counts at this revision (71 rows, numbering unchanged): **by-design 38 ·
carried 21 · closed 10 · finding 0 · operator 3**; round-11 audit queue
**25 → 24** (the dead-arm named item out). The dead-arm closure is a
queue-item closure, not a row closure — the item occupied no §3 row (same
class as the E3 bind item), so row counts move only on the closed side
(9→10 records the carried-9 row's own closure in this round's commit).
Continuity note: E3's counts line (21/9, queue 25) counted the bind item
as a carried→closed row, but E2 recorded it "carried INSIDE the closure,
not new rows" — it occupies no §3 row; the same phantom would recur if
the dead-arm (also not a row) were counted as one. Row-true counts have
been 38·22·8·0·3 since E2; queue-true was 26 at E3 (25 committed).

This supersedes E3's counts line and its "fix … named, not landed" clause,
and supersedes `knowledge/mount-alias-r14.md:56-58` ("queued" → closed).
E1/E2 stand otherwise. Revision trail: `46534902…` (r12 §6) →
`16f93821…` (r13) → `00bf8418…` (r14 E3) → this revision. Sites naming
`00bf8418…` carry the r14 revision; update on next touch or cite this
addendum.

### Independent closure recheck (2026-10-19; current gate `9f163807…`)

The current selftest passes (122 cases, 0 skipped); relevant cases pass for row
70 (86–92, 112–119), row 10 (93–94), row 9 (95–98), and row 8 (99–102).
The current `--drift` run against the r12 baseline reports `GATE_DRIFT: none`
(exit 0).

- **Row 9:** the 8 MiB claim/chain source-read cap is re-confirmed by the
  inclusive-boundary and over-cap cases. Keep the recorded `closed(r12,
  partial)` status and its record-read / explicit verify-all claims-surface
  residuals unchanged; this recheck tests no broader cap claim.
- **Row 10:** `VERSION=v2` remains, all six banner emitters use it, cases 93–94
  pass, and the current r12-baseline drift check is clean.
- **Row 8:** the claims and chain hardlink-refusal cases and both link-count
  controls pass. This confirms the hardlink class only; the recorded TOCTOU,
  same-device-bind, and unmeasurable-stat limits remain.
- **Row 70:** the three refused-province cases and declaration/prose controls
  pass; later fenced-heading and literal-phrase cases also pass. The screen
  remains declaration-only, not a general prose scope detector.
- **Row 56 — partial independent recheck:** the in-repo A-r9 record is 73 lines
  / 7,210 bytes with SHA-256
  `dfd2ae1a149b7c87f8ff399522f99c3461570c5ba06ba9d6b18254b15a3c3b9d`, matching
  the recorded post-fix hash; its C3 pointer at line 50 is `:86`. The original
  `research/deep-research-2026-09-28/A-shokunin-tradition.md` is absent from
  this repository (repo-wide glob found no copy, and the repo-relative read
  failed). Under `PROVINCE.md` scope, no `--root ..` verification was run.
  Therefore this recheck cannot independently reproduce the 19/19 source-span
  audit or corrected-byte `verify-all CLEAN`; record the fixture correction as
  confirmed, but this independent recheck remains partial. The pointer/span
  detection class remains named non-coverage.

No historical erratum or disposition counts were rewritten. The command
receipts and case-level outcomes are appended to `LOG.md`.

### Round-16 addendum (appended 2026-10-21 at round 25, append-only)

Rounds 16–23 landed gate changes without an addendum here (`lessons/round-24.md`
M-6). Each Round-16 … Round-23 addendum was reconstructed at round 25 from that round's
`SCORECARD.md` verdict, its `LOG.md` entry, its knowledge note and read-only
git (`git show <commit>:tools/research-gate.sh | sha256sum`); the per-round
seat drafts with full citations are
`.ufo/waves/round-25/build/LedgerAddR{16..23}.md`. These addenda do not change the original §3 row dispositions; round 20 did
append the Independent closure recheck above, without a disposition delta.

E5 — (`--root //`): gate `dd0951d7…` → `2b64a1c8…`; case 110
at the round-16 landing (the old sweeps-absolute case shifted to 111).
No §3 row and no round-11 queue item moved; the `mount-alias-r14.md`
"queued" → closed wording restates E4's dead-arm closure, not a new one.

### Round-17 addendum (appended 2026-10-21 at round 25, append-only)

Reconstructed at round 25 (see the Round-16 addendum for method).

E6 — (fenced-heading scope shadow): gate `2b64a1c8…` →
`c2915f24…`; cases 112–116. No §3-row/round-11-queue delta; row 70 stays `closed(r12)`
(E1) — the fix hardens an already-landed screen.

### Round-18 addendum (appended 2026-10-21 at round 25, append-only)

Reconstructed at round 25 (see the Round-16 addendum for method).

E7 — (`SCOPE_KENGAKU` phrase gap): gate `c2915f24…` →
`6e694881…`; cases 117–119. No §3-row/round-11-queue delta.

### Round-19 addendum (appended 2026-10-21 at round 25, append-only)

Reconstructed at round 25 (see the Round-16 addendum for method).

E8 — (sweeps symlink escape): gate `6e694881…` → `9f163807…`;
cases 120–122. No §3 row and no §3.9 queue item moved; the closed item is
round-16 named debt (`knowledge/verification-r16.md`, seat 20 — that row's
"queue for round 17" wording is superseded by this line).

### Round-20 addendum (appended 2026-10-21 at round 25, append-only)

Reconstructed at round 25 (see the Round-16 addendum for method).

E9 — (HTML-comment heading shadow): gate `9f163807…` →
`49b36759…`; case 124. No §3-row/round-11-queue delta; row 70 stays `closed(r12)`. The
round's independent closure recheck (above) rewrote no disposition.

### Round-21 addendum (appended 2026-10-21 at round 25, append-only)

Reconstructed at round 25 (see the Round-16 addendum for method).

E10 — (`ptr_resolves_meta` boundary): gate `49b36759…` →
`bfc291ef…`; cases 125–128. No §3-row/round-11-queue delta; row 56 (pointer/span
pairing) is a different class and stays as E1 left it.

### Round-22 addendum (appended 2026-10-21 at round 25, append-only)

Reconstructed at round 25 (see the Round-16 addendum for method).

E11 — (denylist path-start forms): gate `bfc291ef…` →
`dfb798b4…`; cases 129–132 at landing (renumbered 130–133 by round 23). No
row/queue delta; row 5 stays by-design.

### Round-23 addendum (appended 2026-10-21 at round 25, append-only)

Reconstructed at round 25 (see the Round-16 addendum for method).

E12 — (fenced chain `heading` anchor): gate `dfb798b4…` →
`b5d0f93d…`; case 129. No §3-row/round-11-queue delta; row 22 is not re-dispositioned.

### Round-24 addendum (appended 2026-10-21 at round 25, append-only)

Round 24 (`--json` delimiter, gate `b5d0f93d…` → `752e4e38…`, cases 134–136)
closed round-20 named debt, not a §3 row or queue item.

### Round-25 erratum (2026-10-21, append-only)

1. **Template slot filled.** The Round-13 addendum's gate line shipped an
   unfilled template slot after `91a01695…` (`lessons/round-24.md` M-5). It is
   filled in place with `6b17e50c…` — the gate blob at the round-13 landing
   `5993dc4` (`git show 5993dc4:tools/research-gate.sh | sha256sum`), which the
   Round-14 addendum's `6b17e50c…` → `d8bbd0bf…` already names as its before
   side (seat `.ufo/waves/round-25/build/RevengerGSHA.md`).
2. **The E4 counts line is not row-true.** E4's `38 · 21 · 10 · 0 · 3` sums to
   72 over a 71-row ledger: its `closed 9→10` counts the carried-9 row's
   closure, but row 9 was already closed by E1 and the r20 recheck keeps it
   `closed(r12, partial)`. Counted at this revision (rows 1–71 parsed, closures
   E1 {9, 10, 56, 70} and E2 {8} applied): **by-design 38 · carried 22 ·
   closed 8 · finding 0 · operator 3** (sum 71) — the row-true tuple E4's own
   continuity note gives. Round-11 queue: 24 as committed (30 −4 −1 +0 −1);
   25 queue-true (E4: "queue-true was 26 at E3 (25 committed)"). E5–E12 move
   neither. Re-derive: `python3 corpus/evidence/round25-ledger-recount.py`
   from the lane root → `rows=71 by-design=38 carried=22 closed=8 finding=0
   operator=3 sum=71 queue_committed=24 queue_true=25`. This line is the
   counts owner from round 25 on; E4's line stands as history.

### Round-25 append-only preservation correction (after fresh falsification)

The first round-25 integration substituted the Round-13 template slot in
place, then appended a disclosure. FxCritC3 correctly noted QUALITY4 requires
preserving an erratum's filed bytes, not merely disclosing their alteration.
The original Round-13 line is therefore restored byte-for-byte; the earlier
round-25 “filled in place” instruction is superseded by this paragraph.

R25-GSHA-DISPOSITION: superseded by gate 6b17e50c

That is the proven gate blob at `5993dc4` (re-derive `git show
5993dc4:tools/research-gate.sh | sha256sum`). The historic template token now
remains as superseded data, not an unresolved current hash. The counting
script reports raw historical slots separately from unresolved slots; before
raw=1/unresolved=1, after raw=1/unresolved=0. All pre-round ledger bytes are
preserved; the addenda and corrections are appended. The old literal-token
zero prediction was incompatible with append-only preservation and is
explicitly corrected, not silently redefined as a raw-count pass.
