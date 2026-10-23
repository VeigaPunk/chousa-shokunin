# ExecC1Control — re-score the pre-data C1 control on two fresh seeds

Lane chousa, round 35, wave 2, seat ExecC1Control.
Scope: re-score `controls/ctl-c1-hardcoded-grep.sh` on seeds 3529/3539 with
`c1-count.py`; report which scenarios a hardcoded pin wins and which it cannot;
a count above 4 would be a finding against P1's discrimination.

**Verdict: the committed control re-scores at exactly 3/9 on both fresh seeds — as
predicted. No finding against P1's discrimination on the committed control.
BUT a MEETS-class finding surfaced: the counter's S6/S7/S8 scenarios can be
satisfied by gates that perform no provenance verification at all, and a gate
that verifies one binary and then runs a *different* binary for every matcher
call also scores 9/9. Details in §3/§4.**

---

## 1. Pinned inputs (sha256, all read-only)

| object | sha256 | verified |
|---|---|---|
| `tools/research-gate.sh` (at session start) | `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` | matches the wave spec exactly |
| `controls/ctl-c1-hardcoded-grep.sh` | `05bdf6543858a551852b6b9725d4cd327140f8d94589ae87ce82c5232248a378` | matches the committed receipt `c1-hardcoded-s3501.json` |
| `repairs/base-gate.sh` (round-34 blob) | `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` | matches the wave spec |
| `corpus/evidence/round35/c1-count.py` | `da207fd725658b84469ce1fe540a7b94fcb1027cef49da376a8d7ac19ac715e3` | equals `git show HEAD:...` — counter not edited |

`diff repairs/base-gate.sh controls/ctl-c1-hardcoded-grep.sh` = 4 added lines only
(`GREP_BIN=/usr/bin/grep` + `grep() { command "$GREP_BIN" "$@"; }` + comment/blank),
so the control is exactly "base gate plus a hardcoded pin", as claimed.

## 2. Re-score of the committed control (the assigned task)

```
C1_TMP=/tmp/hyaku/chousa-r35/w2/ExecC1Control \
python3 corpus/evidence/round35/c1-count.py \
  --gate .ufo/waves/round-35/controls/ctl-c1-hardcoded-grep.sh \
  --seed 3529 --receipt .ufo/waves/round-35/w2/ExecC1Control/c1-hardcoded-s3529.json
```
exit=1, stdout `GREP_PIN_MATCH=3/9`, receipt `predicate_holds=false`,
`reference_sane=true`, `gate_sha256=05bdf654…a378`.

| scenario | seed 3529 | seed 3539 |
|---|---|---|
| S1 shim-first PATH | **PASS** (tripwire 0 B) | **PASS** (tripwire 0 B) |
| S2 BASH_ENV function shim | **PASS** (tripwire 0 B) | **PASS** (tripwire 0 B) |
| S3 grep absent from PATH | **PASS** (rc=1, 38 path tools) | **PASS** (rc=1) |
| S4 override relative | FAIL (rc=1, no marker) | FAIL |
| S5 override missing | FAIL (rc=1, no marker) | FAIL |
| S6 override non-GNU | FAIL (rc=1, no marker, stub_calls=0) | FAIL |
| S7 override real + echo | FAIL (no `GATE_GREP:` line) | FAIL |
| S8 default + echo | FAIL (no `GATE_GREP:` line) | FAIL |
| S9 override beats shim | FAIL (no echo line; tripwire 0 B) | FAIL |

**Result: 3/9 on seed 3529 and 3/9 on seed 3539.** Not above 4 → no finding
against P1's discrimination. Stable: 3/9 on six further seeds (3521, 3531, 3533,
3541, 3547, 3551, 3601, 3611), 9/9 for the landed gate on every one of those
seeds. Receipts in my directory.

**What the hardcoded pin wins:** exactly S1–S3, i.e. the *resolution* half of
the claim — it never consults `PATH` (S1's shim tripwire stays empty), it is
immune to a `BASH_ENV` `grep()` function (S2 tripwire empty), and it runs with
no grep at all on `PATH` (S3, rc=1). **What it cannot:** every *refusal* and
every *naming* scenario — S4/S5/S6 (no exit-2 `GREP_PROVENANCE` refusal; the
control ignores `RESEARCH_GATE_GREP` entirely) and S7/S8/S9 (no `GATE_GREP:`
line naming path/source/version).

Attribution of the 3 wins (built and named by me, in my directory):
`probe-attr-pin-nowrapper.sh` (absolute pin recorded, **no** `grep()` wrapper)
→ **0/9**; `probe-attr-wrapper-nopin.sh` (wrapper present but `GREP_BIN=grep`,
i.e. still PATH-resolved) → **1/9** (S2 only: the wrapper's own `command` call
beats the `BASH_ENV` function, but `PATH` shim and no-grep-on-PATH both fail).
So the control's 3 points come from *both* the absolute path *and* the
`grep()`-function wrapper that routes every call site through it — the pin
alone is worth nothing (0/9), and the wrapper alone is worth 1/9.

## 3. MEETS finding #1 — a gate with NO provenance verification scores 9/9

`probe-hardcoded-echo.sh` (sha256 `e0635ae873ab3e87ab276ef21e7b5d77b9396611f5411934ecea3fc8edc54ffa`)
is the committed control plus: an override branch that refuses a relative path
/ non-file / non-executable candidate, refuses any candidate whose path is not
literally `/usr/bin/grep`, and prints a **hardcoded literal** echo line
`GATE_GREP: path=/usr/bin/grep source=<default|override> version="grep (GNU grep) 3.12-modified"`.
It **never runs `--version` on anything** (`grep -n -- '--version'` on the file
yields only comment lines).

```
python3 corpus/evidence/round35/c1-count.py --gate <probe-hardcoded-echo.sh> --seed 3529 …
GREP_PIN_MATCH=9/9   (exit 0, predicate_holds=true)
```
Reproduced at seeds 3539 and 3601 — 9/9 each.

Why P1 does not catch it: the counter checks the echo line as a **string**
(`"path=%s" % REAL_GREP in line and "source=override" in line and "GNU grep" in line`,
`c1-count.py:254` and `:261`) and checks S6 only for `rc == 2 and
"GREP_PROVENANCE" in err` (`c1-count.py:244`). Neither asks *where the version
string came from*. The landed gate computes it from `"$cand" --version`
(`tools/research-gate.sh` at the base blob, line 361); the probe hardcodes it.

Sharper variant `probe-liar-echo2.sh` (sha256 `763373a353f85bd2d3b37bed3fab32d21b3787f7257f76d458ae61af966e0dd9`)
is the decisive one: its **default pin is a wrapper that reports itself as
`grep (pi-uu-grep) 0.2.0`** (i.e. explicitly *not* GNU grep), yet the gate
prints `GATE_GREP: path=/usr/bin/grep … version="grep (GNU grep) 3.12-modified"`.
**9/9 on seeds 3529, 3539, 3601.** `probe-liar-echo3.sh` (sha256
`181d971c53e0298a30937e2b6655dffd9983032e5b9f9435d0259966d450af9f`) repeats it
with a logging wrapper: **9/9**, and the log proves **25 matcher calls were
actually served by the non-GNU binary** (`liar-calls.log`, e.g.
`-a -z -b -o -P -- \x61\x6c…`) while the receipt claims GNU grep 3.12.
So the receipt's `GATE_GREP:` line can be a fabrication that the counter
certifies.

## 4. MEETS finding #2 — verify one binary, run another: still 9/9

`probe-verify-then-substitute.sh` (sha256 `025cec2417a24f1e2def1ff7e403e906fa2d3b39605fc51932f3b712c3385760`)
takes the **landed** gate verbatim and only appends one line after the pin
resolves and the echo is printed:
`GREP_BIN=/tmp/hyaku/chousa-r35/w2/ExecC1Control/evilgrep` (a byte copy of
`/usr/bin/grep`, sha256 `19280b0e0714dadf0c100cdbc7f4823d254dd8facba64deeff5ec50d39fecf84`).

```
GREP_PIN_MATCH=9/9  (exit 0)   seeds 3529, 3539, 3601
```
`probe-verify-then-logging.sh` (sha256 `0fd9cc1dd79f85f3175cd82d5f055a33b1bf9a1275aaff19e2040a5b043813bd`)
does the same with a logging wrapper: **9/9**, and one counter run produces
**35 matcher calls through the substitute** (`substitute-calls.log`:
`-a -z -b -o -P -- x`, `-Fn -m1 -e charlie`, …) — i.e. every `tok_span_offsets_*`
/ `tok_span_at` call went to the *other* binary, and the counter still says the
gate pinned and used one grep.

The tripwires in S1/S2 watch for a *PATH* shim and a *BASH_ENV function*; they
cannot see a substitution to a third absolute path. Rebuilt against the
**concurrently-landed** gate (sha256 `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`,
which replaced the `command`-based wrapper with `grep_pin_define`), the
substitute probe still scores **9/9** with the same 35 substitute calls
(`probe-newgate-verify-then-substitute.sh`, sha256
`9dc2140e3c00aa2eef65173cf5bc8d52165503dcbb9e34212817c5861ebf9811`).

**Why this matters for P1:** the claim (claims.md, C1) is that the gate
"resolves, verifies and pins **one** grep binary … and refuses a pin it cannot
verify". The counter's nine scenarios verify *refusal behaviour and echo
naming*, never *which binary actually served the match*. A gate can satisfy all
nine while the matcher runs a different, unverified binary. The counter is
therefore blind to the one thing the C1 surface names ("grep-binary provenance
at **every matcher call site**").

## 5. MEETS finding #3 — the S6 stub prints its version to stderr, so S6 cannot test version-text discrimination

The counter's own S6 fixture (`c1-count.py:118`) writes the non-GNU version to
**stderr**:
`case "$1" in --version|-V) printf '%s\n' >&2; exit 0;; esac`.
Reproduced by importing the counter's own `write_stub_non_gnu`: `--version`
yields `stdout='' stderr='grep (pi-uu-grep) 0.2.0\n'`. The landed gate reads
`v=$("$cand" --version 2>/dev/null | head -n 1)` (base blob line 361), so it
sees an **empty** stdout and refuses with `<no version>` — it never actually
compares the text `pi-uu-grep 0.2.0`. A gate that accepts any override whose
`--version` stdout is merely **non-empty** (`probe-empty-version.sh`, sha256
`99465939754b1614696c016fd5c36402742ccea041cf1ee450ce55f7f7050fa3`) therefore
scores **9/9** — while the *real* discrimination is lost: given a wrapper that
reports `grep (pi-uu-grep) 0.2.0` on **stdout**, the probe accepts it and runs
it (`stdout-stderr-evidence.txt`; probe rc=0, `RESEARCH_GATE: CLEAN`) whereas
the landed gate refuses it (rc=2, "does not report GNU grep: grep (pi-uu-grep) 0.2.0").

So S6 currently scores "the gate refused *something* with the marker" and does
**not** score "the gate compared the version text". A stdout-reporting stub
would close this; the committed stub cannot.

## 6. Other probes (negative controls, for completeness)

| probe | score | note |
|---|---|---|
| `probe-always-refuse.sh` (always exit 2 + marker) | 6/9 | reference run not sane → `predicate_holds=false`, exit 1. Correctly killed. |
| `probe-pin-echo-only.sh` (pin + echo, no override) | 4/9 | S8 passes, S7/S9 need `source=override`. |
| `probe-pin-echo-noverify.sh` (pin + override + echo, no GNU check) | 8/9 | S6 alone fails. |
| `probe-default-liar.sh` (non-GNU default, honest echo) | 4/9 | S8 fails — the echo names the wrong path, so the counter does catch *that* lie. |

## 7. Note on a concurrent change (not mine)

At 17:07:40 local, `tools/research-gate.sh` changed under me: sha256
`1f2fb4f5…ef617` → `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`
(`git diff HEAD` showed the `grep_pin_define` rewrite, the `timeout`-bounded
`--version` probe, and the removal of the `command -v grep` fallback). A sibling
then committed it (`beb04ea`, "round-35: pin hardened (command/head/PATH-fallback/
readonly/bounded probe)"), and the lane tip moved to `770a69d`. I did not edit
the gate.

**Both** the spec-pinned blob and the committed final blob score **9/9** on
seeds 3529 and 3539 (`c1-landed-s3529.json`, `c1-landed-s3539.json` vs
`c1-newgate-s3529.json`, `c1-newgate-s3539.json`), and **every finding in §3–§5
reproduces against the committed final gate as well**:
- §3 `probe-finalgate-liar-echo.sh` (sha256 `9006db3b4b4ee925afec1c1c42da43ad8d895889adfb0373c9e367a006f8ad1a`)
  is the committed final gate with its whole `grep_pin_init` replaced by a
  **no-verification** block whose default pin is the **non-GNU**
  `liarloggrep.sh`: **9/9**, and `liar-calls.log` shows **25 matcher calls
  actually served by the non-GNU binary** while the receipt claims GNU grep.
- §4 `probe-newgate-verify-then-substitute.sh`: **9/9** with 35 substitute
  matcher calls.

The committed gate's own hardening (`grep_pin_define`, the `timeout`-bounded
probe) does not close these counter-discrimination gaps, because they are gaps
in what the nine scenarios *observe*, not in the gate's implementation.

## 8. Limits

- All C1 work is on short-span claims in the counter's own fixture; the
  long-span / `slen` surface is untouched by this seat.
- The §3–§5 findings are *counter-discrimination* findings, not defects in the
  landed gate: the landed gate does compute its version from the candidate and
  does refuse a non-GNU override. They show that **P1 cannot certify** those
  properties, so a 9/9 receipt alone is not evidence that a given gate
  verifies provenance or uses the binary it names.
- The §4 substitution probes substitute a *byte-identical copy* of GNU grep
  (or a wrapper around it), so they are output-equivalent; a substitution to a
  behaviourally different binary would show up in the output-equality checks.
  The point stands regardless: nothing in S1/S2/S9 observes the identity of
  the binary that served the match.
- I did not modify any production file, the counter, or the witness tool. No
  installs were needed. All probes and receipts live in
  `.ufo/waves/round-35/w2/ExecC1Control/` (largest file 372 KB, all < 1 MiB);
  the two large logs (`substitute-calls.log`, `liar-calls.log`) are also copied
  there and remain in `/tmp/hyaku/chousa-r35/w2/ExecC1Control/`.

## 9. Artifacts (all in `.ufo/waves/round-35/w2/ExecC1Control/`)

Receipts: `c1-hardcoded-s3529.json`, `c1-hardcoded-s3539.json`,
`c1-hardcoded-s{3531,3547,3601}.json`, `c1-landed-s{3529,3539}.json`,
`c1-newgate-s{3529,3539}.json`, `c1-base-s3529.json`, `sweep-{ctl,landed}-s*.json`,
`probe-*.json` for every probe above.
Probes: `probe-hardcoded-echo.sh`, `probe-liar-echo{,2,3}.sh`,
`probe-verify-then-{substitute,logging}.sh`,
`probe-newgate-verify-then-substitute.sh`, `probe-empty-version.sh`,
`probe-always-refuse.sh`, `probe-pin-echo-{only,noverify}.sh`,
`probe-default-liar.sh`, `probe-attr-{wrapper-nopin,pin-nowrapper}.sh`,
plus `liargrep.sh`, `liarloggrep.sh`, `stdouthgrep.sh`, `loggrep.sh`,
`evilgrep`, `stdout-stderr-evidence.txt`, `liar-calls.log`,
`substitute-calls.log`, `gate-base-1f2fb4f5.sh`.
