## Round-33 D2 correction — round-32 C1 receipt tally (append-only)

The round-32 C1 row above and `corpus/lessons/round-32.md:92` state "committed receipts on landed
gates: `10f2fe12` ×18 … all 24/24". Counted on the frozen round-32 tree, gate
`10f2fe12043c6f1565c7d7b9446ee0c4dc11e9649aa3350dcab96f8a2ccb4098` carries **21** C1 receipts
(top-level `label` beginning `APPEND_SERIALIZED`), every one `24/24`, `predicate_holds=true`,
counter `e6bf9531…`, 15 distinct seeds (the seven `w2/MutC1Gate` arms share seed 323200). The C1
verdict does not move; the count was wrong.

By seat: `measure` 2, `w2/MutC1Gate` 7, `w2/RerunC1a` 3, `w2/RerunC1b` 5, `w2/NoHarmAfter32` 2,
`w2/CriticAxis32` 1, `w2/CriticMistakes32` 1.

Why 18 and 20 were both printed, in receipt `utc` order: the set reaches 18 at `07:43:22Z`, 20 at
`07:51:22Z`, 21 at `07:56:21Z` (2026-10-23). The two files separating 20 from 18 are
`w2/RerunC1b/rerunc1b-landed-load1.json` and `w2/RerunC1b/rerunc1b-landed-load2.json` (both
`07:51:22Z`: landed gate under eight `yes` spinners, two concurrent counters); the 21st is
`w2/RerunC1b/rerunc1b-landed-fs.json` (`07:56:21Z`: landed gate with `C1_TMP` on tmpfs). The two
critic re-scores (`w2/CriticAxis32/candidate-c1-s32320001.json` `07:30:02Z`,
`w2/CriticMistakes32/candidate-c1-v2-s323212.json` `07:30:17Z`) sit inside the earlier 18 as well,
so D2's attribution "the extra two are critic re-scores" does not survive the timestamps.

Commands (lane root, both exit 0, run 2026-10-23):

1. `python3 .ufo/waves/round-33/w1/ExecD2Census/census.py --lane .` → line 5 prints
   `C1 receipts on gate 10f2fe12: 21`; the tool lists every counted path grouped by
   `(gate_sha256, counter_sha256, seat)` and again in `utc` order (saved:
   `.ufo/waves/round-33/w1/ExecD2Census/census.out`).
2. Without the script:
   `git ls-files .ufo/waves/round-32 | grep '\.json$' | xargs -d '\n' -n 64 sh -c 'for f; do git show "HEAD:$f"; done' _ | jq -s 'map(select((.label? // "") | startswith("APPEND_SERIALIZED")) | select((.gate_sha256? // "") | startswith("10f2fe12"))) | length'`
   → `21`.

The same command with `f4731885` instead of `10f2fe12` → `3`, matching the row's `f4731885` ×3.
No counter was run and no gate executed for this census: only committed blobs were read.
