# ExecRecheckSweep — round-49 w1: recheck normalisation sweep over staged SOURCES.append.md

Scope: classify every staged row's recheck cell with the tool's own logic
(`RECHECK_RE` / `LEAD_RE` from `chousa-shokunin/tools/assimilate-rows.py`, copied
verbatim, tool file untouched), and count pipe carriers and no-URL rows.
Input (read-only): `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md`
(120 lines, 114 data rows S082–S195). No installs performed (none needed;
pacman guard noted — nothing installed). No files written outside this report.

## Method (commands run, observed output)

Scratch script `/tmp/chousa-r49-ExecRecheckSweep/recheck-sweep.py` (deleted after)
imports the tool module without executing main():

```
spec = importlib.util.spec_from_file_location("assimilate_rows", TOOL)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
RECHECK_RE, LEAD_RE, ESC_SPLIT, url_of = mod.RECHECK_RE, mod.LEAD_RE, mod.ESC_SPLIT, mod.url_of
```

Run 1 — `python3 .../recheck-sweep.py` (observed output, verbatim):

```
imported: /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/assimilate-rows.py
RECHECK_RE = ^(\d{4}-\d{2}-\d{2}|\d+d|[A-Za-z][A-Za-z0-9 _-]*)$
LEAD_RE    = ^\s*(\d{4}-\d{2}-\d{2}|\d+d)\b
ESC_SPLIT  = (?<!\\)\|
TOTAL_ROWS=114
RE-CHECK census-valid  = 0
RE-CHECK reducible     = 114
RE-CHECK would-refused  = 0
ROWS cells carry pipe   = 1 (escaped 1, literal/extra 1)
ROWS no http(s) URL     = 11
ROWS cell-count != 11   = 0
-- would-be-refused row ids --

-- rows with cells != 11 (inspect) --
-- rows with no http(s) URL --
S105 S106 S107 S108 S179 S184 S188 S189 S191 S192 S194
-- escaped-pipe rows --
S097
```

Classification rule (mirrors tool `assimilate-rows.py:198-205`): recheck cell is
census-valid if `RECHECK_RE.match` (whole-cell date / `NNd` / symbolic cadence);
else reducible if `LEAD_RE.match` (leading date/`NNd`, prose stripped); else would
be refused. Cells parsed with the tool's `ESC_SPLIT` (escaped `\|` kept whole);
schema expects 11 cells (`assimilate-rows.py:152`), URL via `url_of` (`:63-69`).

Run 2 — `python3 .../recheck-detail.py` (observed output, verbatim):

```
leading-prefix distribution (reducible rows):
  180d	79
  365d	26
  90d	9
```

No date prefixes, no cadence-only cells: all 114 recheck cells carry `NNd`
prose; the reducible set is exactly the full row set. The 10th cell (recheck)
never itself caused a refusal.

Run 3 — cross-check, naive plain `|` split + empty-cell scan:
`python3 - <<'EOF' ... EOF` → `rows: 114`, `rows with empty cell: 0`,
`plain-split rows != 11 cells: [('| S0', 22, 13)]`. Line 22 is S097; its only
pipe is the escaped `\|` pair (13 raw fragments vs 11 ESC cells). Therefore:
**literal pipes inside cells: 0; escaped pipes: exactly 1 (S097)**. S097's
recheck cell: `180d — re-open the dataset page and confirm the label list still
reads "SUPPORTS\|REFUTES\|NOT ENOUGH INFO" (ran 2026-10-23)` — tool rewrite
(`:193-195`) would render it `SUPPORTS / REFUTES / NOT ENOUGH INFO` in append
output; not a refusal.

## Counts (deliverable)

| metric | count | ids |
|---|---|---|
| staged rows total | 114 | S082–S195 |
| recheck census-valid | 0 | — |
| recheck reducible (leading date/NNd) | 114 | all (79×180d, 26×365d, 9×90d) |
| recheck would-be-refused | 0 | (none — empty list) |
| rows whose cells carry a pipe | 1 | S097 (escaped `\|`; 0 literal) |
| rows with no http(s) URL | 11 | S105, S106, S107, S108, S179, S184, S188, S189, S191, S192, S194 |

## No-URL rows (why)

- S105–S108: lane-local own-work rows; source cell names a corpus path + sha256
  prefix, no URL by design (e.g. S105: `chousa chain-hop resolution entry —
  corpus/knowledge/chain-resolution-r3.md (lane-local artifact)`).
- S179/S184/S188/S189/S191/S192/S194: rows whose source is a `本地存档` local
  evidence copy (rounds 13–16, named `.html`/`.txt` files with byte counts and
  sha256), e.g. S184 `本地存档 round13/evidence/en-nmpa-abolished-regulations.html
  (12,700 B, sha...`. All 11 would be refused by the tool *if cited* (`:154-155`).

## Calibration vs C2 adopt (cited set S087,S088,S089,S091,S092,S100,S101,S102,S103)

Verified per cited row (11 cells, URL present, recheck leading `NNd`): all nine
pass — none is in the no-URL list, none has a cell-count defect, none would be
refused. Examples: S087 `180d — re-open the NII manual ...` url=True ncells=11;
S092 `365d — re-open the ERIC record ...` url=True ncells=11; S103 `180d —
re-download the PDF ...` url=True ncells=11. So the round-49 C2 append run
refuses nothing on recheck/URL/schema grounds; every append row's recheck column
reduces to the bare `NNd` prefix and the stripped prose lands in `stripped.tsv`
(`:204-205`).

## Risks / notes

- S097's escaped pipe is the only cell-content pipe; it is not in the cited set,
  so it does not affect the C2 append (it would surface in any future entry that
  cites S097 as a `cell10-pipe` strip, not a refusal).
- All 114 recheck cells are *reducible*, never already census-valid — i.e. the
  staged package carries no pre-normalised recheck values; the tool will rewrite
  every one at append time.
- No tooling installed; no git operations; no production file touched; scratch
  dir `/tmp/chousa-r49-ExecRecheckSweep` deleted before finishing (verified gone:
  `ls /tmp | grep chousa-r49` no longer lists it).

VERDICT: recheck-normalisation sweep over all 114 staged rows — 0 census-valid,
114 reducible (all `NNd`-leading), 0 would-be-refused; 1 pipe-carrying row
(S097, escaped `\|` only), 11 no-URL rows (S105–S108 lane-local, S179/S184/S188/
S189/S191/S192/S194 local-archive), none in C2's cited set — no refusals for the
round-49 C2 adopt.
