# Round 36 wave 1 — no-harm on prior observables

**Verdict: PASS — no harm observed.** On the landed gate at `700bd5fcbf9abc118a6a0f078d51a2e7460c2878`, all four pinned observables equal their recorded values. No lane production files were edited. This is the validated no-harm surface; it does not score C1/C2.

## Observable results

| Observable | Expected (prior recorded value) | Observed | Pass / harm |
|---|---|---|---|
| Claims fixture | `VERDICT_BEARING_CLAIMS=17/17`, CLEAN, exit 0 | `VERDICT_BEARING_CLAIMS=17/17`; CLEAN (`claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0`); exit 0 | PASS / no harm |
| Positive chain fixture | `RESOLVED_HOPS=17/22`, CLEAN, exit 0 | `RESOLVED_HOPS=17/22`; CLEAN (`hops=22 verified=17 exempt=5 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0 resolvable=0`); exit 0 | PASS / no harm |
| Broken chain control | `RESOLVED_HOPS=1/2`, DRIFT with `CHAIN_ANCHOR_NOT_FOUND`, exit 1 | `RESOLVED_HOPS=1/2`; DRIFT (`anchor-missing=1`, `findings=1`, `drift=1`), `CHAIN_ANCHOR_NOT_FOUND`; exit 1 | PASS / no harm |
| Round-1 archives | `VERDICT_BEARING_EXPORTS=3/3` | `VERDICT_BEARING_EXPORTS=3/3`; counter exit 0 | PASS / no harm |

Expected values are pinned in `SKILL.md` (accessed 2026-10-23; claims/chain contract lines 79–82, 155–162, 188–218; round-1 archive observables lines 124–127) and their fixture/runbook records: `corpus/fixtures/claims-r2.README.md` lines 124–158, `corpus/fixtures/chain-r3.README.md` lines 88–95 and 196–208, and `SCORECARD.md` lines 22–30 (all accessed 2026-10-23).

## Commands run, exit codes, deciding output

All observable commands ran from `/home/vgpnk/Projects/shokunin/chousa-shokunin`; command text below is verbatim.

1. `timeout 900s git rev-parse master` — exit 0. Output: `700bd5fcbf9abc118a6a0f078d51a2e7460c2878`.
2. `timeout 900s sha256sum tools/research-gate.sh ../research/deep-research-2026-09-28/A-shokunin-tradition.md ../research/deep-research-2026-09-28/B-multiagent-knowledge.md ../research/deep-research-2026-09-28/C-rank-taxonomy.md` — exit 0, run both before and after the observables. Gate stayed `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`; archive hashes stayed equal to their recorded pins: A `9033857d4625555c7b778dfad6df80e3e1b24ed8bffa3fee2fd445b9c5540b85`, B `6d8dbddd3e2d2f47dcb153c5a3347cc6321db4afc72cf07da40f0f7fe5022006`, C `e48fe70ff92055c217ac6ca6ce68e403aa5689fee8717f3bd0ccf5badc92321b`.
3. `timeout 900s bash -c 'bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..; rc=$?; printf "EXIT_CODE=%d\n" "$rc"'` — exit 0. Deciding lines: `VERDICT_BEARING_CLAIMS=17/17`; `RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)`; `EXIT_CODE=0`.
4. `timeout 900s bash -c 'bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..; rc=$?; printf "EXIT_CODE=%d\n" "$rc"'` — exit 0. Deciding lines: `RESOLVED_HOPS=17/22`; `RESEARCH_GATE: CLEAN (hops=22 verified=17 exempt=5 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0 resolvable=0)`; `EXIT_CODE=0`.
5. `timeout 900s bash -c 'bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3-broken.md --root ..; rc=$?; printf "EXIT_CODE=%d\n" "$rc"'` — exit 0 for the wrapper; gate exit 1. Deciding lines: `FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn surface=chain obs=hop=2 source=research/deep-research-2026-09-28/C-rank-taxonomy.md anchor=quote:"人為 — jin’i-ryū" nearest_line=53 context=The key distinction is between skill, teaching authority, and permission to act.`; `RESOLVED_HOPS=1/2`; `RESEARCH_GATE: DRIFT (hops=2 verified=1 exempt=0 anchor-missing=1 refused=0 invalid=0 findings=1 drift=1 resolvable=0)`; `EXIT_CODE=1`.
6. `timeout 900s python3 -c 'import subprocess; names=("A-shokunin-tradition.md","B-multiagent-knowledge.md","C-rank-taxonomy.md"); rows=[subprocess.run(["bash","tools/research-gate.sh","verify","../research/deep-research-2026-09-28/"+n,"--root",".."],capture_output=True,text=True) for n in names]; print("VERDICT_BEARING_EXPORTS=%d/3" % sum(r.returncode==1 and sum(s.startswith("RESEARCH_GATE: DRIFT (") for s in r.stdout.splitlines())==1 for r in rows))'; rc=$?; printf 'EXIT_CODE=%d\n' "$rc"` — exit 0. Deciding lines: `VERDICT_BEARING_EXPORTS=3/3`; `EXIT_CODE=0`.
7. `timeout 900s mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/SentNoHarm /tmp/hyaku/chousa-r36/w1/SentNoHarm` — exit 0, no output.
8. `timeout 900s sha256sum .ufo/waves/round-36/w1/SentNoHarm/no-harm-receipt.txt` — exit 0. Output: `956fb4695ede2eeaecaf1b7b129dd52c60b19bc3e0ded65ab38327514e139dbb  .ufo/waves/round-36/w1/SentNoHarm/no-harm-receipt.txt`.

## Opened files (access date 2026-10-23)

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1-briefs/SentNoHarm.md`
- `/home/vgpnk/.omp/agent/RULES.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/claims-r2.README.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/chain-r3.README.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/SCORECARD.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round-1/expected.json`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/claims.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c2-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/argv-witness.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py`

## Artifact

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/SentNoHarm/no-harm-receipt.txt` — SHA-256 `956fb4695ede2eeaecaf1b7b129dd52c60b19bc3e0ded65ab38327514e139dbb`.
