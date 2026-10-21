# IntegTokenCost — falsify report (round 27, attempt 1)

Item attacked: integration invariant **TokenCost** for the new S-id iteration —
"streaming ASCII token extraction, not recursive prefix matching or negated-class
substitution; preserve each genuine occurrence, first-row policy and exact used-by."

Target: `dd72641e574679c4f7882dd43de072b4c8892d6f` (lane master).
Gate under test: `tools/research-gate.sh` sha256
`ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (verified in lane
and in sandbox; `git show dd72641e…:tools/research-gate.sh | sha256sum` equal).
Base: `64eec5d4…`, gate sha256 `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`
(matches `git show 64eec5d4…:tools/research-gate.sh | sha256sum`).
Sandbox: `/tmp/chousa-r27-falsify-IntegTokenCost` (lane and base extracted via
`git archive`; synthetic fixtures only; no lane file edited; no tool installs — GNU
`time` absent, bash `time`/`date +%s%N` used).

## Verdict

**HOLDS** on the invariant's four stated clauses. **The item's cost predicate is
REFUTED**: the landed iteration introduces a new 12–34× per-source time regression on
token-dense inputs, while removing a worse base quadratic. These two facts are
reported separately, not netted.

Clause by clause:
- Streaming ASCII token extraction, no recursive prefix matching — HOLDS. The base
  `source_scan=${source_scan#*"$source_match"}` loop and `source_id_re` are gone
  (`grep -n 'source_match\|source_id_re\|source_scan' tools/research-gate.sh` → none);
  the new scan is `printf '%s\n' "$source_value" | LC_ALL=C grep -oE '[[:alnum:]_]+'`
  consumed by `while IFS= read -r source_id` (target:2529). No negated class in it.
- Each genuine occurrence preserved — HOLDS (counts, fuzz, control-byte fixtures).
- First-row policy — HOLDS (duplicate registry rows and second tables).
- Exact used-by — HOLDS (`./` strip, comma lists, near-miss refusal).
- "No new time regression" (the reading this item is named for) — **FALSE** for
  token-dense sources; true for id-dense sources (see table).

## Evidence

### 1. Occurrence identity (exact counts, base vs landed)

Isolated harness evals only `metadata_registry_check_source` from each tree
(`/tmp/chousa-r27-falsify-IntegTokenCost/harness.sh`), used-by deliberately mismatched
so every detected occurrence emits once:

```
base=8193 target=8193   bodies/sids4.txt    (4 MiB, 8192×S001 + 1 injected)
base=4097 target=4097   bodies/sids4b.txt   (4 MiB, 4096×S001 + 1 injected)
base=1    target=1      prose1/2/4, dense1/4, onetok4 (4 MiB single token)
```
rc=0 each; diff of the emitted sequences empty (both count and quiet modes).

86-case mixed-ASCII fuzz (`fuzz/`, ids glued to letters/underscore/digits, single and
shared delimiters, glob metacharacters, CRLF, tabs, 3–20 digit ids, `S000`, `s001`,
empty/whitespace, 40 random draws):

```
LC_ALL=C bash fuzz.sh tools/research-gate.sh fuzz > fuzz-target-c.out   # rc 0
LC_ALL=C bash fuzz.sh base/tools/research-gate.sh fuzz > fuzz-base-c.out # rc 0
diff -q … → identical (86 cases)
```
Binary/control-byte fixtures (`fuzzb/`: `\xff`, `\x80`, truncated `\xc3`, surrogate
`\xed\xa0\x80`, VT/FF, CR, ESC adjacent to ids): base = target = mutant, identical.
The gate never feeds NUL through this path (entry read refuses NUL), so that is moot.

Locale note (harness artifact only): without `LC_ALL=C`, base and landed differ on
`caféS042` / `日本語S043` (base: "no S-id"; landed: S042/S043). In situ this cannot
happen: `verify_metadata` sets `local LC_ALL=C` in both trees (base:2539, target:2564)
before the sole call site (target:2720). End-to-end `caféS042` gives the same finding
in both gates. The landed function-local `LC_ALL=C` (target:2502) is redundant with
its only caller — harmless, makes the function caller-independent.

### 2. First-row policy and exact used-by (end-to-end, both gates identical)

`verify-metadata ENTRY --root W --registry reg` rc=1 (DRIFT) both gates:
- `S020` queued row first, mined second → `META_SOURCE_NOT_MINED` (first row wins).
- `S021` mined first, queued second → CLEAN (second row ignored).
- second table after a plain-text break re-declaring `S031` queued → ignored.
- used-by `./corpus/knowledge/ub.md` → matched; ` corpus/knowledge/ub.md , other.md`
  → matched; `corpus/knowledge/ub.md.bak` → `META_SOURCE_USEDBY_MISSING` (exact, no
  prefix match).
- duplicate source occurrence `S999 S999` → two findings in both gates.
- semantic matrix `S001,S002`, `xS005`, `S006a`, `S007_S008`, `S009-`, `S0010`,
  `S0011x`, `(S014)`, `S015.`, `S013 S013` → identical findings both gates.

### 3. Cost (min-of-3 wall, isolated function, quiet path, host loaded)

| source body | base (recursive) | landed (token loop) | mutant `grep -owE` |
|---|---|---|---|
| prose 1 MiB | 60 ms | 748 ms | 38 ms |
| prose 2 MiB | 132 ms | 1463 ms | 86 ms |
| prose 4 MiB | 239 ms | 2877 ms | 137 ms |
| dense 1 MiB (`a ` tokens) | 83 ms | 1994 ms | 39 ms |
| dense 4 MiB (2,097,152 tokens) | 287 ms | 9873 ms | 141 ms |
| ids 4 MiB, 8193×S001 | >120 s (timeout 124; unattended 132 s / 168 s) | 701 ms | 299 ms |
| one 4 MiB token | 136 ms* | 391 ms | — |

`*` earlier run; base single-pass scan. Landed cost is linear in tokens (~4–5 µs/token;
prose 748→1463→2877 ms), so the 8 MiB cap extrapolates to ~18–20 s for a dense entry and
~5–6 s for prose density (extrapolation, not measured). Base is quadratic in occurrence
count (4096 ids 70.8 s → 8192 ids >120 s).

End-to-end `verify-metadata … --registry` (min of 3; base vs landed):

| entry | base | landed | ratio |
|---|---|---|---|
| 4 KiB | 24 ms | 30 ms | 1.25× |
| 64 KiB | 44 ms | 85 ms | 1.93× |
| 1 MiB | 432 ms | 1096 ms | 2.54× |
| 2 MiB | 943 ms | 2173 ms | 2.30× |
| 4 MiB | 2413–3232 ms | 4898–5192 ms | 1.6–2.2× |

Raw commands: `env -u CHOUSA_RECORD -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0
CHOUSA_ROOT=$W/root bash <gate> verify-metadata <entry> --root $W/root --registry
$W/root/registry.md` (rc=1, same finding in both gates throughout).

### 4. Mutation evidence

- **Revert the targeted fix** (base copy, recursive scan): semantics stay equal under
  the gate's in-situ `LC_ALL=C` (all counts/fuzz identical), but the cost control fails
  — 4 MiB/8193 ids >120 s vs landed 0.70 s. So the landed change is a cost repair, not
  a semantic repair.
- **Forward mutant** `grep -oE '[[:alnum:]_]+'` → `grep -owE 'S[0-9]{3,}'` (one flag):
  86-case fuzz and binary fuzz identical to landed; occurrence counts 1/1/1/1/8193/…;
  end-to-end matrix (sem, dup, fr1, fr2, ub, utf) byte-equal findings; cost
  prose4 137 ms, dense4 141 ms, sids4 299 ms, and end-to-end ml-4 2453 ms vs base
  2413 ms / landed 4898 ms; small64 39 ms vs base 39 ms / landed 84 ms.
- **Break mutant** `grep -oE 'S[0-9]{3,}'` (no word boundary): fuzz control fails on
  `xS001`, `S001x`, `S001_S002` (invented occurrences). The equality control is
  therefore sensitive, not vacuous.
- Second forward form keeping literal token extraction:
  `… | LC_ALL=C grep -oE '[[:alnum:]_]+' | LC_ALL=C grep -xE 'S[0-9]{3,}'`
  measured 41 ms (prose4), 94 ms (dense4), 35 ms (sids4) pipeline-only.

## Minimal counterexample (cost)

Same input, same result, different cost — `bodies/dense4.txt` (4 MiB, `a ` repeated;
one injected `S001`): landed `metadata_registry_check_source` 9.87 s vs base 0.29 s
(34×), each returning exactly one occurrence. Conversely `bodies/sids4.txt` (4 MiB,
8193 genuine occurrences): base exceeds 120 s, landed 0.70 s (171×). The repair moved
the cost from quadratic-in-occurrences to linear-in-tokens with a bash-per-token
constant; the second is bounded, the first was not.

## Risks / limits

- Host is heavily loaded (bash `user` 3–4× `real` observed); all comparisons are
  min-of-3 wall on the same host, ratios stable, absolutes ±20–30%. The 8 MiB figures
  are extrapolations from measured linearity.
- Only `verify-metadata --registry` (the sole call site) exercised; no full selftest,
  no regression script, no base behavioural rerun (out of bounds / owned by L1).
- No NUL, network, host-secret, process, mount or debugger probes; fixtures are
  synthetic files under `/tmp/chousa-r27-falsify-IntegTokenCost`.
- "Streaming" is asserted from mechanism (grep `-o` into a pipe, `read` per line) and
  memory behaviour on a 4 MiB single token; no memory profiling.

## Author-lane advice (no integration performed)

1. Keep the repair: it removes a reproducible >120 s quadratic on a legal 4 MiB /
   8193-occurrence source; the base cannot be the cost reference for id-dense inputs.
2. Remove the new common-case regression with one filter before the bash loop, either
   - literal token extraction: append `| LC_ALL=C grep -xE 'S[0-9]{3,}'` (still
     streaming token extraction, no negated class); or
   - minimal diff: `grep -oE '[[:alnum:]_]+'` → `grep -owE 'S[0-9]{3,}'` (under
     `LC_ALL=C`, `-w` equals whole-token equality; `-o` does not consume boundary
     characters, so `S001,S002` still yields both).
   Both were verified semantically identical to the landed code (86+10 fuzz cases,
   occurrence counts, six end-to-end fixtures) and restore base-or-better cost
   (dense4 9.87 s → 0.14 s; ml-4 4.90 s → 2.45 s). Keep the `[[ … =~ ^S[0-9]{3,}$ ]]`
   guard as belt-and-braces.
3. Optional simplification: the function-local `LC_ALL=C` at target:2502 duplicates
   the only caller's `local LC_ALL=C`; harmless, keep if caller-independence is wanted.
4. If no edit is taken, record the residual explicitly: ≤~20 s per 8 MiB dense entry
   in registry mode (linear in tokens), against a base that is unbounded in occurrences.
