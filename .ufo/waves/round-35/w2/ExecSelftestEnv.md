# ExecSelftestEnv — locale re-measure of `--selftest` (round 35, wave 2)

Seat: read-only attack seat. Scored blob is the wave-base revision `e87c5d7ea2dbf3730b36a3961de3f06261d015e4`;
nothing under `tools/`, `corpus/`, `.ufo/waves/round-35/{controls,measure,repairs}/` or any git/jj state was
written by this seat. No network. No installs (none needed; `bash 5.3.20`, `grep (GNU grep) 3.12-modified`).
All experiments in `/tmp/hyaku/chousa-r35/w2/ExecSelftestEnv/`.

## 1. Pinned blobs (hashed before any run)

| blob | path | sha256 |
|---|---|---|
| landed gate @ `e87c5d7` | `git clone` + `checkout -q e87c5d7…` → `clone/tools/research-gate.sh` | `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` ✓ = the brief's pin |
| pre-round gate | `.ufo/waves/round-35/repairs/base-gate.sh` | `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` ✓ = the round-34 blob |
| same pre-round blob, in-tree | `clone-base/tools/research-gate.sh` @ `08be4c9e3a4ebe55d915ce4761c81854286c23ae` | `a6307edf…995b` (identical) |
| round-34 attempt-1 base (for the disclosure comparison) | `git show a92b9f4:tools/research-gate.sh` | `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346` |

Commands are `LC_ALL=C bash <blob> --selftest` (and `LC_ALL=en_US.UTF-8` as the default-locale control), each
under `timeout 900`; the selftest is deterministic — two independent landed runs gave the same 10 names
(`diff names-landed-C.txt names-landed-C2.txt` empty).

## 2. Failing case names (LC_ALL=C)

**Landed gate `1f2fb4f5`, in-tree clone — `FAIL (10/256 cases)`, exit 1.** The ten names, in report order
(case numbers from the surrounding `ok-case` sequence):
`21 claims-pass`, `55 all-pass.md`, `57 all-structure.md`, `59 claims-pass.jsonl`, `60 all-pass.md`,
`61 all-pass.md`, `62 all-meta.md`, `74 all-dangling.md`, `134 json-unterminated-manifest`,
`135 json-nul-terminated-manifest`.

**Pre-round gate `a6307edf` at its committed path — `FAIL (12/256 cases)`, exit 1.** The same ten plus
`106 claims-lane-fallback` and `127 ptr-lane-abs`.

**Pre-round gate `a6307edf` in-tree (`clone-base`) — `FAIL (10/256 cases)`**, name set byte-identical to the
landed set (`diff names-landed-C.txt names-baseclone-C.txt` empty).

So the literal target command on `repairs/base-gate.sh` reads **12**, not 11 — and the two extra names are a
property of *where the blob sits*, not of the blob. `LANE_ROOT` is the parent of the script dir
(`clone/tools/research-gate.sh:313`, `LANE_ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd)`), so a blob in
`.ufo/waves/round-35/repairs/` has `LANE_ROOT=.ufo/waves/round-35/`, which carries no `PROVINCE.md`. Staging
matrix, all `LC_ALL=C`, all on blob `a6307edf` unless noted:

| staging | result | extra names vs the 10 |
|---|---|---|
| in-tree clone (`PROVINCE.md` readable) | 10/256 | — |
| copy + `PROVINCE.md` + `corpus` symlink | 10/256 | — |
| `PROVINCE.md` present but `chmod 000` | 11/256 | `claims-lane-fallback` |
| no `PROVINCE.md` (repairs/ layout) | 12/256 | `claims-lane-fallback`, `ptr-lane-abs` |
| `PROVINCE.md` dangling symlink | 12/256 | same two |
| landed blob `1f2fb4f5`, no `PROVINCE.md` | 12/256 | same two |

Control on the last row: the *landed* gate staged without `PROVINCE.md` gives the identical 12
(`diff names-base-C.txt names-st-noprov.txt` empty), proving the delta is staging, not the pin. The
mechanics are visible in the output: `FINDING CLAIM_SOURCE_MISSING … source=PROVINCE.md … not a readable
regular file under allowed roots` and `FINDING POINTER_UNRESOLVED … missing under CHOUSA_ROOT`
(`selftest-base-C.out` lines 179–184, 205–209).

## 3. Comparison with the round-34 disclosure (base 11 / landed 10)

The disclosed pair is **not** the round-35 pair: round-34's base was `43a1af35` (251 cases) and its landed
`772a1d8e` (253 cases); the round-35 "base" is the round-34 *landed* blob `a6307edf` (256 cases). Re-derived
by staging `43a1af35` three ways under `LC_ALL=C`:

| `43a1af35` staging | result |
|---|---|
| readable `PROVINCE.md` | 10/251 |
| `PROVINCE.md` `chmod 000` | **11/251** — names byte-identical to committed `round-34/measure/selftest-env/base-C.log` (`diff` empty) |
| no `PROVINCE.md` | 12/251 |

So the disclosed **11** reproduces exactly, and it is a `PROVINCE.md`-readability artifact (the pointer arm
needs only `-f`, `clone/tools/research-gate.sh:773`; the claims arm needs `-f && -r`, `:1531`), not
a gate difference. Landed 10 reproduces too: my landed name set is byte-identical to the committed
`round-34/measure/selftest-env/landed-C.log` set (`diff` empty). Default locale: landed `PASS (256 cases,
0 skipped)` and in-tree base `PASS (256 cases, 0 skipped)` — the round-34 finding holds.

**The "base 11 vs landed 10" delta is not reproducible as a gate difference in round 35.** Under matched
staging the two round-35 blobs are equal at every point of the matrix: **10 vs 10**, **11 vs 11**
(`PROVINCE.md` `chmod 000`: `FAIL (11/256)` for both, `diff names-st-noread-landed.txt names-st-noread-base.txt`
empty), **12 vs 12**.

## 4. Does the grep pin change the count or the failing set? No.

- Matched in-tree staging: base (no pin) 10/256, landed (pin) 10/256, identical name sets.
- `chmod 000` staging: base 11/256, landed 11/256, identical sets.
- Default locale: both `PASS (256 cases, 0 skipped)`.
- PATH control: with a logging shim first on `PATH`, the **base** gate made **1443** shim invocations; the
  **landed** gate made **0** (its pin runs `/usr/bin/grep` through the wrapper). Both runs still produced the
  same 10-name failing set. The pin moves provenance only.
- The pin itself is locale-stable: `GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep)
  3.12-modified"` under both `LC_ALL=C` and `en_US.UTF-8`.
- Bonus, because the lane HEAD moved under me mid-wave (`git rev-parse HEAD` = `038543b208be2d87d01985b9e0aa60771b909d71`,
  `tools/research-gate.sh` now `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`, a hardened
  pin that stops calling through `command` and `head`): that newer blob, staged identically, also gives
  **`FAIL (10/256 cases)` with the same 10 names** (`diff names-landed-C.txt names-new-C.txt` empty). My
  scored blob remains the brief's `1f2fb4f5` clone copy.

## 5. Is any dead-zone case locale-dependent?

**No selftest case is.** Cases `252–256` (`claims-longspan`, `claims-longspan-line`, `claims-deadzone`,
`claims-deadzone-line`, `claims-deadzone-edge`) are all `ok-case … exit=1` in every `LC_ALL=C` run of every
blob above (`selftest-landed-C.out:344-348`), and the whole selftest passes in `en_US.UTF-8`. Their fixtures
are pure ASCII (`w%04d ` runs, `clone/tools/research-gate.sh:7899-7969`), so no decode is involved.

**But the dead-zone *routing* is locale-dependent, and that is a live hole.** The ten `LC_ALL=C` failures are
one cause, unchanged from round 34: the claims fixture's `P4` span is the JSON escape `\u2192`
(`clone/tools/research-gate.sh:4120`) against raw UTF-8 arrow bytes (`:4106`), and `json_unescape`
(`:1398-1449`) decodes `\uXXXX` with `printf -v c '%b' "\u$hex"`, which honours `\u` only in a UTF-8 locale.
Measured primitives: `LC_ALL=C` → `5c 75 32 31 39 32` (the literal six bytes), `en_US.UTF-8` → `e2 86 92`.
`grep -c 'obs=id=P4'` = **10** in both the landed and the base `LC_ALL=C` logs, i.e. all ten failures.

`json_unescape` is the only decode step **not** wrapped in `LC_ALL=C`, while every matcher is
(`tok_span_offsets` `:1662` + `:1665`, `_direct` `:1677`, `_chunk` `:1690` + `:1699`). Consequence: the span
length that picks the direct vs chunk matcher (`TOK_DIRECT_SPAN_MAX=32764`, `:1650`) is measured from
locale-dependent bytes. Two probes on the **landed** gate show the same fixture flipping verdict by locale:

- `dz2`: span = 32760 `w` + `\u2192`; source holds the real arrow. `LC_ALL=C` → decoded span stays literal
  (32766 bytes) → chunk path → `observed=unsupported`; `en_US.UTF-8` → 32763 bytes → direct path →
  `observed=supported`.
- `dz4`: span = 32759 `w` + `\u2192`; source holds the *literal text* `\u2192`. `LC_ALL=C` → 32765 bytes →
  chunk (dead-zone) path → `observed=supported`; `en_US.UTF-8` → 32762 bytes → direct path →
  `observed=unsupported`.

The matcher itself is byte-safe: `grep -P 'x\xff\xfey'` returns rc 0 under `LC_ALL=C` and rc 1 under
`en_US.UTF-8` (PCRE UTF mode rejects invalid UTF-8), but the gate's function-local `LC_ALL=C` neutralises it —
a span of raw `\xff\xfe` reads `observed=supported` in **both** locales (`iu` probe).

## 6. Verdict for this item

Re-measured and **confirmed with one correction to the disclosure framing**: under `LC_ALL=C` the landed gate
`1f2fb4f5` fails **10** cases and the pre-round gate `a6307edf` fails the **same 10** names when staged
alike; run at its committed `repairs/` path the pre-round gate reports **12**, and the round-34 disclosed
**11** is reproduced exactly only when `PROVINCE.md` sits beside the blob and is unreadable. **The grep pin
changes neither the count nor the failing set** (10/10, 11/11, 12/12 in three matched stagings; shim call
counts 1443 vs 0 with identical failing sets). **No dead-zone selftest case is locale-dependent** — all five
long-span/dead-zone cases pass in both locales — but the dead-zone boundary itself is: because
`json_unescape` runs under the ambient locale, a span carrying a `\uXXXX` escape near 32764 bytes takes a
different matcher and can flip `observed=supported`/`unsupported` between `LC_ALL=C` and UTF-8 (dz2/dz4).

## 7. Limits

- The `11`/`12` split is a staging property I established with six stagings, not a code reading of why
  round-34's own staging looked the way it did; I did not reconstruct the round-34 staging directory.
- The dead-zone routing claim is a source reading of `json_unescape` plus two end-to-end probes per
  direction; I did not instrument which matcher ran (that is the witness tool's job, out of this item).
- The lane moved under me: `HEAD` is now `038543b2` / `a4768851`. Everything scored above is bound to the
  brief's pinned `1f2fb4f5` (verified by `sha256sum` on the clone before and after the runs).
- Single-run counts per staging, except the landed `LC_ALL=C` pair, which I ran twice with identical output.

## 8. Artifacts (my directory only, each < 1 MiB, `SHA256SUMS.txt` over all)

`.ufo/waves/round-35/w2/ExecSelftestEnv/` — `selftest-landed-C.out`, `selftest-landed-C2.out`,
`selftest-landed-default.out`, `selftest-base-C.out`, `selftest-base-C-tmpd.out`, `selftest-baseclone-C.out`,
`selftest-baseclone-default.out`, `selftest-base-default.out`, `st-base-C.out`, `st-noprov-C.out`,
`st-dangling-C.out`, `st-noread-landed-C.out`, `st-noread-base-C.out`, `selftest-r34base-C.out`,
`selftest-r34base-prov-C.out`, `selftest-r34base-noread-C.out`, `selftest-new-C.out`, the `names-*.txt` sets,
`probe-dz2.txt`, `probe-dz4-dz3-iu.txt`, `probe-locale-primitives.txt`, `SHA256SUMS.txt` (37 files, 496 KiB).
Raw originals stay in `/tmp/hyaku/chousa-r35/w2/ExecSelftestEnv/`.
