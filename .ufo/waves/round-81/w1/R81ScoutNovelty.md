# R81ScoutNovelty — round 81 w1 — per-surface reconnaissance for C1's novelty and placement

Seat: `R81ScoutNovelty` (scout, read-only). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Base `378fda82dc2cbcc555a0565052cc408121813cef`; candidate landing `7e2da96a0541946e796384d42fea18e09ede9e9f`.
Full report with per-finding commands: `.ufo/waves/round-81/w1/R81ScoutNovelty/recon.md`.
Receipts: `.ufo/waves/round-81/w1/R81ScoutNovelty/receipts/r01…r11*.txt` (each receipt names its command, output and exit code).
No production file, registry, counter, claim, fixture or receipt was edited; no network was used; no tool was installed.
Scratch `/fast/scratch/hyaku/chousa-r81/R81ScoutNovelty/` was deleted before this report.

## Findings

**F1 — C1's literal novelty premise holds at the entry level.** At base, `grep -ril` over `corpus/knowledge/*.md` returns
**0** files for `retract`, `Retraction Watch`, `TARCiS`, `expression of concern`, `backward citation`, `forward citation`
and `co-cit` (receipt `r03`, exit 0). Only 2 files contain "citation searching", and both are **adjacent, not same
ground**: `search-tracking-record-r40.md:14`/`:22` treats it as a *PRISMA-S flow-diagram column label*
(`` `citation searching, and other methods should be reported` (char 6355) `in Column 2.` ``) and
`chinese-search-record-r39.md:15` as a *reporting-form field* (`` asks whether `参考文献追溯`, citation searching or
`手工查阅期刊` were used ``). Every "errata/erratum" hit in the prescribed grep is the lane's own append-only errata
apparatus — unrelated sense (receipt `r01`, exit 0).

**F2 — partial weakening of the novelty rationale: the ground was already in the lane's bytes (not in an entry).**
The base capture `corpus/captures/c9d1e74c3ac8d9eb332c9770.txt` (S120, Cochrane Handbook ch. 4, mined 2026-10-26,
`used-by corpus/knowledge/western-instrument-alignment-r50.md`) already contains, at base:
line 918 `` Guidance on terminology, application, and reporting of citation searching has recently been published (the TARCiS statement) ( Hirt et al 2024a ). ``;
line 740 ` 4.4.6 Identifying fraudulent studies, other retracted publications, errata and comments`;
line 742 `... may, for other reasons, have been corrected, retracted or had expressions of concern associated with them since publication. Review authors should examine any relevant retraction notices and errata for information ( MECIR Box 4.4.e )`;
line 747 ` C48 : Examining errata ( Mandatory ) ` — i.e. a *Mandatory* MECIR expectation to examine retraction notices and
errata — plus the TARCiS reference itself in its bibliography (line 1121).
(receipt `r02`, exit 0). `grep -i -E '4\.4\.6|MECIR Box 4\.4|C48|TARCiS|Hirt|retract|errata'` over
`corpus/knowledge/western-instrument-alignment-r50.md` hits only line 14 (the §4.2.1 MECIR *search-expectations* bullet),
so no base entry teaches either topic. The frozen claim's wording ("no base entry names TARCiS; no base entry is about
erratum/retraction linking") is therefore **not falsified**; but an entry on both topics was buildable from S120 with
**zero** new fetches, and the round instead opened six new URLs (S203–S208) — one of which (S203, the TARCiS manuscript)
is the very work S120 already cites. This is not a K3 firing: S120 is not a quoted source of either new entry and no
located quote of S203–S207 contradicts either entry.

**F3 — placement defect at the landing revision: the lane's own knowledge-index preflight gate FAILS.**
`git diff --stat 378fda82 7e2da96a -- corpus/README.md` → empty; the landing never added a coverage row.
`python3 -B tools/lane-preflight.py --root <landing tree> --only G02` →
`GATE G02 knowledge-index FAIL 2 not named in corpus/README.md: citation-searching-tarcis-r81.md,correction-retraction-status-r81.md`,
`PREFLIGHT=0/1 FAILED=G02`, **exit 1** (receipt `r09`); the same gate on the base tree prints
`GATE G02 knowledge-index PASS 91 entries indexed`, exit 0 (receipt `r10`). The C1 counter is unaffected — it does not
read `corpus/README.md` — so this is a placement/lane-gate finding, not a predicate failure.

**F4 — coverage-map placement and proposed row text.** The two entries belong under a new
`## Round81 coverage and frontier (2026-11-06)` section appended at the end of `corpus/README.md`, in the
`| Note | Holds | Sources |` shape used by the `## Round51…Round62 coverage and frontier` sections (which is where rounds
51–62 put their new knowledge rows). Ready-to-paste row text for both entries is in `recon.md` §2.3.

**F5 — registry: no duplicate URL, no new W04.** Scanning the landing registry's 208 parseable 11-cell rows for repeated
first URL gives 6 duplicate groups, all pre-existing (S059/S074, S021/S032, S022/S030, S024/S031, S019/S029, S020/S033) —
**none involves S203–S208** (receipt `r07`, exit 0). `scripts/sources-census.sh validate --file <lane>/corpus/SOURCES.md --today 2026-11-06`
emits exactly the five pre-existing `W04` rows (S051, S053, S073, S074, S075) that the round's own committed
`.ufo/waves/round-81/census-start.txt` already records, plus `file ok`, exit 0 (receipt `r05`); `census` mode reports
`rows 208, tier.invalid 0, status.invalid 0, missing 0` (receipt `r06`). Fleet-wide, the ICMJE URL is also registered by
sibling lane kotoba as its S119 (the `shared` metric, not a within-lane duplicate).

**F6 — S028 (Crossmark) is same ground and the round left it dangling.** `corpus/SOURCES.md:38` — S028 is `queued`
since 2026-10-21, `used-by —`, and its own *teaches* cell reads "A cited work's update, correction or retraction status
is published metadata a reader can check, a recheck trigger" — the E2 entry's thesis, in the lane's words, 16 days
earlier (quoted at `corpus/lessons/round-25.md:77`). It cannot be cited as a located quote: capture key
`dedff231d5c3d3cdb0b4f8e3` is absent from `corpus/captures/` at base *and* landing, and `refetch.tsv` has no S028 row.
So the E2 entry could not quote it — but it neither cites nor dispositions it, and S028 stays `queued` with no flip
after a round that landed an entry on exactly that ground. Honest dispositions: open Crossmark and cite it, or flip
S028 to `rejected` with a reason and flip condition.

**F7 — the C1 predicate itself is met at the landing revision.** `python3 -B corpus/evidence/round81/depth-r81.py --root .`
on the landing tree → `ENTRY citation-searching-tarcis-r81.md counted=yes reason=all-pass`,
`ENTRY correction-retraction-status-r81.md counted=yes reason=all-pass`, `DEPTH_R81 entries=2 fresh_rows=5
located_quotes=14`, `DEPTH_R81=PASS`, exit 0 (receipt `r08`).

**F8 — three adjacent decision-table observations for the reviewer (none is a K3 firing; no cited located quote
contradicts them).** (i) `citation-searching-tarcis-r81.md:33` renders rec 2's "should be seriously considered" as an
unconditional "run"; (ii) `:39` asserts "(rec 5 was corrected)" about a document the lane could not read (S208 rejected,
HTTP 403), disclosed only in the `## Version caveat` section (`:56–61`), not in the decision row; (iii) `:38`'s reporting
row asks for seeds/dates/iterations/indexes while the located quote at `:53` is only the directionality fragment —
supported by the capture (lines 463–480) but not by the quoted fragment alone.

## Unresolved

Whether F2 should be treated as a weakening of C1's novelty premise, a naming obligation on the new entries, or neither
— a judgement about frozen claim wording, not this seat's to make. S208's recommendation-5 wording stays unreachable
(403); this seat's item names no re-open, so no network was used.

VERDICT: R81ScoutNovelty C1 held — no base knowledge entry governs citation searching or retraction status, but the base S120 capture already held the TARCiS citation and a Mandatory MECIR errata/retraction check, and the landing leaves the lane's own G02 knowledge-index gate failing (exit 1) with the two new entries absent from the coverage map.
