# R51W2ReviewGatesRows — SKILL.md `## Gates` rows `assimilate-rows` (:130) and `chousa round-51 counters and checks` (:133), plus the `correction:` line (:135)

Seat: reviewer (leaf). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`, tip `72566c84e4184846ff9cbc4c92bc33b8291bc53b`
(`git rev-parse HEAD`). Every command below ran from the lane root with `env -u ASSIMILATE_CITES`; the three lines the
brief names resolve as `130|/133|correction` (`grep -n 'round-51 counters\|^| \`assimilate-rows\`\|^correction: SKILL' SKILL.md`).
No tool installed or upgraded; no network; scratch `/dev/shm/chousa-r51-R51W2ReviewGatesRows/` (copies made with `cp -r`,
never a symlink) deleted at hand-off (`ls` → `No such file or directory`). No production file, report, index or jj state touched:
`git status --porcelain` hashed before/after each write-capable replay was unchanged (see §3).

## 1. Values that reproduce (attack result: hold)

| row value | command | observed |
|---|---|---|
| `findings=27 expected=27`, `3b7ad258…` | `python3 tools/assimilate-rows.py --selftest` | `SELFTEST=PASS findings=27 expected=27`, `FIXTURES_SHA256=3b7ad25837a954be5623d27a7b1a231ddf661e67e5a961f0800a112b2260bd00`, rc 0 |
| r50 package `findings=26`, `c5c56480…` with `--cites all` | `… --selftest --fixtures corpus/evidence/round50/c1-fixtures --cites all` | `SELFTEST=PASS findings=26 expected=26`, `FIXTURES_SHA256=c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43`, rc 0 |
| `tool-rev: cf642c6… digest: sha256:6b975f91…` | `git show cf642c669b736bfba6b9fbb91fd5b16cb5579d9d:tools/assimilate-rows.py \| sha256sum` | `6b975f91c809485c8d03e6134e2a17bdb7f9079c22218d74e9321a14632572f6` (pin correct) |
| adopter write set | fixture package copied to scratch, `--entry a.md --entry b.md` | stdout `COLLISIONS=2 … CITED=5 APPEND=2 HELD=3 BODYONLY=4`; files exactly `reg-ids staged-ids collisions renumber.tsv append.md stripped.tsv bodyonly.tsv bodyclash.tsv corpus/knowledge/{a,b}.md` |
| header-only `source:` | both `source:` lines of `a.md` moved below a `####` heading | `CITED=0 APPEND=0 HELD=0 BODYONLY=3` rc 0, ids listed in `bodyonly.tsv` — a post-heading `source:` line is not a citation |
| `--cites` default / env / flag wins | `ASSIMILATE_CITES=all` then `… --cites source` | env-all `CITED=7 APPEND=4`; explicit `--cites source` under env-all `CITED=5 APPEND=2 BODYONLY=4` (flag wins) |
| refusals exit 1, no `renumber.tsv`/`append.md` | unknown `source: S999`; registry heading renamed; 10-cell staged row; appended-row recheck `2026-13-45`, `((bad))` | `REFUSED corpus/knowledge/e.md: source id S999 is neither a staged row nor a lane Registry row` rc 1 (out holds only `collisions reg-ids staged-ids`); `REFUSED registry has no \`## Registry\` heading` rc 1; `REFUSED S010: staged row has 10 cells, not 11` rc 1; rc 1 ×2 recheck |
| usage exit 2 | `ASSIMILATE_CITES=bogus`; `--entry /abs/e.md`; `--selftest --out DIR` | `assimilate-rows: ASSIMILATE_CITES='bogus' must be source or all` rc 2; `--entry '/abs/e.md' must be relative` rc 2; rc 2 |
| selftest writes nothing in the lane | `git status --porcelain \| sha256sum` before/after | identical `6b08d7020a06…` both times |
| C1 `LEGS=5/5` | `python3 corpus/evidence/round51/c1-count.py` and `--seed 4733` | `SELFTEST_DEFAULT/LEGACY_ALL/SOURCE_ONLY/PIPE_IDENTITY/REGISTRY_STRUCTURE` all PASS, `LEGS=5/5`, `C1=PASS`, rc 0 (both runs) |
| do-nothing controls | `c1-count.py --tool corpus/evidence/round51/controls/{tool-before,echo-tool,const-tool,flag-noop-tool}.py` | `1/5`, `2/5`, `1/5`, `2/5`, each `C1=FAIL` rc 1 — equals `controls/c1-before.txt` |
| supplement `6/6` | `python3 corpus/evidence/round51/c1-supplement.py` | `SHAPE/MUTATION/CROSS_ENTRY/SOURCE_LINE/UNKNOWN_SRC/CLASH=PASS 3/3`, `SUPPLEMENT_LEGS=6/6`, rc 0 |
| C2 all legs | `python3 corpus/evidence/round51/c2-count.py` | `ENTRIES=3/3 BOUND=6/7 (min 5) REFUSED=1 BOUND_IDS=S107…S112 REF_ID_UNBOUND=0 NEW_GROUND=3/3 QUOTE_ROWS=61 ON_BOUND=61/61 SPAN_IDS=6/6 QUOTES_IN_{SPAN,ENTRY,LESSON}=61/61 QUOTE_SHORT=61/61 SPAN_CONTEXT=61/61 CAPTURE_BOUND=61/61 SUBSTANCE=PASS ANCHOR_BOUND=6/6 INFERENCE_GROUNDED=3/3 QUARANTINE_VERDICTS=6/6 QUARANTINE_BLOCKED_ADOPTED=0 C2=PASS` rc 0; `--lane-only` `C2=PASS` (capture leg skipped) |
| C3 legs, 36/74 | `python3 corpus/evidence/round51/c3-count.py` (`--root .`) | `CAP_ROWS=36 (base 36) POINTERS=74 (base 74) RESOLVED_BY_CORRECTION=4 DANGLING=0 C3=PASS` rc 0 |
| build-spans, quote-substance | `build-spans.py --check`; `quote-substance-check.py`; plus bad `--cache` and missing manifest | `SPANS_ROWS=61 STALE=0` rc 0; `IDS=6 QUOTES=61 FAILURES=0` rc 0; `bs_badcache_rc=2`; `quote-substance-check: no manifest …` rc 2 |
| open-items-age 0/1/2 | scratch report + lane `LOG.md` | PASS `OPEN_ITEMS_AGE=PASS since=42 rounds=9` rc 0 (LOG.md:1499 sits under `## Round 42`); missing line rc 1 `expected a line beginning: Open operator items: 8d77e6c1 since round 42 (9 rounds)`; `--item deadbeef` rc 2 |
| registry counter | `python3 corpus/evidence/round47/c2-count.py` | `GATES_ROWS=56 ENTRY_POINTS=125 REGISTERED=125/125 UNREGISTERED=0 DANGLING=0 MISMATCHES=0 C2=PASS` rc 0 |
| r49 one-shot passes, r50 cannot | in a scratch clone at `72566c84`: `ASSIMILATE_CITES=all python3 corpus/evidence/round49/c1-count.py`; `python3 corpus/evidence/round50/c1-count.py` | r49 `SETS_PASS=3/3 … C1=PASS` rc 0; r50 `BASELINE=FAIL rc=1 … LEGS=3/5 C1=FAIL` rc 1 |
| correction: four PASSes at `1d7aba09`, each exit 0 | scratch `git clone --no-local` (toplevel verified), checkout `1d7aba0948cf62f6158f77e220f64320a5b6c6cc`, four counters | `LEGS=5/5 C1=PASS` rc 0 · `SUPPLEMENT_LEGS=5/5 C1_SUPPLEMENT=PASS` rc 0 · `ENTRIES=3/3 … C2=PASS` rc 0 · `STALE_HITS=8 UNRESOLVED=0 RECEIPT_ROWS=31 STALE_COUNT=PASS` rc 0 |
| correction: one-shot at `cfe6c9fb` | same clone, checkout `cfe6c9fb` | `BASELINE=FAIL rc=1 findings=?`, `R49_REGRESSION=FAIL rc=1`, `LEGS=3/5 C1=FAIL`, rc 1; tool blob `bdaf80f43f39` (`2a3389d`, `cfe6c9fb`) vs `382aca9b7e31` (`1d7aba09`) |
| freeze hash | `git show d603f6f…:corpus/evidence/round51/claims.md \| sha256sum` | equals working `claims.md` (`6afa1814ef95…`); freeze is an ancestor of HEAD |
| `build-c2-controls.py` | replayed with `TMPDIR` in scratch | output line-identical to committed `controls/c2-controls.txt` (40 lines), `C2=FAIL`×2, rc 0 |

## 2. Defects (severity order)

**F1 (calibration, worst): the round-51 row names a receipt that does not exist.** :133 says “measured values in
`corpus/evidence/round51/measure-after.txt` (header `tool-rev:`)”.
`ls corpus/evidence/round51/` → `measure-r50-at-tip.txt` only; `git log --all -- corpus/evidence/round51/measure-after.txt`
→ no commit; `git grep -n '^tool-rev:'` → rc 1, **no match in the tracked tree**. So the row’s measured-values pointer
dangles and the promised header-bearing receipt was never committed. (The four values themselves still reproduce — see
§1 — but the evidence pointer in the row is false.)

**F2 (operability): the row’s own `--skill SKILL.md` check can never pass on the real `SKILL.md`.**
`python3 corpus/evidence/round51/receipt-check.py corpus/evidence/round51/measure-r50-at-tip.txt --root . --skill SKILL.md`
→
```
RECEIPT_NO_REV corpus/evidence/round51/measure-r50-at-tip.txt
SKILL_NO_PIN SKILL.md
CHECKS=2 OK=0 FAILS=2
RECEIPT_CHECK=FAIL
rc=1
```
The receipt half is by design (`measure-r50-at-tip.txt:1-5` is a round-50 prose header; QUALITY 84 names that class). The
skill half is a defect: `header()` (`receipt-check.py:56-62`) scans **only the first five lines** of the file it is
given, but the only real pin in the tree is `SKILL.md:130` (`tool-rev: cf642c6… digest: sha256:6b975f91…`), and :133
mentions the phrase only in prose. Reachability proof: the same pin text in a one-line scratch file →
`SKILL_PIN_OK …/skillpin.md rev=72566c84e418 tool=tools/assimilate-rows.py`, `CHECKS=2 OK=2 FAILS=0`, rc 0. So
`SKILL_PIN_OK` is unreachable for the registered artifact and this leg is a permanent exit 1 independent of pin truth —
the tool’s docstring (“applies the same test to the header in the Gates row”) describes behaviour it does not have.
Related trap in the same row: `receipt-check.py` with no receipt → `CHECKS=0 OK=0 FAILS=0`, `RECEIPT_CHECK=PASS`, rc 0
(`nargs="*"`), so dropping the argument turns the check green.

**F3 (calibration): the `correction:` line miscounts its blocks.** :135 says “five blocks line-identical to
`corpus/evidence/round50/measure-after.txt`”. Block-split on `^$ ` of both files: the receipt has **4** command blocks
(`c1-count`, `c1-supplement`, `c2-count`, `stale-count-check`), and all **4** are line-identical to the round-50 file
(14/14, 8/8, 20/20, 11/11 non-blank lines). `stale-count-check` even replays `RESOLVED …` lines verbatim. Observed
count 4, stated 5.

**F4 (calibration): the row lists tools the gate admits as “controls”.**
`c1-count.py --tool corpus/evidence/round51/controls/forge-dirname.py` → `LEGS=5/5 C1=PASS` rc **0**;
`--tool …/tool-candidate1.py` → `LEGS=5/5 C1=PASS` rc **0**. :133 names both in its control list without stating their
outcomes, while `claims.md` C1 says “none reaches 3/5” (true only for the four do-nothing tools: 1/5, 2/5, 1/5, 2/5).
The committed `controls/c1-supplement-controls.txt` does record the forge passing the frozen gate and failing the
supplement (`SUPPLEMENT_LEGS=1/6`, replayed: `forge-dirname rc=1 SUPPLEMENT_LEGS=1/6`; `tool-candidate1 rc=1
SUPPLEMENT_LEGS=3/6`). The row’s control cell therefore overstates C1: the 5/5 target is reachable by the forge, and
only the post-freeze supplement separates it. Disclose in the row (the supplement is the discriminator, not the gate).

**F5 (calibration): `c3-controls-erratum.txt`, named in :133, is stale against its builder.**
`python3 corpus/evidence/round51/controls/build-c3-controls.py` prints **5** control blocks; the committed receipt
records **3**. Normalised line sets: builder 44 lines, receipt 28, receipt ⊂ builder (`only_committed` empty). The two
missing blocks are `# control DOTPATH (positive: C3=PASS expected, DANGLING must not grow)` → `CAP_ROWS=37 (base 36)
DANGLING=0 C3=PASS` and `# control DOTPATH at the pre-erratum counter` → `DANGLING=4 C3=FAIL`. History explains it:
receipt last written at `cfe6c9f`, builder extended at `4436e27` (`grep -c DOTPATH` = 0 at `cfe6c9f`). The receipt is
therefore not the builder’s output, and the positive control that guards the E1 extractor fix is unrecorded. Exit codes
still behave (`C3=FAIL` for the three negatives).

**F6 (evidence integrity): a wave-1 seat report is modified in the working tree, and its new claim is false.**
`git status --porcelain` → ` M .ufo/waves/round-51/w1/R51DraftSkillGates.md` (+11/−1, uncommitted; present at this seat’s first
`git status`, before any write-capable replay). The appended text asserts “at the tip: `--tool …/echo-tool.py` prints `LEGS=5/5` `C1=PASS` rc 0 and
`--tool …/const-tool.py` prints `LEGS=4/5`”. At the tip: `echo-tool` → `LEGS=2/5 C1=FAIL` rc 1; `const-tool` →
`LEGS=1/5 C1=FAIL` rc 1. Cause: both controls `os.execv` non-`--selftest` calls to `tool-before.py` (“round 51: the BASE
tool (E4)”), so only `LEGS=1/5`–`2/5` is reachable. A wave-1 report is read-only evidence per this wave’s brief; the
uncommitted claim is contradicted by the landed control set.

## 3. Residual risk / verification gaps

- `--root LANE` on `c1-count.py` does not move the round-50 pin: `R50_FIX`/`R50_PIN` are bound to the counter’s own
  `parents[3]` (`c1-count.py:45-47,98`). The `PIN_CHANGED` exit 2 was therefore exercised on a copied counter tree
  (`corpus/evidence/round51/c1-count.py` + `round50/c1-fixtures` with one byte appended → `PIN_CHANGED the round-50
  pinned fixtures differ from their pin or are missing`, rc 2); the row does not say the pin is root-independent.
- `CAP_ROWS>=36` / `POINTERS>=74` in :133 are BASE_REV observations (`c3-count.py:37,112-113` compares against
  `9ec1751a…`), not code constants; they coincide today.
- :133 says the five C1 legs each run “on nonce packages”; `SELFTEST_DEFAULT`/`LEGACY_ALL` read the lane and pinned
  packages. Wording only, legs full.
- Not run: `.ufo/waves/round-51/gen-w1-spec.py` / `gen-w2-spec.py` — they write `w1-spec.json` beside themselves (a lane write).
- The row’s remaining exit branches (C2 exit 1/2, C3 exit 1/2, `open-items-age` first-citing-round ambiguity) were not
  forced by mutation: those counters gate on lane bytes this seat may not perturb; the branch texts match the code paths
  read (`c2-count.py:79`, `c3-count.py:37`, `open-items-age.py:26-38`).
- Lane tree also carries untracked `w2.ready`, `w2.ready.dispatched`, `w2/`; untouched by this seat.

VERDICT: attacked both gate rows and the correction line by replaying every printed command and checking every stated
value at tip `72566c84` — 30+ values reproduce (findings 27/26, both digests, CF642C6 pin, LEGS=5/5, 6/6, C2/C3 legs,
MISMATCHES=0, the four r50-at-tip exits, the r49/r50 one-shot behaviour, write-set/refusal/exit-2 contracts); six defects
stand: F1 a named receipt that never existed, F2 an unreachable `SKILL_PIN_OK` (five-line window) plus a vacuous
zero-receipt PASS, F3 “five blocks” where four are identical, F4 forge/candidate1 passing the frozen gate 5/5 while
listed as controls, F5 a stale C3 control receipt missing its DOTPATH positive control, F6 an uncommitted wave-1 report
claim (`echo-tool` 5/5) falsified at the tip.
