#!/usr/bin/env python3
"""assimilate-rows — build a lane-schema append block from a staged campaign package.

Addendum section 10 (assimilation contract) as one runnable step, in scratch:

    python3 tools/assimilate-rows.py --staged FILE --knowledge DIR \
        --registry FILE --opened YYYY-MM-DD --out DIR [--entry REL ...] [--cites source|all]

Always writes DIR/reg-ids, DIR/staged-ids and DIR/collisions: sorted ids from
the section-10 pattern `^ {0,3}|[[:space:]]*S[0-9]{3,}` over the WHOLE
registry / staged file (0-3 leading spaces: an indented row collides too), and
their intersection.

With one or more --entry (a path relative to --knowledge, e.g.
`corpus/knowledge/x.md`) it also writes:

- `renumber.tsv` (`staged_id lane_id action url`): every staged id the entries
  cite, in ascending staged-id order. An entry CITES the id right after `source:`
  on each header line (a line that starts with `source:`, above the first `####`
  heading; other ids on the line, and `source:` lines in the body, are not
  citations) — round 51 (QUALITY 77); a `source:` id that is neither a staged row nor
  a Registry row is refused, and an id that is both (a lane id the package also uses) is the staged row
  only when the line's URL is the staged row's URL, else it is the lane's own row and passes through;
  a fenced example header and a header below a `#### Provenance`-style heading are read as written
  (the header ends at the first `#### Observation|Inference|Unknown` heading); `--cites all`
  restores the round-49/50 reading (every staged id token an entry mentions). BY DOCUMENT: a staged row whose URL (the
  census's normalised first http(s) URL of the `source` cell) a Registry row
  already carries maps to that row's id (`held`, nothing appended); a second
  staged row for a URL this run already minted maps to that same id and is labelled
  `twin` (nothing appended either — `held` is reserved for the row the Registry
  already carries); any other
  maps to the next free lane id, contiguous from the registry maximum
  (`append`). Ids are never shifted by arithmetic, and the stdout tail counts the
  two apart: `HELD=<registry rows> TWIN=<twins>`.
- DIR/<entry>: each entry with ONE simultaneous substitution of that entry's OWN
  cited staged ids (in `--cites all` mode: of every cited staged id) (so S100->S101 and S101->S102 never chain). Tokens that are not
  cited pass through unchanged — checking that they name the right lane
  document is the reader's job. In the default `--cites source` mode a staged id
  an entry mentions but does not itself cite on a header `source:` line (also when
  another entry cites it, and a tail id of a header line) is left unchanged and listed in
  `bodyonly.tsv` (`entry<TAB>staged_id`, header line first) and counted as
  `BODYONLY=<n>` on stdout; when such an id is also a lane id (a registry row
  or a minted one) it is also listed in `bodyclash.tsv` and warned on stderr
  (`WARN`), because the unchanged token then reads as that lane row.
- `append.md`: one fleet-schema row per `append` id, in lane-id order: 11
  cells; the same substitution applied inside every cell; an escaped `\\|` and
  any other pipe inside a cell rewritten to ` / ` (a staged row's document
  identity is read from the source cell AFTER that rewrite, and a registry row's
  cells are split with the same escaped-pipe splitter, so an escaped pipe in either
  source cell never loses the URL); status `mined`; opened =
  --opened; recheck reduced to a census-valid value (an ISO date, `NNd`, or a
  symbolic cadence) with the stripped prose kept; `used-by` = exactly the
  given entries that cite the staged id, sorted, comma-separated.
- `stripped.tsv` (`lane_id column stripped`): every cell text the
  normalisation removed (recheck prose, the replaced status/opened/used-by
  values, pipe rewrites), for the round lesson's Gate block.

Refusals (exit 1, nothing claimed): a registry with no `## Registry` heading or
with an `S###` row (0-3 leading spaces) outside the Registry section (the ids it
would continue from are not the registry's) — checked and printed FIRST, before any
entry is read, and also without `--entry` (omitting the entries is not a way past a
broken registry); an entry missing or not UTF-8; a cited staged row with no URL;
any cited staged row whose recheck has no leading calendar-valid date, `NNd` or
cadence — `held` and `twin` rows included, because their recheck is still a claim
about the source even though they carry no row of their own. Headings accept a space or a tab after
the hashes, as the census does. Read-only on its inputs; writes only under
--out. Exit 0 done · 1 refused · 2 usage (missing file, non-UTF-8 registry or
staged file, calendar-invalid --opened, absolute or `..` entry).

Self-test (round 50): `python3 tools/assimilate-rows.py --selftest [--fixtures DIR]
[--expected FILE]` runs the tool above on an isolated fixture package
(default `corpus/fixtures/assimilate-selftest/`: `registry.md`, `staged.md`,
`knowledge/corpus/knowledge/*.md`, `expected.json`; `--opened` fixed at
2026-10-25) and compares the observed finding lines with the `findings` list of
the expected file. A finding line is one of: `TOOLEXIT n`, `REFUSED text`,
`COLLISIONS ids|-`, `MAP staged->lane action`, `ROWCELLS lane n`, `ROWSTATUS
lane status`, `ROWUSEDBY lane list`, `ROWRECHECK lane value`, `ENTRYCITES
entry ids`, `BODYONLY entry id`, `BODYCLASH entry id` (source mode only),
`STRIPPED lane column`. The expected file may add `cases`: a list of the shape
`{"fixtures": <package dir under the fixture root, with its own staged.md,
registry.md and knowledge/>, "findings": [<that package's expected lines>],
"entry": [<entry paths to pass; an empty list runs with no --entry>]}` — each case
is run after the root package and the digest covers every file under the root,
cases included. `--selftest` also takes `--cites source|all` (default
`source`; the round-50 pinned package needs `all`). The environment variable
`ASSIMILATE_CITES=source|all` sets the default of both modes; it restores the round-49 counter
(`ASSIMILATE_CITES=all python3 corpus/evidence/round49/c1-count.py` passes) but not the round-50
one, whose default leg reads the lane default fixtures that are now the source-mode package; an
explicit `--cites` wins. An ambient value changes the verdict of any caller that passes no flag,
so the round-51 counters run the tool with the variable removed from its environment). It prints each as `FINDING <line>`, every
difference as `DIFF missing <line>` / `DIFF unexpected <line>`, then
`FIXTURES_SHA256=<hex>` (sha256 over the sorted relative paths and bytes of
every fixture file) and `SELFTEST=PASS|FAIL`. Exit 0 PASS · 1 FAIL · 2 fixtures
missing, no knowledge entry, or expected file missing or unparseable. The comparison is of multisets
(a duplicated finding is a difference), except the `REFUSED` lines, which are also compared in
order (`DIFF order <observed> (want <expected>)`): a refusal's order is what the operator reads;
`--selftest` with any other option exits 2; a finding line
never carries a tab; an entry citing no id prints `ENTRYCITES <entry> -`; the child runs under a
120-second timeout (`TOOLEXIT 124`). The expected file is written by a
person from the addendum rules, never generated by this tool.

Named limit: the URL is the document identity, so two staged rows for one URL
map to one lane id (`append` for the first, `twin` for each later one; the appended
row's `used-by` names the entries citing ANY of them, and keeps the
first staged row's tier and scope cells: a tier or scope disagreement between the twins is the
reader's to decide); a row held by the lane registry is not widened (report it).
It does not open sources, check quotes, judge province or decide admission.
"""
from __future__ import annotations

import argparse
import collections
import datetime
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

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
        if lead <= 3 and re.match(r"##[ \t]", s):
            inside = s[3:].strip() == "Registry"
            continue
        if lead <= 3 and re.match(r"#[ \t]", s):
            inside = False
            continue
        m = ROW_RE.match(line)
        if inside and m and m.group(1) not in out:
            out[m.group(1)] = [c.strip() for c in ESC_SPLIT.split(s.strip())[1:-1]]
    return out


def pipe_free(cell: str) -> str:
    """The cell as it lands in the append block: any pipe (escaped or not) becomes ` / `."""
    return re.sub(r"\s*\\?\|\s*", " / ", cell)


SOURCE_RE = re.compile(r"^source:[ \t]*(S\d{3,})\b")
HEADER_END = re.compile(r"^####[ \t]+(Observation|Inference|Unknown)\b")


def source_cites(text: str) -> list[tuple[str, str]]:
    """(id, line) for each header `source:` line: the id right after `source:` on a line that starts with
    `source:`, read above the first `#### Observation|Inference|Unknown` heading and outside fenced code
    blocks, one entry per id (first mention). Other ids on the line (an anchor or note) and `source:` lines
    in the body or in a fenced example are not citations."""
    out: list[tuple[str, str]] = []
    fenced = False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if HEADER_END.match(line):
            break
        m = SOURCE_RE.match(line)
        if m and all(m.group(1) != i for i, _l in out):
            out.append((m.group(1), line))
    return out


def source_ids(text: str) -> list[str]:
    return [i for i, _l in source_cites(text)]


def registry_problems(text: str) -> list[str]:
    """Why this registry cannot be renumbered against: no `## Registry` heading, or an S### row outside it."""
    inside, seen, outside = False, False, []
    for line in text.splitlines():
        s = line.lstrip(" ")
        if len(line) - len(s) <= 3 and re.match(r"##[ \t]", s):
            inside = s[3:].strip() == "Registry"
            seen = seen or inside
            continue
        if len(line) - len(s) <= 3 and re.match(r"#[ \t]", s):
            inside = False
            continue
        m = ROW_RE.match(line)
        if m and not inside:
            outside.append(m.group(1))
    out = [] if seen else ["registry has no `## Registry` heading"]
    if outside:
        out.append("registry rows outside the Registry section: " + ", ".join(sorted(set(outside), key=num)))
    return out


def valid_date(s: str) -> bool:
    """A calendar-valid ISO date with a nonzero year (the census epoch() test)."""
    if not DATE_RE.match(s) or s.startswith("0000"):
        return False
    try:
        datetime.date.fromisoformat(s)
    except ValueError:
        return False
    return True


def write_ids(p: pathlib.Path, ids: list[str]) -> None:
    p.write_text("".join(i + "\n" for i in ids), encoding="utf-8")


def split_cells(line: str) -> list[str]:
    return [c.strip() for c in ESC_SPLIT.split(line.strip())[1:-1]]


def observe(fix: pathlib.Path, cites: str = "source", entries: list[str] | None = None) -> list[str]:
    """Run this tool on fixture package `fix`; return its finding lines.

    `entries` overrides the default (every `.md` under `knowledge/`); an empty list runs the child
    with no `--entry` at all, which is a package the tool is asked to refuse."""
    know = fix / "knowledge"
    if entries is None:
        entries = sorted(p.relative_to(know).as_posix() for p in know.rglob("*.md")) if know.is_dir() else []
    out = pathlib.Path(tempfile.mkdtemp(prefix="assimilate-selftest-"))
    try:
        cmd = [sys.executable, str(pathlib.Path(__file__).resolve()), "--staged", str(fix / "staged.md"),
               "--knowledge", str(know), "--registry", str(fix / "registry.md"), "--opened", "2026-10-25",
               "--out", str(out), "--cites", cites]
        for e in entries:
            cmd += ["--entry", e]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            return ["TOOLEXIT 124"]
        found = [f"TOOLEXIT {r.returncode}"]
        found += [f"REFUSED {l[8:].strip()}" for l in r.stderr.splitlines() if l.startswith("REFUSED ")]
        cf = out / "collisions"
        if cf.is_file():
            ids = [l for l in cf.read_text(encoding="utf-8").splitlines() if l]
            found.append("COLLISIONS " + (",".join(ids) if ids else "-"))
        rn = out / "renumber.tsv"
        if rn.is_file():
            for l in rn.read_text(encoding="utf-8").splitlines()[1:]:
                sid, lid, act, _u = l.split("\t")
                found.append(f"MAP {sid}->{lid} {act}")
        ap_ = out / "append.md"
        if ap_.is_file():
            for l in ap_.read_text(encoding="utf-8").splitlines():
                cells = split_cells(l)
                lid = cells[0]
                found.append(f"ROWCELLS {lid} {len(cells)}")
                if len(cells) == 11:
                    found += [f"ROWSTATUS {lid} {cells[7]}", f"ROWUSEDBY {lid} {cells[10]}",
                              f"ROWRECHECK {lid} {cells[9]}"]
        for e in entries:
            q = out / e
            if q.is_file():
                ids = sorted(set(TOKEN_RE.findall(q.read_text(encoding="utf-8"))), key=num)
                found.append(f"ENTRYCITES {e} {','.join(ids) if ids else '-'}")
        for fname, tag in (("bodyonly.tsv", "BODYONLY"), ("bodyclash.tsv", "BODYCLASH")):
            bf = out / fname
            if bf.is_file():
                for l in bf.read_text(encoding="utf-8").splitlines()[1:]:
                    found.append(f"{tag} {l.split(chr(9))[0]} {l.split(chr(9))[1]}")
        sp = out / "stripped.tsv"
        if sp.is_file():
            for l in sp.read_text(encoding="utf-8").splitlines()[1:]:
                lid, col, _t = l.split("\t", 2)
                found.append(f"STRIPPED {lid} {col}")
        return [f.replace("\t", " ") for f in found]
    finally:
        shutil.rmtree(out, ignore_errors=True)


def fixtures_digest(fix: pathlib.Path) -> str:
    h = hashlib.sha256()
    for p in sorted(q for q in fix.rglob("*") if q.is_file()):
        h.update(p.relative_to(fix).as_posix().encode() + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()


def selftest(fixtures: str | None, expected: str | None, cites: str = "source") -> int:
    fix = pathlib.Path(fixtures) if fixtures is not None else pathlib.Path(__file__).resolve().parents[1] / "corpus" / "fixtures" / "assimilate-selftest"
    exp = pathlib.Path(expected) if expected is not None else fix / "expected.json"
    if not (fix / "staged.md").is_file() or not (fix / "registry.md").is_file():
        print(f"SELFTEST=ERROR fixtures {fix}: staged.md or registry.md missing")
        return 2
    if not ((fix / "knowledge").is_dir() and any((fix / "knowledge").rglob("*.md"))):
        print(f"SELFTEST=ERROR fixtures {fix}: no knowledge entry — a self-test with no entry exercises no renumbering")
        return 2
    try:
        doc = json.loads(exp.read_text(encoding="utf-8"))
        want = doc["findings"]
        if not isinstance(want, list) or not all(isinstance(w, str) for w in want):
            raise ValueError("findings must be a list of strings")
        cases: list[tuple[str, pathlib.Path, list[str] | None, list[str]]] = [("", fix, None, want)]
        for c in doc.get("cases", []):
            if not (isinstance(c, dict) and isinstance(c.get("fixtures"), str)
                    and isinstance(c.get("findings"), list) and all(isinstance(w, str) for w in c["findings"])):
                raise ValueError("each case needs `fixtures` (string) and `findings` (list of strings)")
            ent = c.get("entry")
            if ent is not None and (not isinstance(ent, list) or not all(isinstance(x, str) for x in ent)):
                raise ValueError(f"case {c['fixtures']}: `entry` must be a list of entry paths")
            d = fix / c["fixtures"]
            if not (d / "staged.md").is_file() or not (d / "registry.md").is_file() or not (d / "knowledge").is_dir():
                raise ValueError(f"case fixtures {d}: staged.md, registry.md or knowledge missing")
            cases.append((c["fixtures"], d, ent, c["findings"]))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"SELFTEST=ERROR expected file {exp}: {exc}")
        return 2
    ok, n_got, n_want = True, 0, 0
    for label, d, ent, want_c in cases:
        got = observe(d, cites, ent)
        for g in got:
            print(f"FINDING {g}")
        cw, cg = collections.Counter(want_c), collections.Counter(got)
        miss, extra = sorted((cw - cg).elements()), sorted((cg - cw).elements())
        for m in miss:
            print(f"DIFF missing {m}")
        for x in extra:
            print(f"DIFF unexpected {x}")
        # a refusal is judged by the order it is printed in as well as by its presence
        ro = [g for g in got if g.startswith("REFUSED ")]
        rw = [w for w in want_c if w.startswith("REFUSED ")]
        if ro != rw:
            ok = False
            for i in range(max(len(ro), len(rw))):
                o, w = (ro[i] if i < len(ro) else "-"), (rw[i] if i < len(rw) else "-")
                if o != w:
                    print(f"DIFF order {label + ': ' if label else ''}{o} (want {w})")
        n_got += len(got)
        n_want += len(want_c)
        ok = ok and not miss and not extra
    print(f"FIXTURES_SHA256={fixtures_digest(fix)}")
    print(f"SELFTEST={'PASS' if ok else 'FAIL'} findings={n_got} expected={n_want}")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--fixtures")
    ap.add_argument("--expected")
    ap.add_argument("--cites", choices=("source", "all"), default=None)
    for opt in ("staged", "knowledge", "registry", "opened", "out"):
        ap.add_argument("--" + opt)
    ap.add_argument("--entry", action="append", default=[])
    a = ap.parse_args()
    if a.selftest:
        if any((a.staged, a.knowledge, a.registry, a.opened, a.out, a.entry)):
            print("assimilate-rows: --selftest takes only --fixtures and --expected", file=sys.stderr)
            return 2
        sc = a.cites or os.environ.get("ASSIMILATE_CITES") or "source"
        if sc not in ("source", "all"):
            print(f"assimilate-rows: ASSIMILATE_CITES={sc!r} must be source or all", file=sys.stderr)
            return 2
        return selftest(a.fixtures, a.expected, sc)
    cites = a.cites or os.environ.get("ASSIMILATE_CITES") or "source"
    if cites not in ("source", "all"):
        print(f"assimilate-rows: ASSIMILATE_CITES={cites!r} must be source or all", file=sys.stderr)
        return 2
    if not all((a.staged, a.knowledge, a.registry, a.opened, a.out)):
        ap.print_usage(sys.stderr)
        print("assimilate-rows: --staged --knowledge --registry --opened --out are required (or --selftest)", file=sys.stderr)
        return 2
    staged_p, reg_p, know = pathlib.Path(a.staged), pathlib.Path(a.registry), pathlib.Path(a.knowledge)
    if not staged_p.is_file() or not reg_p.is_file() or not valid_date(a.opened):
        print("assimilate-rows: need --staged FILE, --registry FILE and a calendar-valid --opened YYYY-MM-DD", file=sys.stderr)
        return 2
    for e in a.entry:
        if e.startswith("/") or ".." in pathlib.PurePath(e).parts:
            print(f"assimilate-rows: --entry {e!r} must be relative", file=sys.stderr)
            return 2
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    try:
        st_text = staged_p.read_text(encoding="utf-8")
        reg_text = reg_p.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        print(f"assimilate-rows: input is not UTF-8: {exc}", file=sys.stderr)
        return 2
    reg_ids, st_ids = grep_ids(reg_text), grep_ids(st_text)
    write_ids(out / "reg-ids", reg_ids)
    write_ids(out / "staged-ids", st_ids)
    write_ids(out / "collisions", sorted(set(reg_ids) & set(st_ids)))
    print(f"COLLISIONS={len(set(reg_ids) & set(st_ids))}")
    reg_bad = registry_problems(reg_text)      # the ids this run would continue from
    if not a.entry:
        if reg_bad:
            # a registry whose ids cannot be continued from is refused with or without an --entry
            for r in reg_bad:
                print(f"REFUSED {r}", file=sys.stderr)
            return 1
        return 0
    for name in ("renumber.tsv", "append.md", "stripped.tsv", "bodyonly.tsv", "bodyclash.tsv"):
        (out / name).unlink(missing_ok=True)      # a refusal never leaves a previous run's claim behind
    for e in a.entry:
        (out / e).unlink(missing_ok=True)

    staged = staged_rows(st_text)
    base = registry_rows(reg_text)
    texts: dict[str, str] = {}
    refused: list[str] = list(reg_bad)         # the registry precondition is reported first
    for e in a.entry:
        p = know / e
        if not p.is_file():
            refused.append(f"entry missing: {e}")
        else:
            try:
                texts[e] = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                refused.append(f"entry not UTF-8: {e}")
    own: dict[str, set[str]] = {}
    if cites == "source":
        # a `source:` id is a STAGED row when the staged row exists and either no Registry row carries the id or
        # the line's URL is the staged row's URL; otherwise a Registry row of the lane (own-work, passes through)
        for e, tx in texts.items():
            own[e] = set()
            for i, line in source_cites(tx):
                st_url = url_of(pipe_free(staged[i][1])) if i in staged and len(staged[i]) > 1 else ""
                if i in staged and (i not in base or url_of(line) == st_url):
                    own[e].add(i)
                elif i not in base:
                    refused.append(f"{e}: source id {i} is neither a staged row nor a lane Registry row")
        cited = sorted({i for s in own.values() for i in s}, key=num)
    else:
        cited = sorted({t for tx in texts.values() for t in TOKEN_RE.findall(tx) if t in staged}, key=num)
    for sid in cited:
        if len(staged[sid]) != 11:
            refused.append(f"{sid}: staged row has {len(staged[sid])} cells, not 11")
        elif not url_of(pipe_free(staged[sid][1])):
            refused.append(f"{sid}: staged row names no http(s) URL")
    if refused:
        for r in refused:
            print(f"REFUSED {r}", file=sys.stderr)
        return 1

    held: dict[str, str] = {}
    for sid in sorted(base, key=num):
        u = url_of(pipe_free(base[sid][1])) if len(base[sid]) > 1 else ""
        if u:
            held.setdefault(u, sid)
    nxt = max((num(s) for s in base), default=0) + 1
    mapping: dict[str, tuple[str, str]] = {}
    by_url: dict[str, str] = {}
    for sid in cited:
        u = url_of(pipe_free(staged[sid][1]))
        if u in held:
            mapping[sid] = (held[u], "held")
        elif u in by_url:
            mapping[sid] = (by_url[u], "twin")
        else:
            lid = f"S{nxt:03d}"
            nxt += 1
            mapping[sid] = (lid, "append")
            by_url[u] = lid
    sub = {sid: v[0] for sid, v in mapping.items()}

    def subst(s: str, only: set[str] | None = None) -> str:
        return TOKEN_RE.sub(lambda m: sub[m.group(0)] if m.group(0) in sub and (only is None or m.group(0) in only)
                            else m.group(0), s)

    minted = {v[0] for v in mapping.values() if v[1] == "append"}

    # a cited row's recheck is a claim about its source whether or not the row appends (a `held` or `twin`
    # row carries no row of its own), so every cited recheck is validated before any row is built
    recheck_ok: dict[str, str] = {}
    late: list[str] = []
    for sid in cited:
        recheck = subst(staged[sid][9])
        if RECHECK_RE.match(recheck) and (not DATE_RE.match(recheck) or valid_date(recheck)):
            recheck_ok[sid] = recheck
            continue
        m = LEAD_RE.match(recheck)
        if not m or (DATE_RE.match(m.group(1)) and not valid_date(m.group(1))):
            late.append(f"{sid}: recheck {recheck[:60]!r} has no leading valid date or NNd")
        else:
            recheck_ok[sid] = m.group(1)
    if late:
        for r in late:
            print(f"REFUSED {r}", file=sys.stderr)
        return 1

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
        twins = {t for t in cited if mapping[t][0] == lid}
        users = sorted(e for e, tx in texts.items()
                       if twins & (own[e] if cites == "source" else set(TOKEN_RE.findall(tx))))
        recheck = recheck_ok[sid]
        if cells[9] != recheck:
            stripped.append((lid, "recheck", cells[9]))
            cells[9] = recheck
        for col, idx, new in (("status", 7, "mined"), ("opened", 8, a.opened), ("used-by", 10, ", ".join(users))):
            if cells[idx] != new:
                stripped.append((lid, col, cells[idx]))
                cells[idx] = new
        rows.append("| " + " | ".join(cells) + " |")

    for e, tx in texts.items():
        dst = out / e
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(subst(tx, own[e] if cites == "source" else None), encoding="utf-8")
    if cites == "source":
        lane_ids = {s for s in base} | minted
        body = [(e, i) for e, tx in texts.items()
                for i in sorted(set(TOKEN_RE.findall(tx)) - own[e], key=num) if i in staged]
        (out / "bodyonly.tsv").write_text("entry\tstaged_id\n" + "".join(f"{e}\t{i}\n" for e, i in body), encoding="utf-8")
        clash = [(e, i) for e, i in body if i in lane_ids]
        # a body token that is no staged row but equals an id this run mints reads as the new row as well
        clash += [(e, i) for e, tx in texts.items() for i in sorted(set(TOKEN_RE.findall(tx)) - own[e], key=num)
                  if i in minted and i not in staged]
        if clash:
            (out / "bodyclash.tsv").write_text("entry\tstaged_id\n" + "".join(f"{e}\t{i}\n" for e, i in clash), encoding="utf-8")
            for e, i in clash:
                print(f"WARN {e}: body-only id {i} is also a lane id and reads as that row", file=sys.stderr)
    (out / "append.md").write_text("".join(r + "\n" for r in rows), encoding="utf-8")
    (out / "renumber.tsv").write_text(
        "staged_id\tlane_id\taction\turl\n"
        + "".join(f"{sid}\t{mapping[sid][0]}\t{mapping[sid][1]}\t{url_of(pipe_free(staged[sid][1]))}\n" for sid in cited),
        encoding="utf-8")
    (out / "stripped.tsv").write_text(
        "lane_id\tcolumn\tstripped\n"
        + "".join(f"{l}\t{c}\t{s.replace(chr(9), ' ')}\n" for l, c, s in stripped),
        encoding="utf-8")
    held_n = sum(1 for v in mapping.values() if v[1] == "held")
    twin_n = sum(1 for v in mapping.values() if v[1] == "twin")
    print(f"CITED={len(cited)} APPEND={len(rows)} HELD={held_n} TWIN={twin_n}")
    if cites == "source":
        print(f"BODYONLY={len(body)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
