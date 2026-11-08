# R95ScribeCorrections — scoped findings report (round 95, lane `chousa`)

Seat `R95ScribeCorrections` (leaf, scribe). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`,
HEAD `bc94923ba5c0d32e56197365db06809a2bed0b71` ("round-95: wave w1 spec, builder, dispatch, ready marker and
registry"). Assignment: draft the append-only corrections owed from the round-94 non-author spot-check
(`corpus/lessons/round-94-verifier-spotcheck.md`, "Routed defects for next round"), items **D2 and D4–D8**,
re-opening each cited file and line myself, plus the round-94 ledger class tally.

## Behavior

- Six defects re-opened and confirmed against committed bytes: **D2, D4, D5, D6, D7, D8 — all six
  reproduce.** Each is drafted as one correction bullet in
  `.ufo/waves/round-95/w1/R95ScribeCorrections-log-draft.md`, in the mandated form
  `- Correction (r94 spot-check D<n>): <file>:<line> says "<old>"; the record is "<new>" (<evidence
  pointer>). The original text stays.` No original text is rewritten.
- Ledger class tally computed with the prescribed `awk`, after a header check: the file is **headerless**,
  so the `NR>1` form drops row 1. Both forms pasted in the draft; the correct all-rows tally is
  **`falsifies-wording 8` / `falsifies-number 1` / `neutral 10`** over 19 rows.
- Nine receipts written and copied into `.ufo/waves/round-95/w1/` as `R95ScribeCorrections-*.txt`
  (sha256 in the table below). Each receipt contains the exact command, its observed output, and the
  exit code.
- Scratch `/fast/scratch/hyaku/chousa-r95/R95ScribeCorrections/` used for receipt staging only, deleted
  before yield. No fixture repo, no clone, no network, no tool install, no `sudo`, no `pacman`.
- **No production edit.** The only files written are under `.ufo/waves/round-95/w1/` (the draft, this
  report, the receipts). `LOG.md`, `SCORECARD.md`, `plans/round-94.md`, `plans/round-95.md`,
  `.ufo/waves/round-94/claim-falsification.tsv` and every corpus file were read only.

## Gates (self-checks on my own writes)

| check | command | observed |
|---|---|---|
| draft exists, non-empty | `wc -l .ufo/waves/round-95/w1/R95ScribeCorrections-log-draft.md` | 11688 bytes / 79 lines |
| report exists | `wc -c .ufo/waves/round-95/w1/R95ScribeCorrections.md` | this file |
| receipts copied | `sha256sum .ufo/waves/round-95/w1/R95ScribeCorrections-*.txt` | 9 files, digests in the table below |
| no production file touched | `git -C chousa-shokunin status --porcelain` before my writes | only `.ufo/waves/round-95/w1/` entries (all mine) |
| scratch removed | `rm -rf -- /fast/scratch/hyaku/chousa-r95/R95ScribeCorrections` | exit 0 |

## Touched surfaces

Written (all under `.ufo/waves/round-95/w1/`):

- `R95ScribeCorrections-log-draft.md` — the six draft correction bullets + the ledger tally.
- `R95ScribeCorrections.md` — this report.
- `R95ScribeCorrections-ledger-tally.txt`, `-D1-report-miscount.txt`, `-D2-log.md-stale.txt`,
  `-D3-gate-url-datedate.txt`, `-D4-ledger-attribution.txt`, `-D5-sentinel-scope.txt`,
  `-D6-execC3-limits.txt`, `-D7-amendment4-revpair.txt`, `-D8-preamble-stale.txt`.

Read (not modified): `LOG.md`, `SCORECARD.md`, `plans/round-94.md`, `plans/round-95.md`,
`.ufo/waves/round-94/claim-falsification.tsv`, `.ufo/waves/round-94/w1/*.md`,
`corpus/evidence/round94/after/*.txt`, `corpus/evidence/round94/control-driver-r94.py`,
`corpus/lessons/round-94.md`, `corpus/SOURCES.md`, `corpus/lessons/round-94-verifier-spotcheck.md`,
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-94/chousa.md` (fleet root, read-only),
`/home/vgpnk/Projects/shokunin/CORPUS.md` (fleet root, read-only).

## Findings — one per defect, with the exact command, receipt and observed line

### D2 — `LOG.md` round-94 "After" bullet is stale for its own round. **REPRODUCES.**

- Cited text: `LOG.md:2724-2728` quotes `PINNED_FILES=34/34 … RECEIPT SELF_PIN OK rev=41038ed7
  receipts_rev=352924bb` and `DETECTOR_WITNESS=17/17`; `LOG.md:2713` names only freeze `41038ed7` (F) and
  carrier `352924bb` (C).
- Record: the round-94 landing measurement is F3 `ebbcbe39` / C3 `d13c2ff2`. Every scored receipt in
  `corpus/evidence/round94/after/` carries `# computed_against F=ebbcbe396ac9a6352134cae8232968c9cf068c30
  C=d13c2ff24dc8d866239a7428e78ccb82b3817018`; `after/c1-verify.txt:13` prints `PINNED_FILES=35/35` and
  `after/c2-counter.txt:6` prints `DETECTOR_WITNESS=18/18`.
- Commands and observed:
  - `grep -n "PINNED_FILES\|DETECTOR_WITNESS\|computed_against" corpus/evidence/round94/after/*.txt` → exit 0;
    `after/c1-verify.txt:13` `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=35/35
    RECEIPT_PINS=6/6 PIN_ROLES_OK=14/14 CONTROL_DRIVER_R94=PASS`; `after/c2-counter.txt:6` `VERDICT
    fields_hold=1 legs_ok=16/16 DETECTOR_WITNESS=18/18`.
  - `grep -n "PINNED_FILES=35/35\|DETECTOR_WITNESS=18/18" LOG.md` → exit 1, no match.
  - `SCORECARD.md:4201` `PINNED_FILES=35/35 RECEIPT_PINS=6/6 PIN_ROLES_OK=14/14`; `SCORECARD.md:4202`
    `DETECTOR_WITNESS=18/18` — SCORECARD and `after/*.txt` agree, LOG.md does not.
- Staleness, not fabrication: the quoted pair is genuine for its own revision —
  `.ufo/waves/round-94/w1/R94ExecC1Repro-verify.stdout.txt:9-10` prints `rev=41038ed7…
  receipts_rev=352924bb…` / `PINNED_FILES=34/34` at C, and
  `.ufo/waves/round-94/w1/R94CriticClaims-receipts/R94CriticClaims-c2-curation.txt:3` prints
  `DETECTOR_WITNESS=17/17` at C.
- Receipt: `.ufo/waves/round-95/w1/R95ScribeCorrections-D2-log.md-stale.txt`
  (sha256 `a521f4b9670540e09b673a9ca5becc7e2690eaa40172d0144807d6d63e0a6e74`).

### D4 — ledger C2 row credits `R94CriticClaims` with a finding it does not file. **REPRODUCES.**

- Cited text: `.ufo/waves/round-94/claim-falsification.tsv:10` — `C2 w1/R94CriticClaims.md
  falsifies-wording plans/round-94.md predicate tokens span the summary line and the VERDICT line, not one
  line; Amendment 2(c)`.
- Record: the seat files no two-line-predicate finding. Its C2 predicate row reads `reproduced verbatim |
  bound` (`.ufo/waves/round-94/w1/R94CriticClaims.md:122`); its seven fires F1–F7 are F1 (C1 narrative),
  F2 (C1 role vocabulary), F3 (C1 named limit 2), F4 (C2 population wording), F5 (C2 `DUPCOUNT_1=1/1`
  interposition), F6 (C2 `Before` wording), F7 (C1 predicate) — no two-line-predicate item. The finding
  belongs to `R94ReviewerC2` F3, and `plans/round-94.md:98` heads Amendment 2 `(R94ReviewerC2
  F1/F2/F3/F4)` with the two-line clause at `plans/round-94.md:104-105`.
- Commands and observed:
  - `grep -n "^\*\*F[0-9]" .ufo/waves/round-94/w1/R94CriticClaims.md` → exit 0, lines 149 (F7), 165 (F1),
    175 (F2), 189 (F3), 203 (F4), 217 (F5), 228 (F6) — none is a two-line-predicate finding.
  - `grep -n "Predicate: counter line" .ufo/waves/round-94/w1/R94CriticClaims.md` → exit 0, line 122:
    `| Predicate: counter line + `VERDICT fields_hold=1 legs_ok=16/16 DETECTOR_WITNESS=17/17` | reproduced
    verbatim | bound |`.
  - `grep -n "### F3 — LOW: frozen predicate text" .ufo/waves/round-94/w1/R94ReviewerC2.md` → exit 0, line 95.
  - `grep -n "grep -cF" .ufo/waves/round-94/w1/R94ReviewerC2.md` → exit 0, lines 101-103.
  - `.ufo/waves/round-94/w1/receipts-R94ReviewerC2/controls-predicate-contiguous.txt` → `0` /
    `grep_exit=1` and `0` / `grep_exit2=1`.
  - `grep -n "Amendment 2 (" plans/round-94.md` → exit 0, line 98;
    `grep -n "The predicate values are printed across two lines" plans/round-94.md` → exit 0, line 104.
- The narrowing is real (Amendment 2(c) exists and the sentence changed); only the ledger's attribution
  is wrong. A structural check backs it: `grep -rn "two lines\|two-line\|summary line\|VERDICT line"
  .ufo/waves/round-94/w1/*.md` → exit 0 with exactly one hit, `R94ScoutSources.md:214`, and that hit is an
  unrelated negative-control probe ("a two-line probe with an unused `import os`").
- Receipt: `.ufo/waves/round-95/w1/R95ScribeCorrections-D4-ledger-attribution.txt`
  (sha256 `390fad3b90b3cacf741424d0c78236da7e366289b93dabd6a8413caac11e99ed`).

### D5 — ledger C1 SentinelScope row is wider than the seat's evidence. **REPRODUCES.**

- Cited text: `.ufo/waves/round-94/claim-falsification.tsv:4` — `C1 w1/R94SentinelScope.md
  falsifies-wording plans/round-94.md no containment guard for --work, --pins/--expected/--receipts,
  symlinked pin rows or --receipts-rev; Amendment 8`.
- Record: the seat filed F2 (`--work` `rmtree`, no containment guard), F5 (a pins row naming an in-tree
  symlink reads bytes outside the tree), F6 (`--pins` outside the tree is read before containment is
  checked) and F7 (`--receipts-rev` unvalidated like `--rev`). It files nothing on `--expected` or
  `--receipts` — those two flags do not appear in its report at all. The guard for them does exist, added
  by the lane at Amendment 8, not measured by the seat.
- Commands and observed:
  - `grep -n "^## F[0-9]" .ufo/waves/round-94/w1/R94SentinelScope.md` → exit 0, F1–F10 (F2 line 69, F5
    line 154, F6 line 173, F7 line 193).
  - `/usr/bin/grep -n -e "--expected" .ufo/waves/round-94/w1/R94SentinelScope.md` → **exit 1, no match**.
  - `/usr/bin/grep -n -e "--receipts " .ufo/waves/round-94/w1/R94SentinelScope.md` → **exit 1, no match**
    (every `--receipts` hit in that report is `--receipts-rev`).
  - `grep -n "" corpus/evidence/round94/control-driver-r94.py | sed -n "486,494p"` → exit 0:
    `contained = [("--expected", a.expected), ("--pins", a.pins)]`, then `contained.append(("--receipts",
    a.receipts))` under `if a.mode == "verify":`, then the containment loop with
    `SETUP {label} outside --root: {path}`.
  - `grep -n "Amendment 8 (" plans/round-94.md` → exit 0, line 139 —
    `**Amendment 8 (R94SentinelScope F2/F5/F6/F7) — containment and validation.**`
- So the row's scope exceeds the seat's evidence and the `--expected`/`--receipts` containment must be
  attributed to Amendment 8, not to the seat.
- Receipt: `.ufo/waves/round-95/w1/R95ScribeCorrections-D5-sentinel-scope.txt`
  (sha256 `dd8bbef92eaea5ed70c94071f42908f8dd3f9155d5a3578bba3514bfea8544c2`).

### D6 — ledger C3 ExecC3Repro row overstates what was measured. **REPRODUCES.**

- Cited text: `.ufo/waves/round-94/claim-falsification.tsv:15` — `C3 w1/R94ExecC3Repro.md neutral -
  counter and controls reproduced; both named limits measured`.
- Record: the seat says the opposite in its own words. `.ufo/waves/round-94/w1/R94ExecC3Repro.md:176-178`:
  "Named limits 2 (any column-0 `#`…`######` heading, no setext/indented parse) and 3 (a tally inside a
  fenced code block is attributed to the preceding heading) were **not** independently measured by this
  seat; the frozen predicate does not require them and no claim sentence depends on them beyond the
  declaration." The two limits it did measure are named limit 1 (`alias-heading`, line 103) and named
  limit 4 (`third-tail`, line 112).
- Commands and observed:
  - `grep -n "" .ufo/waves/round-94/w1/R94ExecC3Repro.md | sed -n "176,178p"` → exit 0, the two sentences
    quoted above.
  - `/usr/bin/grep -n -e "named limit 1 confirmed" -e "named limit 4"
    .ufo/waves/round-94/w1/R94ExecC3Repro.md` → exit 0, lines 103 and 112.
- Receipt: `.ufo/waves/round-95/w1/R95ScribeCorrections-D6-execC3-limits.txt`
  (sha256 `53b18191ad6714dd9be575677c0d5d077bf8f9ae574de39550328ad009cdb8aa`).

### D7 — `plans/round-94.md` Amendment 4 names the wrong revision pair for the green run. **REPRODUCES.**

- Cited text: `plans/round-94.md:122` — "C1 battery are about `C`'s bytes, and
  `after/c1-forgeries.txt` at F2/C2 is the green run."
- Record: no `after/` file exists at F2 `4cbaed6c` or C2 `f276d7fb`. The directory first lands at F3
  `ebbcbe39` / C3 `d13c2ff2`, and the green run's own header names F3/C3.
- Commands and observed:
  - `git ls-tree 4cbaed6c corpus/evidence/round94/after/` → exit 0, **empty output**.
  - `git ls-tree f276d7fb corpus/evidence/round94/after/` → exit 0, **empty output**.
  - `git show f276d7fb:corpus/evidence/round94/after/` → `fatal: path 'corpus/evidence/round94/after/'
    exists on disk, but not in 'f276d7fb890f6f3057cc85aacd18f5a735e0d975'`.
  - `git ls-tree ebbcbe39 corpus/evidence/round94/after/` → exit 0, six blobs (the six `after/*.txt`).
  - `git show ebbcbe39:corpus/evidence/round94/after/c1-forgeries.txt | head -3` → exit 0, line 1
    `# computed_against F=ebbcbe396ac9a6352134cae8232968c9cf068c30 C=d13c2ff24dc8d866239a7428e78ccb82b3817018`.
  - `git show 4cbaed6c:corpus/evidence/round94/forgeries-r94.py | grep -n "s1-schema-two-column"` → exit 1
    (dropped at F2, as the paragraph says); the same grep at F `41038ed7` → exit 0, line 171. So the
    sentence's `s1`-drop half is accurate; only its revision pair for the green run is wrong.
  - `git log -1 --format="%ct %ci %h %s"` → 4cbaed6c 12:50:45, f276d7fb 12:51:48, ebbcbe39 13:05:45,
    d13c2ff2 13:06:49, all 2026-11-08.
- Receipt: `.ufo/waves/round-95/w1/R95ScribeCorrections-D7-amendment4-revpair.txt`
  (sha256 `26ba7cf70f14eb799fb6382dad750aa61fc8dd6779aceed2f5758038e5fa50e0`).

### D8 — `plans/round-94.md:86` preamble overstates the freeze at which the amendments landed. **REPRODUCES.**

- Cited text: `plans/round-94.md:86` — "Each is a narrowing or a wired guard forced by the wave, applied
  before `C2`; the artifact that forced it is named with its seat."
- Record: Amendments 8 and 9 are absent at F2 `4cbaed6c` and present at F3 `ebbcbe39`; F3/C3 land after
  C2 in commit time. The preamble's scope is Amendments 1–7 at C2 and Amendments 1–9 at C3.
- Commands and observed:
  - `git show 4cbaed6c:plans/round-94.md | grep -n "Amendment 8\|Amendment 9"` → **exit 1, no match**.
  - `git show ebbcbe39:plans/round-94.md | grep -n "Amendment 8\|Amendment 9"` → exit 0, lines 139 and 144.
  - `git show 4cbaed6c:corpus/evidence/round94/control-driver-r94.py | grep -n "contained = "` → exit 1
    (the Amendment 8 guard is absent at F2); the same grep at F3 → exit 0.
  - `git show ebbcbe39:corpus/evidence/round94/control-driver-r94.py | grep -n "contained = "` → exit 0,
    `487:    contained = [("--expected", a.expected), ("--pins", a.pins)]`.
  - Commit timestamps as in D7 (F2 12:50:45 < C2 12:51:48 < F3 13:05:45 < C3 13:06:49).
- `plans/round-94.md` is not rewritten; the correction is an appended note.
- Receipt: `.ufo/waves/round-95/w1/R95ScribeCorrections-D8-preamble-stale.txt`
  (sha256 `20df7cc6ddceef676810940c1a18036732e7b6d3c1af153d12eefd9053f380c9`).

## Ledger class tally (required)

Header check first: the ledger has **no header row** — `head -1 … | cat -A` prints a data row
(`C1^Iw1/R94ExecC1Repro.md^Ifalsifies-number^Iplans/round-94.md^I…`), exit 0. `wc -l` → 19.

```
$ awk -F'\t' 'NR>1{c[$3]++} END{for(k in c) print k, c[k]}' .ufo/waves/round-94/claim-falsification.tsv
neutral 10
falsifies-wording 8
exit=0

$ awk -F'\t' '{c[$3]++} END{for(k in c) print k, c[k]}' .ufo/waves/round-94/claim-falsification.tsv
neutral 10
falsifies-number 1
falsifies-wording 8
exit=0
```

**Correct tally over all 19 rows: `falsifies-wording 8`, `falsifies-number 1`, `neutral 10`.** The
prescribed `NR>1` form reads `falsifies-wording 8` / `neutral 10` and silently omits the one
`falsifies-number` row — the exact class the round-94 report counts separately at
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-94/chousa.md:188` and `:224-225`
("9 `falsifies-wording`, 1 `falsifies-number`, 9 `neutral`"). The ledger's true counts are 8/1/10.

Also measured, because it explains the report's "9": 9 rows name a `plans/round-94.md` pointer
(`awk -F'\t' '$4=="plans/round-94.md"{n++} END{print n}'` → `9`), while 8 rows are class
`falsifies-wording`. The report's 9 is the pointer count, mis-set as the class count. Receipt:
`.ufo/waves/round-95/w1/R95ScribeCorrections-ledger-tally.txt`
(sha256 `b6eb7b09f2c4867f411197c288588c2d868671adcb36247c60f6cad389280c05`).

**Method note for the round-95 report.** `plans/round-95.md:54-55` promises to "compute the class tally
with the `awk` command and paste its output". If that command is the `NR>1` form, the pasted output
will again omit the `falsifies-number` row and read as 8/10. The tally must be taken over all rows
(no `NR>1`) for this headerless file, and the header check stated.

## Out of scope (measured, not drafted)

- **D1** (round-94 report ledger class miscount) and **D3** (lesson `## Gate` omits the URL and access
  date for `S221`) are outside this seat's assignment and are **not** drafted here. Both were measured
  while checking the tally and are recorded for the L1:
  - D1 reproduces: the report says 9/1/9 at `.ufo/reports/round-94/chousa.md:188` and `:224-225`; the
    ledger is 8/1/10 (receipt `R95ScribeCorrections-D1-report-miscount.txt`).
  - D3 reproduces: `/usr/bin/grep -n "git-scm" corpus/lessons/round-94.md` → exit 1 (the URL is absent
    from the lesson) and `/usr/bin/grep -n "read 2026-11-08" corpus/lessons/round-94.md` → exit 1 (the
    access date is absent), while `corpus/SOURCES.md:233` carries both
    (`https://git-scm.com/docs/git-clone` and `read 2026-11-08`). Receipt
    `R95ScribeCorrections-D3-gate-url-datedate.txt`. The contract text the spot-check cites lives in the
    **fleet root** `CORPUS.md:113` ("The round lesson's `## Gate` records, for every new row, the URL, the
    access date …"), not in the lane — worth knowing before drafting.
- C1 and C2 of round 95 (the frozen claims) were **not** attacked by this seat; my assignment is the
  round-94 correction ledger. The tally work above bears on the round-95 report's method note only.
- No `tools/`, `SKILL.md`, `PROVINCE.md`, `corpus/` or `MANIFEST.json` file was read for mutation; no
  git or jj command was run outside read-only `git log`/`git ls-tree`/`git show`/`git status` against the
  lane's own history. No sibling repo touched. No network used. No tool installed or upgraded.

## Artifact paths

- Draft (the deliverable): `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-95/w1/R95ScribeCorrections-log-draft.md`
- This report: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-95/w1/R95ScribeCorrections.md`
- Receipts (copied into `w1/`):
  `R95ScribeCorrections-ledger-tally.txt`, `R95ScribeCorrections-D1-report-miscount.txt`,
  `R95ScribeCorrections-D2-log.md-stale.txt`, `R95ScribeCorrections-D3-gate-url-datedate.txt`,
  `R95ScribeCorrections-D4-ledger-attribution.txt`, `R95ScribeCorrections-D5-sentinel-scope.txt`,
  `R95ScribeCorrections-D6-execC3-limits.txt`, `R95ScribeCorrections-D7-amendment4-revpair.txt`,
  `R95ScribeCorrections-D8-preamble-stale.txt`.

VERDICT: R95ScribeCorrections C1 n/a — outside this seat's assignment (round-94 correction ledger); no round-95 claim was attacked.
VERDICT: R95ScribeCorrections C2 n/a — outside this seat's assignment (round-94 correction ledger); no round-95 claim was attacked.
