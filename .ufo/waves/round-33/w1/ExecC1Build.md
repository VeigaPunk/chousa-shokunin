# ExecC1Build — round 33 wave 1: C1 top-level member reader (candidate build)

Sandbox: `/fast/scratch/hyaku/chousa-r33/w1/ExecC1Build/clone` (git clone of the lane,
`git checkout 3b528b9a926dd53001a1f1da5df6be1c63fca3ca`; `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`
unset). Base gate copy: `base/research-gate.sh`, SHA-256 `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0`.

## Verdict

Build delivered and measured. **The P1 verdict is not mine to issue**: per the wave control rule no
seat runs `c1-count.py` against a candidate, so I ran the counter **zero times** on this build (and
zero times on anything else). What I can state from commands I ran: the reader is a single-pass,
string-state-aware top-level member scan; every pre-existing behaviour I could compare is byte-identical
(241 base selftest case lines, six lane claims fixtures); the selftest is PASS 248/248 with the seven
new cases; and the shapes the frozen claim names (nested decoy before/after, nested-only, duplicated
read key, string confuser, deep container, unparsable line) behave per the contract on my own probes.

## What changed (one file, `tools/research-gate.sh`)

`git -C clone diff --stat` → `1 file changed, 273 insertions(+), 16 deletions(-)`.
Patch: `.ufo/waves/round-33/w1/ExecC1Build/candidate.patch`,
SHA-256 `d82f0b08325ec13473618dfbb9f4120c4f969c08ea98d02b23f17cd7eeedadc1`.
Candidate gate: same artifact copy `candidate-research-gate.sh`,
SHA-256 **`d9786947c818b3ac6727373c4ba450f7c33c3115d2a6b086abbbdd8de285aa12`** (349 829 bytes).
`git -C verifyclone apply --check` on a pristine clone at the tip, then `apply` → the resulting
`tools/research-gate.sh` has the same SHA-256 `d9786947…aa12` (reproducible).

New/changed regions in the candidate (`candidate-research-gate.sh` line numbers):

- `:1109-1127` header comment + `declare -A JSON_PRESENT JSON_STR JSON_DUP JSON_DUPSTR JSON_DUPNONSTR`.
- `:1129-1246` `claim_scan LINE` — one pass, `LC_ALL=C`, string-state aware (quote, backslash escape,
  escaped backslash before a closing quote), bracket stack over `{}`/`[]` outside strings, depth-1
  members only. Records `JSON_PRESENT[K]` (any value type), `JSON_STR[K]` (raw string body, escapes
  intact — byte-for-byte what `json_str` returned before), `JSON_DUP[K]` (repeated at top level) and
  the second occurrence's value (`JSON_DUPSTR` string body / `JSON_DUPNONSTR` flag). Nested values are
  skipped whole; characters inside strings are never structure. Fails closed (`rc=1`, empty tables) on
  unbalanced/mismatched brackets, an unterminated string, trailing bytes after the object, a member
  name that is not a string, and `}` right after a comma. The last scanned line is cached, so the
  accessors scan once per record.
- `:1253-1272` `json_str` / `json_has_key` keep their call shape and semantics and now read the table;
  new `json_dup LINE KEY`.
- `:1593-1607` `verify_claims`: unparsable line → `CLAIM_RECORD_INVALID … not one well-formed JSON
  object` and `CLAIM id=line<N> expected=- observed=invalid source=- at=- verdict=invalid` (never
  supported); the marker-default row test additionally requires `! json_dup id && ! json_dup
  marker_default`.
- `:1611-1640` `verify_claims`: duplicate read-key refusal before any field use. Reason
  `duplicate top-level key <k>`, first duplicate in the order `id source span expect marker line
  sha256 marker_default`. CLAIM line: `observed=invalid`; `source`/`expected` print `-` when that key
  is the duplicated one; a duplicated `id` prints that id only when the two decoded values are
  byte-identical, otherwise `id=line<N>` (L1 clarification, honoured — see probe below).
- `:7545-7626` one contiguous selftest block appended at the END (7 cases, names `r33-top-*`).

No other function, mode, message or exit code was touched. `json_unescape` and every caller line after
the reader are unchanged.

## Evidence

### Selftest (`timeout 1800 bash <gate> --selftest`)

- Base: `base-selftest.out`, `rc=0`, `real 0m30.284s`, `RESEARCH_GATE_SELFTEST: PASS (241 cases, 0 skipped)`.
- Candidate: `selftest-candidate.out`, `rc=0`, `real 0m37.6s`,
  `RESEARCH_GATE_SELFTEST: PASS (248 cases, 0 skipped)` (248 = 241 + 7).
- Case lines (`case-lines-base.txt` 241, `case-lines-candidate.txt` 248,
  `case-line-diff-summary.txt`): first 241 lines `diff` empty → **byte-identical**; full diff is
  `241a242,248` only:
  ```
  ok-case  242 r33-top-nested-line          exit=0
  ok-case  243 r33-top-nested-sha           exit=0
  ok-case  244 r33-top-nested-id            exit=0
  ok-case  245 r33-top-dup-line             exit=1
  ok-case  246 r33-top-confuser-flat        exit=0
  ok-case  247 r33-top-confuser-nested      exit=0
  ok-case  248 r33-top-dup-id               exit=1
  ```
- New cases and what they pin: nested `line` decoy before the top-level member (supported, `at=line:1`);
  nested-only `sha256` naming 64 hex zeros (supported — a read nested pin would read stale); nested
  `id` decoy before the top-level id (CLAIM line names the top-level id); duplicated top-level `line`
  (invalid, `duplicate top-level key line`, id kept); flat string confuser with `{ [ ,` and a trailing
  escaped backslash (`"…backslash \\"`) (unchanged supported verdict); nested container whose string
  holds `} ] {` plus a wrong nested `line` before the top-level `line` (supported); duplicated `id`,
  identical vs differing (id kept vs `id=line2`).

### Byte-identical outputs on lane fixtures

`CHOUSA_STRICT=0 bash <gate> verify-claims <lane>/corpus/fixtures/<f>.jsonl --root <lane>` for
`claims-r2`, `claims-r9`, `full-r6.claims`, `full-r6-broken.claims`, `integrity-r7.claims`,
`integrity-r7-broken.claims`: base and candidate exit codes equal (`rc=1` for all six) and, with only
the `— ts=…` header field normalised, `diff` empty for all six (`cmp-<f>-{base,cand}.norm` in scratch).

### Timing (required pair)

`verify-claims <lane>/corpus/fixtures/claims-r2.jsonl --root <lane>` (17 records):
base 181 / 171 / 179 ms; candidate 216 / 227 / 225 ms (3 runs each, wall clock around `bash`).
Larger probes (scratch `smoke/`):
- 144 flat records, `smoke/many-flat.jsonl`: base 2 572 ms vs candidate 2 935 ms, both
  `VERDICT_BEARING_CLAIMS=144/144`, outputs identical after ts normalisation → reader overhead
  ≈ +2.5 ms/record.
- 144 nested-decoy records, `smoke/many.jsonl` (SHA-256 `3316e3a6…a794841`, 144 lines, deep
  container + nested `line`/`sha256` before the top-level members): base 917/974 ms `0/144` (reads the
  nested `sha256=zz` → invalid); candidate 3 544/3 456 ms `144/144` (it now verifies the records the
  base refused, hence the longer wall time).
- Scanner alone (`source`d `claim_scan` over the same 144 lines, `/tmp/bench.sh`): 129 ms total,
  ≈ 0.9 ms/record.

### Probes (scratch, quoted from console)

`smoke/dupid.jsonl` → `dup-id-probe.jsonl`:
```
CLAIM id=DI1 expected=supported observed=invalid source=src/a.md at=- verdict=invalid
CLAIM id=line2 expected=supported observed=invalid source=src/a.md at=- verdict=invalid
CLAIM id=line3 expected=supported observed=invalid source=src/a.md at=- verdict=invalid
FINDING CLAIM_RECORD_INVALID severity=warn surface=claims obs=line=1 duplicate top-level key id
```
(identical dup id prints the id; differing dup id and non-string second occurrence print `id=line<N>`.)

`smoke/decoy2.jsonl` → `nested-decoy-probe.jsonl`: nested `marker` before `expect=supported` and a
deep `[{"sha256":"zz","line":"3"}]` decoy → candidate `supported` ×4, `RESEARCH_GATE: CLEAN`; base
`invalid` ×2 (nested `marker` read as "marker present but expect=supported", nested `sha256=zz`
read as malformed).

`smoke/edge.jsonl` (candidate, `rc=1`): empty-string member name parses and is ignored; `"a":[}]}` and
`"a":"unterminated}` → `not one well-formed JSON object`, `CLAIM id=lineN … observed=invalid`;
`"line":2` → `line not a JSON string` (unchanged); `{}`/`[]` values skipped; key spelled `l\u0069ne`
is not read as `line` (the not-claimed escape case stays unread).

## Contract mapping (claims.md:29-39)

1. top-level-only fields — `claim_scan` skips nested objects/arrays whole (`:1185-1211`); probes and
   selftest cases 242, 243, 244, 247 above.
2. duplicate read field → invalid — `:1611-1640`, case 245 and probe `dupid.jsonl`.
3. string content is never structure — escape/`\\` handling at `:1176-1183`, `:1189-1210`; cases 246/247.
4. everything else unchanged — 241 identical case lines, six identical fixture outputs, unchanged
   messages, exit codes and counters.

## Limits

- `c1-count.py` was not run on this build or on any other gate (control rule). The 144-record fixture
  classes were reasoned about from the counter source (`c1-count.py:96-113`, `:203-300`) and probed with
  my own fixtures, not scored.
- `marker_default` duplicate rows are refused as invalid (fail closed); claims.md lists marker_default
  rows as not claimed, so this is a fail-closed choice, not a measured requirement.
- Two occurrences of a read key are compared after `json_unescape` (decoded bytes); the duplicate
  refusal itself is raw scan, independent of value equality.
- Not measured: behaviour on multi-megabyte claim lines (the reader is O(n) with a ~0.9 ms/record
  constant on ~200-byte records); `verify-all` manifest parsing is untouched.
- No installs or upgrades; no network; no lane production file, jj state or git index touched (lane
  `tools/research-gate.sh` still `f4731885…f0`). One selftest run was moved to a harness background job
  (`bg_3003`); it completed and nothing was signalled.

## Artifacts (all in `.ufo/waves/round-33/w1/ExecC1Build/`)

| file | sha256 |
|---|---|
| `candidate.patch` | `d82f0b08325ec13473618dfbb9f4120c4f969c08ea98d02b23f17cd7eeedadc1` |
| `candidate-research-gate.sh` | `d9786947c818b3ac6727373c4ba450f7c33c3115d2a6b086abbbdd8de285aa12` |
| `selftest-base.out` | `202702b410343f9442378624c87d3fadd9d8c617af48892f782b0051bb05a465` |
| `selftest-candidate.out` | `cadf3e0ae127f7831aa8bac8f4e6244141026e457c9781429096e0586e5e07b5` |
| `case-line-diff-summary.txt` | `6141c23381bf0c31889101a92967e30662f65bb3a3fa6f86857473056a316c25` |
| `dup-id-probe.jsonl` | `df53ae238f6f4a104a6ff8b21919cf3587096ff9953018ddef0caf387e9f2b1e` |
| `nested-decoy-probe.jsonl` | `1351925c4eb7d58bf3ce1bbfddc1a8e4a5287f6de2ab20ffba3ec245e2aa290c` |

Scratch (not copied): `/fast/scratch/hyaku/chousa-r33/w1/ExecC1Build/{clone,verifyclone,base,smoke,*.out,*.txt}`.
No receipts: this seat produced no counter receipt.
