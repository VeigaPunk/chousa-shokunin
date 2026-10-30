# R65D02 — draft "Sources & frontier" section (round-65 report)

Section text below is ready to integrate verbatim. All numbers are derived from
`corpus/SOURCES.md` at `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` (freeze) versus
`9672a2e998bff2b51d18b0df4d835bd3ae2c453f` (after-measurement tip), and from the
census artifacts `.ufo/waves/round-65/census-start.txt` / `census-end.txt`.
Derivation receipts (exact commands + outputs) follow the section text.

---

## Sources & frontier

Registry rows 153 → 157 (+4) between the round-65 freeze `f99de3b…` and the
after-measurement tip `9672a2e…` (`corpus/SOURCES.md`; count:
`git show <rev>:corpus/SOURCES.md | grep -c '^| S'`). All four rows were opened
2026-10-30 for the receipt-identity question. Added by tier: tier A 2 — S154
(`corpus/SOURCES.md:164`, git-cat-file(1) installed manual, `docs`) and S155
(`corpus/SOURCES.md:165`, hashlib installed module documentation, `code`);
tier B 1 — S156 (`corpus/SOURCES.md:166`, round-64 before-measurement receipt,
`own-work`); tier C 1 — S157 (`corpus/SOURCES.md:167`, reference-validator
docstring candidate, `own-work`, rejected: intent text cannot prove execution
authenticity). Added by status: 3 mined, 1 rejected, 0 queued; the three mined
rows carry `used-by corpus/knowledge/receipt-identity-r65.md`, S157 is rejected
with `used-by —`. Tier totals: A 118→120, B 27→28, C 8→9; status totals:
mined 124→127, queued 19→19, rejected 10→11.

Rows touched: 0. No pre-existing row changed status, recheck, used-by or any
other cell: the pinned diff is 4 insertions and 0 deletions
(`git diff f99de3b… 9672a2e… -- corpus/SOURCES.md`), and `comm -3` over the two
sorted row sets differs by exactly those 4 additions (153 shared rows
byte-identical). Frontier rows advanced: 0 — no existing row moved along the
queued→mined pipeline, no recheck or used-by cell changed, and the
`## Leads (unopened)` section is unchanged; the frontier moved by addition
(four newly opened rows), not by advancement.

Census (frozen command
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`):
the before artifact `.ufo/waves/round-65/census-start.txt` (landed at `f99de3b…`)
and the after artifact `.ufo/waves/round-65/census-end.txt` (landed at
`9672a2e…`) are byte-identical to each other and to a fresh run at the landed
state: five W04 duplicate-url-across-scopes warnings — S051, S053, S073, S074,
S075 (lines 1–5) — then the `chousa ok` line (line 6), and no E-codes. The four
new rows introduced no new validation findings (same 5 W04 before and after).
Exit codes are not embedded in either artifact; re-running the frozen command
this session exited 0 with byte-identical output (`corpus/SOURCES.md` is
unchanged `9672a2e…`→`a6b6f93…`, the working-tree HEAD), and the script's
contract makes warnings-only exit 0 (`scripts/sources-census.sh:16` "exit: 0
clean or warnings"; W04 is warning class `:33`; selftest
"W04-does-not-fail-validation" expects 0 at `:364`). The after census exit 0 is
directly observed; the before census exit 0 is corroborated by identical bytes
plus that contract, not directly observed at its historical moment (observing it
would require a checkout, which this wave forbids).

---

## Derivation receipts (audit trail; not part of the section text)

All git calls read-only with explicit -C. Lane root
`/home/vgpnk/Projects/shokunin/chousa-shokunin`.

1. Pinned diff — 4 added rows, 0 removed:
   `git -C <lane> diff --stat f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd 9672a2e998bff2b51d18b0df4d835bd3ae2c453f -- corpus/SOURCES.md`
   → ` corpus/SOURCES.md | 4 ++++` / ` 1 file changed, 4 insertions(+)`.
   `... | grep -c '^+| S'` → `4`; `... | grep -c '^-| S'` → `0`.
   Full diff hunk: single hunk at `@@ -161,6 +161,10 @@` adding S154–S157;
   no other hunk (so `## Leads (unopened)` and the search log are untouched).

2. Row counts: `git -C <lane> show f99de3b…:corpus/SOURCES.md | grep -c '^| S'`
   → `153`; same at `9672a2e…` → `157`.

3. Added rows by tier/status — parsed from the diff rows themselves:
   S154 tier `A`, kind `docs`, status `mined`, opened `2026-10-30`, used-by
   `corpus/knowledge/receipt-identity-r65.md`; S155 `A`/`code`/`mined`,
   same used-by; S156 `B`/`own-work`/`mined`, same used-by; S157
   `C`/`own-work`/`rejected`, used-by `—`.

4. No modified shared rows: `comm -3 <(git show f99de3b…:corpus/SOURCES.md |
   grep '^| S' | sort) <(git show 9672a2e…:corpus/SOURCES.md | grep '^| S' |
   sort) | wc -l` → `4` (exactly the 4 additions; a touched old row would make
   this >4).

5. Histograms (exact — `awk -F'|' '{print NF}'` gives 13 for all 153 and all
   157 rows, so no escaped-pipe skew):
   before: `98 tier.A/status.mined, 17 tier.A/status.queued, 3
   tier.A/status.rejected, 26 tier.B/status.mined, 1 tier.B/status.queued,
   1 tier.C/status.queued, 7 tier.C/status.rejected` (sum 153);
   after: `100 tier.A/status.mined, 17 tier.A/status.queued, 3
   tier.A/status.rejected, 27 tier.B/status.mined, 1 tier.B/status.queued,
   1 tier.C/status.queued, 8 tier.C/status.rejected` (sum 157).

6. Added-row line numbers at tip: `git -C <lane> show 9672a2e…:corpus/SOURCES.md
   | grep -n '^| S15' | awk -F: '{print $1}'` → `160 161 162 163 164 165 166 167`
   (S150–S157; the added four are `:164`–`:167`).

7. Census artifact provenance: `git -C <lane> log --oneline --follow -- <file>`
   → census-start.txt landed at `f99de3b` (freeze); census-end.txt landed at
   `9672a2e`. `git -C <lane> status --porcelain` on both paths → clean.
   `git show <landed-rev>:<file> | cmp - <live file>` → identical for both
   (`start-identical`, `end-identical`).

8. Frozen command re-run this session (live tree, HEAD `a6b6f93`; input
   `corpus/SOURCES.md` unchanged since `9672a2e` per
   `git diff --stat 9672a2e HEAD` which lists no `corpus/` file):
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`
   → the 6 lines above, then `rc=0`. Output is byte-identical to both
   artifacts' 6 lines.

9. Exit-code contract: `scripts/sources-census.sh:16` (`exit: 0 clean or
   warnings · 1 E/overdue findings`), `:17` (`W-codes … never change status`),
   `:33` (W04 definition), `:361-365` (selftest asserts W04 does not fail
   validation, exit 0), `:645` (W04 emit site).

## Notes for L1 (outside the section)

- Dispatch said tip = `9672a2e…`; the lane HEAD moved on: `9171732` (wave-1
  results + w2 spec/dispatch) and `a6b6f93` (L1 boundary probes) landed after.
  `git -C <lane> diff --stat 9672a2e HEAD` touches only `.ufo/waves/round-65/*`,
  `corpus/evidence/round65/controls/l1-boundary-probes.txt`, and
  `corpus/lessons/round-65.md` — not `corpus/SOURCES.md` — so every number above
  also holds at the current HEAD.
- The two census artifacts are byte-identical to each other: the census did not
  change across the round (warnings-only, exit 0 both ends). If the report wants
  "census unchanged" stated in one clause, use that.
