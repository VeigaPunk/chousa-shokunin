# ExecC2Rerun — round 34 attempt 2, wave 2a2 (falsify + verify)

Seat: `ExecC2Rerun` (executor, leaf). Scope: re-derive the **C2** after-state from the frozen
tip and attack the claim record; C3 spot-checked for the calibration axis. Read-only on all lane
production files; every experiment in `/fast/scratch/hyaku/chousa-r34-a2/w2/ExecC2Rerun/`.

**Verdict: C2's P2 predicate HOLDS on re-derivation (37/37 on three fresh seeds, no committed
lower run on the landed gate). The committed after-receipts are consistent. Three claim-record
defects found (one substantive, two cosmetic) — none of them moves the C2 verdict.**

---

## 0. Pinning (what I scored)

```
$ sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b  tools/research-gate.sh
$ git -C .../chousa-shokunin rev-parse HEAD
fe3db76c0ae9fa18cfebcf127fec073354a1eb03          # working tree tip = re-frozen spec commit
$ git -C .../chousa-shokunin status --porcelain
?? .ufo/waves/round-34/w2a2/                       # only untracked wave dir; no tracked dirt
$ git rev-parse 707da818:tools/research-gate.sh 707da818:corpus/evidence/round34/c2-count.py
8ebd4704e3f4cc2aeeac767db7d5f9b7d12d95a0          # blob ids
8a2c519fbf660e318a7f0afd103cee520bf1f033
$ sha256sum <(git show 707da818:tools/research-gate.sh) <(git show 707da818:corpus/evidence/round34/c2-count.py)
a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b
8c0def4d377cdf1a1e4bd2c9151bb0846216658ff14d725d15ac037c12212173
```

The working-tree gate digest equals the committed blob digest at the frozen tip, and at the
working-tree tip too (`git rev-parse fe3db76:tools/research-gate.sh` → same blob `8ebd4704…`),
so the working tree and the frozen tip carry the same gate bytes. Gate change vs the pre-fix
blob is exactly one production line plus selftest cases:

```
$ git diff 7c7eb3a:tools/research-gate.sh fe0f22e:tools/research-gate.sh   # non-comment lines only
-TOK_DIRECT_SPAN_MAX=32767     # span bytes whose 4N-byte pattern still fits argv
+TOK_DIRECT_SPAN_MAX=32764     # span bytes whose 4N-byte pattern fits argv AND PCRE2
+  dz_span=$(printf 'w%04d ' {1..5461})   # exactly 32766 bytes
… (3 tclaims blocks: claims-deadzone, claims-deadzone-line, claims-deadzone-edge)
```
Full diffstat: `1 file changed, 57 insertions(+), 16 deletions(-)`. No matcher logic changed —
only the routing constant. Matches the design's "no other matcher change".

Scratch clone (used for every run below):

```
$ unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
$ git clone -q …/chousa-shokunin clone && git -C clone checkout -q 707da8184a0fc4d10ab3f17271556cdf364f0af5
$ git -C clone rev-parse HEAD → 707da8184a0fc4d10ab3f17271556cdf364f0af5
$ sha256sum clone/tools/research-gate.sh clone/corpus/evidence/round34/c2-count.py
a6307edf687ac0fb…62995b   clone/tools/research-gate.sh
8c0def4d377cdf1a…12173   clone/corpus/evidence/round34/c2-count.py
```
`df -h /fast` → 42 G avail before the runs; all scratch writes bounded (largest artifact 367 KB).

---

## 1. C2 re-derivation on fresh seeds (the primary item)

Command, run from the clone with `C2_TMP` in scratch and `LC_ALL=C`:

```
LC_ALL=C C2_TMP=/fast/scratch/hyaku/chousa-r34-a2/w2/ExecC2Rerun/tmp \
  timeout 1800 python3 corpus/evidence/round34/c2-count.py --seed N \
  --receipt …/.ufo/waves/round-34/w2a2/ExecC2Rerun/c2-rerun-s<N>.json
```

Seeds 7311, 7417, 7589 are fresh (not 5011/5023/5033/5047). Results:

| seed | label | exit | gate_rc | timed_out | elapsed_s | gate sha (16) | counter sha (16) | predicate_holds | misses |
|---|---|---|---|---|---|---|---|---|---|
| 7311 | `DEADZONE_MATCH=37/37` | 0 | 1 | false | 14.656 | `a6307edf687ac0fb` | `8c0def4d377cdf1a` | true | 0 |
| 7417 | `DEADZONE_MATCH=37/37` | 0 | 1 | false | 10.181 | `a6307edf687ac0fb` | `8c0def4d377cdf1a` | true | 0 |
| 7589 | `DEADZONE_MATCH=37/37` | 0 | 1 | false | (see receipt) | `a6307edf687ac0fb` | `8c0def4d377cdf1a` | true | 0 |

Per-class lines were identical on all three runs and identical to the committed receipts:

```
dz-verbatim-ml 3/3   dz-verbatim-1l 2/2   dz-edge 2/2        dz-mut-head 2/2
dz-mut-tail 2/2      dz-mut-center 2/2    dz-decoys 5/5      dz-decoys-exact 2/2
dz-decoys-line-wrong 2/2   dz-split 2/2   dz-glued-left 2/2  dz-glued-right 2/2
dz-glued-then-valid 1/1    dz-line-bound 2/2   dz-line-wrong 2/2
short-verbatim 2/2   short-mut 2/2
```

Receipts (this seat's directory):
`.ufo/waves/round-34/w2a2/ExecC2Rerun/c2-rerun-s7311.json` (sha256 `32354e71…bb8ea`),
`c2-rerun-s7417.json` (`80a8e424…c0529`), `c2-rerun-s7589.json` (`69b16640…d02e5f`).

**P2 re-derived.** P2 requires `DEADZONE_MATCH=37/37` with `predicate_holds=true` on each of two
fresh-seed runs and no committed run of this counter on the landed gate below 37. Two fresh seeds
are enough; I ran three. Satisfied.

### 1a. Span lengths really are in the dead zone (fixture-level check)

I regenerated the seed-7311 fixture with `--keep` and measured every record's span byte length
against its class:

```
dz-decoys 5  min=32765 max=32767     dz-decoys-exact 2  32765..32766
dz-decoys-line-wrong 2 32765..32767   dz-edge 2 32765..32767
dz-glued-left 2 32766..32767          dz-glued-right 2 32766
dz-glued-then-valid 1 32766           dz-line-bound 2 32766..32767
dz-line-wrong 2 32765                 dz-mut-center 2 32766..32767
dz-mut-head 2 32766                   dz-mut-tail 2 32765..32766
dz-split 2 32767                      dz-verbatim-1l 2 32765..32766
dz-verbatim-ml 3 32765..32767
short-mut 2 4092..4093                short-verbatim 2 4093..4095
```
All 33 dead-zone records sit inside 32765..32767 (the short controls at ~4093 stay on the direct
path). Fixture kept at `/fast/scratch/hyaku/chousa-r34-a2/w2/ExecC2Rerun/fixture-s7311/`
(claims.jsonl 37 lines + truth.json).

Running the gate directly on that fixture: `rc=1`, 37 `CLAIM id=…` lines, 4
`CLAIM_LINE_MISMATCH` findings (exactly the 4 mislocated records), and
`RESEARCH_GATE: DRIFT (claims=37 supported=14 contradicted=0 unsupported=19 mismatched=23 …)`.

### 1b. Do-nothing control, re-derived (the "before" state)

Pre-fix gate blob extracted read-only: `git show 7c7eb3a:tools/research-gate.sh` →
sha256 `772a1d8e4d94dbf3a44a64bf850b1324e51546eeb62abcd7b3ec585f0e003e58` (the digest the
committed before-receipts name). Re-ran the same counter against it on the same fresh seeds:

```
seed 7311 → DEADZONE_MATCH=21/37, exit=1, 16 misses, all observed=unsupported
seed 7417 → DEADZONE_MATCH=21/37, exit=1, 16 misses, all observed=unsupported
```
Miss classes (identical on both seeds): dz-verbatim-ml 3, dz-verbatim-1l 2, dz-edge 2,
dz-decoys-exact 2, dz-line-bound 2, dz-decoys-line-wrong 2, dz-line-wrong 2,
dz-glued-then-valid 1. That is precisely the 12 long `supported` + 4 long `mislocated` records —
every dead-zone record whose truth is *not* "unsupported". Receipts copied into this seat's
directory: `c2-beforegate-s7311.json` (`f20f602c…3c4d`), `c2-beforegate-s7417.json`
(`9fabc61e…d3faffb`). This matches the committed before-receipts (21/37, 16 misses, stderr
`grep: regular expression is too large`).

**Therefore the counter is live on this target**: the same counter, same seeds, same fixture
generator, differs 21/37 → 37/37 purely because of the landed gate.

### 1c. Counter discriminating power (mutants — the counter can fail)

All mutants are scratch copies; the lane gate was never touched.

| scratch gate | counter result | what it shows |
|---|---|---|
| pre-fix `772a1d8e` (real blob) | **21/37**, exit 1 | target is the constant |
| `TOK_DIRECT_SPAN_MAX=32766` (one byte off) | **25/37**, exit 1 | window boundary is genuinely pinned; 32766 still fails 12 records |
| landed gate with the whole-span confirmation removed (`[[ ${hay:offset:slen} == "$span" ]] \|\| continue` deleted) | **26/37**, exit 1 | the counter catches a matcher that only probes chunks (dz-decoys 0/5, dz-mut-tail 0/2, dz-mut-center 0/2) |
| junk gate: always prints `observed=supported`, never mislocated | **14/37**, exit 1 | a "claims everything supported" gate cannot pass; 23 records fail (unsupported + mislocated classes) |
| landed gate, `LC_ALL=C` unset (default `en_US.UTF-8` locale) | **37/37**, exit 0 | the after-state does not depend on `LC_ALL=C` for this counter (the gate forces `LC_ALL=C` internally in `tok_span_offsets`) |

Also probed the host's actual PCRE ceiling directly (grep `-P`, literal and `\xHH` patterns):

```
literal 32764 chars → compiles; literal 32765 → "grep: regular expression is too large"
\xHH pattern of 32764 bytes (131056 text chars) → compiles; 32765 bytes → too large
compact a{60000} → compiles (few code units); alternation of 40000 single chars → too large
```
So the failure is a **compiled-pattern size** ceiling, not a text-length ceiling, and it binds at
32765 pattern bytes = 32765 code units in both encodings. The lane's mechanism note
(`corpus/knowledge/dead-zone-pcre-r34.md:14-15`, quoting pcre2limits(3): "approximately 64
thousand code units") is directionally right about *which* ceiling binds first, but its
arithmetic gloss ("`\xHH` escapes compile to code units at roughly two per span byte") does not
match my measurement — my probe shows the ceiling tracks *pattern bytes* (code units), 1:1, not
2:1. [INFERENCE] The man-page figure is a compiled-size bound in code units; the lane's
"two per span byte" phrasing would put the boundary at ~16383 bytes, which is not what the host
does. The measured boundary (32765 fails, 32764 compiles) is reproduced exactly, so the fix and
the claim's numbers stand; only the explanatory sentence is off.

### 1d. Committed after-receipts vs. what I observed

Committed: `.ufo/waves/round-34/measure-a2/c2-after-s{5011,5023,5033,5047}.json`.

```
file                     label                      gate sha (12)  counter sha (12)  seed  matched  per-class all full
c2-after-s5011.json     DEADZONE_MATCH=37/37       a6307edf687a   8c0def4d377c    5011  37      17/17 classes full
c2-after-s5023.json     DEADZONE_MATCH=37/37       a6307edf687a   8c0def4d377c    5023  37      17/17
c2-after-s5033.json     DEADZONE_MATCH=37/37       a6307edf687a   8c0def4d377c    5033  37      17/17
c2-after-s5047.json     DEADZONE_MATCH=37/37       a6307edf687a   8c0def4d377c    5047  37      17/17
```
All four: same counter digest as the tip blob (`8c0def4d…`), same gate digest as the tip blob
(`a6307edf…`), **four distinct seeds**, `gate_rc=1`, `gate_timed_out=false`, `misses=[]`,
`predicate_holds=true`. Consistent with the four committed before-receipts (21/37, gate
`772a1d8e…`, same counter digest, seeds 5011/5023 — deliberately the same seeds so the
before/after pair differs only in the gate).

I also **re-ran the two committed seeds** through the tip clone and compared field by field
against the committed receipts:

```
seed 5011: mine DEADZONE_MATCH=37/37 / committed 37/37 ; per_class_equal=True ; gate_sha_equal=True ; counter_sha_equal=True
seed 5033: mine DEADZONE_MATCH=37/37 / committed 37/37 ; per_class_equal=True ; gate_sha_equal=True ; counter_sha_equal=True
```
Elapsed differs (mine 13.82 s / 12.12 s vs committed 7.19 s / 6.69 s) — host load only; the
committed runs were issued in a tight sequence. No behavioural difference.

### 1e. "No committed run of this counter on the landed gate below 37" — exhaustive history scan

I scanned every reachable commit's blobs for the counter's label string:

```
$ git grep -h -E 'DEADZONE_MATCH=[0-9]+/37' $(git rev-list --all) -- '*.json' | sort | uniq -c
     48  "label": "DEADZONE_MATCH=21/37",
     80  "label": "DEADZONE_MATCH=37/37",
```
Resolving each distinct receipt blob (path → label → gate sha → counter sha → seed → matched)
gives exactly ten distinct receipts in lane history:

```
measure-a2/c2-after-s5011/5023/5033/5047.json  37/37  gate a6307edf687a  ctr 8c0def4d377c  seeds 5011/5023/5033/5047
measure-a2/c2-before-s5011/5023.json          21/37  gate 772a1d8e4d94  ctr 8c0def4d377c  seeds 5011/5023
```
(the other 78 label occurrences are the same ten files re-counted across the commits that
contain them). **Every run binding the landed gate `a6307edf…` prints 37/37; the only sub-37
runs bind the pre-fix gate `772a1d8e…`.** P2's second clause holds.

Untracked wave-2a2 scratch receipts in this same wave (other seats) — 85 DEADZONE receipts
scanned; 17 of them bind gate `a6307edf…` (seeds 5107, 5501, 6101, 6102, 6131, 6203, 6701309,
6701321, 9011, 9029, 7311, 7417, 7589, 6101, 6102, 9011, 9029) — **all 37/37, none below 37**.

### 1f. Bound checks

- Gate run time: 10–15 s wall for 37 records — far under the counter's 1500 s `GATE_TIMEOUT_S`
  and the claim's 1500 s bound.
- `bash tools/research-gate.sh --selftest` at the tip clone: **`RESEARCH_GATE_SELFTEST: PASS
  (256 cases, 0 skipped)`**, exit 0, 93.95 s. The three dead-zone cases are `ok-case 254
  claims-deadzone`, `ok-case 255 claims-deadzone-line`, `ok-case 256 claims-deadzone-edge`
  (log copied to this seat's directory as `selftest-tip-clone.log`, sha256 `5311643c…c12`).
  This reproduces the SKILL.md tallies the C3 audit asserts.

---

## 2. C3 spot-check (calibration axis)

```
$ cd clone && timeout 900 python3 corpus/evidence/round34/self-audit.py --lane .
… 43 AUDIT lines, all "ok" …
SELF_AUDIT_MISMATCHES=0
SELF_AUDIT_UNDISPOSITIONED=0
```
Exit 0. `diff` against the committed `.ufo/waves/round-34/measure-a2/audit-first-run.txt`:
**identical** (43 checks, same order, same counts). So P3's "K reproduced verbatim by a re-run"
holds (I ran it twice more: once for the diff, once earlier — same output both times).

Check-kind census of the committed set (`audit-set.json`, blob `a95fcc3b…`, unchanged between
`0af0844` and the tip): 12 `git_commit`, 4 `sha256`, 4 `receipt_binding`, 20 `path`, 3
`grep_assert` = **43 checks**, matching the claim's "43 checks".

Discriminating power (scratch copies only):
- injected 2 lies into a scratch copy of the set (bad `expect` digest on `gate-head-digest`,
  bad path on `path-00`) → `SELF_AUDIT_MISMATCHES=2`, `SELF_AUDIT_UNDISPOSITIONED=2`, with the
  two MISMATCH detail lines printed.
- same set + a scratch dispositions file naming one id → `SELF_AUDIT_MISMATCHES=2`,
  `SELF_AUDIT_UNDISPOSITIONED=1` (i.e. the disposition key works).
This reproduces the committed negative control's shape (`measure-a2/audit-negative-control.txt`).
`corpus/evidence/round34/audit-dispositions.md` is committed **empty (0 bytes)** — consistent
with zero mismatches; the tool counts, it does not gate.

---

## 3. Defects found in the claim record (falsify findings)

**D1 (substantive, claim-record arithmetic) — the frozen design's before-state prediction is
wrong and was never amended.** `corpus/evidence/round34/claims-a2.md:103` states, for the
do-nothing control: "The 17 long-supported records … must miss … short records (4) pass.
**Expected ceiling 4/37**." Measured before-state on the unfixed gate is **21/37**, not ≤4/37
(committed receipts `c2-before-s5011/5023.json` = 21/37, and my re-runs = 21/37, 16 misses).
The arithmetic error: the 12 long `supported` + 4 long `mislocated` records fail (16 misses),
but the 17 long `unsupported`-truth records (mutants, decoys, split, glued) *pass* on the broken
gate — the broken matcher reports `observed=unsupported`, which is exactly their truth — and the
4 short records pass, so 21/37 is the ceiling, not 4/37. `claims-a2.md` (frozen at `7c7eb3a`)
was never amended; the SCORECARD/LOG correctly report the measured 21/37, so the *recorded*
before-state is right and only the design's prediction text is stale.
**Effect on the verdict: none.** P2's kill rule is scoped to "a committed run of this counter
**on the landed gate** below 37"; the 21/37 runs bind `772a1d8e…`, not `a6307edf…`. But this is
the same class of defect the round mined from r35 ("planned entries are hypotheses"): a frozen
design sentence that the measurement falsified and no erratum corrected. Recommend an append-only
erratum on `claims-a2.md` (the design file already carries the pattern — see `claims.md:194`).

**D2 (cosmetic) — the gate's own selftest comment misnumbers the new cases.**
`tools/research-gate.sh:7857` says "round-34 attempt-2 C2 selftest cases (cases 255-257)", but
the actual case numbers at the tip are 254, 255, 256 (`ok-case 254 claims-deadzone`,
`255 claims-deadzone-line`, `256 claims-deadzone-edge` in my selftest log). The gate also
numbers the C1 block "cases 252-253" where the run shows 252/253 correct — so only the C2
comment is off by one. SCORECARD.md:1956, LOG.md:1291, SKILL.md:78 and
`corpus/lessons/round-34.md:86` all say "254–256", i.e. the *prose* is right and the gate
comment is wrong. Purely a comment.

**D3 (cosmetic) — mechanism gloss in the knowledge doc.** As noted in §1c, "The `\xHH` escapes
compile to code units at roughly two per span byte" (`corpus/knowledge/dead-zone-pcre-r34.md:15`,
and the parallel phrasing in `corpus/knowledge/long-span-argv-r34.md:16`) predicts a boundary
near 16383 bytes; the host actually fails at 32765 bytes with a 1:1 byte↔code-unit ceiling.
The measured window, the fix and every committed number are unaffected.

**Coverage gap (not a defect, a limit) — C3 does not audit the SCORECARD.** C3's surface is
"the lane's round-34 self-description (SCORECARD rows, LOG entry, SKILL.md tallies, SHONEN
evidence pointers)", but the frozen audit set contains **no check that reads SCORECARD.md** — no
`path` entry for it and no `grep_assert` over it; the three text assertions are 2×SKILL.md and
1×LOG.md, and the SHONEN checks are path-existence only. So `SELF_AUDIT_MISMATCHES=0` does not
certify the SCORECARD round-34 row's numbers (37/37, 21/37, 43 checks, PASS 256). I checked
those numbers by hand instead and they are all correct as of the tip (`SCORECARD.md:1956-1957`,
`LOG.md:1288-1294`, `SKILL.md:77-78`). The set's kill rule forbids editing/deleting checks
after the first counted run, but it explicitly permits *appending* checks — appending a
`grep_assert` on the SCORECARD round-34 row would close this gap and still keep K=0.

---

## 4. Receipts / artifacts

This seat's directory `.ufo/waves/round-34/w2a2/ExecC2Rerun/` (48 KB total, every file < 1 MiB):

| file | sha256 | what |
|---|---|---|
| `c2-rerun-s7311.json` | `32354e714887ef70a03d61eb58e22a16823219e5289717048f22dc84406bb8ea` | fresh-seed C2 receipt, 37/37 |
| `c2-rerun-s7417.json` | `80a8e4240246ae2d4de4a2e30647f2ab04f630fd6841751ecf27074cdddc0529` | fresh-seed C2 receipt, 37/37 |
| `c2-rerun-s7589.json` | `69b16640b28598fba7cd7580f6f64917badbfa190956323bf6639a93d6b02e5f` | third fresh seed, 37/37 |
| `c2-beforegate-s7311.json` | `f20f602cbec5273626a4e272e278dc39ecde5a48d6723dab3a557966ffb23c4d` | do-nothing control on `772a1d8e…`, 21/37 |
| `c2-beforegate-s7417.json` | `9fabc61e0bf4ee170d8d197e25a8a7f7ca6c2d306f5526399ce2ff660d3faffb` | do-nothing control, second seed, 21/37 |
| `c3-selfaudit-rerun.txt` | `b709781c949b5f63371783b93f3b99958f6b48b413a96899de1209646af06452` | self-audit output (identical to committed `audit-first-run.txt`) |
| `selftest-tip-clone.log` | `5311643cc95e6358a9fd513ec8ba67b944617e7d7da2f8df1c4d33d1f0c75c12` | `--selftest` at the tip clone: PASS (256 cases) |

Scratch (cited, not copied): `/fast/scratch/hyaku/chousa-r34-a2/w2/ExecC2Rerun/` — clone,
`gate-before.sh` (pre-fix blob), `gate-32766.sh`, `gate-mut-noconfirm.sh`, `junk-gate.sh`,
`audit-set-broken.json`, `disp.md`, `fixture-s7311/`, `tmp/`.

No writes outside my directory and the scratch dir; no git/jj write commands; no network; no
process signalled (only the shell's own children, all awaited).

---

## 5. Limits

- C1 was not re-scored (frozen exclusion, required controls held — I did not open it).
- The PCRE ceiling is this host's (PCRE2 10.49-1, man file sha256 `a3ea2c67…74bd6`); another
  build could bind a byte or two elsewhere. The lane's own §Limits note says the same.
- I did not re-run the full no-harm battery (`measure-a2/battery/`); I did re-run the gate
  selftest (PASS 256) and the five counters' host state was not touched.
- Timing numbers on this host are ~2× the committed ones (concurrent wave load); no behavioural
  difference was observed.
- §1c's mutant gates were scratch copies of the landed gate; the lane gate file was never
  modified.
