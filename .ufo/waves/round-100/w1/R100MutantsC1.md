# R100MutantsC1 — C1 mutation probe

Lane chousa round 100, seat `R100MutantsC1`, freeze F `6d4e8487ee6a16823c24a8e085c6559b92b9fec8`.
Baseline pristine battery (reproduced, exit 0, receipt `R100MutantsC1-pristine.txt`):
`NEG=7/7 MARK=11/11 BOUND=3/3 NORM=2/2 POS=4/4 REV=11/11 REVPOS=3/3 PROD=6/6 HARM_SAME=27/27 BASE_REV_ADMITTED=8/11 ORACLES_REJECTED=12/12`, `CHALLENGE_CONTROLS_R100=PASS`.
Base tool (`git show 929c784c:tools/gate-records.py`) `--no-oracles` (exit 1, `R100MutantsC1-base-noor.txt`): `REV=3/11 PROD=4/6 CHALLENGE_CONTROLS_R100=FAIL`. Clone `repo/` sha256 `a40505d8…` was never mutated; every mutant is a separate file under scratch `muts/tool/`, run via `--tool <mutant> --no-oracles`. Generator asserts each site occurs exactly once (`count==1` check in `R100MutantsC1-gen_mutants.py`): 38 mutants — 11 marker drops, 21 new-code sites, 6 round-99 rules.

## Tool mutants — 30 KILLED / 8 SURVIVED

KILLED (battery FAIL, exit 1) — tally line records verdict of the battery on the mutant:
all 11 marker drops (each `MARK=10/11`; `m-drop-verifyhuman` also `BOUND=1/3`, `m-drop-couldnt`/`-justamoment` also `NORM=1/2`, `m-drop-checking` also `REV=9/11`, `m-drop-cookies` also `PROD=5/6`);
`n-lstree-corpus` (`REV=0/11 PROD=2/6`), `n-capany-to-cap` (`REV=9/11 PROD=5/6`), `n-z-drop` (`REV=0/11`), `n-sib-raw`/`-none-inv`/`-noassign` (`REV=9/11 PROD=5/6`), `n-strip-drop` (`REV=0/11`), `n-rvcapture-call-none` (`REV=0/11`), `n-none-check-drop` (`REVPOS=2/3 HARM=20/27`), `n-ischallenge-drop` (`REVPOS=1/3`), `n-empty-blob` (`REV=0/11`), `n-blobtype-inv` (`REV=0/11 REVPOS=0/3 HARM=20/27`), `n-urladmit-drop` (`REV=0/11 PROD=2/6`);
r99 rules: `r-lt` (`BOUND=2/3`), `r-max199`/`-201` (`BOUND=2/3`), `r-nonorm` (`REV=10/11`), `r-nolower` (`NEG=0/7 PROD=0/6 REV=2/11`), `r-all` (`NEG=0/7 MARK=0/11 PROD=0/6`).

### Survivors — PASS, `CHALLENGE_CONTROLS_R100=PASS`, exit 0 (identical tallies)

1. `n-cache-repoonly` — cache keyed by repo only, `k=(repo,rev)` → `k=(repo,)`. **UNCOVERED, proven divergent outside the battery.** Receipt: `R100MutantsC1-two-rev.md` (`two.md`) run against a 2-commit fixture `c2proj`. F tool: record 2 `FAIL LINE,WORDS`; mutant: `FAIL CHALLENGE,LINE,WORDS` — the mutant judges `corpus/evidence/note.txt` (same bytes at rev2, not a capture of rev2) as a challenge capture because it cached rev1's map. The battery creates one process per record (`run()` per rec), so a 2-rev file never exercises the cache. C1 sentence says identity is read from "that rev's tree"; a repo-only cache violates the letter in any single-process multi-rev run. This is a genuine Find (coverage gap + latent correctness), not a falsification of a printed count.
2. `n-txtwins-first` / `n-txtwins-inv` — `.txt`-wins priority dropped/inverted. **UNCOVERED but contrived.** No fixture leg registers two capture paths with the same object id (fixture writes distinct bytes per capture). F tool's own "(.txt wins)" rule therefore has no leg firing on a collision; the sibling lookup can differ only when one OID maps to two capture paths (duplicate blob under `.txt` and `.raw` keys). Verified by `ls-tree` probe (`R100MutantsC1` scratch `probe_txtwins.py`): both entries list OID `c112ec5f…`. Partial coverage gap against the sentence's ".raw entry judged by its sibling .txt" clause; the battery's r5/r6 tests use non-colliding OIDs.
3. `n-blobdecode-plain` — strict UTF-8 decode instead of `errors="replace"`. **Uncovered edge.** All battery blobs are valid UTF-8 (raw HTML is ASCII), so undecodable `.raw` never occurs. On a non-UTF8 raw entry the mutant crashes (numeric exit nonzero, traceback) where F judges replacement text. Edge outside the C1 count; noted, not falsifying.
4. `n-rc-ignored` / `n-verify-drop` — `rev-parse` returncode/`--verify` dropped. **Equivalent on sane trees.** Every battery record already passes `git_blob` (commit+blob checks), so `rev:path` resolves and rc==0; divergence requires an object vanishing mid-run.
5. `n-ddash-drop` — `--` dropped from `ls-tree`. **Equivalent:** rev is a 40-hex string; `corpus/captures/` is unambiguous.
6. `n-blobtest-drop` — `parts[1]=="blob"` dropped. **Equivalent for CHALLENGE purposes:** a tree entry could only match `CAPANY` with a 24-hex name; its OID can never be the OID of a blob addressed by `rev:path`.

No survivor falsifies any clause *as counted*: every printed tally of the pristine battery is correct, and none of the 8 survivors is reachable by a single-record battery case. The substantive finding is coverage: the battery does not test (a) multi-rev single-process cache identity (`capture_oids`), (b) duplicate-OID wins rule, (c) non-UTF8 `.raw` decoding. C1's sentence overstates the battery by implication when it implies the rev-branch is mutation-covered — the instrument is weak on those 3 points, but the claim's printed numbers hold.

## Battery mutants — 12 one-site loosenings, each run vs F tool and vs base tool

| mutant | F tool | base tool | note |
|---|---|---|---|
| b1-rev-rc1 (REV verdict: `rc==1` only) | PASS | FAIL | **SURVIVES F.** Any FAIL code counts. A tool emitting `FAIL LINE` (no `CHALLENGE`) on challenge captures still passes all 11 REV legs. Verdict check is weak; does not change prints. |
| b2-drop-revpos | FAIL | FAIL | Killed. |
| b3-guard-drop (`t[g][1]>0`) | PASS | FAIL | Equivalent on fixed sizes. |
| b4-harm-rc-only | PASS | FAIL | **SURVIVES F.** HARM ignores stdout diffs. |
| b5-harm-stdout-only | PASS | FAIL | **SURVIVES F.** HARM ignores exit-code diffs. |
| b6-oracle-sitemissing-pass | PASS | FAIL | **SURVIVES F** (oracle `SITE-MISSING` counted as rejected). |
| b7-base-adm-dropped | PASS | FAIL | **SURVIVES F.** `BASE_REV_ADMITTED=0/11` — print is unchecked to any other value. |
| b8-q-revpos-refused | FAIL | FAIL | Killed. |
| b9-oracle-good-flip (`>=0`) | PASS | FAIL | **SURVIVES F.** Oracle aggregate guard dead. |
| b10-mark-admit | FAIL | FAIL | Killed. |
| b11-bound201-refused | FAIL | FAIL | Killed. |
| b12-harm-guard-drop | PASS | FAIL | Equivalent here (same==len(harm) always). |

All 12 still FAIL on the base tool, so base discrimination is intact; but 8 of 12 loosenings pass the F tool. Strongest weaknesses: b1 (wrong-code FAIL counts as challenge), b4/b5 (HARM compares only one channel), b7 (BASE divergence number never asserted), b6/b9 (oracle bookkeeping can be dead). This puts no printed number in doubt — each surviving battery mutant still *prints* `PASS` only when the F tool truly passes every leg — but shows print `PASS` is a weaker word than "21/21 leg groups mutation-verified".

## Falsification of claim wording

- `BASE_REV_ADMITTED=8/11` in the frozen predicate **is never compared to any threshold by the battery itself**; the battery would print `PASS` with `0/11` or `11/11`. The 8/11 number is a printout, not an enforced property the counting command checks. A service claiming that number as checked evidence relies on a human reading the line, not on `CHALLENGE_CONTROLS_R100=PASS`. Same for the exact `REV=11/11` count being a printout rather than threshold — though a wrong count does change the printed line, so a predicate-matcher sees it; `PASS` alone would not.
- The C1 sentence says "identity is read from GITDIR's tree at the record's rev". True per call, but `n-cache-repoonly` proves a single-process two-record-two-rev file can license a wrong capture set. The battery never makes that call. The sentence claims per-record identity; the implementation is per-(repo) cached. That is a false statement as written for any 2-rev file (**FIRES on the letter**), fixable by one cache-key change or one multi-rev battery leg.

## C2 note (n/a — C1 only lane)

No C2 claim was touched by this seat (mutation probe on `gate-records.py`/battery only). `VERDICT: R100MutantsC1 C1 fired — capture_oids is cached per repo (n-cache-repoonly), so a two-record file with two revs mis-judges the second rev's blob as a capture; the battery (one process per record) never tests it, and the C1 sentence's "that rev's tree" is false as written for such files. All 38 mutant runs otherwise match prints (30 KILLED, 8 survivors all proven equivalent/uncovered, none falsifying a counted number; battery-loosening survivors are weaknesses of PASS-monoprages, not of the printed predicate).`

VERDICT: R100MutantsC1 C1 fired — capture_oids keyed by repo alone mis-judges two-rev files per the C1 sentence, a coverage/letter falsification invisible to one-process-per-record battery.
