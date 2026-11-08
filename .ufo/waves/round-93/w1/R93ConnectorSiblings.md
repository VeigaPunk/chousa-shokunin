# R93ConnectorSiblings — sibling-overlap scan (read-only)

Seat: connector, leaf. Lane: `chousa-shokunin`. Frozen pair attacked: **F2 `b7241252c2358613d3b22b7d0454d98c56dab373`** / **C2
`754b62fb6adc60e44e12375af5461a0ebe302994`**. Scratch: `/fast/scratch/hyaku/chousa-r93/R93ConnectorSiblings/`
(deleted before yield); every receipt cited here is copied into `.../.ufo/waves/round-93/w1/R93ConnectorSiblings/`.

## 0. What was measured, on which bytes

- Clone: `git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin <scratch>/repo` + `git checkout 754b62fb…`;
  `git rev-parse --show-toplevel` = `<scratch>/repo`, `HEAD` = `754b62fb…`. Every scored read below is from a clone at a
  named revision, never from the lane working tree.
- Host interpreters: `python3` = **3.14.8** (default); `python3.13` at `/home/vgpnk/.local/bin/python3.13`.
- Baseline at the frozen pair — receipt `c2-verify-at-frozen-pair.txt`:
  `python3 -B corpus/evidence/round93/control-driver-r93.py verify --root . --repo . --rev b7241252… --receipts-rev 754b62fb… --work <scratch>/w1`
  → `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=22/22 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=PASS`, rc 0.
- The lane advanced **during this seat**: C2 → F3 `d5c19c54`/C3 `d740760e` → F4 `596eabc9…`/C4 `94fbf892` → F5
  `1362f4b2…`/C5 `881a541f` → C6 `c1ebb1d9` (`git log --oneline`, receipt `lane-moved-after-assignment.txt`). One
  worktree read taken at 11:20 (`instrument-pins.txt` sha `1f45495a…`) was **discarded** and re-taken from the C2 blob
  (sha `09e85ae0…`, same 2 500 B, self row `2733d572…`) — recorded in the same receipt, not scored.
- Corroboration at the current carrier — receipt `probe-j-c5-verify.txt`: at C5 (`--rev` F4 `596eabc952f7dcd9bd27030af7dba54714f4af4c`,
  `--receipts-rev 881a541f…`) the same form prints `PINNED_FILES=22/22 … CONTROL_DRIVER_R93=PASS`, rc 0. The C1
  *verify* leg reproduces along the carrier chain; the C1 *battery* leg does not reproduce at C2 (§3, F1).

## 1. Overlap scan — one closest sibling match per pattern

Sweep population: the committed `corpus/` + `tools/` + `SKILL.md` of every sibling lane (chousa excluded), plus the
lane's own commits. `.ufo/` wave chatter was used only for quoting, never as a mechanism witness.

| # | Pattern | Closest sibling match (path:line) | Sibling mechanism | chousa r93 placement | Distinct or duplicate |
|---|---|---|---|---|---|
| P1 | **pins-table walk** (every table row byte-checked on disk) | `kagi-shokunin/corpus/stamps.tsv` (164 rows: path, sha256, lines, bytes) + `kagi-shokunin/corpus/claim-ledger.sh:520-540` (`verify_stamps`: per-row `STALE`/`MISSING`/`NOT-A-FILE`; rows may not be absolute or carry `..`, `:484-485`; `stamp` regenerates the whole row set and refuses a shrinking `stamp` without `--prune`, `:17-24`) | population = the artifacts *a round cites*; 4-field rows; the table does **not** pin itself and pins no receipt | `control-driver-r93.py:278-319` (`pin_report`) walks **every** row of `corpus/evidence/round93/instrument-pins.txt` with `PIN_DISK_MISMATCH`/`PIN_MISSING` per row; 2-field rows; population includes the six receipts and the table's own minus-self row; the same walk is paired with a `git show` blob comparison at two bases (`:336-380`) | **Distinct.** Different population rule (the table is the population), different row shape, and the table pins itself. No duplicate. Near-miss: `tameshi-shokunin/tools/pin-disposition.py:1-30` (a six-leg `pin-manifest-v1`, worktree content vs recorded sha256, "the committed manifest is the configured pin authority for this probe, not an adversarial baseline-authentication gate") — a manifest of harness legs, not an evidence table. |
| P2 | **receipt-pin mechanism** (every committed receipt pinned by digest) | `audio-shokunin/corpus/live/r94-boundary/probes/r94b_manifest.py:14,25-33` + `RECEIPTS.md:46,50`: a `manifest.sha256` over **every** file the seat wrote, regenerated from disk, the manifest **excluded by name** (`SKIP_NAMES = {"manifest.sha256"}`), verified with `sha256sum -c manifest.sha256`, its own digest printed and recorded **outside** the table (`manifest sha256 e072454f…`) | discovery from disk (any file in the evidence dir), one flat body, no per-case codes, self excluded rather than self-pinned | `control-driver-r93.py:169-194` (`receipt_pins`): one pin row per receipt discovered in `--receipts`, per-case codes `RECEIPT_MISMATCH`/`RECEIPT_UNPINNED`/`RECEIPT_MISSING`, checked in both the table walk and the `self_pin` blob check | **Distinct in placement** (same table as the instruments; per-case codes; a removed row is also refused). Not a duplicate — but "discover the receipt set from disk and refuse an unlisted body" is *prior art* in audio/game-dev; the round should not present discovery as new. Near-miss: `kaidoku-shokunin/tools/round-94/c1-receipt-agreement.py:27,43` (`.json`+`.stdout`+`.rc` triples cross-checked for label/met/exit agreement — no digest pin). |
| P3 | **whitespace-quote shape rule** | `kagi-shokunin/corpus/sources-census.sh:410-412`: `q=$quote; q=${q//[[:space:]]/}` then `[[ -z $q ]] || cap_locate …` → `finding SC_CAPTURE "id=$id quote-not-located"` | whitespace-emptiness folded into the *locate* failure of a registry cell (col 13); not counted as its own class | `curation-r93.py:322-326` counts every three-cell quote row whose cell `strip().strip('"').strip()` is empty into `ws_quote_rows`, **before** the shape filter; `:481-485` refuses it as its own leg `WSQUOTE` and prints `Q_WSQUOT`; `:80-82` of the claims make the leg non-deletable (`EXPECTED_LEGS` 14→15) | **Distinct, not a duplicate.** Same idea, different population (a knowledge entry's `Located quotes` table vs the source registry), different observability (a counted leg + `quote=<whitespace>` naming vs an undifferentiated `quote-not-located`). The *class* is not new fleet-wide; the claims already frame C2 as "classification, not a refusal r92 lacks", so there is no overclaim. |
| P4 | **historical-tally derivation** | `mori-shokunin/tools/mori-pin-check.py:29-34,119` (tally pins in `SKILL.md` re-measured live; a tally in another cell of a row or on a continuation line is `hidden` (R9a/R9b); `--min-tally-pins N  floor on tally pins found (a deleted pin is not a fix)`; `stale`/`absent` classes) | re-measures the bound command; the pinned *text* must equal the observed text; a tally that escapes the row's semantic cell is a fatal `hidden`; a **floor** on the pin count | `skill-tally-r93.py:109-152`: each historical tally is *derived* from a named committed receipt — the exact quote `PASS (161 cases, 0 skipped)` must appear in `corpus/evidence/round25-final-measure.log` (and `256`/`round34/audit-dispositions.md`) — and must also be *present* in the `## Gates` scope; tallies outside the scope are enumerated against `TAIL_DECLARED` and an undeclared one prints `HIST_SCOPE_BLEED` | **Distinct.** mori re-measures live; chousa requires the historical figure to be *grounded by a receipt quote* and *present in scope* — a derivation the fleet does not have. The *tail* half is the same class as mori's `hidden`, with a different boundary (ATX scope vs cell/continuation line). Near-miss: `kagi-shokunin/corpus/self-counts.py:15,32` (`expect:<ID>` "runs NOTHING … a host/substrate row's pinned number can still bind a document"; "Historical round-dated observations are outside the table's population") — a committed-expect binding, but without a grounding receipt. |

Result: **0 duplicates**; three of four classes already exist somewhere in the fleet (P1 kagi, P3 kagi, P4 mori), so the
round's novelty is placement and observability, not the class. No sibling mechanism was re-invented in a way that
duplicates the only implementation of a capability.

## 2. Cross-lane convention: evidence-directory-wide pin table with a minus-self row

**Answer: no sibling records one.** Sweep over every sibling lane's committed `corpus/` and `tools/`:

- `sweep2-self-rows-precisely.txt` — **242** pin-shaped tables (≥5 `<sha256>  <path>` rows; audio, game-dev-2d/3d,
  tabi, kengaku, kagi, mori, tameshi, tsukuroi …): **0** carry a row naming themselves.
  `TABLES WITH A ROW NAMING THEMSELVES: none`.
- `sweep2b-reverse-order-self-rows.txt` — path-first tables checked too (`stamps.tsv`, `anchor-pins.tsv`,
  `inrow-pins.tsv`, `self-counts.tsv`): `self_rows=0` for each; chousa's C2 blob has `self row present = 1`.
- `sweep-minus-self-absent.txt` — the token families `minus-self|MINUS_SELF|minus_self|self_pin|SELF_PIN` occur in 12
  sibling lanes (857 files, mostly wave chatter); the three that state the *rule* outside waves are
  `kasegi-shokunin/corpus/instruments/r40-closure.sh`, `r41-closure.sh`, `tameshi-shokunin/corpus/QUALITY.md`.

The three placements that do exist, quoted:

1. **Self excluded by name, self digest recorded outside the table** — `audio-shokunin/corpus/live/r94-boundary/probes/r94b_manifest.py:14`
   `SKIP_NAMES = {"manifest.sha256"}`; `.../RECEIPTS.md:50` `(3429 files; manifest sha256 e072454f9fb977201cc39b4fb6fbb664d3eb20c15bb15acf1253efa2a4f7a8cd)`.
2. **The minus-self value stored inside the object it covers** — `kasegi-shokunin/corpus/instruments/r40-closure.sh:514-519`:
   `# h7_inner FILE — the canonical H7 payload for a receipt, WITHOUT its own H7 / # line: the self-reference is
   closed by never reading the line under test.` (the *value* is a payload line, not a pin row).
3. **Self-pin in an external sidecar** — `kake-shokunin/.ufo/waves/round-92/c92_defects.py:57-58`
   (`SELF_PATH` = the counter, `SELF_PIN = ".ufo/waves/round-92/frozen/c1-self.sha256"`); the same shape as
   `kaidoku-shokunin/SKILL.md:951` (a custody receipt "self-pins the instrument's sha256 … + a `.sha256` sidecar").
4. The **rule** form, in a sibling's QUALITY: `tameshi-shokunin/corpus/QUALITY.md:2530`
   `150. A counter's self-pin is the sha256 of its own bytes with the pin line removed by a stated normalisation rule,
   re-derivable with one command, and checked before any other action; the conjunct a receipt prints is the result of
   that check, never a literal.`

Consequence for chousa: the minus-self **row** is a fleet-first placement, and the only one that makes the table cover
its own coherence with no sidecar and no out-of-band receipt. It is therefore *not* a duplicate. The two normalisation
sites in the driver (disk: `pins_file_sha_minus_self`, `:155-167`, hashes each remaining line's raw text; blob:
`self_pin`, `:366-379`, `splitlines()` + `b"\n"`) are the same rule only while the file has a trailing newline and no
CRLF and no other row whose path merely *ends with* the table's path — the sibling rule 150's "one stated normalisation
rule" is therefore met in effect but not in code shape (two implementations, not one helper).

## 3. Sibling / shared-rule findings

Every finding names the command, the receipt, the observed line, and the exit code.

### F1 — the frozen C2 battery leg does not reproduce (fleet PROTOCOL §Gate standard, "Two evidences")

- Command (receipt `probe-e-battery-on-pristine-c2-python314.txt`):
  `cd <clone@C2> && python3 -B corpus/evidence/round93/forgeries-r93.py --root . --repo . --rev b7241252… --receipts-rev 754b62fb… --work <scratch>/wP`
  Observed: `tarfile.AbsoluteLinkError: '.ufo/waves/round-35/w2/MutGrepShimPath/shims/b/grep' is a link to an absolute path`, **rc 1**, and no `FORGERY_REFUSED=` line.
- Same command under `python3.13` (receipt `probe-f-battery-python313-pristine-c2.txt`):
  `FORGERY_REFUSED=0/2 PRIOR_ACCEPTED=0/2 DERIVE_OK=0/1 POSITIVE=fail`, **rc 1** — `FAIL unexecuted-instrument: r93 rc=1 (PIN_DISK_MISMATCH …), r92 rc=1 accepted=False`, `FAIL positive: r92 rc=1 r93 rc=1`.
- Cause, isolated (receipt `probe-i-archive-tree-no-repo.txt`): the C2 battery builds its trees with `git archive` +
  `tarfile.extractall` (`forgeries-r93.py:41-55` at C2); the extracted tree has no `.git`, so the expected rows that run
  `--repo @ROOT@` fail: `FRESH_OK=4/6`, `CONTROL_DRIVER_R93=FAIL`, rc 1. The failure is intrinsic to the C2 bytes, not to my clone.
- The lane's own repair agrees with this diagnosis: `d740760e` "the forgery battery runs on shared clones (fresh legs
  need a git dir)" replaced `archive()` with `clone()` at C3. So this is a **finding against the frozen pair, already repaired**;
  no action against C6. It is reported because a deviation from the claim's field is a finding, not something to hide.
- Second-order: under 3.14 the battery also cannot even build a tree, so a lane that runs its own claim under the host
  default interpreter measures nothing (`PEP 706` default filter + an absolute symlink in `round-35` wave evidence).

### F2 — receipt population is decided by file extension in one leg and by header in another (chousa QUALITY 204)

- Rule: `chousa-shokunin/corpus/QUALITY.md:1294` `204. A file in a receipts directory is an unscored receipt only when it parses as one. … Check: the leg requires a \`# case=\` header`.
- Code: `control-driver-r93.py:178` discovers only `*.txt`; `:496-497` tolerates a `.txt` **without** `# case=` as "raw instrument evidence"; `:180-186` refuses that same file as `RECEIPT_UNPINNED` (no pin row).
- Probe G (receipt `probe-g-raw-txt-in-receipts-dir.txt`): a headerless `raw-note.txt` added to `controls/receipts/` →
  `RECEIPT PINS FINDING RECEIPT_UNPINNED:raw-note`, `PINNED_FILES=22/22 … CONTROL_DRIVER_R93=FAIL`, **rc 1** — the file
  the R6 leg calls "not a receipt" is refused by T2 as an unpinned receipt. One file, two verdicts.
- Probe H (receipt `probe-h-raw-json-only.txt`): a receipt-shaped `raw-note.json` added alone →
  `COMMITTED_OK=6/6 … PINNED_FILES=22/22 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=PASS`, **rc 0** — invisible to both legs.
- Therefore named limit (4) "a receipt added after `C` is `RECEIPT_UNPINNED`" is true only for `.txt`; a `.json`/`.md`
  receipt added after C is neither scored nor refused. Cross-lane: no fleet rule fixes a `.txt` convention
  (`kaidoku-shokunin/tools/round-94/c1-receipt-agreement.py:27,43` receipts are `.json`+`.stdout`+`.rc`; audio/game-dev
  ship `.json`), so the extension is an unstated lane-local choice, not a shared rule.
- Status at the current carrier: **unrepaired** — C6 driver still `endswith(".txt")` at `:178`, `:357`, `:506`.

### F3 — the pin walk's PASS is table-relative: a committed row deletion prints PASS with a shrunken denominator

- Code: `control-driver-r93.py` (C2 `:303-319`, C6 `:303-323`) walks the pins table's rows and requires
  `checked == len(pins)` (`C2 :529`, **C6 `:540`**); `wanted` (`C2 :292-302`) derives instruments only from the rows the
  expected table executes, and the self row digests the table minus itself. Nothing binds the table's **size**.
- Probe A (receipt `probe-a-worktree-row-delete.txt`): at C2, delete the row for `corpus/evidence/round93/curation-r93.py`
  (an r93 instrument no expected row executes) and re-cut the self row in the **worktree**, frozen revisions →
  `RECEIPT PINS OK 21/21 … RECEIPT SELF_PIN FINDING SELF_DRIFT corpus/evidence/round93/instrument-pins.txt@754b62fb…`,
  **rc 1**. The walk itself is content: `21/21`.
- Probe B (receipt `probe-b-committed-row-delete.txt`): the same edit **committed** and `--receipts-rev` moved to that
  commit → `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=21/21 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=PASS`, **rc 0**.
- Probe K at the **current carrier C6** (receipt `probe-k-c6-committed-row-delete.txt`, C6 `c1ebb1d9`, F5 `1362f4b2…`):
  identical → `PINNED_FILES=21/21 … CONTROL_DRIVER_R93=PASS`, **rc 0**. The F5 `PIN_SELF_ROW_ABSENT` repair
  (`C6 :307`) closes "delete the self row", not "delete a compared row".
- Control (receipt `probe-c-executed-row-delete.txt`): deleting a row the expected table *executes*
  (`round89/curation-r89.py`) → `RECEIPT PINS FINDING INSTRUMENT_UNPINNED:corpus/evidence/round89/curation-r89.py`, **rc 1**.
  So the guard works exactly where `wanted` derives the population, and nowhere else.
- Which rows are outside `wanted ∪ receipts`: the r93 instruments other than the driver's own `base` entry
  (`forgeries-r93.py`, `curation-r93.py`, `skill-tally-r93.py`, `skill-tally-r93-controls.py`), `controls/selftest-r93.txt`,
  `claims.md`, `claims.json` — 7 of 22 at C6 (the battery's first forgery covers `curation-controls-r93.py` only when the
  *battery* is also run).
- Sibling precedent for the class (not binding on chousa, but the class is solved elsewhere):
  `mori-shokunin/tools/mori-pin-check.py:119` `--min-tally-pins N  floor on tally pins found (a deleted pin is not a fix)`;
  `tameshi-shokunin/corpus/QUALITY.md:2545` rule 152 "a receipt the run did not write is a missing row, not a pass …
  never a vacuous pass". The round's own C2/C3 instruments already use the same defence (`EXPECTED_LEGS` 14→15,
  `HIST_SOURCES` length, `TAIL_DECLARED`) — C1 is the only claim of the three without it.
- Status at the current carrier: **unrepaired** — C6 `:540` still `checked == len(pins)`; claims at F4/C6 still fix
  `PINNED_FILES=22/22`, which is now satisfied only by a reviewer reading the receipt against the frozen sentence, not
  by the counter itself.

### F4 — `--selftest` spelling collision with the fleet gate vocabulary (C3 instrument, interface only)

- Fleet rule: `PROTOCOL.md:385` `- **Self-test.** Every gate exposes a self-invocation mode over isolated fixtures (temp
  trees, no network, no live-tree write) asserting both the exit code and a stable expected finding-id … The flag
  spelling is the lane's (\`--selftest\`, …)`.
- Code: `skill-tally-r93.py:44` `ap.add_argument("--selftest", help="captured selftest output; omitted means run the
  tool")`; `:51-56` reads that file and sets `rc = 0`; `:58-60` otherwise runs `tools/research-gate.sh --selftest` **in
  the tree** (not an isolated fixture).
- Assessment: the counter's `--selftest` is a *receipt input*, not a self-invocation mode. It is not a hole — the capture
  path still requires the literal `RESEARCH_GATE_SELFTEST: PASS (n cases, k skipped)` line (`:34,61-64`), so a FAIL
  capture is `SETUP` exit 2, and the hardcoded `rc=0` only decorates that message. But registering this counter as a
  `gate` in `SKILL.md` under the fleet schema would make the same flag mean two different things; either rename the
  input flag (`--verdict-file`) or add a real self-invocation mode at registration. No action requested this round
  (`SKILL.md` is unchanged this round by instruction).

### Not findings (recorded so they are not re-opened)

- `--root`-relative defaults: chousa's T3 (`control-driver-r93.py:42-44,409-415`) is **stricter** than the closest
  sibling — `kagi-shokunin/corpus/quote-locate.py:64` still defaults `--root` to `Path(__file__).resolve().parent.parent`,
  the exact shape chousa's QUALITY 202 forbids. Nothing to repair in chousa; the T3 form is worth copying cross-lane.
- The transient 16-row read of `instrument-pins.txt` (receipt `C6-state-check.txt`, taken while the lane moved
  C5→C6) was an intermediate revision, not a defect: the C5 and C6 blobs both carry 22 rows and the C5 verify PASSes
  (`probe-j-c5-verify.txt`).

## 4. One bounded proposal — port the enumeration floor the other two claims already use

**Evidence (all above):** the C1 walk defends every row it is given but not the number of rows it is given: a committed
deletion of an unexecuted row plus a self-row re-cut prints `PINNED_FILES=21/21 … PASS`, `rc 0` (probe B at C2, probe K
at C6), while the frozen claim fixes `PINNED_FILES=22/22`. The same round's C2 refuses a deleted leg by pinning
`EXPECTED_LEGS` and C3 refuses a deleted historical tally by pinning `HIST_SOURCES`/`TAIL_DECLARED`; mori solves the
identical class with `--min-tally-pins` and tameshi states it as QUALITY 152. C1 is the only claim of the round whose
PASS is weaker than its own printed predicate.

**Proposed move (next freeze, F6):** in `control-driver-r93.py`, replace the table-relative conjunct with an enumerated
floor, and add the matching battery state —

1. `PIN_FLOOR = 22` and `RECEIPT_FLOOR = 6` as module literals (same re-cut discipline as `EXPECTED_LEGS`), and in the
   summary conjunct require `checked == PIN_FLOOR and rchecked == RECEIPT_FLOOR and rtotal == RECEIPT_FLOOR` instead of
   `checked == len(pins) and rchecked == rtotal`; print `PIN_FLOOR_SHORT checked=<n> floor=<N>` when short.
2. One battery state (`forgeries-r93.py`): delete the `curation-r93.py` row, re-cut the self row, commit in the fixture,
   and require `rc 1` + `PIN_FLOOR_SHORT` (the two states F5 added make this the third refusal in the same shape).
3. Keep `wanted` as-is: the floor covers the count, `wanted` covers the identity of executed rows. The residual
   (swap one unexecuted row for another file at equal count) stays inside named limit (1) and should be named there.

**Affected axes:** operability (C1, the lowest scored axis, historical 3/10) improves: `PINNED_FILES` becomes a scored
fact rather than a reviewer comparison. Calibration (C2) and freshness (C3) are untouched — different instruments,
no shared code path. Contract: the claim sentence already states `22/22`/`6/6`, so no claim re-freeze is needed beyond
the instrument bytes; the floor makes the counter agree with the claim instead of being weaker than it.

**Risks:** (i) the floor is a literal and must be re-cut whenever the population legitimately grows (a seventh receipt at
the next carrier) — the same one-line re-cut the lane already performs for `EXPECTED_LEGS`, and it should be named in
the claim's limits; (ii) a floor protects count, not identity — a swap of two rows at equal count survives, so it must be
stated as such, not sold as a completeness proof; (iii) it does not touch F2's extension blind spot — that needs a
header- or manifest-based population and is a separate, smaller move.

**Verification:** clean C2 and C6 trees must still print 22/22 and 6/6 (baseline receipts `c2-verify-at-frozen-pair.txt`,
`probe-j-c5-verify.txt`); probe K must flip from `PASS rc 0` to `FAIL rc 1 PIN_FLOOR_SHORT`; probe C's
`INSTRUMENT_UNPINNED` must be unchanged; the battery's existing POSITIVE and the two F5 refusals must stay green.

## 5. Verdicts

VERDICT: R93ConnectorSiblings C1 fired — at the frozen pair the battery leg is red under both host interpreters
(`tarfile.AbsoluteLinkError` on 3.14, `FORGERY_REFUSED=0/2 PRIOR_ACCEPTED=0/2 … POSITIVE=fail` on 3.13; repaired at C3
`d740760e`), and the pin walk still prints PASS with a shrunken denominator after a committed row deletion
(`PINNED_FILES=21/21`, rc 0 at C2 and at C6) while its receipt path ignores non-`.txt` receipts.

VERDICT: R93ConnectorSiblings C2 held — my run of `curation-r93.py --root .` in the C2 clone printed
`CURATION_R93=PASS`, `LEGS_MEASURED=15/15 Q_SHAPE_FAIL=0 Q_WSQUOT=0`, rc 0 (receipt `c2-counter-at-c2.txt`); the WSQUOTE
mechanism is distinct from the closest sibling (`kagi sources-census.sh:410-412`), not a duplicate.

VERDICT: R93ConnectorSiblings C3 held — my run of `skill-tally-r93.py --root . --selftest …/selftest-r93.txt` in the C2
clone printed `SKILL_TALLY_R93=PASS`, `HIST_DERIVED=2/2 HIST_PRESENT=2/2 TAIL_OK=1 LEGS=4/4`, rc 0 (receipt
`c3-counter-at-c2.txt`); the derivation is distinct from mori's live re-measure and kagi's `expect:` binding, and the
`--selftest` flag collision (F4) is an interface observation, not a predicate failure.
