# Attack12 — precision class #12: two correct held-out Inference bullets, current-tool refusal

seat: L1Chousa48.Attack12 (scout, leaf) · 2026-10-25 · item: construct 2 distinct correctly-reasoned held-out Inference bullet examples for precision class #12 (varied scope, negator distance, unlisted absence words, neighbouring-word binding); use only committed local fixture spans/counts; run current `tools/inference-ground.py` on scratch copies; state whether each correct bullet is refused and why; do not reuse round-47 held-out text; probe, not a frozen fixture or claim; no network.

## 1. Grounding used (committed only)

- `corpus/fixtures/inference-ground-r47/spans.tsv` rows: S901 (`spans/S901-1.txt` = `the release ships a frozen pool of pages; no revision is recorded per sentence`), S902 (`spans/S902-1.txt` = `the archived copy is dated at build time; a placeholder value is not an archive link`).
- `corpus/fixtures/inference-ground-r47/counts.json` (`answers_named_source` 7,572, `answers_archived` 5,959, `answers_without_archive_key` 1,582) passed via `--counts`; my probes exercise span-phrase grounding only — the figure leg is unused (noted so the pool stays comparable).
- Tool: lane HEAD `d4e6ef09b755a961bdae56566a7dcf0c9db0cfd7`; `tools/inference-ground.py` unmodified (clean in `git status`), sha256 `9d789b34562cc0ce35be7e4d7ea67a9fa57eabf8794bbf096c8a8d190925149b`.
- No installs, no network, no lane files modified; scratch `/tmp/chousa-r48-Attack12/` removed at close (report writes only `.ufo/waves/round-48/w1/Attack12.md`).

## 2. Probe a12-a — S901 negated phrase `no revision is recorded` (correct reasoning)

Bullet (entry `/tmp/chousa-r48-Attack12/bodies/a12-a.md`, one `#### Inference` bullet):

> Per the span (`S901`), `no revision is recorded`; the revision trail that would support sentence-level dating is nonexistent here.

Reasoning is correct: the span states no per-sentence revision is recorded, so no per-sentence revision trail exists. A: `revision trail` / `sentence-level dating` (varied scope: the stem `recor` is never reused; `revis` reused once as a noun, not as the quoted verb), absence expressed by `nonexistent` (unlisted absence word), and no literal negator anywhere in the prose (negator distance: the only `no` lives inside the stripped backtick quote).

Run (from lane root):

```
$ python3 tools/inference-ground.py --entry /tmp/chousa-r48-Attack12/bodies/a12-a.md --spans corpus/fixtures/inference-ground-r47/spans.tsv --counts corpus/fixtures/inference-ground-r47/counts.json --root /tmp/chousa-r48-Attack12
GROUND entry=bodies/a12-a.md section=1 bullets=1 tokens=1 grounded=1
FINDING INF_POLARITY_FLIP bullet=1 token='no revision is recorded / revision'
GROUND: FAIL
exit=1
```

**Refused — yes.** Why: P1 (`tools/inference-ground.py:341-345`) — the span negates the phrase (`no` inside the phrase; scope words `revision`, `recorded`, stems `{revis, recor}`, `:291-296`), and the bullet's unquoted `revision` reuses stem `revis` with no negator in its 3-before/2-after window. The absence word `nonexistent` is in no lexicon: it is not in `NEG_WORDS` (`:236-237`), not in `IMPLICIT_NEG` (`:255-257`), and `UN_NEG_RE` (`:258-259`) matches `un-` forms only, not `non-`. So the tool reads the sentence as affirmative and refuses a correct bullet.

Control a12-a-ctrl (same facts, listed `no` inside the window before `revision`: "... there is no revision trail that would support sentence-level dating here") → `GROUND: PASS exit=0`. The refusal is therefore caused by the unlisted absence word + window, not by the semantics.

## 3. Probe a12-b — S902 affirmed phrase `the archived copy is dated at build` (correct reasoning)

Bullet (entry `/tmp/chousa-r48-Attack12/bodies/a12-b.md`):

> Since `the archived copy is dated at build`, a later retrieval does not rewrite that build stamp (`S902`).

Reasoning is correct: the copy is dated at build time, so retrieving it later does not rewrite that stamp. The negator `not` binds `rewrite` (neighbouring-word binding), not `build`; `build` is reused in `build stamp` while `archived/copy/dated` are reused only inside the quote (varied scope).

Run:

```
$ python3 tools/inference-ground.py --entry /tmp/chousa-r48-Attack12/bodies/a12-b.md --spans corpus/fixtures/inference-ground-r47/spans.tsv --counts corpus/fixtures/inference-ground-r47/counts.json --root /tmp/chousa-r48-Attack12
GROUND entry=bodies/a12-b.md section=1 bullets=1 tokens=1 grounded=1
FINDING INF_POLARITY_FLIP bullet=1 token='the archived copy is dated at build / build'
GROUND: FAIL
exit=1
```

**Refused — yes.** Why: P2 (`:346`) — the span does not negate the phrase (no negator before `the archived copy...` in the span; `:295-296`), and the bullet places a negator (`not`) within the 3 words before the scope stem `build` (`does not rewrite` → window `[does, not, rewrite]`). The negator's semantic target is `rewrite`, not `build`; the tool has no binding analysis — any negator in the window flags the stem. (P2's `un`-prefixed branch is not involved.)

Control a12-b-ctrl (same facts, no near-stem negator: "... a later retrieval leaves that build stamp fixed") → `GROUND: PASS exit=0`. The refusal is positional only.

Method note: an initial draft with a capitalized quote (`The archived copy...`) failed grounding (`INF_TOKEN_NOT_IN_SPAN`, `exit=1`) because token grounding is a case-sensitive substring (`tok in s`, `:487`); the bullet was corrected to the verbatim lowercase span text. Observed, not a defect.

## 4. Verdict

- Both correct bullets are refused; refusal rate 2/2 on this class-12 sample, both `INF_POLARITY_FLIP`. The four traits named for the class are covered: varied scope (A: `revision trail` noun reuse vs quoted verb; B: quote-only reuse of `archived/copy/dated`), negator distance (A: no prose negator at all; B: `not` in-window but 2 words away from its real target), unlisted absence words (A: `nonexistent`), neighbouring-word binding (B: `not` binds `rewrite`, flags `build`).
- This reproduces, with fresh text, the R47 measured false-refusal trade (`LabC1FalsePos` 9/10, `HeldOutA` 2/12, `HeldOutB` survivors) on two previously unused constructions, and it is the same trade the R47 lesson's routed defect 1 names (docstring Named-limit coverage for unlisted absence words and negator windows).
- Probe status: these are scratch entries under `/tmp`, not committed fixtures, no claim or predicate proposed. Nothing frozen.
- No installs, no network, nothing else written.
