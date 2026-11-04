#!/usr/bin/env python3
"""Reviewer probe: can a correction block pass c2-count 4/4 while NOT naming the
recorded 18/13 AS superseded values (the claim's Q3 meaning)?

Fixture is disposable and lives under the reviewer scratch root; commits use a
throwaway identity confined to the fixture.
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path("/fast/scratch/hyaku/chousa-r75/R75Review/lane").resolve()
BASE = "8022f72c889c904b5657d52c7f29e1643392a216"
LESSON = "corpus/lessons/round-74.md"
COUNTER = LANE / "corpus/evidence/round75/c2-count.py"


def git(root, *args):
    p = subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True)
    if p.returncode:
        raise SystemExit(f"git {' '.join(args)} rc={p.returncode}: {p.stderr[:300]}")
    return p.stdout.strip()


def run_case(name, block):
    with tempfile.TemporaryDirectory(prefix="c2probe-", dir=os.environ["S"]) as tmp:
        root = Path(tmp)
        git(root, "init", "-q")
        assert Path(git(root, "rev-parse", "--show-toplevel")).resolve() == root.resolve()
        text = subprocess.run(["git", "-C", str(LANE), "show", f"{BASE}:{LESSON}"],
                              text=True, capture_output=True, check=True).stdout
        target = root / LESSON
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        git(root, "add", "--", LESSON)
        git(root, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-qm", "base")
        base = git(root, "rev-parse", "HEAD")
        target.write_text(text + block)
        git(root, "add", "--", LESSON)
        git(root, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-qm", name)
        rev = git(root, "rev-parse", "HEAD")
        p = subprocess.run([sys.executable, "-B", str(COUNTER), "--lane", str(root),
                            "--base", base, "--rev", rev], text=True, capture_output=True)
        print(f"##### {name} exit={p.returncode}")
        print(p.stdout, end="")
        return p.returncode


BLOCK_INTENDED = ("\n## Correction — round-74 quote counts\n"
                  "The located quotes carry 16 words and 11 whitespace tokens; the recorded "
                  "18-word and 13-token figures were wrong and are superseded.\n")
# Names neither recorded value as a superseded count: "18" occurs only inside "S182",
# "13" only as an unrelated net-line figure.
BLOCK_UNDERENFORCED = ("\n## Correction — round-74 quote counts\n"
                       "S182 re-derives to 16 and S183 to 11; the counter scores 4/4 with "
                       "13 net added lines.\n")

# States neither derived count nor superseded value; "116" covers Q2's substrings.
BLOCK_SUBSTRING = ("\n## Correction — round-74 quote counts\n"
                   "The two located quotes total 116 characters; S182 and S183 are "
                   "re-derived in the 13-line note.\n")

def run_midcase():
    """Block inserted mid-document (not appended at the end): still zero deletions."""
    with tempfile.TemporaryDirectory(prefix="c2probe-", dir=os.environ["S"]) as tmp:
        root = Path(tmp)
        git(root, "init", "-q")
        assert Path(git(root, "rev-parse", "--show-toplevel")).resolve() == root.resolve()
        text = subprocess.run(["git", "-C", str(LANE), "show", f"{BASE}:{LESSON}"],
                              text=True, capture_output=True, check=True).stdout
        target = root / LESSON
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        git(root, "add", "--", LESSON)
        git(root, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-qm", "base")
        base = git(root, "rev-parse", "HEAD")
        lines = text.splitlines(True)
        inserted = lines[:1] + ["\n" + BLOCK_INTENDED.strip() + "\n"] + lines[1:]
        target.write_text("".join(inserted))
        git(root, "add", "--", LESSON)
        git(root, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-qm", "mid-insert")
        rev = git(root, "rev-parse", "HEAD")
        p = subprocess.run([sys.executable, "-B", str(COUNTER), "--lane", str(root),
                            "--base", base, "--rev", rev], text=True, capture_output=True)
        print(f"##### mid-insert (not at EOF) exit={p.returncode}")
        print(p.stdout, end="")
        return p.returncode


codes = [run_case("intended", BLOCK_INTENDED), run_midcase(),
         run_case("underenforced", BLOCK_UNDERENFORCED),
         run_case("substring", BLOCK_SUBSTRING)]
sys.exit(0 if all(c == 0 for c in codes) else 1)
