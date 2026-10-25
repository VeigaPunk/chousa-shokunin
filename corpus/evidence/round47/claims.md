# Round 47 — frozen claims (chousa)

author: chousa L1 (in-session L1, hyaku run 6)
date: 2026-10-25
base: `9a9f94dbcb010eca6636886e53950f38ca806329` (round-46 tip plus its
non-author closure `corpus/lessons/round-46-verifier-spotcheck.md`)
freeze: this commit (claims, the three counters, the C1 fixtures and the
controls; no claim work is in it)

No external fetch: the fetch-scope L0 `8d77e6c1` is still open. Every capture
this round reads is on disk (campaign capture cache
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`, file =
`sha256(url)[:24].txt`).
Round tag (QUALITY 64): C1 plumbing, C2 plumbing, C3 ground.

Three claims, three axes, each verifiable without the others. C1 works the
lowest non-retired axis (operability, 3/10 — `SCORECARD.md:7`). C1 is the
round-46 lesson's first named limit (entailment, the round-45 D7 class) and the
round-47 planned candidate; C2 is the second named limit (mention, not
dependence) plus closure routed defects 2 and 4; C3 is the third named limit
(anchor cells, routed defect 5) carried by one assimilation theme under §10,
whose flip condition the round-46 Gate block set.

## R47-C1 — operability — the inference check refuses polarity flips

The round-46 tool checks that an Inference bullet's quoted phrases and figures
are PRESENT in the spans it cites; a bullet that strings correct tokens into an
assertion of the opposite passes (`.ufo/waves/round-46/w2/CritC1D7.md` §1,
lesson round 46 mistake 2). This claim adds one mechanical leg, the
opposite-token probe, and nothing that pretends to judge meaning.

Rule the tool must implement (same sentence as the counter's docstring):
for a phrase located in a cited span, if the span NEGATES it (a negator inside
the phrase, or among the three span words before it), a bullet whose own
unquoted words use one of the phrase's scope words (same five-letter stem)
with no negator in the three words before or two after it is refused; if the
span does NOT negate it, a bullet whose own words put a negator in the three
words before one of the phrase's content words is refused; a figure grounded
by a counts key whose name carries `no`/`not`/`none`/`without` must be
followed by a negator in the bullet's next four words, and one whose key does
not must not be. The finding code is `INF_POLARITY_FLIP`.

Predicate (one sentence): `tools/inference-ground.py`, run by
`python3 corpus/evidence/round47/c1-count.py`, exits 0 on each of the three
`positive-*.md` fixtures and exits 1 with an `INF_POLARITY_FLIP` line on each of
the three `junk-*.md` fixtures of `corpus/fixtures/inference-ground-r47/`,
passes the neutral-name CANARY, and the round-46 counter still prints
`C1=PASS` for it while both round-46 entries still exit 0 under it.

* Counting command: `python3 corpus/evidence/round47/c1-count.py`
* Before (`controls/c1-before.txt`, base tool):
  `POSITIVE_PASS=3/3 JUNK_KILLED=0/3 CANARY=fail R46_COUNTER=pass
  R46_ENTRIES=2/2 C1=FAIL` exit 1.
* Target: `POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass
  R46_ENTRIES=2/2 C1=PASS` exit 0.
* Controls (`controls/c1-controls.txt`): the round-46 tool scores
  `JUNK_KILLED=0/3`; an always-exit-1 tool `POSITIVE_PASS=0/3
  R46_COUNTER=fail`; a negator-word refuser (`controls/neg-word-refuser.py`)
  `POSITIVE_PASS=1/3 R46_ENTRIES=0/2`. All exit 1.
* Kill rule: any leg below target, or a fixture changed after this freeze
  (`FIXTURES_CHANGED=`), fails the claim as declared.
* Named limit, declared now: the probe is lexical — a flip expressed through a
  synonym or antonym with a different stem (`revised` vs `edited`), or through
  scope the three-word window does not reach, still passes.
* Tag: plumbing. Capability row: "polarity probe in the inference check".

## R47-C2 — calibration — the gate registry agrees with the tree its checks depend on

The round-46 set is mention-based: a gate named only by a QUALITY `Check:` line
or read by another gate is invisible to it (`.ufo/waves/round-46/w2/RevC2TagCount.md`),
its floor `ENTRY_POINTS ≥ 71` was prose only (closure routed defect 2), and a
path anywhere in an eight-pipe row with `exit` anywhere registered (routed
defect 4). The lane's self-assessment — "every gate is registered" — is
measured against observed repo state as a mismatch count.

Predicate: `python3 corpus/evidence/round47/c2-count.py` prints
`MISMATCHES=0` and `C2=PASS` (exit 0) with `ENTRY_POINTS ≥ FLOOR`, where the
entry-point set is the round-46 set (A–C, imported from the pinned round-46
counter) plus (D) every existing `*.py`/`*.sh` path an entry point's source
names, closed under that relation, plus (E) every existing `*.py`/`*.sh` path
`corpus/QUALITY.md` or `SKILL.md` outside `## Gates` names; MISMATCHES =
UNREGISTERED (no Gates row names the path in its `entry` cell, with an exit
code in its `verdict map` cell) + DANGLING (a Gates row names a
`*.py`/`*.sh` path the tree does not hold); FLOOR is the freeze-tree
ENTRY_POINTS, enforced in code.

* Counting command: `python3 corpus/evidence/round47/c2-count.py --list`
* Before (`controls/c2-before.txt`): freeze tree and bare base tree, both
  exit 1 with `MISMATCHES>0`.
* Target: `MISMATCHES=0 C2=PASS` exit 0, `ENTRY_POINTS ≥ FLOOR`.
* Controls (`controls/c2-controls.txt`): the round-46 counter prints
  `C2=PASS` on the base tree (the cheap gate this claim's set exposes); the
  round-47 counter on that same tree prints `C2=FAIL`; deleting every
  check-named leg shrinks the set below FLOOR and fails.
* Kill rule: `MISMATCHES>0`, `ENTRY_POINTS < FLOOR`, or a changed round-46
  instrument (`R46_INSTRUMENT=changed`) fails the claim as declared.
* Named limit: row truth (does the verdict map describe the script?) stays a
  reader's check; an entry cell can still name a script that is not a gate.
* Tag: plumbing.

## R47-C3 — depth — the claim-support test, re-grounded by document

Theme (assimilation §10, one theme): what a support test is, how it is
applied, and how reliable it is. Staged package
`/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/`
`claim-support-test-r37.md` (staged S097–S099) and
`claim-support-test-r37-amendment-2026-10-23.md` (staged S113–S115); round 46
refused the amendment until its base entry is adopted with its own rows and
its quotes sit in committed spans (`corpus/lessons/round-46.md` `## Gate`).
Ids bind by document (URL equality): S097 → held S085, S098 → S090,
S099 → S091, S113 → S092, S114 → S093, S115 → S094. Four of the six URLs are
rows of this lane's absent-defect-register slice (register S093, S094, S108,
S110) and are quarantined until hand-checked this round.

Predicate: the sentence in `corpus/evidence/round47/c3-count.py`'s
docstring (entries, six document bindings, ≥12 capture-bound spans with
context and ≥2 per id, ids within S079–S094, every `char N` of the anchor
cells of S085 and S090–S094 equal to a located quote offset, both entries
exit 0 under `tools/inference-ground.py`, four quarantine verdict lines with
no `absent` row adopted).

* Counting command: `python3 corpus/evidence/round47/c3-count.py`
  (and `--lane-only`)
* Before (`controls/c3-before.txt`): `ENTRIES=0/2 CITES_BOUND=0/6
  ANCHOR_BOUND=0/6 QUARANTINE_VERDICTS=0/4 C3=FAIL` exit 1 (the held S085
  anchor names char 2349, which is no quote offset).
* Target: every leg full, `C3=PASS` exit 0 in both modes
  (`CAPTURE_BOUND=skipped` under `--lane-only`).
* Controls (`controls/c3-controls.txt`): the staged entries copied unchanged
  are refused (`REF_ID_UNBOUND>0`, `CITES_BOUND=0/6`); a self-consistent
  manifest with invented digests passes no default-mode `CAPTURE_BOUND`.
* Kill rule: any leg below target in either mode fails the claim as
  declared. A staged sentence the captures contradict is corrected in the
  entry and recorded as a mistake; a register row hand-checked `absent` is
  refused, never adopted.
* Tag: ground.

## Admission rule

Each claim is judged on the counter, kill rule and predicate declared here. A
rule changed after any seat has scored is not this claim's rule. A round is
admitted only when every claim verifies and no axis is harmed; every verdict is
reported.
