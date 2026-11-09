# R99SentinelC1 — bypass and side-effect audit of C1 at F

Seat: `R99SentinelC1`. Lane: `chousa`. Round 99.
Freeze attacked: `F = d41f4cd8b857c6de683e7be5c5e8125b32763a8e`.
Base: `47ed34fa785288837f84cde9db15c41300854a78`.

Scratch (all trees, fixtures and work dirs; deleted before yield):
`/fast/scratch/hyaku/chousa-r99/R99SentinelC1/`.
Attacked tree: `git clone -q --shared /home/vgpnk/Projects/shokunin/chousa-shokunin $S/repo`
then `git -C $S/repo checkout -q d41f4cd8b857c6de683e7be5c5e8125b32763a8e`
(`git -C $S/repo rev-parse --show-toplevel` = `/fast/scratch/hyaku/chousa-r99/R99SentinelC1/repo`).
Every battery ran against `$S/repo`, never against the live lane.

Tooling used (no install performed; all present on the host):
`/usr/bin/strace 7.2`, `git 2.56.0`, `Python 3.14.8`, `/usr/bin/grep (GNU grep) 3.12-modified`.

---

## Summary

The C1 battery passes at F and its predicate holds exactly as frozen. But the CHALLENGE
check enforces the rule on a **string form of the path**, while git resolves the path
**semantically**. The rev leg therefore admits a challenge page through a path spelling
the claim's named limits do not cover, and the round-98 defect class (a GATE-RECORD
quoting S230's http-200 reCAPTCHA page, `OK`, exit 0) is re-openable at F.

**C1 fired.** One uncovered admission (F-1), plus three secondary findings (F-2, F-3, F-4).
**C2 held** on every mechanical check I could run.

---

## F-1 (severity: high) — the rev-leg CHALLENGE check is bypassed by path spelling

### Claim text under test

`claims.md` C1, sentence:

> a url/admit record, or a rev record whose path is `corpus/captures/<24 hex>.txt`, fails
> with code CHALLENGE (exit 1) when its capture's normalized, lower-cased text has at most
> 200 words and contains one of the 11 frozen `CHALLENGE_MARKERS`.

Named limit (d):

> The url/unreach form has no capture and is not checked; a rev record whose path is not
> under `corpus/captures/` is not checked.

### The gap

`tools/gate-records.py:307` gates the rev-leg check on a **regex** against the record's
path string:

```python
if CAP_RE.fullmatch(kv["path"]) and is_challenge("\n".join(lines)):
    codes.append("CHALLENGE")
```

`CAP_RE = re.compile(r"corpus/captures/([0-9a-f]{24})\.txt")` (line 78). Meanwhile the
blob itself is fetched by `git_blob()` (line 227-238) as `git cat-file blob <rev>:<path>`,
and **git resolves that path semantically**: it accepts a leading `./`, a repeated `./`,
and an embedded `//`, and it resolves all of them to the *same blob*. The check and the
fetch use two different notions of "the same path".

So a rev record whose `path=` is spelled `./corpus/captures/<24 hex>.txt` fetches exactly
the same challenge-page blob, but skips the CHALLENGE check entirely, because
`CAP_RE.fullmatch("./corpus/captures/…")` is False.

### Exploit path (measured)

Record (S230's committed reCAPTCHA capture, blob `66f24cb2b71fc4ff29c439e0c994b2a28e9dbde6`):

```
GATE-RECORD S230 rev=d41f4cd8b857c6de683e7be5c5e8125b32763a8e path=./corpus/captures/b5b8d050eea0c638e95ba674.txt line=1 words=3 quote=Checking your browser
```

Command:

```
$ python3 -B tools/gate-records.py verify --root . <probe>.md
```

Observed at F (exit 0, admitted):

```
GATE_RECORD <probe>.md:3 S230 OK
GATE_RECORDS files=1 records=1 ok=1 fail=0
exit=0
```

Observed at F with the canonical spelling of the **same blob** (refused):

```
GATE_RECORD <probe>.md:3 S230 FAIL CHALLENGE
GATE_RECORDS files=1 records=1 ok=0 fail=1
exit=1
```

Blob identity is not in doubt — `git rev-parse` returns the same object for both spellings:

```
$ git rev-parse d41f4cd…:corpus/captures/b5b8d050eea0c638e95ba674.txt d41f4cd…:./corpus/captures/b5b8d050eea0c638e95ba674.txt
66f24cb2b71fc4ff29c439e0c994b2a28e9dbde6
66f24cb2b71fc4ff29c439e0c994b2a28e9dbde6
```

Receipt: `R99SentinelC1-round98-repro.txt` (also `R99SentinelC1-bypass-matrix.txt`).

This is exactly the defect round 98 routed to round 99 (`corpus/lessons/round-98.md:63`,
`corpus/QUALITY.md:1432`): a GATE-RECORD quoting S230's http-200 reCAPTCHA body passes
every check with `OK`, exit 0. The round-98 receipt file itself now flips at F — good,
the admit form is closed — but the rev form re-opens it under a path spelling.

### Full admission matrix at F (measured)

| rev `path=` spelling | git resolves | `CAP_RE.fullmatch` | verdict at F |
|---|---|---|---|
| `corpus/captures/<hex>.txt` | blob | True | **CHALLENGE** (exit 1) |
| `./corpus/captures/<hex>.txt` | blob | False | **OK** (exit 0) — admitted |
| `.//corpus/captures/<hex>.txt` | blob | False | **OK** (exit 0) — admitted |
| `././corpus/captures/<hex>.txt` | blob | False | **OK** (exit 0) — admitted |
| `./corpus/captures//<hex>.txt` | blob | False | **OK** (exit 0) — admitted |
| `./corpus//captures/<hex>.txt` | blob | False | **OK** (exit 0) — admitted |
| `./corpus/captures/./<hex>.txt` | blob | False | **OK** (exit 0) — admitted |
| `corpus/captures/<hex>.raw` | blob | False | **OK** (exit 0) — admitted |
| `./corpus/captures/<hex>.raw` | blob | False | **OK** (exit 0) — admitted |
| `corpus/captures/<HEX>.txt` | not a blob | False | REV/LINE failure — refused |
| `corpus/captures/<hex>.TXT` | not a blob | False | REV/LINE failure — refused |

Command: `python3 -B tools/gate-records.py verify --root . <probe>.md`, run from
`$S/repo` at F. Receipt: `R99SentinelC1-bypass-matrix.txt`.

### Why no named limit covers this

- Limit (a) (lexical) is about the *marker text*, not the path spelling — it does not apply.
- Limit (c) (normalization) is about curly quotes / whitespace / case — it does not apply.
- Limit (d) says "a rev record whose path is not under `corpus/captures/` is not checked".
  The `./corpus/captures/…` spelling **is** under `corpus/captures/` (git puts it there;
  `git rev-parse` proves the blob identity). So limit (d) does not license the admission:
  the exemption limit (d) grants is for paths *outside* the capture directory, and this
  path is inside it.
- Limit (e) (oracle set) is about the battery's oracles — it does not apply.

**This is an uncovered admission.** Under the kill rules as frozen it does not trip K1
(K1 is scoped to the battery's NEG/PROD records, which use the canonical spelling), but it
is exactly the failure the round exists to remove, and the frozen sentence's wording
("a rev record whose path is `corpus/captures/<24 hex>.txt`") describes an intent the
instrument does not enforce.

### The battery cannot see it

The battery's PROD rev leg builds its path by string concatenation only
(`corpus/evidence/round99/challenge-controls-r99.py:176`):

```python
path = f"corpus/captures/{CAP[sid][1]}.txt"
```

so the battery only ever exercises the canonical spelling. I confirmed the battery has
real teeth on the rev leg *existing* but none on it being *correct*: a mutant that drops
the rev-form check entirely is correctly rejected —
`PROD_REFUSED=2/4 … CHALLENGE_CONTROLS_R99=FAIL`, exit 1 — while the shipped F tool,
which admits the bypass, passes. A path-spelling mutant would also pass. This is limit (e)
doing its job, but it means the battery's `PROD_REFUSED=4/4` does **not** establish that
the rev form is closed; it establishes only that one spelling is closed.

### Smallest remediation (tested, not applied)

Normalize the path before the regex test, and widen the guard from "exactly this string"
to "resolves under the capture directory". Two variants I built and ran:

Variant A (`FIXED-A`, receipt `R99SentinelC1-fixed-tool-A.py`) —
`posixpath.normpath(kv["path"])` then `CAP_RE.fullmatch`:

```
--- FIXED-A (normpath + CAP_RE.fullmatch)
    corpus/captures/<hex>.txt         CHALLENGE
    ./corpus/captures/<hex>.txt       CHALLENGE
    .//corpus/captures/<hex>.txt      CHALLENGE
    ././corpus/captures/<hex>.txt     CHALLENGE
    ./corpus/captures//<hex>.txt      CHALLENGE
    ./corpus//captures/<hex>.txt      CHALLENGE
    ./corpus/captures/<hex>.raw       OK   <-- ADMITTED
    corpus/captures/<hex>.raw         OK   <-- ADMITTED
```

Variant B (`FIXED-B`, receipt `R99SentinelC1-fixed-tool-B.py`) — `normpath` **and** guard
on `rp.startswith("corpus/captures/")` (so the `.raw` twin of the same served bytes is
also covered):

```
--- FIXED-B (normpath + startswith("corpus/captures/"))
    corpus/captures/<hex>.txt         CHALLENGE
    ./corpus/captures/<hex>.txt       CHALLENGE
    .//corpus/captures/<hex>.txt      CHALLENGE
    ./corpus/captures//<hex>.txt      CHALLENGE
    ./corpus//captures/<hex>.txt      CHALLENGE
    corpus/captures/<hex>.raw         OK   <-- ADMITTED
```

Variant B still admits the `.raw` twin, because `is_challenge` counts the **raw** HTML's
words (620 for S230's `.raw`, 230 for S234's) against the 200-word ceiling — the `.raw`
body is over the limit while its `.txt` extract is under it. Closing that needs the check
to run on the extracted text form for `.raw` paths too, or the ceiling applied to the
extract rather than the raw bytes.

Both variants keep the frozen battery green —

```
NEG_REFUSED=7/7 POS_ADMITTED=4/4 PROD_REFUSED=4/4 HARM_SAME=25/25 BASE_NEG_ADMITTED=7/7 ORACLES_REJECTED=5/5
CHALLENGE_CONTROLS_R99=PASS
```

— and keep the harm files byte-identical (`GATE_RECORDS files=25 records=186 ok=185 fail=1`,
the one failure being the pre-existing `round-96-verifier-spotcheck.md:61` PARSE, which
the BASE tool reproduces identically on the BASE file, so it is not a round-99 regression).

I did **not** apply any of this: this seat is read-only on production files.

---

## F-2 (severity: medium) — the battery's docstring misstates the o3 oracle's coverage

`corpus/evidence/round99/challenge-controls-r99.py:25-26`:

> o3 refuse only the sha256 of the four committed challenge captures

The byte list `KNOWN_SHA` has **three** digests, and at F the tree holds **five**
committed challenge `.txt` captures, not four:

| capture | sha256 of `.txt` | distinct digest? |
|---|---|---|
| `0954149536aaad411000e1fb.txt` | `7070b59c…` | shared with two others |
| `58725f5e0ac436166546a5ec.txt` | `7070b59c…` | shared |
| `ff9013bd7d9387e45cd6e000.txt` | `7070b59c…` | shared |
| `b5b8d050eea0c638e95ba674.txt` (S230) | `4f25f0b1…` | distinct |
| `b90988847e704a08aabc8321.txt` (S234) | `c42ccd00…` | distinct |

So: five captures, three distinct digests, and the oracle's list covers all five
(`covered_by_o3 = True` for each). The docstring's "four" is wrong on both counts
(it should say five captures / three digests), and the "four" it echoes is the count
QUALITY 229's grep produces — which **misses S234 entirely**, because that pattern does
not contain "Client Challenge". The round-99 battery's own `KNOWN_SHA` does contain
S234's digest, so the oracle is right and only its description is stale.

Command:
`python3 -c "…sha256 each of the five flagged .txt captures; test membership in KNOWN_SHA + the third digest…"`.
Observed: `committed challenge .txt captures covered by o3's byte list: 5/5 (o3 list size = 3 digests)`.

Severity is medium rather than low because the docstring is the only place a reader
learns what the oracle detects, and a "four" that tracks the stale QUALITY-229 count
invites the next author to reuse the same under-counting.

---

## F-3 (severity: low) — `is_challenge` is defeated by any marker mutation the tool's own normalization does not undo

Named limit (c) says:

> Markers are matched after the tool's normalization only (curly quotes, whitespace,
> lower case): no NFKC, so full-width letters or a zero-width character inside a marker
> pass.

Measured, that limit is **accurate** — every one of these mutations of S234's real
capture (all eleven markers rewritten, so none survives) makes the challenge page
**admitted** (`OK`, exit 0) instead of refused:

| mutation of every marker | verdict at F |
|---|---|
| zero-width space (U+200B) between words | **OK** — admitted, exit 0 |
| full-width (U+3000) between words | **OK** — admitted, exit 0 |
| HTML entity `&#32;` for space | **OK** — admitted, exit 0 |
| HTML entity per letter | **OK** — admitted, exit 0 |
| soft hyphen (U+00AD) | **OK** — admitted, exit 0 |
| word joiner (U+2060) | **OK** — admitted, exit 0 |
| NBSP (U+00A0) | CHALLENGE — refused (NBSP is whitespace to `str.split`) |
| control (S234 unmodified) | CHALLENGE — refused |

Receipt: `R99SentinelC1-probe-marker-mutations.txt`. Command: for each case, write the
mutated capture into a scratch lane, build a `url/admit` record quoting a marker-free
phrase from it, then `python3 -B tools/gate-records.py verify --root <lab> <probe>.md`.

**This is a named limit, not an uncovered admission** — it is reported here only to record
that limit (c) was measured rather than assumed, and because two of the six mutations
(HTML entity, soft hyphen) are not mentioned in limit (c)'s own wording, which names only
"full-width letters or a zero-width character".

One realism note in favour of the limit: `tools/capture-fetch.py:83` calls
`html.unescape`, so a stored `.txt` normally has entities decoded. But the extraction is
skipped when the body does not match the HTML sniff at `capture-fetch.py:100` — I confirmed
this on a committed capture (`0c706963f48059d383b89715.txt` stores raw HTML with 221 live
tags and live `&nbsp;`/`&ldquo;`/`&rdquo;`/`&ensp;` entities, because the file starts with
a UTF-8 BOM and the sniff fails). So entity-bearing stored text is real in this lane, and
a challenge page served with entities and a sniff-defeating prefix would be admitted.

---

## F-4 (severity: medium) — the battery cannot distinguish a correct rev-branch check from a wrong one

The frozen sentence says the rev-form check applies to "a rev record whose path is
`corpus/captures/<24 hex>.txt`" and that the capture's text is judged. The battery's two
PROD rev legs quote **line 1** of the challenge capture, and line 1 of every committed
challenge capture happens to *be* the marker line. So a tool that checks only the
**quoted line** — rather than the whole blob — is indistinguishable from a correct one by
the battery.

I built that mutant (`is_challenge(lines[i - 1])` instead of
`is_challenge("\n".join(lines))`) and ran it through the frozen battery:

```
$ python3 -B corpus/evidence/round99/challenge-controls-r99.py --root . --work <scratch> \
    --tool <line-only mutant> --no-oracles
CASE PROD rev-S230 rc=1 verdict=CHALLENGE PASS
CASE PROD rev-S229 rc=1 verdict=CHALLENGE PASS
NEG_REFUSED=7/7 POS_ADMITTED=4/4 PROD_REFUSED=4/4 HARM_SAME=25/25 BASE_NEG_ADMITTED=7/7 ORACLES_REJECTED=0/0
CHALLENGE_CONTROLS_R99=PASS
exit=0
```

**The battery PASSES it** — but the mutant is materially weaker. Quoting S234's challenge
capture on a **non-marker** line:

```
record: GATE-RECORD S234 rev=d41f4cd… path=corpus/captures/b90988847e704a08aabc8321.txt
        line=15 words=3 quote=extension, network issues,
  F-shipped          rc=1 CHALLENGE
  line-only mutant   rc=0 OK
```

So the mutant admits a challenge page whenever the quoted line happens to lack a marker —
and the battery cannot see that. (S234's marker line is line 8; line 15 is ordinary
prose from the same challenge page.)

Two consequences:

1. **The battery's `PROD_REFUSED=4/4` establishes less than the frozen sentence claims.**
   It shows the rev branch fires on two specific records, not that the rev branch judges
   the capture's *text*.
2. It compounds F-1: a *single* battery run cannot distinguish four materially different
   rev-branch behaviours — the correct check (whole blob, canonical path), the F-1
   bypass (whole blob, path-string-gated), the line-only mutant, and the
   rev-check-removed mutant. Only the last of the four is rejected. The frozen predicate
   `PROD_REFUSED=4/4` therefore cannot certify the rev leg.

This is arguably inside named limit (e) ("The battery's oracle set is five patches; it
does not show that every wrong tool fails it"), so I record it as a strengthening of that
limit rather than as an uncovered admission: **the limit is understated.** The oracle set
is not the only gap — the *case* set (NEG/POS/PROD) is also blind to the rev branch's
scope, because the two rev cases quote the marker line by construction.

Smallest remediation (not applied): add a PROD rev case that quotes a **non-marker** line
of a committed challenge capture, and a second PROD rev case with a non-canonical but
git-resolvable path spelling. Both would then discriminate.

---

## Part (2) — false refusals in the real store at F

`is_challenge` (imported from the F tool) run over **every** `corpus/captures/*.txt` at F:

| capture | words | marker matched | a real document? | cited by a GATE-RECORD in corpus/knowledge or corpus/lessons? |
|---|---|---|---|---|
| `0954149536aaad411000e1fb.txt` (S229) | 18 | `cookies must be enabled` | no — PubMed cookie wall | **no** (0 lines) |
| `58725f5e0ac436166546a5ec.txt` | 18 | `cookies must be enabled` | no — cookie wall | **no** (0 lines) |
| `ff9013bd7d9387e45cd6e000.txt` | 18 | `cookies must be enabled` | no — cookie wall | **no** (0 lines) |
| `b5b8d050eea0c638e95ba674.txt` (S230) | 23 | `checking your browser`, `recaptcha` | no — NCBI reCAPTCHA | **no** (0 lines) |
| `b90988847e704a08aabc8321.txt` (S234) | 37 | `client challenge`, `a required part of this site couldn't load` | no — RIPR "Client Challenge" | **no** (0 lines) |

Five flagged of 100 stored `.txt` captures; all five are genuine interstitial pages; **no
committed GATE-RECORD line in `corpus/knowledge` or `corpus/lessons` cites any of them**,
so the HARM leg is unaffected in practice (confirmed: `HARM_SAME=25/25`).

Note the marker `a required part of this site couldn't load` matches S234's capture only
because S234's text uses the **typographic** apostrophe `’` and the tool's `norm()`
folds U+2019 to `'` (`tools/gate-records.py:97`). That folding is load-bearing here.

**No false refusal observed.** The three shortest real documents in the store
(`0cebd3c8…` 0 words, `ad3010d2…` 0 words, `52db06f9…` 1 word) are not flagged; of the
20 captures at or under 200 words, exactly the 5 above are flagged. The nearest
non-challenge neighbour is `be74dca6…` at 25 words, not flagged.

---

## Part (3) — side-effect audit

### `strace -f -e trace=file,network,process` over the battery

```
$ strace -f -e trace=file,network,process -o R99SentinelC1-strace-battery.txt \
    python3 -B corpus/evidence/round99/challenge-controls-r99.py --root . --work $W
battery exit=0
```

- **Writes outside `--work`: 0.** Every `openat(..., O_WRONLY|O_CREAT|O_APPEND|O_TRUNC)`
  in the trace (350 write-ish events in total) is under `$W`.
- **Writes into the cloned repo tree: 0.** **Writes into the live lane: 0.**
  **Writes into `/home/vgpnk` outside scratch: 0.**
- **Sockets: 0.** No `socket(AF_INET…)`, no `connect(`. (Zero `AF_UNIX` either.)
- **Git verbs invoked: `cat-file` and `show` only** — both read-only. No `commit`, `add`,
  `checkout`, `reset`, `update-index`, `update-ref`, `gc`, `repack`, `merge`, `rebase`,
  `clean`, `stash`.
- **Writes into `.git`: 0.** (Git may create its own internal lock/pack files for
  read-only object access, but none appeared.)
- **No `unlink`, no `rename`** anywhere in the trace — nothing deleted.

Receipt: `R99SentinelC1-strace-battery.txt`.

### `strace -f -e trace=file,network,process` over `gate-records.py verify`

```
$ strace -f -e trace=file,network,process -o R99SentinelC1-strace-gate-verify.txt \
    python3 -B tools/gate-records.py verify --root . corpus/knowledge/quotation-error-rates-r99.md corpus/lessons/round-98.md
exit=0
```

Zero write syscalls of any kind, zero sockets. The tool reads committed lane bytes and
runs only `git cat-file`. Receipt: `R99SentinelC1-strace-gate-verify.txt`.

### Python audit hook over the battery (independent of strace)

I patched `builtins.open` / `os.open` / `subprocess.run` in-process and re-ran the
battery:

```
EXIT 0
=== WRITE events outside --work: 0
=== all EXEC events (unique):
   /usr/bin/python3 -B .../tools/gate-records.py verify --root .../repo corpus/knowledge/press-2015-statement-questi
   ... (all 25 harm files, the 11 scratch legs, the 4 prod legs, the 5 oracle tools)
   git -C .../repo show 47ed34fa…:corpus/captures/0954149536aaad411000e1fb.txt
   git -C .../repo show 47ed34fa…:corpus/captures/b5b8d050eea0c638e95ba674.txt
   git -C .../repo show 47ed34fa…:tools/gate-records.py
```

Every exec is the tool under test or a read-only `git show`. Receipt:
`R99SentinelC1-audit-hook.txt`.

### Is the battery's docstring exact about what it reads and writes?

**Reads** — the docstring says "Reads lane files and `git show BASE:<path>`". True, and
complete: the battery also runs `git show BASE:corpus/captures/<hex>.txt` for the two
PROD rev legs (base-rev-S230, base-rev-S229) and `git show BASE:tools/gate-records.py`
for the before-control — all `git show`, all within the stated description.

**Writes** — the docstring says "writes only under `--work`". True, and confirmed
independently twice above (strace and the audit hook).

One imprecision: the docstring says the battery "writes only under `--work`", but the
`Lab` fixture copies the lane's `corpus/SOURCES.md` and `corpus/evidence/round57/refetch.tsv`
into `<work>/cand/lab/`, and `score()` starts with `shutil.rmtree(work)` on that
subdirectory — a delete inside `--work`. On my run that rmtree was a **no-op** (the
subdirectory did not yet exist), so the trace shows **0** `unlink`/`unlinkat` events; on a
re-run into an existing `--work` it would delete inside `--work` only. Either way the
boundary holds and the lane is never touched, but the docstring mentions no deletion at
all.

### The tool's own docstring at F
`tools/gate-records.py:45-49` documents CHALLENGE as applying to "url/admit, and rev when
path is corpus/captures/<24 hex>.txt" and states the rule is lexical. The docstring is
*accurate about what the code does* — but it, like the claim, describes the check as
path-shaped rather than resolution-shaped, which is exactly the F-1 gap. The docstring's
own words "the capture is an interstitial challenge page, not the document" state the
intent; the implementation does not meet it for a `./`-spelled path.

### One deviation to disclose

One of my probe scripts contained a leftover debug line, `open("/tmp/NO","w")`, which
created an empty file at `/tmp/NO` — outside my scratch, which the seat brief forbids.
I found it in the final cleanup pass, inspected it (0 bytes, no content), removed it with
`rm -f /tmp/NO`, and re-checked `/tmp` for any other file of mine (none). No other
command in this seat wrote outside `$S` or the lane's `w1/` directory; the strace and
audit-hook evidence above cover the battery and the tool, and every fixture I wrote went
to `$S/w1/probes/`. I record it rather than leave it unmentioned.

---

## What held (recorded so the audit is not read as a blanket rejection)

- **C1 battery predicate at F — exactly as frozen.**
  `python3 -B corpus/evidence/round99/challenge-controls-r99.py --root . --work <scratch>`
  → `NEG_REFUSED=7/7 POS_ADMITTED=4/4 PROD_REFUSED=4/4 HARM_SAME=25/25 BASE_NEG_ADMITTED=7/7 ORACLES_REJECTED=5/5`,
  `CHALLENGE_CONTROLS_R99=PASS`, exit 0. Receipt: `R99SentinelC1-c1-battery-at-F.txt`.
- **C1 before-control reproduces byte-for-byte.** The committed
  `corpus/evidence/round99/before/c1-base.txt` shows `NEG_REFUSED=0/7 … PROD_REFUSED=0/4
  … CHALLENGE_CONTROLS_R99=FAIL`, exit 1. My own run of the same command against
  `47ed34fa…:tools/gate-records.py` reproduces every CASE line and the tally identically.
  Receipt: `R99SentinelC1-c1-before-control.txt`.
- **The battery has real teeth on the rev leg existing.** A mutant that disables the
  rev-form CHALLENGE check entirely is rejected: `PROD_REFUSED=2/4 … FAIL`, exit 1.
- **C1's HARM leg is genuinely byte-identical.** All 25 harm files, 186 records, verified
  through the F tool; the single FAIL is `corpus/lessons/round-96-verifier-spotcheck.md:61`
  PARSE, which the **BASE** tool reproduces identically on the **BASE** copy of that file —
  pre-existing, not a round-99 regression.
- **C2's four counting commands all pass at F, exactly as frozen.**
  - `python3 -B tools/gate-records.py verify --root . corpus/knowledge/quotation-error-rates-r99.md`
    → `GATE_RECORDS files=1 records=25 ok=25 fail=0`, exit 0.
  - `bash tools/research-gate.sh verify-metadata corpus/knowledge/quotation-error-rates-r99.md --root .`
    → `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN`, exit 0.
  - `python3 -B tools/search-rerun.py verify corpus/knowledge/quotation-error-rates-r99.md --root .`
    → `rev_match=4/4`, `SEARCH_RERUN: CLEAN`, exit 0.
  - `python3 -B corpus/evidence/round99/entry-controls-r99.py --root .`
    → `QUOTES=23/23 FIELD=9/9 IDENTITY=2/2 WARRANTS=8/8 NUMBERS=6/6 TOPIC=1/1
      NUMBERS_SOURCED=6/6 BASE_TOPIC_HITS=0 BASE_ENTRY=absent FORGERY_REFUSED=10/10 ACCEPTED=2/2`,
    `ENTRY_CONTROLS_R99=PASS`, exit 0.
- **C2's structural claims independently re-derived** (not taken from the controls):
  - 23 quote rows present (J0-J8 = 9, G0-G13 = 14); **23/23 are verbatim in their own
    capture** (S233 for G*, S236 for J*).
  - J0 is the S236 record's `title`; J1-J8 are all inside that record's `abstractText`.
    The S236 JSON carries pmid `26528420`, doi `10.7717/peerj.1364`, `pubYear` 2015,
    `journalInfo.journal.title` `PeerJ`, `journalInfo.volume` `3`, `authorString`
    `Jergas H, Baethge C.` — K3 satisfied from the capture itself.
  - 8 decision-table rows.
  - **K2 mechanically re-checked**: every number in every Do cell is present in that
    row's own warrant quotes (11,9% / 25.4% / 14.5% / 28 → J1,J2,J5,G10;
    6.7% → J3,J8,G7; 64.8% → G11). Zero violations.
  - `BASE_TOPIC_HITS=0` re-derived independently by grepping every BASE knowledge file
    for "quotation error" (case-insensitive): 0 hits. The entry is absent at BASE
    (`git cat-file -t 47ed34fa…:corpus/knowledge/quotation-error-rates-r99.md` → not found).
- **C1's other stated numbers hold.** The battery's own fixtures measure as the claim
  says: `ARTICLE` = 381 words (claim: "a 300-plus-word article") and contains both
  `recaptcha` and `just a moment`; `SHORT` = 28 words (claim: "a 30-word page" — 28, not
  30; see below); the four PROD url/admit and rev legs do use `--root` the lane; the two
  committed POS captures are S233 (8,455 words) and S236 (JSON).

**One number in the frozen claim does not match the instrument.** `claims.md` C1 says the
battery admits "a 30-word page with no marker". The `SHORT` fixture is **28** words
(`"Release notes. Version 2.1 fixes the date parser, …"`, `len(SHORT.split()) == 28`).
Neither the battery's docstring nor the claim says "30" anywhere else; the count is
descriptive prose about a POS leg, not a predicate value, and the leg passes either way.
I record it as a deviation from an expected value rather than hide it. The
`ARTICLE` fixture is 381 words against the claim's "300-plus-word" — that one holds.

---

## Note on concurrent L1 work (observed, not mine)

While I was auditing, the L1's working tree changed. `git status` in the live lane now
shows `corpus/evidence/round99/challenge-controls-r99.py` modified, and the diff corrects
**both** of my docstring findings independently:

> `p4 a 28-word page with no marker (F2: "30-word" was wrong, R99ReviewerC1 F1)`
> `o3 (url/admit call) refuse only the sha256 of the three committed challenge capture
>  texts S230, S229/S021/S022/S032 (one text) and S234 … (F2 wording, R99ReviewerC1 F2)`

So F-2 and the "30-word" deviation are already addressed in the lane's in-flight tree
(attributed there to `R99ReviewerC1`). I am **not** claiming credit for them, and I make no
edit to that file — the L1 owns it.

`tools/gate-records.py` is **unchanged** at F (`git rev-parse HEAD:tools/gate-records.py`
= `5a3189e0c68bdf1df599b611b808c048bc8ca269` = the F blob), so **F-1 and F-4 stand
unaddressed against the tool as it stands**. The L1's docstring edit also does not close
F-4: it adds the clause "o3-o5 patch the url/admit call site only; the rev-branch
CHALLENGE call stays unconditional in all three", which makes the oracles *weaker* on the
rev branch, not stronger — i.e. the line-only mutant of F-4 is still accepted.

---

## Receipts written (all under `.ufo/waves/round-99/w1/`)

| file | content |
|---|---|
| `R99SentinelC1-c1-battery-at-F.txt` | battery at F: all 21 CASE lines + tally + PASS, exit 0 |
| `R99SentinelC1-c1-before-control.txt` | base tool under the battery, `--no-oracles`: FAIL, exit 1 |
| `R99SentinelC1-bypass-matrix.txt` | full rev-form path-spelling matrix at F with verdicts |
| `R99SentinelC1-round98-repro.txt` | the round-98 defect re-opened at F via `./` spelling; blob-identity proof |
| `R99SentinelC1-probe-marker-mutations.txt` | 8 marker-mutation cases (ZWSP / fullwidth / entity / soft hyphen / word joiner / NBSP / control) |
| `R99SentinelC1-probe-admit-variants.txt` | admit-form variants: whitespace padding, punctuation padding, control |
| `R99SentinelC1-probe-link-captures.txt` | symlink / hardlink / regular capture handling |
| `R99SentinelC1-probe-rev-paths.txt` | first rev-path enumeration pass |
| `R99SentinelC1-audit-hook.txt` | python audit hook: 0 writes outside `--work`, exec list |
| `R99SentinelC1-strace-battery.txt` | `strace -f -e trace=file,network,process` over the battery (108,830 lines) |
| `R99SentinelC1-strace-gate-verify.txt` | `strace` over `gate-records.py verify` |
| `R99SentinelC1-evidence-index.txt` | F / BASE / scratch paths used by every command above |
| `R99SentinelC1-remediation-variants.txt` | F-shipped vs FIXED-A vs FIXED-B across all path spellings, plus both variants through the frozen battery |
| `R99SentinelC1-fixed-tool-A.py` | the normpath+`CAP_RE.fullmatch` variant (NOT applied to production) |
| `R99SentinelC1-fixed-tool-B.py` | the normpath+`startswith("corpus/captures/")` variant (NOT applied to production) |
| `R99SentinelC1-battery-discrimination.txt` | F-4: line-only mutant PASSES the frozen battery; the same mutant admits S234 quoted on a non-marker line |

Probe fixture files (`rec-*.md`, `p0*.md`, `z*.md`, `m*.md`, `link-*.md`, `fix*.md`,
`final-*.md`, `base-rev-*.md`, `enum-*.md`) remain in the scratch tree
`$S/w1/probes/`, which is deleted before yield; the commands that produce each
observation are quoted inline above and are re-runnable from the quoted paths.

---

VERDICT: R99SentinelC1 C1 fired — the rev-leg CHALLENGE check is gated on a path *string* while git resolves the path *semantically*, so `./corpus/captures/<24hex>.txt` admits S230's reCAPTCHA blob with OK/exit 0 at F, and no named limit covers it.
VERDICT: R99SentinelC1 C2 held — all four counting commands reproduce the frozen tallies at F and the 23 quotes, 8-row table, K2 number placement, S236 identity and BASE_TOPIC_HITS=0 all re-derive independently.
