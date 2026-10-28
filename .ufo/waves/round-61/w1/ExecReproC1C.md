# ExecReproC1C — independent C1 measurement (round 61, w1)

Claims file sha256 verified: 9afec8d493f0ba511a256f38cd5098ff508f9ed311c6c49ff5383add9ce0acec (matches the assignment).
Counter: corpus/evidence/round61/c1-count.py, unmodified. Builders: tools/build-spans.py (sha256 1ed2650a…c80bf6 printed by the counter, equals the claims "before" digest) and controls/ref-build-spans.py.
Every run: `python3 -B <c1-count.py> --builder <B> --work /fast/scratch/hyaku/chousa-r61/ExecReproC1C/w_<tag> --seed <N>` with TMPDIR=/fast/scratch/hyaku/chousa-r61/ExecReproC1C, fresh --work each. Host: 32 cores. Each run took ~1–3 s wall (first 13.16 s).

## Findings

1. Base builder: 7/20, exit 1, at all four seeds, in every run (2 unloaded runs per seed, plus 1 loaded run at 7107 and 7108). Failing legs, identical every time (13): P03, H07, H08, H09, H10, H11, H12, H13, H14, H15, H16, H17, H20. Passing 7: P01, P02, P04, P05, P06, H18, H19. This matches the claims' "before" receipt (7/20; P03, H07–H17, H20 fail).
2. Reference builder: 20/20, exit 0, at all four seeds, in every run including both loaded runs.
3. No leg changed verdict between runs of the same seed, for either builder. Same-seed groups checked (script comparing pass/fail per leg across runs):
   - base 7107: unloaded, unloaded repeat, 2-core load. No flips.
   - base 7108: unloaded, unloaded repeat, 32-process load. No flips.
   - base 7109 and 7110: two unloaded runs each. No flips.
   - ref 7107 (including the 2-core load run), ref 7108 (including the 32-process load run), ref 7109 and 7110: no flips.
4. Load sensitivity (RSS/timeouts): the verdicts did not move, but peak RSS did.
   - Observed RSS ranges across all runs (KiB), threshold in brackets:

     | Builder | H14 BIGTXT | H15 BIGRAW | H20 BIGFORM |
     |---|---|---|---|
     | base | 411844–609196 | 413940–415260 | 220336–292752 |
     | ref | 19432–20624 | 19764–20936 | 219624–293680 |

     H14 and H15 print `limit=98304`; for H20 the log prints no limit, so I did not check one.
   - The ref passes the H14/H15 limit by about 5x and the base fails it by about 4–6x, so these RSS legs are not near their threshold.
   - H20 RSS on ref varies 219–294 MB between runs; its pass verdict was stable. [INFERENCE] The H20 pass/fail threshold is not printed in the log, and I did not read the counter source to confirm how it is judged. The 220→293 MB spread is the one place where run-to-run noise is visible, but it did not flip any verdict in 12 runs.
   - No timeout leg flipped under the 2-core or 32-process load.
5. Extra beyond the item: I added a heavier load (32 busy processes on a 32-core host) for seed 7108 on both builders, besides the requested 2-core load on 7107. No change in LEGS or in which legs failed.

## Runs (LEGS, exit code)

| Tag | Builder | Seed | Load | LEGS | Exit | Failing legs |
|---|---|---|---|---|---|---|
| base-7107 | base | 7107 | none | 7/20 | 1 | the 13 above |
| base-7108 | base | 7108 | none | 7/20 | 1 | the 13 above |
| base-7109 | base | 7109 | none | 7/20 | 1 | the 13 above |
| base-7110 | base | 7110 | none | 7/20 | 1 | the 13 above |
| rep-base-{7107,7108,7109,7110} | base | same 4 | none | 7/20 | 1 | the 13 above |
| load2-base-7107 | base | 7107 | 2 busy loops | 7/20 | 1 | the 13 above |
| load32-base-7108 | base | 7108 | 32 busy loops | 7/20 | 1 | the 13 above |
| ref-{7107,7108,7109,7110} | ref | 4 seeds | none | 20/20 | 0 | none |
| rep-ref-{7107,7108,7109,7110} | ref | same 4 | none | 20/20 | 0 | none |
| load2-ref-7107 | ref | 7107 | 2 busy loops | 20/20 | 0 | none |
| load32-ref-7108 | ref | 7108 | 32 busy loops | 20/20 | 0 | none |

Total: 24 counter runs (12 per builder). Raw per-run outputs are in the scratch directory, which was deleted before yield, as instructed. The leg lines above are quoted from those outputs; for example, base 7107 printed `LEG H14 BIGTXT fail rc=0 rss_kib=608836 limit=98304` and ref printed `LEG H14 BIGTXT pass rc=1 rss_kib=20404 limit=98304`.

## Not done / limits
- I did not run regress.py, c2-count.py, the controls, or the sniff sweep (not in my item).
- I did not read the counter source, so statements about how H20's verdict is derived are INFERENCE.
- No installs, no edits outside this report and my scratch. No labrat spawned.

VERDICT: BASE=7-7/20 REF=20-20/20 flaky_legs=none
