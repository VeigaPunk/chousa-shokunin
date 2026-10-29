# RevProvince — round 62, wave w1 (reviewer, province review)

Scope: is each part of the round-62 work (C1 counter-validity battery; C2 sourced entry on `openat2(2)` path
resolution) inside chousa's province, or does it belong to a sibling? Document review only. I ran no counter,
battery or probe; every fact below is a file read or a read-only grep. Nothing was written except this report.
Scratch `/fast/scratch/hyaku/chousa-r62/RevProvince` was never populated and is removed.

## Findings

**F1 (contested) — the C1 battery's method overlaps tameshi's declared craft; the instance does not.**
- Instance: a counter that tests `tools/build-spans.py`, chousa's own citation-span gate. chousa's PROVINCE
  `Owns:` names "this lane's own corpus and gates" (`chousa-shokunin/PROVINCE.md:6-8`). In province.
- Method: the battery is a reusable forgery/do-nothing battery (null counters, single-defect mutants, salted
  landing copies, forgers that detect the sandbox, stub builders). tameshi's PROVINCE `Owns:` is "the reusable method
  of honest checks: hermetic suites, mutation testing, fail-closed arms, verdict-line discipline, no-permissiveness
  audits, before/after proof" (`tameshi-shokunin/PROVINCE.md:3-5`), and its Refuses clause says "a pattern is admitted
  from evidence in TWO independent lanes before it is claimed general" (`:12-14`).
- The method is not new to the fleet, and tameshi already holds it: the round-40 lesson records "Do-nothing cannot
  pass" (`tameshi-shokunin/corpus/lessons/round-40-verifier-spotcheck.md:93`, control
  `C1_R40_CONTROL_PASS=false`), and round 45 records a "vacuous" counter whose gate accepts forged input
  (`tameshi-shokunin/corpus/lessons/round-45.md:162`, `CritC1Control.md`).
- A second lane has the same failure class in this round: kumitate's round-62 report says it "Falsified the
  inherited R61 C1/C2 counter copies: the C1 zero-seat fabrication reads `DISPATCH61_HELD 4/4`"
  (`kumitate-shokunin/.ufo/reports/round-62/kumitate.md:8`, and the same file line 23 "R61-V2: not repaired").
  Chousa's own round-61 record shows the same class (`chousa-shokunin/.ufo/reports/round-61/chousa.md:19`, forged
  by detection, `CritC1Sniff` 20/20). That is two lanes with forgeable counters, which is the tameshi admission
  condition as a candidate, not as admitted evidence (INFERENCE: whether these count as "independent" is tameshi's call).
- Calibration note: the battery's forgers were written by the lane that wrote the counter. The claims file names
  this as overfit risk (`claims.md`, C1 "Named limits"). Tameshi could not admit the method from chousa's authorship alone.
- **Action:** chousa keeps the instance (`c1v2-battery.py`, `c1v2-count.py`, and its controls). The generic
  battery shape (do-nothing set, null-counter set, mutant set, sandbox rule) is routed to tameshi as a candidate
  for admission. Chousa must not state the battery as a general method. L1 should send the routing to tameshi
  through the fleet channel. This reviewer did not write to tameshi.

**F2 (in) — the C2 sourced entry on `openat2(2)` is chousa's craft.**
- The work is a deep-research entry: registry rows (S138 man page, S139 kernel header, S140 own probe), located
  quotes, claim-vs-quote checks, limits. That is the method chousa owns: "source hierarchy… claim-vs-source
  verification… this lane's own corpus" (`chousa-shokunin/PROVINCE.md:6-8`).
- The subject is kernel API semantics, which no sibling PROVINCE covers. tsukuroi owns "the OS substrate itself:
  package state, systemd, drivers/firmware, boot health" (`tsukuroi-shokunin/PROVINCE.md:6-12`); its surfaces are
  host state (`pacman`, units, journal, driver plane), and it names no syscall or path-resolution surface. The
  match with its "Kernel, driver, device and user-unit state" line (`tsukuroi-shokunin/PROVINCE.md:46`, ADJ-01) is a
  routing row for a symptom, not ownership of kernel API semantics.
- The C2 probe (`controls/candidate-openat2-probe.py`) reads the host's kernel and headers and runs one local
  syscall per flag in a scratch directory. That is a read-only local measurement. It touches no external target, so
  chousa's external-target refusal (`chousa-shokunin/SKILL.md:55-57`) does not apply.
- Adjacency, no contest: a later use of `openat2` to harden agent or seat containment would be kumitate's
  isolation-substrate frontier (`kumitate-shokunin/PROVINCE.md:22`). Chousa's entry stays a source entry; it does
  not prescribe a hardened tool design. `used-by` names only chousa's own builder.

**F3 (in) — the C1 sandbox (`unshare -Ufp`, `RLIMIT_AS`) is a counter-internal device, not an isolation substrate.**
- The battery uses namespaces to keep the builder from seeing the counter. It does not isolate agent seats.
  kumitate's isolation-substrate band (`kumitate-shokunin/PROVINCE.md:22`) is not triggered. I note the
  overlap only so L1 does not later read it as kumitate scope.

**F4 (gap, report-only) — chousa's boundary text does not name its neighbours that matter here.**
- `chousa-shokunin/PROVINCE.md` has no `Adjacent` section. Its only sibling names are kasegi, kengaku, kumitate and
  kagi (`PROVINCE.md:9-15`). `SKILL.md` Boundaries (`SKILL.md:53-63`) names kasegi, kengaku, kumitate and kagi
  too. Neither file names tameshi or tsukuroi, although both sibling PROVINCE files depend on the boundary in F1
  and F2.
- Report only: the L1 integrator decides whether to add a tameshi line to chousa's PROVINCE. This reviewer did not
  edit it. The frozen claims and the `tools/`, `corpus/` and `SKILL.md` paths are not mine to change.

**F5 (coverage of this review) — what was not checked.**
- I did not run `c1v2-battery.py`, `c1v2-count.py`, `c2v2-count.py` or the probe. Province classification does not
  depend on their verdicts. Whether C1 or C2 PASS is a separate question for the counter attackers and the
  verifier.
- I did not check whether tameshi's round-40 and round-45 lessons are admitted entries or only lessons. That
  matters for the F1 routing, and I did not verify it.

## Read and grep commands (all read-only, lane root or fleet root)

- `cat chousa-shokunin/PROVINCE.md`; `grep -n -A40 -i boundaries chousa-shokunin/SKILL.md`; `cat
  chousa-shokunin/corpus/evidence/round62/claims.md`.
- `head -c 2500 */PROVINCE.md` over all 21 sibling `*-shokunin/PROVINCE.md` files (listing in `ls *-shokunin/PROVINCE.md`).
- `sed -n 1,60p corpus/evidence/round62/c1v2-battery.py`; `sed -n 1,40p corpus/evidence/round62/c2v2-count.py`;
  `sed -n 1,50p corpus/evidence/round62/controls/candidate-openat2-probe.py`.
- `grep -rl openat2`/`grep -rn -i openat2 --include=*.md --include=*.py --include=*.sh .` over the fleet: hits in
  kengaku, kaidoku, kasegi and revenger strace audits (consumers of the syscall, not kernel-semantics entries);
  no sibling corpus entry on `openat2` path-resolution semantics.
- `grep -n -i "forg|counter|mutation|no-permissiveness|battery" tameshi-shokunin/PROVINCE.md` and
  `grep -n -i "forg|do-nothing|null" tameshi-shokunin/corpus/lessons/round-45.md
  tameshi-shokunin/corpus/lessons/round-40-verifier-spotcheck.md` (quoted above, lines 93 and 162).
- `grep -n -i "isolation|unshare|sandbox" kumitate-shokunin/PROVINCE.md`; `grep -n -i "kernel|syscall|openat|path resol"
  tsukuroi-shokunin/PROVINCE.md`.
- `sed -n 1,12p kumitate-shokunin/.ufo/reports/round-62/kumitate.md` (the R61 counter falsification line).
- `head -c 600 corpus/evidence/round62/controls/c1v2-before.txt`; `tail -n 4 .../controls/null-counters.txt`;
  `tail -n 3 .../controls/c2v2-controls.txt` (receipts, read only, to confirm the before and control states the
  claims file cites: `c1v2-before` first lines show the landed and positive subjects at `LEGS=20/20 C1=PASS` (the forger lines beyond the first 600 bytes were not read); the
  null counters show `BATTERY=FAIL`; the C2 controls end `C2V2_CONTROLS_UNEXPECTED=0`). I read these receipts as
  text and did not re-run any control.
- Tool installs: none. Pacman untouched. No network.

## Verdict on the question

- C2 (`openat2` entry): in province (chousa's source-research craft; no sibling owns kernel path-resolution
  semantics; tsukuroi's host-state surfaces are not triggered; the probe is a local read-only measurement).
- C1 (counter battery): the instance is in province as chousa's own gate; the reusable forgery-battery method
  is the part that belongs to tameshi. Report the method to tameshi, do not absorb it.
- Nothing is out of province outright. Route the method (F1) to tameshi and note the boundary gap (F4) for L1.

VERDICT: PROVINCE=contested contested_with=tameshi-shokunin
