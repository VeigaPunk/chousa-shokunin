#!/usr/bin/env python3
"""Build gate variants (mutants of the landed gate's grep-pin block) and
counter mutants (one requirement removed each) in scratch. Read-only on lane."""
import hashlib
import os
import re

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
OUT = "/tmp/hyaku/chousa-r35/w2/MutCounterC1"
G = os.path.join(OUT, "gates")
os.makedirs(G, exist_ok=True)

gate_src = open(os.path.join(LANE, "tools/research-gate.sh"), encoding="utf-8").read()
START = "# ---- grep pin (round-35 C1)"
END = "\nN_FINDINGS=0 N_DRIFT=0 ROLL=CLEAN"
i = gate_src.index(START)
j = gate_src.index(END)
PREFIX, SUFFIX = gate_src[:i], gate_src[j:]


def build(name, block):
    text = PREFIX + block.strip("\n") + "\n" + SUFFIX
    p = os.path.join(G, name)
    open(p, "w", encoding="utf-8").write(text)
    os.chmod(p, 0o755)
    h = hashlib.sha256(text.encode()).hexdigest()
    return p, h


COMMON_VERIFY = '''
grep_pin_verify() {
  local cand=$1 v
  [[ -f $cand && -x $cand ]] || return 1
  v=$("$cand" --version 2>/dev/null | head -n 1 || true)
  GREP_PIN_VERSION=$v
  case "$v" in
    *"GNU grep"*) return 0 ;;
  esac
  return 1
}
'''

ECHO = '''  if [[ ${CHOUSA_GREP_PIN_ECHO:-0} == 1 ]]; then
    printf 'GATE_GREP: path=%s source=%s version="%s"\\n' "$GREP_BIN" "$GREP_PIN_SOURCE" "$GREP_PIN_VERSION" >&2
  fi
}
'''

V1 = '''GREP_BIN=''
GREP_PIN_SOURCE=''
GREP_PIN_VERSION=''
grep() { command "$GREP_BIN" "$@"; }

grep_pin_refuse() { # REASON [CANDIDATE]
  printf 'research-gate: GREP_PROVENANCE refused: %s (candidate=%s)\\n' "$1" "${2:-<none>}" >&2
  exit 2
}
''' + COMMON_VERIFY + '''
grep_pin_init() {
  # V1: resolves grep through PATH (first absolute hit) instead of a fixed pin.
  local cand='' c=''
  if [[ -n ${RESEARCH_GATE_GREP:-} ]]; then
    cand=${RESEARCH_GATE_GREP}
    GREP_PIN_SOURCE=override
    case "$cand" in
      /*) ;;
      *) grep_pin_refuse "override is not an absolute path" "$cand" ;;
    esac
    [[ -f $cand ]] || grep_pin_refuse "override is not a regular file" "$cand"
    [[ -x $cand ]] || grep_pin_refuse "override is not executable" "$cand"
    grep_pin_verify "$cand" \\
      || grep_pin_refuse "override does not report GNU grep: ${GREP_PIN_VERSION:-<no version>}" "$cand"
  else
    GREP_PIN_SOURCE=default
    c=$(type -P grep 2>/dev/null || true)
    case "$c" in
      /*) if grep_pin_verify "$c"; then cand=$c; fi ;;
    esac
    if [[ -z $cand ]]; then
      c=/usr/bin/grep
      if grep_pin_verify "$c"; then cand=$c; fi
    fi
    [[ -n $cand ]] || grep_pin_refuse "no usable grep available" ''
  fi
  GREP_BIN=$cand
''' + ECHO

V2 = '''GREP_BIN=''
GREP_PIN_SOURCE=''
GREP_PIN_VERSION=''

grep_pin_refuse() { # REASON [CANDIDATE]
  printf 'research-gate: GREP_PROVENANCE refused: %s (candidate=%s)\\n' "$1" "${2:-<none>}" >&2
  exit 2
}

grep_pin_init() {
  # V2: sanitizes PATH instead of pinning; wrapper only on the override branch.
  PATH=/usr/bin:/bin
  export PATH
  GREP_BIN=/usr/bin/grep
  GREP_PIN_VERSION=$(command /usr/bin/grep --version 2>/dev/null | head -n 1 || true)
  if [[ -n ${RESEARCH_GATE_GREP:-} ]]; then
    GREP_PIN_SOURCE=override
    case "${RESEARCH_GATE_GREP}" in
      /usr/bin/grep) ;;
      /*) grep_pin_refuse "override is not the pinned binary" "${RESEARCH_GATE_GREP}" ;;
      *) grep_pin_refuse "override is not an absolute path" "${RESEARCH_GATE_GREP}" ;;
    esac
    grep() { command "$GREP_BIN" "$@"; }
  else
    GREP_PIN_SOURCE=default
  fi
''' + ECHO

V3 = '''GREP_BIN=''
GREP_PIN_SOURCE=''
GREP_PIN_VERSION=''
grep() { command "$GREP_BIN" "$@"; }

grep_pin_refuse() { # REASON [CANDIDATE]
  printf 'research-gate: GREP_PROVENANCE refused: %s (candidate=%s)\\n' "$1" "${2:-<none>}" >&2
  exit 2
}
''' + COMMON_VERIFY + '''
grep_pin_init() {
  # V3: walks PATH backwards, so the shim-first PATH is escaped but the gate is
  # still unusable without grep somewhere on PATH.
  local cand='' c='' i dir
  local -a dirs=()
  if [[ -n ${RESEARCH_GATE_GREP:-} ]]; then
    cand=${RESEARCH_GATE_GREP}
    GREP_PIN_SOURCE=override
    case "$cand" in
      /*) ;;
      *) grep_pin_refuse "override is not an absolute path" "$cand" ;;
    esac
    [[ -f $cand ]] || grep_pin_refuse "override is not a regular file" "$cand"
    [[ -x $cand ]] || grep_pin_refuse "override is not executable" "$cand"
    grep_pin_verify "$cand" \\
      || grep_pin_refuse "override does not report GNU grep: ${GREP_PIN_VERSION:-<no version>}" "$cand"
  else
    GREP_PIN_SOURCE=default
    IFS=: read -r -a dirs <<< "$PATH"
    for ((i = ${#dirs[@]} - 1; i >= 0; i--)); do
      dir=${dirs[i]}
      c=${dir:-.}/grep
      [[ -f $c && -x $c ]] || continue
      c=$(readlink -f "$c" 2>/dev/null || echo "$c")
      if grep_pin_verify "$c"; then cand=$c; break; fi
    done
    [[ -n $cand ]] || grep_pin_refuse "no PATH entry provides an executable grep" ''
  fi
  GREP_BIN=$cand
''' + ECHO

V4 = '''GREP_BIN=''
GREP_PIN_SOURCE=''
GREP_PIN_VERSION=''
grep() { command "$GREP_BIN" "$@"; }

grep_pin_refuse() { # REASON [CANDIDATE]
  printf 'research-gate: GREP_PROVENANCE refused: %s (candidate=%s)\\n' "$1" "${2:-<none>}" >&2
  exit 2
}
grep_pin_refuse_plain() { # REASON
  printf 'research-gate: bad grep override: %s\\n' "$1" >&2
  exit 2
}
''' + COMMON_VERIFY + '''
grep_pin_init() {
  # V4: syntax/existence refusals are plain exit 2 (no named refusal marker).
  local cand='' c=''
  if [[ -n ${RESEARCH_GATE_GREP:-} ]]; then
    cand=${RESEARCH_GATE_GREP}
    GREP_PIN_SOURCE=override
    case "$cand" in
      /*) ;;
      *) grep_pin_refuse_plain "not an absolute path: $cand" ;;
    esac
    [[ -f $cand ]] || grep_pin_refuse_plain "not a regular file: $cand"
    [[ -x $cand ]] || grep_pin_refuse_plain "not executable: $cand"
    grep_pin_verify "$cand" \\
      || grep_pin_refuse "override does not report GNU grep: ${GREP_PIN_VERSION:-<no version>}" "$cand"
  else
    GREP_PIN_SOURCE=default
    for c in /usr/bin/grep /bin/grep; do
      if grep_pin_verify "$c"; then cand=$c; break; fi
    done
    if [[ -z $cand ]]; then
      c=$(command -v grep 2>/dev/null || true)
      case "$c" in
        /*) if grep_pin_verify "$c"; then cand=$c; fi ;;
      esac
    fi
    [[ -n $cand ]] || grep_pin_refuse "no GNU grep found at /usr/bin/grep, /bin/grep or on PATH" ''
  fi
  GREP_BIN=$cand
''' + ECHO

V5 = '''GREP_BIN=''
GREP_PIN_SOURCE=''
GREP_PIN_VERSION=''
grep() { command "$GREP_BIN" "$@"; }

grep_pin_refuse() { # REASON [CANDIDATE]
  printf 'research-gate: GREP_PROVENANCE refused: %s (candidate=%s)\\n' "$1" "${2:-<none>}" >&2
  exit 2
}
grep_pin_refuse_plain() { # REASON
  printf 'research-gate: bad grep override: %s\\n' "$1" >&2
  exit 2
}
''' + COMMON_VERIFY + '''
grep_pin_init() {
  # V5: the non-GNU verify refusal is a plain exit 2 (no named refusal marker).
  local cand='' c=''
  if [[ -n ${RESEARCH_GATE_GREP:-} ]]; then
    cand=${RESEARCH_GATE_GREP}
    GREP_PIN_SOURCE=override
    case "$cand" in
      /*) ;;
      *) grep_pin_refuse "override is not an absolute path" "$cand" ;;
    esac
    [[ -f $cand ]] || grep_pin_refuse "override is not a regular file" "$cand"
    [[ -x $cand ]] || grep_pin_refuse "override is not executable" "$cand"
    grep_pin_verify "$cand" \\
      || grep_pin_refuse_plain "not GNU grep: ${GREP_PIN_VERSION:-<no version>} ($cand)"
  else
    GREP_PIN_SOURCE=default
    for c in /usr/bin/grep /bin/grep; do
      if grep_pin_verify "$c"; then cand=$c; break; fi
    done
    if [[ -z $cand ]]; then
      c=$(command -v grep 2>/dev/null || true)
      case "$c" in
        /*) if grep_pin_verify "$c"; then cand=$c; fi ;;
      esac
    fi
    [[ -n $cand ]] || grep_pin_refuse "no GNU grep found at /usr/bin/grep, /bin/grep or on PATH" ''
  fi
  GREP_BIN=$cand
''' + ECHO

V6 = '''GREP_BIN=''
GREP_PIN_SOURCE=''
GREP_PIN_VERSION=''
grep() { command "$GREP_BIN" "$@"; }

grep_pin_refuse() { # REASON [CANDIDATE]
  printf 'research-gate: GREP_PROVENANCE refused: %s (candidate=%s)\\n' "$1" "${2:-<none>}" >&2
  exit 2
}
''' + COMMON_VERIFY + '''
grep_pin_init() {
  # V6: pin and refusals are real, but the receipt echo omits source=.
  local cand='' c=''
  if [[ -n ${RESEARCH_GATE_GREP:-} ]]; then
    cand=${RESEARCH_GATE_GREP}
    GREP_PIN_SOURCE=override
    case "$cand" in
      /*) ;;
      *) grep_pin_refuse "override is not an absolute path" "$cand" ;;
    esac
    [[ -f $cand ]] || grep_pin_refuse "override is not a regular file" "$cand"
    [[ -x $cand ]] || grep_pin_refuse "override is not executable" "$cand"
    grep_pin_verify "$cand" \\
      || grep_pin_refuse "override does not report GNU grep: ${GREP_PIN_VERSION:-<no version>}" "$cand"
  else
    GREP_PIN_SOURCE=default
    for c in /usr/bin/grep /bin/grep; do
      if grep_pin_verify "$c"; then cand=$c; break; fi
    done
    if [[ -z $cand ]]; then
      c=$(command -v grep 2>/dev/null || true)
      case "$c" in
        /*) if grep_pin_verify "$c"; then cand=$c; fi ;;
      esac
    fi
    [[ -n $cand ]] || grep_pin_refuse "no GNU grep found at /usr/bin/grep, /bin/grep or on PATH" ''
  fi
  GREP_BIN=$cand
  if [[ ${CHOUSA_GREP_PIN_ECHO:-0} == 1 ]]; then
    printf 'GATE_GREP: path=%s version="%s"\\n' "$GREP_BIN" "$GREP_PIN_VERSION" >&2
  fi
}
'''

W2 = '''GREP_BIN=/usr/bin/grep
GREP_PIN_SOURCE=default
GREP_PIN_VERSION='grep (GNU grep) 3.12-modified'
grep() { command "$GREP_BIN" "$@"; }

grep_pin_refuse() { # REASON [CANDIDATE]
  printf 'research-gate: GREP_PROVENANCE refused: %s (candidate=%s)\\n' "$1" "${2:-<none>}" >&2
  exit 2
}

grep_pin_init() {
  # W2 (deliberately wrong): no resolution, no --version verification, canned
  # echo. "Verifies" an override by string equality with the hardcoded default.
  if [[ -n ${RESEARCH_GATE_GREP:-} ]]; then
    [[ ${RESEARCH_GATE_GREP} == /usr/bin/grep ]] \\
      || grep_pin_refuse "override is not the pinned binary" "$RESEARCH_GATE_GREP"
    GREP_PIN_SOURCE=override
  else
    GREP_PIN_SOURCE=default
  fi
  if [[ ${CHOUSA_GREP_PIN_ECHO:-0} == 1 ]]; then
    printf 'GATE_GREP: path=%s source=%s version="%s"\\n' "$GREP_BIN" "$GREP_PIN_SOURCE" "$GREP_PIN_VERSION" >&2
  fi
}
'''

V7 = '''GREP_BIN=''
GREP_PIN_SOURCE=''
GREP_PIN_VERSION=''
grep_pin_refuse() { # REASON [CANDIDATE]
  printf 'research-gate: GREP_PROVENANCE refused: %s (candidate=%s)\\n' "$1" "${2:-<none>}" >&2
  exit 2
}

grep_pin_verify() {
  local cand=$1 v
  [[ -f $cand && -x $cand ]] || return 1
  v=$("$cand" --version 2>/dev/null | head -n 1 || true)
  GREP_PIN_VERSION=$v
  case "$v" in
    *"GNU grep"*) return 0 ;;
  esac
  return 1
}

grep_pin_init() {
  # V7: wrapper only on the default branch; an override falls back to bare grep.
  local cand='' c=''
  if [[ -n ${RESEARCH_GATE_GREP:-} ]]; then
    cand=${RESEARCH_GATE_GREP}
    GREP_PIN_SOURCE=override
    case "$cand" in
      /*) ;;
      *) grep_pin_refuse "override is not an absolute path" "$cand" ;;
    esac
    [[ -f $cand ]] || grep_pin_refuse "override is not a regular file" "$cand"
    [[ -x $cand ]] || grep_pin_refuse "override is not executable" "$cand"
    grep_pin_verify "$cand" \\
      || grep_pin_refuse "override does not report GNU grep: ${GREP_PIN_VERSION:-<no version>}" "$cand"
  else
    GREP_PIN_SOURCE=default
    for c in /usr/bin/grep /bin/grep; do
      if grep_pin_verify "$c"; then cand=$c; break; fi
    done
    if [[ -z $cand ]]; then
      c=$(command -v grep 2>/dev/null || true)
      case "$c" in
        /*) if grep_pin_verify "$c"; then cand=$c; fi ;;
      esac
    fi
    [[ -n $cand ]] || grep_pin_refuse "no GNU grep found at /usr/bin/grep, /bin/grep or on PATH" ''
    grep() { command "$GREP_BIN" "$@"; }
  fi
  GREP_BIN=$cand
  if [[ ${CHOUSA_GREP_PIN_ECHO:-0} == 1 ]]; then
    printf 'GATE_GREP: path=%s source=%s version="%s"\\n' "$GREP_BIN" "$GREP_PIN_SOURCE" "$GREP_PIN_VERSION" >&2
  fi
}

'''
variants = {"V1": V1, "V2": V2, "V3": V3, "V4": V4, "V5": V5, "V6": V6, "V7": V7, "W2": W2}
manifest = {}
for name, block in variants.items():
    p, h = build(name + ".sh", block)
    manifest[name] = {"path": p, "sha256": h}
    print(name, h)

# counter mutants
cnt = open(os.path.join(LANE, "corpus/evidence/round35/c1-count.py"), encoding="utf-8").read()
MUTS = {
    "M1": [('score("S1-shim-first-path", empty_trip(trip1) and same_as_ref(rc, out),',
            'score("S1-shim-first-path", same_as_ref(rc, out),')],
    "M2": [('score("S2-bash-env-function", empty_trip(trip2) and same_as_ref(rc, out),',
            'score("S2-bash-env-function", same_as_ref(rc, out),')],
    "M3": [('score("S3-no-grep-on-path", same_as_ref(rc, out) and "not found" not in err,',
            'score("S3-no-grep-on-path", "not found" not in err,')],
    "M4": [('score("S4-override-relative", rc == 2 and "GREP_PROVENANCE" in err,',
            'score("S4-override-relative", rc == 2,'),
           ('score("S5-override-missing", rc == 2 and "GREP_PROVENANCE" in err,',
            'score("S5-override-missing", rc == 2,')],
    "M5": [('score("S6-override-non-gnu", rc == 2 and "GREP_PROVENANCE" in err,',
            'score("S6-override-non-gnu", rc == 2,')],
    "M6": [('same_as_ref(rc, out) and "path=%s" % REAL_GREP in line and "source=override" in line and "GNU grep" in line,',
            'same_as_ref(rc, out),'),
           ('same_as_ref(rc, out) and "path=%s" % REAL_GREP in line and "source=default" in line and "GNU grep" in line,',
            'same_as_ref(rc, out),'),
           ('empty_trip(trip2) and same_as_ref(rc, out) and "source=override" in line,',
            'empty_trip(trip2) and same_as_ref(rc, out),')],
}
for name, reps in MUTS.items():
    text = cnt
    for old, new in reps:
        assert text.count(old) == 1, (name, old, text.count(old))
        text = text.replace(old, new)
    p = os.path.join(OUT, "c1-count.%s.py" % name)
    open(p, "w", encoding="utf-8").write(text)
    print(name, hashlib.sha256(text.encode()).hexdigest(), p)

import json
json.dump(manifest, open(os.path.join(OUT, "gate-manifest.json"), "w"), indent=1, sort_keys=True)
