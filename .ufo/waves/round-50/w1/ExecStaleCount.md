# ExecStaleCount — r50 w1: `stale-count-check.py`, a prose-count ↔ receipt gate

Seat ExecStaleCount (leaf, no dispatch). Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`
at HEAD `775417271bcae0ff642133f32b2d5388b1b2339b`. Scratch
`/dev/shm/chousa-r50-ExecStaleCount/` (3.3M, deleted; `ls` → `No such file or directory`).
Lane bytes untouched by me: `git status --porcelain` before and after my run is identical
(` M .ufo/waves/round-49/w2/ScoutPlanned.md` plus the same untracked round-50 paths); only lane
write is this report. No network, no live fetch, no production file, no tool installs (pacman is
host-paused; none was needed). Closes the round-49 routed defect **"stale quote counts (28 vs 31)"**.

## Usage line

```
python3 corpus/evidence/round50/stale-count-check.py [--root REPO] [--receipt TSV]
```

Default `--root` is `Path(__file__).resolve().parents[3]` (the lane root once the file lands at
`corpus/evidence/round50/stale-count-check.py`); default receipt `<root>/corpus/evidence/round49/spans.tsv`.
Exit 0 = no unresolved hit, 1 = an unresolved stale hit, 2 = missing input/usage.

## Script (intended lane path `corpus/evidence/round50/stale-count-check.py`, 79 lines)

```python
#!/usr/bin/env python3
"""stale-count — fail when a count in lane prose disagrees with its receipt.

Counts checked: `QUOTES=<n>`, `<n>-row manifest`, `<n> located quotes`,
`CAPTURE_BOUND=<n>/<n>`, in corpus/QUALITY.md, corpus/README.md and LOG.md,
against the data rows of corpus/evidence/round49/spans.tsv (header excluded).

A hit is resolved only by a LATER line in the SAME file reading
`correction: ... superseded by ...` and naming the stale line (`LOG.md:1803`,
`line 1803`): LOG.md is append-only, so a correction entry closes a line; it may
quote the value it supersedes, not a new disagreeing one.

Usage: python3 corpus/evidence/round50/stale-count-check.py [--root REPO] [--receipt TSV]
Exit:  0 no unresolved hit · 1 an unresolved stale hit · 2 usage/missing input.
"""
import argparse, pathlib, re, sys

PROSE = ("corpus/QUALITY.md", "corpus/README.md", "LOG.md")
PATTERNS = (re.compile(r"QUOTES=(\d+)"), re.compile(r"(\d+)-row manifest"),
            re.compile(r"(\d+) located quotes"), re.compile(r"CAPTURE_BOUND=(\d+)/\1"))
CORRECTION = re.compile(r"correction:.*superseded by")
NAMES = re.compile(r"(?::|line\s+)(\d+)\b")


def receipt_rows(path: pathlib.Path) -> int:
    rows = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return len(rows) - (1 if rows and rows[0].startswith("id\t") else 0)


def said(text: str, m: int) -> list[int]:
    ns = [int(mo.group(1)) for pat in PATTERNS for mo in pat.finditer(text)]
    return [n for i, n in enumerate(ns) if n != m and n not in ns[:i]]


def scan(lines: list[str], m: int) -> list[tuple[int, int, bool]]:
    """[(lineno, disagreeing number, resolved)] over every count form."""
    nums = [said(t, m) for t in lines]
    named = {j: {int(x) for x in NAMES.findall(t)}
             for j, t in enumerate(lines, 1) if CORRECTION.search(t)}
    quoted = {j: {n for k in ns if 1 <= k <= len(lines) for n in nums[k - 1]}
              for j, ns in named.items()}
    out: list[tuple[int, int, bool]] = []
    for i, ns in enumerate(nums, 1):
        if i in named:
            out += [(i, n, n in quoted[i]) for n in ns]
        elif ns:
            ok = any(j > i and i in named[j] and set(nums[j - 1]) <= quoted[j] for j in named)
            out += [(i, n, ok) for n in ns]
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None, help="lane repo root (default: this script's repo)")
    ap.add_argument("--receipt", default=None, help="span manifest (default: round-49 spans.tsv)")
    args = ap.parse_args(argv)
    root = pathlib.Path(args.root) if args.root else pathlib.Path(__file__).resolve().parents[3]
    receipt = pathlib.Path(args.receipt) if args.receipt else root / "corpus/evidence/round49/spans.tsv"
    if not receipt.is_file():
        print(f"RECEIPT_MISSING {receipt}")
        return 2
    m = receipt_rows(receipt)
    hits = unresolved = 0
    for rel in PROSE:
        path = root / rel
        if not path.is_file():
            print(f"PROSE_MISSING {rel}")
            return 2
        for lineno, n, ok in scan(path.read_text(encoding="utf-8").splitlines(), m):
            hits += 1
            unresolved += not ok
            print(f"{'RESOLVED' if ok else 'STALE'} {rel}:{lineno} says {n}, receipt {m}")
    print(f"STALE_HITS={hits} UNRESOLVED={unresolved} RECEIPT_ROWS={m}")
    print("STALE_COUNT=" + ("PASS" if not unresolved else "FAIL"))
    return 1 if unresolved else 0


if __name__ == "__main__":
    sys.exit(main())
```

## Receipt (31), and that the receipt is the right one

```
$ awk 'NR>1' corpus/evidence/round49/spans.tsv | wc -l
31
$ sha256sum corpus/evidence/round49/spans.tsv
96bc0bebcacf8a880736cdace6dd24d1a74645af7509c4068c21878d41a06472  corpus/evidence/round49/spans.tsv
$ python3 corpus/evidence/round49/c2-count.py | grep -E 'QUOTE_ROWS|CAPTURE_BOUND|C2='
QUOTE_ROWS=31 ON_BOUND=31/31
CAPTURE_BOUND=31/31
C2=PASS                                  (exit 0)
$ python3 corpus/evidence/round49/quote-substance-check.py
IDS=8 QUOTES=31 FAILURES=0               (exit 0)
```

`spans.tsv` is 32 lines = `id url capture_sha256 offset span_file quote entry` header + 31 rows;
the frozen counter's `QUOTE_ROWS=31`/`CAPTURE_BOUND=31/31` and the committed
`measure-after.txt:45`/`:78` agree, so 31 is the receipt, not my recomputation. The three prose
sites still say 28.

## Shown able to fail — the three unresolved hits on the CURRENT lane

```
$ python3 /dev/shm/.../stale-count-check.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin
STALE corpus/QUALITY.md:746 says 28, receipt 31
STALE corpus/README.md:1074 says 28, receipt 31
STALE LOG.md:1803 says 28, receipt 31
STALE_HITS=3 UNRESOLVED=3 RECEIPT_ROWS=31
STALE_COUNT=FAIL
EXIT=1
```

Line 1803 carries two forms on one line (`28 located quotes`, `CAPTURE_BOUND=28/28`), both 28, so
it is reported once. The committed round-49 spotcheck names the same three sites
(`corpus/lessons/round-49-verifier-spotcheck.md:96`), so the scan set covers the defect as routed.

## Shown able to pass — correction simulated on a scratch copy

Scratch lane = copies of `corpus/QUALITY.md`, `corpus/README.md`, `LOG.md` and
`corpus/evidence/round49/spans.tsv`; all four `sha256sum` matched the lane before appending
(`COPY_OK`; e.g. `spans.tsv 96bc0beb…`). One `correction: … superseded by …` line appended to
each file, naming its own stale line:

```
$ python3 stale-count-check.py --root /dev/shm/chousa-r50-ExecStaleCount/lane
RESOLVED corpus/QUALITY.md:746 says 28, receipt 31
RESOLVED corpus/README.md:1074 says 28, receipt 31
RESOLVED LOG.md:1803 says 28, receipt 31
RESOLVED LOG.md:1809 says 28, receipt 31
STALE_HITS=4 UNRESOLVED=0 RECEIPT_ROWS=31
STALE_COUNT=PASS
EXIT=0
```

`LOG.md:1809` is the appended correction line itself; it quotes `CAPTURE_BOUND=28/28` while
superseding it, so it resolves as a quotation of the superseded value rather than a new claim.

## Falsifiers (each a scratch mutation of the same fixture; script unchanged)

| Leg | Mutation | Result |
|---|---|---|
| m1 | receipt trimmed to 28 data rows | `STALE_HITS=0 … RECEIPT_ROWS=28 STALE_COUNT=PASS`, exit 0 — verdict tracks the receipt, not a hardcoded 31 (the mirror case, prose 31 vs receipt 31, is the same `n != m` comparison) |
| m2 | correction names `LOG.md:1804` | `STALE LOG.md:1803 says 28`, exit 1 — naming is required |
| m3 | correction names 1803 but says `29-row manifest` | `STALE LOG.md:1809 says 29, receipt 31`, exit 1 — a correction may not smuggle a new disagreeing value |
| m4 | correction naming `corpus/QUALITY.md:746` appended to `corpus/README.md` | `STALE corpus/QUALITY.md:746`, exit 1 — same-file rule |
| m5 | LOG:1803 edited to `CAPTURE_BOUND=27/27` only | `STALE LOG.md:1803 says 27`, exit 1 — the `CAPTURE_BOUND=<n>/<n>` leg fires on its own, and the backreference leaves the pre-repair `CAPTURE_BOUND=21/28` on the same line unmatched |
| base2 | pristine copy, script at `corpus/evidence/round50/`, no `--root` | `STALE` ×3, exit 1 — default root resolves to `parents[3]` correctly |
| usage | `--receipt /dev/shm/…/nope.tsv` | `RECEIPT_MISSING …`, exit 2 |

## Calibration — limits and one located gap

1. **The idiom is pinned, case-sensitive and single-line.** My first simulation wrote
   `Correction (2026-10-25): … superseded by …` and the gate did **not** accept it (`STALE
   corpus/QUALITY.md:746` / `README.md:1074` remained, exit 1) — it fails closed; the accepted form
   is exactly `correction: … superseded by …` on one line.
2. **F1 (gap, outside the pinned scan set).** `corpus/lessons/round-49.md:20` carries a fourth
   `QUOTES=28` ("on this round's manifest `IDS=8 QUOTES=28 FAILURES=0`, exit 0"). The scan set is
   pinned to three files, so the script does not report it — but fixing only the three leaves that
   transcript stale. One-tuple edit if the L1 wants it: `PROSE = (…, "corpus/lessons/round-49.md")`
   (prints 4 hits on the current lane). Round-49 seat reports under `.ufo/waves/round-49/` (e.g.
   `w1/MutSpans.md:22`, `w2/ScribeLog.md:26` → `CAPTURE_BOUND=28/28`) are historical seat output,
   not lane prose, and stay out of scope either way.
3. **Digit forms only.** `QUOTES=eight`, `twenty-eight located quotes` and a count split over two
   lines escape; the four pinned shapes are all the gate can see.
4. **One receipt, one meaning.** Every form is compared to the manifest's data rows; `QUOTE_ROWS`,
   `CAPTURE_BOUND=31/31` and `QUOTES=31` happen to agree here, but a per-id or per-leg total from a
   future counter would be flagged as stale while being true.
5. **Direction of the fix is the L1's.** A `correction:` entry (append-only, LOG-compatible) or a
   direct rewrite to 31 both clear it — m1 shows the comparison is number-driven. What the gate
   forbids is leaving 28 in place.
6. Not attacked: the frozen round-50 C1/C2 claims (other seats own them); this gate reads only
   round-49 prose and the round-49 manifest.

VERDICT: built `corpus/evidence/round50/stale-count-check.py`; on the live lane it reports three
unresolved hits (`QUALITY.md:746`, `README.md:1074`, `LOG.md:1803`, each says 28 vs receipt 31),
exit 1; with one `correction: … superseded by …` line per file on a digest-verified scratch copy it
prints 4 `RESOLVED`, exit 0; five mutations (receipt=28, wrong name, wrong new value, other file,
`CAPTURE_BOUND` leg) each fail as designed; one located gap outside the pinned set:
`corpus/lessons/round-49.md:20` also says `QUOTES=28`.
