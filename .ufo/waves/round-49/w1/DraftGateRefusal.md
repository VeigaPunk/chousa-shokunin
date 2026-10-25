# DraftGateRefusal — round 49, wave 1

## Axes and scope

Axes: operability, depth, calibration. This report makes no change to either frozen predicate, target, counter, or control (`corpus/evidence/round49/claims.md:18-91`). No adoption performed. No network/source fetch performed. I wrote only this report.

## Frozen-counter probes

Commands run from `/home/vgpnk/Projects/shokunin/chousa-shokunin`:

```text
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round49/c1-count.py
...
SETS_PASS=3/3
C1=PASS
C1_RC=0
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round49/c2-count.py
...
ENTRIES=0/2
BOUND=0/9 (min 7) REFUSED=0
...
INFERENCE_GROUNDED=0/2
QUARANTINE_VERDICTS=0/5 (S082,S084,S086,S095,S096)
C2=FAIL
C2_RC=1
```

C1 therefore passed this invocation's A/B/C, GUARD and PIPE legs; this is not a claim of generalized behavior beyond the frozen sets. C2 did not pass: adopted-entry paths do not yet exist in the lane, no bindings/refusals/spans/lesson verdicts are counted. Claims doc says C2 cannot substitute these checks for Gate judgment (`claims.md:83-91`). `python3 .../c2-count.py --lane-only` was also run; output likewise `ENTRIES=0/2`, `BOUND=0/9`, `INFERENCE_GROUNDED=0/2`, `QUARANTINE_VERDICTS=0/5`, `C2=FAIL`, rc 1. This report is not the final wave integration.

## Capture-key command and observations

Required one-liner, with the exact URL strings taken from the package rows (`SOURCES.append.md:60-61,70,74,85,112`):

```python
import hashlib, os
urls={'S124/S135/S187':'https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf','S136':'https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf','S145':'https://bs.bnu.edu.cn/docs/20160407183946745914.pdf','S149':'https://chn.oversea.cnki.net/index/gb/gb-manual.html','S160':'https://check.cnki.net/tmlc/'}
q='/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/'
for k,u in urls.items():
 h=hashlib.sha256(u.encode()).hexdigest()[:24]
 print(k,h,*(f'{e}={os.path.exists(q+h+e)}' for e in ['.txt','.raw','.fail']))
```

Observed output:

```text
S124/S135/S187 e3ca8f4fdd15420b80096a75 .txt=True .raw=True .fail=False
S136 28750bcdf5d36cd90a7709fb .txt=True .raw=True .fail=False
S145 275c79d45b1e9b0fd32cef93 .txt=True .raw=True .fail=False
S149 625375f640d6eb3be0990ef2 .txt=True .raw=True .fail=False
S160 dd50f086f911d06fa2bbd5f9 .txt=True .raw=True .fail=False
```

Note: first invocation had a typo (`urs` rather than `urls`) and returned `NameError`; corrected invocation above produced the observations. Capture existence is not evidence of quote support or a register verdict (QUALITY.md:28-31).

## Gate table draft — two of the five candidates

Candidates and sources are in read-only package `merge/chousa/knowledge/corpus/knowledge/`:

| entry | decision | reason | flip |
|---|---|---|---|
| `cnki-citation-check-r40.md` (S124) | **ADMIT-LATER; refuse this round** | Its manual is directly relevant to citation-check states, but duplicates the adopted theme's already established index-vs-source question only loosely: it is a separate CNKI checking feature, not evidence that index citation data is derived. No source-support adjudication was performed here. Capture `e3ca8f4fdd15420b80096a75.txt` and `.raw` exists. The absence register's first 60 lines has no row matching this URL; absence from that excerpt is not a clean verdict. | Reconsider in a later round if a frozen question specifically asks how citation-checking compares a pasted reference with an index record, with quotes re-grounded from the existing capture and a scoped source row. |
| `cnki-matching-modes-r42.md` (S149) | **REJECT for this round** | The package teaches search-platform per-field matching modes, explicitly distinct from the 引文核对 auxiliary feature (`cnki-matching-modes-r42.md:7,20-32`). It is not evidence for the adopted claim about citation-index data being derived; admitting it would broaden this round beyond its frozen theme. Capture `625375f640d6eb3be0990ef2.txt` and `.raw` exists. | Flip only if a later frozen research question concerns the search platform's field-specific matching taxonomy and the entry is judged within province for that question. |

The `absent-defect-register.md` header defines `payload-absent` as a candidate requiring manual verification, not automatic rejection; `unreachable` likewise is not fabrication (lines 1-9). I did not claim either candidate received a verdict there. These are author-lane draft decisions, not closure verdicts.

## Draft adoption Gate material (not landed)

The staged pair in `.ufo/waves/round-49/assimilation/adopt/corpus/knowledge/` frames the theme as (i) CiNii matched references/counts and J-STAGE resolution/timing, and (ii) Chinese citation-count fields, coauthor self-citation, and reference-data specification (opened files `aggregator-vs-source-r36.md:15-27,44-70`; `citation-count-semantics-r37.md:14-34,36-70`). This is a description of scratch text, not proof of entailment. The lane Gate should record per-document re-groundings and explicit refused-document rows before claiming the frozen C2 result; the counter itself says Gate adjudicates province/quality/coverage (`claims.md:83-85`).

## Touched surfaces and limits

- **Written:** `.ufo/waves/round-49/w1/DraftGateRefusal.md` only.
- **Read:** `PROVINCE.md:3-17`; `corpus/QUALITY.md:1-31`; frozen claims; staged package rows/candidates; read-only absent-defect register; capture existence checks; scratch adopted entries; frozen C1/C2 counter output.
- **Out of scope / not done:** no product, lesson, registry, entries, spans or counters edited; no source fetched; no campaign tool run; no definitive verdict on other three candidate entries; no final C2 pass or source entailment claimed. Tool installs: none.

VERDICT: Probed the frozen counters and drafted two scoped Gate decisions; C1 passed the frozen invocation, C2 remains failing/unbuilt, and no candidate was adopted.
