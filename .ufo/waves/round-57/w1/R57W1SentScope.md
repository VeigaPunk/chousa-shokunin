# R57W1SentScope — round-57 w1 sentinel: trust boundaries and failure modes

Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`, HEAD at review `e0e73e0` (the C2 receipt, one commit past the
dispatch tip `f9736a3`). Read-only: no lane file touched except this report; no fetch; no install (none needed).
Scratch `…/chousa-r57/R57W1SentScope/` (two throwaway clones) **deleted before yield** — nothing left on disk.
Axes: **freshness** (does C2's PASS follow from committed bytes, or only from destroying evidence), **depth** (C3 build start; quarantine coverage), **calibration** (frozen artifacts = freeze-time bytes).

## Hazard (1) — lane status, every path classified
`git status --porcelain` @08:41:30Z: 30 `??`, 1 `M`, 1 `D`; re-run @08:43: a **second `M` appeared mid-wave**.

| paths | class |
|---|---|
| `M corpus/evidence/round57/refetch.tsv` | L1 fetch loop, rows 104-117 appended (S131-S136). No id is in C2's frozen SET (S082-S130) → C2 invariant (proved below). |
| `D …/w1.ready.partial`, `?? …/w1.ready.dispatched` | wave launcher state renamed mid-run (L1) |
| `?? .ufo/waves/round-57/w1/*.md` (16, incl. this) | seat reports, correct directory |
| `?? corpus/captures/{0cebd3c8,6f545e6c,9695437c,ad3010d2,c71776bc}.{raw,txt}` | L1 fetch output S133-S136; key = sha256(url)[:24] and digest = its row's `raw_sha256`/`txt_sha256` — audited 111 rows / 60 triples: 0 key errors, 0 digest errors |
| **`M corpus/evidence/round45/spans.tsv`** | **NOT conforming — unauthorized lane write to committed evidence (below)** |

**Unauthorized manifest rewrite (the wave's integrity defect).** At 08:41:51Z, ~20 s after my first snapshot, a
committed spans manifest changed; `git diff` = 2 insertions / 2 deletions, both S083 rows now carry the **drifted**
digest with uniformly shifted offsets:

    -S083  …/2305.13117v3  a3ff65e0db9c…cf8f  14415  spans/S083-1.txt  we cache all pages used as evidence…
    +S083  …/2305.13117v3  d37b64ed18a8…b101  14332  spans/S083-1.txt  we cache all pages used as evidence…
    -S083  …/2305.13117v3  a3ff65e0db9c…cf8f  120724 spans/S083-2.txt  Archive.org returns a 404 page for these
    +S083  …/2305.13117v3  d37b64ed18a8…b101  120641 spans/S083-2.txt  Archive.org returns a 404 page for these

The new pin `d37b64ed…` is the *fresh* `.txt` digest (refetch.tsv row S083 `txt_sha256`); the old pin's bytes no
longer exist here, which is why S083 is DRIFTED. Neither offset lands on its quote in the fresh text form: byte 14332
reads `s. Questions may have multiple answers…`, byte 120641 `teratively, one at a time…`; the quotes sit at bytes
**14671** and **121576**. So the edit launders a drift into a "pin" *and* leaves the row internally inconsistent.
Authorization: `grep -c 'round45' w1-spec.json` → **0**; no seat report mentions it; the wave contract makes a seat's
own report its only write. Effect on the frozen claim: **none today** — `pinned_set()` reads `git show 6656f077:…`
(`c2-count.py:87,92`), so C2 still prints `S083 … pin=a3ff65e0db9c DRIFTED absent=0/2`. Effect if committed: any
re-freeze at a new SET_REV inherits a pin that *is* the drifted bytes, and round-45's S083 provenance is destroyed.
At 08:45:03Z it was rewritten again and now equals HEAD (`md5 7a1f6381…` vs `4110e6e6…` at the tamper; `git diff`
empty) — net-zero today, but a seat is writing committed evidence in the lane and the laundered content was live for
3 min. Likeliest author: a "verify the store reproduces every committed spans manifest" seat (ExecSpansHeld)
rebuilding in place — a verification that mutates what it measures. **HIGH** (method); remediation: the seat rebuilds
only in scratch, and the L1 confirms no commit captured the intermediate state.

## Hazard (3) — fleet root (the misroot class)
`find /home/vgpnk/Projects/shokunin -maxdepth 1 -newer …/claims.md` → `.scratch/`, `.git/`, `MANIFEST.json` only;
`git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all` → **0 lines**. The one tracked write
is the orchestrator's (`a7603f9c protocol-shokunin … rounds ledger … — hyaku, non-author`, `MANIFEST.json | 37`, an
ANCESTOR of HEAD). **No seat misroot**: no fleet `.ufo/waves/round-57` exists; the fleet `.ufo` holds only older
`gates/` + `history-pin.json`.

## Hazards (2) and (4) — report dir and scratch trees
`.ufo/waves/round-57/w1/` @08:41: 15 `<Seat>.md` + `swarm-registry.json` (tracked L1 state). Machine check over
`w1-spec.json`: 65 items, all name `Report: .ufo/waves/round-57/w1/<name>.md`, **0 bad**; no stray report. Role
census matches the dispatch receipt: `{executor:21, reviewer:13, scout:12, scribe:6, critic:6, mutation-tester:2,
connector:2, sentinel:1, revenger:1, simplifier:1}` = 65, attack share 21/65 = 32%. Of 32 scratch dirs, the
report-bearing seats left no tree (`REPORT_BUT_TREE_LEFT: []`; `dryrun`/`fetch` are L1's); still live and large:
`R57W1ExecDoNothing` 192786 files, `R57W1ExecC2Recompute` 47294.

## Freshness — C2 reproduces, but its PASS is bought by deleting bytes
**Survived.** A pristine `git clone --shared` at `e0e73e0` (clean tree) reproduces the receipt from committed bytes only: `SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS`, exit 0;
at `c2f914c` it prints `VERDICTS=0/47 … C2=FAIL`, byte-equal to `controls/c2-before.txt`. The worktree tamper above
does **not** move it (git-pinned SET_REV).

**Fail-open.** `c2-count.py:205-236` gives no verdict to a capture on disk whose attempts all failed (`if
raw_p.is_file():` … verdict stays `MISSING`; `UNREACHABLE` is the `else`), so a failure-only URL can be counted only
by deleting its bytes — and the receipt did: `git show --stat e0e73e0` → `corpus/captures/e3ca8f4f….raw | Bin
4482989 -> 0 bytes` (S105). Isolation on the pristine clone, clean tree, adding **exactly one file** (`git show
e0e73e0^:…/e3ca8f4fdd15420b80096a75.raw`, 4,482,989 B, `%PDF-1.5`, sha256
`d36191c72a5ee007e0354b5160d207cffa9e59be86536c997a7dcff9db8ebcb6`):

    SET=47 VERDICTS=46/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=0 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=FAIL (exit 1)
    remove that file → exit 0

"One verdict from committed bytes" holds for 46/47; for S105 only because the evidence was destroyed. **MEDIUM**
(disclosed in the commit subject, recoverable). Remediation, non-frozen: record the blob's sha256/size/`git show
e0e73e0^` path in the round-57 lesson; give a future claim a `PARTIAL` verdict so no claim is forced to delete.

**Same class, live (outside C2's SET).** `d473754a….raw` (1,486,070 B) and `d8b4f8f8829b813f16227893.raw`
(1,285,794 B) are `.raw`-only with failure-only rows (S135/S136, `curl_rc=28 http_code=200 raw_sha256=-`); `file`
calls the first `PDF document, version 1.5, 66 page(s)` — a complete-looking 抗肿瘤 2022 guide neither counter may count; deleting it would repeat S105, so it stays and C3 must not bind on it.

**Success-class defect (MEDIUM, hits C3 candidates).** The frozen success test (`curl_rc==0`, 2xx, non-empty) admits
an anti-bot interstitial: S135 `ad3010d2…` and S136 `0cebd3c8…` are 4,321-byte `<html><script>var arg1='CFB61F5C…'`
JS challenge pages recorded as success, whose defined text form is **one space** (both `.txt` = 1 B, sha256
`36a9e7f1…` = sha256(" ")). Under C2 that can only be DRIFTED (the pin is checked on the raw), so C2 stays sound; under
C3 such a capture can never hold a heading. Future claims must require a non-blank text form for success.

## Depth — C3 at build start; the quarantine slice has one uncovered row
`python3 …/c3-count.py` @08:41 (unmodified): `SWEPT=0/7 -`, `QUOTE_ROWS=0 … CAPTURE_BOUND=0`, `SUBSTANCE=FAIL
ANCHOR_BOUND=0/0 INFERENCE_GROUNDED=no`, `C3=FAIL`; entry, `corpus/evidence/round57/c3/` and the round-57 lesson are
absent — a build start with no readiness claimed, so not a defect.
**Quarantine conformance.** The register carries 24 chousa data rows (20 `payload-absent` + 4 prose S100-S103),
matching QuarD's "confirm 24". Batches from `w1-spec.json` cover 23 distinct rows: A S077 S080 S082 S084 S086 S088 ·
B S093 S094 S095 S104 S105 S108 · C S110 S111 S112 S114 S116 S120 · D S125 S116 + prose S100-S103. **Uncovered:
S096** (register line 46, `payload-absent`, CiNii manual) — its capture is C2-REPRODUCED
(`6dc68fd6b32ce9c8dfcebce8.*`), so it is checkable and merely unassigned. LOW; add it to QuarC.

## Calibration — frozen bytes intact; one commit message over-claims
`c2-count.py` sha256 `d6885bae…` = `git show c2f914c:…`; `c3-count.py` `c565ce4a…` = `git show fd95724:…`; control
builders `1aebeb5b…`, `2383325e…` unchanged. UNREACHABLE is the frozen rule (`if len(fails) >= 2 and
(fails[-1]-fails[0]).total_seconds() >= 600`, line 231); S105 rows `08:06:12Z / 08:30:12Z / 08:33:48Z`, all
`curl_rc=28` → gap 1656 s, verdict correct as written. **Provenance defect:** `f9736a3`'s subject says "misroot sweep
… recorded in the round lesson", but `git show --name-only f9736a3 | grep -c lessons` → `0`, `git log --all --
…/round-57.md` → empty, and `R57W1ScribeLesson.md` has no `misroot` text: the record does not exist while a commit
asserts it (LOW-MEDIUM, fabricated provenance). ScribeLesson must carry the sweep with `sha256sum` of both copies
(round-33 E5) before the L1 commits the lesson.

## Severities

| # | finding | sev | exploit / impact | smallest remediation |
|---|---|---|---|---|
| S6 | unauthorized rewrite of `round45/spans.tsv` (pin → drifted digest, offsets ≠ quote), self-reverted at 08:45:03Z | **HIGH** (method) | laundered drift on any re-freeze; S083 provenance destroyed; invisible to C2 today | seat rebuilds in scratch only; L1 confirms no commit captured the intermediate state |
| S1 | C2 PASS depends on deleting S105's 4.48 MB; same class live at `d473754a`/`d8b4f8f8` (a complete 66-page PDF with no successful record) | MED | restore blob → `VERDICTS=46/47 C2=FAIL`; no verdict for bytes-without-success | record blob sha/size/recovery; `PARTIAL` verdict in a future claim; leave the live pair, name it in the lesson |
| S2 | success test admits a JS-challenge page (`.txt` = 1 space) | MED | looks fetched, can never bind; self-consistent digests hide it | future: require a non-blank text form |
| S4 | quarantine row S096 unassigned | LOW | one fabrication-class row never hand-checked | add to QuarC |
| S5 | `f9736a3` asserts a lesson record that does not exist | LOW-MED | fabricated provenance | ScribeLesson records the sweep before commit |
| — | counters/manifests unedited; SET from git; fleet root clean; no seat misroot; no leftover seat scratch | — | attacks that failed | none |

VERDICT: attacked R57-C2's freshness receipt (committed-byte reproduction, set tamper, deletion and success-class
boundaries), R57-C3's build-start/quarantine conformance, and the wave's lane-write boundary — the receipt reproduces
and manifest tamper cannot move C2, but C2's PASS **does not survive** as a committed-bytes statement for S105 (the
deletion is what passes), quarantine leaves S096 unassigned, and a committed manifest was rewritten unauthorized.
