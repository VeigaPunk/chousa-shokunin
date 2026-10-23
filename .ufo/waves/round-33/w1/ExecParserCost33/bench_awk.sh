#!/usr/bin/env bash
# gawk equivalent: CPU time of the child (via bash times children line) per line.
# usage: LC_ALL=<locale> bench_awk.sh <input> <lines> [awkprog]
set -u
f=$1 lines=$2 prog=${3:-walk.awk}
tous() { # "1m2.345s" -> microseconds
  local v=$1 m r i fr
  m=${v%%m*}; r=${v#*m}; r=${r%s}
  i=${r%%.*}; fr=${r#*.}; fr="${fr}000000"; fr=${fr:0:6}
  echo $((10#$m * 60000000 + 10#$i * 1000000 + 10#$fr))
}
times > .awk_t1
w0=${EPOCHREALTIME//[!0-9]/}
awk -f "$prog" "$f" > .awk_out
w1=${EPOCHREALTIME//[!0-9]/}
times > .awk_t2
{ read -r _u1 _s1; read -r cu1 cs1; } < .awk_t1
{ read -r _u2 _s2; read -r cu2 cs2; } < .awk_t2
cpu=$(( $(tous "$cu2") - $(tous "$cu1") + $(tous "$cs2") - $(tous "$cs1") ))
wall=$((w1 - w0))
printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
  "${LC_ALL:-unset}" "$prog" "$lines" "$cpu" "$wall" \
  "$((cpu * 1000 / lines))" "$((wall * 1000 / lines))"
