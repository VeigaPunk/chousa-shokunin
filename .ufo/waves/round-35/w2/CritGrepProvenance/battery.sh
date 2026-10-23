#!/usr/bin/env bash
# Attack scenarios T1..T14 (critic, round-35 C1). Scratch only.
set -u
GATE=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
W=/tmp/hyaku/chousa-r35/w2/CritGrepProvenance
cd "$W"
mkdir -p arms

run() { # name env... -- cmd...
  local name=$1; shift
  local envspec=()
  while [[ $1 != -- ]]; do envspec+=("$1"); shift; done
  shift
  env -i PATH=/usr/local/bin:/usr/bin:/bin HOME="$W" "${envspec[@]}" \
    timeout 120 bash "$GATE" verify-claims "$W/fx/claims.jsonl" --root "$W/fx" \
    >"$W/$name.out" 2>"$W/$name.err"
  local rc=$?
  local obs
  obs=$(grep -a "^CLAIM id=K1" "$W/$name.out" | grep -ao "verdict=\S*" | head -1)
  local prov; prov=$(grep -a "GREP_PROVENANCE" "$W/$name.err" | head -1 | head -c 160)
  local echo_; echo_=$(grep -a "GATE_GREP:" "$W/$name.err" | head -1 | head -c 160)
  printf '%-18s rc=%-3s %-14s %s %s\n' "$name" "$rc" "$obs" "$prov" "$echo_"
}

# T1 wrapper-lie: GNU line for --version, logging shim for everything else
cat > arms/wrap-lie.sh <<'EOF'
#!/bin/sh
if [ "$1" = "--version" ]; then echo 'grep (GNU grep) 9.9.9-critic'; exit 0; fi
printf 'ARGS %s\n' "$*" >> /tmp/hyaku/chousa-r35/w2/CritGrepProvenance/arms/t1-trip.log
exec /usr/bin/grep "$@"
EOF
chmod +x arms/wrap-lie.sh; : > arms/t1-trip.log

# T2 symlink to non-GNU binary (true)
ln -sf /usr/bin/true arms/grep-true

# T3 directory as override
mkdir -p arms/dir-as-grep

# T4 FIFO as override
rm -f arms/fifo-grep; mkfifo arms/fifo-grep

# T5 0-byte executable
: > arms/zero-grep; chmod +x arms/zero-grep

# T6 real GNU grep at path with space
cp /usr/bin/grep "arms/grep with space"

# T7 real GNU grep at path with newline
cp /usr/bin/grep $'arms/grep\nnl'

# T8 --version exits nonzero
cat > arms/nonzero-grep <<'EOF'
#!/bin/sh
if [ "$1" = "--version" ]; then echo 'grep (GNU grep) 1.0' >&2; exit 3; fi
exec /usr/bin/grep "$@"
EOF
chmod +x arms/nonzero-grep

# T9 --version prints nothing
cat > arms/silent-grep <<'EOF'
#!/bin/sh
[ "$1" = "--version" ] && exit 0
exec /usr/bin/grep "$@"
EOF
chmod +x arms/silent-grep

# T10 GNU on line 2 only
cat > arms/line2-grep <<'EOF'
#!/bin/sh
if [ "$1" = "--version" ]; then echo 'bogus line one'; echo 'grep (GNU grep) 2.0'; exit 0; fi
exec /usr/bin/grep "$@"
EOF
chmod +x arms/line2-grep

# T12 BASH_ENV head() shim + non-GNU override (S6 combo)
cat > arms/bashenv-head.sh <<'EOF'
head() { echo 'grep (GNU grep) 3.11-fake'; }
EOF

# T13 BASH_ENV command() shim
cat > arms/bashenv-command.sh <<'EOF'
command() { printf 'CMDFN %s\n' "$*" >> /tmp/hyaku/chousa-r35/w2/CritGrepProvenance/arms/t13-trip.log; builtin command "$@"; }
EOF
: > arms/t13-trip.log

# T14 BASH_ENV head() shim only, default resolution
run t1-wrap-lie      RESEARCH_GATE_GREP="$W/arms/wrap-lie.sh" CHOUSA_GREP_PIN_ECHO=1 --
run t2-sym-non-gnu   RESEARCH_GATE_GREP="$W/arms/grep-true" --
run t3-dir           RESEARCH_GATE_GREP="$W/arms/dir-as-grep" --
run t4-fifo          RESEARCH_GATE_GREP="$W/arms/fifo-grep" --
run t5-zero          RESEARCH_GATE_GREP="$W/arms/zero-grep" --
run t6-space         RESEARCH_GATE_GREP="$W/arms/grep with space" --
run t7-newline       RESEARCH_GATE_GREP="$W/arms/grep
nl" --
run t8-nonzero       RESEARCH_GATE_GREP="$W/arms/nonzero-grep" --
run t9-silent        RESEARCH_GATE_GREP="$W/arms/silent-grep" --
run t10-line2        RESEARCH_GATE_GREP="$W/arms/line2-grep" --
run t12-headplusstub RESEARCH_GATE_GREP="$W/arms/wrap-lie.sh" BASH_ENV="$W/arms/bashenv-head.sh" CHOUSA_GREP_PIN_ECHO=1 --
run t13-cmdfn        BASH_ENV="$W/arms/bashenv-command.sh" CHOUSA_GREP_PIN_ECHO=1 --
run t14-headonly     BASH_ENV="$W/arms/bashenv-head.sh" CHOUSA_GREP_PIN_ECHO=1 --

echo "--- t1 tripwire (calls that reached wrap-lie):"; wc -l < arms/t1-trip.log
echo "--- t13 tripwire (command() interceptions):"; wc -l < arms/t13-trip.log
