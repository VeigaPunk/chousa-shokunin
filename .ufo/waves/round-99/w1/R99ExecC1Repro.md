# R99ExecC1Repro — C1 reproduction and named-limit probes (round 99)

Seat: R99ExecC1Repro. Tree: shared clone at F `d41f4cd8b857c6de683e7be5c5e8125b32763a8e`, path `/fast/scratch/hyaku/chousa-r99/R99ExecC1Repro/repo` (asserted `git rev-parse --show-toplevel` = that dir). Claims read first: `.ufo/waves/round-99/claims.md` + `claims.json` + `plans/round-99.md`. No production edits; scratch only under the seat dir. Tooling: none installed (python3 stdlib only); no network.

## (a) Reproduction — counting command and before command

Candidate (counts as the C1 counting command per claims.md):

```
cd $S/repo && python3 -B corpus/evidence/round99/challenge-controls-r99.py --root . --work $S/work1
```

Receipt: `R99ExecC1Repro-c1-candidate.txt`. Observed:
`NEG_REFUSED=7/7 POS_ADMITTED=4/4 PROD_REFUSED=4/4 HARM_SAME=25/25 BASE_NEG_ADMITTED=7/7 ORACLES_REJECTED=5/5`, `CHALLENGE_CONTROLS_R99=PASS`, exit 0.

Before (base tool, `--tool <base> --no-oracles`):

```
cd $S/repo && python3 -B corpus/evidence/round99/challenge-controls-r99.py --root . --work $S/receipt-base --tool $S/work1/base-gate-records.py --no-oracles
```

Receipt: `R99ExecC1Repro-c1-before.txt`. Observed: `NEG_REFUSED=0/7 POS_ADMITTED=4/4 PROD_REFUSED=0/4 HARM_SAME=25/25 BASE_NEG_ADMITTED=7/7 ORACLES_REJECTED=0/0`, `CHALLENGE_CONTROLS_R99=FAIL`, exit 1. The tallies match the tallies in the committed `corpus/evidence/round99/before/c1-base.txt`; I did NOT diff the full file text against it (correction: an earlier draft said "byte-for-byte"; that was not checked). **Held** on the tallies and exit code.

Also verified `HARM_SAME` compares only `(returncode, stdout)` in the battery (`score()`, battery line 189: `(a.returncode, a.stdout) == (b.returncode, b.stdout)`); my direct `probe4.py` rerun over all 25 harm files found **zero** stdout/stderr/rc diffs between F tool and base tool, so the claim's "byte-identical" wording holds for stdout — but the battery would not catch a stderr-only difference. **Held, with instrument note** (the battery is weaker than the word "byte-identical" if stderr counts).

## (b) Eight NEW challenge fixtures — all admitted (limit a, as named)

Driver copied into w1 as `R99ExecC1Repro-probe.py`; output receipt `R99ExecC1Repro-probe-challenges.txt`. Each fixture built battery-`Lab`-style (copy `SOURCES.md` + `refetch.tsv`, registry row, refetch row http 200, capture keyed `sha256(url)[:24]`), then the F tool `tools/gate-records.py verify --root <lab>` on a single-record file. Word counts are the normalized-whitespace counts the tool uses. All eight were **ADMITTED (`OK`, rc=0)**:

| fixture | words | result | named limit |
|---|---|---|---|
| Akamai "Access Denied … Reference #" | 14 | ADMITTED rc=0 | (a) |
| PerimeterX "Press & Hold to confirm you are a human" | 26 | ADMITTED rc=0 | (a) |
| DataDome "Pardon Our Interruption … not a bot" | 20 | ADMITTED rc=0 | (a) |
| hCaptcha "Please complete the security check … solve the CAPTCHA" | 21 | ADMITTED rc=0 | (a) |
| Sucuri "Website Firewall — Access Denied … blocked" | 23 | ADMITTED rc=0 | (a) |
| AWS WAF "Request blocked by AWS WAF … too much traffic" | 29 | ADMITTED rc=0 | (a) |
| Cloudflare page with 305-word boilerplate footer | 305 | ADMITTED rc=0 | (a) (>200-word leg) |
| German "Sicherheitsprüfung läuft … Aktivieren Sie JavaScript" | 17 | ADMITTED rc=0 | (a) |

Every admission falls under named limit (a) ("a challenge page in other words than the 11 markers, or longer than 200 words, passes"). **No admission outside every named limit — held.** The marker list is a closed 11-phrase list; six real vendors and a non-English page fall outside it. Systematic substring match (`any(m in t for m in CHALLENGE_MARKERS)`, `tools/gate-records.py:125-128`) means `just_a_moment` and `just-a-moment` also evade (receipt `R99ExecC1Repro-probe5-evasion.txt`: `underscore-only … OK`, `hyphen-only … OK`) — this is also limit (a) ("other words"), though it is a lexical-variant within a known vendor family; still (a), not a new finding.

Re-confirmed named limits:
- (c) full-width alone passes: `fw-only … OK rc=0` (`probe3.txt`); full-width + an ASCII second marker refuses — my probe2 contaminated the test with a second line, the clean `fw-only` test proves the limit. Zero-width inside a marker passes when that marker is the only match — not re-tested isolated here (the probe2 zero-width case also carried a second ASCII marker and refused); covered by code reading (`norm()` only replaces 4 curly-quote chars, no NFKC) + `fw-only` admitted.
- (d) checked: unreach form with http 200/curl_rc 0 fails `REFETCH` (never `CHALLENGE`) — round-87 repair still guards it; rev record on a challenge blob outside `corpus/captures/` admitted `OK rc=0` (evil.md fixture, `probe3.txt`). Both as named.
- (a) length leg: 250-word marker page admitted (`big-250-words … OK rc=0`); exact-200 boundary refuses (as claimed by `<= 200`).

## (c) Four short legitimate documents ≤200 words containing a marker

Same driver output (`R99ExecC1Repro-probe-challenges.txt`, lower block). Three of four were **REFUSED with CHALLENGE, rc=1** (`FAIL CHALLENGE … ok=0 fail=1`):

| doc | words | result |
|---|---|---|
| changelog "fix: recaptcha widget …" (23w) | 23 | REFUSED-CHALLENGE rc=1 |
| incident "Cloudflare attention required header returned 503" (22w) | 22 | REFUSED-CHALLENGE rc=1 |
| ticket "user asks are you a robot?" (25w) | 25 | REFUSED-CHALLENGE rc=1 |
| release note, no marker (24w) | 24 | ADMITTED rc=0 (control) |

Named limit (b) says exactly this ("a real document of at most 200 words that contains a marker phrase is refused"). **Held.**

## Finding — no new finding outside named limits

All admissions/refusals observed fall under named limits (a)–(d), which claims.md discloses. I found **no admission outside every named limit**, and the counting/before tallies reproduce exactly. The strongest honest statement remains: C1's sentence is false *as a general claim about challenge pages* — it only catches 11 lexical + ≤200-word cases — but the frozen claim says exactly that and names it limit (a). So the claim text itself is **not false as stated**; this is scope, not a mis-statement. **VERDICT: held.**

No tool installed. No network. Scratch `/fast/scratch/hyaku/chousa-r99/R99ExecC1Repro` retained for the receipts above; nothing written outside w1/ + scratch.

VERDICT: R99ExecC1Repro C1 held — counting and before commands reproduce exactly and every proxy admission or refusal falls under named limits (a)-(d).
