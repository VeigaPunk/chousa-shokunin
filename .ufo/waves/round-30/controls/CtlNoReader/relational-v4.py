#!/usr/bin/env python3
"""No-reader v4 control: posterior over two body/two head/one case-flip roles.

Only supplied registry/items files are opened. This exploits remaining item-only
priors (head/body start capitalization, length sampling, case-toggle grammar),
and any overlap with supplied overlong quotes. It never parses a page, resolves
DNS, connects, reads harness state, or implements contract v2 items 1-3.
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


def base_case_probability(words, starts_run):
    """Case probability under the fixture's original word generator, not a page."""
    if not words or bool(words[0][0].isupper()) != bool(starts_run):
        return 0.0
    probability = 1.0
    for i, word in enumerate(words):
        if i and word[0].isupper():
            return 0.0
        capitals = sum(c.isupper() for c in word[1:])
        if capitals == 0:
            probability *= 0.85
        elif capitals == 1:
            probability *= 0.15 / (len(word) - 1)
        else:
            return 0.0
    return probability


@functools.lru_cache(maxsize=None)
def role_likelihoods(words):
    """Marginalize ordinary and one-case-toggle spellings over latent run starts."""
    n = len(words)
    if not 6 <= n <= 12:
        return (0.0, 0.0, 0.0)
    plain = [base_case_probability(words, start) for start in (False, True)]
    flip = [0.0, 0.0]
    for k, word in enumerate(words):
        for pos, char in enumerate(word):
            if not char.isalpha():
                continue
            restored = list(words)
            restored[k] = word[:pos] + char.swapcase() + word[pos + 1:]
            for start in (False, True):
                flip[start] += base_case_probability(restored, start) / (n * len(word))
    body_cap = sum(1.0 / (length - n + 1) for length in range(50, 61)) / 11
    body = ((1 - body_cap) * plain[0] + body_cap * plain[1]) / 7
    changed = ((1 - body_cap) * flip[0] + body_cap * flip[1]) / 7
    head = 0.0
    for length in range(10, 15):
        upper = min(12, length)
        if n > upper:
            continue
        cap = 1.0 / (length - n + 1)
        head += ((1 - cap) * plain[0] + cap * plain[1]) / (5 * (upper - 5))
    return body, head, changed


def posterior_guesses(group, long_quotes):
    if len(group) != 5:
        return {item_id: "ABSENT" for item_id, _, _ in group}
    likelihoods = [role_likelihoods(tuple(words)) for _, _, words in group]
    anchor = collections.defaultdict(set)
    for words in long_quotes:
        for word in words:
            anchor[word.casefold()].add(word)
    must_be_body_derived = []
    must_be_flip = []
    for _, _, words in group:
        shared = [word for word in words if word.casefold() in anchor]
        must_be_body_derived.append(bool(shared))
        must_be_flip.append(any(word not in anchor[word.casefold()] for word in shared))
    masses = [0.0] * 5
    total = 0.0
    for changed in range(5):
        remaining = [i for i in range(5) if i != changed]
        for body in itertools.combinations(remaining, 2):
            head = [i for i in remaining if i not in body]
            if any(must_be_body_derived[i] for i in head):
                continue
            if any(must_be_flip[i] and i != changed for i in range(5)):
                continue
            weight = likelihoods[changed][2]
            for i in body:
                weight *= likelihoods[i][0]
            for i in head:
                weight *= likelihoods[i][1]
            total += weight
            for i in body:
                masses[i] += weight
    # Per-item posterior > 1/2 maximizes expected score; no source truth is observed.
    return {item_id: ("VERBATIM" if total and masses[i] > total / 2 else "ABSENT")
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
    long_quotes = collections.defaultdict(list)
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
            long_quotes[sid].append(words)
        else:
            groups[sid].append(item)
    for sid, group in groups.items():
        if len(group) >= 4:
            guesses.update(posterior_guesses(group, long_quotes[sid]))
        else:
            guesses.update((item_id, "UNREACHABLE") for item_id, _, _ in group)
    counts = dict.fromkeys(("VERBATIM", "ABSENT", "TOO_LONG", "NO_SOURCE", "UNREACHABLE"), 0)
    for item_id, _, _ in items:
        verdict = guesses[item_id]
        counts[verdict] += 1
        print("QUOTE_REOPEN\t%s\t%s\tno-reader v4 posterior guess; no DNS or fetch" % (item_id, verdict))
    print("QUOTE_REOPEN_SUMMARY " + " ".join("%s=%d" % (key.lower(), value) for key, value in counts.items()))
    return 0 if sum(counts.values()) == counts["VERBATIM"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
