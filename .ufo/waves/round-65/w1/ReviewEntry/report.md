# ReviewEntry — C2 assertion review from direct source openings

Seat: ReviewEntry (reviewer, lane chousa round65, leaf — no subagent dispatch).
Freeze under review: f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd (lane HEAD confirmed at freeze).
Object: claim C2 and the proposed knowledge entry corpus/knowledge/receipt-identity-r65.md.
Method: opened the three pinned sources directly in this seat; recomputed sha256 of each and
compared to corpus/evidence/round65/source-openings.json. No draft from any seat was used as
evidence. No production writes, no git/jj mutations, no network. One isolated probe: the frozen
structural counter run once, informational only (L1 integration verification is the authority).

## 1. Source-opening verification (all three admissions confirmed)

| Source | Frozen sha256 (source-openings.json) | Recomputed sha256 (this seat) | Match |
|---|---|---|---|
| S154 /usr/share/man/man1/git-cat-file.1.gz | 8eb0bb079fa0cdf682920d0327fc1e72d5704961c9c54cdc716909251efd5737 | 8eb0bb079fa0cdf682920d0327fc1e72d5704961c9c54cdc716909251efd5737 | YES |
| S155 /usr/lib/python3.14/hashlib.py | 88fa624821fbdee7eb2ef87c2437b207afe328cf117c7463367e2db5eb1af492 | 88fa624821fbdee7eb2ef87c2437b207afe328cf117c7463367e2db5eb1af492 | YES |
| S156 corpus/evidence/round64/controls/c1v3-before-full.txt | ca05f579dc0f979a772ecec973a1da5d5df8d11881ca678708c72044f8c9c05b | ca05f579dc0f979a772ecec973a1da5d5df8d11881ca678708c72044f8c9c05b | YES |

Quote and placement checks against the opened bytes:

- S154: extracted man page line 505 reads "If <type> is specified, the raw (though
  uncompressed) contents of the <object> will be returned." It sits between `.SH "OUTPUT"`
  (line 495) and `.SH "BATCH OUTPUT"` (line 506) — the entry's "under OUTPUT" placement is
  exact. Man-page header lines confirm "Source: Git 2.56.0", "Date: 2026-09-27"; installed
  `git --version` is 2.56.0. Matches SOURCES.md row 164's metadata.
- S155: lines 31–32 read "- digest(): Return the digest of the bytes passed to the update()
  method / so far as a bytes object." — the frozen quote is exact. Lines 33–34 describe
  hexdigest as a string of double length containing only hexadecimal digits. Entry's
  "lines 27–34" window and "Python 3.14.8" match (installed python3 is 3.14.8).
- S156: line 1 is exactly "LEG CLEAN clean ok ok"; the file ends with
  "CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL"; a grep for
  ^(REVISION|EXIT|SHA256)= over the 44-line file returns nothing (exit 1). Matches the
  entry's observation and the "lines1–44" span in SOURCES.md row 166. Round64 claims.md
  line 267 documents this receipt's outside provenance ("exit 1, committed at or before the
  freeze"), corroborating the entry's caveat that provenance exists outside the file.

Auxiliary check on validator behavior the entry describes: corpus/evidence/round65/controls/
ref-receipt-pin.py line 21 runs `git -C <root> cat-file blob <revision>:<path>` and compares
`hashlib.sha256(q.stdout).hexdigest()` to the declared digest — the entry's description of
"type `blob` at the caller's full revision plus repository-relative path" is the literal
implementation. The receipt body (after the blank separator) is checked only for nonemptiness;
it is never hashed.

Isolated probe (informational): `python3 -B corpus/evidence/round65/c2-count.py` prints
ENTRY_CHECKS=10/10 C2=PASS, exit 0, on the current tree. This seat did not run any battery.

## 2. Admissible claim sentences (admit candidates)

A1. Object-content selection (S154 + implementation description).
    Sentence: "Specifying a type makes git cat-file return the raw contents of the named
    object; the round65 validator names blob at <full-revision>:<repo-relative-path>, so the
    checked bytes are committed object bytes selected by revision and path."
    Reason admitted: the quote is verbatim and section-placement-exact; the validator line
    exists as cited. The further half "not the current working tree" is admitted ONLY as the
    entry's explicitly labeled Inference — the man page itself never mentions the working
    tree; the exclusion rests on Git's object model, which is standard background knowledge,
    not on the quoted sentence.

A2. Content-digest binding, hash assumption scoped (S155).
    Sentence: "A matching SHA256 binds the reported digest to the selected blob bytes under
    the hash assumption; it identifies content, not an actor."
    Reason admitted: digest()/hexdigest() quotes are exact at lines 31–34; equality of
    digests over identical bytes is the documented contract. "Not an actor" is a scoped
    inference — the documented contract is bytes→digest only — and the entry scopes it with
    "under the hash assumption" (collision/preimage resistance assumed, not established by
    the source).

A3. Round64 before-receipt header shape (S156).
    Sentence: "The round64 before receipt begins 'LEG CLEAN clean ok ok', ends with a
    BATTERY=FAIL summary, and carries no self-contained REVISION=/EXIT=/SHA256= header
    lines; provenance for it lives in the round64 claims file."
    Reason admitted: every clause verified directly against the opened file (line 1, tail
    summary, header grep empty, 44-line span); the round64 claims file reference was
    confirmed at line 267.

A4. Distinction synthesis (S154+S155+S156 combined, labeled inference).
    Sentence: "Revision identity, blob-content digest, and reported child exit answer
    different questions; the validator's own exit0 certifies header/blob consistency only,
    not that the measured command passed."
    Reason admitted: each premise is one of A1–A3; the exit semantics (0 consistent / 1
    inconsistent / 2 usage) match the reference docstring. The entry uses the docstring
    (S157) descriptively; S157 remains REJECTED as claim support in SOURCES.md, and this
    sentence does not elevate it.

## 3. Overreach refusals (reject candidates)

R1. REFUSED: "The ten-check structural counter (or this entry passing it) establishes the
    lesson / proves entailment." The counter is startswith/substring/index presence only;
    claims.md itself states it "cannot establish entailment" and that a boilerplate entry
    could pass. Structural pass is necessary, not sufficient, for the semantics.

R2. REFUSED: "S156 shows the round64 battery receipt had no provenance." The source supports
    only absence of in-file headers; round64 claims.md line 267 documents surrounding
    provenance. The naked sentence overreaches the observation; the entry's own wording is
    correctly bounded.

R3. REFUSED: "git cat-file output is authentic/trustworthy repository content (no
    replacement or configuration risk)." The OUTPUT quote is silent on trust; the CAVEATS
    section (extracted lines 719–725) covers remote-object-info placeholders, disk-size
    reporting, and duplicate object copies — none of it content authenticity. Replacement /
    configuration trust is an assumption the entry's Limits file correctly, but no source
    here supports any authenticity claim.

R4. REFUSED: "The round65 receipt format proves execution authenticity / that the measured
    command truly ran." Refuted by construction: the reference validator never hashes the
    body, so replaying a valid header with fabricated output passes. Entry Limits state
    exactly this; any affirmative authenticity sentence is inadmissible on these sources.

R5. REFUSED: "hashlib's digest() provides provenance or authenticity." The documented
    contract is bytes→digest only; upgrading it is unsupported. (The entry does not make
    this upgrade; recorded to fence the boundary.)

## 4. Independence statement

This seat opened all three pinned sources itself and recomputed their digests against the
frozen source-openings.json; every quote above was read from the opened bytes in this
session. The review is from source openings, not from any sibling's draft. Reviewer seat,
lane chousa round65; no subagent dispatch, no production writes, no fleet/sibling/source-tree
writes, no network, no git/jj mutations (read-only `git -C` only, to confirm HEAD at the
freeze). The admissible/rejected split above is a recommendation to L1, not an admission.

## 5. Residual risk and verification gaps

- A1's "not the working tree" half leans on general Git object-model knowledge; the man page
  sentence alone does not state the exclusion. Mitigation in place: the entry labels it
  "Inference". Accepted with that label; a stricter freeze could demand an explicit source
  for the exclusion.
- Replace-refs/alternates behavior of git cat-file was not verified against gitrevisions(7);
  the entry's Limits list it as a trust assumption, which is honest but unexhausted.
- S156 is 44 lines of case output; the header-absence observation was verified by pattern
  grep only, not by a frozen shape oracle.
- Counter state 10/10 PASS observed once, informational; canonical verification belongs to
  L1 after integration. tools/receipt-pin.py (the C1 acquisition target) does not exist yet
  at freeze time — consistent with C1, not a C2 defect.

Tool installs: none (all checks used preinstalled python3 3.14.8, git 2.56.0, coreutils sha256sum).
