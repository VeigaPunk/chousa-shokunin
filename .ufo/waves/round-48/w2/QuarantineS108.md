# QuarantineS108 — hand-check, register `chousa` S108 (lane S092)

Scope: re-verify the `payload-absent` verdict on chousa-register row S108 against the on-disk capture of
https://arxiv.org/html/1803.05355. No live fetch. Read-only; leaf member.

## Inputs

- Register row: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:49`
  `| `chousa` | round3 | S108 | `payload-absent` | https://arxiv.org/html/1803.05355 | `The claims are classified as
  Supported, Refuted or NotEnoughInfo by annotators achieving 0.6841 in Fleiss κ.` | cited source, companion URLs and
  local artifacts were all checked; the quote is in none of them |`
  Quote Q1 (verbatim, 108 chars): sha256 `6203e017c6c4ceb5e5fd7af49430d6879124c83555553f5386090f578a2fdb7e`.
- Lane binding: `corpus/SOURCES.md:102` binds id S092 to this URL (round-47 adoption; the register's per-lane S-number
  is not the lane id — URL is the join key).
- Capture: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/b502d4c6a6ee023bee6f8531.txt`
  — 70165 bytes, 69681 chars, sha256 `e5b57b4875727b969a646b06b0df748e0efc8796aa1eeabc7c7ce5a2f2c85ac5`
  (matches digest column in `corpus/evidence/round47/spans.tsv` for S092 and
  `corpus/evidence/round42/receipts/digests.txt:19`).
  Cache-key check: `printf 'https://arxiv.org/html/1803.05355' | sha256sum | cut -c1-24` → `b502d4c6a6ee023bee6f8531` ✓.
- Companion raw: `b502d4c6a6ee023bee6f8531.raw` — 202174 bytes, sha256
  `b77d86ce5b6cdaa8df7db2226f339961fbfd5dcdf3896b926e19f93a5a9cfc51`.

## Commands run (decisive output)

`re.finditer` over the decoded capture:

```
'Fleiss'      [2831, 6526, 6544, 18018, 18040, 41857, 41883]
'0.6841'      [2821, 6516, 18060]
'Supported , Refuted' [2760, 5566, 14861, 24249, 24361]
'Supported, Refuted'  []                <- literal form absent
'κ'           [2838, 6533, 18025, 18177]   'kappa' [2841, 6536, 18028, 18180]
'annotators achieving' [2800]           <- unique
exact raw substring of Q1 in .txt: False; in .raw: False
```

Span at chars [2731, 2848):

```
'The claims are classified as Supported , Refuted or NotEnoughInfo by annotators achieving 0.6841 in Fleiss κ \\kappa .'
```

Normalisation (drop `\kappa` TeX alt-text, collapse whitespace, remove space before `,`/`.`): the normalised span equals
Q1 character-for-character (`norm(span) == quote → True`).

Punctuation-stripped word-in-order walk from char 2731 (offsets into capture):

```
The 2731  claims 2735  are 2742  classified 2746  as 2757  Supported 2760  Refuted 2772  or 2780
NotEnoughInfo 2783  by 2797  annotators 2800  achieving 2811  0.6841 2821  in 2828  Fleiss 2831  κ 2838
```

All 16 content words occur in order inside one contiguous abstract sentence; the only deviations are render markup:
`Supported ,` (space before comma, chars 2760–2770) and `κ \kappa .` (LaTeX alt-text plus space before the period,
chars 2838–2848). Byte offsets where they differ: char 2731 → byte 2744; char 2848 → byte 2862; char 2797 → byte 2810.

Unique contiguous raw anchor: `by annotators achieving 0.6841 in Fleiss` at char 2797 (byte 2810), the sole occurrence
in the capture.

Local artifact cross-check: `corpus/knowledge/claim-support-test-r37-amendment-2026-10-23.md` (13074 bytes, sha256
`6f6839ae2a0269f0ce8ca291b622b5b4a427c65dd300105a77a9e260ece32fc4`) line 14 also carries the content —
`"Supported , Refuted or NotEnoughInfo by annotators achieving 0.6841 in Fleiss"` — i.e. the claim "the quote is in
none of them" fails on content even for the derived artifact; the literal string is absent there for the same
markup reason.

Corroborating, non-decisive: intro at char 5552 `...and classified as Supported , Refuted or NotEnoughInfo .`; §3 at
chars ≈17990–18080 `We calculated the Fleiss κ \kappa score Fleiss (1971) to be 0.6841 ...`.

## Verdict

- **Q1: `present`.** Every word of the register quote occurs in order in one contiguous abstract sentence at chars
  [2731, 2848) of capture `b502d4c6a6ee023bee6f8531.txt`; the capture span normalises to the quote exactly. The only
  deltas are arXiv HTML-render artifacts (`Supported ,` spacing; `\kappa` alt-text before `.`).
- Register row S108 (`payload-absent`, "the quote is in none of them") is a **false negative** — falsified. The
  mechanical exact-substring check misses because the literal `Supported,` and `κ.` never occur as written.
- This reproduces the round-47 W1 finding (`QuarReg108.md`) independently: same capture digest, same offsets
  (prior wave reported span [2731, 2848) and anchor at char 2797; both confirmed byte-for-byte).

## Residual risk / gaps

- If the acceptance predicate demands literal byte-exact matching with zero normalisation, Q1 would read
  `absent-as-written`; the substance, however, is fully present and the miss class is a known render-markup artifact
  (same class as rounds 43/46/47).
- Capture is the campaign cache, not a live read; whether the bytes match the current arXiv render is unchecked by
  design (no-fetch lane bound).
- The `Supported, Refuted` literal form is absent everywhere in the capture; only the spaced `Supported , Refuted`
  occurs (5 sites). No column-interleave or hyphen-split repair was needed (HTML render, not PDF).

## Tools / hygiene

- No installs or upgrades; no pacman transactions. Scratch `/tmp/chousa-r48-QuarantineS108/` deleted.
- Single write: this report. No production file, sibling lane, git/jj/index, or fleet repo touched.
