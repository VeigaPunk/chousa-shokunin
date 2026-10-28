# Round 61 · w1 · ConnSiblingOverlap (connector) — sibling-overlap scan

Scope: read-only scan of `/home/vgpnk/Projects/shokunin/<lane>-shokunin/{PROVINCE.md,corpus/SOURCES.md,corpus/knowledge}` for write-safety and OS-semantics overlap with the round-61 claims C1 (span builder output safety) and C2 (sourced derived-output safety entry). No sibling file was written; no git, network or fleet write; no install. Scratch created and removed.

## Findings

1. **souji-shokunin already holds the closest sourced material on atomic publication, exclusive creation, and fsync — the strongest overlap.**
   - `corpus/knowledge/origin-record-exclusivity-r28.md` (O_CREAT|O_EXCL atomic; rename() atomic, failure leaves target untouched) — sources S212, S213 (POSIX.1-2024 open/rename pages, snapshots `census/round-28/sources/{open,rename}.html`).
   - `corpus/knowledge/origin-record-durability-r28.md` — fsync is the durability primitive; atomicity ≠ durability; S214.
   - `corpus/knowledge/origin-record-writer-r27.md` — GLib `g_local_file_trash()` write-then-move sequence (S152).
   - `corpus/knowledge/trash-spec-restorable-quarantine.md:11-12,28` — info file created first with O_EXCL; spec §5 forbids a symlinked `.Trash`; r10 C2-Q1 symlinked quarantine root followed by mv/rm.
   - `corpus/knowledge/quarantine-same-filesystem-rename.md:11-12` — atomic staging only when `stat -c %d` matches; `quarantine-staging-no-copy-r23.md` — RENAME_NOREPLACE (S109–S111).
   - `corpus/SOURCES.md` S110 — rename(2), man-pages **6.19**, § DESCRIPTION RENAME_NOREPLACE, snapshot `census/round-22/attempt2/sources/man7-rename.2.txt`.
   - Code-side guards: `tools/souji-quarantine.sh:527` (`quarantine-collision`) and `:1302` (`symlink-or-noncanonical-quarantine-path`), as cited in `trash-spec-restorable-quarantine.md:32`.
   - Man-page sourced OS semantics: `corpus/SOURCES.md` carries 68 `man7.org|man-pages|man N` matches (highest of any sibling); rows S068/S075 (proc_pid_stat(5)), S082/S095/S096 (proc fd/cwd access rule), S070/S077 (open(2) ENXIO), S110 (rename(2)).

2. **kumitate-shokunin holds the most in-tree practice on O_NOFOLLOW / O_EXCL / rename+fsync, documented in knowledge rows, with a deliberate policy divergence.**
   - `corpus/knowledge/local-ship.md:131,152,226` — `read_bounded_ident` opens with `O_CLOEXEC|O_NONBLOCK` and **no** O_NOFOLLOW (symlinked contract files followed by design); `atomic-write.mjs` (cited there) adds O_NOFOLLOW on its dir open. Also `:178` — "lstat-walk→metadata→open→rename TOCTOU is unmitigated" (D-A, moderate, self-declared).
   - `corpus/knowledge/route-probe-cluster.md:164-166` — `writeVerdict` via `openTmpExclusive` (`O_EXCL`), `renameSync`, parent-dir fsync; "the former `atomic-write.mjs` dependency is inlined here".
   - `corpus/knowledge/native-trial-launch.md:71,121,140,191` — receipts/verdict written O_EXCL 0600; `O_WRONLY|O_CREAT|O_NOFOLLOW|O_NONBLOCK + fstat + nlink>1 refuse`.
   - `corpus/knowledge/route-resolution.md:32`, `reconcile-and-cycle.md:169`, `remaining-scripts-census.md:616` — fd-bound reads with O_NOFOLLOW + fstat.
   - INFERENCE/[checked]: `find $S/kumitate-shokunin -name 'atomic-write*'` returned nothing; the file named in knowledge is not in the tree now (consistent with the "inlined" note).
   - Cites no man page or rfc; sourcing for these O_* semantics is not in kumitate SOURCES (7 man-page matches, none on O_NOFOLLOW — INFERENCE from the grep, not read line by line).

3. **kagi-shokunin**: `corpus/knowledge/tac-evidence-integrity.md:41,80` — `O_WRONLY|O_CREAT|O_EXCL` 0600 for tac-daybreak JSON; second run cannot overwrite. Single-instance knowledge; no sourced row for O_EXCL semantics found in its SOURCES.

4. **audio-shokunin**: `corpus/knowledge/2026-10-14-sox-transport-axis.md:5` names a known defect — `build_artifacts.py` "rewrites WAVs non-atomically"; fix = temp-file + `os.replace`, "not yet integrated". Verified: `corpus/fixtures/build_artifacts.py` writes via `wave.open(..., "wb")` directly (lines 18, 34, 41, 53, 68, 83, 154, 169) and contains no `os.replace`. Open named debt, not a sourced atomic-write entry.

5. **tameshi-shokunin**: write-site census, not safety. `corpus/knowledge/r40-write-form-misses.md:10,18` (os.replace as a write site), `r41-variable-destination-writes.md:67` (os.replace/os.rename counted as two destinations), `r42-attribute-and-outflag-destinations.md:103`. Tools `tools/write-path-census{,-v2,-v3,-v4}.py`. These classify where writes go; they do not judge symlink or atomicity safety. Adjacent: a sibling-owned counter touches the write-site surface.

6. **chousa-shokunin (own lane, listed for duplicate-check)**: no chousa knowledge file names O_NOFOLLOW, O_EXCL, rename(2), RENAME_NOREPLACE or os.replace (grep over all corpus/knowledge files). Read-side alias/TOCTOU rows exist and are a standing decision: `hardlink-alias-r13.md:42`, `mount-alias-r14.md:48`, `root-slash-boundary-r15.md:70`, `sweep-symlink-r19.md:32-36` (check-to-use race remains), `verification-r16.md:33,45,56`, `hardening-r10.md:479,582`. Chousa's SOURCES already cites installed man pages without fetching the URL (S064 execve(2), S067 exec(3)) — same access-disclosure pattern C2 uses. No chousa row covers derived-output (write-side) hardening.

7. **Adjacent, not counted**: kaidoku-shokunin (extraction publishes "every oracle regular file", one `unpublished-entry` per symlink; `PROVINCE.md:358` refuses symlinked db/journal paths) — a derived-output publication rule in a different sense. tsukuroi (`symlink` hits in boot-chain and update-safety rows) and tabi (Singleton* symlink triples) — not write-safety. mado/mori `atomic` hits are Wayland commit and kernel counter usage — unrelated.

## Overlap relation to the new C2 entry (`derived-output-safety-r61.md`)

- **Duplicates (risk):** if S134 or S135 are rename(2)/open(2)-class pages (the claims file does not name their topic — INFERENCE), they re-derive souji S110 (rename(2), man-pages 6.19 — the same release as the chousa installed `man-pages 6.19-1`) and souji S212/S213 (POSIX open/rename). Same primitive, different row IDs. Calibration cost: the entry adds no new fact for those leaves unless it adds a derived-output angle souji does not state.
- **Complements:** no sibling row states the output-directory case (an output dir path resolved under a lane root, parent-dir O_NOFOLLOW + fstat, nlink>1 refusal, publish by rename + fsync of the parent). souji covers quarantine/origin records and the trash-spec symlink rule; kumitate covers the code pattern without a sourced entry. C2's derived-output angle is therefore not a duplicate of any single sibling row.
- **Contradicts:** none found. kumitate's deliberate "no O_NOFOLLOW on contract reads" (local-ship.md:131) is a design choice for reads, not a claim about write publication; it does not conflict with a write-side entry.

## Overlap table

| Lane | Path | Subject | Relation to C1/C2 |
|---|---|---|---|
| souji | corpus/knowledge/origin-record-exclusivity-r28.md; origin-record-durability-r28.md; origin-record-writer-r27.md | O_EXCL, rename atomicity, fsync | duplicate risk for C2 leaves; complement on output dirs |
| souji | corpus/knowledge/trash-spec-restorable-quarantine.md:11-12,28 | O_EXCL info-first; symlinked trash root refused | complement |
| souji | corpus/SOURCES.md S110, S212–S214 | rename(2), POSIX open/rename/fsync | source-level duplicate risk (same man-pages 6.19 release) |
| souji | tools/souji-quarantine.sh:527,1302 | collision and symlink refusal in code | complement (code guard, not a counter) |
| kumitate | corpus/knowledge/local-ship.md:131,152,178,226 | O_NOFOLLOW (deliberately absent on reads), TOCTOU unmitigated | complement; policy contrast |
| kumitate | corpus/knowledge/route-probe-cluster.md:164-166; native-trial-launch.md:71,121,140,191 | O_EXCL tmp, rename, fsync; O_NOFOLLOW+fstat+nlink | complement (in-tree practice, no sourced row) |
| kagi | corpus/knowledge/tac-evidence-integrity.md:41,80 | O_EXCL 0600 no-overwrite | complement (single instance) |
| audio | corpus/knowledge/2026-10-14-sox-transport-axis.md:5 | non-atomic WAV write, os.replace unintegrated | contested only as an open defect |
| tameshi | corpus/knowledge/r40–r42-*.md; tools/write-path-census*.py | write-site classification incl. os.replace | adjacent; no safety judgment |
| chousa (own) | corpus/knowledge/hardlink-alias-r13.md:42; mount-alias-r14.md:48; sweep-symlink-r19.md:32-36; hardening-r10.md:479 | read-side TOCTOU standing decision | C1 limit (i) repeats this decision; consistent |

## Commands (all read-only; cwd absolute paths)

- `grep -rEil -- '<term>' $S/*-shokunin/PROVINCE.md $S/*-shokunin/corpus/SOURCES.md $S/*-shokunin/corpus/knowledge` for `O_NOFOLLOW`, `rename\(2\)`, `os\.replace`, `TOCTOU|TOCTTOU`, `RENAME_NOREPLACE`, `O_EXCL`, `atomic`, `symlink`, with `$S=/home/vgpnk/Projects/shokunin`. Output: O_NOFOLLOW 5 files (all kumitate); rename(2) 1 (souji SOURCES); os.replace 4 (tameshi 3, audio 1); TOCTOU 10; RENAME_NOREPLACE 3 (souji); O_EXCL 11 (souji 6, kumitate 4, kagi 1). `atomic` and `symlink` exceeded head -40 and were not fully counted; their hits were classified by line-level grep, not by total.
- Line-level `grep -rnE` on kumitate, tameshi, audio, kagi and souji (O_NOFOLLOW, TOCTOU, os.replace, O_EXCL, rename(2)) — quoted above with line numbers.
- `grep -nE '^\| S13[0-9]' chousa-shokunin/corpus/SOURCES.md` — rows stop at S133; S134–S137 absent (consistent with the claims file: L1 appends them).
- `sed -n` reads of kumitate local-ship.md, route-probe-cluster.md, souji origin-record-writer-r27.md, tameshi r40 head.
- `find` for `atomic-write*` in kumitate (none), `build_artifacts.py` in audio (corpus/fixtures and corpus/live only; no tools/ copy), `write-path-census*.py` in tameshi (four versions).
- `ls chousa-shokunin/corpus/knowledge` — 100+ files, none named for write-side hardening.
- Not run: no counter, builder or test was executed; no sibling file was opened beyond the cited lines. `symlink` and `atomic` hits outside the write-safety reading were not individually reviewed (tsukuroi, tabi, kotodama prose hits classed as noise).

## Installs

None.

## Limits

- Topic of S134/S135/S136 is not stated in the frozen claims file; overlap with souji S110/S212–S214 is therefore a risk statement, not a measured duplicate.
- Grep is lexical; a sibling could hold a derived-output rule without any of these terms (e.g., "publish", "staging dir"). Not searched.
- `symlink` total count not captured (head cut at 40 files).

VERDICT: SIBLING_OVERLAPS=5 contested=souji-shokunin
