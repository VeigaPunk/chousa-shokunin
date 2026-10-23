# RevC3Set — audit of `corpus/evidence/round34/audit-set.json` (43 checks)

Scope: is the committed 43-check set the right calibration surface for "the lane's
round-34 self-assessment"? Seat of `chousa-r34-w2a2`, wave 2a2, 2026-10-23.
All work read-only on the lane; experiments in
`/fast/scratch/hyaku/chousa-r34-a2/w2/RevC3Set/lane` (clone of the lane repo at
frozen tip `707da8184a0fc4d10ab3f17271556cdf364f0af5`). Lane gate pinned:
`sha256sum tools/research-gate.sh` = `a6307edf687ac0fb…2995b` (matches spec prefix).

## Re-derived baseline (the committed count reproduces)

```
git clone -q $LANE lane && git -C lane checkout -q 707da818…   # clean
cd lane && python3 corpus/evidence/round34/self-audit.py        # exit 0
→ 43× "AUDIT id=… ok", SELF_AUDIT_MISMATCHES=0, SELF_AUDIT_UNDISPOSITIONED=0
```
Receipt: `.ufo/waves/round-34/w2a2/RevC3Set/audit-rerun-707da818.txt`
(sha256 `b709781c949b…`), byte-identical in result to the committed
`.ufo/waves/round-34/measure-a2/audit-first-run.txt`. The committed negative
control (`audit-negative-control.txt`, 2 injected lies → 2 counted) is also
committed and its mechanism re-derives: `git_commit` deadbeef prefix fails,
`sha256` zero digest fails. **K=0/0 is an honest, reproducible measurement of
this set against this tree.** The question is only whether the set measures
much.

## What the 43 checks are

| kind | n | ids |
|---|---|---|
| git_commit | 12 | commit-b8053900, 70feb5ea, ef16afb1, f20aeaa7, a92b9f43, 3026a4e5, 934d7cb7, 98af778c, bf7c931a, 7c7eb3a6, 2592f9da, fe0f22e0 |
| sha256 | 4 | gate-head-digest, c1v3-counter-digest, c2-counter-digest, audit-tool-digest |
| receipt_binding | 4 | bind-c1v3-s3601, bind-c1v3-s3602, bind-c2-before-5011, bind-c2-after-5033 |
| path | 20 | path-00..16, shonen-00..02 |
| grep_assert | 3 | skill-tally-256, skill-tally-253-stale, log-r34a1-lesson |

`python3 -c 'len(checks)'` → 43. `audit-dispositions.md` committed empty
(sha256 `e3b0c442…`), so the `UNDISPOSITIONED=0` arm requires K=0.

## Findings

### F1 — structural: the tool audits the working tree, not committed bytes
`self-audit.py` kinds `path`/`sha256`/`grep_assert` and the receipt half of
`receipt_binding` all read `os.path`/`open()` on the checked-out tree
(`self-audit.py:85-117`); only `git_commit` and the *gate* half of
`receipt_binding` (`git show <commit>:…`, :44) touch committed objects.
Demonstrated on the scratch clone (committed bytes identical throughout):
appending an uncommitted `PASS (253 cases)` line to `SKILL.md` →
`AUDIT id=skill-tally-253-stale MISMATCH`, `MISMATCHES=1 UNDISPOSITIONED=1`;
`git checkout --` restores 0/0. Consequence: C3's K conflates repo state with
checkout hygiene — on a dirty lane tree K≠0 while committed bytes are perfect,
and conversely the lane working tree at `fe3db76` (post-freeze commit) passes
because the gate/counters are unchanged. No `git status`-cleanliness or
HEAD-digest check exists to bound this. Not a kill of P3 (the predicate says
"on the landed lane revision" and the committed receipt was taken on a clean
tree [INFERENCE]) but the set's guarantee is weaker than "matches committed
bytes".

### F2 — tautological / near-tautological checks (existence the round itself guarantees)
- All 12 `git_commit` checks can never fail at a revision whose history contains
  the round: every cited prefix was minted by the round's own commits. They
  detect only history rewrite/shallow clones — near-zero discrimination.
  They do NOT check that the cited commits contain what the citation claims
  (e.g. `commit-fe0f22e0` passes even if fe0f22e0 were an empty commit).
- `path-04` (`self-audit.py` exists) is self-referential: the tool's own file is
  enumerated by a run of that same file; it can only fail when the tool is run
  from a foreign tree. `path-03` (c2-count.py) is nearly the same — its content
  is what matters, and only `c2-counter-digest` pins that.
- `shonen-00..02` are *file-exists* checks on three round-25 evidence files
  (`corpus/evidence/round25-*.log`, `corpus/knowledge/metadata-screen-r25.md`)
  that have existed for ~9 rounds. Renaming them would fail the check, but no
  evidence suggests they were ever at risk; they verify SHONEN's oldest, most
  stable pointers, not round-34's new claims.
- `skill-tally-253-stale` (absence of `PASS (253 cases)` in SKILL.md): the
  string it hunts was overwritten in the same commit (`fe0f22e0`) that wrote
  the check — self-sealing within the attempt. Verified: `git show
  98af778c:SKILL.md` has `PASS (253 cases)` at :77-84; tip does not.

### F3 — self-sealing expects (the round pinned its own fresh output)
All four sha256 expects are values the round itself produced this attempt:
gate `a6307edf…` (landed `fe0f22e0`), counters (landed `f20aeaa7`/`7c7eb3a6`),
and `audit-tool-digest` — the tool pinning its own bytes (landed `0af0844c`
with the set). Each expect was necessarily correct at write time; the checks
only detect *post-landing silent edits*. That is real but narrow value — drift
detection, not calibration of the self-assessment.

### F4 — the highest-value surface is essentially unaudited
The claim text ("SCORECARD rows, LOG entry, SKILL.md tallies, SHONEN evidence
pointers", claims-a2.md) vs. what the set covers:

- **SCORECARD.md: zero checks.** The round's scoreboard rows — `DEADZONE_MATCH=
  21/37 → 37/37`, `PASS 256`, `43 checks`, C1's `unverified` verdict (SCORECARD
  :1956-57, :1927) — are the densest report-bound numbers in the repo and none
  is asserted. `grep -c 'SCORECARD' audit-set.json` → 0.
- **Receipt coverage 4/9.** Committed receipts under `measure/`+`measure-a2/`:
  c1v3-s3601, s3602, **s3603-utf8 (unbound)**, c2-before-s5011, **s5023
  (unbound)**, c2-after-**s5011 (unbound)**, s5023, s5033, **s5047 (unbound)**.
  SCORECARD :1956 cites all four c2-after seeds; the set binds only s5033.
  Verified each unbound receipt parses and *would* bind (`gate_sha256` fields
  dumped: c2-after-s5011/5023/5047 all pin `a6307edf…`; c2-before-s5023 pins
  `772a1d8e…`), so the gap is coverage, not a live mismatch — but a byte-edit
  to any unbound receipt (e.g. flipping `predicate_holds` on a `c2-before`
  receipt, currently `False` = the do-nothing evidence) is invisible to K.
- **Frozen-design content unpinned.** `claims.md` (path-00) and `claims-a2.md`
  (path-01) are existence-checked only. `claims-a2.md` *is the freeze* — its
  digest `aaeb375e…` and `claims.md` `4823e5e5…` appear nowhere in the set or
  repo (`grep -rn` over corpus/.ufo/LOG/SCORECARD/SKILL → no hits), and
  `audit-set.json`'s own digest is pinned nowhere either (it cannot self-pin;
  nothing external pins it). A silent post-freeze edit to the claims text
  leaves K=0.
- **LOG.md: one regex.** `log-r34a1-lesson` asserts `corpus/lessons/round-34\.md`
  appears in LOG.md — it does (LOG :1280 and :1296-1299 both contain it; the
  check is satisfied by the attempt-1 entry alone). The attempt-2 LOG block
  (LOG :1284-1302) — C2's 21/37→37/37 numbers, `0af0844c`, the C3 paragraph —
  is unasserted. Commit `0af0844c` is cited in LOG :1293 but absent from the
  12 commit checks (the set cannot self-pin its own landing commit; appendable).
- **SHONEN pointers: 3 of the round-25 set.** SHONEN's cited evidence also
  includes `.ufo/waves/round-25/build/ConnectorMetaSiblings.md` (SHONEN :12),
  `corpus/fixtures/archives-r9/` (:8) — both exist, neither checked. SHONEN
  has zero round-34 text (`grep -n 'round-34\|r34' SHONEN.md` → empty), so
  "SHONEN evidence pointers" coverage is entirely round-25 nostalgia.
- **Attempt-2 evidence receipts unchecked.** `.ufo/waves/round-34/measure-a2/
  audit-first-run.txt`, `audit-negative-control.txt`, `deadzone-fixture-vs-
  gates.txt`, `selftest-a2.log`, and `corpus/knowledge/dead-zone-pcre-r34.md`
  (committed `fce3119`, cited by LOG :1296 and SCORECARD :1966) — all exist,
  none path-checked. `grep 'audit-first-run\|deadzone\|dead-zone-pcre'`
  audit-set.json → exit 1.
- **Wave registries unchecked.** `.ufo/waves/round-34/w1-spec.json`,
  `w1/swarm-registry.json`, and post-freeze `w2a2-spec/plan/taskcall.json` —
  none named in the set (w2a2 files landed `bd8c8bd`/`fe3db76`, after the set
  froze at `0af0844`; appendable only).
- **QUALITY.md / SOURCES.md unasserted** despite LOG citing QUALITY 42-44 and
  S065's re-open; grep over the set → absent.

### F5 — grep_assert can assert presence, never correctness
`skill-tally-256` proves the *string* `PASS (256 cases)` occurs in SKILL.md
(:77-84; :92 contains it inside the historical-tally paragraph too). The tool
has no count kind, so SKILL.md's "256" is never compared to the selftest's
actual case count (`measure-a2/battery/selftest.cases` / `selftest-a2.log` are
committed but unchecked). A wrong-at-birth tally (text-level lie) would pass.
Same class: nothing binds `DEADZONE_MATCH`/`SELF_AUDIT_MISMATCHES` strings in
SCORECARD to the receipts they claim to summarize. 0/0 under this set is
*believable but shallow*: it certifies existence and a handful of digests, not
the arithmetic of the self-assessment.

## Proposed appends (≤5; expects computed from committed bytes at 707da818, do NOT append — L1's call)

```json
{"id":"claims-a2-digest","kind":"sha256","path":"corpus/evidence/round34/claims-a2.md",
 "expect":"aaeb375e51d036d8a80af1e2bd0e99b592a2ac6f10691c5ede2eee50b0b19cfb"}
{"id":"claims-v3-digest","kind":"sha256","path":"corpus/evidence/round34/claims.md",
 "expect":"4823e5e53024e40e9fd74d6b333935df4493c2517dd4585f35e7dc8b9ea061a0"}
{"id":"scorecard-c3-count","kind":"grep_assert","path":"SCORECARD.md",
 "pattern":"SELF_AUDIT_MISMATCHES=0","present":true}
{"id":"bind-c2-after-5047","kind":"receipt_binding",
 "receipt":".ufo/waves/round-34/measure-a2/c2-after-s5047.json","commit":"fe0f22e0"}
{"id":"bind-c1v3-s3603","kind":"receipt_binding",
 "receipt":".ufo/waves/round-34/measure/c1v3-s3603-utf8.json","commit":"934d7cb7"}
```
Derivations: `git show 707da818:claims-a2.md|sha256sum` → aaeb375e…;
`claims.md` → 4823e5e5…; SCORECARD.md :1957 contains `SELF_AUDIT_MISMATCHES=0`
(1 hit); `git show fe0f22e0:tools/research-gate.sh|sha256sum` → a6307edf… =
receipt s5047 gate_sha256 (37/37, holds); `git show 934d7cb7:tools/research-
gate.sh` → 772a1d8e… = receipt s3603-utf8 gate_sha256 (42/42 UTF-8, holds).
All five pass on the tip clone if appended today. Runners-up: path checks for
`measure-a2/audit-first-run.txt` + `corpus/knowledge/dead-zone-pcre-r34.md`,
receipt_binding for c2-before-s5023 (the second do-nothing witness, pins
772a1d8e at bf7c931a), git_commit `0af0844c`.

## Verdict

The set is *valid* — 43/43 pass on the pinned tip, K=0/0 re-derives byte-for-
byte, the negative control is committed, and no expect is stale — but it is a
shallow calibration surface for the claim's stated target: 32/43 checks are
existence/prefix-resolution, 3 grep_asserts are literal-string presence, the
single strongest kind (receipt_binding) covers 4 of 9 committed measurement
receipts, and the artifact carrying the round's actual self-assessment
(SCORECARD.md) plus both frozen claims documents' content go unasserted. K=0
is believable; it is also what a much weaker audit would print. The five
appends above close the largest holes at zero new machinery.
Report: .ufo/waves/round-34/w2a2/RevC3Set.md
