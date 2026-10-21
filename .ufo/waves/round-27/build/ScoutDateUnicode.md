# ScoutDateUnicode — round27 attempt1

- **Assigned item / axes:** C2 — available-locale-independent Unicode regression strategy, read
  from source. Freshness (control calibration). Static read-only seat: no gate, selftest,
  `localedef`, `locale -a`, or any other runtime probe was executed.
- **Base:** `64eec5d41c7cf7f17f5ce1e968e28b3769952596`. Gate line numbers below are from
  `git show HEAD:tools/research-gate.sh`; the shared worktree currently carries an unrelated C1
  edit after line 6007, so working-tree numbers diverge only there. Suite line numbers are the
  current untracked `corpus/evidence/round27-regressions.py` and drift while peers edit it; the
  quoted anchors are authoritative.

## Source findings

**F1 — one unpinned validator call is the whole locale defect.** `metadata_iso_date`
(`tools/research-gate.sh:2295-2307`) tests
`[[ $1 =~ ^([0-9]{4})-([0-9]{2})-([0-9]{2})$ ]] || return 1` at :2296 with no locale pin.
Its callers :2720, :2739, :2747 and `metadata_add_days` (:2343, invoked at :2748) all run inside
`verify_metadata` and inherit its `local LC_ALL=C` (:2539), but the CLI guard at :6295-6298 runs
in main scope and inherits the process locale. Under a collating UTF-8 locale, glibc's `[0-9]` range admits non-ASCII numeric
code points (r26 measured 1050 in `en_US.UTF-8`, ASCII-only in `C` and `C.UTF-8`:
`.ufo/waves/round-26/falsify/FDateAsOfUsage.md:44`). `$((10#…))` at :2297 then aborts under
`set -euo pipefail` (:255), bypassing `die_usage` (:390, exit 2), and the process exits 1 with
raw Bash diagnostics — the accepted r26 receipt (`FDateAsOfUsage.md:55-86`). `metadata_add_days`
:2346 (`[[ $digits =~ ^[0-9]+$ ]]`) has the same form and currently relies on the same caller
pin.

**F2 — the draft suite's control is host-dependent.** In the C2 block of
`corpus/evidence/round27-regressions.py` (currently :118-122), `for locale in ('C',
'en_US.UTF-8'):` hardcodes one locale name and the row forbids `'cannot change locale'`. On a host
where `en_US.UTF-8` is not generated, glibc falls back to `C` and bash prints
`warning: setlocale: LC_ALL: cannot change locale`, so the correct fixed tree produces a false
MISMATCH. On a host where it is generated (this host's `/etc/locale.gen` has `en_US.UTF-8`
uncommented) the row works, but the control's validity depends on locale-gen state — exactly the
availability coupling C2 must remove. `C.UTF-8` cannot replace it: r26 confirmed it admits only
ASCII under `[0-9]`, so it is contract-valid but non-discriminating.

**F3 — harness text encoding is locale-derived.** `round27-regressions.py:25` reads the gate with
`gate.read_text()` and :182 writes the JSON report with `ensure_ascii=False` under
`Path.write_text` without `encoding=`. The gate contains non-ASCII em dashes (header :2 and the
verdict printfs, e.g. :2772), so both operations depend on the parent process locale rather than
on the bytes.

## Recommended strategy (five layers, none dependent on installed locales)

**A. Synthetic trigger locale (primary; makes discrimination deterministic).** Generate a
throwaway collating locale inside the suite's `TemporaryDirectory` and point `LOCPATH` at it;
`--no-archive` keeps `/usr/lib/locale` untouched. Recipe [INFERENCE — to be exercised once by
L1]: `localedef --no-archive -i en_US -f UTF-8 <tmp>/locale/en_US.UTF-8`, then run the gate with
`{'LC_ALL': 'en_US.UTF-8', 'LOCPATH': '<tmp>/locale'}`. Preconditions checked statically in the
suite (`Path.exists`, no hard failure): `/usr/bin/localedef`,
`/usr/share/i18n/locales/en_US`, `/usr/share/i18n/charmaps/UTF-8.gz` — all present on this host.
Before asserting on the gate, prove the locale actually took effect by probing the same regex
engine the gate uses: `bash -c '[[ $1 =~ ^[0-9]$ ]]' _ '١'` under that env must exit 0. A
non-collating or unresolved locale records an explicit `skip` (reason
`synthetic-locale-not-collating`), never a silent pass. This is the only layer that makes the
base-vs-fixed difference deterministic on any glibc host with locale sources.

**B. Capability-discovered installed locales (fallback when A is unavailable).** Parse
`locale -a` in `try/except FileNotFoundError`; keep names matching `(?i)\.utf-?8$` (excluding
`C`, `POSIX`, `C.utf8`/`C.UTF-8`, which r26 proved non-collating), then filter by the same
one-line `[0-9]` probe. If the resulting set is empty, record `skip` with reason
`no-collating-utf8-locale`; do not emit an assertion against an unavailable name. This preserves
coverage without hardcoding `en_US.UTF-8`.

**C. Always-on contract rows (locale-free).** Run the Unicode tokens under `LC_ALL=C`,
`LC_ALL=POSIX`, and the inherited environment (scrubbed base env with `LC_ALL`, `LANGUAGE`,
`LOCPATH` removed — the r26 default-exposure configuration). These rows assert the contract even
where no collating locale exists; they do not discriminate the base under `C`, which is why A/B
and D exist.

Token set (UTF-8 literals in Python source, one row each, slug names): fullwidth `２０２６-10-21`;
Arabic-Indic `٢٠٢٦-10-21`; Devanagari `२०२६-10-21`; astral mathematical bold `𝟐𝟎𝟐𝟔-10-21`
(exercises 4-byte UTF-8 truncation); superscript `²⁰²⁶-10-21`; mixed position `2026-10-2１`;
multibyte plus calendar-invalid `２０２６-02-30`. Expectations, unchanged from the real contract:
exit 2; exact `--as-of must be a valid YYYY-MM-DD date`; anchored `^RESEARCH_GATE: ` count 0;
`^META entry=` count 0; forbid `10#`, `invalid integer`, `arithmetic`, `syntax error`; forbid
`cannot change locale` only for rows whose locale was proved available/synthesised (A/B), not for
the inherited row where a shell startup fallback is environment noise. Add one positive accept row
per trigger locale (ASCII `2026-10-21`, `verified-at 2026-10-01`, `recheck 90d` → `due=2026-12-30
freshness=current`, one anchored verdict) so an over-broad rejection fix cannot pass.

**D. Locale-free structural invariant (always runs; discriminates the base with zero locales).**
Extract the validator with `re.search(r'^metadata_iso_date\(\) \{.*?^\}\n', text, re.M | re.S)`
(same function-extraction practice the suite already uses for the C1 helpers at :74-75) and fail
when the body contains the locale-variant range `[0-9]` and no self-contained `LC_ALL=C` pin.
Pass on either legitimate fix (literal `[0123456789]` members, or an in-function pin, preferably
both); fail on base (`[0-9]{4}`, no pin). Record it as a static result (`observe_static`) with a
`skip`-free expected-pass row. This is a fallback invariant, not a substitute for A/B behaviour;
keep it narrow and name it `ascii-date-validator-self-contained`.

**E. Harness locale independence (required, small).** `gate.read_text(encoding='utf-8')` at :25;
`args.output.write_text(..., encoding='utf-8')` at :182; pass synthetic tokens as UTF-8 bytes
(`token.encode('utf-8')`) rather than relying on `os.fsencode`/`sys.getfilesystemencoding`; build
the base env without forcing `LC_ALL` (keep `LC_ALL='C'` as the `run()` default so existing rows
are unchanged) and scrub `LOCPATH`/`LANGUAGE` so an operator-inherited `LOCPATH` cannot resolve a
locale name the suite believes is absent.

## Suggested fix shape (executor; target, not this seat)

Make `metadata_iso_date` self-contained: `local LC_ALL=C; export LC_ALL` at function entry plus
literal ASCII members `[0123456789]` in the shape test (belt and braces: the pin does not depend
on bracket-list-vs-range collation semantics, the list does not depend on bash propagating a
local locale assignment). Preserve the shape-before-arithmetic order; no arithmetic on unmatched
text. Carry the same self-contained property into the rewritten `metadata_add_days` decimal test
(:2346). Do not add a Unicode case to `run_selftest` — C2 controls belong in
`round27-regressions.py`, leaving the 187 original selftest identities and the legacy 161
untouched.

## Suggested additional control (same strategy, entry side)

`recheck: ９０d` (fullwidth cadence) with ASCII `verified-at` must yield
`META entry=entry.md source=present verified_at=dated recheck=unscheduled due=unknown
freshness=unknown verdict=clean`, exit 0, one `META_RECHECK_UNSCHEDULED` info finding, under the
synthetic locale. r26 left entry-side exposure as inference (`FDateAsOfUsage.md:166`); this
row tests `verify_metadata`'s :2539 pin behaviourally. Optional ordering row: Unicode `--as-of`
plus `--registry <denied synthetic path>` must emit the date message, not the registry refusal
(the r26 guard-bypass evidence). Note for the C3 owner: registry row ids (:2433) parse under the
loader's own pin (:2366) and the entry-side source scan (:2474) under :2539, so a `S٠٠١`
negative control under the synthetic locale is cheap if wanted.

## Acceptance and unrun checks

- Fixed tree: every Unicode row exit 2 with the exact message, zero anchored verdicts, zero
  `META entry=` lines, no arithmetic/`10#` diagnostics; accept row correct; structural row pass;
  suite exits 0. Base archive: synthetic-locale rows and the structural row mismatch, suite
  exits 1; any skipped row is printed and counted in the summary, never folded into mismatches.
- Not run by this seat: `localedef` recipe, locale probes, the suite, the gate, the selftest, any
  build/lint/formatter. No tools installed. L1 owns the single integrated verification.
- **Provenance:** read-only sources: `tools/research-gate.sh` (base HEAD and worktree),
  `corpus/evidence/round27-regressions.py`, `corpus/evidence/round26-date-differential.sh`,
  `.ufo/waves/round-26/falsify/FDateAsOfUsage.md`, `corpus/knowledge/recheck-due-r26.md`,
  `/etc/locale.gen`, `/usr/share/i18n/*` and `/usr/lib/locale` listings. Only this report was
  written. No production, test, fixture, git, or index writes.
