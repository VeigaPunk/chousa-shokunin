# SentNoEgress — round-45 wave-1 egress/scope audit

Seat: L1Chousa45.SentNoEgress (leaf; no dispatch).
Item: prove the round's new code cannot reach the network or write outside its scope.
Scope scanned: `corpus/evidence/round45/c1-count.py`, `c2-count.py`, `c3-count.py`,
`.ufo/waves/round-45/assimilation/map-staged.py`, plus the two tools they spawn
(`tools/parent-lifetime.sh`, `tools/quarantine-check.py`) for transitive egress.

## Verdict

**No egress. No out-of-scope writes.** All four files are egress-free; the only writers
(c1) write inside a `tempfile.TemporaryDirectory` that is removed on exit. `kimi` PATH
injection cannot reach the non-stub binary: the counter prepends its own `$tmp/bin` to PATH
and the launcher resolves `kimi` bare through PATH.

## Grep hits (pattern: urllib|requests|socket|http.client|curl|wget|subprocess|write_text|write_bytes|open( | dev/tcp|os.system|Popen|check_call|check_output|dup2|exec 3<>|/dev/udp)

| file | line | hit | egress | write outside scope |
|---|---|---|---|---|
| c1-count.py | 27 | `import subprocess` | no (local only, see below) | — |
| c1-count.py | 45 | `path.write_text(json.dumps(...))` | no | no — `path` is `tmp/tag/dispatch.json` (under TemporaryDirectory) |
| c1-count.py | 55 | `agent.write_text("stub\n")` | no | no — `tmp/tag/agent.yaml` |
| c1-count.py | 62 | `subprocess.run(argv, env=env, ..., timeout=120)` | no | no — argv is fixed literals, no `shell=True`, no pipes |
| c1-count.py | 90 | `stub.write_text(STUB, ...)` | no | no — `tmp/bin/kimi` |
| map-staged.py | 13 | `import subprocess` | no | — |
| map-staged.py | 34 | `subprocess.run([sys.executable, str(LANE/"tools/quarantine-check.py"), "slice"], capture_output=True, ..., check=True)` | no | no — local python, local tool, fixed arg, no `shell=True` |
| c2-count.py | — | zero hits | — | — (no subprocess, no writes; stdout prints only) |
| c3-count.py | — | zero hits | — | — (no subprocess, no writes; reads captures/entries read-only, prints) |
| parent-lifetime.sh | — | zero hits | — | — |
| quarantine-check.py | — | zero hits | — | — |

## subprocess analysis (can it egress?)

- **c1-count.py:57-62**: `argv = ["bash", str(tool), "--dispatch", str(disp), "--receipt", str(receipt), "--agent", str(agent)]` (+ `["--timeout", timeout]`). No `shell=True`, no pipe/shell metachars, all arguments are literal local paths/flags. `env = dict(os.environ, PATH=f"{tmp/'bin'}:{os.environ.get('PATH','')}", STUB_MODE=mode)` — only PATH prefix + STUB_MODE overridden.
- **Spawned launcher (parent-lifetime.sh)**: full-file grep for network primitives (urllib/requests/socket/http.client/curl/wget/nc/telnet/ftp/dev/tcp/os.system/Popen/etc.) — zero hits. It writes only to `$RECEIPT` and `$logdir` (both under `tmp/tag/` when invoked by c1, per argv construction) and spawns `kimi` via bare PATH lookup (line 73-75). No network commands.
- **map-staged.py:34**: runs `sys.executable` on local `tools/quarantine-check.py` with fixed arg `"slice"`; quarantine-check.py grep clean (no network imports/commands). No `shell=True`.
- **c2/c3**: no subprocess at all.

## c1 temp-dir removal

`main()` wraps every run in `with tempfile.TemporaryDirectory(prefix="chousa-r45-c1-") as t:` (line 86). All writes — `dispatch.json`, `agent.yaml`, `bin/kimi`, and the launcher's receipt/seat-log outputs — land under that tempdir; context-manager exit deletes it (also on exception). No `mkdtemp`/`mktemp` without cleanup anywhere.

## PATH injection vs non-stub `kimi`

- Real `kimi` exists on host: `/home/vgpnk/.kimi-code/bin/kimi` (192 MB binary, mode 755), and is last in the current PATH (`...:/home/vgpnk/.kimi-code/bin`).
- c1 writes the stub to `tmp/bin/kimi` (lines 89-91, `chmod 0o755`) *before* any `run()`, and prepends `tmp/bin` to PATH (line 61). The launcher invokes `kimi` bare (parent-lifetime.sh line 74), so resolution always hits the stub first — the non-stub binary is unreachable.
- The stub (`STUB` heredoc, lines 34-40) contains no exec of external programs: `case "${STUB_MODE:-ok}" in ok) exit 0;; hang) exec sleep 30;; esac; exit 9`.
- No other PATH entry can precede `tmp/bin` (prepend, not append). Verdict: PATH injection cannot run a non-stub `kimi`.

## Writes into lane/campaign tree

None. c2, c3, map-staged perform zero writes (stdout TSV/prints only; c3 opens the shokuknow `.qcache` captures read-only). c1's only writes are inside its TemporaryDirectory. No file outside the tempdir is created, modified, or deleted by any scanned file.

## Commands run (verbatim, trimmed)

- `read` c1-count.py (full), c2-count.py (full), c3-count.py (full), map-staged.py (full), claims.md, RULES.md; re-read elided ranges c1:35-39,51-63,77-119; c3:3-26,52-59,91-166.
- `grep` (pattern above) over the four files → hits as tabled; over parent-lifetime.sh and quarantine-check.py → `No matches found` twice; final sweep → `No matches found`.
- `bash`: `type kimi; command -v kimi; ls -la $(command -v kimi); echo $PATH` → `kimi is /home/vgpnk/.kimi-code/bin/kimi`, `-rwxr-xr-x ... 192285888 Oct 23 13:25 /home/vgpnk/.kimi-code/bin/kimi`, PATH ends `...:/home/vgpnk/.kimi-code/bin`.
- `read` parent-lifetime.sh:60-160 → bare `kimi` invocation at line 74; receipt/logdir paths derived from argv (under tmp when run by c1).
- Report path did not exist before write (ABSENT check).
- No tool installs performed (none needed). No scratch used under /tmp.

## Pointers

- c1-count.py:57-62 (subprocess argv/env), :86 (TemporaryDirectory), :89-91 (stub write/chmod), :45/:55 (in-tmp writes).
- parent-lifetime.sh:73-75 (timeout + bare `kimi` via PATH).
- map-staged.py:34 (local quarantine-check.py run).
- c3-count.py:127-131,143-146 (capture reads — open read-only).
