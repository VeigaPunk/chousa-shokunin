# R84ExecForge — C1 K2 spec-generalization (kill-rule fire test)

Axes: 1) does the landed tool refuse every in-class forgery it contracts to refuse;
2) does it refuse genuine records (K3 harm); 3) are setup/usage errors reported as exits 2.

## Config

- Tree: `git archive 03bbb4580b39b442be69f998fae2db48d64b8c93` → scratch
  `/fast/scratch/hyaku/chousa-r84/R84ExecForge/tree` (copied to wave folder `forge/` below).
- Tool: `tree/tools/gate-records.py` (docstring lines 1–53) via public CLI:
  `python3 tools/gate-records.py verify --root <tree> --repo /home/vgpnk/Projects/shokunin/chousa-shokunin <files>`
  run from the tree root.
- Bases: 15 frozen positives `corpus/evidence/round84/c2-positives.tsv` (S199–S211/S028),
  3 round-84 lesson records `corpus/lessons/round-84.md` lines 18–20 (S214/S018/S023), and
  the unreach S208 record (positives line 10).
- Battery: 56 primary forgeries + 22 extra probes in `forge/` (batch transcript
  `forge/out-batch.txt`), plus singles runs. Each file: 1 record at line 2 (F042 fenced at
  line 3), preamble/postamble prose only.

Result headline: **no in-class forgery was accepted (OK, rc 0) and no in-class line was refused
with a code outside the frozen EXPECTED_CODE set — except the setup leg** (Finding 1). Two
accepted lines meet every check by design (`…`/`...`/no-suffix shorthands, NBSP/tab quotes) — none.

## Findings

### Finding 1 — K2 FIRES via setup leg (claims.md K2, fourth mutation class)

- **Command:**
  `python3 tools/gate-records.py verify --root <tree> --repo /tmp <tree>/forge/F033-line-offbyone.md`
  and `--repo <tree>/does-not-exist-xyz` (and `--repo <tree>/../norepo`, a scratch dir with no
  git history, per claims.md setup-leg text).
- **Receipt:** `forge/out-setup-leg.txt` (stdout+stderr+rc per run).
- **Observed (verbatim):**
  `GATE_RECORD ...F033-line-offbyone.md:2 S199 FAIL LINE,REV`
  `GATE_RECORDS files=1 records=1 ok=0 fail=1`, **rc=1**, stderr empty.
- **Expected (claims.md §"Setup leg"):**
  `exit 2 with GATE_RECORDS_ERROR on stderr — not FAIL REV,LINE with exit 1 — at the landing revision.`
  Verbatim: *"a rev record checked with a non-git `--repo` (a scratch directory with no git history)
  must exit 2 with `GATE_RECORDS_ERROR` on stderr — not `FAIL REV,LINE` with exit 1`*.
- **Docstring breach:** lines 50–51 — *"Exit: 0 when records >= 1 and every record is OK; 1 when any
  record fails or no record is found; 2 on usage or I/O error"*. A non-git `_repo` is an I/O/usage
  error on the rev-form code path (`git_blob` catches `OSError` only, returns None → REV), so it
  lands as a per-record FAIL with rc 1 instead of rc 2. The failure is in the **rev-form** code path
  specifically: for **admit** records (H1 with `--repo /tmp/../norepo`) the tool prints OK rc 0
  because git is never consulted — the same bad `--repo` is silently ignored for admit.
- **In-class (K2 wording covers it if the tool still misreports):** claims.md explicitly states
  *"This leg is scored by the wave's executor seat through the public CLI (K2 wording covers it if
  the tool still misreports)"*. K2 kill-rule text: *"The setup leg (non-git `--repo` exit 2 vs
  `FAIL REV,LINE` exit 1) counts as K2 if the tool misreports it."*
- **Verdict: K2 FIRES** — the setup leg misreports `FAIL LINE,REV` rc 1 where the contract requires
  `GATE_RECORDS_ERROR` rc 2. Hence **C1 does not hold under K2 as written.**

### Finding 2 — All 54 direct in-class forgeries refused with expected codes (no fire on codes)

Full batch `rc=1`: `GATE_RECORDS files=56 records=54 ok=7 fail=47`
(`forge/out-batch.txt`, single-file rc per extra probe in §Extra below).
The 7 OKs are the designed conformance/shorthand lines (F002 …-suffix, F003 no-suffix,
F005 17-hex-prefix, F021b NBSP words=13, F05xx tab-in-quote, H1 `...`-suffix, H2 no-suffix) —
each meets every docstring check; 12 OK singletons include CRLF / BOM / NBSP-all /
U+2028/U+2029 whitespace / span-quote / line-sep (see Extra). None is a forgery (`none` in table).

In-class per-gate verdicts on every mutation the brief required — all refused correctly:
sha case/case-of-hex (F001 CAPTURE_SHA); raw-vs-txt sha (F004 CAPTURE_SHA);
same-url/different-id (F006 REFETCH); failed-attempt fetched (F007 REFETCH);
trailing-slash/fragment/http-vs-https/case (F009–F012 CAPTURE_KEY,REFETCH);
tier lower-case (F013 PARSE), decision case/other (F014/F015 PARSE);
leading-zero / plus / unicode digits in words/call/armestry (F016–F020 PARSE —
fullwidth U+FF11-３, Devanagari U+096B, superscript ² — a broader class than the 9 r83 survivors);
ZWSP-in-quote (F022 QUOTE_ABSENT), curly delimiters (F023 PARSE), HTML entity (F024 QUOTE_ABSENT),
cross-capture quote incl. symbol-for-symbol identity (F026 QUOTE_ABSENT);
short/tag/HEAD/tree rev (F027–F030 LINE,REV), space/non-ASCII path (F031 PARSE, F032 LINE,REV),
line ±1 (F033/F034 LINE), admit capture=none (F035 CAPTURE_PATH+CAPTURE_SHA+QUOTE_ABSENT+REFETCH),
success-claiming unreach (F036 REFETCH), unreach+sha keyset (F037 PARSE),
words=0 (F038 WORDS), indented/tab/4-space/fenced detection (F039–F042 all detected→QUOTE_ABSENT/LINE),
extra text (F045 PARSE), dup quote key (F046 QUOTE_ABSENT,WORDS), L214 leading-zero words (F047 PARSE),
L018 tier flip (F048 TIER), L023 quote word (F049 QUOTE_ABSENT), R202 line+1 (F050/X022 LINE).

### Finding 3 — Detection exclusions behave as contracted (blockquote/list lines, no-fire)

F043 `> GATE-RECORD …` and F044 `- GATE-RECORD …` (bad-quote variants) produce **zero** `GATE_RECORD`
lines in batch and singly `--root <tree> --repo lane <file>` → `GATE_RECORDS files=1 records=0 ok=0
fail=0` **rc=1**. Docstring (line 15–16): *"A mention elsewhere in a line (inline code, list item,
blockquote, HTML comment) is prose, not a record."* Detection is `lead_strip` + `REC_RE`
(`^GATE-RECORD(?:\s|$)`) — `>`/`-` survive stripping, so these are prose, not records.
4-space indents, tab indents, BOM, and ZWSP-prefixed lines **are** detected
(F039–F042, X006/X007): *"first text, after leading whitespace and invisible format characters
(Category Cf)"*. No silent miss found in batch: 56 files → 54 records exactly (only F043/F044 skipped,
as contracted). **No fire.** (Record-line detection edge cases list: fenced blocks ARE records —
F042 ✓ detected at line 3 — unless the forger puts the line under a blockquote/list marker.)

### Finding 4 — K3 harm candidates: none (genuine conformance lines all accepted)

Every line that meets every docstring check was accepted (OK, rc 0):
`…`-suffix (F002), `...`-suffix (H1), no-suffix 16-hex (F003/H2), 17-hex still-prefix (F005),
CRLF endings (X001), NBSP-in-quote w/ words=13 (F021b, X002 all-NBSP), U+2028/U+2029 whitespace
(X004/X005), tab-in-quote (F05xx), BOM+record (X006), capture-spanning quote (X-spanquote:
12 words across capture lines 134–135, whitespace-collapsed — `…'retrieve (Figure 1).'`),
15-hex (H6) correctly **refused** CAPTURE_SHA (`<16 hex digits`, docstring line 33).
Curly-single-quote-replaced quote (X003) is a genuine wrong quote → QUOTE_ABSENT+WORDS (markup
is kept per docstring line 44).
No genuine committed record that was accepted before this round is refused at the landing revision.
**K3 does not fire.**

### Finding 5 — rev-quote class M27 extension: extra coverage holds

Counter M27 (26-word rev quote) is refused with LINE+QUOTE_LEN (x-rev26, 28 words) vs
M11 QUOTE_LEN-only for admit. Rev +1/−1 line, other-line quote, markup-stripped quote,
non-commit revs (tag/HEAD/tree/short/leading-zero-SID) all refused (REV/LINE/PARSE) —
the rev form's `QUOTE_LEN` code path and 10-hex boundary are additionally covered by
F027–F034, X022. **No fire** (no in-class acceptance, no code outside the frozen set for these classes —
all are aggravations of M11/R01 classes).

### Finding 6 — Minor: unreach success definition tighter than docstring? No — deliberate

`curl_rc=0 http=302` (x-302): FAIL REFETCH ✓ (302 is not 2xx; no matching refetch row either).
`curl_rc=0 http=200` (F036): REFETCH ✓. Invalid calendar dates `9999-99-99T99:99:99Z`
(x-fetched-9999) and `2026-13-01T…` pass `TS_RE` shape and fail correctly on REFETCH — the docstring
defines only the regex shape `fetched=<YYYY-MM-DDTHH:MM:SSZ>` (no calendar validation), so REFETCH..OK
there is **in-class-correct**: REFETCH is the frozen code for fetched-drift and the tool uses it
rather than PARSE. Not a code-finding.

## Counts (reproducible from `forge/out-batch.txt` + single receipts)

`files=56 records=54 ok=7 fail=47` (batch rc=1). Singles: 5/5 required OK-variant singles rc=0;
2/2 prose skips rc=1 (records=0); empty file rc=1 (records=0); unterminated quote PARSE rc=1;
extra probes 22/22 refused with expected codes (X003/X007 QUOTE_ABSENT-class, X008/X009 PARSE,
X010–X012 CAPTURE_PATH-class, etc.); span-markup & 302 singles rc=1 as tabled.

## Files written (all under `.ufo/waves/round-84/w1/R84ExecForge/`)

- `R84ExecForge.md` (this report; trajectory copied to `forge/`).
- `forge/` — 90 files (56 primary + 22 X-probes + 11 H/receipt singles) incl. `out-batch.txt`.
- `forge/out-setup-leg.txt` — setup-leg receipts (rc + stderr each).
- `build_forge.py`, `extra_probe.py` — generators (rewrite-safe ASCII; run inside the archive tree
  with `forge/` as output dir).

Scratch `git archive` tree and fixture repos created under
`/fast/scratch/hyaku/chousa-r84/R84ExecForge/`; `mkdir -p` first (no `/tmp` writes).
No network, no commits, no edits to `/home/vgpnk/Projects/shokunin/scripts`,
`.ufo/state`, `MANIFEST.json`, `considerthese/` or sibling repos.
Tools: system `python3` 3.14 and `git` (no installs).

VERDICT: R84ExecForge C1 fired — setup leg prints FAIL LINE,REV rc 1 instead of GATE_RECORDS_ERROR rc 2 for a non-git --repo, which K2 explicitly counts as a fire.
