# ExecPerfProfile — r34 C1 base-gate performance profile (long-span records)

**Seat:** `ChousaR34.ExecPerfProfile` (wave 1, exec lane).
**Scope:** where wall time goes on the **base gate** (`tools/research-gate.sh`, sha256
`43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`) for long-span
records. **No counter was run** against any gate — no candidate was built, no
`ExecC1Build*` patch exists, no receipt was produced. Everything below is the base
gate on my own fixtures.
**Verdict in one line:** the base gate's long-record cost is **not** in grep, not in
`count_nl`/`line_probe`, and not in memory — it is two **per-byte bash loops that are
quadratic in span bytes** (`${s:i:1}` substring extraction, ~9.3 s per 64 KiB span just
to read it), and a counter-shaped 30-record fixture therefore takes **1234 s** of the
counter's 1500 s budget on the base gate.

---

## 1. Method

* Scratch dir: `/fast/scratch/hyaku/chousa-r34/w1/ExecPerfProfile/`
  (fixture generator, PROF logs, gate stdout/stderr). Nothing was written to the lane
  repo, the fleet repo, or any sibling directory. No git/jj write command was run.
* The instrumented gate is a **copy** of the landed gate plus timers only
  (`gate-instr.sh`, sha256 `d7ddacb5e16b61186fd7da2fd8d4621e48f631d1cd1f9dc042191d6bc7c809dc`).
  **Fidelity check:** on the same 32 KiB fixture the pristine gate and the instrumented
  copy produce byte-identical stdout and stderr except the `ts=` timestamp and the
  script name inside the grep error line:
  `diff logs/pristine32768.out logs/instr32768.out` → only line 1 (`ts=…`) differs;
  `diff logs/pristine32768.err logs/instr32768.err` → only the script path differs.
* Timers use bash's `EPOCHREALTIME` (microseconds) via `prof_dt LABEL START`.
  Stage boundaries: `claims.scan_secrets`, `record.claim_scan`,
  `record.span_unescape` / `record.field_extract`, `record.source_read`,
  `tok_span_at.hexloop` / `tok_span_at.matchloop` / `tok_span_at.total`,
  `tok_span_all.*`, `count_nl`, `line_probe`, `record.miss_path`, `record.total`.
* Fixtures: one source file of letters/spaces/newlines holding the span **verbatim**,
  and one claims JSONL with **exactly one** record citing it
  (`{"id","source","span","expect":"supported"}`), for span sizes
  4 KiB / 8 KiB / 16 KiB / 32 KiB / 33 KiB / 48 KiB / 64 KiB.
* **Load caveat:** the host is shared; `/proc/loadavg` was 18–65 on 32 cores during
  the runs (other lanes). Absolute seconds therefore carry ±2x noise between
  batches. Ratios within a batch (same batch, same load) are the trustworthy
  numbers, and the exponent fits are.

### Base-gate behaviour reproduced (the defect itself)

`logs/err33792.txt`:

```
gate-instr.sh: line 1575: /usr/bin/grep: Argument list too long
```

`logs/out33792.txt`:

```
CLAIM id=P033792 expected=supported observed=unsupported source=src/span033792.md at=- verdict=mismatch
FINDING CLAIM_SPAN_NOT_FOUND severity=warn surface=claims obs=id=P033792 nearest_line=3 …
VERDICT_BEARING_CLAIMS=0/1
RESEARCH_GATE: DRIFT (claims=1 supported=0 … mismatched=1 …)
```

So the span **is** in the source verbatim, yet the base gate reads
`observed=unsupported` — the r34 C1 defect, reproduced on my own fixtures.

---

## 2. Wall time per stage, per span size

Base gate, one record per run, **ambient locale** (`LANG=en_US.UTF-8`, `LC_ALL` unset),
`prof/prof*.log`:

| span bytes | record.total | span_unescape | hexloop | claim_scan | source_read | matchloop (grep) | count_nl | line_probe | miss_path |
|---|---|---|---|---|---|---|---|---|---|
| 4 100 | 0.518 s | 0.294 s | 0.132 s | 0.020 s | 0.003 s | 0.019 s | 0.010 s | – | – |
| 8 196 | 1.556 s | 1.001 s | 0.399 s | 0.043 s | 0.007 s | 0.024 s | 0.011 s | – | – |
| 16 384 | 4.001 s | 2.985 s | 0.671 s | 0.167 s | 0.006 s | 0.033 s | 0.016 s | – | – |
| 32 773 | 21.373 s | 15.240 s | 5.377 s | 0.474 s | 0.004 s | 0.008 s | 0.006 s | 0.012 s | 0.014 s |
| 33 795 | 22.362 s | 16.242 s | 5.006 s | 0.680 s | 0.009 s | 0.006 s | 0.006 s | 0.012 s | 0.014 s |
| 49 154 | 45.535 s | 33.015 s | 10.244 s | 1.672 s | 0.005 s | 0.004 s | 0.008 s | 0.010 s | 0.015 s |
| 65 536 | 78.998 s | 58.707 s | 18.127 s | 1.370 s | 0.004 s | 0.007 s | 0.012 s | 0.019 s | 0.027 s |

(`prof/prof4096ml.log`, `prof8192ml.log`, `prof16384ml.log`, `prof32768ml.log`,
`prof33792.log`, `prof49152.log`, `prof65536.log`.)

**Reading of the table.** At a 64 KiB span, 78.998 s of the record is split
**58.707 s `json_unescape` + 18.127 s hex-pattern build = 76.8 s (97.2 %)**. The
actual matching stage (`grep` exec) is **7 ms** — 0.009 % of the record. `count_nl`
(12 ms) and `line_probe` (19 ms) are also negligible, and `claim_scan` (1.37 s) is
third but 43x smaller than the unescape.

**`count_nl` and `line_probe` specifically (asked for):** both are effectively free.
`count_nl` is 1.5–12 ms regardless of haystack size (it is `tr -dc '\n' | wc -c`,
linear); `line_probe` is 2–27 ms. Neither is a scaling risk. The one place
`count_nl` gets called on a long string is `tok_span_at`'s `TOK_L1`/`TOK_L2`
computation (on `before` and on `span`), and that only runs on the *match* path —
which the base gate never reaches for long spans because grep never executes.

### Is any stage superlinear? — yes, two of them, both ≈ quadratic

Log-log fits (`fix/fit.py`, `logs/fit.txt`), exponent `p` in `t ∝ span^p`:

```
record.span_unescape
   span 16384 -> 32773  t 2.985 -> 15.240  ratio 5.10x  exponent p=2.35
   span 32795 -> 49154  t 16.242 -> 33.015 ratio 2.03x  exponent p=1.89
   span 49154 -> 65536  t 33.015 -> 58.707 ratio 1.78x  exponent p=2.00
tok_span_at.hexloop
   span 32795 -> 49154  t 5.006 -> 10.244  ratio 2.05x  exponent p=1.91
   span 49154 -> 65536  t 10.244 -> 18.127 ratio 1.77x  exponent p=1.98
tok_span_at.matchloop   p≈0 (0.004–0.033 s, flat)
record.claim_scan       p≈1.2 (0.020 s -> 1.37 s over 16x bytes; sub-quadratic)
```

`p ≈ 1.9–2.0` on the two hot stages over the 32 KiB–64 KiB band. Below ~16 KiB the
exponent is lower (~1.6) because fixed costs still dominate; the quadratic term only
becomes visible above ~30 KiB — which is exactly the band C1 is about.

### Which operation is superlinear (root cause)

`fix/whichop.sh` / `logs/whichop.txt`, LC_ALL=C, isolated bash loops over a span of
the given size:

| operation | 16 384 B | 65 536 B | growth |
|---|---|---|---|
| read span into a var | 0.003 s | 0.003 s | flat |
| **A: substring read only `c=${s:i:1}`** | **0.497 s** | **9.323 s** | **18.7x for 4x bytes** |
| B: append only `out+=$c` | 0.023 s | 0.090 s | 3.9x |
| C: substring + append | 0.479 s | 9.456 s | 19.7x |
| D: json_unescape shape | 0.480 s | 9.039 s | 18.8x |
| **E: hex build (`printf -v hex` + `regex+=`)** | **0.506 s** | **8.534 s** | **16.9x** |
| F: hex build without `printf` (constant hex) | 0.027 s | 0.092 s | 3.4x |

**`${s:i:1}` is the culprit.** Extracting one character at offset *i* copies/skans the
remaining string, so a per-byte loop is O(n²). The `printf -v hex` inside the hex loop
is *not* the cost (row F vs row E: 0.092 s vs 8.534 s at 64 KiB); the cost is the same
`${span:i:1}` shape that `json_unescape` uses. Both hot stages are the same defect
wearing two hats:

* `tok_span_at` hex loop — `tools/research-gate.sh:1587-1591` (landed file):
  `c=${span:i:1}` then `printf -v hex` then `regex+="\\x$hex"`.
* `json_unescape` — `tools/research-gate.sh:1332-1333`: `c=${s:i:1}` per byte.

---

## 3. The 1500 s counter budget — measured, not extrapolated

A counter-shaped 30-record fixture (24 long spans 32 774–64 456 B, 6 short) was built
by **importing the frozen counter's generator read-only** (`fix/gen_counter_fixture.py`;
the counter module is imported and `generate()` is called — the counter is never run
and never edited) at seed 73501. The **base gate** was then run on it:

```
$ bash fix/run_cf.sh fix/cf73501 cf73501
tag=cf73501 rc=1 wall_s=1234.129
$ tail -3 logs/cfoutcf73501.txt
VERDICT_BEARING_CLAIMS=3/30
RESEARCH_GATE: DRIFT (claims=30 supported=3 … mismatched=27 …)
```

**1234 s of the counter's 1500 s limit is spent by the base gate alone — 82 % of the
budget, before any candidate work.** Stage totals for that run
(`prof/profcf73501.log`, summed by stage):

| stage | n | total |
|---|---|---|
| record.total | 30 | 1 233 512.8 ms |
| record.span_unescape | 30 | 889 832.4 ms |
| tok_span_at.hexloop | 30 | 305 279.0 ms |
| record.claim_scan | 30 | 19 467.3 ms |
| record.miss_path | 27 | 1 337.2 ms |
| line_probe | 26 | 761.5 ms |
| record.source_read | 30 | 542.3 ms |
| tok_span_at.matchloop | 30 | 534.8 ms |
| count_nl | 32 | 411.5 ms |

Quadratic model check: `t ≈ 2.12e-8 · Σ(long span bytes)²` predicts 1231 s for
seed 73501 and 1191 s for seed 3401 — both close to the 1234 s measured, and both
inside the L1's recorded base receipt of "gate rc 1, 490 s" at seed 3401 only because
that receipt was measured on a **less loaded** host (or a shorter-span seed): my
seed-3401-shaped fixture projects 1191 s here. **The 1500 s bound is therefore
seed-sensitive and load-sensitive; it is not a comfortable margin.**

### A free 4x: locale

The gate's own `tok_span_at`/`tok_span_all`/`claim_scan` set `local LC_ALL=C`
(`tools/research-gate.sh:1140`, `1556`, `1586`) — but **`json_unescape` does not**
(`tools/research-gate.sh:1329`), so it runs in the ambient locale, and bash's
per-character `${s:i:1}` is markedly slower under a multibyte locale.

Controlled A/B on the **same** 64 KiB fixture, same batch, same load
(`prof/ab_*.log`):

| locale | wall | claim_scan | span_unescape | hexloop |
|---|---|---|---|---|
| `LC_ALL=C` rep1 | 15.50 s | 580.8 ms | 7 200.2 ms | 7 643.6 ms |
| `LC_ALL=en_US.UTF-8` rep1 | 27.22 s | 520.5 ms | 19 975.7 ms | 6 524.9 ms |
| `LC_ALL=C` rep2 | 13.60 s | 503.7 ms | 6 187.1 ms | 6 852.0 ms |

The unescape stage is **~3x slower** under `en_US.UTF-8`; the hex loop is not
(its function already forces `LC_ALL=C`). On the counter-shaped fixture:
**1234 s (ambient) → 302 s (`LC_ALL=C`)** — a 4.1x reduction of the whole run
(`prof/cf73501_C2.log`: span_unescape 147.3 s, hexloop 142.9 s, claim_scan 9.1 s,
everything else < 0.3 s).

> **Operational note for the counter seats:** the counter's subprocess env is
> `{k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}`
> (`corpus/evidence/round34/c1-count.py:274`), so it **inherits** `LC_ALL`/`LANG`.
> Exporting `LC_ALL=C` for the counter invocation is free, changes no matcher
> semantics (all fixtures are ASCII), and buys ~4x of headroom against the 1500 s
> bound. This is a measurement result, not a code change: I did not modify the gate
> or the counter. It also means **the base-gate control receipt's runtime is
> locale-dependent** — comparing 490 s to a later run is comparing different
> environments unless `LC_ALL` is pinned.

---

## 4. Ceilings that bound any candidate (measured)

`fix/limits.py` / `logs/limits.txt`:

```
(a) argv single-string ceiling (pattern = 4 x span bytes):
  span= 32000 pattern= 128000 bytes -> rc=0
  span= 32700 pattern= 130800 bytes -> rc=0
  span= 32766 pattern= 131064 bytes -> rc=2 grep: regular expression is too large
  span= 32767 pattern= 131068 bytes -> rc=2 grep: regular expression is too large
  span= 32768 pattern= 131072 bytes -> rc=OSError [Errno 7] Argument list too long: 'grep'
(b) PCRE2 compiled-pattern ceiling (same pattern, via -f file):
  max span compiling as -P -f: 32764 bytes (pattern 131056 bytes)
  next size (32765) -> rc=2 grep: regular expression is too large
```

Two independent walls, both *below* the 32768-byte floor of the C1 contract:

1. **Kernel `MAX_ARG_STRLEN`** (32 pages = 131 072 B) — a 32768-byte span produces a
   131 072-byte argv string and the exec fails with E2BIG. This is the base defect.
2. **PCRE2's own compiled-pattern ceiling** — even routing the *same* hex pattern
   through `grep -P -f patternfile` (no argv limit) fails at 32765 bytes with
   "regular expression is too large". **A 4-bytes-per-byte hex pattern cannot fix
   C1 at all**: it is capped at ~32 764 bytes, i.e. *below* the contract's lower
   bound. Any candidate must stop encoding the span as a PCRE pattern.

The contract band is 32768..65536 B, i.e. **entirely above both ceilings**.

---

## 5. Candidate cost — what the alternatives actually cost

Measured on a 64 KiB span present verbatim in a 66 KiB haystack
(`logs/candbench.txt`, `logs/bashmatch.txt`, `logs/bashnative.txt`):

| candidate primitive | 16 384 B | 65 536 B |
|---|---|---|
| `grep -a -z -b -o -F -f` (pattern file) | 0.002 s | 0.006 s |
| `python3 bytes.find` all occurrences | 0.000 s | 0.000 s |
| `python3 bytes.find` + boundary rule | 0.000 s | 0.000 s |
| bash `[[ $hay == *"$needle"* ]]` (whole-span glob) | 0.008 s | 0.012 s |
| bash prefix/suffix: `before=${hay%%"$span"*}` / `after=${hay#*"$span"}` | 0.516 s | 8.481 s |
| *base gate's current hex loop* | 0.671 s | 18.127 s |
| *base gate's current `json_unescape`* | 2.985 s | 58.707 s |

**Reading:** every candidate primitive is between **3 orders of magnitude** and
**~2 orders of magnitude** cheaper than the base gate's two hot loops. The
`grep -F`/python/bash-glob approaches are essentially free (≤ 12 ms at 64 KiB).

Two caveats a candidate author must not trip over:

* **`grep -F -f` with a multi-line span file is not a whole-span matcher.** A pattern
  file is *newline-separated patterns*, so a 64 KiB span of 836 lines becomes 836
  independent one-line patterns. Measured: `grep -a -z -b -o -F -f fix/span65536.txt`
  returns rc=0 on the haystack, and still returns rc=0 after the span file's **first
  line is replaced by `ZZZZZZNOTPRESENTZZZZ`** (`logs/…`, command in §7) — so it
  matched something that is not the span. A `-F -f` candidate must re-join the span
  into one pattern or verify the match.
* **The bash-only prefix/suffix candidate (`%%`/`#`) is itself quadratic**: 0.516 s at
  16 KiB → 8.481 s at 64 KiB (16.4x for 4x bytes). Bash's `%%` pattern removal
  scans per byte. It recovers the prefix/suffix and the *first* occurrence but not
  the *count* of occurrences, which the `line`-field classes need.

### What the counter needs from the matcher (per the counter docstring)

`corpus/evidence/round34/c1-count.py:33-62` requires: `long-line-bound` (2 records)
has **two** delimited occurrences with the named line being the second, and
`long-line-wrong` (2) has two with the named line being neither. So a candidate must
enumerate **all** occurrences, not just the first — `tok_span_at` alone is not enough,
and `tok_span_all` is called a second time from `verify_claims`
(`tools/research-gate.sh:1827`). **A candidate must fix both `tok_span_at` and
`tok_span_all`**, and each currently pays the hex build again — i.e. the base design
pays the quadratic loop **twice** for line-bearing records. Measured with the fully
instrumented copy on a 16 KiB span carrying a `line` field (`prof/linefull16384.log`):

```
tok_span_at.hexloop(spanlen=16384)        410.5 ms
tok_span_at.total(spanlen=16384)          418.9 ms
tok_span_all.hexloop(spanlen=16384)       404.3 ms
tok_span_all.total(spanlen=16384)         413.6 ms
record.total                            1298.5 ms
```

— the hex build is paid **twice** (410.5 + 404.3 ms), i.e. the second call is a
second quadratic term. At 32 773 B (`prof/linefull32768.log`) `tok_span_all` is never
reached: the base gate's `tok_span_at` fails first (grep E2BIG), so the record takes
the miss path instead — the double quadratic cost only materialises **once the
matcher is fixed**, which is exactly the state a candidate creates.

---

## 6. Answers to the specific questions asked

1. **Per-stage wall time and per span size** — §2 table (ambient locale) and §3
   (counter-shaped fixture, ambient vs `LC_ALL=C`).
2. **Is any stage superlinear?** — Yes: `json_unescape` and `tok_span_at`'s hex build,
   both **p ≈ 1.9–2.0** over 32–64 KiB. `claim_scan` is ~p=1.2, `count_nl` and
   `line_probe` are flat and negligible (1.5–27 ms), `grep`'s exec is flat (3–20 ms)
   because it never runs for long spans.
3. **Does this bound the counter's 1500 s limit?** — Yes, tightly: the **base gate
   alone** consumes **1234 s** (82 %) of the budget on a counter-shaped fixture at
   ambient locale; **302 s** with `LC_ALL=C`. Any candidate that keeps a per-byte
   `${s:i:1}` loop is already over budget before its own work.
4. **Which candidate?** — The evidence points at removing the per-byte bash loops
   entirely, not at re-encoding the span as a bigger pattern: the hex-pattern family
   is capped at 32 764 bytes by PCRE2 (below the contract floor), while
   `grep -F`/python/bash-glob primitives cost ≤ 12 ms at 64 KiB. A candidate must
   also enumerate *all* occurrences (`tok_span_all`), and must not use
   `grep -F -f` naively on a multi-line span.

---

## 7. Commands (reproduction)

```bash
cd /fast/scratch/hyaku/chousa-r34/w1/ExecPerfProfile
# one fixture per size, base gate, per-stage timings
python3 fix/gen.py fix/root65536 65536 ml 65543
PROF_LOG=$PWD/prof/x.log bash gate-instr.sh verify-claims fix/root65536/claims.jsonl --root fix/root65536
# size sweep
bash fix/sweep.sh 4096:ml 8192:ml 16384:ml 32768:ml 33792:ml 49152:ml 65536:ml
# counter-shaped 30-record fixture + base-gate timing
python3 fix/gen_counter_fixture.py fix/cf73501 73501
bash fix/run_cf.sh fix/cf73501 cf73501
# the same with LC_ALL=C
LC_ALL=C PROF_LOG=$PWD/prof/cf73501_C2.log bash gate-instr.sh verify-claims fix/cf73501/claims.jsonl --root fix/cf73501
# thresholds
python3 fix/limits.py
# root cause
bash fix/whichop.sh 65536
# candidate primitives
python3 fix/candbench.py 65536 ; bash fix/bashmatch.sh 65536 ; bash fix/bashnative.sh 65536
# exponent fit
python3 fix/fit.py prof4096ml.log prof8192ml.log prof16384ml.log prof32768ml.log prof33792.log prof49152.log prof65536.log
```

## 8. Limits and honesty

* **No counter was run** — not against the base gate, not against any control, not
  against any candidate. No `LONGSPAN_MATCH=` line was produced by me. The
  counter's generator was imported read-only to build a *realistic* fixture; the
  counter file was not edited and its sha256 is unchanged.
* **No candidate implementation of C1 was written.** §5 prices primitives, it does
  not build or score a fix.
* Absolute seconds are **load-noisy** (shared host, loadavg 18–65 / 32 cores);
  ratios and exponents within a batch are the sound numbers. The 1234 s / 302 s
  counter-fixture pair was measured in the same batch on the same fixture.
* `[INFERENCE]` The L1's recorded base receipt of "490 s" at seed 3401 is inconsistent
  with the 1191 s my seed-3401-shaped fixture takes on this host today; the most
  likely causes are host load and ambient locale, both of which I measured to move
  the same run by up to 4x. I did not run the counter to reproduce the 490 s, so this
  remains an inference.
* `count_nl`/`line_probe` were asked for explicitly; they are reported above as
  measured (negligible), and I did not find a path where they matter at long spans —
  on the base gate they are only reached on the miss path, because the match path
  never executes for a long span.
* No installs were performed; no tooling was upgraded. Everything used was already
  on the host (`bash 5.3.20`, `grep` (pi-uu-grep 0.2.0), `python3` 3.14).
* No process was signalled by name or pattern; no background job was left running
  (`jobs -rp` empty; every run was `wait`ed in its own bounded shell).

## 9. Artifacts

Scratch (not committed; cite by path + sha256):
`/fast/scratch/hyaku/chousa-r34/w1/ExecPerfProfile/` — `ARTIFACTS.md` indexes every
file; `ARTIFACT_SHA256.txt` pins the key ones:

```
14c9bb6bfaaef0079cf2eb8604dbd627110becf2bde409876cb215a730967670  prof/profcf73501.log
307ef52d82b99e8cf29312476c0cb9a1d960db278f43ec0ef319f95a43588098  prof/cf73501_C2.log
59636dda8bb941866bcf7429f0d61dbcca6923cd04fd07b1ebcbccd0c1f6bd88  prof/prof65536.log
5b0e3a19510d5940ca877d424d6432132b3f2d5b19820afa50f0354e1f2a8b85  logs/limits.txt
a0a66c3e267a76854e2fec6de70ba8ce7047b949971a797d82045f742b058a6b  logs/whichop.txt
9cbdc81138e20a1e31b093b2b40c101b480814dc6a71b0106a16ef62373a6785  logs/sweep_summary.txt
```

instrumented gate: `gate-instr.sh`
sha256 `d7ddacb5e16b61186fd7da2fd8d4621e48f631d1cd1f9dc042191d6bc7c809dc`
(base + timers only; stdout/stderr verified identical to pristine).

**Evidence copies inside my own directory** (all < 1 MiB; total 152 KB), at
`/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-34/w1/ExecPerfProfile/`:

* `prof/` — 19 PROF logs: `prof4096ml.log` … `prof65536.log` (the size sweep),
  `profcf73501.log` (counter-shaped fixture, ambient locale, 1234 s),
  `cf73501_C2.log` (same fixture, `LC_ALL=C`, 302 s),
  `ab_C_1.log`, `ab_C_2.log`, `ab_en_US.UTF-8_1.log`, `ab_en_US.UTF-8_2.log`
  (the controlled locale A/B), `linefull16384.log`, `linefull32768.log`
  (the `line`-field double hex-build), `line16384.log`, `line32768.log`,
  `cmp1l.log`, `cmpml.log` (single-line vs multi-line span).
* `logs/` — `limits.txt` (argv + PCRE2 ceilings), `whichop.txt` (root-cause
  isolation), `sweep_summary.txt`, `candbench.txt`, `bashmatch.txt`,
  `bashnative.txt`, `matchbench.txt`, `cf_summary.txt`, `fit.txt` (exponents),
  `linefull16384.out`, `linefull32768.out`.

**Repo/fleet state:** untouched. The only files I wrote inside the lane repo are this
report and the evidence directory above. The pre-existing working-tree edits to
`SKILL.md` and `corpus/knowledge/metadata-screen-r25.md` (mtime 08:09, the E3 range
correction) are **not mine** — I did not touch them; `tools/research-gate.sh` is still
sha256 `43a1af35ca668fe5…` and `corpus/evidence/round34/c1-count.py` is still sha256
`5ef347874960b525…`. No git/jj write command was run in either repo.
