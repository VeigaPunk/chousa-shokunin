# ReviewFreezeEq — R49 w1 — freeze integrity + predicate↔docstring↔code

seat: ReviewFreezeEq (leaf — no subagents, no background jobs) · 2026-10-25 · lane: chousa-shokunin
scope: freeze evidence for fe740e7838b3…, then the frozen predicate sentence (claims.md) vs each counter's
docstring vs main()'s code conditions. Writes: this report only. Scratch: none created. Installs: none.

## 1. Freeze integrity — commands + observed output

`$ git -C $LANE show --stat fe740e7838b338d17fec9338c909557e6e7fed7d`
```
commit fe740e7838b338d17fec9338c909557e6e7fed7d · Date: Sun Oct 25 11:34:26 2026 -0300
    round-49: freeze claims C1 (assimilate-rows tool) and C2 (derived-index theme adoption) with counters and controls
 build-spans.py 194 · c1-count.py 402 · c2-count.py 241 · claims.md 91 · controls/{c1-before 18,
 c2-before 40, copy-tool 41} · +3 inherited .ufo/waves/round-49/inherited/*.json.diff (261/308/649)
 10 files changed, 2245 insertions(+)
```
`$ git -C $LANE log --oneline -5`
```
6594092 (HEAD, origin/master, origin/HEAD, master) round-49: C1 candidate tools/assimilate-rows.py (section-10 adopter: by-document renumber, census-schema rows, 0-3-space collisions)
fe740e7 round-49: freeze claims C1 (assimilate-rows tool) and C2 (derived-index theme adoption) with counters and controls
414a2ec round-48 verifier spot-check (integrator, hyaku): non-author admit/reject
73ea811 round-48: land lesson, census and falsification evidence
671b096 round-48: repair polarity precision and document limits
```
- `$ git -C $LANE rev-parse HEAD` → `65940928cc9332b386bcbca92571451cc4374cbe` (HEAD is exactly the named tool commit).
- `$ git -C $LANE merge-base --is-ancestor fe740e78… 65940928…` → exit 0 — freeze precedes the tool commit.
- `$ git -C $LANE show --stat --format=oneline 65940928…` → `tools/assimilate-rows.py | 230 +++`, 1 file changed — the tool commit touches ONLY the tool.
- `$ git -C $LANE diff fe740e78 65940928 -- corpus/evidence/round49/` → empty, exit 0 — zero counter/claims/build-spans/controls bytes moved after the freeze.
- `$ git -C $LANE status --porcelain -- corpus/evidence/round49/ tools/` → `?? corpus/evidence/round49/a05-check.py` only: tracked counters/claims/tool clean (worktree == HEAD == freeze bytes); a05-check.py is an untracked scratch checker, not mine, left untouched.

Freeze holds: fe740e7 (direct parent of the tool commit) introduced claims.md, both counters,
build-spans and the controls; nothing under corpus/evidence/round49/ changed after it; BASE_REV
414a2ec sits two commits below the freeze, as claims.md L6 requires.

## 2. Predicate sentence ↔ docstrings (programmatic)

Extracted the paragraph after each `**Frozen predicate` marker (claims.md) and after each
`Predicate R49-Cx, the same sentence as …` line (docstrings); whitespace-normalized compare:
- c1-count.py: claims.md L21-32 vs docstring L5-16 → IDENTICAL (911 normalized chars both)
- c2-count.py: claims.md L51-69 vs docstring L5-23 → IDENTICAL (1439 normalized chars both)
The docstrings' "same sentence" claim is true — no drift between freeze prose and counters.

## 3. C1 — code conditions vs the sentence (c1-count.py)

In main() (L341-402), not in the sentence:
- a. PACKAGE_CHANGED → exit 2 (L350-352; PINS L54-59 sha256-pin 5 package files) — carried by
  claims.md L34-36 prose and docstring L31 exit codes, not by the sentence itself.
- b. NO_CENSUS → exit 2 (L353-355) — docstring L31's exit-2 parenthetical names only "package
  changed, no git"; a missing fleet census script is unnamed (docstring gap).
- c. NO_BASE_REV → exit 2 (L370-372; git archive/ls-tree of BASE_REV fail) — docstring "no git" ✓.
- d. BASE_CENSUS must pass on the untouched BASE_REV mirror, else exit 2 (L386-389) — a harness
  precondition; the sentence binds only the tool's outputs to the census. [task's example]
- e. TOOL=absent → C1=FAIL exit 1 (L357-360) — the before-state; claims.md L37.
- f. run_tool timeout=120 s → rc 124 → leg fails (L182-185) — in neither sentence nor docstring.
In check_set (ok L274-277), stricter than the sentence:
- g. EXTRA=0 (L228): renumber.tsv must list no non-cited staged id — the sentence says
  "renumbering every cited staged id" but never "only those".
- h. SHAPE on every appended row: 11 cells, no `\|`, leading `|` (L240-244) — the sentence ties
  11-cells to the escaped-pipe clause; here it binds all rows (implied by "pass the fleet census").
- i. PIPE leg beyond the sentence's singular "an escaped-pipe staged cell": the fixture row has
  TWO escaped-pipe cells; the leg requires the recheck cell reduced to exactly "90d" (L332) and a
  stripped.tsv row (lane_id,"recheck",stripped) (L323,L333) — the "90d" reduction appears in
  neither sentence nor docstring prose; stripped.tsv is docstring-interface only (L25-27).
Sentence clauses with no code counterpart: none — BY DOCUMENT (by_doc==len(cited) L227; want
built L213-222: held L218-219, append L220-222 with nxt = max base id + 1 L214, ascending staged
order L212/216), one simultaneous substitution (byte-exact vs single TOKEN_RE.sub L229-235),
exactly the cited rows (L236-246: count, shape, ascending lane-id order, URL match),
mined/opened/recheck/used-by (L247-257; held URL check L258-259), 0-3-space collisions (coll_want
L261 = GREP_RE `^ {0,3}` ∩; GUARD L290-307 asserts ["S002"] L305), 11-cell PIPE (L310-338), 3
sets + GUARD + PIPE (SETS L61-65; ok L398). Note: set labels ("B: a collision-chain entry") are
descriptive — check_set asserts coll_got==coll_want but never that B's collision set is non-empty;
the non-empty collision assertion lives only in GUARD.

## 4. C2 — code conditions vs the sentence (c2-count.py)

In main() (L119-241), not in the sentence:
- a. n > 0 (L233) — redundant: nb≥7 ∧ ids_ok==nb already force n≥14; defensive guard against an
  empty/missing spans.tsv. [task's example]
- b. NO_BASE_OR_REGISTER → exit 2 (L130-132): git show BASE_REV:corpus/SOURCES.md failing or the
  register missing — env precondition (docstring L31 "2 usage/env").
- c. ON_BOUND==n (L170, L233): every spans.tsv row must sit on a bound id with the matching
  staged URL — the sentence requires ≥2 rows per bound id but does not forbid extra rows for
  unbound/held ids; code refuses them.
- d. safe_span traversal guard (L112-116): span_file must be relative without ".." — safety
  condition absent from the sentence (violation → span="" → in_span fails).
- e. Register-row filter (L204): only rows with `chousa` in the lane field, a round\d+ tag and an
  S-id incur verdict duty; the sentence says "each absent-defect-register row on a theme URL" —
  code narrows to chousa round rows.
- f. VERDICT_RE vocabulary present|absent-as-written|unverifiable|fabricated (L68) — the sentence
  never enumerates verdict values; the register is the vocabulary source.
- g. blocked (L213-214) counts fabricated/unverifiable only when the register row's theme URL
  belongs to a BOUND document — exactly the sentence's "no bound document whose verdict is…"; a
  bad verdict on a refused theme doc does not block (by design, matches the sentence).
Sentence clause with no code counterpart: "(derived by `build-spans.py`)" — the counter never
invokes the builder or its --check; it re-verifies content instead (form_text L100-109 reproduces
build-spans form_texts byte-semantics: .txt read utf-8 on file-digest match, else .raw decoded
utf-16le on file-digest match — build-spans.py:55-68; slice check ft[o:o+len(span)]==span L181).
Gap: build-spans fixes the span shape at CONTEXT=80 (build-spans.py:44; slice built at :119-120)
and refuses context-free spans (:121-123), but c2 only requires len(span) > len(quote) (L175) — a
hand-written span with ≠80 chars of context passes c2 while build-spans --check would flag it
stale. The 80-char shape is enforced by no frozen counter.
Everything else maps: two entries exist (L232); ≥7 bound, each exactly-one-URL-row + new since
BASE_REV + mined + opened 2026-10-25 + used-by + exact `source: id — url` line (L142-148);
refused = no row ∧ no source line ∧ refused-doc line naming URL (L149-152); tokens ⊆ bound ∪
{S003} (L155, HELD L64); ≥2 rows per bound id (L182); ≤25 words/≤160 chars (L174); quote in
span/entry/lesson (L171-173); slice-at-offset with file digest (L178-181); span longer than quote
(L175); every `char N` of a bound anchor at a located quote offset, ≥1 (L184-188);
inference-ground exit 0 ×2 (L190-198); verdict line per register row (L209-212, L235).

## 5. Residual risk / verification gaps

- Neither counter nor build-spans --check was executed here; PASS/FAIL on the candidate is the executor seats' evidence.
- renumber.tsv's 4th column (url) is parsed but never compared (c1 L225-226) — interface
  documents it (docstring L25), counter ignores it.
- census() collects only `\tE\d\d\t` stdout lines, truncated to 300 chars (c1 L141-145) —
  diagnostics only; exit codes govern every leg.
- held mapping takes the FIRST base row per URL (setdefault, c1 L206-210) — a duplicate-URL
  registry would bind the lowest id; no fixture exercises it.

VERDICT: attacked the R49 freeze — fe740e78 verified ancestor of tool commit 65940928 with a byte-empty diff over corpus/evidence/round49/ and a clean tracked worktree; predicate sentences byte-identical claims.md↔both docstrings; 9 C1 + 7 C2 code-vs-sentence deltas enumerated (all preconditions/strictness; the one sentence-side gap is C2's unenforced build-spans 80-char span shape) — freeze intact, no counter or claims byte moved.
