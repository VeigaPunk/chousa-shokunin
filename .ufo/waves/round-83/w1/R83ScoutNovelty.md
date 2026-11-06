# R83ScoutNovelty — round 83, wave 1 (leaf scout, read-only reconnaissance)

Seat: `R83ScoutNovelty`. Lane: `chousa-shokunin` at `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Base `a46534a51756f7e7d9bb55dd9a275156d908d84c` · landing `81b81173f19d175e2b2a6b409b2a496d09d0b258` · tip `aca2a781ef2db375881c21bf407e153f786ac61f`.
Date 2026-11-06. No production edits, no git/jj mutation, no network fetch, no subagents. Scratch
`/fast/scratch/hyaku/chousa-r83/R83ScoutNovelty/` was used for every tree/fixture and deleted before this report was written.

**Tooling:** nothing installed or upgraded (git 2.56.0, python 3.14.8, bash 5.3.20, coreutils — all pre-existing).

**Receipts written (all under `.ufo/waves/round-83/w1/R83ScoutNovelty/`):**

| receipt | content |
|---|---|
| `R83ScoutNovelty/r83-k4-ground-sids.txt` | K4 ground greps (S-ids, 3 URLs, partial URL forms) at base/landing/tip |
| `R83ScoutNovelty/r83-k4-novelty-neighbours.txt` | novelty keyword sweep + nearest held entries + registry/lesson prior art |
| `R83ScoutNovelty/r82-routed-defect1.txt` | diff of the two r82 rerun receipts; independent re-run at both trees; the two flipped records' bytes; gate output per tree |
| `R83ScoutNovelty/r82-defect1-ruling.txt` | same two records at 3 gate revisions; SKILL.md item-2 contract text; r82 K2/K3 text |
| `R83ScoutNovelty/r83-corroboration.txt` | frozen depth counter at landing; diff vs baseline; wave classification rows; item-2 Run line per tree; byte-identity with the critic's K2(a) attack |

---

## Surface 1 — C1 kill rule K4 (ground): does any base-list entry cite S009/S212/S213 or their URLs?

**Answer: no. K4 does not fire; the ground is held.**

### 1.1 The base list is exactly the base-revision knowledge set

```
git -C <lane> ls-tree -r --name-only a46534a5... corpus/knowledge | grep '\.md$' | sed 's|corpus/knowledge/||' | sort > base_actual.txt
sort corpus/evidence/round83/base-knowledge.txt > base_listed.txt
diff base_listed.txt base_actual.txt
```
observed: `diff_rc=0  listed_count=94  actual_count=94` — receipt `r83-k4-ground-sids.txt` §A.
`grep -c . corpus/evidence/round83/base-knowledge.txt` = 94, and it contains **no** `.gitkeep` (r82 routed defect 3's counting slip is not repeated; r82's own list had `.gitkeep` and lacked `question-framing-frames-r82.md`, r83's list has the latter and not the former).

### 1.2 No base-list entry cites the three S-ids

```
git -C <lane> grep -n -F 'S009' a46534a5... -- corpus/knowledge   → rc=1 (no match)
git -C <lane> grep -n -F 'S212' a46534a5... -- corpus/knowledge   → rc=1 (no match)
git -C <lane> grep -n -F 'S213' a46534a5... -- corpus/knowledge   → rc=1 (no match)
```
receipt `r83-k4-ground-sids.txt` §B. The grep was run over the whole `corpus/knowledge` tree (a superset of the 94-file base list), so the base-list subset is covered. At landing `81b81173` and tip `aca2a781` the only hits are in the **new** entry `corpus/knowledge/appraisal-judgment-records-r83.md` (line 3 `source: S009, S212, S213`, then Q1–Q16 and the warrant cells) — that file is not in the base list, so it does not trigger K4.

### 1.3 No base-list entry contains any of the three URLs

```
git -C <lane> grep -n -F 'https://www.cochrane.org/authors/handbooks-and-manuals/mecir-manual/.../assessing-risk-bias-included-studies-c52-c60' <rev> -- corpus/knowledge   → rc=1
git -C <lane> grep -n -F 'https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-07' <rev> -- corpus/knowledge   → rc=1
git -C <lane> grep -n -F 'https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-08' <rev> -- corpus/knowledge   → rc=1
```
at **all three** revisions (base, landing, tip) — receipt `r83-k4-ground-sids.txt` §C. Partial forms were also checked at base (`chapter-07`, `chapter-08`, `c52-c60`, `c52-c75`) → all rc=1, §D. The only Cochrane URLs in the base knowledge set are `chapter-24` (`contextual-source-admission-r24.md:2`), `chapter-iv` (`metadata-screen-r25.md:3`, `recheck-due-r26.md:1`) and `training.cochrane.org/handbook/current/chapter-04` (`western-instrument-alignment-r50.md:3`) — none is one of the three.

### 1.4 Corroboration by the frozen counter

```
D=<scratch>/tree-landing; git archive 81b81173 | tar -x -C $D
python3 -B $D/corpus/evidence/round83/depth-r83.py --root $D
```
observed: `ENTRY appraisal-judgment-records-r83.md ok=yes rows=10 quotes=16/16 fails=-` /
`DEPTH_R83 entries=1 ok_entries=1 rows=10 located_quotes=16 fresh_sources=3` / `DEPTH_R83=PASS`, **rc=0** — receipt `r83-corroboration.txt` §A.
The counter's own E7 ("new ground") rule is the operational twin of K4 and passed (`fails=-`).

### 1.5 Does any *held entry* already teach the three things?

Keyword sweep over `corpus/knowledge` at base (`independent`, `two people`, `adjudicat`, `disagree`, `support for judgement`, `precise location`, `two reviewers`, `third person`, `conflict of interest`, `no information`, `working independently`, `risk[- ]of[- ]bias`, `MECIR`) — receipt `r83-k4-novelty-neighbours.txt` §A.

**No held entry teaches duplicate independent judgment, a predefined disagreement process, or recording the source location of a judgment.** The literal phrases `two people`, `support for judgement`, `precise location`, `two reviewers`, `third person`, `conflict of interest`, `no information`, `working independently` all return **rc=0 hits = 0** over the base knowledge set. Nearest held entries, quoted:

| held entry:line | what it says | same ground? |
|---|---|---|
| `corpus/knowledge/quality-control-guideline-issued-text-r48.md:25` | `S118` requires "two independent screeners", a third arbitrating, "选文献，如遇分歧，则由第三方协助判断" | **No.** Same *shape* (two independent people + third-party arbitration) but the ground is **study selection/screening** under a Chinese quality-control guideline, and it says nothing about recording the support or the source location of a judgment. Different source (S118), different act. |
| `corpus/knowledge/japanese-prisma-item-wording-r40.md:14` | PRISMA item 8/9 "ask[s] … whether the reviewers worked independently" | **No.** Reviewer independence as a *counted reporting item*; no process, no record of support/location. |
| `corpus/knowledge/claim-support-test-r37.md:26` and `:33` | Fleiss κ 0.7934, Krippendorff α 0.334, 84.4% — "measure annotator consensus … not an error bound on any one verdict"; "Where the disagreement sits is not read" | **No.** Agreement *measured* as a reliability figure for a labelling protocol; no predefined disagreement-resolution process, no recording of a judgment's source. |
| `corpus/knowledge/anchor-boundaries-r4.md:134` | "no support adjudication, no location binding" (of the lane's chain mode) | **No.** A negation about the lane's own tooling. |
| `corpus/knowledge/claim-support-states-r24.md:1-6` | what a support verdict rests on: access / relevance / support / truth | **No.** What a verdict *rests on*, not how one judgment is *made and recorded*. |
| `corpus/knowledge/sweeps-rejections-r5.md:42,:147` | a sweep "must name where it looked"; "The gate never adjudicates" | **No.** Claim-sweep locality, and explicitly no adjudication. |

Conclusion: the new entry's ground (make the judgment twice, fix the disagreement path in advance, record support + precise location, narrow use of "no information", override only with a stated reason) is **not** held by any base entry.

### 1.6 Residual (out of the K4 class — reported separately, not a kill)

K4 is scoped to *base-list entries* (`corpus/knowledge/*.md` named in `base-knowledge.txt`), so the following does **not** fire K4, but a reader of the claim should know it:

* `corpus/SOURCES.md:19` (at base) — S009's `teaches` cell already read "Require independent duplicate judgments, a predefined disagreement process, and recorded support for each judgment" (registry row, status `queued`, used-by `—`).
* `corpus/SOURCES.md:235-237` (at base) — the chain note already read "Keeping judgments honest — S009 → S011 → S012 → S017: duplicate supported judgments with a disagreement path".
* `corpus/lessons/round-24.md:56` (at base) — S009 was opened 2026-10-19 and C53 quoted: "Use (at least) two people working independently to apply the risk-of-bias tool".

So the *teaching statement* of this ground existed in the registry and in a lesson since round 1/round 24; the *entry* is new, and the counter's E7/E4 rules (which look only at base-list `source:` lines and at quote strings) are unaffected. The candidate entry's own claim — "Held entries say what a support verdict rests on … none says how one judgment is to be made and recorded" (entry lines 9-12) — is accurate as stated about held entries.

---

## Surface 2 — round-82 routed defect 1: the out-of-class record newly refused at the r82 tip

### 2.1 The diff the closure saw

```
diff -u corpus/evidence/round82/repair/rerun-landing.txt corpus/evidence/round82/repair/rerun-repaired.txt
```
observed (`rc=1`, receipt `r82-routed-defect1.txt` §A):

```
- TALLY class=in rc0=3        - TALLY class=in refused=182      + TALLY class=in refused=185
- TALLY class=amb rc0=12      - TALLY class=amb refused=4       + TALLY class=amb rc0=11
- TALLY class=out rc0=24      - TALLY class=out refused=8       + TALLY class=amb refused=5
                                                                  + TALLY class=out rc0=23
                                                                  + TALLY class=out refused=9
```

### 2.2 My independent re-run reproduces both receipts exactly (no selftest run)

Re-running the r82 `repair-rerun.py` Run lines over all 233 wave records against the two **committed** trees (landing `b4a41d25`, repairs `51a5dee8`):

```
landing  : TALLY class=amb rc0=12 / class=amb refused=4  / class=in rc0=3  / class=in refused=182 / class=out rc0=24 / class=out refused=8
repaired : TALLY class=amb rc0=11 / class=amb refused=5  / class=in refused=185 / class=out rc0=23 / class=out refused=9
```
receipt `r82-routed-defect1.txt` §B — byte-identical to the two committed receipts. (This also incidentally pins the unpinned "working tree" of `rerun-repaired.txt` to the committed tree `51a5dee8`, since that tree reproduces its tallies.)

### 2.3 Per-record flips: exactly two records changed status

Re-running every out- and ambiguous-class record against both trees and comparing exit codes (`diffgate.py`, same Run lines):

```
FLIP F-control-claimid-binds class=out item=2 landing_rc=0 repaired_rc=1
FLIP G-two-sweeps-first-bad class=amb item=2 landing_rc=0 repaired_rc=1
```
receipt `r82-routed-defect1.txt` §C.

* The **out-of-class** newly-refused record named by routed defect 1 (`out refused 8 → 9`) is **`F-control-claimid-binds`**.
* The **ambiguous** newly-refused record (`amb refused 4 → 5`) is **`G-two-sweeps-first-bad`**.

### 2.4 The bytes of `F-control-claimid-binds`

`.ufo/waves/round-82/w1/R82ExecForms/records/F-control-claimid-binds.md` (sha256 `e417981c3c362be0accd77bdaaca1d5217b67b04ce116ac38e2fca462cd0e85e`) is `corpus/evidence/round82/c1-records/item2-pass.md` (sha256 `d9f1aa511e8b94c328982b05b6316022ab2c87a37a863817d8d0953a5eec959e`) with **exactly one cell** changed:

```
 | id | kind | text | pointer | status | sweep |
-| N1 | negative | no pre-round knowledge entry file is named for the TARCiS statement | corpus/fixtures/sweeps-r5.md | observed-in-dump | W1 |
+| N1 | negative | no pre-round knowledge entry file is named for the TARCiS statement | corpus/fixtures/sweeps-r5.md | observed-in-dump | n/a |
```
receipt `r82-routed-defect1.txt` §D, `r83-corroboration.txt` §B.

Gate behaviour of that record across four revisions (item-4 Run line `bash tools/research-gate.sh verify-sweeps <record> --root .`):

| gate tree | observed | exit |
|---|---|---|
| `5d792e1e` (r82 pre-base) | `RESEARCH_GATE: CLEAN … findings=0 drift=0` | rc=0 |
| `b4a41d25` (r82 scored landing) | `RESEARCH_GATE: CLEAN … findings=0 drift=0` | rc=0 |
| `51a5dee8` (post-scoring repair) | `FINDING SWEEP_NEGATIVE_UNRESOLVED … obs=claim=N1 sweep=n/a names no sweep row this mode re-ran` | **rc=1** |
| `a46534a5` (round-83 base tip) | same `FINDING SWEEP_NEGATIVE_UNRESOLVED …` | **rc=1** |

receipt `r82-defect1-ruling.txt` §A. The item-2 Run line gives the same 0 → 1 transition (receipt §B of the corroboration set / `item2.txt` run).

### 2.5 Ruling on `F-control-claimid-binds`: it **carries a defect — in-class after all**; the refusal is **not** a false refusal

Two independent texts put this record inside the K2 class, and the wave's own `out` label applied only one of the K2 alternatives:

1. **The frozen r82 K2 rule is a disjunction, and K2(a) is met.** `corpus/evidence/round82/claims.md:53-58`: K2 fires on any record that "(a) differs from `item2-pass.md`, `item4-pass.md` or `sweeps-r5.md` in one reason, flip-condition, `where` or claim-`sweep` cell set to a declared-vocabulary value, **or** (b) … **or** (c) carries a `negative` claim whose sweep cell names no declared `## Sweeps` row id while no `## Sweeps` row's `claim_id` names that claim". This record differs from the baseline in **one** cell — the claim-`sweep` cell — and that cell is set to `n/a`, which is in the frozen closed placeholder vocabulary (`claims.md:46`: "a cell equal to one of: empty, `-`, `--`, `---`, `—`, `–`, `n/a`, …"). K2(a) is therefore satisfied. The wave's own classification row says why it was excluded — "positive control: K2(c) excludes claims a Sweeps row's claim_id names" (`.ufo/waves/round-82/w1/R82ExecForms/receipts/classification.tsv`, receipt `r83-corroboration.txt` §D) — i.e. it consulted K2(c) alone and did not test the K2(a) alternative, which the same record satisfies.
2. **The subject's own documented contract says refuse.** SKILL.md item 2, identical at the r82 landing `b4a41d25` and at the round-83 base tip `a46534a5` (`diff_rc=0`, receipt `r82-defect1-ruling.txt` §B/§C): "Round 82: a negative claim whose sweep cell names no sweep row the mode re-ran (an undeclared id, a header-only `## Sweeps`, **a placeholder**) is `SWEEP_NEGATIVE_UNRESOLVED` … exit 1". A placeholder sweep cell is a documented refusal form; the r83 lesson's rule 2 applies ("a K2 class is the subject's own documented contract, not an open vocabulary").
3. **Decisive: the lane's own critic filed the byte-identical record as an in-class K2(a) attack.** `cmp .ufo/waves/round-82/w1/R82ExecForms/records/F-control-claimid-binds.md .ufo/waves/round-82/w1/R82CriticClaims/attack-k2a-record.md` → **rc=0, identical**, both sha256 `e417981c3c362be0accd77bdaaca1d5217b67b04ce116ac38e2fca462cd0e85e` (receipt `r83-corroboration.txt` §H). `R82CriticClaims.md:96-133` ("### 4.1 K2(a) — claim-`sweep` placeholder accepted through a `claim_id` back-reference (kill)") names that record as the K2(a) **kill**, and the committed repair receipt carries the line `EXTRA R82CriticClaims/attack-k2a-record.md item=2 expect=refuse rc=0 bad` → `… expect=refuse rc=1 ok` (`corpus/evidence/round82/repair/rerun-landing.txt:10` → `rerun-repaired.txt:7`). So two wave seats filed byte-identical records and gave **opposite** expectations: the critic = in-class, expect refuse; `R82ExecForms` `classification.tsv` = "out", "positive control: K2(c) excludes claims a Sweeps row's claim_id names", expect pass. The tip's refusal implements the critic's expectation; the `out` label is the outlier.

Consequence: the tip's refusal of `F-control-claimid-binds` is **the contract-conformant behaviour**, not harm. Conversely, on the frozen r82 text the record was a **K2 firing at the landing too** (its item-2 Run line exits 0 at `b4a41d25`), so the r82 wave's reported K2 firing set (3 in-class passes) understated the class by one record that the wave had labelled a must-pass positive control.

**Ruling for routed defect 1: name `F-control-claimid-binds`; rule = in-class after all (carries a K2(a) form and violates the documented item-2 contract); the tip refusal is correct. Not a false refusal, so no K3-harm.**

### 2.6 Residual (out of the r82 K2 class — the genuine near-harm sibling)

The same receipt pair also contains a second newly-refused record that the closure did not route: **`G-two-sweeps-first-bad`** (sha256 `f69d5f9211338944eb8c7bfd6e0a19cdfe282a74809824b23852d8172cb015b9`), ambiguous-class per the wave, refused at the tip with `FINDING SWEEP_SECTION_DUPLICATE severity=warn surface=sweeps obs=section=Sweeps repeated; only its last body would be read` (rc=1; at `5d792e1e` and `b4a41d25` it was rc=0). Receipts `r82-routed-defect1.txt` §C/§D/§E and `r82-defect1-ruling.txt` §A.

On the frozen r82 K2 text this record is **not** in class: its claim-`sweep` cell names `W2`, a declared row id (K2(c) fails), and it differs from the baseline in two cells plus an added heading, not "in one … cell" (K2(a) fails) — the wave's own `why` column says the same ("not a one-cell difference"). Its only defect is a repeated `## Sweeps` heading whose *shadowed* first body carries `where=n/a`. Two further observations make it a residual rather than a clean kill for the lane:

* `SWEEP_SECTION_DUPLICATE` occurs **0** times in SKILL.md at the round-83 base tip and 2 times in `corpus/lessons/round-82.md:38` — the base-tip gate emits a refusal finding id that the subject's own executable checklist does not document (receipt `r82-defect1-ruling.txt` §D).
* The refusal is generic to any repeated `claims|sweeps|negatives|*reject*` heading, so it also catches records whose *kept* body resolves their claim.

This is out of class for round 83's two frozen claims (r83's C1 subject is the knowledge entry, C2's subject is the new tool `tools/gate-records.py`; neither is `tools/research-gate.sh`), and it is listed here as a residual for the lane, not as a claim firing. Note also that both newly-refused records are refused by the round-83 **base tip** `a46534a5` (which contains `51a5dee8` as an ancestor), so neither is a r83 regression.

---

## Unresolved gaps (stated, not filled)

* I did not re-open the three live Cochrane pages; K2's live-page half of C1 is another seat's rule and my K4 ruling needs only committed bytes.
* I did not run the gate selftest (per seat scope) and did not judge whether `G-two-sweeps-first-bad`'s refusal is acceptable under the r82 counter's positive set (`c1-manifest.tsv` positive group) — the wave classification, not the manifest, is what places it in the ambiguous class.
* The r82 wave's `out`-class labelling was derived from K2(c) alone for at least this one record; I checked the one record the closure routed and the one sibling that moved, not the whole 233-record classification. Whether other `out`-class rows are similarly mis-labelled under K2(a) is unmeasured by me.

## VERDICT lines

VERDICT: R83ScoutNovelty C1 held — K4 (ground) does not fire: no base-list entry cites S009/S212/S213 or contains any of their three URLs at base `a46534a5`, landing `81b81173` or tip `aca2a781` (receipts `r83-k4-ground-sids.txt`, `r83-corroboration.txt`).

VERDICT: R83ScoutNovelty C2 n/a — this seat measured no C2 bytes; the second surface was the round-82 routed defect 1, which is outside round 83's two frozen claims.

VERDICT: R83ScoutNovelty r82-defect-1 in-class — the newly-refused out-of-class record is `F-control-claimid-binds` (claim-`sweep` cell `n/a`, one cell from `item2-pass.md`), which carries a K2(a) form, violates the documented SKILL.md item-2 contract, and is byte-identical to the lane's own in-class K2(a) attack `R82CriticClaims/attack-k2a-record.md`, so the tip refusal is correct, not a false refusal (receipts `r82-routed-defect1.txt`, `r82-defect1-ruling.txt`, `r83-corroboration.txt` §H).
