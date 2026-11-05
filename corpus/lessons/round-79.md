# Round 79 — the subject copy stops being a textual derivative; the self-assessment counter validates its own repairs

Base `ee70e6df19fe43b1b384166cf5d360c3b99dafe2` (round-78 lane tip, admitted by the non-author
spot-check); prefreeze instruments, controls and repairs
`e2bf2bbb5ca66f06b6571cbcaa15554d1a74a67c`; claims freeze
`b58a02dbc8876dd1ad7647d88ca2c9cb2ae51ff9`. Two claims in
`corpus/evidence/round79/claims.md`: C1 operability (lowest scored non-retired axis, the
historical 3/10 held) and C2 calibration. This round answers the round-78 spot-check's routed
defects 1, 2, 9 and 11 and QUALITY 146–147's successor requirements.

## Gate

- Admit S196, own-work B, scoped to QUALITY 147's successor requirement for the outer battery's
  subject copy. `corpus/QUALITY.md` at `ee70e6df19fe43b1b384166cf5d360c3b99dafe2`, criterion 147
  at line 1056, quote inside its opening requirement sentence. Opened 2026-11-04. Located quote:
  "A subject-identity salt is defeated by any normalizer that knows its marker family, so the
  closure is a per-channel measurement and not a property of the salt" (25 words, `wc -w`).
  Grounds C1's target: it is a requirement produced by round 78's own falsification, not a
  measurement of the successor.
- Admit S197, own-work B, scoped to QUALITY 146's successor requirement for the self-assessment
  counter. `corpus/QUALITY.md` at `ee70e6df19fe43b1b384166cf5d360c3b99dafe2`, criterion 146 at
  line 1054, quote inside its opening requirement sentence. Opened 2026-11-04. Located quote:
  "A self-assessment counter validates each resolution line against the bytes it claims to repair,
  and its audit window covers every block rather than the newest" (24 words). Grounds C2's target.
- Reject S198, own-work C, scoped to a defect receipt offered as a source about verification
  method. `.ufo/waves/round-78/w1/R78ReviewB/atkB2-new-block-window.txt` at
  `3eb4a3cad8febf75698a017cb6c4441f763b3454`, wave file lines 1–20, quote on its finding line.
  Opened 2026-11-04. Located quote: "the audit window is the last `## Round-\d+ addition` block".
  REJECTED: a receipt that demonstrates one counter's false green is that counter's own evidence,
  not a source about how self-assessment should be audited (the S195 class one layer out); flip:
  admit scoped to what a control receipt must carry if an admitted entry ever rests on receipt
  format.
- New registry rows S196/S197 mined, used-by this lesson; S198 rejected, used-by `—`. Existing
  `status`/`recheck`/`used-by` cells unchanged. No URL opened or fetched: all three are
  revision-pinned committed paths.
- Non-author spot-check requested: two admits and one reject above. Dispatched wave seats are
  author-lane evidence, not independent admission or promotion reviewers.
- Assimilation: none. The `merge/chousa/` package stays closed: round 78 measured 111 of 114
  staged ids colliding with the live registry (192 rows), the id drift is not renumbered in
  scratch, and the claim cap was spent on C1/C2. No package bytes, no campaign tool, no shokuknow
  write.
- `considerthese/` holds operator-authored files through 2026-10-26 and was opened; no proposal
  was adopted this round (claim cap), recorded rather than implemented. Nothing there was edited.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| the superseder criterion cited the very absent path it was superseding, so the counter flagged the repair | the first `selfcheck-v2.py` run after the repairs printed `CHECK S2-quality-pointers FAIL … unresolved=['116:corpus/evidence/round59/claims.md', '149:corpus/evidence/round59/claims.md']` — criterion 149 described the defect with the missing path inside backticks, and the pointer audit reads backticked tokens | no criterion: QUALITY 146 requires the superseder's own pointers to resolve, but nothing said the superseded defect's absent path must not be re-quoted as a token | criterion 149 now names the round-59 claims path in prose, never in backticks; re-measured `S2 … unresolved=[]` and `SELFCHECK2=PASS unresolved=0/3` |
| the first all-block pointer measurement reported 18 "unresolved" criteria, 17 of them false | the ad-hoc sweep over `corpus/QUALITY.md` classified `ERRATA=0/11`, `LEGS=20/20`, `QUOTES=10/10` and `tools/` as unresolved paths (`pathlike()` accepted any token containing `/`), and `resolves()` never stripped a trailing slash, so the directory token `tools/` could not resolve | nothing: the counter's own filter is the criterion, and the first filter was written before it was measured | `pathlike()` rejects tokens containing `=`/`*`/`;`, and `resolves()` strips a trailing `/` before the prefix test; re-measured `missing=[116]` (one true defect), and the counter's refusal of the hollow mirror was re-run after the change |
| the three registry rows landed outside the `## Registry` table | the census printed `E12 S196/S197/S198 row outside Registry section` after the rows were appended at end of file (the file continues with `## Paths` and `## Search log`) | the census gate (`E12`) caught it; no lane criterion did | rows re-inserted directly after S195 inside the table; `sources-census.sh validate --root … chousa` re-run to exit 0 (W04 warnings only) |
| the claims file named the wrong class provenance and overstated the counter's reach | `corpus/evidence/round79/claims.md:89-93` says the QUALITY class is "116, plus 102 and 103 which the wider audit also resolves", but the frozen receipt prints `missing=[116]` and 102/103 have no gaps (`R79CriticA/quality-gapdump-head.txt`), and the round-77 routed defect 3 is criterion 142, whose glob pointer `pathlike()` excludes (`R79CriticA` F2) | no criterion: the claims file was written from the first over-reporting sweep and the lesson recorded the correction without the claims file being re-derived | recorded, not amended (the freeze is frozen); QUALITY 151's check now requires the kill rule to enumerate exactly the forgers the predicate counts, and the next freeze re-derives every class from the counter's own `--digests` output |
| a control receipt was measured on the worktree and labelled `REV=worktree` | `corpus/evidence/round79/controls/selfcheck2-after.txt:1` prints `LANE=… REV=worktree`, so the after value is not re-derivable from a pinned revision (`R79CriticA` F8, the round-78 routed defect 9 class) | nothing: no criterion bound a control receipt's revision label to a pinned commit | receipts stay frozen and unamended; the landing re-measures the same command at the landing revision into a new file (`controls/selfcheck2-after-landing.txt`), and the successor rule is that a control receipt names the revision it was measured at |

## Instrument limits (recorded, not amended after scoring)

- **A copy that is not a textual derivative is not thereby unidentified.** A forger that regexes
  the wrapper's base85 literal, decodes it, unmarshals the code object and matches the surviving
  string constants identifies 13/13 subjects (Jaccard 0.50–0.93) and reaches
  `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` at exit 0 without scoring one
  (`.ufo/waves/round-79/w1/R79CriticA/a10-payload-decode.py`, `a10-receipt.txt`; re-run by the L1
  at `BATTERY=PASS … exit 0`). No identifier canonicalisation and no execution is needed, because
  re-emission keeps every string constant.
- **The structure channel is a full forgery of both batteries, not a partial one.** A matrix that
  decodes the payload, canonicalises the identifier table and looks the digest up in a table built
  from the committed subjects prints `BATTERY=PASS forgers_rejected=11/11 positive=2/2
  oracle=REJECTED` at exit 0 on v5 *and* v6
  (`R79ExecC/receipt-v6-structure-matrix.txt`, `receipt-v5-structure-matrix.txt`). A one-integer
  semantic change to a positive scores 0/12, so the matrix is an identity lookup, not an evaluator
  (`R79ExecC/control-semantic-altered-subject.txt`).
- **`a9` is empty in content.** It deletes the wrapper's three fixed lines and hashes the
  remainder, which is the empty string on every v6 copy (`sha256("")`), so its REFUSED verdict is a
  property of the wrapper's line count, not a measurement of the textual channel
  (`R79CriticA/a9-empty-normalisation.txt`).
- **The digest-bearing repair format binds a line to bytes, not to a relation.** A criterion whose
  text is unrelated to 116 but which carries `supersedes: 116 digest=ae134338138ad3e0` resolves 116
  (`R79ReviewB/09-correct-digest-unrelated-superseder-v2.txt`); `correction:`/`erratum:` lines
  naming a currently clean target are never validated (`R79CriticA` F3).
- **`RECEIPT_LINES` exposes an append, not a truncation**, and a same-count in-place rewrite is
  invisible to it — carried unchanged from round 78 (the caller's exit code stays authoritative).
- **Two v6 legs are decorative for the frozen predicate.** `R79MutA`'s table shows `--no-content`
  (M4) and identifier renaming (M6) both leave `FORGE_BATTERY=PASS forgers_handled=6/6
  positive=1/1`; with renaming off, `a8` and `a9` still refuse because the channel that
  identifies a v6 copy is payload decoding (`a10`), not the identifier table. The load-bearing
  legs are the identity mechanism itself (M1 killed), the `RECEIPT_LINES` trailer (M5 killed)
  and the permutation leg (M3 killed, the positive control goes MISS).
- **The toolchain leg maps a missing `cc` to a traceback when `perm` already exists.** With a
  pre-seeded `<work>/perm` and no `cc` on `PATH`, `forge-battery.py` skips the compile guard
  and then calls `cc --version`, raising `FileNotFoundError` — a verdict-shaped exit 1 for an
  environment problem, and a pre-existing permutation binary trusted without recompiling
  (QUALITY 148's own O2 clause). Re-measured by the L1 after `R79SentinelA` reported it
  without a retained receipt; the frozen instrument is not amended.
- **Two seats settled without a retained report.** `R79CriticB` and `R79SentinelA` settled
  with partial output only (`w1-results.json`); the sentinel's one claim was re-measured by
  the L1 above, and the critic's last line names an "annotation-future drift" it never filed
  a receipt for — recorded as unverified, never as evidence (the r77 settlement-attestation
  weakness recurring).
- **The `--work` and toolchain legs are outside the frozen predicate.** `matrix-battery-v6.py`
  creates and deletes only its own run directory and maps setup failures to exit 2;
  `forge-battery.py` maps a missing `cc` to exit 2 with a one-line diagnostic (QUALITY 148). The
  wave's sentinel seat measures them separately; the predicate never exercises those paths.

## Claim outcomes — both frozen kill rules fired

- **C1 (operability): the predicate holds; the kill rule fires.** The frozen predicate line
  reproduces at exit 0 (`controls/forge-battery-after-v6.txt`,
  `FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1`), the before receipt is
  `FORGE_BATTERY=FAIL forgers_handled=5/6 positive=1/1` exit 1 with `a8 … verdict=FORGED`, and the
  derivative measurement goes `13/13 MAX_WINDOW=4096` → `0/13 MAX_WINDOW=23`. But the kill rule's
  clause "if any forger is FORGED" is universal while the predicate enumerates six, and
  `R79CriticA`'s `a10-payload-decode.py` is a seventh forger that reaches the battery's own exact
  target line at exit 0 without scoring a subject. Under the rule's literal words C1 does not
  verify; the claim text and its kill rule name different sets, which is the round-78 routed
  defect 1 shape recurring on a new surface.
- **C2 (calibration): the predicate holds; the kill rule fires.** `controls/selfcheck2-before.txt`
  is `SELFCHECK2=FAIL unresolved=3/3` exit 1 at the base where round 78's counter prints PASS, the
  controls reproduce both round-78 false greens and both refusals
  (`CONTROL=PASS cases=4 v1_false_greens=2/2 v2_refusals=2/2`), and the after receipt is
  `SELFCHECK2=PASS unresolved=0/3` exit 0. But the kill rule names "a newer `## Round-<n>
  addition` block hides an earlier criterion from the audit", and a newer block re-using criterion
  number `116.` overwrites the earlier body in `criteria()` (`out[current] = [line]`), printing
  PASS at exit 0 with criterion 116's live dead pointer present
  (`R79CriticA/selfcheck2-duplicate116-head.txt`, independently `R79ReviewB/05-dupid-v2.txt`). The
  blank-line Gates window and the `class`-cell scanner gap are two further inputs of the same
  class (`R79ReviewB/07-blankwindow-no-repair-v2.txt`, `08-stranded-probes-v2.txt`).
- Neither claim is re-declared or narrowed after data. QUALITY 150 carries the three audit-window
  gaps and 151 the decoding channel and the kill-rule-enumeration rule; the instruments and the
  receipts are what they are. The round's admission is false on the rules declared before data, and
  the report says so.