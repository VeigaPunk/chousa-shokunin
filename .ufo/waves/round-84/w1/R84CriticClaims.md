# R84CriticClaims — adversarial critique of frozen claims C1/C2

Scope: claims.md at 3b616420b2dcc1f8a24a1cb9db4198c7adc8929b (freeze) vs
03bbb4580b39b442be69f998fae2db48d64b8c93 (landing). All runs below are in
`/fast/scratch/hyaku/chousa-r84/R84CriticClaims/` (deleted before yield) with
receipts copied to `.ufo/waves/round-84/w1/R84CriticClaims/`.

Commands that bind every finding are given with receipt path and exit code.

## 0. Baseline: both counters pass at landing (replicated)

- `python3 -B corpus/evidence/round84/gate-records-r84.py --root $TREE --repo <lane> --work $W` →
  `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=288/288 EXPECTED_CODE=288/288 EMPTY_REFUSED=1/1 RC=4/4 SETUP=unscored`, `GATE_RECORDS_R84=PASS`, rc 0.
  Receipt: `R84CriticClaims/c2-landing.txt` rc=0.
- `python3 -B corpus/evidence/round84/depth-r84.py --root $TREE` →
  `ENTRY search-transparency-reporting-r84.md ok=yes rows=11 quotes=12/12 fails=-`,
  `DEPTH_R84 entries=1 ok_entries=1 rows=11 located_quotes=12 fresh_sources=3`, `DEPTH_R84=PASS`, rc 0.
  Receipt: `R84CriticClaims/c1-landing.txt` rc=0.
- Pre-repair tool `81b81173` re-run against the same counter →
  `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=288/288 EXPECTED_CODE=262/288 EMPTY_REFUSED=1/1 RC=4/4`, rc 1, 26 WRONG_CODE
  (all in the ASCII-digit classes). Receipt: `R84CriticClaims/c2-prerepair.txt` rc=1. This confirms the
  do-nothing control discriminates on exactly the repaired defect — the battery measures what the
  repair changed.

## 1. Controls adequacy

### 1a. C1 — cheapest controls that could game the battery (all run, all FAIL — battery is NOT gameable by these)

| control | construction | counter line (rc=1) | receipt |
|---|---|---|---|
| C1a "Zyzzyva + registry-only" | reject line if it contains `Zyzzyva` with QUOTE_ABSENT; else OK iff S-id in registry; filename `f\d{3}.md` pattern → FAIL PARSE. No capture/refetch/rev/word validation | `POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=42/288 EXPECTED_CODE=36/288 RC=3/4` | `R84CriticClaims/c1a-zyzzyva.txt` rc=1 |
| C1b "regex shape" | PARSE on non-ASCII digit + word-count agreement (WORDS) + QUOTE_LEN bound; no registry/capture/refetch/rev/tier lookup | `POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=106/288 EXPECTED_CODE=106/288 RC=3/4` | `R84CriticClaims/c1b-regex.txt` rc=1 |

C1b is the stronger cheat (pure syntactic shape, no committed-byte lookup at all): it clears every
positive and fresh positive (POSITIVE 15/15, FRESH 5/5, EMPTY 1/1, RC 3/4) but accepts 182 of 288
forgeries — every lookup-class forgery (M01 unknown-id REGISTRY, M02 tier TIER, M03–M07 capture/
refetch, M08/M14 quote presence QUOTE_ABSENT, M11–M13, M16 dup-key, M17 id-swap, R01–R06 rev/line,
U01–U04). So the counter correctly refuses it. The two controls that key on counter internals
(filename pattern `f\d{3}.md`, the literal `Zyzzyva`) cannot pass: they collapse on fresh positives
or on expected-code matching. **The claim text still verifies after these cheap controls fail**: the
battery's discriminating power comes from committed-byte lookup, not from secret tokens.

The committed whitelist control corroborates this from the other direction: the stub that accepts the
15 frozen lines byte-for-byte scores `POSITIVE=15/15 FRESH_POSITIVE=2/5 FORGED_REFUSED=288/288
EXPECTED_CODE=66/288 RC=3/4` (FAIL, rc 1) — it dies on the fresh-positives leg, as designed, not on
the forgeries. The 5 fresh positives built in-counter from committed captures/registry/refetch are the
anti-whitelist load-bearing piece.

### 1b. C2 — cheap controls that PASS (as declared, and correctly so)

Receipts committed by the lane (replicated in outline):

- `c1-b1-salad-boundary` (B1): entry `ctl-entry-r84.md` with the same located quotes as the real
  entry but decision rows of the form `unrelated action words N / unrelated prohibition words N`
  → `ENTRY ctl-entry-r84.md ok=yes rows=8 quotes=8/8 fails=-`, `DEPTH_R84 entries=2 ok_entries=2
  rows=19 located_quotes=20 fresh_sources=3`, `DEPTH_R84=PASS`, rc 0.
  Receipt: `corpus/evidence/round84/controls/receipts/c1-b1-salad-boundary.txt`.
- `c1-d3-r82-entry-relanded`: re-landed old entry → FAIL (`ok=no fails=E3,E4,E6,E7`, rc 1).
  Receipt: `corpus/evidence/round84/controls/receipts/c1-d3-r82-entry-relanded.txt`.
- `c1-d1-r81-filler`: round-81 filler pair → FAIL (`fails=E1,E6,E7`), rc 1.
  Receipt: `corpus/evidence/round84/controls/receipts/c1-d1-r81-filler.txt`.

B1 PASS is the **declared** counter limit: the counter checks located, fresh, distinct quotes tied by
Q-id/S-id to rows (E1–E7), not whether a row follows from its quote. Kill rule K3 (warrant) is what
catches content-free rows, and only a non-author reviewer can fire it. **The claim text still
verifies after B1 passes** — claims.md states this limit in the Controls section (line 98–99) and
the entry does not pretend the counter judges entailment. The judgment is: the counter is not
*sufficient* for "teaches search-transparency reporting", but the claim never asserts sufficiency.

## 2. Claim–predicate alignment

### 2a. C1 — a real K2 fires at landing: the setup leg

claims.md K2 (frozen) explicitly includes the setup leg:

> "The setup leg (non-git `--repo` exit 2 vs `FAIL REV,LINE` exit 1) counts as K2 if the tool
> misreports it."

Run at landing (public CLI, exactly as the claims describe):

```
python3 -B tools/gate-records.py verify --root $TREE --repo $D/rev.md
# $D is a scratch directory with no git history; record is a rev-form line
```

Observed: `GATE_RECORD ... S199 FAIL LINE,REV`, `GATE_RECORDS files=1 records=1 ok=0 fail=1`,
**rc=1**. No `GATE_RECORDS_ERROR` on stderr. Receipt: `R84CriticClaims/setup-leg.txt` rc=1,
0 occurrences of GATE_RECORDS_ERROR.

Cause: `git_blob()` in `tools/gate-records.py` (lines 176–189) catches every git failure — including
"not a git repository" — and returns `None`; the caller then emits `FAIL REV,LINE` with exit 1. The
tool therefore cannot distinguish "rev not in repo" (a forgery) from "--repo is not a repo at all"
(a usage/I/O error, exit 2). By the frozen kill rule, this is **K2 in-class, fired at the landing
revision**. The counter prints `SETUP=unscored` and defers this leg to the executor seat; the
counter's PASS does not cover it. The C1 claim sentence ("passes a successor battery … through the
public CLI only", counting the setup leg among its classes) is therefore **not met as written**:
one of its four legs misreports at landing. This is not a coverage complaint — it is a measured
in-class forgery misreported by the tool's own documented contract (docstring: exit 2 on usage/I/O
error, and "missing registry or refetch log" is the only GATE_RECORDS_ERROR path).

Smallest safe correction: in `git_blob()`, distinguish a non-git `--repo` (e.g. probe
`git -C repo rev-parse --git-dir` once; on failure emit `GATE_RECORDS_ERROR` + exit 2) from a
missing commit/blob in a valid repo (FAIL REV,LINE). Narrow, no predicate change. But note the
freeze discipline below: the claims as frozen at 3b61642 already name this leg, so the repair would
be post-freeze and cannot rescue the scored C1 under the frozen kill rules ("Repairs after scoring
do not rescue").

### 2b. C1 — predicate measures the claim sentence, with one coverage gap

The counter's output contract mirrors claims.md exactly: positives byte-equal + OK and tool exit 0;
fresh positives OK; every forgery refused with its EXPECTED_CODE and tool exit 1; empty file exit 1.
The docstring checks (PARSE/REGISTRY/TIER/CAPTURE_PATH/CAPTURE_KEY/CAPTURE_SHA/REFETCH/WORDS/
QUOTE_LEN/QUOTE_ABSENT/REV/LINE) all have at least one mutation class. **Coverage gap**: no mutation
exercises (i) a capture path that is a symlink (docstring: CAPTURE_PATH covers "regular (non-symlink)
file"), (ii) a duplicate `quote=` key (M16 duplicates `tier=`, not `quote=`), or (iii) quote text
with leading/trailing Cf (invisible) characters (docstring's lead_strip concept). A tool that
accepts symlink captures or double-quote keys would pass the counter while violating the docstring —
K2 in-class forms the battery does not instantiate. Severity: low (the found setup-leg K2 is the
load-bearing gap); but the battery is not exhaustive over its own docstring.

A second, lesser alignment note: the fresh-rev leg reads `git grep` on the **live repo HEAD**, not a
blob at the landing rev. It works here because HEAD == landing content for corpus/lessons, but the
builder's own comment ("records already committed in lessons at HEAD") shows the "committed at the
landing rev" property is borrowed from the repo state, not the archive under test. If a future
round's HEAD drifted past the archive, FRESH_POSITIVE could fail for reasons unrelated to the tool.

### 2c. C2 — the counter does not measure "teaches search-transparency reporting"

The target predicate is structural: `entries=1 ok_entries=1`, `rows≥7`, `located_quotes≥8`,
`fresh_sources=1`. The landed entry has rows=11, located_quotes=12, fresh_sources=3 — comfortably
above. What it measures: (i) a Decision table with ≥5 rows and a Warrant column (E1), (ii) warrant
cells naming declared quote ids + S-ids (E2), (iii) every quote 8–25 words and whitespace-collapsed
present in its **fresh, mined, round-start** capture (E3), (iv) pairwise-distinct quotes absent from
all base entries (E4), (v) each non-Warrant cell ≥3 words and non-placeholder (E5), (vi) every
source:-id fresh and warrant-named (E6), (vii) no source:-id or its URL in any base-list entry (E7).

It does **not** measure: whether the Do/Never cell follows from its cited quote (explicitly the
declared B1 boundary, claims.md lines 98–99: "the counter does not judge whether a row follows from
its quote; kill rule K3 does"); whether the entry's `recheck` value is sensible (the entry states
`recheck: on-release` and the counter never reads `recheck`); whether S018's quotes are actually
about *search* reporting (Q8 — "the field is fragmented due to inconsistent terminology…" — is
quoted to support a row about comparing approaches with "use a shared taxonomy and unified
benchmarks", which the quote does not state; that is exactly the kind of row K3's clause (a) is
written for: "Do or Never states something its cited quotes do not state or entail"). As a critic
I flag Q8/Q10/Q11/Q12 rows as the weakest warrant links (DCMI's generic date/description
definitions stretched into search-reporting practice), but under the frozen rules that judgment
belongs to the non-author K3 reviewer, not to this counter — and "teaches search-transparency
reporting" is therefore **half-measured by the counter, half deferred to K3**. The claim text is
honest about this division; the predicate is not a stand-alone measure of the title activity.

## 3. Thinness

### 3a. C1 — is the capability new, or redundant with existing lane tools?

- The lessons' own "Location command" practice (round-80/81/82, e.g. `git show <rev>:<path>` +
  char-offset proof + `wc -w` word counts, recorded by hand in the Gate sections) did check
  quote-in-blob, line identity and word counts, but as **hand-run prose**, not a mechanical
  per-record verifier a counter can re-run. gate-records.py mechanizes that: per-record codes,
  normalization, registry/tier/capture/refetch joins, rev→blob→line lookup.
- `tools/quote-reopen.py` verifies a `id source_id quote` TSV against the **live page** named by
  the registry (network re-open). gate-records.py verifies GATE-RECORD lines against **committed
  bytes only** (registry + captures + refetch.tsv + git objects) and never fetches. Different
  evidence bases: quote-reopen proves the quote is still on the live page; gate-records proves the
  record is internally consistent with the committed capture/refetch/rev. Complementary, not
  redundant.
- Overlapping checks: WORDS (vs `wc -w` by hand) and QUOTE_LEN and quote-location overlap with
  pair `build-spans.py --check` / span-holding checks used by older entries; the genuinely new
  surface is the **join** — S-id → registry row → capture key → capture sha → refetch row →
  rev blob → single line, all in one pass, with per-record machine-readable codes. The r83 repair
  (ASCII digit classes, rev-quote `"` boundary) also fixed a real defect the hand practice had
  masked (Unicode `\d` admitting `line=2٢٢` as 222).
- Net: not redundant. It is a thin-but-real mechanization of an existing hand procedure, plus
  registry/refetch joins no existing lane tool did per-record.

### 3b. C2 — is it new ground?

- `search-log-method-r39.md` (S078): the search **log** as a working document (register steps,
  recall against included references). About keeping a log, not about what a **report** must state.
- `search-tracking-record-r40.md` (S117): PRISMA/PRISMA-S **per-source counts routed to flow-diagram
  columns** (Column 1 vs Column 2, supplementary detail). About where counts go in the diagram.
- `citation-searching-tarcis-r81.md` (S203/S204, round 81): **citation searching** terminology,
  when to run it, what to report (backward/forward/indirect; co-citing/co-cited). The closest
  neighbour — but about finding evidence by following citations, not about reporting which
  databases/platforms/strategies/dates a search used.
- The r84 entry's PRISMA 2020 checklist rows (Q1–Q5: databases/registers/websites searched, dates,
  full strategies with filters/limits, selection methods, identification-to-inclusion path) are the
  checklist itself, not any of the three above. S018 (evidence-linking/traceability survey) and
  S023 (DCMI provenance/date terms) are orthogonal ground. NOR: K4 holds by counter.
- Judgment: new ground on the **checklist-reporting axis** (the lane had log-keeping, diagram
  routing, and citation-search reporting, but no entry stating the PRISMA search-reporting items).
  The DCMI rows are the thinnest warrant (generic metadata definitions applied to "search records"),
  but novelty itself is genuine.

## 4. Freeze discipline

Facts (all measured with `git log` / `git show` / `diff -r` between the two archive trees):

- Freeze commit `3b616420` (2026-11-07 23:11:05 -0300) → landing commit `03bbb458` (23:29:04 -0300),
  via `3a17f4da` (23:22:58, "fetch S214/S018/S023, land entry, fix controls"), `9a2fbc3e`, `d047cd8d`,
  `e98e2a6b`, `f0cebde0`.
- **claims.md changed AFTER the freeze, in `3a17f4da` (11 min after the freeze commit).** Pinned
  landing sha `19d68274…` matches the landing text; the freeze-commit text hashes to `f6f032a6…`
  (different). Textual deltas:
  - C1 fresh positives: "six" → "five"; predicate `FRESH_POSITIVE=6/6` → `5/5`;
    `RC=3/3` → `RC=4/4`; K3 "six fresh positives" → "five"; controls k0 description
    "tool absent → FAIL" → "pre-repair tool 81b81173 → FAIL, EXPECTED_CODE 262/288".
  - C2 grounding: "S017 re-opened" → "S214, S018, S023 opened this round (S017 fetched but
    reverted because its landing page carries no quotable checklist text)"; B1 control
    "located quotes from S017" → "from S214"; K4 "cites S017" → "cites S214, S018, or S023";
    frontier-step source list and SOURCES.md curation line rewritten the same way.
- **Both counters are byte-identical between freeze and landing** (`diff` clean for
  `gate-records-r84.py` and `depth-r84.py`; sha256 matches `instrument-pins.txt` at landing:
  gate `3777249c…`, depth `0b9caf79…`, claims `19d68274…`). The counters already implemented the
  "five fresh positives" game at freeze time — the claims prose was the stale artifact, not the
  instrument. The pins file itself (`instrument-pins.txt`) was committed only at the landing
  commit `03bbb458`, i.e. after the claims text moved, so the pin authenticates the post-move text.
- Egress discipline holds: `egress-approval.md` is in the freeze commit; the S018/S023/S214 refetch
  rows carry `fetched_utc` 2026-11-08T02:15:05Z / 02:16:27Z / 02:21:13Z — after the egress table,
  before the landing commit.
- **Assignment-sheet drift**: the brief states "current tip == landing (no post-scoring changes)".
  HEAD is `142913a9` ("round-84: wave w1 dispatched", 23:31:12 -0300), not `03bbb458`. The two
  intervening commits (`f099c415` wave spec, `142913a9` wave dispatch) touch only
  `.ufo/waves/round-84/{build_spec.py,w1-dispatch.json,w1-spec.json,w1.ready,…}` — no
  corpus/knowledge, tools, counters or claims bytes — so the scoring surface is unchanged. But the
  "tip == landing" statement in the assignment is **false as measured**; it is true in substance
  (no scoring-byte change), false in the letter.

Judgment: **no predicate or counter byte changed after scoring** (counters byte-identical; the
tool at landing is the post-r83-repair bytes `6e7a76f8…` from `c7d29e1c`). What moved after the
freeze was the **claims prose around a fixed instrument** (six→five fresh, S017→S214/S018/S023,
RC 3→4): the freeze commit's claims text was the one that was stale, and the prose was corrected
to match the counter that was already frozen. That is a freeze-hygiene defect — a "frozen" claims
file that was edited 11 minutes after its freeze commit — but it does not move the instrument
toward the candidate; if anything the prose moved toward the already-frozen counter. The circularity
risk (claims and counters versions) is real but bounded: anyone re-deriving the predicate from the
freeze commit's prose alone would get 6 fresh positives / S017, which the frozen counter does not
implement. Smallest safe correction: anchor the claim to the pin (claims.md sha at pin time), or
re-freeze the corrected prose in a superseding freeze commit — never silently extend the original
freeze.

## 5. Smallest safe corrections (no edits made; for Main)

1. C1 setup leg (measured K2): in `git_blob()` probe `git -C repo rev-parse --git-dir` once;
   on non-repo, emit `GATE_RECORDS_ERROR` + exit 2 instead of `FAIL REV,LINE` + exit 1.
2. C1 coverage gaps: add mutations for (i) symlink capture path, (ii) duplicated `quote=` key,
   (iii) Cf characters in the quote/line. One mutation each; frozen `EXPECTED_CODE` set unchanged.
3. Freeze hygiene: superseding freeze commit carrying the corrected claims prose + pins; note the
   S017→S214/S018/S023 re-grounding in the commit message (the S017 revert reason is already in
   the prose and is honest).
4. C2: no counter change recommended. K3 reviewer should adjudicate the Q8 row (fragmentation quote →
   shared-taxonomy Do) and the DCMI rows (Q9–Q12: generic "related resource derived from" →
   "record what a resource derives from") first; those are the weakest warrant links.

TOOLING: no installs (operator tooling directive noted; pacman guard respected; only `git`/`python3`).
Cheats built by hand in scratch; no network. Scratch
`/fast/scratch/hyaku/chousa-r84/R84CriticClaims/` deleted after copying receipts here.

VERDICT: R84CriticClaims C1 fired — setup leg misreports (FAIL LINE,REV rc 1 with no GATE_RECORDS_ERROR where frozen K2 requires exit 2) so the claim is not met as written at the landing revision.
VERDICT: R84CriticClaims C2 held — counter passes as pinned and B1 salad PASS is the declared boundary, with warrant judgment (Q8, DCMI rows) deferred to the non-author K3 reviewer under the frozen rules.
