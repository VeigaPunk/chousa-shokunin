#!/usr/bin/env python3
"""R76Mutation: generate single-point mutants of the frozen r76 instruments.

Frozen bytes are only read. Every substitution asserts exactly one occurrence
(fail-closed) and every mutant is compiled and diffed against its parent.
"""
import difflib
import hashlib
import pathlib
import py_compile
import sys

S = pathlib.Path("/fast/scratch/hyaku/chousa-r76/R76Mutation")
R = S / "replica/corpus/evidence/round76"
MATRIX = (R / "loader-matrix-v3.py").read_text()
BATTERY = (R / "matrix-battery-v3.py").read_text()
MUT = S / "mut"
OUT = S / "out"

FROZEN_SHA = {
    "loader-matrix-v3.py": "b79d6441057a01b27eb465c6b0625cd46502114f8b622b370c2cd2805c81913f",
    "matrix-battery-v3.py": "217ae367c7e6e4ed23d1e6c1412de50370f309ba12d4a1703eaff386b7094360",
}


def sub(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"FATAL {label}: expected 1 occurrence, found {n}")
    return text.replace(old, new)


SHUFFLE = '''    order = list(CASES)
    random.Random(seed).shuffle(order)
'''

OK_HEAD = "            ok = (not timed_out and rc == expected_rc and len(checks) == len(CHECK_IDS)\n"
FAILSET = "                  and failed == expected_failed\n"
C2LINE = '                  and any(line.startswith("C2=" + summary + " checks=") for line in out.splitlines()))\n'
COMMIT_CASE = '"--allow-empty", "-qm", "case")'
SALTED_RET = '    return {path: text + f"\\nsalt {salt}-{i}\\n" for i, (path, text) in enumerate(FILES.items())}\n'
PAD_RET = '    return "\\n" + "pad " + secrets.token_hex(random.randint(2, 20)) + "\\n"\n'
RESTORE = '''            for key, value in files.items():
                (root / key).write_text(value)
'''
TIMEOUT_BLOCK = '''    timed_out = False
    try:
        out, _err = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        out, _err = p.communicate()
'''
SUBJECT_ANCHOR = 'CHECK_IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")\n'

V2_KEYS = '''CHECK_IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")

# MUTANT: the r75 v2 commit-subject answer key restored.
V2_KEYS = ("unchanged", "append-0", "append-1", "append-2", "delete-0", "delete-1",
           "delete-2", "replace-equal", "receipt-change", "dup-log-heading",
           "dup-lesson-heading", "dup-card-heading")
SUBJECT = {name: key for (name, *_rest), key in zip(CASES, V2_KEYS)}
'''
CASE_NAME_SUBJECT = '''CHECK_IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")

# MUTANT: each commit subject is the case's own name (class leaks in the subject).
SUBJECT = {name: name for (name, *_rest) in CASES}
'''

MATRIX_MUTANTS = []


def mm(mid, note, text):
    MATRIX_MUTANTS.append((mid, note, text))


mm("M01-drop-shuffle", "case order is the declared order; `secrets` seed no longer reorders",
   sub(MATRIX, SHUFFLE, "    order = list(CASES)  # MUTANT M01: shuffle dropped\n", "M01"))
mm("M02-subject-v2key", "case commits are named after the r75 v2 answer key",
   sub(sub(MATRIX, SUBJECT_ANCHOR, V2_KEYS, "M02a"),
       COMMIT_CASE, '"--allow-empty", "-qm", SUBJECT[name])', "M02b"))
mm("M03-subject-case-name", "case commits carry the case name (class label in the subject)",
   sub(sub(MATRIX, SUBJECT_ANCHOR, CASE_NAME_SUBJECT, "M03a"),
       COMMIT_CASE, '"--allow-empty", "-qm", SUBJECT[name])', "M03b"))
mm("M04-drop-salt", "per-run salt line removed: fixture bytes are byte-stable across runs",
   sub(MATRIX, SALTED_RET, "    return dict(FILES)  # MUTANT M04: no per-run salt\n", "M04"))
mm("M05-drop-pad", "per-run random-length pad removed: size deltas become class-stable",
   sub(MATRIX, PAD_RET, '    return ""  # MUTANT M05: no per-run pad\n', "M05"))
mm("M06-accept-child-exit2", "a candidate exiting 2 satisfies the expected exit code",
   sub(MATRIX, OK_HEAD, "            ok = (not timed_out and (rc == expected_rc or rc == 2) and len(checks) == len(CHECK_IDS)\n", "M06"))
mm("M07-ignore-expected-failed", "the expected failed check-id set is not asserted",
   sub(MATRIX, FAILSET, "                  # MUTANT M07: expected failed set ignored\n", "M07"))
mm("M08-ignore-c2-summary", "the `C2=` per-case summary line is not asserted",
   sub(MATRIX, C2LINE, "                  )  # MUTANT M08: C2= summary ignored\n", "M08"))
mm("M09-skip-timeout-kill", "no child bound and no process-group kill (v2 behaviour)",
   sub(MATRIX, TIMEOUT_BLOCK,
       "    timed_out = False\n    out, _err = p.communicate()  # MUTANT M09: no bound, no kill\n", "M09"))
mm("M10-timeout-counts-pass", "a case that timed out counts as a passed case",
   sub(MATRIX, "            passed += ok\n", "            passed += (True if timed_out else ok)  # MUTANT M10\n", "M10"))
mm("M11-drop-restore", "fixture bytes are not restored between cases (mutations compound)",
   sub(MATRIX, RESTORE, "            pass  # MUTANT M11: fixture not restored\n", "M11"))
mm("M12-pass-exits-2", "the matrix reports a PASS verdict with usage/setup exit code 2",
   sub(MATRIX, '    return 0 if verdict == "PASS" else 1\n',
       '    return 2 if verdict == "PASS" else 1  # MUTANT M12\n', "M12"))
mm("M13-flaky-order", "shuffle only on the first invocation sharing a work parent (run flake)",
   sub(MATRIX, SHUFFLE,
       '    order = list(CASES)\n'
       '    marker = work.parent / "mut-flaky.marker"\n'
       '    if not marker.exists():  # MUTANT M13: shuffle the first run only\n'
       '        marker.write_text("x")\n'
       '        random.Random(seed).shuffle(order)\n', "M13"))

B_POS = '''                if group == "POSITIVE":
                    ok = all(rc == 0 and marks is not None and marks[0] == marks[1] and marks[2] == "PASS"
                             for rc, marks in runs)
                else:
                    ok = all(rc == 1 and marks is not None and marks[0] < marks[1]
                             for rc, marks in runs)
'''
BATTERY_MUTANTS = []


def bm(mid, note, text):
    BATTERY_MUTANTS.append((mid, note, text))


bm("B01-forger-single-run", "a forger is scored on its first run only",
   sub(BATTERY,
       '                    ok = all(rc == 1 and marks is not None and marks[0] < marks[1]\n'
       '                             for rc, marks in runs)\n',
       '                    ok = (runs[0][0] == 1 and runs[0][1] is not None\n'
       '                          and runs[0][1][0] < runs[0][1][1])  # MUTANT B01: first run only\n',
       "B01"))
bm("B02-positive-exit2", "a positive is accepted when the matrix exits 2 (never scored in its favour)",
   sub(BATTERY,
       '                    ok = all(rc == 0 and marks is not None and marks[0] == marks[1] and marks[2] == "PASS"\n',
       '                    ok = all(rc in (0, 2) and marks is not None and marks[0] == marks[1] and marks[2] == "PASS"\n',
       "B02"))

# frozen bytes must be untouched
for name, want in FROZEN_SHA.items():
    got = hashlib.sha256((R / name).read_bytes()).hexdigest()
    if got != want:
        raise SystemExit(f"FATAL frozen {name} sha {got} != {want}")

MUT.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
written = []
for mid, note, text in MATRIX_MUTANTS:
    p = MUT / f"mut-{mid}-matrix-v3.py"
    p.write_text(text)
    py_compile.compile(str(p), doraise=True)
    d = "".join(difflib.unified_diff(MATRIX.splitlines(True), text.splitlines(True),
                                     "loader-matrix-v3.py", p.name))
    (OUT / f"{mid}.diff").write_text(d)
    written.append((str(p), mid, note, hashlib.sha256(text.encode()).hexdigest(),
                    sum(1 for line in d.splitlines() if line.startswith(("+", "-"))
                        and not line.startswith(("+++", "---")))))
for mid, note, text in BATTERY_MUTANTS:
    p = R / f"mut-{mid}-battery-v3.py"
    p.write_text(text)
    py_compile.compile(str(p), doraise=True)
    d = "".join(difflib.unified_diff(BATTERY.splitlines(True), text.splitlines(True),
                                     "matrix-battery-v3.py", p.name))
    (OUT / f"{mid}.diff").write_text(d)
    written.append((str(p), mid, note, hashlib.sha256(text.encode()).hexdigest(),
                    sum(1 for line in d.splitlines() if line.startswith(("+", "-"))
                        and not line.startswith(("+++", "---")))))

for path, mid, note, sha, nlines in written:
    print(f"WROTE {path}\n  sha256={sha} diff_lines={nlines} :: {note}")
print(f"MUTANTS={len(written)}")
