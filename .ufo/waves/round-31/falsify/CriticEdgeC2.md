# CriticEdgeC2 — C2 on inputs the frozen counter does not generate (round 31, wave 2 FALSIFY)

Seat: leaf critic. Target: landed C2 (`6d0ae19f`), gate `tools/research-gate.sh` SHA-256
`c23d7537e03482f2844c9cbc43fc055d3d08d564857a89529b6f13473403823c` (lane tip byte-identical to a
clone at `ee1024fd`; clone gate SHA equals the lane gate SHA). Scratch root
`/fast/scratch/hyaku/chousa-r31/w2/CriticEdgeC2/`, run as uid 1000 (one explicit root probe).
Frozen counter never edited. No network used. No installs needed.

Method: hand-built fixtures the counter cannot emit (its files are `src/%016x.md`, text-only, flat
string pins), run through `bash <gate> verify-claims <claims.jsonl> --root .` with every `CHOUSA_*`
variable unset. Counter baseline re-run as a control.

## Case table (landed gate; edge fixture exit 1, `RESEARCH_GATE: DRIFT`)

| # | input (beyond the counter's shape) | observed | claims.md C2 contract | result |
|---|---|---|---|---|
| E01 | empty file, pin = SHA-256 of empty bytes | `unsupported` + `CLAIM_SPAN_NOT_FOUND` | §3 equal → existing span verdict | holds |
| E02 | file `alpha\0beta…`, pin = SHA-256 of raw bytes, span `alphabeta` (exists only after NUL strip) | `supported` at `line:1` | §3 formally | observation F |
| E03 | same file, pin = hash of NUL-stripped bytes | `stale` + `CLAIM_SOURCE_REVISION_MISMATCH` | §2 | holds |
| E04 | 8 388 609 bytes (**> cap**) + correct pin | `refused` (`CLAIM_SOURCE_READ_TOO_LARGE`), **no** revision finding | §4 refused never read/hashed | holds |
| E05 | exactly 8 388 608 bytes + correct pin | `supported` (hashed) | cap is strict-`>` ("inclusive boundary") | holds |
| E06 | `https://example.invalid/research.md` + pin | `refused` (`CLAIM_SOURCE_EXTERNAL`, crit), no revision finding | §4 | holds |
| E07 | symlink → **in-root** file + pin of target bytes | `supported` | §4 (not a refusal) | premise wrong: symlinks are followed |
| E08 | symlink → out-of-root file + pin | `refused` (`CLAIM_SOURCE_OUT_OF_CORPUS`) | §4 | holds |
| E09 | hardlink `nlink=2` + correct pin | `refused` (`CLAIM_SOURCE_MULTILINKED`) | §4 | holds |
| E10 | `chmod 000` + correct pin (uid 1000) | `refused` ("not a readable regular file") | never a match | holds (see U1) |
| E11–E14 | pin as JSON number / `null` / `true` / `false` | `invalid` (`CLAIM_RECORD_INVALID`) | §1 present non-string → invalid | holds |
| E15 | **duplicate** `"sha256"` (first = matching) | `supported` | §1 silent | divergence D-D |
| E16 | duplicate `"sha256"` (first = UPPERCASE, second = matching) | `invalid` | §1 silent | divergence D-D (Python json would say the pin matches) |
| E17 | duplicate `"sha256"` (first = stale, second = matching) | `stale` | §1 silent | divergence D-D (Python json → supported) |
| E18 | pin = `"<64hex>\n"` (65-char value) | **`supported`** (match) | §1 *any other value → invalid* | **VIOLATION D-A** |
| E19 | pin = `"<64hex>\n\n"` | **`supported`** | §1 | **VIOLATION D-A** |
| E20 | pin = `"<64hex> "` (trailing space) | `invalid` | §1 | holds (control) |
| E21 | pin = `"<64hex>\r"` | `invalid` | §1 | holds (control) |
| E22 | duplicate `"id"` key | reports the **first** id | — | divergence D-D class |
| E23 | `"line":"7"` (mislocated) **+ stale** `"sha256"` | `stale`, **no** `CLAIM_LINE_MISMATCH` | C1 §3 vs C2 §2 | ambiguity D-E |
| E24 | `"line":"7"` + matching pin | `mislocated` + `CLAIM_LINE_MISMATCH` | C1 §3 | holds |
| E25 | directory as source + pin | `refused` | §4 | holds |
| E26 | source filename contains a **newline**, pin correct | **`stale`, `actual=unreadable`** (+ `CLAIM_SOURCE_REVISION_MISMATCH`) | §2 different→stale; §3 equal→span verdict | **VIOLATION D-B** |
| E27 | source filename contains a **backslash**, pin correct | **`stale`, `actual=unreadable`** | §2/§3 | **VIOLATION D-B** |
| E28 | filename contains a space, pin correct | `supported` | §3 | holds (control) |

Pin-value probes (second fixture, exit 1, 11 claims): P1 `"<hex>\n"` → `supported`; P2 `"<hex>\n\n"`
→ `supported`; P3 `"\u0000<hex>"` → `supported` (**all D-A**); P4 `"<hex>\n "` → `invalid`;
P5 object → `invalid`; P6 array → `invalid`; P7 uppercase → `invalid`; P8 65 hex → `invalid`;
P9 63 hex → `invalid`; P10 leading space → `invalid`; P11 `"\u0061"+63hex` → `stale` (decoded value is
valid hex and differs — correct). Leading-`\n`, CRLF, tab and mid-string newline pins → `invalid`.

Key-detection probes: a span containing escaped `\"sha256\":\"…\"` does **not** register a pin
(escaped quotes never form `"sha256"`) — good. But a **nested object** does: S2
`{"…","meta":{"sha256":"<wrong>"}}` and S3 `{"a":{"b":{"sha256":"<wrong>"}}}` — records with **no
top-level pin** — are reported `stale` with a `CLAIM_SOURCE_REVISION_MISMATCH` naming the claim
(**VIOLATION D-C**). C1 shares the helper: `{"meta":{"line":"9"}}` → `mislocated` +
`CLAIM_LINE_MISMATCH` (L1); duplicate `"line"` keys `"9","1"` → bound to `9` (first wins, L2).

U1 (environment caveat): the same `chmod 000` file with a correct pin is **`supported`/match when the
gate runs as root** (`sudo -n`) — the "never a match" property is user-dependent (`-r` is true for
root), so E10's result holds only for the lane's own user.

## Violations with repro

**D-A — a pin that is not exactly 64 lowercase hex is silently coerced into a valid matching pin.**
Gate line 1448: `sha_pin=$(json_unescape "$(json_str "$line" sha256)")` — command substitution strips
trailing newlines and bash drops NUL bytes, so the value validated at line 1461 and compared at 1508
is not the record's value. A 65-char value must be `observed=invalid` (§1) but reports
`observed=supported, verdict=match`.
Repro: `cd /fast/scratch/hyaku/chousa-r31/w2/CriticEdgeC2/p2 && env -u CHOUSA_ROOT timeout 300 bash
../clone/tools/research-gate.sh verify-claims claims.jsonl --root .` → exit 1;
`CLAIM id=P1_trailing_nl … observed=supported … verdict=match`. Counter-blind: I1 sub-variants are
upper/short/long/prefixed/nonhex/**leading**-space; no trailing-whitespace/NUL variant.

**D-B — a correct pin on a source whose filename contains a newline or backslash is reported stale.**
Gate line 1504: `sha256sum -- "$path" | cut -d' ' -f1`. GNU coreutils prefixes the output with `\` and
escapes the name when it contains `\` or a newline, so `cut` yields `\b4034355…` (65 chars), fails
`^[0-9a-f]{64}$`, becomes `sha_actual=unreadable`, and the claim is reported `stale` although the pin
**equals** the file's SHA-256. The emitted finding (`actual=unreadable`) is a false statement: the file
was readable and its hash is computable (`sha256sum < "$path"` returns
`b4034355043e7aecf1898cd9bde724dfa95ba256e3ee7244e1f7def448454d7f`).
Repro: edge fixture run above → exit 1;
`CLAIM id=E27_bs_filename … observed=stale …` and
`FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=warn surface=claims obs=id=E27_bs_filename
pin=b4034355043e actual=unreadable`. Counter-blind: fixture names are `src/%016x.md`.

**D-C — a nested `"sha256"` is read as the record's own pin.** `json_has_key`/`json_str` are flat
regexes over the raw line (gate 1094/1082); a key inside a nested object matches. A record with no
pin is therefore revision-checked and can be flagged drifted — contradicting §4 ("`"sha256"` absent:
behaviour unchanged") and §2's "printed exactly for the stale claims".
Repro: `cd …/p5 && env -u CHOUSA_ROOT timeout 300 bash ../clone/tools/research-gate.sh
verify-claims claims.jsonl --root .` → `CLAIM id=S2_nested_meta … observed=stale …` plus
`FINDING CLAIM_SOURCE_REVISION_MISMATCH … obs=id=S2_nested_meta`. Shared with C1 (L1 above).

**D-D — duplicate keys: the gate is first-wins, standard JSON is last-wins.** One record can carry
two pins and the gate and any JSON reader disagree (`{"sha256":"A","sha256":"B"}`: gate `A`, Python
`json.loads` `B`). E16/E17 therefore reach the opposite verdict to a JSON-faithful checker.
Counter-blind: the counter emits each record via `json.dumps` (unique keys). Contract silent — an
ambiguity, not a proven §-violation, but it is a second authority for the same field.

**D-E (ambiguity, not proven violation).** A record carrying both fields with a stale pin suppresses
C1's `CLAIM_LINE_MISMATCH` (E23 vs E24). C2 §2 says stale is decided "before and regardless of the
span check"; C1 §3 says the line finding is printed "exactly for the claims whose truth is
mislocated". Neither frozen counter generates the combination (design v2 separability), so P1/P2
cannot see it. [INFERENCE] the contracts do not resolve precedence for a combined record.

**F (inherited, not a C2 regression).** The pin hashes raw bytes (`sha256sum`) while the span is
matched on a NUL-stripped copy (`hay=$(cat -- "$path"; printf x)`, gate 1516; bash warns
"ignored null byte in input"). E02 is `supported` for a span absent from the pinned bytes. The span
half is base behaviour (an unmodified base-gate control `be7b8d8d` reproduces it on the same file), but
it makes the frozen SKILL.md text "the SHA-256 of the exact source bytes read" literally false for
NUL-containing sources.

## Holds (positive controls)

Refusals precede hashing for over-cap (E04), external URL (E06), out-of-root resolution (E08),
multilink (E09), unreadable (E10) and non-regular (E25) sources — none emitted a revision finding.
Non-string pins are invalid (§1). Empty-file pin compares correctly. Cap boundary is strict-`>`.
Duplicated-`id` reporting does not double-count (the counter's dup rule is across CLAIM lines).

## Predicate status (reported, not judged)

Frozen P2 run on the landed gate: `python3 corpus/evidence/round31/c2-count.py --seed 777001
--gate tools/research-gate.sh --receipt <falsify dir>` → `REVISION_BINDING_MATCH=120/120`,
`predicate_holds=true`. So **P2 holds while three §-level contract violations live on inputs the
counter cannot generate**. These are fixable defects, not tradeoffs: each correction below was run and
keeps `120/120`.

## Smallest safe corrections (all verified on scratch copies, lane untouched)

1. D-B: gate 1504 → `sha256sum < "$path" 2>/dev/null | cut -d' ' -f1`. Verified: E26/E27 →
   `supported`; C2 counter seed 424242 → `120/120`; C1 counter seed 424242 → `120/120`; `--selftest`
   identical to an unmodified control at the same path (1/228, the `claims-lane-fallback` case, which
   fails for any gate copied outside the lane because `LANE_ROOT` is the script's parent).
2. D-A: gate 1448 → `raw_sha=$(json_str "$line" sha256)`; reject a raw body containing a `\u0000`
   escape; `sha_pin=$(json_unescape "$raw_sha"; printf x); sha_pin=${sha_pin%x}`. Verified:
   E18/E19/P1/P2/P3 → `invalid`; P11 still `stale` (decoded-value semantics kept); C2 counter seed
   99001 → `120/120`, `predicate_holds=true`; selftest parity with the control.
3. D-C: match `sha256`/`line` only at brace-depth 0 (or document flat-records-only and reject nested
   objects). No counter covers this; shared fix with C1.
4. D-D: treat >1 `"sha256"` (and >1 `"id"`) key in a record as `invalid` — one occurrence count, and
   the gate stops disagreeing with every standard JSON reader.

## Impacted axes

- **coverage** — the frozen C2 fixture omits: trailing-newline/NUL pin values (its invalid class has a
  *leading* space only), source filenames coreutils escapes, nested keys and duplicate keys. P2's
  120/120 therefore carries no evidence about the classes above.
- **operability** — checklist item 1's stated outcome ("a changed source reads `stale`") is inverted
  for D-B: an **unchanged** source reads `stale`, with a false drift finding.

## Limits

- Scratch-only experiments; lane untouched except this report and the artifacts in
  `.ufo/waves/round-31/falsify/CriticEdgeC2/`. Mutants run only as copies in `/fast/scratch`.
- Gate run as uid 1000 except the U1 root probe; the unreadable-file result is user-dependent.
- Counters and predicates were not edited; no counter re-scaling was attempted.
- `--selftest` on a copy outside the lane fails exactly one unrelated case by construction
  (`LANE_ROOT` = script parent); an unmodified copy at the same path fails the same case, so the
  mutants introduce no selftest regression.
- D-E is an ambiguity in the frozen text, not an observed wrong verdict: [INFERENCE] both readings are
  defensible and no counter exercises the combination.
