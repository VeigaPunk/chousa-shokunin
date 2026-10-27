# R56ExecWaveSettled — the round-55 wave-settled check on rounds 55 and 56, and the retired/carried wave class

Seat: `R56ExecWaveSettled`. Lane writes: this report only. Everything else ran in
`/fast/scratch/hyaku/chousa-r56/R56ExecWaveSettled` (12 fixture git repos, removed at the end; every
`git -C` fixture asserted `rev-parse --show-toplevel` = the fixture dir before its first commit).
No network, no tool installs or upgrades (none needed). No lane file was modified; the successor below
is a **proposal**, not a landing.

## 1. What I ran, raw

```
$ python3 corpus/evidence/round55/wave-settled-check.py --round 55
UNSETTLED w1 results=2026-10-27T01:26:01-03:00 after report=2026-10-27T01:11:40-03:00
WAVES=1 SETTLED=0
exit=1

$ python3 corpus/evidence/round55/wave-settled-check.py --round 56
usage: no committed <wave>.ready.dispatched under .ufo/waves/round-56
exit=2

$ python3 corpus/evidence/round55/wave-settled-check.py --round 56 --before-filing
usage: no committed <wave>.ready.dispatched under .ufo/waves/round-56
exit=2
```

Commits behind the two timestamps: fleet `.ufo/reports/round-55/chousa.md` added by `ac629889`
(`2026-10-27T01:11:40-03:00`); lane `w1-results.json` added by `e5a3795` (`2026-10-27T01:26:01-03:00`).
The check's round-55 verdict is **correct** and its `WAVES=1` is **wrong** (§3).

Round 56 is **not** UNSETTLED. It is a usage error: `corpus/evidence/round55/wave-settled-check.py:52`
enumerates waves from *committed* `.ready.dispatched` files only, and round 56's dispatch marker is
untracked:

```
$ git status --porcelain | grep round-56
?? .ufo/waves/round-56/w1.ready
?? .ufo/waves/round-56/w1.ready.partial
$ git ls-files -- .ufo/waves/round-56
.ufo/waves/round-56/assimilation/collisions
…
.ufo/waves/round-56/w1-dispatch.json
.ufo/waves/round-56/w1-run.err
.ufo/waves/round-56/w1-spec.json
.ufo/waves/round-56/w1/swarm-registry.json
```

So a wave that is dispatched and in flight but whose marker has not been committed reads as "this round
launched nothing" — exit 2, indistinguishable from an empty round. The item's requirement ("round 56 …
must be UNSETTLED") **fails on the shipped check**.

## 2. Retired / carried waves: what the shipped check can and cannot see

- **Retired-after-dispatch: handled.** `:67-68` accepts a *first-line* ` ABANDONED:` in a committed
  `.ready.dispatched` marker with no results (round 53's `w2`); verified live in §5 (`ABANDONED w2`).
- **Retired-before-dispatch: invisible.** The branch is reached only from `:52`'s `.ready.dispatched`
  list, so its own precondition is "the dispatcher took the wave". Round 55's wave 2 was never taken:
  `ls .ufo/waves/round-55 | grep -i w2` → `gen-w2-spec.py`, `w2-spec.json` (committed in `53f1ce6`,
  "W2 spec prepared and not dispatched"); there is no `w2.ready` and no `w2.ready.dispatched`. The
  check prints `WAVES=1`, i.e. the 36 falsify items the round owed are dropped from the receipt.
- **Carried: no code path at all.** Nothing in the script reads a spec, a marker body other than the
  abandoned test, or any cross-round file; `w2-spec.json` is never opened. The carry of round-55's 36
  items into round 56 exists **only in prompt prose** — `.ufo/waves/round-56/w1-spec.json:10` (context)
  and `:165` (this seat's item text) — and in `.ufo/waves/round-56/w1-dispatch.json:390,865,1020`.
  No lane file records it, so no check could have seen it: round 55's green-shaped `WAVES=1` is a silent
  drop, and under round 56's own rule round 55 is red (`w2` has neither results nor a carried marker).

## 3. Proposed successor (60 lines, fenced; tested, not landed)

Changes against the shipped check: (a) wave discovery is the union of committed **and on-disk**
`<wave>{-spec.json,-results.json,.ready,.ready.dispatched,.carried-to}`, so a prepared spec and an
uncommitted dispatch marker are visible; (b) `<wave>.carried-to` with first line
`carried-to: <round>/<wave>` yields `CARRIED` only when the target has SETTLED (chains followed,
cycles refused) — and `UNSETTLED` when it has not; (c) a wave with neither results nor a carried
marker is UNSETTLED (the item's required failure); (d) verdicts, `WAVES=n SETTLED=k` and the exit
codes 0/1/2 keep the shipped contract.

```python
#!/usr/bin/env python3
"""wave-settled-check-v2 — no report until every wave of its round has a verdict.
EXISTS: any <wave>{-spec.json,-results.json,.ready,.ready.dispatched,.carried-to} committed or on disk under
.ufo/waves/round-N/ (a prepared spec counts: the round owes it a verdict). SETTLED: results committed, not
after the report's commit. CARRIED: <wave>.carried-to's first line `carried-to: R/W` with R/W SETTLED
(chains followed, cycles refused). ABANDONED: the dispatched marker's first line carries ` ABANDONED:`.
UNSETTLED: everything else, notably a wave with neither results nor a carried marker.
Exit 0 all SETTLED/CARRIED/ABANDONED · 1 any UNSETTLED · 2 usage (no wave, or no report commit).
Usage: wave-settled-check-v2.py --round N [--lane DIR] [--fleet DIR] [--id chousa] [--before-filing]
"""
import argparse, datetime as dt, pathlib, re, subprocess, sys
LANE = pathlib.Path(__file__).resolve().parents[3]
PAT = re.compile(r"^(?P<w>.+?)(?:-results\.json|-spec\.json|\.ready(\.dispatched|\.partial)?|\.carried-to)$")

def git(r, *a):
    return subprocess.run(["git", "-C", str(r), *a], capture_output=True, text=True).stdout.strip()

def at(r, p):
    out = git(r, "log", "--diff-filter=A", "--format=%cI", "--", p).splitlines()
    return dt.datetime.fromisoformat(out[-1]) if out else None

def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--round", type=int, required=True); ap.add_argument("--lane", default=str(LANE))
    ap.add_argument("--fleet", default=str(LANE.parent)); ap.add_argument("--id", default="chousa")
    ap.add_argument("--before-filing", action="store_true"); a = ap.parse_args()
    lane, fleet = pathlib.Path(a.lane), pathlib.Path(a.fleet)
    ck = set(git(lane, "ls-files", "--", ".ufo/waves").splitlines())
    def rd(p):
        f = lane / p
        return f.read_text(encoding="utf-8", errors="replace") if f.is_file() else git(lane, "show", f"HEAD:{p}")
    def verdict(rnd, w, filed, seen=()):
        wd, tag = f".ufo/waves/round-{rnd}", f"{rnd}/{w}"
        res, car, dsp = f"{wd}/{w}-results.json", f"{wd}/{w}.carried-to", f"{wd}/{w}.ready.dispatched"
        if (t := at(lane, res) if res in ck else None):
            return (f"UNSETTLED {w} results={t.isoformat()} after report={filed.isoformat()}"
                    if filed and t > filed else f"SETTLED {w} results={t.isoformat()}")
        if (lane / res).is_file(): return f"UNSETTLED {w} results present but uncommitted"
        if dsp in ck and " ABANDONED:" in rd(dsp).split("\n", 1)[0]:
            return f"ABANDONED {w} (marker: {rd(dsp).splitlines()[0][:60]})"
        if car not in ck and not (lane / car).is_file():
            return f"UNSETTLED {w} no committed results and no carried-to marker"
        first = rd(car).strip().splitlines()[0]; m = re.fullmatch(r"carried-to:\s*(\d+)/([\w.-]+)", first)
        if not m: return f"UNSETTLED {w} carried-to marker malformed: {first[:60]!r}"
        tr, tw = int(m[1]), m[2]
        if tag in seen or f"{tr}/{tw}" in seen: return f"UNSETTLED {w} carried-to cycle {tag} -> {tr}/{tw}"
        v = verdict(tr, tw, None, (*seen, tag))
        return (f"CARRIED {w} -> {tr}/{tw} ({v.split()[0].lower()})" if not v.startswith("UNSETTLED")
                else f"UNSETTLED {w} carried-to {tr}/{tw}: {v}")

    wd, report = f".ufo/waves/round-{a.round}", f".ufo/reports/round-{a.round}/{a.id}.md"
    names = {p for p in ck if p.startswith(wd + "/")} | {f"{wd}/{p.name}" for p in (lane / wd).glob("*")}
    ws = {m["w"] for n in names if (m := PAT.match(n.rsplit("/", 1)[-1]))}
    if not ws: print(f"usage: no wave artifacts under {wd}", file=sys.stderr); return 2
    filed = None if a.before_filing else at(fleet, report)
    if filed is None and not a.before_filing: print(f"usage: no fleet commit adds {report} (use --before-filing)", file=sys.stderr); return 2
    out = [verdict(a.round, w, filed) for w in sorted(ws)]; bad = sum(l.startswith("UNSETTLED") for l in out)
    print("\n".join(out + [f"WAVES={len(ws)} SETTLED={len(out) - bad}"]))
    return 1 if bad else 0
sys.exit(main())
```

## 4. Fixtures (12 cases, throwaway git repos; observed output)

`bash fixtures.sh` in scratch, transcript kept and inlined here. `old` = shipped check on the same tree.

| # | fixture | v2 verdict | v2 exit | shipped check |
|---|---|---|---|---|
| C1 | r55 `w2-spec.json` + `w2.carried-to` → `56/w1`; r56 w1 results | `SETTLED w1`, `CARRIED w2 -> 56/w1 (settled)`, `WAVES=2 SETTLED=2` | 0 | `WAVES=1 SETTLED=1`, exit **0** — the retired wave is silently dropped |
| C2 | same, r56 w1 marker only (no results) | `UNSETTLED w2 carried-to 56/w1: UNSETTLED w1 …` | 1 | — |
| C3 | `w2.ready` only, no results, no carried marker | `UNSETTLED w2 no committed results and no carried-to marker` | 1 | — (wave invisible → 0) |
| C4 | r55 results **after** the fleet report / **before** it | `UNSETTLED … after report=…` / `SETTLED …` | 1 / 0 | same |
| C5 | dispatch marker on disk, uncommitted | `UNSETTLED w1 no committed results and no carried-to marker` | **1** | `usage: no committed <wave>.ready.dispatched …`, exit **2** |
| C6 | ` ABANDONED:` on line 1 / on line 2 of the marker | `ABANDONED w1` / `UNSETTLED w1` | 0 / 1 | same semantics |
| C7 | `w1-results.json` renamed to `.bak`, marker present / absent | `UNSETTLED w1 …` / `usage: no wave artifacts` | 1 / 2 | — |
| C8 | `55/w2 → 56/w2 → 55/w2` | `UNSETTLED w2 carried-to 56/w2: UNSETTLED w2 carried-to cycle 56/w2 -> 55/w2` | 1 | — |
| C9 | results `01:26:01-03:00` vs report `04:30:00+00:00` (4 min **before**, mixed offsets) / `01:35:00-03:00` (5 min **after**) | `SETTLED` / `UNSETTLED … after report=2026-10-27T04:30:00+00:00` | 0 / 1 | same |
| C10 | report added, deleted, re-added after results | `UNSETTLED w1 results=…05:00 after report=…01:00` (`--diff-filter=A` printed `07:00` then `01:00`) | 1 | same |
| C11 | chain `55/w2 → 56/w3 → 57/w1` (settled) | `CARRIED w2 -> 56/w3 (carried)`; mid-chain `CARRIED w3 -> 57/w1 (settled)` | 0 | — |
| C12 | `carried over: 56/w1` (malformed) / `w2.carried-to` on disk uncommitted | `UNSETTLED w2 carried-to marker malformed: 'carried over: 56/w1'` / `UNSETTLED w2 carried-to 56/w1: UNSETTLED w1 …` | 1 | — |

Every exit-0 case has a case that fails the same arm (C1↔C3/C2, C9-before↔C9-after, C11↔C8), so no arm
is green by construction.

## 5. Real repositories, old vs proposed (unchanged where the old check was right)

| round | shipped check | proposed v2 |
|---|---|---|
| 52 | `SETTLED w1`, `SETTLED w2`, 0 | identical, 0 |
| 53 | `SETTLED w1`, `ABANDONED w2`, 0 | same verdicts (`ABANDONED w2 (marker: …)`), 0 |
| 54 | `UNSETTLED w2 results=…00:22:58 after report=…23:50:07`, 1 | identical, 1 |
| 55 | `UNSETTLED w1 …`, `WAVES=1 SETTLED=0`, 1 | `UNSETTLED w1 …` **and** `UNSETTLED w2 no committed results and no carried-to marker`, `WAVES=2 SETTLED=0`, 1 |
| 56 | usage, 2 | usage, 2 without `--before-filing` (no report commit); `UNSETTLED w1 no committed results and no carried-to marker`, `WAVES=1 SETTLED=0`, **1** with it |

## 6. Residuals and risks (disclosed, not patched)

- **R1 renamed-out artifacts** (C7b): when every artifact of a wave is renamed off the suffixes the wave
  disappears and the run is exit 2, never exit 0 — not a false green, but `WAVES=` under-counts. A
  `.bak`/`.orig` sibling is still a lane file; a future version could widen `PAT` to
  `<wave>{-results.json,.ready}{.*}` if the lane wants that class counted.
- **R2 add/delete/re-add** (C10): `at()` keeps the **earliest** add (`git log` newest-first, `out[-1]`),
  so re-filing a report after results cannot clear the red — same behaviour as the shipped check, kept
  deliberately; the escape hatch is `--before-filing`, not a re-add.
- **R3 carried target clock**: a carried target is judged with `filed=None`; its own round's run applies
  its report clock. A carry into a round whose directory does not exist yet nests the reason (C12b) —
  correct, ugly.
- **R4 what this does not fix**: the lane still has no machine record of round 55's carry. Landing
  `.ufo/waves/round-55/w2.carried-to` with `carried-to: 56/w1` would make the proposal see it
  (`CARRIED w2 -> 56/w1`); without that marker round 55 stays red on `w2` — which is the honest reading.
  That is a lane write and belongs to the L1, not this seat.
- No lane file, no counter, no probe was touched; the C1/C2 battery and probes are untouched by this seat.
- Overlap: the never-dispatched round-55 W2 item at `.ufo/waves/round-55/gen-w2-spec.py:120` attacks this
  same script with a superset of C4/C5/C7/C9/C10. Cases C1-C3, C6, C8, C11, C12 are new here; the L1
  can credit or dedupe, and I claim no round-55 W2 credit.

VERDICT: attacked the shipped round-55 `wave-settled-check.py` on rounds 55/56 and on the retired/carried
class — its 54/55 verdicts survive but round 56 is falsified (exit 2 usage, not `UNSETTLED`) and a
prepared-never-dispatched wave is silently dropped (`WAVES=1` for round 55); the 60-line successor
survives all 12 fixture cases and reproduces rounds 52-56, so the defect is a missing branch, not a
missing capability.
