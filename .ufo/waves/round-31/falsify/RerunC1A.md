# RerunC1A — C1 counting command re-derived on the landed revision (round 31, wave 2 falsify)

**Verdict: P1 holds on the evidence I ran.** All 5 fresh seeds print
`LINE_BINDING_MATCH=120/120`; every receipt binds the committed counter and the tip gate.
Two gaps found are counter-coverage gaps (the frozen counter cannot see them), not
defects in the landed gate; one is a real (low-severity) parser hole with a named fix.

## 1. What I attacked

Re-derivation of `python3 corpus/evidence/round31/c1-count.py` on the landed revision
(`ee1024fd492144c9c7b315890fac247543c37208`), plus three adversarial probes the
assignment did not name:

* (a) the counter's own discriminating power (mutants of the tip gate),
* (b) P1's second clause ("no run of this counter on that revision prints a lower count")
  — audited across **every** round-31 receipt, not just the ones I generated,
* (c) contract surfaces the counter does not exercise (`at=`, nested JSON keys, CRLF).

## 2. The five runs (acceptance table)

Command, from the lane root, default (landed) gate, `C1_TMP` pointed at my scratch dir:

```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
C1_TMP=/fast/scratch/hyaku/chousa-r31/w2/RerunC1A timeout 900 \
  python3 corpus/evidence/round31/c1-count.py --seed <S> \
  --receipt .ufo/waves/round-31/falsify/RerunC1A/c1-seed<S>.json
```

| seed | score | exit | receipt | counter_sha256 | gate_sha256 |
|---|---|---|---|---|---|
| 202610230101 | **120/120** | 0 | `.ufo/waves/round-31/falsify/RerunC1A/c1-seed202610230101.json` | `c3aca35d…b427` | `c23d7537…823c` |
| 202610230202 | **120/120** | 0 | `…/RerunC1A/c1-seed202610230202.json` | `c3aca35d…b427` | `c23d7537…823c` |
| 202610230303 | **120/120** | 0 | `…/RerunC1A/c1-seed202610230303.json` | `c3aca35d…b427` | `c23d7537…823c` |
| 202610230404 | **120/120** | 0 | `…/RerunC1A/c1-seed202610230404.json` | `c3aca35d…b427` | `c23d7537…823c` |
| 202610230505 | **120/120** | 0 | `…/RerunC1A/c1-seed202610230505.json` | `c3aca35d…b427` | `c23d7537…823c` |

**No MISS. No run below 120/120; every receipt's `misses` list is empty (`"misses": []`),
`predicate_holds=true`, `gate_rc=1`, `gate_timed_out=false`, `elapsed_s` ≈ 2.5–2.9.**
All 12 classes scored full marks on all 5 seeds (B1/B2/B3 12/12, B4 6/6, M1–M3 12/12,
M4 8/8, M5 6/6, M6 8/8, I1 12/12, U1 8/8).

### Hash verification (the acceptance's core)

| item | committed value | receipt value | match |
|---|---|---|---|
| `c1-count.py` @ `ee1024f` | `c3aca35da30ee47edc3402daa559f43320e44a82d3a0143b5ea283ec8c49b427` | identical on all 5 | ✅ |
| `tools/research-gate.sh` @ `ee1024f` (tip gate) | `c23d7537e03482f2844c9cbc43fc055d3d08d564857a89529b6f13473403823c` | identical on all 5 | ✅ |

`git diff ee1024f -- corpus/evidence/round31/c1-count.py tools/research-gate.sh` is empty:
the worktree bytes I ran are the tip bytes. The counter hash is **identical across every
round-31 commit** (`8070f92`, `86188116`, `c17948a`, `6d0ae19`, `ee1024f`) — the counter was
never re-scaled after the data seat, so the kill rule is not engaged. The gate hash moved
`ac1315dd…` (base) → `3b5279eb…` (C1 @ `c17948a`) → `c23d7537…` (C2 @ `6d0ae19`) = tip, as declared.

## 3. P1 clause 2 audited across the whole round (not just my runs)

I parsed **every** JSON receipt under `.ufo/waves/round-31/**` and selected those whose
`counter_sha256` equals the committed counter (`c3aca35d…`): **249 receipts**, of which
**86 ran on the tip gate** (`c23d7537…`) and 4 on the C1-only gate (`3b5279eb…`).

> **tip-gate runs BELOW 120/120: NONE.**

Every one of the 86 prints 120/120. So P1's second clause ("no run of this counter on that
revision in round 31 prints a lower count") is satisfied by the receipts on disk, not merely
by my five. The disclosed 84/120 run in `claims.md` §(b) used an **uncommitted draft**
counter (different `counter_sha256`) against the then-base gate, so it neither binds the
committed counter nor runs on the landed revision; it does not breach the kill rule.

## 4. Adversarial probes (the strongest counterexamples I could build)

### 4a. Discriminating power of the frozen counter — 9 mutants of the tip gate
All mutants were built from `git show ee1024f:tools/research-gate.sh` in my scratch dir
(`/fast/scratch/hyaku/chousa-r31/w2/RerunC1A/`), never in the lane.

| mutant | counter says | caught? |
|---|---|---|
| base gate `be7b8d8d` (no C1) | 50/120 | ✅ |
| C2-only build (`measure/c2only-build.sh`) | 50/120 | ✅ (separability) |
| C1-only build (`measure/c1only-build.sh`) | 120/120 | n/a (correct build) |
| enumerate only the first occurrence | 108/120 | ✅ B2 0/12 |
| always `mislocated` when `line` present | 84/120 | ✅ |
| always `supported` when `line` present | 62/120 | ✅ |
| drop the `CLAIM_LINE_MISMATCH` emission | 62/120 | ✅ |
| emit the finding for **every** claim (stray) | 84/120 | ✅ |
| finding names the wrong `obs=id=` | 62/120 | ✅ |
| finding `severity=info` (not warn/crit) | 62/120 | ✅ |
| **`at=` replaced by `-` (everything else correct)** | **120/120** | ❌ **not caught** |

The counter is sound on the observed/finding axes (it catches all ten behavioural
mutants). **The last row is a real coverage gap**: `c1-count.py`'s `LINE_RE` reads only
`observed=`; it never inspects `at=`. The landed gate sets `at=` to the **bound**
occurrence (probe: bound later occurrence ⇒ `at=line:3`, base gate ⇒ `at=line:1`), and no
counter run can tell those apart. The frozen design does not list `at=` under "Not claimed",
and its v2 amendment carries the parenthetical "`at=` reports only the first" — a clause the
landed gate arguably reads the other way. **Impacted axis: coverage (operability unaffected).
Smallest safe correction (documentation, not code):** state in the round-31 record that
`at=` now follows the bound occurrence for `line`-bearing claims, so the v2 parenthetical
is not read as normative; and/or add `at=` to the counter's `LINE_RE` in a *future* round
(the current counter is frozen and was not touched).

### 4b. Nested JSON key → false `mislocated` / false `stale` (real, low severity)

`json_has_key` (`tools/research-gate.sh:1094`) matches `"line"[[:space:]]*:` anywhere in
the record, so a **nested** object key is read as the record's own field:

```
{"meta":{"line":"9"},"id":"n1","source":"src/s.md","span":"alpha beta gamma delta","expect":"supported"}
→ CLAIM id=n1 … observed=mislocated at=line:1
   FINDING CLAIM_LINE_MISMATCH … obs=id=n1 line=9-9
```

and the C2 twin: `{"meta":{"sha256":"<64 hex>"}, …}` ⇒ `observed=stale` +
`CLAIM_SOURCE_REVISION_MISMATCH`, on a record that carries no top-level `sha256`.
Counter-blind (fixtures have no nested objects).

This is **pre-existing gate-wide behaviour**, not a C1 regression: at base the same flat
parser already shadows top-level `span` (`{"meta":{"span":"WRONG"},…}` ⇒ `observed=unsupported`).
What C1/C2 add is that the flat parser is now reached by two *new* keys, so a false
`mislocated`/`stale` can be produced for a record with no such field.
**Impacted axis: coverage. Severity: low** — every lane claims fixture is flat
(`corpus/fixtures/*.jsonl` contain zero `"line"` keys), so no lane record is affected today.
**Smallest safe correction:** make `json_has_key` (and the `json_str` reads of `line`/`sha256`)
top-level-only — e.g. require the key to follow `{` or `,` at depth 1 — or, if the flat
convention is intentional, record it as a named limit next to the two new fields.

### 4c. Other probes — all correct, no findings
* CRLF source, single- and multi-line spans: bound correctly (`at=line:1`, `at=lines:1-2`).
* `line` present but span absent ⇒ `unsupported` (no finding), per contract item 2.
* Range grammar: `3-2`, `4-4` ⇒ invalid (`line range M<=N`); `07` ⇒ invalid (leading zero);
  `""`/non-string ⇒ invalid (`line not a JSON string`); `1.5`, `x7`, `4-`, `-4`, `4–5` ⇒ invalid.
* Huge decimal (`99999999999999999999`) is accepted as a line number and yields
  `mislocated`, not a crash (string compare, no arithmetic overflow) — the L1 fail-closed
  compare behaves as advertised.
* Env scrub: with `CHOUSA_ROOT=/nonexistent/bogus` exported, the counter still scores
  120/120 (v2 §4 holds); the gate alone does honour `CHOUSA_ROOT` (⇒ `refused`), so the
  counter's `CHOUSA_*` scrub is doing the work.
* Duplicate `id` printed twice: the counter scores it `none` (v2 §4), as designed.
* A key inside a *string* value (`"claim":"see \"line\":\"9\" here"`) is **not** seen as a
  field — the stated invariant of `json_has_key` holds for string values.

## 5. No-harm spot check (C1 landing)

| observable | expected | observed |
|---|---|---|
| `research-gate.sh --selftest` (tip, in scratch clone) | PASS, 228 cases | `RESEARCH_GATE_SELFTEST: PASS (228 cases, 0 skipped)`, exit 0, 39.6 s |
| `verify-claims corpus/fixtures/claims-r2.jsonl --root ..` | `17/17` CLEAN | `VERDICT_BEARING_CLAIMS=17/17`, `RESEARCH_GATE: CLEAN` |
| `verify-chain corpus/fixtures/chain-r3.md --root ..` | `17/22` | `RESOLVED_HOPS=17/22`, CLEAN |
| round-1 exports | `3/3` | `VERDICT_BEARING_EXPORTS=3/3` |
| `tools/quote-reopen.py` | unchanged | `git diff be7b8d8d ee1024f -- tools/quote-reopen.py` → empty |

228 = base 215 + 4 C1 cases (216–219) + 9 C2 cases (220–228), matching the SKILL.md row.

## 6. Limits of this review

* I ran the counter **only** on the landed revision and on my own scratch mutants; I did
  not re-run the C2 counter (out of scope for this seat) and did not audit the C1 patch
  against an independent oracle implementation.
* The mutants are *my* reading of a plausible wrong implementation; a different wrong
  implementation might evade the counter in a way I did not construct. The 10-mutant
  survey is evidence of discriminating power, not a proof of it.
* §4a/§4b are coverage findings about the **frozen counter**, which I did not and must not
  edit; the landed gate's 120/120 is real, but the predicate is weaker than it reads.

## 7. Tooling

No installs, no upgrades, no pacman/uv/cargo transactions — every check was satisfied by
the pre-existing toolchain (`python3`, `git`, `bash`, GNU `grep -P`). Nothing was mutated
in the lane: the counter, the gate, and the frozen design were read-only; my five receipts
live in `.ufo/waves/round-31/falsify/RerunC1A/`, and every mutant/clone/probe lives in
`/fast/scratch/hyaku/chousa-r31/w2/RerunC1A/`. No git/jj write commands were run in the
lane or the fleet repo.
