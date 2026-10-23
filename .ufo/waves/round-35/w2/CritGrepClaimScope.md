# CritGrepClaimScope — round 35 v2

Access date: 2026-10-23. Axes: **operability** (runtime grep selection and invocation cost), **calibration** (what C1's score actually establishes). This is an advisory critique, not a round judgment or admission.

Paths below: `R=/home/vgpnk/Projects/shokunin/chousa-shokunin`; `S=/tmp/hyaku/chousa-r35/w2/CritGrepClaimScope`; `A=$R/.ufo/waves/round-35/w2/CritGrepClaimScope`. All receipts and retained artifacts are in `A`; experiments ran in `S`. Production files, counters, witness, fleet files, Git index and jj state were not edited. No network, installs, subagents, or other judging runtime.

## Principal counterexample: MEETS without startup verification or a pin

**Observed:** named control `A/ctl-resolve-each-call.sh`, SHA-256 `fc2aeaea4ec09662c4abf50107798aa9400ceaf5b6aaeebc30fc518317c2e8c4`, scores `GREP_PIN_MATCH=9/9`, `predicate_holds=true`, `reference_sane=true` on seeds **3535 and 3553**, both counter exits **0**. Receipts: `A/c1-resolve-each-call-s3535.json:3-7,26` and `A/c1-resolve-each-call-s3553.json:3-7,26`.

The control is the pinned base gate plus a 13-line insertion at `A/ctl-resolve-each-call.sh:315-327`. Its actual matcher wrapper is:

```bash
grep() { PATH=/usr/bin:/bin command grep "$@"; }
```

It resolves a bare command through a fixed PATH **on each call**, never chooses/stores an absolute candidate at startup, and never runs a version probe. It rejects every nonempty override except the literal `/usr/bin/grep`, irrespective of that override's contents, and prints a constant GNU version phrase when echo is requested (`:318-325`). It retains the base matching engine and reads the actual claims/sources; it does not replay fixture answers, inspect seed/root fingerprints, or modify the counter. It skips the claimed startup pin/provenance work, although it is not literally a zero-line no-op.

Why it wins:

- S1–S3 cannot distinguish trusted-PATH resolution on every call from an absolute pin. The wrapper also replaces the imported function.
- S4–S6 require only exit 2 and a marker; rejecting an alternative without inspecting it wins. The winning S6 receipt even records **zero stub calls** (`A/c1-resolve-each-call-s3535.json:144-152`; counter `corpus/evidence/round35/c1-count.py:229-246`).
- S7/S8 accept substring matches in an echo and correct claim output. A constant `version="GNU grep"` passes (`c1-count.py:248-263`). S9 checks only `source=override`, empty tripwire and output equality (`:264-274`).

**Impacted axes:** calibration primarily; operability insofar as a 9/9 receipt is presented as proof of startup selection/verification. This is a counter-soundness defect, not evidence that the landed gate failed its own nine scenarios. It satisfies the assignment's requested MEETS counterexample; it is not an admission verdict.

## Re-derived controls and landed results

Pinned with `timeout 10s sha256sum ...` (exit 0):

| Engine | SHA-256 | Seed(s) | Counter / exit |
|---|---|---|---|
| base, `S/base.sh` | `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` | 3501 | 0/9 / 1 |
| committed hardcoded control, copied to `S/hardcoded.sh` | `05bdf6543858a551852b6b9725d4cd327140f8d94589ae87ce82c5232248a378` | 3501 | 3/9 / 1 |
| landed, `S/landed.sh` | `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` | 3535, 3553 | 9/9 / 0 each |
| resolve-each-call control | `fc2aeaea4ec09662c4abf50107798aa9400ceaf5b6aaeebc30fc518317c2e8c4` | 3535, 3553 | 9/9 / 0 each |

Actual common command form, with the gate/seed/receipt substitutions in the table:

```bash
timeout 180s env C1_TMP="$S" C2_TMP="$S" WITNESS_TMP="$S" TMPDIR="$S" \
  python3 "$R/corpus/evidence/round35/c1-count.py" \
  --gate "$S/base.sh" --seed 3501 --receipt "$A/c1-base-s3501-rerun.json"
```

Other receipt names: `c1-hardcoded-s3501-rerun.json`, `c1-landed-s3535.json`, `c1-landed-s3553.json`, `c1-resolve-each-call-s3535.json`, `c1-resolve-each-call-s3553.json`. These reproduce the committed before receipts' counts and gate digests (`.ufo/waves/round-35/controls/c1-base-s3501.json:3-7`; `c1-hardcoded-s3501.json:3-7`). Base S1/S2 still have correct outputs and 852/867 logged shim bytes; the hardcoded control wins exactly S1–S3. Thus the unchanged base and the supplied hardcoded control do **not** meet P1; the stronger work-skipping control does.

## Claim sizing and predicate identity

The actual round prompt is `/home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-35.md:350-372`. Located quote, 2026-10-23: “A target must be one a do-nothing control cannot reach” (`:359`). It also bars universal clauses without full enumeration (`:353-354`), forbids post-data rule changes (`:364-367`), and names axes by changed surface (`:368-372`).

1. **A real surface move, not merely a restatement.** The landed gate adds a central wrapper, candidate selection, self-report check, refusals and opt-in naming (`tools/research-gate.sh:332-399,8036-8039`). The base/after runs above demonstrate changed executable behavior. Operability is a defensible surface label. But the counter does not establish that the entire mechanism described by the claim is necessary to obtain the score.
2. **The universal surface is larger than the counter.** `claims.md:25-27` names every matcher site, including the chunk matcher and other grep uses. `c1-count.py:27-32,64-84,93-94` deliberately exercises only three short-span claims via `verify-claims`. It does not enumerate chunk, chain, selftest or verify-all sites. [INFERENCE] A central wrapper can cover them structurally, but 9/9 alone is not that enumeration and cannot justify the universal wording.
3. **Predicate labels mostly agree; the stated code condition is incomplete.** `claims.md:38-41` requires both 9/9 and `predicate_holds=true`, but abbreviates its code condition as `passed == 9`. Actual code is `holds = passed == TOTAL and ref_ok`, with `TOTAL=9` (`c1-count.py:49,191-192,277-280`). The receipt label is indeed `predicate_holds`, and its human label is `GREP_PIN_MATCH=9/9`. Therefore the full P1 sentence includes the sanity requirement through the boolean, but the advertised code-condition transcription is not exact. No false-reference exploit was needed here: all scored references were sane. The two-seed/no-committed-lower-run clauses are not evaluated by an individual counter invocation.
4. **Fresh seeds are not fresh claim content.** The seed affects the temporary directory prefix and receipt only (`c1-count.py:154-164,281`); `make_fixture` is fixed (`:64-84,187`). The two fresh-seed runs rerun the same semantic scenarios rather than independently generated inputs.

## Measured time: nonzero invocation cost, no demonstrated selftest penalty

Commands actually run, both outer exits 0:

```bash
timeout 1750s python3 "$A/timing.py"
timeout 1750s python3 "$A/timing-utf8.py"
```

Harnesses preserve the two pinned gate digests, run isolated `base/tools/research-gate.sh` and `landed/tools/research-gate.sh` copies with copied `PROVINCE.md`, clean gate overrides/BASH_ENV, set scratch variables, and bound each subprocess with `timeout 900s`. Timing includes process startup and the same timeout wrapper on each side. Sixty pairs alternate execution order after warmup; invocation is `bash G verify-claims "$S/empty.jsonl" --root "$S"`. Full selftests run in **base, landed, landed, base** order.

Successful UTF-8 measurements (`A/timing-utf8.json`, locale `C.utf8`):

| Measurement | Base | Landed | Observed difference |
|---|---:|---:|---:|
| empty-claim invocation median, 60 each, every exit 0 | 13.941 ms | 15.595 ms | +1.654 ms (+11.87%) |
| paired invocation deltas | — | — | median +1.593 ms; mean +1.479 ms; 53/60 positive |
| full selftest runs, seconds, every exit 0 | 37.700, 39.412 | 37.303, 36.479 | means 38.556 vs 36.891 s (landed −1.665 s) |

Every UTF-8 full run prints `RESEARCH_GATE_SELFTEST: PASS (256 cases, 0 skipped)`; all four stdout digests equal `5311643cc95e6358a9fd513ec8ba67b944617e7d7da2f8df1c4d33d1f0c75c12`. Retained logs: `A/utf8-selftest-{0-base,1-landed,2-landed,3-base}.stdout`.

The initial `LC_ALL=C` series is **not hidden** (`A/timing.json` and `A/selftest-*.stdout`): invocation medians 23.255/25.590 ms, all invocation exits 0; full selftests all exit 1 with `FAIL (10/256 cases)`, means 39.231/41.673 s. Both gates miss the Unicode-arrow claim (`selftest-0-base.stdout:21-29`, `selftest-1-landed.stdout:21-29`). The subsequent UTF-8 run changes locale, not gate bytes. [INFERENCE] Locale accounts for these shared Unicode failures; no new C1 regression is claimed from them.

**Interpretation:** a small invocation penalty is measurable in both series. [INFERENCE] It reflects added startup probing/wrapping/parsing; this is not an isolated timing of just the `--version` subprocess. A selftest slowdown is **not established**: only two successful samples per gate, high/changing host load (UTF-8 1-minute load 21.86→13.20), and opposite signs across locale series. Do not report a zero-cost pin, a proven selftest regression, or a causal speedup. Any decision that the invocation cost is an unacceptable axis trade belongs to the canonical judge, not this critique.

## What readers must not assume

- **Authenticated provenance:** verification is a regular/executable-file check plus a first-line `GNU grep` substring (`tools/research-gate.sh:358-366`). It is self-report, not package ownership, signature or implementation authentication. The knowledge entry correctly names this limit (`corpus/knowledge/grep-pin-r35.md:52-60`).
- **Provenance persisted by VERIFY_ALL:** `timeout 90s python3 "$A/manifest-scope.py"` exits 0; its landed `verify-all --json` subprocess exits the expected **1** for the deliberately drifting three-claim fixture. `A/verify-all-scope.json:14-18,82-96` records the GATE_GREP echo only on stderr and the manifest's actual keys. The appended manifest contains record/gate hashes and section results, **no grep path/version/source/hash** (`A/verify-all-manifest.jsonl`; writer `tools/research-gate.sh:3668-3670`). C1 neither tests these writes nor binds the saved receipt to matcher identity.
- **A SHA pin of the grep binary:** `GREP_BIN` holds a pathname (`tools/research-gate.sh:395`), and the wrapper executes that path again on each call (`:351`). The reported `gate_sha256` hashes the gate script, not grep; this is explicit in the manifest writer (`:3647-3648`). The knowledge entry expressly disclaims binary-integrity pinning (`grep-pin-r35.md:57-60`). A path pin is not an immutable-byte pin.

## Smallest safe correction and limits

Keep the landed implementation and frozen evidence intact; record this work-skipping 9/9 control as a **sizing/counter-sufficiency defect**. Do not silently replace P1 after scoring or narrow its historical target. A later independently frozen attempt should minimally test an unpredictable valid absolute GNU override and tie its observed version probe and actual matcher executions to that override; the allowlist/constant-echo control must then fail. A universal call-site claim additionally needs an explicit enumerated site/mode battery or a separately evidenced structural audit. These are proposed corrections, not tests run here.

Use the precise scope description: selection of an absolute **pathname per shell**, with a **self-reported version check**; do not imply binary hashing or persisted VERIFY_ALL provenance. Correct the next predicate transcription to include `reference_sane`. Quantify the small invocation cost instead of assuming no harm. Documentation/measurement defects are fixable; accepting a genuine performance trade is not a critic's authority.

C2 counter, witness and slen probe were opened in the required order, not scored; this report makes no C2 or repair verdict. No production correction was made. All retained artifacts are below 1 MiB (`timeout 10s wc -c "$A"/*`, exit 0; largest 368310 bytes).

Receipt digests (`timeout 10s sha256sum ...`, exit 0):

- `c1-resolve-each-call-s3535.json`: `f900142f8c390014e2f291cae75ee985d8981fa94d364548065ab7c20d76dc0f`
- `c1-resolve-each-call-s3553.json`: `340a19310e6ef7fbaa407054c2dfcd330aaf55b3726227844df92f84407322df`
- `timing-utf8.json`: `1f5ec1e9d81553fd28d66dcb2535eb45f3e74efa43b69c2305f1822403b8b605`
- `timing.json`: `0cea97115851eb73f8ba74cf2592b66e209c04ed9ae11117516affd9906f8425`
- `verify-all-scope.json`: `00eca9221f36326c742b81a28b93c1d4e26ce3a28e06fa2559f9c1e36ba79dc8`
