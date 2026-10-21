# Chousa round-27 residual seat — change (b): `metadata_registry_check_source` S-id token prefilter

**VERDICT: HOLDS (conditional)** — semantic equivalence with dd72641e and "no cost regression" are
confirmed on every input exercised (1,006 source values, byte-identical FINDING/META/verdict lines; cb ≤ dd
on every token-bearing shape, +0.05–0.15 ms/entry on the id-free many-entry shape). But **F1 is a
landed-gate counterexample**: cb is *not* equivalent to dd72641e when the prefilter's own grep faults — cb
flips **DRIFT/exit 1 → CLEAN/exit 0** and asserts "source has no S-id". Equivalence holds only for a working
grep; F1 must be fixed before (b) is admitted. Author-lane advice only; no admission decision is made here.

Target `cb895a2bdd259eb38bec29ef70011d8211a508b5` (gate sha256 `a6bc2855…82386`), compared with
`dd72641e574679c4f7882dd43de072b4c8892d6f` (gate `ca39d14d…92f84`) and round base
`64eec5d41c7cf7f17f5ce1e968e28b3769952596` (gate `c2c813f1…3abc6`); sandbox (read-only w.r.t. the lane)
`/tmp/chousa-r27-residual-ResTokenPrefilter/{base,dd,cb}` git archives + `…/work/`. Tools: bash 5.3.20,
GNU grep 3.12-modified (`/usr/bin/grep`), `man 1p grep`, python 3.14.8 — **nothing installed or upgraded**.

## F1 — [landed-gate counterexample, high] prefilter fails OPEN on a matcher fault → false CLEAN

**Attacks:** the equivalence claim of (b) and the fail-closed discipline change (d) applied to the sibling matcher (`metadata_asof_usage_accepts`). `cb/tools/research-gate.sh:2532-2533`:

```bash
done < <(printf '%s\n' "$source_value" | LC_ALL=C grep -oE '[[:alnum:]_]+' \
  | LC_ALL=C grep -xE 'S[0-9]{3,}' || true)
```

`|| true` swallows **every** non-zero pipeline status. `grep -x` is the only new grep capability the gate takes
on — `grep -c -- 'grep[^|]*-x'` = **base 0 / dd 0 / cb 1**. When that invocation faults (usage → exit 2, internal
→ exit 3, signal) the token stream is empty, `found_id` stays 0, and the gate emits `META_SOURCE_NO_ROW_ID
severity=info` — a **false statement about the artifact** ("the entry cites no id") — and, because the default
severity policy is `STRICT=${CHOUSA_STRICT:-0}` (`cb/tools/research-gate.sh:287`; `info` does not drift), the run
ends **CLEAN with exit 0**.

Counterexample — same fixture, same input (`entry` = `source: S002`), only PATH differs:
`PATH="$STUB:$PATH" bash <rev>/tools/research-gate.sh verify-metadata $ROOT/corpus/knowledge/t.md --root $ROOT --registry $REG`
(stub `work/stubbin/grep` forwards to `/usr/bin/grep` but exits 2 with `grep: unrecognized option '-x'` when `-x` is present — any grep that faults on that option; the lane demonstrably puts stub greps on PATH).

| rev | grep on PATH | exit | verdict | FINDING |
|---|---|---|---|---|
| dd | real GNU grep | 1 | `RESEARCH_GATE: DRIFT (entries=1 complete=1 findings=1 drift=1)` | `META_SOURCE_NOT_MINED severity=warn … source_id=S002 registry row is not mined` |
| dd | stub (exit 2 on `-x`) | 1 | `DRIFT (… drift=1)` | `META_SOURCE_NOT_MINED severity=warn …` |
| cb | real GNU grep | 1 | `DRIFT (… drift=1)` | `META_SOURCE_NOT_MINED severity=warn …` |
| cb | **stub (exit 2 on `-x`)** | **0** | **`RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=1 drift=0)`** | `META_SOURCE_NO_ROW_ID severity=info … source has no S-id` |

**Honest counterweight, two parts.** (i) `dd` is *also* fail-open — its single `grep -oE` is masked by
the same `|| true`, so a fully broken grep degrades `dd` to the same false "no S-id"/CLEAN; what (b)
adds is a **second, independent fault-masked process** in the id-extraction chain, so the points at
which the whole id set can be silently erased go 1 → 2, and the new one (`-x`) is a different
invocation with its own failure modes. Under `CHOUSA_STRICT=1` cb still ends DRIFT but for the wrong
reason (`info` "source has no S-id" instead of `warn` "registry row is not mined"). (ii) Portability is
**not** the issue (`man 1p grep`): `-x` *is* POSIX-mandated, whereas `-o` — already required by `dd` — is
**not** ("only-matching" absent). So (b) adds no new portability requirement, only fault-tolerance debt.

**Recommended author-lane fix (advice, not applied):** make the prefilter fail closed the way change (d)
did for the as-of usage matcher — capture the pipeline status, treat `>1` as a hard fault, then iterate the
post-prefilter stream (which holds only ids, so it stays small):

```bash
local scan_out='' scan_rc=0
scan_out=$(printf '%s\n' "$source_value" | LC_ALL=C grep -oE '[[:alnum:]_]+' \
           | LC_ALL=C grep -xE 'S[0-9]{3,}') || scan_rc=$?
(( scan_rc > 1 )) && die_usage "metadata registry source scan failed (grep exit $scan_rc)"
```

A capability probe mirroring the gate's existing `token_matcher_require()` (`cb/tools/research-gate.sh:
1324-1329`) is the alternative — it is called **only** from `verify_claims` (1337) and `verify_chain` (1647);
the metadata path never probes grep.

## F2 — [coverage weakness] the falsify-controls suite owns a faulty grep but never routes it through the registry path

`corpus/evidence/round27-falsify-controls.py:78-80` builds `faulty-bin/grep` (`exit 2`) and uses it
**only** for the C1 usage-matcher control `'matcher-fault-fails-closed'` (the change-(d) fix). The C3 block
(lines ~140-180) runs `verify-metadata --registry` ten times but never with a faulty grep — the exact fault
class F1 needs is covered for one matcher and uncovered for the other. The existing stub (`exit 2` for
*everything*) is **not** discriminating — with it `dd` and `cb` degrade identically. The discriminating control
must honour `-o`, fail **only** on `-x`, and assert a non-clean verdict / `crit` finding, not
`META_SOURCE_NO_ROW_ID`.

## Equivalence evidence (assigned claim)

Harnesses `work/compare_tokens.py`, `work/extra_cases.py`, `work/fuzz_tokens.py`: each case writes a
synthetic `source:` value into `corpus/knowledge/t.md` under a real root, runs
`verify-metadata <entry> --root <root> --registry <registry>` end to end on base/dd/cb, and compares
**FINDING lines, META lines, verdict line and exit code** byte-for-byte (the `ts=` header is excluded).
Registry rows cover every branch: `S001` mined+used-by (clean), `S000`, `S0001`, 20-digit id mined, `S002`
queued (NOT_MINED), `S003` mined with foreign used-by (USEDBY_MISSING), `S999` absent.

| corpus | count | dd vs cb | base vs dd | base vs cb |
|---|---|---|---|---|
| curated (glued ids, `_`, digits 3–20, `S000`, lowercase `s`, CR, tabs, control bytes, non-ASCII letters adjacent to ids, duplicates, empty/whitespace, multi-line/fence/heading shapes, long tokens) | 96 | **0 diffs** | 0 diffs | 0 diffs |
| + hostile bytes (invalid UTF-8, fullwidth/Arabic/superscript digits, BOM, zero-width, NBSP), `LC_ALL=en_US.UTF-8` exported | 106 | **0 diffs** | — | — |
| randomized differential fuzz, seed 20261021 | 500 | **0 diffs** | — | — |
| randomized differential fuzz, seed 777 | 400 | **0 diffs** | — | — |

**1,006 source values, 0 divergences.** Decisive samples (identical on dd and cb): `glued-S001S002`,
`uscore-S_001`/`S001_`/`_S001_`, `lower-s001`, `empty` → `source has no S-id`; `glued-S0012` →
`source_id=S0012 registry row missing`; `digits-3`/`s000`/`cr-trailing`/`utf8-e-after`/`dup-S001x3` → clean;
`digits-20` → `source_id=S00000000000000000001 registry row missing`; `ctrl-nul-word` → `reason=nul unparsed`;
`dup-S002x2` → two `registry row is not mined` findings. Direct probe of the only plausible matcher
divergence (`bash [[ =~ ^S[0-9]{3,}$ ]]` vs `grep -xE 'S[0-9]{3,}'`): `work/probe_long.sh`, subjects of
1e3…2e6 digits — **AGREE at every length** (no glibc `REG_ESPACE` divergence). `grep -oE '[[:alnum:]_]+'`
under `LC_ALL=C` is byte-identical between GNU grep 3.12 and the harness's `pi-uu-grep 0.2.0` (the gate
subprocess resolves `/usr/bin/grep`; pi-uu-grep is only the agent shell's builtin), and pi-uu-grep's `-x -E`
agrees on `S001/S0001/S000` and rejects `s001/S01/S001_/S12`. Gate self-test in the sandbox (never in the
lane; UTF-8 locale inherited, no exported `LC_ALL=C`): `bash cb/tools/research-gate.sh --selftest` → exit 0,
`RESEARCH_GATE_SELFTEST: PASS (215 cases, 0 skipped)`, 215 `ok-case`, 0 `FAIL-case` (211-215 are new).

## Cost evidence (assigned claim)

`work/time_tokens.py` (single entry, min of 5) and `work/time_multi{,2}.py` (many entries, interleaved rounds,
min of 7) — wall time of the whole `verify-metadata --registry` invocation.

| shape | bytes | base | dd | cb | cb vs dd | cb vs base |
|---|---|---|---|---|---|---|
| dense-token (2 MiB of `a ` = 1,048,576 tokens, no ids) | 2,097,206 | 13,532.73 ms | 17,651.42 ms | **217.78 ms** | **−98.77 %** | −98.39 % |
| id-dense (8,192 × `S001`) | 41,014 | 667.54 ms | 188.25 ms | **186.10 ms** | −1.14 % | −72.12 % |
| id-dense-64k (65,536 × `S001`; extra signal) | 327,734 | 28,793.34 ms | 1,598.51 ms | **1,394.25 ms** | −12.78 % | −95.16 % |
| prose (realistic text, 2 ids) | 24,987 | 759.66 ms | 42.38 ms | **25.80 ms** | −39.13 % | −96.60 % |
| 1,000 entries, id-free source (interleaved, 7 rounds) | — | 4,461.32 ms | 5,691.56 ms | 5,741.10 ms | **+0.87 %** (+0.05 ms/entry) | +28.69 % |
| 1,000 entries, 2-id source (interleaved, 7 rounds) | — | — | 6,799.23 ms | 6,298.88 ms | −7.36 % | — |

**No cost regression remains vs base or dd72641e for change (b).** cb ≤ dd on every token-bearing shape
(98.8 % faster dense-token, 12.8 % id-dense-64k, 39 % prose); its only measured cost is a bounded fixed
**+0.05…+0.15 ms/entry** for the extra grep spawn on an id-free many-entry workload (+0.87 % to +2.59 %
across two interleaved runs at 1,000 entries), recovered by the prefilter as soon as the source carries
any token. The lane's own receipt agrees: `.ufo/waves/round-27/post-falsify/timing.log` —
`before(dd) dense ms=70153` vs `after(cb) dense ms=402`, and `base64eec5d dense(plain) rc=124 ms=300016`
(base **timed out** at 300 s on the dense fixture).

## Inherited (base-identical) behaviour — not attributable to change (b)

* `base`'s `metadata_registry_check_source` was a **pure-bash** scan (`while [[ $source_scan =~ $source_id_re ]]`,
  zero processes); `dd` replaced it with grep tokenization (1 process/entry), `cb` adds a second. On the
  1,000-entry id-free workload that makes dd **+27.58 %** and cb **+28.69 %** versus base — a delta
  inherited from the base→dd C1-C3 repair, not from (b), which adds only +0.87 % on top of dd.
* The `|| true` fail-open on the *tokenization* grep is inherited from `dd` (F1 counterweight (i)); `base` is
  catastrophically slow on token-dense sources (the receipt's 300 s timeout — its scan re-trims the remaining
  subject per match), which is why (b)'s prefilter is a large win, not a risk.

## Residual risk and verification gaps

* F1 is conditional on a grep fault; none was observed with the host's GNU grep 3.12 or pi-uu-grep 0.2.0
  (both implement `-x -E` correctly). The lane working tree moved during this seat (uncommitted gate digest
  `438c0fcb…`); its in-flight diff is scoped to change (a) (GFM escaped-pipe split) and leaves the (b)
  prefilter `|| true` untouched — F1 is still open in flight.
* Only the *registry source scan* was verified; cb's other changes ((a) GFM header width, (c) linear CR
  strip, (d) as-of usage matcher) belong to other seats. The 1,006-value corpus is synthetic and holds no
  real lane knowledge entry, so unusual Markdown (reference links, HTML, nested lists) in a real `source:`
  header is uncovered — that surface belongs to the metadata parser, not the prefilter. Cost numbers are
  host-specific (32 vCPU, warm cache, Arch GNU grep 3.12): absolute times will differ elsewhere, ratios
  should not. Lane read-only throughout: no git/jj write, no edit outside this report; fixtures, stubs and
  harnesses live under `/tmp/chousa-r27-residual-ResTokenPrefilter/`.
