# ExecC2Build — C2 (exempt-hop audit) candidate build, round 32 attempt 2

Status: **candidate built and self-verified, NOT scored.** Per the binding control rule I ran
neither `corpus/evidence/round32/c2-count.py` nor `c1-count.py` against this build (no receipt is
claimed). Verification here is the gate's own selftest, the two named chain fixtures, a hand-built
15-hop class matrix that mirrors the frozen class list, and `verify-all --json` parseability.

Lane tip cloned: `4111607c857bc29ff31883bc095ae00afb527e50` (`git -C lane rev-parse HEAD`).
Base gate in that clone: SHA-256 `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`
(unmodified since base). Build gate: `2a21aa4327e0bb05cfd55ebfacffd397b8a2725dd45ecb7f3b99f420481c2923`.

## Deliverable

`c2.patch` — `git -C <clone> diff -- tools/research-gate.sh` against
`4111607c857bc29ff31883bc095ae00afb527e50` (233 insertions, 46 deletions; only file touched).
SHA-256 `dd1244b5670cc8c953aa49f32831627c2ecf5957a9706e2b04e4d4b00d9dc8fd`.
`git apply --check c2.patch` on a clean tree at the base commit → exit 0 (`PATCH_APPLIES_TO_BASE`).

Artifacts in this directory (all < 1 MiB): `c2.patch`, `selftest-build.out` (sha
`46e5cded4700e3dac4d28ddcbcb1c798cece008eff8621899df8f71adb37f423`), `selftest-base.out`
(`00d3042ddb64c0985ac8f26b0f35232ee639234f016daf40dc99c2305cf93472`), `chain-r3-build.out`
(`e6490f817bd5daf52c7cf9b310e8c8f12c8fd7da3f9a961a51ae5f7917f4eac8`), `chain-r3-base.out`
(`22376dde4cc30133e4c0d27e93d5aa92a0d1a3876ea5ffeed155992ce33bc585`),
`chain-r3-broken-build.out` (`3ec938a96a6ca7e48acefa84ea5523e59e170329b95f899dc26bf63a3f1234c4`),
`matrix.out` + `matrix-record.md` (`e49a7c7a9a8adba5c9df2e1987ce6541df377b5deca8f9e2fccae233bd976b7b`,
`4c870c338b469d79c556108a17da37fda055084fdf763d696691d156908c0ac4`).
Scratch clone and runs: `/fast/scratch/hyaku/chousa-r32/w1/ExecC2Build/{lane,baseline-lane,run}`.

## What changed in `verify_chain`

1. **One probe, both arms.** New `chain_probe()`
   (`tools/research-gate.sh:1804`, patch hunk `@@ -1783,6 +1801,51 @@`) performs exactly the
   resolved arm's checks — `chain_citation` parse, `## Sources` id lookup, undeclared-id refusal,
   `chain_ref_file`, `claim_source_path` (same boundary/canonicalization/dev-cap as verify-claims,
   URL sources refused unread), file read, `chain_anchor_at` — and emits nothing. The resolved arm
   was rewritten onto it with byte-identical findings/`CHAIN` lines; the exempt arm now calls it.
   This is why the two arms cannot drift apart: there is one implementation of the rule.
2. **Status split.** `unresolved|blocked-no-fetch|labelled-dead` (the U set that says the hop could
   not be followed) now probes; `PROBE==verified` ⇒ `N_RESOLVABLE`, one
   `FINDING CHAIN_EXEMPT_RESOLVABLE severity=warn surface=chain obs=hop=<hop> status=<st>
   source=… anchor=<kind>:"…" at=<line>` and
   `CHAIN hop=… observed=resolvable … verdict=mismatch`. Any other probe outcome keeps the old
   `observed=exempt` line. `rejected|not-applicable` keep the old arm untouched (unread, exempt).
3. **Summary, additive at the END only:** `(hops= verified= exempt= anchor-missing= refused=
   invalid= findings= drift= resolvable=N)`. `RESOLVED_HOPS=N/M` is unchanged. The drift invariant
   is now `N_VER + N_EXEMPT + N_RESOLVABLE == N_HOPS` (`:1976`); the warn finding also drifts.
   `verify_all_section` captures the whole `( … )` body and `json_counts` keeps extra keys, so the
   manifest section gains `"resolvable":N` and stays parsable (measured, below).
4. Docs updated in the header contract (`:103-128`) and `usage` (`:372-378`).

No network read was added: a URL citation is still refused by `claim_source_path` before any read
(`CHAIN_SOURCE_EXTERNAL` shape, now silent in the U arm).

## Evidence (commands, exit codes, key output)

Run from the lane checkout `/home/vgpnk/Projects/shokunin/chousa-shokunin` unless noted;
`TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/ExecC2Build/run`.

| Check | Command (gate path abbreviated `$G`) | Result |
|---|---|---|
| selftest, build | `bash $G --selftest` | `RESEARCH_GATE_SELFTEST: PASS (232 cases, 0 skipped)`, exit 0 |
| selftest, base | same, base gate | `PASS (228 cases, 0 skipped)`, exit 0 |
| base lines unchanged | `cmp` of the first 228 `ok-case` lines | `BASE_228_BYTE_IDENTICAL` (exit 0) |
| new cases | `grep chain-exempt selftest-build.out` | cases 229–232 `ok-case` |
| `chain-r3.md` | `bash $G verify-chain corpus/fixtures/chain-r3.md --root ..` | exit 0, `RESOLVED_HOPS=17/22`, `RESEARCH_GATE: CLEAN (… exempt=5 … resolvable=0)` |
| `chain-r3-broken.md` | same on broken fixture | exit 1, `RESOLVED_HOPS=1/2`, `DRIFT (… anchor-missing=1 … drift=1)` |
| no-harm diff | base vs build output of `chain-r3.md`, `sed` masking `ts=` and trailing ` resolvable=0)` | `diff -u` empty → `R3_IDENTICAL_MODULO_TS_AND_NEW_COUNT`; U hops 18–22 still `observed=exempt` |
| claims untouched | `bash $G verify-claims corpus/fixtures/claims-r2.jsonl --root ..` | exit 0, `VERDICT_BEARING_CLAIMS=17/17`, CLEAN |
| r1 observable | SCORECARD counting command with `$G` substituted (both gates) | `VERDICT_BEARING_EXPORTS=3/3` and `3/3` |
| verify-all + manifest | `bash $G verify-all /tmp/c2matrix-exec/root/rec.md --json …/man.jsonl` twice | both exits 1; `SECTION chain … tally=RESOLVED_HOPS=1/15`; `json.loads` on both lines: `chain drift 3`, `tallies.resolvable=3`, `tallies.exempt=11` |
| class matrix | `bash $G verify-chain /tmp/c2matrix-exec/root/rec.md --root .` | exit 1, `hops=15 verified=1 exempt=11 … findings=3 drift=3 resolvable=3`; 15/15 against hand truth |

Class matrix (record kept as `matrix-record.md`, output `matrix.out`) covers every frozen class
shape: R1 `path#quote:` fragment, R2 path + `anchor_kind`+`anchor` (heading, line, quote), R3
declared id, F1 resolved-verifiable, E1 anchor absent, E2 missing file, E3 external URL, E4 no
citation, E5 `rejected`/`not-applicable` with a resolvable citation, E6 undeclared `S` id, E7
out-of-corpus file that exists, E8 glued quote (`qalpha`), E9 heading present only as a plain line,
E10 whole-line anchor that is a strict prefix of its line. Resolvable hops: exactly one
`CHAIN_EXEMPT_RESOLVABLE` each, `observed=resolvable`; every exempt hop: zero findings; the
resolved hop: `observed=verified … at=line:2 verdict=match`, no finding. Total findings = 3 =
resolvable count, i.e. no `CHAIN_SOURCE_*`/`CHAIN_ANCHOR_*`/`CHAIN_CITATION_*` line leaked from the
silent arm (asserted in selftest by `got_other`).

## Harness hazard found while validating (report-only)

`LANE_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)` (`:304`) makes a gate copy's *parent directory* an
allowed source root. A flat `scratch/<gate>.sh` therefore admits every sibling under `scratch/`,
including a `C2_TMP` fixture's `../outside/` file — an E7-shaped control would then score as a
false positive on the *control*, not on the candidate. I hit this twice: the base gate at
`…/ExecC2Build/base-gate.sh` and `…/ExecC2Build/base/tools/research-gate.sh` both failed selftest
cases (`9/228`, then `claims-lane-fallback`) purely because `TMPDIR`/fixtures sat under its lane
root. Fix used and recommended to the L1 for every C2 receipt: place the scored gate at
`<scratch>/<name>/tools/research-gate.sh` with `C2_TMP` **outside** `<scratch>/<name>`, or run with
the counter's fixture temp dir outside the gate's parent. `baseline-lane/` (a full clone with the
base gate overlaid, sha `0bc318b3…`) is the isolated base comparison tree.

## Limits / risks

- P2 is **not claimed**: the frozen counter was never run on this build (control rule). The
  counter's match predicate (`observed=` equality plus the finding-id set, one `CHAIN` line per
  hop, no `FINDING` naming an exempt hop) is mirrored by the matrix and by the selftest's counting
  assertions, but that is evidence, not a score. `[INFERENCE]` R1–R3 will resolve under this build
  because each class was reproduced with the same citation shapes; E1–E10 stay exempt by the same
  probe that leaves them absent.
- `exempt=` no longer counts resolvable hops; a record with false exemptions now reads
  `exempt` lower *and* `resolvable` higher, plus `drift`. Any external tool that hard-codes
  `exempt == hops - verified` will see the arithmetic change — `RESOLVED_HOPS` is unchanged.
- The U arm reads a cited local source (bounded by `claim_source_path`: exists, in root, single
  link, same device, ≤ 8 MiB). This is the claim's intent, but it is a new read on hops that
  previously caused none; E3 (URL) is still never opened.
- Not run here, left to the parent's post-integration gate: the round-31 counters
  (`corpus/evidence/round31/*`, 120/120 each), `--drift` against the r8 baseline, and the frozen
  P2 run on the landed revision.
- No production file in the lane or fleet repo was written; no git/jj write command ran; only read
  git (`rev-parse`, `diff`, `apply --check`, `clone`) in my own scratch trees.
