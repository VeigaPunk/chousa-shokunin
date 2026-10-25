#!/usr/bin/env python3
"""assimilate-rows — build a lane-schema append block from a staged campaign package.

Addendum section 10 (assimilation contract) as one runnable step, in scratch:

    python3 tools/assimilate-rows.py --staged FILE --knowledge DIR \
        --registry FILE --opened YYYY-MM-DD --out DIR [--entry REL ...]

Always writes DIR/reg-ids, DIR/staged-ids and DIR/collisions: sorted ids from
the section-10 pattern `^ {0,3}|[[:space:]]*S[0-9]{3,}` over the WHOLE
registry / staged file (0-3 leading spaces: an indented row collides too), and
their intersection.

With one or more --entry (a path relative to --knowledge, e.g.
`corpus/knowledge/x.md`) it also writes:

- `renumber.tsv` (`staged_id lane_id action url`): every staged id the entries
  cite, in ascending staged-id order. BY DOCUMENT: a staged row whose URL (the
  census's normalised first http(s) URL of the `source` cell) a Registry row
  already carries maps to that row's id (`held`, nothing appended); any other
  maps to the next free lane id, contiguous from the registry maximum
  (`append`). Ids are never shifted by arithmetic.
- DIR/<entry>: each entry with ONE simultaneous substitution of every cited
  staged id (so S100->S101 and S101->S102 never chain). Tokens that are not
  staged ids pass through unchanged — checking that they name the right lane
  document is the reader's job.
- `append.md`: one fleet-schema row per `append` id, in lane-id order: 11
  cells; the same substitution applied inside every cell; an escaped `\\|` and
  any other pipe inside a cell rewritten to ` / `; status `mined`; opened =
  --opened; recheck reduced to a census-valid value (an ISO date, `NNd`, or a
  symbolic cadence) with the stripped prose kept; `used-by` = exactly the
  given entries that cite the staged id, sorted, comma-separated.
- `stripped.tsv` (`lane_id column stripped`): every cell text the
  normalisation removed (recheck prose, the replaced status/opened/used-by
  values, pipe rewrites), for the round lesson's Gate block.

Refusals (exit 1, nothing claimed): an entry missing; a cited staged row with
no URL; a staged row whose recheck has no leading date/`NNd`/cadence.
Read-only on its inputs; writes only under --out. Exit 0 done · 1 refused · 2 usage.

Named limit: the URL is the document identity, so two staged rows for one URL
map to one lane id, and a held row's `used-by` is not widened (report it).
It does not open sources, check quotes, judge province or decide admission.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

GREP_RE = re.compile(r"^ {0,3}\|[ \t\r\f\v]*(S[0-9]{3,})")
ROW_RE = re.compile(r"^ {0,3}\|[ \t]*(S\d{3,})[ \t]*\|")
TOKEN_RE = re.compile(r"\bS\d{3,}\b")
ESC_SPLIT = re.compile(r"(?<!\\)\|")
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|[A-Za-z][A-Za-z0-9 _-]*)$")
LEAD_RE = re.compile(r"^\s*(\d{4}-\d{2}-\d{2}|\d+d)\b")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def url_of(source: str) -> str:
    """Same normalisation as scripts/sources-census.sh url_of()."""
    m = re.search(r"https?://[^\s|]+", source)
    if not m:
        return ""
    u = re.sub(r"/$", "", re.sub(r"#[^ ]*$", "", m.group(0)))
    u = re.sub(r"^[A-Za-z]+://", "", u)
    n = u.find("/")
    return (u[:n].lower() + u[n:]) if n >= 0 else u.lower()


def grep_ids(text: str) -> list[str]:
    return sorted({m.group(1) for line in text.splitlines() if (m := GREP_RE.match(line))})


def num(sid: str) -> int:
    return int(sid[1:])


def staged_rows(text: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for line in text.splitlines():
        m = ROW_RE.match(line)
        if m and m.group(1) not in out:
            out[m.group(1)] = [c.strip() for c in ESC_SPLIT.split(line.strip())[1:-1]]
    return out


def registry_rows(text: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    inside = False
    for line in text.splitlines():
        s = line.lstrip(" ")
        lead = len(line) - len(s)
        if lead <= 3 and s.startswith("## "):
            inside = s[3:].strip() == "Registry"
            continue
        if lead <= 3 and s.startswith("# "):
            inside = False
            continue
        m = ROW_RE.match(line)
        if inside and m and m.group(1) not in out:
            out[m.group(1)] = [c.strip() for c in s.strip().split("|")[1:-1]]
    return out


def write_ids(p: pathlib.Path, ids: list[str]) -> None:
    p.write_text("".join(i + "\n" for i in ids), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--staged", required=True)
    ap.add_argument("--knowledge", required=True)
    ap.add_argument("--registry", required=True)
    ap.add_argument("--opened", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--entry", action="append", default=[])
    a = ap.parse_args()
    staged_p, reg_p, know = pathlib.Path(a.staged), pathlib.Path(a.registry), pathlib.Path(a.knowledge)
    if not staged_p.is_file() or not reg_p.is_file() or not DATE_RE.match(a.opened):
        print("assimilate-rows: need --staged FILE, --registry FILE and --opened YYYY-MM-DD", file=sys.stderr)
        return 2
    for e in a.entry:
        if e.startswith("/") or ".." in pathlib.PurePath(e).parts:
            print(f"assimilate-rows: --entry {e!r} must be relative", file=sys.stderr)
            return 2
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    st_text = staged_p.read_text(encoding="utf-8")
    reg_text = reg_p.read_text(encoding="utf-8")
    reg_ids, st_ids = grep_ids(reg_text), grep_ids(st_text)
    write_ids(out / "reg-ids", reg_ids)
    write_ids(out / "staged-ids", st_ids)
    write_ids(out / "collisions", sorted(set(reg_ids) & set(st_ids)))
    print(f"COLLISIONS={len(set(reg_ids) & set(st_ids))}")
    if not a.entry:
        return 0

    staged = staged_rows(st_text)
    base = registry_rows(reg_text)
    texts: dict[str, str] = {}
    refused: list[str] = []
    for e in a.entry:
        p = know / e
        if not p.is_file():
            refused.append(f"entry missing: {e}")
        else:
            texts[e] = p.read_text(encoding="utf-8")
    cited = sorted({t for tx in texts.values() for t in TOKEN_RE.findall(tx) if t in staged}, key=num)
    for sid in cited:
        if len(staged[sid]) != 11:
            refused.append(f"{sid}: staged row has {len(staged[sid])} cells, not 11")
        elif not url_of(staged[sid][1]):
            refused.append(f"{sid}: staged row names no http(s) URL")
    if refused:
        for r in refused:
            print(f"REFUSED {r}", file=sys.stderr)
        return 1

    held: dict[str, str] = {}
    for sid in sorted(base, key=num):
        u = url_of(base[sid][1]) if len(base[sid]) > 1 else ""
        if u:
            held.setdefault(u, sid)
    nxt = max((num(s) for s in base), default=0) + 1
    mapping: dict[str, tuple[str, str]] = {}
    by_url: dict[str, str] = {}
    for sid in cited:
        u = url_of(staged[sid][1])
        if u in held:
            mapping[sid] = (held[u], "held")
        elif u in by_url:
            mapping[sid] = (by_url[u], "held")
        else:
            lid = f"S{nxt:03d}"
            nxt += 1
            mapping[sid] = (lid, "append")
            by_url[u] = lid
    sub = {sid: v[0] for sid, v in mapping.items()}

    def subst(s: str) -> str:
        return TOKEN_RE.sub(lambda m: sub.get(m.group(0), m.group(0)), s)

    rows: list[str] = []
    stripped: list[tuple[str, str, str]] = []
    for sid in cited:
        lid, action = mapping[sid]
        if action != "append":
            continue
        cells = [subst(c) for c in staged[sid]]
        for i, c in enumerate(cells):
            if "|" in c:
                stripped.append((lid, f"cell{i + 1}-pipe", c))
                cells[i] = re.sub(r"\s*\\?\|\s*", " / ", c)
        cells[0] = lid
        users = sorted(e for e, tx in texts.items() if sid in TOKEN_RE.findall(tx))
        recheck = cells[9]
        if not RECHECK_RE.match(recheck):
            m = LEAD_RE.match(recheck)
            if not m:
                print(f"REFUSED {sid}: recheck {recheck[:60]!r} has no leading date or NNd", file=sys.stderr)
                return 1
            stripped.append((lid, "recheck", recheck))
            cells[9] = m.group(1)
        for col, idx, new in (("status", 7, "mined"), ("opened", 8, a.opened), ("used-by", 10, ", ".join(users))):
            if cells[idx] != new:
                stripped.append((lid, col, cells[idx]))
                cells[idx] = new
        rows.append("| " + " | ".join(cells) + " |")

    for e, tx in texts.items():
        dst = out / e
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(subst(tx), encoding="utf-8")
    (out / "append.md").write_text("".join(r + "\n" for r in rows), encoding="utf-8")
    (out / "renumber.tsv").write_text(
        "staged_id\tlane_id\taction\turl\n"
        + "".join(f"{sid}\t{mapping[sid][0]}\t{mapping[sid][1]}\t{url_of(staged[sid][1])}\n" for sid in cited),
        encoding="utf-8")
    (out / "stripped.tsv").write_text(
        "lane_id\tcolumn\tstripped\n"
        + "".join(f"{l}\t{c}\t{s.replace(chr(9), ' ')}\n" for l, c, s in stripped),
        encoding="utf-8")
    print(f"CITED={len(cited)} APPEND={len(rows)} HELD={len(cited) - len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
