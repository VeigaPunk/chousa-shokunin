#!/usr/bin/env python3
"""Round-76 successor loader matrix — twelve public-CLI cases, answer-key channels salted.

Unit under test: the correction counter `corpus/evidence/round74/correction-count.py`
through its real public CLI. Each run writes ONE disposable fixture repository under
`--work`, commits the salted base, then one commit per case, restoring the fixture
bytes before each case. The real `git show` / `git diff --numstat` loader path is
exercised; no network.

Answer-key channels closed against the round-75 v2 matrix (contract unchanged):

- **Commit subject.** Every case commit carries the literal subject `case`; no case
  name reaches the fixture. (v2 named each commit after its case: a subject oracle
  scored 12/12 without opening a blob.)
- **Tree identity and byte sizes.** Every fixture file body carries a per-run random
  salt line, and every mutation appends a per-run random-length pad line, so no case
  has a stable tree id, blob size or size delta across runs. (v2 was byte-stable:
  a tree-hash memo and an `ls-tree -l` size map each scored 12/12.)
- **Unbounded child.** The candidate runs in its own session under a wall-clock
  bound, `LOADER_MATRIX_CHILD_TIMEOUT` seconds (default 20, minimum 1); on expiry the
  process group is killed and the case is a failure. (v2 let a candidate stall the
  matrix.)
- **Seed.** The run seed is never printed; only its digest, so a reader of the
  matrix's own output cannot replay the shuffle.

Case order is drawn from `secrets.randbits(64)` per run and is not recoverable from
the fixture: a twelve-entry declared-order oracle sees an unknown permutation.

Exit 0 only on all cases; 1 on any mismatch; 2 setup.

Limits (recorded, not closed): this proves the twelve content-decidable cases below.
A counter that reads the unified patch text is reading protected-file content and is
not a forge of this matrix; a counter that re-implements every check is, for these
inputs, a correct counter. `--lane` bytes are disposable; the caller's tree is never
written.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import random
import secrets
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

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

# name, path, operation, expected exit, expected failed check-id set.
# Internal names never reach the fixture (every commit subject is the literal `case`).
CASES = [("case-00-unchanged", None, "same", 0, frozenset())]
CASES += [(f"case-0{i + 1}-append", path, "append", 0, frozenset()) for i, path in enumerate(PATHS)]
CASES += [(f"case-0{i + 4}-delete", path, "delete", 1, frozenset({"C2-6"})) for i, path in enumerate(PATHS)]
CASES += [("case-07-replace-equal", PATHS[0], "replace", 1, frozenset({"C2-6"})),
          ("case-08-receipt-change", RECEIPTS[0], "append", 1, frozenset({"C2-7"})),
          # append-only but structurally wrong: decidable from content, never from numstat
          ("case-09-dup-log-heading", PATHS[0], "dup-log", 1, frozenset({"C2-1", "C2-2"})),
          ("case-10-dup-lesson-heading", PATHS[1], "dup-lesson", 1, frozenset({"C2-3", "C2-5"})),
          ("case-11-dup-card-heading", PATHS[2], "dup-card", 1, frozenset({"C2-4"}))]

CHECK_IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")


def git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.strip()[:400])
    return p.stdout.strip()


def pad_line() -> str:
    """Per-case random-length padding: no case keeps a stable size signature."""
    return "\n" + "pad " + secrets.token_hex(random.randint(2, 20)) + "\n"


def salted(salt: str) -> dict[str, str]:
    """Per-run salt in every file body: no case keeps a stable tree id or blob size."""
    return {path: text + f"\nsalt {salt}-{i}\n" for i, (path, text) in enumerate(FILES.items())}


def mutate(text: str, operation: str) -> str:
    pad = pad_line()
    if operation == "append":
        return text + "\nadditional evidence\n" + pad
    if operation == "delete":
        return text.replace("removable sentinel\n", "") + pad
    if operation == "replace":
        return text.replace("removable sentinel", "replacement sentinel") + pad
    if operation == "dup-log":
        return text + f"\n{LOG_HEAD}\n" + pad
    if operation == "dup-lesson":
        return text + f"\n{LESSON_HEAD}\n" + pad
    if operation == "dup-card":
        return text + f"\n{CARD_HEAD}\n" + pad
    raise ValueError(operation)


def run_child(counter: Path, root: Path, base: str, rev: str, timeout: int):
    """Return (rc, out, timed_out). Child in its own session, killed on expiry."""
    cmd = [sys.executable, "-B", str(counter), "--lane", str(root), "--base", base, "--rev", rev]
    p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True, start_new_session=True,
                         close_fds=True)
    timed_out = False
    try:
        out, _err = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        out, _err = p.communicate()
    return p.returncode, out, timed_out


def run(counter: Path, work: Path, child_timeout: int) -> int:
    seed = secrets.randbits(64)
    print("COUNTER_SHA256=" + hashlib.sha256(counter.read_bytes()).hexdigest())
    print("SEED_SHA256=" + hashlib.sha256(str(seed).encode()).hexdigest())
    print(f"CHILD_TIMEOUT={child_timeout}")
    order = list(CASES)
    random.Random(seed).shuffle(order)
    files = salted(secrets.token_hex(8))
    passed = 0
    with tempfile.TemporaryDirectory(prefix="loader-matrix-v3-", dir=work) as tmp:
        root = Path(tmp)
        git(root, "init", "-q")
        if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
            raise RuntimeError("fixture root mismatch")
        for path, text in files.items():
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
        git(root, "add", "--", *files)
        git(root, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-qm", "case")
        base = git(root, "rev-parse", "HEAD")
        for name, path, operation, expected_rc, expected_failed in order:
            # Restore fixture bytes, never the caller's working tree or index.
            for key, value in files.items():
                (root / key).write_text(value)
            if path:
                (root / path).write_text(mutate(files[path], operation))
            git(root, "add", "--", *files)
            git(root, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
                "commit", "--allow-empty", "-qm", "case")
            rev = git(root, "rev-parse", "HEAD")
            rc, out, timed_out = run_child(counter, root, base, rev, child_timeout)
            checks = {}
            for line in out.splitlines():
                parts = line.split()
                if len(parts) >= 3 and parts[0] == "CHECK" and parts[1] in CHECK_IDS:
                    checks[parts[1]] = parts[2]
            failed = frozenset(key for key, value in checks.items() if value == "FAIL")
            summary = "PASS" if expected_rc == 0 else "FAIL"
            ok = (not timed_out and rc == expected_rc and len(checks) == len(CHECK_IDS)
                  # MUTANT M07: expected failed set ignored
                  and any(line.startswith("C2=" + summary + " checks=") for line in out.splitlines()))
            passed += ok
            print(f"CASE {name} {'PASS' if ok else 'FAIL'} expected_rc={expected_rc} "
                  f"actual_rc={rc} timeout={timed_out} failed={','.join(sorted(failed)) or 'none'} "
                  f"expected_failed={','.join(sorted(expected_failed)) or 'none'}")
    total = len(order)
    verdict = "PASS" if passed == total else "FAIL"
    print(f"LOADER_MATRIX={passed}/{total} MATRIX={verdict}")
    return 0 if verdict == "PASS" else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    try:
        child_timeout = int(os.environ.get("LOADER_MATRIX_CHILD_TIMEOUT", "20"))
    except ValueError:
        print("loader-matrix: LOADER_MATRIX_CHILD_TIMEOUT must be an integer", file=sys.stderr)
        return 2
    if child_timeout < 1:
        print("loader-matrix: LOADER_MATRIX_CHILD_TIMEOUT must be >= 1", file=sys.stderr)
        return 2
    counter = Path(a.counter).resolve()
    work = Path(a.work).resolve()
    if not counter.is_file():
        print(f"loader-matrix: missing counter {counter}", file=sys.stderr)
        return 2
    work.mkdir(parents=True, exist_ok=True)
    return run(counter, work, child_timeout)


if __name__ == "__main__":
    sys.exit(main())
