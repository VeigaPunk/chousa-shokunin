#!/usr/bin/env python3
"""R63-C2 frozen counter — the sourced entry on what pins a citation to a git revision.

Predicate R63-C2 (the same sentence as corpus/evidence/round63/claims.md): in the lane tree ROOT (default this lane)
the file `corpus/knowledge/git-revision-identity-r63.md` exists and

  TRIO     its first 12 lines carry `source:`, `verified-at:` and `recheck:`, and the `source:` line names S142, S143
           and S144;
  ROWS     the registry rows S142, S143, S144 each have 11 cells, tier A (S142, S143) or B (S144), status `mined`,
           `opened` on or after 2026-10-28, a `used-by` naming the entry's repo-relative path, and a `source` cell
           that resolves to local text — S142 to `/usr/share/man/man1/git-rev-parse.1.gz`, S143 to
           `/usr/share/man/man7/gitrevisions.7.gz` (both rendered `MANWIDTH=1000 man -l FILE | col -bx`), S144 to the
           lane file `corpus/evidence/round63/git-revision-probe.txt`, which exists;
  QUOTES   the entry's `## Located quotes` section holds lines `- Q<n> | S<id> | <quote> | <anchor>`; every quote has
           4 to 25 words, occurs in the whitespace-normalised text its row resolves to, and its anchor text occurs in
           that row's `anchor` cell and in the resolved text; at least 2 quotes are bound to S142, 3 to S143 and 2 to
           S144;
  CLAIMS   the `## Claims` section holds at least 5 lines `Claim <n>. <text> [Q<a>, Q<b>]`; every cited Q exists,
           every Q is cited by some claim, and each claim shares at least 2 distinct words of 5 or more letters with
           the quotes it cites;
  ECHO     in every claim at least 3 words of 5 or more letters, and at least 30 % of such words, occur in none of
           the quotes it cites (a claim that only repeats its quote fails);
  LIMITS   the `## Limits` section holds at least 3 bullet lines, at least one starting `- [INFERENCE]`, and the text
           of the section contains the live `git --version` line (the entry names the version it was checked on);
  PROBE    `python3 corpus/evidence/round63/git-revision-probe.py --work <fresh dir>` exits 0 with `PROBE_FACTS=k/k`,
           its `PROBE`/`HEADER` lines equal the committed `git-revision-probe.txt` lines, and the committed `HEADER`
           line for git equals the live `git --version` line;
  MAP      `corpus/README.md` names the entry's repo-relative path;
  CENSUS   the fleet's `scripts/sources-census.sh validate --file ROOT/corpus/SOURCES.md`, run with ROOT as its
           working directory, exits 0,

counted `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=k/k COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1
CENSUS=1/1 C2=PASS`. The counter is structural plus an echo screen: it proves the located quotes exist where the rows
say, that every claim and quote reference resolves, that no claim only repeats its quote, that the probe the entry
rests on still runs on this host's git and that the entry names that git; it does not judge that a claim follows from
its quotes (named limit — reviewers judge that).

`--config openat2` selects the round-62 control configuration (entry `openat2-resolve-r62.md`, rows S138-S140): the
controls prove the counter's engine on a known-good entry; the claim is judged on the default `git` configuration only.

Fleet layout: the counter runs the fleet's census script. `--fleet DIR` names the fleet root (the directory holding
`scripts/sources-census.sh`); default `$SHOKUNIN_ROOT`, else the lane root's parent. A bare `git archive` export of the
lane has no such parent: pass `--fleet`. A missing census script exits 2, never a verdict.

Usage: python3 corpus/evidence/round63/c2-count.py [--root DIR] [--fleet DIR] [--work DIR] [--config git|openat2]
Exit codes: 0 C2=PASS · 1 C2=FAIL · 2 usage/env (no `man`/`col`/`git`, no census script).
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[2]
CONFIGS = {
    "git": dict(
        entry="corpus/knowledge/git-revision-identity-r63.md",
        ids=("S142", "S143", "S144"),
        tier={"S142": "A", "S143": "A", "S144": "B"},
        man={"S142": "/usr/share/man/man1/git-rev-parse.1.gz", "S143": "/usr/share/man/man7/gitrevisions.7.gz"},
        file={},
        own={"S144": "corpus/evidence/round63/git-revision-probe.txt"},
        min_quotes={"S142": 2, "S143": 3, "S144": 2},
        probe="corpus/evidence/round63/git-revision-probe.py",
        bind_git=True,
    ),
    "openat2": dict(
        entry="corpus/knowledge/openat2-resolve-r62.md",
        ids=("S138", "S139", "S140"),
        tier={"S138": "A", "S139": "A", "S140": "B"},
        man={"S138": "/usr/share/man/man2/openat2.2.gz"},
        file={"S139": "/usr/include/linux/openat2.h"},
        own={"S140": "corpus/evidence/round62/openat2-probe.txt"},
        min_quotes={"S138": 3, "S139": 1, "S140": 2},
        probe="corpus/evidence/round62/openat2-probe.py",
        bind_git=False,
    ),
}
MIN_OPENED = "2026-10-28"
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def registry(root: pathlib.Path) -> dict[str, list[str]]:
    rows = {}
    f = root / "corpus" / "SOURCES.md"
    if not f.is_file():
        return rows
    for line in f.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if m:
            cells = line.split("|")
            if len(cells) == 13:
                rows[m.group(1)] = [c.strip() for c in cells[1:12]]
    return rows


def render_man(path: str) -> str | None:
    env = dict(os.environ, MANWIDTH="1000", LC_ALL="C.UTF-8")
    try:
        m = subprocess.run(["man", "-l", path], capture_output=True, env=env, timeout=60)
        c = subprocess.run(["col", "-bx"], input=m.stdout, capture_output=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        raise SystemExit("c2-count: man or col unavailable")
    if m.returncode != 0 or not c.stdout:
        return None
    return norm(c.stdout.decode("utf-8", errors="replace"))


def resolve(cfg, root: pathlib.Path, sid: str, row: list[str]) -> str | None:
    src = row[1]
    if sid in cfg["man"]:
        return render_man(cfg["man"][sid]) if cfg["man"][sid] in src and os.path.exists(cfg["man"][sid]) else None
    if sid in cfg["file"]:
        p = pathlib.Path(cfg["file"][sid])
        return norm(p.read_text(encoding="utf-8", errors="replace")) if cfg["file"][sid] in src and p.is_file() else None
    p = root / cfg["own"][sid]
    return norm(p.read_text(encoding="utf-8", errors="replace")) if cfg["own"][sid] in src and p.is_file() else None


def section(text: str, heading: str) -> list[str]:
    out, on = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            on = line.strip() == heading
            continue
        if on:
            out.append(line)
    return out


def words(s: str) -> set[str]:
    return {w.lower() for w in re.findall(r"[A-Za-z]{5,}", s)}


def probe_lines(text: str) -> list[str]:
    return [l.rstrip() for l in text.splitlines()
            if l.startswith("PROBE ") or l.startswith("PROBE_FACTS=") or l.startswith("HEADER ")]


def live_git() -> str:
    try:
        p = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        raise SystemExit("c2-count: git unavailable")
    if p.returncode != 0 or not p.stdout.strip():
        raise SystemExit("c2-count: git --version failed")
    return p.stdout.strip()


def find_census(fleet_arg: str | None) -> pathlib.Path | None:
    cands = []
    if fleet_arg:
        cands.append(pathlib.Path(fleet_arg))
    elif os.environ.get("SHOKUNIN_ROOT"):
        cands.append(pathlib.Path(os.environ["SHOKUNIN_ROOT"]))
    else:
        cands.append(LANE.parent)
    for c in cands:
        s = c / "scripts" / "sources-census.sh"
        if s.is_file():
            return s
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE))
    ap.add_argument("--fleet", default=None)
    ap.add_argument("--work", default=None)
    ap.add_argument("--config", default="git", choices=sorted(CONFIGS))
    a = ap.parse_args()
    cfg = CONFIGS[a.config]
    root = pathlib.Path(a.root)
    census = find_census(a.fleet)
    if census is None:
        print("c2-count: no scripts/sources-census.sh — pass --fleet DIR (the fleet root, or set SHOKUNIN_ROOT); "
              "a bare git archive of the lane has no fleet parent", file=sys.stderr)
        return 2
    git_line = live_git() if cfg["bind_git"] else ""
    ids = cfg["ids"]
    entry_rel = cfg["entry"]
    entry = root / entry_rel
    res: dict[str, str] = {}
    detail: list[str] = []
    ok_entry = entry.is_file()
    text = entry.read_text(encoding="utf-8") if ok_entry else ""
    res["ENTRY"] = f"{int(ok_entry)}/1"
    head = "\n".join(text.splitlines()[:12])
    src_line = next((l for l in head.splitlines() if l.startswith("source:")), "")
    trio = ok_entry and all(re.search(rf"^{k}:", head, re.M) for k in ("source", "verified-at", "recheck")) \
        and all(i in src_line for i in ids)
    res["TRIO"] = f"{int(bool(trio))}/1"
    rows = registry(root)
    good = 0
    texts: dict[str, str | None] = {}
    for sid in ids:
        r = rows.get(sid)
        if not r:
            detail.append(f"ROW {sid} absent")
            continue
        tier_ok = r[3] == cfg["tier"][sid]
        texts[sid] = resolve(cfg, root, sid, r)
        used = entry_rel in [u.strip() for u in re.split(r"[,;]", r[10])]
        ok = tier_ok and r[7] == "mined" and r[8] >= MIN_OPENED and re.match(r"^\d{4}-\d{2}-\d{2}$", r[8]) \
            and used and texts[sid] is not None
        if not ok:
            detail.append(f"ROW {sid} tier={r[3]} status={r[7]} opened={r[8]} used_by_entry={used} resolves={texts[sid] is not None}")
        good += bool(ok)
    res["ROWS"] = f"{good}/3"
    qlines = [l for l in section(text, "## Located quotes") if l.startswith("- Q")]
    quotes: dict[str, tuple[str, str]] = {}
    qok = 0
    per_row = {i: 0 for i in ids}
    for l in qlines:
        cells = [c.strip() for c in l[2:].split(" | ")]
        if len(cells) != 4 or not re.match(r"^Q\d+$", cells[0]) or cells[1] not in ids:
            detail.append(f"QUOTE malformed: {l[:60]}")
            continue
        qid, sid, quote, anchor = cells
        n = len(quote.split())
        found = texts.get(sid) is not None and norm(quote) in texts[sid]
        anch = anchor != "" and rows.get(sid) is not None and anchor in rows[sid][5] and anchor in (texts[sid] or "")
        if 4 <= n <= 25 and found and anch and qid not in quotes:
            quotes[qid] = (sid, quote)
            per_row[sid] += 1
            qok += 1
        else:
            detail.append(f"QUOTE {qid} {sid} words={n} found={found} anchor_ok={anch}")
    res["QUOTES"] = f"{qok}/{len(qlines)}" if qlines else "0/0"
    cov = all(per_row[i] >= cfg["min_quotes"][i] for i in ids) and qok == len(qlines) > 0
    res["COVERAGE"] = f"{int(cov)}/1"
    claims = [l for l in section(text, "## Claims") if re.match(r"^Claim \d+\.", l)]
    cited, claims_ok, echo_ok = set(), len(claims) >= 5, len(claims) >= 5
    for l in claims:
        m = re.match(r"^Claim \d+\.\s+(.*)\s\[((?:Q\d+(?:,\s*)?)+)\]\s*$", l)
        if not m:
            claims_ok = echo_ok = False
            detail.append(f"CLAIM malformed: {l[:60]}")
            continue
        qs = [q.strip() for q in m.group(2).split(",")]
        if any(q not in quotes for q in qs):
            claims_ok = echo_ok = False
            detail.append(f"CLAIM cites unknown quote: {l[:60]}")
            continue
        cited.update(qs)
        qwords = set().union(*(words(quotes[q][1]) for q in qs))
        cw = words(m.group(1))
        shared = cw & qwords
        if len(shared) < 2:
            claims_ok = False
            detail.append(f"CLAIM shares {len(shared)} words with its quotes: {l[:60]}")
        fresh = cw - qwords
        if len(fresh) < 3 or len(fresh) < 0.3 * len(cw):
            echo_ok = False
            detail.append(f"ECHO claim has {len(fresh)} of {len(cw)} words outside its quotes: {l[:60]}")
    claims_ok = claims_ok and bool(quotes) and cited == set(quotes)
    res["CLAIMS"] = f"{int(claims_ok)}/1"
    res["ECHO"] = f"{int(echo_ok)}/1"
    sec = section(text, "## Limits")
    limits = [l for l in sec if l.lstrip().startswith("- ")]
    lim_ok = len(limits) >= 3 and any(l.lstrip().startswith("- [INFERENCE]") for l in limits)
    if cfg["bind_git"] and git_line not in "\n".join(sec):
        lim_ok = False
        detail.append(f"LIMITS do not name the live `{git_line}`")
    res["LIMITS"] = f"{int(lim_ok)}/1"
    # PROBE: live run of the probe against the committed output, bound to the live git
    probe_ok = False
    committed = root / next(iter(cfg["own"].values()))
    script = root / cfg["probe"]
    if committed.is_file() and script.is_file():
        tmp = pathlib.Path(a.work) if a.work else pathlib.Path(tempfile.mkdtemp(prefix="c2-"))
        try:
            p = subprocess.run([sys.executable, "-B", str(script), "--work", str(tmp / "probe")],
                               capture_output=True, text=True, timeout=300, stdin=subprocess.DEVNULL)
            m = re.search(r"PROBE_FACTS=(\d+)/(\d+)", p.stdout)
            ctext = committed.read_text(encoding="utf-8")
            same = probe_lines(p.stdout) == probe_lines(ctext)
            bound = (not cfg["bind_git"]) or any(l.startswith("HEADER ") and git_line in l for l in ctext.splitlines())
            probe_ok = p.returncode == 0 and bool(m) and m.group(1) == m.group(2) and same and bound
            if not probe_ok:
                detail.append(f"PROBE exit={p.returncode} facts={m.group(0) if m else None} same_as_committed={same} bound_to_live_git={bound}")
        except (OSError, subprocess.TimeoutExpired) as e:
            detail.append(f"PROBE could not run: {e}")
        finally:
            if not a.work:
                shutil.rmtree(tmp, ignore_errors=True)
    else:
        detail.append("PROBE script or committed output absent")
    res["PROBE"] = f"{int(probe_ok)}/1"
    readme = root / "corpus" / "README.md"
    res["MAP"] = f"{int(readme.is_file() and entry_rel in readme.read_text(encoding='utf-8'))}/1"
    c = subprocess.run(["bash", str(census), "validate", "--file", str(root / "corpus" / "SOURCES.md")],
                       capture_output=True, text=True, cwd=root)
    res["CENSUS"] = f"{int(c.returncode == 0)}/1"
    passed = all(v.split("/")[0] == v.split("/")[1] and v != "0/0" for v in res.values())
    print(" ".join(f"{k}={v}" for k, v in res.items()) + f" C2={'PASS' if passed else 'FAIL'}")
    for d in detail:
        print("  " + d)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
