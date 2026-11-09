#!/bin/bash
# Derives the R97SentinelC1 receipts from the raw strace traces (raw traces stay in scratch and are deleted at yield).
set -u
S=/fast/scratch/hyaku/chousa-r97/R97SentinelC1
W=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-97/w1
R=$S/repo
WR='O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND'
MUT='\b(unlink|unlinkat|rename|renameat2|mkdir|mkdirat|rmdir|truncate|chmod|fchmodat|utimensat|symlink|symlinkat|link|linkat|chown|fchownat)\('
GITMUT=', "(update-ref|commit|add|gc|repack|reset|checkout|stash|fetch|write-tree|read-tree|index-pack|replace|init|clone|pack-refs|prune|worktree|symbolic-ref|tag|branch|push|apply|am|rebase|merge|config|hash-object|update-index)"'

summ() { # TRACE OUT WORKMARK(or NOWORK)
  local T=$1 O=$2 WM=$3
  {
    echo "trace=$(basename "$T") lines=$(wc -l < "$T")"
    echo "write_mode_opens_total=$(/usr/bin/grep -E 'open(at)?\(' "$T" | /usr/bin/grep -cE "$WR")"
    echo "write_mode_opens_excl_devnull=$(/usr/bin/grep -E 'open(at)?\(' "$T" | /usr/bin/grep -E "$WR" | /usr/bin/grep -vc '/dev/null')"
    echo "write_mode_opens_outside_workdir_excl_devnull_and_indexlock=$(/usr/bin/grep -E 'open(at)?\(' "$T" | /usr/bin/grep -E "$WR" | /usr/bin/grep -v '/dev/null' | /usr/bin/grep -v 'index.lock' | /usr/bin/grep -vc "$WM")"
    echo "index_lock_O_CREAT_O_EXCL=$(/usr/bin/grep -c 'index.lock.*O_EXCL' "$T")"
    echo "index_lock_unlink=$(/usr/bin/grep -c 'unlink("[^"]*index.lock")' "$T")"
    echo "rename_calls=$(/usr/bin/grep -cE '\brename(at2|at)?\(' "$T")"
    echo "mutating_syscall_lines_total=$(/usr/bin/grep -cE "$MUT" "$T")"
    echo "mutating_syscall_lines_absolute_path_outside_workdir_excl_indexlock=$(/usr/bin/grep -E "$MUT" "$T" | /usr/bin/grep -E '"/' | /usr/bin/grep -v "$WM" | /usr/bin/grep -vc 'index.lock')"
    echo "socket_connect_sendto_getaddrinfo=$(/usr/bin/grep -cE '\b(socket|connect|sendto|getaddrinfo)\(' "$T")"
    echo "address_family_AF_INET_or_AF_UNIX=$(/usr/bin/grep -cE 'AF_INET|AF_UNIX' "$T")"
    echo "tmp_paths=$(/usr/bin/grep -c '"/tmp' "$T")"
    echo "execve_successful_by_program:"
    /usr/bin/grep -E 'execve\(' "$T" | /usr/bin/grep -v ENOENT | sed -E 's/^[0-9]+ +//; s/, \[.*//' | sort | uniq -c | sort -rn
    echo "git_subcommand_tokens_on_usr_bin_git_execve:"
    /usr/bin/grep -E 'execve\("/usr/bin/git", \[' "$T" | /usr/bin/grep -oE ', "[a-z][a-z-]+"(, |\])' | sort | uniq -c | sort -rn
    echo "mutating_git_subcommand_execs=$(/usr/bin/grep -E 'execve\("/usr/bin/git", \[' "$T" | /usr/bin/grep -cE "$GITMUT")"
  } > "$O"
  echo "wrote $O"
}

summ "$S/st-strace.txt" "$W/R97SentinelC1-selftest-strace-summary.txt" NOWORK
summ "$S/c1-battery-strace.txt" "$W/R97SentinelC1-c1-battery-strace-summary.txt" work-c1
summ "$S/entry-strace.txt" "$W/R97SentinelC1-entry-strace-summary.txt" work-entry
/usr/bin/grep -E 'index\.lock' "$S/c1-battery-strace.txt" | sed -E 's/^([0-9]+) +/pid=\1 /' > "$W/R97SentinelC1-c1-index-lock-lines.txt"
echo "wrote index-lock lines: $(wc -l < "$W/R97SentinelC1-c1-index-lock-lines.txt")"
cp "$S/c1-battery-stdout.txt" "$W/R97SentinelC1-c1-battery-stdout.txt"
cp "$S/c1-battery-stderr.txt" "$W/R97SentinelC1-c1-battery-stderr.txt"
cp "$S/entry-stdout.txt" "$W/R97SentinelC1-entry-controls-stdout.txt"
cp "$S/entry-stderr.txt" "$W/R97SentinelC1-entry-controls-stderr.txt"
cp "$S/st-stdout.txt" "$W/R97SentinelC1-selftest-stdout.txt"
cp "$S/c1-status-before.txt" "$W/R97SentinelC1-c1-clone-status-before.txt"
cp "$S/c1-status-after.txt" "$W/R97SentinelC1-c1-clone-status-after.txt"
cp "$S/harness-r13.py" "$W/R97SentinelC1-harness-r13.py"
echo "receipts copied"
