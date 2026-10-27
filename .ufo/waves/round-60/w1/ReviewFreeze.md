# ReviewFreeze — round 60, wave 1 (freeze-integrity audit)

Scope: the frozen claims file `corpus/evidence/round60-claims.md`, prior committed evidence, and the current counter/source (`corpus/evidence/round60/c1-count.py`, `c2-count.py`) only. Read-only; no writes outside this report; no git/jj mutation; no external fetch.

## Verdict

1. **Post-dispatch immutability: HOLDS** on the best available evidence — the frozen file's last write (mtime 17:51:18 -0300) precedes the wave artifacts that pin it (spec 17:55:15, dispatch 17:55:19, ready 17:55:21, dispatched 17:56:56), and no git/jj writer ran in the lane after 17:05:42 (last lane commit; jj op log agrees).
2. **Freeze identity pin: BROKEN.** The pinned SHA `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440` matches no bytes on disk, in any hash form, anywhere in the lane, the wave artifacts, fleet `.ufo/`, or fleet `.scratch/` for files modified today. The mismatch was baked in **before dispatch**: the pin was minted ~4 minutes after the file's last content change. The bytes are intact; the pin is defective.

## Evidence

**E1 — current bytes vs pin.**
`sha256sum corpus/evidence/round60-claims.md` →
`65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1` (3355 bytes; birth 2026-10-27 17:50:39.84 -0300, mtime 17:51:18.66 -0300). Pin (from w1-dispatch.json:737 / w1-spec.json:63, my own seat entry): `09d8053f…a440`. **Mismatch.**

**E2 — no hash form of the current bytes matches the pin.**
sha256 as-is `6572…`; no-trailing-newline `cae804fa…`; plus-newline `ed2999d0…`; CRLF `dbb847b8…`; stripped-ws `cae804fa…`; git-blob-prefixed sha256 `d27121a5…`; `git hash-object` sha1 `5ea0acf0…`. None equals `09d8…`.

**E3 — fleet sweep: no file hashes to the pin.**
Every file under the lane (excluding `.git/`, `.jj/`), fleet `.ufo/` and fleet `.scratch/` modified after 2026-10-27 17:00 was hashed: zero matches for `09d8053f…` (grep exit 1).

**E4 — no VCS history of the file.**
`git status --porcelain` → `?? corpus/evidence/round60-claims.md` (untracked); `git log --all -- corpus/evidence/round60-claims.md` → empty (never committed). Lane jj config uses `snapshot.auto-track="none()"` and no `file track` ever named this path (op log), so no historical bytes exist in jj either. The byte history is unreconstructable from VCS.

**E5 — timeline (mtimes, full-iso).**
`placeholder` 17:50:26 → claims file birth 17:50:39, last write **17:51:18** → `c1-count.py` 17:51:38, `s101-open.txt` 17:51:43, `c1-before.txt` 17:51:47, `s101-receipt.txt` 17:52:00, `c1-control-proof.txt` 17:52:08, `c2-count.py` 17:52:14, `c2-before.txt` 17:52:19 → w1-spec 17:55:15 → w1-dispatch (pin first recorded appearance) 17:55:19 → w1.ready 17:55:21 → dispatched marker 17:56:56 → seat reports 17:56:45+. No write to the claims file after 17:51:18.

**E6 — no lane mutation post-base.**
`git rev-parse master` = `b379919a873e7080a31ef92c7002f55f5374e2c6` = the claims' declared base ("round-59 non-author review"); latest lane commit 17:05:42; jj op log's newest entries are that commit's push — no lane git/jj operation during round 60 work.

**E7 — prior-evidence and source anchors named by the frozen claims all verify:**
- Base tip `b379919a…` exists and is the lane branch tip (E6) ✓
- L0 `8d77e6c1` open: `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:136,140` ✓
- "Round-58 bytes remain frozen" — 17 tracked, clean files under `corpus/evidence/round58/` incl. `controls/build-spans-r55.py` (the pinned r55 control `c1-count.py` binds) and `claims.md` ✓
- `corpus/evidence/round59/s101-open.txt` and `.ufo/waves/round-59/w1/R59Executor09.md` tracked (count 1) ✓
- c2-count.py's own pins hold exactly: FORM `a8e3e7ad213b…` = `.ufo/waves/round-60/s101-open.txt`, RAW `6063a3aff7a4…` = `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` (tracked) — the lane's sha256-pin discipline works everywhere except the claims pin itself
- `corpus/knowledge/citation-count-semantics-r37.md` tracked; starts `\n# `; `#### Unknown` at :74 with the S101 version-in-force caveat at :79 — c2's METADATA/LIMIT checks are well-formed against real bytes
- default `--builder` `tools/build-spans.py` tracked ✓

**E8 — same-identity check.**
My received assignment is byte-identical to the `ReviewFreeze` entry in w1-dispatch.json (:735–737): same report path, same pin, same lane bounds.

## Findings by severity

**HIGH — the freeze pin is unreproducible from any bytes.** E1–E4. Because the file's last write (17:51:18) precedes the pin's first recorded appearance (17:55:19), this is not post-dispatch tampering; the L1 pinned a SHA over different bytes — either a draft that existed between birth 17:50:39 and last write 17:51:18 and was then edited without re-pinning, or bytes that never existed at this path (an in-buffer draft). Consequence: the pin provides zero tamper-evidence; every honest check false-alarms. Independently observed by `C2CounterAudit.md:22` and `S101Reopen.md:21` (and by this seat). Resolution is the L1's call, not a seat's: publish the actual bytes' pin (`6572…`) or restore byte-exact `09d8…` content — either act amends a dispatched freeze and must be recorded as such, never done silently.

**MEDIUM — the frozen predicates are not yet reproducible from committed bytes.** `corpus/evidence/round60-claims.md`, `corpus/evidence/round60/c1-count.py`, `c2-count.py`, and c2's form pin `.ufo/waves/round-60/s101-open.txt` are all untracked at freeze time; a fresh clone fails both counters (c2 exits `C2=ERROR` on the missing form). The round contract commits wave evidence at round end, which closes this — but only if the round-end commit includes all four paths. Convention drift: r58 committed its claims and capture form inside `corpus/evidence/round58/`; r60's claims file sits at `corpus/evidence/round60-claims.md`, outside the round dir.

**LOW — c1-count.py: inert `--seed`, dead leg label.** `--seed 6001` is parsed and never used, while the frozen predicate's command line names it (inert but freeze-text vs counter mismatch). In `run()`, `forged_safe` and `baseline_bad` share the identical condition (`returncode == 0 and not intact`), so `forged_safe` is unreachable and leg (c) (`forge_blocked = forge_state != "forged_safe"`) can never fail via its named state — a destructive forged builder is labeled `baseline_bad` and still fails the candidate leg. The declared property (verdicts from return codes + independently observed filesystem state; child output captured only for diagnosis, never establishing a leg state) holds as written.

**LOW — c2-count.py: `form` ignores `--root`.** `raw` and `entry` honor `--root`; `form` is bound to module `ROOT`, so a `--root <lane-copy>` run still reads the original lane's wave file. Correct while the form exists only in the lane; wrong for any clone-based reproduction (compounds the MEDIUM finding).

## Residual risk / verification gaps

- Post-dispatch immutability rests on mtime + absence of any VCS writer after 17:05:42; an untracked file has no snapshot to diff against and mtimes are spoofable in principle. No counter-evidence found; I ran no mutating command.
- The `09d8…` bytes may exist only in the L1's drafting context. Until the L1 reconciles the pin, the operative claim text is the `6572…` bytes read here — this audit binds those.
- I did not execute either counter; pre-work receipts (`c1-before.txt`, `c1-control-proof.txt`, `c2-before.txt`) exist in the wave dir and counter execution belongs to BuildCounter/SourceGate scope.
- Seat-report mtimes in `w1/` (17:56:45) marginally precede the dispatched-marker mtime (17:56:56) — the dispatcher apparently writes the marker after spawning; harmless here, noted for the orchestrator's marker semantics.

Scratch `/fast/scratch/hyaku/chousa-r60/ReviewFreeze` was used (observed-bytes copy + variant hashing) and is removed before yield.
