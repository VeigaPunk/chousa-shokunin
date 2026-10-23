#!/usr/bin/env bash
# Extracted unchanged: gate 3998-4026 (helper), 7041-7054 (source), 7568-7630 (cases).
set -euo pipefail
SELF=$1
WORK=$2
NOW_EPOCH=1792713600
cases=241
failures=0
mkdir -p "$WORK/lib"
  tclaims() {
    local name=$1 want_rc=$2
    shift 2
    local -a want=() over=()
    local a tok rc=0 out nverdict nvb ok=1
    # r15: CHOUSA_-prefixed args are env overrides (never want-tokens — the
    # bare ^[A-Z_]+= classifier would hijack VERDICT_BEARING_CLAIMS= etc.).
    for a in "$@"; do
      if [[ $a =~ ^CHOUSA_[A-Z_]+= ]]; then over+=("$a"); else want+=("$a"); fi
    done
    cases=$((cases + 1))
    out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 \
      CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
      "${over[@]+"${over[@]}"}" \
      bash "$SELF" verify-claims "$WORK/$name.jsonl" 2>&1) || rc=$?
    nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true)
    nvb=$(grep -c '^VERDICT_BEARING_CLAIMS=' <<<"$out" || true)
    for tok in "${want[@]+"${want[@]}"}"; do
      [[ $out == *"$tok"* ]] || ok=0
    done
    if [[ $rc -eq $want_rc && $nverdict -eq 1 && $nvb -eq 1 && $ok -eq 1 ]]; then
      printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" "$name" "$rc"
    else
      printf 'FAIL-case %-28s exit=%d want=%d verdicts=%d vbearing=%d token=%s\n' \
        "$name" "$rc" "$want_rc" "$nverdict" "$nvb" "${want[*]-}"
      printf '%s\n' "$out" | sed 's/^/    | /'
      failures=$((failures + 1))
    fi
  }
  mkdir -p "$WORK/lib"
  cat >"$WORK/lib/span.md" <<'EOF'
alpha beta gamma delta
epsilon zeta eta theta
iota kappa lambda mu
nu xi omicron pi
rho sigma tau upsilon
phi chi psi omega
trailing gamma delta
epsilon zeta leading
omega phi chi psi
iota kappa lambda muX appended
iota kappa lambda mu again
EOF
  cat >"$WORK/r33-top-nested-line.jsonl" <<'EOF'
{"id":"NB1","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","meta":{"line":"9"},"line":"1"}
EOF
  tclaims r33-top-nested-line 0 \
    'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=1/1' \
    'CLAIM id=NB1 expected=supported observed=supported source=lib/span.md at=line:1 verdict=match'
  # nested-only sha256 names a wrong pin: with no top-level sha256 the claim has
  # no pin and reads supported (a nested member is never the record's field).
  cat >"$WORK/r33-top-nested-sha.jsonl" <<'EOF'
{"id":"NB2","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","meta":{"sha256":"0000000000000000000000000000000000000000000000000000000000000000"}}
EOF
  tclaims r33-top-nested-sha 0 \
    'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=1/1' \
    'CLAIM id=NB2 expected=supported observed=supported source=lib/span.md at=line:1 verdict=match'
  # nested "id" decoy before the top-level id: the CLAIM line names the
  # top-level id, never the nested one.
  cat >"$WORK/r33-top-nested-id.jsonl" <<'EOF'
{"meta":{"id":"FAKEID"},"id":"NB3","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported"}
EOF
  tclaims r33-top-nested-id 0 \
    'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=1/1' \
    'CLAIM id=NB3 expected=supported observed=supported source=lib/span.md at=line:1 verdict=match'
  # duplicated top-level "line" (agreeing or not): invalid, top-level id kept.
  cat >"$WORK/r33-top-dup-line.jsonl" <<'EOF'
{"id":"DP1","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":"1","line":"9"}
EOF
  tclaims r33-top-dup-line 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_RECORD_INVALID severity=warn surface=claims' \
    'duplicate top-level key line' \
    'CLAIM id=DP1 expected=supported observed=invalid source=lib/span.md at=- verdict=invalid' \
    'VERDICT_BEARING_CLAIMS=0/1' \
    'claims=1 supported=0 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=1 findings=1 drift=1'
  # flat string confuser: braces, a bracket, a comma and a trailing escaped
  # backslash inside a string value are string content; the string ends at the
  # quote after \\, so the top-level "line" is still read.
  cat >"$WORK/r33-top-confuser-flat.jsonl" <<'EOF'
{"id":"FC1","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","note":"open { brace [ bracket , ends with a backslash \\","line":"1"}
EOF
  tclaims r33-top-confuser-flat 0 \
    'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=1/1' \
    'CLAIM id=FC1 expected=supported observed=supported source=lib/span.md at=line:1 verdict=match'
  # nested confuser container (a string holding } and ] then a wrong nested
  # "line") before the top-level "line": the container is skipped whole.
  cat >"$WORK/r33-top-confuser-nested.jsonl" <<'EOF'
{"id":"FC2","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","meta":{"note":"close } brace ] bracket { open","line":"9"},"line":"1"}
EOF
  tclaims r33-top-confuser-nested 0 \
    'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=1/1' \
    'CLAIM id=FC2 expected=supported observed=supported source=lib/span.md at=line:1 verdict=match'
  # duplicated "id": both records are invalid; the CLAIM line keeps the id when
  # the two values are byte-identical and falls back to id=line<N> when they
  # differ (the id is then as unreadable as any other).
  cat >"$WORK/r33-top-dup-id.jsonl" <<'EOF'
{"id":"DI1","id":"DI1","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported"}
{"id":"DI2","id":"DI3","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported"}
EOF
  tclaims r33-top-dup-id 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_RECORD_INVALID severity=warn surface=claims' \
    'duplicate top-level key id' \
    'CLAIM id=DI1 expected=supported observed=invalid source=lib/span.md at=- verdict=invalid' \
    'CLAIM id=line2 expected=supported observed=invalid source=lib/span.md at=- verdict=invalid' \
    'VERDICT_BEARING_CLAIMS=0/2' \
    'claims=2 supported=0 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=2 findings=2 drift=2'
printf 'R33_TARGETED_SELFTEST: failures=%d cases=7 original=242-248\n' "$failures"
[[ $failures -eq 0 ]]
