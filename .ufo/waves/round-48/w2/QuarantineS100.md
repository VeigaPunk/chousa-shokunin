# Quarantine hand-check — chousa register row S100 (W2, lane QuarantineS100)

**Verdict: `present`.** The frozen row's premise is false on local byte
evidence: the cited artifact exists at the stated fleet-relative path, its
sha256 pin and byte length match the row, and every gate quote verifies. The
"no locator" entry is a census-checker blind spot, not a missing locator.

## Row under check

- Slice: `.ufo/waves/round-48/assimilation/quarantine-slice:21` —
  `S100` … "the gate block named no locator, so no quote was checked"
- Register: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:269` —
  `| chousa | round3 | S100` | the gate block named no locator, so no quote was checked | #### Gate — S100 |`
  (in section "Rows whose quotes were NEVER CHECKED", rows: 109)
- Census finding (`quote-lint-full-v5.json`, same in v4):
  `{"lane":"chousa","round":"round3","id":"S100","verdict":"no-locator","detail":"#### Gate — S100"}`

## Identity: census id ≠ current id (renumbered since the census)

- `lanes/chousa/round3/SOURCES-PROPOSED.md` today holds rows S105–S115; no S100.
- By URL, census `round3/S104` = jstage `kenkokyoiku` = current **S109**; S105 = jaohfa = current **S110**; S110 = coling CorFEVER = current **S115**. Constant offset **+5**.
- Therefore census `round3/S100` = current **`lanes/chousa/round3/S105`**, the
  own-work row citing `chousa-shokunin/corpus/knowledge/chain-resolution-r3.md`
  (gate block at SOURCES-PROPOSED.md:35-43).
- (Cross-read: the literal current id `S100` is round2's zcmu CNKI .doc row;
  it has a URL locator and verifies too — see "Cross-check" below. Both
  readings resolve; neither is unverifiable.)

## Why the census emitted `no-locator` (checker defect, reproduced)

`quote-lint.py` run today on the current file still yields `url: None, local: None`
for S105–S108 (all four own-work rows — explains why register groups S100–S103):
```
python3  (module import; ql.block_url / ql.local_locator on bound blocks)
S105 | explicit: True | url: None | local: None     (S106–S108 identical)
```
- `block_url` (quote-lint.py:323) needs `URL_LINE_RE` = a bare `URL:` line; the
  gate writes `URL (repository locator): https://github.com/VeigaPunk/shokunin`
  → no match. Row source is `corpus/knowledge/chain-resolution-r3.md`, no http → None.
- `local_locator` (quote-lint.py:348) matches `Local artifact:
  `chousa-shokunin/corpus/knowledge/chain-resolution-r3.md`` but only tries
  `Path(raw)` (cwd-relative) and `lane_dir / raw` =
  `…/lanes/chousa/chousa-shokunin/corpus/…` — a nonexistent path. The path is
  **fleet-relative** (`~/Projects/shokunin/`); `local_locator` never joins the
  fleet root, although its own `local_candidates` index does scan
  `fleet/<lane>-shokunin/corpus`. Blind spot, per code read.

## Byte evidence (artifact present, pin matches, quotes verify)

- File: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/chain-resolution-r3.md`
  `sha256 d794343f8528e263…`, **15,772 B**, mtime 2026-10-19 17:05 -0300 —
  matches the row's anchor pin `sha256 prefix d794343f8528e263, 15,772 bytes`.
- `soffice`/no fetch needed; all four gate quotes verify by punctuation/whitespace fold
  (exact substring fails only because the md hard-wraps ~col 78; my fold strips
  whitespace + `*`/` ``):
  - Q1 "The mode verifies anchor EXISTENCE … neither reported nor required" →
    file lines **107–109** (list item, wrapped)
  - Q2 "**Not semantic support or agreement.** … never parses meaning." →
    lines **133–137** (quote is a sentence-prefix of the item — covered)
  - Q3 "**Not source truth and not external verification.** … cannot resolve
    in this mode." → lines **148–153**
  - Q4 "**One hop, one source, no transitivity.** … no chain-level entailment
    is attempted." → lines **154–156**
- Corroborating cite inside the gate (`research-gate.sh` verify_chain): format
  strings are verbatim in the file but line cites drifted — `…at=$PROBE_AT
  verdict=$verdict` is **line 2622** (cited :2321) and `printf
  'RESOLVED_HOPS=%d/%d\n'` is **line 2666** (cited :2449). research-gate.sh is
  8,812 lines, mtime 2026-10-24 04:26 (after the row's 10-23 open): pointer
  drift on a live file, content matches — stale annotation, not a defect.

## Cross-check: literal current id `S100` (round2 zcmu .doc)

- Gate `#### Gate — S100`, `lanes/chousa/round2/SOURCES-PROPOSED.md:97-104`:
  URL + "Opened: 2026-10-23 (HTTP 200, 801,280 bytes)".
- Local capture (no fetch): `.qcache/b539a80218080da56a75b624.raw` =
  sha256(url)[:24] of the cited URL; **801,280 B** (matches gate count),
  sha256 `46d1866ce9afd516…`, mtime 2026-10-23 20:36; `file` = Composite
  Document V2, Word, 5 pages. The `.txt` sibling is a UTF-8-mojibake dump
  (`efbfbd` replacement bytes) — explains the earlier false `ABSENT` on
  census-id round2/S095 (v1 full.json had it as round3/S100 pre-insert).
- Reproduced the lane's decode: `soffice --headless --convert-to
  'txt:Text (encoded):UTF8'` → 2,321 B UTF-8 text. Quotes:
  - `"…如果引文出现了任一合作者，那么这条引文将被认定为自引"` **exact** at
    byte 366 (char 144) — incl. U+4E00 一, matching the gate's hazard note.
  - opening `"中国知网他引频次的查询需要使用中国引文数据库"` — folds only
    (doc has 《…》); `"成功登录中国引文数据库后，可按题名作者单位等方式查询…"`
    — folds only (doc has 《》, “ ” marks). Both present under punct-strip.

## Residual risk / gaps

- `no-locator` is checker-attributable to the fleet-relative-path blind spot;
  the same defect quarantines S101–S103 (current S106–S108) — siblings
  QuarantineS101–S103 should find identical mechanics.
- Register's `round3` label is census-time numbering; readers matching it
  against current files will mis-bind (S100 current = zcmu, different row).
- Not re-run: full quote-lint (would need no network anyway; reproduction was
  per-function on the current file). No external fetch performed; L0 stays open.

Report: `.ufo/waves/round-48/w2/QuarantineS100.md`
