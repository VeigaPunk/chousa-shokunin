# Round 27 residual review — change (c) trailing-CR strip (seat ResCrStrip)

**VERDICT: HOLDS** — no landed-gate counterexample found; the change is a behavior-preserving
repair of a real quadratic blowup. One control-coverage weakness (the landed selftest is
mutation-blind for (c)) and four inherited, base-identical quadratic suffix-strip sites remain.

## Scope attacked

`git -C <lane> diff dd72641e cb895a2 -- tools/research-gate.sh` — the (c) hunk:
`metadata_registry_load` (cb895a2 line 2431) and the `verify_metadata` entry-read loop
(cb895a2 line 2661) changed `line=${line%$'\r'}` →
`if [[ $line == *$'\r' ]]; then line=${line:0:${#line}-1}; fi`.
Attacks: (i) semantic drift of the strip, (ii) whether "exactly one trailing CR" is preserved,
(iii) the change's own claim that the old form was "quadratic on long lines",
(iv) any *other* CR/suffix-pattern strip in the gate the change missed.

## Method (read-only on the lane; sandbox `/tmp/chousa-r27-residual-ResCrStrip`, deleted at landing)

* Revisions extracted with `git -C <lane> archive <rev> | tar -x -C <sandbox>`. Digests match the
  task: cb895a2 `tools/research-gate.sh`
  `a6bc2855e63045c9ebc0827166756d4da65478a1e255a83903ab459a08582386`; dd72641e
  `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84`.
* Harness: `bash <gate> verify-metadata <entry> --root $FX --registry <reg>` with
  `CHOUSA_STRICT=0 CHOUSA_ROOT=$FX CHOUSA_NOW_EPOCH=1790000000`, compared on stdout+stderr bytes
  and exit code (sha256 of the byte stream per revision). 52 synthetic fixtures (CRLF, lone CR
  mid-line, double CR at end, CR-only line, final line without newline, BOM, empty file,
  whitespace-only lines, fenced blocks with CRLF/tildes, invalid UTF-8, UTF-8 multibyte, NUL,
  H2 break, 1/2/4/8 MiB single-line entries).
* No lane write except this report; no network; no pacman transaction (nothing installed).

## F1 — Landed-gate counterexamples: NONE (this is the headline result)

`python3 -u run_diff2.py` (both revisions over all fixtures) → exit 0, `cases=52 differing=0`.
Long-entry subset: `L1-` 3/3 SAME, `L2-` 3/3 SAME, `L4-` 3/3 SAME, `L8-` 3/3 SAME (identical
sha256 of the byte stream in every pair).
Example decisive row: `L8-lf old_rc=1(264.40s) new_rc=1(0.36s) SAME old=0dac6ac50e99 new=0dac6ac50e99`.

Landed gate selftest, run in the sandbox with the inherited UTF-8 locale (`LC_ALL` unset,
`LANG=en_US.UTF-8`): `bash tools/research-gate.sh --selftest` → exit 0,
`RESEARCH_GATE_SELFTEST: PASS (215 cases, 0 skipped)`.

"Exactly one trailing CR" — proven at the expression level, because the gate cannot observe it:
`micro_eq2.sh` over a 38,725-line corpus (random multibyte UTF-8, invalid UTF-8, CR runs, 100 KB
lines), run twice: `LC_ALL=C` → `lines=38725 eq_divergences=0 one_cr_divergences=0` (exit 0);
`LC_ALL=en_US.UTF-8` → identical (exit 0). `one_cr_divergences` asserts, per line,
`new == line minus exactly one trailing CR` (or `== line` when it ends in no CR), compared with
`cmp` on files (not command substitution). Both call sites declare `local LC_ALL=C`
(cb895a2 lines 2385 and 2568), so `${#line}` is a byte count and the substring is byte-indexed —
the new form cannot split a UTF-8 character. `local LC_ALL=C` really does switch bash's locale
here: `bash -c 'f(){ local LC_ALL=C; printf "%s" "${#1}"; }; f "$(printf "a\xc3\xa9\r")"'` → `4`
vs `3` without the `local`.

## F2 — The change's stated rationale is TRUE and material (not a comment, a measured fix)

Expression micro-benchmark (LC_ALL=C, single string, no CR present):
`${s%$'\r'}` = 1 MiB **1.998 s**, 2 MiB **13.438 s**, 4 MiB **64.784 s** (superlinear ⇒ quadratic);
new form = 0.004 / 0.006 / 0.011 s (linear).
End-to-end through the gate (single-line entry, both revisions, byte-identical output):
1 MiB old 2.36–2.67 s vs new 0.06–0.07 s · 2 MiB old 13.67–13.88 s vs new 0.11–0.12 s ·
4 MiB old 62.98–64.97 s vs new 0.18–0.22 s · 8 MiB old **264.40–270.67 s** vs new 0.36–0.40 s
(≈700×). Note the shape dependence: when the long line *does* end with CR the old form is fast
(8 MiB: old 0.88 s) — the quadratic path is the *common* LF-only case.
Consequence for the wave: any falsify control that fed a multi-MiB line to dd72641 would have
timed out rather than failed — a slow, not wrong, predecessor.

## F3 — Control/coverage weakness: the landed selftest cannot see change (c) at all

Mutation test on the landed gate (mutants placed at `<sandbox>/tools/mut-M*.sh` so the selftest's
path-sensitive cases stay valid; a first placement at the sandbox root produced 9 bogus failures
and was discarded):

| mutant | CR-strip semantics | selftest result | exit |
|---|---|---|---|
| M1 | no strip at all | `PASS (215 cases, 0 skipped)` | 0 |
| M2 | strip **all** trailing CRs (`while` loop) | `PASS (215 cases, 0 skipped)` | 0 |
| M3 | strip **every** CR anywhere in the line (`${line//$'\r'/}`) | `PASS (215 cases, 0 skipped)` | 0 |

So the selftest's CRLF metadata fixture (cb895a2 line 5869) does not discriminate one-CR from
all-CR from none: `^(source|verified-at|recheck):(.*)$` tolerates a trailing CR, the registry row
trim `${row%"${row##*[![:space:]]}"}` already eats trailing CR as whitespace, and every later
test uses `[[:space:]]` classes in which CR is whitespace. Independent confirmation that (c) is
semantically inert: rerunning the whole differential with **M1** (strip removed) against dd72641
→ `cases=52 differing=0` plus `L8-` 3/3 SAME (old 248–252 s vs M1 0.28–0.30 s).
=> Change (c) is a **pure performance repair**; if a future claim depends on the strip's *semantics*
(e.g. exact-byte comparison of a metadata value), that claim is currently unenforced by any
control, selftest case, or falsify control.

## F4 — Inherited (base-identical) residual suffix-pattern strips this change did not touch

Same class as the removed form (single-literal-char suffix pattern ⇒ quadratic when the pattern
does not match at the end), all present **identically** in dd72641e and cb895a2 (base-identical,
not introduced by (c)):

| site (cb895a2) | form | input | measured 1 MiB |
|---|---|---|---|
| `tools/research-gate.sh:3370` | `body=${body%$'\n'}` | `--drift`/`--pin` baseline canonical block | 2.445 s (2 MiB: 13.840 s) |
| `tools/research-gate.sh:1435` | `probe=${span%%$'\n'*}` | claim `span` field | 2.307 s (2 MiB: 14.029 s) |
| `tools/research-gate.sh:1593` | `probe=${text%%$'\n'*}` | chain quote text | 2.307 s (NL at EOF 2 MiB: 13.849 s) |
| `tools/research-gate.sh:1122` | `before=${hay%%"$needle"*}` | claim source file text | 6.425 s |

Not affected: the registry trim sites `:2440`/`:2448`/`:2522` (`${x%%[![:space:]]*}`) are **fast**
(0.005 s / MiB) — the `[![:space:]]` class makes those linear. No CR strip remains anywhere
else in the gate: the only other `$'\r'` literals are the JSON/escape encoders at `:1085` and
`:2824`, which emit CR rather than strip it (`grep -nF "\$'\r'" tools/research-gate.sh` → 4 hits:
2431, 2661, 1085, 2824).

## Residual risk

1. (c) itself: none found — 52 fixtures × 2 revisions byte-identical, 38,725-line expression
   fuzz clean in two locales, selftest green, ~700× faster on 8 MiB lines.
2. The four F4 sites keep the quadratic class alive on long corpus-controlled inputs (claim
   source text, span/quote fields, drift-baseline block). A 8 MiB claim source file would cost
   minutes in `--verify-claims`/`--verify-chain`/`--drift`. Inherited, out of (c)'s scope, but the
   (c) comment's rationale applies verbatim to them.
3. The landed control set cannot detect a regression of (c)'s semantics (F3). If the round's
   frozen claims rely on CR handling being observable, that is unsupported.

## Verification gaps (explicit)

* 8 MiB timings are single-shot per shape under a loaded host (`uptime` load ≈ 14, 32 cores), not
  repeated; per parent instruction the observed 264–271 s baseline is kept as a lower bound and
  was **not** re-run to confirm.
* Sizes > 8 MiB are refused before parsing (`SOURCE_READ_MAX_BYTES` = 8 MiB): 8,388,608 bytes is
  accepted and parsed, 8,388,609 bytes is refused `reason=size` — identically in both revisions
  (verified).
* Not exercised here (other seats' scope): `--drift`/`--pin` with an oversized canonical block
  (F4 row 1), `--verify-claims`/`--verify-chain` with oversized hay/span/text (F4 rows 2–4),
  Windows/other-bash variants (bash 5.3.20 only).
* Round base 64eec5d4 was not re-extracted; "base-identical" claims in F4 are stated from the
  dd72641e↔cb895a2 identity of those lines (identical in both, hence identical in the base).

## Lane-state note (read-only compliance)

The lane working tree advanced **during** this seat: `tools/research-gate.sh` digest moved from
the reviewed `a6bc2855…` (cb895a2) to `ac1315dd…` (an unrelated registry escaped-pipe split change;
`git status` shows other agents' edits to SKILL.md, corpus/*). This seat made no lane edit other
than this report — no write/stage/commit was issued. All findings above are pinned to the archived
cb895a2bdd259eb38bec29ef70011d8211a508b5 and dd72641e574679c4f7882dd43de072b4c8892d6f contents. In
the newer working-tree candidate the two (c) sites are unchanged in form (now lines 2431 and 2675:
`if [[ $line == *$'\r' ]]; then line=${line:0:${#line}-1}; fi`), so this review's equivalence and
timing results carry over to it; the registry-split change is a different seat's scope.

## Tooling

No install or update was performed for this seat (no new tool needed; host bash 5.3.20(1)-release,
Python 3.14.8, coreutils; Arch Linux 7.2.11-arch1-1 x86_64). No pacman transaction, no network.

Scratch: `/tmp/chousa-r27-residual-ResCrStrip` (fixture generator, differential runners, fuzz corpus,
mutant gates, logs) — deleted at landing per parent instruction; decisive receipts are quoted above.
Lane touched read-only apart from this report.
