# W2ExecNoNet — curl / wget / urlopen in parent-lifetime.sh

Seat: W2ExecNoNet (leaf executor). Axes: operability (the assigned grep ran and the paste is the result), calibration (grep exit 1 is no-match, not a failed script; token absence is not a network proof), depth (worktree and HEAD blob, the one dirty hunk, and the commands this file does name). No production file, git index, or jj state was written. No fetch. No descendant spawned. The script was not executed: running it would spawn seats and append a receipt, which this check does not require.

Verdict: matching lines for `curl`, `wget`, or `urlopen` in `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/parent-lifetime.sh`: **none**.

```text
MATCHING_LINES=none
ASSIGNED_HITS=0
```

This does not score R44-C1. `corpus/evidence/round44/claims.md` does not predicate curl/wget/urlopen. That claim was not retuned.

## Assigned grep

Pattern: `curl|wget|urlopen`. Subject path only. One copy of that name exists under the lane (`find` printed only `tools/parent-lifetime.sh`).

Grep tool on that path:

```text
No non-sensitive matches found
```

That wording can hide a "sensitive" hit. A raw grep cannot. Quoted shell, worktree file, 2026-10-24:

```text
=== assigned grep -n -E ===
EXIT:1
=== assigned grep -n -E -i ===
EXIT:1
=== assigned grep -n -F each ===
curl_EXIT:1
wget_EXIT:1
urlopen_EXIT:1
=== wc / sha256 / file / stat ===
 108 3352 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/parent-lifetime.sh
f3b0baac457710d6a210ad4e1f27e8d398f6b51c58290d8c90fea8bdca3e33cb  /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/parent-lifetime.sh
/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/parent-lifetime.sh: Bourne-Again shell script, Unicode text, UTF-8 text executable
mode=755 nlink=1 size=3352 mtime=2026-10-24 21:49:24.365738999 -0300
=== git identity (read-only) ===
043f19a1db91288947493d9f879e61e7a9f07241
 M tools/parent-lifetime.sh
79ee8f2942802ee1d1771a7e5887a7a9a36cdb8b
6071f9f835877d6a9b89b0414b385ee894e3837d
=== byte compare worktree vs HEAD ===
 tools/parent-lifetime.sh | 4 +++-
 1 file changed, 3 insertions(+), 1 deletion(-)
DIFF_EXIT:0
```

`grep` with no selected line exits 1 and prints nothing. That is the no-match convention. It is not a usage error and not a failed measurement. `DIFF_EXIT:0` is `git diff --stat` succeeding while reporting a dirty path. The porcelain line ` M tools/parent-lifetime.sh` is the dirty signal. This seat did not write that diff.

Independent substring count on the same worktree bytes (`BYTES=3352`, `LINES=108`, `NUL=0`):

```text
ASSIGNED_SUBSTRING_HITS 0
COUNT curl=0 casefold=0
COUNT wget=0 casefold=0
COUNT urlopen=0 casefold=0
```

HEAD blob, same pattern (`git show HEAD:tools/parent-lifetime.sh | grep -n -E 'curl|wget|urlopen'`):

```text
HEAD_GREP_EXIT:1
```

Empty stdout. HEAD blob sha256 `f51a69b83d58ba88eee24b69b41fef9d60d22dccf7f951be5342fdb729988a75` (3212 bytes). Worktree git blob `79ee8f2942802ee1d1771a7e5887a7a9a36cdb8b`. HEAD path blob `6071f9f835877d6a9b89b0414b385ee894e3837d`. Tip `043f19a1db91288947493d9f879e61e7a9f07241` (`round-44: freeze parent-lifetime, disposition, and RFC quote claims before scoring`, 2026-10-24 21:46:56 -0300). Token counts: HEAD and worktree both `curl=0 wget=0 urlopen=0`.

## What the dirty hunk is

The worktree is not the freeze commit. The only hunk drops `--auto` from the `kimi` argv and adds a comment. Neither side introduces or removes `curl`, `wget`, or `urlopen`.

```text
diff --git i/tools/parent-lifetime.sh w/tools/parent-lifetime.sh
index 6071f9f..79ee8f2 100755
--- i/tools/parent-lifetime.sh
+++ w/tools/parent-lifetime.sh
@@ -68,8 +68,10 @@ PY
     prompt_file="$logdir/$name.prompt"
     printf '%s\n' "$body" > "$prompt_file"
     # Same shell owns the background pid. Not a pipeline.
+    # --auto and --yolo cannot combine with --prompt (kimi 2.3.1). The host
+    # default permission mode is already auto, so the flag is omitted.
     timeout --signal=TERM --kill-after=20 "$TIMEOUT" \
-      kimi --agent-file "$AGENT" --auto --prompt "$(cat "$prompt_file")" \
+      kimi --agent-file "$AGENT" --prompt "$(cat "$prompt_file")" \
       --output-format text > "$logdir/$name.log" 2>&1 &
```

`--auto` count is 1 on both sides (flag in HEAD, comment in the worktree). `kimi` count is 1 in HEAD and 2 in the worktree (comment plus the argv). Still no assigned token.

## What "none" does not clear

The file names other programs. A token grep does not resolve `PATH`, aliases, or those programs' own sockets. This seat did not trace the `kimi` binary and does not claim it is offline.

Commands the script text actually invokes or names as commands (comment hits included in the scan): `echo`, `timeout` (flag and the `timeout(1)` argv), `date`, `mkdir`, `printf`, `sleep` (selftest only), `mapfile`, `python3`, `kimi`, `cat`, `wait`. No `curl`, `wget`, `nc`, `ssh`, `git`, `jj`, `scp`, or `rsync` in that inventory.

The only Python block is a local JSON read, lines 53–59:

```text
53:  mapfile -t TASKS < <(python3 - "$DISPATCH" << 'PY'
54:import json, sys
55:doc = json.load(open(sys.argv[1], encoding="utf-8"))
56:tasks = doc["taskCall"]["tasks"]
57:for t in tasks:
58:    # name, then the task text, separated by a unit separator
59:    sys.stdout.write(t["name"] + "\x1f" + t["task"].replace("\n", "\x1e") + "\n")
```

`open(sys.argv[1])` is the dispatch file. It is not `urlopen`. The heredoc ends at line 60. There is no import of `urllib`, `requests`, `socket`, `http.client`, or `subprocess`.

Task text is written to a prompt file and passed as one quoted argument. It is not eval'd:

```text
69:    printf '%s\n' "$body" > "$prompt_file"
73:    timeout --signal=TERM --kill-after=20 "$TIMEOUT" \
74:      kimi --agent-file "$AGENT" --prompt "$(cat "$prompt_file")" \
75:      --output-format text > "$logdir/$name.log" 2>&1 &
```

`"$(cat "$prompt_file")"` is a quoted command substitution. The shell does not execute the prompt body. A seat instruction that contains the words `curl` or `wget` is data to `kimi`, not a call by `parent-lifetime.sh`.

That trap is live. `.ufo/waves/round-44/w2-dispatch.json` contains those words (this seat's own item/task, and the wave contract line that forbids curl and wget). Those lines are not lines of `tools/parent-lifetime.sh`. A directory grep of the wave would be a different question and would not be a hit of the assigned file.

Adjacent tokens in the script, case-insensitive, also none: `urllib`, `requests`, `socket`, `http://`, `https://`, `fetch`, `/dev/tcp`, `nc`, `ssh`, `httpx`, `aiohttp`, `ftplib`, `urlretrieve`, `WebClient`, `Invoke-WebRequest`.

```text
ADJACENT_HITS=0
```

The residual is the `kimi` child on line 74 (HEAD: the same argv plus `--auto`). Whether that child opens a socket is outside the assigned tokens and was not measured.

## Remaining risks

- Bound to the bytes hashed above. A later edit of `tools/parent-lifetime.sh` is not covered.
- "None" is absence of those three substrings in this file (case-sensitive and casefold). It is not a runtime ban, not a `kimi` trace, and not C1.
- `PATH` aliases for `date`, `timeout`, `python3`, or `kimi` were not resolved. The script text does not spell a network client.
- The live wave receipt was not scored. This seat did not wait, reap, or rewrite it.

## Blockers

None for the assigned grep.
