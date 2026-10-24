# Round 39 — capture bash pin (operability) and verifier/subject binding (calibration)

author: chousa L1 (host-mapped seat: no live L2 dispatch this round — the wave
is prepared under `.ufo/waves/round-39/` and dispatched by the orchestrator;
the L1's construction runs are disclosed as such in claims.md)
date: 2026-10-24
round: 39 (attempt 1)

Claims: C1 (operability, lowest axis 3/10) — the canonical capture's
grandchild and the verify-all section children run through ONE pinned
absolute `bash` (`RESEARCH_GATE_BASH` override, `BASH_PROVENANCE` refusal),
so a caller PATH `bash` shim cannot interpose (frozen
`corpus/evidence/round39/claims.md`; measured `ENV_PIN_CAPTURE_MATCH`
7/8 → 8/8). C2 (calibration) — round-39 receipts bind `verifier_sha256` and
`subject_counter_sha256`, re-derived by the verifier with named refusals
(measured `RECEIPT_BINDING_MATCH` 8/8; the r38 pipeline is the before-state
control). Routed defects D1–D6 from the round-38 closure are repaired in the
same landing (claims Errata 14–15, erratum counts, SKILL.md row, lesson
records, SCORECARD attribution note).

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| vacuous — the doctored-subject fixture replaced `ENV_PIN_CAPTURE_MATCH` with its implicit-concatenation twin (`"ENV_PIN_CAPTURE_" "MATCH"`) — identical bytes, so the subject-swap cell verified the re-pointed receipt `ok` and the swap attack was never exercised | first c2 construction run, `verifier-subject-rebind` observed `subject_swap_verify_rc: 0` / `VERIFY: ok` (run scored 6/8, `/tmp/chousa-r39-c2.log` — not committed) | none at the freeze; QUALITY 56 lands from this lesson | c2-count cell 3 replaces with a true byte-class change (`ENV_PIN_CAPTURE__MATCH`), hard-fails "not-doctored" if the source matches, and the landed run refuses `subject-counter-sha256-mismatch` (receipts `c2-after-s39101/39121.json`) |
| vacuous — the verifier-weakening doctor deleted the census `return` line, leaving an empty if-body: a syntax crash (stderr-only), so the cell's observable was empty stdout instead of the named refusal — a crash is not a detection | same run: `replaced_verifier_verify_fail: ''` with rc 1 | none at the freeze; QUALITY 56 | the doctor replaces the refusal with `pass` (the r38 Erratum-11 weakening class: absent the binding, the copy would re-adjudicate silently); the landed run refuses `verifier-sha256-mismatch` by name |
| vacuous — the PATH-`env` shim fixture re-added the echo as a prefix assignment (`CHOUSA_GREP_PIN_ECHO=1 exec /usr/bin/env "$@"`), which the forwarded `-u CHOUSA_GREP_PIN_ECHO` un-sets again: the shim was benign, and the first mutant run's `path_env_shim_echo` hold proved nothing about the landed gate (mutant scored 5/8 only via the r38 function cells) | manual probe `bash .ufo/waves/round-39/controls/mut-gate-path-env.sh --pin` under the shim PATH → `grep -c '^GATE_GREP: ' = 0`; receipt `c1-mutenv-s39003.json` (superseded, not committed) | none at the freeze; QUALITY 56 | the shim forwards the `-u` pairs verbatim and re-adds after them (the FN_ECHO parsing shape for the binary case); the rebuilt mutant then fails the cell live (`echo_lines=1`, drift `-GATE_GREP`, `4/8`, committed receipt `c1-mutenv-s39013.json`) |
| landing — the base control was first copied from the EDITED working tree (post-pin bytes `89022659…`), not the pre-round bytes the before-state must bind | `sha256sum` of the copy disagreed with the closure-recorded pre-round gate `0447ad14…` (round-38 closure D1 evidence) | the r38 claims Erratum 6(e) precedent (hash supersessions get an erratum) — applied one round late | restored from `git show 8c7c867:tools/research-gate.sh`; the control now binds `0447ad14…` and the claims freeze names the supersession as Erratum 14 |

## Gate

Rows opened/re-opened this round: **S071 re-opened** (GNU coreutils
`env(1)` — `/usr/share/man/man1/env.1.gz`; canonical URL
`https://www.gnu.org/software/coreutils/manual/coreutils.html#env-u` printed
as the roff tty-link at the anchored line, not fetched; accessed
2026-10-24; located quote 8 words at decompressed line 28 under `.SH
DESCRIPTION` (line 8), `-u, --unset=NAME` `.TP` at line 27: "remove variable
from the environment"; file SHA-256 `4ae797e6e280da9d514bc94f3fbceffac5d0ceb62c197f78bb04bee84a78fb27`
— matches the row). S071's used-by change, old→new:
`corpus/knowledge/pin-capture-env-r37.md` →
`corpus/knowledge/pin-capture-env-r37.md, corpus/knowledge/capture-bash-pin-r39.md`.
No new rows; no other status/recheck/used-by change.

- Rejected candidates (recorded): a second `bash(1)` man-page row for the
  version-reporting surface — S068 holds that file (BASH_ENV scope) and the
  r38 lesson's rejected-candidate row stands; the bash pin's GNU-reporting
  premise is a measured binary property, not a manual citation. A third
  `sha256sum(1)` row — S070/S073 already hold both scopes.
- Census before → after: 73 rows (A 67/B 1/C 5; mined 50/queued 19/rejected 4)
  → 73 rows (same histograms); `sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin chousa` exit 0 both ends (before: round start,
  after: this landing); standing W04 ×3 (S051/S053 duplicates + the expected
  S073-shared coreutils URL).
- Receipts (round close): six committed — `c1-after-s39011.json`,
  `c1-after-s39111.json`, `c2-after-s39101.json`, `c2-after-s39121.json`
  (landed gate, all `VERIFY: ok` against their bound gate/counter/verifier
  bytes), `c1-base-s39001.json` (`VERIFY: ok` against the bound base gate;
  refuses the landed gate `gate-sha256-mismatch`),
  `c1-mutenv-s39013.json` (`VERIFY: ok` against the bound mutant). The first
  c2 construction receipt and the broken-shim mutant receipt were discarded
  as superseded drafting states, named in `## Mistakes`.
- Selftest on the final bytes: `RESEARCH_GATE_SELFTEST: PASS (275 cases,
  0 skipped)`; no-harm battery held (claims 17/17, chain 17/22, broken 1/2,
  archives 3/3, integrity-r7 composed CLEAN).
- Knowledge admitted: `corpus/knowledge/capture-bash-pin-r39.md` (C1, cites
  S071 re-opened this round and S072) and
  `corpus/knowledge/receipt-verifier-subject-r39.md` (C2, own-work);
  sourced-claim requirement: C1 rests on S071 opened this round.
- Non-author spot-check: pending the hyaku closure (as every round).
