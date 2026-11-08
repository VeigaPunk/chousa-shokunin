#!/usr/bin/env python3
"""R87ScoutRegistry — wide-vocabulary over/under-fire measurement, exact."""
import hashlib
import json
import os
import re

ROOT = "/fast/scratch/hyaku/chousa-r87/R87ScoutRegistry/tree"

CONTRAST = ("separate from", "no comparison", "independent of", "distinct from")
WIDE = CONTRAST + ("rather than", "not the same as", "other date properties")
DATE_TERMS = ("publication", "published", "modified", "modification", "created", "issued")
# date-property CONCEPT vocabulary (wider than the counter's DATE_TERMS)
CONCEPTS = [
    "publication date", "date of publication", "publication", "published",
    "modification date", "date modified", "date of modification", "modified",
    "modification", "last modified", "last-modified",
    "creation date", "date created", "created",
    "issue date", "issued",
    "update date", "updated", "timestamp",
    "other date properties", "date properties", "date property",
    "date fields", "date field", "date metadata", "date values", "date value",
]


def norm(s):
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"')):
        s = s.replace(a, b)
    return " ".join(s.split())


reg = {}
raw_ids = []
for ln in open(os.path.join(ROOT, "corpus", "SOURCES.md"), encoding="utf-8"):
    m = re.match(r"^ {0,3}\| (S\d{3,}) \|(.+)\|$", ln.rstrip("\n"))
    if not m:
        continue
    raw_ids.append(m.group(1))
    c = [x.strip() for x in ln.strip().strip("|").split("|")]
    if len(c) == 11:
        reg[c[0]] = c


def cap(sid):
    c = reg.get(sid)
    if not c:
        return None
    for u in re.findall(r"https?://[^\s|)>\]]+", c[1]):
        k = hashlib.sha256(u.encode()).hexdigest()[:24]
        p = os.path.join(ROOT, "corpus", "captures", k + ".txt")
        if os.path.isfile(p):
            return norm(open(p, encoding="utf-8", errors="replace").read())
    return None


def run(contrast_vocab, date_vocab, label):
    checked, flagged, unresolved = [], [], []
    for sid in sorted(reg):
        tl = reg[sid][6].lower()
        if not any(x in tl for x in contrast_vocab):
            continue
        named = [t for t in date_vocab if t in tl]
        if not named:
            continue
        checked.append(sid)
        c = cap(sid)
        miss = [t for t in named if c is None or t not in c.lower()]
        if miss:
            flagged.append((sid, miss, c is None))
    return {"label": label, "checked": checked, "flagged": flagged}


base = run(CONTRAST, DATE_TERMS, "base(counter)")
wide_c = run(WIDE, DATE_TERMS, "wide-contrast + counter-date-terms")
wide_d = run(CONTRAST, CONCEPTS, "counter-contrast + wide-date-concepts")
wide_b = run(WIDE, CONCEPTS, "wide-contrast + wide-date-concepts")

out = {
    "registry_rows": len(reg),
    "raw_id_count": len(raw_ids),
    "base": base,
    "wide_contrast_only": wide_c,
    "wide_date_only": wide_d,
    "wide_both": wide_b,
}

# which rows newly flag in wide_contrast_only vs base
bset = {f[0] for f in base["flagged"]}
out["newly_flagged_wide_contrast"] = [f for f in wide_c["flagged"] if f[0] not in bset]
out["newly_checked_wide_contrast"] = [s for s in wide_c["checked"] if s not in base["checked"]]

# which rows newly flag in wide_both vs base
out["newly_flagged_wide_both"] = [f for f in wide_b["flagged"] if f[0] not in bset]
out["newly_checked_wide_both"] = [s for s in wide_b["checked"] if s not in base["checked"]]

# capture support for every newly-flagged row
sup = []
for sid, miss, nocap in out["newly_flagged_wide_both"] + out["newly_flagged_wide_contrast"]:
    if any(s[0] == sid for s in sup):
        continue
    c = cap(sid)
    tl = reg[sid][6].lower()
    sup.append({
        "sid": sid,
        "status": reg[sid][7],
        "teaches": reg[sid][6],
        "capture_present": c is not None,
        "capture_chars": len(c) if c else 0,
        "missing_terms": miss,
        "capture_contains_missing_terms": {t: (t in c.lower()) if c else None for t in miss},
        "all_missing_terms_truly_absent": all(
            (t not in c.lower()) if c else True for t in miss),
        "contrast_phrases": [x for x in WIDE if x in tl],
        "date_concepts_in_teaches": [x for x in CONCEPTS if x in tl],
    })
out["capture_support_detail"] = sup

# the live-row latent case: rows whose teaches states a contrast against a date
# PROPERTY concept, are live (not superseded), and whose capture lacks it.
sup_by = {}
for sid in sorted(reg):
    m = re.match(r"supersedes (S\d{3,}) —", reg[sid][6])
    if m:
        sup_by.setdefault(m.group(1), []).append(sid)

live_latent = []
for sid in sorted(reg):
    tl = reg[sid][6].lower()
    hits = [x for x in WIDE if x in tl]
    if not hits:
        continue
    concepts = [x for x in CONCEPTS if x in tl]
    if not concepts:
        continue
    c = cap(sid)
    absent = [x for x in concepts if c is None or x not in c.lower()]
    live_latent.append({
        "sid": sid, "status": reg[sid][7], "superseded_by": sup_by.get(sid, []),
        "live": sid not in sup_by,
        "contrast_phrases": hits, "date_concepts": concepts,
        "capture_present": c is not None, "concepts_absent_from_capture": absent,
        "counter_date_terms_in_teaches": [t for t in DATE_TERMS if t in tl],
        "counter_checks_this_row": bool([t for t in DATE_TERMS if t in tl]),
        "teaches": reg[sid][6],
    })
out["all_wide_contrast_rows_status"] = live_latent

print(json.dumps(out, indent=1, ensure_ascii=False))
