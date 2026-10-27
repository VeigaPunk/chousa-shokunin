# R54 C1 counter review — operability

## Findings (severity order)

### High — audit hook does not enforce the claimed no-spawn boundary

`HOOK`'s `BAD` tuple in `corpus/evidence/round54/c1-count.py` covers Python audit events such as `subprocess.Popen` and `os.system`, but ctypes calls into libc bypass those events. Repro under the same hook: `python3 /fast/scratch/hyaku/chousa-r54/R54ReviewC1Counter/hook_one.py ctypes.system` printed `ctypes.system: NOT BLOCKED (audit hook did not fire)`; `ctypes.fork` likewise printed `NOT BLOCKED`.

A stronger counterexample, M15, retained the candidate's CFB/FIB validation and docx path but obtained OLE text by `ctypes.CDLL("libc.so.6").system("soffice ...")`. Command:

```sh
python3 corpus/evidence/round54/c1-count.py --seed 7 --per-leg 2 --tool /fast/scratch/hyaku/chousa-r54/R54ReviewC1Counter/mutants/m15_forge_shell.py --work /fast/scratch/hyaku/chousa-r54/R54ReviewC1Counter/w-m15
```

Observed: `GEN=PASS 2 docs`, `NONWORD=PASS 2 sheets`, `ENCRYPTED=PASS 2 docs`, `MALFORMED=PASS 2 docs`, `REAL=PASS 5 captures`, `REGRESS=PASS r52 ['LEGS=9/9'] ['SUPPLEMENT_LEGS=4/4']`, `LEGS=6/6`, `C1=PASS`. Thus a tool that actually shells to LibreOffice passes the frozen counter, contradicting the predicate's “fails the run on any process spawn” clause and the round-53 closure assertion that a LibreOffice sheller is refused. The existing SHELL control only exercises `subprocess.Popen`, which the hook catches.

### High — ENCRYPTED never tests fObfuscated without fEncrypted

`leg_encrypted` sets `b[o + 0x0B] |= 0x01` or `0x81` (line 218). With the FIB flags word at stream offset `0x0A`, byte `0x0B` bit 0 is `fEncrypted` (`0x0100`) and bit 7 is `fObfuscated` (`0x8000`): these mutations are fEncrypted-only or both flags, never fObfuscated-only. But R54-C1 requires refusal when `fEncrypted or fObfuscated` is set. A mutant that removed the tool's `flags & 0x8000` check therefore still passes:

```sh
python3 corpus/evidence/round54/c1-count.py --seed 7 --per-leg 2 --tool /fast/scratch/hyaku/chousa-r54/R54ReviewC1Counter/mutants/m1_noobf.py --work /fast/scratch/hyaku/chousa-r54/R54ReviewC1Counter/w-m1_noobf
```

Observed: `ENCRYPTED=PASS 2 docs`, `LEGS=6/6`, `C1=PASS`. The counter cannot detect a regression that ignores fObfuscated-only documents.

### High — GEN does not check hyperlink-anchor multiplicity independently

`gen_docs` appends `pre + " " + anchor + " " + post` as one `items` entry (lines 123–131); `leg_gen` counts that combined string, but never the anchor itself. M2b duplicated the field result at the end of the OLE text form. Direct probe output: native anchor count in whitespace-free stdout `1`; M2b anchor count `2`, while the combined paragraph item count remained `1`. Yet the full counter returned `GEN=PASS 2 docs`, `LEGS=6/6`, `C1=PASS` for M2b. This violates the frozen predicate's explicit “hyperlink-anchor text ... appears exactly once” clause.

```sh
python3 corpus/evidence/round54/c1-count.py --seed 7 --per-leg 2 --tool /fast/scratch/hyaku/chousa-r54/R54ReviewC1Counter/mutants/m2b_dupanchor.py --work /fast/scratch/hyaku/chousa-r54/R54ReviewC1Counter/w-m2b_dupanchor
```

### Medium — REAL pinned-quote uniqueness is tool-self-reported

GEN independently checks `text.count(q) == 1`; REAL does not. In `leg_real`, the pinned-quote branch requires a tool-produced `LOCATED count=1` and checks only `text[offset:].startswith(quote)`. It never checks `text.count(PINNED_QUOTES[k]) == 1`. Therefore a tool that reports count 1 while a pinned quote occurs twice can pass that REAL subcheck; the quote count is not independently measured as it is in GEN.

### Low — `wd_start` is a fail-closed file-byte heuristic, not a CFB stream lookup

`wd_start` scans the entire file at 512-byte offsets for `EC A5` plus `nFib >= 0xC1`, and accepts only one hit. All inspected generated docs had one hit at 5120; all five pinned captures also had one hit (at 512 or 103424). However a WordDocument stream in the CFB mini stream (below the 4096-byte cutoff) need not start at a 512-byte file offset; a missing or ambiguous hit makes ENCRYPTED/MALFORMED print `ENV_CHANGED` and abort the whole counter with exit 2. This is fail-closed, but it labels an input-layout/heuristic failure as environment change.

## Asked checks / verified behavior

- **GEN order / short-substring question:** `flat.count(w) == 1` is checked before `find`; `find` is therefore unambiguous, and `j < pos` enforces increasing, non-overlapping order. A repeated item (or a short item occurring both standalone and inside another item) fails rather than passing. The generator's sentences/cells include a random `nx` plus ten-hex suffix, making accidental substring collisions unlikely. The separate anchor omission above is the actual gap.
- **Hyperlink URL is a live test, not vacuous:** generated `<a href>` HTML converts to a real field. Piece dump from `gen_dump.py -- seed 7` showed: `...<0013> HYPERLINK "https://ucwiqlfl.example/u388853933633"<0001><0014>ýêzzzzgä men víd nx3043b026c4<0015>...`. Thus the URL is in the field-code region (0x13–0x14) and the anchor is the result. M17 appended the URL to otherwise valid output and GEN failed with `field code (hyperlink URL) in the text form`; the URL check is live.
- **`--locate`:** GEN independently checks the reported offset against the plain-run stdout and checks `text.count(q) == 1`, but `q` is only a 2/3 prefix of a selected item, not the whole paragraph. REAL pinned quotes do not get that independent count check (finding above).
- **MALFORMED truncation:** exhaustive sweep of the generated seed-11 doc over every cut from 513 through 5120 bytes observed `REFUSED ole-malformed` for all 4608 cuts. Sector-shift mutation writes 7 to CFB header offset 0x1E (sector shift), which the tool rejects as `ole-malformed`.
- **`refused()`:** checks rc 2, empty stdout, no `Traceback` in stderr, and a stderr line prefixed by the expected refusal class; this matches the frozen refusal contract.
- **REAL label/ratio:** ratio code matches the 0.90–1.10 rule. The fallback regex drops any first whitespace-delimited token of 1–12 non-space chars, not specifically a list label. It rescued 253 oracle lines across the five captures (119 each for the byte-twin pair, 0, 1, 14); examples include `——` and `•`. This is a broader allowance than “list label” and masks leading-token rendering differences; residual risk, though the specified ratio still applies.
- **REGRESS:** token parsing of `LEGS=9/9` and `SUPPLEMENT_LEGS=4/4` matches the r52 output. The delegated r52 counters invoke the tool directly without this round's audit hook; M15 nevertheless passes REGRESS by retaining the native docx path.
- **Sample-size guard:** `--per-leg < 2` returns usage exit 2 and K controls generated-doc counts. At K=2, MALFORMED's parity split exercises one truncation and one sector-shift case. However K does not repair the untested fObfuscated-only branch; ENCRYPTED chooses only fEncrypted or fEncrypted+fObfuscated. Usage exit 2 is shared with ENV_CHANGED (documented as “or usage” in the counter docstring).

## Verification evidence

- Frozen `c1-count.py` and `claims.md` have no diff from freeze `5a1a20630d8176a816a60bb43b0d0e7ee2db19a0`; c1 counter SHA-256 at freeze and worktree: `633430a4f74a404645690da19f3b5907970d2b7ab1eabf62f6cc65643103b8e5`.
- Native counter reproduced: `--seed 7 --per-leg 2` → `LEGS=6/6`, `C1=PASS`.
- Control M8 (leak field code) failed GEN; M12 (duplicate ordinary paragraph) failed GEN; M2b (duplicate anchor) passed 6/6; M1 (ignore fObfuscated) passed 6/6; M15 (ctypes→LibreOffice OLE text, native docx path retained) passed 6/6.
- No tools were installed or updated.

VERDICT: first-falsified the frozen C1 counter; fObfuscated-only refusal, anchor uniqueness, and audit-hook no-spawn enforcement are not fully measured, while the HYPERLINK URL and MALFORMED checks are live.
