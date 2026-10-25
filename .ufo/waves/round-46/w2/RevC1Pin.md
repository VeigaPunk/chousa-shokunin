# RevC1Pin — fixture pinning (round 46, wave 2)

seat `L1Chousa46.RevC1Pin` · judged bytes `d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a` · claims frozen at `c2f0e9d1`.
Every mutation ran on a `git archive` copy under `/tmp` (deleted); lane bytes untouched.
Tree note: HEAD moved `d09fc8e` → `3807537` mid-run; `git diff --stat d09fc8e 3807537 -- corpus/fixtures/inference-ground-r46/ corpus/evidence/round46/c1-count.py` is empty, so all numbers hold at both. The worktree counter has changed again since (`M c1-count.py`, a name-keying canary, §P3) — uncommitted, not what is judged.

## Commands (verbatim decisive output)

| # | mutation on the copy | output | exit |
|---|---|---|---|
| A0 | none | `TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS` | 0 |
| B | 1 byte `#`→`X` in `positive-a.md` (sha256→`6e16710f…`) | `FIXTURES_CHANGED=positive-a.md` / `C1=FAIL` | 1 |
| C | delete `junk-uncited.md` | `FIXTURES_CHANGED=junk-uncited.md` / `C1=FAIL` | 1 |
| D | restore C | `POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS` | 0 |
| L | 1 byte in pinned `spans.tsv` | `FIXTURES_CHANGED=spans.tsv` / `C1=FAIL` | 1 |
| M | 1 byte in pinned `counts.json` | `FIXTURES_CHANGED=counts.json` / `C1=FAIL` | 1 |
| N | restore L,M | `3/3 3/3 C1=PASS` | 0 |
| G | `--root` at a copy with `positive-b.md` mutated | `FIXTURES_CHANGED=positive-b.md` / `C1=FAIL` | 1 |
| G2 | `--root` at a byte-faithful copy | `3/3 3/3 C1=PASS` | 0 |

Restores used `git show d09fc8e:<path>`; N/G2 confirm the copy was faithful again.

### Unpinned cover — the two files the tool actually reads
`corpus/fixtures/inference-ground-r46/spans/` holds `S901-1.txt` (sha256 `7c2aa3214d9409886ca91fefa1ed69599c29ec521cd745affae86f93b762b1ef`) and `S902-1.txt` (`c2184ca73ce45977…`). Both exist at the freeze commit, both are absent from `PINNED` (`c1-count.py:42-51`), both are read by `tools/inference-ground.py:137-162` under `spans.parent`.

- E1 1 byte `t`→`Z` in `spans/S901-1.txt` (sha256→`98331790…`) → `TOOL=present POSITIVE_PASS=2/3 JUNK_KILLED=3/3 C1=FAIL` **exit 1, no `FIXTURES_CHANGED` line.**
- I rename `S902-1.txt`→`S902-9.txt`, no byte change → `POSITIVE_PASS=2/3 JUNK_KILLED=3/3 C1=FAIL` exit 1, no attribution.
- J delete `S902-1.txt` → same `2/3 3/3 C1=FAIL` exit 1, no attribution.
- F add `positive-d.md` (4th fixture) → `3/3 3/3 C1=PASS` exit 0; tool accepts it (`GROUND: PASS`), counter never opens it (`POSITIVES`/`JUNKS` fixed tuples, `c1-count.py:37-38`).

### The artifact under test is unconstrained
- H `tools/inference-ground.py` ← 3 lines `sys.exit(0 if "positive" in basename else 1)` (sha256 `d0ed87bd750ee4…`) → `TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS` **exit 0** at `d09fc8e` and `3807537`; `FIXTURES_CHANGED` silent.
- H2 declared control reproduced: always-exit-0 → `JUNK_KILLED=0/3 C1=FAIL` exit 1.
- H3 real tool restored → `3/3 3/3 C1=PASS` exit 0.

### Pin is a pre-flight read, not an invariant of the measured bytes
`c1-count.py:84-90` digests, `:105-106` re-reads the same paths in six subprocesses. In a /tmp copy with a 2 s gap inserted only to make the window deterministic:
- R0 citation-id-only forge, no swap → `POSITIVE_PASS=3/3 JUNK_KILLED=0/3 C1=FAIL` exit 1.
- R1 same forge + the three junk bodies rewritten inside the window (`28dbe59108daf9…`, a body citing nothing) → `POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS` **exit 0**: a tool the claim says must score 1/3 reaches full marks, pin already satisfied.
- Natural window, timers only (no sleep): `PIN_TO_LAST_RUN_SEC=0.170`.

### Residual cheapest gate against the in-flight canary
A 9-line stub reading **no** span file — inference bullet carries an `S` id, two sentences hardcoded as fingerprints (`reverse index of every citation`, `independently re-verified against a live source`; sha256 `9d4995847bb9…`) → `TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass C1=PASS` **exit 0** on the canary-bearing worktree counter. Exact name keying is caught (`CANARY=fail`, exit 1, for both H and a `junk`-substring stub); content fingerprinting is not — the canary copies carry the same sentences.

### Pin truth
All eight `PINNED` values equal the `c2f0e9d1` blobs (`13782968… 1d09c94b… 4e61f56c… 7b3e6b6e… ab32577d… cba03251… 38a536bd… fd414d0a…`), and freeze→landing on the whole fixture tree is empty. The pin does not lie about what it covers.

## Findings

**P1 — high, operability. The kill-rule clause covers 8 of the 10 files the freeze shipped, and the two it skips supply the grounding text.** `claims.md` R46-C1: "a fixture set changed after this freeze, fails the claim as declared." One byte, a rename, or a delete under `spans/` changes the verdict (E1/I/J) yet prints the ordinary `C1=FAIL`, byte-identical to a tool defect — the counter cannot distinguish a post-freeze fixture edit from a regression. `corpus/lessons/round-46.md` mistake 1 states the fix as "a `PINNED` dict of sha256 per fixture", which reads as full coverage; it is per *top-level* file. Close: two entries — `spans/S901-1.txt: 7c2aa321…`, `spans/S902-1.txt: c2184ca7…` — or walk the directory. Additions stay unenforced (F; wave-1 `MutC1Junk` row D — reported here only as its closing status, not as new).

**P2 — high, operability. The pin and the measurement are two independent reads.** A concurrent writer between `:84-90` and `:105-106` turns the declared 1/3 control into `C1=PASS` (R1) with no `FIXTURES_CHANGED`; natural window ≈0.17 s, with 32+ seats in this lane. Content-addressing is therefore not an invariant of the scored bytes. Close: re-digest after the legs and require equality, or pin once and score a private copy.

**P3 — high, calibration. `PINNED` protects the fixtures; nothing protects the tool.** The 3-line name-keyed stub (H) scores full marks at the judged commit, falsifying `c1-count.py:19` ("Cheapest gates that would score full marks without the work") as written, and it outlives the `!= 0`→`== 1` hardening (`MutC1Junk` row F's exit-2 stub is refused now; exit-1 name keying was not). The worktree canary closes name keying only (fingerprint stub, above). No tool sha256 is in the counter, and `SKILL.md:117` records none; `measure-after.txt` names `tool 3018b1d25d762054` (= `3807537`'s revision, not `d09fc8e`'s `819f83ebdc6c…`). Both revisions score PASS, so the number is revision-robust while the attestation is not. Close: pin the tool's sha256, or name the limit.

**P4 — medium, calibration. The registered contract omits the pin.** `SKILL.md:117` gives C1 exit 1 as "any leg short (tool absent, a positive failing, or a junk fixture not refused with exit 1)" — never `FIXTURES_CHANGED=`, so a Gates reader cannot interpret the counter's own refusal line. Add `· exit 1 on FIXTURES_CHANGED=<names> (post-freeze fixture drift)`.

## Was `--root` bypassable by hash collision? No.
`--root` only relocates the tree; `PINNED` is a module constant checked at `:84` before any leg, and no flag skips it (`--tool` picks the artifact, not the pin). Empirically root-independent: G refuses a mutated tree at another root, G2 passes a faithful one. A colliding tree needs eight simultaneous **second preimages** on SHA-256 against messages the attacker cannot choose (not birthday/chosen-prefix), ≈2²⁵⁶ per name; no such attack exists, so — as suspected — it is impossible in practice. The bypass that does work needs no cryptography: P1 (2/10 files uncovered), P2 (check-then-use), P3 (tool unconstrained).

## Verified sound
B/C/L/M/G/G2 and pin truth. `FIXTURES_CHANGED=` names exactly the drifted file(s), stops before any leg, exit 1; restores return `3/3 3/3 C1=PASS` exit 0. Declared controls score as frozen (H2; citation-presence-only 1/3 per `controls/c1-controls.txt`).

## Not in this seat
C2/C3 legs, inference-follows (`CritC1Attack`), mention-based C2 (`CritC2Framing`), `junk-borrowed`'s token-level death — wave 1, not re-argued; I did not re-run `c2-count.py`/`c3-count.py`.

## Pointers
`corpus/evidence/round46/c1-count.py:37-38,42-51,84-90,105-106` · `tools/inference-ground.py:137-162` · `SKILL.md:117` · `corpus/lessons/round-46.md` mistake 1 · `corpus/evidence/round46/claims.md` R46-C1 kill rule · `git ls-tree -r c2f0e9d1 -- corpus/fixtures/inference-ground-r46/` (10 files) · HEAD `3807537`.
