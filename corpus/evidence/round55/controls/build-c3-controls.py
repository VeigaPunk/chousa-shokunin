#!/usr/bin/env python3
"""Build the R55-C3 controls as scratch lane roots under OUTDIR (outside the lane).

  restate/    BASE_REV tree + a `## Round 55 statement errata` block whose eleven lines anchor
              each statement exactly but restate the lane's own committed claim as the
              observation (the self-assessment copied, not re-observed).
  paraphrase/ BASE_REV tree + eleven lines carrying the observations the round-54 W2 seat
              reports state, with paraphrased anchors that do not occur in the targets.

Score: python3 corpus/evidence/round55/c3-count.py --root OUTDIR/<name>
Usage: python3 corpus/evidence/round55/controls/build-c3-controls.py OUTDIR
"""
from __future__ import annotations

import io
import pathlib
import subprocess
import sys
import tarfile

LANE = pathlib.Path(__file__).resolve().parents[4]
BASE_REV = "dba605deb5cd5ed4874e0e3c39ba24737409cd80"
R36 = "corpus/knowledge/source-type-taxonomy-r36.md"
Q = "corpus/QUALITY.md"
L54 = "corpus/lessons/round-54.md"
SUPP = "corpus/evidence/round54/c1-supplement.py"
# (item, target, exact anchor in target, the lane's own claim restated, W2 observation, W2 paraphrase anchor)
ROWS = [
    ("E01", R36, "the stronger claim that the text is unavailable belongs to no line here",
     "no line here", "该标准暂无全文，请等待更新 count=1 char=1712", "belongs to no line on the page"),
    ("E02", R36, "主管部门为 国家标准委 (char 575)", "主管部门为 国家标准委 char=575",
     "主管部门为 国家标准委 char=569", "主管部门为国家标准委 (char 575)"),
    ("E03", R36, "the document-type taxonomy the standard prescribes", "the standard prescribes the taxonomy",
     "附录 S121=0 S122=0; 文献类型 S121=0 S122=0", "the taxonomy that the standard prescribes"),
    ("E04", R36, "count 1 each, on one line", "count 1 each", "国家标准委 S121=2 S122=2",
     "count 1 each on one line"),
    ("E05", Q, "12,963 / 12,795", "located=11972,12007,12963,12795,14049,25123 drift=+802,+802,+970,+634,+802,-9251",
     "located=11972,12007,12795,12963,14049,25123 drift=+802,+802,+802,+802,+802,-9251", "12963 / 12795"),
    ("E06", Q, "18,242 control characters", "C0=18242", "C0=18451 C0_excl_tab_lf=18431 C0_excl_tab_lf_cr=18242",
     "18242 control characters"),
    ("E07", Q, "0 U+FFFD, 0 control characters", "form_C0=0", "form_C0=469 form_LF=469",
     "0 U+FFFD and 0 control characters"),
    ("E08", L54, "on a mirror without the two dumps `pointer-anchor-check.py` prints `BAD=6`", "BAD=6",
     "ANCHORED=7/16 UNANCHORED=9 BAD=9", "mirror without the two dumps prints `BAD=6`"),
    ("E09", Q, "and refuses a tool that delegates to that reader", "ctypes_system_under_hook rc=97 marker=ABSENT",
     "ctypes_system_under_hook rc=0 marker=SPAWNED", "refuses any tool that delegates to that reader"),
    ("E10", Q, "the SHELL control's receipt says the same", "SHELL LEGS=0/6", "SHELL LEGS=1/6",
     "the SHELL receipt says the same"),
    ("E11", SUPP, "randomly named directory outside the generation tree (no HTML, no", "oracle-echo SUPPLEMENT_LEGS=0/3",
     "oracle-echo SUPPLEMENT_LEGS=3/3", "outside the generation tree (no HTML, no sibling)"),
]


def base_tree(dst: pathlib.Path) -> None:
    arc = subprocess.run(["git", "-C", str(LANE), "archive", BASE_REV, "SCORECARD.md", "corpus"], capture_output=True, check=True)
    with tarfile.open(fileobj=io.BytesIO(arc.stdout)) as t:
        t.extractall(dst, filter="data")


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    out = pathlib.Path(sys.argv[1]).resolve()
    if out == LANE.resolve() or LANE.resolve() in out.parents:
        print("usage: OUTDIR must lie outside the lane", file=sys.stderr)
        return 2
    for name, pick in (("restate", lambda r: (r[2], r[3])), ("paraphrase", lambda r: (r[5], r[4]))):
        d = out / name
        base_tree(d)
        block = "\n## Round 55 statement errata\n\n" + "".join(
            f'erratum: {r[0]} {r[1]} anchor: "{pick(r)[0]}" observed: "{pick(r)[1]}"\n' for r in ROWS)
        with (d / "SCORECARD.md").open("a", encoding="utf-8") as f:
            f.write(block)
    print("restate paraphrase")
    return 0


if __name__ == "__main__":
    sys.exit(main())
