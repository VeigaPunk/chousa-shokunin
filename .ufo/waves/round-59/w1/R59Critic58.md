# R59Critic58 — falsification of the round59 quarantine `absent` verdicts (calibration)

## Verdict
The frozen-claims file is still missing (see Blocker). I therefore attacked the only round59 verdict-path artifact committed in the lane: `corpus/evidence/round59/quarantine-verdict-lane.txt`, produced by `tools/quarantine-check.py`. It has **16 `absent` verdicts**. At least **three are false negatives** (S114, S108, S116), and S093 and S094 are suspect for the same reason as S116. The tool's `absent` is not calibrated. It can only say "the quote was not found in our text capture", yet it reports "not present in the local capture of the cited source". The register treats `payload-absent` as a fabrication-class defect. This is a false-positive-fabrication risk, not just a missed positive.

## Blocker (carried over, unchanged)
`/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round59/claims.md` does not exist. I checked on 2026-10-27 16:37 (-03).
- `corpus/evidence/round59/` holds `census-*`, `controls/c1-before.txt`, `quarantine-*` and `s101-open.txt`, and no `claims.md`.
- `git log --all -- .../claims.md` is empty.
- `find` under the fleet root for a newer `claims.md` finds nothing.
- I could not check any claim against frozen bytes. Every finding below is against the committed round59 evidence files, the committed `tools/quarantine-check.py`, the captures in `corpus/captures/`, and the register at `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`.
- Register sha256 is `5afe1810…4bad833`, matching `quarantine-digests.txt`.

## Counterexample 1 — S114: quote present in the raw capture, verdict `absent`
- Capture `corpus/captures/42bac8830527d6f1bb125c49.{raw,txt}`. The raw is HTML of 20142 bytes, but the derived `.txt` is only 1675 chars.
- The register quotes are `主题词： *评价研究;*研究报告;Meta分析;*清单;质量控制` and `学科分类号： R-05;R-37;R348.3;R916.3`.
- The `.raw` contains `<span class="cuhuise12a">主题词：<span class="huise"> *评价研究;*研究报告;Meta分析;*清单;质量控制 </span></span>` at offset ~9429.
- After the tag-strip, unescape and whitespace-removal fold, **both quotes are found in the raw** (my re-derivation printed `True` for both).
- The `.txt` text rendering dropped those fields. The checker never reads `.raw` for HTML, so it issues `absent` ("none of the 2 quarantined quote(s) is present in the local capture").
- Impact: a truthful quote is labelled absent because the text extraction is lossy.

## Counterexample 2 — S108: arXiv HTML math residue, 92/93 chars match
- Quote: `The claims are classified as Supported, Refuted or NotEnoughInfo by annotators achieving 0.6841 in Fleiss κ.`
- `b502d4c6a6ee023bee6f8531.txt` line 240 reads `…achieving 0.6841 in Fleiss κ \kappa .`
- The only difference is the LaTeX alt-text residue `\kappa` from MathML flattening. None of the eleven folds handles it, so the verdict is `absent`.
- Impact: this is a near-verbatim quote, not an absent one.

## Counterexample 3 — S116 (and likely S093, S094): two-column `pdftotext -layout` interleaving
- S116 captures a PDF (`capture_form` → `pdf-text`). `decide()` guards `binary-office` as unverifiable but gives `pdf-text` no guard.
- In `1c15b611118dee97e4105fcf.txt`, lines 154–157 hold `The objective of this task was to generate claims … from information extracted from Wikipedia. We` in the left column and `…diagram to illustrate the different levels of entity` in the right column on the same physical lines. The quote `We used the June 2017 Wikipedia dump` is split across lines as `We` / `used the June 2017 Wikipedia dump, processed`, with right-column text between. No fold can bridge that.
- Quote 1 (`…0.6841 in Fleiss κ (Fleiss, 1971)…`) is present in the capture at lines 25 and 71–73, again split across columns.
- S116 quote 3 (`in 31.75% of the claims more than one sentence was considered…`) is at line 61, followed by right-column text (`The 1992 Los Angeles riots,`), so the column split breaks the match.
- All three S116 quotes are genuinely in the document, yet the verdict is `absent` (none of 3).
- S093 and S094 show the same pattern. S093 line 28 is `are unsupported by the article body; (2) ∼30%    Cited source` and S094 line 16 is `…CFEVER comprises 30,012    2004 looking for business…`. My longest-prefix scan matched 66/99 and 53/75 characters before diverging on a column boundary. I did not read the PDFs themselves, so this is `[INFERENCE]` from capture text only. It matches the verified S116 mechanism.

## Positive-path calibration hole
All three of these defects can only produce `absent` or `unverifiable`. In the committed round59 verdict set there is **no `present` or `mixed` row** for the 24-row slice (0 present, 16 absent, 8 unverifiable). A checker that can never return `present` on the real slice has not had its positive path calibrated on real bytes. `controls/c1-before.txt` only records `C1=FAIL` (4/4 safe, 0/7 refusals), so it says nothing about verdict-path calibration.

## Impacted axes
- **calibration** (primary): `absent` is asserted with more confidence than the evidence supports.
- **operability**: the `absent` bucket needs a manual re-adjudication path.
- **depth**: not assessed. Of the 16 absent captures I checked at most five in detail, and not the Chinese or Japanese PDFs S111, S112, S104, S105.

## Smallest safe correction (findings only; no edits made)
1. `decide()` should downgrade `absent` to `unverifiable` (or a new `absent-in-extraction`) when the capture form is `pdf-text`, unless a column-robust match is also negative (for example per-column re-flow, or a word-bag over a sliding window).
2. For HTML captures, also run the folds against `tag-stripped .raw` when `.txt` is much shorter than raw (S114: 1675 chars vs 20142 bytes).
3. Add a fold to strip `\\[a-zA-Z]+` math alt-text residue (S108).
4. Add a positive control with a known-present quote in a two-column PDF capture and in a truncated-text HTML capture. Both should return `present`.
5. Until then, keep these verdicts out of any claim of "fabrication confirmed".

## Checks and cleanup
Reads only: `read`, bash and python text scans of lane files. No installs, no git writes, no scratch directory created, and nothing to remove. I made no edits to claims, counters or the register.
