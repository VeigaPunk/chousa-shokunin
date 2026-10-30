# Round 63 (attempt 2) — chousa — frozen claims

Frozen before any after-measurement is recorded. Base: lane master `4ece131ca826c646bd28a50802d41bc78d8a9717`.
Date 2026-10-30. This is the second freeze of steered round 63: attempt 1 froze
`corpus/evidence/round63/claims.md` at `62876ef90154714bfa806fbbec7890a9ff11b179`, landed both its claims, and
was ended by the operator's run-11 wrap-up before its wave settled; the closure never ran, the claim was
released, and the orchestrator re-dispatched the same round. Attempt 1's frozen file, verdicts and instruments
stand as its record; nothing in this file rewrites them. A new instrument may not reuse a frozen name, so the
battery is `c1-battery-v2.py`. Digest prefixes below are 16-hex (`sha256sum FILE | cut -c1-16`). No predicate,
counter, battery, kill rule or target below changes after the freeze commit; a changed rule is not the claim's
rule. Post-hoc findings against a frozen instrument are routed as limits and supplements, never as a rewrite.

**No wave this round.** The orchestrator paused new campaign dispatches on 2026-10-30 (provider failures
"minimax plan exhaustion, Cursor pricing, Anthropic 429, ZAI 429 and Devin permission denial"; "Do not request
new waves/replacement seats just to retry these failures"; "New campaign dispatches paused pending provider
availability", irc from the parent session). No `.ready` file is written and no seat is dispatched: the L2
floor of the round contract is therefore unmet and is reported as such, with every attack item this round
would have carried listed in the lesson's routed section. The claims below are judged only by their frozen
counters, their committed controls and the closure's independent re-runs.

Files this round amends or creates (state at the freeze: `tools/lane-preflight.py` exists from attempt 1 and
is amended this round; `tools/claims-audit.py`, `corpus/knowledge/self-claim-audit-r63.md`,
`corpus/lessons/round-63-attempt2.md`, `corpus/SOURCES.md` rows S146–S149 and the after-receipts do not yet
exist or are not yet appended; a path named here is not a false pointer):

`Created by the round:` `tools/claims-audit.py`, `corpus/evidence/round63/audit/audit-a2.tsv`,
`corpus/knowledge/self-claim-audit-r63.md`, `corpus/lessons/round-63-attempt2.md`.
`Amended by the round:` `tools/lane-preflight.py` (G04/G05 rules), `SKILL.md` (gate rows), `corpus/README.md`,
`corpus/SOURCES.md` (rows S146–S149), `SCORECARD.md`, `LOG.md`.

## C1 — operability: the round-63 falsifier class is closed in the battery, not only in the routed list

Target axis: operability — the lane's only numerically scored axis (historical 3/10 on the round-1
archived-export observable; that numeric observable is not moved and no new score is invented). Tag `plumbing`.

Attempt 1's wave demonstrated, with committed findings, that the frozen battery `c1-battery.py` accepts the
round's falsifier class: a zero-gate run that exits 0 is uncovered (`CritC1Skip.md`), six lying outputs are
accepted by its judge on their legs (`CritC1JudgeHoles.md`: form feed on the summary line, a wrong gate name,
a glued status, GATE lines on the usage leg, a silent exit 2, a duplicate summary member), one path-keyed
forger passes it in full by recognising the battery's fixed paths, environment and planted words
(`CritC1PathKeyed.md`, the `token` forger), and a 55-line content oracle that never runs a gate passes all 22
legs (`CritC1DiffOverfit.md`); the same wave found the landed tool's G04/G05 rules false-positive on sibling
files (`CritC1GateRules.md`). Attempt 1 routed all of this to the next round's battery. The routed work is
this claim.

**Predicate R63-C1v2** (the sentence in the docstring of `corpus/evidence/round63/c1-battery-v2.py`): run on a
tool T meeting the lane-preflight contract of attempt 1's `claims.md` as amended for G04/G05 — the battery
copies the lane once into a scratch GOLDEN, then for each of 29 legs copies the golden to a random-named
variant, applies one change, copies T's bytes to a random path outside the variant, runs it from an empty cwd
with a minimal seeded-random environment, and requires — CLEAN (unchanged variant, `--skip G08`: exit 0,
`PREFLIGHT=7/7 FAILED=none ENV=none SKIPPED=G08`); DEFECTS D01–D17 (attempt 1's fifteen defects plus D16 a
broken freeze-check selftest whose source still carries the text D09 edits and D17 the same for
assimilate-rows), each naming the exit code, the exact FAILED and ENV sets and all other run gates PASS;
BENIGN B01–B08 (attempt 1's six plus B07 a SHONEN span holding a verdict ratio and B08 a capability row whose
evidence tokens carry a `:N` suffix, a trailing dot and a `{a,b}` brace shorthand whose members exist), exit 0
with all run gates PASS; ZERO Z01–Z03 (three no-gate selections), exit 2 with all eight GATE lines SKIP and
one summary `PREFLIGHT=0/0` — and prints `CLEAN=1/1 DEFECTS=17/17 BENIGN=8/8 ZERO=3/3 BATTERY=PASS`, exit 0.
The judge is hardened exactly against the six wave holes: no control character on stdout, no non-contract
stdout line, GATE lines must carry the contract name paired with their id and a status followed by
end-of-line or one space, each FAILED/ENV/SKIPPED summary component is `none` or distinct valid ids, a usage
run prints no output lines and names the bad id on stderr. The harness is hardened against the `token` forger:
directory names, tool paths and environment keys are seeded-random per leg, and the planted words of D02, D03,
D04, D05, D06 and D15 carry no fixed keyword (D15's pointer is `zz-<tag>.md`). It never runs G08.

Counting command (from the lane root; scratch under `$HYAKU_SCRATCH/chousa-r63/`):

    python3 corpus/evidence/round63/c1-battery-v2.py --tool tools/lane-preflight.py --fleet <fleet root> --work <dir>

**Before** (the same falsifier class against the frozen battery, receipt `controls/exhibits/exhibit-v1-before.txt`,
runner `controls/run-exhibit-receipts.py`, digest `99953077b7cd2d07`): the frozen `c1-battery.py` accepts the
attempt-1 wave's falsifier class nine of nine — E01 (the frozen reference `controls/pos-ref-preflight.py`, the
zero-gate exit-0 tool), E08 (`exhibits/forge-token.py`, a committed re-creation of the wave's `token` forger)
and E09 (`exhibits/overfit-oracle.py`, the wave's 55-line oracle, byte-exact, sha256 prefix `9ebbe9b8a8d61137`)
each read `BATTERY=PASS` in full, and E02–E07 (the six judge-hole lies, `exhibits/lie-*.py`) are accepted on
their own legs (`--only` runs, `LEG ... ok`). The honest controls (`honest-clean.py`, `honest-d06.py`,
`honest-d14.py`) are accepted too — the judge must not reject honest answers.

**After target**: the same exhibits against the v2 battery (`controls/exhibits/exhibit-v2-after.txt`): all
nine rejected — E01 fails B07/B08 (its old G04/G05 rules flag the benign shapes) and Z01–Z03 (its zero-gate
run exits 0); E02–E07 rejected on their own legs by the strict judge; E08 and E09 read `BATTERY=FAIL` in full
(both miss D16/D17: their G06/G07 are keyed on source text, the selftests are broken — and both fail B07/B08
and Z01–Z03) — while the honest controls stay accepted, and the landed `tools/lane-preflight.py` (with the
G04/G05 amendments of this round) reads `CLEAN=1/1 DEFECTS=17/17 BENIGN=8/8 ZERO=3/3 BATTERY=PASS` exit 0 in
three runs at the landing bytes (`controls/c1v2-landed-runs.txt`), with the full run
`python3 tools/lane-preflight.py --root . --fleet <fleet root>` printing `PREFLIGHT=8/8 FAILED=none ENV=none
SKIPPED=none`, exit 0 (`controls/preflight-full-run-final.txt`).

**Controls** (committed at or before the freeze): the before receipt above is the do-nothing control — the
instrument that skips the claimed work is the frozen battery itself, and it scores 9/9 accepted where the
target is 9/9 rejected; `controls/c1v2-nulls-v2.txt`: `null-pass.py` and `null-diff-oracle.py` (attempt 1's
committed do-nothing tools) read `BATTERY=FAIL` exit 1 under the v2 battery; the three honest-output controls
are accepted under both batteries; the exhibit runner prints per-run lines so the closure can re-derive every
count. The landed tool also still passes the frozen attempt-1 battery in three runs after the G04/G05
amendment (`/fast/scratch/hyaku/chousa-r63/l1/v1-on-fixed-tool.txt` copied to `controls/c1-on-fixed-tool.txt`),
so the amendment regresses nothing the freeze of attempt 1 pinned.

**Kill rule** (frozen): C1 is verified only when the unmodified `c1-battery-v2.py` at the closure reads
`BATTERY=PASS` for `tools/lane-preflight.py` at the landing commit (three runs) and the exhibit receipt reads
nine of nine rejected with the three honest controls accepted. A miss is an honest stop, not narrowed after
landing. A falsifier class a later wave demonstrates against the v2 battery is routed to the next battery, not
a refutation.

**Named limits** (disclosed before data): the exhibits are re-creations by the author of the v2 battery from
the wave findings' committed descriptions — E02–E07 are fixed-output probes valid on their own leg only, E08's
fallback embeds old-rules gates (behaviorally the wave oracle's bodies) because the wave's own fallback is
deleted scratch, and E09 is the wave's byte-exact oracle; a forger that embeds a faithful copy of the amended
tool itself remains indistinguishable (the wave's t00 residual, still open); E08 is rejected under the v2
harness by failed recognition plus its old-rules fallback, not by the D15 keyword (recognition fails first) —
the keyword-free plants are the second layer; the v1 judge's t11 residual (free text after a status) stays
open by design; the v2 battery never runs G08 (the full run is the one receipt for that gate); the gate set is
chousa's own; the 16 attempt-1 mutants were not re-run under v2 (their lies are leg-level, and any tool
failing v1 fails v2 unless its lie matched exactly a hole v2 closes — the six E02–E07 exhibits are that case,
and they are rejected).

## C2 — calibration: a committed checker for false statements in a frozen claims file

Target axis: calibration — self-assessment checked against observed repo state (the axis is unmeasured in
`SCORECARD.md`; no numeric score is invented, the claim is the move from no instrument to a committed one).
Tag `plumbing`.

Round 62's claims file carried 14 statements its own files contradict and attempt 1's carried 4; both were
caught after the freeze by non-author readers, and both spot-checks routed the same fix: "give the
14-statement class a checker or a pre-freeze claims-vs-files read" (round-62 spot-check item 3; attempt-1
lesson mistake 4). This claim lands the checker and the read.

**Predicate R63-C2** (the sentence in the docstring of `tools/claims-audit.py`, digest `d48247f9c77ac1e7`):
given a claims file and a rule TSV (id, rule, anchor, target, expect, note), the checker prints one
`FLAG <id> <class> <detail>` line per rule that fires, `AUDIT_STALE <id>` (and exit 2) when an anchor is
absent from the claims file, and one summary `FLAGGED=<k>/<n> AUDIT=PASS|FAIL`, exit 1 iff some rule fired;
its seven classes are `json-count`, `section-contains`, `section-contains-at`, `git-first-commit`,
`file-kind`, `verbatim-heading` and `scope-narrower`. On the two committed errata'd claims files with the
committed rule files it flags the six mechanically-checkable erratum statements:
`python3 tools/claims-audit.py --claims corpus/evidence/round62/claims.md --audit
corpus/evidence/round63/audit/audit-r62.tsv --root .` prints `FLAGGED=2/2 AUDIT=FAIL` exit 1
(erratum rows 1 and 13), and the audit-r63 twin on attempt 1's claims prints `FLAGGED=4/4 AUDIT=FAIL` exit 1
(E1–E4). **Before**: the tool is absent at the base — the same commands in a `git archive` export of
`4ece131c` exit 2 (`controls/audit-before.txt`). **After target**: the two FLAGGED lines above, plus
`python3 tools/claims-audit.py --selftest` printing `AUDIT_SELFTEST=PASS (3 cases)` exit 0,
`python3 corpus/evidence/round63/audit-probe.py` printing `PROBE_FACTS=11/11` exit 0
(`audit-probe.txt`), and the pre-freeze read of this file itself: `python3 tools/claims-audit.py --claims
corpus/evidence/round63/claims-a2.md --audit corpus/evidence/round63/audit/audit-a2.tsv --root .` prints
`FLAGGED=0/4 AUDIT=PASS` exit 0 (`audit-a2-result.txt`) — the round's own claims pass their own audit before
the freeze.

**Sourced**: the landed entry `corpus/knowledge/self-claim-audit-r63.md` cites rows S146 (`grep(1)`, the
fixed-string semantics of the verbatim-heading class), S147 (`git-log(1)`, the `--diff-filter=A` semantics of
the git-first-commit class) and S148 (the probe output, own-work), each opened this round (2026-10-30,
installed local pages rendered with `MANWIDTH=1000 man -l FILE | col -bx`; no URL is fetched), with S149
(`file(1)`) rejected; the lesson's `## Gate` records each row's access date and located quote, 3 admits and
1 reject, for the non-author spot-check.

**Kill rule** (frozen): C2 is verified only when, at the closure, the four commands above reproduce their
stated outputs with the frozen bytes (`claims-audit.py` `d48247f9c77ac1e7`, `audit-r62.tsv`
`0364cfe29bb67d6e`, `audit-r63.tsv` `6bbd917a5007f030`, `audit-probe.py` `9167ec2a454e4b8e`). A miss is an
honest stop, not narrowed after landing.

**Named limits** (disclosed before data): six of the eighteen erratum statements are machine-checkable; the
other twelve are judgment corrections that stay prose-only (the entry lists which and why). The checker is
lexical and line-local (`json-count`, `verbatim-heading` read the anchor line only); the rule rows are
authored by the same lane that wrote the claims file, so the checker is a screen for demonstrated classes —
a reader outranks it, and a statement true as written but irrelevant passes. `git-first-commit` and
`section-contains-at` need a git checkout (rows SKIP, counted, when `--root` is not a work tree). A number
inside a word (`v2`, `w1`) does not count as a named count.

## Frontier step (not a claim)

Census before and after with exit codes (`.ufo/waves/round-63/census-start-a2.txt` exit 0; rows 145 → 149;
`census-end-a2.txt`); one mistake mined into `corpus/lessons/round-63-attempt2.md` `## Mistakes`; the sourced
claim is C2; at least one admit and one reject for the non-author spot-check (S146/S147/S148 admit, S149
reject). Assimilation: none — the wave-4 quarantine duty was discharged in round 42 (24-row slice verdicted,
`corpus/evidence/round42/quarantine-verdicts.tsv`, zero rows present), package adoption stays closed, and
this round's id-collision check found 64 of the staged package's ids already occupied in the lane registry
(`.ufo/waves/round-63/assimilation/{reg-ids,staged-ids,collisions}`), recorded as a reason adoption stays
closed. considerthese: `CT-20261019-4` (the SKILL.md size-watch threshold) stays an open operator question
(L0 line of round 62, unchanged); no second proposal is mined this round.

## Wave shape

None. Round total 0 seats. The orchestrator paused new campaign dispatches on 2026-10-30 (provider
failures; the two irc directives are quoted in the report); no `.ready` file was written and no wave,
residual call or replacement seat was requested. The L2 floor is unmet this round; the attack items the wave
would have carried (a non-author re-run of every command above, a mutation pass on the v2 battery and the
checker, a re-open of S146–S149, an entailment read of the entry, the spot-check of the S-admits and the
reject) are named in the lesson and routed to the next round.

## Frozen instruments, digests and receipts

sha256 prefixes of the frozen bytes: `c1-battery-v2.py` `0fbfd076e9a6235c`, `claims-audit.py`
`d48247f9c77ac1e7`, `run-exhibit-receipts.py` `99953077b7cd2d07`, `audit-probe.py` `9167ec2a454e4b8e`,
`audit-r62.tsv` `0364cfe29bb67d6e`, `audit-r63.tsv` `6bbd917a5007f030`, `exhibits/forge-token.py`
`aabd28d1f3a63837`, `exhibits/overfit-oracle.py` `9ebbe9b8a8d61137`. The receipts under `controls/` and
`controls/exhibits/` are the committed output of the runners at these bytes; the after-receipts
(`c1v2-landed-runs.txt`, `c1v2-nulls-v2.txt`, `exhibit-v2-after.txt`, `preflight-full-run-final.txt`,
`c1-on-fixed-tool.txt`, `audit-a2-result.txt`) are the observed output of runs on the pre-landing tree whose
measured bytes are the landing commit's — verified at landing by `git diff --stat <landing-hash> --` over the
measured paths being empty.
