# RerunCounterA — C1 falsify: re-derive the after value

## What was attacked

Independent re-derivation of the C1 after value: ran the frozen predicate counter
against `tools/quote-reopen.py verify` on the live lane tip, with a fresh receipt,
then audited the receipt for hidden mismatches, UNREACHABLE verdicts, and doubtful
page-window labels re-checked against the live S003 page.

## Preconditions (verified)

- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master` →
  `b18b3ec9d8a01f966dd81991615bac27df6d66a1`; `merge-base --is-ancestor
  30c9d24da1815e01e161ed2f52d5f951005cc2b8 master` → exit 0 (tip contains the
  landing commit).
- `sha256sum tools/quote-reopen.py` →
  `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea`
- `sha256sum corpus/evidence/round29/c1-count.py` →
  `cd50965032278c355f780d357c5672f14840fc218bb1b7dc4adaa6993b5c175d`
  (receipt field `counter_sha256` equals this — the frozen counter ran unmodified).

## The run (exact command from the assignment)

```
timeout 900 python3 corpus/evidence/round29/c1-count.py \
  --receipt .ufo/waves/round-29/falsify/RerunCounterA/receipt.json \
  -- python3 tools/quote-reopen.py verify
```

run from `/home/vgpnk/Projects/shokunin/chousa-shokunin`, finished in ~7 s wall
(counter-reported `wall_s=2.27`). Full stdout tail:

```
class absent-cross-attributed 4/4        class runtime-page-transpose 24/24
class absent-fabricated 4/4              class runtime-page-window 24/24
class absent-one-word-edit 4/4           class runtime-subspan 14/14
class absent-spliced 4/4                 class runtime-transpose 14/14
class absent-truncated-token 4/4         class too-long-true-text 3/3
class no-source-own-work-row 2/2         class verbatim-inline-markup 9/9
class no-source-unregistered-id 1/1      class verbatim-plain 3/3
class runtime-crossattr 14/14            class verbatim-typographic-apostrophe 2/2
seed=16442982337510174646 tool_exit=1 wall_s=2.27
QUOTE_REOPEN_MATCH=130/130
```

Counter exit code: **0**. Fresh seed `16442982337510174646` — not a replay of the
L1 seeds; new random subspans/transposes/page windows were drawn.

## Receipt audit (`.ufo/waves/round-29/falsify/RerunCounterA/receipt.json`)

- Schema `chousa-r29-c1-receipt/v1`, `match=130`, `total=130`,
  `predicate_holds=true`, `tool_exit=1`, `at=2026-10-23T01:50:29Z`.
- Mismatching cases (`match == false`): **none** — all 130 cases `verdict == label`.
- UNREACHABLE verdicts/labels: **none**. Verdict histogram: ABSENT 72, VERBATIM 52,
  TOO_LONG 3, NO_SOURCE 3 — every class ran and produced a definitive verdict.
- Case mix: 40 frozen fixture items, 42 fixture-derived runtime cases
  (14 subspan VERBATIM, 14 transpose ABSENT, 14 crossattr ABSENT), 48 page-sampled
  cases from 8 live sources S002/S003/S008/S013/S019/S020/S038/S044
  (24 window VERBATIM, 24 transpose ABSENT).

## Doubted page-window labels, re-checked live

Three S003 (hapgood.us SIFT post) windows looked fragile because they span
WordPress comment/pingback chrome. Re-fetched the live page and re-ran the
identical extract+`found` in a scratch script:

- `'Cook, PhD March 15, 2020 at 11:31 am [...]'` → present, boundary-clean. OK.
- `'reinforcing what we've been [...] Reply'` → present. OK. (`[...]` in the
  receipt is NFKC of literal `[…]` in the HTML — confirmed in raw markup.)
- `'original [...] Reply Authoritarian Regimes Could Exploit Cries of 'Deepfake'
  | TechieTrick'` → **no longer present** on a fetch ~5 min after the counter
  run. Root cause inspected in raw HTML: the pingback anchor's remote site title
  now reads `… ‘Deepfake’ | TechieTricks.com` (and a second pingback shows
  `… ‘Deepfake’ – SFB Brands`). The remote linked-site title changed between the
  counter's fetch and mine. This is ordinary live-page drift on a comment
  pingback, *not* a counter or tool defect: at counter-run time the counter's own
  two fetches plus the tool's third fetch all contained the string
  (`found(t1,w) and found(t2,w)` gate in `page_cases`, then tool VERBATIM).
  Residual implication: page-window cases on pages with mutable remote-rendered
  chrome are time-sensitive — a rerun minutes later could legitimately flip one
  to ABSENT. No action required for C1; noted as a reproducibility caveat.

No other label doubted: all 24 page-window labels are VERBATIM and the counter
required each window to be found in two independent fetches before emitting it.

## Verdict

**HOLDS.** Fresh-seed rerun on lane tip `b18b3ec` prints
`QUOTE_REOPEN_MATCH=130/130` with counter exit 0; receipt shows 0 mismatches, 0
UNREACHABLE, and audited doubtful labels are either confirmed present or
explained by post-run drift of the live page.

## Limits

- Third-party live pages can drift between fetches (observed once on S003); the
  predicate is a point-in-time measurement, and the receipt is the honest record.
- I audited the receipt and three windows by hand; I did not re-derive the frozen
  fixture labels (frozen by contract).
- No installs or updates were needed; stdlib `python3` only.
