# FxSentinelMeta — verify-metadata security review

## Scope and checkpoint
- Full integration checked: `e93ac711f885a10d44fdd80a1734997419595b5a`; private clone `/tmp/chousa-r25-FxSentinelMeta`; gate SHA-256 `63a39282a15f19f5b0443212e66ad2dfc8ce0315e65697e479a7206879a598b2`.
- Packaging corrections: `git show 0fc037e6b07f3820ead8c9207a8034ac854197a1:tools/research-gate.sh | sha256sum` yielded `752e4e382ed77c06ac5030ce2179c7ca524934f86fd2a6b25ef946ab027ac553`; inspection found no `verify_metadata()` / `verify-metadata` mode. Intermediate `d8c8cff3923f10481ac9ced66d0af7c41d38130c` had the new gate but `git diff --name-only d8..e93` includes `corpus/evidence/README.md`; d8 and e93 gate blobs are byte-identical. Targeted gate probes below ran on d8's gate bytes, verified identical to final e93. No full suite run.
- Probes created only harmless `/tmp` fixtures and fake secret-shaped tokens; no network or credential/private target file was accessed.

## Findings

### HIGH — pathname checks are TOCTOU; `recheck` echoes a secret-shaped first token
- Evidence: `tools/research-gate.sh:2329-2347` canonicalizes/checks `$file`, then separately stats, NUL-probes, and parses via new opens of `$file`; no stable file-descriptor identity check. `:2430` writes the raw first token into the finding. `metadata-screen-r25.md:41-43` describes raw/canonical path denial and refusal, but does not state that later opens are bound to that checked object.
- Exploit/output: a controlled `/tmp` `wc` wrapper replaced a regular clean `race.md` with a symlink to a fake `/tmp/credentials/fake.md` only after the NUL probe consumed the original bytes. `post-NUL-check-swap: rc=0 swap_ran=True token_echo=True`; output included `FINDING META_RECHECK_UNSCHEDULED ... first-token=FAKE_CREDENTIAL_TOKEN_FOR_TEST_ONLY` and `RESEARCH_GATE: CLEAN`.
- Impact: a concurrent writer controlling the supplied path can substitute a denylisted target after screening; its `recheck:` first token is disclosed in stdout and the gate reports CLEAN. The exact probe is a local race, not evidence of remote reachability.
- Smallest remediation: read and validate/parse the same safely opened object (stable fd, size and identity checks; avoid path reopens); redact `recheck` token contents regardless.

### MEDIUM — hardlink alias bypasses path denylist and leaks first token
- Evidence: `tools/research-gate.sh:2329-2335` checks only raw/canonical path strings; it does not check inode link count. `metadata-screen-r25.md:41-43` documents pathname denial only.
- Exploit/output: linked a harmless fake file under `/tmp/.../.config/entry.md` to `/tmp/.../hardlink.md`; invocation returned `rc=0`, `RESEARCH_GATE: CLEAN`, with `first-token=FAKE_CREDENTIAL_TOKEN_FOR_TEST_ONLY`. No race was used.
- Impact: a readable denied inode with a benign hardlink pathname is parsed; an unscheduled `recheck:` can disclose its first token. Requires a same-filesystem link the caller can create.
- Smallest remediation: refuse `st_nlink != 1` before content reads (and keep token redaction).

### MEDIUM — size-cap fallback reads the entire file before refusing
- Evidence: `tools/research-gate.sh:709-715` falls back to `wc -c <"$1"` after both `stat` forms fail; `:2333` applies the cap only after that helper returns. `metadata-screen-r25.md:41-43` states over-8-MiB entries are “refused unread.”
- Exploit/output: with a local `/tmp` `stat` wrapper forcing both probes to fail, an 8-MiB+1 sparse fixture produced `wc_invocations=1`, then `reason=size`. `wc` consumed the file before refusal.
- Impact: the documented unread cap is false when `stat` is unavailable/fails; unbounded I/O/CPU remains for oversized input in that environment. Normal GNU `stat` on the reviewed host took the pre-read path.
- Smallest remediation: fail closed when metadata sizing is unavailable, or enforce a bounded read on one stable fd instead of `wc`.

### LOW — control bytes in names are emitted raw
- Evidence: `tools/research-gate.sh:2323,2448-2451` inserts basename and input path directly into output without escaping.
- Exploit/output: harmless filename `control<ESC>[2J<LF>spoof.md` passed through; captured output contained raw ESC and the injected line break (`ESC_preserved=True newline_injected=True`).
- Impact: terminal control and log-line confusion/forged-looking records; quoted shell arguments prevent this from being command execution.
- Smallest remediation: escape control bytes in every displayed path/basename, or reject control-byte names.

### LOW — safe direct file symlink is misreported as NUL
- Evidence: `tools/research-gate.sh:711-712` uses `stat` without dereferencing the final symlink; `:2335` compares that link-size with bytes read through the symlink target.
- Exploit/output: a harmless direct symlink to a valid regular `.md` fixture returned `rc=1` and `META_ENTRY_REFUSED ... reason=nul unparsed` despite containing no NUL. Directory symlinks to a fake `/.config/` target were correctly refused as `reason=denylist`.
- Impact: valid symlinked `.md` inputs are refused based on differing link/target lengths; misleading reason and incomplete screen, not secret disclosure by itself.
- Smallest remediation: size the same resolved/opened target that the NUL probe reads.

## Boundary checks
- FIFO direct path: `rc=2`, “not a .md file or directory”; directory containing only a FIFO: `rc=2`, “metadata directory has no .md files” — no FIFO read/hang observed (`tools/research-gate.sh:2304-2318`).
- Stable denylisted symlink-directory, >8-MiB regular file under normal `stat`, and NUL fixture were refused respectively as `reason=denylist`, `reason=size`, and `reason=nul` before header parsing (`:2329-2347`). These steady-state results do not cover hardlinks, concurrent path replacement, or the size fallback above.
- `SKILL.md:76` presents the metadata mode/status contract; `metadata-screen-r25.md:71-83` correctly limits it to key presence/shape, command-first rechecks, source support, and literal `--root ..` detection. Those are truthful scope limits, not new regressions. Hardlink and TOCTOU gaps are additional security boundaries, not claims that semantic verification is performed.

Installs: none. Clone files written: none (only `/tmp` probe fixtures, removed after capture).
VERDICT: Targeted tests confirm a local secret-disclosure path through hardlink aliases and a deterministic post-check TOCTOU; correct the unbound reads and raw token echo before treating pathname screening as a security boundary.