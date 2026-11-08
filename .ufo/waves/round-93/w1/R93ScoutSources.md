# R93ScoutSources — registry and cited-source reconnaissance, round 93 wave 1

**Seat:** R93ScoutSources (scout) · **Lane:** chousa · **Wave:** round-93 / w1
**Target tree:** carrier C2 `754b62fb6adc60e44e12375af5461a0ebe302994` (freeze F2 `b7241252c2358613d3b22b7d0454d98c56dab373`)
**Scratch:** `/fast/scratch/hyaku/chousa-r93/R93ScoutSources` (clone via `git clone --shared`, checked out at C2; removed before yield)
**Receipts:** `.ufo/waves/round-93/w1/R93ScoutSources/receipts/` (9 files, `01`–`09`)

No edits to production bytes. No lane/fleet git or jj mutation, no commits, no pushes, no subagents, no
agent://all. No network beyond re-opening the one item the seat names (S070's installed page, read from
disk; no GET, no fetch). Every command below names the receipt that carries its raw output and exit code.

---

## F1 — S070's premise re-opens byte-exact; the registry row's anchor and `teaches` cells match the installed page, and the two citation-precision defects carried from r91/r92 are unchanged at C2

**Command** — `sha256sum /usr/share/man/man1/sha256sum.1.gz` →
`93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f` (**exit 0**).
Receipt `01-s070-premise.txt`.

**MATCH, no drift.** The seat spec's expected digest is
`93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f`; the installed file hashes to exactly that.
The registry row S070 (`corpus/SOURCES.md:80`) records the same digest in its `anchor` cell
(`file SHA-256 \`93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f\` (opened locally 2026-10-23)`),
so the recorded premise and the host bytes agree. Installed package version confirmed
`pacman -Qi coreutils` → `Version: 9.12-2`, matching the row's `coreutils 9.12-2`.

**Command** — `zcat /usr/share/man/man1/sha256sum.1.gz | grep -n 'Print or check SHA256'` →
`11:Print or check SHA256 (256\-bit) checksums.` (**exit 0**). Receipt `01`.

**The exact line carrying the quote is decompressed line 11**, exactly as the row's anchor says
(`quote at line 11`). Every other anchor offset resolves to the line it claims: `sed -n '4p;5p;8p;11p;19p;20p;54p;55p;56p'`
→ 4 = `sha256sum \- compute and check SHA256 message digest`, 5 = `.SH SYNOPSIS`, 8 = `.SH DESCRIPTION`,
11 = the quote line, 19 = the `-c, --check` tty-link, 20 = `read checksums from the FILEs and check them`,
54 = `The sums are computed as described in FIPS\-180-2.`, 55 = `When checking, the input should be a former
output of this program.`, 56 = `The default mode is to print a line with: checksum, a space,`. Receipt `02`.

**Exact cell text.** S070 row (`corpus/SOURCES.md:80`), the two cells the seat names:

* `anchor` — ``NAME/DESCRIPTION and SYNOPSIS `-c, --check` (decompressed lines 4–11, 19–20, 54–56; quote at line 11); coreutils 9.12-2; file SHA-256 `93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f` (opened locally 2026-10-23)``
* `teaches` — ``` `sha256sum` prints or checks SHA256 (256-bit) checksums, and `--check` reads checksums from files rather than computing a policy. ```

Receipt `03-s070-registry-cells.txt` carries both cells verbatim plus S073's row and the SOURCES.md diff.

**F1a (carried from r92 F1a, unchanged) — the `anchor` cell's `SYNOPSIS` label is the label S073 exists to correct.**
S073 (`corpus/SOURCES.md:83`) carries `supersedes S070 —` in its anchor and states that "`-c, --check` is a
DESCRIPTION `.TP` item, not a SYNOPSIS line". My measurement agrees with S073: decompressed line 5 is
`.SH SYNOPSIS`, line 8 is `.SH DESCRIPTION`, and lines 19–20 (the `-c, --check` item) sit under DESCRIPTION.
So the C1 claim cites the row whose anchor label is known-wrong while the correcting row (S073) exists and is
`mined`. The quoted line 11 is under DESCRIPTION and is unaffected. **Citation-precision finding, not a kill-rule
firing** — the C1 rule rests on the digest text at line 11, which S070's own `teaches` cell states correctly.

**F1b (carried from r91/r92, unchanged) — the claim's quote is the rendered form, not a literal substring of the
source bytes.** `grep -c 'Print or check SHA256 (256-bit) checksums\.'` on the decompressed roff → **0 (exit 1)**;
the roff-escaped form `256\-bit` → **1 (exit 0)**. `od -c` of line 11 shows the hyphen as `\ -`. The rendered page
does carry the literal string: `man --nh --nj -P cat … | grep -n 'Print or check'` → `10:     Print or check SHA256
(256-bit) checksums.  Legacy interface to the` (**exit 0**). Receipt `02`. The r92 lesson (`:24`) calls the rendered
quote "**7 words**"; `printf '%s\n' 'Print or check SHA256 (256-bit) checksums.' | wc -w` → **6**. Receipt `02`.
The r93 frozen claim text does **not** repeat the word count (no `words=`/`7 words` string in
`.ufo/waves/round-93/claims.md` or `claims.json`), so only the carried lesson wording is affected.

**F1c — no committed round-93 re-open artifact for S070 exists at C2.** `git ls-tree -r 754b62fb --name-only |
grep -c 'corpus/lessons/round-93'` → **0**; the newest lesson at C2 is `corpus/lessons/round-92.md`. The only
GATE-RECORD lines naming S001 or S070 anywhere at C2 are in `corpus/lessons/round-91.md:14` and
`corpus/lessons/round-92.md:19` (S001 only, rev form). The frozen claim says S070 is "re-opened this round"
(`.ufo/waves/round-93/claims.md:62`, `claims.json` `C1.sources = ["S070"]`), but at the carrier there is no
round-93 lesson, no round-93 GATE-RECORD, and `corpus/SOURCES.md` is byte-identical base→C2
(`git diff --stat 206226dc..754b62fb -- corpus/SOURCES.md` → empty; sha256 of the working tree, of the C2 blob
and of the live lane tree all `7a2f6d53fe47ac9dc8c8931f8e21619862f0b919ecea0cd387e7f92544f5c1c1`).
Receipts `03`, `07`. **Expected shape for a wave-1 seat — the lesson lands with the integration, not at the carrier —
but it is the same artifact gap r91's scout named (F4) and r92's scout named (F1c); it is recorded, not resolved here.**

---

## F2 — S001: the tool line its Gate names is present byte-identical at base, F2 and C2, and the row's `recheck` cell names **neither** round 92 nor round 93 — it reads `on-release`

**Command** — `grep -n -E '^GATE-RECORD S001 ' corpus/lessons/round-92.md` (the committed rev-form record at C2) →
`19:GATE-RECORD S001 rev=7901eb238a8adc9b8d438dee7779140e28da6e62 path=tools/research-gate.sh line=9010 words=4 quote=RESEARCH_GATE_SELFTEST: PASS (%d cases%s)`. Receipt `05`.

**The tool line its Gate names is `tools/research-gate.sh` line 9010:**
`    printf 'RESEARCH_GATE_SELFTEST: PASS (%d cases%s)\n' "$cases" "${SKIPPED:+, $SKIPPED skipped}"`

It is **byte-identical at all three revisions** — base `206226dc`, freeze F2 `b7241252`, carrier C2 `754b62fb`
(three `git show … | sed -n '9010p'` commands, all printing the same line). Receipt `05`.

**The quote's word count is 4**, matching the record's `words=4`:
`printf '%s\n' 'RESEARCH_GATE_SELFTEST: PASS (%d cases%s)' | wc -w` → **4**.
**The record verifies mechanically:** `python3 tools/gate-records.py verify --root . --repo . corpus/lessons/round-92.md`
→ `GATE_RECORD corpus/lessons/round-92.md:19 S001 OK` / `GATE_RECORDS files=1 records=1 ok=1 fail=0` (**exit 0**).
Receipt `05`. (This is a read-only tool run against committed bytes; it writes nothing.)

**The `recheck` cell — the seat's question — names neither round 92 nor round 93.**

| revision | S001 `recheck` cell |
|---|---|
| base `206226dc9d9baef620e7d3d30bdac5f9194a459f` | `on-release` |
| freeze F2 `b7241252c2358613d3b22b7d0454d98c56dab373` | `on-release` |
| carrier C2 `754b62fb6adc60e44e12375af5461a0ebe302994` | `on-release` |

Receipt `05`. A full history sweep over **every** commit that touched `corpus/SOURCES.md` (89 commits) shows the
S001 `recheck` cell has held exactly one value in the lane's entire history: `on-release` (89 × `on-release`,
no other value). Receipts `05`, `08`.

**DRIFT against the frozen plan's premise.** `.ufo/waves/round-93/claims.md:173` states, under §Frontier step:
"`S001` (the own-work chain row; its `recheck` cell moves round 92 → round 93, logged old→new in the round-93
lesson)". The committed tree has no such "round 92" value to move from:

* **No row in the registry names a specific round in its `recheck` cell.** Sweeping all 219 rows: the complete
  set of `recheck` values is `180d`, `30d`, `365d`, `90d`, `on-release`, `on-round` — six distinct values, none
  round-numbered. The single round-naming cadence is **S148 `on-round`** (a symbolic cadence, not a round
  number). A filter for a value matching `round-?[0-9]+` returns **zero** rows. Receipts `05`, `08`.
* **The plan's "old→new" therefore has no committed "old".** If the L1 writes `round 93` into the cell, the
  `old→new` log the plan asks for must read **`on-release` → `round 93`**, not `round 92` → `round 93`. Writing
  `round 92 → round 93` into the round-93 lesson would name a value that has never existed in this registry.
* **The census accepts the new value but classifies it as a cadence, never overdue.** The census's E09 grammar
  accepts an ISO date, `NNd`, or a symbolic cadence (`/^[A-Za-z][A-Za-z0-9 _-]*$/`); `round 93` matches the
  symbolic form, so the cell stays census-valid, and `overdue` mode would report it as `cadence … recheck=round 93`,
  never overdue. Today S001 is reported as `chousa cadence S001 recheck=on-release opened=2026-10-19`.
  Receipts `06`, `08`.

**F2a — the claim's own wording for C2/C3 does not match what the S001 row records.** The two `**Sources.**` lines
read `S001` re-open (own-work chain row, tier A) — **the counter's leg vocabulary rule** (C2, `claims.md:111`) and
**the selftest verdict line the tally legs read** (C3, `claims.md:160`). Measured cells of the S001 row:

* `kind` = `own-work`, `tier` = `A` (matches the claim's description)
* `scope` = ``this lane's gate behavior at the round-24 landing revision (gate sha recorded once, in corpus/knowledge/json-delimiter-r24.md)``
* `anchor` = ``setup check "manifest unreadable", manifest-append block opening "A manifest whose last byte is not", and selftest cases 134-136 (json-unterminated-, json-nul-terminated-, json-unreadable-manifest) in tools/research-gate.sh; round-24 landing commit``
* `teaches` = ``An appending writer must terminate an unterminated last line before appending, or the JSONL glues two objects onto one invalid line``

Receipt `07`. Two observations, both citation-precision:

1. **The row is the JSONL manifest-append rule, not a leg-vocabulary rule.** Its `teaches` cell is about the
   append delimiter; the C2 leg vocabulary is pinned by `EXPECTED_LEGS = 15` inside the instrument itself
   (`corpus/evidence/round93/curation-r93.py:98`, with the "one record per leg" rule in its docstring) and by
   `corpus/QUALITY.md:1158`. No round-93 instrument names S001 (`grep -rn 'S001' corpus/evidence/round93/` → no
   output) and no QUALITY criterion names S001 (`grep -n 'S001' corpus/QUALITY.md` → no output). The row is a
   legitimate own-work chain row (the `## Paths` section names the chain at `corpus/SOURCES.md:246`:
   `Lane mechanics — S001 → S013`), and its scope/teaches do not state the C2 leg-vocabulary rule. **Finding, on
   the claims' attribution wording only.**
2. **The C3 attribution is sound on the bytes.** The C3 counter reads the rendered verdict line —
   `skill-tally-r93.py:34` `VERDICT_RE = re.compile(r"^RESEARCH_GATE_SELFTEST: PASS \((\d+) cases, (\d+) skipped\)$", re.M)`
   — and the committed selftest receipt carries `RESEARCH_GATE_SELFTEST: PASS (283 cases, 0 skipped)`
   (`corpus/evidence/round93/controls/selftest-r93.txt:285`). The Gate record's line 9010 is the printer of that
   line, so S001's re-open does ground what the claim says it grounds. Note the rendered form
   `(283 cases, 0 skipped)` differs from the printf template `(PASS (%d cases%s))` the Gate record quotes; both
   come from the same line 9010, and the record's `words=4` matches the template.

**Also measured for the S001 anchor (all resolve, at the revision the anchor names).** The anchor pins the r24
landing revision. At commit `6572827a` ("round-24: --json delimiter edge closed (cases 134–136)"):
`manifest unreadable` at gate line 2376, `# A manifest whose last byte is not '\n'` at line 2490, and the committed
r24 selftest log `corpus/evidence/json-r24-20261019T213117Z-selftest.log` carries
`ok-case 134 json-unterminated-manifest` / `135 json-nul-terminated-manifest` / `136 json-unreadable-manifest` —
the anchor's "selftest cases 134-136" is exact at that revision. The gate sha at `6572827a` is
`752e4e382ed77c06ac5030ce2179c7ca524934f86fd2a6b25ef946ab027ac553`, matching the `752e4e38…` recorded in
`corpus/knowledge/json-delimiter-r24.md` (the row's scope cell says the gate sha is recorded once, there).
Receipt `09-s001-anchor-at-r24-landing.txt`. **No drift in the anchor.**

---

## F3 — the six sources the two routed entries cite: `status=mined` and `used-by` naming the citing entry as an exact token — no drift on any of the six

Re-derived with an independent parser and the counter's own tokeniser
(`re.split(r'[^A-Za-z0-9._/-]+', used_by)`), over the C2 blob. Receipt `04-six-routed-sources-usedby.txt`.

| source | `status` | `used-by` cell (exact) | cites entry |
|---|---|---|---|
| S214 | `mined` | `corpus/knowledge/search-transparency-reporting-r84.md` | r84 ✓ (Q1–Q5) |
| S018 | `mined` | `corpus/knowledge/search-transparency-reporting-r84.md` | r84 ✓ (Q6–Q8) |
| S023 | `mined` | `corpus/knowledge/search-transparency-reporting-r84.md` | r84 ✓ (Q9–Q13) |
| S215 | `mined` | `corpus/knowledge/provenance-recording-r85.md` | r85 ✓ (Q1–Q4) |
| S026 | `mined` | `corpus/knowledge/provenance-recording-r85.md` | r85 ✓ (Q5–Q6) |
| S031 | `mined` | `corpus/knowledge/provenance-recording-r85.md` | r85 ✓ (Q7) |

**No drift.** Each `used-by` cell holds exactly one token and that token is the citing entry's full repo path —
the basename is not a separate token, so the match is exact under the counter's split. **Two-sided sweep over all
219 registry rows:** exactly these six mined rows token-join to either routed entry; **zero** mined-and-named-but-uncited
rows; **zero** substring-only mentions anywhere in the registry. The source id sets in each entry's
`## Located quotes` table are exactly `{S018, S023, S214}` and `{S026, S031, S215}` — no id cited by an entry is
missing from the registry, and no registry row naming an entry escapes it. **Capture presence:** S214 →
`a640b15abf781e5c583d7088`, S018 → `248b43277f376e437a356909`, S023 → `f5545a194c06ab421875b047`,
S215 → `6e48bcc4a04d13b7b3ebb68e`, S026 → `67983a3dbbd1d690aa648744`, and S031 → `11d6cc56bb24adfc61eea2b4`
(each present as `.txt` and `.raw` under `corpus/captures/`; S031's key appears in
`corpus/evidence/round57/refetch.tsv` rather than in its registry row, which is consistent with the row's own text).
Receipt `04`.

**Corroboration from the frozen counter on the C2 bytes:** `python3 -B corpus/evidence/round93/curation-r93.py --root .`
→ `SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 … LEGS_MEASURED=15/15` and `CURATION_R93=PASS` (**exit 0**).
This is a read-only counter run against the clone's committed bytes; it is a supporting datapoint, not a C2 verdict
(the C2 mandate sits with the executor/reviewer seats). It is recorded here because it is the mechanism the six
rows feed.

---

## F4 — census is clean at exit 0 with the same five `W04` warnings; the seat spec's row-count grep matches nothing, and the resolved registry row count is 219

**Command** — `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`
→ **exit 0**, five `W04` warnings and `chousa ok /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md`:

```
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

**The five `W04` warnings, listed.** Identical to the five recorded at round start and at the round-92 census
(`corpus/lessons/round-92.md:33`, `corpus/lessons/round-91-verifier-spotcheck.md`). `W04` is a warning code; the
census's own contract says W-codes never change status, and the run's exit code is 0.

**Row count.** The seat spec's `grep -cE '^ (0, 3)\|[[:space:]]*S[0-9](3,)' corpus/SOURCES.md` prints **0 with
exit 1** — the pattern is a literal alternation on `" (0, 3)|"` / `"S<digit>(3,)"` and does not match this
registry's shape (`| S214 | … |`); it is a malformed expression, not a count of zero rows. Resolved three ways
(receipt `06`): `grep -cE '^[[:space:]]*\| S[0-9]{3,} '` → **219**; `grep -oE '^\| S[0-9]{3} ' | sort -u | wc -l`
→ **219** unique ids; the census's own `census` mode → `chousa rows 219` (tier.A 140 / tier.B 59 / tier.C 20;
mined 183 / queued 12 / rejected 24). `awk -F'|' 'NF==13' | wc -l` → 221 (the 219 data rows plus the header and
separator rows, which are also 11-cell). **The registry holds 219 rows**, matching the census recorded in the
frozen claims (`claims.md:4-6`, "registry 219 rows").

**The census was run against the live lane tree; that tree's `corpus/SOURCES.md` is byte-identical to the C2 blob**
(sha256 `7a2f6d53fe47ac9dc8c8931f8e21619862f0b919ecea0cd387e7f92544f5c1c1` for the working tree, for
`git show 754b62fb:corpus/SOURCES.md`, and for the live lane file), so the result is the tree's, not a
working-directory artefact. Receipts `06`, `03`.

**Census view of the rows this seat re-opened** (`overdue` mode, `--today 2026-11-08`):
`S001 recheck=on-release opened=2026-10-19`, `S070 recheck=on-release opened=2026-10-23`,
`S018 recheck=365d`, `S023 recheck=365d`, `S026 recheck=180d`, `S031 recheck=365d`,
`S214 recheck=on-release`, `S215 recheck=365d` — all reported as `cadence` (symbolic/`NNd`, never overdue).
Receipt `06`.

---

## What I did not touch (stated so it is not read as covered)

* **C1's predicate** — I did not run `control-driver-r93.py verify` or `forgeries-r93.py`; the C1 mandate sits
  with the executor/reviewer seats. My C1 work is the S070 surface only.
* **C2's controls and C3's counter/controls** — not run. The one counter run I did make
  (`curation-r93.py --root .`, CURATION_R93=PASS) is a supporting datapoint for F3, not a C2 verdict.
* **The `## Gates` scope, the case-range pins and the tally derivation** — outside this seat's surfaces.
* **`tools/research-gate.sh`, `tools/gate-records.py`, `SKILL.md`** — read only; `tools/gate-records.py verify`
  was run read-only against committed bytes and writes nothing.
* **The pins table and the six receipts** — not this seat's surface (other seats own them).

## Tools

None installed or upgraded. `/home/vgpnk/.omp/agent/RULES.md` read first; the pacman guard is honoured — the only
`pacman` use was the read-only `pacman -Qi coreutils` (version query, no transaction). No `sudo`, no sysctl, no
service restart, no network (S070 was re-opened from the already-installed page on disk; no fetch, no GET).

## Scratch

`/fast/scratch/hyaku/chousa-r93/R93ScoutSources` (clone + `receipts/`) — removed with `rm -rf` after the receipts
were copied into `.ufo/waves/round-93/w1/R93ScoutSources/receipts/`.

---

VERDICT: R93ScoutSources C1 fired — S070's premise re-opens byte-exact (installed sha256 `93c17dff…403f` matches the row, decompressed line 11 carries the quote and every anchor offset resolves), but the claim cites the row whose `SYNOPSIS` anchor label S073 exists to correct, quotes the rendered rather than the literal source form, and the carrier carries no committed round-93 re-open artifact for S070 — citation-precision findings on this seat's surfaces, not a kill-rule firing.
VERDICT: R93ScoutSources C2 held — all six sources the two routed entries cite are `mined` with `used-by` naming the citing entry as an exact token (zero substring-only mentions, zero mined-but-uncited rows, all captures present) and the frozen counter reads `SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20` on the C2 bytes, though the claim's C2 attribution wording names S001 for a leg-vocabulary rule the row does not state.
VERDICT: R93ScoutSources C3 held — S001's Gate record verifies mechanically (`GATE_RECORD … S001 OK`, exit 0) against a `tools/research-gate.sh:9010` line byte-identical at base, F2 and C2 that prints the rendered verdict line the C3 counter's regex reads, and the committed selftest receipt carries `PASS (283 cases, 0 skipped)`; the one defect is that the frozen plan's "`recheck` cell moves round 92 → round 93" names a `round 92` value this registry has never held (S001's cell has read `on-release` in all 89 commits that touched `corpus/SOURCES.md`).
