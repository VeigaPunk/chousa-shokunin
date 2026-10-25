# Round-8 lesson — a behavioral pin freezes an output surface, not an oracle: the volatile contract is an invocation property, and which surface you pin decides the regression class you can see (2026-10-16 UTC)

Round: chousa-shokunin round 8, one freshness/operability move — the gate's own
drift becomes detectable (`--pin <path>` baseline with a declared volatile list,
`--drift <path>` reporting `none`/changed fields/malformed). The design is
adapted from the sibling lane's r10 pattern
(`../mori-shokunin/corpus/lessons/2026-10-15-volatile-contract-behavioral-baselines.md`).

Source seat: lessons-distiller. The `--pin`/`--drift` implementation **landed
mid-window**, in the sequence the mori r10 note documents — header contract and
usage first (`fc8695cd…`), mechanism second (`b4dd27a1…`, 4043 lines), selftest
arms last (`30d89dbf…`→, 4175 lines) — so this note has two layers. §1-§2
measure the gate surface at the entering r7 bytes
`3ba718bf9207eed70c66b8c849ac43b44c76890785e1576eeb5e795a604166b2` (impl
absent there; mutants on **scratch copies** only,
`$HOME/.cache/chousa-tmp/r8-lessons/`); §1b verifies the landed mechanism
itself at named revisions. Lane HEAD `848738c`. The gate file moved repeatedly
during the window (observed shas in §5), so every claim below names the
revision it was read or run at.

Gate under measurement: `tools/research-gate.sh` sha256 `3ba718bf…`, 3666
lines, `VERSION=research-gate-r1`; `--selftest` → `RESEARCH_GATE_SELFTEST: PASS
(74 cases)` exit 0 (47 s wall; run three times — wall-clock ×2, pinned epoch ×1
— all three PASS sets byte-identical, §1). Fixture:
`$HOME/.cache/chousa-tmp/r8-lessons/fx/all-pass.md` (CLEAN record in the r6
fixture's shape) + `claims-pass.jsonl`, `--root` = the fixture dir; measured:
composed CLEAN exit 0, `sections=5 run=5`, integrity
`refs=6 resolved=4 unresolved=0`.

## The lesson

A "pin the output, diff it later" baseline makes **two independent design
decisions, and the lineage only names one of them**. (1) *What you mask* — the
volatile set. The mori r10 lesson solves this for a gate that reads the host:
32 of 33 live lines churn, so a 6-class field mask is load-bearing. (2) *Which
surface you pin* — the invocation and its resolution. That decision is silent
in a byte diff but it decides which regression classes the pin can see at all.
Measured here at `3ba718bf…`: chousa's gate reads only the record, fixtures and
the wall clock, so its volatile set is **one token** (`ts` in the header) and
**zero** when the clock is pinned via `CHOUSA_NOW_EPOCH`
(`research-gate.sh:191-195`) — volatility is an *invocation* property, not a
gate constant, and the pin's harder problem here is (2): the composed
`verify-all` output and the selftest PASS set each miss a regression class the
other catches, and both are blind to oracle strength (a weakened assertion
changes no printed byte at all). A pin freezes a surface, not an oracle — so
the re-pin ritual must include a source review of the gate, not only its bytes.

## 1. The volatility side, measured: one token unpinned, none pinned

All runs under `$HOME/.cache/chousa-tmp/r8-lessons/`; `CHOUSA_NOW_EPOCH=1792100000`
renders `ts=2026-10-15T21:33:20Z` in every mode's header.

```
# composed surface, clock pinned:
CHOUSA_NOW_EPOCH=1792100000 bash tools/research-gate.sh verify-all fx/all-pass.md \
  --claims fx/claims-pass.jsonl --root fx      # 3 runs, exit 0, 873 B, 8 lines
diff va-pinned-1.out va-pinned-2.out  → IDENTICAL
diff va-pinned-1.out va-pinned-3.out  → IDENTICAL
# same invocation, clock live, 3 s apart:
diff va-live-1.out va-live-2.out
1c1
< research-gate research-gate-r1 — ts=2026-10-16T03:21:22Z — …
---
> research-gate research-gate-r1 — ts=2026-10-16T03:21:25Z — …
# token inventory: 16 distinct `k=` tokens; comm of `k=v` sets live1 vs live2
#   changed: ts only — 1 of 16. The other 15 (absent claims drift findings mode
#   record refs resolved root run sections state tally unresolved verdict) equal.
```

- **Line granularity vs field granularity, with chousa numbers.** Only 1 of 8
  lines contains the volatile token, and that line (the verify-all header,
  `research-gate.sh:2096-2097`) also carries four stable provenance tokens
  (`mode=`, `record=`, `claims=`, `root=`). A line-level mask would discard
  four stable tokens to hide one (`root=` deletion is exactly mutant m3 below);
  a field-level mask of `ts` costs nothing else. Same conclusion as the lineage
  ("mask per field, never per line"), restated on this gate's schema.
- **Per-mode uniformity.** Two live runs each of `verify`, `verify-integrity`
  and `verify-chain` on the same fixture differ on the header `ts` token only
  (a same-second pair of `verify` runs is byte-identical — the churn is
  second-granularity, so a pin/drift battery must not conclude "stable" from a
  same-second control).
- **The selftest PASS set has zero volatile tokens.** `diff selftest-1.out
  selftest-2.out` → IDENTICAL (two wall-clock runs), `diff selftest-1.out
  selftest-pinned.out` → IDENTICAL (pinned epoch). 75 lines / 3614 B: 74
  `ok-case N name exit=R` lines plus `RESEARCH_GATE_SELFTEST: PASS (74 cases)`
  (`research-gate.sh:3597-3602`). A PASS-set baseline needs no mask of any kind.
- **The manifest is a third pinnable surface with different semantics.** Two
  pinned `--json` appends over one file produced two **byte-identical** lines
  (sha256 `c941888798d2faa69ff23ce8af7e5360b9671bda94083f14b5d58488e1ea4149`),
  because the line carries `ts` + `record_sha256` + `gate_sha256`
  (`research-gate.sh:2087-2089`). A manifest-pinned baseline is *revision-bound*
  (a whitespace-only gate edit moves `gate_sha256`), while the stdout surface is
  *behavioral* (carries no SHA). The round's "SHA fields masked" clause is thus a
  no-op on the stdout surface and a real design choice — behavior vs revision —
  on the manifest surface.

**Why this differs from the lineage, and what to carry over.** mori's census
reads host state (kernel counters, cgroup watermarks), so its live output is
mostly churn and only a declared mask makes a baseline usable. chousa's gate
reads no host state: its live output churns a single token, and pinning the
clock (a first-class env input, honored by every mode) collapses the volatile
set to empty. The transferable rule is not "reuse a mask"; it is "derive the
set from the invocation, and prefer the invocation that makes it empty". The
lineage's own numbers invert here: its mask covered ~47% of the schema; copying
that list onto chousa would mask 15 of 16 stable tokens (~94%) and buy nothing.
Conversely chousa's near-empty list would leave mori red on every run. The
pin's header should print the (possibly empty) mask so "nothing was masked" is
auditable — with an empty list that string is the strongest form of the pin.

## 1b. The landed mechanism, verified at named revisions

Read at `b4dd27a1…`–`30d89dbf…` (header `:153-199`, implementation
`:2190-2499`, usage `:263-264`), and run in a battery whose `sha256sum
tools/research-gate.sh` was `30d89dbf…` **before and after** the whole battery
(`30d89dbfdb0ebcff…`, 4175 lines — the file was stable across it; the
pin/drift-none arms were re-spot-checked at `46f5ddb3…` with the same
results). All probes: cwd = lane root, outputs under
`$HOME/.cache/chousa-tmp/r8-lessons/`.

| probe | result | exit |
|---|---|---|
| `--pin <path>` | `GATE_PIN: ok path=… gate_sha256=30d89dbf…`; 19-line baseline: header (`pinned_ts=2026-10-16T03:28:08Z`, `# volatile_fields=ts gate_sha256`, the canonical command line), `# --- canonical output follows ---`, then the capture — the self-written fixture's composed output incl. its line `FINDING REF_UNRESOLVED severity=warn …` and `RESEARCH_GATE: DRIFT (sections=5 … drift-sections=1 …)`, then the manifest line | 0 |
| `--drift <that baseline>` 44 s later, live clock | `GATE_DRIFT: none` | 0 |
| `--drift` missing path | `research-gate: --drift baseline missing: …` | 2 |
| `--drift` junk file | `research-gate: --drift baseline malformed (magic line absent): …` | 2 |
| baseline body tampered by one key (`drift-sections=1` → `2`) | `GATE_DRIFT: drift-sections` | 1 |
| baseline's declared list rewritten (`# volatile_fields=ts`) | `GATE_DRIFT: volatile_fields` | 1 |
| drift driver = gate copy with the verify-all header's `— root=` dropped | `GATE_DRIFT: -root` | 1 |
| `--pin` with no PATH | `research-gate: --pin needs PATH` | 2 |

Design facts that bear on this note's claims:

- **The declared volatile set is exactly `ts gate_sha256`** (`:2199`), masked
  shape-scoped (`:2212-2215`: only `ts=YYYY-MM-DDTHH:MM:SSZ`, `"ts":"…"`,
  `"gate_sha256":"…"` become `<V>`; a malformed timestamp keeps its bytes and
  surfaces as drift). §1 independently measured `ts` as the single churning
  token and `gate_sha256` as manifest-only — the landed list is precisely that;
  every counter, `record_sha256` and contract word is compared unmasked. Two
  independent derivations agree.
- **The pinned surface is a third choice, not one of §2's two candidates**: the
  gate writes its own temp fixture (`gate_pin_fixture` `:2220-2268` — the r7
  all-dangling record, so the capture carries a FINDING, a DRIFT verdict and
  the `--json` line), runs the canonical invocation inside it with relative
  paths and the `CHOUSA_*` env stripped (`:2282-2286`), then removes it. So the
  pin's *resolution* is the composed tally/FINDING surface (the span-shift
  blind spot of §2 applies unchanged), its *fixture* is hermetic by
  construction — and neither the selftest PASS set nor solo outputs are pinned.
- **The DRIFT-roll rule, measured**: the canonical fixture itself rolls
  `RESEARCH_GATE: DRIFT`, and `--pin` exits 0 — pinning a DRIFT run is still a
  pin; the roll lives inside the captured bytes.
- **Neither mode prints a `RESEARCH_GATE` line** (`grep -c '^RESEARCH_GATE'` =
  0 in every pin and drift output measured), so a consumer counting verdict
  lines cannot mistake a baseline operation for a record verdict.

## 2. The resolution side, measured with mutants on scratch copies

Five mutants, each a copy of the gate at `3ba718bf…` under
`$HOME/.cache/chousa-tmp/r8-lessons/` (`mut-m*.sh`), run against the same
fixture (pinned clock) and/or through `--selftest`:

| mutant | the change | verify-all fixture output vs base | selftest PASS set vs base |
|---|---|---|---|
| **m1** weakened oracle | removed `'VERDICT_BEARING_CLAIMS=4/4'` from the `claims-pass` want list (`research-gate.sh:2765-2766`) | **IDENTICAL** | **IDENTICAL**, PASS (74) |
| **m3** dropped a field | removed `— root=%s` + `"$ROOT"` from the verify-all header (`:2096-2097`) | 1 line differs (the header) | **IDENTICAL**, PASS (74) |
| **m4** renamed a tally token | `INTEGRITY refs=` → `refs_count=` (`:1877`) | `SECTION integrity … tally=INTEGRITY refs=6 …` loses `tally=…`; **verdict stays CLEAN, exit 0** | **FAIL (11/74)** |
| **m5** silently skipped mode | `VA_ORDER` without `integrity` (`:1980`) | SECTION integrity line gone, `sections=5 run=5` → `4 run=4`; **verdict stays CLEAN, exit 0** | not run (the r7 cases assert `SECTION integrity` / `sections=5` — read off case text, not measured) |
| **span shift** per-row move | `claims-pass.jsonl` P1 span `line1 primary material` → `line2` | **IDENTICAL** (tallies unchanged) | not run; solo `verify-claims` names it: `CLAIM id=P1 … at=line:2 …` vs `at=line:1` |

Conclusions that hold across the set:

1. **The verdict is not the surface — the round's "before" claim, measured.**
   m5 skips a whole mode: the closing counters move (`sections=5 run=5` →
   `4 run=4`) but the verdict word stays `CLEAN` and the exit stays 0. m4
   loses a composed tally: its closing `VERIFY_ALL`/`RESEARCH_GATE` lines are
   byte-identical to base (measured), verdict `CLEAN`, exit 0 — only the
   `SECTION integrity` line's `tally=…` text moves. In neither case does a
   consumer of verdicts, counters-as-verdict or exit codes see a *drift*; a
   byte pin names both (m5's counters, m4's tally). This is the precise gap the
   round closes.
2. **A pin's resolution is the pinned surface's granularity.** The span-shift
   probe moves a per-row disposition (`at=line:1` → `at=line:2`) with every
   tally equal; composed `verify-all` output is byte-identical, the solo
   `verify-claims` output names it. So a verify-all pin misses a whole class of
   per-row movement that solo pins catch — and m4 shows the converse: the
   composed surface catches the composition-layer loss (the `tally=` text is
   produced by the *composition's* own grep, `:1952`) that the solo integrity
   mode's behavior never showed.
3. **A PASS set is a coverage claim, not an assertion claim.** m3: the selftest
   passes 74/74 with a byte-identical PASS set while a printed header field was
   deleted; m1: it passes 74/74 with a byte-identical PASS set while one of its
   own assertions was removed. The artifact contains case names and exits only —
   assertion text is not in it. So "pin the selftest PASS set" freezes *which
   cases exist and how they exit*, never *what they assert*.
4. **The two candidate targets are complements, not alternatives.** The fixture
   pin sees printed-field change on one record shape (m3, m4, m5); the PASS set
   sees 74 case classes and caught m4 (11/74) where the fixture saw it too —
   but it is blind to m3, which the fixture sees. Neither sees m1. And m1 is
   not a pin failure: oracle strength is a property of the assertion text, so
   no behavioral comparison can see it. The ritual must therefore pair the
   drift check with a source review of the gate at the same SHA (a diff of
   `tools/research-gate.sh` between rounds), exactly as the lineage pairs its
   baseline with the gate SHA in the header — record the SHA, compare behavior,
   and read the source diff by hand.

## 3. The third exit value, measured on the landed modes

§1b measured the full three-valued contract on the landed mechanism: `--drift`
equal → `GATE_DRIFT: none` exit 0; one changed key → `GATE_DRIFT: <key>` exit
1; missing or malformed baseline → stderr message exit 2; a baseline whose
declared volatile list differs → exit 1 with the token `volatile_fields`
(changing the contract is itself drift). This is the shape the lane has
already committed to elsewhere — r6's "absence is reported, not clean"
(`2026-10-16-verify-all-composition.md`) and the lineage's §5 ("masking solves
churn; it does not solve absence") — and it is inherited rather than invented:
the gate's pre-existing usage path also exits 2 with empty stdout (measured
this round: `verify` with no record and `verify /no/such/record.md`, both
exit 2, stdout 0 bytes, stderr `research-gate: …`; `research-gate.sh:268`).

## 4. Applying it

1. **Record the invocation, not just the gate.** The volatile set here is a
   function of env (`CHOUSA_NOW_EPOCH`, `CHOUSA_STRICT`, `--root`): the re-run
   recipe is part of the baseline's meaning, same rule the lineage derived for
   its `MORI_*` env.
2. **Pin the clock, or mask its field — then print the choice.** With
   `CHOUSA_NOW_EPOCH` fixed the measured mask is empty; the landed design
   instead keeps the live clock and masks `ts` shape-scoped, which additionally
   lets a *malformed* timestamp surface as drift (measured: `# volatile_fields=ts
   gate_sha256` travels in the baseline header). Either way the declared list —
   empty or not — must be printed, so the "none" says what was withheld.
3. **Pin your surfaces deliberately**: the fixture invocation (field-level
   change, composition, mode skips) and the selftest PASS set (case coverage)
   have disjoint blind spots (measured: m3 vs m4). The landed design pins the
   first (its own hermetic fixture, §1b) and not the PASS set.
4. **Know the pin's resolution, and widen it where it matters.** If per-row
   movement must be visible, pin solo-mode outputs on the same fixture — the
   span-shift probe is invisible to the composed pin.
5. **Pair the drift ritual with a source diff.** m1 and m3 are the measured
   reason: a baseline can be green while the oracle is weakened or an
   unasserted field is deleted. Re-pin as a recorded act with a reason
   (lineage §5.3); never re-pin to turn red green.
6. **Do not export a mask list across gates.** Derive per gate; the two lanes'
   measured churn profiles are near-inverses (mori ~47% of schema masked,
   chousa ~6% [1 of 16 tokens] and 0% when pinned).

## 5. Limits of this note

- One host, one fixture for §1-§2; the gate file moved under this seat's
  measurements (observed `3ba718bf…` → `fc8695cd…` → `b4dd27a1…` →
  `a05abcc6…` → `ab23ea85…` → `c1a45a61…` → `02e001ce…` → `30d89dbf…` →
  `46f5ddb3…`, 3666 → 4183 lines). §1's surface facts are at `3ba718bf…`,
  §1b's battery at `30d89dbf…`, spot-checks at `46f5ddb3…`. Re-check the sha
  before re-running anything.
- Two selftest runs during the window each reported `FAIL (1/84)` at the new
  pin/drift arms, on **different** cases, with transient signatures. (a)
  `drift-clean`: `--drift canonical capture failed (rc=2 verdict-lines=0
  manifest-lines=0 schema-lines=0)` while the gate sha was `30d89dbf…` before
  and after the run and all five sibling pin/drift cases on the same baseline
  passed. (b) a re-run: `all-pass.md rc=127` while the gate file was being
  rewritten mid-run (`30d89dbf…` → `46f5ddb3…`, measured). Both are
  fail-closed (exit 2 / a failed case, never a false `none`), neither
  reproduced on re-run. The rc=2 signature matches the capture's temp dir
  disappearing between its creation and use (`( cd "$fx" || exit 2`, `:2282`)
  — an inference from the signature, not a measured cause; the wave's /tmp was
  under 32-seat load (12 G of 16 G used, 38 `chousa*` entries). The earlier run
  on the pre-arms bytes (`a05abcc6…` → `ab23ea85…`) was `PASS (74 cases)` with
  the PASS set byte-identical to the entering bytes (diff = 0 lines) — this
  seat's own check of the round's 74-case-stability claim.
- If a future revision widens the mask beyond `ts` on the stdout surface,
  §1's deltas are the counter-evidence: those tokens demonstrably do not
  churn, so the wider mask would hide stable provenance rather than noise.
- The mutants are scratch copies; their `--selftest` runs executed from a
  non-lane directory, so `LANE_ROOT` differs from the lane's. All selftest
  fixtures live under `CHOUSA_ROOT=$WORK`, and no measured case depends on the
  lane root, but the copies are not byte-equivalent environments for the
  boundary fallbacks that consult `LANE_ROOT` (`:434`, `:845-846`, `:1474-1475`).
- m5's selftest arm was read off the case text, not run; m4's 11 failures were
  counted from its own run (`grep -c '^FAIL-case'` = 11).
- The 1-token churn result holds only while the gate reads no host state. A
  mode that starts printing a second-granularity clock inside FINDING lines
  (today only the header carries `ts`) would widen the set; the pin, not this
  note, is the instrument that would report that.
- No scalar score, no verdict about the round's admission; the raw logs
  (`selftest-{1,2,pinned,m1,m3,m4}.out`, `va-{pinned-1..3,live-1..2,mut-m1,m3,m4,m5,shifted}.out`,
  `solo-*.out`, `manifest.jsonl`, `mut-m*.sh`) live under
  `$HOME/.cache/chousa-tmp/r8-lessons/` and are ephemeral by design.