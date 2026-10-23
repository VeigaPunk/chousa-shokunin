#!/usr/bin/env bash
# no-name-signals.sh — round-33 D5 hygiene check (chousa lane).
#
# Flags seat artifacts that signal processes by name or pattern instead of by a
# recorded PID / process group. Scanned extensions: *.md *.sh *.py *.txt *.json.
#
# Detected signalling forms (one line, same line):
#   pkill ...                         any form (-x, -f, -u, ...)
#   killall ... / killall5 ...
#   kill [opts] $(pgrep ...)          command substitution
#   kill [opts] `pgrep ...`           backticks
#   kill [opts] $(pidof ...)          pidof variant
#   kill [opts] $(ps -C name ...)     ps-by-command-name variant
#   ps|pgrep|pidof ... | xargs ... kill ...
#
# NOT flagged: bare inspection (pgrep -af ..., ps -ef | grep ...), and scoped
# kills of an already-recorded PID or own process group (kill "$pid",
# kill -- -$$, kill %1, kill -TERM 4321, kill -TERM $(cat pidfile)).
#
# Exit: 0 clean, 1 hits listed on stdout, 2 usage or I/O error.
#
# Fail-closed on prose: a report that *quotes* a banned command (e.g. the D5
# disclosure itself) is listed as a hit, because a citation and an executed
# command are indistinguishable at text level. Each hit carries its kind:
#   code = *.sh/*.py, doc = *.md/*.txt/*.json.
# Once a human has adjudicated a reporting file, pass --exclude PATH for it.
#
# Limits (documented, not detected): aliasing (alias pk=pkill), command
# concatenation (p''kill), `command pkill`, busybox applets, SSH-wrapped
# commands, and pipelines split across lines.
#
# GNU coreutils/findutils/grep assumed (uses find -printf, grep -Z/-E).

set -u
export LC_ALL=C

PROG=${0##*/}
SELF=$(readlink -f -- "$0" 2>/dev/null || printf '%s' "$0")
MAX_BYTES=${NO_NAME_SIGNALS_MAX_BYTES:-16777216}
CODE_ONLY=0
declare -a DIRS=()
declare -a EXCLUDES=()

usage() {
  cat <<EOF
usage: $PROG [options] DIR...

Scan DIR... recursively for *.md *.sh *.py *.txt *.json that signal processes
by name or pattern (pkill / killall / kill \$(pgrep ...) / pgrep ... | xargs kill).

options:
  --code-only        scan only *.sh and *.py (skips prose and receipts)
  --exclude PATH     skip PATH (file or directory subtree); repeatable
  --max-bytes N      skip files larger than N bytes (default 16777216)
  -h, --help         this help

exit: 0 clean, 1 hits listed, 2 usage or I/O error
EOF
}

# Regexes are bash [[ =~ ]] EREs.
RE_PKILL='(^|[^[:alnum:]_])pkill([^[:alnum:]_]|$)'
RE_KILLALL='(^|[^[:alnum:]_])killall5?([^[:alnum:]_]|$)'
RE_CMDSUB="(^|[^[:alnum:]_])kill([[:space:]]+-[^[:space:];|&]+|[[:space:]]+[A-Za-z][A-Za-z0-9_-]*)*[[:space:]]+[\"'\`]?(\\\$\(|\`)[[:space:]]*(pgrep|pidof)([^[:alnum:]_]|\$)"
RE_XARGS="(^|[^[:alnum:]_])(ps|pgrep|pidof)([^[:alnum:]_]|\$).*[|].*xargs([^[:alnum:]_]|\$).*kill([^[:alnum:]_]|\$)"
RE_PSNAME="(^|[^[:alnum:]_])kill([[:space:]]+-[^[:space:];|&]+|[[:space:]]+[A-Za-z][A-Za-z0-9_-]*)*[[:space:]]+[\"'\`]?(\\\$\(|\`)[[:space:]]*ps[^)]*-C([[:space:]]|\$)"
UNION='pkill|killall|pidof|pgrep|kill'

while (($#)); do
  case $1 in
    --code-only) CODE_ONLY=1 ;;
    --exclude)
      shift
      (($#)) || { printf '%s: --exclude needs PATH\n' "$PROG" >&2; exit 2; }
      EXCLUDES+=("$1")
      ;;
    --max-bytes)
      shift
      (($#)) || { printf '%s: --max-bytes needs N\n' "$PROG" >&2; exit 2; }
      [[ $1 =~ ^[0-9]+$ ]] || { printf '%s: --max-bytes not a number: %s\n' "$PROG" "$1" >&2; exit 2; }
      MAX_BYTES=$1
      ;;
    -h|--help) usage; exit 0 ;;
    --)
      shift
      while (($#)); do DIRS+=("$1"); shift; done
      break
      ;;
    -*)
      printf '%s: unknown option: %s\n' "$PROG" "$1" >&2
      usage >&2
      exit 2
      ;;
    *) DIRS+=("$1") ;;
  esac
  shift
done

((${#DIRS[@]})) || { usage >&2; exit 2; }
for d in "${DIRS[@]}"; do
  [[ -d $d ]] || { printf '%s: not a directory: %s\n' "$PROG" "$d" >&2; exit 2; }
done

tmpdir=$(mktemp -d "${TMPDIR:-/tmp}/no-name-signals.XXXXXX") || exit 2
trap 'rm -rf -- "$tmpdir"' EXIT

declare -a EXCL_CANON=()
for e in "${EXCLUDES[@]}"; do
  EXCL_CANON+=("$(readlink -f -- "$e" 2>/dev/null || printf '%s' "$e")")
done

if ((CODE_ONLY)); then
  ext_expr=( \( -name '*.sh' -o -name '*.py' \) )
else
  ext_expr=( \( -name '*.md' -o -name '*.sh' -o -name '*.py' -o -name '*.txt' -o -name '*.json' \) )
fi

declare -a FILES=()
declare -A SEEN=()
skipped_large=0
io_error=0
while IFS= read -r -d '' rec; do
  size=${rec%% *}
  path=${rec#* }
  if ((size > MAX_BYTES)); then
    skipped_large=$((skipped_large + 1))
    continue
  fi
  canon=$(readlink -f -- "$path" 2>/dev/null || printf '%s' "$path")
  [[ -n ${SEEN[$canon]:-} ]] && continue
  SEEN[$canon]=1
  skip=0
  for e in "${EXCL_CANON[@]}"; do
    if [[ $canon == "$e" || $canon == "$e"/* ]]; then skip=1; break; fi
  done
  ((skip)) || FILES+=("$path")
done < <(find "${DIRS[@]}" -type f "${ext_expr[@]}" -printf '%s %p\0' 2>/dev/null | sort -z)

if ((${#FILES[@]})); then
  # Stage 1: keep only files with any candidate token.
  declare -a CAND=()
  chunk=200
  for ((i = 0; i < ${#FILES[@]}; i += chunk)); do
    batch=("${FILES[@]:i:chunk}")
    grep -lZIE -- "$UNION" "${batch[@]}" >"$tmpdir/cand.$$" 2>"$tmpdir/canderr.$$"
    rc=$?
    if ((rc > 1)); then
      printf '%s: IO-ERROR cannot scan batch (%d file(s)): %s\n' "$PROG" "${#batch[@]}" "$(tr '\n' ' ' <"$tmpdir/canderr.$$")" >&2
      io_error=1
    fi
    while IFS= read -r -d '' f; do CAND+=("$f"); done <"$tmpdir/cand.$$"
  done
fi

hits_file=$tmpdir/hits.tsv
: > "$hits_file"
scanned=${#FILES[@]}
cand_count=0

for f in "${CAND[@]-}"; do
  [[ -n $f ]] || continue
  canon=$(readlink -f -- "$f" 2>/dev/null || printf '%s' "$f")
  [[ $canon == "$SELF" ]] && continue
  cand_count=$((cand_count + 1))
  rec_file=$tmpdir/rec.$$
  grep -nIE -- "$UNION" "$f" >"$rec_file" 2>"$tmpdir/err.$$"
  rc=$?
  if ((rc > 1)); then
    printf '%s: IO-ERROR cannot scan %s: %s\n' "$PROG" "$f" "$(tr '\n' ' ' <"$tmpdir/err.$$")" >&2
    io_error=1
    continue
  fi
  while IFS= read -r rec; do
    lineno=${rec%%:*}
    [[ $lineno =~ ^[0-9]+$ ]] || continue
    text=${rec#*:}
    cats=''
    [[ $text =~ $RE_PKILL ]] && cats+='pkill '
    [[ $text =~ $RE_KILLALL ]] && cats+='killall '
    [[ $text =~ $RE_CMDSUB ]] && cats+='kill-cmdsub '
    [[ $text =~ $RE_PSNAME ]] && cats+='kill-ps-name '
    [[ $text =~ $RE_XARGS ]] && cats+='xargs-kill '
    [[ -n $cats ]] || continue
    case $canon in
      *.sh|*.py) kind=code ;;
      *) kind=doc ;;
    esac
    disp=${text//$'\t'/ }
    if ((${#disp} > 300)); then disp="${disp:0:300}..."; fi
    printf '%s\t%s\t%s\t%s\t%s\n' "$f" "$lineno" "$kind" "${cats% }" "$disp" >>"$hits_file"
  done <"$rec_file"
done

sort -t$'\t' -k1,1 -k2,2n "$hits_file" >"$tmpdir/sorted.tsv"
hits=$(wc -l <"$tmpdir/sorted.tsv")

while IFS=$'\t' read -r p l k c t; do
  printf 'HIT %s:%s [%s; %s] %s\n' "$p" "$l" "$k" "$c" "$t"
done <"$tmpdir/sorted.tsv"

if ((hits > 0)); then
  printf '%s: %d hit(s), %d candidate file(s), %d scanned file(s), %d large file(s) skipped (> %d B)\n' \
    "$PROG" "$hits" "$cand_count" "$scanned" "$skipped_large" "$MAX_BYTES"
  if ((io_error)); then
    printf '%s: RESULT DIRTY-INCOMPLETE (exit 2: I/O error, see stderr)\n' "$PROG"
    exit 2
  fi
  printf '%s: RESULT DIRTY (exit 1)\n' "$PROG"
  exit 1
fi

printf '%s: 0 hits, %d candidate file(s), %d scanned file(s), %d large file(s) skipped (> %d B)\n' \
  "$PROG" "$cand_count" "$scanned" "$skipped_large" "$MAX_BYTES"
if ((io_error)); then
  printf '%s: RESULT INCOMPLETE (exit 2: I/O error, see stderr)\n' "$PROG"
  exit 2
fi
printf '%s: RESULT CLEAN (exit 0)\n' "$PROG"
exit 0
