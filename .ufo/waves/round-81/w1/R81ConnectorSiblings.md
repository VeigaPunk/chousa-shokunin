# R81ConnectorSiblings — sibling-overlap scan (read-only)

Seat: R81ConnectorSiblings, lane chousa round 81. Leaf seat: no dispatch, no production edits, no
commits, no absorption. Round base `378fda82dc2cbcc555a0565052cc408121813cef`; candidate landing
`7e2da96a0541946e796384d42fea18e09ede9e9f` was **not** read, run, or judged by this seat — this scan
measures sibling repos only, plus one read-only token check of the C2 counter's own print statements.

Scratch: `/fast/scratch/hyaku/chousa-r81/R81ConnectorSiblings/` (created with `mkdir -p`, deleted at
exit). No clone, archive tree or fixture repo was needed: every sibling read is `git -C <repo> show`
or a worktree read, all under `/home/vgpnk/Projects/shokunin/`. Nothing written outside this folder.

Question put to this seat: **does another lane hold knowledge on citation searching or
correction/retraction status, or a stronger "executable checklist" runner?**

Short answer: **citation searching — no. Correction/retraction status — no (one capture, no knowledge).
Stronger executable-checklist runner — yes, kagi's, and it does not contest chousa's scope.**

---

## 0. Method and pins

Scan population: the 20 sibling repos under `/home/vgpnk/Projects/shokunin/*-shokunin/`, chousa
excluded. Revisions pinned at scan time:

`receipts/revisions.txt` — command
`for d in <20 repos>; do printf '%-26s %s\n' "$d" "$(git -C $d rev-parse HEAD)"; done` (rc=0):

| repo | HEAD |
|---|---|
| audio-shokunin | `f9da7ee97e0ba95da1803c2afe9c616c519bae18` |
| game-dev-2d-shokunin | `1e033ef053beedf9a201daa21fbeb9c8b2f72dc3` |
| game-dev-3d-shokunin | `39ca3973c7865456d97fae18033f3f460c6cf8c1` |
| kagi-shokunin | `44808ced56359c98f35995178fb24a6482899263` |
| kaidoku-shokunin | `0b518f568da7b40a4ab026508d63c942faa7badf` |
| kake-shokunin | `dd7a146df338ec3de07a88f08f36c8278760afec` |
| kama-shokunin | `f77d2ae9f2797a19e7548989fb9e64d8f9411d3f` |
| kasegi-shokunin | `9d0b1eb0709e47c3c6decc09138b5012a8968924` |
| kengaku-shokunin | `34b28c47bc38b4e0aa11f44f2dfe7c9470d551ac` |
| kotoba-shokunin | `0344ddaea831b92546360a55ae02db2654fbccf8` |
| kotodama-shokunin | `5fa04a9bbda25aa31c8270265fd9997eb97d9ebb` |
| kumitate-shokunin | `4f3a8d633f2f4770073c51db5f5ee3300997140d` |
| lore-shokunin | `0f044aa7c7e4e17cfd5b6278179709b60db45d61` |
| mado-shokunin | `24ba2a9ddac21c1211579231e6ee1d98963f9988` |
| mori-shokunin | `7765969c79e6f3df44cce2e303e6a0cf2b054d8b` |
| revenger-shokunin | `654d09298960d0886274d37a0492b8e6d98b2c96` |
| souji-shokunin | `feb283eea6d03656864d9dcba43e178b127681ee` |
| tabi-shokunin | `d65546b30332d41b51b074b1944a8a3ded47a79f` |
| tameshi-shokunin | `6998726ff2fc554b399007cd3a8a92e8178f7da5` |
| tsukuroi-shokunin | `c6941adbcd972de8ad1b93ce5f796e16ea630858` |

**Disclosure — live lanes.** Four of these HEADs moved between my first read and the receipt above
(kama `138a7543`→`f77d2ae9`, souji `0d8ce29a`→`feb283ee`, tameshi `f256302b`→`6998726f`, tsukuroi
`69915b86`→`c6941adb`). The pins above are the instant the receipt was cut; a sibling landing a
mechanism after that instant is outside this scan.

**Disclosure — uncommitted sibling bytes.** Three cited files differ between HEAD and worktree
(`receipts/head-vs-worktree.txt`, command `git -C <repo> show HEAD:<path> | sha256sum` vs `sha256sum
<repo>/<path>`, all rc=0): kagi `SKILL.md`, kagi `PROVINCE.md`, tabi `PROVINCE.md`. For the two kagi
files the quoted lines are byte-identical at HEAD (`receipts/head-pinned-quotes.txt`, `git -C
kagi-shokunin show HEAD:<path> | sed -n '<n>p'`, rc=0). For **tabi** the chousa row I first saw at
`PROVINCE.md:186` is **uncommitted worktree bytes**: `git -C tabi-shokunin status --porcelain --
PROVINCE.md` → ` M PROVINCE.md` (rc=0); `git -C tabi-shokunin show HEAD:PROVINCE.md | wc -l` → `169`;
the same file at HEAD greps `chousa` with **rc=1** (`receipts/tabi-uncommitted.txt`). That row is
**dropped from the findings** — a live lane's in-flight edit is not sibling knowledge and is not
citable.

---

## 1. Citation searching — **no sibling holds it**

Command (`receipts/grep-tarcis.txt`), all file types, all 20 repos:

```
grep -rn -i 'tarcis' <20 repos> 2>/dev/null; echo "[grep_rc=$?]"
```

Observed: `[grep_rc=1]` — **zero hits**. No sibling repo contains the string `tarcis` in any file.

Command (`receipts/grep-knowledge-citation.txt`), sibling `corpus/knowledge/` dirs only:

```
grep -rn -i -E 'tarcis|citation search|forward citation|backward citation|citation chasing|retraction watch|crossmark|expression of concern|is_retracted|retraction notice' <20 knowledge dirs> 2>/dev/null; echo "[grep_rc=$?]"
```

Observed: `[grep_rc=1]` — **zero hits across all 20 sibling knowledge corpora** (1,288 entries
total at these pins). No sibling knowledge entry names TARCiS, citation searching, forward/backward
citation chasing, or citation snowballing.

The broad sweep (`receipts/grep-citation-terms.txt`, 348 hits, rc=0) is almost entirely siblings
**restating chousa's own province** — 160 sibling files contain the literal
`chousa-shokunin/PROVINCE.md` (154 of them under `.ufo/waves/`, i.e. wave reports). Representative, and the pattern is uniform:

- `kagi-shokunin/.ufo/waves/round-26/build/ConnectResearch.md:27` — "**Chousa owns the method.**
  `chousa-shokunin/PROVINCE.md:3-8` lists question framing, source hierarchy, citation chaining,
  claim-vs-source verification and search-strategy taxonomy."
- `kake-shokunin/PROVINCE.md:42` — "`chousa` owns research method and source hierarchy; kake keeps only"
- `kasegi-shokunin/PROVINCE.md:47` — "chousa — research method and source hierarchy"
- `souji-shokunin/PROVINCE.md:116` — "chousa-shokunin owns the research method and source hierarchy; souji's"
- `kengaku-shokunin/PROVINCE.md:284` — "capture and citation method stay chousa's
  (`chousa-shokunin/PROVINCE.md:5-7,10-11`)"

Classification: **unrelated to the hold question — acknowledgement, not knowledge.** These are
siblings ceding the surface, which *strengthens* chousa's C1 ground rather than contesting it.

One fleet-root record exists outside the sibling population, recorded for completeness and not as a
sibling hit: `.ufo/reports/round-12/SOURCES.md:109` — "W1 `art-curation.md` §Leads
(unopened/access-limited) reports AJP-2.1 and TARCiS routes returning 403 … They remain **leads, not
evidence**". That is a round-12 aggregator note that a TARCiS route 403'd; it is not knowledge, and it
is consistent with — not contradictory to — this round's S208 403 rejection.

## 2. Correction / retraction status — **no sibling knowledge; one capture names the mechanism**

Command (`receipts/grep-retraction-mechanism.txt`), `.ufo` wave scratch excluded:

```
grep -rn -i -E 'retraction watch|crossmark|expression of concern|is_retracted' <20 repos> 2>/dev/null | grep -v -- '/\.ufo/'
```

Observed: 9 lines, rc=0. Eight are incidental (Crossref JSON blobs carrying
`"crossmark-restriction"`, a Frontiers page's `crossmark-cdn.crossref.org` script tag, an OpenAlex
record's field set). **One is substantive:**

- `mori-shokunin/corpus/evidence/sources-r65/S576.html:139-140` —
  `<h3 id="is_retracted"><code>is_retracted</code></h3>` /
  "`Boolean.` True if the work is known to be retracted, per the [Retraction Watch database]."

That is a **capture**, not knowledge. Its registry row is `mori-shokunin/corpus/SOURCES.md:356` —
`| S576 | OpenAlex works — work object (docs.openalex.org) | docs | A | the OpenAlex work-record field
semantics behind S262's pinned record copy: the abstract ships only as an inverted index …`. The row's
stated purpose is abstract reconstruction for the OOM paper, not retraction checking, and
`grep -rln 'S576' mori-shokunin/corpus/knowledge/` returns nothing — no mori knowledge entry cites it.

Classification: **unrelated to the hold question, but a real mechanism prior.** The fleet already holds
bytes documenting that retraction status is a machine-readable field backed by the Retraction Watch
database. Chousa's C1 claim is scoped to *its own base* ("no base entry is about erratum/retraction
linking"), which is true; the mechanism's *fleet-wide* novelty is therefore lane-local, not fleet-first.
That is a scope note for the closure, not a contest and not a kill.

## 3. Executable checklist — **kagi holds a stronger mechanism; not contested scope**

### 3.1 The population is barren

Command (`receipts/checklist-sections.txt`), a Python scan of every sibling `SKILL.md` `## Checklist*`
section counting `- [ ]` items and `- Run:` lines:

| repo | line | heading | items | `- Run:` lines |
|---|---|---|---|---|
| kaidoku-shokunin | 895 | `## Checklists` | 0 | 0 |
| kama-shokunin | 193 | `## Checklist — current registered-endpoint workflow` | 0 | 0 |
| kotodama-shokunin | 584 | `## Checklist (executable where a tool exists)` | 4 | **0** |
| mori-shokunin | 149 | `## Checklist (executable)` | 4 | **0** |
| souji-shokunin | 176 | `## Checklists` | 14 | 0 |

`TOTAL_CHECKLIST_SECTIONS=5` (rc=0). And across **every** sibling `SKILL.md`, not just checklist
sections: `grep -n '^- Run:' <18 sibling SKILL.md paths>` → `[grep_rc=1]`, zero hits; the looser
`grep -n 'Run:' <same 18 paths>` → `[grep_rc=1]`, also zero (`receipts/run-line-grep.txt`). Two of the
20 siblings (`audio-shokunin`, `game-dev-2d-shokunin`) have no `SKILL.md` at all and are excluded from
that grep; the denominator is 18, not 20.

So chousa's C2 form — a `Run:` line per checklist item, inside `SKILL.md` — has **no sibling
precedent**. Two siblings carry a section literally titled "executable" with zero Run lines:
`mori-shokunin/SKILL.md:149-154` (4 items) and `kotodama-shokunin/SKILL.md:584-596` (4 items). Both
are the defect chousa's C2 fixes, unfixed.

### 3.2 kagi's mechanism is stronger on declaration, weaker on discrimination

kagi holds the fleet's most developed executable-checklist mechanism, and it is a **knowledge entry**,
not just a tool:

- `kagi-shokunin/corpus/knowledge/checklist-execution.md` (206 lines; HEAD blob
  `485e219a06c5b92f…`, worktree MATCH). §1, lines 15-17: "Before round 15 the checklist was 16 `- [ ]`
  bullets and nothing else: no command mapped an item to an outcome, so "the checklist is done" was a
  claim with no artefact". That is **the same defect class** chousa's C2 is fixing.
- `kagi-shokunin/PROVINCE.md:71` (identical at HEAD): "`corpus/checklist.tsv` holds one row per
  SKILL.md checklist item (8 columns: `id class lead check expect_exit expect_last reason note`), each
  either `runnable` … or `by-hand` (a closed class + a unique ≥24-char reason). The `lead` ERE is a
  **bijection** over the 16 items, so an item with no row, a row with no item, a duplicated lead/item, a
  below-floor runnable ratio (`ceil(items/2)`) and a repeated by-hand reason are all defects."
- `kagi-shokunin/SKILL.md:41` (identical at HEAD): exit 0
  `CHECKLIST_RUN: CLEAN (items=16 runnable=9 by_hand=7 failed=0)` +
  `CHECKLIST_RATIO: runnable=9/16 floor=8 by_hand=7`; 1 `ITEM-FAIL`/`ITEM-LASTLINE`/`UNDECLARED`/
  `EXTRA`/`UNMATCHED-ITEM`/`DUPLICATE-ITEM`/`UNMATCHED-LEAD`/`DUPLICATE-LEAD`/`DUPLICATE-REASON`/
  `RATIO`; 2 `POLICY`/`SETUP`.
- `kagi-shokunin/corpus/checklist-run.sh:27-28` (HEAD blob `7e5ec98b9e1d0afa…`, worktree MATCH),
  24,697 B, mode `-rwxr-xr-x`; `corpus/checklist.tsv` 11,694 B; `--selftest` proves 34 cases.
- `checklist-execution.md:49-50` — the verdict table; `:113-118` — §6 bounds: "**Nothing schedules this
  gate** … the operability ceiling is therefore unchanged and this round does not claim it."

Axis-by-axis against chousa's C2 predicate (`CHECKLIST_RUN=6/6 DISCRIMINATE=3/3`):

| axis | kagi | chousa C2 | stronger |
|---|---|---|---|
| item→command binding | TSV row + `lead` ERE, **bijection enforced** | `Run:` line inside `SKILL.md`, counted 6/6 | **kagi** |
| unmechanisable items | `by-hand` closed class + unique ≥24-char reason, `DUPLICATE-REASON` defect | not modelled; items 1/3/6 counted from their Run line only (stated limit) | **kagi** |
| floor | `ceil(items/2)` runnable ratio, `RATIO` exit 1 | none | **kagi** |
| exit taxonomy | 0/1/2 with `POLICY`/`SETUP` and 9 named defect lines | 0/1/2 (`PASS`/`FAIL`, denominator refused rc=2) | kagi (wider) |
| single-row read | `--only ID` → `CHECKLIST_ROW: CLEAN\|BROKEN (id=…)` explicitly "not the checklist" | not modelled | **kagi** |
| does a Run line produce the stated outcome? | expected exit + expected last line, **no defect fixtures** | `DISCRIMINATE=3/3` on pass/fail pairs differing in exactly one defect | **chousa** |

Neither dominates. kagi is stronger on declaration completeness, bijection and the honest
runnable/by-hand split; chousa is stronger on the one thing kagi's own §5 concedes it lacks — a fixture
that proves a Run line *discriminates* ("A runnable row verifies the item's **machine-checkable half**
… it does not verify the operator's duty").

Classification: **stronger sibling mechanism on the same axis; NOT contested scope.** kagi's
`PROVINCE.md:5` owns "the domain knowledge, playbooks, error patterns, and checklists **above**" —
i.e. kagi's own credential-hygiene checklist. Chousa's province owns "this lane's own corpus and
gates". Each lane mechanising its own `SKILL.md` checklist is lane-local; no sibling claims chousa's
checklist. Nothing here is absorbable and nothing is absorbed.

### 3.3 kotodama's cold-run is a stronger *verification* mechanism, and a live counterexample

`kotodama-shokunin/reports/round-24/cold-run-a.md` (168 lines, HEAD blob `8e6b71e9f99815bb…`,
worktree MATCH) is a zero-history seat executing that lane's checklist "end-to-end exactly as written".
Its per-item verdicts:

- `:40` — "### Item 1 … **NOT EXECUTABLE** (self-declared; declaration verified accurate)"
- `:52` — "### Item 2 … **EXECUTABLE**, ran clean, one ambiguity"
- `:76` — "### Item 3 … **NOT EXECUTABLE AS WRITTEN** (no operand; machinery exists but is unlinked)"
- `:91` — "### Item 4 … **NOT EXECUTABLE AS WRITTEN** (no operand; backing exists)"

Three of four items in a section titled "Checklist (executable where a tool exists)" do not execute when
a reader with no lane history follows them. That is the exact failure mode chousa's C2 could still have
if its Run lines exist but do not produce the stated outcome — and it is why chousa's
`DISCRIMINATE=3/3` is the load-bearing half of C2, not the `6/6`.

Classification: **stronger sibling mechanism for verifying operability (execution by a fresh-context
reader); NOT contested scope** — kotodama's checklist is its own canon checklist.

---

## 4. False friends — homonyms a shallower scan would misreport

Recorded so a later scan does not re-discover them as overlap. `receipts/false-friends.txt`.

- **lore "forward citation"** — `lore-shokunin/reports/r65-citation-scout.md:1` "Round 65 citation scout
  — forward citation membership boundary"; `r65-simplifier.md:9` "…whether a reversed allied row has
  `source_status(candidate['source_id']) == 'unique'` … it emits `lacks a sourced reciprocal relation`".
  This is an **in-world faction relation's `source_id`** resolving in a fictional source index. No
  relation to academic forward-citation searching. **Unrelated.**
- **kengaku "SNOWBALL"** — `kengaku-shokunin/corpus/knowledge/eval-prior-art-calibration.md:20`
  "prices the repeat-content arm (SNOWBALL +15–20%, still < single-turn FULL)". This is the
  repeat-content arm of Laban et al.'s multi-turn paper, not citation snowballing. **Unrelated.**
- **souji / kotoba / tabi "citation search"** — e.g. `souji-shokunin/.ufo/waves/round-24/w2/W2C2Game.md:42`
  "forward citation at the scored rev … README:516 names `../census/round-24/size-census-lane.txt`,
  which does not exist until ca7fc1c"; `tabi-shokunin/.ufo/waves/round-19/w2/SourceS084.md:76`
  "Literal citation searches found S084 in the round-19 lesson's source-opening Gate". Both mean a
  **literal grep for a row id inside the lane's own files**. **Unrelated.**

## 5. Contested-scope determination against `chousa-shokunin/PROVINCE.md`

| candidate | PROVINCE clause | disposition |
|---|---|---|
| citation searching (C1a) | Owns: "citation chaining and hop resolution; claim-vs-source verification; search-strategy taxonomy" | **no contest** — 0 sibling knowledge entries, 0 TARCiS hits |
| correction/retraction status (C1b) | Owns: "claim-vs-source verification" | **no contest** — 0 sibling knowledge entries; mori holds one capture for an unrelated claim |
| executable checklist (C2) | Owns: "this lane's own corpus and gates" | **no contest** — kagi's checklist is kagi's own; chousa's is chousa's own |
| kagi `checklist-execution` mechanism | kagi PROVINCE:5 "the domain knowledge, playbooks, error patterns, and checklists above" | **lane-local; report only, absorb nothing** |

## 6. Hazards this scan hands to the round (no kill claimed)

1. **Token collision.** Chousa's C2 counter prints `CHECKLIST_RUN=<runnable>/6 DISCRIMINATE=<legs>/3`
   (`chousa-shokunin/corpus/evidence/round81/checklist-run.py:131`, docstring `:31-32`; receipt
   `receipts/chousa-token-collision.txt`) while kagi's runner prints
   `CHECKLIST_RUN: CLEAN (items=N runnable=K by_hand=M failed=0)`. Same token family, different
   grammar (`=` vs `:`). A fleet-wide `grep CHECKLIST_RUN` now returns two lanes with incompatible
   lines. Filenames collide too: `checklist-run.py` (chousa) vs `checklist-run.sh` (kagi). Low
   severity — different lanes, different paths — but a closure reading a grep across the fleet can
   mis-attribute a verdict line.
2. **No sibling precedent for `- Run:`.** `grep -n '^- Run:'` over the 18 sibling `SKILL.md` files →
   grep_rc=1, zero hits (`receipts/run-line-grep.txt`). Chousa's C2 form is
   fleet-first, so there is also no sibling gate that would catch a Run line that exists and does not
   discriminate — the `DISCRIMINATE=3/3` leg is the only guard, and it covers items 2/4/5 only (the
   claim's own stated limit).
3. **kotodama's cold-run counterexample** (§3.3) is the strongest available evidence that a checklist
   section titled "executable" can still be 3/4 non-executable. If the closure wants an independent
   probe of C2 beyond the frozen counter, a zero-history read of `SKILL.md` items 1/3/6 — the three
   legs C2 counts from their Run line alone — is the cheapest one, and it is not this seat's to run.

## 7. Absorbed

**Nothing.** No sibling mechanism, entry, quote, or number was copied into chousa's corpus, SKILL.md,
counters, fixtures or receipts. This file and its `receipts/` are the only artifacts.

## 8. Limits

- Sibling HEADs are a moving target (§0 disclosure); four moved mid-scan.
- One cited row (tabi `PROVINCE.md:186`) was **dropped** as uncommitted worktree bytes (§0).
- The scan reads text; it does not execute any sibling gate. kagi's `checklist-run.sh` was **not** run
  — its claimed `items=16 runnable=9 by_hand=7` is quoted from kagi's own SKILL.md registry row and
  knowledge entry, not re-measured here.
- The fleet-root `.ufo/` tree was excluded from the population (it is not a sibling repo); the one
  TARCiS mention found there is reported in §1 for completeness and marked as not a sibling hit.
- **Self-correction, disclosed.** My first `- Run:` sweep built its path list as
  `<space-joined repos>/SKILL.md`, so only the last repo got the suffix and grep recursed the other 19
  repo trees, returning 40 hits from reports and `.ufo/waves/`. That output is discarded. The corrected
  command names all 18 existing `SKILL.md` paths explicitly and returns grep_rc=1
  (`receipts/run-line-grep.txt`). The finding (zero `- Run:` lines in any sibling `SKILL.md`) is the
  corrected one; the malformed run is recorded here rather than dropped.
- `corpus/evidence/round81/egress-approval.md` was not needed: no URL was fetched.

## 9. Verdicts

VERDICT: R81ConnectorSiblings C1 depth n/a — no counter run by this seat; the scan finds zero sibling knowledge entries on citation searching (TARCiS grep rc=1 across all 20 repos) and zero on correction/retraction status, so C1's ground is uncontested and unduplicated in the sibling population, with one fleet-root round-12 lead note and one mori capture naming the Retraction Watch-backed `is_retracted` field recorded as scope notes only.
VERDICT: R81ConnectorSiblings C2 operability n/a — no counter run by this seat; kagi holds a stronger executable-checklist mechanism (`corpus/checklist.tsv` + `checklist-run.sh`, lead-ERE bijection, `ceil(items/2)` floor, 0/1/2 taxonomy) that is lane-local and not contested, while chousa's fixture-discrimination leg is stronger than kagi's, and no sibling `SKILL.md` carries a single `- Run:` line (grep rc=1).
