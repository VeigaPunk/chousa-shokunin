# Attack10 — precision class #10 held-out Inference probes (C1 false-refusal)

seat: L1Chousa48.Attack10 (critic, leaf) · 2026-10-25
item: 2 distinct correctly-reasoned held-out Inference bullets for precision class #10
(varied scope, negator distance, unlisted absence words, neighbouring-word binding);
committed fixture spans/counts only, current `tools/inference-ground.py` on scratch
copies; state refusal + mechanism; no R47 held-out text reused; probe, not a frozen
fixture/claim; no network.

## Tool and fixture state (measured)

- HEAD `d4e6ef0`; `tools/inference-ground.py` unmodified in working tree
  (`git status --porcelain tools/` empty), sha256 `9d789b34562cc0ce35be7e4d7ea67a9fa57eabf8794bbf096c8a8d190925149b`.
- Committed fixtures: `corpus/fixtures/inference-ground-r47/spans.tsv` (S901
  `the release ships a frozen pool` / `no revision is recorded`, S902 `the archived
  copy is dated at build`), spans `S901-1.txt` `S902-1.txt`, `counts.json`
  (7572/5959/1582). sha256: S901-1 `7c2aa321…`, S902-1 `c2184ca7…`, spans.tsv
  `38a536bd…`, counts.json `17fb165b…` (full hashes recorded in run log).
- Run shape (both probes): `python3 tools/inference-ground.py --entry <scratch>
  --spans corpus/fixtures/inference-ground-r47/spans.tsv --counts
  corpus/fixtures/inference-ground-r47/counts.json --root /tmp/chousa-r48-Attack10/probes`.
- Scratch: `/tmp/chousa-r48-Attack10/probes/` (bodies + `--json` findings); removed at close.

## Probe 1 (B1) — unlisted absence word, negated span phrase — REFUSED

Body `p1-nonexistent.md` (sha256 `5a4519a2…`):

> `no revision is recorded` per sentence, and this release's revision history is nonexistent (`S901`).

- Correct reasoning: the span records no per-sentence revision, so the release has no
  revision history (asserting absence, not presence).
- Refused: exit 1, `FINDING INF_POLARITY_FLIP bullet=1 token='no revision is recorded / revision'`.
- Mechanism: `no revision is recorded` carries an internal negator, so P1 scope =
  {revision, recorded}. The bullet restates stem `revis` in "revision history"; its
  absence word `nonexistent` is NOT a negator to the tool — it is absent from
  `IMPLICIT_NEG` (`tools/inference-ground.py:255-256`) and `UN_NEG_RE`
  (`:258-259`) only matches `un-` forms (`un…able/ible/ed/known/clear/sure`), not
  `non-` words. No listed negator in the 3-before/2-after window of `revision`
  (`polarity_flips` P1, `:317-348`), so P1 fires.

## Probe 2 (B2) — neighbouring-word binding, affirmed span phrase — REFUSED

Body `p4-neighbour-binding-build.md` (sha256 `75a30fed…`):

> `the archived copy is dated at build`, and a placeholder is not dated at build, so the placeholder is not the copy (`S902`).

- Correct reasoning: the span affirms the copy is dated at build; the "not" negates
  the placeholder (a different subject of the same sentence), not the copy — the
  bullet keeps the copy's dating affirmed.
- Refused: exit 1, three findings, all `INF_POLARITY_FLIP` with token
  `'the archived copy is dated at build / dated'`, `… / build'`, `… / copy'`.
- Mechanism: span phrase is affirmed, so P2 scans the bullet's unquoted words: `not`
  sits 3 words before affirmed content stems `dated` and `build`, and 2 before `copy`
  (in the 3-before window), so each is flagged as a flip (`polarity_flips` P2,
  `:343-347`). The tool has no clause/subject binding: it reads the window
  mechanically, so a negator that binds the placeholder is read as negating the copy
  phrase. Same over-refusal family as R47 `HeldOutA.md` a05, on a fresh construction
  and fixture (S902, stems dated/build/copy, "placeholder" binding).

## Distinctness and variety

- B1 vs B2: negated vs affirmed span phrase, P1 vs P2 mechanism, different span
  (S901 vs S902), different scope stems (revis vs dated/build/copy), different
  dimensions: B1 = unlisted absence word (non- form); B2 = neighbouring-word binding
  (negator in window, wrong subject). Neither quotes any R47 held-out body
  (p01–p06/a01–a06/hb01–hb12) verbatim.
- Both bullets are grounded (tokens=1 grounded=1, no `INF_TOKEN_NOT_IN_SPAN`) and cite
  `S901`/`S902`; both are correctly-reasoned and both are refused.

## Calibration controls (distance/binding sensitivity, not the deliverable)

- `p3-distant-negator.md`: `no revision is recorded`, so the pool cannot expose a revised
  sentence… — REPASSES (exit 0): `cannot` sits inside the 3-before window of `revised`,
  so P1 correctly suppresses. Confirms refusal is distance-sensitive, not blanket.
- `p2-neighbour-binding.md`: `the release ships a frozen pool`, although the release itself
  is not dated at build — PASSES: no scope stem falls in `not`'s window (dated/build
  are not S901 phrase stems). Confirms B2's refusal needs the affirmed phrase's own
  stem adjacent to the negator.

## Verdict

Current `tools/inference-ground.py` still refuses 2/2 correct held-out bullets of
precision class #10 (unlisted absence words; neighbouring-word binding). The measured
false-refusal trade carried from R47 (HeldOutA 2/12) is reproduced on fresh,
non-reused text; the class is not repaired in the current tool. No production file,
fixture, counter, git/jj index or other report modified; no network; no installs;
scratch `/tmp/chousa-r48-Attack10/` removed at close.
