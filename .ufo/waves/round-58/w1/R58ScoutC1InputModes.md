# R58ScoutC1InputModes — C1 input-mode findings

Scope: frozen round-58 C1 claim/counter and pinned builder input paths. Source reads are read-only. No live fetch. No LSP device was available; symbol locations below are direct source line evidence, not semantic LSP results.

## Frozen context

- `corpus/evidence/round58/claims.md:5-11` defines C1's bounded battery: foreign span, symlink output/cache, FIFO/device, raw 64 MiB cap, quotes 100,000-row cap, output containment and `..` entry refusal. It does not claim general race safety.
- `corpus/evidence/round58/c1-count.py:14-22` enumerates legs/reason classes; `:252-295` specifies FIFO_TXT, DEVZERO_TXT and 80 MiB OLE-headed FAT_RAW; `:150-160` requires a reason token in stderr/stdout. `:297-306` makes MANY_QUOTES 100,001 rows; `:308-317` covers `..`.
- `sha256sum tools/build-spans.py corpus/evidence/round58/controls/build-spans-r55.py` observed both `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` (the claims' r55 pin). `tools/capture-text.py` hash observed `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`.
- Frozen `corpus/evidence/round58/controls/c1-before.txt:1-16` records `FOREIGN` deleted, `SYMLINK_OUT` target written, `.txt` symlink accepted, FIFO_TXT and DEVZERO_TXT refused without required reason token, FAT_RAW refused with `ole-malformed` (not SIZE), MANY_QUOTES accepted; `C1=FAIL`.

## Code paths

- `tools/build-spans.py:63-92` `Forms.get`: memoizes by URL (`:69-70`); constructs `.raw` and `.txt` cache paths (`:71`). It checks `raw.is_file()` and opens/reads 8 header bytes (`:74-76`); `pathlib.Path.is_file()` follows symlinks and is false for FIFO/device nodes. OLE magic or ZIP local-header magic selects raw path (`:77`); lazily imports capture-text, then unbounded `raw.read_bytes()` and SHA256 (`:78-82`). Exceptions from `text_form` are converted to a refusal string (`:83-84`), but `raw.read_bytes()` is outside that try. Otherwise an existing `.txt` is read without size bound, UTF-8 decoded with replacement and newline-normalized (`:85-88`). Missing/unsupported inputs return `no defined text form` (`:89-90`).
- OLE and ZIP: dispatch is by first 8 bytes (`OLE`) or first 4 (`ZIP`); neither extension nor content validation is otherwise performed by Forms. `capture-text.py:389-402` reads OLE up to MAX_PART+1 (256 MiB), checks its own size only after reading, then parses; ZIP delegates to `zipfile.is_zipfile` and package processing. Thus capture-text's cap is not the C1 64 MiB cap, and the builder's earlier `read_bytes()` is itself unbounded. Malformed input can be refused by capture-text but does not thereby meet the frozen SIZE reason.
- `.txt`: only selected if raw is not a regular file with recognized magic (`:85-90`). `.txt.is_file()` follows symlink to a regular target, so symlinked `.txt` is read; a symlink to `/dev/zero` is not considered a regular file and is skipped. FIFOs/devices also fail `is_file()` and are skipped rather than opened, unless a concurrent replacement races the check/open. If a raw FIFO/device is present, it is skipped and `.txt` fallback remains possible.
- Missing raw: missing or non-magic `.raw` plus missing `.txt` returns the generic no-defined-form refusal (`:89-90`). A non-magic regular `.raw` is ignored in favor of `.txt` when present. Raw symlinks to regular recognized files are followed and processed.
- `read_quotes`: `:95-124` calls `path.is_file()` (thus follows symlinks to regular files; rejects FIFO/device as “no input”), then unbounded `read_text(...).splitlines()`; checks header/cells, IDs, same-SID URL and lane-relative `..` policy. There is no row/byte cap here. `build` (`:127-154`) processes all rows before writes; refusal exits before writing. Output then creates `out/spans`, removes unlisted `SPAN_RE` files, and writes manifest/files (`:201-208`); no symlink/type guard is present in this pinned builder.

## Targeted probes actually run

Scratch `/fast/scratch/hyaku/chousa-r58/R58ScoutC1InputModes` was removed before reporting. Probe commands used copied builder/capture-text only, with scratch as cwd/cache/output; no lane file was modified.

1. `.raw` symlink pointing to committed S101 OLE capture. Command: `python3 -B "$S/build-spans.py" --quotes "$S/q-rawlink.tsv" --out "$S/out" --cache "$S/cache"`. Output: `QUOTE S701 char 12033 spans/S701-1.txt`; `SPANS_ROWS=1 WRITTEN=1`; `PROBE_A_RC=0`. This demonstrates this builder accepts a `.raw` symlink; the frozen cache symlink leg covers only `.txt`, so this input form is outside the battery.
2. `.raw` FIFO, no `.txt`: `timeout 3s python3 -B "$S/build-spans.py" --quotes "$S/q-rawfifo.tsv" --out "$S/out-fifo" --cache "$S/cache"`. Output: `PROBE_B_RC=1`; stderr `build-spans: refused S702: no defined text form for c647ba2bf99fab1a068810af (raw neither OLE nor zip, no .txt)`; `OUT_EXISTS=no`. This observed path does not block, but its generic reason would not meet the battery's FIFO/NOT_REGULAR reason classes if applied to a `.raw` FIFO (the frozen leg uses `.txt` FIFO).

## Mismatches / limits

- Confirmed against frozen C1: the pinned builder does not satisfy the hazard battery. The frozen before-receipt already reports 0/7 refusal legs passing. Specifically, `.txt` symlink is followed; FIFO and device are skipped but reason strings lack accepted class tokens; FAT_RAW is refused as malformed OLE rather than due to the required >64 MiB SIZE reason; 100,001 rows have no cap and are accepted; output symlink follows through to target and writes. The builder reads raw and text inputs with unbounded `read_bytes`/`read_text`.
- Battery coverage gap: it does not test `.raw` symlinks/FIFOs/devices, `--quotes` symlink/FIFO, `.txt` size, cache-directory symlink, or `out/spans` symlink. The observed `.raw` symlink success confirms one such gap; raw FIFO probe confirms nonblocking generic refusal but not required reason naming. No conclusion about broader races is claimed.
- The frozen `c1-before.txt` is a receipt, not a run performed for this report. Targeted probes above are the only commands run here. No current candidate C1 counter run was performed.

VERDICT: The pinned round-55 input-mode attack survives: confirmed `.raw` symlink acceptance and frozen receipt falsifies the required C1 hazard behavior; raw FIFO did not hang in the targeted probe but its generic reason is outside frozen reason classes.