# RevProvince — round 63, wave w1 — province review of C1 and C2

Scope: is the lane preflight (C1) and the git-revision citation entry (C2) inside chousa's province, or sibling
ground? Read-only. I ran greps and reads only; I did not run `c1-battery.py`, `c2-count.py`, or any gate. No files
were written except this report; no scratch was created.

Frozen claims checked: `corpus/evidence/round63/claims.md` sha256 `6c46b2cc193e1a44187777e6db98aec52278e37cc4f4b027efbe4365d24c70f5`
(matches the wave context).

## Findings

### F1 — C2 (git-revision citation entry): CONTESTED. The revision-name grammar already has owners.

What chousa owns here (in province): the binding rule. The entry's claim that a citation must carry the artifact and
the revision read is chousa's own rule, and chousa already owns the sibling binding family.
- `chousa-shokunin/PROVINCE.md:5-6` — Owns: "citation chaining and hop resolution; claim-vs-source verification".
- `chousa-shokunin/SKILL.md:19` and `:21` — "Follow a citation chain" and "Reuse a finding: cite the artifact + the revision read".
- `chousa-shokunin/SKILL.md:69-70` — checklist item 1, "Every claim carries a resolvable pointer to the artifact and revision read".
- `chousa-shokunin/corpus/knowledge/revision-binding-r31.md:34` — "The digest pins content, not a Git commit or repository
  revision. Different commits with identical source bytes have the same content pin." This is the gap C2 targets. It is chousa's to fill.
- `chousa-shokunin/corpus/knowledge/citation-version-binding-r36.md:2-3` and `citation-version-binding-r37.md:2-3` — chousa's
  own "binding a citation to a prior state" entries (RFC 7089, NDL WARP). A git-revision binding entry sits beside them.

What is sibling ground (the object-name grammar): `grep -rn 'rev-parse\|gitrevisions\|git-rev' <lane>/corpus/knowledge`
is empty at the base (`grep -rl 'rev-parse' chousa-shokunin/corpus/knowledge` exit 1, no output, run this session). Other
lanes already hold the same grammar, with the same sources:
- `kake-shokunin/corpus/knowledge/commit-citation-hygiene.md:1-3` — source S136, gitrevisions: "a leading substring that is
  unique within the repository"; `verified-at: 2026-10-24`; `:14-20` "Resolution semantics": tokens are resolved with
  `git rev-parse -q --verify`, and uniqueness, not length, is the resolvability test. The candidate entry's Q1 (`controls/c2-positive-entry.md`)
  quotes the same sentence from the same page; its Claim 2 restates the uniqueness rule. This is the strongest overlap:
  the same quote, the same rule, and kake's entry is round 47.
- `kumitate-shokunin/corpus/knowledge/pinned-evidence.md:1` — S031 `git-rev-parse --verify`; `:18` "S031 supplies the primitive";
  `:51` a verdict is pinned to a 40-hex revision via `rev-parse --verify`. This is "pinning a source to a git revision", the
  C2 title, held by kumitate.
- `tsukuroi-shokunin/corpus/knowledge/selector-contract-r21.md:1` — S081 gitrevisions, typed and empty-brace peeling
  (`^{<type>}`), the same rule as the candidate's Claim 1 and Q3.
- `tameshi-shokunin/corpus/knowledge/receipt-revision-binding.md:1-3` (round 56) — a receipt is evidence only for the revision it
  names; `tameshi-shokunin/SKILL.md:1063` pins by `git rev-parse --verify --quiet --end-of-options "refs/heads/<branch>^{commit}"`.
- Also, `souji-shokunin/SKILL.md:118` ("detached HEAD is not a citable pin") and `tabi-shokunin/SKILL.md:1905` (`rev-parse --verify refs/heads/master`,
  never bare `HEAD`) are sibling rules about which revision name is citable.

Split. Claim 3 of the candidate (a blob name pins content, not the commit it came from) is chousa's binding semantics.
Claims 1, 2, 4 and 5 (object-name uniqueness, `core.abbrev` default, peeling, `--disambiguate`) describe Git's
behaviour and are already held by kake, kumitate and tsukuroi.

Verdict C2: contested with kake-shokunin (resolution semantics, same S136 sentence), kumitate-shokunin (`rev-parse --verify`
pinning) and tameshi-shokunin (receipt-to-revision binding). The frozen claim is the rule the entry must state, so this is
a limit to route, not a rewrite. Routing options for L1 (decision not mine): keep the entry scoped to the binding rule
and point at kake's entry for the grammar, or record the overlap as a named limit. I have not verified whether kake's
entry is itself in the citation set of the round-63 counter; that is an open check (see gaps).

### F2 — C1 (lane preflight): IN province as this lane's instance. The generic shape is tameshi's method.

In province: the preflight runs chousa's own gates (G01–G08: census, knowledge index, lesson gate, SHONEN pointers,
SCORECARD paths, freeze, assimilate, research-gate selftest). That is "this lane's own corpus and gates", which chousa owns.
- `chousa-shokunin/PROVINCE.md:7-8` — Owns: "...this lane's own corpus and gates."

Shape: the gate runner plus planted-defect battery (`c1-battery.py`) is tameshi's method, and tameshi says so:
- `tameshi-shokunin/PROVINCE.md:5` — honest checks: "hermetic suites, mutation testing, fail-closed arms, verdict-line discipline, before/after proof".
- `tameshi-shokunin/PROVINCE.md:7-12` — Owns the method "documented from the fleet's existing gates", including "six gates with selftest suites + mutation controls" (kumitate `scripts/*`).
- `tameshi-shokunin/PROVINCE.md:14-17` — "a pattern is admitted from evidence in TWO independent lanes before it is claimed general"; never edits a sibling's gate code.
- `tameshi-shokunin/SKILL.md:90` — the "Hermetic suite (`--selftest`)" shape; `tameshi-shokunin/corpus/knowledge/fleet-suite-census.md:1-12` — a census of
  all six gates' suite and mutation-control completeness.
- Precedent: `kengaku-shokunin/PROVINCE.md:342-344` — "tameshi owns the *method* ... kengaku's C1 attributed-kill battery is an
  application of that method to its own `plans/pkg_gate.py`, not a new method." chousa's C1 battery is the same kind of
  application to chousa's own gates.
- Sibling instance of the same runner shape: `kagi-shokunin/PROVINCE.md:50` (`corpus/checklist-run.sh`, runnable rows).

Calibration: the frozen named limit already says "the gate set is chousa's own ... other lanes are not claimed"
(`claims.md`, named limits). That keeps C1 an instance. It becomes a tameshi question only if the wave claims the shape
generally, which the frozen text does not do.

Verdict C1: in (chousa instance). The method is tameshi's (contested as a general shape, not as chousa's tool).

### F3 — boundary of the item question

The item asks whether revision identity is VC tooling belonging to a sibling. Answer: the grammar of git revision names
is sibling ground (F1). Chousa's share is the binding rule (F1, in). The preflight is chousa's instance of tameshi's
method (F2). Net: the item is contested, not out.

## Lines and commands read (this session)

- `corpus/evidence/round63/claims.md` (full, incl. C1 `:26-110`, C2 `:111-153`, frozen instruments `:161-167`), sha256 check
  `sha256sum corpus/evidence/round63/claims.md | cut -c1-64` = `6c46b2cc…c70f5`.
- `kotoba-shokunin/corpus/knowledge/fleet-commit-resolution-round66.md:1-3` (commit refs: a commit reference "does not make a raw commit identifier a persistent or independently resolvable software citation", citing S122); kasegi `repo-git-state.md:1-20`.
- `PROVINCE.md:1-17`; `SKILL.md:19-21, 55-70`; `grep -n Boundaries/Refuses` across siblings' PROVINCE.md.
- `grep -rl 'rev-parse' chousa-shokunin/corpus/knowledge` → no output, exit 1.
- `grep -rl 'rev-parse' */corpus/knowledge` across siblings (listed in F1).
- `corpus/evidence/round63/controls/c2-positive-entry.md`, `candidate-git-rows.txt`, `candidate-git-revision-probe.txt` (full).
- `corpus/evidence/round63/c1-battery.py:1-30` (docstring predicate).
- sibling heads: kake `commit-citation-hygiene.md:1-3, 14-20, 60-66`; kumitate `pinned-evidence.md:1-12, 18, 51`;
  tsukuroi `selector-contract-r21.md:1`; tameshi `receipt-revision-binding.md:1-3`, `fleet-suite-census.md:1-12`,
  `PROVINCE.md:5-20`, `SKILL.md:70-92, 1063`; kengaku `PROVINCE.md:340-345`; kotoba `fleet-commit-resolution-round66.md:1-3`
  (commit refs: "does not make a raw commit identifier a persistent or independently resolvable software citation", S122); kasegi `repo-git-state.md:1-20`.

## Verification gaps (not run)

- Did not run `c1-battery.py`, `c2-count.py`, the controls, or any gate: outside this item.
- Did not check whether kake's `citation_lint.py` gate would catch a commit-citation overlap in the chousa entry.
- Did not read kotoba's SKILL or kasegi's SKILL in full; only the knowledge heads above.
- [INFERENCE] The frozen claim wording "what a git revision name names" intends the grammar, which is why F1 contests it. This
  reading comes from the claim text, not from a stated frozen intent.

VERDICT: PROVINCE=contested contested_with=kake-shokunin,kumitate-shokunin,tameshi-shokunin
