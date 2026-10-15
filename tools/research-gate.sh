#!/usr/bin/env bash
# research-gate.sh — chousa research-record method gate (probation r1).
#
# Validates Markdown research records: question, ranked sources, chain hops
# resolved-or-marked, pointed claims, kept rejections, negative sweeps;
# hard bounds on external fetch, secrecy, session paths.
#
# Verdict: RESEARCH_GATE: CLEAN|DRIFT
# Exit:    0 CLEAN | 1 DRIFT | 2 setup/usage
# Selftest: RESEARCH_GATE_SELFTEST: PASS (N cases) | FAIL (fail/N)
# Severity: warn|crit always drift; info drifts only under CHOUSA_STRICT=1.
# Recording a finding is never itself fatal, so a pass that gets far enough to
# evaluate the record always closes with exactly one verdict summary.
#
# FINDING <ID> severity=<info|warn|crit> surface=<family> obs=<short>
#
# Preferred ids: NO_QUESTION UNRANKED_SOURCE SOURCE_TABLE_ABSENT
#   HIERARCHY_PRIMARY_LIE CHAIN_HOP_UNRESOLVED CHAIN_ABSENT
#   CLAIM_UNPOINTED CLAIM_TABLE_ABSENT POINTER_EPHEMERAL POINTER_UNRESOLVED
#   REJECTION_DROPPED REJECTION_REASON_ABSENT NEGATIVE_WITHOUT_SWEEP
#   OBS_INFERENCE_COLLAPSE EXTERNAL_WITHOUT_APPROVAL SECRET_SHAPED
#   SESSION_READ RECORD_SCHEMA_INVALID EXPORT_CHROME_PRESENT
#
# Secrecy: print path:line class=<name> only — never span.
# Opens: allowlist metadata only; denylist → SESSION_READ.
# research/README CDP 9222 is provenance, not a hop.
#
set -euo pipefail
shopt -s extglob

VERSION=research-gate-r1
SELF=$(readlink -f -- "${BASH_SOURCE[0]}" 2>/dev/null || {
  p=$0; case "$p" in /*) printf '%s' "$p" ;; *) printf '%s' "$PWD/$p" ;; esac
})
SCRIPT_DIR=$(cd -- "$(dirname -- "$SELF")" && pwd)
LANE_ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd)

MODE=verify
RECORD_ARG=""
ROOT=${CHOUSA_ROOT:-$PWD}
STRICT=${CHOUSA_STRICT:-0}
AGG_ERE=${CHOUSA_AGGREGATOR_ERE:-'aggregator|wikipedia|secondary-summary|chat-export-sources'}
NOW_EPOCH=${CHOUSA_NOW_EPOCH:-}
[[ -n $NOW_EPOCH ]] || NOW_EPOCH=$(date +%s)
TS_UTC=$(date -u -d "@$NOW_EPOCH" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null \
  || date -u -r "$NOW_EPOCH" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null \
  || date -u +%Y-%m-%dT%H:%M:%SZ)

N_FINDINGS=0 N_DRIFT=0 ROLL=CLEAN
declare -a FINDING_LINES=()

N_Q=0 N_SRC=0 N_CH=0 N_CL=0 N_NEG=0 N_REJ=0 N_APPR=0
HAS_META=0 HAS_SOURCES_SEC=0 HAS_CHAIN_SEC=0 HAS_CLAIMS_SEC=0
HAS_REJ_SEC=0 HAS_NEG_SEC=0 HAS_APPROVAL_SEC=0 HAS_SWEEP_SEC=0
SCHEMA_HINT=0 WINDOW_EXTERNAL=0 APPROVAL_GRANTED=0 REJECT_MARKERS=0

usage() {
  cat <<'EOF'
usage: research-gate.sh [--selftest] [--help]
       research-gate.sh verify [--record PATH] [--root PATH]
       research-gate.sh [--record PATH] [--root PATH]

  RECORD via --record, positional, or CHOUSA_RECORD.
Verdict: RESEARCH_GATE: CLEAN|DRIFT
Exit:    0 CLEAN | 1 DRIFT | 2 setup/usage
EOF
}

die_usage() { printf 'research-gate: %s\n' "$1" >&2; usage >&2; exit 2; }

emit_finding() { # id severity surface obs
  local id=$1 sev=$2 surface=$3 obs=$4
  N_FINDINGS=$((N_FINDINGS + 1))
  FINDING_LINES+=("FINDING $id severity=$sev surface=$surface obs=$obs")
  case "$sev" in
    warn|crit) N_DRIFT=$((N_DRIFT + 1)); ROLL=DRIFT ;;
    info) [[ $STRICT == 1 ]] && { N_DRIFT=$((N_DRIFT + 1)); ROLL=DRIFT; } ;;
  esac
  # Finding severity affects counters and ROLL, not control flow. A false return
  # here would abort the CLI under errexit before its deferred verdict prints.
  return 0
}

declare -A SEC_BODY=()
declare -a SEC_ORDER=()

load_sections() {
  local file=$1 line sec=""
  SEC_BODY=(); SEC_ORDER=()
  while IFS= read -r line || [[ -n $line ]]; do
    if [[ $line =~ ^##[[:space:]]+(.*)$ ]]; then
      sec=$(printf '%s' "${BASH_REMATCH[1]}" | sed 's/[[:space:]]*$//')
      case "$sec" in
        "Source table") sec="Sources" ;;
        Chains) sec="Chain" ;;
        Approvals) sec="Approval" ;;
      esac
      SEC_ORDER+=("$sec")
      SEC_BODY[$sec]=""
      continue
    fi
    [[ -z $sec ]] && continue
    SEC_BODY[$sec]+="$line"$'\n'
  done <"$file"
}

table_rows() {
  local sec=$1 body row
  body=${SEC_BODY[$sec]-}
  [[ -n $body ]] || return 0
  local -a headers=()
  local header_done=0
  while IFS= read -r row; do
    [[ $row == \|*\|* ]] || continue
    local inner=${row#|}
    inner=${inner%|}
    if [[ $header_done -eq 0 ]]; then
      if [[ $inner =~ ^[[:space:]]*-+ ]]; then
        header_done=1
        continue
      fi
      if [[ ${#headers[@]} -eq 0 ]]; then
        IFS='|' read -r -a headers <<<"$inner"
        local i
        for i in "${!headers[@]}"; do
          headers[$i]=$(printf '%s' "${headers[$i]}" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | tr 'A-Z' 'a-z')
        done
        continue
      fi
    fi
    [[ $inner =~ ^[[:space:]]*-+ ]] && continue
    local -a cols=()
    IFS='|' read -r -a cols <<<"$inner"
    local j out=""
    for j in "${!headers[@]}"; do
      local c=${cols[$j]-}
      c=$(printf '%s' "$c" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
      out+="${headers[$j]}=$c"$'\t'
    done
    printf '%s\n' "$out"
  done <<<"$body"
}

cell() {
  local row=$1 key=$2
  key=$(printf '%s' "$key" | tr 'A-Z' 'a-z')
  case "$key" in
    rank) key=tier ;;
    src_id) key=id ;;
    path_or_token|path|points_to) key=pointer ;;
    to_token) key=to ;;
  esac
  local e k v
  IFS=$'\t' read -r -a ents <<<"$row"
  for e in "${ents[@]}"; do
    [[ $e == *'='* ]] || continue
    k=${e%%=*}; v=${e#*=}
    k=$(printf '%s' "$k" | tr 'A-Z' 'a-z')
    case "$k" in
      rank) k=tier ;;
      src_id) k=id ;;
      path_or_token|path|points_to) k=pointer ;;
      to_token) k=to ;;
    esac
    if [[ $k == "$key" ]]; then printf '%s' "$v"; return 0; fi
  done
  printf ''
}

section_nonempty_prose() {
  local sec=$1
  # `local a=1 b=${ARR[$a]-}` expands every right-hand side BEFORE assigning, so
  # $sec is unset here and `set -u` aborts (measured: `line 165: sec: unbound
  # variable` killed 13 of 17 selftest cases). Split the declaration.
  local line body=${SEC_BODY[$sec]-}
  [[ -n $body ]] || return 1
  while IFS= read -r line; do
    [[ -z ${line//[[:space:]]/} ]] && continue
    [[ $line == \|* ]] && continue
    [[ $line == \<!--* ]] && continue
    return 0
  done <<<"$body"
  local n
  n=$(table_rows "$sec" | grep -c . || true)
  [[ ${n:-0} -gt 0 ]]
}

norm_ptr() {
  local p=$1
  p=${p#\`}; p=${p%\`}
  printf '%s' "$p"
}

ptr_file_part() {
  local p; p=$(norm_ptr "$1")
  printf '%s' "${p%%:*}"
}

is_ephemeral_ptr() {
  [[ $(norm_ptr "$1") =~ ^(local|artifact|agent|proc|history):// ]]
}

is_url_ptr() {
  [[ $(norm_ptr "$1") =~ ^https?:// ]]
}

is_session_url() {
  local p; p=$(norm_ptr "$1")
  [[ $p =~ :9222(/|$) || $p =~ /json(/|list)?$ ]]
}

DEAD_MARK_RE='ephemeral|scratch|historical|unresolved|lost-tree|lost-base|formerly|removed|relocat|labelled-dead|blocked-no-fetch|proposal'

line_has_mark() { grep -qiE "$DEAD_MARK_RE" <<<"$1"; }

is_denylist_path() {
  local f; f=$(ptr_file_part "$1")
  case "$f" in
    *op.env|*.env|*server.token*|*credentials/*|*/oauth/*) return 0 ;;
  esac
  [[ $f == *chrome-profile* || $f == *Cookies* || $f == *"Login Data"* ]] && return 0
  [[ $f == *'/.omp/'* || $f == *'/.config/'* || $f == *'/.local/state/'* ]] && return 0
  return 1
}

ptr_resolves_meta() {
  local p f
  p=$(norm_ptr "$1")
  is_ephemeral_ptr "$p" && return 1
  is_url_ptr "$p" && return 1
  is_denylist_path "$p" && return 1
  f=$(ptr_file_part "$p")
  [[ -z $f ]] && return 1
  if [[ $f != /* ]]; then
    [[ -f $ROOT/$f || -f $LANE_ROOT/$f ]] && return 0
    return 1
  fi
  local root_r
  root_r=$(cd -- "$ROOT" 2>/dev/null && pwd -P || printf '%s' "$ROOT")
  case "$f" in
    "$root_r"/*) [[ -f $f ]] && return 0 ;;
  esac
  return 1
}

check_pointer() {
  local ptr=$1 row=$2 surface=$3 ctx=$4
  ptr=$(norm_ptr "$ptr")
  if [[ -z $ptr ]]; then
    emit_finding CLAIM_UNPOINTED warn "$surface" "ctx=$ctx empty pointer"
    return 1
  fi
  if is_session_url "$ptr" || is_denylist_path "$ptr"; then
    emit_finding SESSION_READ crit secrecy "ctx=$ctx path=$(ptr_file_part "$ptr") denied (not opened)"
    return 1
  fi
  if is_ephemeral_ptr "$ptr"; then
    if line_has_mark "$row"; then return 0; fi
    emit_finding POINTER_EPHEMERAL warn "$surface" "ctx=$ctx ptr_class=ephemeral unlabeled"
    return 1
  fi
  if is_url_ptr "$ptr"; then
    if [[ $APPROVAL_GRANTED -eq 1 && $WINDOW_EXTERNAL -eq 1 ]]; then return 0; fi
    emit_finding EXTERNAL_WITHOUT_APPROVAL crit approval "ctx=$ctx url pointer without approved external window"
    return 1
  fi
  # declared source id (S1, …) is a valid pointer once Sources pass filled SRC_TIER
  if [[ $ptr =~ ^S[A-Za-z0-9_-]+$ ]]; then
    if [[ -n ${SRC_TIER[$ptr]+x} ]]; then return 0; fi
    emit_finding POINTER_UNRESOLVED warn "$surface" "ctx=$ctx source_id=$ptr not in ## Sources"
    return 1
  fi
  if ptr_resolves_meta "$ptr"; then return 0; fi
  if line_has_mark "$row"; then return 0; fi
  emit_finding POINTER_UNRESOLVED warn "$surface" "ctx=$ctx ptr=$(printf '%.80s' "$ptr") missing under CHOUSA_ROOT"
  return 1
}

scan_secrets() {
  local file=$1 lineno=0 line class
  while IFS= read -r line || [[ -n $line ]]; do
    lineno=$((lineno + 1))
    class=""
    if [[ $line =~ op:// ]]; then class=op_uri
    elif [[ $line =~ Bearer[[:space:]]+[A-Za-z0-9._~+/=-]{8,} ]]; then class=bearer
    elif [[ $line =~ sk-[A-Za-z0-9_]{10,} ]]; then class=sk_prefix
    elif [[ $line =~ ghp_[A-Za-z0-9]{20,} ]]; then class=ghp_prefix
    elif [[ $line =~ github_pat_[A-Za-z0-9_]{10,} ]]; then class=github_pat
    elif [[ $line =~ AKIA[A-Z0-9]{12,} ]]; then class=aws_akia
    elif [[ $line =~ BEGIN[[:space:]]+OPENSSH[[:space:]]+PRIVATE[[:space:]]+KEY ]]; then class=ssh_key
    elif [[ $line =~ BEGIN[[:space:]]+([A-Z]+[[:space:]]+)?PRIVATE[[:space:]]+KEY ]]; then class=pem_key
    elif [[ $line =~ server\.token=[[:graph:]]+ ]]; then class=server_token_assign
    elif [[ $line =~ api[_-]?key=[[:graph:]]+ ]]; then class=api_key_assign
    elif [[ $line =~ password=[[:graph:]]+ ]]; then class=password_assign
    fi
    if [[ -n $class ]]; then
      emit_finding SECRET_SHAPED crit secrecy "path=$file:$lineno class=$class"
    fi
  done <"$file"
}

verify_record() {
  local record=$1
  # Honor the verification-time environment; otherwise retain the selected root.
  ROOT=${CHOUSA_ROOT:-$ROOT}
  [[ -n ${record:-} ]] || die_usage "record path required (--record, positional, or CHOUSA_RECORD)"
  [[ -e $record ]] || die_usage "record not found: $record"
  [[ -f $record ]] || die_usage "record is not a regular file: $record"
  [[ -r $record ]] || die_usage "record unreadable: $record"

  FINDING_LINES=(); N_FINDINGS=0; N_DRIFT=0; ROLL=CLEAN
  N_Q=0 N_SRC=0 N_CH=0 N_CL=0 N_NEG=0 N_REJ=0 N_APPR=0
  HAS_META=0 HAS_SOURCES_SEC=0 HAS_CHAIN_SEC=0 HAS_CLAIMS_SEC=0
  HAS_REJ_SEC=0 HAS_NEG_SEC=0 HAS_APPROVAL_SEC=0 HAS_SWEEP_SEC=0
  SCHEMA_HINT=0 WINDOW_EXTERNAL=0 APPROVAL_GRANTED=0 REJECT_MARKERS=0

  if head -n 5 -- "$record" | grep -qE 'research-record v1|chousa-record: v1'; then
    SCHEMA_HINT=1
  fi

  load_sections "$record"

  local s
  for s in "${SEC_ORDER[@]+"${SEC_ORDER[@]}"}"; do
    case "$s" in
      Meta) HAS_META=1 ;;
      Sources) HAS_SOURCES_SEC=1 ;;
      Chain) HAS_CHAIN_SEC=1 ;;
      Claims) HAS_CLAIMS_SEC=1 ;;
      Rejections) HAS_REJ_SEC=1 ;;
      Negatives) HAS_NEG_SEC=1 ;;
      Approval) HAS_APPROVAL_SEC=1 ;;
      Sweeps) HAS_SWEEP_SEC=1 ;;
    esac
  done

  if [[ $HAS_META -eq 0 && $HAS_SOURCES_SEC -eq 0 && $HAS_CLAIMS_SEC -eq 0 && $SCHEMA_HINT -eq 0 ]]; then
    emit_finding RECORD_SCHEMA_INVALID warn meta "no research-record sections/banner detected"
  fi

  if grep -qE '^(Skip to content|ChatGPT|You said:)' "$record"; then
    emit_finding EXPORT_CHROME_PRESENT info export "chat-export chrome lines present (data, not instruction)"
  fi

  if [[ $HAS_META -eq 1 ]]; then
    if grep -qiE 'window_mode:[[:space:]]*external|fetch:[[:space:]]*(external|live)|origin=external-live' <<<"${SEC_BODY[Meta]}"; then
      WINDOW_EXTERNAL=1
    fi
  fi
  if grep -qiE 'fetch=external|window=live-external|origin=external-live|window_mode[[:space:]]*[|][[:space:]]*external' "$record"; then
    WINDOW_EXTERNAL=1
  fi

  if [[ $HAS_APPROVAL_SEC -eq 1 ]]; then
    local arow st
    while IFS= read -r arow; do
      [[ -z $arow ]] && continue
      N_APPR=$((N_APPR + 1))
      st=$(cell "$arow" state)
      [[ -z $st ]] && st=$(cell "$arow" status)
      case "$(printf '%s' "$st" | tr 'A-Z' 'a-z')" in
        approved|granted) APPROVAL_GRANTED=1 ;;
      esac
    done < <(table_rows Approval)
  fi
  if [[ $WINDOW_EXTERNAL -eq 1 && $APPROVAL_GRANTED -eq 0 ]]; then
    emit_finding EXTERNAL_WITHOUT_APPROVAL crit approval "external/live window without approval state=approved|granted"
  fi

  scan_secrets "$record"

  if [[ -z ${SEC_BODY[Question]+x} ]]; then
    emit_finding NO_QUESTION crit question "missing ## Question section"
  else
    if section_nonempty_prose Question; then N_Q=1
    else emit_finding NO_QUESTION crit question "## Question present but empty"
    fi
  fi

  declare -g -A SRC_TIER=()
  if [[ $HAS_SOURCES_SEC -eq 0 ]]; then
    emit_finding SOURCE_TABLE_ABSENT warn sources "missing ## Sources / ## Source table"
  else
    local srow id tier ptr
    while IFS= read -r srow; do
      [[ -z $srow ]] && continue
      N_SRC=$((N_SRC + 1))
      id=$(cell "$srow" id); [[ -z $id ]] && id="row$N_SRC"
      tier=$(cell "$srow" tier | tr 'A-Z' 'a-z')
      ptr=$(cell "$srow" pointer)
      if [[ -z $tier ]]; then
        emit_finding UNRANKED_SOURCE warn sources "source=$id missing tier"
      else
        case "$tier" in
          primary|secondary|aggregator|unsourced|rejected|export|fleet-gate|proposal)
            SRC_TIER[$id]=$tier
            [[ $tier == rejected ]] && REJECT_MARKERS=$((REJECT_MARKERS + 1))
            ;;
          *) emit_finding UNRANKED_SOURCE warn sources "source=$id tier=$tier not in allowed set" ;;
        esac
      fi
      if [[ -z $ptr ]]; then
        emit_finding UNRANKED_SOURCE warn sources "source=$id missing pointer"
      else
        local fpart; fpart=$(ptr_file_part "$ptr")
        if [[ ${tier:-} == primary ]]; then
          if grep -qiE "$AGG_ERE" <<<"$fpart $srow"; then
            emit_finding HIERARCHY_PRIMARY_LIE warn sources "source=$id primary but aggregator-class path/class"
          fi
          local cls; cls=$(cell "$srow" class | tr 'A-Z' 'a-z')
          [[ $cls == aggregator ]] && emit_finding HIERARCHY_PRIMARY_LIE warn sources "source=$id primary with class=aggregator"
        fi
        check_pointer "$ptr" "$srow" sources "source:$id" || true
      fi
    done < <(table_rows Sources)
    if [[ $N_SRC -eq 0 ]]; then
      emit_finding SOURCE_TABLE_ABSENT warn sources "## Sources has no data rows"
    fi
  fi

  if [[ $HAS_CLAIMS_SEC -eq 0 ]]; then
    emit_finding CLAIM_TABLE_ABSENT warn claims "missing ## Claims"
  else
    local crow cid kind ptr st sweep
    while IFS= read -r crow; do
      [[ -z $crow ]] && continue
      N_CL=$((N_CL + 1))
      cid=$(cell "$crow" id); [[ -z $cid ]] && cid="C$N_CL"
      kind=$(cell "$crow" kind | tr 'A-Z' 'a-z')
      ptr=$(cell "$crow" pointer)
      st=$(cell "$crow" status | tr 'A-Z' 'a-z')
      sweep=$(cell "$crow" sweep)
      if [[ -z $kind ]]; then
        emit_finding OBS_INFERENCE_COLLAPSE warn claims "claim=$cid missing kind="
      else
        case "$kind" in
          observation|inference|negative|opinion|proposal|unknown) ;;
          *) emit_finding OBS_INFERENCE_COLLAPSE warn claims "claim=$cid kind=$kind invalid" ;;
        esac
      fi
      if [[ $kind == negative ]]; then
        N_NEG=$((N_NEG + 1))
        if [[ -z $sweep ]]; then
          local found=0 sw
          if [[ $HAS_SWEEP_SEC -eq 1 ]]; then
            while IFS= read -r sw; do
              [[ $(cell "$sw" claim_id) == "$cid" || $(cell "$sw" id) == "$cid" ]] && found=1
            done < <(table_rows Sweeps)
          fi
          if [[ $found -eq 0 ]]; then
            emit_finding NEGATIVE_WITHOUT_SWEEP warn negatives "claim=$cid negative without sweep"
          fi
        fi
      fi
      if [[ $kind != opinion && $kind != proposal ]]; then
        if [[ -z $ptr ]]; then
          emit_finding CLAIM_UNPOINTED warn claims "claim=$cid missing pointer"
        else
          check_pointer "$ptr" "$crow" claims "claim:$cid" || true
        fi
      fi
      if [[ $st == verified && -z $ptr ]]; then
        emit_finding CLAIM_UNPOINTED warn claims "claim=$cid status=verified without pointer"
      fi
    done < <(table_rows Claims)
    if [[ $N_CL -eq 0 ]]; then
      emit_finding CLAIM_TABLE_ABSENT warn claims "## Claims has no data rows"
    fi
  fi

  if [[ $HAS_NEG_SEC -eq 1 ]]; then
    local nrow
    while IFS= read -r nrow; do
      [[ -z $nrow ]] && continue
      N_NEG=$((N_NEG + 1))
      if [[ -z $(cell "$nrow" sweep) ]]; then
        emit_finding NEGATIVE_WITHOUT_SWEEP warn negatives "negative id=$(cell "$nrow" id) missing sweep"
      fi
    done < <(table_rows Negatives)
  fi

  if [[ $HAS_CHAIN_SEC -eq 0 ]]; then
    if [[ $N_CL -gt 0 ]]; then
      emit_finding CHAIN_ABSENT warn chain "claims present but ## Chain missing"
    fi
  else
    local hrow hop st to notes
    while IFS= read -r hrow; do
      [[ -z $hrow ]] && continue
      N_CH=$((N_CH + 1))
      hop=$(cell "$hrow" hop); [[ -z $hop ]] && hop="H$N_CH"
      st=$(cell "$hrow" status | tr 'A-Z' 'a-z')
      to=$(cell "$hrow" to)
      notes=$(cell "$hrow" notes)
      [[ -z $notes ]] && notes=$(cell "$hrow" note)
      [[ -z $notes ]] && notes=$(cell "$hrow" reason)
      case "$st" in
        resolved)
          if [[ -n $to && -n ${SRC_TIER[$to]+x} ]]; then
            :
          elif [[ -z $to ]] || ! ptr_resolves_meta "$to"; then
            emit_finding CHAIN_HOP_UNRESOLVED warn chain "hop=$hop status=resolved but to= does not resolve"
          fi
          ;;
        unresolved|blocked-no-fetch)
          if [[ -z $notes ]]; then
            emit_finding CHAIN_HOP_UNRESOLVED warn chain "hop=$hop status=$st missing reason/notes"
          fi
          ;;
        rejected|labelled-dead|not-applicable) ;;
        "")
          emit_finding CHAIN_HOP_UNRESOLVED warn chain "hop=$hop missing status"
          ;;
        *)
          emit_finding CHAIN_HOP_UNRESOLVED warn chain "hop=$hop status=$st not in allowed set"
          ;;
      esac
    done < <(table_rows Chain)
  fi

  if [[ $HAS_REJ_SEC -eq 0 ]]; then
    emit_finding REJECTION_DROPPED warn rejections "missing ## Rejections section"
  else
    local rrow reason rc=0
    while IFS= read -r rrow; do
      [[ -z $rrow ]] && continue
      rc=$((rc + 1)); N_REJ=$((N_REJ + 1))
      reason=$(cell "$rrow" reason)
      if [[ -z $reason ]]; then
        emit_finding REJECTION_REASON_ABSENT warn rejections "rejection id=$(cell "$rrow" id) empty reason"
      fi
    done < <(table_rows Rejections)
    if [[ $REJECT_MARKERS -gt 0 && $rc -eq 0 ]]; then
      emit_finding REJECTION_DROPPED warn rejections "rejected markers exist but rejections table empty"
    fi
  fi

  printf 'research-gate %s — ts=%s — mode=verify — record=%s\n' "$VERSION" "$TS_UTC" "$record"
  local f
  for f in "${FINDING_LINES[@]+"${FINDING_LINES[@]}"}"; do
    printf '%s\n' "$f"
  done
  printf 'RESEARCH_GATE: %s (findings=%d drift=%d questions=%d sources=%d chains=%d claims=%d negatives=%d rejections=%d approvals=%d)\n' \
    "$ROLL" "$N_FINDINGS" "$N_DRIFT" "$N_Q" "$N_SRC" "$N_CH" "$N_CL" "$N_NEG" "$N_REJ" "$N_APPR"

  [[ $ROLL == CLEAN ]] && return 0
  return 1
}

run_selftest() {
  local WORK cases=0 failures=0
  WORK=$(mktemp -d /tmp/chousa-research-gate-selftest.XXXXXX) \
    || die_usage "mktemp failed"
  trap 'rm -rf -- "$WORK"' EXIT
  mkdir -p "$WORK/lib" "$WORK/noise"
  printf 'line1 primary material\nline2\n' >"$WORK/lib/primary.md"
  printf 'aggregator chrome sources sidebar\n' >"$WORK/noise/chat-export-sources.md"

  export CHOUSA_ROOT="$WORK"
  export CHOUSA_NOW_EPOCH="$NOW_EPOCH"

  write_rec() { cat >"$WORK/$1.md"; }

  # name want_rc [required output substring ... | NAME=VAL env override ...]
  # Exercise the public CLI with errexit active, not a function under set +e.
  # Isolate inherited record/strict/aggregator settings and pass the fixture root.
  tcase() {
    local name=$1 want_rc=$2
    shift 2
    local -a want=() over=()
    local a rc=0 out nverdict tok ok=1 leak=''
    for a in "$@"; do
      if [[ $a =~ ^[A-Z_]+= ]]; then over+=("$a"); else want+=("$a"); fi
    done
    cases=$((cases + 1))
    out=$(env -u CHOUSA_RECORD -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 \
      "${over[@]+"${over[@]}"}" CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
      bash "$SELF" verify "$WORK/$name.md" 2>&1) || rc=$?
    nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true)
    for tok in "${want[@]+"${want[@]}"}"; do
      [[ $out == *"$tok"* ]] || ok=0
    done
    # Secrecy is asserted before the pass/fail split, so a case that fails for an
    # unrelated reason still cannot echo the planted span through the dump below.
    if [[ $out == *'sk-fxdemo_not_real_0000'* ]]; then
      leak=' secret-span-echoed'
      out=${out//sk-fxdemo_not_real_0000/[span-redacted]}
    fi
    if [[ $rc -eq $want_rc && $nverdict -eq 1 && $ok -eq 1 && -z $leak ]]; then
      printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" "$name" "$rc"
    else
      printf 'FAIL-case %-28s exit=%d want=%d verdicts=%d%s token=%s\n' \
        "$name" "$rc" "$want_rc" "$nverdict" "$leak" "${want[*]-}"
      printf '%s\n' "$out" | sed 's/^/    | /'
      failures=$((failures + 1))
    fi
  }

  write_rec pass-control <<'EOF'
# research-record v1
<!-- chousa-record: v1 -->
## Meta
| key | value |
|---|---|
| window | loopback |
| fetch | none |
## Question
When does apprenticeship completion appear in local survey material?
## Sources
| id | tier | pointer | notes |
|---|---|---|---|
| S1 | primary | lib/primary.md:1 | local fixture |
| S2 | secondary | lib/primary.md:2 | local fixture |
## Chain
| hop | from | to | status | notes |
|---|---|---|---|---|
| 1 | C1 | S1 | resolved | direct |
## Claims
| id | kind | text | pointer | status | sweep |
|---|---|---|---|---|---|
| C1 | observation | primary file has line1 | lib/primary.md:1 | verified | |
## Negatives
| id | text | sweep | status |
|---|---|---|---|
| N1 | no fx-only ghost source | `test ! -f lib/ghost.md` | swept |
## Rejections
| id | ref | reason |
|---|---|---|
| R1 | noise/chat-export-sources.md | UI chrome is not a primary source |
## Unknowns
| id | text |
|---|---|
| U1 | outbound host cites in live exports unverified-locally |
## Approval
| target | why | scope | state |
|---|---|---|---|
| (none) | loopback-only | local | not-required |
EOF
  tcase pass-control 0 'RESEARCH_GATE: CLEAN'

  write_rec pass-hop-marked-unresolved <<'EOF'
# research-record v1
## Meta
| key | value |
|---|---|
| window | loopback |
## Question
What happens when a hop cannot be opened locally?
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | secondary | lib/primary.md:1 |
## Chain
| hop | from | to | status | notes |
|---|---|---|---|---|
| 1 | C1 | https://example.invalid/x | unresolved | blocked-no-fetch loopback |
## Claims
| id | kind | text | pointer | status |
|---|---|---|---|---|
| C1 | inference | remote primary not recovered | S1 | unresolved |
## Rejections
| id | ref | reason |
|---|---|---|
| R1 | example.invalid | no external window |
## Approval
| target | state |
|---|---|
| none | not-required |
EOF
  tcase pass-hop-marked-unresolved 0 'RESEARCH_GATE: CLEAN'

  # The same informational finding stays CLEAN normally and drifts in strict
  # mode. Both paths must reach the deferred summary under CLI errexit.
  sed '1a Skip to content' "$WORK/pass-control.md" >"$WORK/pass-export-chrome.md"
  cp -- "$WORK/pass-export-chrome.md" "$WORK/fail-export-chrome-strict.md"
  tcase pass-export-chrome 0 \
    'RESEARCH_GATE: CLEAN' 'FINDING EXPORT_CHROME_PRESENT severity=info'
  tcase fail-export-chrome-strict 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING EXPORT_CHROME_PRESENT severity=info' \
    CHOUSA_STRICT=1

  # A malformed export must not truncate the pass: the info emitter sits ahead of
  # every structural check, so the later findings still have to be recorded and
  # exactly one summary has to close the run (tcase counts the verdict lines).
  write_rec fail-chrome-malformed-export <<'EOF'
Skip to content
ChatGPT
You said:
random prose without sections
EOF
  tcase fail-chrome-malformed-export 1 \
    'RESEARCH_GATE: DRIFT' \
    'FINDING EXPORT_CHROME_PRESENT severity=info' \
    'FINDING RECORD_SCHEMA_INVALID' \
    'FINDING NO_QUESTION' \
    'FINDING SOURCE_TABLE_ABSENT' \
    'FINDING CLAIM_TABLE_ABSENT' \
    'FINDING REJECTION_DROPPED'

  write_rec fail-no-question <<'EOF'
# research-record v1
## Meta
| key | value |
|---|---|
| window | loopback |
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Chain
| hop | from | to | status | notes |
|---|---|---|---|---|
| 1 | C1 | S1 | resolved | x |
## Claims
| id | kind | text | pointer | status |
|---|---|---|---|---|
| C1 | observation | x | lib/primary.md:1 | verified |
## Rejections
| id | ref | reason |
|---|---|---|
| R1 | n/a | none-recorded |
EOF
  tcase fail-no-question 1 'FINDING NO_QUESTION'

  write_rec fail-unranked-source <<'EOF'
# research-record v1
## Question
Q?
## Sources
| id | tier | pointer |
|---|---|---|
| S1 |  | lib/primary.md:1 |
## Chain
| hop | from | to | status | notes |
|---|---|---|---|---|
| 1 | C1 | S1 | resolved | x |
## Claims
| id | kind | text | pointer | status |
|---|---|---|---|---|
| C1 | observation | x | S1 | verified |
## Rejections
| id | ref | reason |
|---|---|---|
| R1 | n/a | none-recorded |
EOF
  tcase fail-unranked-source 1 'FINDING UNRANKED_SOURCE'

  write_rec fail-chain-hop-unresolved <<'EOF'
# research-record v1
## Question
Q?
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Chain
| hop | from | to | status | notes |
|---|---|---|---|---|
| 1 | C1 | S1 | pending | |
## Claims
| id | kind | text | pointer | status |
|---|---|---|---|---|
| C1 | observation | x | S1 | verified |
## Rejections
| id | ref | reason |
|---|---|---|
| R1 | n/a | none-recorded |
EOF
  tcase fail-chain-hop-unresolved 1 'FINDING CHAIN_HOP_UNRESOLVED'

  write_rec fail-claim-unpointed <<'EOF'
# research-record v1
## Question
Q?
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Chain
| hop | from | to | status | notes |
|---|---|---|---|---|
| 1 | C1 | S1 | resolved | x |
## Claims
| id | kind | text | pointer | status |
|---|---|---|---|---|
| C1 | observation | x |  | verified |
## Rejections
| id | ref | reason |
|---|---|---|
| R1 | n/a | none-recorded |
EOF
  tcase fail-claim-unpointed 1 'FINDING CLAIM_UNPOINTED'

  write_rec fail-rejection-dropped <<'EOF'
# research-record v1
## Question
Q?
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
| S9 | rejected | noise/chat-export-sources.md |
## Chain
| hop | from | to | status | notes |
|---|---|---|---|---|
| 1 | C1 | S1 | resolved | x |
## Claims
| id | kind | text | pointer | status |
|---|---|---|---|---|
| C1 | observation | x | S1 | verified |
EOF
  tcase fail-rejection-dropped 1 'FINDING REJECTION_DROPPED'

  write_rec fail-negative-without-sweep <<'EOF'
# research-record v1
## Question
Q?
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Chain
| hop | from | to | status | notes |
|---|---|---|---|---|
| 1 | C1 | S1 | resolved | x |
## Claims
| id | kind | text | pointer | status | sweep |
|---|---|---|---|---|---|
| C1 | observation | x | S1 | verified | |
| N1 | negative | absent thing | S1 | unresolved | |
## Rejections
| id | ref | reason |
|---|---|---|
| R1 | n/a | none-recorded |
EOF
  tcase fail-negative-without-sweep 1 'FINDING NEGATIVE_WITHOUT_SWEEP'

  write_rec fail-obs-inference-collapse <<'EOF'
# research-record v1
## Question
Q?
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Chain
| hop | from | to | status | notes |
|---|---|---|---|---|
| 1 | C1 | S1 | resolved | x |
## Claims
| id | kind | text | pointer | status |
|---|---|---|---|---|
| C1 |  | mixes obs and guess | S1 | verified |
## Rejections
| id | ref | reason |
|---|---|---|
| R1 | n/a | none-recorded |
EOF
  tcase fail-obs-inference-collapse 1 'FINDING OBS_INFERENCE_COLLAPSE'

  write_rec fail-hierarchy-primary-lie <<'EOF'
# research-record v1
## Question
Q?
## Sources
| id | tier | pointer | class |
|---|---|---|---|
| S1 | primary | noise/chat-export-sources.md | aggregator |
## Chain
| hop | from | to | status | notes |
|---|---|---|---|---|
| 1 | C1 | S1 | resolved | x |
## Claims
| id | kind | text | pointer | status |
|---|---|---|---|---|
| C1 | observation | x | S1 | verified |
## Rejections
| id | ref | reason |
|---|---|---|
| R1 | n/a | none-recorded |
EOF
  tcase fail-hierarchy-primary-lie 1 'FINDING HIERARCHY_PRIMARY_LIE'

  write_rec fail-pointer-ephemeral <<'EOF'
# research-record v1
## Question
Q?
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Chain
| hop | from | to | status | notes |
|---|---|---|---|---|
| 1 | C1 | S1 | resolved | x |
## Claims
| id | kind | text | pointer | status |
|---|---|---|---|---|
| C1 | observation | x | local://round-1/x.md | verified |
## Rejections
| id | ref | reason |
|---|---|---|
| R1 | n/a | none-recorded |
EOF
  tcase fail-pointer-ephemeral 1 'FINDING POINTER_EPHEMERAL'

  write_rec fail-external-without-approval <<'EOF'
# research-record v1
## Meta
| key | value |
|---|---|
| window_mode | external-approved |
| fetch | external |
## Question
Q?
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Chain
| hop | from | to | status | notes |
|---|---|---|---|---|
| 1 | C1 | S1 | resolved | x |
## Claims
| id | kind | text | pointer | status |
|---|---|---|---|---|
| C1 | observation | x | S1 | verified |
## Rejections
| id | ref | reason |
|---|---|---|
| R1 | n/a | none-recorded |
## Approval
| target | state |
|---|---|
| web | pending |
EOF
  tcase fail-external-without-approval 1 'FINDING EXTERNAL_WITHOUT_APPROVAL'

  write_rec fail-secret-shaped <<'EOF'
# research-record v1
## Question
Q?
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Chain
| hop | from | to | status | notes |
|---|---|---|---|---|
| 1 | C1 | S1 | resolved | x |
## Claims
| id | kind | text | pointer | status |
|---|---|---|---|---|
| C1 | observation | x | S1 | verified |
## Rejections
| id | ref | reason |
|---|---|---|
| R1 | n/a | none-recorded |
## Notes
planted: sk-fxdemo_not_real_0000
EOF
  tcase fail-secret-shaped 1 'FINDING SECRET_SHAPED'

  write_rec fail-session-read <<'EOF'
# research-record v1
## Question
Q?
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Chain
| hop | from | to | status | notes |
|---|---|---|---|---|
| 1 | C1 | S1 | resolved | x |
## Claims
| id | kind | text | pointer | status |
|---|---|---|---|---|
| C1 | observation | bad hop | /home/vgpnk/.omp/agent/config.yml:1 | verified |
## Rejections
| id | ref | reason |
|---|---|---|
| R1 | n/a | none-recorded |
EOF
  tcase fail-session-read 1 'FINDING SESSION_READ'

  # Schema drift without export chrome, so this case stays on the schema path and
  # the chrome-plus-malformed continuation above is not a second test of it.
  write_rec fail-schema <<'EOF'
# untitled capture
random prose without sections
EOF
  tcase fail-schema 1 'FINDING RECORD_SCHEMA_INVALID'

  # Setup/usage is asserted the way a consumer sees it: a fresh process, its real
  # exit code, and an empty stdout — usage text goes to stderr — so exit 2 can
  # never be mistaken for a verdict-bearing run.
  tsetup() {
    local name=$1 want_rc=$2
    shift 2
    local rc=0 out err
    cases=$((cases + 1))
    # stdout and stderr are captured apart: the counting command the scorecard
    # uses reads stdout only, so a verdict line could hide inside a merged pipe.
    out=$(env -u CHOUSA_RECORD -u CHOUSA_STRICT -u CHOUSA_AGGREGATOR_ERE \
      CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
      bash "$SELF" "$@" 2>"$WORK/setup-$name.err") || rc=$?
    err=$(cat "$WORK/setup-$name.err")
    if [[ $rc -eq $want_rc && ${#out} -eq 0 && -n $err ]]; then
      printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" "setup-$name" "$rc"
    else
      printf 'FAIL-case setup-%s exit=%d want=%d stdout_bytes=%d stderr_bytes=%d\n' \
        "$name" "$rc" "$want_rc" "${#out}" "${#err}"
      printf '%s\n' "$err" | sed 's/^/    | /'
      failures=$((failures + 1))
    fi
  }
  tsetup no-record 2 verify
  tsetup missing-file 2 verify "$WORK/no-such-record.md"

  if [[ $failures -eq 0 ]]; then
    printf 'RESEARCH_GATE_SELFTEST: PASS (%d cases)\n' "$cases"
    exit 0
  fi
  printf 'RESEARCH_GATE_SELFTEST: FAIL (%d/%d cases)\n' "$failures" "$cases"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    --selftest) MODE=selftest; shift ;;
    verify) MODE=verify; shift ;;
    --record)
      [[ $# -ge 2 ]] || die_usage "--record needs PATH"
      RECORD_ARG=$2; shift 2 ;;
    --root)
      [[ $# -ge 2 ]] || die_usage "--root needs PATH"
      ROOT=$2; shift 2 ;;
    --) shift; break ;;
    -*) die_usage "unknown flag: $1" ;;
    *)
      [[ -z $RECORD_ARG ]] || die_usage "multiple record paths"
      RECORD_ARG=$1; shift ;;
  esac
done

case "$MODE" in
  selftest) run_selftest ;;
  verify)
    RECORD_PATH=${RECORD_ARG:-${CHOUSA_RECORD:-}}
    verify_record "$RECORD_PATH"
    ;;
  *) die_usage "unknown mode: $MODE" ;;
esac
