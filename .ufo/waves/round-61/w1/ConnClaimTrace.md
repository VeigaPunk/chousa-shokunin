# ConnClaimTrace — cross-claim trace of the R55W2SentBuilder hazards (round 61, w1)

Seat ConnClaimTrace (connector, leaf, no dispatch). Read-only on the lane; no lane file, git index or
tools/ edited. One probe run of the reference builder (scratch `/fast/scratch/hyaku/chousa-r61/ConnClaimTrace`,
removed). No network. No install.

## Findings

1. **Only 2 of 16 hazards are traced end to end** (leg + reference guard + entry claim): h2 (symlinked
   `spans/`) and h3 (symlinked span file / `spans.tsv`). Both are explained by the write-side link claims of the
   positive entry (`controls/c2-positive-entry.md`, Claims 1–3, 5).
2. **The entry explains link writes only.** Read-side reads (h5d), memory (h4, h5e/f, h4e, h6), input parsing
   (h7), exit codes (h8, h9), `--out` clobber (h1), and the pycache write (trace) have no entry claim. The
   counter's named limits (ii)–(iv) disclose some gaps but explain none of the mechanisms. [Strict count;
   see §5 for the lenient count.]
3. **Memory guard is not measured.** Reference `_read` caps the on-disk size (L140, 64 MiB) and `MAX_FORM`
   is checked only after the form exists (L150). The H20 predicate (`c1-count.py:562`) is
   `rc != 0 and not timeout and clean_out` — it reads RSS into the detail string but not into the verdict.
   Probe A (below): a docx whose text form is 256 MiB (261 515 B on disk) is refused with exit 1, leaves
   no output, and peaks at **803 MiB**. By reading the predicate, H20 would score this input PASS
   [INFERENCE: this probe did not run the counter's own fixture]. The counter's H14/H15 do gate RSS
   (`:482`, limit 96 MiB), so this is a leg-specific blind spot.
4. **Reference guard missing for U+2028.** `ref-build-spans.py:159` still uses `str.splitlines()`. Probe B:
   a quote containing U+2028 exits 2 with `need 4 non-empty tab cells, got 3` (and a second spurious line),
   nothing written. Output-safe, but the diagnosis the transcript flagged (§6) is still wrong. No leg covers it.
5. **Two legs do not discriminate.** H18 (FIFO) and H19 (ENTRYDOT) pass at base (`controls/c1-before.txt`:
   `H18 FIFO pass rc=1`, `H19 ENTRYDOT pass rc=2`). H18 checks only no-hang/no-write, not the false receipt
   the transcript flagged (§3). H19 covers `../x` only; `/etc/…` and `a/../b` have no leg.
6. **Entry is not landed.** `corpus/knowledge/derived-output-safety-r61.md` is absent (`ls`: no such file).
   The explanation column below is traced to the positive control `controls/c2-positive-entry.md`. Re-trace when
   the landed entry exists.

## 1. Trace table (hazards = the transcript's measured cases; 16 rows)

Legs: `c1-count.py` leg; base result from `controls/c1-before.txt` (seed 61001). Guard: line in
`controls/ref-build-spans.py`. Entry: `controls/c2-positive-entry.md` Claim n / Limit, or the counter's named limits
(`claims.md`, C1 limits (i)–(iv)). Status: FULL = leg ✓ and guard ✓ and entry/limit explains the mechanism.

| # | Hazard (R55W2SentBuilder case) | (a) counter leg [base] | (b) reference guard | (c) entry claim / limit | Status |
|---|---|---|---|---|---|
| 1 | h1 `--out` holds another round's spans; 19 committed spans + manifest destroyed, exit 0 | H07 FOREIGN [FAIL]; H09 ORPHAN [FAIL] | `guard_out` L273–276: differs/orphans → refuse unless `--replace` ✓ | none | OPEN: no explanation |
| 2 | h2 `out/spans` symlink → dir; writes and unlinks in the link target | H10 SPANSLINK [FAIL] | `guard_out` L259–261 refuses symlinked `spans/` ✓ | Claim 1 (O_NOFOLLOW ignores earlier components), Claim 5 / Q7; Limit TOCTOU | **FULL** |
| 3 | h3 span file and `spans.tsv` symlinks; both targets truncated | H11 FILELINK [FAIL]; H12 TSVLINK [FAIL] | L262–263 (tsv), L269–270 (span files); tmp via `O_EXCL\|O_NOFOLLOW`, `os.replace` L280–292 ✓ | Claim 2 (O_EXCL), Claim 3 (rename replaces link), Claim 5 / Q8 | **FULL** |
| 4 | h4a/b docx bomb: 64 MiB / 250 MiB form, 197 / 759 MiB RSS | H20 BIGFORM [FAIL]: refusal + no timeout + empty out; RSS not in predicate (`:562`) | `_read` L140 caps on-disk size only; `MAX_FORM` L150 runs after materialising. **Probe A: 803 MiB peak, refused** | none (limit (ii) calls the 64 MiB cap a choice) | GAP: leg blind to memory; guard refuses after the cost |
| 5 | h4e six URLs × 250 MiB form, 2008 MiB, 20 s | none (limit (iii): "one 192 MiB read, not the sum") | `self.memo[url] = res` L131 keeps every form; no aggregate bound | limit (iii) names the gap | GAP: no leg, no guard |
| 6 | h5e/f `.txt` 1 GiB (3.1 GiB peak); `.raw` 1.5 GiB OLE (1.8 GiB) | H14 BIGTXT [FAIL]; H15 BIGRAW [FAIL] (RSS < 96 MiB in predicate `:482`) | size `stat` before read: `_read` L140–143 ✓ | limit (ii): cap value only; mechanism (read before cap) not stated | PARTIAL: cap-value explanation only |
| 7 | h5a `.txt` FIFO (receipt false: `is_file()` skips it) | H18 FIFO [**PASS at base**] | `_probe` `S_ISREG` L103–104 ✓ | none | GAP: no explanation; leg non-discriminating |
| 8 | h5b/c `.txt` / `.raw` → `/dev/zero` | none device-specific (H13 uses a regular outside file; H18 a FIFO) | `_probe` realpath + `commonpath` L96–98 refuses [INFERENCE: not run] | none | GAP: no leg, no explanation |
| 9 | h5d `.txt` symlink → file outside cache; its bytes and digest enter the manifest | H13 OUTSIDE [FAIL] ✓ | L96–98 `resolves outside the cache` ✓ | none (entry covers write-side links only) | OPEN: no explanation |
| 10 | h6a/b 100 000 rows: 31.5 s, 100 000 files | none (limit (iv): "not a leg") | none: no row cap; two scans per row L195–199 | limit (iv) names it | GAP: no leg, no guard |
| 11 | h7a–d entry `../..`, `/etc/…`, `a/../b`, `..hidden/x` | H19 ENTRYDOT [**PASS at base**]: `../x` only | `read_quotes` L176 refuses `/`-prefix and `..` parts ✓ | none (transcript §6: "defence in depth") | PARTIAL: `/etc`, `a/../b` untested; no explanation |
| 12 | h7e/f quote with U+2028: row misreported | none | **none**: `splitlines()` L159 still in place. **Probe B: exit 2, misdiagnosed, nothing written** | none | GAP: no leg, no guard, no explanation |
| 13 | h8 `--out` is a regular file → traceback, exit 1 | H16 OUTFILE [FAIL] | `guard_out` L257–258 → exit 2 ✓ | none | OPEN: no explanation |
| 14 | h9 / h9b unreadable capture → traceback | H17 UNREADABLE [FAIL] | `_read` L144–145 → refused, exit 1 ✓ | none | OPEN: no explanation |
| 15 | h11 `spans.tsv` is a directory: orphan already unlinked, then `IsADirectoryError` | none (H07 = a file; H12 = a symlink) | `guard_out` L262–263 refuses before any unlink; orphan unlink last L305–306 [INFERENCE: not run] | Claim 4 covers temp names left on failure, not orphan order | GAP: no leg; partial explanation |
| 16 | trace: `tools/__pycache__/capture-text…pyc` written on zip/OLE runs | P03 NOPYC [FAIL] | `_capture_text` sets `dont_write_bytecode` L76–84 ✓ | none | OPEN: no explanation |

Transcript labels: there is no `h10` in `R55W2SentBuilder.md`. The labels run h9, h9b, h11; row 10 is the h6 group.

## 2. Gaps, by kind

- **No leg:** rows 5, 8, 10, 12, 15 (row 4 memory, row 11 `/etc` and `a/../b` are partial; row 7 is non-discriminating).
- **No guard:** rows 5, 10, 12. Row 4 refuses only after the memory cost is paid (Probe A).
- **No explanation (entry or limit):** rows 1, 4, 7, 8, 9, 11, 12, 13, 14, 16. Rows 5, 10 are explained by a limit
  that names the gap but not a mechanism; rows 6, 15 partially.
- **Measured but not gated:** row 4's RSS (H20 predicate). Row 7's false receipt.

## 3. Probes (reference builder, `controls/ref-build-spans.py`, one run each, host MemAvailable 15.1 GB)

- **Probe A (row 4, h4b-class):** zip `word/document.xml` with a 256 MiB `w:t`, deflated to 261 515 B on disk.
  `python3 -B tools/build-spans.py --quotes qa.tsv --out out-a --cache cache` →
  `rc 1, maxrss 803 MiB, out absent`, stderr `refused S001: capture-text refused …: 'word/document.xml' inflates to
  268435768 bytes (limit 268435456)`. The refusal came from `capture-text.py`'s inflate cap, not `MAX_FORM`.
- **Probe B (row 12, U+2028):** cache `.txt` "alpha beta one\u2028two gamma delta", quote `one\u2028two`. →
  `rc 2, out absent`, stderr `… line 2: need 4 non-empty tab cells, got 3` and `… line 3: need 4 non-empty tab cells, got 2`.
- Quote check: entry Q7 and Q8 match the transcript text verbatim (`str in` → True, True).
- Reference `read_quotes` (L159) and counter H20 (L562) read from the files; not executed beyond the probes.

## 4. Counter legs with base results (`controls/c1-before.txt`, seed 61001, verbatim)

`P03 fail`, `H07–H17 fail` (H08 rc=2, H09 rc=0, H10–H13 victim changed or leaked, H14 rss 412 980 KiB, H15 rc=1 rss
414 768, H16/H17 traceback), `H18 pass rc=1`, `H19 pass rc=2`, `H20 fail rc=0 rss 220 412 KiB`. Result: `LEGS=7/20 C1=FAIL`.
Reference (`controls/c1-reference.txt`): `LEGS=20/20 C1=PASS` at seeds 61001–61003. Counters were not re-run here.

## 5. Calibration

- Strict count (leg ✓ and guard ✓ and mechanism explained): **2/16** (rows 2, 3).
- Lenient count (limit (ii) accepted as explaining the cap, row 6): **3/16**. Rows 4, 5, 10 remain non-FULL because
  they lack a leg or guard.
- Routed, not refuted: the H20 RSS gap and the H18/H19 non-discrimination are counter limits, per `claims.md`
  ("a wave seat's demonstration that a hazard class outside the 20 legs still reaches the landed builder is routed
  as a counter limit"). The counter is frozen; these were not edited.
- Not claimed: the reference's TOCTOU (limit (i)), DIR-as-symlink (not in the transcript), or any row not in the
  transcript.

## 6. Installs

None.

VERDICT: HAZARDS_FULLY_TRACED=2/16
