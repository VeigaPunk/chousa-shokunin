# R92CriticClaims — claims shared-assumption falsification (C1+C2+C3)

Seat: R92CriticClaims (critic). Carrier C5 `16ccf7693c61b8ffe392fc757352304f239bfcad`, freeze F5 `42e0337822a508208800f98faa3a63c6af9f8c27`. Scratch `/fast/scratch/hyaku/chousa-r92/R92CriticClaims/` (clone at C5, `--shared`). Tool installs: none this seat (pacman guard honored; no `uv tool`/`npx`/binaries needed). Network: none (commit bytes only; S070 re-opened locally via `man sha256sum`).

## Axes
- A. Freeze integrity — do 16 pins match F5 blobs (minus-self for self row); does C5 pin F5; are non-history files byte-identical F5↔C5?
- B. No-work control — can the frozen predicate be reached without doing the claimed work (missing receipt, substring, unread body, unread selftest)?
- C. Cross-claim coupling — is C3's `## Gates` boundary case-sensitive vs the claim sentence "section only (up to the next `## `)"?
- D. "No scored run preceded F5" — git evidence: which commits carry receipts, and what `computed_against` do they pin?
- E. Ledger pre-shape — `claim-falsification.tsv` rows (per claim × attack seat) and seat coverage.

## Attempt 1 — freeze integrity (re-derived, not trusted)
Command:
```
R=/fast/scratch/hyaku/chousa-r92/R92CriticClaims/repo; F=42e0337822a508208800f98faa3a63c6af9f8c27
git -C $R show $F:corpus/evidence/round92/instrument-pins.txt > pins-at-F5.txt
while read -r h p; do git -C $R show $F:$p | sha256sum; done < pins-at-F5.txt
python3 -B -c '... minus-self sha256 over rows-without-self-row ...'
git -C $R diff --name-only $F $C   # C=16ccf769
```
Observed (receipt: `scratch/pins-at-F5.txt` + this report):
- 15 non-self pins: `OK` — each pin equals `sha256(git show F5:<path>)`. The self row's naive whole-blob hash differs (`pin=5f2885… blob=c42dc6…`) — exactly the designed minus-self split.
- Minus-self check: `computed-minus-self=5f288597d4bad803cbd3ba511d06e362c99911c30782742f378a872977f03275 match=True` — self-pin holds by its own construction.
- F5 vs C5: `git diff --name-only` = only the six `controls/receipts/*.txt`. All 15 non-self pinned files: `IDENTICAL` (blob hash at F5 = blob hash at C5 = pin). Pins file itself: `PINS IDENTICAL` F5↔C5.
- Carrier receipts pin the freeze: all six carry `# computed_against=42e0337822a508208800f98faa3a63c6af9f8c27` (= F5).
- S070 re-opened locally: `man sha256sum` → `Print or check SHA256 (256-bit) checksums.` (col -b head; `sha256sum 0.8.0`). A naive `grep "Print or check"` on the raw man stream MISSES (man hyphenation) — the claim quote is accurate as rendered text.
Verdict: **neutral (holds)**. No falsification. Freeze/carrier wiring is byte-exact under the frozen minus-self rule.

## Attempt 2 — no-work control, per claim
- C1 (`control-driver-r92.py verify`): driver reads receipt bytes before scoring (`open(os.path.join(a.receipts, f)).read()` line 464; `check_body(row, open(path).read())` line 488) and writes receipts only in `emit` (line 398), never in `verify`. Re-ran verify at clean tree: `CONTROL_DRIVER_R92=PASS … COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6` (exit 0). So a *missing* receipt (not committed bytes) cannot silently pass — committed bytes are what `verify` scores — but the predicate binds *committed* bytes only: any state reachable without fresh legs (e.g. a hand-edited receipt with coherent headers) that still matches `expected.tsv` tokens passes `COMMITTED/EXACT/PIN`; only `FRESH_OK` forces re-running the command. K4 ("a missing receipt is accepted, a committed receipt is not read, a substring satisfies a token, a duplicate pin path is scored, or the self-pin is minted inside verify") is therefore split: "not read"/"substring"/"duplicate pin"/"self-pin minted in verify" are all refused by code (whole-token `K=V`, `SETUP PIN_DUPLICATE` exit 2, minus-self recompute); "missing receipt accepted" is the one literal under-count — a *deleted-on-disk* receipt is not what verify scores (it scores the committed blob via `--repo`/`--receipts-rev`), so deleting the working-tree file does not reach PASS-failure; it still PASSES. That is by design (committed-bytes semantics), not a skip. **Narrowing needed (wording, not code):** K4's "a missing receipt is accepted" should read "a missing committed receipt (blob absent at `--receipts-rev`/`--rev`) is accepted" — the on-disk deletion is out of scope by the committed-bytes design. Neutral-as-coded; falsifies-wording on that one K4 sub-clause.
- C2 (`curation-r92.py`): `used-by` tokenised via `used_by_tokens` (non-identifier split, exact token match) — substring join is gone (lines 228-239). No-work states: (i) deleting a Located-quote row changes `Q_ROWS` count (pinned 20) — refused; (ii) a five-cell decision row is `DECISION_WIDTH`, never dropped (WARRANT leg). The shared assumption "the counter reads the entry and registry" is not skippable. **Neutral (holds).**
- C3 (`skill-tally-r92.py`): fixture `del161` (161→160 inside Gates): `OTHERS_OK=0 LEGS=2/3` → `SKILL_TALLY_R92=FAIL LEG_FAIL OTHERS expected={161:1,256:1} observed={256:1,160:1}` exit 1. The others multiset is compared by equality (`other_counts == EXPECTED_OTHERS`), not by tolerance. **Neutral (holds).**

## Attempt 3 — cross-claim coupling: `## Gates` case-sensitivity
Claim sentence: tally + case-range searches run over "the `## Gates` section only (up to the next `## `)". Code (`skill-tally-r92.py:73-77`):
```
gates_start = text.find("## Gates")          # case-sensitive, exact bytes
nxt = text.find("\n## ", gates_start + 1)     # any level-2 heading ends it
```
Fixture `casec`: `sed 's/^## Gates$/## gates/' SKILL.md` → line 82 now `## gates`. Run: `skill-tally-r92.py --root casec --selftest selftest-r92.txt` → `SKILL_TALLY_R92=SETUP no ## Gates section in SKILL.md` exit 2.
Counterexample: renaming the heading lowercase does NOT reach PASS — it is a setup refusal (exit 2), not a miscount. But the coupling is real: C3's PASS silently depends on the *bytes* `## Gates` (capital G) in `SKILL.md`, while the claim sentence names the section semantically ("the `## Gates` section"). A case-only rename is refused loudly, which satisfies K2 ("derives any bound from SKILL.md prose rather than the tool's own ok-case names" — no, bounds still come from selftest case names), and is consistent with Named Limit 1 ("The section boundary is the next `## ` at column 0; a clause moved outside `## Gates` leaves the leg"). **Neutral (holds) with a wording note:** the claim should state the heading match is case-sensitive (`find("## Gates")`, exit 2 `SETUP no ## Gates section`) — otherwise a reader may expect `## gates` to score. Smallest narrowing: add to C3 Named limits "(5) The heading is matched case-sensitively as the bytes `## Gates`; a `## gates` rename yields `SETUP no ## Gates section` exit 2, not a miscount."

## Attempt 4 — "no scored run preceded F5" (git evidence)
`git log --oneline F5..C5` = single commit `16ccf769` (carrier). `git log -- corpus/evidence/round92/` shows the four superseded pairs in order: bf12c30e (F1, no pins) → 85a2eeef (F2) → ddb5fdf4 (carrier, 6 receipts, `computed_against=85a2eeef…`) → 9722365f → dc7056c4 → e40bce1a (carrier, `computed_against=dc7056c4…`) → 007d7ea7 (F3-emitted, never carried) → d818f090 (F4 carrier, `computed_against=007d7ea7…`) → 5b7ab7f6 (plan) → 42e03378 (F5) → 16ccf769 (C5). Every superseded carrier's receipts pin *its own* freeze (85a2eeef, dc7056c4, 007d7ea7) — verifiable from `git show <carrier>:…/c1-gate-r89.txt | grep computed_against`. So: receipts WERE emitted and committed at pre-F5 freezes (ddb5fdf4, e40bce1a, d818f090 each carry six `computed_against`-pinned receipts), contradicting the literal plan wording "before any scored run" (§§Pre-wave freeze repair 1-2, lines 45, 59, 97) IF "scored run" is read as "emit + verify pass". The plan elsewhere correctly narrows it: "superseded before any scored run and before this wave — their defects are recorded" — i.e. no *wave scoring / settlement* consumed them; each was superseded by a re-freeze before the wave. Also note the seq: 5b7ab7f6 ("plan — record F4 pre-wave repair 2 naming") sits BETWEEN F4 (d818f090) and F5 (42e03378), and F5's message is "pins regenerated from 5b7ab7f6 without the plan row" — so the plan-row exclusion is the F5 delta; the "16 rows (no plan row)" statement checks out (pin count 16, plans/round-92.md absent from the pins file).
Verdict: **falsifies-wording**. "Before any scored run" is falsified as a literal historical claim: three superseded carriers contain emitted, committed, `computed_against`-pinned receipts (i.e. scored runs were performed to produce them). Narrowest true statement: "no superseded pair was scored *in any settlement* / consumed by the wave; each was superseded by a re-freeze before the wave, and only F5/C5 receipts are scored." The fix is one sentence in `plans/round-92.md` §§1-2 (replace "before any scored run" with "before any settlement scoring"), NOT a claim change — claims.json/claims.md use the correct F5/C5 pins. No freeze-integrity consequence.

## Attempt 5 — ledger pre-shape (`claim-falsification.tsv`)
File does not yet exist (checked: no `claim-falsification.tsv` under `.ufo/waves/round-92/`; only `w1-dispatch.json`, `claims.json`, `w1/`). Proposed rows (one per claim × attack seat; 12 wave seats from `w1-dispatch.json`):
| column | content |
|---|---|
| `claim` | C1 / C2 / C3 |
| `seat` | one of the 12 dispatch members |
| `attack` | the single shared assumption this seat falsified or tried to |
| `command` | exact reproducer (copy-paste runnable) |
| `observed` | ticket line + exit code |
| `verdict` | fired (predicate/kill-rule falsified) / held / n-a |
| `narrowing` | pointer to `plans/round-92.md` section (or `none`) |
Rows needed: 3 claims × (R92ExecC1Repro, R92ExecC2Repro, R92ExecC3Repro, R92ExecMutations, R92RevPrior, R92ReviewerC1, R92ReviewerC2, R92ReviewerC3, R92CriticClaims, R92SentinelScope, R92ConnectorSiblings, R92ScoutRegistry) = 36 de-duplicated (executor/mutation rows may be `n/a` for out-of-claim seats, but the seat MUST be named). Every dispatch seat is named → no missing seat (18/18 mandate: 12 registry members + carriers; the remaining 6 seats are the pre-wave F1-F4 calibration history, already recorded in `plans/round-92.md` §§Pre-wave freeze repair 1-2, not wave seats). The 4 superseded pairs are accounted in the plan, not the ledger. Smallest safe correction: L1 (ChousaR92) creates the 36-row TSV at wave settlement; the three real narrowings from THIS seat (C1 K4 "missing receipt" wording; C3 case-sensitive-heading limit (5); plan "before any scored run" → "before any settlement scoring") are `narrowing` cells pointing at `plans/round-92.md` Amendments. Verdict on pre-shape: **neutral (holds)** — no seat omitted; the ledger simply does not exist yet and 36 rows are owed.

## Summary
- Fired (falsifies-wording): Attempt 4 ("no scored run" — superseded carriers carry scored receipts); Attempt 2/C1 K4 sub-clause ("missing receipt" — on-disk deletion vs committed-blob semantics).
- Held: freeze integrity (15+minus-self OK, C5 pins F5, byte-identity), C2/C3 no-work, C3 coupling.
- Narrowings (smallest): (1) plan §§1-2: "before any scored run" → "before any settlement scoring / before this wave"; (2) C1 K4: "missing receipt" → "missing committed receipt at --receipts-rev"; (3) C3 limits +(5): case-sensitive `## Gates` bytes, `## gates` → exit 2 SETUP.

VERDICT: R92CriticClaims C1 held — C1 predicate verified byte-exact at F5/C5; K4's "missing receipt" wording over-reads committed-bytes semantics.
VERDICT: R92CriticClaims C2 held — tokenised used-by, width-pinned decision rows and 14-leg measurement verified; no no-work path reached PASS.
VERDICT: R92CriticClaims C3 held — Gates-scoping is case-sensitive (exit 2 on rename, never a pass) and the pinned others multiset is equality-checked; wording narrowing only.
