# MutC2Keyed — C2 fixture-keyed shortcut probes (round 34 attempt 2, wave 2a2)

Seat: mutation-tester, target "C2 fixture-keyed shortcuts (no real dead-zone search)".
Mode read-only on lane production; every experiment in a scratch clone.

## Pins

- Lane tip `707da8184a0fc4d10ab3f17271556cdf364f0af5`; `git show 707da81:tools/research-gate.sh | sha256sum`
  = `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` = working-tree
  `tools/research-gate.sh` at start **and** at end (restoration evidence: unchanged).
- Counter `corpus/evidence/round34/c2-count.py` sha256
  `8c0def4d377cdf1a1e4bd2c9151bb0846216658ff14d725d15ac037c12212173`; working tree equals the
  committed blob; never edited.
- Pre-C2 gate: `git show bf7c931a:tools/research-gate.sh` sha256
  `772a1d8e4d94dbf3a44a64bf850b1324e51546eeb62abcd7b3ec585f0e003e58` (`TOK_DIRECT_SPAN_MAX=32767`,
  chunk matcher present; `base-772a1d8e.sh` in artifacts).
- Seeds used: **6101, 6103** (fresh; not 5011/5023/5033/5047). `C2_TMP` set inside scratch.
  All runs `timeout 1800` / `timeout 900`; the shell call waited; no processes of mine remain
  (`pgrep -af c2-count.py` shows only a sibling seat's seed-7101 run, PID 3371355 — not touched).

## Baseline (landed gate, same counter and fixture)

```
python3 corpus/evidence/round34/c2-count.py --gate <clone>/tools/research-gate.sh \
  --seed 6101 --receipt receipts/base-s6101.json      # DEADZONE_MATCH=37/37, elapsed 22.5 s
python3 corpus/evidence/round34/c2-count.py --gate <clone>/tools/research-gate.sh \
  --seed 6103 --receipt receipts/base-landed-s6103.json  # DEADZONE_MATCH=37/37
```

Receipt `base-s6101.json`: `gate_sha256=a6307edf…`, `counter_sha256=8c0def4d…`,
`matched=37`, `predicate_holds=true`. Committed receipts `.ufo/waves/round-34/measure-a2/c2-after-s{5011,5023,5033,5047}.json`
all read `gate_sha256=a6307edf…`, `matched=37`, `predicate_holds=true` (opened). The landed
after-state is re-derived on fresh seeds.

## Controls (each: scratch copy of the landed gate, one minimal patch, `bash -n` clean)

Patches touch only the span path (`tok_span_offsets` / `tok_span_at`) or insert one keyed
branch at the observed-computation site (`research-gate.sh:1880`). No counter edit.

| # | control (key) | sha256 (16) | seeds | count | verdict |
|---|---|---|---|---|---|
| 1 | `ctl1-lengthkey` — span length in [32765,32767] ⇒ supported, no source read | `ecc776d74541e296` | 6101/6103 | 20/37, 20/37 | **MISSES** |
| 2 | `ctl2-labelkey` — echo the record label (`expect=supported` on every record) | `26a8acf7882bbda5` | 6101/6103 | 0/37, 0/37 | **MISSES** |
| 3 | `ctl3-idkey` — `id` hex value mod 3 picks the verdict (randomised metadata) | `ec5cb861f69ddf85` | 6101/6103 | 8/37, 12/37 | **MISSES** |
| 4 | `ctl4-fixedkey` — root prefix `chousa-r34-c2-*` + length ⇒ python3 whole-bytes exact search; never calls `tok_span_offsets_chunk`/`_direct` | `92ed87c94abf24c2` | 6101/6103 | 37/37, 37/37 | **MEETS** |
| 5 | `ctl5-noboundary` — landed matcher, boundary helpers forced true | `8b2a68a777449d6d` | 6101/6103 | 33/37, 33/37 | **MISSES** |
| 6 | `ctl6-claimshape` — record shapes `c[0-9a-f]{10}` + `src/[0-9a-f]{16}\.md` + `expect=supported` ⇒ same python exact search; temp-dir prefix never consulted | `5ca84192160f20a4` | 6101/6103 | 37/37, 37/37 | **MEETS** |

Per-class results are in `receipts/ctl*-s*.log` and the receipts' `per_class`/`misses`.

### What each key actually bought

1. **Length key, 20/37.** The 12 dead-zone *supported* records (10 non-line + 2 `dz-line-bound`)
   and the 4 short records score, but the 17 dead-zone `unsupported` records read `supported`
   (`dz-mut-*` 6, `dz-decoys` 5, `dz-split` 2, `dz-glued-*` 4). Span length alone carries no
   truth; the counter's 33/4 long/short split is not a class key.
2. **Label key, 0/37 — counter guard.** Every record carries `expect=supported` (counter:279), so
   echoing the label makes all 37 verdicts `match`, the gate exits **0** with no
   `RESEARCH_GATE: DRIFT`; the counter scores every record `none` unless `rc == 1 and drift`
   (counter:336). Receipt `gate_rc=0`. A label echo cannot even be scored, by design.
3. **Id key, 8/37 and 12/37.** Ids are `c%010x` from `rng.getrandbits(40)` (counter:273-275), drawn
   before the class is built and independent of truth; a 3-way split lands at chance (expected
   37/3 ≈ 12.3). Record order (`rng.shuffle(plan)`, counter:269), file creation order
   (`rng.shuffle(files)`, counter:287) and mtimes (`1.6e9 + randrange(10**8)`, counter:292) come
   from the same independent RNG stream — [INFERENCE] no function of them can predict truth, so
   they were not run as separate controls.
4. **Fixed-string key, 37/37 — the finding.** See below.
5. **No-boundary key, 33/37.** Replacing the token-boundary rules with `return 0` misses exactly
   `dz-glued-left 0/2` and `dz-glued-right 0/2` (MISS lines: truth=unsupported, observed=supported);
   every other class still scores. The boundary classes are the only thing separating a plain
   exact-substring search from the contract — and `ctl4`/`ctl6` keep the real boundary helpers, so
   they get those four for free.
6. **Claim-shape key, 37/37 — variant that does not need the temp prefix.** The detector is the
   record shape (`id`/`source`/`expect` regexes), i.e. the fixture is recognisable from the claims
   file alone. Same 37/37 on both seeds. (The counter strips `CHOUSA_*` from the gate environment,
   counter:328, so the prefix key is stable.)

## The MEETS finding: why the counter lets a keyed gate through

`ctl4` and `ctl6` never execute the landed dead-zone routing. Their condition replaces the
`tok_span_offsets` body for every span ≥32765 bytes and returns offsets from
`python3` `bytes.find` with an exact whole-span `==` (no `\xHH` PCRE pattern, no
`TOK_DIRECT_SPAN_MAX`, no probe chunk, no grep). Evidence that the keyed branch, not the landed
fallback, produced the score: an instrumented copy (`probe-ctl4-instrumented.sh`,
`5552b125ac36a524`) appends one line per branch entry; seed 6103 scored **37/37** with
**39 firings** (`keyed-fired.log`), and `probe-ctl6-instrumented.sh` (`a42ffa11737916ea`) scored
**37/37** with **39 firings** (`keyed6.log`). 39 = 33 dead-zone records × one `tok_span_offsets`
call + 6 `tok_span_all` enumerations for the line-bearing long records [INFERENCE, exact for the
fixture shape]. Without the branch these gates are byte-identical fallbacks to the landed gate, so
the tracer is what proves execution.

Why it passes:

- The counter scores **only** the `CLAIM … observed=` label and the `CLAIM_LINE_MISMATCH` finding
  set, parsed by `LINE_RE`/`FIND_LINE_RE` (counter:95-96). Gate stderr (where
  `grep: regular expression is too large` appears) is stored as a receipt tail and never asserted;
  nothing observes which matcher ran, how long it took, or whether grep was invoked at all.
- Every one of the 17 classes' truths is exactly the semantics "exact whole-span occurrence +
  round-4 token boundaries + optional line range". Any engine implementing that semantics is
  behaviourally indistinguishable from the chunk matcher. `ctl4`/`ctl6` do implement it, so they
  are correct implementations — the counter cannot tell them from the landing fix.
- The fixture is fingerprintable and self-describing: `mkdtemp(prefix="chousa-r34-c2-")`
  (counter:314) plus `c%010x` ids and `src/%016x.md` names (counter:273-276); and for every
  supported truth the span is inserted verbatim into the source (e.g. counter:189,196,207,256),
  while decoys are same-length one-edit copies. An exact search is guaranteed to reproduce truth.

Consequence for P2: the predicate is **behavioural**, not mechanism-pinning. A gate that (a) is
keyed on the counter's own temp prefix or on its record shapes and (b) uses a non-grep exact
search scores 37/37 without ever exercising the dead-zone routing the claim's "Fix" paragraph
describes. This is a coverage finding, not a contract violation: `ctl4`/`ctl6` satisfy C2's
written contract clauses 1–4, and the landed gate independently re-derives 37/37.

## Claim-record defect found while re-deriving the before-state

`claims-a2.md:100-103` says the do-nothing control's "17 long-supported records … must miss … short
records (4) pass. Expected ceiling 4/37." The committed receipts
`measure-a2/c2-before-s5011.json` and `-s5023.json` both print `matched=21`, `label=DEADZONE_MATCH=21/37`
(gate `772a1d8e…`, same counter sha). I re-derived it on fresh seeds:

```
python3 corpus/evidence/round34/c2-count.py --gate base-772a1d8e.sh --seed 6101  # 21/37
python3 corpus/evidence/round34/c2-count.py --gate base-772a1d8e.sh --seed 6103  # 21/37
```

`receipts/base772a-s6101.log` shows matched classes 21 = **19 `unsupported`-truth records**
(`dz-mut-*` 6, `dz-decoys` 5, `dz-split` 2, `dz-glued-*` 4, `short-mut` 2) **+ `short-verbatim` 2**;
all 12 dead-zone supported and all 4 mislocated records miss. The claim's "17 long-supported" is
actually the count of long *unsupported* records, and "4/37" counts only the short records: the
dead-zone failure yields the correct label for every record whose truth is `unsupported`, which
the prediction ignores. SCORECARD.md:1956 reports 21/37, so the frozen design v4 and the
scorecard disagree; the claim text was not reconciled.

Effect on P2: none on the predicate as written (the 21/37 runs are on the pre-fix gate
`772a1d8e`, not the landed gate; no committed run *on the landed gate* is below 37; landed
receipts are 37/37 ×4 plus my fresh 37/37 ×2). But the claim's own do-nothing expectation is
falsified by its own receipt, and the paragraph's arithmetic is wrong on both numbers (17, 4).

## Limits

- Six keying strategies scored on two fresh seeds each; the two MEETS controls are alternative
  implementations, so their 37/37 says nothing about whether the *landed* chunk matcher is what
  runs — that was verified separately by the pristine baseline (37/37, gate a6307edf).
- Not attempted: mutation of the landed chunk matcher itself (not my target), C3 self-audit,
  C1 long-span surface, selftest/battery re-runs (out of scope), any fleet/sibling state.
- No network; no lane jj/git writes; lane gate hash identical before/after
  (`a6307edf…`), `git status --porcelain` shows only `?? .ufo/waves/round-34/w2a2/`.
- Artifacts (each <1 MiB): `.ufo/waves/round-34/w2a2/MutC2Keyed/` — six control gates,
  two instrumented probes, `keyed-fired.log`, `keyed6.log`, all receipts/logs.
