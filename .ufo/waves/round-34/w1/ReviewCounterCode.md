# Round 34 W1 — ReviewCounterCode: line-by-line review of `corpus/evidence/round34/c1-count.py` (pre-data)

Seat: ReviewCounterCode (UFO-FSD reviewer, leaf). Date: 2026-10-23.
Scope: the counter as committed at `70feb5eacc959eb98071461fe89f0b892c0810d8` (sha-256
`5ef347874960b52561a1cfa517f3f3fc0d1763830e3580c44b993f8394c0a565`, matches claims.md).
Gate under test: base round-33 gate (sha-256 `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`, matches claims.md).

## Verdict
The counter is **correct and consistent with the frozen P1 predicate** as a measurement instrument:
its fixture truths, class counts, boundary math, regexes, scoring, and receipt fields all check out.
No defect found that would flip a score on the landed gate or on an honest fix. Findings below are
documentation-precision and robustness notes; none change a count. The counter's reported base-gate
score was reproduced end-to-end at 19/30 (see §4), matching the claims.md "Before" ceiling.

---

## 1. Findings by severity

### F1 (medium, documentation/mechanism precision) — the claimed E2BIG onset is exact at 32768, but the actually-broken band begins 3 bytes earlier (32765) via PCRE2, not exec
Evidence (commands run on this host, 2026-10-23):
- Kernel single-argument limit: `subprocess.run(["/bin/true", "a"*n])` → max OK `n=131071`, first failing `n=131072`.
  → the docstring/claims figure "131072-byte single-string limit" and "span of 32768 bytes or more" (4·32768 = 131072) are exactly right for exec(2) `MAX_ARG_STRLEN`.
- Exact gate argv shape (`grep -a -z -b -o -P -- "$regex"`, stdin haystack):
  - span 32764 → rc 0 (match)
  - span 32765, 32766, 32767 → grep rc 2, stderr `/usr/bin/grep: regular expression is too large` (exec succeeded; PCRE2 compiled-pattern size limit)
  - span 32768, 32769 → exec fails `OSError: [Errno 7] Argument list too long` (E2BIG)
- So the observable failure onset for the gate is span 32765, three bytes below the claimed 32768.
- Impact: no counter record lives in 32765–32767 (long-edge floor = 32768), so no truth or count changes.
  The claim's *mechanism* sentence is precise for its stated band; the "broken zone" is 3 bytes wider than stated. Claims.md's own source note (pcre2limits(3)) actually anticipates this.

### F2 (medium, satisfiability evidence) — the obvious "-P -f" fix is closed inside the claimed band; the fixture's band is satisfiable only via a non-PCRE path
- `grep -a -z -b -o -P -f patfile` (pattern = `\xHH` literal of a 32768-byte span) → rc 2
  `/usr/bin/grep: regular expression is too large`; same at 65000.
- `grep -a -z -b -o -F -f patfile` (fixed string) matches a 65000-byte span (rc 0, occurrence found).
- Conclusion: P1 (30/30) is achievable by an honest fix; the counter does not demand the impossible.
  This also validates claims.md's pcre2limits(3) warning.

### F3 (low, robustness) — relative `C1_TMP`/`TMPDIR` handling
- Missing relative dir (e.g. `C1_TMP=reltmp` without `./reltmp`): `tempfile.mkdtemp` raises → counter prints
  `c1-count: temp dir: [Errno 2] No such file or directory: 'reltmp/chousa-r34-c1-…'` and exits 2 (loud, fine).
- Existing relative dir: fixture root and claims path become relative; subprocess `cwd=root` applies them
  in the child, so the gate receives a claims path it cannot find. A direct replica of the counter's exact
  call (same env minus CHOUSA_*, same `cwd`, same relative args) exits **rc=2 in 0.1 s** with
  `research-gate: claims file not found: reltmp/…/claims.jsonl` + usage. The counter then scores every record
  "none" and prints `0/30` (false miss, not false pass).
- Note: a full run of the counter under the existing-relative configuration did not terminate within 300 s
  in my probe (observed, exit 124 by my timeout; no receipt written) — I could not reproduce that hang with
  the direct replica; environment/contention suspected, unproven. Mitigation is already in the lane contract
  (absolute scratch dirs). Report as robustness note, not a scoring defect.

### F4 (low, coverage note) — untested bands are wider than the claim's wording suggests
- The fixture tests 64–4106 bytes (short classes; overshoot ≤ 10 bytes) and ≥ 32768 bytes (long classes).
  The 4097–32767 band is untested, and on this host the actually-broken band begins at 32765 — so a fix
  that fails only for spans 32765–32767 would pass 30/30. This is exactly the "not claimed" zone, so it is
  a residual risk, not a counter bug. A v2 could add a record just above the true observed onset.
- The `-`/`'` joiner rule is never exercised (vocabulary is `[a-z]` with separators space/newline only).
  The fixture cannot therefore be tripped by the joiner; it also cannot detect a gate regression in the
  joiner rule. Same classification: coverage note.

### F5 (low, doc nit) — class band overshoot
- `Gen.text` can overshoot its target by up to one word + separator (≤ 10 bytes). So "short 64..4096" can
  produce 4097–4106; "long 33000..65000" up to 65010. Long-edge is clamped to ≤ 32900 by its loop and the
  overshoot bound (max 32898 < 32900). No functional impact; observed lengths verified within bands.

---

## 2. Checks that passed (with evidence)

### 2.1 Frozen predicate identity
- P1 sentence (claims.md): two fresh-seed runs print `LONGSPAN_MATCH=30/30`, receipt `predicate_holds=true`,
  no committed lower run. Docstring: "Code condition: holds = matched == TOTAL (TOTAL = 30)".
- Code: `holds = matched == TOTAL`; `label = "LONGSPAN_MATCH=%d/%d"`; receipt `predicate_holds: holds`;
  exit `0 if holds else 1`. Identical predicate. `TOTAL = 30` asserted at import (verified `TOTAL=30`).

### 2.2 Class arithmetic vs claims.md
- `CLASS_COUNTS` sums: total 30, long 24, short 6, long-unsupported 13 (2+2+3+2+2+2).
- claims.md "Before" ceiling 19 = 6 short + 13 long-unsupported. Verified by script and by the live run (§4).

### 2.3 Fixture generation correctness vs gate boundary rules (structural audit, seed 78 fixture)
- Independent re-derivation of verdicts from the generated files (delimited-occurrence semantics using the
  gate's TOK_WS/TOK_PUNCT membership, all occurrences enumerated, line bind = exact range match):
  supported 12, unsupported 16, mislocated 2 — exactly `CLASS_COUNTS` truth (9+3, 13+3, 2).
- Determinism: `C.generate(root, 78)` twice → byte-identical file hashes and truth maps.
- Spot-checks from `keep-s3451` (seed 3451): long-edge id `cadd851fd9c` span 32824 (band ✓), present
  verbatim in source, truth supported; long-line-wrong `c0cc7bf684b` span 55813, line 14-547, truth
  mislocated; long-line-bound `cc0ed434644` span 47810, line 507-993, truth supported.

### 2.4 Boundary/token rules used by the fixture
- Separators are `" "`/`"\n"` → always in TOK_WS; spans always start/end with a letter; so verbatim
  occurrences at separator/EOF junctions are always delimited; the deliberately glued classes put a letter
  adjacent on the relevant side (left/right) — matching the gate's `tok_left_ok`/`tok_right_ok` rule
  (letter is neither TOK_WS nor TOK_PUNCT). No separator/vocabulary choice can flip a verdict.
- `long-split` removes the separator at a split point and inserts a 300–2000-byte filler between halves, so
  the full span never occurs. Mutation classes change one letter, so the record span never occurs.

### 2.5 Line-range arithmetic
- `line_range(text, off, span)`: `l1 = text.count("\n",0,off)+1`, `l2 = l1 + span.count("\n")`.
- Gate `count_nl` = `tr -dc '\n' | wc -c`; `TOK_L1 = count_nl(before)+1`, `TOK_L2 = TOK_L1 + count_nl(span)`. Identical semantics (both count bytes/`\n`).
- `long-line-bound` names the second occurrence; `long-line-wrong` names `a1+1`, which can never equal a1
  (differs in both entries) or a2 (requires `span_nl + mid_nl == 1`; mid has ≥ 2 newlines and span has ≥ 1,
  so ≥ 3). The `assert wrong not in (a1, a2)` is trivially safe. Gate M>N validation is satisfied (multiline spans).

### 2.6 Regex fidelity vs printed gate formats (8/8, replayed with importlib)
- `LINE_RE` `^CLAIM id=(\S+) expected=\S+ observed=(\S+) ` vs `CLAIM id=$id expected=$expect observed=$observed source=$src at=$at verdict=$verdict` (research-gate.sh:1888). Groups verified on supported/unsupported/mislocated/invalid/refused flavors.
- `FIND_LINE_RE` `^FINDING CLAIM_LINE_MISMATCH .*\bobs=id=(\S+)` vs `FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=…` (emit_finding, :448-451; CLAIM_LINE_MISMATCH emission at :1862). Matches, id captured.
- Header/DRIFT/VERDICT lines don't collide with either regex; `RESEARCH_GATE: DRIFT` prefix matches the `startswith` check.

### 2.7 Scoring, rc/DRIFT filter, duplicates, receipt
- Parse gated on `not timed_out and rc == 1 and drift`; gate returns 1 on DRIFT, 0 on CLEAN, 2 on usage; fixture always contains mismatches → DRIFT at a correct gate. Correct.
- Duplicate id (two CLAIM lines) → `"none"`. Unknown ids ignored (`in truth` guard). Missing records → `"none"`.
- `ok = obs == t and ((cid in f_line) == (t == "mislocated"))` — exactly the docstring rule; "+finding-set" annotation when obs matches but finding-set is wrong.
- Receipt fields: schema, counter_sha256 (sha of `__file__` — equals the committed hash), gate, gate_sha256, seed, utc, elapsed_s, gate_rc, gate_timed_out, gate_stderr_tail (last 2000 chars), total, matched, label, predicate_holds, per_class, misses. All present and truthful; `gate` stores the argument string, `gate_sha256` the bytes.

### 2.8 Source-cap / record-validation fit
- `SOURCE_READ_MAX_BYTES = 8 MiB` (:308) — largest generated file ≈ 139 KB (two 65 KB spans + fillers), safe.
- Record validation (:1684-1743) accepts the fixture shapes: nonempty id/source/span/expect, optional string `line` matching `^[1-9][0-9]*(-[1-9][0-9]*)?$` with M>N, no marker/sha256/escaped-NUL keys. No invalid records.
- `--root` is a global flag (:7775); `verify-claims` dispatch confirmed (:7760).

---

## 3. Empirical base-gate run (seed 3451, receipt in my dir)
Command (run from lane root, gate copied to scratch; C1_TMP/TMPDIR = my scratch; GIT_* unset):
```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE C1_TMP=/fast/scratch/hyaku/chousa-r34/w1/ReviewCounterCode TMPDIR=$S \
  timeout 1800 python3 corpus/evidence/round34/c1-count.py \
  --gate /fast/scratch/hyaku/chousa-r34/w1/ReviewCounterCode/gate-copy.sh \
  --seed 3451 --receipt .ufo/waves/round-34/w1/ReviewCounterCode/base-s3451.json \
  --keep /fast/scratch/hyaku/chousa-r34/w1/ReviewCounterCode/keep-s3451
```
PID 2653670 (recorded; no other processes from this seat left).
Result (`base-s3451.json`):
- `label = "LONGSPAN_MATCH=19/30"`, `predicate_holds=false`, `gate_rc=1`, `gate_timed_out=false`, `elapsed_s=1140.537`.
- Per-class misses exactly: long-verbatim-ml 0/3, long-verbatim-1l 0/2, long-edge 0/2, long-line-bound 0/2, long-line-wrong 0/2 — i.e., the 9 long-supported and 2 mislocated; all 13 long-unsupported + 6 short match. Matches the claims.md "Before" ceiling.
- stderr tail (copied from the receipt I opened, ≤25 words): "line 1553: /usr/bin/grep: Argument list too long" — the base failure mode as claimed (grep exec E2BIG).

## 4. Residual risks / verification gaps
1. The 4097–32767-byte band is untested; on this host the broken band starts at 32765, so a fix that leaves 32765–32767 broken still scores 30/30 (F1/F4).
2. Relative `C1_TMP` can produce a silent false miss (gate rc=2 → all "none") if the dir exists; contract already mandates absolute scratch dirs (F3).
3. `text=True` decoding: the gate prints an em-dash in its header; under an ASCII-only locale (no PEP-538 coercion) this could raise `UnicodeDecodeError` before scoring. Not observed here (`en_US.UTF-8`); [INFERENCE].
4. The 300 s non-termination of the existing-relative probe run remains unexplained (direct replica dies in 0.1 s); not reproduced since; attributed to host contention in that window. Low.
5. `--keep` writes `truth.json` next to a copy of the claims file (post-run, audit-only), which reads slightly against the docstring's "truth never written beside the claims" — the gate never sees it; observation only.

## 5. What I ran / opened (honesty record)
- Opened: claims.md; c1-count.py (342 lines); research-gate.sh lines 1469-1548, 1684-1743, 1739-1908, 448-451, 307-311, 1368-1373, 7759-7777.
- Ran: sha256sum (both files + gate copy, match claims.md); git rev-parse HEAD → 70feb5e; kernel single-arg limit probe (/bin/true, 131071/131072); grep -P argv probes (32764-32769 spans, exact gate shape); `-P -f` vs `-F -f` probes (32768/65000); regex replay (8/8); structural truth audit (seed 78) + determinism; base-gate counter run seed 3451 (receipt above); relative-C1_TMP probes (direct replica + two counter invocations).

Artifacts (all in my seat dir only): `base-s3451.json`, `run-s3451.log`, probe outputs under scratch (`/fast/scratch/hyaku/chousa-r34/w1/ReviewCounterCode/`), gate copy (sha `43a1af35ca668fe5…`). No repo files modified; no git/jj writes.
