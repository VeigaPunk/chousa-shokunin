# R54W2ReviewSkillReadme — SKILL.md round-54 rows + corpus/README.md "Round54 coverage and frontier" truth review (FALSIFY)

Date 2026-10-26. Read first: `corpus/evidence/round54/claims.md` (freeze `5a1a206`, ancestor of HEAD, `git merge-base --is-ancestor` OK) and `claims-erratum.md` E1–E4. Lane HEAD `178667d` (W2 dispatch on top of integrated `447cf7e`); nothing below proposes changing a frozen predicate/target/counter/control. No tool installed (soffice 26.8.1.1 preinstalled; pypdf already in the uv cache — proven by an `--offline` run before the verbatim run). All runs with `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` under my scratch; lane `git status --porcelain` after every run shows only peers' W2 report files (no `__pycache__`, no droppings).

## 1. Gate registry (round47 c2-count)

`python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round47/c2-count.py` →
```
ENTRY_POINTS=144 (abc=110 dependence=+9 check_named=+25)
FLOOR=92
GATES_ROWS=64
REGISTERED=144/144
UNREGISTERED=0
DANGLING=0
MISMATCHES=0
C2=PASS
exit=0
```
Every `*.py`/`*.sh` the three round-54 rows name exists (DANGLING=0) and is registered in a Gates `entry` cell.

## 2. SKILL.md:139 `capture-text` (OLE `.doc`) tool row — every claim ran true

- Usage exits: no args → argparse usage, exit 2; `--locate ''` → `usage: --locate needs a non-empty quote`, exit 2; `--locate 'GB/T 7714'` on `6dc68fd6….raw` → `LOCATED count=4 offset=12802`, **exit 1** (2+ matches) — verdict map `0/1/2` confirmed on all three branches.
- Pins, all measured: `git show 8a7d0f1:tools/capture-text.py | sha256sum` → `fd0ed3f58565b781ab8eedaad5d229976e150bdd8e391a2b0cacd0a0825fcd89` (== row pin; landed tool differs, `2c0140bc…`, per E2 — row labels it "Candidate commit"). Five cache keys → sha256[:20]: `54fe0734…`→`d341c133e37d65f02f8f`, byte twin `74ced3e9…`→same, `6dc68fd6…`→`6063a3aff7a4081e93a6`, `b539a802…`→`46d1866ce9afd51682e7`, `bdff491a…`→`ac0fad62ed9a11fa3bd1` — all five match. Pinned quotes: `--locate` → `LOCATED count=1 offset=12795` (6dc68fd6) and `count=1 offset=4678` (bdff491a); offset 4678 equals Python `str.find` index, confirming "code-point indices".
- Self-test receipt `c1-after-candidate.txt`: four runs (three unseeded + `--seed 7`), each `LEGS=6/6 C1=PASS exit=0`, tool sha `fd0ed3f5…` — as the row states.
- Write scope "read-only; stdout only": `grep -n "open(" tools/capture-text.py` → only `rb`/zip reads; write-mode matches 0.
- "supersedes the round-52 row … by name": SKILL.md:134's row name is verbatim `capture-text` (r52 C1; the OOXML `.docx` text form for claim-vs-source checks), and its OOXML rule text is identical to row 139's "unchanged from r52" text.

## 3. SKILL.md:140 counters row — all four pinned usage probes reproduced

- `c1-count.py --per-leg 1` → `usage: --per-leg must be at least 2 (sample-size guard)` exit 2. `c2-count.py --nope` → argparse usage exit 2. `build-spans.py --cache /nonexistent-cache` → `build-spans: no capture cache /nonexistent-cache` exit 2. `build-c1-controls.py` (no arg) → uncaught `IndexError`, exit 1 (the row itself documents this). Extra verdict-map paths: `build-spans` with a scratch root and no `quotes.tsv` → `build-spans: no input …/quotes.tsv` exit 2; bad header → `header must be id url quote entry (tab-separated)` exit 2.
- `build-spans.py --check` → `SPANS_ROWS=33 STALE=0` exit 0, wrote nothing (lane status unchanged). (The writing mode `SPANS_ROWS=n WRITTEN=n` was NOT run — it writes lane files, outside my write scope; `--check STALE=0` shows the on-disk spans are exactly what the builder derives.)
- `c2-count.py` full → `C2=PASS` exit 0 (`ENTRIES=2/2`, `BOUND=3/3`, `BOUND_IDS=S121,S122,S123`, `REF_ID_UNBOUND=0`, `QUOTE_ROWS=33 ON_BOUND=33/33`, `CAPTURE_BOUND=33/33`, `SUBSTANCE=PASS`, `ANCHOR_BOUND=3/3`, `INFERENCE_GROUNDED=2/2`, `QUARANTINE_VERDICTS=3/3 (S080,S088,S096)`, `QUARANTINE_BLOCKED_ADOPTED=0`); `--lane-only` → same with `CAPTURE_BOUND=skipped` — verdict map exact.
- `build-c2-controls.py` verbatim → exit 0, both blocks `C2=FAIL`: STAGED `REF_ID_UNBOUND=6 BOUND=0/3`, TOOLED `BOUND=3/3 BOUND_IDS=S121,S122,S123 REF_ID_UNBOUND=3 ANCHOR_BOUND=0/3` — matches the row's pinned receipt text; source aborts via `git show BASE:corpus/SOURCES.md` `check=True` + `tools/assimilate-rows.py` run, scratch only `tempfile.mkdtemp` under my TMPDIR.
- Pins in source: `BASE_REV c49ffc6c…`, `OPENED 2026-10-26`, `MIN_PER_ID=3`, CACHE/REGISTER under `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/`, three URLs byte-equal to SOURCES.md S121/S122/S123 first source-cell URLs, HIT URL == S101's row URL.
- Receipts match the row: `controls/c1-before.txt` base tool `LEGS=1/6` (REGRESS only) `C1=FAIL` exit 1 ×4 runs; `controls/c1-controls.txt` `--seed 54` const `0/6`, naive `0/6`, refuseall `1/6`, shell `1/6`; `controls/c2-before.txt` `ENTRIES=0/2 BOUND=0/3 REF_ID_UNBOUND=0 SUBSTANCE=FAIL C2=FAIL` exit 1. Scratch cleanup: `c1-count.py:308` mkdtemp, `:326` rmtree.

## 4. SKILL.md:141 post-freeze row — every usage line ran as written

- `c1-supplement.py --per-leg 1` → `usage: --per-leg must be at least 2` exit 2; source guards `ENV_CHANGED soffice not found` exit 2 (soffice present, so not triggered live).
- `build-c1-forge.py <scratch>/forgeout` → exit 0, wrote `forge.py`. **Reproduced the receipt**: `c1-count.py --tool forge.py --seed 7` → `LEGS=6/6 C1=PASS` exit 0; `c1-supplement.py --tool forge.py --seed 7` → `SUPPLEMENT_LEGS=0/3 SUPPLEMENT=FAIL` exit 1 (`REFUSED ole-malformed: forge` ×3) — forge sha `f73ac5c3…` identical to `controls/c1-forge.txt`, which also shows CONST/NAIVE/REFUSEALL/SHELL `0/3`. The frozen counter stays forgeable; the supplement catches it — exactly as E1 and the row say.
- `uv run --quiet --with pypdf python corpus/evidence/round54/pdf-crosscheck.py` verbatim → `PDF_QUOTES=21 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14` exit 0 (== E4; verdict map "exit 0 iff k=0" holds; `--offline` pre-run proved no network needed).
- `considerthese-ledger-check.py` default → `PROPOSALS=35 ROWS=35 IMPL=24 FMT=9 OPEN=1 OPS=1 BAD=0` exit 0. Mutants reproduced: dropped row → `FAIL MISSING CT-20261026-4` exit 1; dead IMPL pointer → `FAIL POINTER CT-20261019-1 no/such/file.py` exit 1; `--ledger /nonexistent` → `USAGE …` exit 2.
- `tracked-deletion-check.py` → `TRACKED_DELETION=PASS` exit 0 (landed tool). Candidate blob (sha `fd0ed3f5…`) → `tracked.doc rc=0 BAD '…DELETEDTEXT…'`, `TRACKED_DELETION=FAIL` exit 1 — the row's "candidate prints DELETEDTEXT and fails, the landed tool passes" reproduced both arms.
- `measure-after.txt`: landed tool sha `2c0140bc…` named; C1 `6/6` ×4, supplement `3/3` ×4, tracked-deletion PASS, C2 PASS — matches the row.

## 5. build-spans UTF-16LE statement — TRUE in source

`build-spans.py:5-8` ("for any other raw it stays the UTF-16LE decoding (the round-48 OLE `.doc` finding)"), `:14-16` ("carries its OWN `.docx` reader … so the C2 claim is verifiable without the C1 tool `tools/capture-text.py`"), `:107-113` `raw_form`: `docx_text` for a `PK\x03\x04` zip, else `b.decode("utf-16le", errors="replace")`; no import of `tools/capture-text.py`. SKILL's "(it does NOT use the round-54 OLE text form)" and README's "still slices a non-zip `.raw` as UTF-16LE … no new `.doc` quote is written until it reads through the tool" are both true (spans.tsv holds only S121/S122/S123 rows).

## 6. README "Round54 coverage and frontier" — checked against the files it describes

- r36 row: every quoted string present in `source-type-taxonomy-r36.md` (`发布 于 2025-12-02`, `实施 于 2026-07-01`, `（全部代替）`, `本标准非等效采用ISO国际标准：ISO 690:2021。`, `本系统不提供文本阅读服务`, 归口 filled by different bodies on the two pages). The entry's own recheck one-liner run verbatim → `1 1797 1 15212`, exactly its pinned values. S121 `.txt` chars 1000–1100: `…标准状态…发布 于 2025-12-02 \n\n 实施 于 2026-07-01…` — adjacent lines of one block, not one contiguous string, as README says.
- r37 row: scope exclusion (`本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。`), 7.3 carrier-after-slash rule, `附录Ａ（规范性）` vs `附录Ｂ（资料性）`, five carrier rows 磁带/磁盘/光盘/联机网络/缩微资料(MM), change-list renames (普通图书→图书, 舆图→地图, EB→网站、网页), 7.6 `ＹＹＹＹ－ＭＭ－ＤＤ`, colophon `中国标准出版社出版发行`, OCR slip `图书主要贵任者` — all in the entry.
- Per-document credit: base sweep re-run verbatim → `exit=1`, no output (three documents absent at base; c2-count's BOUND logic independently proves the three rows are new-since-BASE_REV and first-URL-bound). S101 earns none: `grep S101 source-type-taxonomy-r37.md` → no match (E3 cut), c2-count `HELD_CITED=- HELD_BAD=0`.
- S082 history: `corpus/lessons/round-44.md:108` "Staged S082, the SAMR record for GB/T 7714-2025" + `citation-version-binding-r36.md:21` "Round 43 classed that row not-carried … Flip: a text capture of that record contains the issued and effective dates as a cont[iguous span]"; r36 entry's Unknown states the flip "is met line by line, not as one span" — README's sentence is faithful.
- S130 claim: tool on `bdff491a….raw` → len 13718, `find('是否检索灰色文献')=4678`, U+FFFD count 0 — README's "char 4678, 0 U+FFFD" exact.
- Corrections: SCORECARD `## Round 54 pointer corrections` at :2736 with exactly 9 `^correction: ` lines; mechanical check of all nine (`anchor` at its recorded `char<N>` in its target dump) → `OK=9 BAD=0`; dumps byte-identical to tool output (`diff` → `S100_MATCH` on `b539a802`, `S101_MATCH` on `6dc68fd6`); dump sha256 prefixes `70ca0f0d…`/`a8e3e7ad…` match the preamble; the preamble's `263 U+FFFD, 243 0x0B` equals my measured whole-file UTF-16LE decode of the S101 capture exactly, as relayed from lesson `## Mistakes` row 2. (S100's own decode is 11154 U+FFFD / 26 0x0B — equally broken; the preamble's parenthetical numbers are S101's, faithfully cited from the lesson row it names. Borderline wording, not a defect.)
- Frontier: "Advanced" tier/form items match the entries; every "Left open" item is real — the HIT carrier-alphabet item correctly waits on a span builder that reads OLE `.doc` (build-spans cannot, per §5); 表Ａ．２ applicability and the entitled-copy collation are disclaimed in r37's Unknown; S130 adoption deferred.

## Findings

No defect found. Every usage line in the three round-54 SKILL rows ran as written with the documented exit code; every pin (commit ids, tool/blob sha256, five cache-key digests, two quote offsets, BASE_REV/OPENED/MIN_PER_ID, receipt contents) verified by direct measurement; the build-spans UTF-16LE statement is true in source; the README's per-document credit, S101 non-citation, S082 history, S130 form, correction anchors and frontier claims all check against the files. Residual: the writing mode of `build-spans.py` and the soffice-missing `ENV_CHANGED` arms were verified via `--check`/source, not live (writing mode would breach my write scope; soffice is present).

VERDICT: attacked the three round-54 SKILL gate rows and the README Round54 section line by line — usage lines, exit codes 0/1/2, all pins, the UTF-16LE statement, per-document credit, corrections and frontier — with ~30 executed commands including a forge reproduction (6/6 vs 0/3) and a nine-anchor mechanical check; everything survived, zero defects.
