# ExecR34C1V3 — r34 long-span counter (c1-count-v3) re-derived on the landed gate

Seat: `chousa-r35-w2-ExecR34C1V3` (leaf executor; no subagents dispatched).
Date: 2026-10-23. Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Axis focus: **operability** (and, for the counter's own discipline, calibration).

---

## 0. Target result (as assigned)

Command (wave base revision `e87c5d7ea2dbf3730b36a3961de3f06261d015e4`, cloned to scratch):

```
LC_ALL=C C1_TMP=<scratch> python3 clone/corpus/evidence/round34/c1-count-v3.py \
  --gate clone/tools/research-gate.sh --seed 3593 \
  --receipt .ufo/waves/round-35/w2/ExecR34C1V3/c1v3-s3593.json
```

| seed | gate sha256 (scored) | counter sha256 | result | elapsed | exit |
|---|---|---|---|---|---|
| 3593 | `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` | `970cf9a709d72ed8b3ec91eeabc2b1778831f695b5ea18b40f026489f7f2da2a` | `LONGSPAN_MATCH=42/42` | **19.853 s** | 0 |
| 3607 | `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` | `970cf9a709d72ed8b3ec91eeabc2b1778831f695b5ea18b40f026489f7f2da2a` | `LONGSPAN_MATCH=42/42` | **29.022 s** | 0 |

Both receipts: `gate_rc: 1`, `gate_timed_out: false`, `matched: 42`, `total: 42`,
`predicate_holds: true`, `misses: []`, all 17 classes full
(`long-verbatim-ml 3/3`, `long-verbatim-1l 2/2`, `long-edge 2/2`,
`long-mut-head 2/2`, `long-mut-tail 2/2`, `long-mut-center 2/2`,
`long-decoys 7/7`, `long-decoys-exact 2/2`, `long-decoys-line-wrong 2/2`,
`long-split 2/2`, `long-glued-left 2/2`, `long-glued-right 2/2`,
`long-glued-then-valid 2/2`, `long-line-bound 2/2`, `long-line-wrong 2/2`,
`short-verbatim 3/3`, `short-mut 3/3`).

**Timing.** 19.9 s and 29.0 s wall clock, i.e. **1.3 %–1.9 % of the counter's
1500 s bound** (`corpus/evidence/round34/c1-count-v3.py:118`). The counter's own
`elapsed_s` covers fixture generation plus the gate run. No run came near the
bound; the 1500 s bound is not a live constraint on the landed gate.

Receipts (in-lane, sha256 pinned):
- `.ufo/waves/round-35/w2/ExecR34C1V3/c1v3-s3593.json`
- `.ufo/waves/round-35/w2/ExecR34C1V3/c1v3-s3607.json`

**Verdict on the assigned target: MEETS.** The r34 long-span counter scores
42/42 on two fresh seeds against the wave-base landed gate, with the gate sha
in each receipt equal to the sha the L1 named (`1f2fb4f5…`), so these are
measurements of the claimed gate and not of a control.

---

## 1. The most valuable result of this seat: the counter is NOT vacuous, and the landed gate is robust where the base gate is not

### 1a. The r34 counter discriminates broken long-span engines (calibration check)

Two mutants of the landed gate, each named and sha-pinned, seed 3593:

| mutant | change | result | gate sha256 |
|---|---|---|---|
| `mut-A1-directmax.sh` | `TOK_DIRECT_SPAN_MAX=32764` → `999999` (long spans forced through the argv/PCRE-limited direct matcher) | **25/42** | `e7e2a1433de63dd3c6c5de080739a6f08ab3cbcca61735c42a92b883b22fed3c` |
| `mut-A2-noconfirm.sh` | whole-span confirmation `[[ ${hay:offset:slen} == "$span" ]] \|\| continue` deleted | **29/42** | `ed62ef67ba3bb750eb2e95512de6ab05b67009c2fab7fa42f58d433a1cb7670e` |

A1's misses are exactly the long-span supported classes (`long-verbatim-ml 0/3`,
`long-edge 0/2`, `long-decoys-exact 0/2` …). A2's misses are the
confirmation-dependent classes (`long-decoys 7/7` → wrong verdicts,
`long-mut-tail`, `long-mut-center`). So the 42/42 on the landed gate is a
measurement of the long-span matcher, not a rubber stamp: the counter kills
both the "no chunk matcher" and the "no whole-span confirmation" engines.

### 1b. The base gate ALSO scores 42/42 — the r34 counter does not measure the round-35 work at all

`base-gate.sh` = the round-34 blob the round-35 freeze names as the pre-round
gate, sha256 `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b`:

```
LC_ALL=C C1_TMP=… python3 c1-count-v3.py --gate base-gate.sh --seed 3593
→ LONGSPAN_MATCH=42/42   elapsed 23.827 s   gate_rc 1
```
(receipt `c1v3-base-s3593.json`, sha256 `79947c3b2f230e035004fd65f296993a21cf27193a4119f6fee3430b2bf0efaf`)

**This is the key calibration statement about the round-35 claim record.** The
r34 long-span counter scores the *pre-round* gate and the *landed* gate
identically (42/42 vs 42/42). It is therefore blind to everything round 35
actually did (the grep pin, R1 `slen`, R2 comments). Re-deriving 42/42 with
this counter on the landed gate therefore **does not corroborate the round-35
C1 claim** — it only re-confirms that the round-34 long-span work survived.
The frozen round-35 P1 predicate correctly uses a *different* counter
(`corpus/evidence/round35/c1-count.py`, `GREP_PIN_MATCH`), and my measurement
gives no independent reason to doubt that. But the round-35 claim record
should not be read as if this counter backs C1.

### 1c. The landed gate is robust to a hostile PATH where the base gate is not

Same counter, same seed 3593, but with a **corrupting** `grep` shim first on
`PATH` (reports GNU grep for `--version`; makes the `-a -z -b -o -P` matcher
call report no match):

| gate | result | gate_rc | stderr |
|---|---|---|---|
| landed `1f2fb4f5…` | **42/42** | 1 | — |
| base `a6307edf…` | **0/42** | 2 | `research-gate: GNU grep with -z/-P support is required for claims and chain token matching` |

Receipts: `c1v3-shim-landed-s3593.json`
(`e019efdff243163e379f5046e3719f15fd49ac9205790b78e93eb9401a9b92d5`),
`c1v3-shim-base-s3593.json`
(`7dd61fbec1f6578642361940213bf9c405b91cf1522d5f99240c522f5bc0d509`).

This is the round-35 C1 mechanism observed **through an independent counter**:
the base gate's long-span matcher dies when PATH's grep lies; the landed gate's
pinned absolute path is immune and still scores 42/42. The BASH_ENV function
shim tells the same story from the other side: with `BASH_ENV` defining a
`grep()` function, the **base** gate's matcher is intercepted (760 543 bytes of
tripwire log, `c1v3-benv-base-s3593.json`) while the **landed** gate logs
**0 bytes** and still scores 42/42 (`c1v3-benv-s3593.json`,
`15e34181ec08bbca26d5bb4256bd219f3e4607a6145aae744e3330acdad46115`).
**No MEETS finding here: the landed gate survives every interception I could
construct.**

---

## 2. Finding: a dead branch in the wave-base gate's grep pin (operability defect)

`tools/research-gate.sh` at the wave base (`1f2fb4f5…`), lines 369–394:

```
369  grep_pin_init() {
...
384      for c in /usr/bin/grep /bin/grep; do
385        if grep_pin_verify "$c"; then cand=$c; break; fi
386      done
387      if [[ -z $cand ]]; then
388        c=$(command -v grep 2>/dev/null || true)
389        case "$c" in
390          /*) if grep_pin_verify "$c"; then cand=$c; fi ;;
391        esac
392      fi
393      [[ -n $cand ]] || grep_pin_refuse "no GNU grep found at /usr/bin/grep, /bin/grep or on PATH" ''
```

Line 388 asks `command -v grep` **after** line 351 has already defined the
shell function `grep() { command "$GREP_BIN" "$@"; }`. `command -v` therefore
resolves the *function*, not a binary, and prints the bare word `grep` — which
the `case "$c" in /*)` at line 389 rejects. **The PATH fallback is dead code.**

Proof (scratch, `deadfallback-proof.sh`, replicating lines 351/388/389 verbatim):

```
command -v grep            -> [grep]
PATH fallback branch: NOT TAKEN (not an absolute path)
type -P grep (what would work) -> [/usr/bin/grep]
```

End-to-end proof with a mutant gate (`mut-C1-deadfallback.sh`, sha256
`250e9dcbc0fbd405b183134f63022e4f3dc6d612e1ce493da4f63aa26042b261`, only
change: the two hardcoded candidates replaced by nonexistent paths), run with a
real GNU grep first on `PATH`:

```
research-gate: GREP_PROVENANCE refused: no GNU grep found at /usr/bin/grep, /bin/grep or on PATH (candidate=<none>)
rc=2
```

The refusal message promises a PATH search that the code cannot perform.

**Severity: low, and already fixed elsewhere.** On this host `/usr/bin/grep`
exists and reports GNU grep, so the default path always succeeds and the dead
branch is unreachable in practice; the visible effect is a misleading refusal
message, not a wrong verdict. It only bites a host whose GNU grep lives
somewhere other than `/usr/bin/grep` or `/bin/grep` (a Nix/BSD prefix, a
container with grep only in `/usr/local/bin`), where the gate refuses to run
even though a usable GNU grep is on `PATH` — the exact "operability" axis the
round scored 3/10.

**Independently confirmed and fixed mid-wave.** A sibling seat committed
`beb04ea` ("pin hardened (command/head/PATH-fallback/readonly/bounded probe)")
while this seat was measuring. The hardened gate (`a4768851…`) deletes the
fallback and says why in its own comment at `tools/research-gate.sh:405-408`:
*"No PATH consultation at all: the round-35 wave measured that a `command -v
grep` fallback resolves this script's own grep() function and is therefore dead
code."* The hardened refusal message is correspondingly honest: `"no GNU grep
at /usr/bin/grep or /bin/grep (set RESEARCH_GATE_GREP to an absolute path)"`.
So this finding was already in flight in the lane; what it adds is the
end-to-end mutant proof that the branch was not merely untidy but unreachable,
and the observation that the *fix is the right one* (deleting a branch that
cannot fire is better than repairing it to `type -P`).

---

## 3. Attack results on the pin (all against the wave-base gate `1f2fb4f5…`)

| attack | mechanism | result | verdict |
|---|---|---|---|
| PATH shim first, corrupting matcher | `PATH=shimbin:…` | **42/42**, 22.5 s | landed gate immune (base: 0/42) |
| BASH_ENV `grep()` function | `BASH_ENV=bashenv-grep.sh` | **42/42**, 19.1 s, tripwire **0 bytes** | landed gate immune (base: 760 543 bytes intercepted) |
| ambient `RESEARCH_GATE_GREP` = non-GNU stub | override to `fakegrep.sh` | **0/42**, rc 2 | refuses, correctly |
| ambient `RESEARCH_GATE_GREP` = real GNU grep copy | override to `pathgrep/grep` | **42/42**, 17.5 s | override honoured, output identical to default |
| override to a **lying** GNU grep | `liargrep.sh` reports `grep (GNU grep) 3.12-corrupt`, corrupts the matcher | **0/42**, rc 2, stderr `GNU grep with -z/-P support is required…` | caught by the runtime `-z/-P` capability probe at `tools/research-gate.sh:1762`, not by the version check — the stated limit in claims.md ("Provenance is self-reported") is therefore **narrower than stated for a non-functional liar**: the pin's version check is fooled, but the runtime probe still refuses. A liar that is *functionally* correct but *behaviourally* different would pass both. |
| no `grep` on `PATH` at all | 33-tool `PATH` without grep | gate runs, `--help` rc 0 | base gate: same, but its matcher dies (see §1c) |

The r34 counter does **not** control the ambient environment the way the r35
counter does: `corpus/evidence/round34/c1-count-v3.py:369` strips only
`CHOUSA_*` from the environment, while `corpus/evidence/round35/c1-count.py:88`
strips `CHOUSA_*` **and** `RESEARCH_GATE_*`. Consequence, measured: an ambient
`RESEARCH_GATE_GREP` in the operator's shell silently changes the r34
counter's result (42/42 → 0/42 with a non-GNU override,
`c1v3-ovr-fake-s3593.json`). The r35 counter fixed this; the r34 counter did
not. **[INFERENCE]** Any future round that re-uses `c1-count-v3.py` on a host
with `RESEARCH_GATE_GREP` exported in the environment would report a spurious
0/42. The two receipts I committed were produced with no ambient
`RESEARCH_GATE_*` (`env | grep -c RESEARCH_GATE` → `0`), so they are clean.

---

## 4. Claim-record and receipt audit

- **P1-v3's "no committed run of the same counter against the landed gate
  prints a lower count" clause was vacuous before this seat.** A cross-check of
  every committed receipt carrying the schema `chousa-r34-c1-receipt/v3` in the
  repo found **zero** receipts whose `gate_sha256` is the landed gate's
  `1f2fb4f5…`; the only two are the ones I just committed. The three committed
  r34 measure receipts (`.ufo/waves/round-34/measure/c1v3-s360{1,2,3}*.json`)
  all carry gate sha `772a1d8e…` — a **different gate blob** (the round-34
  tip), not the round-35 landed gate. So before this seat the clause was true
  only because it had no instances to range over; now it has two 42/42
  instances on the named gate and still holds.
- **The SCORECARD's "0/42 ×2 by the 1500 s bound in the UTF-8 locale" note no
  longer reproduces.** `SCORECARD.md:1927` records the *base* as 0/42 twice
  under UTF-8. I re-ran seed 3593 with `LC_ALL` unset (`en_US.UTF-8`):
  base gate → **42/42**, 38.5 s; landed gate → **42/42**, 36.3 s. Both finish
  in well under the bound. The note is stale for the current base blob and
  should be corrected or its provenance (which base blob, which locale, which
  clock) stated. The r34 gate's own long-span work (chunk matcher +
  whole-span confirmation) is what removed the locale blow-up; that is
  round-34 debt, not round-35 work.
- **Round-35 claim text.** `corpus/evidence/round35/claims.md:137` puts
  "C1 carried debt (spans ≥ 32768, `unverified (required controls held)`)"
  in the *not claimed* list, and `SCORECARD.md:1950` repeats that the frozen
  exclusion is not re-opened. My §1a mutants are consistent with that: the
  r34 counter is a *regression* instrument for the round-34 debt, and I have
  not re-scored the round-34 C1 verdict.

---

## 5. Round shape: the landed gate moved under this seat

The wave-base gate (`1f2fb4f5…`) was committed as the round-35 landing at
`e87c5d7`. **While this seat was measuring**, a sibling seat committed
`beb04ea` with a hardened pin (sha `a4768851…`). I therefore report the
assigned target against the **frozen wave-base sha `1f2fb4f5…`** (as the task
specifies), and additionally re-ran the counter against the new HEAD gate for
continuity:

| gate | seed | result | elapsed | receipt |
|---|---|---|---|---|
| HEAD `a4768851…` | 3593 | **42/42** | 17.9 s | `c1v3-head-s3593.json` |
| HEAD `a4768851…` | 3607 | **42/42** | 23.4 s | `c1v3-head-s3607.json` |

So the long-span behaviour is unchanged by the pin hardening. Note for the
record: **no committed receipt of the r34 counter exists against the new HEAD
gate sha `a4768851…`** (cross-checked across the repo) — my two `c1v3-head-s*`
receipts in this directory are the first.

---

## 6. Artifacts

All in-lane (`.ufo/waves/round-35/w2/ExecR34C1V3/`), each well under 1 MiB:

| file | sha256 (receipt content) |
|---|---|
| `c1v3-s3593.json` | primary, gate `1f2fb4f5…`, 42/42 |
| `c1v3-s3607.json` | primary, gate `1f2fb4f5…`, 42/42 |
| `c1v3-head-s3593.json` | gate `a4768851…`, 42/42 |
| `c1v3-head-s3607.json` | gate `a4768851…`, 42/42 |
| `c1v3-base-s3593.json` | gate `a6307edf…`, 42/42 (base also passes) |
| `c1v3-A1-s3593.json` | mutant `e7e2a143…`, 25/42 |
| `c1v3-A2-s3593.json` | mutant `ed62ef67…`, 29/42 |
| `c1v3-shim-landed-s3593.json` | gate `1f2fb4f5…`, 42/42 under corrupting PATH |
| `c1v3-shim-base-s3593.json` | gate `a6307edf…`, 0/42 under corrupting PATH |
| `c1v3-benv-s3593.json` | gate `1f2fb4f5…`, 42/42, BASH_ENV tripwire 0 bytes |
| `c1v3-benv-base-s3593.json` | gate `a6307edf…`, 42/42, BASH_ENV tripwire 760 543 bytes |
| `c1v3-ovr-fake-s3593.json` | ambient non-GNU override → 0/42 |
| `c1v3-ovr-real-s3593.json` | ambient real override → 42/42 |
| `c1v3-liar-s3593.json` | lying-GNU override → 0/42 (runtime probe catches) |
| `c1v3-utf8-s3593.json` | landed, UTF-8, 42/42 |
| `c1v3-utf8-base-s3593.json` | base, UTF-8, 42/42 (SCORECARD note stale) |

Mutant gates, shims and logs live in
`/tmp/hyaku/chousa-r35/w2/ExecR34C1V3/` (scratch, outside the repo):

```
mut-A1-directmax.sh     e7e2a1433de63dd3c6c5de080739a6f08ab3cbcca61735c42a92b883b22fed3c
mut-A2-noconfirm.sh     ed62ef67ba3bb750eb2e95512de6ab05b67009c2fab7fa42f58d433a1cb7670e
mut-C1-deadfallback.sh  250e9dcbc0fbd405b183134f63022e4f3dc6d612e1ce493da4f63aa26042b261
head-gate.sh            a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad
base-gate.sh            a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b
```
Scratch sha256 list: `sha256sum /tmp/hyaku/chousa-r35/w2/ExecR34C1V3/*.sh /tmp/hyaku/chousa-r35/w2/ExecR34C1V3/*.json`.

No production file was read-modified: `tools/research-gate.sh`, `corpus/`,
`SCORECARD.md`, `LOG.md` and the wave directories were opened read-only. No
git/jj write command was run. No network. No package install.

---

## 7. Limits of this seat

- This seat measured **C1 (operability) only**, and only through the r34
  long-span counter plus direct gate invocations. **C2 (mechanism witness) was
  not touched**; no statement here bears on `WITNESS_SEPARATED`.
- The `c1-count-v3.py` counter is the **round-34** instrument. My §1b result
  (base = landed = 42/42) means it cannot be cited as evidence for the
  round-35 grep-pin claim. The round-35 C1 predicate (`GREP_PIN_MATCH`) has
  its own counter and its own seats; I did not re-run it.
- The dead-fallback finding (§2) is against the **wave-base** gate; the sibling
  commit `beb04ea` had already removed that branch by the time I finished, so
  it is a report on the frozen base, not a live defect in the current HEAD.
- The `liargrep.sh` result shows the runtime `-z/-P` probe catches a
  *non-functional* liar. It does **not** show the pin catches a functional but
  behaviourally different grep; that remains the stated limit in
  `corpus/evidence/round35/claims.md`.
- All timings are single-run wall clock on this host under concurrent wave
  load; they are not benchmarks.
