#!/usr/bin/env python3
"""build-spans.py — round-45 builder of the lane-held capture spans (D1 fix).

Reads the campaign's on-disk captures (read-only), locates each quote, and
writes into the lane: corpus/evidence/round45/spans/<id>-<n>.txt (the quote
with up to CONTEXT chars either side, cut at the capture's own bytes),
spans.tsv (id, url, capture_sha256, offset, span_file, quote, entry) and
counts.json (the seven train.json counts with the capture sha256).
Each quote must occur exactly once in its capture, or nothing is written.
"""
import hashlib
import json
import pathlib
import re
import sys

LANE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/home/vgpnk/Projects/shokunin/chousa-shokunin")
CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
EV = LANE / "corpus" / "evidence" / "round45"
FIELD = "corpus/knowledge/evidence-archive-field-policy-r41.md"
README = "https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/README.md"
PAPER = "https://arxiv.org/html/2305.13117v3"
TRAIN = "https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/data/train.json"
CONTEXT = 160
QUOTES = [
    ("S082", README, "An archive.org link for the source url"),
    ("S082", README, "Where possible, an archive.org link to the original claim url"),
    ("S083", PAPER, "we cache all pages used as evidence in the internet archive"),
    ("S083", PAPER, "Archive.org returns a 404 page for these"),
]


def cap(url):
    p = CACHE / (hashlib.sha256(url.encode()).hexdigest()[:24] + ".txt")
    return p, hashlib.sha256(p.read_bytes()).hexdigest(), p.read_text(encoding="utf-8")


def main():
    rows, spans = [], []
    seen = {}
    for sid, url, q in QUOTES:
        _, digest, text = cap(url)
        if text.count(q) != 1:
            sys.exit(f"quote not unique in capture: {q!r} count={text.count(q)}")
        i = text.find(q)
        lo, hi = max(0, i - CONTEXT), min(len(text), i + len(q) + CONTEXT)
        seen[sid] = seen.get(sid, 0) + 1
        name = f"spans/{sid}-{seen[sid]}.txt"
        spans.append((name, text[lo:hi]))
        rows.append([sid, url, digest, str(lo), name, q, FIELD])
    (EV / "spans").mkdir(parents=True, exist_ok=True)
    for name, body in spans:
        (EV / name).write_text(body, encoding="utf-8")
    head = ["id", "url", "capture_sha256", "offset", "span_file", "quote", "entry"]
    (EV / "spans.tsv").write_text("\n".join("\t".join(r) for r in [head] + rows) + "\n", encoding="utf-8")

    p, digest, text = cap(TRAIN)
    d = json.loads(text)
    ev = [a for r in d for qq in r.get("questions", []) for a in qq.get("answers", []) if "cached_source_url" in a]
    cl = [r for r in d if "cached_original_claim_url" in r]
    counts = {
        "records": len(d),
        "evidence_with_field": len(ev),
        "evidence_nonempty": sum(1 for a in ev if a["cached_source_url"]),
        "evidence_empty": sum(1 for a in ev if not a["cached_source_url"]),
        "claims_with_field": len(cl),
        "claims_nonempty": sum(1 for r in cl if r["cached_original_claim_url"]),
        "claims_empty": sum(1 for r in cl if not r["cached_original_claim_url"]),
    }
    ans = [a for r in d for qq in r.get("questions", []) for a in qq.get("answers", [])]
    wb = lambda v: isinstance(v, str) and re.match(r"^https?://web\.archive\.org/", v) is not None
    nokey = [a for a in ans if "cached_source_url" not in a]
    src = [a for a in ans if a.get("source_url")]
    real = [a for a in src if a.get("source_url") != "Metadata"]
    filled = [a["cached_source_url"] for a in ev if a["cached_source_url"]]
    extra = {
        "answers": len(ans),
        "answers_without_key": len(nokey),
        "answers_without_key_unanswerable": sum(1 for a in nokey if a.get("answer_type") == "Unanswerable"),
        "answers_with_source_url": len(src),
        "sourced_answers_without_key": sum(1 for a in src if "cached_source_url" not in a),
        "real_source_answers": len(real),
        "real_source_answers_without_key": sum(1 for a in real if "cached_source_url" not in a),
        "real_source_answers_web_archive": sum(1 for a in real if wb(a.get("cached_source_url"))),
        "filled_web_archive": sum(1 for v in filled if wb(v)),
        "filled_not_web_archive": sum(1 for v in filled if not wb(v)),
        "filled_metadata_placeholder": sum(1 for v in filled if v == "Metadata"),
        "web_archive_wrapping_archive_is_or_md": sum(1 for v in filled if wb(v) and re.search(r"archive\.(is|md)/", v)),
    }
    out = {"url": TRAIN, "capture": p.name, "capture_bytes": p.stat().st_size,
           "capture_sha256": digest, "accessed": "2026-10-25", "counts": counts,
           "extra_not_frozen": extra}
    (EV / "counts.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print("spans", len(spans), "counts", counts)


if __name__ == "__main__":
    main()
