# chousa-r38.W2ScribeLesson

## Verdict

Lesson draft complete: 7-row `## Mistakes` (the three required — vacuous verifier, scope-coupled c2 cells, live `BASH_ENV` — plus unsealed doctors, unquoted shim, expectation race, in-place freeze edit), a `## Gate` with S072/S073 corrected against `w1/ScribeSources.md`'s own findings and my re-opened bytes, receipt/census close notes, and QUALITY row 55; drafts are text here only, nothing written.

## Evidence

Lane tip `git -C …/chousa-shokunin rev-parse master` → `8e93bc916527b3c21f0f702967fa65c3b4c31699`. No counter was run: **no seed is claimed**; seeds below are receipt fields. The working tree is dirty beyond my report — `claims.md` (+Errata 9/10), `verify-receipts.py` (`33c7c87e…`), `c1-count.py` (`a48e5b22…`) and `tools/research-gate.sh` (`0447ad14…`) were edited by other seats after my runs; my receipt and selftest numbers are against the HEAD bytes then in the tree (`37e2b996…` gate, `79040790…` c1-count).

**Receipts — 9/9 `VERIFY: ok`, twice** (`verify-receipts.py --receipt <f> --gate <g> --counter <c>`): c1-after-s38001/-s38011/-s38351 → `ok … counter=c1-count.py` (landed gate); c1-base-s38001 → `ok … gate=base-gate-r37.sh`; c1-base2-s38003 → `ok … gate=base-gate-r38.sh`; c2-after-s38101/-s38111/-s38371 and c2-base-s38101 → `ok … counter=c2-count.py`. Both base receipts use their own control gate; against the landed gate they return `VERIFY-FAIL: gate-sha256-mismatch`, rc 1. A first pass using each receipt's `subject_counter` as `--counter` returned `VERIFY-FAIL: counter-sha256-mismatch` ×4 — my error; `counter_sha256` binds the *scoring* counter (F4). Counts: C1 7/7 ×3, base 2/7 ×2; C2 7/7 ×3, base 0/7. `c2-after-s38101`: `seed=38101 matched=7 total=7 predicate_holds=True`, `predicate=RECEIPT_BINDING_MATCH=7/7`, `gate_sha256{,_pre,_post}=37e2b996…`, `expect_sha256=d34f1735…`, 7 scenarios.

Hashes: gate `37e2b996…ab6d27d`; expectations `d34f1735…faf8aa`; c1-count `79040790…c3462221`; c2-count `414a7a10…cc403e3`; verify-receipts HEAD `b63e7e20…d5cf952`, run states `3fc41661…f8abf919` then `33c7c87e…182fdb` (9/9 under both); claims.md HEAD `2bc82126…` → `59d0eb6b…`.

**Census (stdout-only, no write):** `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0; `chousa W04 S051 duplicate url …`, `chousa W04 S053 duplicate url …`, `chousa ok …/corpus/SOURCES.md`. `grep -c '^| S'` → 71 (last `S071`); A 65 / B 1 / C 5; mined 48 / queued 19 / rejected 4; `grep 'S072\|S073'` → no match.

**S072/S073 re-opened by me (2026-10-24, no network):** `sha256sum /usr/share/info/bash.info.gz` → `cde1a336…105588f`; `zcat | sed -n '1305,1310p'` → node header 1307 (`Node: Shell Functions`), heading 1309; `1459,1464p` → sentence 1461–1464; `grep -n gnu.org` → line 30 `<http://www.gnu.org/software/bash/>`. `sha256sum …/sha256sum.1.gz` → `93c17dff…e8403f`; `grep -n '^\.SH'` → `3 NAME 5 SYNOPSIS 8 DESCRIPTION 61 AUTHOR`; `5,8p;15,21p` → SYNOPSIS body 6–7, DESCRIPTION 8, `-b, --binary` 16–17, `-c, --check` 19–20 (quote 20). `pacman -Q bash coreutils` → `bash 5.3.20-1`, `coreutils 9.12-2`. `wc -w`: S073 quote **8**, S072 quote **22**.

**Selftest (final bytes, my run):** `bash tools/research-gate.sh --selftest` → `ok-case 268 pin-env-fn-echo-scrub exit=0` … `ok-case 272 env-pin-override-fake exit=2`, `RESEARCH_GATE_SELFTEST: PASS (272 cases, 0 skipped)`, exit 0, 153.89 s wall (`/tmp/r38scribe.lZm0dD`); corroborates `.ufo/waves/round-38/w2/W2ExecNoHarmFinal.md:12-16`.

## Findings

1. **`w1/ScribeSources.md`'s S073 quote is 8 words, not 7** (`wc -w` = 8 on "read checksums from the FILEs and check them"); its Gate draft says "7 words".
2. **Row arithmetic is 71 → 73, not 70 → 72** — that report measures `grep -c '^| S'` = 71, and round-37's lesson records 71 before this round.
3. **S070's supersede has an unstated dependency:** `corpus/SOURCES.md:80` is S070 `mined` with `used-by … claim-pin-provenance-r37.md`, and `corpus/knowledge/claim-pin-provenance-r37.md:7` names S070 in `source:`; flipping S070 to `queued` alone breaks QUALITY 7 — repoint the entry to S073 in the same commit, or keep S070 `mined` with a supersede note.
4. **`verify-receipts.py --counter` takes the SCORING counter, not `subject_counter`** — passing the subject yields a false `counter-sha256-mismatch` (observed ×4); close-out must use `c1-count.py` for c1 receipts, `c2-count.py` for c2.
5. **S072 has no printed html-node URL** — `bash.info` prints only `<http://www.gnu.org/software/bash/>` (line 30); the draft cites that printed URL, not an unopened page.
6. **S072 cannot launder the encoding** — no `BASH_FUNC` line exists in `bash.info`, so `BASH_FUNC_name%%` stays the Erratum-5/6 measurement, not a citation.
7. **Close-time doc drift:** `SKILL.md` `## Gates` still prints `PASS (267 cases)` per row and has no round-38 counter row (r38 selftest 272).
8. **Verifier identity is unbound and the verifier moved mid-wave:** receipts carry no `verifier_sha256` (Erratum 2 debt), and `verify-receipts.py` went `b63e7e20…` (HEAD) → `3fc41661…` → `33c7c87e…` during wave 2; 9/9 held under both run states, but "ok" is verifier-version-relative — the close names the verifier bytes it certified with.
9. **A post-seal gate or counter edit invalidates the receipt set:** a committed c1 receipt verified against the current working-tree gate+counter returns `VERIFY-FAIL: counter-sha256-mismatch`, rc 1 — the receipt binds `counter_sha256`/`gate_sha256` of the sealed bytes. The close must regenerate the nine receipts under whatever bytes it lands (or revert the wave-2 edits), else "9/9 ok" is true only at `37e2b996…` / `79040790…`.

## Draft — `corpus/lessons/round-38.md` (not written to disk)

```markdown
# Round 38 — env-pin capture (operability) and receipt binding (calibration)

Dates are UTC. Frozen at `95e33de…` (round-37 closure); landed in three commits — freeze
`504c1d2`, wave-1 integration `1f0add7`, SentScope integration `8e93bc9`. A v1 two-wave shape:
wave 1 (30 reports under `.ufo/waves/round-38/w1/`) falsified the frozen verifier; the
integration closed Errata 1–8; wave 2 re-attacked the integrated bytes; claim bodies are frozen.
- **C1 operability** (lowest scored axis, 3/10; surface: the `--pin` capture's one absolute `env` invocation) — before `ENV_PIN_CAPTURE_MATCH=2/7` on both controls (`base-gate-r37.sh` seed 38001, `base-gate-r38.sh` seed 38003); after 7/7 on seeds 38001, 38011 (L1), 38351 (wave), receipts binding gate `37e2b996…`. Narrowed (Erratum 6) to function-export interposition + override refusal; PATH independence, the `bash`-name vector and hostile drift are pre-registered r39 cells.
- **C2 calibration** (surface: receipt binding) — before `RECEIPT_BINDING_MATCH=0/7` (r37 counter, seed 38101); after 7/7 on 38101, 38111 (L1), 38371 (wave). Separable: the r38 counters also score 7/7 on the unfixed gate; each half has single-hunk mutants.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| vacuous (the frozen verifier certified self-consistency, not provenance: re-sealed r37 receipt, c1 receipt rerouted as c2 with the counter hash swapped to a public digest, doctored `pin_rc`, zero-scenario receipt all verified `ok`) | `w1/CritC2Kill.md` findings 1–3 | **none** — no criterion required a receipt's rows to be tied semantically to the frozen table; digest agreement was the whole standard (QUALITY 55) | §Erratum 2: binds counter family + predicate, parses the expectation table, requires the exact frozen census with each `expect` tied to the frozen row, re-derives every `ok`; the four fixtures are those Errata 2/9 report refusing, and `c2-count` stays 7/7 |
| scope (three c2 cells asserted the SUBJECT counter's exit code, coupling C2 to C1's gate fix — 4/7 on the base gate — falsifying "c2 is gate-agnostic" on the frozen bytes) | `w1/ExecDoNothingCtl.md` finding 3 (seed 38202; `expectations.jsonl:8,10,14`), `w1/RevSeparability.md` | QUALITY 54 (in force since round 37, not applied at the freeze) | §Erratum 4: cells assert receipt existence + verification only; a C2-only tree at 7/7 on the unfixed gate is separability, not a do-nothing path |
| survivor (harness left `BASH_ENV` live: one caller startup file moved the committed 2/7 r37 control to 7/7 and forged the refusal token; a PATH-resolved non-importing `bash` moved the landed gate) | `w1/RevCounterC1.md` finding 1 (seeds 38219/38221), `w1/RevClaimsC1.md` | **none** — `base_env()` scrubbed the attack variables, never the startup channel | §Erratum 5: `BASH_ENV`/`ENV`/`SHELLOPTS`/`BASHOPTS` scrubbed, `/usr/bin/bash` pinned with timeouts, observable is the anchored `research-gate: ENV_PROVENANCE refused:` line; PATH coverage r39 |
| survivor (tamper doctors never re-sealed, so all three c2 tamper cells were caught at `receipt-self-digest` and the named binding checks were never exercised; a verifier mutant dropping them still scored 7/7) | `w1/RevCounterC2.md` finding 5; `w1/MutVerify.md` finding 4 | QUALITY 52 (in force since round 36, not applied at the freeze) | §Erratum 3: `doctor()` re-seals; each cell asserts its exact refusal (`counter-sha256-mismatch` / `expect-sha256-mismatch` / `receipt-self-digest`) |
| scope (the c2 self-rewrite fixture interpolated the caller's `--gate` path unquoted into shell source: a gate filename carrying shell syntax executed as the counter user) | `w1/SentScope.md` finding 1 | **none** | §Erratum 8a: every interpolated path shlex-quoted |
| scope (both counters hashed the expectation table only at receipt time; a mid-run edit let a receipt bind bytes the scenarios did not score) | `w1/SentScope.md` finding 2 | **none** | §Erratum 8b: pre-run hash, refuse with no receipt on mid-run change |
| process (the frozen claims file was edited in place after the freeze instead of an appended erratum) | `w1/ScribeSources.md` finding 7 (`+6` insertions); disclosed as §Erratum 1 | QUALITY 4 (errata append-only) — disclosed, so recorded not silent | kept as §Erratum 1 with its disclosure sentence; body text otherwise untouched |

## Gate

Rows added this round: **S072**, **S073** (71 → 73 rows; census `validate` exit 0, W04 ×2
standing for S051/S053). Opened locally 2026-10-24; no network.
- **S072** GNU Bash Reference Manual `bash.info` (Bash Edition 5.3, 18 May 2025; makeinfo 7.2), Node `Shell Functions` (3.3): header 1307, heading 1309, sentence 1461–1464, quote 1461–1463; `bash 5.3.20-1`; SHA-256 `cde1a336…588f`; URL printed by the info file at line 30 `http://www.gnu.org/software/bash/` (not fetched; the html-node rendering is not printed). Located quote (22 words incl. the elision token): "Functions may be exported so that child shell processes … automatically have them defined with the ‘-f’ option to the ‘export’ builtin". The manual states export-and-inherit and never the `BASH_FUNC_name%%` encoding, so that half stays the Erratum-5 measurement [INFERENCE].
- **S073** GNU coreutils `sha256sum(1)`, `.SH SYNOPSIS` line 5 (body 6–7, no option entries) versus `.SH DESCRIPTION` line 8, `-c, --check` at 19–20 (quote at 20), FIPS-180-2/format 54–58; page header "GNU coreutils 9.12", September 2026; installed `coreutils 9.12-2`; SHA-256 `93c17dff…403f`; URL printed as the roff tty-link at the anchored line `https://www.gnu.org/software/coreutils/manual/coreutils.html#cksum-c` (not fetched). Located quote (8 words): "read checksums from the FILEs and check them". The correction is the *label*, not the offsets: S070's 4–11, 19–20, 54–56 verify, but 19–20 is a DESCRIPTION `.TP` entry [INFERENCE].
- **Corrections from `w1/ScribeSources.md` §Findings, re-verified:** sentence span 1461–1464 (dispatched 1460–1463); S073 quote 8 words, not 7; rows 71 → 73, not 70 → 72. Rejected candidate: `/usr/share/man/man1/bash.1.gz` — S068 holds the `BASH_ENV` anchor there and excludes exported-function behaviour.
- **Supersede bookkeeping (open dependency):** S070 (`corpus/SOURCES.md:80`, `mined`, used-by `knowledge/engine-swap-canary-r36.md, knowledge/claim-pin-provenance-r37.md`) is the row S073 corrects; flipping it to `queued` without repointing `knowledge/claim-pin-provenance-r37.md:7` leaves that entry citing a non-`mined` row (QUALITY 7). Do both in one commit, or keep S070 `mined` with a supersede note. Arithmetic: 71 rows (A 65 / B 1 / C 5; mined 48 / queued 19 / rejected 4) → 73 with both new rows `queued` (A 67; mined 48 / queued 21), or mined 47 / queued 22 if S070 flips.
- **Census receipt:** `validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, W04 ×2 + `ok`, on the pre-add registry (71 rows, malformed 0). After: not measured — the rows are drafts; the closure re-runs `validate` on the landed registry.
- **Receipts (round close, measured):** the nine receipts under `corpus/evidence/round38/receipts/` verify `ok` (5 c1 / 4 c2) against gate `37e2b996…`, expectations `d34f1735…`, and the SCORING counter (`c1-count.py` / `c2-count.py` — not `subject_counter`, which yields a false `counter-sha256-mismatch`). The two base receipts bind their own controls (`a7d3922c…`, `9fcac047…`) and refuse the landed gate. Counts: C1 7/7 ×3, base 2/7 ×2; C2 7/7 ×3, base 0/7. `verifier_sha256` is unbound (carried debt, Erratum 2) and the verifier changed twice mid-wave (`b63e7e20…` HEAD → `3fc41661…` → `33c7c87e…`; 9/9 under both run states), so a close-out records the verifier bytes it certified with, and any post-seal gate/counter edit forces receipt regeneration (a committed receipt against the working-tree bytes refuses `counter-sha256-mismatch`).
- **Selftest (final bytes):** `RESEARCH_GATE_SELFTEST: PASS (272 cases, 0 skipped)`, exit 0, 153.89 s; corroborated by `.ufo/waves/round-38/w2/W2ExecNoHarmFinal.md:12-16`.
- **Knowledge admission candidates / spot-check (both pending, not satisfied):** no round-38 `knowledge/` entry exists; C1 (env-pin capture) and C2 (receipt binding) are L1 candidates — if admitted, C1 cites S072 for the inheritance statement only, C2 cites S073 (superseding S070). The non-author spot-check is the closure's verdict, not this lesson's.
- **Sourced claim:** the exported-function vector rests on S072 for the manual's statement that functions are exported to child shells; the `BASH_FUNC_*` transport is a measurement. C2's digest contract rests on S073 through the round-37 entry.
```

## Draft — `corpus/QUALITY.md` row 55 (highest landed row is 54; not written)

```markdown
55. **A verifier's pass is a claim about provenance and truth, not about an artifact's
    agreement with itself.** A verifier that re-hashes the receipt's own fields certifies only
    self-consistency: re-sealing restores every digest, a counter hash can be swapped for a
    public digest, and an unparsed expectation table lets a doctored observation keep `ok=true`.
    A receipt-verifying gate binds (a) the counter family and the frozen predicate it claims,
    (b) the frozen expectation bytes — parsed, not only hashed — (c) the exact scenario census
    with each row's `expect` tied to the frozen table, and (d) re-derives every `ok` from (b)
    and (c). Check: mutate each of the four independently, re-seal each mutant, and require a
    named refusal. Shown able to fail: round-38's frozen `verify-receipts.py` accepted a
    re-bound legacy r37 receipt, a c1 receipt rerouted as c2 (counter hash swapped to the
    public digest), a `pin_rc` 0→99 doctoring and a zero-scenario receipt
    (`.ufo/waves/round-38/w1/CritC2Kill.md` findings 1–3); after Erratum 2 all four refuse
    while `c2-count` stays 7/7. — `lessons/round-38.md`.
```

## Limits

- Drafts are text in this report only; `corpus/SOURCES.md`, `corpus/lessons/round-38.md` and `corpus/QUALITY.md` were not written, and no jj/git state was touched. Census "after" counts and admission decisions belong to the L1/closure.
- No counter was run, so no seed is claimed; seeds above are receipt fields. My executions: `verify-receipts.py` ×20 (two verifier byte states), `sources-census.sh validate` (stdout-only), one `--selftest` (PASS 272), `sha256sum`, `zcat`/`sed`/`grep`, `pacman -Q`.
- Word counts use `printf '%s\n' '<quote>' | wc -w`; the `…` elision counts as a token. Line numbers are decompressed-stream positions, not gzip offsets.
- QUALITY 55's "now refuse" clause follows Erratum 2 plus `c2-count`'s 7/7, not a personal re-run of `CritC2Kill`'s four fixtures; the mid-wave verifier edits are another seat's and are not adjudicated here.
- No tool installed or upgraded; the host-wide pacman pause was not exercised.
