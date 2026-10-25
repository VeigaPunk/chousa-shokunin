# Attack09 — C1 precision probe, class #9 (executor, leaf; no subagent)

seat: `L1Chousa48.Attack09` · lane HEAD `d4e6ef09b755a961bdae56566a7dcf0c9db0cfd7` · tool `tools/inference-ground.py` sha256 `9d789b34562cc0ce35be7e4d7ea67a9fa57eabf8794bbf096c8a8d190925149b`
item: construct 2 distinct correctly-reasoned held-out Inference bullets for precision class #9 (varied scope, negator distance, unlisted absence words, neighbouring-word binding); run current tool on scratch copies; report whether each is refused and why; no round-47 held-out text reuse; probe only.
installs: none · network: none · scratch `/tmp/chousa-r48-Attack09/` removed at close · lane writes: this report only.

## 0. Class-definition note (measured)
No taxonomy file enumerating classes #1–#12 exists in the repo (searched `.ufo/waves/round-48/*`, `w1-spec.json` items, round-47 w1/w2 reports, `SCORECARD.md`). The w1 spec gives every probe seat the same four-axis description. Interpreted here as [INFERENCE]: each probe seat partitions the documented C1 false-refusal axes (`round-47-verifier-spotcheck.md:62`, `HeldOutA.md:30-31`, `LabC1FalsePos.md:69-76`); class #9 is taken as the negation-side false-refusal complex, and the two bullets below are chosen to sit in distinct members of it.

## 1. Method
Committed-only local material: `corpus/fixtures/inference-ground-r47/spans.tsv` + `spans/S901-1.txt`, `S902-1.txt` + `counts.json` copied verbatim to scratch. Each body = one `#### Inference` bullet, one cited source id, one grounding token (a quoted span phrase or a counts figure). Ran:

```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
python3 tools/inference-ground.py --entry <scratch>/bodyN.md \
  --spans <scratch>/spans.tsv --counts <scratch>/counts.json --root <scratch>
```

## 2. Bullet 1 — phrase leg, correct absence reasoning (unlisted absence word; varied noun scope; neighbouring-word binding)
Body `body1.md` (scratch):
```
- Since the span states `no revision is recorded` per sentence, the corpus is
  devoid of any record of sentence-level revision (`S901`).
```
Observation: `no revision is recorded` (S901-1) is a NEGATED phrase (negator inside). Content after negator → scope stems {`revis`, `recor`}. The bullet reasons correctly: no per-sentence revision recorded ⇒ corpus devoid of sentence-level revision records.
**Result: REFUSED — exit 1.**
```
GROUND entry=body1.md section=1 bullets=1 tokens=1 grounded=1
FINDING INF_POLARITY_FLIP bullet=1 token='no revision is recorded / revision'
GROUND: FAIL
```
Why refused (tool `polarity_flips`, P1, `inference-ground.py:317-348`): the bullet restates the negated phrase's scope noun `revision` (stem `revis`) with no recognized negator in its 3-before/2-after window (`:344-346`). `devoid` IS in `IMPLICIT_NEG` (`:255-257`) and clears the adjacent `record` occurrence, but it sits outside `revision`'s window (`devoid of any record of sentence-level revision` → 6+ words earlier), so the tool reads `revision` as affirmed and refuses. Calibration: the bullet is semantically identical in polarity to the landed positive `positive-negation-kept.md` (`a revision cannot be traced…`), which passes only because its `cannot` sits 2 words after `revision`.

## 3. Bullet 2 — figure leg, correct keyless reasoning (unlisted absence word; counts-key binding)
Body `body2.md` (scratch):
```
- 1,582 sourced answers are keyless, so their citations stay unbound (`S902`).
```
Observation: in `counts.json`, 1,582 is carried by key `figures/answers_without_archive_key` — a NEGATED key (`without` ∈ `NEG_KEY_PARTS`, `:238`; leaf-derived, `key_negated` `:389-397`). The bullet reasons correctly: answers without an archive key are keyless; their citations are unbound. No listed negator follows the figure (correct — the sentence expresses absence with `keyless`/`unbound`, neither listed).
**Result: REFUSED — exit 1.**
```
GROUND entry=body2.md section=1 bullets=1 tokens=1 grounded=1
FINDING INF_POLARITY_FLIP bullet=1 token='1,582 / counts key figures/answers_without_archive_key'
GROUND: FAIL
```
Why refused (`figure_flip` P3, `:400-415`): a figure grounded solely by a negated key must be followed by a listed negator in the next 4 words (`:412`). Next 4 words = `sourced answers are keyless`; `keyless`/`unbound` are unlisted absence forms (neither in `NEG_WORDS`/`IMPLICIT_NEG`, nor `UN_NEG_RE`, which matches only `un…ed/able/ible/known/clear/sure` — `unbound` fails the suffix group). So the tool demands a negator that the correct sentence does not need, and refuses.

## 4. Verdict
Both probes are genuine **false refusals** (correct, held-out, freshly worded bullets killed by `INF_POLARITY_FLIP`). They are distinct members of the class: phrase-leg unlisted-absence + varied noun scope + window distance (bullet 1) vs figure-leg unlisted-absence + negated-counts-key binding (bullet 2). No round-47 held-out body text was reused; the only shared text is the committed ground phrases/figures themselves (`no revision is recorded`, `1,582`, which the fixtures require as grounding tokens).

Axes covered: **varied scope** (noun `revision` vs figure-bearing clause; phrase leg vs figure leg) — bullet 1; **negator distance** (`devoid` beyond `revision`'s window) — bullet 1; **unlisted absence words** (`keyless`, `unbound`; `devoid` only partially) — both; **neighbouring-word binding** (3-before/2-after vs next-4 windows) — both.

## 5. Commands run (decisive output above)
`git rev-parse HEAD`; `sha256sum tools/inference-ground.py`; two × `python3 tools/inference-ground.py --entry <scratch>/bodyN.md --spans <scratch>/spans.tsv --counts <scratch>/counts.json --root <scratch>` (exit 1 both). Scratch `/tmp/chousa-r48-Attack09/` removed at close.

## 6. Risks / blockers
- Class #9 has no repo definition; seat-level interpretation flagged above. If a taxonomy exists elsewhere it is not in this lane; this probe stands on the measured behavior regardless.
- Bullet 1's `devoid` partially fires the implicit-negator list, so refusal is caused by the *other* scope occurrence — mechanism reported exactly as observed.
- No blockers. No tool changes proposed (probe only).
