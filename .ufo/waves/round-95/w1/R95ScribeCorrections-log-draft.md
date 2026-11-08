# R95ScribeCorrections — append-only corrections owed from the round-94 non-author spot-check

Seat `R95ScribeCorrections` (leaf, scribe). Source of the defects:
`corpus/lessons/round-94-verifier-spotcheck.md`, section **"Routed defects for next round"**, items D2 and
D4–D8 (D1 and D3 are outside this seat's assignment; they are measured in the companion report for
completeness and are **not** drafted here).

Every defect below was re-opened by this seat against committed bytes at the lane root
`/home/vgpnk/Projects/shokunin/chousa-shokunin` (HEAD `bc94923b`, lane root at round-95 wave commit).
Each bullet names the file and line, quotes the original text verbatim, states the record, and points at
the evidence pointer. **No original text is rewritten**; these are the append-only correction entries owed
in `LOG.md` round 95 (and, for D7–D8, an appended note, since `plans/round-94.md` is not rewritten).

The exact commands and their observed output, with exit codes, are in the receipts copied beside this
draft under `.ufo/waves/round-95/w1/` as `R95ScribeCorrections-*.txt`.

---

## Draft correction bullets

- Correction (r94 spot-check D2): `LOG.md:2724-2728` says "`CONTROL_DRIVER_R94=PASS`
  (`COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=34/34 RECEIPT_PINS=6/6
  PIN_ROLES_OK=14/14`, `RECEIPT SELF_PIN OK rev=41038ed7 receipts_rev=352924bb`) … `CURATION_R94=PASS`
  (`LEGS_MEASURED=16/16 Q_PUNCTQUOT=0 Q_SHAPE_FAIL=0 DETECTOR_WITNESS=17/17`)"; the record is
  "the round-94 landing measurement is at F3 `ebbcbe39` / C3 `d13c2ff2`, and every scored receipt in
  `corpus/evidence/round94/after/` carries `# computed_against F=ebbcbe396ac9a6352134cae8232968c9cf068c30
  C=d13c2ff24dc8d866239a7428e78ccb82b3817018`; `after/c1-verify.txt:13` prints `PINNED_FILES=35/35` and
  `after/c2-counter.txt:6` prints `DETECTOR_WITNESS=18/18`; `LOG.md:2713` names only F `41038ed7` / C
  `352924bb`, so the round-94 `After` bullet is stale for its own round" (evidence:
  `.ufo/waves/round-95/w1/R95ScribeCorrections-D2-log.md-stale.txt`;
  `grep -n "PINNED_FILES\|DETECTOR_WITNESS\|computed_against" corpus/evidence/round94/after/*.txt` → exit 0,
  `after/c1-verify.txt:13` `PINNED_FILES=35/35`, `after/c2-counter.txt:6` `DETECTOR_WITNESS=18/18`;
  `grep -n "PINNED_FILES=35/35\|DETECTOR_WITNESS=18/18" LOG.md` → exit 1, no match). The earlier pair is
  genuine for its own revision — `R94ExecC1Repro-verify.stdout.txt:9-10` prints `rev=41038ed7…
  receipts_rev=352924bb…` and `PINNED_FILES=34/34` at C, and
  `R94CriticClaims-receipts/R94CriticClaims-c2-curation.txt:3` prints `DETECTOR_WITNESS=17/17` at C — so this
  is staleness, not fabrication. The original text stays.

- Correction (r94 spot-check D4): `.ufo/waves/round-94/claim-falsification.tsv:10` says "C2
  w1/R94CriticClaims.md falsifies-wording plans/round-94.md predicate tokens span the summary line and the
  VERDICT line, not one line; Amendment 2(c)"; the record is "the seat `R94CriticClaims` files no
  two-line-predicate finding: its C2 predicate row reads `reproduced verbatim | bound`
  (`.ufo/waves/round-94/w1/R94CriticClaims.md:122`) and its seven fires are F1–F7 — F1/F2/F3/F7 are C1, F4
  is the C2 population wording, F5 is the `DUPCOUNT_1=1/1` interposition, F6 is the C2 `Before` wording — with
  no two-line-predicate item among them; the two-line predicate finding belongs to `R94ReviewerC2` F3
  (predicate-text fidelity, `grep -cF` → 0 on the contiguous string), and `plans/round-94.md:98` heads
  Amendment 2 `(R94ReviewerC2 F1/F2/F3/F4)` with the two-line clause at `plans/round-94.md:104-105`"
  (evidence: `.ufo/waves/round-95/w1/R95ScribeCorrections-D4-ledger-attribution.txt`;
  `grep -n "^\*\*F[0-9]" .ufo/waves/round-94/w1/R94CriticClaims.md` → exit 0, fires F1–F7 with C1/C2 tags;
  `grep -n "Predicate: counter line" .ufo/waves/round-94/w1/R94CriticClaims.md` → exit 0, line 122
  `reproduced verbatim | bound`; `grep -n "### F3 — LOW: frozen predicate text"
  .ufo/waves/round-94/w1/R94ReviewerC2.md` → exit 0, line 95; `grep -n "grep -cF"
  .ufo/waves/round-94/w1/R94ReviewerC2.md` → exit 0, lines 101-103;
  `.ufo/waves/round-94/w1/receipts-R94ReviewerC2/controls-predicate-contiguous.txt` prints `0` /
  `grep_exit=1` and `0` / `grep_exit2=1`). The narrowing is real; only the ledger's attribution is wrong.
  The original text stays.

- Correction (r94 spot-check D5): `.ufo/waves/round-94/claim-falsification.tsv:4` says "C1
  w1/R94SentinelScope.md falsifies-wording plans/round-94.md no containment guard for --work,
  --pins/--expected/--receipts, symlinked pin rows or --receipts-rev; Amendment 8"; the record is "the seat
  `R94SentinelScope` filed F2 (`--work` `rmtree`, no containment guard), F5 (a pins row naming an in-tree
  symlink reads bytes outside the tree), F6 (`--pins` outside the tree is read before containment is
  checked) and F7 (`--receipts-rev` is not validated the way `--rev` is); it files nothing on `--expected`
  or `--receipts`, which do not appear in its report at all — `grep -n -e "--expected"
  .ufo/waves/round-94/w1/R94SentinelScope.md` → exit 1, no match; `grep -n -e "--receipts "
  .ufo/waves/round-94/w1/R94SentinelScope.md` → exit 1, no match. The `--expected`/`--pins`/`--receipts`
  containment guard does exist, added by the lane at Amendment 8, not measured by the seat:
  `corpus/evidence/round94/control-driver-r94.py:486-494` contains all three labels. The row's scope is
  therefore wider than the seat's evidence and the guard must be attributed to Amendment 8, not to the seat"
  (evidence: `.ufo/waves/round-95/w1/R95ScribeCorrections-D5-sentinel-scope.txt`;
  `grep -n "^## F[0-9]" .ufo/waves/round-94/w1/R94SentinelScope.md` → exit 0, F1–F10; `grep -n -e
  "--expected" …` → exit 1; `grep -n "" corpus/evidence/round94/control-driver-r94.py | sed -n "486,494p"`
  → exit 0, `contained = [("--expected", a.expected), ("--pins", a.pins)]` plus `("--receipts", a.receipts)`
  in verify mode; `grep -n "Amendment 8 (" plans/round-94.md` → exit 0, line 139). The original text stays.

- Correction (r94 spot-check D6): `.ufo/waves/round-94/claim-falsification.tsv:15` says "C3
  w1/R94ExecC3Repro.md neutral - counter and controls reproduced; both named limits measured"; the record is
  "named limits 1 and 4 were measured; limits 2 and 3 were declared unmeasured by the seat itself:
  `.ufo/waves/round-94/w1/R94ExecC3Repro.md:176-178` reads 'Named limits 2 (any column-0 `#`…`######`
  heading, no setext/indented parse) and 3 (a tally inside a fenced code block is attributed to the
  preceding heading) were **not** independently measured by this seat'. The two limits it did measure are
  named limit 1 (the `alias-heading` fixture, `R94ExecC3Repro.md:103-109`) and named limit 4 (the
  `third-tail` fixture, `R94ExecC3Repro.md:112-114`)" (evidence:
  `.ufo/waves/round-95/w1/R95ScribeCorrections-D6-execC3-limits.txt`; `grep -n ""
  .ufo/waves/round-94/w1/R94ExecC3Repro.md | sed -n "176,178p"` → exit 0, the two sentences quoted above;
  `grep -n -e "named limit 1 confirmed" -e "named limit 4" .ufo/waves/round-94/w1/R94ExecC3Repro.md` → exit 0,
  lines 103 and 112). The original text stays.

- Correction (r94 spot-check D7): `plans/round-94.md:122` says "C1 battery are about `C`'s bytes, and
  `after/c1-forgeries.txt` at F2/C2 is the green run."; the record is "`after/c1-forgeries.txt` does not
  exist at F2 `4cbaed6c` or C2 `f276d7fb` — `git ls-tree 4cbaed6c corpus/evidence/round94/after/` and
  `git ls-tree f276d7fb corpus/evidence/round94/after/` both print nothing, and
  `git show f276d7fb:corpus/evidence/round94/after/` returns `fatal: path 'corpus/evidence/round94/after/'
  exists on disk, but not in 'f276d7fb890f6f3057cc85aacd18f5a735e0d975'`. The `after/` directory first lands
  at F3 `ebbcbe39` / C3 `d13c2ff2`, and the green run's own header reads `# computed_against
  F=ebbcbe396ac9a6352134cae8232968c9cf068c30 C=d13c2ff24dc8d866239a7428e78ccb82b3817018`. The `s1` drop
  itself was at F2 as the paragraph says — `git show 4cbaed6c:corpus/evidence/round94/forgeries-r94.py |
  grep -n "s1-schema-two-column"` → exit 1 (dropped), while the same grep at F `41038ed7` → exit 0, line 171.
  So the sentence's revision pair is wrong: the green run is at F3/C3, not F2/C2" (evidence:
  `.ufo/waves/round-95/w1/R95ScribeCorrections-D7-amendment4-revpair.txt`; `git ls-tree 4cbaed6c
  corpus/evidence/round94/after/` → exit 0, empty; `git ls-tree f276d7fb corpus/evidence/round94/after/` →
  exit 0, empty; `git show ebbcbe39:corpus/evidence/round94/after/c1-forgeries.txt | head -3` → exit 0,
  the `# computed_against F=ebbcbe39… C=d13c2ff2…` header; `git log -1 --format="%ct %ci %h %s"` for
  4cbaed6c / f276d7fb / ebbcbe39 / d13c2ff2 → 12:50:45 / 12:51:48 / 13:05:45 / 13:06:49 on 2026-11-08).
  `plans/round-94.md` is not rewritten; the original text stays.

- Correction (r94 spot-check D8): `plans/round-94.md:86` says "Each is a narrowing or a wired guard forced
  by the wave, applied before `C2`; the artifact that forced it is named with its seat."; the record is
  "Amendments 8 and 9 were not applied before `C2`: they are absent from the plan at F2 `4cbaed6c` —
  `git show 4cbaed6c:plans/round-94.md | grep -n "Amendment 8\|Amendment 9"` → exit 1, no match — and
  present at F3 `ebbcbe39` (`git show ebbcbe39:plans/round-94.md | grep -n "Amendment 8\|Amendment 9"` →
  exit 0, lines 139 and 144). The guards they install are likewise F3-only: `git show
  4cbaed6c:corpus/evidence/round94/control-driver-r94.py | grep -n "contained = "` → exit 1 (absent at F2),
  while the same grep at F3 → exit 0. Commit timestamps confirm the order: F2 12:50:45, C2 12:51:48, F3
  13:05:45, C3 13:06:49 (2026-11-08) — F3 and C3 land after C2. The preamble's scope is therefore
  Amendments 1–7 at C2 and Amendments 1–9 at C3" (evidence:
  `.ufo/waves/round-95/w1/R95ScribeCorrections-D8-preamble-stale.txt`). `plans/round-94.md` is not
  rewritten; the original text stays.

---

## Round-94 ledger class tally (as required)

The ledger file **has no header row** — line 1 is already a data row
(`C1^Iw1/R94ExecC1Repro.md^Ifalsifies-number^Iplans/round-94.md^I…`), so the prescribed `NR>1` form drops
row 1 (the single `falsifies-number` row) and undercounts. Both forms are pasted, with the header check
first.

```
$ head -1 .ufo/waves/round-94/claim-falsification.tsv | cat -A
C1^Iw1/R94ExecC1Repro.md^Ifalsifies-number^Iplans/round-94.md^Ibattery exited 1 at carrier C on the unsatisfiable s1-schema case; Amendment 4 dropped it and F3/C3 prints FORGERIES=PASS$
exit=0

$ wc -l .ufo/waves/round-94/claim-falsification.tsv
19 .ufo/waves/round-94/claim-falsification.tsv

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

**Tally over all 19 rows (the correct one — the file is headerless): `falsifies-wording 8`,
`falsifies-number 1`, `neutral 10`.** The `NR>1` form above reads `falsifies-wording 8` / `neutral 10`
and silently omits the `falsifies-number` row, which is the one row the round-94 report itself counts
separately. Note also that 9 rows name a `plans/round-94.md` pointer
(`awk -F'\t' '$4=="plans/round-94.md"{n++} END{print n}'` → `9`) — that 9 is what the round-94 report
miscounted as `falsifies-wording`. Evidence receipt:
`.ufo/waves/round-95/w1/R95ScribeCorrections-ledger-tally.txt`.
