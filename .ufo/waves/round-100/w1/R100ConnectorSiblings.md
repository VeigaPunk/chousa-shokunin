# R100ConnectorSiblings — cross-lane pattern scan (chousa round 100, read-only)

Tree attacked: `git clone -q --shared <lane> $S/repo && git -C $S/repo checkout -q 6d4e8487ee6a16823c24a8e085c6559b92b9fec8`
(`rev-parse HEAD` = the freeze; `status --porcelain` empty). All batteries ran against that clone, never the live lane.
Scratch `S=/fast/scratch/hyaku/chousa-r100/R100ConnectorSiblings` (deleted before yield). Lane writes: this file and the
`R100ConnectorSiblings-*.txt` receipts in this directory only.

Axes under test: **operability** (C1 `C1-GATE-REVCAP-R100`) and **freshness** (C2 `C2-ENTRY-UPDATE-R100`).

## What the round's own instruments say (re-derived, not taken on trust)

| command | observed | exit |
|---|---|---|
| `python3 -B corpus/evidence/round100/challenge-controls-r100.py --root . --work <scratch>` | `NEG=7/7 MARK=11/11 BOUND=3/3 NORM=2/2 POS=4/4 REV=11/11 REVPOS=3/3 PROD=6/6 HARM_SAME=27/27 BASE_REV_ADMITTED=8/11 ORACLES_REJECTED=12/12` + `CHALLENGE_CONTROLS_R100=PASS` | 0 |
| same, `--tool <929c784c:tools/gate-records.py> --no-oracles` | `REV=3/11 … PROD=4/6 … BASE_REV_ADMITTED=8/11` + `CHALLENGE_CONTROLS_R100=FAIL` | 1 |
| `python3 -B corpus/evidence/round100/entry-controls-r100.py --root .` | `QUOTES=16/16 … FRESH=1/1 … FORGERY_REFUSED=13/13 ACCEPTED=2/2` + `ENTRY_CONTROLS_R100=PASS` | 0 |
| `python3 -B tools/gate-records.py verify --root . corpus/knowledge/quotation-error-update-r100.md` | `GATE_RECORDS files=1 records=17 ok=17 fail=0` | 0 |
| `bash tools/research-gate.sh verify-metadata …quotation-error-update-r100.md --root .` | `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN` | 0 |
| `python3 -B tools/search-rerun.py verify …quotation-error-update-r100.md --root .` | `rev_match=3/3`, `SEARCH_RERUN: CLEAN` | 0 |
| `python3 -B tools/gate-records.py verify --root . corpus/knowledge/quotation-error-rates-r99.md` | `records=25 ok=25 fail=0` (unchanged) | 0 |
| `python3 -B corpus/evidence/round99/entry-controls-r99.py --root .` | `ENTRY_CONTROLS_R99=PASS` | 0 |

Every number in the frozen claims reproduces exactly (`R100ConnectorSiblings-c1-battery.txt`, `-c1-base.txt`,
`-c2-counts.txt`). Both claims' *numbers* hold; the findings below are about what the wording asserts beyond the
instrument, and about two live shapes the frozen text does not separate.

## Cross-lane scan (a) — cited-file resolution by content identity, or path normalisation before a guard

| path | rev | one line | relation to chousa C1 |
|---|---|---|---|
| `kagi-shokunin/corpus/knowledge/claim-instrument-carrier-binding.md` §1–2 | `967afd4912aebfe2edce4414162bbd1f26b37c04` | "A registry row binds a carrier by **path equality plus digest equality**, never by filename"; "the filename is a handle, not an identity" | **C1 duplicates and supersedes the identity half.** Kagi's rule keeps *path* as an anchor; C1 drops the path and keys on the blob oid, which is the stronger form for the byte-copy attack (C1's r7/r8 admit no renamed copy). Kagi's digest half has no counterpart in C1's rev form (see route R3). |
| `kama-shokunin/tools/digest-ledger.py` | `9c5a864461fadcb2d720a872ce7f83aac6a2ef85` | "find every full SHA-256 the lane's documents cite and classify it… it hashes what a document points at"; every cited digest is classified against the blob set of REV | **C1 lacks this.** A rev GATE-RECORD carries no digest (`capture_sha256` is an `admit`-form key only; `REV_KEYS` has no digest), so the record asserts *nothing* about which bytes it means — the tool infers the capture set from the tree. Their synthesis closes C1's named limit (b). |
| `tameshi-shokunin/tools/quoted-line-exists.py` | `baa63c452713c21762c21f092eea0a2e40930468` | quotes must be byte-backed by cited receipt blobs at REV (`ls-tree` + `cat-file --batch`), with `ABSENT`/`ambiguous`/`skipped` counters and the round-69 **MISS-record exclusion** (a receipt's own record of a missing quote may not back that quote) | **Duplicates C1's technique on another object** (quote bytes vs challenge captures). The MISS-record exclusion has no chousa analogue in `gate-records.py`; `tools/quote-reopen.py` is the surface to check it against. |
| `tsukuroi-shokunin/tools/check-knowledge-refs-r68.py` | `a5fc44a7e3cea43a1fc8edbd8e50ab4f1a0c4f8f` | every entry's `source:` S-id is resolved against `corpus/SOURCES.md` **at a commit** (`read_blob` refuses a non-blob path), dangling ids named | **C2's registry binding is worktree-only.** `gate-records.py` loads `root/corpus/SOURCES.md`; the rev form resolves captures at `--repo` but the registry at `--root`. Mixed provenance, not asserted by either claim. |
| `mado-shokunin/tools/mado-receipt-citecheck.py` | `5f9ce459803dc17aceb16a6f8507006b85737c35` | path citations resolved at `--rev` against `ls-tree -r --name-only`; "MISSING paths are named, never silently skipped", files over the read cap counted | **Opposite resolution strategy** (path spelling), kept honest by counters. C1 needs no such counter because `rev-parse` failure is `REV`+`LINE` — but the tool has no counter for *how many* rev records it resolved vs skipped. |
| `souji-shokunin/tools/souji-citation-reconcile.py` | `bbd9b9746ba9e3c5d640bf095bbad18a00c80e83` | compares a register row's `receipt` to `file` after `os.path.normpath` | The "normalise then compare" pattern C1 deliberately abandons: normalisation cannot see a byte copy at another path, which is exactly r7/r8. |

## Cross-lane scan (b) — the 2025 quotation-inaccuracy update, and stale-knowledge flags

**Null for the update itself.** `git -C <lane> grep -l -F 40696441 HEAD` and `-F 'quotation inaccuracy'` return 0 for
every sibling lane (`R100ConnectorSiblings-sibling-evidence.txt`). The one content-adjacent hit outside chousa is
`tameshi-shokunin/corpus/SOURCES.md` S328 (rev `ae65bab9e1a7272374faf71248b216553cb79ae8`): the **2017** Mogull paper
that chousa holds as S233, rejected there with a scoped reason ("re-derives the same quotation-error ground S327 already
holds… the lane counts pointer mismatches, it reports no rate"). So: no lane needs C2's update; two lanes independently
hold the 2017 layer; neither holds the 2025 layer. **Route the entry, do not absorb it** — chousa is the only holder and
the update stays chousa-local knowledge.

Stale-knowledge mechanisms, ranked by how much they would have caught something here:

| path | rev | mechanism | relation to C2 |
|---|---|---|---|
| `kagi-shokunin/corpus/QUALITY.md` QM70/QM73 | `61792976d8ffa11f37894c01d2ba7ec6e6b2a1ab` | "a prose on-release with no clock reads as watched while nothing watches it"; "a row that declares `on-release` without a bound clock in the same commit is a defect"; when the clock fires, the line is re-run or scoped down | **Contradicts chousa's register.** 118 of 238 `corpus/SOURCES.md` rows carry `on-release` and none is clock-bound; `research-gate.sh` maps `on-release` to `due=on-release freshness=event`, i.e. never due, at any `--as-of`. |
| `tabi-shokunin/corpus/knowledge/chromium-156-release-pin-recheck.md` | `e8720bcfcdf97a4bd53fa91a0dab1e4616ae01d4` | `recheck: on-release — \`node scripts/check-release-pins.mjs --rev <REV> --stable <current Stable>\`; a population > 0 at a newer Stable means this note is due again` | **Should adopt the shape:** an on-release that names the watcher and the predicate. Both chousa entries write bare `recheck: on-release` (r99:5, r100:5). |
| `kama-shokunin/corpus/knowledge/engine-pin-watch.md` | `0718b6abbda6afa6b0ce586f46739fbb92c7cf9c` | `recheck: run \`python3 tools/pin-watch.py check --pins registry/engine-pins.tsv\`; 30d` | same: a recheck is a command with an observable. |
| `kagi-shokunin/corpus/knowledge/iso-11770-3-edition-status.md` | `70867f40dd6cc75cda57556d80601fda603f7290` | a status entry for a superseded edition: which edition is in force, what replaced the withdrawn one, and a recheck that is a re-runnable `curl … | grep -c` with an expected count | **The closest sibling to C2's job** (a stale reading flagged where it is held). Its recheck is a command; C2's is a link. |
| `kengaku-shokunin/corpus/knowledge/bench-arena-round7-noise-n25.md` `## Updates to prior corpus claims` | `7c2217ed8018d480d6e4b4cb948adcdb357944c1` | retro-correction list naming the prior entry and the changed verdict, appended never in place | Different `## Update` shape (errata list, not supersession pointer). chousa's two-way `updates:` + `## Update` has no duplicate; kengaku's "never an in-place edit" discipl<sup>1</sup> corroborates it. |

<sup>1</sup> kengaku's section heading at the sampled file is `## Updates to prior corpus claims` followed later by
`## Errata (appended round 9, never an in-place edit)`; the phrase quoted is the errata header, not a rule row.

## Findings

### F1 — C1: the quote is checked against one file, the CHALLENGE verdict against another (`<k>.raw` sibling)

The rev form line-checks the quote in `rev:path`'s bytes, then calls `rev_capture_text`, which for a `.raw` entry
**replaces the blob with the sibling `.txt`** (`tools/gate-records.py:261-275`). For the 92 of 101 `.txt`/`.raw` pairs in
the frozen tree whose bytes differ (`R100ConnectorSiblings-c1-pairs.txt`), the two checks read different files.

Proof (`R100ConnectorSiblings-c1-raw-shadow.txt`, fixture repo under `--work`, committed with the fixture identity):

```
CASE A  .raw = "Just a moment while we verify your browser." (challenge page), sibling .txt = benign page,
        record cites corpus/captures/<k>.raw line=1 quote="Just a moment"
  → GATE_RECORD …/gate-…_raw.md:1 S230 OK ; GATE_RECORDS files=1 records=1 ok=1 fail=0   exit 0
CASE B  .raw benign, .txt = the challenge page (record still cites the .raw)
  → GATE_RECORD …:1 S230 FAIL CHALLENGE ; ok=0 fail=1                                    exit 1
```

The C1 sentence's parenthetical licences case A ("for a `.raw` entry, its sibling `.txt` at that rev when one exists"),
so the *tool* does what the sentence says (C1 not fired). But the **Kill rule** says C1 fails when a wave artifact shows
"a rev record whose blob has a capture's object id at that rev, **whose capture text is a challenge page** by the
round-99 rule, and which this tool prints OK". In case A the cited blob's own text *is* a challenge page and the tool
prints OK. **The two frozen sentences disagree on this shape**; a later wave artifact cannot tell which governs it. State
it, do not smooth it. Severity is bounded (the lane stores the `.txt` as the authoritative text), but the divergence is
mechanical and the record's `quote=` can be taken verbatim from the challenge `.raw`.

### F2 — C2: "fired" is not instrument-enforced; an explicit denial is an *accepted* forgery

C2's sentence: "The round-99 entry's `recheck: on-release` fired and was answered." The freshness leg (`fresh()` in
`entry-controls-r100.py`) checks only that the old entry's `## Update` contains the new entry's path and the string
`S238`, and that the new entry's `updates:` points back.

Proof (`R100ConnectorSiblings-c2-fired-mutant.txt`): on a shared clone of F, change one sentence in
`corpus/knowledge/quotation-error-rates-r99.md:119` to

> `Round 100 (2026-11-09): this entry's \`recheck: on-release\` has NOT fired; no new release exists.`

and re-run the C2 counting command:

```
QUOTES=16/16 … FRESH=1/1 … FORGERY_REFUSED=13/13 ACCEPTED=2/2
ENTRY_CONTROLS_R100=PASS        exit 0
```

So the 13 forgery cases do not include the one that attacks the claim's load-bearing word; the freshness instrument
cannot distinguish "fired" from "explicitly did not fire". This is the same mechanism `R100CriticClaims-form-probes.txt`
already routed for the decision table ("mutations in narrative prose … are invisible to the controls") — the narrative
it does not cover is the firing claim itself. The lane-scale consequence is in `R100ConnectorSiblings-onrelease-model.txt`:
118/238 registry rows are `on-release`; `research-gate.sh:3819-3821` sets `due=on-release freshness=event`, and
`--as-of 2026-11-09` and `--as-of 2027-11-09` both print `freshness=event` — the gate has no state in which an
`on-release` is due, so a "fired" claim can only ever be prose. kagi QM70/QM73 (above) call exactly this a defect.

### F3 — C1: the frozen sentence's last clause is literally true, and that is the exposed surface

`R100ConnectorSiblings-c1-noncapture.txt`: a rev record citing `notes/only-challenge.txt`, whose challenge bytes are in
no `corpus/captures/` entry at that rev, prints `S230 OK … ok=1 fail=0`, **exit 0**. This is C1's fourth sentence
("A rev record whose blob is not a capture of that rev is not judged by CHALLENGE") working as written — not a
false statement. Recorded because it fixes the attack surface for round 101: the identity gate is what makes a
one-byte-different challenge copy (named limit b) and every non-capture challenge page pass, and only a digest anchor on
the record (route R3) can judge those bytes without judging every rev blob.

## Routes (no absorption — next round's L1 decides)

- **R1 (adopt, C2):** kagi QM70/QM73 + tabi/kama — an `on-release` must name its watcher (command + predicate) in the
  same commit, and a fired clock's line is re-run or scoped down. chousa's `recheck:` vocabulary already permits it
  (`corpus/QUALITY.md` criterion 6: "optionally followed by the re-run command").
- **R2 (adopt, C2):** tameshi's MISS-record exclusion is the general form of F2 — a record's own text about missingness
  must not count as evidence. Whatever tool decides a future firing must exclude the entry's own prose.
- **R3 (adopt, C1):** kama `digest-ledger` + kagi carrier-binding — a rev GATE-RECORD that asserts it cites a capture
  should carry the blob's digest, and `is_challenge` should judge the cited blob's own bytes when that assertion is
  present. This closes named limit (b) and F1 without judging every rev blob (q3 stays positive).
- **R4 (adopt, C1):** tsukuroi `check-knowledge-refs-r68` — resolve the registry at the same revision the captures are
  resolved at; today `--repo` and `--root` can name different trees.
- **R5 (note, C1):** kagi QM76 requires a `kind: gate` registry row to carry a runnable `--selftest`; chousa's
  `tools/gate-records.py` has no `--selftest` at all (its battery lives in `corpus/evidence/round100/`). Not claimed by
  C1, but the review round should route it rather than re-derive it.

## Bounded proposed move (connector duty — one move, freshness axis)

**M1 (round 101, ~10 lines): make "fired" falsifiable, and name the next watcher.**
1. Add `f14` to `corpus/evidence/round100/entry-controls-r100.py`: the F2 denial (`fired` → `has NOT fired; no new
   release exists` in the r99 `## Update`, link intact). It must be refused, i.e. `FRESH=0/1`; today it is accepted
   (F2 receipt).
2. Change `recheck:` in both quotation entries (and rows S236/S238) from bare `on-release` to
   `on-release — <command>` in tabi/kama shape, the command being the Europe PMC REST search already used by S238's URL,
   bounded to the author pair + "quotation", with a printed predicate (a newer record's `pmid`).

**Affected axes.** Freshness improves: the firing becomes a leg that can fail (f14) and the next release becomes
detectable by a named watcher (R1). Operability is untouched: `tools/gate-records.py` is not edited; both edited entries
are HARM files whose GATE-RECORD lines are unchanged, so the C1 predicate line must reproduce byte-for-byte.

**Risks.** (i) f14 changes C2's frozen line (`FORGERY_REFUSED=13/13` → `14/14`), so it is a round-101 amendment, not an
edit to round 100's predicate; (ii) a `recheck:` command is unproven until a gate consumes it — without the f14 half the
"fired" claim stays prose with a longer sentence (kagi QM73's exact warning); (iii) the Europe PMC watcher needs an
egress approval table row and must not be written into `corpus/captures/` (the round-100 approval discipline).

**Verification.** On the candidate tree: `entry-controls-r100.py` → `FORGERY_REFUSED=14/14`, `ENTRY_CONTROLS_R100=PASS`,
and the same control on the un-mutated entry still PASS; `challenge-controls-r100.py` → the frozen C1 line unchanged
(`HARM_SAME=27/27` unchanged, since the two edited files gain no GATE-RECORD);
`research-gate.sh verify-metadata` on both entries → `METADATA_COMPLETE=1/1`, and `recheck=scheduled` (not
`unscheduled`) still prints.

## Receipts (this directory)

`R100ConnectorSiblings-c1-battery.txt` · `-c1-base.txt` · `-c1-raw-shadow.txt` · `-c1-noncapture.txt` · `-c1-pairs.txt` ·
`-c2-entry.txt` (in `-c2-counts.txt`) · `-c2-counts.txt` · `-c2-fired-mutant.txt` · `-onrelease-model.txt` ·
`-sibling-evidence.txt` · `-identity-tools.txt`

VERDICT: R100ConnectorSiblings C1 held — the predicate line, the before-line and all 14 rev cases reproduce on F; the `.raw` sibling rule lets a record's quote come from a challenge page whose CHALLENGE verdict is read from another file (F1, a contradiction between the C1 sentence and its kill rule, not a false sentence).
VERDICT: R100ConnectorSiblings C2 held — all five counting commands reproduce exactly; the sentence's word "fired" is asserted by no instrument, and the denial forgery that should kill it is accepted (`FRESH=1/1`, exit 0), with no clock anywhere in the lane that could observe a release.
