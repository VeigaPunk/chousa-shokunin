# ScoutInherited — round 49 wave 1

Item: read the three archived pre-revert diffs under `.ufo/waves/round-49/inherited/`, name what produced them, and judge whether the reverted (master) bytes are the correct historical evidence. Read-only: no lane file, git index, jj state, fleet repo or `/home/vgpnk/Projects/shokuknow` written. No network, no tool install. Scratch `/tmp/chousa-r49-ScoutInherited/` deleted.

## 1. The diffs; the "+" side is the pre-revert worktree

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ git hash-object <3 paths>              # == git rev-parse HEAD:<same>
207ed99db5c79a58cfd08c045a99cd34c0d63bf3  .ufo/waves/round-40/w1/swarm-registry.json
3d3b1c327e6acf6e5d83d0e0915305dfbea580d3  .ufo/waves/round-41/w1/swarm-registry.json
3a846cd2fc737e70b195a03cad37686da677bda2  corpus/evidence/round41/receipts/cells/cells.json
```
All three are back at master. **The archive is lossless**: in a fresh fixture repo (`git apply` only, no commit) the three diffs rebuild the lost bytes exactly — `4567c25c91fa…` / `034d47a153c…` / `95478bf634f…` = the three `+` blobs. The same blobs survive in the lane object store (abandoned commits `cb14413` chousa-shokunin 11:16 and `1c557f3` protocol-shokunin 11:34; neither an ancestor of HEAD).

## 2. cells.json — producer: a CONTROL-arm re-run of the round-41 counter

Pre-revert blob `95478bf` is the **control** receipt, not the landed one: `gate=…/controls/base-gate-r41.sh`, `k=1 of 12`; master `3a846cd` is `gate=…/tools/research-gate.sh`, `k=12 of 12`, all 12 cells `predicate_holds=true`. The counter writes one fixed path, so a control arm clobbers the landed receipt: `corpus/evidence/round41/c1-count.py:99` `RCPTS = LANE/"corpus"/"evidence"/"round41"/"receipts"`, `:101-104` `out_dir = RCPTS/"cells"`, `:258` `(out_dir/"cells.json").write_text(...)`; `LANE = Path(__file__).resolve().parents[3]` = the lane root when run from the lane.

**Reproduced** (counter copy + control gate in scratch, TMPDIR redirected): `CAPTURE_PIN_MATCH=1/12  PASS S1-base-clean  FAIL S2…S12` (exit 1). Per-cell comparison against `95478bf`: identical `gate`, `k/n`, `predicate_holds` for all 12 cells, identical evidence-key sets. The archived `+` lines carry the same fingerprints — `research-gate: --drift baseline missing: /tmp/ExecC1LandedReceipt-ctl/chousa-r41-c1-bnnkud11/s4/baseline.txt` and trap marks under `/tmp/ExecC1LandedReceipt-ctl/` — a **wave seat** re-ran the counter's control arm inside the lane. Gate pin epoch `date -u -d @1792827947` = **2026-10-24T07:45:47Z** (3 min after the r41 live registry write at 07:42:46Z; round 41 ran 07:15:40–07:34:10Z).

**Most likely command:** `python3 corpus/evidence/round41/c1-count.py --gate .ufo/waves/round-41/controls/base-gate-r41.sh` from the lane root — the exact command the wave's `ExecC1BaseReceipt` item names, with the seat's TMPDIR inherited. This is the named r41 **D2** defect ("the counter rewrites it on every run"), now a concrete control-arm overwrite.

**Reverted master bytes = correct historical evidence: YES.** Master `3a846cd` is what round 41 cites: `corpus/evidence/round41/measure-after-c1.txt` = `CAPTURE_PIN_MATCH=12/12` + 12 × `PASS`; `corpus/lessons/round-41.md:9` names `corpus/evidence/round41/receipts/cells/cells.json` as that run's receipt; `SCORECARD.md:2286` C1 row `1/12 → 12/12`, work commit `1bd9001330f19d89ec36592010d4218881ea5941` (`git log -- corpus/evidence/round41/receipts/cells/cells.json` → `1bd9001`). Committing the control receipt would have replaced the landed measurement with the do-nothing control (`k=1`) — falsification.

**Residual in committed bytes (read-only finding).** The round-43 assimilation mirror committed the *control* receipt: `.ufo/waves/round-43/assimilation/validate/corpus/evidence/round41/receipts/cells/cells.json` = blob `95478bf` (`base-gate-r41.sh`, k=1), while the r45 mirror holds `226b8907` (`research-gate.sh`, k=12). Every other mirrored file matches master (`claims.md` `d9e1e6a…`, `cells-before.json` `ab61d62…` in both). [INFERENCE] r43 mirrored the worktree, r45 mirrored HEAD.

## 3. The two registries — producer: the orchestrator's wave runner

Both `+` blobs are documents the wave tool writes, not lane edits.

- **r40** — master `207ed99`: schema `ufo-swarm-registry-v1`, key `"path"`, members map, `agentId: null`; byte-equal to `w1-dispatch.json`'s `registry` (`reg==disp.registry → True`). `+` `4567c25`: schema `ufo-swarm-registry-v1`, `wave`/`createdAt`/`updatedAt`/`reportDir`, members map with **resolved agentIds** (`ExecC1BaseReceipt`, …); 33 members = the spec's 33 items, identical names/order.
- **r41** — master `3d3b1c3`: legacy schema `ufo-swarm-wave-registry-v1`, members **array**, `agentId: null`; byte-equal (sha256 `9e0e9d17…`) to fleet-root `/home/vgpnk/Projects/shokunin/.ufo/waves/round-41/w1/swarm-registry.legacy-wave-v1.json`, tracked by fleet `5ac02c4f` "chousa r41 pre-dispatch registry archive (orchestrator artifact)". `+` `034d47a`: schema `ufo-swarm-registry-v1`, `wave`/`createdAt`/`updatedAt`/`reportDir`, members map with agentIds `ExecC1BaseReceipt-2`, `ExecC1LandedReceipt-2`, …; 35 members = the spec's 35 items, identical names/order.

Tool-as-writer evidence: `ufo-swarm-wave.mjs:665-679` `buildRegistryDoc` emits exactly `{schema,wave,createdAt,updatedAt,reportDir[,priorRegistries],members}`; `:653-656` `writeRegistry` writes `JSON.stringify(registry,null,2)+"\n"` (the `+` blobs: 2-space indent + trailing newline; the committed r41 blob: 1-space, no trailing newline); `:1710` `persistWaveRegistry` and `:1956` `mainRecord` are the only two writers, and `mainRecord` preserves `createdAt` while bumping `updatedAt` — matching r40 `createdAt 07:16:35.766Z` / `updatedAt 07:18:06.849Z` and r41 `07:41:44.810Z` / `07:42:46.931Z` (run, then `record`). Timeline (`/home/vgpnk/Projects/shokunin/.ufo/watchdog.log`): round 40 ran 03:29:24–04:13:35-0300, round 41 04:15:40–04:34:10, round 42 from 19:58:10 — the r40 write falls inside round 41's window, and the fleet's round-41 lane report says so: "the orchestrator's running round-40 wave has written ~28 seat reports + registry updates under `.ufo/waves/round-40/w1/`" (`.ufo/reports/round-41/chousa.md:27`, repeated `:61`). The r41 write is 7 min after round 41 closed.

**Most likely commands** (`scripts/hyaku/lane-addendum.md:110-114`, `UFO_PROJECT_ROOT=<lane>`):
```
node ~/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs run    --spec .ufo/waves/round-4X/w1-spec.json
node ~/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs record --registry .ufo/waves/round-4X/w1/swarm-registry.json --assignments '{…}'
```
`run`→`persistWaveRegistry` writes `reportDir/swarm-registry.json` (the lane path, hence the overwrite of the lane's own committed copy); `record`→`mainRecord` fills the agentIds. Member sets equal this lane's own spec item lists exactly. The `-2` suffixes are harness second-generation handles.

**Are the reverted committed bytes correct historical evidence? Different per file.** r40 `207ed99`: **yes** for the lane — the dispatch-payload registry copy (`agentId: null`), the "prepared wave" state the lane's `DISPATCH-README.md` describes; the `+` side is orchestrator-owned runtime state, and committing it would put another actor's live handles in lane history — the sweep the round-43/44 dispositions refused (`left-named; not hunk-verified`). r41 `3d3b1c3`: **not loadable by today's tool** — `ufo-swarm-registry.mjs:112-114` rejects any `schema` ≠ `ufo-swarm-registry-v1`; running the real loader on both files: `HEAD r40 committed ACCEPTED; memberCount=33` / `HEAD r41 committed REJECTED: invalid_registry: not a ufo-swarm-registry-v1 document`. Master keeps a legacy archive copy; the discarded `034d47a` was the **only** record that the r41 wave dispatched with resolved agent handles — the fact `corpus/lessons/round-42.md:26` records as the mistake class "prepared-as-dispatched — a validated spec with null agent ids was the round's wave evidence" (QUALITY 61: a spec is not a dispatch). **Operator decision still open, unanswered:** `.ufo/l0-questions.md:144` (chousa | round-43) asks "Commit them as historical wave evidence, or leave them?" — no `L0 ANSWER` on that line (`grep -n ANSWER …/l0-questions.md` → lines 52, 53, 126 only). My read: commit the two live registries as wave evidence, keep the landed cells.json — but that is the lane's/operator's call; I changed nothing. Either way nothing is lost: the `+` bytes are recoverable from the archive (§1).

## 4. Detail correction to the committed round-49 lesson (`corpus/lessons/round-49.md:30`)

That row says the three were "reverted to the committed bytes; their pre-revert diffs are kept in `.ufo/waves/round-49/inherited/`". This seat adds two factual refinements, no change of decision: (i) the cells.json overwrite was a **control-arm** run (k=1, base gate) at 2026-10-24T07:45:47Z, not a landed re-run — the archived `+` side proves it; (ii) the two registries were re-rendered by the orchestrator's wave runner (`run`+`record`), the r41 one carrying resolved agent ids while the r41 master copy is a legacy-schema artifact the current loader rejects. The r43 mirror carrying the control receipt is a residual provenance defect in committed bytes.

## Confidence and gaps
- **High** — producer of each diff (control-gate counter run; wave-runner `run`/`record` re-render); cells.json reproduced cell-by-cell; blob identities and timestamps exact.
- **High** — master bytes are the correct evidence for cells.json (12/12 receipt cited by `measure-after-c1.txt`, `round-41.md:9`, `SCORECARD.md:2286`).
- **Medium** — that the registry `+` blobs came from *this* lane's specs: member sets/order match the lane specs exactly, but the runner writes to `reportDir`, so an identically-named wave from another root could in principle have written the same path; no `ufo-swarm-wave` log survives in the lane.
- **Gap (named, unresolved)** — no operator answer to `.ufo/l0-questions.md:144`; the r41 registry question (commit the dispatch evidence or leave master) stays the lane's/operator's call.
- **Gap** — round-41 session transcripts are absent from `~/.omp/agent/sessions/` (only 2026-10-25 sessions exist), so the seat behind `/tmp/ExecC1LandedReceipt-ctl` is inferred from the TMPDIR name, not read from a transcript.

VERDICT: I attributed all three inherited diffs (cells.json = a round-41 counter **control-arm** overwrite at 2026-10-24T07:45:47Z, reproduced to k=1 with matching per-cell evidence; the two registries = the orchestrator's `ufo-swarm-wave.mjs run`/`record` re-render, r40 at 07:16–07:18Z and r41 at 07:41–07:42Z), verified the archived diffs reconstruct the lost blobs byte-exactly, and judged the reverted master bytes correct for cells.json (the cited 12/12 landed receipt) but legacy and tool-unloadable for the r41 registry — whose dispatch evidence is archived, recoverable, and pending the still-unanswered round-43 operator question.
