# R51CritForgeC2 — C2 counter, cheapest-pass attack (round 51, wave 1)

seat `R51CritForgeC2` (critic) · lane `chousa-shokunin` · base `9ec1751a24231e899ceea4688e21c8edf6046d35`
attacked `corpus/evidence/round51/c2-count.py` (frozen R51-C2). Package built only under
`/dev/shm/chousa-r51-R51CritForgeC2/root`, counted with `--root`; no lane file, index or jj
state touched. No tool installed. Scratch deleted at the end.

## Result — C2=PASS on boilerplate

`python3 corpus/evidence/round51/c2-count.py --root /dev/shm/chousa-r51-R51CritForgeC2/root`
exits 0 on a package whose whole evidence base is navigation/boilerplate: a running footer,
table column headers, two DOI lines, a Flash-plugin notice, a **docx container member name**
and a running header — with three identical manifest rows per id, one `char N` per row copied
out of the manifest, six invented `present` verdicts, and CJK inference bullets that assert
the negation of the quoted sentence.
```
ENTRIES=3/3
BOUND=7/7 (min 5) REFUSED=0
BOUND_IDS=S107,S108,S109,S110,S111,S112,S113
REF_ID_UNBOUND=0
NEW_GROUND=3/3
QUOTE_ROWS=21 ON_BOUND=21/21
SPAN_IDS=7/7 (min 3 each)
QUOTES_IN_SPAN=21/21
QUOTES_IN_ENTRY=21/21
QUOTES_IN_LESSON=21/21
QUOTE_SHORT=21/21
SPAN_CONTEXT=21/21
CAPTURE_BOUND=21/21
SUBSTANCE=PASS
ANCHOR_BOUND=7/7
INFERENCE_GROUNDED=3/3
QUARANTINE_VERDICTS=6/6 (S104,S105,S111,S112,S114,S120)
QUARANTINE_BLOCKED_ADOPTED=0
C2=PASS
```
The seven "quotes" (`.txt` form read as UTF-8, `text.find`, count in that form; all ≤160
chars and ≤25 whitespace words):

| id | quote | char | n |
|---|---|---|---|
| S107 | `124      日健教誌        第 32 巻    第2 号     2024 年` | 21168 | 1 |
| S108 | `記載のポイント例                                           より良い記載のポイント例` | 1101 | 1 |
| S109 / S110 | `DOI:10.12300/j.issn.1674-5817.2025.017` / `DOI:10.12300/j.issn.1674-5817.2024.109` | 121 / 134 | 1 |
| S111 | `此页面上的内容需要较新版本的 Adobe Flash Player。` | 142 | 1 |
| S112 | `word/document.xml` (docx ZIP member name; count 2, so not a "located quote") | 1817 | 2 |
| S113 | `60                       剱持・岡／日本保健医療行動科学会雑誌                            38（1），2023      60－69` | 0 | 1 |

The derivation tool refuses what the counter accepts: `build-spans.py --root .../root --check`
→ `refused S112: quote not exactly once in any form (3a8b45977cd111e45e3980a5.txt:2x,
3a8b45977cd111e45e3980a5.raw:0x)`, exit 1.

## Shortcut → refusing leg (harness `variants.py`, one clone per row)

| variant | C2 | refusing leg |
|---|---|---|
| V0 boilerplate quotes, 3 identical rows/id, 1 anchor, invented verdicts | **PASS** | none |
| V1 one shared 4-char quote `ting` for 2 of 3 rows of **every** id | **PASS** | none |
| V2 that 4-char quote for all 21 rows | FAIL | `SUBSTANCE` (`NO_SUBSTANTIVE_QUOTE longest=4` ×7), `INFERENCE_GROUNDED=0/3` |
| V3 false `refused-doc` line for a rich capture (JSTAGE has 検索式 ×8) | **PASS** (`BOUND=6 REFUSED=1`) | none |
| V4 10-cell registry row for the doc + `refused-doc` line | **PASS** (`BOUND=6 REFUSED=1`) | none |
| V5 `verdict: fabricated` then `verdict: present` for S120 | **PASS** (`BLOCKED=0`) | none |
| V6 / V6b `unverifiable` / `absent-as-written`, same bound container-only doc | FAIL / **PASS** | `QUARANTINE_BLOCKED_ADOPTED=1` / none |
| V7 stubbed root tools + 1-space quotes + uncited bullet | **PASS** | none (root substitution, not lane bytes) |
| V8 every manifest row attributes its span to one entry | **PASS** | none |
| V9 fabricated digests: full run / `--lane-only` | FAIL / **PASS** | `CAPTURE_BOUND=0/21` / `CAPTURE_BOUND=skipped` |

## What each shortcut proves, and the line that fails to stop it

1. **Boilerplate quotes.** Nothing tests that a quote carries the theme; the only floor is `quote-substance-check.py` (≥3 non-space, one ≥12 per id, span ≤ quote+162), which a footer and a plugin notice clear. Declared limit ("presence, not entailment") — but S112 goes further.
2. **A container member name is not a text quote.** The NIPH capture's `.txt` is the docx ZIP re-encoded (`PK\x03\x04…`, member names, no document text): `検索期間` is **0** in `.txt` and **0** in the `.raw` UTF-16LE decode, while it **is** in the payload (`word/document.xml` opened read-only: `True`). `c2-count.py:117-127` accepts any form whose file digest matches and `:211` only slices it, so the document can only be bound on container bytes; the honest verdict for S120 is `unverifiable`, which **blocks** (V6), while `present` (V0, false) or `absent-as-written` (V6b) pass.
3. **Three rows per id = one quote.** `per_id` (`:199`, required at `:212`) counts rows, not distinct quotes; V0 reuses one span file and one offset three times, and V1 fills two of three rows of all seven ids with one 4-char string. Only the ≥12-char floor stops full reuse (V2).
4. **Anchors.** `offsets` is built from the manifest itself (`:206-207`), so `ANCHOR_BOUND` compares an anchor cell with a number derived from the same row: it cannot fail once the manifest is accepted, one `char N` satisfies "at least one", and no independent location is proved.
5. **Refusal is a string match.** `:174-177` requires `len(r)==11` for `hits`, so a **malformed row** makes the document invisible and it counts as REFUSED (V4) though a lane row exists; `no_src` only forbids a `source:` line, so V3 refuses a capture carrying 検索式 ×8.
6. **`used-by` is a comma list** (`:168-170`) compared with the citing entries whose use is nominal, and the manifest's `entry` cell is free: V8 attributes all seven documents' spans to one entry and passes.
7. **Verdict lines are strings.** `:242-247` keeps the **last** line per id, so `fabricated` then `present` passes (V5). V0's six lines are invented; the register's own quotes are absent from every capture form (S104, S105 ×2, S111, S112 ×2, S114, S120 ×2 → count 0 in `.txt` and in `.raw` UTF-16LE), so `present` is false for all six.
8. **`--lane-only` prints PASS with `CAPTURE_BOUND=skipped`** (`:262`, with `ok` at `:268-272`): fabricated digests pass (V9), and the claims list `--lane-only` as a counting command.
9. **Both tool legs are `--root`-relative** (`:214-217`, `:224-234`): a stub in the root passes both (V7).
10. **CJK polarity is unchecked.** `words()` (`tools/inference-ground.py:256`) is Latin-only, so quoting `その日時，使用した検索式を同時に記録しておくこ` (JSTAGE `.txt`, char 10234, count 1) the bullet says `検索式を記録する必要はない`, and both `inference-ground` and the counter pass (`INFERENCE_GROUNDED=3/3`, C2=PASS).
11. **`--counts /dev/null` can false-FAIL.** A bullet grounded by the round's real counts passes (`--counts counts.json` rc=0) and is refused by the counter's `--counts /dev/null` (`INF_TOKEN_NOT_IN_SPAN`, rc=1 → `INFERENCE_GROUNDED=2/3`, C2=FAIL).
12. **Dead and unpinned bits.** `HELD` (`:81`) is an empty set; the register is read by absolute path with no digest pin, so an edit silently changes the sweep size frozen at 6; `NEW_GROUND` (`:181-186`) tests one occurrence of the term anywhere. `REF_ID_UNBOUND` cannot see a token whose id is bound to a *different* document: "The J-STAGE article (S109)" (staged S109 = JSTAGE, lane S109 = SLARC_A) leaves `REF_ID_UNBOUND=0`, C2=PASS.

## What the closure must spot-check by hand (the counter cannot)

- Does each quote state something about what a search record must carry, and is it the document the entry discusses? (V0's seven do not.)
- Are the three rows per id three *distinct* sentences at three distinct offsets, and is each inference bullet consistent with its quote? (CJK: never checked.)
- Is a `refused-doc` line a true refusal — no text form, or a capture that cannot carry the claim — and not a way to skip a hard document? NIPH and SinoMed are chrome/container only; that is the only defensible refusal and it must be named as such.
- Were the six register verdicts re-checked against the capture, and was `unverifiable` avoided only because it blocks?
- Do the entries carry the staged documents' findings at all? The counter never opens `/home/vgpnk/Projects/shokuknow/merge/chousa` (only `CACHE`/`REGISTER`, `:53-54`).

## Smallest safe corrections (for L1; not applied)

1. Refuse a form that is not a text extraction (`.txt` starting `PK\x03\x04` / `%PDF`) and treat
   a container-only capture as REFUSED, not bound.
2. Require ≥2 distinct `(offset, quote)` pairs per bound id and ≥12 non-space chars per row.
3. Compute `ANCHOR_BOUND` from the capture (`text.find(quote)`), not the manifest, one anchor per
   distinct quote.
4. Count registry rows by id regardless of width; a refused doc must have no row of any width and
   no capture carrying the entry's term.
5. Reject duplicate verdict lines; verify `present` against the capture form.
6. Make `--lane-only` exit non-zero (or print `C2=INCOMPLETE`).
7. Resolve both tools from `LANE` and pin their digests; pass the round's real `--counts`.
8. Add a CJK polarity check, or state that the inference leg is vacuous for CJK entries.

Impacted axis: C2 (depth, sourced) only — every shortcut lands on the binding/quote/verdict legs;
C1 and C3 were not exercised. Defects 2-9, 11, 12 are fixable in the counter; 1 and 10 are
declared limits of the lane's own tools that the Gate must carry.

VERDICT: built a 7/7-bound, C2=PASS package out of footers, column headers, DOI lines, a Flash
notice, a docx member name and one shared 4-char string — eleven of the twelve probes pass; only
full quote reuse, an honest `unverifiable` verdict and a full-run digest check refuse, so the
Gate must hand-judge entailment, refusal truth, quote distinctness and register verdicts.
