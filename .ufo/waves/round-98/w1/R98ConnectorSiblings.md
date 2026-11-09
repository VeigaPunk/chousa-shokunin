# R98ConnectorSiblings — cross-lane pattern scan (read-only), round 98

Seat scope: scan sibling lane repos under `/home/vgpnk/Projects/shokunin/*-shokunin` read-only for (a) self-tests
that check their own harness (canaries, known-fail sets) or batteries with equivalent-mutant legs, and (b) knowledge
on PRESS, search peer review, or reading a paper through an index record instead of the publisher. For each match:
path, revision, one-line relevance, and whether chousa's C1/C2 contradicts or duplicates it. Route, do not absorb.

Attacked tree was not needed for this seat: every sibling read is `git -C <repo> show/grep`, no clone, no battery run
against the lane. Scratch `/fast/scratch/hyaku/chousa-r98/R98ConnectorSiblings/` (the two S231 re-fetch bodies) is
deleted before yield. No tool installed; no pacman.

Revisions at scan time: `.ufo/waves/round-98/w1/R98ConnectorSiblings-revisions-and-identity.txt` (21 lanes; e.g.
kagi `39e76bc`, kotoba `0344dda`, kotodama `5fa04a9b`, mado `f77ed5e9`, mori `7765969c`, tameshi `ab60e134`;
chousa F `aac826848dda5029ba459568b29d9a92176dc2b6`).

Prior art in this seat: round-97's scan (`w1/R97ConnectorSiblings-sibling-scan.txt`) swept per-case guard idioms and
externally-written mutant sets, and found no sibling PRESS knowledge. This scan keeps that negative and adds the two
narrower sweeps this seat was given (self-checking harnesses / equivalent-mutant legs; index-record reads).

---

## (a) Self-tests that check their own harness; batteries with equivalent-mutant legs

Marker sweep (receipt `R98ConnectorSiblings-scan-markers.txt`): `hash-of-self`, `hash_of_self`, `guard-blind`,
`always-pass`, `equivalent mutants must survive`, `PRESS 2015`, `27005575` over every sibling at its tip.

| path | revision | relevance | vs chousa C1 |
|---|---|---|---|
| `kotoba-shokunin:verifiers/check_mutation_battery.py` | `0344dda` | Three-leg battery: `kill-set` + `equivalents survived E of E` + `disclosed survivors S of S`, with guards G1 revision identity / G2 copy integrity / G3 registry presence, and `--self-test` whose G1/G2 arms are themselves kill channels | **Duplicates** C1's design (kill leg + equivalent leg + oracles) and **contradicts nothing**; it is *ahead* of C1 on two legs C1 lacks: an asserted *disclosed-survivors* set and a self-test of the battery's own guards |
| `mori-shokunin:corpus/knowledge/equivalent-mutant-adjudication-r84.md` | `7765969c` | Rule: a survivor is exempt only if the edit cannot change observable behaviour, and "the exemption is proven, not asserted" (K3) | **Duplicates** C1's equivalent leg in intent, **contradicts nothing**; C1's battery asserts the three equivalents by edit shape and never witnesses the equivalence (see R3) |
| `mori-shokunin:corpus/knowledge/selftest-flake-r9.md` | `7765969c` | A committed oracle (`mori-silence-cases.sh`) re-run byte-unchanged against a fixed census; determinism gate for a self-test | Neutral precedent for C1's no-write/yield legs |
| `tameshi-shokunin:corpus/knowledge/control-assertion-anchoring.md` | `ab60e134` | The code a control grades must be a *measurement*: observed exit codes taken from the process, not typed into the driver | C1's battery does take them from the process (Held, see §Held); the entry is the citable rule if a reviewer asks |
| `tameshi-shokunin:corpus/knowledge/executor-test-sufficiency.md`, `gates-survey-kumitate.md` | `ab60e134` | Coverage-limit discipline for driver/selftest pairs | Neutral; the "does not cover" wording C1 already carries matches this house pattern |
| `mado-shokunin:quality/counters/c2-r93-selftest-strength.py` | `f77ed5e9` | Counter whose predicate is "does a gate catch a weakened, still-green selftest", with `neutral` edits that must stay OK and oracles (always-OK, always-WEAK, sha-diff) | **Duplicates** C1's oracle family including the hash-of-self analogue (`sha-diff`); C1's ORACLES leg is the smaller set (5) of the same shapes |
| `mado-shokunin:.ufo/waves/round-41/w1/MutC1CounterGates/matrix.md` | `f77ed5e9` | Same battery, twice-run: two kill verdicts flipped on a nonce and did not reproduce ("nonce lottery, not reproduced") | **Contradicts nothing in C1's wording**, but names a hazard no C1 leg excludes (see R1) |
| `kagi-shokunin:corpus/knowledge/claim-instrument-falsifiability.md` | `39e76bc` | "A gate's self-invocation must execute its own aggregation" — the exact rationale of C1's `g00` guard canary | **Duplicates** C1's `_guard_canary` move; different lane, no conflict |
| `kake-shokunin:scripts/citing_set_hostile_selftest.py` | `dd7a146d` | Hostile-shape fixtures built at run time, each refused by the runner | Same known-fail-set shape as C1's ORACLES leg (5 stand-ins), smaller/older |
| `kotodama-shokunin:corpus/knowledge/verification/gate-battery-surface-verification.md` | `5fa04a9b` | Battery-surface verification contract (what a green battery does not license) | Neutral; the wording rule C1 could cite for limit (a) |
| `lore-shokunin:corpus/knowledge/r99-gate-blind-spot-table.md` | `0f044aa` | Per-mutation catch/does-not-catch table, replayed on the revision, with a self-test (`dependency_freeze --self-test` 18/18) | **Duplicates** the blind-spot-table form; C1's two named survivors are the same class of row and are still only prose in C1, not a table |

No sibling carries `hash-of-self` / `guard-blind` as a *lived* term except chousa itself (chousa r97/r98 batteries);
the concepts exist elsewhere under different names (`sha-diff` gate in mado, `sha-diff` analogue in mado's neutral
leg). Nothing in (a) contradicts C1; three items are duplicates of moves C1 makes.

## (b) PRESS, search peer review, index-record reads

| path | revision | relevance | vs chousa C2 |
|---|---|---|---|
| any sibling `corpus/knowledge/*.md`, word `PRESS` | 21 tips | **Negative**: 0 files outside chousa (`R98ConnectorSiblings-chousa-tiers.txt`) — same negative as round-97's scan, re-measured at these tips | **No duplicate, no contradiction**: C2 is the fleet's only PRESS knowledge |
| `kagi-shokunin:corpus/lessons/round-62.md` (+ `w1/R62ScoutSources.md`, `capture/notes.md`) | `39e76bc` | PubMed `pubmed.ncbi.nlm.nih.gov` served a **203 cookie wall** on 5 attempts from this host; the PMC mirror/efetch XML is the working route; the PMC **article HTML embeds a per-request `csrfmiddlewaretoken`** so two fetches of one URL gave two digests, and the pin was moved to the token-free NLM XML | **Corroborates** C2's S229 rejection (independent host observation, 2026-11-07); **duplicates** the "capture must be re-fetchable" rule C2 does not state (see R5) |
| `kagi-shokunin:corpus/knowledge/source-capture-binding.md` | `39e76bc` | A row naming a capture claims bytes: sha256 + byte count + locator quote under the declared normalization; `verified-at` records `refetch byte-identical` | **Duplicates** C2's capture discipline in stricter form; C2's S231 row records capture key/bytes but no refetch identity |
| `kagi-shokunin:corpus/lessons/round-62.md` §Mistakes + `S132` row | `39e76bc` | `EXT_ID:11554662` in Europe PMC resolved to a **different paper** (2001 rhinology case series, not NegEx): an index lookup's identity must be checked, not assumed | **Names the failure mode C2's K5 checks by hand** and that no C2 instrument checks (see R4) |
| `tameshi-shokunin:corpus/SOURCES.md:203-204` (S327, S328) + `.ufo/waves/round-100/w1/specs/R100SC1.md` | `ab60e134` | Europe PMC REST `resultType=core` records graded **tier A**, quotes located in `abstractText` by word count, headers + snapshot committed, independent re-fetch required | **Duplicates** C2's S231 route and tier; the fleet convention is *not* uniform: |
| `kotodama-shokunin:.ufo/waves/round-51/falsify/ReviewCSec13.md` (S118 row) | `5fa04a9b` | The same Europe PMC REST abstract shape graded **`B (abstract)`** | **Contradicts** tameshi/chousa's tier A on that shape (different lane rubrics; see R6) |
| `chousa-shokunin:corpus/SOURCES.md` S120/S123/S229/S231 | F | chousa's own rubric: publisher's own text = A; third-party copy = B; the *same* abstract as PubMed displays it = A | C2's tier A is **internally consistent** with S229; it is not derived in the claim |

No sibling has "search peer review" knowledge other than chousa's own `search-peer-review-dedup-r96.md`; the
nearest sibling material is quotation-accuracy measurement (tameshi S327/S328), which is a *different* topic.

---

## Routed items (each with command, receipt, observed line)

**R1 — C1 has no determinism leg; a sibling battery's kill verdicts flipped on a nonce.** Axis: operability.
`git -C mado-shokunin show HEAD:.ufo/waves/round-41/w1/MutC1CounterGates/matrix.md | grep -n -A6 'Control-suite flakiness'`
→ `40:## Control-suite flakiness found while testing (side finding)` … `43:Two controls have rare nonce-dependent kill
conditions and fired on draws where the counter edit under test **cannot** have caused them`
(`R98ConnectorSiblings-mado-kagi.txt`, rc=0). chousa's predicate is a single line compared once (K1); a second run of
`python3 -B corpus/evidence/round98/selftest-controls-r98.py --root . --work <scratch> --no-regression` with its tally
line diffed against the first would exclude a flip. I inspected the battery for randomness sources
(`grep -n -e random -e token_hex -e shuffle -e uuid -e time …` → matches are only the word "time"/"times" in the
docstring and in `SETUP … applies N times` lines; `R98ConnectorSiblings-c1-nondeterminism.txt`, rc=0) so the
*battery* is deterministic, but the 37 scored mutants are re-applied in fresh processes and the claim's 35/37 is an
exact count.
Route to `R98ExecC1Repro` / `R98ReviewerC1`.

**R2 — C1's battery is not self-scored and has no asserted survivor identity.** Axis: operability.
`R98ConnectorSiblings-c1-legs.txt` (docstring lines 13-35, 205-220, 300-308; rc=0): the docstring says of the two
named survivors "the two named survivors are reported, not required"; `required = sorted(set(external) -
set(NAMED_SURVIVORS))` and `passed = all(x == y and y > 0 for x, y in t.values())` — `EXTERNAL_R97_KILLED` is
printed, not asserted. kotoba's round-91 battery has the missing legs (`disclosed survivors S of S`, G1-G3, and a
`--self-test` whose arms are kill channels; `R98ConnectorSiblings-mori-kotoba.txt`, rc=0). Route: add a
`SURVIVORS == {u01,u05}` leg and score the battery's own guard code, or state in C1's named limits that the battery's
guards are unscored. Route to `R98MutantsC1` / `R98ReviewerC1`.

**R3 — C1's equivalent leg asserts equivalence; it does not witness it.** Axis: calibration. mori r84 §K3:
"An adjudicated equivalent mutant is exempt from the survivor count only while the graded bytes…" and "The
exemption is proven, not asserted" (`R98ConnectorSiblings-mori-kotoba.txt`, rc=0). The battery's `EQUIVALENT` dict
(`R98ConnectorSiblings-c1-legs.txt` lines 75-81) only requires survive + POSITIVE line. **I did the witness for the
one non-trivial edit**: e3 rewrites `lines[-1] == b""` → `not lines[-1]` in `lines_of`, whose only input path is
`data.split(b"\n")` and whose only in-tool caller is `hit()` — a bytes list, where `not b""` ≡ `== b""`
(`R98ConnectorSiblings-c1-survivor-identity.txt`, rc=0). So the three *are* equivalent; the route is that the
battery does not carry this witness, so a reviewer must re-derive it per round. Route to `R98ReviewerC1`.

**R4 — C2 has no record-identity leg; the sibling precedent shows an index lookup returning the wrong paper.**
Axis: depth. The committed capture carries `"pmid":"27005575"` and `"doi":"10.1016/j.jclinepi.2016.01.021"`
(`R98ConnectorSiblings-revisions-and-identity.txt`, rc=0) but no counting command reads them: `gate-records.py` checks
quote-in-capture, `search-rerun.py verify` checks `rev_match`, and `entry-controls-r98.py`'s legs are
POSITIVE/DO_NOTHING/NEW_ONLY/FORGERY/ELEMENTS/WARRANTS/LANE_FILLED. kagi's `S132` row records `EXT_ID:11554662`
resolving to a 2001 rhinology case series (`R98ConnectorSiblings-kagi-capture.txt`, rc=0). K5 is therefore
reviewer-only; a one-line leg (`grep -c '"pmid":"27005575"' <capture>` plus a title/author substring) would make it
instrument-checked. Route to `R98ExecC2Repro` / `R98ReviewerC2`.

**R5 — C2's S231 body is semantically stable but NOT byte-reproducible; a digest-pin recheck would be wrong.**
Axis: depth. Two live GETs of the SOURCES row's URL (2026-11-09, read-only, scratch only) returned `HTTP=200
bytes=7289` each and hashed **identically to each other** (`e8470177…`), but **differently from the committed
capture** (`.raw` = `.txt` = `4111c45a…`). Parsed comparison: every value equal, `abstractText` equal (1835 chars); the
only byte difference is JSON key order inside `journalInfo.journal` (`nlmid` before vs after `isoabbreviation`), first
diff at offset 2910 (`R98ConnectorSiblings-s231-refetch.txt`). Consequence: all quotes still locate (gate-records
reads the capture text), but kagi's `source-capture-binding` rule ("refetch byte-identical") cannot be applied to this
row by sha256; a recheck leg must compare post-parse fields. Route to `R98ReviewerC2` as a named limit, and to the L1
as a wording fix if any future claim says "re-fetch identical".

**R6 — tier A over an index-record abstract is a chousa/tameshi convention, not a fleet one.** Axis: depth.
tameshi `S327`/`S328` (Europe PMC `resultType=core`) are tier A (`R98ConnectorSiblings-tameshi-kotodama.txt`, rc=0);
kotodama's `S118` (Europe PMC REST abstract) is `B (abstract)` (same receipt). chousa's own S229 already grades "the
statement's abstract as PubMed displays it" as tier A and S123 a third-party copy as B
(`R98ConnectorSiblings-chousa-tiers.txt`, rc=0). C2's "tier A for the abstract scope" is therefore consistent with
S229 but undefended in the claim; the reviewer should quote chousa's own rubric (S120: publisher's own text = A)
rather than assert A. Route to `R98ReviewerC2`. Not a falsification.

---

## Held (checked, not fired)

- **C1 survivor identity is enforced, indirectly.** With `|external| = 37`, a printed `EXTERNAL_R97_KILLED=35/37`
  plus `KILL_REQUIRED=35/35` forces exactly two survivors and none of the 35 required; both must be
  `{u01,u05}` because they are the only mutants excluded from `required`. So the sentence "all except the named
  survivors" is true *under K1's line comparison*, though no leg asserts the set. (`R98ConnectorSiblings-c1-survivor-identity.txt`)
- **C1's e3 equivalent is genuinely equivalent** (witness above), not a behaviour change mislabelled.
- **(b) negative is stable**: no sibling `corpus/knowledge` entry carries the word `PRESS` at the 21 tips, matching
  round-97's scan at older revisions (`R98ConnectorSiblings-chousa-tiers.txt`).
- Nothing in (a) or (b) makes a C1/C2 sentence false as stated; the five items above are gaps and limits, routed.

## Tooling

None installed or upgraded; no pacman transaction attempted.

VERDICT: R98ConnectorSiblings C1 held — no sibling contradicts C1 and its battery legs are deterministic and its named survivors are pinned by the printed count, but the battery is not self-scored, has no asserted survivor set, and carries no equivalence witness (R1-R3 routed).
VERDICT: R98ConnectorSiblings C2 held — no sibling contradicts C2 and chousa's PRESS content is fleet-unique, but the S231 capture is byte-order-unstable across refetches, no instrument checks the record's pmid/doi identity, and tier A over an index-record abstract is a chousa/tameshi convention that kotodama's rubric contradicts (R4-R6 routed).
