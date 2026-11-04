#!/usr/bin/env python3
"""R78ConnectorA sibling-overlap scan (read-only, fail-closed).

Three concept classes are searched across every sibling lane's corpus/QUALITY.md:

  i    a verification harness printing an invertible answer key or a strippable
       subject identity
  ii   a receipt a child process can append to
  iii  a self-assessment registry row whose cell count does not match its header

A zero-hit class is NOT a clean verdict: it is reported as NO-EVIDENCE and the run
exits 1 (fail-closed).  Every cited quote is verified whitespace-normalised against
the lane file it names; a quote that does not resolve is UNVERIFIED and exits 1.

Usage: python3 -B scan.py --fleet DIR
Exit: 0 all classes hit and all quotes verbatim · 1 zero-hit class or unverified
      quote · 2 usage / unreadable lane file.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

CLASSES = {
    "i": [
        r"answer key", r"invertible", r"strippable", r"leak the case",
        r"memoris\w*", r"hidden-case", r"sniffer channel", r"visible fixture",
        r"drawn per run", r"randomises the fixtures per run",
    ],
    "ii": [
        r"nothing appends to it", r"tee of one observed run",
        r"unedited tee", r"append(?:ed|ing)? to (?:it|the receipt)",
        r"receipt never grants a write destination",
    ],
    "iii": [
        r"column count", r"cell count", r"cells>7", r"over-count row",
        r"nine-cell row", r"eight-cell row", r"fields=\d+",
        r"exactly one header row",
    ],
}

# (lane, id-token, quote, class) — every quote must resolve in that lane's QUALITY.md.
QUOTES = [
    ("tsukuroi-shokunin", "90",
     "A counter that holds no answer key is scored against every channel through which "
     "the scored code can see it is being watched", "i"),
    ("kengaku-shokunin", "Q38",
     "a content leg's verdict key is produced by executing the pinned source over generated "
     "end states and is stored nowhere in the counter", "i"),
    ("souji-shokunin", "Q102",
     "whose fixtures leak the case (directory names, commit messages, fixed digests) does not "
     "discriminate a tool that memorises them", "i"),
    ("mori-shokunin", "8",
     "if any encodes which scenario is running, there is a sniffer channel", "i"),
    ("kasegi-shokunin", "R39",
     "one invocation writes it once and nothing appends to it or edits it afterwards", "ii"),
    ("kaidoku-shokunin", "120",
     "a receipt never grants a write destination", "ii"),
    ("kama-shokunin", "KQ106",
     "binds the answering process by a value the tool cannot write", "ii"),
    ("mado-shokunin", "132",
     "A registry row carries the table's own column count, and the append is gated by the "
     "table's census", "iii"),
    ("kaidoku-shokunin", "117",
     "a table census declares the logical-column mapping and accepts an over-count row only "
     "for named filed paths", "iii"),
    ("kaidoku-shokunin", "111",
     "a declared inventory is not its own population", "iii"),
    ("tsukuroi-shokunin", "92",
     "A rendered table in a committed scorecard or report carries exactly one header row", "iii"),
    ("kama-shokunin", "KQ999",
     "a sentence no lane file contains at all", "iii"),
    ("kama-shokunin", "KQ112",
     "refuses a `--work` that already holds files (exit 2, `work-reused`, nothing scored)", "iii"),
]


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fleet", required=True)
    a = ap.parse_args()
    fleet = pathlib.Path(a.fleet).resolve()
    lanes = sorted(p for p in fleet.glob("*-shokunin") if (p / "corpus" / "QUALITY.md").is_file())
    if not lanes:
        print(f"scan: no lane QUALITY.md under {fleet}", file=sys.stderr)
        return 2

    texts: dict[str, str] = {}
    for lane in lanes:
        p = lane / "corpus" / "QUALITY.md"
        try:
            texts[lane.name] = p.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print(f"scan: unreadable {p}: {exc}", file=sys.stderr)
            return 2

    hits = {k: [] for k in CLASSES}
    for lane, text in texts.items():
        if lane == "chousa-shokunin":
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for cls, pats in CLASSES.items():
                if any(re.search(p, line, re.I) for p in pats):
                    ident = re.match(r"\s*(?:-\s+\*\*Row\s+)?(\d+|[A-Z]{1,3}\d+)\b", line)
                    hits[cls].append((lane, ident.group(1) if ident else "-", n,
                                      norm(line)[:110]))

    print(f"LANES={len(lanes)} SCANNED={len(texts) - 1} (chousa excluded: it is the scanned lane)")
    zero = []
    for cls in ("i", "ii", "iii"):
        print(f"CLASS={cls} hits={len(hits[cls])}")
        for lane, ident, n, head in hits[cls][:12]:
            print(f"  CLASS={cls} lane={lane} id={ident} line={n} :: {head}")
        if not hits[cls]:
            zero.append(cls)

    bad = []
    for lane, ident, quote, cls in QUOTES:
        text = texts.get(lane)
        if text is None:
            print(f"QUOTE=UNVERIFIED lane={lane} id={ident} (lane file absent)")
            bad.append((lane, ident))
            continue
        q = norm(quote)
        ok = q in norm(text)
        print(f"QUOTE={'VERBATIM' if ok else 'UNVERIFIED'} class={cls} lane={lane} id={ident} "
              f"chars={len(q)}")
        if not ok:
            bad.append((lane, ident))

    ok_all = not zero and not bad
    print(f"SIBLING_SCAN={'PASS' if ok_all else 'FAIL'} classes_hit={3 - len(zero)}/3 "
          f"zero_hit={','.join(zero) or 'none'} unverified={len(bad)}")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
