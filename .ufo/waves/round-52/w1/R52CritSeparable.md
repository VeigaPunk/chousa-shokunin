# R52CritSeparable — round-shape critique (frozen claims 37468ead, wave 1)

Seat: R52CritSeparable (critic). No installs needed (tooling directive: none performed; no tool added).
Scratch: `/fast/scratch/hyaku/chousa-r52/R52CritSeparable` (TMPDIR exported; removed at end). Fixture repo
`$D` = git clone (fetch-only) of the lane at 37468ead + base 00f8c7f5, verified
`git -C $D rev-parse --show-toplevel` = `$D`.

## Q1 — Are C1 and C2 causally separable (claims.md asserts it)? VERDICT: yes, verified.

Evidence (freeze export = `git archive 37468ead` into `$D`; counter run from `$D`):

- At the freeze the tool is absent: `ls $D/tools/capture-text.py` → `No such file or directory`
  (`$D/tools/` holds absent-split, argv-witness, assimilate-rows, inference-ground, mechanism-witness,
  parent-lifetime, quarantine-check, quote-reopen, research-gate only).
- Grep of the whole frozen tree for `capture-text` (`grep -rn` over `*.py *.sh *.md`): hits only in
  `c1-count.py` (its `--tool` default, line 248), `claims.md` (prose), `build-spans.py:15` (prose).
  No code path in `c2-count.py` or `build-spans.py` references it.
- `c2-count.py` imports exactly one module: build-spans (`_builder`, lines 88-92). Its docx dependency is
  `build-spans.py` `docx_text`/`raw_form` (lines 75-112) — self-contained (zipfile+ET). Subprocess use in
  c2-count is `git show` base SOURCES, `git grep` base terms, `quote-substance-check.py`,
  `inference-ground.py`; no capture-text.
- Empirical: `python3 $D/corpus/evidence/round52/c2-count.py --root $D` at the freeze runs and exits 1:
  `ENTRIES=0/3 BOUND=0/4 … C2=FAIL` (identical to recorded `controls/c2-before.txt`). The failure is the
  missing staged entries — not the missing tool (the counter never probes it).
- The C2 CAPTURE_BOUND machinery works without the tool: in `$D` (no `tools/capture-text.py`),
  `build-spans.py` `docx_text(NIPH_raw)` = 19682 chars; `raw_form` = 19682 (see Q4). So C2 can pass with
  the span builder's own reader; the tool is not a causal precondition.
- Nuance: claims.md:120-121 admit each claim only on the **landed** commit; "C2 passes at freeze" is not a
  requirement — at freeze it does (by design) fail on absent entries, which is the documented before-state.

## Q2 — Is C1 operability a real artefact or plumbing dressed as a capability? VERDICT: borderline; real post-freeze consumers, none in the frozen counted chain/frozen gate.

- At the freeze: no lane workflow calls it. `grep -n capture-text tools/research-gate.sh` → no hits;
  `build-spans.py` carries its own reader (Q1); the only caller in the frozen tree is `c1-count.py`
  (`--tool` default). So at the freeze, the tool's sole consumer is its own counter — plumbing-shaped.
- Post-freeze (working tree), the wave build consumes it:
  - `gen-w1-spec.py` (FREEZE=37468ead, CAND=804a4537; lines 69, 111) tells the NIPH entry scribe and the
    quarantine executor to run `python3 tools/capture-text.py <raw>` (and `--locate`).
  - `SKILL.md` working tree adds a `capture-text` tool row and a round-52 counters row (lines 134-135);
    this is **uncommitted** (`git status --short -- SKILL.md` → ` M SKILL.md`; `git show HEAD:SKILL.md |
    grep -c capture-text` → 0).
  - `tools/capture-text.py` landed as its own commit 804a4537 ("round-52: C1 candidate …", 115 lines),
    after the freeze, as claims.md:5-6 state.
- Conclusion: not a pure decoy — the round's drafting workflow genuinely uses it to produce the NIPH text
  form (the round-51 refused capture). But the frozen, counted evidence chain (c2-count, build-spans) does
  not depend on it, and the gate registration is still uncommitted at review time.

## Q3 — Does a do-nothing control reach either target? VERDICT: no; all rerun controls reproduce the recorded baselines, none passes.

Ran everything from `$D` (freeze), `TMPDIR` = scratch:

- C1 at freeze, default tool (absent): `LEGS=0/9 C1=FAIL` exit 1 (matches `controls/c1-before.txt`).
- C1 stubs (do-nothing/cheap): `naive-tool.py` → `LEGS=4/9 C1=FAIL` (PARAS, RUNS_ENTITIES, LOCATE,
  REAL); `cache-txt-tool.py` → `LEGS=0/9`; `const-tool.py` → `LEGS=0/9`. None reaches 9/9.
- C2 controls: `python3 corpus/evidence/round52/controls/build-c2-controls.py` → STAGED
  `REF_ID_UNBOUND=31 BOUND=0/4 C2=FAIL` exit 1; TOOLED (assimilate-rows rewrite, append block, no
  quotes/spans/lesson) `BOUND=0/4 C2=FAIL` exit 1. Matches `controls/c2-controls.txt` exactly
  (adopter run exit=0, COLLISIONS=31, CITED=5 APPEND=4 HELD=1).
- Conclusion: the counters are not trivially reachable; do-nothing inputs fail both targets.
- Note: naive-tool passes REAL only by luck on the pinned NIPH (count=1, offset 10319 — the naive reader
  includes Fallback/instrText dupes here) and fails REFUSE on `norel`; consistent with the claims' table.

## Q4 — Is the duplicated docx reader in build-spans.py a maintainability harm? VERDICT: yes — real, and I found a concrete divergence.

- The rule exists in three encodings: `tools/capture-text.py` (working tree, landed), `build-spans.py`
  `docx_text` (lines 75-103), and the `c1-count.py` generators' expected strings. No shared implementation.
- Pinned capture: agree. `capture-text.py NIPH_raw` exit 0, 19682 chars, no U+FFFD, `--locate
  'SRにおける文献検索期間について明記する'` → `LOCATED count=1 offset=8996`. `build-spans.docx_text` on the same
  raw: 19682 chars, and **content-equal** to the tool's output (`len equal: True … content equal: True`).
  The claim's freeze check only compared length (claims.md:17-18) — I verified full equality.
- Divergence found (18-case adversarial battery; c1 generators + hand-built edge packages; compare tool
  stdout/rc vs build-spans `docx_text`):
  - `e2_external_then_internal`: `_rels/.rels` has an External officeDocument relationship then an internal
    one. Tool: skips External (`TargetMode != "External"`, capture-text.py:57), reads internal part →
    `internal text\n`, rc 0. build-spans: picks the **first** relationship ending `/officeDocument`
    regardless of TargetMode, `normpath`+`z.read` fails → `None` → `raw_form` silently falls back to
    UTF-16LE decoding the zip bytes. Divergence observed: tool `rc 0, 14 chars`; spans `rc 2, 0 chars`.
  - Failure-mode split: the tool refuses (`REFUSED`, exit 2); build-spans returns None and degrades to a
    garbage decode (masked in C2 only by the digest check failing closed).
- Practical harm: any future rule change (e.g., TargetMode/External handling, extra elements) must be edited
  in three places with no cross-test except one length check on one file; `build-spans.docx_text` has no
  unit tests of its own; the C1 counter tests only the tool, not the span builder.

## VERDICT
Attacked the round's shape: (1) separability of C1/C2 is real and holds (C2's path never touches the tool;
C2 at freeze fails on absent entries, not on capture-text) — (2) C1 is plumbing-shaped at the freeze (sole
consumer = its own counter) but acquires real workflow consumers post-freeze (gen-w1-spec drafting,
SKILL.md gate rows, uncommitted) — (3) all do-nothing controls rerun clean and fail both targets (C1
0/9-4/9; C2 0/4) — (4) the duplicated docx reader is a genuine maintainability harm, demonstrated by a
concrete divergence on External officeDocument relationships despite exact agreement on the pinned NIPH.
