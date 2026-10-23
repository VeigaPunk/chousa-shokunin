#!/usr/bin/env python3
"""Round 36, C1 counter — the engine-swap canary family.

Frozen predicate (corpus/evidence/round36/claims.md, C1, P1): C1 is met iff
this counter prints ENGINE_SWAP_CANARY=14/14 with predicate_holds=true on each
of two fresh seeds against the landed lane revision, and no committed run of
the same counter against the landed gate prints a lower count.
Code condition: holds = passed == TOTAL (TOTAL = 14) and reference runs sane.
Receipt label: predicate_holds.

Surface: one gate resolves/verifies/pins ONE grep binary, and the receipt can
say WHICH engine answered WHICH record. The fourteen scenarios each separate a
different output-equivalent engine swap that the round-35 counter left alive
(the ten pin-contract demonstrations of `.ufo/waves/round-35/` plus the FOUR
routed gate defects S11-S14). Every scenario names its engine or its gate contract:

  S1  PATH shim first on PATH        a shim that logs and execs real grep never fires
  S2  BASH_ENV grep() function       an imported shell function never receives a call
  S3  grep absent from PATH          the pinned absolute path needs no PATH lookup
  S4  relative override              refused (exit 2, GREP_PROVENANCE)
  S5  missing override               refused
  S6  non-GNU stub override          refused, and the stub is called EXACTLY ONCE
                                     (its --version probe) — never for a match
  S7  DISTINCT-path override         an override whose path differs from the
                                     default is honoured: output equal, echo line
                                     fullmatches path/source/version, and the
                                     recorder actually receives the matcher calls
  S8  default pin                    same echo contract for the default path,
                                     version compared to a LIVE --version of it
  S9  override beats BASH_ENV shim   the function shim receives nothing, the
                                     recorder receives the matches
  S10 semantic canary                per-record attribution: every record's own
                                     span (or its 4096-byte chunk) appears as a
                                     `-a -z -b -o -P` argv on the pinned recorder,
                                     and an output-equivalent python exact-search
                                     engine misses its LONG record (it still
                                     attributes the direct short one; separation
                                     is the long id's absence, not a count of 0)
  S11 manifest hash shim            a PATH sha256sum shim cannot poison the
                                     manifest: both sha fields are 64-hex and
                                     equal the true hashes
  S12 C-locale arm                  a `\\u00e9` claim decodes byte-exactly under
                                     LC_ALL=C (bash's printf %b is locale-bound)
  S13 pin echo isolation            a baseline pinned with CHOUSA_GREP_PIN_ECHO=1
                                     drifts to `none` against the unchanged gate
  S14 pin drift token               an injected GATE_GREP line pairs as
                                     `-GATE_GREP`, not the anonymous `-LINE`

Fixture A (resolution): three short-span claims. Fixture B (canary): one
dead-zone span (seeded length 32765..32767) plus one short span. Fixture C
(locale): a `caf\\u00e9` claim. Fixture D (manifest): a minimal clean record.
The recorder is a distinct-path GNU-reporting wrapper (its --version execs the
real grep) that appends one NUL-delimited argv record per invocation under a
per-run marker; the marker and log name are drawn outside the gate's
environment. Limits stated in claims.md: a gate that READS the recorder script
can forge records (active anti-instrumentation), and the canary says nothing
about whether grep's answer is correct — the output equality does that.

Exit: 0 iff holds; 1 otherwise; 2 harness error.
No network; writes only its temp dir (C1_TMP or TMPDIR) and --receipt.
"""
import argparse
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time

LABEL = "ENGINE_SWAP_CANARY"
TOTAL = 14
GATE_TIMEOUT_S = 600
LINE_RE = re.compile(r"^CLAIM id=(\S+) expected=\S+ observed=(\S+) .*verdict=(\S+)$")
SHIM_VERSION = "grep (pi-uu-grep) 0.2.0"
REAL_GREP = "/usr/bin/grep"
GATE_RE = re.compile(r"^GATE_GREP: path=(\S+) source=(\S+) version=\"(.*)\"$")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def make_fixture_a(root):
    """Three short-span claims: supported, mutated, glued-left."""
    os.makedirs(os.path.join(root, "src"), exist_ok=True)
    words = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india", "juliett"]
    span = " ".join(words)
    src = "lead " + span + " tail\n"
    with open(os.path.join(root, "src", "ok.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(src)
    mut = span[:-1] + ("z" if span[-1] != "z" else "y")
    glued = "leadQ" + span + " tail\n"
    with open(os.path.join(root, "src", "glued.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(glued)
    rows = [
        {"id": "K1", "source": "src/ok.md", "span": span, "expect": "supported"},
        {"id": "K2", "source": "src/ok.md", "span": mut, "expect": "supported"},
        {"id": "K3", "source": "src/glued.md", "span": span, "expect": "supported"},
    ]
    claims = os.path.join(root, "claims.jsonl")
    with open(claims, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(json.dumps(r) for r in rows) + "\n")
    return claims


def make_fixture_b(root, rng):
    """One dead-zone span (seeded length) plus one short span, both supported."""
    os.makedirs(os.path.join(root, "src"), exist_ok=True)
    words = ["".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(rng.randint(3, 8)))
             for _ in range(40)]
    n = rng.choice([32765, 32766, 32767])
    k = n // 7
    long_span = "".join("w%04d " % i for i in range(1, k + 1))
    rem = n - len(long_span)
    if rem:
        long_span += "z" * rem if rem == 1 else "w" * rem
    assert len(long_span) == n, (len(long_span), n)
    short_span = " ".join(words[:6])
    with open(os.path.join(root, "src", "long.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("lead " + long_span + " tail\n")
    with open(os.path.join(root, "src", "short.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("lead " + short_span + " tail\n")
    rows = [
        {"id": "C-LONG-%d" % n, "source": "src/long.md", "span": long_span, "expect": "supported"},
        {"id": "C-SHORT", "source": "src/short.md", "span": short_span, "expect": "supported"},
    ]
    claims = os.path.join(root, "claims.jsonl")
    with open(claims, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(json.dumps(r) for r in rows) + "\n")
    return claims, {"C-LONG-%d" % n: long_span.encode(), "C-SHORT": short_span.encode()}


def make_fixture_c(root):
    os.makedirs(os.path.join(root, "src"), exist_ok=True)
    with open(os.path.join(root, "src", "cafe.md"), "wb") as f:
        f.write(b"lead caf\xc3\xa9 tail\n")
    row = {"id": "L1", "source": "src/cafe.md", "span": "caf\u00e9", "expect": "supported"}
    claims = os.path.join(root, "claims.jsonl")
    with open(claims, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(row) + "\n")
    return claims


RECORD_D = """# research-record v1
<!-- chousa-record: v1 -->
## Meta
| key | value |
|---|---|
| window | loopback |
| fetch | none |
## Question
Does the manifest carry only true hex identity under a hostile PATH?
## Sources
| id | tier | pointer | notes |
|---|---|---|---|
| S1 | primary | lib/primary.md:1 | local fixture |
## Chain
| hop | from | to | status | anchor_kind | anchor | notes |
|---|---|---|---|---|---|---|
| 1 | C1 | S1 | resolved | quote | line1 primary material | direct |
## Claims
| id | kind | text | pointer | status | sweep |
|---|---|---|---|---|---|
| C1 | observation | primary file has line1 | lib/primary.md:1 | verified | |
## Sweeps
| id | claim_id | where | status |
|---|---|---|---|
| SW1 | C1 | lib/ghost*.md | swept |
## Rejections
| id | ref | reason | flip |
|---|---|---|---|
| R1 | noise/chat-export-sources.md | UI chrome is not a primary source | a primary attestation in that file would flip this |
## Approval
| target | state |
|---|---|
| (none) | not-required |
"""

CLAIMS_D = ('{"id":"D1","source":"lib/primary.md","span":"line1 primary material",'
            '"expect":"supported"}\n')


def make_fixture_d(root):
    os.makedirs(os.path.join(root, "lib"), exist_ok=True)
    with open(os.path.join(root, "lib", "primary.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("line1 primary material\n")
    with open(os.path.join(root, "record.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(RECORD_D)
    with open(os.path.join(root, "claims.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        f.write(CLAIMS_D)
    return os.path.join(root, "record.md"), os.path.join(root, "claims.jsonl")


def write_shim(path, tripwire):
    with open(path, "w", encoding="utf-8") as f:
        f.write("#!/bin/sh\nprintf '%s\\n' \"$*\" >>\"%s\" 2>/dev/null\nexec %s \"$@\"\n"
                % ("%s", tripwire, REAL_GREP))
    os.chmod(path, 0o755)


def write_stub_non_gnu(path, tripwire):
    with open(path, "w", encoding="utf-8") as f:
        f.write("#!/bin/sh\nprintf '%s\\n' \"stub $*\" >>\"%s\" 2>/dev/null\n"
                "case \"$1\" in --version|-V) printf '%s\\n' >&2; exit 0;; esac\n"
                "exit 0\n" % ("%s", tripwire, SHIM_VERSION))
    os.chmod(path, 0o755)


def write_bash_env(path, tripwire):
    with open(path, "w", encoding="utf-8") as f:
        f.write("grep() { printf 'fn %s\\n' \"$*\" >>%s 2>/dev/null; command %s \"$@\"; }\n"
                % ("%s", tripwire, REAL_GREP))


def make_recorder(scratch, tag, rng):
    """Distinct-path GNU-reporting recorder: logs NUL-delimited argv per call.

    The marker and the log basename are drawn per invocation and live inside the
    script text, never in the gate's environment."""
    recdir = os.path.join(scratch, "rec-" + tag)
    os.makedirs(recdir, exist_ok=True)
    marker = "CALL-" + "".join(rng.choice("0123456789abcdef") for _ in range(24))
    log = os.path.join(recdir, "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(12)) + ".log")
    path = os.path.join(recdir, "grep-recorder")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("#!/bin/bash\n"
                "{ printf '%s\\n' '%s'; for a in \"$@\"; do printf '%%s\\0' \"$a\"; done; printf '\\n'; } >>'%s'\n"
                "exec %s \"$@\"\n" % (marker, marker, log, REAL_GREP))
    os.chmod(path, 0o755)
    open(log, "w").close()
    return path, log, marker


def read_calls(log, marker):
    try:
        blob = open(log, "rb").read()
    except OSError:
        return []
    calls = []
    tok = marker.encode() + b"\n"
    for part in blob.split(tok):
        if not part.strip(b"\n"):
            continue
        args = part.split(b"\n", 1)[0].split(b"\0")
        if args and args[0] == b"":
            args = args[1:]
        while args and args[-1] == b"":
            args = args[:-1]
        if args:
            calls.append([a.decode("utf-8", "replace") for a in args])
    return calls


HEXTOK = re.compile(r"\\x([0-9A-Fa-f]{2})")


def decode_hex_pattern(p):
    """-> bytes when the whole string is \\xHH escapes, else None."""
    out = bytearray()
    i = 0
    while i < len(p):
        m = HEXTOK.match(p, i)
        if not m:
            return None
        out.append(int(m.group(1), 16))
        i += 4
    return bytes(out)


def decode_matcher_pattern(p):
    """-> ('direct', bytes) | ('chunk', bytes) | None for a matcher argv pattern."""
    m = re.match(r"^(\\x[0-9A-Fa-f]{2})\(\?=(.*)\)$", p, re.S)
    if m:
        head = decode_hex_pattern(m.group(1))
        rest = decode_hex_pattern(m.group(2))
        if head is None or rest is None:
            return None
        return ("chunk", head + rest)
    b = decode_hex_pattern(p)
    if b is not None:
        return ("direct", b)
    return None


def matcher_calls(calls):
    """Matcher-shaped argv: -a -z -b -o -P plus one pattern argument."""
    out = []
    for args in calls:
        flags = set()
        pat = None
        for a in args:
            if a in ("-a", "-z", "-b", "-o", "-P"):
                flags.add(a)
            elif a != "--" and not a.startswith("-"):
                pat = a
        if {"-a", "-z", "-b", "-o", "-P"} <= flags and pat is not None:
            out.append(pat)
    return out


def attributed_records(calls, spans):
    """-> {id: kind} for every record whose own span/chunk appears in a matcher call."""
    got = {}
    pats = [d for d in (decode_matcher_pattern(p) for p in matcher_calls(calls)) if d is not None]
    for rid, span in spans.items():
        for kind, decoded in pats:
            if decoded is None:
                continue
            if kind == "direct" and decoded == span:
                got[rid] = "direct"
                break
            if kind == "chunk" and decoded == span[:4096]:
                got[rid] = "chunk"
                break
    return got


def run_gate(gate, argv, root, extra_env=None, path_override=None):
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("CHOUSA_") and not k.startswith("RESEARCH_GATE_")}
    if path_override is not None:
        env["PATH"] = path_override
    if extra_env:
        env.update(extra_env)
    p = subprocess.run(["bash", gate] + argv, capture_output=True, text=True, env=env,
                       cwd=root, timeout=GATE_TIMEOUT_S)
    return p.returncode, p.stdout, p.stderr


def parse(out):
    drift = any(l.startswith("RESEARCH_GATE: DRIFT") for l in out.splitlines())
    obs = {}
    for l in out.splitlines():
        m = LINE_RE.match(l)
        if m:
            obs[m.group(1)] = (m.group(2), m.group(3))
    return drift, obs


K1_BRANCH = '''  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then
    printf '%s' "$hay" | python3 "@HELPER@" "$span"
    return 0
  fi
'''

K1_HELPER = '''import os, sys
hay = sys.stdin.buffer.read()
span = os.fsencode(sys.argv[1])
off = 0
while True:
    i = hay.find(span, off)
    if i < 0:
        break
    sys.stdout.write("%d\\n" % i)
    off = i + len(span)
'''


def patch_exact_search(gate_text, helper):
    lines = gate_text.splitlines(keepends=True)
    start = None
    for i, l in enumerate(lines):
        if l.startswith("tok_span_offsets()"):
            start = i
            break
    if start is None:
        raise RuntimeError("tok_span_offsets not found")
    for j in range(start + 1, min(start + 40, len(lines))):
        if lines[j].strip().startswith("local hay=$1 span=$2"):
            return "".join(lines[:j + 1] + [K1_BRANCH.replace("@HELPER@", helper)] + lines[j + 1:])
    raise RuntimeError("parameter locals not found")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", default="tools/research-gate.sh")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--receipt", default=None)
    a = ap.parse_args()
    seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(8), "big")
    gate = os.path.abspath(a.gate)
    if not os.path.isfile(gate):
        print("c1-count: gate not found: %s" % gate, file=sys.stderr)
        return 2
    base = os.environ.get("C1_TMP") or os.environ.get("TMPDIR") or tempfile.gettempdir()
    try:
        root = tempfile.mkdtemp(prefix="r36c1-%08x-" % (seed & 0xFFFFFFFF), dir=base)
    except OSError as e:
        print("c1-count: temp dir: %s" % e, file=sys.stderr)
        return 2
    rng = random.Random(seed)
    scratch = os.path.join(root, "_scratch")
    os.makedirs(scratch)
    trip1 = os.path.join(scratch, "trip-path.log")
    trip2 = os.path.join(scratch, "trip-fn.log")
    trip3 = os.path.join(scratch, "trip-stub.log")
    for t in (trip1, trip2, trip3):
        open(t, "w").close()
    shim_dir = os.path.join(scratch, "bin")
    os.makedirs(shim_dir)
    write_shim(os.path.join(shim_dir, "grep"), trip1)
    stub = os.path.join(scratch, "stub-grep")
    write_stub_non_gnu(stub, trip3)
    bash_env = os.path.join(scratch, "bash_env.sh")
    write_bash_env(bash_env, trip2)
    clean_path = "/usr/local/bin:/usr/bin:/bin"
    results, runs = [], []
    receipt = {"label": None, "gate": gate, "seed": seed}
    t0 = time.time()
    try:
        rec_a, rlog_a, rmark_a = make_recorder(scratch, "a", rng)

        def score(name, ok, detail, run=None):
            results.append({"scenario": name, "pass": bool(ok), "detail": detail})
            if run is not None:
                runs.append(run)

        def trip_empty(p):
            try:
                return os.path.getsize(p) == 0
            except OSError:
                return False

        # ---- fixture A reference -------------------------------------------------
        fa = os.path.join(root, "fx-a")
        claims_a = make_fixture_a(fa)
        rc0, out0, err0 = run_gate(gate, ["verify-claims", claims_a, "--root", fa], fa, path_override=clean_path)
        drift0, obs_a = parse(out0)
        ref_a = (rc0 == 1 and drift0 and obs_a.get("K1") == ("supported", "match")
                 and obs_a.get("K2") == ("unsupported", "mismatch")
                 and obs_a.get("K3") == ("unsupported", "mismatch"))
        receipt["reference_a"] = {"rc": rc0, "drift": drift0, "obs": obs_a}
        runs.append({"scenario": "reference-a", "rc": rc0, "stderr_tail": err0[-400:]})

        def same_as_a(rc, out):
            d, o = parse(out)
            return rc == rc0 and d == drift0 and o == obs_a

        if not ref_a:
            raise RuntimeError("reference run A not sane: rc=%s drift=%s obs=%s" % (rc0, drift0, obs_a))

        # S1 PATH shim first
        open(trip1, "w").close()
        rc, out, err = run_gate(gate, ["verify-claims", claims_a, "--root", fa], fa,
                                path_override=shim_dir + ":" + clean_path)
        score("S1-shim-first-path", trip_empty(trip1) and same_as_a(rc, out),
              {"tripwire_bytes": os.path.getsize(trip1), "output_matches_reference": same_as_a(rc, out), "rc": rc},
              {"scenario": "S1", "rc": rc, "stderr_tail": err[-400:]})
        # S2 BASH_ENV function shim
        open(trip2, "w").close()
        rc, out, err = run_gate(gate, ["verify-claims", claims_a, "--root", fa], fa,
                                extra_env={"BASH_ENV": bash_env}, path_override=clean_path)
        score("S2-bash-env-function", trip_empty(trip2) and same_as_a(rc, out),
              {"tripwire_bytes": os.path.getsize(trip2), "output_matches_reference": same_as_a(rc, out), "rc": rc},
              {"scenario": "S2", "rc": rc, "stderr_tail": err[-400:]})
        # S3 grep absent from PATH (symlink farm of the tools the gate uses)
        nogrep = os.path.join(root, "nogrepbin")
        os.makedirs(nogrep, exist_ok=True)
        made = []
        for name in ("bash", "sh", "od", "tr", "sed", "cut", "date", "wc", "sort", "cat", "mkdir",
                     "mktemp", "dirname", "basename", "readlink", "stat", "ls", "find", "python3",
                     "sleep", "mv", "rm", "cp", "touch", "awk", "env", "xargs", "flock", "printf",
                     "expr", "test", "true", "false", "id", "timeout", "sha256sum", "head", "tail"):
            for d in ("/usr/bin", "/bin"):
                p = os.path.join(d, name)
                if os.path.isfile(p) and os.access(p, os.X_OK):
                    link = os.path.join(nogrep, name)
                    if not os.path.lexists(link):
                        os.symlink(p, link)
                    made.append(name)
                    break
        rc, out, err = run_gate(gate, ["verify-claims", claims_a, "--root", fa], fa, path_override=nogrep)
        score("S3-no-grep-on-path", same_as_a(rc, out) and "not found" not in err,
              {"rc": rc, "output_matches_reference": same_as_a(rc, out), "path_tools": len(made),
               "stderr_tail": err[-300:]},
              {"scenario": "S3", "rc": rc, "stderr_tail": err[-400:]})
        # S4 relative override
        rc, out, err = run_gate(gate, ["verify-claims", claims_a, "--root", fa], fa,
                                extra_env={"RESEARCH_GATE_GREP": "bin/grep"}, path_override=clean_path)
        score("S4-override-relative", rc == 2 and "GREP_PROVENANCE" in err,
              {"rc": rc, "marker": "GREP_PROVENANCE" in err, "stderr_tail": err[-300:]},
              {"scenario": "S4", "rc": rc, "stderr_tail": err[-400:]})
        # S5 missing override
        rc, out, err = run_gate(gate, ["verify-claims", claims_a, "--root", fa], fa,
                                extra_env={"RESEARCH_GATE_GREP": os.path.join(scratch, "absent-grep")},
                                path_override=clean_path)
        score("S5-override-missing", rc == 2 and "GREP_PROVENANCE" in err,
              {"rc": rc, "marker": "GREP_PROVENANCE" in err, "stderr_tail": err[-300:]},
              {"scenario": "S5", "rc": rc, "stderr_tail": err[-400:]})
        # S6 non-GNU stub: refused after EXACTLY ONE --version probe, never a match
        open(trip3, "w").close()
        rc, out, err = run_gate(gate, ["verify-claims", claims_a, "--root", fa], fa,
                                extra_env={"RESEARCH_GATE_GREP": stub}, path_override=clean_path)
        stub_lines = [l for l in open(trip3, encoding="utf-8", errors="replace").read().splitlines() if l]
        stub_version_only = len(stub_lines) == 1 and stub_lines[0].split()[1:] == ["--version"]
        score("S6-override-non-gnu", rc == 2 and "GREP_PROVENANCE" in err and stub_version_only,
              {"rc": rc, "marker": "GREP_PROVENANCE" in err, "stub_calls": stub_lines[:3],
               "version_only": stub_version_only, "stderr_tail": err[-300:]},
              {"scenario": "S6", "rc": rc, "stub_calls": stub_lines[:3], "stderr_tail": err[-600:]})
        # S7 distinct-path override: honoured, fullmatch echo, recorder got the calls
        open(rlog_a, "w").close()
        rc, out, err = run_gate(gate, ["verify-claims", claims_a, "--root", fa], fa,
                                extra_env={"RESEARCH_GATE_GREP": rec_a, "CHOUSA_GREP_PIN_ECHO": "1"},
                                path_override=clean_path)
        live_rec = subprocess.run([rec_a, "--version"], capture_output=True, text=True).stdout.splitlines()[0]
        echo = next((l for l in err.splitlines() if l.startswith("GATE_GREP: ")), "")
        want = 'GATE_GREP: path=%s source=override version="%s"' % (rec_a, live_rec)
        calls_a = read_calls(rlog_a, rmark_a)
        rec_matches = matcher_calls(calls_a)
        score("S7-override-distinct-path",
              same_as_a(rc, out) and echo == want and len(rec_matches) >= 1,
              {"rc": rc, "output_matches_reference": same_as_a(rc, out), "echo_fullmatch": echo == want,
               "echo_line": echo, "matcher_calls": len(rec_matches)},
              {"scenario": "S7", "rc": rc, "echo_line": echo, "want": want, "stderr_tail": err[-400:]})
        # S8 default echo
        default_grep = REAL_GREP if os.path.exists(REAL_GREP) else "/bin/grep"
        live_def = subprocess.run([default_grep, "--version"], capture_output=True, text=True).stdout.splitlines()[0]
        rc, out, err = run_gate(gate, ["verify-claims", claims_a, "--root", fa], fa,
                                extra_env={"CHOUSA_GREP_PIN_ECHO": "1"}, path_override=clean_path)
        echo = next((l for l in err.splitlines() if l.startswith("GATE_GREP: ")), "")
        want = 'GATE_GREP: path=%s source=default version="%s"' % (default_grep, live_def)
        score("S8-default-echo", same_as_a(rc, out) and echo == want,
              {"rc": rc, "output_matches_reference": same_as_a(rc, out), "echo_fullmatch": echo == want,
               "echo_line": echo},
              {"scenario": "S8", "rc": rc, "echo_line": echo, "want": want, "stderr_tail": err[-400:]})
        # S9 override beats BASH_ENV shim
        open(trip2, "w").close()
        open(rlog_a, "w").close()
        rc, out, err = run_gate(gate, ["verify-claims", claims_a, "--root", fa], fa,
                                extra_env={"BASH_ENV": bash_env, "RESEARCH_GATE_GREP": rec_a,
                                           "CHOUSA_GREP_PIN_ECHO": "1"},
                                path_override=clean_path)
        echo = next((l for l in err.splitlines() if l.startswith("GATE_GREP: ")), "")
        want9 = 'GATE_GREP: path=%s source=override version="%s"' % (rec_a, live_rec)
        score("S9-override-beats-shim",
              trip_empty(trip2) and same_as_a(rc, out) and echo == want9,
              {"tripwire_bytes": os.path.getsize(trip2), "output_matches_reference": same_as_a(rc, out),
               "echo_fullmatch": echo == want9, "echo_line": echo},
              {"scenario": "S9", "rc": rc, "stderr_tail": err[-400:]})
        # S10 semantic canary: per-record attribution + exact-search separation
        fb = os.path.join(root, "fx-b")
        claims_b, spans_b = make_fixture_b(fb, rng)
        rc_ref_b, out_ref_b, _ = run_gate(gate, ["verify-claims", claims_b, "--root", fb], fb,
                                          path_override=clean_path)
        drift_b, obs_b = parse(out_ref_b)
        ref_b = (rc_ref_b == 0 and not drift_b
                 and all(obs_b.get(rid) == ("supported", "match") for rid in spans_b))
        rec_b, rlog_b, rmark_b = make_recorder(scratch, "b", rng)
        open(rlog_b, "w").close()
        rc, out, err = run_gate(gate, ["verify-claims", claims_b, "--root", fb], fb,
                                extra_env={"RESEARCH_GATE_GREP": rec_b}, path_override=clean_path)
        landed_attr = attributed_records(read_calls(rlog_b, rmark_b), spans_b)
        # separation control: output-equivalent python exact search for long spans
        helper = os.path.join(scratch, "span_search.py")
        with open(helper, "w", encoding="utf-8") as f:
            f.write(K1_HELPER)
        k1_gate = os.path.join(scratch, "k1-exact.sh")
        with open(k1_gate, "w", encoding="utf-8") as f:
            f.write(patch_exact_search(open(gate, encoding="utf-8", errors="surrogateescape").read(), helper))
        os.chmod(k1_gate, 0o755)
        syntax = subprocess.run(["bash", "-n", k1_gate], capture_output=True, text=True)
        rec_k, rlog_k, rmark_k = make_recorder(scratch, "k", rng)
        open(rlog_k, "w").close()
        rc_k, out_k, _ = run_gate(k1_gate, ["verify-claims", claims_b, "--root", fb], fb,
                                  extra_env={"RESEARCH_GATE_GREP": rec_k}, path_override=clean_path)
        k1_attr = attributed_records(read_calls(rlog_k, rmark_k), spans_b)
        k1_same = (rc_k == rc_ref_b) and parse(out_k) == (drift_b, obs_b)
        long_ids = {rid for rid, span in spans_b.items() if len(span) > 32764}
        k1_long_missing = not (long_ids & set(k1_attr))
        score("S10-semantic-canary",
              ref_b and len(landed_attr) == len(spans_b) and k1_long_missing and k1_same
              and syntax.returncode == 0,
              {"ref_b_sane": ref_b, "landed_attributed": sorted(landed_attr.items()),
               "records": len(spans_b), "long_records": sorted(long_ids),
               "k1_attributed": sorted(k1_attr.items()), "k1_long_missing": k1_long_missing,
               "k1_output_equivalent": k1_same, "k1_gate_sha256": sha256_file(k1_gate),
               "rc": rc, "rc_ref": rc_ref_b},
              {"scenario": "S10", "rc": rc, "landed": sorted(landed_attr), "k1": sorted(k1_attr)})
        # S11 manifest hash shim
        fd = os.path.join(root, "fx-d")
        record_d, claims_d = make_fixture_d(fd)
        hostile_bin = os.path.join(scratch, "hashbin")
        os.makedirs(hostile_bin, exist_ok=True)
        with open(os.path.join(hostile_bin, "sha256sum"), "w", encoding="utf-8") as f:
            f.write("#!/bin/sh\nprintf 'HOSTILE-CUT-OUTPUT  -\\n'\nexit 0\n")
        os.chmod(os.path.join(hostile_bin, "sha256sum"), 0o755)
        manifest = os.path.join(fd, "manifest.jsonl")
        if os.path.exists(manifest):
            os.unlink(manifest)
        rc, out, err = run_gate(gate, ["verify-all", record_d, "--claims", claims_d, "--json", manifest,
                                       "--root", fd], fd,
                                path_override=hostile_bin + ":" + clean_path)
        true_rec = sha256_file(record_d)
        true_gate = sha256_file(gate)
        man_ok = False
        try:
            man = json.loads(open(manifest, encoding="utf-8").read().splitlines()[0])
            man_ok = (re.fullmatch(r"[0-9a-f]{64}", man.get("record_sha256", "")) is not None
                      and re.fullmatch(r"[0-9a-f]{64}", man.get("gate_sha256", "")) is not None
                      and man["record_sha256"] == true_rec and man["gate_sha256"] == true_gate)
        except (OSError, ValueError, IndexError):
            man_ok = False
        score("S11-manifest-hash-shim", rc == 0 and man_ok,
              {"rc": rc, "manifest_ok": man_ok, "true_record_sha": true_rec, "true_gate_sha": true_gate,
               "stderr_tail": err[-300:]},
              {"scenario": "S11", "rc": rc, "manifest_ok": man_ok, "stderr_tail": err[-400:]})
        # S12 C-locale arm
        fc = os.path.join(root, "fx-c")
        claims_c = make_fixture_c(fc)
        rc_utf, out_utf, _ = run_gate(gate, ["verify-claims", claims_c, "--root", fc], fc,
                                      extra_env={"LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"},
                                      path_override=clean_path)
        rc_c, out_c, err_c = run_gate(gate, ["verify-claims", claims_c, "--root", fc], fc,
                                      extra_env={"LC_ALL": "C", "LANG": "C"}, path_override=clean_path)
        ref_c = (rc_utf == 0 and parse(out_utf) == (False, {"L1": ("supported", "match")}))
        score("S12-locale-c", ref_c and rc_c == rc_utf and parse(out_c) == parse(out_utf),
              {"utf8_rc": rc_utf, "c_rc": rc_c, "utf8_obs": parse(out_utf)[1], "c_obs": parse(out_c)[1],
               "stderr_tail": err_c[-200:]},
              {"scenario": "S12", "utf8_rc": rc_utf, "c_rc": rc_c})
        # S13 pin echo isolation
        pin1 = os.path.join(fd, "pin-echo.txt")
        if os.path.exists(pin1):
            os.unlink(pin1)
        rc_pin, out_pin, err_pin = run_gate(gate, ["--pin", pin1], fd,
                                            extra_env={"CHOUSA_GREP_PIN_ECHO": "1"}, path_override=clean_path)
        env_now = {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}
        dr = subprocess.run(["bash", gate, "--drift", pin1], capture_output=True, text=True, env=env_now, cwd=fd)
        baseline_has_echo = os.path.exists(pin1) and any(
            l.startswith("GATE_GREP: ") for l in open(pin1, encoding="utf-8").read().splitlines())
        score("S13-pin-echo-isolation",
              rc_pin == 0 and dr.returncode == 0 and dr.stdout.strip() == "GATE_DRIFT: none"
              and not baseline_has_echo,
              {"pin_rc": rc_pin, "drift_rc": dr.returncode, "drift_out": dr.stdout.strip()[:200],
               "baseline_echo": baseline_has_echo, "stderr_tail": err_pin[-300:]},
              {"scenario": "S13", "pin_rc": rc_pin, "drift_rc": dr.returncode})
        # S14 pin drift token
        pin2 = os.path.join(fd, "pin-token.txt")
        if os.path.exists(pin2):
            os.unlink(pin2)
        rc_pin2, out_pin2, _ = run_gate(gate, ["--pin", pin2], fd, path_override=clean_path)
        text = open(pin2, encoding="utf-8").read().splitlines()
        idx = text.index("# --- canonical output follows ---")
        text.insert(idx + 1, 'GATE_GREP: path=/usr/bin/grep source=default version="x"')
        with open(pin2, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(text) + "\n")
        dr2 = subprocess.run(["bash", gate, "--drift", pin2], capture_output=True, text=True, env=env_now, cwd=fd)
        score("S14-pin-drift-token",
              rc_pin2 == 0 and dr2.returncode == 1 and "-GATE_GREP" in dr2.stdout
              and "-LINE" not in dr2.stdout,
              {"pin_rc": rc_pin2, "drift_rc": dr2.returncode, "drift_out": dr2.stdout.strip()[:200]},
              {"scenario": "S14", "pin_rc": rc_pin2, "drift_rc": dr2.returncode})

        passed = sum(1 for r in results if r["pass"])
        holds = passed == TOTAL and ref_a and ref_b
        receipt.update({"label": "%s=%d/%d" % (LABEL, passed, TOTAL), "matched": passed, "total": TOTAL,
                        "predicate_holds": holds, "gate_sha256": sha256_file(gate),
                        "elapsed_s": round(time.time() - t0, 2), "scenarios": results, "runs": runs})
        print("%s=%d/%d" % (LABEL, passed, TOTAL))
        for r in results:
            print("  %-28s %s  %s" % (r["scenario"], "PASS" if r["pass"] else "FAIL",
                                      json.dumps(r["detail"], sort_keys=True)[:260]))
    except (subprocess.TimeoutExpired, RuntimeError) as e:
        receipt = {"label": "%s=error" % LABEL, "predicate_holds": False, "gate": gate, "seed": seed,
                   "error": str(e)}
        print("%s=error %s" % (LABEL, e), file=sys.stderr)
    finally:
        if a.receipt:
            with open(a.receipt, "w", encoding="utf-8") as f:
                json.dump(receipt, f, indent=1, sort_keys=True)
        shutil.rmtree(root, ignore_errors=True)
    return 0 if receipt.get("predicate_holds") else 1


if __name__ == "__main__":
    sys.exit(main())
