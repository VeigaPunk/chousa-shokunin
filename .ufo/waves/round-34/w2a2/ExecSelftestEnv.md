# ExecSelftestEnv — locale-dependence re-measure (round 34 attempt 2, wave 2a2)

Seat: read-only attack seat. Lane tip frozen at `707da8184a0fc4d10ab3f17271556cdf364f0af5`;
nothing in the lane, the lane jj/git state or the fleet repo was written by this seat (only
this report and this seat's own artifact directory). No network. No installs.

## 1. What was measured

Gate blobs pinned by SHA-256 before any run (never scored from the working tree):

| blob | source | sha256 |
|---|---|---|
| landed gate (tip) | `git show 707da818:tools/research-gate.sh` | `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` (= disclosed prefix `a6307edf687ac0fb`) |
| pre-C2 gate | `git show bf7c931a:tools/research-gate.sh` | `772a1d8e4d94dbf3a44a64bf850b1324e51546eeb62abcd7b3ec585f0e003e58` (= the lane's own "unfixed gate `772a1d8e`" named in claims-a2.md) |
| attempt-1 base gate | `git show a92b9f4:tools/research-gate.sh` | `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346` (the round-34 base named in `corpus/lessons/round-34.md`) |

Scratch root: `/fast/scratch/hyaku/chousa-r34-a2/w2/ExecSelftestEnv/` (`git clone -q` of the lane
repo, `checkout -q 707da818…`; `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset before every git
call). `TMPDIR` was pointed into the scratch dir for every run.

## 2. The headline answer

**Under `LC_ALL=C` the landed gate and the pre-C2 gate fail the SAME ten cases — the three new
dead-zone cases (254–256) do not fail under `LC_ALL=C`; they pass.** The landed/pre-C2 failure set
is byte-identical to the attempt-1 committed `landed-C.log` set, and the ten names are exactly the
attempt-1 disclosed family minus the eleventh name (`claims-lane-fallback`), which is a
**run-location artifact, not a locale effect** (proved in §5).

### Landed gate `a6307edf` @ `707da818`, in-tree clone, `LC_ALL=C`
```
LC_ALL=C TMPDIR=<scratch> bash clone/tools/research-gate.sh --selftest
→ exit=1 ; RESEARCH_GATE_SELFTEST: FAIL (10/256 cases)      [45.6 s]
```
Failing case names (10):
`claims-pass`, `all-pass.md` (×3 — three different fixture dirs), `all-structure.md`,
`claims-pass.jsonl`, `all-meta.md`, `all-dangling.md`, `json-unterminated-manifest`,
`json-nul-terminated-manifest`.

### Pre-C2 gate `772a1d8e` @ `bf7c931a`, in-tree clone, `LC_ALL=C`
```
cp pre-c2-gate.sh clone2/tools/research-gate.sh   # sha256 772a1d8e…3e58 verified
LC_ALL=C TMPDIR=<scratch> bash clone2/tools/research-gate.sh --selftest
→ exit=1 ; RESEARCH_GATE_SELFTEST: FAIL (10/253 cases)      [39.5 s]
```
Failing names: **identical 10** (`diff landed-C.names prec2-intree-C.names` → empty).
The three new dead-zone cases do not exist on this blob (253 cases), so "modulo the three new
dead-zone cases" is exactly the right qualifier: the C2 landing added **no** locale-dependent case.

### Comparison with the disclosed attempt-1 measurement
| measurement | disclosed (attempt 1) | this seat (re-measure) |
|---|---|---|
| base gate, `LC_ALL=C` | 11 cases FAIL (`measure/selftest-env/base-C.log`) | **10** in-tree; **11** reproduced exactly when the base blob runs with no `PROVINCE.md` beside it (§5) |
| landed gate `772a1d8e`, `LC_ALL=C` | 10 cases FAIL (`measure/selftest-env/landed-C.log`) | **10**, and the **name set is identical** to the committed log (`diff` empty) |
| landed gate `a6307edf`, `LC_ALL=C` | not measured in attempt 1 | **10/256**, same 10 names |
| default locale | passes | passes: `PASS (256 cases, 0 skipped)` landed, `PASS (253 cases)` pre-C2, `PASS (251 cases)` base |

So the disclosed pair (base 11 / landed 10) is **reproduced exactly** — the base's eleventh
failure is re-created by construction (§5) — and the landed gate's set is unchanged by the C2
landing. The one correction the disclosure deserves: the attempt-1 "base 11 vs landed 10" delta is
**not** a base-vs-landed gate difference. Both gates fail the same 10 in the same environment;
the eleventh case (`claims-lane-fallback`) appears whenever the gate blob sits beside a directory
tree without a readable `PROVINCE.md`, which is how the attempt-1 base run was staged. Reading the
committed `base-C.log` (lines 179–183) confirms it: the base run's own output shows
`CLAIM_SOURCE_MISSING … source=PROVINCE.md … not a readable regular file under allowed roots`,
i.e. the eleventh failure was a missing-file refusal, not a span-matching difference.

## 3. Which of the three new dead-zone cases fail under `LC_ALL=C`

**None.** From `landed-C.log` (the `LC_ALL=C` run of the landed gate):

```
346:ok-case  254 claims-deadzone        exit=1
347:ok-case  255 claims-deadzone-line   exit=1
348:ok-case  256 claims-deadzone-edge   exit=1
349:RESEARCH_GATE_SELFTEST: FAIL (10/256 cases)
```

All three are `ok-case` lines (their own expected exit is 1, and they produced it), i.e. they
PASS under `LC_ALL=C`. They also pass in the default locale (`landed-default.log` →
`PASS (256 cases, 0 skipped)`). The lane's own committed note
`.ufo/waves/round-34/measure-a2/selftest-lc-all-c-a2.txt` (committed at `707da818`) states the
same three names; this seat's independently produced set matches it name-for-name.

## 4. Root cause of the ten locale failures (one cause, not ten)

Every one of the ten failing blocks in `landed-C.log` carries the same finding — 10/10 blocks
contain `FINDING CLAIM_SPAN_NOT_FOUND … obs=id=P4`:
```
grep -c 'obs=id=P4' landed-C.log   → 10
```
`P4` is the case-21 claim whose span is the JSON escape `\u2192`:
`tools/research-gate.sh:4045` `{"id":"P4","source":"claimsrc/arrow.md","span":"arrow check \u2192 done",…}`
against the raw UTF-8 fixture `tools/research-gate.sh:4031`
`printf 'arrow check \xe2\x86\x92 done\n' >"$WORK/claimsrc/arrow.md"`.
`json_unescape` (`tools/research-gate.sh:1329`) decodes `\uXXXX` with
`printf -v c '%b' "\u$hex"`; bash's `%b` honours `\u` only in a UTF-8 locale. Measured directly:

```
LC_ALL=C        bash -c 'printf -v c "%b" "\u2192"; printf %s "$c" | od -An -tx1'  → 5c 75 32 31 39 32  (literal "\u2192")
LC_ALL=en_US.UTF-8 bash -c '…same…'                                                    → e2 86 92          (the arrow)
```

Under `LC_ALL=C` the decoded span is the 6 ASCII bytes `\u2192`, which is not in the source file,
so `P4` reads `observed=unsupported`; every downstream case that asserts `VERDICT_BEARING_CLAIMS=4/4`
or `RESEARCH_GATE: CLEAN` on that fixture then fails (`claims-pass`, `all-pass.md` ×3,
`all-structure.md`, `claims-pass.jsonl`, `all-meta.md`, `all-dangling.md`), and the two
`r24_case` manifest cases fail on `rc=1/0` because the `verify-all` run drifts on `P4`
(`tools/research-gate.sh:6341-6342`). **One locale-sensitive byte-decode decision, ten visible
case failures.** The lane already records the general family
(`corpus/knowledge/anchor-boundaries-r4.md:163`; `corpus/lessons/round-34.md`) but not this
specific `\uXXXX` decode line, which is the sharpest available lever if the family is ever to be
closed. [INFERENCE] — I did not patch the gate (out of scope: read-only wave).

## 5. The "base 11" number, isolated

Same base blob `43a1af35`, same `LC_ALL=C`, three staged locations:

| staging | result |
|---|---|
| in-tree clone (`clone3/`, `PROVINCE.md` present, corpus present) | `FAIL (10/251 cases)` — same 10 names |
| extracted to scratch **with** `corpus` symlink, **without** `PROVINCE.md` | `FAIL (11/251 cases)` — 10 names **+ `claims-lane-fallback`** |
| extracted to scratch with `PROVINCE.md` copied in | `FAIL (10/251 cases)` — same 10 names |

The 11-name set is byte-identical to the committed attempt-1 `base-C.log` set
(`diff repro-base.names a1-base-C.names` → empty). Control on the same staging, landed gate
`a6307edf`: with a `PROVINCE.md` **symlink** beside it the landed gate also shows 11
(`FAIL (11/256 cases)`) and in the **default locale** the same staging shows `FAIL (1/256 cases)`
with `claims-lane-fallback` as the only failure — i.e. that eleventh case tracks the presence of a
real `PROVINCE.md` in the gate's own directory, not the locale and not the gate version.

`claims-lane-fallback` is the case that pins `PROVINCE.md` line 3 (`tools/research-gate.sh:5849`,
`5874`); the gate resolves `LANE_ROOT` as the parent of its own script dir
(`tools/research-gate.sh:313`), so a blob staged outside the lane tree cannot see it.

## 6. Scratch-location trap (recorded because it changes numbers)

Running the extracted blobs from a bare scratch dir (no `corpus`, no `PROVINCE.md`) gives
**20** failures for **all three** blobs — landed, pre-C2 and base all fail the *same* 20 names
(`diff` empty between the three sets):
`chain-exempt-unresolvable`, `chain-fail-counting`, `chain-fail-out-of-corpus`,
`claims-fail-out-of-corpus`, `claims-root-slash-xdev`, `ptr-symlink`, `ptr-traversal`,
`sweeps-symlink-dir`, `sweeps-symlink-escape`, `claims-lane-fallback` — on top of the 10 above.
This is the "scratch-location fails" effect named in the lane's own commit `707da818`
("the old gate has 253 cases and scratch-location fails"). **Consequence for re-derivation:** the
number 10/11 is a property of the *staging*, not of the gate blob. Any re-derivation must place the
gate inside a tree carrying `PROVINCE.md` and `corpus/`, otherwise it measures the fixture, not the
gate. [INFERENCE, from the three controlled stagings above.]

## 7. Adjacent checks I ran while in the neighbourhood (reported for completeness)

- `sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` →
  `a6307edf687ac0fb…562995b` — the working-tree file equals the committed blob at `707da818`.
- The four committed C2 receipts `.ufo/waves/round-34/measure-a2/c2-after-s{5011,5023,5033,5047}.json`
  each carry `label=DEADZONE_MATCH=37/37`, `predicate_holds=true`, `gate_sha256=a6307edf687ac0fb…`,
  `counter_sha256=8c0def4d377cdf1a…` — the after-measurements bind the pinned gate and a single
  counter digest. (Read-only inspection; I did not re-run the counter — a sibling seat owns that.)
- `python3 corpus/evidence/round34/self-audit.py` on the lane tip prints
  `SELF_AUDIT_MISMATCHES=0` / `SELF_AUDIT_UNDISPOSITIONED=0` — reproduced, exit 0.

## 8. Verdict for this item

**Confirmed.** Under `LC_ALL=C` the landed gate `a6307edf` (tip `707da818`) fails **10** cases and
the pre-C2 gate `772a1d8e` (tip `bf7c931a`) fails **10** cases, with **identical** failing-case
sets (`claims-pass`, `all-pass.md`×3, `all-structure.md`, `claims-pass.jsonl`, `all-meta.md`,
`all-dangling.md`, `json-unterminated-manifest`, `json-nul-terminated-manifest`). The landed set
is also identical to the attempt-1 committed `landed-C.log` set. **None of the three new
dead-zone cases (254 `claims-deadzone`, 255 `claims-deadzone-line`, 256 `claims-deadzone-edge`)
fails under `LC_ALL=C`** — all three pass; the C2 landing is locale-clean for its new cases. The
attempt-1 disclosed pair (base 11 / landed 10) is reproduced exactly, with the correction that the
base's eleventh case (`claims-lane-fallback`) is a staging artifact (missing `PROVINCE.md` beside
the extracted blob) and not a base-vs-landed gate difference; under a matched staging both gates
fail the same 10. Default-locale selftest passes on all three blobs (256 / 253 / 251 cases).

## 9. Limits

- The three new dead-zone cases were exercised only through the gate's own `--selftest`; I did not
  re-run `c2-count.py` (a sibling seat owns the counter re-derivation).
- The locale root cause in §4 is a mechanism reading of the gate source plus two one-line bash
  probes; I did not patch the gate or produce a fix (read-only wave, out of scope).
- The 10/11/20 staging numbers are single runs each (the selftest is deterministic: three
  independent stagings of the same blob produced the same sets).
- Every artifact I produced is under 1 MiB; the raw logs live in the scratch dir and are copied
  (not symlinked) into my own directory.

## 10. Artifacts (my directory only)

`/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-34/w2a2/ExecSelftestEnv/` —
`landed-C.log` (sha256 `da4813cc6c1752f7…`), `prec2-intree-C.log` (`9639154c4865682f…`),
`base-intree-C.log` (`712a2c70354eb3a3…`), `prec2-C.log` (`8e0f740e18affce7…`),
`landed-scratch-C.log` (`e1ea297896e0ab3b…`), `repro-base-C.log` (`81eab8961356ff44…`),
`repro2-base-C.log` (`efde9502ca14a4e2…`), `repro2-landed-C.log` (`ff1a0b62b2f8e56d…`),
default-locale logs (`landed-default.log` `5311643cc95e6358…`, `prec2-intree-default.log`
`550bfea86bb2632b…`, `base-intree-default.log` `acf0564af458e7a2…`), the failing-name sets
(`*.names`, `failing-sets.txt`) and `SHA256SUMS.txt` over all of them.
Scratch originals (full runs): `/fast/scratch/hyaku/chousa-r34-a2/w2/ExecSelftestEnv/`.

No writes outside this directory and this report; no git/jj write commands were issued in the lane
or the fleet.
