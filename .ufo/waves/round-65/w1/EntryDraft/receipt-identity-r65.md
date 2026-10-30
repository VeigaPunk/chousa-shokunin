source: S154 — installed git-cat-file(1), /usr/share/man/man1/git-cat-file.1.gz (Git 2.56.0, page dated 2026-09-27, rendered `MANWIDTH=1000 man -l FILE | col -bx`; sha256 8eb0bb079fa0cdf682920d0327fc1e72d5704961c9c54cdc716909251efd5737); S155 — installed module documentation, /usr/lib/python3.14/hashlib.py (Python 3.14.8; sha256 88fa624821fbdee7eb2ef87c2437b207afe328cf117c7463367e2db5eb1af492); S156 — round64 before measurement, corpus/evidence/round64/controls/c1v3-before-full.txt at base d6ed8155e9b4735639a2cf0a3e479c62f2056195 (44 lines; sha256 ca05f579dc0f979a772ecec973a1da5d5df8d11881ca678708c72044f8c9c05b); supplementary S157 — receipt validator reference docstring, corpus/evidence/round65/controls/ref-receipt-pin.py (sha256 0719d7175da072454f514e0eea52b266f66c2246a085f4ea824793f634315fa2)
verified-at: 2026-10-30 (all four file digests recomputed locally this round and matched round65/source-openings.json; every quote below located at the cited line of the rendered page, module file or ledger)
recheck: from the lane root: sha256sum the four pinned paths, re-render S154, and run `python3 corpus/evidence/round65/c2-count.py`; redo on any Git, Python or manual-page upgrade

# Receipt identity: object identity, content digest, reported exit, execution authenticity

Provenance trio first, as opened this round. S154 grounds what `git cat-file` returns for a named object; S155 grounds what a digest covers; S156 is a verdict-bearing receipt file that can be held, hashed and read without any of the runs it reports being attached to it. Quotes are verbatim from the pinned bytes; interpretation is marked [INFERENCE].

## Located quotes

- Q1 | S154 rendered line16 (DESCRIPTION) | Output the contents or other properties such as size, type or delta information of one or more objects.
- Q2 | S154 rendered line26 (OPTIONS, `<object>`) | The name of the object to show.
- Q3 | S154 rendered line159 (OUTPUT) | If <type> is specified, the raw (though uncompressed) contents of the <object> will be returned.
- Q4 | S155 lines31-32 (module documentation) | Return the digest of the bytes passed to the update() method so far as a bytes object.
- Q5 | S156 line1 | LEG CLEAN clean ok ok
- Q6 | S156 line31 | LEG E05 defect FAIL rc=0 want 1
- Q7 | S156 line44 | CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL
- Q8 | S157 module docstring | Validate receipt header consistency, not execution authenticity.

## Claims

Claim 1. The installed manual models retrieval as name-first: `<object>` is defined as "The name of the object to show.", the command's DESCRIPTION is to output "contents or other properties" of objects, and with an explicit type "the raw (though uncompressed) contents of the <object> will be returned". [Q1, Q2, Q3] [INFERENCE] In this interface the object's name is what the manual treats as the object's identity within the repository — retrieval is defined from the name inward — and the SYNOPSIS forms `<rev>:<path|tree-ish>` and `--path=<path|tree-ish> <rev>` select among repository objects, so bytes obtained this way are committed object bytes, independent of any working-tree modifications.

Claim 2. The hashlib module documentation defines `digest()` as returning "the digest of the bytes passed to the update() method so far as a bytes object", with `hexdigest()` as its hexadecimal spelling. [Q4] [INFERENCE] A content digest covers exactly the bytes the caller fed: producer, time and origin are absent from the value, so byte-identical artifacts share one digest, and one digest cannot distinguish a measured artifact from a fabricated byte-copy of it.

Claim 3. S156 is a 44-line ledger: line 1 reads "LEG CLEAN clean ok ok", line 31 records "LEG E05 defect FAIL rc=0 want 1" — a reported exit (rc=0) written next to the expected value — and the last line is the written summary "CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL". [Q5, Q6, Q7] [INFERENCE] Reading and hashing S156 verifies the file — held at sha256 ca05f579…c05b, per the header above — but the exits it reports are tokens in bytes; no process is attached to them, and a recorded rc=0 can sit beside its own refutation ("want 1") in the same pinned text.

Claim 4. The four notions answer different questions: object identity — which stored object does a name select (S154); content digest — which bytes agree (S155); reported exit — what value does the record carry (S156); execution authenticity — did the recorded run occur as recorded. [Q1-Q7] The round65 reference validator's own docstring states "Validate receipt header consistency, not execution authenticity.", and SOURCES row S157 registers that intent text as rejected as execution proof. [Q8] [INFERENCE] A receipt whose bytes hash correctly is authentic as an artifact and may still be false as testimony; consistency checking and authenticity checking are different obligations.

## Limits

- Ground: one host, one git (2.56.0-1, page dated 2026-09-27), one Python (3.14.8). Upgrades can change wording or behavior; the recheck line above is the renewal path.
- S154 defers object-name spelling to gitrevisions(7), which was not opened this round; nothing here states how object names are computed or which hash algorithms can name objects. [INFERENCE] Any statement that a git object name is itself a hash of header-plus-content is outside this entry's opened ground.
- hashlib.py is the interface module; the compression functions live in extension modules not opened here, so the documentation pins interface semantics, not implementation. Digest collision-resistance is assumed, never established by an opened source.
- Transcription delta: round65/source-openings.json registers Q3 as "contents of the object will be returned", dropping the literal `<object>` token that the rendered page and the roff source carry; the verbatim form is cited above and the registered file digest still matches.
- The R65-C2 counter (corpus/evidence/round65/c2-count.py) checks ten textual presences: six in this entry, one in corpus/SOURCES.md rows S154-S156, one in a corpus/README.md index line, plus the two headings. 10/10 is a presence result, not entailment; a boilerplate entry could pass it, per the frozen claims.
- Working-tree state at drafting: at base d6ed8155 the entry file and the round65 evidence directory do not exist (`git -C <lane> ls-tree d6ed8155`); the current working tree already carries an uncommitted preliminary entry (untracked), SOURCES.md rows S154-S157 and a README index line (both modified), under which the counter reads ENTRY_CHECKS=10/10 C2=PASS, exit0 (observed 2026-10-30). The frozen before-control ENTRY_CHECKS=0/10 describes the base, not the current tree.
- This entry asserts nothing about cryptographic execution authentication; that limitation belongs to R65-C1 equally. No working-tree file is hashed into any receipt identity discussed here; the digests cited are over the pinned source files themselves.
