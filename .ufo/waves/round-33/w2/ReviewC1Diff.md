# Wave 2 — ReviewC1Diff: C1 diff review, tools/research-gate.sh (base f4731885 → landed 94a7be5a)

Scope: `claim_scan` correctness vs RFC 8259 claim-line subset, the duplicate path in
`verify_claims`, the scan cache, locale handling, `json_unescape`/`scan_secrets`
interaction, error paths. Line numbers below are the landed gate
(`tools/research-gate.sh` @ `0fb300b5`, SHA-256 `94a7be5a…`).

Scratch: `/fast/scratch/hyaku/chousa-r33/w2/ReviewC1Diff/` (gate-landed.sh = verified
94a7be5a copy, gate-base.sh = verified f4731885, probes/*.jsonl+*.out, keep4291/).

## Counter runs (kill rule; every run reported)

| seed | gate_sha256 | result | receipt |
|---|---|---|---|
| 4117 | `b808e9b5…` (NOT landed) | TOPLEVEL_FIELD_MATCH=0/156, rc=1, gate_rc=1, no DRIFT line | `.ufo/waves/round-33/w2/ReviewC1Diff/c1-v2-s4117.json` |
| 4291 | `263ffb9d…` (NOT landed) | TOPLEVEL_FIELD_MATCH=156/156, predicate_holds=true | `…/c1-v2-s4291.json` |
| 4493 | `94a7be5a…` (landed copy) | TOPLEVEL_FIELD_MATCH=156/156, predicate_holds=true, gate_rc=1 | `…/c1-v2-s4493.json` |
| 4529 | `94a7be5a…` (landed copy) | TOPLEVEL_FIELD_MATCH=156/156, predicate_holds=true, gate_rc=1 | `…/c1-v2-s4529.json` |

Commands: `prlimit --nproc=2000 --as=4000000000 -- timeout 900 python3
corpus/evidence/round33/c1-count-v2.py --gate <gate> --seed N --receipt <f>` from the
lane root, stdout redirected to `c1-s*.stdout`. Seeds 4117/4291/4493/4529 are fresh.

**Incident that produced the 0/156:** `tools/research-gate.sh` in the lane worktree was
modified while I worked — `94a7be5a` at 09:0x, `b808e9b5` during the s4117 run,
`263ffb9d` at s4291, `165acd5f` later. The s4117 miss ran against a transient mutated
file, not the landed revision: receipt `gate_sha256=b808e9b5`, `gate_rc=1`, no
`RESEARCH_GATE: DRIFT` line, so every record scored `none`. It is a run on the landed
*path* but not on the landed *bytes*; per the kill rule I report it verbatim. The
in-flight diff (uncommitted, `git diff`) is an L1 fix for wave-2 findings: it replaces
`[[:space:]]` with `$' \t\r\n'`, validates bare tokens against a literal/number regex
inside nested containers, and replaces `JSON_DUPSTR/JSON_DUPNONSTR` with a raw-body
`JSON_DUPDIFF` — crediting `ProbeWhitespace33`, `ProbeMalformed33`,
`ProbeFlatBehaviour33`, `CriticClaim33`. I did not write to the lane; all verdicts
below are measured on my verified `gate-landed.sh` copy (SHA re-verified before the
probe sweep: `94a7be5a…`).

## Findings

### F1 (MEDIUM, contract-honesty, fail-open): "not one well-formed JSON object" is only partially enforced

claims.md (v2, "Not claimed"): "lines that are not exactly one valid JSON object (the
candidate is asked to fail closed on them; no fixture class counts it)". Landed usage
text (:365-367) and header comment (:50-53, :1126-1128) promise invalid on any line
that "is not one well-formed JSON object". `claim_scan` validates the top-level member
grammar but not RFC 8259 elsewhere — measured on landed gate
(`bash gate-landed.sh verify-claims probes/X.jsonl --root root`, rc + CLAIM lines in
`probes/*.landed.out`):

- `{"id":"P1","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","note":tru}`
  → `observed=supported`, `RESEARCH_GATE: CLEAN`, rc 0 (probe A). The bare-token branch
  (:1204-1216) accepts any run of non-delimiter bytes: `tru`, `1x`, `1:2`, `x"`, `\`.
- `…,"meta":{"a":,}` (probe B) and `…,"meta":{"b"}` (probe J) → `observed=supported`,
  CLEAN, rc 0. Inside `{}`/`[]` only bracket balance and string state are checked
  (:1199-1224); member grammar, commas and colons inside nested values are unchecked.
- `{"id":"P3",\x0b"source":…}` (probe C) → CLEAN. `[[:space:]]` in the skip loops
  (:1145, :1150, :1171, …) admits `\v` and `\f`, which RFC 8259 §2 excludes from
  whitespace. (The in-flight mutated gate fixes this one class.)
- `…,"note":"a\x01b"}` (probe D) → CLEAN. Raw control bytes U+0000-001F inside strings
  are accepted (RFC 8259 §7 requires escaping). Base did the same; only landed
  *promises* well-formedness.

Same inputs print CLEAN on the base gate too — this is not a verdict regression but a
fail-open gap between the landed gate's documented contract and its parser, on inputs
the counter never emits (the counter writes only `json.dumps` output). P1 is
unaffected; the gap is the "asked to fail closed" clause in claims.md.

### F2 (LOW): duplicated `marker_default` converts a marker row into an invalid claim

`{"marker_default":"M","marker_default":"N"}` — landed: `CLAIM_RECORD_INVALID`, claims=1,
DRIFT (probe H). Base: silently consumed, claims=0, CLEAN (`probes/H.base.out`).
Contract: a `{"marker_default":…}` row "is not a claim" (gate header); the v2 counted
dup list is line/sha256/source/span/expect/id — `marker_default` is neither listed as
counted nor explicitly excused the way `marker` and differing `id` are. Landed reads
the dup list `id source span expect marker line sha256 marker_default` (:1621), so a
duplicated `marker_default` is a drift-emitting claim where the pre-C1 wording suggests
the row should never be one. Deliberate fail-closed reading, but it is a behavior
change on an unenumerated input with no contract citation.

### F3 (LOW): dup-`id` identical test compares decoded bodies, not raw

Landed keeps `show_id=<id>` when the second `id` unescapes equal to the first
(:1636-1639: `id2 == id` after `json_unescape`). `{"id":"\u0044I","id":"DI",…}` has
distinct raw bodies yet prints `id=DI` — the id shown is strictly the *second*
spelling's decode while the first occurrence was `"\u0044I"`. Cosmetic only (the
record is invalid either way; the counter generates identical raw+decoded values).
The in-flight patch's `JSON_DUPDIFF` already switches this to raw-body comparison.
Also observed: `{"id":"P9","id":5,…}` → `id=line1` (probe I); `{"id":5,"id":"PX",…}` →
`id=line1` (probe T); `{"id":"a","id":{"x":1},…}` → `id=line1` (probe U). All correct
per "differing or non-string values leave the id unreadable".

### F4 (LOW, operability): claim_scan is per-byte; large lines stall verify-claims

One 2 MB claim line (`"pad":"xx…"`): `timeout 60` killed `verify-claims` after 60 s
wall / 10m16s user (bg_4317, exit 124). The per-byte `${s:i:1}` walk forks nothing but
bash substring+pattern work per byte is ~30 µs/byte → minutes per MB. No timeout exists
in verify_claims; a large or adversarial claims file DoSes the checklist command.
Counter lines (~1-2 KB) are unaffected; P1 unaffected.

## Verified correct on the landed gate (no finding)

- Top-level grammar checks that exist are right: `{"a":1,}` trailing comma, `{}}`,
  `{"id":"PR"} {}` trailing garbage, `{"x":[1,}` mismatched bracket, `{` unclosed →
  all CLAIM_RECORD_INVALID (probes E, P, R). `allow_close` correctly permits `{}` only.
- Nested-skip honours strings and escapes: confuser strings with `] } , :`, escaped
  quotes, and a trailing `\\` end strings correctly (selftest r33-top-* cases + my M/Q).
- Keys are raw (escapes intact): `"l\u0069ne":"9"` does not bind `line` (probe N,
  observed=supported at=line:1) — matches the not-claimed escape-keys clause.
- Cache: `JSON_SCAN_LINE` hit path returns the same rc; `jfield`/`json_str` subshells
  inherit the parent's tables so the per-record rescan happens once. No staleness
  path found: every accessor re-calls `claim_scan "$line"`.
- `LC_ALL=C` is correctly scoped (`local` inside `claim_scan`); `[[ $c == [$ws] ]]`-style
  matching and byte indexing are locale-safe. The `verify_claims` edge-trim still uses
  caller-locale `[[:space:]]` — consistent with base.
- Dup display rules measured: identical `id` dup prints the id (K), differing/non-string
  prints `lineN` (I/T/U); dup `expect`→`expected=-` and dup `source`→`source=-` (G);
  unread-key dups allowed (L); `marker_default` row still consumed when clean (S).
- `json_unescape`/`scan_secrets` interaction unchanged: raw bodies keep escapes
  intact; `scan_secrets` runs on the raw file before the loop — untouched by C1.
- Counter input space: `generate()` emits only `json.dumps` records (`, `/`: `
  separators, ASCII) — every emitted line is well-formed JSON, so F1's fail-open is
  unreachable from the counter; combined with correct top-level handling this is why
  156/156 reproduces on seeds 4493/4529 (and 4291 on the mutated gate).

## Verdict

**C1 HOLDS on the landed gate.** Two fresh-seed runs on verified `94a7be5a` bytes print
156/156 (receipts `c1-v2-s4493.json`, `c1-v2-s4529.json`). The s4117 0/156 is a
worktree-mutation artifact (gate_sha `b808e9b5` ≠ landed); it does not falsify P1,
which is defined on the landed revision. Contract items 1-3 are correctly implemented
for every input class the counter generates. Residual risk: F1 fail-open on non-JSON
input contradicts the gate's own documented contract (un-counted by P1); F2/F3 are
minor unenumerated-input deviations; F4 is an operability DoS on large claims files.
The live, uncommitted worktree edit partially remediates F1/F3 but leaves nested-value
grammar and in-string control bytes fail-open.
