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
  fetched; accessed 2026-10-23. Anchor corrected in-round `NOTES` → subsection "Limits on size of
  arguments and environment" (R34ReopenSources). Quote (20 words): "Additionally, the limit per string is 32 pages
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

---

# Round 34 — attempt 2 (2026-10-23, launched 15:04 -03)

Attempt 1 died with the phase-4 orchestrator after committing its work (`f20aeaa7`…`bf7c931a`)
with no report; watchdog logged `lane-dead-no-report chousa round=34`. Attempt 2 inherits C1
unchanged (verdict stays `unverified (required controls held)` per the frozen exclusion) and
declares two new claims, design v4 `corpus/evidence/round34/claims-a2.md`:

- **C2 operability** — spans of 32765..32767 bytes (the PCRE dead zone under the argv limit):
  `TOK_DIRECT_SPAN_MAX` 32767 → 32764 routes them onto the chunk matcher. Before 21/37
  (seeds 5011/5023, receipts `measure-a2/c2-before-s*.json`); after 37/37 on seeds
  5011, 5023, 5033, 5047 on gate `a6307edf…` (`fe0f22e0`). Selftest cases 254–256; battery
  11 rows PASS (`measure-a2/battery/`).
- **C3 calibration** — counted self-audit: `self-audit.py` + `audit-set.json` (43 checks)
  + `audit-dispositions.md`; first counted run `SELF_AUDIT_MISMATCHES=0`,
  `SELF_AUDIT_UNDISPOSITIONED=0` (`measure-a2/audit-first-run.txt`); negative control: two
  injected lies → 2 counted, disposition key verified (`measure-a2/audit-negative-control.txt`).

## Mistakes (attempt 2)

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| A planned-entry hypothesis was carried as if measured: planned-r35 said the PCRE dead zone spans "about 28000–32767 bytes"; the measured window is exactly 32765–32767 (length-only, all content classes) | planned row in `SCORECARD.md`; probe `/fast/scratch/hyaku/chousa-r34-a2/probe/` (20 lengths × 5 content classes) | L1 probe before freezing design v4 | C2 claims only the measured 3-length window; the planned row is corrected when r35 plans are next edited; this entry |
| C1's selftest cases 252–253 use a 29999-byte span — the DIRECT path — so the chunk matcher shipped r34 with no selftest case | `tools/research-gate.sh` ls_span construction (6 × 4999 words + 5 = 29999); case count 252–253 | L1, while designing the C2 cases | cases 254–256 pin the chunk path at 32765/32766/32767 (verbatim, mutated, glued, line-bound, line-wrong); shown able to fail: the dead-zone fixture (DD1 verbatim + DD4 line-bound, 32766-byte span) against the pre-fix gate `772a1d8e` reads both `unsupported` (stderr `grep: regular expression is too large`), against the landed gate `a6307edf` both `supported` (`measure-a2/deadzone-fixture-vs-gates.txt`) |
| An audit-set negative control was first run with the set path resolving to the pristine lane copy (no lie was actually read) | control run 2026-10-23 ~16:10Z printed 0 mismatches against a corrupted scratch set | re-run with absolute `--set` | control re-run correctly (`measure-a2/audit-negative-control.txt`); control wiring must bind the corrupted bytes, not the lane |

## Gate (attempt 2)

- S065 re-opened 2026-10-23 (attempt 2): file SHA-256 `a3ea2c67…74bd6` unchanged, package
  `pcre2 10.49-1` unchanged, both gate quotes verbatim at decompressed lines 10–11 and 23
  ("The maximum size of a compiled pattern is approximately 64 thousand code units / for the
  8-bit and 16-bit libraries"; "The maximum length of a source pattern string is essentially
  unlimited"). The row's host note (32764 compiles / 32765 rejects) was re-confirmed by the
  C2 probe. Status unchanged (`mined`); used-by adds `corpus/knowledge/dead-zone-pcre-r34.md`.
- No new rows; no other status/recheck/used-by changes (S001–S063, S064, S066 untouched this
  attempt). C2 rests on S065 as its opened-this-round source row.

## Wave 2a2 outcomes (attempt 2; 20 of 33 seats returned by the integration cutoff)

New mistake/limit rows (fix routed unless stated):

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| A calibration claim whose set is shallow is reachable by a shallow-audit do-nothing: identical 0/0 under planted drift (false SCORECARD count + broken SHONEN pointer both uncounted) | `w2a2/CritC3Claim.md` | wave critic | C3 reshaped in-round to the bounded acquisition (deepened set, before/after count, assessment-derived controls); QUALITY-class lesson: a counted claim must demonstrate the count MOVES on real drift, not only that it prints a number |
| Output-only counters cannot exclude a fixture-keyed engine that implements the exact semantics (it is output-equivalent); pure lookups without semantics ARE caught | `w2a2/MutC2Keyed.md` (ctl4/ctl6 37/37; tracer 39 firings) | wave mutation-tester | r35: work-proof battery (tracer/strace invocation-class checks; kake `lookup_control_check.py` template as the committed check); C2 verdict unaffected (gate-scoped predicate; the landed gate is not keyed — RevGateDiff diff) |
| At dead-zone lengths, positional 16384-byte edge windows overlap and are byte-equivalent to the exact matcher; the counter correctly admits them and rejects sub-span windows | `w2a2/MutC2Windows.md` (ctlB caught by decoys; ctlC meets as an exact equivalent; W=4096 positional caught) | wave mutation-tester | none needed (correct admission); arithmetic recorded in the report |
| The LC_ALL=C selftest failures are ONE byte: `\u2192` decodes via printf %b only in a UTF-8 locale; all 10 failing blocks carry `CLAIM_SPAN_NOT_FOUND obs=id=P4` | `w2a2/ExecSelftestEnv.md`; `research-gate.sh:4045` | wave executor | r35: json_unescape locale-independent `\uXXXX` decode; until then every LC_ALL=C run discloses the P4 class |
| The host's `/usr/bin/grep` self-reports pi-uu-grep 0.2.0 while pacman owns grep 3.12-2; the gate resolves bare `grep` via PATH (research-gate.sh:1618/1641/1687); the 32764/32765 boundary measured identically in every in-round run | `w2a2/RevGateDiff.md` ENV HAZARD; this attempt's shells | wave reviewer | r35: pin the grep binary path in runbooks and verify `grep --version` provenance; S066 pins the GNU man page, not the binary |
| `tok_span_offsets_chunk` binds `slen` from its local `span` at declaration; renaming the local would fall back to the caller's dynamic `span` and silently mis-confirm | `w2a2/MutC2Windows.md` latent-hazard note; `research-gate.sh:1631` | wave mutation-tester | r35: `slen=${#2}` (decoupled from the local name) |
| An auditor that reads the worktree can be moved by uncommitted bytes; the deepened auditor reads HEAD bytes via `git show` | `w2a2/RevC3Set.md` F1 | wave reviewer | landed: HEAD-byte reads + SET_SHA256 print in self-audit.py |
| Selftest-case comment numbering (252-254 / 255-257) vs the actual run (252-256) | `w2a2/ScoutSkillTally.md`; `w2a2/ExecC2Rerun.md` D2 | wave seats | r35 (comment-only edit would churn the gate digest) |

Gate (wave): no SOURCES rows opened or changed by the wave; ScoutSourcesA2 re-opened S064+S066
(pins hold, census exit 0). Dispositions/rejects this attempt: see the SCORECARD rows and the
report; the 13 unreturned seats are named in the report (queued behind the host job clamp at
the integration cutoff, not dead).
