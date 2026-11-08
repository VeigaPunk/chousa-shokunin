# R90SentinelScope — adversarial scope, control-discipline and safety review

Lane `chousa` (`/home/vgpnk/Projects/shokunin/chousa-shokunin`), round 90, wave 1.
Seat `R90SentinelScope`. Read-only outside my own output folder; leaf member (no dispatch, no
subagents, no production edits, no lane/fleet git or jj mutation, no commits or pushes).

Revisions under review:

| role | revision |
|---|---|
| base | `f54a45ed197dd475af50d82e43a22df3d2e99782` (round-89 landing + non-author spot-check) |
| claim freeze | `8d9893b42eb22690ea5f920ab87fd7e1810b847a` |
| tree attacked | `9bad12011187d114ba2c4588c5df08a21ab28145` (freeze + committed control receipts) |

Scratch: `/fast/scratch/hyaku/chousa-r90/R90SentinelScope/` (created with `mkdir -p`, every fixture
under it, removed before this report was yielded). No network was used by this seat; no `sudo`,
no sysctl, no host service touched, no `pacman` transaction.

Every finding below names the exact command, the receipt path I wrote, and the observed line plus
exit code. Receipts are copied into `.ufo/waves/round-90/w1/R90SentinelScope/receipts/`.

---

## F1 — The six committed receipts carry a pin that no instrument could satisfy at the freeze they were committed in (severity: high, control discipline)

**Command.**
```
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 8d9893b42eb22690ea5f920ab87fd7e1810b847a:corpus/evidence/round90/controls/receipts/c1-gate-r89.txt | grep '^# computed_against='
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin ls-tree -r --name-only f8fa55ec94cb34e7b572a9d87d7f62d88bc80bf8 corpus/evidence/round89/ | wc -l
```

**Observed.** At the freeze commit `8d9893b4` all six committed receipts carry
`# computed_against=f8fa55ec94cb34e7b572a9d87d7f62d88bc80bf8` — the round-88 verifier spot-check,
not the freeze. `corpus/evidence/round89/` contains **0** files at `f8fa55ec`: the instruments the
receipts measure (`gate-records-r89.py`, `mutate-r89.py`, `curation-r89.py`) did not exist at the
revision the receipts name, so the receipt bodies could not have been produced there. The carrier
commit `9bad1201` then **rewrote** all six `# computed_against=` headers (plus the `c1-harm-setup`
body path `…/emit/absent-tool.py` → `…/emit2/absent-tool.py`) — `git diff 8d9893b4 9bad1201 --
corpus/evidence/round90/controls/receipts/` = 6 files, 7 insertions, 7 deletions, every hunk a
one-line header/path edit.

**Receipt.** `receipts/scope-evidence.txt` §(a).

**Impact.** The frozen claim C1 clause (f) requires `# computed_against=` to equal `--rev`. At the
freeze revision the receipts violate their own clause: running the driver at the freeze tree with
`--rev 8d9893b4 --receipts-rev 8d9893b4` prints
`RECEIPT c1-gate-r89 FINDING PIN_MISMATCH:f8fa55ec…` for all six rows and
`COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=0/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=FAIL` (exit 1). The pin
was **re-stamped by hand after the freeze commit**, not minted by the emitter, so the receipts'
claimed measurement provenance is not evidenced by the bytes at the revision the freeze names. The
carrier's rewrite is what makes the predicate pass. This is the same shape as the round's own
named-limit 1 ("a coherent joint edit of the instrument, its receipt and its expectation row
survives") applied to the *pin* rather than the expectation row: the receipt body was left
byte-identical while the header that attests *where* it was computed was changed.

**Smallest remediation.** Do not hand-edit a committed receipt's provenance header. Re-emit the
six receipts with the driver at `--rev 8d9893b4` (`control-driver-r90.py emit --rev <freeze>`),
commit the emitted bytes as the carrier, and record the re-pin in `plans/round-90.md` as an
amendment naming the freeze-commit mis-pin. Round 91 owns it.

---

## F2 — The driver accepts a receipt whose *unbound* fields are falsified, so a joint edit of receipt + carrier commit passes with a PASS (severity: high, control discipline)

**Command.**
```
# fixture: clone the lane, checkout 9bad1201, rewrite c1-harm.txt's unbound fields, commit, then verify
python3 -B corpus/evidence/round90/control-driver-r90.py verify --root <clone> --repo <clone> \
  --rev 8d9893b42eb22690ea5f920ab87fd7e1810b847a --receipts-rev <the falsifying commit> --work <scratch>
```

**Observed.** `HARM_RECHECK files=15 records=31 moved=0 base_rc=0 head_rc=0` was rewritten to
`HARM_RECHECK files=999 records=31 moved=0 base_rc=7 head_rc=0` and committed; the driver printed
`RECEIPT c1-harm OK committed+exact+pin+fresh` and
`COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS` (exit 0). The
committed receipt now asserts `files=999` and `base_rc=7` — neither number is the one the
instrument prints (`files=15 base_rc=0`) — and the PASS line still stands. `records=31` (the harm
row's `records>=1` predicate key) and `moved=0` (its required token) were left intact, which is
exactly the leg set the row binds.

**Receipt.** `receipts/scope-evidence.txt` §(a) and the reproduction is reproduced verbatim in the
report body above; the committed-fixture reproduction is reproducible from the four commands in
"Reproduction" below.

**Impact.** `EXACT_OK` is a **second, independent pass** over the same `check_body` result
(`control-driver-r90.py:293-296`) and is not a term of `passed`; the fresh leg compares the fresh
run against the *expectation row*, never against the committed receipt's body. So the only thing
that binds a committed receipt to reality is the row's required tokens and predicates. A receipt
can carry any other number and still be certified `OK` by the driver, as long as the changed bytes
are committed at the `--receipts-rev` the caller names. Combined with F1, the "receipts pin the
freeze revision" property rests on the caller choosing `--receipts-rev`, not on the driver.

**Smallest remediation.** Add a leg that compares the fresh re-run's *body tokens* to the committed
receipt's body tokens for the same case (not merely to the expectation row), and make
`exact_only`/`EXACT_OK` a term of `passed`. Round 91 owns it.

---

## F3 — The command form this round's own dispatch names (`--root <lane> --repo <clone>`) prints `CONTROL_DRIVER_R90=FAIL` (severity: high, operability / dispatch correctness)

**Command.**
```
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round90/control-driver-r90.py verify \
  --root /home/vgpnk/Projects/shokunin/chousa-shokunin --repo /fast/scratch/hyaku/chousa-r90/R90SentinelScope/repo \
  --rev 8d9893b42eb22690ea5f920ab87fd7e1810b847a --receipts-rev 9bad12011187d114ba2c4588c5df08a21ab28145 --work <scratch>
```

**Observed (exit 1).**
```
RECEIPT SELF_PIN FINDING SELF_DRIFT ../../../../../../home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round90/control-driver-r90.py, …expected.tsv, …/receipts/c1-gate-r89.txt, …
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=FAIL
```

**Receipt.** `receipts/c1-formA-root-lane-repo-clone.txt`, `receipts/c1-invocation-matrix.txt`.

**Invariance matrix** (all five runs, same freeze/carrier revs, only the script/root/repo triple varied):

| script | `--root` | `--repo` | exit | verdict |
|---|---|---|---|---|
| lane | lane | clone | 1 | **FAIL** (SELF_DRIFT) |
| lane | lane | lane | 0 | PASS |
| clone | clone | clone | 0 | PASS |
| clone | lane | clone | 0 | PASS |
| clone | clone | lane | 1 | **FAIL** (SELF_DRIFT) |

**Impact.** `self_pin()` (`control-driver-r90.py:161-181`) computes each scoring file's path
relative to `os.path.abspath(repo)`. When the driver's own file, the expectations file and the
receipts live in a tree other than `--repo`, the relative path escapes the repository and
`git show <rev>:<escaping path>` fails, so every scoring byte is reported as drifted and the run
fails on a path artefact. This is the command form the round-90 dispatch text states for C1
("`--root <lane> --repo <clone at 9bad1201…>`"), and it is the form in
`.ufo/waves/round-90/build_spec.py:60-62` — a committed file. A seat following the dispatch
verbatim gets `CONTROL_DRIVER_R90=FAIL` at exit 1 on correct bytes.

**Smallest remediation.** Resolve the scoring files' paths relative to `--root` (the tree the
receipts were read from) rather than relative to `--repo`, or read them from `--root` and compare
to `--repo`'s blobs only when `--root` is inside `--repo`. Round 91 owns it; the frozen claim's own
counting command (`--root . --repo .`) is unaffected.

---

## F4 — The S220 registry row cites a capture that is not in the tree it lands in (severity: high, provenance / scope)

**Command.**
```
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin ls-tree -r --name-only 9bad12011187d114ba2c4588c5df08a21ab28145 corpus/captures/ | grep -c e6ec761
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain corpus/captures/
```

**Observed.** `0` — `corpus/captures/e6ec761219e8044b0e9e067a.{txt,raw}` are **not tracked** at the
carrier; they are untracked working-tree files (`?? corpus/captures/e6ec761219e8044b0e9e067a.raw`,
`?? corpus/captures/e6ec761219e8044b0e9e067a.txt`), and the index is empty. A clean clone of the
carrier has 181 capture files and **not** S220's. Meanwhile `corpus/SOURCES.md` at the carrier
carries the S220 row whose location cell names "capture key e6ec761219e8044b0e9e067a", and the
registry row is `mined`.

**Receipt.** `receipts/scope-evidence.txt` §(b)/(c).

**Impact.** The registry's own contract (`tools/gate-records.py:32-34`, `CAPTURE_PATH` /
`CAPTURE_KEY` / `CAPTURE_SHA`) requires the capture to be a regular file inside `LANE` with
`capture_sha256` a prefix of its bytes. Verified by running the lane's own gate tool against a
`GATE-RECORD S220` line citing that capture:

* against a clean clone of the carrier → `GATE_RECORD … S220 FAIL CAPTURE_PATH,CAPTURE_SHA,QUOTE_ABSENT,REFETCH,WORDS` (exit 1);
* against the lane working tree (capture present but untracked) → only `WORDS` fails, i.e. my
  hand-written `words=18` was wrong; the capture bytes themselves verify (`CAPTURE_PATH`,
  `CAPTURE_SHA`, `QUOTE_ABSENT`, `REFETCH` all clear) — the quote
  `Select only those matches that exactly match the whole line` is present exactly once in the
  `.txt` form.

So the ground source's *bytes* are good and the *quote* is real, but the S220 row lands in the
registry with its cited capture outside the commit that carries it. The S220 row is the sole
registry row added this round (218 → 219 rows confirmed) and it is the cited ground source for
C1's whole-token rule.

**Smallest remediation.** Commit `corpus/captures/e6ec761219e8044b0e9e067a.txt` and `.raw` in the
same commit that lands the S220 registry row (or land them before it), so the cited capture key
resolves inside the tree. Round 91 owns it.

---

## F5 — Egress: the successful S219 fetch is absent from the egress table and the S220 fetch is a second GET of the same URL under a different id (severity: medium, egress discipline)

**Command.**
```
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff f54a45ed197dd475af50d82e43a22df3d2e99782 9bad12011187d114ba2c4588c5df08a21ab28145 -- corpus/evidence/round57/refetch.tsv
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 9bad12011187d114ba2c4588c5df08a21ab28145:.ufo/waves/round-90/egress.tsv
```

**Observed.** Three rows were added to `corpus/evidence/round57/refetch.tsv`:

| id | url | attempt | fetched_utc | curl_rc | http | raw_sha256 / txt_sha256 |
|---|---|---|---|---|---|---|
| S219 | `https://www.gnu.org/software/grep/manual/html_node/Matching-Control.html` | 1 | 2026-11-08T09:44:25Z | 28 | 000 | `-` / `-` |
| S219 | `https://man7.org/linux/man-pages/man1/grep.1.html` | 1 | 2026-11-08T09:44:57Z | 0 | 200 | `d6f07a7f…` / `5a5e69c5…` |
| S220 | `https://man7.org/linux/man-pages/man1/grep.1.html` | 1 | 2026-11-08T09:52:31Z | 0 | 200 | `d6f07a7f…` / `5a5e69c5…` |

**Naming as required.**
* The **S219 failed attempt** is row 1: `curl_rc=28` (timeout), `http=000`, no bytes. It landed
  under id **S219**, and **no registry row exists for S219** (registry count of `| S219 ` rows at
  the carrier = 0; `S220` = 1). The plan's stated intent — S219 stays reserved to the round-89
  control fixture's mirror row and is not a registry row — holds.
* The **S220 success** is row 3: `curl_rc=0`, `http=200`, `raw_sha256=d6f07a7f…`,
  `txt_sha256=5a5e69c5…`, capture key `e6ec761219e8044b0e9e067a` (= `sha256(url)[:24]`, verified
  by recomputation). The **S220 registry row exists** in `corpus/SOURCES.md` at the carrier, status
  `mined`, tier A, capture key `e6ec761219e8044b0e9e067a`, used-by `corpus/evidence/round90/claims.md`.
* **Row 2 is a third fetch that the brief's framing does not name**: a *successful* GET
  (`rc=0`, `http=200`) of the same man7.org URL under id **S219** at 09:44:57Z, with byte-identical
  digests to the S220 row. The committed egress table at the carrier has **two** rows and does not
  mention it: it lists S219 only for the *failed* gnu.org attempt and S220 for the man7.org page.
  The intermediate commit `6ccf22b9` did carry an S219→man7.org row ("same `-x` wording, reachable
  from this host; the row is written only if the located quote is present", access `2026-11-08`),
  which the carrier's rewrite replaced by the S220-labelled row.

**Receipt.** `receipts/scope-evidence.txt` §(b).

**Impact.** The round's egress table is the artefact that records "what was fetched and under
which id"; it now under-reports by one successful GET, and the refetch ledger shows the same
content fetched twice under two different ids eight minutes apart (`attempt=1` for each, because
`tools/capture-fetch.py` counts attempts per `(id,url)` pair, not per URL). No registry row was
written for the S219-labelled success, so the "no row under S219" rule still holds; the
discrepancy is in the ledger's own accounting, and the plan's item 6 ("the failed gnu.org attempt
is logged under `S219` in `refetch.tsv`") describes only one of the two S219 rows.

**Smallest remediation.** Record the 09:44:57Z successful man7.org GET in
`.ufo/waves/round-90/egress.tsv` as a third row under S219 (or amend `plans/round-90.md` item 6 to
name it), so the egress table and `refetch.tsv` agree. Round 91 owns it.

---

## F6 — Scope: the round's diff is inside the lane and inside the declared surface; `SKILL.md` is unchanged at the carrier (severity: none — clean finding)

**Command.**
```
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff f54a45ed197dd475af50d82e43a22df3d2e99782 9bad12011187d114ba2c4588c5df08a21ab28145 --stat
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff --name-only f54a45ed197dd475af50d82e43a22df3d2e99782 9bad12011187d114ba2c4588c5df08a21ab28145
```

**Observed.** 26 files, all inside `/home/vgpnk/Projects/shokunin/chousa-shokunin`, all inside
this round's declared surface: `.ufo/waves/round-90/{build_spec.py,claims.json,egress.tsv}`,
`corpus/SOURCES.md` (one row), `corpus/evidence/round57/refetch.tsv` (three rows),
`corpus/evidence/round90/**` (the seven instruments, `claims.md`, `controls/expected.tsv`,
`controls/receipts/*`, `instrument-pins.txt`, `census-start.txt`), `plans/round-90.md`.
**No path outside the lane.** No sibling repo, no `/home/vgpnk/Projects/shokunin/scripts`, no
`.ufo/state`, no `MANIFEST.json`, no `considerthese/`, no `tools/` change (`git diff base..carrier
-- tools/` is empty — `tools/research-gate.sh` and `tools/gate-records.py` are unchanged, as the
round states). The lane is a separate git repository nested beside the fleet repo (the fleet repo
does not track `chousa-shokunin`), so the lane's commits cannot have touched the fleet's tracked
files.

**`SKILL.md` at the carrier:** unchanged — `git diff base..carrier --name-only` does not list it,
and `git diff base..carrier -- SKILL.md` is empty. The C3 repair is a *working-tree* change only
(`M SKILL.md` in `git status`), consistent with "the repair lands after the wave". Its shape is
exactly the declared one: 9 tally cells in the Gates table (lines 86–93, **cell 5 only** — the
`self-test` column) plus the one host-note statement at line 781, and nothing else. The
case-range note added inside cell 5 of line 86 ("r82 bash-pin-override cases 276–283") is inside
the same cell as its tally, so `SKILL.md` moved only within the tally cells and the one
case-range note. I verified this cell-by-cell rather than by line count.

**Working-tree drift I did not touch** (recorded for the L1, not a finding against the round):
`SKILL.md` (M), `plans/round-90.md` (M, ten amendments appended by the L1 after the freeze),
plus untracked `.ufo/waves/round-90/w1*`, `corpus/evidence/round90/after/`,
`corpus/evidence/round90/controls/selftest-r90.txt` and the two untracked S220 capture files
(F4). None is mine.

**Receipt.** `receipts/scope-evidence.txt` §(c).

---

## F7 — Attribution: every round-90 commit is `chousa-shokunin <chousa@shokunin.local>` (severity: none — clean finding)

**Command.**
```
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin log --format='%h A=%an <%ae> C=%cn <%ce> %s' f54a45ed197dd475af50d82e43a22df3d2e99782..9bad12011187d114ba2c4588c5df08a21ab28145
```

**Observed.** All four commits in the range — `af71d0a1`, `6ccf22b9`, `8d9893b4`, `9bad1201` —
carry author **and** committer `chousa-shokunin <chousa@shokunin.local>`. The base commit
`f54a45ed` is `protocol-shokunin <protocol@shokunin.local>` (the round-89 integrator's
non-author spot-check) — outside this round's authorship.

**Receipt.** `receipts/scope-evidence.txt` §(d).

---

## F8 — Credential shape: no secret value in any file this round added (severity: none — clean finding)

**Command.** A tightened scan over **every** file changed base→carrier:
`op://[A-Za-z0-9_/.-]{3,}|ghp_[A-Za-z0-9]{10,}|\bsk-[A-Za-z0-9]{10,}|Bearer [A-Za-z0-9._~+/=-]{10,}`
applied to each file's blob at the carrier.

**Observed.** Zero hits in all 26 changed files. The only earlier hits on the loose pattern
`sk-` were the substring inside `assessing-risk-bias` / `risk-of-bias` in two Cochrane URLs
(S009, S212) — false positives, no values. The round's own `build_spec.py` and the wave dispatch
files contain the *pattern strings* `op://`, `ghp_`, `sk-`, `Bearer ` only because they quote this
seat's brief; that is the search vocabulary, not a credential. The S220 registry row carries a
public URL and a capture key, no token.

**Receipt.** `receipts/scope-evidence.txt` §(e).

---

## F9 — Safety: no round-90 instrument touches the network, sudo, sysctl or the host (severity: none — clean finding)

**Command.**
```
grep -rnE 'curl |wget |urllib|requests\.|socket\.|sudo |sysctl|systemctl|chown|chmod |iptables' corpus/evidence/round90/*.py
```

**Observed.** No hits in any of the seven round-90 instruments. The driver, the forgery battery,
the harm recheck, the three curation instruments and the tally check are pure
`subprocess`/`open()` over local bytes; `control-driver-r90.py` states "no network" in its
docstring and honours it. No host sysctl was mutated, no service restarted, no `sudo` invoked by
this seat.

One **low-severity** robustness note (not a claim defect): the driver builds its instrument
command line by string substitution into a `bash -lc` invocation
(`control-driver-r90.py:96-99`, `run_instrument`), so a `--root`/`--work` path containing shell
metacharacters is interpreted by the shell. I confirmed the mechanism benignly inside my scratch
(`--work "$S/w$(touch $S/INJECTED)"` created the file — i.e. command substitution in `--work` is
executed). It is not exploitable by an untrusted party here (the operator chooses the paths and
the lane is single-author), and it is the same pattern the round-89 instruments already use, so I
record it as a hardening note rather than a defect: quote the substituted paths, or drop the
shell and exec an argv list.

---

## Reproduction (exact commands; all under `/fast/scratch/hyaku/chousa-r90/R90SentinelScope/`)

```sh
S=/fast/scratch/hyaku/chousa-r90/R90SentinelScope
L=/home/vgpnk/Projects/shokunin/chousa-shokunin
F=8d9893b42eb22690ea5f920ab87fd7e1810b847a
C=9bad12011187d114ba2c4588c5df08a21ab28145
mkdir -p "$S"
git clone --shared "$L" "$S/repo"; git -C "$S/repo" checkout "$C"
test "$(git -C "$S/repo" rev-parse --show-toplevel)" = "$S/repo"   # asserted before any git mutation

# F1: the freeze's own pins
git -C "$L" show "$F:corpus/evidence/round90/controls/receipts/c1-gate-r89.txt" | grep '^# computed_against='
git -C "$L" ls-tree -r --name-only f8fa55ec94cb34e7b572a9d87d7f62d88bc80bf8 corpus/evidence/round89/ | wc -l   # 0
git -C "$L" diff --stat "$F" "$C" -- corpus/evidence/round90/controls/receipts/

# F3: the dispatch's own command form
python3 -B "$L/corpus/evidence/round90/control-driver-r90.py" verify --root "$L" --repo "$S/repo" \
  --rev "$F" --receipts-rev "$C" --work "$S/workA"     # exit 1, CONTROL_DRIVER_R90=FAIL, SELF_DRIFT
bash "$S/matrix.sh"                                      # the five-row invariance matrix

# F4: the S220 capture is not in the tree
git -C "$L" ls-tree -r --name-only "$C" corpus/captures/ | grep -c e6ec761   # 0
git -C "$L" status --porcelain corpus/captures/                            # ?? …e6ec761….raw / .txt

# F2: a committed falsification of a receipt's unbound fields still prints PASS
git clone --shared "$L" "$S/repo-forg"; git -C "$S/repo-forg" checkout "$C"
#   rewrite c1-harm.txt files=15->files=999, base_rc=0->base_rc=7; commit
python3 -B "$S/repo-forg/corpus/evidence/round90/control-driver-r90.py" verify --root "$S/repo-forg" \
  --repo "$S/repo-forg" --rev "$F" --receipts-rev "$(git -C "$S/repo-forg" rev-parse HEAD)" \
  --work "$S/work-forg"                                   # exit 0, CONTROL_DRIVER_R90=PASS
```

## What I ran and what it printed (all at the carrier, all from a clean clone)

| check | command | observed | exit |
|---|---|---|---|
| C1 driver, clone/clone | `control-driver-r90.py verify --root $S/repo --repo $S/repo --rev $F --receipts-rev $C --work $S/work` | `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS` | 0 |
| C1 driver, lane/clone (dispatch form) | same with `--root $L --repo $S/repo` | `… CONTROL_DRIVER_R90=FAIL` + `SELF_PIN FINDING SELF_DRIFT …` | 1 |
| C1 driver at the freeze | `… --rev $F --receipts-rev $F` on a clone at `$F` | `PIN_OK=0/6 CONTROL_DRIVER_R90=FAIL` (all six `PIN_MISMATCH:f8fa55ec…`) | 1 |
| C1 forgery battery | `control-forgeries-r90.py --root $S/repo --work $S/work-forg --rev $F` | `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass` | 0 |
| receipts-dir write discipline | sha256+mtime+size of all 9 receipt files before/after two `verify` runs | `RECEIPTS_DIR_UNCHANGED=YES`, `RECEIPTS_DIR_STAT_UNCHANGED=YES` | — |
| C2 counter | `curation-r90.py --root $S/repo` | `LEGS_MEASURED=10/10`, `VERDICT fields_hold=1 legs_ok=10/10 DETECTOR_WISTNESS=8/8`, `CURATION_R90=PASS` | 0 |
| C2 mutants | `curation-r90-mutants.py --root $S/repo --work $S/work-c2mut` | `MUTANTS_KILLED=10/10 COUNTER_DETECTED=9 BATTERY_DETECTED=1 PRIOR_R89_SURVIVORS=2/2` | 0 |
| C2 controls | `curation-r90-controls.py --root $S/repo --work $S/work-c2ctl` | `FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7 CONTROLS=PASS` | 0 |
| C3 at the carrier | `skill-tally-r90.py --root $S/repo` | `TALLY_ROWS=9 STALE_TALLIES=9/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=FAIL` | 1 |
| C3 discrimination (9 cells → 283) | `skill-tally-r90.py --root <scratch copy>` | `TALLY_ROWS=9 STALE_TALLIES=0/9 … SKILL_TALLY_R90=PASS` | 0 |
| instrument pins | sha256 of each pinned path at `$F` and at `$C` vs `instrument-pins.txt` | all 11 `OK` at both revisions | — |
| S220 gate check, clean clone | `tools/gate-records.py verify --root . --repo . <S220 GATE-RECORD>` | `S220 FAIL CAPTURE_PATH,CAPTURE_SHA,QUOTE_ABSENT,REFETCH,WORDS` | 1 |

Note on C3's `OTHER_OCCURRENCES=3`: I recounted the binding regex over `SKILL.md` at the carrier
independently and got exactly three unbound occurrences — line 186 (`256 cases`), line 188
(`161 cases`) and line 640 (`215 cases`) — and nine bound ones (table lines 86–93 plus line 781).
The claim's prose labels them "round-25/32/34/37 quotes"; the actual three are a round-34 quote
inside the round-25 historical paragraph (L186), the round-25 final quote (L188) and a round-27
quote (L640). The count `3` is right; the labels are not. The L1 has already recorded this as
Amendment 1 in the working-tree plan; I am not claiming it as new.

## Scope statement

Read-only outside `.ufo/waves/round-90/w1/R90SentinelScope/`. I wrote only that folder
(this file + `receipts/`) and my scratch under
`/fast/scratch/hyaku/chousa-r90/R90SentinelScope/`, which I removed before yielding. I made no
lane or fleet git/jj mutation, no commit, no push; I did not touch `/home/vgpnk/Projects/shokunin/scripts`,
`/home/vgpnk/Projects/shokunin/.ufo/state`, `MANIFEST.json`, `considerthese/` or any sibling repo;
I used no network; I ran no `sudo`, mutated no host sysctl and restarted no service. No tool was
installed or upgraded this round (`/home/vgpnk/.omp/agent/RULES.md` read; the pacman guard was
respected — no pacman transaction of any kind).

---

VERDICT: R90SentinelScope C1 fired — the dispatch's own `--root <lane> --repo <clone>` form prints `CONTROL_DRIVER_R90=FAIL` at exit 1 on correct bytes (SELF_PIN resolves scoring paths relative to `--repo`), the six receipts were hand-re-pinned after the freeze commit to a revision whose instruments did not exist there, and a committed falsification of a receipt's unbound fields still prints PASS.
VERDICT: R90SentinelScope C2 held — the counter, mutants and controls all reproduce their frozen tokens at exit 0 from a clean clone of `9bad1201`, the registry diff is exactly the one S220 row (218 → 219) and no S219 row, and no C2 artefact reaches outside the lane.
VERDICT: R90SentinelScope C3 held — `SKILL.md` is byte-unchanged at the carrier, the tally check prints `STALE_TALLIES=9/9 … FAIL` there and `STALE_TALLIES=0/9 … PASS` on the nine-cell 283 copy, and the working-tree repair touches only the nine tally cells and the one case-range note.
