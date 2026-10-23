# ExecD2Census — round-33 D2: round-32 C1 receipt tally

Verdict: **D2 is reproduced, and the number it prescribes is also short.** The counting command D2
asks for, run over committed round-32 receipts at the frozen tip (`3b528b9a926dd53001a1f1da5df6be1c63fca3ca`),
finds **21** C1 receipts binding gate `10f2fe12043c6f1565c7d7b9446ee0c4dc11e9649aa3350dcab96f8a2ccb4098`
— not 18 (report/SCORECARD) and not 20 (round-32 spot-check). All 21 are `APPEND_SERIALIZED=24/24`,
`predicate_holds=true`, counter `e6bf9531…`, `total=24`, 15 distinct seeds. The C1 verdict is
unchanged; only the count was wrong.

## Commands (cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`, GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset)

1. `git ls-files .ufo/waves/round-32 | grep -c json` → `1150`; suffix split: `1134` `.json`, `14`
   `.jsonl` (line-delimited manifests, skipped by name, never parsed as receipts).
2. `python3 .ufo/waves/round-33/w1/ExecD2Census/census.py --lane .` → exit 0. Full output saved at
   `.ufo/waves/round-33/w1/ExecD2Census/census.out` (6095 bytes). Line 5:
   `C1 receipts on gate 10f2fe12: 21`.
3. Independent check without the script (exit 0, 12.6 s):
   `git ls-files .ufo/waves/round-32 | grep '\.json$' | xargs -d '\n' -n 64 sh -c 'for f; do git show "HEAD:$f"; done' _ | jq -s 'map(select((.label? // "") | startswith("APPEND_SERIALIZED")) | select((.gate_sha256? // "") | startswith("10f2fe12"))) | length'`
   → `21`.
4. Same one-liner with `f4731885` → `3` (matches the SCORECARD row's `f4731885` ×3: `measure/final/c1-s3210{1,2}.json` and `w2/RerunC1b/rerunc1b-fs-tmpfs.json`).
5. Field check over the 21 → `{"n":21,"predicates":[true],"totals":[24],"counters":["e6bf9531"],"unique_seeds":15}`
   (the seven `w2/MutC1Gate` arms share seed 323200).

Census content is read from committed blobs (`HEAD:<path>` through one `git cat-file --batch`), so a
worktree edit cannot move a count; `git status --porcelain .ufo/waves/round-32` printed nothing, and
the census reports `0` index paths absent from HEAD. Of 1134 `.json` paths, 1107 parse to objects and
27 are JSON arrays (command logs, summary/case tables, `chronology`/census manifests) — none is a
malformed C1 receipt, so nothing receipt-shaped was dropped silently.

## The 21, by seat (purpose from each seat's report; utc from the receipt)

| seat | n | purpose | utc |
|---|---|---|---|
| `measure` | 2 | post-build C1 measurement, seeds 32001/32002 | 07:21:31Z, 07:23:15Z |
| `w2/MutC1Gate` | 7 | pristine + six restored gate arms, counter 24/24 each, seed 323200 | 07:29:01Z, 07:39:38Z ×2, 07:41:28Z ×2, 07:43:22Z ×2 |
| `w2/RerunC1a` | 3 | independent re-runs, seeds 44001–44003 | 07:29:29Z ×2, 07:31:20Z |
| `w2/RerunC1b` | 5 | lane-gate load pair (07:31:11Z ×2), landed-gate load pair (07:51:22Z ×2), landed gate on tmpfs (07:56:21Z) | 07:31:11Z–07:56:21Z |
| `w2/NoHarmAfter32` | 2 | post-repair no-harm C1, seeds 3301/3302 | 07:30:31Z, 07:33:15Z |
| `w2/CriticAxis32` | 1 | critic re-score, seed 32320001 | 07:30:02Z |
| `w2/CriticMistakes32` | 1 | critic re-score, seed 323212 | 07:30:17Z |

## Exactly which files separate 20 from 18

Sorted by receipt `utc`, the set crosses 18 at **07:43:22Z**, 20 at **07:51:22Z** and 21 at
**07:56:21Z** (`census.out`, "target gate 10f2fe12 in utc order"). So:

- **The 2 files that make 20 vs 18** (both `w2/RerunC1b`, both `2026-10-23T07:51:22Z`):
  `.ufo/waves/round-32/w2/RerunC1b/rerunc1b-landed-load1.json` (seed 11267997743373557187) and
  `…/rerunc1b-landed-load2.json` (seed 15995727672319425323). Purpose per
  `.ufo/waves/round-32/w2/RerunC1b.md:10-11`: the landed gate in a clone at `5d8a1707` under eight
  `timeout 300 yes` spinners, with a second counter run concurrently; both `24/24`.
- **The 21st** (one more than the spot-check's 20): `…/w2/RerunC1b/rerunc1b-landed-fs.json`
  (seed 16933628124814463246, `2026-10-23T07:56:21Z`), the landed gate with `C1_TMP=/dev/shm` tmpfs
  instead of the `/fast` xfs. It is the latest receipt on this gate.
- The two **critic re-scores** are not the delta: they sit at 07:30:02Z / 07:30:17Z, i.e. inside the
  18 as well. D2's sentence "the extra two are critic re-scores" therefore does not survive the
  timestamps; [INFERENCE] the ×18 was tallied from the receipt set as it stood between 07:43:22Z and
  07:51:22Z, and the spot-check's 20 from the set between 07:51:22Z and 07:56:21Z. I cannot observe
  when either tally ran, so that ordering is inferred from the utc cut points, not proven.

## Draft SCORECARD correction (append-only; not applied — lane files are not mine to write)

Full text at `.ufo/waves/round-33/w1/ExecD2Census/note-D2.md` (sha256 `024e1a08…768e73`). It states
the 21 count, the by-seat split, the `utc` cut points and both commands above, and says explicitly
that the C1 verdict does not move. Intended placement: a new `## Round-33 …` section appended to
`SCORECARD.md`; it names the round-32 C1 row by its claim text (the row at `SCORECARD.md:1817`),
never editing it.

## Limits

- Control rule respected: I ran **no** C1 counter and executed no gate; every read was `git show`/
  `git ls-files` on committed blobs plus `python3`/`jq` parsing. No candidate was scored.
- `jaq` is not installed on this host (`jaq: command not found`); the one-liner uses `jq`
  (`/home/vgpnk/.local/bin/jq`). The spot-check's census used `jaq`; if its filter differed in some
  detail I did not reproduce, the 20 could have another cause — the utc explanation is the only one
  I could make land exactly on 18/20/21.
- Counting labels: a C1 receipt is a top-level object whose `label` starts with `APPEND_SERIALIZED`.
  Receipts from mutant counters also carry that label (255 such receipts across 46 gate prefixes in
  round-32), so the gate prefix is part of the count, not just the label.
- No processes were started in the background; nothing outside
  `.ufo/waves/round-33/w1/ExecD2Census{,/}` was written.

## Files

| path | sha256 |
|---|---|
| `.ufo/waves/round-33/w1/ExecD2Census/census.py` (6003 B) | `fa6d963394075069dea2e9101feed202b47c1f8dab5ca89ce615383f83fc1cda` |
| `.ufo/waves/round-33/w1/ExecD2Census/census.out` (6095 B) | `3c1a965ef0fe7895778e3ab7ef3517a200614536de8ee11273828ad9e139c9d6` |
| `.ufo/waves/round-33/w1/ExecD2Census/census.err` (0 B) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `.ufo/waves/round-33/w1/ExecD2Census/note-D2.md` | `024e1a080c4b962f8cae1b54de485a1d998e202212bd47f888953e1c0f768e73` |
| this report | — |
