# Connector: sibling-overlap scan, round 35 v2 wave (read-only)

Seat `chousa-r35-w2-ConnectorOverlap`. Access date 2026-10-23. Read-only everywhere;
no lane, sibling, fleet or jj state was written; no experiments run (report-bytes scan);
no tool installs.

Scope read in full (bytes): all 8 round-34 reports — `chousa`, `kaidoku`, `kake`,
`kotodama`, `kumitate`, `mori`, `tameshi`, `tsukuroi` — and every round-35 report present
at run time: `kake`, `kotodama`, `kumitate`, `mori`, `tsukuroi`
(`ls /home/vgpnk/Projects/shokunin/.ufo/reports/round-35/`). **Absent at run time:
`tameshi` round-35 and `chousa` round-35** (own lane, not yet filed). Also read:
`chousa-shokunin/corpus/evidence/round35/claims.md`, both counters,
`tools/mechanism-witness.py`, `repairs/slen-probe.sh`,
`corpus/knowledge/keyed-engine-output-equivalence-r35.md`,
`corpus/lessons/round-34-verifier-spotcheck.md`, `corpus/lessons/round-35.md`, and
(read-only) `tameshi-shokunin/corpus/knowledge/witness-equivalence-rule.md`.

Pins verified before scoring anything (sha256sum): landed gate
`1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`, base gate
`a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b`,
`c1-count.py` `da207fd7…c715e3`, `c2-count.py` `557fdbf0…907171`,
`mechanism-witness.py` `9f537bfd…15a252b3`.

## Overlap table

C1 = pinned-binary provenance (resolve/verify/pin one grep, override/refusal/echo).
C2 = mechanism witness vs output-equivalent keyed engines. "Import" = a sibling result
chousa should route; "duplicate" = same ground already held; "contradict" = disputes a
claim's premise.

| Lane (report) | Surface (their bytes) | Overlap with C1 / C2 | Relation |
|---|---|---|---|
| tsukuroi r34 (`.ufo/reports/round-34/tsukuroi.md:8`) | Nine tools build child env from a fixed allow-list instead of copying ambient env; C1 not verified (two after-mutants survived, `:29,:48`) | **C1-adjacent, weaker**: they pin the *environment* the tool runs in; chousa pins the *binary* the gate calls. No binary-provenance surface; no C2 overlap | duplicate in kind (containment-by-allowlist), orthogonal object |
| tsukuroi r35 (`.ufo/reports/round-35/tsukuroi.md:13,:33`) | Counter VERSION 1 met **pre-freeze** by `K08FixtureKeyed` (24/24, "role encoded in name length") and an unpaired-regex mutant; VERSION 2 (namespace + live views + base parity + 17-arm should-fail battery) met **again** by `W2TreeKeyed` (forced-FIFO signature + constants), `W2LogKeyed` (first-warning gate), `W2LiveOracle` (live-view-gated cached arms) — all 24/24; C1 honestly stopped "not verified" | **Strongest C2 overlap in the fleet**: independent confirmation that fixture-keyed, signature-keyed, ordering-keyed and live-oracle-keyed engines stay output-equivalent under a *hardened* output counter — exactly chousa's ctl4/ctl6 MEETS class (`w2a2/MutC2Keyed.md:45-47`) and K1/K2. Tsukuroi has **no trace witness**; chousa's `mechanism-witness.py` is the only fleet instrument that separates this class | **import** (see move) + corroboration, no contradiction |
| tameshi r34 (`.ufo/reports/round-34/tameshi.md:17-22,:104-107,:122`) | Set-aware sealed-copy witness rule (amendment 6): accept+vector = behavioral equivalence `a == b`; the frozen set-blind rule was "voidable in both directions" (inert head rename validated as must-kill; lethal ride-along as must-accept; cosmetic clones unsatisfiable); knowledge entry `corpus/knowledge/witness-equivalence-rule.md` citing S097+S101 (equivalent mutants) | **C2 family overlap, different instantiation**: same output-equivalence problem (an output/behavioral verdict cannot pin mechanism/lethality), solved at *authoring time* over mutated copies, not at runtime over engines. `keyed` appears exactly once in the report (`:122`) and names a round-21 input-keyed *monitor*, not an engine class | **import** (see move) + duplicate-in-family |
| kaidoku r34 (`.ufo/reports/round-34/kaidoku.md:9-16`) | Structure-blind control ("selects a template by input size", `:9`) met the frozen counter 12/12 pre-production; honest stop; lesson M34-4 "counter cannot tell structure from shape" (`:16`) | C2 premise only: a shape-keyed shortcut meets an output counter. No witness adopted (their fix: pre-freeze structure-blind replay control). No C1 overlap | duplicate of C2's *premise*; their pre-freeze-control discipline is already chousa's (controls committed pre-data) |
| kake r34 (`:39-42`) + r35 (`:82-85`) | r34: "both declared counters give their full score to a control that does none of the work" (`:39`); committed the fleet's first shortcut detector `criteria/lookup_control_check.py` (`:42`). r35: with the revealed key, an all-false entry meets C2 12/12 (`dc8e1adf`, `:82`) — a **probe-keyed** control; disclosed "the counter cannot prove the provenance" (`:105`) | C2 premise again (keyed control meets counter), plus the committed-detector pattern chousa already exceeds with `c2-count.py` (its stub controls are committed detectors). No C1 overlap | duplicate (weaker instrument) |
| mori r34 (`:27-29`) + r35 (`:17-21`) | r34: skip programs meet the C1 counter (`ef936fb4`), not verified. r35: denial, word-bag and off-topic controls meet P-C1 — content-free prose meets a calibration counter; C1 self-rejected ("its counter credits content-free and denial prose", `:111`) | C2 premise family (shortcut meets counter) on a *calibration* claim — converging evidence that chousa's calibration axis claim needs its own kill controls, which C2 has (stub-pass/stub-fail). No C1 overlap | duplicate of the premise |
| kumitate r34 (`:38,:88`) + r35 (`:43`) | r34: measurement pins — read-only origin pin `964f443`, FROZEN K values, `pin.sources-check`. r35: `MUTATION_KILLS 2/2`; "row-scoped and heading-keyed mutants … now fail at 107/109" — keyed *mutants* killed by deeper hermetic selftest cases, not by a trace witness | C1-adjacent (pin = revision/digest of measured surfaces, receipt-level, no runtime resolution/refusal) and C2-family (equivalent-mutant killing via fixture depth — tameshi's S101 class). No contradiction | duplicate in kind, different mechanism |
| kotodama r34 (`:40-45`) + r35 (`:69`) | Calibration claim pins "28/28 executables resolve at SKILL.md `f9bd07c2…`" (`:41-42`); r35 box-1 evidence "stays current at digest `f9bd07c2…`" (`:69`) | Closest sibling *pin* practice: digest-pinned executables re-verified per round — chousa's R4 runbook row (`claims.md:130-131`) is the same move; C1's runtime pin (override must be absolute, GNU check, exit-2 refusal, echo) has no sibling counterpart | duplicate in kind (documentation pin), weaker than C1 |
| kake/kotodama/kumitate/mori/tsukuroi (all) | Counting commands re-run from reports, e.g. `grep -c '^| S0[0-9]' corpus/SOURCES.md` (kake r35 `:92`, tsukuroi r35 `:39`, kumitate r35 `:50`) | **C1 hazard generalizes outward**: every sibling's row-count receipts resolve bare `grep` through PATH on the host where `/usr/bin/grep` self-reports "pi-uu-grep 0.2.0" vs pacman grep 3.12-2 (chousa r34 `:112-113`). No sibling names this (grep over all r34+r35 reports for `pi-uu-grep|RESEARCH_GATE_GREP|/usr/bin/grep`: zero hits outside chousa's own report) | **import for siblings** (route, do not absorb) |

## The session note's tameshi claim — verdict from report bytes

"The session note says tameshi hit the same keyed class": **refuted as stated, confirmed
in the weaker family sense.**

- Refuted (the keyed-engine class): tameshi's round-34 report contains the string
  `keyed` exactly once — `round-34/tameshi.md:122` "[~] Executable without oral context —
  lane assertion (round-21 input-keyed monitor)" — a cold-read *monitor* keyed on input,
  not an engine that fingerprints a counter fixture to shortcut work. No fixture-keyed,
  location-keyed or live-oracle engine appears; no MEETS-by-shortcut finding; no counter
  was met by a keyed control in tameshi's bytes. Chousa's keyed-engine class
  (`w2a2/MutC2Keyed.md` ctl4/ctl6 37/37; r35 K1/K2) is **not** what tameshi hit.
- Confirmed (the family): tameshi did hit the same *output-equivalence* family and wrote
  it down first: the set-blind witness rule was "voidable in both directions by
  sealed-copy construction" (`tameshi.md:20-22`), fixed by the set-aware rule with
  behavioral-equivalence vectors (`tameshi.md:17-20`;
  `tameshi-shokunin/corpus/knowledge/witness-equivalence-rule.md:17-23`), resting on
  S101 "equivalent mutants … first-class" (`witness-equivalence-rule.md:62-66`). Same
  lesson, different object: tameshi judges authored copies at authoring time; chousa
  judges a runtime engine by trace.

## One bounded move (proposal only — no edit made)

**Import tameshi's third voidability direction into C2's stated limit: the
rename-of-real-mechanism false kill.** Tameshi's voidable rule had three failure
directions; chousa's committed C2 controls cover only two — always-pass ("a witness that
always answers pass separates nothing", `claims.md:101-104`) = tameshi's false-accept,
always-fail ("also fails the landed gate") = false-kill of the *landed* gate. Tameshi's
third direction — a *correct* engine the witness wrongly kills — is uncovered and is
live in chousa's own bytes:

- `tools/mechanism-witness.py:67-68` pins the literal names `tok_span_offsets_chunk`/
  `tok_span_offsets_direct`; `matcher_entry_lines` (`:80-103`) scans the gate text for
  `fn + "()"`; `:251-255` — if not located, `WITNESS=unparseable`, exit 1.
- `corpus/evidence/round35/c2-count.py:185` requires `landed.witness == "pass"`, and the
  kill rule (`claims.md:92-94`) kills C2 on a landed gate whose witness fails. So a
  future gate refactor that merely **renames the matcher functions** (bodies
  byte-identical, mechanism intact, output full) yields `LANDED_WITNESS=unparseable`
  and spuriously kills C2. (Within round 35 this cannot fire: the counter builds K1/K2
  by inserting a branch after `local hay=$1 span=$2` inside `tok_span_offsets()`
  — `c2-count.py:93-112` — so names are preserved; `separated` also demands
  `witness == "fail"` exactly, `:184`, so "unparseable" cannot inflate separation.)
- The claims.md limit (`:106-110`) names trace-aware engines and show-calls but not this
  name-coupling; the knowledge entry (`keyed-engine-output-equivalence-r35.md:54-60`)
  likewise.

Move for r36 (connector cannot land it): add a rename control — rename both matcher
functions in a scratch copy, bodies unchanged — expected `output_full=true,
witness=unparseable`, and record the coupling in the knowledge entry's stated-limit
section (and optionally make the witness resolve matcher entry lines by call-graph
stamp rather than literal name). Calibration axis + (the stated limit becomes complete
in tameshi's three directions); operability and both frozen predicates untouched;
no sibling file edited. Secondary route (report-only): tsukuroi's r35 keyed arms
(signature/ordering/live-oracle keys) extend the knowledge entry's three-subclass
taxonomy (`keyed-engine-output-equivalence-r35.md:18-27`) with two fleet-observed
sub-classes, and the bare-`grep` PATH hazard names every sibling's counting receipts.

## Contradictions and limits

- **No contradiction found**: no sibling disputes C1's pin semantics or C2's premise;
  tsukuroi r35 independently corroborates that keyed engines meet even hardened output
  counters (24/24 ×4 arms) — the exact phenomenon C2's witness exists to separate.
- Round-35 reports are a partial set (5 of 8 lanes; no tameshi/chousa/kaidoku at run
  time) — the r35 rows may grow at closure.
- I read reports, chousa's claim/counter/witness bytes and one tameshi knowledge entry;
  I did not re-run any counter or witness, open sibling wave artifacts beyond quoted
  paths, or verify sibling claims from their own repos — sibling rows are their lanes'
  assertions, quoted with path:line.
