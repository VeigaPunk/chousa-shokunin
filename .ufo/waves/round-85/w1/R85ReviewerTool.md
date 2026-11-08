# R85ReviewerTool — code review of `tools/gate-records.py` @ 64803d33362f50cf9094e91fc3a4a07216c563ca

## Axes
1. **Spec fidelity** — does each docstring check (PARSE, REGISTRY, TIER, CAPTURE_PATH, CAPTURE_KEY, CAPTURE_SHA, REFETCH, WORDS, QUOTE_LEN, QUOTE_ABSENT, REV, LINE, setup error) match the code at its sentence?
2. **Attack surface** — inputs that print OK while the docstring check is violated (K2), and genuine inputs refused (K3).
3. **Parsing robustness** — key order, duplicate keys, empty values, `quote=` placement, whitespace, CRLF, unicode, record-line detection, word-bound sentence.
4. **Exit/error contract** — exiting, I/O failure behaviour, and any writing/fetching/mutating path.
5. **Documentation consistency** — docstring vs claims.md, incl. the `capture-fetch.py` store rule.

## Method (one line each)
- Read `corpus/evidence/round85/claims.md` (C1 K1–K4) and `plans/round-85.md` (amendments) first, then the tool docstring/code and the counter `corpus/evidence/round85/gate-records-r85.py` in full.
- Extracted `git archive 64803d33…` into `/fast/scratch/hyaku/chousa-r85/R85ReviewerTool` and ran the tool on real frozen positives (`c2-positives.tsv`) plus hand-built mutations, always with `--repo /home/vgpnk/Projects/shokunin/chousa-shokunin` (read-only `git cat-file`).
- Ran the frozen counter at the landing bytes — see receipts.

## Counter (K1, grounding)
```
$ python3 -B corpus/evidence/round85/gate-records-r85.py --root /fast/scratch/hyaku/chousa-r85/R85ReviewerTool --repo /home/vgpnk/Projects/shokunin/chousa-shokunin
TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=354/354 EXPECTED_CODE=354/354 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1
GATE_RECORDS_R85=PASS
rc 0
```
Receipt: `.ufo/waves/round-85/w1/R85ReviewerTool/counter-landing.txt`.

## (1) Check-by-check vs docstring

| Check | Docstring | Code | Verdict |
|---|---|---|---|
| PARSE | "the line fits none of the three forms (unknown/missing/duplicate key, bad value, extra text)" | `parse()` returns `None` → `FAIL PARSE`; rejects unknown/missing/dup keys, non-ASCII digits (`INT_RE`/`[0-9]` only), leading zeros (`INT_RE`), non-http URL, bad `fetched`, empty/bad-typed values, extra text after `quote=` for all forms | **Enforces.** Verified: tab separators, double-space head, tab-before-`quote=`, fron `tier=` (empty), `quote=` not last, tab lead → `FAIL PARSE`; dup `tier=` key → PARSE; Arabic-Indic digits → PARSE. No bypass found. |
| REGISTRY | "S<id> has no 11-column Registry row (0–3 leading spaces)" | `load_registry` requires exactly 11 cells after `\|`-split (any leading-space count ≤3 via `ROW_RE`); `check()` adds `REGISTRY` when `sid` absent | **Enforces.** Verified S999 → `FAIL REFETCH,REGISTRY`; S1234 (4-digit, valid regex, unregistered) → `REFETCH,REGISTRY`. |
| TIER | "url forms: tier differs from the registry row's tier cell" | `if form in ("admit","unreach"): if regrow and regrow[3] != kv["tier"]: TIER` | **Enforces.** Verified tier A→B on admit → `FAIL TIER`. |
| CAPTURE_PATH | "not `corpus/captures/<24 hex>.txt`, or is not a regular (non-symlink) file inside LANE" | `CAP_RE.fullmatch` + `os.path.islink(cap)` reject + `os.path.isfile` + `realpath` dirname == `realpath(root/corpus/captures)` | **Enforces.** Verified bad-key-short and `../` → `CAPTURE_PATH` (among others). Symlink branch present by inspection (no symlink fixture built; code path is a direct `islink` check — I trust the code, not a run, for this one branch). |
| CAPTURE_KEY | "key is not `sha256(url)[:24]`" | `key = sha256(url.encode())[:24]; if cm and cm.group(1) != key: CAPTURE_KEY` | **Enforces.** Verified URL+`?x=1` / swapped capture → `CAPTURE_KEY` (counter M13/M03 also cover). |
| CAPTURE_SHA | "capture_sha256 shorter than 16 hex digits or not a prefix of sha256(capture bytes)" | `SHA_RE.fullmatch` allows 16–64 hex + optional `…`/`...`; if no match → `CAPTURE_SHA`; else `not capsha.startswith(group(1))` → `CAPTURE_SHA` | **Enforces** (65-hex both non-match and non-prefix correctly yield CAPTURE_SHA; 16-hex and 64-hex prefixes pass). Ellipsis `...` (ASCII) is accepted as well as `…` — docstring writes `[…]`, SHA_RE accepts both; benign superset, see §5. |
| REFETCH (admit) | "no refetch.tsv row with this id, url, key, fetched, curl_rc 0, **http exactly 200**, txt_sha256 = sha256(capture)" | `r[5]=="0" and r[6]=="200"` exact string match | **Enforces exactly-200.** The narrowing from 2xx is real: `r[6] == "200"` rejects 203 (verified 3 rows with `curl_rc=0 http=203` exist and would not satisfy the check). |
| REFETCH (unreach) | "no row with id, url, fetched whose curl_rc/http equal the record's, **or the record's curl_rc/http denote a success**" | `success = curl_rc=="0" and http=="200"`; `ok = (not success) and any(row matches)` | **Enforces.** Verified unreach recast as `curl_rc=0 http=200` → `FAIL REFETCH`. |
| WORDS | "words differs from the number of whitespace-separated tokens of the quote" | `if kv["words"] != str(n): WORDS` with `n = len(quote.split())` (Python whitespace, Unicode-aware) | **Enforces.** Verified words+1 → `FAIL WORDS`; em-space in quote → PARSE (because the token stream then differs from the record's `words` token count in a way the parser's exact `== str(n)` catches? — observed `FAIL PARSE` is via `quote=` placement interacting with non-ASCII whitespace; the WORDS-vs-split semantics themselves are exact). |
| QUOTE_LEN | "a quoted record has fewer than 1 or more than 25 words" | `if not 1 <= n <= 25: QUOTE_LEN` | **Enforces** (the same sentence as the docstring; boundaries verified: 1-word → QUOTE_ABSENT only, 26-word → QUOTE_ABSENT,QUOTE_LEN, empty → QUOTE_ABSENT,QUOTE_LEN). |
| QUOTE_ABSENT | "quote, normalized, does not occur in the normalized capture text" | `if norm(quote) not in text: QUOTE_ABSENT`, with the docstring's normalization (U+2018/19/201C/201D → ASCII, whitespace collapse) | **Enforces.** Verified case-mismatch and synthetic quote → `FAIL QUOTE_ABSENT`. |
| REV | "rev is not a commit in GITDIR or path is not a blob at rev" | `HEX40_RE.fullmatch` then `git cat-file -t rev^{commit}` must be `commit` and `rev:path` must be `blob` | **Enforces.** Short rev (39) → `REV`; uppercase hex → `REV` (case-sensitive); dir-as-path → `REV`; `../../etc/passwd` → `REV`. |
| LINE | "line is outside the blob, or the normalized quote does not occur in that one line" | `i > len(lines) or norm(quote) not in norm(lines[i-1])` → `LINE`, and `REV`&`LINE` both emitted when blob absent | **Enforces** (off-by-one and one-line tests verified; line==0 → PARSE). |
| Setup error | "exit 2 on usage or I/O error (missing FILE, missing registry/refetch log, or `--repo` naming a directory that is not a git repository)" + "GATE_RECORDS_ERROR" on stderr | `if a.repo: subprocess.run(["git","-C",a.repo,"rev-parse","--git-dir"])`; non-zero → print `GATE_RECORDS_ERROR …` to stderr, return 2 | **Mostly enforces; one hole: `--repo ''`.** Bare dir, file, nonexistent dir → `GATE_RECORDS_ERROR`, exit 2 (verified). Subdirectory of a repo and worktree root → `rev-parse --git-dir` succeeds and the tool proceeds (semantically "inside a git repository", not strictly "naming" one — benign, git's own definition). **`--repo ''` → the `if a.repo:` guard skips the probe entirely; the tool then runs and emits `FAIL LINE,REV`, exit 1 — not the documented exit-2 setup error.** Verified: `python3 -B tool verify --root . --repo '' revtest.md` → `GATE_RECORD revtest.md:1 S199 FAIL LINE,REV` rc 1, stderr empty. See receipts `empty-repo.txt`, `probe-bundle.txt`. |
| Calendar `fetched` | "must also be a real calendar instant (`TS_RE` alone accepted 2026-13-40…)" | `_valid_ts` via `datetime.strptime("%Y-%m-%dT%H:%M:%SZ")` | **Enforces.** Verified `2026-02-29T00:00:00Z` (non-leap year) → `FAIL PARSE`; `2024-02-29` (leap) → `REFETCH` (calendar valid, refetch-mismatch — correct split); hour 24 → `PARSE`. |

## (2) OK-while-violated (K2) and refused-while-genuine (K3)

**K2 — nothing that prints OK while the docstring check is violated was found.** The counter passes all 354 forgeries with the right codes at round 85. The one exception below is a setup-path deviation, not a record-acceptance.

**FINDING (setup/probe hole, minor, does not fire any kill rule as written): `--repo ''` bypasses the non-git setup probe.** `main()` line 284 is `if a.repo:`, so the empty string never reaches the probe; the run degrades to per-record `FAIL LINE,REV` exit 1 instead of the documented `GATE_RECORDS_ERROR` exit 2. This is the correct *fail-closed* direction (it never accepts a bad check), and none of K1–K4 fire on it: K2 requires `OK`/wrong-code for a *frozen-class forgery* (none achieves it), K1 requires the setup leg to fail — with the counter's actual setup leg (a fresh empty directory, not `''`) it passes; K4 is about whitelisting. It is a deviation from the docstring's own sentence ("`--repo` naming a directory that is not a git repository" — `''` names no directory), and I flag it because the repair's whole point is exit-2 fidelity. Receipts: `empty-repo.txt`, `probe-bundle.txt`.

Also observed: **`admit` with `decision=reject` prints OK.** The docstring's form is `decision=<admit|reject>`, and the code validates only membership in that set, never consistency with the form. A record claiming `decision=reject` but passing every other admit check is treated as admit — docstring-level ambiguity (the form lists `decision=<admit|reject>` without saying which belongs to which form), not a demonstrable spec violation. I flag it as an inconsistency in the spec, not a K2 fire (no frozen class covers it, and the counter's U04 "admit-without-capture" tests the reverse direction).

**K3 — nothing genuine was refused.** All 15 frozen + 5 fresh positives print OK at the landing revision (POSITIVE=15/15, FRESH_POSITIVE=5/5).

## (3) Parsing

- **Record detection** (`lead_strip` + `REC_RE`): strips leading whitespace *and* Cf characters (BOM, ZWSP, etc.), then requires `^GATE-RECORD(\s|$)`. Verified: leading tab/BOM/ZWSP → detected and accepted; blockquote `>`, list item `-`, inline code `` ` `` → **not** treated as records (records=0 → exit 1) — exactly as the docstring says ("A mention elsewhere in a line … is prose, not a record").
- **Key order**: keys appear once each, "in any order, before `quote=`". Verified: rev keys reordered → OK. `quote=` must be last; a duplicated `quote=` inside an admit quote breaks at the first ` quote=` and the tail mislexes (top-token parse failure → `FAIL QUOTE_ABSENT,WORDS` for `admit-dup-quote-eq`) — refused, not accepted, so correct direction; the docstring's "quote= is last" is a real constraint of the implementation.
- **Duplicate keys**: `if not k or k in kv or not v: return None` → PARSE. Verified.
- **Empty values**: `tier=` (empty) → PARSE. Verified.
- **CRLF / trailing whitespace**: `parse()` does `lead_strip(line).rstrip("\r\n")` and `qraw.rstrip()`; verified trailing-space and CR both → OK (docstring is silent on CRLF; acceptance is consistent, never harmful).
- **Unicode**: digits are `[0-9]` only (no Unicode digit class), matching the docstring's "Every digit … is ASCII 0-9, no leading zero". Unicode whitespace inside a quote changes `quote.split()` tokenization and is caught by WORDS/PARSE — refused, consistent with "whitespace runs (Python str.split) collapse".
- **Word bound**: docstring "`1–25 word`" and code "`1 <= n <= 25`" are the same sentence; boundaries 1/25/26 verified against `QUOTE_LEN` emission above.

## (4) Exit contract, error handling, writes

- Exit 0 iff records ≥ 1 and all OK; exit 1 on any failure or zero records; exit 2 on usage/I/O error with `GATE_RECORDS_ERROR` to stderr. Verified all three; missing registry, missing refetch, missing input, directory-as-input each → exit 2 with `GATE_RECORDS_ERROR`; empty/missing subcommand → exit 2.
- **Unreadable capture is NOT a clean exit 2.** A chmod-0 capture raises an uncaught `PermissionError` (traceback on stderr, rc 1). The docstring's exit-2 list does not include unreadable captures, but K4-adjacent robustness: this is the one code path that exits 1 by exception rather than by return, with the full traceback printed. Receipt: `unreadable-capture.txt`.
- **Invalid UTF-8 in the record file** (`errors="replace"`) → `FAIL PARSE`, rc 1 — handled, no crash.
- **Capture is a directory** → `CAPTURE_PATH` family, rc 1 — refreshed as `FAIL CAPTURE_PATH,CAPTURE_SHA,…` (no crash).
- **Writes/fetches/git mutation**: none. Static audit: no `open(…, "w"/"a"/"x")`, no `curl`, no network; subprocess calls are exactly `git cat-file -t`/`git cat-file blob` (read-only) and `git rev-parse --git-dir`. Consistent with the docstring's "never fetches, never writes a file and never runs a mutating git command."

## (5) Docstring / claims.md inconsistencies

1. **`capture-fetch.py`'s store rule (docstring §REFETCH parenthetical).** Docstring: "`2xx would have passed; … matching capture-fetch.py's own 200..299 store rule narrowed to 200`". Actual: `capture-fetch.py` line 10 `On a successful attempt (curl_rc == 0, http_code 200-299, non-empty body)` and line 152 `if 200 <= code <= 299:` — so the `200..299` characterization is accurate, and the tool's narrowing to exactly `200` is a deliberate tightening on top of it. The claims.md differentiator calls it "REFETCH success narrowed from 2xx to exactly 200" — consistent across docstring, claims, and code.
2. **`admit`/`decision=reject` ambiguity** (see §2): the form spec `decision=<admit|reject>` reads as if both are valid on both url forms; the code treats `reject` on an admit form as OK. Spec and code agree textually and diverge only in intent. Minor.
3. **`SHA_RE` ellipsis superset**: docstring writes `capture_sha256=<>=16 hex>[…]` (the Unicode ellipsis). Code also accepts ASCII `...`. Superset, benign, undocumented.
4. **`--repo ''` vs "naming a directory"**: the repair sentence in the docstring and claims.md assumes `--repo` always names a directory. The empty string does not reach the probe (see §1 setup row). Documentation and code agree for all real paths; the empty string is an undocumented gap.
5. **Claims.md "each forged line in its own file, all given to one tool run"** matches the counter (one `g%04d.md` per forgery, single `run()` call). Claims.md "timeouts/timeouts-free" — the counter imposes no timeout on the setup leg; the tool itself spawns non-timed subprocesses. No material divergence.
6. **Claims.md whitelist/TIER nuance**: nothing found; TIER requires the registry tier cell, not just membership — confirmed by code.

## Tooling recorded (per operator directive)
- No tools installed. Python 3.14.8 (stdlib), git and existing suite only.

## Residual risk / verification gaps
- Symlink inside the capture store: the `islink` reject branch was inspected but not exercised with a live symlink fixture (deliberately avoided mutating the lane tree). Low risk — direct `os.path.islink` call.
- Replica of the D1 stale-refetch forgery could not be built for S203 specifically (its only refetch row is a 200 row); D1 is covered by the counter on admits where a failed attempt exists — receipted by `FORGED_REFUSED=354/354 EXPECTED_CODE=354/354`.
- Worktree root as `--repo` not built live; `rev-parse --git-dir` semantics make this trusted.

VERDICT: R85ReviewerTool C1 held — counter 354/354 with expected codes, no K2/K3/K4 fire; only two minor doc deviations flagged (--repo '' exits 1 instead of 2; admit+decision=reject accepted).
