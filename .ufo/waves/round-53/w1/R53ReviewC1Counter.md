# R53ReviewC1Counter — frozen C1 counter (corpus/evidence/round53/c1-count.py) vs R53-C1 predicate

Review target: `c1-count.py` (384 lines, sha256 e3aff6bf…703c7), committed at the freeze commit a6ff732c (clean tree). Tool under test: `tools/assimilate-rows.py` at candidate v4 (commit 32aab5e). All runs in `/fast/scratch/hyaku/chousa-r53/R53ReviewC1Counter/` with TMPDIR set there.

## Baseline (v4 passes, as frozen)
```
$ TMPDIR=$S python3 …/round53/c1-count.py --per-leg 1 --seed 7 --work $S/base-seed7
SEED=7
TWIN case1 PASS rc=0 held=0 twin=1 append=3 map=ok rows=3
HELD case1 PASS rc=0 held=1 twin=0 append=1 map=ok rows=1
MIX case1 PASS rc=0 held=4 twin=2 append=4 map=ok rows=4
RECHECK case1 PASS on=held rc=1 refused-line=True renumber=False append=False
ORDER case1 PASS kind=row-outside rc=1 refused=2 registry-first=True
NOENTRY case1 PASS kind=row-outside broken-rc=1 sound-rc=0
REAL PASS rc=0 map=ok rows=5 count-line=['CITED=6 APPEND=5 HELD=0 TWIN=1']
REGRESS PASS r50-pin=ok r51-counter=LEGS=5/5
LEGS=8/8  C1=PASS
```
Same `LEGS=8/8 C1=PASS` on seeds 1, 7, and unseeded (SEED=unseeded) — three independent runs all green on v4.

## Findings by severity

### 1. HIGH — RECHECK leg tests only the calendar-invalid-date arm; the predicate's "no leading calendar-valid date or NNd" arm is never generated, so a predicate-violating tool scores C1=PASS
Predicate: "refuses … when one has no leading calendar-valid date or `NNd`". The leg's bad values come only from `recheck_bad()` (c1-count.py:118-122), which always emits an ISO-shaped invalid date (`YYYY-MM-DD` with impossible day/month/year). No generated row ever carries a recheck that lacks a leading date or NNd (e.g. `2026/02/30`, `30-02-2026`, empty). Since only the date arm is probed, the "no date at all" arm is untestable.

Reproduction: mutant M1 = v4 with the recheck block (tool:511-515) changed to refuse only `DATE_RE.match(lead) and not valid_date(lead)` (i.e. accepts `2026/02/30`, `soon`, `TBD`). Direct demo on a cited row with recheck `2026/02/30`:
```
v4: rc=1 stderr="REFUSED S595: recheck '2026/02/30' has no leading valid date or NNd"  renumber=False append=False
M1: rc=0 stderr="" stdout="CITED=1 APPEND=1 HELD=0 TWIN=0" renumber=True append=True
```
The frozen counter against M1: `LEGS=8/8 C1=PASS` — RECHECK=PASS, REGRESS=PASS, ALL legs PASS, while M1 violates the frozen sentence (it proceeds despite a cited row with no leading calendar-valid date or NNd).
```
$ TMPDIR=$S python3 …/round53/c1-count.py --tool $S/mutant-m1.py --per-leg 1 --seed 53 --work $S/m1
RECHECK case1 PASS on=twin rc=1 refused-line=True renumber=False append=False
REGRESS PASS r50-pin=ok r51-counter=LEGS=5/5
LEGS=8/8  C1=PASS
```
REGRESS cannot compensate: round-50 fixtures `expected.json` contains zero `REFUSED` expectations (`grep -c REFUSED …/round50/c1-fixtures/expected.json` → 0), and the round-51 counter's packages only use valid `90d` rechecks (c1-count.py r51:48,66,146,169,178,196). Nothing in any leg probes the non-date/non-NNd arm. A counter that must falsify the sentence cannot, as built.

### 2. MEDIUM — `--per-leg 0` (or negative) yields vacuous PASS for the six generated legs → `LEGS=8/8 C1=PASS`
main() loops `for k in range(a.per_leg)` (c1-count.py:353) with no lower bound; `all([]) is True`. Observed:
```
$ TMPDIR=$S python3 …/round53/c1-count.py --per-leg 0 --seed 7 --work $S/perleg0
SEED=7
REAL PASS …  REGRESS PASS …
LEGS=8/8  C1=PASS
```
No `case1` line for any generated leg, yet all six report PASS. The kill rule's runs use default 3, so this is a latent "green button" rather than today's protocol failure — but the counter's own CLI can claim C1=PASS with the generated legs never exercised.

### 3. MEDIUM — `counts_ok` matches the tokens anywhere in stdout, not on the count line
`counts_ok` (c1-count.py:185-187) does `re.search(rf"(^|\s)HELD={held}(\s|$)", so)` over ALL of stdout. A stdout line anywhere (a note, a WARN, a decoy) satisfies it even when the real count line lies. Demonstrated:
```
counts_ok("CITED=6 APPEND=5 HELD=9 TWIN=9\nNOTE HELD=0 TWIN=1\n", 0, 1) → True
```
predicate pins "its count line carries `HELD=…` and `TWIN=…`" — a lying count line passes if any decoy token exists. The token regex itself behaves (sanity: `HELD=12` not matched for held=1; `UNHELD=1` not matched).

### 4. MEDIUM — ORDER leg classifies refusal lines by substring; the registry-first check is wording-coupled
`case_order` (c1-count.py:272-274) tags a stderr line as registry iff `"registry" in l`, entry iff `"entry missing" in l`, then requires `max(regi) < min(enti)`. If an entry-missing refusal's text ever mentions "registry", the same correct ordering flips to False:
```
ref = ["REFUSED registry has no `## Registry` heading",
       "REFUSED entry missing: corpus/knowledge/m888.md — registry rows unknowable"]
regi=[0,1] enti=[1] → registry-first=False   (would FAIL, though ordering is correct)
```
v4's actual wordings (`REFUSED registry …` at tool:428-430; `REFUSED entry missing: <name>` at tool:444) have no such overlap, so this is latent fragility, not a false FAIL today. It also tests wording, not the semantic "registry refusals printed first".

### 5. LOW — `expect()`'s normalisation equals the tool's `url_of` on every reachable spelling; latent divergences are unreachable
`expect` norm (c1-count.py:191): `re.sub(r"^[a-z]+://","",u.lower().rstrip("/"))` — lowercases host AND path, strips all trailing slashes, keeps fragments, scheme regex lowercase-only. Tool `url_of` (tool:133-142): strips `#frag`, strips ONE trailing slash, lowercases host only, keeps path case. Property test: exhaustive over the generator's reachable spelling space (scheme×host-case×trailing-slash = 8 spellings, 36 pairs) + 15,000 generator pairs (seeded Gen) → 0 disagreements. Latent divergences demonstrated but unreachable because the generator never emits fragments, ports, uppercase paths, or double slashes:
```
'https://H.TEST/p#frag' vs 'https://h.test/p'   url_of-eq=True  norm-eq=False
'https://h.test/PaTh' vs 'https://h.test/path'  url_of-eq=False norm-eq=True
'https://h.test/p//'  vs 'https://h.test/p'    url_of-eq=False norm-eq=True
```
Answer to the seat question: the generator never produces a spelling where the two disagree.

### 6. LOW — REGRESS hardcodes `--seed 53` (c1-count.py:316): deterministic sub-run
Observed identical REGRESS line under seeds 1, 7, and unseeded while the generated legs vary (all `REGRESS PASS r50-pin=ok r51-counter=LEGS=5/5`). A round-51 regression that manifests only under other seeds is invisible. The frozen sentence only requires "the round-51 frozen counter prints `LEGS=5/5`", so this is a falsification-power weakness, not a contract breach.

### 7. Observation — REAL pin coverage is complete
`pin()` (c1-count.py:66-73) hashes `SOURCES.append.md` + the three `REAL_ENTRIES`; the registry comes from `git show BASE_REV:corpus/SOURCES.md` (frozen by rev). The tool reads exactly these inputs (`--staged`, `--registry`, and only explicit `--entry` paths under `--knowledge`; no directory scan). Current pin passed the ENV_CHANGED gate in every run, so no uncovered package input was found. REAL also hardcodes `counts_ok(so,0,1)` and `n_rows==5`, matching the sentence's `HELD=0 TWIN=1`.

### 8. Observation — RECHECK leg checks no stdout on refusal; registry-refusal legs check no append-file absence
Per predicate, only the recheck refusal pins file absence (renumber.tsv/append.md) — case_recheck checks both ✓. Registry-refusal legs check only `renumber.tsv` absence (c1-count.py:276), which matches the sentence (no file clause on registry refusal). `case_recheck` exercises both held-on (on=held) and twin-on (on=twin) placements across runs ✓.

## Residual risk / gaps
- The counter cannot falsify the no-date/non-NNd refusal arm (finding 1) — the largest gap; REGRESS offers no backstop.
- `--per-leg` has no floor (finding 2); `counts_ok` is token-anywhere (finding 3); ORDER is substring-coupled (finding 4).
- `expect()` vs `url_of` agree on all reachable spellings ✓; fixed REGRESS seed is deterministic ✓ (as frozen).

VERDICT: attacked the frozen C1 counter leg-by-leg; found one high (RECHECK never exercises the no-date/NNd arm — a predicate-violating tool scores LEGS=8/8 C1=PASS), two medium (per-leg 0 vacuous PASS; counts_ok token-anywhere; ORDER substring fragility), and confirmed the rest faithful to the sentence on the reachable space.
