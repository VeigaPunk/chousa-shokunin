# Round 61 · w1 · RevProvince — province review

Seat: reviewer (leaf, no dispatch). Lane HEAD `9f32ac0`; frozen claims sha256 `9afec8d4…ce0acec` (as named by L1).
Question: is hardening a span builder's output directory, and an entry on symlink/rename semantics, inside chousa's province, or does it belong to a sibling?

## Findings

1. **Builder hardening is in province.** `tools/build-spans.py` is chousa's own instrument. SKILL.md registers it as the lane-level span builder (gate rows for `build-spans`, rounds 55 and 56). PROVINCE.md `Owns` names "this lane's own corpus and gates". The builder writes lane corpus artifacts (`spans.tsv`, `spans/`), so its output directory is lane-owned by definition.
2. **The lane already holds this subject for its own gates.** Symlink, hardlink, mount-alias and TOCTOU entries are in the lane's knowledge tree and were written for chousa's own source-reading gates: `corpus/knowledge/hardening-r10.md`, `hardlink-alias-r13.md`, `mount-alias-r14.md`, `sweep-symlink-r19.md`, `pointer-boundary-r21.md`, `metadata-screen-r25.md`. The round-61 entry extends that line to the output side. That is precedent for in-province, not an absorption.
3. **No sibling province claims span-builder output safety.** Commands run (read-only, from `/home/vgpnk/Projects/shokunin`):
   - `grep -liE 'span manifest|span builder|build-spans|spans\.tsv' */PROVINCE.md | grep -v '^chousa'` returned no lines.
   - `grep -ciE 'harden|symlink|rename|O_NOFOLLOW|TOCTOU|output director' kumitate-shokunin/PROVINCE.md` → `0`.
   - The same grep on `tsukuroi-shokunin/PROVINCE.md` → `1`, at line 241 (see Overlap B). It is not a claim on host hardening.
   - Across all `*/PROVINCE.md`, the terms symlink/TOCTOU/O_NOFOLLOW/hardening hit only kagi, kaidoku, kake, mado and souji, each about its own reader, its own removal fence or its own tool. None claims application output hardening.
4. **Host hardening is not what the claim covers.** The task framing ("tsukuroi: host hardening") does not match tsukuroi's PROVINCE. Tsukuroi owns read-only OS substrate state (pacman, systemd, driver/firmware, boot) and "never installs, upgrades, or removes packages; never restarts services". The C1/C2 subject is an application writer's guard on its own output directory. No tsukuroi surface covers it.
5. **POSIX syscall semantics: no owner.** No `*/PROVINCE.md` claims open(2)/rename(2) semantics as domain. The C2 entry cites the primary man pages (`/usr/share/man/man2/open.2.gz`, `rename.2.gz`) for a claim about one tool. That is the lane's source-hierarchy method (primary sources) applied to its own gate. It is in province only while it stays scoped to that tool (see Adjacency line, and Risk R1).
6. **Calibration point on the pending rows.** `grep -c S134 corpus/SOURCES.md` at `9f32ac0` → `0`. Rows S134–S137 do not exist yet. The claims file says the L1 appends them after sources are opened, so C2's ROWS leg cannot pass before that. This is a pre-landing state, not a province finding. I did not run `c2-count.py`, since that is the L1's verification.

## Overlap with the evidence

- **A. Souji (deletion receipts) — adjacent, not contested.** `tools/build-spans.py` lines 202–206 run `sd.mkdir(...)`, then `p.unlink()` on any `spans/` entry matching `SPAN_RE` that the new run does not name. That is a deletion act. Souji's PROVINCE owns "receipt-gated removal" and states that its own fence is "not a universal defense against hostile bind mounts, hardlinks or concurrent filesystem replacement" (souji PROVINCE.md, Round 14 boundary). The builder's orphan-unlink is chousa-internal and is cited here as evidence, not as a removal policy. Any generalisation (a shared "safe delete in output dirs" rule) belongs to souji.
- **B. Tsukuroi (sourced rename-write precedent) — adjacent, not contested.** Tsukuroi PROVINCE.md lines 239–241 carry a Frontier entry that reads btrfs-progs `cmds/scrub.c` for its `_tmp`-then-rename write under `flock`. That is a sourced rename-write mechanism, but about another program's on-disk host record that tsukuroi observes. Chousa's entry is about its own writer. Keep the two separate: a rename-write question about a host record stays tsukuroi's.
- **C. Kumitate / tameshi (bounded child runner) — adjacent, not contested.** The C1 counter (`corpus/evidence/round61/c1-count.py`, amended A1) gives each child its own session, a 512 MiB file-size limit and a process-group kill. Kengaku's PROVINCE (round-38 split, lines 312–325) names the fleet bounded runner as kumitate's (`cap-run.mjs`) and the sandboxed-probe method as tameshi's. The counter's child-harness code is chousa gate code. It is cited as prior art, not absorbed into kumitate's runner.
- **D. Kaidoku / revenger / kagi — not overlapping.** Kaidoku's symlink refusals (PROVINCE.md:358, :382–400) are its own reader's refusals on shipped artifacts. Kagi's symlink count is a census row. Neither governs an output writer.

## Adjacency line the report must carry (verbatim in any downstream report or entry)

> ADJACENCY (chousa r61 C1/C2): the span builder's output-directory hardening (`tools/build-spans.py`) and the `derived-output-safety-r61` entry are chousa's, under its own gates. POSIX open(2)/rename(2) text is cited from primary man pages as ground for that tool only; it is not a chousa claim about syscall semantics in general. Not claimed here: host filesystem or OS state (tsukuroi; read-only, no remediation, and its btrfs-scrub `_tmp`-then-rename entry is a different writer); any generalised removal or orphan-deletion policy (souji, receipt-gated); the child-process runner pattern (kumitate `cap-run.mjs` per the fleet round-38 split; the counter's own child harness is cited, not absorbed); shipped-artifact reverse engineering (kaidoku, revenger); secret material (kagi).

## Risks

- **R1 — scope drift of the C2 entry (medium).** Its Claims 1–3 are general POSIX statements (O_NOFOLLOW guards the final component only; O_EXCL on a symlink fails; rename overwrites a link). If the entry is later cited as chousa's authority on filesystem semantics, it overreaches the lane's province. Mitigation: the adjacency line above, carried with any citation.
- **R2 — the claim-to-quote check is structural (named limit, unchanged).** `c2-count.py` does not judge whether a claim follows from its quotes. Province review cannot close this either.
- **R3 — no verification run by this seat.** I read the frozen files and the sibling PROVINCE files only. I did not run `c1-count.py`, `c2-count.py`, `regress.py` or the controls, since the item does not ask for them.

## Commands run (read-only; no writes outside the report and scratch)

- `cat chousa-shokunin/PROVINCE.md`; `cat */PROVINCE.md` (kumitate, tsukuroi, mori, souji, tabi, kasegi, kengaku, tameshi, kotoba, kama, kagi; grep-scoped for kaidoku, kake, mado, lane3).
- `sed -n 52,70p chousa-shokunin/SKILL.md` (Boundaries).
- `cat corpus/evidence/round61/claims.md` (sha256 `9afec8d4…` as named; claims read as frozen).
- `grep -ciE '...' */PROVINCE.md` and the sibling greps above (outputs in Findings 3 and Overlap).
- `sed -n 98,110p souji-shokunin/PROVINCE.md`; `sed -n 236,244p tsukuroi-shokunin/PROVINCE.md`.
- `head -c 2500 corpus/evidence/round61/controls/c2-positive-entry.md`; `sed -n 1,40p corpus/evidence/round61/c2-count.py`.
- `sed -n 190,210p tools/build-spans.py`; `grep -nE 'rename|unlink|symlink|...' tools/build-spans.py` (only `p.unlink()`/`write_bytes` lines matched in the write path).
- `grep -c S134 corpus/SOURCES.md` → `0`.
- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin log --oneline -3 -- corpus/knowledge/{hardening-r10,hardlink-alias-r13,sweep-symlink-r19}.md` (read-only).
- Scratch `/fast/scratch/hyaku/chousa-r61/RevProvince` created empty; removed before yield.
- Installs: none.

## Not verified

- No counter, control or regress run. The C1 and C2 scores are the L1's to verify.
- The claims in the C2 entry were not checked against the man pages in this seat; they are the claim-verification reviewers' job.
- Sibling PROVINCE files were read at their working-tree state, not at pinned commits. Tsukuroi's own declaration warns that sibling declarations drift.

VERDICT: PROVINCE=in contested_with=none
