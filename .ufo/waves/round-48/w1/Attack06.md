# Attack06 — round 48 wave 1: precision class #6 held-out probe (correct bullets, refusal rate)

seat: L1Chousa48.Attack06 (critic, leaf) · 2026-10-25 · item: construct 2 distinct correctly-reasoned held-out Inference bullets for precision class #6 (varied scope, negator distance, unlisted absence words, neighbouring-word binding); run the current `tools/inference-ground.py` on scratch copies over committed local fixtures; state whether each correct bullet is refused and why; no reuse of round-47 held-out text; probe only, no frozen fixture/claim; no network.

## 1. Environment (measured)

- Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`; HEAD `d4e6ef09b755a961bdae56566a7dcf0c9db0cfd7` (`git rev-parse HEAD`).
- Tool: `tools/inference-ground.py` sha256 `9d789b34562cc0ce35be7e4d7ea67a9fa57eabf8794bbf096c8a8d190925149b`; `git status --porcelain -- tools/inference-ground.py corpus/fixtures/inference-ground-r47` prints nothing (tool and fixtures clean).
- Fixtures (used verbatim, committed): `corpus/fixtures/inference-ground-r47/spans.tsv` (S901, S902), `spans/S901-1.txt` = `the release ships a frozen pool of pages; no revision is recorded per sentence`, `spans/S902-1.txt` = `the archived copy is dated at build time; a placeholder value is not an archive link`, `counts.json` (unused by these bullets: no figure tokens).
- No installs, no network, no lane files modified; scratch `/tmp/chousa-r48-Attack06/` removed at close.

## 2. Probe A6-1 — unlisted absence word (`nonexistent`) + listed negator beyond the window

Entry: `/tmp/chousa-r48-Attack06/A6-1.md` (sha256 `098d508fa60fda1d47ed12a3aa1a788e51a79f0dc908315478743c81d54b282d`). One `#### Inference` bullet:

> Since `no revision is recorded`, the release can only show a nonexistent revision log, and nothing in the chart will ever help a later editor recover the missing per-sentence changes (`S901`).

- Which phrase: `no revision is recorded` (S901; in-phrase negator `no` → negated, scope stems {`revis`, `recor`}, `inference-ground.py:283-296`).
- Correctness: the span says no per-sentence revision is recorded; the bullet reasons the release shows a nonexistent revision log and nothing recovers the per-sentence changes. Affirms only what the span asserts; no flip.

Command + observed output:

```
$ python3 tools/inference-ground.py --entry /tmp/chousa-r48-Attack06/A6-1.md \
    --spans corpus/fixtures/inference-ground-r47/spans.tsv \
    --counts corpus/fixtures/inference-ground-r47/counts.json
GROUND entry=A6-1.md section=1 bullets=1 tokens=1 grounded=1
FINDING INF_POLARITY_FLIP bullet=1 token='no revision is recorded / revision'
GROUND: FAIL
EXIT=1
```

Verdict: **refused (false refusal)**. Mechanism: P1 (`polarity_flips`, `inference-ground.py:317-348`) — the bullet restates the negated phrase's stem `revision` outside the quote; the window 3-before/2-after (`inference-ground.py:333-335`) contains no negator. `nonexistent` is an unlisted absence word: it is not in `NEG_WORDS` (`:236-237`) nor `IMPLICIT_NEG` (`:255-257`), and `UN_NEG_RE` (`:258-259`) matches only `un…` forms, not `non-…`. The listed negator `nothing` (`:256`) sits at word 11+, outside the window. This is exactly the routed-defect-1 class (`nonexistent`-type unlisted absence words); the bullet is correct and is refused.

## 3. Probe A6-2 — neighbouring-word binding + varied scope (affirmed phrase, negator scoping another noun)

Entry: `/tmp/chousa-r48-Attack06/A6-2.md` (sha256 `80bebf556622d8d5146e0f15e2643e30aae6951b1200e748bad86575db61905a`). Bullet:

> Since `the archived copy is dated at build`, that date marks the copy, not the build event (`S902`).

- Which phrase: `the archived copy is dated at build` (S902; affirmed — no negator inside or in the 3 preceding span words; scope stems {`archi`, `copy`, `date`, `buil`}).
- Correctness: the span affirms the archived copy is dated at build; the bullet adds that the date marks the copy, not the build event — the negator `not` scopes the neighbouring noun *event*, not the established build date. Same construction class as wave-2 `a05` (judged correct there), with new wording.

Command + observed output:

```
$ python3 tools/inference-ground.py --entry /tmp/chousa-r48-Attack06/A6-2.md \
    --spans corpus/fixtures/inference-ground-r47/spans.tsv \
    --counts corpus/fixtures/inference-ground-r47/counts.json
GROUND entry=A6-2.md section=1 bullets=1 tokens=1 grounded=1
FINDING INF_POLARITY_FLIP bullet=1 token='the archived copy is dated at build / build'
GROUND: FAIL
EXIT=1
```

Verdict: **refused (false refusal)**. Mechanism: P2 (`:336-338`) — the bullet's own `not` lands in the 3 words before the scope stem `build` (`not the build event`), so the probe binds the neighbouring negator to a stem it does not govern. `build` is in the phrase's scope set because it is a content word of the quote; the negation semantically targets the separate *event* noun. Same windowed lexical binding as `a05`, new text.

## 4. Class #6 coverage of the four named dimensions

| dimension | exercised by | observed |
|---|---|---|
| unlisted absence words | A6-1 (`nonexistent`, `non-` prefix) | not counted as a negator → P1 fires |
| negator distance | A6-1 (`nothing` at word 11+ from `revision`) | listed negator outside 3/2 window → P1 fires |
| varied scope | A6-2 (`not` scopes *event*) | P2 refuses regardless of semantic scope |
| neighbouring-word binding | A6-2 (`not the build event`) | window binds `not` to `build` |

Result: 2/2 correct bullets refused, both `INF_POLARITY_FLIP`, both exit 1. No silent pass, no other finding code; both bullets grounded 1/1. This matches the round-47 measured trade (wave-1 9/10, wave-2 2/12) and extends it into the `non-` absence and neighbouring-binding corners with bullets not present in any round-47 held-out report.

## 5. Operational note (transparency)

A first draft of A6-2 wrote the phrase un-backticked; the tool then reported `INF_UNGROUNDED` (tokens=0). Grounding requires a backticked/double-quoted phrase (`grounding_tokens`, `:150-161`). The phrase was backticked and rerun; result above. This confirms the tool's fail-closed behaviour on ungrounded bullets, unrelated to polarity.

## 6. Probe conclusion (no code/fixture/claim change)

The current tool's rule-5 P1/P2 probe falsely refuses both correctly-reasoned bullets by design of the frozen predicate: it cannot read `non-` absence words and it reads windowed negators without semantic scope. As a probe, the smallest safe correction is documentation: add a false-positive sentence to the tool docstring's Named limit and the round-47 lesson naming (i) `nonexistent`-type unlisted absence words and (ii) negators bound to a neighbouring noun in the 3-before window (e.g. `not the build event`), both already anticipated by routed defect 1 and HeldOutA's corrected sentence. No predicate, counter, fixture, floor or target change; no installs; scratch removed.
