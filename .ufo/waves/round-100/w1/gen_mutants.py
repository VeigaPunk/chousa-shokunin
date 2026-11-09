#!/usr/bin/env python3
"""Generate one-site tool mutants of tools/gate-records.py at F. Assert each site occurs exactly once."""
import pathlib, hashlib, sys

S = pathlib.Path("/fast/scratch/hyaku/chousa-r100/R100MutantsC1")
SRC = (S / "repo" / "tools" / "gate-records.py").read_text(encoding="utf-8")
MUTDIR = S / "muts" / "tool"
MUTDIR.mkdir(parents=True, exist_ok=True)

MARKERS = [
    ("m-drop-cookies", "    \"cookies must be enabled\",\n"),
    ("m-drop-checking", "    \"checking your browser\",\n"),
    ("m-drop-recaptcha", "    \"recaptcha\",\n"),
    ("m-drop-clientch", "    \"client challenge\",\n"),
    ("m-drop-couldnt", "    \"a required part of this site couldn't load\",\n"),
    ("m-drop-justamoment", "    \"just a moment\",\n"),
    ("m-drop-verifyhuman", "    \"verify you are human\",\n"),
    ("m-drop-enablejs", "    \"enable javascript and cookies to continue\",\n"),
    ("m-drop-attention", "    \"attention required\",\n"),
    ("m-drop-ddos", "    \"ddos protection\",\n"),
    ("m-drop-robot", "    \"are you a robot\",\n"),
]

NEW = [
    ("n-lstree-corpus", '"--", "corpus/captures/"', '"--", "corpus/"'),
    ("n-txtwins-inv", 'path.endswith(".txt")', 'not path.endswith(".txt")'),
    ("n-blobtest-drop", 'if len(parts) == 3 and parts[1] == "blob" and CAPANY_RE.fullmatch(path):',
     'if len(parts) == 3 and CAPANY_RE.fullmatch(path):'),
    ("n-z-drop", '"ls-tree", "-z", rev,', '"ls-tree", rev,'),
    ("n-sib-raw", 'sib = git_blob(repo, rev, name[:-4] + ".txt")', 'sib = git_blob(repo, rev, name[:-4] + ".raw")'),
    ("n-verify-drop", '"rev-parse", "--verify", "--quiet"', '"rev-parse", "--quiet"'),
    ("n-cache-repoonly", '    k = (repo, rev)\n', '    k = (repo,)\n'),
    ("n-rvcapture-call-none", 'ctext = rev_capture_text(repo, kv["rev"], kv["path"], blob)', 'ctext = None'),
    ("n-sib-none-inv", '        if sib is not None:', '        if sib is None:'),
    ("n-capany-to-cap", 'parts[1] == "blob" and CAPANY_RE.fullmatch(path)', 'parts[1] == "blob" and CAP_RE.fullmatch(path)'),
    ("n-txtwins-first", 'if parts[2] not in m or path.endswith(".txt"):', 'if parts[2] not in m:'),
    ("n-strip-drop", 'capture_oids(repo, rev).get(p.stdout.strip())', 'capture_oids(repo, rev).get(p.stdout)'),
    ("n-rc-ignored", 'if p.returncode == 0 else None', 'if True else None'),
    ("n-none-check-drop", '    if name is None:\n        return None\n', '    if False:\n        return None\n'),
    ("n-ischallenge-drop", '            if ctext is not None and is_challenge(ctext):', '            if ctext is not None:'),
    ("n-sib-noassign", '            blob = sib', '            blob = blob'),
    ("n-empty-blob", '    return blob.decode("utf-8", errors="replace")\n\n\ndef _valid_ts',
     '    return ""\n\n\ndef _valid_ts'),
    ("n-blobtype-inv", 'if t.returncode != 0 or t.stdout.strip() != "blob":', 'if t.returncode != 0 or t.stdout.strip() != "commit":'),
    ("n-ddash-drop", '"ls-tree", "-z", rev, "--", "corpus/captures/"', '"ls-tree", "-z", rev, "corpus/captures/"'),
    ("n-urladmit-drop", '            if ctext is not None and is_challenge(ctext):\n                codes.append("CHALLENGE")',
     '            if ctext is not None and False:\n                codes.append("CHALLENGE")'),
    ("n-blobdecode-plain", '    return blob.decode("utf-8", errors="replace")',
     '    return blob.decode("utf-8")'),
]

R99 = [
    ("r-lt", 'return len(t.split()) <= CHALLENGE_MAX_WORDS', 'return len(t.split()) < CHALLENGE_MAX_WORDS'),
    ("r-max199", 'CHALLENGE_MAX_WORDS = 200', 'CHALLENGE_MAX_WORDS = 199'),
    ("r-max201", 'CHALLENGE_MAX_WORDS = 200', 'CHALLENGE_MAX_WORDS = 201'),
    ("r-nonorm", '    t = norm(text).lower()', '    t = text.lower()'),
    ("r-nolower", '    t = norm(text).lower()', '    t = norm(text)'),
    ("r-all", 'return len(t.split()) <= CHALLENGE_MAX_WORDS and any(m in t for m in CHALLENGE_MARKERS)',
     'return len(t.split()) <= CHALLENGE_MAX_WORDS and all(m in t for m in CHALLENGE_MARKERS)'),
]

mutants = []
for name, old in MARKERS:
    mutants.append((name, old, ""))  # drop line
mutants += NEW
mutants += R99

manifest = []
ok = True
for name, old, new in mutants:
    count = SRC.count(old)
    if count != 1:
        print(f"!! {name}: site count {count} != 1")
        ok = False
        continue
    m = SRC.replace(old, new)
    p = MUTDIR / f"{name}.py"
    p.write_text(m, encoding="utf-8")
    h = hashlib.sha256(m.encode()).hexdigest()[:12]
    manifest.append((name, h))
    print(f"OK {name} {h}")
print(f"manifest {len(manifest)}/{len(mutants)}")
manifest_path = S / "muts" / "tool-manifest.txt"
manifest_path.write_text("\n".join(f"{n} {h}" for n, h in manifest) + "\n")
print("ALL EXACT-ONCE" if ok and len(manifest) == len(mutants) else "SOME FAILED")
