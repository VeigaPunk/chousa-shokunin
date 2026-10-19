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
#   CLAIM_RECORD_INVALID CLAIM_SOURCE_EXTERNAL CLAIM_SOURCE_OUT_OF_CORPUS
#   CLAIM_SOURCE_SESSION CLAIM_SOURCE_EPHEMERAL CLAIM_SOURCE_MISSING
#   CLAIM_SPAN_NOT_FOUND CLAIM_SPAN_UNEXPECTED CONTRADICTION_MARKER_ABSENT
#   SWEEP_REJECTION_INCOMPLETE SWEEP_LOCATION_ABSENT SWEEP_LOCATION_UNRESOLVED
#   SWEEP_LOCATION_OUT_OF_CORPUS SWEEP_CLAIM_FALSE REF_UNRESOLVED
#   VERIFY_ALL_CLAIMS_UNRESOLVED VERIFY_ALL_SECTION_UNAVAILABLE
#   SCOPE_BOUNTY_ABSORBED SCOPE_MODEL_QUALITY_ABSORBED
#   SCOPE_ORCHESTRATION_ABSORBED
#   CLAIM_SOURCE_READ_TOO_LARGE (r12: source over SOURCE_READ_MAX_BYTES)
#   CLAIM_SOURCE_MULTILINKED (r13: hardlink alias of possibly out-of-corpus
#   content; a symlink's true path is re-checked, a hardlink's partners are
#   not soundly enumerable — refused unread)
#   CLAIM_SOURCE_CROSS_DEVICE (r14: source st_dev differs from the resolving
#   root's device — a bind alias keeps its path and nlink but not its
#   superblock device; same-device binds stay invisible — refused unread)
#
# Claims mode: verify-claims <claims-file> checks each claim's verbatim span
# against its cited source. Blank lines and #-comment lines are ignored; a
# {"marker_default":…} line sets the default contradiction marker and is not a
# claim. Every other line is one JSON claim {"id","source","span","expect"} with
# expect supported|contradicted|unsupported. Sources are local files under the
# same boundary as verify pointers (canonicalized; session paths denied, URLs
# refused — never fetched). expect=contradicted additionally needs a marker the
# fixture names explicitly (per-claim "marker" or the default) to byte-co-occur
# inside the span's source lines; without it the claim is unproven. A marker on
# a non-contradicted entry is a fixture violation (CLAIM_RECORD_INVALID).
# A source larger than SOURCE_READ_MAX_BYTES (8 MiB, inclusive boundary) is
# refused BEFORE any read — CLAIM_SOURCE_READ_TOO_LARGE (warn, drift;
# CHAIN_SOURCE_READ_TOO_LARGE in chain mode) — never partially searched.
# A multi-linked source is likewise refused unread —
# CLAIM_SOURCE_MULTILINKED (crit, drift; CHAIN_SOURCE_MULTILINKED in chain
# mode): an in-root hardlink alias can name out-of-corpus content that
# readlink -f cannot see. The refusal is nlink-based, so a legit in-root
# multi-link family refuses too (named limit). A source whose st_dev differs
# from the resolving root's device is refused unread —
# CLAIM_SOURCE_CROSS_DEVICE (crit, drift; CHAIN_SOURCE_CROSS_DEVICE in chain
# mode): a bind alias keeps its in-root path and its nlink but not its
# superblock device. Same-device binds are stat-invisible and stay a named
# limit (mount-alias-r14.md). Probe order at the chokepoint is nlink, then
# size, then device — a combined source reports the earliest class.
# Per claim: CLAIM id=… expected=… observed=… source=… at=… verdict=…
#   observed: supported|contradicted|unsupported|unproven|refused|invalid
#   verdict:  match|mismatch|refused|invalid
# Summary: VERDICT_BEARING_CLAIMS=N/M — N claims whose observed status matched
# the pre-registered expectation, over the M claims read; CLEAN only when N=M.
# The RESEARCH_GATE line counts observed dispositions: claims, supported,
# contradicted, unsupported, mismatched (adjudicated but != expect), unproven,
# refused, invalid, findings, drift — so a CLEAN run shows claims=Σdispositions,
# mismatched=refused=invalid=0 and N=M.
#
# Chain mode: verify-chain <record.md> resolves each hop's citation — the r1
# verify path checks hops only structurally, so a resolved hop may cite an
# anchor the target never contains. A resolved hop must carry a citation:
# source = a source id declared in ## Sources (any id, not only S…) or a local
# path (same boundary and canonicalization as verify-claims) plus an anchor
# the source must contain —
# heading (a Markdown heading whose trimmed text equals the anchor), quote
# (verbatim span, line-aware misses), or line (one whole line, trailing
# whitespace trimmed). Anchor comes from an `anchor_kind`+`anchor` column pair
# or from a `to` fragment: path#kind:text (a bare #text reads as a heading).
# Unresolved/marked hops (unresolved blocked-no-fetch rejected labelled-dead
# not-applicable) stay exempt but counted. Per hop:
#   CHAIN hop=… status=… observed=… source=… anchor=… at=… verdict=…
#   observed: verified|anchor-missing|refused|invalid|exempt
#   verdict:  match|mismatch|refused|invalid|exempt
# Summary: RESOLVED_HOPS=N/M — N verified hops over M hops read; CLEAN iff
# every non-exempt hop verified (N = M − exempt) and no finding drifts.
# Extra ids: CHAIN_ABSENT CHAIN_SOURCE_EXTERNAL CHAIN_SOURCE_SESSION
#   CHAIN_SOURCE_EPHEMERAL CHAIN_SOURCE_OUT_OF_CORPUS CHAIN_SOURCE_MISSING
#   CHAIN_SOURCE_READ_TOO_LARGE
#   CHAIN_SOURCE_MULTILINKED (r13)
#   CHAIN_SOURCE_CROSS_DEVICE (r14)
#   CHAIN_ANCHOR_NOT_FOUND CHAIN_CITATION_INVALID
#
# Sweeps mode: verify-sweeps <record.md> makes kept rejections and negative
# sweeps verdict-bearing. Every ## Rejections row needs a non-empty reason and
# a non-empty flip-condition (a flip/flip_condition column, or any column whose
# name contains flip/falsif/reversal); a rejection missing either is
# SWEEP_REJECTION_INCOMPLETE and counts incomplete (drift).
# Every negative sweep — a ## Sweeps row, or a Negatives row carrying a
# where/looked_at/… column or a clean sweep cell — must name where it looked.
# A local path set (a whitespace-free comma/semicolon list of paths/globs) is
# re-run: any glob hit is SWEEP_CLAIM_FALSE naming the hit (zero hits verify).
# Non-local sets (http(s)://…, local://…, external:…, web:…, session:…) and
# declared source ids are exempt but counted — a content sweep carries no
# probe the gate could re-run. A path escaping the corpus boundary is refused
# unopened (SWEEP_LOCATION_OUT_OF_CORPUS), an undeclared source id is
# SWEEP_LOCATION_UNRESOLVED, a sweep naming nowhere is SWEEP_LOCATION_ABSENT.
# A row marked unresolved/blocked-no-fetch/labelled-dead/not-applicable in a
# status column is exempt like an unresolved hop. Per item:
#   SWEEP id=… where=… looked=local|source-ids|non-local|exempt|unnamed
#     hits=… at=… observed=verified|hit|exempt|refused|invalid
#     verdict=match|mismatch|exempt|refused|invalid
#   REJECTION id=… ref=… reason=present|absent flip=present|absent
#     observed=complete|incomplete verdict=match|mismatch
# Summary: VERIFIED_SWEEPS=N/M REJECTIONS_OK=K/L — N sweeps re-verified empty
# of M sweep items read (exempt counted); K complete rejections of L read.
# CLEAN iff verified+exempt=M and K=L and no finding drifts.
#
# A where value containing whitespace is read as a command/description: its
# structured words (URLs, ids, path/glob-shaped tokens) are extracted, other
# words ignored — so an r1-style `test ! -f lib/ghost.md` cell names
# lib/ghost.md. Whitespace-free values are split on commas/semicolons only.
#
# Integrity mode: verify-integrity <record> resolves every cross-section
# reference against the rows that declare it — the r6 hole where a sweep cell
# could name a claim id no ## Claims row declares, or a hop/rejection a source
# id no ## Sources row declares, and nothing checked. Declared ids: source ids
# from ## Sources; claim ids from ## Claims and ## Negatives; sweep ids from
# ## Sweeps. Reference cells: chain from/to/claim (a to fragment after # is
# stripped); claims sweep and source/src/ref/cite/pointer; negatives
# sweep/where; sweeps claim_id and where; rejections ref/reference. Each
# whitespace/comma/semicolon-separated token of a reference cell is classified
# once: a token equal to a declared id resolves (kind=source|claim|sweep — any
# declared id, not only the …<digit> shapes); a token in an undeclared id shape
# (S<digit>…, C|N<digit>…, SW<digit>…) is REF_UNRESOLVED severity=warn (drift)
# naming kind, id, section, row and cell; a non-local naming (URLs; local://
# artifact:// agent:// proc:// history://; external: web: live: chat: session:)
# is exempt; local paths/globs, prose and sentinels are not integrity tokens
# and are not counted (the sweeps/claims/chain sections own them). Exempt-but-
# counted, as in the hop/sweep idioms: a chain row whose status is
# unresolved|blocked-no-fetch|rejected|labelled-dead|not-applicable, and a
# sweeps/negatives row whose status is
# unresolved|blocked-no-fetch|labelled-dead|not-applicable, has its reference
# tokens counted exempt rather than required to resolve; a non-local naming
# stays exempt wherever a location is named. Per reference:
#   REF kind=… id=… section=… row=… cell=… observed=resolved|unresolved|exempt
#     verdict=match|mismatch|exempt [status=…|reason=non-local]
# Summary: INTEGRITY refs=N resolved=M unresolved=K — N counts every extracted
# reference token (exempts included), M resolved, K unresolved; the exempt
# count is N−M−K. resolved counts each occurrence once; CLEAN iff K=0 and no
# finding drifts.
#
# verify-all mode: verify-all <record> [--claims PATH] [--json PATH] runs every
# applicable mode over one input as fresh gate calls and composes one verdict.
# Applicable: structure — always, for a Markdown record; claims — when a claims
# surface is bound (the input itself when it is a claims JSONL: no ## section
# lines and at least one JSON-object line; else --claims PATH; else a ## Meta
# row named claims/claims_file/claims-file/claimset, boundary-checked like a
# source); chain — when the record declares ## Chain; sweeps — when it declares
# ## Sweeps, ## Negatives or ## Rejections; integrity — whenever at least one
# other section runs (it cross-checks the ids the record declares, so a record
# with no sections has no reference token and reports refs=0). An ABSENT
# section is reported state=absent and never drifts by itself; the composed
# verdict is DRIFT iff any RUN section drifts. Sections execute the same CLI
# paths (bash "$SELF" <mode>), so each section tally is that solo mode's tally
# by construction — including integrity's tally, which is the solo mode's
# INTEGRITY summary.
#   SECTION <name> state=absent
#   SECTION <name> state=run verdict=… findings=N drift=N [tally=…]
# followed by that section's FINDING lines, then
#   VERIFY_ALL sections=5 run=N absent=N drift-sections=N findings=N drift=N
# and one closing RESEARCH_GATE: CLEAN|DRIFT with the same composed counters.
# --json PATH appends (>>, never rewrites) one JSON line: schema, UTC, record
# and gate SHA-256, per-section state/verdict/tallies, composed verdict.
#
# Pin/drift mode: the gate's own behavioral baseline, adapted from
# mori-shokunin r10 (tools/mori-census.sh --pin/--drift; its contract note
# corpus/knowledge/drift-pin-r10.md and the lesson
# 2026-10-15-volatile-contract-behavioral-baselines.md there), sized down to a
# gate whose canonical output is deterministic per input.
#   --pin PATH    runs the canonical reference invocation, normalizes it and
#                 writes a baseline text file to PATH. Exit 0 on success —
#                 pinning a run that itself rolls DRIFT is still a pin — and
#                 exit 2 when the capture or the write fails. Prints one
#                 GATE_PIN: ok path=… gate_sha256=… line.
#   --drift PATH  re-runs the same invocation, normalizes with the CURRENT
#                 rules and byte-compares against the baseline body:
#                   equal  -> GATE_DRIFT: none               exit 0
#                   differ -> GATE_DRIFT: <tokens>           exit 1
#                   baseline missing, unreadable, malformed, or the capture
#                   failing -> message on stderr              exit 2
#                 Writes nothing. Neither mode prints a RESEARCH_GATE line:
#                 their contract is the GATE_PIN/GATE_DRIFT line and the exit
#                 code, so a consumer counting verdict lines cannot mistake a
#                 baseline operation for a record verdict.
# The canonical invocation is `verify-all record.md --claims claims.jsonl
# --json manifest.jsonl --root .` run with cwd = a fresh temp fixture the gate
# writes itself (the same recipe shape its selftest uses). The fixture's
# record has four CLEAN sections and one integrity finding, so the capture
# covers SECTION, FINDING, VERIFY_ALL and composed-verdict lines, and the
# appended --json line is the receipt the manifest mode writes. Every printed
# path is relative, so the capture is byte-stable wherever the gate is run;
# the fixture is written and removed by the capture, never committed.
# Volatile contract (recorded verbatim in every baseline header; masked values
# are replaced by <V>):
#   ts           the header clock and the manifest "ts": the single live input
#                of the canonical invocation. Masked shape-scoped — only
#                ts=<YYYY-MM-DDTHH:MM:SSZ> and "ts":"…" match; a malformed
#                timestamp keeps its bytes and surfaces as drift.
#   gate_sha256  the manifest's revision stamp: masked so the pin compares
#                behavior, not revision (mori r10's script_sha256 rule; a
#                comment-only edit is `none`).
# Everything else is compared unmasked, including record_sha256 (the fixture
# bytes are part of the behavior) and every contract word (VERSION, mode=,
# record=, claims=, root=, state=, verdict=, findings=, drift=, tally=,
# severity=, surface=, obs=), so editing one is drift.
# Drift tokens (LC_ALL=C sorted, space-joined): <key> a non-volatile key=value
# whose value changed; -<key>/+<key> a field a changed line dropped/added;
# -<id>/+<id> a line removed/added, id in GATE MANIFEST VERIFY_ALL VERDICT
# SECTION:<name> FINDING:<id> LINE; output-order for a pure reorder;
# volatile_fields when the baseline's declared volatile list differs from the
# current one (changing the contract is itself drift).
#
# Token boundaries (matching semantics shared by claims spans and chain quote
# anchors — the substring classes): an occurrence of a span/quote counts only
# when both of its outer edges sit at a token boundary, i.e. the character
# immediately before it and the character immediately after it are each one of
# {file edge, line edge (newline), ASCII whitespace (space tab CR LF VT FF),
# ASCII punctuation}. `-` and `'` are boundaries only when they do not join
# two word characters: a word-internal hyphen/apostrophe is part of its word
# (`cross-check`, `workers'`), so an occurrence ending or starting mid-word is
# not a hit. A word character is an ASCII letter, an ASCII digit, or any
# non-ASCII character; `_` is ASCII punctuation here (Markdown emphasis), so it
# is a boundary, while `—`, `。` and other non-ASCII bytes are not boundaries —
# an undecidable edge fails closed. Only the outer edges are checked, so a
# multi-line span is delimited by its first and last character alone and may
# cut mid-token inside. Matching stays byte-exact and case-sensitive, and the
# reported hit is the first delimited occurrence (line:N, or lines:N-M when it
# spans lines). A substring occurrence glued into a word (a truncated
# `…kiwami semantic`, a padded extra word running into a longer source token, a
# possessive) is a miss and takes the existing line-aware not-found report.
#
# Secrecy: print path:line class=<name> only — never span.
# Opens: allowlist metadata only; denylist → SESSION_READ.
# research/README CDP 9222 is provenance, not a hop.
#
set -euo pipefail
shopt -s extglob

# Banner contract (r12): the version token is the revision alone and never
# repeats the program name — v1 rendered the stutter "research-gate
# research-gate-r1" at every banner site. v2 = this corrected generation.
# The version token is a declared contract word (NOT in volatile_fields), so
# changing it is gate drift by design and requires a recorded re-pin. The
# baseline file-format magic "# chousa-gate drift baseline v1" is a separate
# counter and is not bumped.
VERSION=v2

# Claim/chain source read cap (r12). A source larger than this is refused
# BEFORE any read, so an oversized file is neither slurped into a shell
# variable nor partially searched. 8 MiB = 8388608; the boundary is
# inclusive (size == cap reads; size == cap+1 refuses).
SOURCE_READ_MAX_BYTES=$((8 * 1024 * 1024))
SELF=$(readlink -f -- "${BASH_SOURCE[0]}" 2>/dev/null || {
  p=$0; case "$p" in /*) printf '%s' "$p" ;; *) printf '%s' "$PWD/$p" ;; esac
})
SCRIPT_DIR=$(cd -- "$(dirname -- "$SELF")" && pwd)
LANE_ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd)

MODE=verify
RECORD_ARG=""
PIN_ARG=""
DRIFT_ARG=""
ROOT_ARG_SET=0
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
       research-gate.sh verify-claims [CLAIMS] [--root PATH]
       research-gate.sh verify-chain [RECORD] [--root PATH]
       research-gate.sh verify-sweeps [RECORD] [--root PATH]
       research-gate.sh verify-integrity [RECORD] [--root PATH]
       research-gate.sh verify-all [RECORD] [--claims PATH] [--json PATH]
                      [--root PATH]
       research-gate.sh --pin PATH
       research-gate.sh --drift PATH
       research-gate.sh [--record PATH] [--root PATH]

  RECORD via --record, positional, or CHOUSA_RECORD.
  CLAIMS via positional or CHOUSA_CLAIMS.
  Claims file: one JSON object per claim line:
    {"id":…,"source":…,"span":…,"expect":supported|contradicted|unsupported
     [,"marker":…]}
  Spans must appear verbatim in sources at token boundaries; sources are
  local files only.
  Chain mode: each hop with status=resolved must cite a source (a source id
  from ## Sources, or a local path) plus an anchor — an anchor_kind column
  (heading|quote|line) with an anchor column, or a to fragment
  path#kind:text (bare #text = heading). The anchor must appear in the cited
  source: headings by text, quotes verbatim at token boundaries, lines as
  whole lines.
  Unresolved/marked hops stay exempt but counted. Sources obey the same
  boundary as verify-claims (local, canonicalized, never fetched).
  Sources over 8 MiB are refused unread (CLAIM_SOURCE_READ_TOO_LARGE;
  CHAIN_SOURCE_READ_TOO_LARGE in chain mode). Multi-linked sources are
  refused unread (CLAIM_SOURCE_MULTILINKED; CHAIN_SOURCE_MULTILINKED in
  chain mode) — a hardlink alias can name out-of-corpus content. Cross-device
  sources are refused unread (CLAIM_SOURCE_CROSS_DEVICE;
  CHAIN_SOURCE_CROSS_DEVICE in chain mode) — a bind alias keeps its path and
  nlink but not its superblock device; the comparison is against the
  resolving root's device.
  A token boundary is a file/line edge, ASCII whitespace or ASCII
  punctuation at the match's outer edges; a word-internal hyphen or
  apostrophe is not a boundary, so a truncated quote (mid-word), a padded
  extra word running into a longer token, or a possessive join is a miss.
  Multi-line spans are delimited by their first and last character only.
  Sweeps mode: every ## Rejections row needs a non-empty reason and a
  non-empty flip-condition (flip/flip_condition column, or any column whose
  name contains flip/falsif/reversal). Negative sweeps must name where they
  looked (a where/looked_at column, or a clean sweep cell): local path sets
  (comma-separated paths/globs) are re-run — any hit is SWEEP_CLAIM_FALSE
  naming the hit, zero hits verify; URLs, external:/web:/session: names and
  declared source ids count as exempt; a sweep naming nowhere drifts.
  Summary: VERIFIED_SWEEPS=N/M REJECTIONS_OK=K/L.
  Integrity mode: every cross-section reference token must resolve to a row
  that declares it — source ids from ## Sources, claim ids from ## Claims and
  ## Negatives, sweep ids from ## Sweeps — read from chain from/to/claim,
  claims sweep/source/src/ref/cite/pointer, negatives sweep/where, sweeps
  claim_id/where and rejections ref/reference cells. An undeclared id in the
  S<digit>… / C|N<digit>… / SW<digit>… shapes is REF_UNRESOLVED (drift);
  declared ids resolve; non-local namings and rows marked
  unresolved/blocked-no-fetch/labelled-dead/not-applicable/rejected stay
  exempt but counted; local paths/globs and prose are not integrity tokens.
  Summary: INTEGRITY refs=N resolved=M unresolved=K (exempt = N−M−K).
  verify-all composes structure + claims + chain + sweeps + integrity over ONE
  input: absent sections are reported absent (never drift by themselves); the
  composed verdict is DRIFT iff any run section drifts, exit 1. --claims
  binds a claims file to a record; a record may also name one in a ## Meta
  row (claims/claims_file/claims-file/claimset); a claims JSONL passed as
  the input is its own claims surface. --json PATH appends (never rewrites)
  one JSON line recording UTC, record + gate SHA-256, per-section tallies
  and the composed verdict.
  Pin/drift: --pin PATH writes a behavioral baseline of the gate's canonical
  reference run (verify-all over a hermetic fixture the gate writes itself,
  plus that run's --json manifest line), with the declared volatile contract
  (ts, gate_sha256) recorded in its header; exit 0, or 2 when the capture or
  the write fails. --drift PATH re-runs the same invocation and byte-compares
  the normalized captures: GATE_DRIFT: none exit 0, GATE_DRIFT: <changed
  tokens> exit 1, baseline missing/unreadable/malformed (or a failed capture)
  exit 2. Neither mode prints a RESEARCH_GATE line.
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
  # r17: a `## ` line inside a fenced code block is literal text, not a
  # heading — a fenced `## Meta` must not reset the real Meta body. Two
  # passes: first pair fences (same char, closing length >= opening, 0-3
  # literal-space indent; an unclosed opener is plain text = fail closed),
  # then skip `## ` lines inside paired fences.
  local -a LINES=()
  local fence_char='' fence_len=0 unclosed=-1
  local i n c l
  while IFS= read -r line || [[ -n $line ]]; do LINES+=("$line"); done <"$file"
  n=${#LINES[@]}
  for ((i = 0; i < n; i++)); do
    line=${LINES[$i]}
    if [[ -n $fence_char ]]; then
      if [[ $line =~ ^\ {0,3}(\`{3,}|~{3,})[[:space:]]*$ ]]; then
        c=${BASH_REMATCH[1]:0:1}; l=${#BASH_REMATCH[1]}
        [[ $c == "$fence_char" && $l -ge $fence_len ]] && fence_char=''
      fi
    elif [[ $line =~ ^\ {0,3}(\`{3,}|~{3,})(.*)$ ]]; then
      fence_char=${BASH_REMATCH[1]:0:1}; fence_len=${#BASH_REMATCH[1]}; unclosed=$i
    fi
  done
  [[ -n $fence_char ]] || unclosed=-1
  # r17: an unclosed opener IS a fence — everything after it is literal
  # (fail closed: a `## ` inside an unclosed fence cannot shadow a real
  # heading). The opener itself is consumed as fence content.
  fence_char=''; fence_len=0
  for ((i = 0; i < n; i++)); do
    line=${LINES[$i]}
    if [[ -n $fence_char ]]; then
      if [[ $line =~ ^\ {0,3}(\`{3,}|~{3,})[[:space:]]*$ ]]; then
        c=${BASH_REMATCH[1]:0:1}; l=${#BASH_REMATCH[1]}
        [[ $c == "$fence_char" && $l -ge $fence_len ]] && fence_char=''
      fi
      [[ -z $sec ]] && continue
      SEC_BODY[$sec]+="$line"$'\n'
      continue
    fi
    if [[ $line =~ ^\ {0,3}(\`{3,}|~{3,})(.*)$ ]]; then
      fence_char=${BASH_REMATCH[1]:0:1}; fence_len=${#BASH_REMATCH[1]}
      [[ -z $sec ]] && continue
      SEC_BODY[$sec]+="$line"$'\n'
      continue
    fi
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
  done
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
  # r15: in_root normalizes the prefix (raw "$root_r"/* is //* with --root /);
  # the -f test still refuses the root directory itself.
  if in_root "$f" "$root_r" && [[ -f $f ]]; then return 0; fi
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

in_root() { # CANON ROOT -> rc 0 when CANON is ROOT itself or under it
  # r15 root-slash boundary: the prefix test must survive ROOT=/ — the raw
  # form "$root"/* renders //* there and matches nothing (measured), refusing
  # every absolute source OUT_OF_CORPUS. The trailing slash is stripped for
  # the PREFIX TEST ONLY: callers keep the un-normalized root for identity
  # decisions (claim_source_path's device probe stats the declared root,
  # r14 contract). A materialized helper, not an inline "${root%/}" in a
  # case word — the empty expansion inside a case pattern still dead-arms.
  local c=$1 r=$2
  # r16: strip ALL trailing slashes — pwd -P preserves '//' (measured:
  # 'cd // && pwd -P' → '//'), so a single ${r%/} leaves '/' which still
  # renders '//*'. The loop collapses '//' → '/' → ''.
  while [[ $r == */ && $r != / ]]; do r=${r%/}; done
  [[ $r == / ]] && r=
  [[ $c == "$r" || $c == "$r"/* ]]
}

file_size_bytes() { # PATH -> stdout byte size; rc 1 when no probe can measure
  local n                        # it. stat is the pre-read probe (no data
  if n=$(stat -c '%s' -- "$1" 2>/dev/null); then printf '%s' "$n"; return 0; fi
  if n=$(stat -f '%z' -- "$1" 2>/dev/null); then printf '%s' "$n"; return 0; fi
  if n=$(wc -c <"$1" 2>/dev/null); then
    n=${n//[[:space:]]/}
    [[ $n =~ ^[0-9]+$ ]] && { printf '%s' "$n"; return 0; }
  fi
  return 1
}

# ---- structure: declared-scope refusal screen (round 12) ----
# Only the DECLARED surface is read: rows of the record's own ## Meta section
# whose key cell is `domain` or `scope` — both the Meta table row
# `| scope | value |` and the `scope: value` line row. Prose, ## Question
# text, note cells, source/archive pointers and every other section are never
# keyword-scanned: the r9 B archive names multi-agent knowledge in prose and
# its record stays CLEAN. One finding per matched refused province per
# declaration row, provinces in the fixed order bounty → model-quality →
# orchestration, so multi-province declarations pin reproducible line order.
# Deliberately NOT triggers: bare bounty/agent/swarm/dispatch/eval(uation)/
# quality/benchmark/model — they carry legitimate research senses (the
# B-archive vocabulary) and negations are not parsed (named limit). warn
# drifts (exit 1); a record with no declaration row takes the old path
# byte-identically.
SCOPE_BOUNTY='bug bounty|bounty program|bounty programs|bounty hunt|bounty hunting|bounty scope|claim package|claim packages|kasegi'
# r18: llm benchmark(s) and llm scoring were missing despite the model-
# quality boundary (the wave's adversary seats confirmed they are refused-
# province phrases; ai benchmark(s) stays out — too broad for AI-methodology
# research, named debt). The plural form needs a separate entry: scope_hit
# matches literal phrases, never stems.
SCOPE_KENGAKU='model quality|model evaluation|model evaluations|model eval|model benchmark|model benchmarks|model scoring|llm quality|llm evaluation|llm eval|llm benchmark|llm benchmarks|llm scoring|language model quality|language model evaluation|kengaku'
SCOPE_KUMITATE='orchestration|dispatch mechanism|multi agent dispatch|multiagent dispatch|agent dispatch|swarm wave|swarm waves|swarm call|swarm calls|swarm dispatch|swarm orchestration|fleet dispatch|agent lifecycle|agent lifecycles|agent roster|agent rosters|kumitate'
scope_norm() { # VALUE -> lowercase, punctuation runs -> single spaces, trimmed
  local v=$1
  v=$(printf '%s' "$v" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' \
        | sed -E 's/^["\x27\x60]//;s/["\x27\x60]$//')
  printf '%s' "$v" | tr 'A-Z' 'a-z' \
    | LC_ALL=C sed 's/[^a-z0-9][^a-z0-9]*/ /g;s/^ //;s/ $//'
}
scope_hit() { # NORMED LIST(|-separated phrases) -> first phrase contained, or ''
  local v=" $1 " p
  local IFS='|'
  for p in $2; do
    if [[ $v == *" $p "* ]]; then printf '%s' "$p"; return 0; fi
  done
  printf ''
}
scope_decl_screen() { # screens SEC_BODY[Meta]; emits SCOPE_* warn per refused row
  local row mk mv hit id prov
  while IFS= read -r row; do
    [[ -z $row ]] && continue
    mk='' mv=''
    if [[ $row =~ ^[[:space:]]*\|[[:space:]]*([A-Za-z_][A-Za-z0-9_-]*)[[:space:]]*:?[[:space:]]*\|[[:space:]]*([^|]*)\| ]]; then
      mk=${BASH_REMATCH[1]}; mv=${BASH_REMATCH[2]}
    elif [[ $row =~ ^[[:space:]]*([A-Za-z_][A-Za-z0-9_-]*)[[:space:]]*:[[:space:]]*(.*)$ ]]; then
      mk=${BASH_REMATCH[1]}; mv=${BASH_REMATCH[2]}
    else
      continue
    fi
    mk=$(printf '%s' "$mk" | tr 'A-Z' 'a-z')
    [[ $mk == domain || $mk == scope ]] || continue
    mv=$(scope_norm "$mv")
    [[ -n $mv ]] || continue
    for prov in bounty kengaku kumitate; do
      case $prov in
        bounty)   id=SCOPE_BOUNTY_ABSORBED        hit=$(scope_hit "$mv" "$SCOPE_BOUNTY") ;;
        kengaku)  id=SCOPE_MODEL_QUALITY_ABSORBED hit=$(scope_hit "$mv" "$SCOPE_KENGAKU") ;;
        kumitate) id=SCOPE_ORCHESTRATION_ABSORBED hit=$(scope_hit "$mv" "$SCOPE_KUMITATE") ;;
      esac
      [[ -n $hit ]] && emit_finding "$id" warn scope \
        "declared=$mk match=$hit route=$prov action=report-never-absorb"
    done
  done <<<"${SEC_BODY[Meta]-}"
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

  # Declared-scope refusal (r12): a ## Meta domain/scope row naming a refused
  # province (kasegi/kengaku/kumitate) drifts; no declaration row = the old
  # bytes exactly.
  if [[ $HAS_META -eq 1 ]]; then
    scope_decl_screen
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

# ---- claims mode: claim-vs-source verification (local files only) ----

json_str() { # LINE KEY -> raw JSON string body on stdout (escapes intact); rc=1 absent
  local line=$1 key=$2
  local re="\"${key}\"[[:space:]]*:[[:space:]]*\"((\\\\.|[^\"\\\\])*)\""
  if [[ $line =~ $re ]]; then
    printf '%s' "${BASH_REMATCH[1]}"
    return 0
  fi
  return 1
}

jfield() { json_str "$1" "$2" 2>/dev/null || true; }

json_unescape() { # RAW JSON string body -> decoded bytes on stdout
  local s=$1 out='' i c hex cp
  local n=${#s}
  for ((i = 0; i < n; i++)); do
    c=${s:i:1}
    if [[ $c != '\' ]]; then out+=$c; continue; fi
    i=$((i + 1)); c=${s:i:1}
    case "$c" in
      '"') out+='"' ;;
      '\') out+='\' ;;
      /) out+='/' ;;
      b) out+=$'\b' ;;
      f) out+=$'\f' ;;
      n) out+=$'\n' ;;
      r) out+=$'\r' ;;
      t) out+=$'\t' ;;
      u)
        hex=''
        if ((i + 4 < n)); then hex=${s:i+1:4}; fi
        if [[ $hex =~ ^[0-9A-Fa-f]{4}$ ]]; then
          cp=$((16#$hex)); i=$((i + 4))
          if ((cp < 0x80)); then
            printf -v c '%b' "\\$(printf '%03o' "$cp")"; out+=$c
          elif ((cp >= 0xD800 && cp <= 0xDFFF)); then
            out+='?'
          elif printf -v c '%b' "\u$hex" 2>/dev/null; then
            out+=$c
          else
            out+='?'
          fi
        else
          out+='\u'
        fi
        ;;
      *) out+='\'; out+=$c ;;
    esac
  done
  printf '%s' "$out"
}

count_nl() { # STRING -> newline count (linear in bytes). The previous
  local n                        # negated-class expansion was quadratic in the
  n=$(printf '%s' "$1" | tr -dc '\n' | wc -c)  # string length — measured
  n=${n//[[:space:]]/}           # >60 s at the 8 MiB source the r12 cap
  printf '%d' "$n"               # admits; tr|wc -c is ~3 ms there.
}

line_probe() { # HAY NEEDLE -> 1-based line of first needle occurrence; rc=1 none
  local hay=$1 needle=$2 before
  [[ -n $needle ]] || return 1
  [[ $hay == *"$needle"* ]] || return 1
  before=${hay%%"$needle"*}
  printf '%d' "$(( $(count_nl "$before") + 1 ))"
}

longest_token() { # STRING -> its longest whitespace-separated token
  local s=$1 t best=''
  local IFS=$' \t'
  for t in $s; do
    if [[ ${#t} -gt ${#best} ]]; then best=$t; fi
  done
  printf '%s' "$best"
}

claim_source_path() { # SRC -> rc 0: CLAIM_SRC_PATH; rc 1: CLAIM_REFUSE + CLAIM_REFUSE_OBS
  local src root_r lane_r cand canon src_root
  src=$(norm_ptr "$1")
  CLAIM_REFUSE=''; CLAIM_REFUSE_OBS=''; CLAIM_SRC_PATH=''
  if is_session_url "$src" || is_denylist_path "$src"; then
    CLAIM_REFUSE=CLAIM_SOURCE_SESSION
    CLAIM_REFUSE_OBS="path=$(ptr_file_part "$src") denied (not opened)"
    return 1
  fi
  if is_ephemeral_ptr "$src"; then
    CLAIM_REFUSE=CLAIM_SOURCE_EPHEMERAL
    CLAIM_REFUSE_OBS="ptr_class=ephemeral"
    return 1
  fi
  if is_url_ptr "$src"; then
    CLAIM_REFUSE=CLAIM_SOURCE_EXTERNAL
    CLAIM_REFUSE_OBS="url source refused (no external fetch)"
    return 1
  fi
  root_r=$(cd -- "$ROOT" 2>/dev/null && pwd -P || printf '%s' "$ROOT")
  lane_r=$(cd -- "$LANE_ROOT" 2>/dev/null && pwd -P || printf '%s' "$LANE_ROOT")
  if [[ $src == /* ]]; then
    cand=$src
  elif [[ -e $ROOT/$src ]]; then
    cand=$ROOT/$src
  elif [[ -e $LANE_ROOT/$src ]]; then
    cand=$LANE_ROOT/$src
  else
    cand=$ROOT/$src
  fi
  canon=$(readlink -f -- "$cand" 2>/dev/null || printf '%s' "$cand")
  # WHICH allowed root resolved the source is kept (src_root): the two roots
  # can sit on different filesystems (a tmpfs corpus root against a disk lane
  # root, or the corpus on a mounted volume), so the device probe below must
  # compare against the resolving root, never a fixed one. Both prefixes
  # match only when one root nests inside the other; the longer (more
  # specific) prefix is the resolving root — a corpus root that is itself a
  # mount refutes nothing: the declared root IS the boundary.
  # r15: in_root normalizes for the PREFIX test only; with --root / the raw
  # "$root_r"/* rendered //* and refused every absolute source OUT_OF_CORPUS.
  # src_root stays un-normalized: the device probe stats the declared root.
  if in_root "$canon" "$lane_r" && in_root "$canon" "$root_r"; then
    if (( ${#lane_r} >= ${#root_r} )); then src_root=$lane_r; else src_root=$root_r; fi
  elif in_root "$canon" "$lane_r"; then
    src_root=$lane_r
  elif in_root "$canon" "$root_r"; then
    src_root=$root_r
  else
    CLAIM_REFUSE=CLAIM_SOURCE_OUT_OF_CORPUS
    CLAIM_REFUSE_OBS="resolved=$canon outside allowed roots"
    return 1
  fi
  if [[ ! -f $canon || ! -r $canon ]]; then
    CLAIM_REFUSE=CLAIM_SOURCE_MISSING
    CLAIM_REFUSE_OBS="not a readable regular file under allowed roots"
    return 1
  fi
  # Probe before the read (r12 cap, r13 alias, r14 device): this single
  # chokepoint serves claims, chain and verify-all's declared-claims
  # resolution, so all three refuse alike. One stat serves all three arms;
  # the order is identity-class (nlink), volume-class (size), then
  # mount-boundary (device) — a combined source reports the earliest class.
  local size nlink dev root_dev
  if read -r size nlink dev < <(stat -c '%s %h %d' -- "$canon" 2>/dev/null); then
    if [[ $nlink =~ ^[0-9]+$ ]] && (( nlink != 1 )); then
      CLAIM_REFUSE=CLAIM_SOURCE_MULTILINKED
      CLAIM_REFUSE_OBS="nlink=$nlink multi-linked source refused (possible hardlink alias of out-of-corpus content; not read)"
      return 1
    fi
    if [[ $size =~ ^[0-9]+$ ]] && (( size > SOURCE_READ_MAX_BYTES )); then
      CLAIM_REFUSE=CLAIM_SOURCE_READ_TOO_LARGE
      CLAIM_REFUSE_OBS="size=$size cap=$SOURCE_READ_MAX_BYTES exceeded (not read)"
      return 1
    fi
    # Device probe (r14): a bind alias keeps its in-root path (readlink -f
    # follows symlinks, never mounts) and its nlink (a bind is not a link),
    # so st_dev is the one identity signal it cannot keep — a source on
    # another filesystem than the resolving root is refused unread. Same-
    # device binds are stat-invisible and stay a named limit
    # (mount-alias-r14.md). A root whose device is unmeasurable fails open
    # here (documented residual): stat(root) needs no permission the file
    # read did not already need.
    if [[ $dev =~ ^[0-9]+$ ]] \
        && root_dev=$(stat -c '%d' -- "$src_root" 2>/dev/null) \
        && [[ $root_dev =~ ^[0-9]+$ ]] && [[ $dev != "$root_dev" ]]; then
      CLAIM_REFUSE=CLAIM_SOURCE_CROSS_DEVICE
      CLAIM_REFUSE_OBS="dev=$dev root_dev=$root_dev root=$src_root cross-device source refused (possible bind alias of out-of-corpus content; not read)"
      return 1
    fi
  elif size=$(file_size_bytes "$canon") && (( size > SOURCE_READ_MAX_BYTES )); then
    # Probe fallback: the alias and device checks need %h/%d and are skipped
    # when stat is unmeasurable (documented residual); the r12 cap semantics
    # hold.
    CLAIM_REFUSE=CLAIM_SOURCE_READ_TOO_LARGE
    CLAIM_REFUSE_OBS="size=$size cap=$SOURCE_READ_MAX_BYTES exceeded (not read)"
    return 1
  fi
  CLAIM_SRC_PATH=$canon
  return 0
}

claim_source_sev() {
  case "$1" in
    CLAIM_SOURCE_EXTERNAL|CLAIM_SOURCE_SESSION|CLAIM_SOURCE_OUT_OF_CORPUS|CLAIM_SOURCE_MULTILINKED|CLAIM_SOURCE_CROSS_DEVICE) printf 'crit' ;;
    *) printf 'warn' ;;
  esac
}

# ---- token-boundary matching (header rule; claims spans and chain quotes) ----
# TOK_WS and TOK_PUNCT are the two boundary character classes; `-` and `'` are
# absent from TOK_PUNCT because they are boundaries only when they do not join
# two word characters. Membership is asked with [[ $SET == *"$c"* ]] so an
# ASCII-only set is matched against a whole (possibly multibyte) character:
# every non-ASCII byte misses both sets and is therefore a word character.

TOK_WS=$' \t\n\r\v\f'
TOK_PUNCT='!"#$%&()*+,./:;<=>?@[\]^_`{|}~'

tok_word_char() { # CHAR -> rc0: word character (ASCII alnum or non-ASCII)
  local c=$1
  [[ -n $c ]] || return 1
  [[ $c == [0-9A-Za-z] ]] && return 0
  [[ $c == - || $c == "'" ]] && return 1
  [[ $TOK_WS == *"$c"* || $TOK_PUNCT == *"$c"* ]] && return 1
  return 0
}

tok_left_ok() { # BEFORE SPAN -> rc0: the left edge is a token boundary
  local before=$1 span=$2 c n=''
  [[ -n $before ]] || return 0                    # start of file / line start
  c=${before: -1}                                 # last character before the hit
  if [[ $c == - || $c == "'" ]]; then
    if [[ ${#before} -ge 2 ]]; then n=${before: -2:1}; fi
    if tok_word_char "$n" && tok_word_char "${span:0:1}"; then
      return 1                                    # word-internal joiner
    fi
    return 0
  fi
  [[ $TOK_WS == *"$c"* || $TOK_PUNCT == *"$c"* ]]
}

tok_right_ok() { # AFTER SPAN -> rc0: the right edge is a token boundary
  local after=$1 span=$2 c n=''
  [[ -n $after ]] || return 0                     # end of file / line end
  c=${after:0:1}                                  # first character after the hit
  if [[ $c == - || $c == "'" ]]; then
    if [[ ${#after} -ge 2 ]]; then n=${after:1:1}; fi
    if tok_word_char "$n" && tok_word_char "${span: -1}"; then
      return 1                                    # word-internal joiner
    fi
    return 0
  fi
  [[ $TOK_WS == *"$c"* || $TOK_PUNCT == *"$c"* ]]
}

tok_span_at() { # HAY SPAN -> TOK_AT (line:N|lines:N-M) + TOK_L1/TOK_L2
  # rc0: first boundary-delimited occurrence; rc1: none. Occurrences that are
  # substrings but glued into a word are skipped, not reported.
  local hay=$1 span=$2 rest=$hay before after dropped=0
  TOK_AT=- TOK_L1=0 TOK_L2=0
  [[ -n $span ]] || return 1
  while :; do
    [[ $rest == *"$span"* ]] || return 1
    before=${rest%%"$span"*}
    after=${rest#*"$span"}
    if tok_left_ok "$before" "$span" && tok_right_ok "$after" "$span"; then
      TOK_L1=$(( dropped + $(count_nl "$before") + 1 ))
      TOK_L2=$(( TOK_L1 + $(count_nl "$span") ))
      if [[ $TOK_L1 -eq $TOK_L2 ]]; then TOK_AT=line:$TOK_L1; else TOK_AT=lines:$TOK_L1-$TOK_L2; fi
      return 0
    fi
    dropped=$(( dropped + $(count_nl "$before") + $(count_nl "$span") ))
    rest=$after
  done
}

verify_claims() {
  local claims=$1
  ROOT=${CHOUSA_ROOT:-$ROOT}
  [[ -n ${claims:-} ]] || die_usage "claims file required (verify-claims PATH or CHOUSA_CLAIMS)"
  [[ -e $claims ]] || die_usage "claims file not found: $claims"
  [[ -f $claims ]] || die_usage "claims file is not a regular file: $claims"
  [[ -r $claims ]] || die_usage "claims file unreadable: $claims"

  FINDING_LINES=(); N_FINDINGS=0; N_DRIFT=0; ROLL=CLEAN

  local N_CLAIMS=0 N_SUP=0 N_CON=0 N_UNS=0 N_UNP=0 N_MISM=0 N_REFUSED=0 N_INVALID=0
  local default_marker='' lineno=0 line CLAIM_REFUSE='' CLAIM_REFUSE_OBS='' CLAIM_SRC_PATH=''
  local -a CLAIM_LINES=()
  local id src span expect marker observed verdict at bad l
  local hay start_line end_line region m probe nearer tok ctx path show_id show_exp

  scan_secrets "$claims"

  while IFS= read -r line || [[ -n $line ]]; do
    lineno=$((lineno + 1))
    [[ -z ${line//[[:space:]]/} ]] && continue
    [[ $line == \#* ]] && continue
    while [[ $line == [[:space:]]* ]]; do line=${line#?}; done
    while [[ $line == *[[:space:]] ]]; do line=${line%?}; done
    if [[ $line != \{*\} ]]; then
      N_CLAIMS=$((N_CLAIMS + 1)); N_INVALID=$((N_INVALID + 1))
      emit_finding CLAIM_RECORD_INVALID warn claims "line=$lineno not a JSON object"
      CLAIM_LINES+=("CLAIM id=line$lineno expected=- observed=invalid source=- at=- verdict=invalid")
      continue
    fi
    if ! json_str "$line" id >/dev/null 2>&1 && json_str "$line" marker_default >/dev/null 2>&1; then
      default_marker=$(json_unescape "$(jfield "$line" marker_default)")
      continue
    fi
    N_CLAIMS=$((N_CLAIMS + 1))

    id=$(json_unescape "$(jfield "$line" id)")
    src=$(json_unescape "$(jfield "$line" source)")
    span=$(json_unescape "$(jfield "$line" span)"; printf x); span=${span%x}
    expect=$(json_unescape "$(jfield "$line" expect)")
    marker=$(json_unescape "$(jfield "$line" marker)")
    bad=''
    if [[ -z $id ]]; then bad="missing id"
    elif [[ -z $src ]]; then bad="missing source"
    elif [[ -z $span ]]; then bad="missing/empty span"
    elif [[ -z $expect ]]; then bad="missing expect"
    else
      case "$expect" in
        supported|contradicted|unsupported) ;;
        *) bad="expect=$expect invalid" ;;
      esac
      if [[ -z $bad && $expect != contradicted && -n $marker ]]; then
        bad="marker present but expect=$expect (fixture violation)"
      fi
    fi
    if [[ -n $bad ]]; then
      N_INVALID=$((N_INVALID + 1))
      show_id=${id:-line$lineno}; show_exp=${expect:--}
      emit_finding CLAIM_RECORD_INVALID warn claims "line=$lineno $bad"
      CLAIM_LINES+=("CLAIM id=$show_id expected=$show_exp observed=invalid source=${src:--} at=- verdict=invalid")
      continue
    fi

    if ! claim_source_path "$src"; then
      N_REFUSED=$((N_REFUSED + 1))
      emit_finding "$CLAIM_REFUSE" "$(claim_source_sev "$CLAIM_REFUSE")" claims \
        "id=$id source=$src obs=$CLAIM_REFUSE_OBS"
      CLAIM_LINES+=("CLAIM id=$id expected=$expect observed=refused source=$src at=- verdict=refused")
      continue
    fi
    path=$CLAIM_SRC_PATH

    hay=$(cat -- "$path"; printf x)
    hay=${hay%x}
    if tok_span_at "$hay" "$span"; then
      start_line=$TOK_L1
      end_line=$TOK_L2
      at=$TOK_AT
      case "$expect" in
        supported) observed=supported ;;
        unsupported)
          observed=supported
          emit_finding CLAIM_SPAN_UNEXPECTED warn claims "id=$id at=$at span present but expect=unsupported"
          ;;
        contradicted)
          region=$(printf '%s\n' "$hay" | sed -n "${start_line},${end_line}p")
          m=${marker:-$default_marker}
          if [[ -z $m ]]; then
            observed=unproven
            emit_finding CONTRADICTION_MARKER_ABSENT warn claims "id=$id at=$at no marker defined (per-claim or marker_default)"
          elif [[ $region == *"$m"* ]]; then
            observed=contradicted
          else
            observed=unproven
            emit_finding CONTRADICTION_MARKER_ABSENT warn claims "id=$id at=$at declared marker not found within span lines"
          fi
          ;;
      esac
    else
      at=-
      case "$expect" in
        supported|contradicted)
          observed=unsupported
          nearer=''; ctx=''
          probe=${span%%$'\n'*}
          nearer=$(line_probe "$hay" "$probe" || true)
          if [[ -z $nearer ]]; then
            tok=$(longest_token "$probe")
            if [[ -n $tok ]]; then
              nearer=$(printf '%s\n' "$hay" | grep -Fn -m1 -e "$tok" | head -n1 | cut -d: -f1 || true)
            fi
          fi
          if [[ -n $nearer ]]; then
            ctx=$(printf '%s\n' "$hay" | sed -n "${nearer}p" | tr '\t' ' ')
            ctx=$(printf '%.80s' "$ctx")
          fi
          emit_finding CLAIM_SPAN_NOT_FOUND warn claims "id=$id nearest_line=${nearer:--} context=${ctx:--}"
          ;;
        unsupported) observed=unsupported ;;
      esac
    fi

    case "$observed" in
      supported) N_SUP=$((N_SUP + 1)) ;;
      contradicted) N_CON=$((N_CON + 1)) ;;
      unsupported) N_UNS=$((N_UNS + 1)) ;;
      unproven) N_UNP=$((N_UNP + 1)) ;;
    esac
    if [[ $observed == "$expect" ]]; then
      verdict=match
    else
      N_MISM=$((N_MISM + 1)); verdict=mismatch
    fi
    CLAIM_LINES+=("CLAIM id=$id expected=$expect observed=$observed source=$src at=$at verdict=$verdict")
  done <"$claims"

  printf 'research-gate %s — ts=%s — mode=claims — claims=%s\n' "$VERSION" "$TS_UTC" "$claims"
  for l in "${CLAIM_LINES[@]+"${CLAIM_LINES[@]}"}"; do printf '%s\n' "$l"; done
  for l in "${FINDING_LINES[@]+"${FINDING_LINES[@]}"}"; do printf '%s\n' "$l"; done
  local N_MATCH=$((N_CLAIMS - N_MISM - N_REFUSED - N_INVALID))
  if [[ $N_MATCH -ne $N_CLAIMS ]]; then ROLL=DRIFT; fi
  printf 'VERDICT_BEARING_CLAIMS=%d/%d\n' "$N_MATCH" "$N_CLAIMS"
  printf 'RESEARCH_GATE: %s (claims=%d supported=%d contradicted=%d unsupported=%d mismatched=%d unproven=%d refused=%d invalid=%d findings=%d drift=%d)\n' \
    "$ROLL" "$N_CLAIMS" "$N_SUP" "$N_CON" "$N_UNS" "$N_MISM" "$N_UNP" "$N_REFUSED" "$N_INVALID" "$N_FINDINGS" "$N_DRIFT"

  [[ $ROLL == CLEAN ]] && return 0
  return 1
}

# ---- chain mode: hop-citation resolution (local files only) ----

chain_cell() { # ROW KEY... -> first non-empty cell value ('' if none)
  local row=$1 k v
  shift
  for k in "$@"; do
    v=$(cell "$row" "$k")
    if [[ -n $v ]]; then printf '%s' "$v"; return 0; fi
  done
  printf ''
  return 0
}

chain_disp() { # STRING -> at most 80 chars, '-' when empty
  local v=${1:-}
  v=$(printf '%.80s' "$v")
  [[ -n $v ]] || v=-
  printf '%s' "$v"
}

chain_citation() { # ROW -> rc0: CITE_TO CITE_KIND CITE_TEXT; rc1: CITE_ERR
  local row=$1 to ack ak atext frag fk kind_claim=''
  CITE_TO='' CITE_KIND='' CITE_TEXT='' CITE_ERR=''
  to=$(norm_ptr "$(chain_cell "$row" to)")
  ack=$(chain_cell "$row" anchor_kind kind)
  ak=$(printf '%s' "$ack" | tr 'A-Z' 'a-z')
  atext=$(chain_cell "$row" anchor anchor_text span fragment locator)
  if [[ -n $atext && $atext == *:* ]]; then
    fk=$(printf '%s' "${atext%%:*}" | tr 'A-Z' 'a-z')
    case "$fk" in
      heading|quote|line) kind_claim=$fk; atext=${atext#*:} ;;
    esac
  fi
  if [[ $to == *'#'* ]]; then
    frag=${to#*#}; to=${to%%#*}
    [[ -n $atext ]] && { CITE_ERR="both anchor column and to#fragment present"; return 1; }
    fk=''
    if [[ $frag == *:* ]]; then
      fk=$(printf '%s' "${frag%%:*}" | tr 'A-Z' 'a-z')
      case "$fk" in heading|quote|line) ;; *) fk='' ;; esac
    fi
    if [[ -n $fk ]]; then
      kind_claim=$fk; atext=${frag#*:}
    else
      atext=$frag
      [[ -z $ak ]] && kind_claim=heading
    fi
  fi
  [[ -n $to ]] || { CITE_ERR="resolved hop missing source"; return 1; }
  [[ -n $atext ]] || { CITE_ERR="resolved hop missing anchor"; return 1; }
  if [[ -n $ak && -n $kind_claim && $ak != "$kind_claim" ]]; then
    CITE_ERR="anchor_kind=$ack conflicts with anchor kind prefix=$kind_claim"
    return 1
  fi
  case "$ak" in
    '') ak=${kind_claim:-quote} ;;
    heading|quote|line) ;;
    *) CITE_ERR="anchor_kind=$ack not in heading|quote|line"; return 1 ;;
  esac
  CITE_TO=$to CITE_KIND=$ak CITE_TEXT=$atext
  return 0
}

chain_anchor_at() { # HAY KIND TEXT -> CITE_AT; rc0 found / rc1 not found
  local hay=$1 kind=$2 text=$3 line tline lineno=0
  CITE_AT=-
  case "$kind" in
    heading)
      while IFS= read -r line || [[ -n $line ]]; do
        lineno=$((lineno + 1))
        [[ $line =~ ^#+[[:space:]]+(.*)$ ]] || continue
        tline=${BASH_REMATCH[1]}
        while [[ $tline == *[[:space:]] ]]; do tline=${tline%?}; done
        if [[ $tline == "$text" ]]; then CITE_AT=line:$lineno; return 0; fi
      done <<<"$hay"
      return 1
      ;;
    quote)
      tok_span_at "$hay" "$text" || return 1
      CITE_AT=$TOK_AT
      return 0
      ;;
    line)
      while IFS= read -r line || [[ -n $line ]]; do
        lineno=$((lineno + 1))
        tline=$line
        while [[ $tline == *[[:space:]] ]]; do tline=${tline%?}; done
        if [[ $tline == "$text" ]]; then CITE_AT=line:$lineno; return 0; fi
      done <<<"$hay"
      return 1
      ;;
  esac
  return 1
}

chain_nearest() { # HAY TEXT -> CHAIN_NEAREST CHAIN_CTX (quote-style probes)
  local hay=$1 text=$2 probe tok nearer ctx
  probe=${text%%$'\n'*}
  nearer=$(line_probe "$hay" "$probe" || true)
  if [[ -z $nearer ]]; then
    tok=$(longest_token "$probe")
    if [[ -n $tok ]]; then
      nearer=$(printf '%s\n' "$hay" | grep -Fn -m1 -e "$tok" | head -n1 | cut -d: -f1 || true)
    fi
  fi
  ctx=''
  if [[ -n $nearer ]]; then
    ctx=$(printf '%s\n' "$hay" | sed -n "${nearer}p" | tr '\t' ' ')
    ctx=$(printf '%.80s' "$ctx")
  fi
  CHAIN_NEAREST=${nearer:--}
  CHAIN_CTX=${ctx:--}
  return 0
}

chain_ref_file() { # REF -> file part; URL/session/ephemeral forms pass untouched
  local ref=$1
  if is_url_ptr "$ref" || is_ephemeral_ptr "$ref" || is_session_url "$ref" || is_denylist_path "$ref"; then
    printf '%s' "$ref"
  else
    printf '%s' "$(ptr_file_part "$ref")"
  fi
}

chain_refuse_id() { # CLAIM_* refusal -> CHAIN_* finding id
  case "$1" in
    CLAIM_SOURCE_EXTERNAL) printf 'CHAIN_SOURCE_EXTERNAL' ;;
    CLAIM_SOURCE_SESSION) printf 'CHAIN_SOURCE_SESSION' ;;
    CLAIM_SOURCE_EPHEMERAL) printf 'CHAIN_SOURCE_EPHEMERAL' ;;
    CLAIM_SOURCE_OUT_OF_CORPUS) printf 'CHAIN_SOURCE_OUT_OF_CORPUS' ;;
    CLAIM_SOURCE_READ_TOO_LARGE) printf 'CHAIN_SOURCE_READ_TOO_LARGE' ;;
    CLAIM_SOURCE_MULTILINKED) printf 'CHAIN_SOURCE_MULTILINKED' ;;
    CLAIM_SOURCE_CROSS_DEVICE) printf 'CHAIN_SOURCE_CROSS_DEVICE' ;;
    *) printf 'CHAIN_SOURCE_MISSING' ;;
  esac
}

chain_source_sev() {
  case "$1" in
    CHAIN_SOURCE_EXTERNAL|CHAIN_SOURCE_SESSION|CHAIN_SOURCE_OUT_OF_CORPUS|CHAIN_SOURCE_MULTILINKED|CHAIN_SOURCE_CROSS_DEVICE) printf 'crit' ;;
    *) printf 'warn' ;;
  esac
}

verify_chain() {
  local record=$1
  ROOT=${CHOUSA_ROOT:-$ROOT}
  [[ -n ${record:-} ]] || die_usage "record path required (verify-chain RECORD, --record, or CHOUSA_RECORD)"
  [[ -e $record ]] || die_usage "record not found: $record"
  [[ -f $record ]] || die_usage "record is not a regular file: $record"
  [[ -r $record ]] || die_usage "record unreadable: $record"

  FINDING_LINES=(); N_FINDINGS=0; N_DRIFT=0; ROLL=CLEAN
  scan_secrets "$record"
  load_sections "$record"

  local N_HOPS=0 N_VER=0 N_EXEMPT=0 N_MISM=0 N_REFUSED=0 N_INVALID=0
  local -a CHAIN_LINES=()
  declare -g -A SRC_PTR=()
  local srow sid sptr
  if [[ -n ${SEC_BODY[Sources]+x} ]]; then
    while IFS= read -r srow; do
      [[ -z $srow ]] && continue
      sid=$(cell "$srow" id)
      [[ -z $sid ]] && continue
      sptr=$(cell "$srow" pointer)
      SRC_PTR[$sid]=$sptr
    done < <(table_rows Sources)
  fi

  if [[ -z ${SEC_BODY[Chain]+x} ]]; then
    emit_finding CHAIN_ABSENT warn chain "missing ## Chain section"
  fi

  local hrow hop st to ref disp path hay obs at verdict l
  local CITE_TO='' CITE_KIND='' CITE_TEXT='' CITE_ERR=''
  local CITE_AT='' CHAIN_NEAREST='' CHAIN_CTX=''
  local CLAIM_REFUSE='' CLAIM_REFUSE_OBS='' CLAIM_SRC_PATH=''
  if [[ -n ${SEC_BODY[Chain]+x} ]]; then
    while IFS= read -r hrow; do
      [[ -z $hrow ]] && continue
      N_HOPS=$((N_HOPS + 1))
      hop=$(cell "$hrow" hop); [[ -z $hop ]] && hop="H$N_HOPS"
      st=$(cell "$hrow" status | tr 'A-Z' 'a-z')
      case "$st" in
        resolved)
          to=$(norm_ptr "$(chain_cell "$hrow" to)")
          disp=$(chain_disp "$to")
          if ! chain_citation "$hrow"; then
            N_INVALID=$((N_INVALID + 1))
            emit_finding CHAIN_CITATION_INVALID warn chain "hop=$hop status=resolved $CITE_ERR"
            CHAIN_LINES+=("CHAIN hop=$hop status=resolved observed=invalid source=$disp anchor=- at=- verdict=invalid")
            continue
          fi
          to=$CITE_TO
          if [[ -n ${SRC_PTR[$to]+x} ]]; then
            if [[ -z ${SRC_PTR[$to]} ]]; then
              N_REFUSED=$((N_REFUSED + 1))
              emit_finding CHAIN_SOURCE_MISSING warn chain "hop=$hop to=$to source row has no pointer"
              CHAIN_LINES+=("CHAIN hop=$hop status=resolved observed=refused source=$to anchor=- at=- verdict=refused")
              continue
            fi
            ref=${SRC_PTR[$to]}
          elif [[ $to =~ ^S[A-Za-z0-9_-]+$ ]]; then
            N_REFUSED=$((N_REFUSED + 1))
            emit_finding CHAIN_SOURCE_MISSING warn chain "hop=$hop to=$to source_id not in ## Sources"
            CHAIN_LINES+=("CHAIN hop=$hop status=resolved observed=refused source=$to anchor=- at=- verdict=refused")
            continue
          else
            ref=$to
          fi
          ref=$(chain_ref_file "$ref")
          if ! claim_source_path "$ref"; then
            N_REFUSED=$((N_REFUSED + 1))
            local rid; rid=$(chain_refuse_id "$CLAIM_REFUSE")
            emit_finding "$rid" "$(chain_source_sev "$rid")" chain \
              "hop=$hop source=$(chain_disp "$ref") obs=$CLAIM_REFUSE_OBS"
            CHAIN_LINES+=("CHAIN hop=$hop status=resolved observed=refused source=$(chain_disp "$ref") anchor=- at=- verdict=refused")
            continue
          fi
          path=$CLAIM_SRC_PATH
          disp=$(chain_disp "$ref")
          hay=$(cat -- "$path"; printf x)
          hay=${hay%x}
          CITE_AT='-'; CHAIN_NEAREST='-'; CHAIN_CTX='-'
          if chain_anchor_at "$hay" "$CITE_KIND" "$CITE_TEXT"; then
            N_VER=$((N_VER + 1)); obs=verified; verdict=match
          else
            N_MISM=$((N_MISM + 1)); obs=anchor-missing; verdict=mismatch
            if [[ $CITE_KIND == quote ]]; then
              chain_nearest "$hay" "$CITE_TEXT"
            fi
            emit_finding CHAIN_ANCHOR_NOT_FOUND warn chain \
              "hop=$hop source=$disp anchor=$CITE_KIND:\"$(printf '%.60s' "$CITE_TEXT")\" nearest_line=$CHAIN_NEAREST context=$CHAIN_CTX"
          fi
          CHAIN_LINES+=("CHAIN hop=$hop status=resolved observed=$obs source=$disp anchor=$CITE_KIND:\"$(printf '%.60s' "$CITE_TEXT")\" at=$CITE_AT verdict=$verdict")
          ;;
        unresolved|blocked-no-fetch|rejected|labelled-dead|not-applicable)
          N_EXEMPT=$((N_EXEMPT + 1))
          CHAIN_LINES+=("CHAIN hop=$hop status=$st observed=exempt source=$(chain_disp "$(norm_ptr "$(chain_cell "$hrow" to)")") anchor=- at=- verdict=exempt")
          ;;
        "")
          N_INVALID=$((N_INVALID + 1))
          emit_finding CHAIN_CITATION_INVALID warn chain "hop=$hop missing status"
          CHAIN_LINES+=("CHAIN hop=$hop status=- observed=invalid source=- anchor=- at=- verdict=invalid")
          ;;
        *)
          N_INVALID=$((N_INVALID + 1))
          emit_finding CHAIN_CITATION_INVALID warn chain "hop=$hop status=$st not in allowed set"
          CHAIN_LINES+=("CHAIN hop=$hop status=$st observed=invalid source=- anchor=- at=- verdict=invalid")
          ;;
      esac
    done < <(table_rows Chain)
    if [[ $N_HOPS -eq 0 ]]; then
      emit_finding CHAIN_ABSENT warn chain "no chain hop rows to verify"
    fi
  fi

  printf 'research-gate %s — ts=%s — mode=chain — record=%s\n' "$VERSION" "$TS_UTC" "$record"
  for l in "${CHAIN_LINES[@]+"${CHAIN_LINES[@]}"}"; do printf '%s\n' "$l"; done
  for l in "${FINDING_LINES[@]+"${FINDING_LINES[@]}"}"; do printf '%s\n' "$l"; done
  if [[ $((N_VER + N_EXEMPT)) -ne $N_HOPS ]]; then ROLL=DRIFT; fi
  printf 'RESOLVED_HOPS=%d/%d\n' "$N_VER" "$N_HOPS"
  printf 'RESEARCH_GATE: %s (hops=%d verified=%d exempt=%d anchor-missing=%d refused=%d invalid=%d findings=%d drift=%d)\n' \
    "$ROLL" "$N_HOPS" "$N_VER" "$N_EXEMPT" "$N_MISM" "$N_REFUSED" "$N_INVALID" "$N_FINDINGS" "$N_DRIFT"

  [[ $ROLL == CLEAN ]] && return 0
  return 1
}

# ---- sweeps mode: kept rejections + negative sweeps (local re-runs only) ----

sweep_has_bad_char() { # TOKEN -> rc0: carries a byte a path token cannot name
  local t=$1 c i
  local bad=$' \t`$"\'(){}<>|&\\;,#!'
  for ((i = 0; i < ${#t}; i++)); do
    c=${t:i:1}
    [[ $bad == *"$c"* ]] && return 0
  done
  return 1
}

sweep_looks_path() { # TOKEN -> rc0: path- or glob-shaped naming
  local t=$1
  [[ -n $t ]] || return 1
  sweep_has_bad_char "$t" && return 1
  [[ $t == */* || $t == *'*'* || $t == *'?'* ]] && return 0
  [[ $t =~ \.[A-Za-z0-9]+$ ]] && return 0
  return 1
}

sweep_token_class() { # TOKEN -> local|nonlocal|sourceid|junk on stdout
  local t=$1
  [[ -n $t ]] || { printf 'junk'; return 0; }
  if is_url_ptr "$t" || is_ephemeral_ptr "$t"; then printf 'nonlocal'; return 0; fi
  case "$t" in
    external|external:*|web|web:*|live|live:*|chat|chat:*|session|session:*|non-local|nonlocal)
      printf 'nonlocal'; return 0 ;;
  esac
  if sweep_looks_path "$t"; then printf 'local'; return 0; fi
  if [[ $t =~ ^S[A-Za-z0-9_-]+$ ]]; then printf 'sourceid'; return 0; fi
  printf 'junk'
}

sweep_trim_token() { # TOKEN -> edge quotations / trailing punctuation stripped
  local t=$1 guard=0
  while [[ $t == [[:space:]]* ]]; do t=${t#?}; done
  while [[ $t == *[[:space:]] ]]; do t=${t%?}; done
  while :; do
    guard=$((guard + 1)); [[ $guard -gt 8 ]] && break
    if [[ $t == \`*\` && ${#t} -ge 2 ]]; then t=${t#?}; t=${t%?}; continue; fi
    if [[ $t == '"'*'"' && ${#t} -ge 2 ]]; then t=${t#?}; t=${t%?}; continue; fi
    if [[ $t == "'"*"'" && ${#t} -ge 2 ]]; then t=${t#?}; t=${t%?}; continue; fi
    if [[ $t == *')' || $t == *',' || $t == *';' ]]; then t=${t%?}; continue; fi
    break
  done
  printf '%s' "$t"
}

sweep_where_tokens() { # RAW -> location tokens, one per line; empty = unnamed
  local raw=$1 tok
  raw=$(sweep_trim_token "$raw")
  [[ -n $raw ]] || return 0
  local -a out=() words=()
  if [[ $raw == *[[:space:]]* ]]; then
    # command/description form: keep only structured words, ignore the rest
    read -r -a words <<<"$raw"
    for tok in "${words[@]+"${words[@]}"}"; do
      tok=$(sweep_trim_token "$tok")
      [[ -n $tok ]] || continue
      [[ $(sweep_token_class "$tok") == junk ]] && continue
      out+=("$tok")
    done
  else
    # whitespace-free form: a comma/semicolon-separated path set (no globbing)
    set -f
    local IFS=',;'
    for tok in $raw; do
      tok=$(sweep_trim_token "$tok")
      [[ -n $tok ]] && out+=("$tok")
    done
    set +f
  fi
  for tok in "${out[@]+"${out[@]}"}"; do printf '%s\n' "$tok"; done
}

sweep_row_cell_scan() { # ROW ERE -> first cell whose key matches ERE ('' if none)
  local row=$1 re=$2 e k v
  local -a ents=()
  local IFS=$'\t'
  read -r -a ents <<<"$row"
  for e in "${ents[@]+"${ents[@]}"}"; do
    [[ $e == *'='* ]] || continue
    k=${e%%=*}; v=${e#*=}
    if [[ ${k,,} =~ $re ]]; then printf '%s' "$v"; return 0; fi
  done
  printf ''
  return 0
}

sweep_flip_cell() { # ROW -> flip-condition cell ('' when none)
  local v
  v=$(chain_cell "$1" flip flip_condition flip-condition flipcondition would_flip \
    wouldflip falsifier flip_when flipwhen flip_if flipif flips_if flipsif)
  [[ -n $v ]] || v=$(sweep_row_cell_scan "$1" 'flip|falsif|reversal|counter')
  printf '%s' "$v"
}

sweep_raw_where() { # ROW -> raw named-location string ('' when none)
  local v
  v=$(chain_cell "$1" where looked_at "looked at" looked scope searched paths \
    location targets)
  [[ -n $v ]] || v=$(sweep_row_cell_scan "$1" 'where|looked|scope|glob|target|locat')
  [[ -n $v ]] || v=$(cell "$1" sweep)
  printf '%s' "$v"
}

sweep_path_guarded() { # PATTERN -> rc0: glob-safe under an allowed root; rc1 refuse
  local pat=$1 dir base canon comp c i
  local root_r lane_r
  root_r=$(cd -- "$ROOT" 2>/dev/null && pwd -P || printf '%s' "$ROOT")
  lane_r=$(cd -- "$LANE_ROOT" 2>/dev/null && pwd -P || printf '%s' "$LANE_ROOT")
  local -a comps=()
  local IFS='/'
  read -r -a comps <<<"$pat"
  for comp in "${comps[@]+"${comps[@]}"}"; do
    [[ $comp == .. ]] && return 1
  done
  dir=${pat%/*}
  [[ $dir == "$pat" ]] && dir=.
  for ((i = 0; i < ${#dir}; i++)); do
    c=${dir:i:1}
    if [[ $c == '*' || $c == '?' || $c == '[' ]]; then dir=${dir:0:i}; break; fi
  done
  dir=${dir%/}
  if [[ -z $dir ]]; then
    if [[ $pat == /* ]]; then dir=/; else dir=.; fi
  fi
  if [[ $dir == /* ]]; then base=$dir; else base="$ROOT/$dir"; fi
  if [[ -e $base ]]; then
    canon=$(readlink -f -- "$base" 2>/dev/null || printf '%s' "$base")
  elif command -v realpath >/dev/null 2>&1; then
    canon=$(realpath -m -- "$base" 2>/dev/null || printf '%s' "$base")
  else
    canon=$(readlink -f -- "$base" 2>/dev/null || printf '%s' "$base")
  fi
  # r15: same dead-arm class (raw case rendered // and //* with --root /,
  # refusing every absolute sweep location); in_root normalizes the prefix.
  if in_root "$canon" "$root_r" || in_root "$canon" "$lane_r"; then return 0; fi
  return 1
}

sweep_glob_matches() { # PATTERN -> matching paths, one per line ('' when none)
  local pat=$1 m
  (
    cd -- "$ROOT" 2>/dev/null || exit 1
    # nullglob only nulls words that carry a glob character: a literal path is
    # echoed back even when nothing is there, so literals take an existence
    # test instead (measured: `for m in lib/ghost.md` printed the pattern and
    # made every literal path a phantom hit).
    if [[ $pat == *'*'* || $pat == *'?'* || $pat == *'['* ]]; then
      shopt -s nullglob globstar
      for m in $pat; do
        [[ $m == . || $m == .. ]] && continue
        printf '%s\n' "$m"
      done
    elif [[ -e $pat || -L $pat ]]; then
      printf '%s\n' "$pat"
    fi
  )
}

verify_sweeps() {
  local record=$1
  ROOT=${CHOUSA_ROOT:-$ROOT}
  [[ -n ${record:-} ]] || die_usage "record path required (verify-sweeps RECORD, --record, or CHOUSA_RECORD)"
  [[ -e $record ]] || die_usage "record not found: $record"
  [[ -f $record ]] || die_usage "record is not a regular file: $record"
  [[ -r $record ]] || die_usage "record unreadable: $record"
  [[ -d $ROOT ]] || die_usage "root is not a directory: $ROOT (--root)"

  FINDING_LINES=(); N_FINDINGS=0; N_DRIFT=0; ROLL=CLEAN
  scan_secrets "$record"
  load_sections "$record"

  declare -g -A SRC_PTR=()
  local srow sid sptr
  if [[ -n ${SEC_BODY[Sources]+x} ]]; then
    while IFS= read -r srow; do
      [[ -z $srow ]] && continue
      sid=$(cell "$srow" id)
      [[ -z $sid ]] && continue
      sptr=$(cell "$srow" pointer)
      SRC_PTR[$sid]=$sptr
    done < <(table_rows Sources)
  fi

  local N_SW=0 N_SW_VER=0 N_SW_EX=0 N_SW_HIT=0 N_SW_REF=0 N_SW_INV=0
  local N_REJ=0 N_REJ_OK=0
  local -a SWEEP_LINES=() REJECTION_LINES=() SWEEP_ROWS=()
  local -a tokens=() local_pats=() sid_toks=() hit_list=()
  local rrow rid rref rreason rflip rp fp miss row nrow rawloc tok cls whr looked st
  local hits first p m i2 listed l
  local have_local have_nonlocal have_sid have_junk refused

  if [[ -n ${SEC_BODY[Rejections]+x} ]]; then
    while IFS= read -r rrow; do
      [[ -z $rrow ]] && continue
      N_REJ=$((N_REJ + 1))
      rid=$(cell "$rrow" id); [[ -z $rid ]] && rid="R$N_REJ"
      rref=$(cell "$rrow" ref)
      rreason=$(cell "$rrow" reason)
      rflip=$(sweep_flip_cell "$rrow")
      if [[ -n $rreason ]]; then rp=present; else rp=absent; fi
      if [[ -n $rflip ]]; then fp=present; else fp=absent; fi
      miss=''
      [[ $rp == absent ]] && miss=reason
      [[ $fp == absent ]] && miss="${miss:+$miss,}flip"
      if [[ -z $miss ]]; then
        N_REJ_OK=$((N_REJ_OK + 1))
        REJECTION_LINES+=("REJECTION id=$rid ref=$(chain_disp "$rref") reason=present flip=present observed=complete verdict=match")
      else
        emit_finding SWEEP_REJECTION_INCOMPLETE warn sweeps "id=$rid missing=$miss"
        REJECTION_LINES+=("REJECTION id=$rid ref=$(chain_disp "$rref") reason=$rp flip=$fp observed=incomplete verdict=mismatch")
      fi
    done < <(table_rows Rejections)
  fi

  if [[ -n ${SEC_BODY[Sweeps]+x} ]]; then
    while IFS= read -r row; do
      [[ -z $row ]] && continue
      SWEEP_ROWS+=("$row")
    done < <(table_rows Sweeps)
  fi
  if [[ ${#SWEEP_ROWS[@]} -eq 0 && -n ${SEC_BODY[Negatives]+x} ]]; then
    while IFS= read -r nrow; do
      [[ -z $nrow ]] && continue
      rawloc=$(sweep_raw_where "$nrow")
      [[ -z $rawloc ]] && continue
      SWEEP_ROWS+=("$nrow")
    done < <(table_rows Negatives)
  fi

  for row in "${SWEEP_ROWS[@]+"${SWEEP_ROWS[@]}"}"; do
    N_SW=$((N_SW + 1))
    sid=$(cell "$row" id); [[ -z $sid ]] && sid="SW$N_SW"
    whr=$(sweep_raw_where "$row")
    st=$(cell "$row" status | tr 'A-Z' 'a-z')
    case "$st" in
      unresolved|blocked-no-fetch|labelled-dead|not-applicable)
        N_SW_EX=$((N_SW_EX + 1))
        SWEEP_LINES+=("SWEEP id=$sid where=$(chain_disp "$whr") looked=exempt hits=- at=- observed=exempt verdict=exempt")
        continue ;;
    esac
    tokens=()
    while IFS= read -r tok; do tokens+=("$tok"); done < <(sweep_where_tokens "$whr")
    if [[ ${#tokens[@]} -eq 0 ]]; then
      N_SW_INV=$((N_SW_INV + 1))
      emit_finding SWEEP_LOCATION_ABSENT warn sweeps "id=$sid no location named"
      SWEEP_LINES+=("SWEEP id=$sid where=$(chain_disp "$whr") looked=unnamed hits=- at=- observed=invalid verdict=invalid")
      continue
    fi
    # Display the location set the gate actually used, not the raw cell: for a
    # command-form cell that is the extracted token list.
    whr=$(printf '%s,' "${tokens[@]}"); whr=${whr%,}
    have_local=0 have_nonlocal=0 have_sid=0 have_junk=0
    local_pats=(); sid_toks=()
    for tok in "${tokens[@]}"; do
      cls=$(sweep_token_class "$tok")
      case "$cls" in
        local) have_local=1; local_pats+=("$tok") ;;
        nonlocal) have_nonlocal=1 ;;
        sourceid) have_sid=1; sid_toks+=("$tok") ;;
        *) have_junk=1 ;;
      esac
    done
    looked=unnamed
    if [[ $have_local -eq 1 ]]; then looked=local
    elif [[ $have_sid -eq 1 ]]; then looked=source-ids
    elif [[ $have_nonlocal -eq 1 ]]; then looked=non-local
    fi
    if [[ $have_junk -eq 1 ]]; then
      N_SW_INV=$((N_SW_INV + 1))
      emit_finding SWEEP_LOCATION_ABSENT warn sweeps "id=$sid unclassifiable location naming"
      SWEEP_LINES+=("SWEEP id=$sid where=$(chain_disp "$whr") looked=$looked hits=- at=- observed=invalid verdict=invalid")
      continue
    fi
    refused=0
    for p in "${local_pats[@]+"${local_pats[@]}"}"; do
      if ! sweep_path_guarded "$p"; then
        refused=1
        emit_finding SWEEP_LOCATION_OUT_OF_CORPUS crit sweeps "id=$sid path=$(chain_disp "$p") refused unopened"
      fi
    done
    for tok in "${sid_toks[@]+"${sid_toks[@]}"}"; do
      if [[ -z ${SRC_PTR[$tok]+x} ]]; then
        refused=1
        emit_finding SWEEP_LOCATION_UNRESOLVED warn sweeps "id=$sid source_id=$tok not in ## Sources"
      fi
    done
    if [[ $refused -eq 1 ]]; then
      N_SW_REF=$((N_SW_REF + 1))
      SWEEP_LINES+=("SWEEP id=$sid where=$(chain_disp "$whr") looked=$looked hits=- at=- observed=refused verdict=refused")
      continue
    fi
    if [[ $have_local -eq 1 ]]; then
      hit_list=()
      for p in "${local_pats[@]+"${local_pats[@]}"}"; do
        while IFS= read -r m; do hit_list+=("$m"); done < <(sweep_glob_matches "$p")
      done
      hits=${#hit_list[@]}
      first=-
      [[ $hits -gt 0 ]] && first=${hit_list[0]}
      if [[ $hits -gt 0 ]]; then
        N_SW_HIT=$((N_SW_HIT + 1))
        listed=''
        for ((i2 = 0; i2 < hits && i2 < 5; i2++)); do listed+="${hit_list[$i2]} "; done
        emit_finding SWEEP_CLAIM_FALSE warn sweeps "id=$sid where=$(chain_disp "$whr") hits=$hits first=$first listed=${listed% }"
        SWEEP_LINES+=("SWEEP id=$sid where=$(chain_disp "$whr") looked=local hits=$hits at=$first observed=hit verdict=mismatch")
      else
        N_SW_VER=$((N_SW_VER + 1))
        SWEEP_LINES+=("SWEEP id=$sid where=$(chain_disp "$whr") looked=local hits=0 at=- observed=verified verdict=match")
      fi
      continue
    fi
    N_SW_EX=$((N_SW_EX + 1))
    SWEEP_LINES+=("SWEEP id=$sid where=$(chain_disp "$whr") looked=$looked hits=- at=- observed=exempt verdict=exempt")
  done

  printf 'research-gate %s — ts=%s — mode=sweeps — record=%s\n' "$VERSION" "$TS_UTC" "$record"
  for l in "${SWEEP_LINES[@]+"${SWEEP_LINES[@]}"}"; do printf '%s\n' "$l"; done
  for l in "${REJECTION_LINES[@]+"${REJECTION_LINES[@]}"}"; do printf '%s\n' "$l"; done
  for l in "${FINDING_LINES[@]+"${FINDING_LINES[@]}"}"; do printf '%s\n' "$l"; done
  if [[ $((N_SW_VER + N_SW_EX)) -ne $N_SW || $N_REJ_OK -ne $N_REJ ]]; then ROLL=DRIFT; fi
  printf 'VERIFIED_SWEEPS=%d/%d REJECTIONS_OK=%d/%d\n' "$N_SW_VER" "$N_SW" "$N_REJ_OK" "$N_REJ"
  printf 'RESEARCH_GATE: %s (sweeps=%d verified=%d exempt=%d hit=%d refused=%d invalid=%d rejections=%d rejections-ok=%d findings=%d drift=%d)\n' \
    "$ROLL" "$N_SW" "$N_SW_VER" "$N_SW_EX" "$N_SW_HIT" "$N_SW_REF" "$N_SW_INV" "$N_REJ" "$N_REJ_OK" "$N_FINDINGS" "$N_DRIFT"

  [[ $ROLL == CLEAN ]] && return 0
  return 1
}

# ---- integrity mode: cross-section reference resolution (declared rows only) ----

integ_trim() { # TOKEN -> edge decoration stripped (quotes, backticks, brackets)
  local t=$1 guard=0
  while :; do
    guard=$((guard + 1)); if [[ $guard -gt 16 ]]; then break; fi
    case "$t" in
      '`'*|'"'*|"'"*|'('*|'['*|'{'*|'<'*|'*'*|'!'*|'?'*) t=${t#?}; continue ;;
    esac
    break
  done
  while :; do
    guard=$((guard + 1)); if [[ $guard -gt 32 ]]; then break; fi
    case "$t" in
      *'`'|*'"'|*"'"|*')'|*']'|*'}'|*'>'|*','|*';'|*'.'|*':'|*'!'|*'?') t=${t%?}; continue ;;
    esac
    break
  done
  printf '%s' "$t"
}

integ_emit_ref() { # KIND ID SECTION ROW CELL DISPO DETAIL -> count + REF line
  N_IREF=$((N_IREF + 1))
  local obs verdict extra=''
  case "$6" in
    resolved) N_IRES=$((N_IRES + 1)); obs=resolved; verdict=match ;;
    unresolved) N_IUNRES=$((N_IUNRES + 1)); obs=unresolved; verdict=mismatch ;;
    *) N_IEXEMPT=$((N_IEXEMPT + 1)); obs=exempt; verdict=exempt; extra=" ${7:-reason=exempt}" ;;
  esac
  IREF_LINES+=("REF kind=$1 id=$(chain_disp "$2") section=$3 row=$(chain_disp "$4") cell=$5 observed=$obs verdict=$verdict$extra")
  if [[ $6 == unresolved ]]; then
    emit_finding REF_UNRESOLVED warn integrity \
      "kind=$1 id=$(chain_disp "$2") section=$3 row=$(chain_disp "$4") cell=$5"
  fi
  return 0
}

integ_token() { # SECTION ROW CELL TOKEN EXEMPT_STATUS -> classify + emit
  local tok=$4 kind='' dispo='' detail=''
  if [[ -n ${SRC_IDS[$tok]+x} ]]; then kind=source; dispo=resolved
  elif [[ -n ${CLAIM_IDS[$tok]+x} ]]; then kind=claim; dispo=resolved
  elif [[ -n ${SWEEP_IDS[$tok]+x} ]]; then kind=sweep; dispo=resolved
  elif [[ $tok =~ ^[CN][0-9][A-Za-z0-9_-]*$ ]]; then kind=claim; dispo=unresolved
  elif [[ $tok =~ ^SW[0-9][A-Za-z0-9_-]*$ ]]; then kind=sweep; dispo=unresolved
  elif [[ $tok =~ ^S[0-9][A-Za-z0-9_-]*$ ]]; then kind=source; dispo=unresolved
  elif [[ $(sweep_token_class "$tok") == nonlocal ]]; then kind=location; dispo=exempt; detail='reason=non-local'
  else return 0; fi
  if [[ $dispo != exempt && -n ${5:-} ]]; then
    dispo=exempt; detail="status=$5"
  fi
  integ_emit_ref "$kind" "$tok" "$1" "$2" "$3" "$dispo" "$detail"
  return 0
}

integ_cell() { # SECTION ROW CELL RAW EXEMPT_STATUS -> one REF per id-shaped token
  local raw=$4 st=${5:-} tok
  if [[ -z $raw ]]; then return 0; fi
  local -a toks=()
  while IFS= read -r tok; do
    if [[ -n $tok ]]; then toks+=("$tok"); fi
  done < <(printf '%s\n' "$raw" | tr ',;' '  ' | tr -s '[:space:]' '\n')
  for tok in "${toks[@]+"${toks[@]}"}"; do
    tok=$(integ_trim "$tok")
    if [[ -n $tok ]]; then integ_token "$1" "$2" "$3" "$tok" "$st"; fi
  done
  return 0
}

verify_integrity() {
  local record=$1
  ROOT=${CHOUSA_ROOT:-$ROOT}
  [[ -n ${record:-} ]] || die_usage "record path required (verify-integrity RECORD, --record, or CHOUSA_RECORD)"
  [[ -e $record ]] || die_usage "record not found: $record"
  [[ -f $record ]] || die_usage "record is not a regular file: $record"
  [[ -r $record ]] || die_usage "record unreadable: $record"
  [[ -d $ROOT ]] || die_usage "root is not a directory: $ROOT (--root)"

  FINDING_LINES=(); N_FINDINGS=0; N_DRIFT=0; ROLL=CLEAN
  scan_secrets "$record"
  load_sections "$record"

  declare -g -A SRC_IDS=() CLAIM_IDS=() SWEEP_IDS=()
  local row rid rrow rowname st exst to n l
  local -a IREF_LINES=()
  local N_IREF=0 N_IRES=0 N_IUNRES=0 N_IEXEMPT=0

  while IFS= read -r row; do
    if [[ -z $row ]]; then continue; fi
    rid=$(cell "$row" id)
    if [[ -n $rid ]]; then SRC_IDS[$rid]=1; fi
  done < <(table_rows Sources)
  while IFS= read -r row; do
    if [[ -z $row ]]; then continue; fi
    rid=$(cell "$row" id)
    if [[ -n $rid ]]; then CLAIM_IDS[$rid]=1; fi
  done < <(table_rows Claims)
  while IFS= read -r row; do
    if [[ -z $row ]]; then continue; fi
    rid=$(cell "$row" id)
    if [[ -n $rid ]]; then CLAIM_IDS[$rid]=1; fi
  done < <(table_rows Negatives)
  while IFS= read -r row; do
    if [[ -z $row ]]; then continue; fi
    rid=$(cell "$row" id)
    if [[ -n $rid ]]; then SWEEP_IDS[$rid]=1; fi
  done < <(table_rows Sweeps)

  # Chain rows: from/claim name the claim, to names the source (fragment cut);
  # a row whose status is the exempt set has its tokens counted exempt.
  n=0
  while IFS= read -r rrow; do
    if [[ -z $rrow ]]; then continue; fi
    n=$((n + 1))
    rowname=$(cell "$rrow" hop)
    if [[ -z $rowname ]]; then rowname="H$n"; fi
    st=$(cell "$rrow" status | tr 'A-Z' 'a-z')
    exst=''
    case "$st" in
      unresolved|blocked-no-fetch|rejected|labelled-dead|not-applicable) exst=$st ;;
    esac
    integ_cell chain "$rowname" from "$(chain_cell "$rrow" from)" "$exst"
    integ_cell chain "$rowname" claim "$(chain_cell "$rrow" claim claim_id claim-id)" "$exst"
    to=$(norm_ptr "$(chain_cell "$rrow" to)")
    integ_cell chain "$rowname" to "${to%%#*}" "$exst"
  done < <(table_rows Chain)

  n=0
  while IFS= read -r rrow; do
    if [[ -z $rrow ]]; then continue; fi
    n=$((n + 1))
    rowname=$(cell "$rrow" id)
    if [[ -z $rowname ]]; then rowname="C$n"; fi
    integ_cell claims "$rowname" sweep "$(chain_cell "$rrow" sweep sweeps sweep_id)" ""
    integ_cell claims "$rowname" source "$(chain_cell "$rrow" source src source_id)" ""
    integ_cell claims "$rowname" ref "$(chain_cell "$rrow" ref reference cite)" ""
    integ_cell claims "$rowname" pointer "$(cell "$rrow" pointer)" ""
  done < <(table_rows Claims)

  n=0
  while IFS= read -r rrow; do
    if [[ -z $rrow ]]; then continue; fi
    n=$((n + 1))
    rowname=$(cell "$rrow" id)
    if [[ -z $rowname ]]; then rowname="N$n"; fi
    st=$(cell "$rrow" status | tr 'A-Z' 'a-z')
    exst=''
    case "$st" in
      unresolved|blocked-no-fetch|labelled-dead|not-applicable) exst=$st ;;
    esac
    integ_cell negatives "$rowname" sweep "$(chain_cell "$rrow" sweep sweeps sweep_id)" "$exst"
    integ_cell negatives "$rowname" where "$(chain_cell "$rrow" where looked_at looked location)" "$exst"
  done < <(table_rows Negatives)

  n=0
  while IFS= read -r rrow; do
    if [[ -z $rrow ]]; then continue; fi
    n=$((n + 1))
    rowname=$(cell "$rrow" id)
    if [[ -z $rowname ]]; then rowname="SW$n"; fi
    st=$(cell "$rrow" status | tr 'A-Z' 'a-z')
    exst=''
    case "$st" in
      unresolved|blocked-no-fetch|labelled-dead|not-applicable) exst=$st ;;
    esac
    integ_cell sweeps "$rowname" claim_id "$(chain_cell "$rrow" claim_id claim-id claim negative_id)" "$exst"
    integ_cell sweeps "$rowname" where "$(sweep_raw_where "$rrow")" "$exst"
  done < <(table_rows Sweeps)

  n=0
  while IFS= read -r rrow; do
    if [[ -z $rrow ]]; then continue; fi
    n=$((n + 1))
    rowname=$(cell "$rrow" id)
    if [[ -z $rowname ]]; then rowname="R$n"; fi
    integ_cell rejections "$rowname" ref "$(chain_cell "$rrow" ref reference)" ""
  done < <(table_rows Rejections)

  printf 'research-gate %s — ts=%s — mode=integrity — record=%s\n' "$VERSION" "$TS_UTC" "$record"
  for l in "${IREF_LINES[@]+"${IREF_LINES[@]}"}"; do printf '%s\n' "$l"; done
  for l in "${FINDING_LINES[@]+"${FINDING_LINES[@]}"}"; do printf '%s\n' "$l"; done
  if [[ $N_IUNRES -ne 0 ]]; then ROLL=DRIFT; fi
  printf 'INTEGRITY refs=%d resolved=%d unresolved=%d\n' "$N_IREF" "$N_IRES" "$N_IUNRES"
  printf 'RESEARCH_GATE: %s (refs=%d resolved=%d unresolved=%d exempt=%d findings=%d drift=%d)\n' \
    "$ROLL" "$N_IREF" "$N_IRES" "$N_IUNRES" "$N_IEXEMPT" "$N_FINDINGS" "$N_DRIFT"

  [[ $ROLL == CLEAN ]] && return 0
  return 1
}

# ---- verify-all mode: one input, one composed deep verdict ----

json_escape() { # STRING -> JSON string body (quote, backslash, control bytes)
  local s=$1 out='' i c hex
  local LC_ALL=C
  for ((i = 0; i < ${#s}; i++)); do
    c=${s:i:1}
    if [[ $c == '"' ]]; then out+='\"'
    elif [[ $c == '\' ]]; then out+='\\'
    elif [[ $c == $'\n' ]]; then out+='\n'
    elif [[ $c == $'\r' ]]; then out+='\r'
    elif [[ $c == $'\t' ]]; then out+='\t'
    elif [[ $c == [[:cntrl:]] ]]; then
      printf -v hex '%04x' "'$c"
      out+="\\u$hex"
    else
      out+="$c"
    fi
  done
  printf '%s' "$out"
}

json_counts() { # "k=v k=v …" -> JSON object body (integer values stay bare)
  local counts=$1 out='' kv k v first=1
  for kv in $counts; do
    k=${kv%%=*}; v=${kv#*=}
    if [[ $first -eq 0 ]]; then out+=','; fi
    first=0
    if [[ $v =~ ^-?[0-9]+$ ]]; then
      out+="\"$(json_escape "$k")\":$v"
    else
      out+="\"$(json_escape "$k")\":\"$(json_escape "$v")\""
    fi
  done
  printf '{%s}' "$out"
}

VAS_OUT='' VAS_RC=0 VAS_VERDICT='' VAS_FIND=0 VAS_DRIFT=0 VAS_COUNTS=''
VAS_NATIVE='' VAS_FINDINGS=''

verify_all_section() { # NAME MODE ARG [ARG…] -> VAS_*; unavailable on rc∉{0,1}
  local name=$1 mode=$2
  shift 2
  local rc=0 line nverdict
  VAS_OUT=$(bash "$SELF" "$mode" "$@" --root "$ROOT" 2>&1) || rc=$?
  VAS_RC=$rc
  VAS_VERDICT='' VAS_FIND=0 VAS_DRIFT=0 VAS_COUNTS='' VAS_NATIVE='' VAS_FINDINGS=''
  nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$VAS_OUT" || true)
  if [[ ( $rc -ne 0 && $rc -ne 1 ) || ${nverdict:-0} -ne 1 ]]; then
    VAS_VERDICT=DRIFT VAS_FIND=1 VAS_DRIFT=1
    VAS_FINDINGS="FINDING VERIFY_ALL_SECTION_UNAVAILABLE severity=crit surface=verify-all obs=section=$name rc=$rc verdict-lines=${nverdict:-0}"
    return 0
  fi
  line=$(grep -m1 '^RESEARCH_GATE: ' <<<"$VAS_OUT")
  if [[ $line =~ ^RESEARCH_GATE:[[:space:]](CLEAN|DRIFT)[[:space:]]\((.*)\)$ ]]; then
    VAS_VERDICT=${BASH_REMATCH[1]} VAS_COUNTS=${BASH_REMATCH[2]}
  else
    VAS_VERDICT=DRIFT VAS_FIND=1 VAS_DRIFT=1
    VAS_FINDINGS="FINDING VERIFY_ALL_SECTION_UNAVAILABLE severity=crit surface=verify-all obs=section=$name rc=$rc unparsable-verdict"
    return 0
  fi
  if [[ $VAS_COUNTS =~ (^| )findings=([0-9]+) ]]; then VAS_FIND=${BASH_REMATCH[2]}; fi
  if [[ $VAS_COUNTS =~ (^| )drift=([0-9]+) ]]; then VAS_DRIFT=${BASH_REMATCH[2]}; fi
  case "$mode" in
    verify-claims) VAS_NATIVE=$(grep -m1 '^VERDICT_BEARING_CLAIMS=' <<<"$VAS_OUT" || true) ;;
    verify-chain) VAS_NATIVE=$(grep -m1 '^RESOLVED_HOPS=' <<<"$VAS_OUT" || true) ;;
    verify-sweeps) VAS_NATIVE=$(grep -m1 '^VERIFIED_SWEEPS=.*REJECTIONS_OK=' <<<"$VAS_OUT" || true) ;;
    verify-integrity) VAS_NATIVE=$(grep -m1 '^INTEGRITY refs=' <<<"$VAS_OUT" || true) ;;
  esac
  VAS_FINDINGS=$(grep '^FINDING ' <<<"$VAS_OUT" || true)
  return 0
}

verify_all() {
  local record=$1
  ROOT=${CHOUSA_ROOT:-$ROOT}
  [[ -n ${record:-} ]] || die_usage "record path required (verify-all RECORD, --record, or CHOUSA_RECORD)"
  [[ -e $record ]] || die_usage "record not found: $record"
  [[ -f $record ]] || die_usage "record is not a regular file: $record"
  [[ -r $record ]] || die_usage "record unreadable: $record"
  [[ -d $ROOT ]] || die_usage "root is not a directory: $ROOT (--root)"
  if [[ -n ${CLAIMS_ARG:-} ]]; then
    [[ -e $CLAIMS_ARG ]] || die_usage "claims file not found: $CLAIMS_ARG (--claims)"
    [[ -f $CLAIMS_ARG ]] || die_usage "claims file is not a regular file: $CLAIMS_ARG (--claims)"
    [[ -r $CLAIMS_ARG ]] || die_usage "claims file unreadable: $CLAIMS_ARG (--claims)"
  fi
  if [[ -n ${JSON_ARG:-} ]]; then
    local jdir
    jdir=$(dirname -- "$JSON_ARG")
    [[ -d $jdir ]] || die_usage "manifest directory not found: $jdir (--json)"
    if [[ -e $JSON_ARG && ! -f $JSON_ARG ]]; then
      die_usage "manifest path is not a regular file: $JSON_ARG (--json)"
    fi
  fi

  local -a VA_ORDER=(structure claims chain sweeps integrity)
  local -A SEC_STATE=() SEC_VERDICT=() SEC_FIND=() SEC_DRIFT=() SEC_COUNTS=()
  local -A SEC_NATIVE=() SEC_FINDINGS=()
  local name has_heads json_lines claims_surface='' declared='' crow
  for name in "${VA_ORDER[@]}"; do SEC_STATE[$name]=absent; done

  has_heads=$(grep -c '^##[[:space:]]' -- "$record" || true)
  json_lines=$(grep -c '^[[:space:]]*{' -- "$record" || true)
  if [[ ${has_heads:-0} -eq 0 && ${json_lines:-0} -gt 0 ]]; then
    # The input is itself a claims JSONL: it is its own claims surface.
    claims_surface=$record
  else
    SEC_STATE[structure]=run
    load_sections "$record"
    if [[ -n ${SEC_BODY[Chain]+x} ]]; then SEC_STATE[chain]=run; fi
    if [[ -n ${SEC_BODY[Sweeps]+x} || -n ${SEC_BODY[Negatives]+x} || -n ${SEC_BODY[Rejections]+x} ]]; then
      SEC_STATE[sweeps]=run
    fi
    if [[ -n ${SEC_BODY[Meta]+x} ]]; then
      # Meta rows are | key | value | (canonical) or key: value lines; the
      # binding key is claims/claims_file/claims-file/claimset.
      while IFS= read -r crow; do
        [[ -z $crow ]] && continue
        if [[ $crow =~ ^[[:space:]]*\|[[:space:]]*(claims|claims_file|claims-file|claimset)[[:space:]]*\|[[:space:]]*([^|]+)\| ]]; then
          declared=${BASH_REMATCH[2]}
        elif [[ $crow =~ ^[[:space:]]*(claims|claims_file|claims-file|claimset)[[:space:]]*:[[:space:]]*([^[:space:]]+) ]]; then
          declared=${BASH_REMATCH[2]}
        fi
        declared=$(printf '%s' "$declared" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        if [[ -n $declared ]]; then break; fi
      done <<<"${SEC_BODY[Meta]}"
    fi
    if [[ -n ${CLAIMS_ARG:-} ]]; then
      claims_surface=$CLAIMS_ARG
    elif [[ -n $declared ]]; then
      if claim_source_path "$declared"; then
        claims_surface=$CLAIM_SRC_PATH
      else
        SEC_STATE[claims]=run
        SEC_VERDICT[claims]=DRIFT SEC_FIND[claims]=1 SEC_DRIFT[claims]=1
        SEC_COUNTS[claims]='findings=1 drift=1'
        SEC_FINDINGS[claims]="FINDING VERIFY_ALL_CLAIMS_UNRESOLVED severity=warn surface=verify-all obs=declared=$declared reason=$CLAIM_REFUSE"
      fi
    fi
  fi
  if [[ -n $claims_surface ]]; then SEC_STATE[claims]=run; fi

  # Integrity cross-checks the ids the record declares; it needs at least one
  # other section to have a surface at all. With none (no runnable section) it
  # is honestly absent rather than a vacuous CLEAN.
  local n_other=0
  for name in structure claims chain sweeps; do
    if [[ ${SEC_STATE[$name]} != absent ]]; then n_other=$((n_other + 1)); fi
  done
  if [[ $n_other -ge 1 ]]; then SEC_STATE[integrity]=run; fi

  local n_run=0 n_absent=0 n_dsec=0 n_find=0 n_drift=0 roll=CLEAN
  for name in "${VA_ORDER[@]}"; do
    if [[ ${SEC_STATE[$name]} == run && -z ${SEC_VERDICT[$name]:-} ]]; then
      case "$name" in
        structure) verify_all_section structure verify "$record" ;;
        claims) verify_all_section claims verify-claims "$claims_surface" ;;
        chain) verify_all_section chain verify-chain "$record" ;;
        sweeps) verify_all_section sweeps verify-sweeps "$record" ;;
        integrity) verify_all_section integrity verify-integrity "$record" ;;
      esac
      SEC_VERDICT[$name]=$VAS_VERDICT
      SEC_FIND[$name]=$VAS_FIND
      SEC_DRIFT[$name]=$VAS_DRIFT
      SEC_COUNTS[$name]=$VAS_COUNTS
      SEC_NATIVE[$name]=$VAS_NATIVE
      SEC_FINDINGS[$name]=$VAS_FINDINGS
    fi
  done
  for name in "${VA_ORDER[@]}"; do
    if [[ ${SEC_STATE[$name]} == absent ]]; then n_absent=$((n_absent + 1)); continue; fi
    n_run=$((n_run + 1))
    n_find=$((n_find + ${SEC_FIND[$name]:-0}))
    n_drift=$((n_drift + ${SEC_DRIFT[$name]:-0}))
    if [[ ${SEC_VERDICT[$name]} == DRIFT ]]; then
      n_dsec=$((n_dsec + 1)); roll=DRIFT
    fi
  done

  if [[ -n ${JSON_ARG:-} ]]; then
    local line sha_rec sha_gate sec_json='' first=1 cj
    sha_rec=$(sha256sum -- "$record" 2>/dev/null | cut -d' ' -f1 || true)
    sha_gate=$(sha256sum -- "$SELF" 2>/dev/null | cut -d' ' -f1 || true)
    if [[ -z $sha_rec || -z $sha_gate ]]; then
      printf 'research-gate: sha256sum unavailable; manifest not written\n' >&2
      exit 2
    fi
    for name in "${VA_ORDER[@]}"; do
      if [[ $first -eq 0 ]]; then sec_json+=','; fi
      first=0
      if [[ ${SEC_STATE[$name]} == absent ]]; then
        sec_json+="{\"name\":\"$name\",\"state\":\"absent\"}"
      else
        cj=$(json_counts "${SEC_COUNTS[$name]:-}")
        sec_json+="{\"name\":\"$name\",\"state\":\"run\",\"verdict\":\"${SEC_VERDICT[$name]}\""
        sec_json+=",\"findings\":${SEC_FIND[$name]:-0},\"drift\":${SEC_DRIFT[$name]:-0},\"tallies\":$cj"
        if [[ -n ${SEC_NATIVE[$name]:-} ]]; then
          sec_json+=",\"native\":\"$(json_escape "${SEC_NATIVE[$name]}")\""
        fi
        sec_json+='}'
      fi
    done
    line="{\"schema\":\"chousa-verify-all/v1\",\"ts\":\"$TS_UTC\",\"record\":\"$(json_escape "$record")\""
    line+=",\"record_sha256\":\"$sha_rec\",\"gate_sha256\":\"$sha_gate\",\"sections\":[$sec_json]"
    line+=",\"verdict\":\"$roll\",\"sections_run\":$n_run,\"sections_absent\":$n_absent,\"drift_sections\":$n_dsec}"
    if ! printf '%s\n' "$line" >>"$JSON_ARG"; then
      printf 'research-gate: manifest append failed: %s\n' "$JSON_ARG" >&2
      exit 2
    fi
  fi

  printf 'research-gate %s — ts=%s — mode=verify-all — record=%s — claims=%s — root=%s\n' \
    "$VERSION" "$TS_UTC" "$record" "${claims_surface:--}" "$ROOT"
  for name in "${VA_ORDER[@]}"; do
    if [[ ${SEC_STATE[$name]} == absent ]]; then
      printf 'SECTION %s state=absent\n' "$name"
      continue
    fi
    if [[ -n ${SEC_NATIVE[$name]:-} ]]; then
      printf 'SECTION %s state=run verdict=%s findings=%s drift=%s tally=%s\n' \
        "$name" "${SEC_VERDICT[$name]}" "${SEC_FIND[$name]:-0}" "${SEC_DRIFT[$name]:-0}" "${SEC_NATIVE[$name]}"
    else
      printf 'SECTION %s state=run verdict=%s findings=%s drift=%s\n' \
        "$name" "${SEC_VERDICT[$name]}" "${SEC_FIND[$name]:-0}" "${SEC_DRIFT[$name]:-0}"
    fi
    if [[ -n ${SEC_FINDINGS[$name]:-} ]]; then printf '%s\n' "${SEC_FINDINGS[$name]}"; fi
  done
  printf 'VERIFY_ALL sections=%d run=%d absent=%d drift-sections=%d findings=%d drift=%d\n' \
    "${#VA_ORDER[@]}" "$n_run" "$n_absent" "$n_dsec" "$n_find" "$n_drift"
  printf 'RESEARCH_GATE: %s (sections=%d run=%d absent=%d drift-sections=%d findings=%d drift=%d)\n' \
    "$roll" "${#VA_ORDER[@]}" "$n_run" "$n_absent" "$n_dsec" "$n_find" "$n_drift"

  [[ $roll == CLEAN ]] && return 0
  return 1
}

# ---- pin/drift: the gate's own behavioral baseline (r8) ----
#
# Lineage: mori-shokunin r10 turned its census into a pinned artifact with a
# declared volatile-field contract (tools/mori-census.sh --pin/--drift, its
# design note corpus/knowledge/drift-pin-r10.md, lesson
# 2026-10-15-volatile-contract-behavioral-baselines.md). This lane adapts the
# pattern to a gate whose canonical output is deterministic per input, so the
# volatile set is two fields instead of a counter-class list. The full
# contract (invocation, volatile list, exit codes, token grammar) is in the
# file header under "Pin/drift mode"; the implementation notes here cover what
# the header does not.
#
# Captures are frozen before anything compares them: the canonical run writes
# to a file (never a live pipe), the file is normalized into a variable, and
# the fixture is removed before the drift report prints. The fixture is built,
# used and removed inside one capture call, so pin and drift always compare
# the same invocation shape even if the lane tree changes underneath.
GATE_DRIFT_VOLATILE_FIELDS='ts gate_sha256'
GATE_BASELINE_MAGIC='# chousa-gate drift baseline v1'
GATE_BASELINE_MARKER='# --- canonical output follows ---'
GATE_MANIFEST_MARKER='# --- json manifest line follows ---'

GATE_CAP='' GATE_CAP_RC=0 GATE_CAP_NOTE='' GATE_CAP_DIR=''
GATE_REPORT=''
GDRIFT_KEYS=()
declare -A GDRIFT_KEYVAL=()

gate_drift_normalize() { # PATH -> stdout, volatile values masked to <V>
  local f=$1 line
  while IFS= read -r line || [[ -n $line ]]; do
    line=$(printf '%s' "$line" | sed -E \
      -e 's/ts=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z/ts=<V>/g' \
      -e 's/"ts":"[^"]*"/"ts":"<V>"/g' \
      -e 's/"gate_sha256":"[^"]*"/"gate_sha256":"<V>"/g') || true
    printf '%s\n' "$line"
  done <"$f"
}

gate_pin_fixture() { # DIR — the canonical hermetic fixture (header contract)
  local dir=$1
  mkdir -p "$dir/lib" "$dir/noise" || return 1
  printf 'line1 primary material\nline2\n' >"$dir/lib/primary.md" || return 1
  printf 'aggregator chrome sources sidebar\n' >"$dir/noise/chat-export-sources.md" || return 1
  cat >"$dir/claims.jsonl" <<'PINFIX' || return 1
{"id":"P1","source":"lib/primary.md","span":"line1 primary material","expect":"supported"}
PINFIX
  cat >"$dir/record.md" <<'PINFIX' || return 1
# research-record v1
<!-- chousa-record: v1 -->
## Meta
| key | value |
|---|---|
| window | loopback |
| fetch | none |
| domain | deep-research method |
## Question
Does a dangling sweep binding drift a composed verdict the four r6 sections pass?
## Sources
| id | tier | pointer | notes |
|---|---|---|---|
| S1 | primary | lib/primary.md:1 | local fixture |
## Chain
| hop | from | to | status | anchor_kind | anchor | notes |
|---|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | quote | line1 primary material | direct |
## Claims
| id | kind | text | pointer | status | sweep |
|---|---|---|---|---|---|
| C1 | observation | primary file has line1 | lib/primary.md:1 | verified | |
## Negatives
| id | text | sweep | status |
|---|---|---|---|
| N1 | no fx-only ghost source | SW1 | swept |
## Sweeps
| id | claim_id | where | status |
|---|---|---|---|
| SW1 | C9 | lib/ghost*.md | swept |
## Rejections
| id | ref | reason | flip |
|---|---|---|---|
| R1 | noise/chat-export-sources.md | UI chrome is not a primary source | a primary attestation in that file would flip this |
## Approval
| target | state |
|---|---|
| (none) | not-required |
PINFIX
  return 0
}

gate_canonical_capture() { # -> GATE_CAP | GATE_CAP_RC + GATE_CAP_NOTE
  local fx rc=0 nv nml nsch vcap mcap
  GATE_CAP='' GATE_CAP_RC=0 GATE_CAP_NOTE=''
  fx=$(mktemp -d "${TMPDIR:-/tmp}/chousa-gate-pin.XXXXXX") || {
    GATE_CAP_RC=2; GATE_CAP_NOTE='mktemp-failed'; return 0; }
  GATE_CAP_DIR=$fx
  if ! gate_pin_fixture "$fx"; then
    GATE_CAP_RC=2 GATE_CAP_NOTE='fixture-write-failed'
    rm -rf -- "$fx" 2>/dev/null || true
    GATE_CAP_DIR=''
    return 0
  fi
  ( cd "$fx" || exit 2
    env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_STRICT -u CHOUSA_ROOT \
      -u CHOUSA_AGGREGATOR_ERE \
      bash "$SELF" verify-all record.md --claims claims.jsonl \
      --json manifest.jsonl --root . >capture.txt 2>&1 ) || rc=$?
  nv=$(grep -c '^RESEARCH_GATE: ' -- "$fx/capture.txt" 2>/dev/null || true)
  nml=$(grep -c '' -- "$fx/manifest.jsonl" 2>/dev/null || true)
  nsch=$(grep -c '^{"schema":"chousa-verify-all/v1"' -- "$fx/manifest.jsonl" 2>/dev/null || true)
  if [[ ( $rc -eq 0 || $rc -eq 1 ) && ${nv:-0} -eq 1 && ${nml:-0} -eq 1 && ${nsch:-0} -eq 1 ]]; then
    vcap=$(gate_drift_normalize "$fx/capture.txt") || vcap=''
    mcap=$(gate_drift_normalize "$fx/manifest.jsonl") || mcap=''
    if [[ -z $vcap || -z $mcap ]]; then
      GATE_CAP_RC=2 GATE_CAP_NOTE='empty-capture'
    else
      GATE_CAP=$(printf '%s\n%s\n%s\n' "$vcap" "$GATE_MANIFEST_MARKER" "$mcap")
    fi
  else
    GATE_CAP_RC=2
    GATE_CAP_NOTE="rc=$rc verdict-lines=${nv:-0} manifest-lines=${nml:-0} schema-lines=${nsch:-0}"
  fi
  rm -rf -- "$fx" 2>/dev/null || true
  GATE_CAP_DIR=''
  return 0
}

gate_drift_line_id() { # LINE -> pairing identity, one whitespace-free token
  local line=$1 rest
  case "$line" in
    SECTION\ *) rest=${line#SECTION }; printf 'SECTION:%s' "${rest%% *}" ;;
    FINDING\ *) rest=${line#FINDING }; printf 'FINDING:%s' "${rest%% *}" ;;
    VERIFY_ALL\ *) printf 'VERIFY_ALL' ;;
    RESEARCH_GATE:*) printf 'VERDICT' ;;
    '{'*) printf 'MANIFEST' ;;
    "$GATE_MANIFEST_MARKER") printf 'MANIFEST-MARKER' ;;
    research-gate\ *) printf 'GATE' ;;
    *) printf 'LINE' ;;
  esac
}

gate_drift_scan() { # LINE -> GDRIFT_KEYS (first-seen order) + GDRIFT_KEYVAL
  # A token counts only as key=value with a key-shaped key, so the header's
  # em dashes, the verdict word and JSON punctuation contribute nothing; a
  # duplicated key's values are concatenated so one occurrence cannot hide
  # another (mori r10 drift_scan). The manifest line is one compact JSON
  # object: "key": is rewritten to key= first, so its fields are named too.
  local line=$1 toks tok key
  GDRIFT_KEYS=()
  GDRIFT_KEYVAL=()
  if [[ $line == '{'* ]]; then
    line=$(printf '%s' "$line" | sed -E 's/"([A-Za-z0-9_-]+)":/\1=/g; s/,/ /g') || true
  fi
  toks=$(printf '%s\n' "$line" | grep -oE '[A-Za-z_][A-Za-z0-9_-]*=[^[:space:]]*' || true)
  while IFS= read -r tok; do
    [[ -n $tok ]] || continue
    key=${tok%%=*}
    [[ -n ${GDRIFT_KEYVAL[$key]+x} ]] || GDRIFT_KEYS+=("$key")
    GDRIFT_KEYVAL[$key]="${GDRIFT_KEYVAL[$key]:-}${tok#*=}"
  done <<<"$toks"
}

gate_drift_field_report() { # BASE_LINE NEW_LINE ID -> changed field tokens
  local bl=$1 nl=$2 id=$3 k
  local -a bkeys=() nkeys=() changed=()
  local -A bval=() nval=()
  gate_drift_scan "$bl"
  bkeys=("${GDRIFT_KEYS[@]}")
  for k in "${bkeys[@]}"; do bval[$k]=${GDRIFT_KEYVAL[$k]}; done
  gate_drift_scan "$nl"
  nkeys=("${GDRIFT_KEYS[@]}")
  for k in "${nkeys[@]}"; do nval[$k]=${GDRIFT_KEYVAL[$k]}; done
  for k in "${bkeys[@]}"; do
    if [[ -z ${nval[$k]+x} ]]; then changed+=("-$k"); continue; fi
    [[ ${bval[$k]} == "${nval[$k]}" ]] || changed+=("$k")
  done
  for k in "${nkeys[@]}"; do
    [[ -n ${bval[$k]+x} ]] || changed+=("+$k")
  done
  # A difference that lives outside key=value tokens (verdict word, a state
  # sentence) falls back to naming the line's id instead of a silent change.
  if [[ ${#changed[@]} -eq 0 ]]; then changed+=("$id"); fi
  printf '%s\n' "${changed[@]}"
}

gate_drift_report() { # BASELINE_BODY CAPTURE -> GATE_REPORT
  local body=$1 cap=$2 line
  local -a base=() new=() b_used=() n_used=() rep=()
  local i j id matched fields joined sorted
  while IFS= read -r line; do base+=("$line"); done <<<"$body"
  while IFS= read -r line; do new+=("$line"); done <<<"$cap"
  # pass 1 — exact matches (multiset), so a removed/added line is not mispaired
  # with a same-id sibling and mis-reported as a field change.
  for i in "${!base[@]}"; do
    for j in "${!new[@]}"; do
      [[ ${n_used[$j]:-0} -eq 1 ]] && continue
      if [[ ${new[$j]} == "${base[$i]}" ]]; then b_used[$i]=1; n_used[$j]=1; break; fi
    done
  done
  # pass 2 — same-id pairing names the changed non-volatile fields.
  for i in "${!base[@]}"; do
    [[ ${b_used[$i]:-0} -eq 1 ]] && continue
    id=$(gate_drift_line_id "${base[$i]}")
    matched=-1
    for j in "${!new[@]}"; do
      [[ ${n_used[$j]:-0} -eq 1 ]] && continue
      [[ $(gate_drift_line_id "${new[$j]}") == "$id" ]] || continue
      matched=$j; break
    done
    if [[ $matched -ge 0 ]]; then
      n_used[$matched]=1
      fields=$(gate_drift_field_report "${base[$i]}" "${new[$matched]}" "$id")
      while IFS= read -r line; do [[ -n $line ]] && rep+=("$line"); done <<<"$fields"
    else
      rep+=("-$id")
    fi
  done
  # pass 3 — anything left on the capture side was added.
  for j in "${!new[@]}"; do
    [[ ${n_used[$j]:-0} -eq 1 ]] && continue
    rep+=("+$(gate_drift_line_id "${new[$j]}")")
  done
  # The joined strings differed yet no line or field is named: a pure reorder
  # (pass 1 is order-independent). Say so instead of a false 'none'.
  if [[ ${#rep[@]} -eq 0 ]]; then rep+=("output-order"); fi
  joined=$(printf '%s\n' "${rep[@]}")
  sorted=$(LC_ALL=C sort -u <<<"$joined")
  GATE_REPORT=${sorted//$'\n'/ }
}

run_pin() { # PATH
  local path=$1 sha text
  gate_canonical_capture
  if [[ $GATE_CAP_RC -ne 0 || -z $GATE_CAP ]]; then
    printf 'research-gate: --pin canonical capture failed (%s): %s\n' \
      "${GATE_CAP_NOTE:-unknown}" "$path" >&2
    exit 2
  fi
  sha=$(sha256sum -- "$SELF" 2>/dev/null | cut -d' ' -f1) || sha=''
  if [[ -z $sha ]]; then
    printf 'research-gate: --pin sha256sum unavailable; baseline not written\n' >&2
    exit 2
  fi
  # The text is staged in a variable and written by ONE simple printf: a
  # redirection failure on a compound command exits 0 on this bash (measured,
  # 5.3.15: `{ …; } >/missing/dir/f` prints the error, runs nothing, returns
  # 0), so `{ …; } >"$path"` would report a phantom success. The simple
  # command's redirection failure is real and caught.
  text=''
  text+="$GATE_BASELINE_MAGIC — written by research-gate.sh --pin"$'\n'
  text+='# lineage: mori-shokunin r10 pin/drift (tools/mori-census.sh); volatile contract per the gate header'$'\n'
  text+="# gate_sha256=$sha"$'\n'
  text+="# pinned_ts=$TS_UTC"$'\n'
  text+='# canonical: verify-all record.md --claims claims.jsonl --json manifest.jsonl --root . (cwd = a fresh temp fixture written by the gate)'$'\n'
  text+="# volatile_fields=$GATE_DRIFT_VOLATILE_FIELDS"$'\n'
  text+='# volatile_note=values of these fields are masked to <V>; --drift re-normalizes with the CURRENT list and reports every changed field. Changing the list is itself drift; gate_sha256 is informational (behavior, not revision, is compared).'$'\n'
  text+="$GATE_BASELINE_MARKER"$'\n'
  text+="$GATE_CAP"$'\n'
  if ! printf '%s' "$text" >"$path" 2>/dev/null; then
    printf 'research-gate: --pin could not write baseline: %s\n' "$path" >&2
    exit 2
  fi
  printf 'GATE_PIN: ok path=%s gate_sha256=%s\n' "$path" "$sha"
  exit 0
}

run_drift() { # PATH
  local path=$1 line first='' in_block=0 have_vol=0 declared='' body='' vol_token=''
  [[ -e $path ]] || {
    printf 'research-gate: --drift baseline missing: %s\n' "$path" >&2
    exit 2
  }
  [[ -f $path && -r $path ]] || {
    printf 'research-gate: --drift baseline unreadable: %s\n' "$path" >&2
    exit 2
  }
  while IFS= read -r line || [[ -n $line ]]; do
    [[ -n $first ]] || first=$line
    if [[ $in_block -eq 1 ]]; then body+="$line"$'\n'; continue; fi
    if [[ $line == "$GATE_BASELINE_MARKER" ]]; then in_block=1; continue; fi
    if [[ $line == '# volatile_fields='* ]]; then
      have_vol=1
      declared=${line#'# volatile_fields='}
    fi
  done <"$path"
  [[ $first == "$GATE_BASELINE_MAGIC"* ]] || {
    printf 'research-gate: --drift baseline malformed (magic line absent): %s\n' "$path" >&2
    exit 2
  }
  [[ $in_block -eq 1 ]] || {
    printf 'research-gate: --drift baseline malformed (canonical marker absent): %s\n' "$path" >&2
    exit 2
  }
  [[ $have_vol -eq 1 ]] || {
    printf 'research-gate: --drift baseline malformed (volatile_fields contract absent): %s\n' "$path" >&2
    exit 2
  }
  [[ -n $body ]] || {
    printf 'research-gate: --drift baseline malformed (empty canonical block): %s\n' "$path" >&2
    exit 2
  }
  body=${body%$'\n'}
  # The declared contract is compared too: a baseline pinned under a DIFFERENT
  # volatile list is drifting even when nothing in this run exercises the
  # changed mask (the recorded list is the contract — mori r10's d7710981
  # refinement).
  [[ $declared == "$GATE_DRIFT_VOLATILE_FIELDS" ]] || vol_token=volatile_fields
  gate_canonical_capture
  if [[ $GATE_CAP_RC -ne 0 || -z $GATE_CAP ]]; then
    printf 'research-gate: --drift canonical capture failed (%s): %s\n' \
      "${GATE_CAP_NOTE:-unknown}" "$path" >&2
    exit 2
  fi
  if [[ $body == "$GATE_CAP" ]]; then
    if [[ -n $vol_token ]]; then
      printf 'GATE_DRIFT: %s\n' "$vol_token"
      exit 1
    fi
    printf 'GATE_DRIFT: none\n'
    exit 0
  fi
  gate_drift_report "$body" "$GATE_CAP"
  printf 'GATE_DRIFT: %s%s\n' "${GATE_REPORT:-none}" "${vol_token:+ $vol_token}"
  exit 1
}

run_selftest() {
  local cases=0 failures=0
  WORK=$(mktemp -d "${TMPDIR:-/tmp}/chousa-research-gate-selftest.XXXXXX") \
    || die_usage "mktemp failed"
  trap 'rm -rf -- "${WORK:-}"' EXIT
  OUTSIDE_FILE=$(mktemp "${TMPDIR:-/tmp}/chousa-gate-outside.XXXXXX") \
    || die_usage "mktemp failed"
  # WORK/OUTSIDE_FILE/GATE_CAP_DIR are globals with ${:-} guards: at
  # errexit-exit the EXIT trap sees function locals as unset (measured), which
  # silently skips the cleanup, and a quota-limited tmp dir can fail the first
  # fixture write. Honoring TMPDIR lets a crowded /tmp be swapped for another
  # scratch mount. GATE_CAP_DIR is the pin/drift capture fixture: removed at
  # the end of every capture, and re-swept here if a capture died mid-flight.
  trap 'rm -rf -- "${WORK:-}" "${OUTSIDE_FILE:-}" "${GATE_CAP_DIR:-}"' EXIT
  printf 'outside text\n' >"$OUTSIDE_FILE"
  mkdir -p "$WORK/lib" "$WORK/noise" "$WORK/claimsrc"
  printf 'line1 primary material\nline2\n' >"$WORK/lib/primary.md"
  printf 'aggregator chrome sources sidebar\n' >"$WORK/noise/chat-export-sources.md"
  printf 'alpha claim holds\nbeta claim holds CONTRADICTION-MARKER: source disagrees\ngamma claim retracted\n' >"$WORK/claimsrc/ledger.md"
  printf 'arrow check \xe2\x86\x92 done\n' >"$WORK/claimsrc/arrow.md"
  printf '# Chain target\nintro line\n## Term table\nalpha row present\nThe craftsman certifies the work\nomega final line\n' >"$WORK/lib/chain_target.md"
  cat >"$WORK/lib/boundary.md" <<'EOF'
The punctuation case: alpha boundary word, then stops.
The line-break case: delta boundary word-
The possessive case: gamma boundary word's outcome.
The glued case: theta boundary word continuation-suffix here.
EOF

  cat >"$WORK/claims-pass.jsonl" <<'EOF'
# selftest positive claims
{"id":"P1","source":"lib/primary.md","span":"line1 primary material","expect":"supported"}
{"id":"P2","source":"claimsrc/ledger.md","span":"beta claim holds","expect":"contradicted","marker":"CONTRADICTION-MARKER:"}
{"id":"P3","source":"lib/primary.md","span":"line-nine phantom text","expect":"unsupported"}
{"id":"P4","source":"claimsrc/arrow.md","span":"arrow check \u2192 done","expect":"supported"}
EOF
  cat >"$WORK/claims-fail-tampered.jsonl" <<'EOF'
{"id":"T1","source":"lib/primary.md","span":"line1 PRIMARY material","expect":"supported"}
EOF
  cat >"$WORK/claims-fail-external.jsonl" <<'EOF'
{"id":"E1","source":"https://example.invalid/research.md","span":"remote text","expect":"supported"}
EOF
  cat >"$WORK/claims-fail-session.jsonl" <<'EOF'
{"id":"S1","source":"./.config/agent-token.txt","span":"token text","expect":"supported"}
EOF
  cat >"$WORK/claims-fail-contradicted-unmarked.jsonl" <<'EOF'
{"id":"K1","source":"claimsrc/ledger.md","span":"beta claim holds","expect":"contradicted"}
{"id":"K2","source":"claimsrc/ledger.md","span":"beta claim holds","expect":"contradicted","marker":"NOT-IN-SOURCE"}
EOF
  cat >"$WORK/claims-fail-counting.jsonl" <<'EOF'
# exact-counting case
{"marker_default":"CONTRADICTION-MARKER:"}
{"id":"C1","source":"lib/primary.md","span":"line1 primary material","expect":"supported"}
{"id":"C2","source":"claimsrc/ledger.md","span":"beta claim holds","expect":"contradicted"}
{"id":"C3","source":"lib/primary.md","span":"phantom text never present","expect":"unsupported"}
{"id":"C4","source":"lib/primary.md","span":"line1 primary materialX","expect":"supported"}
{"id":"C5","source":"https://example.invalid/x","span":"remote","expect":"supported"}
not a json object
EOF
  cat >"$WORK/claims-fail-stray-marker.jsonl" <<'EOF'
{"id":"W1","source":"lib/primary.md","span":"line1 primary material","expect":"supported","marker":"STRAY"}
EOF
  printf '{"id":"O1","source":"%s","span":"outside text","expect":"supported"}\n' "$OUTSIDE_FILE" >"$WORK/claims-fail-out-of-corpus.jsonl"
  printf '{"id":"O2","source":"../%s","span":"outside text","expect":"supported"}\n' "$(basename "$OUTSIDE_FILE")" >>"$WORK/claims-fail-out-of-corpus.jsonl"
  cat >"$WORK/claims-boundary-pass.jsonl" <<'EOF'
# token boundaries: punctuation, a non-word-internal hyphen, a line edge and a
# multi-line span are all delimited and must still resolve
{"id":"BP1","source":"lib/boundary.md","span":"alpha boundary word","expect":"supported"}
{"id":"BP2","source":"lib/boundary.md","span":"delta boundary word","expect":"supported"}
{"id":"BP3","source":"lib/primary.md","span":"line2","expect":"supported"}
{"id":"BP4","source":"lib/primary.md","span":"line1 primary material\nline2","expect":"supported"}
EOF
  cat >"$WORK/claims-boundary-fail.jsonl" <<'EOF'
# token boundaries: three substring games that only boundary matching refuses
# (a mid-token truncation, a padded extra word glued into a hyphenated
# compound, and a possessive apostrophe join)
{"id":"BF1","source":"lib/boundary.md","span":"alpha boundary wor","expect":"supported"}
{"id":"BF2","source":"lib/boundary.md","span":"theta boundary word continuation","expect":"supported"}
{"id":"BF3","source":"lib/boundary.md","span":"gamma boundary word","expect":"supported"}
EOF

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
      CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
      "${over[@]+"${over[@]}"}" \
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

  # Claims-mode case runner: same fresh-process discipline as tcase, plus one
  # VERDICT_BEARING_CLAIMS summary expected per run.
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

  # Chain-mode case runner: same fresh-process discipline as tclaims, plus one
  # RESOLVED_HOPS summary expected per run.
  tchain() {
    local name=$1 want_rc=$2
    shift 2
    local -a want=() over=()
    local a tok rc=0 out nverdict nrh ok=1
    for a in "$@"; do
      if [[ $a =~ ^CHOUSA_[A-Z_]+= ]]; then over+=("$a"); else want+=("$a"); fi
    done
    cases=$((cases + 1))
    out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 \
      CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
      "${over[@]+"${over[@]}"}" \
      bash "$SELF" verify-chain "$WORK/$name.md" 2>&1) || rc=$?
    nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true)
    nrh=$(grep -c '^RESOLVED_HOPS=' <<<"$out" || true)
    for tok in "${want[@]+"${want[@]}"}"; do
      [[ $out == *"$tok"* ]] || ok=0
    done
    if [[ $rc -eq $want_rc && $nverdict -eq 1 && $nrh -eq 1 && $ok -eq 1 ]]; then
      printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" "$name" "$rc"
    else
      printf 'FAIL-case %-28s exit=%d want=%d verdicts=%d hops=%d token=%s\n' \
        "$name" "$rc" "$want_rc" "$nverdict" "$nrh" "${want[*]-}"
      printf '%s\n' "$out" | sed 's/^/    | /'
      failures=$((failures + 1))
    fi
  }

  # Sweeps-mode case runner: same fresh-process discipline as tchain, plus one
  # VERIFIED_SWEEPS…REJECTIONS_OK summary expected per run.
  tsweeps() {
    local name=$1 want_rc=$2
    shift 2
    local -a want=() over=()
    local a tok rc=0 out nverdict nsum ok=1
    for a in "$@"; do
      if [[ $a =~ ^CHOUSA_[A-Z_]+= ]]; then over+=("$a"); else want+=("$a"); fi
    done
    cases=$((cases + 1))
    out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 \
      CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
      "${over[@]+"${over[@]}"}" \
      bash "$SELF" verify-sweeps "$WORK/$name.md" 2>&1) || rc=$?
    nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true)
    nsum=$(grep -c '^VERIFIED_SWEEPS=.*REJECTIONS_OK=' <<<"$out" || true)
    for tok in "${want[@]+"${want[@]}"}"; do
      [[ $out == *"$tok"* ]] || ok=0
    done
    if [[ $rc -eq $want_rc && $nverdict -eq 1 && $nsum -eq 1 && $ok -eq 1 ]]; then
      printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" "$name" "$rc"
    else
      printf 'FAIL-case %-28s exit=%d want=%d verdicts=%d sums=%d token=%s\n' \
        "$name" "$rc" "$want_rc" "$nverdict" "$nsum" "${want[*]-}"
      printf '%s\n' "$out" | sed 's/^/    | /'
      failures=$((failures + 1))
    fi
  }

  # Integrity-mode case runner: same fresh-process discipline as tsweeps, plus
  # one INTEGRITY refs=… summary expected per run.
  tintegrity() {
    local name=$1 want_rc=$2
    shift 2
    local -a want=() over=()
    local a tok rc=0 out nverdict nsum ok=1
    for a in "$@"; do
      if [[ $a =~ ^CHOUSA_[A-Z_]+= ]]; then over+=("$a"); else want+=("$a"); fi
    done
    cases=$((cases + 1))
    out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 \
      CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
      "${over[@]+"${over[@]}"}" \
      bash "$SELF" verify-integrity "$WORK/$name.md" 2>&1) || rc=$?
    nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true)
    nsum=$(grep -c '^INTEGRITY refs=' <<<"$out" || true)
    for tok in "${want[@]+"${want[@]}"}"; do
      [[ $out == *"$tok"* ]] || ok=0
    done
    if [[ $rc -eq $want_rc && $nverdict -eq 1 && $nsum -eq 1 && $ok -eq 1 ]]; then
      printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" "$name" "$rc"
    else
      printf 'FAIL-case %-28s exit=%d want=%d verdicts=%d sums=%d token=%s\n' \
        "$name" "$rc" "$want_rc" "$nverdict" "$nsum" "${want[*]-}"
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

  tclaims claims-pass 0 \
    'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=4/4' \
    'CLAIM id=P1 expected=supported observed=supported source=lib/primary.md at=line:1 verdict=match' \
    'CLAIM id=P2 expected=contradicted observed=contradicted source=claimsrc/ledger.md at=line:2 verdict=match' \
    'CLAIM id=P3 expected=unsupported observed=unsupported source=lib/primary.md at=- verdict=match' \
    'CLAIM id=P4 expected=supported observed=supported source=claimsrc/arrow.md at=line:1 verdict=match'

  tclaims claims-fail-tampered 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_SPAN_NOT_FOUND' \
    'nearest_line=1' 'context=line1 primary material' \
    'observed=unsupported' 'VERDICT_BEARING_CLAIMS=0/1'

  tclaims claims-fail-out-of-corpus 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_SOURCE_OUT_OF_CORPUS severity=crit' \
    'observed=refused' 'VERDICT_BEARING_CLAIMS=0/2'

  tclaims claims-fail-external 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_SOURCE_EXTERNAL severity=crit' \
    'VERDICT_BEARING_CLAIMS=0/1'

  tclaims claims-fail-session 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_SOURCE_SESSION severity=crit' \
    'VERDICT_BEARING_CLAIMS=0/1'

  tclaims claims-fail-contradicted-unmarked 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CONTRADICTION_MARKER_ABSENT' \
    'no marker defined (per-claim or marker_default)' \
    'declared marker not found within span lines' \
    'observed=unproven' 'VERDICT_BEARING_CLAIMS=0/2' \
    'claims=2 supported=0 contradicted=0 unsupported=0 mismatched=2 unproven=2 refused=0 invalid=0'

  # A marker on a non-contradicted entry is a fixture violation (drift), and
  # the counting rule is the observable: N matched of M read, with the exact
  # per-disposition counters in the closing summary (directive lines, comments
  # and blanks are not claims).
  tclaims claims-fail-stray-marker 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_RECORD_INVALID' \
    'marker present but expect=supported (fixture violation)' \
    'observed=invalid' 'VERDICT_BEARING_CLAIMS=0/1'

  tclaims claims-fail-counting 1 \
    'VERDICT_BEARING_CLAIMS=3/6' \
    'claims=6 supported=1 contradicted=1 unsupported=2 mismatched=1 unproven=0 refused=1 invalid=1' \
    'FINDING CLAIM_RECORD_INVALID' 'not a JSON object'

  tsetup claims-no-path 2 verify-claims
  tsetup claims-missing-file 2 verify-claims "$WORK/no-such-claims.jsonl"

  # Chain mode cases: the citation of every resolved hop is resolved against the
  # real target (heading text, verbatim quote, whole line); unresolved/marked
  # hops stay exempt but are counted.
  write_rec chain-pass <<'EOF'
# research-record v1
## Meta
| key | value |
|---|---|
| window | loopback |
## Question
Do cited chain hops resolve to real corpus locations?
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/chain_target.md |
| S2 | secondary | lib/primary.md:1 |
| K1 | secondary | lib/primary.md |
## Chain
| hop | from | to | status | anchor_kind | anchor | notes |
|---|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | heading | Term table | direct |
| 2 | C1 | S1 | resolved | quote | alpha row present | direct |
| 3 | C1 | lib/chain_target.md#line:omega final line | resolved | | | inline fragment |
| 4 | C1 | S2 | resolved | quote | line1 primary material | via source id |
| 5 | C1 | https://example.invalid/x | unresolved | | | blocked-no-fetch |
| 6 | C1 | K1 | resolved | line | line2 | non-S declared id |
EOF
  tchain chain-pass 0 \
    'RESEARCH_GATE: CLEAN' 'RESOLVED_HOPS=5/6' \
    'hops=6 verified=5 exempt=1 anchor-missing=0 refused=0 invalid=0' \
    'CHAIN hop=1 status=resolved observed=verified source=lib/chain_target.md anchor=heading:"Term table" at=line:3 verdict=match' \
    'CHAIN hop=2 status=resolved observed=verified source=lib/chain_target.md anchor=quote:"alpha row present" at=line:4 verdict=match' \
    'CHAIN hop=3 status=resolved observed=verified source=lib/chain_target.md anchor=line:"omega final line" at=line:6 verdict=match' \
    'CHAIN hop=4 status=resolved observed=verified source=lib/primary.md anchor=quote:"line1 primary material" at=line:1 verdict=match' \
    'CHAIN hop=5 status=unresolved observed=exempt source=https://example.invalid/x anchor=- at=- verdict=exempt' \
    'CHAIN hop=6 status=resolved observed=verified source=lib/primary.md anchor=line:"line2" at=line:2 verdict=match'

  write_rec chain-fail-tampered <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/chain_target.md |
## Chain
| hop | from | to | status | anchor_kind | anchor |
|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | quote | alpha row present but wrong |
EOF
  tchain chain-fail-tampered 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CHAIN_ANCHOR_NOT_FOUND' \
    'nearest_line=4' 'context=alpha row present' \
    'observed=anchor-missing' 'at=-' 'RESOLVED_HOPS=0/1' \
    'hops=1 verified=0 exempt=0 anchor-missing=1 refused=0 invalid=0 findings=1 drift=1'

  write_rec chain-fail-anchor-kinds <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/chain_target.md |
## Chain
| hop | from | to | status | anchor_kind | anchor |
|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | heading | Missing heading |
| 2 | C1 | S1 | resolved | line | not a real line |
EOF
  tchain chain-fail-anchor-kinds 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CHAIN_ANCHOR_NOT_FOUND' \
    'anchor=heading:"Missing heading"' 'anchor=line:"not a real line"' \
    'nearest_line=-' 'RESOLVED_HOPS=0/2' \
    'hops=2 verified=0 exempt=0 anchor-missing=2 refused=0 invalid=0 findings=2 drift=2'

  printf '# research-record v1\n## Chain\n| hop | from | to | status | anchor_kind | anchor |\n|---|---|---|---|---|---|\n| 1 | C1 | %s | resolved | quote | outside text |\n| 2 | C1 | ../%s | resolved | quote | outside text |\n' \
    "$OUTSIDE_FILE" "$(basename "$OUTSIDE_FILE")" >"$WORK/chain-fail-out-of-corpus.md"
  tchain chain-fail-out-of-corpus 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CHAIN_SOURCE_OUT_OF_CORPUS severity=crit' \
    'observed=refused' 'RESOLVED_HOPS=0/2' \
    'hops=2 verified=0 exempt=0 anchor-missing=0 refused=2 invalid=0 findings=2 drift=2'

  write_rec chain-fail-external <<'EOF'
# research-record v1
## Chain
| hop | from | to | status | anchor_kind | anchor |
|---|---|---|---|---|---|
| 1 | C1 | https://example.invalid/x | resolved | quote | remote text |
EOF
  tchain chain-fail-external 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CHAIN_SOURCE_EXTERNAL severity=crit' \
    'url source refused (no external fetch)' 'RESOLVED_HOPS=0/1'

  write_rec chain-fail-invalid <<'EOF'
# research-record v1
## Chain
| hop | from | to | status | anchor_kind | anchor |
|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | | |
| 2 | C1 | S1 | resolved | slug | Heading text |
| 3 | C1 | S1 | pending | | |
EOF
  tchain chain-fail-invalid 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CHAIN_CITATION_INVALID' \
    'resolved hop missing anchor' 'anchor_kind=slug not in heading|quote|line' \
    'status=pending not in allowed set' 'observed=invalid' \
    'RESOLVED_HOPS=0/3' 'hops=3 verified=0 exempt=0 anchor-missing=0 refused=0 invalid=3 findings=3 drift=3'

  printf '# research-record v1\n## Sources\n| id | tier | pointer |\n|---|---|---|\n| S1 | primary | lib/chain_target.md |\n## Chain\n| hop | from | to | status | anchor_kind | anchor |\n|---|---|---|---|---|---|\n| 1 | C1 | S1 | resolved | heading | Term table |\n| 2 | C1 | S1 | resolved | quote | alpha row present |\n| 3 | C1 | S1 | unresolved | | |\n| 4 | C1 | S1 | labelled-dead | | |\n| 5 | C1 | S1 | resolved | quote | alpha row present but wrong |\n| 6 | C1 | %s | resolved | quote | outside text |\n| 7 | C1 | S1 | resolved | | |\n| 8 | C1 | S1 | pending | | |\n' \
    "$OUTSIDE_FILE" >"$WORK/chain-fail-counting.md"
  tchain chain-fail-counting 1 \
    'RESOLVED_HOPS=2/8' \
    'hops=8 verified=2 exempt=2 anchor-missing=1 refused=1 invalid=2 findings=4 drift=4' \
    'observed=exempt' 'FINDING CHAIN_ANCHOR_NOT_FOUND' 'FINDING CHAIN_SOURCE_OUT_OF_CORPUS' \
    'FINDING CHAIN_CITATION_INVALID' 'FINDING CHAIN_CITATION_INVALID'

  write_rec chain-fail-no-chain <<'EOF'
# research-record v1
## Question
Is there a chain to resolve?
EOF
  tchain chain-fail-no-chain 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CHAIN_ABSENT' \
    'RESOLVED_HOPS=0/0' 'hops=0 verified=0 exempt=0 anchor-missing=0 refused=0 invalid=0 findings=1 drift=1'

  tsetup chain-no-path 2 verify-chain
  tsetup chain-missing-file 2 verify-chain "$WORK/no-such-record.md"

  # Round-4 token-boundary cases. The claims pair and the chain pair run the
  # same fixture bytes (lib/boundary.md) through both modes, so the delimited
  # passes (punctuation edge, non-word-internal hyphen, line edge, multi-line
  # span) and the glued misses (mid-token truncation, padded extra word into a
  # hyphenated compound, possessive apostrophe) are evidence that one rule
  # governs both modes.
  tclaims claims-boundary-pass 0 \
    'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=4/4' \
    'CLAIM id=BP1 expected=supported observed=supported source=lib/boundary.md at=line:1 verdict=match' \
    'CLAIM id=BP2 expected=supported observed=supported source=lib/boundary.md at=line:2 verdict=match' \
    'CLAIM id=BP3 expected=supported observed=supported source=lib/primary.md at=line:2 verdict=match' \
    'CLAIM id=BP4 expected=supported observed=supported source=lib/primary.md at=lines:1-2 verdict=match'

  tclaims claims-boundary-fail 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_SPAN_NOT_FOUND' \
    'CLAIM id=BF1 expected=supported observed=unsupported source=lib/boundary.md at=- verdict=mismatch' \
    'CLAIM id=BF2 expected=supported observed=unsupported source=lib/boundary.md at=- verdict=mismatch' \
    'CLAIM id=BF3 expected=supported observed=unsupported source=lib/boundary.md at=- verdict=mismatch' \
    'nearest_line=1' 'nearest_line=4' 'nearest_line=3' 'VERDICT_BEARING_CLAIMS=0/3' \
    'claims=3 supported=0 contradicted=0 unsupported=3 mismatched=3 unproven=0 refused=0 invalid=0'

  write_rec chain-pass-boundary <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/boundary.md |
## Chain
| hop | from | to | status | anchor_kind | anchor |
|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | quote | alpha boundary word |
| 2 | C1 | S1 | resolved | quote | delta boundary word |
| 3 | C1 | lib/primary.md#line:line2 | resolved | | |
EOF
  tchain chain-pass-boundary 0 \
    'RESEARCH_GATE: CLEAN' 'RESOLVED_HOPS=3/3' \
    'hops=3 verified=3 exempt=0 anchor-missing=0 refused=0 invalid=0' \
    'CHAIN hop=1 status=resolved observed=verified source=lib/boundary.md anchor=quote:"alpha boundary word" at=line:1 verdict=match' \
    'CHAIN hop=2 status=resolved observed=verified source=lib/boundary.md anchor=quote:"delta boundary word" at=line:2 verdict=match' \
    'CHAIN hop=3 status=resolved observed=verified source=lib/primary.md anchor=line:"line2" at=line:2 verdict=match'

  write_rec chain-fail-boundary <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/boundary.md |
## Chain
| hop | from | to | status | anchor_kind | anchor |
|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | quote | alpha boundary wor |
| 2 | C1 | S1 | resolved | quote | theta boundary word continuation |
| 3 | C1 | S1 | resolved | quote | gamma boundary word |
EOF
  tchain chain-fail-boundary 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CHAIN_ANCHOR_NOT_FOUND' \
    'observed=anchor-missing' 'at=-' 'RESOLVED_HOPS=0/3' \
    'nearest_line=1' 'nearest_line=4' 'nearest_line=3' \
    'hops=3 verified=0 exempt=0 anchor-missing=3 refused=0 invalid=0 findings=3 drift=3'

  # Round-5 sweeps cases. The parked target lib/planted-ghost.md is created here,
  # after every r1-r4 case has already run, so the four earlier suites are
  # untouched by it; the empty sweeps name lib/ghost*.md, which every case
  # keeps empty.
  printf 'planted material\n' >"$WORK/lib/planted-ghost.md"

  write_rec sweeps-pass <<'EOF'
# research-record v1
<!-- chousa-record: v1 -->
## Meta
| key | value |
|---|---|
| window | loopback |
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Sweeps
| id | claim_id | where | status |
|---|---|---|---|
| SW1 | N1 | lib/ghost*.md | swept |
| SW2 | N2 | https://example.invalid/archive | swept |
| SW3 | N3 | S1 | swept |
| SW4 | N4 | | blocked-no-fetch |
## Negatives
| id | text | sweep | status |
|---|---|---|---|
| N1 | no fx-only ghost source | lib/ghost*.md | swept |
| N2 | no upstream dictionary attestation | https://example.invalid/ | blocked-no-fetch |
| N3 | no counterexample inside the primary | S1 | swept |
## Rejections
| id | ref | reason | flip |
|---|---|---|---|
| R1 | noise/chat-export-sources.md | UI chrome is not a primary source | a primary attestation in that file would flip this |
EOF
  tsweeps sweeps-pass 0 \
    'RESEARCH_GATE: CLEAN' \
    'VERIFIED_SWEEPS=1/4 REJECTIONS_OK=1/1' \
    'SWEEP id=SW1 where=lib/ghost*.md looked=local hits=0 at=- observed=verified verdict=match' \
    'SWEEP id=SW2 where=https://example.invalid/archive looked=non-local hits=- at=- observed=exempt verdict=exempt' \
    'SWEEP id=SW3 where=S1 looked=source-ids hits=- at=- observed=exempt verdict=exempt' \
    'SWEEP id=SW4 where=- looked=exempt hits=- at=- observed=exempt verdict=exempt' \
    'REJECTION id=R1 ref=noise/chat-export-sources.md reason=present flip=present observed=complete verdict=match' \
    'sweeps=4 verified=1 exempt=3 hit=0 refused=0 invalid=0 rejections=1 rejections-ok=1 findings=0 drift=0'

  write_rec sweeps-fail-planted-hit <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Sweeps
| id | claim_id | where | status |
|---|---|---|---|
| SW1 | N1 | lib/planted*.md | swept |
## Rejections
| id | ref | reason | flip |
|---|---|---|---|
| R1 | (none) | no source was rejected | a source row appearing would flip this |
EOF
  tsweeps sweeps-fail-planted-hit 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING SWEEP_CLAIM_FALSE severity=warn' \
    'first=lib/planted-ghost.md' \
    'SWEEP id=SW1 where=lib/planted*.md looked=local hits=1 at=lib/planted-ghost.md observed=hit verdict=mismatch' \
    'VERIFIED_SWEEPS=0/1 REJECTIONS_OK=1/1'

  write_rec sweeps-fail-rejection-incomplete <<'EOF'
# research-record v1
## Rejections
| id | ref | reason | flip |
|---|---|---|---|
| R1 | noise/a.md | reason recorded here | |
| R2 | noise/b.md | | a fresh attestation would flip this |
EOF
  tsweeps sweeps-fail-rejection-incomplete 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING SWEEP_REJECTION_INCOMPLETE severity=warn' \
    'missing=flip' 'missing=reason' \
    'REJECTION id=R1 ref=noise/a.md reason=present flip=absent observed=incomplete verdict=mismatch' \
    'REJECTION id=R2 ref=noise/b.md reason=absent flip=present observed=incomplete verdict=mismatch' \
    'VERIFIED_SWEEPS=0/0 REJECTIONS_OK=0/2'

  write_rec sweeps-fail-unnamed <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Sweeps
| id | claim_id | where | status |
|---|---|---|---|
| SW1 | N1 | | swept |
## Rejections
| id | ref | reason | flip |
|---|---|---|---|
| R1 | (none) | no source was rejected | a source row appearing would flip this |
EOF
  tsweeps sweeps-fail-unnamed 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING SWEEP_LOCATION_ABSENT severity=warn' \
    'SWEEP id=SW1 where=- looked=unnamed hits=- at=- observed=invalid verdict=invalid' \
    'VERIFIED_SWEEPS=0/1 REJECTIONS_OK=1/1'

  printf '# research-record v1\n## Sweeps\n| id | claim_id | where |\n|---|---|---|\n| SW1 | N1 | ../%s |\n## Rejections\n| id | ref | reason | flip |\n|---|---|---|---|\n| R1 | (none) | no source was rejected | a source row appearing would flip this |\n' \
    "$(basename "$OUTSIDE_FILE")" >"$WORK/sweeps-fail-out-of-corpus.md"
  tsweeps sweeps-fail-out-of-corpus 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING SWEEP_LOCATION_OUT_OF_CORPUS severity=crit' \
    'observed=refused verdict=refused' 'VERIFIED_SWEEPS=0/1 REJECTIONS_OK=1/1'

  write_rec sweeps-fail-unresolved-id <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Sweeps
| id | claim_id | where |
|---|---|---|
| SW1 | N1 | S7 |
## Rejections
| id | ref | reason | flip |
|---|---|---|---|
| R1 | (none) | no source was rejected | a source row appearing would flip this |
EOF
  tsweeps sweeps-fail-unresolved-id 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING SWEEP_LOCATION_UNRESOLVED severity=warn' \
    'source_id=S7 not in ## Sources' \
    'SWEEP id=SW1 where=S7 looked=source-ids hits=- at=- observed=refused verdict=refused' \
    'VERIFIED_SWEEPS=0/1 REJECTIONS_OK=1/1'

  write_rec sweeps-fail-counting <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Sweeps
| id | claim_id | where | status |
|---|---|---|---|
| SW1 | N1 | lib/ghost*.md | swept |
| SW2 | N2 | lib/planted*.md | swept |
| SW3 | N3 | https://example.invalid/ | swept |
| SW4 | N4 | S1 | swept |
| SW5 | N5 | | swept |
## Rejections
| id | ref | reason | flip |
|---|---|---|---|
| R1 | (none) | no source was rejected | a new source row would flip this |
| R2 | (none) | no source was rejected | |
| R3 | (none) | | a new source row would flip this |
EOF
  tsweeps sweeps-fail-counting 1 \
    'VERIFIED_SWEEPS=1/5 REJECTIONS_OK=1/3' \
    'sweeps=5 verified=1 exempt=2 hit=1 refused=0 invalid=1 rejections=3 rejections-ok=1 findings=4 drift=4' \
    'FINDING SWEEP_CLAIM_FALSE' 'FINDING SWEEP_LOCATION_ABSENT' \
    'FINDING SWEEP_REJECTION_INCOMPLETE'

  write_rec sweeps-pass-cell-command <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Negatives
| id | text | sweep | status |
|---|---|---|---|
| N1 | no fx-only ghost source | `test ! -f lib/ghost.md` | swept |
## Rejections
| id | ref | reason | flip |
|---|---|---|---|
| R1 | (none) | no source was rejected | a new source row would flip this |
EOF
  tsweeps sweeps-pass-cell-command 0 \
    'RESEARCH_GATE: CLEAN' \
    'SWEEP id=N1 where=lib/ghost.md looked=local hits=0 at=- observed=verified verdict=match' \
    'VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1'

  tsetup sweeps-no-path 2 verify-sweeps
  tsetup sweeps-missing-file 2 verify-sweeps "$WORK/no-such-record.md"

  # verify-all composition cases (r6): fresh-process CLI, one composed
  # RESEARCH_GATE line and one VERIFY_ALL line per run. CLAIMS/JSON are '-' or
  # names under WORK. With a manifest, WANT_JLINES lines must parse (python3
  # when present) and carry the schema and both SHA fields; the first line's
  # hash is memoized so the append run proves line 1 is never rewritten.
  write_rec all-pass <<'EOF'
# research-record v1
<!-- chousa-record: v1 -->
## Meta
| key | value |
|---|---|
| window | loopback |
| fetch | none |
## Question
Does this fixture pass every applicable mode when composed as one verdict?
## Sources
| id | tier | pointer | notes |
|---|---|---|---|
| S1 | primary | lib/primary.md:1 | local fixture |
## Chain
| hop | from | to | status | anchor_kind | anchor | notes |
|---|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | quote | line1 primary material | direct |
| 2 | C1 | S1 | unresolved | | | blocked-no-fetch |
## Claims
| id | kind | text | pointer | status | sweep |
|---|---|---|---|---|---|
| C1 | observation | primary file has line1 | lib/primary.md:1 | verified | |
## Sweeps
| id | claim_id | where | status |
|---|---|---|---|
| SW1 | C1 | lib/ghost*.md | swept |
## Rejections
| id | ref | reason | flip |
|---|---|---|---|
| R1 | noise/chat-export-sources.md | UI chrome is not a primary source | a primary attestation in that file would flip this |
## Approval
| target | state |
|---|---|
| (none) | not-required |
EOF
  write_rec all-structure <<'EOF'
# research-record v1
## Meta
| key | value |
|---|---|
| window | loopback |
## Sources
| id | tier | pointer | notes |
|---|---|---|---|
| S1 | primary | lib/primary.md:1 | local fixture |
## Chain
| hop | from | to | status | anchor_kind | anchor | notes |
|---|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | quote | line1 primary material | direct |
## Claims
| id | kind | text | pointer | status | sweep |
|---|---|---|---|---|---|
| C1 | observation | primary file has line1 | lib/primary.md:1 | verified | |
## Sweeps
| id | claim_id | where | status |
|---|---|---|---|
| SW1 | C1 | lib/ghost*.md | swept |
## Rejections
| id | ref | reason | flip |
|---|---|---|---|
| R1 | noise/chat-export-sources.md | UI chrome is not a primary source | a primary attestation in that file would flip this |
EOF

  local TALL_JSON_H1=''
  tall() { # INPUT WANT_RC WANT_NV WANT_NS CLAIMS|- JSON|- WANT_JLINES|- [tokens…]
    local input=$1 want_rc=$2 want_nv=$3 want_ns=$4 claims=$5 json=$6 want_jl=$7
    shift 7
    local -a want=() over=() extra=()
    local a rc=0 out nverdict nsum ok=1 msg='' tok n h1
    for a in "$@"; do
      if [[ $a =~ ^CHOUSA_[A-Z_]+= ]]; then over+=("$a"); else want+=("$a"); fi
    done
    cases=$((cases + 1))
    if [[ $claims != - ]]; then extra+=(--claims "$WORK/$claims"); fi
    if [[ $json != - ]]; then extra+=(--json "$WORK/$json"); fi
    out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 \
      CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
      "${over[@]+"${over[@]}"}" \
      bash "$SELF" verify-all "$WORK/$input" "${extra[@]+"${extra[@]}"}" 2>&1) || rc=$?
    nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true)
    nsum=$(grep -c '^VERIFY_ALL ' <<<"$out" || true)
    if [[ $rc -ne $want_rc ]]; then ok=0; msg+="rc=$rc/$want_rc "; fi
    if [[ ${nverdict:-0} -ne $want_nv ]]; then ok=0; msg+="verdicts=$nverdict/$want_nv "; fi
    if [[ ${nsum:-0} -ne $want_ns ]]; then ok=0; msg+="sums=$nsum/$want_ns "; fi
    for tok in "${want[@]+"${want[@]}"}"; do
      if [[ $out != *"$tok"* ]]; then ok=0; msg+="missing:'$tok' "; fi
    done
    if [[ $json != - ]]; then
      n=$(wc -l <"$WORK/$json" 2>/dev/null | tr -d ' ' || true)
      if [[ ${n:-0} -ne $want_jl ]]; then ok=0; msg+="manifest-lines=${n:-0}/$want_jl "; fi
      if command -v python3 >/dev/null 2>&1; then
        python3 -c 'import json,sys
for ln in sys.stdin.read().splitlines():
    if ln.strip():
        json.loads(ln)' <"$WORK/$json" >/dev/null 2>&1 || { ok=0; msg+="json-invalid "; }
      fi
      grep -q '"schema":"chousa-verify-all/v1"' -- "$WORK/$json" || { ok=0; msg+="schema-absent "; }
      grep -qE '"record_sha256":"[0-9a-f]{64}"' -- "$WORK/$json" || { ok=0; msg+="record-sha-absent "; }
      grep -qE '"gate_sha256":"[0-9a-f]{64}"' -- "$WORK/$json" || { ok=0; msg+="gate-sha-absent "; }
      grep -q '"verdict":"CLEAN"' -- "$WORK/$json" || { ok=0; msg+="verdict-field "; }
      h1=$(sed -n 1p -- "$WORK/$json" | sha256sum | cut -d' ' -f1)
      if [[ -n $TALL_JSON_H1 ]]; then
        if [[ $h1 != "$TALL_JSON_H1" ]]; then ok=0; msg+="line1-rewritten "; fi
      else
        TALL_JSON_H1=$h1
      fi
    fi
    if [[ $ok -eq 1 ]]; then
      printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" "$input" "$rc"
    else
      printf 'FAIL-case %-28s %s\n' "$input" "$msg"
      printf '%s\n' "$out" | sed 's/^/    | /'
      failures=$((failures + 1))
    fi
  }

  tall all-pass.md 0 1 1 claims-pass.jsonl - - \
    'RESEARCH_GATE: CLEAN' \
    'SECTION structure state=run verdict=CLEAN findings=0 drift=0' \
    'SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=4/4' \
    'SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=1/2' \
    'SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1' \
    'SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=5 resolved=3 unresolved=0' \
    'VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0'

  tall all-pass.md 1 1 1 claims-fail-tampered.jsonl - - \
    'RESEARCH_GATE: DRIFT' \
    'SECTION claims state=run verdict=DRIFT' \
    'FINDING CLAIM_SPAN_NOT_FOUND' \
    'SECTION structure state=run verdict=CLEAN' \
    'SECTION chain state=run verdict=CLEAN' \
    'SECTION sweeps state=run verdict=CLEAN' \
    'VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1'

  tall all-structure.md 1 1 1 claims-pass.jsonl - - \
    'RESEARCH_GATE: DRIFT' \
    'SECTION structure state=run verdict=DRIFT' \
    'FINDING NO_QUESTION' \
    'SECTION claims state=run verdict=CLEAN' \
    'SECTION chain state=run verdict=CLEAN' \
    'SECTION sweeps state=run verdict=CLEAN' \
    'VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1'

  tall all-pass.md 0 1 1 - - - \
    'RESEARCH_GATE: CLEAN' \
    'SECTION claims state=absent' \
    'SECTION structure state=run verdict=CLEAN' \
    'SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=5 resolved=3 unresolved=0' \
    'VERIFY_ALL sections=5 run=4 absent=1 drift-sections=0 findings=0 drift=0'

  tall claims-pass.jsonl 0 1 1 - - - \
    'RESEARCH_GATE: CLEAN' \
    'SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=4/4' \
    'SECTION structure state=absent' \
    'SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=0 resolved=0 unresolved=0' \
    'VERIFY_ALL sections=5 run=2 absent=3 drift-sections=0 findings=0 drift=0'

  tall all-pass.md 0 1 1 claims-pass.jsonl r6-manifest.jsonl 1 \
    'RESEARCH_GATE: CLEAN'
  tall all-pass.md 0 1 1 claims-pass.jsonl r6-manifest.jsonl 2 \
    'RESEARCH_GATE: CLEAN'

  # Meta-declared claims binding (r6): the record names its claims surface in
  # ## Meta (| claims | PATH |); a declaration that cannot resolve under the
  # corpus boundary is VERIFY_ALL_CLAIMS_UNRESOLVED and drifts the section.
  sed 's;| fetch | none |;| fetch | none |\n| claims | claims-pass.jsonl |;' \
    "$WORK/all-pass.md" >"$WORK/all-meta.md"
  sed 's;| fetch | none |;| fetch | none |\n| claims | no-such-claims.jsonl |;' \
    "$WORK/all-pass.md" >"$WORK/all-meta-missing.md"
  tall all-meta.md 0 1 1 - - - \
    'RESEARCH_GATE: CLEAN' \
    'SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=4/4' \
    'VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0'
  tall all-meta-missing.md 1 1 1 - - - \
    'RESEARCH_GATE: DRIFT' \
    'SECTION claims state=run verdict=DRIFT' \
    'FINDING VERIFY_ALL_CLAIMS_UNRESOLVED' \
    'VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1'

  tall no-such-record.md 2 0 0 - - -

  # Integrity cases (r7): cross-section references resolve to declared rows or
  # drift. Appended after the r6 cases so cases 1-64 keep their case numbers,
  # names and exits; the r6 composition expectations above advanced 4 → 5
  # sections because integrity is genuinely composed there now.
  write_rec integrity-pass <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
| S2 | secondary | lib/primary.md:2 |
## Chain
| hop | from | to | status | anchor_kind | anchor |
|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | quote | line1 primary material |
## Claims
| id | kind | text | pointer | status | sweep |
|---|---|---|---|---|---|
| C1 | observation | primary file has line1 | lib/primary.md:1 | verified | SW1 |
## Negatives
| id | text | sweep | status |
|---|---|---|---|
| N1 | no fx-only ghost source | SW1 | swept |
## Sweeps
| id | claim_id | where | status |
|---|---|---|---|
| SW1 | C1 | lib/ghost*.md | swept |
| SW2 | N1 | S1,S2 | swept |
## Rejections
| id | ref | reason | flip |
|---|---|---|---|
| R1 | lib/ghost*.md | no source was rejected | a new source row would flip this |
EOF
  tintegrity integrity-pass 0 \
    'RESEARCH_GATE: CLEAN' 'INTEGRITY refs=8 resolved=8 unresolved=0' \
    'REF kind=claim id=C1 section=chain row=1 cell=from observed=resolved verdict=match' \
    'REF kind=source id=S1 section=chain row=1 cell=to observed=resolved verdict=match' \
    'REF kind=sweep id=SW1 section=claims row=C1 cell=sweep observed=resolved verdict=match' \
    'REF kind=sweep id=SW1 section=negatives row=N1 cell=sweep observed=resolved verdict=match' \
    'REF kind=claim id=C1 section=sweeps row=SW1 cell=claim_id observed=resolved verdict=match' \
    'REF kind=claim id=N1 section=sweeps row=SW2 cell=claim_id observed=resolved verdict=match' \
    'REF kind=source id=S2 section=sweeps row=SW2 cell=where observed=resolved verdict=match' \
    'RESEARCH_GATE: CLEAN (refs=8 resolved=8 unresolved=0 exempt=0 findings=0 drift=0)'

  write_rec integrity-fail-dangling-claim <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Sweeps
| id | claim_id | where | status |
|---|---|---|---|
| SW1 | C9 | lib/ghost*.md | swept |
EOF
  tintegrity integrity-fail-dangling-claim 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING REF_UNRESOLVED severity=warn' \
    'obs=kind=claim id=C9 section=sweeps row=SW1 cell=claim_id' \
    'REF kind=claim id=C9 section=sweeps row=SW1 cell=claim_id observed=unresolved verdict=mismatch' \
    'INTEGRITY refs=1 resolved=0 unresolved=1' \
    'RESEARCH_GATE: DRIFT (refs=1 resolved=0 unresolved=1 exempt=0 findings=1 drift=1)'

  write_rec integrity-fail-dangling-source <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Chain
| hop | from | to | status | anchor_kind | anchor |
|---|---|---|---|---|---|
| 1 | S1 | S1 | resolved | quote | line1 primary material |
## Rejections
| id | ref | reason | flip |
|---|---|---|---|
| R1 | S7 | rejected a source id no ## Sources row declares | a declared source row would flip this |
EOF
  tintegrity integrity-fail-dangling-source 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING REF_UNRESOLVED severity=warn' \
    'obs=kind=source id=S7 section=rejections row=R1 cell=ref' \
    'REF kind=source id=S7 section=rejections row=R1 cell=ref observed=unresolved verdict=mismatch' \
    'INTEGRITY refs=3 resolved=2 unresolved=1' \
    'RESEARCH_GATE: DRIFT (refs=3 resolved=2 unresolved=1 exempt=0 findings=1 drift=1)'

  write_rec integrity-fail-dangling-chain-claim <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Chain
| hop | from | to | status | anchor_kind | anchor |
|---|---|---|---|---|---|
| 1 | C9 | S1 | resolved | quote | line1 primary material |
EOF
  tintegrity integrity-fail-dangling-chain-claim 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING REF_UNRESOLVED severity=warn' \
    'obs=kind=claim id=C9 section=chain row=1 cell=from' \
    'REF kind=claim id=C9 section=chain row=1 cell=from observed=unresolved verdict=mismatch' \
    'INTEGRITY refs=2 resolved=1 unresolved=1'

  write_rec integrity-fail-dangling-sweep <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Claims
| id | kind | text | pointer | status | sweep |
|---|---|---|---|---|---|
| C1 | observation | primary file has line1 | lib/primary.md:1 | verified | SW9 |
## Sweeps
| id | claim_id | where | status |
|---|---|---|---|
| SW1 | C1 | lib/ghost*.md | swept |
EOF
  tintegrity integrity-fail-dangling-sweep 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING REF_UNRESOLVED severity=warn' \
    'obs=kind=sweep id=SW9 section=claims row=C1 cell=sweep' \
    'REF kind=sweep id=SW9 section=claims row=C1 cell=sweep observed=unresolved verdict=mismatch' \
    'INTEGRITY refs=2 resolved=1 unresolved=1'

  write_rec integrity-exempt-counted <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Chain
| hop | from | to | status | anchor_kind | anchor |
|---|---|---|---|---|---|
| 1 | C9 | S7 | blocked-no-fetch | | |
## Sweeps
| id | claim_id | where | status |
|---|---|---|---|
| SW1 | S1 | https://example.invalid/archive | swept |
EOF
  tintegrity integrity-exempt-counted 0 \
    'RESEARCH_GATE: CLEAN' 'INTEGRITY refs=4 resolved=1 unresolved=0' \
    'REF kind=claim id=C9 section=chain row=1 cell=from observed=exempt verdict=exempt status=blocked-no-fetch' \
    'REF kind=source id=S7 section=chain row=1 cell=to observed=exempt verdict=exempt status=blocked-no-fetch' \
    'REF kind=source id=S1 section=sweeps row=SW1 cell=claim_id observed=resolved verdict=match' \
    'REF kind=location id=https://example.invalid/archive section=sweeps row=SW1 cell=where observed=exempt verdict=exempt reason=non-local' \
    'RESEARCH_GATE: CLEAN (refs=4 resolved=1 unresolved=0 exempt=3 findings=0 drift=0)'

  write_rec integrity-fail-counting <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Chain
| hop | from | to | status | anchor_kind | anchor |
|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | quote | line1 primary material |
| 2 | C9 | S7 | unresolved | | |
## Claims
| id | kind | text | pointer | status | sweep |
|---|---|---|---|---|---|
| C1 | observation | primary file has line1 | lib/primary.md:1 | verified | |
## Negatives
| id | text | sweep | status |
|---|---|---|---|
| N2 | no fx-only ghost source | SW1 | swept |
## Sweeps
| id | claim_id | where | status |
|---|---|---|---|
| SW1 | N7 | lib/ghost*.md | swept |
| SW2 | C1 | https://example.invalid/archive | swept |
## Rejections
| id | ref | reason | flip |
|---|---|---|---|
| R1 | S9 | rejected an undeclared source id | a declared source row would flip this |
EOF
  tintegrity integrity-fail-counting 1 \
    'RESEARCH_GATE: DRIFT' \
    'INTEGRITY refs=9 resolved=4 unresolved=2' \
    'RESEARCH_GATE: DRIFT (refs=9 resolved=4 unresolved=2 exempt=3 findings=2 drift=2)' \
    'obs=kind=claim id=N7 section=sweeps row=SW1 cell=claim_id' \
    'obs=kind=source id=S9 section=rejections row=R1 cell=ref' \
    'REF kind=claim id=C9 section=chain row=2 cell=from observed=exempt verdict=exempt status=unresolved'

  tsetup integrity-no-path 2 verify-integrity
  tsetup integrity-missing-file 2 verify-integrity "$WORK/no-such-record.md"

  # Composed inclusion (r7): a record the four r6 sections all call CLEAN but
  # whose sweep binding dangles composes DRIFT through the integrity section
  # alone — the r6-omission demonstration, now named.
  write_rec all-dangling <<'EOF'
# research-record v1
<!-- chousa-record: v1 -->
## Meta
| key | value |
|---|---|
| window | loopback |
| fetch | none |
## Question
Does a dangling sweep binding drift a composed verdict the four r6 sections pass?
## Sources
| id | tier | pointer | notes |
|---|---|---|---|
| S1 | primary | lib/primary.md:1 | local fixture |
## Chain
| hop | from | to | status | anchor_kind | anchor | notes |
|---|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | quote | line1 primary material | direct |
## Claims
| id | kind | text | pointer | status | sweep |
|---|---|---|---|---|---|
| C1 | observation | primary file has line1 | lib/primary.md:1 | verified | |
## Negatives
| id | text | sweep | status |
|---|---|---|---|
| N1 | no fx-only ghost source | SW1 | swept |
## Sweeps
| id | claim_id | where | status |
|---|---|---|---|
| SW1 | C9 | lib/ghost*.md | swept |
## Rejections
| id | ref | reason | flip |
|---|---|---|---|
| R1 | noise/chat-export-sources.md | UI chrome is not a primary source | a primary attestation in that file would flip this |
## Approval
| target | state |
|---|---|
| (none) | not-required |
EOF
  tall all-dangling.md 1 1 1 claims-pass.jsonl - - \
    'RESEARCH_GATE: DRIFT' \
    'SECTION integrity state=run verdict=DRIFT findings=1 drift=1 tally=INTEGRITY refs=4 resolved=3 unresolved=1' \
    'FINDING REF_UNRESOLVED severity=warn' \
    'obs=kind=claim id=C9 section=sweeps row=SW1 cell=claim_id' \
    'SECTION structure state=run verdict=CLEAN' \
    'SECTION claims state=run verdict=CLEAN' \
    'SECTION chain state=run verdict=CLEAN' \
    'SECTION sweeps state=run verdict=CLEAN' \
    'VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1'

  # Pin/drift cases (r8): the gate's own behavioral baseline. Appended after
  # the r7 cases so cases 1-74 keep their case numbers, names and exits. Every
  # pin/drift run is a fresh process against the shipped CLI, and each capture
  # runs the canonical invocation (verify-all over the internal hermetic
  # fixture plus its --json manifest line) in its own temp fixture.
  tpin() { # NAME WANT_RC [want-substrings…] — writes $WORK/NAME.baseline
    local name=$1 want_rc=$2
    shift 2
    local -a want=("$@")
    local rc=0 out n ok=1 tok
    cases=$((cases + 1))
    out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_STRICT -u CHOUSA_ROOT \
      -u CHOUSA_AGGREGATOR_ERE CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
      bash "$SELF" --pin "$WORK/$name.baseline" 2>&1) || rc=$?
    n=$(grep -c '^GATE_PIN: ' <<<"$out" || true)
    for tok in "${want[@]+"${want[@]}"}"; do
      [[ $out == *"$tok"* ]] || ok=0
    done
    if [[ $rc -eq $want_rc && ${n:-0} -eq 1 && $ok -eq 1 ]]; then
      printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" "$name" "$rc"
    else
      printf 'FAIL-case %-28s exit=%d want=%d pin-lines=%s token=%s\n' \
        "$name" "$rc" "$want_rc" "${n:-0}" "${want[*]-}"
      printf '%s\n' "$out" | sed 's/^/    | /'
      failures=$((failures + 1))
    fi
  }

  # Drift cases. DRIVER=PATH runs a different copy of the gate (the mutant
  # arm); NAME=VALUE tokens are env overrides; everything else is a required
  # substring. An exit-0/1 run must print exactly one GATE_DRIFT line; an
  # exit-2 run must print none (its reason is the message, asserted by token).
  tdrift() { # NAME WANT_RC BASELINE [DRIVER=PATH] [ENV=VAL…] [want…]
    local name=$1 want_rc=$2 baseline=$3
    shift 3
    local -a want=() over=()
    local a drv="$SELF" rc=0 out n ok=1 tok
    for a in "$@"; do
      case "$a" in
        DRIVER=*) drv=${a#DRIVER=} ;;
        [A-Z_]*=*) over+=("$a") ;;
        *) want+=("$a") ;;
      esac
    done
    cases=$((cases + 1))
    out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_STRICT -u CHOUSA_ROOT \
      -u CHOUSA_AGGREGATOR_ERE CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
      "${over[@]+"${over[@]}"}" \
      bash "$drv" --drift "$baseline" 2>&1) || rc=$?
    n=$(grep -c '^GATE_DRIFT: ' <<<"$out" || true)
    if [[ $want_rc -le 1 ]]; then
      [[ ${n:-0} -eq 1 ]] || ok=0
    else
      [[ ${n:-0} -eq 0 ]] || ok=0
    fi
    for tok in "${want[@]+"${want[@]}"}"; do
      [[ $out == *"$tok"* ]] || ok=0
    done
    if [[ $rc -eq $want_rc && $ok -eq 1 ]]; then
      printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" "$name" "$rc"
    else
      printf 'FAIL-case %-28s exit=%d want=%d drift-lines=%s token=%s\n' \
        "$name" "$rc" "$want_rc" "${n:-0}" "${want[*]-}"
      printf '%s\n' "$out" | sed 's/^/    | /'
      failures=$((failures + 1))
    fi
  }

  # The canonical run itself rolls DRIFT (one integrity finding by design), so
  # this pin also proves the documented rule: pinning a DRIFT run is still a
  # pin (exit 0), the roll lives inside the captured bytes.
  tpin pin-clean 0 'GATE_PIN: ok'
  tdrift drift-clean 0 "$WORK/pin-clean.baseline" 'GATE_DRIFT: none'

  # The volatile contract absorbs real churn: the same fixture re-run with a
  # clock 2 h later moves ts (header and manifest) and nothing else, so the
  # drift is 'none' because the mask says so, not because the run repeats.
  tdrift drift-volatile-churn 0 "$WORK/pin-clean.baseline" \
    CHOUSA_NOW_EPOCH="$((NOW_EPOCH + 7200))" 'GATE_DRIFT: none'

  # A one-field regression in a copy of the gate: the SECTION printers rename
  # findings= to finds= and nothing else changes. The copy runs as the drift
  # driver, so the comparison is behavioral (the copy's gate_sha256 differs
  # and is masked) and the renamed field is named in the report.
  sed 's/state=run verdict=%s findings=%s/state=run verdict=%s finds=%s/' \
    "$SELF" >"$WORK/gate-mutant.sh"
  tdrift drift-one-field-mutant 1 "$WORK/pin-clean.baseline" \
    "DRIVER=$WORK/gate-mutant.sh" '+finds' '-findings'

  # Absence and malformation are exit 2, never a false 'none': a two-valued
  # contract would let cannot-compare masquerade as clean (mori r10 lesson,
  # "The exit contract needs a third value").
  tdrift drift-missing 2 "$WORK/no-such-baseline.txt" 'baseline missing'
  printf 'not a baseline\n' >"$WORK/drift-malformed.baseline"
  tdrift drift-malformed 2 "$WORK/drift-malformed.baseline" 'malformed'

  # A baseline whose declared volatile list differs from the current one is
  # itself drift: the recorded contract is part of what was pinned.
  sed 's/^# volatile_fields=.*/# volatile_fields=ts/' \
    "$WORK/pin-clean.baseline" >"$WORK/drift-vol-list.baseline"
  tdrift drift-volatile-list 1 "$WORK/drift-vol-list.baseline" 'volatile_fields'

  tsetup pin-no-path 2 --pin
  tsetup drift-no-path 2 --drift
  tsetup pin-unwritable 2 --pin "$WORK/no-such-dir/base.txt"
  tsetup pin-drift-exclusive 2 --pin "$WORK/a.txt" --drift "$WORK/b.txt"

  # ---- r12: declared-scope refusal screen (cases 86-92) ----
  # Base record is CLEAN (window loopback, one source/chain/claim/rejection).
  # Each fail fixture adds ONE ## Meta declaration row naming exactly one
  # refused province; the pass fixtures pin both declaration grammars
  # (table row and `key: value` line), prose-not-scanned, and the B-archive
  # vocabulary declared in-province (near-miss). Appended after case 85 so
  # cases 1-85 keep their numbers.
  write_rec scope-base <<'EOF'
# research-record v1
## Meta
| key | value |
|---|---|
| window | loopback |
## Question
Do the local claims resolve?
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Chain
| hop | from | to | status | notes |
|---|---|---|---|---|
| 1 | C1 | S1 | resolved | direct |
## Claims
| id | kind | text | pointer | status |
|---|---|---|---|---|
| C1 | observation | primary file has line1 | S1 | verified |
## Rejections
| id | ref | reason | flip |
|---|---|---|---|
| R1 | n/a | none-recorded | a source row would flip this |
EOF
  printf 'line1 primary material\nline2\n' >"$WORK/lib/primary.md"
  add_scope_row() { sed "s#^| window | loopback |#| window | loopback |\n| $2 | $3 |#" \
    "$WORK/scope-base.md" >"$WORK/$1.md"; }
  add_scope_row scope-fail-bounty domain 'bounty program scope and claim packages'
  add_scope_row scope-fail-model-quality domain 'model-quality evaluation claims'
  add_scope_row scope-fail-orchestration scope 'orchestration and multi-agent dispatch'
  add_scope_row scope-pass-declared-table domain 'deep-research method'
  add_scope_row scope-pass-near-miss domain 'multi-agent knowledge; specialist evaluation of knowledge bases'
  sed "s#^| window | loopback |#| window | loopback |\nscope: deep-research method#" \
    "$WORK/scope-base.md" >"$WORK/scope-pass-declared-line.md"
  sed 's#^Do the local claims resolve?$#Prose decoy: bounty-program scope, model-quality evaluation claims and orchestration/dispatch of agents appear only here in prose, never in a ## Meta declaration row.#' \
    "$WORK/scope-base.md" >"$WORK/scope-pass-prose-decoy.md"
  tcase scope-fail-bounty 1 'RESEARCH_GATE: DRIFT' \
    'FINDING SCOPE_BOUNTY_ABSORBED severity=warn surface=scope' \
    'declared=domain match=bounty program route=bounty' 'findings=1 drift=1'
  tcase scope-fail-model-quality 1 'RESEARCH_GATE: DRIFT' \
    'FINDING SCOPE_MODEL_QUALITY_ABSORBED severity=warn surface=scope' \
    'declared=domain match=model quality route=kengaku' 'findings=1 drift=1'
  tcase scope-fail-orchestration 1 'RESEARCH_GATE: DRIFT' \
    'FINDING SCOPE_ORCHESTRATION_ABSORBED severity=warn surface=scope' \
    'declared=scope match=orchestration route=kumitate' 'findings=1 drift=1'
  tcase scope-pass-declared-table 0 'RESEARCH_GATE: CLEAN (findings=0 drift=0'
  tcase scope-pass-declared-line 0 'RESEARCH_GATE: CLEAN (findings=0 drift=0'
  tcase scope-pass-near-miss 0 'RESEARCH_GATE: CLEAN (findings=0 drift=0'
  tcase scope-pass-prose-decoy 0 'RESEARCH_GATE: CLEAN (findings=0 drift=0'

  # ---- r12 2a: banner contract (cases 93-94) ----
  # The version literal is pinned at two sites (the variable and this case),
  # so renaming VERSION takes a deliberate second edit. The mutant copy proves
  # the banner is drift-bearing: the version token is not a key=value field,
  # so the report names the line id GATE.
  cp "$WORK/pass-control.md" "$WORK/banner-pin.md"
  tcase banner-pin 0 'research-gate v2 ' 'mode=verify'
  sed 's/^VERSION=.*/VERSION=v9/' "$SELF" >"$WORK/gate-banner-mutant.sh"
  tdrift drift-banner-version 1 "$WORK/pin-clean.baseline" \
    "DRIVER=$WORK/gate-banner-mutant.sh" 'GATE_DRIFT: GATE'

  # ---- r12 2b: 8 MiB source-read cap (cases 95-98) ----
  # Boundary pair straddles the first refused size (8388608 reads, 8388609
  # refuses). The over-cap span sits on line 1: a partial read or post-read
  # clamp would report observed=supported, so observed=refused at=- proves the
  # source was never searched. Generated in $WORK at run time — no binary is
  # committed.
  mkdir -p "$WORK/claimsrc"
  cap_span='size cap boundary span holds'
  { printf '%s\n' "$cap_span"; head -c $((SOURCE_READ_MAX_BYTES - ${#cap_span} - 1)) /dev/zero | tr '\0' a; } >"$WORK/claimsrc/cap-at.md"
  { printf '%s\n' "$cap_span"; head -c $((SOURCE_READ_MAX_BYTES - ${#cap_span})) /dev/zero | tr '\0' a; } >"$WORK/claimsrc/cap-over.md"
  printf '{"id":"Z1","source":"claimsrc/cap-at.md","span":"%s","expect":"supported"}\n' "$cap_span" >"$WORK/claims-cap-at.jsonl"
  printf '{"id":"Z2","source":"claimsrc/cap-over.md","span":"%s","expect":"supported"}\n' "$cap_span" >"$WORK/claims-cap-over.jsonl"
  write_rec chain-cap-at <<EOF
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | claimsrc/cap-at.md |
## Chain
| hop | from | to | status | anchor_kind | anchor |
|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | quote | $cap_span |
EOF
  write_rec chain-cap-over <<EOF
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | claimsrc/cap-over.md |
## Chain
| hop | from | to | status | anchor_kind | anchor |
|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | quote | $cap_span |
EOF
  tclaims claims-cap-at 0 'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=1/1' \
    'CLAIM id=Z1 expected=supported observed=supported source=claimsrc/cap-at.md at=line:1 verdict=match'
  tclaims claims-cap-over 1 'RESEARCH_GATE: DRIFT' \
    'FINDING CLAIM_SOURCE_READ_TOO_LARGE severity=warn surface=claims' \
    'CLAIM id=Z2 expected=supported observed=refused source=claimsrc/cap-over.md at=- verdict=refused' \
    'VERDICT_BEARING_CLAIMS=0/1'
  tchain chain-cap-at 0 'RESEARCH_GATE: CLEAN' 'RESOLVED_HOPS=1/1' \
    'CHAIN hop=1 status=resolved observed=verified source=claimsrc/cap-at.md' \
    'at=line:1 verdict=match'
  tchain chain-cap-over 1 'RESEARCH_GATE: DRIFT' \
    'FINDING CHAIN_SOURCE_READ_TOO_LARGE severity=warn surface=chain' \
    'CHAIN hop=1 status=resolved observed=refused source=claimsrc/cap-over.md anchor=- at=- verdict=refused' \
    'RESOLVED_HOPS=0/1'

  # ---- r13: multi-linked source refusal (cases 99-102) ----
  # 99/100: a claim/chain source cited through an in-root hardlink alias of
  # an OUT-OF-ROOT original is refused unread — the r2 residual: readlink -f
  # resolves the alias in-root so the boundary check alone passes (a symlink's
  # true path is re-checked; a hardlink's partners are not soundly
  # enumerable). 101: two in-root aliases of one in-root file refuse too —
  # the refusal is nlink-based (the legit-family false positive is a named
  # limit, knowledge/hardlink-alias-r13.md). 102: a single-link control
  # reads. Generated in $WORK at run time; no repo fixture.
  printf 'out-of-root content\n' >"$WORK/alias-outside.txt"
  mkdir -p "$WORK/aliasroot"
  ln "$WORK/alias-outside.txt" "$WORK/aliasroot/alias-in.md"
  printf '{"id":"H1","source":"aliasroot/alias-in.md","span":"out-of-root content","expect":"supported"}\n' >"$WORK/claims-hardlink-alias.jsonl"
  write_rec chain-hardlink-alias <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | aliasroot/alias-in.md |
## Chain
| hop | from | to | status | anchor_kind | anchor |
|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | quote | out-of-root content |
EOF
  printf 'alias original content\n' >"$WORK/alias-orig.txt"
  ln "$WORK/alias-orig.txt" "$WORK/aliasroot/family-a.md"
  ln "$WORK/alias-orig.txt" "$WORK/aliasroot/family-b.md"
  printf '{"id":"H2","source":"aliasroot/family-a.md","span":"alias original content","expect":"supported"}\n' >"$WORK/claims-hardlink-family.jsonl"
  printf '{"id":"H3","source":"lib/primary.md","span":"line1 primary material","expect":"supported"}\n' >"$WORK/claims-single-link.jsonl"
  tclaims claims-hardlink-alias 1 'RESEARCH_GATE: DRIFT' \
    'FINDING CLAIM_SOURCE_MULTILINKED severity=crit surface=claims' \
    'CLAIM id=H1 expected=supported observed=refused source=aliasroot/alias-in.md at=- verdict=refused' \
    'VERDICT_BEARING_CLAIMS=0/1'
  tchain chain-hardlink-alias 1 'RESEARCH_GATE: DRIFT' \
    'FINDING CHAIN_SOURCE_MULTILINKED severity=crit surface=chain' \
    'CHAIN hop=1 status=resolved observed=refused source=aliasroot/alias-in.md anchor=- at=- verdict=refused' \
    'RESOLVED_HOPS=0/1'
  tclaims claims-hardlink-family 1 'RESEARCH_GATE: DRIFT' \
    'FINDING CLAIM_SOURCE_MULTILINKED severity=crit surface=claims' \
    'CLAIM id=H2 expected=supported observed=refused source=aliasroot/family-a.md at=- verdict=refused'
  tclaims claims-single-link 0 'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=1/1' \
    'CLAIM id=H3 expected=supported observed=supported source=lib/primary.md at=line:1 verdict=match'

  # ---- r14: cross-device (mount-alias) source refusal (cases 103-106) ----
  # A cross-device source can exist in-root only through a mount; the only
  # unprivileged forge on this host is a tmpfs mounted inside one ephemeral
  # `unshare --user --mount` child (a bind of the repo is refused there,
  # measured rc=2). Mount, fixture write and gate run share that child;
  # nothing reaches the host and cases 1-102 keep their bytes. No userns =>
  # the ns cases are skipped BY NAME and the skip is counted in the summary.
  NS_STATE='' NS_WHY='' SKIPPED=0
  ns_probe() { # silent; sets NS_STATE=yes|no once
    [[ -n $NS_STATE ]] && return 0
    command -v unshare >/dev/null 2>&1 || { NS_STATE=no NS_WHY='unshare absent'; return 0; }
    mkdir -p "$WORK/nsprobe"
    if unshare --user --map-root-user --mount --propagation private bash -c '
         mount -t tmpfs none "$1" 2>/dev/null || exit 1
         [[ $(stat -c %d "$1") != $(stat -c %d "$2") ]]' _ "$WORK/nsprobe" "$WORK" 2>/dev/null
    then NS_STATE=yes; else NS_STATE=no NS_WHY='no unprivileged user+mount namespace'; fi
    return 0
  }
  ns_run() { # MODE FILE FIXDIR FIXNAME FIXBODY [ENV=V…] -> gate out; rc = gate rc
    local mode=$1 file=$2 fixdir=$3 fixname=$4 fixbody=$5
    shift 5
    local -a extra=("$@")
    NS_MODE=$mode NS_FILE=$file NS_FIXDIR=$fixdir NS_FIXNAME=$fixname NS_FIXBODY=$fixbody \
      NS_SELF=$SELF NS_ROOT=$WORK NS_NOW=$NOW_EPOCH
    export NS_MODE NS_FILE NS_FIXDIR NS_FIXNAME NS_FIXBODY NS_SELF NS_ROOT NS_NOW
    unshare --user --map-root-user --mount --propagation private bash -c '
      mount -t tmpfs none "$NS_FIXDIR" || exit 97
      printf "%s\n" "$NS_FIXBODY" >"$NS_FIXDIR/$NS_FIXNAME" || exit 98
      exec env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE \
        CHOUSA_STRICT=0 CHOUSA_ROOT="$NS_ROOT" CHOUSA_NOW_EPOCH="$NS_NOW" \
        "$@" bash "$NS_SELF" "$NS_MODE" "$NS_FILE"' _ "${extra[@]+"${extra[@]}"}" 2>&1
  }
  tnscase() { # NAME WANT_RC MODE TARGET SUMPFX FIXDIR FIXNAME FIXBODY [want…|ENV=V…]
    local name=$1 want_rc=$2 mode=$3 target=$4 sum=$5 fixdir=$6 fixname=$7 fixbody=$8
    shift 8
    local -a want=() extra=()
    local a rc=0 out nverdict nsum=0 ok=1 tok
    for a in "$@"; do case "$a" in [A-Z_]*=*) extra+=("$a") ;; *) want+=("$a") ;; esac; done
    ns_probe
    cases=$((cases + 1))
    if [[ $NS_STATE != yes ]]; then
      SKIPPED=$((SKIPPED + 1))
      printf 'skip-case %-2d %-26s reason=%s\n' "$cases" "$name" "$NS_WHY"
      return 0
    fi
    out=$(ns_run "$mode" "$target" "$fixdir" "$fixname" "$fixbody" "${extra[@]+"${extra[@]}"}") || rc=$?
    nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true)
    if [[ -n $sum ]]; then nsum=$(grep -c "^$sum" <<<"$out" || true); else nsum=1; fi
    for tok in "${want[@]+"${want[@]}"}"; do [[ $out == *"$tok"* ]] || ok=0; done
    if [[ $rc -eq $want_rc && $nverdict -eq 1 && $nsum -eq 1 && $ok -eq 1 ]]; then
      printf 'ok-case  %-2d %-26s exit=%d\n' "$cases" "$name" "$rc"
    else
      printf 'FAIL-case %-26s exit=%d want=%d verdicts=%d sums=%d token=%s\n' \
        "$name" "$rc" "$want_rc" "$nverdict" "$nsum" "${want[*]-}"
      printf '%s\n' "$out" | sed 's/^/    | /'
      failures=$((failures + 1))
    fi
  }
  # 103/104: the canonical path is in-root but its st_dev differs from the
  # resolving root's device (tmpfs mounted over $WORK/crossdev inside the ns)
  # => mount alias of another filesystem, refused unread. 105: same path and
  # bytes WITHOUT the mount must read (true-positive control). 106: a
  # LANE_ROOT source (repo device) cited with CHOUSA_ROOT=$WORK (tmpfs) must
  # stay CLEAN — the only case that catches a naive compare-to-CHOUSA_ROOT
  # implementation; it pins PROVINCE.md's span `deep-research method`
  # (line 3, nlink=1), so a text change makes it FAIL loudly.
  mkdir -p "$WORK/crossdev"
  printf '{"id":"D1","source":"crossdev/cross.md","span":"cross-device content here","expect":"supported"}\n' >"$WORK/claims-cross-device.jsonl"
  printf '{"id":"D2","source":"crossdev/cross.md","span":"cross-device content here","expect":"supported"}\n' >"$WORK/claims-cross-device-control.jsonl"
  printf '{"id":"L1","source":"PROVINCE.md","span":"deep-research method","expect":"supported"}\n' >"$WORK/claims-lane-fallback.jsonl"
  write_rec chain-cross-device <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | crossdev/cross.md |
## Chain
| hop | from | to | status | anchor_kind | anchor |
|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | quote | cross-device content here |
EOF
  tnscase claims-cross-device 1 verify-claims "$WORK/claims-cross-device.jsonl" 'VERDICT_BEARING_CLAIMS=' \
    "$WORK/crossdev" cross.md 'cross-device content here' \
    'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_SOURCE_CROSS_DEVICE severity=crit surface=claims' \
    'CLAIM id=D1 expected=supported observed=refused source=crossdev/cross.md at=- verdict=refused' \
    'VERDICT_BEARING_CLAIMS=0/1'
  tnscase chain-cross-device 1 verify-chain "$WORK/chain-cross-device.md" 'RESOLVED_HOPS=' \
    "$WORK/crossdev" cross.md 'cross-device content here' \
    'RESEARCH_GATE: DRIFT' 'FINDING CHAIN_SOURCE_CROSS_DEVICE severity=crit surface=chain' \
    'CHAIN hop=1 status=resolved observed=refused source=crossdev/cross.md anchor=- at=- verdict=refused' \
    'RESOLVED_HOPS=0/1'
  printf 'cross-device content here\n' >"$WORK/crossdev/cross.md"
  tclaims claims-cross-device-control 0 'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=1/1' \
    'CLAIM id=D2 expected=supported observed=supported source=crossdev/cross.md at=line:1 verdict=match'
  tclaims claims-lane-fallback 0 'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=1/1' \
    'CLAIM id=L1 expected=supported observed=supported source=PROVINCE.md at=line:3 verdict=match'

  # 107-110 (r15): the --root / dead-arm — raw "$root_r"/* rendered //* and
  # matched nothing, refusing every absolute source OUT_OF_CORPUS. in_root()
  # normalizes the prefix; src_root keeps the declared root for the device
  # probe. The CHOUSA_ROOT=/ override rides the r15 harness channel.
  # 107: deterministic ghost — an absent absolute path passes the healed
  # boundary and fails the -f probe (pre-fix: OUT_OF_CORPUS crit).
  printf '{"id":"R1","source":"/chousa-r15-absent/absent.md","span":"never present","expect":"unsupported"}\n' \
    >"$WORK/claims-root-slash-absent.jsonl"
  tclaims claims-root-slash-absent 1 'RESEARCH_GATE: DRIFT' \
    'FINDING CLAIM_SOURCE_MISSING severity=warn surface=claims' \
    'CLAIM id=R1 expected=unsupported observed=refused source=/chousa-r15-absent/absent.md' \
    'VERDICT_BEARING_CLAIMS=0/1' CHOUSA_ROOT=/
  # 108: read arm — an existing in-/ absolute source reads CLEAN (this host:
  # /etc/hostname dev 31 == / dev 31, nlink 1, 9 B — the span is the file's
  # own first line, measured at case-build). The device probe still stats
  # the declared root (/) — a cross-device in-/ source must still refuse.
  # 109: that refusal — $WORK is tmpfs (dev 57 != 31) so the absolute path
  # passes the prefix test and dies at the device arm (pre-fix: OUT_OF_CORPUS).
  if [[ -r /etc/hostname ]] && read -r _hspan </etc/hostname && [[ -n $_hspan ]]; then
    printf '{"id":"R2","source":"/etc/hostname","span":"%s","expect":"supported"}\n' "$_hspan" \
      >"$WORK/claims-root-slash-read.jsonl"
    tclaims claims-root-slash-read 0 'RESEARCH_GATE: CLEAN' \
      'CLAIM id=R2 expected=supported observed=supported source=/etc/hostname at=line:1 verdict=match' \
      'VERDICT_BEARING_CLAIMS=1/1' CHOUSA_ROOT=/
  else
    cases=$((cases + 1)); SKIPPED=$((SKIPPED + 1))
    printf 'skip-case %-2d %-26s reason=%s\n' "$cases" claims-root-slash-read '/etc/hostname unreadable'
  fi
  printf 'cross-device content here\n' >"$WORK/rootdev.md"
  printf '{"id":"R3","source":"%s","span":"cross-device content here","expect":"supported"}\n' "$WORK/rootdev.md" \
    >"$WORK/claims-root-slash-xdev.jsonl"
  tclaims claims-root-slash-xdev 1 'RESEARCH_GATE: DRIFT' \
    'FINDING CLAIM_SOURCE_CROSS_DEVICE severity=crit surface=claims' \
    'CLAIM id=R3 expected=supported observed=refused' \
    'VERDICT_BEARING_CLAIMS=0/1' CHOUSA_ROOT=/
  # 111 (r16): --root // — pwd -P preserves '//' so in_root must strip ALL
  # trailing slashes, not just one (the r15 single-strip left '/' which still
  # rendered '//*'). Same /etc/hostname read, same expected CLEAN.
  if [[ -r /etc/hostname ]] && read -r _hspan </etc/hostname && [[ -n $_hspan ]]; then
    printf '{"id":"R4","source":"/etc/hostname","span":"%s","expect":"supported"}\n' "$_hspan" \
      >"$WORK/claims-root-dslash.jsonl"
    tclaims claims-root-dslash 0 'RESEARCH_GATE: CLEAN' \
      'CLAIM id=R4 expected=supported observed=supported source=/etc/hostname at=line:1 verdict=match' \
      'VERDICT_BEARING_CLAIMS=1/1' CHOUSA_ROOT=//
  else
    cases=$((cases + 1)); SKIPPED=$((SKIPPED + 1))
    printf 'skip-case %-2d %-26s reason=%s\n' "$cases" claims-root-dslash '/etc/hostname unreadable'
  fi
  # 110: sweeps symmetric arm — an absolute in-/ location glob resolves
  # through the healed guard (pre-fix: SWEEP_LOCATION_OUT_OF_CORPUS crit).
  # The glob names only; a nonexistent /-rooted dir verifies with zero rows.
  write_rec sweeps-root-slash <<'EOF'
# research-record v1
## Sweeps
| id | where | query | expected |
|---|---|---|---|
| W1 | /chousa-r15-absent/*.md | absent-dir-sweep | no hits |
EOF
  tsweeps sweeps-root-slash 0 'RESEARCH_GATE: CLEAN' \
    'SWEEP id=W1 where=/chousa-r15-absent/*.md' 'observed=verified verdict=match' \
    'VERIFIED_SWEEPS=1/1' CHOUSA_ROOT=/

  # 112-116 (r17): the fenced-heading shadow — a `## ` line inside a fenced
  # code block is literal text, not a heading. A fenced `## Meta` must not
  # reset the real Meta body. The two-pass parser pairs fences (same char,
  # closing length >= opening, 0-3 literal-space indent; unclosed opener =
  # plain text, fail closed).
  # 112: the bypass — real Meta declares refused province, fenced `## Meta`
  # declares in-province (pre-fix: CLEAN, the fenced copy shadowed the real).
  add_scope_row scope-fence-shadow domain 'bounty program scope and claim packages'
  cat >>"$WORK/scope-fence-shadow.md" <<'EOF'
## Notes
```text
## Meta
| key | value |
|---|---|
| domain | deep-research method |
```
EOF
  tcase scope-fence-shadow 1 'RESEARCH_GATE: DRIFT' \
    'FINDING SCOPE_BOUNTY_ABSORBED severity=warn surface=scope' 'findings=1 drift=1'
  # 113: the phantom — no real Meta, only a fenced `## Meta` (pre-fix: the
  # phantom Meta's refused phrase drifted; post-fix: no Meta → no domain →
  # CLEAN by the declaration-only contract).
  cat >"$WORK/scope-fence-only.md" <<'EOF'
# research-record v1
## Question
Do the local claims resolve?
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Chain
| hop | from | to | status | notes |
|---|---|---|---|---|
| 1 | C1 | S1 | resolved | direct |
## Claims
| id | kind | text | pointer | status |
|---|---|---|---|---|
| C1 | observation | primary file has line1 | S1 | verified |
## Rejections
| id | ref | reason | flip |
|---|---|---|---|
| R1 | n/a | none-recorded | a source row would flip this |
## Notes
```text
## Meta
| key | value |
|---|---|
| domain | bounty program scope and claim packages |
```
EOF
  tcase scope-fence-only 0 'RESEARCH_GATE: CLEAN' 'findings=0 drift=0'
  # 114: nested 4-backtick fence — the inner 3-backtick `## Meta` is content
  # under the outer fence; the single-toggle fix would close early and let
  # the fenced Meta through (pre-fix AND naive-toggle: CLEAN).
  add_scope_row scope-fence-nested domain 'bounty program scope and claim packages'
  cat >>"$WORK/scope-fence-nested.md" <<'EOF'
## Notes
````text
```
## Meta
| key | value |
|---|---|
| domain | deep-research method |
```
````
EOF
  tcase scope-fence-nested 1 'RESEARCH_GATE: DRIFT' \
    'FINDING SCOPE_BOUNTY_ABSORBED severity=warn surface=scope' 'findings=1 drift=1'
  # 115: indented closer inside a fence — the 4-space-indented ``` is content,
  # not a closer; the naive toggle treats it as a close (pre-fix AND naive:
  # CLEAN). The real Meta's refused phrase must still refuse.
  add_scope_row scope-fence-indented domain 'bounty program scope and claim packages'
  cat >>"$WORK/scope-fence-indented.md" <<'EOF'
## Notes
```text
    ```
## Meta
| key | value |
|---|---|
| domain | deep-research method |
```
EOF
  tcase scope-fence-indented 1 'RESEARCH_GATE: DRIFT' \
    'FINDING SCOPE_BOUNTY_ABSORBED severity=warn surface=scope' 'findings=1 drift=1'
  # 116: unclosed fence after all sections — the fenced `## Meta` is the last
  # section; the unclosed opener is plain text (fail closed), so the real
  # Meta's refused phrase must still refuse (pre-fix AND naive: CLEAN).
  cat >"$WORK/scope-fence-unclosed.md" <<'EOF'
# research-record v1
## Meta
| key | value |
|---|---|
| window | loopback |
| domain | bounty program scope and claim packages |
## Question
Do the local claims resolve?
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/primary.md:1 |
## Chain
| hop | from | to | status | notes |
|---|---|---|---|---|
| 1 | C1 | S1 | resolved | direct |
## Claims
| id | kind | text | pointer | status |
|---|---|---|---|---|
| C1 | observation | primary file has line1 | S1 | verified |
## Rejections
| id | ref | reason | flip |
|---|---|---|---|
| R1 | n/a | none-recorded | a source row would flip this |
## Notes
```text
## Meta
| key | value |
|---|---|
| domain | deep-research method |
EOF
  tcase scope-fence-unclosed 1 'RESEARCH_GATE: DRIFT' \
    'FINDING SCOPE_BOUNTY_ABSORBED severity=warn surface=scope'

  # 117-119 (r18): the SCOPE_KENGAKU phrase gap — llm benchmark(s) and
  # llm scoring were missing despite the model-quality boundary. The
  # plural form needs a separate entry (scope_hit matches literal phrases,
  # never stems). ai benchmark(s) stays out — too broad (AI-methodology
  # research is not model-quality scope).
  add_scope_row scope-fail-llm-benchmarks domain 'LLM benchmarks'
  tcase scope-fail-llm-benchmarks 1 'RESEARCH_GATE: DRIFT' \
    'FINDING SCOPE_MODEL_QUALITY_ABSORBED severity=warn surface=scope' \
    'declared=domain match=llm benchmarks route=kengaku' 'findings=1 drift=1'
  add_scope_row scope-fail-llm-scoring domain 'llm scoring'
  tcase scope-fail-llm-scoring 1 'RESEARCH_GATE: DRIFT' \
    'FINDING SCOPE_MODEL_QUALITY_ABSORBED severity=warn surface=scope' \
    'declared=domain match=llm scoring route=kengaku' 'findings=1 drift=1'
  # control: benchmark terms in prose only (not a Meta declaration) must
  # stay CLEAN — the screen reads only Meta domain/scope rows.
  sed 's#^Do the local claims resolve?$#Prose mentions LLM benchmarks, llm scoring and ai benchmarks here — never in a ## Meta declaration row.#' \
    "$WORK/scope-base.md" >"$WORK/scope-pass-benchmark-prose.md"
  tcase scope-pass-benchmark-prose 0 'RESEARCH_GATE: CLEAN' 'findings=0 drift=0'

  if [[ $failures -eq 0 ]]; then
    printf 'RESEARCH_GATE_SELFTEST: PASS (%d cases%s)\n' "$cases" "${SKIPPED:+, $SKIPPED skipped}"
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
    verify-claims) MODE=claims; shift ;;
    verify-chain) MODE=chain; shift ;;
    verify-sweeps) MODE=sweeps; shift ;;
    verify-integrity) MODE=integrity; shift ;;
    verify-all) MODE=all; shift ;;
    --pin)
      [[ $# -ge 2 ]] || die_usage "--pin needs PATH"
      MODE=pin; PIN_ARG=$2; shift 2 ;;
    --drift)
      [[ $# -ge 2 ]] || die_usage "--drift needs PATH"
      MODE=drift; DRIFT_ARG=$2; shift 2 ;;
    --record)
      [[ $# -ge 2 ]] || die_usage "--record needs PATH"
      RECORD_ARG=$2; shift 2 ;;
    --root)
      [[ $# -ge 2 ]] || die_usage "--root needs PATH"
      ROOT=$2; ROOT_ARG_SET=1; shift 2 ;;
    --claims)
      [[ $# -ge 2 ]] || die_usage "--claims needs PATH"
      CLAIMS_ARG=$2; shift 2 ;;
    --json)
      [[ $# -ge 2 ]] || die_usage "--json needs PATH"
      JSON_ARG=$2; shift 2 ;;
    --) shift; break ;;
    -*) die_usage "unknown flag: $1" ;;
    *)
      [[ -z $RECORD_ARG ]] || die_usage "multiple record paths"
      RECORD_ARG=$1; shift ;;
  esac
done

if [[ $MODE != all && ( -n ${CLAIMS_ARG:-} || -n ${JSON_ARG:-} ) ]]; then
  die_usage "--claims/--json are only valid with verify-all"
fi

# pin/drift take exactly one baseline path: a record, claims surface, manifest
# or root would be silently ignored by the canonical invocation, so refusing
# them keeps the mode fail-closed like the other setup paths. Both baseline
# flags in one invocation are refused too: mode flags are last-wins, which
# would silently pin or drift the wrong path.
if [[ $MODE == pin || $MODE == drift ]]; then
  [[ -z $RECORD_ARG && -z ${CLAIMS_ARG:-} && -z ${JSON_ARG:-} && $ROOT_ARG_SET -eq 0 ]] \
    || die_usage "--pin/--drift take only a baseline path"
  if [[ $MODE == pin ]]; then
    [[ -z $DRIFT_ARG ]] || die_usage "--pin and --drift are mutually exclusive"
  else
    [[ -z $PIN_ARG ]] || die_usage "--pin and --drift are mutually exclusive"
  fi
fi

case "$MODE" in
  selftest) run_selftest ;;
  pin) run_pin "$PIN_ARG" ;;
  drift) run_drift "$DRIFT_ARG" ;;
  verify)
    RECORD_PATH=${RECORD_ARG:-${CHOUSA_RECORD:-}}
    verify_record "$RECORD_PATH"
    ;;
  claims)
    CLAIMS_PATH=${RECORD_ARG:-${CHOUSA_CLAIMS:-}}
    verify_claims "$CLAIMS_PATH"
    ;;
  chain)
    CHAIN_PATH=${RECORD_ARG:-${CHOUSA_RECORD:-}}
    verify_chain "$CHAIN_PATH"
    ;;
  sweeps)
    SWEEPS_PATH=${RECORD_ARG:-${CHOUSA_RECORD:-}}
    verify_sweeps "$SWEEPS_PATH"
    ;;
  integrity)
    INTEGRITY_PATH=${RECORD_ARG:-${CHOUSA_RECORD:-}}
    verify_integrity "$INTEGRITY_PATH"
    ;;
  all)
    ALL_PATH=${RECORD_ARG:-${CHOUSA_RECORD:-}}
    verify_all "$ALL_PATH"
    ;;
  *) die_usage "unknown mode: $MODE" ;;
esac
