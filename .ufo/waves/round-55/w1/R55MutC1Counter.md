# R55MutC1Counter — mutation test of the frozen C1 counter `corpus/evidence/round55/c1-count.py`

seat: R55MutC1Counter · lane commit 6ca924995d48facbf704d2aa22ddaec236059039 (candidate
`tools/build-spans.py` present); BASE dba605deb5cd5ed4874e0e3c39ba24737409cd80.
Scratch: `/fast/scratch/hyaku/chousa-r55/R55MutC1Counter` (removed before finish).

## Method (grounded)

```
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 6ca9249... | tar -x -C $S/lane
git -C $S/lane init -q && git -C $S/lane fetch -q <lane> 6ca9249... dba605de...
git -C $S/lane checkout -qf FETCH_HEAD
git -C $S/lane rev-parse --show-toplevel → /fast/scratch/.../lane   (fixture repo verified)
git -C $S/lane status --porcelain | wc -l → 0
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round55/controls/build-c1-controls.py $S/ctl
  → delegate.py r54shim.py txtonly.py
python3 $S/lane/corpus/evidence/round55/c1-count.py --tool <T> --seed 55 --work $S/w-<tag>   (fresh empty dir each run)
```

Note: the archive copy alone is insufficient — REGRESS runs `git -C LANE show BASE_REV:...`
(counter line 393), so the scratch lane was made a fixture repo with the two revs fetched
first; the counter sha256 was unchanged by this (see restoration evidence). No lane file was
written; mutations were applied to `$S/lane/corpus/evidence/round55/c1-count.py` only.

## Baseline (pristine counter, --seed 55, per-leg 3) — reproduces claims.md

- candidate: `GENOLE=PASS OLEPIN=PASS REFUSE=PASS REGRESS=PASS LEGS=4/4 C1=PASS` rc 0
  (REGRESS: "r54 33 rows identical")
- R54SHIM: GENOLE FAIL `S901 span is not a slice of the defined form` · OLEPIN FAIL `S921 …`
  · REFUSE FAIL `NOFORM: rc=0` · REGRESS PASS → `LEGS=1/4` (claims: 1/4 REGRESS only ✓)
- TXTONLY: GENOLE FAIL `rc=1` · OLEPIN FAIL `rc=1` · REFUSE FAIL `SIDECAR: no refusal line
  for S942` (it refused the good row S941 when that run's pin lacked a sidecar) · REGRESS PASS → `LEGS=1/4` ✓
- DELEGATE: all legs `rc=97 AUDIT_FORBIDDEN ctypes.dlopen` → `LEGS=0/4` ✓

## Mutants (each = one minimal edit to the scratch counter, then all 4 tools, --seed 55)

| mutant (edit) | candidate | R54SHIM | TXTONLY | DELEGATE | verdict |
|---|---|---|---|---|---|
| NO_SLICE — `form[o:o+len(span)]!=span or len(span)<=len(quote)` → `False` (also drops the >quote-length clause) | 4/4 PASS | 1/4 (REGRESS; dies now at `S901/S921 char`) | 1/4 | 0/4 | SURVIVED — load is taken by the char check (redundant vs NO_CHAR) |
| NO_CHAR — `span.find(quote)<0 or o+span.find(quote)!=char` → `False` | 4/4 | 1/4 (dies at slice check) | 1/4 | 0/4 | SURVIVED — redundant vs slice check |
| NO_SHA — `cells[2] != sha256(fbytes)` → `False` | 4/4 | 1/4 (slice) | 1/4 | 0/4 | SURVIVED — untested clause |
| NO_QUOTE — `f"QUOTE {sid} char {char} {name}" not in out` → `False` | 4/4 | 1/4 (slice) | 1/4 | 0/4 | SURVIVED — untested clause |
| NO_EXTRA — `have != names` → `False` | 4/4 | 1/4 (slice) | 1/4 | 0/4 | SURVIVED — untested clause |
| REF_TSV — drop `if (run/"out"/"spans.tsv").exists(): return "spans.tsv written"` | 4/4 | 1/4 (`NOFORM: rc=0` earlier) | 1/4 | 0/4 | SURVIVED — untested clause |
| ALLOW_ROOT — hook `ALLOW = ("/",)` | 4/4 | 1/4 | 1/4 | 0/4 (still `ctypes.dlopen`) | SURVIVED — path arm untested; DELEGATE dies on the event list first |
| NO_ORACLE_SHA — drop `hashlib.sha256(CAPTURE_TEXT.read_bytes())…!= CAPTURE_TEXT_SHA` | 4/4 | 1/4 | 1/4 | 0/4 | SURVIVED — env-pin untested |
| WIN_NL — windows may contain `\n` | **1/4** (GENOLE `rc=2 … need 4 non-empty tab cells`; OLEPIN rc 2; REFUSE NOFORM rc 2; REGRESS PASS) | 1/4 (same rc 2) | 1/4 (parse traceback) | 0/4 | KILLED — the candidate itself collapses: quotes with newlines break quotes.tsv rows; the filter protects the harness's own TSV format |

All per-leg failure reasons were identical to pristine unless noted. No control ever gained a
leg under any mutant → 9/9 SURVIVED under the seat's definition (control-leg flip).

## Untested clauses (no shipped control exercises them — coverage findings, not contract changes)

1. `capture_sha256` cell vs digest of the file read (line 260).
2. `QUOTE <id> char <N> <span_file>` stdout line (line 274).
3. extra/missing span files set-equality (line 277).
4. refusal run writing `spans.tsv` (line 324) — controls fail earlier on `rc` or the refusal
   line; a tool that exits 1, prints `build-spans: refused <id>` AND writes spans.tsv is
   currently undetected (the sibling span-file check at line 326 is similarly untested).
5. hook path-allowlist arm: DELEGATE is denied by `ctypes.dlopen` before any path check —
   a subprocess-free `.txt`-sidecar reader or a soffice-via-`os.scandir`/open-outside-rundir
   shortcut would also be caught only by event arms (BAD tuple is exercised; the ALLOW path
   arm is not).
6. pinned-oracle sha256 and pinned-capture sha256-prefix env pins (lines 441, `pinned()`) —
   no control swaps the oracle; these guard the counter's own environment, not a shortcut.
7. slice-equality vs char-check redundancy: each alone still kills R54SHIM; the pair is a
   one-deep defence — a control writing correct slices but wrong `offset` (or vice versa)
   would probe one check at a time.
8. `len(span) <= len(quote)` (longer-than-quote) — dropped inside NO_SLICE, never exercised
   independently.

## Restoration evidence

```
sha256sum $S/lane/corpus/evidence/round55/c1-count.py $S/c1-pristine.py
→ 5506f240c53ff83c7c17b7252c7627871b4b1af7c1ca739b461fdbcc32048906  (both, identical)
git -C $S/lane status --porcelain | wc -l → 0
pgrep -u $USER -f soffice.bin | wc -l → 0;  pgrep -u $USER -f $S | wc -l → 0
```

Every mutant run was preceded and followed by a byte-restore of the pristine counter
(sha256 asserted after each of the 9 restores, all `5506f240…`). The real lane
`/home/vgpnk/Projects/shokunin/chousa-shokunin` was never modified; only this report was
written there. Tooling: no installs were needed (system python3, git, soffice present).

VERDICT: attacked the frozen C1 counter with 9 minimal mutants — all 9 survived (no control
gained a leg); slice and char checks proved redundant against each other; six clauses
(digest cell, QUOTE line, extra-file set, refusal-with-manifest, hook path allowlist, env
pins) are exercised by no shipped control; WIN_NL showed the windows filter guards the
counter's own TSV input format.
