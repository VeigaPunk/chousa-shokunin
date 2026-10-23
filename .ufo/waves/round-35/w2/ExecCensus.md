# ExecCensus — source registry census (chousa, round-35 w2)

Seat: `chousa-r35-w2-ExecCensus`. Scope: the source registry census only. Read-only on
`corpus/SOURCES.md`; the registry was never edited by this seat (final mtime
`2026-10-23 17:00:03 -0300`, unchanged by my runs; `git status --porcelain=v1` shows
`M corpus/SOURCES.md` from the L1's mid-wave edit, not from me).

## 1. The census command (as assigned)

```
cd /home/vgpnk/Projects/shokunin
./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa; echo exit=$?
```

**Exit code: 0.** Every line of output (3 lines):

```
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

Re-run twice, byte-identical (see `census-receipt.txt`, sha256
`54f02aca6e7e16beb69bca6625866d116a63fc5f7f3d452f8f2392412881948b`).
Census script sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`.
The two W-codes are scope-splits of one URL across two rows (S050/S051 html52, S052/S053
socket.html) and per the script's own contract ("warnings do not affect clean lanes",
`scripts/sources-census.sh:33`) they do not change the status — hence `ok` + exit 0.

Fleet-wide context: `./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin`
(all lanes) → **exit 0**, 319 output lines, **0 E-codes**, 298 W-codes; `census` mode
→ `chousa rows 68`, `FLEET rows 2543`, `FLEET missing 0`.

## 2. Row count

`grep -c '^| S[0-9]' corpus/SOURCES.md` (run from `/home/vgpnk/Projects/shokunin/chousa-shokunin`):

- **First run of this seat: 66** (registry sha256 `3281259a49ffd2dd3e95b1924d494db4229fb499d90991ff7aaea10ea08c18ab`).
- **Final: 68** (registry sha256 `54bf6cc800ad3d958cfa4bf274aa852991be69e17d3095594c2337d4b19f0bf2`).

The registry grew **during** this seat's window: the L1 appended **S067** and **S068** to the
working tree (`git diff -U0 corpus/SOURCES.md` → `+| S067`, `+| S068`; committed HEAD `2b2e017`
still has 66 rows, max id S066). The census reported `ok`/exit 0 in both states, and the
lane-local frozen census agrees on the final state:
`bash corpus/evidence/round25-sources-census.sh .` → `rows=66` **before** the append,
`rows=68` **after** (same command re-run on the current tree).

Cross-check: the fleet census's own counter says `chousa rows 68`, matching `grep -c` = 68.
All 68 rows sit inside the `## Registry` section (lines 9–79; `## Paths` starts at line 80).

## 3. Last five row ids with status/tier

Final state (68 rows), columns `id | tier | status | used-by`:

```
S064 tier=A status=mined used-by=corpus/knowledge/long-span-argv-r34.md
S065 tier=A status=mined used-by=corpus/knowledge/long-span-argv-r34.md, corpus/knowledge/dead-zone-pcre-r34.md
S066 tier=A status=mined used-by=corpus/knowledge/long-span-argv-r34.md
S067 tier=A status=mined used-by=corpus/knowledge/grep-pin-r35.md
S068 tier=A status=mined used-by=corpus/knowledge/grep-pin-r35.md
```

(At the 66-row state the last five were S062–S066, all tier A / mined; S062–S063 →
`claim-record-fields-r33.md`, S064/S066 → `long-span-argv-r34.md`, S065 → `long-span-argv-r34.md, dead-zone-pcre-r34.md`.)

## 4. Does any row's `used-by` name a round-35 artifact?

**Yes — two rows, but only after the L1's mid-wave append; and only one of the round's three
knowledge notes is registered.**

- **S067 and S068** both carry `used-by = corpus/knowledge/grep-pin-r35.md` — a round-35
  artifact (`corpus/knowledge/grep-pin-r35.md`, currently untracked, `git status` `??`).
- Before the append (66-row state) **no** row's `used-by` named any round-35 artifact:
  the distinct `used-by` values across all 66 rows were only `—` plus `corpus/knowledge/*-r24.md`,
  `*-r25.md`, `*-r26.md`, `*-r29.md`, `*-r30.md`, `*-r31.md`, `*-r32.md`, `*-r33.md`, `*-r34.md`
  and `corpus/lessons/round-27.md`, `round-28.md`.
- **No row names `corpus/evidence/round35/*`** (`grep -c 'evidence/round35' corpus/SOURCES.md` → 0).
- **The other two round-35 knowledge notes are registered by no row**:
  `corpus/knowledge/bash-local-expansion-r35.md` and
  `corpus/knowledge/keyed-engine-output-equivalence-r35.md` → 0 matches in `corpus/SOURCES.md`.
  `grep-pin-r35.md` is the only r35 note with a registry row.

## 5. Calibration probes of the census itself (scratch copies only)

Experiments ran on copies under `/tmp/hyaku/chousa-r35/w2/ExecCensus/` (probe receipts:
`probe-receipts.txt`, sha256 `8c84e65f974e94a05ad464a953d4a7b76d2399a27768991c471f5c67a150cd12`).
The production registry was not touched.

| # | mutation on a scratch copy | census verdict | exit |
|---|---|---|---|
| P1 | clean copy of the live registry + `corpus/knowledge/` + `corpus/lessons/` | `W04 S051`, `W04 S053`, `ok` | 0 |
| P2 | + **mined** row S067 in `## Registry`, `used-by` → nonexistent `corpus/knowledge/nonexistent-r35.md` | `E11 S067 missing used-by corpus/knowledge/nonexistent-r35.md` | **1** |
| P3 | + **queued** row S067, same dangling `used-by` | `ok` — **no E11** | 0 |
| P4 | P3 copy + `corpus/knowledge/probe-dangling-sid.md` whose `source:` cites **S999** (no such row) | `ok` — **no finding** | 0 |
| P5 | row appended after the last section (outside `## Registry`) | `E12 S067 row outside Registry section` | 1 |
| P6 | `git archive HEAD` of the lane (66 rows, committed) | `W04 S051`, `W04 S053`, `ok` | 0 |

Reading of the probes (the operative calibration result):

1. **E11 is `mined`-only.** `scripts/sources-census.sh:560` skips every row whose status is not
   `mined` before testing `used-by` paths. P3: a **queued** row whose `used-by` names a file that
   does not exist is reported as `ok`/exit 0. The lane's own frozen census
   (`corpus/evidence/round25-sources-census.sh`) has the same shape (`s=="mined"` guard), so the
   two census implementations agree — but a *queued* registry row is never path-checked by either.
2. **The census is one-directional: registry → disk only.** P4: a knowledge file citing an
   **S-id that has no row** (`S999`) is invisible to `validate` (exit 0). There is no
   disk → registry check anywhere in `scripts/sources-census.sh`
   (`grep -n 'knowledge' scripts/sources-census.sh` → only fixture rows). Consequence for round 35:
   `chousa ok` / exit 0 is **compatible with** the round-35 notes
   `bash-local-expansion-r35.md` and `keyed-engine-output-equivalence-r35.md` having no registry
   row at all, and with `grep-pin-r35.md` being cited by S067/S068 while still being untracked.
   The census's "clean" verdict does not mean "every round-35 knowledge entry is registered".
3. **The census does not check the QUALITY criterion-6 metadata header.** 3 of the 44
   `corpus/knowledge/*.md` files have **no `source:` line at all** —
   `bash-local-expansion-r35.md`, `grep-pin-r35.md`, `keyed-engine-output-equivalence-r35.md`
   (plus the pre-existing `dead-zone-pcre-r34.md`). The lane's `round24-measure.sh` claim-2 check
   is hard-coded to three r24 entries (`corpus/evidence/round24-measure.sh:31`), so no instrument
   in the lane sweeps `corpus/knowledge/*` for the header. The census's exit 0 is silent on this.

## 6. Anchor re-verification of the two new rows (S067, S068)

Independently re-opened this round (read-only, no network):

- **S067** (`exec(3)`, tier A, mined): claims sha256 `2f1badd36afd699bbe4e62ff36d810a99ed5e2b4476747b168e33ba5ed1b1523`
  for `/usr/share/man/man3/exec.3.gz` — **matches** `sha256sum /usr/share/man/man3/exec.3.gz`.
  Claims anchor "decompressed lines 104–112, quote at 107–110" — **matches**: line 104 is
  `These functions duplicate the actions of the shell in`, 106 `if the specified filename does not
  contain a slash (/) character.`, 107–110 `The file is sought in the colon-separated list of
  directory pathnames / specified in the / .B PATH / environment variable.`
  The row's parenthetical "`execvp.3.gz` is a `.so man3/exec.3` shim" is **accurate**:
  `/usr/share/man/man3/execvp.3.gz` is 36 bytes and decompresses to `.so man3/exec.3`.
  `pacman -Qo /usr/share/man/man3/execvp.3.gz` → `man-pages 6.19-1` — matches the row.
- **S068** (`bash(1)`, tier A, mined): claims sha256 `b68beb3e385f7d8aead26bf7887c12f93ca769dcd528fd7282d70938b09bdffe`
  for `/usr/share/man/man1/bash.1.gz` — **matches** `sha256sum`. Claims anchor "decompressed lines
  388–404, quote at 391–395" — **matches**: 391–395 is `.B bash / is started non-interactively,
  to run a shell script, for example, it / looks for the variable / .SM / .B BASH_ENV`.
  `pacman -Qo /usr/share/man/man1/bash.1.gz` → `bash 5.3.20-1`; `bash --version` → `5.3.20(1)-release` — matches.

**One substantive scope/anchor mismatch found in S068** (the round's only new *external* row pair
is thus not fully closed):

- S068's `scope` cell reads *"non-interactive startup file (`BASH_ENV`) **and exported shell
  functions**"*; its `teaches` cell additionally claims *"the script's own later definition
  overrides it"*. The cited anchor (decompressed lines 388–404) contains **neither** the
  exported-functions text nor anything about definition precedence: `zcat bash.1.gz | sed -n
  '388,404p' | grep -c -i 'export\|function'` → **0**. The exported-functions passage is at
  decompressed lines **5297–5301** (`Functions may be exported so that child shell processes …
  automatically have them defined with the -f option to the export builtin`) — outside the cited
  range — and the "later definition overrides it" clause has no anchor in the cited page at all.
  By QUALITY criterion 7 (`corpus/QUALITY.md:23-25`: a source used outside its row's scope is an
  inference and labelled one) the second half of that scope/teaches text is an unlabelled
  inference. [INFERENCE — the scope mismatch is measured; the QUALITY reading is my reading of
  the criterion.]
  The BASH_ENV half of S068 is fully supported (the gate's `grep()` wrapper beating an imported
  `BASH_ENV` function is measured separately by the round-35 C1 counter's S2 scenario).

## 7. Verdict for this item

- **Assigned deliverable met.** Census exit code **0**, all output lines reproduced above; row
  count **66 → 68** (registry edited by the L1 mid-wave, hash recorded for both states); last five
  row ids **S064–S068**, all `tier=A` / `status=mined`; **yes**, S067 and S068's `used-by` names a
  round-35 artifact (`corpus/knowledge/grep-pin-r35.md`) — but **no row names any round-35
  *evidence* artifact**, and the round's other two knowledge notes have no registry row.
- **Registry census is clean but not discriminating for the round-35 gaps.** The census proves
  registry→disk path integrity for *mined* rows only (P2 vs P3) and has **no** reverse
  disk→registry check (P4), so "chousa ok, exit 0" is exactly what the lane would also print with
  two unregistered r35 notes and an untracked `grep-pin-r35.md` in the tree. Any future claim that
  "the registry covers round 35" needs a check the census does not provide.
- **New finding for the round record (S068):** cited anchor does not cover the second half of the
  row's own scope/teaches (exported shell functions; later-definition precedence). The exported-
  functions text exists in the same man page at decompressed lines 5297–5301.

## Limits / what I did not do

- I did not edit `corpus/SOURCES.md` or any other lane production file (read-only contract).
- I did not re-score C1 or C2, and did not run the round-35 counters — this seat's item is the
  census; other wave seats cover the claim predicates.
- `quote-reopen.py` was **not** run against S067/S068: both rows are local man pages, and the
  tool re-opens *web* sources against the registry URL (S067's URL was explicitly not fetched), so
  a `VERBATIM` verdict is not obtainable for them; I verified the anchors by hand instead, as
  recorded in §6.
- Fleet-wide `validate` and `census` were run read-only; no registry in any lane was modified.
- `census` mode's `status.rejected=4` / `queued=19` for chousa were taken from the fleet output
  and were not independently re-derived beyond `round24-measure.sh`'s identical counts.

## Artifacts (all inside `.ufo/waves/round-35/w2/ExecCensus/`, 8.0 KiB total)

- `census-receipt.txt` (sha256 `54f02aca6e7e16beb69bca6625866d116a63fc5f7f3d452f8f2392412881948b`)
- `probe-receipts.txt` (sha256 `8c84e65f974e94a05ad464a953d4a7b76d2399a27768991c471f5c67a150cd12`)
- scratch probe trees (P1–P6) under `/tmp/hyaku/chousa-r35/w2/ExecCensus/{probe2,probe5,probe6,head3}/`

No tools were installed this run.
