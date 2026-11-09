#!/bin/bash
# Fixture-only: does `git status --porcelain` see an ignored write and an untracked write? All git runs name -C "$D".
set -u
S=/fast/scratch/hyaku/chousa-r97/R97SentinelC1
D=$(mktemp -d -p "$S") && test -n "$D" && git -C "$D" init -q || exit 9
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D" || { echo "TOPLEVEL_MISMATCH"; exit 9; }
echo "fixture=$D"
printf '__pycache__/\n*.pyc\n' > "$D/.gitignore"
echo tracked > "$D/t.txt"
git -C "$D" add -A
git -C "$D" -c user.name=fixture -c user.email=fixture@invalid commit -q -m init
mkdir -p "$D/tools/__pycache__"; echo x > "$D/tools/__pycache__/w.cpython-314.pyc"; echo x > "$D/new-untracked.txt"
echo "--- git status --porcelain:"; git -C "$D" status --porcelain; echo "rc=$?"
echo "--- git status --porcelain --ignored:"; git -C "$D" status --porcelain --ignored; echo "rc=$?"
cd "$S" && rm -rf -- "$D"; echo "fixture_removed=$( [ -e "$D" ] && echo no || echo yes )"
