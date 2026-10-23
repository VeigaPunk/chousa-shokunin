#!/usr/bin/env bash
# Minimal standalone C1-style character-walk benchmark (not the gate).
# usage: LC_ALL=<locale> bench.sh <mode> <file> <reps>
#   modes: slice | walk | growappend | grow | check
#   slice      : per-char ${line:i:1} + one test (isolates slicing cost)
#   walk       : string-state + depth machine, records depth-1 member raw values,
#                duplicate detection for the seven read keys
#   growappend : walk, plus s+=$c (append to a growing string) per char
#   grow       : walk, plus s+=$c then c=${s:i:1} (slicing a growing string)
#   check      : print members/dup/read values once (no timing)
# Emits one TSV line: mode<TAB>locale<TAB>size<TAB>reps<TAB>total_us<TAB>per_call_us<TAB>per_byte_ns<TAB>members<TAB>dup
set -u

mode=${1:?mode}
file=${2:?file}
reps=${3:-1}

W_MEMBERS=0; W_DUP=0
W_ID=''; W_SRC=''; W_SPAN=''; W_EXP=''; W_MARK=''; W_LINE=''; W_SHA=''

parse_walk() { # $1 = line; fixed-string per-char walk
  local line=$1 n=${#line} i=0 c
  local st=0 depth=0 wantkey=0 iskey=0 tok=-1 key='' lastkey='' val='' dupc=0
  local members=0 dup=0 expect_val=0
  local cnt_id=0 cnt_src=0 cnt_span=0 cnt_exp=0 cnt_mark=0 cnt_line=0 cnt_sha=0
  local rid='' rsrc='' rspan='' rexp='' rmark='' rline='' rsha=''
  while (( i < n )); do
    c=${line:i:1}
    if (( st == 1 )); then
      if [[ $c == '\' ]]; then
        st=2
      elif [[ $c == '"' ]]; then
        if (( iskey )); then
          if (( depth == 1 )); then
            key=${line:tok:i-tok}
            lastkey=$key
            dupc=0
            case $key in
              id) cnt_id=$((cnt_id+1)); dupc=$cnt_id;;
              source) cnt_src=$((cnt_src+1)); dupc=$cnt_src;;
              span) cnt_span=$((cnt_span+1)); dupc=$cnt_span;;
              expect) cnt_exp=$((cnt_exp+1)); dupc=$cnt_exp;;
              marker) cnt_mark=$((cnt_mark+1)); dupc=$cnt_mark;;
              line) cnt_line=$((cnt_line+1)); dupc=$cnt_line;;
              sha256) cnt_sha=$((cnt_sha+1)); dupc=$cnt_sha;;
            esac
            (( dupc > 1 )) && dup=1
          fi
          wantkey=0
        elif (( expect_val == 1 && depth == 1 )); then
          val=${line:tok:i-tok}
          members=$((members+1))
          expect_val=0
          case $lastkey in
            id) rid=$val;; source) rsrc=$val;; span) rspan=$val;;
            expect) rexp=$val;; marker) rmark=$val;; line) rline=$val;;
            sha256) rsha=$val;;
          esac
        fi
        iskey=0; tok=-1; st=0
      fi
    elif (( st == 2 )); then
      st=1
    elif [[ $c == '"' ]]; then
      tok=$((i+1)); iskey=$wantkey; st=1
    elif [[ $c == '{' || $c == '[' ]]; then
      if (( depth == 0 )); then
        depth=1; wantkey=1
      else
        if (( depth == 1 )); then
          (( expect_val == 1 )) && { members=$((members+1)); expect_val=0; }
        fi
        depth=$((depth+1))
      fi
    elif [[ $c == '}' || $c == ']' ]]; then
      (( depth > 0 )) && depth=$((depth-1))
      (( depth == 1 )) && expect_val=0
    elif [[ $c == ':' ]]; then
      (( depth == 1 )) && expect_val=1
    elif [[ $c == ',' ]]; then
      (( depth == 1 )) && { expect_val=0; wantkey=1; }
    elif (( depth == 1 && expect_val == 1 )); then
      members=$((members+1)); expect_val=0
    fi
    (( i++ ))
  done
  W_MEMBERS=$members; W_DUP=$dup
  W_ID=$rid; W_SRC=$rsrc; W_SPAN=$rspan; W_EXP=$rexp
  W_MARK=$rmark; W_LINE=$rline; W_SHA=$rsha
}

parse_grow() { # $1 = line; append each char to s, slice the growing s
  local line=$1 n=${#line} i=0 c s=''
  local st=0 depth=0 wantkey=0 iskey=0 tok=-1 key='' lastkey='' val='' dupc=0
  local members=0 dup=0 expect_val=0
  local cnt_id=0 cnt_src=0 cnt_span=0 cnt_exp=0 cnt_mark=0 cnt_line=0 cnt_sha=0
  local rid='' rsrc='' rspan='' rexp='' rmark='' rline='' rsha=''
  while (( i < n )); do
    c=${line:i:1}
    s+=$c
    c=${s:i:1}
    if (( st == 1 )); then
      if [[ $c == '\' ]]; then
        st=2
      elif [[ $c == '"' ]]; then
        if (( iskey )); then
          if (( depth == 1 )); then
            key=${s:tok:i-tok}
            lastkey=$key
            dupc=0
            case $key in
              id) cnt_id=$((cnt_id+1)); dupc=$cnt_id;;
              source) cnt_src=$((cnt_src+1)); dupc=$cnt_src;;
              span) cnt_span=$((cnt_span+1)); dupc=$cnt_span;;
              expect) cnt_exp=$((cnt_exp+1)); dupc=$cnt_exp;;
              marker) cnt_mark=$((cnt_mark+1)); dupc=$cnt_mark;;
              line) cnt_line=$((cnt_line+1)); dupc=$cnt_line;;
              sha256) cnt_sha=$((cnt_sha+1)); dupc=$cnt_sha;;
            esac
            (( dupc > 1 )) && dup=1
          fi
          wantkey=0
        elif (( expect_val == 1 && depth == 1 )); then
          val=${s:tok:i-tok}
          members=$((members+1))
          expect_val=0
          case $lastkey in
            id) rid=$val;; source) rsrc=$val;; span) rspan=$val;;
            expect) rexp=$val;; marker) rmark=$val;; line) rline=$val;;
            sha256) rsha=$val;;
          esac
        fi
        iskey=0; tok=-1; st=0
      fi
    elif (( st == 2 )); then
      st=1
    elif [[ $c == '"' ]]; then
      tok=$((i+1)); iskey=$wantkey; st=1
    elif [[ $c == '{' || $c == '[' ]]; then
      if (( depth == 0 )); then
        depth=1; wantkey=1
      else
        if (( depth == 1 )); then
          (( expect_val == 1 )) && { members=$((members+1)); expect_val=0; }
        fi
        depth=$((depth+1))
      fi
    elif [[ $c == '}' || $c == ']' ]]; then
      (( depth > 0 )) && depth=$((depth-1))
      (( depth == 1 )) && expect_val=0
    elif [[ $c == ':' ]]; then
      (( depth == 1 )) && expect_val=1
    elif [[ $c == ',' ]]; then
      (( depth == 1 )) && { expect_val=0; wantkey=1; }
    elif (( depth == 1 && expect_val == 1 )); then
      members=$((members+1)); expect_val=0
    fi
    (( i++ ))
  done
  W_MEMBERS=$members; W_DUP=$dup
  W_ID=$rid; W_SRC=$rsrc; W_SPAN=$rspan; W_EXP=$rexp
  W_MARK=$rmark; W_LINE=$rline; W_SHA=$rsha
}

parse_growappend() { # $1 = line; walk, plus s+=$c per char (append cost only)
  local line=$1 n=${#line} i=0 c s=''
  local st=0 depth=0 wantkey=0 iskey=0 tok=-1 key='' lastkey='' val='' dupc=0
  local members=0 dup=0 expect_val=0
  local cnt_id=0 cnt_src=0 cnt_span=0 cnt_exp=0 cnt_mark=0 cnt_line=0 cnt_sha=0
  local rid='' rsrc='' rspan='' rexp='' rmark='' rline='' rsha=''
  while (( i < n )); do
    c=${line:i:1}
    s+=$c
    if (( st == 1 )); then
      if [[ $c == '\' ]]; then
        st=2
      elif [[ $c == '"' ]]; then
        if (( iskey )); then
          if (( depth == 1 )); then
            key=${line:tok:i-tok}
            lastkey=$key
            dupc=0
            case $key in
              id) cnt_id=$((cnt_id+1)); dupc=$cnt_id;;
              source) cnt_src=$((cnt_src+1)); dupc=$cnt_src;;
              span) cnt_span=$((cnt_span+1)); dupc=$cnt_span;;
              expect) cnt_exp=$((cnt_exp+1)); dupc=$cnt_exp;;
              marker) cnt_mark=$((cnt_mark+1)); dupc=$cnt_mark;;
              line) cnt_line=$((cnt_line+1)); dupc=$cnt_line;;
              sha256) cnt_sha=$((cnt_sha+1)); dupc=$cnt_sha;;
            esac
            (( dupc > 1 )) && dup=1
          fi
          wantkey=0
        elif (( expect_val == 1 && depth == 1 )); then
          val=${line:tok:i-tok}
          members=$((members+1))
          expect_val=0
          case $lastkey in
            id) rid=$val;; source) rsrc=$val;; span) rspan=$val;;
            expect) rexp=$val;; marker) rmark=$val;; line) rline=$val;;
            sha256) rsha=$val;;
          esac
        fi
        iskey=0; tok=-1; st=0
      fi
    elif (( st == 2 )); then
      st=1
    elif [[ $c == '"' ]]; then
      tok=$((i+1)); iskey=$wantkey; st=1
    elif [[ $c == '{' || $c == '[' ]]; then
      if (( depth == 0 )); then
        depth=1; wantkey=1
      else
        if (( depth == 1 )); then
          (( expect_val == 1 )) && { members=$((members+1)); expect_val=0; }
        fi
        depth=$((depth+1))
      fi
    elif [[ $c == '}' || $c == ']' ]]; then
      (( depth > 0 )) && depth=$((depth-1))
      (( depth == 1 )) && expect_val=0
    elif [[ $c == ':' ]]; then
      (( depth == 1 )) && expect_val=1
    elif [[ $c == ',' ]]; then
      (( depth == 1 )) && { expect_val=0; wantkey=1; }
    elif (( depth == 1 && expect_val == 1 )); then
      members=$((members+1)); expect_val=0
    fi
    (( i++ ))
  done
  W_MEMBERS=$members; W_DUP=$dup
  W_ID=$rid; W_SRC=$rsrc; W_SPAN=$rspan; W_EXP=$rexp
  W_MARK=$rmark; W_LINE=$rline; W_SHA=$rsha
}

IFS= read -r line < "$file" || true
size=${#line}
rounds=${4:-3}
target_ns=${TARGET_NS:-1200000000}

# locale probe: a two-byte UTF-8 character counts 1 char in UTF-8, 2 in C
mb='é'
read -r la _ < /proc/loadavg
printf 'probe\tlocale=%s\tcharmap=%s\tlen(é)=%s\tloadavg1=%s\n' "${LC_ALL:-unset}" \
  "$(locale charmap 2>/dev/null)" "${#mb}" "$la"

if [[ $mode == check ]]; then
  parse_walk "$line"
  printf 'check\tsize=%s\tmembers=%s\tdup=%s\tid=%s\tsource=%s\tspan=%s\texpect=%s\tmarker=%s\tline=%s\tsha256=%s\n' \
    "$size" "$W_MEMBERS" "$W_DUP" "$W_ID" "$W_SRC" "$W_SPAN" "$W_EXP" "$W_MARK" "$W_LINE" "$W_SHA"
  exit 0
fi

case $mode in
  slice | walk | growappend | grow | fixed0 | fixedend | smallloop) ;;
  *)
    echo "unknown mode: $mode" >&2
    exit 2
    ;;
esac

# CPU time of this shell, ns resolution (kernel scheduler accounting)
cpu_ns() { local a b c; read -r a b c < /proc/self/schedstat; CN=$a; }
wall_us() { WU=${EPOCHREALTIME//[!0-9]/}; }

block() { # $1 = reps; sets BLK_CPU_NS, BLK_WALL_US
  local reps=$1 r
  cpu_ns; local c0=$CN
  wall_us; local w0=$WU
  case $mode in
    slice)
      for ((r = 0; r < reps; r++)); do
        q=0
        for ((i = 0; i < size; i++)); do
          c=${line:i:1}
          [[ $c == '"' ]] && q=$((q + 1))
        done
      done
      W_MEMBERS=$q
      ;;
    walk) for ((r = 0; r < reps; r++)); do parse_walk "$line"; done;;
    growappend) for ((r = 0; r < reps; r++)); do parse_growappend "$line"; done;;
    grow) for ((r = 0; r < reps; r++)); do parse_grow "$line"; done;;
    fixed0) for ((r = 0; r < reps; r++)); do c=${line:0:1}; done;;
    fixedend)
      last=$((size - 1))
      for ((r = 0; r < reps; r++)); do c=${line:last:1}; done
      ;;
    smallloop) for ((r = 0; r < reps; r++)); do j=$((r % 500)); c=${line:j:1}; done;;
  esac
  wall_us; local w1=$WU
  cpu_ns; local c1=$CN
  BLK_CPU_NS=$((c1 - c0))
  BLK_WALL_US=$((w1 - w0))
}

# warm-up, then two calibration calls; reps sized to target CPU time
block 1
block 1
per=$BLK_CPU_NS
(( per < 1 )) && per=1
reps=$((target_ns / per))
(( reps < 1 )) && reps=1
cap=20000
case $mode in fixed0 | fixedend | smallloop) cap=400000;; esac
(( reps > cap )) && reps=$cap
(( per > 2000000000 )) && rounds=1

for ((rr = 1; rr <= rounds; rr++)); do
  block "$reps"
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$mode" "${LC_ALL:-unset}" "$size" "$reps" "$rr" "$BLK_CPU_NS" "$BLK_WALL_US" \
    "$((BLK_CPU_NS / reps))" "$((BLK_CPU_NS / (reps * size)))" "$W_MEMBERS" "$W_DUP"
done
