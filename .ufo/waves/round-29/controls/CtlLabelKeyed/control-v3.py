#!/usr/bin/env python3
"""No-fetch shortcut using frozen committed labels and batch transpose contrasts.

Unknown paired quotes are oriented by receipt-derived n-gram evidence, not by
checking source pages. No labels from this evaluation or uncommitted receipts
are loaded. This is deliberately not a source verifier.
"""
import argparse
import csv
import json
import math
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
REVISION = "aa5e1a3187955fa923de14e11c150bf1c526efc6"
FIXTURE = LANE / "corpus/fixtures/quote-reopen-r29"
HINTS = {tuple(s.split()) for s in (
    "of the", "in the", "to the", "on the", "as a", "is a", "this is",
    "can be", "may be", "must be", "will be", "should be", "for the",
    "with the", "that the", "and the", "are the", "from the", "does not",
    "not be", "if the", "it is", "there is", "such as", "more than",
    "less than", "as well", "well as", "by the", "a new", "the same",
)}


def git(*args):
    return subprocess.run(
        ["timeout", "10s", "git", *args], cwd=LANE, capture_output=True,
        text=True, check=True, timeout=12,
    ).stdout


def rows(path):
    with open(path, encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def grams(tokens, n):
    return [tokens[i:i + n] for i in range(len(tokens) - n + 1)]


def transposed(a, b):
    changes = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
    return (
        len(a) == len(b) and len(changes) == 2
        and changes[1] == changes[0] + 1
        and a[changes[0]] == b[changes[1]]
        and a[changes[1]] == b[changes[0]]
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--items", required=True)
    args = parser.parse_args()
    keyed = {}
    truths = set()
    positives = defaultdict(set)

    def remember(sid, quote, label):
        keyed[sid, quote] = label
        if label in {"VERBATIM", "TOO_LONG"}:
            tokens = tuple(quote.split())
            truths.add((sid, tokens))
            positives[sid].add(tokens)

    labels = {r["id"]: r["label"] for r in rows(FIXTURE / "labels.tsv")}
    for row in rows(FIXTURE / "items.tsv"):
        remember(row["source_id"], row["quote"], labels[row["id"]])
    names = git("ls-tree", "-r", "--name-only", REVISION, "--", ".ufo").splitlines()
    receipt_names = [name for name in names if (
        Path(name).suffix == ".json"
        and (Path(name).name.startswith("receipt")
             or Path(name).name.startswith("before-do-nothing"))
    )]
    for name in receipt_names:
        receipt = json.loads(git("show", f"{REVISION}:{name}"))
        for case in receipt.get("cases", ()):
            if {"source_id", "quote", "label"} <= case.keys():
                remember(case["source_id"], case["quote"], case["label"])

    frequencies = {n: Counter() for n in range(2, 5)}
    for sid, tokens in truths:
        lower = tuple(t.lower() for t in tokens)
        for n, counts in frequencies.items():
            counts.update(grams(lower, n))
    positive_bags = defaultdict(list)
    for sid, tokens in truths:
        positive_bags[sid, tuple(sorted(tokens))].append(tokens)
    contrast = {n: Counter() for n in range(2, 5)}
    for (sid, quote), label in keyed.items():
        if label != "ABSENT":
            continue
        bad = tuple(quote.split())
        for good in positive_bags.get((sid, tuple(sorted(bad))), ()):
            if not transposed(good, bad):
                continue
            g, b = tuple(t.lower() for t in good), tuple(t.lower() for t in bad)
            for n, counts in contrast.items():
                delta = Counter(grams(g, n))
                delta.subtract(grams(b, n))
                counts.update(delta)

    def score(tokens):
        lower = tuple(t.lower() for t in tokens)
        return sum(
            (n - 1) ** 2 * (
                math.log1p(frequencies[n][gram])
                + 0.3 * contrast[n][gram]
                + (0.3 if gram in HINTS else 0)
            )
            for n in frequencies for gram in grams(lower, n)
        )

    incoming = rows(args.items)
    answers, details = {}, {}
    groups = defaultdict(dict)
    for row in incoming:
        rid, sid, quote = row["id"], row["source_id"], row["quote"]
        tokens = tuple(quote.split())
        verdict = keyed.get((sid, quote))
        if verdict is not None:
            answers[rid], details[rid] = verdict, "committed-label-key"
        elif any(
            known[start:start + len(tokens)] == tokens
            for known in positives.get(sid, ())
            for start in range(len(known) - len(tokens) + 1)
        ):
            answers[rid], details[rid] = "VERBATIM", "committed-positive-token-span"
        groups[sid, tuple(sorted(tokens))].setdefault(tokens, []).append(rid)

    for group in groups.values():
        if len(group) != 2:
            continue
        first, second = group
        if not transposed(first, second):
            continue
        left, right = group[first], group[second]
        known_left = {answers[rid] for rid in left if rid in answers}
        known_right = {answers[rid] for rid in right if rid in answers}
        if known_left == {"VERBATIM"} or known_right == {"ABSENT"}:
            winner = 0
        elif known_right == {"VERBATIM"} or known_left == {"ABSENT"}:
            winner = 1
        else:
            scores = score(first), score(second)
            if scores[0] == scores[1]:
                continue
            winner = int(scores[1] > scores[0])
        for side, ids in enumerate((left, right)):
            for rid in ids:
                if rid not in answers:
                    answers[rid] = "VERBATIM" if side == winner else "ABSENT"
                    details[rid] = "paired-transpose-contrast-guess"

    counts = Counter()
    for row in incoming:
        rid = row["id"]
        verdict = answers.get(rid, "ABSENT")
        detail = details.get(rid, "unknown-key-default-absent")
        counts[verdict] += 1
        print(f"QUOTE_REOPEN\t{rid}\t{verdict}\t{detail}; no page fetched by control")
    print("QUOTE_REOPEN_SUMMARY " + " ".join(
        f"{label.lower()}={counts[label]}"
        for label in ("VERBATIM", "ABSENT", "TOO_LONG", "NO_SOURCE", "UNREACHABLE")
    ))
    return 1 if any(counts[label] for label in counts if label != "VERBATIM") else 0


if __name__ == "__main__":
    raise SystemExit(main())
