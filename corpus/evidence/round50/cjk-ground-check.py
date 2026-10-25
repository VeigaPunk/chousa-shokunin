#!/usr/bin/env python3
"""cjk-ground-check — shows the round-50 `tools/inference-ground.py` CJK change able to fail, in scratch.

Before the change a bullet whose only grounding quote is a pure-Chinese phrase read as zero grounding tokens
(`INF_UNGROUNDED`); after it the phrase is a token that must occur in a cited span. Three cases in a scratch dir:
  A  correct bullet, phrase in the span        -> must exit 0 (the old tool exits 1: the blind spot)
  B  bullet quoting a phrase NOT in the span    -> must exit 1 INF_TOKEN_NOT_IN_SPAN (a blind tool exits 1 for the
     wrong reason, INF_UNGROUNDED, so the reason is checked)
  C  bullet citing no id                        -> must exit 1 INF_UNCITED
Usage: python3 cjk-ground-check.py [--old TOOL]   (--old: the pre-change tool, to print the A-case blind spot)
Exit 0 all three cases behave; 1 a case misbehaves; 2 usage."""
import argparse
import pathlib
import subprocess
import sys
import tempfile

LANE = pathlib.Path(__file__).resolve().parents[3]
ap = argparse.ArgumentParser()
ap.add_argument("--old")
ap.add_argument("--tool", default=str(LANE / "tools" / "inference-ground.py"))
a = ap.parse_args()
d = pathlib.Path(tempfile.mkdtemp(prefix="chousa-r50-cjk-"))
span = "该列表的第一列显示的是是否查找到该引用文献，及引文内容的正确性。"
(d / "s.txt").write_text("前文。" + span + "后文。", encoding="utf-8")
(d / "spans.tsv").write_text("id\turl\tcapture_sha256\toffset\tspan_file\tquote\tentry\n"
                             f"S900\thttps://example.test/x\t{'0' * 64}\t0\ts.txt\t{span}\te.md\n", encoding="utf-8")
(d / "reg.md").write_text("## Registry\n\n| S900 | doc — https://example.test/x | docs | B | s | a | t | mined | 2026-10-25 | 90d | — |\n", encoding="utf-8")
head = "source: S900 — https://example.test/x\nverified-at: 2026-10-25\nrecheck: 90d\n\n#### Inference\n\n"
cases = {
    "A": (head + f"- The list's first column reports found-ness and correctness: `{span}` (S900).\n", 0, None),
    "B": (head + "- The list reports a verdict: `该列表显示最终的判定结论并给出评分` (S900).\n", 1, "INF_TOKEN_NOT_IN_SPAN"),
    "C": (head + f"- The list's first column reports found-ness: `{span}`.\n", 1, "INF_UNCITED"),
}


def run(tool: str, entry: pathlib.Path) -> tuple[int, str]:
    p = subprocess.run([sys.executable, tool, "--entry", str(entry), "--spans", str(d / "spans.tsv"), "--counts", "/dev/null",
                        "--registry", str(d / "reg.md"), "--root", str(d)], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


ok = True
for k, (text, want_rc, want_tag) in cases.items():
    e = d / f"{k}.md"
    e.write_text(text, encoding="utf-8")
    rc, out = run(a.tool, e)
    good = rc == want_rc and (want_tag is None or want_tag in out)
    ok &= good
    print(f"CASE {k} rc={rc} want={want_rc} tag={want_tag or '-'} -> {'PASS' if good else 'FAIL'}")
    if a.old and k == "A":
        rc0, out0 = run(a.old, e)
        print(f"OLD_TOOL case A rc={rc0} {'INF_UNGROUNDED' if 'INF_UNGROUNDED' in out0 else out0.strip()[:80]}")
print("CJK_GROUND=" + ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
