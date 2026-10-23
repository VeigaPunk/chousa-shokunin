#!/usr/bin/env python3
"""No-reader control: infer grouped verdicts from quote shape and cross-item overlap.

Only the two supplied text files are opened. No HTML parser, DNS, network, harness
state, receipt, filesystem enumeration, or process inspection is used. The static
prior exploits the frozen fixture's two body windows, title, script, and case-flip
per source; it is deliberately not a page verifier or a contract-v2 repair.
"""
import argparse
import collections
import functools
import itertools
import re
import sys
import unicodedata

DEADLINE = 30.0
QMAP = str.maketrans({"\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'",
                      "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u201f": '"',
                      "\u00ad": None, "\u200b": None, "\u200c": None,
                      "\u200d": None, "\ufeff": None})


def inner_cap(words):
    return any(c.isupper() for word in words for c in word[1:])


def head_likelihood(words, script=False):
    """Likelihood of the observed length and initial case for a title/script window."""
    n = len(words)
    capital = bool(words and words[0][0].isupper())
    if script and capital:
        return 0.0
    total = 0.0
    for length in range(6, 11):
        upper = min(8, length)
        if not 4 <= n <= upper:
            continue
        if script:
            case = 1.0
        else:
            at_start = 1.0 / (length - n + 1)
            case = at_start if capital else 1.0 - at_start
        total += case / (5 * (upper - 3))
    return total


def body_likelihood(windows):
    """Marginalize body-block placement using only overlap and capitalization.

    Within a block, a shared pseudo-word fixes two windows' relative offsets;
    windows without a shared word must not overlap. Across blocks, words cannot
    be shared. Unknown block lengths are marginalized over 30..42 words.
    """
    lengths = [len(w) for w in windows]
    capital = [bool(w and w[0][0].isupper()) for w in windows]
    lower = [tuple(word.casefold() for word in w) for w in windows]
    sets = [set(w) for w in lower]
    relations = {}
    for a, b in itertools.combinations(range(3), 2):
        shared = sets[a] & sets[b]
        if not shared:
            relations[a, b] = None
            continue
        delta = lower[a].index(next(iter(shared))) - lower[b].index(next(iter(shared)))
        lo, hi = max(0, delta), min(lengths[a], delta + lengths[b])
        if lo >= hi or any(lower[a][k] != lower[b][k - delta] for k in range(lo, hi)):
            return 0.0
        if any(lower[a].index(word) - lower[b].index(word) != delta for word in shared):
            return 0.0
        relations[a, b] = delta

    def allowed_pair(a, sa, b, sb):
        if a > b:
            return allowed_pair(b, sb, a, sa)
        delta = relations[a, b]
        if delta is not None:
            return sb - sa == delta
        return sa + lengths[a] <= sb or sb + lengths[b] <= sa

    @functools.lru_cache(maxsize=None)
    def same_block(indices):
        total = 0.0
        for length in range(30, 43):
            starts = {i: ([0] if capital[i] else range(1, length - lengths[i] + 1))
                      for i in indices}
            denominator = 1
            for i in indices:
                denominator *= length - lengths[i] + 1
            if len(indices) == 1:
                count = len(starts[indices[0]])
            elif len(indices) == 2:
                a, b = indices
                count = sum(allowed_pair(a, sa, b, sb)
                            for sa in starts[a] for sb in starts[b])
            else:
                a, b, c = indices
                # Third-start compatibility is a bitset, not a cubic position loop.
                masks_a = {sa: sum(1 << sc for sc in starts[c] if allowed_pair(a, sa, c, sc))
                           for sa in starts[a]}
                masks_b = {sb: sum(1 << sc for sc in starts[c] if allowed_pair(b, sb, c, sc))
                           for sb in starts[b]}
                count = sum((masks_a[sa] & masks_b[sb]).bit_count()
                            for sa in starts[a] for sb in starts[b]
                            if allowed_pair(a, sa, b, sb))
            total += count / denominator / 13
        return total

    partitions = [(((0, 1, 2),), 13.0 / 72),
                  (((0, 1), (2,)), 17.0 / 72),
                  (((0, 2), (1,)), 17.0 / 72),
                  (((1, 2), (0,)), 17.0 / 72),
                  (((0,), (1,), (2,)), 1.0 / 9)]
    total = 0.0
    for groups, prior in partitions:
        owners = {i: k for k, group in enumerate(groups) for i in group}
        if any(delta is not None and owners[a] != owners[b]
               for (a, b), delta in relations.items()):
            continue
        term = prior
        for group in groups:
            term *= same_block(group)
        total += term
    return total


def grouped_guesses(group):
    """Choose two body candidates by posterior marginals, never from page bytes."""
    flips = [i for i, (_, _, words) in enumerate(group) if inner_cap(words)]
    if len(group) != 5 or len(flips) != 1:
        return {item_id: ("VERBATIM" if len(words) > 8 and not inner_cap(words) else "ABSENT")
                for item_id, _, words in group}
    flip = flips[0]
    rest = [i for i in range(5) if i != flip]
    masses = [0.0] * 5
    total = 0.0
    for body in itertools.combinations(rest, 2):
        if any(not 6 <= len(group[i][2]) <= 15 for i in body):
            continue
        absent = [i for i in rest if i not in body]
        body_group = body + (flip,)
        # A title/script word cannot also be a body word or belong to the other head window.
        token_sets = [set(word.casefold() for word in item[2]) for item in group]
        if any(token_sets[i] & token_sets[j] for i in absent for j in range(5) if i != j):
            continue
        head = sum(head_likelihood(group[t][2]) * head_likelihood(group[s][2], script=True)
                   for t, s in (absent, absent[::-1]))
        if not head:
            continue
        weight = head * body_likelihood([group[i][2] for i in body_group])
        total += weight
        for i in body:
            masses[i] += weight
    if not total:
        return {item_id: ("VERBATIM" if len(words) > 8 and not inner_cap(words) else "ABSENT")
                for item_id, _, words in group}
    chosen = set(sorted(rest, key=lambda i: (masses[i], len(group[i][2]), group[i][0]), reverse=True)[:2])
    return {item_id: ("VERBATIM" if i in chosen else "ABSENT")
            for i, (item_id, _, _) in enumerate(group)}


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
    groups = collections.defaultdict(list)
    guesses = {}
    for line in lines[1:]:
        if not line:
            continue
        item_id, sid, quote = line.split("\t", 2)
        words = unicodedata.normalize("NFKC", quote).translate(QMAP).split()
        item = (item_id, sid, words)
        items.append(item)
        if not re.search(r"https?://\S+", rows.get(sid, "")):
            guesses[item_id] = "NO_SOURCE"
        elif len(words) > 25:
            guesses[item_id] = "TOO_LONG"
        else:
            groups[sid].append(item)
    for group in groups.values():
        if len(group) >= 4:
            guesses.update(grouped_guesses(group))
        else:
            guesses.update((item_id, "UNREACHABLE") for item_id, _, _ in group)
    counts = dict.fromkeys(("VERBATIM", "ABSENT", "TOO_LONG", "NO_SOURCE", "UNREACHABLE"), 0)
    for item_id, _, _ in items:
        verdict = guesses[item_id]
        counts[verdict] += 1
        print("QUOTE_REOPEN\t%s\t%s\tno-reader relational guess; no DNS or fetch" % (item_id, verdict))
    print("QUOTE_REOPEN_SUMMARY " + " ".join("%s=%d" % (key.lower(), value) for key, value in counts.items()))
    return 0 if sum(counts.values()) == counts["VERBATIM"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
