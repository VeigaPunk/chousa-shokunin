# RevC1V2LegsP2 — review of legs P04 CHECK, P05 REFUSEROW, P06 REBUILD (c1v2-count.py, both profiles)

Scope: `corpus/evidence/round62/c1v2-count.py` (docstring + `leg_p04`, `leg_p05`, `leg_p06`, `clean_out`,
`snap`, `run`, `_env_and_limits`). Read-only on the lane; no edits to frozen files; no git mutation; no installs.
Scratch `/fast/scratch/hyaku/chousa-r62/RevC1V2LegsP2/` (deleted before yield). Counter runs used `python3 -B`,
`--work` under scratch, `C1V2_SEED` set (and once unset).

## Findings

**F1 — tautology: P05 passes a builder that does nothing but exit 1.** (`tautology`)
- Builder `import sys` / `sys.exit(1)` (no writes, no rows checked).
- `C1V2_SEED=1 python3 -B corpus/evidence/round62/c1v2-count.py --builder t1.py --work <d>` →
  `LEG P05 REFUSEROW pass neutral: ok rc=1 | plain: ok rc=1` (same at seed 2). P05 = `rc==1 and clean_out`; any
  exit-1 stub with an empty `out` satisfies it. Composite still fails (`LEGS=11/20`; P04 and P06 printed as fail, the rest not printed), so the
  battery is safe, but P05 alone measures nothing about refusal.
- Fix class (for the next round's battery, not this one): P05 needs a positive partner, e.g. the same builder on the
  good quote table must reach golden in the same run, or refusal must be shown by a diff against a no-refusal run.

**F2 — tautology: P05 "no file written" inspects only DIR, so writes elsewhere pass.** (`tautology`)
- `clean_out(fx)` and `snap` look at `fx.out` only; neutral cwd (outside fixture) and the cache are never checked.
- Builder `build-spans.py` with the refusal branch of `build()` extended by
  `pathlib.Path("leak-cwd.txt").write_text("leak")` and `(forms.cache / "leak-cache.txt").write_text("leak")`
  (otherwise the V1 builder, with the link-replace policy). Manual run in scratch:
  `python3 -B t3/build-spans.py --quotes q/q.tsv --out out --cache cache` → stderr `refused S101: quote occurs 0x`,
  exit 1; afterwards the fixture holds `leak-cwd.txt` and `cache/leak-cache.txt` and no `out/`.
- Counter: `LEG P05 REFUSEROW pass neutral: ok rc=1 | plain: ok rc=1` (seeds 1, 2). The H13 leak check has the same
  DIR-only scope (`os.walk(fx.out)`), so an out-of-DIR write is invisible to every leg except by its own marker.
- Note the neutral profile puts cwd outside the fixture and then never checks it: the profile varies a location that
  no leg reads.

**F3 — tautology: P04 passes a `--check` that verifies only the `-1` span files.** (`tautology`, partial checker)
- Victim selection `sorted((fx.out/"spans").iterdir())[0]` always picks the `-1` file of the lexicographically
  smallest id (two_url_rows: ids A (rows -1, -2) and B (-1)). Any `--check` that skips every `-n` with n≥2 passes.
- Mutant t2 = V1 with, in `check()` after `name = want.split("\t")[4]`, `if not name.endswith("-1.txt"): continue`.
- Counter: `LEG P04 CHECK pass neutral: ok rc=0,0,1 | plain: ok rc=0,0,1` (seeds 1, 2). The docstring's `--check`
  "re-derives every row" is therefore not enforced by P04; P04's changed byte is not randomised over span files.
- Fix class: change the victim to a seeded choice over all span files (counter change, next round).

**F4 — false positive: golden pins output line terminators the builder docstring never states.** (`false_positive`)
- The builder docstring fixes the output columns and span-file bytes; it says nothing about the trailing newline or
  the line terminator of `spans.tsv` (the only line-ending rule is for the INPUT TSV, `tools/build-spans.py` l.28).
  The counter's golden is `"\n".join(lines) + "\n"`.
- Mutant t5 (CRLF manifest): `tsv = ("\r\n".join(lines) + "\r\n").encode("utf-8")` →
  `LEG P06 REBUILD fail neutral: FAIL rc=0,0 | plain: FAIL rc=0,0` and `LEG H10 SPANSLINK fail ... rc=0`
  (seeds 1, 2); `LEGS=13/20 C1V2=FAIL`. P04 still passes (`--check` parses with `splitlines`).
- Mutant t6 (no trailing newline): `tsv = "\n".join(lines).encode("utf-8")` → P06 fail in both profiles, H10 fail,
  `LEGS=13/20` (seeds 1, 2); P04 pass.
- Both are readable, contract-consistent outputs; the counter rejects them because the golden is byte-exact. P04
  and P06 disagree about the same manifest. Route as a counter limit (compare parsed rows, or pin the terminator in
  the builder docstring first), not as a builder defect.

## Correct builders (false-positive hunt, item (a))

Three correct builders, each a variant of a pos-indep control, edited in scratch:

| builder | from | change (policy/order/IO) | seeds run | result |
|---|---|---|---|---|
| V1 | pos-indep1.py | build first, then `heal_links()`: unlink (never follow) links at `DIR/spans`, `DIR/spans.tsv`, span files; DIR link still refused (replace-a-link policy) | 1–8 + unset (3561151621) | 20/20 PASS every run |
| V2 | pos-indep3.py | quotes read with locale default encoding (`read_text()`) | 1–8 + unset (3613029202) | 20/20 PASS every run |
| V3 | pos-indep2.py | refuse output links before row checks (guard order: output refusal exit 2 precedes row refusal exit 1) | 1–8 + unset (1550271699) | 20/20 PASS every run |

- P04, P05, P06 pass in both profiles for all three builders at all nine seeds: no false positive from these legs.
- Locale probe (V2): the neutral LANG set `C`/`POSIX`/`C.UTF-8` does not change any leg (Python 3.14 UTF-8 mode).
- Profile check over all runs (correct builders and mutants, 920 `LEG` lines in scratch outputs): zero legs with
  differing status between `plain` and `neutral`, and zero differing `rc` strings for P0x/Hxx.

## Profile dependence (item (c))

- P04/P05/P06 verdicts do not depend on profile for any builder tried (table above and 920-line check). The AND rule
  (`results[n] = (all(oks), det)`) means a leg can only fail more, never less, from the second profile, so neutral
  cannot mask a plain-profile failure.
- Can neutral make a P04/P05/P06 hazard ineffective? No hazard of these legs depends on a name: P04 changes a byte,
  P05 uses an absent quote, P06 reruns. Name collision between `out_name` and `cache_name` needs equal length and
  letters (about 4e-7 per fixture at length 4, INFERENCE from `secrets.choice(range(4,9))`), so it is negligible.
- Env/limits that could bind a P0x leg: RLIMIT_FSIZE (384 MiB–1 GiB neutral vs 512 MiB plain), AS 200–224 MiB vs
  200 MiB, pipes vs files, cwd and HOME. None binds a builder that writes kilobytes; they bind H14/H15/H20 (not in
  scope, not run for this review beyond the full counter runs, which passed for V1–V3).
- Counter exceptions (P04 on a builder that writes no `spans/`) are recorded as FAIL with a path in the detail, so the
  profile text differs by path only; no verdict depends on it.

## Verification gaps

- Mutants t0 (exit 0 no-op) and t4 (`--check` always 0) fail P04 as expected (`LEG P04 CHECK fail ...`, t4
  `rc=0,0,0`), so P04 does discriminate those; not a defect.
- Not run: H14/H15/H20 with a correct builder under the AS/FSIZE limits beyond what V1–V3 already passed; no
  leak test beyond the manual demo (F2); no test of a symlink-replace on a span file beyond V1's full-counter pass.
- No live network; no lane file changed; no pacman/git mutation.

## Verdict inputs

defects: F1 tautology, F2 tautology, F3 tautology, F4 false positive. Legs: P04 (F3, F4), P05 (F1, F2), P06 (F4).

VERDICT: LEG_DEFECTS=4 false_positive=1 tautology=3 legs=P04 CHECK, P05 REFUSEROW, P06 REBUILD
