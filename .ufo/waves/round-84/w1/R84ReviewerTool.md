# R84ReviewerTool — code review of tools/gate-records.py at 03bbb4580b39b442be69f998fae2db48d64b8c93 vs docstring + claims.md C1 K2/K3/K4

Scope: leaf review only. No production edits. Byte source: archive of 03bbb458…
at scratch `/fast/scratch/hyaku/chousa-r84/R84ReviewerTool/root`, tool at
`/fast/scratch/hyaku/chousa-r84/R84ReviewerTool/root/tools/gate-records.py`.
Lane checkout `/home/vgpnk/Projects/shokunin/chousa-shokunin` used only as
`--repo` (read-only `git cat-file`) and as the receipt destination. Scratch
deleted before yield (see §7).

Head note: lane HEAD is `142913a959bf99423c5546c27bb1815ed1a3a776`
(wave w1 dispatched), 2 commits past the stated identical landing/tip
`03bbb458`. The tool bytes at `03bbb458` / `f0cebde0` and at HEAD are
identical (no post-scoring change to `tools/gate-records.py`), so the
review target is unaffected.

Counter baseline (reproduced at landing):
`python3 -B corpus/evidence/round84/gate-records-r84.py --root <archive> --repo <lane>`
→ `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=288/288 EXPECTED_CODE=288/288 EMPTY_REFUSED=1/1 RC=4/4 SETUP=unscored / GATE_RECORDS_R84=PASS`, rc 0. Receipt: `counter-landing.txt`. Pre-repair tool `81b81173` → `EXPECTED_CODE=262/288 FAIL` (matches committed `c2-k0-donothing.txt` exactly); stubs accept/refuse/quote-only reproduce committed receipts exactly. Whitelist stub reproduces `FRESH_POSITIVE=2/5, EXPECTED_CODE=66/288 FAIL` **only when CWD is a lane tree** (see F-3).

## Verdict section — read first

- **K2 (in-class forgery accepted / wrong code): FIRED** — the setup leg.
  A rev record under a non-git `--repo` is reported `FAIL LINE,REV`, exit 1,
  empty stderr. claims.md C1 §4 + K2 explicitly require exit 2 with
  `GATE_RECORDS_ERROR` on stderr. This is the sole K2 firing found.
- **K3 (genuine record refused): HELD.** All 15 frozen + 5 fresh positives
  are `OK` (counter §F-5). No genuine-record refusal beyond K2-closure was
  found. One deliberate asymmetry (setup leg) is the K2 above, not a second
  defect.
- **K4 (whitelist passes counter): DOES NOT FIRE**, with a CWD fragility
  caveat (F-3). The genuine whitelist control fails the counter as claimed
  when run the way its receipt was produced.
- 11 forensic contradictions / robustness gaps below; none other fires K2
  in the frozen classes. The battery itself is not load-bearing-false:
  K0 / f1 / f2 / f3 controls reproduce.

## 1. Per-check docstring vs code (line refs: tool-at-landing.py)

**PARSE (docstring L28).** Code: `parse()` L99–149. Requires exactly one
`GATE-RECORD (S[0-9]{3,}) ` + `rest`, finds the FIRST ` quote=` (`rest.find ),
splits head on single space `" "`, rejects empty/duplicate/missing keys,
v != `""`, token without `=`, URL form key-set membership, `TS_RE`, ASCII
digits everywhere (post-repair `[0-9]` — verified: fullwidth `２０２６`,
superscript `²`, Arabic-Indic `٢/٣/٠/٤` all `PARSE`; `S19٩` → `PARSE ?`).
Consistent. Three micro-drifts are documented-but-not-enforced / enforced-
but-not-documented: see F-1 (empty quoted admit → `QUOTE_ABSENT,QUOTE_LEN`
instead of `PARSE`), F-2 (trailing space after a complete record → `OK`,
docstring says extra text → `PARSE`). Duplicate keys → `PARSE` (code
L114, counter M16 passes). Unknown key (`bogus=1`), missing key (drop
`line=`), case variants (`WORDS=`, `tier=a`, `Admit`, `quote=None`) → `PARSE`.
Key order **within head is free**: reordered head → `OK` (structural.log
`st-keyorder.md`). `quote=` **must be** the last key: `rest.startswith
("quote=")` → `PARSE`; ` ... extra=1` after `quote=none` → `PARSE`; junk
after admit's closing quote → `PARSE`; junk after unreach (`... extra`
without `=`) → `PARSE`. A second ` quote=` inside a rev quote body is
quote text, not a second key (already exercised by r83 M34 class; code
`find` picks the first) — a rev quote containing ` ... words=12 ...` does
NOT trigger duplicate-key `PARSE` (only `LINE,WORDS` if it breaks the line
content). This is correct under "quote= last" but easy to misread.

**REGISTRY.** `load_registry` L152–163: `ROW_RE = ^ {0,3}\|\s*(S[0-9]{3,})\s*\|`,
splits `strip().strip("|").split("|")`, keeps only 11-cell rows,
`setdefault(cells[0])`. Matches docstring L29 (0–3 spaces). Verified:
tier change A→B → `TIER`; 10-column row → `REGISTRY` (row skipped);
4-leading-space row → `REGISTRY` (drift.log r2/r3); unknown id S999 →
`REGISTRY` (counter M01).

**TIER (L30, url forms only).** Code L204–206: only when `regrow is not
None`; rev form never emits `TIER`. Matches docstring ("url forms").

**CAPTURE_PATH (L31).** Code L210–216: fullmatch `24hex.txt`; rejects symlink
(`os.path.islink`), non-file, and realpath-dir ≠ realpath captures dir.
`../` traversal → `CAPTURE_PATH` + cascades (edge.log `e9-dotdot-cap.md`).
Symlinked capture → `CAPTURE_PATH` (drift r8). Non-hex name → `CAPTURE_PATH`
(P28 probe → `CAPTURE_PATH,CAPTURE_SHA,QUOTE_ABSENT,REFETCH`). Note: the
tool joins `root/capture` lexically then realpaths the dir; `..` inside
`corpus/captures/../captures/x` resolves back and *is* rejected by CAP_RE
first (fail-closed, good).

**CAPTURE_KEY (L32).** L217–218: captured 24-hex ≠ `sha256(url)[:24]` →
`CAPTURE_KEY`. Note: when the path is traversal (`CAP_RE` no-match) key
is skipped (cm None) — `CAPTURE_KEY` not emitted; docstring doesn't
promise it in that case. Consistent.

**CAPTURE_SHA (L33).** L220–222: `SHA_RE = ([0-9a-f]{16,64})(?:…|\.\.\.)?`
fullmatch; must be prefix of `sha256(bytes)`. Verified:
16/64 hex genuine → `OK`; 17th-bit flip → `CAPTURE_SHA` (edge
`e3-capsha-17hex.md` uses +1 bit); full 64 genuine → `OK`; uppercase →
`CAPTURE_SHA`; `zzzz` → `CAPTURE_SHA`; `…` only → `CAPTURE_SHA`.
A genuine 16-hex followed by `...` (`ok-admit-dotdot-sha.md`) → `OK`.
Corner: code evaluates `capsha=None` on missing/bad path → also
`CAPTURE_SHA` (collateral; P28/P29-class probes show the 4-code cascade).
Cascading is allowed ("all reported").

**REFETCH (L34–36).** L223–224 (admit) requires same id/url/key/fetched,
`curl_rc=="0"`, `2[0-9][0-9]`, txt_sha256 == sha(capture). L236–237
(unreach) requires same id/url/fetched + equal curl_rc/http **and**
`not success` where success = `curl_rc=="0" and http.startswith("2")`.
Verified drift r4 (txt drift) → `REFETCH`; r5 (refetch curl 1) → `REFETCH`;
r6 (refetch http 503) → `REFETCH`; r83 P03/M03 drift → `REFETCH`; U01
success-claimed → `REFETCH` in counter. Semantically consistent with
docstring, incl. the r83 `P05/P06` downgrade and `P24` rejection.

**WORDS (L37).** L198–201: `kv["words"] != str(len(quote.split()))` →
`WORDS`, for admit and rev only. unreach `words=0` is a parse-time
literal (L131); `words=00`/`words=1` with `quote=none` → `PARSE`
(unreachable via WORDS). Verified `words=+12` → `PARSE` (INT_RE),
`words=999999999` → `PARSE` (>7 digits, INT_RE cap), `words=leading-zero`
→ `PARSE` (M31).

**QUOTE_LEN (L38).** L202–203: `not 1<=n<=25` → `QUOTE_LEN`. P27 (26 words)
→ `QUOTE_LEN`. Empty admit quote (`""`) → `QUOTE_ABSENT,QUOTE_LEN`
(correct words math; note docstring PARSE-line drift F-1 below).

**QUOTE_ABSENT (L39).** L227–233: normalized quote must be substring of
normalized capture; also fires when capture missing. Normalization L87–89
matches docstring L43–44 exactly (punctuation/case kept).

**REV (L40).** L242–246: `HEX40_RE` fullmatch else `git_blob` failure →
`REV` + `LINE` (LINE always co-fires — see doc drift D-3). Verified:
short rev (P11 `b780382`) → `REV,LINE`; 39-hex → `REV,LINE`; 42-hex →
`REV,LINE`; non-hex → `REV,LINE`; rev `^{commit}` suffix → `REV,LINE`
(parse value contains non-hex, fullmatch fails); tree path → `REV,LINE`.
Consistent.

**LINE (L41).** L250–253: 1-based, `i > len(lines)` or quote absent from
`norm(lines[i-1])` → `LINE`. Last newline popped (L249). `line=0` → `PARSE`
(L147). `line=0222` → `PARSE` (leading zero). Verified P32 past-EOF →
`LINE`, M27/R01/R06 counter legs.

**SETUP (L50–51, claims C1§4).** Docstring promises exit 2 + GATE_* errors
only for missing FILE / missing registry / missing refetch / usage. A
non-git `--repo` is **not** in that list, but claims.md §4 + K2 explicitly
require `GATE_RECORDS_ERROR` exit 2 there. Code never validates `--repo`;
`git_blob` swallows OSError/non-zero rc → `None` → `FAIL LINE,REV` exit 1.
**FIRES K2 (see finding F-0).**

## 2. Parsing matrix — record class, lead_strip, REC_RE (seat Q2)

Docstring record class (L13–16): first text after leading WS + Cf is
`GATE-RECORD` followed by whitespace or EOL; mentions elsewhere are prose.
Code: `REC_RE = ^GATE-RECORD(?:\s|$)` (L68) on `lead_strip(ln)` (L71–76,
`isspace() or unicodedata.category=="Cf"`). `parse()` is stricter (single
spaces).

Observed (structural.log / sys.log / cf.log):
- leading space/tab → record, `OK` (matches class).
- BOM / ZWSP `U+200B` / word-joiner `U+2060` / LRM `U+200E` / `U+180E` /
  soft hyphen `U+00AD` / `U+FEFF` → record, `OK` (Cf stripped; docstring
  promises exactly this). `U+2028/2029` (Zl/Zp, `isspace=True`) also stripped —
  beyond the doc's "whitespace" wording but harmless (still a record).
- `CRLF`/`CR`-only and trailing spaces/tabs after the record → `OK`
  (`rstrip("\r\n")`, `qraw.rstrip()`); **`st-final-sp.md` (one trailing
  space) → OK**: docstring PARSE "extra text" → should be arguably
  refused; the tool's `rstrip` accepts trailing whitespace on REV (raw
  `qraw.rstrip()` L120) and admit/unreach (L125/L131). Draft inconsistency
  D-2. Not a K2 class (frozen battery has no such forgery).
- `GATE-RECORD\tS199` → **record, FAIL PARSE** (tab between lead and id,
  `parse` requires single space). Record class honored, form refused.
  `GATE-RECORD  S199` (double space) → `PARSE` (empty token). `words`
  with double space `  words=12` → `PARSE` (empty token `""` no `=`).
  Tabs inside the head (`\twords=12\t`) → `PARSE` — head split is on
  `" "` only. This is stricter than the class ("whitespace") but
  consistent with `quote=`-anchored split and the frozen counter (which
  only emits single spaces). Not a K2 gap.
- key order: shuffled head → `OK` (st-keyorder). duplicate same-value
  (`words=12 words=12`) → `PARSE`. unknown/missing key → `PARSE`. `key=`
  (empty value) → `PARSE` via `not v` (L114). `key=a=b` → value `a=b`
  (split `,1`) → then set-membership fails → `PARSE` for unknown key.
- prose mentions: `The tool checks GATE-RECORD ...`, `- GATE-RECORD`,
  `> GATE-RECORD`, `<!-- GATE-RECORD -->`, `xxx GATE-RECORD`,
  `## GATE-RECORD`, `| GATE-RECORD |`, `xGATE-RECORD`, fenced
  ```` ```GATE-RECORD ```` → all `records=0` (true prose, never checked).
  `k12-blank-then-rec.md` (two blank lines then record) → `OK` at line 3.
  Inside a paragraph mid-line `...GATE-RECORD...` → `records=0`. One line
  with `0/1` and two records glued (`rev quote=... GATE-RECORD ...`) → one
  record FAIL `LINE,QUOTE_LEN,WORDS` (second GATE-RECORD is quote body).
  `GATE-RECORD` alone / `GATE-RECORD ` (EOL) → `FAIL PARSE ?` (REC_RE
  `$` fires, parse fails, SID absent → `?`). `GATE-RECORD S19` (2 digits)
  → `PARSE ?` (SID_RE `?` no match within `[0-9]{3,}`).

Inconsistencies in the record-class area:
- `lead_strip` strips Zl/Zp + all `isspace()` including `U+000B/C`,
  `U+0085` — wider than "whitespace + Cf" as written. Docstring L13 says
  "leading whitespace and invisible format characters (Unicode category
  Cf, e.g. ...)" — `isspace()` covers Zs + Cc + Zl/Zp; Cf and Zs agree on
  most glyphs. Edge not in frozen classes; not a kill.

## 3. Exit contract (K4 shape), error paths, mutation surface (seat Q3)

- Exit 0 iff records ≥1 and all OK; 1 if any FAIL or 0 records; 2 on
  usage/IO. Reproduced: ok files → 0; fail → 1; empty file → 1 with
  `GATE_RECORDS files=1 records=0 ok=0 fail=0`; no args → 2 (argparse);
  `verify` with no files → 2; unknown flag → 2 (argparse message on
  stderr, tool returns 2 via SystemExit catch L265–267); directory as
  FILE → 2 (`GATE_RECORDS_ERROR missing <dir>`, since `os.path.isfile`
  false); missing FILE → 2; missing root registry / missing refetch →
  2 with `GATE_RECORDS_ERROR missing ...` on stderr. Matches L50–51.
- **Unreadable FILE (chmod 000)** → uncaught PermissionError traceback,
  exit 1 (fixt.log `f2-unreadable.md`) — exit 1 coincides with the
  failure contract but emits a traceback, not a GATE error. The docstring
  reserves exit 2 for "usage or I/O error" — this is an I/O error
  misreported as exit 1. Not a frozen class; recommend mapping open()
  OSError → exit 2.
- Invalid UTF-8 input line (`\xff\xFE ...`) → `errors="replace"` → records
  0 exit 1 (f1 probe). Graceful; acceptable.
- NUL byte appended → `FAIL LINE,WORDS` (NUL preserved by normalization,
  quote mismatch). No crash.
- Missing refetch log / missing registry → 2 (verified both).
- **Non-git `--repo` → exit 1 `FAIL LINE,REV` (no stderr)** — claims.md
  class (F-0), the only in-class K2.
- Mutation/fetch surface: only `subprocess.run` = 3× `git -C repo
  cat-file -t {rev}^{commit}` + `-t rev:path` + `blob rev:path` (L179/183/
  186), read-only, no shell. No `open(...,"w"/"a")`, no `os.remove/
  rename/unlink/mkdir/makedirs`, no network imports (only argparse,
  hashlib, os, re, subprocess, sys, unicodedata). `os.path.realpath`
  doesn't create files. The tool does not write its own receipt or touch
  the repo. Docstring L11 promise ("never fetches, never writes, never
  mutating git") holds. Writes noticed are only via print to stdout/stderr.
- Note: `capture=...` path is lexical `os.path.join(root, capture)` —
  a symlinked *parent* (root/corpus/captures itself a symlink) resolves
  via realpath comparison, fail-closed. Good.

## 4. Findings

**F-0 — SEVERITY HIGH (K2 FIRES). Setup leg misreported.**
Command: `python3 -B "$T" verify --root "$S/root" --repo "$S/nogit"
"$S/probes/st-setup.md"` (st-setup.md = frozen S199 rev line; `nogit/` =
empty scratch dir, `git rev-parse` fails there).
stdout: `GATE_RECORD .../st-setup.md:1 S199 FAIL LINE,REV` + summary;
stderr: (empty); `exit:1`.
Receipt: `setup.out.txt`, `setup.err.txt`, `setup.rc.txt`,
`structural.log` tail (SETUP block), `exit.log`.
Expected by claims.md K2/setup leg: exit 2 + `GATE_RECORDS_ERROR` on
stderr. Docstring doesn't promise it, but claims.md explicitly binds it,
so it fires K2. Root cause: `git_blob()` maps any OSError/non-zero git
rc to `None` → `REV+LINE` fail rather than a repo error. A non-git dir
is indistinguishable from "rev not in repo" at that layer.

**F-1 — LOW. Empty quoted admit (`quote=""`) misclassified.**
`quote=""` with `words=13` → `QUOTE_ABSENT,QUOTE_LEN,WORDS` (structural.log
`st-quote-empty-admit.md`), empty-quote `words=0` → `QUOTE_ABSENT,QUOTE_LEN`
(`st-admit-emptyquote-words0.md`, `e1-ws-quote.md`); docstring PARSE L28
("the line fits none of the three forms") would put `quote=""` (0 words)
arguably in PARSE since the form requires `quote="<text>"`. It is in
fact refused with QUOTE_* codes (never OK), so no K2 — the counter's M12
expects QUOTE_LEN and gets it. Docstring/parser wording drift only;
counter cannot produce a forged `""` for an admit (M12 with words=0 gets
QUOTE_LEN). Record as doc drift, not a fire.

**F-2 — LOW. Trailing whitespace after a complete record → OK.**
`st-final-sp.md` (rev + space), `st-unreach-trailing.md`, admit + space
(`st-final-sp-admit.md`) → OK. `rstrip()` on quote raw (L120/L125/L131)
accepts trailing spaces. Docstring's "extra text → PARSE" reads as
refusing this; in practice trailing whitespace is not "extra text" in
most readers and the counter never emits it. Not a frozen class.

**F-3 — MEDIUM (robustness, control fragility). Whitelist stub is CWD-dependent.**
`stub-whitelist.py` opens relative `corpus/evidence/round84/
c2-positives.tsv` (copied receipt `stub-whitelist.py` line 4). Run from a
non-lane CWD it crashes (`FileNotFoundError` traceback, exit 1) and the
counter reports POSITIVE=0/15 instead of the intended whitelist FAIL —
my first byte-run (from scratch CWD) gave `POSITIVE=0/15`. The
committed receipt `c2-f4-stub-whitelist.txt` (`FRESH_POSITIVE=2/5 …
FAIL`) is reproducible only with CWD inside a lane tree
(`run-controls-r84.sh` ran it from the lane checkout at REV d047cd8d).
The counter (`run()` L158) passes no `cwd`, so the control is valid only
under the harness's CWD assumption. The control is still a *valid* FAIL
in the as-provisioned environment, so K4 holds there; but the same
counter invoked with e.g. CWD=`/tmp` would make the whitelist fail for
the wrong reason. Freezing note: `POSITIVE=0/15` (crash) is clearly
distinguishable from whitelist intent (15/15) in the committed receipts,
so a checker could catch it. Recommend the stub harden or the counter
pass `cwd=root`.

**F-4 — MEDIUM (robustness). Unreadable input file traceback.**
chmod-000 FILE → Python traceback + exit 1 (fixt.log). Docstring L50–51
reserves exit 2 for I/O errors; this is one. Not a frozen class.

**F-5 — K4 controls verified, not assumed.** K0 re-run reproduces
`262/288` exactly (`k0-recompute.txt`). Stub-accept/refuse/quote-only
reruns reproduce committed tallies exactly. Whitelist reproduces
`FRESH_POSITIVE=2/5` only from a lane CWD (see F-3) — under that
condition K4 does hold: it fails the counter, as claims require.

**F-6 — r83 survivor probes: 14/16 refuse as expected; 2 OK-on-purposelines.**
All 16 P-probes run (`mut.log`):
- P03→REFETCH, P11→`REV,LINE` (expected REV — code always co-fires LINE;
  counter's expected-code check is *contains*, so fine), P24→REFETCH,
  P27→QUOTE_LEN, P30→PARSE, P31→PARSE, P34→PARSE, P35→PARSE, P36→PARSE,
  P05→REFETCH, P06→REFETCH, P28→`CAPTURE_PATH…`, P32→LINE.
- **P24b (`curl_rc=28 http=200`, refetch row attempt-1 RC 28 H 200 exists
  verbatim) → OK.** Docstring REFETCH-unreach clause says "or the record's
  curl_rc/http denote a success" is refused. `curl_rc=28` + `http=200`
  is *not* a success (timeout), and the refetch row literally records
  exactly those values. So OK is correct under the doc; the "P24b OK" is
  a genuine record, not a forgery. R83 filed it as a probe of the
  *admit* direction (P05 admit with 28/2xx). Not a finding.
- **P29 (labeled symlink probe) → OK** because at landing the capture
  path is a regular file (mode 100644, hash matches the record's
  capture_sha). The swap did not survive at this rev (`git ls-files`
  mode 100644; sha `6e2577…` matches both machine copy and record). The
  probe was built in a different tree (r83) where the symlink existed;
  re-running it at r84 fires nothing. The tool's symlink defense is
  verified separately by drift r8 (real symlink → `CAPTURE_PATH`).

**F-7 — Duplicate registry row: first wins silently.**
Two S203 rows (tier A, then inserted tier C) → record tier A prints OK
(drift r7b). Docstring claims "S<id> has no 11-column Registry row" —
with two rows the id *has* rows; neither doc nor census contract
addresses ambiguity. r83+ wrote census logic the same way (`setdefault`),
so the behavior mirrors the census consumer. A Tier forgery smuggled
inside a *second* row is undetectable if the first row is genuine. Not a
frozen class (counter only ever has one row per S-id; the archive never
ships duplicates – verified `uniq -d` empty on landing tree). Worth a
dedicated REGISTRY on `len(rows)>1` if the registry ever gains rows in CI.

**F-8 — `st-rev-dotpath.md` OK.** `path=./corpus/lessons/...` + genuine
rev → OK. `git cat-file` resolves `./` lexically; the docstring says
"repo-relative path". `./`-prefixed is arguably repo-relative, so OK is
defensible. A strict reading would refuse it. Not in frozen classes.

## 5. Docstring / claims.md inconsistencies (for the record)

- **D-1 (claims.md vs docstring, setup): claims.md binds exit-2 on the
  setup leg; the docstring omits it.** Claims win for scoring → F-0 fires.
- **D-2 (trailing whitespace):** docstring L28 "extra text" implies
  `PARSE`, code `rstrip()`s (L120/L125/L131) → OK. Same for admit
  trailing space. Not frozen.
- **D-3 (REV→LINE cascade):** docstring L40–41 lists REV and LINE as
  separate codes; when REV fails the tool always adds LINE (L245–246).
  A `REV`-only expected class gets `REV,LINE` — still contains REV, so
  the counter's expected-code check passes. Not a miss.
- **D-4 (empty quote):** docstring's "fits none of the three forms"
  doesn't cleanly cover `quote=""` (F-1). Counter expects QUOTE_LEN;
  docstring doesn't say which code. Suggest either PARSE or leave as is.
- **D-5 (claims.md "288" count):** claims.md says "9 r83 survivors",
  "288 forgeries across all mutation classes". The counter computes 288
  on this run (`FORGED_REFUSED=288/288`), but claims.md §1 lists 8 labels
  (M03/M11/M24/M27/M30/M31/M34/M35/M36 = actually 9 counting M36) — fine.
  The counter's M17/P24b absorptions make per-class expectations differ
  slightly from shorthand, but the expected-code direction is preserved
  (P24b OK is *not* enrolled in C2 battery per claims §1's enumerated
  mutations; the counter's U01 is the live one and fires correctly).
- **D-6 (counter docstring vs claims.md):** counter's "F  fresh positives"
  is built from committed captures but `build_fresh_positives` for rev
  reuses *existing* lesson lines (`git grep rev=` in corpus/lessons, not
  fresh text search over blobs) — fresh positives are fresh *combinations*
  (new lines not previously listed), not fresh quotes. This still defeats
  the whitelist (2/5 under harness CWD) and matches claims' "built
  in-counter". Note only.
- **D-7 (whitelist stub claims vs behavior):** claims K4 asserts
  "a tool that accepts the 15 frozen lines and refuses everything else
  FAILS the counter on at least one leg". True from harness CWD. But the
  stub refuses-by-PARSE and fails by EXPECTED_CODE/RC — the receipt shows
  `FORGED_REFUSED=288/288` (it refuses everything right) and fails via
  FRESH_POSITIVE + EXPECTED_CODE + RC=3. K4's essence is satisfied.

## 6. What was run, commands and receipts

Every probe was run as
`python3 -B <archive>/tools/gate-records.py verify --root <archive> --repo /home/vgpnk/Projects/shokunin/chousa-shokunin <probe>`
scratch archive at `03bbb4580b39b442be69f998fae2db48d64b8c93`, with
repo set to the live lane checkout (read-only cat-file only). Exit codes
recorded verbatim.

- Counter at landing: `counter-landing.txt` (PASS, rc 0).
- Pre-repair (K0) + stubs: `k0-recompute.txt`, tool copies
  `tool-pre-repair-81b81173.py`, `tool-at-landing.py`, `stub-whitelist.py`.
- Structural (key order, duplicate, unknown, missing, case, tab/split,
  dotpath, uppercase-rev, etc.): `structural.log`, `par.log`,
  `rev2.log`, `quote.log`, `spec.log`, `uni.log`, `cf.log`, `sys.log`
  (record-class vs prose), tiny input copies in `inputs/`.
- CAPTURE_SHA / path / hash edges: `edge.log`; drifted roots r1–r8:
  `drift.log` (tier, 10-col, 4-space, txt-drift, refetch-curl, refetch-503,
  duplicate row, symlinked capture).
- Exit / IO: `exit.log` (incl. setup leg) + `setup.out.txt` /
  `setup.err.txt` / `setup.rc.txt`; unreadable/invalid-UTF8/NUL:
  `fixt.log`.
- r83 survivors: `mut.log` (all 16 P0X probes against landing root).

Findings summary vs seat questions:
1. Docstring-vs-code per check: §1. Sole in-class OK-while-forbidden is F-0.
2. Parsing: §2.
3. Exit/errors/mutation: §3 + F-0/F-4.
4. Inconsistencies: §5.

## 7. Hygiene + tools

- Scratch: `/fast/scratch/hyaku/chousa-r84/R84ReviewerTool/` — **deleted**
  before yield.
- Receipts live under `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/
  waves/round-84/w1/R84ReviewerTool/` (this report + *.log + inputs/).
- Toolchain: Python 3.14.8 used; no installs. RULES.md read; no pacman
  used (operator pause respected).

VERDICT: R84ReviewerTool C1 fired — non-git --repo reports FAIL LINE,REV exit 1 instead of exit 2 GATE_RECORDS_ERROR per claims K2/setup leg.
