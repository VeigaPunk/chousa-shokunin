# ReviewR4RoleMix — independent r39 role count; does routed R4 reproduce from committed bytes?

seat: ReviewR4RoleMix (leaf L2, chousa round 40, wave 1)
assigned attack: count the r39 roles independently from `w1-spec.json` and `w1-plan.json`,
compare with the committed r39 report and the verifier spot-check, and decide whether the
routed R4 mismatch reproduces from committed bytes.
lane root: /home/vgpnk/Projects/shokunin/chousa-shokunin (all paths absolute below unless
marked lane-relative)
disposition under test: `corpus/evidence/round40/routed-defect-dispositions.json:20-29` →
R4 `"status": "not-reproduced"`, decision “Committed r39 spec, plan, and report agree on
reviewer 6 and revenger 2 (32 seats); the spot-check's reviewer 8 and revenger 0 assertion
does not match those artifacts.”
contrary assertion: `corpus/lessons/round-39-verifier-spotcheck.md:74` — “report's wave role
mix (reviewer 6 / revenger 2) does not match the validated spec (`w1-spec.json`: reviewer 8 /
revenger 0; totals 32 both).”

## Verdict

**The R4 mismatch does NOT reproduce from committed bytes; the `not-reproduced` disposition
is correct.** Four independent representations of the same 32-seat r39 wave agree exactly:
spec `items[].role`, plan `tasks[].agent`, plan `registry.members[].role`, and the committed
fleet report's mix line — all `reviewer 6 / revenger 2`, total 32, elementwise identical over
all ten roles. No committed revision of the r39 spec or plan, on any ref, carries
`reviewer 8 / revenger 0`; the spot-check's contrary pair is unreproducible from the bytes it
cites. The disposition, the R4 erratum (`corpus/evidence/round39/claims.md:199`), and the
round-40 SCORECARD R4 line are accurate as written.

Separately, the frozen counter `c2-count.py` under-implements the frozen R4 code condition
for the **report** leg: it substring-matches two role counts instead of re-deriving the
report's mix, so it cannot detect report drift. This is a calibration finding about the
discriminator (F1 below), not a falsification of the disposition — the committed report
does satisfy the stronger condition, which I re-derived elementwise.

## Evidence 1 — canonical reproducer (committed blobs only)

Command (run from the lane root; reads `git show HEAD:` for spec/plan/spot-check and the
fleet repo's committed report, so it is independent of any dirty worktree):

```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 - <<'PY'
import subprocess, json, collections, re
lane="/home/vgpnk/Projects/shokunin/chousa-shokunin"
fleet="/home/vgpnk/Projects/shokunin"
def blob(repo,p): return subprocess.run(["git","-C",repo,"show",f"HEAD:{p}"],capture_output=True,text=True,check=True).stdout
spec=json.loads(blob(lane,".ufo/waves/round-39/w1-spec.json"))
plan=json.loads(blob(lane,".ufo/waves/round-39/w1-plan.json"))
s=collections.Counter(i["role"] for i in spec["items"])
p=collections.Counter(t["agent"] for t in plan["tasks"])
rep=blob(fleet,".ufo/reports/round-39/chousa.md")
spot=blob(lane,"corpus/lessons/round-39-verifier-spotcheck.md")
i=rep.index("role mix"); seg=rep[i:i+260].replace("\n"," ")
r=collections.Counter({k:int(v) for k,v in re.findall(r"([a-z][a-z-]*) (\d+)", seg)})
print("spec n=%d:"%len(spec["items"]), dict(sorted(s.items())))
print("plan n=%d:"%len(plan["tasks"]), dict(sorted(p.items())))
print("spec==plan per role:", s==p)
print("spec==plan per name:", {x['name']:x['role'] for x in spec['items']}=={t['name']:t['agent'] for t in plan['tasks']})
print("report mix text:", seg[:192])
print("report mix == spec mix:", r==s, "| totals:", sum(r.values()), sum(s.values()))
print("spotcheck R4:", [l for l in spot.splitlines() if l.startswith("- **R4")][0])
PY
```

Output (verbatim):

```
spec n=32: {'connector': 1, 'critic': 5, 'executor': 6, 'mutation-tester': 3, 'revenger': 2, 'reviewer': 6, 'scout': 3, 'scribe': 3, 'sentinel': 2, 'simplifier': 1}
plan n=32: {'connector': 1, 'critic': 5, 'executor': 6, 'mutation-tester': 3, 'revenger': 2, 'reviewer': 6, 'scout': 3, 'scribe': 3, 'sentinel': 2, 'simplifier': 1}
spec==plan per role: True
spec==plan per name: True
report mix text: role mix executor 6 / reviewer 6 / critic 5 / scout 3 / scribe 3 / mutation-tester 3 / sentinel 2 / revenger 2 / connector 1 / simplifier 1), **0 dispatched / 0 dead this seat** (host mapping:
report mix == spec mix: True | totals: 32 32
spotcheck R4: - **R4 (minor):** report's wave role mix (reviewer 6 / revenger 2) does not match the validated spec (`w1-spec.json`: reviewer 8 / revenger 0; totals 32 both).
```

This is stronger than the disposition's wording: agreement holds not only for reviewer 6 /
revenger 2 but for all ten role counts and for every seat name's role.

## Evidence 2 — no committed revision ever carries 8/0

Command (git blob read at every commit that contains the path, plus the r39 base commit):

```
git show <rev>:.ufo/waves/round-39/{w1-spec.json,w1-plan.json} | count items[].role / tasks[].agent
git cat-file -e 8c7c867b66e103712ae33e1d076786f50dd3239e:.ufo/waves/round-39/w1-spec.json
```

Output:

```
6d914e951 | w1-spec.json: n=32 reviewer=6 revenger=2; w1-plan.json: n=32 reviewer=6 revenger=2
35e10b9a7 | w1-spec.json: n=32 reviewer=6 revenger=2; w1-plan.json: n=32 reviewer=6 revenger=2
7180206b0 | w1-spec.json: n=32 reviewer=6 revenger=2; w1-plan.json: n=32 reviewer=6 revenger=2
fatal: path '.ufo/waves/round-39/w1-spec.json' exists on disk, but not in '8c7c867b66e103712ae33e1d076786f50dd3239e'
```

`git log --all -- .ufo/waves/round-39/` names exactly those three commits (6d914e9 authored
the wave; 35e10b9 and 7180206 are the other objects containing the path), and the tip commits
`691d264` (lane tip when the spot-check was written) and `6bc90e0` (current lane HEAD) both
read 6/2 as well. `BASE39 8c7c867` predates the wave, so there is no earlier committed r39
spec to conflict with.

Sweeps (read-only, current committed trees):
- lane sweep: all 5258 tracked `*.json` files scanned, plus every
  `.ufo/waves/**/*.json` (258 wave JSONs carrying item/task lists): **exactly one** file has
  reviewer 8 — `.ufo/waves/round-33/w2-spec.json`, 34 seats
  (`critic 2, executor 15, mutation-tester 5, reviewer 8, scout 3, sentinel 1`, no revenger
  field). Wrong round and wrong total (34 ≠ 32), so it cannot be the cited `w1-spec.json`.
- fleet `/home/vgpnk/Projects/shokunin/.ufo/waves/` scanned recursively (45 JSON files with
  item/task lists): no `round-39/` directory and no 32-seat spec with reviewer 8. Fleet
  reports that state “reviewer 8” belong to other rounds (13, 14, 30, 31, 33, 44, 49, 61, 63,
  65), never r39.
- The plan's internal `registry.members` (32 entries) matches the spec seat names and roles
  with zero differences, so the validator-side registry cannot be the source either.

## Evidence 3 — the report predates the spot-check and was never rewritten

- `corpus/…` fleet report history: exactly one commit, `f713ee1` at 2026-10-24 03:17:42,
  subject “round-39: chousa report”; no later edit. Working-tree blob `ce2b87a0…` equals
  `HEAD:.ufo/reports/round-39/chousa.md`; `git status --porcelain` empty.
- r39 spec/plan commit `6d914e9` at 03:15:48; spot-check commit `691d264` at 03:27:55.
  The spot-check's assertion was therefore already contradicted by committed bytes
  (spec, plan, report) that existed ~10–12 minutes before it was written. There was no
  post-hoc reconciliation of the report to the spec.

## Evidence 4 — counter state

`python3 corpus/evidence/round40/c2-count.py` →

```
R2_DISPOSITION=ok
R3_DISPOSITION=ok
R4_DISPOSITION=ok
R5_DISPOSITION=ok
R39_CALIBRATION_DISPOSITIONS=4/4
```

exit 0. The frozen counter bytes (`2a9b0c86…`, introduced at freeze commit `6c01a41`,
unchanged since) and the disposition bytes (`eb6d32b5…`, introduced `d164f88`, unchanged
since) are the bytes I ran. All six C2 inputs are clean and equal to their HEAD blobs
(worktree = HEAD, `git status --porcelain` empty for each):
spec `3a1f47ed…`, plan `730e2dae…`, spot-check `c1921178…`, dispositions `eb6d32b5…`,
counter `2a9b0c86…`, r39 claims `fb19ab9d…`; fleet report `ce2b87a0…`.

## Findings by severity

### F1 — MEDIUM (calibration): the R4 check does not re-derive the report's role counts

`c2-count.py:72-79` re-derives the spec and plan histograms honestly
(`spec_mix == plan_mix`), but the report leg is only
`"reviewer 6 / critic 5" in report and "revenger 2" in report`. Seven of the ten role counts
(executor, scout, scribe, mutation-tester, sentinel, connector, simplifier) and the report's
seat total are never checked against the spec, so the frozen R4 code condition —
“exact role-count agreement among the committed spec, validator plan, and report”
(`corpus/evidence/round40/claims.md:25`) — is not implemented for the report, and the claim's
own requirement “not count prose labels alone” (`claims.md:23`) is violated on that leg.

Reachable false positives, executed against the **real** counter in a scratch clone
(`git clone --shared` of the lane into `/tmp/r4probe/fleet/chousa-shokunin`, fleet report
copied to `/tmp/r4probe/fleet/.ufo/reports/round-39/chousa.md`; production untouched,
scratch removed afterwards):

```
baseline (committed report)                rc=0 R4_DISPOSITION=ok / R39_CALIBRATION_DISPOSITIONS=4/4
report executor 6 -> 9                     rc=0 R4_DISPOSITION=ok / R39_CALIBRATION_DISPOSITIONS=4/4
report total 32 seats -> 33 seats          rc=0 R4_DISPOSITION=ok / R39_CALIBRATION_DISPOSITIONS=4/4
report mix replaced by prose only          rc=0 R4_DISPOSITION=ok / R39_CALIBRATION_DISPOSITIONS=4/4
```

A report stating `executor 9` (mix sums 35 against a “32 seats” total) or `33 seats`, or no
mix table at all, still yields 4/4. Impact on this round's verdict: none — I independently
parsed the committed report and it equals the spec mix elementwise (Evidence 1), so the
disposition is true. Impact on the claim: the counter's check set does not by itself support
the report-agreement half of the R4 disposition, which is the support the kill rule demands
(`claims.md:33`, “unsupported by the counter's checks”). Because P2 freezes the counter's
identity, hardening it requires an appended erratum, not a silent edit. Smallest fix: parse
the report's mix block into a `Counter` and require equality with `spec_mix` plus equal
totals; anchor the spot-check check on the `**R4` bullet (F3).

### F2 — LOW (calibration): “committed evidence” is not enforced

`c2-count.py:24-25` (`text()`) reads every textual input from the working tree
(`claims39`, `lesson39`, scorecard, spot-check, spec, plan, fleet report; constants at
`c2-count.py:11-18`). `tracked()` exists (lines 37-40) but is used only for the R2 receipt.
A dirty but tracked file is therefore validated as if committed. Scratch-clone execution with
one executor moved to scribe in the **working-tree** spec and plan (both, so the histograms
still match), while `HEAD` still reads 6 executors:

```
dirty spec+plan: ExecC1Rederive executor->scribe     rc=0 R4_DISPOSITION=ok / R39_CALIBRATION_DISPOSITIONS=4/4
   committed HEAD still executor count: 6
restored worktree                                    rc=0 R4_DISPOSITION=ok / R39_CALIBRATION_DISPOSITIONS=4/4
```

Today the real repo is clean for all six inputs (Evidence 4), so the disposition's
“committed” wording holds. Fix: read via `git show HEAD:<path>` (or assert `tracked()` and a
clean worktree) for the four r39 artifacts.

### F3 — LOW (calibration): the spot-check leg matches any occurrence, not the routed assertion

`closure_mismatch = "reviewer 8 / revenger 0" in spotcheck` accepts the literal anywhere in
the file. Negating the claim in place in the scratch copy —

```
spot-check R4 line negated in place                 rc=0 R4_DISPOSITION=ok / R39_CALIBRATION_DISPOSITIONS=4/4
```

— i.e. `NOT reviewer 8 / revenger 0` still passes. The frozen condition only requires the
contrary statement to “remain cited”, so this is not a current-state defect; it is a fidelity
gap: the counter cannot distinguish the spot-check asserting 8/0 from the spot-check quoting
it as refuted. Anchor on the `- **R4` line and require both numbers inside it.

### F4 — INFO (residual): histogram-role collection is lossy and totals are unasserted

`role_mix()` (`c2-count.py:43-45`) silently skips rows lacking the key, and no check asserts
32 rows / unique names / `plan.counts.total == 32`, nor compares `plan.registry.members` to
`plan.tasks`. All hold today (32 items, 32 tasks, 32 registry members, unique names, roles
identical), so this is residual only. A row with a missing `role` would be dropped rather than
refused.

### Adjacent, not mine (route only)

`SCORECARD.md` gained 17 lines after the measured commit (`282dc76` appended the round-40
measured-claims section; `d164f88 → HEAD`). R3/R5 counter inputs read SCORECARD; R4 inputs
(claims39, spot-check, spec, plan, dispositions, counter) are byte-identical between
`d164f88` and HEAD, so my verdict holds at both. Defer any SCORECARD judgement to the R3/R5
seats.

## Provenance of the wrong numbers (mechanism, labelled inference)

Fact (verified): exactly 8 r39 seat names begin with `Rev` — six reviewers (`RevClaims`,
`RevSeparability`, `RevCounters`, `RevGate`, `RevRoutedDefects`, `RevReceipts`) plus the two
revengers (`RevErrataCtx`, `RevTextOverreach`); no other seat uses the prefix. Counting that
prefix instead of the `role` field yields exactly `reviewer 8 / revenger 0` while preserving
“totals 32 both”, which is the spot-check's exact pair. It is the only deterministic miscount
I found that reproduces the assertion from r39 bytes.

[INFERENCE] The spot-check most likely counted `Rev*` seat names, or carried a habitual
`reviewer 8` mix (that count appears in at least ten other fleet round reports). The
spot-check's authoring method is not recoverable from committed bytes; the disposition is
correct either way because it rests on the cited artifacts, not on explaining the error.

## Residual risk and verification gaps

- The spot-check's counting method is unknowable from git; the two mechanisms above are
  inference, not evidence. Pre-commit working-tree states of the spec/plan are unrecoverable,
  so “no version ever had 8/0” is proven for committed bytes only — which is the standard the
  disposition claims.
- I did not execute the external wave validator (`ufo-swarm-wave.mjs`). I verified the
  committed plan's own rows, `counts {spawn:32, resume:0, total:32}`, and the 0-byte
  `w1-plan.err`; that the plan was validator-produced is another seat's check.
- F1/F2/F3 mutations ran only in a removed `/tmp` clone. No lane, fleet, index, or report
  file was modified; no pacman transaction attempted; no tool installed.
- Concurrent peer writes were present at report time (`tools/research-gate.sh`,
  `corpus/SOURCES.md`, `.ufo/waves/round-40/w1/swarm-registry.json` modified). None is an R4
  input; all six R4 inputs were re-checked HEAD-identical after those writes
  (worktree = HEAD, `git status --porcelain` empty for each).
- Convergence note (data, not authority): the sibling `CriticR4Disposition` independently
  reached “disposition supported”, and my sweep agrees with its single 8-reviewer artifact
  finding (round-33 w2, 34 seats). `CriticC2Calibration` independently reports the counter's
  prose-label weakness; my F1/F2/F3 isolate the R4 arms specifically.

## Artifact pointers

- `corpus/evidence/round40/routed-defect-dispositions.json:20-29` (R4 disposition, status +
  decision under test)
- `corpus/evidence/round40/claims.md:23,25,33` (frozen re-derivation requirement, R4 code
  condition, kill rule)
- `corpus/evidence/round39/claims.md:199` (R4 erratum)
- `.ufo/waves/round-39/w1-spec.json` (blob `3a1f47ed…`), `.ufo/waves/round-39/w1-plan.json`
  (blob `730e2dae…`), `.ufo/waves/round-39/gen-w1-spec.py:118-156,270-277` (hardcoded 6
  reviewer / 2 revenger items; no 8/0 path)
- `corpus/lessons/round-39-verifier-spotcheck.md:74` (blob `c1921178…`)
- `fleet:.ufo/reports/round-39/chousa.md:168-170` (blob `ce2b87a0…`, commit `f713ee1`)
- `corpus/evidence/round40/c2-count.py:24-25,37-45,72-79` (blob `2a9b0c86…`)
- `SCORECARD.md` round-40 R4 line (fleet-committed) and round-40 measured-claims section

Tool installs this seat: none (`git`, `python3` only; pacman paused host-wide, no transaction
attempted).

Report: .ufo/waves/round-40/w1/ReviewR4RoleMix.md
