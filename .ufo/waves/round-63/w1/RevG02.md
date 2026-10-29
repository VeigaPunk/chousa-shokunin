# RevG02 — review of the G02 knowledge-index gate

Scope: the G02 rule in `corpus/evidence/round63/controls/pos-ref-preflight.py` (docstring line 17; `g02` lines 86-93; `main` lines 183-223), the G02 bullet of `corpus/evidence/round63/claims.md` (lines 42-43), and the frozen battery docstring (`c1-battery.py` lines 1-42). Read-only on the lane; no file under `corpus/evidence/round63/`, `tools/`, `corpus/` or `SKILL.md` was edited. No git, network, fleet or sibling writes.

## Method

- Golden copy built with the frozen `build_golden` (imported from `c1-battery.py`, writes only to scratch): 11335 files; base run `GATE G02 knowledge-index PASS 84 entries indexed`, `PREFLIGHT=7/7`, rc 0.
- 24 single-change cases, one copy each in scratch, each run as
  `python3 -B pos-ref-preflight.py --root <copy> --fleet /home/vgpnk/Projects/shokunin --skip G08 --work <scratch>` (driver: scratch `drive.py`; 43 s wall, 8 parallel).
- 9 probes (B1-B9) for usage, encoding and symlink inputs, run with `--only G02` where the other gates add nothing.
- "Expect" below is my reading of the docstring ("an index row is a claim") and of the claim text; where it is interpretation it is marked INFERENCE.

## Case results (G02 line as printed by the reference)

| case | input | G02 line observed | expect | class |
|---|---|---|---|---|
| fn_substring_longer | new `corpus/knowledge/verified-r9.md`; README names only `archives-verified-r9.md` (README: 2 hits for each name) | `PASS 85 entries indexed` | FAIL | D1 |
| fn_url_only | `url-only-r63.md` named only as `https://example.invalid/corpus/knowledge/url-only-r63.md` in README | `PASS 85 entries indexed` | FAIL (INFERENCE) | D3 |
| fn_codespan_prose | `codespan-r63.md` named only in a prose code span | `PASS 85 entries indexed` | FAIL (INFERENCE) | D3 |
| fn_struck_row | `struck-r63.md` named only in `~~\| knowledge/struck-r63.md \| retired \|~~` | `PASS 85 entries indexed` | FAIL (INFERENCE) | D3 |
| fn_subdir_entry | `corpus/knowledge/nested/nested-r63.md`, not indexed | `PASS 84 entries indexed` | FAIL (scope, INFERENCE) | D4 |
| fn_nonmd_entry | `plain-r63.txt`, `UPPER-r63.MD`, not indexed | `PASS 84 entries indexed` | FAIL (scope, INFERENCE) | D4 |
| fn_hidden_entry | `.hidden-r63.md`, not indexed | `FAIL 1 not named ...: .hidden-r63.md` | FAIL | ok (pathlib `*` matches dotfiles) |
| fn_dangling_row | `derived-output-safety-r61.md` deleted; README still names it (2 hits) | `PASS 83 entries indexed` | FAIL (INFERENCE) | D5 |
| fn_knowledge_dir_removed | `corpus/knowledge/` removed | `PASS 0 entries indexed` | FAIL | D2 |
| fn_knowledge_is_file | `corpus/knowledge` replaced by a regular file | `PASS 0 entries indexed` | FAIL | D2 |
| fn_knowledge_unreadable | `chmod 000 corpus/knowledge` (uid 1000) | `PASS 0 entries indexed` | FAIL | D2 |
| fp_underscore_escape | `escaped_r63.md`; README row `knowledge/escaped\_r63.md` (markdown-escaped underscore) | `FAIL 1 not named ...: escaped_r63.md` | PASS | D6 |
| fp_pct_link | `gate notes r63.md`; README `[gate notes](knowledge/gate%20notes%20r63.md)` | `FAIL 1 not named ...: gate notes r63.md` | PASS | D7 |
| fp_nfd_name | `café-r63.md` (NFC bytes); README names it in NFD | `FAIL 1 not named ...: café-r63.md` | PASS? (ambiguous) | D8 |
| crash_nonutf8_entry | knowledge file `bad-\xff-r63.md`, not indexed | `FAIL 1 not named ...: bad-<0xFF byte>-r63.md` (raw byte on stdout, no traceback) | FAIL, clean line | D10 |
| valid_nonutf8_readme | README with a junk line `\xff\xfe` not naming anything | `PASS 84 entries indexed` | PASS | ok (errors=replace) |
| valid_empty_entry | empty indexed `empty-r63.md` | `PASS 85 entries indexed` | PASS | ok |
| crash_readme_empty | `corpus/README.md` empty | `FAIL 84 not named ...` | FAIL | ok |
| crash_readme_dir | README replaced by a directory | `FAIL corpus/README.md absent` | FAIL | ok (message wrong, see note N1) |
| crash_readme_fifo | README replaced by a FIFO | `FAIL corpus/README.md absent` (returned, no hang) | FAIL | ok (message wrong, N1) |
| crash_readme_unreadable | `chmod 000` README | `FAIL gate crashed: PermissionError ...` | FAIL | ok |
| crash_knowledge_fifo | FIFO `fifo-r63.md`, not indexed | `FAIL 1 not named ...: fifo-r63.md` (no hang) | FAIL | ok |
| crash_corpus_missing | `corpus/` removed | `FAIL corpus/README.md absent` | FAIL | ok |
| probe B1 | `--root <nonexistent>` | stderr `not a directory`, rc 2 | usage, rc 2 | ok (not a pass) |
| probe B2 | `--root <a regular file>` | stderr `not a directory`, rc 2 | usage, rc 2 | ok |
| probe B3 | `--root <empty dir>`, `--only G02` | `FAIL corpus/README.md absent`, rc 1 | FAIL | ok |
| probe B4 | `--work <existing regular file>` | Python traceback `FileExistsError` from `main`, rc 1, no GATE lines | usage, rc 2 | D9 |
| probe B5 | README is a symlink loop | `FAIL corpus/README.md absent` | FAIL | ok (message N1) |
| probe B7 | `--root` golden, README got an invalid byte inside a *second* mention of `archived-export-intake.md` | `PASS` | (not a defect: the name is indexed elsewhere) | none |
| probe B8 | knowledge entry is a dangling symlink, name indexed | `PASS 85 entries indexed` | FAIL (INFERENCE) | D4 |
| probe B9 | golden, `--only G02` | `PASS 84 entries indexed`, rc 0 | PASS | ok |

## Defects

Each id is one defect class; inputs are the cases listed. Counts are defect classes.

- **D1 false_negative — substring match.** `g02` uses `f not in readme` (line 92). Input: `corpus/knowledge/verified-r9.md`, with README naming only `archives-verified-r9.md`. Observed: `GATE G02 knowledge-index PASS 85 entries indexed`. The gate counts a name as indexed when it is a suffix of another name. The same holds for any short name that is a substring of a longer indexed one (`r9.md`, `r31.md`). Fix: whole-token match, `re.search(r"(?<![\w.-])" + re.escape(f) + r"(?![\w.-])", readme)`.
- **D2 false_negative — vacuous pass on a missing, non-directory or unreadable index.** Lines 91 (`if kd.is_dir() else []`) and `glob` silently yields nothing on a permission error. Inputs: `corpus/knowledge` removed; replaced by a file; `chmod 000`. Observed in all three: `GATE G02 knowledge-index PASS 0 entries indexed` (rc is 1 only because G01/G04/G05 fail in those copies, not G02). Fix: FAIL if `kd` is not a directory, if `os.access(kd, R_OK|X_OK)` is false, if iterdir raises OSError, or if zero `*.md` entries exist.
- **D3 false_negative (calibration) — a name counted as an index row when it is only a URL, a code span or struck out.** Inputs: `fn_url_only`, `fn_codespan_prose`, `fn_struck_row`; all `PASS 85 entries indexed`. The docstring says "an index row is a claim", which these are not. Fix: strip `~~…~~`, `<!-- … -->` and fenced blocks from the README first, then require the name in a table cell `` `knowledge/NAME` `` or a link target `](…/NAME)`. This changes the frozen rule's wording; route as a limit for the next battery, do not edit the frozen candidate.
- **D4 false_negative (scope) — entries the glob never sees pass silently.** Inputs: `corpus/knowledge/nested/nested-r63.md` (subdirectory), `plain-r63.txt` and `UPPER-r63.MD` (non-`*.md`), dangling symlink `dangling-r63.md` (B8). All `PASS`. Fix: walk `corpus/knowledge/**`; every non-directory entry must be a regular `*.md` (allowlist `.gitkeep`), subdirectory `*.md` files are checked the same way, a broken symlink is FAIL.
- **D5 false_negative (calibration) — a dangling index row passes.** Input: README still names `derived-output-safety-r61.md`; the file is deleted. Observed `GATE G02 knowledge-index PASS 83 entries indexed`. G02 only checks files → README, never README → files. Fix: for each `knowledge/NAME.md` token in the README, FAIL unless `kd/NAME.md` is a regular file.
- **D6 false_positive — markdown-escaped underscore.** Input: row `knowledge/escaped\_r63.md` for file `escaped_r63.md`. Observed `FAIL 1 not named in corpus/README.md: escaped_r63.md`. A valid index in rendered markdown. Fix: unescape `\_` (and `\*`, `\[`, `\]`) before matching.
- **D7 false_positive — percent-encoded link target.** Input: `[gate notes](knowledge/gate%20notes%20r63.md)` for `gate notes r63.md`. Observed `FAIL ... gate notes r63.md`. Fix: `urllib.parse.unquote` the README text before matching (or match both the raw and unquoted forms).
- **D8 false_positive (ambiguous, low) — Unicode normalisation.** Input: NFC `café-r63.md`, README in NFD. Observed `FAIL ... café-r63.md`. Linux names are bytes so the mismatch is real, but a reader would call the entry indexed. Fix if wanted: `unicodedata.normalize("NFC", …)` on both sides.
- **D9 crash — `--work` is a regular file.** Input: `--work <file>` (B4). Observed a Python traceback (`FileExistsError: … File exists`) from `main`'s `work.mkdir`, rc 1, no GATE or PREFLIGHT line. Not a pass, but not the contract's usage exit 2 either. Fix: wrap the `mkdir` in a try, `OSError` → message to stderr, return 2 (usage).
- **D10 crash (output) — invalid UTF-8 on stdout.** Input: knowledge file `bad-\xff-r63.md`. Observed (`od -c`): the G02 line contains the raw byte `377` (not valid UTF-8); no traceback, but the line cannot be decoded strictly by a consumer. Fix: print names with `f.encode("utf-8", "surrogateescape").decode("utf-8", "backslashreplace")` (or `ascii()`).

Note N1 (message, not counted): the detail `corpus/README.md absent` is printed for a README that is a directory, a FIFO or a symlink loop; the message should read `is not a regular file`.

No hang observed: FIFO README (returns at once via `is_file`), FIFO knowledge entry (names only, never opened).

## Claim-file notes (routed, not edited)

- claims.md line 42: "every file name of `corpus/knowledge/*.md` occurs in `corpus/README.md`". The word "occurs" is undefined (it is a substring test); the clause says nothing of a missing directory, a subdirectory, or the README → files direction.
- The docstring's parenthetical "(an index row is a claim)" is not in the claim text: the claim and the reference differ in intent.
- The claims' Named limits (lines 104-109) disclose that G04 and G05 are lexical. G02's substring, vacuous-pass and entry-scope behaviour is not disclosed. This is an undisclosed limit: route it to the erratum, not an edit.
- The frozen battery's G02 legs (D04 unindexed entry, D05 lost mention) use the candidate's own naming; none of D1-D10 is exercised. A tool that adopts the fixes above passes the battery unchanged; the battery does not detect these classes.

## Verification gaps

- G08 not run (battery and mandate skip it). Other gates' behaviour (G01, G04, G05 in the vacuous cases) observed only as side effects, not reviewed.
- D3, D5, D8 and the scope items in D4 rest on the docstring intent; they are INFERENCE for the frozen rule, which the claim text does not fully specify.
- No battery run and no candidate patch; the fixes above are proposals for the L1 and the next round.

## Tooling

No tool installed or upgraded. Scratch `/fast/scratch/hyaku/chousa-r63/RevG02/` (golden, cases, probes, drive.py, results.json) removed before yield.

VERDICT: GATE_DEFECTS=10 fn=5 fp=3 crash=2 gate=G02
