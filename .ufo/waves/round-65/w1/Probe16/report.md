# Probe16 — round65 receipt absolute-path probe (isolated fixture)

Seat: Probe16 (leaf, lane chousa round65). Scope: one surface only — the path field of the
`SHA256=` header line of a receipt, probed against the frozen reference
`corpus/evidence/round65/controls/ref-receipt-pin.py` (production `tools/receipt-pin.py`
absent at freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd — verified by directory listing).
No production writes; no git mutations outside the scratch fixture repo; full battery NOT run.

## Frozen format basis (claims.md C1, independently derived expectations)

- Header grammar: `REVISION=<40 lowercase hex>`, `EXIT=<decimal 0..255>`,
  `SHA256=<64 lowercase hex> <canonical relative POSIX path>`, blank separator, nonempty body.
- "Digest binds the Git blob at the declared revision; revision must equal caller-supplied
  --revision. No working-tree hashing. 0 consistent, 1 invalid, 2 usage/environment."
- Predicate boundary used for pass/fail: exit code exact; stdout exact `RECEIPT_PIN=PASS`
  for rc 0, `RECEIPT_PIN=FAIL ` prefix class for rc 1 (mirrors frozen c1-count check).

## Fixture (all under scratch `/fast/scratch/hyaku/chousa-r65/Probe16/`, deleted on exit)

- Fresh `fixture-repo` (`git init -q -b main`), toplevel asserted == fixture dir before any
  mutation; committed `payload.txt` + `sub/note.txt`; REV and blob digest taken via
  read-only `git -C ... cat-file`. TMPDIR pinned inside scratch.
- Driver `probe16-abs-fixture.py` builds 11 receipts and runs the reference with
  `--root fixture-repo --revision REV`; receipts preserved in `probe16-abs-cases/`,
  full run log in `probe16-abs-results.txt`. Driver rc 0.

## Result: PROBE16_ABS=11/11 PASS

| case | path field | expected | observed | verdict |
|---|---|---|---|---|
| valid-relative | `payload.txt` | 0 PASS | 0 PASS | OK (fixture can pass) |
| abs-real-file | `/fast/.../payload.txt` (exists on disk, hashes to the declared digest) | 1 FAIL | 1 FAIL path | OK |
| abs-root-style | `/payload.txt` | 1 FAIL | 1 FAIL path | OK |
| abs-double-slash | `//payload.txt` | 1 FAIL | 1 FAIL path | OK |
| dot-prefix | `./payload.txt` | 1 FAIL | 1 FAIL path | OK |
| dotdot-mid | `sub/../payload.txt` | 1 FAIL | 1 FAIL path | OK |
| trailing-slash | `payload.txt/` | 1 FAIL | 1 FAIL path | OK |
| empty-path | `SHA256=<hex>␣` (space, no path) | 1 FAIL | 1 FAIL digest header | OK |
| no-path-field | `SHA256=<hex>` (no space/path) | 1 FAIL | 1 FAIL digest header | OK |
| windows-abs | `C:\payload.txt` | 1 FAIL | 1 FAIL blob/digest | OK |
| wrong-digest-valid-rel | `payload.txt` + `0`*64 | 1 FAIL | 1 FAIL blob/digest | OK |

Strongest signal: **abs-real-file** — an absolute path naming a real, correctly digested file
is still rejected. Acceptance requires the canonical relative POSIX form; absolute paths can
never satisfy the frozen format regardless of filesystem truth. `windows-abs` shows a
non-POSIX absolute is not classified `path` but dies at the blob/digest stage with the same
exit 1 (class is reference detail, exit code is frozen). `wrong-digest-valid-rel` confirms the
relative-path gate alone does not pass receipts — the digest must bind the blob at REV.

## Exit-code taxonomy anchors (recorded, separate from the 11 case surfaces)

- `--revision` uppercase → **exit 2** via argparse `error: --revision requires full lowercase
  object id`. Exit 2 is reachable for CLI usage violations.
- **Unreadable receipt file → exit 1** (`RECEIPT_PIN=FAIL [Errno 2] No such file or
  directory: ...`), not exit 2. Finding for L1: the reference docstring says
  "2 usage/environment", but environment errors on the receipt-read path are caught by the
  same `(OSError, ...)` handler as malformed content and fold into exit 1. In this reference
  the exit-2 surface is usage-only. If the production tool must honor "environment → 2",
  this is a divergence to fix before C1 scoring; frozen C1 cases never exercise it, so the
  20/20 predicate is unaffected either way.
- Corollary class note: `empty-path` reports error class `digest header` (header regex needs
  ≥1 char after the separating space) rather than `path`; exit code 1 matches the frozen
  format either way. Exact error-class text is reference detail, not frozen.

## Constraints honored / records

- Install record: none — probe used only system `python3` 3.14.8 (`/usr/bin/python3`) and
  `git` (`/usr/bin/git`); no uv/npx/binary/pacman transactions (pacman paused host-wide).
- Read-only git in lane used explicit `-C`; the only git mutations were inside the scratch
  fixture repo after a toplevel assertion. No clone was taken (0 of max 1).
- Scratch deleted on exit after receipts were copied here; no `/tmp` evidence.
- Files written by this seat: this report, `probe16-abs-fixture.py`,
  `probe16-abs-results.txt`, `probe16-abs-cases/*.txt` — all inside
  `.ufo/waves/round-65/w1/Probe16/`; plus the lane trailer mirror `.ufo/waves/round-65/w1/Probe16.md`.

## Risks / notes for L1 integration

1. Environment-error → exit-code mapping (1 observed vs 2 documented) is the only semantic
   divergence candidate surfaced; decide whether production must match docstring or freeze.
2. Probe covers the reference only; production `tools/receipt-pin.py` still needs the frozen
   C1 counter run by L1 after integration.
3. Error-class strings (`path`, `digest header`, `blob/digest`) are consistent across runs
   here but are not part of the frozen predicate; do not assert them in counters beyond the
   `RECEIPT_PIN=FAIL ` prefix.

Report: .ufo/waves/round-65/w1/Probe16.md
