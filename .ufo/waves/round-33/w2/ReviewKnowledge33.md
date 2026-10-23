# ReviewKnowledge33 — falsify `corpus/knowledge/claim-record-fields-r33.md` against landed gate 94a7be5a

Seat: reviewer. Attacked the knowledge entry sentence by sentence: re-read `claim_scan`,
`json_str`/`json_has_key`/`json_dup`/`json_unescape` and the `verify_claims` duplicate/malformed
paths in the landed `tools/research-gate.sh` (SHA-256 `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e`,
verified `sha256sum`), opened every cited receipt/artifact, ran the frozen counter on the landed
gate under the kill rule, and ran two probe fixtures on a scratch copy of the gate
(`/fast/scratch/hyaku/chousa-r33/w2/ReviewKnowledge33/tools/research-gate.sh`, sha256
`94a7be5a…8506e` identical to the lane file). No installs, no network, no lane writes.

## Kill-rule counter runs (landed gate, fresh seeds)

- `python3 corpus/evidence/round33/c1-count-v2.py --gate tools/research-gate.sh --seed 7601
  --receipt .ufo/waves/round-33/w2/ReviewKnowledge33/c1v2-s7601.json` (lane root, `C1_TMP`/`TMPDIR`
  in my scratch) → exit 0, `TOPLEVEL_FIELD_MATCH=156/156`, receipt `gate_sha256=94a7be5a…`,
  `matched=156, total=156, gate_rc=1`.
- Same command, seed 7602 → exit 0, `TOPLEVEL_FIELD_MATCH=156/156`, receipt `c1v2-s7602.json`,
  `matched=156`. No lower run observed (P1 v2 not disturbed).

## Findings

### F1 (moderate) — the entry calls the *candidate* gate "landed"
`corpus/knowledge/claim-record-fields-r33.md:4` says "gate behaviour measured on gate SHA-256
`52f07c74…1b2a`" and `:58` calls that hash "landed gate `52f07c74…`". `git rev-list` shows
`52f07c74` is the blob at the *candidate* commit `eb179ec3844f`; the landed gate at tip `0fb300b`
is `94a7be5a…` (`git show 0fb300b5:tools/research-gate.sh | sha256sum` = `94a7be5a…`). The cited
receipts `.ufo/waves/round-33/measure/candidate/c1v2-s335{1,2}.json` record
`gate_sha256=52f07c74…` — i.e. the numbers are right but the word "landed" names bytes that are
not the landed bytes. Landed-gate evidence exists uncited:
`.ufo/waves/round-33/measure/integrated/c1v2-s337{1,2}.json` (`gate_sha256=94a7be5a…`, 156/156).
This is exactly the QUALITY-15 shape (measured bytes must equal the cited commit): the sentence
is defensible only because a second measurement happened to land.

### F2 (moderate) — `claim_scan` accepts malformed scalars; "fail closed on non-objects" overclaimed
Entry `:28-30` asserts a line "that is not one well-formed object" reads `CLAIM id=line<N> …
observed=invalid`, and `:66` claims "the reader refuses" malformed lines. Probe
(`probe-claims.jsonl` → `probe-malformed.out`, exit 1):
`{"id":"P1",…,"junk":tru}` → `CLAIM id=P1 … observed=supported … verdict=match`;
`{"id":"P6",…,"junk":'x'}` → `supported`; `{"id":"P7",…,"junk":nul}` → `supported`.
All three are not JSON (python3 `json.loads` rejects each: "Expecting value"/"Expecting ','
delimiter"). `claim_scan`'s scalar branch (`tools/research-gate.sh:1217-1226`) accepts any
nonempty run up to a delimiter; string bodies also admit unescaped control bytes.
claims.md v2 asks the candidate to "fail closed" on non-objects (`:139-140`); on malformed
scalars it does not. No counter class draws these — C1/P1 is undisturbed — but the contract
adjacent sentence and the entry's "refuses them" are false on this input class.

### F3 (minor) — duplicated-id display rule wrong for ≥3 occurrences
Entry `:25-26`: a duplicated `id` "prints that id only when both values are identical". Probe line
`{"id":"a","id":"a","id":"b",…}` → `CLAIM id=a … observed=invalid` (probe-malformed.out line 4):
the gate compares only occurrence 1 vs occurrence 2 (`JSON_DUPSTR` keeps only the second value,
`research-gate.sh:1231-1237,1636-1639`), so with three differing-set values the id still prints.
The honest rule is "first two decoded values identical (and the second a string)". Not counted
(contract v2 counts `id` identical only) but the entry states it unconditionally.

## Verified-held sentences (probed or receipt-backed)

- Nested member ignored incl. arrays/2-level containers and same-name decoys: `claim_scan`
  collects depth-1 members only (`research-gate.sh:1190-1216`); probe `{"meta":{"line":"9"}}` →
  `supported` at real line (P5). ✓ `:19-22,49-50`.
- Every read key duplicated at top level → `CLAIM_RECORD_INVALID … duplicate top-level key <k>`
  fixed-order first hit; even agreeing values invalid: `:1622-1645`, probes E1, `id`/"a"/1. ✓
  `:23-26` (except the F3 edge).
- `id` identical-dup prints the id; differing/non-string second value → `id=line<N>`:
  probe lines 4, claims2 lines 1-2 → `line1`/`line2`. ✓.
- String content never structure (confusers `\\"`, trailing `\\`, fake `"line":"3"` inside a
  string): counter S1/S2 classes 12/12 + 6/6 on all runs. ✓ `:27-29`.
- Escaped key `l\u0069ne`/`i\u0064` is not the plain key (raw-compare, `:1161-1162`): probe E3 →
  `supported` at line:1, E4 `i\u0064` → "missing id". ✓ `:52-53`.
- Counts: 156 records / 15 classes (counter docstring + per-class output); base `f4731885` 60/156
  (rescore summary `pristine-gate`/`do-nothing` lines, seeds 3341-3342; claims.md v2 before run
  seed 3311); best non-oracle control 142/156 (`CtlC1DupPolicy c-differ-only`, both seeds);
  oracle 156/156 twice. ✓ `:57-61`. Note: only *receipts*, not the seed, name the 60/156 runs —
  entry omits the receipt pointer for the base number (borderline Q9/37).
- RFC 8259 quotes verbatim: line 322 "The names within an object SHOULD be unique."; line 333
  "…Many implementations report the last name/value pair" (ends "only." l.334; "Other
  implementations report an error or fail to parse" l.334-335) — confirmed in
  `/fast/scratch/hyaku/chousa-r33/L1/reopen/rfc8259.txt` and `reopen-L1.txt`. Python "ignores all
  but the last name-value pair for a given name" confirmed in `json.norm.txt` and by
  `json.loads('{"a":1,"a":2}')` → `{'a': 2}`. ✓ `:38-45`.
- Cost: `ExecParserCost33.md` table walk-C 1.670 ms @500 B, 3.473 s @64 KiB (entry says ~1.7 ms /
  ~3.5 s); superlinear, `${s:i:1}` O(len). Base `json_unescape` already per-char (`git show
  2b9cc73:tools/research-gate.sh` `json_unescape` loop). ✓ `:68-71`.
- Not-claimed bullets accurate except F2 ("the reader refuses them" wrong). ✓ `:65-67` rest.
- Round-31 measurement `{"meta":{"line":"9"}}`→`mislocated`: `c1-count-v3.py:16-22` corroborates
  (landed r31 gate 0bc318b3). D4 routing confirmed `lessons/round-32-verifier-spotcheck.md` D4 row
  (~line 166). ✓ `:14-15`.

## QUALITY admission criteria

- Q6 metadata header: source/verified-at/recheck all present; recheck gives cwd ("lane root:") and
  a runnable command (`--gate`/`--seed`/`--receipt` all optional, c1-count-v2.py:338-341) — Q13 OK.
- Q7 scope: S062/S063 tier A, `mined`, `used-by` names this entry (SOURCES.md:72-73); scope
  disclaimers ("not this lane's reader contract") respected. ✓
- Q8 support states: `:44-45` explicitly says neither source mandates the design. ✓
- Q10: `grep -nE '\$\{[A-Z_]+\}|TODO|TBD|LANE_HASH'` → no hits. Q23: `prose-check.py` → 0 hits, exit 0.
- Q15/Q9: **fails in spirit** — see F1 ("landed" names non-landed bytes).

## Verdict

**HOLDS** on the counted C1 v2 predicate (two fresh-seed receipts, 156/156, exit 0, DRIFT path).
The knowledge entry is mostly accurate but ships three defects: F1 mislabels the candidate gate as
landed (evidence exists for the real landed gate, uncited), F2 overclaims fail-closed behaviour —
the reader accepts non-JSON scalar values and lets them ride to `observed=supported` (contract
exposure, outside all 15 counter classes), and F3 mis-states the duplicated-id display rule for
≥3 occurrences. Residual risk: claim_scan is a JSON-shaped scanner, not a JSON validator — any
future claim leaning on "one well-formed object" inherits that gap; the fix is a scalar/string
validity check in `claim_scan` or narrower entry wording.
