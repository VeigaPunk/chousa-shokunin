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
#   CLAIM_SPAN_NOT_FOUND CLAIM_SPAN_UNEXPECTED CLAIM_LINE_MISMATCH
#   CONTRADICTION_MARKER_ABSENT
#   CLAIM_SOURCE_REVISION_MISMATCH (r31: pinned sha256 differs from source bytes)
#   SWEEP_REJECTION_INCOMPLETE SWEEP_LOCATION_ABSENT SWEEP_LOCATION_UNRESOLVED
#   SWEEP_LOCATION_OUT_OF_CORPUS SWEEP_CLAIM_FALSE REF_UNRESOLVED
#   VERIFY_ALL_CLAIMS_UNRESOLVED VERIFY_ALL_SECTION_UNAVAILABLE
#   SCOPE_BOUNTY_ABSORBED SCOPE_MODEL_QUALITY_ABSORBED
#   SCOPE_ORCHESTRATION_ABSORBED
#   META_SOURCE_ABSENT META_VERIFIED_AT_ABSENT META_VERIFIED_AT_UNDATED
#   META_SOURCE_NO_ROW_ID META_SOURCE_ROW_MISSING META_SOURCE_NOT_MINED
#   META_SOURCE_USEDBY_MISSING META_VERIFIED_AT_BARE META_RECHECK_OVERDUE
#   META_RECHECK_ABSENT META_RECHECK_UNSCHEDULED META_RECHECK_ROOT_PARENT
#   META_ENTRY_REFUSED (r25: denylisted/oversized/NUL entry, refused unparsed)
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
# expect supported|contradicted|unsupported. Fields are read from the record's
# TOP-LEVEL members only (r33): a nested member of the same name is ignored, a
# repeated top-level read field makes the record invalid, and a line that is not
# one well-formed JSON object is invalid. A claim may also name the source
# lines its span must occupy: the optional JSON string field "line" holds "N"
# or "N-M" (N>=1, M>N, decimal, no leading zeros, no spaces). A present "line"
# with any other value (empty, non-string, malformed) makes the record invalid.
# When "line" is present and the span has a boundary-delimited occurrence, the
# claim is bound iff some delimited occurrence starts on line N and ends on
# line N or M; bound claims keep the existing verdict (at= set to that
# occurrence), unbound claims report observed=mislocated with
# CLAIM_LINE_MISMATCH (warn, drift). Span absent with "line" present behaves as
# today (observed=unsupported). Sources are local files under the
# same boundary as verify pointers (canonicalized; session paths denied, URLs
# refused — never fetched). expect=contradicted additionally needs a marker the
# fixture names explicitly (per-claim "marker" or the default) to byte-co-occur
# inside the span's source lines; without it the claim is unproven. A marker on
# A claim may carry optional "sha256": exactly 64 lowercase hex characters pinning
# the exact bytes of the source file (r31 C2). A present malformed value makes the
# record invalid (CLAIM_RECORD_INVALID); a mismatch of the pin against the source
# bytes is observed=stale with CLAIM_SOURCE_REVISION_MISMATCH (warn, drift),
# before and regardless of the span check; absent or equal leaves behavior unchanged.
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
#   observed: supported|contradicted|unsupported|unproven|stale|refused|invalid|mislocated
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
# not-applicable) are exempt from resolution but counted. A hop whose status
# says it could not be followed (unresolved blocked-no-fetch labelled-dead) is
# audited against the same citation/source/boundary/anchor rules the resolved
# arm applies, silently: when its citation would verify as if the row said
# resolved, the hop prints observed=resolvable (verdict mismatch) with exactly
# one CHAIN_EXEMPT_RESOLVABLE (warn, drift) — a false unavailability mark —
# never a CHAIN_SOURCE_*/CHAIN_ANCHOR_*/CHAIN_CITATION_* finding. A hop whose
# citation would not verify (no citation, external URL, missing file,
# undeclared id, out-of-corpus path, anchor absent) stays observed=exempt with
# no finding. rejected/not-applicable record a judgment, not an
# unavailability: they stay exempt and unread whatever their citation.
# Per hop:
#   CHAIN hop=… status=… observed=… source=… anchor=… at=… verdict=…
#   observed: verified|anchor-missing|refused|invalid|resolvable|exempt
#   verdict:  match|mismatch|refused|invalid|exempt
# Summary: RESOLVED_HOPS=N/M — N verified hops over M hops read; CLEAN iff
# every non-exempt hop verified (N = M − exempt − resolvable) and no finding
# drifts.
# Extra ids: CHAIN_ABSENT CHAIN_SOURCE_EXTERNAL CHAIN_SOURCE_SESSION
#   CHAIN_SOURCE_EPHEMERAL CHAIN_SOURCE_OUT_OF_CORPUS CHAIN_SOURCE_MISSING
#   CHAIN_SOURCE_READ_TOO_LARGE
#   CHAIN_SOURCE_MULTILINKED (r13)
#   CHAIN_SOURCE_CROSS_DEVICE (r14)
#   CHAIN_ANCHOR_NOT_FOUND CHAIN_CITATION_INVALID
#   CHAIN_EXEMPT_RESOLVABLE (r32; warn, drift)
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
# and gate SHA-256, per-section state/verdict/tallies, composed verdict. The
# append is one lock-held step (r32 C1): the manifest is opened for append, an
# exclusive flock(2) is taken on that open file, and the lock covers the
# last-byte probe and the write, so cooperating appenders serialize and no
# blank line can appear. The lock is unbounded (a blocking LOCK_EX, released
# when the gate closes the fd); it needs flock(1), and a host without it
# refuses to write the manifest rather than append unlocked.
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
REGISTRY_ARG=''
REGISTRY_ARG_SET=0
PIN_ARG=""
DRIFT_ARG=""
ROOT_ARG_SET=0
AS_OF_ARG_SET=0 AS_OF_ARG=''
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
       research-gate.sh verify-metadata PATH [--root PATH] [--as-of YYYY-MM-DD] [--registry FILE]
       research-gate.sh verify-all [RECORD] [--claims PATH] [--json PATH]
                      [--root PATH]
       research-gate.sh --pin PATH
       research-gate.sh --drift PATH
       research-gate.sh [--record PATH] [--root PATH]

  RECORD via --record, positional, or CHOUSA_RECORD.
  CLAIMS via positional or CHOUSA_CLAIMS.
  Metadata mode checks source, verified-at and recheck in the Markdown header.
  Metadata --as-of computes each entry's recheck due date and freshness.
  Metadata --registry FILE checks source S-ids against a bounded SOURCES.md table.
  PATH is one .md file or a directory of direct .md children; a recheck using
  --root .. reports META_RECHECK_ROOT_PARENT (info).
  Claims file: one JSON object per claim line:
    {"id":…,"source":…,"span":…,"expect":supported|contradicted|unsupported
     [,"marker":…][,"line":"N"|"N-M"][,"sha256":…]}
  Fields are read from the top-level object only: a nested member of the same
  name is ignored; a repeated top-level read field, or a line that is not one
  well-formed JSON object, makes the record invalid (observed=invalid).
  A present "line" (N>=1, M>N, decimal, no leading zeros, no spaces) pins
  the span to exactly that source line range: bound iff some boundary-delimited
  occurrence spans it (at= set to that occurrence); otherwise observed=
  mislocated with FINDING CLAIM_LINE_MISMATCH (warn, drift). Any other present
  "line" value makes the record invalid (observed=invalid).
  Optional "sha256": exactly 64 lowercase hex characters pinning the exact source
  bytes; malformed present value makes the record invalid, a mismatch is
  observed=stale (CLAIM_SOURCE_REVISION_MISMATCH) before the span check.
  Spans must appear verbatim in sources at token boundaries; sources are
  local files only.
  Chain mode: each hop with status=resolved must cite a source (a source id
  from ## Sources, or a local path) plus an anchor — an anchor_kind column
  (heading|quote|line) with an anchor column, or a to fragment
  path#kind:text (bare #text = heading). The anchor must appear in the cited
  source: headings by text, quotes verbatim at token boundaries, lines as
  whole lines.
  Unresolved/marked hops stay exempt but counted. A hop that says it could
  not be followed (unresolved|blocked-no-fetch|labelled-dead) is still
  audited: a citation that would verify as if the row said resolved prints
  observed=resolvable with one CHAIN_EXEMPT_RESOLVABLE warning and drifts;
  any other such hop stays exempt. rejected/not-applicable stay unread.
  Sources obey the same boundary as verify-claims (local, canonicalized,
  never fetched).
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
  and the composed verdict. The append is one critical section: an exclusive
  flock(2) on the manifest fd the gate opened for append is taken before the
  last-byte probe and held through the write, so concurrent appenders
  serialize (a cooperating LOCK_EX holder delays the append until release).
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
  # r20: the same shadow class exists through HTML comments — a `## ` inside
  # <!-- --> is literal text, not a heading. Track comment state alongside
  # fence state; a heading inside either is literal.
  local in_comment=0
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
    if [[ $in_comment -eq 1 ]]; then
      [[ $line == *'-->'* ]] && in_comment=0
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
    if [[ $line == *'<!--'* ]]; then
      [[ $line != *'-->'* ]] && in_comment=1
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

is_denylist_path_value() {
  local f=$1
  case "$f" in
    *op.env|*.env|*server.token*|*credentials/*|*/oauth/*) return 0 ;;
  esac
  [[ $f == *chrome-profile* || $f == *Cookies* || $f == *"Login Data"* ]] && return 0
  # r22: the path-start forms also deny — a citation '.config/foo' (no './'
  # prefix) must refuse the same as './.config/foo'. The */X/* patterns need
  # a leading component; bare-start forms have none.
  [[ $f == *'/.omp/'* || $f == *'/.config/'* || $f == *'/.local/state/'* ]] && return 0
  [[ $f == '.omp/'* || $f == '.config/'* || $f == '.local/state/'* ]] && return 0
  return 1
}

is_denylist_fs_path() {
  local f=$1
  is_denylist_path_value "$f" && return 0
  is_denylist_path_value "$(ptr_file_part "$f")"
}

is_denylist_path() {
  is_denylist_path_value "$(ptr_file_part "$1")"
}

ptr_resolves_meta() {
  # r21: relative pointers were checked with raw -f — a 'lib/../../etc/x'
  # or a symlink to outside passed if the file existed under the raw path.
  # Canonicalize the candidate the same way claim_source_path does, then
  # check in_root against BOTH roots. The absolute arm also checks both
  # roots — the r15 single-root check refused valid lane-root pointers.
  # The denylist applies to the canonical target too: a benign symlink to
  # .config/passwd must not pass because the citation itself was clean.
  local p f root_r lane_r cand canon
  p=$(norm_ptr "$1")
  is_ephemeral_ptr "$p" && return 1
  is_url_ptr "$p" && return 1
  is_denylist_path "$p" && return 1
  f=$(ptr_file_part "$p")
  [[ -z $f ]] && return 1
  root_r=$(cd -- "$ROOT" 2>/dev/null && pwd -P || printf '%s' "$ROOT")
  lane_r=$(cd -- "$LANE_ROOT" 2>/dev/null && pwd -P || printf '%s' "$LANE_ROOT")
  if [[ $f == /* ]]; then
    cand=$f
  elif [[ -e $ROOT/$f || -L $ROOT/$f ]]; then
    cand=$ROOT/$f
  elif [[ -e $LANE_ROOT/$f || -L $LANE_ROOT/$f ]]; then
    cand=$LANE_ROOT/$f
  else
    return 1
  fi
  canon=$(readlink -f -- "$cand" 2>/dev/null || printf '%s' "$cand")
  is_denylist_fs_path "$canon" && return 1
  if in_root "$canon" "$root_r" || in_root "$canon" "$lane_r"; then
    [[ -f $canon ]] && return 0
  fi
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

# C1 (round 33): a claim record is one JSON object per line and the gate reads
# id/source/span/expect/marker/line/sha256 (and marker_default) from ITS
# TOP-LEVEL members only (corpus/evidence/round33/claims.md). claim_scan walks
# the line once in the C locale with string state (quotes, backslash escapes,
# including an escaped backslash before a closing quote) and bracket depth over
# {} and [] outside strings, and records depth-1 members in four tables:
#   JSON_PRESENT[K]  K is a top-level member (any value type)
#   JSON_STR[K]      K's raw string body (escapes intact: what json_str returned)
#   JSON_DUP[K]      K occurs more than once among the top-level members
#   JSON_DUPDIFF[K]  some repeat of K is not a string with the first raw body
# A member of the same name inside a nested object or array is inside a skipped
# value and never lands in a table; characters inside a string value are never
# structure. A line that is not one well-formed object (unbalanced or mismatched
# brackets, trailing garbage, a member name that is not a string, whitespace
# other than space/tab/CR/LF, a bare token that is not a JSON literal or number)
# fails closed: rc=1 and no tables. Not checked (as at base): raw control bytes
# inside strings, and the member/element grammar inside nested values beyond
# bracket balance and bare tokens. First occurrence wins in the value tables; a
# repeat is only flagged, so a duplicated read field is refused by the caller.
# The last scanned line is cached, so the accessors scan once per record.
declare -A JSON_PRESENT=() JSON_STR=() JSON_DUP=() JSON_DUPDIFF=()
JSON_SCAN_LINE=''
JSON_SCAN_RC=1

claim_scan() { # LINE -> JSON_* tables + JSON_SCAN_RC; rc0: one well-formed object
  local LC_ALL=C
  local s=$1
  if [[ $s == "$JSON_SCAN_LINE" ]]; then return "$JSON_SCAN_RC"; fi
  JSON_SCAN_LINE=$s
  JSON_SCAN_RC=1
  JSON_PRESENT=(); JSON_STR=(); JSON_DUP=(); JSON_DUPDIFF=()
  local n=${#s} i=0 c key val stk top is_str esc in_str tok
  # JSON whitespace only (space, tab, CR, LF): a form feed or vertical tab is not
  # whitespace in RFC 8259 and makes the line malformed (r33 post-falsify:
  # ProbeWhitespace33). A scalar is one RFC 8259 literal or number (r33
  # post-falsify: ProbeFlatBehaviour33, ProbeMalformed33, CriticClaim33).
  local ws=$' \t\r\n'
  local lit='^(true|false|null|-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-]?[0-9]+)?)$'
  # Runs are consumed with one regex match each, not one ${s:i:1} per byte: a
  # substring costs time in the line length, so a byte loop is quadratic in it
  # (r33 post-falsify: ProbeLongLines33, 64 KiB unread member 0.07 s -> 4.7 s).
  local strrun='^[^"\\]+'                      # string body up to " or backslash
  local tokrun=$'^[^][{}",: \t\r\n]+'          # bare token inside a nested value
  local wsrun=$'^[ \t\r\n]+'
  # an escape is one of \" \\ \/ \b \f \n \r \t or \u + four hex digits (RFC 8259
  # §7); anything else is malformed (r33 post-falsify: MutC1GateString, "\q")
  local escok='^\\(["\\/bfnrt]|u[0-9A-Fa-f]{4})'
  # leading whitespace, then the single opening brace
  while (( i < n )); do c=${s:i:1}; [[ $c == [$ws] ]] || break; i=$((i + 1)); done
  (( i < n )) && [[ ${s:i:1} == '{' ]] || return 1
  i=$((i + 1))
  local allow_close=1   # only an empty object may close before a member
  while :; do
    while (( i < n )); do c=${s:i:1}; [[ $c == [$ws] ]] || break; i=$((i + 1)); done
    (( i < n )) || return 1
    c=${s:i:1}
    if [[ $c == '}' ]]; then
      (( allow_close )) || return 1        # a trailing comma is not a member
      i=$((i + 1))
      while (( i < n )); do c=${s:i:1}; [[ $c == [$ws] ]] || break; i=$((i + 1)); done
      (( i == n )) || return 1             # trailing garbage
      JSON_SCAN_RC=0
      return 0
    fi
    [[ $c == '"' ]] || return 1            # a member name is a JSON string
    # member name: raw text, escapes intact, so a key spelled with an escape
    # (the not-claimed "l\u0069ne") is not read as the plain key
    key=''; i=$((i + 1))
    while :; do
      (( i < n )) || return 1
      if [[ ${s:i} =~ $strrun ]]; then
        key+=${BASH_REMATCH[0]}; i=$((i + ${#BASH_REMATCH[0]})); continue
      fi
      c=${s:i:1}
      if [[ $c == '\' ]]; then
        [[ ${s:i:6} =~ $escok ]] || return 1
        key+=${s:i:2}; i=$((i + 2)); continue
      fi
      i=$((i + 1)); break                   # the closing quote
    done
    # colon
    while (( i < n )); do c=${s:i:1}; [[ $c == [$ws] ]] || break; i=$((i + 1)); done
    (( i < n )) && [[ ${s:i:1} == ':' ]] || return 1
    i=$((i + 1))
    while (( i < n )); do c=${s:i:1}; [[ $c == [$ws] ]] || break; i=$((i + 1)); done
    (( i < n )) || return 1
    c=${s:i:1}; val=''; is_str=0
    if [[ $c == '"' ]]; then
      # string value: raw body with escapes intact
      is_str=1; i=$((i + 1))
      while :; do
        (( i < n )) || return 1
        if [[ ${s:i} =~ $strrun ]]; then
          val+=${BASH_REMATCH[0]}; i=$((i + ${#BASH_REMATCH[0]})); continue
        fi
        c=${s:i:1}
        if [[ $c == '\' ]]; then
          [[ ${s:i:6} =~ $escok ]] || return 1
          val+=${s:i:2}; i=$((i + 2)); continue
        fi
        i=$((i + 1)); break                 # the closing quote
      done
    elif [[ $c == '{' || $c == '[' ]]; then
      # nested value: skip to its matching close, strings honoured; every bare
      # token outside strings must be one JSON literal or number
      stk=$c; i=$((i + 1)); in_str=0; tok=''
      while [[ -n $stk ]]; do
        (( i < n )) || return 1
        if (( in_str )); then
          if [[ ${s:i} =~ $strrun ]]; then i=$((i + ${#BASH_REMATCH[0]})); continue; fi
          c=${s:i:1}
          if [[ $c == '\' ]]; then
            [[ ${s:i:6} =~ $escok ]] || return 1
            i=$((i + 2)); continue
          fi
          in_str=0; i=$((i + 1)); continue  # the closing quote
        fi
        if [[ ${s:i} =~ $tokrun ]]; then
          tok+=${BASH_REMATCH[0]}; i=$((i + ${#BASH_REMATCH[0]})); continue
        fi
        if [[ ${s:i} =~ $wsrun ]]; then
          i=$((i + ${#BASH_REMATCH[0]}))     # before the literal test reuses BASH_REMATCH
          [[ -z $tok || $tok =~ $lit ]] || return 1
          tok=''; continue
        fi
        c=${s:i:1}
        case "$c" in
          '"'|'{'|'['|'}'|']'|','|':'|' '|$'\t'|$'\r'|$'\n')
            if [[ -n $tok ]]; then
              [[ $tok =~ $lit ]] || return 1  # not a JSON literal or number
              tok=''
            fi
            ;;
        esac
        case "$c" in
          '"') in_str=1 ;;
          '{'|'[') stk+=$c ;;
          '}'|']')
            top=${stk: -1}
            if [[ $c == '}' && $top == '{' ]] || [[ $c == ']' && $top == '[' ]]; then
              stk=${stk%?}
            else
              return 1                     # mismatched bracket
            fi
            ;;
          ','|':'|' '|$'\t'|$'\r'|$'\n') ;;
          *) tok+=$c ;;
        esac
        i=$((i + 1))
      done
    else
      # number, true, false, null: up to a delimiter, then one RFC 8259 literal
      while (( i < n )); do
        c=${s:i:1}
        case "$c" in
          ','|'}'|']'|' '|$'\t'|$'\r'|$'\n') break ;;
        esac
        val+=$c; i=$((i + 1))
      done
      [[ $val =~ $lit ]] || return 1
    fi
    # an empty member name cannot be an associative-array subscript (bash 5.3
    # rejects ""); no read key is empty, so the table simply skips it.
    if [[ -n $key ]]; then
      if [[ -n ${JSON_PRESENT["$key"]+x} ]]; then
        # flag the key when ANY repeat is not a string whose raw body equals the
        # first occurrence's (r33 post-falsify: three or more repeats,
        # ReviewKnowledge33), so the caller can tell agreeing repeats apart
        if (( ! is_str )) || [[ -z ${JSON_STR["$key"]+x} || $val != "${JSON_STR["$key"]}" ]]; then
          JSON_DUPDIFF["$key"]=1
        fi
        JSON_DUP["$key"]=1
      else
        JSON_PRESENT["$key"]=1
        if (( is_str )); then JSON_STR["$key"]=$val; fi
      fi
    fi
    # after a value only ',' (another member) or the closing brace may follow
    while (( i < n )); do c=${s:i:1}; [[ $c == [$ws] ]] || break; i=$((i + 1)); done
    (( i < n )) || return 1
    c=${s:i:1}
    if [[ $c == '}' ]]; then
      i=$((i + 1))
      while (( i < n )); do c=${s:i:1}; [[ $c == [$ws] ]] || break; i=$((i + 1)); done
      (( i == n )) || return 1
      JSON_SCAN_RC=0
      return 0
    fi
    [[ $c == ',' ]] || return 1
    i=$((i + 1)); allow_close=0
  done
}

json_str() { # LINE KEY -> raw JSON string body of the TOP-LEVEL member; rc=1 absent/non-string
  claim_scan "$1" || return 1
  [[ -n ${JSON_STR["$2"]+x} ]] || return 1
  printf '%s' "${JSON_STR["$2"]}"
}

jfield() { json_str "$1" "$2" 2>/dev/null || true; }

json_has_key() { # LINE KEY -> rc0: KEY is a TOP-LEVEL member of the record (any value type)
  # presence is tracked separately from json_str so a present non-string value
  # (number, bool, null, …) is distinguishable from an absent key, and a member
  # inside a nested object or a key spelling inside a string value is not seen.
  claim_scan "$1" || return 1
  [[ -n ${JSON_PRESENT["$2"]+x} ]]
}

json_dup() { # LINE KEY -> rc0: KEY occurs more than once among the TOP-LEVEL members
  claim_scan "$1" || return 1
  [[ -n ${JSON_DUP["$2"]+x} ]]
}

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
  if is_session_url "$src" || is_denylist_fs_path "$src"; then
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
  if is_denylist_fs_path "$canon"; then
    CLAIM_REFUSE=CLAIM_SOURCE_SESSION
    CLAIM_REFUSE_OBS="path=$(ptr_file_part "$src") denied (not opened)"
    return 1
  fi
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
  local LC_ALL=C
  export LC_ALL
  local hay=$1 span=$2 before after offset rest=$1 skipped=0
  TOK_AT=- TOK_L1=0 TOK_L2=0
  [[ -n $span ]] || return 1
  # Literal shell matching keeps the span inside Bash, not an exec argv.
  while [[ $rest == *"$span"* ]]; do
    before=${rest%%"$span"*}
    offset=$((skipped + ${#before}))
    before=${hay:0:offset}
    after=${hay:offset+${#span}}
    if tok_left_ok "$before" "$span" && tok_right_ok "$after" "$span"; then
      TOK_L1=$(( $(count_nl "$before") + 1 ))
      TOK_L2=$(( TOK_L1 + $(count_nl "$span") ))
      if [[ $TOK_L1 -eq $TOK_L2 ]]; then TOK_AT=line:$TOK_L1; else TOK_AT=lines:$TOK_L1-$TOK_L2; fi
      return 0
    fi
    skipped=$((offset + 1))
    rest=${hay:skipped}
  done
  return 1
}

tok_span_all() { # HAY SPAN -> stdout: "L1 L2" per boundary-delimited occurrence
  # rc0: at least one delimited occurrence; rc1: none. Same matcher and
  # boundary rules as tok_span_at, but every delimited occurrence is emitted
  # (tok_span_at stops at the first) with its 1-based start and end lines.
  local LC_ALL=C
  export LC_ALL
  local hay=$1 span=$2 before after occurrence offset regex='' i c hex l1 l2 found=0
  [[ -n $span ]] || return 1
  for ((i = 0; i < ${#span}; i++)); do
    c=${span:i:1}
    printf -v hex '%02x' "'$c"
    regex+="\\x$hex"
  done
  while IFS= read -r -d '' occurrence; do
    offset=${occurrence%%:*}
    before=${hay:0:offset}
    after=${hay:offset+${#span}}
    if tok_left_ok "$before" "$span" && tok_right_ok "$after" "$span"; then
      found=1
      l1=$(( $(count_nl "$before") + 1 ))
      l2=$(( l1 + $(count_nl "$span") ))
      printf '%d %d\n' "$l1" "$l2"
    fi
  done < <(printf '%s' "$hay" | grep -a -z -b -o -P -- "$regex")
  [[ $found -eq 1 ]]
}

token_matcher_require() {
  if printf 'x' | grep -a -z -b -o -P -- 'x' >/dev/null 2>&1; then return 0; fi
  printf 'research-gate: GNU grep with -z/-P support is required for claims and chain token matching\n' >&2
  return 1
}

verify_claims() {
  local claims=$1
  ROOT=${CHOUSA_ROOT:-$ROOT}
  [[ -n ${claims:-} ]] || die_usage "claims file required (verify-claims PATH or CHOUSA_CLAIMS)"
  [[ -e $claims ]] || die_usage "claims file not found: $claims"
  [[ -f $claims ]] || die_usage "claims file is not a regular file: $claims"
  [[ -r $claims ]] || die_usage "claims file unreadable: $claims"
  token_matcher_require || return 2

  FINDING_LINES=(); N_FINDINGS=0; N_DRIFT=0; ROLL=CLEAN

  local N_CLAIMS=0 N_SUP=0 N_CON=0 N_UNS=0 N_UNP=0 N_MISM=0 N_REFUSED=0 N_INVALID=0
  local default_marker='' lineno=0 line CLAIM_REFUSE='' CLAIM_REFUSE_OBS='' CLAIM_SRC_PATH=''
  local -a CLAIM_LINES=()
  local id src span expect marker observed verdict at bad l sha_pin='' sha_present='' sha_actual=''
  local hay start_line end_line region m probe nearer tok ctx path show_id show_exp
  local linef='' line_n=0 line_m=0 line_present=0 lbad='' bound l1 l2
  local dup='' dupk='' show_src='' nulk=''

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
    # C1: one well-formed JSON object per record. A line the reader cannot parse
    # (unbalanced or mismatched brackets, trailing garbage, a member name that is
    # not a string) fails closed as invalid instead of being read by regex.
    if ! claim_scan "$line"; then
      N_CLAIMS=$((N_CLAIMS + 1)); N_INVALID=$((N_INVALID + 1))
      emit_finding CLAIM_RECORD_INVALID warn claims "line=$lineno not one well-formed JSON object"
      CLAIM_LINES+=("CLAIM id=line$lineno expected=- observed=invalid source=- at=- verdict=invalid")
      continue
    fi
    # C1: a read field repeated among the top-level members makes the record
    # invalid (RFC 8259 §4: duplicate names make receiver behaviour
    # unpredictable), whether or not the values agree. The first duplicate in a
    # fixed order names the reason. Computed before the marker-default test so
    # a marker-default row with any repeated read field is refused, never
    # silently taken (r33 post-falsify: RerunC1a F1, RerunC1b G2).
    dup=''
    for dupk in id source span expect marker line sha256 marker_default; do
      if json_dup "$line" "$dupk"; then dup=$dupk; break; fi
    done
    # a marker-default row has a top-level "marker_default" string, no top-level
    # "id" string and no repeated read field
    if [[ -z $dup ]] && ! json_str "$line" id >/dev/null 2>&1 \
       && json_str "$line" marker_default >/dev/null 2>&1; then
      default_marker=$(json_unescape "$(jfield "$line" marker_default)")
      continue
    fi
    bad=''; observed=''; at=''; sha_present=''; sha_pin=''
    N_CLAIMS=$((N_CLAIMS + 1))
    if [[ -n $dup ]]; then
      N_INVALID=$((N_INVALID + 1))
      id=$(json_unescape "$(jfield "$line" id)")
      expect=$(json_unescape "$(jfield "$line" expect)")
      src=$(json_unescape "$(jfield "$line" source)")
      show_id=${id:-line$lineno}; show_exp=${expect:--}; show_src=${src:--}
      if [[ $dup == id ]]; then
        # a duplicated id prints that id only when every repeat is a string with
        # the same raw body as the first; otherwise the id is as unreadable as
        # any other and the line number stands in
        show_id=line$lineno
        if [[ -n $id && -z ${JSON_DUPDIFF[id]+x} ]]; then show_id=$id; fi
      fi
      [[ $dup == expect ]] && show_exp=-
      [[ $dup == source ]] && show_src=-
      emit_finding CLAIM_RECORD_INVALID warn claims "line=$lineno duplicate top-level key $dup"
      CLAIM_LINES+=("CLAIM id=$show_id expected=$show_exp observed=invalid source=$show_src at=- verdict=invalid")
      continue
    fi

    id=$(json_unescape "$(jfield "$line" id)")
    src=$(json_unescape "$(jfield "$line" source)")
    span=$(json_unescape "$(jfield "$line" span)"; printf x); span=${span%x}
    expect=$(json_unescape "$(jfield "$line" expect)")
    marker=$(json_unescape "$(jfield "$line" marker)")
    # C1: optional "line" field. json_str reads string values; json_has_key
    # detects a present key of ANY value type, so a present empty or non-string
    # value is distinguishable from an absent key (both are invalid).
    line_present=0; linef=''; lbad=''
    if json_has_key "$line" line; then
      line_present=1
      if json_str "$line" line >/dev/null 2>&1; then
        linef=$(json_unescape "$(jfield "$line" line)")
      fi
    fi
    bad=''
    if json_has_key "$line" sha256; then
      # a present non-string value is malformed, never "absent" (r31)
      sha_present=1; sha_pin='-'
      # decode the JSON string exactly: keep trailing newlines (printf x) and
      # treat an escaped NUL (bash drops NULs) as malformed, so neither can be
      # decoded away into a match (r31)
      if json_str "$line" sha256 >/dev/null 2>&1; then
        sha_raw=$(json_str "$line" sha256)
        if [[ ${sha_raw,,} != *'\u0000'* ]]; then
          sha_pin=$(json_unescape "$sha_raw"; printf x); sha_pin=${sha_pin%x}
        fi
      fi
    fi
    # an escaped NUL in any read string field would be dropped by the decoder
    # (bash cannot hold NUL), so "al\u0000pha" would verify as "alpha": refuse
    # it as sha256 already is (r33 post-falsify: ProbeMalformed33 F4)
    # (escaped backslash pairs are removed first, so a literal "\\u0000" text is
    # not mistaken for one; the tables are this record's: claim_scan ran above)
    nulk=''
    for dupk in id source span expect marker line; do
      [[ -n ${JSON_STR[$dupk]+x} ]] || continue
      sha_raw=${JSON_STR[$dupk]//\\\\/}
      if [[ ${sha_raw,,} == *'\u0000'* ]]; then nulk=$dupk; break; fi
    done
    if [[ -n $nulk ]]; then bad="$nulk holds an escaped NUL (\\u0000)"
    elif [[ -z $id ]]; then bad="missing id"
    elif [[ -z $src ]]; then bad="missing source"
    elif [[ -z $span ]]; then bad="missing/empty span"
    elif [[ -z $expect ]]; then bad="missing expect"
    else
      case "$expect" in
        supported|contradicted|unsupported) ;;
        *) bad="expect=$expect invalid" ;;
      esac
      if [[ -n $sha_present && ! $sha_pin =~ ^[0-9a-f]{64}$ ]]; then
        bad="sha256 malformed (not 64 lowercase hex characters)"
      fi
      if [[ -z $bad && $expect != contradicted && -n $marker ]]; then
        bad="marker present but expect=$expect (fixture violation)"
      fi
    fi
    if [[ -z $bad && $line_present -eq 1 ]]; then
      if [[ -z $linef ]]; then
        bad="line not a JSON string"
      elif [[ $linef =~ ^[1-9][0-9]*$ ]]; then
        line_n=$linef; line_m=$linef
      elif [[ $linef =~ ^([1-9][0-9]*)-([1-9][0-9]*)$ ]]; then
        line_n=${BASH_REMATCH[1]}; line_m=${BASH_REMATCH[2]}
        # Decimal compare without arithmetic: same-length leading-zero-free
        # digit strings compare lexicographically == numerically; M<=N is
        # rejected (equality, shorter, or lexicographically smaller).
        if [[ $line_m == "$line_n" ]] \
           || [[ ${#line_m} -lt ${#line_n} ]] \
           || { [[ ${#line_m} -eq ${#line_n} && $line_m < $line_n ]]; }; then
          bad="line range M<=N"
        fi
      else
        bad="line value malformed"
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

    if [[ -n $sha_present ]]; then
      # hash via stdin: sha256sum escapes file names holding '\' or a newline
      # and would prefix its output with '\' (r31)
      sha_actual=$(sha256sum < "$path" 2>/dev/null | cut -d' ' -f1 || true)
      # fail closed: an unmeasurable source is not a match (r31)
      [[ $sha_actual =~ ^[0-9a-f]{64}$ ]] || sha_actual=unreadable
      if [[ $sha_actual != "$sha_pin" ]]; then
        observed=stale
        at=-
        emit_finding CLAIM_SOURCE_REVISION_MISMATCH warn claims \
          "id=$id pin=${sha_pin:0:12} actual=${sha_actual:0:12}"
      fi
    fi

    if [[ -z ${observed:-} ]]; then
      hay=$(cat -- "$path"; printf x)
      hay=${hay%x}
      if tok_span_at "$hay" "$span"; then
      start_line=$TOK_L1
      end_line=$TOK_L2
      at=$TOK_AT
      bound=1
      if [[ $line_present -eq 1 ]]; then
        # C1: bind iff some boundary-delimited occurrence spans exactly the
        # named line range. tok_span_at stops at the first occurrence, so all
        # delimited occurrences are enumerated and compared; at= follows the
        # bound occurrence (or stays the first when none binds).
        bound=0
        while read -r l1 l2; do
          # string equality: both sides are leading-zero-free decimals, so it
          # equals numeric equality without arithmetic on untrusted digits (r31)
          if [[ $l1 == "$line_n" && $l2 == "$line_m" ]]; then
            start_line=$l1
            end_line=$l2
            if [[ $l1 -eq $l2 ]]; then at=line:$l1; else at=lines:$l1-$l2; fi
            bound=1
            break
          fi
        done < <(tok_span_all "$hay" "$span")
      fi
      if [[ $bound -eq 1 ]]; then
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
        observed=mislocated
        emit_finding CLAIM_LINE_MISMATCH warn claims "id=$id line=$line_n-$line_m first_delimited_occurrence=$TOK_AT"
      fi
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
      # r23: a # heading inside a fenced code block is literal text, not a
      # heading — the raw ^#+ matcher must not match it. Track fence state
      # (same char must close, closing length >= opening, 0-3 literal-space
      # indent; unclosed = literal to EOF, fail closed).
      local fence_char='' fence_len=0 c l
      while IFS= read -r line || [[ -n $line ]]; do
        lineno=$((lineno + 1))
        if [[ -n $fence_char ]]; then
          if [[ $line =~ ^\ {0,3}(\`{3,}|~{3,})[[:space:]]*$ ]]; then
            c=${BASH_REMATCH[1]:0:1}; l=${#BASH_REMATCH[1]}
            [[ $c == "$fence_char" && $l -ge $fence_len ]] && fence_char=''
          fi
          continue
        fi
        if [[ $line =~ ^\ {0,3}(\`{3,}|~{3,})(.*)$ ]]; then
          fence_char=${BASH_REMATCH[1]:0:1}; fence_len=${#BASH_REMATCH[1]}
          continue
        fi
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

chain_probe() { # ROW -> PROBE=verified|anchor-missing|refused|invalid (silent)
  # The one citation resolution both chain arms use: chain_citation parses the
  # row, the source is a declared id or a path under the same boundary as
  # verify-claims (claim_source_path: local, canonicalized, never fetched),
  # and chain_anchor_at finds the anchor in those bytes. Emits nothing and
  # reads no network: the resolved arm turns PROBE into its own findings, the
  # exempt arm audits a hop that claims it could not be followed.
  local row=$1 to ref hay
  PROBE=invalid PROBE_CITE_ERR='' PROBE_TO='' PROBE_REF='' PROBE_WHY=''
  PROBE_REFUSE_ID='' PROBE_REFUSE_OBS='' PROBE_KIND='' PROBE_TEXT='' PROBE_AT='-'
  PROBE_HAY=''
  chain_citation "$row" || { PROBE_CITE_ERR=$CITE_ERR; return 0; }
  PROBE_TO=$CITE_TO PROBE_KIND=$CITE_KIND PROBE_TEXT=$CITE_TEXT
  to=$CITE_TO
  if [[ -n ${SRC_PTR[$to]+x} ]]; then
    if [[ -z ${SRC_PTR[$to]} ]]; then
      PROBE=refused PROBE_WHY=pointer-empty
      return 0
    fi
    ref=${SRC_PTR[$to]}
  elif [[ $to =~ ^S[A-Za-z0-9_-]+$ ]]; then
    PROBE=refused PROBE_WHY=undeclared-id
    return 0
  else
    ref=$to
  fi
  ref=$(chain_ref_file "$ref")
  PROBE_REF=$ref
  if ! claim_source_path "$ref"; then
    PROBE=refused PROBE_WHY=boundary
    PROBE_REFUSE_ID=$(chain_refuse_id "$CLAIM_REFUSE")
    PROBE_REFUSE_OBS=$CLAIM_REFUSE_OBS
    return 0
  fi
  hay=$(cat -- "$CLAIM_SRC_PATH"; printf x)
  hay=${hay%x}
  PROBE_HAY=$hay
  if chain_anchor_at "$hay" "$PROBE_KIND" "$PROBE_TEXT"; then
    PROBE=verified PROBE_AT=$CITE_AT
  else
    PROBE=anchor-missing
  fi
  return 0
}

verify_chain() {
  local record=$1
  ROOT=${CHOUSA_ROOT:-$ROOT}
  [[ -n ${record:-} ]] || die_usage "record path required (verify-chain RECORD, --record, or CHOUSA_RECORD)"
  [[ -e $record ]] || die_usage "record not found: $record"
  [[ -f $record ]] || die_usage "record is not a regular file: $record"
  [[ -r $record ]] || die_usage "record unreadable: $record"
  token_matcher_require || return 2

  FINDING_LINES=(); N_FINDINGS=0; N_DRIFT=0; ROLL=CLEAN
  scan_secrets "$record"
  load_sections "$record"

  local N_HOPS=0 N_VER=0 N_EXEMPT=0 N_MISM=0 N_REFUSED=0 N_INVALID=0
  local N_RESOLVABLE=0
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

  local hrow hop st to disp obs at verdict l
  local CITE_TO='' CITE_KIND='' CITE_TEXT='' CITE_ERR=''
  local CHAIN_NEAREST='' CHAIN_CTX=''
  local CLAIM_REFUSE='' CLAIM_REFUSE_OBS='' CLAIM_SRC_PATH=''
  local PROBE='' PROBE_CITE_ERR='' PROBE_TO='' PROBE_REF='' PROBE_WHY=''
  local PROBE_REFUSE_ID='' PROBE_REFUSE_OBS='' PROBE_KIND='' PROBE_TEXT=''
  local PROBE_AT='-' PROBE_HAY=''
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
          chain_probe "$hrow"
          if [[ $PROBE == invalid ]]; then
            N_INVALID=$((N_INVALID + 1))
            emit_finding CHAIN_CITATION_INVALID warn chain "hop=$hop status=resolved $PROBE_CITE_ERR"
            CHAIN_LINES+=("CHAIN hop=$hop status=resolved observed=invalid source=$disp anchor=- at=- verdict=invalid")
            continue
          fi
          if [[ $PROBE == refused ]]; then
            N_REFUSED=$((N_REFUSED + 1))
            case "$PROBE_WHY" in
              pointer-empty)
                emit_finding CHAIN_SOURCE_MISSING warn chain "hop=$hop to=$PROBE_TO source row has no pointer"
                CHAIN_LINES+=("CHAIN hop=$hop status=resolved observed=refused source=$PROBE_TO anchor=- at=- verdict=refused") ;;
              undeclared-id)
                emit_finding CHAIN_SOURCE_MISSING warn chain "hop=$hop to=$PROBE_TO source_id not in ## Sources"
                CHAIN_LINES+=("CHAIN hop=$hop status=resolved observed=refused source=$PROBE_TO anchor=- at=- verdict=refused") ;;
              *)
                emit_finding "$PROBE_REFUSE_ID" "$(chain_source_sev "$PROBE_REFUSE_ID")" chain \
                  "hop=$hop source=$(chain_disp "$PROBE_REF") obs=$PROBE_REFUSE_OBS"
                CHAIN_LINES+=("CHAIN hop=$hop status=resolved observed=refused source=$(chain_disp "$PROBE_REF") anchor=- at=- verdict=refused") ;;
            esac
            continue
          fi
          disp=$(chain_disp "$PROBE_REF")
          CHAIN_NEAREST='-'; CHAIN_CTX='-'
          if [[ $PROBE == verified ]]; then
            N_VER=$((N_VER + 1)); obs=verified; verdict=match
          else
            N_MISM=$((N_MISM + 1)); obs=anchor-missing; verdict=mismatch
            if [[ $PROBE_KIND == quote ]]; then
              chain_nearest "$PROBE_HAY" "$PROBE_TEXT"
            fi
            emit_finding CHAIN_ANCHOR_NOT_FOUND warn chain \
              "hop=$hop source=$disp anchor=$PROBE_KIND:\"$(printf '%.60s' "$PROBE_TEXT")\" nearest_line=$CHAIN_NEAREST context=$CHAIN_CTX"
          fi
          CHAIN_LINES+=("CHAIN hop=$hop status=resolved observed=$obs source=$disp anchor=$PROBE_KIND:\"$(printf '%.60s' "$PROBE_TEXT")\" at=$PROBE_AT verdict=$verdict")
          ;;
        unresolved|blocked-no-fetch|labelled-dead)
          # r32 C2: a hop whose status says it could not be followed is still
          # audited with the same silent probe. A citation that would verify
          # under the resolved arm is a false unavailability mark:
          # observed=resolvable, exactly one FINDING, drift. Every other such
          # hop stays exempt with no finding — the silence is the contract.
          chain_probe "$hrow"
          if [[ $PROBE == verified ]]; then
            N_RESOLVABLE=$((N_RESOLVABLE + 1))
            emit_finding CHAIN_EXEMPT_RESOLVABLE warn chain \
              "hop=$hop status=$st source=$(chain_disp "$PROBE_REF") anchor=$PROBE_KIND:\"$(printf '%.60s' "$PROBE_TEXT")\" at=$PROBE_AT"
            CHAIN_LINES+=("CHAIN hop=$hop status=$st observed=resolvable source=$(chain_disp "$PROBE_REF") anchor=$PROBE_KIND:\"$(printf '%.60s' "$PROBE_TEXT")\" at=$PROBE_AT verdict=mismatch")
          else
            N_EXEMPT=$((N_EXEMPT + 1))
            CHAIN_LINES+=("CHAIN hop=$hop status=$st observed=exempt source=$(chain_disp "$(norm_ptr "$(chain_cell "$hrow" to)")") anchor=- at=- verdict=exempt")
          fi
          ;;
        rejected|not-applicable)
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
  if [[ $((N_VER + N_EXEMPT + N_RESOLVABLE)) -ne $N_HOPS ]]; then ROLL=DRIFT; fi
  printf 'RESOLVED_HOPS=%d/%d\n' "$N_VER" "$N_HOPS"
  printf 'RESEARCH_GATE: %s (hops=%d verified=%d exempt=%d anchor-missing=%d refused=%d invalid=%d findings=%d drift=%d resolvable=%d)\n' \
    "$ROLL" "$N_HOPS" "$N_VER" "$N_EXEMPT" "$N_MISM" "$N_REFUSED" "$N_INVALID" "$N_FINDINGS" "$N_DRIFT" "$N_RESOLVABLE"

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
      # r19: the base check alone is not enough — a wildcard inside an
      # in-root directory can match a symlink whose target is outside the
      # allowed roots. Canonicalize every expanded match and refuse the
      # whole sweep if any match resolves outside root_r/lane_r.
      local root_r lane_r match_canon match_escape=0
      root_r=$(cd -- "$ROOT" 2>/dev/null && pwd -P || printf '%s' "$ROOT")
      lane_r=$(cd -- "$LANE_ROOT" 2>/dev/null && pwd -P || printf '%s' "$LANE_ROOT")
      for m in "${hit_list[@]+"${hit_list[@]}"}"; do
        [[ $m == /* ]] || m=$ROOT/$m
        match_canon=$(readlink -f -- "$m" 2>/dev/null || printf '%s' "$m")
        if ! in_root "$match_canon" "$root_r" && ! in_root "$match_canon" "$lane_r"; then
          match_escape=1
          break
        fi
      done
      hits=${#hit_list[@]}
      first=-
      [[ $hits -gt 0 ]] && first=${hit_list[0]}
      if [[ $match_escape -eq 1 ]]; then
        N_SW_REF=$((N_SW_REF + 1))
        emit_finding SWEEP_LOCATION_OUT_OF_CORPUS crit sweeps \
          "id=$sid where=$(chain_disp "$whr") match=$(chain_disp "$match_canon") refused (symlink escape; not opened)"
        SWEEP_LINES+=("SWEEP id=$sid where=$(chain_disp "$whr") looked=local hits=- at=- observed=refused verdict=refused")
      elif [[ $hits -gt 0 ]]; then
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

# ---- metadata mode: bounded header screen for knowledge-entry metadata ----

metadata_iso_date() {
  local LC_ALL=C
  [[ $1 =~ ^([0-9]{4})-([0-9]{2})-([0-9]{2})$ ]] || return 1
  local year=$((10#${BASH_REMATCH[1]})) month=$((10#${BASH_REMATCH[2]}))
  local day=$((10#${BASH_REMATCH[3]})) maxday=31
  ((year >= 1 && month >= 1 && month <= 12 && day >= 1)) || return 1
  case "$month" in
    4|6|9|11) maxday=30 ;;
    2)
      maxday=28
      if ((year % 400 == 0 || (year % 4 == 0 && year % 100 != 0))); then maxday=29; fi
      ;;
  esac
  ((day <= maxday))
}

metadata_days_from_civil() { # YEAR MONTH DAY -> META_DAYS (days since 1970-01-01)
  local year=$1 month=$2 day=$3 era yoe doy doe
  if ((month <= 2)); then year=$((year - 1)); fi
  if ((year >= 0)); then era=$((year / 400)); else era=$(((year - 399) / 400)); fi
  yoe=$((year - era * 400))
  if ((month > 2)); then
    doy=$(((153 * (month - 3) + 2) / 5 + day - 1))
  else
    doy=$(((153 * (month + 9) + 2) / 5 + day - 1))
  fi
  doe=$((yoe * 365 + yoe / 4 - yoe / 100 + doy))
  META_DAYS=$((era * 146097 + doe - 719468))
}

metadata_civil_from_days() { # META_DAYS -> META_DATE_RESULT (YYYY-MM-DD)
  local z=$(( $1 + 719468 )) era doe yoe year doy mp month day
  if ((z >= 0)); then era=$((z / 146097)); else era=$(((z - 146096) / 146097)); fi
  doe=$((z - era * 146097))
  yoe=$(((doe - doe / 1460 + doe / 36524 - doe / 146096) / 365))
  year=$((yoe + era * 400))
  doy=$((doe - (365 * yoe + yoe / 4 - yoe / 100)))
  mp=$(((5 * doy + 2) / 153))
  day=$((doy - (153 * mp + 2) / 5 + 1))
  if ((mp < 10)); then month=$((mp + 3)); else month=$((mp - 9)); fi
  if ((month <= 2)); then year=$((year + 1)); fi
  printf -v META_DATE_RESULT '%04d-%02d-%02d' "$year" "$month" "$day"
}

metadata_days_from_iso() { # YYYY-MM-DD -> META_DAYS
  local year=${1:0:4} month=${1:5:2} day=${1:8:2}
  metadata_days_from_civil "$((10#$year))" "$((10#$month))" "$((10#$day))"
}

metadata_add_days() { # VALID_DATE DECIMAL_DAYS -> META_DATE_RESULT; out of range = 1
  local LC_ALL=C
  local date=$1 digits=$2 year month day start last_day amount
  metadata_iso_date "$date" || return 1
  [[ $digits =~ ^[0123456789]+$ ]] || return 1
  # Normalize decimal text before bounding; only supported-sized values reach arithmetic.
  # Capture the significant suffix in one ERE pass; extglob recurses on long zero runs.
  [[ $digits =~ ^0*([123456789][0123456789]*)?$ ]] || return 1
  digits=${BASH_REMATCH[1]:-}
  [[ -n $digits ]] || digits=0
  (( ${#digits} <= 7 )) || return 1
  amount=$((10#$digits))
  year=${date:0:4}; month=${date:5:2}; day=${date:8:2}
  metadata_days_from_civil "$((10#$year))" "$((10#$month))" "$((10#$day))"
  start=$META_DAYS
  metadata_days_from_civil 9999 12 31
  last_day=$META_DAYS
  ((amount <= last_day - start)) || return 1
  metadata_civil_from_days "$((start + amount))"
}

metadata_registry_load() {
  local path=$1 canon fdpath fdcanon probe refuse='' registry_fd read_rc=0
  local content='' fsize links line row cell i header_candidate=0 header_found=0 header_width=0
  local id_col=-1 status_col=-1 usedby_col=-1 is_separator
  local row_id row_status row_usedby split_row
  local LC_ALL=C
  local -a cells=()

  [[ -n $path ]] || die_usage "--registry needs PATH"
  [[ -e $path ]] || die_usage "metadata registry not found"
  [[ -r $path ]] || die_usage "metadata registry unreadable"
  [[ -f $path ]] || die_usage "metadata registry is not a regular file"

  canon=$(readlink -f -- "$path" 2>/dev/null || printf '%s' "$path")
  if is_denylist_fs_path "$path" || is_denylist_fs_path "$canon"; then
    refuse=denylist
  elif ! exec {registry_fd}<"$canon"; then
    refuse=unreadable
  else
    fdpath="/proc/$$/fd/$registry_fd"
    fdcanon=$(readlink -f -- "$fdpath" 2>/dev/null || true)
    if [[ -z $fdcanon ]] || is_denylist_fs_path "$fdcanon"; then
      refuse=denylist
    elif [[ ! -f $fdpath ]] || ! probe=$(stat -Lc '%s %h' -- "$fdpath" 2>/dev/null) \
      || [[ ! $probe =~ ^([0-9]+)[[:space:]]+([0-9]+)$ ]]; then
      refuse=stat
    else
      fsize=${BASH_REMATCH[1]}; links=${BASH_REMATCH[2]}
      if ((links != 1)); then
        refuse=multilink
      elif ((fsize > SOURCE_READ_MAX_BYTES)); then
        refuse=size
      else
        IFS= read -r -d '' -n "$((SOURCE_READ_MAX_BYTES + 1))" content \
          <&"$registry_fd" || read_rc=$?
        if ((${#content} > SOURCE_READ_MAX_BYTES)); then
          refuse=size
        elif ((read_rc == 0)); then
          refuse=nul
        elif ((read_rc != 1)); then
          refuse=read
        fi
      fi
    fi
    exec {registry_fd}<&-
  fi
  [[ -z $refuse ]] || die_usage "metadata registry refused: $refuse"
  declare -gA META_REGISTRY_STATUS=() META_REGISTRY_USEDBY=()

  while IFS= read -r line || [[ -n $line ]]; do
    # Strip one trailing CR without the suffix-pattern scan that is quadratic on long lines.
    if [[ $line == *$'\r' ]]; then line=${line:0:${#line}-1}; fi
    if [[ $line != *'|'*'|'* ]]; then
      ((header_found)) && break
      header_candidate=0
      id_col=-1; status_col=-1; usedby_col=-1
      header_width=0
      continue
    fi
    row=$line
    row=${row#"${row%%[![:space:]]*}"}
    row=${row%"${row##*[![:space:]]}"}
    [[ $row == '|'* ]] && row=${row#|}
    [[ $row == *'|' && $row != *'\|' ]] && row=${row%|}
    # Let read honor escaped pipes, but preserve every other literal backslash.
    # Header indexes, delimiter width, and body cells must use the same split.
    split_row=${row//\\/\\\\}
    split_row=${split_row//'\\|'/'\|'}
    IFS='|' read -a cells <<<"${split_row}|__chousa_registry_end__"
    cells=("${cells[@]:0:${#cells[@]}-1}")
    for i in "${!cells[@]}"; do
      cell=${cells[$i]}
      cell=${cell#"${cell%%[![:space:]]*}"}
      cell=${cell%"${cell##*[![:space:]]}"}
      cells[$i]=$cell
    done

    if ((header_found)); then
      row_id=${cells[$id_col]-}
      if [[ $row_id =~ ^S[0-9]{3,}$ ]] \
          && [[ -z ${META_REGISTRY_STATUS[$row_id]+x} ]]; then
        row_status=${cells[$status_col]-}
        row_usedby=${cells[$usedby_col]-}
        META_REGISTRY_STATUS[$row_id]=$row_status
        META_REGISTRY_USEDBY[$row_id]=$row_usedby
      fi
      continue
    fi

    if ((header_candidate)); then
      is_separator=1
      (( ${#cells[@]} == header_width )) || is_separator=0
      if ((is_separator)); then
        for cell in "${cells[@]}"; do
          [[ $cell =~ ^:?-{3,}:?$ ]] || { is_separator=0; break; }
        done
      fi
      if ((is_separator)); then
        header_found=1
        header_candidate=0
        continue
      fi
      header_candidate=0
      id_col=-1; status_col=-1; usedby_col=-1
      header_width=0
    fi
    for i in "${!cells[@]}"; do
      case "${cells[$i]}" in
        id) if ((id_col < 0)); then id_col=$i; fi ;;
        status) if ((status_col < 0)); then status_col=$i; fi ;;
        used-by) if ((usedby_col < 0)); then usedby_col=$i; fi ;;
      esac
    done
    if ((id_col >= 0 && status_col >= 0 && usedby_col >= 0)); then
      header_candidate=1
      header_width=${#cells[@]}
    else
      id_col=-1; status_col=-1; usedby_col=-1
      header_width=0
    fi
  done <<<"$content"
  ((header_found)) || die_usage "metadata registry has no table with id, status, and used-by columns"
}

metadata_registry_check_source() {
  local source_value=$1 entry_path=$2 entry_base=$3
  local source_id source_tokens source_ids='' scan_rc=0 found_id=0 used_by token matched i
  local LC_ALL=C
  local -a used_by_tokens=()
  # Keep byte-oriented ASCII token boundaries independent of grep -w's Unicode
  # interpretation. Capture stages separately: pipefail would hide an early
  # scanner error (2) behind the final filter's ordinary no-match status (1).
  source_tokens=$(printf '%s\n' "$source_value" | LC_ALL=C grep -oE '[[:alnum:]_]+') || scan_rc=$?
  if ((scan_rc == 0)); then
    source_ids=$(printf '%s\n' "$source_tokens" | LC_ALL=C grep -xE 'S[0-9]{3,}') || scan_rc=$?
  fi
  unset source_tokens
  if ((scan_rc > 1)); then
    emit_finding META_SOURCE_SCAN_FAILED crit metadata \
      "entry=$entry_base source-id scanner failed; registry relationship unknown"
    return 0
  fi
  while IFS= read -r source_id; do
    [[ $source_id =~ ^S[0-9]{3,}$ ]] || continue
    found_id=1
    if [[ -z ${META_REGISTRY_STATUS[$source_id]+x} ]]; then
      emit_finding META_SOURCE_ROW_MISSING warn metadata \
        "entry=$entry_base source_id=$source_id registry row missing"
    elif [[ ${META_REGISTRY_STATUS[$source_id]} != mined ]]; then
      emit_finding META_SOURCE_NOT_MINED warn metadata \
        "entry=$entry_base source_id=$source_id registry row is not mined"
    else
      used_by=${META_REGISTRY_USEDBY[$source_id]}
      IFS=',' read -r -a used_by_tokens <<<"$used_by"
      matched=0
      for i in "${!used_by_tokens[@]}"; do
        token=${used_by_tokens[$i]}
        token=${token#"${token%%[![:space:]]*}"}
        token=${token%"${token##*[![:space:]]}"}
        while [[ $token == ./* ]]; do token=${token#./}; done
        [[ -n $entry_path && $token == "$entry_path" ]] && matched=1
      done
      if ((matched == 0)); then
        emit_finding META_SOURCE_USEDBY_MISSING warn metadata \
          "entry=$entry_base source_id=$source_id used-by does not name entry"
      fi
    fi
  done <<<"$source_ids"
  ((found_id)) || emit_finding META_SOURCE_NO_ROW_ID info metadata \
    "entry=$entry_base source has no S-id"
}

metadata_registry_entry_path() {
  local file=$1 root=$2 entry_path
  if [[ $root == / ]]; then
    [[ $file == /* ]] || { printf ''; return 0; }
    entry_path=${file#/}
  elif [[ $file == "$root/"* ]]; then
    entry_path=${file#"$root"/}
  else
    printf ''
    return 0
  fi
  printf '%s' "$entry_path"
}

metadata_verified_at_bare() {
  local value=$1 rest
  [[ $value =~ ^[[:space:]]*([0-9]{4}-[0-9]{2}-[0-9]{2}) ]] || return 1
  rest=${value#*"${BASH_REMATCH[1]}"}
  [[ ! $rest =~ [^[:space:]] ]]
}

verify_metadata() {
  local path=${1:-} file base line fence_char='' fence_len=0 fence_c fence_l
  local key rest active_key='' source_state verified_state recheck_state
  local has_source has_verified has_recheck source_value verified_value recheck_value
  local recheck_first entry_drift_start entry_complete complete=0
  local due_date freshness cadence_days verified_first freshness_fields asof_days due_days
  local asof_year asof_month asof_day
  local canon refuse fsize links meta_fd fdpath fdcanon probe content read_rc
  local registry_root entry_path
  local LC_ALL=C
  local -a files=() candidates=() metadata_lines=()
  local had_nullglob=0 candidate
  local ROOT_PARENT_RE='(^|[^[:alnum:]_-])--root[[:space:]]+\.\.($|[^[:alnum:]_./-])'

  [[ -n $path ]] || die_usage "metadata path required (verify-metadata PATH)"
  [[ -e $path ]] || die_usage "metadata path not found: $path"
  [[ -r $path ]] || die_usage "metadata path unreadable: $path"
  [[ -d $ROOT ]] || die_usage "root is not a directory: $ROOT (--root)"
  if (( AS_OF_ARG_SET )); then
    asof_year=${AS_OF_ARG:0:4}; asof_month=${AS_OF_ARG:5:2}; asof_day=${AS_OF_ARG:8:2}
    metadata_days_from_civil "$((10#$asof_year))" "$((10#$asof_month))" "$((10#$asof_day))"
    asof_days=$META_DAYS
  fi

  if [[ -d $path ]]; then
    shopt -q nullglob && had_nullglob=1
    shopt -s nullglob
    candidates=("$path"/*.md)
    if (( had_nullglob == 0 )); then shopt -u nullglob; fi
    for candidate in "${candidates[@]}"; do
      [[ -f $candidate ]] || continue
      [[ -r $candidate ]] || die_usage "metadata entry unreadable: $candidate"
      files+=("$candidate")
    done
    ((${#files[@]} > 0)) || die_usage "metadata directory has no .md files: $path"
  else
    [[ -f $path && $path == *.md ]] \
      || die_usage "metadata path is not a .md file or directory: $path"
    files=("$path")
  fi
  if ((REGISTRY_ARG_SET)); then
    metadata_registry_load "$REGISTRY_ARG"
    registry_root=$(cd -- "$ROOT" 2>/dev/null && pwd -P) \
      || die_usage "root is not a directory: $ROOT (--root)"
  fi

  FINDING_LINES=(); N_FINDINGS=0; N_DRIFT=0; ROLL=CLEAN
  for file in "${files[@]}"; do
    printf -v base '%q' "${file##*/}"
    # Bind all metadata probes and parsing to one opened object, not repeated
    # pathname opens. Refuse multi-linked entries like the source chokepoint.
    # No wc fallback: an unavailable stat must not read an oversized file.
    canon=$(readlink -f -- "$file" 2>/dev/null || printf '%s' "$file")
    refuse=''; content=''
    if is_denylist_fs_path "$file" || is_denylist_fs_path "$canon"; then
      refuse=denylist
    elif ! exec {meta_fd}<"$canon"; then
      refuse=unreadable
    else
      fdpath="/proc/$$/fd/$meta_fd"
      fdcanon=$(readlink -f -- "$fdpath" 2>/dev/null || true)
      if [[ -z $fdcanon ]] || is_denylist_fs_path "$fdcanon"; then
        refuse=denylist
      elif [[ ! -f $fdpath ]] || ! probe=$(stat -Lc '%s %h' -- "$fdpath" 2>/dev/null) \
        || [[ ! $probe =~ ^([0-9]+)[[:space:]]+([0-9]+)$ ]]; then
        refuse=stat
      else
        fsize=${BASH_REMATCH[1]}; links=${BASH_REMATCH[2]}
        if ((links != 1)); then
          refuse=multilink
        elif ((fsize > SOURCE_READ_MAX_BYTES)); then
          refuse=size
        else
          # One bounded read creates the exact snapshot later parsed. `-d ''`
          # stops at NUL; -n also bounds growth after stat to cap+1 bytes.
          read_rc=0
          IFS= read -r -d '' -n "$((SOURCE_READ_MAX_BYTES + 1))" content <&"$meta_fd" || read_rc=$?
          if ((${#content} > SOURCE_READ_MAX_BYTES)); then
            refuse=size
          elif ((read_rc == 0)); then
            refuse=nul
          elif ((read_rc != 1)); then
            refuse=read
          fi
        fi
      fi
      exec {meta_fd}<&-
    fi
    if [[ -n $refuse ]]; then
      emit_finding META_ENTRY_REFUSED crit metadata "entry=$base reason=$refuse unparsed"
      freshness_fields=''
      if (( AS_OF_ARG_SET )); then
        freshness_fields=' due=refused freshness=refused'
      fi
      metadata_lines+=("META entry=$base source=refused verified_at=refused recheck=refused${freshness_fields} verdict=drift")
      continue
    fi
    fence_char='' fence_len=0 active_key=''
    has_source=0 has_verified=0 has_recheck=0
    if ((REGISTRY_ARG_SET)); then source_value=''; fi
    verified_value='' recheck_value=''
    while IFS= read -r line || [[ -n $line ]]; do
      if [[ $line == *$'\r' ]]; then line=${line:0:${#line}-1}; fi
      if [[ $line =~ ^[[:space:]]*$ ]]; then active_key=''; fi
      if [[ -n $fence_char ]]; then
        case "$active_key" in
          source) source_value+=$'\n'"$line" ;;
          verified-at) verified_value+=$'\n'"$line" ;;
          recheck) recheck_value+=$'\n'"$line" ;;
        esac
        if [[ $line =~ ^\ {0,3}(\`{3,}|~{3,})[[:space:]]*$ ]]; then
          fence_c=${BASH_REMATCH[1]:0:1}; fence_l=${#BASH_REMATCH[1]}
          [[ $fence_c == "$fence_char" && $fence_l -ge $fence_len ]] \
            && fence_char=''
        fi
        continue
      fi
      if [[ $line =~ ^\ {0,3}(\`{3,}|~{3,})(.*)$ ]]; then
        case "$active_key" in
          source) source_value+=$'\n'"$line" ;;
          verified-at) verified_value+=$'\n'"$line" ;;
          recheck) recheck_value+=$'\n'"$line" ;;
        esac
        fence_char=${BASH_REMATCH[1]:0:1}; fence_len=${#BASH_REMATCH[1]}
        continue
      fi
      [[ $line == '## '* ]] && break
      if [[ $line =~ ^[[:space:]]*$ ]]; then active_key=''; continue; fi
      if [[ $line =~ ^(source|verified-at|recheck):(.*)$ ]]; then
        key=${BASH_REMATCH[1]}; rest=${BASH_REMATCH[2]}
        active_key=''
        case "$key" in
          source)
            has_source=1
            if ((REGISTRY_ARG_SET)); then
              active_key=source; source_value=$rest
            fi
            ;;
          verified-at)
            has_verified=1; active_key=verified-at; verified_value=$rest
            ;;
          recheck)
            has_recheck=1; active_key=recheck; recheck_value=$rest
            ;;
        esac
        continue
      fi
      case "$active_key" in
        source) source_value+=$'\n'"$line" ;;
        verified-at) verified_value+=$'\n'"$line" ;;
        recheck) recheck_value+=$'\n'"$line" ;;
      esac
    done <<<"$content"

    recheck_first=''
    entry_drift_start=$N_DRIFT
    entry_complete=1
    if (( has_source )); then
      source_state=present
    else
      source_state=absent; entry_complete=0
      emit_finding META_SOURCE_ABSENT warn metadata "entry=$base key=source absent"
    fi
    if (( REGISTRY_ARG_SET )); then
      entry_path=$(metadata_registry_entry_path "$fdcanon" "$registry_root")
      metadata_registry_check_source "$source_value" "$entry_path" "$base"
    fi
    if (( has_verified )); then
      if [[ $verified_value =~ ^[[:space:]]*[0-9]{4}-[0-9]{2}-[0-9]{2} ]]; then
        verified_state=dated
      else
        verified_state=undated; entry_complete=0
        emit_finding META_VERIFIED_AT_UNDATED warn metadata \
          "entry=$base key=verified-at does not begin YYYY-MM-DD"
      fi
    else
      verified_state=absent; entry_complete=0
      emit_finding META_VERIFIED_AT_ABSENT warn metadata \
        "entry=$base key=verified-at absent"
    fi
    if (( REGISTRY_ARG_SET )) && metadata_verified_at_bare "$verified_value"; then
      emit_finding META_VERIFIED_AT_BARE warn metadata \
        "entry=$base key=verified-at has date only"
    fi
    if (( has_recheck )); then
      if [[ $recheck_value =~ ^[[:space:]]*([^[:space:]]+) ]]; then
        recheck_first=${BASH_REMATCH[1]}
      else
        recheck_first=''
      fi
      if metadata_iso_date "$recheck_first" \
         || [[ $recheck_first =~ ^[0-9]+d$ || $recheck_first == on-release ]]; then
        recheck_state=scheduled
      else
        recheck_state=unscheduled
        emit_finding META_RECHECK_UNSCHEDULED info metadata \
          "entry=$base key=recheck unscheduled"
      fi
      if [[ $recheck_value =~ $ROOT_PARENT_RE ]]; then
        emit_finding META_RECHECK_ROOT_PARENT info metadata \
          "entry=$base recheck uses --root .."
      fi
    else
      recheck_state=absent; entry_complete=0
      emit_finding META_RECHECK_ABSENT warn metadata "entry=$base key=recheck absent"
    fi
    freshness_fields=''
    if (( AS_OF_ARG_SET )); then
      due_date=unknown; freshness=unknown
      if metadata_iso_date "$recheck_first"; then
        due_date=$recheck_first; freshness=current
      elif [[ $recheck_first =~ ^([0-9]+)d$ ]]; then
        cadence_days=${BASH_REMATCH[1]}
        verified_first=''
        if [[ $verified_value =~ ^[[:space:]]*([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
          verified_first=${BASH_REMATCH[1]}
        fi
        if metadata_iso_date "$verified_first" \
           && metadata_add_days "$verified_first" "$cadence_days"; then
          due_date=$META_DATE_RESULT; freshness=current
        fi
      elif [[ $recheck_first == on-release ]]; then
        due_date=on-release; freshness=event
      fi
      if [[ $freshness == current ]]; then
        metadata_days_from_iso "$due_date"; due_days=$META_DAYS
        if ((asof_days > due_days)); then freshness=overdue; fi
        if [[ $freshness == overdue ]]; then
          emit_finding META_RECHECK_OVERDUE warn metadata \
            "entry=$base due=$due_date as_of=$AS_OF_ARG"
        fi
      fi
      freshness_fields=" due=$due_date freshness=$freshness"
    fi
    (( entry_complete )) && complete=$((complete + 1))
    if (( N_DRIFT > entry_drift_start )); then
      metadata_lines+=("META entry=$base source=$source_state verified_at=$verified_state recheck=$recheck_state${freshness_fields} verdict=drift")
    else
      metadata_lines+=("META entry=$base source=$source_state verified_at=$verified_state recheck=$recheck_state${freshness_fields} verdict=clean")
    fi
  done

  printf 'research-gate %s — ts=%s — mode=verify-metadata — path=%q — root=%q\n' \
    "$VERSION" "$TS_UTC" "$path" "$ROOT"
  for line in "${metadata_lines[@]+"${metadata_lines[@]}"}"; do printf '%s\n' "$line"; done
  for line in "${FINDING_LINES[@]+"${FINDING_LINES[@]}"}"; do printf '%s\n' "$line"; done
  printf 'METADATA_COMPLETE=%d/%d\n' "$complete" "${#files[@]}"
  printf 'RESEARCH_GATE: %s (entries=%d complete=%d findings=%d drift=%d)\n' \
    "$ROLL" "${#files[@]}" "$complete" "$N_FINDINGS" "$N_DRIFT"

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
    # The append below must read the manifest's last byte to keep JSONL
    # delimiting; a non-empty manifest it cannot read is refused before any
    # write rather than appended to blind (r24).
    if [[ -s $JSON_ARG && ! -r $JSON_ARG ]]; then
      die_usage "manifest unreadable: $JSON_ARG (--json; its last byte decides the delimiter)"
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
    # A manifest whose last byte is not '\n' (hand-edited, truncated, or
    # written by another tool) would glue this object onto its last line —
    # `{"prior":true}{"schema":...}` — invalid JSONL. Terminate it first;
    # an empty or newline-terminated manifest is appended to unchanged (r24).
    # The last byte is read as hex: a bare $(tail -c1) drops NUL bytes and
    # would miss a NUL-terminated manifest. (Unreadable + non-empty is
    # refused at setup, before any write.)
    #
    # The probe and the append are ONE critical section (r32 C1). At base they
    # were two operations with no lock, so two appenders that both saw an
    # unterminated last line both prefixed a newline and left a blank line
    # (r24 delimiter edge). The manifest is opened for append on a dedicated
    # fd (O_APPEND; created when absent, never truncated, so the inode and the
    # prior bytes survive), a blocking exclusive flock(2) is taken on THAT open
    # file description before the last byte is read, and it is held until this
    # run's line is written; the close then releases it. flock's fd form locks
    # the shell's own description, so the lock outlives the flock(1) helper
    # and a cooperating LOCK_EX holder on the manifest excludes both the probe
    # and the append. The wait is unbounded (LOCK_EX blocks, as the contract
    # states); a host without flock(1) cannot serialize, so it fails closed
    # instead of appending unlocked.
    if ! command -v flock >/dev/null 2>&1; then
      printf 'research-gate: flock(1) unavailable; manifest not written: %s\n' "$JSON_ARG" >&2
      exit 2
    fi
    local jfd='' jlast=''
    if ! exec {jfd}>>"$JSON_ARG"; then
      printf 'research-gate: manifest open failed: %s\n' "$JSON_ARG" >&2
      exit 2
    fi
    if ! flock -x "$jfd"; then
      printf 'research-gate: manifest lock failed: %s\n' "$JSON_ARG" >&2
      exit 2
    fi
    # Probe the file the locked fd refers to, not the path: if PATH is a
    # symlink retargeted after the open, a path probe would read another
    # file's last byte while the append goes to the locked one (SentinelC1After,
    # round 32). /proc/$$/fd/N reopens the fd's own inode; without /proc the
    # path is the only handle.
    local jprobe=$JSON_ARG
    if [[ -e /proc/$$/fd/$jfd ]]; then
      jprobe=/proc/$$/fd/$jfd
    fi
    if [[ -s $jprobe ]]; then
      jlast=$(tail -c1 -- "$jprobe" 2>/dev/null | od -An -tx1 | tr -d ' \n' || true)
      # Non-empty but unreadable now (setup admits an empty unreadable
      # manifest; a cooperating writer may have filled it before this lock):
      # the delimiter cannot be decided, so refuse rather than glue
      # (CriticC1Contract, round 32).
      if [[ -z $jlast ]]; then
        exec {jfd}>&-
        printf 'research-gate: manifest unreadable under lock (its last byte decides the delimiter): %s\n' "$JSON_ARG" >&2
        exit 2
      fi
    fi
    if [[ -n $jlast && $jlast != 0a ]]; then
      line=$'\n'$line
    fi
    if ! printf '%s\n' "$line" >&"$jfd"; then
      printf 'research-gate: manifest append failed: %s\n' "$JSON_ARG" >&2
      exit 2
    fi
    exec {jfd}>&-
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
  local cases=0 failures=0 zero_prefix='' unicode_locale='' candidate_locale
  local plain_rc=0 plain_out='' plain_fields=0 plain_verdicts=0
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

  # 120-122 (r19): the sweeps symlink escape — the base check canonicalizes
  # the glob's literal directory but not each match, so a wildcard inside
  # an in-root dir can match a symlink whose target is outside the allowed
  # roots. The fix canonicalizes every expanded match; any escape refuses
  # the whole sweep.
  # 120: outside leaf symlink — sweepdir/escape.md -> OUTSIDE_FILE (outside
  # $WORK); sweepdir/*.md must refuse (pre-fix: SWEEP_CLAIM_FALSE hit).
  mkdir -p "$WORK/sweepdir"
  ln -s "$OUTSIDE_FILE" "$WORK/sweepdir/escape.md"
  write_rec sweeps-symlink-escape <<'EOF'
# research-record v1
## Sweeps
| id | where | query | expected |
|---|---|---|---|
| W1 | sweepdir/*.md | escape-check | no hits |
EOF
  tsweeps sweeps-symlink-escape 1 'RESEARCH_GATE: DRIFT' \
    'FINDING SWEEP_LOCATION_OUT_OF_CORPUS severity=crit surface=sweeps' \
    'observed=refused verdict=refused'
  # 121: outside dir symlink — sweepdir2/linkdir -> a dir outside $WORK;
  # sweepdir2/*/*.md traverses the symlink to outside files (pre-fix:
  # SWEEP_CLAIM_FALSE hit). The outside dir is created as a sibling of WORK
  # so it shares the filesystem but is outside the allowed root.
  mkdir -p "$WORK/../chousa-outside-r19" "$WORK/sweepdir2"
  printf 'nested outside\n' >"$WORK/../chousa-outside-r19/nested.md"
  ln -s "$WORK/../chousa-outside-r19" "$WORK/sweepdir2/linkdir"
  write_rec sweeps-symlink-dir <<'EOF'
# research-record v1
## Sweeps
| id | where | query | expected |
|---|---|---|---|
| W1 | sweepdir2/*/*.md | dir-escape-check | no hits |
EOF
  tsweeps sweeps-symlink-dir 1 'RESEARCH_GATE: DRIFT' \
    'FINDING SWEEP_LOCATION_OUT_OF_CORPUS severity=crit surface=sweeps' \
    'observed=refused verdict=refused'
  # 122: in-root symlink control — safe/alias.md -> target/inside.md (both
  # in-root); safe/*.md must NOT refuse the boundary (the symlink resolves
  # inside the allowed root — normal hit semantics still apply).
  mkdir -p "$WORK/safe" "$WORK/target"
  printf 'in-root content\n' >"$WORK/target/inside.md"
  ln -s "$WORK/target/inside.md" "$WORK/safe/alias.md"
  write_rec sweeps-inroot-symlink <<'EOF'
# research-record v1
## Sweeps
| id | where | query | expected |
|---|---|---|---|
| W1 | safe/*.md | inroot-check | no hits |
EOF
  tsweeps sweeps-inroot-symlink 1 'RESEARCH_GATE: DRIFT' \
    'SWEEP_CLAIM_FALSE' 'observed=hit verdict=mismatch'

  # 123: the exact-cap source's only match is at EOF, exercising the long-prefix
  # path through the shared token-boundary matcher without committing binary data.
  { head -c $((SOURCE_READ_MAX_BYTES - ${#cap_span} - 1)) /dev/zero | tr '\0' a; printf ' %s' "$cap_span"; } >"$WORK/claimsrc/cap-eof.md"
  printf '{"id":"Z3","source":"claimsrc/cap-eof.md","span":"%s","expect":"supported"}\n' \
    "$cap_span" >"$WORK/claims-cap-eof.jsonl"
  tclaims claims-cap-eof 0 'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=1/1' \
    'CLAIM id=Z3 expected=supported observed=supported source=claimsrc/cap-eof.md at=line:1 verdict=match'

  # 124 (r20): the HTML-comment heading shadow — a `## ` inside <!-- --> is
  # literal text, not a heading. Same class as the fenced-heading shadow
  # (r17): a `## Meta` inside an HTML comment must not reset the real Meta
  # body. The parser now tracks comment state alongside fence state.
  add_scope_row scope-comment-shadow domain 'bounty program scope and claim packages'
  cat >>"$WORK/scope-comment-shadow.md" <<'EOF'
## Notes
<!--
## Meta
| key | value |
|---|---|
| domain | deep-research method |
-->
EOF
  tcase scope-comment-shadow 1 'RESEARCH_GATE: DRIFT' \
    'FINDING SCOPE_BOUNTY_ABSORBED severity=warn surface=scope' 'findings=1 drift=1'

  # 125-128 (r21): ptr_resolves_meta boundary — relative pointers were
  # checked with raw -f (no canonicalization), so 'lib/../../etc/passwd'
  # and symlinks to outside passed; absolute pointers checked root_r only
  # (lane-root pointers refused). The fix canonicalizes the candidate and
  # checks in_root against both roots; the denylist applies to the
  # canonical target too.
  # 125: traversal — lib/../../etc/passwd where the file exists under the
  # raw path but canonicalizes outside (pre-fix: accepted).
  mkdir -p "$WORK/lib"
  printf 'x\n' >"$WORK/../chousa-outside-r21.txt"
  write_rec ptr-traversal <<'EOF'
# research-record v1
## Meta
| key | value |
|---|---|
| window | loopback |
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/../../chousa-outside-r21.txt |
EOF
  tcase ptr-traversal 1 'RESEARCH_GATE: DRIFT' \
    'FINDING POINTER_UNRESOLVED severity=warn surface=sources'
  # 126: symlink pointer — lib/link.md -> outside file (pre-fix: -f passed).
  mkdir -p "$WORK/lib"
  ln -s "$WORK/../chousa-outside-r21.txt" "$WORK/lib/link.md"
  write_rec ptr-symlink <<'EOF'
# research-record v1
## Meta
| key | value |
|---|---|
| window | loopback |
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/link.md |
EOF
  tcase ptr-symlink 1 'RESEARCH_GATE: DRIFT' \
    'FINDING POINTER_UNRESOLVED severity=warn surface=sources'
  # 127: absolute lane-root pointer — an absolute path under LANE_ROOT
  # (pre-fix: refused because only root_r was checked). The fixture uses
  # PROVINCE.md (a real lane-root file) so the pointer resolves.
  write_rec ptr-lane-abs <<'EOF'
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
| S1 | primary | PLACEHOLDER_LANE_ABS |
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
  sed "s|PLACEHOLDER_LANE_ABS|$LANE_ROOT/PROVINCE.md|" "$WORK/ptr-lane-abs.md" >"$WORK/ptr-lane-abs2.md"
  mv "$WORK/ptr-lane-abs2.md" "$WORK/ptr-lane-abs.md"
  tcase ptr-lane-abs 0 'RESEARCH_GATE: CLEAN' 'findings=0 drift=0'
  # 128: .config denylist via canonical target — a benign symlink to a
  # .config file (pre-fix: the citation was clean, target unchecked).
  mkdir -p "$WORK/lib" "$WORK/../chousa-config-r21/.config"
  printf 'secret\n' >"$WORK/../chousa-config-r21/.config/agent-token.txt"
  ln -s "$WORK/../chousa-config-r21/.config/agent-token.txt" "$WORK/lib/benign.md"
  write_rec ptr-deny-symlink <<'EOF'
# research-record v1
## Meta
| key | value |
|---|---|
| window | loopback |
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/benign.md |
EOF
  tcase ptr-deny-symlink 1 'RESEARCH_GATE: DRIFT' \
    'FINDING POINTER_UNRESOLVED severity=warn surface=sources'

  # 133 (r23): the fenced-heading anchor — chain `heading` anchors scanned
  # raw lines with ^#+ and matched headings inside fences (false positive).
  # The fix tracks fence state in chain_anchor_at — a # heading inside a
  # fence is literal, not an anchor target.
  mkdir -p "$WORK/lib"
  cat >"$WORK/lib/fence-target.md" <<'EOF'
# real heading
some text
```
## Phantom Heading
this is inside a fence
```
EOF
  printf '# research-record v1\n## Sources\n| id | tier | pointer |\n|---|---|---|---|\n| S1 | primary | lib/fence-target.md |\n## Chain\n| hop | from | to | status | anchor_kind | anchor |\n|---|---|---|---|---|---|\n| 1 | C1 | S1 | resolved | heading | Phantom Heading |\n' \
    >"$WORK/chain-fence-anchor.md"
  tchain chain-fence-anchor 1 'RESEARCH_GATE: DRIFT' \
    'FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn surface=chain' \
    'CHAIN hop=1 status=resolved observed=anchor-missing' 'RESOLVED_HOPS=0/1'

  # 129-132 (r22): the .config/.omp/.local-state path-start denylist — the
  # */X/* patterns need a leading component; bare-start forms '.config/foo',
  # '.omp/foo', '.local/state/foo' (no './' prefix) passed CLEAN while
  # './.config/foo' refused. The fix adds bare-start patterns.
  # 129: .config path-start — must refuse SESSION_READ.
  printf '{"id":"S1","source":".config/agent-token.txt","span":"secret","expect":"supported"}\n' \
    >"$WORK/claims-config-start.jsonl"
  mkdir -p "$WORK/.config" && printf 'secret\n' >"$WORK/.config/agent-token.txt"
  tclaims claims-config-start 1 'RESEARCH_GATE: DRIFT' \
    'FINDING CLAIM_SOURCE_SESSION severity=crit surface=claims' \
    'CLAIM id=S1 expected=supported observed=refused' 'VERDICT_BEARING_CLAIMS=0/1'
  # 130: .omp path-start — must refuse SESSION_READ.
  printf '{"id":"S1","source":".omp/token.txt","span":"secret","expect":"supported"}\n' \
    >"$WORK/claims-omp-start.jsonl"
  mkdir -p "$WORK/.omp" && printf 'secret\n' >"$WORK/.omp/token.txt"
  tclaims claims-omp-start 1 'RESEARCH_GATE: DRIFT' \
    'FINDING CLAIM_SOURCE_SESSION severity=crit surface=claims' \
    'CLAIM id=S1 expected=supported observed=refused' 'VERDICT_BEARING_CLAIMS=0/1'
  # 131: .local/state path-start — must refuse SESSION_READ.
  printf '{"id":"S1","source":".local/state/cred.txt","span":"secret","expect":"supported"}\n' \
    >"$WORK/claims-localstate-start.jsonl"
  mkdir -p "$WORK/.local/state" && printf 'secret\n' >"$WORK/.local/state/cred.txt"
  tclaims claims-localstate-start 1 'RESEARCH_GATE: DRIFT' \
    'FINDING CLAIM_SOURCE_SESSION severity=crit surface=claims' \
    'CLAIM id=S1 expected=supported observed=refused' 'VERDICT_BEARING_CLAIMS=0/1'
  # 132: benign .config-adjacent path — NOT a denylist hit (the path-start
  # patterns must not over-refuse).
  mkdir -p "$WORK/.config-adjacent" && printf 'line1\n' >"$WORK/.config-adjacent/file.md"
  printf '{"id":"S1","source":".config-adjacent/file.md","span":"line1","expect":"supported"}\n' \
    >"$WORK/claims-config-adjacent.jsonl"
  tclaims claims-config-adjacent 0 'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=1/1'

  # 134–136 (r24): the --json manifest delimiter edge — an append onto a
  # manifest whose last byte is not '\n' glued the new object onto the prior
  # line (`{"prior":true}{"schema":...}`). The fix terminates the prior line
  # first; the prior bytes stay byte-identical (append-only) and no blank line
  # is written. 135: a NUL last byte (a bare $(tail -c1) drops NUL and misses
  # it). 136: a non-empty manifest whose last byte cannot be read is refused
  # before any write (a write-only manifest would otherwise be glued).
  r24_case() { # NAME PRIOR(printf fmt) WANT_RC WANT_LINES PRIOR_IS_JSON [TOKEN]
    local name=$1 prior=$2 want_rc=$3 want_lines=$4 pj=$5 tok=${6:-}
    local f="$WORK/$1.jsonl" rc=0 out msg='' n
    cases=$((cases + 1))
    printf "$prior" >"$f"
    if [[ $name == *unreadable* ]]; then chmod 200 "$f"; fi
    out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 \
      CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
      bash "$SELF" verify-all "$WORK/all-pass.md" --claims "$WORK/claims-pass.jsonl" \
      --json "$f" 2>&1) || rc=$?
    chmod 600 "$f"
    [[ $rc -eq $want_rc ]] || msg+="rc=$rc/$want_rc "
    n=$(wc -l <"$f" | tr -d ' ')
    [[ $n -eq $want_lines ]] || msg+="manifest-lines=$n/$want_lines "
    # -a: GNU grep treats a NUL as a line break in a binary file (case 135).
    [[ $(grep -a -c '^$' -- "$f" || true) -eq 0 ]] || msg+="blank-line "
    if [[ $want_lines -eq 2 ]]; then
      sed -n 2p -- "$f" | grep -q '^{"schema":"chousa-verify-all/v1"' || msg+="schema-not-own-line "
    fi
    if [[ $pj -eq 1 ]]; then
      [[ $(sed -n 1p -- "$f") == '{"prior":true}' ]] || msg+="prior-line-altered "
      if command -v python3 >/dev/null 2>&1; then
        python3 -c 'import json,sys
for ln in sys.stdin.read().splitlines():
    if ln.strip():
        json.loads(ln)' <"$f" >/dev/null 2>&1 || msg+="json-invalid "
      fi
    fi
    if [[ -n $tok && $out != *"$tok"* ]]; then msg+="missing:'$tok' "; fi
    if [[ -z $msg ]]; then
      printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" "$name" "$rc"
    else
      printf 'FAIL-case %-28s %s\n' "$name" "$msg"
      printf '%s\n' "$out" | sed 's/^/    | /'
      failures=$((failures + 1))
    fi
  }
  r24_case json-unterminated-manifest '{"prior":true}' 0 2 1
  r24_case json-nul-terminated-manifest '{"prior":true}\0' 0 2 0
  if [[ $(id -u) -ne 0 ]]; then
    r24_case json-unreadable-manifest '{"prior":true}' 2 0 1 'manifest unreadable'
  else
    cases=$((cases + 1)); SKIPPED=$((SKIPPED + 1))
    printf 'skip-case %-2d %-26s reason=%s\n' "$cases" json-unreadable-manifest 'root reads any file'
  fi

  metadata_case() { # NAME PATH WANT_RC [expected output ... | ENV=VALUE | @order=a,b]
    local name=$1 path=$2 want_rc=$3
    shift 3
    local -a want=() over=()
    local arg rc=0 out nverdict expected_order='' actual_order msg='' tok
    for arg in "$@"; do
      if [[ $arg == @order=* ]]; then
        expected_order=${arg#@order=}
      elif [[ $arg =~ ^[A-Z_]+= ]]; then
        over+=("$arg")
      else
        want+=("$arg")
      fi
    done
    cases=$((cases + 1))
    out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE \
      CHOUSA_STRICT=0 CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
      "${over[@]+"${over[@]}"}" \
      bash "$SELF" verify-metadata "$path" --root "$WORK" 2>&1) || rc=$?
    nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true)
    for tok in "${want[@]+"${want[@]}"}"; do
      [[ $out == *"$tok"* ]] || msg+="missing:'$tok' "
    done
    if [[ $want_rc -eq 2 ]]; then
      [[ ${nverdict:-0} -eq 0 ]] || msg+="verdict-lines=$nverdict/0 "
    else
      [[ ${nverdict:-0} -eq 1 ]] || msg+="verdict-lines=$nverdict/1 "
    fi
    if [[ -n $expected_order ]]; then
      actual_order=$(printf '%s\n' "$out" \
        | sed -n 's/^META entry=\([^ ]*\) .*/\1/p' | paste -sd, -)
      [[ $actual_order == "$expected_order" ]] \
        || msg+="meta-order=$actual_order/$expected_order "
    fi
    if [[ $rc -eq $want_rc && -z $msg ]]; then
      printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" "$name" "$rc"
    else
      printf 'FAIL-case %-28s rc=%d/%d %s\n' "$name" "$rc" "$want_rc" "$msg"
      printf '%s\n' "$out" | sed 's/^/    | /'
      failures=$((failures + 1))
    fi
  }

  cat >"$WORK/meta-clean.md" <<'EOF'
source: S001 https://example.invalid/source#anchor
verified-at: 2026-10-20 checked the claim
recheck: 90d (re-open the source)
## Claim
The body is outside the metadata header.
EOF
  metadata_case metadata-clean "$WORK/meta-clean.md" 0 \
    'META entry=meta-clean.md source=present verified_at=dated recheck=scheduled verdict=clean' \
    'METADATA_COMPLETE=1/1' \
    'RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)'

  cat >"$WORK/meta-no-source.md" <<'EOF'
verified-at: 2026-10-20 checked
recheck: 90d
EOF
  metadata_case metadata-no-source "$WORK/meta-no-source.md" 1 \
    'FINDING META_SOURCE_ABSENT severity=warn surface=metadata obs=entry=meta-no-source.md' \
    'META entry=meta-no-source.md source=absent verified_at=dated recheck=scheduled verdict=drift' \
    'METADATA_COMPLETE=0/1'
  cat >"$WORK/meta-no-verified.md" <<'EOF'
source: S001
recheck: 90d
EOF
  metadata_case metadata-no-verified "$WORK/meta-no-verified.md" 1 \
    'FINDING META_VERIFIED_AT_ABSENT severity=warn surface=metadata obs=entry=meta-no-verified.md' \
    'META entry=meta-no-verified.md source=present verified_at=absent recheck=scheduled verdict=drift' \
    'METADATA_COMPLETE=0/1'
  cat >"$WORK/meta-no-recheck.md" <<'EOF'
source: S001
verified-at: 2026-10-20 checked
EOF
  metadata_case metadata-no-recheck "$WORK/meta-no-recheck.md" 1 \
    'FINDING META_RECHECK_ABSENT severity=warn surface=metadata obs=entry=meta-no-recheck.md' \
    'META entry=meta-no-recheck.md source=present verified_at=dated recheck=absent verdict=drift' \
    'METADATA_COMPLETE=0/1'

  cat >"$WORK/meta-undated.md" <<'EOF'
source: S001
verified-at: sometime yesterday
recheck: on-release
EOF
  metadata_case metadata-undated "$WORK/meta-undated.md" 1 \
    'FINDING META_VERIFIED_AT_UNDATED severity=warn surface=metadata obs=entry=meta-undated.md' \
    'verified_at=undated recheck=scheduled verdict=drift'

  cat >"$WORK/meta-unscheduled.md" <<'EOF'
source: S001
verified-at: 2026-10-20 checked
recheck: when-needed (command follows)
EOF
  metadata_case metadata-unscheduled "$WORK/meta-unscheduled.md" 0 \
    'FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=meta-unscheduled.md' \
    'recheck=unscheduled verdict=clean' 'RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=1 drift=0)'
  metadata_case metadata-unscheduled-strict "$WORK/meta-unscheduled.md" 1 \
    'FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=meta-unscheduled.md' \
    'recheck=unscheduled verdict=drift' 'RESEARCH_GATE: DRIFT (entries=1 complete=1 findings=1 drift=1)' \
    CHOUSA_STRICT=1

  cat >"$WORK/meta-root-parent.md" <<'EOF'
source: S001
verified-at: 2026-10-20 checked
recheck: 90d (`bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..`)
EOF
  metadata_case metadata-root-parent "$WORK/meta-root-parent.md" 0 \
    'FINDING META_RECHECK_ROOT_PARENT severity=info surface=metadata obs=entry=meta-root-parent.md' \
    'recheck=scheduled verdict=clean' 'RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=1 drift=0)'

  cat >"$WORK/meta-fenced.md" <<'EOF'
```yaml
source: S001
verified-at: 2026-10-20 checked
recheck: 90d
```
## Claim
EOF
  metadata_case metadata-fenced "$WORK/meta-fenced.md" 1 \
    'FINDING META_SOURCE_ABSENT severity=warn surface=metadata obs=entry=meta-fenced.md' \
    'FINDING META_VERIFIED_AT_ABSENT severity=warn surface=metadata obs=entry=meta-fenced.md' \
    'FINDING META_RECHECK_ABSENT severity=warn surface=metadata obs=entry=meta-fenced.md' \
    'METADATA_COMPLETE=0/1'

  cat >"$WORK/meta-after-heading.md" <<'EOF'
source: S001
verified-at: 2026-10-20 checked
## Claim
recheck: 90d
EOF
  metadata_case metadata-after-heading "$WORK/meta-after-heading.md" 1 \
    'FINDING META_RECHECK_ABSENT severity=warn surface=metadata obs=entry=meta-after-heading.md' \
    'recheck=absent verdict=drift' 'METADATA_COMPLETE=0/1'

  printf 'source: S001\r\nverified-at: 2026-10-20 checked\r\nrecheck: 365d\r\n## Claim\r\n' \
    >"$WORK/meta-crlf.md"
  metadata_case metadata-crlf "$WORK/meta-crlf.md" 0 \
    'META entry=meta-crlf.md source=present verified_at=dated recheck=scheduled verdict=clean' \
    'METADATA_COMPLETE=1/1' 'RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)'

  mkdir -p "$WORK/meta-directory"
  cat >"$WORK/meta-directory/z.md" <<'EOF'
source: S001
verified-at: 2026-10-20 checked
EOF
  cat >"$WORK/meta-directory/a.md" <<'EOF'
source: S001
verified-at: 2026-10-20 checked
recheck: 180d
EOF
  metadata_case metadata-directory "$WORK/meta-directory" 1 \
    'METADATA_COMPLETE=1/2' \
    'META entry=a.md source=present verified_at=dated recheck=scheduled verdict=clean' \
    'META entry=z.md source=present verified_at=dated recheck=absent verdict=drift' \
    '@order=a.md,z.md'

  metadata_case metadata-missing-path "$WORK/meta-missing.md" 2 \
    'metadata path not found'
  mkdir -p "$WORK/meta-empty-directory"
  metadata_case metadata-empty-directory "$WORK/meta-empty-directory" 2 \
    'metadata directory has no .md files'

  printf 'source: S001\nverified-at: 2026-10-20 checked\nrecheck: 90d\x00\n' \
    >"$WORK/meta-nul.md"
  metadata_case metadata-nul-refused "$WORK/meta-nul.md" 1 \
    'FINDING META_ENTRY_REFUSED severity=crit surface=metadata obs=entry=meta-nul.md reason=nul unparsed' \
    'META entry=meta-nul.md source=refused verified_at=refused recheck=refused verdict=drift' \
    'METADATA_COMPLETE=0/1'
  mkdir -p "$WORK/.config" "$WORK/meta-alias"
  printf 'source: S001\nverified-at: 2026-10-20 checked\nrecheck: 90d\n' \
    >"$WORK/.config/private.md"
  ln -s "$WORK/.config/private.md" "$WORK/meta-alias/alias.md"
  metadata_case metadata-denylist-alias "$WORK/meta-alias" 1 \
    'FINDING META_ENTRY_REFUSED severity=crit surface=metadata obs=entry=alias.md reason=denylist unparsed' \
    'METADATA_COMPLETE=0/1'
  cat >"$WORK/meta-continuation.md" <<'EOF'
source: S001
verified-at: 2026-10-20 checked
recheck: 90d
note: `bash tools/research-gate.sh verify-chain x.md --root ..`
## Claim
EOF
  metadata_case metadata-nonkey-continuation "$WORK/meta-continuation.md" 0 \
    'FINDING META_RECHECK_ROOT_PARENT severity=info surface=metadata obs=entry=meta-continuation.md' \
    'METADATA_COMPLETE=1/1'

  ln -s "$WORK/meta-clean.md" "$WORK/meta-safe-link.md"
  metadata_case metadata-safe-symlink "$WORK/meta-safe-link.md" 0 \
    'METADATA_COMPLETE=1/1' 'findings=0 drift=0'
  cp "$WORK/meta-clean.md" "$WORK/meta-hard-seed.md"
  ln "$WORK/meta-hard-seed.md" "$WORK/meta-hard-alias.md"
  metadata_case metadata-hardlink-refused "$WORK/meta-hard-alias.md" 1 \
    'reason=multilink unparsed' 'METADATA_COMPLETE=0/1'

  mkdir -p "$WORK/meta-stat-fail"
  printf '#!/usr/bin/env bash\nexit 1\n' >"$WORK/meta-stat-fail/stat"
  chmod +x "$WORK/meta-stat-fail/stat"
  metadata_case metadata-stat-unavailable "$WORK/meta-clean.md" 1 \
    'reason=stat unparsed' 'METADATA_COMPLETE=0/1' \
    "PATH=$WORK/meta-stat-fail:$PATH"

  printf 'source: S001\nverified-at: 2026-10-20 checked\nrecheck: 2026-02-30\n' \
    >"$WORK/meta-invalid-date.md"
  metadata_case metadata-invalid-calendar "$WORK/meta-invalid-date.md" 0 \
    'META_RECHECK_UNSCHEDULED' 'recheck=unscheduled verdict=clean'
  printf 'source: S001\nverified-at: 2026-10-20 checked\n##\tLiteral\nrecheck: 90d\n' \
    >"$WORK/meta-tab-heading.md"
  metadata_case metadata-literal-heading "$WORK/meta-tab-heading.md" 0 \
    'recheck=scheduled verdict=clean' 'METADATA_COMPLETE=1/1'

  printf 'source: S001\nverified-at: 2026-10-20 checked\nrecheck: FAKE_TOKEN_MUST_NOT_ECHO\n' \
    >"$WORK/meta-noecho.md"
  cases=$((cases + 1)); rc=0
  out=$(CHOUSA_STRICT=0 bash "$SELF" verify-metadata "$WORK/meta-noecho.md" --root "$WORK" 2>&1) || rc=$?
  if [[ $rc -eq 0 && $out == *META_RECHECK_UNSCHEDULED* && $out != *FAKE_TOKEN_MUST_NOT_ECHO* ]]; then
    printf 'ok-case  %-2d %-28s exit=0\n' "$cases" metadata-no-content-echo
  else
    printf 'FAIL-case %-28s token echoed or finding lost\n' metadata-no-content-echo
    failures=$((failures + 1))
  fi

  # Swap the caller pathname after stat: parsing must still use the originally
  # opened inode, not re-open the replacement denylisted symlink.
  mkdir -p "$WORK/meta-stat-swap" "$WORK/credentials"
  cp "$WORK/meta-clean.md" "$WORK/meta-race.md"
  cp "$WORK/meta-noecho.md" "$WORK/credentials/fake.md"
  cat >"$WORK/meta-stat-swap/stat" <<'EOF'
#!/usr/bin/env bash
/usr/bin/stat "$@" || exit $?
if [[ -n ${META_RACE_PATH:-} ]]; then
  rm -- "$META_RACE_PATH"
  ln -s "$META_RACE_TARGET" "$META_RACE_PATH"
fi
EOF
  chmod +x "$WORK/meta-stat-swap/stat"
  metadata_case metadata-stable-object "$WORK/meta-race.md" 0 \
    'findings=0 drift=0' 'METADATA_COMPLETE=1/1' \
    "PATH=$WORK/meta-stat-swap:$PATH" \
    "META_RACE_PATH=$WORK/meta-race.md" "META_RACE_TARGET=$WORK/credentials/fake.md"

  cases=$((cases + 1))
  out=$(bash "$SELF" --help 2>&1) || rc=$?
  if [[ ${rc:-0} -eq 0 && $out == *'verify-metadata PATH [--root PATH]'* ]]; then
    printf 'ok-case  %-2d %-28s exit=0\n' "$cases" metadata-usage
  else
    printf 'FAIL-case %-28s usage entry missing or --help failed\n' metadata-usage
    failures=$((failures + 1))
  fi
  printf 'source: S001\nverified-at: 2026-10-20 checked\nrecheck: 90d' \
    >"$WORK/meta-no-final-newline.md"
  metadata_case metadata-no-final-newline "$WORK/meta-no-final-newline.md" 0 \
    'META entry=meta-no-final-newline.md source=present verified_at=dated recheck=scheduled verdict=clean' \
    'METADATA_COMPLETE=1/1'

  cat >"$WORK/meta-fenced-heading.md" <<'EOF'
```markdown
## Fenced body heading
```
source: S001
verified-at: 2026-10-20 checked
recheck: 90d
EOF
  metadata_case metadata-fenced-heading "$WORK/meta-fenced-heading.md" 0 \
    'META entry=meta-fenced-heading.md source=present verified_at=dated recheck=scheduled verdict=clean' \
    'METADATA_COMPLETE=1/1'

  cat >"$WORK/meta-heading-boundary.md" <<'EOF'
source: S001
verified-at: 2026-10-20 checked
recheck: never
recheck: 90d
## Claim
recheck: never
EOF
  metadata_case metadata-heading-boundary "$WORK/meta-heading-boundary.md" 0 \
    'META entry=meta-heading-boundary.md source=present verified_at=dated recheck=scheduled verdict=clean' \
    'METADATA_COMPLETE=1/1'

  metadata_asof_case() { # NAME PATH AS_OF WANT_RC [expected output ...]
    local name=$1 path=$2 asof=$3 want_rc=$4
    shift 4
    local -a want=()
    local tok rc=0 out nverdict msg=''
    want=("$@")
    cases=$((cases + 1))
    out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE \
      CHOUSA_STRICT=0 CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
      bash "$SELF" verify-metadata "$path" --root "$WORK" --as-of "$asof" 2>&1) || rc=$?
    nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true)
    for tok in "${want[@]+"${want[@]}"}"; do
      [[ $out == *"$tok"* ]] || msg+="missing:'$tok' "
    done
    if [[ $want_rc -eq 2 ]]; then
      [[ ${nverdict:-0} -eq 0 ]] || msg+="verdict-lines=$nverdict/0 "
    else
      [[ ${nverdict:-0} -eq 1 ]] || msg+="verdict-lines=$nverdict/1 "
    fi
    if [[ $rc -eq $want_rc && -z $msg ]]; then
      printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" "$name" "$rc"
    else
      printf 'FAIL-case %-28s rc=%d/%d %s\n' "$name" "$rc" "$want_rc" "$msg"
      printf '%s\n' "$out" | sed 's/^/    | /'
      failures=$((failures + 1))
    fi
  }
  metadata_asof_usage_accepts() { # RC EXPECTED OUTPUT
    local rc=$1 expected=$2 out=$3 nverdict grc=0
    nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out") || grc=$?
    # grep exits 1 on zero matches; any other status is a matcher fault, never acceptance.
    ((grc <= 1)) && [[ $rc -eq 2 && $out == *"$expected"* && $nverdict -eq 0 ]]
  }
  metadata_asof_usage_case() { # NAME EXPECTED [CLI args ...]
    local name=$1 expected=$2
    shift 2
    local rc=0 out nverdict
    cases=$((cases + 1))
    out=$(bash "$SELF" "$@" 2>&1) || rc=$?
    nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true)
    if metadata_asof_usage_accepts "$rc" "$expected" "$out"; then
      printf 'ok-case  %-2d %-28s exit=2\n' "$cases" "$name"
    else
      printf 'FAIL-case %-28s rc=%d expected=%s verdicts=%s\n' \
        "$name" "$rc" "$expected" "${nverdict:-0}"
      printf '%s\n' "$out" | sed 's/^/    | /'
      failures=$((failures + 1))
    fi
  }
  metadata_asof_usage_control_case() { # NAME WANT_ACCEPT RC EXPECTED OUTPUT
    local name=$1 want_accept=$2 rc=$3 expected=$4 synthetic_out=$5 accepted=0 helper_out
    local SELF="$WORK/meta-asof/usage-stub.sh"
    cases=$((cases + 1))
    helper_out=$(FAKE_RC="$rc" FAKE_OUTPUT="$synthetic_out" \
      metadata_asof_usage_case "$name" "$expected")
    [[ $helper_out == 'ok-case  '* ]] && accepted=1
    if [[ $accepted -eq $want_accept ]]; then
      printf 'ok-case  %-2d %-28s accepted=%d\n' "$cases" "$name" "$accepted"
    else
      printf 'FAIL-case %-28s accepted=%d want=%d\n' "$name" "$accepted" "$want_accept"
      printf '%s\n' "$helper_out" | sed 's/^/    | /'
      failures=$((failures + 1))
    fi
  }

  mkdir -p "$WORK/meta-asof"
  cat >"$WORK/meta-asof/overdue.md" <<'EOF'
source: S001 fixture
verified-at: 2026-01-02 checked fixture
recheck: 90d

## Body
EOF
  metadata_asof_case metadata-asof-overdue "$WORK/meta-asof/overdue.md" 2026-10-21 1 \
    'META entry=overdue.md source=present verified_at=dated recheck=scheduled due=2026-04-02 freshness=overdue verdict=drift' \
    'FINDING META_RECHECK_OVERDUE severity=warn surface=metadata obs=entry=overdue.md due=2026-04-02 as_of=2026-10-21'
  cat >"$WORK/meta-asof/current.md" <<'EOF'
source: S001 fixture
verified-at: 2026-10-01 checked fixture
recheck: 90d

## Body
EOF
  metadata_asof_case metadata-asof-current "$WORK/meta-asof/current.md" 2026-10-21 0 \
    'META entry=current.md source=present verified_at=dated recheck=scheduled due=2026-12-30 freshness=current verdict=clean'
  cat >"$WORK/meta-asof/date-past.md" <<'EOF'
source: S001 fixture
verified-at: 2026-01-02 checked fixture
recheck: 2026-03-01

## Body
EOF
  metadata_asof_case metadata-asof-date-past "$WORK/meta-asof/date-past.md" 2026-10-21 1 \
    'META entry=date-past.md source=present verified_at=dated recheck=scheduled due=2026-03-01 freshness=overdue verdict=drift' \
    'FINDING META_RECHECK_OVERDUE severity=warn surface=metadata obs=entry=date-past.md due=2026-03-01 as_of=2026-10-21'
  cat >"$WORK/meta-asof/event.md" <<'EOF'
source: S001 fixture
verified-at: 2026-01-02 checked fixture
recheck: on-release

## Body
EOF
  metadata_asof_case metadata-asof-event "$WORK/meta-asof/event.md" 2026-10-21 0 \
    'META entry=event.md source=present verified_at=dated recheck=scheduled due=on-release freshness=event verdict=clean'
  cat >"$WORK/meta-asof/unknown.md" <<'EOF'
source: S001 fixture
verified-at: 2026-01-02 checked fixture
recheck: bash tools/x.sh

## Body
EOF
  metadata_asof_case metadata-asof-unknown "$WORK/meta-asof/unknown.md" 2026-10-21 0 \
    'META entry=unknown.md source=present verified_at=dated recheck=unscheduled due=unknown freshness=unknown verdict=clean'
  cat >"$WORK/meta-asof/boundary.md" <<'EOF'
source: S001 fixture
verified-at: 2026-07-23 checked fixture
recheck: 90d

## Body
EOF
  metadata_asof_case metadata-asof-boundary "$WORK/meta-asof/boundary.md" 2026-10-21 0 \
    'META entry=boundary.md source=present verified_at=dated recheck=scheduled due=2026-10-21 freshness=current verdict=clean'

  metadata_asof_usage_case metadata-asof-invalid '--as-of must be a valid YYYY-MM-DD date' \
    verify-metadata "$WORK/meta-asof/current.md" --root "$WORK" --as-of 2026-02-30
  metadata_asof_usage_case metadata-asof-missing '--as-of needs YYYY-MM-DD' \
    verify-metadata "$WORK/meta-asof/current.md" --root "$WORK" --as-of
  metadata_asof_usage_case metadata-asof-wrong-mode '--as-of is only valid with verify-metadata' \
    verify "$WORK/all-pass.md" --as-of 2026-10-21

  cat >"$WORK/meta-asof/leap-2028.md" <<'EOF'
source: S001 fixture
verified-at: 2028-02-28 checked fixture
recheck: 0001d

## Body
EOF
  metadata_asof_case metadata-asof-leap-2028 "$WORK/meta-asof/leap-2028.md" 2028-02-29 0 \
    'META entry=leap-2028.md source=present verified_at=dated recheck=scheduled due=2028-02-29 freshness=current verdict=clean'
  cat >"$WORK/meta-asof/leap-2027.md" <<'EOF'
source: S001 fixture
verified-at: 2027-02-28 checked fixture
recheck: 1d

## Body
EOF
  metadata_asof_case metadata-asof-leap-2027 "$WORK/meta-asof/leap-2027.md" 2027-03-01 0 \
    'META entry=leap-2027.md source=present verified_at=dated recheck=scheduled due=2027-03-01 freshness=current verdict=clean'
  cat >"$WORK/meta-asof/large-cadence.md" <<'EOF'
source: S001 fixture
verified-at: 2026-01-02 checked fixture
recheck: 999999999999999999999999999999999999d

## Body
EOF
  metadata_asof_case metadata-asof-large-cadence "$WORK/meta-asof/large-cadence.md" 2026-10-21 0 \
    'META entry=large-cadence.md source=present verified_at=dated recheck=scheduled due=unknown freshness=unknown verdict=clean'
  cat >"$WORK/meta-asof/date-overflow.md" <<'EOF'
source: S001 fixture
verified-at: 9999-12-31 checked fixture
recheck: 1d

## Body
EOF
  metadata_asof_case metadata-asof-date-overflow "$WORK/meta-asof/date-overflow.md" 9999-12-31 0 \
    'META entry=date-overflow.md source=present verified_at=dated recheck=scheduled due=unknown freshness=unknown verdict=clean'
  cat >"$WORK/meta-asof/invalid-verified-date.md" <<'EOF'
source: S001 fixture
verified-at: 2026-02-30 checked fixture
recheck: 1d

## Body
EOF
  metadata_asof_case metadata-asof-invalid-verified-date "$WORK/meta-asof/invalid-verified-date.md" 2026-10-21 0 \
    'META entry=invalid-verified-date.md source=present verified_at=dated recheck=scheduled due=unknown freshness=unknown verdict=clean'
  metadata_asof_case metadata-asof-refused "$WORK/meta-nul.md" 2026-10-21 1 \
    'META entry=meta-nul.md source=refused verified_at=refused recheck=refused due=refused freshness=refused verdict=drift'

  metadata_registry_case() { # NAME ENTRY REGISTRY WANT_RC [expected output ...]
    local name=$1 path=$2 registry=$3 want_rc=$4
    shift 4
    local rc=0 out nverdict msg='' tok
    local -a wants=("$@")
    cases=$((cases + 1))
    out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE \
      CHOUSA_STRICT=0 CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
      bash "$SELF" verify-metadata "$path" --root "$WORK" --registry "$registry" \
      2>&1) || rc=$?
    nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true)
    for tok in "${wants[@]}"; do
      [[ $out == *"$tok"* ]] || msg+="missing:'$tok' "
    done
    if [[ $want_rc -eq 2 ]]; then
      [[ ${nverdict:-0} -eq 0 ]] || msg+="verdict-lines=$nverdict/0 "
    else
      [[ ${nverdict:-0} -eq 1 ]] || msg+="verdict-lines=$nverdict/1 "
    fi
    if [[ $rc -eq $want_rc && -z $msg ]]; then
      printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" "$name" "$rc"
    else
      printf 'FAIL-case %-28s rc=%d/%d %s\n' "$name" "$rc" "$want_rc" "$msg"
      printf '%s\n' "$out" | sed 's/^/    | /'
      failures=$((failures + 1))
    fi
  }

  mkdir -p "$WORK/corpus/knowledge"
  cat >"$WORK/meta-registry.md" <<'EOF'
| id | status | used-by |
|---|---|---|
| S001 | mined | corpus/knowledge/meta-reg-bare.md |
| S002 | queued | corpus/knowledge/meta-reg-queued.md |
| S003 | mined | meta-reg-usedby.md |
EOF
  printf 'source: S999\nverified-at: 2026-10-20 checked\nrecheck: 90d\n' \
    >"$WORK/corpus/knowledge/meta-reg-missing.md"
  metadata_registry_case metadata-registry-missing-row \
    "$WORK/corpus/knowledge/meta-reg-missing.md" "$WORK/meta-registry.md" 1 \
    'FINDING META_SOURCE_ROW_MISSING severity=warn surface=metadata obs=entry=meta-reg-missing.md source_id=S999'

  printf 'source: S002\nverified-at: 2026-10-20 checked\nrecheck: 90d\n' \
    >"$WORK/corpus/knowledge/meta-reg-queued.md"
  metadata_registry_case metadata-registry-not-mined \
    "$WORK/corpus/knowledge/meta-reg-queued.md" "$WORK/meta-registry.md" 1 \
    'FINDING META_SOURCE_NOT_MINED severity=warn surface=metadata obs=entry=meta-reg-queued.md source_id=S002'

  printf 'source: S003\nverified-at: 2026-10-20 checked\nrecheck: 90d\n' \
    >"$WORK/corpus/knowledge/meta-reg-usedby.md"
  metadata_registry_case metadata-registry-used-by-path \
    "$WORK/corpus/knowledge/meta-reg-usedby.md" "$WORK/meta-registry.md" 1 \
    'FINDING META_SOURCE_USEDBY_MISSING severity=warn surface=metadata obs=entry=meta-reg-usedby.md source_id=S003'

  printf 'source: S001\nverified-at: 2026-10-20\nrecheck: 90d\n' \
    >"$WORK/corpus/knowledge/meta-reg-bare.md"
  metadata_registry_case metadata-registry-verified-at-bare \
    "$WORK/corpus/knowledge/meta-reg-bare.md" "$WORK/meta-registry.md" 1 \
    'FINDING META_VERIFIED_AT_BARE severity=warn surface=metadata obs=entry=meta-reg-bare.md'

  printf 'source: xS001 S001a\nverified-at: 2026-10-20 checked\nrecheck: 90d\n' \
    >"$WORK/corpus/knowledge/meta-reg-noid.md"
  metadata_registry_case metadata-registry-no-token-id \
    "$WORK/corpus/knowledge/meta-reg-noid.md" "$WORK/meta-registry.md" 0 \
    'FINDING META_SOURCE_NO_ROW_ID severity=info surface=metadata obs=entry=meta-reg-noid.md'

  cat >"$WORK/meta-registry-positive.md" <<'EOF'
| used-by | source | status | id |
|---|---|---|---|
| ./corpus/knowledge/meta-reg-positive.md | fixture | mined | S0001 |
EOF
  cat >"$WORK/corpus/knowledge/meta-reg-positive.md" <<'EOF'
source: citation continuation
  S0001
verified-at: 2026-10-20
  checked the claim
recheck: 90d
EOF
  metadata_registry_case metadata-registry-positive-continuations \
    "$WORK/corpus/knowledge/meta-reg-positive.md" "$WORK/meta-registry-positive.md" 0 \
    'META entry=meta-reg-positive.md source=present verified_at=dated recheck=scheduled verdict=clean' \
    'findings=0 drift=0'

  cat >"$WORK/meta-registry-duplicate.md" <<'EOF'
| id | status | used-by |
|---|---|---|
| S0999 | queued | corpus/knowledge/meta-reg-duplicate.md |
| S0999 | mined | corpus/knowledge/meta-reg-duplicate.md |
EOF
  printf 'source: S0999\nverified-at: 2026-10-20 checked\nrecheck: 90d\n' \
    >"$WORK/corpus/knowledge/meta-reg-duplicate.md"
  metadata_registry_case metadata-registry-duplicate-first-row \
    "$WORK/corpus/knowledge/meta-reg-duplicate.md" "$WORK/meta-registry-duplicate.md" 1 \
    'FINDING META_SOURCE_NOT_MINED severity=warn surface=metadata obs=entry=meta-reg-duplicate.md source_id=S0999'

  printf '| id | status | used-by |\n|---|---|---|\n\x00' \
    >"$WORK/meta-registry-nul.md"
  metadata_registry_case metadata-registry-refused-nul \
    "$WORK/corpus/knowledge/meta-reg-missing.md" "$WORK/meta-registry-nul.md" 2 \
    'metadata registry refused: nul'
  cat >"$WORK/meta-asof/usage-stub.sh" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$FAKE_OUTPUT"
exit "$FAKE_RC"
EOF
  metadata_asof_usage_control_case metadata-asof-usage-help-control 1 2 \
    'synthetic usage diagnostic' \
    $'synthetic usage diagnostic\nusage: fixture\nVerdict: RESEARCH_GATE: CLEAN|DRIFT'
  metadata_asof_usage_control_case metadata-asof-usage-clean-control 0 2 \
    'synthetic usage diagnostic' \
    $'RESEARCH_GATE: CLEAN\nsynthetic usage diagnostic\nVerdict: RESEARCH_GATE: CLEAN|DRIFT'
  metadata_asof_usage_control_case metadata-asof-usage-drift-control 0 2 \
    'synthetic usage diagnostic' \
    $'RESEARCH_GATE: DRIFT\nsynthetic usage diagnostic\nVerdict: RESEARCH_GATE: CLEAN|DRIFT'
  metadata_asof_usage_control_case metadata-asof-usage-exit-control 0 1 \
    'synthetic usage diagnostic' \
    $'synthetic usage diagnostic\nusage: fixture\nVerdict: RESEARCH_GATE: CLEAN|DRIFT'
  metadata_asof_usage_control_case metadata-asof-usage-diagnostic-control 0 2 \
    'synthetic usage diagnostic' \
    $'usage: fixture\nVerdict: RESEARCH_GATE: CLEAN|DRIFT'

  # Find an installed locale whose inherited regex admits these non-ASCII digits.
  unicode_locale=''
  while IFS= read -r candidate_locale; do
    if LC_ALL="$candidate_locale" bash -c \
      '[[ "２０２６-10-21" =~ ^([0-9]{4})-([0-9]{2})-([0-9]{2})$ ]]' \
      >/dev/null 2>&1; then
      unicode_locale=$candidate_locale
      break
    fi
  done < <(locale -a 2>/dev/null)
  if [[ -n $unicode_locale ]]; then
    printf 'metadata-asof-unicode-date-locale=%s\n' "$unicode_locale"
    LC_ALL="$unicode_locale" metadata_asof_usage_case \
      metadata-asof-unicode-date-locale \
      '--as-of must be a valid YYYY-MM-DD date' \
      verify-metadata "$WORK/meta-asof/current.md" --root "$WORK" --as-of '２０２６-10-21'
  else
    cases=$((cases + 1)); SKIPPED=$((SKIPPED + 1))
    printf 'skip-case %-2d %-28s reason=no available locale admits Unicode digits\n' \
      "$cases" metadata-asof-unicode-date-locale
  fi
  LC_ALL=C metadata_asof_usage_case metadata-asof-unicode-date-C \
    '--as-of must be a valid YYYY-MM-DD date' \
    verify-metadata "$WORK/meta-asof/current.md" --root "$WORK" --as-of '２０２６-10-21'

  # These synthetic long cadences exercise a full 128 KiB prefix without recursive trimming.
  printf -v zero_prefix '%*s' 131072 ''
  zero_prefix=${zero_prefix// /0}
  printf 'source: S001 fixture\nverified-at: 2026-01-02 checked fixture\nrecheck: %s90d\n\n## Body\n' \
    "$zero_prefix" >"$WORK/meta-asof/zero-prefix-90.md"
  metadata_asof_case metadata-asof-128k-zero-prefix "$WORK/meta-asof/zero-prefix-90.md" 2026-10-21 1 \
    'META entry=zero-prefix-90.md source=present verified_at=dated recheck=scheduled due=2026-04-02 freshness=overdue verdict=drift' \
    'FINDING META_RECHECK_OVERDUE severity=warn surface=metadata obs=entry=zero-prefix-90.md due=2026-04-02 as_of=2026-10-21'

  plain_rc=0
  plain_out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE \
    CHOUSA_STRICT=0 CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
    bash "$SELF" verify-metadata "$WORK/meta-asof/zero-prefix-90.md" --root "$WORK" 2>&1) \
    || plain_rc=$?
  plain_fields=$(grep -E -c '^META entry=.*( due=| freshness=)' <<<"$plain_out" || true)
  plain_verdicts=$(grep -c '^RESEARCH_GATE: ' <<<"$plain_out" || true)
  cases=$((cases + 1))
  if [[ $plain_rc -eq 0 && $plain_fields -eq 0 && $plain_verdicts -eq 1 \
        && $plain_out == *'META entry=zero-prefix-90.md source=present verified_at=dated recheck=scheduled verdict=clean'* \
        && $plain_out == *'METADATA_COMPLETE=1/1'* \
        && $plain_out == *'RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)'* ]]; then
    printf 'ok-case  %-2d %-28s exit=0\n' "$cases" metadata-asof-128k-zero-prefix-plain
  else
    printf 'FAIL-case %-28s rc=%d expected=0 date-fields=%s/0 verdict-lines=%s/1\n' \
      metadata-asof-128k-zero-prefix-plain "$plain_rc" "$plain_fields" "$plain_verdicts"
    printf '%s\n' "$plain_out" | sed 's/^/    | /'
    failures=$((failures + 1))
  fi
  metadata_registry_finding_count_case() { # NAME ENTRY REGISTRY WANT_RC FINDING COUNT [OTHER_FINDING OTHER_COUNT]
    local name=$1 path=$2 registry=$3 want_rc=$4 finding=$5 want_count=$6
    local other_finding=${7:-} other_count=${8:-}
    local rc=0 out nverdict actual_count actual_other msg=''
    cases=$((cases + 1))
    out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE \
      CHOUSA_STRICT=0 CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
      bash "$SELF" verify-metadata "$path" --root "$WORK" --registry "$registry" \
      2>&1) || rc=$?
    nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true)
    actual_count=$(grep -Fxc -- "$finding" <<<"$out" || true)
    [[ $actual_count -eq $want_count ]] \
      || msg+="finding-lines=$actual_count/$want_count "
    if [[ -n $other_finding ]]; then
      actual_other=$(grep -Fxc -- "$other_finding" <<<"$out" || true)
      [[ $actual_other -eq $other_count ]] \
        || msg+="other-finding-lines=$actual_other/$other_count "
    fi
    if [[ $want_rc -eq 2 ]]; then
      [[ ${nverdict:-0} -eq 0 ]] || msg+="verdict-lines=$nverdict/0 "
    else
      [[ ${nverdict:-0} -eq 1 ]] || msg+="verdict-lines=$nverdict/1 "
    fi
    if [[ $rc -eq $want_rc && -z $msg ]]; then
      printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" "$name" "$rc"
    else
      printf 'FAIL-case %-28s rc=%d/%d %s\n' "$name" "$rc" "$want_rc" "$msg"
      printf '%s\n' "$out" | sed 's/^/    | /'
      failures=$((failures + 1))
    fi
  }

  # C3 regressions use only files and links created under this selftest's
  # temporary WORK directory.
  cat >"$WORK/meta-registry-header-break-blank.md" <<'EOF'
| id | status | used-by |

| S999 | mined | corpus/knowledge/meta-reg-missing.md |
|---|---|---|
| S999 | mined | corpus/knowledge/meta-reg-missing.md |
EOF
  metadata_registry_case metadata-registry-header-break-blank \
    "$WORK/corpus/knowledge/meta-reg-missing.md" "$WORK/meta-registry-header-break-blank.md" 2 \
    'metadata registry has no table with id, status, and used-by columns'

  cat >"$WORK/meta-registry-header-break-prose.md" <<'EOF'
| id | status | used-by |
Registry note between tables.
| S999 | mined | corpus/knowledge/meta-reg-missing.md |
|---|---|---|
| S999 | mined | corpus/knowledge/meta-reg-missing.md |
EOF
  metadata_registry_case metadata-registry-header-break-prose \
    "$WORK/corpus/knowledge/meta-reg-missing.md" "$WORK/meta-registry-header-break-prose.md" 2 \
    'metadata registry has no table with id, status, and used-by columns'

  cat >"$WORK/meta-registry-width-short.md" <<'EOF'
| id | status | used-by |
|---|---|
| S999 | mined | corpus/knowledge/meta-reg-missing.md |
EOF
  metadata_registry_case metadata-registry-width-short \
    "$WORK/corpus/knowledge/meta-reg-missing.md" "$WORK/meta-registry-width-short.md" 2 \
    'metadata registry has no table with id, status, and used-by columns'

  cat >"$WORK/meta-registry-width-long.md" <<'EOF'
| id | status | used-by |
|---|---|---|---|
| S999 | mined | corpus/knowledge/meta-reg-missing.md |
EOF
  metadata_registry_case metadata-registry-width-long \
    "$WORK/corpus/knowledge/meta-reg-missing.md" "$WORK/meta-registry-width-long.md" 2 \
    'metadata registry has no table with id, status, and used-by columns'

  cat >"$WORK/meta-registry-column-reorder.md" <<'EOF'
Registry prose before the table.
| used-by | id | status |
|---|---|---|
| corpus/knowledge/meta-reg-column-reorder.md | S001 | mined |
EOF
  cat >"$WORK/corpus/knowledge/meta-reg-column-reorder.md" <<'EOF'
source: S001
verified-at: 2026-10-20 checked
recheck: 90d
EOF
  metadata_registry_case metadata-registry-column-reorder \
    "$WORK/corpus/knowledge/meta-reg-column-reorder.md" "$WORK/meta-registry-column-reorder.md" 0 \
    'META entry=meta-reg-column-reorder.md source=present verified_at=dated recheck=scheduled verdict=clean' \
    'findings=0 drift=0'

  printf 'source: xS999 S999\nverified-at: 2026-10-20 checked\nrecheck: 90d\n' \
    >"$WORK/corpus/knowledge/meta-reg-glued-before-standalone.md"
  metadata_registry_finding_count_case metadata-registry-glued-before-standalone \
    "$WORK/corpus/knowledge/meta-reg-glued-before-standalone.md" "$WORK/meta-registry.md" 1 \
    'FINDING META_SOURCE_ROW_MISSING severity=warn surface=metadata obs=entry=meta-reg-glued-before-standalone.md source_id=S999 registry row missing' 1

  printf 'source: S002,S002\nverified-at: 2026-10-20 checked\nrecheck: 90d\n' \
    >"$WORK/corpus/knowledge/meta-reg-duplicate-occurrences.md"
  metadata_registry_finding_count_case metadata-registry-duplicate-occurrences \
    "$WORK/corpus/knowledge/meta-reg-duplicate-occurrences.md" "$WORK/meta-registry.md" 1 \
    'FINDING META_SOURCE_NOT_MINED severity=warn surface=metadata obs=entry=meta-reg-duplicate-occurrences.md source_id=S002 registry row is not mined' 2

  printf 'source: xS002 S002x _S002 S002_\nverified-at: 2026-10-20 checked\nrecheck: 90d\n' \
    >"$WORK/corpus/knowledge/meta-reg-nonstandalone.md"
  metadata_registry_finding_count_case metadata-registry-nonstandalone-ASCII \
    "$WORK/corpus/knowledge/meta-reg-nonstandalone.md" "$WORK/meta-registry.md" 0 \
    'FINDING META_SOURCE_NO_ROW_ID severity=info surface=metadata obs=entry=meta-reg-nonstandalone.md source has no S-id' 1 \
    'FINDING META_SOURCE_NOT_MINED severity=warn surface=metadata obs=entry=meta-reg-nonstandalone.md source_id=S002 registry row is not mined' 0

  mkdir -p "$WORK/registry:synthetic/credentials"
  cat >"$WORK/registry:synthetic/credentials/source-table.md" <<'EOF'
| id | status | used-by |
|---|---|---|
| S001 | mined | corpus/knowledge/meta-reg-bare.md |
EOF
  metadata_registry_case metadata-registry-colon-denylist \
    "$WORK/corpus/knowledge/meta-reg-bare.md" "$WORK/registry:synthetic/credentials/source-table.md" 2 \
    'metadata registry refused: denylist'

  mkdir -p "$WORK/entry:synthetic/credentials"
  cat >"$WORK/entry:synthetic/credentials/entry.md" <<'EOF'
source: S001
verified-at: 2026-10-20 checked
recheck: 90d
EOF
  metadata_case metadata-entry-colon-denylist \
    "$WORK/entry:synthetic/credentials/entry.md" 1 \
    'FINDING META_ENTRY_REFUSED severity=crit surface=metadata obs=entry=entry.md reason=denylist unparsed' \
    'METADATA_COMPLETE=0/1'

  printf 'source: S001\nverified-at: 2026-10-20 checked\nrecheck: 90d\n' \
    >"$WORK/metadata.env:1.md"
  metadata_case metadata-colon-anchor-denylist-compat "$WORK/metadata.env:1.md" 1 \
    'FINDING META_ENTRY_REFUSED severity=crit surface=metadata obs=entry=metadata.env:1.md reason=denylist unparsed' \
    'METADATA_COMPLETE=0/1'

  printf 'source: S001\nverified-at: 2026-10-20 checked\nrecheck: 90d\n' \
    >"$WORK/metadata:synthetic.md"
  metadata_case metadata-ordinary-colon-allowed "$WORK/metadata:synthetic.md" 0 \
    'META entry=metadata:synthetic.md source=present verified_at=dated recheck=scheduled verdict=clean' \
    'findings=0 drift=0'

  mkdir -p "$WORK/claim:synthetic/credentials"
  printf 'Synthetic content not opened by the denylist control.\n' \
    >"$WORK/claim:synthetic/credentials/source.md"
  ln -s "$WORK/claim:synthetic/credentials/source.md" \
    "$WORK/claim:synthetic/alias.md"
  printf '{"id":"FS1","source":"claim:synthetic/alias.md","span":"Synthetic content","expect":"supported"}\n' \
    >"$WORK/claims-registry-colon-deny.jsonl"
  tclaims claims-registry-colon-deny 1 \
    'FINDING CLAIM_SOURCE_SESSION severity=crit surface=claims' \
    'CLAIM id=FS1 expected=supported observed=refused' \
    'VERDICT_BEARING_CLAIMS=0/1'

  printf 'source: S001 fixture\nverified-at: 2026-01-02 checked fixture\nrecheck: %s0d\n\n## Body\n' \
    "$zero_prefix" >"$WORK/meta-asof/zero-cadence.md"
  metadata_asof_case metadata-asof-all-zero-cadence "$WORK/meta-asof/zero-cadence.md" 2026-01-02 0 \
    'META entry=zero-cadence.md source=present verified_at=dated recheck=scheduled due=2026-01-02 freshness=current verdict=clean'

  # r27 falsify repairs: GFM cell width with escaped pipes, mixed outer pipes,
  # no header across a blank line, and a usage-record matcher fault.
  printf 'source: S001\nverified-at: 2026-10-20 checked\nrecheck: 90d\n' \
    >"$WORK/corpus/knowledge/meta-reg-gfm.md"
  printf '| id | status | used-by | note \\| alt |\n|---|---|---|---|\n| S001 | mined | corpus/knowledge/meta-reg-gfm.md | x |\n' \
    >"$WORK/meta-registry-escaped.md"
  metadata_registry_case metadata-registry-escaped-pipe-width \
    "$WORK/corpus/knowledge/meta-reg-gfm.md" "$WORK/meta-registry-escaped.md" 0 \
    'findings=0 drift=0'
  printf '| id | status | used-by | note \\| alt |\n|---|---|---|---|---|\n| S001 | mined | corpus/knowledge/meta-reg-gfm.md | x |\n' \
    >"$WORK/meta-registry-escaped-wide.md"
  metadata_registry_case metadata-registry-escaped-pipe-overwide \
    "$WORK/corpus/knowledge/meta-reg-gfm.md" "$WORK/meta-registry-escaped-wide.md" 2 \
    'metadata registry has no table'
  printf '| id | status | used-by |\n---|---|---\n| S001 | mined | corpus/knowledge/meta-reg-gfm.md |\n' \
    >"$WORK/meta-registry-mixed-pipes.md"
  metadata_registry_case metadata-registry-mixed-outer-pipes \
    "$WORK/corpus/knowledge/meta-reg-gfm.md" "$WORK/meta-registry-mixed-pipes.md" 0 \
    'findings=0 drift=0'
  printf '| id | status | used-by |\n\n|---|---|---|\n| S001 | mined | corpus/knowledge/meta-reg-gfm.md |\n' \
    >"$WORK/meta-registry-blank-delimiter.md"
  metadata_registry_case metadata-registry-delimiter-after-blank \
    "$WORK/corpus/knowledge/meta-reg-gfm.md" "$WORK/meta-registry-blank-delimiter.md" 2 \
    'metadata registry has no table'
  cases=$((cases + 1))
  if ( grep() { return 2; }; metadata_asof_usage_accepts 2 'expected diagnostic' \
      $'expected diagnostic\nusage: fixture' ); then
    printf 'FAIL-case %-28s matcher fault accepted\n' metadata-asof-usage-matcher-fault
    failures=$((failures + 1))
  else
    printf 'ok-case  %-2d %-28s accepted=0\n' "$cases" metadata-asof-usage-matcher-fault
  fi

  # ---- round-31 C1 selftest cases (after the r27 matcher-fault case): ----
  # optional "line" field (claim location binding). The fixture source has
  # delimited occurrences of named spans on specific lines, a glued copy and a
  # prefix on other lines, and a multi-line span; every contract rule gets a
  # pass and a fail case.
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
  # bound: single line, later delimited occurrence (enumeration), multi-line
  # ranges, and span absent with "line" present (unsupported, unchanged).
  cat >"$WORK/c1-pass-bound.jsonl" <<'EOF'
{"id":"L1","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":"1"}
{"id":"B1","source":"lib/span.md","span":"iota kappa lambda mu","expect":"supported","line":"11"}
{"id":"ML1","source":"lib/span.md","span":"gamma delta\nepsilon zeta","expect":"supported","line":"7-8"}
{"id":"ML2","source":"lib/span.md","span":"zeta eta theta\niota","expect":"supported","line":"2-3"}
{"id":"U1","source":"lib/span.md","span":"never present anywhere","expect":"unsupported","line":"3"}
EOF
  tclaims c1-pass-bound 0 \
    'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=5/5' \
    'CLAIM id=L1 expected=supported observed=supported source=lib/span.md at=line:1 verdict=match' \
    'CLAIM id=B1 expected=supported observed=supported source=lib/span.md at=line:11 verdict=match' \
    'CLAIM id=ML1 expected=supported observed=supported source=lib/span.md at=lines:7-8 verdict=match' \
    'CLAIM id=ML2 expected=supported observed=supported source=lib/span.md at=lines:2-3 verdict=match' \
    'CLAIM id=U1 expected=unsupported observed=unsupported source=lib/span.md at=- verdict=match'
  # mislocated: wrong line, glued copy on named line, prefix on named line,
  # wrong multi-line range, past EOF, and two real occurrences with a third
  # line named.
  cat >"$WORK/c1-fail-mislocated.jsonl" <<'EOF'
{"id":"M1","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":"4"}
{"id":"G1","source":"lib/span.md","span":"iota kappa lambda mu","expect":"supported","line":"10"}
{"id":"P1","source":"lib/span.md","span":"phi chi psi omega","expect":"supported","line":"9"}
{"id":"MR1","source":"lib/span.md","span":"gamma delta\nepsilon zeta","expect":"supported","line":"7-9"}
{"id":"E1","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":"99"}
{"id":"T1","source":"lib/span.md","span":"iota kappa lambda mu","expect":"supported","line":"5"}
EOF
  tclaims c1-fail-mislocated 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims' \
    'obs=id=E1 line=99-99 first_delimited_occurrence=line:1' \
    'obs=id=G1 line=10-10 first_delimited_occurrence=line:3' \
    'obs=id=MR1 line=7-9 first_delimited_occurrence=lines:1-2' \
    'obs=id=T1 line=5-5 first_delimited_occurrence=line:3' \
    'observed=mislocated' 'VERDICT_BEARING_CLAIMS=0/6' \
    'claims=6 supported=0 contradicted=0 unsupported=0 mismatched=6 unproven=0 refused=0 invalid=0 findings=6 drift=6'
  # invalid present "line" values: leading zero, zero, M<=N, spaces, dangling
  # dash, non-decimal, en-dash, empty string, and a non-string value.
  cat >"$WORK/c1-fail-invalid-line.jsonl" <<'EOF'
{"id":"I0","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":"0"}
{"id":"I07","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":"07"}
{"id":"I53","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":"5-3"}
{"id":"I44","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":"4-4"}
{"id":"Is","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":" 4"}
{"id":"It","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":"4 "}
{"id":"Id","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":"4-"}
{"id":"Im","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":"-4"}
{"id":"Ix","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":"x7"}
{"id":"Ids","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":"1.5"}
{"id":"Ie","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":"4–5"}
{"id":"Ie2","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":""}
{"id":"In","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":5}
EOF
  tclaims c1-fail-invalid-line 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_RECORD_INVALID' \
    'line range M<=N' 'line value malformed' 'line not a JSON string' \
    'observed=invalid' 'VERDICT_BEARING_CLAIMS=0/13' \
    'claims=13 supported=0 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=13 findings=13 drift=13'
  # "line" absent: behaviour unchanged.
  cat >"$WORK/c1-pass-no-line.jsonl" <<'EOF'
{"id":"N1","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported"}
{"id":"N2","source":"lib/span.md","span":"never present anywhere","expect":"unsupported"}
EOF
  tclaims c1-pass-no-line 0 \
    'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=2/2' \
    'CLAIM id=N1 expected=supported observed=supported source=lib/span.md at=line:1 verdict=match' \
    'CLAIM id=N2 expected=unsupported observed=unsupported source=lib/span.md at=- verdict=match'
  # ---- r31 C2: revision binding via optional "sha256" (cases 220-228) ----
  # A present "sha256" pins the exact bytes of the source file: malformed
  # present values invalidate the record (CLAIM_RECORD_INVALID); a mismatch is
  # observed=stale with CLAIM_SOURCE_REVISION_MISMATCH before and regardless of
  # the span check; absent or equal leaves behavior unchanged. Boundary
  # refusals keep precedence (refused sources are never hashed). CRLF sources
  # hash as their exact bytes; the span check behaves as today.
  printf 'sha source line one\n' >"$WORK/claimsrc/sha-src.txt"
  SHA_GOOD=$(sha256sum -- "$WORK/claimsrc/sha-src.txt" | cut -d' ' -f1)
  printf 'sha source line one' >"$WORK/claimsrc/sha-src-nonl.txt"
  printf 'sha source line two\n' >"$WORK/claimsrc/sha-src-tampered.txt"
  SHA_TAMPERED=$(sha256sum -- "$WORK/claimsrc/sha-src-tampered.txt" | cut -d' ' -f1)
  printf 'sha source line one\r\n' >"$WORK/claimsrc/sha-src-crlf.txt"
  SHA_CRLF=$(sha256sum -- "$WORK/claimsrc/sha-src-crlf.txt" | cut -d' ' -f1)

  printf '{"id":"S0","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported"}\n' \
    >"$WORK/claims-sha-absent.jsonl"
  printf '{"id":"S1","source":"claimsrc/sha-src.txt","span":"sha source phantom","expect":"supported"}\n' \
    >"$WORK/claims-sha-absent-fail.jsonl"
  printf '{"id":"M1","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported","sha256":"%s"}\n' "$SHA_GOOD" \
    >"$WORK/claims-sha-match.jsonl"
  printf '{"id":"M2","source":"claimsrc/sha-src.txt","span":"sha source phantom","expect":"supported","sha256":"%s"}\n' "$SHA_GOOD" \
    >"$WORK/claims-sha-match-spanfail.jsonl"
  printf '{"id":"T1","source":"claimsrc/sha-src-tampered.txt","span":"sha source line two","expect":"supported","sha256":"%s"}\n' "$SHA_GOOD" \
    >"$WORK/claims-sha-stale.jsonl"
  printf '{"id":"T2","source":"claimsrc/sha-src-nonl.txt","span":"sha source phantom","expect":"supported","sha256":"%s"}\n' "$SHA_GOOD" \
    >>"$WORK/claims-sha-stale.jsonl"
  printf '{"id":"T3","source":"claimsrc/sha-src-crlf.txt","span":"sha source line one","expect":"supported","sha256":"%s"}\n' "$SHA_GOOD" \
    >>"$WORK/claims-sha-stale.jsonl"
  cat >"$WORK/claims-sha-invalid.jsonl" <<EOF
{"id":"I1","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported","sha256":"A$(printf 'a%.0s' {1..63})"}
{"id":"I2","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported","sha256":"$(printf 'a%.0s' {1..63})"}
{"id":"I3","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported","sha256":"$(printf 'a%.0s' {1..65})"}
{"id":"I4","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported","sha256":"sha256:$(printf 'a%.0s' {1..64})"}
{"id":"I5","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported","sha256":"$(printf 'g%.0s' {1..64})"}
{"id":"I6","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported","sha256":" $(printf 'a%.0s' {1..63})"}
{"id":"I7","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported","sha256":""}
EOF
  printf '{"id":"V1","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported","sha256":"%s"}\n' "$SHA_GOOD" \
    >"$WORK/claims-sha-validity.jsonl"
  printf '{"id":"V2","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported","sha256":"G$(printf 'a%.0s' {1..63})"}\n' \
    >>"$WORK/claims-sha-validity.jsonl"
  printf '{"id":"R1","source":"https://example.invalid/research.md","span":"remote text","expect":"supported","sha256":"%s"}\n' "$SHA_GOOD" \
    >"$WORK/claims-sha-refused.jsonl"
  printf '{"id":"C1","source":"claimsrc/sha-src-crlf.txt","span":"sha source line one","expect":"supported","sha256":"%s"}\n' "$SHA_CRLF" \
    >"$WORK/claims-sha-crlf.jsonl"

  tclaims claims-sha-absent 0 'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=1/1' \
    'CLAIM id=S0 expected=supported observed=supported source=claimsrc/sha-src.txt at=line:1 verdict=match'
  tclaims claims-sha-absent-fail 1 'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_SPAN_NOT_FOUND' \
    'observed=unsupported' 'VERDICT_BEARING_CLAIMS=0/1'
  tclaims claims-sha-match 0 'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=1/1' \
    'CLAIM id=M1 expected=supported observed=supported source=claimsrc/sha-src.txt at=line:1 verdict=match'
  tclaims claims-sha-match-spanfail 1 'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_SPAN_NOT_FOUND' \
    'observed=unsupported' 'VERDICT_BEARING_CLAIMS=0/1'
  tclaims claims-sha-stale 1 'RESEARCH_GATE: DRIFT' \
    'FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=warn surface=claims' \
    'observed=stale' 'VERDICT_BEARING_CLAIMS=0/3' 'mismatched=3' \
    "pin=${SHA_GOOD:0:12} actual=${SHA_TAMPERED:0:12}"
  tclaims claims-sha-invalid 1 'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_RECORD_INVALID' \
    'observed=invalid' 'VERDICT_BEARING_CLAIMS=0/7' 'invalid=7'
  tclaims claims-sha-validity 1 'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_RECORD_INVALID' \
    'CLAIM id=V1 expected=supported observed=supported source=claimsrc/sha-src.txt at=line:1 verdict=match' \
    'CLAIM id=V2 expected=supported observed=invalid source=claimsrc/sha-src.txt at=- verdict=invalid' \
    'VERDICT_BEARING_CLAIMS=1/2'
  tclaims claims-sha-refused 1 'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_SOURCE_EXTERNAL severity=crit' \
    'observed=refused' 'VERDICT_BEARING_CLAIMS=0/1'
  tclaims claims-sha-crlf 0 'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=1/1' \
    'CLAIM id=C1 expected=supported observed=supported source=claimsrc/sha-src-crlf.txt at=line:1 verdict=match'

  # ---- exempt-hop audit (r32 C2) -------------------------------------------
  # A hop whose status says it could not be followed (unresolved,
  # blocked-no-fetch, labelled-dead) is audited with the resolved arm's own
  # citation/source/boundary/anchor probe, silently. A citation that would
  # verify there is a false unavailability mark: observed=resolvable, exactly
  # one CHAIN_EXEMPT_RESOLVABLE warning naming the hop, drift. Every other
  # such hop — and every rejected/not-applicable hop, which records a judgment
  # — stays observed=exempt with no finding. tchain_audit asserts what the
  # substring runner cannot: the resolvable/exempt/finding totals and the
  # absence of any resolved-arm finding from the silent arm.
  printf 'glued case: qalpha row present here\nplain intro line\nomega final line and more\n' \
    >"$WORK/lib/chain_near.md"
  tchain_audit() { # NAME WANT_RC N_RESOLVABLE N_EXEMPT [want substring …]
    local name=$1 want_rc=$2 want_res=$3 want_ex=$4
    shift 4
    local -a want=("$@")
    local rc=0 out tok ok=1 got_res got_ex got_find got_other nverdict
    cases=$((cases + 1))
    out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 \
      CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
      bash "$SELF" verify-chain "$WORK/$name.md" 2>&1) || rc=$?
    nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true)
    got_res=$(grep -c '^CHAIN hop=.* observed=resolvable ' <<<"$out" || true)
    got_ex=$(grep -c '^CHAIN hop=.* observed=exempt ' <<<"$out" || true)
    got_find=$(grep -c '^FINDING CHAIN_EXEMPT_RESOLVABLE severity=warn surface=chain obs=hop=' <<<"$out" || true)
    got_other=$(grep -cE '^FINDING CHAIN_(SOURCE|ANCHOR|CITATION)_' <<<"$out" || true)
    for tok in "${want[@]+"${want[@]}"}"; do
      [[ $out == *"$tok"* ]] || ok=0
    done
    if [[ $rc -eq $want_rc && $nverdict -eq 1 && $ok -eq 1 \
        && $got_res -eq $want_res && $got_ex -eq $want_ex \
        && $got_find -eq $want_res && $got_other -eq 0 ]]; then
      printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" "$name" "$rc"
    else
      printf 'FAIL-case %-28s exit=%d want=%d verdicts=%d resolvable=%s/%d exempt=%s/%d findings=%s/%d silent-leak=%s token=%s\n' \
        "$name" "$rc" "$want_rc" "$nverdict" "$got_res" "$want_res" "$got_ex" "$want_ex" \
        "$got_find" "$want_res" "$got_other" "${want[*]-}"
      printf '%s\n' "$out" | sed 's/^/    | /'
      failures=$((failures + 1))
    fi
  }

  write_rec chain-exempt-resolvable <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/chain_target.md |
## Chain
| hop | from | to | status | anchor_kind | anchor |
|---|---|---|---|---|---|
| 1 | C1 | lib/chain_target.md#quote:alpha row present | unresolved | | |
| 2 | C1 | S1 | blocked-no-fetch | line | omega final line |
| 3 | C1 | S1 | labelled-dead | heading | Term table |
| 4 | C1 | S1 | unresolved | quote | alpha row present |
| 5 | C1 | lib/chain_target.md#heading:Term table | blocked-no-fetch | | |
| 6 | C1 | S1 | labelled-dead | line | intro line |
| 7 | C1 | lib/chain_target.md | unresolved | quote | The craftsman certifies the work |
EOF
  tchain_audit chain-exempt-resolvable 1 7 0 \
    'RESEARCH_GATE: DRIFT' 'RESOLVED_HOPS=0/7' \
    'hops=7 verified=0 exempt=0 anchor-missing=0 refused=0 invalid=0 findings=7 drift=7 resolvable=7' \
    'FINDING CHAIN_EXEMPT_RESOLVABLE severity=warn surface=chain obs=hop=1 status=unresolved' \
    'CHAIN hop=1 status=unresolved observed=resolvable source=lib/chain_target.md anchor=quote:"alpha row present" at=line:4 verdict=mismatch' \
    'CHAIN hop=2 status=blocked-no-fetch observed=resolvable source=lib/chain_target.md anchor=line:"omega final line" at=line:6 verdict=mismatch' \
    'CHAIN hop=3 status=labelled-dead observed=resolvable source=lib/chain_target.md anchor=heading:"Term table" at=line:3 verdict=mismatch' \
    'CHAIN hop=7 status=unresolved observed=resolvable source=lib/chain_target.md anchor=quote:"The craftsman certifies the work" at=line:5 verdict=mismatch'

  printf '# research-record v1\n## Sources\n| id | tier | pointer |\n|---|---|---|\n| S1 | primary | lib/chain_target.md |\n## Chain\n| hop | from | to | status | anchor_kind | anchor |\n|---|---|---|---|---|---|\n| 1 | C1 | S1 | unresolved | quote | absent anchor text |\n| 2 | C1 | lib/ghost.md | blocked-no-fetch | line | intro line |\n| 3 | C1 | https://example.invalid/x | labelled-dead | quote | remote text |\n| 4 | C1 | S1 | unresolved | | |\n| 5 | C1 | S9 | blocked-no-fetch | line | intro line |\n| 6 | C1 | ../%s | labelled-dead | line | outside text |\n| 7 | C1 | lib/chain_near.md | unresolved | quote | alpha row present |\n| 8 | C1 | lib/chain_near.md | blocked-no-fetch | heading | plain intro line |\n| 9 | C1 | lib/chain_near.md | labelled-dead | line | omega final line |\n' \
    "$(basename "$OUTSIDE_FILE")" >"$WORK/chain-exempt-unresolvable.md"
  tchain_audit chain-exempt-unresolvable 0 0 9 \
    'RESEARCH_GATE: CLEAN' 'RESOLVED_HOPS=0/9' \
    'hops=9 verified=0 exempt=9 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0 resolvable=0' \
    'CHAIN hop=3 status=labelled-dead observed=exempt source=https://example.invalid/x anchor=- at=- verdict=exempt' \
    'CHAIN hop=6 status=labelled-dead observed=exempt' \
    'CHAIN hop=7 status=unresolved observed=exempt source=lib/chain_near.md'

  write_rec chain-exempt-judgment <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/chain_target.md |
## Chain
| hop | from | to | status | anchor_kind | anchor |
|---|---|---|---|---|---|
| 1 | C1 | S1 | rejected | quote | alpha row present |
| 2 | C1 | S1 | not-applicable | heading | Term table |
EOF
  tchain_audit chain-exempt-judgment 0 0 2 \
    'RESEARCH_GATE: CLEAN' 'RESOLVED_HOPS=0/2' \
    'hops=2 verified=0 exempt=2 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0 resolvable=0' \
    'CHAIN hop=1 status=rejected observed=exempt source=S1 anchor=- at=- verdict=exempt' \
    'CHAIN hop=2 status=not-applicable observed=exempt source=S1 anchor=- at=- verdict=exempt'

  write_rec chain-exempt-mixed <<'EOF'
# research-record v1
## Sources
| id | tier | pointer |
|---|---|---|
| S1 | primary | lib/chain_target.md |
## Chain
| hop | from | to | status | anchor_kind | anchor |
|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | quote | alpha row present |
| 2 | C1 | S1 | unresolved | line | omega final line |
| 3 | C1 | S1 | unresolved | line | omega final line extra |
EOF
  tchain_audit chain-exempt-mixed 1 1 1 \
    'RESEARCH_GATE: DRIFT' 'RESOLVED_HOPS=1/3' \
    'hops=3 verified=1 exempt=1 anchor-missing=0 refused=0 invalid=0 findings=1 drift=1 resolvable=1' \
    'CHAIN hop=1 status=resolved observed=verified source=lib/chain_target.md anchor=quote:"alpha row present" at=line:4 verdict=match' \
    'FINDING CHAIN_EXEMPT_RESOLVABLE severity=warn surface=chain obs=hop=2 status=unresolved' \
    'CHAIN hop=3 status=unresolved observed=exempt source=S1 anchor=- at=- verdict=exempt'
  # ---- round-32 C1 (r32): the --json append is one lock-held critical
  # section (verify_all opens the manifest for append on a dedicated fd, takes
  # a blocking exclusive flock(2) on that fd, then probes the last byte and
  # writes, then closes). 233: a cooperating holder of LOCK_EX on the manifest
  # keeps verify-all before its probe — while the gate is blocked the file
  # holds exactly the holder's unterminated fragment — and the append happens
  # only after release, terminating the fragment (two lines, no blank line,
  # fragment otherwise intact). 234: the lock is gone when the gate returns, so
  # a second verify-all appends its own line on the same inode.
  printf 'lock source line\n' >"$WORK/c1lk-src.txt"
  printf '{"id":"LK1","source":"c1lk-src.txt","span":"lock source line","expect":"supported"}\n' \
    >"$WORK/c1lk-record.md"
  c1lk_to=()
  if command -v timeout >/dev/null 2>&1; then c1lk_to=(timeout 120); fi
  c1lk_verify() { # MANIFEST OUT -> rc
    "${c1lk_to[@]}" env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 \
      CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
      bash "$SELF" verify-all "$WORK/c1lk-record.md" --json "$1" >"$2" 2>&1
  }
  if [[ -r /proc/locks ]] && command -v flock >/dev/null 2>&1; then
    cases=$((cases + 1))
    c1lk_msg='' c1lk_rc=0
    c1lk_mf="$WORK/c1lk-hold.jsonl"; : >"$c1lk_mf"
    c1lk_ino=$(stat -c %i -- "$c1lk_mf")
    c1lk_flag="$WORK/c1lk-release.flag"; rm -f "$c1lk_flag"
    cat >"$WORK/c1lk-holder.sh" <<'C1LK_HOLDER'
manifest=$1 flag=$2 frag=$3
exec {fd}>>"$manifest" || exit 3
flock -x "$fd" || exit 4
printf '%s' "$frag" >&"$fd" || exit 5
i=0
while [[ ! -e $flag ]]; do
  i=$((i + 1))
  if [[ $i -ge 600 ]]; then exit 6; fi
  sleep 0.1
done
C1LK_HOLDER
    bash "$WORK/c1lk-holder.sh" "$c1lk_mf" "$c1lk_flag" '{"frag":229}' &
    c1lk_hpid=$!
    c1lk_seen=0
    i=0
    while [[ $i -lt 100 ]]; do
      if [[ $(cat -- "$c1lk_mf" 2>/dev/null || true) == '{"frag":229}' ]]; then c1lk_seen=1; break; fi
      i=$((i + 1)); sleep 0.1
    done
    [[ $c1lk_seen -eq 1 ]] || c1lk_msg+='holder-fragment-absent '
    "${c1lk_to[@]}" env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 \
      CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
      bash "$SELF" verify-all "$WORK/c1lk-record.md" --json "$c1lk_mf" \
      >"$WORK/c1lk-gate-hold.out" 2>&1 &
    c1lk_gpid=$!
    c1lk_held=0
    i=0
    while [[ $i -lt 200 ]]; do
      if ! kill -0 "$c1lk_gpid" 2>/dev/null; then break; fi
      if grep -Eq "^[0-9]+:[[:space:]]+->[[:space:]]+FLOCK[[:space:]]+ADVISORY[[:space:]]+WRITE[[:space:]]+[0-9]+[[:space:]]+[0-9a-fA-F]+:[0-9a-fA-F]+:$c1lk_ino[[:space:]]" /proc/locks; then
        c1lk_held=1; break
      fi
      i=$((i + 1)); sleep 0.1
    done
    # The gate must be sitting on the lock (not finished, not past it) and the
    # manifest must still hold exactly the holder's bytes.
    if [[ $c1lk_held -eq 1 ]]; then
      [[ $(cat -- "$c1lk_mf") == '{"frag":229}' ]] || c1lk_msg+='appended-under-holder-lock '
    else
      c1lk_msg+='gate-not-blocked-on-lock '
    fi
    : >"$c1lk_flag"
    wait "$c1lk_gpid" || c1lk_rc=$?
    wait "$c1lk_hpid" || true
    n=$(wc -l <"$c1lk_mf" | tr -d ' ')
    [[ $n -eq 2 ]] || c1lk_msg+="manifest-lines=$n/2 "
    [[ $(sed -n 1p -- "$c1lk_mf") == '{"frag":229}' ]] || c1lk_msg+='fragment-line '
    sed -n 2p -- "$c1lk_mf" | grep -q '^{"schema":"chousa-verify-all/v1"' || c1lk_msg+='schema-not-own-line '
    [[ $(grep -a -c '^$' -- "$c1lk_mf" || true) -eq 0 ]] || c1lk_msg+='blank-line '
    [[ $c1lk_rc -eq 0 ]] || c1lk_msg+="gate-rc=$c1lk_rc/0 "
    [[ $(stat -c %i -- "$c1lk_mf") == "$c1lk_ino" ]] || c1lk_msg+='inode-changed '
    if command -v python3 >/dev/null 2>&1; then
      python3 -c 'import json,sys
for ln in sys.stdin.read().splitlines():
    if ln.strip():
        json.loads(ln)' <"$c1lk_mf" >/dev/null 2>&1 || c1lk_msg+='json-invalid '
    fi
    if [[ -z $c1lk_msg ]]; then
      printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" c1lk-holder-blocks-append "$c1lk_rc"
    else
      printf 'FAIL-case %-28s %s\n' c1lk-holder-blocks-append "$c1lk_msg"
      sed 's/^/    | /' "$WORK/c1lk-gate-hold.out" 2>/dev/null || true
      failures=$((failures + 1))
    fi
  else
    cases=$((cases + 1)); SKIPPED=$((SKIPPED + 1))
    printf 'skip-case %-2d %-26s reason=%s\n' "$cases" c1lk-holder-blocks-append 'no /proc/locks or no flock(1)'
  fi
  cases=$((cases + 1))
  c1lk_msg=''
  c1lk_mf2="$WORK/c1lk-second.jsonl"; : >"$c1lk_mf2"
  c1lk_ino2=$(stat -c %i -- "$c1lk_mf2")
  c1lk_rca=0 c1lk_rcb=0
  c1lk_verify "$c1lk_mf2" "$WORK/c1lk-gate-second-a.out" || c1lk_rca=$?
  c1lk_verify "$c1lk_mf2" "$WORK/c1lk-gate-second-b.out" || c1lk_rcb=$?
  n=$(wc -l <"$c1lk_mf2" | tr -d ' ')
  [[ $n -eq 2 ]] || c1lk_msg+="manifest-lines=$n/2 "
  [[ $(grep -c '^{"schema":"chousa-verify-all/v1"' -- "$c1lk_mf2" || true) -eq 2 ]] || c1lk_msg+='schema-lines '
  [[ $(grep -a -c '^$' -- "$c1lk_mf2" || true) -eq 0 ]] || c1lk_msg+='blank-line '
  [[ $c1lk_rca -eq 0 && $c1lk_rcb -eq 0 ]] || c1lk_msg+="gate-rc=$c1lk_rca,$c1lk_rcb/0,0 "
  [[ $(stat -c %i -- "$c1lk_mf2") == "$c1lk_ino2" ]] || c1lk_msg+='inode-changed '
  [[ $(tail -c1 -- "$c1lk_mf2" | od -An -tx1 | tr -d ' \n') == 0a ]] || c1lk_msg+='no-final-newline '
  if command -v python3 >/dev/null 2>&1; then
    python3 -c 'import json,sys
for ln in sys.stdin.read().splitlines():
    if ln.strip():
        json.loads(ln)' <"$c1lk_mf2" >/dev/null 2>&1 || c1lk_msg+='json-invalid '
  fi
  if [[ -z $c1lk_msg ]]; then
    printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" c1lk-second-append "$c1lk_rcb"
  else
    printf 'FAIL-case %-28s %s\n' c1lk-second-append "$c1lk_msg"
    sed 's/^/    | /' "$WORK/c1lk-gate-second-a.out" 2>/dev/null || true
    sed 's/^/    | /' "$WORK/c1lk-gate-second-b.out" 2>/dev/null || true
    failures=$((failures + 1))
  fi
  # ---- round-32 R2: verify-claims grammar/binding detectors ----
  # Routed defect R2, selftest half (corpus/lessons/round-31-verifier-spotcheck.md
  # :209-214): the round-31 mutants survived because the selftest had no case for
  # these rules. Every case below was measured against the landed gate before it
  # was asserted; expected outcomes are both the contract and the landed output.
  # A present non-string "sha256" is malformed, never absent: number, null, array
  # and object values all invalidate the record before any source is read.
  printf '{"id":"SN1","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported","sha256":5}\n' \
    >"$WORK/claims-r2-sha-nonstring.jsonl"
  printf '{"id":"SN2","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported","sha256":null}\n' \
    >>"$WORK/claims-r2-sha-nonstring.jsonl"
  printf '{"id":"SN3","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported","sha256":["%s"]}\n' "$SHA_GOOD" \
    >>"$WORK/claims-r2-sha-nonstring.jsonl"
  printf '{"id":"SN4","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported","sha256":{"v":"%s"}}\n' "$SHA_GOOD" \
    >>"$WORK/claims-r2-sha-nonstring.jsonl"
  tclaims claims-r2-sha-nonstring 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_RECORD_INVALID severity=warn surface=claims' \
    'sha256 malformed (not 64 lowercase hex characters)' \
    'CLAIM id=SN1 expected=supported observed=invalid source=claimsrc/sha-src.txt at=- verdict=invalid' \
    'CLAIM id=SN2 expected=supported observed=invalid source=claimsrc/sha-src.txt at=- verdict=invalid' \
    'CLAIM id=SN3 expected=supported observed=invalid source=claimsrc/sha-src.txt at=- verdict=invalid' \
    'CLAIM id=SN4 expected=supported observed=invalid source=claimsrc/sha-src.txt at=- verdict=invalid' \
    'VERDICT_BEARING_CLAIMS=0/4' \
    'claims=4 supported=0 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=4 findings=4 drift=4'
  # Present non-string "line" values the earlier block does not cover: null, an
  # array and a JSON float. All are "line not a JSON string" (invalid), never
  # absent and never a binding.
  cat >"$WORK/claims-r2-line-nonstring.jsonl" <<'EOF'
{"id":"LN1","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":null}
{"id":"LN2","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":["1"]}
{"id":"LN3","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":1.5}
EOF
  tclaims claims-r2-line-nonstring 1 \
    'RESEARCH_GATE: DRIFT' 'line not a JSON string' 'observed=invalid' \
    'CLAIM id=LN1 expected=supported observed=invalid source=lib/span.md at=- verdict=invalid' \
    'CLAIM id=LN2 expected=supported observed=invalid source=lib/span.md at=- verdict=invalid' \
    'CLAIM id=LN3 expected=supported observed=invalid source=lib/span.md at=- verdict=invalid' \
    'VERDICT_BEARING_CLAIMS=0/3' \
    'claims=3 supported=0 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=3 findings=3 drift=3'
  # End-line-only binding is not supported: a span starting on line 2 and ending
  # on line 3 is mislocated when only line 3 is named (the pin names a start line
  # or an exact start-end range, never an end line). EX1 shows the contrast: a
  # span lying wholly on line 3 does bind to line "3".
  cat >"$WORK/claims-r2-endline.jsonl" <<'EOF'
{"id":"EL1","source":"lib/span.md","span":"epsilon zeta eta theta\niota kappa lambda mu","expect":"supported","line":"3"}
{"id":"EX1","source":"lib/span.md","span":"iota kappa lambda mu","expect":"supported","line":"3"}
EOF
  tclaims claims-r2-endline 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims' \
    'CLAIM id=EL1 expected=supported observed=mislocated source=lib/span.md at=lines:2-3 verdict=mismatch' \
    'obs=id=EL1 line=3-3 first_delimited_occurrence=lines:2-3' \
    'CLAIM id=EX1 expected=supported observed=supported source=lib/span.md at=line:3 verdict=match' \
    'VERDICT_BEARING_CLAIMS=1/2' \
    'claims=2 supported=1 contradicted=0 unsupported=0 mismatched=1 unproven=0 refused=0 invalid=0 findings=1 drift=1'
  # Per-claim span-before-stale: a stale pin is decided before the span and the
  # "line" binding, so a claim whose span is present (or absent, or pinned to a
  # wrong line) reads stale with at=- and only the revision finding.
  printf '{"id":"SB1","source":"claimsrc/sha-src-tampered.txt","span":"sha source line two","expect":"supported","line":"1","sha256":"%s"}\n' "$SHA_GOOD" \
    >"$WORK/claims-r2-span-stale.jsonl"
  printf '{"id":"SB2","source":"claimsrc/sha-src-tampered.txt","span":"sha source line two","expect":"supported","line":"9","sha256":"%s"}\n' "$SHA_GOOD" \
    >>"$WORK/claims-r2-span-stale.jsonl"
  printf '{"id":"SB3","source":"claimsrc/sha-src-tampered.txt","span":"sha source phantom","expect":"supported","line":"1","sha256":"%s"}\n' "$SHA_GOOD" \
    >>"$WORK/claims-r2-span-stale.jsonl"
  tclaims claims-r2-span-stale 1 \
    'RESEARCH_GATE: DRIFT' 'FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=warn surface=claims' \
    'CLAIM id=SB1 expected=supported observed=stale source=claimsrc/sha-src-tampered.txt at=- verdict=mismatch' \
    'CLAIM id=SB2 expected=supported observed=stale source=claimsrc/sha-src-tampered.txt at=- verdict=mismatch' \
    'CLAIM id=SB3 expected=supported observed=stale source=claimsrc/sha-src-tampered.txt at=- verdict=mismatch' \
    "pin=${SHA_GOOD:0:12} actual=${SHA_TAMPERED:0:12}" \
    'VERDICT_BEARING_CLAIMS=0/3' \
    'claims=3 supported=0 contradicted=0 unsupported=0 mismatched=3 unproven=0 refused=0 invalid=0 findings=3 drift=3'
  # Whitespace around an otherwise 64-hex pin is malformed, never trimmed into a
  # match (leading, trailing and both sides; the existing block covers the
  # short-body leading-space shape only).
  printf '{"id":"WP1","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported","sha256":"%s "}\n' "$SHA_GOOD" \
    >"$WORK/claims-r2-ws-pin.jsonl"
  printf '{"id":"WP2","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported","sha256":" %s"}\n' "$SHA_GOOD" \
    >>"$WORK/claims-r2-ws-pin.jsonl"
  printf '{"id":"WP3","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported","sha256":" %s "}\n' "$SHA_GOOD" \
    >>"$WORK/claims-r2-ws-pin.jsonl"
  tclaims claims-r2-ws-pin 1 \
    'RESEARCH_GATE: DRIFT' 'sha256 malformed (not 64 lowercase hex characters)' \
    'CLAIM id=WP1 expected=supported observed=invalid source=claimsrc/sha-src.txt at=- verdict=invalid' \
    'CLAIM id=WP2 expected=supported observed=invalid source=claimsrc/sha-src.txt at=- verdict=invalid' \
    'CLAIM id=WP3 expected=supported observed=invalid source=claimsrc/sha-src.txt at=- verdict=invalid' \
    'VERDICT_BEARING_CLAIMS=0/3' \
    'claims=3 supported=0 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=3 findings=3 drift=3'
  # Hash-read fault injection: sha256sum unavailable through a PATH shim. The
  # same record reads supported on the normal PATH and must never read supported
  # once the hash tool is unmeasurable: fail closed to stale with actual=unreadable
  # (research-gate.sh: fail closed: an unmeasurable source is not a match). The
  # source-unreadable arm reaches the same sha_actual=unreadable branch; it is a
  # TOCTOU window (claim_source_path already required -r), so the shim is the
  # deterministic injection.
  mkdir -p "$WORK/r2faultbin"
  printf '#!/bin/sh\nexit 127\n' >"$WORK/r2faultbin/sha256sum"
  chmod +x "$WORK/r2faultbin/sha256sum"
  printf '{"id":"HF1","source":"claimsrc/sha-src.txt","span":"sha source line one","expect":"supported","sha256":"%s"}\n' "$SHA_GOOD" \
    >"$WORK/claims-r2-hash-fault.jsonl"
  cases=$((cases + 1))
  r2_ok=1 r2_ctl_rc=0 r2_fault_rc=0
  r2_ctl_out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 \
    CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
    bash "$SELF" verify-claims "$WORK/claims-r2-hash-fault.jsonl" 2>&1) || r2_ctl_rc=$?
  [[ $r2_ctl_rc -eq 0 ]] || r2_ok=0
  [[ $r2_ctl_out == *'CLAIM id=HF1 expected=supported observed=supported'* ]] || r2_ok=0
  [[ $r2_ctl_out == *'VERDICT_BEARING_CLAIMS=1/1'* ]] || r2_ok=0
  r2_fault_out=$(env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 \
    CHOUSA_ROOT="$WORK" CHOUSA_NOW_EPOCH="$NOW_EPOCH" \
    PATH="$WORK/r2faultbin:$PATH" \
    bash "$SELF" verify-claims "$WORK/claims-r2-hash-fault.jsonl" 2>&1) || r2_fault_rc=$?
  [[ $r2_fault_rc -eq 1 ]] || r2_ok=0
  [[ $r2_fault_out == *'FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=warn surface=claims'* ]] || r2_ok=0
  [[ $r2_fault_out == *'actual=unreadable'* ]] || r2_ok=0
  [[ $r2_fault_out == *'VERDICT_BEARING_CLAIMS=0/1'* ]] || r2_ok=0
  [[ $r2_fault_out != *'observed=supported'* ]] || r2_ok=0
  if [[ $r2_ok -eq 1 ]]; then
    printf 'ok-case  %-2d %-28s exit=%d\n' "$cases" r2-hash-fault-shim "$r2_fault_rc"
  else
    printf 'FAIL-case %-28s control_rc=%d fault_rc=%d\n' \
      r2-hash-fault-shim "$r2_ctl_rc" "$r2_fault_rc"
    printf '%s\n' "$r2_ctl_out" "$r2_fault_out" | sed 's/^/    | /'
    failures=$((failures + 1))
  fi
  # Nested-key contract, string half: a key spelling inside a STRING value is not
  # a field. The object half ({"meta":{"line":"9"}} read as the record's own key
  # until round 32, .ufo/waves/round-32/w1/ExecR2Selftest31.md) is fixed by the
  # round-33 top-level reader (claim_scan) and asserted by the r33-top-* cases
  # at the end of the selftest.
  printf '{"id":"NS1","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","note":"{\\"line\\":\\"9\\"}"}\n' \
    >"$WORK/claims-r2-nested-string.jsonl"
  tclaims claims-r2-nested-string 0 \
    'RESEARCH_GATE: CLEAN' 'VERDICT_BEARING_CLAIMS=1/1' \
    'CLAIM id=NS1 expected=supported observed=supported source=lib/span.md at=line:1 verdict=match'
  # ---- round-33 C1 selftest cases (top-level field reader) ----
  # A claim's read fields are members of its top-level object only: a member of
  # the same name inside a nested object or array changes nothing, characters
  # inside a string value are never structure, and a read field repeated among
  # the top-level members makes the record invalid (corpus/evidence/round33/
  # claims.md, C1 contract). Each case below was measured on the landed gate
  # (the nested decoy reads as the record's field there) and on this reader.
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
  # ---- round-33 post-falsify repairs (wave 2): fail closed on what the reader
  # still accepted. A bare token that is not a JSON literal or number (at the
  # top level or inside a nested value) and a form feed between members make
  # the line malformed; the counted C1 classes never contain either.
  printf '%s\n' \
    '{"id":"PF1","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","x":tru}' \
    '{"id":"PF2","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","x":{"y":xyz}}' \
    '{"id":"PF3","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","x":[1,-2.5e3,true,null,"q"]}' \
    >"$WORK/r33-post-literals.jsonl"
  printf '{"id":"PF4",\f"source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported"}\n' \
    >>"$WORK/r33-post-literals.jsonl"
  tclaims r33-post-literals 1 \
    'RESEARCH_GATE: DRIFT' \
    'CLAIM id=line1 expected=- observed=invalid source=- at=- verdict=invalid' \
    'CLAIM id=line2 expected=- observed=invalid source=- at=- verdict=invalid' \
    'CLAIM id=PF3 expected=supported observed=supported source=lib/span.md at=line:1 verdict=match' \
    'CLAIM id=line4 expected=- observed=invalid source=- at=- verdict=invalid' \
    'claims=4 supported=1 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=3 findings=3 drift=3'
  # An escaped NUL in a read string field would decode away ("al\u0000pha" ->
  # "alpha"); it is refused as sha256 already was. A marker-default row with a
  # repeated read field is refused, and three id repeats print the id only when
  # every repeat agrees.
  printf '%s\n' \
    '{"id":"PN1","source":"lib/span.md","span":"al\u0000pha beta gamma delta","expect":"supported"}' \
    '{"marker_default":"M","line":"1","line":"2"}' \
    '{"id":"PN3","id":"PN3","id":"PN9","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported"}' \
    '{"id":"PN4","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","note":"literal \\u0000 text"}' \
    >"$WORK/r33-post-nul-dup.jsonl"
  tclaims r33-post-nul-dup 1 \
    'RESEARCH_GATE: DRIFT' 'span holds an escaped NUL' \
    'CLAIM id=PN1 expected=supported observed=invalid source=lib/span.md at=- verdict=invalid' \
    'CLAIM id=line2 expected=- observed=invalid source=- at=- verdict=invalid' \
    'CLAIM id=line3 expected=supported observed=invalid source=lib/span.md at=- verdict=invalid' \
    'CLAIM id=PN4 expected=supported observed=supported source=lib/span.md at=line:1 verdict=match' \
    'claims=4 supported=1 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=3 findings=3 drift=3'
  # An escape outside RFC 8259 §7 ("\q", "\x", a short "\u12") is malformed in a
  # member name, a string value or a nested string; valid escapes (including a
  # surrogate pair) and a 20 KiB unread member still verify (the reader consumes
  # runs with one regex match each, r33 post-falsify).
  printf '%s\n' \
    '{"id":"PE1","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","n":"a\q"}' \
    '{"id":"PE2","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","m":["\x"]}' \
    '{"id":"PE3","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","n":"\u12"}' \
    '{"id":"PE4","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","n":"a\u00e9\n\t\/\\\"z","m":{"k":"\uD83D\uDE00"}}' \
    >"$WORK/r33-post-escapes.jsonl"
  printf '{"id":"PE5","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","pad":"%s"}\n' \
    "$(printf '%*s' 20480 '' | tr ' ' w)" >>"$WORK/r33-post-escapes.jsonl"
  tclaims r33-post-escapes 1 \
    'RESEARCH_GATE: DRIFT' \
    'CLAIM id=line1 expected=- observed=invalid source=- at=- verdict=invalid' \
    'CLAIM id=line2 expected=- observed=invalid source=- at=- verdict=invalid' \
    'CLAIM id=line3 expected=- observed=invalid source=- at=- verdict=invalid' \
    'CLAIM id=PE4 expected=supported observed=supported source=lib/span.md at=line:1 verdict=match' \
    'CLAIM id=PE5 expected=supported observed=supported source=lib/span.md at=line:1 verdict=match' \
    'claims=5 supported=2 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=3 findings=3 drift=3'

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
    verify-metadata) MODE=metadata; shift ;;
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
    --registry)
      [[ $# -ge 2 ]] || die_usage "--registry needs PATH"
      REGISTRY_ARG=$2; REGISTRY_ARG_SET=1; shift 2 ;;
    --claims)
      [[ $# -ge 2 ]] || die_usage "--claims needs PATH"
      CLAIMS_ARG=$2; shift 2 ;;
    --json)
      [[ $# -ge 2 ]] || die_usage "--json needs PATH"
      JSON_ARG=$2; shift 2 ;;
    --as-of)
      [[ $# -ge 2 ]] || die_usage "--as-of needs YYYY-MM-DD"
      AS_OF_ARG_SET=1; AS_OF_ARG=$2; shift 2 ;;
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
if (( AS_OF_ARG_SET )); then
  [[ $MODE == metadata ]] || die_usage "--as-of is only valid with verify-metadata"
  metadata_iso_date "$AS_OF_ARG" || die_usage "--as-of must be a valid YYYY-MM-DD date"
fi
if ((REGISTRY_ARG_SET)) && [[ $MODE != metadata ]]; then
  die_usage "--registry is only valid with verify-metadata"
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
  metadata)
    METADATA_PATH=${RECORD_ARG:-}
    verify_metadata "$METADATA_PATH"
    ;;
  all)
    ALL_PATH=${RECORD_ARG:-${CHOUSA_RECORD:-}}
    verify_all "$ALL_PATH"
    ;;
  *) die_usage "unknown mode: $MODE" ;;
esac
