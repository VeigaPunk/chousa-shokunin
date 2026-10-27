# R54W2CritTrends — attacking the round-54 trend verdicts before filing

Rule source: `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md` §"The three trends" — `improved`/`harmed`/`unchanged`/`unprovable-but-better`, no scalars; discernment is checked from outside and "a subagent the lane dispatched is still the lane" (LEARNING.md:46). Round-53 precedent (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-53/chousa.md:51-53`): expansion `improved`, quality `improved narrowly`, discernment `unchanged pending non-author closure` — the closure then filed `discernment — improved` from its own agree table (`corpus/lessons/round-53-verifier-spotcheck.md:74`). Tip attacked: `178667d` (claims froze `5a1a206`; E1–E4 read).

## expansion — `improved` survives; the credit must read three documents / two entries

Evidence (ran or opened):
- Two admitted entries on ground absent at base: `git grep -l -e 'ISO 690:2021' -e '文献载体标识' c49ffc6 -- corpus/knowledge` → exit 1, no output (re-ran; matches README "Round54 coverage and frontier" and the frozen `NEW_GROUND` leg).
- `python3 corpus/evidence/round54/c2-count.py` at `178667d` → `BOUND=3/3 REFUSED=0 NEW_GROUND=2/2 QUOTE_ROWS=33 … CAPTURE_BOUND=33/33 ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=2/2 C2=PASS` (ran; PYTHONDONTWRITEBYTECODE=1).
- Each `source:` cites a `mined` row: r36 head carries `source: S121 — <samr url>` and `source: S122 — <openstd url>`; r37 carries `source: S123 — <jmu url>` (`corpus/knowledge/source-type-taxonomy-r36.md:2-3`, `:r37.md:2`). `corpus/SOURCES.md:131-133` tail cells read `mined | 2026-10-26 | 180d | corpus/knowledge/source-type-taxonomy-r3{6,7}.md` — one row per document, `used-by` naming exactly the citing entries.
- No admitted entry fails its admission bar: `python3 corpus/evidence/round54/build-spans.py --check` → `SPANS_ROWS=33 STALE=0`; `uv run --with pypdf python corpus/evidence/round54/pdf-crosscheck.py` → `PDF_QUOTES=21 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14` (QUALITY 96 leg; ran).
- New kinds of source: an authority record (S121), the same authority's service notice (S122), a third-party print reproduction (S123); the tier split is the frontier paragraph, not a stretch.
- S101 earns no credit: 0 occurrences of `S101` in either entry; `HELD_CITED=- HELD_BAD=0` in the counter run above. Any draft counting a fourth document or crediting S101 is wrong.

Flips: `unchanged` if a bound row loses `mined` or `used-by`, or entries cite unbound ids; `harmed` iff a round-54 admitted entry is shown failing the bar it was admitted under (e.g., an S123 quote absent from the sidecar, or the r36 归口 cross-page reading falsified). Named limit: LEARNING's wording is "uncovered ground"; theme C itself was partially held (S101's data specification cites GB/T 7714 in passing), but lane practice and the frozen claim count credit per document absent at base — a stricter protocol reading that counted only new *themes* would flip this to `unchanged`; that is a protocol question, not a lane call, and round-53 filed it the same way.

## quality — `improved` survives; file it as re-verification plus sharpening, never as entry supersession

Evidence (ran or opened):
- Corrections: nine round-49 anchors re-pointed into the defined OLE form. `python3 corpus/evidence/round53/pointer-anchor-check.py` → `ANCHORED=16/16 UNANCHORED=0 BAD=0` (ran — covers all nine new `correction:` lines, not just the seven round-53 ones). Spot-verified: `S101-text-form.txt` holds `为便于文献的统计和期刊评价` count 1 @11972 and `参考文献格式，参照ISO 690` count 1 @25123.
- Re-checks with verdicts: `QUARANTINE_VERDICTS=3/3 (S080,S088,S096)`; S096's round-42 `unverifiable` superseded by `absent-as-written` at a located offset (`corpus/lessons/round-54.md:57`) — nothing left unmarked.
- Entailment narrowing is evidenced, not asserted: r36's `ground:` and `#### Observation` keep the portal notice scoped to `本系统`; r37 records the 7.3 re-cut, the 普通图书 correction, normative-vs-informative appendices, and names 图书主要贵任者 an OCR slip rather than quoting it as the standard's text.
- QUALITY 97–100 (corpus/QUALITY.md :937,:939,:941,:943, read in full) each cite their lesson evidence, carry a runnable check and a ran shown-failure; 98 and 100 encode this round's counter legs, 97 the anchor mistake, 99 the wave-dispatch mistake.
- The OLE form's quality-trend role is derivative only: it made the corrections and the S096 re-verdict possible (`tools/capture-text.py` on the S130 raw → `是否检索灰色文献` count 1 @4678, 0 U+FFFD; ran). The operability gain itself is C1 and stays under the E1 cap (frozen counter forgeable; supplement is not the claim rule).

Flips: `unchanged` if a filed `correction:` fails `pointer-anchor-check`, or a QUALITY row lacks its lesson; `harmed` iff a corpus holding is found false/stale and left unmarked.
Residual attack the filing must survive: the S100/S101 row *cells* still print the stale offsets and the label "(UTF-16LE text of the raw `.doc` capture)" (`corpus/SOURCES.md:110-111`). Under the append-only convention the `correction:` section is the marking — the corrections section itself says the label "is superseded by these lines" — but QUALITY 97's check, read literally against the cells, flags them. A verdict sentence claiming the cells were fixed overclaims; the correct claim is "marked by nine anchored corrections." A non-author who reads only SOURCES.md could still register a disagreement; that is the known cost of append-only, disclosed here so it is a named limit, not a surprise.

## discernment — `unchanged (pending non-author closure)` is the only supported verdict

LEARNING.md:42-47 requires a non-author to spot-check at least one admit and one reject; every round-54 gate decision (two narrowed admits, the S101-leg refuse, the S130 refuse, the package-amendment non-landing, three quarantine verdicts) was made by W1 seats or the L1 — lane-dispatched, therefore lane. `harmed` is also unsupported: round-53's outside check recorded agree ×6 / disagree ×0 (`round-53-verifier-spotcheck.md:61-66`), so there is no live disagreement left unlearned, and all four new criteria cite a lesson. `unprovable-but-better` is foreclosed — it needs a named non-author reviewer on record.

What the lane may claim: `discernment — unchanged`; and, as evidence not verdict, that a checkable sample is prepared and verified — I ran its items: S121 `本标准非等效采用ISO国际标准：ISO 690:2021。` count 1 @1797; S123 `本文件不适用于图书馆员…` count 1 @5602; S130 reject leg `是否检索灰色文献` count 1 @4678 in the defined OLE form (all ran). Flip: to `improved` only inside the closure's own verdict after non-author agreement on ≥1 admit + ≥1 reject (the round-53 pattern); to `harmed` if a disagreement arrives and the lane files no lesson/criterion for it.

Watch item for the final filing: QUALITY 99 binds every "dispatched" sentence to the marker/results file at the report's own commit — `w1.ready.dispatched` exists only from `178667d` onward (`git show --stat 178667d`), so a report section written against an earlier tree must re-check before it calls W1 dispatched.

## Not re-run

`c1-count.py` full and `c1-supplement.py` (heavy; `corpus/evidence/round54/measure-after.txt` at tool sha `2c0140bc…` shows `LEGS=6/6 C1=PASS` on three unseeded runs and `--seed 7`). All trend findings above rest on checks I ran or files I opened.

VERDICT: attacked the round-54 trend set — expansion `improved` survives (three documents, S101 zero credit), quality `improved` survives (corrections marked append-only, criteria lesson-grounded), discernment survives only as `unchanged pending non-author closure`; any lane filing of `improved`/`harmed`/`unprovable-but-better` for discernment is unsupported by this evidence.
