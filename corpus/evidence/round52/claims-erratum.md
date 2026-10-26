# Round 52 — claims erratum (post-freeze disclosures)

The frozen predicates, counters (`c1-count.py`, `c2-count.py`, `build-spans.py`), controls and targets in
`corpus/evidence/round52/claims.md` (freeze `37468eadd8d098e80289b2f31a22de3872d4a1f6`) are unchanged after the
freeze. What changed or was found after seats scored:

- **E1 — C1 supplement (post-freeze, not the claim's rule).** W1 `R52CritForgeC1` passed the frozen counter
  `LEGS=9/9` with an 85-line regex tool keyed to the generators' XML spelling and a REAL stub of 21 characters
  (`controls/forge-shape.py`, copied verbatim from the seat's report). `c1-supplement.py` re-spells the same
  generated documents (random namespace prefixes, `w:` as the default namespace, shuffled rels attributes,
  comments, CDATA, decimal references, paired and typed `w:tab`/`w:br`) and pins the NIPH text form's sha256
  (`754aae42…`, computed from the independent reader `build-spans.py` `docx_text`). The frozen counter's verdict
  stands as measured; the supplement is reported beside it, never instead of it.
- **E2 — tool changes after the candidate `804a4537` (outside the frozen predicate).** (a) A main part whose
  root is not `w:document` is refused (W1 `R52ExecRealDocx`: two `.xlsx` and an OLE `.doc` with an embedded
  OPC zip printed an empty text form at exit 0); (b) `_rels/.rels` or a main part inflating past 256 MiB is
  refused and `MemoryError` maps to a refusal (W1 `R52SentCapture` H1); (c) an officeDocument target that
  normalises outside the package root is refused (H3, cosmetic: the candidate read only zip members);
  (d) `el.clear()` after each end event. These add refusal classes the frozen sentence does not list; the
  sentence's own refusal classes and every other behaviour are unchanged, and no frozen leg exercises the
  new ones (the counter generates only `w:document` parts under 1 MiB).
- **E3 — named, not changed: the two readers diverge on an External officeDocument relationship listed
  first.** `build-spans.py` `docx_text` takes the first relationship whose Type ends in `/officeDocument`
  regardless of `TargetMode`, then falls back to the UTF-16LE form; the tool skips External relationships
  (W1 `R52CritSeparable`, `R52ExecFormDiff`). No C2 capture has an External relationship; the frozen
  builder is left as frozen.
- **E4 — named limits of the frozen C2 counter (W1 `R52CritForgeC2`).** A scratch root with boilerplate quotes,
  one quote reused per id, one anchor offset and a refused NIPH passes `C2=PASS`; so does a NIPH span cut from
  the `.txt` sidecar's zip bytes (`[Content_Types].xml`), because a span's digest may name the sidecar. The
  counter measures binding and presence; substance and entailment are the closure's, as the claim says.
