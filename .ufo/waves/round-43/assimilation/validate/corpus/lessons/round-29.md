# Round 29 — re-opening located quotes against their live source

Dates are UTC (the host clock reads UTC-3, so local time showed 2026-10-22).
Base `6c5eb1466f2b8abbd3de576389037f435016d07b`. One claim, C1, on operability.
`tools/quote-reopen.py verify` is a new command. It re-opens located quotes
against the live URL named by `corpus/SOURCES.md`. It reached
`QUOTE_REOPEN_MATCH=130/130` under the frozen design v3 counter on landed
revision `30c9d24da1815e01e161ed2f52d5f951005cc2b8`. This round does not touch
the path-denylist surface of rounds 26 to 28.

## Spot-check intake

| Previous outside finding | Disposition |
|---|---|
| round-28 D1, digit-glued tokens (`round-28-verifier-spotcheck.md:42-45`) | fixed for new prose: `corpus/evidence/round29/prose-check.py` and QUALITY criterion 23. Shown able to fail: exit 1 on `lessons/round-28.md` (9 glued tokens, 5 custody hits), exit 0 on this lesson. Older text is carried unchanged (append-only); sweep `.ufo/waves/round-29/build/ScoutCustodyVocab.md` |
| round-28 D2, custody vocabulary (`:46-49`) | fixed for new prose by the same check and criterion 23; no round-29 file uses it |
| round-28 D3, stale "no end census" statements (`:50-54`, routed `:125-126`) | fixed: dated corrections appended to `LOG.md`, `SCORECARD.md` and `lessons/round-28.md` citing the witness at fleet commit `b4b338e9` (exit 0, `chousa ok`); review `.ufo/waves/round-29/falsify/ReviewQualityRepairs.md` |
| round-28 D4, counts not re-run (`:55-57`) | fixed in practice: every count in the round-29 report is a command re-run with its output; criterion 24 makes control receipts committed evidence |
| round-28 D5, long wall time (`:58-59`) | carried as disclosure: the report states launch-to-report time |
| round-28 routed 4, C1 open; same surface would trip frontier rotation | carried, deliberately not worked: round 29 uses a different surface (`tools/quote-reopen.py`, not `research-gate.sh`). The round-27 C3 complete-path-versus-prefix conflict and the S045 ancestor over-refusal stay open and operator-owned |
| round-27 decision: C3 harmed, keep original clause and red visible | carried unchanged: `research-gate.sh` is byte-identical (SHA-256 `ac1315dd…`), and no control, clause or expectation was edited |
| operator-`*.md` teachings | none exist in the lane (`ScoutSpotcheckRoutes.md`) |

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| A counter met by a shortcut, because every item could be read from committed bytes | v1 label-keyed control `QUOTE_REOPEN_MATCH=82/82` without fetching (`.ufo/waves/round-29/controls/CtlLabelKeyed/receipt.json`) | the pre-data control wave (addendum §9) | design v2 added 48 page-sampled items drawn at run time; the same control fell to 106/130. Shown able to fail: v1 receipt `predicate_holds: true`, v2 receipt `false` |
| A control receipt that met the counter was explained away instead of triggering a re-design | v2 seed-replay control printed 130/130 on `--seed 2901/2902` (`receipt-v2-warmed*.json`), committed at `8026fe60` with the L1 reading "outside the predicate" | seats ConnectorPlanWalk, ScoutSpotcheckRoutes and ScribeQuality flagged it within minutes | design v3 (`aa5e1a31`) removed `--seed` before any data seat ran the counter. The executor seats confirmed in writing that they had not run it. QUALITY criterion 24 now names seed replay. Shown able to fail: `c1-count.py --seed 1 -- true` exits 2 at v3, and the replay control scores 106/130 |
| The L1's own wave-1 prompt told the executor to run the counter with `--seed 2901`, a committed seed | `.ufo/waves/round-29/build-spec.json`, item ExecTool | none | stop-order sent before any run; QUALITY criterion 24 |
| Seats scored contract-following reimplementations on the frozen fixture before the tool existed | `CtlCasefoldNoBoundary` pristine baseline 82/82 under v1; `MutateBlockInline` 40/40 | none | disclosed in `claims.md`. These are not the claim's tool and did not change any rule. Next round's control-wave context should forbid full-contract baselines on the fixture |
| A tool limit found by using the tool: pages that omit `</head>` extract to empty text | S047 page; `.ufo/waves/round-29/falsify/CriticHeadOmission.md` (1 of 32 HTML registry pages) | none | named in `knowledge/quote-reopen-r29.md` Limits and QUALITY criterion 25; a contract change is a later round's claim |
| Lane prose quality (round-28 D1 and D2) | `round-28-verifier-spotcheck.md:42-49` | none before this round | criterion 23 with `prose-check.py`, shown able to fail as in the intake table |
| A stale time-bound statement (round-28 D3) | `round-28-verifier-spotcheck.md:50-54` | none | dated append-only corrections |

## Gate

Sources opened between 01:25 and 01:45 UTC on 2026-10-23. Each quote below is
at most 25 words, copied from the page and re-located with the reference
extractor (`c1-count.py`) and with the landed tool where the tool can read the
page:

| Row | URL | Located quote | Verdict |
|---|---|---|---|
| S046 | https://www.w3.org/TR/annotation-model/#text-quote-selector, §4.2.4 | "This Selector describes a range of text by copying it, and including some of the text immediately before (a prefix) and after (a suffix) it" | admit, tier A spec, mined; tool `VERBATIM` (`falsify/AttackRowS046.md`) |
| S047 | https://wicg.github.io/scroll-to-text-fragment/, §3.6.1 | "Intuitively, this is a case-insensitive search also ignoring accents, umlauts, and other marks." | admit, tier A spec, mined. Located in body text only; the tool says `ABSENT` because of the `</head>` limit (`falsify/AttackRowS047.md`) |
| S048 | https://unicode.org/reports/tr15/, §1.2 | "Normalization Form KC additionally folds the differences between compatibility-equivalent characters that are inappropriately distinguished in many circumstances." | admit, tier A spec, mined; tool `VERBATIM` (`falsify/AttackRowS048.md`) |
| S049 | https://docs.python.org/3/library/html.parser.html, HTMLParser constructor | "all character references (except the ones in elements like script and style) are automatically converted to the corresponding Unicode characters." | admit, tier A docs, mined; tool `VERBATIM` (`falsify/AttackRowS049.md`) |

Rejected inference: "a `VERBATIM` verdict shows the quote supports the claim
or that the source is true". S046 and S047 define location, not support.
QUALITY criterion 8 keeps those states apart. Flip: none. Location never
becomes support.

Fixture sources re-opened for the fixture without row changes: S002, S003,
S008, S013, S019, S020, S038, S044. No existing row changed `status`,
`recheck` or `used-by`.

Freshness by-product, not a claim: the tool re-opened all 33 earlier Gate
quotes from rounds 24 to 28 (`falsify/ScoutFreshnessH.md`, 11 held-out seats).
27 were `VERBATIM`. 3 were `UNREACHABLE`: two PDFs (S011, S037) and S014, which
now answers 403 to a direct GET. 3 were `ABSENT`: `h05` (S006) is a round-24
summary, not a quote, already corrected in round 25; `h20` and `h21` (S021, S022)
hit a PubMed 203 cookie page, and `h20` also capitalizes a mid-sentence "a".
Blind hand readings agreed with the tool on 32 of 33 items. The one
disagreement, `h13` (S014), is the 403 gate.

## Census

Start (base): `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`
→ `chousa ok`, exit 0; manual census rows 45, malformed 0, tier A 39 B 1 C 5,
status mined 22 queued 19 rejected 4, no duplicates, no missing used-by. The
end census is recorded in SCORECARD.md Round 29 and the round report.

## Learning

Author assessments, for the outside check to rule on: expansion improved (one
new capability on uncovered ground, re-opening against live sources, cited by
mined rows S046 to S049); quality improved (QUALITY criteria 23 to 25, D1 to
D3 repairs); discernment unchanged by self-assessment (no outside judgment yet).

## Falsify wave findings (33 seats, `.ufo/waves/round-29/falsify/`)

- Re-derivation: the predicate held in every re-run (RerunCounterA 1 run,
  RerunCounterB 2 runs, ScoutFreshnessH 3 runs, each 130/130). The receipts
  carry the v3 counter hash and the predicate command.
- Held-out: blind readings and the tool agreed on 32 of 33 earlier Gate
  quotes. The independent second implementation agreed with the landed tool on
  all 73 fixture and held-out items (`DiffToolB.md`).
- Mutants: 3 killed (boundary 126, quote map 126, inline-as-block 117) and 3
  survived (verdict order, script and head text, case-insensitive matching).
  The fixture lacks the classes that would kill them. That is a coverage gap
  for the next round. The claim is not re-scaled.
- Counter discrimination: an offline snapshot verifier scored 130/130 with no
  network call (`CriticClaimDesign.md`). The counter checks verdicts against
  current page content, not that the answering process fetched live. This
  control was found after data, so it is reported here, not used to re-design.
  Live fetching is evidenced by the loopback harness, which counts server hits
  (`OfflineConformance.md`: 65 of 65 with only the address guard disabled,
  20 of 64 as landed because loopback is refused), and by code review.
- Security (`SentinelTool.md`): T2, T3, T5, T6 and T7 are closed. T1 (DNS
  rebinding between check and connect) and T4 (slow-drip reads past the 30 s
  deadline) are open; they are next-round items.
- Chronology qualification (`CriticClaimDesign.md`): "before any data seat ran
  the counter" holds for the two executor seats. The mutation seat
  `MutateCounter` ran scratch replays of `counter.main()` with recorded page
  cases between 01:25:59 and 01:27:45 UTC, before the v3 freeze at 01:28:23.
  Those were counter-mutation experiments, not candidate measurements, and
  were disclosed in its stop reply.
- Erratum: `.ufo/waves/round-29/build/ExecTool.md:5` prints a mistyped
  revision. The control-receipt commit is
  `66bf1b9300733b24b76efe393646b3037402088e`.
- Simplifier: about 13 removable lines and a latent cache key that does not
  strip the URL fragment (`SimplifierTool.md`). They were not applied, so the
  measured bytes stay the landed bytes.

## Seats and holds

Control wave 8, build wave 32, falsify wave 33: 73 seats in total. One seat
died: CriticPredicate (critic), refused with "This content was flagged for
possible cybersecurity risk" (`code=cyber_policy`). Its item is a hold. It was
not retried, and nothing it wrote after the refusal is used.

### 2026-10-23 correction to the chronology wording (routed defect D5)

The frozen `corpus/evidence/round29/claims.md:13-14` says “Before any data seat had run the counter”. The supported wording is “before either primary executor scored its candidate”; it does not mean no wave-1 seat had executed counter machinery. Before the v3 freeze, the CtlCasefoldNoBoundary control produced a contract-following scratch reference baseline of 82/82 under v1 (`.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/report.md`, pristine output at lines 123-145). The adjacent `receipt.json` is the mutant result of 78/82, not the reference baseline. MutateCounter also replayed scratch `counter.main()` with recorded page cases and fixed entropy: receipts span 01:25:59 to 01:27:45 UTC, before the v3 freeze at 01:28:23 (`.ufo/waves/round-29/build/MutateCounter.md:11,43-45`; chronology corroboration: `.ufo/waves/round-29/falsify/CriticClaimDesign.md:13-28`). These were a reference baseline and counter-mutation replays, not measurements of either primary executor's candidate. The frozen claims file remains unchanged. Routed by `corpus/lessons/round-29-verifier-spotcheck.md:156-159`.
