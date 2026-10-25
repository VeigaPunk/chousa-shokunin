# DraftMistake — round 49 wave 1: Mistakes rows for round-49 lesson

Seat: DraftMistake (leaf; no subagents). Date: 2026-10-25. Lane: chousa-shokunin.
Scope: draft the `## Mistakes` row(s) for `corpus/lessons/round-49.md` (file does not
exist yet; rows are drafted here for L1 to compose). Required mistake mined: the
round-47 held-out label a05 accepted as 'correctly reasoned' by the round-47 non-author
closure and propagated as 'exit-level 3/12 incl. a05' into the round-48 lesson S095 Gate
block; the round-48 closure ruled it false.

## Drafted row (copy-ready for round-49.md)

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| Held-out label adopted on a charitable reading and propagated uncorrected (a05) | `.ufo/waves/round-47/w2/HeldOutA.md:24,34` (source classification) → accepted at `corpus/lessons/round-47-verifier-spotcheck.md:29` ("exit-level 3/12 incl. a05, an over-refusal") → quoted verbatim into `corpus/lessons/round-48.md:34` (S095 Gate block); falsified by `.ufo/waves/round-48/w2/AttackPrecision.md:47,50` and `corpus/lessons/round-48-verifier-spotcheck.md:43,46` (ruling (a): the a05 "correctly-reasoned" label is FALSE on the plain reading; the true false-refusal count is 2/12 (p03, p04)) | None — the r48 closure itself names the acceptance "an error of charity" (`round-48-verifier-spotcheck.md:43`); QUALITY 69 (`corpus/QUALITY.md:689-703`) requires recording false-refusal cue/window classes but no criterion audits a held-out label against the phrase it quotes (charity is not evidence) | Append-only correction entry (round-49 lesson and/or `round-47-verifier-spotcheck.md`) superseding "exit-level 3/12 incl. a05" with "true figure 2/12 (p03, p04); a05's refusal was correct", and sweep the two live propagation sites (`round-47-verifier-spotcheck.md:29`, `round-48.md:34`). SCORECARD.md:2545 already carries the dispute ("re-open a05 in closure") and needs no change. Check shown able to fail: any a05/3/12 propagation in a lessons file must be co-located with the correction in the same file — fails today (exit 1) on `round-47-verifier-spotcheck.md:29` and `round-48.md:34`, passes (exit 0) after append-only corrections |

## Evidence (reads; file:line)

- `round-47-verifier-spotcheck.md:29` — the r47 non-author closure ruling: "`HeldOutA`
  refuses 2/12 correctly-reasoned bullets (exit-level 3/12 incl. a05, an over-refusal of
  a common construction) vs 0 before". This is the acceptance and the propagation source.
- `HeldOutA.md:12` — headline "refusals **2/12** (p03, p04); every other bullet PASS";
  `:24` table lists `a05 … exit=1` (a third refusal); `:34` labels a05 "an over-refusal
  of a common natural construction" via the "second date" scope defense. Internal
  headline/table contradiction noted by `AttackPrecision.md:54`.
- `AttackPrecision.md:47` — a05 row: "**disputed, defensible only narrowly**: … Read
  plainly — `that date` = the archived copy's date … the bullet *does* deny the affirmed
  phrase, making the label wrong"; `:50` "a05's correctness holds only on the charitable
  reading".
- `round-48.md:34` — S095 Gate block quotes line 29 verbatim ("exit-level 3/12 incl.
  a05, an over-refusal"); `round-48.md:71` — the same lesson records "W2
  `AttackPrecision.md` disputes `a05` … the closure must independently adjudicate it".
- `round-48-verifier-spotcheck.md:41,43,46` — ruling (a): "the a05 'correctly-reasoned'
  label is FALSE on the plain reading, and the r47 non-author closure's acceptance of it
  was an error of charity"; "true false-refusal count … is **2/12 (p03, p04)** …
  the propagated 'exit-level 3/12 incl. a05' figure … overcounts the defect class by
  one"; `:65` — S095 row "admissible, … **but** quote 1 propagates the a05 mislabel —
  the row itself is admissible, the quoted figure is not".
- `corpus/QUALITY.md:689-703` — criterion 69: records false refusals and cue/window
  classes; no plain-reading label audit rule. `SCORECARD.md:2545` — carries the dispute
  and defers, so no sweep needed there.

Captured-by: **none** — the mislabel survived every existing rule until the r48 closure
ruled it; the r48 lesson's S095 quote is verbatim-accurate, so quote fidelity rules did
not (and cannot) catch a quote whose *content* is a false claim. The fix is append-only;
no predicate, target, counter, or control is touched.

## Fix shown able to fail

Check (proposed rule): scan `corpus/lessons/*.md`; any line propagating the uncorrected
figure — regex `(?i)(?:3/12[^\n]*a05|a05[^\n]*3/12)` — must be co-located in the same
file with the correction — `a05` + `2/12` + a correction marker (overcounts / "refusal
is correct" / "label is FALSE" / "error of charity" / superseded / plain reading). Ran
against current files:

```
$ python3 - <<'PY'   # (check body: prop/corr/mark regexes as above over corpus/lessons/*.md)
FAIL round-47-verifier-spotcheck.md: propagation lines [29] without correction lines []
FAIL round-48.md: propagation lines [34] without correction lines []
exit=1
```

So the check fails on the r47/r48 text. Append-only corrections (copies in scratch
`/tmp/chousa-r49-DraftMistake/` + a named correction entry each) then:

```
PASS over 2 files: all a05/3/12 propagations carry a correction
exit=0
```

The correction entries are: r47 spotcheck — "Line 29's 'exit-level 3/12 incl. a05…
an over-refusal' is superseded by the round-48 closure ruling (a) …: the a05
'correctly-reasoned' label is FALSE on the plain reading; the true false-refusal count is
2/12 (p03, p04); a05's refusal was correct. The over-refusal figure overcounts the
defect class by one." r48 lesson — "The S095 Gate quote at line 34 carries the r47
figure 'exit-level 3/12 incl. a05', which the round-48 closure ruled FALSE …; true figure
2/12 (p03, p04), a05's refusal was correct. The row stands; the quoted figure does not."
Both are pure appends; they are the fix the row proposes.

Tooling: read `~/.omp/agent/RULES.md` (channels, pacman pause). No install or update was
made or needed (no tooling change for a drafting seat). No network/live fetch: L0
`8d77e6c1` open — all reads were on-disk lane files. Scratch `/tmp/chousa-r49-DraftMistake/`
created and deleted before finishing. The only write: this report file. Out-of-scope:
C1 adopter / C2 counter (sibling seats), claim gate, any production edit, git/jj state.

VERDICT: drafted the round-49 Mistakes row for the a05 mislabel propagation (accepted on
charity at r47 spotcheck:29, quoted into r48 S095 at r48.md:34, ruled false by r48
closure) with an append-only fix whose check fails on the current text (exit 1) and
passes after the append-only correction (exit 0).
