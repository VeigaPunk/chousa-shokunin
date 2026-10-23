# Round 36 · W1 · RevCounterHonesty — fraud/vacuity audit of `c1-count.py`'s own guards

Seat: L1chousa36.RevCounterHonesty (leaf, no subagents). Date of all accesses: 2026-10-23.
Lane tip read via `git rev-parse master HEAD` → `700bd5fcbf9abc118a6a0f078d51a2e7460c2878` (both).
Gate pin: `sha256sum tools/research-gate.sh .ufo/waves/round-36/controls/base-gate-r36.sh` →
`a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8` (landed, exit 0) and
`a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad` (base control, exit 0). Both match the
context's frozen values. Counter pin: `sha256sum corpus/evidence/round36/c1-count.py` →
`3fefffe745ed10d2fd06c4c3cc9073ab7bfb46dd82e32c166976fd3aaf4c35be` (681 lines).
No network; no lane production file written; experiments only in `/tmp/hyaku/chousa-r36/w1/RevCounterHonesty/`.

## 0. Verdict (up front)

**VERDICT: C1 GUARDS LARGELY SOUND, TWO REAL VACUITIES PROVEN, ONE STATED-LIMIT MEETS DEMONSTRATED.
Fresh-seed re-derivation: `ENGINE_SWAP_CANARY=14/14` + `predicate_holds=true` on seeds 36301 and 36311
against the landed gate (exit 0 both). Kill-rule sentence 3 is enforced in code (c1-count.py:446 → label
`=error`, holds=false, exit 1 — observed live). Kill-rule sentence 2 has NO in-counter enforcement: the
receipt's `gate_sha256` (c1-count.py:662) hashes the `--gate` argument, so it can never differ from
itself; a comment-only byte-different gate scores 14/14 (seed 36321). S9's guard never observes the
override engine executing: a gate whose wrapper never execs the pin scores 12/14 with **S9 PASS**
(seed 36351). MEETS: a for-show gate that discards every pinned-engine answer and answers from
`/usr/bin/grep` scores `ENGINE_SWAP_CANARY=14/14`, `predicate_holds=true`, exit 0 (seed 36371) —
the claims.md call-for-show limit, demonstrated at gate level across all fourteen scenarios.**

## 1. Guard table (c1-count.py @ 3fefffe7…, line-verified)

| # | Guard | Lines | Deciding condition | Bypass a broken fixture/gate could try | Verdict |
|---|-------|-------|--------------------|----------------------------------------|---------|
| G1 | Reference A sanity | 435-437, raise at 446 | `rc0==1` ∧ drift ∧ K1 `supported/match` ∧ K2,K3 `unsupported/mismatch`; else `RuntimeError` → label `ENGINE_SWAP_CANARY=error`, `predicate_holds=false`, exit 1 | A fixture weakened so K2/K3 pass makes ref_a false → counter refuses to score (fails closed) | **Holds** (observed live, §4.5) |
| G2 | Output equality `same_as_a` | 441-443 | rc ∧ drift ∧ **every** parsed CLAIM line equal to reference; used by S1 452, S2 459, S3 479, S7 516, S8 528, S9 541 | Gate forges CLAIM lines without computing them — but then S10's argv channel or S7's recorder check diverges | Holds as equality; cannot see *how* output was produced (inherent) |
| G3 | Tripwire emptiness | 424-428; used 452, 459, 541 | PATH-shim / BASH_ENV log file must stay 0 bytes | Gate would need the scratch tripwire path (counter-random); no knowledge channel | **Holds** |
| G4 | S3 tool-farm completeness | 455-479 | output equality ∧ `"not found" not in stderr` | A gate needing an unlisted tool prints `command not found` → caught | Holds |
| G5 | S4/S5 override refusal | 486, 493 | `rc==2` ∧ `GREP_PROVENANCE` in stderr | A gate refusing ALL overrides passes S4/S5 but fails S7 (override must be honoured) | Holds via cross-scenario tension |
| G6 | S6 non-GNU refusal, exactly one `--version` probe | 501-502 | `rc==2` ∧ marker ∧ `len(lines)==1` ∧ args `== ["--version"]` | Stub faking GNU text on **stdout** gets pinned → S6 then *fails* (rc 0≠2): counter kills the permissive gate, never inflates | **Holds** (engine-side inflation closed) |
| G7 | S7 override honoured + recorder sees matcher calls | 516-519 | output eq ∧ echo line fullmatch (path+source+**live** `--version`) ∧ `len(rec_matches)>=1` | Gate pins+echoes the recorder and calls it once for-show with one matcher-shaped argv — passes S7 with a single call | Vacuity, subsumed by G9 (S10) for per-record |
| G8 | S8 default echo vs live version | 528 | output eq ∧ echo fullmatch | Same for-show shape as G7 but the default pin *is* the working engine on this host | Vacuous only in the H1 sense |
| G9 | S10 per-record attribution + k1 separation | 552-554 (ref_b), 556-583; decode 283-305, 307-321 | ref_b sane ∧ **every** record's own span/chunk in a `-a -z -b -o -P` argv ∧ k1 gate output-equivalent (573) ∧ k1 long records **un**attributed (575) ∧ `bash -n` | A gate that calls the pin per record and discards the answers attributes everything → **passes** (H1, proven); an engine that skips calls fails (proven: k1 control) | **Holds for query-provenance only; cannot prove answer-use** |
| G10 | S11 manifest truth under hostile PATH | 601-608 | both fields 64-lowercase-hex ∧ equal hashes the counter computes itself (own hashlib, 61-66) | Gate hardcoding a wrong hash fails; avoiding PATH sha256sum entirely also passes — but then the manifest is true anyway | Holds |
| G11 | S12 C-locale decode | 621-622 | UTF-8 ref sane ∧ C-locale run byte-identical (rc + all CLAIM lines) | Gate locale-dependent elsewhere than `json_unescape` is out of arm's reach (stated limit) | Holds within stated scope |
| G12 | S13 pin-echo isolation | 636-641 | drift from env scrubbed of `CHOUSA_*` (632-633) → `GATE_DRIFT: none` ∧ no `GATE_GREP:` line in pin | Echo line with non-canonical prefix would escape `startswith` but then trips drift as `-LINE` | Holds |
| G13 | S14 drift token naming | 653-656 | injected token drifts as `-GATE_GREP` ∧ `-LINE` absent | — | Holds |
| G14 | Final predicate + receipt hash | 660-668 | `holds = passed==14 ∧ ref_a ∧ ref_b`; exit 0 iff holds; `receipt["gate_sha256"]=sha256_file(gate)` | **The hash is computed FROM the gate under test — self-referential; never compared to the frozen `a7d3922c…`** | **Vacuous in-counter (H2, proven)** |

Note: `predicate_holds=true` appears only in the receipt JSON, never on stdout; stdout prints the label
line plus scenario lines (663-666). claims.md P1's "prints … with `predicate_holds=true`" is satisfied
via the receipt + exit code, not stdout — phrasing nit, no behavioral gap.

## 2. Proven findings (each with command, exit, label)

### H1 — MEETS: argv channel proves query, not use; a for-show gate scores 14/14 (seed 36371)
`gate-forshow3.sh` (artifact copy, sha256 `023923278a9c81fa94c3c40da1bd300c895903bab3c0c1707d0809b958accc9f`)
is the landed gate with exactly one line changed — the pin wrapper (research-gate.sh:359) now reads:
```bash
grep() { "$GREP_BIN" "$@" >/dev/null 2>&1 </dev/null || true; /usr/bin/grep "$@"; }
```
i.e. **every** pinned-engine call executes (so argv, echo, and tripwire channels all see it) but its
stdout/stderr/stdin are discarded; every answer comes from `/usr/bin/grep`.

```
C1_TMP=$S TMPDIR=$S python3 corpus/evidence/round36/c1-count.py \
  --gate $S/gate-forshow3.sh --seed 36371 --receipt $A/c1-forshow3-s36371.json
→ EXIT=0 ; stdout line 1: ENGINE_SWAP_CANARY=14/14 ; receipt: holds=true, gate_sha256=02392327…
   S1…S14 all PASS; S10 landed_attributed = [['C-LONG-32765','chunk'],['C-SHORT','direct']]
```
Why it matters: S7's "the recorder actually receives the matcher calls", S9's "override beats shim",
and S10's per-record attribution all pass while the pinned engine never supplies a single byte of
answer. The canary's epistemics are exactly claims.md's stated limit ("proves the pinned engine was
queried for each record, not that its answer was used") — here demonstrated at **gate** level with a
frozen predicate pass, not merely argued. This is the ceiling of what C1 can certify; it does NOT
contradict P1 (the label means what the freeze says), but any future reading of S7/S9/S10 as "the pin
did the matching" is falsified by this receipt.
Deciding line: c1-count.py:577 (`ref_b and len(landed_attr)==len(spans_b) and k1_long_missing …`) —
satisfied by argv presence alone.

### H2 — kill-rule sentence 2 is not enforced by the counter (label not bound to gate identity)
claims.md: "a scored run whose `gate_sha256` differs from the receipt's is not the claim's measurement."
The receipt's hash IS computed from the gate under test (c1-count.py:662), so the sentence can never
fire by itself; only an external auditor comparing to the frozen `a7d3922c…` enforces it.
Proof — comment-only byte difference, behavior identical:
```
printf '\n# audit: comment-only byte difference …\n' >> gate-comment.sh   # sha256 7728d34a1d21a864…
python3 corpus/evidence/round36/c1-count.py --gate $S/gate-comment.sh --seed 36321 --receipt …
→ EXIT=0 ; ENGINE_SWAP_CANARY=14/14 ; holds=true ; receipt gate_sha256=7728d34a1d21a864… (receipt
  c1-commentpatch-s36321.json)
```
A 14/14 label therefore attaches to ANY gate handed via `--gate`; the freeze's identity binding lives
entirely outside the counter. (Not a bug — the design — but the kill rule should be read as an
auditor procedure, not a counter property.)

### H3 — S9 passes while the override engine never executes (docstring overstates its own guard)
Module docstring (c1-count.py:32-33): S9 … "the recorder receives the matches". The check (541-543) is
only `trip_empty(trip2) and same_as_a(rc,out) and echo == want9` — **no recorder-log observation**.
Proof — `gate-pinnaming.sh` (sha256 `5c028fed1fbe33288c7fd62246c98c0ea7a07c47bc4f33d38fa0b29d41764379`)
replaces the wrapper with `grep() { /usr/bin/grep "$@"; }` (pin never exec'd; echo still names it):
```
python3 corpus/evidence/round36/c1-count.py --gate $S/gate-pinnaming.sh --seed 36351 --receipt …
→ EXIT=1 ; ENGINE_SWAP_CANARY=12/14 ; holds=false
   S9-override-beats-shim PASS   (echo fullmatch, shim silent, output equal — pin never ran)
   S7-override-distinct-path FAIL (matcher_calls=0 — G7 catches it)
   S10-semantic-canary FAIL      (landed_attributed=[] — G9 catches it)
```
So S9 alone certifies nothing about execution; it is carried entirely by S7+S10. Guard-table note, not
a P1 break (the conjunction still fails the broken gate).

### H4 — minor doc-vs-code: k1 control "attributes 0/2" (docstring line 36) vs code (575-577)
Code requires only that the LONG records be missing from k1 attribution; the short record legitimately
still attributes via grep. Observed in the H1 receipt: `k1_attributed = [['C-SHORT','direct']]`,
`k1_long_missing=true`. The enforced check is the correct separation; the docstring overstates.

### Holds where it matters — engine-side stub inflation is closed
A stub that fakes GNU text on stdout gets pinned (research-gate.sh:382-389 checks stdout only, stated
limit) but then lands the verdicts itself → S6 fails (rc 0≠2), i.e. the counter kills the permissive
gate; a stub that answers by exec'ing real grep is output-equivalent by construction and gains nothing
anywhere (S6 refused, S7/S10 need pin-argv). **Strongest guard: G1+G9 conjunction** — reference sanity
fails closed on any weakened fixture (observed: §4.5), and the k1 control proves attribution is not a
restatement of output equality (an output-equivalent no-argv gate drops to 13/14 by construction).

## 3. Kill-rule sentence-by-sentence vs actual exit/label condition (claims.md C1 vs c1-count.py:660-668)

1. "Any run of the counter against the landed gate below 14/14 kills C1" — **matches**: label prints the
   count (`ENGINE_SWAP_CANARY=12/14`, exit 1, H3 receipt); `holds` requires `passed == TOTAL` (660).
2. "a scored run whose `gate_sha256` differs from the receipt's is not the claim's measurement" —
   **vacuous in-counter** (H2): the receipt hash is derived from the scored gate itself (662); sentence
   enforceable only by external comparison to `a7d3922c…`.
3. "a scenario made to pass by weakening its fixture (reference no longer sane) is not a measurement" —
   **matches, enforced at 446**: sanity failure raises → label `ENGINE_SWAP_CANARY=error`,
   `predicate_holds=false`, exit 1. Observed live (§4.5), not inferred.

## 4. Command log (verbatim; all exit codes; scratch `S=/tmp/hyaku/chousa-r36/w1/RevCounterHonesty`, artifacts `A=.ufo/waves/round-36/w1/RevCounterHonesty`)

1. `sha256sum tools/research-gate.sh .ufo/waves/round-36/controls/base-gate-r36.sh && git rev-parse master HEAD` → 0.
2. `wc -l corpus/evidence/round36/c1-count.py … tools/research-gate.sh && ls .ufo/waves/round-36/measure/` → 0 (681/294/377/8258 lines; 8 committed receipts).
3. `sha256sum corpus/evidence/round36/c1-count.py` → 0 (`3fefffe7…`).
4. `C1_TMP=$S TMPDIR=$S timeout 1800 python3 corpus/evidence/round36/c1-count.py --seed 36301 --receipt $A/c1-fresh-s36301.json` → **0**, `ENGINE_SWAP_CANARY=14/14`, holds=true, gate `a7d3922c…`.
5. same, `--seed 36311` → **0**, `ENGINE_SWAP_CANARY=14/14`, holds=true.
6. `cp tools/research-gate.sh $S/gate-comment.sh && printf '\n# audit: …\n' >> … ; … --gate $S/gate-comment.sh --seed 36321 --receipt $A/c1-commentpatch-s36321.json` → **0**, `14/14`, holds=true, gate `7728d34a…` (H2).
7. `sed "s|grep() { \"\$GREP_BIN\" \"\$@\"; }|grep() { /usr/bin/grep \"\$@\"; }|" tools/research-gate.sh > $S/gate-pinnaming.sh && … --gate $S/gate-pinnaming.sh --seed 36351 --receipt $A/c1-pinnaming-s36351.json` → **1**, `12/14`, S9 PASS (H3).
8. v1 for-show (`grep() { "$GREP_BIN" "$@" >/dev/null 2>&1; /usr/bin/grep "$@"; }`, sha256 `07d988a6…`), `--seed 36341` → **1**, stderr: `ENGINE_SWAP_CANARY=error reference run A not sane: rc=2 drift=False obs={}`. Cause: `set -euo pipefail` (research-gate.sh:292) + unprotected rc-1 discard.
9. v2 (`… 2>&1 || true; …`, sha256 `715ca8e7…`), manual `PATH=/usr/local/bin:/usr/bin:/bin bash $S/gate-forshow2.sh verify-claims claims.jsonl --root $S/diag` → GATE_EXIT=2, `research-gate: GNU grep with -z/-P support is required…` (research-gate.sh:1821): the discard call **drained the probe's stdin pipe** (token_matcher_require, 1819-1820).
10. v3 `</dev/null` fix, manual smoke → GATE_EXIT=0, `CLAIM id=K1 … verdict=match`; then `--gate $S/gate-forshow3.sh --seed 36371 --receipt $A/c1-forshow3-s36371.json` → **0**, `14/14`, holds=true (H1).
11. `grep -n 'score("' corpus/evidence/round36/c1-count.py` → 0 (line numbers in §1); `grep -n -e "def score" -e "raise RuntimeError" … ` → 0; `grep -n 'support is required' tools/research-gate.sh` → 0 (1821).
12. Receipt/log reads and `sha256sum` of all artifacts → 0.

Both failed probes (8, 9) are the counter's guards working: G1 refused to score a non-sane reference.

## 5. Files opened (access date 2026-10-23)

- `.ufo/waves/round-36/w1-briefs/RevCounterHonesty.md` (assignment)
- `corpus/evidence/round36/claims.md` (C1/P1/kill rule/limits; "queried … not that its answer was used" quote, ≤25 words)
- `corpus/evidence/round36/c1-count.py` (full, ranges 1-123/124-330/333-563/439-543/544-681)
- `tools/research-gate.sh` (329-473 pin machinery; 1794-1833 token_matcher_require; lines 292, 359 via grep)
- The six receipts + stdout/stderr logs listed in §6.

## 6. Artifacts (all under `.ufo/waves/round-36/w1/RevCounterHonesty/`, each < 1 MiB)

| artifact | sha256 |
|---|---|
| `c1-fresh-s36301.json` (landed gate, fresh seed) | `c3c2081bf1713c523becd6a1ac6729c531b02cd3840fa3ababf6543975e81de9` |
| `c1-fresh-s36311.json` (landed gate, fresh seed) | `1b3781c75dc1d69e5a4150754b47bc84479bff730d714890469c755f05ab46b3` |
| `c1-commentpatch-s36321.json` (H2) | `f2ac39c56ae02e2078c17b888cb6416a7949996a7977cd88ad852da683494b0c` |
| `c1-forshow-s36341.json` (error receipt, G1 live) | `51fe76ca37fbeec9f655c68bad3ce699343736610dda729d844c5b97edc5a2da` |
| `c1-pinnaming-s36351.json` (H3) | `85b899fcfe72ce8f93591ec647db03dac10d365f78357d96d4563b2f505aadd6` |
| `c1-forshow3-s36371.json` (H1, MEETS) | `cfd3349798b97125e09a149495be7f5fe8c3f8ce3415a51e7bb01fd67d38fb94` |
| `gate-comment.sh` | `7728d34a1d21a864a8ddefc635e6bd36d5c68a5842e77835ba4eb5fc9e3aff31` |
| `gate-pinnaming.sh` | `5c028fed1fbe33288c7fd62246c98c0ea7a07c47bc4f33d38fa0b29d41764379` |
| `gate-forshow3.sh` | `023923278a9c81fa94c3c40da1bd300c895903bab3c0c1707d0809b958accc9f` |
| `/tmp/.../gate-forshow.sh` (v1, failed probe) | `07d988a6b55695a5bed3b32ab52861affdf3d515d856d0faef5d1ddd2db6b179` |
| `/tmp/.../gate-forshow2.sh` (v2, failed probe) | `715ca8e79231b15f08e246a6ba5bdbd74e13e00c3d90f796d3feb1286a14c794` |
| stdout/stderr logs for every run | `/tmp/hyaku/chousa-r36/w1/RevCounterHonesty/c1-*.std{out,err}` |

No tool installs were needed (python3/bash/sed only). No pacman transactions.

## 7. Residual risk & verification gaps

- The base-gate 10/14 control was not re-run here (sibling assignment `ExecC1BaseCtl`); my H2/H3/H1
  runs all used non-frozen gate blobs and are correctly NOT C1 measurements — their value is the guard
  audit, and their receipts carry the differing `gate_sha256` per H2's mechanism.
- H1's for-show gate needed stdin redirection on the discard call; a stricter variant that also
  duplicates stdin (`3<&0`) was not tested — irrelevant to the finding (discard must not consume the
  caller's stdin, `</dev/null` is the honest minimal form).
- C2 (`argv-witness.py`, `c2-count.py`) was read for context sizing only (294/377 lines); its guards
  are outside this seat's target.
- LSP: no language server was queried for this audit; all semantic checks are direct line-cited reads
  plus executed behavior (bash gate runs are their own ground truth).
