# RevScenarioS6S7S8S9 — audit of c1-count.py scenarios S6–S9 (round-35 C1)

Date: 2026-10-23. Gate scored: `tools/research-gate.sh`
sha256 `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` (verified,
matches the wave pin). Counter: `corpus/evidence/round35/c1-count.py`, read-only.
Scratch: `/tmp/hyaku/chousa-r35/w2/RevScenarioS6S7S8S9` (`$D` below); evidence copies
in `evidence/` beside this report.

## Re-derived baseline

`C1_TMP=$D python3 corpus/evidence/round35/c1-count.py --seed 424242 --receipt $D/c1-landed-s424242.json`
→ `GREP_PIN_MATCH=9/9`, all nine PASS, receipt `gate_sha256=1f2fb4f5…` (fresh seed, exit 0).
Hardcoded control receipt `controls/c1-hardcoded-s3501.json` (committed): `3/9`,
S7/S8/S9 all False — current assertions discriminate the landed gate from the
committed cheapest control.

## S6 — non-GNU override refused (scenario docstring: "wrapper is never used for a match")

Counter stub `write_stub_non_gnu` (c1-count.py:115-120) prints `grep (pi-uu-grep) 0.2.0`
to **stderr** on `--version`/`-V`, exit 0, and exits 0 silently for anything else.

Gate mechanism (`grep_pin_verify`, research-gate.sh:358-367):
`v=$("$cand" --version 2>/dev/null | head -n 1 || true)` — **stdout only**, stderr
discarded, **candidate exit code ignored**; accept iff first stdout line matches
`*"GNU grep"*`. `grep_pin_init` runs at line 8039, before any mode reads a record,
so a refusal is structurally pre-match.

Ran the counter-equivalent stub as the override:

    env -i PATH=… RESEARCH_GATE_GREP=$D/stubs/stub-non-gnu.sh bash tools/research-gate.sh verify-claims claims.jsonl --root $D/fix
    rc=2; stderr: research-gate: GREP_PROVENANCE refused: override does not report GNU grep: <no version> (candidate=…/stub-non-gnu.sh)
    trip-stub.log: exactly ONE line: `stub --version`

Confirmed: the stub is invoked once, argv `--version` only; never used for a match.
(The real counter's run recorded `stub_calls: 1` in the receipt above.)

### Finding S6-a (counter gap, demonstrated): `stub_calls` is recorded, never asserted

Scored predicate (c1-count.py:244): `rc == 2 and "GREP_PROVENANCE" in err`. The
docstring intent "never used for a match" is data, not code. Mutant
`evidence/gate-late-refuse.sh` (sha256 `12fc5a87…`) inserts one match-shaped call
`grep -a -z -b -o -P -- x /dev/null` between failed verify and `grep_pin_refuse`:

    rc=2, GREP_PROVENANCE present → S6 predicate TRUE
    trip log: `stub --version` + `stub -a -z -b -o -P -- x /dev/null` (stub_calls=2)

A gate that refuses *late* — after spending the refused pin on a match — still wins
the point. Tighter assertion: `stub_calls == ["--version"]`-equivalent, i.e.
`stub_calls.splitlines() == ["stub --version"]` (or `len(...) == 1 and line
endswith("--version")`). Severity: low-moderate — a real gate that matches before
refusing is exotic, but the claimed invariant is exactly what the scenario sells.

### Finding S6-b (gate observation): `--version` exit code ignored

Stub `stub-gnu-rc7.sh` (GNU text on **stdout**, `--version` exits 7, all other calls
exit 7): gate **admitted the pin** (exit-code blind), then died rc=2 at
`token_matcher_require` (research-gate.sh:1762-1765) with "GNU grep with -z/-P
support is required", log showing `stub-rc7 --version` then `stub-rc7 -a -z -b -o
-P -- x`. So "GNU on stdout + wrong exit code" is *admitted by provenance* and
killed only by the later capability probe — S6's check (`rc==2`+marker) would FAIL
such a gate (marker absent), i.e. the counter's refusal-marker requirement is the
stricter half. Intent-wise: provenance is text-only self-report; the `-z/-P` probe
in `verify_claims` is the real second gate. A working-but-lying binary is
explicitly out of reach (gate comment :346-347 "a binary that lies about its
version is out of this check's reach"; control stub-gnu-rc0.sh ran the full
fixture to rc=1 with the stub serving 5 real match calls). Worth one defensive
line in `grep_pin_verify` (`"$cand" --version` rc check) — currently a stub that
*crashes* on --version but prints first is still accepted.

## S7/S8/S9 — echo-line parse is substring, not field equality

Current checks (c1-count.py:254, 261, 272):
S7: `"path=/usr/bin/grep" in line and "source=override" in line and "GNU grep" in line`
S8: same with `source=default`
S9: `empty_trip and same_as_ref and "source=override" in line` — **no path check at all**
Line pick: `next(l for l in err.splitlines() if l.startswith("GATE_GREP: "))` — first match only; a second GATE_GREP line is ignored.

### Demonstrated hole: honest echo of a wrong pin passes S7's substring check

Built `$D/path=/usr/bin/grep` (a real copy of GNU grep at a path that *contains*
the substring `path=/usr/bin/grep`), pinned via `RESEARCH_GATE_GREP`:

    GATE_GREP: path=/tmp/hyaku/chousa-r35/w2/RevScenarioS6S7S8S9/path=/usr/bin/grep source=override version="grep (GNU grep) 3.12-modified"

`"path=/usr/bin/grep" in line` → **True** though the pin is not `/usr/bin/grep`.
Also passes: `path=/usr/bin/grep path=/evil` dual-token lines, `version="…"` values
like `GNU grep-not`. For S7 the counter forces `RESEARCH_GATE_GREP=/usr/bin/grep`,
so exploitation needs the gate to echo a *different* path containing the substring
(canonicalized/decorated echo or outright fabrication) — narrow but real; for S9 the
missing `path=` check is wider (any override binary echoing source=override wins the
echo half; the tripwire still pins it to non-BASH_ENV resolution).

### Tighter assertion (proposed)

    m = re.fullmatch(r'GATE_GREP: path=(\S+) source=(\S+) version="([^"]*)"', line)
    ok = m and m.group(1) == REAL_GREP and m.group(2) == "override"   # "default" for S8
         and "GNU grep" in m.group(3)
    lines = [l for l in err.splitlines() if l.startswith("GATE_GREP: ")]
    ok = ok and len(lines) == 1

Verified in-process: current(trick)=True tight(trick)=False;
current(landed)=True tight(landed)=True; dual-`path=` line: current=True
tight=False. For S7/S9 additionally assert `m.group(1) == os.environ override
value` (already `/usr/bin/grep` here); for S8 the expected default token is
exactly `/usr/bin/grep`.

### Current assertion still discriminates

Against committed artifacts: landed gate S7/S8 lines are the exact
`GATE_GREP: path=/usr/bin/grep source=… version="grep (GNU grep) 3.12-modified"`
and score PASS; hardcoded control has no echo line at all → line="" → FAIL on all
of S7/S8/S9 (receipt above). The hole is only vs pins whose echoed path *contains*
the expected token — it never widens acceptance of the no-echo class the control
represents.

## Verdict

No MEETS-killing defect: landed gate earns 9/9 honestly (fresh seed re-derived;
S6 stub called once with `--version`, pre-match refusal at init :8039). Residual
counter hardening: (1) assert `stub_calls == 1` (and argv `--version`) in S6 —
demonstrated exploitable by a late-refusal mutant; (2) fullmatch the GATE_GREP
line and exact-compare `path`/`source` in S7/S8/S9 — demonstrated gameable via
substring paths and dual tokens; (3) add `path=` check to S9. Gate-side nit:
`grep_pin_verify` ignores the `--version` exit code (provenance is text-only by
design; capability probe catches dead binaries later).

## Limits

Mutant gate was a one-line local patch, not run through the full counter (S6
predicate applied directly to its observed rc/stderr/log — same quantities the
counter scores). No second-seed full-counter run beyond the receipt cited; S8's
trick-path variant needs a default-list mutation to exploit (S7/S9 need only the
echo). All runs env-scrubbed `env -i PATH=/usr/local/bin:/usr/bin:/bin`; no
network; nothing written outside $D and this directory.
