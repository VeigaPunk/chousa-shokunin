# W2ExecNoHarmFinal

## Verdict
Axes: operability and calibration. The five requested no-harm checks matched their expected outcomes on the lane checkout; this was a regression battery, not an adversarial attack pass.

## Evidence
`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master`:
```text
8e93bc916527b3c21f0f702967fa65c3b4c31699
```

`bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --selftest | tail -3` (verbatim output):
```text
ok-case  271 env-pin-override-missing     exit=2
ok-case  272 env-pin-override-fake        exit=2
RESEARCH_GATE_SELFTEST: PASS (272 cases, 0 skipped)
```
The requested pipeline does not use `pipefail`, so it preserves `tail`'s status rather than independently exposing the gate process status; the reported PASS line is observed.

`bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh verify-claims /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/claims-r2.jsonl --root ..` (verbatim output):
```text
research-gate v2 — ts=2026-10-24T04:14:49Z — mode=claims — claims=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/claims-r2.jsonl
CLAIM id=A01 expected=supported observed=supported source=research/deep-research-2026-09-28/A-shokunin-tradition.md at=line:52 verdict=match
CLAIM id=A02 expected=supported observed=supported source=research/deep-research-2026-09-28/A-shokunin-tradition.md at=line:80 verdict=match
CLAIM id=A03 expected=supported observed=supported source=research/deep-research-2026-09-28/A-shokunin-tradition.md at=line:81 verdict=match
CLAIM id=A04 expected=supported observed=supported source=research/deep-research-2026-09-28/A-shokunin-tradition.md at=line:88 verdict=match
CLAIM id=A05 expected=contradicted observed=contradicted source=research/deep-research-2026-09-28/A-shokunin-tradition.md at=line:64 verdict=match
CLAIM id=A06 expected=unsupported observed=unsupported source=research/deep-research-2026-09-28/A-shokunin-tradition.md at=- verdict=match
CLAIM id=B01 expected=supported observed=supported source=research/deep-research-2026-09-28/B-multiagent-knowledge.md at=line:47 verdict=match
CLAIM id=B02 expected=supported observed=supported source=research/deep-research-2026-09-28/B-multiagent-knowledge.md at=line:64 verdict=match
CLAIM id=B03 expected=supported observed=supported source=research/deep-research-2026-09-28/B-multiagent-knowledge.md at=line:79 verdict=match
CLAIM id=B04 expected=supported observed=supported source=research/deep-research-2026-09-28/B-multiagent-knowledge.md at=line:69 verdict=match
CLAIM id=B05 expected=unsupported observed=unsupported source=research/deep-research-2026-09-28/B-multiagent-knowledge.md at=- verdict=match
CLAIM id=C01 expected=supported observed=supported source=research/deep-research-2026-09-28/C-rank-taxonomy.md at=line:89 verdict=match
CLAIM id=C02 expected=supported observed=supported source=research/deep-research-2026-09-28/C-rank-taxonomy.md at=line:92 verdict=match
CLAIM id=C03 expected=supported observed=supported source=research/deep-research-2026-09-28/C-rank-taxonomy.md at=line:97 verdict=match
CLAIM id=C04 expected=supported observed=supported source=research/deep-research-2026-09-28/C-rank-taxonomy.md at=line:102 verdict=match
CLAIM id=C05 expected=supported observed=supported source=research/deep-research-2026-09-28/C-rank-taxonomy.md at=line:130 verdict=match
CLAIM id=C06 expected=contradicted observed=contradicted source=research/deep-research-2026-09-28/C-rank-taxonomy.md at=line:53 verdict=match
VERDICT_BEARING_CLAIMS=17/17
RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)
```

`bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh verify-chain /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/chain-r3.md --root ..` (verbatim output):
```text
research-gate v2 — ts=2026-10-24T04:14:49Z — mode=chain — record=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/chain-r3.md
CHAIN hop=1 status=resolved observed=verified source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=line:"1. When does an apprentice earn domain independence?" at=line:74 verdict=match
CHAIN hop=2 status=resolved observed=verified source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"I could not substantiate this spelling as an established art" at=line:64 verdict=match
CHAIN hop=3 status=resolved observed=verified source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"minarai/deshi/shokunin/jin'i-ryu/kiwami semantics" at=line:35 verdict=match
CHAIN hop=4 status=resolved observed=verified source=research/deep-research-2026-09-28/C-rank-taxonomy.md anchor=line:"“Jin’i-ryū” does not support the proposed literal tra" at=line:107 verdict=match
CHAIN hop=5 status=resolved observed=verified source=research/deep-research-2026-09-28/C-rank-taxonomy.md anchor=quote:"I found no authoritative attestation establishing jin’i-ry" at=line:109 verdict=match
CHAIN hop=6 status=resolved observed=verified source=research/deep-research-2026-09-28/B-multiagent-knowledge.md anchor=quote:"Track five axes separately: task competence, retention, evid" at=line:57 verdict=match
CHAIN hop=7 status=resolved observed=verified source=research/deep-research-2026-09-28/B-multiagent-knowledge.md anchor=quote:"Sources: Voyager and Generative Agents; Reflexion; Dynamic C" at=line:71 verdict=match
CHAIN hop=8 status=resolved observed=verified source=research/deep-research-2026-09-28/B-multiagent-knowledge.md anchor=quote:"Evolving strategies and domain playbooks" at=line:67 verdict=match
CHAIN hop=9 status=resolved observed=verified source=research/deep-research-2026-09-28/B-multiagent-knowledge.md anchor=quote:"In one AppWorld case, a rewrite reduced accumulated context " at=line:79 verdict=match
CHAIN hop=10 status=resolved observed=verified source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"graduated responsibility through actual work, rather than in" at=line:88 verdict=match
CHAIN hop=11 status=resolved observed=verified source=research/deep-research-2026-09-28/C-rank-taxonomy.md anchor=quote:"The axes your system needs are knowledge provenance, demonst" at=line:67 verdict=match
CHAIN hop=12 status=resolved observed=verified source=research/deep-research-2026-09-28/C-rank-taxonomy.md anchor=line:"Kyū/dan is a grading structure, not an autonomy ladder" at=line:87 verdict=match
CHAIN hop=13 status=resolved observed=verified source=research/deep-research-2026-09-28/C-rank-taxonomy.md anchor=quote:"In Go, kyū 級 counts downward toward 1-kyū; dan 段 count" at=line:89 verdict=match
CHAIN hop=14 status=resolved observed=verified source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"They do not establish a universal ladder of minarai → desh" at=line:52 verdict=match
CHAIN hop=15 status=resolved observed=verified source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"A skilled craft worker/artisan. The word itself does not cer" at=line:63 verdict=match
CHAIN hop=16 status=resolved observed=verified source=research/deep-research-2026-09-28/B-multiagent-knowledge.md anchor=quote:"It offers much weaker support for unrestricted whole-corpus " at=line:55 verdict=match
CHAIN hop=17 status=resolved observed=verified source=research/deep-research-2026-09-28/C-rank-taxonomy.md anchor=line:"“Jin’i-ryū” does not support the proposed literal tra" at=line:107 verdict=match
CHAIN hop=18 status=blocked-no-fetch observed=exempt source=https://kotobank.jp/ anchor=- at=- verdict=exempt
CHAIN hop=19 status=blocked-no-fetch observed=exempt source=https://arxiv.org/ anchor=- at=- verdict=exempt
CHAIN hop=20 status=unresolved observed=exempt source=S3 anchor=- at=- verdict=exempt
CHAIN hop=21 status=unresolved observed=exempt source=S2 anchor=- at=- verdict=exempt
CHAIN hop=22 status=unresolved observed=exempt source=S1 anchor=- at=- verdict=exempt
RESOLVED_HOPS=17/22
RESEARCH_GATE: CLEAN (hops=22 verified=17 exempt=5 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0 resolvable=0)
```

`bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh verify-all /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/full-r6-broken.md --claims /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/full-r6-broken.claims.jsonl --root ..` (verbatim stdout; command exited 1):
```text
research-gate v2 — ts=2026-10-24T04:14:49Z — mode=verify-all — record=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/full-r6-broken.md — claims=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/full-r6-broken.claims.jsonl — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=DRIFT findings=1 drift=1 tally=RESOLVED_HOPS=2/3
FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn surface=chain obs=hop=2 source=research/deep-research-2026-09-28/B-multiagent-knowledge.md anchor=quote:"Track five axes separately: task competence, retention, evid" nearest_line=57 context=The strongest design implication is to make knowledge changes—not agent self-a
SECTION sweeps state=run verdict=DRIFT findings=1 drift=1 tally=VERIFIED_SWEEPS=1/2 REJECTIONS_OK=1/2
FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=id=R2 missing=flip
SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=13 resolved=12 unresolved=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=2 findings=2 drift=2
RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=2 findings=2 drift=2)
```

SCORECARD.md:28–29 archive one-liner, re-executed verbatim:
```bash
python3 -c 'import subprocess; names=("A-shokunin-tradition.md","B-multiagent-knowledge.md","C-rank-taxonomy.md"); rows=[subprocess.run(["bash","tools/research-gate.sh","verify","../research/deep-research-2026-09-28/"+n,"--root",".."],capture_output=True,text=True) for n in names]; print("VERDICT_BEARING_EXPORTS=%d/3" % sum(r.returncode==1 and sum(s.startswith("RESEARCH_GATE: DRIFT (") for s in r.stdout.splitlines())==1 for r in rows))'
```
Output:
```text
VERDICT_BEARING_EXPORTS=3/3
```

## Findings
1. The round-2 claim fixture remained `17/17` CLEAN; the recorded per-claim observations match expectations. Grounding: `corpus/fixtures/claims-r2.README.md:152-158`.
2. The chain fixture remained `17/22` CLEAN (17 verified, 5 exempt); the broken-hop fixture was not part of this assignment. Grounding: `corpus/fixtures/chain-r3.README.md:198-205`.
3. The full-r6 broken twin produced exactly two drift sections, `chain` and `sweeps`; `structure`, `claims`, and `integrity` were CLEAN. Grounding: `corpus/fixtures/full-r6.README.md:158-167`; explicit companion path supplied above.
4. The SCORECARD archive observable remained `3/3`. Grounding: `SCORECARD.md:26-30`.
5. The selftest output reports PASS for 272 cases, 0 skipped. Grounding: the exact requested command and output above; its pipeline status caveat is stated above.

## Limits
Only the assigned no-harm regression battery was run; no C1/C2 counters or adversarial probes were run, so no seed applies and this report does not independently re-adjudicate the strengthened receipt pipeline. No tool was installed or upgraded. No blocker observed.