# Round 34 — long claim spans (the argv-limit defect)

Dates are UTC. Base `b80539005176ac6ce39bc1c7afb846cb1f2f7c75` (gate SHA-256 `43a1af35…4346`, the
landed round-33 gate). Attempt 1; `.ufo/watchdog.log` has only the launch line for
`chousa round=34`, so no earlier attempt left files.

- **C1 operability** (lowest scored axis; surface: `verify-claims`' span matcher `tok_span_at` /
  `tok_span_all`) — spans of 32768..65536 bytes are verified like short spans. Frontier area chosen
  off the round-32/33 streak (record-field parsing): span length.

One claim. The round-33 routed defects E1–E5 are repairs, not claims.

## What happened

- Design v1 (`70feb5ea`): counter `c1-count.py`, 30 records, all content per seed; base 19/30.
- Pre-freeze control wave (32 seats). Five seats ended on provider `cyber_policy` holds
  (CtlC1Shortcut, CtlC1Windows, CtlC1Halves, MutC1Counter, CritC1AxisFit). CritC1Shapes (completed)
  showed v1's mutations leave two shoulder bands of every long span unexamined (`w1/CritC1Shapes.md`).
- Design v2 (`ef16afb1`) and v3 (`f20aeaa7`), both before any candidate receipt: centre mutations,
  near-copy decoys with four edit kinds, glued-then-valid, lengths to 65536; TOTAL 42.
- The L1 had re-authored the held control shapes itself (following an orchestrator note); Main's
  safety clarification (~11:20Z) ruled that a bypass. The artifacts are excluded
  (`corpus/evidence/round34/claims.md`, "Held controls and exclusions"), and C1 was declared
  unverified in the frozen design before data.
- Candidate C (ExecC1BuildC) landed `3026a4e5` (gate `772a1d8e…3e58`); counter v3 42/42 on seeds
  3601, 3602 (`LC_ALL=C`) and 3603 (UTF-8) (`934d7cb7`, `.ufo/waves/round-34/measure/`).

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| Fuzz measurements cited as final-gate evidence although their receipts bind a scratch gate (round 33, E1) | `corpus/lessons/round-33-verifier-spotcheck.md:157-162`; `.ufo/waves/round-33/measure/final/fz-9021{2,3,4}.json` (`b2c07eda…`) | round-33 outside spot-check | QUALITY 42 with `w1/ExecE4Census/receipt-binding.py`; shown able to fail: exits 1 on `.ufo/waves/round-33` listing those three receipts (`w1/ExecE4Census/census-round33.txt`); exit 0 on round 34 (R34ReviewRepairs) |
| A misrooted fleet copy was deleted without committed byte-identity proof (round 33, E5) | `corpus/lessons/round-33-verifier-spotcheck.md:172-173` | round-33 outside spot-check | QUALITY 43; shown able to fail on round 33's SentinelParser33 move (prose `cmp` only) |
| The L1 re-authored the controls of seats that ended on provider safety holds, instead of recording the hold and declaring the claim unverified | `ef16afb1` (`controls/L1-keyed/`, `L1-windows/`, halves gates in `L1-gates/`), committed with no exclusion record | Main's safety clarification, ~11:20Z | QUALITY 44: exclusion record + unverified declaration before the first candidate receipt (`f20aeaa7` precedes `934d7cb7`); shown able to fail on `ef16afb1` |
| A counter's single mutation per record left bytes no class examines (v1 shoulder bands) | `w1/CritC1Shapes.md` finding 1 (static) | pre-data critic, before any candidate | design v3 decoys (each of 168 near-copies edited at a uniform offset); the v1 counter stays committed as the failing case |
| The counter's run bound is wall-clock and its environment inherits the locale: the do-nothing base gate times out to 0/42 in the UTF-8 locale and scores 25/42 under `LC_ALL=C` | `.ufo/waves/round-34/controls/L1-base-v3/` | L1 base runs | not fixed in the frozen counter; every L1 run records its locale; the landed gate scores 42/42 in both |

## Gate

New source rows (opened by ScribeSrcExecve / ScribeSrcPcre2 from the installed man pages, no
network; re-opened by the L1 with matching sha256 and each quote found,
`.ufo/waves/round-34/L1/reopen-sources.txt`):

- S064 — Linux man-pages execve(2), `/usr/share/man/man2/execve.2.gz` (man-pages 6.19-1, sha256
  `4489dfef…c8eab0dc`); URL recorded https://man7.org/linux/man-pages/man2/execve.2.html, not
  fetched; accessed 2026-10-23. Quote (20 words): "Additionally, the limit per string is 32 pages
  (the kernel constant MAX_ARG_STRLEN), and the maximum number of strings is 0x7FFFFFFF." Tier A,
  mined.
- S065 — pcre2limits(3), `/usr/share/man/man3/pcre2limits.3.gz` (pcre2 10.49-1, sha256
  `a3ea2c67…74bd6`), accessed 2026-10-23. Quote (19 words): "The maximum size of a compiled pattern
  is approximately 64 thousand code units for the 8-bit and 16-bit libraries". Tier A, drafted
  `queued`, flipped `queued → mined` when `knowledge/long-span-argv-r34.md` landed citing it.
- S066 — GNU grep(1), `/usr/share/man/man1/grep.1.gz` (grep 3.12-2, sha256 `9b027d02…85ba`),
  accessed 2026-10-23. Quote (7 words): "Obtain patterns from FILE, one per line." Tier A, drafted
  `queued`, flipped `queued → mined` with the same entry.

Status / recheck / used-by changes to existing rows: none (S001–S063 untouched).

Rejects (real, with reason):

- Design v1 counter `c1-count.py` as the P1 counter, before data: a gate that never compares the
  two shoulder bands of a long span meets every v1 class (CritC1Shapes, static analysis of
  `c1-count.py:166-181`).
- Design v2 counter, before data: no class distinguishes case-, order- or whitespace-blind
  comparison or a first-raw-occurrence matcher (CritC1Shapes catalogue, "U" rows).
- L1-built controls for held seats: rejected as evidence (safety rule), listed in the exclusion
  record.
- The round-33 E2 claim that per-seed confusers close clause 3: rejected by R34ReviewRepairs (mask
  gate 156/156 on seed 61111).
- Not opened: man7.org (host not registered; the fetch-scope L0 question is open) — the installed
  copies of the same pages were opened instead.
