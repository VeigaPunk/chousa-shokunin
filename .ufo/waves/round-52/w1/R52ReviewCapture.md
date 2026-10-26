# R52ReviewCapture — line review of tools/capture-text.py vs frozen R52-C1

Target: commit `804a45370dc992bfe714817281535055c2f9b032` (frozen copy saved in scratch,
sha256 `3986a9715328175d02639dcd1016ffaa12e80607f0f427ed07628fcaf18dcdd1`, git blob
`07401e12f0e953e7b62aa054b14f663c5d31e389`). Predicate: `corpus/evidence/round52/claims.md:28-47`.
No LSP server/device is mounted for this seat — review is source-read plus executed
reproductions (text grep used only as literal fallback, per role note).

## 0. Worktree drift (disclosure, flag to orchestrator)

The worktree file changed TWICE under this review, uncommitted (`git status`: ` M tools/capture-text.py`):
S1 = 804a453 bytes (115 ln) → S2 added `w:document` root check + `el.clear()` (120 ln) →
S3 added `MAX_PART=256MiB`, `bounded()`, target-root guard, `except MemoryError` (diff vs 804a453: 34 ln at read time).
Current worktree sha256 at report time: `8e1ac6e4ebdeac748212944660557a6cbfd072582be477921ad77f7b31ccb638`.
Frozen claims say the candidate "landed at 804a453"; adopter receipts must pin WHICH bytes were counted.
All repros below were executed against BOTH the saved frozen copy and the worktree state present at run time;
each result labels which.

## 1. Frozen predicate behaviors VERIFIED (repros in §3 script)

| Predicate clause (claims.md line) | Result |
|---|---|
| main part from `_rels/.rels` officeDocument rel (32-33) | OK — b6: External rel first, internal second → internal used, exit 0; REAL NIPH: rId1 `word/document.xml` selected among 4 rels |
| leading `/` stripped (33) | OK — b1 target `/word/document.xml` → text form, exit 0 |
| Target `..` resolved (spec ask) | OK — b2 `word/../word/document.xml` → normpath, exit 0; escaping `../etc/...` refused exit 2 |
| `w:t` text, entities decoded (34-35) | OK — bundle A: `A&amp;B&#65;&#x43;` → `A&BAC` exact |
| `w:tab`/`w:br`/`w:cr` under `w:r` → `\t\n\n` (35-36) | OK — `one\ttwo` + two `\n` in bundle A |
| every `w:p` end `\n`, nested incl. (37) | OK — table cell, textbox, direct `<w:p><w:p>…` → `a\nb\n` (two ends, two newlines) |
| `mc:Fallback` emits nothing, Choice kept (37-38) | OK — `box` emitted, `NOPE`/`NESTED` (nested Fallback) absent |
| `w:delText`/`w:instrText`/`w:pPr/w:tabs` dropped (38-39) | OK — `keep` only; no tab from `<w:tabs><w:tab …/>` |
| UTF-8 stdout, code-point offsets (31, 41) | OK — NIPH: 19682 cps → 48936 raw bytes; `--locate 'tail\n'` offset=44 (code points) vs 52 bytes — code-point proof |
| `--locate` line, exit 0 iff n==1 else 1 (40-42) | OK — count=11→offset 5 exit 1; count=0→-1 exit 1; count=1→exit 0; on refusal exit 2, stdout empty |
| refuse: not a zip / no officeDocument rel / missing target (42-44) | OK — exit 2, `REFUSED` stderr, stdout empty in every case (incl. empty `<Relationships/>`, wrong-ns rels, External-only rel) |
| REAL leg (46-47) | OK — sha256 of `…qcache/3a8b45977cd111e45e3980a5.raw` = `16fc8c55…`; text form 19682 cps; `SRにおける文献検索期間について明記する` count=1 offset=8996; `--locate` agrees; `c1-count.py` = `LEGS=9/9 C1=PASS` exit 0 (one reviewer run, TMPDIR in scratch) |

## 2. Defects

### D1 (high) — encrypted main part: uncaught `RuntimeError`, exit 1 + traceback
`text_form`'s handler (804a453 line 98) catches `(BadZipFile, ET.ParseError, OSError)` only; `zipfile`
raises `RuntimeError` for an encrypted member. Violates the docstring exit contract (exit 2 + `REFUSED`
stderr + empty stdout for an unreadable package). S3's diff leaves that tuple unchanged → persists.
Repro (frozen copy): build `fx/a.docx`, set flag bit 0 on `word/document.xml` local+central headers → `fx/enc.docx`.
```
$ python3 $S/capture-text-old.py $S/fx/enc.docx
exit= 1 | stdout= b'' | stderr_last= RuntimeError: File 'word/document.xml' is encrypted,
password required for extraction | traceback: True
```
Same on worktree S2 (driver run: `c2_encrypted_main exit= 1 … traceback: True`).

### D2 (medium) — ISO 29500 **Strict**-namespace .docx: silent empty text at 804a453
All matching is pinned to the transitional namespace `…wordprocessingml/2006/main`; a Strict capture
(`purl.oclc.org/ooxml/wordprocessingml/2006/main`) matches nothing. At 804a453 there is no root check →
**exit 0, empty stdout, no refusal** (silent wrong form). Worktree S2/S3 refuses exit 2 "not
WordprocessingML" — honest, but still not the predicate's text form of a WordprocessingML capture.
```
o3_strict     OLD804a453 exit=0 out=b'' err=''
o3_strict     WORKTREE   exit=2 out=b'' err="REFUSED main part 'word/document.xml' is not WordprocessingM"
```
The C1 generator only emits transitional, so no leg catches this; pinned capture is transitional (verified).

### D3 (low) — first dangling internal officeDocument rel aborts the search
`main_part` raises inside the loop (line 63) instead of trying the next matching rel: a package whose
FIRST officeDocument rel dangles but whose SECOND is valid is refused although a usable main part exists.
```
b7_dangling_1st  exit=2 out=b'' err="REFUSED officeDocument target 'word/absent.xml' is not in the packag"
```
Same on both witnessed versions. Counter `MAIN_PART` decoys are non-officeDocument rels, so this ordering is untested.

### D4 (low) — relationship Target percent-encoding never decoded
OPC targets are URI-quoted; the tool compares the quoted string against raw zip member names.
```
b4_pct20  exit=2 out=b'' err="REFUSED officeDocument target 'word/na%20me.xml' is not in the packa"
```
(member `word/na me.xml`). Latent: the pinned NIPH rels contain no `%` (verified: `percent-enc in rels: False`).

### D5 (medium-low) — huge main part unbounded at 804a453
No size guard at the frozen candidate; a shrink/zip-bomb-shaped part renders with large RSS (measured:
25 MiB single `w:t` → 92 MiB child maxrss on 804a453; 139 MiB on worktree S2 which already had
`el.clear()`; amplification is out/join/encode copies plus tree). OOM would exit 137/SIGKILL — outside
the documented exit set. Worktree S3 adds `MAX_PART` (256 MiB) + `MemoryError` → `REFUSED`, fixing this in flight.
```
exit=0 chars=26214453 wall=0.10s child_maxrss=92 MiB (part 25 MiB)   # frozen copy
```

### D6 (low) — `--locate ''` reports count=0 for a quote that occurs len(text) times
Guard `n = text.count(a.locate) if a.locate else 0` forces count=0/offset=-1/exit 1. Deterministic and
inside the exit-1 branch, but semantically false and undocumented (docstring defines only 0/2+/1).
```
quote=''  exit=1 line=LOCATED count=0 offset=-1 | truth count=50 find=0
```

### D7 (low) — `w:t` with a child element silently loses text after the child
`el.text` at end event only; schema-invalid input (`CT_Text` is simple content) but parser-visible:
```
o6_wtchild  OLD804a453 exit=0 out=b'x\n'    # <w:t>x<w:b/>y</w:t> → "x", "y" lost
```

### D8 (trivial) — S3 nits
`target.startswith("/")` is dead (target is `lstrip`ed + normpathed first); External-only officeDocument
rel refuses as "no officeDocument relationship" though one exists (b5, behavior correct, message
inexact); multiple valid internal rels → first wins silently.

## 3. Reproduction script (scratch driver, outputs quoted above)

Fenced for the L1; run with `TMPDIR=$S`. Fixtures are stdlib `zipfile` packages
(`[Content_Types].xml`, `_rels/.rels`, `word/document.xml` unless stated). Key cases (label → construction):
a=13-paragraph bundle incl. AlternateContent/Fallback/nested-Fallback/table/CJK; b1/b2/b3=Target `/…`,
`../` inside, `../` escaping; b4=Target `na%20me.xml` vs member `na me.xml`; b5/b6=TargetMode External
only / first; b7=two internal rels, first dangling; b8/b10=no/missing target; b9=wrong rel Type;
b11/b12=main part not XML / XML-but-HTML; enc=flag-bit-0 patched `a.docx` (both headers);
o1–o7 per §1/§2; big=25 MiB `w:t`. Locator matrix: `--locate` over `文献検索/one/A&BC/''/'\n'/neverpresent/tail\n`.
Driver verbatim is ~120 lines; per Evidence rule every cited output is pasted above and all
fixtures were generated at run time in `$S/fx/` (removed with the scratch).

## 4. Line map (804a453, 115 lines) — coverage

2-32 docstring: form rules match behavior; exit contract broken by D1; strict-ns silent (D2); no size bound (D5).
42-46 constants: namespace URIs correct; `RUN_BREAKS` map correct.
51-64 `main_part`: KeyError/ParseError refusal ✓; Type case-sensitive ✓; TargetMode External skipped ✓
(lowercase `external` treated internal — lenient on schema-invalid input, o5); normpath+lstrip ✓;
dangling-first abort = D3; no percent-decode = D4; no bound = D5 (S3 adds it).
66-98 `text_form`: is_zipfile gate ✓; iterparse stack push/pop balanced ✓ (no pop-under possible on
well-formed input; malformed → ParseError → REFUSED); fallback counter nested-safe ✓; breaks only when
`stack[-1]==w:r` and not in fallback ✓; every `w:p` end `\n` ✓; `w:t` = `el.text or ""` (D7); handler
tuple misses RuntimeError/MemoryError (D1, D5) — S3 adds MemoryError only.
100-113 `main`: usage exit 2 ✓ (no-args/`--locate` missing value/missing file all measured exit 2);
Refused → `REFUSED` stderr + exit 2 + empty stdout ✓; stdout via `buffer.write` UTF-8 ✓ (locale-safe);
locate guard = D6; exit `n==1` ✓.

## 5. Residual risk / verification gaps

- Worktree kept moving during review; S3+ states after sha `8e1ac6e4…` were not re-tested (except where
  the 34-line diff is itself the evidence, e.g. RuntimeError tuple unchanged).
- Did not test zip shuffling/zip64/data-descriptor shapes, nor non-UTF-8 zip member-name encodings.
- Did not audit C2/spans or the counter's generator (out of seat scope); counter run once as context, 9/9.
- Strict-OOXML and encrypted captures are realistic but absent from every C1 leg — C1 can stay 9/9 while
  D1/D2 hold; that is inherent to the frozen predicate's leg list, not a counting error.
- Scratch `/fast/scratch/hyaku/chousa-r52/R52ReviewCapture/` removed after this report; all cited
  receipts are pasted above verbatim.
