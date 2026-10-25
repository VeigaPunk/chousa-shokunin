# ExecNoHarm — round-40 no-harm regression battery

## Verdict

**No existing mode is harmed.** All six assigned checks (selftest, r1 archive aggregate, claims, valid chain, broken-chain control, composed integrity) match their round-39 pinned observables exactly, on gate bytes identical to the round-39 landed pin. The round-40 correction commits changed receipts, dispositions, registry rows and prose — not the gate, not the fixtures. A round-41 sibling rewrote the gate after these captures and committed it at `1bd9001` (`2cb04bdd…`, tip `a3aac04`); that gate is a different subject and is not exercised here. The committed `6bc90e0` bytes were re-extracted from `git show 6bc90e0:tools/research-gate.sh` and re-run, reproducing every output byte-for-byte (drift section). The verdict is scoped to `6bc90e0:tools/research-gate.sh` = `4253c187…07e3`.

Axes: **operability** (mode verdicts and exit codes), **calibration** (each observed value equals its committed pin, including the two intentionally nonzero controls), **depth** (byte-identity argument plus the archive predicate's meaning, below).

## Environment and pins

- cwd for every command: `/home/vgpnk/Projects/shokunin/chousa-shokunin`
- Lane tip at capture: `6bc90e04ac60307befacd554f7eee2b7284e2652`; at capture time (07:19–07:21Z) `sha256sum tools/research-gate.sh` returned the committed digest below and `git diff HEAD -- tools corpus/fixtures` was empty. A round-41 sibling rewrote the gate after the captures and committed it at `1bd9001`; tip at 07:35:29Z is `a3aac04` with gate `2cb04bdd…` (see the drift section immediately below). This report's subject is `6bc90e0:tools/research-gate.sh`.
- `sha256sum tools/research-gate.sh` = `4253c18738f84df9200cbc93f8e077ba63a418c5ee822c1324e1a8d75a9b07e3` — equals the r39 landed pin recorded at `corpus/lessons/round-39-verifier-spotcheck.md:25` and bound as `gate_sha256` in every committed r39/r40 active receipt.
- Fixture digests: `claims-r2.jsonl` `23d078cb…8802`, `chain-r3.md` `06115f2f…ba07`, `chain-r3-broken.md` `b66222a1…5c6a`, `integrity-r7.md` `4310ce86…1b1b`, `integrity-r7.claims.jsonl` `8e83b23d…abb3`.
- Expected values are the r39 pin: `SCORECARD.md:2228-2229` ("selftest PASS 275 … claims 17/17 CLEAN, chain 17/22 CLEAN, broken control 1/2 DRIFT, archives 3/3, integrity-r7 composed CLEAN") and the r39 battery item. Command forms are the r39 battery's own (`.ufo/waves/round-39/w1-spec.json`).
- Time of runs: 2026-10-24T07:19:31Z–07:21:24Z. No tool installed or updated; no pacman transaction; no network.

## Post-run worktree drift and committed-byte re-proof (SentinelWriteScope W0)

The sentinel reported that `tools/research-gate.sh` became dirty in the lane worktree. Timeline, measured:

- **My captures ran the committed bytes.** At 07:19Z `sha256sum tools/research-gate.sh` = `4253c187…07e3`, and the gate's own `GATE_PIN` line at 07:21:24Z prints `gate_sha256=4253c18738f84df9200cbc93f8e077ba63a418c5ee822c1324e1a8d75a9b07e3`. The sentinel's dirty write is mtime 07:23:46Z, after my battery finished. At 07:27:51Z I measured the live file as `2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34`, mtime 07:26:28Z, `git diff --stat` +92/−2 (round-41 C1 capture-tool pins) — the sibling is still editing, and the live digest moves. None of that is this seat's write.
- **No lane path was passed to `--pin`.** My pin target was `/tmp/r40-noharm/gate-pin.baseline`, not the gate or any lane file; the sentinel's truncation hazard did not apply here.
- **Re-proof from committed bytes.** `git show 6bc90e0:tools/research-gate.sh` → `/tmp/r40-noharm/headgate/research-gate-head.sh`, sha256 `4253c187…07e3`, 404197 bytes (same size as the r39 pin). Re-running claims, chain, chain-broken, verify-all, and the archive one-liner against that copy produced outputs **byte-identical** to the 07:19 captures after normalizing only the banner `ts=` field; archive `VERDICT_BEARING_EXPORTS=3/3`.
- **Selftest false-fail at a bare path, then a true pass in a lane-shaped mirror.** Running the extracted copy as `/tmp/r40-noharm/headgate/research-gate-head.sh --selftest` reported `FAIL (2/275 cases)`: case `claims-lane-fallback` refused `PROVINCE.md` as `CLAIM_SOURCE_MISSING`, and case `ptr-lane-abs` resolved to `/tmp/r40-noharm/PROVINCE.md` ("missing under CHOUSA_ROOT"). Both are location artifacts of the committed `LANE_ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd)` (`tools/research-gate.sh:313`): the selftest's lane-fallback cases require a lane-shaped root. Placing the same `6bc90e0` bytes at `/tmp/r40-noharm/mirror/tools/research-gate.sh` with `git show 6bc90e0:PROVINCE.md` at `/tmp/r40-noharm/mirror/PROVINCE.md` gives exit 0, `RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)`, 275 `ok-case` lines, stderr 0 bytes. Exact false-fail text (head-extract run, `ts` as observed):

```text
FAIL-case claims-lane-fallback         exit=1 want=0 verdicts=1 vbearing=1 token=RESEARCH_GATE: CLEAN VERDICT_BEARING_CLAIMS=1/1 CLAIM id=L1 expected=supported observed=supported source=PROVINCE.md at=line:3 verdict=match
    | CLAIM id=L1 expected=supported observed=refused source=PROVINCE.md at=- verdict=refused
    | FINDING CLAIM_SOURCE_MISSING severity=warn surface=claims obs=id=L1 source=PROVINCE.md obs=not a readable regular file under allowed roots
FAIL-case ptr-lane-abs                 exit=1 want=0 verdicts=1 vbearing=1 token=RESEARCH_GATE: CLEAN findings=0 drift=0
    | FINDING POINTER_UNRESOLVED severity=warn surface=sources obs=ctx=source:S1 ptr=/tmp/r40-noharm/PROVINCE.md missing under CHOUSA_ROOT
```

Conclusion: the committed gate passes 275/275; the two failures are harness-location effects, not mode harm. They are recorded as an operational limit for any future seat that re-proves from `git show`.

### Revision movement after the report (SentinelWriteScope W0/W1/W7)

- **Drift window closed by commit.** At 07:35:29Z the tip is `a3aac04`; `git log --oneline 6bc90e0..HEAD -- tools/research-gate.sh` → `1bd9001` (round-41 pin capture surface). `git cat-file blob a3aac04:tools/research-gate.sh` and the worktree both hash `2cb04bdd…`, so the worktree no longer differs from HEAD. My verdict remains scoped to `4253c187…07e3` (revision `6bc90e0`); the round-41 gate is a different subject and was not exercised here.
- **C1 is revision-scoped (cited, not re-measured).** SentinelWriteScope W0 reports `python3 corpus/evidence/round40/c1-count.py` at the new tip → `R39_ACTIVE_RECEIPTS=2/6`, exit 1 (four `gate-sha256-mismatch`), while the same six rows verified against `git cat-file blob 6bc90e0:tools/research-gate.sh` in a mktemp dir → 6/6. That is consistent with my own 6/6 measured at `6bc90e0`; the four gate-binding receipts name `4253c187`. I did not re-run the counter at tip — W0 is the sentinel's ground truth and not this battery's subject.
- **W1 pin hazard did not fire here.** `--pin PATH` truncates/overwrites its target with exit 0. My target `/tmp/r40-noharm/gate-pin.baseline` did not exist before the pin and is now a normal 2989-byte baseline; I passed no SELF, lane, or tracked path. Future re-proofs must never pass the gate's own path to `--pin`.
- **W7 command binding.** The item names "r1 archive, claims, chain, and integrity regression commands" without spelling them out in-round. I bound them to the only committed pin: the r39 no-harm battery recorded at `SCORECARD.md:2228-2229` and in the r39 wave item (`.ufo/waves/round-39/w1-spec.json`, ExecNoHarm prompt). Any other command set would need its own pin.

## Assigned commands and exact output

### 1. Research-gate selftest

`bash tools/research-gate.sh --selftest` — exit **0**; stdout 277 lines (275 `ok-case`, one locale note at line 193, one summary), stderr 0 bytes; `grep -c '^ok-case'` = 275, zero FAIL lines.

```text
ok-case  272 env-pin-override-fake        exit=2
ok-case  273 pin-bash-path-shim           exit=0
ok-case  274 bash-pin-override-missing    exit=2
ok-case  275 bash-pin-override-fake       exit=2
RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)
```

Pinned expectation: PASS 275 cases, 0 skipped. Observed: PASS 275 cases, 0 skipped. Match. This run executed the committed bytes: the file still hashed to `4253c187…07e3` at 07:19Z, and the first sibling write is mtime 07:23:46Z. The post-drift re-proof on `git show 6bc90e0:` bytes (mirror pass, bare-path false-fail) is in the drift section above.

### 2. r1 archive observable

`python3 -c 'import subprocess; names=("A-shokunin-tradition.md","B-multiagent-knowledge.md","C-rank-taxonomy.md"); rows=[subprocess.run(["bash","tools/research-gate.sh","verify","../research/deep-research-2026-09-28/"+n,"--root",".."],capture_output=True,text=True) for n in names]; print("VERDICT_BEARING_EXPORTS=%d/3" % sum(r.returncode==1 and sum(s.startswith("RESEARCH_GATE: DRIFT (") for s in r.stdout.splitlines())==1 for r in rows))'` — exit **0**.

```text
VERDICT_BEARING_EXPORTS=3/3
```

Per-input expansion (`bash tools/research-gate.sh verify <archive> --root ..`), each exit 1 with exactly one DRIFT summary line and 8 output lines:

| Archive | Exit | DRIFT lines | Summary |
|---|---:|---:|---|
| `A-shokunin-tradition.md` | 1 | 1 | `RESEARCH_GATE: DRIFT (findings=6 drift=5 questions=0 sources=0 chains=0 claims=0 negatives=0 rejections=0 approvals=0)` |
| `B-multiagent-knowledge.md` | 1 | 1 | `RESEARCH_GATE: DRIFT (findings=6 drift=5 questions=0 sources=0 chains=0 claims=0 negatives=0 rejections=0 approvals=0)` |
| `C-rank-taxonomy.md` | 1 | 1 | `RESEARCH_GATE: DRIFT (findings=6 drift=5 questions=0 sources=0 chains=0 claims=0 negatives=0 rejections=0 approvals=0)` |

Each per-input finding set is identical: `RECORD_SCHEMA_INVALID` (warn), `EXPORT_CHROME_PRESENT` (info), `NO_QUESTION` (crit), `SOURCE_TABLE_ABSENT` (warn), `CLAIM_TABLE_ABSENT` (warn), `REJECTION_DROPPED` (warn).

Pinned expectation: aggregates to `3/3`. Observed: `3/3`. Match. Depth note: this predicate counts **exit 1 plus one DRIFT line**, so a clean exit would be the regression here; per the round-37 lesson (`corpus/lessons/round-37.md:30`), reading per-input DRIFT as harm is the known misreading — the round-1 observable is verdict-bearing DRIFT, and it is unchanged.

### 3. Claims mode

`bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..` — exit **0**, stderr 0 bytes.

```text
research-gate v2 — ts=2026-10-24T07:19:31Z — mode=claims — claims=corpus/fixtures/claims-r2.jsonl
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

Pinned expectation: 17/17 CLEAN. Observed: 17/17 CLEAN. Match; every row matches, including the two `contradicted` and two `unsupported` expectations (the fixture still discriminates, it is not a pass-through).

### 4. Chain mode — valid fixture

`bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..` — exit **0**, stderr 0 bytes.

```text
research-gate v2 — ts=2026-10-24T07:19:31Z — mode=chain — record=corpus/fixtures/chain-r3.md
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

Pinned expectation: 17/22 CLEAN. Observed: 17/22 CLEAN. Match.

### 5. Chain mode — broken control

`bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3-broken.md --root ..` — exit **1**, stderr 0 bytes.

```text
research-gate v2 — ts=2026-10-24T07:19:32Z — mode=chain — record=corpus/fixtures/chain-r3-broken.md
CHAIN hop=1 status=resolved observed=verified source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"I could not substantiate this spelling as an established art" at=line:64 verdict=match
CHAIN hop=2 status=resolved observed=anchor-missing source=research/deep-research-2026-09-28/C-rank-taxonomy.md anchor=quote:"人為 — jin’i-ryū" at=- verdict=mismatch
FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn surface=chain obs=hop=2 source=research/deep-research-2026-09-28/C-rank-taxonomy.md anchor=quote:"人為 — jin’i-ryū" nearest_line=53 context=The key distinction is between skill, teaching authority, and permission to act.
RESOLVED_HOPS=1/2
RESEARCH_GATE: DRIFT (hops=2 verified=1 exempt=0 anchor-missing=1 refused=0 invalid=0 findings=1 drift=1 resolvable=0)
```

Pinned expectation: 1/2 DRIFT (exit 1). Observed: 1/2 DRIFT (exit 1). Match; the control still discriminates (hop 2 refuses rather than passing).

### 6. Integrity mode (composed, as named in the battery)

`bash tools/research-gate.sh verify-all corpus/fixtures/integrity-r7.md --claims corpus/fixtures/integrity-r7.claims.jsonl --root ..` — exit **0**, stderr 0 bytes.

```text
research-gate v2 — ts=2026-10-24T07:19:32Z — mode=verify-all — record=corpus/fixtures/integrity-r7.md — claims=corpus/fixtures/integrity-r7.claims.jsonl — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=4/4
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=2/3 REJECTIONS_OK=2/2
SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=16 resolved=15 unresolved=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0)
```

Pinned expectation: integrity-r7 composed CLEAN. Observed: composed CLEAN, 5/5 sections run, `INTEGRITY refs=16 resolved=15 unresolved=0`. Match.

## Supplementary probes (beyond the assigned six; separated so the parent can discount them)

Run because the item asks about harm to *any existing mode*; all are read-only over the lane, and the pin probe writes only under `/tmp`.

- Standalone integrity mode: `bash tools/research-gate.sh verify-integrity corpus/fixtures/integrity-r7.md --root .` → exit 0; `INTEGRITY refs=16 resolved=15 unresolved=0`; `RESEARCH_GATE: CLEAN (refs=16 resolved=15 unresolved=0 exempt=1 findings=0 drift=0)`. Matches the round-35 pin `refs=16 resolved=15 unresolved=0`, CLEAN, exit 0 (`.ufo/waves/round-35/w2/RevGrepModesB.md:37`).
- Pin/drift self-consistency: `bash tools/research-gate.sh --pin /tmp/r40-noharm/gate-pin.baseline` → exit 0, `GATE_PIN: ok path=/tmp/r40-noharm/gate-pin.baseline gate_sha256=4253c18738f84df9200cbc93f8e077ba63a418c5ee822c1324e1a8d75a9b07e3`; `bash tools/research-gate.sh --drift /tmp/r40-noharm/gate-pin.baseline` → exit 0, `GATE_DRIFT: none`. Both modes function and agree with the pinned bytes.
- Frozen counters re-derived at capture revision `6bc90e0` (not gate modes; corroborates the milestone predicates at that revision): `python3 corpus/evidence/round40/c1-count.py` → `R39_ACTIVE_RECEIPTS=6/6`, exit 0, six `VERIFY: ok` lines; `python3 corpus/evidence/round40/c2-count.py` → `R2_DISPOSITION=ok`, `R3_DISPOSITION=ok`, `R4_DISPOSITION=ok`, `R5_DISPOSITION=ok`, `R39_CALIBRATION_DISPOSITIONS=4/4`, exit 0. Both equal `corpus/evidence/round40/measure-after.txt`. At the moved tip, W0 reports 2/6 (see drift section); the 6/6 here is not a current-tip claim.
- `bash tools/research-gate.sh --version` → exit 2, "unknown flag: --version" plus usage. This is not a mode and not a regression: the gate exposes no `--version` flag; its version is the banner contract `VERSION=v2` at `tools/research-gate.sh:302` (the r12 scorecard's `VERSION=research-gate-r1` is that era's banner and survives only as the r1-history note at `:297`). Recorded so nobody mistakes the exit-2 for harm.

## Harm analysis

1. **Byte identity.** The gate tested is `4253c187…07e3`, the exact round-39 landed gate that held the r39 battery; `git log -- tools/research-gate.sh` shows its last change at round-39 commit `6d914e9`, and none of round-40's four commits (`6c01a41` freeze, `d164f88` receipts/dispositions, `282dc76` measurements/lesson, `6bc90e0` spot-check) touches `tools/` or `corpus/fixtures/`. Since the gate's modes are pure functions of those bytes plus their inputs, and the inputs' digests are pinned above, no mode can differ from the r39 pin — and the observed outputs confirm it mode by mode.
2. **Expected-nonzero controls stayed nonzero and correctly valued.** Broken chain 1/2 DRIFT and archive DRIFT 3/3 are the pinned pass conditions; a CLEAN here would have been the regression. Both discriminate (a refusal/anchor-miss is reported, not swallowed).
3. **Selftest surface intact.** 275/275, 0 skipped, exit 0, empty stderr; the 275 count is exactly the r39 count, so the round-40 receipt/disposition work introduced no case loss and no new failure. The negative-control expectation for the highest case numbers (272–275, env/bash pin override cases) is still `exit=2`, i.e. the fail-closed behavior is still what the suite records.
4. **No production or repo mutation by this battery.** The runs are read-only over lane artifacts (the pin probe wrote only under `/tmp`). `git status --porcelain` after the runs lists wave bookkeeping (`.ufo/waves/round-40/w1/swarm-registry.json` modified by the orchestrator), sibling-authored report notes and sibling `round41` directories, and — after my captures — `tools/research-gate.sh` modified by round-41 sibling work (mtime 07:23:46Z onward; drift section). No lane path was changed by this seat.

## Limits

- The battery ran the gate's own committed fixtures; it does not re-audit receipt expectation digests or the R4 role-count claim (other round-40 seats own those). The C1/C2 counter re-derivations above are corroboration only.
- The gate's selftest resolves lane files from `LANE_ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd)` (`tools/research-gate.sh:313`), so re-proving committed bytes from a bare `/tmp` extract false-fails cases 106 (`claims-lane-fallback`) and 132 (`ptr-lane-abs`) unless `PROVINCE.md` sits one level above the script. The lane-shaped mirror avoids this; the failure text is recorded above so nobody reads it as gate harm.
- The round-41 gate edit (+92/−2, capture-tool pins) was committed at `1bd9001` (`2cb04bdd…`) and was not exercised by this battery; this report's verdict applies to the committed bytes `4253c187…07e3` (revision `6bc90e0`), re-proved from `git show`.
- The C1/C2 counter outputs are `6bc90e0`-scoped, not current-tip claims. Per SentinelWriteScope W0, `c1-count.py` at tip `a3aac04` gives `R39_ACTIVE_RECEIPTS=2/6` (four `gate-sha256-mismatch`), because the four active receipts bind `4253c187`; re-issuing or re-scoping them is a round-41 decision, not this seat's.
- Round-41 evidence (`corpus/evidence/round41/`) is now committed; a sibling-modified `cells.json` remains in the worktree. Neither is an input to any command above. They are noted as observation, not harm.
- No tool installed, no network fetch, no model routing change.

## Artifact pointer

This report: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-40/w1/ExecNoHarm.md`.
Raw captures (`/tmp`, this session only, non-durable): `/tmp/r40-noharm/{selftest,claims,chain,chain-broken,integrity,integrity-standalone,pin,drift,archive}.out`, `archive-{A,B,C}-*.out`; post-drift re-proof: `headgate/research-gate-head.sh` (sha `4253c187…07e3`), `head-{claims,chain,chain-broken,integrity,archive}.out`, `head-selftest.out`, `mirror/tools/research-gate.sh` + `mirror/PROVINCE.md`, `mirror-selftest.out`. Durable re-derivation commands are embedded verbatim above.
