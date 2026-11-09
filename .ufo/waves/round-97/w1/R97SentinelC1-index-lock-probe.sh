#!/bin/bash
# Fixture-only probe: does `git status --porcelain` tolerate a held .git/index.lock? All git runs name -C "$D".
set -u
S=/fast/scratch/hyaku/chousa-r97/R97SentinelC1
D=$(mktemp -d -p "$S") && test -n "$D" && git -C "$D" init -q || exit 9
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D" || { echo "TOPLEVEL_MISMATCH"; exit 9; }
echo "fixture=$D"
cd "$D" || exit 9
echo a > f.txt
git -C "$D" add f.txt
git -C "$D" -c user.name=fixture -c user.email=fixture@invalid commit -q -m init
echo "--- no lock, status:"; git -C "$D" status --porcelain; echo "rc=$?"
echo "--- foreign lock held (empty index.lock), tracked file unchanged:"
: > "$D/.git/index.lock"
git -C "$D" status --porcelain; echo "rc=$?"
ls "$D/.git/index.lock" > /dev/null && echo "foreign_lock_present_after_status=yes"
rm -f "$D/.git/index.lock"
echo "--- foreign lock held, tracked file modified:"
echo b >> f.txt
: > "$D/.git/index.lock"
git -C "$D" status --porcelain; echo "rc=$?"
rm -f "$D/.git/index.lock"
echo "--- --no-optional-locks, foreign lock held:"
: > "$D/.git/index.lock"
git -C "$D" --no-optional-locks status --porcelain; echo "rc=$?"
rm -f "$D/.git/index.lock"
cd "$S" && rm -rf -- "$D"
echo "fixture_removed=$( [ -e "$D" ] && echo no || echo yes )"
