# W2ScoutProvince — Memento version-anchor note vs chousa province

**Verdict: in province.** A Memento version-anchor note is inside this lane's province. `PROVINCE.md` does not name Memento, RFC 7089, or version-anchor. The production entry is absent. The yes is a scope judgment, not a claim that the note has already been absorbed.

Axes used: operability (one yes/no a later seat can apply), calibration (in-scope method vs the live-fetch refuse; not a C3 score), depth (the note identified against the capture, not against the word Memento alone).

## Scope sentence used

From `/home/vgpnk/Projects/shokunin/chousa-shokunin/PROVINCE.md` lines 5–8, the Owns sentence:

> **Owns:** question framing; source hierarchy (primary / secondary / aggregator / unsourced); citation chaining and hop resolution; claim-vs-source verification; search-strategy taxonomy; the external-target approval table for a research window; this lane's own corpus and gates.

The coarser Domain line (line 3) is the lane label, not the deciding sentence: "deep-research method (調査) — the reusable craft of source research."

## What the note is

The note this round means is a knowledge entry that binds a citation to a timestamped prior state, and says where that binding stops. The frozen C3 path is `corpus/knowledge/citation-version-binding-r36.md` (`corpus/evidence/round44/c3-count.py` lines 24–30; `corpus/evidence/round44/claims.md` lines 77–81). A draft of that entry exists at `.ufo/waves/round-44/assimilation/draft/citation-version-binding-r36.md`. Its title is "Binding a citation to a prior state, and where that binding stops." Its ground line says the lane's byte-span check does not date a prior state, and that this entry is that missing half, opened from a committed capture.

That object is citation chaining and claim-vs-source verification, stored in this lane's own corpus. Those are Owns items. It is not bounty scope (kasegi), not a model-quality claim (kengaku), not orchestration or agent lifecycle (kumitate), and it records no secret value (kagi).

The capture the draft cites was read locally, not fetched. Contiguous text at `d0c4a09a9de32cb91d5e3797.txt` lines 380–382:

> The presence of a "Memento-Datetime" header and associated value for a given response constitutes a promise that the resource state reflected in the response will no longer change (see Section 4.5.6).

That header is the version anchor: a datetime promise about a prior resource state, not a byte hash and not a live TimeGate. This is not the fixture token "Memento-Skills" (Zhou et al.) in `corpus/fixtures/`.

## Bound, not absorbed

The same file's Refuses sentence (lines 10–15) still applies. The clause that bounds this yes:

> external live-target research without operator approval (loopback-only otherwise)

The draft itself says no live TimeGate was opened and that the fetch-scope ruling is open. Opening a TimeGate against an external archive is not licensed by this verdict. Closing rule, line 17: "Out of province → report, never absorb."

Sibling provinces do not claim the topic by name. `kumitate-shokunin/PROVINCE.md` line 27 routes "Research method → chousa." `kake-shokunin/PROVINCE.md` lines 36–37: "chousa owns research method and source hierarchy; kake keeps only domain findings and its own corpus/SOURCES.md rows." Operating a web archive or a publishing host would be kake. This note does not do that.

## Checks quoted

`rg` on this lane's `PROVINCE.md` for `Memento|RFC 7089|version-anchor|version anchor`: no lines, `province_rg_exit=1`.

The same pattern on `/home/vgpnk/Projects/shokunin/*/PROVINCE.md`: no lines, `sibling_rg_exit=1`.

`test -f corpus/knowledge/citation-version-binding-r36.md`: `ABSENT`.

`rg` for a row-start `S079` in production `corpus/SOURCES.md`: no match. The staged validate copy at `.ufo/waves/round-44/assimilation/validate/corpus/SOURCES.md` line 252 already teaches "binding a citation to a timestamped prior state" for RFC 7089. That row is not production.

## Not claimed

Byte offset of the quote was not measured here. C3 was not run. Freshness was not scored. No production file, sibling file, git index, or jj state was edited. No fetch.
