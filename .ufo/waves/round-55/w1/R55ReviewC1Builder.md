# R55ReviewC1Builder — C1 builder review

Axes: operability, depth, calibration. Scope: candidate builder and the nine requested edge probes. Claims remain frozen; this report records findings only.

## Code review

Compared `corpus/evidence/round54/build-spans.py` at `25abbe82` with candidate `tools/build-spans.py` at `6ca924995d48facbf704d2aa22ddaec236059039` using:

```text
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff 25abbe82:corpus/evidence/round54/build-spans.py 6ca924995d48facbf704d2aa22ddaec236059039:tools/build-spans.py
```

Diff shows removal of round-54 `.txt`-first/UTF-16LE `.raw` fallback and embedded DOCX parser; candidate instead calls `capture-text.py` for OLE/zip and selects `.txt` only otherwise. CLI changed from fixed round directory/`--root` to required `--quotes`/`--out`. Candidate validates one URL per S### and rejects absolute/`..` entry paths. It normalizes CRLF and bare CR to LF before writing spans; round-54 specially clipped raw spans around CR.

## Probe results

Copied candidate and `capture-text.py` into `/fast/scratch/hyaku/chousa-r55/R55ReviewC1Builder`; isolated cache and output directories used. Each result is exit code plus captured stdout/stderr:

```text
empty exit 1 stdout '' stderr "build-spans: refused S124: quote occurs 0x in 11b99d11909aeb5094640dbe.txt: 'x'\n"
bom exit 0 stdout 'QUOTE S124 char 1 spans/S124-1.txt\nSPANS_ROWS=1 WRITTEN=1\n' stderr ''
eol exit 0 stdout 'QUOTE S124 char 2 spans/S124-1.txt\nSPANS_ROWS=1 WRITTEN=1\n' stderr ''
tab exit 2 stdout '' stderr 'build-spans: /fast/scratch/hyaku/chousa-r55/R55ReviewC1Builder/tab.tsv line 2: need 4 non-empty tab cells, got 5\n'
xlsx exit 1 stdout '' stderr 'build-spans: refused S124: capture-text refused 7f58f470f62c54e79125f514.raw: no _rels/.rels in the package\n'
ole-sidecar exit 1 stdout '' stderr 'build-spans: refused S124: capture-text refused a4d0fd6bd8b502033ebf3d71.raw: ole-malformed: short or unsigned header\n'
stale exit 1 stdout 'SPANS_HEADER_STALE\nSPANS_ROW_STALE spans/S124-1.txt\nSPANS_ROWS=1 STALE=2\n' stderr ''
two-url exit 2 stdout '' stderr 'build-spans: /fast/scratch/hyaku/chousa-r55/R55ReviewC1Builder/two-url.tsv line 3: S124 names utwo, earlier rows name uone\n'
dotdot exit 2 stdout '' stderr "build-spans: /fast/scratch/hyaku/chousa-r55/R55ReviewC1Builder/dotdot.tsv line 2: entry '../x.md' must be lane-relative\n'
```

Probe driver created empty txt, BOM-prefixed `x`, `a\r\nq\rb`, tab-containing quote `a\tb`, a zip with no Word relationship, malformed OLE-signature raw with sidecar `x`, stale output manifest, differing URLs for S124, and `../x.md` entry. Empty text refuses the absent quote; BOM is retained (quote starts at char 1); CRLF and lone CR normalize successfully; literal tab quote is unrepresentable in the row TSV and rejected as 5 cells; non-Word zip and malformed OLE refuse without sidecar fallback; stale manifest is detected; conflicting URL and parent traversal are rejected. The malformed OLE probe is a refusal-path test, not a valid OLE document test.

## Docstring versus code

Docstring lines are `tools/build-spans.py:2-30`; implementation lines cited below:

- “Text form … `<key>.raw` is an OLE … or a zip …” and capture-text stdout; `.txt` sidecar never used; refusal — implemented by magic checks and `Forms.get` (`:67-90`).
- “otherwise `<key>.txt`, read as UTF-8 (errors replaced) with universal newlines” — implemented by decode replacement and CR normalization (`:85-88`).
- “neither: a refused row” — implemented (`:89-90`, `:131-153`).
- Digest of file read — raw digest from bytes (`:80-82`); txt digest from bytes (`:86-88`).
- Quote exactly once — `count` check (`:135-138`).
- Span exact formula and `<id>-<n>` — formula and input-order count (`:139-149`); files and manifest are UTF-8 bytes (`:206-208`).
- Input/output schema — parser and constants (`:44-45`, `:95-124`, `:186-192`).
- Refusal prints stderr, writes nothing, exits 1 — build refuses before `main` write phase (`:151-153`, `:198-206`).
- Prints QUOTE and N — emitted using `off` and cells (`:209-212`).
- `--check` re-derives/comparisons, writes nothing and prints summary — `:198-200`, `:157-183`.
- Usage / exit code claims — parser arguments `:186-192`; returns 2 for missing cache/input/header and 1 refusal/stale (`:96-123`, `:193-200`, `:183`).

**Concrete documentation mismatch:** docstring says span is `form[max(0, off-80) : off+len(quote)+80]` (`:15-17`), while `.txt` form is first normalized CRLF/bare CR to LF (`:87-88`). This is internally consistent with the docstring’s universal-newline form. No observed contradiction in the executed probes. Caveat: `read_quotes` uses `splitlines()` and tab-splitting, so quote text containing literal tabs cannot be represented; this is a TSV format limitation, not an unexplained successful quote.

## Residual risk / verification gaps

No valid OLE `.doc` or valid `.xlsx` was constructed in this bounded probe, so these results do not establish behavior on either. In particular the requested OLE `.doc` with a sidecar quote once was tested only with malformed OLE bytes; observed refusal shows no fallback for that malformed signature, not for a valid OLE file. No C1 counter was run here. Scratch removal was registered with an EXIT trap; subsequent cleanup command observed `scratch_exists=yes` (the probe shell was still running/exit cleanup had not yet been observed), so cleanup remains unverified.

VERDICT: Built first falsifiers of the C1 candidate's edge behavior; all exercised probes returned the expected refusal/success classes, with valid OLE-sidecar behavior and counter scoring not established.