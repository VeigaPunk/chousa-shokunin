# SepAudit32 — wave 2 (falsify): separability receipts, round 32 attempt 2

Verdict: **HOLDS** (the separability requirement is met in v2 terms), with two low-severity
provenance/documentation findings (F1, F2) that do not break either claim.

Target attacked: `corpus/evidence/round32/claims.md:92-97` (Separability, written under design
v1 and carried untouched into v2): "C1 changes only the `--json` append block of `verify_all`;
… C2 changes only the exempt arm of `verify_chain` … C2 counter on the C1-only build prints
84/120; C1 counter on the C2-only build prints a count below 24."

## Builds (scratch, frozen base)

Base gate `sha256 0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`
(`git clone -q <lane> <dir> && git -C <dir> checkout -q 7a7259f0ad41a68068131bfa422a829db9fd1b55`;
hash matches `claims.md` base gate).

Commands (scratch root `/fast/scratch/hyaku/chousa-r32/w2/SepAudit32`):

```
git -C c1only apply <w1>/ExecC1Build/c1.patch   # exit 0
git -C c2only apply <w1>/ExecC2Build/c2.patch   # exit 0
bash -n c1only/tools/research-gate.sh c2only/tools/research-gate.sh   # SYNTAX_OK
```

| build | gate SHA-256 | copy kept in w2/SepAudit32 |
|---|---|---|
| C1-only (base + c1.patch) | `3144a46f443f2202e00bb96a0f0ce147beadc1cc22b87b353bcc73bb5b4884aa` | `c1-only-gate.sh` |
| C2-only (base + c2.patch) | `2a21aa4327e0bb05cfd55ebfacffd397b8a2725dd45ecb7f3b99f420481c2923` | `c2-only-gate.sh` |

## Cross-counter runs (fresh seeds, committed counters unmodified)

Run from lane root, `C1_TMP=C2_TMP=TMPDIR=/fast/scratch/hyaku/chousa-r32/w2/SepAudit32/tmp`,
`timeout 900 prlimit --nproc=8000 python3 corpus/evidence/round32/<counter> --gate <scratch>/tools/research-gate.sh --seed <s> --receipt .ufo/waves/round-32/w2/SepAudit32/<name>.json`.

1. **C2 counter on the C1-only build** — `c2-count-v2.py` (`counter_sha256 8ec1a1ed…`), seed 7201:
   `EXEMPT_AUDIT_MATCH=0/132`, `RECORD_CHECKS=fail:gate-rc=0,drift-summary-lines=0`, every class
   0 (R1–R3 0/12 each = 0/36), exit 1. **Equals the v2 base value `0/132`** (`claims.md:177`,
   `claims.md:182`: before value under v2 is **0/132**), not the stale v1 `84/120`.
   Receipt `.ufo/waves/round-32/w2/SepAudit32/c2-on-c1only-s7201.json`
   (`sha256 8474ee62656a7d889ee0430f456f5b924e29bb3a8035a6829d76b3daae900784`; records
   `gate_sha256 3144a46f…`, `matched 0`, `predicate_holds false`).
2. **C1 counter on the C2-only build** — `c1-count-v2.py` (`counter_sha256 e6bf9531…`), seed 7201:
   `APPEND_SERIALIZED=0/24` (F_unterminated 0/12; L_empty/L_terminated/L_unterminated 0/4 each),
   exit 1. **Below 24**, and equal to the v2 base value `0/24` (`claims.md:159`).
   Receipt `.ufo/waves/round-32/w2/SepAudit32/c1-on-c2only-s7201.json`
   (`sha256 7b92596e1ddd9198937860d5dcc9ed66383a3d19279200da2824dcb3b2125e14`; records
   `gate_sha256 2a21aa43…`, `matched 0`, `predicate_holds false`).

Build sanity (non-candidate receipts, labeled; they rule out a broken build/strace environment as
the cause of the zeros): `c1-count-v2.py` on the C1-only build, seed 7202 → `APPEND_SERIALIZED=24/24`
exit 0 (`buildsanity-c1-on-c1only-s7202.json`, `sha256 67474843…`); `c2-count-v2.py` on the C2-only
build, seed 7202 → `EXEMPT_AUDIT_MATCH=132/132` exit 0 (`buildsanity-c2-on-c2only-s7202.json`,
`sha256 0ed32286…`).

## Structural separability (source level)

Function bodies extracted with `awk '/^verify_all\(\) \{/{p=1} p{print} p&&/^\}$/{exit}'` (same for
`verify_chain`, `chain_probe`) and hashed; landed = lane `tools/research-gate.sh` `10f2fe12…`:

| body | base | C1-only | C2-only | landed `10f2fe12` |
|---|---|---|---|---|
| `verify_all` | `cc7dfc31…` | `e98168cb…` | `cc7dfc31…` (base) | `e98168cb…` |
| `verify_chain` | `ef629b8c…` | `ef629b8c…` (base) | `f0519a28…` | `f0519a28…` |
| `chain_probe` | absent (empty hash) | absent | `2fee8557…` | `2fee8557…` |

Each patch changes exactly its own surface (`+0` cross-changes: c1.patch hunks are header docs,
usage, `verify_all` append block, selftest cases; c2.patch hunks are header docs, usage,
`chain_probe`, `verify_chain`, selftest cases), and both single-patch bodies are byte-identical to
the landed gate's bodies. The zeros above are therefore the other patch's surface, not a defect.

## Findings

- **F1 (provenance, low, no behavior):** the landed gate is **not** byte-equal to
  base + `c1.patch` + `c2.patch`. `git apply` of the two patches in sequence fails
  (`error: patch failed: tools/research-gate.sh:6869`; `git apply -3` ends in a conflict) because
  both patches insert selftest blocks at the same anchor. The landed gate also carries a one-line
  selftest comment edit absent from both patches: `# ---- r31 C2: … (cases 216-224)` →
  `(cases 216-228)` (base line 6799 → landed line 6907; visible as `@@ -6799,7 +6907,7 @@` in
  `diff base-gate landed`). Behavior-neutral (a comment); function-body hashes above show the
  executable surfaces still equal the single-patch builds. Separability therefore holds against
  the landed artifact, not merely against the patch text.
- **F2 (stale requirement text, low):** `claims.md:97` still requires "C2 counter on the C1-only
  build prints 84/120" — a v1 value. Under v2 the C2 counter's before value is `0/132`
  (`claims.md:177`, `claims.md:182`), and the C1-only build indeed prints `0/132`. A literal
  reading of line 97 is unsatisfiable under v2; the v2-sense requirement (the counter keeps its
  before value on the other claim's patch) is met. `claims.md` is production docs — I did not edit
  it; the parent should annotate Separability for v2.

## Limits

- One fresh seed per cross run, as the ticket specifies (7201); seed 7202 runs are labeled
  build-sanity and are not candidate receipts.
- The scratch gates are base + one patch, not the landed revision; the result carries over to the
  landed gate via the byte-identical `verify_all` / `verify_chain` / `chain_probe` bodies above.
- No selftest, lint or formatter was run (editing wave in flight; gate execution belongs to the
  parent). No network, no installs. No lane/fleet writes, no git/jj writes in the lane or fleet
  repo; scratch trees under `/fast/scratch/hyaku/chousa-r32/w2/SepAudit32` were removed after the
  runs, receipts and gate copies kept.
- All processes started were bounded (`timeout`, `prlimit --nproc=8000`) and have exited; none
  remain.
