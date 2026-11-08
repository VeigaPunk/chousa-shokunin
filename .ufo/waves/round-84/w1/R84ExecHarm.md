# R84ExecHarm — C1 K3 (harm) + K4 + side-effect audit, round 84

Seat spec: fire-or-hold C1 kill rule K3 (harm) and K4 on real lane history, plus side-effect audit.
Landing rev: 03bbb4580b39b442be69f998fae2db48d64b8c93. Pre-repair rev: 81b81173 (pre-c7d29e1c).

## (0) Setup — exact commands exercised

- Archive: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 03bbb4580b39b442be69f998fae2db48d64b8c93 | tar -x -C /fast/scratch/hyaku/chousa-r84/R84ExecHarm`
- Pre-repair tool: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 81b81173:tools/gate-records.py`
- Per-file runner (scratch/run2.py): `python3 <tool> verify --root <tree> --repo /home/vgpnk/Projects/shokunin/chousa-shokunin <file>`, one run per file.
- Lessons list: 133 files under corpus/lessons/ (find). Other list: 158 files (git grep -l over rev). Receipts: `.ufo/waves/round-84/w1/R84ExecHarm/live-lessons.txt`, `live-other.txt`, `pre-lessons.txt`, `pre-other.txt` — each line `FILE <rel> rc=<rc> records=<n> ok=<k> fail=<m>` plus `FAIL` detail lines.

Tooling: read RULES.md first; no installs (strace 7.2, ltrace, python3 3.14.8 already present; pacman paused per guard).

## (1) Landing-record tabulation (task item 1)

**corpus/lessons/ (133 files): 21 records, 21 OK, 0 FAIL — both tools identical.** Only 5 files carry records:
round-80.md 4/4, round-81.md 6/6, round-82.md 5/5, round-83.md 3/3, round-84.md 3/3 (S214/S018/S023). All 128 other lesson files: records=0, exit 1 (no records is not a pass). Per-file table: `live-lessons.txt`.

**Other committed files (158): landing 220 records, 100 OK, 120 FAIL; pre-repair 220 records, 95 OK, 125 FAIL.** The 120 landing FAILs are almost entirely forgery fixtures, probes, mutants with quotes, and R83 audit artifacts. Full per-record table: `live-other.txt`.

### Verdict-flip analysis (pre vs landing, 9 file-level diffs, 0 lesson diffs)

| file | pre | landing | nature |
|---|---|---|---|
| .ufo/waves/round-83/w1/R83CriticClaims.md:40 | FAIL PARSE | OK | rev-quote leading-`"` boundary fix (M34 class) |
| R83CriticClaims/c2-k3-rev-quote-leading-dq.txt:4 | FAIL PARSE | OK | same fix |
| R83CriticClaims/rev-quote-entry-line56.md:1 | FAIL PARSE | OK | same fix (same record) |
| R83CriticClaims/rev-quote-leading-dq.md:1 | FAIL PARSE | OK | same fix |
| R83ExecForge.md:36 | OK | FAIL PARSE | non-ASCII numerals `line=2٢٢` (bytes `line=2 331 242 331 242`; see below) |
| R83ExecForge/forge/c052-line-arabic-222.md:1 | OK | FAIL PARSE | same non-ASCII numeral |
| R83ExecForge/forge/c057-rev-quote-leading-dquote.md:1 | FAIL PARSE | OK | leading-`"` fix |
| R83ExecHarm.md:105 | FAIL PARSE | OK | leading-`"` fix |
| R83ReviewerTool.md:19 | FAIL PARSE | OK | leading-`"` fix |
| R83ExecForge/forge/c026 (words=2٠), c053 (line=2٢٣), c058 (words=1٢) | FAIL (WORDS/LINE) | FAIL PARSE | still refused, code changed |

**HARM candidates (pre OK → landing FAIL): exactly 2, both non-ASCII-numeral records.** Neither fires K3: K3's exclusion sentence — "A refusal that closes a genuine K2 in-class form at the base revision is not harm" — covers them, because non-ASCII numerals per numeric field are a frozen K2 mutation class (claims class 2, seeded by the repair itself per QUALITY 164 / R83ExecForge Finding 1). The old tool's acceptance was a known forgery hole, not genuine behavior. Byte proof (c052 = R83ExecForge.md:36): `line=2٢٢` (U+0662 U+0662); blob b7803829:corpus/lessons/round-79-verifier-spotcheck.md line 222 carries the quote verbatim, so the pre-acceptance exploited the Unicode-digit class exactly as the r83 audit documented.

**FIXED by repair (material, non-flip): 6 records newly OK** — all leading-`"` rev quotes (e.g. R83ReviewerTool.md:19 `quote=" ".join(s.split())` — located: `git -C <lane> show 81b81173:tools/gate-records.py | sed -n '85p'` gives `return " ".join(s.split())`, and quote-locate returns True; R83ExecHarm.md:105 located at aca2a781:corpus/README.md:490). These were false PARSEs closed by the repair — K3-negative direction (less harm than before, not more).

### Hand-verified FAILs beyond flips (task item 2 — genuine defects in old records)

All are refused under BOTH tools; none is repair-caused, so none fires K3. All lie outside the 15 frozen positives + fresh positives (the K3 measurement set) and are not in corpus/lessons/ (which is 21/21 OK at landing):

- R80CriticA.md:336 `GATE-RECORD S195 rev=b7803829… path=corpus/lessons/does-not-exist.md` → FAIL LINE,REV both (illustrative truncated rev is no commit; path does not exist).
- R80ReviewerB.md:124 prose mention → FAIL PARSE both (line begins `GATE-RECORD in the round-80 lesson is audited…`, fits no form).
- R83ReviewerTool.md:35 `path=.ufo/waves/round-80/w2/Exec/SubjC2 RECEIPT/...` → FAIL PARSE both (space inside path is unexpressible in the record grammar; blob exists at 81b8117, proved by `git show`). Genuine old-record defect.
- R83ExecForge.md:67 `words=2٠` → FAIL PARSE both (non-ASCII numeral).
- R83ScribeLesson/receipts/05-considerthese.txt:15-17 bare `GATE-RECORD S009/S212/S213` → FAIL PARSE both (clipped receipt, not full records).
- corpus/evidence/round80/gate-grounding-check.py:13 template line `GATE-RECORD <id> rev=<40-hex>…` → FAIL PARSE both.
- .ufo/waves/round-83/w1/R83ExecHarm/04-fail-bytes-by-hand.txt (8 FAILs) — R83's own byte-by-byte audit of forged records (`bytez` LINE, 27-word QUOTE_LEN, etc.); genuine defects, documented as such.
- .ufo/waves/round-83/w1/R83MutationTool probes/logs (P03,P05,P06,P11,P22,P24,P27,P28,P30-P32,P34-P36) and R83ExecForge/forge/* mutants (c001-c058 subset + others) — deliberately forged fixtures, refused as designed (REFETCH/PARSE/CAPTURE_*/LINE/QUOTE_LEN/WORDS variants).

**No genuine committed record that both (a) is a real lesson record and (b) meets every docstring check is refused at landing.** The lesson corpus is 21/21 OK; the only pre-accepted→now-refused records are the two frozen-K2 non-ASCII-numeral forgeries.

## (2) K4 (setup leg) — direct test

Claims class 4 expects exit 2 + GATE_RECORDS_ERROR on stderr for a rev record with a non-git `--repo` at landing. Exercised:
`python3 tools/gate-records.py verify --root <tree> --repo /fast/scratch/.../nogit setup-leg-record.txt` where the record is R83ReviewerTool.md:19 (rev form, OK with the real repo).
Observed at landing (receipt `setup-stdout.txt`, `setup-stderr.txt`): prints `GATE_RECORD … S212 FAIL LINE,REV`, `GATE_RECORDS files=1 records=1 ok=0 fail=1`, **rc 1, stderr empty**. Same at pre-repair. **The tool misreports the setup leg** — git_blob returns None → REV,LINE codes instead of the usage error. Per claim wording ("counts as K2 if the tool misreports it"), this is a K2-class misreport, not a K4 rescue (K4 is about the whitelist control, which the counter's fresh positives already decide; I did not run the whitelist counter — out of my seat scope). Within my seat: K4's essence (a whitelist-only tool passing) is foreclosed by the K3 evidence above — the tool's verdicts track document bytes (21/21 lessons, quote/rev locator behavior, non-ASCII refusal), not the 15 frozen lines. I flag the setup leg as a hazard finding, not a K3 fire.

## (3) Side-effect audit (task item 3)

- **strace** (`strace -f -e trace=network,openat,unlink,rename,write`, receipt `strace.txt` + `strace-stdout.txt`): 0 socket calls, 0 unlink, 0 rename, 0 writes to any tree file (only `/dev/null` write events and Python's own reads). `find <tree> -newer tools/gate-records.py` → no corpus/.ufo file newer after the run. No `__pycache__`/`.pyc` in the tree (checked separately).
- **git subcommands observed in strace:** child PIDs open `.git/objects/...` read-only and run `git cat-file` (hierarchy visible in trace: git child opens `.git/objects/pack`, `.git/objects/<sha>`, writes the blob to fd 1). No other git subcommand; no `execve` of anything besides python/git.
- **Source grep** (`tools/gate-records.py`): exactly three subprocess calls, all `git -C <repo> cat-file [-t | blob]` (lines 179/183/186); every `open()` is read-only (`rb` or `encoding="utf-8", errors="replace"`); no socket/urllib/http imports; no os.remove/rename/shutil/system/Popen. The docstring's "It never fetches, never writes a file and never runs a mutating git command" matches the bytes.

Any write, network, or mutating git → FIRES K3 per seat spec: **none found; K3 side-effect clause did not fire.**

## (4) K3/K4 verdict per claim

- **K3 (harm): HELD.** No genuine lesson record that meets every check is refused at landing (21/21 OK, and 0 lesson diffs pre vs landing). The only records newly refused were frozen-K2 forgery forms (non-ASCII numerals) whose pre-acceptance is explicitly excluded from harm, and the repair additionally unblocked 6 genuine records. Side-effect clause: no writes/network/mutating git observed.
- **K4 (whitelist): HELD on my evidence.** The tool's verdicts are byte-determined (registry/refetch/capture/blob checks), not frozen-line recognition; the whitelist control stands or falls by the counter's fresh-positives leg (outside my seat), and the setup-leg misreport is a K2-class finding, not a whitelist pass.
- **C2: n/a** (not my seat).

VERDICT: R84ExecHarm C1 held — K3 not fired: all 21 lesson records pass at landing and the only newly-refused records are the frozen non-ASCII-numeral forgeries the r83 repair was built to close, with zero side effects observed.
