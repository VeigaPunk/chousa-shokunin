#!/usr/bin/env python3
"""Round 34 attempt 2, C3 self-audit: count mismatches between the lane's
self-assessment text and observed repo state (calibration axis).

Frozen predicate (claims-a2.md, C3, P3): C3 is met iff, on the landed lane
revision, this tool with the committed audit set prints
SELF_AUDIT_UNDISPOSITIONED=0, and the printed SELF_AUDIT_MISMATCHES=K is
reproduced verbatim by a re-run (every counted mismatch carries a committed
disposition line in audit-dispositions.md: `<id> | fixed <commit>` / `routed
<where>` / `accepted <reason>`).

The tool COUNTS, it does not gate: exit is 0 whenever the set was readable,
whatever K is. Check kinds (enumerated in audit-set.json):
- git_commit   {"prefix": ...}            prefix resolves to a commit in lane history
- path         {"path": ...}              path exists at the lane root
- sha256       {"path": ..., "expect": ...}  file digest equals the pinned digest
- receipt_binding {"receipt": ..., "commit": ...}  the committed JSON receipt's
              gate_sha256 equals the digest of tools/research-gate.sh at <commit>
- receipt_gate_file {"receipt": ..., "gate_file": ...}  a control receipt binds a
              non-lane gate committed as a file (mask/control gates)
- grep_assert  {"path": ..., "pattern": ..., "present": true|false}  a named text
              assertion holds (regex search, per line)

Usage: python3 corpus/evidence/round34/self-audit.py [--set PATH]
          [--lane PATH] [--dispositions PATH]
All audited file reads resolve COMMITTED bytes at HEAD via `git show HEAD:<path>` (a dirty
worktree cannot move the count); untracked paths fail closed. No network; writes nothing.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_show_blob_sha(lane, commit, path):
    p = subprocess.run(["git", "-C", lane, "show", "%s:%s" % (commit, path)],
                       capture_output=True)
    if p.returncode != 0:
        return None
    return hashlib.sha256(p.stdout).hexdigest()


def git_commit_exists(lane, prefix):
    p = subprocess.run(["git", "-C", lane, "rev-parse", "--verify", "--quiet",
                        prefix + "^{commit}"], capture_output=True, text=True)
    return p.returncode == 0, p.stdout.strip() if p.returncode == 0 else ""


def head_bytes(lane, path):
    """Committed bytes of path at HEAD (None if not tracked there)."""
    p = subprocess.run(["git", "-C", lane, "show", "HEAD:%s" % path],
                       capture_output=True)
    return p.stdout if p.returncode == 0 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", default="corpus/evidence/round34/audit-set.json")
    ap.add_argument("--lane", default=".")
    ap.add_argument("--dispositions", default="corpus/evidence/round34/audit-dispositions.md")
    a = ap.parse_args()
    lane = os.path.abspath(a.lane)
    with open(os.path.join(lane, a.set)) as f:
        checks = json.load(f)["checks"]
    dispositions = {}
    dpath = os.path.join(lane, a.dispositions)
    if os.path.isfile(dpath):
        with open(dpath) as f:
            for line in f:
                line = line.rstrip("\n")
                if "|" in line and not line.startswith("#"):
                    cid = line.split("|", 1)[0].strip()
                    dispositions[cid] = line.split("|", 1)[1].strip()
    import hashlib as _hl
    with open(os.path.join(lane, a.set), "rb") as _sf:
        print("SET_SHA256=%s" % _hl.sha256(_sf.read()).hexdigest())
    mismatches = []
    for chk in checks:
        cid, kind = chk["id"], chk["kind"]
        detail = "ok"
        ok = True
        try:
            if kind == "git_commit":
                ok, full = git_commit_exists(lane, chk["prefix"])
                detail = "resolves %s" % full[:12] if ok else "prefix %s does not resolve" % chk["prefix"]
            elif kind == "path":
                raw = head_bytes(lane, chk["path"])
                ok = raw is not None
                detail = "tracked at HEAD" if ok else "missing or untracked at HEAD: %s" % chk["path"]
            elif kind == "sha256":
                raw = head_bytes(lane, chk["path"])
                if raw is None:
                    ok, detail = False, "not tracked at HEAD: %s" % chk["path"]
                else:
                    got = hashlib.sha256(raw).hexdigest()
                    ok = got == chk["expect"]
                    detail = "digest %s" % got[:16] if ok else "digest %s != pinned %s" % (got[:16], chk["expect"][:16])
            elif kind == "receipt_binding":
                raw = head_bytes(lane, chk["receipt"])
                if raw is None:
                    ok, detail = False, "not tracked at HEAD: %s" % chk["receipt"]
                else:
                    r = json.loads(raw.decode("utf-8", "replace"))
                    got = r.get("gate_sha256", "")
                    want = git_show_blob_sha(lane, chk["commit"], "tools/research-gate.sh")
                    if want is None:
                        ok, detail = False, "commit %s has no gate blob" % chk["commit"]
                    else:
                        ok = got == want
                        detail = ("binds %s@%s" % (got[:12], chk["commit"][:8]) if ok
                                  else "receipt gate %s != %s@%s" % (got[:12], want[:12], chk["commit"][:8]))
            elif kind == "receipt_gate_file":
                # a CONTROL receipt legitimately binds a non-lane gate committed as a file.
                raw = head_bytes(lane, chk["receipt"])
                graw = head_bytes(lane, chk["gate_file"])
                if raw is None:
                    ok, detail = False, "not tracked at HEAD: %s" % chk["receipt"]
                elif graw is None:
                    ok, detail = False, "not tracked at HEAD: %s" % chk["gate_file"]
                else:
                    r = json.loads(raw.decode("utf-8", "replace"))
                    got = r.get("gate_sha256", "")
                    want = hashlib.sha256(graw).hexdigest()
                    ok = got == want
                    detail = ("binds %s" % chk["gate_file"] if ok
                              else "receipt gate %s != %s (%s)" % (got[:12], want[:12], chk["gate_file"]))
            elif kind == "grep_assert":
                raw = head_bytes(lane, chk["path"])
                if raw is None:
                    ok, detail = False, "not tracked at HEAD: %s" % chk["path"]
                else:
                    found = any(re.search(chk["pattern"], line)
                                for line in raw.decode("utf-8", "replace").splitlines())
                    ok = found == chk.get("present", True)
                    detail = "pattern %s %s" % (chk["pattern"], "present" if found else "absent")
            else:
                ok, detail = False, "unknown check kind: %s" % kind
        except Exception as e:  # a check that errors is a mismatch, not a crash
            ok, detail = False, "check error: %r" % (e,)
        if ok:
            print("AUDIT id=%s ok %s" % (cid, detail))
        else:
            print("AUDIT id=%s MISMATCH %s: %s" % (cid, kind, detail))
            mismatches.append(cid)
    undispositioned = [m for m in mismatches if m not in dispositions]
    print("SELF_AUDIT_MISMATCHES=%d" % len(mismatches))
    for m in mismatches:
        print("  mismatch: %s (%s)" % (m, "dispositioned: " + dispositions[m] if m in dispositions else "NO DISPOSITION"))
    print("SELF_AUDIT_UNDISPOSITIONED=%d" % len(undispositioned))
    return 0


if __name__ == "__main__":
    sys.exit(main())
