# K3 candidate: corpus/fixtures/sweeps-r5.README.md  (base gate 5d792e1e vs landed gate b4a41d25, same record bytes, same corpus)
# record has no <!-- chousa-record: v1 --> marker; it is fixture documentation with a prose rejection table

## base gate (five-d792 gate in tree /fast/scratch/hyaku/chousa-r82/R82ExecRepro/tree-k3)
research-gate: record not found: ../corpus/fixtures/sweeps-r5.README.md
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
rc=2

## landed gate (tree /fast/scratch/hyaku/chousa-r82/R82ExecRepro/tree-b4a41d251b488f06b4a6ab01a11bc12ce72edd20)
research-gate v2 — ts=2026-11-06T20:08:30Z — mode=sweeps — record=corpus/fixtures/sweeps-r5.README.md
REJECTION id=R1 ref=research/README.md:12 reason=absent flip=present observed=incomplete verdict=mismatch
REJECTION id=R2 ref=B-multiagent-knowledge.md:79 reason=absent flip=present observed=incomplete verdict=mismatch
REJECTION id=R3 ref=B-multiagent-knowledge.md:63 reason=absent flip=present observed=incomplete verdict=mismatch
FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=id=R1 missing=reason section=Rejections — provenance and flip-conditions
FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=id=R2 missing=reason section=Rejections — provenance and flip-conditions
FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=id=R3 missing=reason section=Rejections — provenance and flip-conditions
VERIFIED_SWEEPS=0/0 REJECTIONS_OK=0/3
RESEARCH_GATE: DRIFT (sweeps=0 verified=0 exempt=0 hit=0 refused=0 invalid=0 rejections=3 rejections-ok=0 findings=3 drift=3)
rc=1

## landed gate, verify mode
research-gate v2 — ts=2026-11-06T20:08:30Z — mode=verify — record=corpus/fixtures/sweeps-r5.README.md
FINDING RECORD_SCHEMA_INVALID severity=warn surface=meta obs=no research-record sections/banner detected
FINDING NO_QUESTION severity=crit surface=question obs=missing ## Question section
FINDING SOURCE_TABLE_ABSENT severity=warn surface=sources obs=missing ## Sources / ## Source table
FINDING CLAIM_TABLE_ABSENT severity=warn surface=claims obs=missing ## Claims
FINDING REJECTION_DROPPED severity=warn surface=rejections obs=missing ## Rejections section
RESEARCH_GATE: DRIFT (findings=5 drift=5 questions=0 sources=0 chains=0 claims=0 negatives=0 rejections=0 approvals=0)
rc=1

## header line of the prose table
76:| id | ref | reason (from the method) | flip_condition |
