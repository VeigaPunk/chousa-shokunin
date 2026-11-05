#!/usr/bin/env python3
"""R79ReviewB independent C2 attack driver. Builds every fixture in a scratch clone of the
lane and runs the FROZEN counters from the lane tree (read-only, -B). Receipts -> wave folder."""
import hashlib
import pathlib
import subprocess

S = pathlib.Path("/fast/scratch/hyaku/chousa-r79/R79ReviewB")
M = S / "mirror"
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
R = LANE / ".ufo/waves/round-79/w1/R79ReviewB"
BASE = "ee70e6df19fe43b1b384166cf5d360c3b99dafe2"
HEAD = "b58a02dbc8876dd1ad7647d88ca2c9cb2ae51ff9"
V1 = LANE / "corpus/evidence/round78/selfcheck.py"
V2 = LANE / "corpus/evidence/round79/selfcheck-v2.py"
R.mkdir(parents=True, exist_ok=True)
SUMMARY: list[str] = []


def git(*a, cwd=M):
    return subprocess.run(["git", "-C", str(cwd), *a], capture_output=True, text=True,
                          check=True).stdout


def assert_mirror():
    top = pathlib.Path(git("rev-parse", "--show-toplevel").strip())
    assert top == M, f"toplevel {top} is not the mirror"


def reset(rev):
    assert_mirror()
    git("reset", "-q", "--hard", rev)
    git("clean", "-qfd")


def run(label, script, *args, cwd=M):
    p = subprocess.run(["python3", "-B", str(script), *args], capture_output=True, text=True,
                       cwd=str(cwd))
    body = p.stdout + (("STDERR:\n" + p.stderr) if p.stderr else "") + f"EXIT={p.returncode}\n"
    (R / f"{label}.txt").write_text(body)
    pred = [x for x in p.stdout.splitlines() if x.startswith("SELFCHECK")]
    SUMMARY.append(f"{label}: {pred[-1] if pred else '(no predicate line)'} exit={p.returncode}")
    return p.returncode


def pair(label, rev):
    run(f"{label}-v1", V1, "--lane", str(M))
    run(f"{label}-v2", V2, "--lane", str(M))
    (R / f"{label}.diff").write_text(git("diff", rev))


def append(rel, text):
    p = M / rel
    t = p.read_text()
    if t and not t.endswith("\n"):
        t += "\n"
    p.write_text(t + text)


def replace_once(rel, old, new):
    p = M / rel
    t = p.read_text()
    assert t.count(old) == 1, (rel, t.count(old))
    p.write_text(t.replace(old, new))


def drop_lines(rel, prefix):
    p = M / rel
    lines = p.read_text().splitlines(keepends=True)
    keep = [l for l in lines if not l.startswith(prefix)]
    assert len(keep) == len(lines) - 1, (rel, prefix)
    p.write_text("".join(keep))


# --- instruments and lane state (read-only) ---
digests = []
for path in (V1, V2, LANE / "corpus/evidence/round79/selfcheck-control.py"):
    digests.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(LANE)}")
(R / "instrument-digests.txt").write_text("\n".join(digests) + "\n")
(R / "lane-status-before.txt").write_text(git("status", "--porcelain", cwd=LANE))
(R / "lane-head.txt").write_text(git("rev-parse", "HEAD", cwd=LANE))

# --- 00 pristine base in the scratch clone ---
reset(BASE)
pair("00-base", BASE)
run("00-base-v2-digests", V2, "--lane", str(M), "--digests")
run("00-lane-rev-base-v1", V1, "--lane", str(LANE), "--rev", BASE, cwd=LANE)
run("00-lane-rev-base-v2", V2, "--lane", str(LANE), "--rev", BASE, cwd=LANE)

# --- 01 HOLLOW: three digest-hollow repair lines on the base bytes ---
reset(BASE)
append("SKILL.md", "correction: SKILL.md:168 cells=8 digest=deadbeefdeadbeef\n")
append("corpus/QUALITY.md",
       "\n149. **Hollow repair probe (review fixture R79ReviewB).** This appended criterion "
       "carries supersedes: 116 digest=deadbeefdeadbeef while its own single pointer token, "
       "`corpus/QUALITY.md`, resolves against the committed tree.\n")
append("corpus/lessons/round-77.md", "erratum: round-77.md:73 digest=deadbeefdeadbeef\n")
pair("01-hollow", BASE)

# --- 02 WINDOW: newer round block with one resolving criterion; 116 untouched ---
reset(BASE)
append("corpus/QUALITY.md",
       "\n## Round-79 addition (review fixture R79ReviewB)\n\n149. **Pointer hygiene probe "
       "(review fixture R79ReviewB).** The criteria added by a round addition block cite only "
       "committed paths; this probe's own pointer token, `corpus/QUALITY.md`, resolves.\n")
pair("02-window", BASE)

# --- 03 PARTIAL: lane HEAD bytes, one digit of the S1 digest broken ---
reset(HEAD)
replace_once("SKILL.md", "correction: SKILL.md:168 cells=7 digest=e6e751ec67878243",
             "correction: SKILL.md:168 cells=7 digest=e6e751ec67878244")
pair("03-partial-one-digit", HEAD)

# --- 04 HEAD honest copy (unmodified lane bytes in scratch) ---
reset(HEAD)
pair("04-head-honest", HEAD)
run("04-lane-worktree-v1", V1, "--lane", str(LANE), cwd=LANE)
run("04-lane-worktree-v2", V2, "--lane", str(LANE), cwd=LANE)

# --- 05 DUPID: honest S1+S3 repairs, plus a restated criterion 116 (dead pointer stays) ---
reset(BASE)
append("SKILL.md", "correction: SKILL.md:168 cells=7 digest=e6e751ec67878243\n")
append("corpus/lessons/round-77.md", "erratum: round-77.md:73 digest=7f2d54a7eb33df54\n")
append("corpus/QUALITY.md",
       "\n116. **Restated pointer (duplicate id probe, R79ReviewB).** Pointer `corpus/QUALITY.md` "
       "resolves; the defect of criterion 116 is not repaired here.\n")
(R / "05-dupid-deadpointer-grep.txt").write_text(
    git("grep", "-n", "corpus/evidence/round59/claims.md", "--", "corpus/QUALITY.md"))
pair("05-dupid", BASE)

# --- 06 BLANKWINDOW: blank line before the malformed row 168 (correction kept) ---
reset(HEAD)
lines = (M / "SKILL.md").read_text().splitlines(keepends=True)
idx = [i for i, l in enumerate(lines) if l.startswith("| `round77 order-and-content battery`")]
assert len(idx) == 1, idx
row = lines[idx[0]]
(R / "06-row168-pipes.txt").write_text(
    f"row168 pipes={row.count('|')} (header has 9 pipes = 8 cells; row is 7 cells)\n")
lines.insert(idx[0], "\n")
(M / "SKILL.md").write_text("".join(lines))
pair("06-blankwindow-correction-kept", HEAD)

# --- 07 BLANKWINDOW-NOREPAIR: as 06 and the 168 correction line removed ---
reset(HEAD)
lines = (M / "SKILL.md").read_text().splitlines(keepends=True)
idx = [i for i, l in enumerate(lines) if l.startswith("| `round77 order-and-content battery`")]
lines.insert(idx[0], "\n")
(M / "SKILL.md").write_text("".join(lines))
drop_lines("SKILL.md", "correction: SKILL.md:168 cells=")
pair("07-blankwindow-no-repair", HEAD)

# --- 08 CLASS: stranded-looking rows; first cell literal 'class' vs plain ---
reset(BASE)
append("corpus/lessons/round-77.md",
       "\n| class | class-probe | R79ReviewB | first cell is the literal word class |\n"
       "| probe | plain-probe | R79ReviewB | first cell is not class |\n")
pair("08-stranded-probes", BASE)

# --- 09 CONTENT: correct digest of 116 carried by an unrelated criterion (lexical limit) ---
reset(BASE)
append("SKILL.md", "correction: SKILL.md:168 cells=7 digest=e6e751ec67878243\n")
append("corpus/lessons/round-77.md", "erratum: round-77.md:73 digest=7f2d54a7eb33df54\n")
append("corpus/QUALITY.md",
       "\n149. **Unrelated text (content probe, R79ReviewB).** Carries the digest of criterion "
       "116 and nothing else; pointer `corpus/QUALITY.md` resolves. supersedes: 116 "
       "digest=ae134338138ad3e0\n")
pair("09-correct-digest-unrelated-superseder", BASE)

# --- 10 DIRPTR: a new criterion citing a bare directory prefix (resolver laxity) ---
reset(BASE)
append("SKILL.md", "correction: SKILL.md:168 cells=7 digest=e6e751ec67878243\n")
append("corpus/lessons/round-77.md", "erratum: round-77.md:73 digest=7f2d54a7eb33df54\n")
append("corpus/QUALITY.md",
       "\n149. **Directory pointer probe (R79ReviewB).** Pointer `corpus/` is a bare directory "
       "and names no file.\n")
pair("10-dir-pointer-new-criterion", BASE)

reset(BASE)
(R / "summary.txt").write_text("\n".join(SUMMARY) + "\n")
print("\n".join(SUMMARY))
