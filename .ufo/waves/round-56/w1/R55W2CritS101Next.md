# R55W2CritS101Next — S101 builder frontier check

Axes: operability, depth, calibration. Attacked the round-55 README statement about four round-54 S101 quotes. No frozen round-56 predicate or production file changed.

## Reproduction

Input rows are `R54DraftEntryStb.md:212-215` in `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-54/w1/`; exact quote strings and URL are those rows. Ran the current lane `tools/build-spans.py` (not the historical revision used by the W1 report), with the required read-only capture cache and scratch-only input/output:

```sh
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py --quotes "$S/quotes.tsv" --out "$S/out" --cache /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache
```

Observed:

```text
QUOTE S101 char 13105 spans/S101-1.txt
QUOTE S101 char 13194 spans/S101-2.txt
QUOTE S101 char 13484 spans/S101-3.txt
QUOTE S101 char 25014 spans/S101-4.txt
SPANS_ROWS=4 WRITTEN=4
```

There were no refusals. The README statement “build 4/4 with the new builder” is accurate for these quote inputs and the current builder: 4 rows written, exit success. The prior W1 report independently records unique whole-defined-form matches and exact-slice checks (`R55ExecS101Leg.md:13-22`); this run's offsets agree exactly.

## Correction-anchor comparison

`R54DraftS101Reanchor.md:50-56` gives the six S101 Registry pointer corrections: old→new positions 11170→11972, 11205→12007, 11993→12795, 12161→12963, 13247→14049, and 34374→25123. This build tested four different round-54 draft quotes, so it does not retest those six anchors. Its four offsets (13105, 13194, 13484, 25014) are not those Registry quote anchors; do not conflate them. The cited correction report states those corrections were derived in the defined text form and supplies unique target anchors (`R54DraftS101Reanchor.md:48-59`). The builder offsets therefore neither contradict nor independently validate the Registry corrections.

VERDICT — the four S101 quote build survives (4/4, no refusals; offsets match the earlier report); the Registry correction offsets concern separate quotes and remain untested by this four-quote build.
