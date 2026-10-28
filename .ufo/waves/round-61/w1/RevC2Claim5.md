# RevC2Claim5 — entailment review of Claim 5, `corpus/evidence/round61/controls/c2-positive-entry.md`

Seat RevC2Claim5 (reviewer, leaf, no dispatch). Read-only on the lane; scratch `/fast/scratch/hyaku/chousa-r61/RevC2Claim5/` (removed before yield). No install, no network, no git mutation (read-only `git show` / `cat-file` / `log`).

## Claim 5 as written (entry line 29-ish, "Claim 5.")

> In the round-55 fixture runs the builder removed a victim file and created another inside a symlinked victim directory, and truncated two victim files through links, each time exiting 0. [Q7, Q8]

## 1. Quotes re-opened in full context

Rendered with `MANWIDTH=1000 man -l /usr/share/man/man2/open.2.gz | col -bx` and `... rename.2.gz` (man-pages 6.19, 2026-02-08). Q1-Q6 are present in the rendered pages (not Claim 5's subject; checked only for the quote-present rule).

S136 (`.ufo/waves/round-56/w1/R55W2SentBuilder.md`, lines 11-12 table, lines 33-34 code block, lines 25-31 section 1):

- Q7 (line 33, under `## 1. --out is trusted; spans/ and span files are not checked for links`): `# h2     victim/S404-9.txt(28) before → absent after; victim/S001-1.txt(457) created; exit 0, stderr empty`. Table row h2 (line 11): `| h2 | out/spans symlink → dir | 0 | … | unlink + create in the link target |`.
- Q8 (line 34, same section): `# h3     victim/IMPORTANT.txt 10→457 B, victim/LEDGER.tsv 74→243 B (both targets truncated); exit 0`. Table row h3 (line 12): `| h3 | span file and spans.tsv are symlinks | 0 | … | truncated both link targets |`.

Both quotes are present verbatim (checked by reading lines 33-34) and both sit in section 1, whose opening sentence is about exactly this hazard, so no out-of-context problem with the removal/creation/exit-0 facts.

## 2. Mechanism cross-check (code read, not a fixture run)

- Current `tools/build-spans.py` sha256 prefix `1ed2650a…` equals the round-55 blob `29cfb12:tools/build-spans.py` (`git -C <lane> show 29cfb12…:tools/build-spans.py`, sha `1ed2650a…`). So the code S136 attacked is the code the lane still holds.
- Lines 201-208 of that blob: `sd = out / "spans"`; `sd.mkdir(parents=True, exist_ok=True)`; `for p in sd.iterdir(): if SPAN_RE.match(p.name) and ... : p.unlink()` (203-205); `(out / "spans.tsv").write_bytes(...)` (206); `(out / name).write_bytes(...)` (208). Nothing checks `is_symlink()`.
- So with `out/spans` → `victim/`, `iterdir` lists victim's files and `unlink` removes `S###-N.txt` names there, and `write_bytes` creates in the target: matches Q7. With `spans.tsv` → victim file, `write_bytes` opens `wb` (O_TRUNC, follows links) and rewrites the target: matches Q8.
- INFERENCE: the observed exit 0 and byte counts are as S136 reports them. I did not re-run the fixtures (S136's scratch was removed at its exit and no captured run output is committed; the quotes are transcribed comment lines). The mechanism is consistent with the code; the numbers are not independently reproduced this round.

## 3. Verdict analysis

Supported parts:
- "removed a victim file" — Q7 `victim/S404-9.txt(28) before → absent after`. Supported.
- "created another" — Q7 `victim/S001-1.txt(457) created`. Supported.
- "truncated two victim files through links" — Q8 `(both targets truncated)`, table row h3 "truncated both link targets", link context "span file and spans.tsv are symlinks". Supported as the source's own wording.
- "each time exiting 0" — Q7 and Q8 both end `exit 0`; table column 0 for h2 and h3. Supported.
- Scope "round-55 fixture runs" — matches S136 (round-55 builder, blob 29cfb12). Not an overreach.

Misread parts:
1. **Which object is the symlink.** The claim says "inside a symlinked victim directory". S136 says the symlink is `out/spans` and the victim directory is its *target* (table h2: "`out/spans` symlink → dir"; "unlink + create in the link target"). The victim directory itself is not a symlink. The claim attributes the link to the wrong object. This is a misreading of the context row, and it is the only part of the claim that describes the mechanism.
2. **"truncated" for an overwrite.** Q8's byte counts grow (10→457 B, 74→243 B). The file is opened with O_TRUNC and rewritten (`write_bytes`), so the observable result is an overwrite with new content, not a truncation. The claim echoes the source's word; a reader comparing the claim to the sizes would be misled. Wording precision, not a factual error in the quote.
3. **Victim-name mapping (not claimed; a trap for rewrites).** S136 does not say which victim name is the span file and which is `spans.tsv` in h3 (table only says "span file and spans.tsv are symlinks"). Any rewrite must not bind IMPORTANT.txt or LEDGER.tsv to a role.

Not overreach: nothing in Claim 5 goes beyond Q7/Q8 and their row context in generality (it names the round, the two cases and exit codes; it does not extend to other builders or to "all runs").

Calibration note (not a verdict input): Claim 5's sourcing is a lane seat's own run transcription, not a primary source and not re-run this round. The entry's Limits section does not say so. The claim is evidence about this builder, not about derived-output safety in general; the entry's Limits should carry "reported by S136 seat; not re-run in round 61".

Verdict for Claim 5: **misread** (the symlink attribution is wrong; the "truncated" wording contradicts the quoted sizes). The core facts (removal, creation, writes through links, exit 0) are supported by Q7/Q8 in context.

## 4. Proposed rewrite (Claim 5)

> Claim 5. In the round-55 fixture runs the builder exited 0 in both cases where a symbolic link redirected its writes. Case h2 (`out/spans` a symbolic link to a victim directory): it removed `victim/S404-9.txt` and created `victim/S001-1.txt` in the link target. Case h3 (the span file and `spans.tsv` were symbolic links): it overwrote both link targets, `victim/IMPORTANT.txt` 10→457 B and `victim/LEDGER.tsv` 74→243 B. [Q7, Q8]

Rewrite notes: no victim name is bound to a role in h3; "overwrote" replaces "truncated" (sizes grew); the symlink is named as `out/spans`, not as the victim directory. Add to the entry's Limits: "Claim 5 reports a lane seat's fixture runs (S136); the runs were not repeated in round 61; the mechanism was checked against the code at blob 29cfb12 only."

## 5. Out-of-scope observations (noted, not verdicts; for L1)

Read while checking the quotes. Not part of CLAIM5.
- Claim 4 ("so a failed run can leave the temporary name behind and cleanup belongs on the error path"): the quoted rename(2) text (Q5, Q6) describes a window in which both names refer to the same file; it says nothing about failed runs leaving temp names. The temp-name conclusion is INFERENCE and should be marked as such or dropped.
- Claim 2 ("so a fresh temporary name cannot be written through a planted link"): Q3 is conditioned on "When these two flags are specified" (O_CREAT with O_EXCL, rendered line 123); the claim's conclusion about temporary names is a reasonable inference, not a quote. Mark it.

## Install and cleanup record

No installs. Scratch created and removed (`rm -rf /fast/scratch/hyaku/chousa-r61/RevC2Claim5`). No writes outside this report.

Commands and outputs (abridged):
- `MANWIDTH=1000 man -l /usr/share/man/man2/open.2.gz | col -bx` → 516 lines; Q1-Q3 located at O_NOFOLLOW and O_EXCL paragraphs.
- `MANWIDTH=1000 man -l /usr/share/man/man2/rename.2.gz | col -bx` → 210 lines; Q4-Q6 at lines 38 and 46 (DESCRIPTION).
- `sed -n 1,40p`, `sed -n 85,120p` of S136 → table rows 11-12, quotes 33-34, section-1 context lines 25-31.
- `git -C <lane> show 29cfb12abd70f688b48c0d17f31e636f2d81104a:tools/build-spans.py` → sha256 `1ed2650a…`; lines 201-208 as cited.
- `sha256sum tools/build-spans.py` → `1ed2650a…` (same file).

VERDICT: CLAIM5=misread rewrite_needed=yes
