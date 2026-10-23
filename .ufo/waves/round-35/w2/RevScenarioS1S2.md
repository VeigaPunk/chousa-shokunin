# Round 35 w2 — RevScenarioS1S2: audit of the C1 counter's S1/S2 assertions

Reviewer: chousa-r35-w2-RevScenarioS1S2. Date: 2026-10-23. Leaf, read-only on lane
production files; all experiments in `/tmp/hyaku/chousa-r35/w2/RevScenarioS1S2/` and
this directory. No installs performed. Gate pins verified:
`tools/research-gate.sh` sha256 `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`,
`.ufo/waves/round-35/repairs/base-gate.sh` sha256 `a6307edf687ac0fb…995b` (both re-derived this session).

## Question audited

Is `tripwire empty` + `output equals reference` (c1-count.py:214-221, S1/S2) sufficient
to prove the gate never executes the PATH/BASH_ENV shim? Named candidate evasions:
shim invoked with no argv; shim under a different name; shim inside a subshell whose
redirect fails.

## Answer: NOT sufficient. Two attack gates score 9/9, predicate_holds=true, while shims execute.

### Baseline (sanity)

`env -u BASH_ENV C1_TMP=<scratch> TMPDIR=<scratch> python3 corpus/evidence/round35/c1-count.py
--seed 3501 --receipt <artdir>/landed-s3501.json` → `GREP_PIN_MATCH=9/9`, rc=0,
`gate_sha256=1f2fb4f522d9a670…` (receipt). The landed gate scores full marks in my env.

### Attack A — landed gate + one PATH-shim probe + EXIT tripwire sweep → 9/9

Artifact `attack-a.sh` (sha256 `51ffec6a5e940e6e657257461023dfe48a76ef1adae0ec1e756fac9459c9f6f4`),
diff vs landed gate: (1) in the default pin branch, before pinning, probe the
PATH-resolved grep with `type -P grep` and run `"$c" --version`; (2) an EXIT trap that
captures and zeroes `$PWD/_shim/trip-*.log` (shimlog-a). Counter run: 9/9, rc=0,
receipt `attack-a-s3501.json` (`predicate_holds=true`, gate sha recorded honestly).
`attack-shimlog-a.txt` captures `--version` under `trip-path.log`: the PATH shim
executed during the S1 run, the counter scored S1 PASS with `tripwire_bytes: 0`.
S1's own doc string says the scenario requires "the gate never execs the PATH shim"
(c1-count.py:31-32); attack A violates exactly that while scoring PASS.

### Attack B — the round-34 base behavior (every matcher call through the PATH shim) → 9/9

Artifact `attack-b.sh` (sha256 `3a7cbefc2d9fcc29ecc709fd8da96d178d11794371f6641e0ab73d81136bbda2`):
default pin branch resolves `type -P grep` FIRST and pins it if it verifies (the shim
verifies: it execs real `/usr/bin/grep`, so `--version` reports GNU), plus the same
EXIT sweep. Counter run: 9/9, rc=0, `predicate_holds=true`, S1 `tripwire_bytes: 0`,
`output_matches_reference: true` (receipt `attack-b-s3501.json`). `attack-shimlog-b.txt`
captures the shim executing EVERY matcher call, e.g.:

```
--version
-a -z -b -o -P -- x
-a -z -b -o -P -- \x61\x6c\x70\x68\x61…  (x4, one per claim match)
-Fn -m1 -e charlie
```

This is a MEETS-class result in the counter's own terms: an engine that routes all
matcher greps through an attacker-controlled PATH shim receives the maximum score the
instrument can award, byte-identical output, empty tripwires. The shim delegation is
byte-equivalent by construction — precisely the round-34 property C1 claims to have
removed ("a PATH shim answers identically … while running different code",
research-gate.sh:335-337).

### Why the tripwire is forgeable (instrument defect, cited)

1. `run_gate` launches the gate with `cwd=root` (c1-count.py:94) and keeps its scratch
   at `root/_shim` (c1-count.py:168). The tripwires are reachable from the gate's own
   working directory — no privilege, no guessing: `"$PWD"/_shim/trip-*.log`.
2. `empty_trip` (c1-count.py:201-205) is checked only after the gate process exits, so
   any in-gate truncation before exit is invisible. Deletion fails safe (OSError →
   False), truncation does not.
3. Secondary leak: the gate env strips only `CHOUSA_*`/`RESEARCH_GATE_*` (c1-count.py:88),
   so `C1_TMP`/`TMPDIR` survive into the gate; a gate could locate the counter root
   even if the cwd tell were closed.
4. `same_as_ref` (c1-count.py:207-210) compares rc/drift/parsed CLAIM lines only —
   necessary, never sufficient, for "which grep ran".

### The three named naive evasions: all caught (tripwire mechanism itself is sound)

Tested against a copy of the counter's exact shim (write_shim body, c1-count.py:109-112),
tripwire at `/tmp/hyaku/chousa-r35/w2/RevScenarioS1S2/t/trip.log`:

- no argv: `./shim` (zero args) still appends 1 byte (`printf '%s\n' "$*"` prints a
  newline) — file grew to 11 bytes after `--version` + bare call; `empty_trip` (size==0)
  catches it.
- different name (`cp shim grep-alias; ./grep-alias …`): still logs (target path is
  embedded in the shim, not argv-dependent) — caught.
- subshell with failing outer redirect (`( ./shim … >/nonexistent-dir/out )`): the
  shim's own `>>tripwire` append is independent of the outer redirect; still logs — caught.

[INFERENCE] `ulimit -f 0` before invoking grep would kill the shim's 1-byte append with
SIGXFSZ, but it kills the shim's shell before `exec grep`, so output breaks and
`same_as_ref` catches it. A mount-namespace bind-over of the tripwire would work but
still needs the path from (1)/(3).

### The landed gate itself is honest under S1/S2 — and its PATH fallback is dead code

First A/B attempt used `command -v grep` for probe/resolution: no shim traffic occurred
at all (shimlogs empty). Reason: the gate defines `grep() { command "$GREP_BIN" "$@"; }`
(research-gate.sh:351) before `grep_pin_init` (research-gate.sh:369), and bash's
`command -v grep` reports that function (bare name, not `/*`), so the default branch's
PATH fallback (research-gate.sh:388-391) can never yield an absolute path — it is dead
code given the gate's own wrapper. The landed gate therefore pins `/usr/bin/grep` (or
refuses) and never execs a PATH shim; its 9/9 is genuine. Note S3's "gate runs without
grep on PATH" passes via the filesystem default, not via the fallback.

## Verdict

- **Calibration finding (C1 instrument):** S1/S2 do NOT prove the pin. `tripwire empty`
  is forgeable by any gate that can see the counter's scratch (cwd or env) and truncate
  before exit; two such gates score `GREP_PIN_MATCH=9/9 predicate_holds=true` — the
  counter's discrimination between the landed gate and a shim-routing engine is 0 bits.
  This is the most valuable class of result for the wave: a 9/9 engine that executes
  the shim exists (attack B).
- **P1 as frozen is not killed:** the kill rule fences scored runs by gate sha
  ("a scored run whose gate sha256 differs from the receipt's is not the claim's
  measurement", claims.md C1 kill rule); both attack receipts carry their own shas
  (`51ffec…`, `3a7cbefc…`), not `1f2fb4…`. The landed gate's honest 9/9 stands. What
  fails is the audit strength claimed for S1/S2 as evidence of the pin.
- **Suggested instrument hardening (not applied — read-only lane):** create tripwires
  outside the fixture root under `os.urandom` names never present in the gate env or
  cwd (pass the path only to the shim via the shim file itself, which already embeds
  it), and/or verify emptiness via an held-open fd's inode size, and strip
  `C1_TMP`/`TMPDIR`/`BASH_ENV` from the gate env (BASH_ENV currently passes through a
  hostile operator shell into every run, including the reference).

## Artifacts (this directory; all < 1 MiB)

- `attack-a.sh` sha256 `51ffec6a5e940e6e657257461023dfe48a76ef1adae0ec1e756fac9459c9f6f4`
- `attack-b.sh` sha256 `3a7cbefc2d9fcc29ecc709fd8da96d178d11794371f6641e0ab73d81136bbda2`
- Receipts: `landed-s3501.json`, `attack-a-s3501.json`, `attack-b-s3501.json`
  (label `GREP_PIN_MATCH=9/9`, `predicate_holds=true` in all three)
- Shim evidence: `attack-shimlog-a.txt` (probe line), `attack-shimlog-b.txt` (probe +
  all matcher calls)
- Scratch (large logs; /tmp): `/tmp/hyaku/chousa-r35/w2/RevScenarioS1S2/` (tmp dirs
  auto-removed by the counter; `t/` holds the evasion-scenario probes)

## Limits

One seed (3501) per run; the finding is about the instrument, not seed-dependent.
Attack gates were not run against C2 or the witness. `empty_trip`'s fail-safe on
deletion was read from code (c1-count.py:201-205), not exercised. The dead-code
observation on research-gate.sh:388-391 follows from bash `command -v` semantics and
wrapper order (:351 before :369); I did not construct a runtime case where
/usr/bin/grep and /bin/grep are both absent.
