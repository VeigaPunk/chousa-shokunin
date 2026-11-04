# R73C01 — do-nothing-control attacks

Axes: C1 operability/completion, C2 calibration/record precision, evidence provenance, reproducibility, claim independence. This is an attack report, not a round admission or canonical judgment. No frozen predicate was changed.

All receipt paths below are relative to this folder. `receipts.txt` contains actual commands, stdout/stderr and return codes. `reproduce.py` reconstructs the scratch fixtures; the fixture reads original base objects through a read-only local object alternate, with no fetch. Source snapshot: `frozen-c2-count.py` and `frozen-claims.md`. The fixture's initial files and two r72 receipts were read using `git -C <lane> show f748abbb6bf58388e732facd4ecec5612419c457:<path>`. Every fixture commit was preceded by an assertion that its git top-level equals the fixture directory. No gate battery or preflight was run by this seat.

## 1. C1: fabricated output reproduces all three expected counts

Attack target: claims.md:64–66, the three frozen counting commands. Persisted fabricated inputs:

- `fabricated-battery-r73.txt`: `RESEARCH_GATE_SELFTEST: fabricated`
- `fabricated-preflight-r73.txt`:
  ```text
  PREFLIGHT=0/7 FAILED=all ENV=broken
  # Required but never produced: SKIPPED=none
  ```

These were placed under the exact relative paths `corpus/evidence/round73/controls/{battery,preflight}-r73.txt` inside scratch, never in the lane controls folder. The exact frozen greps returned **1, 1, 1**, each rc=0 (`receipts.txt:105–114`). There was no battery run and no preflight run.

Attack result: all three counters accept the fabrication. The weakest individual counter is unanchored `grep -c 'SKIPPED=none'`: it accepts a comment describing an unmet requirement, independently of the `PREFLIGHT=` line that explicitly describes failure. The verdict-token counter also accepts an arbitrary value, not merely a real PASS/FAIL summary.

Important distinction: the full claim's prose DOES bind additional behavior: fresh actual runs, single-writer ordering, unset budgets, measured-revision headers, result/tally disclosure, and a commit carrying the receipts. Therefore this is a false green of the counters, not evidence that fabricated receipts satisfy the full claim. The counting commands consult only the two named working-tree paths: they do not bind commit identity, real execution, headers, tallies or the relation between the two preflight matches. Merely replaying r72 bytes is indeed red, but that narrow do-nothing control does not test fabricated new bytes.

Smallest future amendment for the weakest counter: require `SKIPPED=none` on the same anchored, parsed `PREFLIGHT=` summary line, rather than anywhere in the file. That closes the demonstrated comment/split-line bypass, not arbitrary forgery. To address provenance, counters must consume committed receipt bytes at a named revision and a trusted runner must capture the command/exit status and reconcile summaries with case/gate output. Text matching alone cannot prove execution. Findings only; no post-data amendment applied.

## 2. C2: mandatory identities cannot be omitted, but denials can pass

Attack target: `c2-count.py:90–114`, substring-based semantic checks, and `:125–134`, numstat loading.

The exact-base control is **C2=FAIL checks=2/7** (`receipts.txt:19–29`). A second scratch commit appends only the three required headings and self-refuting text. Its saved blocks are under `fabricated-blocks/`. They say “Nothing was corrected,” call 8426/8435 wrong labels, and explicitly deny the required tree statements. Thus they do not perform either record correction.

Plain-text score: **6/7**, with C2-1..5 and C2-7 green (`receipts.txt:40–55`). The semantic checks accept negations: C2-2/3/5 require substrings, not correct relationships or affirmative corrections.

Literal omission negative control: replacing 8426, 8435, 7f7ea19a and 6dd6c82 with `OMITTED` yields **4/7**, failing C2-2, C2-3 and C2-5 even with the diff bypass below (`receipts.txt:94–104`). Therefore **no**, the seven checks cannot pass with those required tokens literally absent. **Yes**, they can pass with those tokens mentioned only in denials that correct nothing.

### C2-6 measures additions, not removals

`git diff --numstat` prints added, deleted, path. `c2-count.py:131` assigns `parts[0]` to `deleted`; `:110–112` then requires this value to be zero and labels it “removed lines.” The append-only fixture has `4\t0\t<path>` for each required document (`receipts.txt:41–44`), but the counter reports four removed lines per file and fails C2-6 (`:52`). An ordinary append-only correction is therefore penalized by this implementation. This is a fixable counter defect, not a precision-versus-cost tradeoff.

### Same committed revision flips red/green through uncommitted attributes

Cheapest false-green control: put `*.md -diff` in the SCRATCH fixture's `.git/info/attributes`. No tracked bytes or commit identity change. Numstat becomes `-\t-\t<path>`; `:131` converts each nonnumeric value to zero. The denial-only revision now prints **C2=PASS checks=7/7**, rc=0 (`receipts.txt:56–71`). Remove that local attribute and the SAME revision reverts to **6/7**, rc=1 (`:73–83`). This directly falsifies the claim that all seven checks depend solely on committed bytes at `--rev`.

Impacted axes: calibration, append-only integrity, false provenance and cross-clone reproducibility. The control need not carry any C1 receipt (`receipts.txt:72`). No attribute was written in the lane repository.

Smallest safe future correction: read numstat's second column, reject nonnumeric fields instead of accepting them as zero, and bind the check to attribute-independent bytes. For this append-only requirement, checking each original committed blob is a byte prefix of its replacement avoids local diff attributes entirely. Semantic correctness still needs evidence-backed review of the actual line/tree relationships; merely demanding their tokens cannot distinguish the saved denials. The frozen counter was not edited.

## 3. Independence attack

Attack target: claims.md's statement that neither claim needs the other to have landed.

- C2 counter green with C1 absent: the denial-plus-local-attribute fixture scores 7/7 with both r73 receipt paths absent (`receipts.txt:56–72`). This proves mechanical nondependence, not valid C2 correction or valid admission. A genuine C2 correction likewise has no intrinsic dependency on whether a separate battery completed; the counter's C2-6 defect prevents an ordinary append from scoring green under the unchanged implementation.
- C1 counters green with C2 red: the three greps score 1/1/1 with fabricated receipts, while the exact-base C2 document state still scores 2/7 (`receipts.txt:105–125`). Neither set of counters reads the other claim's required new artifacts. C1 additionally reads working-tree files whereas C2's document reads use committed revisions.

Attack result: no cross-claim causal dependency was found. C2 can be recorded while C1 honest-stops, and C1's completion receipts can exist while C2 remains uncorrected. This does NOT establish that either complete claim is true, and the common round admission rule can still require both. Smallest correction: preserve the separability statement, but distinguish claim-local outcomes from joint round admission and make receipt revision binding explicit. Do not treat counter independence as evidence of soundness.

## Scope and cleanup

All lane changes were confined to this seat's output folder; the separately requested seat report is the only sibling file written. No tools installed. No network, source-tree edits, lane git mutations, full selftest battery, subagent dispatch or canonical judgment. Scratch `/fast/scratch/hyaku/chousa-r73/w1/R73C01` was deleted; see `cleanup.txt`.

Self-evaluation: accuracy 4/5 (the driver captures exact-base runs; findings do not establish malicious intent); completeness 4/5 (all three assigned attacks covered, no full-battery execution by design); clarity 4/5 (counter acceptance is explicitly distinguished from whole-claim truth); actionability 4/5 (minimal future corrections supplied, not applied to frozen rules); conciseness 4/5 (extra provenance detail retained to make counterexamples reproducible). Overall 4.0/5. Highest-impact recommendation: report the C2-6 defect and its same-revision red/green flip without silently changing this round's frozen predicate.
