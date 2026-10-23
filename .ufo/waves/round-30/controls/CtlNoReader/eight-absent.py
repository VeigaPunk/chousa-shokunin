#!/usr/bin/env python3
"""No-reader control: grouped length/case guesses; singleton eight-word quotes ABSENT."""
import argparse
import collections
import re
import sys
import unicodedata

DEADLINE = 30.0
QMAP = str.maketrans({"\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'",
                      "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u201f": '"',
                      "\u00ad": None, "\u200b": None, "\u200c": None,
                      "\u200d": None, "\ufeff": None})


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["verify"])
    ap.add_argument("--items", required=True)
    ap.add_argument("--registry", required=True)
    args = ap.parse_args(argv)
    rows = {}
    with open(args.registry, encoding="utf-8") as f:
        for line in f:
            cells = line.split("|")
            if line.startswith("| ") and len(cells) >= 4:
                rows.setdefault(cells[1].strip(), cells[2])
    with open(args.items, encoding="utf-8") as f:
        lines = f.read().splitlines()
    if not lines or lines[0] != "id\tsource_id\tquote":
        return 2
    items = []
    group_sizes = collections.Counter()
    for line in lines[1:]:
        if not line:
            continue
        item_id, sid, quote = line.split("\t", 2)
        words = unicodedata.normalize("NFKC", quote).translate(QMAP).split()
        items.append((item_id, sid, words))
        if len(words) <= 25:
            group_sizes[sid] += 1
    counts = dict.fromkeys(("VERBATIM", "ABSENT", "TOO_LONG", "NO_SOURCE", "UNREACHABLE"), 0)
    for item_id, sid, words in items:
        if not re.search(r"https?://\S+", rows.get(sid, "")):
            verdict = "NO_SOURCE"
        elif len(words) > 25:
            verdict = "TOO_LONG"
        elif group_sizes[sid] < 4:
            verdict = "ABSENT" if len(words) == 8 else "UNREACHABLE"
        elif any(c.isupper() for word in words for c in word[1:]):
            verdict = "ABSENT"
        else:
            verdict = "VERBATIM" if len(words) > 8 else "ABSENT"
        counts[verdict] += 1
        print("QUOTE_REOPEN\t%s\t%s\tno-reader eight-word guess; no DNS or fetch" % (item_id, verdict))
    print("QUOTE_REOPEN_SUMMARY " + " ".join("%s=%d" % (key.lower(), value) for key, value in counts.items()))
    return 0 if sum(counts.values()) == counts["VERBATIM"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
