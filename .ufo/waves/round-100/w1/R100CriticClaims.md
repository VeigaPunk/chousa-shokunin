# R100CriticClaims — adversarial review of C1/C2 at F 6d4e8487 (falsification seat)

Every finding names exact command, receipt path, observed line, exit code.
Receipts in `.ufo/waves/round-100/w1/` (seat-prefixed): `R100CriticClaims-c1-battery.txt`,
`R100CriticClaims-c2-controls.txt`, `R100CriticClaims-probe-c1.py`,
`R100CriticClaims-probe-c2.py`, `R100CriticClaims-probe-c2b.py`,
`R100CriticClaims-standin-build.py`, `R100CriticClaims-standin-head-tree.py`,
`R100CriticClaims-verify-claims.py`, `R100CriticClaims-run-outputs.txt`, `R100CriticClaims-form-probes.txt`.
Attack tree: `$S/repo` = shared clone @ 6d4e8487ee6a16823c24a8e085c6559b92b9fec8
(S=/fast/scratch/hyaku/chousa-r100/R100CriticClaims), batteries run against $S/repo, never the live lane.
All counting commands re-run at F by me and reproduce the frozen lines (see run-outputs.txt):
C1 `NEG=7/7 … ORACLES_REJECTED=12/12`, `CHALLENGE_CONTROLS_R100=PASS` exit 0;
C2 `QUOTES=16/16 … FORGERY_REFUSED=13/13 ACCEPTED=2/2`, `ENTRY_CONTROLS_R100=PASS` exit 0;
gate-new `records=17 ok=17 fail=0` exit 0; metadata `METADATA_COMPLETE=1/1 RESEARCH_GATE: CLEAN` exit 0;
rerun `rev_match=3/3 SEARCH_RERUN: CLEAN` exit 0; gate-old `records=25 ok=25 fail=0` exit 0;
r99 controls `ENTRY_CONTROLS_R99=PASS` exit 0. The frozen tallies are honest as *executed*.
The question is what they enforce. That is where the findings live.

## C1 — operability (tools/gate-records.py + challenge-controls-r100.py)

### F-1 (claim-enforcing hole): the battery cannot see capture sets read at the wrong rev.
Claims.md C1 sentence: "a rev record whose blob … has the object id of a capture … of **that rev's** tree"
(kill rule likewise: "whose blob has a capture's object id **at that rev**"). Instrument leg:
`rev_capture_text` calls `capture_oids(repo, rev)` — correct in the shipped tool (my fixture probes
v1/v2 confirm: same path `corpus/captures/aaaa…txt` at rev A (challenge bytes) → `FAIL CHALLENGE`;
at rev B (non-challenge bytes) → `OK`; receipt `R100CriticClaims-probe-c1.py` output: `[v1-A-challenge] rc=1 …
FAIL CHALLENGE`, `[v2-B-nonchallenge] rc=0 … OK`, both exit as shown, dirty working tree ignored [v7]).
**But** the frozen battery's fixture repo has exactly ONE commit (frev), and its PROD legs read the lane's
BASE rev (oïd-stable across BASE→F lanes), so a tool that resolves the object id at the record's rev but
builds its capture set at **HEAD** passes every leg. I built that stand-in (one-line change:
`capture_oids(repo, "HEAD")` in `rev_capture_text`) and ran the frozen battery against it (`--no-oracles`):
`NEG=7/7 MARK=11/11 BOUND=3/3 NORM=2/2 POS=4/4 REV=11/11 REVPOS=3/3 PROD=6/6 HARM_SAME=27/27
BASE_REV_ADMITTED=8/11 ORACLES_REJECTED=0/0 CHALLENGE_CONTROLS_R100=PASS` (exit of battery 0; cost ~4 s).
The stand-in **violates the claim's central clause** (it judges a rev record against a different rev's tree)
yet prints the frozen PASS line verbatim. Divergence demo (receipt `R100CriticClaims-probe-c1.py`, fixture fx-c1):
record `rev=B path=notes/blob.txt` (bytes = k2.txt's blob **at B**): frozen tool → `FAIL CHALLENGE`
(`[v3-bytecopy] rc=1 … FAIL CHALLENGE`); HEAD-tree stand-in → `OK` (oid absent from HEAD's capture set,
verified by probe: oid `59b80c31…` in `capture_oids(B)` = True, in `capture_oids(HEAD=E)` = False).
The battery's single-commit fixture is blind to the exact leg the claim names ("that rev's tree"). This is
the same class as round-99 F-1: a kill-rule case exists (a wave artifact with a rev record whose blob has a
capture's oid at that rev but not at HEAD, printed OK by the stand-in) that no battery case distinguishes.
**Smallest safe correction:** give the battery's fixture repo two commits whose capture sets differ for the
same path (as my fx-c1 does), and add a rev leg judged across them (A-challenge must refuse; B-clean must
admit; a byte-copy at a non-capture path must refuse at B but admit at E). Cost: one fixture commit + 3 legs.

### F-2 (oracle gap, non-blocking): universal-rev stand-in is rejected, but only just, and by the wrong leg.
A tool refusing **every** rev record whose blob is a ≤200-word marked page regardless of capture identity
(the seat spec's suggested counterexample) scores `REV=9/11 REVPOS=2/3 PROD=5/6 … FAIL` under the frozen
battery (observed run, fail lines `CASE REV r5 rc=0 verdict=OK FAIL`, `CASE REV r6 …`, `CASE REVPOS q3
rc=1 verdict=CHALLENGE FAIL`, `CASE PROD rev-raw-S230 rc=0 … FAIL`). So this specific cheat is caught —
but only via `.raw`-sibling legs (r5/r6/prod-rev-raw) and the NOTE decoy (q3), i.e. incidentally, not via a
designed "non-capture challenge blob must be admitted" leg. Note claims.md says "A rev record whose blob is
**not a capture of that rev is not judged by CHALLENGE**" — the **only** legs exercising that clause are
q1/q2 (S233 article, not challenge at all) and q3 (NOTE: "reCAPTCHA widget" mention, not a challenge page;
a universal-rev thrives on it failing for the wrong reason — see above). There is **no** battery leg whose
blob is (a) challenge-shaped, (b) ≤200 words, (c) not any capture's blob at that rev, and (d) must be admitted.
A slightly different universal variant (refuse iff blob is_challenge, but only when the record's path is
*not* under `corpus/captures/`) passes the byte-copy legs r7/r8 by construction and differs from the claim
on exactly the untested quadrant. Correction: add one fixture leg — challenge-shaped non-capture blob at a
non-capture path, verdict must be OK. One leg kills the whole family.

### F-3 (named-limit honesty check): the remaining C1 clauses held under my probes.
Sibling preference (v5: raw-clean/sibling-challenge → OK [sibling wins]… wait — v5 printed `OK` not
`CHALLENGE`; see below); raw-without-sibling judged by own bytes [v4] → `FAIL CHALLENGE`; byte-copy at
another path [v3] → `FAIL CHALLENGE`; working-tree trap [v7] → `OK` (identity from GITDIR tree, limit (c)
holds); short rev → `REV` code (guard, not identity). One observation for the integrator: v5
(raw blob **clean**, sibling .txt **challenge**) prints `OK` — the tool judges the raw record by the clean
sibling… no: `capture_oids` maps oid→path with ".txt wins", and the record's path *is* the .raw path;
`rev_capture_text` resolves oid→`.raw` name, then substitutes sibling `.txt` bytes (challenge) → should be
CHALLENGE, but observed OK. Root cause: at D, k2.txt still held **CH2**… my probe committed k2.raw clean
*without* changing k2.txt (still CH2 challenge), so sibling=challenge → tool printed OK — meaning
sibling substitution produced the challenge text but verdict OK? Actually `is_challenge(CH2)`? CH2
("Security check in progress. Please stand by while we are checking your browser.") carries marker
"checking your browser" and is 12 words → CHALLENGE expected. Observed OK. This suggests the .txt-wins
oid map returned the **txt** name for the *clean* oid… no, clean-raw oid ≠ sibling oid. The tube: oid of
D:k2.raw (clean) → map (built at D) → name k2.raw → blob=self(clean) is_challenge=False → OK, i.e. the
sibling branch didn't fire because `git_blob(repo, rev, name[:-4]+".txt")` … k2.txt exists at D — unless
`name` resolved to k2.txt via the txt-wins rule (clean-raw oid collides? no). I treat this as a real
behaviour worth re-probing rather than claiming: the claimed sibling rule (limit (d)/o3) is exercised by
battery r5/r6 (which pass), and my v5 construction may have a subtle defect (k2.txt content at D). It does
not overturn the battery PASS; logged as unresolved probe noise, not a finding against the tool.
Hmm — but the seat spec asked me to run cheap stand-ins; v5 OK-vs- CHALLENGE ambiguity is exactly the
kind of thing that must not be papered over. The battery's own r5/r6 (raw path, sibling challenge) both
refuse correctly (observed in frozen battery), so the sibling leg works for the cases that matter; my v5
fixture's k2.txt at D was CH2 (challenge) yet verdict OK — I cannot explain it from the code (sibling
substitution should fire). Smallest safe correction: the L1 should add the v5 case (raw clean + sibling
challenge) to the fixture and confirm verdict CHALLENGE; if it prints OK, that's a live bug in
`rev_capture_text` masked by the battery never covering it. Worth one leg either way.

### C1 verdict
Tool matches its sentence on every leg I could run; the **battery** enforces less than the sentence:
F-1 (HEAD-tree stand-in prints PASS while violating "that rev's tree" — provably wrong verdict on my v3
record) and F-2 (no admitted-challenge-shaped-non-capture leg). Wording "has the object id of a … entry of
that rev's tree" is true of the tool, not of the counter. Kill rule says "any wave artifact shows a rev
record … which this tool prints OK" — for the *shipped* tool that holds (my probes: no such artifact).
So the claim stands; the evidence chain it cites (battery PASS) would also pass for a wrong tool. Verdict:
**fired** (wording/number: the predicate's evidentiary value is overstated — ORACLES_REJECTED=12/12 does not
cover the HEAD-tree mutant, which meets the entire frozen tally without the claimed property). Severity:
moderate — fix is cheap (one extra fixture commit + 4 legs) and should land before the axis score moves.

## C2 — freshness (quotation-error-update-r100.md + r99 ## Update)

### Antecedent check
`quotation-error-rates-r99.md` header still reads `recheck: on-release` (line 5, unchanged) and its new
`## Update` (lines 117-125) names the entry and S238 and flags the 2015 reading superseded — the freshness
flag mechanism works as claimed (FRESH=1/1). New entry also carries `recheck: on-release` (line 5 of new
file) — same tripwire class, fine. S237/S239 rejection: egress-approval shows only S237–S239 rows; S237
(PMC4627914) is a *round-99* source id (r99 entry line 153 GATE-RECORD S235 — note the id drift: r99 entry
cites S235 for PMC4627914, r100 claims.json sources list only S238; S237 was used for a different PMC id
by the plan's route table. I attempted to read egress-approval.md to confirm the S237 three-GET-500s; the
grep returned nothing for S237, i.e. the approval table does not itself attest the 500s — the receipts do
(before/ had c2-base exit 2). Minor: claims.md says "S237 … answered http 500 to three lane GETs each"
but S237's refetch row lives in the committed refetch.tsv — I did not independently re-verify the count of
GETs (network off-limits beyond named-URL re-opens, and S237's URL is a fullTextXML route now known-500).
Not counted as a finding against the claim; the claim's operative content (S238 admitted, S239 500) is
visible in the new entry's GATE-RECORDs (S239 unreach record present, line 119).

### F-4 (kill-rule hole, scope-checked): sign/form of C2 numerals — claims are safe, the instrument's reach is limited.
Claims.md C2 kill rule forbids "a number whose sign or form differs from its warrant" and its named limit (b)
discloses: "The controls check numerals as tokens; spelled-out quantities … and a paraphrase's sense are not
checked." Two evaluations, carefully separated because the brief required them:

*Decisions-row role/negation probes (probe-c2.py output, receipt `R100CriticClaims-probe-c2.py`):* a slope-row
Do rewritten as "significant improvement … (slope: -0.002 [95% CI: -0.03 to 0.02], p = 0.85)" passes
`score()` fully (`passes = True`, NUMBERS 24/24); a role-swapped row 2 ("earlier review included 46 studies
… total 16.9% … update identified 28 studies") passes fully (`NUMBERS (24, 24)`, `passes: True`).
These are **Do-cell inversions of the sources** that no frozen counter refuses. They are, however, inside
named limit (b): sense is not checked, and the *sentence* only claims numeral-token-ness, which holds.
So they do not falsify the C2 sentence; they show the kill rule's overreach clause is human-judged, not
instrumented — as disclosed. Recorded as an enforced-disclosure finding, not a wording falsehood.

*Form probe — pinned mechanism (receipt `R100CriticClaims-probe-c2b.py` plus form probes above):* the phrase
`major 11,9% as printed` occurs **twice** in the new entry: line 11 (What-this-entry-governs) and line 57
(decision row 2, warrants J1,J2,U4,U7). Mutating the **first** (line 11, narrative) to `11.9%` leaves
`score()` passing (NUMBERS 24/24) because the narrative occurrence is in neither a Do nor a Never cell — the
instrument never looks at it. Mutating the **second** (line 57, inside the Do cell) to `11.9%` **fails**:
`NUMBERS after mutating SECOND occurrence: (23, 24) passes: False`. The numeral-form clause **is** enforced
in decision cells, exactly by raw-token equality (`11.9%` ≠ `11,9%`). The sign clause is enforced the same
way (forgery f11: `-0.002`→`0.002` refused). So the kill rule's form/sign branch is real; my earlier
"form mutation passes" was first-occurrence noise. The true uncovered cases are (a) numerals in **narrative
prose** outside decision cells (F-6's lying Update is the extreme instance) and (b) sense/role (limit (b)).
Both are disclosed in spirit; (b) is named explicitly, (a) is the one-line fix in F-6 below.
Duplicate text already integrated above; see F-4b.


### F-5: NEVER leg is vacuous in this entry and over-couples; the "what is checked" story has a gap.
Observed: all 8 current Never cells are exactly `(none stated by the sources)` → NEVER=8/8 trivially; the
sentence's "every Do/Never numeral is a token of that row's own warrant quotes" is vacuous for Never cells
in the frozen entry (24 numerals, all Do cells in rows 1–4; rows 5–8 carry none — receipt probe-c2.py
row listing). Worse, the NEVER leg passes **iff** the Never cell is NONE_STATED **or** contains ≥1 numeral:
my probe P-C2-2 (Never = "never report the slope as flat", numeral-free, not NONE_STATED) fails with
`NUMBERS=(24,24)` unchanged — i.e. a *correct* prohibition without numerals is **refused** by the controls
unless it carries a numeral. That's a wrong-way gate: it incentivises Never cells to contain numerals that
may not belong to the row (each such numeral must then be a warrant token — another reason finding 1's
mechanism matters). The kill rule's "number whose sign or form differs" therefore has no Never-cell
instrument at all beyond token presence. Correction: express the Never leg as "empty of operative numeral
OR numeral-token-in-warrant" (current) **plus** a human-judged limit line; or drop the Never numeral
coupling and let NONE_STATED be the only machine-checked state. Either is a 2-line change + 1 forgery leg.

### F-6: FRESH leg names-but-doesn't-verify.
The lying-##-Update probe (names entry + S238, states `26.9%`, `major 18.0%`, "significant improvement")
passes `score()` fully (FRESH=1/1). So "so the stale 2015 reading is flagged where it is held" is enforced
only as *presence* of the two strings, never as truth of the flag's content. The kill rule ("any wave
artifact shows … a number whose sign or form differs from its warrant") doesn't clearly cover the Update
prose (it's not a decision row). Cheapest do-nothing control (pre-link: FRESH=0/1) shows presence matters,
but a flag that lies is invisible. Correction: extend the FRESH leg to assert the Update contains one of
`## Update`'s promised pointers *and* one checkable correct numeral (`16.9%` or `46 studies`) — 2 lines.
Note this is the same token-presence disease as F-4 at one remove.

### Overreach audit of the current entry (independent read)
I read all 8 rows against their warrants. The slope row (U9 → "no significant improvement … slope -0.002
… p=0.85") and the impact-factor row ("record the association only as printed") are faithful to the
abstract's truncation points (U10 ends "was:", the row records only the printed rho — honest). Row 2's
"the gap between them is not a measured trend" is a lane caution placed in the **Do** cell; it is an
inference, not a quote entailment — but it is marked as the lane's discipline, and limit (c) covers it.
Row 5 "about half of incorrect quotations were classed major" is numeral-free paraphrase of U7 — inside
limit (b). I found **no** live overreach in the frozen entry beyond these disclosed inferences. C2's danger
is entirely in the *unenforced* kill-rule wording (F-4/F-6), not in the shipped text.

### Axis question — is C2 freshness or depth/coverage?
AXES.md: freshness = "Drift detection — skill claims re-verified against live surfaces; stale items flagged
or fixed". C2 is precisely this: a scheduled recheck (`recheck: on-release`) fired on a new release (the
authors' 2025 update) and the stale claim was flagged at source with a pointer to the new reading. The axis
_assignment is right_, and better than a plain "new sources" move would be — the flag's presence in the old
entry is the durable artifact. What F-6 shows is that the freshness *evidence* (FRESH leg) verifies presence,
not correctness; the axis would still be freshness even if the flag lied, which is why the correction above
matters more than re-axis-ing. No axis change recommended. Separately: C2 was "sourced on S238 opened this
round" — verified (`corpus/captures/b5eec205612ee5f138cf065d.txt` present at F, sha matches GATE-RECORDs).

### Do-nothing control cost
C2's pre-link control (entry present, old entry without ## Update) is the cheapest control that skips the
work (FRESH=0/1, exit 1) — correct and minimal; a cheaper control (old entry untouched AND new entry
absent) is just the base case, already shown by c2-base.txt (exit 2). C1's `--no-oracles` base run is the
cheapest C1 do-nothing (base tool under the same battery). Both are the right controls, not profligate.
The *new-entry-present-but-Update-lying* case (F-6) is not covered by either — that is the gap, not a
missing cheap control.

## Battery/tool nits that are not findings
- `HARM_SAME=27/27`, `BASE_REV_ADMITTED=8/11` reproduce exactly; HARM includes C2's entry (no rev record —
  separability note correct). The `BASE_REV_ADMITTED=8/11` number (base tool admits 8 of 11 refuses) is
  consistent with `before/c1-base.txt REV=3/11`.
- C1 battery runtime ~25 s as stated; mine ~22.7 s (candidate) / ~3.9 s (single run no-oracle reuse
  excluded). Fine.
- Receipt hygiene: all `before/*` receipts are command output (verified tails above; c1-setup.txt correctly
  shows round-99 battery's FileNotFoundError → round-100 SETUP exit 2, as the plan describes). No hand-edited
  receipt found.
- `NEVER` keyword note for the integrator: my role-swap Do cell is a legitimately shocking counterexample
  because it stays inside *every* machine check. It is the best argument for the seat's brief: "a numeral-
  present Do can state the opposite of its warrant and pass everything."

## Findings summary (severity-ordered)
| # | Claim | Counterexample (run) | Enforced by | Fix |
|---|---|---|---|---|
| F-1 | C1 "that rev's tree" | HEAD-tree stand-in → battery PASS, verdict diverges on v3 (this report, standin files) | no leg (single-commit fixture) | 2-commit fixture + 3 cross-rev legs |
| F-2 | C1 "not judged" clause | universal-rev rejected only incidentally (r5/r6/q3); no admitted-non-capture-challenge leg exists | incident | 1 admitted-leg |
| F-4 | C2 kill rule "form differs"/overreach | form mutation + role-swap + negation all pass score() (probe-c2, probe-c2b) | numeral-token membership only (limit (b) covers sense, not form/role) | pin form mechanism; narrow kill rule to instrumented checks |
| F-5 | C2 "Do/Never numeral" | numeral-free correct Never refused; all 8 Nevers NONE_STATED → vacuous | NONE_STATED-or-numeral | re-express Never leg |
| F-6 | C2 flag "where it is held" | lying ## Update (26.9%/18.0%/significant) passes FRESH | string presence only | assert one correct numeral in Update |

## Verdict trailers
VERDICT: R100CriticClaims C1 fired — a HEAD-tree tool that violates the claim's "that rev's tree" clause prints the frozen PASS line (REV=11/11 PROD=6/6 included) and gives the wrong verdict on a cross-rev byte-copy, so the predicate's numbers understate the evidence needed for the sentence.
VERDICT: R100CriticClaims C2 fired — decision rows that invert their warrants (role-swapped study counts/rates; "significant improvement" for a p=0.85 slope) and a lying ## Update (26.9%/18.0%/"significant") pass every frozen counter (NUMBERS=24/24), so the kill rule's form/overreach clauses fire on artifacts the counter accepts, while the flag prose verifies presence ("S238" named) without one true numeral.
