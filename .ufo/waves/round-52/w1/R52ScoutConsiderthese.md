# R52ScoutConsiderthese — considerthese assimilation (lane tip `13bc280`, read-only)

Read: all EIGHT files `considerthese/2026-10-26.md … 2026-10-19.md` (`wc -l` = 463; the brief said seven, `2026-10-26.md` (46 lines, commit `9b99ede`) is new since round 51's sweep of 417 lines). Lane mining record: `grep -rn considerthese corpus/lessons corpus/QUALITY.md LOG.md` -> QUALITY 60/61/62/64/68/71 (`QUALITY.md:540,551,563,595,684,732`), lessons round-24 (M-7), 44, 47 (`:272`), 48 (`:69-73`), 49 (`:180`), 50 (`:159-161`), 51 (`:173-175`), LOG.md:1526,1553,1623,1688,1781,1805,1830. Round 51 swept 10-19..10-25 (`.ufo/waves/round-51/w1/R51ScoutConsiderthese.md`: 31 proposals; 19 IMPL / 10 FMT / 2 OPEN by its status column). I re-opened that ledger; its 31 statuses stand except where re-checked below. Nothing was edited; scratch removed.

## Ledger delta: 2026-10-26.md (new) — the only file not yet swept

| Item | Section | Status | Evidence |
|---|---|---|---|
| L0 `8d77e6c1` age (9 rounds) | Waiting | IMPL (lane side) | `corpus/evidence/round51/open-items-age.py` exists; 10-26 itself cites it. Item itself stays operator-owned. |
| Round-47 polarity trade: confirm moot after 12/12 | Waiting | OPEN, operator-owned | `SCORECARD.md:2513` still reads `improved, disputed as a trade`; no ruling line recorded. Not a lane artefact. |
| Uncommitted inherited `swarm-registry.json` / QUALITY edit | Waiting | STALE at lane tip | `git status --short` in lane shows only ` M SKILL.md` (round-52 seat work) and `?? .ufo/waves/round-52/...`; `git status --short -- '*swarm-registry*'` shows only `?? .ufo/waves/round-52/w1/swarm-registry.json` (new); `git diff --stat -- corpus/QUALITY.md` empty. 10-26 is wrong or reading a different tree; not mineable. |
| Stable proposal ids `CT-YYYYMMDD-n` | Proposals | FMT | names no lane artefact (reflection's own format) |
| Recurring weaknesses as a streak table | Proposals | OPEN, thin | The forgeable-frozen-counter streak (r49, r50, r51) is already routed: `round-51-verifier-spotcheck.md` §6 item 1 and the round-52 C1 work. `grep -n -i -E 'streak\|recurr\|repeat(ed)? (blocker\|class)' corpus/QUALITY.md SCORECARD.md` -> no streak table (only `QUALITY.md:354`, unrelated). |
| Report where lane and verifier disagree | Proposals | OPEN, in province, checkable | no artefact: `ls corpus/evidence/round52/` has no gap script; `grep -rn -l -i -E 'verdict-gap\|VERDICT_GAPS' . --include=*.py --include=*.md` -> no output. |
| One independent CJK quote spot-check per review | Proposals | FMT | a reader outside the lane; lane-side analogues exist (`quote-substance-check.py`, non-author spot-checks agree 8/8 in r50, r51) |

## The four-receipt item (2026-10-25 "Waiting on you")

Still failing at tip, and reclassified rather than fixed. Run (read-only, `TMPDIR` in scratch), `python3 corpus/evidence/round40/c1-count.py`:

```
corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round39/receipts/c1-after-s39111.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round39/receipts/c2-after-s39101.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round39/receipts/c2-after-s39121.json: fail VERIFY-FAIL: gate-sha256-mismatch
R39_ACTIVE_RECEIPTS=2/6      rc=1
```

(the other two rows print `VERIFY: ok`.) Cause: `git log -1 --format='%h %s' -- tools/research-gate.sh` = `1bd9001 round-41: pin capture invocation surface…`; current `sha256sum tools/research-gate.sh` begins `2cb04bddfd5601d7`, the receipts bind `4253c187…` (`corpus/evidence/round48/receipt-recheck.txt`). Round 48 ran the pinned leg at the adding commits `d164f88e`/`6d914e95`: `PINNED_ADDING_COMMITS=6/6`, and declared the mismatch expected drift with no bytes reissued (QUALITY 68, `QUALITY.md:664-688`; `lessons/round-48.md:69-73`). 10-26 `:35` drops it from the open list. Verdict: failing-as-designed; a counter that prints `2/6` rc 1 forever is the cost (the pinned leg is in the evidence file, not in `c1-count.py`). Not re-opened as a pick.

## Other statuses re-checked at tip

- 10-19 "Watch SKILL.md size / distil": still open, unactioned — `wc -l SKILL.md` = 738 (was 733 in round 51, ~420 when proposed); no QUALITY check names size. No agreed threshold, so not picked.
- 10-22 "cost per gain / wall time / streaks": out of province (`PROVINCE.md` refuses orchestration → kumitate).
- 10-25 "waiting on you box with age": IMPL as `open-items-age.py` (round 51).

Totals now: 38 rows (31 older + 7 from 10-26: 4 proposals + 3 waiting items). The 31 older rows keep round 51's split; the seven 10-26 rows split 1 IMPL / 1 STALE / 2 FMT / 1 OPEN-operator / 2 OPEN-lane (streak table, verdict gap).

## The one pick: lane-vs-verifier verdict gap (10-26 Proposals, bullet 3)

Why it fits: calibration is a judged axis of this lane; the data is already committed (SCORECARD `## Round N verdict` axis table vs `corpus/lessons/round-N-verifier-spotcheck.md` axis table) and parseable without prose judgement. It is the only open item with a measurable disagreement today: round 47 operability lane `improved, disputed as a trade` (`SCORECARD.md:2513`) vs verifier `harmed` (`round-47-verifier-spotcheck.md:35`); round 50 calibration lane `improved narrowly` (`SCORECARD.md:2607`) vs verifier `unchanged` (`round-50-verifier-spotcheck.md:59`). Not picked: the streak table (already routed in r51 §6 and round-52 C1), ids / CJK spot-check (reflection-only), SKILL.md size (no threshold).

Prototype (intended path `corpus/evidence/round52/verdict-gap.py`; run from scratch, read-only). Output on rounds 46-51 at tip:

```
R46 axes lane=6 verifier=6
R47 operability: lane=improved verifier=harmed
R47 axes lane=6 verifier=6
R48 axes lane=6 verifier=0
R49 axes lane=6 verifier=6
R50 calibration: lane=improved verifier=unchanged
R50 axes lane=6 verifier=6
R51 axes lane=6 verifier=6
VERDICT_GAPS=2      rc=1
```

Named limits: direction is the first of improved|unchanged|harmed, so "narrowly"/"disputed" qualifiers are dropped; `R48 verifier=0` is the parser missing round 48's verifier format (axes written as `- **discernment — unchanged.**` bullets, `round-48-verifier-spotcheck.md:73-74`) — the lane version must either handle that form or exit 2 on a round with zero verifier axes.

```python
#!/usr/bin/env python3
"""verdict-gap — lane axis grade vs non-author verifier axis grade, per round (considerthese 2026-10-26)."""
import pathlib, re, sys
ROOT = pathlib.Path(sys.argv[1]); R0, R1 = int(sys.argv[2]), int(sys.argv[3])
AX = ("operability", "depth", "calibration", "coverage", "freshness", "adjacency")
def dirn(s):
    m = re.search(r"improved|unchanged|harmed|regress", s.replace("*", "").lower())
    return m.group(0) if m else None
def table(lines):
    out = {}
    for l in lines:
        m = re.match(r"^\|\s*(%s)\s*\|\s*(.*?)\s*\|" % "|".join(AX), l)
        if m and dirn(m.group(2)):
            out.setdefault(m.group(1), dirn(m.group(2)))
    return out
sc = (ROOT / "SCORECARD.md").read_text(encoding="utf-8").splitlines()
gap = 0
for n in range(R0, R1 + 1):
    st = next((i for i, l in enumerate(sc) if re.match(r"^## Round %d verdict" % n, l)), None)
    vf = ROOT / f"corpus/lessons/round-{n}-verifier-spotcheck.md"
    if st is None or not vf.exists():
        print(f"R{n} MISSING scorecard={st is not None} verifier={vf.exists()}"); gap += 1; continue
    en = next((i for i in range(st + 1, len(sc)) if sc[i].startswith("## ")), len(sc))
    lane, ver = table(sc[st:en]), table(vf.read_text(encoding="utf-8").splitlines())
    for a in AX:
        if a in lane and a in ver and lane[a] != ver[a]:
            print(f"R{n} {a}: lane={lane[a]} verifier={ver[a]}"); gap += 1
    print(f"R{n} axes lane={len(lane)} verifier={len(ver)}")
print(f"VERDICT_GAPS={gap}")
sys.exit(1 if gap else 0)
```

Check that would show it implemented (absent today: `ls corpus/evidence/round52/` lists `build-spans.py c1-count.py c2-count.py census-start.txt claims.md controls` only):

```
python3 corpus/evidence/round52/verdict-gap.py --root . --from 46 --to 51
# implemented = the file exists, the round-52 SCORECARD verdict links its output, and the run prints
#   R47 operability: lane=improved verifier=harmed / R50 calibration: lane=improved verifier=unchanged  (rc 1 = gaps listed, not hidden)
# shown able to fail: change a lane axis cell in a scratch copy of SCORECARD.md from `improved` to `unchanged` for round 51 -> an extra `R51 …` gap line.
```

Caveat: the pick makes a calibration signal visible; it closes no operator item and changes no grade. The L1 owns the argument handling (the prototype takes positional args) and the round-48 verifier form.

Tooling: no install or upgrade. Scratch `/fast/scratch/hyaku/chousa-r52/R52ScoutConsiderthese/` removed at the end.

VERDICT: swept all eight considerthese files (31 round-51 rows kept + 7 new 10-26 rows) and re-ran the four-receipt check (still `R39_ACTIVE_RECEIPTS=2/6` rc 1, four `gate-sha256-mismatch`, expected drift since `1bd9001`, dropped by 10-26); picked one open proposal — the lane-vs-verifier verdict gap — with a prototype that prints 2 real gaps (r47 operability, r50 calibration) and a check command absent today.
