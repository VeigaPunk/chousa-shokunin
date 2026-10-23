#!/usr/bin/env bash
# minimal control: cost of ${s:0:1} vs string length, no functions, no fixtures
set -u
n=$1 iters=$2
s=$(printf 'x%.0s' $(seq 1 $n))
read -r a _ _ < /proc/self/schedstat
t0=${EPOCHREALTIME//[!0-9]/}
for ((i=0;i<iters;i++)); do c=${s:0:1}; done
t1=${EPOCHREALTIME//[!0-9]/}
read -r b _ _ < /proc/self/schedstat
printf 'len=%s iters=%s cpu_ns_per_iter=%s wall_us_per_iter=%s\n' "$n" "$iters" "$(( (b-a)/iters ))" "$(( (t1-t0)/iters ))"
