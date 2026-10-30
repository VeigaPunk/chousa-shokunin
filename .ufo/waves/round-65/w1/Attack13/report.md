# Attack13 — C1 frozen case `short-digest`: nearby-bypass attack

Seat: Attack13 (critic, lane chousa round65). Freeze: `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` (verified via `git rev-parse HEAD`).
Scope: attack the C1 frozen case `short-digest`; construct nearby forged/malformed receipts outside that exact case; state whether the frozen counter detects them. Bounded isolated probes only; frozen bytes unaltered (all probes read frozen files; mutants lived only in scratch).

## Frozen counter branch (corpus/evidence/round65/c1-count.py)

- Fixed 20-case list; each case runs `<python> -B <tool> --receipt <case>.txt --root <lane> --revision d6ed8155...` and requires exact `rc` plus token: `rc=0 → stdout.strip()=="RECEIPT_PIN=PASS"`; `rc=1 → stdout.startswith("RECEIPT_PIN=FAIL ")`. Case outcomes: 3 valid-shape (rc 0), 17 malformed (rc 1).
- `short-digest` = valid receipt with the 64-hex SHA256 replaced by `h[:16]` (48 chars truncated). Expected rc 1. It guards exactly the 16-char truncation shape.

## Reference validator contract (controls/ref-receipt-pin.py)

Exactly `REVISION=<40 lower hex>` / `EXIT=<0..255>` / `SHA256=<64 lower hex> <repo-relative POSIX path>` / empty separator / nonempty body; single occurrence, fixed order; revision must equal `--revision`; digest binds `git cat-file blob <rev>:<path>` (no working-tree hashing). Regexes are exact-width: `[0-9a-f]{40}`, `(?:0|[1-9][0-9]{0,2})`, `([0-9a-f]{64})`.

## Nearby forged/malformed receipts constructed (outside the frozen 16-char case)

All derived from the counter's own valid receipt (same base blob `SKILL.md@d6ed8155...`, true digest `4355e16a...08ce1a`). Reference-validator results (probe: `attack13-ref-probe.log`):

| variant | mutation vs valid | ref rc | ref verdict |
|---|---|---|---|
| digest-63 | true digest minus last char (length 63) | 1 | FAIL digest header |
| digest-65 | true digest plus `a` (length 65) | 1 | FAIL digest header |
| digest-60 | truncated to 60 chars | 1 | FAIL digest header |
| digest-16-upper | `h[:16].upper()` — short+upper combo | 1 | FAIL digest header |
| digest-empty | `SHA256= SKILL.md` | 1 | FAIL digest header |
| digest-nonhex64 | `z`*64, right length wrong alphabet | 1 | FAIL digest header |
| digest-internal-space | `h[:32]+' '+h[32:]` | 1 | FAIL digest header |
| digest-0x-prefix | `0x`+h (66 chars) | 1 | FAIL digest header |
| digest-ok-path-trailing-space | valid 64-hex, path `SKILL.md ` | 1 | FAIL blob/digest |
| digest-ok-path-double-space | valid 64-hex, two spaces before path | 1 | FAIL blob/digest |
| frozen-short-digest-16 | the frozen case itself | 1 | FAIL digest header |

The reference validator holds the full format contract against every nearby variant — no reference bypass found.

## Does the frozen counter detect the nearby bypass? — No (outside the exact case)

- **Baseline replication**: frozen counter vs reference → `CASES=20/20 C1=PASS` (matches frozen `c1-positive.txt`).
- **Nearby-bypass mutant** (`attack13-mutant-lenient-digest.py`, scratch-only): identical to the reference except digest regex `[0-9a-f]{60,64}` and prefix comparison `real[:len(m[1])]==m[1]`. It **accepts digest-63 and digest-60 receipts (rc=0, RECEIPT_PIN=PASS)** — a truncated-but-mostly-correct digest is admitted. Run under the frozen counter it still scores **20/20 C1=PASS**: no frozen case exercises digest lengths 60–64 or 65; the only length-adjacent frozen cases are exactly-16 (`short-digest`) and exactly-64 (`wrong-digest`, `upper-digest`).
- **Contrast** (`attack13-mutant-prefix-any.py`): a naive prefix-match mutant accepting any 1..64-char prefix IS caught — frozen counter returns `CASES=19/20 C1=FAIL` with exactly `CASE short-digest FAIL rc=0`. So the frozen case does guard its own exact mutation, and detection stops at the case boundary.

Verdict: the frozen counter detects the exact frozen `short-digest` case and misses structurally nearby forgeries outside the 20-case list. This is a **coverage boundary of the fixed-case oracle, not a false claim**: claims.md freezes the predicate as "all frozen receipt-consistency cases match their exact exit and token" and disclaims "general parser safety". The counter is not a mutation-testing oracle; no hidden regression, no duplicate authority, no identity/provenance break.

## Impacted axes

- **C1 operability**: 20/20 predicate mechanism unaffected; impact is informational coverage only (nearby length mutations 60–65 unexercised). No score effect; the target validator is expected to enforce the full contract like the reference, which rejects all variants.
- C2 untouched.

## Smallest safe correction

None to frozen bytes (freeze + kill rule forbids counter changes; the predicate is exactly the 20 frozen cases). For L1 integration notes only: (a) accept `tools/receipt-pin.py` only if it enforces the full format contract as the reference does — in particular exactly-64 lowercase-hex digest and exact-width regexes; (b) record as a documented out-of-scope coverage boundary that digest lengths 60–65 adjacent to the frozen 16/64 cases are not counter-exercised. A mutant that accepts 60–64-char prefixes would pass C1 while admitting forged receipts; this is a known, bounded, interface-coverage tradeoff — the canonical judge should reject any request to expand the frozen case list this round, and reject any target that relaxes digest width below the reference contract.

## Method & hygiene

- Bounded isolated probes: 12 receipt variants; 3 frozen-counter runs (reference, lenient mutant, prefix mutant); 7 direct mutant probes. All local, read-only git (`-C`, `cat-file`, `rev-parse`, `status`); no network, no mutations, no installs (none needed), pacman untouched.
- Frozen files read-only; mutants and receipts existed only under `/fast/scratch/hyaku/chousa-r65/Attack13/`, deleted after evidence copy. TMPDIR confined to scratch; no /tmp evidence.
- Lane tree at freeze with pre-existing seat/L1 working changes unrelated to this seat; this seat wrote only `.ufo/waves/round-65/w1/Attack13/`.

Evidence in this folder: `attack13-ref-probe.log`, `attack13-counter-probe.log`, `attack13-contrast-probe.log`, `attack13-mutant-lenient-digest.py`, `attack13-mutant-prefix-any.py`, `attack13-variant-receipts.tar.gz` (12 receipts).
