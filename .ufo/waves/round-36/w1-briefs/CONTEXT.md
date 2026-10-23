# Goal
chousa lane (deep-research method), round 36, attempt 2, wave 1 of a v1 two-wave shape — build and
independently re-derive the round's two frozen claims. Lane repo /home/vgpnk/Projects/shokunin/chousa-shokunin (jj-colocated, branch master,
HEAD detached; read the tip with `git rev-parse master`). Wave base revision 700bd5fcbf9abc118a6a0f078d51a2e7460c2878; the landed gate
/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh has sha256 a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8 (verify: sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh); the pre-round control gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh is the
round-35 blob a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad.
Read FIRST, in this order: the frozen claim design /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/claims.md (two claims, P1/P2, kill rules, stated
limits, repairs R1-R6), then the C1 counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py, the C2 counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c2-count.py, the per-record witness /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/argv-witness.py,
and the round-35 witness /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py it replaces. Committed receipts: /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/measure/.
The round's two claims, landed by the L1's construction runs on seeds 36001/36011 (NOT the wave's):
- C1 operability (lowest scored axis, operability 3/10): the gate and its counter separate an
  output-equivalent engine swap in fourteen independent scenarios (PATH shim, BASH_ENV function,
  PATH-less host, relative/missing/non-GNU overrides, distinct-path override honoured and observed,
  default pin with a LIVE --version, override beating an imported shim, per-record argv attribution,
  manifest hash identity under a hostile sha256sum, C-locale decode, and the two pin echo/drift cells).
  P1 = `ENGINE_SWAP_CANARY=14/14` + `predicate_holds=true` on each of two fresh seeds. Before (base
  gate): 10/14 (S11-S14 fail). The cheapest do-nothing control is the base gate itself.
- C2 calibration: `tools/argv-witness.py` scores the matcher PER RECORD through the pinned engine's
  out-of-band argv channel (a distinct-path GNU-reporting recorder as `RESEARCH_GATE_GREP` logs one
  NUL-delimited argv per invocation; each record's own span must appear in a `-a -z -b -o -P` argv),
  separating the five output-equivalent survivors the round-35 witness admitted (python-exact,
  environment-keyed, witness-forge, one-call-for-show, body-replaced) while a renamed matcher passes.
  P2 = `WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass` on two fresh seeds.
  Before (base tree + r35 witness): 2/5, landed attribution absent, renamed fail.
Your job: independently re-derive both claims on FRESH seeds (36301, 36311, 36321, 36331, 36341 — do not
reuse 36001/36011/36021), attack each claim's fixture, and draft the frontier artifacts. A MEETS
finding — an output-equivalent engine that still scores 14/14 or attributes every record, a witness
bypass that passes P2, a scenario that passes without the gate behaving — is the most valuable result;
say exactly why, with the command and the receipt.

# Contract
- Every `Report:` trailer path is relative to /home/vgpnk/Projects/shokunin/chousa-shokunin — write it at /home/vgpnk/Projects/shokunin/chousa-shokunin/<that path>. Write your report once.
  Extra artifacts (receipts, patched gates, logs, drafts) go ONLY inside your own directory
  /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ (create it); keep each artifact under 1 MiB (large logs stay in /tmp/hyaku/chousa-r36/w1; cite path+sha256).
- Read-only on ALL lane production files (tools/, corpus/, SCORECARD.md, LOG.md, SKILL.md, README.md,
  PROVINCE.md, SHONEN.md, .ufo/waves/round-36/{controls,measure}/ …) and on the fleet repo, sibling
  lanes, lane jj state and the lane Git index. No git/jj write commands anywhere; read-only git
  (log/show/diff/status/rev-parse/cat-file) is fine. Experiments only in /tmp/hyaku/chousa-r36/w1/<YourName>/: copy files,
  or `git clone -q /home/vgpnk/Projects/shokunin/chousa-shokunin <dir> && git -C <dir> checkout -q 700bd5fcbf9abc118a6a0f078d51a2e7460c2878` (unset GIT_DIR/GIT_WORK_TREE/
  GIT_INDEX_FILE first). Counters: set C1_TMP / C2_TMP / WITNESS_TMP / TMPDIR to your scratch dir.
- Pin every gate you score: sha256 it. A receipt whose gate sha256 is neither a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8 nor the base
  control a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad nor a control you built and named is not evidence. Never edit the committed
  counters, the witness, the claims file or the gate — a bug is a finding.
- Processes: never signal by name/pattern (no pkill/killall/ps|grep kill loops); keep the PIDs you start
  and kill only those. Disk: /tmp/hyaku/chousa-r36/w1 is on /tmp; do not write to /fast. Network: NONE. Bound every command
  with `timeout` (<=1800 s for selftest/counters, <=900 s otherwise). Leaf seat: no subagents (an
  executor may spawn at most one read-only labrat probe). Do not run `pacman` anything.
- Honesty: report only what you ran or opened; quote commands, exit codes, key output. Mark inference
  [INFERENCE]. Located quotes <=25 words with path + access date 2026-10-23.
- Time box: return within 35 minutes of your start; a partial report with what you verified beats none.
# Tooling directive — operator, 2026-10-19 (always on, every agent)
You may install or update tools that help the task without asking; read /home/vgpnk/.omp/agent/RULES.md
first and record each install (tool, version, channel, reason). All pacman transactions are PAUSED
host-wide: install via `uv tool`/`npx`/an official binary in ~/.local/bin, or file an L0 question; never
`pacman -S/-Sy/-Syu/-U/-R` and never restart a host service.
