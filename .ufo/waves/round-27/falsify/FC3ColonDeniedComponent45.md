# FC3 falsify — `colon-denied-component` (round27 attempt1)

Item: C3 control `colon-denied-component`, `corpus/evidence/round27-regressions.py:168`
(registry `ROOT/synthetic:fixture/.config/registry.md`, expect exit 2, `metadata registry refused: denylist`, 0 `^RESEARCH_GATE: `).
Revision dd72641e574679c4f7882dd43de072b4c8892d6f; gate sha256 ca39d14d…2f84 (verified in sandbox); regressions.py sha256 5afea786…a5df.
Sandbox: `/tmp/chousa-r27-falsify-FC3ColonDeniedComponent45` (git archive of dd72641e). No installs. No full selftest or full regression run.

## Verdict: HOLDS (with one coverage gap)

The landed gate refuses every colon-before-denied-component variant I tried. Reverting the targeted fix makes the control fail for the intended reason. One gap: the control does not observe the contract's "no reading" clause. Two survivable mutants are listed below, along with a one-line strengthening.

## (1) Expectation independence — holds

- Exit 2, `metadata registry refused: denylist` and the zero-verdict count all come from the existing usage-error interface. At base 64eec5d the `refuse=denylist` → `die_usage "metadata registry refused: $refuse"` path already exists, and only the predicate changed. These are not sets computed by the gate.
- The fixture is derived from the claim text ("no reading a denylisted synthetic path when a colon occurs earlier"). `.config` is a pre-existing denylist component, and the paired `ordinary-colon-is-allowed` control stops a "refuse any colon" gate from passing.

## (2) Mutation of the targeted fix

Harness: `one.py` copies the control's setup from regressions.py lines 47–68 and 166–175 verbatim for one path. `python3 one.py tools/<gate>.sh 'synthetic:fixture/.config/registry.md'` (timeout 120 s each, all exit 0):

| gate | change | rc | verdicts | control |
|---|---|---|---|---|
| landed | — | 2 | 0 | PASS |
| BASE 64eec5d | pre-fix | 0 | 1 (`RESEARCH_GATE: CLEAN`) | FAIL |
| M1 | `is_denylist_fs_path` = prefix-only (helper revert) | 0 | 1 CLEAN | FAIL |
| M4 | all 3 registry-loader calls → `is_denylist_path` (exact pre-fix callsites) | 0 | 1 CLEAN | FAIL |
| M2 | only `$path` check → prefix | 2 | 0 | PASS (caught by canon) |
| M3 | `$path`+`$canon` → prefix; `fdcanon` kept | 2 | 0 | PASS (**opened before refusal**) |
| M5 | M4 + denylist check moved **after the read** | 2 | 0 | PASS (**file read, then refused**) |

The failing mutants fail for the intended reason. They are not parse or setup errors: the gate exits 0 with `META entry=entry.md … verdict=clean` / `RESEARCH_GATE: CLEAN`, which means it opened and parsed the denylisted registry. A `bash -x` trace of M4 shows `ptr_file_part` → `…/synthetic` → not denied, then `fdcanon=…/synthetic:fixture/.config/registry.md` and parsing.

M2 and M3 surviving is defense in depth: the three checks overlap. M5 surviving is a real gap. The contract says "no **reading**", but the fixture content is benign, so read-then-refuse cannot be told apart from refuse-before-read.

## (3) Nearby inputs on the landed gate (registry path, same harness)

These were refused (exit 2, denylist), which is correct:

- the relative-argument form
- `a:b:c/.config/…`, `:/.config/…`, `x:/.config/…`
- `synthetic:fixture/{.omp,.local/state,credentials,oauth,chrome-profile,Login Data,server.token}/registry.md`
- `synthetic:fixture/Cookies`, `synthetic:fixture/op.env`
- `synthetic:fixture//.config/…`, `synthetic:fixture/.config/sub/…`

These were read (exit 0 CLEAN). None is a bypass caused by the colon:

- `synthetic:.config/registry.md` and `.config:x/registry.md`: no actual `.config` component, so allowing them is correct.
- `synthetic:fixture/.config` (a regular file named `.config`) and `synthetic:fixture/a.env/registry.md`: these are inherited from the denylist value grammar (`*/.config/*` needs a trailing slash, and `*.env` is anchored at the end). The no-colon analogues `.config` and `a.env/registry.md` are read identically on both landed and base. This is outside this item, and the claim already says to report inherited grammar limits.

Calibration tradeoff (over-refusal, not a bypass): `ordinary.env:notes/registry.md` is **refused**, because the retained prefix arm checks `…/ordinary.env`. `a.env/registry.md` is **read**. So whether a path under a `*.env` directory is refused depends on whether a colon follows `.env`. Base behaved the same way, and the change is deliberate legacy compatibility (`legacy-env-anchor-refusal`). It is fail-closed, so it is not a defect for the judge; the cost is calibration only.

No counterexample where the landed gate reads a denylisted component that follows a colon.

## Smallest safe correction (controls only, gate unchanged)

Make the fixture discriminate on "not read". Write the colon-denied registry with a trailing NUL (`header + row + '\0'`) and keep the expectation `metadata registry refused: denylist`, adding forbidden `refused: nul`. Measured with `NUL=1 one.py …`:

| gate | result |
|---|---|
| landed | `refused: denylist` (PASS) |
| M4 | `refused: nul` (FAIL) |
| M5 | `refused: nul` (FAIL) |
| M3 | PASS (refused after open, before read) |

M3 still passes, which is acceptable: no content is read, though an open happens. This kills the read-then-deny mutant class without changing the gate. An adversarial mutant that overrides `nul` with `denylist` can still evade it, and only an out-of-band read observation could close that.

Impacted axes: calibration (control strength), with no regression seen. Operability and freshness were not touched.

## Limits

- Registry loader only. I checked the entry reader, the claims source, and chain/sweep/citation callsites (which still use the prefix-only `is_denylist_path` for citation pointers by design) only by reading the code. I did not attack them.
- The harness copies the control setup instead of running regressions.py. Every result is a single command on sandbox mutants.
