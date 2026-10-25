# R50ExecWaveCheckLive — filing-order checks, dry run (W2)

Leaf executor, chousa round 50 wave 2. Scope: run the three filing-order checks the lesson commits to
(QUALITY 75/78/76), record the exact W2 command + output the final report will carry, report any check
that misbehaves. No production file, index, jj state or `shokuknow` path written. No tool installed
(none expected; pacman paused host-wide — no transaction attempted).
## 1. W1 check — exactly the 13 misdirected seats

```
$ python3 corpus/evidence/round50/wave-complete-check.py .ufo/waves/round-50/w1-spec.json .ufo/waves/round-50/w1; echo "EXIT=$?"
MISSING MineConsider / ExecMirrorCensus / ExecInfStaged / ExecReplayC1 / ExecFormProbe / CritForgeC1 /
CritForgeC2 / ReviewProvince / ReviewQuarMap / CritTheme / ConnSiblings / ConnCrossClaim / ScoutCoverage
  (stdout was these 13 names, one `MISSING <name>` per line in this order; joined here for length)
OK 29/42 reports present in .ufo/waves/round-50/w1      [stderr]
EXIT=1
```

Set-identical to `name-collision-check.py:3-5` and `corpus/lessons/round-50.md:17` (Mistakes row 4);
29 + 13 = 42 = `w1-spec.json` items, all unique. It reproduces the misdirected set, not just a count.
## 2. W2 name-collision — 0, plus structural check

```
$ python3 corpus/evidence/round50/name-collision-check.py .ufo/waves/round-50/w2-spec.json; echo "EXIT=$?"
NAME_COLLISIONS=0 ITEMS=43
EXIT=0
```

Corroborated structurally (the check alone could pass vacuously): 43/43 names start `R50`, all unique,
`set(w1)&set(w2)==[]` — so the same-round cross-wave case it excludes by design is not live here.
## 3. Lesson decode-form — PASS

```
$ python3 corpus/evidence/round50/decode-form-check.py corpus/lessons/round-50.md; echo "EXIT=$?"
FORM_NAMED corpus/lessons/round-50.md
DECODE_FORM=PASS
EXIT=0
```
## 4. The W2 command the final report will carry

```
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round50/wave-complete-check.py \
  /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-50/w2-spec.json \
  /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-50/w2
```

Live snapshot — not a completion claim; the dir fills while seats write. Stdout is 39 `MISSING <name>`
lines in this order (wrapped here for length; at filing time paste them verbatim), then the stderr tally:

```
$ python3 corpus/evidence/round50/wave-complete-check.py .ufo/waves/round-50/w2-spec.json .ufo/waves/round-50/w2; echo "EXIT=$?"
MISSING R50ReopenRowS104 / R50ReopenRowS105 / R50ReopenRowS106 / R50CritEntryR40 / R50CritEntryR41 /
R50CritEntryR39 / R50CritGateDecisions / R50CritForgeC1 / R50CritForgeC2 / R50CritTheme /
R50CritErratum / R50CritAxisC1 / R50MutStaleCount / R50MutWaveComplete / R50MutCitedId /
R50MutLandedC2 / R50MutInferenceCJK / R50MutSelftestV2 / R50ReviewProvince / R50ReviewQuarMap /
R50ReviewQuality / R50ReviewGatesRows / R50ReviewLesson / R50ReviewProvenanceLines / R50ExecReplay /
R50ExecCensusMirror / R50ExecInfLanded / R50ExecNegativeSweeps / R50ExecFormProbe /
R50ExecPerturbAdopter / R50ExecWaveCheckLive / R50ScribeLogDraft / R50ScribeScorecardDraft /
R50ScribeReportDraft / R50ConnSiblings / R50ConnCrossClaim / R50ScoutCoverage / R50ScoutConsider /
R50SimplifyChecks
OK 4/43 reports present in .ufo/waves/round-50/w2      [stderr]
EXIT=1
```

Count at my start: **4/43** (`ls .ufo/waves/round-50/w2/*.md | wc -l` → 4: `R50ReopenQuotesS104/S105/S106.md`,
`R50ReopenRefusedBnu.md`). Re-run 22:17:23Z: **9/43**, exit 1. Snapshot only; the final report must re-run
and paste its own. This seat was MISSING at snapshot time and is counted from disk as soon as this file is
written — which is exactly why the filing-time run should use `--rev <tip> --lane
/home/vgpnk/Projects/shokunin/chousa-shokunin`: disk mode counts uncommitted drafts. Verified in a
`/dev/shm` fixture (`rev-parse --show-toplevel` == fixture before commit): commit with only `Alpha.md` →
`MISSING Beta` / exit 1; next commit → `OK 2/2`, exit 0. The tally goes to **stderr**.
## 5. Check that misbehaves — `decode-form-check.py` is vacuous

Docstring 6-9 says `FORM_NAMED` means the text names a form ("`.txt` read as UTF-8, `utf-8-sig`, or
`.raw` decoded as UTF-16LE"). The regex (line 19) adds an undocumented bare `decode form` alternative, so
a table header alone passes:

```
$ python3 corpus/evidence/round50/decode-form-check.py header.md; echo "EXIT=$?"
FORM_NAMED header.md          # '| id | decode form | quote |' + '| S1 | | x (char 549) |'
DECODE_FORM=PASS
EXIT=0
$ python3 corpus/evidence/round50/decode-form-check.py header2.md; echo "EXIT=$?"   # same, header 'form'
FORM_MISSING header2.md
DECODE_FORM=FAIL
EXIT=1
```

Decisive: copy of `corpus/lessons/round-50.md` with `utf-8-sig`, `UTF-8`, `UTF-16LE`, `.txt`, `.raw` all
replaced, header kept → `FORM_NAMED stripped.md` / `DECODE_FORM=PASS` / `EXIT=0`. `round-50.md` carries
`decode form` three times (lines 8, 30, 45 header), so its PASS is not evidence for QUALITY 76. The
lesson's substance holds — lines 47-49 name `.txt` UTF-8 for S104/S105/S106 — but the gate does not
establish it. Fix (not applied, outside my write): drop the bare alternative or require it near a real
form token. Secondary: a missing path raises uncaught `FileNotFoundError`, exit 1, vs documented 2.
## 6. Named limits of the other two (not defects; no live exposure)
- `wave-complete-check.py` is existence-only: `: > Alpha.md` → `OK 2/2`, exit 0, so WAVE-DONE on this
  check alone is satisfiable by a 0-byte file; w1 is unaffected (smallest report 6073 bytes). `sub/Alpha.md`
  is not counted → `MISSING Alpha`, exit 1 (by design). A duplicated spec name collapses silently
  (`OK 1/1` for a 2-item duplicate spec). Guards hold: empty `items`, missing spec, dir outside lane,
  bogus rev, one positional arg → all exit 2.
- `name-collision-check.py` globs `round-*/*/*.md`, one level only: `round-49/w1/sub/DeepSeat.md` →
  `NAME_COLLISIONS=0`, exit 0 — nested reports evade it. Attribution nit: `setdefault` on a sorted glob
  keeps the earliest round, so `ExecMirrorCensus` prints `round-47/w1/...` while `w1-results.json` records
  that seat returning `round-49/w1/...` (both exist) — detection right, pointer names a round that is not
  the one that caused the misdirection, against `round-50.md:17`'s "13 seat names of round 49". Guards
  hold (no `reportDir`/`--round` → 2; item without `name` → 2). Positive control: `w1-spec.json` → 13
  `NAME_COLLISION`, `ITEMS=42`, exit 1.
## 7. Cross-seat flag received and retracted
`R50ReopenRowS105` flagged a uniform spans.tsv S105 offset shift (−80 tail, −48 head), then retracted it:
`offset` is the span-block start, not the quote position. Mechanism confirmed at source —
`corpus/evidence/round50/build-spans.py` docstring ("`offset` is the span's start", "80 chars of captured
context either side", "N = offset + the quote's position in its span"), `CONTEXT = 80`, `start = max(0, off
- CONTEXT)`. Designed window, not drift; row S105 survived. Not re-derived per row by me (spans attack is
the row seats' / `R50ExecReplay`'s). Residual: the bare `offset` header is ambiguous against `char N`.
Scratch `/dev/shm/chousa-r50-R50ExecWaveCheckLive/` and the git fixture (`mktemp -d -p /dev/shm`) deleted;
no lane file other than this report written.
VERDICT: attacked the three filing-order checks — W1 prints exactly the 13 misdirected seats (exit 1),
W2 collision is 0/43 with all names R50-prefixed and disjoint from W1, and both reproduce their known-bad
positive controls; defect found in `decode-form-check.py`: an undocumented bare `decode form` alternative
makes it print `DECODE_FORM=PASS` on a header-only table and on the real lesson with every form name
stripped, so the lesson's QUALITY 76 pass is vacuous.
