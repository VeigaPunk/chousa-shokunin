# R83MutationTool — mutation test of `tools/gate-records.py` against the frozen C2 counter

Seat R83MutationTool (leaf; no subagents). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Subject: `tools/gate-records.py` at the candidate landing `81b81173f19d175e2b2a6b409b2a496d09d0b258`
(sha256 `d38443769fe7c2ba014ec9d7861c4078cec24d0a193eeadb2cd5222d0d392687`; byte-identical at tip
`aca2a781`, verified with `git diff --stat 81b81173 aca2a781 -- tools/gate-records.py` → empty).
Counter: `corpus/evidence/round83/gate-records-r83.py`, sha256
`a1d86a925630ef4e322f1d85be1e917b7cb9b94e0e9bf00c1ffa4db62e1e7bb6`, equal to its `instrument-pins.txt` pin.
Positives table `c2-positives.tsv` sha256 `8c089828981bb0c8b5a0ab253bb4ec5f1537825cb84cea8964497310bb01f3c6`, also pinned.
Scratch `/fast/scratch/hyaku/chousa-r83/R83MutationTool` (removed before yield; every cited receipt was copied here first).
No tool was installed or upgraded for this seat.

## 1. Baseline (pristine tool, pristine tree)

```
$ cd /fast/scratch/hyaku/chousa-r83/R83MutationTool
$ python3 -B corpus/evidence/round83/gate-records-r83.py \
    --root /fast/scratch/hyaku/chousa-r83/R83MutationTool \
    --repo /home/vgpnk/Projects/shokunin/chousa-shokunin \
    --work /fast/scratch/hyaku/chousa-r83/R83MutationTool
TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3
GATE_RECORDS_R83=PASS
rc=0
```

Receipt `R83MutationTool/00-baseline.out`. The tree is `git archive 81b8117 | tar -x -C <scratch>`.
Baseline PASS, so every mutant below is scored against a green detector.

## 2. Method

36 single-point mutants of the subject, each a byte-copy with exactly one edit (each `old` asserted to occur
exactly once in the pristine file before writing). Every mutant was scored by the frozen counter through its
`--tool` override, same root, same repo, same work dir:

```
python3 -B corpus/evidence/round83/gate-records-r83.py \
  --root /fast/scratch/hyaku/chousa-r83/R83MutationTool \
  --repo /home/vgpnk/Projects/shokunin/chousa-shokunin \
  --tool /fast/scratch/hyaku/chousa-r83/R83MutationTool/mutants/<label>.py \
  --work /fast/scratch/hyaku/chousa-r83/R83MutationTool
```

The 36 were run 8-way parallel (`drivers/mutate.py`), then the 15 survivors were re-run serially and reproduced
identically. The pristine subject was never edited: its sha256 after all runs is still
`d3844376…392687` (`data/mutant-manifest.txt`). Mutant files and their unified diffs are in `mutants/`,
per-run stdout+stderr in `logs/<label>.out`, the machine summary in `01-summary.tsv` / `02-results.json`.

Forgery mix of the frozen battery: 10 admit positives × 17 mutations, 1 unreach × 4, 4 rev × 6 = 198.

## 3. Results — 36 mutants, 21 killed, 15 survivors, 0 inconclusive

```
label                          verdict   rc  counter line
M01-sha-min-1                  KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=188/198 EXPECTED_CODE=188/198 EMPTY_REFUSED=1/1 RC=3/3
M02-drop-capture-key           KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=178/198 EMPTY_REFUSED=1/1 RC=3/3
M03-drop-refetch-txtsha        SURVIVOR  0   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3
M04-drop-refetch-fetched       KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=188/198 EXPECTED_CODE=188/198 EMPTY_REFUSED=1/1 RC=3/3
M05-accept-curl-nonzero        SURVIVOR  0   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3
M06-accept-non2xx              SURVIVOR  0   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3
M07-words-off-by-one           KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=174/198 EXPECTED_CODE=174/198 EMPTY_REFUSED=1/1 RC=3/3
M08-quote-len-0-26             KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=189/198 EXPECTED_CODE=178/198 EMPTY_REFUSED=1/1 RC=3/3
M09-skip-lead-strip            KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=188/198 EXPECTED_CODE=188/198 EMPTY_REFUSED=1/1 RC=3/3
M10-skip-indented              KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=188/198 EXPECTED_CODE=188/198 EMPTY_REFUSED=1/1 RC=3/3
M11-rev-short                  SURVIVOR  0   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3
M12-line-whole-blob            KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=195/198 EXPECTED_CODE=195/198 EMPTY_REFUSED=1/1 RC=3/3
M13-exit0-zero-records         KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=0/1 RC=2/3
M14-exit0-with-fail            KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=0/1 RC=1/3
M15-drop-registry              KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=188/198 EMPTY_REFUSED=1/1 RC=3/3
M16-drop-tier                  KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=188/198 EXPECTED_CODE=188/198 EMPTY_REFUSED=1/1 RC=3/3
M17-drop-capture-path          KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=188/198 EMPTY_REFUSED=1/1 RC=3/3
M18-drop-capture-sha           KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=178/198 EXPECTED_CODE=178/198 EMPTY_REFUSED=1/1 RC=3/3
M19-drop-quote-absent          KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=178/198 EXPECTED_CODE=178/198 EMPTY_REFUSED=1/1 RC=3/3
M20-dup-key-accept             KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=188/198 EXPECTED_CODE=188/198 EMPTY_REFUSED=1/1 RC=3/3
M21-parse-fail-ok              KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=177/198 EXPECTED_CODE=177/198 EMPTY_REFUSED=1/1 RC=3/3
M22-drop-refetch-url           SURVIVOR  0   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3
M23-drop-refetch-sid           KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=188/198 EXPECTED_CODE=188/198 EMPTY_REFUSED=1/1 RC=3/3
M24-unreach-accept-success     SURVIVOR  0   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3
M25-unreach-drop-fetched       KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=197/198 EXPECTED_CODE=197/198 EMPTY_REFUSED=1/1 RC=3/3
M26-unreach-drop-http          KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=197/198 EXPECTED_CODE=197/198 EMPTY_REFUSED=1/1 RC=3/3
M27-quote-len-admit-only       SURVIVOR  0   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3
M28-cap-re-loose               SURVIVOR  0   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3
M29-no-islink                  SURVIVOR  0   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3
M30-ts-loose                   SURVIVOR  0   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3
M31-int-loose                  SURVIVOR  0   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3
M32-rev-no-pop                 SURVIVOR  0   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3
M33-unreach-decision-any       KILLED    1   TOOL=present POSITIVE=15/15 FORGED_REFUSED=197/198 EXPECTED_CODE=197/198 EMPTY_REFUSED=1/1 RC=3/3
M34-admit-quote-unterminated   SURVIVOR  0   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3
M35-drop-url-regex             SURVIVOR  0   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3
M36-drop-ts-check              SURVIVOR  0   TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3
```

Every row's full stdout+stderr is `logs/<label>.out`; the same data machine-readable in `01-summary.tsv`.

## 4. Survivors — exact diff, killing class, and what the landed tool does with that class

For each survivor I built the killing input, ran the **landed** tool and the **mutant** on the same probe file
(`probes/<probe>.md`, outputs `logs/probe-<probe>.out`). A survivor is a battery blind spot; it is a C2 kill only
if the landed tool accepts the class. It never did (section 5).

### 4.1 Killable with committed lane bytes (9)

**M03-drop-refetch-txtsha** — `logs/M03-drop-refetch-txtsha.out`
```diff
-                 and re.fullmatch(r"2\d\d", r[6]) and capsha is not None and r[8] == capsha for r in refetch)
+                 and re.fullmatch(r"2\d\d", r[6]) and capsha is not None for r in refetch)
```
Killing class: an admit record pinned to a refetch row whose `txt_sha256` differs from `sha256(capture)`.
The committed log contains such rows: `S113 @ 2026-10-27T08:07:08Z` (row txt `cc79e6bf…`, capture sha `6e2577b0…`)
and `S114 @ 08:07:11Z` (data/reachability.txt §D). Probe `P03-stale-refetch-row`:
- landed: `GATE_RECORD …/P03-stale-refetch-row.md:1 S113 FAIL REFETCH`, rc 1
- mutant: `GATE_RECORD …/P03-stale-refetch-row.md:1 S113 OK`, rc 0
A forgery of this shape expecting `REFETCH` kills the mutant. Landed tool refuses it — no K2.

**M11-rev-short** — `logs/M11-rev-short.out`
```diff
-        if HEX40_RE.fullmatch(kv["rev"]):
+        if re.fullmatch(r"[0-9a-f]{4,40}", kv["rev"]):
```
Killing class: rev record with an abbreviated rev. Probe `P11-short-rev` (`rev=b780382`):
- landed: `… S199 FAIL LINE,REV`, rc 1
- mutant: `… S199 OK`, rc 0
A rev forgery expecting `REV` kills it. Landed tool refuses (with `REV`; see residual R5 on the code choice).

**M24-unreach-accept-success** — `logs/M24-unreach-accept-success.out`
```diff
-        success = kv["curl_rc"] == "0" and kv["http"].startswith("2")
+        success = False
```
Killing class: an unreach record whose (id, url, fetched) row is a successful fetch. Probe `P24-unreach-claims-success`
(S113 @ 08:30:59Z, rc 0, http 200):
- landed: `… S113 FAIL REFETCH`, rc 1
- mutant: `… S113 OK`, rc 0
A forgery of this shape expecting `REFETCH` kills it. Landed tool refuses — no K2.

**M27-quote-len-admit-only** — `logs/M27-quote-len-admit-only.out`
```diff
-        if not 1 <= n <= 25:
+        if form == "admit" and not 1 <= n <= 25:
```
Killing class: rev record with a 26-word quote. Probe `P27-rev-26-words` (QUALITY.md line 845 at `b780382`):
- landed: `… S200 FAIL QUOTE_LEN`, rc 1
- mutant: `… S200 OK`, rc 0
A rev forgery expecting `QUOTE_LEN` kills it. Landed tool refuses — no K2.

**M30-ts-loose** — `logs/M30-ts-loose.out`
```diff
-TS_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
+TS_RE = re.compile(r"\S+")
```
Killing class: `fetched` that is not a timestamp. Probe `P30-bad-timestamp` (`fetched=2026-11-06`):
- landed: `… S113 FAIL PARSE`, rc 1
- mutant: `… S113 FAIL REFETCH`, rc 1
A forgery expecting `PARSE` kills it (refused but with the wrong code). Landed tool refuses — no K2.

**M31-int-loose** — `logs/M31-int-loose.out`
```diff
-INT_RE = re.compile(r"0|[1-9]\d{0,6}")
+INT_RE = re.compile(r"\d{1,7}")
```
Killing class: `words`/`line` with a leading zero. Probe `P31-words-leading-zero` (`words=012`):
- landed: `… S113 FAIL PARSE`, rc 1
- mutant: `… S113 FAIL WORDS`, rc 1
A forgery expecting `PARSE` kills it. Landed tool refuses — no K2.

**M34-admit-quote-unterminated** — `logs/M34-admit-quote-unterminated.out`
```diff
-        if len(q) < 2 or not (q.startswith('"') and q.endswith('"')):
+        if len(q) < 1 or not q.startswith('"'):
```
Killing class: admit record whose quote has no closing `"`. Probe `P34-unterminated-quote`:
- landed: `… S113 FAIL PARSE`, rc 1
- mutant: `… S113 OK`, rc 0
This is the sharpest survivor: the mutant accepts a malformed record as genuine (the truncated quote still matches by
substring). A forgery expecting `PARSE` kills it. Landed tool refuses — no K2.

**M35-drop-url-regex** — `logs/M35-drop-url-regex.out`
```diff
-        if not re.fullmatch(r"https?://\S+", kv["url"]) or not TS_RE.fullmatch(kv["fetched"]):
+        if not TS_RE.fullmatch(kv["fetched"]):
```
Killing class: `url` that is not http(s). Probe `P35-ftp-url` (`url=ftp://example.org/x`):
- landed: `… S113 FAIL PARSE`, rc 1
- mutant: `… S113 FAIL CAPTURE_KEY,REFETCH`, rc 1
A forgery expecting `PARSE` kills it. Landed tool refuses — no K2.

**M36-drop-ts-check** — `logs/M36-drop-ts-check.out`
```diff
-        if not re.fullmatch(r"https?://\S+", kv["url"]) or not TS_RE.fullmatch(kv["fetched"]):
+        if not re.fullmatch(r"https?://\S+", kv["url"]):
```
Same killing class and probe as M30 (`P36-bad-timestamp`: landed `FAIL PARSE`, mutant `FAIL REFETCH`). Landed tool
refuses — no K2.

### 4.2 Killable only by writing into `corpus/captures/` (2; out of class for K2)

**M28-cap-re-loose** — `logs/M28-cap-re-loose.out`
```diff
-CAP_RE = re.compile(r"corpus/captures/([0-9a-f]{24})\.txt")
+CAP_RE = re.compile(r"corpus/captures/(.+)\.txt")
```
Killing class: `capture=corpus/captures/<stem not 24 hex>.txt` naming a **real** file. The committed captures dir has
76 `.txt` files, all 24-hex, and 79 `.raw` files; a nonexistent non-hex path does not separate the mutant (the
`isfile` branch still raises `CAPTURE_PATH`). Probe `P28-nonhex-capture-name` (a copy of the S113 capture named
`zz-not-hex.txt` in the scratch tree):
- landed: `… S113 FAIL CAPTURE_PATH,CAPTURE_SHA,QUOTE_ABSENT,REFETCH`, rc 1
- mutant: `… S113 FAIL CAPTURE_KEY`, rc 1
A forgery expecting `CAPTURE_PATH` kills it. Landed tool refuses — no K2; the class needs a capture-tree write, which
K2 declares out of class.

**M29-no-islink** — `logs/M29-no-islink.out`
```diff
-        if (cap is None or os.path.islink(cap) or not os.path.isfile(cap)
+        if (cap is None or not os.path.isfile(cap)
```
Killing class: a symlink at the capture path resolving inside `corpus/captures/`. Zero symlinks are committed
(data/reachability.txt §E). Probe `P29-symlink-capture` (scratch root `tree-sym/`, capture replaced by a symlink to
a sibling file with the same bytes):
- landed: `… S113 FAIL CAPTURE_PATH,CAPTURE_SHA,QUOTE_ABSENT,REFETCH`, rc 1
- mutant: `… S113 OK`, rc 0
A forgery expecting `CAPTURE_PATH` kills it. Landed tool refuses — no K2; needs a capture-tree write.

### 4.3 Not distinguishable with the committed bytes (4; equivalent under this data)

**M05-accept-curl-nonzero** — `logs/M05-accept-curl-nonzero.out`
```diff
-        ok = any(r[0] == sid and r[1] == url and r[2] == key and r[4] == kv["fetched"] and r[5] == "0"
+        ok = any(r[0] == sid and r[1] == url and r[2] == key and r[4] == kv["fetched"]
```
To accept, a record must match a row with `curl_rc != 0`, `http` 2xx **and** a real `txt_sha256`. The log has 13 such
rows and **none** has a real `txt_sha256` (all `-`; data/reachability.txt §B). Probe `P05-curl28-2xx-row` (S103,
rc 28, http 200): landed and mutant both `FAIL REFETCH` rc 1. Unreachable class with committed bytes.

**M06-accept-non2xx** — `logs/M06-accept-non2xx.out`
```diff
-                 and re.fullmatch(r"2\d\d", r[6]) and capsha is not None and r[8] == capsha for r in refetch)
+                 and re.fullmatch(r"\d{3}", r[6]) and capsha is not None and r[8] == capsha for r in refetch)
```
Needs a non-2xx row with a real `txt_sha256`: 26 non-2xx rows, **none** with one (§C). Probe `P06-non2xx-row`:
both `FAIL REFETCH` rc 1. Unreachable class with committed bytes.

**M22-drop-refetch-url** — `logs/M22-drop-refetch-url.out`
```diff
-        ok = any(r[0] == sid and r[1] == url and r[2] == key and r[4] == kv["fetched"] and r[5] == "0"
+        ok = any(r[0] == sid and r[2] == key and r[4] == kv["fetched"] and r[5] == "0"
```
To separate it you need a row whose `key` is not `sha256(url)[:24]`, because the record's key is always derived from
its own url; there are **0** such rows (§A), so a url change forces a key change and `CAPTURE_KEY` co-fires. Probe
`P22-url-swap-keeps-capture` (S114 url with S113 capture): landed and mutant both `FAIL CAPTURE_KEY,REFETCH` rc 1.
Unreachable class with committed bytes.

**M32-rev-no-pop** — `logs/M32-rev-no-pop.out`
```diff
-            if lines and lines[-1] == "":
-                lines.pop()
+            pass
```
Equivalent mutant: without the pop the bound grows by one, but the phantom line is empty, so the `LINE` check still
fires for `line = len+1`. Probe `P32-line-past-eof`: landed and mutant both `FAIL LINE` rc 1. No input distinguishes
them.

## 5. K2 candidates

**None.** For every survivor class above the landed tool prints `FAIL` (section 4), so no in-class record that
violates a docstring check is accepted. The landed tool is strictly stronger than each mutant on the class that the
mutant relaxes. I did not test K3 (genuine-record harm) or the C2 predicate (b) at the tip — out of this seat's scope.

## 6. Residuals (out of class or non-killing observations)

- **R1 — the forgery generator never varies the data side.** All 198 forgeries mutate only the 15 positive record
  lines; `refetch.tsv` and `corpus/captures/` are never varied. Every REFETCH sub-check that needs a data-side
  divergence is therefore untested, except where the committed data already diverges — and it does: six rows carry a
  capture whose sha256 differs from the row's `txt_sha256` (§D), and the battery does not use any of them. M03 is the
  concrete survivor. Routed defect: add a forgery pinned to `S113 @ 2026-10-27T08:07:08Z` expecting `REFETCH`.
- **R2 — one expected code per forgery.** When two checks co-fire with different codes, a mutant that drops one
  survives (M22: url vs key; M28: `CAPTURE_PATH` vs `CAPTURE_KEY`). Routed defect: allow a forgery to expect a code
  set, or add a forgery that isolates the check.
- **R3 — the counter cannot express two `CAPTURE_PATH` branches.** Forgeries live in its own mkdtemp, captures are
  read from `--root`; a symlinked capture and a non-hex-named `.txt` capture cannot be presented without writing the
  lane tree. Routed defect: run the F leg against a temp root carrying those two fixtures.
- **R4 — PARSE coverage is thin.** 21 of 198 forgeries expect `PARSE` and all are missing/duplicate-key shapes
  (`M15`, `M16`, `U04`). No forgery covers a bad url shape, a bad timestamp, a bad integer, or an unterminated
  quote — hence M30/M31/M34/M35/M36 survive, and M34's mutant accepts a truncated quote as `OK`. Routed defect: one
  PARSE forgery per value grammar.
- **R5 — short-rev code choice (not a kill).** The landed tool reports `FAIL LINE,REV` for an abbreviated rev
  (probe `P11-short-rev`), while its form spec says `rev=<40 hex>` and PARSE covers "bad value". It still FAILs, and
  K2 requires `OK`, so this is a docstring/code-choice note for the next round, not a firing.
- **R6 — unreach "denote a success" reading (recorded, not scored).** Probe `P24b-unreach-http200-rc28`:
  `GATE-RECORD S103 url=https://library.um.edu.mo/upload/databases/c1b0fa89e2809581b12c79b9c60ea1af.pdf fetched=2026-10-27T08:05:52Z tier=B decision=reject capture=none curl_rc=28 http=200 words=0 quote=none`
  → landed `OK`, rc 0. Row S103 is `curl_rc 28, http 200, txt_sha256 "-"` (the transfer timed out; nothing was
  captured). Under the reading "http 2xx denotes success" this would violate REFETCH; under the tool's reading
  (`success = curl_rc 0 AND 2xx`) the record is truthful and `OK` is correct. I do not score it as a K2 firing; the
  bytes are recorded so a reviewer can rule on the reading.

## 7. Receipts

- `R83MutationTool/00-baseline.out` — baseline command, output, rc, pins, tree provenance.
- `R83MutationTool/01-summary.tsv`, `02-results.json` — all 36 mutants: label, description, counter line, rc, verdict.
- `R83MutationTool/mutants/<label>.py` and `<label>.diff` — exact mutant bytes and single-point diff.
- `R83MutationTool/logs/<label>.out` — exact command, counter stdout+stderr, rc for each mutant.
- `R83MutationTool/logs/probe-*.out` — landed vs mutant on each killing-class probe.
- `R83MutationTool/probes/*.md` — the probe record lines themselves.
- `R83MutationTool/data/reachability.txt` — row/capture reachability counts (§A–§E).
- `R83MutationTool/data/mutant-manifest.txt` — sha256 of every mutant; pristine subject re-hash after all runs.
- `R83MutationTool/data/serial-survivor-recheck.txt` — the 15 survivors re-run serially, all `PASS` rc 0.
- `R83MutationTool/drivers/mutate.py`, `drivers/probes.py` — the drivers that produced the above.

VERDICT: R83MutationTool C2 held — baseline `GATE_RECORDS_R83=PASS` rc 0 and no survivor class is accepted by the landed tool (every probe prints FAIL), but 15/36 mutants survive the frozen battery, 9 of them killable with committed lane bytes (M03, M11, M24, M27, M30, M31, M34, M35, M36), so the counter is a routed blind spot rather than a C2 falsification.
