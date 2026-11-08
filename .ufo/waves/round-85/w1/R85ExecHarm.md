# R85ExecHarm — C1 K3 (harm) / K4 on real lane history + side-effect audit (round 85)

Seat: R85ExecHarm. Landing attacked: `64803d33362f50cf9094e91fc3a4a07216c563ca` (== current tip), base `43c3f7284eee4889cdcc6ac1626573f6579cd533`.
Method: `git archive 64803d3… | tar -x -C tree/` (landing), `git archive 43c3f72… | tar -x -C tree-base/` (base). Tool under test: `tools/gate-records.py verify --root tree --repo /home/vgpnk/Projects/shokunin/chousa-shokunin FILE...` (landing bytes). Tool diff (base→landing) is exactly the three round-85 repairs: (a) `_valid_ts` calendar check in `parse`, (b) REFETCH `2[0-9][0-9]` → `== "200"` (admit) and unreach `startswith("2")` → `== "200"`, (c) non-git `--repo` → `GATE_RECORDS_ERROR` exit 2 via `git rev-parse --git-dir`. No other behavioral change in the diff (receipt `tool-diff.txt`).
Counter pins verified: `sha256(tree/corpus/evidence/round85/gate-records-r85.py)=62496d36…1d22`, `sha256(tree/tools/gate-records.py)=2de79722…beb` — both match `corpus/evidence/round85/instrument-pins.txt`. Advisory counter run at landing: `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=354/354 EXPECTED_CODE=354/354 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1`, `GATE_RECORDS_R85=PASS`, rc 0 (run output pasted in §0 receipt `runs/r85-lessons.out` companion — see §0).

## (1) Full-lane tabulation at landing

- **Every file under `corpus/lessons/` (135 files)**: single tool run over all 135, rc **0**. Summary line (receipt `r85-lessons.out`): `GATE_RECORDS files=135 records=24 ok=24 fail=0`. Per-file tabulation (receipt `r85-lessons-tabulate.tsv`): only 6 lesson files carry any GATE-RECORD line; all 24 records are `OK`:
  - `corpus/lessons/round-80.md` records=4 ok=4 (`GATE_RECORD …:19 S199 OK`, `:20 S200 OK`, `:21 S201 OK`, `:22 S202 OK`)
  - `round-81.md` records=6 ok=6 (S203–S208, `:23–:28` all OK)
  - `round-82.md` records=5 ok=5 (S008,S209,S210,S211,S028, `:57–:61` all OK)
  - `round-83.md` records=3 ok=3 (S009,S212,S213, `:19–:21` all OK)
  - `round-84.md` records=3 ok=3 (S214,S018,S023, `:18–:20` all OK)
  - `round-85.md` records=3 ok=3 (S215,S026,S024, `:14–:16` all OK)
  - remaining 129 lesson files: `records=0` (no GATE-RECORD line; tool exit 0 on the aggregate because records≥1 and all OK per FILE-batch semantics — per-file they print `records=0 ok=0 fail=0`).
  - **Lesson FAILs: none.**
- **Every other committed file containing a `GATE-RECORD` line** (`git grep -n -E '^[[:space:]]*GATE-RECORD' 64803d3…`, 355 lines in 274 distinct files, receipt `grep.txt`): run per-file (receipt `r85-grep-tabulate.tsv`, 274 rows) and per-record base-vs-landing comparison (receipt `compare-base-vs-landing.txt`). At landing: **354 records total, 141 OK, 213 FAIL** (0 records change verdict base→landing — see below). FAIL-by-class:
  - `forge/probe/input` (14?): 191 FAIL — `PARSE` 67, `LINE,REV` 18, `REFETCH` 16, `QUOTE_ABSENT` 12, `LINE` 8, `CAPTURE_SHA` 8, `CAPTURE_PATH,…` 8, `CAPTURE_KEY,REFETCH` 9, `WORDS` 3, `TIER` 2, etc.
  - `fixture` 7 FAIL (`LINE` 3, `LINE,REV` 2, `QUOTE_LEN` 1, `WORDS` 1) — the round-80 real-corrupt fixtures (absent-quote, bound-27, off-by-one, prefix-rev, tip-defect, tree-rev, wordcount), each a deliberate single-defect fixture; `real-clean`/`real-records`/`after-clean` are OK.
  - `log/receipt` 19 FAIL (`PARSE` 10 incl. probe `.out` files, `REFETCH` 4, etc.).
  - `template/mutant` 10 FAIL (`PARSE` — the docstring template line `GATE-RECORD <id> rev=<40-hex> …` in `corpus/evidence/round80/gate-grounding-check.py:13` and 8 mutant copies).
  - `report-md` 7 FAIL (`PARSE` 6 incl. prose-template lines, `LINE,REV` 1 — `R80CriticA.md:336 S195 rev=b7803829…` bogus record), `other` (R83ExecHarm `04-fail-bytes-by-hand.txt` reprint) 8 FAIL.
  - OK by class: fixture 36, report-md 26, forge/probe/input 46, log/receipt 8, other 1, lesson 24 = 141.

## (2) Hand verdict on every FAIL + the two mandated regressions

**Every developed, corpus-located object named below. Exit codes observed.**

### Base-vs-landing verdict-change table (decisive)
Per-record alignment of base tool (`tree-base/tools/gate-records.py`) vs landing tool (`tree/tools/gate-records.py`) over all 274 files / 354 records: **base-OK→landing-FAIL = 0; base-FAIL→landing-OK = 0** (receipt `regressions-baseOK-landingFAIL.txt` is empty, 0 bytes; full matrix receipt `compare-base-vs-landing.txt`, 1532 lines). So across *committed lane bytes as they stand*, the narrowing + calendar repairs change **no** record verdict. The two retuned classes therefore have exactly zero intersection with any committed genuine record — see (a),(b) for the direct probes.

### (a) Historical records with refetch http 203/204/206 (2xx ≠ 200)
`refetch.tsv` rows with `http` matching `2[0-9][0-9]` but ≠ 200 (from `corpus/evidence/round57/refetch.tsv` at landing): **exactly 3 rows, all http=203** —
- `S021 https://pubmed.ncbi.nlm.nih.gov/17638714/ 58725f5e0ac436166546a5ec 2026-11-08T02:15:39Z curl_rc 0 http 203 txt_sha256 7070b59c3434b677…` (columns: id,url,key,n,fetched,curl_rc,http,orig_sha,txt_sha; field 9 `7070b59c…`)
- `S032` same url/key, `2026-11-08T02:15:50Z`, `0 203`, same txt_sha `7070b59c…`
- `S022 https://pubmed.ncbi.nlm.nih.gov/28912002/ ff9013bd7d9387e45cd6e000 2026-11-08T02:16:21Z 0 203 7070b59c…`
No 204/206 rows at all. All three rows' `txt_sha256` = `7070b59c3434b677…` = sha256 of the PubMed "Cookies must be enabled" interstitial capture bytes, and their `capture` bodies read (e.g. `corpus/captures/ff9013bd7d9387e45cd6e000.txt` head): `pubmed.ncbi.nlm.nih.gov … Cookies must be enabled … Enable cookies … reload this page to continue.` — a cookie-challenge page, not a quotable source body. Committed probe `R84SentinelScope/receipts/e7-203-admit-ok.txt:8` shows the r84 acceptance: `GATE_RECORD … S022 OK … exit=0 <-- the tool prints OK: a cookie wall is certified as a quotable admitted source` (that receipt file's own pasted line is truncated `…w`, so it FAILs `PARSE` under both tools as committed — a receipt truncation, not a genuine record).
- **Record-change answer: zero committed records change verdict** (proven by the 0/0 alignment above). The only records that *would* change are *uncommitted hypothetical admits* built on these 203 rows, which is exactly the intended narrowing and is a genuine in-class forgery form (docstring REFETCH: "a 203 cookie-challenge page carries no quotable body"). Direct probe with the complete forged line `GATE-RECORD S022 url=https://pubmed.ncbi.nlm.nih.gov/28912002/ fetched=2026-11-08T02:16:21Z tier=A decision=admit capture=corpus/captures/ff9013bd7d9387e45cd6e000.txt capture_sha256=7070b59c3434b677 words=4 quote="Cookies must be enabled"` (registry row `corpus/SOURCES.md:32 | S022 | … | A |`, capture sha verified `7070b59c3434b67711f6a6ad723834ee1fce7a82230ac6970c1b12844c042a00` = `sha256sum` of that capture): base → `GATE_RECORD forged/e7-203-admit.txt:1 S022 OK`, rc 0; landing → `FAIL REFETCH`, rc 1. Same for S021 (`fetched=2026-11-08T02:15:39Z`): base `OK` rc 0 → landing `FAIL REFETCH` rc 1. **Not harm; K2-closure by design.**
- Consequence for capture-fetch: `tools/capture-fetch.py:10` documents store rule `200-299` and `:152 if 200 <= code <= 299:` — a 203 body *can* be stored on disk (and was). The tool's `REFETCH` code now refuses to credit such a stored cookie-wall body as an admitted source. No committed lesson admits on a 203 row (all 24 lesson admits, incl. S215/S026/S024 round-85, are http exactly 200 per their refetch rows — otherwise they'd have failed `REFETCH` at landing; they print OK).

### (b) Historical records with calendar-invalid `fetched`
`refetch.tsv` scan (all 9-field rows): **0 calendar-invalid `fetched`** (only header `fetched_utc` is shape-bad). Workspace-wide `fetched=` token scan (all committed GATE-RECORD + forge files): exactly 2 shape-valid/calendar-invalid tokens, both planted forgeries in `R84ExecForge/forge/`:
- `x-fetched-bad.md:2 fetched=2026-13-01T18:44:29Z` (month 13): base → `S203 FAIL REFETCH` rc 1; landing → `S203 FAIL PARSE` rc 1. Same rc, different code. The record never passed under base (no refetch row with that fetched time), so not harm.
- `x-fetched-9999.md:2 fetched=9999-99-99T99:99:99Z`: base → `FAIL REFETCH` rc 1; landing → `FAIL PARSE` rc 1.
All other genuine `fetched` tokens validate (`shape=True calendar=True`, incl. every lesson token 2026-11-06/08 and all counter tokens). Full scan output retained in scratch logs (all rows in §2); the two invalid tokens are the only ones in the repo.

### Hand verdict table — sample of representative FAILs (full per-record lines in receipts)
| file:line S-id code (landing) | deciding bytes (hand) | verdict |
|---|---|---|
| `fixture/round-80.real-absent-quote.md:21 S201 FAIL LINE` | quote says "bytez", blob `b7803829:corpus/QUALITY.md:1054` says "bytes" | genuine defect — tool correct |
| `fixture/round-80.real-bound-27.md:21 S201 FAIL QUOTE_LEN` | 27 tokens > 25 bound | genuine defect — tool correct |
| `fixture/round-80.real-off-by-one.md:21 LINE`, `…prefix-rev… LINE,REV` (rev not an object), `…tree-rev… LINE,REV` (rev is a tree), `…wordcount… WORDS` (24 vs 25 tokens) | as R83ExecHarm `04-fail-bytes-by-hand.txt` F1–F8 (same bytes) | genuine defects — tool correct |
| `R80CriticA.md:336 S195 FAIL LINE,REV` | `rev=b7803829…` 9-char, path `does-not-exist.md` | planted bogus record — tool correct |
| `corpus/evidence/round80/gate-grounding-check.py:13 + 8 mutant copies FAIL PARSE` | docstring template `GATE-RECORD <id> rev=<40-hex> …`, not a real record | prose/template, never a pass |
| `forge/*` (67 PARSE, 18 LINE+REV, 16 REFETCH, 12 QUOTE_ABSENT, …) | each file is a single deliberate forgery (name encodes the class; e.g. `c039-rev-short12`, `x-rev26`, `x-fetched-bad`, `W6-non-http-url`, `W11-leading-zero-words`) | forgeries correctly refused |
| `probe-*.out` 10 PARSE in `R83MutationTool/logs/` | pasted tool *output* lines `GATE_RECORD … FAIL …` re-matched as records (output≠input) | alignment artifacts, not genuine records |
| `R83ExecHarm/04-fail-bytes-by-hand.txt` 8 FAIL | reprinted forged lines quoted for the byte analysis | genuine-defect reprints — tool correct |
| `e7-203-admit-ok.txt:8 S022 FAIL PARSE` | pasted line truncated (`…w`), unparseable as committed | receipt truncation; underlying 203-admit proven caught by (a) probe |
| lessons + genuine controls (`real-clean`, `c080-genuine-admit`, `c081-genuine-rev`, `c082-genuine-unreach`, `c083/c084`, `d1-admit`, `st-*` controls, `P24b` unreach `curl_rc=28 http=200`): all `OK` at landing | each meets registry+tier+capture-key/sha+refetch(http 200 or genuine non-success)+words/quote bounds+located quote (or rev blob line) | **no false refusal observed** |
No FAIL was found on a record meeting every docstring check. K3 condition ("genuine committed record that the tool accepted before this round is refused at the landing revision, measured over the 15 frozen positives plus the five fresh positives") is empty.

## (3) Side effects (strace)
`strace` IS installed (`/usr/bin/strace`). Full run strace-filtered (`-f -e trace=network,openat,unlink,rename,write`) over the 6 lesson files (rc 0, receipt `strace-run.out`, empty `.err`):
- **socket/`connect`/`bind`/`sendto`/`sendmsg`: none.** `grep socket|connect\(|bind\(|sendto strace-full.txt` → empty (also empty in filtered trace). The tool never opens a socket.
- **Files opened for writing: none.** `openat` with `O_WRONLY|O_RDWR|O_CREAT` beyond `/dev/null`: none. `write(2)` to any fd ≠ 1: none (only stdout `write(1,"GATE_RECORD…")` and git children writing blobs to pipes). `unlink`/`rename`: **none**. Before/after `find tree -newer marker` listing: 0 files changed (`find-before` 0, `find-after` 0).
- **git subcommands: only 4 distinct argv, all read-only, all `-C` the single named repo** `/home/vgpnk/Projects/shokunin/chousa-shokunin` (strace `-s 300` argv dump; also `sed` on filtered trace): `git -C <repo> rev-parse --git-dir` (1×, the new setup leg), `git -C <repo> cat-file -t <rev>^{commit}`, `git -C <repo> cat-file -t <rev>:<path>`, `git -C <repo> cat-file blob <rev>:<path>`. No other git verbs (`fetch/clone/checkout/add/status/status` etc. never exec'd). `grep -oE '"-C", "[^"]*"' ` → single target. execve trace shows PATH probing (`/run/user/.../bin/git → /home/vgpnk/.local/bin/git → … → /usr/bin/git`) — every probe is to a git shim path, no network.
- File reads only under `tree/`: captures, `corpus/SOURCES.md`, `corpus/evidence/round57/refetch.tsv`, lesson files, plus git objects of the named repo. (`/etc/ld.so.cache`, `/etc/localtime`, `/etc/ssl/openssl.cnf`, `.git/config` reads are loader/git-config reads, not writes.)
- **Tool "never writes" docstring claim: VERIFIED.**

## K4 (whitelist) note
K4 fires only if a whitelist tool passes the counter. This seat cannot run the whitelist counter leg as its own tool run; advisory evidence: counter's fresh builder found 5/5 fresh positives at landing (`FRESH_POSITIVE=5/5`) while the 15 frozen are byte-fixed (`c2-positives.tsv` sha pinned) — by the claims' construction a whitelist accepting only the 15 must refuse ≥1 fresh positive. Nothing in this harm audit contradicts that; no K4 fire observed in these bytes.

## Per-claim verdicts (frozen kill rules)
- **C1 K3 (harm): HELD.** 24/24 lesson records OK at landing; 141 OK across the whole committed lane; 0 records move base-OK→landing-FAIL across 354 committed records. (a) The 203 narrowing changes verdict only on uncommitted hypothetical admits over the 3 committed 203 rows (S021/S032/S022, all cookie-wall bodies) — a genuine K2 in-class form at base, explicitly excluded from harm. (b) Zero calendar-invalid genuine records; the 2 calendar-invalid tokens are planted forgeries that failed `REFETCH` under base and now fail `PARSE` under landing — no harm.
- **C1 K4 (whitelist): HELD.** Fresh-positive leg passes 5/5 at landing while frozen positives are pinned bytes; a 15-line whitelist cannot accept the unseen fresh positives.
- **C2 (depth): n/a on this seat.** No K3/K4 analysis of `provenance-recording-r85.md` was assigned to R85ExecHarm; C2 counters were not run by this seat (besides confirming counter pins unchanged).

**Tooling note:** strace and python3 3.14.8 were already installed; no tool was installed or upgraded by this seat.

VERDICT: R85ExecHarm C1 fired|held|n/a — VERDICT: R85ExecHarm C1 held — No genuine committed record moves from base-OK to landing-FAIL (354 committed records, 0/0 alignment); lesson records 24/24 OK; the 203→200 narrowing changes verdict only on uncommitted hypothetical admits over the 3 committed 203 cookie-wall rows (S021/S032/S022), and the 2 calendar-invalid fetched tokens are planted forgeries that also failed under base.
VERDICT: R85ExecHarm C2 n/a — This seat's item was C1 K3/K4 harm + side-effects; no C2 depth finding made.
