# ConnectSiblings — round 46 wave 1

item: sibling-overlap scan of the C3 theme (`FEVER`, `AVeriTeC`, `AveriMaTeC`,
`zenodo`, `archive.org`, `Memento`, `cached_source_url`, `evidence pool`) across every
`/home/vgpnk/Projects/shokunin/*-shokunin/corpus/` (chousa excluded), the fleet-root
misroot sweep over `git status --porcelain`, and one bounded connector move.
seat: leaf connector. Read-only; no fetch, no production write, no git/jj mutation.
Only file written: this one. No `/tmp` scratch created.

## 1. Commands (decisive lines; long path lists condensed with `{}`/`;`, nothing else altered)

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
 M .ufo/state/{14 lanes}.report-baseline ; M .ufo/watchdog.log
 M scripts/hyaku/{hyaku.env,lane-addendum.md}
?? .omp/mcp.json ; ?? .scratch/goal-20261025-hyaku-12h.md
?? .ufo/reports/round-69/revenger.md ; ?? .ufo/state/{kotoba,kotodama,revenger}.report-baseline
?? .ufo/waves/round-24/ ; ?? .ufo/waves/round-69/

$ grep -rniE --include='*.md' --include='*.tsv' --include='*.json' \
    'FEVER|AVeriTeC|AveriMaTeC|Memento|cached_source_url|evidence pool' */corpus/
audio 0 · game-dev-2d 0 · game-dev-3d 0 · kagi 0 · kaidoku 0 · kake 0 · kama 0 ·
kasegi 0 · kengaku 2 · kotoba 0 · kotodama 1 · kumitate 0 · lore 0 · mado 0 · mori 0 ·
revenger 0 · souji 0 · tabi 0 · tameshi 0 · tsukuroi 0
```

An include-less first sweep returned only binary `.x86_64` and vendored `cannon-es.js`
noise; unused below.

## 2. Sibling overlap: the theme is absent as held ground

20 lane corpora scanned, 3 hit lines, all false positives:

| lane | path:line | text | absorbs C3's theme? |
|---|---|---|---|
| kengaku | `corpus/knowledge/eval-design-digest-3.md:65` | "35.1 EM / 64.6 Fever, better than either alone" | **No** — FEVER as a benchmark *score* in a ReAct paper note; no evidence field, no archive binding |
| kengaku | `corpus/lessons/round-30.md:23` | "both the memento snapshot and the live page served 200" | **No, but adjacent** — Memento as a *fetch route* for one payload-absent row, not admitted ground on S079 |
| kotodama | `corpus/SOURCES.md:771` | "colds, fevers, rheumatism" | **No** — medical fever |

`zenodo` breadth (kotodama 9, kaidoku 5) is citation URLs and PyPI-JSON text; `archive.org` breadth (kotodama 434, souji 4, lore 2) is locators for unreachable hosts. **Judgment: C3 absorbs no sibling's held ground.**

## 3. What siblings *do* hold: capture-binding as unstated practice

| lane | path:line | practised |
|---|---|---|
| lore | `corpus/SOURCES.md:40` | S032 binds one citation to **two** Wayback captures, each with "decompressed sha256", plus a re-open seat |
| kaidoku | `corpus/SOURCES.md:31,34` | "snapshot sha256" per source row |
| tameshi | `corpus/SOURCES.md:119`; `lessons/round-39.md:14`,`round-40.md:20` | "Access 2026-10-24. Snapshot sha256 `eb9d…`" per row |
| kagi | `corpus/SOURCES.md:35,165` | "decoded-http-body-v1 representation"; "its capture digest is a point" |
| kumitate / revenger | `lessons/round-58-verifier-spotcheck.md:22`; `knowledge/round-64-firmware-region-byte-evidence.md:210` | verifiers re-check "the capture digests"; byte-counted snapshot quotes per row |

Second-order consequence, and why this is a connector finding: the theme is not novel
fleet-wide — it is the first *statement* of a rule six lanes already obey by habit. The
entries must not present capture-binding as a discovery nor borrow a sibling's figures.

## 4. Misroot sweep: zero misrooted chousa artifacts

| untracked path | names chousa / round-46? | attribution |
|---|---|---|
| `.omp/mcp.json` | no | harness MCP config, fleet level |
| `.scratch/goal-20261025-hyaku-12h.md:63` | **chousa** in a schedule line ("Next block: chousa (0 this run), kumitate, …") | fleet-level hyaku goal, correctly at fleet root; not a chousa artifact |
| `.ufo/reports/round-69/revenger.md`; `.ufo/state/{kotoba,kotodama,revenger}.report-baseline` | no | fleet report convention; per-lane baselines |
| `.ufo/waves/round-24/w2/RevUnlandedResolution.md`, `.ufo/waves/round-69/w1/ScoutAmp.md` | no (grep empty) | fleet-repo waves; round space distinct from the lane's `round-46` |

Nothing deleted; nothing defective beyond this attribution. Lane-side untracked state is
the expected build set (`corpus/evidence/round46/*`, the two entries,
`tools/inference-ground.py`).

## 5. Contradiction, stated not smoothed

`corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md` Unknown carries
"how large that share is was not measured from this capture." Staged source,
`/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/
evidence-pool-versioning-r39-amendment-2026-10-23.md:74`: "How large that share is was
not measured." The lane has measured it from a capture it holds:

* `evidence-snapshot-coverage-r40.md:12` — "1,582 answers name a `source_url` and carry
  no archive field at all, 1,491 of them a real source rather than `Metadata`" (S084).
* `evidence-snapshot-coverage-r40.md:21` — "Of the 7,572 answers that name a real
  source …, 5,959 (78.7%) carry a web.archive.org link" (S084).

Both readings recorded: the narrowing to "from this capture" is true of S088, yet it
leaves the hole looking unmeasured when round 45 counted 18.66% (1,582/8,479) and 78.70%
(5,959/7,572, recomputed `0.78698…`). Under C3's kill rule ("a staged sentence that the
captures contradict is corrected in the entry and recorded as a mistake; it is never
silently carried"), carrying it as Unknown — even narrowed — sits on the weaker side of
the rule. Second instance, duplication not contradiction: the amendment's first
Observation and `evidence-archive-field-policy-r41.md:11` are the same dictionary
sentence, re-derived from a second document.

```
$ grep -rlF 'An archive.org link for the source url' .qcache/
b73f7e8dd5b0ace740e48046.txt (S088 page)  ce16d57277fedfd4f0e7750e.txt (S082 README)
$ python3 -c "import hashlib;print(hashlib.sha256(b'https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/README.md').hexdigest()[:24])"
ce16d57277fedfd4f0e7750e
```

`ce16d57277fedfd4f0e7750e` is S082's capture: re-deriving a fact from a second document is depth *only if stated*; unstated, depth counts one fact twice.

## 6. Proposed move (one, bounded — text-only, one file)

In `corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md`, in the two
slots already marked for correction:

1. Replace the last Unknown bullet with a bounded Observation binding the held S084
   count by document: conditional archive measured at 78.7% of real-source answers
   (5,959/7,572), 1,582 answers with no archive field
   (`corpus/knowledge/evidence-snapshot-coverage-r40.md`, S084). Record the staged
   sentence as corrected-and-recorded, per the kill rule.
2. In the Inference bullet "AVeriTeC applies that route per citation rather than per
   corpus", name both instruments as held: FEVER's dated pool (S085–S087, no per-page
   revision) against per-citation archived copy with measured coverage (r40, S084) and
   a documented double-archive 404 class (r41, S082–S083); add one clause that the S088
   sentence re-derives r41's S082 sentence.

No new spans, rows, counters, fixtures, predicates or targets.

## 7. Axes, risks, verification

**depth — improves.** One staged Unknown the lane can answer stops being carried; one
dictionary fact stops counting twice; the FEVER-vs-AVeriTeC contrast gains a measured
leg — all at zero new capture cost. **operability — unchanged** (no tool, counter or
fixture). **calibration — unchanged, one guard:** `corpus/evidence/round46/c3-count.py:
50-52` already whitelists `S079`–`S084`, so `S082`/`S084` are legal tokens, and
`QUOTE_ROWS` must stay 11, so the r40 figure is cited by lane path, never minted as a
twelfth row.

Risks: (i) reflow must not perturb committed quote bytes — `An archive.org link for the source url`, `Our best estimate for the date the claim first appeared`, `temporally constrained evidence annotation`, `published before the claim’s date` (curly apostrophe); (ii) reading "cite r40" as licence to add a span breaks `QUOTE_ROWS=11/11`; (iii) circularity — answered by warranting on S084, citing r40 after it; (iv) register row S116 is already adjudicated a two-column extraction false positive in `ScoutQuarantineOverlap.md`.

Verification (main agent, after landing): `python3 corpus/evidence/round46/c3-count.py`
→ `ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=2/2 C3=PASS`, exit 0; and the same with `CAPTURE_BOUND=skipped` under `--lane-only`.

## 8. Second-order: the frozen counters are no longer at the freeze bytes

`git diff --stat corpus/evidence/round46/` — `c1-count.py | 5 ++++-`, `c2-count.py | 27
+++++++++++++++++++++++----`, `2 files changed, 27 insertions(+), 5 deletions(-)`. Both
are post-freeze, both cite mutation seats (`MutC1Junk`, `MutC2Forge`): c1's junk leg
moves `!= 0` → `== 1` (matching the frozen "exits 1", so a crash is no longer a kill);
c2 gains fence-awareness, HTML-comment stripping and boundary-safe path membership. Each
strictly tightens and each is a conformance fix toward the frozen text, not a target
change — but under "a rule changed after any seat has scored is not this claim's rule",
no earlier C1/C2 PASS is inheritable: name the counter revision per verdict and re-run
before admission. `c3-count.py` is unmodified at this writing.

## Verdict

No sibling absorbs C3's theme (3 hits in 20 corpora, all false positives) and the fleet root holds zero misrooted chousa artifacts. The live defect is in-lane: the adopted amendment carries the staged "not measured" Unknown that `evidence-snapshot-coverage-r40.md:12,21` answers from S084, and re-derives r41's S082 sentence from S088 unstated — which C3's own kill rule says to record as a correction. Fix is one file of text; every counter leg stays where it was frozen.

tooling: none installed or upgraded.
