# ScribeLessonGate — round 40, wave 1 (scribe)

Seat: chousa round-40 leaf L2. Assigned attack: review the `round-40.md`
`## Gate` for every new SOURCES row's URL or own-work locator, access date,
located quote under 25 words, and complete old-to-new registry changes.

Pins used: lane HEAD `6bc90e0` (non-author spot-check), subject Gate commit
`282dc76` (`round-40: record committed measurements and lesson`; the Gate file
is unchanged from `282dc76` to HEAD), round baseline `691d264`.

Method: read-only against committed lane artifacts; no external fetch, no
production edit, no index/jj operation. The only file written is this report.
`tools/quote-reopen.py` was imported and its own `html_to_text`/`norm`/`found`
functions were exercised against the committed 2026-10-23 page capture; the
tool's live `verify` subcommand (which fetches) was not run.

## Axes walked

1. Provenance completeness — URL/locator, access date, registry delta.
2. Quote fidelity — verbatim span, ≤25 words, printed exactly as quoted.
3. Registry diff integrity — old→new exactness, "only change" claims.
4. Calibration — severity, and whether unobserved claims were upgraded.

## Verdict

**Gate holds on all four requested checks.** Exactly one new registry row
(S074) exists; its URL, access date, reason, flip condition and `used-by=—` are
present and match the committed row. S059's only committed cell change is
`used-by`, and the Gate prints both old and new values exactly. The located
quote is 13 words (limit 25) and is verbatim in the anchored paragraph of the
committed page capture.

Five findings (one P2, four P3), none falsifying a Gate claim about committed
bytes:

- **F1 (P3, precision):** the quote is printed with a sentence-final period that
  is not part of the anchored span; the gate tool's own matcher returns ABSENT
  for the string exactly as printed and VERBATIM without the period.
- **F2 (P3, completeness):** the registry-change inventory covers the table but
  omits the committed `## Paths` bullet (`corpus/SOURCES.md:106`) and does not
  record that a `## Search log` entry was appended (`:109`).
- **F3 (P3, precision):** "same URL and anchor" for S074 is true of the URL but
  the two anchor cells are not identical text (both resolve to the same
  paragraph; the duplicate verdict is unaffected).
- **F4 (P3, currency):** Gate `:51` still says the non-author spot-check is
  pending; at HEAD a non-author spot-check with 4/4 agreement is committed as
  `6bc90e0`. True at authoring commit `282dc76`, stale at HEAD; r39 precedent is
  identical (`corpus/lessons/round-39.md:69`).
- **F5 (P2, procedure):** no `tools/quote-reopen.py` receipt exists for the newly
  located Gate quote (QUALITY criteria 25/30), and no round-40 page capture was
  committed. Substance is corroborated (see Holds), but the named artifact is
  absent.

## Checklist

| Check | S059 (re-opened) | S074 (new row) | Verdict |
|---|---|---|---|
| URL / own-work locator | row `:69` URL `https://docs.python.org/3/library/hashlib.html`; Gate `:40` same page plus `#hash-algorithms` | row `:84` and Gate `:41` both `https://docs.python.org/3/library/hashlib.html`; row is `kind=docs`, so no own-work locator required | HOLD |
| Access date | Gate `:40` `accessed 2026-10-24`; row `opened` stays `2026-10-23` (first-open); 2026-10-24 recorded at `SOURCES.md:109` and note `:2` (`verified-at`) | row `opened=2026-10-24` and anchor cell "opened 2026-10-24"; Gate `:41` `accessed 2026-10-24` | HOLD (asymmetry is the lane's r39 S071 convention, see F2) |
| Located quote <25 words | 13 words, verbatim in the anchored paragraph of the pinned capture | Gate `:41` "the same 13-word quote was located" (by reference; same page and paragraph) | HOLD; F1 period precision |
| old→new registry changes | `used-by` only; old and new strings printed exactly and match the committed cell | new tier-A `rejected`, `used-by=—`, reason + flip printed and matched | HOLD for the table; F2 for file-level delta |

## Exact commands and observed output

1. Registry delta, entire round:
   `git diff 691d264 -- corpus/SOURCES.md` →
   `1 file changed, 4 insertions(+), 1 deletion(-)`; hunks = S059 row replacement,
   S074 row addition, one `## Paths` bullet, one `## Search log` entry. No row
   deleted, no other row touched.
2. Field-level old→new (python, `git show 691d264:corpus/SOURCES.md` vs
   `corpus/SOURCES.md`) →
   `S059 changed fields: ['used-by']`
   `old used-by = corpus/knowledge/revision-binding-r31.md`
   `new used-by = corpus/knowledge/revision-binding-r31.md, corpus/knowledge/receipt-expectation-digests-r40.md`
   All ten other S059 cells byte-identical (`status=mined`, `opened=2026-10-23`,
   `recheck=on-release`).
3. S074 cells as committed →
   ``['S074', 'Python 3.15.1 documentation, `hashlib` — https://docs.python.org/3/library/hashlib.html', 'docs', 'A', 'duplicate row proposal …', '“Hash algorithms” section, paragraph beginning “There is one constructor method named for each type of hash”; Python 3.15.1, opened 2026-10-24', 'REJECTED: … flip: …', 'rejected', '2026-10-24', 'on-release', '—']``.
4. Row census, old → new: `73 → 74`; tier `A 67→68, B 1→1, C 5→5`; status
   `mined 50→50, queued 19→19, rejected 4→5`. Matches `round-40.md` "Sources
   census" exactly; the only added row is S074.
5. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`
   → exit 0, exactly four W04 lines (S051, S053, S073 pre-existing; S074 new
   duplicate URL) and `chousa ok …/corpus/SOURCES.md`. Matches the lesson's
   round-end output byte-for-byte.
6. Quote length: `printf 'the digest of the concatenation of the data fed to it so far' | wc -w`
   → `13`. Tool limit is `MAX_WORDS = 25` (`tools/quote-reopen.py:61`), so
   13 < 25 holds.
7. Quote location, using the gate tool's own extractor and normalizer (same
   normalization its fetch path applies at `tools/quote-reopen.py:434`) on
   `.ufo/waves/round-31/build/ScribeSrcHashlib/response.body`:
   `gate_as_printed_with_period words=13 found=False`;
   `gate_span_no_period words=13 found=True`;
   `spotcheck_variant words=12 found=True`;
   context: `… ask it for the digest of the concatenation of the data fed to it so far using t…`.
   Raw HTML splits the sentence across a newline and `<em class="dfn">digest</em>`
   (`response.body:258`), so only normalized matching finds it; `<h2>Hash algorithms`
   with `href="#hash-algorithms"` immediately precedes the paragraph.
8. Anchor phrase in Gate `:40`, "There is one constructor method named for each
   type of hash." → 11 words, `found=True` (the period there is source
   punctuation, so this one is exact as printed).
9. Candidate citation: `corpus/evidence/round39/verify-receipts.py:73-79` is
   `def sha256_file` streaming `h.update(chunk)` → `h.hexdigest()`;
   `:138-139` is `if receipt["expect_sha256"] != sha256_file(args.expectations):
   return fail("expect-sha256-mismatch")`. The Gate `:36` and the note `:1` cite
   exactly these lines. Holds.
10. Spot-check currency: `corpus/lessons/round-40.md` was committed only at
    `282dc76` (`git log -- corpus/lessons/round-40.md`), and
    `git diff --stat 282dc76..HEAD -- corpus/lessons/round-40.md` is empty;
    `corpus/lessons/round-40-verifier-spotcheck.md:38-41` is committed at
    `6bc90e0` with AGREE on the S059 admit and the S074 reject.
11. Prior tool receipts for this quote: `grep -rn quote-reopen corpus/lessons/round-40.md
    corpus/evidence/round40/` → no matches. The only committed S059
    quote-reopen receipt is `.ufo/waves/round-31/falsify/AttackRowS059/quote-reopen.out`,
    and its `items.tsv` quote is the **hexdigest** sentence, not the
    digest-concatenation sentence: `S059  S059  Like digest() except the digest
    is returned as a string object of double length, containing only hexadecimal
    digits.` So the 13-word quote has no prior `VERBATIM` receipt.

## Findings

### F1 — P3, precision: printed quote carries a period outside the span

Gate `:40`: `Located quote (13 words): “the digest of the concatenation of the
data fed to it so far.”` The page span ends at `far` (`…so far using the
digest() or hexdigest() methods.`). Under the gate tool's matcher the string
**as printed** returns `found=False`; the same 13 words without the period
return `found=True`. The non-author spot-check already prints the period-free
form (`round-40-verifier-spotcheck.md:38`) and the S074 anchor cell omits it.
Substance is not misquoted; only "exactly as printed" (QUALITY 30) is at risk.
Fix: drop the period inside the quotation marks (or end the span at `far`).

### F2 — P3, completeness: file-level registry changes not fully inventoried

Gate `:42-43` documents the table changes and summarizes the search-log
screening, but two committed changes to the same file are unreported:

- `corpus/SOURCES.md:106` — a new `## Paths` bullet ("Receipt expectation
  digests — S059: …").
- `corpus/SOURCES.md:109` — the appended round-40 `## Search log` line; the Gate
  gives its screening counts but does not record the append or its
  identified/screened/included/excluded figures (`1/1/1/0`).

The S059 row's `opened` cell also stays `2026-10-23` while the Gate says
`accessed 2026-10-24`; the honest reading is that the row has no re-open date
field and the 2026-10-24 date lives at `:109` and in the note's `verified-at:`.
This matches the r39 S071 precedent (`S071` first opened 2026-10-23, "re-opened
2026-10-24" recorded in `capture-bash-pin-r39.md`), so it is a convention, not a
row defect — but the Gate does not say it.
Fix: one bullet naming `:106` and `:109`, plus "row cells: `used-by` only;
`opened` remains 2026-10-23; the 2026-10-24 access is recorded in the search log
and the note's `verified-at:`".

### F3 — P3, precision: "same URL and anchor" overstates anchor identity

Gate `:41` says S074 has "same URL and anchor". URLs are identical. Anchor
cells are not identical text: S059's anchor names `Hash algorithms` **and**
`Hash Objects` plus four methods (`digest_size`, `.update()`, `.digest()`,
`.hexdigest()`), while S074's names only the Hash-algorithms paragraph. Both do
resolve to the paragraph that carries the quote, so the duplicate rejection
stands on URL + scope, not anchor equality.
Fix: "same URL, same anchored paragraph".

### F4 — P3, currency: spot-check bullet stale at HEAD

Gate `:51`: "Pending an outside non-author review of at least one admit and one
reject." At HEAD that predicate is false: `6bc90e0` commits
`round-40-verifier-spotcheck.md`, whose table agrees on the S059 admit, the S074
reject, the knowledge-entry admit, and the rejected authorship/truth claim
(4/4). It was true at the Gate's own commit `282dc76`. `round-39.md:69` shows
the same pattern ("pending the hyaku closure (as every round)"), so this is the
lane's chronology, not a rewriting of history; a reader at HEAD can still be
misled.
Fix: append an erratum at the next round (Gate file is at `282dc76` bytes), or
have the round report point at the spot-check lesson.

### F5 — P2, procedure: no criterion-25/30 quote-reopen receipt

QUALITY 25 ("A cited web quote is re-opened, and a miss is recorded") and 30
("A Gate quote is verbatim before admission") require the newly located quote to
be put, exactly as printed, in a TSV item naming `S059` and verified with
`python3 tools/quote-reopen.py verify --items <tsv>`, admitting only on
`VERBATIM`. No such TSV, receipt, or `QUOTE_REOPEN` line exists for round 40,
and no round-40 page capture was committed; the only S059 quote-reopen receipt
on disk is r31's, for a different sentence. My static check shows the span is
verbatim in the committed 2026-10-23 capture and the anchor has not drifted, but
that is not the named artifact. Producing it needs a live fetch, which this seat
is not authorized to make.
Fix: run the tool on the period-free span and commit the output beside the
round-40 controls (operator/live-fetch authorization required).

## Conflicts recorded verbatim

1. Gate `:41` "same URL and anchor" vs committed row `:69` anchor
   "`Hash algorithms` and `Hash Objects`: `hashlib.hash.digest_size`, `.update()`,
   `.digest()`, `.hexdigest()`; Python 3.15.1 documentation, page as served
   2026-10-23" and row `:84` anchor "“Hash algorithms” section, paragraph
   beginning “There is one constructor method named for each type of hash”;
   Python 3.15.1, opened 2026-10-24".
2. Gate `:51` "Pending an outside non-author review of at least one admit and one
   reject." vs `round-40-verifier-spotcheck.md:38` "live fetch 2026-10-24 …
   AGREE" (committed `6bc90e0`).
3. Gate `:40` "…so far.”" vs pinned page "…so far using the digest() or
   hexdigest() methods." and spot-check `:38` "…so far".

## Holds (independently re-derived)

- H1 URL/locator: one new row (S074), absolute `https://` URL in row and Gate;
  no own-work row added this round, so no locator is missing.
- H2 Access date: 2026-10-24 stated for both rows in the Gate; S074's row carries
  it in `opened` and its anchor cell; S059's re-open date is carried at
  `SOURCES.md:109` and note `:2`. Live observation itself is seat-reported
  (ScoutHashSource live GET; non-author spot-check `:38`) — I did not fetch.
- H3 Quote fidelity: 13 words; verbatim in the normalized committed capture,
  inside the paragraph directly after `<h2>Hash algorithms` / `#hash-algorithms`.
- H4 S059 old→new: exactly `corpus/knowledge/revision-binding-r31.md` →
  `corpus/knowledge/revision-binding-r31.md, corpus/knowledge/receipt-expectation-digests-r40.md`;
  only `used-by` changed; `status`/`recheck` unchanged as claimed.
- H5 Registry table census: 73→74 rows, A 67→68, rejected 4→5; validator exit 0
  with the four expected W04 warnings including S074; matches the lesson.
- H6 Candidate/admitted citation: note exists, `source:`/`verified-at:`/`recheck:`
  present, S059 and verifier `:73-79,138-139` cited exactly; the Limit paragraph
  disclaims truth, authority, and authorship as the Gate states.
- H7 S074 semantics: tier A, `rejected`, `used-by=—`, reason and flip condition
  printed in the Gate and present in the row; no new source admitted.

## Out of scope / not checked

- C1/C2 counter correctness and receipt contents (other seats; not re-run here).
- R2–R5 dispositions, `routed-defect-dispositions.json`, SCORECARD/LOG edits.
- Truth of the knowledge entry's mechanism claim beyond its citations.
- Live fetch of `docs.python.org` (no authorization in this seat).
- No tools installed or updated; pacman untouched.

## Observed concurrent changes (not mine)

`git status --porcelain` at review time also shows ` M tools/research-gate.sh`
(+85 lines, mtime 2026-10-24 04:23:46 -0300), ` M .ufo/waves/round-40/w1/swarm-registry.json`,
sibling `?? .ufo/waves/round-40/w1/*.md` reports, and `?? .ufo/waves/round-41/`,
`?? corpus/evidence/round41/`. None of these were caused or touched by this
seat; the +85-line gate edit is outside this audit.

## Artifact pointers

- Audited Gate: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-40.md:32-51`
- Rows: `corpus/SOURCES.md:69` (S059), `:84` (S074), `:106` (Paths), `:109` (search log)
- Knowledge note: `corpus/knowledge/receipt-expectation-digests-r40.md:1-3,13,19`
- Pinned page: `.ufo/waves/round-31/build/ScribeSrcHashlib/response.body:252-259`
- Prior (different-quote) tool receipt: `.ufo/waves/round-31/falsify/AttackRowS059/items.tsv`, `quote-reopen.out`
- Non-author spot-check: `corpus/lessons/round-40-verifier-spotcheck.md:38-41`
- Counter scripts read for citations only: `corpus/evidence/round39/verify-receipts.py:73-79,138-139`
- Report: `.ufo/waves/round-40/w1/ScribeLessonGate.md` (this file)
