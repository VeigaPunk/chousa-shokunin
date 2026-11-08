# R85ExecForge — C1 kill rule K2 (spec generalization) at `64803d33`

Seat: executor, leaf. Claim attacked: **C1 operability** (the round-85 repair of `tools/gate-records.py verify`).
Landing revision `64803d33362f50cf9094e91fc3a4a07216c563ca`; base for the load-bearing comparison
`43c3f7284eee4889cdcc6ac1626573f6579cd533`. No production file, registry row, capture, refetch row or claim byte was touched.

Task: author NEW in-class `GATE-RECORD` forgeries that the frozen battery does not contain, each violating one check of the
docstring at the landing revision, in one file each under `<tree>/forge/`, and run the landed tool on them from the tree root.

## Method (exact commands)

```
S=/fast/scratch/hyaku/chousa-r85/R85ExecForge
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 64803d33... | tar -x -C $S/tree
cd $S/tree && python3 tools/gate-records.py verify --root $S/tree \
    --repo /home/vgpnk/Projects/shokunin/chousa-shokunin forge/*.md
# base comparison, same 81 files:
cd $S/base && python3 tools/gate-records.py verify --root $S/base \
    --repo /home/vgpnk/Projects/shokunin/chousa-shokunin <same 81 absolute paths>
# frozen counter:
cd $S/tree && python3 -B corpus/evidence/round85/gate-records-r85.py --root $S/tree \
    --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --work $S/work
```

Receipts in this folder: `receipt-landed-full.txt` (81 files, rc 1), `receipt-base-full.txt` (same files on the base tool),
`receipt-counter.txt` (frozen counter), `receipt-positives.txt` (15/15, rc 0), `receipt-round85-records.txt` (3/3, rc 0),
`receipt-empty.txt` (records=0, rc 1), `receipt-setup.txt` (non-git `--repo` → `GATE_RECORDS_ERROR`, rc 2),
`receipt-d1-audit.txt` (counter class census), `receipt-base-tool-excerpts.txt` (base 2xx test, authoritative lines).
Per-line table: `summary.tsv` (81 rows: predicted code, in-class, landed status/codes, base status/codes, violated check).
Forged lines: `forge/*.md`, one line per file; `forge/manifest.json` carries the construction note per line.

Observed summary of the controlling run:

```
GATE_RECORDS files=81 records=80 ok=14 fail=66
rc=1
```

`records=80` of 81 files: `forge/k05-lowercase-head.md` is deliberately not a record (lower-case head). Solo run:
`GATE_RECORDS files=1 records=0 ok=0 fail=0`, rc 1  (`receipt-k05-solo.txt`; the behaviour is reproduced in the
bundle because the file contributes no line).

## Coverage of the assigned checklist

| assigned item | files | landed result | in-class per K2 |
|---|---|---|---|
| `fetched` month 13 / day 32 / hour 24 / minute 60 / second 60 / Feb 29 non-leap | t01 t02 t03 t04 t05 t06, plus t07 Apr-31, t08/t09 unreach forms, t10 leap second | t01–t09 `PARSE`; t10 `PARSE` | t01–t09 yes; t10 borderline (see H3) |
| refetch row of a 203 attempt for the same url/time | f01 (S021 admit on the 203 cookie page), f02 (same row, wrong id) | `REFETCH` both | yes |
| refetch row whose http is 201 / 299 | n01 (201), n03 (299) | `REFETCH` both | yes |
| upper-case or mixed-case sha prefix | s01 (upper), s11 (mixed) | `CAPTURE_SHA` both | yes |
| `…` vs `...` vs no suffix | s02 (`...`), s05/s09/s10 (no suffix) | `OK` all four | no — documented grammar (see N1) |
| sha of the `.raw` file instead of the `.txt` | s04 | `CAPTURE_SHA` | yes |
| refetch row matching url but a different id | f02 | `REFETCH` | yes |
| url trailing slash / fragment / http vs https | u01 u02 u03, plus u04 host case, u05 no scheme, u06 two params | `CAPTURE_KEY,REFETCH` (u05 `PARSE`) | yes |
| tier lower-case | d01 | `PARSE` | yes |
| decision other than admit|reject | d02 `ADMIT`, d03 `maybe` | `PARSE` both | yes |
| words leading zero / plus / unicode digits | w08, w01, w03 | `PARSE` all | yes (w08 duplicates frozen D5) |
| quote NBSP / tab / ZWSP / curly vs straight / entities / line break / different capture | c02 c04 c03 c01 c05 c06 c08, plus c09 curly delimiters | c01/c02/c04/c06 `OK`; c03/c05 `QUOTE_ABSENT,WORDS`; c08 `QUOTE_ABSENT`; c09 `PARSE` | no for the four `OK` (documented normalization, see N2); yes for c03/c05/c08/c09 |
| rev 39-hex / tag / HEAD / `rev^{commit}` / 26-word quote / line=0 / 7-digit line | r01 r04 r03 r05 r09 r08 w06, plus r02 upper, r06 tree id, r07 line 1, r11 words=000, r12 tail quote, r13/r14 paths, r15 6-digit line | `REV`(+`LINE`), `QUOTE_LEN`, `PARSE`, `LINE` as documented | yes (r01 duplicates frozen D2) |

Full per-line detail (predicted vs observed code, base-tool status, violated check) is `summary.tsv`.

## Findings

### F1 — K2 does not fire: every in-class forgery is refused with its documented code

63 forged lines are in-class per `claims.md` K2 (a frozen class — registry, tier, capture-key, capture-path, capture-sha,
refetch, words, quote-len, quote-absent, line, rev, parse — or one of the round-85 differentiators); 58 of them are new
members the frozen battery does not contain. All 63 print `FAIL` with the code the docstring assigns that check; the extra
codes that appear alongside (e.g. `REV` together with `LINE`, `CAPTURE_KEY` together with `REFETCH`) are the documented
dependent checks, and the frozen counter's `EXPECTED_CODE` convention tests membership, not equality. No in-class line
printed `OK`. Representative evidence lines from `receipt-landed-full.txt`:

```
t01-month13.md:1 S203 FAIL PARSE
t06-feb29-nonleap.md:1 S203 FAIL PARSE
f01-admit-203-s021.md:1 S021 FAIL REFETCH
s04-sha-raw.md:1 S203 FAIL CAPTURE_SHA
u03-url-https2http.md:1 S203 FAIL CAPTURE_KEY,REFETCH
d01-tier-lower.md:1 S203 FAIL PARSE
w03-words-fullwidth.md:1 S203 FAIL PARSE
c08-diff-capture.md:1 S203 FAIL QUOTE_ABSENT
r03-rev-tagname.md:1 S199 FAIL LINE,REV
r09-rev-quote26-real.md:1 S199 FAIL QUOTE_LEN
r08-rev-line0.md:1 S199 FAIL PARSE
w06-line-7digits.md:1 S199 FAIL LINE
```

### F2 — the 200-only narrowing IS load-bearing, and the frozen counter never exercises its accept-boundary

`f01` (a self-consistent admit for S021 whose only refetch row is the committed 203 attempt, quote `"Cookies must be enabled"`
located inside that 203 capture) prints `OK` on the base tool at `43c3f728` and `FAIL REFETCH` on the landing tool
(`receipt-base-full.txt` vs `receipt-landed-full.txt`). That is the repair's one acceptance change in my battery.

It is not scored by the frozen counter: the differentiator `D1-stale-refetch-txt-sha-drift` builds **zero** forgeries
(`receipt-d1-audit.txt`: `D1-eligible admits: 0`; the only failed rows that carry a `txt_sha256` are the two PubMed URLs, whose
registry rows S021/S032 are `queued`, so neither the 15 frozen admits nor the 5 fresh admits ever reference them). The
counter's own 354 is entirely D2–D7 plus the estate classes. So `claims.md`'s sentence “one load-bearing forgery per
differentiated class” is not met for class 1 by the instrument as frozen, even though the underlying repair is real and
demonstrable — measured here, and only here, by the base-vs-landing pair.

This is an instrument-coverage finding, not a kill: K1 is still met at the landing revision (predicate reproduced below),
and K2 is about acceptance, which does not occur.

```
TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=354/354 EXPECTED_CODE=354/354 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1
GATE_RECORDS_R85=PASS            (rc 0; receipt-counter.txt)
```

### F3 — the calendar repair changes the refusal code only, never acceptance

Every calendar-invalid line I built (`t01`–`t09`, `t10`) is refused by **both** tools. The landing tool says `PARSE`; the base
tool says `REFETCH`. The reason is structural: admit and unreach both require an exact `fetched` match with a committed
`refetch.tsv` row, and every committed stamp is a real calendar instant, so no forged timestamp can survive `REFETCH` and then
be caught by `_valid_ts`. The repair therefore re-labels ~12 refusals per counter run but cannot flip an accept to a refuse.

This matters to the claim's wording (“`fetched` must be a real calendar instant”) only as a precision point: the check is real
and correctly implemented (`2026-13-01`, `2026-01-32`, `24:`, `:60`, `2026-02-29`, `2026-04-31` all `PARSE`), but it is not
load-bearing for any record that could otherwise pass. `receipt-base-full.txt` lines `t01`–`t10` are the measurement.

### F4 — the repair also widens in the other direction: an unreach on a 203 attempt is now accepted

`n02` (S021, `curl_rc=0 http=203`, `decision=reject`, matching the committed row) is `FAIL REFETCH` on the base tool and `OK`
on the landing tool. That follows the docstring's 200-only success rule (“a 203 cookie-challenge page carries no quotable
body”): a 203 attempt is an honest `unreach`. Consequence worth recording: the same committed 203 attempt can now be cited
as an admit and is refused (`f01`) or as an unreach and is accepted (`n02`); both are consistent with the documented contract.

### F5 — no K3 harm in the measured set; three borderline refusals outside it

The K3 set is `OK` in full: 15/15 frozen positives rc 0 (`receipt-positives.txt`) and the round-85 lesson's 3 records rc 0
(`receipt-round85-records.txt`). Records that arguably meet every check yet are refused, none of them committed:

- `k08`/`k09`: a record whose separator after `GATE-RECORD` is a TAB, or two spaces, is **detected** as a record (the docstring’s
  detection rule is “`GATE-RECORD` followed by whitespace or EOL”, and `REC_RE` accepts `\s`) but `parse()` requires one literal
  space, so it prints `FAIL PARSE`. The form grammar in the docstring is written with single spaces, so this is a documented-
  grammar tension rather than a clear violation; no committed record is tab-separated.

- `t10`: `2016-12-31T23:59:60Z` is a real UTC instant (leap second) and is refused `PARSE` by `strptime`. “Real calendar instant”
  in the docstring does not cover leap seconds; no committed `fetched` value is a `:60` stamp.

- `d05`: reverse of the same coin — a record with `decision=reject` but a fully valid capture+quote is **accepted** (`OK`). No
  docstring check ties `decision` to capture presence, so it is not in-class per K2, but the tool certifies a record whose text
  says “reject” while its bytes prove a successful capture. Latent soundness gap, not a fire.

### F6 — what stayed unchanged

No production byte, registry row, capture, `refetch.tsv` row, claim, plan or instrument was written. The 81 forged lines live
only under `<tree>/forge/` in scratch and are copied here; scratch `/fast/scratch/hyaku/chousa-r85/R85ExecForge` is deleted at
exit. No tool was installed or upgraded this seat (no channel used).

## Kill-rule reading

- **K2 (in-class): held.** 63 in-class forged lines, 58 of them new members, all refused with the documented code; zero
  in-class `OK`. The only `OK` lines are ones the docstring’s own grammar or normalization explicitly permits.
- **K3 (harm): no harm in the measured set** (15/15 and 3/3). The refusals that could be argued harmful are confined to
  uncommitted forms (`k08`, `k09`, `t10`) and are outside the frozen measurement set.
- **K1:** predicate reproduced at the landing revision (`GATE_RECORDS_R85=PASS`, rc 0). Instrument-coverage gap F2 is advisory:
  it means the counter under-counts the repair’s real effect, not that the landing fails.
- **K4:** not my item; no whitelist tool was built this seat.

VERDICT: R85ExecForge C1 held — 63 in-class forged lines (58 new members, 5 duplicates of frozen classes) are all refused with their documented codes and no in-class line prints OK, though the frozen counter's D1 differentiator contributes zero forges while the real accept-boundary case (a 203-only admit) is accepted at the base revision and refused at the landing revision.
