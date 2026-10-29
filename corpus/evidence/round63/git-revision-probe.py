#!/usr/bin/env python3
"""git revision-identity probe (round 63): what this host's git does for the revision names a citation can use —
a full object name, an abbreviation, an annotated or lightweight tag, a branch, a `<rev>:<path>` blob — next to what
the installed pages git-rev-parse(1) (S142) and gitrevisions(7) (S143) say.

Usage: python3 corpus/evidence/round63/git-revision-probe.py --work DIR   (DIR absent or empty, its parent present and
not a symlink itself; removed afterwards)
Prints `HEADER git=<git --version>` and `HEADER python=<version>`, `PROBE <id> <name> observed=<x> expected=<y>
ok|DIFFERENT` lines, then `PROBE_FACTS=<k>/<n>`. Every fixture repository is created under DIR with an explicit
`git -C <dir>`, an identity and dates fixed by environment, no global or system git configuration, and commit
content fixed, so the output is identical on every run of the same git. `expected` is typed in this script by its
author: `PROBE_FACTS` counts agreement between the host and those typed expectations, a self-consistency check and
not an independent measurement. Basis of each expectation: see the `# cite` comment on its `probe(...)` call —
a quote from S142 or S143 (rendered `MANWIDTH=1000 man -l FILE | col -bx`), or INFERENCE where no sentence of either page
predicts it (P02, P05, P06, P13).
Exit codes: 0 all facts as expected · 1 a fact differs or cleanup failed · 2 usage/environment (no git, --work refused).
"""
import argparse
import os
import pathlib
import platform
import shutil
import subprocess
import sys

BASE_ENV = {
    "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "probe", "GIT_AUTHOR_EMAIL": "probe@invalid", "GIT_AUTHOR_DATE": "2026-01-01T00:00:00+0000",
    "GIT_COMMITTER_NAME": "probe", "GIT_COMMITTER_EMAIL": "probe@invalid", "GIT_COMMITTER_DATE": "2026-01-01T00:00:00+0000",
    "LC_ALL": "C", "GIT_TERMINAL_PROMPT": "0",
}


def git(d, *args, stdin=None, check=True):
    env = dict(os.environ)
    for k in list(env):
        if k.startswith("GIT_"):
            del env[k]
    env.update(BASE_ENV)
    p = subprocess.run(["git", "-C", str(d), *args], capture_output=True, text=True, env=env, input=stdin, timeout=120)
    if check and p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr.strip()[:120]}")
    return p


def commit(d, name, text):
    (pathlib.Path(d) / name).write_text(text, encoding="utf-8")
    git(d, "add", "--", name)
    git(d, "commit", "-q", "-m", f"add {name}")
    return git(d, "rev-parse", "HEAD").stdout.strip()


def init(path, fmt):
    pathlib.Path(path).mkdir(parents=True)
    git(path, "init", "-q", f"--object-format={fmt}", "-b", "main")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    if shutil.which("git") is None:
        print("git-revision-probe: git not found", file=sys.stderr)
        return 2
    raw = pathlib.Path(a.work)
    if raw.is_symlink() or not raw.parent.is_dir() or (raw.exists() and any(raw.iterdir())):
        print("git-revision-probe: --work must be absent or empty, with its parent present and not a symlink", file=sys.stderr)
        return 2
    raw.mkdir(exist_ok=True)
    out = []
    facts = []

    def probe(pid, label, observed, expected):
        ok = observed == expected
        facts.append(ok)
        out.append(f"PROBE {pid} {label} observed={observed} expected={expected} {'ok' if ok else 'DIFFERENT'}")

    try:
        gv = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=30).stdout.strip()
        out.append(f"HEADER git={gv}")
        out.append(f"HEADER python={platform.python_version()}")
        r1 = raw / "sha1"
        init(r1, "sha1")
        c1 = commit(r1, "a.txt", "alpha\n")
        # cite P01: S143 "The full SHA-1 object name (40-byte hexadecimal string), or a leading substring that is unique within the repository."
        probe("P01", "sha1-full-name-length", len(c1), 40)
        r2 = raw / "sha256"
        init(r2, "sha256")
        c2 = commit(r2, "a.txt", "alpha\n")
        # cite P02: INFERENCE the pages describe SHA-1 names; the 64-digit length of a sha256 repository is observed, not stated
        probe("P02", "sha256-full-name-length", len(c2), 64)
        git(r1, "tag", "-a", "v1", "-m", "annotated")
        git(r1, "tag", "lw")
        tag_id = git(r1, "rev-parse", "--verify", "--end-of-options", "v1").stdout.strip()
        peeled = git(r1, "rev-parse", "--verify", "--end-of-options", "v1^{commit}").stdout.strip()
        # cite P03: S143 "<rev>^{commit} describes the corresponding commit object."
        probe("P03", "annotated-tag-id-differs-from-commit-id", tag_id != c1, True)
        # cite P04: S142 "git rev-parse "$VAR^{commit}" will make sure $VAR names an existing object that is a commit-ish (i.e. a commit, or an annotated tag that points at a commit)."
        probe("P04", "peeled-annotated-tag-equals-commit-id", peeled == c1, True)
        lw = git(r1, "rev-parse", "--verify", "--end-of-options", "lw").stdout.strip()
        # cite P05: INFERENCE a lightweight tag is a ref directly at the commit; the pages do not say its id equals the commit id
        probe("P05", "lightweight-tag-id-equals-commit-id", lw == c1, True)
        c1b = commit(r1, "b.txt", "beta\n")
        main_now = git(r1, "rev-parse", "--verify", "--end-of-options", "main").stdout.strip()
        # cite P06: INFERENCE a branch name resolves to the commit its ref holds now; the page says `master typically means the commit object referenced by refs/heads/master`
        probe("P06", "branch-name-moves-after-new-commit", main_now != c1 and main_now == c1b, True)
        blob1 = git(r1, "rev-parse", "--verify", "--end-of-options", f"{c1}:a.txt").stdout.strip()
        blob2 = git(r1, "rev-parse", "--verify", "--end-of-options", f"{c1b}:a.txt").stdout.strip()
        # cite P07: S143 "A suffix : followed by a path names the blob or tree at the given path in the tree-ish object named by the part before the colon."
        probe("P07", "unchanged-file-blob-id-same-across-commits", blob1 == blob2, True)
        short = c1b[:4]
        p8 = git(r1, "rev-parse", "--verify", "--quiet", "--end-of-options", f"{short}^{{object}}", check=False)
        # cite P08: S143 "dae86e both name the same commit object if there is no other object in your repository whose object name starts with dae86e."
        probe("P08", "unique-4-digit-prefix-resolves", p8.returncode, 0)
        seen = {}
        n = 0
        collide = None
        while collide is None:
            text = f"filler {n}\n"
            h = git(r1, "hash-object", "--stdin", stdin=text).stdout.strip()
            n += 1
            if h[:4] in seen and seen[h[:4]][0] != h:
                collide = (h[:4], seen[h[:4]][0], h, text)
                break
            git(r1, "hash-object", "-w", "--stdin", stdin=text)
            seen[h[:4]] = (h, text)
            if n > 6000:
                raise RuntimeError("no 4-digit collision found")
        pref, first, second, second_text = collide
        resolves = git(r1, "rev-parse", "--verify", "--quiet", "--end-of-options", f"{pref}^{{object}}", check=False).returncode == 0
        git(r1, "hash-object", "-w", "--stdin", stdin=second_text)
        amb = git(r1, "rev-parse", "--verify", "--end-of-options", f"{pref}^{{object}}", check=False)
        # cite P09: S143 "or a leading substring that is unique within the repository."
        probe("P09", "prefix-resolves-then-ambiguous-after-second-object", (resolves, amb.returncode != 0), (True, True))
        # cite P10: INFERENCE the pages do not give git's error wording; the word `ambiguous` in its message is observed
        probe("P10", "ambiguous-prefix-error-mentions-ambiguous", "ambiguous" in amb.stderr, True)
        dis = git(r1, "rev-parse", f"--disambiguate={pref}").stdout.split()
        # cite P11: S142 "Show every object whose name begins with the given prefix."
        probe("P11", "disambiguate-lists-both-objects", sorted(dis) == sorted({first, second}), True)
        s2 = git(r1, "rev-parse", "--short=2", "--end-of-options", "HEAD").stdout.strip()
        # cite P12: S142 "The minimum length is 4, the default is the effective value of the core.abbrev configuration variable"
        probe("P12", "short-length-minimum-is-four", len(s2), 4)
        s0 = git(r1, "rev-parse", "--short", "--end-of-options", "HEAD").stdout.strip()
        # cite P13: INFERENCE the page names core.abbrev as the default but not its value; seven is observed for a small repository
        probe("P13", "default-short-length-small-repository", len(s0), 7)
        missing = git(r1, "rev-parse", "--verify", "--quiet", "--end-of-options", "0" * 40 + "^{object}", check=False)
        # cite P14: S142 "git rev-parse "$VAR^{object}" can be used."
        probe("P14", "unknown-full-name-fails-verify", missing.returncode != 0, True)
    except Exception as e:
        print(f"git-revision-probe: {type(e).__name__}: {e}", file=sys.stderr)
        shutil.rmtree(raw, ignore_errors=True)
        return 2
    shutil.rmtree(raw, ignore_errors=True)
    if raw.exists():
        print("git-revision-probe: cleanup failed", file=sys.stderr)
        return 1
    for l in out:
        print(l)
    print(f"PROBE_FACTS={sum(facts)}/{len(facts)}")
    return 0 if all(facts) and len(facts) == 14 else 1


if __name__ == "__main__":
    sys.exit(main())
