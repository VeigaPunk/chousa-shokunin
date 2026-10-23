#!/usr/bin/env python3
"""Differential probe: research-gate.sh token-boundary matching vs the frozen
round-29 quote-reopen match rule (c1-count.py reference functions).

Gate side: verify-claims over a scratch Markdown source, expect=supported;
observed=supported means the gate's matcher accepted the span.
New-command side: c1-count.found(c1-count.norm(file_text), span).
Read-only with respect to the lane; all writes stay in this scratch dir.
"""
import importlib.util
import json
import os
import re
import subprocess
import sys

SCRATCH = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
GATE = os.path.join(LANE, "tools", "research-gate.sh")
COUNTER = os.path.join(LANE, "corpus", "evidence", "round29", "c1-count.py")

# (probe id, raw source content, span)
PROBES = [
    ("emdash-left-neighbor",  "alpha\u2014omega sentinel",               "omega"),
    ("curly-left-neighbor",   "he said \u201chello there\u201d loudly",  "hello there"),
    ("hyphen-cut-before",     "cross-check the plan",                    "cross"),
    ("apos-cut-head",         "jin'i-ryu style guide",                   "i-ryu"),
    ("underscore-neighbor",   "foo_bar baz qux",                         "foo"),
    ("ws-run-collapse",       "gamma   delta epsilon",                   "gamma delta"),
    ("newline-in-gap",        "line one\nline two done",                 "one line two"),
    ("midword-cut",           "transmission complete now",               "transmiss"),
    ("case-sensitive",        "Alpha Beta gamma",                        "alpha beta"),
    ("nfkc-ligature",         "\ufb01ne print here",                     "fine print"),
    ("cjk-neighbor",          "\u8010\u4e45token\u7aef\u70b9",           "token"),
    ("digit-glued",           "route66 map drawn",                       "66 map"),
    ("punct-both-sides",      "(closed paren) end",                      "closed paren"),
    ("soft-hyphen-in-word",   "auto\u00admatic control unit",            "automatic control"),
]

# probe.md: one physical line per probe except the embedded-newline probe.
phys = []
for _pid, raw, _span in PROBES:
    phys.extend(raw.split("\n"))
source_text = "\n".join(phys) + "\n"
with open(os.path.join(SCRATCH, "probe.md"), "w", encoding="utf-8") as f:
    f.write(source_text)

claims = [{"id": pid, "source": "probe.md", "span": span, "expect": "supported"}
          for pid, _raw, span in PROBES]
with open(os.path.join(SCRATCH, "probe.jsonl"), "w", encoding="utf-8") as f:
    for c in claims:
        f.write(json.dumps(c, ensure_ascii=True) + "\n")

# --- gate side -------------------------------------------------------------
env = dict(os.environ)
for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
    env.pop(k, None)
run = subprocess.run(["bash", GATE, "verify-claims", "probe.jsonl", "--root", SCRATCH],
                     cwd=SCRATCH, env=env, capture_output=True, text=True, timeout=120)
with open(os.path.join(SCRATCH, "gate-stdout.txt"), "w", encoding="utf-8") as f:
    f.write(run.stdout)
with open(os.path.join(SCRATCH, "gate-stderr.txt"), "w", encoding="utf-8") as f:
    f.write(run.stderr)
gate_obs = {}
for m in re.finditer(r"^CLAIM id=(\S+) expected=\S+ observed=(\S+)", run.stdout, re.M):
    gate_obs[m.group(1)] = m.group(2)

# --- new-command side (frozen reference functions, imported read-only) -----
spec = importlib.util.spec_from_file_location("cc", COUNTER)
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)
page = cc.norm(source_text)

print(f"gate exit={run.exit_code if hasattr(run, 'exit_code') else run.returncode} "
      f"summary={[l for l in run.stdout.splitlines() if l.startswith(('VERDICT_BEARING', 'RESEARCH_GATE'))]}")
print(f"{'probe':<22} {'gate observed':<14} {'new verdict':<11} same?")
for pid, _raw, span in PROBES:
    g = gate_obs.get(pid, "??")
    n = "VERBATIM" if cc.found(page, span) else "ABSENT"
    same = "same" if (g == "supported") == (n == "VERBATIM") else "DIFFER"
    print(f"{pid:<22} {g:<14} {n:<11} {same}")
