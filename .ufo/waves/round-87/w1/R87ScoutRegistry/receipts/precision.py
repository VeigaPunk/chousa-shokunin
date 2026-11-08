#!/usr/bin/env python3
"""R87ScoutRegistry — vocabulary precision probe for DATE_TERMS / CONTRAST.

Measures:
  1. substring over-fire: rows whose teaches contains a DATE_TERM only as a
     morphological neighbour ("unpublished" contains "published").
  2. word-sense over-fire: rows whose teaches contains a DATE_TERM in a
     non-date-property sense (verb "modified", "created claims").
  3. under-fire: live rows whose teaches states a contrast against a date
     PROPERTY concept the counter's 6-literal DATE_TERMS list cannot see.
"""
import hashlib
import json
import os
import re

ROOT = "/fast/scratch/hyaku/chousa-r87/R87ScoutRegistry/tree"
CONTRAST = ("separate from", "no comparison", "independent of", "distinct from")
WIDE = CONTRAST + ("rather than", "not the same as", "other date properties")
DATE_TERMS = ("publication", "published", "modified", "modification", "created", "issued")

reg = {}
for ln in open(os.path.join(ROOT, "corpus", "SOURCES.md"), encoding="utf-8"):
    m = re.match(r"^ {0,3}\| (S\d{3,}) \|(.+)\|$", ln.rstrip("\n"))
    if not m:
        continue
    c = [x.strip() for x in ln.strip().strip("|").split("|")]
    if len(c) == 11:
        reg[c[0]] = c

sup_by = {}
for sid in sorted(reg):
    m = re.match(r"supersedes (S\d{3,}) —", reg[sid][6])
    if m:
        sup_by.setdefault(m.group(1), []).append(sid)

out = {}

# 1. substring over-fire: DATE_TERM found inside a longer word
neighbours = {
    "published": ["unpublished", "republished", "prepublished"],
    "publication": ["republication", "publications"],
    "modified": ["unmodified", "remodified"],
    "modification": ["modifications"],
    "created": ["uncreated"],
    "issued": ["reissued", "issued"],
}
sub_over = []
for sid in sorted(reg):
    tl = reg[sid][6].lower()
    words = set(re.findall(r"[a-z]+", tl))
    for t in DATE_TERMS:
        for nb in neighbours.get(t, []):
            if nb in words:
                sub_over.append({"sid": sid, "term": t, "word": nb,
                                 "contrast_in_teaches": [c for c in WIDE if c in tl],
                                 "status": reg[sid][7], "teaches": reg[sid][6]})
out["substring_overfire_rows"] = sub_over

# 1b. which of those would the counter actually CHECK (contrast phrase present)
out["substring_overfire_counter_checked"] = [r for r in sub_over if r["contrast_in_teaches"]]

# 2. word-sense over-fire: DATE_TERM present but no date-property sense
sense_rows = []
for sid in sorted(reg):
    tl = reg[sid][6].lower()
    named = [t for t in DATE_TERMS if t in tl]
    if not named:
        continue
    if not any(c in tl for c in WIDE):
        continue
    # date-property sense markers that the counter's list implies
    prop_sense = ("date", "dates", "timestamp", "property", "properties")
    has_prop = any(p in tl for p in prop_sense)
    sense_rows.append({"sid": sid, "status": reg[sid][7], "named": named,
                       "has_date_property_word": has_prop,
                       "superseded_by": sup_by.get(sid, []),
                       "teaches": reg[sid][6]})
out["date_term_rows_with_contrast"] = sense_rows

# 3. under-fire: live rows whose teaches states a contrast against a date
#    PROPERTY concept invisible to DATE_TERMS
PROPERTY_CONCEPTS = [
    "publication date", "date of publication", "publication",
    "modification date", "date modified", "date of modification", "modified",
    "modification", "last modified", "last-modified",
    "creation date", "date created", "issued", "issue date",
    "update date", "updated", "timestamp",
    "other date properties", "date properties", "date property",
    "date fields", "date field", "date metadata",
]
under = []
for sid in sorted(reg):
    tl = reg[sid][6].lower()
    if not any(c in tl for c in WIDE):
        continue
    named = [t for t in DATE_TERMS if t in tl]
    props = [p for p in PROPERTY_CONCEPTS if p in tl]
    if not props or named:
        continue
    under.append({"sid": sid, "status": reg[sid][7],
                  "live": sid not in sup_by,
                  "superseded_by": sup_by.get(sid, []),
                  "date_property_concepts": props,
                  "counter_sees_date_term": False,
                  "teaches": reg[sid][6]})
out["underfire_property_contrast_rows"] = under

print(json.dumps(out, indent=1, ensure_ascii=False))
