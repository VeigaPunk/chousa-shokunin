# ExecC2Impl — C2 revision-binding build (round 31, WAVE 1 BUILD)

Seat: ChousaR31.ExecC2Impl. Scope: tools/research-gate.sh only, in the sandbox
clone at d78d18893849cecb710f3b691ec986e1321d39ee. No runs of c1-count.py /
c2-count.py (wave rule respected).

## Answer to L1 interjection (04:26:45Z lane rewrite)
NO — I never edited or copied over the lane gate
/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh. All edits
were made only in the clone /fast/scratch/hyaku/chousa-r31/w1/ExecC2Impl/repo/
(edit tool + `bash" runs against that clone's absolute path). Timing of my
clone edits: ~04:24-04:26Z (first selftest of the modified clone finished
~04:28Z, after the rewrite timestamp). I have no write access to lane files
except my report dir; no git/jj writes anywhere.

## What was implemented (contract C2, claims.md)
verify-claims gains the optional JSON string field "sha256" (exactly 64
lowercase hex, no trimming/prefix/uppercase):
1. Present malformed value (incl. present-empty) → `observed=invalid`,
   CLAIM_RECORD_INVALID. `json_str` rc distinguishes absent vs present-empty
   (`sha_present` flag; `jfield` never used for presence).
2. Boundary refusals keep precedence: hash check runs only after
   `claim_source_path` succeeds (refused sources are never hashed).
3. After resolution: `sha256sum -- "$path"` on the exact canonical source
   bytes (never the `$(cat)` string); mismatch → `observed=stale` +
   FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=warn surface=claims
   `id=… pin=<12> actual=<12>`, `at=-`, span check skipped. Equal → existing
   span verdict. Absent → unchanged.
4. stale counts only as a mismatch (N_MISM): no new summary field, summary
   line format untouched. `set -euo pipefail` kept; matcher uses the same
   fixed `^[0-9a-f]{64}$` bracket (ASCII-safe).
Header comment, finding-ID list and `--help` updated; 9 selftest cases
(216-224) appended after case 215, each contract rule with a pass and a fail
case + boundary precedence + CRLF handling (exact-bytes hash, span behavior
today).

## Evidence
- `cd <clone> && timeout 1800 bash tools/research-gate.sh --selftest` →
  `RESEARCH_GATE_SELFTEST: PASS (224 cases, 0 skipped)`, exit 0 (base 215;
  new cases 216-224 all `ok-case`). Tail captured at
  /fast/scratch/hyaku/chousa-r31/w1/ExecC2Impl/selftest-tail.txt.
- `bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl
  --root /home/vgpnk/Projects/shokunin` →
  `VERDICT_BEARING_CLAIMS=17/17`, `RESEARCH_GATE: CLEAN`, exit 0. Base-gate
  run on the same input is byte-identical modulo ts (diff of normalized
  outputs empty).
- `bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md
  --root /home/vgpnk/Projects/shokunin` → `RESOLVED_HOPS=17/22` CLEAN,
  exit 0 (extra no-harm).
- `bash tools/research-gate.sh --drift
  corpus/evidence/gate-baseline-r12-20261019T115519Z.json` → `GATE_DRIFT:
  none`, exit 0; base gate at d78d188 gives the same (`GATE_DRIFT: none`,
  exit 0). Diff of both drift outputs empty → drift result unchanged at
  d78d188.
- Manual fixture runs of every new path (match / stale / invalid / validity /
  CRLF / refused) produced the expected CLAIM/FINDING lines and exit codes,
  e.g. stale: `FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=warn
  surface=claims obs=id=T1 pin=ed82fd71c85e actual=a1b069a5106d`;
  invalid present-empty: `obs=line=2 sha256= invalid`.
- `git -C <clone> diff d78d18893849cecb710f3b691ec986e1321d39ee -- tools/research-gate.sh`
  → c2.patch (197 lines) at
  .ufo/waves/round-31/build/ExecC2Impl/c2.patch; applies cleanly
  (`git apply --check` on a pristine d78d188 clone: PATCH_APPLIES_CLEAN).
- Candidate SHA-256 (modified tools/research-gate.sh):
  `41b294fda032d037e8e947d384b84cbd803760bea591ddb61cd6af973458b82d`.

## Verdict
C2 contract implemented and self-tested; no-harm checks all green (selftest
224/224, claims-r2 17/17 CLEAN, chain-r3 17/22 CLEAN, drift none/identical
to base). Patch delivered at the acceptance path.

## Limits
- Sha-regex is ASCII-range; under exotic multibyte locales `[0-9a-f]`
  stays byte-equivalent (no LC_ALL change introduced; existing token matcher
  keeps its `local LC_ALL=C`).
- The pin compares content bytes, not git revisions (claim intent; no
  commit binding).
- Non-string `"sha256"` values (e.g. numbers) are treated as absent, like
  other fields' non-string handling; not in the frozen counter classes.
- Tool installs/updates: none (no channel records).
