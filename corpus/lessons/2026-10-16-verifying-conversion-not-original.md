# Round-9 lesson — verifying a conversion is not verifying the original: a composed CLEAN certifies the record's fidelity to chosen spans of the archive bytes, and the chain of custody stops at the export (2026-10-16 UTC)

Round: chousa-shokunin round 9, one coverage move — the three read-only
archived inputs under `research/deep-research-2026-09-28/` exist as gate-format
records under `corpus/fixtures/archives-r9/` (`A-r9.md`, `B-r9.md`, `C-r9.md`),
each run end-to-end through `verify-all`, with
`corpus/fixtures/claims-r9.jsonl` adding 10 claims beyond round 2's 17.
Fixture-led by design: no gate file changed (working-tree sha256 equals the
HEAD `f11073a` blob; `git diff --numstat tools/research-gate.sh` EMPTY,
re-derived at measurement time).

Source seat: lessons-distiller. Gate under measurement:
`tools/research-gate.sh` sha256
`46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd`
(selftest 85, the round-8 revision). Read-only sources, sha256 re-derived and
unchanged from the r2 pins: `9033857d…` A-shokunin-tradition.md (110 lines,
109 NL), `6d8dbddd…` B-multiagent-knowledge.md (101/100), `e48fe70f…`
C-rank-taxonomy.md (155/154). Fixture shas at measurement (2026-10-16
04:36–04:39Z): A-r9.md `338918fc…`, B-r9.md `abfa5290…`, C-r9.md
`97be0e69…`, archives-r9/README.md `ec312657…`, claims-r9.jsonl
`f6f0d1ab…`, claims-r9.README.md `64b63db6…`. verified-at: 2026-10-16
04:30–04:39Z, from the lane cwd, fresh-process CLI runs; scratch under
`$HOME/.cache/chousa-tmp/r9-lessons/` (per-user /tmp quota).
recheck (from the lane cwd):
`bash tools/research-gate.sh verify-all corpus/fixtures/archives-r9/A-r9.md --root ..`
(and `B-r9`/`C-r9`) ·
`bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r9.jsonl --root ..`.

## The lesson

A gate-format RECORD converted from a raw source is itself a derived artifact,
and a composed CLEAN binds exactly one hop: record → the source bytes actually
quoted. The verdict does not travel to the source as a whole, and it cannot
reach the sources the source itself cites. Six measurements from this round:

1. **Same bytes, two verdicts; the delta is the conversion.** Run raw through
   the structure mode, each archive exits 1 with exactly one
   `RESEARCH_GATE: DRIFT` summary — findings `RECORD_SCHEMA_INVALID`,
   `EXPORT_CHROME_PRESENT`, `NO_QUESTION`, `SOURCE_TABLE_ABSENT`,
   `CLAIM_TABLE_ABSENT`, `REJECTION_DROPPED` (`findings=6 drift=5`);
   `verify-all` on each raw archive composes
   `sections=5 run=2 absent=3 drift-sections=1 findings=6 drift=5`, exit 1.
   The converted records compose
   `sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0`, CLEAN
   exit 0, each (all re-measured). "CLEAN" is therefore a property of the
   conversion and its span selection, not of the bytes alone; the raw-DRIFT
   run is the control that must travel with any conversion-CLEAN report.
2. **The conversion authors what the source cannot supply.** The archives
   contain zero Markdown headings and zero pipe-table lines (`grep -c '^#'`
   = 0, `grep -c '^|'` = 0, all three); each record carries 9 headings and
   44/45/48 table rows. Every section, table row, tier and ranking is
   authored; against a headingless source the chain anchor kinds available
   are `quote`/`line` only — a `heading` anchor matches `^#+ ` heading lines
   (`research-gate.sh:1225-1233`) and can never resolve in an export.
3. **The chain of custody terminates at the export.** The archives contain
   zero `http` strings; citations render as flattened chips — `コトバンク`
   (A:68, A:72, C:82, C:121, C:131), `adachi-hanga.com` (A:83), `arxiv.org`
   (B:51, B:72), `jstage.jst.go.jp` (C:103) — with bare `+N` counter lines
   (A:69 `+3`, A:84 `+2`, B:73 `+6`, C:83 `+5`, C:122 `+4`). The archive's
   own sources are un-nameable from the bytes and un-fetchable by policy
   ("No original external source was fetched and none may be",
   `corpus/README.md`); each record keeps its chip as one marked
   `blocked-no-fetch` hop (A hop 7, B hop 7, C hop 8; exempt-but-counted, so
   `RESOLVED_HOPS=6/7`, `6/7`, `7/8`). No CLEAN on these records can say
   anything about the archive's cited sources; the fixture README states it
   in its own words ("not the external truth of anything the archives cite").
4. **Coverage is a selection, and it must be carried with the verdict.** The
   gate-checked claim surfaces are 27 claims (r2's 17 + claims-r9's 10);
   their spans touch 23 distinct source lines (A 10, B 7, C 6). Adding the
   19 in-record, byte-checked `span` cells, the union is 31 distinct lines —
   against 109 prose lines in the three conversation regions (non-blank
   conversation lines excluding the in-conversation UI markers; 366 lines
   total across the three exports). A CLEAN claims run speaks for those
   spans: roughly one prose line in five is under a check. The fixture README
   prints its own selection accounting (46 claim rows total; 29 new this
   round) and names the residual distortion: "`text` cells paraphrase; only
   `span` cells and chain anchors are verbatim".
5. **Even the conversion's own row anchors are only partially checked.** A
   probe record whose `## Claims` row pointer cites
   `research/deep-research-2026-09-28/A-shokunin-tradition.md:99999` (a line
   that does not exist) closes structure CLEAN (exit 0) and composes
   all-sections CLEAN (`sections=5 run=5 drift=0`): structure mode checks the
   pointer's file existence only (`check_pointer` `research-gate.sh:506-537`
   → `ptr_resolves_meta` `:486-504` → `ptr_file_part` strips at the first
   `:` `:454-457`), and the claims mode reads only `id/source/span/expect`
   from the JSONL (`verify_claims` `:1009`), never the record's rows. Nothing
   compares a row's `path:line` with the span's actual occurrence line. The
   same class occurred inside the round's own artifact:
   `corpus/fixtures/archives-r9/A-r9.md:50` (row C3) declares
   `A-shokunin-tradition.md:76` while its `span` occurs at line 86 (see
   Defects); the composed verdict stays CLEAN because no mode compares them.
6. **Derived structure adds claims the source never made, and cuts remove
   answers.** The `## Sources` ranking, `## Rejections` and hop notes are
   authored; the exports are fragments (A's answer reaches only its first
   numbered section, A:74; B's only its first `(1)` section, B:77; the
   remaining sections never appear in the bytes), so a record structures what
   survived the cut. The fixture README names exactly this: "an absent
   section in an archive is not an answer of \"no\"".

## Cross-checks (what held)

- My independent `verify-all` runs reproduce the README's recorded composed
  tallies exactly, on the same gate and record shas. A: claims
  `VERDICT_BEARING_CLAIMS=10/10` · chain `6/7` · sweeps
  `VERIFIED_SWEEPS=1/1 REJECTIONS_OK=4/4` · integrity
  `refs=13 resolved=12 unresolved=0`; B: `10/10` · `6/7` · `1/1 3/3` ·
  `14/13/0`; C: `10/10` · `7/8` · `1/1 4/4` · `15/14/0`; every record
  `VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0` CLEAN exit 0.
  (The single exempt integrity reference per record is the `from` token of
  the `blocked-no-fetch` chain row, counted but not required to resolve.)
- `verify-claims corpus/fixtures/claims-r9.jsonl` →
  `VERDICT_BEARING_CLAIMS=10/10` (supported 7, contradicted 2, unsupported 1)
  CLEAN exit 0; my gate-free substring check agrees (9/10 occurrences — C07
  is the by-design unsupported probe, whose "longest token (`generic`) still
  points at the real C:133 sentence"), and the r9-vs-r2 span containment
  cross-product is empty (re-derived).
- Row-anchor audit of the three records (gate-free): 18 of 19 rows' pointer
  lines match their span's actual occurrence; the single miss is A row C3
  (§5).
- The older surfaces held at the same gate: r1 observable
  `VERDICT_BEARING_EXPORTS=3/3`; r2 claims `17/17` CLEAN; r3 chain
  `RESOLVED_HOPS=17/22` CLEAN.
- Inter-archive hops are convergences, not citations: `grep -cE
  "deep-research|archive [ABC]|export [ABC]|A-shokunin|B-multiagent|C-rank"`
  returns 0 in each archive (re-run), and each hop note says so; the gate
  verifies the anchor exists in the target archive — which is exactly what a
  convergence check can establish and no more.

## Applying it (durable rules)

1. State the terminus beside the verdict: "record → archive, N spans"; never
   "the archive is verified". Ship the raw-DRIFT control next to the
   conversion-CLEAN.
2. Report coverage as spans-over-lines (`k distinct source lines of M prose
   lines`), not as an adjective; omitted content is unverified by
   construction, and a fragment's silence is not an answer.
3. Before anchoring into a source, record which anchor kinds that source can
   support (heading anchors need headings; an export supports `quote`/`line`).
4. Selection is the conversion's unchecked act: the gate verifies that chosen
   spans occur, never that the choice was right or complete. The conversion
   README is the only carrier of that statement — check it says what it
   selected and what it left.
5. Pair row-level `path:line` anchors with span-level companions, and
   re-derive row lines from source bytes by an independent pass — the gate
   will not (probe and `A-r9.md:50` are the measured reasons).
6. Keep derived artifacts at their true tier (`export`, never promoted) and
   keep their own citations as marked, unopened hops; a clean conversion must
   not launder the source's provenance.

## Defects and follow-ups (outside this seat's write scope)

- `corpus/fixtures/archives-r9/A-r9.md:50` (row C3, pointer cell) —
  `research/deep-research-2026-09-28/A-shokunin-tradition.md:76` while the
  row's `span` cell occurs at line 86 (byte-identical, single line);
  `claims-r9.jsonl` A11 and `claims-r9.README.md`'s provenance table both pin
  A:86, and A-r9.md's own chain hop 3 note (line 38) says "A:86 close". The
  composed verdict is CLEAN because no mode compares the two. Fix or absorb
  at the fixtures seat; if A-r9.md is revised, its sha row in
  `archives-r9/README.md` (and this note's pins) must move with it.
- The dispatch text says "verify-all is CLEAN on each (modulo documented
  integrity findings)"; the measured state is simpler — zero integrity
  findings surfaced on any record (README: "no integrity findings surfaced,
  so none needed documenting").
- `claims-r9.README.md` §Record binding records the binding at 04:35Z; my
  re-runs at 04:37–04:39Z reproduce its tallies at the same record shas. Any
  later edit to a record invalidates both measurement rows.

## Limits of this note

- One host, one gate revision (`46f5ddb3…`, selftest 85), fixture shas as
  listed in the preamble; all CLI runs were read-only lane/local opens; no
  network.
- Re-derived this round: the raw-DRIFT control on all three archives, raw
  `verify-all` drift on all three archives, the three composed runs, the claims run, the
  gate-free span byte-check and containment cross-product, the 19-row pointer
  audit, the coverage union, the convergence grep, and the gate blob-vs-HEAD
  identity. Not re-derived: a `--selftest` run (outside this seat), the sweep
  glob internals beyond the gate's own re-run, and chain-miss controls (no
  defect drove one).
- The row audit is a gate-free script of this seat
  (`$HOME/.cache/chousa-tmp/r9-lessons/audit-rows2.py`); it compares the first
  raw-substring occurrence, which for these spans is unique in their sources
  — a multi-occurrence span would need a different comparison. The probe
  record for §5 lives at `$HOME/.cache/chousa-tmp/r9-lessons/fx/lineblind.md`
  (scratch, ephemeral by design).
- Coverage union counts distinct lines by first occurrence; spans can span
  several lines and lines can carry several spans, so it is a proxy (floor on
  touched lines), not a measure of verified meaning.
- No scalar score, no verdict about the round's admission.