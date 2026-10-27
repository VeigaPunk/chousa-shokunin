# R57W1ReviewRecipe — recipe-bytes verification (R57-C2 freshness)

Seat: R57W1ReviewRecipe (reviewer, leaf). Lane: chousa-shokunin. Claim base 6656f077;
R57-C2 frozen c2f914c5; lane tip at dispatch f9736a39 (HEAD now e0e73e0f, post-dispatch).
Scope: verify the capture recipe bytes are faithful to the campaign so REPRODUCED verdicts
stay verifiable. Attack: name any recipe drift. No lane writes but this file; no fetches.

Files examined (read-only):
- tools/capture-fetch.py (CF, 200 ln) — lane L1 re-fetch tool
- corpus/evidence/round57/c2-count.py (C2, 247 ln) — frozen counter
- /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/quote-lint.py (QL, 965 ln) — campaign source

## 1. html_to_text — identical across CF / C2 / QL

All three carry the same 6 regexes in the same order with the same replacement strings.
AST statement count is 7 (=6 subs + return) in each; per-pattern comparison:

    pattern #1..#4 identical-to-quote-lint across all: True (×4)
    pattern #5 identical-to-quote-lint across all: False   <-- ONLY #5

pattern #5 source bytes (cat -A shows QL's literal NBSP as M-BM- = U+00A0):
- QL  L521:  s = re.sub(r"[ \tM-BM- ]+", " ", s)   # class holds literal U+00A0
- CF  L74:   s = re.sub(r"[ \t\xa0]+", " ", s)      # \xa0 escape  -> U+00A0
- C2  L116:  s = re.sub(r"[ \t\u00a0]+", " ", s)    # \u00a0 escape -> U+00A0

codepoints of QL class: [0x5b, 0x20, 0x5c, 0x74, 0xa0, 0x5d, 0x2b] = `[ \t<NBSP>]+`.
Python re parses `\xa0` and `\u00a0` to U+00A0, so all three compile the SAME character
class `[<sp><tab>U+00A0]`. Functional torture-test (style/script/comment/br/div/p tags,
`&nbsp;`, raw NBSP, tab, double-space) → output identical on all three:

    sample: ' hi w x\n\n a b c d\n '   (all three MATCH)

The `.pattern` strings differ only because the raw-string escape style differs; the regexes
and their order are identical. This is the expected "naming/context difference" class.

## 2. recipe_txt — CF == C2 (AST-identical); transformation == QL fetch recipe

AST-normalized (docstring-stripped) body: `recipe_txt capture-fetch == c2-count: True`.
Against QL fetch() (L462-512) the byte transformation is the same:
`%PDF-` → `pdftotext -layout`, return when non-blank; else UTF-8-decode and, only if the
HTML-detection regex matches, run html_to_text. Detection regex
`(?is)^\s*(?:<!doctype\s+html|<html[\s>]|<head[\s>]|<body[\s>])` present in all three
(CF L86, C2 L130, QL L509). Differences are operational, not recipe:
- pdftotext timeout 60s (QL L497) → 120s (CF L83-84, C2 L123). More lenient; identical
  output for any PDF extracting within 120s.
- QL catches TimeoutExpired → txt="" (L498-499); lane lets it raise (edge-case robustness).
- QL caches to disk / writes "pdf-extract-empty" fail marker / keeps the .pdf; lane writes
  tmp/r.pdf, unlinks, returns the string (cache + temp lifecycle, not transformation).
These do not touch the emitted text; REPRODUCED binds raw sha256, and the counter's
CONSISTENT check recomputes recipe_txt on the same bytes with the same 120s cap, so the
check is internally closed regardless.

## 3. UA string — byte-identical to campaign

    $ grep -A1 '^UA = ' quote-lint.py > ql.ua ; grep -A1 '^UA = ' capture-fetch.py > cf.ua
    $ diff ql.ua cf.ua && echo identical   →  UA IDENTICAL
Both are `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36`
(QL L57-58 == CF L53-54). The curl command is the campaign's verbatim
`curl -fsSL --compressed --max-time 15 -A <UA>` (QL L482-483 == CF L124-125); CF adds
`-w %{http_code}` (L125) solely to record http_code in the ledger — it does not change the
bytes fetched or the success rule (rc==0, 200-299, non-empty, CF L133-139; QL relies on
`-f`). Same 25s subprocess timeout both.

## 4. TMPDIR/scratch honouring + 3-attempt cap (CF)

- CF honours `$HYAKU_SCRATCH` (default /fast/scratch/hyaku) for ALL file IO — L183
  `scratch = Path(os.environ.get("HYAKU_SCRATCH", ...))/"chousa-r57"/"fetch"`; curl out/code
  L125-126, recipe tmp L144 (`tmp = scratch/"recipe"`), ledger staging L111
  (`scratch/"refetch.append"`). Docstring L24 documents it; never /tmp. `import tempfile`
  (L45) is vestigial — `grep -n 'tempfile\.' CF` → no call sites.
- C2 honours TMPDIR via `tempfile.TemporaryDirectory()` (C2 L197) for its recipe tempdir.
- 3-attempt cap: `MAX_ATTEMPTS = 3` (L54); main() counts existing refetch.tsv rows per
  (id,url) (L182) and skips when `n >= MAX_ATTEMPTS` (L192-193), numbering the next attempt
  n+1. Cap is cumulative across calls, keyed on (id,url). Header validated on read (L103-104).

## 5. pdftotext version — counter's env gate matches host

- C2 L56 `PDFTOTEXT = "pdftotext version 26.08.0"`, enforced at L169-170 (`env(...)` →
  `ENV_CHANGED pdftotext is not 26.08.0`, exit 2) before any verdict work.
- Host: `pdftotext -v` → `pdftotext version 26.08.0` (poppler). Match.

## Frozen-file integrity

- `git -C lane diff c2f914c5 -- corpus/evidence/round57/c2-count.py --stat` → empty
  (counter unchanged since its freeze commit).
- `git -C lane diff 6656f077 -- tools/capture-fetch.py --stat` → `new file mode 100755`
  (tool added this round; full 200-ln content reviewed above, recipe functions identical
  to the campaign's).
- No edits made to any frozen counter/tool (read-only inspection).

## Named deviations (recipe-drift assessment)

None that affect the byte transformation or verdict verifiability. The only deltas from
quote-lint.py are: (a) escape style of html_to_text pattern #5 (`\xa0`/`\u00a0` vs literal
NBSP) — semantically identical; (b) pdftotext timeout 60→120s + dropped TimeoutExpired
guard — operational; (c) `-w %{http_code}` on curl — ledger-only; (d) cache/temp-file
lifecycle — outside the recipe. Every REPRODUCED verdict remains verifiable.

## Residual risk / gaps

- pdftotext 60→120s divergence only bites a PDF whose extraction takes 61-120s; even then
  it affects DRIFTED-quote FLAG text, never the sha256-bound REPRODUCED class.
- I compared the three in-repo recipe copies; I did not re-run the frozen counters (left to
  the L1 / dedicated counter seats).

Scratch: `/fast/scratch/hyaku/chousa-r57/R57W1ReviewRecipe` held only extracted function
texts and UA snippets; removed on exit (trap). No installs/upgrades were needed (pacman
paused; nothing fetched; nothing written but this report).

VERDICT: attacked the capture recipe's fidelity (html_to_text/recipe_txt vs campaign
quote-lint, UA, curl flags, scratch/TMPDIR honouring, 3-attempt cap, pdftotext 26.08.0) —
the recipe is faithful, NO drift found; R57-C2 freshness verdicts remain verifiable.
