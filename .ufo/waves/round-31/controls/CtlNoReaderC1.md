# CtlNoReaderC1 — C1 no-reader control (round 31, pre-data control wave)

Seat `ChousaR31.CtlNoReaderC1`. Target: C1 coverage / line binding, counter
`corpus/evidence/round31/c1-count.py` (predicate `LINE_BINDING_MATCH=120/120`).
Sandbox `/fast/scratch/hyaku/chousa-r31/CtlNoReaderC1/`. Every run wrapped in `timeout 900`;
fitting seeds (1000–1079, 2000–2039) and scoring seeds are disjoint.

## Control

`control_noreader.sh` (gate substitute; `bash <gate> verify-claims <claims.jsonl> --root <tmp>`)
reads **only** the claims path — never a source file — and decides from claim-file features:

1. `"line"` absent → `supported` (B4 is the only no-line class).
2. `"line"` present but not `N` / `N-M` (N≥1, M>N, decimal, no leading zero) → `invalid`.
3. span contains `"\n"`: range `N-(N+1)` with `N≤27` → `supported`; anything else multi-line
   (single `N`, or width ≥ 3) → `mislocated`.
   Sound without the source: B3 starts at `a+1 ≤ n-3 ≤ 27`; M4-`late` starts at `a+2 ≤ n-2 ≤ 28`,
   so a width-2 range starting at ≥28 cannot be B3.
4. valid single `N` → `mislocated` (largest class; no source-free posterior for `supported`
   exceeds 0.42 and the analytic maximum is 0.361).
5. it prints `FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=<id> …` for every
   claim it labels `mislocated` (required by counter design v2, ignored by v1), and each id once.

`control_noreader_maxsel.sh` adds one gambling rule: relabel the 12 claims with the highest
analytic `P(supported | line value)` (n~U{14..30}, class counts fixed) as `supported`.
`control_noreader_nofind.sh` is the same rule without FINDING lines (ablation).

No source access, proved by
`strace -f -e trace=openat,open,stat,newfstatat,statx,getdents64,access` on a kept fixture
(`strace-control-noreader.log`): exactly one access under the fixture root —
`openat(..., ".../claims.jsonl", O_RDONLY)`; zero accesses to `src/` or any `.md`. The control
also emits complete output with `--root /definitely/not/a/root`.

Install record: none (python3 and strace already present; no pacman/uv/npx use).

## Receipts

Counter revisions are hash-pinned copies in this seat's dir (`c1-count-v1-154e09e7.py`,
`c1-count-v2final-81fe5015.py`), because the lane copies were being edited during the wave (§5).

| control | counter | seeds | score | receipt |
|---|---|---|---|---|
| `control_noreader.sh` | v1 `154e09e7` = HEAD `d78d188` | 810001–810006 | 85, 85, 84, 86, 85, 85 (mean 85.0) | `seed-81000{1..6}.json` |
| `control_noreader.sh` | v2-final `81fe5015` | 910001–910005 | 86, 86, 86, 86, 86 | `v2f-seed-91000{1..5}.json` |
| `control_noreader_maxsel.sh` | v1 `154e09e7` | 810001–810005 | 84, 83, 85, 90, 83 (max 90) | `v1-maxsel-81000{1..5}.json` |
| `control_noreader_maxsel.sh` | v2-final `81fe5015` | 910001–910005 | 80, 81, 84, 87, 78 (max 87) | `v2f-maxsel-91000{1..5}.json` |
| `control_noreader_nofind.sh` | v2-final `81fe5015` | 910001 | **30** | `nofind-v2f-seed-910001.json` |

Offline (same rule, 80 seeds; fitting axis only): v1 mean 86.15, min 82, max 88;
v2 exactly 86 on all 80 seeds. Maxsel offline: v1 mean 83.65 **max 92**, v2 mean 83.78 max 91.
The 30-seed sweep `sweep-30seeds.log` (lane path, counter `d201ef4b`) also returned 86 every run.

**Best no-reader score: 86/120 (71.7 %) at means; 92/120 on one seed** with the count gamble
(that variant's mean is 83.7, i.e. it loses on average). 34 claims are always missed:
B1 12 + B2 12 (supported, one-line spans), U1 8 (unsupported), M4-late 2.
Per class (v2-final): B3 12/12, B4 6/6, M1 12/12, M2 12/12, M3 12/12, M4 6/8, M5 6/6, M6 8/8,
I1 12/12; B1 0/12, B2 0/12, U1 0/8.

## Findings

### 1. What the claims file leaks (answer to "which features predict truth")

| feature | measurement | usable? |
|---|---|---|
| `line` format invalid | invalid 960/960 (100 %) | yes — 12 claims, by design |
| `line` absent | supported 480/480 (100 %) | yes — 6 claims |
| span has `"\n"` | width-2 range → supported 960/1108 (86.6 %, v1) / 960/1120 (85.7 %, v2); width ≥3 → mislocated 194/194 (100 %) | yes — 18/20 multi-line claims |
| line value > 30 | mislocated 100 % (M5 tail, ~6 claims/fixture) | yes, but already the default label |
| line-value magnitude | analytic max P(supported) 0.361 at v=20; empirical 0.42 at n=17 (v1); v2 bumps at `v=1` (2.0 supported vs 1.94 mislocated/fixture) and `v=n` (B1 first/last, 0.7 claim/seed) | **no** — v1's `v=1` would *lose* 1.65/seed; v2's `v=1` gains 0.06/seed |
| key order (full/prefix/position) | held-out 0.4833 = constant baseline; the only gain is `line`-key presence (= feature 2) | no |
| `id` / `source` hex | held-out 0.4833 = baseline (both versions); χ²(id nibble)=42.5/37.9, χ²(src nibble)=30.3/59.1, df=45 (v1/v2) | no |
| span word count / length, claim text, file position, key count | held-out 0.4896 / 0.4833 / 0.4833 / 0.4833 / (only line-presence) | no |
| greedy tree over all features (depth 2/3/5, held-out) | 0.6992 / **0.7188** / 0.7188 (v1), 0.7000 / 0.7167 / 0.7152 (v2) — never beats the rule | no |

So beyond the format-invalid class, two features predict truth far better than chance:
`line`-absence (perfect) and newline-in-span (86.6 % precision on width-2). Both follow from
the class design, not from source bytes: a no-reader gate can know a claim's class family, but
never whether a one-line span sits on the named line. No feature separates `supported` from
`mislocated` inside the one-line group.

### 2. The fixed class counts do not rescue it

Among valid one-line claims the fixture holds exactly 24 supported / 50 mislocated / 8
unsupported, so a control can try to pick the 24 most-likely-supported. The ceiling is
`P(supported|x) ≤ 0.361` analytically (empirical ~0.42 on a 0.35-claim/seed value), so any
24-set contains ~8.2 (v1) / 8.6 (v2) true supported and `50 + 2·S_top − 24` goes negative:
measured mean 81.6–84.4, max 91–92 versus 86 flat for the plain rule. The gamble only wins on
lucky seeds. [INFERENCE] A *metadata* reader (stat → n, outside this seat, not built) could add
at most ~1 claim/seed: with n known, `v=n` is 2 guaranteed B1-last plus ~0.8 B2 against ~1.8
mislocated and ~0.4 unsupported, so labelling that one value supported nets ~+1. The 34-claim
gap stays either way.

### 3. v2's FINDING rule is a formatting trap, not a truth discriminator

v2-final requires `obs == truth` **and** a `FINDING CLAIM_LINE_MISMATCH … obs=id=<id>` for every
mislocated truth and no finding on any other truth. Measured: the same control scores 86/120
with findings for its own mislocated labels and **30/120** without them (`nofind` receipt). The
rule adds no resisting power against a claims-file-only gate — it only penalises gates that emit
a mislocated verdict without the matching finding (or a stray finding). Its real bite is on
candidates; it does not change the control ceiling.

### 4. Counter revision drift during the wave — wave integrity

The lane working tree went dirty mid-wave; the counters changed under the runs:
at least four distinct `c1-count.py` hashes in ~20 minutes.

| revision | sha256 | when observed |
|---|---|---|
| HEAD `d78d188` (frozen v1) | `154e09e7f73bebaf…` | 01:24, and all v1 receipts |
| v2 mid ("design v2", fixed SUBVARIANTS) | `d201ef4ba5cf9637…` | file mtime 01:26:45; 30-seed sweep |
| v2 mid (edit) | `c0a0908c88b902a7…` | 01:29 (snapshot) – 01:36 (drift check) |
| v2 final (FINDING rule, env scrub, dup→none, harness exit 2) | `81fe501528d05c11…` | 01:33 mtime, still current at last check |

`git status` shows both ` M corpus/evidence/round31/c1-count.py` and ` M …/c2-count.py`; the diff
against HEAD adds `SUBVARIANTS`. Consequences:

- Receipts pin the counter hash they touched, so each row above is reproducible from the
  hash-pinned copies. Do not mix receipt sets across revisions.
- v2 is deterministic at class level: the control scores exactly 86 on 80/80 offline
  seeds and 5/5 fresh v2-final runs (plus 30/30 sweep runs on v2-mid), while v1 swung 82–88. The two-fresh-seed predicate no
  longer samples fixture variation for a class-blind control.
- If v2 lands, freeze the hash and re-run every control against the committed revision; my
  v2-final receipts already use `81fe5015`.

### 5. No premature saturation of the C1 surface

A no-reader control cannot approach 120: the 34 misses are exactly the claims whose verdict
needs the source bytes (one-line supported vs mislocated, and the absent-span class).
A candidate scoring below ~86 would be doing worse than not reading the sources at all.

## Verdict

**design holds** — the strongest claims-file-only control reaches 86/120 (max 92 on one seed
with a gamble that loses in the mean), 34 below the predicate, and every point it earns comes
from `line` format/absence and newline-in-span class shape, never from source bytes.
