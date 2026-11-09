# R99ReviewerC1 — C1 correctness review (leaf reviewer)

Scope: correctness of the C1 diff at F (`d41f4cd8b857c6de683e7be5c5e8125b32763a8e`, base `47ed34fa785288837f84cde9db15c41300854a78`). Shared clone at `/fast/scratch/hyaku/chousa-r99/R99ReviewerC1/repo`, checked out at F. Read `.ufo/waves/round-99/claims.md` + `claims.json` + `plans/round-99.md` first. No network. No production edits.

Commands reproduced (all run against `$S/repo`, never the live lane):

```
python3 -B corpus/evidence/round99/challenge-controls-r99.py --root . --work <scratch>
  -> exit 0, NEG_REFUSED=7/7 POS_ADMITTED=4/4 PROD_REFUSED=4/4 HARM_SAME=25/25
     BASE_NEG_ADMITTED=7/7 ORACLES_REJECTED=5/5, CHALLENGE_CONTROLS_R99=PASS
  receipt: .ufo/waves/round-99/w1/R99ReviewerC1-c1-battery.txt
git show 47ed34fa...:tools/gate-records.py > <scratch>/base-tool.py
python3 -B corpus/evidence/round99/challenge-controls-r99.py --root . --work <scratch> --tool <scratch>/base-tool.py --no-oracles
  -> exit 1, NEG_REFUSED=0/7 PROD_REFUSED=0/4 CHALLENGE_CONTROLS_R99=FAIL,
     byte-identical CASE lines to corpus/evidence/round99/before/c1-base.txt (header/comment lines excepted)
  receipt: .ufo/waves/round-99/w1/R99ReviewerC1-c1-base.txt
git diff 47ed34fa... d41f4cd8... -- tools/gate-records.py
  receipt: .ufo/waves/round-99/w1/R99ReviewerC1-gate-diff.txt
```

## (1) Module docstring CHALLENGE paragraph vs code — HELD (one observation)

`tools/gate-records.py:45-51` (docstring) vs `:109-128`, `:280-281`, `:307-308`:

- Forms: docstring "url/admit, and rev when path is corpus/captures/<24 hex>.txt" == admit branch unconditional `is_challenge(text)` (:280) and rev branch `CAP_RE.fullmatch(kv["path"]) and is_challenge(...)` (:307). `CAP_RE = corpus/captures/([0-9a-f]{24})\.txt` (:78), fullmatch needs the whole path. MATCH.
- Normalization: docstring "normalized, lower-cased text … at most CHALLENGE_MAX_WORDS (200) words AND contains one of CHALLENGE_MARKERS" == `t = norm(text).lower(); len(t.split()) <= 200 and any(m in t ...)`. Double-norm at admit site (`text = norm(fh.read())` then `norm` inside `is_challenge`) is idempotent. Threshold `<=` is at-most. MATCH.
- Marker count: tuple (:110-122) has 11 entries; docstring correctly does not hard-code a count ("one of CHALLENGE_MARKERS"). Frozen claims ("11 frozen") is true.

Observation (not a mismatch): the "Normalization" box (:53-54) says matching keeps case; CHALLENGE matching *additionally* lower-cases. The CHALLENGE paragraph itself discloses "lower-cased", so the conjunction is unambiguous, but a reader of only the box could misread case-sensitivity. No behavior is misstated.

`is_challenge` boundary verified: 200-word marker page refuses, 201-word admits (tested inline, `len==200 True / len==201 False`).

## (2) Marker provenance comment vs the four committed captures — HELD

Comment `tools/gate-records.py:104-108` claims S229/S021/S022/S032 → "cookies must be enabled"; S230 → "checking your browser" + "recaptcha"; S234 → "client challenge" + "a required part of this site couldn't load". Measured on normalized lower-cased committed bytes (via `is_challenge` internals):

- `b5b8d050eea0c638e95ba674` (S230): 23 words, hits `checking your browser`, `recaptcha`. sha256 `4f25f0b1...` == `KNOWN_SHA[0]`.
- `0954149536aaad411000e1fb` (S229): 18 words, hits `cookies must be enabled`. sha256 `7070b59c...` == `KNOWN_SHA[1]`.
- `58725f5e0ac436166546a5ec` (S021/S032 shared capture): same bytes as S229's, sha256 `7070b59c...`, hits `cookies must be enabled`. Refetch: S021 and S032 both key `58725f5e...` (HTTP 203). S022's PubMed capture `ff9013bd...` also hits `cookies must be enabled`; S022's other row is a Cochrane 404. So all four ids do have a committed capture carrying the marker (S022 via its second row). Provenance accurate.
- `b90988847e704a08aabc8321` (S234): 37 words, hits `client challenge`, `a required part of this site couldn't load` (capture has U+2019 `couldn’t`; `norm` maps it to `'`, so the ASCII marker matches). sha256 `c42ccd00...` == the third hash hard-coded in oracle o3.

Residual note: two markers — `ddos protection` and `are you a robot` — occur in no committed capture and in no battery fixture (CF/TURNSTILE/ATTN cover `just a moment`, `enable javascript and cookies to continue`, `verify you are human`, `attention required`). Their "widely served interstitial" provenance is asserted, not evidenced in-tree. That is an evidence gap in the comment, not a false behavior claim: the markers are inert until such a page is captured. Reported as low-severity observation.

## (3) Battery legs vs claims.md — HELD (with two low-grade observations)

- NEG verdict = `CHALLENGE` alone: `score()` requires `rc == 1 and verdict == "CHALLENGE"`, where `verdict` returns the whole `FAIL <token>`. `CHALLENGE,QUOTE_ABSENT` sorts differently and fails, so K1 (codes other than CHALLENGE alone) is enforced. GOOD.
- NEG split 3+4: n1–n3 are the committed S230/S229/S234 captures; n4–n7 are battery-written (CF string, TURNSTILE string, ATTN string, upper-cased double-spaced S230 via `re.sub(r"\s+","  ",…)`. "four written here" accurate. S233/S236 POS quotes are located in their captures (`norm(quote) in norm(capture)` both true); ARTICLE is 381 words and hits `recaptcha` + `just a moment` but `is_challenge == False` (over 200 words); SHORT is 28 words with no marker (see Finding F1 on the "30-word" number).
- PROD is the production path: legs run with `--root LANE` (the lane itself), records built from lane registry/refetch/git blobs (`prod_ts` from lane `refetch.tsv`, rev legs via `git -C lane show BASE:path`, first line with ≥3 words: rev-S230 line 1 `Checking your browser`, rev-S229 line 11 `Cookies must be`). S234's capture/refetch/registry rows exist only at F (absent at BASE, verified) — consistent with PROD running at F. Lab fixtures use `S901+` ids, `fixture.invalid` host, `sha(url)[:24]` keys, copied SOURCES/refetch + appended row per fixture: "a copy … plus one row per fixture" accurate. GOOD.
- HARM set = every knowledge/lesson `.md` with a GATE-RECORD line: battery pattern `^\s*GATE-RECORD\s` vs the tool's `lead_strip` + `^GATE-RECORD(?:\s|$)`. Checked over all 25 files — zero files differ between the two definitions, zero tool-records missed by the battery pattern. `HARM_SAME` compares `(returncode, stdout)` candidate-vs-base per file (stderr not compared; the tool writes nothing to stderr on this path). "byte-identical" in claims.md is stdout+exit, which is what is compared. The 25 include the new C2 entry. GOOD.

## (4) Oracles (o1–o5) — one FALSE docstring sentence (Finding F2); each still fails the battery

`CORPUS battery docstring :24-27` states: "o4 act only when ROOT has no `.git` (passes the scratch legs, fails PROD), o5 act only when ROOT has a `.git` (passes PROD, fails the scratch legs)", "o3 refuse only the sha256 of the four committed challenge captures".

Single-oracle battery scores (`--no-oracles`, each oracle as `--tool`; observed fail lines):

- o1-short-only: `POS p4 FAIL` (refuses every ≤200-word capture, marker or not).
- o2-marker-only: `POS p3 FAIL` (refuses marker at any length, so the 381-word article is refused).
- o3-known-bytes: `NEG n4,n5,n6,n7 FAIL` (admits the three battery-written challenge pages + upper-cased S230 whose bytes are not in the known set).
- o4-scratch-only: `PROD S230,S234 FAIL` (admits lane admit legs; NEG+POS pass).
- o5-lane-only: `NEG n1..n7 FAIL` (admits scratch legs; PROD passes).

The falsity: o1/o2 patch `is_challenge()`'s return, so they gate **both** admit and rev branches. o3/o4/o5 patch only the admit call site `            if is_challenge(text):` (each `src.count(old) == 1`, so the patch provably cannot touch the rev site). The rev site `CAP_RE.fullmatch(...) and is_challenge(...)` stays unconditional for o3/o4/o5. Consequences observed:

- o4 PROD rev legs PASS (refuse) on the lane (which *has* `.git`), i.e. o4 acts on rev records even when ROOT has `.git`. Battery output: `CASE PROD rev-S230 PASS`, `CASE PROD rev-S229 PASS`.
- Direct proof (scratch root without `.git`, `--repo` lane): o5 and o4 both print `GATE_RECORD … S230 FAIL CHALLENGE` on a rev record — o5 "acts" on rev in a no-`.git` root, contradicting "act only when ROOT has a `.git`".

So battery docstring sentences "o4 act only when ROOT has no `.git`", "o5 act only when ROOT has a `.git`", and "o3 refuse only the sha256 …" are false for the rev form: o3/o4/o5 refuse beyond their stated gate whenever a rev record names a capture blob. The frozen predicate `ORACLES_REJECTED=5/5` is still true (each oracle still forces `CHALLENGE_CONTROLS_R99=FAIL`, exit 1), and a rev-blind tool is still rejected — by the PROD rev legs, not by the oracles (verified: deleting the rev `CHALLENGE` append yields `PROD_REFUSED=2/4`, FAIL). But the battery's own stated oracle reasons misdescribe rev coverage, and there are no scratch-side rev legs to discriminate o3/o4/o5 rev behavior. Severity: medium (docstring + oracle-design gap; predicate unaffected).

Related imprecision (low): "the four committed challenge captures" in the o3 description counts capture *files* (`b5b8…`, `0954…`, `b909…`, `5872…`); distinct content hashes are three (`5872…` repeats `0954…`'s bytes). The oracle covers all three distinct hashes, so behavior is complete; the "four" counts files. Not a falsification of behavior.

## (5) Before receipt — HELD

`corpus/evidence/round99/before/c1-base.txt` records `git show BASE:tools/gate-records.py` + `--tool <base> --no-oracles` against the frozen battery. My re-run with the frozen battery + base tool reproduces all 20 CASE lines and both tally lines exactly (`NEG_REFUSED=0/7 … PROD_REFUSED=0/4 … FAIL`, exit 1). The header's "pre-freeze tree" vs F: the battery at F already contains the P0 rev legs (the before receipt shows `CASE PROD rev-*` lines), consistent with P0 having landed before the freeze. The base tool indeed admits all seven challenge records (`BASE_NEG_ADMITTED=7/7` in both receipts).

## (6) QUALITY 126 — meets the literal requirement; limit (f) is honest in substance (with a specificity caveat)

`corpus/QUALITY.md:1002` (126): a counter binds a claim only after a committed detection-forger battery has passed it, with limits recorded. Here the counter and battery are the same committed `challenge-controls-r99.py`; its five oracles are rejected (`ORACLES_REJECTED=5/5`), limits (a)–(f) are recorded in frozen `claims.md`. Limit (f) discloses: o4/o5 detect scratch-vs-lane only by `.git` presence; "a forger that detects the battery any other way (process tree, `S9xx` fixture ids, the `fixture.invalid` host) is not scored." That is the honest residue: a process-tree bot (`challenge-controls` in `ppid`'s cmdline), an env/cwd-name bot, or an `RLIMIT`/stdio bot would pass NEG/POS/PROD alike because every leg runs as a subprocess of the battery with those fixture markers, and none is scored. The PROD legs do catch host/`S9xx` gating as a side effect (PROD uses real URLs `S229/S230/S234` on the lane), but a pure process-tree forger survives — honestly admitted.

Caveat (observation, not a violation): (f)'s parenthetical names three detection families and covers the rest with "any other way", whereas 126's own tail enumerates residuals (pid-1/`/proc/1/cmdline`, `HOME==cwd`, argv/session, content fingerprints, timing/mtime). (f) is less specific than that precedent. A reviewer could fairly ask that (f) name the battery's own gratuitous telltales (the `work/lab` and `rec-*.md` layout, the `2026-11-09T04:00:33Z` fixture timestamp) — but the generic disclaimer plus limit (e)("does not show that every wrong tool fails it") carries the substance. I do not score this as a false statement.

Background check: QUALITY 229's lexical floor (`Checking your browser|Cookies must be enabled|Just a moment|reCAPTCHA`) matches `b5b8…` and `0954…` but misses `b909…` (S234) — verified with `/usr/bin/grep -lE`. The new CHALLENGE check catches it (`is_challenge(b909…) == True`). The round-99 motivation is accurately stated.

Other named limits audited: (a) lexical/>200 pass, (b) false refusal of ≤200-word marker documents, (c) no-NFKC (full-width/zero-width marker interiors pass — verified), (d) `url/unreach` and non-capture rev paths unchecked. (d) is slightly loose: the code checks only `corpus/captures/<24hex>.txt`, so a rev path under `corpus/captures/` with a different suffix (e.g. `.raw`) is also unchecked, while (d) says "not under `corpus/captures/`". The frozen sentence itself states the `.txt` form precisely; (d) understates the unchecked class. Low severity; noted, not scored as false.

## Findings

| # | file:line | defect | command / observed output |
|---|---|---|---|
| F1 | `claims.md:19` and battery `:17` ("a 30-word page") | Frozen number is false as stated: `SHORT` is 28 words (`len(SHORT.split()) == 28`), not 30. Predicate unaffected (`POS_ADMITTED=4/4` does not check word counts), but the sentence's number is wrong. | `python3 -B challenge-controls…` POS p4 `rc=0 verdict=OK PASS` (behavior fine); `len("Release notes…binary.".split()) == 28`. Receipt `.ufo/waves/round-99/w1/R99ReviewerC1-c1-battery.txt`. |
| F2 | `corpus/evidence/round99/challenge-controls-r99.py:24-27` | Oracle descriptions "o4 act only when …", "o5 act only when …", "o3 refuse only the sha256 …" are false for the rev form: o3/o4/o5 patch only the admit call site; the rev `CHALLENGE` branch stays unconditional (o4 refuses rev-S230/rev-S229 on a `.git` lane; o5 refuses a rev record in a no-`.git` scratch root). Each oracle still fails the battery (predicate holds), and rev-blind tools still fail via PROD rev legs — but rev coverage is by legs, not oracles, and the docstring says otherwise. | `python3 -B corpus/evidence/round99/challenge-controls-r99.py --root . --work <scratch> --tool <o4> --no-oracles` → `PROD_REFUSED=2/4`, `CASE PROD rev-S230 … PASS`; direct scratch-root rev probe: o4/o5 both `FAIL CHALLENGE`. Receipt `.ufo/waves/round-99/w1/R99ReviewerC1-c1-battery.txt`. |
| F3 (obs) | `tools/gate-records.py:104-108` | Markers `ddos protection`, `are you a robot` have no committed-capture or fixture provenance; provenance asserted, not evidenced. Inert until captured. | `/usr/bin/grep`-scan `corpus/captures/*.txt` → 0 hits for both markers. |
| F4 (obs) | `claims.md:42-48` limit (d); `(f)` | (d) understates the unchecked rev class (`.raw` under `corpus/captures/` also unchecked); (f) enumerates 3 detection families exhaustively by phrase rather than by 126-style list. Neither misstates behavior. | Code read `CAP_RE.fullmatch(kv["path"])` (`tools/gate-records.py:307`); receipt `.ufo/waves/round-99/w1/R99ReviewerC1-gate-diff.txt`. |

No other falsification found: C1 battery `PASS` at F, base-tool `FAIL`, `HARM_SAME=25/25` (all files, stdout+exit), verdict-exclusivity (K1), marker/capture provenance for the four committed captures, docstring↔code equivalence, and QUALITY-229 motivation all verify.

VERDICT: R99ReviewerC1 C1 fired — frozen "30-word page" is 28 words and the battery docstring's o3/o4/o5 "only when/only the sha" oracle descriptions are false for the rev branch, though the frozen predicate (7/7, 4/4, 4/4, 25/25, 7/7, 5/5, exit 0) still holds.
