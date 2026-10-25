# ExecPerturbPkg — round 49 w2 C1 replay-limit generalization probe (seat report)

seat: ExecPerturbPkg (leaf executor, godspeed)
date: 2026-10-25
lane: /home/vgpnk/Projects/shokunin/chousa-shokunin (tip 87e93353; tool sha 4b995dbc… = measure-after @ 4ce61fc)
scope: attack the W1 C1 replay limit (CritForgeC1) with a PERTURBED staged
package — renumber two staged ids, swap two URLs, add a novel row cited by an
entry, add an escaped pipe to an appended row — run the real
`tools/assimilate-rows.py`, and verify outputs by independent reasoning.
files changed: only this report. No installs (RULES.md read; nothing needed).

## 1. Inputs and perturbations (scratch /dev/shm/chousa-r49-ExecPerturbPkg)

Base registry: `git -C <lane> show 414a2ec6cde05a921dbdd9e02e7ae56b0db647ef:corpus/SOURCES.md`
(95 rows S001–S095; max 95). Staged package: `…/merge/chousa/SOURCES.append.md`;
entries: `aggregator-vs-source-r36.md`, `citation-count-semantics-r37.md`.
Perturbations applied to copies (probe_gen.py; staged rows 114→115):

1. renumber staged ids S101→S201, S102→S202 (row id cells + every S101/S102
   token in the citation-count entry) — breaks any golden derived from S101/S102;
2. swap source URLs of staged S091 and S098: S091 now carries
   `https://aclanthology.org/2026.findings-acl.19.pdf` == base row S090's URL,
   so the cited S091 must flip to HELD→S090; S098 (uncited) becomes inert;
3. add novel staged row S310 (`https://novel.example/page`), cited by the
   aggregator entry (source line + prose) — must append as S104;
4. escaped pipe `\|` in S310's anchor cell (`section 2 \| 3, char 40`) —
   must be rewritten to ` / ` and logged;
also: stale pass-through token "S102" left in the citation-count entry, giving
the simultaneity chain S202→S103→S101 in one text (S103 is still staged).

## 2. Tool run (real adopter, perturbed inputs)

```
$ cd <lane> && python3 tools/assimilate-rows.py --staged S/staged.md --knowledge S/know \
    --registry S/registry-SOURCES.md --opened 2026-10-25 --out S/out \
    --entry corpus/knowledge/aggregator-vs-source-r36.md \
    --entry corpus/knowledge/citation-count-semantics-r37.md
COLLISIONS=14
CITED=10 APPEND=9 HELD=1
EXIT=0
```
(`S` = /dev/shm/chousa-r49-ExecPerturbPkg; tool sha256 `4b995dbc2e950613a632c83dba068e932396c1cf1d6a44dc1255f1c4f04abc32`.)

## 3. Independent verification (verify.py, written from scratch — no c1-count imports)

Recomputes the mapping from the files: url_of (census normalisation), staged
rows (unescaped-pipe split), registry rows under `## Registry`, cited = entry
tokens ∩ staged ids, expected lane id = base row with that URL else next free
from max, ascending staged-id order; byte-compares rewritten entries against a
single `re.sub` pass; builds the scratch mirror like c1-count `make_mirror`
(corpus from `git archive BASE_REV`, other tracked paths empty placeholders,
appended rows spliced after the last Registry row, entries placed) and runs
`sources-census.sh validate --file`.

```
$ python3 S/verify.py
BASE_MAX=95 CITED=10 APPEND=9 HELD=1 COLLISIONS=14
RENUMBER_BY_DOC=10/10 CONTIGUOUS=yes SIMULTANEOUS=2/2 CENSUS=ok
VERIFY=PASS
EXIT=0
```

Observable artifacts (out/):
- renumber.tsv (10 rows, ascending): S087→S096, S088→S097, S089→S098,
  `S091→S090 held`, S092→S099, S100→S100, S103→S101, S201→S102, S202→S103,
  S310→S104; URL column equals each staged row's current normalised URL.
- append.md: exactly 9 rows, ids S096–S104 (contiguous from base max), each
  11 cells, status `mined`, opened 2026-10-25, recheck census-valid (e.g. `90d`),
  used-by exactly the citing entry(s); S104 anchor reads `section 2 / 3, char 40`
  (pipe rewritten); no `\|` remains.
- stripped.tsv logs `S104 cell6-pipe section 2 \| 3, char 40`, recheck
  reductions and opened/used-by replacements.
- collisions: S082–S095 (14) = independent grep intersection (0–3-space pattern).
- Rewritten entries byte-equal the single-pass reference: aggregator gets
  S091→S090, S310→S104, S087–S092→S096–S099; citation-count gets S201→S102,
  S202→S103, S103→S101, and the stale literal `S102` passes through unchanged.
  The chain S202→S103→S101 would chain to S101 under a double pass; byte
  equality proves one simultaneous pass.

## 4. Frozen counter at tip (still passes)

```
$ python3 corpus/evidence/round49/c1-count.py
… SET_A/B/C PASS, GUARD PASS, PIPE PASS, SETS_PASS=3/3, C1=PASS, EXIT=0
```
(tool sha line matches measure-after @ 4ce61fc; no counter/claim bytes changed).

## 5. What this establishes

The real tool derives every artifact from its actual inputs: every perturbed
input changed the outputs, and all of them match the independent by-document
expectation (including a held flip via URL identity, non-contiguous staged ids
S201/S202/S310, and an escaped-pipe rewrite). A canned golden-replay tool
(CritForgeC1's cheapest.py style) would fail this package: its constants were
captured from the unperturbed package (renumber S101/S102 rows, 10-row
append.md, no S104, un-swapped URLs), so its copied artifacts would not match
the derived expectations above — the perturb leg is the smallest safe
correction the W1 critic proposed, and the real tool passes it. The frozen
counter remains a conformance check on fixed inputs (QUALITY 72 note stands);
this probe shows the *real* mechanism is not a replay.

Risks: probe used a synthetic URL for S310 (not a live source; no fetch, per
L0); the stale-URL text in the rewritten aggregator S091 source line is an
intended artefact of testing id-token substitution, not a repo defect.

VERDICT: C1 replay limit — holds — the real assimilate-rows.py passes the
perturbed-package generalization probe (by-document renumber, contiguity,
simultaneous substitution, escaped-pipe rewrite, mirror census all verify
independently), so the W1 replay hole is a counter limitation, not a tool flaw.
