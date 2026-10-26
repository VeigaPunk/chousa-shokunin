# R52W2MutC2Counter — mutation test of the frozen C2 counter (c2-count.py)

Seat: R52W2MutC2Counter. Target: the frozen round-52 C2 counter
`corpus/evidence/round52/c2-count.py` at lane commit `e769c037` (base
`00f8c7f`), on real bytes in a scratch `--shared` clone
(`/fast/scratch/hyaku/chousa-r52/R52W2MutC2Counter/clone`, `git rev-parse
--show-toplevel` asserted before any fixture mutation). No tools installed; no
network; no writes outside the clone + this report file.

## Baseline (pristine)

`python3 corpus/evidence/round52/c2-count.py --root $S/clone` → exit 0,
`C2=PASS`; legs: ENTRIES=3/3, BOUND=4/4 REFUSED=0 (ids S113,S114,S115,S116),
REF_ID_UNBOUND=0, NEW_GROUND=3/3, QUOTE_ROWS=38 ON_BOUND=38/38,
SPAN_IDS=4/4, QUOTES_IN_SPAN/ENTRY/LESSON=38/38, QUOTE_SHORT=38/38,
SPAN_CONTEXT=38/38, CAPTURE_BOUND=38/38, SUBSTANCE=PASS, ANCHOR_BOUND=4/4,
INFERENCE_GROUNDED=3/3, QUARANTINE_VERDICTS=1/1 (S120), BLOCKED=0.
Anchor cells read: S113 char 2034,2328,2433,3139,4850 · S114 char
1650,1707,1785,5530 · S115 char 8996,9020,9408,9419,9428 · S116 char
475,592,641,753 (SOURCES.md rows 123–126, cell 6).

## Mutants (all applied byte-exact to the clone, detector per mutant, then
restored from a saved pristine copy; hashes sha256[:16])

| # | Mutant (one behavior-bearing point) | Expected leg | Observed FAIL legs | Verdict |
|---|---|---|---|---|
| M1 | S114 anchor `char 1707`→`char 1708` (SOURCES.md row 124) | ANCHOR_BOUND | ANCHOR_BOUND=3/4 | KILLED |
| M2a | E_JPW body `完全な検索戦略`→``完全な検索戦略X`` (term not a manifest quote) | (quote-in-entry) | none — C2=PASS, exit 0 | SURVIVED |
| M2b | E_JPW body quote `試験登録，Web サイトの完全な検索戦略を記載する`→+`X` (exact spans.tsv/S116-7 quote) | QUOTES_IN_ENTRY | none — C2=PASS, exit 0 | SURVIVED |
| M3 | E_ZHR `source: S113 —`→`source: S114 —` (one source line) | BOUND, REF_ID_UNBOUND | BOUND=3/4, REF_ID_UNBOUND=8, ON_BOUND=32/38, ANCHOR_BOUND=3/3 | KILLED |
| M4 | S113 used-by cell +`, corpus/SOURCES.md` | BOUND, REF_ID_UNBOUND | BOUND=3/4, REF_ID_UNBOUND=9, ON_BOUND=32/38 | KILLED |
| M5 | lesson `register S120 (round 5) verdict: present` line deleted (line 74) | QUARANTINE_VERDICTS | none — C2=PASS, exit 0 | SURVIVED |
| M5b | all VERDICT_RE-matching S120 lines deleted (lines 15 and 74) | QUARANTINE_VERDICTS | QUARANTINE_VERDICTS=0/1 | KILLED |
| M6 | S116 source cell: dead original URL placed before the archive URL | BOUND, ON_BOUND | BOUND=3/4, REF_ID_UNBOUND=6, ON_BOUND=29/38 | KILLED |
| M7 | entry `chinese-prisma-s-reception-r52.md` renamed to `.bak` | ENTRIES, BOUND, GROUNDED | ENTRIES=2/3, BOUND=2/4, NEW_GROUND=2/3, QUOTES_IN_ENTRY=23/38, ON_BOUND=23/38, INFERENCE_GROUNDED=2/3 | KILLED |
| M8 | spans.tsv row S114-9 (footer quote `网站版权…`, char 6121, non-anchor) dropped | (row-count floor) | none — C2=PASS, exit 0 | SURVIVED |
| M9 | spans/S113-4.txt: one byte `c`→`d` in `copyright` (inside quote) | QUOTES_IN_SPAN, CAPTURE_BOUND, ANCHOR_BOUND | QUOTES_IN_SPAN=37/38, CAPTURE_BOUND=37/38, ANCHOR_BOUND=3/4 | KILLED |
| M10 | `S111` (unbound staged id) appended to E_ZHR body | REF_ID_UNBOUND | REF_ID_UNBOUND=1 | KILLED |

## Survivors (coverage findings; the contract is untouched)

- **M2a/M2b — an entry's quoted wording is not re-verified.** Mutating the
  entry body quote (even the exact spans.tsv quote string) flips no leg:
  QUOTES_IN_ENTRY=38/38 stays PASS because the check tests the *manifest row's*
  quote against the entry and the span file, and the entry text is never
  parsed back against the span rows; `inference-ground.py` grounds from the
  span *files* (`span_texts()`), not from the entry's quoted sentence. An
  entry whose quote silently drifts one character still verifies.
- **M5 — the quarantine-verdict leg accepts a citation, not the verdict
  statement.** Deleting the `register S120 (round 5) verdict: present` line
  (74) alone keeps QUARANTINE_VERDICTS=1/1: lesson row 15 quotes the same
  verdict inline (`` `register S120 (round 5) verdict: present` ``) and
  VERDICT_RE matches inside that cell. The leg is satisfied by any occurrence;
  only removing every match (M5b) fails it.
- **M8 — a dropped non-anchor span row is invisible.** Removing spans row
  S114-9 (offset 6041, quote `网站版权…`, char 6121; not among S114's four
  anchor chars) keeps every leg at n-1/37: row-count floor (SPAN_IDS) only
  needs ≥3 per bound id; SUBSTANCE floors are per-id; INFERENCE_GROUNDED=3/3
  is unchanged. The manifest is not required to cover every entry char.

Killed mutants confirm the legs fire on: anchor offsets (M1), source-line
binding (M3), used-by exactness (M4), archiver-first binding (M6), entry
presence (M7), span-file bytes (M9), unbound ids (M10), total verdict removal
(M5b).

## Restoration evidence

After each mutant the pristine bytes were restored (cp from saved copies) and
sha256[:16] confirmed: SOURCES.md `e8e603ef48724acc`, E_JPW
`a35ed7b96436c263`, E_ZHR `2bcc7f01a48c8202`, lesson
`9109bd81c75599f4`, spans.tsv `8c844c1a7d1e6621`, S113-4.txt
`5f7bba8125ff0014`. Final run on restored bytes: `C2=PASS`, exit 0.

VERDICT: attacked the frozen C2 counter with 11 mutants — 7 killed (M1, M3,
M4, M6, M7, M9, M10, M5b), 4 survived (M2a, M2b, M5, M8): entry-body quote
drift, verdict-line duplication, and a dropped non-anchor span row are not
detected; strongest finding is M8 (loss of a manifests row passes every leg).
