# Round 56 — frozen claims (chousa)

author: chousa L1 (hyaku run 9, agent `ChousaR56`)
date: 2026-10-27
freeze: before any round-56 wave seat exists or scores; the C1 battery (`corpus/evidence/round56/battery/`) and the
C2 entry, rows, spans and lesson are written after this file
base: `e5a3795191601797613eb986b36fa0b1a73fe6a1` (`BASE_REV`; the round-55 tip `53f1ce6b`, the closure spot-check
`98484fb9`, the orchestrator's W1 salvage `f2b15b48` and the late round-55 `w1-results.json` committed under round 55
as `e5a37951`)

No external fetch or network egress: L0 `8d77e6c1` remains open; every source opened this round is an on-disk capture
under the read-only `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`.

Two claims, two distinct axes, causally separable:

- C1's counter runs gates and battery tools on generated documents, four pinned OLE captures and round 54's manifest;
  it never reads the lane's registry, entries, lesson or round-56 spans.
- C2's counter judges the registry, the entry, the lesson and the round-56 manifest against text forms it derives
  itself; it never runs a gate, a battery tool or a probe, so C2 can land without C1 and C1 without C2.

Pre-freeze counter fixes (before any seat existed, found by the L1's own control runs and disclosed here): the first
control pass showed M9 (WIN_NL) as an equivalent mutant — the window filter carries a second newline guard
(`any(ord(c) < 0x20 for c in w)`), so M9 now drops both guards, as `R55MutC1Counter`'s edit did; and the REFUSE leg's
reason on a hook kill is `rc=97` without the stderr (`refused_ok`), so DENIED accepts `AUDIT_FORBIDDEN` or `rc=97` per
leg. Writing the controls also showed the first kill rule (any verdict-vector difference) forgeable: a tool that
alternates its behaviour, or reads its run directory's sequence number, "kills" every mutant. The frozen rule therefore
requires the mutated clause's own failure reason in G's run, random run-directory names, and two G and two mutant runs
in a random order; the JUNK control carries an alternating FLIP forge. That second rule still let FLIP kill M3 (order
`mGmG` at seed 56, one chance in six per seed), so the frozen rule asks one entry to kill at BOTH seeds with three G and
three mutant runs each in a random order (a call-counting forge matches one order in 20 per seed, 1 in 400 for both). The receipts in `controls/` are from the fixed
counter.

The L1 wrote the round-56 gate (`c1-gate.py`: the round-55 counter plus two hook events) and the two probes before
this freeze and ran them once under the round-55 counter (both probes `LEGS=4/4` — the bypasses are real). The L1
also wrote the eight-entry battery in scratch and ran the frozen counter on it once as a feasibility check of the
counter, not a measurement (`CANDIDATE=2/2 KILLED=9/9 DENIED=2/2`, 124 runs, 132 s); the battery is committed after
this freeze as the candidate and measured there. No seat has scored. M9 (WIN_NL) is killed by the landed builder
itself in every receipt (before and all controls), so the claim's movement is the other eight mutants and the two
probes.

Routed items this round meets (round-55 closure, `corpus/lessons/round-55-verifier-spotcheck.md` section 6, and the
orchestrator note): (1) settle round 55's waves — the late `w1-results.json` is committed under round 55 (`e5a37951`);
the ten W1 seats with no report file have their final output in it; the 36 never-dispatched W2 items of
`.ufo/waves/round-55/w2-spec.json` are dispatched unchanged inside this round's wave (their verdicts are on round 55's
landed claims and are integrated as round-55 corrections, never as round-56 measurements); (2) C1 counter hardening —
C1: the nine `R55MutC1Counter` mutants become the frozen mutant set and the two hook gaps `R55CritForgeHook` named
become frozen probes; (3) D3 — every after-measurement below is cited at the revision its receipt header names;
(4) D4 — appended correction to the round-55 lesson's quarantine line (char 1012, not 994); (5) `build-spans`
registry class — the builder is re-registered as a gate whose gate is `c1-gate.py` and whose clause coverage is C1.

## R56-C1 — operability (lowest scored axis, 3/10): clause coverage and hook closure of the build-spans gate

**Frozen predicate (one sentence, = the `c1-count.py` docstring):**

run on gate G (default `corpus/evidence/round56/c1-gate.py`) and battery B
(default `corpus/evidence/round56/battery/`) at seeds 7 and 56 with
`--per-leg 2`, (i) G passes the lane's `tools/build-spans.py` with all four
legs PASS and exit 0 at both seeds (CANDIDATE=2/2); (ii) each of the nine
frozen mutants M1-M9 of G (the nine edits `R55MutC1Counter` applied to the
round-55 counter: NO_SLICE, NO_CHAR, NO_SHA, NO_QUOTE, NO_EXTRA, REF_TSV,
ALLOW_ROOT, NO_ORACLE_SHA, WIN_NL) is KILLED — some single battery entry,
at EACH seed, fails a leg of G with the reason the mutated clause returns
(M8: G's `ENV_CHANGED` oracle line) in its first G run and in three more G
runs, and passes that leg (M8: runs without `ENV_CHANGED`) in three mutant
runs, the six runs in a random order; M9, whose clause returns no reason, is
KILLED when, at some seed, the landed builder's verdict vector (exit code and
each leg's PASS/FAIL) equals its first G vector in three G runs and differs
from it in three mutant runs, in a random order; and
(iii) each of the two
frozen hook probes P1 FORKEXEC (`_posixsubprocess.fork_exec` of /bin/true,
then the landed builder) and P2 DIRFD (chdir into a subdirectory of the run
directory, then a `dir_fd`-relative open of the lane's SKILL.md, then the
landed builder) is DENIED — at both seeds G exits 1 with all four legs FAIL
and every leg reason carrying `AUDIT_FORBIDDEN` or the hook's exit `rc=97` — counted
`CANDIDATE=2/2 KILLED=9/9 DENIED=2/2 C1=PASS`.

Counting command: `python3 corpus/evidence/round56/c1-count.py` (exit 0 = C1=PASS). Target: `CANDIDATE=2/2 KILLED=9/9
DENIED=2/2 C1=PASS`. Kill rule: any of the three counts short of its target at the after-measurement is a miss, reported
as such; the target is never narrowed after data.

Before (do-nothing: the round-55 counter as gate, the round-55 controls as battery): `controls/c1-before.txt`.
Controls (`controls/c1-controls.txt`): HOOKONLY (the round-56 gate, round-55 controls as battery — the hook work without
the battery), JUNK (eight tools that refuse everything, exit 0 writing nothing, or copy the builder — a battery that
skips the violation work), EMPTY (the default invocation at the freeze, no battery). A control meeting the target means
the counter is wrong.

## R56-C2 — depth (sourced): the grey-literature row of the Chinese drug clinical comprehensive evaluation workflow standard, by document

**Frozen predicate (one sentence, = the `c2-count.py` docstring):**

the grey-literature evidence-source row of the Chinese drug clinical
comprehensive evaluation workflow standard enters the lane BY DOCUMENT as the
lane entry `corpus/knowledge/grey-literature-field-china-r42.md`, which
exists; of the four new documents it may rest on (the standard's text served
by ttbz.org.cn, the standard's explanatory note served by ttbz.org.cn, the
journal-hosted copy of the workflow guideline on journal.china-pharmacy.com,
the national health commission's 2020 management guideline on nhc.gov.cn) at
least three are BOUND — exactly one lane Registry row whose FIRST source-cell
URL is the document's URL, that row new since BASE_REV, `mined`, opened
2026-10-27, its `used-by` naming exactly the existing entries citing it (at
least one), and every citing entry carrying a `source: <that id> — <url>`
line — the standard's ttbz text among them, and every other one is REFUSED
(no lane row, no `source:` line naming its URL in the entry, and a
`refused-doc` line naming its URL in the round-56 lesson); the lane's issued
quality-control guideline capture is cited, if at all, only as
`source: S118 — <its url>` with S118's `used-by` naming the entry; no `S###`
token appears in the entry except a bound id or S118 so cited; at BASE_REV no
`corpus/knowledge` file held `中国循证医学中心`, and the entry holds it;
`corpus/evidence/round56/spans.tsv` carries at least three quote rows per
bound id, each quote at most 25 whitespace words and 160 characters, inside
its span file, inside the entry and inside the round-56 lesson, each span
file the exact slice, at the recorded offset, of the document's DEFINED text
form whose file digest is the recorded one — for a capture whose `.raw` is an
OLE compound file or a zip, the stdout of `tools/capture-text.py` as committed
at BASE_REV run on the `.raw`, otherwise the `.txt` capture read with
universal newlines — and longer than its quote; the round-51
`quote-substance-check.py` exits 0 on the manifest; every `char N` in a bound
row's `anchor` cell (at least one) is the offset of a quote of that id in that
form; the entry exits 0 under `tools/inference-ground.py` with this manifest;
and the lesson carries a re-check verdict line for each absent-defect-register
row on a theme URL (the sweep prints how many: 0 at the freeze), with no bound
document whose verdict is `fabricated` or `unverifiable`.

Counting command: `python3 corpus/evidence/round56/c2-count.py` (exit 0 = C2=PASS). Kill rule: `C2=FAIL` at the
after-measurement is a miss. Before: `controls/c2-before.txt` (`BOUND=0/4 … C2=FAIL`). Controls
(`controls/c2-controls.txt`, built by `controls/build-c2-controls.py`): STAGED (the package entry and its staged rows
copied unchanged: `REF_ID_UNBOUND=3 BOUND=0/4 C2=FAIL`), REWRITE (the mechanical renumber by document: `BOUND=3/4
QUOTE_ROWS=0 GUIDELINE_BOUND=no C2=FAIL`).

Assimilation (§10): theme = the 灰色文献 evidence-source row of 药品临床综合评价工作流程指南 (staged
`grey-literature-field-china-r42.md`, admitted candidate; staged `grey-literature-national-route-r44.md`, the same
theme on an overlapping document set — refusal candidate, merged by document into the r42 entry if admitted at all).
Renumber by document: S168 (the standard's ttbz text) → S127, S156 = S169 (the explanatory note) → S128, S155 (the
journal-hosted copy) → S129, S157 (NHC 2020 management guideline) → S130. The lane's held S118 (the issued 2024
quality-control guideline) answers both staged entries' `#### Unknown` and may be cited as held.

## Round shape (planned)

One v2 wave (policy v2, 64–128): the 36 round-55 W2 items unchanged plus the round-56 build and attack items; the L1
holds the planner seat.
