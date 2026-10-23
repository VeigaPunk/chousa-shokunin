# ReviewKnowledge32 — knowledge entries vs QUALITY.md (round 32, falsify wave 2)

Scope: `corpus/knowledge/manifest-append-lock-r32.md` and `corpus/knowledge/exempt-hop-audit-r32.md`
against `corpus/QUALITY.md` (criteria 1–35). Checked against gate `10f2fe12…`, counters
`e6bf9531…` / `8ec1a1ed…` (sha256 verified, receipts match), `claims.md` §C1/§C2 design v2,
receipts under `.ufo/waves/round-32/measure/` and `w1/`, SOURCES.md S060/S061, and the gate code.

Verdict: **HOLDS with defects** — no false factual claim and no missing counter claim found;
three low-severity quality defects below (one unmarked inference, one wrong-anchor number, one
unscoped-source adjective). C2 file: no findings.

## Findings (severity, then line)

1. **Low — unmarked inference, mechanism stated as cause** — `manifest-append-lock-r32.md:38-40`:
   "because its append lands microseconds after the unlock while the next writer's probe takes
   milliseconds." No measured anchor: `grep -n 'micro\|milli\|delay'` over
   `.ufo/waves/round-32/w1/CtlC1PartialLockB.md` and `CtlC1PartialLockB/` hits only the frozen
   300,000 µs delay string, no probe/append timing figures. The sentence repeats
   `claims.md:132-133` (frozen contract), but a contract assertion is not a measured anchor —
   QUALITY 2/3. Mark [INFERENCE] or cite a timing receipt.
2. **Low — number with the wrong anchor** — `manifest-append-lock-r32.md:13`: "round 25 saw it in
   2 of 6 seeded runs" is parenthesised to `json-delimiter-r24.md:66-71`, which records **one**
   blank line in **3** runs at 16 writers ("16 parallel appenders × 3 runs … one run wrote one
   blank line", `json-delimiter-r24.md:66-70`). The 2/6 evidence lives elsewhere
   (`corpus/lessons/round-25.md:20`, `LOG.md:866`, `.ufo/waves/round-25/build/ExecAppendRace.md`).
   Number is right, anchor misleads — QUALITY 2/9.
3. **Low — unscoped-source adjective** — `manifest-append-lock-r32.md:44`: "flock(2) locks are
   advisory." The only in-file flock source S060 excludes "flock(2) lock lifetime, advisory
   semantics or NFS behaviour" from its scope (`SOURCES.md:70`), so under QUALITY 7 this is an
   unlabelled inference (consistent with, but not anchored by, the contract's "cooperating
   writer" framing `claims.md:26-27` and gate comment `research-gate.sh:3284`).

## Verified (no overclaim)

- manifest-append L10-15 defect: probe/append race matches `json-delimiter-r24.md:66-70` and
  claims.md:16-21. L18-22 fix: `exec {jfd}>>` + `flock -x "$jfd"` + `tail -c1` probe + printf
  append + `exec {jfd}>&-` all inside the lock at `research-gate.sh:3292-3310`; flock(1) absent →
  exit 2 at `:3287-3289`; inode/bytes preserved (`>>`, never truncated).
- L26-30 PATH.lock rationale correctly tagged [INFERENCE]. L34-40 counter description matches
  `c1-count-v2.py` docstring (24 trials, W_L=8, W_F=16, 300 ms strace write delay, exit-2
  self-check). "24/24 control → 0/24" matches `controls/L1-design-v2/c1-probeonly-s3201.json`
  (`APPEND_SERIALIZED=0/24`) and `CtlC1PartialLockB/b-s3247102{1,2}.json` (24/24, v1).
- L47-51 counter-blindness limit honest: oracle B (lock on a separate open of PATH) scored 24/24
  under v2 (`OracleC1B/v2-rescore.md`, `v2/B-s401{1,2}.json`).
- exempt-hop L10-14: base gate exempt arm covered
  `unresolved|blocked-no-fetch|rejected|labelled-dead|not-applicable` with no read (base
  `7a7259f0` gate header `:164`); "exemption is record-declared and unverifiable" verbatim at
  `corpus/README.md:360` (Frontier, Round 3 paragraph).
- L16-19 S061 reading inside the row's stated scope (`SOURCES.md:71`). L23-30 audit description
  matches gate: `emit_finding CHAIN_EXEMPT_RESOLVABLE warn …` hardwired warn at `:1953`, U arm
  `:1943-1959`, `rejected|not-applicable` unread at `:1961-1964`, `resolvable=%d` last field of
  the `RESEARCH_GATE:` summary at `:1987`, record drifts via emit_finding warn → ROLL=DRIFT
  (`:447`) → exit 1.
- L37 [INFERENCE] present. L41-47 counts exact: CLASS_COUNTS `c2-count-v2.py:79-95` = 36
  resolvable U + 12 resolved + 12 judged + 72 exempt, 16 classes, TOTAL 132; exemplars map
  E8 `glued` (`x`+anchor), E9 `plain_heading`, E10 `partial_line`, E11 `case`, E12 `spaced`.
  Record checks (one `RESEARCH_GATE: DRIFT`, exit 1, dedup, unknown hop) per docstring and
  `after-c2-s32011/32012.json` (`record_fails=[]`, `gate_rc=1`, 132/132).
- L53 "none flips" = scout verdict, `.ufo/waves/round-32/w1/ScoutExemptCorpus32.md:3`.
- Headers satisfy QUALITY 6/13 (source/verified-at/recheck, cwd stated, no bare `--root ..`);
  S060/S061 status `mined`, `used-by` names the entries (`SOURCES.md:70-71`);
  `prose-check.py` on both files: `TOTAL hits=0`, exit 0 (criterion 23).
- Receipts: `measure/after-c1-s32001/32002.json` both `APPEND_SERIALIZED=24/24
  predicate_holds=true`; `after-c2-s32011/32012.json` both `EXEMPT_AUDIT_MATCH=132/132`; all four
  name gate `10f2fe12…` and counters `e6bf9531…`/`8ec1a1ed…` = working-tree sha256. W2 sibling
  receipts on the landed gate (CriticC2Contract 2×, MutC2Gate pristine) also 132/132 — no lower
  run found.

## Adjacent observation (outside target files, not counted)

`c2-count-v2.py` docstring says the record "holds 120 hops" while TOTAL=132 — stale v1 line in
the counter, not in either knowledge entry.

No installs made; all commands read-only, `timeout`-bounded shell greps/python sha256.
