# R100ReviewerC1 — C1 correctness review at freeze F `6d4e8487` (seat S=`/fast/scratch/hyaku/chousa-r100/R100ReviewerC1`)

Tree: shared clone `git clone -q --shared …/chousa-shokunin $S/repo`, checkout F. Diff base→F for `tools/gate-records.py` and `corpus/evidence/round100/challenge-controls-r100.py` read in full (58-diff / 419-line battery). Batteries run against `$S/repo`, never the live lane. Receipts: `R100ReviewerC1-candidate.txt`, `R100ReviewerC1-base.txt`, `R100ReviewerC1-receipt.txt` (this directory).

## Reproduction (all observed, not assumed)

- Candidate: `python3 -B corpus/evidence/round100/challenge-controls-r100.py --root . --work $S/w-cand` → exit 0, tail `NEG=7/7 MARK=11/11 BOUND=3/3 NORM=2/2 POS=4/4 REV=11/11 REVPOS=3/3 PROD=6/6 HARM_SAME=27/27 BASE_REV_ADMITTED=8/11 ORACLES_REJECTED=12/12`, `CHALLENGE_CONTROLS_R100=PASS`. Predicate (claims.md l.22-23) matches exactly, HARM 27 ≥ 26.
- Base: same battery `--tool $S/base-tool.py --no-oracles` (base tool `git show 929c784c:tools/gate-records.py`, sha256 `e92c4526…b3c1`) → exit 1, `REV=3/11 PROD=4/6 FAIL`. `diff` of the 47 `CASE` lines vs `corpus/evidence/round100/before/c1-base.txt`: **identical** — (4) the before receipt really ran the base tool with the frozen battery. Battery+tool unchanged between P=`96835234` and F (`git diff P F -- battery tool` empty, rc=0), so `before/c1-candidate.txt` (PASS, ORACLES 12/12) is the code under review.

## (1) Docstring ↔ code — HELD, two loose edges

`tools/gate-records.py:45-57` and `rev_capture_text:261-276` / `capture_oids:244-258` agree with `claims.md:11-17` on identity = oid equality via `git rev-parse --verify --quiet rev:path` vs `git ls-tree -z rev -- corpus/captures/`, `.raw` → sibling `.txt` via `git_blob` at that rev when present, whole-blob judged otherwise, unchanged `is_challenge` (`tools/gate-records.py:133-136`, markers/200-words). Residual edges (no claim false):
- Docstring "The text judged is the whole blob" (l.56) is immediately qualified by the sibling clause — loose but not a falsehood; claims.md sentence phrases it correctly. **Held.**
- rev-parse failure is unstated: code returns `None` (→ not CHALLENGE). Unreachable in `check()`'s call path — `rev_capture_text` runs only when `git_blob` already proved (rev, path) resolves, so `rev-parse` cannot fail except on unencodable paths. Harmless; noting for honesty.
- `capture_oids` fails open on ls-tree error (empty map → non-capture → OK) but only reachable if rev is invalid, which `blob is None` already excluded. No defect.

## (2) `capture_oids` parsing — HELD

`meta, _, path = ent.partition("\t"); parts = meta.split(); len==3 and type=="blob" and CAPANY.fullmatch(path)`. Probed with live fixtures (`$S/fx`, `$S/fx2`):
- `-z` output verified: `mode TAB type TAB oid NUL path`. A capture path cannot contain tab/newline (regex `[0-9a-f]{24}`), so a tab-bearing **non**-capture path splits at the first tab and `fullmatch` rejects the remainder — excluded, no corruption.
- Non-recursive: `ls-tree rev -- corpus/captures/` lists top-level entries only (+ a `tree` entry for subdirs). `corpus/captures/sub/<key>.txt` is thereby not a "the rev's tree" entry — matches the sentence, which names `corpus/captures/<24 hex>` exactly. A subdir file would also not be admitted by the url/admit `CAP_RE` path rule, so exclusion is coherently correct, not a hole.
- `.txt wins` is order-independent: `if oid not in m or path.endswith(".txt")` overwrites raw→txt, never txt→raw. Verified with same-oid `.raw`/`.txt` fixture.
- Mode unchecked: a `120000` symlink's ls-tree type is `blob`, so a symlinked capture path IS entered (and its target bytes judged). Only reachable as a weird state; arguably correct ("entry"). Not a falsehood. No battery leg covers it — consistent with named limit (b)/(e), not a defect at F.

## (3) Battery legs vs claims.md — HELD with ONE coverage gap

Verified each leg's mechanism, not just tallies:
- **REV distinctness**: r1 `./`, r2 `//`, r3 `/./`, r4 `../` are spelling variants of **one** mechanism (git tree normalisation), r5/r6 `.raw`-sibling (two different blobs), r7/r8 byte-copies (two blobs), r9 whole-blob, r10 exact (round-99), r11 rev-internal `norm`. r1–r4 are one route spelled four ways — the battery docstring (§REV, l.24-33) lists them accurately, claims.md makes no distinctness claim. Not a defect; recorded so a reader cannot mistake 11 for 11 independent mechanisms.
- **r9**: `S234` line 8 ("Client Challenge") and line 14 ("A required part of this site couldn't load…") carry markers; `rev_record(skip_markers=True)` (battery l.190-198) picks line 15 ("extension, network issues, or browser settings. …") — a markerless quotable line. "quoting a line with no marker (the whole blob is judged)" — **true**.
- **q3**: `corpus/evidence/captures-note.txt` (NOTE, l.104: marker "reCAPTCHA", 15 words) oid not in map → admitted. "not a capture; a marker in a short non-capture blob is not CHALLENGE" — **true**, and it is the leg that kills o4.
- **PROD**: `run(tool, lane, …)` without `--repo` (l.292-301); tool defaults `repo=root` (`gate-records.py:381`) — the production path against LANE's registry/refetch/git objects at BASE. Six legs = claims.md's enumeration. **true.**
- **12 oracles, each run myself** (imported `score()`, per-oracle file, failing `CASE` lines captured — `R100ReviewerC1-receipt.txt`): all 12 `ok=False`. Failure sets: o1→r7,r8; o2→r5,r6,PROD-raw; o3→r5,r6,PROD-raw; o4→q3; o5→q1; o6→r5,r6,r8,r11,PROD-raw (correctly NOT r7 — S230's sha is in its list); o7→r1–r11; o8→PROD×4 rev; o9→m10; o10→b200; o11→b201; o12→r11. Each fails for its stated reason (docstring l.39-45).
- **GAP (named limit (d) untested)**: no battery leg has a `.raw` **without** a sibling `.txt`. o2 (txt-only) and o3 (no-sibling) produce **identical** fail sets, so the battery cannot distinguish "judge raw by own bytes" from "ignore raw" — the positive behaviour claims.md states in named limit (d) ("A `.raw` entry with no sibling `.txt` at that rev is judged by its own bytes"). I wired a raw-only fixture myself: the **code is correct** (`FAIL CHALLENGE`), so the gap is battery-coverage-only. Named limit (e) ("the twelve named stand-ins, not every possible forger") does not honestly cover it — (d) is stated positive behaviour, not a forger class, and S230's own raw (620 words, non-challenge) vs `.txt` (23 words, challenge) proves the distinction is load-bearing. Actionable: three-line fixture addition. Not claim-falsifying at F (code honours (d)); it fires on the battery's implication that ORACLES 12/12 pins every stated variant. The claims Sentence itself does not claim (d) is leg-pinned, so the verdict is narrow.

## (4)(5) Before receipt / QUALITY 126

- (4) **held** — see Reproduction. The before receipt's CASE lines are byte-identical to my re-run at F.
- (5) **126**: the battery is a tool-mutant/oracle battery with committed before/ receipts and recorded limits — it demonstrates the battery **can fail** (12/12 mutants rejected, base FAIL). It is not a detection-forger battery for the **tool** (a tool branching on cwd/env/argv to detect the lab is untested). Named limit (e) names exactly this residue. Is (e) the honest residue? For the tool-side detection class, yes — (e) is needed and accurate. For the named-limit-(d) leg gap, (e) does not cover it (different defect class; §3 above). I find no overclaim against 126 as written; the battery does what 126's structure demands, with (e) disclosed.

## (6) Separability — HELD

`harm_files` (battery l.332-341) includes `corpus/knowledge/quotation-error-update-r100.md` (C2's entry): 27 HARM files, 10 of which carry rev records. `HARM_SAME=27/27` proves the candidate changes nothing on C2's file, and C2's entry has no `rev=` record. Its captures (S238 `b5eec205…` 327 words, S236 `405a0054…` 307 words) are `is_challenge=False` — "no challenge capture in C2's entry" is literally true, and the url/admit branch is untouched by the diff, so C2's counters ("run with the base tool unchanged") are genuinely unchanged.

## Kill rule sweep

`grep GATE-RECORD .ufo/waves/round-100/` at F: only `claims.md` prose mentions — no wave-100 artifact carries a rev record, so the kill rule's last clause ("any wave artifact shows a rev record whose blob has a capture's oid … and which this tool prints OK") cannot breach at F. (173 rev records exist across older waves; none is a wave-100 artifact.)

## Residual risk

- Battery leg for `.raw`-without-sibling (named limit (d)) — code right, battery silent. A future regression there would pass 12/12.
- rev-parse-failure / ls-tree-error fail-open paths are unreachable today but unstated in the docstring; a refactor could make them reachable silently.
- The r1–r4 spelling legs test one mechanism four ways; if git changed `.`/`..` handling in rev-paths, four legs would move together.

VERDICT: R100ReviewerC1 C1 held — the sentence, tally, before-receipt, and separability all reproduce/meets, with the battery silent on named limit (d)'s raw-without-sibling behaviour (code correct, verified by my own fixture).
