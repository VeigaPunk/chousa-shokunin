# Round 33 — claim fields from the top-level object only

Dates are UTC. Base `2b9cc73aed30c2e2c95699db6617d9531ef49fb2` (gate SHA-256 `f4731885…03f0`, the
landed round-32 gate). Attempt 1; no earlier attempt of this round left files
(`.ufo/watchdog.log` has only the launch line for `chousa round=33`).

- **C1 operability** (lowest scored axis; surface: `verify-claims`' claim-record field reader,
  `json_str`/`json_has_key` and their callers) — fields are read from the record's top-level JSON
  object only; a repeated top-level read field is invalid; string content is never structure.
  Carried as round-31 D-C and round-32 D4.

One claim. The round-32 routed defects D1, D2, D3 and D5 are repairs, not claims.

Frozen design: `corpus/evidence/round33/claims.md` — v1 `3b528b9a` (08:23Z), v2 `e3e24ec8`
(08:35Z, after the pre-data critic CriticAxisFit33 and before any candidate receipt). Control
evidence committed at `96be7925` (08:40Z); candidate `eb179ec3` (gate `52f07c74…`, 08:41Z);
measurement `7f6aeb70`; integration `0fb300b5` (gate `94a7be5a…`: header and usage text only).

## Spot-check intake (round 32, `round-32-verifier-spotcheck.md:152-169`)

| Route | Disposition | Evidence |
|---|---|---|
| D1 C2 fixture encodes truth in file order | Counter v3 `corpus/evidence/round32/c2-count-v3.py` (new file; v2 unedited): bodies first, writes shuffled across classes, mtimes drawn independently. Controls scored before the landed gate: exact round-32 metadata control 132/132 under v2 → 96/132 and 95/132 under v3; mtime-only 96, inode-only 95, no-reader 78, round-31 gate 0. Landed audit then 132/132 on `f4731885` and `52f07c74` (two seeds each) and on `94a7be5a`. QUALITY 36 | `.ufo/waves/round-33/w1/ExecD1CounterV3/`, `.ufo/waves/round-33/measure/d1-v3/` |
| D2 tally without counting command | `python3 corpus/evidence/round33/d2-census.py --lane .` prints `C1 receipts on gate 10f2fe12: 21` (not 18, not 20); the two receipts between 18 and 20 are RerunC1b's load runs (07:51:22Z), not critic re-scores; the 21st is RerunC1b's tmpfs run. Correction appended to `SCORECARD.md`. QUALITY 37 | `.ufo/waves/round-33/w1/ExecD2Census.md` |
| D3 battery revision header | `battery.sh` prints `lane_revision=` and `gate_sha256=` (plus counter and fixture hashes) before any row. QUALITY 38 | `.ufo/waves/round-33/w1/ExecNoHarmBase33/battery.sh`; `measure/battery-candidate/battery.out:1-19` |
| D4 nested keys | C1 | below |
| D5 signals by name | Every wave context forbids name/pattern signals; `corpus/evidence/round33/no-name-signals.sh` exits 1 on round 32 (`w2/RerunC1b.md:31`, `pkill -x sleep`). QUALITY 39 | `.ufo/waves/round-33/w1/ExecD5Check.md` |

## Control wave findings (before data)

- Wave 1 (32 seats, 08:26Z): every v1 control missed 144/144 (do-nothing 60, junk 0–87,
  no-reader 69–99, last-wins 69, brace-depth 121–132, strip-nested 128–130, refuse-nested 20–36,
  duplicate-policy 132–138, partial-fields 122–140, no-finding 0–129). The python oracle scored
  144/144.
- CriticAxisFit33 found two v1 gaps before any candidate: the duplicate class counted 3 of the 7
  keys the contract names, and the counter accepted any gate exit. Design v2 (`e3e24ec8`) widened
  duplicates to six keys (TOTAL 156) and requires exit 1 + a DRIFT line. The L1 re-scored all 34
  control gates under v2 before the candidate (`controls/L1-v2-rescore/summary.txt`): best
  non-oracle 142/156. Shown afterwards: a three-key duplicate gate scores 144/144 under v1 and
  144/156 under v2 (`controls/L1-mistake/`).
- Holds (safety filter `cyber_policy`, ended, not retried or rerouted): CtlC1Shortcut (label-keyed
  shortcuts) and MutC1Counter (counter-of-counter). No output.

## Falsify wave findings (34 seats, `.ufo/waves/round-33/w2/`)

- **P1 v2 held on every landed-gate run.** ReceiptCensus33 counts every committed v2 receipt on
  `52f07c74`, `94a7be5a` and `165acd5f`: all 156/156, none below. Final gate `43a1af35`: 156/156 on
  seeds 3701/3702 (`measure/final/`).
- **§9 counterexample, post-data (C1 not verified by its counter).** CriticControls33 inferred that
  a gate masking the counter's six fixed CONFUSER strings, then regex-stripping nested containers
  and counting repeats, needs no string lexer. The L1 built it (`w2/L1ShortcutMask/`, gate
  `ae7d4bfc`): **156/156 on seeds 3391 and 3392.** The counter's clause-3 classes use six fixed
  literals, so a shortcut keyed on fixture content meets P1. The counter is not amended. The
  labelled-shortcut control that should have caught this before data was the held CtlC1Shortcut.
- Non-counter evidence on the reader itself: FuzzDiff33 750/750 on `94a7be5a` (base 313/750),
  and 1950/1950 on the final gate over three seeds (`measure/final/fz-9021{2,3,4}.json`);
  RerunC1a 449 + 410 records; ProbeNestedOnly33 382; NoHarmCorpus33 35 committed JSONL files, exit
  codes identical, every changed line explained.
- **Contract breaks outside the counter, repaired in-round** (gates `165acd5f`, then `43a1af35`):
  bare tokens such as `tru`, `01`, `xyz` (top level and nested) and FF/VT whitespace accepted
  (ProbeWhitespace33, ProbeFlatBehaviour33, ProbeMalformed33, CriticClaim33); a marker_default row
  with a repeated read field silently taken (RerunC1a, RerunC1b, ProbeMarkerDefault33); three id
  repeats compared only two (ReviewKnowledge33); `"\u0000"` in span decoded away
  (ProbeMalformed33 F4, pre-existing at base); invalid escapes such as `\q` accepted
  (MutC1GateString, pre-existing); 64 KiB unread member 0.07 s → 4.7 s (ProbeLongLines33): the
  reader now consumes runs with one regex match each (0.11 s). Selftest 248 → 251 cases.
- Still not checked (disclosed): raw control bytes inside strings, member grammar inside nested
  values beyond bracket balance and bare tokens, escaped key spellings. Spans of 32 KiB or more
  cannot be located (`tok_span_at` argv limit; base too, ProbeLongLines33 F1).
- Mid-wave gate edits: the L1 edited `tools/research-gate.sh` in the lane while seats were running
  counters against that path. Receipts on intermediate worktree gates `b808e9b5` (0/156, a
  half-written edit: `p46: unbound variable`), `45d76b4f`, `fc08410e` (156/156) belong to no
  committed revision and are not scored revisions.
- Sources: ReopenS062 found the S062 anchor ended mid-sentence (316–333); corrected to 316–335.
  ReopenS063 holds.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| A counter's adversarial classes use a small fixed set of literal strings, so a gate keyed on those literals meets the counter without the general behaviour | `.ufo/waves/round-33/w2/L1ShortcutMask/mask-s339{1,2}.json` 156/156 | none before data: the label-keyed control seat ended on a safety hold, and no other seat built it; CriticControls33 found it after data | QUALITY 40: confuser content is generated per seed, and a fixture-literal mask control is scored before freezing. Shown able to fail: the mask gate meets `c1-count-v2.py` (156/156) |
| A counter enumerated fewer contract keys than the contract names (3 of 7 duplicate keys) | `controls/L1-mistake/v1-s338{1,2}.json` 144/144 under v1; `v2-s338{1,2}.json` 144/156 | pre-data critic CriticAxisFit33 (F1), before any candidate | design v2; the check is the same gate scored under both counters |
| The L1 edited the gate in the lane checkout while falsify seats scored it | ReceiptCensus33; `w2/ReviewC1Diff/c1-v2-s4117.json` (0/156 on `b808e9b5`) | seats' own hash discipline (receipts record `gate_sha256`) | QUALITY 41: post-falsify repairs are built in a scratch copy and installed after the wave settles (done for the last repair, `43a1af35`); shown able to fail on `b808e9b5` |
| A report tally carried no counting command (round 32 D2) | `SCORECARD.md` ×18; census 21 | outside spot-check | QUALITY 37 (`d2-census.py`) |

## Gate

New source rows (opened by ScribeSourceRFC8259 / ScribeSourcePyJson, re-opened by the L1 with the
same body SHA-256 and each quote found once, `.ufo/waves/round-33/measure/reopen-L1.txt`; again by
ReopenS062 / ReopenS063):

- S062 — https://www.rfc-editor.org/rfc/rfc8259.txt, accessed 2026-10-23, HTTP 200, sha256
  `61a5378f…cd2d7`. Quotes: "The names within an object SHOULD be unique." (line 322); "Many
  implementations report the last name/value pair" (line 333). Admitted tier A, mined. Anchor
  corrected in-round 316–333 → 316–335 (ReopenS062).
- S063 — https://docs.python.org/3/library/json.html, accessed 2026-10-23, HTTP 200, sha256
  `5ceeeaf6…5608b` (footer 07:34 UTC). Quote: "By default, this module does not raise an
  exception; instead, it ignores all but the last name-value pair for a given name:" (found once
  after whitespace squeeze). Admitted tier A, mined (drafted `queued`, flipped `queued → mined`
  when the knowledge entry landed).

Status / recheck / used-by changes to existing rows: none (S001–S061 untouched).

Rejects (real, with reason):

- Design v1 counter `c1-count.py`: rejected as the P1 counter before data — it counted 3 of 7
  duplicate keys and accepted any exit; a three-key duplicate gate meets it 144/144.
- Counter v2 as verification of contract clause 3: rejected post-data — the fixture-literal mask
  shortcut meets it 156/156; P1 is not amended.
- Not opened: ECMA-404 (host not registered; RFC 8259 covers the same grammar at tier A).

Round shape: two v1 waves — wave 1 build + pre-data controls 32 seats, wave 2 falsify 34 seats;
round total 66. Holds: CtlC1Shortcut, MutC1Counter. Dead seats: none.

Misroot sweep (`git -C /home/vgpnk/Projects/shokunin status --porcelain`): SentinelParser33 wrote
its report to the fleet root (`.ufo/waves/round-33/w1/SentinelParser33.md`, a relative trailer
path). Copied byte-exact into the lane (`cmp` equal), fleet copy deleted. Class: seat resolved the
`Report:` trailer from the fleet root although the wave context named the lane; captured-by: the
misroot sweep; fix: none new beyond the existing context sentence (one seat of 66).
