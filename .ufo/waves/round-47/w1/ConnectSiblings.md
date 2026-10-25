# ConnectSiblings — round 47 wave 1 (connector, sibling-overlap scan)

Seat: `L1Chousa47.ConnectSiblings`, connector, leaf. Item: grep all sibling lane corpora
(`/home/vgpnk/Projects/shokunin/*-shokunin/corpus/`, chousa excluded, 20 lanes) for FEVER, CFEVER,
climate-fever, CorFEVER, PEOPLEPROFILES, `Not Enough Info`, `NOT ENOUGH INFO`, Fleiss, Cohen; judge
theme absorption; bounded data-walk: do the C1 polarity rule or C2 dependence registry duplicate a
sibling mechanism (sibling `tools/`: `polarity`, `negat`, `Gates`). Report only. No fetch, no edits,
no installs. Lane HEAD read: `a15610a59aaeaf43b79ccc650acee4bd4da00341`.

## 1. Theme scan (C3) — verdict: no sibling holds this ground

Command (case-sensitive per term, then `-i` for fever / not enough info / fleiss):
`rg -n -F "<term>" <20 sibling corpus dirs>`. Counts: FEVER 0, CFEVER 0, climate-fever 0,
CorFEVER 0, PEOPLEPROFILES 0, `Not Enough Info` 0, `NOT ENOUGH INFO` 0, Fleiss 0, Cohen 10.
Case-insensitive extras: 3 hits.

| hit | lane path:line | reading |
|---|---|---|
| `35.1 EM / 64.6 Fever` | kengaku `corpus/knowledge/eval-design-digest-3.md:65` | ReAct↔CoT-SC hybrid score (FEVER as a benchmark) in a digest of a wiki ReAct note, `source-status: historical-unavailable` (same file :12-17). A benchmark-score mention used for "composition beats selection", not the support-test theme |
| `not enough information to determine a type` | kasegi `corpus/source-snapshots/round-23/S031.txt:110` | CVE record spec 5.1.7.1; unrelated |
| `fevers` | kotodama `corpus/SOURCES.md:771` (S817) | sweat-bath medicine; unrelated |
| `Cohen d = 0.500 / 0.9636 = 0.519` | kengaku `corpus/evidence/round11-power/power_analysis_r11.md:29` | effect size (Cohen's d), not Cohen's kappa / agreement |
| `Cohen & West` (publisher) | kotodama `knowledge/myth-symbol/ritual-liminality.md:7`, `direction-symbolism.md:9`, `purity-pollution-boundary-systems.md:7`, `culture-material/funerary-material-culture.md:14` | bibliography publisher |
| Jeffrey Jerome Cohen | kotodama `knowledge/myth-symbol/monsters-hybrid-beings.md:180`, `SOURCES.md:385` (S356), `:386` (S357) | monster theory |
| Matthew Isaac Cohen (editor) | kotodama `SOURCES.md:273` (S244) | puppetry volume |
| Lipsitch, Tchetgen Tchetgen, Cohen | mado `SOURCES.md:213` (S211) | negative controls in epidemiology |

Adjacent probe (not ordered; bounded): `fact verification` 0, `support test` 0, `inter-annotator` 0;
`kappa` 17 files, all tokens/URLs (e.g. kengaku `grader_r12_draft.py:3026` token list,
game-dev-3d S031 author `adaikkappan`). One near-concept: kotoba
`corpus/knowledge/scoped-rules-counter-round61.md:67-68` "A2 support-by-text not entailment" —
an arm bound of kotoba's own verifier (`verifiers/check_scoped_rules.py`), not a held account of what a
claim-support test is, how it is applied or how reliable it is.
Judgment: adopting the §10 theme (FEVER-family support test, NEI class, agreement statistics)
absorbs no sibling's held ground. Only residual courtesy: the C3 entry should not phrase its
definition as fleet-wide; kotoba's "support-by-text" arm is a lane-local instrument term.

## 2. C1 polarity rule vs sibling tools — verdict: no duplicate

Commands: `rg -n -i -g '*.py' -g '*.sh' -g '!**/frozen/**' polarity|negat <8 sibling tools dirs>`
(tools dirs exist in kaidoku, kama, kotodama, mado, mori, souji, tameshi, tsukuroi only). Raw
`polarity` hits were mostly kotodama `tools/gates/frozen/**/packet*.yml` linguistic notes
(`coupling_note: "polarity machinery"`), i.e. data, not mechanism. Live-code candidates:
- kotodama `tools/gates/handoff-packet-check.py:322-327`: `_CANON_NEGATED = (not|no|non|never|without|denied)`
  vetoes a fragment as an affirmative canon-standing claim. One-sided fragment filter; no cited span,
  no span-vs-bullet comparison, no stem scope, no counts-key leg.
- kotodama `tools/harness/claims-freshness.py:37-42, 2598-2605`: "polarity" = the declared boolean
  `expect` of a before-check; fixture 8 flips `expect` and asserts the opposite status. Same word,
  different object (check declaration, not text negation).
- tsukuroi `tools/check-locator-clarification.py:162` `NEGATIVE_DOMAIN_UNSWEPT`: absence-claim sweep.
- chousa `tools/inference-ground.py:26-35, 222-224` (rule 5, `NEG_WORDS` 11 words, `NEG_KEY_PARTS`
  4): span-relative negation with 5-letter-stem scope, 3/2-word windows and a counts-key leg.
No sibling holds an Inference-bullet grounding tool (`rg -l 'INF_|Inference bullet'` in sibling tools: 0).

## 3. C2 dependence registry vs sibling tools — verdict: registry auditing is convergent fleet practice; legs D/E are not duplicated

`rg -n 'Gates' <sibling tools, non-frozen>` and `rg -l 'UNREGISTERED|DANGLING|ENTRY_POINTS'`:
- mori `tools/mori-gate-registry.py:1-55` (sha256 `8b82ac99…5832`, last commit `18fd68b0`): reads
  every table whose header is the eight standard cells. It attributes a path only when the entry cell's
  FIRST backticked command invokes it (`entry_names`, :247-251; `entry_target`, :233-237), and it requires
  a real `--selftest` argv branch. Its population is a glob (`tools/*.py|*.sh` plus round count files) with
  no dependence closure.
- kama `tools/gate-registry-check.py:1-40`: any cell of a registry row registers. Its population is round
  counters, and `missing-path:` ≈ DANGLING. No closure.
- souji `tools/souji-coverage-agreement.py:1-12`: DANGLING-MAP-PATH over the corpus README map, not gates.
  souji `tools/souji-evidence-cache.py:217-220` explicitly disclaims transitivity.
- tsukuroi `tools/probe-child-env-allowlist-r36.py:1054`: the closest closure analogue. It follows the
  import graph over `tools/` for an env allowlist, not a registry.
PROTOCOL §Gate standard (`/home/vgpnk/Projects/shokunin/PROTOCOL.md:398-403`) makes each lane's
`SKILL.md` its own registry home, so C2 is lane-local and absorbs nothing. Gap check on chousa's
literal-path leg D (the import-by-name case tsukuroi's closure would catch): of all 92 entry points,
only `corpus/evidence/round30/c1-count.py:57` and `c2-count.py:63` import a local module by name
(`import qr_harness`). `corpus/evidence/round30/qr_harness.py` is already in A–C (`REG abc`), so
the gap has zero effect on this tree [observed]. Leg D adds exactly one path:
`corpus/evidence/round25-meta-oracle.py` (UNREG).

## 4. Cross-instrument reading (evidence for the proposal)

chousa's `## Gates` header (`SKILL.md:78`) is byte-identical to mori's `HEADER`
(`mori-gate-registry.py:462`), so mori's auditor reads chousa's registry as a second instrument.
mori's audit mode has no writes (open-for-write/mkdtemp only inside `selftest()`, :490/:506).
```
$ python3 -B corpus/evidence/round47/c2-count.py --list      # lane root, HEAD a15610a5
ENTRY_POINTS=92 (abc=84 dependence=+1 check_named=+7)  FLOOR=92  GATES_ROWS=36
REGISTERED=67/92  UNREGISTERED=25  DANGLING=0  MISMATCHES=25  C2=FAIL      (exit 1)
$ python3 /tmp/.../dump_eps.py   # same set logic as c2-count main(), imports its functions
67 REG (66 abc, 1 chk) · 25 UNREG (18 abc, 6 chk, 1 dep)
$ python3 -B …/mori-shokunin/tools/mori-gate-registry.py --rev HEAD \
    --repo …/chousa-shokunin --registry SKILL.md --audit <each of the 67 REG paths>
registered=3 unregistered=37 no_selftest=27 duplicate=0 wrong_row=0 tables=1
REGISTRY=unmet                                                               (exit 1)
```
Contradiction, not smoothed: of 67 paths c2-count scores registered, mori attributes 30 to a row
(3 PASS + 27 `no_selftest`). The other 37 sit in non-first positions of bundled entry cells. Example:
`SKILL.md:101` "research-gate round-31 counters" has four `·`-joined commands in one entry cell,
and mori reports `no row names corpus/evidence/round31/c2-count.py`. Cause: the round-46
`names()` (`corpus/evidence/round46/c2-count.py:114-117`) matches a path anywhere in the entry cell,
but PROTOCOL.md:401-402 defines a row as one "entry command" with one "self-test command and
spelling". The 27 `no_selftest` rows are a separate fleet-schema gap (Self-test clause,
PROTOCOL.md:385-389) outside C2's predicate. Whether the self-test cells declare controls
instead was not checked [INFERENCE: possible mori false positive on non-`--selftest` spellings].

## 5. Proposed move (one, bounded)

Axes: calibration (+), operability (0), depth (0).
Move: when wave 1 registers the 25 UNREGISTERED paths, give each path its own Gates row whose entry
cell's first backticked command is `python3 <path>` / `sh <path>`, with an exit code in the verdict
map. Do not append paths to the existing bundled rows. Also record the mori read-only cross-reading
from §4 in the round lesson as an unscored second instrument against C2's declared named limit
("an entry cell can still name a script that is not a gate").
Why it is non-obvious: the frozen c2-count scores both styles identically, so appending 25 paths
into existing `·` cells is the cheapest route to `MISMATCHES=0`. That route would raise the
fleet-schema bundled count from 37 to as many as 62 of 92, a calibration loss no chousa counter
shows. Per-path rows reach the same C2 target and keep the sibling-instrument reading from getting
worse. No predicate, counter, fixture, floor or target changes.
Second-order effects: runtime, none (SKILL.md text only). Contract: C2 legs unchanged, and DANGLING
stays 0 only if each new row names existing paths. Substrate: Gates grows from 36 to up to 61 rows,
and verdict-map prose repeated across rows can drift. Verification: one extra read-only run.

Risks: duplicated verdict-map text (mitigation: a short per-row map naming the counter's own exit
lines); mori's `no_selftest` would also rise for the new rows (expected; outside C2, report it
rather than "fix" it); running a sibling's tool is a lane-side read, not a closure verdict
(PROTOCOL.md:415-418 limits only the integrator).

Verification for the L1 (after the Gate block lands, at the new tip):
1. `python3 corpus/evidence/round47/c2-count.py --list` → `MISMATCHES=0 C2=PASS`, exit 0.
2. `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-gate-registry.py --rev <tip>
   --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --registry SKILL.md --audit <each of the 92>`
   → for the 25 newly registered paths, no `no row names` lines (attributed: PASS or
   `no_selftest`). The legacy bundled count stays 37, not higher.

## Ledger

Installs/updates: none. Network: none. Writes: this file only. Scratch
`/tmp/chousa-r47-ConnectSiblings/` (dump_eps.py, c2.txt, eps.txt, reg.txt, mori.txt) deleted at end.
Digest: chousa `corpus/evidence/round47/c2-count.py` sha256 `36b3934e…36d1`.
