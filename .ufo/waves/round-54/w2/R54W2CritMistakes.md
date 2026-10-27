# R54W2CritMistakes — attack on `corpus/lessons/round-54.md` `## Mistakes` (4 rows)

Tip moved under me: observed `178667d` then `25abbe8` (census end + W2 markers). All runs `TMPDIR=/fast/scratch/hyaku/chousa-r54/R54W2CritMistakes`, `PYTHONDONTWRITEBYTECODE=1`. No lane file written except this report.

## Row 1 (W2 reported dispatched) — survives, one honesty caveat

- Pointers resolve. `.ufo/reports/round-53/chousa.md:14` carries "W2: 43 seats dispatched … had not arrived" verbatim. `git cat-file -e d21eb285:.ufo/waves/round-53/w2.ready` → OK; `w2.ready.dispatched` and `w2-results.json` → `fatal: path … does not exist` (exit 128).
- Fix shown able to fail, ran: `python3 corpus/evidence/round50/wave-complete-check.py .ufo/waves/round-53/w2-spec.json .ufo/waves/round-53/w2 --rev d21eb285 --lane .` → 43 `MISSING` lines, `OK 0/43`, exit 1; on `w1-spec.json`/`w1` → `OK 49/49`, exit 0. The registry committed at `5a1a2063` holds 43 members, all `agentId: None` (counted: `agentId null: 43`).
- `captured-by: none — QUALITY 75's check existed and was not run` is honest but self-undercutting: the row's own evidence pointer IS the Q75 check (`wave-complete-check.py`, Q75's named check), so "none" means no run, not no criterion. Q75 governs filing (0/43 reports ⇒ no filing), the "dispatched" label needed Q99 — the row conflates both; the parenthetical saves it.
- Fix verified live: `.ufo/reports/round-54/chousa.md:97` writes "38 seats …, dispatched (`w2.ready.dispatched`)"; the marker exists on disk and in HEAD (`git cat-file -e HEAD:…w2.ready.dispatched` → OK, committed at `25abbe8`).

## Row 2 (anchors in undefined UTF-16LE form) — survives; two precision defects in the fix

- Pointers resolve: `corpus/SOURCES.md:110-111` name "(UTF-16LE text of the raw .doc capture)" with the nine `char N`s; `corpus/lessons/round-49.md:92-100` is the same nine offsets. S100 ×3 + S101 ×6 = nine ✓.
- Decode stats reproduce on `6dc68fd6b32ce9c8dfcebce8.raw`: `chars 64512 FFFD 263 0x0B 243 ctrls 18242` — matches the row (263 U+FFFD, 243 `0x0B`) and Q97 (64,512 / 18,242).
- `captured-by` honest: Q76's `decode-form-check.py` only requires the form be *named* (`FORM_NAMED`), verified reading QUALITY.md:800-808.
- Fix shown able to fail, ran: lane `python3 corpus/evidence/round53/pointer-anchor-check.py --root .` → `ANCHORED=16/16 UNANCHORED=0 BAD=0` exit 0 ✓. **But "mirror without the two dumps → BAD=6" is wrong: observed `ANCHORED=7/16 UNANCHORED=9 BAD=9` exit 1.** `BAD=6` reproduces only when S101's dump alone is missing (`ANCHORED=10/16 BAD=6`); S100 alone missing gives `BAD=3`. The claim's direction (fails) holds; the number is stale.
- **Latent defect in the fix's criterion (QUALITY 97, line 937): its old→new pairing transposes two quotes.** Tool-run `--locate` on the raw: `本规范推荐采用GB/T 7714中规定的顺序编码制格式著录` → `offset=12795` (the quote Registry-anchored at 11,993) and `文献类型及载体类型标志` → `offset=12963` (anchored at 12,161). SCORECARD.md:2745-2746 pair them correctly (`11993->12795`, `12161->12963`); Q97 prints `12,963` for 11,993 and `12,795` for 12,161. Consequence: the true drift is **+802 for five of six** (12795-11993=802, 12963-12161=802, 14049-13247=802, 11972-11170=802, 12007-11205=802; only 25123-34374=-9251), so Q97's "no constant repairs an old anchor" is false as stated — a single +802 repairs five anchors. The criterion's conclusion survives (the raw decode is undefined: FFFD/18,242 ctrls/binary preamble; an anchor must name a defined form), but its printed arithmetic does not.

## Row 3 (uncommitted swarm registry) — survives

- Pointers resolve: `lessons/round-53-verifier-spotcheck.md:13` names the untracked registry; `git cat-file -e d21eb285:.ufo/waves/round-53/w2/swarm-registry.json` → `exists on disk, but not in 'd21eb285'` (128); at `5a1a2063` → exit 0.
- `captured-by: the closure (non-author)` — honest; no criterion existed.
- Fix durable: this round's W2 registry is committed at `25abbe8` (`.ufo/waves/round-54/w2/swarm-registry.json` in its stat). I watched `census-end.txt` flip `??` → tracked as `25abbe8` landed — transient mid-wave, committed same round; the class did not recur in the committed tip.

## Row 4 (forgeable counter, RW-1) — survives; QUALITY 85 judgement correct

- Receipt verifies: `controls/c1-forge.txt` shows the rebuilt forge `LEGS=6/6 C1=PASS` (seed 7 + unseeded) and `SUPPLEMENT_LEGS=0/3`; candidate 3/3 per `measure-after.txt:53`. `corpus/evidence/round53/recurring.tsv` records RW-1 count 5 at r53 → "sixth round running" consistent.
- **QUALITY 85 decision: the row is right.** Q85's forge keyed on predictable work-dir/subtest *names* (`forge-dirname.py` read `--out` names); the r54 forge keyed on sibling *source files* (`src-<tag>/<name>.html` beside `doc-<tag>/`) and a reachable REAL oracle — a mechanism Q85 never mentions. Q88's `REAL_TEXT` pins the expected text but a delegating tool regenerates it. No pre-r54 criterion covered it; Q98's added sentence ("An oracle also has to be out of the tool's reach") is the right capture.
- Fix shown able to fail in code: `c1-supplement.py:44-52` `isolate()` copies each doc alone under a random name — kills the sibling-read forge; receipt shows `SUPPLEMENT_LEGS=0/3` for the rebuilt forge and all four controls.

## Missing mistakes (assignee's suggested + found)

1. **REGRESS outside the audit hook — a real counter defect not in the table.** `c1-count.py:286-291` spawns `round52/c1-count.py` unhooked; r52 `call()` (`round52/c1-count.py:214-216`) runs `[sys.executable, tool]` directly. The frozen predicate's "run as an ordinary command under an audit hook" over-describes: 1/6 legs is not hooked. Bounded: SHELL scored `r52 LEGS=1/9` (c1-controls.txt), and Q98 names the limit — disclosed, but the *predicate wording* overclaims; the Mistakes table doesn't carry it. Suggest a row-4 footnote rather than a new row.
2. **`.pyc` residue in the lane — minor, same class as row 3 but ignored.** `c1-supplement.py:39-40` and `c2-count.py:88-89` import siblings via `importlib` → `corpus/evidence/round54/__pycache__/{build-spans,c1-count,c2-count}.cpython-314.pyc` (23:14–23:19) and `round52/__pycache__/c1-count.cpython-314.pyc` (REGRESS import) on disk; `.gitignore:3` covers them so nothing dangles, but every counter run leaves artifacts — the seat brief's `PYTHONDONTWRITEBYTECODE` hint confirms it's observed noise. Row 3's fix ("commit each wave's registry") doesn't address ignored litter.
3. **Candidate's Traceback path (E2) — borderline missing.** The shipped candidate hung/Tracebacked on a malformed Clx the frozen MALFORMED leg never generates, and E2's fix is invisible to the claim ("no frozen leg reaches the Clx walk"). Disclosed in erratum + `tracked-deletion-check.py`; the process lesson (a post-candidate correctness fix unmeasurable by the frozen rule) is the deeper mistake, arguably row-4-adjacent. Defensible omission.
4. Transient only, not missing: `census-end.txt` was `??` mid-wave at `178667d`, committed at `25abbe8` — the lesson cites it and the tip carries it.

VERDICT: attacked `## Mistakes` rows 1–4 (pointers, captured-by honesty, shown-fail) and the suggested omissions; all four rows survive — found defects are confined to Q97's transposed pairing/+802-drift overstatement, row 2's stale `BAD=6`, an unhooked REGRESS leg, and ignored `.pyc` residue.

## Tooling
No installs. Used system python3 3.14 (`.pyc` names) and git; `soffice` not invoked.
