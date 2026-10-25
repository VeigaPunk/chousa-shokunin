# ConnectRouteTable — Round 45 w1

**Seat:** L1Chousa45.ConnectRouteTable (connector, leaf)
**Task:** read `/home/vgpnk/.omp/agent/config.yml` (READ ONLY) and report `task.agentModelOverrides` for scout, reviewer, critic, connector, sentinel, executor, mutation-tester, scribe, simplifier, labrat; `async.maxJobs`, `task.maxConcurrency`, `task.maxRecursionDepth`; file sha256; alias resolution per role. No changes made.

## Commands run

1. `read /home/vgpnk/.omp/agent/config.yml` (full, 554 lines) — verbatim relevant excerpts below.
2. `sha256sum /home/vgpnk/.omp/agent/config.yml` → verbatim:
   ```
   def1ba11422fdae40d97a376feb355bbb7c26e6d7648e6691a88ff9bea12c17b  /home/vgpnk/.omp/agent/config.yml
   ```
3. `ls` of report dir — `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-45/w1/` exists (contains `swarm-registry.json`; no `ConnectRouteTable.md` before this write).

## Findings

Source file: `/home/vgpnk/.omp/agent/config.yml` — sha256 `def1ba11422fdae40d97a376feb355bbb7c26e6d7648e6691a88ff9bea12c17b`. `setupVersion: 2`.

### task.agentModelOverrides (config.yml:357-375)

| Role | Override entry | Resolved alias | Resolved model (config.yml:344) |
|---|---|---|---|
| scout | `@m_flash` | m_flash | `commandcode/deepseek/deepseek-v4.1-flash` :high |
| reviewer | `@m_flash` | m_flash | `commandcode/deepseek/deepseek-v4.1-flash` :high |
| critic | `@m_flash` | m_flash | `commandcode/deepseek/deepseek-v4.1-flash` :high |
| connector | `@m_flash` | m_flash | `commandcode/deepseek/deepseek-v4.1-flash` :high |
| sentinel | `@m_flash` | m_flash | `commandcode/deepseek/deepseek-v4.1-flash` :high |
| executor | `@m_flash` | m_flash | `commandcode/deepseek/deepseek-v4.1-flash` :high |
| mutation-tester | `@m_flash` | m_flash | `commandcode/deepseek/deepseek-v4.1-flash` :high |
| scribe | `@m_flash` | m_flash | `commandcode/deepseek/deepseek-v4.1-flash` :high |
| simplifier | `@m_flash` | m_flash | `commandcode/deepseek/deepseek-v4.1-flash` :high |
| labrat | `@m_flash` | m_flash | `commandcode/deepseek/deepseek-v4.1-flash` :high |

Alias definition (config.yml:344): `m_flash: commandcode/deepseek/deepseek-v4.1-flash:max` — note: the alias's own reasoning level is `:max`; override string is `@m_flash` with no `:level` suffix, so the alias's baked `:max` applies (model `commandcode/deepseek/deepseek-v4.1-flash` is in `enabledModels`, config.yml:42). The table above shows the alias-declared level.

### Concurrency / recursion (config.yml:354-356, 547-548)

- `task.maxConcurrency: 400`
- `task.maxRecursionDepth: 3`
- `async.maxJobs: 450`

### Other routing-relevant entries

- `modelRoles` also defines `default: anthropic/claude-opus-5-5:medium` (config.yml:353); `task`/`main`/`planner` overrides are also `@m_flash` (config.yml:358-361), plus `revenger`, `sonic`, `distiller`, `seance`, `security-reviewer` are `@m_flash` (config.yml:366-375).
- `retry.modelFallback: true`; `m_flash` fallback chain (config.yml:492-499): `charm-hyper/deepseek-v4.1-flash` → `opencode-go/deepseek-v4.1-flash` → `devin/deepseek-v4-1-flash` → `devin/swe-2:max` → `cursor/default` → `inception/mercury-3:max` → `openai-codex/gpt-6-luna:low`.

## Contradictions / notes (stated, not smoothed)

- **Uniformity:** all 15 override roles map to a single alias (`m_flash`) — no role-differentiated model allocation exists in this file. Whether that is intended policy or flattening is not decidable from config alone; it means critic/reviewer/connector/sentinel run the same model as executor/scribe.
- **Level discrepancy:** override entries omit a `:level`; the alias itself declares `:max`. If the harness interprets `@alias` as alias-default level, all roles run `:max`; if it applies a separate default, levels may differ. Not resolvable from file contents alone.

## Verdict

Route table read successfully, read-only; no writes outside the one report file; no installs (no tooling needed; pacman untouched).

**Resolvable pointers:** `/home/vgpnk/.omp/agent/config.yml:344` (m_flash alias), `:357-375` (task.agentModelOverrides), `:354-356` (task.maxConcurrency=400, maxRecursionDepth=3), `:547-548` (async.maxJobs=450); sha256 `def1ba11422fdae40d97a376feb355bbb7c26e6d7648e6691a88ff9bea12c17b`.
