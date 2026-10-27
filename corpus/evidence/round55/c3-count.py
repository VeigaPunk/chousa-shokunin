#!/usr/bin/env python3
"""c3-count — frozen counter for round 55 claim C3 (calibration).

Predicate R55-C3, the same sentence as corpus/evidence/round55/claims.md:
each of the eleven lane self-statements E01-E11 below — committed at BASE_REV
and contradicted by an observation the round-54 W2 seats reported — carries,
in `SCORECARD.md` under the heading `## Round 55 statement errata`, an
appended line `erratum: <Exx> <target> anchor: "<A>" observed: "<O>"` whose
target is the item's target file, whose anchor A contains the item's key
phrase and occurs exactly once in that target at the counted tree (the
statement is corrected by an appended erratum, never rewritten away), and
whose observed text O equals, byte for byte, the observation this counter
computes from committed bytes at BASE_REV, the read-only capture cache and
probe runs it makes itself; the last `erratum:` line naming an item governs.

The counter never prints the observation it expects: an item prints `OK`,
`MISSING` (no erratum line), `ANCHOR` (anchor absent, repeated, or without the
key) or `WRONG` (observed text differs), then
`ERRATA=k/11 MISSING=m ANCHOR=a WRONG=w` and `C3=PASS` iff k == 11.

Items (target · key phrase · observation):
  E01 r36 entry · "belongs to no line here" · the S122 capture's latent
      no-full-text string: count and char offset
  E02 r36 entry · "主管部门为 国家标准委 (char 575)" · the phrase's offset in S121
  E03 r36 entry · "the document-type taxonomy the standard prescribes" ·
      counts of 附录 and 文献类型 in the S121 and S122 forms
  E04 r36 entry · "count 1 each, on one line" · count of 国家标准委 in both forms
  E05 QUALITY.md · "12,963 / 12,795" · the six S101 phrases located in the
      defined OLE form (BASE tool) and their drift from the stated anchors
  E06 QUALITY.md · "18,242 control characters" · C0 counts of the UTF-16LE
      decode under three exclusion sets
  E07 QUALITY.md · "0 U+FFFD, 0 control characters" · C0 and LF counts of the
      defined OLE form
  E08 lessons/round-54.md · "prints `BAD=6`" · pointer-anchor-check (BASE) on a
      BASE mirror without the two round-54 text-form dumps
  E09 QUALITY.md · "and refuses a tool that delegates to that reader" · a
      ctypes libc system() call run under the round-54 hook
  E10 QUALITY.md · "the SHELL control's receipt says the same" · the SHELL
      block's LEGS line in controls/c1-controls.txt
  E11 round54/c1-supplement.py · "outside the generation tree (no HTML, no" ·
      SUPPLEMENT_LEGS of an oracle-echo tool that never opens the `.doc`

Usage: python3 corpus/evidence/round55/c3-count.py [--root LANE] [--work DIR] [--skip-slow]
`--skip-slow` skips E11 (soffice) and then can never print C3=PASS.
Scratch: `--work`, default a mkdtemp under $TMPDIR, removed on exit.
Exit codes: 0 C3=PASS · 1 C3=FAIL · 2 usage/env (capture digest changed, no git).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

LANE = pathlib.Path(__file__).resolve().parents[3]
BASE_REV = "dba605deb5cd5ed4874e0e3c39ba24737409cd80"
CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
S121 = ("adf6ba934e813b2c326fa150.txt", "4e46154f4a841d17d858")
S122 = ("b9ca2a4fdf9455867534f144.txt", None)
S101RAW = ("6dc68fd6b32ce9c8dfcebce8.raw", "6063a3aff7a4081e93a6")
R36 = "corpus/knowledge/source-type-taxonomy-r36.md"
QUAL = "corpus/QUALITY.md"
L54 = "corpus/lessons/round-54.md"
SUPP = "corpus/evidence/round54/c1-supplement.py"
ITEMS = [
    ("E01", R36, "belongs to no line here"),
    ("E02", R36, "主管部门为 国家标准委 (char 575)"),
    ("E03", R36, "the document-type taxonomy the standard prescribes"),
    ("E04", R36, "count 1 each, on one line"),
    ("E05", QUAL, "12,963 / 12,795"),
    ("E06", QUAL, "18,242 control characters"),
    ("E07", QUAL, "0 U+FFFD, 0 control characters"),
    ("E08", L54, "prints `BAD=6`"),
    ("E09", QUAL, "and refuses a tool that delegates to that reader"),
    ("E10", QUAL, "the SHELL control's receipt says the same"),
    ("E11", SUPP, "outside the generation tree (no HTML, no"),
]
S101_ANCHORS = [
    (11170, "为便于文献的统计和期刊评价"),
    (11205, "每一篇文章或资料应根据其内容性质标识一个文献标志码"),
    (11993, "本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中规定的作者-出版年制。"),
    (12161, "文献类型及载体类型标志；"),
    (13247, "参照ISO 690及ISO 690-2，每一参考文献条目的末尾均以“.”结束。"),
    (34374, "参考文献格式，参照ISO 690"),
]
LINE_RE = re.compile(r'^erratum: (E\d\d) (\S+) anchor: "(.*)" observed: "(.*)"\s*$')
ECHO = r'''import html, pathlib, re, sys
p = pathlib.Path(sys.argv[1]); w = p.parent.parent
for o in sorted(w.glob("oracle-*/" + p.stem + ".txt")):
    sys.stdout.write(o.read_text(encoding="utf-8-sig")); sys.exit(0)
src = sorted((w / "src-iso").glob("*.html"))
if src:
    sys.stdout.write("\n".join(html.unescape(re.sub(r"<[^>]+>", " ", s.read_text(encoding="utf-8"))) for s in src)); sys.exit(0)
sys.exit(2)
'''


def env_fail(msg: str) -> None:
    print(f"ENV_CHANGED {msg}")
    sys.exit(2)


def git_show(path: str) -> bytes:
    r = subprocess.run(["git", "-C", str(LANE), "show", f"{BASE_REV}:{path}"], capture_output=True)
    if r.returncode != 0:
        env_fail(f"git show {BASE_REV[:12]}:{path}")
    return r.stdout


def cap_text(name: str, pin: str | None) -> str:
    p = CACHE / name
    if not p.is_file():
        env_fail(f"capture {name} missing")
    b = p.read_bytes()
    if pin and hashlib.sha256(b).hexdigest()[:20] != pin:
        env_fail(f"capture {name} digest")
    return b.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")


def base_tool(work: pathlib.Path):
    t = work / "base-capture-text.py"
    t.write_bytes(git_show("tools/capture-text.py"))
    spec = importlib.util.spec_from_file_location("base_capture_text", t)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def raw_bytes() -> bytes:
    p = CACHE / S101RAW[0]
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()[:20] != S101RAW[1]:
        env_fail(f"capture {S101RAW[0]} digest")
    return p.read_bytes()


def observe(work: pathlib.Path, slow: bool) -> dict[str, str | None]:
    a, b = cap_text(*S121), cap_text(*S122)
    obs: dict[str, str | None] = {}
    s = "该标准暂无全文，请等待更新"
    obs["E01"] = f"{s} count={b.count(s)} char={b.find(s)}"
    s = "主管部门为 国家标准委"
    obs["E02"] = f"{s} char={a.find(s)}"
    obs["E03"] = f"附录 S121={a.count('附录')} S122={b.count('附录')}; 文献类型 S121={a.count('文献类型')} S122={b.count('文献类型')}"
    obs["E04"] = f"国家标准委 S121={a.count('国家标准委')} S122={b.count('国家标准委')}"
    ct = base_tool(work)
    form = ct.text_form(str(CACHE / S101RAW[0]))
    raw_bytes()
    located = [form.find(q) if form.count(q) == 1 else -1 for _, q in S101_ANCHORS]
    drift = [f"{n - o:+d}" if n >= 0 else "?" for (o, _), n in zip(S101_ANCHORS, located)]
    obs["E05"] = f"located={','.join(map(str, located))} drift={','.join(drift)}"
    u = raw_bytes().decode("utf-16le", errors="replace")
    c0 = [ch for ch in u if ord(ch) < 0x20]
    obs["E06"] = (f"C0={len(c0)} C0_excl_tab_lf={sum(ch not in '\t\n' for ch in c0)} "
                  f"C0_excl_tab_lf_cr={sum(ch not in '\t\n\r' for ch in c0)}")
    obs["E07"] = f"form_C0={sum(ord(ch) < 0x20 for ch in form)} form_LF={form.count(chr(10))}"
    mirror = work / "mirror"
    mirror.mkdir()
    arc = subprocess.run(["git", "-C", str(LANE), "archive", BASE_REV], capture_output=True)
    if arc.returncode != 0:
        env_fail("git archive")
    subprocess.run(["tar", "-x", "-C", str(mirror)], input=arc.stdout, check=True)
    for d in ("S100-text-form.txt", "S101-text-form.txt"):
        (mirror / "corpus" / "evidence" / "round54" / d).unlink()
    pac = work / "pointer-anchor-check.py"
    pac.write_bytes(git_show("corpus/evidence/round53/pointer-anchor-check.py"))
    r = subprocess.run([sys.executable, str(pac), "--root", str(mirror)], capture_output=True, text=True, timeout=300)
    last = [l for l in r.stdout.splitlines() if l.startswith("ANCHORED=")]
    obs["E08"] = last[-1].strip() if last else f"rc={r.returncode} no ANCHORED line"
    hooksrc = git_show("corpus/evidence/round54/c1-count.py").decode("utf-8")
    m = re.search(r'HOOK = r"""\n(.*?)"""', hooksrc, re.S)
    if not m:
        env_fail("round-54 HOOK constant")
    (work / "hook.py").write_text(m.group(1))
    marker = work / "marker"
    (work / "probe.py").write_text(
        "import ctypes, sys\nctypes.CDLL(None).system(('printf SPAWNED > ' + sys.argv[1]).encode())\n")
    r = subprocess.run([sys.executable, str(work / "hook.py"), str(work / "probe.py"), str(marker)],
                       capture_output=True, timeout=60)
    obs["E09"] = f"ctypes_system_under_hook rc={r.returncode} marker={marker.read_text() if marker.is_file() else 'ABSENT'}"
    ctl = git_show("corpus/evidence/round54/controls/c1-controls.txt").decode("utf-8").split("## shell", 1)
    legs = re.findall(r"^LEGS=\S+", ctl[1], re.M) if len(ctl) == 2 else []
    obs["E10"] = f"SHELL {legs[0]}" if legs else "SHELL no LEGS line"
    obs["E11"] = None
    if slow:
        if not shutil.which("soffice"):
            env_fail("soffice not found")
        sw = work / "supp"
        echo = work / "echo.py"
        echo.write_text(ECHO)
        # the BASE supplement resolves LANE from its own path; run the BASE copies inside the BASE mirror
        mdir = mirror / "corpus" / "evidence" / "round54"
        r = subprocess.run([sys.executable, str(mdir / "c1-supplement.py"), "--tool", str(echo), "--seed", "11",
                            "--per-leg", "2", "--work", str(sw)], capture_output=True, text=True, timeout=1800,
                           env={**os.environ, "TMPDIR": str(work), "PYTHONDONTWRITEBYTECODE": "1"})
        legs = re.findall(r"^SUPPLEMENT_LEGS=\S+", r.stdout, re.M)
        obs["E11"] = f"oracle-echo {legs[-1]}" if legs else f"oracle-echo rc={r.returncode} no SUPPLEMENT_LEGS line"
    return obs


def errata(root: pathlib.Path) -> dict[str, tuple[str, str, str]]:
    sc = root / "SCORECARD.md"
    text = sc.read_text(encoding="utf-8") if sc.is_file() else ""
    out: dict[str, tuple[str, str, str]] = {}
    inside = False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Round 55 statement errata"
            continue
        m = LINE_RE.match(line) if inside else None
        if m:
            out[m.group(1)] = (m.group(2), m.group(3), m.group(4))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE))
    ap.add_argument("--work")
    ap.add_argument("--skip-slow", action="store_true")
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    own = a.work is None
    work = pathlib.Path(tempfile.mkdtemp(prefix="r55c3-")) if own else pathlib.Path(a.work)
    work.mkdir(parents=True, exist_ok=True)
    if any(work.iterdir()):
        print("usage: --work must be empty", file=sys.stderr)
        return 2
    try:
        obs = observe(work, not a.skip_slow)
    finally:
        if own:
            shutil.rmtree(work, ignore_errors=True)
    lines = errata(root)
    k = miss = anc = wrong = 0
    for iid, target, keyp in ITEMS:
        if iid not in lines:
            print(f"{iid} MISSING")
            miss += 1
            continue
        tgt, anchor, observed = lines[iid]
        tp = root / target
        ttext = tp.read_text(encoding="utf-8") if tp.is_file() else ""
        if tgt != target or keyp not in anchor or ttext.count(anchor) != 1:
            print(f"{iid} ANCHOR")
            anc += 1
        elif obs[iid] is None or observed != obs[iid]:
            print(f"{iid} WRONG" + (" (slow item skipped)" if obs[iid] is None else ""))
            wrong += 1
        else:
            print(f"{iid} OK")
            k += 1
    print(f"ERRATA={k}/{len(ITEMS)} MISSING={miss} ANCHOR={anc} WRONG={wrong}")
    ok = k == len(ITEMS)
    print("C3=PASS" if ok else "C3=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
