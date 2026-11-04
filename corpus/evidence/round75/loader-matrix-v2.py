#!/usr/bin/env python3
"""Round-75 successor loader matrix — twelve real-commit public-CLI cases, shuffled.

The round-74 matrix (`corpus/evidence/round74/loader-matrix.py`, sha256
979638251845071cfb2c5e130cd81800251c5a6cb041438deb258d8877e2ff8d) ran nine
cases in a fixed order. A source-blind counter that reads no repository bytes
at all — it counts its own invocations and replays the scripted answers — scores
9/9 on it (`corpus/evidence/round74/R74Critic/forge-order-oracle.log`), and a
diff-only counter that reads `git diff --numstat` and never opens a protected
file also scores 9/9, because all nine cases are decidable from the diff alone.

This matrix keeps the nine cases and adds three cases whose correct verdict is
decidable only from protected-file CONTENT: a second anchored heading appended
to each protected file, which the counter's exact count/section semantics must
reject while `git diff` still reports a pure append with no receipt change.

Two discriminations follow, both required by the round's frozen predicate:

  1. Case execution order is a random permutation drawn from
     `secrets.randbits(64)` at every run (QUALITY 120: the candidate cannot read
     the order); the seed is printed. An invocation-count oracle cannot map its
     n-th call to the n-th expected outcome.
  2. Three cases are append-only but structurally wrong, so a diff-only oracle
     expected to answer PASS returns the wrong check-id set (QUALITY 134: the
     verdict is bound to content, not to numstat).

Every case writes a real Git commit in a disposable fixture repository and
invokes the candidate through its public CLI (`--lane --base --rev`), so the
real `git show`/`git diff --numstat` loader path is exercised. Only disposable
fixture repositories are written; no network. `--work` is required.

Exit 0 only on 12/12; 1 on any mismatch; 2 setup.
"""
import argparse
import hashlib
import random
import secrets
from pathlib import Path
import subprocess
import sys
import tempfile

PATHS = ("LOG.md", "corpus/lessons/round-72.md", "SCORECARD.md")
RECEIPTS = (
    "corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt",
    "corpus/evidence/round72/controls/after-r72-corrections.txt",
)
LOG_HEAD = "## Round 72 correction entry"
LESSON_HEAD = "## Correction — round-72 spot-check"
CARD_HEAD = "## Round 72 correction note"

FILES = {
    PATHS[0]: "# Log\nremovable sentinel\n## Round 72 correction entry\n"
              "8426 is exempt; 8435 exits.\n",
    PATHS[1]: "# Lesson\nremovable sentinel\n## Correction — round-72 spot-check\n"
              "V72-1 8426 8435. V72-2 measured at the landing tip 7f7ea19a; "
              "three at the verdicts tree 6dd6c82; two recorded.\n",
    PATHS[2]: "# Scorecard\nremovable sentinel\n## Round 72 correction note\n"
              "V72-1 and V72-2.\n",
    RECEIPTS[0]: "historical battery\n",
    RECEIPTS[1]: "historical counts\n",
}

# name, path, operation, expected exit, expected failed check-id set
CASES = [("unchanged", None, "same", 0, frozenset())]
CASES += [(f"append-{i}", path, "append", 0, frozenset()) for i, path in enumerate(PATHS)]
CASES += [(f"delete-{i}", path, "delete", 1, frozenset({"C2-6"})) for i, path in enumerate(PATHS)]
CASES += [("replace-equal", PATHS[0], "replace", 1, frozenset({"C2-6"})),
          ("receipt-change", RECEIPTS[0], "append", 1, frozenset({"C2-7"})),
          # append-only but structurally wrong: decidable from content, never from numstat
          ("dup-log-heading", PATHS[0], "dup-log", 1, frozenset({"C2-1", "C2-2"})),
          ("dup-lesson-heading", PATHS[1], "dup-lesson", 1, frozenset({"C2-3", "C2-5"})),
          ("dup-card-heading", PATHS[2], "dup-card", 1, frozenset({"C2-4"}))]


def git(root, *args):
    p = subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.strip()[:400])
    return p.stdout.strip()


def mutate(text: str, operation: str) -> str:
    if operation == "append":
        return text + "\nadditional evidence\n"
    if operation == "delete":
        return text.replace("removable sentinel\n", "")
    if operation == "replace":
        return text.replace("removable sentinel", "replacement sentinel")
    if operation == "dup-log":
        return text + f"\n{LOG_HEAD}\n"
    if operation == "dup-lesson":
        return text + f"\n{LESSON_HEAD}\n"
    if operation == "dup-card":
        return text + f"\n{CARD_HEAD}\n"
    raise ValueError(operation)


def run(counter: Path, work: Path) -> int:
    seed = secrets.randbits(64)
    order = list(CASES)
    random.Random(seed).shuffle(order)
    passed = 0
    print("COUNTER_SHA256=" + hashlib.sha256(counter.read_bytes()).hexdigest())
    print(f"SEED={seed}")
    with tempfile.TemporaryDirectory(prefix="loader-matrix-v2-", dir=work) as tmp:
        root = Path(tmp)
        git(root, "init", "-q")
        if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
            raise RuntimeError("fixture root mismatch")
        for path, text in FILES.items():
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
        git(root, "add", "--", *FILES)
        git(root, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-qm", "base")
        base = git(root, "rev-parse", "HEAD")
        for name, path, operation, expected_rc, expected_failed in order:
            # Restore fixture bytes, never the caller's working tree or index.
            for key, value in FILES.items():
                (root / key).write_text(value)
            if path:
                (root / path).write_text(mutate(FILES[path], operation))
            git(root, "add", "--", *FILES)
            git(root, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
                "commit", "--allow-empty", "-qm", name)
            rev = git(root, "rev-parse", "HEAD")
            p = subprocess.run([sys.executable, "-B", str(counter), "--lane", str(root),
                                "--base", base, "--rev", rev], text=True, capture_output=True)
            checks = {line.split()[1]: line.split()[2] for line in p.stdout.splitlines()
                      if line.startswith("CHECK ")}
            failed = frozenset(key for key, value in checks.items() if value == "FAIL")
            summary = "PASS" if expected_rc == 0 else "FAIL"
            ok = (p.returncode == expected_rc and len(checks) == 7 and failed == expected_failed
                  and any(line.startswith("C2=" + summary + " checks=") for line in p.stdout.splitlines()))
            passed += ok
            print(f"CASE {name} {'PASS' if ok else 'FAIL'} expected_rc={expected_rc} "
                  f"actual_rc={p.returncode} failed={','.join(sorted(failed)) or 'none'} "
                  f"expected_failed={','.join(sorted(expected_failed)) or 'none'} base={base} rev={rev}")
            if not ok:
                print(p.stdout, end="")
                print(p.stderr, end="")
    print(f"LOADER_MATRIX={passed}/{len(CASES)} MATRIX={'PASS' if passed == len(CASES) else 'FAIL'}")
    return 0 if passed == len(CASES) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--counter", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    a = ap.parse_args()
    try:
        return run(a.counter.resolve(), a.work.resolve())
    except (OSError, RuntimeError) as exc:
        print(f"MATRIX_SETUP: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
